# E-mail 07 — Sandboxes, Permissões e o Controle de Execução

**Assunto:** Credenciais do operador**: o agente com as permissões de…
**Momento:** dia 12

---

A armadilha desta etapa: **Credenciais do operador**: o agente com as permissões de quem o invoca é o incidente mais previsível do harness [17]**

Implementar isolamento real de execução — contêineres, permissões por escopo e políticas — para que o agente faça muito sem poder fazer qualquer coisa.

Credenciais do operador para o agente é o incidente mais previsível do harness. Aqui você mapeia ação → zona → política: leitura é livre, escrita é controlada, ação destrutiva exige humano. O agente passa a fazer muito — sem poder fazer qualquer coisa.

O teste de uma linha que confirma que deu certo:

```bash
python scripts/validar-codigo.py livros/harness-engineering --capitulo 6 --executar
```

Entrega desta etapa: `config/zonas.json`

[Ver o passo completo](https://exemplo.com/obra?utm_source=email&utm_medium=sequencia&utm_campaign=harness-engineering&utm_content=email-07)

*Passo 6 de 8 da sequência.*

---
