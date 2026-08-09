---
description: Gera a CAMPANHA de TODA a coleção (todos os materiais de uma vez + campanha.json) — itera o manifesto da coleção e aplica o fluxo /campanha a cada membro. Contrato em melhorias/09-08-2026-campanhas-camada-nova.md.
---

# /campanha-completa `[colecao]`

Gera a camada CAMPANHA de **todos os materiais da coleção** de uma única vez
(`output/<colecao>/campanhas/<material-slug>/` para cada membro do manifesto)
e escreve o `campanha.json` do hub.

**Pré-condição:** manifesto da coleção existe (`colecao.py --sincronizar`).

## Passo 1 — Estrutura, moldes, artes e cronogramas (0 token)

```
python scripts/criar-campanha.py --completo [<colecao>]
```

Sem argumento, a coleção é descoberta quando há apenas uma campanha existente.
Para cada membro do manifesto: estrutura de pastas + moldes + PNGs (Chromium) +
cronogramas. Ao final, `campanha.json` lista todos os materiais (status
`estrutura` para os novos).

## Passo 2 — Copy final (LLM, custo baixo) — material a material

Para cada material, siga o Passo 2 do comando `/campanha`: reescreva os moldes
com copy de divulgação (vocabulário condutor, badge, CTA) e troque
`Status: RASCUNHO` por `Status: FINAL`.

## Passo 3 — Gate da coleção

```
python scripts/validar-campanha.py --completo <colecao> --estrito
```

`R-CP-C1` reprova se qualquer material do manifesto estiver sem campanha ou com
status ≠ `completa`. Para cada material com status completa, os gates
individuais (R-CP-1..5) rodam de novo.

Fluxo por material (para os que reprovarem):

```
python scripts/validar-campanha.py --material <slug> --estrito   # achar a falha
python scripts/criar-campanha.py --material <slug> --marcar-completa  # apos corrigir
```

## Passo 4 — Relatório telegráfico

1 linha: N materiais, gate R-CP-C1 conforme, caminho do `campanha.json`.
