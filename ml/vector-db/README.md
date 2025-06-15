# Vector Database API

FastAPI service for vector similarity search and text embeddings. Built with FAISS for vector storage and Hugging Face transformers for text embedding.

## Quick Start

### Docker (Recommended)
```bash
docker-compose up --build
```

### Local Development
```bash
pip install -r requirements.txt
python -m app.main --host 0.0.0.0 --port 8000
```

API will be available at `http://localhost:8000`

## API Endpoints

### Create Index
```bash
curl -X POST "http://localhost:8000/create_index" \
  -H "Content-Type: application/json" \
  -d '{"name": "docs", "dimension": 384}'
```

### Add Documents
```bash
curl -X POST "http://localhost:8000/add_documents" \
  -H "Content-Type: application/json" \
  -d '{
    "index_name": "docs",
    "documents": [
      {"content": "Machine learning and AI", "metadata": {"type": "tech"}},
      {"content": "Python is a language", "metadata": {"type": "programming"}}
    ]
  }'
```

### Search
```bash
curl -X POST "http://localhost:8000/search_index" \
  -H "Content-Type: application/json" \
  -d '{"index_name": "docs", "query_text": "What is AI?", "k": 3}'
```

### Get Embeddings
```bash
curl -X POST "http://localhost:8000/get_embedding" \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Hello world", "Machine learning"]}'
```

### Health Check
```bash
curl "http://localhost:8000/health"
```

## Documentation

- Interactive API docs: `http://localhost:8000/docs`
- OpenAPI schema: `http://localhost:8000/openapi.json`

## Architecture

```
app/
├── api/
│   ├── endpoints.py    # FastAPI routes
│   ├── models.py       # Pydantic schemas
│   └── service.py      # Business logic
├── services/
│   ├── vector_db.py    # FAISS vector database
│   ├── config.py       # Configuration
│   ├── document.py     # Document model
│   └── embedder/       # Directory for Embedding components
└── main.py            # Application entry point
```

## Dependencies

- **FastAPI** - Web framework
- **FAISS** - Vector similarity search
- **Transformers** - Hugging Face models
- **PyTorch** - ML framework


## TODO

- [ ] Add support for loading .bin files for embedder (fine-tuned models)

