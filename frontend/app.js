/**
 * AI RPA Assistant - Frontend JavaScript
 * Gerencia comunicação com a API e atualização de status
 */

// Configuração da API
const API_BASE_URL = window.location.origin;

// Verificar se está em produção (Vercel)
const isProduction = window.location.hostname.includes('vercel.app') ||
                     window.location.hostname.includes('now.sh') ||
                     !window.location.hostname.includes('localhost');

// Elementos DOM
const sqliteStatus = document.getElementById('sqlite-status');
const agentsStatus = document.getElementById('agents-status');
const loadingElement = document.getElementById('loading');
const responseElement = document.getElementById('response');
const responseContent = document.getElementById('response-content');

// Função para mostrar loading
function showLoading() {
    loadingElement.classList.add('show');
    responseElement.style.display = 'none';
}

// Função para esconder loading
function hideLoading() {
    loadingElement.classList.remove('show');
}

// Função para mostrar resposta
function showResponse(data) {
    responseContent.textContent = JSON.stringify(data, null, 2);
    responseElement.style.display = 'block';
    responseElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Função para mostrar erro
function showError(error, isProductionError = false) {
    let errorMessage = `Erro: ${error}`;

    if (isProductionError) {
        errorMessage = `
⚠️ API Não Disponível

Este frontend está hospedado no Vercel como demonstração estática.

Para usar a API completa com:
• Agentes de IA
• Web Scraping
• Gerenciamento de Tarefas
• SQLite Database

Execute o backend localmente:
1. Clone o repositório
2. Execute: python app.py
3. Acesse: http://localhost:8000

Ou acesse o GitHub para mais informações:
https://github.com/Daniel-Gehlen/Assistente-de-Automa-o-com-IA
        `.trim();
    }

    responseContent.textContent = errorMessage;
    responseElement.style.display = 'block';
    responseElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Função para fazer requisição à API
async function apiRequest(endpoint, method = 'GET', body = null) {
    // Se estiver em produção (Vercel), mostrar mensagem de API não disponível
    if (isProduction) {
        return {
            success: false,
            error: 'API não disponível nesta versão. Este é apenas o frontend hospedado no Vercel. Para usar a API completa, execute o backend localmente.',
            isProduction: true
        };
    }

    try {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
            },
        };

        if (body) {
            options.body = JSON.stringify(body);
        }

        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        const data = await response.json();

        return { success: true, data, status: response.status };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

// Função para testar endpoint
async function testEndpoint(endpoint) {
    showLoading();

    const result = await apiRequest(endpoint);

    hideLoading();

    if (result.success) {
        showResponse(result.data);
    } else {
        showError(result.error, result.isProduction);
    }
}

// Função para testar agente
async function testAgent() {
    const task = document.getElementById('agentTask').value;
    const agentName = document.getElementById('agentName').value;

    if (!task.trim()) {
        alert('Por favor, insira uma tarefa para o agente.');
        return;
    }

    showLoading();

    const result = await apiRequest('/api/agents/process', 'POST', {
        task,
        agent_name: agentName
    });

    hideLoading();

    if (result.success) {
        showResponse(result.data);
    } else {
        showError(result.error, result.isProduction);
    }
}

// Função para atualizar status dos serviços
async function updateServiceStatus() {
    // Se estiver em produção, mostrar status de demonstração
    if (isProduction) {
        if (sqliteStatus) {
            sqliteStatus.textContent = 'Demo';
            sqliteStatus.parentElement.querySelector('.status-indicator').classList.remove('status-healthy', 'status-unhealthy');
            sqliteStatus.parentElement.querySelector('.status-indicator').classList.add('status-healthy');
        }

        if (agentsStatus) {
            agentsStatus.textContent = 'Demo';
            agentsStatus.parentElement.querySelector('.status-indicator').classList.remove('status-healthy', 'status-unhealthy');
            agentsStatus.parentElement.querySelector('.status-indicator').classList.add('status-healthy');
        }
        return;
    }

    try {
        // Health check
        const healthResult = await apiRequest('/health');

        if (healthResult.success) {
            const health = healthResult.data;

            // Atualizar status do SQLite
            if (sqliteStatus) {
                const sqliteHealthy = health.services?.sqlite === 'healthy';
                sqliteStatus.textContent = sqliteHealthy ? 'Operacional' : 'Indisponível';
                sqliteStatus.parentElement.querySelector('.status-indicator').classList.remove('status-healthy', 'status-unhealthy');
                sqliteStatus.parentElement.querySelector('.status-indicator').classList.add(sqliteHealthy ? 'status-healthy' : 'status-unhealthy');
            }

            // Atualizar status dos agentes
            if (agentsStatus) {
                const agentsHealth = health.services?.agents;
                const healthyAgents = agentsHealth ? Object.values(agentsHealth).filter(status => status === 'healthy').length : 0;
                const totalAgents = agentsHealth ? Object.keys(agentsHealth).length : 0;

                agentsStatus.textContent = totalAgents > 0 ? `${healthyAgents}/${totalAgents} Ativos` : 'Indisponível';
                agentsStatus.parentElement.querySelector('.status-indicator').classList.remove('status-healthy', 'status-unhealthy');
                agentsStatus.parentElement.querySelector('.status-indicator').classList.add(healthyAgents > 0 ? 'status-healthy' : 'status-unhealthy');
            }
        } else {
            // Serviço indisponível
            if (sqliteStatus) {
                sqliteStatus.textContent = 'Indisponível';
                sqliteStatus.parentElement.querySelector('.status-indicator').classList.remove('status-healthy');
                sqliteStatus.parentElement.querySelector('.status-indicator').classList.add('status-unhealthy');
            }

            if (agentsStatus) {
                agentsStatus.textContent = 'Indisponível';
                agentsStatus.parentElement.querySelector('.status-indicator').classList.remove('status-healthy');
                agentsStatus.parentElement.querySelector('.status-indicator').classList.add('status-unhealthy');
            }
        }
    } catch (error) {
        console.error('Erro ao atualizar status:', error);

        // Em caso de erro, mostrar como indisponível
        if (sqliteStatus) {
            sqliteStatus.textContent = 'Erro';
            sqliteStatus.parentElement.querySelector('.status-indicator').classList.remove('status-healthy');
            sqliteStatus.parentElement.querySelector('.status-indicator').classList.add('status-unhealthy');
        }

        if (agentsStatus) {
            agentsStatus.textContent = 'Erro';
            agentsStatus.parentElement.querySelector('.status-indicator').classList.remove('status-healthy');
            agentsStatus.parentElement.querySelector('.status-indicator').classList.add('status-unhealthy');
        }
    }
}

// Função para criar nova tarefa
async function createTask() {
    if (isProduction) {
        showError('Criação de tarefas não disponível no modo demo.', true);
        return;
    }

    const name = prompt('Nome da tarefa:');
    if (!name) return;

    const description = prompt('Descrição da tarefa (opcional):');

    showLoading();

    const result = await apiRequest('/api/tasks', 'POST', {
        name,
        description: description || null,
        status: 'pending'
    });

    hideLoading();

    if (result.success) {
        alert(`Tarefa criada com sucesso! ID: ${result.data.task_id}`);
        showResponse(result.data);
    } else {
        showError(result.error);
    }
}

// Função para salvar dados de scraping
async function saveScrapingData() {
    if (isProduction) {
        showError('Web scraping não disponível no modo demo.', true);
        return;
    }

    const url = prompt('URL do site:');
    if (!url) return;

    const title = prompt('Título da página:');
    if (!title) return;

    showLoading();

    const result = await apiRequest('/api/scraping', 'POST', {
        url,
        data: { title },
        metadata: { timestamp: new Date().toISOString() }
    });

    hideLoading();

    if (result.success) {
        alert('Dados de scraping salvos com sucesso!');
        showResponse(result.data);
    } else {
        showError(result.error);
    }
}

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    // Atualizar status dos serviços ao carregar a página
    updateServiceStatus();

    // Atualizar status a cada 30 segundos
    setInterval(updateServiceStatus, 30000);

    console.log('🤖 AI RPA Assistant - Frontend inicializado');
    console.log('📍 API Base URL:', API_BASE_URL);
    console.log('🌐 Modo:', isProduction ? 'Produção (Vercel)' : 'Desenvolvimento');

    // Se estiver em produção, mostrar aviso
    if (isProduction) {
        console.log('⚠️ Modo demonstração - API não disponível');

        // Adicionar aviso visual na página
        const heroSection = document.querySelector('.hero-section');
        if (heroSection) {
            const demoNotice = document.createElement('div');
            demoNotice.className = 'alert alert-info mt-3';
            demoNotice.innerHTML = `
                <i class="bi bi-info-circle-fill"></i>
                <strong>Modo Demonstração</strong> - Este frontend está hospedado no Vercel.
                Para usar a API completa, execute o backend localmente.
                <a href="https://github.com/Daniel-Gehlen/Assistente-de-Automa-o-com-IA" target="_blank" class="alert-link">
                    Ver instruções no GitHub
                </a>
            `;
            heroSection.appendChild(demoNotice);
        }
    }
});

// Adicionar atalhos de teclado
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter para testar agente
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const activeElement = document.activeElement;
        if (activeElement && activeElement.id === 'agentTask') {
            testAgent();
        }
    }
});

// Função para copiar resposta
function copyResponse() {
    const responseText = responseContent.textContent;
    navigator.clipboard.writeText(responseText).then(() => {
        alert('Resposta copiada para a área de transferência!');
    }).catch(err => {
        console.error('Erro ao copiar:', err);
    });
}

// Adicionar botão de copiar se não existir
if (responseElement && !document.getElementById('copyButton')) {
    const copyButton = document.createElement('button');
    copyButton.id = 'copyButton';
    copyButton.className = 'btn btn-sm btn-outline-secondary mt-2';
    copyButton.innerHTML = '<i class="bi bi-clipboard"></i> Copiar';
    copyButton.onclick = copyResponse;
    responseElement.appendChild(copyButton);
}
