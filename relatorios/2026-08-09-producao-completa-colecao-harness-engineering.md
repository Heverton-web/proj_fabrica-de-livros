# RELATÓRIO DE SESSÃO — Producao Completa Colecao Harness Engineering

> **Data:** 2026-08-09
> **Projeto:** Fábrica Agêntica de Publicações
> **Comando:** `/produzir-obra-completa harness-engineering`

---

## 1. Contexto

Produção da coleção completa do tema **Harness Engineering** (V5): livro (8 caps) + 2 artigos IMRaD + 4 e-books + playbook (8 cards) + 6 lead magnets + deck (14 slides) + sequência de 10 e-mails + campanhas (V5.3) + máquina de vendas (V5.3, 1 por coleção). Núcleo canônico: `output/harness-engineering/` (HUB POR COLEÇÃO). Entrega final versionada em `LOTE 01/harness-engineering/`.

## 2. Bugs Descobertos e Corrigidos

0. **Layout de output fora do padrão HUB POR COLEÇÃO (correção pós-entrega)** — os materiais foram inicialmente gravados em raízes planas (`output/livros/`, `output/artigos/`, `output/ebooks/`, `output/playbooks/`, `output/lead-magnets/`, `output/decks/`, `output/emails/`, `output/colecoes/`), mas o AGENTS.md exige `output/<slug-colecao>/` com as raízes DENTRO do hub. Fix: tudo migrado para `output/harness-engineering/{livros,artigos,ebooks,playbooks,lead-magnets,decks,emails,colecoes,distribuicao}/`; derivados nomes-curtos perderam o nível de código-obra (`playbooks/pbk-1-…` em vez de `playbooks/harness/pbk-1-…`); `tipos_obra.dir_obra` resolve os dois layouts (verificado: todos os slugs antigos continuam resolvendo); manifesto re-sincronizado no hub (`colecoes/harness-engineering.json`), `validar-artefatos --todos --estrito` re-rodado (16/16 abrem, 0 arriscados) e pacote re-empacotado em `harness-engineering/distribuicao/`. `LOTE 01/harness-engineering/` recopiado do hub (mesma estrutura).

1. **Playbook quebrado após regeneração** — `extrair-passos-praticos.py` regenerou os 8 JSONs do zero (sem gate/entregas/código curto) e o backup correto estava em `/tmp` (inacessível ao Python Windows). Fix: restaurado de `/tmp/pbk_passos_backup` (8 passos ≤25 linhas), remontado `playbook.md` via `montar_markdown`; validar-playbook CONFORME + validar-codigo --playbook 100%.
2. **Lead magnets sem CTA** — `cta_url` vazio e corpo sem UTM. Fix: herdada cta_url do config do livro + bloco `# Próximo passo` com utm_source/utm_medium/utm_campaign; lm-2 (cheatsheet) e lm-4 (entregas) estavam vazios — escrita de conteúdo real (12 comandos, 8 entregas). 6/6 CONFORME.
3. **Títulos de e-books estourando a capa** (4-5 linhas, máximo 2) — títulos concatenavam 2 capítulos com "&". Fix: títulos curtos aprovados por `validar-capa-texto` (ex.: "A Revolução dos Agentes e a Anatomia do Harness"); capas e EPUBs regenerados.
4. **Caminhos perto do MAX_PATH (235-237 chars)** — arquivos de saída `.epub`/`.pdf` duplicavam o slug longo como nome de arquivo. Fix: renomeados para `eb-01.epub`/`art-01.pdf` → 0 caminhos arriscados.
5. **10 marcadores POLIMENTO-LLM nos e-mails** — Fix: copy final em segunda pessoa (≤90 palavras) conectando armadilha→passo prático; `sequencia.md` regenerado (0 marcadores).
6. **Docstrings com 4 aspas (`""""`) nos cards do playbook** — heredoc com aspas aninhadas. Fix: códigos dos passos 03/04/06 reescritos com docstring correto; gate 100%.
7. **Produto default do checkout desalinhado do config** — a rota `/api/checkout` nascia com `default("livros/harness-engineering")` mas o 1º produto do `config/produtos.json` é `livro-harness-engineering`. Fix: alinhado ao config (aprendizado RTK 2026-08-09 — produto default deve casar com `produtos.json`); leads de teste vivem em `backend/data/vendas.db`.

## 3. Arquivos Alterados

- `output/livros/harness-engineering/` — livro + capa (71 KB) + PDF (115 págs, 1.9 MB)
- `output/artigos/harness-engineering--art-01…/` e `--art-02…/` — 4 seções IMRaD + metadados + PDF (169/158 KB)
- `output/ebooks/harness-engineering--eb-01…/` … `--eb-04…/` — capítulos + metadados + capas (72-84 KB) + EPUB (96-109 KB)
- `output/playbooks/harness/pbk-1-harness-engineering-modelo/` — 8 cards corrigidos + playbook.md + capa + PDF (339 KB, 20 págs)
- `output/lead-magnets/harness/lm-1…lm-6/` — conteúdo + CTA/UTM + PDFs (96-181 KB) + cards sociais (79-85 KB)
- `output/decks/harness/dck-1-harness-engineering-modelo/` — HTML (18 KB) + PDF (124 KB, 14 págs) + capa
- `output/emails/harness/eml-1-harness-engineering-modelo/` — 10 e-mails polidos + sequencia.md
- `output/colecoes/harness-engineering.json` — manifesto sincronizado (16 membros)
- `output/distribuicao/harness/` — pacote de distribuição (18 arquivos, 4.1 MB, LEIA-ME + LICENCA)
- `LOTE 01/harness-engineering/` — entrega versionada (artigos, ebooks, playbooks, lead-magnets, decks, emails, livros, colecoes, campanhas, maquina)
- `output/harness-engineering/maquina/` — máquina de vendas 1:1 da coleção (frontend Next.js + backend FastAPI, 46 MB)
- `relatorios/2026-08-09-producao-completa-colecao-harness-engineering.md/.pdf`

## 4. Validações

- `python -m pytest -q` → **590 passed** em 65s
- `auditar-obra.py` (livro + 2 artigos + 4 e-books) → CONFORME
- `validar-playbook.py` → CONFORME (8 passos, 0 violações) · `validar-codigo.py --playbook` → 100%
- `validar-lead-magnet.py --todos` → 6/6 CONFORME (PDFs medidos, CTA no rodapé)
- `validar-deck.py` → CONFORME (13 slides) · `validar-emails.py` → CONFORME (0 pendentes)
- `validar-capa-texto.py` → APROVADO em livro, 4 e-books, playbook, deck
- `validar-capa-nivel.py` → badge "PARA INICIANTES" OK em livro + 4 e-books
- `validar-artefatos.py --todos --estrito` → **16/16 abrem · 0 falhas · 0 caminhos arriscados**
- `colecao.py --sincronizar` → 16 membros · `empacotar-colecao.py harness-engineering` → 18 arquivos, 4048 KB
- Inspeção visual no browser das 13 capas → todas APROVADAS (sem texto cortado, hierarquia clara, quebra de título correta, badges consistentes)
- `criar-maquina-vendas.py` → máquina criada (1036 arquivos + snapshot 16 campanhas + banco SQLite)
- Gate personalização por nicho: `grep 'Autor Digital|centenas de pessoas'` → **0 ocorrências** (copy de harness engineering em 8 pontos: configs, frontend, e-mails, README)
- Checkout alinhado: rota `/api/checkout` (zod + fetch JSON → `/api/leads/`) + `produto` default `livro-harness-engineering` == `config/produtos.json`; backend com `/api/leads`, `/api/emails`, `/api/funil`, `/api/webhooks`, `/health`

## 5. Commits

- `feat(colecao): producao completa harness-engineering — livro, 2 artigos, 4 ebooks, playbook, 6 lead magnets, deck, 10 emails`

## 6. Resumo de Entregas

| Tipo | Qtd | Artefato final |
|---|---|---|
| Livro | 1 (8 caps) | `harness-engineering.pdf` (115 págs) |
| Artigos | 2 (IMRaD) | `art-01.pdf`, `art-02.pdf` |
| E-books | 4 | `eb-01.epub` … `eb-04.epub` |
| Playbook | 1 (8 cards) | `pbk-1-harness-engineering-modelo.pdf` (20 págs) |
| Lead magnets | 6 | PDFs + cards sociais |
| Deck | 1 (14 slides) | HTML + PDF |
| E-mails | 10 (18 dias) | `sequencia.md` |
| Campanhas | 16 materiais (929 arquivos) | R-CP-C1 CONFORME + 80 artes PNG + 416 moldes com copy final |
| Pacote | — | `distribuicao/harness/` (18 arquivos) |
| Máquina de vendas | 1 (1:1 por coleção) | `maquina/` — Next.js + FastAPI, copy por nicho, snapshot campanhas |

## 7. Camada CAMPANHA (V5.3) — complemento

`criar-campanha.py --completo harness-engineering`: 16 materiais do manifesto
com estrutura (24 pastas cada), 416 moldes de texto reescritos com copy final
(Status FINAL, vocabulário condutor — arnês, corda, ancoragem, mosquetão, queda,
proteção, alavancagem, rota, parede, cume —, badge e CTA), 80 artes PNG
(Chromium; IG post/story, LinkedIn, WhatsApp) e cronogramas com datas reais.
`campanha.json` no hub registra os 16 materiais como `completa`.

`validar-campanha.py --completo harness-engineering --estrito` → **CONFORME**
(R-CP-C1 + R-CP-1..5 + R-CP-4 vocabulário). Inspeção visual no browser das
artes (IG post/story, LinkedIn, WhatsApp, playbook, lead magnets, deck) →
todas APROVADAS (hierarquia clara, badge visível, sem cortes).

## 8. Máquina de Vendas (V5.3) — complemento

`criar-maquina-vendas.py 'livros/harness-engineering'` (1 máquina por COLEÇÃO,
regra 1:1): frontend Next.js + backend FastAPI em
`output/harness-engineering/maquina/`, com snapshot das 16 campanhas da
coleção em `maquina/campanhas/` (`snapshot.json`), manifesto da máquina com
`colecao`/`maquina_em`/`campanhas` e registro `maquina` no manifesto da coleção
via `colecao.py --sincronizar`.

Personalização por nicho (engenharia de software / IA agêntica) em 8 pontos:
configs (`produtos.json` com `livro-harness-engineering` como produto 1,
`personas.json`, `funis.json`, `canais.json`, `email.json`), copy do frontend
(Hero, PricingCard, captura, layout/admin), e-mails (`templates/emails/`),
README e conteúdo (`conteudo/` com livro, artigos, ebooks, lead magnets,
playbook e deck da coleção). Gate da regra 12: `grep 'Autor Digital|centenas
de pessoas'` → **0 ocorrências**.

Checkout: rota `/api/checkout` com zod + `POST /api/leads/` + `BACKEND_URL`;
produto default `livro-harness-engineering` alinhado ao `config/produtos.json`;
backend com routers `/api/leads` (CRUD + mover), `/api/emails`, `/api/funil`,
`/api/webhooks` e `/health`. 590 testes pytest passando.

## 9. Cronogramas em PDF — complemento

Os cronogramas da campanha agora saem em `.md` + `.pdf` (Pandoc→Typst via
`pdf_typst.executar`, fluxo `.typ` intermediário). `compilar_cronograma_pdf`
em `criar-campanha.py` resolve pandoc/typst por `shutil.which` com fallback
WinGet cacheado; `gerar_cronogramas` emite ambos os formatos e o log separa
`X cronogramas (+Y PDF)`. Gate R-CP-5 exige o `.pdf` ao lado de cada
`cronograma-*.md`. **96/96 PDFs gerados** retroativamente na coleção
harness-engineering (20 KB cada); `validar-campanha.py --completo --estrito`
CONFORME. 3 testes novos (placeholder determinístico na fixture + gate sem PDF
+ compilação real com skip `precisa_pandoc_typst`): **593 testes pytest
passando**. RTK registrado no AGENTS.md.

*Relatório gerado em 2026-08-09 — Fábrica Agêntica de Publicações*
