---
description: Gera o SLIDE DECK (16:9) de uma obra a partir do sumário, dos diagramas já renderizados e dos cards do playbook — custo 0 token. Contrato em SPEC_DECK.md.
---

# /criar-deck `<prefixo>/<slug>`

**Pré-condição:** `sumario_macro.json` da obra existe.
Playbook é opcional (enriquece os bullets).

## Passo 1 — Renderizar diagramas primeiro

```
python scripts/renderizar-diagramas.py <prefixo>/<slug> --capitulos
```

O deck **copia** diagramas já renderizados; sem este passo, R-DK-4 vira aviso.

## Passo 2 — Montagem (0 token)

```
python scripts/gerar-deck.py <prefixo>/<slug> --cta-url <url>
```

Estrutura: capa → objetivo → mapa dos estágios → divisor por Parte →
1 slide por capítulo → CTA.

## Passo 3 — Gate

```
python scripts/validar-deck.py decks/<slug>--deck --estrito
```

Reprova mais comum: `R-DK-2` (bullet longo). Corrija encurtando o
`pilares_previstos` no `sumario_macro.json` do livro-mãe e regere — **não**
edite o `deck.md` à mão, ele é derivado.

## Passo 4 — Capa + PDF

```
python scripts/gerar-capa.py decks/<slug>--deck --tipo deck
python compilar-para-pdf.py decks/<slug>--deck --tipo deck
```

## Passo 5 — Coleção

```
python scripts/colecao.py --sincronizar --slug <prefixo>/<slug>
```

## Passo 6 — Relatório telegráfico

Slides, diagramas embutidos, veredito do gate, caminho do PDF.
