"""
FastAPI - AI RPA Assistant (Versão 100% Gratuita - Hospedagem Otimizada)
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from typing import Dict, Any
import os

from backend.database.sqlite_client import SQLiteClient
from backend.services.ai.simple_agents import AgentOrchestrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sqlite_db = None
agent_orchestrator = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    global sqlite_db, agent_orchestrator

    logger.info("🚀 Iniciando aplicação 100% gratuita (versão otimizada)...")

    try:
        sqlite_db = SQLiteClient()
        await sqlite_db.connect()
        logger.info("✅ SQLite conectado (banco único e leve)")

        agent_orchestrator = AgentOrchestrator()
        await agent_orchestrator.initialize()
        logger.info("✅ Agentes de IA simplificados inicializados")

        logger.info("🎉 Todos os serviços gratuitos estão rodando!")

    except Exception as e:
        logger.error(f"❌ Erro na inicialização: {str(e)}")
        logger.warning("Alguns serviços podem não estar disponíveis")

    yield

    logger.info("Encerrando aplicação...")
    if sqlite_db:
        sqlite_db.close()
    logger.info("✅ Aplicação encerrada")


app = FastAPI(
    title="AI RPA Assistant - Versão 100% Gratuita",
    description="Assistente de automação com IA usando apenas ferramentas open-source",
    version="1.0.0-free",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "status": "online",
        "message": "AI RPA Assistant - Versão 100% Gratuita (Otimizada)",
        "version": "1.0.0-free-optimized",
        "features": {
            "sqlite": True,
            "simple_agents": True,
            "scraping": True,
            "tasks": True
        },
        "cost": "💰 100% GRATUITO - Hospedagem otimizada para plataformas gratuitas!"
    }


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Verifica saúde dos serviços"""
    health_status = {
        "api": "healthy",
        "services": {},
        "cost": "free"
    }

    if sqlite_db:
        try:
            await sqlite_db.health_check()
            health_status["services"]["sqlite"] = "healthy"
        except Exception:
            health_status["services"]["sqlite"] = "unhealthy"
            health_status["api"] = "degraded"

    if agent_orchestrator:
        try:
            agent_health = await agent_orchestrator.health_check()
            health_status["services"]["agents"] = agent_health
        except Exception:
            health_status["services"]["agents"] = "unhealthy"

    return health_status


@app.get("/models")
async def list_available_models():
    """Lista modelos/agentes disponíveis"""
    try:
        if agent_orchestrator:
            agents = agent_orchestrator.get_available_agents()
            return {
                "agents": agents,
                "total": len(agents),
                "message": "Agentes disponíveis (100% gratuitos)",
                "note": "Versão simplificada - usando regras predefinidas"
            }
        else:
            return {"error": "Agentes não inicializados"}
    except Exception as e:
        return {"error": f"Erro ao listar agentes: {str(e)}"}


@app.post("/api/agents/process")
async def process_agent_task(request: Dict[str, Any]):
    """Processa tarefa usando agente de IA"""
    try:
        task = request.get("task")
        agent_name = request.get("agent_name")
        context = request.get("context")

        if not task:
            raise HTTPException(status_code=400, detail="Campo 'task' é obrigatório")

        result = await agent_orchestrator.process_task(task, agent_name, context)
        return result

    except Exception as e:
        logger.error(f"Erro ao processar tarefa: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/agents/health")
async def agents_health():
    """Verifica saúde dos agentes"""
    try:
        health = await agent_orchestrator.health_check()
        return {"agents": health}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/tasks")
async def create_task(request: Dict[str, Any]):
    """Cria uma nova tarefa"""
    try:
        name = request.get("name")
        description = request.get("description")
        status = request.get("status", "pending")

        if not name:
            raise HTTPException(status_code=400, detail="Campo 'name' é obrigatório")

        task_id = await sqlite_db.insert_task(name, description, status)
        return {"task_id": task_id, "status": "created"}

    except Exception as e:
        logger.error(f"Erro ao criar tarefa: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tasks")
async def list_tasks(limit: int = 100):
    """Lista tarefas"""
    try:
        tasks = await sqlite_db.list_tasks(limit)
        return {"tasks": tasks, "total": len(tasks)}

    except Exception as e:
        logger.error(f"Erro ao listar tarefas: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tasks/{task_id}")
async def get_task(task_id: int):
    """Obtém uma tarefa por ID"""
    try:
        task = await sqlite_db.get_task(task_id)
        if task:
            return task
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter tarefa: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/tasks/{task_id}")
async def update_task(task_id: int, request: Dict[str, Any]):
    """Atualiza uma tarefa"""
    try:
        status = request.get("status")
        result = request.get("result")
        error = request.get("error")

        await sqlite_db.update_task(task_id, status, result, error)
        return {"status": "updated"}

    except Exception as e:
        logger.error(f"Erro ao atualizar tarefa: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/scraping")
async def save_scraped_data(request: Dict[str, Any]):
    """Salva dados de scraping"""
    try:
        url = request.get("url")
        data = request.get("data")
        metadata = request.get("metadata")

        if not url or not data:
            raise HTTPException(status_code=400, detail="Campos 'url' e 'data' são obrigatórios")

        doc_id = await sqlite_db.insert_scraped_data(url, data, metadata)
        return {"doc_id": doc_id, "status": "saved"}

    except Exception as e:
        logger.error(f"Erro ao salvar dados: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/scraping")
async def list_scraped_data(limit: int = 100):
    """Lista dados de scraping"""
    try:
        data = await sqlite_db.list_scraped_data(limit)
        return {"data": data, "total": len(data)}

    except Exception as e:
        logger.error(f"Erro ao listar dados: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/scraping/{url}")
async def get_scraped_data(url: str):
    """Obtém dados de scraping por URL"""
    try:
        data = await sqlite_db.get_scraped_data(url)
        if data:
            return data
        raise HTTPException(status_code=404, detail="Dados não encontrados")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter dados: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
