// Traduz .mcp.json (schema "mcpServers" command+args, usado por Claude Code/Cursor/Windsurf)
// para opencode.json (schema "mcp" type:"local" command:[...] do OpenCode). Os dois schemas
// diferem, entao nao pode ser link/junction — precisa gerar. Preserva chaves manuais do
// opencode.json (instructions, permission, agent, etc.) via merge (o bloco mcp e sobrescrito).
//
// Rode de novo sempre que .mcp.json mudar: node scripts/sync-opencode-mcp.mjs
// (tambem invocado por scripts/setup-links.ps1/.sh)

import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const raizProjeto = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const origem = path.join(raizProjeto, ".mcp.json");
const destino = path.join(raizProjeto, "opencode.json");

const mcpJson = JSON.parse(await readFile(origem, "utf-8"));

const mcp = {};
for (const [nome, def] of Object.entries(mcpJson.mcpServers)) {
  if (def.url) {
    mcp[nome] = { type: "remote", url: def.url, enabled: true };
  } else {
    mcp[nome] = {
      type: "local",
      command: [def.command, ...(def.args || [])],
      ...(def.cwd ? { cwd: def.cwd } : {}),
      enabled: true,
    };
  }
}

let anterior = {};
try {
  anterior = JSON.parse(await readFile(destino, "utf-8"));
} catch {
  /* ainda nao existe */
}

const gerado = {
  $schema: anterior.$schema ?? "https://opencode.ai/config.json",
  instructions: anterior.instructions ?? ["AGENTS.md"],
  mcp,
  permission: anterior.permission ?? {
    edit: "allow",
    bash: "allow",
    read: "allow",
    glob: "allow",
    grep: "allow",
    list: "allow",
    webfetch: "allow",
    websearch: "allow",
    task: "allow",
    skill: "allow",
  },
  ...anterior,
  mcp, // bloco mcp sempre sobrescrito pela fonte .mcp.json
};

await writeFile(destino, JSON.stringify(gerado, null, 2) + "\n", "utf-8");
console.log(`Gerado: ${destino} (${Object.keys(mcp).length} servidores MCP traduzidos de .mcp.json)`);
