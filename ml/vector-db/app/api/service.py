import os
import time
import shutil
import logging
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime

import numpy as np

from ..services.config import VectorDBConfig, DistanceMetric, IndexType
from ..services.vector_db import VectorDB
from ..services.bm25_index import BM25Index
from ..services.document import Document
from ..services.embedder.huggingface import HuggingFaceEmbedder
from ..services.embedder.api import KlusterAIEmbedder
from ..services.embedder.bm25 import BM25Embedder
from ..services.embedder.base import BaseEmbedder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
            "EMBEDDER_MODEL", "BAAI/bge-m3"
        )
        self.default_embedder_type = default_embedder_type or os.getenv(
            "EMBEDDER_TYPE", "klusterai"
        )
        self.default_distance_metric = os.getenv("DISTANCE_METRIC", "L2")
        self.default_index_type = os.getenv("INDEX_TYPE", "IVF_FLAT")
        self.default_nlist = int(os.getenv("NLIST", "100"))
        self.default_nprobe = int(os.getenv("NPROBE", "10"))
        self.embedder_device = os.getenv("EMBEDDER_DEVICE", "cpu")
        self.embedder_max_length = int(os.getenv("EMBEDDER_MAX_LENGTH", "512"))
        self.embedder_pooling = os.getenv("EMBEDDER_POOLING_STRATEGY", "mean")
        self.embedder_normalize = (
            os.getenv("EMBEDDER_NORMALIZE", "true").lower() == "true"
        )

        self.indices: Dict[str, VectorDB] = {}
        self.embedders: Dict[str, BaseEmbedder] = {}

        os.makedirs(self.data_dir, exist_ok=True)
        logger.info(f"Creating {self.default_embedder, self.default_embedder_type}")
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
            elif model_type == "bm25":
                self.embedders[model_name] = BM25Embedder(
                    k1=kwargs.get("k1", 1.2),
                    b=kwargs.get("b", 0.75),
                    epsilon=kwargs.get("epsilon", 0.25),
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
        bm25_k1: Optional[float] = None,
        bm25_b: Optional[float] = None,
        bm25_epsilon: Optional[float] = None,
    ) -> bool:
        """Create a new index with default values from environment."""
        if name in self.indices:
            raise ValueError(f"Index '{name}' already exists")

        distance_metric = distance_metric or self.default_distance_metric
        index_type = index_type or self.default_index_type
        nlist = nlist or self.default_nlist
        nprobe = nprobe or self.default_nprobe
        distance_metric_enum = DistanceMetric(distance_metric)
        index_type_enum = IndexType(index_type)

        if index_type_enum == IndexType.BM25:
            self.indices[name] = BM25Index(
                k1=bm25_k1 or 1.2,
                b=bm25_b or 0.75,
                epsilon=bm25_epsilon or 0.25,
                index_path=os.path.join(self.data_dir, name),
            )
        else:
            config = VectorDBConfig(
                dimension=dimension,
                distance_metric=distance_metric_enum,
                index_type=index_type_enum,
                nlist=nlist,
                nprobe=nprobe,
                bm25_k1=bm25_k1 or 1.2,
                bm25_b=bm25_b or 0.75,
                bm25_epsilon=bm25_epsilon or 0.25,
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

        doc_objects = []
        texts = []

        for doc_data in documents:
            content = doc_data.get("content", "")
            if not content:
                raise ValueError("Document must have 'content' field")

            texts.append(content)

            doc = Document(
                id=doc_data.get("id", None),
                content=content,
                metadata=doc_data.get("metadata", {}),
            )
            doc_objects.append(doc)

        if isinstance(db, BM25Index):
            db.add_documents(doc_objects)
        else:
            embedder = self._get_embedder(embedder_model or self.default_embedder)
            embeddings = embedder.encode(texts)

            for doc, embedding in zip(doc_objects, embeddings):
                doc.vector = embedding

            db.add_documents(doc_objects)

        return len(doc_objects), [doc.id for doc in doc_objects]

    def get_document(self, index_name: str, document_id: str) -> Dict:
        """Get a document from an index."""
        if index_name not in self.indices:
            raise ValueError(f"Index '{index_name}' not found")

        db = self.indices[index_name]
        return db.get_document(document_id)

    def search(
        self,
        index_name: str,
        query_vector: Optional[List[float]] = None,
        query_text: Optional[str] = None,
        k: int = 5,
        nprobe: Optional[int] = None,
        embedder_model: Optional[str] = None,
    ) -> Tuple[List[float], List[Document], float]:
        """Search for similar documents."""
        if index_name not in self.indices:
            raise ValueError(f"Index '{index_name}' not found")

        if not query_vector and not query_text:
            raise ValueError("Either query_vector or query_text must be provided")

        db = self.indices[index_name]
        start_time = time.time()

        if isinstance(db, BM25Index):
            if not query_text:
                raise ValueError("BM25 search requires query_text")

            scores, documents = db.search(query_text, k=k)
            query_time = (time.time() - start_time) * 1000

            return scores, documents, query_time
        else:
            if query_text:
                embedder = self._get_embedder(embedder_model or self.default_embedder)
                query_vector = embedder.encode([query_text])[0].tolist()

            # Search
            query_array = np.array(query_vector, dtype=np.float32)

            search_kwargs = {}
            if nprobe:
                search_kwargs["nprobe"] = nprobe

            distances, documents = db.search(query_array, k=k, **search_kwargs)

            query_time = (time.time() - start_time) * 1000

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
            if isinstance(db, BM25Index):
                stats = db.get_stats()
                indices_info[name] = {
                    "document_count": stats["num_documents"],
                    "vocabulary_size": stats["vocabulary_size"],
                    "avg_doc_length": stats["avg_doc_length"],
                    "index_type": "BM25",
                    "bm25_k1": stats["k1"],
                    "bm25_b": stats["b"],
                    "bm25_epsilon": stats["epsilon"],
                }
            else:
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

        db = self.indices[name]
        del self.indices[name]

        index_path: str = os.path.join(self.data_dir, name)
        if os.path.exists(index_path):
            if os.path.isdir(index_path):
                shutil.rmtree(index_path)
            else:
                os.remove(index_path)

        if isinstance(db, BM25Index):
            # BM25 index file
            bm25_file: str = f"{index_path}.bm25"
            if os.path.exists(bm25_file):
                os.remove(bm25_file)
        else:
            # Vector index files
            index_file: str = f"{index_path}.index"
            if os.path.exists(index_file):
                os.remove(index_file)

            data_file: str = f"{index_path}.data"
            if os.path.exists(data_file):
                os.remove(data_file)

        return True
