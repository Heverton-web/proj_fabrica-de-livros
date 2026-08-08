---
description: Gera a família de LEAD MAGNETS (checklist, armadilhas, cheat sheet, mapa, entregas, mini-guia) a partir dos cards do playbook — 5 dos 6 formatos custam 0 token. Contrato em SPEC_LEAD_MAGNET.md.
---

# /criar-lead-magnet `<prefixo>/<slug>` `[--formato X | --todos]`

**Pré-condição:** playbook existente (`/criar-playbook`) **ou** livro com
capítulos EITA — neste caso os cards são extraídos na hora, sem custo.

## Passo 0 — CTA (obrigatório, R-LM-1)

Lead magnet sem CTA rastreável é reprovado no gate. Se o operador não informou
`--cta-url`, **pergunte antes de gerar** — é o único ponto de interação.

## Passo 1 — Geração (0 token)

```
python scripts/gerar-lead-magnet.py <prefixo>/<slug> --todos --cta-url <url> --cta-texto "<texto>"
```

Ou um formato só: `--formato checklist|armadilhas|cheatsheet|mapa|entregas|mini-guia`.

Cada formato é uma agregação de um campo dos cards. Nenhuma prosa é escrita.

## Passo 2 — Polimento (apenas `mini-guia`)

Só o formato `mini-guia` traz `<!-- POLIMENTO-LLM -->`. Escreva os 2 parágrafos
pedidos lendo **apenas** a §2 *Explica* do capítulo indicado (LeanCTX).
Os outros cinco formatos não precisam de nenhuma escrita.

## Passo 3 — PDF (motor Chromium, não Typst)

```
python scripts/gerar-lead-magnet-pdf.py --todos
```

`compilar-para-pdf.py lead-magnets/<slug>` também funciona — ele detecta
`motor_pdf=chromium` no registro e delega para o script acima.

Depurar layout: `--manter-html` preserva o `_lead_magnet.html` intermediário.
**Nunca entregue o HTML** — ele é camada intermediária, como o `.typ`.

## Passo 4 — Capa + card social

```
python scripts/gerar-capa.py lead-magnets/<slug-lm> --tipo lead-magnet --social
```

Gera `imagens/capa.png` (A4 300dpi) e `imagens/card_social.png` (1080×1350).

## Passo 5 — Gate (depois do PDF, não antes)

```
python scripts/validar-lead-magnet.py --todos --estrito
```

**A ordem importa:** R-LM-3 e R-LM-8 medem o PDF compilado. Rodando o gate antes
da compilação, R-LM-3 cai para uma estimativa por caracteres — que já aprovou
material com o dobro do teto de páginas.

Reprovas típicas: `R-LM-1` (sem UTM), `R-LM-3` (passou do teto), `R-LM-7`
(poucos itens — o livro-mãe tem cards rasos), `R-LM-8` (PDF pesado: procure CSS
que rasteriza, como `filter` ou `box-shadow` em texto).

## Passo 6 — Coleção

```
python scripts/colecao.py --sincronizar --slug <prefixo>/<slug>
```

## Passo 7 — Relatório telegráfico

Formatos gerados, itens por formato, páginas MEDIDAS no PDF, peso, veredito do gate.
