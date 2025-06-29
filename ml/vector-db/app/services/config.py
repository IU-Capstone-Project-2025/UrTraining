from dataclasses import dataclass
from typing import Optional
from enum import Enum


class DistanceMetric(Enum):
    """Supported distance metrics."""

    L2 = "L2"
    IP = "IP"
    COSINE = "COSINE"


class IndexType(Enum):
    """Supported index types."""

    FLAT = "Flat"
    IVF_FLAT = "IVFFlat"
    BM25 = "BM25"


@dataclass
class VectorDBConfig:
    """Configuration for vector database."""

    dimension: int
    distance_metric: DistanceMetric = DistanceMetric.L2
    index_type: IndexType = IndexType.IVF_FLAT

    # IVF params
    nlist: int = 100
    nprobe: int = 10

    # BM25 params
    bm25_k1: float = 1.2
    bm25_b: float = 0.75
    bm25_epsilon: float = 0.25

    index_path: Optional[str] = None
