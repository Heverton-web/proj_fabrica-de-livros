---
description: Gera a CAMPANHA de UM material da coleção (estrutura + moldes de copy + artes HTML→Chromium + cronogramas) — custo 0 token no script, copy final escrita pelo agente com LLM. Contrato em melhorias/09-08-2026-campanhas-camada-nova.md.
---

# /campanha `<slug>`

Gera a camada CAMPANHA de **um material** da coleção
(`output/<colecao>/campanhas/<material-slug>/`): redes-sociais (Instagram e
LinkedIn) + canais-comunicacao (e-mails e WhatsApp), com artes, textos,
templates e cronogramas.

**Pré-condição:** o material tem `config_obra.json` (ex.: livro, TCC, artigo,
e-book, playbook, lead magnet, deck) e o manifesto da coleção existe
(`colecao.py --sincronizar` já rodado na coleção).

## Passo 1 — Estrutura, moldes, artes e cronogramas (0 token)

```
python scripts/criar-campanha.py --material <slug>
```

Gera: 24 pastas do registro, moldes de texto com rascunho extraído do material
(título, subtítulo, vocabulário condutor, CTA), PNGs das artes
(Playwright/Chromium: post IG 1080×1350, story 1080×1920, LinkedIn 1200×628,
WhatsApp 1080×1080) com a identidade visual da coleção, templates HTML das
artes e cronogramas com datas reais.

`--sem-artes` pula o Chromium (mantém só o HTML fonte das artes).
`--regenerar` sobrescreve moldes já editados (cuidado).

## Passo 2 — Copy final (LLM, custo baixo)

Reescreva **todos** os moldes `textos/**/*.md` como copy de divulgação com o
tom da coleção: vocabulário condutor, badge de nível, CTA do manifesto.
Use os cabeçalhos de contexto de cada molde. Troque `Status: RASCUNHO` por
`Status: FINAL` em cada arquivo reescrito.

## Passo 3 — Gate

```
python scripts/validar-campanha.py --material <slug> --estrito
```

Reprova mais comum: `R-CP-2` (molde RASCUNHO pendente ou copy genérica
`Autor Digital|centenas de pessoas`) e `R-CP-4` (vocabulário condutor ausente
da copy). Corrija na copy e revalide — nunca contorne o gate.

## Passo 4 — Registrar como completa

```
python scripts/criar-campanha.py --material <slug> --marcar-completa
```

O `campanha.json` da coleção passa a listar o material com status `completa`
(requisito do gate `R-CP-C1` do `/campanha-completa`).

## Passo 5 — Relatório telegráfico

1 linha: pastas/moldes/artes criados + gate conforme + status no manifesto.
