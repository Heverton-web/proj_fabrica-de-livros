# E-mail 03 — Anatomia de um Harness: O Corpo Que Carrega o Cérebro

**Assunto:** Ambiente compartilhado "para simplificar"**: rodar o…
**Momento:** dia 4

---

A armadilha desta etapa: **Ambiente compartilhado "para simplificar"**: rodar o agente com as mesmas permissões do operador transforma qualquer erro em incidente de segurança; o isolamento é a primeira linha [7][17]**

Dissecar as camadas do harness — ambiente de execução, ferramentas, memória, estado e loops de feedback — mostrando cada peça com exemplo concreto.

Ambiente compartilhado significa que um erro vira incidente. A solução é declarar cada peça do arnês — ferramentas, memória, estado — na configuração, em vez de deixar o agente improvisar. Você separa o corpo do cérebro: o modelo decide, o harness executa.

O teste de uma linha que confirma que deu certo:

```bash
python scripts/validar-codigo.py livros/harness-engineering --capitulo 2 --executar
```

Entrega desta etapa: `tests/test_contrato.py`

[Ver o passo completo](https://exemplo.com/obra?utm_source=email&utm_medium=sequencia&utm_campaign=harness-engineering&utm_content=email-03)

*Passo 2 de 8 da sequência.*

---
