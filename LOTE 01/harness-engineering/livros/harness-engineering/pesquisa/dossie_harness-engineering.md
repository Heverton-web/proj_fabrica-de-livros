# Dossiê de Pesquisa — Harness Engineering

> Revisado em: 2026-08-09. Classificação de fontes (A) primária/peer-reviewed, (B) documentação oficial, (C) conteúdo secundário. Meta R-FT-1: ≥70% A+B (alvo ≥80%).

## Conceitos-chave

- **Harness Engineering**: disciplina de engenharia de software que projeta, constrói e mantém o arcabouço externo ao modelo de linguagem — ambiente de execução, ferramentas, memória, controle de estado, loops de feedback e guardrails — que transforma um LLM não-determinístico em um sistema autônomo confiável. Máxima da área: **Agente = Modelo + Harness** [1][3][18].
- **Test Harness (herança da engenharia de software clássica)**: fixtures, scripts de teste, linters e analisadores estáticos que verificam deterministicamente se as saídas do agente atendem a contratos lógicos e funcionais [2][4][18].
- **Safety Harness / Guardrails**: camada regulatória que intercepta tool calls para bloquear ações destrutivas, vazamento de dados ou alucinações críticas — ex.: exigir aprovação humana para deletes/deploys em produção [5][7][17].
- **AI Agent Harness / System Scaffolding**: todo o código, configuração e lógica de execução que não pertence ao LLM: sistema de arquivos + Git, sandboxes, orquestração de ferramentas, MCP, gestão de contexto [3][6][7].
- **Ciclo ReAct (Reason → Act → Observe)**: loop básico em que o modelo decide uma ação, o harness executa (terminal, navegador, FS) e devolve o resultado como novo contexto [4].
- **Controle dual**: *Guides* (feedforward — AGENTS.md, linters, arquitetura) antecipam comportamento indesejado; *Sensors* (feedback — testes determinísticos, LLM-as-a-judge) observam e corrigem após a ação [5].
- **Context Rot**: degradação de qualidade por contexto poluído/velho; combate com compactação inteligente, offloading de ferramentas e divulgação progressiva (progressive disclosure) [6][8].
- **Ralph Wiggum Loop**: padrão de iteração em que o agente revisa o próprio trabalho em loop (com revisores agente-a-agente) até satisfazer critérios — usado para execuções de longa duração (horas) [1].
- **Approval Gates**: prompts de aprovação humana para ações sensíveis; o abuso gera *consent fatigue* (fadiga de consentimento) [15][16][17].
- **Injeção de prompt indireta**: dados externos não confiáveis (README, issues, docs) injetam instruções maliciosas que o agente interpreta como legítimas [14][15].
- **Menor privilégio (least privilege)**: agentes não herdam permissões de root nem tokens globais; escopo restrito por sessão, diretórios limitados, trilhas de auditoria [14][17].

## Artigos Científicos e Papers

- JIM, C. et al. *SWE-bench: Can Language Models Resolve Real-world GitHub Issues?* ICLR, 2024. Disponível em: https://arxiv.org/abs/2310.06770. Acesso em: 09 ago. 2026. (A)
- ALEITHAN, A. et al. *SWE-Bench+: Enhanced Coding Benchmark for LLMs*. University of Waterloo, 2024. Disponível em: https://arxiv.org/abs/2410.06992. Acesso em: 09 ago. 2026. (A)
- YAO, S. et al. *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR, 2023. Disponível em: https://arxiv.org/abs/2210.03629. Acesso em: 09 ago. 2026. (A)
- NING, X. et al. *Code as Agent Harness: Toward Executable, Verifiable, and Stateful Agent Systems*. arXiv:2605.18747, 2026. Disponível em: https://arxiv.org/html/2605.18747v1. Acesso em: 09 ago. 2026. (A)
- HU, W. *Architectural Design Decisions in AI Agent Harnesses*. arXiv:2604.18071, 2026. Disponível em: https://arxiv.org/html/2604.18071v1. Acesso em: 09 ago. 2026. (A)
- UTESVSKY, R. (Adversa AI). *SymJack: The approval prompt is lying to you — symlink-RCE in five AI coding agents*. 2026. Disponível em: https://adversa.ai/blog/the-approval-prompt-is-lying-to-you-symlink-rce-in-five-ai-coding-agents-claude-code-cursor-antigravity-copilot-grok-build/. Acesso em: 09 ago. 2026. (C)

## Estado da arte / ferramentas de referência

- **OpenAI — Harness engineering: leveraging Codex in an agent-first world** (Ryan Lopopolo, 11 fev. 2026): experimento real de 5 meses construindo produto de software com 0 linhas de código escritas à mão; ~1 milhão de linhas, ~1.500 PRs, 3,5 PRs/engenheiro/dia; lições sobre especificar intenção, legibilidade do app para o agente e feedback loops [1]. (A)
- **Thoughtworks / Martin Fowler — Harness engineering for coding agent users** (Birgitta Böckeler, abr. 2026): taxonomia de sensores computacionais vs. inferenciais, categorias regulatórias de maintainability harness, controle feedforward/feedback [5]. (B)
- **LangChain — The Anatomy of an Agent Harness** (Vivek Trivedy, mar. 2026): arquivos, sandboxes, memória e estratégias contra context rot [6]. (B)
- **Databricks — What is an AI Agent Harness?**: visão institucional sobre governança empresarial, sandboxes e impacto do harness no desempenho de modelos de fronteira [7]. (B)
- **Awesome Harness Engineering** (repositório comunitário, 2026): curadoria de ferramentas, papers e práticas da área [8]. (B)
- **Ferramentas de eval e guardrails**: Promptfoo, DeepEval (evals/regressão de prompts), Guardrails AI (validação em runtime), LangGraph (orquestração por grafos de estado) [6][8]. (B)
- **Model Context Protocol (MCP)**: padrão aberto da Anthropic para conectar LLMs a ferramentas/dados; padroniza a camada de tools do harness [13]. (B)
- **Sandboxing**: Docker, gVisor, Firecracker (microVMs efêmeras), eBPF para interceptação de syscalls em tempo real (projeto ActPlane) [14][17]. (B)

## Casos de uso corporativos

- **Engenharia de software agêntica (OpenAI/Codex)**: produto completo construído por agentes; humanos desenham ambientes, especificam intenção e constroem loops de feedback; revisão majoritariamente agente-a-agente; execuções únicas de até 6 horas [1]. (A)
- **Atendimento ao cliente autônomo**: ~26% dos casos primários de agentes em produção — resolução de requisições pontuais sem intervenção humana [12]. (B)
- **Pesquisa, análise de dados e conhecimento**: síntese de grandes volumes de dados internos/externos, automação de fluxos de conhecimento [12]. (B)
- **Adoção**: 57% das organizações já têm agentes em produção (LangChain State of Agent Engineering, ~1.300 profissionais); 89% têm observabilidade, 52% usam evals formais [12]. (B)
- **Previsões Gartner**: 40% dos aplicativos corporativos terão agentes especializados até o fim de 2026 (de <5% em 2025); mais de 40% dos projetos de agentes serão cancelados até 2027 por custo, ROI incerto e controles de risco inadequados [10][11]. (A)

## Limitações e controvérsias

- **Qualidade e alucinações**: principal bloqueio em produção (~32%); alucinações em cadeias multi-passos comprometem tarefas complexas e geram perdas financeiras bilionárias estimadas [12]. (B)
- **Latência e custo**: loops de raciocínio + tool calls elevam latência (2ª barreira, ~20%); agentes autônomos multiplicam consumo de tokens [12]. (B)
- **Segurança e governança**: em grandes corporações, segurança supera latência como preocupação (~25%); agentes com privilégios de escrita/API abrem vetores para execuções indesejadas, vazamento e prompt injection indireto [14][15][17]. (C)
- **Paradoxo DORA 2024**: IA aumenta produtividade individual, fluxo e satisfação, mas impactou negativamente desempenho de entrega (estabilidade/throughput) — fundamentos de engenharia continuam essenciais [9]. (A)
- **SymJack (2026)**: coding agents (Claude Code, Cursor, Codex, Copilot, Grok) enganáveis por ataques de symlink — o prompt de aprovação mostra caminho benigno, mas o kernel redireciona escrita para credenciais; RCE no próximo reinício. Defesa: *intent-aware security* e resolução de symlinks antes de exibir destinos reais [16]. (C)
- **Riscos do MCP**: confused deputy (servidor executa com permissões do hospedeiro), injeção de prompt via metadados de ferramentas, cadeia de suprimentos de servidores não oficiais [14][15]. (C)
- **"Agent washing"**: rebranding de chatbots simples como agentes autônomos infla o mercado e distorce métricas [11]. (A)

## Fontes brutas (para Nó 7 — Auditor de Rastreabilidade)

- OPENAI (LOPOPOLO, Ryan). *Harness engineering: leveraging Codex in an agent-first world*. 11 fev. 2026. Disponível em: https://openai.com/index/harness-engineering/. Acesso em: 09 ago. 2026. (A)
- JIM, Carlos et al. *SWE-bench: Can Language Models Resolve Real-world GitHub Issues?* Disponível em: https://arxiv.org/abs/2310.06770. Acesso em: 09 ago. 2026. (A)
- ALEITHAN, Ali et al. *SWE-Bench+: Enhanced Coding Benchmark for LLMs*. Disponível em: https://arxiv.org/abs/2410.06992. Acesso em: 09 ago. 2026. (A)
- YAO, Shunyu et al. *ReAct: Synergizing Reasoning and Acting in Language Models*. Disponível em: https://arxiv.org/abs/2210.03629. Acesso em: 09 ago. 2026. (A)
- BÖCKELER, Birgitta. *Harness engineering for coding agent users*. Thoughtworks/Martin Fowler, abr. 2026. Disponível em: https://martinfowler.com/articles/harness-engineering.html. Acesso em: 09 ago. 2026. (B)
- TRIVEDY, Vivek. *The Anatomy of an Agent Harness*. LangChain, mar. 2026. Disponível em: https://www.langchain.com/blog/the-anatomy-of-an-agent-harness. Acesso em: 09 ago. 2026. (B)
- DATABRICKS ENGINEERING. *What is an AI Agent Harness?* 2026. Disponível em: https://www.databricks.com/blog/ai-harness. Acesso em: 09 ago. 2026. (B)
- AI-BOOST. *Awesome Harness Engineering*. GitHub, 2026. Disponível em: https://github.com/ai-boost/awesome-harness-engineering. Acesso em: 09 ago. 2026. (B)
- GOOGLE CLOUD / DORA. *Accelerate State of DevOps Report 2024*. Disponível em: https://dora.dev/research/2024/dora-report/. Acesso em: 09 ago. 2026. (A)
- GARTNER. *Gartner Predicts Over 40 Percent of Agentic AI Projects Will Be Canceled by End of 2027*. 25 jun. 2025. Disponível em: https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027. Acesso em: 09 ago. 2026. (A)
- GARTNER. *Gartner Predicts 40 Percent of Enterprise Apps Will Feature Task-Specific AI Agents by 2026*. 26 ago. 2025. Disponível em: https://www.gartner.com/en/newsroom/press-releases/2025-08-26-gartner-predicts-40-percent-of-enterprise-apps-will-feature-task-specific-ai-agents-by-2026-up-from-less-than-5-percent-in-2025. Acesso em: 09 ago. 2026. (A)
- LANGCHAIN. *State of Agent Engineering 2026*. Disponível em: https://www.langchain.com/state-of-agent-engineering. Acesso em: 09 ago. 2026. (B)
- ANTHROPIC. *Introducing the Model Context Protocol*. Disponível em: https://www.anthropic.com/news/model-context-protocol. Acesso em: 09 ago. 2026. (B)
- RED HAT PRODUCT SECURITY (CANO GABARDA, F.). *Model Context Protocol (MCP): Understanding security risks and controls*. 2025. Disponível em: https://www.redhat.com/en/blog/model-context-protocol-mcp-understanding-security-risks-and-controls. Acesso em: 09 ago. 2026. (B)
- EMBRACE THE RED. *MCP: Untrusted Servers and Confused Clients, Plus a Sneaky Exploit*. 2025. Disponível em: https://embracethered.com/blog/posts/2025/model-context-protocol-security-risks-and-exploits/. Acesso em: 09 ago. 2026. (C)
- UTESVSKY, Roy (Adversa AI). *SymJack: The approval prompt is lying to you*. 2026. Disponível em: https://adversa.ai/blog/the-approval-prompt-is-lying-to-you-symlink-rce-in-five-ai-coding-agents-claude-code-cursor-antigravity-copilot-grok-build/. Acesso em: 09 ago. 2026. (C)
- LASSO SECURITY (OXENBERG, O.; SUISA, E.). *Claude Code Security: Protect Autonomous Coding Agents*. 2026. Disponível em: https://www.lasso.security/blog/claude-code-security. Acesso em: 09 ago. 2026. (C)
- NING, X. et al. *Code as Agent Harness: Toward Executable, Verifiable, and Stateful Agent Systems*. arXiv:2605.18747, 2026. Disponível em: https://arxiv.org/html/2605.18747v1. Acesso em: 09 ago. 2026. (A)
- HU, W. *Architectural Design Decisions in AI Agent Harnesses*. arXiv:2604.18071, 2026. Disponível em: https://arxiv.org/html/2604.18071v1. Acesso em: 09 ago. 2026. (A)
