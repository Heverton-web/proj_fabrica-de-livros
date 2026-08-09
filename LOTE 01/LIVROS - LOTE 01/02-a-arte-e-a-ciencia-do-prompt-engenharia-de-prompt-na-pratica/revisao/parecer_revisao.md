# Parecer de Revisão Técnica — Livro 2 "A Pilha Agêntica"

**Obra:** *A arte e a ciência do prompt: engenharia de prompt na prática*
**Slug:** `livros/a-arte-e-a-ciencia-do-prompt-engenharia-de-prompt-na-pratica`
**Série:** A Pilha Agêntica — AI-Driven Development (AIDD)
**Data:** 5 de agosto de 2026

---

## 1. Escopo da Revisão

Revisão técnica da Fase 2.5 da esteira da Fábrica Agêntica, cobrindo os 10 capítulos da obra:

| Capítulo | Título (resumo) |
|---|---|
| 1 | O que é um prompt: da comunicação à especificação |
| 2 | Anatomia de um bom prompt: instrução, contexto, exemplos, formato |
| 3 | Few-shot e zero-shot: aprender por demonstração e por instrução |
| 4 | Chain-of-thought: o raciocínio visível |
| 5 | Decomposição de tarefas e prompts de sistema vs. de usuário |
| 6 | Por que prompt engineering não escala sozinha em produção |
| 7 | Versionamento, teste e governança de prompts |
| 8 | Avaliação manual: reconhecer a resposta plausível-porém-errada |
| 9 | Limites da disciplina e segurança (injeção de prompt) |
| 10 | A ponte para a Context Engineering |

## 2. Verificação de Requisitos (Auditoria Automatizada)

**VEREDITO: CONFORME**

| Requisito | Status |
|---|---|
| R1 — Mínimo 10 capítulos | OK (10) |
| R2 — Mínimo 150 páginas (~375.000 caracteres) | OK (375.566) |
| R3 — 7 seções EITA-V2 por capítulo | OK (10/10) |
| R4 — Mínimo 20 referências ABNT por capítulo | OK (20/20 por capítulo) |
| R9 — Ausência de horizontal rules | OK |
| R10 — Mínimo 3 citações inline por capítulo | OK |
| R11 — Mínimo 1 diagrama Mermaid na seção Ilustra | OK (10/10 diagramas válidos) |
| R12 — Bloco de código na seção Técnica | OK |
| R13 — Sem truncamento nem pendências | OK |
| R14 — Rastreabilidade citação ↔ referência | OK (sem órfãs, sem não-citadas) |
| R15 — Referências em ordem numérica (NBR 6023) | OK |

## 3. Verificações Complementares

- **Rastro de referências:** 10/10 capítulos — 20 citações no corpo ↔ 20 entradas na seção 7, ordem correta, zero órfãs, zero não-citadas.
- **Código:** 49 blocos validados — taxa de aprovação 100% (39 Python OK + 10 Mermaid sem validador dedicado, todos sintaticamente válidos na renderização).
- **Diagramas:** 10/10 Mermaid válidos e renderizáveis.
- **Sobreposição entre capítulos:** nenhuma relevante.
- **Motivo condutor:** recorrente em todos os capítulos (a pilha que se empilha).
- **Callback ao capítulo anterior:** presente em todos os capítulos aplicáveis.

## 4. Observações de Estilo (não bloqueantes)

1. **Grafia inconsistente de termos** (9 ocorrências em nível de alerta): variações como *esta/está*, *porque/porquê*, *análise/analise*, *contínua/continua* e *válida/valida* aparecem com acentuação divergente. Recomenda-se revisão editorial de acentuação na passagem final para PDF.
2. **Citações empilhadas** (466 ocorrências no total da obra): clusters de citações múltiplas `[1][2]` no fim de frases conferem tom de revisão de literatura. Mantido por fidelidade ao estilo da série (Livro 1 adotou o mesmo padrão); pode ser suavizado em edições futuras sem afetar conformidade.

## 5. Veredito Final

A obra **atende integralmente** aos requisitos estruturais, de referenciamento e de qualidade técnica da esteira (R1–R15). O conteúdo técnico está alinhado ao estado da arte da disciplina em agosto de 2026, com fontes reais e verificáveis, e a progressão pedagógica segue o motivo condutor da série. **Aprovada para a Fase 3 (compilação ABNT).**

---

*Parecer emitido pelo revisor técnico da Fábrica Agêntica.*
