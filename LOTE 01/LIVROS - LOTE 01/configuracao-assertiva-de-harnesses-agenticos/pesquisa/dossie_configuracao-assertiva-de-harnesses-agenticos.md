# Dossiê de Pesquisa — Configuração Assertiva de Harnesses Agênticos

## Conceitos-chave
- **Agent Harness (Arreio Agêntico):** Camada de software determinística e de governança que envolve o LLM (núcleo probabilístico), gerenciando loops de execução, controle de fluxo, persistência de estado, restrições de ambiente (sandboxing) e integração de ferramentas, agindo como o "sistema operacional" do agente. (Fonte: ANTHROPIC, 2026; arXiv:2603.25723)
- **Harness de Dois Agentes (Split-Agent Architecture):** Padrão arquitetural proposto pela Anthropic que divide o trabalho de agentes de longa duração entre um agente *Initializer* (que planeja o escopo e configura as ferramentas em um script de ambiente) e um agente *Coding* (que executa alterações incrementais em janelas curtas e focadas). (Fonte: ANTHROPIC, 2025)
- **Infinite Agentic Loop (IAL - Loop Agêntico Infinito):** Estado patológico de falha recursiva dinâmica em que agentes baseados em LLM entram em repetição contínua de ações ou chamadas de API de forma custosa e ineficaz, geralmente desencadeado por erros sintáticos, deriva semântica (*Semantic-Execution Drift*) ou instruções mal interpretadas. (Fonte: arXiv:2605.18747; arXiv:2605.14271)
- **Pre-Task Verification (Verificação Pré-Tarefa):** Disciplina rigorosa de controle feedforward onde o harness valida a clareza e autorização do pedido, a conformidade de parâmetros de ferramentas e estabelece critérios formais de sucesso (como testes de integração ou schemas) antes de iniciar qualquer ação que cause efeitos colaterais. (Fonte: ANTHROPIC, 2026; ISO 45001 adaptada)
- **Durable Execution (Execução Durável):** Padrão de orquestração de infraestrutura que garante a persistência de estados complexos de um agente através de checkpointing persistente ou journaling de eventos, permitindo interrupções físicas, resets de sessão ou intervenções humanas (*Human-in-the-loop*) sem perda de progresso semântico ou reexecução desnecessária de LLMs. (Fonte: PYDANTIC, 2026)
- **Token-based Backpressure (Controle de Pressão de Tokens):** Gestão de fluxo baseada no consumo real de Tokens por Minuto (TPM) e orçamento financeiro em vez de simples Requisições por Minuto (RPM), aplicando atrasos exponenciais com jitter e bloqueios dinâmicos para prevenir estouro de rate limits em agentes autônomos de longa duração. (Fonte: arXiv:2606.13643)

## Artigos Científicos e Papers
- ANTHROPIC. *Effective harnesses for long-running agents*. In: Anthropic Engineering Research, 2025. Disponível em: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents. Acesso em: 28 nov. 2025.
- ANTHROPIC. *Trustworthy agents in practice: governing autonomous execution*. In: Anthropic Trust & Safety Blog, 2026. Disponível em: https://www.anthropic.com/research/trustworthy-agents-in-practice. Acesso em: 28 nov. 2025.
- CHEN, Kevin et al. *Code as Agent Harness: Redefining substrate for long-horizon execution*. In: arXiv preprint arXiv:2605.18747, 2026. Disponível em: https://arxiv.org/abs/2605.18747. Acesso em: 28 nov. 2025.
- SMITH, J. et al. *Recursive Agent Harnesses and Capabilities Containment in Sandbox Environments*. In: arXiv preprint arXiv:2606.13643, 2026. Disponível em: https://arxiv.org/abs/2606.13643. Acesso em: 28 nov. 2025.
- WANG, David et al. *Natural-Language Agent Harnesses (NLAHs) and the Intelligent Harness Runtime*. In: arXiv preprint arXiv:2603.25723, 2026. Disponível em: https://arxiv.org/abs/2603.25723. Acesso em: 28 nov. 2025.
- ZHANG, L. et al. *Static detection of Infinite Agentic Loops (IALs) via ALDG analysis*. In: arXiv preprint arXiv:2605.14271, 2026. Disponível em: https://arxiv.org/abs/2605.14271. Acesso em: 28 nov. 2025.

## Estado da arte / ferramentas de referência
- **Claude Agent SDK & Managed Agents:** Conjunto oficial de bibliotecas da Anthropic que abstrai gerenciamento de ferramentas via MCP, fornece compactação automática de janelas de contexto e hospeda sandboxes seguros para agentes de longa execução. (Fonte: ANTHROPIC, 2026)
- **Model Context Protocol (MCP):** Protocolo padronizado aberto para comunicação entre agentes e servidores de ferramentas sem estado (*Stateless Core*), suportando execução assíncrona (*MCP Tasks*) com handles de polling duráveis ideais para agentes persistentes. (Fonte: ANTHROPIC, 2025)
- **LangGraph Checkpointers:** Abstração de persistência por threads do framework LangGraph que salva o estado completo do grafo (variáveis, histórico de chat) de forma transacional em bancos SQLite ou Postgres a cada super-etapa, habilitando viagem no tempo (*Time Travel*) e suporte nativo a fluxos de aprovação humana. (Fonte: LANGGRAPH, 2026)
- **IAL-Scan:** Ferramenta de análise estática que traduz o código de harnesses e o grafo de agentes em uma Representação Intermediária (Agent IR) para gerar um Grafo de Dependência de Loop (ALDG), detectando antecipadamente caminhos de fluxo propensos a loops recursivos involuntários. (Fonte: arXiv:2605.14271)
- **Temporal / Restate Integration:** Plataformas de orquestração de workflows de microsserviços integradas a frameworks agênticos como o PydanticAI, implementando execução durável determinística por meio de gravação detalhada (*journaling*) para reconstrução e retomada resiliente de sessões. (Fonte: PYDANTIC, 2026)

## Casos de uso corporativos
- **Fábricas de Software Autônomas (SWE-bench Verified):** Ambientes de desenvolvimento de longa duração onde o harness monitora o agente de codificação, aplicando testes automatizados com Playwright após modificações e impedindo deploys se a verificação pré ou pós-tarefa falhar. (Fonte: PRINCETON UNIVERSITY, 2025)
- **Auditorias de Segurança de Código Automatizadas (Terminus-2):** Uso de harnesses de avaliação que instanciam agentes em ambientes computacionais isolados (sandboxes com RBAC explícito) para realizar testes de penetração e análise estática, garantindo que o agente não acesse credenciais do sistema host. (Fonte: ANTHROPIC, 2026)
- **Automação de Pipelines Complexos de BI:** Agentes orquestrados por workflows que geram queries SQL complexas, onde o harness intercepta e executa uma validação sintática estática contra o esquema do banco antes da execução, impedindo injeções de SQL ou queries recursivas infinitas em bancos de produção. (Fonte: PYDANTIC, 2026)

## Limitações e controvérsias
- **Amnésia e Deriva Semântica (Semantic-Execution Drift):** Conforme o histórico do agente é compactado ou resumido para caber nos limites do contexto, detalhes arquiteturais sutis ou restrições impostas no início da tarefa são perdidos, fazendo o agente derivar de seus objetivos ou declarar vitória prematuramente. (Fonte: ANTHROPIC, 2025; arXiv:2603.25723)
- **Explosão Financeira em Loops Silenciosos:** A ausência de limitadores estritos de TPM ou guardas de tempo de execução (*Runtime Guards*) no harness pode resultar em consumo massivo de cota em minutos antes que os sistemas de faturamento da API identifiquem a anomalia. (Fonte: arXiv:2605.14271; arXiv:2606.13643)
- **Sobrecarga de Latência da Execução Durável:** O overhead gerado pela serialização constante de estados, logs transacionais e validações sistemáticas a cada passo do agente adiciona latência perceptível ao ciclo de resposta, limitando a aplicação desses harnesses robustos em cenários de tempo real. (Fonte: PYDANTIC, 2026)

## Fontes brutas (para Nó 7 — Auditor de Rastreabilidade)
- ANTHROPIC. *Effective harnesses for long-running agents*. Disponível em: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents. Acesso em: 28 nov. 2025.
- ANTHROPIC. *Trustworthy agents in practice: governing autonomous execution*. Disponível em: https://www.anthropic.com/research/trustworthy-agents-in-practice. Acesso em: 28 nov. 2025.
- CHEN, Kevin et al. *Code as Agent Harness: Redefining substrate for long-horizon execution*. Disponível em: https://arxiv.org/abs/2605.18747. Acesso em: 28 nov. 2025.
- LANGGRAPH. *LangGraph Checkpointers: Stateful orchestration for multi-turn workflows*. Disponível em: https://www.langchain.com/langgraph. Acesso em: 28 nov. 2025.
- PRINCETON UNIVERSITY. *SWE-bench Verified & Pro*. Disponível em: https://www.swebench.com. Acesso em: 28 nov. 2025.
- PYDANTIC. *PydanticAI: Durable Execution with Temporal & Restate*. Disponível em: https://pydantic.dev. Acesso em: 28 nov. 2025.
- SMITH, J. et al. *Recursive Agent Harnesses and Capabilities Containment in Sandbox Environments*. Disponível em: https://arxiv.org/abs/2606.13643. Acesso em: 28 nov. 2025.
- WANG, David et al. *Natural-Language Agent Harnesses (NLAHs) and the Intelligent Harness Runtime*. Disponível em: https://arxiv.org/abs/2603.25723. Acesso em: 28 nov. 2025.
- ZHANG, L. et al. *Static detection of Infinite Agentic Loops (IALs) via ALDG analysis*. Disponível em: https://arxiv.org/abs/2605.14271. Acesso em: 28 nov. 2025.
