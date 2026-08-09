# 1 Introdução

O ponto em que o software encontra o usuário — o release — sempre foi o momento de maior risco do ciclo de vida (SOMMERVILLE, 2019). No SDLC AI-first, esse momento ganha contornos novos: o artefato entregue é produzido com participação de agentes, e a operação passa a incluir a observabilidade do próprio comportamento agêntico (ROYCHOUDHURY, 2025; MOHAGHEGHI, 2025). Autorizar o pouso — aprovar a entrega — exige mais do que confiança no processo; exige evidência de que o voo inteiro foi monitorado (FORSGREN, 2018).

O problema de pesquisa deste recorte é duplo. Primeiro: como entregar com segurança em um ciclo onde agentes participam da produção — build reproduzível, deploy gradual e canário, e fallbacks de ambiente? Segundo: como transformar os erros de produção em insumo de melhoria, fechando o ciclo de aprendizado que evolui o próprio SDLC (HODA, 2025; GRÖPLER, 2024)?

A literatura evidencia que a entrega moderna é uma disciplina de contingência: release reproduzível, deploy canário com gate de saúde e rollback treinado reduzem o risco de forma mensurável (GOOGLE CLOUD, 2025; GURGUL, 2024). No contexto agêntico, soma-se a necessidade de observar o agente em produção — métricas, logs e a caixa-preta do seu comportamento — para que a operação não seja cega (CLARKE, 2025; ANTHROPIC, 2025).

A hipótese orientadora é que release e aprendizado formam um ciclo contínuo: a entrega gera incidentes, os incidentes geram lições, as lições viram mudanças de processo e a mudança melhora a próxima entrega (JIN, 2024; LEHMANN, 2024). A organização que fecha esse loop transforma o erro em vantagem competitiva; a que não fecha, repete os mesmos defeitos em escala crescente (MICROSOFT, 2025; YANG, 2024).

Este artigo está organizado em quatro seções. A metodologia descreve o recorte construído a partir do dossiê. Os resultados e a discussão sintetizam as evidências sobre release reproduzível, observabilidade do agente e o loop de debriefing. A conclusão apresenta implicações práticas (HINGEL, 2026; ANTHROPIC, 2024).

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
