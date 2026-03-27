from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from enum import Enum

class AgentType(str, Enum):
    CODING_ASSISTANT = "coding_assistant"
    WEB_SCRAPER = "web_scraper"
    DATA_ANALYST = "data_analyst"
    RPA_CONTROLLER = "rpa_controller"
    DOCUMENT_ANALYZER = "document_analyzer"
    TASK_ORCHESTRATOR = "task_orchestrator"

class AgentRequest(BaseModel):
    task: str = Field(..., min_length=1, description="Tarefa a ser executada")
    agent_name: Optional[AgentType] = Field(None, description="Nome do agente")
    context: Optional[Dict[str, Any]] = Field(None, description="Contexto adicional")

class AgentResponse(BaseModel):
    success: bool
    output: Optional[str] = None
    agent: str
    model: Optional[str] = None
    error: Optional[str] = None

class AgentHealth(BaseModel):
    agents: Dict[str, str]
