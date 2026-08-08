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

## Passo 3 — Capa + card social

```
python scripts/gerar-capa.py lead-magnets/<slug-lm> --tipo lead-magnet --social
```

Gera `imagens/capa.png` (A4 300dpi) e `imagens/card_social.png` (1080×1350).

## Passo 4 — Gate

```
python scripts/validar-lead-magnet.py --todos --estrito
```

Reprovas típicas: `R-LM-1` (sem UTM), `R-LM-3` (passou do teto de páginas),
`R-LM-7` (poucos itens — o livro-mãe tem cards rasos).

## Passo 5 — PDF

```
python compilar-para-pdf.py lead-magnets/<slug-lm> --tipo lead-magnet
```

## Passo 6 — Coleção

```
python scripts/colecao.py --sincronizar --slug <prefixo>/<slug>
```

## Passo 7 — Relatório telegráfico

Formatos gerados, itens por formato, páginas estimadas, veredito do gate.
