# 8 Qualidade, Segurança e Dívida Técnica do Código Gerado

## 8.1 Corretude funcional versus qualidade estrutural

A avaliação automatizada de agentes de IA concentrou-se historicamente na corretude funcional — se o código gerado resolve a tarefa proposta, aferida por testes. A evidência acumulada, contudo, demonstra que corretude e qualidade estrutural são dimensões distintas: código que passa nos testes funcionais pode apresentar bugs latentes, vulnerabilidades exploráveis e arquitetura de baixa manutenibilidade (SABRA et al., 2025; SANTA MOLISON et al., 2025). Estudo da SonarQube com 4.442 tarefas Java constatou que mesmo soluções funcionalmente corretas carregam probabilidade de 5% a 8% de conter bugs e cerca de 2% de conter vulnerabilidades (SABRA et al., 2025).

Pesquisa dedicada à manutenibilidade comparou código gerado por LLMs com código escrito por humanos, concluindo que as diferenças mais relevantes situam-se na complexidade ciclomática, no acoplamento entre classes e na legibilidade — atributos que não aparecem em testes funcionais, mas determinam o custo de manutenção ao longo do ciclo de vida (SANTA MOLISON et al., 2025). A implicação prática é direta: processos de adoção de IA que validam exclusivamente por testes automatizados aprovam código com qualidade estrutural inferior, transferindo o custo para a manutenção futura (SANTA MOLISON et al., 2025; GUO et al., 2025).

## 8.2 Insegurança por padrão: evidências de benchmarks de segurança

A dimensão de segurança concentra as evidências mais robustas de degradação. O CyberSecEval 3, da Meta, demonstrou que modelos líderes produzem código inseguro em 35% a 40% das tarefas, com falhas recorrentes de validação de entrada (CWE-20), injeção de SQL (CWE-89), injeção de comandos (CWE-78), credenciais embutidas no código, path traversal e dependências alucinadas (BHATTAHALI et al., 2024; Snyk, 2025). O SeCodePLT estimou que 40% a 65% das amostras de código gerado contêm vulnerabilidades (SCHERMANN et al., 2024). Avaliação focada em PHP revelou vulnerabilidades e limitações específicas de ecossistemas web menos cobertos pelos corpora de treinamento (VAVEKANAND et al., 2024).

O panorama é agravado pelo "paradoxo da confiança": desenvolvedores que utilizam assistentes de IA consideram seu código mais seguro precisamente quando ele apresenta mais vulnerabilidades (PERRY et al., 2022; Snyk, 2025). O refinamento iterativo agrava o quadro: cinco rodadas de refinamento com IA elevaram a proporção de vulnerabilidades críticas em aproximadamente 38% sobre código inicialmente seguro (Snyk, 2025). A interpretação mais aceita é que os ciclos de iteração otimizam a adequação funcional do código ao teste — e não sua postura de segurança, que permanece dependente do padrão estatístico do modelo (Snyk, 2025; SCHERMANN et al., 2024).

## 8.3 Dívida técnica e a "assinatura de máquina"

A dimensão mais recente da literatura é a dívida técnica estrutural. Análise de código gerado por LLMs em larga escala identificou uma "assinatura de máquina": o código produzido por agentes acumula padrões de procedural bloat, God Classes, acoplamento excessivo e ausência de camadas de abstração — características estatisticamente distinguíveis do código escrito por humanos (ZHU; TSANTALIS; RIGBY, 2026). A contribuição central do estudo é a chamada Lei Inversa Volume-Qualidade: quanto maior o volume de código gerado por máquinas em um repositório, menor a qualidade estrutural média do conjunto, em contraste com a relação convencional observada em código humano (ZHU; TSANTALIS; RIGBY, 2026).

A metáfora da assinatura é operacionalmente útil: se o código gerado tem características estatísticas identificáveis, ele também pode ser detectado, monitorado e mitigado por ferramentas de análise estática e por políticas de revisão (ZHU; TSANTALIS; RIGBY, 2026; ENDOR LABS, 2025). A dívida técnica, nesse contexto, deixa de ser um conceito difuso e passa a ser mensurável: proporção de código gerado, densidade de padrões de acoplamento, complexidade ciclomática média e débito de refatoração estimado (SANTA MOLISON et al., 2025; ZHU; TSANTALIS; RIGBY, 2026).

## 8.4 Guardrails organizacionais e técnicos

A resposta prática combina guardrails técnicos e organizacionais. No plano técnico, a literatura e os relatos corporativos convergem para: (i) análise estática obrigatória em todo código gerado, com gates de segurança (SAST) e varredura de dependências (Snyk, 2025; ENDOR LABS, 2025); (ii) testes dinâmicos e de regressão ampliados, incluindo testes de segurança (BHATTAHALI et al., 2024); e (iii) medição contínua de qualidade estrutural, com metas de complexidade e cobertura (SANTA MOLISON et al., 2025; ZHU; TSANTALIS; RIGBY, 2026).

No plano organizacional, os padrões observados incluem revisão humana obrigatória para código gerado, como na política da Amazon que exige revisão de engenheiro sênior antes do merge (ALURA, 2026); limites de autonomia para agentes, diferenciando tarefas delegáveis das que exigem aprovação (STRAY et al., 2025); e instrumentação de produção com métricas de densidade de defeitos introduzidos por origem de código — humano ou gerado (CUI et al., 2025; ENDOR LABS, 2025). A existência desses guardrails não elimina o risco, mas o torna mensurável e gerenciável (Snyk, 2025; ALURA, 2026).

## 8.5 Síntese parcial

Esta seção examinou as dimensões de qualidade, segurança e dívida técnica do código gerado. Ficou evidenciado que (i) corretude funcional não implica qualidade estrutural, com riscos mensuráveis de bugs latentes e vulnerabilidades; (ii) benchmarks de segurança documentam insegurança por padrão em 35% a 65% dos casos, agravada pelo paradoxo da confiança e pela iteração sem guardrails; (iii) a assinatura de máquina e a Lei Inversa Volume-Qualidade demonstram que código gerado acumula dívida técnica estrutural identificável; e (iv) guardrails técnicos (SAST, testes, medição) e organizacionais (revisão humana, limites de autonomia, telemetria) configuram a resposta prática da indústria (ZHU; TSANTALIS; RIGBY, 2026; Snyk, 2025; ALURA, 2026). A próxima seção examina a produtividade e o impacto organizacional da adoção (CUI et al., 2025; STRAY et al., 2025).

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

HONG, Sirui et al. MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework. ICLR, 2024. Disponível em: https://arxiv.org/abs/2308.00352. Acesso em: 08 ago. 2026.

SNYK. AI Code Generation: Code Security & Quality, Benefits, Risks & Tools. 2025. Disponível em: https://snyk.io/blog/ai-code-generation-code-security-quality-benefits-risks-top-tools/. Acesso em: 08 ago. 2026.

ZHU, Yuecai; TSANTALIS, Nikolaos; RIGBY, Peter C. AI-Generated Smells: An Analysis of Code and Architecture in LLM- and Agent-Driven Development. 2026. Disponível em: https://arxiv.org/abs/2605.02741. Acesso em: 08 ago. 2026.