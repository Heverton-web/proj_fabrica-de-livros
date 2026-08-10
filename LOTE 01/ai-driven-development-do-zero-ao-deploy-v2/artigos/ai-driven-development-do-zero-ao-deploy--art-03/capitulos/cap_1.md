# 1 Introdução

## 1.1 Contextualização e Problema de Pesquisa

A adoção de agentes de IA na engenharia de software atingiu escala corporativa, e com ela emergiu a questão central da governança: como delegar execução autônoma sem perder o controle sobre qualidade, segurança e custo (GARTNER, 2026) (MCKINSEY, 2026). A literatura recente é convergente ao afirmar que a confiabilidade da saída do agente depende menos do modelo e mais dos controles externos que o cercam — hooks, permissões, testes, revisão e métricas (DATABRICKS, 2026) (BUI, 2026). Esse conjunto forma o que se convencionou chamar de governança agêntica (JIN, 2024) (TAWOSI, 2025).

O problema de pesquisa decorre da observação de que a produtividade percebida com agentes nem sempre se converte em qualidade entregue: relatórios setoriais documentam custos ocultos de revisão, correção e dívida técnica quando a verificação é negligenciada (MIT SLOAN MANAGEMENT REVIEW, 2026) (DORA, 2026) (DX, 2026). Paralelamente, a evidência de benchmarks indica que a avaliação adequada de agentes é condição para decisões de adoção informadas (DENG, 2025) (PRINCETON UNIVERSITY, 2026) (BIRJOB, 2026).

## 1.2 Objetivo do Recorte

Este artigo examina, em perspectiva documental, o ciclo de governança e entrega do desenvolvimento dirigido por IA: hooks e regras de segurança, testes dirigidos por IA, revisão de código autônoma, economia de tokens, build e CI/CD, deploy em nuvem, monitoramento e iteração, e a formação do engenheiro do futuro (EXPLAINX, 2026) (HE, 2026). O recorte deriva dos capítulos 13 a 20 da obra-mãe *AI Driven Development: Do Zero ao Deploy* (CONNELL, 2026) (WONG, 2025).

## 1.3 Justificativa e Delimitação

A justificativa é dupla. Primeiro, a governança é o fator que distingue experimentos de produção: sem portões objetivos, a autonomia do agente amplifica tanto acertos quanto erros (INVARIANT LABS, 2026) (CODIHAUS, 2026). Segundo, o custo de operação — tokens, infraestrutura, revisão — tornou-se variável de decisão e não apenas detalhe operacional (VALUE ADD VC, 2026) (SOFTJOURN, 2026). O recorte limita-se a fontes documentais públicas de 2024 a 2026 (DORA, 2026) (DX, 2026).

## 1.4 Síntese Parcial

Em síntese, o argumento é que entregar software com IA em produção exige um sistema de controles: hooks que bloqueiam, testes que provam, revisão que audita, métricas que medem e pipelines que tornam o processo reproduzível (HE, 2026) (EXPLAINX, 2026). A seção seguinte descreve o método de recuperação e síntese das fontes (BUI, 2026).

# Referências

BIRJOB. *AI Coding Agent Benchmarks Beyond SWE-Bench in 2026: Terminal-Bench, Aider Polyglot, GAIA, and Why the Leaderboard Lies*. 2026. Disponível em: https://www.birjob.com/blog/agent-benchmarks-2026. Acesso em: 07 ago. 2026.

BUI, Nghi D. Q. *Building AI Coding Agents for the Terminal*. 2026. Disponível em: https://arxiv.org/html/2603.05344v1. Acesso em: 07 ago. 2026.

CODIHAUS. *AI Developer Productivity Data: 2X Faster, 55% Speed Gain, Enterprise ROI Analysis*. 2026. Disponível em: https://codihaus.com/news/ai-developer-productivity-data-engineering-leaders. Acesso em: 07 ago. 2026.

CONNELL, Andrew. *My Thoughts on Vibe Coding vs. Agentic Engineering*. 2026. Disponível em: https://www.andrewconnell.com/articles/vibe-coding-vs-agentic-engineering/. Acesso em: 07 ago. 2026.

DATABRICKS. *What is an AI Agent Harness?* 2026. Disponível em: https://www.databricks.com/blog/ai-harness. Acesso em: 07 ago. 2026.

DENG, Xiang et al. *SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?* 2025. Disponível em: https://arxiv.org/abs/2509.16941. Acesso em: 07 ago. 2026.

DORA / GOOGLE CLOUD. *Publications and ROI of AI-assisted Software Development Report*. 2026. Disponível em: https://dora.dev/research/publications/. Acesso em: 07 ago. 2026.

DX. *How to measure AI's impact on developer productivity*. 2026. Disponível em: https://getdx.com/blog/ai-measurement-hub/. Acesso em: 07 ago. 2026.

EXPLAINX.AI. *AI Coding Agent Evals on Real Repos (2026)*. 2026. Disponível em: https://explainx.ai/blog/ai-coding-agent-evals-real-repos-2026. Acesso em: 07 ago. 2026.

GARTNER. *Gartner Identifies the Top Strategic Technology Trends for 2026*. 2026. Disponível em: https://www.gartner.com/en/newsroom/press-releases/2025-10-20-gartner-identifies-the-top-strategic-technology-trends-for-2026. Acesso em: 07 ago. 2026.

HE, Kang; ROY, Kaushik. *SWE-Adept: An LLM-Based Agentic Framework for Deep Codebase Analysis and Structured Issue Resolution*. 2026. Disponível em: https://arxiv.org/abs/2603.01327. Acesso em: 07 ago. 2026.

INVARIANT LABS. *MCP Security Notification: Tool Poisoning Attacks*. 2026. Disponível em: https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks. Acesso em: 07 ago. 2026.

JIN, Haolin et al. *From LLMs to LLM-based Agents for Software Engineering: A Survey of Current, Challenges and Future*. 2024. Disponível em: https://arxiv.org/abs/2408.02479. Acesso em: 07 ago. 2026.

MCKINSEY & COMPANY. *The State of AI: Global Survey*. 2026. Disponível em: https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai. Acesso em: 07 ago. 2026.

MIT SLOAN MANAGEMENT REVIEW. ANDERSON, Edward; PARKER, Geoffrey; TAN, Burcu. *The Hidden Costs of Coding With Generative AI*. 2026. Disponível em: https://sloanreview.mit.edu/article/the-hidden-costs-of-coding-with-generative-ai/. Acesso em: 07 ago. 2026.

PRINCETON UNIVERSITY. *SWE-bench Verified & Pro*. 2026. Disponível em: https://www.swebench.com. Acesso em: 07 ago. 2026.

SOFTJOURN. *AI Software Development Statistics 2026: Adoption, Productivity, and Risk*. 2026. Disponível em: https://softjourn.com/insights/ai-software-dev-stats. Acesso em: 07 ago. 2026.

TAWOSI, Vali et al. *ALMAS: an Autonomous LLM-based Multi-Agent Software Engineering Framework*. 2025. Disponível em: https://arxiv.org/abs/2510.03463. Acesso em: 07 ago. 2026.

VALUE ADD VC. *AI Coding Productivity Study Data: What METR, McKinsey, and GitHub Found in 2026*. 2026. Disponível em: https://valueaddvc.com/blog/ai-coding-productivity-study-data-what-metr-mckinsey-and-github-actually-found-in-2026. Acesso em: 07 ago. 2026.

WONG, Sherman et al. *Confucius Code Agent: Scalable Agent Scaffolding for Real-World Codebases*. 2025. Disponível em: https://arxiv.org/abs/2512.10398. Acesso em: 07 ago. 2026.
