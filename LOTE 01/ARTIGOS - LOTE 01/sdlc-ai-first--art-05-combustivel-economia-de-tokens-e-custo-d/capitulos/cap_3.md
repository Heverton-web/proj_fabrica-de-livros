# 3 Resultados e Discussão

A síntese das fontes do dossiê sustenta que o token é o recurso dominante do SDLC AI-first. Em primeiro lugar, a literatura sobre LLMs e agentes evidencia que o custo de contexto cresce com a complexidade do ciclo, e que o desperdício — logs inteiros no contexto, buscas redundantes, releituras — corrói a viabilidade da automação (JIN, 2024; LEHMANN, 2024). O relatório do ciclo de vida precisa do número: quanto custa cada fase em tokens, e onde o desperdício se concentra (MOHAGHEGHI, 2025).

Em segundo lugar, o recorte revela as técnicas que materializam a disciplina. A compressão de logs — manter o essencial, descartar o ruído — reduz o custo de leitura sem perder a evidência (CLARKE, 2025; ANTHROPIC, 2025). A seleção cirúrgica de contexto — grep antes de read, injetar só o necessário — evita que a sessão encha com conteúdo irrelevante (GURGUL, 2024). O handoff bem projetado, por sua vez, estende a vida útil da sessão ao transferir estado de forma compacta (MICROSOFT, 2025).

Em terceiro lugar, o recorte documenta o papel dos rate limits como variável de projeto. Os resultados indicam que o buffer de rate limit não é obstáculo, mas design: a organização que planeja o consumo em picos consegue operar com motores gratuitos ou baratos sem parar o ciclo (HINGEL, 2026; ANTHROPIC, 2024). A resiliência de custo é pré-condição da escala.

A discussão organiza-se em três eixos. O primeiro é a maturidade em níveis. A literatura sugere uma escala que vai do copiloto individual ao ciclo adversarial autônomo, passando pela delegação supervisionada e pela spec-driven (HODA, 2025; ROYCHOUDHURY, 2025). Cada nível tem requisitos próprios de verificação, governança e economia de contexto (YANG, 2024; JIMENEZ, 2024).

O segundo eixo são os anti-padrões. O dossiê documenta três falhas recorrentes: prompt-and-pray (gerar sem verificar), specs decorativas (documentos que não viram critérios) e verificação pelo próprio agente (quem escreve valida sozinho) (MOHAGHEGHI, 2025; GURGUL, 2024). A detecção automática desses padrões é o primeiro passo para eliminá-los (CLARKE, 2025).

O terceiro eixo é o risco da adoção. Os resultados indicam que a dívida técnica do código gerado por IA — não testado, não documentado — e a erosão de competências humanas são as ameaças mais citadas (LEHMANN, 2024; FORSGREN, 2018). A governança mínima — humanos arbitrando, evidência obrigatória, reversibilidade — é a resposta (ROYCHOUDHURY, 2025).

A síntese permite identificar tensões não resolvidas. A primeira é o equilíbrio entre economia e rigor: cortar contexto demais pode cortar evidência junto (MOHAGHEGHI, 2025). A segunda é a medição da produtividade agêntica, ainda sem consenso (FORSGREN, 2018). A terceira é a governança da próxima década, com responsabilidade legal e ética das decisões delegadas (HODA, 2025).

Como limitação, registra-se que o recorte se apoia em fontes recentes (2018-2026), o que pode superestimar a velocidade da evolução. A ausência de dados primários impede afirmações causais (JIN, 2024; GRÖPLER, 2024).

No conjunto, os resultados sustentam que o futuro do SDLC pertence a quem combina disciplina de contexto com governança de delegação (ANTHROPIC, 2025; SOMMERVILLE, 2019). O comandante que mede o combustível e audita as rotas decola com segurança; o que improvisa, fica no chão (WANG, 2024; EVANS, 2003).

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
