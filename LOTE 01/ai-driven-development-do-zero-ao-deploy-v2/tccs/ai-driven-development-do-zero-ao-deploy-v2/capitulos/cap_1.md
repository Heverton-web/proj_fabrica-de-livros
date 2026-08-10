# 1 Introdução

## 1.1 Contextualização da problemática

A engenharia de software, desde a sua consolidação como disciplina nas décadas de 1960 e 1970, caracteriza-se pela busca contínua de métodos, processos e ferramentas que elevem a produtividade e a qualidade dos artefatos produzidos. Essa trajetória é marcada por sucessivas ondas de automação — dos compiladores às linguagens de alto nível, dos ambientes integrados de desenvolvimento (IDEs) às plataformas de integração contínua —, cada uma das quais redistribuiu as tarefas entre humanos e máquinas (STAHNKE; VAHLDICK, 2013). A mais recente dessas ondas, protagonizada pelos modelos de linguagem de grande escala (large language models — LLMs) e pelos agentes de inteligência artificial, inaugura um paradigma que a literatura recente passou a denominar *AI Driven Development* (ADD): um modelo de produção de software em que modelos de linguagem e agentes participam ativamente de todas as fases do ciclo de vida — especificação, arquitetura, codificação, testes, revisão, implantação e manutenção —, atuando de forma reativa, proativa ou autônoma (TEQNOVOS, 2025; BAYTECH CONSULTING, 2026).

O marco fundacional dessa trajetória é o lançamento, em 2021, do Codex original, modelo treinado em código que demonstrou a viabilidade de gerar programas completos a partir de descrições em linguagem natural (CHEN et al., 2021). No mesmo período, a padronização de benchmarks funcionais como HumanEval e MBPL estabeleceu um regime de avaliação da geração de código que se tornou referência para os estudos subsequentes (CHEN et al., 2021). Nos anos seguintes, a evolução deixou de se limitar à geração pontual de trechos de código e passou a abranger sistemas agênticos capazes de planejar, navegar em repositórios, editar arquivos, executar comandos e validar resultados de forma iterativa — os chamados agentes de software (software engineering agents — SWE agents) (YANG et al., 2024; DONG et al., 2025).

A relevância do fenômeno é quantificável. Estudos controlados randomizados realizados com 4.867 desenvolvedores em empresas como Microsoft, Accenture e organizações da Fortune 100 identificaram ganho médio de 26,08% nas tarefas concluídas por semana entre usuários de assistentes de codificação (CUI et al., 2025). O relatório DORA de 2025 indica que cerca de 90% dos respondentes utilizam inteligência artificial generativa no trabalho diário e que 80% se percebem mais produtivos com o seu uso (DORA/GOOGLE CLOUD, 2025). No plano macro, estima-se que Google e Microsoft já tenham cerca de 30% do código novo escrito ou assistido por IA (ALURA, 2026), enquanto o GitHub Octoverse registra crescimento ano a ano na parcela de código gerado ou assistido por modelos (FUTUREWARNS, 2026).

## 1.2 O problema de pesquisa

Apesar da rápida adoção, o conhecimento sobre as reais capacidades, limites e consequências do desenvolvimento dirigido por IA permanece fragmentado e, em vários pontos, contraditório. De um lado, os resultados em benchmarks públicos de resolução de issues reais, como o SWE-bench Verified, alcançam índices crescentes de acerto em subconjuntos validados por humanos (JIMENEZ et al., 2024; LLM-STATS, 2026). De outro, evidências empíricas indicam que o desempenho em benchmarks não se transfere linearmente para o trabalho real de engenharia: tarefas que envolvem coordenação multi-semana, revisão entre pares e decisões de produto não são capturadas pelos cenários sintéticos (BENCHMARKING AGENTS, 2026). Estudos de segurança demonstram que modelos líderes produzem código inseguro em 35% a 40% das vezes (BHATTAHALI et al., 2024) e que desenvolvedores que usam assistentes de IA tendem a escrever código menos seguro ao mesmo tempo em que acreditam mais em sua segurança — fenômeno denominado *paradoxo da confiança* (PERRY et al., 2022; SNYK, 2025).

No âmbito organizacional, o relatório DORA de 2025 estabelece que a IA é um amplificador de desempenho, e não uma solução: a adoção correlaciona-se com maior throughput, mas também com maior instabilidade, mais falhas de mudança e retrabalho quando não há sistemas e processos maduros (DORA/GOOGLE CLOUD, 2025; INFOQ, 2026). Paralelamente, pesquisas sobre a qualidade estrutural do código gerado identificam uma "assinatura de máquina" na dívida técnica — padrões como bloat procedural, God Classes e acoplamento cíclico —, que persistem mesmo em código funcionalmente correto (ZHU; TSANTALIS; RIGBY, 2026).

Configura-se, portanto, um problema de pesquisa com dupla face: por um lado, compreender o que o paradigma ADD é capaz de realizar na prática; por outro, identificar os mecanismos de avaliação, governança e garantia de qualidade que determinam se essa adoção produz ganhos sustentáveis ou amplifica disfunções existentes. A literatura oferece revisões sistemáticas abrangentes sobre agentes em engenharia de software (JIN et al., 2024; LIU et al., 2024; JIANG; LO; LIU, 2025), mas a integração dos achados de benchmarks, estudos de produtividade, segurança e qualidade estrutural em uma síntese coesa, em língua portuguesa e orientada à realidade das organizações de software, permanece uma lacuna.

## 1.3 Objetivos

### 1.3.1 Objetivo geral

Analisar o paradigma do desenvolvimento de software dirigido por agentes de inteligência artificial — o *AI Driven Development* —, caracterizando seus fundamentos, ferramentas, formas de avaliação, riscos e implicações para a engenharia de software da atualidade.

### 1.3.2 Objetivos específicos

a) Descrever os fundamentos conceituais do ADD, incluindo a taxonomia dos paradigmas prompt-based, fine-tune-based e agent-based da engenharia de software impulsionada por LLMs;

b) Examinar a evolução dos modelos de linguagem aplicados à geração de código e os instrumentos de avaliação funcional dessa geração;

c) Analisar a arquitetura dos agentes de software autônomos, seus loops de raciocínio, memória, uso de ferramentas e interfaces agente-computador;

d) Investigar os sistemas multiagentes e os protocolos de interoperabilidade que sustentam a infraestrutura de desenvolvimento agêntico;

e) Mapear o ecossistema de ferramentas comerciais e as práticas emergentes de adoção, incluindo o desenvolvimento dirigido por especificação;

f) Avaliar criticamente os benchmarks de agentes e as lacunas metodológicas de medição, em especial o hiato entre desempenho em benchmark e desempenho em produção;

g) Sintetizar as evidências sobre qualidade, segurança e dívida técnica do código gerado por LLMs e agentes;

h) Analisar as evidências empíricas de produtividade e os modelos organizacionais de adoção de IA, com ênfase no relatório DORA de 2025.

## 1.4 Justificativa

A justificativa desta pesquisa assenta-se em três dimensões complementares. A primeira é de ordem prática: organizações de todos os portes estão incorporando ferramentas de IA ao fluxo de desenvolvimento sem dispor de evidências organizadas sobre como fazê-lo de forma segura e produtiva (ALURA, 2026; FUTUREWARNS, 2026). A compreensão dos guardrails de qualidade — revisão humana obrigatória, análise estática de segurança (SAST), varredura de dependências (SCA) e governança de processos — é condição para que os ganhos documentados nos estudos controlados (CUI et al., 2025) não sejam convertidos em débito técnico e vulnerabilidades (SNYK, 2025; ENDOR LABS, 2025).

A segunda dimensão é acadêmica. O campo é jovem e evolui rapidamente: os principais surveys de agentes para engenharia de software foram publicados entre 2024 e 2025 (JIN et al., 2024; LIU et al., 2024; GUO et al., 2025; JIANG; LO; LIU, 2025) e a literatura sobre a qualidade do código gerado encontra-se em consolidação (ZHU; TSANTALIS; RIGBY, 2026; SANTA MOLISON et al., 2025). A síntese crítica desses materiais em língua portuguesa contribui para a formação de engenheiros de software e para a redução da assimetria informacional entre a comunidade internacional e a brasileira.

A terceira dimensão é estratégica. Os relatórios setoriais projetam a consolidação do trabalho agêntico e da orquestração multiagente como direção dominante do desenvolvimento de software (FORRESTER, 2026; TEQNOVOS, 2025). Compreender antecipadamente as capacidades, as limitações e as condições organizacionais de sucesso desse paradigma é requisito para a tomada de decisão informada por parte de gestores, arquitetos e desenvolvedores.

## 1.5 Metodologia

esta pesquisa caracteriza-se como qualitativa, de natureza exploratória-descritiva, baseada em revisão de literatura do tipo narrativa estruturada. O corpus foi constituído por quatro categorias de fontes: (i) artigos científicos revisados por pares e preprints indexados em arXiv e periódicos, cobrindo o período de 2013 a 2026; (ii) relatórios técnicos institucionais, com destaque para o DORA Report 2025 (DORA/GOOGLE CLOUD, 2025), o SWE-bench e seus derivados (JIMENEZ et al., 2024) e a especificação do Model Context Protocol (MODEL CONTEXT PROTOCOL, 2025); (iii) documentação e materiais oficiais de ferramentas e plataformas comerciais (TOOLBOXKART, 2026; OFLIGHT, 2026); e (iv) publicações técnicas da indústria, como análises do Snyk (SNYK, 2025) e da Endor Labs (ENDOR LABS, 2025).

A coleta foi realizada por meio de busca sistematizada em bases acadêmicas e repositórios técnicos, seguida de triagem por relevância temática e atualidade. O material foi organizado em um dossiê de pesquisa estruturado em seis blocos — conceitos-chave, artigos científicos, estado da arte, casos de uso corporativos, limitações e controvérsias, e fontes brutas —, posteriormente indexado para recuperação semântica. A análise seguiu os quatro momentos do framework ACAD: contextualização de cada tema, levantamento do referencial teórico pertinente, análise crítica das evidências e síntese parcial ao final de cada seção. A redação observou as normas ABNT, com numeração progressiva (NBR 6024) e citação autor-data (NBR 10520).

Delimita-se o escopo: não são objeto deste trabalho a comparação exaustiva de modelos de linguagem individuais, o desenvolvimento de novos benchmarks ou a realização de experimentos controlados com ferramentas específicas, embora tais elementos sejam mobilizados como evidência secundária. A análise se concentra no paradigma ADD como objeto de estudo, com recorte temporal de 2021 a 2026.

## 1.6 Estrutura do trabalho

O trabalho organiza-se em dez seções. A seção 2 estabelece os fundamentos da engenharia de software dirigida por IA, com a taxonomia dos paradigmas e o impacto sobre o ciclo de vida do software. A seção 3 analisa os modelos de linguagem e a geração de código. A seção 4 examina os agentes de software autônomos. A seção 5 aborda os sistemas multiagentes e os protocolos de interoperabilidade. A seção 6 mapeia o ecossistema de ferramentas e práticas de mercado. A seção 7 avalia os benchmarks de agentes e suas lacunas metodológicas. A seção 8 sintetiza as evidências sobre qualidade, segurança e dívida técnica. A seção 9 analisa produtividade e impacto organizacional. A seção 10 apresenta as considerações finais, limitações e direções futuras.

## Referências

AICOOLIES. OpenHands vs Devin vs SWE-Agent: Autonomous Coding Agent Comparison. 2026. Disponível em: https://aicoolies.com/comparisons/openhands-vs-devin-vs-swe-agent. Acesso em: 08 ago. 2026.

ALURA. IA na Engenharia de Software: Guardrails de Qualidade e Estrategias de Adoção. 2026. Disponível em: https://www.alura.com.br/conteudo/ia-engenharia-software-guardrails-qualidade-estrategias-adocao. Acesso em: 08 ago. 2026.

ANTHROPIC. Introducing the Model Context Protocol. 2025. Disponível em: https://www.anthropic.com/news/model-context-protocol. Acesso em: 08 ago. 2026.

BAYTECH CONSULTING. Unlocking 2026: The Future of AI-Driven Software Development. 2026. Disponível em: https://www.baytechconsulting.com/blog/unlocking-ai-software-development-2026. Acesso em: 08 ago. 2026.

BENCHLM.AI. SWE-bench Verified Benchmark 2026: 44 LLM Scores. 2026. Disponível em: https://benchlm.ai/benchmarks/sweVerified. Acesso em: 08 ago. 2026.

BENCHMARKING AGENTS. AI Agent Benchmarks: SWE-bench, WebArena, AgentBench, Terminal-Bench, OSWorld, Tau-Bench. 2026. Disponível em: https://benchmarkingagents.com/agent-benchmarks. Acesso em: 08 ago. 2026.

BHATTAHALI, Sandeep Kumar et al. CyberSecEval 3: Advancing the Evaluation of Cybersecurity Risks and Capabilities in Large Language Models. Meta, 2024. Disponível em: https://arxiv.org/abs/2408.01605. Acesso em: 08 ago. 2026.

ENDOR LABS. The Most Common Security Vulnerabilities in AI-Generated Code. 2025. Disponível em: https://www.endorlabs.com/learn/the-most-common-security-vulnerabilities-in-ai-generated-code. Acesso em: 08 ago. 2026.

FORRESTER. Predictions 2026: Software Development Goes From Jamming To A Full Orchestra. 2026. Disponível em: https://www.forrester.com/blogs/predictions-2026-software-development-goes-from-jamming-to-full-orchestra. Acesso em: 08 ago. 2026.

FUTUREWARNS. AI in Software Development: 2026. 2026. Disponível em: https://futurewarns.com/ai-in-software-development-2026. Acesso em: 08 ago. 2026.

INFOQ. AI Is Amplifying Software Engineering Performance, Says the DORA Report. 2026. Disponível em: https://www.infoq.com/news/2026/03/ai-dora-report/. Acesso em: 08 ago. 2026.

JIANG, Zhonghao; LO, David; LIU, Zhongxin. Agentic Software Issue Resolution with Large Language Models: A Survey. 2025. Disponível em: https://arxiv.org/abs/2507.03126. Acesso em: 08 ago. 2026.

LLM-STATS. SWE-Bench Verified Leaderboard. 2026. Disponível em: https://llm-stats.com/benchmarks/swe-bench-verified. Acesso em: 08 ago. 2026.

MODEL CONTEXT PROTOCOL. Specification 2025-11-25. 2025. Disponível em: https://modelcontextprotocol.io/specification/2025-11-25. Acesso em: 08 ago. 2026.

OFLIGHT. Codex vs Claude Code vs Cursor vs Copilot: 2026 AI Coding Tool Comparison. 2026. Disponível em: https://www.oflight.co.jp/en/columns/codex-vs-claude-code-cursor-copilot-comparison-2026. Acesso em: 08 ago. 2026.

SNYK. AI Code Generation: Code Security & Quality, Benefits, Risks & Tools. 2025. Disponível em: https://snyk.io/blog/ai-code-generation-code-security-quality-benefits-risks-top-tools/. Acesso em: 08 ago. 2026.

STAHNKE, Eduardo; VAHLDICK, Adilson. Inteligência Artificial Aplicada na Engenharia de Software. Resumos Internos, v. 2, n. 1, 2013. Disponível em: https://www.researchgate.net/publication/392212068. Acesso em: 08 ago. 2026.

TEQNOVOS. Top Trends in Large Language Models (LLMs) for Software Development. 2025. Disponível em: https://teqnovos.com/blog/top-trends-in-large-language-models-llms-for-software-development-in-2026/. Acesso em: 08 ago. 2026.

TOOLBOXKART. OpenAI Codex vs GitHub Copilot vs Claude Code (2026). 2026. Disponível em: https://toolboxkart.tech/blog/codex-vs-github-copilot-vs-claude-code/. Acesso em: 08 ago. 2026.

ZHU, Yuecai; TSANTALIS, Nikolaos; RIGBY, Peter C. AI-Generated Smells: An Analysis of Code and Architecture in LLM- and Agent-Driven Development. 2026. Disponível em: https://arxiv.org/abs/2605.02741. Acesso em: 08 ago. 2026.