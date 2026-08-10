# RELATÓRIO DE OUTPUTS — FÁBRICA AGÊNTICA DE PUBLICAÇÕES

**Mapeamento completo dos arquivos e pastas gerados em cada fluxo**

> **Autor:** Heverton Eduardo Peres
> **Versão:** V5.3 (HUB por Coleção / Campanhas / Máquina de Vendas)
> **Data:** 2026-08-10

---

# SUMÁRIO

1. Fluxo 1 — Criação de Materiais
2. Fluxo 2 — Criação de Campanha de Marketing
3. Fluxo 3 — Criação da Máquina de Vendas
4. Mapa consolidado por tipo de arquivo
5. Estrutura completa do HUB por Coleção

---

# FLUXO 1 — CRIAÇÃO DE MATERIAIS

O fluxo de criação de materiais produz até **10 tipos de obra** a partir de um único
tema, dividido em 5 fases (0 a 4). Cada fase entrega outputs incrementais.

---

## Fase 0 — Esboço e Parametrização

**Comando:** `/esbocar <tema>`

| Arquivo gerado | Caminho | Descrição |
|---|---|---|
| `config_obra.json` | `output/<colecao>/livros/<slug>/` | Parâmetros da obra (tipo, senioridade, tamanho, derivados, CTA) |

---

## Fase 1 — Pesquisa e Arquitetura

**Comandos:** `indexar-dossie.py --indexar`, skill `pesquisador`, skill `arquiteto`

| Arquivo / Pasta gerada | Caminho | Descrição |
|---|---|---|
| `pesquisa/` (pasta) | `output/<colecao>/livros/<slug>/pesquisa/` | Dossiê de pesquisa — fontes, textos indexados, referências |
| `sumario_macro.json` | `output/<colecao>/livros/<slug>/` | Arquitetura completa da obra (partes, capítulos, marcos EITA/ACAD) |
| `derivados.json` | `output/<colecao>/livros/<slug>/` | Registro de artigos e e-books fatiados a partir do livro-mãe |

---

## Fase 2 — Manufatura de Capítulos

**Comandos:** `pool-capitulos.py --plano --lote 4`

| Arquivo / Pasta gerada | Caminho | Descrição |
|---|---|---|
| `capitulos/cap_<N>.md` | `output/<colecao>/livros/<slug>/capitulos/` | Capítulo redigido (framework EITA-V2: 7 seções) |
| `estado_obra.json` | `output/<colecao>/livros/<slug>/` | Estado atual da manufatura por capítulo |

---

## Fase 2.5 — Revisão Técnica (Gates F1/F2)

**Comandos:** `auditar-obra.py`, `validar-codigo.py`, `renderizar-diagramas.py --validar`

| Arquivo / Pasta gerada | Caminho | Descrição |
|---|---|---|
| `validacao/` (pasta) | `output/<colecao>/livros/<slug>/validacao/` | Relatórios dos gates de conteúdo (R-RF, R-MT, R-ES, R-AF, R-FT) |
| `imagens/diagramas/` | `output/<colecao>/livros/<slug>/imagens/` | Diagramas Mermaid renderizados em PNG |
| `imagens/cap_<N>_ilustracao.png` | `output/<colecao>/livros/<slug>/imagens/` | Ilustrações 2D flat por capítulo |
| `imagens/capa.png` | `output/<colecao>/livros/<slug>/imagens/` | Capa gráfica A4 (2D flat, badge de nível) |

---

## Fase 3 — Compilação e PDF

### 1.1 Livro (`/criar-livro`)

| Arquivo gerado | Caminho | Descrição |
|---|---|---|
| `livro-compilado.md` | `output/<colecao>/livros/<slug>/` | Markdown unificado de todos os capítulos |
| `<titulo>.pdf` | `output/<colecao>/livros/<slug>/` | PDF final ABNT (Pandoc → Typst): capa + CIP + sumário + capítulos + referências |
| `livro_final.pdf` | `output/<colecao>/livros/<slug>/` | Alias do PDF final |
| `<titulo>.epub` | `output/<colecao>/livros/<slug>/` | EPUB para leitores digitais |
| `<slug>.typ` | `output/<colecao>/livros/<slug>/` | Intermediário Typst (necessário para recompilação) |

**Exemplo real (coleção `oh-my`):**

```
output/oh-my/livros/oh-my/
├── livro-compilado.md     (251 KB)
├── livro_final.pdf         (3,7 MB — PDF ABNT final)
├── oh-my-pi.pdf            (3,7 MB — alias)
├── sumario_macro.json
├── derivados.json
├── config_obra.json
├── imagens/capa.png
└── capitulos/cap_01.md ... cap_N.md
```

---

### 1.2 TCC (`/criar-tcc`)

| Arquivo gerado | Caminho | Descrição |
|---|---|---|
| `tcc_metadados.json` | `output/<colecao>/tccs/<slug>/` | Resumo, palavras-chave, abstract, orientador, curso |
| `tcc-compilado.md` | `output/<colecao>/tccs/<slug>/` | Markdown unificado (seções ACAD) |
| `<titulo>.pdf` | `output/<colecao>/tccs/<slug>/` | PDF NBR 14724 (capa ABNT sóbria, folha de aprovação, sumário, referências NBR 6023) |

---

### 1.3 Artigo (`/criar-artigo`)

| Arquivo gerado | Caminho | Descrição |
|---|---|---|
| `artigo_metadados.json` | `output/<colecao>/artigos/<slug>/` | Título, resumo NBR 6028, keywords, autores |
| `_artigo_meta.md` | `output/<colecao>/artigos/<slug>/` | Markdown completo (seções IMRaD) |
| `livro_final.md` | `output/<colecao>/artigos/<slug>/` | Fonte Markdown (alias) |
| `<titulo-longo>.pdf` | `output/<colecao>/artigos/<slug>/` | PDF NBR 6022 (resumo + abstract + IMRaD + referências NBR 6023) |

**Exemplo real (coleção `oh-my` — 4 artigos gerados):**

```
output/oh-my/artigos/oh-my--art-01-que-coding/
├── _artigo_meta.md
├── artigo_metadados.json
├── livro_final.md
├── config_obra.json
└── oh-my-pi--art-01-o-que-e-um-coding-agent-e-por-que-voce-p.pdf
```

---

### 1.4 E-book (`/criar-ebook`)

| Arquivo gerado | Caminho | Descrição |
|---|---|---|
| `ebook-compilado.md` | `output/<colecao>/ebooks/<slug>/` | Markdown em tom comercial-leve |
| `livro-compilado.md` | `output/<colecao>/ebooks/<slug>/` | Cópia do texto-fonte (para referência) |
| `ebook.typ` | `output/<colecao>/ebooks/<slug>/` | Intermediário Typst |
| `ebook_metadados.json` | `output/<colecao>/ebooks/<slug>/` | Título, subtítulo, CTA |
| `<codigo-ebook>.pdf` | `output/<colecao>/ebooks/<slug>/` | PDF do e-book (tom comercial) |

**Exemplo real (coleção `oh-my` — 8 e-books gerados):**

```
output/oh-my/ebooks/
├── oh-my--eb-01-que-coding/
│   ├── ebook-compilado.md     (21 KB)
│   ├── ebook.typ              (31 KB)
│   ├── ebook_metadados.json
│   └── oh-my--eb-01-que-coding.pdf  (233 KB)
├── oh-my--eb-02-instalacao-primeiros/
...
└── oh-my--eb-08-memory-system/
```

---

### 1.5 Playbook (`/criar-playbook`)

| Arquivo gerado | Caminho | Descrição |
|---|---|---|
| `playbook.md` | `output/<colecao>/playbooks/<slug>--pbk/` | Markdown com todos os cards de bancada |
| `playbook.typ` | `output/<colecao>/playbooks/<slug>--pbk/` | Intermediário Typst |
| `playbook.pdf` | `output/<colecao>/playbooks/<slug>--pbk/` | PDF com cards de bancada |
| `passos/` (pasta) | `output/<colecao>/playbooks/<slug>--pbk/passos/` | Cards individuais por capítulo |
| `sumario_macro.json` | `output/<colecao>/playbooks/<slug>--pbk/` | Sumário herdado do livro-mãe |

**Exemplo real (coleção `oh-my`):**

```
output/oh-my/playbooks/pbk-1-oh-my/
├── playbook.md    (61 KB — cards de todos os capítulos)
├── playbook.pdf   (618 KB — PDF formatado para bancada)
├── playbook.typ   (70 KB)
├── config_obra.json
├── sumario_macro.json
└── passos/
```

---

### 1.6 Lead Magnet (`/criar-lead-magnet`)

Gera até **6 formatos**, cada um como trio de arquivos `.md` + `.typ` + `.pdf`:

| Formato | O que agrega | Mínimo de itens |
|---|---|---|
| `armadilhas` | Campo `armadilhas` dos cards do playbook | 6 |
| `cheat-sheet` | Comandos e atalhos da seção Técnica | 6 |
| `checklist` | Campo `feito_quando` (passos) dos cards | 6 |
| `entregas` | Campo `entregas` dos cards | 6 |
| `mapa-mental` | Estágios do `sumario_macro` | 3 |
| `mini-guia` | Seção Explica do capítulo indicado (com polimento, máx 180 palavras) | 1 |

**Exemplo real (coleção `oh-my` — 4 lead magnets gerados):**

```
output/oh-my/lead-magnets/
├── armadilhas-omp.md     (6,8 KB)
├── armadilhas-omp.pdf    (170 KB)
├── armadilhas-omp.typ    (16 KB)
├── cheat-sheet-omp.md    (5,5 KB)
├── cheat-sheet-omp.pdf   (212 KB)
├── checklist-omp.md      (4,9 KB)
├── checklist-omp.pdf     (206 KB)
├── mapa-mental-omp.md    (19 KB)
└── mapa-mental-omp.pdf   (165 KB)
```

---

### 1.7 Slide Deck (`/criar-deck`)

| Arquivo gerado | Caminho | Descrição |
|---|---|---|
| `index.html` | `output/<colecao>/decks/` | Deck HTML navegável 16:9 (tecla `F` = fullscreen) |
| `deck.pdf` | `output/<colecao>/decks/` | PDF 16:9 exportado via Chromium |
| `gerar-pdf.mjs` | `output/<colecao>/decks/` | Script de exportação HTML para PDF |

**Exemplo real (coleção `oh-my`):**

```
output/oh-my/decks/
├── index.html    (31 KB — deck completo navegável)
└── gerar-pdf.mjs (844 bytes)
```

---

### 1.8 Sequência de E-mails (`/criar-emails`)

| Arquivo gerado | Caminho | Descrição |
|---|---|---|
| `01-boas-vindas.md` | `output/<colecao>/emails/` | E-mail de abertura da sequência |
| `02-conteudo-valor.md` | `output/<colecao>/emails/` | E-mail de valor (conteúdo educativo) |
| `03-cases-uso.md` | `output/<colecao>/emails/` | E-mail de casos de uso / prova social |
| `04-dicas-avancadas.md` | `output/<colecao>/emails/` | E-mail de dica avançada |
| `05-oferta-cta.md` | `output/<colecao>/emails/` | E-mail de oferta e chamada para ação |
| `sequencia-emails.md` | `output/<colecao>/emails/` | Markdown consolidado com todos os e-mails e cronograma |
| `sequencia-emails.pdf` | `output/<colecao>/emails/` | PDF da sequência (Pandoc → Typst) |
| `sequencia-emails.typ` | `output/<colecao>/emails/` | Intermediário Typst |

**Exemplo real (coleção `oh-my`):**

```
output/oh-my/emails/
├── 01-boas-vindas.md      (1,5 KB)
├── 02-conteudo-valor.md   (1,9 KB)
├── 03-cases-uso.md        (2,3 KB)
├── 04-dicas-avancadas.md  (2,5 KB)
├── 05-oferta-cta.md       (2,1 KB)
├── sequencia-emails.md    (11 KB — consolidado + cronograma)
├── sequencia-emails.pdf   (185 KB)
└── sequencia-emails.typ   (20 KB)
```

---

### 1.9 Manifesto de Coleção (`/colecao`)

| Arquivo gerado | Caminho | Descrição |
|---|---|---|
| `<nome-colecao>.json` | `output/<colecao>/colecoes/` | Manifesto com todos os membros, tipo, estado, CTA, badge |

---

## Resumo — Contagem de arquivos (coleção `oh-my`)

| Material | Arquivos entregáveis | Formatos |
|---|---|---|
| Livro-mãe | 2 (PDF + MD compilado) | `.pdf`, `.md`, `.epub` |
| Artigos (×4) | 4 PDFs + 4 MDs | `.pdf`, `.md` |
| E-books (×8) | 8 PDFs + 8 MDs | `.pdf`, `.md` |
| Playbook | 1 PDF + 1 MD | `.pdf`, `.md` |
| Lead Magnets (×4) | 4 PDFs + 4 MDs | `.pdf`, `.md` |
| Deck | 1 HTML navegável | `.html` |
| E-mails | 1 PDF + 5 MDs individuais + 1 MD consolidado | `.pdf`, `.md` |
| **TOTAL** | **~45 arquivos entregáveis** | |

---

# FLUXO 2 — CRIAÇÃO DE CAMPANHA DE MARKETING

O fluxo de campanhas gera materiais de divulgação completos para **cada material da
coleção** nas principais redes sociais e canais de comunicação.

**Comando:** `python scripts/criar-campanha.py --material <slug>` ou `--completo <colecao>`

---

## Estrutura gerada por campanha

Para cada material da coleção:

```
output/<colecao>/campanhas/<material-slug>/
│
├── redes-sociais/
│   ├── instagram/
│   │   ├── artes/
│   │   │   ├── feed-story/            (Stories 1080×1920 px)
│   │   │   │   ├── arte-01.png
│   │   │   │   └── arte-N.png
│   │   │   └── post/                  (Feed 1080×1350 px)
│   │   │       ├── arte-01.png
│   │   │       └── arte-N.png
│   │   ├── textos/                    (Legendas + hashtags)
│   │   │   ├── post-01.md
│   │   │   └── post-N.md
│   │   ├── templates/                 (HTML editável das artes)
│   │   │   └── arte-N.html
│   │   └── cronograma-divulgacao/
│   │       ├── cronograma.md          (4 dimensões: o quê/por quê/como/quando)
│   │       └── cronograma.pdf
│   │
│   └── linkedin/
│       ├── artes/post/                (1200×628 px)
│       │   └── arte-N.png
│       ├── textos/
│       │   └── artigo-01.md           (Artigo ou post longo)
│       ├── templates/
│       └── cronograma-divulgacao/
│           ├── cronograma.md
│           └── cronograma.pdf
│
├── canais-comunicacao/
│   ├── emails/
│   │   ├── sequencia-mkt/             (E-mails de marketing/lançamento)
│   │   │   ├── textos/
│   │   │   │   ├── email-01.md
│   │   │   │   └── email-N.md
│   │   │   ├── templates/
│   │   │   └── cronograma-divulgacao/
│   │   │       ├── cronograma.md
│   │   │       └── cronograma.pdf
│   │   └── sequencia-nutricao/        (E-mails de nutrição pós-captura)
│   │       ├── textos/
│   │       └── cronograma-divulgacao/
│   │
│   └── whatsapp/
│       ├── sequencia-divulgacao/
│       │   ├── artes/                 (1080×1080 px)
│       │   │   └── arte-N.png
│       │   ├── textos/
│       │   │   └── mensagem-N.md
│       │   └── cronograma-divulgacao/
│       │       ├── cronograma.md
│       │       └── cronograma.pdf
│       └── sequencia-nutricao/
│           ├── textos/
│           └── cronograma-divulgacao/
│
└── campanha.json                      (Manifesto da campanha)
```

---

## Detalhamento dos arquivos de campanha

### Artes Visuais (PNG — geradas via HTML+CSS → Chromium)

| Canal | Dimensão | Arquivo gerado |
|---|---|---|
| Instagram Stories | 1080×1920 px | `artes/feed-story/arte-N.png` |
| Instagram Feed | 1080×1350 px | `artes/post/arte-N.png` |
| LinkedIn | 1200×628 px | `artes/post/arte-N.png` |
| WhatsApp | 1080×1080 px | `artes/arte-N.png` |

> Os templates HTML (editáveis) ficam em `templates/arte-N.html` e podem ser
> modificados antes de regerar as artes.

### Textos de Copy (Markdown)

| Canal | Arquivo | Conteúdo |
|---|---|---|
| Instagram | `textos/post-N.md` | Legenda + hashtags |
| LinkedIn | `textos/artigo-N.md` | Artigo ou post longo |
| E-mails | `textos/email-N.md` | Corpo do e-mail + linha de assunto |
| WhatsApp | `textos/mensagem-N.md` | Mensagem de disparo |

### Cronogramas (MD + PDF)

Cada canal tem seu `cronograma.md` com as **4 dimensões obrigatórias** (gate R-CP-4):

| Dimensão | O que informa |
|---|---|
| **O quê** | Arquivo exato a publicar (arte PNG + texto MD) |
| **Por quê** | Objetivo do dia (fase do funil: gancho / aprofundamento / urgência-CTA) |
| **Como** | Formato de publicação com arte/texto/CTA reais |
| **Quando** | Data + horário por formato |

O cronograma é compilado em PDF via Pandoc → Typst.

### Manifesto `campanha.json`

Campos: `id`, `slug`, `material`, `status`, `criada_em`, `concluida_em`,
`janela_dias`, `canais` ativos, `snapshot` de artes e textos.

---

## Gates de Validação da Campanha

| Gate | Código | O que verifica |
|---|---|---|
| Artes suficientes | R-CP-1 | Quantidade de artes >= dias do cronograma |
| Artes por formato | R-CP-3 | Contagem correta por canal (IG/LI/WhatsApp) |
| Cronogramas com 4 dimensões | R-CP-4 | Presença de O quê / Por quê / Como / Quando |
| Copy personalizada | R-CP-5 | `grep 'Autor Digital'` retorna vazio |

**Validar:**
```bash
python scripts/validar-campanha.py --material <slug> --estrito
```

---

# FLUXO 3 — CRIAÇÃO DA MÁQUINA DE VENDAS

A Máquina de Vendas é um **projeto full-stack deployável** gerado em
`output/<slug-colecao>/maquina/` (regra 1:1 — uma máquina por coleção).

**Comando:** `/criar-maquina <slug>`

---

## Estrutura completa gerada

```
output/<slug-colecao>/maquina/
│
├── manifesto.json              (ID, slug, coleção-fonte, snapshot de campanhas)
├── README.md                   (Arquitetura + deploy + operação — personalizado por nicho)
├── AGENTS.md                   (Regras para agentes de IA)
├── CLAUDE.md                   (Alias de AGENTS.md)
├── SPEC.md                     (Contrato da máquina)
├── docker-compose.yml          (Orquestração: frontend + backend + automações)
├── vercel.json                 (Config deploy Vercel — frontend)
├── .env.example                (Todas as variáveis de ambiente — sem valores reais)
├── .mcp.json                   (MCPs gerados: db_state + file_writer)
│
├── config/
│   ├── produtos.json           (Catálogo: preços, produto default)
│   ├── funis.json              (Funis: steps, produto, desconto)
│   ├── personas.json           (Personas da comunicação por nicho)
│   ├── canais.json             (Instagram: hashtags, localizações, limites)
│   ├── email.json              (SMTP, taxa limite, assinatura, listas)
│   ├── pagamento.json          (Hotmart: CLIENT_ID/SECRET, webhook)
│   ├── roteamento_modelos.json (Temperatura/max_tokens por tarefa de IA)
│   └── subagentes.json         (Agentes de IA por função)
│
├── database/
│   ├── schema.sql              (Esquema das tabelas)
│   ├── seed.sql                (Dados iniciais — funis, produtos padrão)
│   └── maquina.db              (SQLite criado na 1ª execução)
│
├── backend/app/
│   ├── main.py                 (FastAPI — monta routers)
│   ├── config.py               (Configuração a partir do .env)
│   ├── routers/
│   │   ├── leads.py            (POST /api/leads/ — cria lead)
│   │   ├── funil.py            (Métricas do funil e status dos leads)
│   │   ├── emails.py           (Sequências e disparos — respeita rate limits)
│   │   └── webhooks.py         (Confirmação de pagamento Hotmart)
│   ├── services/
│   │   ├── lead_service.py
│   │   ├── email_service.py
│   │   ├── metricas_service.py
│   │   ├── scoring_service.py  (Prioriza leads quentes)
│   │   └── auto_correct.py     (A/B automático)
│   ├── models/
│   │   ├── lead.py
│   │   ├── venda.py
│   │   ├── campanha.py
│   │   └── interacao.py
│   └── database/
│       ├── connection.py       (sqlite3)
│       └── migrations.py
│
├── frontend/                   (Next.js 14 — App Router + TailwindCSS + TypeScript)
│   ├── app/
│   │   ├── page.tsx            (Landing de venda: hero → dor → solução → preço → CTA)
│   │   ├── captura/page.tsx    (Landing de captura — links de bio, tráfego pago)
│   │   ├── checkout/page.tsx   (Checkout: nome/e-mail → POST /api/checkout)
│   │   ├── obrigado/page.tsx   (Pós-compra / obrigado)
│   │   └── admin/
│   │       ├── page.tsx        (Dashboard de métricas)
│   │       ├── leads/page.tsx
│   │       ├── metricas/page.tsx
│   │       └── emails/page.tsx
│   ├── app/api/
│   │   ├── lead/route.ts       (Cria lead — validação Zod)
│   │   ├── checkout/route.ts   (Cria lead + processa pedido — validação Zod)
│   │   ├── webhook/route.ts    (Webhook Hotmart/SendGrid)
│   │   └── health/route.ts     (Status da aplicação)
│   ├── components/
│   │   ├── Hero.tsx
│   │   ├── LeadForm.tsx
│   │   ├── ValueStack.tsx
│   │   ├── Testimonials.tsx
│   │   ├── PricingCard.tsx
│   │   ├── Guarantee.tsx
│   │   └── MetricsChart.tsx
│   ├── lib/
│   │   ├── api.ts              (Cliente do backend FastAPI)
│   │   └── analytics.ts        (Rastreamento UTM)
│   └── package.json
│
├── scripts/
│   ├── lead_hunter.py          (Captura leads no Instagram — cron 8h/14h/20h)
│   ├── email_sender.py         (Envia e-mails do funil — cron 9h, máx 30/h)
│   ├── funnel_monitor.py       (Gera metrics.json + webhooks — 1×/hora)
│   ├── auto_correct.py         (A/B automático — diário)
│   └── deploy.sh               (Docker/VPS: full/status/rollback/backup)
│
├── templates/emails/           (Templates de e-mail personalizados por nicho)
│
├── conteudo/                   (Cópia da obra e derivados)
│   ├── livro.md                (Livro-mãe em Markdown)
│   ├── livro.pdf               (PDF do livro-mãe)
│   ├── ebook-N.pdf             (PDFs dos e-books)
│   ├── playbook.pdf            (PDF do playbook)
│   └── lead-magnet-N.pdf       (PDFs dos lead magnets)
│
└── campanhas/                  (Snapshot das campanhas da coleção)
    ├── snapshot.json           (Origem, atualizado_em, materiais incluídos)
    └── <material>/             (Cópia de artes PNG + textos MD + cronogramas)
        ├── redes-sociais/
        └── canais-comunicacao/
```

---

## Banco de Dados — Tabelas

| Tabela | Colunas principais | Status do lead |
|---|---|---|
| `leads` | email, nome, fonte, funil, status | novo → nutrido → pago → cancelado |
| `vendas` | pedido, valor, status, lead_id | pendente → pago → cancelado |
| `campanhas` | variante A/B, métrica, resultado | — |
| `interacoes` | abertura, clique, descadastro | — |

---

## Automações — Cron

| Script | Cron | Função |
|---|---|---|
| `lead_hunter.py` | 8h / 14h / 20h | Captura leads por hashtags e localizações no Instagram |
| `email_sender.py` | 9h | Envia e-mails da sequência do funil (máx. 30/h, 200/dia) |
| `funnel_monitor.py` | 1×/hora | Lê o banco, grava `metrics.json`, dispara webhooks Slack/Discord |
| `auto_correct.py` | diário | Analisa métricas e propõe variantes A/B (assunto, CTA, horário) |

---

## Variáveis de Ambiente (`.env.example`)

| Grupo | Variáveis |
|---|---|
| App | `APP_ENV`, `APP_SECRET_KEY`, `SITE_URL`, `LOG_LEVEL` |
| Backend | `BACKEND_URL`, `NEXT_PUBLIC_BACKEND_URL` |
| Banco | `DATABASE_PATH` (default `./database/leads.db`) |
| Instagram | `INSTAGRAM_ACCESS_TOKEN`, `INSTAGRAM_APP_ID`, `INSTAGRAM_APP_SECRET` |
| SMTP | `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `FROM_EMAIL`, `FROM_NAME` |
| Hotmart | `HOTMART_WEBHOOK_SECRET`, `HOTMART_CLIENT_ID`, `HOTMART_CLIENT_SECRET` |
| IA | `OPENAI_API_KEY`, `OPENAI_MODEL` (gpt-4o-mini) |
| Deploy | `VPS_HOST`, `VPS_USER`, `VPS_PATH`, `VERCEL_TOKEN` |
| Alertas | `SLACK_WEBHOOK_URL`, `DISCORD_WEBHOOK_URL` |
| Limites | `MAX_EMAILS_PER_HOUR=30`, `MAX_EMAILS_PER_DAY=200`, `MAX_LEADS_PER_DAY=100` |

---

## Gates de Validação da Máquina

| Gate | Verificação |
|---|---|
| Copy personalizada | `grep 'Autor Digital'` retorna vazio |
| Rota `/api/checkout` | POST retorna 200 com nome/e-mail JSON |
| Lead chega em `/api/leads/` | Registro confirmado no SQLite |
| Produto default alinhado | `config/produtos.json` bate com rota checkout |
| `.env` preenchido | Nenhuma variável com valor `XXXXX` |

---

# MAPA CONSOLIDADO — Tipos de arquivo por fluxo

| Extensão | Fluxo 1 (Materiais) | Fluxo 2 (Campanhas) | Fluxo 3 (Máquina) |
|---|---|---|---|
| `.pdf` | Livro, TCC, Artigo, E-book, Playbook, LM, E-mails | Cronogramas | Conteúdo (cópias) |
| `.md` | Todos os tipos (fonte) | Textos de copy, cronogramas | README, AGENTS, SPEC |
| `.epub` | Livro, E-book | — | — |
| `.html` | Slide Deck (entregável navegável) | Templates de artes | Frontend (compilado) |
| `.png` | Capas, ilustrações, diagramas | Artes IG/LI/WhatsApp | Capas copiadas |
| `.json` | Manifesto, config, estado | `campanha.json` | Configs, manifesto |
| `.typ` | Intermediário Typst (todos os PDFs) | — | — |
| `.sql` | — | — | `schema.sql`, `seed.sql` |
| `.ts` / `.tsx` | — | — | Frontend Next.js (15+ arquivos) |
| `.py` | — | — | Backend FastAPI + automações (10+ arquivos) |
| `.sh` | — | — | `deploy.sh` |
| `.yml` | — | — | `docker-compose.yml` |

---

# ESTRUTURA COMPLETA DO HUB POR COLEÇÃO

Visão do `output/<colecao>/` após execução dos **3 fluxos completos**:

```
output/<colecao>/
│
├── livros/<slug>/
│   ├── livro-compilado.md
│   ├── livro_final.pdf         (FLUXO 1 — Livro-mãe)
│   ├── <titulo>.epub
│   ├── sumario_macro.json
│   ├── derivados.json
│   ├── config_obra.json
│   └── imagens/capa.png
│
├── artigos/<slug>--art-N-<nome>/
│   ├── <titulo>.pdf            (FLUXO 1 — Artigos derivados)
│   ├── _artigo_meta.md
│   └── artigo_metadados.json
│
├── ebooks/<slug>--eb-N-<nome>/
│   ├── ebook-compilado.md      (FLUXO 1 — E-books derivados)
│   ├── <codigo>.pdf
│   └── ebook_metadados.json
│
├── playbooks/pbk-N-<slug>/
│   ├── playbook.md             (FLUXO 1 — Playbook)
│   ├── playbook.pdf
│   └── passos/
│
├── lead-magnets/
│   ├── armadilhas-<slug>.md + .pdf    (FLUXO 1 — Lead Magnets)
│   ├── cheat-sheet-<slug>.md + .pdf
│   ├── checklist-<slug>.md + .pdf
│   ├── mapa-mental-<slug>.md + .pdf
│   ├── entregas-<slug>.md + .pdf
│   └── mini-guia-<slug>.md + .pdf
│
├── decks/
│   ├── index.html              (FLUXO 1 — Slide Deck navegável)
│   └── gerar-pdf.mjs
│
├── emails/
│   ├── 01-boas-vindas.md       (FLUXO 1 — Sequência de E-mails)
│   ├── 02-conteudo-valor.md
│   ├── 03-cases-uso.md
│   ├── 04-dicas-avancadas.md
│   ├── 05-oferta-cta.md
│   ├── sequencia-emails.md
│   └── sequencia-emails.pdf
│
├── colecoes/<nome>.json         (Manifesto de coleção)
│
├── distribuicao/
│   ├── LEIA-ME.md
│   └── LICENCA.txt
│
├── campanhas/<material-slug>/
│   ├── redes-sociais/instagram/ (FLUXO 2 — Artes PNG + textos MD + cronograma MD+PDF)
│   ├── redes-sociais/linkedin/  (FLUXO 2 — Artes PNG + textos MD + cronograma MD+PDF)
│   ├── canais-comunicacao/emails/      (FLUXO 2 — Textos MD + cronograma MD+PDF)
│   ├── canais-comunicacao/whatsapp/    (FLUXO 2 — Artes PNG + textos MD + cronograma MD+PDF)
│   └── campanha.json
│
└── maquina/
    ├── manifesto.json           (FLUXO 3 — Máquina de Vendas)
    ├── README.md / AGENTS.md / SPEC.md
    ├── docker-compose.yml / vercel.json / .env.example / .mcp.json
    ├── config/*.json             (8 arquivos de configuração)
    ├── database/                 (schema.sql + seed.sql + maquina.db)
    ├── backend/app/              (FastAPI: routers, services, models, database)
    ├── frontend/                 (Next.js 14: pages, API routes, components)
    ├── scripts/                  (lead_hunter.py, email_sender.py, funnel_monitor.py, auto_correct.py, deploy.sh)
    ├── templates/emails/         (Templates de e-mail por nicho)
    ├── conteudo/                 (Cópias: livro.pdf, ebook-N.pdf, playbook.pdf, LM-N.pdf)
    └── campanhas/                (Snapshot de artes + textos das campanhas)
```

---

## Notas importantes

> **Motor de PDF:**
> - Pandoc → Typst: livro, TCC, artigo, e-book, playbook, e-mails, cronogramas.
> - HTML + CSS → Chromium: lead magnets, slide deck, artes de campanha.

> **MAX_PATH do Windows (260 caracteres):**
> Todos os caminhos foram projetados para caber dentro desse limite (V5.1, ~150 chars).

> **Regra 1:1 — Máquina de Vendas:**
> Uma única pasta `maquina/` por coleção. Tentativas de gerar uma segunda máquina
> no mesmo hub são recusadas sem sobrescrever.

> **Intermediários `.typ`:**
> Os arquivos `.typ` são necessários para recompilação sem relançar o LLM.
> Não remova após a compilação inicial.

> **Snapshot de campanhas na máquina:**
> A pasta `maquina/campanhas/` é uma cópia dos artefatos de campanha no momento
> da criação da máquina. Para atualizar, use a skill `sincronizar-maquina-vendas`.

---

*Relatório gerado automaticamente pela Fábrica Agêntica de Publicações — 2026-08-10.*
