# SPEC_LEAD_MAGNET — Contrato do Lead Magnet (V5)

> Tipo derivado de **extração determinística**. Cinco dos seis formatos custam
> **0 token**: são *queries de agregação* sobre os cards do playbook.

## 1. Definição

Material curto de **topo de funil**: alta densidade prática, promessa explícita
no título e **CTA rastreável** para a obra-mãe.

O que separa lead magnet de "PDF curto": **conteúdo + conversão**. Sem CTA
rastreável o gate reprova (R-LM-1).

## 2. Fonte de derivação

**Fonte preferencial: o PLAYBOOK**, não a prosa do livro. Os cards já são a
camada estruturada da fábrica; cada formato é uma agregação de um campo.

| Formato | Campo agregado | Custo LLM |
|---|---|---|
| `checklist` | ⑥ `feito_quando` de todos os cards | **0** |
| `armadilhas` | ⑦ `armadilhas` | **0** |
| `cheatsheet` | ④ `execucao` → comandos | **0** |
| `entregas` | ③ `entregas` | **0** |
| `mapa` | `sumario_macro.estagios` + objetivos | **0** |
| `mini-guia` | 1 card completo + esqueleto de polimento | ~1–2k |

Derivação permitida: **playbook → lead-magnet** (preferida) ou
**livro → lead-magnet** (extrai os cards na hora, mesmo parser, 0 token).

## 3. Regras (gate: `scripts/validar-lead-magnet.py`)

| Regra | Enunciado |
|---|---|
| **R-LM-1** | CTA final com URL rastreável (UTM) para a obra-mãe. O CTA também aparece no rodapé de toda página. |
| **R-LM-2** | Promessa explícita no título: número ("As 20 armadilhas"), "como", ou substantivo de formato (checklist, mapa, cheat sheet, guia) |
| **R-LM-3** | Teto de páginas do formato respeitado (checklist 8, cheatsheet 6, mapa 4, mini-guia 12, armadilhas 10, entregas 6). **Medido no PDF compilado**; a estimativa por caracteres só vale antes da compilação |
| **R-LM-4** | **Zero teoria** — similaridade com §1–§3 do livro-mãe abaixo de 0,15 (mais estrito que R-PBK-0) |
| **R-LM-5** | Par de saídas: PDF A4 (download) + PNG 1080×1350 (card social/anúncio) |
| **R-LM-6** | Badge de nível + cor da coleção herdados da obra-mãe |
| **R-LM-7** | Quantidade mínima de itens do formato atingida (`min_itens`); o teto (`max_itens`) é aplicado na geração, por rodízio entre capítulos |
| **R-LM-8** | Peso do PDF sob 250 KB por página — lead magnet vai por e-mail e download |

## 4. UTM

Montada por `gerar-lead-magnet.py`, não escrita à mão:

```
<cta_url>?utm_source=lead-magnet&utm_medium=pdf
         &utm_campaign=<slug-obra-mae>&utm_content=<formato>
```

## 5. Estrutura de saída

```
output/lead-magnets/<slug-mae>--lm-NN-<formato>/
├── config_obra.json      tipo_obra=lead-magnet, formato_lm, cta_url, cta_texto
├── sumario_macro.json    titulo, subtitulo (promessa), itens
├── lead_magnet.md        material montado (com bloco "# Próximo passo")
├── imagens/              capa A4 + card_social.png
└── revisao/
    ├── relatorio_lead_magnet.json
    └── relatorio_gate.json
```

## 6. Pipeline

```bash
python scripts/gerar-lead-magnet.py livros/<slug> --todos --cta-url https://exemplo.com/livro
python scripts/gerar-lead-magnet-pdf.py --todos
python scripts/gerar-capa.py lead-magnets/<slug>--lm-01-armadilhas --tipo lead-magnet --social
python scripts/validar-lead-magnet.py --todos --estrito
```

## 7. Motor de renderização

O PDF **não** sai do Typst: sai de **HTML+CSS renderizado pelo Chromium**
(`templates/template_lead_magnet.html` + Playwright). CSS dá controle fino de
gradiente, sobreposição e tipografia de campanha — o que uma peça de marketing
exige e o Typst não entrega bem.

**O HTML é camada intermediária, como o `.typ` dos outros tipos: o entregável é
o PDF.** Nenhum tipo declara `.html` em `extensoes_saida`.

Não usa Paged.js: o Chromium já implementa `@page`, `break-*` e orphans/widows;
o rodapé com o CTA vem de `page.pdf(footerTemplate=...)`. Isso evita vendorizar
~200 KB de JS de terceiros.

Três armadilhas do Chromium que o template já contorna (com teste de regressão):

| Armadilha | Efeito observado | Correção |
|---|---|---|
| `filter: brightness()` rasteriza por elemento | PDF de 100 KB → **6,6 MB** com ~100 `h2` | `color-mix()` |
| `break-before: avoid` é ignorado | 1 página em branco em **todo** lead magnet | exceção no seletor: `h1:not(:first-of-type)` |
| `break-inside: avoid` na tabela | tabela de 20 linhas empurrada inteira, páginas quase vazias | proteger a **linha** (`tr`), não a tabela |

O parâmetro `margin` de `page.pdf()` **sobrepõe** o `@page { margin }` do CSS,
inclusive o `:first`. A capa usa `--altura-util: 257mm` (297 − 18 − 22) para não
transbordar.

## 8. Nota de escala

Um livro G (12 capítulos) rende os 6 formatos por **menos de 8k tokens no total**.
Não confunda com e-book: e-book reescreve prosa (caro), lead magnet agrega
campos já estruturados (grátis).
