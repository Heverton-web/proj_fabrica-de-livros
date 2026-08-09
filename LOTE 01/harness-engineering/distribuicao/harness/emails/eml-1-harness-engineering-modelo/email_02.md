# E-mail 02 — A Revolução dos Agentes: Por Que o Modelo Não Basta

**Assunto:** "O modelo é tão bom que não precisa de teste"**: o DORA…
**Momento:** dia 2

---

A armadilha desta etapa: **"O modelo é tão bom que não precisa de teste"**: o DORA 2024 mostrou exatamente o contrário — produtividade individual sem estabilidade de entrega é um custo escondido [9]**

Explicar por que LLMs sozinhos não produzem trabalho confiável e introduzir a equação Agente = Modelo + Harness, com o mapa do que será construído na obra.

A produtividade sem estabilidade é um custo escondido — e o teste é a âncora que transforma a narrativa em evidência. Nesta etapa, você escreve o teste determinístico da sua tarefa crítica antes de qualquer prompt. Se o agente erra, o teste acusa; se acerta, você tem prova, não intuição.

O teste de uma linha que confirma que deu certo:

```bash
python scripts/validar-codigo.py livros/harness-engineering --capitulo 1 --executar
```

Entrega desta etapa: `AGENTS.md`

[Ver o passo completo](https://exemplo.com/obra?utm_source=email&utm_medium=sequencia&utm_campaign=harness-engineering&utm_content=email-02)

*Passo 1 de 8 da sequência.*

---
