# Plano de ação — Padronização HUB POR COLEÇÃO

Data: 09-08-2026
Decisão: **manter o agrupamento "HUB POR COLEÇÃO"** como padrão único da pasta `output/`, atualizando documentação, removendo regras mortas/órfãos e implementando a limpeza.

## 1. Diagnóstico (estado real)

| Item | Estado | Uso real |
|---|---|---|
| `output/<slug-colecao>/` (hubs: `ia-agentica-desbloqueada/`, `sistemas-agenticos/`, `analista-financeiro-futuro-odontologia-pt/`, `harness-engineering/`, etc.) | **PADRÃO REAL** — cada hub contém `livros/`, `tccs/`, `artigos/`, `ebooks/`, `playbooks/`, `lead-magnets/`, `decks/`, `emails/`, `distribuicao/` e `colecoes/*.json` | Suportado por `tipos_obra.py` (`_sereis`, `dir_obra`, `listar_materiais`, `_obra_raiz`) e `colecao.py` (`_dir_colecoes` prioriza `<obra>/colecoes/`) |
| `output/series.json` | Registro de **cores de accent** por série/coleção (usado por `series_capa.py` em capas, PPTX, PDF) | **MANTER** o arquivo (o código depende); campo `membros` com 40/40 destinos `livros/<slug>` **inexistentes** (órfãos históricos do layout plano) |
| `output/series/` | **NÃO EXISTE** no disco nem no código | Regra morta do AGENTS.md §"Estrutura de Séries (V5.1)" |
| `output/livros/`, `output/tccs/`, `output/colecoes/` | Pastas **vazias** (sem symlinks de compatibilidade prometidos) | Remover |
| AGENTS.md §"Estrutura de Séries (V5.1)" | Descreve `output/series/<slug-serie>/` + symlinks — **nunca implementado** | Diretriz ultrapassada → reescrever como HUB POR COLEÇÃO |
| AGENTS.md §"COLEÇÃO" e §"Output" | Manifesto em `output/colecoes/<nome>.json` e raízes em `output/livros/` etc. | Desatualizado → manifestos vivem em `<obra>/colecoes/`; raízes vivem dentro dos hubs |
| `docs/superpowers/specs/06-08-specs-capas-padronizadas-design.md` e `plans/2026-08-06-padronizacao-capas.md` | Referenciam `output/_series.json` (nome migrado p/ `series.json`) | Docs históricos de superpowers → manter como registro histórico, não editar |
| `docs/manual-completo-fabrica.md` (L125/147/438) | Descreve `series.json` como cores das séries | Corrigir semântica: "cores da coleção" |
| `scripts/gerar-capa.py` (L8), `scripts/nomes_curtos.py` (L131) | Comentários citando `output/_series.json` | Atualizar para `series.json` |
| `scripts/colecao.py` (docstring L11) | "grava output/colecoes/<colecao>.json" | Atualizar: grava em `<obra>/colecoes/` quando o hub existe |
| `.agents/`, `agentic/`, `.cursor/rules/`, `.windsurfrules`, `.clinerules`, `.github/copilot-instructions.md` | Junctions/hardlinks do AGENTS.md | Verificar integridade após a edição do AGENTS.md |

## 2. Plano de ação

### FASE 1 — ATUALIZAR o que precisa ser atualizado

1. **AGENTS.md (fonte única; espelhos via hardlink)**
   - Reescrever §"Estrutura de Séries (V5.1)" → **"Estrutura de Coleções (HUB)"**:
     ```
     output/<slug-colecao>/
     ├── livros/  tccs/  artigos/  ebooks/  playbooks/  lead-magnets/  decks/  emails/
     ├── distribuicao/
     └── colecoes/<nome>.json        # manifestos sincronizados
     ```
   - §"Output": raízes de tipos vivem **dentro do hub** (sem `output/livros/` etc. no topo).
   - §"COLEÇÃO": manifesto em `<obra>/colecoes/<nome>.json` (fallback plano `output/colecoes/` apenas quando nenhum hub existe — comportamento atual de `colecao.py`).
   - Glossário de nomenclatura: **coleção = hub** (unidade de organização); **série = termo obsoleto**, preservado apenas como nome interno de compatibilidade do registro de cores `output/series.json` (não renomear: quebraria cores persistidas e a migração `_series.json`).
   - Remover a promessa de "Symlinks de compatibilidade em `output/livros/`..." (nunca implementada).
2. **Scripts** (comentários e docstrings, sem mudança de comportamento):
   - `scripts/gerar-capa.py` L8: `_series.json` → `series.json`.
   - `scripts/nomes_curtos.py` L131: idem.
   - `scripts/colecao.py` docstring: local real dos manifestos.
3. **Docs**: `docs/manual-completo-fabrica.md` — trocar "série" por "coleção" nos trechos de estrutura (L125/147/438); `docs/referencia-capa-design.md` idem (L25).

### FASE 2 — REMOVER regras mortas, órfãos e diretrizes ultrapassadas

1. **AGENTS.md**: excluir a seção "Estrutura de Séries (V5.1)" (substituída na Fase 1) e qualquer menção a `output/series/`.
2. **`output/series.json` — reindexar membros**: novo modo `python scripts/series_capa.py --reindexar` que reconstrói o registro preservando as **cores** já gravadas e substituindo `membros` pelos slugs **reais no disco** (varredura `tipos_obra.listar_materiais` + `_sereis`), eliminando os 40 destinos órfãos `livros/<slug>`.
3. **Pastas vazias legadas**: remover `output/livros/`, `output/tccs/`, `output/colecoes/` (git não versiona pastas vazias; o código as recria quando necessário — `_dir_colecoes` fallback).
4. **`docs/superpowers/specs|plans/2026-08-06-*`**: manter como **registro histórico** (sem edição); adicionar nota de migração apenas se houver manutenção futura.
5. **Espelhos**: conferir se `.clinerules`, `.windsurfrules`, `.cursor/rules/fabrica-agentica.mdc`, `.github/copilot-instructions.md` continuam hardlinks do AGENTS.md (editar apenas o AGENTS.md).

### FASE 3 — IMPLEMENTAR e validar

1. Aplicar Fase 1 + Fase 2 (edição AGENTS.md + scripts + docs + reindexação).
2. Rodar a suíte completa `python -m pytest -q` — **100% obrigatório** (R16).
3. Fumaça real:
   - `python scripts/colecao.py --sincronizar` → manifestos atualizados nos hubs.
   - `python scripts/series_capa.py --reindexar` → cores preservadas, membros órfãos zerados.
   - `python scripts/validar-artefatos.py --todos --estrito` → abertura dos artefatos intacta.
4. Commit + push (regras 10 e 16).
5. Registrar aprendizado no RTK scratchpad (AGENTS.md §7) e gerar relatório de sessão em `relatorios/`.

## 3. Critérios de aceite

- `grep -r "output/series/" AGENTS.md CLAUDE.md .clinerules .windsurfrules .cursor docs` → vazio.
- `output/series.json` sem membros apontando para caminho inexistente.
- Nenhum diretório vazio `output/livros|tccs|colecoes`.
- Suíte `pytest` 100% verde; manifestos e cores de capa inalterados após a reindexação.

## 4. Riscos e mitigações

- **Renomear `series.json`** → quebraria cores persistidas e capas: **não renomear**; apenas documentar como "registro de cores da coleção".
- **Remover `output/colecoes/`** → `_dir_colecoes` recria por fallback: comportamento inalterado.
- **Specs/plans históricos de superpowers** → não editar (registro histórico); risco zero de impacto no código.
