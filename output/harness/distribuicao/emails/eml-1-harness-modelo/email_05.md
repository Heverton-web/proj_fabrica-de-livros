# E-mail 05 — Safety Harness e Guardrails: A Camada Que Impede a Queda

**Assunto:** Segurança no prompt**: "por favor, não apague nada" não é…
**Momento:** dia 8

---

A armadilha desta etapa: **Segurança no prompt**: "por favor, não apague nada" não é guardrail; é sugestão [20]**

Mostrar como proteger o sistema contra ações destrutivas do agente — aprovações humanas, limites de escopo, bloqueio de tool calls e princípio do menor privilégio.

"Por favor, não apague nada" é sugestão, não guardrail. Aqui você declara a zona de atuação do agente e as regras fail-closed: ação não reconhecida é bloqueada, nunca deixada passar por falta de previsão. O capacete não negocia — ele impede a queda.

O teste de uma linha que confirma que deu certo:

```bash
python scripts/validar-codigo.py livros/harness-engineering --capitulo 4 --executar
```

Entrega desta etapa: `config/guardrails.yaml`

[Ver o passo completo](https://exemplo.com/obra?utm_source=email&utm_medium=sequencia&utm_campaign=harness-engineering&utm_content=email-05)

*Passo 4 de 8 da sequência.*

---
