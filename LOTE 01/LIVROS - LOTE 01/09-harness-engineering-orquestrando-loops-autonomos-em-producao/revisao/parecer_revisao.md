# Parecer de Revisão — Livro 9: Harness Engineering

**Obra:** Harness Engineering: orquestrando loops autônomos em produção
**Slug:** `livros/09-harness-engineering-orquestrando-loops-autonomos-em-producao`
**Fase:** 2.5 — Peer Review Autônomo (revisor-tecnico)
**Data:** 06 ago. 2026

## Veredito final: CONFORME

Auditoria determinística (`auditar-obra.py`) — **R1 a R15 todos OK**:

| Requisito | Veredito |
|---|---|
| R1 — Mínimo 12 capítulos | OK (12) |
| R2 — Mínimo 120 páginas (~300.000 caracteres) | OK (340.659 caracteres, ~136 páginas) |
| R3 — 7 seções EITA-V2 por capítulo | OK |
| R4 — Mínimo 20 referências ABNT por capítulo | OK (20/capítulo) |
| R9 — Sem horizontal rules | OK |
| R10 — Mínimo 3 citações inline [N] | OK |
| R11 — Diagrama Mermaid na seção Ilustra | OK (12/12 válidos) |
| R12 — Bloco de código na seção Técnica | OK (CI 100%) |
| R13 — Sem truncamento/pendências (TODO/placeholder) | OK |
| R14 — Rastreabilidade [N] texto ↔ referências | OK |
| R15 — Referências em ordem numérica (NBR 6023) | OK |

## Auto-correções aplicadas (REGRA 4)

1. **cap_1 — refs insuficientes (17/20):** adicionadas 3 referências ABNT
   ([18]-[20], LangGraph, Oracle Budget Guardrails, Model Context Protocol)
   com citações inline correspondentes no texto.
2. **cap_8 — diagrama Mermaid com falha de renderização:** o rótulo `pass@k alto`
   e o subtítulo `Rubrica LLM-as-judge` quebravam o parser do mermaid-cli;
   substituídos por `aprovacao alta` e `Rubrica com LLM` — diagrama validado.
3. **CI de código:** 12/12 capítulos com blocos verificáveis válidos
   (`validar-codigo.py` — taxa 100%).
4. **Diagramas Mermaid:** 12/12 válidos (`renderizar-diagramas.py --validar`).

## Observações de qualidade

- Motivo condutor "a locomotiva e os trilhos" presente em todos os capítulos
  (seção Ilustra + vocabulário em transições), com persona Engenheiro de
  Plataforma/MLOps recorrente.
- Callbacks nomeados entre capítulos consecutivos presentes.
- Estrutura da obra: 4 Partes, 12 capítulos, Introdução + Conclusão gerais.
- Total de referências: 240 (20 × 12 capítulos).
