import logging
from typing import List

from fastapi import FastAPI, HTTPException, Depends

from .models import (
    CreateIndexRequest,
    CreateIndexResponse,
    AddDocumentsRequest,
    AddDocumentsResponse,
    SearchRequest,
    SearchResponse,
    SearchResult,
    GetEmbeddingRequest,
    GetEmbeddingResponse,
    GetIndexDocsRequest,
    GetIndexDocsResponse,
    DocumentInfo,
    HealthResponse,
    DeleteIndexResponse,
    GetDocumentRequest,
    GetDocumentResponse,
)
from .service import VectorDBService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

vector_service = VectorDBService()
app = FastAPI(
    title="Vector Database API",
    description="API for vector similarity search and document storage",
    version="1.0.0",
)


def get_vector_service() -> VectorDBService:
    """Dependency to get the vector service."""
    return vector_service


@app.post("/create_index", response_model=CreateIndexResponse)
async def create_index(
    request: CreateIndexRequest, service: VectorDBService = Depends(get_vector_service)
):
    """Create a new vector index."""
    try:
        success = service.create_index(
            name=request.name,
            dimension=request.dimension,
            distance_metric=request.distance_metric,
            index_type=request.index_type,
            nlist=request.nlist,
            nprobe=request.nprobe,
            bm25_k1=request.bm25_k1,
            bm25_b=request.bm25_b,
            bm25_epsilon=request.bm25_epsilon,
        )

        return CreateIndexResponse(
            success=success,
            message=f"Index '{request.name}' created successfully",
            index_name=request.name,
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating index: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/add_documents", response_model=AddDocumentsResponse)
async def add_documents(
    request: AddDocumentsRequest, service: VectorDBService = Depends(get_vector_service)
):
    """Add documents to an index."""
    try:
        added_count, document_ids = service.add_documents(
            index_name=request.index_name, documents=request.documents
        )

        return AddDocumentsResponse(
            success=True,
            message=f"Added {added_count} documents to index '{request.index_name}'",
            added_count=added_count,
            document_ids=document_ids,
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error adding documents: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/get_document", response_model=GetDocumentResponse)
async def get_document(
    request: GetDocumentRequest, service: VectorDBService = Depends(get_vector_service)
):
    """Get a document from an index."""
    return GetDocumentResponse(
        success=True,
        document=service.get_document(request.index_name, request.document_id),
    )


@app.post("/search_index", response_model=SearchResponse)
async def search_index(
    request: SearchRequest, service: VectorDBService = Depends(get_vector_service)
):
    """Search for similar vectors in an index."""
    try:
        distances, documents, query_time = service.search(
            index_name=request.index_name,
            query_vector=request.query_vector,
            query_text=request.query_text,
            k=request.k,
            nprobe=request.nprobe,
        )

        results = []
        for distance, doc in zip(distances, documents):
            if doc.id:
                results.append(
                    SearchResult(
                        id=doc.id,
                        content=f"{doc.content[:10]}...",
                        metadata=doc.metadata or {},
                        distance=distance,
                    )
                )

        return SearchResponse(success=True, results=results, query_time_ms=query_time)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error searching index: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/get_embedding", response_model=GetEmbeddingResponse)
async def get_embedding(
    request: GetEmbeddingRequest, service: VectorDBService = Depends(get_vector_service)
):
    """Get embeddings for texts."""
    try:
        embeddings, dimension, model_used = service.get_embeddings(
            texts=request.texts, model_name=request.model_name
        )

        return GetEmbeddingResponse(
            success=True,
            embeddings=embeddings,
            dimension=dimension,
            model_used=model_used,
        )

    except Exception as e:
        logger.error(f"Error getting embeddings: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/get_index_docs", response_model=GetIndexDocsResponse)
async def get_index_docs(
    request: GetIndexDocsRequest, service: VectorDBService = Depends(get_vector_service)
):
    """Get documents from an index with pagination."""
    try:
        documents, total_count = service.get_index_documents(
            index_name=request.index_name, limit=request.limit, offset=request.offset
        )

        doc_infos: List[DocumentInfo] = [
            DocumentInfo(id=doc.id, content=doc.content, metadata=doc.metadata or {})
            for doc in documents
        ]

        return GetIndexDocsResponse(
            success=True,
            documents=doc_infos,
            total_count=total_count,
            offset=request.offset,
            limit=request.limit,
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting index documents: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/health", response_model=HealthResponse)
async def health(service: VectorDBService = Depends(get_vector_service)):
    """Health check endpoint."""
    try:
        health_info = service.get_health_info()
        return HealthResponse(**health_info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/indices/{index_name}", response_model=DeleteIndexResponse)
async def delete_index(
    index_name: str, service: VectorDBService = Depends(get_vector_service)
):
    """Delete an index and all its data."""
    try:
        success = service.delete_index(index_name)
        return DeleteIndexResponse(
            success=success,
            message=f"Index '{index_name}' deleted successfully",
            deleted_index=index_name,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
