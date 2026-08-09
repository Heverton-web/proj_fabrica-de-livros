# 2 Metodologia

## 2.1 Natureza do recorte e corpus documental

Este artigo é um recorte investigativo derivado de um dossiê técnico mais amplo, produzido para a obra-mãe *AI Driven Development: Do Zero ao Deploy*, e não um estudo experimental com coleta de dados original. A opção metodológica é a de revisão analítico-integrativa de literatura técnica, aplicada a quatro blocos temáticos do dossiê-mãe que correspondem aos Capítulos 7 a 10 daquela obra: configuração prática do harness (`settings.json`, hooks, permissions), construção de tools e servidores MCP com blindagem contra tool poisoning, economia severa de tokens (caveman, RTK-memory, lean-ctx, headroom) e integração de agentes em CI/CD com portão de aprovação humana. O corpus consolidado que sustenta esses quatro blocos reúne mais de oitenta fontes verificáveis, combinando documentação oficial de fornecedor (ANTHROPIC, 2026; MODEL, 2026), catálogos de ataque de organismos de padronização em segurança (OWASP, 2026; CLOUD, 2026), pré-publicações científicas indexadas em arXiv (ARXIV, 2026), relatos de prática de equipes técnicas de mercado (DEPLOYHQ, 2026; SPACELIFT, 2026; TEAMVOY, 2026) e análises técnicas independentes publicadas por profissionais individuais (WILLISON, 2026; KONISHI, 2026).

## 2.2 Critério de seleção e recuperação das fontes

A seleção das fontes que compõem cada seção deste artigo não foi feita por leitura integral do dossiê-mãe, mas por recuperação indexada: o dossiê foi previamente segmentado em blocos temáticos e indexado por relevância textual (TF-IDF), permitindo consultas pontuais por termos associados a cada um dos quatro pilares do recorte — por exemplo, "settings.json hooks permissions harness configuração", "servidores MCP schemas tool poisoning blindagem segurança", "economia de tokens caveman RTK-memory lean-ctx headroom contexto" e "CI/CD deploy agentes portão de aprovação humana pipeline". Esse procedimento de recuperação seletiva evita carregar o dossiê inteiro em qualquer etapa de síntese e concentra a leitura nos blocos de maior escore de relevância para cada seção IMRaD (Introdução, Metodologia, Resultados e Discussão, Conclusão), preservando a rastreabilidade entre cada afirmação do texto e a fonte original consultada (ANTHROPIC, 2026).

## 2.3 Procedimento de síntese analítica

A partir dos blocos recuperados, o procedimento de síntese seguiu três etapas. Primeiro, o agrupamento das fontes por camada funcional dentro de cada pilar — por exemplo, dentro do bloco de harness, distinguindo fontes que descrevem o arquivo de configuração propriamente dito (EXPLAINX, 2026) das que descrevem a arquitetura de segurança multicamadas que o envolve (GENERAL, 2026). Segundo, a triangulação entre fontes de natureza distinta — documentação primária de fornecedor, catálogo de ataque de organismo independente e relato de incidente ou prática de mercado — para reduzir o risco de viés de uma única fonte ao descrever um mesmo fenômeno, como ocorre na convergência entre OWASP (2026), Microsoft (2026) e Willison (2026) sobre o mesmo padrão de vulnerabilidade de tool poisoning em MCP. Terceiro, a redação de cada seção com citação autor-data densa (NBR 10520), de modo que toda afirmação analítica remeta a uma fonte identificável do corpus, sem introdução de dado, autor ou ano que não conste do dossiê-mãe já indexado.

## 2.4 Limites do método

Como recorte derivado, este artigo herda as limitações do dossiê-mãe: não há coleta primária de dados de campo, não há experimento controlado comparando configurações de harness ou arquiteturas de MCP, e a maior parte das fontes é datada de 2026, refletindo a velocidade de publicação de um campo técnico em rápida mudança — o que exige leitura do recorte como fotografia de um estado da arte específico, não como conclusão definitiva. Adicionalmente, a natureza autor-data das citações privilegia a atribuição institucional (por exemplo, ANTHROPIC, 2026; MICROSOFT, 2026) sobre a atribuição individual quando a fonte primária é documentação corporativa sem autoria nominal — limitação inerente ao próprio corpus disponível, não uma escolha editorial deste recorte.

## Referências Bibliográficas

ANTHROPIC, 2026. *Effective harnesses for long-running agents*. Disponível em: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents. Acesso em: 02 ago. 2026.

MODEL, 2026. *Specification and documentation for the Model Context Protocol*. Model Context Protocol. Disponível em: https://github.com/modelcontextprotocol/modelcontextprotocol. Acesso em: 02 ago. 2026.

OWASP, 2026. *MCP Tool Poisoning*. Disponível em: https://owasp.org/www-community/attacks/MCP_Tool_Poisoning. Acesso em: 02 ago. 2026.

CLOUD, 2026. *Agentic MCP Security Best Practices Guide*. Cloud Security Alliance. Disponível em: https://labs.cloudsecurityalliance.org/agentic/agentic-mcp-security-best-practices-v1/. Acesso em: 02 ago. 2026.

ARXIV, 2026. *GitInject: Real-World Prompt Injection Attacks in AI-Powered CI/CD Pipelines*. Disponível em: https://arxiv.org/pdf/2606.09935. Acesso em: 02 ago. 2026.

DEPLOYHQ, 2026. *AI Agents in CI/CD Pipelines: From GitHub Issue to Production Deploy*. Disponível em: https://www.deployhq.com/blog/ai-agents-cicd-pipelines-github-issue-to-production-deploy. Acesso em: 02 ago. 2026.

SPACELIFT, 2026. *Where Do AI Agents Fit in CI/CD Pipelines?*. Disponível em: https://spacelift.io/blog/agentic-cicd. Acesso em: 02 ago. 2026.

TEAMVOY, 2026. *AI Agents in CI/CD Pipelines: A Guide for Tech Leads*. Disponível em: https://teamvoy.com/blog/building-ai-agents-into-your-ci-cd-pipeline-a-playbook-for-tech-leads/. Acesso em: 02 ago. 2026.

WILLISON, Simon, 2026. *Model Context Protocol has prompt injection security problems*. Disponível em: https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/. Acesso em: 02 ago. 2026.

KONISHI, Hidekazu, 2026. *Claude Code Features and Settings Reference 2026*. Disponível em: https://hidekazu-konishi.com/entry/claude_code_features_settings_reference_2026.html. Acesso em: 02 ago. 2026.

EXPLAINX, 2026. *Claude Code settings.json: Every Option Explained*. Disponível em: https://www.explainx.ai/blog/claude-code-settings-json-complete-reference-2026. Acesso em: 02 ago. 2026.

GENERAL, 2026. *Anthropic Claude Code Security Best Practices: Permissions, Hooks, MCP, Sandboxing, and CI/CD*. General Analysis. Disponível em: https://generalanalysis.com/guides/anthropic-claude-code-security-best-practices. Acesso em: 02 ago. 2026.

MICROSOFT, 2026. *Protecting against indirect prompt injection attacks in MCP*. Disponível em: https://developer.microsoft.com/blog/protecting-against-indirect-injection-attacks-mcp/. Acesso em: 02 ago. 2026.

HUMANLAYER, 2026. *12-Factor Agents — Principles for Building Reliable LLM Applications*. Disponível em: https://www.humanlayer.dev/12-factor-agents. Acesso em: 02 ago. 2026.

FUJITSU, 2026. *Fujitsu automates entire software development lifecycle with new AI-Driven Software Development Platform*. Disponível em: https://global.fujitsu/en-global/pr/news/2026/02/17-01. Acesso em: 02 ago. 2026.

FUTURUM, 2026. *AI Reaches 97% of Software Development Organizations*. Futurum Group. Disponível em: https://futurumgroup.com/press-release/ai-reaches-97-of-software-development-organizations/. Acesso em: 02 ago. 2026.

FORRESTER, 2026. *Agentic Software Development Takes The Lead: From Code Assistants To Orchestrated SDLC Agents*. Disponível em: https://www.forrester.com/blogs/agentic-software-development-takes-the-lead-from-code-assistants-to-orchestrated-sdlc-agents/. Acesso em: 02 ago. 2026.

RESEARCHGATE, 2026. *AI-First Software Development Lifecycle: An Agent-Driven Framework for Autonomous Planning, Coding, Testing, and Deployment*. Disponível em: https://www.researchgate.net/publication/403670772_AI-First_Software_Development_Lifecycle_An_Agent-Driven_Framework_for_Autonomous_Planning_Coding_Testing_and_Deployment. Acesso em: 02 ago. 2026.

AGENTA, 2026. *Top techniques to Manage Context Lengths in LLMs*. Disponível em: https://agenta.ai/blog/top-6-techniques-to-manage-context-length-in-llms. Acesso em: 02 ago. 2026.

REDIS, 2026. *Context Window Overflow in 2026: Fix LLM Errors Fast*. Disponível em: https://redis.io/blog/context-window-overflow/. Acesso em: 02 ago. 2026.

TOTALUM, 2026. *Claude Code subagents: the 2026 production playbook*. Disponível em: https://www.totalum.app/blog/claude-code-subagents-totalum. Acesso em: 02 ago. 2026.

AUGMENT, 2026. *How to Set Up AI Code Review in Your CI/CD Pipeline*. Augment Code. Disponível em: https://www.augmentcode.com/guides/ai-code-review-ci-cd-pipeline. Acesso em: 02 ago. 2026.

APTIBLE, 2026. *Prompt Injection in MCP: Tool Poisoning and Blast Radius*. Disponível em: https://www.aptible.com/mcp-security/mcp-prompt-injection. Acesso em: 02 ago. 2026.

SENTRY, 2026. *Exploiting Tool and Function Calling in LLM Agents*. Disponível em: https://blog.sentry.security/exploiting-tool-and-function-calling-in-llm-agents/. Acesso em: 02 ago. 2026.

MINDSTUDIO, 2026. *What Is an Agent Harness? The Architecture Behind Claude Code, Codex, and Cursor*. Disponível em: https://www.mindstudio.ai/blog/what-is-agent-harness-architecture-explained. Acesso em: 02 ago. 2026.
