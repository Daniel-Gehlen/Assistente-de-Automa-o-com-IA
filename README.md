# AI RPA Assistant

Este projeto utiliza apenas ferramentas **open-source**:

| Componente | Tecnologia |
|------------|------------|
| API | FastAPI |
| Banco de Dados SQL | PostgreSQL |
| Banco de Dados NoSQL | MongoDB |
| LLM (IA) | Ollama + Llama 3.2 |
| RPA | Selenium + Playwright |
| Containerização | Docker |
| Agentes IA | Implementação própria |

## 🚀 Instalação

### Pré-requisitos
- Docker e Docker Compose
- Python 3.10+
- 8GB RAM mínimo (16GB recomendado)

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/Daniel-Gehlen/Assistente-de-Automa-o-com-IA.git
cd Assistente-de-Automação-com-IA

# 2. Suba os containers
make docker-up

# 3. Instale as dependências
make install

# 4. Rode a aplicação
make run
```

## 🤖 Modelos de IA Disponíveis

O sistema usa **Ollama** para rodar LLMs localmente:

- **llama3.2** - Modelo base (7B parâmetros)
- **mistral** - Alternativa leve
- **phi3** - Modelo pequeno e rápido
- **nomic-embed-text** - Para embeddings

Para baixar outros modelos:
```bash
make setup-ollama
```

## 🎯 Funcionalidades

### 1. Agentes de IA Locais
- **Web Scraper**: Extrai dados de sites
- **RPA Controller**: Automatiza tarefas repetitivas
- **Data Analyst**: Analisa dados e gera insights
- **Coding Assistant**: Ajuda a escrever código
- **Document Analyzer**: Analisa documentos

### 2. Automação RPA
- Selenium: Automação web
- Playwright: Automação multi-browser
- PyAutoGUI: Automação de interface gráfica

### 3. Bancos de Dados
- PostgreSQL: Dados estruturados
- MongoDB: Dados não estruturados

## 🔧 Exemplos de Uso

### Testar LLM Local
```bash
make test-llm
```

### Usar Agente via API
```bash
curl -X POST http://localhost:8000/api/agents/process \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Crie um script Python para extrair títulos de uma página web",
    "agent_name": "coding_assistant"
  }'
```

### Verificar Saúde dos Serviços
```bash
make health
```

### Listar Modelos Disponíveis
```bash
make models
```

## 📚 Documentação da API

Após iniciar a aplicação, acesse:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🏗️ Estrutura do Projeto

```
├── backend/
│   ├── api/
│   │   └── main.py           # FastAPI principal
│   ├── database/
│   │   ├── postgres_client.py # PostgreSQL
│   │   └── mongodb_client.py  # MongoDB
│   ├── services/
│   │   ├── ai/
│   │   │   ├── local_llm.py         # Ollama client
│   │   │   └── agent_orchestrator.py # Agentes
│   │   └── rpa/
│   │       └── automation.py        # Selenium/Playwright
│   └── utils/
├── frontend/                  # (Opcional)
├── tests/                     # Testes
├── scripts/                   # Scripts auxiliares
├── docs/                      # Documentação
├── docker-compose.yml         # Containers
├── Dockerfile                 # Imagem da API
├── requirements.txt           # Dependências Python
├── Makefile                   # Comandos úteis
└── README.md                  # Este arquivo
```

## 📈 Performance Esperada

| Hardware | Velocidade do LLM | Recomendação |
|----------|------------------|--------------|
| 8GB RAM, CPU | Lento | Apenas testes |
| 16GB RAM, GPU básica | Médio | Uso básico |
| 32GB RAM, GPU dedicada | Rápido | Produção |

## 🐛 Solução de Problemas

### Ollama não funciona
```bash
# Verificar se o container está rodando
docker-compose ps ollama

# Ver logs
docker-compose logs ollama

# Reiniciar
docker-compose restart ollama
```

### Modelo não baixado
```bash
# Listar modelos
curl http://localhost:11434/api/tags

# Baixar modelo
curl -X POST http://localhost:11434/api/pull -d '{"name": "llama3.2"}'
```

### API não inicia
```bash
# Verificar logs
docker-compose logs api

# Verificar portas
lsof -i :8000
```

## 🤝 Contribuindo

Contribuições são bem-vindas.

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'feat: nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📝 Licença

MIT - Livre para uso comercial e pessoal

---
