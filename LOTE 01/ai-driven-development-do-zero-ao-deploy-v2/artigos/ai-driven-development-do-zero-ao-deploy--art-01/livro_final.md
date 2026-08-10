# 1 Introdução

## 1.1 Contextualização e Problema de Pesquisa

Entre 2024 e 2026 a engenharia de software atravessa uma mudança estrutural que a literatura técnica compara à adoção do DevOps e do Agile: modelos de linguagem de grande porte deixam de operar como autocomplete avançado — paradigma no qual o desenvolvedor permanece integralmente no loop, revisando cada sugestão em modo conversacional — para atuar como agentes autônomos capazes de planejar, executar, testar e iterar tarefas inteiras do ciclo de engenharia sob supervisão mínima (CONNELL, 2026; AUGMENT CODE, 2026). A distinção entre os dois paradigmas não é apenas de grau de autonomia, mas de arquitetura de controle: a codificação agêntica trata testes automatizados, linting, integração contínua e revisão de código como a superfície que torna a saída do agente auditável e confiável, ao passo que a codificação por vibe trata esses controles como opcionais, o que eleva o risco operacional e reduz a responsabilização em produção (AUGMENT CODE, 2026; CONNELL, 2026; BIRJOB, 2026).

Dados de mercado sustentam a relevância do problema: levantamentos indicam que a maioria das organizações de desenvolvimento já utiliza IA de forma ativa em algum ponto do ciclo de vida do software, e analistas posicionam a inteligência artificial agêntica entre as tendências tecnológicas estratégicas da década (GARTNER, 2026; SOFTJOURN, 2026; MCKINSEY, 2026). Esse movimento, no entanto, expõe uma lacuna conceitual: a difusão de ferramentas agênticas de codificação sem que a arquitetura interna que sustenta a autonomia desses sistemas seja amplamente compreendida por quem os adota. A diferença entre "ter um LLM" e "ter um agente de codificação" é tratada, na prática corporativa, como incidental, quando na verdade é estrutural (DATABRICKS, 2026; BUI, 2026; TAWOSI, 2025).

## 1.2 Objetivo do Recorte

O presente artigo tem como objetivo examinar, em perspectiva investigativa documental, dois temas centrais do livro-mãe *AI Driven Development: Do Zero ao Deploy*: (i) a definição precisa do que é — e do que não é — o desenvolvimento dirigido por IA, e (ii) o modelo arquitetural de quatro camadas — Tela, Harness, LLM e Tools — que a literatura técnica converge em descrever como o substrato dessa transição (BUI, 2026; DATABRICKS, 2026; JIN, 2024). Para isso, o recorte abrange também a preparação do ambiente de trabalho, o primeiro diálogo entre humano e agente, a engenharia de contexto e a autoria de arquivos de instrução como CLAUDE.md e AGENTS.md, entendidos como a instanciação prática das camadas (SOURCEGRAPH, 2026; TASKADE, 2026; TERMDOCK, 2026).

## 1.3 Justificativa e Delimitação

A justificativa decorre de duas observações. Primeiro, a adoção corporativa de ferramentas agênticas vem crescendo mais rápido do que a compreensão dos mecanismos que as tornam confiáveis, produzindo decisões de investimento baseadas em demonstrações superficiais de capacidade (CODIHAUS, 2026; VALUE ADD VC, 2026). Segundo, a literatura recente demonstra que a produtividade percebida não se traduz automaticamente em qualidade entregue: métricas de ciclos de desenvolvimento indicam ganhos de velocidade, mas relatórios setoriais alertam para custos ocultos de revisão e correção (DORA, 2026; MIT SLOAN MANAGEMENT REVIEW, 2026; DX, 2026). O recorte limita-se a fontes documentais públicas — relatórios de analistas, documentação oficial de plataformas e artigos de repositórios científicos — publicadas ou atualizadas entre 2024 e 2026, sem coleta primária de dados (UNBUILT LAB, 2026).

## 1.4 Síntese Parcial

Em síntese, o problema investigado situa-se na interseção entre três correntes: a corrente da produtividade (estudos de adoção e ROI), a corrente da arquitetura (harness, camadas e protocolos) e a corrente da governança (riscos de segurança e responsabilização) (INVARIANT LABS, 2026; CLOUD SECURITY ALLIANCE, 2026). A compreensão da arquitetura de quatro camadas é condição necessária para avaliar tanto o potencial quanto os riscos da adoção (HE, 2026; WONG, 2025). A seção seguinte descreve o procedimento metodológico adotado para recuperar e sintetizar as fontes que sustentam a análise das camadas (DENG, 2025; PRINCETON UNIVERSITY, 2026; EXPLAINX, 2026).

# Referências

AUGMENT CODE. *Vibe Coding vs Spec-Driven Development (2026): When to Use Each*. 2026. Disponível em: https://www.augmentcode.com/guides/vibe-coding-vs-spec-driven-development. Acesso em: 07 ago. 2026.

BIRJOB. *AI Coding Agent Benchmarks Beyond SWE-Bench in 2026: Terminal-Bench, Aider Polyglot, GAIA, and Why the Leaderboard Lies*. 2026. Disponível em: https://www.birjob.com/blog/agent-benchmarks-2026. Acesso em: 07 ago. 2026.

BUI, Nghi D. Q. *Building AI Coding Agents for the Terminal*. 2026. Disponível em: https://arxiv.org/html/2603.05344v1. Acesso em: 07 ago. 2026.

CLOUD SECURITY ALLIANCE. *Agentic MCP Security Best Practices Guide*. 2026. Disponível em: https://labs.cloudsecurityalliance.org/agentic/agentic-mcp-security-best-practices-v1/. Acesso em: 07 ago. 2026.

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

SOURCEGRAPH. *Context Engineering: A Practical Guide for AI Agents (2026)*. 2026. Disponível em: https://sourcegraph.com/blog/context-engineering. Acesso em: 07 ago. 2026.

TASKADE. *Context Engineering: What It Is + How to Do It (2026)*. 2026. Disponível em: https://www.taskade.com/blog/context-engineering. Acesso em: 07 ago. 2026.

TAWOSI, Vali et al. *ALMAS: an Autonomous LLM-based Multi-Agent Software Engineering Framework*. 2025. Disponível em: https://arxiv.org/abs/2510.03463. Acesso em: 07 ago. 2026.

TERMDOCK. *SKILL.md vs CLAUDE.md vs AGENTS.md Compared*. 2026. Disponível em: https://www.termdock.com/blog/skill-md-vs-claude-md-vs-agents-md. Acesso em: 07 ago. 2026.

UNBUILT LAB. *AI Development ROI Measurement: Complete Platform Guide*. 2026. Disponível em: https://unbuiltlab.com/blog/ai-development-roi-measurement-complete-platform-guide.html. Acesso em: 07 ago. 2026.

VALUE ADD VC. *AI Coding Productivity Study Data: What METR, McKinsey, and GitHub Found in 2026*. 2026. Disponível em: https://valueaddvc.com/blog/ai-coding-productivity-study-data-what-metr-mckinsey-and-github-actually-found-in-2026. Acesso em: 07 ago. 2026.

WONG, Sherman et al. *Confucius Code Agent: Scalable Agent Scaffolding for Real-World Codebases*. 2025. Disponível em: https://arxiv.org/abs/2512.10398. Acesso em: 07 ago. 2026.

# 2 Metodologia

## 2.1 Natureza do Recorte

O presente trabalho caracteriza-se como recorte investigativo documental, derivado do dossiê de pesquisa previamente construído e indexado para a obra-mãe *AI Driven Development: Do Zero ao Deploy* (UNBUILT LAB, 2026). Não há coleta primária de dados: a evidência empírica provém exclusivamente de fontes secundárias publicadas entre 2024 e 2026, entre as quais relatórios de analistas (GARTNER, 2026; MCKINSEY & COMPANY, 2026), relatórios de produtividade setorial (DORA / GOOGLE CLOUD, 2026; DX, 2026), documentação oficial de plataformas (DATABRICKS, 2026) e artigos revisados por pares ou depositados em repositórios científicos (JIN et al., 2024; DENG et al., 2025; TAWOSI et al., 2025; WONG et al., 2025).

## 2.2 Procedimento de Reaproveitamento do Dossiê

O dossiê-mãe foi organizado em blocos temáticos e indexado por recuperação vetorial local, permitindo busca por relevância (SOURCEGRAPH, 2026; TASKADE, 2026). Para cada tema deste recorte — definição de AIDD, arquitetura de quatro camadas, ambiente de trabalho, prompt de engenharia, contexto e arquivos de instrução — executou-se consulta por termos-chave ao índice, com retorno dos blocos mais relevantes e de suas fontes (BUI, 2026; AUGMENT CODE, 2026). As fontes retornadas foram então selecionadas segundo critérios de pertinência temática e autoridade editorial, e consolidadas na lista de referências ao final de cada seção (CLOUD SECURITY ALLIANCE, 2026).

## 2.3 Critério de Seleção das Fontes

Adotaram-se três critérios de inclusão: (i) pertinência direta a pelo menos um dos seis capítulos-fonte do livro-mãe (definição, camadas, ambiente, primeiro diálogo, contexto, manuais de instrução); (ii) publicações de entidades reconhecidas — analistas, universidades, plataformas e laboratórios de segurança — ou de autores com produção verificável na área (CONNELL, 2026; AUGMENT CODE, 2026); e (iii) atualidade, privilegiando materiais de 2025-2026, com tolerância para o survey seminal de JIN et al. (2024) (BIRJOB, 2026; PRINCETON UNIVERSITY, 2026). Excluíram-se fontes sem data identificável, conteúdo promocional sem dados e materiais que apenas replicam relatórios primários .

## 2.4 Construção Textual e Citação

A redação seguiu o framework ACAD (Contextualização, Referencial Teórico, Análise, Síntese Parcial), com tom acadêmico impessoal em terceira pessoa e citação autor-data conforme a NBR 10520 (HE, 2026; EXPLAINX.AI, 2026). Toda afirmação factual, dado estatístico ou atribuição conceitual recebe citação explícita no corpo, e cada referência listada ao final da seção corresponde a uma fonte efetivamente consultada (INVARIANT LABS, 2026). A rastreabilidade citacao-referência foi verificada de forma determinística antes da consolidação final, reduzindo o risco de atribuição indevida (CODIHAUS, 2026; MIT SLOAN MANAGEMENT REVIEW, 2026).

# Referências

AUGMENT CODE. *Vibe Coding vs Spec-Driven Development (2026): When to Use Each*. 2026. Disponível em: https://www.augmentcode.com/guides/vibe-coding-vs-spec-driven-development. Acesso em: 07 ago. 2026.

BIRJOB. *AI Coding Agent Benchmarks Beyond SWE-Bench in 2026: Terminal-Bench, Aider Polyglot, GAIA, and Why the Leaderboard Lies*. 2026. Disponível em: https://www.birjob.com/blog/agent-benchmarks-2026. Acesso em: 07 ago. 2026.

BUI, Nghi D. Q. *Building AI Coding Agents for the Terminal*. 2026. Disponível em: https://arxiv.org/html/2603.05344v1. Acesso em: 07 ago. 2026.

CLOUD SECURITY ALLIANCE. *Agentic MCP Security Best Practices Guide*. 2026. Disponível em: https://labs.cloudsecurityalliance.org/agentic/agentic-mcp-security-best-practices-v1/. Acesso em: 07 ago. 2026.

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

SOURCEGRAPH. *Context Engineering: A Practical Guide for AI Agents (2026)*. 2026. Disponível em: https://sourcegraph.com/blog/context-engineering. Acesso em: 07 ago. 2026.

TASKADE. *Context Engineering: What It Is + How to Do It (2026)*. 2026. Disponível em: https://www.taskade.com/blog/context-engineering. Acesso em: 07 ago. 2026.

TAWOSI, Vali et al. *ALMAS: an Autonomous LLM-based Multi-Agent Software Engineering Framework*. 2025. Disponível em: https://arxiv.org/abs/2510.03463. Acesso em: 07 ago. 2026.

TERMDOCK. *SKILL.md vs CLAUDE.md vs AGENTS.md Compared*. 2026. Disponível em: https://www.termdock.com/blog/skill-md-vs-claude-md-vs-agents-md. Acesso em: 07 ago. 2026.

UNBUILT LAB. *AI Development ROI Measurement: Complete Platform Guide*. 2026. Disponível em: https://unbuiltlab.com/blog/ai-development-roi-measurement-complete-platform-guide.html. Acesso em: 07 ago. 2026.

VALUE ADD VC. *AI Coding Productivity Study Data: What METR, McKinsey, and GitHub Found in 2026*. 2026. Disponível em: https://valueaddvc.com/blog/ai-coding-productivity-study-data-what-metr-mckinsey-and-github-actually-found-in-2026. Acesso em: 07 ago. 2026.

WONG, Sherman et al. *Confucius Code Agent: Scalable Agent Scaffolding for Real-World Codebases*. 2025. Disponível em: https://arxiv.org/abs/2512.10398. Acesso em: 07 ago. 2026.

# 3 Resultados e Discussão

## 3.1 AIDD: Definição, Fronteiras e Evidência de Adoção

Os resultados da análise documental confirmam que AI Driven Development (AIDD) designa uma modalidade de engenharia de software em que agentes de IA participam ativamente de múltiplas etapas do ciclo de vida — especificação, planejamento, implementação, teste e revisão — operando a partir de intenções expressas em linguagem natural e de restrições explícitas codificadas no projeto (BUI, 2026; CONNELL, 2026). A literatura distingue o AIDD do *vibe coding* por uma diferença estrutural: no primeiro, a saída do agente passa por camadas de verificação determinística e governança; no segundo, a saída é aceita pela aparência de plausibilidade (AUGMENT CODE, 2026; BIRJOB, 2026). Essa distinção aparece também nos dados de adoção: relatórios setoriais apontam crescimento do uso de agentes em equipes de engenharia, com ênfase na correlação entre maturidade de prática e qualidade percebida (GARTNER, 2026; SOFTJOURN, 2026; MCKINSEY & COMPANY, 2026).

## 3.2 A Arquitetura de Quatro Camadas: Tela, Harness, LLM e Tools

O segundo resultado diz respeito à arquitetura. A análise converge na descrição de quatro camadas interconectadas: a camada de Tela (interface entre humano e sistema), a camada de Harness (orquestração, permissões e gerenciamento de contexto), a camada de LLM (raciocínio) e a camada de Tools (efeito real no mundo) (DATABRICKS, 2026; BUI, 2026). O Harness emerge como o componente crítico: é ele que transforma um modelo de linguagem em um agente operacional, aplicando permissões, gerenciando o contexto e registrando trilhas de auditoria (JIN et al., 2024; HE, 2026; WONG et al., 2025). A camada de Tools, por sua vez, é o ponto de contato com sistemas externos, conectada crescentemente por protocolos abertos como o Model Context Protocol (AUGMENT CODE, 2026; CLOUD SECURITY ALLIANCE, 2026).

## 3.3 Risco e Governança na Camada de Tools

O terceiro resultado é o mapeamento de riscos. A revisão documental identificou ameaças concretas na camada de ferramentas, destacando-se o envenenamento de ferramentas (*tool poisoning*) — descrições de ferramentas maliciosas ou enganosas capazes de induzir o agente a ações indevidas (INVARIANT LABS, 2026; CLOUD SECURITY ALLIANCE, 2026). Esses riscos reforçam a tese de que a confiabilidade do AIDD depende menos da capacidade bruta do modelo e mais da robustez do harness que o envolve — permissões determinísticas, aprovações explícitas e revisão humana em pontos de alto impacto (DATABRICKS, 2026). A produtividade, medida em velocidade de entrega, não deve ser confundida com redução de custo total: estudos apontam ganhos de 2x em tarefas isoladas, mas também custos ocultos de revisão, correção e dívida técnica quando a verificação é negligenciada (CODIHAUS, 2026; MIT SLOAN MANAGEMENT REVIEW, 2026; VALUE ADD VC, 2026; DORA / GOOGLE CLOUD, 2026).

## 3.4 Síntese Parcial

Em síntese, os resultados articulam três achados: (i) o AIDD é um paradigma distinto do *vibe coding*, caracterizado por verificações externas ao modelo; (ii) a arquitetura de quatro camadas tem no Harness o seu núcleo de confiabilidade; e (iii) a camada de Tools concentra os principais riscos de segurança, mitigáveis por governança determinística (EXPLAINX.AI, 2026; TAWOSI et al., 2025). A seção seguinte conclui o recorte retomando o argumento central e suas implicações para a adoção corporativa (PRINCETON UNIVERSITY, 2026; DENG et al., 2025).

# Referências

AUGMENT CODE. *Vibe Coding vs Spec-Driven Development (2026): When to Use Each*. 2026. Disponível em: https://www.augmentcode.com/guides/vibe-coding-vs-spec-driven-development. Acesso em: 07 ago. 2026.

BIRJOB. *AI Coding Agent Benchmarks Beyond SWE-Bench in 2026: Terminal-Bench, Aider Polyglot, GAIA, and Why the Leaderboard Lies*. 2026. Disponível em: https://www.birjob.com/blog/agent-benchmarks-2026. Acesso em: 07 ago. 2026.

BUI, Nghi D. Q. *Building AI Coding Agents for the Terminal*. 2026. Disponível em: https://arxiv.org/html/2603.05344v1. Acesso em: 07 ago. 2026.

CLOUD SECURITY ALLIANCE. *Agentic MCP Security Best Practices Guide*. 2026. Disponível em: https://labs.cloudsecurityalliance.org/agentic/agentic-mcp-security-best-practices-v1/. Acesso em: 07 ago. 2026.

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

SOURCEGRAPH. *Context Engineering: A Practical Guide for AI Agents (2026)*. 2026. Disponível em: https://sourcegraph.com/blog/context-engineering. Acesso em: 07 ago. 2026.

TASKADE. *Context Engineering: What It Is + How to Do It (2026)*. 2026. Disponível em: https://www.taskade.com/blog/context-engineering. Acesso em: 07 ago. 2026.

TAWOSI, Vali et al. *ALMAS: an Autonomous LLM-based Multi-Agent Software Engineering Framework*. 2025. Disponível em: https://arxiv.org/abs/2510.03463. Acesso em: 07 ago. 2026.

TERMDOCK. *SKILL.md vs CLAUDE.md vs AGENTS.md Compared*. 2026. Disponível em: https://www.termdock.com/blog/skill-md-vs-claude-md-vs-agents-md. Acesso em: 07 ago. 2026.

UNBUILT LAB. *AI Development ROI Measurement: Complete Platform Guide*. 2026. Disponível em: https://unbuiltlab.com/blog/ai-development-roi-measurement-complete-platform-guide.html. Acesso em: 07 ago. 2026.

VALUE ADD VC. *AI Coding Productivity Study Data: What METR, McKinsey, and GitHub Found in 2026*. 2026. Disponível em: https://valueaddvc.com/blog/ai-coding-productivity-study-data-what-metr-mckinsey-and-github-actually-found-in-2026. Acesso em: 07 ago. 2026.

WONG, Sherman et al. *Confucius Code Agent: Scalable Agent Scaffolding for Real-World Codebases*. 2025. Disponível em: https://arxiv.org/abs/2512.10398. Acesso em: 07 ago. 2026.

# 4 Conclusão

## 4.1 Retomada do Argumento Central

O recorte investigativo permitiu sustentar a tese central do livro-mãe em três proposições. Primeira: AI Driven Development é um paradigma de engenharia distinto do *vibe coding*, definido não pela presença de um modelo de linguagem, mas pela existência de camadas de verificação e governança externas ao modelo (AUGMENT CODE, 2026; CONNELL, 2026). Segunda: a arquitetura de quatro camadas — Tela, Harness, LLM e Tools — tem no Harness o seu núcleo de confiabilidade, pois é nessa camada que permissões, contexto e trilhas de auditoria são aplicados de forma determinística (DATABRICKS, 2026; BUI, 2026; JIN et al., 2024). Terceira: a camada de Tools, ponto de contato com o mundo externo, concentra os riscos mais severos, como o envenenamento de ferramentas, cuja mitigação depende de governança, não de capacidade de raciocínio do modelo (INVARIANT LABS, 2026; CLOUD SECURITY ALLIANCE, 2026).

## 4.2 Implicações para a Adoção

As implicações práticas decorrem diretamente dos achados. Organizações que adotam ferramentas agênticas de codificação devem avaliar a robustez do harness que envolve o modelo — permissões explícitas, aprovações em pontos de alto impacto, revisão determinística — antes de considerar a capacidade de raciocínio como critério isolado de escolha (HE, 2026; WONG et al., 2025). Da mesma forma, a medição de produtividade deve separar velocidade de tarefa de custo total: ganhos de 2x em tarefas isoladas convivem com custos ocultos de revisão e dívida técnica (CODIHAUS, 2026; MIT SLOAN MANAGEMENT REVIEW, 2026; DORA / GOOGLE CLOUD, 2026). A engenharia de contexto e a autoria deliberada de arquivos de instrução, como CLAUDE.md e AGENTS.md, aparecem como práticas de baixo custo e alto retorno, pois condicionam o agente antes da primeira linha de código (SOURCEGRAPH, 2026; TASKADE, 2026; TERMDOCK, 2026; AUGMENT CODE, 2026).

## 4.3 Limitações e Trabalhos Futuros

O recorte limita-se a fontes documentais públicas; não foram coletados dados primários de adoção em organizações específicas (UNBUILT LAB, 2026; DX, 2026). Estudos futuros podem investigar, com evidência primária, a relação entre maturidade de governança do harness e taxas de incidentes em produção, bem como a evolução dos benchmarks de avaliação de agentes (BIRJOB, 2026; PRINCETON UNIVERSITY, 2026; DENG et al., 2025; EXPLAINX.AI, 2026). A expansão do recorte para os temas de testes dirigidos por IA, revisão autônoma e CI/CD com agentes constitui desdobramento natural da agenda de pesquisa (TAWOSI et al., 2025; GARTNER, 2026; MCKINSEY & COMPANY, 2026).

# Referências

AUGMENT CODE. *Vibe Coding vs Spec-Driven Development (2026): When to Use Each*. 2026. Disponível em: https://www.augmentcode.com/guides/vibe-coding-vs-spec-driven-development. Acesso em: 07 ago. 2026.

BIRJOB. *AI Coding Agent Benchmarks Beyond SWE-Bench in 2026: Terminal-Bench, Aider Polyglot, GAIA, and Why the Leaderboard Lies*. 2026. Disponível em: https://www.birjob.com/blog/agent-benchmarks-2026. Acesso em: 07 ago. 2026.

BUI, Nghi D. Q. *Building AI Coding Agents for the Terminal*. 2026. Disponível em: https://arxiv.org/html/2603.05344v1. Acesso em: 07 ago. 2026.

CLOUD SECURITY ALLIANCE. *Agentic MCP Security Best Practices Guide*. 2026. Disponível em: https://labs.cloudsecurityalliance.org/agentic/agentic-mcp-security-best-practices-v1/. Acesso em: 07 ago. 2026.

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

SOURCEGRAPH. *Context Engineering: A Practical Guide for AI Agents (2026)*. 2026. Disponível em: https://sourcegraph.com/blog/context-engineering. Acesso em: 07 ago. 2026.

TASKADE. *Context Engineering: What It Is + How to Do It (2026)*. 2026. Disponível em: https://www.taskade.com/blog/context-engineering. Acesso em: 07 ago. 2026.

TAWOSI, Vali et al. *ALMAS: an Autonomous LLM-based Multi-Agent Software Engineering Framework*. 2025. Disponível em: https://arxiv.org/abs/2510.03463. Acesso em: 07 ago. 2026.

TERMDOCK. *SKILL.md vs CLAUDE.md vs AGENTS.md Compared*. 2026. Disponível em: https://www.termdock.com/blog/skill-md-vs-claude-md-vs-agents-md. Acesso em: 07 ago. 2026.

UNBUILT LAB. *AI Development ROI Measurement: Complete Platform Guide*. 2026. Disponível em: https://unbuiltlab.com/blog/ai-development-roi-measurement-complete-platform-guide.html. Acesso em: 07 ago. 2026.

VALUE ADD VC. *AI Coding Productivity Study Data: What METR, McKinsey, and GitHub Found in 2026*. 2026. Disponível em: https://valueaddvc.com/blog/ai-coding-productivity-study-data-what-metr-mckinsey-and-github-actually-found-in-2026. Acesso em: 07 ago. 2026.

WONG, Sherman et al. *Confucius Code Agent: Scalable Agent Scaffolding for Real-World Codebases*. 2025. Disponível em: https://arxiv.org/abs/2512.10398. Acesso em: 07 ago. 2026.
