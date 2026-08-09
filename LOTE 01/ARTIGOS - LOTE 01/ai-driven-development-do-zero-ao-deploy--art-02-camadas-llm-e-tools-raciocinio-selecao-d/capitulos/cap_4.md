# 4 Conclusão

Este recorte demonstrou que a arquitetura que transforma um LLM em um agente de codificação capaz de produzir efeito real no mundo não é monolítica, mas estratificada em três camadas com propriedades e falhas distintas: o raciocínio e a seleção de ferramentas do modelo (HARTENFELLER, 2026; SENTRY, 2026; TOOLTWEAK, 2025), a orquestração via skills, subagentes e servidores MCP (SKILLS, 2026; TOTALUM, 2026; OWASP, 2026), e o contrato de configuração entre humano e agente materializado em CLAUDE.md, AGENTS.md e engenharia de prompt (DEPLOYHQ, 2026; ANTHROPIC, 2025). A convergência de múltiplas fontes independentes — documentação de fornecedor, pesquisa em segurança e relatos corporativos de adoção — indica que nenhuma dessas camadas, isoladamente, garante confiabilidade suficiente para dispensar supervisão humana em ações consequentes (GOVERNED, 2026; GITINJECT, 2026; FORRESTER, 2026).

A implicação prática central é que qualquer política de governança de agentes de codificação precisa endereçar as três camadas simultaneamente: tratar a documentação de ferramentas com o mesmo rigor de um contrato de API (BLAXEL, 2026; AGENTA, 2026), auditar descrições de skills e servidores MCP como superfície de ataque (APTIBLE, 2026; CLOUD, 2026; SYSTEMATIZATION, 2025), e manter arquivos de configuração de projeto concisos o suficiente para não competir com o próprio orçamento de instruções do harness (HUMANLAYER, 2025; HOOKS, 2026). Trabalhos futuros, fora do escopo documental deste recorte, poderiam medir empiricamente a taxa de falha de seleção de ferramentas sob diferentes formatos de documentação, algo que a literatura consultada ainda trata majoritariamente em nível qualitativo (BRIDGING, 2025; WILLISON, 2025).

# Referências

AGENTA. *The guide to structured outputs and function calling with LLMs*. 2026. Disponível em: https://agenta.ai/blog/the-guide-to-structured-outputs-and-function-calling-with-llms. Acesso em: 02 ago. 2026.

ANTHROPIC. *Effective context engineering for AI agents*. 2025. Disponível em: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents. Acesso em: 02 ago. 2026.

APTIBLE. *Prompt Injection in MCP: Tool Poisoning and Blast Radius*. 2026. Disponível em: https://www.aptible.com/mcp-security/mcp-prompt-injection. Acesso em: 02 ago. 2026.

BLAXEL. *What Is LLM Function Calling?*. 2026. Disponível em: https://blaxel.ai/blog/what-is-llm-function-calling. Acesso em: 02 ago. 2026.

BRIDGING AI and Software Security: A Comparative Vulnerability Assessment of LLM Agent Deployment Paradigms. ARXIV.ORG, 2025. Disponível em: https://arxiv.org/pdf/2507.06323. Acesso em: 02 ago. 2026.

CLOUD SECURITY ALLIANCE. *Agentic MCP Security Best Practices Guide*. 2026. Disponível em: https://labs.cloudsecurityalliance.org/agentic/agentic-mcp-security-best-practices-v1/. Acesso em: 02 ago. 2026.

DEPLOYHQ. *CLAUDE.md, AGENTS.md & Copilot Instructions: Configure Every AI Coding Assistant*. 2026. Disponível em: https://www.deployhq.com/blog/ai-coding-config-files-guide. Acesso em: 02 ago. 2026.

FORRESTER. *Agentic Software Development Takes The Lead: From Code Assistants To Orchestrated SDLC Agents*. 2026. Disponível em: https://www.forrester.com/blogs/agentic-software-development-takes-the-lead-from-code-assistants-to-orchestrated-sdlc-agents/. Acesso em: 02 ago. 2026.

GITINJECT: Real-World Prompt Injection Attacks in AI-Powered CI/CD Pipelines. ARXIV.ORG, 2026. Disponível em: https://arxiv.org/pdf/2606.09935. Acesso em: 02 ago. 2026.

GOVERNED AI-Assisted Engineering: Graduated Human Oversight for Agentic Code Generation in Regulated Domains. ARXIV.ORG, 2026. Disponível em: https://arxiv.org/pdf/2606.22484. Acesso em: 02 ago. 2026.

HARTENFELLER. *Best Practices for LLM Tools or Function Calling for Oracle Developers*. 2026. Disponível em: https://hartenfeller.dev/blog/ai-tools-best-practice-oracle. Acesso em: 02 ago. 2026.

HOOKS reference. ANTHROPIC, Claude Code Docs, 2026. Disponível em: https://code.claude.com/docs/en/hooks. Acesso em: 02 ago. 2026.

HUMANLAYER. *Writing a good CLAUDE.md*. 2025. Disponível em: https://www.humanlayer.dev/blog/writing-a-good-claude-md. Acesso em: 02 ago. 2026.

KONISHI, Hidekazu. *Claude Code Subagents and Multi-Agent Orchestration Guide*. 2026. Disponível em: https://hidekazu-konishi.com/entry/claude_code_subagents_and_orchestration_guide.html. Acesso em: 02 ago. 2026.

MCP. *Specification and documentation for the Model Context Protocol*. 2026. Disponível em: https://github.com/modelcontextprotocol/modelcontextprotocol. Acesso em: 02 ago. 2026.

OWASP FOUNDATION. *MCP Tool Poisoning*. 2026. Disponível em: https://owasp.org/www-community/attacks/MCP_Tool_Poisoning. Acesso em: 02 ago. 2026.

SKILLS. Agent Skills — Claude Platform Docs. ANTHROPIC, 2026. Disponível em: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview. Acesso em: 02 ago. 2026.

SUBAGENT Orchestration Guide — Claude Code Skill. MCP MARKET, 2026. Disponível em: https://mcpmarket.com/tools/skills/subagent-orchestration-guide-1. Acesso em: 02 ago. 2026.

SYSTEMATIZATION of Knowledge: Security and Safety in the Model Context Protocol Ecosystem. ARXIV.ORG, 2025. Disponível em: https://arxiv.org/pdf/2512.08290. Acesso em: 02 ago. 2026.

SENTRY. *Exploiting Tool and Function Calling in LLM Agents*. 2026. Disponível em: https://blog.sentry.security/exploiting-tool-and-function-calling-in-llm-agents/. Acesso em: 02 ago. 2026.

TOOLTWEAK: An Attack on Tool Selection in LLM-based Agents. ARXIV.ORG, 2025. Disponível em: https://arxiv.org/pdf/2510.02554. Acesso em: 02 ago. 2026.

TOTALUM. *Claude Code subagents: the 2026 production playbook*. 2026. Disponível em: https://www.totalum.app/blog/claude-code-subagents-totalum. Acesso em: 02 ago. 2026.

WILLISON, Simon. *Model Context Protocol has prompt injection security problems*. 2025. Disponível em: https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/. Acesso em: 02 ago. 2026.
