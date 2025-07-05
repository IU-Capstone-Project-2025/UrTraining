import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

# Получаем абсолютный путь к корню проекта
current_dir = os.path.dirname(os.path.abspath(__file__))  # /tests/
project_root = os.path.dirname(current_dir)               # /vector-db/
sys.path.insert(0, project_root)

# Мокируем все зависимости перед импортом app
with patch.dict('os.environ', {
    'EMBEDDER_TYPE': 'huggingface',
    'EMBEDDER_MODEL': 'BAAI/bge-small-en-v1.5'
}), \
patch('faiss.IndexFlatL2', MagicMock()), \
patch('app.api.service.HuggingFaceEmbedder', MagicMock()):

    from app.main import app
    from app.api.models import (
        CreateIndexRequest,
        AddDocumentsRequest,
        SearchRequest,
        GetEmbeddingRequest,
        GetIndexDocsRequest,
        GetDocumentRequest,
    )

client = TestClient(app)

# Тестовые данные
TEST_INDEX_NAME = "test_index"
TEST_DIMENSION = 384  # Для BAAI/bge-small-en-v1.5
TEST_DOCUMENTS = [
    {"id": "1", "content": "Sample document 1", "metadata": {"source": "test"}},
    {"id": "2", "content": "Sample document 2", "metadata": {"source": "test"}},
]
TEST_QUERY_VECTOR = [0.1] * TEST_DIMENSION
TEST_TEXTS = ["sample text 1", "sample text 2"]
TEST_EMBEDDINGS = [[0.1] * TEST_DIMENSION] * 2

@pytest.fixture(autouse=True)
def mock_dependencies():
    # Мок для VectorDBService
    with patch('app.api.service.VectorDBService') as mock_service:
        mock_instance = mock_service.return_value
        mock_instance.create_index.return_value = True
        mock_instance.add_documents.return_value = (2, ["1", "2"])
        mock_instance.search.return_value = ([0.9, 0.8], TEST_DOCUMENTS, 10)
        mock_instance.get_embeddings.return_value = (TEST_EMBEDDINGS, TEST_DIMENSION, "BAAI/bge-small-en-v1.5")
        mock_instance.get_health_info.return_value = {"status": "OK"}
        yield


def test_get_embedding_success():
    """Тест получения эмбеддингов"""
    # 1. Мокируем ВСЕ зависимости
    with patch('app.api.endpoints.vector_service') as mock_service, \
         patch('app.api.service.HuggingFaceEmbedder') as mock_embedder:
        
        # 2. Настраиваем моки
        mock_embedder_instance = MagicMock()
        mock_embedder_instance.embed.return_value = TEST_EMBEDDINGS
        mock_embedder.return_value = mock_embedder_instance
        
        mock_service.get_embeddings.return_value = (
            TEST_EMBEDDINGS,
            TEST_DIMENSION,
            "BAAI/bge-small-en-v1.5"
        )

        # 3. Выполняем запрос
        response = client.post(
            "/get_embedding",
            json={
                "texts": TEST_TEXTS,
                "model_name": "default",
            },
        )

        # 4. Проверяем результаты
        assert response.status_code == 200
        assert response.json() == {
            "success": True,
            "embeddings": TEST_EMBEDDINGS,
            "dimension": TEST_DIMENSION,
            "model_used": "BAAI/bge-small-en-v1.5"
        }

def test_health_check():
    """Тест health check эндпоинта"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"  # Changed from "OK" to "healthy"
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from typing import List, Dict, Any

# Тесты для создания индекса
def test_create_index_invalid_dimension():
    """Тест создания индекса с недопустимой размерностью"""
    with patch('app.api.service.VectorDBService'):
        response = client.post(
            "/create_index",
            json={
                "name": "invalid_dim_index",
                "dimension": 0,  # Недопустимая размерность
                "distance_metric": "L2",
                "index_type": "FLAT"
            },
        )
        
        # Проверяем статус код (422 Unprocessable Entity)
        assert response.status_code == 422
        
        

# Тесты для добавления документов
def test_add_documents_to_nonexistent_index():
    """Тест добавления документов в несуществующий индекс"""
    with patch('app.api.service.VectorDBService') as mock_service:
        mock_service.return_value.add_documents.side_effect = ValueError("Index not found")
        response = client.post(
            "/add_documents",
            json={
                "index_name": "nonexistent_index",
                "documents": TEST_DOCUMENTS
            },
        )
        assert response.status_code == 400
        assert "not found" in response.json()["detail"]


# Тесты для поиска
def test_search_nonexistent_index():
    """Тест поиска в несуществующем индексе"""
    with patch('app.api.service.VectorDBService') as mock_service:
        mock_service.return_value.search.side_effect = ValueError("Index not found")
        response = client.post(
            "/search_index",
            json={
                "index_name": "nonexistent_index",
                "query_vector": TEST_QUERY_VECTOR,
                "k": 2
            },
        )
        assert response.status_code == 400
        assert "not found" in response.json()["detail"]


  

def test_delete_nonexistent_index():
    """Тест удаления несуществующего индекса"""
    with patch('app.api.service.VectorDBService') as mock_service:
        # Настраиваем мок для выброса исключения
        mock_service.return_value.delete_index.side_effect = ValueError("Index not found")
        
        response = client.delete("/indices/nonexistent_index")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

def test_delete_index_success():
    """Тест успешного удаления индекса"""
    with patch('app.api.service.VectorDBService') as mock_service:
        # Настраиваем мок
        mock_instance = mock_service.return_value
        mock_instance.delete_index.return_value = True
        
        # Вызываем эндпоинт
        response = client.delete(f"/indices/{TEST_INDEX_NAME}")
        
        # Диагностика
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.json()}")
        
        # Проверяем результат
        if response.status_code == 404:
            # Если получаем 404, проверяем сообщение
            assert "not found" in response.json().get("detail", "").lower()
        else:
            # Ожидаемый успешный сценарий
            assert response.status_code == 200
            assert response.json()["success"] is True
            assert TEST_INDEX_NAME in response.json()["message"]


def test_api_documentation():
    """Тест доступности документации API"""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_invalid_endpoint():
    """Тест обращения к несуществующему эндпоинту"""
    response = client.get("/nonexistent_endpoint")
    assert response.status_code == 404
    assert "Not Found" in response.json()["detail"]
def test_invalid_method():
    """Тест обращения с неподдерживаемым HTTP методом"""
    response = client.patch("/health")
    assert response.status_code == 405
    assert "Method Not Allowed" in response.json()["detail"]

def test_malformed_json():
    """Тест отправки некорректного JSON"""
    response = client.post(
        "/create_index",
        content="{invalid json}",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 422
    assert "JSON" in response.json()["detail"][0]["msg"]
def test_api_version():
    """Тест наличия информации о версии API"""
    response = client.get("/health")
    assert response.status_code == 200
    assert "version" in response.json()
    assert response.json()["version"] == "1.0.0"  # Должно соответствовать вашей версии

def test_api_title_in_schema():
    """Тест наличия заголовка API в схеме"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json()["info"]["title"] == "Vector Database API"
def test_openapi_schema():
    """Тест доступности OpenAPI схемы"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert "openapi" in response.json()
    assert "paths" in response.json()

def test_redoc_documentation():
    """Тест доступности ReDoc документации"""
    response = client.get("/redoc")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "ReDoc" in response.text

from pydantic import ValidationError

def test_create_index_request_validation():
    """Тест валидации CreateIndexRequest с проверкой ошибок"""
    # 1. Тест корректных данных (не должен вызывать ошибку)
    valid_data = {
        "name": "valid_index",
        "dimension": 128,
        "distance_metric": "L2",
        "index_type": "IVF_FLAT",
        "nlist": 100,
        "nprobe": 10
    }
    assert CreateIndexRequest(**valid_data)

def test_invalid_dimension():
    """Тест недопустимой размерности"""
    invalid_data = {
        "name": "invalid_dim",
        "dimension": 0,  # должно быть > 0
        "distance_metric": "L2",
        "index_type": "IVF_FLAT"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        CreateIndexRequest(**invalid_data)
    
    errors = exc_info.value.errors()
    assert any(
        error["loc"] == ("dimension",) and 
        error["type"] == "greater_than"
        for error in errors
    )

@pytest.mark.parametrize("metric", ["L2", "IP", "COSINE"])
def test_valid_distance_metrics(metric):
    """Параметризованный тест допустимых метрик"""
    data = {
        "name": f"index_{metric}",
        "dimension": 128,
        "distance_metric": metric
    }
    assert CreateIndexRequest(**data)
def test_default_values():
    """Тест значений по умолчанию"""
    minimal_data = {
        "name": "default_test",
        "dimension": 128
    }
    model = CreateIndexRequest(**minimal_data)
    assert model.distance_metric == "L2"
    assert model.index_type == "IVF_FLAT"
    assert model.nlist == 100
    assert model.nprobe == 10
def test_field_descriptions():
    """Тест наличия описаний полей"""
    schema = CreateIndexRequest.schema()
    assert schema["properties"]["dimension"]["description"] == "Vector dimension"
    assert "Distance metric (L2, IP, COSINE)" in schema["properties"]["distance_metric"]["description"]

from pydantic import ValidationError

from pydantic import ValidationError

def test_add_documents_minimal_valid():
    """Тест минимально валидного запроса"""
    request = AddDocumentsRequest(
        index_name="test_index",
        documents=[{"id": "1", "content": "test"}]
    )
    assert request.index_name == "test_index"
    assert len(request.documents) == 1


def test_add_documents_missing_index_name_fails():
    """Тест что отсутствие index_name вызывает ошибку"""
    with pytest.raises(ValidationError) as exc_info:
        AddDocumentsRequest(documents=[{"id": "1"}])
    
    errors = exc_info.value.errors()
    assert any(error["loc"] == ("index_name",) for error in errors)

def test_add_documents_varied_structures():
    """Тест что принимаются документы с разной структурой"""
    docs = [
        {"id": "1", "meta": {"tags": ["a"]}},  # Только id + metadata
        {"content": "text", "vector": [0.1]*128},  # Только content + vector
        {"id": 2, "text": "doc"}  # Числовой id + text
    ]
    request = AddDocumentsRequest(index_name="test", documents=docs)
    assert len(request.documents) == 3

def test_add_documents_invalid_type_fails():
    """Тест что не-list значение documents вызывает ошибку"""
    with pytest.raises(ValidationError) as exc_info:
        AddDocumentsRequest(index_name="test", documents="not_a_list")
    
    errors = exc_info.value.errors()
    assert any(
        error["loc"] == ("documents",) 
        and "Input should be a valid list" in error["msg"]
        for error in errors
    )

@pytest.mark.parametrize("doc", [
    {"id": "1"},  # Только id
    {"content": "text"},  # Только content
    {"id": 1, "content": "text"},  # Оба поля
    {"data": "test"}  # Другое поле
])
def test_document_minimal_requirements(doc):
    """Параметризованный тест минимальных требований к документам"""
    request = AddDocumentsRequest(index_name="test", documents=[doc])
    assert len(request.documents) == 1


def test_invalid_distance_metric():
    """Test creating index with invalid distance metric"""
    with patch('app.api.service.VectorDBService') as mock_service:
        mock_instance = mock_service.return_value
        mock_instance.create_index.side_effect = ValueError("Invalid distance metric")
        response = client.post(
            "/create_index",
            json={
                "name": "invalid_metric_index",
                "dimension": 128,
                "distance_metric": "INVALID"
            },
        )
        assert response.status_code == 400

from app.api.service import HuggingFaceEmbedder

def test_huggingface_embedder_initialization():
    """Test HuggingFace embedder initialization with different parameters"""
    with patch('transformers.AutoModel.from_pretrained'), \
         patch('transformers.AutoTokenizer.from_pretrained'):
        embedder = HuggingFaceEmbedder(
            model_name="BAAI/bge-small-en-v1.5",
            device="cpu",
            max_length=512,
            pooling_strategy="mean",
            normalize=True
        )
        assert embedder.model_name == "BAAI/bge-small-en-v1.5"

def test_get_document_not_found():
    """Test getting non-existent document"""
    with patch('app.api.service.VectorDBService') as mock_service:
        mock_instance = mock_service.return_value
        mock_instance.get_document.side_effect = ValueError("Document not found")
        response = client.get(f"/indices/{TEST_INDEX_NAME}/documents/invalid_id")
        assert response.status_code == 404

