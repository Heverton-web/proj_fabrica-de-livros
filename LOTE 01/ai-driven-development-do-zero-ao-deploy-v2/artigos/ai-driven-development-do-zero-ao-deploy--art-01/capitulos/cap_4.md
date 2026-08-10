# 4 Conclusão

## 4.1 Retomada do Argumento Central

O recorte investigativo permitiu sustentar a tese central do livro-mãe em três proposições. Primeira: AI Driven Development é um paradigma de engenharia distinto do *vibe coding*, definido não pela presença de um modelo de linguagem, mas pela existência de camadas de verificação e governança externas ao modelo (AUGMENT CODE, 2026; CONNELL, 2026). Segunda: a arquitetura de quatro camadas — Tela, Harness, LLM e Tools — tem no Harness o seu núcleo de confiabilidade, pois é nessa camada que permissões, contexto e trilhas de auditoria são aplicados de forma determinística (DATABRICKS, 2026; BUI, 2026; JIN et al., 2024). Terceira: a camada de Tools, ponto de contato com o mundo externo, concentra os riscos mais severos, como o envenenamento de ferramentas, cuja mitigação depende de governança, não de capacidade de raciocínio do modelo (INVARIANT LABS, 2026; CLOUD SECURITY ALLIANCE, 2026).

## 4.2 Implicações para a Adoção

As implicações práticas decorrem diretamente dos achados. Organizações que adotam ferramentas agênticas de codificação devem avaliar a robustez do harness que envolve o modelo — permissões explícitas, aprovações em pontos de alto impacto, revisão determinística — antes de considerar a capacidade de raciocínio como critério isolado de escolha (HE, 2026; WONG et al., 2025). Da mesma forma, a medição de produtividade deve separar velocidade de tarefa de custo total: ganhos de 2x em tarefas isoladas convivem com custos ocultos de revisão e dívida técnica (CODIHAUS, 2026; MIT SLOAN MANAGEMENT REVIEW, 2026; DORA / GOOGLE CLOUD, 2026). A engenharia de contexto e a autoria deliberada de arquivos de instrução, como CLAUDE.md e AGENTS.md, aparecem como práticas de baixo custo e alto retorno, pois condicionam o agente antes da primeira linha de código (SOURCEGRAPH, 2026; TASKADE, 2026; TERMDOCK, 2026; AUGMENT CODE, 2026).

## 4.3 Limitações e Trabalhos Futuros

O recorte limita-se a fontes documentais públicas; não foram coletados dados primários de adoção em organizações específicas (UNBUILT LAB, 2026; DX, 2026). Estudos futuros podem investigar, com evidência primária, a relação entre maturidade de governança do harness e taxas de incidentes em produção, bem como a evolução dos benchmarks de avaliação de agentes (BIRJOB, 2026; PRINCETON UNIVERSITY, 2026; DENG et al., 2025; EXPLAINX.AI, 2026). A expansão do recorte para os temas de testes dirigidos por IA, revisão autônoma e CI/CD com agentes constitui desdobramento natural da agenda de pesquisa (TAWOSI et al., 2025; GARTNER, 2026; MCKINSEY & COMPANY, 2026).

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
