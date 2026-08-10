# 7 Avaliação de Agentes: Benchmarks e Lacunas de Medição

## 7.1 A necessidade de avaliação padronizada

A avaliação de agentes de IA para engenharia de software exige instrumentos padronizados capazes de comparar modelos, arquiteturas e ferramentas sob condições controladas. Sem benchmarks confiáveis, a seleção de ferramentas apoia-se em percepções subjetivas, marketing de fornecedores e avaliações anedóticas — situação incompatível com a decisão técnica informada exigida pela engenharia de software (JIMENEZ et al., 2024; GUO et al., 2025). A literatura registra esforço intenso de construção de benchmarks desde a primeira onda de modelos geradores de código, com progressiva sofisticação metodológica (DONG et al., 2025; GUO et al., 2025).

A evolução dos benchmarks acompanha a evolução dos próprios sistemas avaliados: enquanto a geração autônoma de funções isoladas exigia conjuntos de problemas de programação competitiva, os agentes modernos, que operam sobre repositórios reais, demandam tarefas integrais de engenharia — ler um repositório, localizar o ponto de alteração, implementar a mudança e validá-la com os testes existentes (JIMENEZ et al., 2024; YANG et al., 2024). Essa transição reposicionou o objeto da medição: não se avalia mais apenas a corretude sintática do código produzido, mas a capacidade de resolver problemas reais de manutenção de software (JIMENEZ et al., 2024).

## 7.2 O SWE-bench e o SWE-bench Verified

O SWE-bench consolidou-se como referência central da área. O benchmark é construído a partir de 2.294 problemas reais extraídos de 12 repositórios Python de código aberto (django, sympy, scikit-learn, matplotlib e outros), cada problema consistindo em um issue do GitHub, um patch de referência gerado por desenvolvedores humanos e um conjunto de testes que validam a solução (JIMENEZ et al., 2024). A tarefa do agente é gerar o patch que resolve o issue; o agente é considerado bem-sucedido se os testes previamente falhando passam e os demais continuam passando (JIMENEZ et al., 2024).

O SWE-bench Verified é um subconjunto de 500 problemas validados manualmente por humanos, criado para eliminar ambiguidades e casos com descrições insuficientes que contaminavam a métrica original (JIMENEZ et al., 2024). Essa curadoria elevou a confiabilidade das comparações e tornou-se o número mais citado nos relatórios de fornecedores: o Codex alcança entre 78% e 85% (BENCHLM.AI, 2026; TOOLBOXKART, 2026), e o Claude Code lidera com aproximadamente 80,8% na configuração mais recente (BENCHLM.AI, 2026). A divulgação desses números nos materiais de marketing, entretanto, raramente informa as condições exatas de execução — número de tentativas, modelos, custos e infraestrutura — o que limita a comparabilidade entre fornecedores (BENCHLM.AI, 2026; TOOLBOXKART, 2026).

## 7.3 Outros benchmarks e a medição de habilidades específicas

Além do SWE-bench, o campo desenvolveu benchmarks para habilidades específicas da engenharia de software. O HumanEval, proposto com o Codex original, avalia a síntese de funções a partir de descrições docstring (CHEN et al., 2021). O CyberSecEval 3 (Meta) mede a propensão de modelos a gerar código inseguro, revelando que modelos líderes produzem código vulnerável em 35% a 40% das tarefas, com falhas recorrentes de validação de entrada (CWE-20), injeção de SQL (CWE-89) e injeção de comandos (CWE-78) (BHATTAHALI et al., 2024; Snyk, 2025). O SeCodePLT, por sua vez, estima que 40% a 65% das amostras de código gerado contêm vulnerabilidades, embora a maioria não acione gatilhos de segurança em execução (SCHERMANN et al., 2024; ENDOR LABS, 2025).

Benchmarks de corretude funcional convivem com métricas de qualidade estrutural. Estudo da SonarQube com 4.442 tarefas Java constatou que mesmo código que passa nos testes funcionais carrega probabilidade de 5% a 8% de conter bugs e cerca de 2% de conter vulnerabilidades (SABRA et al., 2025). A medição de segurança também revela efeitos contraintuitivos: o "paradoxo da confiança" documenta que desenvolvedores que utilizam assistentes de IA consideram seu código mais seguro exatamente quando ele apresenta mais vulnerabilidades (PERRY et al., 2022; Snyk, 2025). Em conjunto, esses resultados demonstram que a corretude funcional é condição necessária, mas insuficiente, para a qualidade do código gerado (SABRA et al., 2025; SCHERMANN et al., 2024).

## 7.4 Lacunas metodológicas dos benchmarks atuais

A despeito do avanço, os benchmarks apresentam lacunas metodológicas significativas. A primeira é a contaminação: problemas públicos, replicados em múltiplos benchmarks, podem integrar os corpora de treinamento dos modelos, inflando os resultados de forma artificial (JIMENEZ et al., 2024; GUO et al., 2025). A segunda é a limitação de domínio: o SWE-bench concentra-se em Python e em poucos repositórios, restringindo a generalização para outras linguagens, ecossistemas e tipos de tarefa (JIMENEZ et al., 2024). A terceira é a ausência de medição econômica: poucos benchmarks reportam custo por solução (tokens, chamadas, tempo) — variável decisiva para a adoção empresarial (TOOLBOXKART, 2026; CUI et al., 2025).

A quarta lacuna é a não medição de atributos emergentes da prática real: capacidade de diálogo em linguagem natural, gestão de contexto longo, aderência a políticas de repositório e qualidade do código sob revisão humana (STRAY et al., 2025; GUO et al., 2025). Benchmarks avaliam o desfecho — o patch correto — mas não o processo, e o processo é precisamente onde as organizações investem em governança (ENDOR LABS, 2025; ALURA, 2026). Por fim, há o problema da flutuação temporal: modelos e configurações mudam rapidamente, tornando obsoletas em meses comparações publicadas com rigor estatístico (BENCHLM.AI, 2026).

## 7.5 Rumos da avaliação: do benchmark à medição organizacional

A resposta às lacunas não é o abandono dos benchmarks, mas sua complementação por medição organizacional contínua. As práticas emergentes combinam: (i) benchmarks públicos para seleção inicial de ferramentas e modelos; (ii) avaliações internas com tarefas representativas do domínio da organização, incluindo linguagens e padrões próprios; (iii) telemetria de produção, com métricas de taxa de aceitação, tempo de revisão, defeitos introduzidos e custo por tarefa (CUI et al., 2025; STRAY et al., 2025); e (iv) auditorias periódicas de segurança do código gerado, por análise estática e testes dinâmicos (Snyk, 2025; ENDOR LABS, 2025).

Estudos de adoção em larga escala fornecem a evidência de que a medição organizacional é viável e informativa: o estudo randomizado com 4.867 desenvolvedores mensurou ganho de 26,08% nas tarefas concluídas por semana, e o estudo longitudinal da NAV IT documentou custo de verificação das sugestões e adoção heterogênea entre engenheiros (CUI et al., 2025; NAV IT, 2025). Esses estudos indicam que a questão central da avaliação deslocou-se de "qual modelo resolve mais issues" para "como o sistema de IA + humano + processos se comporta no contexto específico da organização" (STRAY et al., 2025; GUO et al., 2025).

## 7.6 Síntese parcial

Esta seção examinou o estado da arte e as lacunas da avaliação de agentes. Ficou evidenciado que (i) o SWE-bench e sua versão Verified tornaram-se a referência de comparação, com curadoria manual de 500 problemas e liderança do Claude Code (80,8%) e do Codex (78-85%); (ii) benchmarks complementares medem segurança (CyberSecEval 3, SeCodePLT) e qualidade estrutural (SonarQube), revelando que código funcionalmente correto pode conter vulnerabilidades; (iii) as lacunas metodológicas incluem contaminação de treino, domínio restrito, ausência de custo e foco exclusivo no desfecho; e (iv) a tendência é a combinação de benchmarks públicos com medição organizacional contínua, alinhada às decisões de governança (JIMENEZ et al., 2024; CUI et al., 2025; STRAY et al., 2025). A próxima seção examina as dimensões de qualidade, segurança e dívida técnica do código gerado (Snyk, 2025; ENDOR LABS, 2025).

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

NAV IT. Adopting GitHub Copilot in a Large Public Sector Organization: A Longitudinal Study. 2025. Disponível em: https://arxiv.org/abs/2509.20353. Acesso em: 08 ago. 2026.

SNYK. AI Code Generation: Code Security & Quality, Benefits, Risks & Tools. 2025. Disponível em: https://snyk.io/blog/ai-code-generation-code-security-quality-benefits-risks-top-tools/. Acesso em: 08 ago. 2026.

TOOLBOXKART. OpenAI Codex vs GitHub Copilot vs Claude Code (2026). 2026. Disponível em: https://toolboxkart.tech/blog/codex-vs-github-copilot-vs-claude-code/. Acesso em: 08 ago. 2026.