from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field


class CreateIndexRequest(BaseModel):
    """Request model for creating an index."""

    name: str = Field(..., description="Index name")
    dimension: int = Field(..., gt=0, description="Vector dimension")
    distance_metric: str = Field(
        default="L2", description="Distance metric (L2, IP, COSINE)"
    )
    index_type: str = Field(
        default="IVF_FLAT", description="Index type (FLAT, IVF_FLAT, BM25)"
    )
    nlist: int = Field(default=100, gt=0, description="Number of clusters for IVF")
    nprobe: int = Field(default=10, gt=0, description="Number of clusters to probe")
    
    # BM25-specific parameters
    bm25_k1: Optional[float] = Field(default=1.2, gt=0, description="BM25 k1 parameter (term frequency saturation)")
    bm25_b: Optional[float] = Field(default=0.75, ge=0, le=1, description="BM25 b parameter (length normalization)")
    bm25_epsilon: Optional[float] = Field(default=0.25, ge=0, description="BM25 epsilon parameter (IDF floor)")


class CreateIndexResponse(BaseModel):
    """Response model for index creation."""

    success: bool
    message: str
    index_name: str


class AddDocumentsRequest(BaseModel):
    """Request model for adding documents."""

    index_name: str = Field(..., description="Index name")
    documents: List[Any]


class AddDocumentsResponse(BaseModel):
    """Response model for adding documents."""

    success: bool
    message: str
    added_count: int
    document_ids: List[str]


class GetDocumentRequest(BaseModel):
    """Request model for getting a document."""

    index_name: str = Field(..., description="Index name")
    document_id: str = Field(..., description="Document ID")


class GetDocumentResponse(BaseModel):
    """Response model for getting a document."""

    success: bool
    document: Dict[str, Any]


class SearchRequest(BaseModel):
    """Request model for vector search."""

    index_name: str = Field(..., description="Index name")
    query_vector: Optional[List[float]] = Field(None, description="Query vector")
    query_text: Optional[str] = Field(None, description="Query text (will be embedded)")
    k: int = Field(default=5, gt=0, le=100, description="Number of results")
    nprobe: Optional[int] = Field(None, gt=0, description="Number of clusters to probe")


class SearchResult(BaseModel):
    """Single search result."""

    id: str
    content: str
    metadata: Dict[str, Any]
    distance: float


class SearchResponse(BaseModel):
    """Response model for search."""

    success: bool
    results: List[SearchResult]
    query_time_ms: float


class GetEmbeddingRequest(BaseModel):
    """Request model for getting embeddings."""

    texts: List[str] = Field(..., description="Texts to embed")
    model_name: Optional[str] = Field(None, description="Embedder model name")


class GetEmbeddingResponse(BaseModel):
    """Response model for embeddings."""

    success: bool
    embeddings: List[List[float]]
    dimension: int
    model_used: str


class GetIndexDocsRequest(BaseModel):
    """Request model for getting index documents."""

    index_name: str = Field(..., description="Index name")
    limit: int = Field(
        default=10, gt=0, le=1000, description="Maximum number of documents"
    )
    offset: int = Field(default=0, ge=0, description="Offset for pagination")


class DocumentInfo(BaseModel):
    """Document information."""

    id: str
    content: str
    metadata: Dict[str, Any]


class GetIndexDocsResponse(BaseModel):
    """Response model for index documents."""

    success: bool
    documents: List[DocumentInfo]
    total_count: int
    offset: int
    limit: int


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    timestamp: str
    version: str
    indices: Dict[str, Dict]
    loaded_embedders: List[str]
    config: Dict


class DeleteIndexResponse(BaseModel):
    """Response for index deletion."""

    success: bool
    message: str
    deleted_index: str
