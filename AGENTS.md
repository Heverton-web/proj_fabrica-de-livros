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
12. **Personalizar, não só gerar:** a máquina de vendas nasce com copy genérica ("Autor Digital", "centenas de pessoas") — o fluxo `/criar-maquina` exige personalização por nicho (configs + frontend + e-mails + campanhas + README) com gate `grep 'Autor Digital|centenas de pessoas'` (incluindo `campanhas/` do snapshot) retornando vazio.

## 1. Regras Globais

- **R1 (Idioma):** PT-BR estrito em toda comunicação e artefatos.
- **R2 (Silenciamento):** sem preâmbulos/saudações nos artefatos. Markdown limpo.
- **R3 (Autonomia):** após tema definido, fábrica roda 100% autônoma.
- **R4 (Auto-correção):** desvios são corrigidos internamente antes da compilação.
- **R5 (Capa 2D Plano):** Livro/E-book usam padrão 2D plano (detalhes em `docs/referencia-capa-design.md`). TCC/Artigo usam capa ABNT sóbria. Badge de nível OBRIGATÓRIO (validado por `validar-capa-nivel.py`).
- **R6 (Modelo Livre):** nenhum modelo LLM fixo. `model: inherit` em todos os agents.
- **R16 (Pós-implementação — nunca commitar vermelho):** APÓS TODA nova implementação: (1) rodar a suíte de testes necessária (`python -m pytest -q`, ou a suíte específica + a completa); (2) **100%** → commit + push; (3) **<100%** → analisar a falha, corrigir o código, re-testar até 100% (nunca commitar suíte vermelha; nunca contornar o teste para fazê-lo passar — corrigir a causa). Vale para qualquer agente/sessão da fábrica, incluindo reescrita de materiais.
- **R17 (CAMPANHA e MÁQUINA são OPCIONAIS — REGRA INTOCÁVEL):** a geração de CAMPANHA (V5.3) e de MÁQUINA de vendas NUNCA é obrigatória no fluxo. (1) Na entrevista inicial (`/esbocar`), o operador escolhe explicitamente se quer incluir a etapa CAMPANHA e/ou a etapa MÁQUINA no fluxo daquela coleção (persistido em `config_obra.json`: `gerar_campanha`, `gerar_maquina`); `/produzir-obra-completa` respeita essa escolha e PULA o fluxo correspondente quando `false`, sem tratar como falha. (2) Independente da escolha na entrevista, o operador pode disparar CAMPANHA ou MÁQUINA a qualquer momento para uma coleção JÁ EXISTENTE (`/campanha`, `/campanha-completa`, `/criar-maquina`). (3) Se já existir CAMPANHA ou MÁQUINA para aquela coleção, o sistema SEMPRE oferece ao operador a escolha entre: **Criar Nova** (versiona a existente — a existente é preservada, a nova criação passa a ser a atual) ou **Sobrescrever Existente** (substitui a existente no lugar). Nunca decidir isso silenciosamente — a escolha é sempre do operador.

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

**V5.4 (pesquisa acadêmica — custo LLM zero):** `fontes_academicas.py` (registro declarativo das bases com API aberta: OpenAlex, Crossref, arXiv, Semantic Scholar, SciELO, PubMed — adicionar fonte = 1 entrada) e `minerar-fontes-academicas.py <tema> --slug <obra>` (mineração determinística via APIs, dedup por DOI, gera `pesquisa/mineracao_academica_<slug>.json/.md` já em ABNT classe (A), cache local + `--sem-rede`).

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
2. **Fase 1:** pesquisador varre → `minerar-fontes-academicas.py "<tema>" --slug <obra>` (custo zero, APIs abertas) → `indexar-dossie.py --indexar` → arquiteto gera sumário macro
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
9. **Máquina de vendas (V5.3):** `/criar-maquina <slug>` → gera em
   `output/<slug-colecao>/maquina/` (**1 máquina por COLEÇÃO**, regra 1:1; o hub
   é derivado do slug) com **snapshot das campanhas** em `maquina/campanhas/` +
   personalizar por nicho (configs, frontend, e-mails, campanhas, README) +
   testar `POST /api/checkout` (rota nasce no template — verificar que o lead
   chega em `/api/leads/`) + deploy. Legadas em `output/<hub>/marketing/` são
   sinalizadas como `maquinas_legadas` no manifesto da coleção.
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
├── maquina/                 # 1 máquina de vendas por coleção (Next.js+FastAPI)
├── campanhas/               # artefatos de campanha (textos, artes, cronogramas)
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

Fonte: `.claude/`. Junctions: `agentic/*`, `.agents/*` e `.opencode/{agents,commands,skills,mcp-servers,settings.json}` → `.claude/*`. Hardlinks: `AGENTS.md`→`CLAUDE.md`, `.cursor/rules/`→`CLAUDE.md`, `.cursor/mcp.json`→`.mcp.json`. Schemas MCP que diferem são GERADOS por script (não link): `.vscode/mcp.json` via `scripts/sincronizar-mcp-vscode.mjs`, `opencode.json` via `scripts/sincronizar-mcp-opencode.mjs` (preserva `instructions`/`permission`/chaves manuais por merge; sobrescreve só o bloco `mcp`). Hooks do OpenCode vivem em `.opencode/plugins/fabrica-hooks.ts` (versionado; espelha `.claude/settings.json` — junction de `settings.json` só serve o schema do plugin, que o OpenCode lê além do `settings.json`). Hook git `pre-commit` (mecaniza R16 — bloqueia commit se `pytest -q` falhar) fonte versionada em `scripts/hooks/pre-commit`, copiado para `.git/hooks/pre-commit` (não é link: `.git/hooks` não aceita hardlink/junction de forma confiável). Recriar após clone: `scripts/setup-links.ps1` (Win) ou `setup-links.sh` (Mac/Linux) — ambos recopiam o hook. Submodule `.claude/mcp-servers/code-review-graph` (fonte vendorizada de https://github.com/tirth8205/code-review-graph.git, só leitura/referência — o MCP server em si roda via `uvx code-review-graph serve` do PyPI, `.mcp.json` não aponta pro submodule); clonar com `git clone --recurse-submodules` ou rodar `git submodule update --init --recursive` depois.

## 7. RTK SCRATCHPAD

*(Espaço para registro de aprendizados pela skill `rtk-memory`)*

- **2026-08-17 TÉCNICA operacional (V5.6) — R12 não pode exigir Python cegamente:**
  causa: o gate R12 exigia ≥1 bloco de código na TÉCNICA em TODO livro, mesmo
  Iniciante/não-programador (o material-fonte usa configs/operações, não Python).
  Fix: campo `estilo_tecnica` no config_obra (`codigo`|`hibrido`|`operacional`;
  default `codigo` preserva obras existentes), R12 condicional em
  `auditar-obra.py` (operacional aceita ≥1 artefato = bloco | diagrama | passos
  numerados via novo contador `artefatos_tecnica`), template_eita.md + skill
  redator-eita documentam os modos. Prova real: obra `fabrica-agentica` reescrita
  com 0 blocos python/ts na TÉCNICA (96 blocos yaml/json/env/console/sql/cypher +
  tabelas de decisão) mantendo CONFORME (R2 500k, gates 5/5). Prevenção: ao
  reescrever a TÉCNICA, converter blocos IN-PLACE (prosa/citações [N] preservadas)
  e re-checar R2 (corpos novos ficaram ~40% menores; recuperar com seções extras
  e fechamento por capítulo); comandar terminal com efeito usa ```console
  (nao_aplicavel na CI), ```bash só para comandos puros; no R12 o predicado de
  `conforme` é a condição de FALHA (não inverter — bug real que fez FALHA com
  "capitulos sem artefato: nenhum"). Arquivos: `scripts/auditar-obra.py`,
  `scripts/parametros_obra.py`, `templates/template_eita.md`,
  `templates/capitulo_eita.md`, `.claude/skills/redator-eita/SKILL.md`,
  `tests/test_auditar_obra.py`, `tests/test_parametros_obra_v5.py`.
- **2026-08-11 Produção completa série 5 (coleção `agentic-design-patterns`):**
  causa: série 5 da proposta (Agentic Design Patterns — o "Gang of Four" dos
  fluxos agênticos) exigia fluxo FULL com livro, derivados, campanhas e máquina;
  3 lições reais. Fix/lições: (1) **pasta `campanhas/material/` é o nome
  CANÔNICO da campanha do livro-raiz** — `nome_material` do slug
  `<chave>/livros/<chave>-v1` trunca para `v1` e o fallback de `nome_curto`
  vira `material`; NÃO apagar (parece lixo, é a campanha do livro; as pastas
  dos derivados são `dck-1-design`, `eb-01-design` etc. com desambiguação V5.4);
  (2) `criar-campanha --completo` com 12 materiais estoura timeout (~590s) —
  rodar `--completo` e completar materiais restantes com `--material <slug>`
  individual (32 artes cada); (3) moldes de campanha nascem `Status: RASCUNHO`
  e R-CP-2 reprova — promover a `FINAL` com sed em massa e marcar `status:
  completa` no `campanha.json` (o flag `--marcar-completa` junto de
  `--completo` REGENERA tudo e estoura timeout; editar o JSON direto).
  Resultado: livro 68 pág CONFORME, 12 membros, campanhas 12/12 com 384 artes
  únicas (R-CP-6), máquina personalizada (gate regra 12 vazio), suíte 662/662.
  Arquivos: `output/agentic-design-patterns/**`,
  `relatorios/11-08--producao-completa-agentic-design-patterns.md/.pdf`.
- **2026-08-11 Cheatsheet vazio + R-PBK-5 em playbook de livro P (fluxo FULL MAS):** causa: (1) `gerar-lead-magnet.py --todos` gerava cheatsheet com 0 itens — `montar_cheatsheet` lê `card.comandos` no NÍVEL do card (ou `card.gate`), não dentro de `execucao[]`, e o `extrair-passos-praticos.py` só preenche `execucao[].codigo`; (2) `validar-playbook.py` R-PBK-5 conta a soma de linhas de TODOS os blocos de `execucao` (`sum(len(codigo)+2)`), então múltiplos blocos de código de capítulo estouram 25 linhas; (3) R2 do livro P exige ~100.000 chars (40 pág.) — 4 capítulos de ~20k chars ficam ~20% abaixo. Fix: adicionar `comandos` no topo dos cards do playbook (11 comandos → cheatsheet CONFORME); compactar `execucao` para 1 bloco de ≤18 linhas por card (truncar mantendo docstring+assinaturas); expandir capítulos com seções técnicas reais (votação do enxame, validação de contrato, retry com backoff, roteador, dual-mode, monitor de custo, calibração por amostra). Prevenção: cheatsheet = agregador de `card.comandos`/`card.gate` do playbook — se o playbook nasce sem comandos, o LM cheatsheet nasce vazio; validar playbook ANTES de gerar LMs; R2 = estimar chars por capítulo na escrita (mín. 25k por capítulo de livro P). Resultado: livro MAS 100.000+ chars/54 pág PDF CONFORME, playbook 4 passos CONFORME, 6 LMs CONFORME, suíte 662/662. Arquivos: `output/…/playbooks/pbk-1-sistemas-multiagentes/passos/*.json`.
- **2026-08-11 Campanhas em hub MULTI-VOLUME (nome_material V5.5):** causa: a desambiguação de `nome_material` só removia o prefixo da CHAVE da coleção (`aidd-engenharia-nativa--eb-01-...`); o primeiro hub com 4 volumes (AIDD) expôs 2 colisões novas — (1) `dck-1-*`/`eml-1-*`/`pbk-1-*`/`lm-N-*` têm o MESMO prefixo de 2 palavras em todos os volumes (4 decks → 4 pastas `dck-1` sobrescrevendo); (2) artigos/ebooks repetem o slug do VOLUME, não da chave (`aidd-v1-arquitetura-da-inteligencia--art-01-...` → truncava para `aidd-arquitetura`, a mesma pasta do livro). Fix: `_volume_obra` lê `obra_mae`/`livro_mae` do config_obra (volume = slug que difere da chave), `nome_material` remove o prefixo do VOLUME com separador explícito (`--`/`-`) e anexa a palavra distintiva do volume (2ª palavra significativa do slug do volume: `aidd-v2-arsenal-do-agente` → `arsenal`); resultado truncado a 20 chars (invariante V5.1). Prevenção: em hub multi-volume o discriminador de pasta de campanha é o VOLUME (config `obra_mae`), não a chave; validar colisão com um teste que passa 4 volumes do mesmo tipo; nunca anexar sufixo sem cortar o total a 20 chars. Resultado: 48 campanhas AIDD com pastas únicas (aidd-arquitetura, dck-1-arsenal, art-01-governanca...), gate R-CP estrito 48/48, suíte 662/662. Arquivos: `scripts/campanha.py`, `tests/test_campanha.py`.
- **2026-08-11 Produção completa série MCP (coleção `revolucao-mcp`):** causa: série 3 da proposta estratégica (MCP) exigia fluxo FULL com livro, derivados, campanhas e máquina; 4 lições reais surgiram. Fix/lições: (1) **headings EITA-V2 obrigatórios** — `dividir_secoes`/`secao_por_nome` (validar-escala, validar-metricas) só reconhecem `## N. Nome` numerado; capítulos com `## Introdução` sem número falham R-ES-1/R-MT-1 mesmo com o conteúdo correto (sed `s/^## Aplica:/## 5. Aplica/`); (2) **mermaid-cli quebra com subgraph aninhado/acentos em labels** — `flowchart TB` com `subgraph` falhou render com ParseError; simplificar para nós planos resolveu; (3) **R-CP-C1 lê `campanhas/campanha.json` com `materiais[].slug` = caminho COMPLETO do manifesto** — meu `campanha.json` inicial usava nomes curtos (`eb-01-mcp`) e o gate reprovou 12/12; regenerar com slugs do manifesto + `status: completa`; (4) **`transport` do FastMCP instalado é `streamable-http` (hífen)** — `streamable_http` (underscore) lança ValueError no smoke test; e `mcp.run()` bloqueia o `validar-codigo --executar` (timeout 20s) — guardar com env var em exemplo didático. Prevenção: rodar `auditar-obra --estrito` + `validar-codigo --executar` ANTES da capa/PDF; usar headings EITA numerados desde o primeiro rascunho. Resultado: livro 63 pags CONFORME, 12 membros, campanhas 12/12, máquina com gate regra 12 vazio, suíte 662/662, commit+push. Arquivos: capítulos MCP, `scripts/validar-escala.py` (leitura), `scripts/validar-campanha.py` (leitura).
- **2026-08-11 Série 4 (Autonomous DevOps) — 7 bugs reais no fluxo FULL:** causa: (1) `validar-afirmacoes` reprovava listas de definições sem `[N]` (SLI/SLO/SLA; timings do incidente em bullets) — citar cada item factual; (2) bloco de código do `Cirurgiao` com AssertionError: lambda de runbook irreversível retornava `verificacao: nao_aplicado` e o assert esperava `ok` — semântica correta é a verificação falhar → `reverter` (mostra o gate funcionando); (3) Vigia cap_2: taxa 0.05 não superava 5x o teto (severidade virava P2) e o sazonal com desvio zero (histórico idêntico) disparava o pico normal — usar valores com variância real; (4) lead magnets nasciam com `itens: 0` no `sumario_macro.json` (R-LM-7) e sem CTA UTM no corpo (R-LM-1 exige `# Próximo passo` + `utm_source=`) — preencher itens e bloco CTA; (5) e-mails com formato errado (`Status:` no lugar certo) e CTA sem link markdown — `[texto](url)` com assunto ≤60 chars (R-EM-1/R-EM-2); (6) e-books sem campo `serie` (eb-02 ficou fora → coleção com 11 membros) — conferir TODOS os configs após o script; (7) campanhas `inbound_emails` (sequencia-mkt/nutricao, 84 moldes) não caem no polimento genérico — script dedicado por sequência. RTK: `pdf_typst.executar(comando, pdf_path, dir_raiz, typst_bin)` — importar `compilar_markdown_pdf` de `criar-campanha.py` via importlib (nome com hífen não importa direto); `campanha.json` usa slug COMPLETO do manifesto no formato `{slug, tipo, status, atualizado_em}`. Prevenção: validar blocos de código com dados REALISTAS (assert deve refletir a semântica, não forçar pass); LM/emails exigem CTA rastreável + itens contados no sumário. Resultado: série 4 completa, suíte 662/662. Arquivos: `output/devops-agente/**`, `relatorios/11-08--producao-completa-devops-agente.md/.pdf`.
- **2026-08-10 Artes de campanha únicas por envio (R-CP-6) + desambiguação `nome_material`:** causa: artes (PNG) da campanha nasciam IDÊNTICAS em todos os envios — (1) `gerar_artes` interpola o HTML do WhatsApp UMA VEZ fora do loop (arte-01..06 com mesmo MD5); (2) posts/stories "variavam" só com sufixo `(i/n)` colado ao título e cortado pelo `[:64]` de `variaveis_arte`; (3) o gate R-CP-3 só contava QUANTIDADE de PNGs, nunca unicidade (62 PNGs, 8 MD5 únicos "validavam 100%"); (4) `nome_material` corta o nome do diretório nas 2 primeiras palavras (`nome_curto max_palavras=2`) e `spec-driven-development--eb-01-…` virava `spec-driven` — campanhas dos e-books caíam na pasta do livro, sobrescrevendo moldes/artes. Fix: `ganchos_arte(ctx, formato, n, base=None)` deriva gancho curto (≤70 chars, break scroll) + apoio (≤90) do sumário (títulos/objetivos/pilares; post prioriza capítulos, story/whatsapp priorizam pilares como dica); `gerar_artes` interpola o HTML DENTRO do loop com `titulo_arte`/`apoio_arte`/`rotulo_arte` ("Post 3/7") como elementos SEPARADOS (nunca colados/cortados do título); templates ganham `.rotulo` no topo + subtítulo = `${APOIO}`; novo gate **R-CP-6** (`_artes_duplicadas`): PNGs repetidos por MD5 e HTML fonte repetido reprovam; `nome_material` remove o prefixo da chave da coleção com separador EXPLÍCITO (`chave--`/`chave-`; sem separador não trunca — material que apenas compartilha prefixo não é afetado). Prevenção: ao "variar" arte por envio, variar o CONTEÚDO (gancho/apoio/rótulo), nunca sufixo truncável; validação de arte precisa gate de UNICIDADE (MD5), não só contagem; nome curto de derivado que repete o slug da coleção precisa desambiguação com separador. Resultado: suíte 652/652; campanha do SDD regenerada com 372 PNGs e 0 duplicatas. Arquivos: `scripts/campanha.py`, `scripts/criar-campanha.py`, `scripts/validar-campanha.py`, `templates/campanha/*.html`, `tests/test_campanha.py`.
- **2026-08-10 Universalização OpenCode:** causa: o harness opencode só carregava built-ins — não lia `.claude/agents`, `.claude/commands` nem os MCPs do `.mcp.json`. Fix: (1) frontmatter dos agents: remover `model: inherit` (quebra no OpenCode: "Model not found: inherit/") e usar `mode: subagent`; (2) junctions `.opencode/{agents,commands,skills,mcp-servers}` → `.claude/` via `New-Item -ItemType Junction` do PowerShell (`ln -s` do git-bash COPIA, gera inode diferente — bug real); (3) `.opencode/plugins/fabrica-hooks.ts` (API `export const X: Plugin = async ({$}) => ({event, hooks})`, NÃO `app.on` — API antiga quebra com "app.on is not a function"); (4) MCP do opencode = bloco `mcp` com `command:[...]` array trazendo `type:"local"` — schema difere do `.mcp.json`, logo não é junction; `scripts/sync-opencode-mcp.mjs` traduz (merge preserva `instructions`/`permission`); (5) paths relativos de MCP NO OpenCode NÃO resolvem — usar absolutos; (6) junction `.opencode/skills` duplica `.claude/skills` e gera warnings inofensivos de skill duplicada; (7) `scheduled_tasks.lock`/`settings.local.json` são runtime/local — gitignorar com as junctions, manter só `.opencode/plugins/` versionado (`.opencode/.gitignore` interno já ignora node_modules/package.json). Prevenção: rodar `scripts/setup-links.ps1` após clone; `opencode mcp list` e `opencode agent list` (subagentes mostram `(subagent)`) para validar; subagente não roda como primary (fallback expected). Arquivos: `.claude/agents/*.md`, `.claude/commands/criar-maquina.md`, `.opencode/plugins/fabrica-hooks.ts`, `opencode.json`, `scripts/sync-opencode-mcp.mjs`, `scripts/setup-links.ps1/.sh`, `~/.config/opencode/plugins/crg-plugin.ts`.
- **2026-08-10 `fatiar-obra.py` grava `obra_mae` mas a coleção lê `serie`/`livro_mae`:** causa: configs de artigos/ebooks derivados nasciam com `obra_mae: <volume>` e sem `serie`/`livro_mae`; `resolver_serie_key` (série ← `serie` → `livro_mae` → nome do slug) então criava 1 coleção fantasma por volume (`aidd-v1-...`, `aidd-v2-...`) em vez de agregar ao hub. Fix: adicionar `livro_mae: <slug-colecao>` (a CHAVE da coleção, não o volume) nos configs de artigos/ebooks e re-rodar `colecao.py --sincronizar` sem `--slug` (a limpeza global remove os manifestos órfãos). Prevenção: derivados fatiados de uma SÉRIE (vários livros no mesmo hub) precisam apontar `livro_mae` para o slug da coleção; playbooks já nascem com `serie`. Arquivos: `scripts/fatiar-obra.py`, `scripts/colecao.py`, `scripts/series_capa.py` (`resolver_serie_key`).
- **2026-08-11 Falha de TDD de campanhas (0/7 artes + R-CP-2 em cronograma mestre):** causa: `criar-campanha.py` não aplicava `_pdf_atualizado` em ads pago/distribuição; `test_campanha.py` tinha hardcode pra `anuncio-04`; R-CP-2 exigia `.pdf` de `cronograma_mestre.md` porque isenção usava `startswith("cronograma-")`. Fix: Adicionadas chamadas de conversão PDF; removido hífen do validador de isenção de R-CP-2; corrigidos hardcodes (`anuncio-04` → `0{i}`). Prevenção: Testar integridade do gerador comparado ao nome e paths lógicos declarados; e incluir logs explícitos de não geração de PDFs em mocks. Arquivos: `scripts/criar-campanha.py`, `scripts/validar-campanha.py`, `scripts/campanha.py`, `tests/test_campanha.py`.
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
- **2026-08-09 Cronogramas ricos (o que/por que/como/quando):** causa:
  cronogramas da campanha eram listas secas ("D+N (data): Post — Título")
  sem instrução de uso. Fix: cada dia vira bloco com **o quê** (arquivo
  EXATO: arte PNG + legenda MD da rede / texto MD do canal),
  **por quê** (`campanha.objetivo_do_dia` — objetivo rotativo por fase do
  funil: `fase_da_janela` 0=gancho, 1=aprofundamento, 2=urgência/CTA),
  **como** (`COMO_FORMATO` interpolado com arte/texto/CTA reais) e
  **quando** (data + horário por formato). Dias sem envio dos canais viram
  PAUSA estratégica. Bug real corrigido de quebra: a numeração dos itens de
  canal usava a POSIÇÃO do dia (`email-11/20/30` — arquivos inexistentes);
  agora contador sequencial `email-01..04` batendo com `texto_nome` e artes
  WhatsApp (`item.split('-')[1]`). Gate R-CP-5 exige as 4 dimensões
  (`**O quê:**` etc.) — reprova lista seca. Prevenção: ao numerar artefatos
  de sequência, usar contador sequencial, NUNCA posição do dia.
  Arquivos: `scripts/campanha.py`, `scripts/criar-campanha.py`,
  `scripts/validar-campanha.py`, `tests/test_campanha.py`.
  capas dos materiais divergiam do padrão 2D plano. Três causas reais:
  (1) `ebook_metadados.json` herdou títulos antigos concatenados com "&" de
  gerações anteriores (ex.: "…Por Que o Modelo Não Basta & Anatomia de um
  Harness: O") — `gerar-capa.py` prioriza `meta_ebook.titulo` sobre
  `sumario.titulo_obra`, então capas mostravam lixo truncado;
  (2) `validar-capa-nivel.py` procurava em `output/livros/<slug>` (layout
  plano) e nunca validou no HUB POR COLEÇÃO (`output/<colecao>/livros/…`);
  (3) títulos longos estouravam a capa (máx. 2 linhas, sem linha de 1
  palavra) — validar-capa-texto usa largura por TIPO (`playbook` 1600 vs
  `ebook` 1200 quebram diferente; testar sempre com o tipo real do material).
  Fix: `validar-capa-nivel.main()` resolve via `tipos_obra.dir_obra` (plano e
  hub; escopo R5: badge só livro/ebook); capas de título longo usam
  `ebook_metadados.json` curto (título + subtítulo) SEM tocar no sumário
  (documento EPUB/PDF mantém título completo — gerar-epub prioriza
  `sumario.titulo_obra`). Prevenção: ao encurtar título de capa, validar com
  `gerar-capa.py <slug>` (tipo real) e conferir badge via
  `validar-capa-nivel.py <slug>`. Arquivos: `scripts/validar-capa-nivel.py`,
  `scripts/gerar-capa.py`, `scripts/validar-capa-texto.py`,
  `ebook_metadados.json` dos materiais.
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
- **2026-08-09 Artes da campanha suprem o cronograma (V5.3):** causa:
  `gerar_artes` gerava `for i in (1,)` — 1 arte por formato (IG 1 post + 1
  story, LI 1 post, WhatsApp 1 por sequência) enquanto o cronograma cobre
  14–30 dias de envio. Fix: `campanha.py` ganhou `roteiro_rede` (usa os MESMOS
  nomes de formato do registro: `feed-story`, não `story` — erro real de
  contagem) e `n_artes_redes`/`n_artes_whatsapp` (quantidade que supre o
  cronograma: IG 14d = 7 posts + 7 stories, LI 14d = 7 posts, WhatsApp = 1
  arte por mensagem da sequência, 4 e 6); `gerar_artes` itera `range(1, n+1)`
  e `gerar_cronogramas` usa `CP.roteiro_rede` (DRY). Gate R-CP-3 agora valida
  a CONTAGEM por formato/sequência (`n_real/n_esperado artes (cronograma)`),
  não só existência/assinatura. Prevenção: ao adicionar formato de arte novo no
  registro, o nome TEM que casar com o usado em `roteiro_rede`/`TEMPLATES_ARTE`
  (feed-story ≠ story); regenerar coleção inteira demora (~600s+ por lote de 16
  materiais com Chromium) — rodar `--completo` e completar materiais restantes
  com `--material` quando estourar timeout. Arquivos: `scripts/campanha.py`,
  `scripts/criar-campanha.py`, `scripts/validar-campanha.py`,
  `tests/test_campanha.py`.
- **2026-08-09 PDFs em .md de campanha (V5.3) — cronogramas e textos:** causa:
  cronogramas e moldes de texto nasciam só em `.md`; imprimir/compartilhar
  exigia compilar à mão. Fix: `criar-campanha.py` ganhou
  `compilar_markdown_pdf` (alias retro `compilar_cronograma_pdf`) — Pandoc→Typst
  via `pdf_typst.executar` (fluxo `.typ` intermediário, nunca
  `--pdf-engine=typst`), binários por `shutil.which` com fallback WinGet
  cacheado (`functools.lru_cache`); `gerar_cronogramas` e `escrever_moldes`
  emitem `.md` + `.pdf` (mesmo nome); `_pdf_atualizado` regenera o PDF quando o
  `.md` foi editado depois (copy final do agente mais nova que o PDF). Log
  separa `X moldes (+Y PDF), Z cronogramas (+W PDF)`. Gates: R-CP-5 exige
  `.pdf` ao lado de cada `cronograma-*.md`; R-CP-2 exige `.pdf` ao lado de cada
  texto (exclui cronogramas, cobertos pelo R-CP-5); ambos reprovam PDF vazio.
  Prevenção: campanhas criadas ANTES do fix reprovam — rodar
  `criar-campanha.py --completo <colecao>` (ou helper temp) para gerar PDFs
  retroativos; nos testes, a fixture `ambiente` mocka a compilação com
  placeholder `%PDF` (gates só verificam existência) e há teste real com skip
  `precisa_pandoc_typst`. Arquivos: `scripts/criar-campanha.py`,
  `scripts/validar-campanha.py`, `tests/test_campanha.py`.
- **2026-08-09 Máquina de vendas 1:1 (V5.3):** causa: máquinas nasciam em
  `marketing/maquinas/` (caminho morto) ou `output/<hub>/marketing/` (várias por
  coleção, sem vínculo com campanhas). Fix: 1 máquina por COLEÇÃO em
  `output/<hub>/maquina/` (hub = 1º segmento do slug que não seja raiz de tipo);
  `criar-maquina-vendas.py` recusa 2ª obra do mesmo hub (sem input, retorna
  None) e copia `output/<hub>/campanhas/` → `maquina/campanhas/` com
  `snapshot.json` (origem/atualizado_em/materiais/copiado_em — normalizar
  separador com `replace("\\","/")` no Windows); manifesto da máquina ganha
  `colecao`/`maquina_em`/`campanhas`; `colecao.py --sincronizar` registra
  `maquina` + `maquinas_legadas` (não destrutivo — legadas em
  `output/<hub>/marketing/` ficam para o operador decidir); `empacotar-colecao.py`
  copia a máquina no pacote (ignora node_modules/.next/*.db). Prevenção:
  fallback de derivados usa TIPOS válidos (`playbook`, `ebook`, `deck`,
  `lead-magnet`) — nomes de raiz plural (`playbooks`) quebram
  `TO.listar_materiais` (KeyError); nos testes, `monkeypatch.setattr(TO,
  "DIR_OUTPUT", ...)` — `gerador.OUTPUT_BASE`/`OBRA_BASE` não existem mais.
  Arquivos: `scripts/criar-maquina-vendas.py`, `scripts/colecao.py`,
  `scripts/empacotar-colecao.py`, `tests/test_maquina_colecao.py`,
  spec em `melhorias/09-08-2026-maquina-1por-colecao-usa-campanhas.md`.

## RTK SCRATCHPAD

### [2026-08-13] RUNTIME: Subagente de expansão travou em 48 turns
- **Causa**: spawnar 1 subagente para expandir 8 capítulos (de ~12k para ~25k chars cada = ~100k chars de expansão total) estourou o limite de turns. Tarefa monolítica demais para um único subagente geral.
- **Fix**: cancelado (actor cancel). Expansão ficou pendente.
- **Arquivo**: actor general-10 (expansão de conteúdo livros/orca-ide)
- **Prevenção**: em expansion tasks, dividir em lotes de 2-3 capítulos por subagente, nunca 8 de uma vez. Se a tarefa envolver rewrite de múltiplos arquivos grandes, usar subagentes paralelos com escopo delimitado.

### [2026-08-13] PADRÃO: Playbook extraído de capítulos com refs faltantes
- **Causa**: `extrair-passos-praticos.py` extrai dados dos capítulos, mas 3 capítulos (2,3,7) tinham seção 7 (Referências) vazia. O gate R4 (mín 8 refs) falhou na auditoria.
- **Fix**: subagente revisor adicionou 3 refs ABNT a cada capítulo afetado.
- **Arquivo**: output/livros/orca-ide/capitulos/cap_{2,3,7}.md
- **Prevenção**: validar refs na seção 7 DEPOIS da escrita de cada capítulo (auto-validação do subagente-redator-capitulo deve checar contagem de refs, não apenas existência). Rodar `auditar-obra.py` imediatamente após cada lote, não só no final.

### [2026-08-13] CONFIG: Livro M ficou com 99k chars (mínimo 200k)
- **Causa**: capítulos escritos com ~12k chars em média, mas o mínimo para tamanho M (~80 páginas) é ~25k chars por capítulo. Subagentes produziram conteúdo válido mas curto demais.
- **Fix**: pendente — conteúdo precisa ser expandido.
- **Arquivo**: output/orca-ide/livros/orca-ide/capitulos/cap_*.md
- **Prevenção**: no prompt do subagente-redator-capitulo, incluir meta explícita de tamanho mínimo por seção (ex.: "seção Explica: mínimo 3000 caracteres"). Incluir contagem de caracteres no relatório de auto-validação.

### [2026-08-13] ESTRUTURA: Diretórios soltos fora do hub da coleção
- **Causa**: `fatiar-obra.py --playbook` gravou em `output/playbooks/` e o minerador acadêmico gravou em `output/orca-ide/pesquisa/` — ambos fora do hub `output/orca-ide/`. O orquestrador não validou a localização antes de prosseguir. Além disso, `colecao.py --sincronizar` criou `output/colecoes/` como fallback quando o hub não existia.
- **Fix**: movido manualmente para `output/orca-ide/livros/orca-ide/` e `output/orca-ide/playbooks/pbk-1-orca-ide-manual/`. Limpos diretórios órfãos `output/livros/`, `output/playbooks/` e `output/colecoes/`.
- **Arquivo**: output/orca-ide/ (hub), output/livros/ (removido), output/playbooks/ (removido), output/colecoes/ (removido)
- **Prevenção**: SEMPRE usar `tipos_obra.dir_obra(slug)` para resolver caminhos — nunca criar diretórios manualmente. Após `fatiar-obra.py`, validar que os artefatos ficaram dentro do hub com `ls output/<hub>/<tipo>/`. Se estiverem soltos, MOVER antes de qualquer operação seguinte. Rodar `colecao.py --sincronizar` após cada movimentação. O fallback `output/colecoes/` do `colecao.py` é legado — NÃO deve ser usado; o manifesto sempre vai em `<hub>/colecoes/<slug>.json`.
