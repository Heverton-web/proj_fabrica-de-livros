# Dossiê de Pesquisa — MiMoCode: Visão Geral

> Material coletado em agosto/2026 para a obra **"MiMoCode: o que é, para que serve,
> como configurar, como usar, quais as configurações que ninguém te ensina, como
> extrair ao máximo do Harness MiMoCode"** (tamanho G, 10 capítulos, ≥20 refs/cap).

## 1. URLs oficiais

| # | Fonte | URL |
|---|-------|-----|
| [1] | Repositório oficial GitHub | https://github.com/XiaomiMiMo/MiMo-Code |
| [2] | Documentação / central de notícias | https://mimo.mi.com/docs/en-US/news/latest/mimocode |
| [3] | Ecossistema / awesome list | https://github.com/XiaomiMiMo/awesome-mimo-agent |
| [4] | README oficial (NPM) | https://github.com/XiaomiMiMo/MiMo-Code/blob/main/README_npm.md |
| [5] | Instalação (script) | https://mimo.xiaomi.com/install |

## 2. O que é e história

- **MiMoCode** (comando `mimo`) é um assistente de programação **nativo de terminal**
  (TUI), lançado oficialmente na versão `v0.1.0` em **junho de 2026** pela **equipe
  MiMo da Xiaomi**.
- É um **fork direto do projeto open source OpenCode** (`anomalyco/opencode`), herdando
  a arquitetura TypeScript e o modelo de plugins, com pacotes migrados de `@opencode-ai/*`
  para `@mimo-ai/*`.
- Introduz sistemas próprios de engenharia de agentes: **memória persistente** baseada
  em **SQLite FTS5**, **gerenciamento inteligente de contexto**, **workflows
  determinísticos** e o modo **Compose**.
- **Licença MIT** (com restrições de uso para serviços hospedados e políticas de marca Xiaomi).

## 3. Instalação

- macOS/Linux: `curl -fsSL https://mimo.xiaomi.com/install | bash`
- Windows (PowerShell): `powershell -ep Bypass -c "irm https://mimo.xiaomi.com/install.ps1 | iex"`
- NPM (todas as plataformas): `npm install -g @mimo-ai/cli`
- Inicialização: `mimo`

## 4. Recursos principais

- **Agente TUI** com múltiplos modos principais alternáveis via `Tab`:
  - `build` (padrão): permissões completas de ferramentas.
  - `plan`: análise somente-leitura (exploração e design).
  - `compose`: orquestração specs-driven (desenvolvimento orientado a especificação).
- **Modo Plan**: planejamento estruturado antes da mutação de arquivos.
- **MCP / ACP**: Model Context Protocol e Agent Client Protocol.
- **Memória persistente** (SQLite FTS5) em três pilares:
  - Memória de projeto (`MEMORY.md`)
  - Checkpoints de sessão (`checkpoint.md`)
  - Notas de progresso de tarefas (`tasks/<id>/progress.md`)
- **Skills**: 20+ skills nativas (docs Office/PDF, arXiv, design, frontend design),
  acionadas via `/` ou por relevância BM25.
- **Workflows determinísticos**: scripts JS em sandbox (ex.: `compose`, `deep-research`,
  `fact-check`, `research-experiment`).
- **Avançados**: `/goal` (juiz independente anti-parada prematura), `/dream`
  (consolidação de memória a cada 7 dias), `/distill` (converte fluxos manuais em
  skills), `/voice` (entrada de voz em tempo real, TenVAD + MiMo ASR).

## 5. Fatos com fontes

- Benchmarks publicados (mesmo modelo base MiMo): 62% SWE-Bench Pro vs 57% Claude Code;
  73% Terminal Bench 2 vs 68% [2].
- Repositório ultrapassou milhares de estrelas nos primeiros dias pós-lançamento (jun/2026) [1].
- Integrações da comunidade (ex.: adaptadores no ecossistema `rtk-ai/rtk`) [3].
