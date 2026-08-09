# 4 Conclusão

A síntese apresentada neste recorte sustenta que a transição de *vibe coding* para
*agentic coding* não é uma mudança de grau de conveniência, mas uma mudança de
arquitetura de controle: a autonomia do agente só se torna confiável quando
ladeada por superfícies de verificação explícitas — testes automatizados como
definição prévia de correção (Arxiv, 2025), e um modelo de quatro camadas — Tela,
Harness, LLM e Tools — que distribui, entre interface de supervisão humana e
runtime do agente, a responsabilidade de decidir o que é permitido antes de
decidir o que é tentado (Pillitteri, 2026; Mindstudio, 2026). A interseção entre
Tela e Harness, examinada com maior densidade neste artigo, mostra que padrões
como *intent preview*, *approval gates* e estimativa de "raio de impacto" só
funcionam porque o Harness já aplicou, previamente, um pipeline determinístico de
permissões (Github, 2026; Konishi, 2026).

Como implicação prática, a literatura converge em recomendar que a adoção
corporativa de ferramentas agênticas de codificação seja avaliada não pelo poder
de raciocínio do modelo isoladamente, mas pela robustez do harness que o envolve —
sua capacidade de expor *intent preview* legível, aplicar portões de aprovação
graduados e resistir a ataques direcionados à camada de ferramentas, como o
envenenamento de ferramentas via MCP (Owasp, 2026; Anthropic, 2026). Capítulos
subsequentes desta série de recortes tratam, com maior profundidade técnica, as
camadas LLM e Tools e a configuração prática de harness em ambiente de produção.

# Referências

AGENTA. The guide to structured outputs and function calling with LLMs. 2026. Disponível em: https://agenta.ai/blog/the-guide-to-structured-outputs-and-function-calling-with-llms. Acesso em: 02 ago. 2026.

AIMULTIPLE. Top agent harnesses: Claude Code vs Codex. 2026. Disponível em: https://aimultiple.com/agent-harness. Acesso em: 02 ago. 2026.

ANTHROPIC. Building effective AI agents. 2026. Disponível em: https://www.anthropic.com/research/building-effective-agents. Acesso em: 02 ago. 2026.

ARTEZIO. 2026 playbook for software development — LLMs' roadmap for languages, skills & AI. 2026. Disponível em: https://www.artezio.com/pressroom/blog/playbook-development-languages/. Acesso em: 02 ago. 2026.

ARXIV. Towards optimizing the costs of LLM usage. 2024. Disponível em: https://arxiv.org/pdf/2402.01742. Acesso em: 02 ago. 2026.

ARXIV. Vibe coding vs. agentic coding: fundamentals and practical implications of agentic AI. 2025. Disponível em: https://arxiv.org/pdf/2505.19443. Acesso em: 02 ago. 2026.

ARXIV. Agentic AI in the software development lifecycle. 2026. Disponível em: https://arxiv.org/pdf/2604.26275. Acesso em: 02 ago. 2026.

BLAXEL. What is LLM function calling?. 2026. Disponível em: https://blaxel.ai/blog/what-is-llm-function-calling. Acesso em: 02 ago. 2026.

COMET. Prompt engineering for agentic AI systems: an introduction. 2026. Disponível em: https://www.comet.com/site/blog/prompt-engineering/. Acesso em: 02 ago. 2026.

FORRESTER. Agentic software development takes the lead: from code assistants to orchestrated SDLC agents. 2026. Disponível em: https://www.forrester.com/blogs/agentic-software-development-takes-the-lead-from-code-assistants-to-orchestrated-sdlc-agents/. Acesso em: 02 ago. 2026.

FUJITSU. Fujitsu automates entire software development lifecycle with new AI-driven software development platform. 2026. Disponível em: https://global.fujitsu/en-global/pr/news/2026/02/17-01. Acesso em: 02 ago. 2026.

FUTURUM GROUP. AI reaches 97% of software development organizations. 2026. Disponível em: https://futurumgroup.com/press-release/ai-reaches-97-of-software-development-organizations/. Acesso em: 02 ago. 2026.

GITHUB. Claude Code system prompts. 2026. Disponível em: https://github.com/Piebald-AI/claude-code-system-prompts. Acesso em: 02 ago. 2026.

HARTENFELLER. Best practices for LLM tools or function calling for Oracle developers. 2026. Disponível em: https://hartenfeller.dev/blog/ai-tools-best-practice-oracle. Acesso em: 02 ago. 2026.

HUMANLAYER. Writing a good CLAUDE.md. 2026. Disponível em: https://www.humanlayer.dev/blog/writing-a-good-claude-md. Acesso em: 02 ago. 2026.

IBM. What is chain of thought (CoT) prompting?. 2026. Disponível em: https://www.ibm.com/think/topics/chain-of-thoughts. Acesso em: 02 ago. 2026.

KONISHI, Hidekazu. Claude Code features and settings reference 2026. 2026. Disponível em: https://hidekazu-konishi.com/entry/claude_code_features_settings_reference_2026.html. Acesso em: 02 ago. 2026.

MICROSOFT. An AI led SDLC: building an end-to-end agentic software development lifecycle with Azure and GitHub. 2026. Disponível em: https://techcommunity.microsoft.com/blog/appsonazureblog/an-ai-led-sdlc-building-an-end-to-end-agentic-software-development-lifecycle-wit/4491896. Acesso em: 02 ago. 2026.

MINDSTUDIO. What is an agent harness? The architecture behind Claude Code, Codex, and Cursor. 2026. Disponível em: https://www.mindstudio.ai/blog/what-is-agent-harness-architecture-explained. Acesso em: 02 ago. 2026.

OWASP FOUNDATION. MCP tool poisoning. 2026. Disponível em: https://owasp.org/www-community/attacks/MCP_Tool_Poisoning. Acesso em: 02 ago. 2026.

PILLITTERI, Pasquale. Claude Code harness: the runtime architecture that turns an LLM into an autonomous agent. 2026. Disponível em: https://pasqualepillitteri.it/en/news/1892/claude-code-harness-runtime-architecture-2026-guide. Acesso em: 02 ago. 2026.

PROMPTHUB. Prompt engineering for AI agents. 2026. Disponível em: https://www.prompthub.us/blog/prompt-engineering-for-ai-agents. Acesso em: 02 ago. 2026.

RESEARCHGATE. AI-first software development lifecycle: an agent-driven framework for autonomous planning, coding, testing, and deployment. 2026. Disponível em: https://www.researchgate.net/publication/403670772_AI-First_Software_Development_Lifecycle_An_Agent-Driven_Framework_for_Autonomous_Planning_Coding_Testing_and_Deployment. Acesso em: 02 ago. 2026.

WAVESPEED AI. Claude Code agent harness: architecture breakdown. 2026. Disponível em: https://wavespeed.ai/blog/posts/claude-code-agent-harness-architecture/. Acesso em: 02 ago. 2026.

WIKIPEDIA. Model context protocol. 2026. Disponível em: https://en.wikipedia.org/wiki/Model_Context_Protocol. Acesso em: 02 ago. 2026.
