# 3 Resultados e Discussão

A síntese das fontes do dossiê sustenta que a entrega moderna é uma disciplina de contingência. Em primeiro lugar, os relatórios DORA evidenciam que as equipes de alta performance combinam deploy frequente com estabilidade — o que, na prática, exige releases reproduzíveis e gates automatizados (GOOGLE CLOUD, 2025; FORSGREN, 2018). O release que depende de passos manuais não declarados não é um artefato, é um acidente em potencial.

Em segundo lugar, o recorte revela a centralidade do deploy gradual. O canário com gate de saúde — expor uma fração do tráfego, medir sinais vitais e só então expandir — é a técnica mais citada para reduzir o raio de explosão de um release defeituoso (GURGUL, 2024; GRÖPLER, 2024). O rollback, por sua vez, deixa de ser plano de emergência e vira procedimento treinado em staging antes da decolagem (MICROSOFT, 2025).

Em terceiro lugar, o contexto agêntico introduz uma novidade: a necessidade de observar o comportamento do próprio agente em produção. Os resultados indicam que métricas, logs e a "caixa-preta" das decisões agênticas são pré-condição para operar sem cegueira (CLARKE, 2025; ANTHROPIC, 2025). Sem observabilidade do agente, o operador não sabe se o comportamento em produção é o mesmo que foi verificado em staging (MOHAGHEGHI, 2025).

A discussão organiza-se em três eixos. O primeiro é o debriefing como insumo, não burocracia. A literatura converge para a recomendação de que o post-mortem deve produzir ação verificável — uma skill nova, uma spec revisada, um teste adicionado — e não apenas um documento arquivado (HODA, 2025; ROYCHOUDHURY, 2025). A diferença entre memória e aprendizado é a verificação de que a lição virou mudança (JIN, 2024).

O segundo eixo é a captura de conhecimento. O dossiê documenta que erros recorrentes viram memória organizacional: procedimentos empacotados que impedem a repetição do mesmo defeito (ANTHROPIC, 2025; CLARKE, 2025). A skill é o artefato que materializa a lição aprendida, transformando experiência individual em capacidade da equipe (LEHMANN, 2024).

O terceiro eixo é a revisão de specs por evidência. Os resultados sugerem que o SDLC aprende a cada iteração: quando a spec não previa um caso de borda que estourou em produção, a lição é incorporada à própria spec (MICROSOFT, 2025; HODA, 2025). Esse é o mecanismo que impede a repetição do mesmo incidente (GRÖPLER, 2024).

A síntese permite identificar tensões não resolvidas. A primeira é a cultura: debriefing sem cultura de não-culpabilização produz relatos incompletos (HODA, 2025). A segunda é a propagação: lições que não chegam a outros times são conhecimento desperdiçado (GURGUL, 2024). A terceira é o custo da observabilidade, que compete com o custo de contexto do próprio ciclo (MOHAGHEGHI, 2025).

Como limitação, registra-se que o recorte se apoia em fontes de 2018-2026, com predomínio recente, e que a ausência de dados primários impede afirmações causais sobre o impacto do debriefing (JIN, 2024; LEHMANN, 2024).

No conjunto, os resultados sustentam que autorização de pouso e debriefing são as duas metades do mesmo ciclo: a entrega monitorada gera os dados que o aprendizado consome, e o aprendizado melhora a próxima entrega (ANTHROPIC, 2024; FORSGREN, 2018). O voo não termina na aterrissagem — termina no relatório do piloto (YANG, 2024; WANG, 2024).

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
