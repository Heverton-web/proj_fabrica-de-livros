# 1 Introdução

## 1.1 Contextualização e Problema de Pesquisa

O desenvolvimento dirigido por IA transfere ao agente uma parcela crescente do trabalho de engenharia, mas a qualidade do resultado depende diretamente da qualidade da especificação que antecede o código (CONNELL, 2026) (AUGMENT CODE, 2026). A literatura recente demonstra que agentes produzem resultados significativamente melhores quando recebem modelos de domínio explícitos, regras de negócio documentadas e critérios de aceite verificáveis antes da primeira linha de código (BUI, 2026) (SOURCEGRAPH, 2026). Esse achado desloca o centro de gravidade do ofício: especificar bem passa a ser tão importante quanto codar bem (DATABRICKS, 2026) (JIN, 2024).

O problema de pesquisa decorre da lacuna entre a promessa das ferramentas agênticas e a prática observada. Organizações que adotam agentes sem antes modelar o domínio relatam retrabalho, ambiguidade e entregas divergentes da intenção do negócio (CODIHAUS, 2026) (DX, 2026). Em contraste, equipes que tratam a especificação como artefato de primeira classe — glossário, regras de negócio, mapa de domínio — conseguem delegar implementação com confiança (TERMDOCK, 2026) (TASKADE, 2026).

## 1.2 Objetivo do Recorte

Este artigo examina, em perspectiva documental, o conjunto de práticas que viabilizam a construção guiada por IA a partir do domínio: modelagem do domínio antes de codar, geração do esqueleto do projeto, uso de skills reutilizáveis, conexão do agente ao mundo real por MCP, construção de ferramentas próprias e orquestração de subagentes (MODEL CONTEXT PROTOCOL, 2026) (INVARIANT LABS, 2026). O recorte deriva dos capítulos 7 a 12 da obra-mãe *AI Driven Development: Do Zero ao Deploy* e se apoia exclusivamente em fontes documentais públicas (WONG, 2025) (TAWOSI, 2025).

## 1.3 Justificativa e Delimitação

A justificativa é dupla. Primeiro, a capacidade de um agente está limitada pelo vocabulário e pelas restrições que o projeto lhe fornece: sem modelo de domínio, o agente improvisa nomes, regras e fronteiras (SOURCEGRAPH, 2026) (ZIEMINSKI, 2026). Segundo, o ecossistema de extensão — skills, servidores MCP e ferramentas próprias — cresceu a ponto de exigir critérios objetivos de escolha e de segurança (INVARIANT LABS, 2026) (MODEL CONTEXT PROTOCOL, 2026). O recorte limita-se a fontes de 2024 a 2026, sem coleta primária de dados (DENG, 2025) (PRINCETON UNIVERSITY, 2026).

## 1.4 Síntese Parcial

Em síntese, o argumento a desenvolver é que a construção agêntica madura combina disciplina de especificação com curadoria de ferramentas: o domínio modelado fornece a fundação; skills, MCP e subagentes fornecem a capacidade (HE, 2026) (EXPLAINX, 2026). A seção seguinte descreve o método de recuperação e síntese das fontes (DORA, 2026).

# Referências

AUGMENT CODE. *How to Build Your AGENTS.md (2026): The Context File That Makes AI Coding Agents Actually Work*. 2026. Disponível em: https://www.augmentcode.com/guides/how-to-build-agents-md. Acesso em: 07 ago. 2026.

BUI, Nghi D. Q. *Building AI Coding Agents for the Terminal*. 2026. Disponível em: https://arxiv.org/html/2603.05344v1. Acesso em: 07 ago. 2026.

CODIHAUS. *AI Developer Productivity Data: 2X Faster, 55% Speed Gain, Enterprise ROI Analysis*. 2026. Disponível em: https://codihaus.com/news/ai-developer-productivity-data-engineering-leaders. Acesso em: 07 ago. 2026.

CONNELL, Andrew. *My Thoughts on Vibe Coding vs. Agentic Engineering*. 2026. Disponível em: https://www.andrewconnell.com/articles/vibe-coding-vs-agentic-engineering/. Acesso em: 07 ago. 2026.

DATABRICKS. *What is an AI Agent Harness?* 2026. Disponível em: https://www.databricks.com/blog/ai-harness. Acesso em: 07 ago. 2026.

DENG, Xiang et al. *SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?* 2025. Disponível em: https://arxiv.org/abs/2509.16941. Acesso em: 07 ago. 2026.

DORA / GOOGLE CLOUD. *Publications and ROI of AI-assisted Software Development Report*. 2026. Disponível em: https://dora.dev/research/publications/. Acesso em: 07 ago. 2026.

DX. *How to measure AI's impact on developer productivity*. 2026. Disponível em: https://getdx.com/blog/ai-measurement-hub/. Acesso em: 07 ago. 2026.

EXPLAINX.AI. *AI Coding Agent Evals on Real Repos (2026)*. 2026. Disponível em: https://explainx.ai/blog/ai-coding-agent-evals-real-repos-2026. Acesso em: 07 ago. 2026.

HE, Kang; ROY, Kaushik. *SWE-Adept: An LLM-Based Agentic Framework for Deep Codebase Analysis and Structured Issue Resolution*. 2026. Disponível em: https://arxiv.org/abs/2603.01327. Acesso em: 07 ago. 2026.

INVARIANT LABS. *MCP Security Notification: Tool Poisoning Attacks*. 2026. Disponível em: https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks. Acesso em: 07 ago. 2026.

JIN, Haolin et al. *From LLMs to LLM-based Agents for Software Engineering: A Survey of Current, Challenges and Future*. 2024. Disponível em: https://arxiv.org/abs/2408.02479. Acesso em: 07 ago. 2026.

MODEL CONTEXT PROTOCOL. *Specification (2026-07-28)*. 2026. Disponível em: https://modelcontextprotocol.io/specification/2026-07-28. Acesso em: 07 ago. 2026.

PRINCETON UNIVERSITY. *SWE-bench Verified & Pro*. 2026. Disponível em: https://www.swebench.com. Acesso em: 07 ago. 2026.

SOURCEGRAPH. *Context Engineering: A Practical Guide for AI Agents (2026)*. 2026. Disponível em: https://sourcegraph.com/blog/context-engineering. Acesso em: 07 ago. 2026.

TASKADE. *Context Engineering: What It Is + How to Do It (2026)*. 2026. Disponível em: https://www.taskade.com/blog/context-engineering. Acesso em: 07 ago. 2026.

TAWOSI, Vali et al. *ALMAS: an Autonomous LLM-based Multi-Agent Software Engineering Framework*. 2025. Disponível em: https://arxiv.org/abs/2510.03463. Acesso em: 07 ago. 2026.

TERMDOCK. *SKILL.md vs CLAUDE.md vs AGENTS.md Compared*. 2026. Disponível em: https://www.termdock.com/blog/skill-md-vs-claude-md-vs-agents-md. Acesso em: 07 ago. 2026.

WONG, Sherman et al. *Confucius Code Agent: Scalable Agent Scaffolding for Real-World Codebases*. 2025. Disponível em: https://arxiv.org/abs/2512.10398. Acesso em: 07 ago. 2026.

ZIEMINSKI, Karo. *Context Engineering for Product Builders: The 2026 Operating Manual*. 2026. Disponível em: https://karozieminski.substack.com/p/context-engineering-product-builders-guide-2026. Acesso em: 07 ago. 2026.
