"""
Entry point para Vercel - FastAPI Application
"""
import sys
import os

# Adicionar o diretório atual ao path para imports funcionarem
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar a aplicação FastAPI
from backend.api.main import app

# Exportar para Vercel encontrar
__all__ = ['app']
