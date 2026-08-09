# Parecer de Revisão Técnica

**Obra:** A Pilha Agêntica — Livro 1: Antes do prompt: fundamentos de software e de modelos de linguagem
**Slug:** livros/a-pilha-agentica-livro-1-antes-do-prompt
**Fase:** 2.5 — Peer Review Autônomo
**Data:** 5 de agosto de 2026
**Revisor:** Skill `revisor-tecnico` (auditoria determinística via scripts locais)

---

## 1. Veredito

**CONFORME**

A obra atende integralmente os requisitos contratuais automatizáveis (R1-R4, R9-R15), com código 100% aprovado no CI de sintaxe e diagramas 100% válidos. Não há pendências de truncamento, citações órfãs ou sobreposição relevante entre capítulos.

---

## 2. Evidências Determinísticas

### 2.1 Auditoria contratual (`scripts/auditar-obra.py`)

| Requisito | Descrição | Status |
|-----------|-----------|--------|
| R1 | Mínimo 10 capítulos | OK (10/10) |
| R2 | Mínimo 150 páginas (~375.000 caracteres) | OK (375.052) |
| R3 | 7 seções EITA-V2 por capítulo | OK (10/10) |
| R4 | Mínimo 20 referências ABNT por capítulo | OK (20/20 em todos) |
| R9 | Ausência de horizontal rules | OK |
| R10 | Mínimo 3 citações inline [N] | OK |
| R11 | Mínimo 1 diagrama Mermaid na Ilustra | OK |
| R12 | Bloco de código na Técnica | OK |
| R13 | Sem truncamento nem placeholders | OK |
| R14 | Rastreabilidade [N] ↔ referências | OK |
| R15 | Referências em ordem ascendente (NBR 6023) | OK |

### 2.2 CI de código (`scripts/validar-codigo.py`)

- 10/10 capítulos: nenhum erro de sintaxe nos blocos verificáveis.
- Relatório: `validacao/relatorio_codigo.json`

### 2.3 Diagramas (`scripts/renderizar-diagramas.py --capitulos --validar`)

- 16/16 diagramas válidos (cap_01: 1, cap_02: 1, cap_03: 2, cap_04: 1, cap_05: 1, cap_06: 2, cap_07: 2, cap_08: 1, cap_09: 3, cap_10: 2).
- Relatório: `validacao/relatorio_diagramas.json`

### 2.4 Rastreabilidade de referências (`scripts/_check_rastro.py`)

- 10/10 capítulos: 20 citações no corpo, 20 entradas na seção 7, nenhuma órfã, nenhuma não citada, ordem ascendente OK.

### 2.5 Qualidade editorial (auditoria)

- Motivo condutor recorrente em todos os capítulos: OK.
- Callback ao capítulo anterior: OK em todos os aplicáveis.
- Ritmo de frase variado: OK.
- Sobreposição relevante entre capítulos: nenhuma.

---

## 3. Ressalvas Não Bloqueantes

| Classe | Detalhe | Ação |
|--------|---------|------|
| Grafia inconsistente (estilo) | 13 termos com variantes de acentuação (ex.: `esta`/`está`, `porque`/`porquê`, `contínua`/`continua`) | Registrado como ressalva de estilo; não afeta conformidade estrutural |
| Citações empilhadas (estilo) | 36 ocorrências de citações múltiplas adjacentes em cap_02..cap_10 | Tom de revisão de literatura; aceitável para obra de referência técnica |

Estas ressalvas não bloqueiam a entrega: a obra segue para a Fase 3 (Acabamento ABNT).

---

## 4. Conclusão

A obra cumpre 100% dos requisitos contratuais automatizáveis. Todos os capítulos passaram pela auditoria estrutural, pelo CI de código e pela validação de diagramas. O Markdown é expedido para a Fase 3 com veredito **CONFORME**.

**Próximo passo:** Fase 3 — Acabamento ABNT (`compilar-para-pdf.py <slug> --paginas-exatas`).
