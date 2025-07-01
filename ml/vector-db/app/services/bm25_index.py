import os
import pickle
from typing import List, Tuple, Optional, Dict

from .document import Document
from .embedder.bm25 import BM25Embedder


class BM25Index:
    """BM25-based document index for text retrieval."""

    def __init__(
        self,
        k1: float = 1.2,
        b: float = 0.75,
        epsilon: float = 0.25,
        index_path: Optional[str] = None
    ):
        """
        Initialize BM25 index.

        Args:
            k1: BM25 k1 parameter (term frequency saturation)
            b: BM25 b parameter (length normalization)
            epsilon: BM25 epsilon parameter (IDF floor)
            index_path: Path to save/load index
        """
        self.k1 = k1
        self.b = b
        self.epsilon = epsilon
        self.index_path = index_path

        # Initialize BM25 embedder
        self.bm25 = BM25Embedder(k1=k1, b=b, epsilon=epsilon)

        # Document storage
        self.documents: Dict[str, Document] = {}
        self.id_to_index: Dict[str, int] = {}
        self.index_to_id: Dict[int, str] = {}
        self._next_index: int = 0

        # Load existing index if path exists
        if self.index_path and os.path.exists(f"{self.index_path}.bm25"):
            self.load(self.index_path)

    def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents to the BM25 index.

        Args:
            documents: List of documents to add
        """
        # Store documents first
        for doc in documents:
            if not doc.content:
                raise ValueError(f"Document {doc.id} doesn't have content")
            
            # Store document
            self.documents[str(doc.id)] = doc
            self.id_to_index[doc.id] = self._next_index
            self.index_to_id[self._next_index] = doc.id
            self._next_index += 1

        # Rebuild corpus and mappings to ensure consistency
        self._rebuild_corpus()

    def _rebuild_corpus(self) -> None:
        """Rebuild the BM25 corpus and maintain consistent document mappings."""
        # Reset mappings
        self.id_to_index = {}
        self.index_to_id = {}
        
        # Rebuild in consistent order (sorted by document ID for reproducibility)
        sorted_docs = sorted(self.documents.items())
        all_contents = []
        
        for idx, (doc_id, doc) in enumerate(sorted_docs):
            all_contents.append(doc.content)
            self.id_to_index[doc_id] = idx
            self.index_to_id[idx] = doc_id
        
        # Update next index
        self._next_index = len(self.documents)
        
        # Fit BM25 model with ordered contents
        self.bm25.fit(all_contents)

    def search(
        self, 
        query_text: str, 
        k: int = 5, 
        **kwargs
    ) -> Tuple[List[float], List[Document]]:
        """
        Search for similar documents using BM25.

        Args:
            query_text: Query text to search for
            k: Number of results to return
            **kwargs: Additional parameters (unused for BM25)

        Returns:
            Tuple containing:
            - List of BM25 scores
            - List of matching documents
        """
        if not self.documents:
            return [], []

        # Get BM25 scores for query
        results = self.bm25.search(query_text, k=min(k, len(self.documents)))
        
        scores = []
        documents = []
        
        for doc_idx, score in results:
            if doc_idx < len(self.bm25.corpus):
                # Find document by corpus position
                doc_id = self.index_to_id.get(doc_idx)
                if doc_id and doc_id in self.documents:
                    scores.append(score)
                    documents.append(self.documents[doc_id])
                else:
                    # Fallback: create empty document
                    scores.append(score)
                    documents.append(Document(id=None, content="", metadata={}))

        return scores, documents

    def get_document(self, doc_id: str) -> Optional[Document]:
        """Get document by ID."""
        return self.documents.get(doc_id)

    def save(self, path: str) -> None:
        """
        Save the BM25 index to disk.

        Args:
            path: Path to save the index
        """
        data = {
            "bm25_state": {
                "k1": self.bm25.k1,
                "b": self.bm25.b,
                "epsilon": self.bm25.epsilon,
                "corpus": self.bm25.corpus,
                "doc_tokens": self.bm25.doc_tokens,
                "doc_lengths": self.bm25.doc_lengths,
                "avg_doc_length": self.bm25.avg_doc_length,
                "doc_freqs": dict(self.bm25.doc_freqs),
                "idf_scores": self.bm25.idf_scores,
                "num_docs": self.bm25.num_docs,
            },
            "documents": self.documents,
            "id_to_index": self.id_to_index,
            "index_to_id": self.index_to_id,
            "next_index": self._next_index,
        }

        with open(f"{path}.bm25", "wb") as f:
            pickle.dump(data, f)

    def load(self, path: str) -> None:
        """
        Load the BM25 index from disk.

        Args:
            path: Path to load the index from
        """
        with open(f"{path}.bm25", "rb") as f:
            data = pickle.load(f)

        # Restore BM25 state
        bm25_state = data["bm25_state"]
        self.bm25.k1 = bm25_state["k1"]
        self.bm25.b = bm25_state["b"]
        self.bm25.epsilon = bm25_state["epsilon"]
        self.bm25.corpus = bm25_state["corpus"]
        self.bm25.doc_tokens = bm25_state["doc_tokens"]
        self.bm25.doc_lengths = bm25_state["doc_lengths"]
        self.bm25.avg_doc_length = bm25_state["avg_doc_length"]
        self.bm25.doc_freqs = bm25_state["doc_freqs"]
        self.bm25.idf_scores = bm25_state["idf_scores"]
        self.bm25.num_docs = bm25_state["num_docs"]

        # Restore document storage
        self.documents = data["documents"]
        self.id_to_index = data["id_to_index"]
        self.index_to_id = data["index_to_id"]
        self._next_index = data["next_index"]

    def get_stats(self) -> Dict:
        """Get index statistics."""
        return {
            "num_documents": len(self.documents),
            "vocabulary_size": self.bm25.get_vocabulary_size(),
            "avg_doc_length": self.bm25.avg_doc_length,
            "k1": self.bm25.k1,
            "b": self.bm25.b,
            "epsilon": self.bm25.epsilon,
        } 