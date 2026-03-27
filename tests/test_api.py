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
    from unittest.mock import AsyncMock, MagicMock

    # Mock do SQLite
    mock_sqlite = AsyncMock()
    mock_sqlite.connect = AsyncMock()
    mock_sqlite.health_check = AsyncMock(return_value=True)
    mock_sqlite.insert_task = AsyncMock(return_value=1)
    mock_sqlite.list_tasks = AsyncMock(return_value=[
        {"id": 1, "name": "Teste", "description": "Descrição teste", "status": "pending"}
    ])
    mock_sqlite.get_task = AsyncMock(return_value={"id": 1, "name": "Teste"})
    mock_sqlite.update_task = AsyncMock()
    mock_sqlite.insert_scraped_data = AsyncMock(return_value="doc_id_123")
    mock_sqlite.list_scraped_data = AsyncMock(return_value=[
        {"url": "https://example.com", "data": {"title": "Teste"}}
    ])
    mock_sqlite.get_scraped_data = AsyncMock(return_value={"url": "https://example.com", "data": {}})

    # Mock do Agent Orchestrator
    mock_agents = AsyncMock()
    mock_agents.initialize = AsyncMock()
    mock_agents.health_check = AsyncMock(return_value={
        "coding_assistant": "healthy",
        "web_scraper": "healthy"
    })
    mock_agents.process_task = AsyncMock(return_value={
        "success": True,
        "output": "Resposta do agente",
        "agent": "coding_assistant",
        "model": "rules-based (gratuito)"
    })
    mock_agents.get_available_agents = MagicMock(return_value=["coding_assistant", "web_scraper", "data_analyst"])

    # Injetar mocks no módulo
    import backend.api.main as main_module
    original_sqlite = main_module.sqlite_db
    original_agents = main_module.agent_orchestrator

    main_module.sqlite_db = mock_sqlite
    main_module.agent_orchestrator = mock_agents

    with TestClient(app) as test_client:
        yield test_client

    # Restaurar originais
    main_module.sqlite_db = original_sqlite
    main_module.agent_orchestrator = original_agents


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
    response = client.get("/models")
    assert response.status_code == 200
    data = response.json()
    assert "agents" in data
    assert "total" in data


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
    response = client.post("/api/tasks", json={
        "name": "Nova tarefa",
        "description": "Descrição da tarefa"
    })

    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data


def test_list_tasks(client):
    """Testa listagem de tarefas"""
    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = response.json()
    assert "tasks" in data


def test_save_scraped_data(client):
    """Testa salvamento de dados de scraping"""
    response = client.post("/api/scraping", json={
        "url": "https://example.com",
        "data": {"title": "Página de exemplo"}
    })

    assert response.status_code == 200
    data = response.json()
    assert "doc_id" in data


def test_list_scraped_data(client):
    """Testa listagem de dados de scraping"""
    response = client.get("/api/scraping")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
