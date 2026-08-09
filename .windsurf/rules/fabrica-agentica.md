---
description: Regras, squad e fluxo da Fábrica Agêntica de Publicações — orquestrador para qualquer agente neste diretório.
alwaysApply: true
---

# FÁBRICA AGÊNTICA DE PUBLICAÇÕES — Orquestrador Central

> V5 (coleção): Livro, TCC, Artigo, E-book, Playbook, Lead Magnet, Deck, E-mails.
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
11. **UTF-8 no Windows:** todo script Python com `print`/emojis DEVE ter `console_utf8()` (padrão `scripts/tipos_obra.py`) ou `sys.stdout.reconfigure(encoding="utf-8")` — sem isso quebra em cp1252 (ex.: `criar-maquina-vendas.py`).
12. **Personalizar, não só gerar:** a máquina de vendas nasce com copy genérica ("Autor Digital", "centenas de pessoas") — o fluxo `/criar-maquina` exige personalização por nicho (configs + frontend + e-mails + README) com gate `grep 'Autor Digital|centenas de pessoas'` retornando vazio.

## 1. Regras Globais

- **R1 (Idioma):** PT-BR estrito em toda comunicação e artefatos.
- **R2 (Silenciamento):** sem preâmbulos/saudações nos artefatos. Markdown limpo.
- **R3 (Autonomia):** após tema definido, fábrica roda 100% autônoma.
- **R4 (Auto-correção):** desvios são corrigidos internamente antes da compilação.
- **R5 (Capa 2D Plano):** Livro/E-book usam padrão 2D plano (detalhes em `docs/referencia-capa-design.md`). TCC/Artigo usam capa ABNT sóbria. Badge de nível OBRIGATÓRIO (validado por `validar-capa-nivel.py`).
- **R6 (Modelo Livre):** nenhum modelo LLM fixo. `model: inherit` em todos os agents.
- **R16 (Pós-implementação — nunca commitar vermelho):** APÓS TODA nova implementação: (1) rodar a suíte de testes necessária (`python -m pytest -q`, ou a suíte específica + a completa); (2) **100%** → commit + push; (3) **<100%** → analisar a falha, corrigir o código, re-testar até 100% (nunca commitar suíte vermelha; nunca contornar o teste para fazê-lo passar — corrigir a causa). Vale para qualquer agente/sessão da fábrica, incluindo reescrita de materiais.

### Tipos de Obra (V5) — registro declarativo em `scripts/tipos_obra.py`

| Tipo | Natureza | Custo LLM | Spec | Comando | Produtor |
|---|---|---|---|---|---|
| Livro | geração | alto | `SPEC.md` | `/criar-livro` | `redator-eita` |
| TCC | geração | alto | `SPEC_TCC.md` | `/criar-tcc` | `redator-academico` |
| Artigo | compressão | baixo | `SPEC_ARTIGO.md` | `/criar-artigo` | `redator-academico` |
| E-book | compressão | baixo | `SPEC_EBOOK.md` | `/criar-ebook` | `redator-ebook` |
| Playbook | extração | **zero** | `SPEC_PLAYBOOK.md` | `/criar-playbook` | `extrair-passos-praticos.py` |
| Lead Magnet | extração | **zero** | `SPEC_LEAD_MAGNET.md` | `/criar-lead-magnet` | `gerar-lead-magnet.py` |
| Deck | extração | **zero** | `SPEC_DECK.md` | `/criar-deck` | `gerar-deck.py` + `gerar-deck-html.py` |
| E-mails | extração | baixo | `SPEC_EMAILS.md` | `/criar-emails` | `gerar-sequencia-emails.py` |

**Motores de saída:** Pandoc→Typst é o padrão. Duas exceções onde o design vem
de CSS: **lead magnet** (`gerar-lead-magnet-pdf.py`) e **deck**
(`gerar-deck-html.py`), ambos HTML+CSS→Chromium.

O HTML é camada **intermediária** no lead magnet (entregável = PDF) e
**entregável** no deck (apresenta no navegador, offline). PPTX do deck existe via
`gerar-pptx.py`, mas fora do pacote.

**Nomenclatura curta (V5.1):** `output/<raiz>/<código-obra>/<pfx>-<seq>-<nome>/`.
Caminhos caíram de ~197 para ~150 chars (MAX_PATH do Windows = 260). Vale para os
tipos V5; artigo/e-book mantêm o nome V4 para não orfanar artefatos já compilados.
Regras em `scripts/nomes_curtos.py`.

**Adicionar um tipo novo = 1 entrada em `scripts/tipos_obra.py`.** Os 6 pontos de
dispatch (`parametros_obra`, `fatiar-obra`, `auditar-obra`, `gerar-capa`,
`metadados_livro`, `compilar-para-pdf`) consultam o registro — não se edita mais
6 arquivos por tipo. Matriz: `python scripts/tipos_obra.py --matriz`.

**Regra de derivação:** cascateie onde **comprime**, faça fan-out onde **expande**.
Compressão/extração são baratas; expansão (ex.: TCC → livro) custa geração.

### COLEÇÃO

Conjunto de todos os artefatos derivados de um mesmo **núcleo canônico**
(dossiê + `sumario_macro` + `motivo_condutor`), compartilhando identidade visual,
vocabulário condutor, badge de nível e CTA. Manifesto derivado em
`<obra>/colecoes/<nome>.json` — o hub da coleção (`scripts/colecao.py
--sincronizar`, comando `/colecao`). O fallback plano `output/colecoes/<nome>.json`
só existe quando nenhum hub foi criado (comportamento atual de `colecao.py`).

**Nenhum arquivo ou pasta gerado usa prefixo `_`** — em glob de shell, listagem
de nuvem e empacotamento ele é tratado como oculto. Caminhos legados são migrados
automaticamente (`nomes_curtos.migrar_prefixo_underscore`).

## 2. Squad

### Skills Editorial
`pesquisador` (F1) → `arquiteto` (F1) → `estrategista` (F2) → `redator-eita`/`redator-academico`/`redator-ebook` (F2) → `revisor-tecnico` (F2.5) → `compilador-abnt`/`compilador-tcc`/`compilador-artigo` (F3)

### Subagentes (`.claude/agents/`)
`subagente-pesquisador`, `subagente-redator-capitulo`, `subagente-redator-secao-tcc`, `subagente-redator-artigo`, `subagente-adaptador-ebook`, `subagente-revisor-tecnico`, `subagente-ilustrador`

### Scripts Determinísticos
`indexar-dossie.py` (RAG), `pool-capitulos.py` (lotes), `renderizar-diagramas.py`, `validar-codigo.py`, `auditar-obra.py`, `metadados_livro.py`, `parametros_obra.py`, `validar-abnt-tcc.py`, `fatiar-obra.py`, `gerar-epub.py`, `pdf_typst.py`, `series_capa.py`, `validar-capa-texto.py`, `validar-capa-nivel.py`

**V5:** `tipos_obra.py` (registro de tipos), `secoes_eita.py` (parser EITA canônico), `colecao.py`, `extrair-passos-praticos.py`, `validar-playbook.py`, `gerar-lead-magnet.py`, `validar-lead-magnet.py`, `gerar-deck.py`, `validar-deck.py`, `gerar-sequencia-emails.py`, `validar-emails.py`, `gerar-lead-magnet-pdf.py`, `gerar-pptx.py`, `gerar-deck-html.py`, `nomes_curtos.py`, `validar-artefatos.py`, `empacotar-colecao.py`

**Gates de conteúdo (F1/F2 — mérito, além da estrutura R1-R15):** `validar-referencias.py` (R-RF: URL/DOI reais, 4xx/DNS reprova, cache + `--sem-rede`), `validar-metricas.py` (R-MT: ≥1 métrica com valor+unidade+citação por capítulo; `metricas_obrigatorias` no sumário), `validar-escala.py` (R-ES: limites/contorno na seção Aplica), `validar-afirmacoes.py` (R-AF: dado factual sem `[N]` no parágrafo reprova), `validar-fontes.py` (R-FT: hierarquia A/B/C do dossiê ≥70% A+B). `validar-codigo.py --executar` (smoke test real de python/js/bash) e `--playbook` (gate dos cards vira comando executado). Registrados em `tipos_obra.py` → campo `gates_conteudo` do tipo `livro`; `auditar-obra.py --estrito` os encadeia (referências offline).

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

`templates/template.typ` (Livro ABNT), `template_tcc.typ` (TCC NBR 14724), `template_artigo.typ` (Artigo NBR 6022), `template_eita.md` (molde EITA-V2), `template_playbook.typ` (cards de bancada), `template_lead_magnet.html` (A4 + CTA no rodapé), `template_deck.html` (16:9 navegável + PDF)

## 5. Fluxo Operacional

1. **Input:** operador define tema → `/esbocar <tema>`
2. **Fase 1:** pesquisador varre → `indexar-dossie.py --indexar` → arquiteto gera sumário macro
3. **Fase 2:** `pool-capitulos.py --plano --lote 4` → subagentes-redator em lotes (estratégia + redação + diagrama + CI + auto-validação). Retentativa com backoff (máx. 3)
4. **Fase 2.5:** `auditar-obra.py` (encadeia os gates de conteúdo F1/F2 via `gates_conteudo` no `--estrito`) + `validar-codigo.py --executar` + `renderizar-diagramas.py --validar` → `revisor-tecnico` corrige (inclui conferência por amostra: reabrir 1 fonte por capítulo e conferir o dado citado)
5. **Fase 3:** `compilador-abnt` merge + pré/pós-textuais + referências ABNT
6. **PDF:** `compilar-para-pdf.py <slug> --paginas-exatas` → Pandoc→`.typ`→Typst
7. **Fase 4 (V5) — Coleção:** `/criar-playbook` → `/criar-lead-magnet --todos` +
   `/criar-deck` + `/criar-emails` (paralelos) → `colecao.py --sincronizar` →
   `empacotar-colecao.py`. Playbook **antes** dos lead magnets/e-mails.
8. **Entrega:** `validar-artefatos.py --todos --estrito` (testa se cada arquivo
   ABRE) → `empacotar-colecao.py <coleção>`. O pacote leva **só o que está
   finalizado e abre**, com `LICENCA.txt` e `LEIA-ME.md` que declara o que ficou
   de fora e por quê.
9. **Máquina de vendas:** `/criar-maquina <slug>` → gerar + **personalizar por
   nicho** (configs, frontend, e-mails, README) + testar `POST /api/checkout`
   (rota nasce no template — verificar que o lead chega em `/api/leads/`) + deploy.
10. **Campanha (V5.3):** `/campanha <slug>` (1 material) ou `/campanha-completa
    [colecao]` (todos os membros do manifesto) → `criar-campanha.py` (estrutura +
    moldes de copy + artes HTML→Chromium + cronogramas; custo zero) → agente
    escreve a copy final nos moldes (LLM baixo) → `validar-campanha.py --estrito`
    (gates R-CP-1..5) → `--marcar-completa`. Vive em
    `output/<colecao>/campanhas/<material>/` + `campanha.json` (hub). Não é tipo
    de obra: camada própria (registro declarativo em `scripts/campanha.py`).

**Output (HUB POR COLEÇÃO):** cada coleção vive em `output/<slug-colecao>/` com
as raízes de tipos **dentro do hub** — `livros/`, `tccs/`, `artigos/`, `ebooks/`,
`playbooks/`, `lead-magnets/`, `decks/`, `emails/`, `distribuicao/` e
`colecoes/<nome>.json` (manifestos). Não existem raízes planas no topo
(`output/livros/` etc.) — ver "Estrutura de Coleções (HUB)" abaixo.
**Nota:** não usar `pandoc --pdf-engine=typst` com figuras (bug de path absoluto Windows). Gerar `.typ` na pasta do livro e chamar `typst compile --root`.

### Estrutura de Coleções (HUB)

O agrupamento padrão da pasta `output/` é o **HUB POR COLEÇÃO**: uma pasta por
coleção (núcleo canônico: dossiê + `sumario_macro` + `motivo_condutor`):
```
output/<slug-colecao>/
├── livros/  tccs/  artigos/  ebooks/  playbooks/  lead-magnets/  decks/  emails/
├── campanhas/<material-slug>/  # Campanhas (V5.3): redes-sociais + canais-comunicacao
├── distribuicao/            # PDFs compilados para distribuição
├── marketing/<slug-livro>/  # Máquinas de vendas (Next.js+FastAPI)
└── colecoes/<nome>.json     # Manifestos sincronizados (colecao.py --sincronizar)
```
Suportado por `tipos_obra.py` (`_sereis`, `dir_obra`, `listar_materiais`,
`_obra_raiz`) e `colecao.py` (`_dir_colecoes` prioriza `<obra>/colecoes/`).

**Glossário de nomenclatura:** **coleção = hub** (unidade de organização da
pasta `output/`); **série = termo obsoleto**, preservado apenas como nome
interno de compatibilidade do registro de cores `output/series.json` (não
renomear: as cores persistidas e a migração de `_series.json` dependem do nome).

### Entrega de Sessão (V5.2) — `relatorios/`

Toda sessão de trabalho na fábrica deve encerrar com um **relatório em
`relatorios/`** (raiz do projeto), em **MD + PDF** (Pandoc→Typst):

```
relatorios/<YYYY-MM-DD>-<tema-da-sessao>.md
relatorios/<YYYY-MM-DD>-<tema-da-sessao>.pdf
```

Conteúdo mínimo: contexto, bugs descobertos/corrigidos (causa→fix), arquivos
alterados, validações (testes/verificações rodadas), commits feitos e resumo
de entregas. O relatório é commitado e pushado junto com o trabalho da sessão.

## 6. Portabilidade Multi-IDE

Fonte: `.claude/`. Junctions: `agentic/*` e `.agents/*` → `.claude/*`. Hardlinks: `AGENTS.md`→`CLAUDE.md`, `.cursor/rules/`→`CLAUDE.md`, `.cursor/mcp.json`→`.mcp.json`. VS Code: `scripts/sync-vscode-mcp.mjs`.

## 7. RTK SCRATCHPAD

*(Espaço para registro de aprendizados pela skill `rtk-memory`)*

- **2026-08-09 Reescrita e transmutação de materiais:** causa: a esteira só
  criava novo (-v2) ou retomava; não dava para regravar capítulo/obra nem mudar
  de tipo sem orfanar série/coleção. Fix: `pool-capitulos.py --reescrever <n>`
  (backup em `revisao/backups/<ts>/` + flag `reescrever` no estado que o
  `montar_visao` respeita até `--registrar --sucesso`); campo `reescrever_de`
  no registro de tipos (transmutação: livro←ebook/playbook/artigo/tcc,
  tcc←livro/ebook, ebook←livro/tcc/playbook, artigo←livro/tcc/ebook);
  `scripts/transmutar-obra.py` (recorte origem→destino, slug destino com
  sufixo `--liv/--tcc/--ebk/--art` no layout plano, `slug_origem` no config,
  registro em `derivados.json` da origem); comandos `/reescrever-capitulo`,
  `/reescrever`, `/refinar`, `/reescrever-como`; skills com Modo
  reescrita/transmutação (preservar refs [N] e diagramas; gates do DESTINO
  obrigatórios). Prevenção: R16 — após toda implementação, suíte 100% → commit
  e push; <100% → analisar, corrigir, testar (nunca commitar vermelho).
  Arquivos: `scripts/pool-capitulos.py`, `scripts/tipos_obra.py`,
  `scripts/transmutar-obra.py`, `.claude/commands/reescrever*.md`,
  `.claude/commands/refinar.md`.
- **2026-08-09 Gates de conteúdo F1/F2 (mérito além da estrutura):** causa:
  validar estrutura (R1-R15) não pegava referência inventada, código que não
  roda, capítulo sem métrica nem limite de escala, dado factual sem citação.
  Fix: 5 gates novos + `validar-codigo --executar/--playbook`; registro via
  campo `gates_conteudo` no tipo `livro` (tipos_obra.py) e encadeamento em
  `auditar-obra --estrito` (referências rodam offline `--sem-rede`; o
  revisor-tecnico roda com rede). Prevenção: estrategista declara
  `metricas_obrigatorias` no draft; redator-eita cita no mesmo parágrafo,
  inclui métrica e limites de escala; pesquisador classifica fontes `(A)/(B)/(C)`
  no dossiê (gate R-FT-1 ≥70% A+B). Ajustes calibrados: superlativos de ênfase
  ("o mais importante") e garantias técnicas ("nunca confie") NÃO são
  disparadores factuais (ruído); `**Desafio` (exercício do autor) é excluído;
  cache de referências só é conclusivo para ok/falha — `nao_verificado` não
  bloqueia checagem futura. Achado real do gate: `fin.ai/blog/ai-agent-roi-customer-support`
  404 no cap_1; playbook pbk-1 tem 13 blocos truncados sem elipse (código
  cortado no meio). Arquivo: `scripts/validar-*.py` + `tests/test_validar_*`.
- **2026-08-09 Máquina de vendas — checkout:** causa: rota `/api/checkout`
  faltava no template (checkout page postava nela → 404 em toda máquina nova) e
  page antiga usava form urlencoded vazio → 500 no `request.json()`. Fix: rota
  com zod + `/api/leads/` + `BACKEND_URL`; page client com nome/e-mail + fetch
  JSON. Prevenção: `produto` default alinhado ao `config/produtos.json`
  (ex.: `dentista-gestor-livro`); leads de teste vivem em
  `backend/data/vendas.db` (não `database/maquina.db`) — limpar. Arquivo:
  `templates/maquina/frontend/app/api/checkout/route.ts`.
- **2026-08-09 Máquina de vendas — fluxo:** causa: template nascia com copy
  genérica; `criar-maquina-vendas.py` quebrava no Windows cp1252 (emojis).
  Fix: personalização por nicho em 8 pontos com gate `grep 'Autor Digital|centenas de pessoas'`
  vazio (regra 12); `sys.stdout.reconfigure` no corpo de `criar_maquina`
  (regra 11). Derivados copiados via `output/colecoes/<slug>.json` (nomenclatura
  V5 não casa com substring — fallback 1ª palavra). Prevenção: máquinas antigas
  sincronizam copiando rota+page do template — skill `sincronizar-maquina-vendas`.
- **2026-08-09 Skill `gerar-relatorio-sessao`:** toda sessão com mudanças
  encerra em `relatorios/<YYYY-MM-DD>-<tema>.md/.pdf` (convenção V5.2) —
  relatório → testes → commit → push. Fix: `scripts/gerar-relatorio-sessao.py`
  (slug NFKD, 6 seções obrigatórias, Pandoc→Typst) + skill que orquestra o
  fluxo completo. Prevenção: nunca commitar sem `pytest -q` verde; mensagem via
  `git commit -F` (acentos/quebras de linha quebram `-m`); `_commit_msg*.txt`
  vaza no `git add -A` — apagar ANTES do add ou `git rm --cached` + `--amend`.
  Arquivo: `.claude/skills/gerar-relatorio-sessao/SKILL.md`.
- **2026-08-09 Padronização HUB POR COLEÇÃO:** causa: `output/` misturava layout
  plano (`output/livros/`, `output/tccs/` vazios) com hubs; `output/series.json`
  tinha 120/125 `membros` órfãos (destinos `livros/<slug>` de layout antigo);
  docs/AGENTS.md ainda descreviam organização por "série" (regra morta
  `output/series/`). Fix: coleção = hub único (`output/<obra>/<tipo>/...` com
  manifesto em `<obra>/colecoes/<nome>.json`); "série" virou termo obsoleto —
  preservado APENAS como nome interno de `output/series.json` (cores persistidas
  + migração `_series.json` dependem — NÃO renomear); `series_capa.py --reindexar`
  reconstrói `membros` com slugs reais (via `tipos_obra.listar_materiais` +
  `resolver_serie_key`), preserva cores, órfãos saem, chaves sem material ficam
  com `membros: []` (cor reservada). Prevenção: ao criar material novo, usar
  sempre `dir_obra`/`listar_materiais` (resolvem plano, por-obra e single-book);
  rodar `series_capa.py --reindexar` após reorganizações de `output/`.
  Arquivo: `scripts/series_capa.py`, `scripts/tipos_obra.py`, `AGENTS.md` §COLEÇÃO.
- **2026-08-09 Reestruturação HUB POR COLEÇÃO (manifestos por hub):** causa:
  `_dir_colecoes` gravava os 7 manifestos no 1º hub com `colecoes/` (analista)
  e single-books viviam na raiz de `livros/`/`tccs/` (fora do padrão `*/*`);
  `<hub>/series.json` (metadados ricos) duplicava o conceito do manifesto.
  Fix: `_dir_colecoes_da` resolve o dir pelo hub da coleção (1º segmento comum
  dos membros que não seja raiz de tipo; fallback plano `output/colecoes/`);
  `_metadados_ricos` funde `<hub>/series.json` no manifesto e apaga o legado
  (idempotente: reusa `metadados` do manifesto anterior); single-books migrados
  para `<tipo>/<slug>/`; `_todos_dirs_manifestos` varre `DIR_OUTPUT/*/colecoes`
  (NÃO `tipos_obra._sereis()` — usa `TO.DIR_OUTPUT` real, quebra teste com
  monkeypatch). Prevenção: limpeza global de manifestos órfãos deve varrer
  fallback + hubs; `_slug_arquivo` vira `ç` em `-` (minha-cole-o.json).
  Arquivo: `scripts/colecao.py`, `tests/test_colecao_hub.py`.
- **2026-08-09 Camada CAMPANHA (V5.3):** causa: a coleção entregava materiais,
  mas nenhuma camada de divulgação (posts, artes, sequências, cronogramas).
  Fix: `output/<colecao>/campanhas/<material>/` (HUB por coleção, subpasta por
  material: redes-sociais/instagram+linkedin e canais-comunicacao/emails+whatsapp);
  registro declarativo em `scripts/campanha.py` (artefato novo = 1 linha);
  `criar-campanha.py --material/--completo/--marcar-completa` (estrutura +
  moldes com rascunho determinístico do config_obra/sumário/manifesto + artes
  HTML+CSS→Chromium PNG + cronogramas com datas reais; custo zero) →
  agente reescreve copy (LLM baixo) → `validar-campanha.py` (R-CP-1..5 +
  R-CP-C1 no --completo; copy genérica regra 12 reprova; molde `Status: RASCUNHO`
  pendente reprova até a reescrita). Prevenção: campanha NÃO é tipo de obra
  (não toca tipos_obra.py); identidade vem do manifesto (`cor_accent`,
  `motivo_condutor.vocabulario`, `nucleo.senioridade`, `cta_url`); arquivo do
  manifesto usa slug normalizado (`_slug_arquivo` — `Colecao Teste` →
  `colecao-teste.json`); nos testes, monkeypatch de TODOS os `DIR_OUTPUT`
  (colecao.py incluído — esquecer `colecao.DIR_OUTPUT` faz o `varrer()` ler o
  output real e o teste falha de forma confusa).
  Arquivos: `scripts/campanha.py`, `scripts/criar-campanha.py`,
  `scripts/validar-campanha.py`, `templates/campanha/*.html`,
  `.claude/commands/campanha.md`, `.claude/commands/campanha-completa.md`,
  `tests/test_campanha.py`, spec em `melhorias/09-08-2026-campanhas-camada-nova.md`.
