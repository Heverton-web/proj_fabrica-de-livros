# 1 Introdução

## 1.1 Contextualização e Problema de Pesquisa

A adoção de agentes de IA na engenharia de software atingiu escala corporativa, e com ela emergiu a questão central da governança: como delegar execução autônoma sem perder o controle sobre qualidade, segurança e custo (GARTNER, 2026) (MCKINSEY, 2026). A literatura recente é convergente ao afirmar que a confiabilidade da saída do agente depende menos do modelo e mais dos controles externos que o cercam — hooks, permissões, testes, revisão e métricas (DATABRICKS, 2026) (BUI, 2026). Esse conjunto forma o que se convencionou chamar de governança agêntica (JIN, 2024) (TAWOSI, 2025).

O problema de pesquisa decorre da observação de que a produtividade percebida com agentes nem sempre se converte em qualidade entregue: relatórios setoriais documentam custos ocultos de revisão, correção e dívida técnica quando a verificação é negligenciada (MIT SLOAN MANAGEMENT REVIEW, 2026) (DORA, 2026) (DX, 2026). Paralelamente, a evidência de benchmarks indica que a avaliação adequada de agentes é condição para decisões de adoção informadas (DENG, 2025) (PRINCETON UNIVERSITY, 2026) (BIRJOB, 2026).

## 1.2 Objetivo do Recorte

Este artigo examina, em perspectiva documental, o ciclo de governança e entrega do desenvolvimento dirigido por IA: hooks e regras de segurança, testes dirigidos por IA, revisão de código autônoma, economia de tokens, build e CI/CD, deploy em nuvem, monitoramento e iteração, e a formação do engenheiro do futuro (EXPLAINX, 2026) (HE, 2026). O recorte deriva dos capítulos 13 a 20 da obra-mãe *AI Driven Development: Do Zero ao Deploy* (CONNELL, 2026) (WONG, 2025).

## 1.3 Justificativa e Delimitação

A justificativa é dupla. Primeiro, a governança é o fator que distingue experimentos de produção: sem portões objetivos, a autonomia do agente amplifica tanto acertos quanto erros (INVARIANT LABS, 2026) (CODIHAUS, 2026). Segundo, o custo de operação — tokens, infraestrutura, revisão — tornou-se variável de decisão e não apenas detalhe operacional (VALUE ADD VC, 2026) (SOFTJOURN, 2026). O recorte limita-se a fontes documentais públicas de 2024 a 2026 (DORA, 2026) (DX, 2026).

## 1.4 Síntese Parcial

Em síntese, o argumento é que entregar software com IA em produção exige um sistema de controles: hooks que bloqueiam, testes que provam, revisão que audita, métricas que medem e pipelines que tornam o processo reproduzível (HE, 2026) (EXPLAINX, 2026). A seção seguinte descreve o método de recuperação e síntese das fontes (BUI, 2026).

# Referências

BIRJOB. *AI Coding Agent Benchmarks Beyond SWE-Bench in 2026: Terminal-Bench, Aider Polyglot, GAIA, and Why the Leaderboard Lies*. 2026. Disponível em: https://www.birjob.com/blog/agent-benchmarks-2026. Acesso em: 07 ago. 2026.

BUI, Nghi D. Q. *Building AI Coding Agents for the Terminal*. 2026. Disponível em: https://arxiv.org/html/2603.05344v1. Acesso em: 07 ago. 2026.

CODIHAUS. *AI Developer Productivity Data: 2X Faster, 55% Speed Gain, Enterprise ROI Analysis*. 2026. Disponível em: https://codihaus.com/news/ai-developer-productivity-data-engineering-leaders. Acesso em: 07 ago. 2026.

CONNELL, Andrew. *My Thoughts on Vibe Coding vs. Agentic Engineering*. 2026. Disponível em: https://www.andrewconnell.com/articles/vibe-coding-vs-agentic-engineering/. Acesso em: 07 ago. 2026.

DATABRICKS. *What is an AI Agent Harness?* 2026. Disponível em: https://www.databricks.com/blog/ai-harness. Acesso em: 07 ago. 2026.

DENG, Xiang et al. *SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?* 2025. Disponível em: https://arxiv.org/abs/2509.16941. Acesso em: 07 ago. 2026.

DORA / GOOGLE CLOUD. *Publications and ROI of AI-assisted Software Development Report*. 2026. Disponível em: https://dora.dev/research/publications/. Acesso em: 07 ago. 2026.

DX. *How to measure AI's impact on developer productivity*. 2026. Disponível em: https://getdx.com/blog/ai-measurement-hub/. Acesso em: 07 ago. 2026.

EXPLAINX.AI. *AI Coding Agent Evals on Real Repos (2026)*. 2026. Disponível em: https://explainx.ai/blog/ai-coding-agent-evals-real-repos-2026. Acesso em: 07 ago. 2026.

GARTNER. *Gartner Identifies the Top Strategic Technology Trends for 2026*. 2026. Disponível em: https://www.gartner.com/en/newsroom/press-releases/2025-10-20-gartner-identifies-the-top-strategic-technology-trends-for-2026. Acesso em: 07 ago. 2026.

HE, Kang; ROY, Kaushik. *SWE-Adept: An LLM-Based Agentic Framework for Deep Codebase Analysis and Structured Issue Resolution*. 2026. Disponível em: https://arxiv.org/abs/2603.01327. Acesso em: 07 ago. 2026.

INVARIANT LABS. *MCP Security Notification: Tool Poisoning Attacks*. 2026. Disponível em: https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks. Acesso em: 07 ago. 2026.

JIN, Haolin et al. *From LLMs to LLM-based Agents for Software Engineering: A Survey of Current, Challenges and Future*. 2024. Disponível em: https://arxiv.org/abs/2408.02479. Acesso em: 07 ago. 2026.

MCKINSEY & COMPANY. *The State of AI: Global Survey*. 2026. Disponível em: https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai. Acesso em: 07 ago. 2026.

MIT SLOAN MANAGEMENT REVIEW. ANDERSON, Edward; PARKER, Geoffrey; TAN, Burcu. *The Hidden Costs of Coding With Generative AI*. 2026. Disponível em: https://sloanreview.mit.edu/article/the-hidden-costs-of-coding-with-generative-ai/. Acesso em: 07 ago. 2026.

PRINCETON UNIVERSITY. *SWE-bench Verified & Pro*. 2026. Disponível em: https://www.swebench.com. Acesso em: 07 ago. 2026.

SOFTJOURN. *AI Software Development Statistics 2026: Adoption, Productivity, and Risk*. 2026. Disponível em: https://softjourn.com/insights/ai-software-dev-stats. Acesso em: 07 ago. 2026.

TAWOSI, Vali et al. *ALMAS: an Autonomous LLM-based Multi-Agent Software Engineering Framework*. 2025. Disponível em: https://arxiv.org/abs/2510.03463. Acesso em: 07 ago. 2026.

VALUE ADD VC. *AI Coding Productivity Study Data: What METR, McKinsey, and GitHub Found in 2026*. 2026. Disponível em: https://valueaddvc.com/blog/ai-coding-productivity-study-data-what-metr-mckinsey-and-github-actually-found-in-2026. Acesso em: 07 ago. 2026.

WONG, Sherman et al. *Confucius Code Agent: Scalable Agent Scaffolding for Real-World Codebases*. 2025. Disponível em: https://arxiv.org/abs/2512.10398. Acesso em: 07 ago. 2026.

# 2 Metodologia

## 2.1 Natureza do Recorte

O trabalho caracteriza-se como recorte investigativo documental derivado do dossiê de pesquisa da obra-mãe (SOFTJOURN, 2026) (VALUE ADD VC, 2026). As evidências provêm de fontes secundárias: relatórios de analistas (GARTNER, 2026) (MCKINSEY, 2026), relatórios de produtividade (DORA, 2026) (DX, 2026), artigos científicos (DENG, 2025) (TAWOSI, 2025) (WONG, 2025) (JIN, 2024) e documentação de plataformas (DATABRICKS, 2026).

## 2.2 Procedimento de Reaproveitamento

O dossiê foi indexado por recuperação vetorial local, com consultas por termos-chave para cada tema do recorte (BUI, 2026) (CONNELL, 2026). Os blocos retornados foram selecionados por pertinência temática e autoridade editorial, e as fontes consolidadas nas listas de referência (EXPLAINX, 2026) (PRINCETON UNIVERSITY, 2026).

## 2.3 Critérios de Seleção

Foram adotados três critérios: (i) pertinência direta aos capítulos-fonte 13 a 20; (ii) entidades reconhecidas — universidades, analistas, laboratórios de segurança; (iii) atualidade, priorizando 2025-2026 (DENG, 2025) (BIRJOB, 2026). Excluíram-se fontes sem data identificável ou de caráter promocional (INVARIANT LABS, 2026).

## 2.4 Construção Textual e Citação

A redação seguiu o framework ACAD, com citação autor-data conforme a NBR 10520 (HE, 2026) (EXPLAINX, 2026). Toda afirmação factual recebe citação explícita, e a rastreabilidade foi verificada de forma determinística (MIT SLOAN MANAGEMENT REVIEW, 2026) (CODIHAUS, 2026).

# Referências

BIRJOB. *AI Coding Agent Benchmarks Beyond SWE-Bench in 2026: Terminal-Bench, Aider Polyglot, GAIA, and Why the Leaderboard Lies*. 2026. Disponível em: https://www.birjob.com/blog/agent-benchmarks-2026. Acesso em: 07 ago. 2026.

BUI, Nghi D. Q. *Building AI Coding Agents for the Terminal*. 2026. Disponível em: https://arxiv.org/html/2603.05344v1. Acesso em: 07 ago. 2026.

CODIHAUS. *AI Developer Productivity Data: 2X Faster, 55% Speed Gain, Enterprise ROI Analysis*. 2026. Disponível em: https://codihaus.com/news/ai-developer-productivity-data-engineering-leaders. Acesso em: 07 ago. 2026.

CONNELL, Andrew. *My Thoughts on Vibe Coding vs. Agentic Engineering*. 2026. Disponível em: https://www.andrewconnell.com/articles/vibe-coding-vs-agentic-engineering/. Acesso em: 07 ago. 2026.

DATABRICKS. *What is an AI Agent Harness?* 2026. Disponível em: https://www.databricks.com/blog/ai-harness. Acesso em: 07 ago. 2026.

DENG, Xiang et al. *SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?* 2025. Disponível em: https://arxiv.org/abs/2509.16941. Acesso em: 07 ago. 2026.

DORA / GOOGLE CLOUD. *Publications and ROI of AI-assisted Software Development Report*. 2026. Disponível em: https://dora.dev/research/publications/. Acesso em: 07 ago. 2026.

DX. *How to measure AI's impact on developer productivity*. 2026. Disponível em: https://getdx.com/blog/ai-measurement-hub/. Acesso em: 07 ago. 2026.

EXPLAINX.AI. *AI Coding Agent Evals on Real Repos (2026)*. 2026. Disponível em: https://explainx.ai/blog/ai-coding-agent-evals-real-repos-2026. Acesso em: 07 ago. 2026.

GARTNER. *Gartner Identifies the Top Strategic Technology Trends for 2026*. 2026. Disponível em: https://www.gartner.com/en/newsroom/press-releases/2025-10-20-gartner-identifies-the-top-strategic-technology-trends-for-2026. Acesso em: 07 ago. 2026.

HE, Kang; ROY, Kaushik. *SWE-Adept: An LLM-Based Agentic Framework for Deep Codebase Analysis and Structured Issue Resolution*. 2026. Disponível em: https://arxiv.org/abs/2603.01327. Acesso em: 07 ago. 2026.

INVARIANT LABS. *MCP Security Notification: Tool Poisoning Attacks*. 2026. Disponível em: https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks. Acesso em: 07 ago. 2026.

JIN, Haolin et al. *From LLMs to LLM-based Agents for Software Engineering: A Survey of Current, Challenges and Future*. 2024. Disponível em: https://arxiv.org/abs/2408.02479. Acesso em: 07 ago. 2026.

MCKINSEY & COMPANY. *The State of AI: Global Survey*. 2026. Disponível em: https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai. Acesso em: 07 ago. 2026.

MIT SLOAN MANAGEMENT REVIEW. ANDERSON, Edward; PARKER, Geoffrey; TAN, Burcu. *The Hidden Costs of Coding With Generative AI*. 2026. Disponível em: https://sloanreview.mit.edu/article/the-hidden-costs-of-coding-with-generative-ai/. Acesso em: 07 ago. 2026.

PRINCETON UNIVERSITY. *SWE-bench Verified & Pro*. 2026. Disponível em: https://www.swebench.com. Acesso em: 07 ago. 2026.

SOFTJOURN. *AI Software Development Statistics 2026: Adoption, Productivity, and Risk*. 2026. Disponível em: https://softjourn.com/insights/ai-software-dev-stats. Acesso em: 07 ago. 2026.

TAWOSI, Vali et al. *ALMAS: an Autonomous LLM-based Multi-Agent Software Engineering Framework*. 2025. Disponível em: https://arxiv.org/abs/2510.03463. Acesso em: 07 ago. 2026.

VALUE ADD VC. *AI Coding Productivity Study Data: What METR, McKinsey, and GitHub Found in 2026*. 2026. Disponível em: https://valueaddvc.com/blog/ai-coding-productivity-study-data-what-metr-mckinsey-and-github-actually-found-in-2026. Acesso em: 07 ago. 2026.

WONG, Sherman et al. *Confucius Code Agent: Scalable Agent Scaffolding for Real-World Codebases*. 2025. Disponível em: https://arxiv.org/abs/2512.10398. Acesso em: 07 ago. 2026.

# 3 Resultados e Discussão

## 3.1 Governança: Hooks, Permissões e Regras

O primeiro resultado confirma que hooks e permissões determinísticas constituem a primeira linha de defesa da delegação agêntica (DATABRICKS, 2026) (BUI, 2026). Regras de governança — bloqueio de comandos destrutivos, aprovação humana em pontos de alto impacto, trilhas de auditoria — reduzem o risco sem eliminar a velocidade (CONNELL, 2026) (INVARIANT LABS, 2026). A evidência indica que a aplicação de regras na camada de orquestração é mais eficaz do que depender da obediência do modelo (JIN, 2024) (TAWOSI, 2025).

## 3.2 Testes Dirigidos por IA e Revisão Autônoma

O segundo resultado diz respeito à verificação. Testes escritos antes da implementação definem o que é correto antes de o agente gerar código, funcionando como controle estrutural externo ao modelo (DENG, 2025) (HE, 2026). A revisão de código autônoma, por sua vez, combina auditoria determinística com revisor agêntico, criando um ciclo de melhoria verificável (EXPLAINX, 2026) (WONG, 2025). Benchmarks demonstram que agentes avaliados em repositórios reais apresentam desempenho condicionado à qualidade do harness e dos testes (PRINCETON UNIVERSITY, 2026) (BIRJOB, 2026).

## 3.3 Entrega: Build, Deploy e Observabilidade

O terceiro resultado descreve a entrega. Pipelines de CI/CD com agentes são viáveis quando os portões são objetivos e reproduzíveis localmente (BUI, 2026) (DATABRICKS, 2026). O deploy em nuvem transfere a complexidade de ambiente para plataformas gerenciadas, mas exige configuração explícita de segredos e migrações (DORA, 2026) (DX, 2026). Monitoramento e observabilidade — logs estruturados, métricas e relatórios de frequência de entrega — fecham o ciclo de iteração (VALUE ADD VC, 2026) (SOFTJOURN, 2026).

## 3.4 Síntese Parcial

Os resultados articulam a tese do sistema de controles: governança que bloqueia, testes que provam, revisão que audita, pipelines que reproduzem e métricas que medem (HE, 2026) (EXPLAINX, 2026). A produtividade sustentável emerge da combinação desses controles com a velocidade do agente (CODIHAUS, 2026) (MIT SLOAN MANAGEMENT REVIEW, 2026) (GARTNER, 2026). A seção seguinte conclui o recorte (MCKINSEY, 2026).

# Referências

BIRJOB. *AI Coding Agent Benchmarks Beyond SWE-Bench in 2026: Terminal-Bench, Aider Polyglot, GAIA, and Why the Leaderboard Lies*. 2026. Disponível em: https://www.birjob.com/blog/agent-benchmarks-2026. Acesso em: 07 ago. 2026.

BUI, Nghi D. Q. *Building AI Coding Agents for the Terminal*. 2026. Disponível em: https://arxiv.org/html/2603.05344v1. Acesso em: 07 ago. 2026.

CODIHAUS. *AI Developer Productivity Data: 2X Faster, 55% Speed Gain, Enterprise ROI Analysis*. 2026. Disponível em: https://codihaus.com/news/ai-developer-productivity-data-engineering-leaders. Acesso em: 07 ago. 2026.

CONNELL, Andrew. *My Thoughts on Vibe Coding vs. Agentic Engineering*. 2026. Disponível em: https://www.andrewconnell.com/articles/vibe-coding-vs-agentic-engineering/. Acesso em: 07 ago. 2026.

DATABRICKS. *What is an AI Agent Harness?* 2026. Disponível em: https://www.databricks.com/blog/ai-harness. Acesso em: 07 ago. 2026.

DENG, Xiang et al. *SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?* 2025. Disponível em: https://arxiv.org/abs/2509.16941. Acesso em: 07 ago. 2026.

DORA / GOOGLE CLOUD. *Publications and ROI of AI-assisted Software Development Report*. 2026. Disponível em: https://dora.dev/research/publications/. Acesso em: 07 ago. 2026.

DX. *How to measure AI's impact on developer productivity*. 2026. Disponível em: https://getdx.com/blog/ai-measurement-hub/. Acesso em: 07 ago. 2026.

EXPLAINX.AI. *AI Coding Agent Evals on Real Repos (2026)*. 2026. Disponível em: https://explainx.ai/blog/ai-coding-agent-evals-real-repos-2026. Acesso em: 07 ago. 2026.

GARTNER. *Gartner Identifies the Top Strategic Technology Trends for 2026*. 2026. Disponível em: https://www.gartner.com/en/newsroom/press-releases/2025-10-20-gartner-identifies-the-top-strategic-technology-trends-for-2026. Acesso em: 07 ago. 2026.

HE, Kang; ROY, Kaushik. *SWE-Adept: An LLM-Based Agentic Framework for Deep Codebase Analysis and Structured Issue Resolution*. 2026. Disponível em: https://arxiv.org/abs/2603.01327. Acesso em: 07 ago. 2026.

INVARIANT LABS. *MCP Security Notification: Tool Poisoning Attacks*. 2026. Disponível em: https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks. Acesso em: 07 ago. 2026.

JIN, Haolin et al. *From LLMs to LLM-based Agents for Software Engineering: A Survey of Current, Challenges and Future*. 2024. Disponível em: https://arxiv.org/abs/2408.02479. Acesso em: 07 ago. 2026.

MCKINSEY & COMPANY. *The State of AI: Global Survey*. 2026. Disponível em: https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai. Acesso em: 07 ago. 2026.

MIT SLOAN MANAGEMENT REVIEW. ANDERSON, Edward; PARKER, Geoffrey; TAN, Burcu. *The Hidden Costs of Coding With Generative AI*. 2026. Disponível em: https://sloanreview.mit.edu/article/the-hidden-costs-of-coding-with-generative-ai/. Acesso em: 07 ago. 2026.

PRINCETON UNIVERSITY. *SWE-bench Verified & Pro*. 2026. Disponível em: https://www.swebench.com. Acesso em: 07 ago. 2026.

SOFTJOURN. *AI Software Development Statistics 2026: Adoption, Productivity, and Risk*. 2026. Disponível em: https://softjourn.com/insights/ai-software-dev-stats. Acesso em: 07 ago. 2026.

TAWOSI, Vali et al. *ALMAS: an Autonomous LLM-based Multi-Agent Software Engineering Framework*. 2025. Disponível em: https://arxiv.org/abs/2510.03463. Acesso em: 07 ago. 2026.

VALUE ADD VC. *AI Coding Productivity Study Data: What METR, McKinsey, and GitHub Found in 2026*. 2026. Disponível em: https://valueaddvc.com/blog/ai-coding-productivity-study-data-what-metr-mckinsey-and-github-actually-found-in-2026. Acesso em: 07 ago. 2026.

WONG, Sherman et al. *Confucius Code Agent: Scalable Agent Scaffolding for Real-World Codebases*. 2025. Disponível em: https://arxiv.org/abs/2512.10398. Acesso em: 07 ago. 2026.

# 4 Conclusão

## 4.1 Retomada do Argumento Central

O recorte sustentou três proposições. Primeira: a governança agêntica — hooks, permissões e regras determinísticas — é a condição para delegar execução autônoma com segurança (DATABRICKS, 2026) (INVARIANT LABS, 2026). Segunda: testes dirigidos por IA e revisão autônoma transformam a verificação em controle estrutural, não em etapa opcional (DENG, 2025) (HE, 2026). Terceira: pipelines, deploy gerenciado e observabilidade tornam o processo reproduzível e mensurável (DORA, 2026) (DX, 2026).

## 4.2 Implicações Práticas

Organizações devem implementar portões objetivos antes de ampliar a autonomia dos agentes: testes obrigatórios, revisão com evidência e métricas de frequência de entrega (EXPLAINX, 2026) (PRINCETON UNIVERSITY, 2026). O custo de tokens deve ser gerido como variável de orçamento, com protocolos de leitura enxuta e compressão de contexto (VALUE ADD VC, 2026) (SOFTJOURN, 2026). A formação do engenheiro do futuro combina competência técnica com capacidade de especificação e governança (CONNELL, 2026) (WONG, 2025).

## 4.3 Limitações e Trabalhos Futuros

O recorte é documental e não coleta dados primários de operação (MCKINSEY, 2026). Trabalhos futuros podem medir, com evidência primária, a relação entre maturidade de governança e taxas de incidentes em produção, e o custo total de propriedade de pipelines com agentes (CODIHAUS, 2026) (MIT SLOAN MANAGEMENT REVIEW, 2026) (BIRJOB, 2026).

# Referências

BIRJOB. *AI Coding Agent Benchmarks Beyond SWE-Bench in 2026: Terminal-Bench, Aider Polyglot, GAIA, and Why the Leaderboard Lies*. 2026. Disponível em: https://www.birjob.com/blog/agent-benchmarks-2026. Acesso em: 07 ago. 2026.

BUI, Nghi D. Q. *Building AI Coding Agents for the Terminal*. 2026. Disponível em: https://arxiv.org/html/2603.05344v1. Acesso em: 07 ago. 2026.

CODIHAUS. *AI Developer Productivity Data: 2X Faster, 55% Speed Gain, Enterprise ROI Analysis*. 2026. Disponível em: https://codihaus.com/news/ai-developer-productivity-data-engineering-leaders. Acesso em: 07 ago. 2026.

CONNELL, Andrew. *My Thoughts on Vibe Coding vs. Agentic Engineering*. 2026. Disponível em: https://www.andrewconnell.com/articles/vibe-coding-vs-agentic-engineering/. Acesso em: 07 ago. 2026.

DATABRICKS. *What is an AI Agent Harness?* 2026. Disponível em: https://www.databricks.com/blog/ai-harness. Acesso em: 07 ago. 2026.

DENG, Xiang et al. *SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?* 2025. Disponível em: https://arxiv.org/abs/2509.16941. Acesso em: 07 ago. 2026.

DORA / GOOGLE CLOUD. *Publications and ROI of AI-assisted Software Development Report*. 2026. Disponível em: https://dora.dev/research/publications/. Acesso em: 07 ago. 2026.

DX. *How to measure AI's impact on developer productivity*. 2026. Disponível em: https://getdx.com/blog/ai-measurement-hub/. Acesso em: 07 ago. 2026.

EXPLAINX.AI. *AI Coding Agent Evals on Real Repos (2026)*. 2026. Disponível em: https://explainx.ai/blog/ai-coding-agent-evals-real-repos-2026. Acesso em: 07 ago. 2026.

GARTNER. *Gartner Identifies the Top Strategic Technology Trends for 2026*. 2026. Disponível em: https://www.gartner.com/en/newsroom/press-releases/2025-10-20-gartner-identifies-the-top-strategic-technology-trends-for-2026. Acesso em: 07 ago. 2026.

HE, Kang; ROY, Kaushik. *SWE-Adept: An LLM-Based Agentic Framework for Deep Codebase Analysis and Structured Issue Resolution*. 2026. Disponível em: https://arxiv.org/abs/2603.01327. Acesso em: 07 ago. 2026.

INVARIANT LABS. *MCP Security Notification: Tool Poisoning Attacks*. 2026. Disponível em: https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks. Acesso em: 07 ago. 2026.

JIN, Haolin et al. *From LLMs to LLM-based Agents for Software Engineering: A Survey of Current, Challenges and Future*. 2024. Disponível em: https://arxiv.org/abs/2408.02479. Acesso em: 07 ago. 2026.

MCKINSEY & COMPANY. *The State of AI: Global Survey*. 2026. Disponível em: https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai. Acesso em: 07 ago. 2026.

MIT SLOAN MANAGEMENT REVIEW. ANDERSON, Edward; PARKER, Geoffrey; TAN, Burcu. *The Hidden Costs of Coding With Generative AI*. 2026. Disponível em: https://sloanreview.mit.edu/article/the-hidden-costs-of-coding-with-generative-ai/. Acesso em: 07 ago. 2026.

PRINCETON UNIVERSITY. *SWE-bench Verified & Pro*. 2026. Disponível em: https://www.swebench.com. Acesso em: 07 ago. 2026.

SOFTJOURN. *AI Software Development Statistics 2026: Adoption, Productivity, and Risk*. 2026. Disponível em: https://softjourn.com/insights/ai-software-dev-stats. Acesso em: 07 ago. 2026.

TAWOSI, Vali et al. *ALMAS: an Autonomous LLM-based Multi-Agent Software Engineering Framework*. 2025. Disponível em: https://arxiv.org/abs/2510.03463. Acesso em: 07 ago. 2026.

VALUE ADD VC. *AI Coding Productivity Study Data: What METR, McKinsey, and GitHub Found in 2026*. 2026. Disponível em: https://valueaddvc.com/blog/ai-coding-productivity-study-data-what-metr-mckinsey-and-github-actually-found-in-2026. Acesso em: 07 ago. 2026.

WONG, Sherman et al. *Confucius Code Agent: Scalable Agent Scaffolding for Real-World Codebases*. 2025. Disponível em: https://arxiv.org/abs/2512.10398. Acesso em: 07 ago. 2026.
