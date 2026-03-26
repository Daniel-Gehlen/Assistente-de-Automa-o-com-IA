.PHONY: help install run test docker-up docker-down lint format clean health

help:
	@echo "Comandos disponíveis (Versão Gratuita):"
	@echo "  make install      - Instala dependências"
	@echo "  make run          - Roda a aplicação"
	@echo "  make docker-up    - Sobe containers (PostgreSQL, MongoDB, Ollama)"
	@echo "  make docker-down  - Derruba containers"
	@echo "  make test         - Executa testes"
	@echo "  make lint         - Verifica código"
	@echo "  make format       - Formata código"
	@echo "  make clean        - Limpa cache e arquivos temporários"
	@echo "  make health       - Verifica saúde dos serviços"
	@echo "  make models       - Lista modelos disponíveis no Ollama"

install:
	python3 -m venv venv
	source venv/bin/activate && pip install --upgrade pip
	source venv/bin/activate && pip install -r requirements.txt
	source venv/bin/activate && playwright install chromium
	@echo "✅ Dependências instaladas"

run:
	source venv/bin/activate && uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload

docker-up:
	docker-compose up -d
	@echo "Aguardando serviços..."
	sleep 15
	@echo "✅ Serviços rodando:"
	@echo "  - PostgreSQL: localhost:5432"
	@echo "  - MongoDB: localhost:27017"
	@echo "  - Ollama: localhost:11434"
	@echo "  - API: localhost:8000"

docker-down:
	docker-compose down
	@echo "✅ Containers parados"

test:
	source venv/bin/activate && pytest tests/ -v --cov=backend --cov-report=term-missing

lint:
	source venv/bin/activate && flake8 backend/ --max-line-length=120 --ignore=E203,W503
	source venv/bin/activate && black backend/ --check

format:
	source venv/bin/activate && black backend/
	source venv/bin/activate && isort backend/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.log" -delete 2>/dev/null || true
	@echo "✅ Cache limpo"

health:
	@curl -s http://localhost:8000/health | python3 -m json.tool || echo "API não está rodando"

models:
	@curl -s http://localhost:11434/api/tags | python3 -m json.tool || echo "Ollama não está rodando"

test-llm:
	@echo "Testando LLM local..."
	@curl -X POST http://localhost:11434/api/generate -d '{"model": "llama3.2", "prompt": "Olá, como você está?", "stream": false}' | python3 -m json.tool || echo "Ollama não está rodando"

setup-ollama:
	@echo "Baixando modelos..."
	curl -X POST http://localhost:11434/api/pull -d '{"name": "llama3.2"}'
	curl -X POST http://localhost:11434/api/pull -d '{"name": "nomic-embed-text"}'
	@echo "✅ Modelos baixados"
