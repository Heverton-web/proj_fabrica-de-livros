# 3 Resultados e Discussão

## 3.1 AIDD: Definição, Fronteiras e Evidência de Adoção

Os resultados da análise documental confirmam que AI Driven Development (AIDD) designa uma modalidade de engenharia de software em que agentes de IA participam ativamente de múltiplas etapas do ciclo de vida — especificação, planejamento, implementação, teste e revisão — operando a partir de intenções expressas em linguagem natural e de restrições explícitas codificadas no projeto (BUI, 2026; CONNELL, 2026). A literatura distingue o AIDD do *vibe coding* por uma diferença estrutural: no primeiro, a saída do agente passa por camadas de verificação determinística e governança; no segundo, a saída é aceita pela aparência de plausibilidade (AUGMENT CODE, 2026; BIRJOB, 2026). Essa distinção aparece também nos dados de adoção: relatórios setoriais apontam crescimento do uso de agentes em equipes de engenharia, com ênfase na correlação entre maturidade de prática e qualidade percebida (GARTNER, 2026; SOFTJOURN, 2026; MCKINSEY & COMPANY, 2026).

## 3.2 A Arquitetura de Quatro Camadas: Tela, Harness, LLM e Tools

O segundo resultado diz respeito à arquitetura. A análise converge na descrição de quatro camadas interconectadas: a camada de Tela (interface entre humano e sistema), a camada de Harness (orquestração, permissões e gerenciamento de contexto), a camada de LLM (raciocínio) e a camada de Tools (efeito real no mundo) (DATABRICKS, 2026; BUI, 2026). O Harness emerge como o componente crítico: é ele que transforma um modelo de linguagem em um agente operacional, aplicando permissões, gerenciando o contexto e registrando trilhas de auditoria (JIN et al., 2024; HE, 2026; WONG et al., 2025). A camada de Tools, por sua vez, é o ponto de contato com sistemas externos, conectada crescentemente por protocolos abertos como o Model Context Protocol (AUGMENT CODE, 2026; CLOUD SECURITY ALLIANCE, 2026).

## 3.3 Risco e Governança na Camada de Tools

O terceiro resultado é o mapeamento de riscos. A revisão documental identificou ameaças concretas na camada de ferramentas, destacando-se o envenenamento de ferramentas (*tool poisoning*) — descrições de ferramentas maliciosas ou enganosas capazes de induzir o agente a ações indevidas (INVARIANT LABS, 2026; CLOUD SECURITY ALLIANCE, 2026). Esses riscos reforçam a tese de que a confiabilidade do AIDD depende menos da capacidade bruta do modelo e mais da robustez do harness que o envolve — permissões determinísticas, aprovações explícitas e revisão humana em pontos de alto impacto (DATABRICKS, 2026). A produtividade, medida em velocidade de entrega, não deve ser confundida com redução de custo total: estudos apontam ganhos de 2x em tarefas isoladas, mas também custos ocultos de revisão, correção e dívida técnica quando a verificação é negligenciada (CODIHAUS, 2026; MIT SLOAN MANAGEMENT REVIEW, 2026; VALUE ADD VC, 2026; DORA / GOOGLE CLOUD, 2026).

## 3.4 Síntese Parcial

Em síntese, os resultados articulam três achados: (i) o AIDD é um paradigma distinto do *vibe coding*, caracterizado por verificações externas ao modelo; (ii) a arquitetura de quatro camadas tem no Harness o seu núcleo de confiabilidade; e (iii) a camada de Tools concentra os principais riscos de segurança, mitigáveis por governança determinística (EXPLAINX.AI, 2026; TAWOSI et al., 2025). A seção seguinte conclui o recorte retomando o argumento central e suas implicações para a adoção corporativa (PRINCETON UNIVERSITY, 2026; DENG et al., 2025).

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
