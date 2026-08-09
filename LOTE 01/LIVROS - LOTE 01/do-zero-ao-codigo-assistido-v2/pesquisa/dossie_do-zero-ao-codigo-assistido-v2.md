# Dossiê de Pesquisa — Do Zero ao Código Assistido: programando com agentes de IA

## Conceitos-chave
- **LLM (Large Language Model)**: modelo de linguagem de grande escala baseado na arquitetura Transformer, pré-treinado em grandes corpora de texto e código; base de todos os assistentes de código atuais. Fonte: Vaswani et al. (2017); Springer Applied Intelligence (2026).
- **Transformer**: arquitetura neural baseada em mecanismos de atenção (self-attention) que permite processamento paralelo de sequências; introduzida em 2017 e base de todos os LLMs modernos. Fonte: arXiv:1706.03762.
- **Agente de código (coding agent)**: sistema que combina um LLM com ferramentas (terminal, editor, execução de testes, navegação de arquivos) em um loop planejar-agir-observar para executar tarefas de engenharia de software de ponta a ponta. Fonte: Liu et al. (ACM TOSEM, 2024); arXiv:2508.00083.
- **Harness (arnês)**: infraestrutura que conecta o LLM ao ambiente real de desenvolvimento — permissões, sandbox, contexto do repositório, loop de execução — determinante para o desempenho de agentes de longa duração. Fonte: Anthropic (2025); code.claude.com.
- **MCP (Model Context Protocol)**: protocolo aberto que padroniza a conexão de modelos de linguagem a fontes de dados e ferramentas externas (arquivos, bancos, APIs), evitando integrações ponto a ponto. Fonte: modelcontextprotocol.io.
- **Prompt engineering**: disciplina de formular instruções e contexto para obter saídas previsíveis e corretas de LLMs; técnicas: few-shot, chain-of-thought, divisão de tarefas. Fonte: guia oficial de prompt engineering (OpenAI).
- **Benchmark de engenharia de software (SWE-bench)**: conjunto de issues reais de repositórios populares do GitHub usado para avaliar a capacidade de agentes de resolver problemas completos de engenharia de software. Fonte: swebench.com.
- **Modelos de raciocínio (reasoning models)**: LLMs treinados com aprendizado por reforço para emitir cadeias de raciocínio longas antes de responder, como DeepSeek-R1; melhoram tarefas de lógica e código. Fonte: arXiv:2501.12948 (DeepSeek-R1).
- **CI de código / revisão agêntica**: uso de ferramentas determinísticas (linters, type-checkers, testes) acopladas ao loop do agente para validar o código gerado, reduzindo alucinações e regressões. Fonte: survey Springer (2026); awesome-cli-coding-agents.
- **Custo e provedores gratuitos**: camadas free de APIs (OpenRouter, Groq) e execução local (Ollama) permitem começar a usar agentes de código sem investimento inicial. Fonte: OpenRouter; Ollama.

## Artigos Científicos e Papers
- VASWANI, Ashish et al. *Attention is all you need*. In: Advances in Neural Information Processing Systems (NeurIPS), 2017. Disponível em: https://arxiv.org/abs/1706.03762. Acesso em: 06 ago. 2026.
- LIU, Jiachen et al. *Large language model-based agents for software engineering: a survey*. In: ACM Transactions on Software Engineering and Methodology, 2024. Disponível em: https://dl.acm.org/doi/abs/10.1145/3796507. Acesso em: 06 ago. 2026.
- JOEL, Sathvik; WU, Jie; FARD, Fatemeh. *A survey on LLM-based code generation for low-resource and domain-specific programming languages*. In: ACM Transactions on Software Engineering and Methodology, 2025. Disponível em: https://dl.acm.org/doi/abs/10.1145/3770084. Acesso em: 06 ago. 2026.
- ANÔNIMOS. *A survey on code generation with LLM-based agents*. In: arXiv:2508.00083, 2025. Disponível em: https://arxiv.org/abs/2508.00083. Acesso em: 06 ago. 2026.
- *Code generation with large language models: a survey from neural program synthesis to autonomous software development*. In: Applied Intelligence, v. 56, art. 200, Springer, 2026. Disponível em: https://link.springer.com/article/10.1007/s10489-026-07230-0. Acesso em: 06 ago. 2026.
- RAMÍREZ-RUEDA, Rolando et al. *Transforming software development: a study on the integration of multi-agent systems and large language models for automatic code generation*. In: 12th International Conference on Software Engineering Research and Innovation (CONISOFT), IEEE, 2024. Disponível em: https://ieeexplore.ieee.org/document/10795597. Acesso em: 06 ago. 2026.
- *Software development using transformer-based LLMs*. In: IEEE Xplore, 2025. Disponível em: https://ieeexplore.ieee.org/document/11452207. Acesso em: 06 ago. 2026.
- PENG, Sida et al. *The impact of AI on developer productivity: evidence from GitHub Copilot*. In: arXiv:2302.06590, 2023. Disponível em: https://arxiv.org/abs/2302.06590. Acesso em: 06 ago. 2026.
- GONÇALVES, Carlos Adriano. *Assessment on the effectiveness of GitHub Copilot as a code assistance tool: an empirical study*. In: Progress in Artificial Intelligence — 23rd EPIA Conference, Springer, 2024. Disponível em: https://link.springer.com/chapter/10.1007/978-3-031-73503-5_3. Acesso em: 06 ago. 2026.
- DEEPSEEK-AI. *DeepSeek-R1: incentivizing reasoning capability in LLMs via reinforcement learning*. In: arXiv:2501.12948, 2025. Disponível em: https://arxiv.org/abs/2501.12948. Acesso em: 06 ago. 2026.
- *GitHub Copilot and developer productivity: an observational dose-response analysis*. In: arXiv:2606.00438, 2026. Disponível em: https://arxiv.org/abs/2606.00438. Acesso em: 06 ago. 2026.

## Estado da arte / ferramentas de referência
- **Claude Code**: agente de codificação que atua diretamente no terminal, com permissões granulares, modo plano, hooks e integração MCP. Fonte: https://code.claude.com/docs/en/how-claude-code-works.
- **OpenCode**: CLI agêntica open source com skills, subagentes e suporte multi-provedor. Fonte: https://github.com/opencode-ai/opencode (awesome-cli-coding-agents).
- **awesome-cli-coding-agents**: catálogo curado de CLIs agênticas de codificação (Claude Code, Codex CLI, Cursor CLI, Antigravity, OpenCode e outros). Fonte: https://github.com/opencode-ai/awesome-cli-coding-agents.
- **Cursor e Antigravity**: IDEs/assistentes com IA integrada; comparados por ergonomia, contexto e custo para iniciantes. Fonte: artigos de comparação técnica (2026).
- **GitHub Copilot**: assistente de pair programming mais difundido; estudos empíricos indicam ganho médio de 55,8% de velocidade em tarefas padronizadas. Fonte: arXiv:2302.06590; GitHub Blog (2022).
- **Model Context Protocol (MCP)**: padrão aberto da Anthropic para conexão de modelos a ferramentas e dados; adotado por Claude Code, Cursor, OpenCode e outros. Fonte: https://modelcontextprotocol.io.
- **Provedores gratuitos**: OpenRouter (agregador com modelos free), Groq (inferência acelerada por LPU), Ollama (modelos locais em CPU/GPU). Fonte: openrouter.ai; ollama.com.
- **SWE-bench Verified & Pro**: benchmarks de referência para avaliar agentes de engenharia de software em issues reais. Fonte: https://www.swebench.com.
- **Harnesses para agentes de longa duração**: pesquisa da Anthropic sobre design de ambiente (memória, tool use, guardrails) para agentes que rodam por horas. Fonte: Anthropic (2025-11-26).

## Casos de uso corporativos
- **Automação de PRs com agentes**: empresas relatam agentes de código resolvendo issues e abrindo pull requests com revisão humana, com padrões de falha e rejeição mapeados ("Coding Agents in the Wild"). Fonte: IEEE Access (2026) — via citações do ACM survey.
- **Engenharia assistida por IA no GitHub**: estudo de dose-resposta observacional indica efeito de eficiência consistente entre engenheiros que usam Copilot. Fonte: arXiv:2606.00438.
- **Pesquisa do NAV (Noruega)**: estudo de campo com desenvolvedores do setor público mostrou percepção de produtividade sem correlação com commits — o valor percebido é fluxo e redução de esforço tedioso. Fonte: arXiv:2509.20353.
- **Adoção global de IA em código**: classificador neural em 30 milhões de commits do GitHub rastreou difusão de código gerado por IA entre desenvolvedores. Fonte: Science (2026) — via Semantic Scholar.
- **Fábrica agêntica de publicações**: o próprio repositório desta obra (proj_fabrica-de-livros) é um caso de orquestração multi-agente com skills, subagentes e MCPs para produção editorial. Fonte: AGENTS.md do projeto.

## Limitações e controvérsias
- **Segurança de código gerado**: LLMs geram código vulnerável em taxas preocupantes; estudos empíricos mostram que Copilot não é pior que humanos, mas a revisão humana continua obrigatória. Fonte: Empirical Software Engineering (2023); Perry et al. (CCS 2023) — via Springer.
- **Lacuna benchmark vs. mundo real**: benchmarks isolam tarefas de nível de função; não há evidência conclusiva de que os resultados se estendem a workflows reais de repositório e manutenção de longo prazo. Fonte: Springer Applied Intelligence (2026).
- **Confiança cega em sugestões**: desenvolvedores tendem a aceitar sugestões da IA com menos escrutínio do que em pair programming humano ("From Developer Pairs to AI Copilots"). Fonte: arXiv (2025) — via Semantic Scholar.
- **Produtividade percebida ≠ métricas objetivas**: estudos observacionais não encontraram mudanças significativas em atividade de commits após adoção de Copilot, apesar da percepção de ganho. Fonte: arXiv:2509.20353.
- **Contaminação de benchmarks**: avaliações podem estar contaminadas se os dados de teste fizeram parte do treino; há pesquisas dedicadas a quantificar isso em geração de código. Fonte: ACL 2024 — via Springer survey.
- **Custo e contexto**: agentes de longa duração consomem muito contexto e tokens; design de harness e limitação de escopo são decisões críticas de economia. Fonte: Anthropic (2025).

## Fontes brutas (para Nó 7 — Auditor de Rastreabilidade)
- VASWANI, Ashish et al. *Attention is all you need*. Disponível em: https://arxiv.org/abs/1706.03762. Acesso em: 06 ago. 2026.
- ANTHROPIC. *Effective harnesses for long-running agents*. Disponível em: https://www.anthropic.com/research/effective-harnesses-for-long-running-agents. Acesso em: 06 ago. 2026.
- ANTHROPIC. *How Claude Code works*. Disponível em: https://code.claude.com/docs/en/how-claude-code-works. Acesso em: 06 ago. 2026.
- MODEL CONTEXT PROTOCOL. *Documentação oficial*. Disponível em: https://modelcontextprotocol.io. Acesso em: 06 ago. 2026.
- PRINCETON UNIVERSITY. *SWE-bench Verified & Pro*. Disponível em: https://www.swebench.com. Acesso em: 06 ago. 2026.
- OPENCODE. *awesome-cli-coding-agents*. Disponível em: https://github.com/opencode-ai/awesome-cli-coding-agents. Acesso em: 06 ago. 2026.
- OPENROUTER. *Modelos gratuitos e provedores*. Disponível em: https://openrouter.ai. Acesso em: 06 ago. 2026.
- OLLAMA. *Execução local de LLMs*. Disponível em: https://ollama.com. Acesso em: 06 ago. 2026.
- OPENAI. *Prompt engineering guide*. Disponível em: https://platform.openai.com/docs/guides/prompt-engineering. Acesso em: 06 ago. 2026.
- SCIELO. *Blog e preprints em português sobre IA generativa*. Disponível em: https://blog.scielo.org. Acesso em: 06 ago. 2026.
- GITHUB BLOG. *Research: quantifying GitHub Copilot's impact on developer productivity and happiness*. Disponível em: https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-on-developer-productivity-and-happiness/. Acesso em: 06 ago. 2026.
- LIU, Jiachen et al. *Large language model-based agents for software engineering: a survey*. Disponível em: https://dl.acm.org/doi/abs/10.1145/3796507. Acesso em: 06 ago. 2026.
- JOEL, Sathvik; WU, Jie; FARD, Fatemeh. *A survey on LLM-based code generation for low-resource and domain-specific programming languages*. Disponível em: https://dl.acm.org/doi/abs/10.1145/3770084. Acesso em: 06 ago. 2026.
- *A survey on code generation with LLM-based agents*. Disponível em: https://arxiv.org/abs/2508.00083. Acesso em: 06 ago. 2026.
- *Code generation with large language models: a survey from neural program synthesis to autonomous software development*. Disponível em: https://link.springer.com/article/10.1007/s10489-026-07230-0. Acesso em: 06 ago. 2026.
- RAMÍREZ-RUEDA, Rolando et al. *Transforming software development: a study on the integration of multi-agent systems and large language models for automatic code generation*. Disponível em: https://ieeexplore.ieee.org/document/10795597. Acesso em: 06 ago. 2026.
- *Software development using transformer-based LLMs*. Disponível em: https://ieeexplore.ieee.org/document/11452207. Acesso em: 06 ago. 2026.
- PENG, Sida et al. *The impact of AI on developer productivity: evidence from GitHub Copilot*. Disponível em: https://arxiv.org/abs/2302.06590. Acesso em: 06 ago. 2026.
- GONÇALVES, Carlos Adriano. *Assessment on the effectiveness of GitHub Copilot as a code assistance tool: an empirical study*. Disponível em: https://link.springer.com/chapter/10.1007/978-3-031-73503-5_3. Acesso em: 06 ago. 2026.
- DEEPSEEK-AI. *DeepSeek-R1: incentivizing reasoning capability in LLMs via reinforcement learning*. Disponível em: https://arxiv.org/abs/2501.12948. Acesso em: 06 ago. 2026.
- *GitHub Copilot and developer productivity: an observational dose-response analysis*. Disponível em: https://arxiv.org/abs/2606.00438. Acesso em: 06 ago. 2026.
- *Developer productivity with and without GitHub Copilot: a field study* (NAV). Disponível em: https://arxiv.org/abs/2509.20353. Acesso em: 06 ago. 2026.
