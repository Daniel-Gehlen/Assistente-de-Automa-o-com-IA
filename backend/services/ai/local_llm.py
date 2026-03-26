"""
Serviço de LLM local usando Ollama (100% gratuito)
"""
import aiohttp
import asyncio
from typing import Dict, Any, List, Optional
import logging
import os

logger = logging.getLogger(__name__)


class LocalLLM:
    """Cliente para LLM local usando Ollama"""

    def __init__(self):
        self.base_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = os.getenv("LLM_MODEL", "llama3.2")
        self.embedding_model = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")

    async def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """Gera texto usando modelo local"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "temperature": temperature
                    }
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("response", "")
                    else:
                        logger.error(f"Erro na geração: {response.status}")
                        return ""
        except Exception as e:
            logger.error(f"Erro ao gerar texto: {str(e)}")
            return ""

    async def chat(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """Chat com histórico usando modelo local"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/chat",
                    json={
                        "model": self.model,
                        "messages": messages,
                        "stream": False,
                        "temperature": temperature
                    }
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("message", {}).get("content", "")
                    else:
                        logger.error(f"Erro no chat: {response.status}")
                        return ""
        except Exception as e:
            logger.error(f"Erro no chat: {str(e)}")
            return ""

    async def get_embeddings(self, text: str) -> List[float]:
        """Gera embeddings usando modelo local"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/embeddings",
                    json={
                        "model": self.embedding_model,
                        "prompt": text
                    }
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("embedding", [])
                    else:
                        logger.error(f"Erro nos embeddings: {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Erro ao gerar embeddings: {str(e)}")
            return []

    async def health_check(self) -> bool:
        """Verifica se o serviço está saudável"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/tags") as response:
                    if response.status == 200:
                        data = await response.json()
                        models = data.get("models", [])
                        if any(m.get("name", "").startswith(self.model) for m in models):
                            logger.info(f"Modelo {self.model} disponível")
                            return True
                        else:
                            logger.warning(f"Modelo {self.model} não encontrado")
                            return False
                    return False
        except Exception as e:
            logger.error(f"Health check falhou: {str(e)}")
            return False
