# 1 Introdução

O desenvolvimento de software orientado por inteligência artificial migrou, entre 2024 e 2026, de um paradigma de autocompletar assistido para um paradigma de agência plena, no qual sistemas baseados em modelos de linguagem de grande porte (LLMs) planejam, selecionam ferramentas e produzem efeitos diretos sobre repositórios, pipelines e ambientes de produção. Dados de mercado recentes indicam adoção ativa por parcela majoritária das organizações de desenvolvimento de software (FUTURUM GROUP, 2026), e a Forrester descreve a migração de assistentes pontuais para agentes orquestradores de ciclo de vida completo como tendência dominante do período (FORRESTER, 2026). Esse deslocamento reabre, contudo, uma pergunta estrutural pouco discutida fora dos manuais de engenharia: o que exatamente acontece entre o instante em que um LLM recebe uma instrução e o instante em que uma ação concreta — escrever um arquivo, chamar uma API, abrir um pull request — é executada no mundo real?

A literatura técnica recente responde a essa pergunta com uma arquitetura em camadas. Anthropic e observadores independentes descrevem o harness — o runtime agêntico que envolve o modelo — como a camada que decide o que é permitido, enquanto o próprio modelo decide apenas o que tentar (PILLITTERI, 2026; MINDSTUDIO, 2026; AIMULTIPLE, 2026). Entre a intenção do modelo e a execução efetiva medeiam mecanismos de raciocínio estruturado — chain-of-thought, ReAct, Tree of Thoughts e Reflexion (IBM, 2026; PROMPTING, 2026; PROMPTHUB, 2026) —, um subsistema de seleção e chamada de ferramentas (function calling) com validação de esquema (HARTENFELLER, 2026; BLAXEL, 2026; AGENTA, 2026; PROMPTLAYER, 2025) e uma camada de composição multiagente que distribui trabalho entre skills, subagentes e servidores do Model Context Protocol (MCP) (SKILLS, 2026; ORCHESTRATE, 2026; MCP, 2026; WIKIPEDIA, 2026). Cada uma dessas camadas amplia o "raio de impacto" (blast radius) potencial de uma decisão tomada por um modelo estatístico, o que desloca o problema de engenharia de "o modelo acerta a resposta?" para "o sistema que envolve o modelo contém o erro antes que ele produza efeito irreversível?" (SENTRY, 2026; OWASP, 2026).

Paralelamente, a camada de contrato entre humano e agente — arquivos como CLAUDE.md e AGENTS.md, que fixam contexto e regras específicas de projeto, e a engenharia de prompt propriamente dita — assumiu papel de especificação operacional, não de sugestão estilística (DEPLOYHQ, 2026; HUMANLAYER, 2025; TEAM400, 2026). Pesquisas sobre limites de seguimento de instrução em LLMs frontier sugerem que modelos seguem de forma confiável um número finito de diretrizes simultâneas, o que impõe restrições objetivas sobre quanto desses arquivos de configuração pode crescer antes de gerar comportamento imprevisível (MODIFYING, 2026; HOOKS, 2026).

## 1.1 Problema de Pesquisa e Objetivo

O problema de pesquisa deste recorte pode ser formulado assim: como as três camadas — raciocínio e seleção de ferramentas do LLM, orquestração via skills/subagentes/MCP, e o contrato de configuração humano-agente — se articulam para produzir (ou falhar em produzir) efeito confiável no mundo real, e quais vulnerabilidades estruturais essa articulação introduz? O objetivo deste artigo é sintetizar, a partir do dossiê técnico consolidado sobre desenvolvimento orientado por IA, uma leitura integrada dessas três camadas, evidenciando tanto os mecanismos que as tornam produtivas (TOTALUM, 2026; KONISHI, 2026; SUBAGENT, 2026) quanto os vetores de risco documentados na literatura de segurança de 2026, notadamente o tool poisoning em servidores MCP (OWASP, 2026; APTIBLE, 2026; WILLISON, 2025; CLOUD, 2026; SYSTEMATIZATION, 2025) e os ataques de seleção adversarial de ferramentas (TOOLTWEAK, 2025; BRIDGING, 2025).

## 1.2 Justificativa

A justificativa deste recorte é dupla. Em primeiro lugar, a maior parte da literatura de mercado trata "agentes de codificação" como uma caixa-preta unificada, obscurecendo o fato de que raciocínio, seleção de ferramentas e orquestração multiagente são subsistemas com falhas e garantias distintas — um agente pode raciocinar corretamente e ainda assim selecionar a ferramenta errada, ou selecionar a ferramenta certa e ainda assim ser vítima de uma descrição de ferramenta envenenada (SENTRY, 2026; OWASP, 2026). Em segundo lugar, práticas corporativas documentadas de integração de agentes em pipelines de CI/CD dependem, na prática, exatamente dessa separação de camadas para manter um portão de aprovação humana antes do deploy em produção (GOVERNED, 2026; GITINJECT, 2026), o que torna a compreensão precisa de cada camada uma condição prévia para qualquer política de governança de risco aplicada a esses sistemas. O restante do artigo detalha, na Seção 2, como o recorte foi construído a partir do dossiê-mãe; na Seção 3, discute em profundidade as três camadas e suas interseções; e na Seção 4, sintetiza as implicações práticas.

# Referências

AGENTA. *The guide to structured outputs and function calling with LLMs*. 2026. Disponível em: https://agenta.ai/blog/the-guide-to-structured-outputs-and-function-calling-with-llms. Acesso em: 02 ago. 2026.

AIMULTIPLE. *Top Agent Harnesses: Claude Code vs Codex*. 2026. Disponível em: https://aimultiple.com/agent-harness. Acesso em: 02 ago. 2026.

APTIBLE. *Prompt Injection in MCP: Tool Poisoning and Blast Radius*. 2026. Disponível em: https://www.aptible.com/mcp-security/mcp-prompt-injection. Acesso em: 02 ago. 2026.

BLAXEL. *What Is LLM Function Calling?*. 2026. Disponível em: https://blaxel.ai/blog/what-is-llm-function-calling. Acesso em: 02 ago. 2026.

BRIDGING AI and Software Security: A Comparative Vulnerability Assessment of LLM Agent Deployment Paradigms. ARXIV.ORG, 2025. Disponível em: https://arxiv.org/pdf/2507.06323. Acesso em: 02 ago. 2026.

CLOUD SECURITY ALLIANCE. *Agentic MCP Security Best Practices Guide*. 2026. Disponível em: https://labs.cloudsecurityalliance.org/agentic/agentic-mcp-security-best-practices-v1/. Acesso em: 02 ago. 2026.

DEPLOYHQ. *CLAUDE.md, AGENTS.md & Copilot Instructions: Configure Every AI Coding Assistant*. 2026. Disponível em: https://www.deployhq.com/blog/ai-coding-config-files-guide. Acesso em: 02 ago. 2026.

FORRESTER. *Agentic Software Development Takes The Lead: From Code Assistants To Orchestrated SDLC Agents*. 2026. Disponível em: https://www.forrester.com/blogs/agentic-software-development-takes-the-lead-from-code-assistants-to-orchestrated-sdlc-agents/. Acesso em: 02 ago. 2026.

FUTURUM GROUP. *AI Reaches 97% of Software Development Organizations*. 2026. Disponível em: https://futurumgroup.com/press-release/ai-reaches-97-of-software-development-organizations/. Acesso em: 02 ago. 2026.

GITINJECT: Real-World Prompt Injection Attacks in AI-Powered CI/CD Pipelines. ARXIV.ORG, 2026. Disponível em: https://arxiv.org/pdf/2606.09935. Acesso em: 02 ago. 2026.

GOVERNED AI-Assisted Engineering: Graduated Human Oversight for Agentic Code Generation in Regulated Domains. ARXIV.ORG, 2026. Disponível em: https://arxiv.org/pdf/2606.22484. Acesso em: 02 ago. 2026.

HARTENFELLER. *Best Practices for LLM Tools or Function Calling for Oracle Developers*. 2026. Disponível em: https://hartenfeller.dev/blog/ai-tools-best-practice-oracle. Acesso em: 02 ago. 2026.

HOOKS reference. ANTHROPIC, Claude Code Docs, 2026. Disponível em: https://code.claude.com/docs/en/hooks. Acesso em: 02 ago. 2026.

HUMANLAYER. *Writing a good CLAUDE.md*. 2025. Disponível em: https://www.humanlayer.dev/blog/writing-a-good-claude-md. Acesso em: 02 ago. 2026.

IBM. *What is chain of thought (CoT) prompting?*. 2026. Disponível em: https://www.ibm.com/think/topics/chain-of-thoughts. Acesso em: 02 ago. 2026.

KONISHI, Hidekazu. *Claude Code Subagents and Multi-Agent Orchestration Guide*. 2026. Disponível em: https://hidekazu-konishi.com/entry/claude_code_subagents_and_orchestration_guide.html. Acesso em: 02 ago. 2026.

MCP. *Specification and documentation for the Model Context Protocol*. 2026. Disponível em: https://github.com/modelcontextprotocol/modelcontextprotocol. Acesso em: 02 ago. 2026.

MINDSTUDIO. *What Is an Agent Harness? The Architecture Behind Claude Code, Codex, and Cursor*. 2026. Disponível em: https://www.mindstudio.ai/blog/what-is-agent-harness-architecture-explained. Acesso em: 02 ago. 2026.

MODIFYING system prompts. ANTHROPIC, Claude API Docs, 2026. Disponível em: https://platform.claude.com/docs/en/agent-sdk/modifying-system-prompts. Acesso em: 02 ago. 2026.

ORCHESTRATE subagents at scale with dynamic workflows. ANTHROPIC, Claude Code Docs, 2026. Disponível em: https://code.claude.com/docs/en/workflows. Acesso em: 02 ago. 2026.

OWASP FOUNDATION. *MCP Tool Poisoning*. 2026. Disponível em: https://owasp.org/www-community/attacks/MCP_Tool_Poisoning. Acesso em: 02 ago. 2026.

PILLITTERI, Pasquale. *Claude Code Harness: The Runtime Architecture That Turns an LLM into an Autonomous Agent*. 2026. Disponível em: https://pasqualepillitteri.it/en/news/1892/claude-code-harness-runtime-architecture-2026-guide. Acesso em: 02 ago. 2026.

PROMPTHUB. *Prompt Engineering for AI Agents*. 2026. Disponível em: https://www.prompthub.us/blog/prompt-engineering-for-ai-agents. Acesso em: 02 ago. 2026.

PROMPTING GUIDE. *Tree of Thoughts (ToT)*. 2026. Disponível em: https://www.promptingguide.ai/techniques/tot. Acesso em: 02 ago. 2026.

PROMPTLAYER. *How JSON Schema Works for LLM Tools & Structured Outputs*. 2025. Disponível em: https://blog.promptlayer.com/how-json-schema-works-for-structured-outputs-and-tool-integration/. Acesso em: 02 ago. 2026.

SENTRY. *Exploiting Tool and Function Calling in LLM Agents*. 2026. Disponível em: https://blog.sentry.security/exploiting-tool-and-function-calling-in-llm-agents/. Acesso em: 02 ago. 2026.

SKILLS. Agent Skills — Claude Platform Docs. ANTHROPIC, 2026. Disponível em: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview. Acesso em: 02 ago. 2026.

SUBAGENT Orchestration Guide — Claude Code Skill. MCP MARKET, 2026. Disponível em: https://mcpmarket.com/tools/skills/subagent-orchestration-guide-1. Acesso em: 02 ago. 2026.

SYSTEMATIZATION of Knowledge: Security and Safety in the Model Context Protocol Ecosystem. ARXIV.ORG, 2025. Disponível em: https://arxiv.org/pdf/2512.08290. Acesso em: 02 ago. 2026.

TEAM400. *Claude Agent SDK — How to Customise System Prompts for Your AI Agents*. 2026. Disponível em: https://team400.ai/blog/2026-04-claude-agent-sdk-system-prompts-customisation. Acesso em: 02 ago. 2026.

TOOLTWEAK: An Attack on Tool Selection in LLM-based Agents. ARXIV.ORG, 2025. Disponível em: https://arxiv.org/pdf/2510.02554. Acesso em: 02 ago. 2026.

TOTALUM. *Claude Code subagents: the 2026 production playbook*. 2026. Disponível em: https://www.totalum.app/blog/claude-code-subagents-totalum. Acesso em: 02 ago. 2026.

WIKIPEDIA. *Model Context Protocol*. 2026. Disponível em: https://en.wikipedia.org/wiki/Model_Context_Protocol. Acesso em: 02 ago. 2026.

WILLISON, Simon. *Model Context Protocol has prompt injection security problems*. 2025. Disponível em: https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/. Acesso em: 02 ago. 2026.
