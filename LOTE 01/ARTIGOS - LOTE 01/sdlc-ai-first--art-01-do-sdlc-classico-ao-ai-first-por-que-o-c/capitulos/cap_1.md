# 1 Introdução

O ciclo de vida de desenvolvimento de software (SDLC) foi desenhado em uma época em que o custo dominante da produção era a hora-homem. Os modelos Waterfall e Ágil, apesar de suas diferenças estruturais, compartilham essa premissa: o processo existe para coordenar pessoas, e a qualidade depende de disciplina humana aplicada a documentos, reuniões e revisões manuais (SOMMERVILLE, 2019). Esse contrato implícito governou a indústria por décadas, e continua sendo o referencial sobre o qual a maioria das equipes organiza fluxos, ferramentas e métricas (FORSGREN, 2018).

Nos últimos anos, porém, o surgimento de modelos de linguagem de grande escala (LLMs) capazes de gerar, revisar e executar código alterou a economia dessa equação. O que antes era trabalho exclusivamente humano passou a ser executável por agentes de software com custo marginal próximo de zero (JIN, 2024). A literatura recente registra a transição de três estágios: o autocomplete assistivo, a geração de código orientada por prompt e, finalmente, os agentes autônomos que operam dentro de um harness, com acesso a ferramentas, testes e ciclo de feedback (JIMENEZ et al., 2024; YANG et al., 2024).

Este estágio final é o que a literatura denomina *agentic software engineering*: sistemas que não apenas sugerem código, mas planejam, executam comandos, verificam resultados e iteram até satisfazer um critério de aceite (MOHAGHEGHI et al., 2025; ROYCHOUDHURY et al., 2025). A mudança não é incremental — ela altera a própria natureza do SDLC, porque o artefato-mestre deixa de ser o documento e passa a ser a especificação executável acompanhada de testes (LEHMANN, 2024). O problema de pesquisa deste artigo é precisamente este: como o contrato do ciclo de vida muda quando a execução é delegável a agentes, e qual o novo papel reservado ao humano nesse arranjo (HODA, 2025).

A hipótese central é que o SDLC AI-first não elimina o humano, mas reposiciona sua função de produtor para controlador. O humano passa a autorizar decolagens de fase, arbitrar desvios e verificar evidências — função análoga à de um controlador de tráfego aéreo que não pilota a aeronave, mas decide quando ela decola, por qual rota segue e quando pode aterrissar (GRÖPLER et al., 2024; HINGEL, 2026). Essa metáfora, adotada como motivo condutor da obra-mãe, organiza a análise dos próximos capítulos.

O objetivo deste recorte é duplo. Primeiro, caracterizar a transição estrutural do SDLC clássico para o AI-first, evidenciando em que pontos o contrato tradicional se rompe (GURGUL, 2024). Segundo, descrever a matriz de papéis emergente — humano orquestra, agente executa, verificação refuta — e discutir as implicações para responsabilidade e governança em cada fase do ciclo (MICROSOFT, 2025; ANTHROPIC, 2025).

A justificativa do estudo é prática e urgente. Organizações que adotam ferramentas de IA sem redesenhar o processo reproduzem, em escala, os defeitos do fluxo manual — ou pior, criam novos defeitos decorrentes da ausência de verificação (GOOGLE CLOUD, 2025). Compreender o novo contrato é pré-condição para capturar o valor dos agentes sem transferir para eles o risco que o processo deveria conter (ANTHROPIC, 2024; CLARKE, 2025).

O artigo está organizado em quatro seções. A segunda descreve a metodologia de construção do recorte a partir do dossiê da obra-mãe. A terceira apresenta os resultados e a discussão, sintetizando as evidências sobre a mudança de custo dominante e o novo papel humano. A quarta conclui com as implicações para a prática e para a pesquisa futura.

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
