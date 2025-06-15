from abc import ABC, abstractmethod
import faiss
from .config import VectorDBConfig, DistanceMetric, IndexType


class VectorIndex(ABC):
    """Abstract base class for vector indices."""

    @abstractmethod
    def build_index(self, config: VectorDBConfig) -> faiss.Index:
        """Build and return the FAISS index."""
        pass


class FlatIndex(VectorIndex):
    """Flat index implementation."""

    def build_index(self, config: VectorDBConfig) -> faiss.Index:
        if config.distance_metric == DistanceMetric.L2:
            return faiss.IndexFlatL2(config.dimension)
        elif config.distance_metric == DistanceMetric.IP:
            return faiss.IndexFlatIP(config.dimension)
        else:
            raise ValueError(f"Unsupported distance metric: {config.distance_metric}")


class IVFFlatIndex(VectorIndex):
    """IVF Flat index implementation."""

    def build_index(self, config: VectorDBConfig) -> faiss.Index:
        if config.distance_metric == DistanceMetric.L2:
            quantizer = faiss.IndexFlatL2(config.dimension)
        elif config.distance_metric == DistanceMetric.IP:
            quantizer = faiss.IndexFlatIP(config.dimension)
        else:
            raise ValueError(f"Unsupported distance metric: {config.distance_metric}")

        return faiss.IndexIVFFlat(quantizer, config.dimension, config.nlist)


class IndexFactory:
    """Factory for creating vector indices."""

    _index_map = {
        IndexType.FLAT: FlatIndex,
        IndexType.IVF_FLAT: IVFFlatIndex,
    }

    @classmethod
    def create_index(cls, config: VectorDBConfig) -> faiss.Index:
        """Create an index based on configuration."""
        if config.index_type not in cls._index_map:
            raise ValueError(f"Unsupported index type: {config.index_type}")

        index_builder: VectorIndex = cls._index_map[config.index_type]()
        return index_builder.build_index(config)
