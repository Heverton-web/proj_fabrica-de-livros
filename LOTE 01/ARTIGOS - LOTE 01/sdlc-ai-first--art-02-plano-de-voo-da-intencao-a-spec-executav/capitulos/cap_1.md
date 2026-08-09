# 1 Introdução

A transição para o desenvolvimento de software orientado a agentes reposiciona o artefato central do processo. No ciclo clássico, o documento de requisitos era um registro de intenções que dependia da interpretação humana para se tornar software (SOMMERVILLE, 2019). No ciclo AI-first, esse artefato assume uma função nova e mais severa: ele é, ao mesmo tempo, contrato com a máquina que executa, critério de aceite para a verificação e registro do entendimento compartilhado do time (LEHMANN, 2024). A especificação deixa de ser descrição e passa a ser execução potencial.

Esse reposicionamento tem uma consequência imediata: a qualidade da especificação torna-se o fator dominante da qualidade do produto. Requisitos vagos, que no fluxo tradicional eram absorvidos pela inteligência do desenvolvedor, tornam-se bloqueadores quando não há intérprete humano no caminho (JIN, 2024). A literatura recente converge para o conceito de *spec executável* — uma especificação cujos critérios de aceite são verificáveis por máquina e cujos casos de borda são explícitos (MICROSOFT, 2025; HINGEL, 2026).

O problema de pesquisa deste recorte é duplo. Primeiro: como transformar intenção vaga em especificação executável, com requisitos numerados, critérios de aceite mensuráveis e casos de borda explícitos? Segundo: como modelar o domínio — vocabulário ubíguo, fronteiras entre módulos e decisões de arquitetura — de modo que a execução agêntica não produza retrabalho (EVANS, 2003; HODA, 2025).

A hipótese orientadora é que a disciplina de especificação e design, historicamente tratada como etapa preliminar burocrática, torna-se o coração do SDLC AI-first: quanto melhor o contrato, menos ciclos de correção e menos custo de contexto desperdiçado (GRÖPLER, 2024; GURGUL, 2024). O design orientado a fronteiras — módulos profundos, interfaces estáveis e decisões registradas — é a pré-condição estrutural para que agentes paralelos trabalhem sem colidir (MOHAGHEGHI, 2025).

Este artigo está organizado em quatro seções. A metodologia descreve como o recorte foi construído a partir do dossiê da obra-mãe. Os resultados e a discussão sintetizam as evidências sobre spec executável, vocabulário ubíguo e registros de decisão de arquitetura (ADR). A conclusão apresenta as implicações práticas para equipes em transição (ANTHROPIC, 2025; ROYCHOUDHURY, 2025).

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
