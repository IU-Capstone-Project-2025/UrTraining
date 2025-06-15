import os
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime

import numpy as np

from ..services.config import VectorDBConfig, DistanceMetric, IndexType
from ..services.vector_db import VectorDB
from ..services.document import Document
from ..services.embedder.huggingface import HuggingFaceEmbedder
from ..services.embedder.base import BaseEmbedder


class VectorDBService:
    """Service layer for managing vector databases."""

    def __init__(
        self,
        data_dir: str = "./data",
        default_embedder: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        self.data_dir: str = data_dir
        self.default_embedder: str = default_embedder
        self.indices: Dict[str, VectorDB] = {}
        self.embedders: Dict[str, BaseEmbedder] = {}

        os.makedirs(data_dir, exist_ok=True)
        self._get_embedder(default_embedder)

    def _get_embedder(self, model_name: str) -> BaseEmbedder:
        """Get or create embedder."""
        if model_name not in self.embedders:
            self.embedders[model_name] = HuggingFaceEmbedder(model_name)
        return self.embedders[model_name]

    def create_index(
        self,
        name: str,
        dimension: int,
        distance_metric: str = "L2",
        index_type: str = "IVF_FLAT",
        nlist: int = 100,
        nprobe: int = 10,
    ) -> bool:
        """Create a new vector index."""
        if name in self.indices:
            raise ValueError(f"Index '{name}' already exists")

        distance_metric_enum = DistanceMetric(distance_metric)
        index_type_enum = IndexType(index_type)
        config = VectorDBConfig(
            dimension=dimension,
            distance_metric=distance_metric_enum,
            index_type=index_type_enum,
            nlist=nlist,
            nprobe=nprobe,
            index_path=os.path.join(self.data_dir, name),
        )

        self.indices[name] = VectorDB(config)
        return True

    def add_documents(
        self,
        index_name: str,
        documents: List[Dict],
        embedder_model: Optional[str] = None,
    ) -> Tuple[int, List[str]]:
        """Add documents to an index."""
        if index_name not in self.indices:
            raise ValueError(f"Index '{index_name}' not found")

        db = self.indices[index_name]
        embedder = self._get_embedder(embedder_model or self.default_embedder)

        # Process documents
        doc_objects = []
        texts = []

        for doc_data in documents:
            content = doc_data.get("content", "")
            if not content:
                raise ValueError("Document must have 'content' field")

            texts.append(content)

            doc = Document(
                id=doc_data.get("id", ""),
                content=content,
                metadata=doc_data.get("metadata", {}),
            )
            doc_objects.append(doc)

        embeddings = embedder.encode(texts)

        for doc, embedding in zip(doc_objects, embeddings):
            doc.vector = embedding

        db.add_documents(doc_objects)

        return len(doc_objects), [doc.id for doc in doc_objects]

    def search(
        self,
        index_name: str,
        query_vector: Optional[List[float]] = None,
        query_text: Optional[str] = None,
        k: int = 5,
        nprobe: Optional[int] = None,
        embedder_model: Optional[str] = None,
    ) -> Tuple[List[float], List[Document], float]:
        """Search for similar vectors."""
        if index_name not in self.indices:
            raise ValueError(f"Index '{index_name}' not found")

        if not query_vector and not query_text:
            raise ValueError("Either query_vector or query_text must be provided")

        db: VectorDB = self.indices[index_name]
        start_time: float = time.time()

        if query_text:
            embedder = self._get_embedder(embedder_model or self.default_embedder)
            query_vector = embedder.encode([query_text])[0].tolist()

        query_array = np.array(query_vector, dtype=np.float32)

        search_kwargs = {}
        if nprobe:
            search_kwargs["nprobe"] = nprobe

        distances, documents = db.search(query_array, k=k, **search_kwargs)

        query_time = (time.time() - start_time) * 1000  # ms

        return distances.tolist(), documents, query_time

    def get_embeddings(
        self, texts: List[str], model_name: Optional[str] = None
    ) -> Tuple[List[List[float]], int, str]:
        """Get embeddings for texts."""
        embedder = self._get_embedder(model_name or self.default_embedder)
        embeddings = embedder.encode(texts)

        return embeddings.tolist(), embedder.get_dimension(), embedder.model_name

    def get_index_documents(
        self, index_name: str, limit: int = 10, offset: int = 0
    ) -> Tuple[List[Document], int]:
        """Get documents from an index with pagination."""
        if index_name not in self.indices:
            raise ValueError(f"Index '{index_name}' not found")

        db = self.indices[index_name]
        all_docs = list(db.documents.values())
        total_count = len(all_docs)

        start_idx = offset
        end_idx = offset + limit
        paginated_docs = all_docs[start_idx:end_idx]

        return paginated_docs, total_count

    def get_health_info(self) -> Dict:
        """Get health information about the service."""
        indices_info = {}
        for name, db in self.indices.items():
            indices_info[name] = {
                "document_count": len(db.documents),
                "vector_count": db.index.ntotal,
                "dimension": db.dimension,
                "distance_metric": db.config.distance_metric.value,
                "index_type": db.config.index_type.value,
            }

        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "indices": indices_info,
            "loaded_embedders": list(self.embedders.keys()),
        }
