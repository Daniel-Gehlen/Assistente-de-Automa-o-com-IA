"""
Agentes de IA Simplificados - Versão 100% Gratuita
Usa apenas bibliotecas leves e APIs gratuitas
"""
import logging
import json
import re
from typing import Dict, Any, Optional
import httpx
import os

logger = logging.getLogger(__name__)


class SimpleAgent:
    """Agente de IA simplificado usando APIs gratuitas"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.api_key = os.getenv("OPENAI_API_KEY")  # Opcional - pode ser None
        self.use_free_api = not self.api_key

    async def process(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Processa tarefa usando IA ou regras predefinidas"""
        try:
            if self.use_free_api:
                return await self._process_with_rules(task, context)
            else:
                return await self._process_with_api(task, context)
        except Exception as e:
            logger.error(f"❌ Erro no agente {self.name}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }

    async def _process_with_rules(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Processa tarefa usando regras predefinidas (100% gratuito)"""
        task_lower = task.lower()

        # Agente de código
        if self.name == "coding_assistant":
            if "python" in task_lower or "função" in task_lower:
                return {
                    "success": True,
                    "output": self._generate_python_function(task),
                    "agent": self.name,
                    "model": "rules-based (gratuito)"
                }
            elif "html" in task_lower or "página" in task_lower:
                return {
                    "success": True,
                    "output": self._generate_html_page(task),
                    "agent": self.name,
                    "model": "rules-based (gratuito)"
                }
            else:
                return {
                    "success": True,
                    "output": f"Para a tarefa: '{task}', recomendo dividir em etapas menores e implementar cada uma separadamente.",
                    "agent": self.name,
                    "model": "rules-based (gratuito)"
                }

        # Agente de scraping
        elif self.name == "web_scraper":
            return {
                "success": True,
                "output": f"Para scraping de '{task}', use requests + BeautifulSoup. URL de exemplo: https://example.com",
                "agent": self.name,
                "model": "rules-based (gratuito)"
            }

        # Agente de análise
        elif self.name == "data_analyst":
            return {
                "success": True,
                "output": f"Para análise de dados sobre '{task}', recomendo usar pandas para processamento e matplotlib para visualização.",
                "agent": self.name,
                "model": "rules-based (gratuito)"
            }

        return {
            "success": True,
            "output": f"Tarefa '{task}' processada com sucesso usando regras predefinidas.",
            "agent": self.name,
            "model": "rules-based (gratuito)"
        }

    async def _process_with_api(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Processa tarefa usando API OpenAI (se configurada)"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-3.5-turbo",
                        "messages": [
                            {"role": "system", "content": f"Você é um assistente especializado em {self.description}"},
                            {"role": "user", "content": task}
                        ],
                        "max_tokens": 500
                    },
                    timeout=30.0
                )

                if response.status_code == 200:
                    data = response.json()
                    output = data["choices"][0]["message"]["content"]
                    return {
                        "success": True,
                        "output": output,
                        "agent": self.name,
                        "model": "gpt-3.5-turbo"
                    }
                else:
                    raise Exception(f"API retornou status {response.status_code}")

        except Exception as e:
            logger.warning(f"⚠️ API OpenAI falhou, usando regras: {str(e)}")
            return await self._process_with_rules(task, context)

    def _generate_python_function(self, task: str) -> str:
        """Gera função Python baseada na descrição"""
        # Extrair nome da função da tarefa
        func_match = re.search(r'função\s+(\w+)', task.lower())
        func_name = func_match.group(1) if func_match else "minha_funcao"

        return f'''def {func_name}():
    """
    Função gerada automaticamente
    Tarefa: {task}
    """
    # TODO: Implementar lógica específica
    print("Função {func_name} executada com sucesso!")
    return True

# Exemplo de uso:
# resultado = {func_name}()
'''

    def _generate_html_page(self, task: str) -> str:
        """Gera página HTML básica"""
        return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Página Gerada</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Página HTML Gerada</h1>
        <p>Tarefa: {task}</p>
        <p>Esta página foi gerada automaticamente pelo agente de código.</p>
    </div>
</body>
</html>
'''


class AgentOrchestrator:
    """Orquestrador de agentes simplificado"""

    def __init__(self):
        self.agents = {}
        self.initialized = False

    async def initialize(self):
        """Inicializa agentes"""
        try:
            self.agents = {
                "coding_assistant": SimpleAgent(
                    "coding_assistant",
                    "geração de código e programação"
                ),
                "web_scraper": SimpleAgent(
                    "web_scraper",
                    "web scraping e extração de dados"
                ),
                "data_analyst": SimpleAgent(
                    "data_analyst",
                    "análise de dados e visualização"
                )
            }
            self.initialized = True
            logger.info("✅ Agentes simplificados inicializados")
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar agentes: {str(e)}")
            raise

    async def health_check(self) -> Dict[str, str]:
        """Verifica saúde dos agentes"""
        if not self.initialized:
            return {"status": "not_initialized"}

        health = {}
        for name, agent in self.agents.items():
            health[name] = "healthy" if agent else "unhealthy"
        return health

    async def process_task(self, task: str, agent_name: str = None, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Processa tarefa usando agente específico"""
        if not self.initialized:
            raise Exception("Agentes não inicializados")

        # Selecionar agente
        if agent_name and agent_name in self.agents:
            agent = self.agents[agent_name]
        else:
            # Auto-selecionar agente baseado na tarefa
            agent = self._select_agent(task)

        # Processar tarefa
        return await agent.process(task, context)

    def _select_agent(self, task: str) -> SimpleAgent:
        """Seleciona agente mais adequado para a tarefa"""
        task_lower = task.lower()

        if any(word in task_lower for word in ["código", "python", "função", "programar", "html", "css"]):
            return self.agents["coding_assistant"]
        elif any(word in task_lower for word in ["scraping", "extrair", "website", "dados web"]):
            return self.agents["web_scraper"]
        elif any(word in task_lower for word in ["análise", "dados", "gráfico", "estatística"]):
            return self.agents["data_analyst"]
        else:
            return self.agents["coding_assistant"]  # Padrão

    def get_available_agents(self) -> list:
        """Lista agentes disponíveis"""
        return list(self.agents.keys())
