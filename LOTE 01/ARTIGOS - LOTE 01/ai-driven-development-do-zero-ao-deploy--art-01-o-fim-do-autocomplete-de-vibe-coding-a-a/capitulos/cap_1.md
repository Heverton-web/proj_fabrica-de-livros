# 1 Introdução

## 1.1 Contextualização e Problema de Pesquisa

Entre 2024 e 2026 a engenharia de software atravessa uma mudança estrutural que a
literatura técnica compara à adoção do DevOps e do Agile: modelos de linguagem de
grande porte (LLMs) deixam de operar como "autocomplete avançado" — paradigma
denominado *vibe coding*, em que o desenvolvedor permanece integralmente no loop,
revisando cada sugestão em modo conversacional — para atuar como agentes autônomos
capazes de planejar, executar, testar e iterar tarefas inteiras do ciclo de
engenharia sob supervisão mínima, paradigma denominado *agentic coding* (ARXIV,
2025). A distinção entre os dois paradigmas não é apenas de grau de autonomia, mas
de arquitetura de controle: a codificação agêntica trata testes automatizados,
linting, integração contínua e revisão de código como a superfície que torna a
saída do agente auditável e confiável, ao passo que a codificação por vibe trata
esses controles como opcionais, o que eleva o risco operacional e reduz a
responsabilização (*accountability*) em produção (ARXIV, 2025; FORRESTER, 2026).

Dados de mercado recentes sustentam a relevância do problema: relatórios de
analistas indicam que a maioria das organizações de desenvolvimento de software já
utiliza IA de forma ativa em algum ponto do ciclo de vida (FUTURUM GROUP, 2026;
FORRESTER, 2026), e fornecedores de plataforma relatam iniciativas de automação de
ponta a ponta do *software development lifecycle* (SDLC) apoiadas em agentes
(FUJITSU, 2026; MICROSOFT, 2026). Esse movimento de mercado, no entanto, expõe uma
lacuna conceitual: a difusão de ferramentas agênticas de codificação
(Claude Code, Cursor, GitHub Copilot, entre outras) sem que a arquitetura interna
que sustenta a autonomia desses sistemas seja amplamente compreendida por quem os
adota — a diferença entre "ter um LLM" e "ter um agente de codificação" é tratada,
na prática corporativa, como incidental, quando na verdade é estrutural
(MINDSTUDIO, 2026; AIMULTIPLE, 2026).

Um segundo eixo do problema de pesquisa concerne à tensão entre codificação
agêntica e práticas clássicas de engenharia, notadamente o TDD (*Test-Driven
Development*). A literatura reporta que agentes de IA geram código plausível em
segundos, mas "parecer plausível" e "de fato funcionar" são propriedades distintas:
sem *guardrails*, a saída do agente passa no *vibe check* mas falha em produção
(ARXIV, 2025). A resposta documentada pela comunidade técnica é reforçar, não
abandonar, o TDD — escrever o teste antes de qualquer implementação define o que é
"correto" antes que o agente gere uma linha de código, funcionando como camada de
controle estrutural externa ao próprio modelo (ARXIV, 2025; ARXIV, 2026).

## 1.2 Objetivo do Recorte

Este recorte investigativo tem por objetivo caracterizar (i) a transição conceitual
de *vibe coding* para *agentic coding* como mudança de paradigma de engenharia, e
(ii) o modelo arquitetural de quatro camadas — Tela, Harness, LLM e Tools — que a
literatura técnica converge em descrever como o substrato estrutural dessa
transição, com ênfase nas camadas Tela e Harness, responsáveis, respectivamente,
pela interface de supervisão humana (*intent preview*, *approval gates*, *hybrid
autonomy*, estimativa de "raio de impacto") e pelo runtime que transforma um modelo
de linguagem em um agente de codificação capaz (MINDSTUDIO, 2026; PILLITTERI,
2026; WAVESPEED, 2026).

## 1.3 Justificativa e Delimitação

A justificativa do recorte decorre da constatação, presente na literatura
consultada, de que a arquitetura de quatro camadas é tratada de forma dispersa —
fornecedores de harness (GITHUB, 2026; MICROSOFT, 2026), fabricantes de modelo
(ANTHROPIC, 2026) e analistas de mercado (FORRESTER, 2026; FUTURUM GROUP, 2026)
descrevem partes do mesmo fenômeno sob vocabulários distintos, sem uma síntese
única que relacione paradigma (vibe versus agentic), arquitetura (as quatro
camadas) e superfície de controle humano (a camada Tela). Este artigo delimita-se
aos capítulos 1 a 3 do dossiê-mãe que fundamenta a obra da qual deriva, não
abrangendo as camadas LLM e Tools em profundidade técnica de implementação — objeto
de recorte posterior — mas tratando-as na medida necessária para situar o papel das
camadas Tela e Harness na cadeia de decisão do agente (ANTHROPIC, 2026; AGENTA,
2026; BLAXEL, 2026; COMET, 2026; HARTENFELLER, 2026; IBM, 2026; PROMPTHUB, 2026;
RESEARCHGATE, 2026; ARTEZIO, 2026; WIKIPEDIA, 2026; HUMANLAYER, 2026; KONISHI,
2026; OWASP, 2026; ARXIV, 2024).

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
