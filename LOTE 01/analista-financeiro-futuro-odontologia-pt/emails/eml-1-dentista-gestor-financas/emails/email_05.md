# E-mail 05 — Do Caos ao Comando: KPIs, Dashboards e Decisão

**Assunto:** Mostrar 50 KPIs sem hierarquia — ninguém lê, ninguém decide
**Momento:** dia 8

---

A armadilha desta etapa: **Mostrar 50 KPIs sem hierarquia — ninguém lê, ninguém decide**

Consolidar KPIs odontológicos (ticket médio, inadimplência, receita por cadeira, margem), dashboards gratuitos, alertas e o papel humano na decisão — fechando com conformidade (CNES, Simples Nacional, LGPD).

<!-- POLIMENTO-LLM: 1 parágrafo conectando a armadilha ao passo prático. Máx. 90 palavras, segunda pessoa. -->

O teste de uma linha que confirma que deu certo:

```bash
python -c "import pandas as pd; df = pd.read_csv('kpis_mensais.csv'); m = df['margem'].iloc[-1]; print('Margem do mes:', m, '%', '| Semafaro:', 'VERDE' if m >= 20 else 'AMARELO' if m >= 15 else 'VERMELHO')"
```

Entrega desta etapa: `caixa_clinica.csv`

[Ver o passo completo](https://seu-site.com.br/ia?utm_source=email&utm_medium=sequencia&utm_campaign=analista-financeiro-futuro-odontologia&utm_content=email-05)

*Passo 4 de 4 da sequência.*

---
