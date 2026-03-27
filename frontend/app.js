/**
 * AI RPA Assistant - Frontend JavaScript
 * Versão 100% Gratuita
 */

const API_BASE_URL = window.location.origin;

// Elementos DOM
const checkHealthBtn = document.getElementById('checkHealth');
const healthStatusDiv = document.getElementById('healthStatus');
const listModelsBtn = document.getElementById('listModels');
const modelsListDiv = document.getElementById('modelsList');
const taskForm = document.getElementById('taskForm');
const taskResultDiv = document.getElementById('taskResult');
const loadTasksBtn = document.getElementById('loadTasks');
const tasksListDiv = document.getElementById('tasksList');
const scrapingForm = document.getElementById('scrapingForm');
const scrapingResultDiv = document.getElementById('scrapingResult');

// Funções utilitárias
function showLoading(element) {
    element.classList.add('loading');
}

function hideLoading(element) {
    element.classList.remove('loading');
}

function formatJSON(obj) {
    return JSON.stringify(obj, null, 2);
}

function createStatusBadge(status) {
    const badge = document.createElement('span');
    badge.className = `status ${status}`;
    badge.textContent = status === 'pending' ? 'Pendente' : status === 'completed' ? 'Concluído' : 'Falhou';
    return badge;
}

// Verificar saúde do sistema
checkHealthBtn.addEventListener('click', async () => {
    showLoading(healthStatusDiv);

    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();

        let html = '<h3>Status do Sistema</h3>';
        html += `<p><strong>API:</strong> ${data.api}</p>`;
        html += '<p><strong>Serviços:</strong></p><ul>';

        for (const [service, status] of Object.entries(data.services)) {
            const icon = status === 'healthy' ? '✅' : '❌';
            html += `<li>${icon} ${service}: ${status}</li>`;
        }

        html += '</ul>';
        html += `<p><strong>Custo:</strong> ${data.cost}</p>`;

        healthStatusDiv.innerHTML = html;
    } catch (error) {
        healthStatusDiv.innerHTML = `<p style="color: red;">Erro ao verificar saúde: ${error.message}</p>`;
    } finally {
        hideLoading(healthStatusDiv);
    }
});

// Listar modelos disponíveis
listModelsBtn.addEventListener('click', async () => {
    showLoading(modelsListDiv);

    try {
        const response = await fetch(`${API_BASE_URL}/models`);
        const data = await response.json();

        if (data.error) {
            modelsListDiv.innerHTML = `<p style="color: red;">${data.error}</p>`;
            return;
        }

        let html = '<h3>Modelos Disponíveis</h3>';
        html += `<p>Total: ${data.total} modelos</p>`;
        html += '<ul>';

        data.models.forEach(model => {
            html += `<li><strong>${model.name}</strong> - Tamanho: ${(model.size / 1e9).toFixed(2)} GB</li>`;
        });

        html += '</ul>';
        html += `<p><em>${data.message}</em></p>`;

        modelsListDiv.innerHTML = html;
    } catch (error) {
        modelsListDiv.innerHTML = `<p style="color: red;">Erro ao listar modelos: ${error.message}</p>`;
    } finally {
        hideLoading(modelsListDiv);
    }
});

// Processar tarefa
taskForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const agentName = document.getElementById('agentName').value;
    const task = document.getElementById('taskInput').value;

    showLoading(taskResultDiv);

    try {
        const response = await fetch(`${API_BASE_URL}/api/agents/process`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                task: task,
                agent_name: agentName
            })
        });

        const data = await response.json();

        let html = '<h3>Resultado da Tarefa</h3>';
        html += `<p><strong>Agente:</strong> ${data.agent || agentName}</p>`;
        html += `<p><strong>Modelo:</strong> ${data.model || 'llama3.2 (local)'}</p>`;
        html += `<p><strong>Sucesso:</strong> ${data.success ? 'Sim' : 'Não'}</p>`;

        if (data.success) {
            html += '<p><strong>Resposta:</strong></p>';
            html += `<pre style="background: #f5f5f5; padding: 15px; border-radius: 8px; overflow-x: auto;">${data.output}</pre>`;
        } else {
            html += `<p style="color: red;"><strong>Erro:</strong> ${data.error}</p>`;
        }

        taskResultDiv.innerHTML = html;
    } catch (error) {
        taskResultDiv.innerHTML = `<p style="color: red;">Erro ao processar tarefa: ${error.message}</p>`;
    } finally {
        hideLoading(taskResultDiv);
    }
});

// Carregar tarefas salvas
loadTasksBtn.addEventListener('click', async () => {
    showLoading(tasksListDiv);

    try {
        const response = await fetch(`${API_BASE_URL}/api/tasks`);
        const data = await response.json();

        if (data.tasks.length === 0) {
            tasksListDiv.innerHTML = '<p>Nenhuma tarefa encontrada.</p>';
            return;
        }

        let html = '<h3>Tarefas Salvas</h3>';
        html += `<p>Total: ${data.total} tarefas</p>`;

        data.tasks.forEach(task => {
            const taskItem = document.createElement('div');
            taskItem.className = 'task-item';

            const createdAt = new Date(task.created_at).toLocaleString('pt-BR');

            taskItem.innerHTML = `
                <h4>${task.name}</h4>
                <p>${task.description || 'Sem descrição'}</p>
                <p><small>Criado em: ${createdAt}</small></p>
            `;

            taskItem.appendChild(createStatusBadge(task.status));
            tasksListDiv.appendChild(taskItem);
        });

        tasksListDiv.innerHTML = html;
    } catch (error) {
        tasksListDiv.innerHTML = `<p style="color: red;">Erro ao carregar tarefas: ${error.message}</p>`;
    } finally {
        hideLoading(tasksListDiv);
    }
});

// Salvar dados de scraping
scrapingForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const url = document.getElementById('scrapingUrl').value;
    const dataText = document.getElementById('scrapingData').value;

    showLoading(scrapingResultDiv);

    try {
        // Tentar parsear como JSON
        let data;
        try {
            data = JSON.parse(dataText);
        } catch {
            // Se não for JSON válido, salvar como texto
            data = { content: dataText };
        }

        const response = await fetch(`${API_BASE_URL}/api/scraping`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                url: url,
                data: data
            })
        });

        const result = await response.json();

        if (result.doc_id) {
            scrapingResultDiv.innerHTML = `
                <h3>Dados Salvos com Sucesso!</h3>
                <p><strong>ID do Documento:</strong> ${result.doc_id}</p>
                <p><strong>Status:</strong> ${result.status}</p>
            `;
        } else {
            scrapingResultDiv.innerHTML = `<p style="color: red;">Erro ao salvar dados: ${result.error || 'Erro desconhecido'}</p>`;
        }
    } catch (error) {
        scrapingResultDiv.innerHTML = `<p style="color: red;">Erro ao salvar dados: ${error.message}</p>`;
    } finally {
        hideLoading(scrapingResultDiv);
    }
});

// Botões dos agentes
document.querySelectorAll('.btn-agent').forEach(btn => {
    btn.addEventListener('click', () => {
        const agentName = btn.dataset.agent;
        document.getElementById('agentName').value = agentName;

        // Rolar até o formulário
        document.getElementById('taskForm').scrollIntoView({ behavior: 'smooth' });

        // Focar no campo de tarefa
        document.getElementById('taskInput').focus();
    });
});

// Carregar tarefas ao iniciar
document.addEventListener('DOMContentLoaded', () => {
    // Verificar saúde automaticamente
    setTimeout(() => {
        checkHealthBtn.click();
    }, 1000);
});
