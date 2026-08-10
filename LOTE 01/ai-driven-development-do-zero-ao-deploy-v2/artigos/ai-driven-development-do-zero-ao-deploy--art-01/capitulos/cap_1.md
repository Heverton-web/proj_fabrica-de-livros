# 1 Introdução

## 1.1 Contextualização e Problema de Pesquisa

Entre 2024 e 2026 a engenharia de software atravessa uma mudança estrutural que a literatura técnica compara à adoção do DevOps e do Agile: modelos de linguagem de grande porte deixam de operar como autocomplete avançado — paradigma no qual o desenvolvedor permanece integralmente no loop, revisando cada sugestão em modo conversacional — para atuar como agentes autônomos capazes de planejar, executar, testar e iterar tarefas inteiras do ciclo de engenharia sob supervisão mínima (CONNELL, 2026; AUGMENT CODE, 2026). A distinção entre os dois paradigmas não é apenas de grau de autonomia, mas de arquitetura de controle: a codificação agêntica trata testes automatizados, linting, integração contínua e revisão de código como a superfície que torna a saída do agente auditável e confiável, ao passo que a codificação por vibe trata esses controles como opcionais, o que eleva o risco operacional e reduz a responsabilização em produção (AUGMENT CODE, 2026; CONNELL, 2026; BIRJOB, 2026).

Dados de mercado sustentam a relevância do problema: levantamentos indicam que a maioria das organizações de desenvolvimento já utiliza IA de forma ativa em algum ponto do ciclo de vida do software, e analistas posicionam a inteligência artificial agêntica entre as tendências tecnológicas estratégicas da década (GARTNER, 2026; SOFTJOURN, 2026; MCKINSEY, 2026). Esse movimento, no entanto, expõe uma lacuna conceitual: a difusão de ferramentas agênticas de codificação sem que a arquitetura interna que sustenta a autonomia desses sistemas seja amplamente compreendida por quem os adota. A diferença entre "ter um LLM" e "ter um agente de codificação" é tratada, na prática corporativa, como incidental, quando na verdade é estrutural (DATABRICKS, 2026; BUI, 2026; TAWOSI, 2025).

## 1.2 Objetivo do Recorte

O presente artigo tem como objetivo examinar, em perspectiva investigativa documental, dois temas centrais do livro-mãe *AI Driven Development: Do Zero ao Deploy*: (i) a definição precisa do que é — e do que não é — o desenvolvimento dirigido por IA, e (ii) o modelo arquitetural de quatro camadas — Tela, Harness, LLM e Tools — que a literatura técnica converge em descrever como o substrato dessa transição (BUI, 2026; DATABRICKS, 2026; JIN, 2024). Para isso, o recorte abrange também a preparação do ambiente de trabalho, o primeiro diálogo entre humano e agente, a engenharia de contexto e a autoria de arquivos de instrução como CLAUDE.md e AGENTS.md, entendidos como a instanciação prática das camadas (SOURCEGRAPH, 2026; TASKADE, 2026; TERMDOCK, 2026).

## 1.3 Justificativa e Delimitação

A justificativa decorre de duas observações. Primeiro, a adoção corporativa de ferramentas agênticas vem crescendo mais rápido do que a compreensão dos mecanismos que as tornam confiáveis, produzindo decisões de investimento baseadas em demonstrações superficiais de capacidade (CODIHAUS, 2026; VALUE ADD VC, 2026). Segundo, a literatura recente demonstra que a produtividade percebida não se traduz automaticamente em qualidade entregue: métricas de ciclos de desenvolvimento indicam ganhos de velocidade, mas relatórios setoriais alertam para custos ocultos de revisão e correção (DORA, 2026; MIT SLOAN MANAGEMENT REVIEW, 2026; DX, 2026). O recorte limita-se a fontes documentais públicas — relatórios de analistas, documentação oficial de plataformas e artigos de repositórios científicos — publicadas ou atualizadas entre 2024 e 2026, sem coleta primária de dados (UNBUILT LAB, 2026).

## 1.4 Síntese Parcial

Em síntese, o problema investigado situa-se na interseção entre três correntes: a corrente da produtividade (estudos de adoção e ROI), a corrente da arquitetura (harness, camadas e protocolos) e a corrente da governança (riscos de segurança e responsabilização) (INVARIANT LABS, 2026; CLOUD SECURITY ALLIANCE, 2026). A compreensão da arquitetura de quatro camadas é condição necessária para avaliar tanto o potencial quanto os riscos da adoção (HE, 2026; WONG, 2025). A seção seguinte descreve o procedimento metodológico adotado para recuperar e sintetizar as fontes que sustentam a análise das camadas (DENG, 2025; PRINCETON UNIVERSITY, 2026; EXPLAINX, 2026).

# Referências

AUGMENT CODE. *Vibe Coding vs Spec-Driven Development (2026): When to Use Each*. 2026. Disponível em: https://www.augmentcode.com/guides/vibe-coding-vs-spec-driven-development. Acesso em: 07 ago. 2026.

BIRJOB. *AI Coding Agent Benchmarks Beyond SWE-Bench in 2026: Terminal-Bench, Aider Polyglot, GAIA, and Why the Leaderboard Lies*. 2026. Disponível em: https://www.birjob.com/blog/agent-benchmarks-2026. Acesso em: 07 ago. 2026.

BUI, Nghi D. Q. *Building AI Coding Agents for the Terminal*. 2026. Disponível em: https://arxiv.org/html/2603.05344v1. Acesso em: 07 ago. 2026.

CLOUD SECURITY ALLIANCE. *Agentic MCP Security Best Practices Guide*. 2026. Disponível em: https://labs.cloudsecurityalliance.org/agentic/agentic-mcp-security-best-practices-v1/. Acesso em: 07 ago. 2026.

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

SOURCEGRAPH. *Context Engineering: A Practical Guide for AI Agents (2026)*. 2026. Disponível em: https://sourcegraph.com/blog/context-engineering. Acesso em: 07 ago. 2026.

TASKADE. *Context Engineering: What It Is + How to Do It (2026)*. 2026. Disponível em: https://www.taskade.com/blog/context-engineering. Acesso em: 07 ago. 2026.

TAWOSI, Vali et al. *ALMAS: an Autonomous LLM-based Multi-Agent Software Engineering Framework*. 2025. Disponível em: https://arxiv.org/abs/2510.03463. Acesso em: 07 ago. 2026.

TERMDOCK. *SKILL.md vs CLAUDE.md vs AGENTS.md Compared*. 2026. Disponível em: https://www.termdock.com/blog/skill-md-vs-claude-md-vs-agents-md. Acesso em: 07 ago. 2026.

UNBUILT LAB. *AI Development ROI Measurement: Complete Platform Guide*. 2026. Disponível em: https://unbuiltlab.com/blog/ai-development-roi-measurement-complete-platform-guide.html. Acesso em: 07 ago. 2026.

VALUE ADD VC. *AI Coding Productivity Study Data: What METR, McKinsey, and GitHub Found in 2026*. 2026. Disponível em: https://valueaddvc.com/blog/ai-coding-productivity-study-data-what-metr-mckinsey-and-github-actually-found-in-2026. Acesso em: 07 ago. 2026.

WONG, Sherman et al. *Confucius Code Agent: Scalable Agent Scaffolding for Real-World Codebases*. 2025. Disponível em: https://arxiv.org/abs/2512.10398. Acesso em: 07 ago. 2026.
