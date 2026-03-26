---
name: modus-operandi
description: Modus Operandi padrão para implementação de melhorias e novas funcionalidades seguindo fluxos atômicos e documentação via Git/GitHub.
category: workflow
---

# Modus Operandi Skill

## 📋 Descrição

Este é o protocolo padrão para implementação de melhorias e novas funcionalidades. Ele exige que as mudanças sejam feitas de forma modular, com o mínimo de novas nomenclaturas, e totalmente documentadas via Issues, Branches e Pull Requests no GitHub.

## 🚀 Como usar

Sempre que uma nova funcionalidade ou melhoria for solicitada, este fluxo deve ser ativado automaticamente.

## 📝 Diretrizes Gerais

1. **Atômico e Modular**: Implementar melhorias de forma modularizada e atômica.
2. **Nomenclatura**: Utilizar o mínimo de novas nomenclaturas, reaproveitando as existentes. Criar novas apenas se estritamente necessário.
3. **Ambiente Local e Remoto**: Implementar localmente e no repositório GitHub para garantir documentação total.
4. **Git Ignore**: Manter configurações e arquivos locais (como logs e artefatos de agentes) fora do repositório remoto via `.gitignore`.

## 🔄 Fluxo de Implementação (Ordem Lógica)

### 1. Preparação

- Se não tiver já criado, criar estrutura de testes automatizados.
- Implementar testes para o código existente.
- **Ferramentas de Teste Recomendadas**:
  - **Acessibilidade/Links**: `linkinator`, `@axe-core/playwright`, `cspell`.
  - **Formatação**: `Prettier`, `ESLint`.
  - **Funcionais**: `Playwright`, `Robot Framework`, `Jest`.

### 2. Se, e somente se, cabível para o projeto presente sem danificá-lo e levando em consideração que é um projeto para github pages ou vercel, melhorias na Camada de Dados

- Otimizar queries e persistência.
- Implementar sistemas de cache.

### 4. Melhorias de Código

- Refatorar código duplicado.
- Melhorar validações de entrada e segurança.

### 5. Se não existirem, melhorias de Infraestrutura

- Implementar logs estruturados e monitoramento.
- Criar tratamento de erros global.

### 6. Novas Funcionalidades

- Desenvolvimento da lógica de negócio e interface aprimorados com os meljores práticas de engenharia de software atuais.

## 🛠️ Protocolo Git (Rigoroso)

Para cada implementação:

1. **Criar Issue**: Título descritivo e objetivos claros.
2. **Criar Branch**: `git checkout -b feature/nome-da-melhoria`.
3. **Desenvolver e Commitar**:
   - `git commit -m "tipo: descrição clara"`
   - Tipos: `feat`, `fix`, `perf`, `refactor`, `test`.
4. **Enviar e Fundir**:
   - `git push origin branch`
   - Criar Pull Request e fazer Merge após aprovação.

## 🔄 Integração Automatizada

- O agente deve sempre sugerir a criação de Issues e Branches antes de começar a escrever o código principal. Ao final de cada implementação deve voltar a main e testar localmente na main no navegador.

