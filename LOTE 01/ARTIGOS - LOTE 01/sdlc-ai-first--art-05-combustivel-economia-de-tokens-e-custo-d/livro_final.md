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

# 2 Metodologia

Este artigo é um recorte analítico derivado do livro-mãe *SDLC AI-first*, especificamente dos capítulos 9 e 10, dedicados à economia de tokens e ao futuro do ciclo com maturidade e governança (SOMMERVILLE, 2019; HODA, 2025). Seguindo o protocolo da esteira, não houve pesquisa primária: o embasamento foi reaproveitado do dossiê da obra-mãe.

O procedimento metodológico seguiu três etapas. Na primeira, identificou-se o recorte temático a partir dos pilares do sumário macro: tokens e rate limits, LeanCTX e compressão de logs, handoffs e sessões longas, níveis de maturidade L1-L5 e anti-padrões (LEHMANN, 2024; MOHAGHEGHI, 2025).

Na segunda etapa, consultou-se o índice RAG do dossiê com os termos "token", "context", "rate limit", "handoff", "maturidade" e "anti-padrões". Os blocos recuperados fundamentaram a síntese, garantindo rastreabilidade das afirmações (JIN, 2024; ROYCHOUDHURY, 2025).

Na terceira etapa, triangulou-se a literatura acadêmica com os relatórios DORA (GOOGLE CLOUD, 2025; FORSGREN, 2018) e a documentação técnica sobre otimização de contexto e protocolo de ferramentas (CLARKE, 2025; ANTHROPIC, 2024).

A análise é qualitativa e interpretativa, com caráter de revisão crítica aplicada. Não foram executados experimentos controlados — coerente com a natureza do recorte (GURGUL, 2024; GRÖPLER, 2024). As limitações são discutidas na seção de resultados.

As citações seguem a NBR 10520 (autor-data) e as referências completas estão na seção final, conforme a NBR 6023 (MICROSOFT, 2025; WANG, 2024). O referencial combina pesquisa revisada por pares e documentação técnica (HINGEL, 2026; YANG, 2024).

Por fim, registra-se o uso da metáfora do combustível — herdada do motivo condutor da obra-mãe — como categoria analítica. O token é o combustível de cada voo do SDLC AI-first, e o comandante que não controla o consumo não chega ao destino (EVANS, 2003; ANTHROPIC, 2025). A metáfora estrutura a interpretação dos resultados sobre sustentabilidade do ciclo.

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

# 4 Conclusão

Este recorte confirmou que a economia de tokens e a governança de maturidade são as duas condições de escala do SDLC AI-first. A literatura evidencia que o custo de contexto é o novo gargalo da engenharia assistida por IA, e que a disciplina de lean context — injetar apenas o necessário — decide a viabilidade financeira do ciclo (JIN, 2024; LEHMANN, 2024).

O estudo também demonstrou que a maturidade se mede pela capacidade de delegar com segurança em escala: do copiloto ao ciclo adversarial autônomo, cada nível exige mais verificação e mais disciplina de contexto (HODA, 2025; ROYCHOUDHURY, 2025). Os anti-padrões — prompt-and-pray, specs decorativas, verificação pelo próprio agente — são os pontos de falha mais documentados (MOHAGHEGHI, 2025; GURGUL, 2024).

Para a prática, as recomendações são: orçar contexto por fase como recurso finito, institucionalizar a compressão de logs e o handoff como cidadãos de primeira classe, e diagnosticar a maturidade com instrumento explícito antes de escalar delegação (MICROSOFT, 2025; CLARKE, 2025). Para a pesquisa, ficam em aberto a mensuração do retorno do lean context e o estudo longitudinal dos efeitos da delegação sobre competências (FORSGREN, 2018; GRÖPLER, 2024). O recorte encerra a série, devolvendo ao leitor a imagem do Comandante de Operações de Software (WANG, 2024; YANG, 2024).

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