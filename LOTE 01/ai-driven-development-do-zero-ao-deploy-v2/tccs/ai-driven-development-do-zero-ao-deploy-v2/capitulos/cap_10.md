# 10 Considerações Finais

## 10.1 Síntese da pesquisa

Esta pesquisa investigou o AI Driven Development (ADD) como paradigma emergente de engenharia de software no qual modelos de linguagem de grande escala (LLMs) e agentes de IA participam ativamente de todas as fases do ciclo de vida — especificação, arquitetura, codificação, testes, revisão, implantação e manutenção (TEQNOVOS, 2025; GUO et al., 2025). A análise percorreu os fundamentos do paradigma (seção 2), a evolução dos modelos de linguagem e da geração de código (seção 3), os agentes autônomos (seção 4), os sistemas multiagentes e protocolos de interoperabilidade (seção 5), o ecossistema de ferramentas (seção 6), a avaliação por benchmarks (seção 7), a qualidade, segurança e dívida técnica (seção 8) e a produtividade e o impacto organizacional (seção 9).

Os resultados consolidados indicam que o ADD representa uma mudança estrutural, e não incremental, na produção de software: o locus da automação deslocou-se da compilação e dos builds para a própria atividade de escrita de especificações, código, testes e documentação (SAUVOLA et al., 2024; TERRAGNI; ROOP; BLINCOE, 2024). Evidências randomizadas documentam ganho médio de 26,08% nas tarefas concluídas por semana (CUI et al., 2025), e levantamentos setoriais estimam que cerca de 90% dos desenvolvedores já utilizam IA generativa, com cerca de 30% do código novo sendo escrito ou assistido por IA em grandes empresas (DORA; GOOGLE CLOUD, 2025; ALURA, 2026).

## 10.2 Principais achados

A pesquisa produziu quatro achados principais. Primeiro, a evidência de produtividade é robusta, porém condicionada: o ganho concentra-se em tarefas bem delimitadas e beneficia mais desenvolvedores menos experientes, enquanto tarefas de alta incerteza permanecem imunes à automação (CUI et al., 2025; DORA; GOOGLE CLOUD, 2025). Segundo, a segurança do código gerado é a fragilidade central: benchmarks como CyberSecEval 3 e SeCodePLT documentam código inseguro em 35% a 65% dos casos, agravado pelo paradoxo da confiança e pela iteração sem guardrails (BHATTAHALI et al., 2024; SCHERMANN et al., 2024; PERRY et al., 2022; Snyk, 2025).

Terceiro, a qualidade estrutural do código gerado degrada com o volume: a assinatura de máquina e a Lei Inversa Volume-Qualidade demonstram que o acúmulo de artefatos produzidos por agentes introduz dívida técnica identificável — procedural bloat, God Classes e acoplamento excessivo (ZHU; TSANTALIS; RIGBY, 2026; SANTA MOLISON et al., 2025). Quarto, a padronização avança por protocolos abertos de interoperabilidade — MCP, ACP, A2A e ANP — que organizam a integração agente-ferramenta e agente-agente em camadas complementares, ainda em consolidação (NASCIMENTO et al., 2025; ANTHROPIC, 2025).

## 10.3 Implicações práticas

Para a prática da engenharia de software, os resultados implicam recomendações concretas. A adoção de ferramentas de IA deve ser precedida por instrumentação, com métricas de produtividade, qualidade e segurança definidas antes do início (CUI et al., 2025; STRAY et al., 2025). O código gerado exige guardrails obrigatórios: análise estática (SAST), testes de segurança e revisão humana, como adotado pela Amazon (ALURA, 2026; ENDOR LABS, 2025). A autonomia de agentes deve ser escalada gradualmente, com limites explícitos e rastreabilidade de decisões (JIANG et al., 2025; STRAY et al., 2025).

Para as equipes, a capacitação deve deslocar-se da proficiência sintática para a orquestração: especificar tarefas, avaliar artefatos gerados e intervir nos pontos de exceção (JIANG et al., 2025; TEQNOVOS, 2025). Para a seleção de ferramentas, benchmarks públicos como o SWE-bench Verified devem ser complementados por avaliações no domínio da organização e por telemetria de produção, evitando decisões baseadas em percepções subjetivas (JIMENEZ et al., 2024; BENCHLM.AI, 2026; TOOLBOXKART, 2026).

## 10.4 Limitações da pesquisa

Esta pesquisa apresenta limitações reconhecidas. A primeira é a dependência da literatura disponível até o período de levantamento: o campo evolui rapidamente, e parte dos resultados reportados pode tornar-se obsoleta em poucos meses (BENCHLM.AI, 2026). A segunda é a heterogeneidade metodológica das fontes: a análise combinou ensaios randomizados, estudos longitudinais, relatórios setoriais e materiais de fornecedores, com diferentes níveis de rigor (DORA; GOOGLE CLOUD, 2025; TOOLBOXKART, 2026). A terceira é a concentração de benchmarks em ecossistemas de linguagens específicos, limitando a generalização para outros domínios (JIMENEZ et al., 2024; GUO et al., 2025).

## 10.5 Desdobramentos futuros

A pesquisa sugere direções de investigação futura. No plano técnico, são promissoras: a consolidação de protocolos de interoperabilidade e seus efeitos sobre a adoção corporativa (NASCIMENTO et al., 2025); o desenvolvimento de benchmarks que incorporem custo, processo e atributos emergentes da prática real (GUO et al., 2025; BENCHLM.AI, 2026); e a mitigação da assinatura de máquina por técnicas de geração orientada à manutenibilidade (ZHU; TSANTALIS; RIGBY, 2026; SANTA MOLISON et al., 2025). No plano organizacional, destacam-se: estudos longitudinais de longo prazo sobre dívida técnica acumulada (ZHU; TSANTALIS; RIGBY, 2026; NAV IT, 2025); avaliação de programas de capacitação em orquestração de agentes (JIANG et al., 2025; TEQNOVOS, 2025); e a análise de governança da autonomia de agentes em ambientes regulados (ALURA, 2026; ENDOR LABS, 2025).

## 10.6 Conclusão

O AI Driven Development consolida-se como paradigma operacional da engenharia de software: a evidência de ganho de produtividade é real, mas condicionada a guardrails de qualidade, segurança e governança (CUI et al., 2025; DORA; GOOGLE CLOUD, 2025). A resposta da indústria combina protocolos abertos de interoperabilidade, benchmarks cada vez mais robustos e políticas explícitas de revisão e autonomia (NASCIMENTO et al., 2025; JIMENEZ et al., 2024; ALURA, 2026). A conclusão central desta pesquisa é que o sucesso da adoção de IA na engenharia de software não depende da capacidade dos modelos, mas da capacidade das organizações de orquestrá-los: mensurar, validar, revisar e integrar agentes ao processo produtivo humano (STRAY et al., 2025; JIANG et al., 2025; GUO et al., 2025).

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

NAV IT. Adopting GitHub Copilot in a Large Public Sector Organization: A Longitudinal Study. 2025. Disponível em: https://arxiv.org/abs/2509.20353. Acesso em: 08 ago. 2026.

SNYK. AI Code Generation: Code Security & Quality, Benefits, Risks & Tools. 2025. Disponível em: https://snyk.io/blog/ai-code-generation-code-security-quality-benefits-risks-top-tools/. Acesso em: 08 ago. 2026.

TEQNOVOS. Top Trends in Large Language Models (LLMs) for Software Development. 2025. Disponível em: https://teqnovos.com/blog/top-trends-in-large-language-models-llms-for-software-development-in-2026/. Acesso em: 08 ago. 2026.

TERRAGNI, Valerio; ROOP, Partha; BLINCOE, Kelly. The Future of Software Engineering in an AI-Driven World. 2024. Disponível em: https://arxiv.org/abs/2406.07737. Acesso em: 08 ago. 2026.

TOOLBOXKART. OpenAI Codex vs GitHub Copilot vs Claude Code (2026). 2026. Disponível em: https://toolboxkart.tech/blog/codex-vs-github-copilot-vs-claude-code/. Acesso em: 08 ago. 2026.

ZHU, Yuecai; TSANTALIS, Nikolaos; RIGBY, Peter C. AI-Generated Smells: An Analysis of Code and Architecture in LLM- and Agent-Driven Development. 2026. Disponível em: https://arxiv.org/abs/2605.02741. Acesso em: 08 ago. 2026.