# Dossiê de Pesquisa — OpenCode: o que é, para que serve, e aquilo que ninguém te conta

## Conceitos-chave

- **OpenCode**: agente de codificação por IA de código aberto, executado no terminal (TUI), desktop e extensões de IDE. Criado pelo ecossistema SST (hoje mantido sob a organização anomalyco). Site oficial: opencode.ai; repositório oficial: github.com/anomalyco/opencode (anteriormente sst/opencode). [1]
- **TUI (Text User Interface)**: interface de usuário por texto rodando no terminal. O comando `opencode` sem argumentos inicia a TUI — é o uso padrão. [2]
- **Cliente–Servidor**: mesmo rodando localmente, o OpenCode separa a TUI (cliente) do servidor headless (backend). O servidor expõe uma API HTTP com spec OpenAPI 3.1 em `/doc`. Isso permite múltiplos clientes e uso programático. [3]
- **AI SDK + Models.dev**: o OpenCode usa o Vercel AI SDK e o catálogo Models.dev para suportar 75+ provedores de LLM. Credenciais ficam em `~/.local/share/opencode/auth.json`. [4]
- **config.json / opencode.json**: arquivo JSON/JSONC de configuração. Suporta `$schema`, `model`, `small_model`, `provider`, `agent`, `permission`, `instructions`, `server`, `mcp`, `plugin`, `share`, `theme`, `formatter`, `tools`, `environment` etc. Precedência: remota (`.well-known/opencode`) → global (`~/.config/opencode/opencode.json`) → `OPENCODE_CONFIG` → projeto (`opencode.json` no raiz do repo) → `.opencode/` → `OPENCODE_CONFIG_CONTENT` → managed settings (MDM). Configs são mescladas, não substituídas. [5]
- **tui.json**: config específica da TUI (keybinds, tema, scroll, atenção). Schema em opencode.ai/tui.json. [6]
- **MCP (Model Context Protocol)**: protocolo aberto para conectar ferramentas/contexto externo ao LLM. O OpenCode suporta servidores MCP locais e remotos com OAuth automático. [7]
- **Agentes (agents)**: assistentes especializados com prompt, modelo e permissões próprios. Há dois tipos: **primary** (Build e Plan, alternados com Tab) e **subagent** (General, Explore, Scout; invocados por `@`). Agentes custom em JSON ou Markdown (`.opencode/agents/*.md`). [8]
- **Permissões**: sistema de controle de ações (`allow`/`ask`/`deny`) por ferramenta (read, edit, bash, grep, glob, webfetch, websearch, task, skill, lsp, question, external_directory, doom_loop). Suporta padrões glob e sintaxe de objeto por comando. `--auto` aprova tudo que não for explicitamente negado. [9]
- **Slash commands**: comandos internos da TUI como `/init`, `/undo`, `/redo`, `/share`, `/connect`, `/models`, `/theme`, `/help`; comandos custom em Markdown (`.opencode/commands/*.md`) ou via chave `command` no config, com placeholders `$ARGUMENTS`, `$1..$n`, `!comando`, `@arquivo`. [10]
- **Plugins**: extensões JS/TS que engancham eventos do ciclo de vida (ex.: `tool.execute.before`, `session.created`, `shell.env`) e podem adicionar ferramentas custom (SDK `@opencode-ai/plugin`). Carregados de `.opencode/plugins/`, `~/.config/opencode/plugins/` e pacotes npm via chave `plugin`. [11]
- **Compartilhamento (share)**: gera link público `opncd.ai/s/<share-id>` da conversa; modos `manual` (padrão), `auto` e `disabled`. Compartilhado = acessível a qualquer pessoa com o link. [12]
- **Sessões**: conversas persistentes; comandos `opencode session list`, `session delete`; flags `--continue`/`-c`, `--session`/`-s`, `--fork`. Export/import de sessões em JSON (`.json` ou `.md`). [13]
- **AGENTS.md**: arquivo de diretrizes do projeto gerado pelo `/init`; deve ser commitado no Git. O OpenCode também lê `.claude/CLAUDE.md` e `.agents/` (compatibilidade com ecosistemas Claude Code e agentes). [14]
- **Skills**: instruções reutilizáveis em `SKILL.md` (frontmatter `name` + `description`), descobertas sob demanda via ferramenta `skill`. Busca em `.opencode/skills/`, `.claude/skills/`, `.agents/skills/` (projeto e global). [15]
- **OpenCode Zen e OpenCode Go**: serviços oficiais de modelos testados/verificados pela equipe; recomendados para quem está começando; configurados via `/connect` e opencode.ai/auth. [16]
- **Modelos locais**: provedores OpenAI-compatíveis (Ollama, LM Studio, vLLM, Atomic Chat) via `provider` custom com `npm: "@ai-sdk/openai-compatible"` e `options.baseURL`. [17]
- **Servidor headless**: `opencode serve` expõe API HTTP; `opencode web` abre interface web; `opencode attach <url>` conecta a TUI a um servidor remoto. `OPENCODE_SERVER_PASSWORD` habilita basic auth. [18]

## Artigos Científicos e Papers

- YANG, John; JIMENEZ, Carlos E.; WETTIG, Alexander; LIERET, Kilian; YAO, Shunyu; NARASIMHAN, Karthik; PRESS, Ofir. *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering*. In: NEURIPS, 2024. Disponível em: https://arxiv.org/abs/2405.15793. Acesso em: 03 ago. 2026.
- XIA, Chunqiu Steven; DENG, Yinlin; DUNN, Soren; ZHANG, Lingming. *Agentless: Demystifying LLM-based Software Engineering Agents*. arXiv, 2024. Disponível em: https://arxiv.org/abs/2407.01489. Acesso em: 03 ago. 2026.
- WANG, Xingyao; LI, Boxuan; SONG, Yufan; XU, Frank F.; TANG, Xiangru; ZHUGE, Mingchen et al. *OpenHands: An Open Platform for AI Software Developers as Generalist Agents*. In: ICLR, 2025. Disponível em: https://arxiv.org/abs/2407.16741. Acesso em: 03 ago. 2026.
- JIMENEZ, Carlos E.; YANG, John; WETTIG, Alexander; YAO, Shunyu; PEI, Kexin; PRESS, Ofir; NARASIMHAN, Karthik. *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?*. In: ICLR, 2024. Disponível em: https://arxiv.org/abs/2310.06770. Acesso em: 03 ago. 2026.
- HASAN, Mohammed Mehedi; LI, Hao; FALLAHZADEH, Emad; RAJBAHADUR, Gopi Krishnan; ADAMS, Bram; HASSAN, Ahmed E. *Model Context Protocol (MCP) at First Glance: Studying the Security and Maintainability of MCP Servers*. arXiv, 2026. Disponível em: https://arxiv.org/abs/2506.13538. Acesso em: 03 ago. 2026.
- HOU, Xinyi; ZHAO, Yanjie; WANG, Shenao; WANG, Haoyu. *Model Context Protocol (MCP): Landscape, Security Threats, and Future Research Directions*. arXiv, 2025. Disponível em: https://arxiv.org/abs/2503.23278. Acesso em: 03 ago. 2026.
- CIM, Musa; TOPCU, Burak; DAS, Chita; KANDEMIR, Mahmut Taylan. *Parallel Context Compaction for Long-Horizon LLM Agent Serving*. arXiv, 2026. Disponível em: https://arxiv.org/abs/2605.23296. Acesso em: 03 ago. 2026.
- KANG, Minki; CHEN, Wei-Ning; HAN, Dongge; INAN, Huseyin A.; WUTSCHITZ, Lukas; CHEN, Yanzhi; SIM, Robert; RAJMOHAN, Saravan. *ACON: Optimizing Context Compression for Long-horizon LLM Agents*. In: ICML, 2026. Disponível em: https://arxiv.org/abs/2510.00615. Acesso em: 03 ago. 2026.
- SIDIK, Bronislav; ROKACH, Lior. *Beyond Static Sandboxing: Learned Capability Governance for Autonomous AI Agents*. In: NeurIPS Agent Safety Workshop, 2026. Disponível em: https://arxiv.org/abs/2604.11839. Acesso em: 03 ago. 2026.
- BAI, Longju; HUANG, Zhemin; WANG, Xingyao; SUN, Jiao; MIHALCEA, Rada; BRYNJOLFSSON, Erik; PENTLAND, Alex; PEI, Jiaxin. *How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding Tasks*. arXiv, 2026. Disponível em: https://arxiv.org/abs/2604.22750. Acesso em: 03 ago. 2026.

## Estado da arte / ferramentas de referência

- **OpenCode (opencode.ai)**: agente de codificação open-source para terminal; 75+ provedores via AI SDK + Models.dev; TUI, desktop e extensões de IDE; servidor headless com OpenAPI 3.1. [1]
- **Claude Code (Anthropic)**: concorrente proprietário, TUI exclusiva, modelos Claude; referência de mercado para agentes de terminal. [19]
- **Cursor**: editor baseado em VS Code com IA integrada; concorrente no modelo IDE. [20]
- **Aider**: CLI open-source de pair programming com IA, orientado a Git (commits automáticos). [21]
- **Gemini CLI (Google)**: agente de codificação open-source no terminal, concorrente direto. [22]
- **OpenHands (ex-OpenDevin)**: plataforma open-source de agentes de software generalistas; base acadêmica (ICLR 2025). [23]
- **SWE-agent**: framework de agente de engenharia de software da Princeton (NeurIPS 2024); popularizou o conceito de ACI (Agent-Computer Interface). [24]
- **MCP (Model Context Protocol)**: padrão aberto da Anthropic (nov. 2024) para conexão de ferramentas/contexto; adotado por OpenCode, Claude Code, Cursor e outros. [25]
- **Models.dev**: catálogo de modelos LLM e provedores usado pelo OpenCode para listar modelos e metadados. [4]
- **OpenCode Zen / OpenCode Go**: modelos oficiais testados pela equipe; Zen = lista curada; Go = plano de baixo custo com modelos de codificação abertos. [16]
- **Atomic Chat**: app desktop que roda LLMs locais atrás de API compatível com OpenAI (padrão http://127.0.0.1:1337/v1); integração zero-setup com OpenCode. [17]
- **GitHub Agent (opencode github)**: agente para automação de repositórios via GitHub Actions (`opencode github install` / `run`). [13]
- **ACP (Agent Client Protocol)**: `opencode acp` inicia servidor compatível com o protocolo ACP via stdin/stdout em ND-JSON. [13]

## Casos de uso corporativos

- **Automação de repositórios via GitHub Actions**: `opencode github install` configura workflow; `opencode github run` executa o agente no CI — automação de issues/PRs em repositórios corporativos. [13]
- **Review de código em massa**: criar um agente custom `code-reviewer` (mode: subagent, edit deny) e usá-lo com `@code-reviewer` ou via ferramenta Task; invocação de subagentes por primary agents mantém o contexto principal limpo. [8]
- **Servidor headless compartilhado no time**: `opencode serve`/`opencode web` com `OPENCODE_SERVER_PASSWORD` permite vários devs se conectarem por `opencode attach <url>`; mDNS (`--mdns`) descobre servidores na rede (`opencode.local`). [18]
- **Padrões organizacionais via remote config**: `.well-known/opencode` entrega defaults (ex.: MCP servers da empresa desabilitados por padrão) e o time ativa localmente com `enabled: true`. [5]
- **Governança de compliance (MDM)**: managed config em `/Library/Application Support/opencode/` (macOS), `/etc/opencode/` (Linux) ou `%ProgramData%\opencode` (Windows) impõe regras que o usuário não pode sobrescrever; macOS via `.mobileconfig` (Jamf, Kandji, FleetDM). [5]
- **Plano Build/Plan no fluxo de desenvolvimento**: usar Plan mode (Tab) para propor implementação sem alterar código e Build mode para executar — padrão recomendado pela própria documentação para features. [2]
- **Compartilhamento de sessões para colaboração**: `/share` gera link público para pedir ajuda ou mostrar progresso; `share: "disabled"` para projetos sensíveis (commitado no repo). [12]
- **MCP empresariais**: Sentry (issues/erros), Context7 (busca em docs), Grep by Vercel (busca de código no GitHub) como ferramentas acopladas ao agente. [7]
- **Gerenciamento de custo**: `opencode stats --days 30 --models --project` para rastrear consumo por modelo/projeto; `maxSteps`/`steps` em agentes para limitar iterações agenticas e controlar custo. [13][8]
- **Telemetria e observabilidade via plugins**: `opencode-helicone-session`, `opencode-wakatime` no registry de plugins; hooks `session.idle`, `tool.execute.after` para notificação e métricas. [11]

## Limitações e controvérsias

- **Contexto limitado**: MCP servers e ferramentas adicionam tokens ao contexto; servidores como o GitHub MCP tendem a estourar o limite — recomendação oficial: usar com parcimônia e desabilitar por agente. [7]
- **Plugins de assinatura Claude Pro/Max banidos**: versões antigas do OpenCode traziam plugins que usavam assinatura Claude Pro/Max; a partir da v1.3.0 isso foi removido porque a Anthropic proíbe explicitamente; o bypass é considerado uso contra os termos. [16]
- **Segurança de credenciais**: chaves em `~/.local/share/opencode/auth.json` (texto); `auth.json` e MCP OAuth (`mcp-auth.json`) devem ser protegidos; `read` de arquivos `.env` é negado por padrão. [9][4]
- **Exposição acidental no share**: conversas compartilhadas são públicas a qualquer pessoa com o link; incluem histórico completo, mensagens e metadados; retenção indefinida até `/unshare`. Recomendações oficiais de privacidade. [12]
- **Riscos de agentes autônomos**: `--auto` aprova tudo que não for explicitamente negado (documentação marca como "dangerous!"); permissão `doom_loop` (mesma tool 3x idêntica) e `external_directory` (fora do worktree) pedem confirmação por padrão. [9]
- **MCP sob ataque**: papers acadêmicos documentam riscos de segurança e manutenibilidade dos servidores MCP (injeção de prompt, dados sensíveis, cadeia de suprimentos). [25][26]
- **Custo de tokens em tarefas agenticas**: consumo de tokens em coding agents é difícil de prever; papers estudam como agentes gastam dinheiro e como comprimir contexto de longa duração. [27][28]
- **Formatters desabilitados por padrão**: formatação automática exige `formatter: true` no config — recurso de qualidade de código "escondido". [29]
- **Truecolor**: temas completos exigem terminal com suporte a 24-bit color (`COLORTERM=truecolor`); sem isso, cores degradam para 256. [30]
- **Windows nativo vs WSL**: docs recomendam WSL no Windows para melhor performance/compatibilidade; suporte a Bun em Windows ainda em progresso. [1]

## Fontes brutas (para Nó 7 — Auditor de Rastreabilidade)

- ANOMALYCO. *OpenCode — AI coding agent built for the terminal*. Disponível em: https://opencode.ai. Acesso em: 03 ago. 2026.
- ANOMALYCO. *OpenCode — repositório oficial (antigo sst/opencode)*. Disponível em: https://github.com/anomalyco/opencode. Acesso em: 03 ago. 2026.
- OPENCODE. *Intro — Get started with OpenCode*. Disponível em: https://opencode.ai/docs. Acesso em: 03 ago. 2026.
- OPENCODE. *Config — Using the OpenCode JSON config*. Disponível em: https://opencode.ai/docs/config. Acesso em: 03 ago. 2026.
- OPENCODE. *TUI config — tui.json*. Disponível em: https://opencode.ai/tui.json. Acesso em: 03 ago. 2026.
- OPENCODE. *Config schema — opencode.ai/config.json*. Disponível em: https://opencode.ai/config.json. Acesso em: 03 ago. 2026.
- OPENCODE. *Agents — Configure and use specialized agents*. Disponível em: https://opencode.ai/docs/agents. Acesso em: 03 ago. 2026.
- OPENCODE. *Permissions — Control which actions require approval to run*. Disponível em: https://opencode.ai/docs/permissions. Acesso em: 03 ago. 2026.
- OPENCODE. *Tools — Manage the tools an LLM can use*. Disponível em: https://opencode.ai/docs/tools. Acesso em: 03 ago. 2026.
- OPENCODE. *MCP servers — Add local and remote MCP tools*. Disponível em: https://opencode.ai/docs/mcp-servers. Acesso em: 03 ago. 2026.
- OPENCODE. *Providers — Using any LLM provider in OpenCode*. Disponível em: https://opencode.ai/docs/providers. Acesso em: 03 ago. 2026.
- OPENCODE. *Server — Interact with opencode server over HTTP*. Disponível em: https://opencode.ai/docs/server. Acesso em: 03 ago. 2026.
- OPENCODE. *CLI — OpenCode CLI options and commands*. Disponível em: https://opencode.ai/docs/cli. Acesso em: 03 ago. 2026.
- OPENCODE. *Commands — Create custom commands for repetitive tasks*. Disponível em: https://opencode.ai/docs/commands. Acesso em: 03 ago. 2026.
- OPENCODE. *Plugins — Write your own plugins to extend OpenCode*. Disponível em: https://opencode.ai/docs/plugins. Acesso em: 03 ago. 2026.
- OPENCODE. *Share — Share your OpenCode conversations*. Disponível em: https://opencode.ai/docs/share. Acesso em: 03 ago. 2026.
- OPENCODE. *Keybinds — Customize your keybinds*. Disponível em: https://opencode.ai/docs/keybinds. Acesso em: 03 ago. 2026.
- OPENCODE. *Themes — Select a built-in theme or define your own*. Disponível em: https://opencode.ai/docs/themes. Acesso em: 03 ago. 2026.
- OPENCODE. *Agent Skills — Define reusable behavior via SKILL.md definitions*. Disponível em: https://opencode.ai/docs/skills. Acesso em: 03 ago. 2026.
- OPENCODE. *Formatters — OpenCode uses language specific formatters*. Disponível em: https://opencode.ai/docs/formatters. Acesso em: 03 ago. 2026.
- OPENCODE. *OpenCode Zen — curated models*. Disponível em: https://opencode.ai/docs/providers. Acesso em: 03 ago. 2026.
- OPENCODE. *OpenCode Go — low cost subscription plan*. Disponível em: https://opencode.ai/docs/providers. Acesso em: 03 ago. 2026.
- OPENCODE. *OpenCode ecosystem — plugins*. Disponível em: https://opencode.ai/docs/plugins. Acesso em: 03 ago. 2026.
- ANTHROPIC. *Introducing the Model Context Protocol*. Disponível em: https://www.anthropic.com/news/model-context-protocol. Acesso em: 03 ago. 2026.
- ANTHROPIC. *Claude Code documentation*. Disponível em: https://docs.anthropic.com/en/docs/claude-code. Acesso em: 03 ago. 2026.
- CURSOR. *Cursor — The AI Code Editor*. Disponível em: https://www.cursor.com. Acesso em: 03 ago. 2026.
- AIDER. *Aider — AI pair programming in your terminal*. Disponível em: https://aider.chat. Acesso em: 03 ago. 2026.
- GOOGLE. *Gemini CLI*. Disponível em: https://github.com/google-gemini/gemini-cli. Acesso em: 03 ago. 2026.
- OPENHANDS. *OpenHands — An Open Platform for AI Software Developers*. Disponível em: https://github.com/All-Hands-AI/OpenHands. Acesso em: 03 ago. 2026.
- PRINCETON UNIVERSITY. *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering*. Disponível em: https://arxiv.org/abs/2405.15793. Acesso em: 03 ago. 2026.
- PRINCETON UNIVERSITY. *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?*. Disponível em: https://arxiv.org/abs/2310.06770. Acesso em: 03 ago. 2026.
- MODELS.DEV. *Models.dev — open model catalog*. Disponível em: https://models.dev. Acesso em: 03 ago. 2026.
- SENTRY. *Sentry MCP server*. Disponível em: https://mcp.sentry.dev/mcp. Acesso em: 03 ago. 2026.
- CONTEXT7. *Context7 — docs on demand for AI*. Disponível em: https://context7.com. Acesso em: 03 ago. 2026.
- VERGEL (VERCEL). *Grep by Vercel*. Disponível em: https://mcp.grep.app. Acesso em: 03 ago. 2026.
- EXA. *Exa AI — web search API*. Disponível em: https://exa.ai. Acesso em: 03 ago. 2026.
- SST. *SST — framework para aplicações serverless*. Disponível em: https://sst.dev. Acesso em: 03 ago. 2026.
- OLLAMA. *Ollama — run LLMs locally*. Disponível em: https://ollama.com. Acesso em: 03 ago. 2026.
- LM STUDIO. *LM Studio — run local LLMs*. Disponível em: https://lmstudio.ai. Acesso em: 03 ago. 2026.
- VLLM. *vLLM — fast LLM inference*. Disponível em: https://docs.vllm.ai. Acesso em: 03 ago. 2026.
- NIXOS/NIXPKGS. *Homebrew — opencode formula (anomalyco/tap)*. Disponível em: https://formulae.brew.sh. Acesso em: 03 ago. 2026.
- OSSINSIGHT. *Open source analytics for opencode*. Disponível em: https://ossinsight.io. Acesso em: 03 ago. 2026.
- GITHUB. *GitHub Actions documentation*. Disponível em: https://docs.github.com/actions. Acesso em: 03 ago. 2026.
