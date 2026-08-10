# 9 Produtividade e Impacto Organizacional da Adoção de IA

## 9.1 Evidência experimental de ganhos de produtividade

A questão central da adoção de IA na engenharia de software é empírica: ferramentas generativas aumentam efetivamente a produtividade? A evidência mais robusta provém de estudos randomizados controlados (RCTs) — o padrão-ouro de inferência causal. Estudo conduzido com 4.867 desenvolvedores da Microsoft, da Accenture e de empresas Fortune 100 randomizou participantes entre uso e não uso do GitHub Copilot, registrando aumento de 26,08% nas tarefas concluídas por semana, medido por pull requests, commits e builds (CUI et al., 2025). O ganho foi heterogêneo: desenvolvedores menos experientes obtiveram os maiores incrementos, enquanto profissionais seniores apresentaram ganhos menores, possivelmente em razão de fluxos de trabalho já otimizados (CUI et al., 2025; INFOQ, 2024).

A robustez do resultado decorre do desenho experimental: a randomização controla variáveis de confusão (perfil do desenvolvedor, complexidade da tarefa, contexto do projeto), permitindo atribuir a diferença à intervenção (CUI et al., 2025). Estudos correlacionais e surveys corporativos corroboram a direção do efeito, embora com menor rigor causal (INFOQ, 2024; TOOLBOXKART, 2026). O levantamento anual da DORA reforça o panorama: cerca de 90% dos desenvolvedores já utilizam IA generativa em algum grau, e a percepção dominante é a de que a IA atua como amplificador de desempenho — acelerando a execução de tarefas conhecidas — sem substituir o julgamento humano (DORA; GOOGLE CLOUD, 2025).

## 9.2 Onde a produtividade aumenta e onde não muda

A análise fina das evidências sugere que o ganho de produtividade concentra-se em tarefas bem delimitadas: geração de código boilerplate, escrita de testes, documentação, refatoração mecânica e prototipagem (CUI et al., 2025; GUO et al., 2025). Nessas tarefas, o assistente reduz o tempo de digitação e de busca, liberando atenção do desenvolvedor para decisões de design (STRAY et al., 2025). O custo oculto documentado é a verificação: sugestões precisam ser lidas, compreendidas e testadas, e o tempo de verificação pode compensar parte do ganho de escrita — fenômeno observado no estudo longitudinal da NAV IT, que registrou custo de verificação das sugestões e adoção heterogênea entre engenheiros (NAV IT, 2025).

Em tarefas de alta incerteza — arquitetura, integração entre sistemas legados, análise de requisitos ambíguos e incidentes de produção — as evidências de ganho são fracas ou inexistentes (DORA; GOOGLE CLOUD, 2025; STRAY et al., 2025). A literatura converge para uma leitura qualificada: a IA generativa não é uma solução de produtividade em si, mas um amplificador que potencializa processos já bem estruturados (DORA; GOOGLE CLOUD, 2025). Organizações com pipelines de CI/CD maduros, testes automatizados e revisão disciplinada extraem mais valor da adoção do que organizações sem essas bases (DORA; GOOGLE CLOUD, 2025; CUI et al., 2025).

## 9.3 Impacto sobre habilidades e dinâmica de equipes

A adoção de IA altera o mapa de habilidades da engenharia de software. A capacidade de especificar, delegar e avaliar trabalho de agentes — competências de orquestração — ganha relevância relativa, enquanto a proficiência em sintaxe e APIs específicas perde peso (JIANG et al., 2025; TEQNOVOS, 2025). O estudo longitudinal da NAV IT documentou ceticismo entre desenvolvedores seniores e adoção entusiástica entre juniores, sugerindo que a tecnologia pode alterar a distribuição de influência técnica nas equipes (NAV IT, 2025). O efeito sobre a trajetória de aprendizado é ambíguo: ferramentas de IA aceleram a resolução de tarefas, mas podem reduzir o contato com o erro e a reflexão que sustentam o aprendizado profundo (STRAY et al., 2025; GUO et al., 2025).

A literatura também aponta mudança nos padrões de colaboração: revisão de código, originalmente centrada em humanos, passa a incluir a revisão de artefatos gerados por agentes — pull requests produzidos por IA, patches sugeridos e testes sintetizados (ALURA, 2026; STRAY et al., 2025). Políticas como a revisão obrigatória por engenheiro sênior na Amazon configuram a resposta organizacional a essa nova modalidade de trabalho (ALURA, 2026). O papel do revisor desloca-se da verificação de conformidade sintática para a validação de intenção, arquitetura e segurança (ZHU; TSANTALIS; RIGBY, 2026; ENDOR LABS, 2025).

## 9.4 Riscos organizacionais e condições de sucesso

A adoção de IA carrega riscos organizacionais documentados. O primeiro é o risco de segurança: o paradoxo da confiança demonstra que a percepção de segurança aumenta na mesma proporção em que o código gerado acumula vulnerabilidades (PERRY et al., 2022; Snyk, 2025). O segundo é o risco de dívida técnica estrutural: a assinatura de máquina e a Lei Inversa Volume-Qualidade indicam que o acúmulo de código gerado degrada a qualidade estrutural média do repositório (ZHU; TSANTALIS; RIGBY, 2026). O terceiro é o risco de medição: métricas de produtividade por linhas de código ou por commits tornam-se enganosas quando grande parte do código é gerada e apenas revisada por humanos (STRAY et al., 2025; DORA; GOOGLE CLOUD, 2025).

As condições de sucesso emergem das evidências: (i) instrumentação prévia, com métricas definidas antes da adoção (CUI et al., 2025); (ii) guardrails de segurança, com análise estática obrigatória e testes de segurança do código gerado (Snyk, 2025; ENDOR LABS, 2025); (iii) política explícita de revisão e limites de autonomia para agentes (ALURA, 2026; STRAY et al., 2025); e (iv) programas de capacitação que formem a competência de orquestração de agentes e de avaliação crítica de artefatos gerados (JIANG et al., 2025; TEQNOVOS, 2025). A combinação dessas condições transforma a adoção de IA de experimento individual em decisão organizacional gerenciável (DORA; GOOGLE CLOUD, 2025).

## 9.5 Síntese parcial

Esta seção examinou a evidência de produtividade e o impacto organizacional da adoção de IA. Ficou evidenciado que (i) RCTs documentam ganho médio de 26,08% nas tarefas concluídas por semana, concentrado em tarefas bem delimitadas e em desenvolvedores menos experientes; (ii) o ganho exige verificação, que consome parte do tempo economizado, e praticamente não ocorre em tarefas de alta incerteza; (iii) a IA reconfigura habilidades e dinâmica de equipes, com a orquestração substituindo parte da proficiência sintática e políticas de revisão obrigatória emergindo como norma; e (iv) o sucesso da adoção depende de instrumentação, guardrails de segurança, políticas de revisão e capacitação — condições que transformam o uso individual em estratégia organizacional (CUI et al., 2025; DORA; GOOGLE CLOUD, 2025; STRAY et al., 2025). A próxima e última seção consolida as conclusões e os desdobramentos futuros da pesquisa (ZHU; TSANTALIS; RIGBY, 2026; Snyk, 2025).

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

INFOQ. Study Shows AI Coding Assistant Improves Developer Productivity. 2024. Disponível em: https://www.infoq.com/news/2024/09/copilot-developer-productivity. Acesso em: 08 ago. 2026.

NAV IT. Adopting GitHub Copilot in a Large Public Sector Organization: A Longitudinal Study. 2025. Disponível em: https://arxiv.org/abs/2509.20353. Acesso em: 08 ago. 2026.

SNYK. AI Code Generation: Code Security & Quality, Benefits, Risks & Tools. 2025. Disponível em: https://snyk.io/blog/ai-code-generation-code-security-quality-benefits-risks-top-tools/. Acesso em: 08 ago. 2026.

TEQNOVOS. Top Trends in Large Language Models (LLMs) for Software Development. 2025. Disponível em: https://teqnovos.com/blog/top-trends-in-large-language-models-llms-for-software-development-in-2026/. Acesso em: 08 ago. 2026.

TOOLBOXKART. OpenAI Codex vs GitHub Copilot vs Claude Code (2026). 2026. Disponível em: https://toolboxkart.tech/blog/codex-vs-github-copilot-vs-claude-code/. Acesso em: 08 ago. 2026.

ZHU, Yuecai; TSANTALIS, Nikolaos; RIGBY, Peter C. AI-Generated Smells: An Analysis of Code and Architecture in LLM- and Agent-Driven Development. 2026. Disponível em: https://arxiv.org/abs/2605.02741. Acesso em: 08 ago. 2026.