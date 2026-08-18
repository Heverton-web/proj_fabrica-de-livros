---
title: "Plano de Ação — Padronização de Nomenclatura de Scripts"
subtitle: "Fábrica Agêntica de Publicações · regra tipo+o-que+extensão"
author: "Fábrica Agêntica de Publicações"
date: "Agosto 2026"
lang: pt-BR
---

# 1. Sumário executivo

| Item | Resultado |
|---|---|
| **Regra alvo** | `<tipo>-<o-que>.<ext>` (kebab-case, minúsculo, sem underscore) |
| **Escopo varrido** | `scripts/` (84 arquivos), `tests/` (41), `.claude/commands` (19), `.claude/agents` (7), `.claude/skills` (34 pastas) |
| **Blast radius** | 1.228 ocorrências de `scripts/*.py` em 217 arquivos do repo |
| **Já conformes** | ~60 de 84 scripts já seguem `verbo-oque.py` |
| **Não conformes** | 6 scripts "lixo" com `_prefixo`, 8 com `underscore_em_vez_de_hifen`, 10 módulos-biblioteca noun-first (alto risco), 2 `.mjs` em inglês |
| **Risco principal** | 10 módulos-registro (`tipos_obra.py` sozinho tem **74 importadores**) — renomear quebra imports em cascata |
| **Recomendação** | Regra vale para **scripts executáveis** (CLI, `if __name__ == "__main__"`); módulos-biblioteca importados ficam isentos (convenção Python padrão) — ver §4 |
| **Esforço** | Fase A (baixo risco): 2-3h · Fase B (módulos, opcional): 6-10h se aprovada |

---

# 2. Diagnóstico do estado atual

## 2.1 Já conformes (maioria — não mexer)

`gerar-*`, `validar-*`, `criar-*`, `compilar-*`, `auditar-*`, `extrair-*`,
`migrar-*`, `renomear-*`, `corrigir-*`, `personalizar-*`, `empacotar-*`,
`indexar-*`, `minerar-*`, `fatiar-*`, `transmutar-*`, `formatar-*`,
`classificar-*`, `compensar-*`, `revisar-e-polir-*`, `sincronizar-*`
já seguem `tipo(verbo)-o-que.py`. Nenhuma ação necessária.

## 2.2 Scratch/debug com prefixo `_` (candidatos a exclusão ou rename)

| Arquivo atual | Diagnóstico | Ação sugerida |
|---|---|---|
| `_gerar_ebooks_tmp.py` | nome com `_tmp` — script descartável | confirmar se ainda é usado; se não, **excluir**; se sim, `gerar-ebooks-lote.py` |
| `_regenerar_artes.py` | debug pontual de campanha | excluir ou `regenerar-artes.py` |
| `_testar_resolucao.py` | duplicado com `2` | excluir os dois ou consolidar em `verificar-resolucao-imagem.py` |
| `_testar_resolucao2.py` | idem | idem |
| `_verificar_arnes.py` | **typo** no nome (provável "artes") | excluir ou `verificar-artes-campanha.py` |
| `_verificar_progresso.py` | debug pontual | excluir ou `verificar-progresso-obra.py` |

Todos violam também a regra de portfólio (§0.12 do `CLAUDE.md`: nenhum artefato
gerado usa prefixo `_`). Tratar como débito técnico preexistente.

## 2.3 Separador inconsistente (`_` → `-`) — risco baixo

| Atual | Novo |
|---|---|
| `descobrir_modelos.py` | `descobrir-modelos.py` |
| `detectar_llms_gratuitas.py` | `detectar-llms-gratuitas.py` |
| `executar_oh_my.ps1` | `executar-oh-my.ps1` |
| `resolver_oh_my.py` | `resolver-oh-my.py` |

## 2.4 Falta o `tipo` (verbo) no início

| Atual | Novo |
|---|---|
| `qualidade-mimocode.py` | `validar-qualidade-mimocode.py` |

## 2.5 Inglês em vez de PT-BR (R1)

| Atual | Novo |
|---|---|
| `sync-opencode-mcp.mjs` | `sincronizar-mcp-opencode.mjs` |
| `sync-vscode-mcp.mjs` | `sincronizar-mcp-vscode.mjs` |
| `setup-links.ps1` / `.sh` | manter — nome documentado em prosa no `CLAUDE.md` §6 (custo de rename > benefício); ou `configurar-links.ps1/.sh` se o operador preferir 100% de conformidade |

## 2.6 Módulos-biblioteca (noun-first) — decisão de escopo, ver §4

`tipos_obra.py` (74 importadores), `parametros_obra.py`, `metadados_livro.py`,
`nomes_curtos.py`, `secoes_eita.py`, `series_capa.py`, `fontes_academicas.py`,
`pdf_typst.py`, `colecao.py` (híbrido: módulo + CLI `--sincronizar`),
`campanha.py` (híbrido: registro + CLI), `task_router.py` (a classificar:
módulo ou CLI — verificar antes da Fase B).

---

# 3. Taxonomia de `<tipo>` (vocabulário fechado)

Baseada nos verbos já dominantes no projeto — não inventar verbos novos:

`gerar` · `validar` · `criar` · `compilar` · `auditar` · `extrair` · `migrar` ·
`renomear` · `corrigir` · `personalizar` · `sincronizar` · `empacotar` ·
`indexar` · `minerar` · `fatiar` · `transmutar` · `formatar` · `classificar` ·
`converter` · `revisar` · `resolver` · `descobrir` · `detectar` · `verificar` ·
`compensar` · `configurar`

Regra de escolha: usar o verbo que já aparece no `docstring`/`--help` do
script; não reclassificar semântica, só nomenclatura.

---

# 4. Decisão de escopo (recomendação)

A regra `tipo-oque.ext` nasceu para **scripts executados diretamente**
(`python scripts/x.py`, entradas do `tipos_obra.py`, comandos em
`.claude/commands/*.md`). Aplicá-la também aos **módulos de biblioteca**
(`tipos_obra.py`, `colecao.py`, etc.) contraria a convenção Python padrão
(módulo = substantivo do domínio que ele modela) e dispara reescrita de
import em **74 arquivos** só para `tipos_obra.py` — risco desproporcional ao
ganho, já que ninguém digita `python scripts/tipos_obra.py` na prática.

**Recomendação:** Fase A cobre apenas §2.2 a §2.5 (16 arquivos, baixo risco).
Módulos de §2.6 ficam de fora por padrão. Se o operador quiser 100% de
cobertura mesmo assim, a Fase B abaixo cobre esse caso — mas só deve rodar
com aprovação explícita, dado o custo.

---

# 5. O que NÃO tocar

- `relatorios/**` e `melhorias/**` (exceto este arquivo) — registro histórico
  datado; referenciam nomes de script que existiam **no momento daquela
  sessão**. Reescrever seria falsificar o histórico (mesmo princípio de não
  reescrever `git log`).
- `docs/superpowers/specs/**` e `docs/superpowers/plans/**` — specs de
  features já implementadas, mesmo motivo.
- `templates/maquina/**` — subprojeto próprio (Next.js/FastAPI da máquina de
  vendas), vocabulário e scripts independentes deste repo.
- `.claude/mcp-servers/code-review-graph/**` — submodule vendorizado
  (read-only).

---

# 6. Execução — Fase A (recomendada, baixo risco)

1. **Congelar:** rodar `python -m pytest -q` para confirmar baseline verde
   (R16 — nunca partir de suíte vermelha).
2. **Triagem dos scratch (§2.2):** perguntar ao operador, arquivo por arquivo,
   se ainda é usado (`grep -rn "<nome>" --include="*.py" --include="*.md"`).
   Excluir os confirmados mortos; renomear os vivos.
3. **Rename com `git mv`** (preserva histórico/blame) para os 10 arquivos de
   §2.3-§2.5, um lote por vez.
4. **Atualizar referências** por arquivo renomeado, nesta ordem (grep exato do
   nome antigo, exclude `relatorios/`, `melhorias/`, `docs/superpowers/`):
   - `scripts/*.py` (imports cruzados, `subprocess`, docstrings)
   - `tests/*.py`
   - `.claude/commands/*.md`, `.claude/agents/*.md`, `.claude/skills/**/SKILL.md`
   - `CLAUDE.md` (hardlink propaga para `AGENTS.md`, `.cursor/rules/*.mdc`,
     `.windsurfrules`, `.clinerules`, `.github/copilot-instructions.md` —
     **1 edição basta**; conferir depois com `git diff` se os 5 realmente
     mudaram juntos)
   - `docs/*.md` (documentação viva)
   - `SPEC*.md`, `PLANO_V4_MULTI_FORMATO.md`
5. **Achado a investigar:** `.windsurf/rules/fabrica-agentica.md` apareceu na
   varredura com as mesmas 31 ocorrências do grupo hardlink, mas não está na
   lista oficial de hardlinks do §6 do `CLAUDE.md`. Confirmar se é duplicata
   órfã (candidata a remoção) ou hardlink não documentado.
6. **Rodar suíte completa** (`python -m pytest -q`) — 100% obrigatório (R16).
7. **Smoke test funcional:** rodar 1-2 comandos reais que invocam os scripts
   renomeados (ex.: `python scripts/descobrir-modelos.py`) para confirmar que
   não há referência hardcoded esquecida fora de grep (ex.: strings montadas
   dinamicamente).
8. **Commit + push** (por lote, nunca um commit gigante misturando tudo).

---

# 7. Execução — Fase B (opcional, só com aprovação explícita)

Cobre os 10 módulos de §2.6. Mesma mecânica do passo 3-8 acima, mas:

- Fazer **um módulo por vez**, começando pelo de menor blast radius
  (`fontes_academicas.py`, 2 refs) e deixando `tipos_obra.py` (74 refs) por
  último.
- Antes de cada rename, rodar
  `grep -rln "import <modulo>\|from <modulo>\|scripts\.<modulo>"` para ter a
  lista exata de arquivos a tocar.
- `colecao.py` e `campanha.py` são híbridos (módulo + CLI) — decidir nome
  único que sirva aos dois papéis (ex.: manter substantivo, já que o uso
  majoritário é `import`).
- Suíte 100% + smoke test **após cada módulo**, não só no final.

---

# 8. Checklist de validação final

- [ ] `python -m pytest -q` → 100%
- [ ] `grep -rn "<nome-antigo>"` (fora de `relatorios/`, `melhorias/`,
      `docs/superpowers/`) → vazio, para cada arquivo renomeado
- [ ] `git status` limpo, nenhum arquivo órfão sobrando com nome antigo
- [ ] `.claude/settings.json` (hook `pre-commit`, referências de path) revisado
- [ ] Comandos `.claude/commands/*.md` testados manualmente (ao menos 1 fluxo
      ponta a ponta, ex.: `/criar-lead-magnet`)
- [ ] Commit + push por lote, mensagens descrevendo o rename

---

# 9. Riscos e mitigação

| Risco | Mitigação |
|---|---|
| Import quebrado silenciosamente (Python não falha até rodar o path) | Suíte completa + smoke test real após cada lote, não só grep |
| `CLAUDE.md` hardlink diverge sem perceber | `git diff` nos 5-6 arquivos hardlinkados após a edição |
| Referência dinâmica (`f"scripts/{nome}.py"`) não pega no grep textual | Buscar também por `Path(__file__).parent / "..."` e strings f-string com `scripts` |
| Renomear módulo com 74 importadores quebra a esteira inteira | Fase B fora do escopo padrão; só com aprovação e um módulo por vez |
| Scratch script `_verificar_arnes.py` ser usado por engano em automação | Confirmar com `grep` antes de excluir, nunca assumir "não usado" |

---

# 10. Próximos passos

1. Operador aprova o escopo (Fase A apenas, ou A+B).
2. Operador confirma quais dos 6 scripts `_scratch` ainda são usados.
3. Executar Fase A em lotes, com commit+push e suíte verde a cada lote (R16).
4. Se aprovado, Fase B módulo a módulo.
5. Fechar sessão com `gerar-relatorio-sessao` (convenção V5.2).
