# Dossiê de Pesquisa — Volume 3: Governança e Controle

## Conceitos-chave

- **Spec-Driven Development (SDD)**: metodologia que inverte o fluxo tradicional — a especificação (o quê e por quê) é a Fonte da Verdade e o código é artefato gerado/verificado a partir dela. "Intent is the source of truth."
- **Spec como contrato vivo**: documento executável que evolui com o projeto; contrato entre humanos e agentes que torna decisões técnicas explícitas, revisáveis e evoluíveis.
- **Hooks**: triggers que validam código ou executam testes automaticamente — loops de feedback autônomos que corrigem erros antes do commit (ex.: método Ralph Wiggum).
- **Scripts de contexto**: automações de suporte que "ensinam" o contexto do legado do projeto para a IA (linters, testes, convenções persistidas).
- **CLAUDE.md / AGENTS.md**: arquivos de configuração estratégica que servem como Fonte da Verdade e memória persistente do time de agentes — conhecimento do projeto sobrevive entre sessões.
- **Critérios de aceite**: escritos como resultados observáveis ("WHEN o usuário submete senha válida, é redirecionado para /login") que viram testes de ponta a ponta.
- **Spec drift**: divergência entre o especificado e o implementado; a primeira causa de falha do SDD.
- **EARS**: linguagem de requisitos ("The system shall POST to X within 500ms WHEN Y") que reduz ambiguidade para o parser da IA.
- **Steering documents**: product.md, structure.md, tech.md — equivalente de AGENTS.md dividido por propósito (meta do produto, estrutura do código, decisões de stack).

## Artigos Científicos e Papers

- TAGHAVI, Pardis; BHAVANI, Santosh. *Spec Kit Agents: Context-Grounded Agentic Workflows*. In: arXiv (Cornell University). 2026. Disponível em: http://arxiv.org/abs/2604.05278. Acesso em: 10 ago. 2026. (A)
- ALFÉREZ, Mauricio et al. *Model-Driven Requirements Specification for Software Product Lines*. In: Model-Driven Domain Analysis and Software Development. Disponível em: https://doi.org/10.4018/978-1-61692-874-2.ch017. Acesso em: 10 ago. 2026. (A)
- BERZINS, V.; LUQI. *An introduction to the specification language SPEC*. In: IEEE Software. 1990. Disponível em: https://doi.org/10.1109/52.50776. Acesso em: 10 ago. 2026. (A)
- TREUDE, Christoph; POSKITT, Christopher M. *Bot-Driven Development: From Simple Automation to Autonomous Software Development Bots*. In: 2025 IEEE/ACM International Workshop on Bots in Software Engineering (BotSE). 2025. Disponível em: https://doi.org/10.1109/botse67031.2025.00012. Acesso em: 10 ago. 2026. (A)
- PENG, Sheng-Wei; LIN, Yi-Hsun; LEE, Yi-Pei. *Inference Economics of Enterprise Coding Agents: A Case Study of Cloud vs. On-Premise LLMs*. In: arXiv (Cornell University). 2026. Disponível em: https://arxiv.org/abs/2607.13080. Acesso em: 10 ago. 2026. (A)

## Estado da arte / ferramentas de referência

- **GitHub Spec Kit**: loop formal de quatro fases (specify, plan, tasks, implement); documento da abordagem spec-as-source. Disponível em: https://github.com/github/spec-kit
- **Amazon Kiro**: fluxo stage-gated sequencial que produz requirements.md, design.md e tasks.md antes de qualquer código. Disponível em: https://kiro.dev
- **AGENTS.md (open standard)**: formato suportado em mais de 20 ferramentas (Codex, Cursor, Jules, VS Code) para setup, estilo de código e fronteiras arquiteturais em um arquivo legível por máquina. Disponível em: https://agents.md
- **cc-sdd**: CLI comunitária que instala fluxos SDD como skills (EARS, critérios de aceite, design com Mermaid, TDD por tarefa). Disponível em: https://github.com/codegen-ai/cc-sdd
- **CLAUDE.md (Anthropic)**: carregado na raiz do repositório no início da sessão; fonte de contexto permanente do projeto. Disponível em: https://code.claude.com/docs/en/context
- **DeepLearning.AI — SDD com Coding Agents**: curso que formaliza constitution do projeto + feature specs para preservar contexto e reduzir dívida cognitiva. Disponível em: https://www.deeplearning.ai/courses/spec-driven-development-with-coding-agents

## Casos de uso corporativos

- **Spec-as-source em Tessl**: código marcado "GENERATED FROM SPEC - DO NOT EDIT"; edita-se a spec e regenera-se o código — elimina drift por construção.
- **Kiro autopilot hooks**: agentes observam eventos (arquivo salvo, teste falhou, PR aberto) e checam automaticamente contra a spec; divergência é sinalizada antes da revisão.
- **Fluxos SDD com Spec Kit + Claude Code**: requirements antes de feature, design revisado antes de aprovar, tasks numeradas executadas uma a uma — menos premissas erradas, menos reescritas.
- **Constitution de projeto**: teams preservam decisões entre sessões com AGENTS.md/CLAUDE.md, evitando context collapse em projetos multi-sessão.

## Limitações e controvérsias

- **Spec drift**: se a spec não é atualizada junto com o código, o drift corrói o benefício; critérios objetivos de revisão são essenciais.
- **Overhead**: para tarefas <15 min, o overhead de spec não compensa; break-even aproximado: se o agente precisar de mais de dois ciclos de correção, escreva a spec.
- **SDD vs. vibe coding**: SDD é explicitamente posicionado contra o prompt-and-pray; mas sem disciplina o SDD vira documentação morta.
- **Hallucinated interfaces**: sem spec, o agente inventa método de API/config/db que compila e falha em runtime — spec previne.
- **Context collapse**: tarefas multi-sessão/multi-arquivo perdem decisões anteriores; especificações registradas mitigam.
- **Ferramentas em beta**: Spec Kit/Kiro/Tessl/cc-sdd consolidam em 2026; sem padrão único estabelecido.

## Fontes brutas (para Nó 7 — Auditor de Rastreabilidade)

- TAGHAVI, Pardis; BHAVANI, Santosh. *Spec Kit Agents: Context-Grounded Agentic Workflows*. Disponível em: http://arxiv.org/abs/2604.05278. Acesso em: 10 ago. 2026. (A)
- ALFÉREZ, Mauricio et al. *Model-Driven Requirements Specification for Software Product Lines*. Disponível em: https://doi.org/10.4018/978-1-61692-874-2.ch017. Acesso em: 10 ago. 2026. (A)
- BERZINS, V.; LUQI. *An introduction to the specification language SPEC*. Disponível em: https://doi.org/10.1109/52.50776. Acesso em: 10 ago. 2026. (A)
- TREUDE, Christoph; POSKITT, Christopher M. *Bot-Driven Development: From Simple Automation to Autonomous Software Development Bots*. Disponível em: https://doi.org/10.1109/botse67031.2025.00012. Acesso em: 10 ago. 2026. (A)
- PENG, Sheng-Wei; LIN, Yi-Hsun; LEE, Yi-Pei. *Inference Economics of Enterprise Coding Agents: A Case Study of Cloud vs. On-Premise LLMs*. Disponível em: https://arxiv.org/abs/2607.13080. Acesso em: 10 ago. 2026. (A)
- GITHUB. *GitHub Spec Kit — spec-driven development*. Disponível em: https://github.com/github/spec-kit. Acesso em: 10 ago. 2026. (B)
- AMAZON. *Kiro — spec-driven development with stage gates*. Disponível em: https://kiro.dev. Acesso em: 10 ago. 2026. (B)
- AGENTS.MD. *Open standard para instruções de agentes*. Disponível em: https://agents.md. Acesso em: 10 ago. 2026. (B)
- ANTHROPIC. *Claude Code — Context (CLAUDE.md)*. Disponível em: https://code.claude.com/docs/en/context. Acesso em: 10 ago. 2026. (B)
- DEEPLEARNING.AI. *Spec-Driven Development with Coding Agents*. Disponível em: https://www.deeplearning.ai/courses/spec-driven-development-with-coding-agents. Acesso em: 10 ago. 2026. (C)
