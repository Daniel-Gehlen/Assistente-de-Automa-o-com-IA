"""
Cliente SQLite - Banco de dados único e leve para hospedagem gratuita
"""
import sqlite3
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import os

logger = logging.getLogger(__name__)


class SQLiteClient:
    """Cliente SQLite unificado para tarefas e dados de scraping"""

    def __init__(self, db_path: str = "data/app.db"):
        self.db_path = db_path
        self.connection = None
        # Criar diretório se não existir
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

    async def connect(self):
        """Conecta ao banco de dados SQLite"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Para retornar dicionários
            await self._create_tables()
            logger.info(f"✅ SQLite conectado: {self.db_path}")
        except Exception as e:
            logger.error(f"❌ Erro ao conectar SQLite: {str(e)}")
            raise

    async def _create_tables(self):
        """Cria tabelas necessárias"""
        cursor = self.connection.cursor()

        # Tabela de tarefas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'pending',
                result TEXT,
                error TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Tabela de dados de scraping
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scraped_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL UNIQUE,
                data TEXT NOT NULL,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Tabela de cache
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cache (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                expires_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.connection.commit()
        logger.info("✅ Tabelas SQLite criadas/verificadas")

    async def health_check(self) -> bool:
        """Verifica saúde do banco"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            return True
        except Exception:
            return False

    # ==================== TAREFAS ====================

    async def insert_task(self, name: str, description: str = None, status: str = "pending") -> int:
        """Insere uma nova tarefa"""
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO tasks (name, description, status) VALUES (?, ?, ?)",
            (name, description, status)
        )
        self.connection.commit()
        task_id = cursor.lastrowid
        logger.info(f"✅ Tarefa criada: ID {task_id}")
        return task_id

    async def list_tasks(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Lista tarefas"""
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM tasks ORDER BY created_at DESC LIMIT ?",
            (limit,)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    async def get_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Obtém tarefa por ID"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    async def update_task(self, task_id: int, status: str = None, result: str = None, error: str = None):
        """Atualiza uma tarefa"""
        cursor = self.connection.cursor()
        updates = []
        params = []

        if status is not None:
            updates.append("status = ?")
            params.append(status)
        if result is not None:
            updates.append("result = ?")
            params.append(result)
        if error is not None:
            updates.append("error = ?")
            params.append(error)

        updates.append("updated_at = ?")
        params.append(datetime.now().isoformat())
        params.append(task_id)

        query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        self.connection.commit()
        logger.info(f"✅ Tarefa {task_id} atualizada")

    # ==================== DADOS DE SCRAPING ====================

    async def insert_scraped_data(self, url: str, data: Dict[str, Any], metadata: Dict[str, Any] = None) -> str:
        """Insere dados de scraping"""
        cursor = self.connection.cursor()
        data_json = json.dumps(data, ensure_ascii=False)
        metadata_json = json.dumps(metadata, ensure_ascii=False) if metadata else None

        cursor.execute(
            "INSERT OR REPLACE INTO scraped_data (url, data, metadata) VALUES (?, ?, ?)",
            (url, data_json, metadata_json)
        )
        self.connection.commit()
        doc_id = str(cursor.lastrowid)
        logger.info(f"✅ Dados de scraping salvos: {url}")
        return doc_id

    async def list_scraped_data(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Lista dados de scraping"""
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM scraped_data ORDER BY created_at DESC LIMIT ?",
            (limit,)
        )
        rows = cursor.fetchall()
        result = []
        for row in rows:
            data = dict(row)
            data['data'] = json.loads(data['data'])
            if data['metadata']:
                data['metadata'] = json.loads(data['metadata'])
            result.append(data)
        return result

    async def get_scraped_data(self, url: str) -> Optional[Dict[str, Any]]:
        """Obtém dados de scraping por URL"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM scraped_data WHERE url = ?", (url,))
        row = cursor.fetchone()
        if row:
            data = dict(row)
            data['data'] = json.loads(data['data'])
            if data['metadata']:
                data['metadata'] = json.loads(data['metadata'])
            return data
        return None

    # ==================== CACHE ====================

    async def set_cache(self, key: str, value: Any, expires_in_seconds: int = 3600):
        """Define valor no cache"""
        cursor = self.connection.cursor()
        value_json = json.dumps(value, ensure_ascii=False)
        expires_at = datetime.now().timestamp() + expires_in_seconds

        cursor.execute(
            "INSERT OR REPLACE INTO cache (key, value, expires_at) VALUES (?, ?, ?)",
            (key, value_json, expires_at)
        )
        self.connection.commit()

    async def get_cache(self, key: str) -> Optional[Any]:
        """Obtém valor do cache"""
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT value, expires_at FROM cache WHERE key = ?",
            (key,)
        )
        row = cursor.fetchone()
        if row:
            value_json, expires_at = row
            if expires_at and datetime.now().timestamp() > expires_at:
                # Cache expirado
                cursor.execute("DELETE FROM cache WHERE key = ?", (key,))
                self.connection.commit()
                return None
            return json.loads(value_json)
        return None

    async def delete_cache(self, key: str):
        """Remove valor do cache"""
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM cache WHERE key = ?", (key,))
        self.connection.commit()

    async def clear_expired_cache(self):
        """Remove cache expirado"""
        cursor = self.connection.cursor()
        cursor.execute(
            "DELETE FROM cache WHERE expires_at IS NOT NULL AND expires_at < ?",
            (datetime.now().timestamp(),)
        )
        self.connection.commit()
        logger.info("✅ Cache expirado limpo")

    def close(self):
        """Fecha conexão"""
        if self.connection:
            self.connection.close()
            logger.info("✅ SQLite desconectado")
