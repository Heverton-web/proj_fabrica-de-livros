# 3 Modelos de Linguagem e Geração de Código

## 3.1 Contextualização

A geração de código por modelos de linguagem constitui o alicerce empírico do AI Driven Development. Desde os primeiros modelos capazes de completar trechos de programa até os sistemas agênticos atuais, a capacidade de produzir código funcional a partir de linguagem natural evoluiu de forma acelerada, impulsionada por avanços arquiteturais, por corpora de treinamento cada vez maiores e por regimes de avaliação cada vez mais rigorosos (CHEN et al., 2021; GUO et al., 2025). estaEsta seção analisa essa evolução, os instrumentos de medição e as capacidades e limitações documentadas da geração de código por LLMs.

## 3.2 Referencial Teórico: evolução dos modelos de código

### 3.2.1 Do Codex aos modelos agênticos

O marco inaugural da geração de código por LLMs em escala industrial foi o Codex, modelo treinado a partir do GPT-3 sobre corpus massivo de código público, apresentado em 2021 com o benchmark HumanEval (CHEN et al., 2021). O Codex demonstrou a viabilidade de resolver problemas de programação em linguagem natural, estabelecendo o paradigma de avaliação por pass@k e inspirando toda uma geração de assistentes, incluindo o GitHub Copilot (TOOLBOXKART, 2026). O modelo original foi deprecado em 2023, mas o nome persistiu na plataforma OpenAI Codex, relançada em 2025 como agente de codificação autônomo em nuvem (TOOLBOXKART, 2026; OFLIGHT, 2026).

A geração de código evoluiu em três frentes complementares. Na frente arquitetural, o surgimento de modelos especializados em código — como os da família Codex, os modelos com janelas de contexto estendidas e arquiteturas Mixture-of-Experts (MoE) — ampliou a capacidade de raciocínio sobre programas longos e multiarquivo (SILICONFLOW, 2026). Na frente de integração, os modelos passaram a ser acoplados a ferramentas e ambientes, primeiro via APIs e, posteriormente, via protocolos de interoperabilidade como o Model Context Protocol (ANTHROPIC, 2025; MODEL CONTEXT PROTOCOL, 2025). Na frente agêntica, a geração deixou de ser um ato único e passou a integrar loops de planejamento, edição, execução e reparo (DONG et al., 2025; XIA et al., 2025).

### 3.2.2 Aprendizagem de uso de ferramentas

A geração de código efetiva depende da capacidade dos modelos de acionar ferramentas externas — compiladores, gerenciadores de pacotes, sistemas de testes, buscadores — de forma autônoma. O trabalho seminal do Toolformer demonstrou que modelos de linguagem podem aprender, por auto-supervisão, a decidir quando e como chamar APIs externas, ampliando substancialmente suas capacidades (SCHICK et al., 2023). Esse princípio é o fundamento dos agentes modernos: a decisão de uso de ferramentas é internalizada pelo modelo e refinada por feedback dos resultados (YAO et al., 2023; GUO et al., 2025).

### 3.2.3 Benchmarks funcionais: HumanEval e sucessores

A avaliação da geração de código funcional foi padronizada pelo HumanEval, conjunto de 164 problemas de programação com casos de teste ocultos, cuja métrica pass@k mede a fração de soluções corretas entre k amostras geradas (CHEN et al., 2021). Essa métrica tornou-se o padrão da indústria e foi sucedida por suítes mais amplas e rigorosas, incluindo MBPL, MultiPL-E e CWEval, que avaliam não apenas a corretude funcional, mas também a segurança das saídas (WANG et al., 2025). O avanço dos resultados nessas suítes — de percentuais de dígito único em 2021 para resultados superiores a 90% em benchmarks funcionais atuais — documenta a rápida maturação da geração de código (LLM-STATS, 2026; BENCHLM.AI, 2026).

## 3.3 Análise: capacidades e limitações da geração de código

### 3.3.1 A qualidade funcional é condição necessária, mas insuficiente

A literatura converge na distinção entre corretude funcional e qualidade de engenharia. Estudos quantitativos com 4.442 tarefas Java demonstraram que o código gerado que passa nos testes ainda apresenta probabilidade de 5% a 8% de conter bugs e cerca de 2% de conter vulnerabilidades, sem correlação significativa entre a métrica pass@1 e a qualidade estrutural do código (SABRA; SCHMITT; SONAR, 2025). Resultados análogos foram obtidos na análise multi-linguagem e multi-modelo (arXiv:2502.01853, 2025). A corretude funcional, portanto, não é suficiente para garantir a manutenibilidade ou a segurança dos artefatos produzidos.

### 3.3.2 Segurança do código gerado

A dimensão de segurança concentra as evidências mais preocupantes. O CyberSecEval 3, da Meta, documentou que modelos líderes produzem código inseguro em 35% a 40% das amostras (BHATTAHALI et al., 2024). O dataset SeCodePLT encontrou vulnerabilidades em 40% a 65% das amostras de código gerado (SCHERMANN et al., 2024). As falhas mais recorrentes incluem ausência de validação de entrada (CWE-20), injeção de SQL (CWE-89), injeção de comandos (CWE-78), credenciais hardcoded, path traversal e dependências alucinadas (SNYK, 2025; ENDOR LABS, 2025). Estudos específicos em desenvolvimento web confirmam a ocorrência desses padrões em linguagens como PHP (VAVEKANAND et al., 2024).

### 3.3.3 O paradoxo da confiança

Um dos achados mais contraintuitivos da literatura é o paradoxo da confiança: desenvolvedores que utilizam assistentes de IA escrevem código menos seguro ao mesmo tempo em que acreditam mais na segurança do que produzem (PERRY et al., 2022). O estudo de Stanford que documentou o fenômeno mostrou que os usuários do assistente geravam soluções com maior taxa de vulnerabilidades e, paradoxalmente, expressavam maior confiança na correção de suas respostas (PERRY et al., 2022; SNYK, 2025). Complementarmente, experimentos mostraram que rodadas iterativas de refinamento com IA podem elevar a quantidade de vulnerabilidades críticas em cerca de 38% quando aplicadas a código originalmente seguro (SNYK, 2025).

### 3.3.4 Manutenibilidade e dívida técnica

A análise da manutenibilidade do código gerado revela padrões estruturais distintos. O estudo de ZHU, TSANTALIS e RIGBY (2026) identificou uma "assinatura de máquina" na dívida técnica de código produzido por LLMs e agentes: prevalência de bloat procedural, God Classes e acoplamento cíclico, com a chamada "Lei Inversa Volume-Qualidade", segundo a qual o volume de código gerado é preditor de degradação estrutural. O estudo demonstrou ainda que nem a corretude funcional nem prompts detalhados evitam essa degradação (ZHU; TSANTALIS; RIGBY, 2026). Em contraste, o estudo de SANTA MOLISON et al. (2025) encontrou indicadores mistos de manutenibilidade e confiabilidade comparados ao código humano, sublinhando a heterogeneidade dos resultados segundo tarefa e modelo.

### 3.3.5 Heterogeneidade dos resultados

Os resultados da geração de código variam fortemente segundo a natureza da tarefa. Tarefas autocontidas de programação competitiva são resolvidas com alta taxa de sucesso, enquanto tarefas de integração, refatoração em bases legadas e manutenção de sistemas de grande porte apresentam desempenho substancialmente inferior (GUO et al., 2025; JIANG; LO; LIU, 2025). A literatura explica essa heterogeneidade pela necessidade de contexto de projeto — histórico, convenções, arquitetura existente — que os benchmarks funcionais não capturam (BENCHMARKING AGENTS, 2026).

## 3.4 Síntese Parcial

Os modelos de linguagem evoluíram de geradores de trechos para sistemas capazes de produzir soluções completas e, posteriormente, para componentes de agentes autônomos (CHEN et al., 2021; DONG et al., 2025). A avaliação funcional avançou do HumanEval para suítes que medem também segurança e qualidade (WANG et al., 2025). As evidências, contudo, são inequívocas quanto à insuficiência da corretude funcional: o código gerado apresenta riscos de segurança sistemáticos (BHATTAHALI et al., 2024; SCHERMANN et al., 2024), paradoxo de confiança nos usuários (PERRY et al., 2022) e padrões estruturais de dívida técnica (ZHU; TSANTALIS; RIGBY, 2026). Esses achados fundamentam a necessidade de camadas de verificação e governança que serão examinadas nas seções 7 e 8, e delimitam o que os agentes de software — objeto da seção 4 — podem realisticamente entregar.

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

ENDOR LABS. The Most Common Security Vulnerabilities in AI-Generated Code. 2025. Disponível em: https://www.endorlabs.com/learn/the-most-common-security-vulnerabilities-in-ai-generated-code. Acesso em: 08 ago. 2026.

JIANG, Zhonghao; LO, David; LIU, Zhongxin. Agentic Software Issue Resolution with Large Language Models: A Survey. 2025. Disponível em: https://arxiv.org/abs/2507.03126. Acesso em: 08 ago. 2026.

LLM-STATS. SWE-Bench Verified Leaderboard. 2026. Disponível em: https://llm-stats.com/benchmarks/swe-bench-verified. Acesso em: 08 ago. 2026.

MODEL CONTEXT PROTOCOL. Specification 2025-11-25. 2025. Disponível em: https://modelcontextprotocol.io/specification/2025-11-25. Acesso em: 08 ago. 2026.

OFLIGHT. Codex vs Claude Code vs Cursor vs Copilot: 2026 AI Coding Tool Comparison. 2026. Disponível em: https://www.oflight.co.jp/en/columns/codex-vs-claude-code-cursor-copilot-comparison-2026. Acesso em: 08 ago. 2026.

SABRA, Abbas; SCHMITT, Olivier; SONAR, Joseph Tyler. Assessing the Quality and Security of AI-Generated Code: A Quantitative Analysis. 2025. Disponível em: https://arxiv.org/abs/2508.14727. Acesso em: 08 ago. 2026.

SILICONFLOW. The Best Open Source LLM for Engineering in 2026. 2026. Disponível em: https://www.siliconflow.com/articles/en/best-open-source-LLM-for-engineering. Acesso em: 08 ago. 2026.

SNYK. AI Code Generation: Code Security & Quality, Benefits, Risks & Tools. 2025. Disponível em: https://snyk.io/blog/ai-code-generation-code-security-quality-benefits-risks-top-tools/. Acesso em: 08 ago. 2026.

TOOLBOXKART. OpenAI Codex vs GitHub Copilot vs Claude Code (2026). 2026. Disponível em: https://toolboxkart.tech/blog/codex-vs-github-copilot-vs-claude-code/. Acesso em: 08 ago. 2026.

ZHU, Yuecai; TSANTALIS, Nikolaos; RIGBY, Peter C. AI-Generated Smells: An Analysis of Code and Architecture in LLM- and Agent-Driven Development. 2026. Disponível em: https://arxiv.org/abs/2605.02741. Acesso em: 08 ago. 2026.