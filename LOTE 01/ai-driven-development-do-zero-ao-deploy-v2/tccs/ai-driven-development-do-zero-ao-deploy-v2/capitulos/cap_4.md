# 4 Agentes de Software Autônomos

## 4.1 Contextualização

A transição da geração pontual de código para a execução autônoma de tarefas completas de engenharia materializa-se nos agentes de software. Um agente de software é um sistema baseado em LLM que planeja, navega em repositórios, edita arquivos, executa comandos e valida resultados de forma iterativa, com o objetivo de resolver tarefas reais de engenharia de software (YANG et al., 2024; LIU et al., 2024). estaEsta seção examina a arquitetura desses sistemas — interfaces, loops de raciocínio, memória e ferramentas — e os sistemas de referência que estabeleceram o estado da arte: SWE-agent, OpenHands e Devin.

## 4.2 Referencial Teórico: arquitetura dos agentes

### 4.2.1 A Interface Agente-Computador (ACI)

O conceito central introduzido pelo SWE-agent é o de *Agent-Computer Interface* (ACI): o conjunto de primitivas de observação e ação pelas quais um modelo de linguagem interage com um computador (YANG et al., 2024). A pesquisa demonstrou que o desenho da ACI — observações concisas, comandos de alto nível, feedback estruturado de testes — tem impacto no desempenho do agente maior do que a escolha do modelo subjacente. O SWE-agent obteve, com ACI bem projetada, desempenho superior ao de modelos maiores usados sem tais interfaces, em uma época em que os benchmarks agênticos estavam sendo estabelecidos (YANG et al., 2024; CODESOTA, 2026).

### 4.2.2 Loops de raciocínio-ação

A operação dos agentes baseia-se em loops iterativos de raciocínio e ação. O framework ReAct estabeleceu o padrão: intercalar raciocínio explícito (thoughts) e ações (acts), permitindo que o modelo planeje, execute e observe os efeitos de suas decisões (YAO et al., 2023). O Reflexion estendeu o padrão com um mecanismo de memória verbal: o agente registra reflexões sobre suas falhas em uma memória episódica e as utiliza em tentativas subsequentes, configurando uma forma de aprendizado por reforço verbal (SHINN et al., 2023). Esses mecanismos compõem a base cognitiva dos agentes de engenharia atuais (DONG et al., 2025; JIANG; LO; LIU, 2025).

### 4.2.3 Memória e ferramentas

A autonomia dos agentes depende de duas infraestruturas complementares: memória e ferramentas. A memória organiza o contexto — histórico de decisões, estado do repositório, resultados de testes — em camadas de curto e longo prazo, permitindo ao agente manter coerência em tarefas longas (LIU et al., 2024; JIN et al., 2024). O uso de ferramentas, por sua vez, expande o escopo de ação: compiladores, linters, gerenciadores de testes e navegadores são acionados pelo agente como primitivas de ação, seguindo o princípio do Toolformer de aprendizagem autônoma de uso de ferramentas (SCHICK et al., 2023). A integração padronizada dessas ferramentas é objeto do Model Context Protocol, que define primitivas de recursos, prompts, ferramentas e amostragem (MODEL CONTEXT PROTOCOL, 2025; NASCIMENTO et al., 2025).

## 4.3 Análise: sistemas de referência

### 4.3.1 SWE-agent

O SWE-agent, desenvolvido na Universidade de Princeton, é a referência acadêmica do campo: estabeleceu as ACIs, o padrão de avaliação e a arquitetura de resolução de issues baseada em execução local (YANG et al., 2024). Sua abordagem de interface mínima com observações enxutas demonstrou ganhos significativos de desempenho em SWE-bench em relação a sistemas anteriores, e seu código foi mantido posteriormente na forma do mini-swe-agent (AICOOLIES, 2026). Sua importância é metodológica: definiu as condições de experimentação controlada em tarefas reais de engenharia.

### 4.3.2 OpenHands

O OpenHands (ex-OpenDevin) é a plataforma open-source mais difundida para agentes de desenvolvimento, com runtime em sandbox Docker/Kubernetes, suporte a agentes paralelos e agnosticismo de modelo (WANG et al., 2024; AICOOLIES, 2026). Sua adoção por empresas como Apple, Google, Amazon, Netflix e NVIDIA demonstra a convergência entre pesquisa acadêmica e prática industrial. A plataforma destaca-se pela segurança de execução em ambiente isolado e pela reprodutibilidade dos experimentos (WANG et al., 2024).

### 4.3.3 Devin e os agentes gerenciados em nuvem

O Devin, da Cognition, representa a categoria dos agentes gerenciados em nuvem: um "engenheiro de software IA" com editor, navegador e terminal próprios, integrações com GitHub, Slack, Jira e Linear, e execução assíncrona de tarefas (AICOOLIES, 2026; TOOLBOXKART, 2026). Essa arquitetura desloca a execução do ambiente local do desenvolvedor para infraestrutura remota, com implicações de governança, custo e observabilidade. O OpenAI Codex, relançado em 2025, segue o mesmo modelo de execução assíncrona em sandbox em nuvem, com criação autônoma de pull requests (TOOLBOXKART, 2026).

### 4.3.4 Abordagens alternativas e o debate da complexidade

A literatura registra um debate relevante sobre a necessidade de agentes complexos. O sistema Agentless demonstrou que uma pipeline simples de localização e edição, sem raciocínio agêntico iterativo, alcança desempenho competitivo em SWE-bench (XIA et al., 2025). Esse resultado contesta a premissa de que autonomia plena é necessária para resolver issues reais e sugere que a arquitetura de pipeline — contexto bem montado, localização precisa e edição cirúrgica — pode ser mais determinante que a sofisticação do loop de raciocínio (XIA et al., 2025). Complementarmente, estudos de context engineering mostram que a qualidade do contexto fornecido ao modelo supera o prompt engineering na resolução de tarefas (MURUGESAN, 2026).

## 4.4 Síntese Parcial

Os agentes de software autônomos representam a materialização operacional do ADD. Sua arquitetura assenta-se em ACIs bem desenhadas (YANG et al., 2024), loops de raciocínio-ação com reflexão (YAO et al., 2023; SHINN et al., 2023), memória estruturada e uso de ferramentas (SCHICK et al., 2023; LIU et al., 2024). Os sistemas de referência — SWE-agent, OpenHands e Devin — definem três modelos de operação: acadêmico, plataforma open-source e serviço gerenciado em nuvem (AICOOLIES, 2026). O debate entre autonomia plena e pipelines simplificados (XIA et al., 2025) qualifica a interpretação dos resultados de benchmark, que será aprofundada na seção 7. A existência de múltiplos agentes interagindo entre si e com ferramentas padronizadas levanta, por sua vez, as questões de orquestração e interoperabilidade examinadas na seção 5.

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

JIANG, Zhonghao; LO, David; LIU, Zhongxin. Agentic Software Issue Resolution with Large Language Models: A Survey. 2025. Disponível em: https://arxiv.org/abs/2507.03126. Acesso em: 08 ago. 2026.

MODEL CONTEXT PROTOCOL. Specification 2025-11-25. 2025. Disponível em: https://modelcontextprotocol.io/specification/2025-11-25. Acesso em: 08 ago. 2026.

MURUGESAN, Thirunaavukkarasu. Enhancing SWE Bench with Context Engineering: A Comparative Study Against Prompt Engineering in LLM-Based Software Tasks. Journal of Information Systems Engineering & Management, 2026. Disponível em: https://doi.org/10.55267/iadt.07.2026.20. Acesso em: 08 ago. 2026.

TOOLBOXKART. OpenAI Codex vs GitHub Copilot vs Claude Code (2026). 2026. Disponível em: https://toolboxkart.tech/blog/codex-vs-github-copilot-vs-claude-code/. Acesso em: 08 ago. 2026.