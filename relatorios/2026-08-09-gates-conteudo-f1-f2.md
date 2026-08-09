# RELATÓRIO DE SESSÃO — Gates de Conteúdo F1/F2 (sine qua non)

> **Data:** 2026-08-09
> **Projeto:** Fábrica Agêntica de Publicações

---

## 1. Contexto

Implementação integral do plano melhorias/09-08-2026-gates-conteudo-sine-qua-non.md: 6 gates determinísticos de MÉRITO de conteúdo além da estrutura R1-R15 — referências reais, métricas mensuráveis, limites de escala, afirmações fundamentadas, hierarquia de fontes A/B/C e execução real de código. F1 (determinístico): validar-referencias.py, validar-metricas.py, validar-escala.py, validar-codigo.py --executar/--playbook. F2: validar-afirmacoes.py, validar-fontes.py + skills pesquisador (classificação A/B/C) e revisor-tecnico (conferência por amostra). F3: registro gates_conteudo no tipo livro (tipos_obra.py), encadeamento em auditar-obra.py --estrito, skills estrategista/redator-eita e AGENTS.md.

---

## 2. Bugs Descobertos e Corrigidos

### validar-referencias: cache com nao_verificado (--sem-rede) bloqueava checagem real posterior

- **Causa:** validar-referencias: cache com nao_verificado (--sem-rede) bloqueava checagem real posterior
- **Fix:** fix: cache só é conclusivo para ok/falha; nao_verificado não é gravado
- **Arquivo:** `scripts/validar-referencias.py`

### extrair_referencias: https://doi.org/<doi> duplicava como url

- **Causa:** extrair_referencias: https://doi.org/<doi> duplicava como url
- **Fix:** fix: DOIs capturados primeiro, url doi.org filtrada
- **Arquivo:** `scripts/validar-referencias.py`

### validar-afirmacoes: superlativos de ênfase ('o mais importante') e garantias técnicas ('nunca confie') geravam ruído

- **Causa:** validar-afirmacoes: superlativos de ênfase ('o mais importante') e garantias técnicas ('nunca confie') geravam ruído
- **Fix:** fix: disparadores restritos a fatos externos (%/unidade/superlativo de mercado); exercícios **Desafio excluídos
- **Arquivo:** `scripts/validar-afirmacoes.py`

### executar_bloco: stderr de traceback Python mostrava só o cabeçalho

- **Causa:** executar_bloco: stderr de traceback Python mostrava só o cabeçalho
- **Fix:** fix: última linha não-vazia do stderr (mensagem real)
- **Arquivo:** `scripts/validar-codigo.py`

### validar-escala: fixtures de teste fora do formato EITA numerado (## N.)

- **Causa:** validar-escala: fixtures de teste fora do formato EITA numerado (## N.)
- **Fix:** fix: testes usam ## 1. Introdução / ## 5. Aplica
- **Arquivo:** `tests/test_validar_escala.py`

---

## 3. Arquivos Alterados

_Não informado._

---

## 4. Validações

- pytest -q: 518 passed em 50.50s (67 novos testes)
- python -m py_compile em todos os scripts novos
- auditar-obra --estrito no livro real: 3 gates reprovando (referências 404, escala, afirmações) — comportamento esperado
- Gate de referências no livro real: fin.ai/blog/ai-agent-roi-customer-support -> HTTP 404 (fonte inexistente detectada)
- playbook pbk-1: 13 blocos de código truncados sem elipse (código cortado no meio) detectados por --playbook --executar

---

## 5. Commits

- `1b03708 feat(v5.2): gates de conteúdo sine qua non (F1/F2) + encadeamento --estrito` (pushado em `main`)

---

## 6. Resumo de Entregas

- 6 gates novos + extensão validar-codigo (--executar, --playbook)
- Registro gates_conteudo + encadeamento no auditar-obra --estrito
- Skills atualizadas (pesquisador, revisor-tecnico, estrategista, redator-eita)
- AGENTS.md + RTK scratchpad com aprendizados
- Suíte: 518 testes passando (451 anteriores + 67 novos)

---

*Relatório gerado em 2026-08-09 — Fábrica Agêntica de Publicações*
