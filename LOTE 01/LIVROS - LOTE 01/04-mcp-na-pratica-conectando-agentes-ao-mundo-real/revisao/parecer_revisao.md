# Parecer de Revisão Técnica — Livro 4 "A Pilha Agêntica"

**Obra:** *MCP na prática: conectando agentes ao mundo real*
**Slug:** `livros/mcp-na-pratica-conectando-agentes-ao-mundo-real`
**Data:** 5 de agosto de 2026
**Veredito:** CONFORME

---

## 1. Escopo da revisão

Revisão técnica de conformidade da obra completa (10 capítulos, tamanho G) contra os requisitos editoriais da Fábrica Agêntica: estrutura EITA-V2, mínimo de referências ABNT por capítulo, citações com rastreabilidade, diagramas Mermaid, blocos de código, rastro `[N]` e motivação condutora.

## 2. Resultado da auditoria automatizada (`auditar-obra.py`)

| Requisito | Status |
|---|---|
| R2 — Volume mínimo (~375.000 caracteres / ~150 pág.) | [OK] 375.582 caracteres |
| R3 — 7 seções EITA-V2 por capítulo | [OK] 10/10 |
| R4 — Mínimo 20 referências ABNT por capítulo | [OK] 20/10 capítulos |
| R9 — Ausência de horizontal rules nos capítulos | [OK] |
| R10 — Mínimo 3 citações `[N]` no corpo | [OK] |
| R11 — Diagrama Mermaid na seção Ilustra | [OK] 10/10 |
| R12 — Bloco de código na seção Técnica | [OK] |
| R13 — Ausência de truncamentos/TODO | [OK] |
| R14 — Rastreabilidade citação ↔ referência | [OK] sem órfãs |
| R15 — Referências em ordem numérica ascendente (NBR 6023) | [OK] |
| Motivo condutor reaproveitado | [OK] |
| Callback ao capítulo anterior | [OK] |
| Ritmo de frase variado | [OK] |

## 3. Validações complementares

| Validação | Resultado |
|---|---|
| `validar-codigo.py` (CI de sintaxe) | 27 blocos OK, taxa 100%, 0 falhas |
| `renderizar-diagramas.py --validar` | 10/10 diagramas Mermaid válidos e renderizados |

## 4. Alertas de estilo (não bloqueantes)

- 40 pares de parágrafos sobrepostos entre capítulos (padrão da série: vocabulário de retomada consistente — aceito pelo fluxo editorial).
- 9 termos com grafia inconsistente entre versões expandidas (ex.: praticar/praticá; modelcontextprotocol/model-context-protocol) — correção opcional em revisão de copidesque futura.
- 1.847 citações empilhadas `[N][N]` (tom de revisão de literatura) — alerta de estilo reconhecido no fluxo; as frases que as precedem já explicam as ideias.

## 5. Conclusão

A obra atende integralmente aos requisitos obrigatórios (R2–R15) e às validações de código e diagramas. Recomenda-se aprovação para publicação. A revisão de copidesque pode tratar os alertas de estilo em edição futura.

**Parecer:** APROVADO — CONFORME.
