# 1 Introdução

Todo SDLC tem um recurso dominante. No ciclo clássico, era a hora-homem; no SDLC AI-first, é o token — a unidade de contexto que os agentes consomem em cada fase (JIN, 2024; LEHMANN, 2024). A economia de tokens deixou de ser detalhe operacional e se tornou variável de projeto: é ela que decide se a automação compensa, se as sessões sobrevivem e se o ciclo inteiro é financeiramente viável (MOHAGHEGHI, 2025; GRÖPLER, 2024).

O problema de pesquisa deste recorte é duplo. Primeiro: como governar o consumo de contexto — rate limits, compressão de logs, subagentes enxutos e handoffs bem projetados — para manter o ciclo economicamente sustentável? Segundo: como posicionar o SDLC AI-first no futuro — níveis de maturidade, anti-padrões e os riscos de dívida técnica e erosão de competências (HODA, 2025; ROYCHOUDHURY, 2025)?

A literatura evidencia que o custo de contexto é o novo gargalo da engenharia assistida por IA. Estudos e relatórios da indústria apontam que a produtividade do agente depende tanto da qualidade do prompt quanto do desenho do fluxo de contexto: quanto menos tokens desperdiçados, mais trabalho útil por sessão (MICROSOFT, 2025; GURGUL, 2024). A disciplina de lean context — injetar apenas o necessário — é a resposta prática a esse gargalo (CLARKE, 2025; ANTHROPIC, 2025).

A hipótese orientadora é que a maturidade do SDLC AI-first se mede pela capacidade de delegar com segurança em escala: do copiloto individual ao ciclo adversarial autônomo, cada nível exige mais infraestrutura de verificação e mais disciplina de contexto (YANG, 2024; JIMENEZ, 2024). A organização que ignora o custo de contexto não escala — ela quebra (FORSGREN, 2018; SOMMERVILLE, 2019).

Este artigo está organizado em quatro seções. A metodologia descreve o recorte construído a partir do dossiê. Os resultados e a discussão sintetizam as evidências sobre economia de tokens, níveis de maturidade e anti-padrões. A conclusão apresenta o roadmap do profissional que lidera o ciclo (HINGEL, 2026; ANTHROPIC, 2024).

# Referências

ANTHROPIC. Building effective agents. 2025. Disponível em: https://www.anthropic.com/research/building-effective-agents. Acesso em: 02 ago. 2026.

ANTHROPIC. Introducing the Model Context Protocol. 2024b. Disponível em: https://www.anthropic.com/news/model-context-protocol. Acesso em: 02 ago. 2026.

WANG, Yuchen; GUO, Shangxin; TAN, Chee Wei. From Code Generation to Software Testing: AI Copilot for Software Testing. 2024. Disponível em: https://arxiv.org/abs/2406.06574. Acesso em: 02 ago. 2026.

CLARKE, Peter et al. Model Context Protocol: overview e adoção. 2025. Disponível em: https://modelcontextprotocol.io. Acesso em: 02 ago. 2026.

EVANS, Eric. Domain-Driven Design: Tackling Complexity in the Heart of Software. Boston: Addison-Wesley, 2003.

FORSGREN, Nicole; HUMBLE, Jez; KIM, Gene. Accelerate: The Science of Lean Software and DevOps. Portland: IT Revolution Press, 2018.

GOOGLE CLOUD. State of AI-assisted Software Development (DORA 2025). Disponível em: https://dora.dev. Acesso em: 02 ago. 2026.

GRÖPLER, Robin et al. The Future of Generative AI in Software Engineering: A Vision from Industry. 2024. Disponível em: https://arxiv.org/abs/2411.17941. Acesso em: 02 ago. 2026.

GURGUL, Vincent; GUBELA, Robin; LESSMANN, Stefan. The State of Generative AI in Software Development. 2024. Disponível em: https://arxiv.org/abs/2410.18485. Acesso em: 02 ago. 2026.

HINGEL, Paula. How AI Changes the SDLC: A Six-Stage Guide. Augment Code, 2026. Disponível em: https://www.augmentcode.com. Acesso em: 02 ago. 2026.

HODA, Rashina. Toward Agentic Software Engineering Beyond Code: Framing Vision, Values, and Vocabulary. 2025. Disponível em: https://arxiv.org/abs/2505.10262. Acesso em: 02 ago. 2026.

JIMENEZ, Carlos E. et al. SWE-bench: Can Language Models Resolve Real-World GitHub Issues? ICLR, 2024. Disponível em: https://arxiv.org/abs/2310.06770. Acesso em: 02 ago. 2026.

JIN, Haolin et al. From LLMs to LLM-based Agents for Software Engineering: A Survey of Current, Challenges and Future. 2024. Disponível em: https://arxiv.org/abs/2408.02479. Acesso em: 02 ago. 2026.

LEHMANN, Fabian et al. Software Engineering in the Era of LLMs. 2024. Disponível em: https://arxiv.org/abs/2412.05229. Acesso em: 02 ago. 2026.

MICROSOFT. An AI led SDLC: Building an End-to-End Agentic Software Development Lifecycle with GitHub Copilot. 2025. Disponível em: https://learn.microsoft.com. Acesso em: 02 ago. 2026.

MOHAGHEGHI, Milad et al. Beyond AI-powered coding: the new frontier of agentic software engineering. 2025. Disponível em: https://arxiv.org/abs/2503.21353. Acesso em: 02 ago. 2026.

QODO. AI-assisted code review. 2025. Disponível em: https://www.qodo.ai. Acesso em: 02 ago. 2026.

ROYCHOUDHURY, Abhik et al. Agentic Software Engineering: state and perspectives. 2025. Disponível em: https://arxiv.org/abs/2505.02778. Acesso em: 02 ago. 2026.

SOMMERVILLE, Ian. Engenharia de Software. 10. ed. São Paulo: Pearson, 2019.

YANG, John et al. SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering. 2024. Disponível em: https://arxiv.org/abs/2405.15793. Acesso em: 02 ago. 2026.
