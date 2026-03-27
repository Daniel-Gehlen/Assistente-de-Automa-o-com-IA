"""
Testes para a API FastAPI
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.api.main import app


@pytest.fixture
def client():
    """Fixture para cliente de teste"""
    return TestClient(app)


@pytest.fixture
def mock_postgres():
    """Mock para PostgreSQL"""
    mock = AsyncMock()
    mock.connect = AsyncMock()
    mock.health_check = AsyncMock(return_value=True)
    mock.insert_task = AsyncMock(return_value=1)
    mock.list_tasks = AsyncMock(return_value=[
        {"id": 1, "name": "Teste", "description": "Descrição teste", "status": "pending"}
    ])
    mock.get_task = AsyncMock(return_value={"id": 1, "name": "Teste"})
    mock.update_task = AsyncMock()
    return mock


@pytest.fixture
def mock_mongodb():
    """Mock para MongoDB"""
    mock = AsyncMock()
    mock.connect = AsyncMock()
    mock.health_check = AsyncMock(return_value=True)
    mock.insert_scraped_data = AsyncMock(return_value="doc_id_123")
    mock.list_scraped_data = AsyncMock(return_value=[
        {"url": "https://example.com", "data": {"title": "Teste"}}
    ])
    mock.get_scraped_data = AsyncMock(return_value={"url": "https://example.com", "data": {}})
    return mock


@pytest.fixture
def mock_agent_orchestrator():
    """Mock para Agent Orchestrator"""
    mock = AsyncMock()
    mock.initialize = AsyncMock()
    mock.health_check = AsyncMock(return_value={
        "coding_assistant": "healthy",
        "web_scraper": "healthy"
    })
    mock.process_task = AsyncMock(return_value={
        "success": True,
        "output": "Resposta do agente",
        "agent": "coding_assistant",
        "model": "llama3.2 (local)"
    })
    return mock


def test_root_endpoint(client):
    """Testa endpoint raiz"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "100% Gratuita" in data["message"]


def test_health_endpoint(client):
    """Testa endpoint de saúde"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "api" in data
    assert "services" in data
    assert data["cost"] == "free"


def test_models_endpoint(client):
    """Testa endpoint de modelos"""
    with patch("backend.api.main.aiohttp") as mock_aiohttp:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "models": [
                {"name": "llama3.2", "size": 4000000000},
                {"name": "nomic-embed-text", "size": 274000000}
            ]
        })

        mock_session = AsyncMock()
        mock_session.get = AsyncMock(return_value=mock_response)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)

        mock_aiohttp.ClientSession = MagicMock(return_value=mock_session)

        response = client.get("/models")
        assert response.status_code == 200


def test_process_agent_task(client):
    """Testa processamento de tarefa de agente"""
    with patch("backend.api.main.agent_orchestrator") as mock_orchestrator:
        mock_orchestrator.process_task = AsyncMock(return_value={
            "success": True,
            "output": "Código Python gerado",
            "agent": "coding_assistant"
        })

        response = client.post("/api/agents/process", json={
            "task": "Crie uma função Python",
            "agent_name": "coding_assistant"
        })

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


def test_create_task(client):
    """Testa criação de tarefa"""
    with patch("backend.api.main.postgres_db") as mock_db:
        mock_db.insert_task = AsyncMock(return_value=1)

        response = client.post("/api/tasks", json={
            "name": "Nova tarefa",
            "description": "Descrição da tarefa"
        })

        assert response.status_code == 200
        data = response.json()
        assert data["task_id"] == 1


def test_list_tasks(client):
    """Testa listagem de tarefas"""
    with patch("backend.api.main.postgres_db") as mock_db:
        mock_db.list_tasks = AsyncMock(return_value=[
            {"id": 1, "name": "Tarefa 1", "status": "pending"},
            {"id": 2, "name": "Tarefa 2", "status": "completed"}
        ])

        response = client.get("/api/tasks")
        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) == 2


def test_save_scraped_data(client):
    """Testa salvamento de dados de scraping"""
    with patch("backend.api.main.mongodb_db") as mock_db:
        mock_db.insert_scraped_data = AsyncMock(return_value="doc_id_123")

        response = client.post("/api/scraping", json={
            "url": "https://example.com",
            "data": {"title": "Página de exemplo"}
        })

        assert response.status_code == 200
        data = response.json()
        assert data["doc_id"] == "doc_id_123"


def test_list_scraped_data(client):
    """Testa listagem de dados de scraping"""
    with patch("backend.api.main.mongodb_db") as mock_db:
        mock_db.list_scraped_data = AsyncMock(return_value=[
            {"url": "https://example.com", "data": {"title": "Teste"}}
        ])

        response = client.get("/api/scraping")
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 1
