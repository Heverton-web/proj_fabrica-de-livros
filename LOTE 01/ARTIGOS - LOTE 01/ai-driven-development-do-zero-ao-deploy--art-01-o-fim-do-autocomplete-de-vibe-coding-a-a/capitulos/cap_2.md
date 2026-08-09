# 2 Metodologia

## 2.1 Natureza do Recorte

Este artigo constitui um recorte investigativo de natureza documental, derivado de
um dossiê de pesquisa técnica mais amplo, previamente minerado e indexado para a
obra "AI Driven Development: Do Zero ao Deploy". Não se trata de pesquisa empírica
com coleta primária de dados — não há experimento controlado, estudo de caso único
nem levantamento com participantes — mas de análise qualitativa de fontes
secundárias já reunidas: documentação oficial de fornecedores (ANTHROPIC, 2026;
GITHUB, 2026; MICROSOFT, 2026), preprints acadêmicos (ARXIV, 2024; ARXIV, 2025;
ARXIV, 2026), relatórios de analistas de mercado (FORRESTER, 2026; FUTURUM GROUP,
2026) e material técnico de blogs especializados (MINDSTUDIO, 2026; AIMULTIPLE,
2026; WAVESPEED, 2026; PILLITTERI, 2026). Essa delimitação metodológica é
deliberada: o objetivo do recorte é sintetizar e relacionar achados já
disponíveis, não gerar dado novo.

## 2.2 Procedimento de Reaproveitamento do Dossiê

O dossiê-mãe foi indexado em blocos temáticos por meio de um mecanismo de
recuperação por relevância (TF-IDF), permitindo consulta seletiva por termos em
vez de carregamento integral do corpus. Para este recorte, a consulta priorizou os
blocos correspondentes aos capítulos 1, 2 e 3 do sumário macro do livro-mãe —
respectivamente "Fundamentos de AI Driven Development", "Arquitetura em 4 Camadas:
Tela, Harness, LLM, Tools" e material correlato sobre configuração prática de
harness. Nenhuma varredura web adicional foi realizada: o critério metodológico
central é que toda afirmação factual do artigo remonta a um bloco já presente no
dossiê-mãe, nunca a conhecimento não rastreável.

## 2.3 Critério de Seleção das Fontes

Três critérios guiaram a seleção dos blocos e das referências citadas: (i)
pertinência direta a um dos três pilares do recorte — a transição vibe-para-agentic
(ARXIV, 2025), a arquitetura de quatro camadas (MINDSTUDIO, 2026; PILLITTERI, 2026)
e a relação entre a camada Tela (supervisão humana) e a camada Harness (runtime do
agente) (WAVESPEED, 2026; ANTHROPIC, 2026); (ii) atualidade, com preferência por
fontes de 2025-2026 e inclusão de preprints anteriores apenas quando descrevem
fundamentos ainda vigentes na literatura mais recente (ARXIV, 2024); e (iii)
triangulação, isto é, preferência por afirmações corroboradas por mais de uma
fonte independente — por exemplo, a caracterização da camada Harness como
intermediária entre interface e modelo aparece tanto em material de fornecedor de
IDE (GITHUB, 2026) quanto em análise comparativa de mercado (AIMULTIPLE, 2026;
WAVESPEED, 2026) e em conteúdo técnico especializado (MINDSTUDIO, 2026;
PILLITTERI, 2026).

## 2.4 Construção Textual e Citação

A redação seguiu o framework ACAD (Contextualização, Referencial Teórico,
Análise/Desenvolvimento, Síntese Parcial) dentro de cada seção IMRaD, com citação
autor-data (NBR 10520) para toda afirmação factual, métrica ou definição técnica
extraída do dossiê. Não há, portanto, um "método experimental" a relatar no sentido
das ciências naturais — o objeto deste artigo é uma síntese analítica de literatura
técnica e de mercado sobre arquitetura de agentes de codificação, e a
"metodologia" descrita aqui é o procedimento editorial-documental que sustenta essa
síntese, incluindo o uso de fontes como FUJITSU (2026), RESEARCHGATE (2026),
ARTEZIO (2026), IBM (2026), BLAXEL (2026), AGENTA (2026), COMET (2026), PROMPTHUB
(2026), HARTENFELLER (2026), HUMANLAYER (2026), KONISHI (2026), WIKIPEDIA (2026) e
OWASP (2026) para compor o quadro de referência de suporte às três seções restantes
deste artigo.

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
