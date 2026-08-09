# Dossiê de Pesquisa — Skills e Commands: empacotando conhecimento reutilizável para agentes

> Livro 6 da Parte III (A camada de harness) — série de mega-livro da Fábrica Agêntica.
> Tema: como empacotar conhecimento procedural (skills) e fluxos determinísticos (commands)
> para agentes de IA, dentro da camada de harness que orquestra o loop agêntico.

## Conceitos-chave

- **Agent Skill**: pacote modular baseado em sistema de arquivos (pasta com `SKILL.md` + scripts/references/assets) que estende as capacidades de um agente de IA, transformando-o em especialista de domínio. Diferente de prompts efêmeros ou do `CLAUDE.md` estático (agentskills.io; ANTHROPIC).
- **Progressive Disclosure (Divulgação Progressiva)**: princípio de carregamento em 3 níveis — (1) apenas metadados YAML (`name`/`description`, ~100 tokens) sempre injetados no system prompt; (2) corpo do `SKILL.md` lido sob demanda quando o gatilho semântico é acionado; (3) scripts e referências executados/abertos conforme necessário, sem poluir a janela de contexto (agentskills.io/specification).
- **Harness (arreio do agente)**: camada de software que envolve o LLM (política estocástica de geração) e o transforma em agente funcional, stateful e autônomo — controla o agent loop (raciocínio→ação→observação), sandboxes, gestão de contexto/memória e tool use. É onde skills e commands são registrados e despachados (arXiv:2605.18747; ANTHROPIC).
- **Slash Command customizado**: arquivo Markdown (`.claude/commands/*.md` legado ou formato de skill) com frontmatter YAML (`description`, `argument-hint`, `allowed-tools`, `disable-model-invocation`) que mapeia um comando curto (`/nome`) para um prompt multi-etapas determinístico; captura argumentos via `$ARGUMENTS` e placeholders `$0..$n` (code.claude.com/docs).
- **Injeção dinâmica de contexto**: linhas `!` (execução Bash em tempo real, ex. `!git diff HEAD`) e `@` (referência a arquivos, ex. `@package.json`) nos arquivos de comando, executadas antes de montar o prompt (code.claude.com/docs).
- **Model Context Protocol (MCP)**: padrão aberto cliente-servidor (JSON-RPC 2.0) que separa ferramentas, recursos e prompts; doado à Linux Foundation em dez. 2025. Complementar às skills: MCP conecta dados/ferramentas externos; skills codificam o "saber fazer" procedural (arXiv:2504.21030).
- **Scaffolding**: infraestrutura estática montada antes do primeiro prompt (system prompt, registro de ferramentas, injeção de habilidades); o harness governa o comportamento dinâmico durante a execução (arXiv:2603.05344).
- **Capability Uplift vs Encoded Preference**: taxonomia de skills — (a) elevam capacidades que o agente não tem (Playwright, scraping, PDF); (b) codificam preferência/opinião/estilo da equipe (regras de revisão, estilo de código) (FIRECRAWL).
- **Memória procedural**: camada da memória do agente que guarda o "como fazer" (skills/tips recuperáveis), distinta da episódica e semântica; frameworks recentes extraem strategy/recovery/optimization tips de trajetórias de execução (arXiv:2603.10600; arXiv:2603.07670).

## Artigos Científicos e Papers

- XU, Renjun; YAN, Yang. *Agent Skills for Large Language Models: Architecture, Acquisition, Security, and the Path Forward*. In: ACM CAIS, 2026. Disponível em: https://arxiv.org/abs/2602.12430. Acesso em: 06 ago. 2026.
- ZHANG, et al. *Code as Agent Harness: Toward Executable, Verifiable, and Stateful Agent Systems*. In: arXiv, 2026. Disponível em: https://arxiv.org/abs/2605.18747. Acesso em: 06 ago. 2026.
- *Stop Comparing LLM Agents Without Disclosing the Harness*. In: arXiv, 2026. Disponível em: https://arxiv.org/abs/2605.23950. Acesso em: 06 ago. 2026.
- BUI, et al. *Building AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned*. In: arXiv, 2026. Disponível em: https://arxiv.org/abs/2603.05344. Acesso em: 06 ago. 2026.
- *Natural-Language Agent Harnesses (NLAHs)*. In: arXiv, 2026. Disponível em: https://arxiv.org/abs/2603.25723. Acesso em: 06 ago. 2026.
- KRISHNAN, Naveen. *Advancing Multi-Agent Systems Through Model Context Protocol*. In: arXiv, 2025. Disponível em: https://arxiv.org/abs/2504.21030. Acesso em: 06 ago. 2026.
- MA, Zhiyuan; LIU, Jiayu; LUO, Xianzhen; HUANG, Zhenya; ZHU, Qingfu; CHE, Wanxiang. *Tool-MVR: Meta-Verification and Reflection Learning for Reliable Tool-Use*. In: KDD 2025 / arXiv, 2025. Disponível em: https://arxiv.org/abs/2506.04625. Acesso em: 06 ago. 2026.
- DU, Pengfei. *Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers*. In: arXiv, 2026. Disponível em: https://arxiv.org/abs/2603.07670. Acesso em: 06 ago. 2026.
- FANG, Gaodan; ISAHAGIAN, Vatche; JAYARAM, K. R.; KUMAR, Ritesh; MUTHUSAMY, Vinod; OUM, Punleuk; THOMAS, Gegi. *Trajectory-Informed Memory Generation for Self-Improving Agent Systems*. In: IBM Research / arXiv, 2026. Disponível em: https://arxiv.org/abs/2603.10600. Acesso em: 06 ago. 2026.
- YANG, Chang; ZHOU, Chuang; XIAO, Yilin; et al. *Graph-based Agent Memory: Taxonomy, Techniques, and Applications*. In: arXiv, 2026. Disponível em: https://arxiv.org/abs/2602.05665. Acesso em: 06 ago. 2026.

## Estado da arte / ferramentas de referência

- **Especificação aberta de Agent Skills** (agentskills.io): padrão agnóstico de ferramenta — `skill-name/SKILL.md` (frontmatter obrigatório `name` + `description`, opcionais `license`, `compatibility`, `metadata`, `allowed-tools`) + `scripts/`, `references/`, `assets/`. Especificação: https://agentskills.io/specification.
- **anthropics/skills**: repositório oficial da Anthropic com skills de demonstração (PDF, DOCX, XLSX, PPTX, entre outras). https://github.com/anthropics/skills.
- **Claude Code Skills & Commands**: documentação oficial — `.claude/skills/<skill>/SKILL.md` e `.claude/commands/`, frontmatter com `disable-model-invocation`, `argument-hint`, `allowed-tools`/`disallowed-tools`, `context: fork`, placeholders `$ARGUMENTS`/`$0..$n`, injeção `!cmd` e `@file`. https://code.claude.com/docs/en/skills; https://code.claude.com/docs/en/agent-sdk/slash-commands.
- **skills.sh / Vercel Labs**: marketplace e gerenciador de pacotes aberto — `npx skills add <owner/repo> --skill <nome>` para buscar, auditar e instalar skills do GitHub. https://skills.sh; https://github.com/vercel-labs/skills.
- **obra/superpowers**: framework metodológico de engenharia para agentes (brainstorming, TDD, subagentes), compatível com Claude Code, Cursor, Codex, Gemini CLI, Copilot CLI, OpenCode, Pi. https://github.com/obra/superpowers.
- **awesome-skills.com**: curadoria comunitária de centenas de skills (frontend Vercel, regras Karpathy, scraping Firecrawl, segurança Trail of Bits). https://awesome-skills.com.
- **RUCAIBox/awesome-agent-harness**: curadoria de pesquisa e ferramentas da área de harness engineering. https://github.com/RUCAIBox/awesome-agent-harness.
- **AGENTS.md (Codex/OpenAI)**: arquivo padrão aberto de instruções de projeto lido pelo agente antes de planejar; abordagem complementar às skills. https://learn.chatgpt.com/docs/agent-configuration/agents-md.
- **Cursor Rules (.mdc)**: arquivos de regras com frontmatter `globs` para anexo dinâmico por escopo de arquivo. https://cursor.com/docs/rules.
- **Windsurf Rules**: `.windsurfrules` e `.windsurf/rules/*.md` com modos de ativação por contexto. https://codeium.com/windsurf.

## Casos de uso corporativos

- **Anthropic (uso interno)**: equipes de data infrastructure usam agentes para diagnosticar falhas em clusters Kubernetes e permitir que finanças/jurídico construam ferramentas via descrição em texto; padrões internos documentados em arquivos de contexto (CLAUDE.md) melhoram a precisão do agente. Fonte: Codingscape (https://codingscape.com/blog/how-anthropic-engineering-teams-use-claude-code-every-day).
- **Fountain**: orquestração multi-agente hierárquica por escopos (Security, API, Frontend) para revisões de código em paralelo. Fonte: Claude Code Ultimate Guide (https://github.com/FlorianBruniaux/claude-code-ultimate-guide).
- **CRED (fintech, 15M+ usuários)**: agentes integrados ao SDLC completo mantendo conformidade de serviços financeiros, dobrando a velocidade de execução. Fonte: Claude Code Ultimate Guide (idem).
- **Padrão de governança de agentes em 4 pilares**: (1) documentação contextual (CLAUDE.md/AGENTS.md); (2) slash commands customizados para fluxos repetitivos (`/security-scan`, `/deploy-staging`); (3) skills reutilizáveis que codificam conhecimento institucional; (4) governança de permissões (`.permissions.allow`) e servidores MCP intermediando dados sensíveis. Fonte: GetDX (https://getdx.com/blog/ai-code-enterprise-adoption/); Medium/Heeki Park (https://heeki.medium.com/collaborating-with-agents-teams-in-claude-code-f64a465f3c11).
- **SWE-bench como padrão de medição**: agentes com scaffolding correto ultrapassam 45-50% de acurácia no SWE-bench Verified; a variação de desempenho é dominada pelo harness, não só pelo modelo (tese da Binding Constraint). Fonte: https://www.anthropic.com/engineering/swe-bench-sonnet; https://www.swebench.com.

## Limitações e controvérsias

- **Segurança de skills de comunidade**: skills instaladas de fontes não confiáveis podem conter instruções maliciosas ou scripts com efeitos colaterais; o paper de Xu & Yan (2026) propõe o "Skill Trust and Lifecycle Governance Framework" e taxonomia de aquisição. A skill de auditoria de segurança deve preceder a instalação (skill-security-auditor).
- **Progressive disclosure depende de descrição de qualidade**: a ativação de uma skill depende do gatilho semântico da `description`; descrições vagas ou com overtriggering degradam a precisão do agente e aumentam o ruído de contexto.
- **Skills vs prompts monolíticos**: teams recém-migrados tendem a empilhar tudo em `CLAUDE.md` (contexto sempre ativo, custo de tokens fixo); skills transferem esse custo para carregamento sob demanda, mas exigem disciplina de organização e testes.
- **Tensão entre determinismo e flexibilidade**: commands são determinísticos (fluxos fixos), mas podem ficar obsoletos quando o harness/modelo evolui; skills de linguagem natural (NLAHs) propõem harnesses editáveis em linguagem natural, invertendo essa rigidez (arXiv:2603.25723).
- **Benchmarks sem disclousure de harness**: comparar LLM agents sem descrever o harness (contexto, ferramentas, scaffolding) produz métricas enganosas — a tese da Binding Constraint Thesis (arXiv:2605.23950) exige relato transparente do harness em qualquer avaliação.
- **Memória e janela de contexto**: tarefas longas estouram a janela; compactação adaptativa, arquivos de progresso e memória procedural são mitigadores, mas cada um adiciona complexidade de manutenção e risco de perda de informação (ANTHROPIC effective harnesses; arXiv:2603.07670).

## Fontes brutas (para Nó 7 — Auditor de Rastreabilidade)

- AGENTSKILLS.IO. *Agent Skills Specification*. Disponível em: https://agentskills.io/specification. Acesso em: 06 ago. 2026.
- ANTHROPIC. *Agent Skills — Claude Platform Docs*. Disponível em: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview. Acesso em: 06 ago. 2026.
- ANTHROPIC. *Claude Code Skills Documentation*. Disponível em: https://code.claude.com/docs/en/skills. Acesso em: 06 ago. 2026.
- ANTHROPIC. *Claude Code SDK — Slash Commands*. Disponível em: https://code.claude.com/docs/en/agent-sdk/slash-commands. Acesso em: 06 ago. 2026.
- ANTHROPIC. *Effective Harnesses for Long-Running Agents*. Disponível em: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents. Acesso em: 06 ago. 2026.
- ANTHROPIC. *Claude 3.5 Sonnet and SWE-bench*. Disponível em: https://www.anthropic.com/engineering/swe-bench-sonnet. Acesso em: 06 ago. 2026.
- ANTHROPIC. *Anthropic Skills Repository*. Disponível em: https://github.com/anthropics/skills. Acesso em: 06 ago. 2026.
- BUI, et al. *Building AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned*. Disponível em: https://arxiv.org/abs/2603.05344. Acesso em: 06 ago. 2026.
- CODINGSCAPE. *How Anthropic Engineering Teams Use Claude Code Every Day*. Disponível em: https://codingscape.com/blog/how-anthropic-engineering-teams-use-claude-code-every-day. Acesso em: 06 ago. 2026.
- CURSOR. *Cursor Rules Documentation*. Disponível em: https://cursor.com/docs/rules. Acesso em: 06 ago. 2026.
- DU, Pengfei. *Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers*. Disponível em: https://arxiv.org/abs/2603.07670. Acesso em: 06 ago. 2026.
- FANG, Gaodan; ISAHAGIAN, Vatche; JAYARAM, K. R.; KUMAR, Ritesh; MUTHUSAMY, Vinod; OUM, Punleuk; THOMAS, Gegi. *Trajectory-Informed Memory Generation for Self-Improving Agent Systems*. Disponível em: https://arxiv.org/abs/2603.10600. Acesso em: 06 ago. 2026.
- FIRECRAWL. *Best Claude Code Skills to Try*. Disponível em: https://www.firecrawl.dev/blog/best-claude-code-skills. Acesso em: 06 ago. 2026.
- FLORIANBRUNIAUX. *Claude Code Ultimate Guide — Agent Teams*. Disponível em: https://github.com/FlorianBruniaux/claude-code-ultimate-guide. Acesso em: 06 ago. 2026.
- GETDX. *AI Code Generation: Best Practices for Enterprise Adoption*. Disponível em: https://getdx.com/blog/ai-code-enterprise-adoption/. Acesso em: 06 ago. 2026.
- KRISHNAN, Naveen. *Advancing Multi-Agent Systems Through Model Context Protocol*. Disponível em: https://arxiv.org/abs/2504.21030. Acesso em: 06 ago. 2026.
- MA, Zhiyuan; LIU, Jiayu; LUO, Xianzhen; HUANG, Zhenya; ZHU, Qingfu; CHE, Wanxiang. *Tool-MVR: Meta-Verification and Reflection Learning for Reliable Tool-Use*. Disponível em: https://arxiv.org/abs/2506.04625. Acesso em: 06 ago. 2026.
- MEDIUM (HEEKI PARK). *Collaborating with Agent Teams in Claude Code*. Disponível em: https://heeki.medium.com/collaborating-with-agents-teams-in-claude-code-f64a465f3c11. Acesso em: 06 ago. 2026.
- OPENAI. *Custom Instructions with AGENTS.md*. Disponível em: https://learn.chatgpt.com/docs/agent-configuration/agents-md. Acesso em: 06 ago. 2026.
- RUCAIBOX. *Awesome Agent Harness*. Disponível em: https://github.com/RUCAIBox/awesome-agent-harness. Acesso em: 06 ago. 2026.
- SWEBENCH. *SWE-bench Verified & Pro*. Disponível em: https://www.swebench.com. Acesso em: 06 ago. 2026.
- VERCEL LABS. *Skills — package manager for agent skills*. Disponível em: https://github.com/vercel-labs/skills. Acesso em: 06 ago. 2026.
- VERCEL LABS. *skills.sh — open marketplace*. Disponível em: https://skills.sh. Acesso em: 06 ago. 2026.
- VINCENT, Jesse (obra). *Superpowers — engineering skills for agents*. Disponível em: https://github.com/obra/superpowers. Acesso em: 06 ago. 2026.
- VSCODE. *VS Code Agent Skills Documentation*. Disponível em: https://code.visualstudio.com/docs/agent-customization/agent-skills. Acesso em: 06 ago. 2026.
- WINDSURF (CODEIUM). *Windsurf Documentation*. Disponível em: https://codeium.com/windsurf. Acesso em: 06 ago. 2026.
- XU, Renjun; YAN, Yang. *Agent Skills for Large Language Models: Architecture, Acquisition, Security, and the Path Forward*. Disponível em: https://arxiv.org/abs/2602.12430. Acesso em: 06 ago. 2026.
- YANG, Chang; ZHOU, Chuang; XIAO, Yilin; et al. *Graph-based Agent Memory: Taxonomy, Techniques, and Applications*. Disponível em: https://arxiv.org/abs/2602.05665. Acesso em: 06 ago. 2026.
- ZHANG, et al. *Code as Agent Harness: Toward Executable, Verifiable, and Stateful Agent Systems*. Disponível em: https://arxiv.org/abs/2605.18747. Acesso em: 06 ago. 2026.
- *Stop Comparing LLM Agents Without Disclosing the Harness*. Disponível em: https://arxiv.org/abs/2605.23950. Acesso em: 06 ago. 2026.
- *Natural-Language Agent Harnesses (NLAHs)*. Disponível em: https://arxiv.org/abs/2603.25723. Acesso em: 06 ago. 2026.
