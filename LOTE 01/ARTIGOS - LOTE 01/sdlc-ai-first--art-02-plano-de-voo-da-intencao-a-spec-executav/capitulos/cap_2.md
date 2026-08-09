# 2 Metodologia

Este artigo é um recorte analítico derivado do livro-mãe *SDLC AI-first: O Ciclo de Vida do Software na Era dos Agentes*. Seguindo o protocolo da esteira de produção, o recorte não realizou pesquisa primária: todo o embasamento foi reaproveitado do dossiê da obra-mãe, composto por artigos científicos indexados em arXiv, ICLR e ACM, além de fontes institucionais de provedores (ANTHROPIC, 2025; MICROSOFT, 2025).

O procedimento metodológico seguiu três etapas. Na primeira, identificou-se o recorte temático: os capítulos 3 e 4 da obra-mãe, dedicados respectivamente à transformação de intenção em spec executável e à cartografia do domínio com design orientado a agentes (SOMMERVILLE, 2019; EVANS, 2003). Os pilares previstos no sumário macro — elicitação de intenção, critérios de aceite, deep modules, vocabulário ubíguo e ADRs — orientaram a busca de evidência.

Na segunda etapa, realizou-se consulta ao índice RAG do dossiê da obra-mãe. Para os termos "spec executável", "critério de aceite", "domain-driven design", "deep module" e "ADR", recuperaram-se os blocos mais relevantes do índice, que fundamentaram a síntese dos resultados (LEHMANN, 2024; HODA, 2025). Essa etapa garante rastreabilidade: nenhuma afirmação deste artigo provém de fonte fora do dossiê.

Na terceira etapa, triangulou-se a literatura acadêmica com a documentação técnica e os relatórios da indústria. O relatório DORA foi usado como fonte sobre o impacto de práticas de qualidade — como testes automatizados e revisão — no throughput e na estabilidade (GOOGLE CLOUD, 2025; FORSGREN, 2018). A documentação de provedores de IA foi empregada para caracterizar o estado da arte da execução agêntica e do protocolo de ferramentas (CLARKE, 2025; ANTHROPIC, 2024).

A análise é qualitativa e interpretativa, com caráter de revisão crítica aplicada. Não foram coletados dados primários nem executados experimentos controlados — coerente com a natureza do recorte, que consolida evidências publicadas (GURGUL, 2024; GRÖPLER, 2024). As limitações dessa escolha são discutidas na seção de resultados.

As citações seguem a norma NBR 10520 (sistema autor-data) e as referências completas estão listadas na seção final, conforme a NBR 6023 (JIMENEZ, 2024; WANG, 2024). O referencial combina fontes revisadas por pares com documentação técnica, permitindo contrastar a visão acadêmica e a visão da indústria (HINGEL, 2026; ROYCHOUDHURY, 2025).

Por fim, registra-se a decisão metodológica de utilizar a metáfora do plano de voo como categoria analítica, herdada do motivo condutor da obra-mãe. A especificação é o plano de voo aprovado antes da decolagem — sem ele, nenhuma fase inicia (MOHAGHEGHI, 2025; YANG, 2024). O uso da metáfora visa facilitar a comunicação dos resultados para profissionais de software em geral.

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
