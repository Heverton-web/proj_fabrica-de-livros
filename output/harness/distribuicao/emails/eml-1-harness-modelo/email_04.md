# E-mail 04 — Test Harness: A Herança da Engenharia de Software

**Assunto:** Confiar na autoavaliação do modelo**: "o agente disse que…
**Momento:** dia 6

---

A armadilha desta etapa: **Confiar na autoavaliação do modelo**: "o agente disse que completou" não é evidência; é narrativa [18]**

Apresentar o harness de teste — fixtures, execução determinística, linters e CI — como a primeira linha de verificação do trabalho do agente.

"O agente disse que completou" não é evidência. Nesta etapa você cria a régua de qualidade que mede a resposta antes de aceitá-la: relevância, completude, segurança e rastreabilidade. Uma linha de comando confirma — ou reprova — sem depender de autoavaliação.

O teste de uma linha que confirma que deu certo:

```bash
python scripts/validar-codigo.py livros/harness-engineering --capitulo 3 --executar
```

Entrega desta etapa: `evals/regua.py`

[Ver o passo completo](https://exemplo.com/obra?utm_source=email&utm_medium=sequencia&utm_campaign=harness-engineering&utm_content=email-04)

*Passo 3 de 8 da sequência.*

---
