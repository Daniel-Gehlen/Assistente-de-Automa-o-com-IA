"""
Orquestrador de agentes de IA usando LLMs locais (100% gratuito)
"""
from typing import Dict, Any, List
import logging
from .local_llm import LocalLLM

logger = logging.getLogger(__name__)


class LocalLLMAgent:
    """Agente de IA usando LLM local gratuito"""

    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.llm = LocalLLM()

    async def process(self, input_text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Processa uma tarefa com o LLM local"""
        try:
            prompt = f"""Você é um {self.role}.
Tarefa: {input_text}

Contexto: {context if context else 'Nenhum contexto adicional'}

Responda de forma clara e objetiva."""

            response = await self.llm.generate(prompt)

            return {
                "success": True,
                "output": response,
                "agent": self.name,
                "model": "llama3.2 (local)"
            }

        except Exception as e:
            logger.error(f"Erro no processamento: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }

    async def chat(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Chat interativo com histórico"""
        try:
            response = await self.llm.chat(messages)

            return {
                "success": True,
                "output": response,
                "agent": self.name
            }

        except Exception as e:
            logger.error(f"Erro no chat: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def health_check(self) -> bool:
        """Verifica saúde do agente"""
        return await self.llm.health_check()


class AgentOrchestrator:
    """Orquestrador de agentes usando LLMs locais (100% gratuito)"""

    def __init__(self):
        self.agents: Dict[str, LocalLLMAgent] = {}

    async def initialize(self):
        """Inicializa todos os agentes com modelos locais"""
        try:
            agents_config = [
                ("web_scraper", "Especialista em scraping web e extração de dados. Você ajuda a extrair informações de websites."),
                ("rpa_controller", "Especialista em automação RPA. Você cria scripts de automação para tarefas repetitivas."),
                ("data_analyst", "Especialista em análise de dados. Você analisa dados e gera insights."),
                ("task_orchestrator", "Especialista em orquestração. Você coordena tarefas complexas."),
                ("coding_assistant", "Assistente de programação. Você ajuda a escrever código Python para automação."),
                ("document_analyzer", "Analisador de documentos. Você extrai informações de textos e documentos.")
            ]

            for name, role in agents_config:
                agent = LocalLLMAgent(name, role)
                health = await agent.health_check()
                if health:
                    self.agents[name] = agent
                    logger.info(f"✅ Agente {name} registrado com LLM local")
                else:
                    logger.warning(f"⚠️ Agente {name} não disponível (LLM local não pronto)")

            if not self.agents:
                logger.warning("Nenhum agente disponível. Verifique se o Ollama está rodando.")
                await self._setup_fallback_agent()

            logger.info(f"Orquestrador inicializado com {len(self.agents)} agentes gratuitos")

        except Exception as e:
            logger.error(f"Erro na inicialização: {str(e)}")
            await self._setup_fallback_agent()

    async def _setup_fallback_agent(self):
        """Configura um agente fallback simples"""
        fallback = LocalLLMAgent("fallback", "Assistente geral")
        self.agents["fallback"] = fallback
        logger.info("✅ Agente fallback configurado")

    async def process_task(self, task: str, agent_name: str = None, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Processa uma tarefa usando o agente específico"""
        try:
            if agent_name:
                if agent_name not in self.agents:
                    return {
                        "success": False,
                        "error": f"Agente {agent_name} não encontrado. Agentes disponíveis: {list(self.agents.keys())}"
                    }
                agent = self.agents[agent_name]
            else:
                agent = await self._select_agent(task)

            result = await agent.process(task, context)
            return result

        except Exception as e:
            logger.error(f"Erro no processamento da tarefa: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def _select_agent(self, task: str) -> LocalLLMAgent:
        """Seleciona o agente mais adequado baseado em palavras-chave"""
        task_lower = task.lower()

        if any(keyword in task_lower for keyword in ["scrap", "extrair", "coletar", "web", "site"]):
            return self.agents.get("web_scraper", self.agents.get("fallback"))
        elif any(keyword in task_lower for keyword in ["autom", "rpa", "clicar", "preencher", "bot"]):
            return self.agents.get("rpa_controller", self.agents.get("fallback"))
        elif any(keyword in task_lower for keyword in ["analisar", "insight", "dados", "relatório", "gráfico"]):
            return self.agents.get("data_analyst", self.agents.get("fallback"))
        elif any(keyword in task_lower for keyword in ["código", "python", "programar", "script", "função"]):
            return self.agents.get("coding_assistant", self.agents.get("fallback"))
        elif any(keyword in task_lower for keyword in ["documento", "pdf", "texto", "resumo"]):
            return self.agents.get("document_analyzer", self.agents.get("fallback"))
        else:
            return self.agents.get("task_orchestrator", self.agents.get("fallback"))

    async def health_check(self) -> Dict[str, Any]:
        """Verifica saúde de todos os agentes"""
        health_status = {}

        for name, agent in self.agents.items():
            try:
                is_healthy = await agent.health_check()
                health_status[name] = "healthy" if is_healthy else "unhealthy"
            except Exception as e:
                health_status[name] = f"unhealthy: {str(e)}"

        return health_status
