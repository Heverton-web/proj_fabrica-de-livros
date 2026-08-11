import type { Plugin } from "@opencode-ai/plugin"

/**
 * Replica os hooks do .claude/settings.json para o OpenCode:
 *  - PostToolUse (Edit|Write)  -> code-review-graph update + atualizar-documentacao
 *  - SessionStart              -> code-review-graph status
 *
 * Fonte canônica: .claude/settings.json (Claude Code). Mantenha os dois em sincronia.
 */
export const FabricaHooks: Plugin = async ({ $, worktree }) => {
  const isGit = async (): Promise<boolean> => {
    try {
      const out = await $`git rev-parse --git-dir`.nothrow().quiet()
      return out.exitCode === 0
    } catch {
      return false
    }
  }

  const updateGraph = async () => {
    if (!(await isGit())) return
    try {
      await $`code-review-graph update --skip-flows --repo ${worktree}`.nothrow().quiet()
    } catch {
      /* silencioso */
    }
  }

  const updateDocs = async () => {
    if (!(await isGit())) return
    try {
      const out = await $`git diff --name-only`.nothrow().quiet()
      const changed = out.stdout.toString()
      if (/docs\/(manual-completo-fabrica|guia-execucao-maquina-vendas)\.md|templates\/template\.typ/.test(changed)) {
        await $`python scripts/atualizar-documentacao.py --se-sujo --silencioso`.nothrow().quiet()
      }
    } catch {
      /* silencioso */
    }
  }

  const graphStatus = async () => {
    if (!(await isGit())) return
    try {
      await $`code-review-graph status --repo ${worktree}`.nothrow().quiet()
    } catch {
      /* silencioso */
    }
  }

  return {
    "tool.execute.after": async (input) => {
      if (input.tool === "edit" || input.tool === "write") {
        await Promise.all([updateGraph(), updateDocs()])
      }
    },
    event: async ({ event }) => {
      if (event.type === "session.created") {
        await graphStatus()
      }
    },
  }
}
