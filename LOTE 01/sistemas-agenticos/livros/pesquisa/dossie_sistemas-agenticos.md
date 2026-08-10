# Dossiê de Pesquisa — Sistemas Agênticos de IA

## Conceitos-chave
- **Sistema agêntico (agentic system)**: sistema que percebe, raciocina, planeja e age autonomamente para atingir metas, usando LLMs como núcleo cognitivo combinado a memória, ferramentas e feedback do ambiente (Arunkumar et al., 2026; arXiv 2601.12560).
- **Agência**: capacidade de agir conforme objetivos/própria vontade; conceito central em IA desde Russell & Norvig; distingue agentes de ferramentas passivas (Agentic LLMs Survey, arXiv 2503.23037).
- **Dual-paradigma**: sistemas simbólicos/clássicos (planejamento algorítmico, estado persistente) vs. neurais/generativos (orquestração por prompt, geração estocástica); "conceptual retrofitting" é o erro de confundir os dois (Abou Ali et al., 2025; arXiv 2510.25445).
- **Loop agêntico (ReAct)**: intercalação de raciocínio (thought) e ação (act), base de grounding e trilhas verificáveis (Yao et al., 2023).
- **Agente transformer**: modelo policy embutido em loop de controle com interfaces explícitas para observações, memória, ferramentas com esquemas tipados e verificadores/críticos (arXiv 2601.01743).
- **Protocolo de comunicação**: MCP (tools/resources/prompts, JSON-RPC, versão 2026-07-28 stateless) e A2A (descoberta via agent-card, HTTP+JSON, task IDs) (modelcontextprotocol.io; Anyscale).
- **RAG vs memória**: RAG recupera conhecimento externo estático; memória de agente evolui com interações e feedback do ambiente; fronteira cada vez mais tênue (Weiß, 2026; arXiv 2512.13564).
- **Observabilidade**: traces (runs), threads (sessões multi-turn), trajetórias; semantic conventions GenAI da OpenTelemetry (`gen_ai.request.model`, `gen_ai.usage.input_tokens`) (LangSmith docs; opentelemetry.io).
- **Top 10 OWASP para aplicações agênticas (2026)**: Goal Hijack (ASI01), Tool Misuse (ASI02), Identity & Privilege Abuse (ASI03), Supply Chain (ASI04), Unexpected Code Execution (ASI05), Memory Poisoning (ASI06), Insecure Inter-Agent Communication (ASI07), Cascading Failures (ASI08), Human-Agent Trust Exploitation (ASI09), Rogue Agents (ASI10) (genai.owasp.org).
- **AI Act (UE)**: obrigações para modelos GPAI (art. 53: documentação técnica, política de copyright, resumo de conteúdo de treinamento; >10^23 FLOP) e risco sistêmico (art. 55: notificação, mitigação, incidentes; >10^25 FLOP); em aplicação desde 02/08/2025; GPAI Code of Practice publicado 10/07/2025 (digital-strategy.ec.europa.eu).
- **Agent washing**: renomear assistentes/RPA/chatbots como "agentes" sem capacidades agênticas reais; Gartner estima apenas ~130 de milhares de vendors reais (Gartner, 2025).

## Artigos Científicos e Papers
- ABOU ALI, M.; DORNAIKA, F.; CHARAFEDDINE, J. *Agentic AI: A Comprehensive Survey of Architectures, Applications, and Challenges*. arXiv:2510.25445, 2025. Disponível em: https://arxiv.org/abs/2510.25445.
- ARUNKUMAR, V.; GANGADHARAN, G. R.; BUYYA, R. *Agentic Artificial Intelligence (AI): Architectures, Taxonomies, and Evaluation of Large Language Model Agents*. arXiv:2601.12560, 2026. Disponível em: https://arxiv.org/abs/2601.12560.
- *AI Agent Systems: Architectures, Applications, and Evaluation*. arXiv:2601.01743, 2026. Disponível em: https://arxiv.org/abs/2601.01743.
- DEROUICHE, H.; BRAHMI, Z.; MAZENI, H. *Agentic AI Frameworks: Architectures, Protocols, and Design Challenges*. arXiv:2508.10146, 2025. Disponível em: https://arxiv.org/html/2508.10146.
- *Agentic Large Language Models, a survey*. arXiv:2503.23037, 2025. Disponível em: https://arxiv.org/html/2503.23037.
- LUO, J. et al. *Large Language Model Agent: A Survey on Methodology, Applications and Challenges*. arXiv:2503.21460, 2025. Disponível em: https://arxiv.org/abs/2503.21460.
- WANG, L. et al. *A Survey on Large Language Model based Autonomous Agents*. arXiv:2308.11432, 2023. Disponível em: https://arxiv.org/abs/2308.11432.
- CHENG, Y. et al. *Exploring Large Language Model based Intelligent Agents: Definitions, Methods, and Prospects*. arXiv:2401.03428, 2024. Disponível em: https://arxiv.org/html/2401.03428.
- HUANG, W. et al. *A Review of Prominent Paradigms for LLM-Based Agents: Tool Use (Including RAG), Planning, and Feedback Learning*. arXiv:2406.05804, 2024. Disponível em: https://arxiv.org/html/2406.05804.
- ZHAO, P.; JIN, Z.; CHENG, N. *An In-depth Survey of Large Language Model-based Artificial Intelligence Agents*. arXiv:2309.14365, 2023. Disponível em: https://arxiv.org/html/2309.14365.
- DE SILVA, L.; MENEGUZZI, F.; LOGAN, B. *BDI Agent Architectures: A Survey*. In: Proceedings of IJCAI 2020. Disponível em: https://www.ijcai.org/proceedings/2020/0684.pdf.
- RAO, A. S.; GEORGEFF, M. P. *Modeling Rational Agents within a BDI-Architecture*. 1991. Disponível em: https://jmvidal.cse.sc.edu/library/rao91a.pdf.
- WOOLDRIDGE, M. *The Belief-Desire-Intention Model of Agency*. ATAL'98. Disponível em: https://www.cs.ox.ac.uk/people/michael.wooldridge/pubs/atal98b.pdf.
- SINGH, A. et al. *Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG*. arXiv:2501.09136, 2025. Disponível em: https://arxiv.org/abs/2501.09136.
- WEISS, T. *Memory in the Age of AI Agents*. arXiv:2512.13564, 2026. Disponível em: https://arxiv.org/abs/2512.13564.
- DU, P. *Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers*. arXiv:2603.07670, 2026. Disponível em: https://arxiv.org/html/2603.07670.
- ZHANG, Z. et al. *A Survey on the Memory Mechanism of Large Language Model based Agents*. arXiv:2404.13501, 2024. Disponível em: https://arxiv.org/html/2404.13501.
- LIU, X. et al. *AgentBench: Evaluating LLMs as Agents*. arXiv:2308.03688, ICLR'24. Disponível em: https://arxiv.org/abs/2308.03688.
- ZHU, Y. et al. *Establishing Best Practices for Building Rigorous Agentic Benchmarks (ABC)*. arXiv:2507.02825, 2025. Disponível em: https://arxiv.org/html/2507.02825.
- PARK, J. S. et al. *Generative Agents: Interactive Simulacra of Human Behavior*. arXiv:2304.03442, 2023. (mencionado em surveys de memória) Disponível em: https://arxiv.org/abs/2304.03442.

## Estado da arte / ferramentas de referência
- **LangGraph**: grafos de execução (State, Nodes, Edges), reducers, checkpoints, human-in-the-loop via interrupt(), Send API para map-reduce; padrões: prompt chaining, parallelization, routing, orchestrator-worker, evaluator-optimizer (docs.langchain.com).
- **MCP (Model Context Protocol)**: especificação 2026-07-28 — núcleo stateless, primitivas tools/resources/prompts, extensões Tasks, MCP Apps, EMA; SDKs TS/Python/Go/C#; ~meio bilhão de downloads/mês (modelcontextprotocol.io; blog oficial).
- **A2A (Agent-to-Agent)**: descoberta dinâmica via agent-card.json, fronteiras HTTP+JSON, task IDs rastreáveis, versionamento por protocolo (Anyscale, 2026).
- **OpenTelemetry GenAI Semantic Conventions**: atributos padronizados gen_ai.* para spans, métricas (gen_ai.client.operation.duration, gen_ai.client.token.usage) e eventos; suporte em VS Code Copilot, Codex, Claude Code (opentelemetry.io).
- **Ray Serve / KubeRay**: microserviços de agentes com autoscaling independente (GPU para LLM, CPU para tools); padrão LLM + MCP servers + agentes como serviços (anyscale.com; docs.ray.io).
- **Kubernetes Agent Sandbox (SIG Apps)**: CRD Sandbox para workloads stateful singleton de agentes, isolamento gVisor/Kata, warm pools contra cold start (kubernetes.io/blog, 2026).
- **Benchmarks**: AgentBench (8 ambientes, 27 LLMs), SWE-bench Verified (500 amostras), SWE-Lancer ($1M Upwork), MLE-bench (75 Kaggle), GAIA, tau-bench, WebArena, OSWorld, PaperBench (evals.openai.com; github.com/THUDM/AgentBench).
- **Frameworks**: AutoGen, CrewAI, MetaGPT, Semantic Kernel, Agno, Google ADK, SmolAgents, PydanticAI, OpenAI Agents SDK, LlamaIndex (Derouiche et al., 2025).
- **Hospedagem de LLM**: vLLM (single-node), Ray Serve + vLLM (multi-node/multi-model), llm-d + K8s Inference Gateway (disaggregated prefill/decode) (premai.io, 2026).

## Casos de uso corporativos
- **Gartner (2025)**: 40% dos apps empresariais com agentes de tarefa até 2026 (<5% em 2025); receita de agentic AI pode chegar a ~30% do software empresarial (~US$450B) em 2035; 15% das decisões diárias autônomas até 2028; 33% dos apps de software com agentic AI em 2028; 50% dos knowledge workers desenvolverão novas skills até 2029 (gartner.com).
- **Deloitte (2025)**: mercado de agentic AI de US$3,7B (2023) para US$103,6B (2032); >80% dos líderes de automação acelerando investimentos em 2025 (Forrester); custo-por-token e reuso de agentes como P&L operacional (deloitte.com).
- **Gartner Hype Cycle 2026**: agentic AI no Pico de Expectativas Infladas; apenas 17% das organizações implantaram agentes, mas >60% planejam em 2 anos; emergência de governança, segurança e FinOps para agentic AI (gartner.com).
- **Contra-cautela**: Gartner prevê >40% dos projetos agentic cancelados até 2027 por custos, valor pouco claro ou controles de risco inadequados (gartner.com, 2025).
- **OWASP**: incidentes reais — EchoLeak (exfiltração), Amazon Q (tool misuse), GitHub MCP exploit (supply chain), AutoGPT RCE, Gemini Memory Attack, Replit meltdown (rogue agent) (genai.owasp.org).
- **Anthropic MCP em produção**: code execution with MCP reduz token usage de 150k para 2k tokens (-98,7%); PII tokenização antes do contexto do modelo (anthropic.com/engineering).

## Limitações e controvérsias
- **Hallucination in action, infinite loops, prompt injection**: falhas de modo principais de agentes em produção (arXiv 2601.12560).
- **Qualidade de benchmarks**: SWE-bench Verified com testes insuficientes (24% das posições do top-50 incorretas); ~30% das tarefas de SWE-Bench Pro quebradas; tau-bench conta resposta vazia como sucesso (38% de sucesso para agente trivial) (OpenAI; arXiv 2507.02825).
- **Agentes vs workflows**: muitos casos "agentic" não exigem agentes — usar agentes quando decisões são necessárias, automação para rotinas, assistentes para recuperação (Gartner).
- **Conceptual retrofitting**: confusão entre paradigmas simbólico e neural leva a avaliação e governança inadequadas (arXiv 2510.25445).
- **Custo e latência**: agentic RAG amplifica tokens (raciocínio intermediário, tool calls, crítica) — token amplification; trade-offs retrieval depth vs cost, planning vs latency (arXiv 2603.07379).
- **Memória**: contextos longos não substituem memória externa (custo quadrático, sem persistência entre sessões, sem governança/delete) (arXiv 2603.07670).
- **Regulação**: enforcement do AI Act para GPAI a partir de 02/08/2026 (multas); conformidade até 2027 para modelos pré-existentes (digital-strategy.ec.europa.eu).

## Fontes brutas (para Nó 7 — Auditor de Rastreabilidade)
- ABOU ALI, Mohamad; DORNAIKA, Fadi; CHARAFEDDINE, Jinan. *Agentic AI: A Comprehensive Survey of Architectures, Applications, and Challenges*. Disponível em: https://arxiv.org/abs/2510.25445. Acesso em: 07 ago. 2026.
- ARUNKUMAR, V.; GANGADHARAN, G. R.; BUYYA, Rajkumar. *Agentic Artificial Intelligence (AI): Architectures, Taxonomies, and Evaluation of Large Language Model Agents*. Disponível em: https://arxiv.org/abs/2601.12560. Acesso em: 07 ago. 2026.
- *AI Agent Systems: Architectures, Applications, and Evaluation*. Disponível em: https://arxiv.org/abs/2601.01743. Acesso em: 07 ago. 2026.
- DEROUICHE, Hana; BRAHMI, Zaki; MAZENI, Haithem. *Agentic AI Frameworks: Architectures, Protocols, and Design Challenges*. Disponível em: https://arxiv.org/html/2508.10146. Acesso em: 07 ago. 2026.
- *Agentic Large Language Models, a survey*. Disponível em: https://arxiv.org/html/2503.23037. Acesso em: 07 ago. 2026.
- LUO, Junyu; ZHANG, Weizhi; YUAN, Ye et al. *Large Language Model Agent: A Survey on Methodology, Applications and Challenges*. Disponível em: https://arxiv.org/abs/2503.21460. Acesso em: 07 ago. 2026.
- WANG, Lei; MA, Chen; FENG, Xueyang et al. *A Survey on Large Language Model based Autonomous Agents*. Disponível em: https://arxiv.org/abs/2308.11432. Acesso em: 07 ago. 2026.
- CHENG, Yuheng; ZHANG, Ceyao; ZHANG, Zhengwen et al. *Exploring Large Language Model based Intelligent Agents: Definitions, Methods, and Prospects*. Disponível em: https://arxiv.org/html/2401.03428. Acesso em: 07 ago. 2026.
- HUANG, Wenhao; ABUDULAILI, Xin; RONG, Yang et al. *A Review of Prominent Paradigms for LLM-Based Agents: Tool Use (Including RAG), Planning, and Feedback Learning*. Disponível em: https://arxiv.org/html/2406.05804. Acesso em: 07 ago. 2026.
- ZHAO, Pengyu; JIN, Zijian; CHENG, Ning. *An In-depth Survey of Large Language Model-based Artificial Intelligence Agents*. Disponível em: https://arxiv.org/html/2309.14365. Acesso em: 07 ago. 2026.
- DE SILVA, Lavindra; MENEGUZZI, Felipe; LOGAN, Brian. *BDI Agent Architectures: A Survey*. Disponível em: https://www.ijcai.org/proceedings/2020/0684.pdf. Acesso em: 07 ago. 2026.
- RAO, Anand S.; GEORGEFF, Michael P. *Modeling Rational Agents within a BDI-Architecture*. Disponível em: https://jmvidal.cse.sc.edu/library/rao91a.pdf. Acesso em: 07 ago. 2026.
- WOOLDRIDGE, Michael. *The Belief-Desire-Intention Model of Agency*. Disponível em: https://www.cs.ox.ac.uk/people/michael.wooldridge/pubs/atal98b.pdf. Acesso em: 07 ago. 2026.
- SINGH, Aditi; EHTESHAM, Abul; KUMAR, Saket et al. *Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG*. Disponível em: https://arxiv.org/abs/2501.09136. Acesso em: 07 ago. 2026.
- WEISS, T. *Memory in the Age of AI Agents*. Disponível em: https://arxiv.org/abs/2512.13564. Acesso em: 07 ago. 2026.
- DU, Pengfei. *Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers*. Disponível em: https://arxiv.org/html/2603.07670. Acesso em: 07 ago. 2026.
- ZHANG, Zeyu; BO, Xiaohe; MA, Chen et al. *A Survey on the Memory Mechanism of Large Language Model based Agents*. Disponível em: https://arxiv.org/html/2404.13501. Acesso em: 07 ago. 2026.
- LIU, Xiao; YU, Hao; ZHANG, Hanchen et al. *AgentBench: Evaluating LLMs as Agents*. Disponível em: https://arxiv.org/abs/2308.03688. Acesso em: 07 ago. 2026.
- ZHU, Yuxuan; JIN, Tengjun; PRUKSACHATKUN, Yada et al. *Establishing Best Practices for Building Rigorous Agentic Benchmarks*. Disponível em: https://arxiv.org/html/2507.02825. Acesso em: 07 ago. 2026.
- PARK, Joon Sung; O'BRIEN, Joseph; CAI, Carrie et al. *Generative Agents: Interactive Simulacra of Human Behavior*. Disponível em: https://arxiv.org/abs/2304.03442. Acesso em: 07 ago. 2026.
- MODEL CONTEXT PROTOCOL. *Specification 2026-07-28*. Disponível em: https://modelcontextprotocol.io/specification/2026-07-28. Acesso em: 07 ago. 2026.
- SORIA PARRA, David; DELIMARSKY, Den. *The 2026-07-28 Specification | MCP Blog*. Disponível em: https://blog.modelcontextprotocol.io/posts/2026-07-28/. Acesso em: 07 ago. 2026.
- ANTHROPIC. *Code execution with MCP: building more efficient AI agents*. Disponível em: https://www.anthropic.com/engineering/code-execution-with-mcp. Acesso em: 07 ago. 2026.
- LANGCHAIN. *Workflows and agents — Docs*. Disponível em: https://docs.langchain.com/oss/python/langgraph/workflows-agents. Acesso em: 07 ago. 2026.
- LANGCHAIN. *Graph API overview — Docs*. Disponível em: https://docs.langchain.com/oss/python/langgraph/graph-api. Acesso em: 07 ago. 2026.
- LANGCHAIN. *Trace with OpenTelemetry — LangSmith Docs*. Disponível em: https://docs.langchain.com/langsmith/trace-with-opentelemetry. Acesso em: 07 ago. 2026.
- LANGCHAIN. *Observability concepts — LangSmith Docs*. Disponível em: https://docs.langchain.com/langsmith/observability-concepts. Acesso em: 07 ago. 2026.
- OPENAI. *Evals (PaperBench, SWE-Lancer, MLE-bench, SWE-bench Verified)*. Disponível em: https://evals.openai.com/. Acesso em: 07 ago. 2026.
- OPENAI. *Separating signal from noise in coding evaluations*. Disponível em: https://openai.com/index/separating-signal-from-noise-coding-evaluations/. Acesso em: 07 ago. 2026.
- THUDM. *AgentBench: A Comprehensive Benchmark to Evaluate LLMs as Agents*. Disponível em: https://github.com/THUDM/AgentBench. Acesso em: 07 ago. 2026.
- OWASP GEN AI SECURITY PROJECT. *OWASP Top 10 for Agentic Applications for 2026*. Disponível em: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/. Acesso em: 07 ago. 2026.
- OWASP. *AI Agent Security Cheat Sheet*. Disponível em: https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html. Acesso em: 07 ago. 2026.
- ANYSCALE. *AI agents on Ray Serve: Single to multi-agent architecture*. Disponível em: https://www.anyscale.com/blog/ai-agents-on-ray-serve-single-to-multi-agent-architecture. Acesso em: 07 ago. 2026.
- RAY PROJECT. *Deploy on Kubernetes — Ray Serve*. Disponível em: https://docs.ray.io/en/latest/serve/production-guide/kubernetes.html. Acesso em: 07 ago. 2026.
- KUBERNETES. *Running Agents on Kubernetes with Agent Sandbox*. Disponível em: https://kubernetes.io/blog/2026/03/20/running-agents-on-kubernetes-with-agent-sandbox/. Acesso em: 07 ago. 2026.
- OPENTELEMETRY. *Inside the LLM Call: GenAI Observability with OpenTelemetry*. Disponível em: https://opentelemetry.io/blog/2026/genai-observability/. Acesso em: 07 ago. 2026.
- OPENTELEMETRY. *Semantic Conventions for Generative AI*. Disponível em: https://github.com/open-telemetry/semantic-conventions-genai. Acesso em: 07 ago. 2026.
- EUROPEAN COMMISSION. *Guidelines on the scope of obligations for providers of general-purpose AI models under the AI Act*. Disponível em: https://digital-strategy.ec.europa.eu/en/library/guidelines-scope-obligations-providers-general-purpose-ai-models-under-ai-act. Acesso em: 07 ago. 2026.
- EUROPEAN COMMISSION. *General-purpose AI obligations under the AI Act*. Disponível em: https://digital-strategy.ec.europa.eu/en/factpages/general-purpose-ai-obligations-under-ai-act. Acesso em: 07 ago. 2026.
- EUROPEAN COMMISSION. *The General-Purpose AI Code of Practice*. Disponível em: https://digital-strategy.ec.europa.eu/en/node/13953/printable/pdf. Acesso em: 07 ago. 2026.
- GARTNER. *Gartner Predicts 40% of Enterprise Apps Will Feature Task-Specific AI Agents by 2026*. Disponível em: https://www.gartner.com/en/newsroom/press-releases/2025-08-26-gartner-predicts-40-percent-of-enterprise-apps-will-feature-task-specific-ai-agents-by-2026-up-from-less-than-5-percent-in-2025. Acesso em: 07 ago. 2026.
- GARTNER. *Gartner Predicts Over 40% of Agentic AI Projects Will Be Canceled by End of 2027*. Disponível em: https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027. Acesso em: 07 ago. 2026.
- GARTNER. *2026 Hype Cycle for Agentic AI*. Disponível em: https://www.gartner.com/en/articles/hype-cycle-for-agentic-ai. Acesso em: 07 ago. 2026.
- DELOITTE. *Agentic AI in enterprise: Adoption, risk, and transformation*. Disponível em: https://www.deloitte.com/content/dam/assets-zone3/us/en/docs/services/consulting/2025/agentic-ai-enterprise-adoption-guide.pdf. Acesso em: 07 ago. 2026.
- PREMAI. *Deploying LLMs on Kubernetes: vLLM, Ray Serve & GPU Scheduling Guide*. Disponível em: https://www.premai.io/blog/deploying-llms-on-kubernetes-vllm-ray-serve-gpu-scheduling-guide-2026/. Acesso em: 07 ago. 2026.
