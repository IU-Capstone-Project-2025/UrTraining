# Vector Database API

FastAPI service for vector similarity search and BM25 text retrieval. Built with FAISS for vector storage, Hugging Face transformers for text embedding, and custom BM25 implementation for keyword-based search.

## Features

- **Vector Search**: Dense vector similarity search using FAISS with multiple distance metrics
- **BM25 Search**: Traditional keyword-based search using BM25 algorithm
- **Multiple Embedders**: Support for Hugging Face transformers and KlusterAI embeddings
- **Flexible Configuration**: Configurable index types, distance metrics, and BM25 parameters
- **Persistent Storage**: Save and load indices with all metadata

## Quick Start

### With Docker Compose

```bash
cd ml/vector-db

# Start the service
docker-compose build
docker-compose up -d

# The API will be available at http://localhost:8000
# API documentation at http://localhost:8000/docs
```

### Direct Docker Run

```bash
docker build -t vector-db .

# Run with default configuration
docker run -p 8000:8000 -v $(pwd)/data:/app/data vector-db

# Or
# Run with custom configuration
docker run -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -e DEFAULT_EMBEDDER_MODEL=sentence-transformers/all-mpnet-base-v2 \
  -e DEFAULT_DISTANCE_METRIC=COSINE \
  -e EMBEDDER_DEVICE=cpu \
  vector-db
```

## API Usage Examples

### 1. Create a Vector Index

```bash
curl -X POST "http://localhost:8000/create_index" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my_vector_docs",
    "dimension": 384,
    "index_type": "IVF_FLAT",
    "distance_metric": "COSINE"
  }'
```

### 2. Create a BM25 Index

```bash
curl -X POST "http://localhost:8000/create_index" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my_bm25_docs",
    "dimension": 1,
    "index_type": "BM25",
    "bm25_k1": 1.2,
    "bm25_b": 0.75,
    "bm25_epsilon": 0.25
  }'
```

### 3. Add Documents

```bash
curl -X POST "http://localhost:8000/add_documents" \
  -H "Content-Type: application/json" \
  -d '{
    "index_name": "my_vector_docs",
    "documents": [
      {
        "content": "Python is a programming language",
        "metadata": {"category": "programming"}
      },
      {
        "content": "Machine learning is a subset of AI",
        "metadata": {"category": "ai"}
      }
    ]
  }'
```

### 4. Search by Text (Vector Index)

```bash
curl -X POST "http://localhost:8000/search_index" \
  -H "Content-Type: application/json" \
  -d '{
    "index_name": "my_vector_docs",
    "query_text": "artificial intelligence",
    "k": 5
  }'
```

### 5. Search by Text (BM25 Index)

```bash
curl -X POST "http://localhost:8000/search_index" \
  -H "Content-Type: application/json" \
  -d '{
    "index_name": "my_bm25_docs",
    "query_text": "machine learning programming",
    "k": 5
  }'
```

### 6. Get Embeddings

```bash
curl -X POST "http://localhost:8000/get_embedding" \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["Hello world", "Machine learning"]
  }'
```

### 7. Health Check

```bash
curl "http://localhost:8000/health"
```

### 8. Delete Index

```bash
curl -X DELETE "http://localhost:8000/indices/my_vector_docs"
```

## Index Types

### Vector Indices
- **FLAT**: Exact search with brute force
- **IVF_FLAT**: Inverted file index for faster approximate search

### BM25 Index
- **BM25**: Traditional keyword-based search using BM25 algorithm
- Supports configurable parameters:
  - `k1`: Term frequency saturation (default: 1.2)
  - `b`: Length normalization (default: 0.75)  
  - `epsilon`: IDF floor to prevent negative scores (default: 0.25)

## Distance Metrics (Vector Indices Only)
- **L2**: Euclidean distance
- **IP**: Inner product
- **COSINE**: Cosine similarity

## Architecture

- **FastAPI**: Modern web framework with automatic API documentation
- **FAISS**: High-performance vector similarity search
- **Custom BM25**: Pure Python implementation of BM25 algorithm
- **Hugging Face Transformers**: State-of-the-art embedding models
- **Pydantic**: Data validation and serialization
- **Docker**: Containerized deployment

## Dependencies

- Python 3.12.3
- FastAPI
- FAISS-CPU
- Transformers
- NumPy
- Uvicorn

## Performance Considerations

### Vector Search
- Best for semantic similarity and dense retrieval
- Requires preprocessing (embedding generation)
- Fast similarity computation with FAISS
- Memory scales with embedding dimension × number of documents

### BM25 Search
- Best for keyword matching and sparse retrieval
- No preprocessing required
- Fast text-based search
- Memory scales with vocabulary size
- Better for exact term matching

## TODO

- [ ] Add support for loading .bin files for finetuned retrievers
- [ ] Implement hybrid search (BM25 + Vector)
- [ ] Add more advanced BM25 variants (BM25F, BM25+)
- [ ] Support for custom tokenizers in BM25

