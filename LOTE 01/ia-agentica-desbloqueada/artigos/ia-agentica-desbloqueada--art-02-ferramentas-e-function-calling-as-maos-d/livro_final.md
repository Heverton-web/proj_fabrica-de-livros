## 1. Introdução

Se o agent loop é o cérebro dos sistemas autônomos, as ferramentas e o planejamento são as mãos e a bússola: sem ferramentas, o agente fala sobre o mundo sem agir sobre ele; sem planejamento, o agente reage a cada passo sem visão de longo prazo (AMAZON, 2026; ANTHROPIC, 2024). Este artigo examina o estado da arte do function calling — o mecanismo de execução de ferramentas a partir de decisão do modelo — e do planejamento de tarefas com decomposição e re-planejamento (ORACLE, 2026; YAO, 2023).

O objetivo é duplo: descrever o contrato de ferramentas e o ciclo de execução com validação e observação estruturada, e analisar as abordagens de planejamento — intrínseco, plano explícito e re-planejamento — com os critérios de escolha pela incerteza da tarefa (ANTHROPIC, 2024; WANG, 2025). A motivação prática é a lacuna entre a literatura de agentes e a engenharia de produção: muitos sistemas falham não pelo modelo, mas pelas mãos e pela bússola (LANGCHAIN, 2025).

O artigo estrutura-se em quatro seções: introdução, metodologia, resultados e discussão, e conclusão — com foco em sistemas que integram ferramentas e planejamento no mesmo fluxo. A memória de longo prazo, recuperada seletivamente, é tratada como insumo do planejamento (LANGCHAIN, 2025; XI, 2023).

# Referências

ADIMULAM, A.; GUPTA, R.; KUMAR, S., 2026. *The Orchestration of Multi-Agent Systems: Architectures, Protocols, and Enterprise Adoption*. Disponível em: https://arxiv.org/html/2601.13671v1. Acesso em: 07 ago. 2026.

AMAZON WEB SERVICES (AWS), 2026. *Traditional agent architecture: perceive, reason, act*. AWS Prescriptive Guidance: Foundations of Agentic AI on AWS. Disponível em: https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-foundations/traditional-agents.html. Acesso em: 07 ago. 2026.

ANTHROPIC, 2024. *Building Effective Agents*. Disponível em: https://www.anthropic.com/engineering/building-effective-agents. Acesso em: 07 ago. 2026.

ANTHROPIC, 2026. *Demystifying Evals for AI Agents*. Disponível em: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents. Acesso em: 07 ago. 2026.

BRAINTRUST, 2026. *AI Gateway Comparison: The 6 Best Ranked (2026)*. Disponível em: https://www.braintrust.dev/articles/ai-gateway-comparison-2026. Acesso em: 07 ago. 2026.

CERBOS, 2026. *AI Agents, the Model Context Protocol, and the Future of Authorization Guardrails*. Disponível em: https://www.cerbos.dev/news/securing-ai-agents-model-context-protocol. Acesso em: 07 ago. 2026.

COALITION FOR SECURE AI (CoSAI), 2026. *Securing the AI Agent Revolution: A Practical Guide to Model Context Protocol Security*. Disponível em: https://www.coalitionforsecureai.org/securing-the-ai-agent-revolution-a-practical-guide-to-mcp-security/. Acesso em: 07 ago. 2026.

DIGITAL APPLIED, 2026. *State of AI Agents 2026: 200+ Data Points Compiled*. Disponível em: https://www.digitalapplied.com/blog/state-of-ai-agents-2026-200-data-points. Acesso em: 07 ago. 2026.

DORA / GOOGLE CLOUD, 2025. *DORA: State of AI-assisted Software Development 2025*. Disponível em: https://dora.dev/dora-report-2025/. Acesso em: 07 ago. 2026.

FIN.AI, 2026. *AI Agent ROI: Customer Support Returns*. Disponível em: https://fin.ai/blog/ai-agent-roi-customer-support. Acesso em: 07 ago. 2026.

GALILEO, 2026. *How to Build Human-in-the-Loop Oversight for Production AI Agents*. Disponível em: https://galileo.ai/blog/human-in-the-loop-agent-oversight. Acesso em: 07 ago. 2026.

GARTNER, 2025. *Gartner Predicts 40% of Enterprise Apps Will Feature Task-Specific AI Agents by 2026*. Disponível em: https://www.gartner.com/en/newsroom/press-releases/2025-08-26-gartner-predicts-40-percent-of-enterprise-apps-will-feature-task-specific-ai-agents-by-2026-up-from-less-than-5-percent-in-2025. Acesso em: 07 ago. 2026.

GOOGLE CLOUD, 2026. *Choose a Design Pattern for Your Agentic AI System*. Cloud Architecture Center. Disponível em: https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system. Acesso em: 07 ago. 2026.

GUO, Taicheng; et al., 2024. *Large Language Model based Multi-Agents: A Survey of Progress and Challenges*. IJCAI. Disponível em: https://arxiv.org/abs/2402.01680. Acesso em: 07 ago. 2026.

HONG, Sirui; et al., 2024. *MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework*. ICLR. Disponível em: https://arxiv.org/abs/2308.00352. Acesso em: 07 ago. 2026.

LANGCHAIN TEAM, 2025. *LangMem SDK for Agent Long-Term Memory*. Disponível em: https://www.langchain.com/blog/langmem-sdk-launch. Acesso em: 07 ago. 2026.

LANGCHAIN, 2026. *The Best AI Agent Frameworks in 2026*. Disponível em: https://www.langchain.com/resources/ai-agent-frameworks. Acesso em: 07 ago. 2026.

MICROSOFT AZURE ARCHITECTURE CENTER, 2026. *AI Agent Orchestration Patterns*. Disponível em: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns. Acesso em: 07 ago. 2026.

ORACLE DEVELOPERS, 2026. *What Is the AI Agent Loop? The Core Architecture Behind Autonomous AI Systems*. Disponível em: https://blogs.oracle.com/developers/what-is-the-ai-agent-loop-the-core-architecture-behind-autonomous-ai-systems. Acesso em: 07 ago. 2026.

WANG, Lei; et al., 2025. *A Survey on Large Language Model based Autonomous Agents*. Disponível em: https://arxiv.org/abs/2308.11432. Acesso em: 07 ago. 2026.

XI, Zhiheng; et al., 2023. *The Rise and Potential of Large Language Model Based Agents: A Survey*. Disponível em: https://arxiv.org/abs/2309.07864. Acesso em: 07 ago. 2026.

YAO, Shunyu; et al., 2023. *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR. Disponível em: https://arxiv.org/abs/2210.03629. Acesso em: 07 ago. 2026.

ZENITY, 2026. *What Is the Model Context Protocol? Full Guide*. Disponível em: https://zenity.io/academy/model-context-protocol-explained. Acesso em: 07 ago. 2026.
