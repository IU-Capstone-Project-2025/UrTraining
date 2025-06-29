import numpy as np
from typing import List, Union, Dict, Optional, Callable
from collections import defaultdict
import math
import re

from .base import BaseEmbedder


class BM25Embedder(BaseEmbedder):
    
    def __init__(
        self,
        k1: float = 1.2,
        b: float = 0.75,
        epsilon: float = 0.25,
        tokenizer: Optional[Callable] = None
    ):
        """
        Initialize BM25 embedder.
        
        Args:
            k1: Controls term frequency saturation point (default: 1.2)
            b: Controls length normalization (0=no normalization, 1=full normalization)
            epsilon: Floor value for IDF to prevent negative scores
            tokenizer: Custom tokenizer function, defaults to simple split
        """
        self.k1 = k1
        self.b = b
        self.epsilon = epsilon
        self.tokenizer = tokenizer or self._default_tokenizer
        self.model_name = "BM25"  # For compatibility with service layer
        
        self.corpus: List[str] = []
        self.doc_tokens: List[List[str]] = []
        self.doc_lengths: List[int] = []
        self.avg_doc_length: float = 0.0
        self.doc_freqs: Dict[str, int] = defaultdict(int)
        self.idf_scores: Dict[str, float] = {}
        self.num_docs: int = 0
        
        # Since BM25 doesn't produce fixed-size vectors, we'll use a mock dimension
        self._dimension = 1  # BM25 scores are scalar values
    
    def _default_tokenizer(self, text: str) -> List[str]:
        """Default tokenization: lowercase, split on whitespace and punctuation."""
        # Simple tokenization - can be improved with more sophisticated methods
        text = text.lower()
        # Split on whitespace and common punctuation
        tokens = re.findall(r'\b\w+\b', text)
        return tokens
    
    def _compute_idf(self):
        """Compute IDF scores for all terms in the corpus."""
        self.idf_scores = {}
        for term, freq in self.doc_freqs.items():
            # BM25 IDF formula with epsilon floor
            idf = math.log((self.num_docs - freq + 0.5) / (freq + 0.5))
            self.idf_scores[term] = max(self.epsilon, idf)
    
    def fit(self, documents: List[str]) -> None:
        """
        Fit the BM25 model on a corpus of documents.
        
        Args:
            documents: List of document texts to build the index from
        """
        self.corpus = documents
        self.doc_tokens = []
        self.doc_lengths = []
        self.doc_freqs = defaultdict(int)
        self.num_docs = len(documents)
        
        # Tokenize all documents and compute statistics
        total_length = 0
        for doc in documents:
            tokens = self.tokenizer(doc)
            self.doc_tokens.append(tokens)
            doc_length = len(tokens)
            self.doc_lengths.append(doc_length)
            total_length += doc_length
            
            # Count document frequencies
            unique_tokens = set(tokens)
            for token in unique_tokens:
                self.doc_freqs[token] += 1
        
        # Compute average document length
        self.avg_doc_length = total_length / self.num_docs if self.num_docs > 0 else 0
        
        # Compute IDF scores
        self._compute_idf()
    
    def _bm25_score(self, query_tokens: List[str], doc_tokens: List[str], doc_length: int) -> float:
        """
        Compute BM25 score between query and document.
        
        Args:
            query_tokens: Tokenized query
            doc_tokens: Tokenized document
            doc_length: Length of the document
            
        Returns:
            BM25 score
        """
        score = 0.0
        doc_token_counts = defaultdict(int)
        
        # Count term frequencies in document
        for token in doc_tokens:
            doc_token_counts[token] += 1
        
        # Compute BM25 score
        for token in query_tokens:
            if token in doc_token_counts and token in self.idf_scores:
                tf = doc_token_counts[token]
                idf = self.idf_scores[token]
                
                # BM25 formula
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * (doc_length / self.avg_doc_length))
                
                score += idf * (numerator / denominator)
        
        return score
    
    def encode(self, texts: Union[str, List[str]], **kwargs) -> np.ndarray:
        """
        Encode texts using BM25 scoring against the fitted corpus.
        
        For BM25, this returns similarity scores against all documents in the corpus.
        Each "encoding" is a vector of BM25 scores vs each document.
        
        Args:
            texts: Query text(s) to encode
            **kwargs: Additional parameters (unused for BM25)
            
        Returns:
            Array of shape (len(texts), num_docs) containing BM25 scores
        """
        if not self.corpus:
            raise ValueError("BM25 model must be fitted with documents before encoding")
        
        if isinstance(texts, str):
            texts = [texts]
        
        scores_matrix = []
        
        for query_text in texts:
            query_tokens = self.tokenizer(query_text)
            doc_scores = []
            
            # Compute BM25 score against each document in corpus
            for i, (doc_tokens, doc_length) in enumerate(zip(self.doc_tokens, self.doc_lengths)):
                score = self._bm25_score(query_tokens, doc_tokens, doc_length)
                doc_scores.append(score)
            
            scores_matrix.append(doc_scores)
        
        return np.array(scores_matrix, dtype=np.float32)
    
    def search(self, query: str, k: int = 5) -> List[tuple]:
        """
        Search for top-k most relevant documents for a query.
        
        Args:
            query: Search query text
            k: Number of top results to return
            
        Returns:
            List of tuples (doc_index, score) sorted by relevance
        """
        if not self.corpus:
            raise ValueError("BM25 model must be fitted with documents before searching")
        
        query_tokens = self.tokenizer(query)
        scores = []
        
        for i, (doc_tokens, doc_length) in enumerate(zip(self.doc_tokens, self.doc_lengths)):
            score = self._bm25_score(query_tokens, doc_tokens, doc_length)
            scores.append((i, score))
        
        # Sort by score (descending) and return top-k
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:k]
    
    def get_dimension(self) -> int:
        """Get the 'dimension' - for BM25 this is the corpus size."""
        return len(self.corpus) if self.corpus else 1
    
    def get_vocabulary_size(self) -> int:
        """Get the size of the vocabulary."""
        return len(self.doc_freqs)
    
    def get_document_count(self) -> int:
        """Get the number of documents in the corpus."""
        return self.num_docs
