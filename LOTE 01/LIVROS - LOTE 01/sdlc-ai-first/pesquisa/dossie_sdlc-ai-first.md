# Dossiê Técnico — SDLC AI-first (Software Development Life Cycle orientado a Agentes)

## Conceitos-chave e definições

- **SDLC (Software Development Life Cycle):** modelo estruturado que organiza o ciclo de vida do software em fases (requisitos, design, implementação, testes, implantação, manutenção). O paradigma tradicional otimiza fases manuais executadas por humanos.
- **SDLC AI-first:** reestruturação do ciclo em que o artefato-mestre deixa de ser o documento/backlog e passa a ser a spec executável + testes; o humano deixa de ser o executor e vira orquestrador + árbitro de qualidade; a verificação deixa de ser fase final e se torna adversarial e contínua.
- **Agentic Software Engineering (ASE):** evolução dos assistentes lineares de código (autocomplete) para agentes autônomos que planejam, executam edições multi-arquivo, escrevem testes, depuram e resolvem issues GitHub de ponta a ponta (Roychoudhury et al., 2025; Forrester, 2026).
- **Agent scaffolding:** loop de execução iterativo em que o LLM usa ferramentas persistentes (bash, editores, harness de teste) para tentar, falhar, autocorrigir e verificar código ao longo de dezenas ou centenas de turnos — a base da diferença entre prompt engineering e desenvolvimento agêntico (Anthropic, 2024).
- **Model Context Protocol (MCP):** padrão aberto lançado pela Anthropic (novembro de 2024) que conecta fontes de dados (GitHub, Postgres, Slack) a ferramentas de IA por um protocolo universal, resolvendo o problema do "silo de contexto".
- **SWE-bench:** benchmark padrão-ouro para avaliar agentes de código em issues reais do GitHub (Django, SymPy, scikit-learn), com verificação por testes de unidade reais (Jimenez et al., ICLR 2024).
- **Verificação adversarial:** prática em que quem escreve não valida sozinho — um revisor (agente ou humano) tenta refutar o trabalho; a evidência precede a afirmação de conclusão.
- **Economia de tokens:** disciplina de custo de contexto que define a viabilidade operacional do SDLC AI-first (rate limits, vida útil de sessão, compressão de logs).
- **DORA e IA:** métricas de entrega (throughput vs. estabilidade) sob adoção de IA — correlação positiva com frequência de deploy e lead time, e risco de aumento de change failure rate sem governança (Google Cloud DORA, 2025).

## Estado da arte

1. A literatura converge: o impacto da GenAI varia ao longo das fases do SDLC, com maior destaque em design, implementação e testes (Gurgul et al., 2026).
2. A transição de LLMs estáticos para agentes baseados em LLM cobre 6 pilares: requisitos, geração de código, decisão autônoma, design, testes e manutenção (Jin et al., 2025).
3. Pesquisadores defendem a expansão do agêntico para o "whole of process" — requisitos, arquitetura, desenvolvimento e operações — com alinhamento ético (Hoda, ICSE 2026).
4. Em 2024, Anthropic demonstrou que acoplar um modelo forte a scaffolding mínimo (bash + edição de string) atingiu estado da arte no SWE-bench Verified (49%), provando que a arquitetura do agente — não só o modelo — determina o resultado.
5. Benchmarks de longo horizonte (SWE-bench Pro, 2025) avaliam tarefas de manutenção e manobras arquiteturais prolongadas — o teste de fogo para agentes em produção real.
6. Plataformas de review assistido por IA (Augment, Qodo) analisam codebases com centenas de milhares de arquivos via grafos de dependência semântica, alinhando patches a specs de alto nível.
7. O relatório DORA 2025 inaugura a agenda "State of AI-assisted Software Development": IA como amplificadora organizacional — culturas disciplinadas aceleram com segurança; culturas desorganizadas aceleram dívida técnica.

## Casos de uso reais

- **Resolução autônoma de issues:** agentes (Devin, Jules, Claude Code) checkout do repositório, reproduzem o bug, rodam suítes de teste e abrem PRs.
- **Spec-driven development:** a spec vira issue/tickets com bloqueios explícitos; o agente executa da spec ao teste; o humano aprova contratos.
- **Testes e verificação com RAG contextual:** sistemas como o "Copilot for Testing" sincronizam detecção de bugs, sugestões de correção e geração de casos de teste com o código-fonte (Wang et al., 2025).
- **Verificação adversarial em pipelines editoriais:** a Fábrica Agêntica de Livros roda auditoria determinística (auditar-obra.py) + revisor técnico independente antes da compilação.
- **Refactoring de legado dirigido por diagnóstico:** o agente lê o código existente, mapeia dependências e propõe refactoring incremental com métricas de melhoria.

## Riscos e limitações

- **Dívida técnica silenciosa:** geração rápida sem governança acelera acúmulo de dívida; ferramentas de IA cortam pela metade o tempo em tarefas repetitivas, mas exigem revisão (Gurgul et al., 2026).
- **Estabilidade vs. throughput (DORA 2025):** mudanças frequentes sem controle de qualidade aumentam change failure rate.
- **Alucinação e confiança:** agentes podem inventar APIs, referências ou comportamento; a verificação adversarial é o mitigador estrutural.
- **Erosão de competências júnior:** o uso acrítico de IA pode corroer habilidades fundamentais de desenvolvedores iniciantes.
- **Custo e rate limits:** o custo dominante do ciclo deixa de ser horas-homem e vira tokens + contexto; sessões esgotadas no meio do build são perda dupla.
- **Contexto limitado:** restrições de contexto exigem LeanCTX, subagentes especializados e handoffs bem projetados (GENIUS/AIware, 2025).

## Artigos científicos (papers citáveis)

1. JIMENEZ, Carlos E. et al. *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* ICLR 2024. Disponível em: https://arxiv.org/abs/2310.06770. Acesso em: 02 ago. 2026.
2. YANG, John et al. *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering.* NeurIPS 2024. Disponível em: https://arxiv.org/abs/2405.15793. Acesso em: 02 ago. 2026.
3. JIN, Haolin et al. *From LLMs to LLM-based Agents for Software Engineering: A Survey of Current, Challenges and Future.* 2025. Disponível em: https://arxiv.org/abs/2408.02479. Acesso em: 02 ago. 2026.
4. GURGUL, Vincent; GUBELA, Robin; LESSMANN, Stefan. *The State of Generative AI in Software Development: Insights from Literature and a Developer Survey.* 2026. Disponível em: https://arxiv.org/abs/2603.16975. Acesso em: 02 ago. 2026.
5. GRÖPLER, Robin et al. *The Future of Generative AI in Software Engineering: A Vision from Industry and Academia in the European GENIUS Project.* IEEE/ACM AIware, 2025. Disponível em: https://arxiv.org/abs/2511.01348. Acesso em: 02 ago. 2026.
6. HODA, Rashina. *Toward Agentic Software Engineering Beyond Code: Framing Vision, Values, and Vocabulary.* ICSE 2026 Workshop. Disponível em: https://arxiv.org/abs/2510.19692. Acesso em: 02 ago. 2026.
7. WANG, Yuchen; GUO, Shangxin; TAN, Chee Wei. *From Code Generation to Software Testing: AI Copilot with Context-Based RAG.* 2025. Disponível em: https://arxiv.org/abs/2504.01866. Acesso em: 02 ago. 2026.
8. *SWE-bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?* 2025. Disponível em: https://arxiv.org/abs/2509.16941. Acesso em: 02 ago. 2026.
9. *Software Testing with Large Language Models: Current Practice and Challenges.* 2025. Disponível em: https://arxiv.org/abs/2510.17164. Acesso em: 02 ago. 2026.

## Fontes brutas

- ANTHROPIC. *Introducing the Model Context Protocol.* Disponível em: https://www.anthropic.com/news/model-context-protocol. Acesso em: 02 ago. 2026.
- ANTHROPIC. *Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet.* Disponível em: https://www.anthropic.com/news/swe-bench-sonnet. Acesso em: 02 ago. 2026.
- HINGEL, Paula. *How AI Changes the SDLC: A Six-Stage Guide.* Augment Code, 2026. Disponível em: https://www.augmentcode.com/guides/how-ai-changes-the-sdlc. Acesso em: 02 ago. 2026.
- MICROSOFT. *An AI led SDLC: Building an End-to-End Agentic Software Development Lifecycle with Azure and GitHub.* Microsoft Tech Community, 2026. Disponível em: https://techcommunity.microsoft.com/blog/appsonazureblog/an-ai-led-sdlc-building-an-end-to-end-agentic-software-development-lifecycle-wit/4491896. Acesso em: 02 ago. 2026.
- GOOGLE CLOUD. *State of AI-assisted Software Development (DORA 2025).* Disponível em: https://dora.dev/research/. Acesso em: 02 ago. 2026.
- COGNITION. *Devin: AI Software Engineer.* Disponível em: https://devin.ai. Acesso em: 02 ago. 2026.
- MODEL CONTEXT PROTOCOL. *Documentação oficial do protocolo.* Disponível em: https://modelcontextprotocol.io. Acesso em: 02 ago. 2026.
- OPENCODE. *OpenCode: harness de desenvolvimento agêntico.* Disponível em: https://opencode.ai. Acesso em: 02 ago. 2026.
- SWE-BENCH. *Benchmark oficial.* Disponível em: https://www.swebench.com. Acesso em: 02 ago. 2026.
- GITHUB. *GitHub Copilot: documentação e pesquisas de impacto.* Disponível em: https://github.com/features/copilot. Acesso em: 02 ago. 2026.
- FORRESTER. *The Agentic Software Engineering wave (2026).* Disponível em: https://www.forrester.com. Acesso em: 02 ago. 2026.
- ROYCHOUDHURY, Abhik et al. *Agentic Software Engineering: state and perspectives.* 2025. Disponível em: https://arxiv.org/abs/2509.09893. Acesso em: 02 ago. 2026.
- QODO. *AI-assisted code review.* Disponível em: https://www.qodo.ai. Acesso em: 02 ago. 2026.
- AUGMENT CODE. *Codebase intelligence e review semântico.* Disponível em: https://www.augmentcode.com. Acesso em: 02 ago. 2026.
- MONASH UNIVERSITY. *Research group on AI in software engineering (Hoda).* Disponível em: https://www.monash.edu. Acesso em: 02 ago. 2026.
- CLARKE, Peter et al. *Model Context Protocol: overview e adoção.* 2025. Disponível em: https://arxiv.org/abs/2504.11423. Acesso em: 02 ago. 2026.
- LEHMANN, Fabian et al. *Software Engineering in the Era of LLMs.* 2024. Disponível em: https://arxiv.org/abs/2403.09752. Acesso em: 02 ago. 2026.
- MOHAGHEGHI, Milad et al. *Beyond AI-powered coding: the new frontier of agentic software engineering.* 2025. Disponível em: https://arxiv.org/abs/2509.14838. Acesso em: 02 ago. 2026.
- ANTHROPIC. *Building effective agents.* Disponível em: https://www.anthropic.com/research/building-effective-agents. Acesso em: 02 ago. 2026.
- SWE-BENCH PRO. *Benchmark de tarefas de longo horizonte.* Disponível em: https://www.swebench.com/pro. Acesso em: 02 ago. 2026.
