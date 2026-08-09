# Dossiê de Pesquisa — Livro 5 "A Pilha Agêntica"

**Obra:** *CLAUDE.md, AGENTS.md e Rules: a engenharia da memória e das regras do projeto*
**Slug:** `livros/claude-md-agents-md-e-rules-engenharia-da-memoria-e-das-regras-do-projeto`
**Data:** 5 de agosto de 2026

---

## 1. Fontes Autoritativas (22)

1. **ANTHROPIC.** *Memory: how Claude remembers your project*. Claude Code Documentation, 2025–2026. Disponível em: https://docs.anthropic.com/en/docs/claude-code/memory. Acesso em: 5 ago. 2026.
2. **ANTHROPIC.** *Overview: Claude Code*. Claude Code Documentation, 2025–2026. Disponível em: https://docs.anthropic.com/en/docs/claude-code/overview. Acesso em: 5 ago. 2026.
3. **AGENTS.MD.** *AGENTS.md: the standard for AI agent instructions*. Agentic AI Foundation / OpenAI, ago. 2025. Disponível em: https://agents.md/. Acesso em: 5 ago. 2026.
4. **LINUX FOUNDATION.** *Linux Foundation announces the formation of the Agentic AI Foundation*. Linux Foundation Press Release, 9 dez. 2025. Disponível em: https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation. Acesso em: 5 ago. 2026.
5. **AGENTIC AI FOUNDATION.** *Agentic AI Foundation official portal*. AAIF, 2025–2026. Disponível em: https://aaif.io/. Acesso em: 5 ago. 2026.
6. **OSMANI, Addy.** *15 AGENTS.md — engineering guide to AGENTS.md*. Addy Osmani, 2025–2026. Disponível em: https://addyosmani.com/agents/15-agents-md/. Acesso em: 5 ago. 2026.
7. **AUGMENT CODE.** *How to build AGENTS.md: construction guide*. Augment Code Guides, 2025–2026. Disponível em: https://www.augmentcode.com/guides/how-to-build-agents-md. Acesso em: 5 ago. 2026.
8. **CURSOR.** *Rules: Cursor Documentation*. Cursor / Anysphere, 2025–2026. Disponível em: https://cursor.com/docs/rules. Acesso em: 5 ago. 2026.
9. **AGYN.** *AGENTS.md vs CLAUDE.md: does Claude Code or Codex read both?*. Agyn Blog, jun. 2026. Disponível em: https://agyn.io/blog/claude-md-agents-md-compatibility. Acesso em: 5 ago. 2026.
10. **OPENAI.** *Codex: AGENTS.md and coding agents*. OpenAI Documentation, 2025–2026. Disponível em: https://openai.com/index/introducing-codex/. Acesso em: 5 ago. 2026.
11. **GITHUB.** *GitHub Copilot: repository instructions and AGENTS.md support*. GitHub Documentation, 2025–2026. Disponível em: https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions. Acesso em: 5 ago. 2026.
12. **GITHUB.** *GitHub Copilot Coding Agent: reading repository instructions*. GitHub Changelog, 2025–2026. Disponível em: https://github.blog/. Acesso em: 5 ago. 2026.
13. **ANTHROPIC.** *Writing tools for AI agents — using AI agents*. Anthropic Engineering Blog, set. 2025. Disponível em: https://www.anthropic.com/engineering/writing-tools-for-agents. Acesso em: 5 ago. 2026.
14. **ANTHROPIC.** *Effective context engineering for AI agents*. Anthropic Engineering Blog, set. 2025. Disponível em: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents. Acesso em: 5 ago. 2026.
15. **ANTHROPIC.** *Introducing the Model Context Protocol*. Anthropic News, 25 nov. 2024. Disponível em: https://www.anthropic.com/news/model-context-protocol. Acesso em: 5 ago. 2026.
16. **MODEL CONTEXT PROTOCOL.** *Architecture*. MCP Specification 2025-11-25, 25 nov. 2025. Disponível em: https://modelcontextprotocol.io/specification/2025-11-25/architecture. Acesso em: 5 ago. 2026.
17. **LINUX FOUNDATION.** *Agentic AI Foundation: governance of foundational agentic infrastructure*. Linux Foundation Blog, dez. 2025. Disponível em: https://www.linuxfoundation.org/blog/. Acesso em: 5 ago. 2026.
18. **CURSOR.** *Best practices for rules and context*. Cursor Documentation, 2025–2026. Disponível em: https://cursor.com/docs/context/rules. Acesso em: 5 ago. 2026.
19. **AIDER.** *AGENTS.md support and multi-tool interoperability*. Aider Documentation, 2025–2026. Disponível em: https://aider.chat/docs/repomap.html. Acesso em: 5 ago. 2026.
20. **ANTHROPIC.** *Claude Code best practices: memory and configuration*. Anthropic Engineering Blog, 2025–2026. Disponível em: https://www.anthropic.com/engineering/claude-code-best-practices. Acesso em: 5 ago. 2026.
21. **CODEQL / GITHUB.** *Reproducible rules and configuration as code*. GitHub Blog, 2025–2026. Disponível em: https://github.blog/. Acesso em: 5 ago. 2026.
22. **MODEL CONTEXT PROTOCOL.** *Registry Repository*. GitHub Repository, 2025–2026. Disponível em: https://github.com/modelcontextprotocol/registry. Acesso em: 5 ago. 2026.

## 2. Síntese dos Eixos Temáticos

### Eixo 1 — CLAUDE.md como contrato comportamental (Anthropic, 2025–2026)
O CLAUDE.md não é documentação para humanos (como o README.md) — é um **contrato comportamental** escrito para o agente:
- **O que colocar:** comandos críticos (`npm test`, lint, build, format), mapa de arquitetura e diretórios-chave, regras duras/negativas ("nunca commitar `.env`", "sem class components"), preferências de workflow e limites explícitos de escopo.
- **O que nunca colocar:** segredos, tokens ou connection strings (aparecem no contexto e nos logs); regras já enforced por linter (Prettier/ESLint); aspirações vagas ou personalidade genérica ("seja um engenheiro sênior").
- **Tamanho ideal:** menos de 200 linhas por arquivo (recomendação da Anthropic para evitar context bloat e garantir adesão); marcadores `IMPORTANT` e `YOU MUST` melhoram a adesão mensurada.
- **Sintaxe:** `@path/to/import` importa arquivos externos (expandidos no launch, recursão até 4 hops); literais com backticks (`` `@README` ``); diretórios hierárquicos concatenados da raiz ao diretório de trabalho.

### Eixo 2 — MEMORY.md e memória automática entre sessões
- **Subsistema auto-memória:** habilitado por padrão (Claude Code v2.1.59+), grava aprendizados sob `~/.claude/projects/<projeto>/memory/`.
- **Estrutura:** `MEMORY.md` como índice mestre (carregado até 200 linhas / 25 KB por sessão); arquivos tópico-específicos (ex.: `debugging.md`, `api-conventions.md`) lidos sob demanda via file tools.
- **Consolidação (Dreams pipeline):** automação em períodos ociosos que mescla duplicatas, substitui entradas obsoletas/contraditórias pelos valores recentes e descobre novos insights dos transcripts de sessão.
- **Subagentes:** memória automática localizada para tarefas isoladas, sem contaminar o thread principal.

### Eixo 3 — AGENTS.md como padrão neutro (Agentic AI Foundation)
- **Origem:** lançado pela OpenAI em agosto de 2025 como formato aberto; desenvolvido com Amp, Google (Jules), Cursor, Factory e Aider para eliminar arquivos de configuração fragmentados (`.cursorrules`, `CLAUDE.md`, `copilot-instructions.md`).
- **Definição:** "README para agentes" — Markdown puro, sem schema proprietário, parseável por qualquer agente LLM.
- **Conteúdo estrutural:** comandos exatos e completos (com flags), instruções de teste, estrutura do projeto, estilo de código e padrões não-óbvios, fronteiras e guardrails com tier de permissão (✅ Always · ⚠️ Ask First · 🚫 Never).
- **Monorepos:** arquivos aninhados; o agente parseia o mais próximo (precedência por proximidade).
- **Governança:** em 9 dez. 2025, a Linux Foundation anunciou a **Agentic AI Foundation (AAIF)** como casa neutra do AGENTS.md, do MCP (Anthropic) e do goose (Block); membros platinum incluem AWS, Anthropic, Bloomberg, Cloudflare, Google, Microsoft e OpenAI.

### Eixo 4 — .cursorrules e .cursor/rules/ (Cursor)
- **Arquitetura modular:** arquivos `.mdc` (Markdown com frontmatter) em `.cursor/rules/` substituem/complementam o `.cursorrules` legado.
- **Modos de ativação:** `alwaysApply: true` (sempre aplicado); `alwaysApply: false` + `globs` (auto-attached por glob); `alwaysApply: false` + `description` (agent-selected inteligente); manual via `@-mention`.
- **Globs:** padrões `*`, `**`, `src/**/*.tsx`, `tailwind.config.*` para escopo por arquivo/diretório/linguagem.
- **Precedência:** Team Rules (Cloud) → Project Rules (`.cursor/rules/` e `AGENTS.md`) → User Rules (Global).

### Eixo 5 — Hierarquia e cascata em monorepos
- **Precedência por proximidade:** o arquivo mais próximo do diretório de trabalho vence (AGENTS.md aninhado, CLAUDE.md hierárquico concatenado da raiz).
- **Padrão de ponte recomendado:** `AGENTS.md` como fonte canônica neutra (Cursor, OpenCode, Continue) + `CLAUDE.md` importando via `@AGENTS.md` com overrides específicos do Claude Code.
- **Conflitos:** Claude Code lê `CLAUDE.md` e não faz fallback automático para `AGENTS.md`; a ponte explícita resolve a duplicação.

### Eixo 6 — Drift entre documentação e prática
- **Rule drift:** os padrões do código evoluem, as regras estáticas envelhecem — agentes propõem padrões legados.
- **Mitigação:** regras curtas e composáveis (< 500 linhas); **referenciar arquivos em vez de snippets** (`@filename.ts` aponta para implementações canônicas — o drift desaparece porque a referência fica fresca); atualização automatizada via CI/PR (tagging `@cursor` em PRs); verificação de carregamento de contexto (pedir ao agente que cite restrições no início da sessão).

## 3. Métricas de mercado (2026)
- Anthropic recomenda **< 200 linhas por CLAUDE.md** e carrega **até 200 linhas / 25 KB** do MEMORY.md por sessão.
- A **Agentic AI Foundation** (9 dez. 2025) reúne AGENTS.md, MCP e goose sob a Linux Foundation, com AWS, Anthropic, Bloomberg, Cloudflare, Google, Microsoft e OpenAI como membros platinum.
- A integração do AGENTS.md é suportada por Claude Code, Cursor, Codex, GitHub Copilot, Aider, Google Jules, Gemini CLI, Zed, Warp, Factory, Goose, Windsurf e Augment Code.
