# 3 Resultados e Discussão

## 3.1 Harness: settings.json, hooks e permissions como camadas de controle

O arquivo `.claude/settings.json` funciona como painel único de decisão do harness: controla qual modelo roda, quais comandos de shell são permitidos, quais servidores MCP se conectam, quais hooks disparam em edições de arquivo e quais variáveis de ambiente são injetadas em cada chamada de shell (EXPLAINX, 2026). Permissões são expressas como arrays `allow`, `deny` e `ask`, com padrões granulares como `Bash(git add:*)`, `WebSearch` ou `SlashCommand(/run-prompt:*)` — a aplicação decide o que é permitido antes de qualquer execução, independentemente do que o modelo tenta (KONISHI, 2026). Hooks são definidos em três níveis de aninhamento: um evento ao qual responder (`PreToolUse`, `Stop`), um grupo de correspondência (*matcher*) que filtra quando o hook dispara e um ou mais manipuladores que rodam na correspondência, recebendo a entrada via stdin (hooks de comando) ou como corpo de requisição POST (hooks HTTP) (EXPLAINX, 2026).

A camada de hooks resolve um problema que permissions sozinhas não resolvem: confiar em um `deny` de padrão de string exata como antepara final ignora que variações de espaçamento, encadeamento de comandos ou um alias de shell podem produzir um comando funcionalmente idêntico sem bater no padrão declarado — só um hook que inspeciona o comando resolvido no momento da execução corrige essa lacuna de fato (GENERAL, 2026). Por isso, a literatura descreve a segurança do harness como estrutura multicamadas: permissions como aplicação diária, *managed settings* como política corporativa, hooks como aplicação determinística e controles de MCP como governança de ferramentas, na mesma lógica de "acesso mínimo, observação constante, dupla checagem" com que se trataria um agente de IA como um novo funcionário júnior com acesso root (GENERAL, 2026). Guias independentes de arquitetura de harness convergem no mesmo ponto: o harness decide o que é permitido, o modelo decide apenas o que tentar, e a diferença entre as duas coisas é onde vive todo o risco operacional (MINDSTUDIO, 2026; AIMULTIPLE, 2026).

## 3.2 Tools e servidores MCP: schemas e blindagem contra tool poisoning

Ferramentas no padrão de *tool use* da Claude API expõem um `input_schema` em JSON Schema; quando o modelo decide usar uma ferramenta, retorna um `tool_use` e a aplicação executa a operação, devolvendo um `tool_result` (ANTHROPIC, 2026). Para servidores MCP construídos em FastMCP (Python) ou no MCP SDK (Node/TypeScript), a orientação predominante é equilibrar cobertura abrangente de endpoints de API com ferramentas de fluxo de trabalho especializadas, evitando expor um número excessivo de operações granulares que aumentam a superfície de decisão — e de ataque — do agente (MODEL, 2026). Validação de todas as saídas de chamadas de função antes da execução e *schema validation* para capturar incompatibilidades de tipo são práticas obrigatórias; *rate limiting* previne chamadas de função descontroladas, e operações sensíveis exigem aprovação humana ou regras de validação determinísticas independentes do raciocínio do modelo (APTIBLE, 2026).

O *MCP Tool Poisoning* é o ataque de referência documentado nesse domínio: diferente da injeção de prompt tradicional, a poluição de ferramentas embute instruções diretamente na descrição da ferramenta, injetando-as no contexto do modelo durante a fase de registro do MCP e influenciando a decisão do agente antes de qualquer chamada real (OWASP, 2026). A Microsoft descreve o mesmo padrão como vulnerabilidade estrutural do protocolo, recomendando validação de proveniência de servidores MCP e sandboxing de execução (MICROSOFT, 2026). Willison (2026) argumenta que a combinação, num único agente, de acesso a dados privados, exposição a conteúdo não confiável e capacidade de comunicação externa constitui uma "trifecta letal" que nenhum schema de ferramenta, por si só, neutraliza — a defesa exige também isolamento de rede, permissões mínimas por ferramenta e revisão humana de descrições de MCP antes da instalação, prática recomendada tanto pela Cloud Security Alliance quanto por relatos independentes de exploração real de chamadas de função em agentes de produção (CLOUD, 2026; SENTRY, 2026).

## 3.3 Economia severa de tokens como disciplina de contexto

A terceira camada de resultados trata de um problema distinto, mas estruturalmente acoplado às duas primeiras: o custo de operar agentes de codificação em escala é dominado pelo processamento de contexto, não pela geração de texto em si — quanto mais específica a tarefa, mais contexto estranho pode ser cortado, princípio que fundamenta técnicas de compressão como `headroom` (compressão de logs e saídas de comando) e `caveman` (comunicação telegráfica sem perda de precisão técnica) (ANTHROPIC, 2026). O framework acadêmico *SkillReducer* propõe otimizar *skills* de agentes especificamente para eficiência de token, e o paper "The Efficiency Frontier" formaliza um framework unificado de otimização custo-desempenho para gerenciamento de contexto em LLMs — ambos sustentam teoricamente práticas como `rtk-memory`, o registro de padrões e erros para evitar retrabalho de descoberta (ARXIV, 2026).

Sobre busca em código, a literatura observa que, durante a fase de exploração, um agente precisa de geração de hipóteses de cobertura ampla, não de resolução precisa de símbolos: grep retorna um cluster de conceitos a partir do qual o modelo infere organização de repositório e convenções de nomenclatura, com custo de token pago a cada resultado despejado na janela de contexto — o princípio que fundamenta `lean-ctx` (grep antes de leitura integral) (AGENTA, 2026). O *context engineering* trata a janela de contexto como disciplina central: retrieval ranqueado, filtragem de distintividade semântica e *compaction* de contexto — sumarizar histórico quando a sessão se aproxima do limite da janela, preservando detalhes críticos e descartando saídas redundantes — são técnicas já em uso na própria engenharia de agentes de longa duração (ANTHROPIC, 2026; REDIS, 2026). O paralelo com as camadas anteriores é direto: assim como permissions e hooks formam anteparas redundantes contra execução indevida, e schemas e revisão humana formam anteparas contra tool poisoning, as técnicas de economia de tokens formam anteparas contra o colapso econômico de sessões agênticas estendidas — sem elas, o mesmo agente que hoje é auditável e seguro se torna operacionalmente inviável em escala (TOTALUM, 2026).

## 3.4 Do zero ao deploy: portão de aprovação humana no CI/CD

A quarta camada fecha o ciclo no ponto de maior consequência: o deploy em produção. Práticas de segurança recomendadas incluem credenciais de curta duração e privilégio mínimo para agentes, limite de gasto de tokens, e a manutenção de um portão de aprovação humana entre as mudanças de código do agente e o deploy em produção — o agente abre o *pull request*, o CI valida, um humano aprova o *merge*, e o pipeline de deploy dispara automaticamente; o agente nunca faz deploy direto em produção sem revisão humana (DEPLOYHQ, 2026). Relatos documentados de equipes técnicas — DeployHQ, Spacelift e Teamvoy — descrevem pipelines reais com agentes revisando *pull requests*, reparando testes e disparando remediação de segurança, sempre com esse portão de aprovação antes de produção (SPACELIFT, 2026; TEAMVOY, 2026).

Os riscos que justificam esse portão não são hipotéticos: alucinação de correções, repetição de ações, comportamento não determinístico e introdução de vulnerabilidades de segurança tornam testes em sandbox, limiares de confiança, *guardrails* operacionais e monitoramento contínuo essenciais, não opcionais (RESEARCHGATE, 2026). O paper "GitInject" documenta ataques reais de injeção de prompt em pipelines de CI/CD alimentados por IA, explorando dados de repositório — títulos de *pull request*, *issues*, comentários — como vetor, o que reforça que o mesmo raciocínio de blindagem contra tool poisoning discutido na Seção 3.2 se aplica, sem exceção, aos metadados que o pipeline de CI/CD injeta no contexto do agente (ARXIV, 2026). Adoção corporativa documentada — Fujitsu automatizando o SDLC completo, e um caso de referência combinando Azure e GitHub Actions — reforça que esse padrão de portão de aprovação humana já é prática de mercado, não recomendação teórica isolada (FUJITSU, 2026; FORRESTER, 2026).

## 3.5 Síntese integrativa

Lidos em conjunto, os quatro pilares formam uma única pilha de governança: harness (permissions e hooks) decide o que é permitido na sessão; tools e MCP (schemas e blindagem) decidem o que é seguro invocar; economia de tokens decide o que é sustentável manter em contexto; e o portão de CI/CD decide o que é aceitável levar a produção. Nenhuma camada substitui a outra — a ausência de qualquer uma delas reabre exatamente a lacuna que as demais foram desenhadas para fechar, achado que se sustenta de forma consistente em toda a literatura revisada neste recorte (HUMANLAYER, 2026; GENERAL, 2026).

## Referências Bibliográficas

EXPLAINX, 2026. *Claude Code settings.json: Every Option Explained*. Disponível em: https://www.explainx.ai/blog/claude-code-settings-json-complete-reference-2026. Acesso em: 02 ago. 2026.

KONISHI, Hidekazu, 2026. *Claude Code Features and Settings Reference 2026*. Disponível em: https://hidekazu-konishi.com/entry/claude_code_features_settings_reference_2026.html. Acesso em: 02 ago. 2026.

GENERAL, 2026. *Anthropic Claude Code Security Best Practices: Permissions, Hooks, MCP, Sandboxing, and CI/CD*. General Analysis. Disponível em: https://generalanalysis.com/guides/anthropic-claude-code-security-best-practices. Acesso em: 02 ago. 2026.

MINDSTUDIO, 2026. *What Is an Agent Harness? The Architecture Behind Claude Code, Codex, and Cursor*. Disponível em: https://www.mindstudio.ai/blog/what-is-agent-harness-architecture-explained. Acesso em: 02 ago. 2026.

AIMULTIPLE, 2026. *Top Agent Harnesses: Claude Code vs Codex*. Disponível em: https://aimultiple.com/agent-harness. Acesso em: 02 ago. 2026.

ANTHROPIC, 2026. *Effective harnesses for long-running agents*. Disponível em: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents. Acesso em: 02 ago. 2026.

MODEL, 2026. *Specification and documentation for the Model Context Protocol*. Model Context Protocol. Disponível em: https://github.com/modelcontextprotocol/modelcontextprotocol. Acesso em: 02 ago. 2026.

APTIBLE, 2026. *Prompt Injection in MCP: Tool Poisoning and Blast Radius*. Disponível em: https://www.aptible.com/mcp-security/mcp-prompt-injection. Acesso em: 02 ago. 2026.

OWASP, 2026. *MCP Tool Poisoning*. Disponível em: https://owasp.org/www-community/attacks/MCP_Tool_Poisoning. Acesso em: 02 ago. 2026.

MICROSOFT, 2026. *Protecting against indirect prompt injection attacks in MCP*. Disponível em: https://developer.microsoft.com/blog/protecting-against-indirect-injection-attacks-mcp/. Acesso em: 02 ago. 2026.

WILLISON, Simon, 2026. *Model Context Protocol has prompt injection security problems*. Disponível em: https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/. Acesso em: 02 ago. 2026.

CLOUD, 2026. *Agentic MCP Security Best Practices Guide*. Cloud Security Alliance. Disponível em: https://labs.cloudsecurityalliance.org/agentic/agentic-mcp-security-best-practices-v1/. Acesso em: 02 ago. 2026.

SENTRY, 2026. *Exploiting Tool and Function Calling in LLM Agents*. Disponível em: https://blog.sentry.security/exploiting-tool-and-function-calling-in-llm-agents/. Acesso em: 02 ago. 2026.

ARXIV, 2026. *GitInject: Real-World Prompt Injection Attacks in AI-Powered CI/CD Pipelines*. Disponível em: https://arxiv.org/pdf/2606.09935. Acesso em: 02 ago. 2026.

AGENTA, 2026. *Top techniques to Manage Context Lengths in LLMs*. Disponível em: https://agenta.ai/blog/top-6-techniques-to-manage-context-length-in-llms. Acesso em: 02 ago. 2026.

REDIS, 2026. *Context Window Overflow in 2026: Fix LLM Errors Fast*. Disponível em: https://redis.io/blog/context-window-overflow/. Acesso em: 02 ago. 2026.

TOTALUM, 2026. *Claude Code subagents: the 2026 production playbook*. Disponível em: https://www.totalum.app/blog/claude-code-subagents-totalum. Acesso em: 02 ago. 2026.

DEPLOYHQ, 2026. *AI Agents in CI/CD Pipelines: From GitHub Issue to Production Deploy*. Disponível em: https://www.deployhq.com/blog/ai-agents-cicd-pipelines-github-issue-to-production-deploy. Acesso em: 02 ago. 2026.

SPACELIFT, 2026. *Where Do AI Agents Fit in CI/CD Pipelines?*. Disponível em: https://spacelift.io/blog/agentic-cicd. Acesso em: 02 ago. 2026.

TEAMVOY, 2026. *AI Agents in CI/CD Pipelines: A Guide for Tech Leads*. Disponível em: https://teamvoy.com/blog/building-ai-agents-into-your-ci-cd-pipeline-a-playbook-for-tech-leads/. Acesso em: 02 ago. 2026.

RESEARCHGATE, 2026. *AI-First Software Development Lifecycle: An Agent-Driven Framework for Autonomous Planning, Coding, Testing, and Deployment*. Disponível em: https://www.researchgate.net/publication/403670772_AI-First_Software_Development_Lifecycle_An_Agent-Driven_Framework_for_Autonomous_Planning_Coding_Testing_and_Deployment. Acesso em: 02 ago. 2026.

FUJITSU, 2026. *Fujitsu automates entire software development lifecycle with new AI-Driven Software Development Platform*. Disponível em: https://global.fujitsu/en-global/pr/news/2026/02/17-01. Acesso em: 02 ago. 2026.

FORRESTER, 2026. *Agentic Software Development Takes The Lead: From Code Assistants To Orchestrated SDLC Agents*. Disponível em: https://www.forrester.com/blogs/agentic-software-development-takes-the-lead-from-code-assistants-to-orchestrated-sdlc-agents/. Acesso em: 02 ago. 2026.

HUMANLAYER, 2026. *12-Factor Agents — Principles for Building Reliable LLM Applications*. Disponível em: https://www.humanlayer.dev/12-factor-agents. Acesso em: 02 ago. 2026.
