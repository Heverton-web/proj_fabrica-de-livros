---
description: Transmuta um material EXISTENTE de um tipo para outro (ex.: ebook→livro, livro→TCC, TCC→livro), com recorte, registro e gates do destino. Uso: /reescrever-como <slug-origem> --tipo <destino> [--novo-slug]
---

Você é o Orquestrador Mestre. O operador disparou `/reescrever-como` com
`$ARGUMENTS` = `<slug-origem> --tipo <destino> [--novo-slug]`.

Objetivo: reescrever um material existente em um material de OUTRO tipo
(transmutação). A ORIGEM nunca é alterada. O par origem→destino é validado
contra a matriz `reescrever_de` (`python scripts/tipos_obra.py --matriz`).

Pares válidos (V5.2):
- `livro` ← `ebook | playbook | artigo | tcc` (expansão, custo alto)
- `tcc` ← `livro | ebook` (reframing acadêmico, NBR 10520)
- `ebook` ← `livro | tcc | playbook` (reescrita de tom)
- `artigo` ← `livro | tcc | ebook` (compressão científica)

## Passo 1 — Esqueleto (determinístico)
1. Valide o par e crie a estrutura destino (recorte da origem: títulos +
   objetivos das unidades; herda motivo_condutor, série, senioridade e dossiê):
   ```bash
   python scripts/transmutar-obra.py <slug-origem> --tipo <destino> [--slug-novo <novo>]
   ```
   Registra em `derivados.json` da origem. Guarde o slug destino exibido.

## Passo 2 — Redação (subagentes do DESTINO, lotes de 4)
2. Para cada unidade do sumário destino, despache o subagente do tipo destino
   (redator-eita / redator-academico / redator-ebook) com a skill em **Modo
   Transmutação**:
   - Base = seção/capítulo correspondente da ORIGEM (releia o arquivo).
   - Preserve: referências reais (valide contra o dossiê copiado), diagramas
     Mermaid reutilizáveis, motivo condutor, vocabulário.
   - Converta o formato de citação quando o destino pedir outro
     (livro: `[N]`; tcc/artigo: autor-data NBR 10520).
   - TCC: framework ACAD (Contextualização, Referencial, Análise, Síntese).
   - Ebook: tom leve, sem `[N]` no corpo, CTA final.
3. Para expansão (→ livro): cada unidade da origem vira um capítulo EITA
   completo (7 seções) — pesquise complementos APENAS no dossiê copiado.

## Passo 3 — Gates do DESTINO (obrigatórios)
4. `python scripts/auditar-obra.py <slug-destino> --estrito`
   `python scripts/validar-codigo.py <slug-destino> --estrito --executar`
   + `validar-referencias.py`, `validar-metricas.py`, `validar-escala.py`,
   `validar-afirmacoes.py`, `validar-fontes.py` (livro);
   `validar-abnt-tcc.py` (tcc); EBOOK-LEN (ebook).
5. Revisão técnica: `revisor-tecnico` no destino até `--estrito` retornar 0.
6. Compile o destino (`compilar-para-pdf.py` com o tipo certo).

## Passo 4 — Integração
7. `python scripts/colecao.py --sincronizar --slug <slug-destino>` (mesma série).
8. Se o destino for livro/TCC, gere os derivados do destino (playbook → ...)
   seguindo o fluxo normal.

## Passo 5 — Relatório telegráfico (REGRA 2)
Origem, destino, par validado, unidades recortadas, slug destino, veredito da
auditoria, gates do destino. A origem permanece intacta.
