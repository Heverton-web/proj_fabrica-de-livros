# 3 Resultados e Discussão

A síntese das fontes do dossiê sustenta que o harness é a variável de resultado da execução agêntica. Em primeiro lugar, a literatura sobre agentes de código mostra que a interface agente-computador — o que o agente enxerga e manipula — determina a taxa de sucesso em tarefas reais (JIMENEZ, 2024; YANG, 2024). O SWE-agent demonstrou que um harness bem projetado, com feedback de testes e edição direta de arquivos, multiplica a capacidade de resolução de problemas do GitHub (MOHAGHEGHI, 2025; YANG, 2024).

Em segundo lugar, o recorte revela a importância das camadas de conhecimento e ferramentas. As skills — procedimentos empacotados com quando usar e como executar — reduzem a variabilidade do comportamento do agente e materializam o aprendizado organizacional (ANTHROPIC, 2025; HODA, 2025). Os MCPs, por sua vez, padronizam o acesso a ferramentas externas, eliminando a necessidade de integrações ad hoc por agente (CLARKE, 2025; ANTHROPIC, 2024).

Em terceiro lugar, o isolamento com worktrees emerge como condição do trabalho paralelo. Os resultados indicam que agentes operando em worktrees independentes evitam colisões e permitem despacho paralelo de subagentes, com merge controlado (ROYCHOUDHURY, 2025; GURGUL, 2024). Sem isolamento, o paralelismo é uma ilusão: os agentes competem pelos mesmos arquivos e o resultado é corrompido antes da verificação.

A discussão dos resultados organiza-se em três eixos. O primeiro é a verificação adversarial em três níveis. A literatura converge para a recomendação de que a máquina verifica o que é automatizável (typecheck, lint, testes), o revisor adversarial refuta o que é julgável e o humano decide o merge (LEHMANN, 2024; ROYCHOUDHURY, 2025). Cada nível tem limiar e evidência próprios.

O segundo eixo é a evidência antes de afirmação. O dossiê documenta que a qualidade da verificação depende da qualidade da evidência: output de comando real, log de execução e hash de artefato substituem a promessa verbal do agente (JIN, 2024; MICROSOFT, 2025). A evidência verificável é o que distingue a revisão do teatro.

O terceiro eixo é a calibragem do rigor. Os resultados sugerem que a intensidade da verificação deve ser proporcional ao risco do artefato: módulos de pagamento exigem refutação pesada, enquanto utilitários internos admitem verificação leve (GRÖPLER, 2024; MOHAGHEGHI, 2025). O rigor uniforme desperdiça contexto; o rigor zero acumula dívida.

A síntese permite identificar tensões não resolvidas. A primeira é o custo do harness: construir e manter a infraestrutura exige investimento que nem toda equipe justifica (LEHMANN, 2024). A segunda é a obsolescência das skills: procedimentos empacotados envelhecem e precisam de manutenção (HODA, 2025). A terceira é a confiança excessiva no agente que a própria ferramenta induz (GURGUL, 2024; GRÖPLER, 2024).

Como limitação, registra-se que o recorte se apoia em fontes de 2024-2026, o que pode superestimar a maturidade das ferramentas. A ausência de dados primários impede afirmações causais sobre o impacto do harness (JIN, 2024; MOHAGHEGHI, 2025).

No conjunto, os resultados sustentam que motores e radar formam um par indissociável: a autonomia concedida na execução deve ser compensada por verificação adversarial na entrega (ANTHROPIC, 2025; FORSGREN, 2018). O harness é a sala de máquinas; a verificação é a torre que autoriza o pouso — e nenhuma decola sem o outro (WANG, 2024; SOMMERVILLE, 2019).

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
