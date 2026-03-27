# Deploy Gratuito - AI RPA Assistant

## Opcoes 100% Gratuitas para Producao

### 1. Railway (Recomendado)
**Custo**: $0/mes (plano gratuito)
**Vantagens**:
- Deploy automatico do GitHub
- Banco PostgreSQL incluso
- MongoDB incluso
- SSL gratuito
- Dominio personalizado

**Como fazer**:
1. Acesse railway.app
2. Conecte seu GitHub
3. Selecione o repositorio
4. Clique em "Deploy"
5. Configure variaveis de ambiente

### 2. Render
**Custo**: $0/mes (plano gratuito)
**Vantagens**:
- Web services gratuitos
- Banco PostgreSQL gratis
- SSL automatico
- Deploy via GitHub

**Limitacoes**:
- Dorme apos 15min inativo
- Pode ser lento no primeiro acesso

### 3. Fly.io
**Custo**: $0/mes (plano gratuito)
**Vantagens**:
- 3 maquinas virtuais gratis
- 160GB bandwidth/mes
- Deploy via CLI
- Performance excelente

**Como fazer**:
```bash
curl -L https://fly.io/install.sh | sh
fly auth login
fly launch
fly deploy
```

### 4. Oracle Cloud (Sempre Gratis)
**Custo**: $0 para sempre
**Vantagens**:
- 2 VMs com 1GB RAM cada
- 200GB armazenamento
- Sempre gratis (sem expiracao)

### 5. Google Cloud Platform
**Custo**: $0 (tier gratuito)
**Vantagens**:
- $300 creditos iniciais
- Cloud Run (serverless)
- Cloud SQL (PostgreSQL)

## Melhor Opcao: Railway

### Passo a Passo

1. **Preparar o projeto**
   - Dockerfile ja esta pronto!

2. **Criar conta Railway**
   - Acesse railway.app
   - Faca login com GitHub

3. **Criar novo projeto**
   - Clique "New Project"
   - Select "Deploy from GitHub repo"
   - Escolha o repositorio

4. **Adicionar servicos**
   - Clique "New" → "Database" → "PostgreSQL"
   - Clique "New" → "Database" → "MongoDB"

5. **Configurar variaveis**
   - Va em "Variables"
   - Adicione as variaveis de ambiente

6. **Deploy automatico**
   - Railway detecta o Dockerfile
   - Faz build automaticamente
   - Disponibiliza URL publica

## Deploy Manual (VPS Gratis)

### Oracle Cloud Forever Free

1. **Criar conta**
   - Acesse cloud.oracle.com

2. **Criar instancia**
   - Shape: VM.Standard.E2.1.Micro
   - OS: Ubuntu 22.04

3. **Configurar**
```bash
sudo apt update
sudo apt install docker.io docker-compose-v2 -y
git clone https://github.com/Daniel-Gehlen/Assistente-de-Automa-o-com-IA.git
cd Assistente-de-Automacao-com-IA
sudo docker compose up -d
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2
```

## Recomendacao Final

**Para iniciantes**: Railway
**Para controle total**: Oracle Cloud
**Para performance**: Fly.io

O projeto ja esta pronto para deploy!
