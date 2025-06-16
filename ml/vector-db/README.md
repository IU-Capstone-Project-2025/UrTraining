# Vector Database API

FastAPI service for vector similarity search and text embeddings. Built with FAISS for vector storage and Hugging Face transformers for text embedding.

## Quick Start

### With Docker Compose

```bash
# Clone or navigate to the project directory
cd ml/vector-db

# Start the service
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

### 1. Create an Index

```bash
curl -X POST "http://localhost:8000/indices" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my_documents",
    "dimension": 384
  }'
```

### 2. Add Documents

```bash
curl -X POST "http://localhost:8000/indices/my_documents/documents" \
  -H "Content-Type: application/json" \
  -d '{
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

### 3. Search by Text

```bash
curl -X POST "http://localhost:8000/indices/my_documents/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query_text": "artificial intelligence",
    "k": 5
  }'
```

### 4. Get Embeddings

```bash
curl -X POST "http://localhost:8000/embeddings" \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["Hello world", "Machine learning"]
  }'
```

### 5. Health Check

```bash
curl "http://localhost:8000/health"
```

### 6. Delete Index

```bash
curl -X DELETE "http://localhost:8000/indices/my_documents"
```

## Architecture

- **FastAPI**: Modern web framework with automatic API documentation
- **FAISS**: High-performance vector similarity search
- **Hugging Face Transformers**: State-of-the-art embedding models
- **Pydantic**: Data validation and serialization
- **Docker**: Containerized deployment

## Dependencies

- Python 3.9+
- FastAPI
- FAISS-CPU
- Sentence Transformers
- NumPy
- Uvicorn

## TODO

- [ ] Add support for loading .bin files for embeddings

