# Dossiê de Pesquisa — MiMoCode: Referência Técnica (configurações avançadas)

## 1. CLI (`mimo`) — comandos e flags

Base: help oficial do CLI (fornecido pelo autor) cruzado com a documentação [1][2][5].

- `mimo` → inicia a TUI interativa (default).
- `mimo run [message..]` → execução headless com uma mensagem.
- `mimo serve` → servidor headless (HTTP/WebSocket); `mimo attach <url>` conecta uma TUI.
- `mimo mcp` → gerencia servidores MCP; `mimo acp` → protocolo ACP.
- `mimo providers` (alias `auth`) → gerencia provedores e credenciais.
- `mimo agent` → gerencia agentes; `mimo session` → gerencia sessões.
- `mimo export [sessionID]` / `mimo import <file>` → exporta/importa dados de sessão (JSON).
- `mimo stats` → uso de tokens e custo; `mimo models [provider]` → lista modelos.
- `mimo github` / `mimo pr <number>` → integração GitHub (fetch PR e roda).
- `mimo plugin <module>` (alias `plug`) → instala plugins e atualiza config.
- `mimo db` → ferramentas de banco local (SQLite FTS5).
- `mimo upgrade [target]` / `mimo uninstall` / `mimo completion`.
- Flags globais: `-m/--model provider/model`, `-c/--continue`, `-s/--session`,
  `--fork`, `--prompt`, `--agent`, `--never-ask`, `--trust`,
  `--dangerously-skip-permissions`, `--print-logs`, `--log-level`,
  `--pure` (sem plugins externos), `--port`, `--hostname`, `--mdns`,
  `--mdns-domain`, `--cors`, `--no-auth`.

## 2. Arquivos de configuração

- **Projeto**: `.mimocode/mimocode.jsonc` (ou `.json`)
- **Global**: `~/.config/mimocode/mimocode.jsonc` (ou `.json`)
- **Prefs da TUI**: `.mimocode/tui.json` / `~/.config/mimocode/tui.json`
- **Credenciais**: `~/.local/share/mimocode/auth.json` (Windows: `%LOCALAPPDATA%\mimocode\`,
  sobrescrevível via `MIMOCODE_HOME`).
- Schema JSON: `https://mimo.xiaomi.com/mimocode/config.json`
- Estrutura principal:
  ```json
  {
    "$schema": "https://mimo.xiaomi.com/mimocode/config.json",
    "model": "openai/gpt-4o",
    "provider": {
      "custom": {
        "name": "Custom",
        "npm": "@ai-sdk/openai-compatible",
        "only_configured_models": true,
        "models": { "MODEL_ID": { "name": "MODEL_ID" } },
        "options": { "baseURL": "https://api.example.com/v1", "apiKey": "sk-..." }
      }
    },
    "compaction": { "max_context": { "openai/gpt-4o": "300K" } },
    "permission": { "external_directory": { "/tmp/**": "allow" } }
  }
  ```

## 3. Providers e modelos

- **MiMo Auto**: canal anônimo gratuito (por tempo limitado), zero configuração.
- **Plataforma MiMo (Xiaomi)**: OAuth, modelos MiMo proprietários, multimodal.
- **Codex (ChatGPT Pro/Plus)**: OAuth OpenAI.
- **Catálogo**: Anthropic, OpenAI, OpenRouter, xAI/Grok, **Ollama** local/remoto.
- **`small_model`**: modelo secundário p/ tarefas de fundo, checkpoints e subagentes heurísticos.
- **Custom OpenAI-compatible**: `provider.custom` com `baseURL` e `apiKey`.
- IDs com `/` são suportados (primeira `/` separa provider de modelo).

## 4. Permissões e segurança

- Padrão: nega edições/execução fora do workspace, pedindo aprovação.
- `--dangerously-skip-permissions`: pula todas as confirmações (CI/sandbox confiável),
  com aviso de segurança.
- Regras avaliadas em sequência; a **última** regra correspondente prevalece.
- Regras `deny` sempre sobrepõem `allow`; operações sem regra caem em `ask`.

## 5. MCP e ACP

- **MCP**: integra ferramentas/dados externos via JSON-RPC; gerido por `mimo mcp` ou config.
- **ACP**: controle agêntico — delegação entre agentes e orquestração remota.

## 6. Agents e AGENTS.md

- Três modos principais (alternar `Tab`): `build`, `plan`, `compose`.
- `AGENTS.md` por projeto define instruções; agentes primários spawnam subagentes em
  background (tarefas paralelas, git worktrees, loops de verificação).
- Modo `compose` trava o conjunto de ferramentas para execução multi-passos confiável.

## 7. Dicas avançadas

- **Sessões**: continuar (`-c`), retomar por id (`-s`), **fork** (`--fork`).
- **Share**: exportar/importar sessões (`mimo export` / `mimo import`).
- **Auto-compactação**: `/context-limit` ou `compaction.max_context` p/ forçar
  compactação antes do limite nativo (menos latência/custo).
- **Git worktrees**: o workflow `compose` isola tarefas em worktrees com TDD antes do merge.
- **`/dream`** → extrai conhecimento persistente para `MEMORY.md`;
  **`/distill`** → converte fluxos manuais repetidos em skills/subagentes reutilizáveis.
