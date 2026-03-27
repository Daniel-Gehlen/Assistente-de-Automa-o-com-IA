#!/bin/bash
# Script de setup para AI RPA Assistant - Versão 100% Gratuita
set -e

echo "🚀 Configurando AI RPA Assistant (Versão 100% Gratuita)..."

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.10+"
    exit 1
fi

# Verificar versão do Python
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Versão do Python $PYTHON_VERSION é inferior à mínima requerida ($REQUIRED_VERSION)"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION encontrado"

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
    echo "✅ Ambiente virtual criado"
else
    echo "✅ Ambiente virtual já existe"
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Atualizar pip
echo "⬆️ Atualizando pip..."
pip install --upgrade pip

# Instalar dependências
echo "📚 Instalando dependências..."
pip install -r requirements.txt

# Instalar Playwright
echo "🎭 Instalando Playwright..."
playwright install chromium

# Criar arquivo .env se não existir
if [ ! -f ".env" ]; then
    echo "⚙️ Criando arquivo .env..."
    cat > .env << EOF
# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ai_rpa_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# MongoDB
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=ai_rpa_db

# Redis
REDIS_HOST=localhost

# Ollama
OLLAMA_HOST=http://localhost:11434
USE_LOCAL_LLM=true
LLM_MODEL=llama3.2
EMBEDDING_MODEL=nomic-embed-text

# Selenium
SELENIUM_HEADLESS=true

# Playwright
PLAYWRIGHT_HEADLESS=true
EOF
    echo "✅ Arquivo .env criado"
else
    echo "✅ Arquivo .env já existe"
fi

echo ""
echo "🎉 Setup concluído com sucesso!"
echo ""
echo "📋 Próximos passos:"
echo "1. Iniciar containers: make docker-up"
echo "2. Baixar modelos Ollama: make setup-ollama"
echo "3. Executar aplicação: make run"
echo ""
echo "💰 Lembrete: Este projeto é 100% gratuito!"
