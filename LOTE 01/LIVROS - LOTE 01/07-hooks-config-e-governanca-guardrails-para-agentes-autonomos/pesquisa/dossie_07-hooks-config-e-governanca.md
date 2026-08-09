# Dossiê Técnico — Hooks, Config e Governança: Guardrails para Agentes Autônomos

**Obra:** Livro 7 · Parte III — A Camada de Harness
**Slug:** livros/07-hooks-config-e-governanca-guardrails-para-agentes-autonomos
**Tamanho:** G (5 Partes, 10 capítulos) · **Refs mínimas por capítulo:** 20

## 1. Síntese do tema

O Livro 6 fechou a camada de empacotamento de conhecimento (skills e commands). O Livro 7
avança para a camada de **controle determinístico**: hooks, configuração e governança como
guardrails de segurança para agentes autônomos. A tese central: instruções em linguagem
natural (CLAUDE.md, rules) dependem da probabilidade do modelo obedecer; hooks e permissões
executam **no harness**, de forma determinística e inegociável, independentemente do que o
modelo "decida". É a diferença entre pedir e impor.

### 1.1 Conceitos fundamentais

- **Hook:** ponto de interceptação programática no ciclo de vida do agente (antes/depois de
  ferramentas, entrada de prompt, início/fim de sessão, subagentes). Executa comandos shell,
  endpoints HTTP, prompts LLM ou subagentes, com contrato de saída em JSON + exit codes.
- **Exit code 2:** código de bloqueio imediato — interrompe a ação e devolve o stderr ao
  modelo como motivo do bloqueio (loop de auto-correção forçada).
- **Matchers:** filtros de disparo por nome de ferramenta (case-sensitive, regex), caminho de
  arquivo, regex de comando ou hook-source.
- **hookSpecificOutput:** saída JSON refinada do PreToolUse com `permissionDecision`
  (allow/deny/ask), `updatedInput` (reescrita de argumentos) e `additionalContext`
  (injeção de contexto).
- **Scopes de settings.json:** managed (empresa) > CLI args > local > projeto > usuário.
- **Camada de permissões:** avaliação estrita Deny → Ask → Allow; deny nu remove a ferramenta
  do contexto do modelo; deny por escopo bloqueia apenas o comando correspondente.
- **Modos de permissão:** default, acceptEdits, plan, auto, dontAsk, bypassPermissions.
- **Governança enterprise:** managed policy (MDM, servidor, arquivos de sistema),
  `allowManagedPermissionRulesOnly`, `permissions.disableBypassPermissionsMode`,
  sandbox OS-level, SSO/SCIM, audit logs (180 dias) e Compliance API para SIEM.
- **Modelo de ameaças agentic:** indirect prompt injection, tool poisoning, data exfiltration
  via ferramentas, privilege/identity abuse, rogue agents, cascading failures.
- **Princípio de Least Agency:** evolução do least privilege — o agente começa com o menor
  grau de autonomia e ganha agência conforme demonstra confiabilidade.
- **OWASP Top 10 for Agentic Applications (2026):** ASI01 Goal Hijack, ASI02 Tool Misuse,
  ASI08 Cascading Failures, ASI10 Rogue Agents.
- **MITRE ATLAS:** táticas/técnicas adversárias contra sistemas de IA, com cobertura de
  plano de controle de agentes, persistência de contexto e envenenamento de toolchain.
- **Sandboxing:** Docker efêmero com egress deny-by-default, gVisor (isolamento de syscalls),
  namespaces + cgroups, sandbox OS-level do Claude Code (`sandbox.enabled`).

## 2. Fatos-chave e referências por frente de pesquisa

### Frente A — Sistema de hooks do Claude Code
- ~30 eventos de ciclo de vida: SessionStart, SessionEnd, Setup, ConfigChange, CwdChanged,
  InstructionsLoaded, UserPromptSubmit, UserPromptExpansion, PreToolUse, PermissionRequest,
  PermissionDenied, PostToolUse, PostToolUseFailure, PostToolBatch, SubagentStart,
  SubagentStop, TaskCreated, TaskCompleted, TeammateIdle, Stop, PreCompact, PostCompact.
- Tipos de handler: `command` (shell), `http` (POST JSON), `prompt` (LLM de um turno),
  `agent` (subagente com ferramentas).
- PreToolUse é o hook mais crítico para segurança: bloqueia antes de Bash/Edit/Write.
- Stop pode recusar o fim de turno (força o modelo a continuar até passar nos testes).
- SessionStart suporta matcher por source (startup, resume, clear, compact).
- Configuração em bloco `"hooks"` dentro de settings.json nos 4 escopos.

### Frente B — Configuração e permissões
- Escopo managed é absoluto: não pode ser sobrescrito por desenvolvedores.
- `additionalDirectories` habilita monorepos/pastas irmãs com controle explícito.
- `/permissions` e `/config` são os comandos de gestão interativa de regras.
- "Yes, don't ask again" grava regra permanente em `.claude/settings.local.json`
  (que é auto-adicionado ao .gitignore).
- `--allowedTools`/`--disallowedTools`/`--permission-mode` para CI headless.
- `--dangerously-skip-permissions` = bypassPermissions; alerta de disjuntor só para
  `rm -rf /` e `~`; deve ser usado apenas em ambientes isolados.
- Sandbox OS-level: `sandbox.enabled`, `sandbox.network.allowedDomains`.

### Frente C — Governança e guardrails para agentes autônomos
- Superfície de ataque dos agentes: input estático → planejamento iterativo + ferramentas.
- Human-in-the-loop com approval gates para operações destrutivas; CIBA para
  autorização assíncrona em canal externo.
- Circuit breakers/kill switches contra anomalias (volume de API, desvio de plano).
- Audit trails com cadeia de delegação (usuário → orquestrador → subagentes), logs imutáveis.
- Frameworks: OWASP Top 10 for Agentic Applications, OWASP Top 10 for LLM Applications,
  MITRE ATLAS, NIST AI RMF, ISO/IEC 42001, EU AI Act (artigos 9, 14, 15).

### Frente D — Comparativo de harnesses
- Claude Code: settings.json cascata + CLAUDE.md; Deny>Ask>Allow; hooks JSON/exit codes;
  approval interativo persistente.
- OpenCode: config.json central, plugins, allowlists/denylists, hooks programáticos.
- Cursor: `.cursor/rules/*.mdc` com glob patterns (applyTo), delegação a extensões.
- Copilot: `copilot-instructions.md`, `*.instructions.md`, AGENTS.md; guardrails na nuvem.
- Windsurf/Cascade: `.windsurfrules`, hooks.json com 12 eventos, exit code 2 bloqueia.
- Cline/Roo Code: auto-approve por categoria de risco, longest-prefix wins para
  allowedCommands/deniedCommands, dupla aprovação para MCP.

## 3. Fontes brutas

- ANTHROPIC. *Hooks Guide*. Disponível em: https://code.claude.com/docs/en/hooks-guide. Acesso em: 06 ago. 2026.
- ANTHROPIC. *Hooks Reference*. Disponível em: https://code.claude.com/docs/en/hooks. Acesso em: 06 ago. 2026.
- ANTHROPIC. *Settings Reference*. Disponível em: https://code.claude.com/docs/en/settings. Acesso em: 06 ago. 2026.
- ANTHROPIC. *Configure Permissions*. Disponível em: https://code.claude.com/docs/en/permissions. Acesso em: 06 ago. 2026.
- ANTHROPIC. *Enterprise Admin Setup*. Disponível em: https://code.claude.com/docs/en/admin-setup. Acesso em: 06 ago. 2026.
- ANTHROPIC. *Access Audit Logs*. Disponível em: https://support.claude.com/en/articles/9970975-access-audit-logs. Acesso em: 06 ago. 2026.
- OWASP. *Top 10 for LLM Applications*. Disponível em: https://genai.owasp.org/. Acesso em: 06 ago. 2026.
- OWASP. *Top 10 for Agentic Applications*. Disponível em: https://genai.owasp.org/. Acesso em: 06 ago. 2026.
- MITRE. *ATLAS — Adversarial Threat Landscape for Artificial-Intelligence Systems*. Disponível em: https://atlas.mitre.org/. Acesso em: 06 ago. 2026.
- CLOUD SECURITY ALLIANCE. *MAESTRO & Agentic Threat Research*. Disponível em: https://labs.cloudsecurityalliance.org/agentic/csa-research-note-atlas-agentic-gap-analysis-20260327/. Acesso em: 06 ago. 2026.
- CLOUD SECURITY ALLIANCE. *Security Guidance for Critical Areas of Focus in Cloud Computing*. Disponível em: https://cloudsecurityalliance.org/. Acesso em: 06 ago. 2026.
- NIST. *AI Risk Management Framework (AI RMF 1.0)*. Disponível em: https://www.nist.gov/itl/ai-risk-management-framework. Acesso em: 06 ago. 2026.
- ISO. *ISO/IEC 42001:2023 — Information technology — Artificial intelligence — Management system*. Disponível em: https://www.iso.org/standard/81230.html. Acesso em: 06 ago. 2026.
- EUROPEAN UNION. *Regulation (EU) 2024/1689 (EU AI Act)*. Disponível em: https://eur-lex.europa.eu/eli/reg/2024/1689/oj. Acesso em: 06 ago. 2026.
- CYCODE. *OWASP Top 10 for Agentic Applications 2026 Explained*. Disponível em: https://cycode.com/blog/owasp-top-10-agentic-applications/. Acesso em: 06 ago. 2026.
- AUTH0. *Lessons from OWASP Top 10 for Agentic Applications: Least Privilege to Least Agency*. Disponível em: https://auth0.com/blog/owasp-top-10-agentic-applications-lessons/. Acesso em: 06 ago. 2026.
- MODULOS. *OWASP Top 10 for Agentic Applications (2026) Governance Guide*. Disponível em: https://docs.modulos.ai/frameworks/owasp-top-10-agentic/. Acesso em: 06 ago. 2026.
- GITHUB. *Adding repository custom instructions for GitHub Copilot*. Disponível em: https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot. Acesso em: 06 ago. 2026.
- GITHUB. *AGENTS.md file for GitHub Copilot*. Disponível em: https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot. Acesso em: 06 ago. 2026.
- DEVIAN. *Windsurf Cascade Hooks*. Disponível em: https://docs.devin.ai/desktop/cascade/hooks. Acesso em: 06 ago. 2026.
- ROO CODE. *Auto-Approving Actions*. Disponível em: https://roocodeinc.github.io/Roo-Code/features/auto-approving-actions/. Acesso em: 06 ago. 2026.
- OPENCODE. *OpenCode Configuration*. Disponível em: https://opencode.ai/docs/config/. Acesso em: 06 ago. 2026.
- ANTHROPIC. *Claude Code on GitHub*. Disponível em: https://github.com/anthropics/claude-code. Acesso em: 06 ago. 2026.
- ANTHROPIC. *Model Context Protocol Documentation*. Disponível em: https://modelcontextprotocol.io/. Acesso em: 06 ago. 2026.
- GOOGLE. *gVisor — Application Kernel for Containers*. Disponível em: https://gvisor.dev/. Acesso em: 06 ago. 2026.
- DOCKER. *Docker security best practices*. Disponível em: https://docs.docker.com/engine/security/. Acesso em: 06 ago. 2026.
- OWASP. *Prompt Injection — OWASP Cheat Sheet*. Disponível em: https://cheatsheetseries.owasp.org/cheatsheets/Prompt_Injection_Cheat_Sheet.html. Acesso em: 06 ago. 2026.
- OWASP. *LLM Tool Poisoning — OWASP Top 10 for LLM Applications*. Disponível em: https://genai.owasp.org/. Acesso em: 06 ago. 2026.
- CURSOR. *Rules Documentation*. Disponível em: https://cursor.com/docs/context/rules. Acesso em: 06 ago. 2026.
- CLINE. *Cline VS Code Extension*. Disponível em: https://github.com/cline/cline. Acesso em: 06 ago. 2026.
