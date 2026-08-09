# 1 Introdução

## 1.1 Contextualização do problema

A adoção de harnesses agênticos de codificação — ferramentas que colocam um modelo de linguagem no centro de um ciclo de leitura, edição e execução de comandos sobre um repositório real — deixou de ser experimento de laboratório para se tornar prática corrente de engenharia de software. Levantamentos de mercado de 2026 registram que 76,6% das organizações já usam IA ativamente em desenvolvimento, com 20,4% adicionais avaliando adoção (FUTURUM, 2026), e a Forrester descreve a migração de assistentes de código pontuais para agentes orquestrados de ciclo de vida completo (SDLC) como a tendência dominante do ano (FORRESTER, 2026). Esse deslocamento levanta um problema de pesquisa concreto: um harness como o Claude Code decide o que é permitido — cada ferramenta possui seu próprio portão de permissão, verificado contra um pipeline de regras antes de qualquer execução —, enquanto o modelo decide apenas o que tentar (ANTHROPIC, 2026). A distância entre "o que o agente tenta" e "o que o agente pode" é preenchida por configuração explícita: o arquivo `settings.json`, os hooks determinísticos, os servidores MCP (Model Context Protocol) e as próprias práticas de economia de contexto que decidem quanto e o quê o modelo enxerga a cada chamada.

Essa distância é também o ponto de maior risco documentado na literatura técnica recente. O OWASP catalogou o *MCP Tool Poisoning* como um vetor de injeção indireta de prompt em que instruções maliciosas embutidas na descrição de uma ferramenta MCP sequestram o raciocínio do agente no momento do registro da ferramenta, antes mesmo de qualquer chamada real (OWASP, 2026). A Microsoft documenta o mesmo padrão de ataque como problema estrutural do protocolo, não falha isolada de implementação (MICROSOFT, 2026). Willison (2026) demonstrou publicamente que a arquitetura do MCP, ao combinar acesso a dados privados, exposição a conteúdo não confiável e capacidade de comunicação externa, reproduz a "trifecta letal" de vulnerabilidades já conhecida em agentes de IA. No extremo oposto do pipeline, o paper "GitInject" documenta ataques reais de injeção de prompt em pipelines de CI/CD alimentados por IA, explorando títulos de *pull request*, *issues* e comentários de repositório como superfície de ataque (ARXIV, 2026).

## 1.2 Objetivo do recorte

Este artigo tem por objetivo sintetizar, de forma integrada, quatro frentes de governança técnica de agentes de codificação que a literatura recente trata de modo predominantemente fragmentado: (i) a configuração prática do harness via `settings.json`, hooks e permissions; (ii) a construção de tools e servidores MCP com schemas validados e blindagem contra tool poisoning; (iii) a disciplina de economia severa de tokens como pré-condição de sustentabilidade operacional de agentes de longa duração; e (iv) a integração desses agentes em pipelines de CI/CD sob um portão de aprovação humana antes do deploy em produção. O recorte não propõe uma técnica nova, mas articula essas quatro frentes como uma única pilha de controle, na qual cada camada cobre a lacuna de exposição deixada pelas demais.

## 1.3 Justificativa e relevância

A justificativa para tratar essas quatro frentes como um objeto de estudo único decorre de uma constatação recorrente na literatura: nenhuma camada isolada é suficiente. A abordagem de segurança do Claude Code é descrita como multicamadas — permissions como aplicação diária, *managed settings* como política corporativa, hooks como aplicação determinística e controles de MCP como governança de ferramentas —, com a analogia recorrente de tratar o agente "como um funcionário júnior novo com acesso root": dar apenas o acesso necessário, observar constantemente e checar duas vezes quando a ação for arriscada (GENERAL, 2026). A mesma lógica de anteparas redundantes aparece no fechamento do ciclo: práticas de segurança recomendadas para deploy incluem credenciais de curta duração, privilégio mínimo, limite de gasto de tokens e a manutenção de um portão de aprovação humana entre a mudança de código do agente e o deploy em produção — o agente abre o *pull request*, o CI valida, um humano aprova o merge e o pipeline de deploy dispara automaticamente, nunca o contrário (TEAMVOY, 2026). Relatos de equipes técnicas de mercado confirmam esse padrão em produção: DeployHQ, Spacelift e Augment Code documentam pipelines reais com agentes revisando PRs e reparando testes, sempre com aprovação humana antes de produção (DEPLOYHQ, 2026; SPACELIFT, 2026; AUGMENT, 2026). Finalmente, a camada de economia de tokens é justificada por um argumento de custo estrutural: em fluxos de agente estendidos, o processamento de contexto domina o custo total, de modo que a curadoria do que entra na janela de contexto — e não apenas a escolha de palavras do prompt — determina diretamente a viabilidade econômica de operar agentes de codificação em escala (AGENTA, 2026; REDIS, 2026). Compreender essas quatro frentes como uma pilha única, e não como tópicos avulsos, é o que este artigo se propõe a demonstrar.

## Referências Bibliográficas

ANTHROPIC, 2026. *Effective harnesses for long-running agents*. Disponível em: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents. Acesso em: 02 ago. 2026.

EXPLAINX, 2026. *Claude Code settings.json: Every Option Explained*. Disponível em: https://www.explainx.ai/blog/claude-code-settings-json-complete-reference-2026. Acesso em: 02 ago. 2026.

OWASP, 2026. *MCP Tool Poisoning*. Disponível em: https://owasp.org/www-community/attacks/MCP_Tool_Poisoning. Acesso em: 02 ago. 2026.

CLOUD, 2026. *Agentic MCP Security Best Practices Guide*. Cloud Security Alliance. Disponível em: https://labs.cloudsecurityalliance.org/agentic/agentic-mcp-security-best-practices-v1/. Acesso em: 02 ago. 2026.

MICROSOFT, 2026. *Protecting against indirect prompt injection attacks in MCP*. Disponível em: https://developer.microsoft.com/blog/protecting-against-indirect-injection-attacks-mcp/. Acesso em: 02 ago. 2026.

GENERAL, 2026. *Anthropic Claude Code Security Best Practices: Permissions, Hooks, MCP, Sandboxing, and CI/CD*. General Analysis. Disponível em: https://generalanalysis.com/guides/anthropic-claude-code-security-best-practices. Acesso em: 02 ago. 2026.

ARXIV, 2026. *GitInject: Real-World Prompt Injection Attacks in AI-Powered CI/CD Pipelines*. Disponível em: https://arxiv.org/pdf/2606.09935. Acesso em: 02 ago. 2026.

HUMANLAYER, 2026. *12-Factor Agents — Principles for Building Reliable LLM Applications*. Disponível em: https://www.humanlayer.dev/12-factor-agents. Acesso em: 02 ago. 2026.

FUJITSU, 2026. *Fujitsu automates entire software development lifecycle with new AI-Driven Software Development Platform*. Disponível em: https://global.fujitsu/en-global/pr/news/2026/02/17-01. Acesso em: 02 ago. 2026.

FUTURUM, 2026. *AI Reaches 97% of Software Development Organizations*. Futurum Group. Disponível em: https://futurumgroup.com/press-release/ai-reaches-97-of-software-development-organizations/. Acesso em: 02 ago. 2026.

FORRESTER, 2026. *Agentic Software Development Takes The Lead: From Code Assistants To Orchestrated SDLC Agents*. Disponível em: https://www.forrester.com/blogs/agentic-software-development-takes-the-lead-from-code-assistants-to-orchestrated-sdlc-agents/. Acesso em: 02 ago. 2026.

RESEARCHGATE, 2026. *AI-First Software Development Lifecycle: An Agent-Driven Framework for Autonomous Planning, Coding, Testing, and Deployment*. Disponível em: https://www.researchgate.net/publication/403670772_AI-First_Software_Development_Lifecycle_An_Agent-Driven_Framework_for_Autonomous_Planning_Coding_Testing_and_Deployment. Acesso em: 02 ago. 2026.

DEPLOYHQ, 2026. *AI Agents in CI/CD Pipelines: From GitHub Issue to Production Deploy*. Disponível em: https://www.deployhq.com/blog/ai-agents-cicd-pipelines-github-issue-to-production-deploy. Acesso em: 02 ago. 2026.

SPACELIFT, 2026. *Where Do AI Agents Fit in CI/CD Pipelines?*. Disponível em: https://spacelift.io/blog/agentic-cicd. Acesso em: 02 ago. 2026.

MODEL, 2026. *Specification and documentation for the Model Context Protocol*. Model Context Protocol. Disponível em: https://github.com/modelcontextprotocol/modelcontextprotocol. Acesso em: 02 ago. 2026.

WILLISON, Simon, 2026. *Model Context Protocol has prompt injection security problems*. Disponível em: https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/. Acesso em: 02 ago. 2026.

REDIS, 2026. *Context Window Overflow in 2026: Fix LLM Errors Fast*. Disponível em: https://redis.io/blog/context-window-overflow/. Acesso em: 02 ago. 2026.

AGENTA, 2026. *Top techniques to Manage Context Lengths in LLMs*. Disponível em: https://agenta.ai/blog/top-6-techniques-to-manage-context-length-in-llms. Acesso em: 02 ago. 2026.

TOTALUM, 2026. *Claude Code subagents: the 2026 production playbook*. Disponível em: https://www.totalum.app/blog/claude-code-subagents-totalum. Acesso em: 02 ago. 2026.

TEAMVOY, 2026. *AI Agents in CI/CD Pipelines: A Guide for Tech Leads*. Disponível em: https://teamvoy.com/blog/building-ai-agents-into-your-ci-cd-pipeline-a-playbook-for-tech-leads/. Acesso em: 02 ago. 2026.

AUGMENT, 2026. *How to Set Up AI Code Review in Your CI/CD Pipeline*. Augment Code. Disponível em: https://www.augmentcode.com/guides/ai-code-review-ci-cd-pipeline. Acesso em: 02 ago. 2026.

KONISHI, Hidekazu, 2026. *Claude Code Features and Settings Reference 2026*. Disponível em: https://hidekazu-konishi.com/entry/claude_code_features_settings_reference_2026.html. Acesso em: 02 ago. 2026.

APTIBLE, 2026. *Prompt Injection in MCP: Tool Poisoning and Blast Radius*. Disponível em: https://www.aptible.com/mcp-security/mcp-prompt-injection. Acesso em: 02 ago. 2026.

SENTRY, 2026. *Exploiting Tool and Function Calling in LLM Agents*. Disponível em: https://blog.sentry.security/exploiting-tool-and-function-calling-in-llm-agents/. Acesso em: 02 ago. 2026.

MINDSTUDIO, 2026. *What Is an Agent Harness? The Architecture Behind Claude Code, Codex, and Cursor*. Disponível em: https://www.mindstudio.ai/blog/what-is-agent-harness-architecture-explained. Acesso em: 02 ago. 2026.

AIMULTIPLE, 2026. *Top Agent Harnesses: Claude Code vs Codex*. Disponível em: https://aimultiple.com/agent-harness. Acesso em: 02 ago. 2026.
