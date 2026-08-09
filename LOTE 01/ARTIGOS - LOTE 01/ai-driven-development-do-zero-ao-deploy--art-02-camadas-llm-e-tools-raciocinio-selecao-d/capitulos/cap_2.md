# 2 Metodologia

Este artigo não reporta um experimento controlado nem coleta dados primários; trata-se de um recorte investigativo de natureza documental-analítica, construído por reaproveitamento de um dossiê técnico já indexado, consolidado previamente sobre desenvolvimento de software orientado por IA. O método, portanto, não é o de validação empírica de hipótese, mas o de síntese estruturada de literatura técnica e científica já mineirada, organizada segundo um recorte temático específico dentro de uma obra-mãe mais ampla.

## 2.1 Corpus e Fonte de Dados

O corpus deste recorte corresponde aos blocos de conteúdo indexados nos capítulos 4, 5 e 6 do sumário macro da obra-mãe "AI Driven Development: Do Zero ao Deploy", que tratam, respectivamente, da arquitetura em quatro camadas (Tela, Harness, LLM, Tools) (MINDSTUDIO, 2026; PILLITTERI, 2026; AIMULTIPLE, 2026), da configuração de skills, subagentes e MCP (SKILLS, 2026; ORCHESTRATE, 2026; MCP, 2026; TOTALUM, 2026; KONISHI, 2026) e da engenharia de prompt e dos arquivos de contrato CLAUDE.md/AGENTS.md (DEPLOYHQ, 2026; HUMANLAYER, 2025; TEAM400, 2026; MODIFYING, 2026). Esse dossiê consolida mais de oitenta fontes brutas verificáveis — documentação oficial de fornecedores, artigos de pesquisa em repositórios de pré-publicação e relatos técnicos de adoção corporativa —, das quais este recorte seleciona e reorganiza o subconjunto pertinente aos três pilares enunciados na introdução.

## 2.2 Critério de Seleção e Recorte

O critério de seleção de blocos obedeceu a relevância temática recuperada por indexação semântica local (TF-IDF) sobre o dossiê-mãe, consultado por meio de buscas dirigidas aos três pilares: (i) raciocínio do LLM e seleção de ferramentas com efeito real no mundo (HARTENFELLER, 2026; BLAXEL, 2026; SENTRY, 2026; AGENTA, 2026; PROMPTLAYER, 2025; IBM, 2026; PROMPTING, 2026; PROMPTHUB, 2026; COMET, 2026); (ii) orquestração via skills, subagentes e MCP (WIKIPEDIA, 2026; WEBFUSE, 2026; SUBAGENT, 2026); e (iii) o contrato de configuração entre humano e agente via CLAUDE.md/AGENTS.md e engenharia de prompt (HOOKS, 2026; HUMANLAYER, 2026). Nenhuma fonte nova foi pesquisada para a produção deste artigo — a regra de reaproveitamento integral do dossiê-mãe é deliberada, e visa preservar a rastreabilidade entre a obra completa e cada recorte derivado, evitando divergência factual entre livro-mãe e artigos.

## 2.3 Procedimento de Síntese

A partir dos blocos recuperados, o procedimento de síntese seguiu três etapas: primeiro, agrupamento dos blocos por pilar temático; segundo, identificação de convergências e tensões entre fontes (por exemplo, entre a promessa de autonomia de orquestração multiagente e os riscos de segurança documentados para MCP) (OWASP, 2026; APTIBLE, 2026; WILLISON, 2025; CLOUD, 2026; GENERAL, 2026; SYSTEMATIZATION, 2025); terceiro, redação impessoal em terceira pessoa com citação autor-data obrigatória para toda afirmação factual, seguindo a norma NBR 10520, e numeração progressiva de seções conforme a NBR 6024. Vetores de risco documentados em pesquisa recente sobre ataques de seleção de ferramentas (TOOLTWEAK, 2025; BRIDGING, 2025) e sobre injeção de prompt em pipelines de CI/CD (GITINJECT, 2026) foram tratados como achados de igual peso analítico aos relatos de adoção corporativa (FORRESTER, 2026; FUTURUM GROUP, 2026), evitando o viés de otimismo tecnológico comum em material de marketing de fornecedores.

## 2.4 Limitações do Método

Por depender de um dossiê já constituído, este recorte herda as limitações da pesquisa original: predominância de fontes de documentação técnica de fornecedores e de blogs especializados sobre artigos revisados por pares, e uma janela temporal concentrada em 2024–2026, período de mudança acelerada nas práticas de mercado (GOVERNED, 2026). A ausência de coleta primária impede qualquer inferência causal sobre eficácia comparada entre arquiteturas de orquestração (LangGraph, CrewAI, AutoGen ou Dynamic Workflows); o artigo limita-se a mapear o estado documentado da técnica e suas tensões internas, não a medi-lo empiricamente (CODEANT, 2026; YAGE, 2026; LUHARUKA, 2026; REDIS, 2026; REDIS, 2025).

# Referências

AGENTA. *The guide to structured outputs and function calling with LLMs*. 2026. Disponível em: https://agenta.ai/blog/the-guide-to-structured-outputs-and-function-calling-with-llms. Acesso em: 02 ago. 2026.

AIMULTIPLE. *Top Agent Harnesses: Claude Code vs Codex*. 2026. Disponível em: https://aimultiple.com/agent-harness. Acesso em: 02 ago. 2026.

APTIBLE. *Prompt Injection in MCP: Tool Poisoning and Blast Radius*. 2026. Disponível em: https://www.aptible.com/mcp-security/mcp-prompt-injection. Acesso em: 02 ago. 2026.

BLAXEL. *What Is LLM Function Calling?*. 2026. Disponível em: https://blaxel.ai/blog/what-is-llm-function-calling. Acesso em: 02 ago. 2026.

BRIDGING AI and Software Security: A Comparative Vulnerability Assessment of LLM Agent Deployment Paradigms. ARXIV.ORG, 2025. Disponível em: https://arxiv.org/pdf/2507.06323. Acesso em: 02 ago. 2026.

CLOUD SECURITY ALLIANCE. *Agentic MCP Security Best Practices Guide*. 2026. Disponível em: https://labs.cloudsecurityalliance.org/agentic/agentic-mcp-security-best-practices-v1/. Acesso em: 02 ago. 2026.

CODEANT. *Why Your Coding Agent Should Use ripgrep (rg) Instead of grep*. 2026. Disponível em: https://codeant.ai/blogs/why-coding-agents-should-use-ripgrep. Acesso em: 02 ago. 2026.

COMET. *Prompt Engineering for Agentic AI Systems: An Introduction*. 2026. Disponível em: https://www.comet.com/site/blog/prompt-engineering/. Acesso em: 02 ago. 2026.

DEPLOYHQ. *CLAUDE.md, AGENTS.md & Copilot Instructions: Configure Every AI Coding Assistant*. 2026. Disponível em: https://www.deployhq.com/blog/ai-coding-config-files-guide. Acesso em: 02 ago. 2026.

FORRESTER. *Agentic Software Development Takes The Lead: From Code Assistants To Orchestrated SDLC Agents*. 2026. Disponível em: https://www.forrester.com/blogs/agentic-software-development-takes-the-lead-from-code-assistants-to-orchestrated-sdlc-agents/. Acesso em: 02 ago. 2026.

FUTURUM GROUP. *AI Reaches 97% of Software Development Organizations*. 2026. Disponível em: https://futurumgroup.com/press-release/ai-reaches-97-of-software-development-organizations/. Acesso em: 02 ago. 2026.

GENERAL ANALYSIS. *Anthropic Claude Code Security Best Practices: Permissions, Hooks, MCP, Sandboxing, and CI/CD*. 2026. Disponível em: https://generalanalysis.com/guides/anthropic-claude-code-security-best-practices. Acesso em: 02 ago. 2026.

GITINJECT: Real-World Prompt Injection Attacks in AI-Powered CI/CD Pipelines. ARXIV.ORG, 2026. Disponível em: https://arxiv.org/pdf/2606.09935. Acesso em: 02 ago. 2026.

GOVERNED AI-Assisted Engineering: Graduated Human Oversight for Agentic Code Generation in Regulated Domains. ARXIV.ORG, 2026. Disponível em: https://arxiv.org/pdf/2606.22484. Acesso em: 02 ago. 2026.

HARTENFELLER. *Best Practices for LLM Tools or Function Calling for Oracle Developers*. 2026. Disponível em: https://hartenfeller.dev/blog/ai-tools-best-practice-oracle. Acesso em: 02 ago. 2026.

HOOKS reference. ANTHROPIC, Claude Code Docs, 2026. Disponível em: https://code.claude.com/docs/en/hooks. Acesso em: 02 ago. 2026.

HUMANLAYER. *Writing a good CLAUDE.md*. 2025. Disponível em: https://www.humanlayer.dev/blog/writing-a-good-claude-md. Acesso em: 02 ago. 2026.

HUMANLAYER. *12-Factor Agents — Principles for Building Reliable LLM Applications*. 2026. Disponível em: https://www.humanlayer.dev/12-factor-agents. Acesso em: 02 ago. 2026.

IBM. *What is chain of thought (CoT) prompting?*. 2026. Disponível em: https://www.ibm.com/think/topics/chain-of-thoughts. Acesso em: 02 ago. 2026.

KONISHI, Hidekazu. *Claude Code Subagents and Multi-Agent Orchestration Guide*. 2026. Disponível em: https://hidekazu-konishi.com/entry/claude_code_subagents_and_orchestration_guide.html. Acesso em: 02 ago. 2026.

LUHARUKA, Shubham. *Context Optimization: A Comprehensive Framework for Reducing Large Language Model Token Usage*. 2026. Disponível em: https://luharuka.medium.com/context-optimization-a-comprehensive-framework-for-reducing-large-language-model-token-usage-fed8d9229e30. Acesso em: 02 ago. 2026.

MCP. *Specification and documentation for the Model Context Protocol*. 2026. Disponível em: https://github.com/modelcontextprotocol/modelcontextprotocol. Acesso em: 02 ago. 2026.

MINDSTUDIO. *What Is an Agent Harness? The Architecture Behind Claude Code, Codex, and Cursor*. 2026. Disponível em: https://www.mindstudio.ai/blog/what-is-agent-harness-architecture-explained. Acesso em: 02 ago. 2026.

MODIFYING system prompts. ANTHROPIC, Claude API Docs, 2026. Disponível em: https://platform.claude.com/docs/en/agent-sdk/modifying-system-prompts. Acesso em: 02 ago. 2026.

ORCHESTRATE subagents at scale with dynamic workflows. ANTHROPIC, Claude Code Docs, 2026. Disponível em: https://code.claude.com/docs/en/workflows. Acesso em: 02 ago. 2026.

OWASP FOUNDATION. *MCP Tool Poisoning*. 2026. Disponível em: https://owasp.org/www-community/attacks/MCP_Tool_Poisoning. Acesso em: 02 ago. 2026.

PILLITTERI, Pasquale. *Claude Code Harness: The Runtime Architecture That Turns an LLM into an Autonomous Agent*. 2026. Disponível em: https://pasqualepillitteri.it/en/news/1892/claude-code-harness-runtime-architecture-2026-guide. Acesso em: 02 ago. 2026.

PROMPTHUB. *Prompt Engineering for AI Agents*. 2026. Disponível em: https://www.prompthub.us/blog/prompt-engineering-for-ai-agents. Acesso em: 02 ago. 2026.

PROMPTING GUIDE. *Tree of Thoughts (ToT)*. 2026. Disponível em: https://www.promptingguide.ai/techniques/tot. Acesso em: 02 ago. 2026.

PROMPTLAYER. *How JSON Schema Works for LLM Tools & Structured Outputs*. 2025. Disponível em: https://blog.promptlayer.com/how-json-schema-works-for-structured-outputs-and-tool-integration/. Acesso em: 02 ago. 2026.

REDIS. *Context Window Overflow in 2026: Fix LLM Errors Fast*. 2026. Disponível em: https://redis.io/blog/context-window-overflow/. Acesso em: 02 ago. 2026.

REDIS. *Context Window Management for LLM Apps: Dev Guide*. 2025. Disponível em: https://redis.io/blog/context-window-management-llm-apps-developer-guide/. Acesso em: 02 ago. 2026.

SENTRY. *Exploiting Tool and Function Calling in LLM Agents*. 2026. Disponível em: https://blog.sentry.security/exploiting-tool-and-function-calling-in-llm-agents/. Acesso em: 02 ago. 2026.

SKILLS. Agent Skills — Claude Platform Docs. ANTHROPIC, 2026. Disponível em: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview. Acesso em: 02 ago. 2026.

SUBAGENT Orchestration Guide — Claude Code Skill. MCP MARKET, 2026. Disponível em: https://mcpmarket.com/tools/skills/subagent-orchestration-guide-1. Acesso em: 02 ago. 2026.

SYSTEMATIZATION of Knowledge: Security and Safety in the Model Context Protocol Ecosystem. ARXIV.ORG, 2025. Disponível em: https://arxiv.org/pdf/2512.08290. Acesso em: 02 ago. 2026.

TEAM400. *Claude Agent SDK — How to Customise System Prompts for Your AI Agents*. 2026. Disponível em: https://team400.ai/blog/2026-04-claude-agent-sdk-system-prompts-customisation. Acesso em: 02 ago. 2026.

TOOLTWEAK: An Attack on Tool Selection in LLM-based Agents. ARXIV.ORG, 2025. Disponível em: https://arxiv.org/pdf/2510.02554. Acesso em: 02 ago. 2026.

TOTALUM. *Claude Code subagents: the 2026 production playbook*. 2026. Disponível em: https://www.totalum.app/blog/claude-code-subagents-totalum. Acesso em: 02 ago. 2026.

WEBFUSE. *MCP Cheat Sheet: Model Context Protocol Quick Reference*. 2026. Disponível em: https://www.webfuse.com/mcp-cheat-sheet. Acesso em: 02 ago. 2026.

WIKIPEDIA. *Model Context Protocol*. 2026. Disponível em: https://en.wikipedia.org/wiki/Model_Context_Protocol. Acesso em: 02 ago. 2026.

WILLISON, Simon. *Model Context Protocol has prompt injection security problems*. 2025. Disponível em: https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/. Acesso em: 02 ago. 2026.

YAGE.AI. *Why Coding Agents Still Use grep as Their Search Backbone*. 2026. Disponível em: https://yage.ai/share/why-coding-agents-still-use-grep-en-20260327.html. Acesso em: 02 ago. 2026.
