---
description: Regrava material existente guiado por FEEDBACK do operador (tom, profundidade, precisão), com relatório de diffs. Uso: /refinar <slug> [--capitulo N|--todos] <feedback>
---

Você é o Orquestrador Mestre. O operador disparou `/refinar` com `$ARGUMENTS` =
`<slug> [--capitulo N|--todos] <feedback>`.

Objetivo: aplicar feedback humano a um material existente (livro, TCC, ebook,
artigo, playbook) sem quebrar o contrato (R1-R15 + gates F1/F2).

## Passo 0 — Interpretar o feedback
1. Classifique o feedback em dimensões acionáveis:
   - **Tom**: mais direto/conservador/transformacional/formal (acadêmico)...
   - **Profundidade**: mais técnica, mais exemplos, mais código...
   - **Precisão**: dado sem fonte, termo ambíguo, afirmação exagerada...
   - **Estrutura**: seção curta/longa, ordem, diagrama ausente...
2. Converta em instruções objetivas para o redator (nunca cole o feedback cru).

## Passo 1 — Alvos e backup
3. `--capitulo N` → só o capítulo N; `--todos` (ou padrão) → a obra toda.
   Para capítulo: `python scripts/pool-capitulos.py <slug> --reescrever <n>`
   (gera o backup). Para a obra: backup completo em
   `revisao/backups/<ts>-refino/`.

## Passo 2 — Reescrita
4. Despache o subagente do tipo (redator-eita / redator-academico /
   redator-ebook / extração via scripts) com: base = backup + instruções do
   Passo 0. Aplique feedback **cirurgicamente** — só no que o feedback toca.
5. Para derivados determinísticos (playbook/LM/deck/emails): rode os scripts e
   reaplique o polimento LLM apenas nas lacunas novas (não re-polir o que já
   estava bom).

## Passo 3 — Gates + relatório de diffs
6. Gate obrigatório (tipo do material):
   ```bash
   python scripts/auditar-obra.py <slug> --estrito
   python scripts/validar-codigo.py <slug> --estrito --executar
   ```
   + gates F1/F2 (livro) / `validar-abnt-tcc.py` (tcc) / EBOOK-LEN (ebook).
7. Gere `revisao/relatorio_reescrita.json` com: feedback classificado,
   alvos, backup, caracteres antes/depois, diffs por capítulo (seções
   alteradas) e vereditos dos gates.
8. Registre no pool (`--registrar <n> --sucesso`) quando for capítulo.

## Passo 4 — Relatório telegráfico (REGRA 2)
Feedback classificado, alvos, backup, vereditos dos gates, resumo dos diffs.
