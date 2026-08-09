# 3 Resultados e Discussão

A síntese das fontes do dossiê confirma a tese da transição estrutural. Em primeiro lugar, a literatura é convergente ao apontar que o custo dominante do desenvolvimento mudou: do esforço humano medido em horas-homem para o consumo de tokens e contexto medido em unidades computacionais (JIN et al., 2024; LEHMANN et al., 2024). Essa mudança tem consequência profunda: a escassez deixou de ser a capacidade de escrever e passou a ser a capacidade de especificar, orquestrar e verificar (GRÖPLER, 2024).

Em segundo lugar, os benchmarks mostram uma trajetória clara de capacitação dos agentes. O SWE-bench documentou, entre 2023 e 2025, a evolução de modelos que resolviam menos de 2% dos problemas reais do GitHub para modelos que ultrapassam 70% no conjunto Verified (JIMENEZ, 2024; ANTHROPIC, 2024). A progressão não é linear nem uniforme, mas a direção é inequívoca: a capacidade de executar tarefas de engenharia real, com edição de múltiplos arquivos e execução de testes, tornou-se factível (YANG, 2024).

Em terceiro lugar, o recorte revela que a mera adoção de ferramentas de IA sem redesenho do processo produz resultados ambíguos. Os relatórios DORA apontam que equipes que incorporam IA assistida sem alterar o fluxo de trabalho observam ganhos em velocidade de entrega, mas não necessariamente em estabilidade — a menos que a verificação automatizada acompanhe a geração (GOOGLE CLOUD, 2025; FORSGREN, 2018). Esse dado sustenta a hipótese central do artigo: o problema não é a máquina, é o contrato.

A discussão desses resultados organiza-se em torno de três eixos. O primeiro eixo é a redistribuição de papéis. A literatura sobre agentes de software converge para um desenho em que o humano não desaparece, mas muda de posição: de executor para orquestrador e árbitro (HODA, 2025; ROYCHOUDHURY et al., 2025). Essa redistribuição não é trivial — ela exige novas competências de especificação, leitura de evidência e decisão sob incerteza, competências distintas daquelas que formaram a geração anterior de engenheiros (MOHAGHEGHI, 2025).

O segundo eixo é a centralidade da especificação executável. Quando o agente executa, o artefato que sobra é a spec: ela é, simultaneamente, contrato com a máquina, contrato com o time e critério de aceite (MICROSOFT, 2025; HINGEL, 2026). Artigos do dossiê convergem para a recomendação de que requisitos vagos — que antes eram absorvidos pela interpretação humana — tornam-se bloqueadores na era dos agentes, pois não há intérprete humano no meio do caminho (LEHMANN et al., 2024; EVANS, 2003).

O terceiro eixo é a governança da verificação. A evidência da literatura é de que a verificação não pode ser delegada ao próprio agente que produziu o artefato: quem escreve não valida sozinho (QODO, 2025; ANTHROPIC, 2024). O desenho recomendado — e adotado pela obra-mãe — é o de uma camada adversarial de verificação, com máquina, revisor e humano exercendo papéis complementares (CLARKE, 2025; GURGUL, 2024).

A síntese dos resultados permite ainda identificar tensões não resolvidas na literatura. A primeira é a mensuração: não há consenso sobre como medir produtividade em ambiente agêntico, e métricas herdadas do SDLC clássico podem mascarar regressões de qualidade (FORSGREN, 2018). A segunda é a erosão de competências: delegar demais pode atrofiar a capacidade de avaliação crítica dos engenheiros (HODA, 2025; GRÖPLER, 2024). A terceira é a responsabilidade legal e ética das decisões delegadas, tema ainda incipiente na literatura (ROYCHOUDHURY, 2025).

Como limitação do estudo, registra-se que o recorte se apoia majoritariamente em fontes publicadas entre 2024 e 2026, o que pode superestimar a velocidade da transição. Além disso, a ausência de dados primários impede afirmações causais sobre o impacto organizacional da adoção. Essas limitações apontam para a necessidade de estudos longitudinais que acompanhem equipes reais em transição (JIN et al., 2024; MOHAGHEGHI et al., 2025).

No conjunto, os resultados sustentam que o SDLC AI-first não é uma versão automatizada do ciclo clássico, mas um novo arranjo contratual em que o humano opera a torre de controle: autoriza decolagens, monitora o radar e arbitra desvios, enquanto os agentes pilotam as fases de execução (HINGEL, 2026; MICROSOFT, 2025). Essa constatação tem implicações diretas para a formação profissional e para o desenho de processos, exploradas na conclusão.

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
