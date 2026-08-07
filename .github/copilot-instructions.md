---
description: Regras, squad e fluxo da Fábrica Agêntica de Publicações — orquestrador para qualquer agente neste diretório.
alwaysApply: true
---

# FÁBRICA AGÊNTICA DE PUBLICAÇÕES — Orquestrador Central

> V4 (multi-formato): Livro, TCC, Artigo Científico, E-book.
> Hardlink de `CLAUDE.md`, `.cursor/rules/fabrica-agentica.mdc`, `.windsurfrules`,
> `.clinerules`, `.github/copilot-instructions.md`. Edite apenas este arquivo.
> Junctions: `agentic/` e `.agents/` apontam para `.claude/` (portabilidade multi-IDE).
> Para recriar links após clone: `scripts/setup-links.ps1` (Win) ou `setup-links.sh` (Mac/Linux).

## 0. Economia Severa de Tokens (PRIORIDADE MÁXIMA)

1. **Caveman Ativo:** pensamento telegráfico (3-5 linhas), sem preâmbulos/saudações.
2. **Headroom & RTK:** logs/builds >7 linhas → comprimir (3 topo + 4 fim). EXCEÇÃO: conteúdo em `output/**` e dados de obra NUNCA são comprimidos.
3. **LeanCTX:** grep antes de read em código/config. Limitar leitura por linha.
4. **Delegação Cavecrew:** subagentes comprimidos para buscas/edições extensas (nunca para prosa).
5. **Pandoc+Typst ISENTO:** compilação PDF é liberada e obrigatória. Nenhuma regra de token economy interfere.
6. **Fallback Terminal:** se sandbox bloquear, exibir comandos PowerShell no chat para o usuário rodar.
7. **Soberania do Usuário:** nada é barrado sem confirmação explícita do operador.
8. **Fidelidade de Conteúdo (sobrepõe 2-4):** arquivos em `output/**`, JSONs de estado, e verificações de `auditar-obra.py`/`validar-codigo.py`/`revisor-tecnico` são isentos de compressão — leitura sempre integral.
9. **Busca via Grafo:** usar `.code-review-graph` antes de tools de leitura/busca.
10. **Auto-commit/push:** alterações devem ser commitadas e pushadas para manter grafo atualizado.

## 1. Regras Globais

- **R1 (Idioma):** PT-BR estrito em toda comunicação e artefatos.
- **R2 (Silenciamento):** sem preâmbulos/saudações nos artefatos. Markdown limpo.
- **R3 (Autonomia):** após tema definido, fábrica roda 100% autônoma.
- **R4 (Auto-correção):** desvios são corrigidos internamente antes da compilação.
- **R5 (Capa 2D Plano):** Livro/E-book usam padrão 2D plano (detalhes em `docs/referencia-capa-design.md`). TCC/Artigo usam capa ABNT sóbria. Badge de nível OBRIGATÓRIO (validado por `validar-capa-nivel.py`).
- **R6 (Modelo Livre):** nenhum modelo LLM fixo. `model: inherit` em todos os agents.

### Tipos de Obra (V4)

| Tipo | Spec | Comando | Redator | Compilador |
|---|---|---|---|---|
| Livro | `SPEC.md` | `/criar-livro` | `redator-eita` | `compilador-abnt` |
| TCC | `SPEC_TCC.md` | `/criar-tcc` | `redator-academico` | `compilador-tcc` |
| Artigo | `SPEC_ARTIGO.md` | `/criar-artigo` | `redator-academico` | `compilador-artigo` |
| E-book | `SPEC_EBOOK.md` | `/criar-ebook` | `redator-ebook` | `gerar-epub.py` |

Artigo/E-book reaproveitam dossiê do livro-mãe via `fatiar-obra.py` + `indexar-dossie.py`.

## 2. Squad

### Skills Editorial
`pesquisador` (F1) → `arquiteto` (F1) → `estrategista` (F2) → `redator-eita`/`redator-academico`/`redator-ebook` (F2) → `revisor-tecnico` (F2.5) → `compilador-abnt`/`compilador-tcc`/`compilador-artigo` (F3)

### Subagentes (`.claude/agents/`)
`subagente-pesquisador`, `subagente-redator-capitulo`, `subagente-redator-secao-tcc`, `subagente-redator-artigo`, `subagente-adaptador-ebook`, `subagente-revisor-tecnico`, `subagente-ilustrador`

### Scripts Determinísticos
`indexar-dossie.py` (RAG), `pool-capitulos.py` (lotes), `renderizar-diagramas.py`, `validar-codigo.py`, `auditar-obra.py`, `metadados_livro.py`, `parametros_obra.py`, `validar-abnt-tcc.py`, `fatiar-obra.py`, `gerar-epub.py`, `pdf_typst.py`, `series_capa.py`, `validar-capa-texto.py`, `validar-capa-nivel.py`

### Token Economy Skills
`lean-ctx`, `headroom`, `caveman`, `rtk-memory`, `pre-flight-check`, `calcular-gastos-sessao`

### Fable Skills
`fable-method`, `fable-domain`, `fable-judge`, `fable-loop`, `self-learning`

## 3. MCPs

- `db_state` (SQLite) — estado da esteira
- `file_writer` — grava Markdown
- `mcp_deep_search` → `WebSearch`/`WebFetch` nativos
- `pdf_gen` (fallback CloudConvert) — método principal: Pandoc+Typst via `compilar-para-pdf.py`

## 4. Templates

`templates/template.typ` (Livro ABNT), `template_tcc.typ` (TCC NBR 14724), `template_artigo.typ` (Artigo NBR 6022), `template_eita.md` (molde EITA-V2)

## 5. Fluxo Operacional

1. **Input:** operador define tema → `/esbocar <tema>`
2. **Fase 1:** pesquisador varre → `indexar-dossie.py --indexar` → arquiteto gera sumário macro
3. **Fase 2:** `pool-capitulos.py --plano --lote 4` → subagentes-redator em lotes (estratégia + redação + diagrama + CI + auto-validação). Retentativa com backoff (máx. 3)
4. **Fase 2.5:** `auditar-obra.py` + `validar-codigo.py` → `revisor-tecnico` corrige
5. **Fase 3:** `compilador-abnt` merge + pré/pós-textuais + referências ABNT
6. **PDF:** `compilar-para-pdf.py <slug> --paginas-exatas` → Pandoc→`.typ`→Typst

**Output:** `output/livros/<slug>/`, `output/tccs/<slug>/`, `output/artigos/<slug>/`, `output/ebooks/<slug>/`
**Nota:** não usar `pandoc --pdf-engine=typst` com figuras (bug de path absoluto Windows). Gerar `.typ` na pasta do livro e chamar `typst compile --root`.

## 6. Portabilidade Multi-IDE

Fonte: `.claude/`. Junctions: `agentic/*` e `.agents/*` → `.claude/*`. Hardlinks: `AGENTS.md`→`CLAUDE.md`, `.cursor/rules/`→`CLAUDE.md`, `.cursor/mcp.json`→`.mcp.json`. VS Code: `scripts/sync-vscode-mcp.mjs`.

## 7. RTK SCRATCHPAD

*(Espaço para registro de aprendizados pela skill `rtk-memory`)*
