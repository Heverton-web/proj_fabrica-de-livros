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

# 4 Conclusão

Este recorte confirmou que o harness e a verificação adversarial são as duas faces da execução agêntica segura. A literatura evidencia que a interface agente-computador determina a taxa de sucesso da execução (JIMENEZ, 2024; YANG, 2024), e que skills e MCPs reduzem a variabilidade do comportamento enquanto worktrees viabilizam o paralelismo (ANTHROPIC, 2025; CLARKE, 2025).

O estudo também demonstrou que a autonomia concedida na execução exige verificação proporcional na entrega: máquina verifica o automatizável, revisor adversário refuta o julgável e humano decide o merge, sempre sobre evidência verificável (ROYCHOUDHURY, 2025; LEHMANN, 2024). Sem essa camada, a delegação é risco acumulado (MOHAGHEGHI, 2025; GURGUL, 2024).

Para a prática, as recomendações são: investir na interface do harness antes de escalar agentes, empacotar conhecimento em skills com ciclo de vida definido, isolar trabalho com worktrees e calibrar o rigor da verificação pelo risco do artefato (JIN, 2024; MICROSOFT, 2025). Para a pesquisa, ficam em aberto a mensuração do retorno do harness e o estudo da obsolescência de skills (HODA, 2025; GRÖPLER, 2024). O próximo recorte da série examina como essa infraestrutura se comporta na entrega e operação reais (WANG, 2024; FORSGREN, 2018).

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