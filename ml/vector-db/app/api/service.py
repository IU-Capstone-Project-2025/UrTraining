import os
import time
import shutil
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime

import numpy as np

from ..services.config import VectorDBConfig, DistanceMetric, IndexType
from ..services.vector_db import VectorDB
from ..services.document import Document
from ..services.embedder.huggingface import HuggingFaceEmbedder
from ..services.embedder.api import KlusterAIEmbedder
from ..services.embedder.base import BaseEmbedder


class VectorDBService:
    """Service layer for managing vector databases."""

    def __init__(
        self,
        data_dir: Optional[str] = None,
        default_embedder: Optional[str] = None,
        default_embedder_type: Optional[str] = None,
    ):
        self.data_dir = data_dir or os.getenv("VECTOR_DB_DATA_DIR", "./data")
        self.default_embedder = default_embedder or os.getenv(
            "DEFAULT_EMBEDDER_MODEL", "BAAI/bge-m3"
        )
        self.default_embedder_type = default_embedder_type or os.getenv(
            "DEFAULT_EMBEDDER_TYPE", "klusterai"
        )
        self.default_distance_metric = os.getenv("DEFAULT_DISTANCE_METRIC", "L2")
        self.default_index_type = os.getenv("DEFAULT_INDEX_TYPE", "IVF_FLAT")
        self.default_nlist = int(os.getenv("DEFAULT_NLIST", "100"))
        self.default_nprobe = int(os.getenv("DEFAULT_NPROBE", "10"))
        self.embedder_device = os.getenv("EMBEDDER_DEVICE", "cpu")
        self.embedder_max_length = int(os.getenv("EMBEDDER_MAX_LENGTH", "512"))
        self.embedder_pooling = os.getenv("EMBEDDER_POOLING_STRATEGY", "mean")
        self.embedder_normalize = (
            os.getenv("EMBEDDER_NORMALIZE", "true").lower() == "true"
        )

        self.indices: Dict[str, VectorDB] = {}
        self.embedders: Dict[str, BaseEmbedder] = {}

        os.makedirs(self.data_dir, exist_ok=True)
        print(self.default_embedder, self.default_embedder_type)
        self._get_embedder(self.default_embedder, self.default_embedder_type)

    def _get_embedder(
        self, model_name: str, model_type: str = "klusterai", **kwargs: Any
    ) -> BaseEmbedder:
        """Get or create embedder with configured parameters."""
        if model_name not in self.embedders:
            if model_type == "huggingface":
                self.embedders[model_name] = HuggingFaceEmbedder(
                    model_name=model_name,
                    device=self.embedder_device,
                    max_length=self.embedder_max_length,
                    pooling_strategy=self.embedder_pooling,
                    normalize=self.embedder_normalize,
                )
            elif model_type == "klusterai":
                api_key = os.getenv("KLUSTER_AI_API_KEY")
                if not api_key:
                    raise ValueError(
                        "KLUSTER_AI_API_KEY environment variable is required for KlusterAI embedder"
                    )
                self.embedders[model_name] = KlusterAIEmbedder(
                    api_key=api_key,
                    model_name=model_name,
                    dimension=kwargs.get("dimension", 1024),
                )
            else:
                raise ValueError(f"Unsupported model type: {model_type}")
        return self.embedders[model_name]

    def create_index(
        self,
        name: str,
        dimension: int,
        distance_metric: Optional[str] = None,
        index_type: Optional[str] = None,
        nlist: Optional[int] = None,
        nprobe: Optional[int] = None,
    ) -> bool:
        """Create a new vector index with default values from environment."""
        if name in self.indices:
            raise ValueError(f"Index '{name}' already exists")

        # Use provided values or fall back to environment defaults
        distance_metric = distance_metric or self.default_distance_metric
        index_type = index_type or self.default_index_type
        nlist = nlist or self.default_nlist
        nprobe = nprobe or self.default_nprobe

        # Convert string enums
        distance_metric_enum = DistanceMetric(distance_metric)
        index_type_enum = IndexType(index_type)

        # Create config
        config = VectorDBConfig(
            dimension=dimension,
            distance_metric=distance_metric_enum,
            index_type=index_type_enum,
            nlist=nlist,
            nprobe=nprobe,
            index_path=os.path.join(self.data_dir, name),
        )

        # Create vector database
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
            # Extract text content
            content = doc_data.get("content", "")
            if not content:
                raise ValueError("Document must have 'content' field")

            texts.append(content)

            # Create document object
            doc = Document(
                id=doc_data.get("id", ""),  # Will auto-generate if empty
                content=content,
                metadata=doc_data.get("metadata", {}),
            )
            doc_objects.append(doc)

        # Generate embeddings
        embeddings = embedder.encode(texts)

        # Add vectors to documents
        for doc, embedding in zip(doc_objects, embeddings):
            doc.vector = embedding

        # Add to database
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

        db = self.indices[index_name]
        start_time = time.time()

        # Convert query text to vector if needed
        if query_text:
            embedder = self._get_embedder(embedder_model or self.default_embedder)
            query_vector = embedder.encode([query_text])[0].tolist()

        # Search
        query_array = np.array(query_vector, dtype=np.float32)

        search_kwargs = {}
        if nprobe:
            search_kwargs["nprobe"] = nprobe

        distances, documents = db.search(query_array, k=k, **search_kwargs)

        query_time = (time.time() - start_time) * 1000  # Convert to ms

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

        # Apply pagination
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
            "config": {
                "data_dir": self.data_dir,
                "default_embedder": self.default_embedder,
                "default_distance_metric": self.default_distance_metric,
                "default_index_type": self.default_index_type,
                "default_nlist": self.default_nlist,
                "default_nprobe": self.default_nprobe,
                "embedder_device": self.embedder_device,
                "embedder_max_length": self.embedder_max_length,
                "embedder_pooling": self.embedder_pooling,
                "embedder_normalize": self.embedder_normalize,
            },
        }

    def delete_index(self, name: str) -> bool:
        """Delete an index and its associated files."""
        if name not in self.indices:
            raise ValueError(f"Index '{name}' not found")

        del self.indices[name]

        index_path: str = os.path.join(self.data_dir, name)
        if os.path.exists(index_path):
            if os.path.isdir(index_path):
                shutil.rmtree(index_path)
            else:
                os.remove(index_path)

        index_file: str = f"{index_path}.index"
        if os.path.exists(index_file):
            os.remove(index_file)

        return True
