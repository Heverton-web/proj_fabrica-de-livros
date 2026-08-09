# Dossiê: Antes do prompt — fundamentos de software e de modelos de linguagem

**Série:** A Pilha Agêntica (Livro 1)
**Objetivo da obra:** preparar alguém que nunca programou — ou que programa mas nunca usou IA de forma séria — para toda a série. Ninguém entende Context Engineering sem entender o que é uma janela de contexto; ninguém entende Harness Engineering sem entender o que é um hook, um teste automatizado ou uma máquina de estados.
**Público:** iniciante absoluto em programação e IA, com aspiração a dominar AI-Driven Development (AIDD) até o nível profissional.

---

## Visão Geral

O Livro 1 da série "A Pilha Agêntica" constrói o "chão" técnico sobre o qual toda a série se apoia. Ele cobre duas metades que se complementam: (1) os fundamentos de engenharia de software que qualquer pessoa precisa dominar antes de orquestrar agentes de IA (lógica de programação, Git, arquitetura, testes, CI/CD, observabilidade) e (2) o funcionamento real dos modelos de linguagem (tokens, janela de contexto, atenção, alucinação, sampling) — porque não se entende Context Engineering sem entender o que o modelo "vê". O livro termina com o vocabulário essencial do campo (agente, modelo, tool, tool calling, function calling) e o panorama histórico que leva de autocomplete a agentes autônomos (2022–2026).

## Por que este livro importa

Em agosto de 2026, a maior parte do mercado ainda trata "prompt engineering" como o teto da disciplina — mas o profissional fluente em AIDD opera uma pilha inteira: Context Engineering, MCP Engineering, Rules Engineering, Skills Engineering, Hook Engineering, Spec Engineering, Loop Engineering, Harness Engineering e Eval Engineering. Todas essas disciplinas assumem o leitor como dono do chão técnico. Sem esse chão, o restante da pilha não se sustenta.

---

## Bloco 1 — Fundamentos de software para quem nunca programou

### 1.1 Lógica de programação essencial
- Variáveis, tipos, condicionais, loops, funções — o vocabulário comum a todas as linguagens.
- Como ler código sem se aprofundar em uma linguagem só: reconhecer padrões estruturais.
- Pensamento algorítmico: decompor um problema em passos executáveis por uma máquina.
- Por que agentes de IA escrevem código — e por que o humano precisa saber ler e validar o que foi escrito.

### 1.2 Controle de versão (Git), branches e pull requests
- O modelo de snapshots do Git e por que versionar código é inegociável.
- Branches como isolamento de trabalho; pull requests como porta de entrada de mudanças com revisão.
- Estratégias de branching: Git Flow, GitHub Flow, Trunk-Based Development.
- Por que nenhum fluxo agêntico funciona sem Git: agentes criam branches, abrem PRs e rodam CI (GitHub Actions, Codex, Claude Code).

### 1.3 Arquitetura de software básica
- Funções e módulos: organizar código em blocos reutilizáveis (deep modules).
- O que é uma API: contratos entre sistemas; HTTP, requisições e respostas; servidores.
- Bancos de dados: por que dados precisam ser persistidos; SQL e armazenamento.
- Modelo cliente-servidor e o que acontece quando você abre um site.

### 1.4 Testes automatizados, CI/CD e observabilidade
- Testes unitários, de integração e E2E: a pirâmide de testes (Vocke; Fowler).
- TDD e o ciclo red-green-refactor (Beck).
- CI/CD: integração contínua, automação de build, pipelines (Fowler; GitHub Actions; GitLab CI).
- Observabilidade: os três pilares (logs, métricas, traces) e os Quatro Sinais de Ouro do Google SRE.
- Por que essas disciplinas "voltaram" a importar na era da IA: com 40–60% do código em PRs corporativos sendo gerado por IA, test gates e validação determinística são a defesa.

---

## Bloco 2 — Como um modelo de linguagem realmente funciona

### 2.1 Tokens e tokenização
- Token ≠ palavra: subpalavras (BPE); ~4 caracteres/token em inglês; português acentuado custa mais.
- Vocabulário fixo de 32k–256k tokens; ferramenta oficial da OpenAI para visualizar.
- Implicação prática: "orçamento" de tokens é dinheiro e atenção.

### 2.2 Janela de contexto e codificação posicional
- Janela de contexto = limite de tokens (entrada + saída) processados em uma inferência.
- RoPE e extensão de contexto para 1M+ tokens (Llama, Gemini 1.5).
- Atenção com custo quadrático O(n²) e otimizações (Ring Attention).
- Contexto longo ≠ memória: context rot e degradação da atenção em meio ao contexto (Chroma; Anthropic).

### 2.3 Mecanismo de atenção
- Self-attention: queries, keys e values; o que o modelo "procura" ao prever o próximo token.
- Por que atenção explica tanto a qualidade quanto as falhas dos LLMs.

### 2.4 Por que modelos "alucinam"
- Taxonomia de alucinações extrínsecas (Weng, 2024): dados de pré-treinamento, fine-tuning de conhecimento novo.
- Mitigações: RAG, avaliação por agentes (SAFE), citações verificáveis.
- Implicação prática para AIDD: nunca confiar cegamente em fatos gerados; sempre ancorar em fontes.

### 2.5 Temperatura e amostragem
- Modelo gera distribuição de probabilidade sobre o vocabulário; temperatura controla achatamento.
- Top-k e Top-p (nucleus sampling); temperatura 0 ≈ determinístico.
- Por que o mesmo prompt pode dar respostas diferentes — e como isso afeta testes de agentes.

---

## Bloco 3 — Vocabulário essencial do campo

- **Modelo (LLM):** motor cognitivo; processa linguagem, raciocina, gera tokens; estático sem ferramentas.
- **Tool / Ferramenta:** interface externa (API, banco, interpretador, script, servidor MCP) que o modelo pode chamar.
- **Tool calling / Function calling:** troca estruturada — definição de ferramentas em JSON Schema → decisão do modelo → execução local → observação devolvida ao modelo (OpenAI; Prompting Guide).
- **Agente:** sistema autônomo sobre um LLM que combina raciocínio, planejamento, memória e tool calling em um loop (ação → observação → decisão).
- **Framework clássico de agente:** Agente = LLM + Memória + Planejamento + Ferramentas (Weng, 2023).

---

## Bloco 4 — Panorama histórico: de autocomplete a agentes autônomos (2022–2026)

1. **2021–2022 — Autocomplete:** GitHub Copilot (Codex) integrado ao editor; predição de linhas e funções.
2. **2023 — Conversacional:** ChatGPT; Copilot Chat; indexação de repositórios na nuvem; "ler o projeto".
3. **2024 — Protocolos e padrões:** Model Context Protocol (MCP) da Anthropic padroniza conexões de dados e ferramentas; início do agentic coding.
4. **2025 — Agentes de terminal e IDEs nativas de IA:** Claude Code, OpenAI Codex reimaginado, Cursor/Windsurf (Composer/Cascade), GitHub Copilot Coding Agent, Google Jules.
5. **2026 — Era dos agentes autônomos e do AIDD:** OpenCode (dual-agent, 75+ provedores), AGENTS.md/CLAUDE.md como camada de instrução persistente, 92% dos devs dos EUA usam IA diariamente, 40–60% do código em PRs é gerado por IA, confiança na exatidão cai para 29% — e o desenvolvedor vira arquiteto/especificador/revisor.

---

## Artigos Científicos

1. **LULLA, Jai Lal; et al.** *On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents*. Singapore Management University / Heidelberg University / King's College London, 2026 (JAWs 2026 / arXiv:2601.20404v1). Estudo empírico em 124 PRs do GitHub: AGENTS.md reduz tempo médio de execução em 28,64% (mediana) e consumo de tokens de saída em 16,58%.
2. **GEKHMAN, Zorik; et al.** *Does Fine-Tuning LLMs on New Knowledge Encourage Hallucinations?* (2024). Estudo empírico que mostra como o fine-tuning de conhecimento novo desestabiliza o alinhamento e induz a mais alucinações.
3. **WENG, Lilian.** *LLM-Powered Autonomous Agents* (2023). O framework acadêmico clássico: Agente = LLM + Memória + Planejamento + Ferramentas; referência para todo o estudo de agentes.
4. **WENG, Lilian.** *Extrinsic Hallucinations in LLMs* (2024). Taxonomia e mitigação de alucinações — base para o capítulo de por que modelos "alucinam".

---

## Fontes brutas

- ANTHROPIC. *Introducing the Model Context Protocol*. Disponível em: https://www.anthropic.com/news/model-context-protocol. Acesso em: 5 ago. 2026.
- ANTHROPIC. *Effective Context Engineering for AI Agents*. Disponível em: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents. Acesso em: 5 ago. 2026.
- ATLASSIAN. *Git branching strategies*. Disponível em: https://www.atlassian.com/git/tutorials/comparing-workflows. Acesso em: 5 ago. 2026.
- BECK, Kent. *Test-Driven Development: By Example*. Boston: Addison-Wesley Professional, 2002.
- CHACON, Scott; STRAUB, Ben. *Pro Git*. 2. ed. Apress/Git SCM, 2014. Disponível em: https://git-scm.com/book/en/v2. Acesso em: 5 ago. 2026.
- CHROMA. *Context Rot: How Increasing Input Tokens Impacts LLM Performance*. Disponível em: https://www.trychroma.com/research/context-rot. Acesso em: 5 ago. 2026.
- CODERABBIT. *From Copilot to agents: The history of AI coding*. Disponível em: https://www.coderabbit.ai/blog/a-very-brief-history-of-ai-coding-from-copilot-to-next-gen-agents. Acesso em: 5 ago. 2026.
- DAILY.DEV. *Vibe Coding Explained: AI-Driven Development in 2026*. Disponível em: https://daily.dev/blog/vibe-coding-2026-ai-changing-how-developers-write-code/. Acesso em: 5 ago. 2026.
- EWASCHUK, Rob; BEYER, Betsy (Ed.). *Site Reliability Engineering: Monitoring Distributed Systems*. Google SRE Book. Disponível em: https://sre.google/sre-book/monitoring-distributed-systems/. Acesso em: 5 ago. 2026.
- FOWLER, Martin. *Continuous Integration*. Disponível em: https://martinfowler.com/articles/continuousIntegration.html. Acesso em: 5 ago. 2026.
- GARTENBERG, Chaim. *What is a long context window?* Google DeepMind. Disponível em: https://blog.google/innovation-and-ai/products/long-context-window-ai-models/. Acesso em: 5 ago. 2026.
- GITHUB ACTIONS DOCS. *Understanding GitHub Actions*. Disponível em: https://docs.github.com/en/actions/about-github-actions/understanding-github-actions. Acesso em: 5 ago. 2026.
- GITHUB DOCS. *About branches*. Disponível em: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-branches. Acesso em: 5 ago. 2026.
- GITHUB DOCS. *About pull requests*. Disponível em: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests. Acesso em: 5 ago. 2026.
- GITLAB. *CI/CD pipeline architecture*. Disponível em: https://docs.gitlab.com/ee/ci/. Acesso em: 5 ago. 2026.
- GOOGLE AI DEVELOPERS. *Long Context Guide (Gemini API)*. Disponível em: https://ai.google.dev/gemini-api/docs/long-context. Acesso em: 5 ago. 2026.
- ITECS. *Claude Code vs. GitHub Copilot: Agentic vs. Autocomplete*. Disponível em: https://itecsonline.com/post/claude-code-vs-github-copilot-2026-agentic-vs-autocomplete-enterprise-guide. Acesso em: 5 ago. 2026.
- KARPATHY, Andrej. *Software 3.0: Software in the Age of AI* (palestra, transcrição comentada por Latent Space). Disponível em: https://www.latent.space/p/s3. Acesso em: 5 ago. 2026.
- KARPATHY, Andrej. *Sequoia Ascent 2026 Summary (Software 3.0 & Agentic Engineering)*. Disponível em: https://karpathy.bearblog.dev/sequoia-ascent-2026/. Acesso em: 5 ago. 2026.
- KEYHOLE SOFTWARE. *Vibe Coding Trends 2026: Adoption, Productivity, and Code Quality Data*. Disponível em: https://keyholesoftware.com/vibe-coding-trends-2026/. Acesso em: 5 ago. 2026.
- LATENT SPACE. *How to train a Million Context LLM — with Mark Huang of Gradient.ai*. Disponível em: https://www.latent.space/p/gradient. Acesso em: 5 ago. 2026.
- LULLA, Jai Lal; et al. *On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents*. Disponível em: https://arxiv.org/html/2601.20404v1. Acesso em: 5 ago. 2026.
- MIGHTYBOT. *Best AI Coding Agents in 2026, Ranked*. Disponível em: https://mightybot.ai/blog/coding-ai-agents-for-accelerating-engineering-workflows/. Acesso em: 5 ago. 2026.
- OPENAI. *Function Calling Guide*. Disponível em: https://developers.openai.com/api/docs/guides/function-calling. Acesso em: 5 ago. 2026.
- OPENAI. *Tokenizer (ferramenta interativa)*. Disponível em: https://platform.openai.com/tokenizer. Acesso em: 5 ago. 2026.
- OPENAI / AGENTS.MD FOUNDATION. *Open Standards for Agentic Configuration (AGENTS.md)*. Disponível em: https://agents.md/. Acesso em: 5 ago. 2026.
- OPENTELEMETRY. *What is OpenTelemetry?* Disponível em: https://opentelemetry.io/docs/what-is-opentelemetry/. Acesso em: 5 ago. 2026.
- PROMPTING GUIDE. *Function Calling in AI Agents*. Disponível em: https://www.promptingguide.ai/agents/function-calling. Acesso em: 5 ago. 2026.
- SITEPOINT. *Vibe Coding 2026: The Complete Guide to AI-First Development*. Disponível em: https://www.sitepoint.com/vibe-coding-2026-complete-guide/. Acesso em: 5 ago. 2026.
- TESTING LIBRARY. *Guiding Principles*. Disponível em: https://testing-library.com/docs/guiding-principles/. Acesso em: 5 ago. 2026.
- TIAN PAN. *CLAUDE.md and AGENTS.md: The Configuration Layer That Makes AI Coding Agents Actually Follow Your Rules*. Disponível em: https://tianpan.co/blog/2026-02-25-claude-md-agents-md-ai-coding-agent-instruction-files. Acesso em: 5 ago. 2026.
- VOCKE, Ham; FOWLER, Martin. *The Practical Test Pyramid*. Disponível em: https://martinfowler.com/articles/practical-test-pyramid.html. Acesso em: 5 ago. 2026.
- WENG, Lilian. *LLM-Powered Autonomous Agents*. Disponível em: https://lilianweng.github.io/posts/2023-06-23-agent/. Acesso em: 5 ago. 2026.
- WENG, Lilian. *Extrinsic Hallucinations in LLMs*. Disponível em: https://lilianweng.github.io/posts/2024-07-07-hallucination/. Acesso em: 5 ago. 2026.
