# 4 Conclusão

Este recorte investigativo mostrou que a governança de agentes de codificação não se resolve por uma única técnica, mas pela composição de quatro camadas complementares. A primeira é a configuração explícita do harness via `settings.json`, hooks e permissions (EXPLAINX, 2026). A abordagem multicamadas dessa configuração é descrita em detalhe por General (2026). A segunda é a construção de tools e servidores MCP com schemas validados e blindagem ativa contra tool poisoning (OWASP, 2026), problema documentado de forma independente por Microsoft (2026) e também por Willison (2026). A terceira é a disciplina de economia severa de tokens como pré-condição de sustentabilidade operacional em sessões estendidas (ANTHROPIC, 2026), sustentada teoricamente pelo corpus indexado em Arxiv (2026). A quarta é o portão de aprovação humana obrigatório entre a mudança de código proposta pelo agente e o deploy em produção (DEPLOYHQ, 2026), padrão confirmado na prática por Teamvoy (2026). A convergência entre documentação primária de fornecedor, catálogos de ataque de organismos independentes e relatos de prática de mercado sustenta a mesma conclusão a partir de ângulos distintos: nenhuma dessas camadas, isoladamente, neutraliza os riscos documentados de alucinação, injeção de prompt indireta e explosão de custo de contexto que acompanham a adoção acelerada de IA agêntica em desenvolvimento de software, tendência de mercado quantificada por Futurum (2026) e por Forrester (2026).

A principal implicação prática deste recorte é que equipes que adotam harnesses agênticos como Claude Code devem tratar as quatro camadas como um requisito único de arquitetura, não como itens de configuração independentes a serem endereçados em momentos separados do ciclo de maturidade — a antepara mais fraca determina o nível de exposição real da esteira inteira, independentemente de quão bem configuradas estejam as demais.

## Referências Bibliográficas

EXPLAINX, 2026. *Claude Code settings.json: Every Option Explained*. Disponível em: https://www.explainx.ai/blog/claude-code-settings-json-complete-reference-2026. Acesso em: 02 ago. 2026.

GENERAL, 2026. *Anthropic Claude Code Security Best Practices: Permissions, Hooks, MCP, Sandboxing, and CI/CD*. General Analysis. Disponível em: https://generalanalysis.com/guides/anthropic-claude-code-security-best-practices. Acesso em: 02 ago. 2026.

OWASP, 2026. *MCP Tool Poisoning*. Disponível em: https://owasp.org/www-community/attacks/MCP_Tool_Poisoning. Acesso em: 02 ago. 2026.

MICROSOFT, 2026. *Protecting against indirect prompt injection attacks in MCP*. Disponível em: https://developer.microsoft.com/blog/protecting-against-indirect-injection-attacks-mcp/. Acesso em: 02 ago. 2026.

WILLISON, Simon, 2026. *Model Context Protocol has prompt injection security problems*. Disponível em: https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/. Acesso em: 02 ago. 2026.

ANTHROPIC, 2026. *Effective harnesses for long-running agents*. Disponível em: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents. Acesso em: 02 ago. 2026.

ARXIV, 2026. *GitInject: Real-World Prompt Injection Attacks in AI-Powered CI/CD Pipelines*. Disponível em: https://arxiv.org/pdf/2606.09935. Acesso em: 02 ago. 2026.

DEPLOYHQ, 2026. *AI Agents in CI/CD Pipelines: From GitHub Issue to Production Deploy*. Disponível em: https://www.deployhq.com/blog/ai-agents-cicd-pipelines-github-issue-to-production-deploy. Acesso em: 02 ago. 2026.

TEAMVOY, 2026. *AI Agents in CI/CD Pipelines: A Guide for Tech Leads*. Disponível em: https://teamvoy.com/blog/building-ai-agents-into-your-ci-cd-pipeline-a-playbook-for-tech-leads/. Acesso em: 02 ago. 2026.

FUTURUM, 2026. *AI Reaches 97% of Software Development Organizations*. Futurum Group. Disponível em: https://futurumgroup.com/press-release/ai-reaches-97-of-software-development-organizations/. Acesso em: 02 ago. 2026.

FORRESTER, 2026. *Agentic Software Development Takes The Lead: From Code Assistants To Orchestrated SDLC Agents*. Disponível em: https://www.forrester.com/blogs/agentic-software-development-takes-the-lead-from-code-assistants-to-orchestrated-sdlc-agents/. Acesso em: 02 ago. 2026.

CLOUD, 2026. *Agentic MCP Security Best Practices Guide*. Cloud Security Alliance. Disponível em: https://labs.cloudsecurityalliance.org/agentic/agentic-mcp-security-best-practices-v1/. Acesso em: 02 ago. 2026.

APTIBLE, 2026. *Prompt Injection in MCP: Tool Poisoning and Blast Radius*. Disponível em: https://www.aptible.com/mcp-security/mcp-prompt-injection. Acesso em: 02 ago. 2026.

SENTRY, 2026. *Exploiting Tool and Function Calling in LLM Agents*. Disponível em: https://blog.sentry.security/exploiting-tool-and-function-calling-in-llm-agents/. Acesso em: 02 ago. 2026.

AGENTA, 2026. *Top techniques to Manage Context Lengths in LLMs*. Disponível em: https://agenta.ai/blog/top-6-techniques-to-manage-context-length-in-llms. Acesso em: 02 ago. 2026.

REDIS, 2026. *Context Window Overflow in 2026: Fix LLM Errors Fast*. Disponível em: https://redis.io/blog/context-window-overflow/. Acesso em: 02 ago. 2026.

TOTALUM, 2026. *Claude Code subagents: the 2026 production playbook*. Disponível em: https://www.totalum.app/blog/claude-code-subagents-totalum. Acesso em: 02 ago. 2026.

RESEARCHGATE, 2026. *AI-First Software Development Lifecycle: An Agent-Driven Framework for Autonomous Planning, Coding, Testing, and Deployment*. Disponível em: https://www.researchgate.net/publication/403670772_AI-First_Software_Development_Lifecycle_An_Agent-Driven_Framework_for_Autonomous_Planning_Coding_Testing_and_Deployment. Acesso em: 02 ago. 2026.

FUJITSU, 2026. *Fujitsu automates entire software development lifecycle with new AI-Driven Software Development Platform*. Disponível em: https://global.fujitsu/en-global/pr/news/2026/02/17-01. Acesso em: 02 ago. 2026.

HUMANLAYER, 2026. *12-Factor Agents — Principles for Building Reliable LLM Applications*. Disponível em: https://www.humanlayer.dev/12-factor-agents. Acesso em: 02 ago. 2026.

MINDSTUDIO, 2026. *What Is an Agent Harness? The Architecture Behind Claude Code, Codex, and Cursor*. Disponível em: https://www.mindstudio.ai/blog/what-is-agent-harness-architecture-explained. Acesso em: 02 ago. 2026.

AIMULTIPLE, 2026. *Top Agent Harnesses: Claude Code vs Codex*. Disponível em: https://aimultiple.com/agent-harness. Acesso em: 02 ago. 2026.

MODEL, 2026. *Specification and documentation for the Model Context Protocol*. Model Context Protocol. Disponível em: https://github.com/modelcontextprotocol/modelcontextprotocol. Acesso em: 02 ago. 2026.
