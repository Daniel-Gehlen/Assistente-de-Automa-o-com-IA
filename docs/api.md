# Documentação da API - AI RPA Assistant

## Visão Geral

A API do AI RPA Assistant fornece endpoints para interagir com agentes de IA locais, gerenciar tarefas e automatizar processos.

## Base URL

```
http://localhost:8000
```

## Endpoints

### 1. Raiz
**GET** `/`
Retorna informações básicas sobre a API.

### 2. Health Check
**GET** `/health`
Verifica a saúde de todos os serviços.

### 3. Listar Modelos
**GET** `/models`
Lista modelos de IA disponíveis no Ollama.

### 4. Processar Tarefa com Agente
**POST** `/api/agents/process`
Envia uma tarefa para um agente de IA processar.

### 5. Criar Tarefa
**POST** `/api/tasks`
Cria uma nova tarefa no banco de dados.

### 6. Listar Tarefas
**GET** `/api/tasks?limit=100`
Lista todas as tarefas salvas.

### 7. Obter Tarefa
**GET** `/api/tasks/{task_id}`
Obtém uma tarefa específica por ID.

### 8. Atualizar Tarefa
**PUT** `/api/tasks/{task_id}`
Atualiza o status e resultado de uma tarefa.

### 9. Salvar Dados de Scraping
**POST** `/api/scraping`
Salva dados coletados de scraping no MongoDB.

### 10. Listar Dados de Scraping
**GET** `/api/scraping?limit=100`
Lista dados de scraping salvos.

### 11. Obter Dados de Scraping
**GET** `/api/scraping/{url}`
Obtém dados de scraping por URL.

## Códigos de Resposta
- `200` - Sucesso
- `400` - Requisição inválida
- `404` - Recurso não encontrado
- `500` - Erro interno do servidor

## Documentação Interativa
Após iniciar a aplicação, acesse:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
