---
title: "Cheat Sheet: O Dentista Gestor: Finanças de Clínica com IA"
subtitle: "Todos os comandos de O Dentista Gestor: Finanças de Clínica com IA em uma folha de bancada"
author: "Heverton Eduardo Peres"
lang: pt-BR
---

# Folha de bancada

Todos os comandos, na ordem de execução. Imprima e deixe ao lado do teclado.

## Etapa 1 — O Dentista que Virou Gestor

```bash
python -c "import pandas as pd; df = pd.read_csv('caixa_clinica.csv'); print('Entradas:', df['Entrada'].fillna(0).sum(), '| Saidas:', df['Saida'].fillna(0).sum()); print('OK: caixa conferido')"
```

*Verificação:* `python -c "import pandas as pd; df = pd.read_csv('caixa_clinica.csv'); print('Entradas:', df['Entrada'].fillna(0).sum(), '| Saidas:', df['Saida'].fillna(0).sum()); print('OK: caixa conferido')"`

## Etapa 2 — Os Números da Clínica: Fluxo de Caixa, Ticket Médio e Custos

```bash
python -c "import pandas as pd; df = pd.read_csv('kpis_mensais.csv'); print(df[['mes','margem','inadimplencia']].to_string(index=False))"
```

*Verificação:* `python -c "import pandas as pd; df = pd.read_csv('kpis_mensais.csv'); print(df[['mes','margem','inadimplencia']].to_string(index=False))"`

## Etapa 3 — IA na Bancada: Modelos Gratuitos e Planilhas

```bash
python -c "print('Gate: confira que pacientes_faturamento.csv tem apenas colunas anonimizadas (codigo, procedimento, valor, mes) antes de qualquer upload')"
```

*Verificação:* `python -c "print('Gate: confira que pacientes_faturamento.csv tem apenas colunas anonimizadas (codigo, procedimento, valor, mes) antes de qualquer upload')"`

## Etapa 4 — Do Caos ao Comando: KPIs, Dashboards e Decisão

```bash
python -c "import pandas as pd; df = pd.read_csv('kpis_mensais.csv'); m = df['margem'].iloc[-1]; print('Margem do mes:', m, '%', '| Semafaro:', 'VERDE' if m >= 20 else 'AMARELO' if m >= 15 else 'VERMELHO')"
```

*Verificação:* `python -c "import pandas as pd; df = pd.read_csv('kpis_mensais.csv'); m = df['margem'].iloc[-1]; print('Margem do mes:', m, '%', '| Semafaro:', 'VERDE' if m >= 20 else 'AMARELO' if m >= 15 else 'VERMELHO')"`


## Etapa 5 - Apurar o DRE do mes



## Etapa 6 - Calcular o ticket medio



# Próximo passo

Este material é um recorte de **O Dentista Gestor: Finanças de Clínica com IA**. A obra completa traz a teoria, os exemplos comentados e as referências.

> **Quero a obra completa** — https://seu-site.com.br/ia?utm_source=lead-magnet&utm_medium=pdf&utm_campaign=analista-financeiro-futuro-odontologia&utm_content=cheatsheet
