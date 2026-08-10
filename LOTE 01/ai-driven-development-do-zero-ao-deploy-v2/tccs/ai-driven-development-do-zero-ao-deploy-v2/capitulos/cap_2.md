# 2 Fundamentos da Engenharia de Software Dirigida por IA

## 2.1 Contextualização: a natureza da mudança de paradigma

A engenharia de software constitui um campo historicamente dependente da intensidade de trabalho humano qualificado para a transformação de requisitos em artefatos executáveis. A emergência dos modelos de linguagem de grande escala introduz um ator novo nesse processo: uma entidade capaz de produzir artefatos textuais — e, portanto, código — com fluência próxima à humana, em escala e velocidade sem precedentes (CHEN et al., 2021; STAHNKE; VAHLDICK, 2013). O que distingue a onda atual de automações anteriores é o deslocamento do locus da automação: não se automatiza mais apenas a compilação ou o gerenciamento de builds, mas a própria atividade de escrita de especificações, código, testes e documentação (SAUVOLA et al., 2024; TERRAGNI; ROOP; BLINCOE, 2024).

O termo *AI Driven Development* (ADD) foi cunhado para descrever esse paradigma: um modo de produção de software no qual LLMs e agentes de IA participam ativamente de todas as fases do ciclo de vida — especificação, arquitetura, codificação, testes, revisão, implantação e manutenção —, em graus variáveis de autonomia, de sugestões reativas até operação totalmente autônoma (TEQNOVOS, 2025; BAYTECH CONSULTING, 2026). Nessa definição, a IA deixa de ser uma ferramenta auxiliar pontual e passa a integrar a estrutura do processo, modificando papéis, competências e formas de colaboração dentro das equipes (STRAY et al., 2025; VINICIUS3W, 2025).

## 2.2 Referencial Teórico: taxonomia dos paradigmas de LLM na engenharia de software

### 2.2.1 Os três paradigmas de GUO et al. (2025)

A literatura consolidou a classificação da engenharia de software impulsionada por LLMs (*LLM-empowered software engineering*) em três paradigmas complementares (GUO et al., 2025):

a) **Paradigma baseado em prompts (prompt-based):** o modelo é utilizado como um gerador de artefatos a partir de descrições textuais elaboradas por humanos. É o modo mais difundido, exemplificado por assistentes de autocompletar e chatbots de apoio à codificação (CHEN et al., 2021; STRAY et al., 2025). A qualidade da saída depende criticamente da qualidade da entrada, o que impulsionou o desenvolvimento de técnicas de engenharia de prompt e de context engineering (MURUGESAN, 2026).

b) **Paradigma baseado em ajuste fino (fine-tune-based):** modelos genéricos são especializados em tarefas de engenharia de software por meio de treinamento adicional sobre corpora de código e dados técnicos. Essa abordagem produz modelos de domínio, como os especializados em geração de código, capazes de incorporar convenções, idiomas de programação e padrões arquiteturais específicos (GUO et al., 2025; DONG et al., 2025).

c) **Paradigma baseado em agentes (agent-based):** LLMs são incorporados a sistemas autônomos que planejam, executam ações sobre o ambiente (edição de arquivos, execução de comandos, consulta a ferramentas), observam os resultados e iteram até atingir um objetivo — os chamados *software engineering agents* (YANG et al., 2024; LIU et al., 2024; JIN et al., 2024).

### 2.2.2 Agentes de software: definição e capacidades

Um agente de software é definido como um sistema baseado em LLM que planeja, navega em repositórios de código, edita arquivos, executa comandos e valida resultados de forma iterativa para resolver tarefas reais de engenharia (YANG et al., 2024). Diferentemente dos assistentes de autocompletar, o agente opera em ciclos percepção-raciocínio-ação: interpreta o estado do repositório, decide o próximo passo, executa a ação e observa o efeito antes de prosseguir (YAO et al., 2023). Essa arquitetura de loop é o coração do paradigma agêntico e a fonte de sua capacidade de lidar com tarefas de composição — problemas que exigem múltiplas edições coordenadas em arquivos distintos (JIANG; LO; LIU, 2025; XIA et al., 2025).

### 2.2.3 Interface agente-computador (ACI)

A interação do agente com o ambiente computacional exige interfaces projetadas especificamente para modelos de linguagem. O conceito de *Agent-Computer Interface* (ACI) designa o conjunto de canais pelos quais o agente observa e age sobre o sistema — terminal, editor, navegador, APIs — e um dos achados mais relevantes do campo é que o desenho dessa interface impacta o desempenho do agente mais do que a escolha do modelo subjacente (YANG et al., 2024; CODESOTA, 2026). Interfaces com observações concisas, ações de alto nível e feedback estruturado reduzem a carga cognitiva do modelo e aumentam a taxa de sucesso na resolução de issues (YANG et al., 2024).

### 2.2.4 O ciclo de vida do software impactado

A participação de LLMs e agentes estende-se por todo o ciclo de vida: na especificação, com a elaboração assistida de requisitos e critérios de aceite; na arquitetura, com a geração de propostas de projeto e análise de trade-offs; na codificação, com a geração, refatoração e reparo de código; nos testes, com a síntese de casos de teste e a análise de cobertura; na revisão, com a inspeção automatizada de pull requests; e na manutenção, com a triagem de issues e a correção de defeitos (GUO et al., 2025; TEQNOVOS, 2025; BAYTECH CONSULTING, 2026). Esse espectro completo faz do ADD um paradigma transversal, e não uma técnica pontual de geração de código.

## 2.3 Análise: da assistência reativa à autonomia proativa

A literatura documenta uma progressão contínua no grau de autonomia das ferramentas. O GitHub Copilot, lançado em 2021 sobre o modelo Codex original, inaugurou a assistência reativa de autocompletar (CHEN et al., 2021; TOOLBOXKART, 2026). A partir de 2023, padrões de *agentic coding* — em que o modelo decide a sequência de ações, planeja, usa ferramentas e reflete sobre resultados — passaram a dominar o discurso e a prática (YAO et al., 2023; SHINN et al., 2023; MINDSHARE, 2026). Em 2025, surgiram os primeiros agentes de codificação autônomos em nuvem, capazes de executar tarefas completas de forma assíncrona e paralela, criando pull requests sem intervenção humana contínua (TOOLBOXKART, 2026; AICOOLIES, 2026).

Essa progressão não é meramente incremental: ela altera a distribuição de responsabilidade entre humano e máquina. No modo assistido, o desenvolvedor permanece o autor, e a IA sugere; no modo agêntico, o agente torna-se executor, e o desenvolvedor assume papel de supervisor e avaliador de saídas (STRAY et al., 2025; VINICIUS3W, 2025). Estudos de campo documentam a mudança percebida de papel: os desenvolvedores gastam tempo adicional verificando sugestões e relatam limitações de explicabilidade das decisões dos agentes (STRAY et al., 2025; STRAY; MOE; GANESHAN; KOBBENES, 2025).

A análise crítica revela também uma tensão estrutural: quanto maior a autonomia concedida ao agente, maior a dependência da qualidade dos processos de verificação circundantes. Os dados de segurança são ilustrativos: mesmo os modelos líderes produzem código inseguro em parcela expressiva das amostras (BHATTAHALI et al., 2024; SCHERMANN et al., 2024), e a ausência de revisão humana sistemática converte a autonomia em risco (SNYK, 2025; ALURA, 2026). O ADD não elimina, portanto, a necessidade de engenharia — transfere-a para as camadas de especificação, verificação e governança.

## 2.4 Síntese Parcial

Os fundamentos do ADD revelam um paradigma em três camadas: uma camada de modelos (LLMs generalistas e especializados), uma camada de interfaces (ACIs e ferramentas) e uma camada de processos (fluxos de verificação e governança). A taxonomia de GUO et al. (2025) organiza os modos de uso, e a literatura agêntica demonstra que a eficácia depende tanto dos modelos quanto do desenho das interfaces e dos loops de ação (YANG et al., 2024; JIANG; LO; LIU, 2025). A mudança de papel do desenvolvedor — de autor para supervisor — é o efeito organizacional mais consistente documentado (STRAY et al., 2025). Esses fundamentos fornecem a base para as seções seguintes, que examinam os modelos e a geração de código (seção 3), os agentes autônomos (seção 4) e as camadas superiores do paradigma.

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

JIANG, Zhonghao; LO, David; LIU, Zhongxin. Agentic Software Issue Resolution with Large Language Models: A Survey. 2025. Disponível em: https://arxiv.org/abs/2507.03126. Acesso em: 08 ago. 2026.

MINDSHARE. Claude Code vs OpenAI Codex: Which AI Coding Agent Is Better? 2026. Disponível em: https://www.mindstudio.ai/blog/claude-code-vs-openai-codex-comparison. Acesso em: 08 ago. 2026.

MURUGESAN, Thirunaavukkarasu. Enhancing SWE Bench with Context Engineering: A Comparative Study Against Prompt Engineering in LLM-Based Software Tasks. Journal of Information Systems Engineering & Management, 2026. Disponível em: https://doi.org/10.55267/iadt.07.2026.20. Acesso em: 08 ago. 2026.

SNYK. AI Code Generation: Code Security & Quality, Benefits, Risks & Tools. 2025. Disponível em: https://snyk.io/blog/ai-code-generation-code-security-quality-benefits-risks-top-tools/. Acesso em: 08 ago. 2026.

STAHNKE, Eduardo; VAHLDICK, Adilson. Inteligência Artificial Aplicada na Engenharia de Software. Resumos Internos, v. 2, n. 1, 2013. Disponível em: https://www.researchgate.net/publication/392212068. Acesso em: 08 ago. 2026.

STRAY, Viktoria; MOE, Nils Brede; GANESHAN, Nina; KOBBENES, Sebastian. Generative AI and Developer Workflows: How GitHub Copilot and ChatGPT Influence Solo and Pair Programming. 2025. Disponível em: https://arxiv.org/abs/2503.12131. Acesso em: 08 ago. 2026.

TEQNOVOS. Top Trends in Large Language Models (LLMs) for Software Development. 2025. Disponível em: https://teqnovos.com/blog/top-trends-in-large-language-models-llms-for-software-development-in-2026/. Acesso em: 08 ago. 2026.

TERRAGNI, Valerio; ROOP, Partha; BLINCOE, Kelly. The Future of Software Engineering in an AI-Driven World. 2024. Disponível em: https://arxiv.org/abs/2406.07737. Acesso em: 08 ago. 2026.

TOOLBOXKART. OpenAI Codex vs GitHub Copilot vs Claude Code (2026). 2026. Disponível em: https://toolboxkart.tech/blog/codex-vs-github-copilot-vs-claude-code/. Acesso em: 08 ago. 2026.