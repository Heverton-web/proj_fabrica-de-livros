---
description: Reescreve a OBRA INTEIRA (livro/TCC) no mesmo slug, preservando config/sumário/dossiê por padrão — sem orfanar série, coleção ou derivados. Uso: /reescrever <slug> [--dossie|--sumario]
---

Você é o Orquestrador Mestre. O operador disparou `/reescrever` com
`$ARGUMENTS` = `<slug> [--dossie|--sumario]`.

Objetivo: regravar a obra inteira no MESMO slug. Por padrão PRESERVA
`config_obra.json` (tema, série, tamanho), `sumario_macro.json` (arquitetura) e
o dossiê — a reescrita é de redação, não de pesquisa.

- `--dossie`  → re-roda a pesquisa (dossiê novo; Fase 1 via `subagente-pesquisador`)
- `--sumario` → re-arquiteta (arquiteto; sumário novo)
- Ambos → pesquisa + arquitetura novas.

## Passo 0 — Backup completo da obra
1. Copie `output/<slug>/capitulos/` para `output/<slug>/revisao/backups/<ts>-obra/`
   (cada capítulo + estado do pool). O backup é a BASE de cada reescrita.
2. Confirme que a obra está em estado auditável (`auditar-obra.py <slug>` roda).

## Passo 1 — (Opcional) Nova pesquisa/arquitetura
3. Se `--dossie`: invoque `subagente-pesquisador` com o tema →
   `python scripts/indexar-dossie.py <slug> --indexar`.
4. Se `--sumario`: invoque `arquiteto` → novo `sumario_macro.json`.

## Passo 2 — Reescrever todos os capítulos (pool em lotes de 4)
5. Para cada capítulo do sumário:
   ```bash
   python scripts/pool-capitulos.py <slug> --reescrever <n>
   ```
6. Despache os `subagente-redator-capitulo` em lotes de 4 (mesmo fluxo do
   `/criar-livro` Passo 2), cada um com **base = backup**
   (`revisao/backups/<ts>-obra/cap_<n>.md`) e com os gates F1/F2 como contrato.
   Registre o desfecho de cada um (`--registrar <n> --sucesso|--falha`).
7. `python scripts/pool-capitulos.py <slug> --pendentes --estrito` até vazio.

## Passo 3 — Fase 2.5 + F3 (obrigatórias)
8. `python scripts/auditar-obra.py <slug> --estrito` + `validar-codigo.py <slug> --estrito --executar`
   + gates de conteúdo; `revisor-tecnico` corrige até `--estrito` retornar 0
   (máx. 3 rodadas).
9. Recompile: `compilador-abnt` → `compilar-para-pdf.py <slug> --paginas-exatas`.

## Passo 4 — Derivados (cascata, reescrever também)
10. Re-rodar os derivados para refletir o conteúdo novo (a ordem importa):
    ```bash
    # playbook ANTES de lead magnets e e-mails
    ```
    `/criar-playbook <slug>` → `/criar-lead-magnet <slug> --todos` +
    `/criar-deck <slug>` + `/criar-emails <slug>` → `/colecao --sincronizar` →
    `python scripts/empacotar-distribuicao.py <slug>`.

## Passo 5 — Relatório telegráfico (REGRA 2)
Slug, escopo (redação só / +dossiê / +sumário), capítulos regravados, backups
(caminho), veredito da auditoria, derivados re-gerados.
