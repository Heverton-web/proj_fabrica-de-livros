---
title: "Mapa de Entregas: O Dentista Gestor: Finanças de Clínica com IA"
subtitle: "Todos os artefatos que você produz em O Dentista Gestor: Finanças de Clínica com IA"
author: "Heverton Eduardo Peres"
lang: pt-BR
---

# O que você produz

Cada etapa entrega artefatos concretos. Esta é a lista completa — use como inventário do projeto.

| Etapa | Entrega | Verificação |
|---|---|---|
| 1 | `caixa_clinica.csv` | `python -c "import pandas as pd; df = pd.read_csv('caixa_clinica.csv'); print('Entradas:', df['Entrada'].fillna(0).sum(), '| Saidas:', df['Saida'].fillna(0).sum()); print('OK: caixa conferido')"` |
| 1 | `contas_a_pagar.csv` | `python -c "import pandas as pd; df = pd.read_csv('caixa_clinica.csv'); print('Entradas:', df['Entrada'].fillna(0).sum(), '| Saidas:', df['Saida'].fillna(0).sum()); print('OK: caixa conferido')"` |
| 1 | `pacientes_faturamento.csv` | `python -c "import pandas as pd; df = pd.read_csv('caixa_clinica.csv'); print('Entradas:', df['Entrada'].fillna(0).sum(), '| Saidas:', df['Saida'].fillna(0).sum()); print('OK: caixa conferido')"` |
| 1 | `kpis_mensais.csv` | `python -c "import pandas as pd; df = pd.read_csv('caixa_clinica.csv'); print('Entradas:', df['Entrada'].fillna(0).sum(), '| Saidas:', df['Saida'].fillna(0).sum()); print('OK: caixa conferido')"` |
| 2 | `caixa_clinica.csv` | `python -c "import pandas as pd; df = pd.read_csv('kpis_mensais.csv'); print(df[['mes','margem','inadimplencia']].to_string(index=False))"` |
| 2 | `kpis_mensais.csv` | `python -c "import pandas as pd; df = pd.read_csv('kpis_mensais.csv'); print(df[['mes','margem','inadimplencia']].to_string(index=False))"` |
| 3 | `pacientes_faturamento.csv` | `python -c "print('Gate: confira que pacientes_faturamento.csv tem apenas colunas anonimizadas (codigo, procedimento, valor, mes) antes de qualquer upload')"` |
| 4 | `caixa_clinica.csv` | `python -c "import pandas as pd; df = pd.read_csv('kpis_mensais.csv'); m = df['margem'].iloc[-1]; print('Margem do mes:', m, '%', '| Semafaro:', 'VERDE' if m >= 20 else 'AMARELO' if m >= 15 else 'VERMELHO')"` |
| 4 | `kpis_mensais.csv` | `python -c "import pandas as pd; df = pd.read_csv('kpis_mensais.csv'); m = df['margem'].iloc[-1]; print('Margem do mes:', m, '%', '| Semafaro:', 'VERDE' if m >= 20 else 'AMARELO' if m >= 15 else 'VERMELHO')"` |


# Próximo passo

Este material é um recorte de **O Dentista Gestor: Finanças de Clínica com IA**. A obra completa traz a teoria, os exemplos comentados e as referências.

> **Quero a obra completa** — https://seu-site.com.br/ia?utm_source=lead-magnet&utm_medium=pdf&utm_campaign=analista-financeiro-futuro-odontologia&utm_content=entregas
