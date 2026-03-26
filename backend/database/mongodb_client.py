"""
Cliente MongoDB para dados não estruturados
"""
import os
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class MongoDBClient:
    """Cliente para MongoDB"""

    def __init__(self):
        self.uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        self.database_name = os.getenv("MONGODB_DB", "ai_rpa_db")
        self.client = None
        self.db = None

    async def connect(self):
        """Conecta ao MongoDB"""
        try:
            import pymongo
            self.client = pymongo.MongoClient(self.uri)
            self.db = self.client[self.database_name]
            logger.info("✅ MongoDB conectado")
            await self._create_collections()
        except Exception as e:
            logger.error(f"❌ Erro ao conectar MongoDB: {str(e)}")
            raise

    async def _create_collections(self):
        """Cria coleções necessárias"""
        try:
            # Coleção de dados de scraping
            if "scraped_data" not in self.db.list_collection_names():
                self.db.create_collection("scraped_data")
                self.db.scraped_data.create_index("url")
                self.db.scraped_data.create_index("created_at")

            # Coleção de dados de agentes
            if "agent_data" not in self.db.list_collection_names():
                self.db.create_collection("agent_data")
                self.db.agent_data.create_index("agent_name")
                self.db.agent_data.create_index("created_at")

            # Coleção de embeddings
            if "embeddings" not in self.db.list_collection_names():
                self.db.create_collection("embeddings")
                self.db.embeddings.create_index("text_hash", unique=True)

            # Coleção de cache
            if "cache" not in self.db.list_collection_names():
                self.db.create_collection("cache")
                self.db.cache.create_index("key", unique=True)
                self.db.cache.create_index("expires_at", expireAfterSeconds=0)

            logger.info("✅ Coleções MongoDB criadas/verificadas")
        except Exception as e:
            logger.error(f"❌ Erro ao criar coleções: {str(e)}")

    async def insert_scraped_data(self, url: str, data: Dict[str, Any], metadata: Dict = None) -> str:
        """Insere dados de scraping"""
        try:
            document = {
                "url": url,
                "data": data,
                "metadata": metadata or {},
                "created_at": datetime.utcnow()
            }
            result = self.db.scraped_data.insert_one(document)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Erro ao inserir dados de scraping: {str(e)}")
            return None

    async def get_scraped_data(self, url: str) -> Optional[Dict[str, Any]]:
        """Obtém dados de scraping por URL"""
        try:
            return self.db.scraped_data.find_one({"url": url})
        except Exception as e:
            logger.error(f"Erro ao obter dados de scraping: {str(e)}")
            return None

    async def list_scraped_data(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Lista dados de scraping"""
        try:
            return list(self.db.scraped_data.find().sort("created_at", -1).limit(limit))
        except Exception as e:
            logger.error(f"Erro ao listar dados de scraping: {str(e)}")
            return []

    async def insert_agent_data(self, agent_name: str, data: Dict[str, Any], metadata: Dict = None) -> str:
        """Insere dados de agente"""
        try:
            document = {
                "agent_name": agent_name,
                "data": data,
                "metadata": metadata or {},
                "created_at": datetime.utcnow()
            }
            result = self.db.agent_data.insert_one(document)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Erro ao inserir dados de agente: {str(e)}")
            return None

    async def get_agent_data(self, agent_name: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Obtém dados de agente por nome"""
        try:
            return list(self.db.agent_data.find({"agent_name": agent_name}).sort("created_at", -1).limit(limit))
        except Exception as e:
            logger.error(f"Erro ao obter dados de agente: {str(e)}")
            return []

    async def store_embedding(self, text: str, embedding: List[float], metadata: Dict = None) -> str:
        """Armazena embedding"""
        try:
            import hashlib
            text_hash = hashlib.md5(text.encode()).hexdigest()

            document = {
                "text": text,
                "text_hash": text_hash,
                "embedding": embedding,
                "metadata": metadata or {},
                "created_at": datetime.utcnow()
            }

            result = self.db.embeddings.update_one(
                {"text_hash": text_hash},
                {"$set": document},
                upsert=True
            )
            return text_hash
        except Exception as e:
            logger.error(f"Erro ao armazenar embedding: {str(e)}")
            return None

    async def get_embedding(self, text: str) -> Optional[List[float]]:
        """Obtém embedding por texto"""
        try:
            import hashlib
            text_hash = hashlib.md5(text.encode()).hexdigest()
            result = self.db.embeddings.find_one({"text_hash": text_hash})
            return result["embedding"] if result else None
        except Exception as e:
            logger.error(f"Erro ao obter embedding: {str(e)}")
            return None

    async def set_cache(self, key: str, value: Any, ttl_seconds: int = 3600):
        """Define cache com TTL"""
        try:
            from datetime import timedelta
            expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)

            document = {
                "key": key,
                "value": value,
                "expires_at": expires_at
            }

            self.db.cache.update_one(
                {"key": key},
                {"$set": document},
                upsert=True
            )
        except Exception as e:
            logger.error(f"Erro ao definir cache: {str(e)}")

    async def get_cache(self, key: str) -> Optional[Any]:
        """Obtém valor do cache"""
        try:
            result = self.db.cache.find_one({"key": key})
            if result and result.get("expires_at"):
                if result["expires_at"] > datetime.utcnow():
                    return result["value"]
                else:
                    self.db.cache.delete_one({"key": key})
            return None
        except Exception as e:
            logger.error(f"Erro ao obter cache: {str(e)}")
            return None

    async def delete_cache(self, key: str):
        """Deleta cache"""
        try:
            self.db.cache.delete_one({"key": key})
        except Exception as e:
            logger.error(f"Erro ao deletar cache: {str(e)}")

    async def health_check(self) -> bool:
        """Verifica saúde do MongoDB"""
        try:
            self.client.admin.command('ping')
            return True
        except Exception as e:
            logger.error(f"MongoDB health check falhou: {str(e)}")
            return False

    async def close(self):
        """Fecha conexão"""
        if self.client:
            self.client.close()
            logger.info("MongoDB desconectado")
