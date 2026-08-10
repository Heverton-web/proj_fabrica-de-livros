# Dossiê de Pesquisa — AI Driven Development: Do Zero ao Deploy

> Obra v2 — Foco: **projeto prático do início ao fim** (público iniciante, tamanho XG).
> Motivo condutor sugerido: a jornada de uma "missão de construção" — do terreno baldio
> (zero) ao prédio em produção (deploy), com o engenheiro agêntico como mestre de obras.

## Conceitos-chave

- **AI Driven Development (AIDD)**: abordagem em que fluxos inteiros do ciclo de vida de software (requisitos, código, testes, revisão, deploy) são impulsionados e orquestrados por agentes de IA integrados ao repositório e aos pipelines. É o guarda-chuva metodológico e estratégico — não apenas "escrever código com IA". Fonte: DORA, 2025.
- **Vibe Coding**: termo cunhado por Andrej Karpathy (fev. 2025) — aceitar código gerado em bloco via linguagem natural, sem revisar linha a linha. Ideal para protótipos; esbarra no "muro de três meses" do débito técnico. Fonte: CONNELL, 2026.
- **Agentic Coding (Engenharia Agêntica)**: uso de agentes autônomos para tarefas complexas de ponta a ponta (refatoração, migração, testes), mantendo julgamento e responsabilidade finais com o humano (chef guiando sous-chef). Fonte: CONNELL, 2026.
- **Efeito Espelho (DORA)**: a IA não cria excelência sozinha — amplifica processos existentes. 90% dos profissionais usam IA, mas equipes caóticas veem instabilidade aumentar. Fonte: IT REVOLUTION, 2026.
- **Harness (agente harness)**: infraestrutura de software que envolve o modelo e o transforma em agente autônomo — loop perceive-reason-act, subagentes, skills, gestão de contexto. Fonte: DATABRICKS, 2026; BUI, 2026.
- **Context Engineering**: arte e ciência de arquitetar dinamicamente o ecossistema de informações (instruções, memória, histórico, ferramentas) que alimenta o modelo a cada passo — evolução da engenharia de prompt stateless. Fonte: SOURCEGRAPH, 2026; TASKADE, 2026.
- **Model Context Protocol (MCP)**: padrão aberto (Anthropic, 2024) que padroniza a comunicação cliente-servidor via JSON-RPC 2.0, expondo Resources, Prompts e Tools. Elimina integrações fragmentadas. Fonte: ANTHROPIC, 2024; MODEL CONTEXT PROTOCOL, 2026.
- **Tool Poisoning (TPA)**: vulnerabilidade em que servidores MCP maliciosos embutem instruções adversariais invisíveis nas descrições das ferramentas que o LLM lê, causando exfiltração de dados. Fonte: INVARIANT LABS, 2025; CLOUD SECURITY ALLIANCE, 2026.
- **CLAUDE.md / AGENTS.md**: arquivos de diretrizes persistentes lidos no início de cada sessão — manual de bordo do agente. AGENTS.md é padrão aberto (Agentic AI Foundation/Linux Foundation), agnóstico de ferramenta. Fonte: AUGMENT CODE, 2026; TERMDOCK, 2026.
- **Skills**: instruções procedurais modulares (SKILL.md) carregadas sob demanda — o agente lê apenas os resumos leves e injeta o detalhe quando a tarefa corresponde. Economiza tokens. Fonte: TERMDOCK, 2026.
- **SWE-bench / SWE-bench Pro / Terminal-Bench**: benchmarks que avaliam agentes em problemas reais de GitHub, tarefas long-horizon e operação em shell real. Líderes ainda <25% Pass@1 em Pro. Fonte: DENG et al., 2025; BIRJOB, 2026.
- **Spec-Driven Development**: desenvolvimento orientado a especificações vivas — especificação como contrato verificável entre humano e agente, mitigando alucinações estruturais em repositórios grandes. Fonte: AUGMENT CODE, 2026.

## Artigos Científicos e Papers

- HE, Kang; ROY, Kaushik. *SWE-Adept: An LLM-Based Agentic Framework for Deep Codebase Analysis and Structured Issue Resolution*. arXiv:2603.01327, 2026. Disponível em: https://arxiv.org/abs/2603.01327. Acesso em: 07 ago. 2026.
- WONG, Sherman et al. *Confucius Code Agent: Scalable Agent Scaffolding for Real-World Codebases*. arXiv:2512.10398, 2025. Disponível em: https://arxiv.org/abs/2512.10398. Acesso em: 07 ago. 2026.
- DENG, Xiang et al. *SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?* arXiv:2509.16941, 2025. Disponível em: https://arxiv.org/abs/2509.16941. Acesso em: 07 ago. 2026.
- TAWOSI, Vali et al. *ALMAS: an Autonomous LLM-based Multi-Agent Software Engineering Framework*. arXiv:2510.03463, 2025. Disponível em: https://arxiv.org/abs/2510.03463. Acesso em: 07 ago. 2026.
- JIN, Haolin et al. *From LLMs to LLM-based Agents for Software Engineering: A Survey of Current, Challenges and Future*. arXiv:2408.02479, 2024. Disponível em: https://arxiv.org/abs/2408.02479. Acesso em: 07 ago. 2026.
- BUI, Nghi D. Q. *Building AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned*. arXiv:2603.05344, 2026. Disponível em: https://arxiv.org/html/2603.05344v1. Acesso em: 07 ago. 2026.

## Estado da arte / ferramentas de referência

- **Claude Code (Anthropic)**: agente de terminal com alta precisão em refatorações em larga escala e compreensão de contexto em repositórios grandes. Fonte: SOFTJOURN, 2026.
- **Cursor & Windsurf**: IDEs AI-first para desenvolvimento agêntico fluido na interface de trabalho. Fonte: SOFTJOURN, 2026.
- **GitHub Copilot**: pioneiro, na Fortune 100, com revisão de PRs e geração de código; adoção voluntária de 81,4% no 1º dia na Microsoft. Fonte: CODIHAUS, 2026.
- **Codex / OpenAI Ecosystem**: base de múltiplos assistentes de backend com raciocínio avançado. Fonte: SOFTJOURN, 2026.
- **Arquitetura de 4 camadas**: (1) Tela/IDE, (2) Harness/orquestrador, (3) LLM com roteamento de modelos, (4) Tools/MCP/persistência. Fonte: BUI, 2026; DATABRICKS, 2026.
- **MCP Specification (2026-07-28)**: JSON-RPC 2.0, recursos sob demanda (lazy tool discovery), servidores desacoplados. Fonte: MODEL CONTEXT PROTOCOL, 2026.
- **CI para agentes / evals privados**: suíte interna de 20-50 tarefas históricas do próprio repositório; métrica real = taxa de alterações aceitas em PRs e custo de revisão humana. Fonte: EXPLAINX.AI, 2026.
- **Context rot / Lost in the Middle**: janelas longas não resolvem dados desorganizados — contexto precisa ser arquitetado. Fonte: SOURCEGRAPH, 2026.

## Casos de uso corporativos

- **Geração e scaffolding de boilerplate**: redução de até 46% do tempo em tarefas padronizadas (McKinsey). Fonte: VALUE ADD VC, 2026.
- **Diagnóstico de erros e debugging**: interpretação de logs complexos — um dos maiores ganhadores de tempo. Fonte: VALUE ADD VC, 2026.
- **Refatoração e migração de frameworks** em larga escala (React, Java). Fonte: VALUE ADD VC, 2026.
- **Testes unitários e documentação** automatizados a partir de especificação. Fonte: VALUE ADD VC, 2026.
- **Microsoft/GitHub**: 90%+ da Fortune 100 usa Copilot; aumento mensurável de PRs mescladas por semana. Fonte: CODIHAUS, 2026.
- **Google**: percentual expressivo de código interno assistido/gerado por IA, com rigorosas revisões de segurança. Fonte: VALUE ADD VC, 2026.
- **ROI**: 300-600% em 3 anos em empresas >1.000 devs; payback de 6-12 meses (DX). Fonte: UNBUILT LAB, 2026.
- **Code review autônomo**: CodeRabbit e agentes em GitHub Actions pré-analisam segurança/estilo antes do revisor humano. Fonte: VALUE ADD VC, 2026.

## Limitações e controvérsias

- **Efeito Espelho (DORA)**: IA amplifica processos bons e ruins; sem estrutura, aumenta instabilidade. Fonte: IT REVOLUTION, 2026.
- **Alucinação e débito técnico oculto**: código gerado por IA em brownfield pode introduzir dependências complexas; code churn em alta (GitClear). Fonte: MIT SLOAN, 2025.
- **Segurança**: código gerado por IA pode conter vulnerabilidades CWE em taxas superiores se não filtrado por SAST. Fonte: VALUE ADD VC, 2026.
- **Gargalo do code review**: volume de código gerado sobrecarrega revisores humanos sem automação. Fonte: VALUE ADD VC, 2026.
- **Custos ocultos de tokens**: gastos com tokens de IA corporativa escalando; falta de governança leva a abandono (Gartner). Fonte: GARTNER, 2026.
- **Benchmarks enganosos**: até 20% dos casos "resolvidos" em leaderboards públicos têm falhas semânticas ou ajuste de harness. Fonte: BIRJOB, 2026.
- **Contexto gerado por LLM degrada**: arquivos de contexto auto-gerados reduzem sucesso em até 3% e aumentam custos >20% (ETH Zurich). Fonte: HUß, 2026.

## Fontes brutas (para Nó 7 — Auditor de Rastreabilidade)

- ANTHROPIC. *Introducing the Model Context Protocol*. Disponível em: https://www.anthropic.com/news/model-context-protocol. Acesso em: 07 ago. 2026.
- AUGMENT CODE. *How to Build Your AGENTS.md (2026): The Context File That Makes AI Coding Agents Actually Work*. Disponível em: https://www.augmentcode.com/guides/how-to-build-agents-md. Acesso em: 07 ago. 2026.
- AUGMENT CODE. *Vibe Coding vs Spec-Driven Development (2026): When to Use Each*. Disponível em: https://www.augmentcode.com/guides/vibe-coding-vs-spec-driven-development. Acesso em: 07 ago. 2026.
- BIRJOB. *AI Coding Agent Benchmarks Beyond SWE-Bench in 2026: Terminal-Bench, Aider Polyglot, GAIA, and Why the Leaderboard Lies*. Disponível em: https://www.birjob.com/blog/agent-benchmarks-2026. Acesso em: 07 ago. 2026.
- BUI, Nghi D. Q. *Building AI Coding Agents for the Terminal*. Disponível em: https://arxiv.org/html/2603.05344v1. Acesso em: 07 ago. 2026.
- CLOUD SECURITY ALLIANCE. *Agentic MCP Security Best Practices Guide*. Disponível em: https://labs.cloudsecurityalliance.org/agentic/agentic-mcp-security-best-practices-v1/. Acesso em: 07 ago. 2026.
- CODIHAUS. *AI Developer Productivity Data: 2X Faster, 55% Speed Gain, Enterprise ROI Analysis*. Disponível em: https://codihaus.com/news/ai-developer-productivity-data-engineering-leaders. Acesso em: 07 ago. 2026.
- CONNELL, Andrew. *My Thoughts on Vibe Coding vs. Agentic Engineering*. Disponível em: https://www.andrewconnell.com/articles/vibe-coding-vs-agentic-engineering/. Acesso em: 07 ago. 2026.
- DATABRICKS. *What is an AI Agent Harness?* Disponível em: https://www.databricks.com/blog/ai-harness. Acesso em: 07 ago. 2026.
- DENG, Xiang et al. *SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?* Disponível em: https://arxiv.org/abs/2509.16941. Acesso em: 07 ago. 2026.
- DORA / GOOGLE CLOUD. *Publications and ROI of AI-assisted Software Development Report*. Disponível em: https://dora.dev/research/publications/. Acesso em: 07 ago. 2026.
- DX. *How to measure AI's impact on developer productivity*. Disponível em: https://getdx.com/blog/ai-measurement-hub/. Acesso em: 07 ago. 2026.
- EXPLAINX.AI. *AI Coding Agent Evals on Real Repos (2026)*. Disponível em: https://explainx.ai/blog/ai-coding-agent-evals-real-repos-2026. Acesso em: 07 ago. 2026.
- GARTNER. *Gartner Identifies the Top Strategic Technology Trends for 2026*. Disponível em: https://www.gartner.com/en/newsroom/press-releases/2025-10-20-gartner-identifies-the-top-strategic-technology-trends-for-2026. Acesso em: 07 ago. 2026.
- HE, Kang; ROY, Kaushik. *SWE-Adept: An LLM-Based Agentic Framework for Deep Codebase Analysis and Structured Issue Resolution*. Disponível em: https://arxiv.org/abs/2603.01327. Acesso em: 07 ago. 2026.
- HUß, Roland. *What Goes in AGENTS.md (and What Doesn't)*. Disponível em: https://ro14nd.de/what-goes-in-agents-md/. Acesso em: 07 ago. 2026.
- INVARIANT LABS. *MCP Security Notification: Tool Poisoning Attacks*. Disponível em: https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks. Acesso em: 07 ago. 2026.
- IT REVOLUTION. *AI's Mirror Effect: How the 2025 DORA Report Reveals Your Organization's True Capabilities*. Disponível em: https://itrevolution.com/articles/ais-mirror-effect-how-the-2025-dora-report-reveals-your-organizations-true-capabilities/. Acesso em: 07 ago. 2026.
- JIN, Haolin et al. *From LLMs to LLM-based Agents for Software Engineering: A Survey of Current, Challenges and Future*. Disponível em: https://arxiv.org/abs/2408.02479. Acesso em: 07 ago. 2026.
- MCKINSEY & COMPANY. *The State of AI: Global Survey*. Disponível em: https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai. Acesso em: 07 ago. 2026.
- MIT SLOAN MANAGEMENT REVIEW. ANDERSON, Edward; PARKER, Geoffrey; TAN, Burcu. *The Hidden Costs of Coding With Generative AI*. Disponível em: https://sloanreview.mit.edu/article/the-hidden-costs-of-coding-with-generative-ai/. Acesso em: 07 ago. 2026.
- MODEL CONTEXT PROTOCOL. *Specification (2026-07-28)*. Disponível em: https://modelcontextprotocol.io/specification/2026-07-28. Acesso em: 07 ago. 2026.
- PRINCETON UNIVERSITY. *SWE-bench Verified & Pro*. Disponível em: https://www.swebench.com. Acesso em: 07 ago. 2026.
- SOFTJOURN. *AI Software Development Statistics 2026: Adoption, Productivity, and Risk*. Disponível em: https://softjourn.com/insights/ai-software-dev-stats. Acesso em: 07 ago. 2026.
- SOURCEGRAPH. *Context Engineering: A Practical Guide for AI Agents (2026)*. Disponível em: https://sourcegraph.com/blog/context-engineering. Acesso em: 07 ago. 2026.
- TASKADE. *Context Engineering: What It Is + How to Do It (2026)*. Disponível em: https://www.taskade.com/blog/context-engineering. Acesso em: 07 ago. 2026.
- TAWOSI, Vali et al. *ALMAS: an Autonomous LLM-based Multi-Agent Software Engineering Framework*. Disponível em: https://arxiv.org/abs/2510.03463. Acesso em: 07 ago. 2026.
- TERMDOCK. *SKILL.md vs CLAUDE.md vs AGENTS.md Compared*. Disponível em: https://www.termdock.com/blog/skill-md-vs-claude-md-vs-agents-md. Acesso em: 07 ago. 2026.
- UNBUILT LAB. *AI Development ROI Measurement: Complete Platform Guide*. Disponível em: https://unbuiltlab.com/blog/ai-development-roi-measurement-complete-platform-guide.html. Acesso em: 07 ago. 2026.
- VALUE ADD VC. *AI Coding Productivity Study Data: What METR, McKinsey, and GitHub Found in 2026*. Disponível em: https://valueaddvc.com/blog/ai-coding-productivity-study-data-what-metr-mckinsey-and-github-actually-found-in-2026. Acesso em: 07 ago. 2026.
- WONG, Sherman et al. *Confucius Code Agent: Scalable Agent Scaffolding for Real-World Codebases*. Disponível em: https://arxiv.org/abs/2512.10398. Acesso em: 07 ago. 2026.
- ZIEMINSKI, Karo. *Context Engineering for Product Builders: The 2026 Operating Manual*. Disponível em: https://karozieminski.substack.com/p/context-engineering-product-builders-guide-2026. Acesso em: 07 ago. 2026.
