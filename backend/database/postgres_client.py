"""
Cliente PostgreSQL para dados estruturados
"""
import os
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class PostgresClient:
    """Cliente para PostgreSQL"""

    def __init__(self):
        self.host = os.getenv("POSTGRES_HOST", "localhost")
        self.port = os.getenv("POSTGRES_PORT", "5432")
        self.database = os.getenv("POSTGRES_DB", "ai_rpa_db")
        self.user = os.getenv("POSTGRES_USER", "postgres")
        self.password = os.getenv("POSTGRES_PASSWORD", "postgres")
        self.connection = None

    async def connect(self):
        """Conecta ao PostgreSQL"""
        try:
            import psycopg2
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            logger.info("✅ PostgreSQL conectado")
            await self._create_tables()
        except Exception as e:
            logger.error(f"❌ Erro ao conectar PostgreSQL: {str(e)}")
            raise

    async def _create_tables(self):
        """Cria tabelas necessárias"""
        try:
            cursor = self.connection.cursor()

            # Tabela de tarefas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    status VARCHAR(50) DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    result JSONB,
                    error TEXT
                )
            """)

            # Tabela de logs de automação
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS automation_logs (
                    id SERIAL PRIMARY KEY,
                    task_id INTEGER REFERENCES tasks(id),
                    action VARCHAR(255),
                    status VARCHAR(50),
                    details JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Tabela de configurações
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    id SERIAL PRIMARY KEY,
                    key VARCHAR(255) UNIQUE NOT NULL,
                    value TEXT,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            self.connection.commit()
            cursor.close()
            logger.info("✅ Tabelas PostgreSQL criadas/verificadas")
        except Exception as e:
            logger.error(f"❌ Erro ao criar tabelas: {str(e)}")
            self.connection.rollback()

    async def insert_task(self, name: str, description: str, status: str = "pending") -> int:
        """Insere uma nova tarefa"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO tasks (name, description, status) VALUES (%s, %s, %s) RETURNING id",
                (name, description, status)
            )
            task_id = cursor.fetchone()[0]
            self.connection.commit()
            cursor.close()
            return task_id
        except Exception as e:
            logger.error(f"Erro ao inserir tarefa: {str(e)}")
            self.connection.rollback()
            return None

    async def update_task(self, task_id: int, status: str, result: Dict = None, error: str = None):
        """Atualiza uma tarefa"""
        try:
            cursor = self.connection.cursor()
            import json
            result_json = json.dumps(result) if result else None
            cursor.execute(
                "UPDATE tasks SET status = %s, result = %s, error = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
                (status, result_json, error, task_id)
            )
            self.connection.commit()
            cursor.close()
        except Exception as e:
            logger.error(f"Erro ao atualizar tarefa: {str(e)}")
            self.connection.rollback()

    async def get_task(self, task_id: int) -> Dict[str, Any]:
        """Obtém uma tarefa por ID"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
            columns = [desc[0] for desc in cursor.description]
            row = cursor.fetchone()
            cursor.close()
            if row:
                return dict(zip(columns, row))
            return None
        except Exception as e:
            logger.error(f"Erro ao obter tarefa: {str(e)}")
            return None

    async def list_tasks(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Lista tarefas"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC LIMIT %s", (limit,))
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            cursor.close()
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            logger.error(f"Erro ao listar tarefas: {str(e)}")
            return []

    async def insert_automation_log(self, task_id: int, action: str, status: str, details: Dict = None):
        """Insere log de automação"""
        try:
            cursor = self.connection.cursor()
            import json
            details_json = json.dumps(details) if details else None
            cursor.execute(
                "INSERT INTO automation_logs (task_id, action, status, details) VALUES (%s, %s, %s, %s)",
                (task_id, action, status, details_json)
            )
            self.connection.commit()
            cursor.close()
        except Exception as e:
            logger.error(f"Erro ao inserir log: {str(e)}")
            self.connection.rollback()

    async def get_setting(self, key: str) -> Optional[str]:
        """Obtém uma configuração"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT value FROM settings WHERE key = %s", (key,))
            row = cursor.fetchone()
            cursor.close()
            return row[0] if row else None
        except Exception as e:
            logger.error(f"Erro ao obter configuração: {str(e)}")
            return None

    async def set_setting(self, key: str, value: str, description: str = None):
        """Define uma configuração"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO settings (key, value, description) VALUES (%s, %s, %s) ON CONFLICT (key) DO UPDATE SET value = %s, updated_at = CURRENT_TIMESTAMP",
                (key, value, description, value)
            )
            self.connection.commit()
            cursor.close()
        except Exception as e:
            logger.error(f"Erro ao definir configuração: {str(e)}")
            self.connection.rollback()

    async def health_check(self) -> bool:
        """Verifica saúde do PostgreSQL"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            return True
        except Exception as e:
            logger.error(f"PostgreSQL health check falhou: {str(e)}")
            return False

    async def close(self):
        """Fecha conexão"""
        if self.connection:
            self.connection.close()
            logger.info("PostgreSQL desconectado")
