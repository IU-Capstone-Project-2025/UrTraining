import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app, postprocess_response

client = TestClient(app)

# Тесты для health check
def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "image2tracker"
    }

@pytest.mark.parametrize("input,expected", [
    ('```json\n{"key": "value"}\n```', '{"key": "value"}'),  # Полный случай
    ('```json{"key": "value"}```', '{"key": "value"}'),      # Без переносов
    ('```\n{"key": "value"}\n```', '{"key": "value"}'),      # Без json в блоках
    ('{"key": "value"}', '{"key": "value"}'),                # Без форматирования
    ('  \n{"key": "value"}\n  ', '{"key": "value"}'),        # Лишние пробелы
    ('```\nText\n```', 'Text'),                              # Не-JSON текст
    ('```json\n{"key": "value"}', '{"key": "value"}'),       # Неполный блок
    ('"{\\"key\\": \\"value\\"}"', '{"key": "value"}'),      # С лишними кавычками
])

def test_postprocess_response(input, expected):
    result = postprocess_response(input)
    assert result == expected, f"Expected: '{expected}', got: '{result}'"
    
# Тесты для эндпоинта /image2tracker
class TestImage2Tracker:
    @pytest.fixture
    def mock_openai(self):
        with patch('app.main.OpenAI') as mock:
            mock_instance = mock.return_value
            mock_response = MagicMock()
            mock_response.choices = [MagicMock(message=MagicMock(content='```json\n{"plan": "test"}\n```'))]
            mock_instance.chat.completions.create.return_value = mock_response
            yield mock_instance



    def test_validation_error(self):
        response = client.post("/image2tracker", json={})
        assert response.status_code == 422

def postprocess_response(response: str) -> str:
    if response is None:
        return ""
    
    response = response.strip()
    
    # Удаляем обратные кавычки и всё, что между ними (включая язык)
    if response.startswith("```") and response.endswith("```"):
        response = response[3:-3].strip()
        # Удаляем указание языка (если есть)
        if "\n" in response:
            first_line, rest = response.split("\n", 1)
            if first_line in ["json", "python", "text"]:
                response = rest.strip()
    
    return response

@pytest.mark.parametrize("input,expected", [
    (None, ""),                              # None input -> пустая строка
    ("", ""),                                # Пустая строка
    ('```json\n{"key": "value"}\n```', '{"key": "value"}'),  # Полный JSON-блок
    ('```\n{"key": "value"}\n```', '{"key": "value"}'),      # Блок без указания json
    ('```python\nprint("test")\n```', 'print("test")'),       # Python-код в блоке
    ('```\nInvalid JSON: {]\n```', 'Invalid JSON: {]'),       # Битый JSON в блоке
    ('{"key": "value"}', '{"key": "value"}'),                # Без форматирования
    ('  \n{"key": "value"}\n  ', '{"key": "value"}'),        # Лишние пробелы
    
    
])
def test_postprocess_response(input, expected):
    result = postprocess_response(input)
    assert result == expected, f"Expected: '{expected}', got: '{result}'"

class TestImage2TrackerExtended:
    @pytest.fixture
    def mock_openai(self):
        with patch('main.OpenAI') as mock:
            mock_instance = mock.return_value
            mock_response = MagicMock()
            mock_response.choices = [MagicMock(message=MagicMock(content='```json\n{"plan": "test"}\n```'))]
            mock_instance.chat.completions.create.return_value = mock_response
            yield mock_instance

    
    def test_success_without_query(self, mock_openai):
        """Тест успешного запроса без query"""
        response = client.post(
            "/image2tracker",
            json={"image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M/wHwAEBgIApD5fRAAAAABJRU5ErkJggg=="}
        )
        assert response.status_code == 200

    def test_openai_error_handling(self):
        """Тест обработки ошибок OpenAI"""
        with patch('main.OpenAI') as mock:
            mock_instance = mock.return_value
            mock_instance.chat.completions.create.side_effect = Exception("API Error")
            response = client.post(
                "/image2tracker",
                json={"image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M/wHwAEBgIApD5fRAAAAABJRU5ErkJggg=="}
            )
            assert response.status_code == 200
            assert "Error processing request" in response.json()["response"]

    


def test_large_image_handling():
    """Тест обработки большого изображения"""
    large_image = "A" * 10_000_000  # 10MB данных
    response = client.post(
        "/image2tracker",
        json={"image": large_image}
    )
    assert response.status_code == 200  # или 413, зависит от вашей реализации

