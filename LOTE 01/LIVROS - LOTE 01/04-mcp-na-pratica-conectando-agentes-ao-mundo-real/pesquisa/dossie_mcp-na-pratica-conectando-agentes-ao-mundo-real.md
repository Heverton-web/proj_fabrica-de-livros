# Dossiê de Pesquisa — Livro 4 "A Pilha Agêntica"

**Obra:** *MCP na prática: conectando agentes ao mundo real*
**Slug:** `livros/mcp-na-pratica-conectando-agentes-ao-mundo-real`
**Data:** 5 de agosto de 2026

---

## 1. Fontes Autoritativas (22)

1. **ANTHROPIC.** *Introducing the Model Context Protocol*. Anthropic News, 25 nov. 2024. Disponível em: https://www.anthropic.com/news/model-context-protocol. Acesso em: 5 ago. 2026.
2. **MODEL CONTEXT PROTOCOL.** *Architecture*. MCP Specification 2025-11-25, 25 nov. 2025. Disponível em: https://modelcontextprotocol.io/specification/2025-11-25/architecture. Acesso em: 5 ago. 2026.
3. **MODEL CONTEXT PROTOCOL.** *Basic Specification: Transports*. MCP Specification 2025-11-25, 2025. Disponível em: https://modelcontextprotocol.io/specification/2025-11-25/basic/transports. Acesso em: 5 ago. 2026.
4. **MODEL CONTEXT PROTOCOL.** *Specification 2026-07-28: Server Tools*. MCP Specification, 28 jul. 2026. Disponível em: https://modelcontextprotocol.io/specification/2026-07-28/server/tools. Acesso em: 5 ago. 2026.
5. **MODEL CONTEXT PROTOCOL.** *Specification 2026-07-28: Server Resources*. MCP Specification, 28 jul. 2026. Disponível em: https://modelcontextprotocol.io/specification/2026-07-28/server/resources. Acesso em: 5 ago. 2026.
6. **MODEL CONTEXT PROTOCOL.** *Security Best Practices (Draft)*. MCP Specification. Disponível em: https://modelcontextprotocol.io/specification/draft/basic/security_best_practices. Acesso em: 5 ago. 2026.
7. **MODEL CONTEXT PROTOCOL.** *TypeScript SDK*. GitHub Repository, 2026. Disponível em: https://github.com/modelcontextprotocol/typescript-sdk. Acesso em: 5 ago. 2026.
8. **MODEL CONTEXT PROTOCOL.** *Python SDK*. GitHub Repository, 2026. Disponível em: https://github.com/modelcontextprotocol/python-sdk. Acesso em: 5 ago. 2026.
9. **MODEL CONTEXT PROTOCOL.** *TypeScript SDK Documentation*. MCP SDK Portal, 2026. Disponível em: https://ts.sdk.modelcontextprotocol.io/. Acesso em: 5 ago. 2026.
10. **MODEL CONTEXT PROTOCOL.** *Python SDK Documentation*. MCP SDK Portal, 2026. Disponível em: https://py.sdk.modelcontextprotocol.io/. Acesso em: 5 ago. 2026.
11. **MODEL CONTEXT PROTOCOL.** *Quickstart Guide*. MCP Documentation. Disponível em: https://modelcontextprotocol.io/docs/quickstart/quickstart. Acesso em: 5 ago. 2026.
12. **MODEL CONTEXT PROTOCOL.** *MCP Registry Preview*. Official MCP Blog, 8 set. 2025. Disponível em: https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/. Acesso em: 5 ago. 2026.
13. **MODEL CONTEXT PROTOCOL.** *Registry Repository*. GitHub Repository, 2025–2026. Disponível em: https://github.com/modelcontextprotocol/registry. Acesso em: 5 ago. 2026.
14. **GITHUB.** *GitHub MCP Registry: the fastest way to discover AI tools*. GitHub Changelog, 16 set. 2025. Disponível em: https://github.blog/changelog/2025-09-16-github-mcp-registry-the-fastest-way-to-discover-ai-tools/. Acesso em: 5 ago. 2026.
15. **CLOUD SECURITY ALLIANCE.** *Agentic MCP Security Best Practices Guide v1*. CSA Labs, 27 mar. 2026. Disponível em: https://labs.cloudsecurityalliance.org/agentic/agentic-mcp-security-best-practices-v1/. Acesso em: 5 ago. 2026.
16. **INVARIANT LABS.** *MCP Security Notification: Tool Poisoning Attacks*. Invariant Labs Blog, 1 abr. 2025. Disponível em: https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks. Acesso em: 5 ago. 2026.
17. **WILLISON, Simon.** *Model Context Protocol has prompt injection security problems*. Simon Willison's Weblog, 9 abr. 2025. Disponível em: https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/. Acesso em: 5 ago. 2026.
18. **WANG, Zhen et al. (Tsinghua University & Ant Group).** *Systematic Analysis of MCP Security (MCPLib)*. arXiv:2508.12538, 18 ago. 2025. Disponível em: https://arxiv.org/html/2508.12538v1. Acesso em: 5 ago. 2026.
19. **CISA.** *Guide to Secure Adoption of Agentic AI*. CISA News, 1 mai. 2026. Disponível em: https://www.cisa.gov/news-events/news/cisa-us-and-international-partners-release-guide-secure-adoption-agentic-ai. Acesso em: 5 ago. 2026.
20. **CENTER FOR INTERNET SECURITY (CIS).** *Model Context Protocol (MCP) Companion Guide — CIS Controls v8.1*. CIS White Papers, 20 abr. 2026. Disponível em: https://www.cisecurity.org/insights/white-papers/controls-v8-1-model-context-protocol-companion-guide. Acesso em: 5 ago. 2026.
21. **NATIONAL SECURITY AGENCY (NSA).** *Security Design Considerations for AI-Driven Automation Leveraging the Model Context Protocol*. NSA Press Release, 20 mai. 2026. Disponível em: https://www.nsa.gov/Press-Room/Press-Releases-Statements/Press-Release-View/Article/4496698/. Acesso em: 5 ago. 2026.
22. **PULSEMCP.** *MCP Server Directory*. PulseMCP, 2025–2026. Disponível em: https://www.pulsemcp.com/servers. Acesso em: 5 ago. 2026.

## 2. Síntese dos Eixos Temáticos

### Eixo 1 — Arquitetura MCP: host, client, server (MCP Specification, 2025–2026)
O Model Context Protocol define um padrão aberto para integrar agentes de IA a ferramentas e dados externos:
- **Host:** processo contêiner que coordena aplicações como o Claude Desktop ou IDEs de IA; gerencia múltiplas instâncias de cliente, políticas de autorização e ciclo de vida das conexões.
- **Client:** wrapper de conexão 1:1 com um servidor MCP, mantendo sessão stateful e roteando mensagens JSON-RPC 2.0 bidirecionais sem expor o histórico da conversa fora do contexto designado.
- **Server:** processo local ou serviço remoto que expõe capacidades e dados via primitivas padronizadas.
- **Três primitivas:** Tools (funções executáveis controladas pelo modelo), Resources (dados endereçados por URI, app-driven) e Prompts (modelos de mensagem reutilizáveis).

### Eixo 2 — Transportes e versões da especificação
- **stdio:** transporte padrão para integrações locais; o cliente lança o servidor como subprocesso e troca mensagens JSON-RPC 2.0 delimitadas por nova linha via stdin/stdout.
- **Streamable HTTP:** substituiu o legado HTTP+SSE a partir da versão 2024-11-05; endpoint unificado com POST (JSON-RPC) e GET (Server-Sent Events), sessões via header `MCP-Session-Id`, resumibilidade via `Last-Event-ID` e validação de `Origin` contra ataques de DNS rebinding.
- Especificações evolutivas: 2024-11-05 → 2025-11-25 → 2026-07-28 (linha estável v2 dos SDKs).

### Eixo 3 — Construindo servidores MCP do zero
- **TypeScript:** SDK oficial sob a organização `modelcontextprotocol` no GitHub; documentação com tutorial de servidor em dez minutos; adaptadores finos opcionais (`@modelcontextprotocol/express`, `@modelcontextprotocol/hono`).
- **Python:** SDK oficial instalável via `pip install "mcp[cli]"` ou `uv add "mcp[cli]"`; anotações de tipo Python atuam diretamente como schemas de validação (sem boilerplate de JSON Schema).
- **Quickstart oficial:** servidor de clima expondo ferramentas `get-alerts` e `get-forecast` contra a National Weather Service API, conectado a um host como o Claude Desktop.

### Eixo 4 — Consumindo servidores existentes: registro e ecossistema
- **Registro oficial MCP** (preview em 8 set. 2025, apoiado por Anthropic, GitHub, Microsoft e PulseMCP): catálogo upstream de servidores públicos; GitHub anunciou o GitHub MCP Registry em 16 set. 2025.
- **Ecossistema:** PulseMCP (22.000+ servidores em meados de 2026), Glama, MCP.so e Smithery (hosting/deploy de servidores comunitários).
- Grande provedores mantêm servidores oficiais: Google Cloud (BigQuery), AWS (documentação), entre outros.

### Eixo 5 — Segurança MCP: least-privilege, OAuth, audit logging, RBAC
- **Least privilege:** tokens e capacidades de ferramentas com escopo mínimo; servidores só aceitam tokens emitidos para seu público específico (mitigação de reuso/passthrough).
- **Autorização:** OAuth 2.1 com PKCE obrigatório para conexões remotas; mitigação de confused deputy com validação de consentimento por cliente, redirect URI com match exato e `state` criptograficamente seguro.
- **Proibição de token passthrough:** servidores não podem aceitar tokens upstream e repassá-los a APIs de terceiros sem verificação de audiência e validação local.
- **Audit logging:** registro de todas as invocações de ferramentas, decisões de política e mudanças de contexto, retido por mínimo de 90 dias em frameworks empresariais.
- **CIS Companion Guide (abr. 2026):** aplicação dos CIS Controls v8.1 a implantações MCP — identidade, controle de acesso, logging e segurança de aplicação.

### Eixo 6 — Riscos documentados (porta de entrada não revisada)
- **Prompt injection via MCP:** LLMs não distinguem comandos do usuário, dados da aplicação e instruções embutidas em saídas/descrições de ferramentas (Willison, 2025).
- **Tool Poisoning Attacks (Invariant Labs, abr. 2025):** instruções adversárias escondidas em descrições de ferramentas (tags `<IMPORTANT>`, comentários de código) que induzem o modelo a executar ações não autorizadas e exfiltrar dados por argumentos não usados.
- **Cross-server tool shadowing:** servidores maliciosos injetam instruções que sequestram ferramentas confiáveis em contexto compartilhado.
- **SSRF:** servidores remotos maliciosos retornam URLs em endpoints de descoberta OAuth apontando para redes internas (`192.168.x.x`) ou metadados de nuvem (`169.254.169.254`).
- **CVE-2025-6514 (JFrog):** RCE pré-autenticação (CVSS 9.6) no pacote `mcp-remote` — `authorization_endpoint` não validado passado a execução de shell.
- **MCPLib (Tsinghua/Ant Group, ago. 2025):** taxonomia com 31 tipos de ataque MCP (injeção direta/indireta de ferramentas, ataques de usuários maliciosos e exploits inerentes ao LLM).
- **Local server compromise:** binários locais herdam privilégios do cliente; sem sandboxing podem exfiltrar arquivos sensíveis (`~/.ssh/id_rsa`).

### Eixo 7 — MCP Engineering como disciplina
- Decisão central: **o que expor, com que granularidade e com que controle de acesso** — a superfície de ataque do agente é a soma das ferramentas conectadas.
- Esquemas least-privilege: expor o menor conjunto de ferramentas com os menores escopos necessários à tarefa.
- Três fronteiras de confiança (CSA, 2026): LLM↔Client, Client↔Server, Server↔Sistemas downstream — cada uma com controles próprios.
- Guias governamentais: CISA (mai. 2026) integra agentic AI a Zero Trust; NSA (mai. 2026) recomenda isolamento em runtime, atestação e enforcement de fronteiras.

## 3. Métricas de mercado (2026)
- PulseMCP cataloga 22.000+ servidores MCP (meados de 2026), refletindo adoção massiva e superfície de ataque crescente.
- Ataques de tool poisoning demonstrados em ferramentas reais (Cursor, Claude Desktop) com exfiltração prática (Invariant Labs, abr. 2025).
- O pacote `mcp-remote` atingia 437.000+ ambientes de instalação quando a CVE-2025-6514 (CVSS 9.6) foi divulgada.
