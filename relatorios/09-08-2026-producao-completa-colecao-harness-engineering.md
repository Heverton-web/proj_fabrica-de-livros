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
- `relatorios/09-08--producao-completa-colecao-harness-engineering.md/.pdf`

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

## 9. PDFs em .md de campanha — cronogramas e textos — complemento

Todo `.md` da campanha agora sai com `.pdf` ao lado (Pandoc→Typst via
`pdf_typst.executar`, fluxo `.typ` intermediário). `compilar_markdown_pdf`
(alias retro `compilar_cronograma_pdf`) em `criar-campanha.py` resolve
pandoc/typst por `shutil.which` com fallback WinGet cacheado;
`gerar_cronogramas` e `escrever_moldes` emitem `.md` + `.pdf` (mesmo nome);
`_pdf_atualizado` regenera o PDF quando o `.md` foi editado depois (reflete a
copy final do agente). Log separa `X moldes (+Y PDF), Z cronogramas (+W PDF)`.
Gates: R-CP-5 exige `.pdf` de cada `cronograma-*.md`; R-CP-2 exige `.pdf` de
cada texto. **512 PDFs gerados** retroativamente na coleção harness-engineering
(416 textos 14 KB cada + 96 cronogramas 20 KB cada);
`validar-campanha.py --completo --estrito` CONFORME. 5 testes novos
(placeholder determinístico + gates sem PDF + compilação real com skip
`precisa_pandoc_typst`): **595 testes pytest passando**. RTK atualizado no
AGENTS.md.

## 10. Artes que suprem o cronograma — correção

Bug real: `gerar_artes` gerava `for i in (1,)` — **1 arte por formato**
(Instagram 1 post + 1 story, LinkedIn 1 post, WhatsApp 1 por sequência),
enquanto o cronograma cobre 14–30 dias de envio. Fix:
`campanha.py` ganhou `roteiro_rede` (usa os MESMOS nomes de formato do
registro: `feed-story`, não `story` — erro real de contagem) e
`n_artes_redes`/`n_artes_whatsapp` (quantidade que supre o cronograma:
IG 14d = 7 posts + 7 stories, LI 14d = 7 posts, WhatsApp = 1 arte por
mensagem da sequência: 4 e 6). `gerar_artes` itera `range(1, n+1)` e
`gerar_cronogramas` usa `CP.roteiro_rede` (DRY). Gate R-CP-3 agora valida a
CONTAGEM por formato/sequência (`n_real/n_esperado artes (cronograma)`).

**Regeneração completa da coleção**: **496 PNGs** = 16 materiais × 31 artes
(7 IG post + 7 IG story + 7 LI post + 4 WhatsApp nutrição + 6 WhatsApp
divulgação), renderizados com Chromium real (lote de 16 materiais +
complemento de 2 com timeout). `validar-campanha.py --completo --estrito`
CONFORME. 3 testes novos (quantidade por cronograma, gate insuficiente IG,
gate insuficiente WhatsApp; fixture mocka `_renderizar_png` com placeholder):
**598 testes pytest passando**. RTK atualizado no AGENTS.md.

## 11. Capas no padrão do projeto — correção (R5)

Queixa: capas dos materiais não seguiam o padrão 2D plano da Editora
Agêntica. Causas reais encontradas:

1. **Títulos antigos concatenados nos 4 `ebook_metadados.json`** — ex.:
   eb-01 tinha "A Revolução dos Agentes: Por Que o Modelo Não Basta & Anatomia
   de um Harness: O" (concatenação de 2 capítulos com "&"), herdada de uma
   geração anterior. O `gerar-capa.py` prioriza `meta_ebook.titulo` antes do
   `sumario.titulo_obra` — as capas mostravam o texto truncado. Fix: títulos
   curtos do sumário gravados nos 4 metadados + capas regeneradas.
2. **`validar-capa-nivel.py` quebrado no HUB POR COLEÇÃO** — procurava em
   `output/livros/<slug>` (layout plano), nunca no hub
   `output/<colecao>/livros/<slug>`; o gate nunca validou de verdade. Fix:
   `main()` resolve via `tipos_obra.dir_obra` (aceita plano e hub) e mantém o
   escopo R5 (badge obrigatório só em livro/ebook).
3. **Títulos ainda estourando em 3 capas** (máximo 2 linhas, sem linha de 1
   palavra): eb-01 ("A Revolução dos Agentes e a Anatomia do Harness" → 3
   linhas), playbook ("PLAYBOOK — … — … CONFIÁVEL" → 3 linhas) e lm-6
   ("MINI-GUIA: … AUTÔNOMO" → linha com 1 palavra). Fix: capa usa metadata
   curto (`ebook_metadados.json`) com título + subtítulo — documento
   (sumário/EPUB/PDF) mantém o título completo. O validar-capa-texto precisa
   do **tipo real** (`playbook` usa largura 1600 vs `ebook` 1200 — quebra
   diferente; testar sempre com o tipo do material).

Resultado: **13/13 capas conformes** em `validar-capa-texto` + badge
"PARA INICIANTES" OK (livro + 4 e-books via hub) + inspeção visual no
browser APROVADA (sem cortes, hierarquia clara). 598 testes pytest passando.
LOTE 01 sincronizado.

## 12. Cronogramas ricos — o que / por que / como / quando

Queixa: cronogramas eram listas secas ("D+N (data): Post — Título") sem
instrução de uso. Fix: cada dia agora é um bloco com as **4 dimensões**:

- **O quê:** arquivo EXATO a publicar (arte PNG + legenda MD da rede; texto
  MD do canal — ex.: `artes/post/post-01.png` + `textos/post/post-01.md`)
- **Por quê:** objetivo do envio no funil, rotativo por fase da janela
  (`campanha.fase_da_janela`: 0=gancho, 1=aprofundamento, 2=urgência/CTA;
  `objetivo_do_dia` alterna variações por fase)
- **Como:** passo a passo do formato (`COMO_FORMATO` interpolado com
  arte/texto/CTA reais — hashtags, sticker de enquete, pre-header, horário)
- **Quando:** data + horário sugerido por formato (`HORARIO_FORMATO`: post
  9h, story 12h/18h30, e-mail 9h, WhatsApp 10-11h)

Cabeçalho ganhou seção **Como usar** + resumo do roteiro. Dias sem envio nos
canais viram **PAUSA estratégica** (por quê = frequência calculada; como =
ações concretas de manutenção: responder interações, repostar, preparar o
próximo envio).

**Bug real corrigido de quebra:** a numeração dos itens dos canais usava a
POSIÇÃO do dia (email-11/20/30 em janela de 30 dias) — arquivos que nunca
existiram. Agora usa contador sequencial (email-01..04), batendo com
`texto_nome` e com as artes do WhatsApp (`arte-NN.png` via `item.split`).

**Gate R-CP-5 estendido:** exige `**O quê:**`/`**Por quê:**`/`**Como:**`/
`**Quando:**` em todo cronograma (reprova lista seca).

**96/96 cronogramas regenerados** (MD+PDF) na coleção harness-engineering;
`validar-campanha --completo --estrito` CONFORME; 3 testes novos
(dimensões por dia, envio+pausa nos canais, gate sem dimensões):
**601 testes pytest passando**. RTK atualizado no AGENTS.md.

## 13. Nota — sessão paralela e migração de nomenclatura V5.1

Após o commit `7f3522d` (cronogramas ricos), outra sessão trabalhou no
mesmo repositório em paralelo e pushou:

- `8de9cb3` — `scripts/migrar-slug.py` + `scripts/corrigir-nomenclatura.py`
  (nomes curtos V5.1, MAX_PATH 260)
- `4d948b4` — `campanha.nome_material` limitado a 20 chars via
  `nomes_curtos.nome_curto`

**Estado observado (sem intervenção, conforme decisão do operador):** a
mudança de `nome_material` quebrou temporariamente o gate de campanha
(R-CP-1: pastas ausentes em todos os materiais) porque as pastas reais de
campanha ainda têm nomes longos (`campanhas/harness-engineering--art-01-…`,
`pbk-1-harness-engineering-modelo` etc.) enquanto o código agora resolve
para `harness-engineering`, `pbk-1`, `lm-6`. O teste
`test_nome_material_pega_ultimo_segmento` também falha com essa mudança.

**Ação:** registrar aqui para a sessão de migração completar o serviço:
renomear as pastas de `output/<colecao>/campanhas/` para os nomes curtos
(resolver `NC.nome_curto(nome, max_palavras=2, maximo=20)`), atualizar
`campanha.json` (materiais) e o `LOTE 01`, e validar o gate R-CP-C1 voltar a
CONFORME. Ficou pendente também revalidar `601` testes.

*Relatório gerado em 2026-08-09 — Fábrica Agêntica de Publicações*
