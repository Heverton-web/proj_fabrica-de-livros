# Dossiê Técnico — Harness Engineering: orquestrando loops autônomos em produção

> Livro 9 · Parte III — A Camada de Harness · Tamanho G · 20 refs/capítulo
> Fonte de matéria-prima da Fase 1 (Nó 0A). Formato: fontes brutas ABNT.

---

## 1. Frente A — Harness Engineering e Context Engineering

O termo **harness** designa a camada de software que envolve o modelo de linguagem e
governa seu ciclo de execução: contexto (o que entra e sai da janela de atenção a cada
turno), ferramentas (ACI — Agent-Computer Interface), memória (persistência curto/longo
prazo, compaction, notas estruturadas) e o loop de execução (perceber–raciocinar–agir).
A engenharia de contexto (sucessora da engenharia de prompt) trata do "conjunto de
estratégias para curar e manter o conjunto ideal de tokens durante a inferência".
Conceitos centrais: janela de contexto como superfície de controle, context rot
(degradación da atenção com o crescimento da janela), compaction, structured
note-taking, progressive disclosure, system prompts em "altitude" correta e design
de ACI com poka-yoke.

- ANTHROPIC. **Building effective agents.** San Francisco: Anthropic Engineering, 2024. Disponível em: https://www.anthropic.com/engineering/building-effective-agents.
- ANTHROPIC. **Effective context engineering for AI agents.** San Francisco: Anthropic Engineering, 2025. Disponível em: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents.
- ANTHROPIC. **Writing effective tools for agents.** San Francisco: Anthropic Engineering, 2025. Disponível em: https://www.anthropic.com/engineering/writing-tools-for-agents.
- ANTHROPIC. **Model Context Protocol: specification and documentation.** San Francisco: Anthropic, 2024. Disponível em: https://modelcontextprotocol.io/.
- LANGCHAIN. **LangGraph: documentation and conceptual guides.** San Francisco: LangChain, 2024-2025. Disponível em: https://langchain-ai.github.io/langgraph/.
- LIU, Jerry. **Building performant agentic RAG and context systems.** San Francisco: LlamaIndex, 2024. Disponível em: https://www.llamaindex.ai/blog.

## 2. Frente B — Padrões de Orquestração de Agentes Autônomos

Padrões de orquestração em produção: **supervisor/worker** (decomposição e delegação com
isolamento de contexto), **planner-executor** (fases separadas, checkpoints de aprovação),
**reflection/reflexão** (o agente avalia a própria saída antes de retornar), **ReAct**
(raciocínio + ação em ciclo), **DAPER** (Detect–Analyze–Plan–Execute–Report para agentes
proativos). Frameworks: LangGraph (grafos de estado, checkpointers, persistência),
CrewAI (papéis/tarefas), OpenAI Agents SDK (handoffs), AWS Bedrock AgentCore, e execução
durável via Temporal (journal imutável, replay determinístico, idempotency keys).

- RUNKLE, Sydney. **Choosing the right multi-agent architecture.** LangChain Blog, 2026. Disponível em: https://www.langchain.com/blog/choosing-the-right-multi-agent-architecture.
- DANTRA, Ruskin; MAO, Shun; LIM, Justin; DAVIS, Cornelia. **Orchestrating intelligent agents at scale: how AgentCore and Temporal create robust AI systems.** AWS APN Blog, 2026. Disponível em: https://aws.amazon.com/blogs/apn/how-temporal-uses-amazon-bedrock-agentcore-to-create-robust-ai-systems/.
- SHEN, Alfred; DERBAKOVA, Anya. **Design multi-agent orchestration with reasoning using Amazon Bedrock and open source frameworks.** AWS Machine Learning Blog, 2026. Disponível em: https://aws.amazon.com/blogs/machine-learning/design-multi-agent-orchestration-with-reasoning-using-amazon-bedrock-and-open-source-frameworks/.
- TEMPORAL TECHNOLOGIES. **Durable multi-agentic AI architecture with Temporal.** Temporal Blog, 2025. Disponível em: https://temporal.io/blog/using-multi-agent-architectures-with-temporal.
- DIGITAL APPLIED. **Multi-agent orchestration: 5 patterns that work in 2026.** Digital Applied Research & Engineering Blog, 2026. Disponível em: https://www.digitalapplied.com/blog/multi-agent-orchestration-5-patterns-that-work.
- OPENAI. **OpenAI Agents SDK: documentation and guides.** San Francisco: OpenAI, 2025. Disponível em: https://openai.github.io/openai-agents-python/.

## 3. Frente C — Confiabilidade e Observabilidade de Loops

Agentes **falham de forma educada** (polite failures): completam o ciclo com saída
sintaticamente válida, mas tomam decisões incorretas. Observabilidade: telemetria
OpenTelemetry GenAI (convenções `gen_ai.*`), tracing por passo/árvore de execução,
LangSmith/Langfuse. Evals de agentes (Anthropic): task/trial/transcript/outcome,
graders por código vs. LLM-as-a-judge vs. humanos, pass@k, capability evals vs.
regression evals, golden sets. Confiabilidade operacional: step budget, circuit
breakers, rate limits com backoff coordenado (evitar retry storms), guardrails e
kill switches em runtime, durabilidade com replay determinístico e idempotência.

- NEWTON-KING, James. **Inside the LLM call: GenAI observability with OpenTelemetry.** OpenTelemetry Blog, 2026. Disponível em: https://opentelemetry.io/blog/2026/genai-observability/.
- ANTHROPIC. **Demystifying evals for AI agents.** San Francisco: Anthropic Engineering, 2026. Disponível em: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents.
- EXPANSO. **AI agent observability: best practices in 2026.** Expanso Blog, 2026. Disponível em: https://expanso.io/blog/ai-agent-observability-best-practices/.
- ZYLOS RESEARCH. **Durable execution for AI agent runtimes: checkpointing, replay, and recovery.** Zylos Research, 2026. Disponível em: https://zylos.ai/research/2026-04-24-durable-execution-agent-runtimes/.
- ORACLE AI & DATA SCIENCE. **Runtime budget guardrails for agentic AI.** Oracle Blogs, 2026. Disponível em: https://blogs.oracle.com/ai-and-datascience/runtime-budget-guardrails-agentic-ai.
- LANGCHAIN. **LangSmith: observability and evaluation platform.** San Francisco: LangChain, 2025. Disponível em: https://docs.smith.langchain.com/.

## 4. Frente D — Governança, Segurança e Operação

Governança: HITL em três níveis (in-the-loop, on-the-loop, over-the-loop), fila de
aprovação assíncrona com TTL e checkpointing, princípio da **menor agência** (least
agency), allow-lists e validação de schema de ferramentas, trilha de auditoria imutável,
identidade de máquina dedicada por agente. Riscos: loops infinitos e doom spirals,
tetos de custo (cost circuit breakers), drift de comportamento com model pinning,
testes em sandbox/simulação (contêineres efêmeros, WebAssembly), separação
cognitivo-executiva (Parallax). Segurança: prompt injection indireto como vetor nº 1
(OWASP Top 10 for Agentic Applications: goal hijack ASI01, tool misuse ASI02, identity
& privilege abuse ASI03), defesa em camadas com isolamento de privilégios.

- OWASP FOUNDATION. **OWASP Top 10 for agentic applications.** GenAI Security Project, 2025 (atualizado 2026). Disponível em: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/.
- FOKOU, Joel. **Parallax: why AI agents that think must never act.** arXiv preprint, 2026. Disponível em: https://arxiv.org/abs/2604.12986.
- MICROSOFT. **Architecting trust: a NIST-based security governance framework for AI agents.** Microsoft Defender for Cloud Blog, 2026. Disponível em: https://techcommunity.microsoft.com/blog/microsoftdefendercloudblog/architecting-trust-a-nist-based-security-governance-framework-for-ai-agents/4490556.
- HANCOCK, Parker. **When AI agents misbehave: governance and security for autonomous AI.** Baker Botts LLP, 2026. Disponível em: https://ourtake.bakerbotts.com/post/102me2l/when-ai-agents-misbehave-governance-and-security-for-autonomous-ai.
- FOUNTAIN CITY. **AI agent governance: a practitioner's guide.** Fountain City Engineering, 2026. Disponível em: https://fountaincity.tech/resources/blog/ai-agent-governance-practitioners-guide/.
- NIST. **AI Risk Management Framework (AI RMF 1.0).** Gaithersburg: National Institute of Standards and Technology, 2023. Disponível em: https://www.nist.gov/itl/ai-risk-management-framework.

---

## 5. Síntese de tese do livro (matéria-prima para a planta baixa)

1. **Autonomia sem harness é caos**: loops sem contenção degeneram em loops infinitos,
   custo descontrolado e decisões erradas que parecem corretas (polite failures).
2. **O harness é a camada**: contexto (janela de atenção), ferramentas (ACI), memória
   (persistência) e loop (controle de fluxo) formam o runtime do agente.
3. **Orquestração é engenharia**: supervisor, planner-executor, reflexão e ReAct são
   padrões de projeto, não acidentes — cada um com trade-offs de custo, latência e
   isolamento.
4. **Produção exige instrumentação**: telemetria por passo, evals com golden sets,
   step budgets, circuit breakers, kill switches e execução durável.
5. **Governança é arquitetura**: menor agência, trilha de auditoria imutável, HITL
   assíncrono, model pinning e separação cognitivo-executiva.
