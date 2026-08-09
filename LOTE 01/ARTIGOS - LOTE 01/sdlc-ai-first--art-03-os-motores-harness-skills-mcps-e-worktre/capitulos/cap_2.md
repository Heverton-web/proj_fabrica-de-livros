# 2 Metodologia

Este artigo é um recorte analítico derivado do livro-mãe *SDLC AI-first*, especificamente dos capítulos 5 e 6, dedicados respectivamente ao ecossistema de execução (harness, skills, MCPs e worktrees) e à verificação adversarial (SOMMERVILLE, 2019; ROYCHOUDHURY, 2025). Seguindo o protocolo da esteira, não houve pesquisa primária: o embasamento foi reaproveitado do dossiê da obra-mãe.

O procedimento metodológico seguiu três etapas. Na primeira, identificou-se o recorte temático a partir dos pilares previstos no sumário macro: arquitetura harness-LLM-ferramentas, isolamento com worktrees, despacho paralelo de subagentes, e a camada de verificação em três níveis (máquina, adversarial e humano) (ANTHROPIC, 2025; GURGUL, 2024).

Na segunda etapa, realizou-se a consulta ao índice RAG do dossiê com os termos "harness", "agent-Computer interface", "MCP", "skills", "verificação adversarial" e "evidência antes de afirmação". Os blocos recuperados fundamentaram a síntese dos resultados, garantindo rastreabilidade de todas as afirmações (JIMENEZ, 2024; YANG, 2024).

Na terceira etapa, triangulou-se a literatura acadêmica com a documentação técnica dos provedores. A documentação do Model Context Protocol foi empregada para caracterizar a camada de ferramentas (CLARKE, 2025; ANTHROPIC, 2024). Os relatórios DORA foram usados como fonte sobre a relação entre automação, velocidade e estabilidade (GOOGLE CLOUD, 2025; FORSGREN, 2018).

A análise é qualitativa e interpretativa, com caráter de revisão crítica aplicada. Não foram executados experimentos controlados — coerente com a natureza do recorte, que consolida evidências publicadas (LEHMANN, 2024; MOHAGHEGHI, 2025). As limitações são discutidas na seção de resultados.

As citações seguem a NBR 10520 (autor-data) e as referências completas estão na seção final, conforme a NBR 6023 (HODA, 2025; WANG, 2024). O referencial combina fontes revisadas por pares e documentação técnica, permitindo contrastar pesquisa e indústria (HINGEL, 2026; GRÖPLER, 2024).

Por fim, registra-se o uso da metáfora dos motores — herdada do motivo condutor da obra-mãe — como categoria analítica. O harness é a sala de máquinas do SDLC AI-first, e o radar é a torre que vigia os voos (EVANS, 2003; MICROSOFT, 2025). A metáfora facilita a comunicação dos resultados para um público amplo de profissionais.

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
