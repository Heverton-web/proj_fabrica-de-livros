# Dossiê de Pesquisa — Volume 2: O Arsenal do Agente

## Conceitos-chave

- **Agent Skills**: módulos reutilizáveis baseados em arquivos (instruções, metadados e recursos opcionais como scripts/templates) que dão ao agente conhecimento especializado de domínio. Carregam sob demanda (progressive disclosure), não inflando o contexto.
- **Progressive disclosure**: cada skill expõe apenas uma descrição curta no contexto; o corpo completo é carregado quando a tarefa exige — a chave da economia de tokens.
- **Granularidade**: skills devem ser específicas e coesas (uma responsabilidade), nunca monólitos; granularidade correta é o que a literatura comum omite.
- **Idempotência**: reexecutar a mesma skill/operação com as mesmas entradas produz o mesmo resultado, sem efeitos colaterais duplicados — padrões Check-Before-Act, Upsert e Tombstone.
- **Model Context Protocol (MCP)**: padrão aberto que conecta aplicações de IA (hosts/clients) a fontes de dados e ferramentas (servers) via JSON-RPC 2.0.
- **Primitivas MCP — Tools**: funções que o LLM chama para agir (model-controlled); métodos `tools/list` e `tools/call`.
- **Primitivas MCP — Resources**: fontes de dados passivas para contexto, geralmente read-only (application-controlled); `resources/list`, `resources/read`, `resources/subscribe`.
- **Primitivas MCP — Prompts**: templates de instrução pré-construídos (user-controlled); `prompts/list`, `prompts/get`.
- **Autonomia assistida**: o agente opera com os recursos necessários para resolver problemas complexos com intervenção humana mínima, mas com guardrails.
- **A2A (Agent-to-Agent)**: protocolo de interoperabilidade entre agentes, complementar ao MCP (que conecta agente a ferramentas/dados).

## Artigos Científicos e Papers

- NARGUND, Nisharg; SWAIN, Anil Kumar; BEHERA, Naliniprava. *Model Context Protocol (MCP): A Lightweight, Modular Framework for Tool-Augmented LLM Agents*. In: 2025 13th International Conference on Intelligent Systems and Embedded Design (ISED). 2025. Disponível em: https://doi.org/10.1109/ised67359.2025.11405153. Acesso em: 10 ago. 2026. (A)
- EHTESHAM, Abul et al. *A survey of agent interoperability protocols: Model Context Protocol (MCP), Agent Communication Protocol (ACP), Agent-to-Agent Protocol (A2A), and Agent Network Protocol (ANP)*. In: arXiv.org. 2025. Disponível em: https://www.semanticscholar.org/paper/18f349f0452eea2e9cce6b7d3424e0f9f7d9c5bc. Acesso em: 10 ago. 2026. (A)
- FAN, Shiqing et al. *MCPToolBench++: A Large Scale AI Agent Model Context Protocol MCP Tool Use Benchmark*. In: arXiv.org. 2025. Disponível em: https://www.semanticscholar.org/paper/153e3227cdc8e8b54034b6166a468bd751e117cc. Acesso em: 10 ago. 2026. (A)
- LIU, Wenrui et al. *MCPAgentBench: A Real-world Task Benchmark for Evaluating LLM Agent MCP Tool Use*. In: arXiv.org. 2025. Disponível em: https://www.semanticscholar.org/paper/f880f0433dc8bc2d9c8cb2b66cf003e772091b99. Acesso em: 10 ago. 2026. (A)
- RAJAK, Shaik; NAGANABOINA, Venkata Ramesh; REDDY, G. Pradeep. *Model Context Protocol (MCP) and Agent-to-Agent (A2A) Protocol for Scalable Agentic AI Systems*. In: 2026 Third International Conference on Innovations in Cybersecurity and Data Science (ICICDS). 2026. Disponível em: https://doi.org/10.1109/icicds70526.2026.11604962. Acesso em: 10 ago. 2026. (A)
- SILVA, L.; KÖCHER, Aljosha; GEHLHOFF, Felix. *Beyond Formal Semantics for Capabilities and Skills: Model Context Protocol in Manufacturing*. In: IEEE International Conference on Emerging Technologies and Factory Automation. 2025. Disponível em: https://www.semanticscholar.org/paper/383684744f191c35bc07cfb11446cffbc6720c9e. Acesso em: 10 ago. 2026. (A)
- ZHANG, Dongsen et al. *MCP Security Bench (MSB): Benchmarking Attacks Against Model Context Protocol in LLM Agents*. In: arXiv.org. 2025. Disponível em: https://www.semanticscholar.org/paper/bb33f9e07e661b52a6fade948f71d5a0e0bbc773. Acesso em: 10 ago. 2026. (A)
- WANG, Zihan et al. *MPMA: Preference Manipulation Attack Against Model Context Protocol*. In: AAAI Conference on Artificial Intelligence. 2025. Disponível em: https://www.semanticscholar.org/paper/b603506125f970db799d84fc9e1b5ce9b2a45162. Acesso em: 10 ago. 2026. (A)
- ZHOU, Zhenhong et al. *MCPShield: A Security Cognition Layer for Adaptive Trust Calibration in Model Context Protocol Agents*. In: arXiv.org. 2026. Disponível em: https://www.semanticscholar.org/paper/862cf894d5234e55038e588326b0ed86eca878b3. Acesso em: 10 ago. 2026. (A)

## Estado da arte / ferramentas de referência

- **Model Context Protocol (especificação oficial)**: define os três primitivos de servidor (tools, resources, prompts) e os métodos de protocolo; evolução sob governança aberta (Linux Foundation). Disponível em: https://modelcontextprotocol.io
- **Agent Skills (Anthropic)**: sistema de skills com frontmatter YAML, carregamento sob demanda e progressive disclosure; pré-construídas para documentos e customizáveis. Disponível em: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- **Anthropic Engineering — Equipping agents**: padrões para escrever skills que o agente realmente usa (nomes/descrições claras, granularidade, idempotência). Disponível em: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- **Anthropic Engineering — Writing effective tools**: guia de design de ferramentas para agentes (anotações, isError, evitar blobs gigantes). Disponível em: https://www.anthropic.com/engineering/writing-tools-for-agents
- **OpenAI Codex — MCP**: Codex como host MCP, conexão a servidores remotos e compartilhamento de configuração. Disponível em: https://developers.openai.com/codex/mcp

## Casos de uso corporativos

- **Skill collections**: equipes empacotam revisão de código, padrões de segurança e formatos de saída como skills carregadas sob demanda por rotina/PR.
- **Hosts MCP em produção**: ChatGPT desktop, Claude Desktop, Codex CLI, Copilot Studio e Cloudflare Agents conectando servidores MCP para dados e ferramentas externas.
- **Agentes de engenharia com MCP**: GitHub MCP server para issues/PRs, servidores de banco de dados e APIs via MCP em pipelines agentic.

## Limitações e controvérsias

- **Segurança MCP**: benchmarks (MSB) e ataques (MPMA, preferência manipulada) mostram que servidores não confiáveis podem injetar ou manipular o agente — anotações de ferramentas são não confiáveis.
- **Context bloat**: colocar documentação grande como tool (em vez de resource) estoura o contexto e degrada latência.
- **Ferramentas destrutivas sem escopo**: deleções acidentais exigem separação + aprovação humana (human-in-the-loop é SHOULD do spec).
- **Idempotência negligenciada**: chamadas duplicadas (retry, webhook) geram efeitos colaterais duplicados — o padrão é deduplicar no chamador.
- **Hype vs. maturidade**: protocolos de interoperabilidade (MCP/A2A/ACP/ANP) ainda consolidam; padrão único não está estabelecido.

## Fontes brutas (para Nó 7 — Auditor de Rastreabilidade)

- NARGUND, Nisharg; SWAIN, Anil Kumar; BEHERA, Naliniprava. *Model Context Protocol (MCP): A Lightweight, Modular Framework for Tool-Augmented LLM Agents*. Disponível em: https://doi.org/10.1109/ised67359.2025.11405153. Acesso em: 10 ago. 2026. (A)
- EHTESHAM, Abul et al. *A survey of agent interoperability protocols: Model Context Protocol (MCP), Agent Communication Protocol (ACP), Agent-to-Agent Protocol (A2A), and Agent Network Protocol (ANP)*. Disponível em: https://www.semanticscholar.org/paper/18f349f0452eea2e9cce6b7d3424e0f9f7d9c5bc. Acesso em: 10 ago. 2026. (A)
- FAN, Shiqing et al. *MCPToolBench++: A Large Scale AI Agent Model Context Protocol MCP Tool Use Benchmark*. Disponível em: https://www.semanticscholar.org/paper/153e3227cdc8e8b54034b6166a468bd751e117cc. Acesso em: 10 ago. 2026. (A)
- LIU, Wenrui et al. *MCPAgentBench: A Real-world Task Benchmark for Evaluating LLM Agent MCP Tool Use*. Disponível em: https://www.semanticscholar.org/paper/f880f0433dc8bc2d9c8cb2b66cf003e772091b99. Acesso em: 10 ago. 2026. (A)
- RAJAK, Shaik; NAGANABOINA, Venkata Ramesh; REDDY, G. Pradeep. *Model Context Protocol (MCP) and Agent-to-Agent (A2A) Protocol for Scalable Agentic AI Systems*. Disponível em: https://doi.org/10.1109/icicds70526.2026.11604962. Acesso em: 10 ago. 2026. (A)
- SILVA, L.; KÖCHER, Aljosha; GEHLHOFF, Felix. *Beyond Formal Semantics for Capabilities and Skills: Model Context Protocol in Manufacturing*. Disponível em: https://www.semanticscholar.org/paper/383684744f191c35bc07cfb11446cffbc6720c9e. Acesso em: 10 ago. 2026. (A)
- ZHANG, Dongsen et al. *MCP Security Bench (MSB): Benchmarking Attacks Against Model Context Protocol in LLM Agents*. Disponível em: https://www.semanticscholar.org/paper/bb33f9e07e661b52a6fade948f71d5a0e0bbc773. Acesso em: 10 ago. 2026. (A)
- WANG, Zihan et al. *MPMA: Preference Manipulation Attack Against Model Context Protocol*. Disponível em: https://www.semanticscholar.org/paper/b603506125f970db799d84fc9e1b5ce9b2a45162. Acesso em: 10 ago. 2026. (A)
- ZHOU, Zhenhong et al. *MCPShield: A Security Cognition Layer for Adaptive Trust Calibration in Model Context Protocol Agents*. Disponível em: https://www.semanticscholar.org/paper/862cf894d5234e55038e588326b0ed86eca878b3. Acesso em: 10 ago. 2026. (A)
- MODEL CONTEXT PROTOCOL. *Specification — Tools, Resources, Prompts*. Disponível em: https://modelcontextprotocol.io. Acesso em: 10 ago. 2026. (B)
- ANTHROPIC. *Agent Skills — Overview*. Disponível em: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview. Acesso em: 10 ago. 2026. (B)
- ANTHROPIC. *Equipping agents for the real world with Agent Skills*. Disponível em: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills. Acesso em: 10 ago. 2026. (B)
- ANTHROPIC. *Writing effective tools for agents — with agents*. Disponível em: https://www.anthropic.com/engineering/writing-tools-for-agents. Acesso em: 10 ago. 2026. (B)
- OPENAI. *Model Context Protocol — Codex*. Disponível em: https://developers.openai.com/codex/mcp. Acesso em: 10 ago. 2026. (B)
