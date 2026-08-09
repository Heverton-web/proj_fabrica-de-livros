# 1 Introdução

A execução agêntica não acontece no vácuo: ela depende de uma camada de infraestrutura que conecta o modelo de linguagem às ferramentas, às regras e ao isolamento necessário para o trabalho paralelo (ANTHROPIC, 2025; CLARKE, 2025). Essa camada — o harness — é o tema central deste recorte. Sem ela, o agente é apenas um modelo conversando; com ela, o agente vira um operário capaz de editar arquivos, rodar testes e iterar até satisfazer o critério de aceite (MOHAGHEGHI, 2025).

O problema de pesquisa deste artigo é duplo. Primeiro: como arquitetar o harness — a orquestração entre modelo, ferramentas (MCPs), procedimentos empacotados (skills) e isolamento de trabalho (worktrees)? Segundo: como garantir que a execução produzida nesse ecossistema seja verificável, por meio de uma camada adversarial que refuta em vez de confirmar (ROYCHOUDHURY, 2025; YANG, 2024)?

A literatura recente evidencia que a qualidade da infraestrutura determina a qualidade da execução. Estudos sobre agentes de código mostram que a interface entre o agente e o computador — o que o agente pode ver e tocar — é tão importante quanto o modelo subjacente (JIMENEZ, 2024; YANG, 2024). O SWE-agent demonstrou que uma interface bem projetada multiplica a taxa de sucesso em tarefas reais, evidenciando que o harness não é detalhe de implementação, mas variável de resultado (MOHAGHEGHI, 2025).

A hipótese orientadora é que a execução agêntica e a verificação adversarial formam um par indissociável: quanto mais autonomia se concede ao agente, mais rigorosa deve ser a camada que refuta o seu trabalho (GURGUL, 2024; HODA, 2025). Delegar execução sem construir verificação não é produtividade — é acúmulo de risco (JIN, 2024; LEHMANN, 2024).

Este artigo está organizado em quatro seções. A metodologia descreve a construção do recorte a partir do dossiê. Os resultados e a discussão sintetizam as evidências sobre harness, skills, MCPs, worktrees e verificação adversarial em três níveis. A conclusão apresenta as implicações para equipes que desejam operar motores agênticos com segurança (MICROSOFT, 2025; GRÖPLER, 2024).

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
