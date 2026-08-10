# 5 Sistemas Multiagentes e Protocolos de Interoperabilidade

## 5.1 Do agente isolado à colaboração entre agentes

A trajetória da engenharia de software dirigida por inteligência artificial (IA) iniciou-se com agentes individuais capazes de planejar, navegar em repositórios, editar arquivos, executar comandos e validar resultados de forma iterativa (YANG et al., 2024). À medida que esses sistemas amadureceram, contudo, tornou-se evidente que um único agente, por mais capaz que seja, opera com horizontes limitados: seu contexto é finito, sua especialidade é restrita e sua capacidade de verificação é parcial. A resposta natural a essa limitação foi a coordenação — múltiplos agentes colaborando sob diferentes papéis, trocando mensagens e compartilhando artefatos (HONG et al., 2024; DONG et al., 2025).

A distinção entre automação monolítica e colaboração multiagente não é meramente quantitativa. Um agente único executa um pipeline linear de percepção-planejamento-ação; um sistema multiagente introduz concorrência de perspectivas, revisão cruzada e especialização funcional. Essa diferença estrutural aproxima o processo de produção de software do modelo organizacional humano, no qual papéis como arquiteto, implementador, testador e revisor operam em paralelo e se interdependem (HONG et al., 2024). A literatura sobre agentes LLM mostra que a decomposição de tarefas complexas em subagentes com responsabilidades bem definidas tende a melhorar a aderência às instruções e a qualidade dos artefatos produzidos, ao custo de maior sobrecarga de comunicação e de orquestração (DONG et al., 2025; GUO et al., 2025).

## 5.2 Arquiteturas de orquestração: o caso MetaGPT

Entre as arquiteturas multiagentes propostas, o MetaGPT é a referência mais citada. O sistema decompõe a produção de software na sequência clássica de fases — análise de requisitos, design, implementação, teste e documentação — e atribui cada fase a um agente especializado: product manager, arquiteto, engenheiro de software e gerente de projeto (HONG et al., 2024). O diferencial do MetaGPT reside na comunicação estruturada: em vez de trocar mensagens de texto livre, os agentes publicam artefatos intermediários em uma "linha de montagem" de documentos, incluindo requisitos, diagramas de arquitetura e especificações de interfaces. A codificação de procedimentos organizacionais em templates — o chamado "meta-programming" — reduz a ambiguidade das mensagens e confere aos agentes um repositório compartilhado de conhecimento de domínio (HONG et al., 2024).

Os resultados reportados indicam que, em tarefas de benchmark, a abordagem multiagente do MetaGPT supera pipelines de geração única de código, sobretudo quando a tarefa exige múltiplas etapas de refinamento (HONG et al., 2024). É importante, porém, situar esses resultados: os ganhos concentram-se em problemas de escopo médio, nos quais a decomposição em subtarefas é viável e mensurável. Em tarefas abertas de engenharia de software real, a vantagem comparativa dos sistemas multiagentes permanece tema de debate, pois a orquestração adiciona latência e custo de tokens que precisam ser compensados por ganhos efetivos de qualidade (XIA et al., 2025; GUO et al., 2025).

## 5.3 Ciclos de reflexão e autocrítica entre agentes

A colaboração entre agentes não se limita à divisão de tarefas; envolve também mecanismos de autoavaliação e correção. O framework ReAct estabeleceu a base ao intercalar raciocínio e ação, permitindo que o agente observe os resultados de suas ações e revise seu plano (YAO et al., 2023). O Reflexion amplia esse princípio ao introduzir "memória verbal": após uma tentativa, o agente gera uma avaliação textual do próprio desempenho e a utiliza como insumo para a tentativa seguinte (SHINN et al., 2023). Em sistemas multiagentes, essa capacidade individual de reflexão é escalada para a revisão cruzada — um agente implementa, outro testa e um terceiro audita o resultado, em ciclo que se repete até o atendimento dos critérios de aceitação (HONG et al., 2024; DONG et al., 2025).

Há evidências de que ciclos de refinamento iterativo melhoram a corretude funcional, mas não a segurança. Estudo empírico demonstrou que cinco rodadas de refinamento com IA elevaram a proporção de vulnerabilidades críticas em aproximadamente 38% sobre código inicialmente seguro (Snyk, 2025). Esse resultado tem implicação direta para a arquitetura multiagente: a revisão cruzada melhora a conformidade com requisitos explícitos, porém tende a reforçar padrões de raciocínio já estabelecidos pelo modelo, incluindo falhas de segurança conhecidas. A validação, portanto, precisa ser assistida por ferramentas externas — analisadores estáticos, testes de segurança e revisão humana — e não apenas por outros agentes (PERRY et al., 2022; Snyk, 2025).

## 5.4 Protocolos de interoperabilidade entre agentes

A proliferação de agentes e de ferramentas criou um problema de integração: cada agente precisava de adaptadores proprietários para cada ferramenta, e a comunicação entre agentes de fornecedores distintos exigia acordos ad hoc. A padronização avançou por meio de protocolos abertos, analisados em revisão sistemática da literatura (NASCIMENTO et al., 2025):

O Model Context Protocol (MCP), proposto pela Anthropic, ataca a integração agente-ferramenta. O protocolo define um modelo cliente-servidor no qual o agente (cliente) descobre capacidades e invoca ferramentas expostas por servidores, com transporte padronizado e comunicação JSON-RPC. A adoção do MCP generalizou-se rapidamente: ambientes como Claude Code o utilizam nativamente, e o ecossistema de servidores MCP passou a incluir bancos de dados, sistemas de arquivos, navegadores e APIs corporativas (ANTHROPIC, 2025; NASCIMENTO et al., 2025).

O Agent Communication Protocol (ACP) ataca o problema complementar: a comunicação entre agentes, definindo mensagens estruturadas de diálogo, descoberta de capacidades e encerramento de sessões. O Agent-to-Agent Protocol (A2A) propõe interoperabilidade ponto a ponto com base em "cards de agente" — descrições declarativas de habilidades que permitem que um agente descubra e delegue tarefas a outro. O Agent Network Protocol (ANP) estende o modelo para redes distribuídas de agentes, com roteamento de mensagens entre nós heterogêneos (NASCIMENTO et al., 2025).

A coexistência desses protocolos reflete uma divisão natural de fronteiras: MCP para ferramentas, ACP para diálogo entre agentes, A2A para delegação e descoberta, e ANP para redes. A consolidação é incipiente, e a interoperabilidade plena — na qual um agente de um fornecedor delega tarefas a um agente de outro fornecedor com garantias de contrato — permanece objetivo de pesquisa mais do que realidade operacional (NASCIMENTO et al., 2025; TEQNOVOS, 2025).

## 5.5 Padrões emergentes e implicações para as equipes de desenvolvimento

A adoção corporativa de sistemas multiagentes já produziu padrões observáveis. A Stripe opera os "Minions", agentes autônomos em nuvem que executam tarefas de código com mínima intervenção humana; Amazon adota política de revisão obrigatória por engenheiro sênior para qualquer código gerado por IA; e Google e Microsoft reportam que cerca de 30% do código novo já é escrito ou assistido por IA (ALURA, 2026). Esses casos ilustram um espectro de governança: da autonomia supervisionada à revisão humana obrigatória, o grau de independência conferido aos agentes é uma decisão organizacional, não meramente técnica (STRAY et al., 2025; CUI et al., 2025).

No plano técnico, dois padrões se destacam. O primeiro é a adoção de plataformas abertas e extensíveis, como o OpenHands, que permitem integrar modelos, ferramentas e agentes customizados sob uma interface comum de execução (WANG et al., 2024). O segundo é o design de fluxos de trabalho "agentless" — pipelines determinísticos de planejamento e reparo que alcançam desempenho competitivo sem a complexidade de orquestração de agentes autônomos (XIA et al., 2025). A existência desse contraste reforça a lição central desta seção: a colaboração entre agentes deve ser introduzida quando a decomposição da tarefa e a especialização de papéis produzirem ganhos mensuráveis, e não como fim em si (DONG et al., 2025; GUO et al., 2025).

As implicações para equipes humanas são profundas. O engenheiro de software deixa de ser o executor único de tarefas e passa a atuar como especificador de fluxos de agentes, avaliador de artefatos e gestor de exceções (JIANG et al., 2025). A competência crítica desloca-se da escrita de código para a orquestração: saber quando delegar, como validar e onde intervir. Ao mesmo tempo, a rastreabilidade do processo exige instrumentação: logs de decisão, versões de prompts, trilhas de ferramentas invocadas e métricas de custo por tarefa (STRAY et al., 2025; CUI et al., 2025). Sistemas multiagentes, portanto, não eliminam a necessidade de controle humano; redefinem sua posição no ciclo de produção (ALURA, 2026; TOOLBOXKART, 2026).

## 5.6 Síntese parcial

esta seção examinou a evolução dos agentes isolados para sistemas multiagentes e os protocolos que viabilizam sua interoperabilidade. Verificou-se que (i) a colaboração entre agentes especializados supera pipelines monolíticos em tarefas decomponíveis, com o MetaGPT como arquétipo de orquestração por artefatos estruturados; (ii) ciclos de reflexão e revisão cruzada melhoram a corretude funcional, mas não a segurança, exigindo validação por ferramentas externas e revisão humana; (iii) os protocolos MCP, ACP, A2A e ANP organizam a integração agente-ferramenta e agente-agente em camadas complementares ainda em consolidação; e (iv) a adoção corporativa vem produzindo padrões de governança e plataformas abertas que redefinem o papel do engenheiro de software como orquestrador e avaliador de agentes. Esses achados fornecem a base para o exame do ecossistema de ferramentas e práticas de mercado, tema da próxima seção (NASCIMENTO et al., 2025; HONG et al., 2024; XIA et al., 2025).

## Referências

AICOOLIES. OpenHands vs Devin vs SWE-Agent: Autonomous Coding Agent Comparison. 2026. Disponível em: https://aicoolies.com/comparisons/openhands-vs-devin-vs-swe-agent. Acesso em: 08 ago. 2026.

ALURA. IA na Engenharia de Software: Guardrails de Qualidade e Estrategias de Adoção. 2026. Disponível em: https://www.alura.com.br/conteudo/ia-engenharia-software-guardrails-qualidade-estrategias-adocao. Acesso em: 08 ago. 2026.

ANTHROPIC. Introducing the Model Context Protocol. 2025. Disponível em: https://www.anthropic.com/news/model-context-protocol. Acesso em: 08 ago. 2026.

BAYTECH CONSULTING. Unlocking 2026: The Future of AI-Driven Software Development. 2026. Disponível em: https://www.baytechconsulting.com/blog/unlocking-ai-software-development-2026. Acesso em: 08 ago. 2026.

BENCHLM.AI. SWE-bench Verified Benchmark 2026: 44 LLM Scores. 2026. Disponível em: https://benchlm.ai/benchmarks/sweVerified. Acesso em: 08 ago. 2026.

BENCHMARKING AGENTS. AI Agent Benchmarks: SWE-bench, WebArena, AgentBench, Terminal-Bench, OSWorld, Tau-Bench. 2026. Disponível em: https://benchmarkingagents.com/agent-benchmarks. Acesso em: 08 ago. 2026.

BHATTAHALI, Sandeep Kumar et al. CyberSecEval 3: Advancing the Evaluation of Cybersecurity Risks and Capabilities in Large Language Models. Meta, 2024. Disponível em: https://arxiv.org/abs/2408.01605. Acesso em: 08 ago. 2026.

CHEN, Mark et al. Evaluating Large Language Models Trained on Code. 2021. Disponível em: https://arxiv.org/abs/2107.03374. Acesso em: 08 ago. 2026.

CODESOTA. SWE-bench 2026: Compare Devin, Codex, Claude Code, Cursor, OpenHands, Aider. 2026. Disponível em: https://www.codesota.com/tasks/swe-bench. Acesso em: 08 ago. 2026.

CUI, Kevin Zheyuan et al. The Effects of Generative AI on High-Skilled Work: Evidence from Three Field Experiments with Software Developers. SSRN 4945566, 2025. Disponível em: https://economics.mit.edu/sites/default/files/inline-files/draft_copilot_experiments.pdf. Acesso em: 08 ago. 2026.

DONG, Yihong et al. A Survey on Code Generation with LLM-based Agents. 2025. Disponível em: https://arxiv.org/abs/2508.00083. Acesso em: 08 ago. 2026.

DORA/GOOGLE CLOUD. 2025 State of AI-Assisted Software Development Report. 2025. Disponível em: https://dora.dev/dora-report-2025/. Acesso em: 08 ago. 2026.

DORA; GOOGLE CLOUD. State of Cloud-Native Development Report. 2025. Disponível em: https://dora.dev/reports/. Acesso em: 08 ago. 2026.

ENDOR LABS. The Most Common Security Vulnerabilities in AI-Generated Code. 2025. Disponível em: https://www.endorlabs.com/learn/the-most-common-security-vulnerabilities-in-ai-generated-code. Acesso em: 08 ago. 2026.

FORRESTER. Predictions 2026: Software Development Goes From Jamming To A Full Orchestra. 2026. Disponível em: https://www.forrester.com/blogs/predictions-2026-software-development-goes-from-jamming-to-full-orchestra. Acesso em: 08 ago. 2026.

FUTUREWARNS. AI in Software Development: 2026. 2026. Disponível em: https://futurewarns.com/ai-in-software-development-2026. Acesso em: 08 ago. 2026.

GUO, Jiale et al. A Comprehensive Survey on Benchmarks and Solutions in Software Engineering of LLM-Empowered Agentic System. 2025. Disponível em: https://arxiv.org/abs/2510.09721. Acesso em: 08 ago. 2026.

SNYK. AI Code Generation: Code Security & Quality, Benefits, Risks & Tools. 2025. Disponível em: https://snyk.io/blog/ai-code-generation-code-security-quality-benefits-risks-top-tools/. Acesso em: 08 ago. 2026.

TEQNOVOS. Top Trends in Large Language Models (LLMs) for Software Development. 2025. Disponível em: https://teqnovos.com/blog/top-trends-in-large-language-models-llms-for-software-development-in-2026/. Acesso em: 08 ago. 2026.

TOOLBOXKART. OpenAI Codex vs GitHub Copilot vs Claude Code (2026). 2026. Disponível em: https://toolboxkart.tech/blog/codex-vs-github-copilot-vs-claude-code/. Acesso em: 08 ago. 2026.