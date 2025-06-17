import os
import pickle
from typing import List, Tuple, Optional, Dict

import faiss
import numpy as np

from .config import VectorDBConfig, DistanceMetric
from .document import Document
from .indices import IndexFactory


class VectorDB:
    """Vector database implementation using FAISS with document storage."""

    def __init__(self, config: VectorDBConfig) -> None:
        """
        Initialize vector database.

        Args:
            config (VectorDBConfig): Configuration for the vector database
        """
        self.config: VectorDBConfig = config
        self.dimension: int = config.dimension
        self.index: faiss.Index = IndexFactory.create_index(config)

        # Document storage
        self.documents: Dict[str, Document] = {}
        self.id_to_index: Dict[str, int] = {}
        self.index_to_id: Dict[int, str] = {}
        self._next_index: int = 0

        if config.index_path and os.path.exists(f"{config.index_path}.index"):
            self.load(config.index_path)

    def _normalize_vectors(self, vectors: np.ndarray) -> np.ndarray:
        """Normalize vectors for cosine similarity."""
        if self.config.distance_metric == DistanceMetric.COSINE:
            norms = np.linalg.norm(vectors, axis=1, keepdims=True)
            return vectors / (norms + 1e-8)
        return vectors

    def _requires_training(self) -> bool:
        """Check if index requires training."""
        return hasattr(self.index, "is_trained") and not self.index.is_trained

    def train(self, vectors: np.ndarray) -> None:
        """
        Train the index with vectors.

        Args:
            vectors (np.ndarray): Training vectors of shape (n, dimension)
        """
        if self._requires_training():
            normalized_vectors = self._normalize_vectors(vectors)
            self.index.train(normalized_vectors)

    def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents to the database.

        Args:
            documents (List[Document]): Documents to add
        """
        vectors: List[np.ndarray] = []

        for doc in documents:
            if doc.vector is None:
                raise ValueError(f"Document {doc.id} doesn't have a vector")

            if doc.vector.shape[0] != self.dimension:
                raise ValueError(
                    f"Vector dimension {doc.vector.shape[0]} doesn't match "
                    f"expected dimension {self.dimension}"
                )

            vectors.append(doc.vector)

            # Store document
            self.documents[doc.id] = doc
            self.id_to_index[doc.id] = self._next_index
            self.index_to_id[self._next_index] = doc.id
            self._next_index += 1

        vectors_array = np.array(vectors).astype("float32")

        # Train if necessary
        if self._requires_training():
            self.train(vectors_array)

        # Add vectors to index
        normalized_vectors = self._normalize_vectors(vectors_array)
        self.index.add(normalized_vectors)

    def search(
        self, query_vector: np.ndarray, k: int = 5, **kwargs
    ) -> Tuple[np.ndarray, List[Document]]:
        """
        Search for similar vectors.

        Args:
            query_vector (np.ndarray): Query vector of shape (dimension,)
            k (int): Number of nearest neighbors to return
            **kwargs: Additional search parameters

        Returns:
            Tuple containing:
            - Distances to nearest neighbors
            - Documents of nearest neighbors
        """
        if query_vector.ndim == 1:
            query_vector = query_vector.reshape(1, -1)

        if hasattr(self.index, "nprobe"):
            nprobe = kwargs.get("nprobe", self.config.nprobe)
            self.index.nprobe = nprobe

        normalized_query = self._normalize_vectors(query_vector)
        distances, indices = self.index.search(normalized_query, k)

        documents = []
        for idx in indices[0]:
            if idx != -1 and idx in self.index_to_id:
                doc_id = self.index_to_id[idx]
                documents.append(self.documents[doc_id])
            else:
                documents.append(Document(id=None, content="empty doc", metadata={}))

        return distances[0], documents

    def get_document(self, doc_id: str) -> Optional[Document]:
        """Get document by ID."""
        return self.documents.get(doc_id)

    def save(self, path: str) -> None:
        """
        Save the index and documents to disk.

        Args:
            path (str): Path to save the database
        """
        faiss.write_index(self.index, f"{path}.index")

        data = {
            "documents": self.documents,
            "id_to_index": self.id_to_index,
            "index_to_id": self.index_to_id,
            "next_index": self._next_index,
            "config": self.config,
        }

        with open(f"{path}.data", "wb") as f:
            pickle.dump(data, f)

    def load(self, path: str) -> None:
        """
        Load the index and documents from disk.

        Args:
            path (str): Path to load the database from
        """
        self.index = faiss.read_index(f"{path}.index")

        with open(f"{path}.data", "rb") as f:
            data = pickle.load(f)

        self.documents = data["documents"]
        self.id_to_index = data["id_to_index"]
        self.index_to_id = data["index_to_id"]
        self._next_index = data["next_index"]
