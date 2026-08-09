# 2 Metodologia

Este artigo é um recorte analítico derivado de um livro-mãe produzido na Fábrica Agêntica de Publicações, cujo tema é o ciclo de vida de desenvolvimento de software na era dos agentes. Seguindo o protocolo da esteira, o recorte não realizou pesquisa primária nova: todo o embasamento empírico e bibliográfico foi reaproveitado do dossiê de pesquisa do livro-mãe, composto por 9 artigos científicos indexados em arXiv, ICLR e ACM, além de 20 fontes institucionais (ANTHROPIC, 2025; MICROSOFT, 2025).

O procedimento metodológico adotou três etapas. Na primeira, identificou-se o recorte temático do artigo: os capítulos 1 e 2 da obra-mãe, respectivamente dedicados à transição do SDLC clássico ao AI-first e à definição da matriz de papéis entre humano, agente e verificação (SOMMERVILLE, 2019; HODA, 2025). A seleção foi guiada pelos pilares previstos no sumário macro do livro: a mudança de custo dominante de horas-homem para tokens e contexto, e o tripé spec-driven, verify-driven e feedback-driven (LEHMANN, 2024).

Na segunda etapa, realizou-se a consulta ao índice RAG do dossiê do livro-mãe. Para cada termo de busca derivado dos títulos dos capítulos-fonte — "agentic software engineering", "SDLC", "SWE-bench", "human role", "verification" — recuperaram-se os cinco blocos mais relevantes do índice, que alimentaram a síntese apresentada na seção de resultados (JIMENEZ et al., 2024; MOHAGHEGHI et al., 2025). Essa etapa garante rastreabilidade: toda afirmação deste artigo tem origem identificável no dossiê, nunca em informação inventada.

Na terceira etapa, os achados foram triangulados com a literatura técnica institucional e os benchmarks públicos. O SWE-bench foi utilizado como referência de avaliação de agentes de código, por ser o benchmark mais citado na literatura recente para medir a capacidade de resolução de problemas reais de GitHub (JIMENEZ, 2024). Os relatórios DORA foram empregados como fonte sobre o impacto da IA assistida no throughput e na estabilidade das equipes (GOOGLE CLOUD, 2025; FORSGREN, 2018).

A análise é qualitativa e interpretativa, com caráter de revisão crítica de literatura aplicada. Não foram coletados dados primários de campo nem executados experimentos controlados — coerente com a natureza do recorte, que visa consolidar e discutir evidências já publicadas sobre a transição para o SDLC AI-first (GURGUL, 2024; GRÖPLER, 2024). As limitações decorrentes dessa escolha são discutidas na seção de resultados.

As citações seguem a norma NBR 10520, com sistema autor-data, e as referências completas estão listadas na seção final, conforme a NBR 6023 (EVANS, 2003; ANTHROPIC, 2024). O referencial teórico combina fontes acadêmicas revisadas por pares com documentação técnica de provedores, o que permite contrastar a visão da pesquisa com a visão da indústria sobre o mesmo fenômeno (HINGEL, 2026; CLARKE, 2025).

Por fim, registra-se a decisão metodológica de utilizar a metáfora da torre de controle de tráfego aéreo como categoria analítica. Essa escolha, herdada do motivo condutor da obra-mãe, serve para estruturar a interpretação do novo papel humano no ciclo: o controlador de voo autoriza, monitora e arbitra, mas não pilota (HODA, 2025; ROYCHOUDHURY et al., 2025). O uso de uma metáfora como ferramenta analítica é deliberado e visa facilitar a comunicação dos resultados para um público amplo de profissionais de software.

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
