# E-mail 06 — O Ciclo ReAct e os Loops de Execução

**Assunto:** Chamada única "direta ao modelo"**: sem loop, sem…
**Momento:** dia 10

---

A armadilha desta etapa: **Chamada única "direta ao modelo"**: sem loop, sem observação, sem correção de curso — o agente é um LLM com prompt bonito [4]**

Construir o primeiro harness funcional: o loop Reason → Act → Observe com execução de ferramentas, tratamento de erro e iteração até o objetivo.

Uma chamada direta ao modelo é um LLM com prompt bonito: sem loop, sem observação, sem correção de curso. Nesta etapa você monta o ciclo Reason → Act → Observe com teto de iterações. O agente passa a aprender com a execução — e a parar quando o objetivo é atingido.

O teste de uma linha que confirma que deu certo:

```bash
python scripts/validar-codigo.py livros/harness-engineering --capitulo 5 --executar
```

Entrega desta etapa: `loop/reat.py`

[Ver o passo completo](https://exemplo.com/obra?utm_source=email&utm_medium=sequencia&utm_campaign=harness-engineering&utm_content=email-06)

*Passo 5 de 8 da sequência.*

---
