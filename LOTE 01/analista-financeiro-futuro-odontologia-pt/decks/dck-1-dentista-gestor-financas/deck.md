---
title: "O Dentista Gestor: Finanças de Clínica com IA"
subtitle: "Apresentação · Gestor de Clínica Odontológica"
author: "Heverton Eduardo Peres"
lang: pt-BR
---

# Objetivo

O cirurgião-dentista é formado para clinicar, não para gerir. Entre a última consulta do dia e a primeira do amanhã existe um expediente invisível: o dos números. Este livro ensina o dentista dono de clínica a assumir esse expediente com ferramentas de IA gratuitas — planilhas, chats e dashboards — para transformar caos financeiro em comando. Cada capítulo combina teoria curta, exemplo prático, código executável e referências verificáveis.

# O caminho

- **Fim de expediente** — capítulos 1, 2, 3, 4

# Fim de Expediente: O Dentista Gestor

> Estágio 1 de 1

# O Dentista que Virou Gestor

*Apresentar o problema estrutural da gestão financeira odontológica (mortalidade de clínicas, falta de formação em gestão) e posicionar a IA gratuita como o…*

- Liste as três despesas fixas da sua clínica (ou da clínica que você vai montar) e seus valores mensais
- Calcule o ticket médio do último mês: faturamento ÷ pacientes atendidos. Se você não tem o número, estime com…
- Abra o assistente de IA gratuito e peça: "monte uma planilha de fluxo de caixa para uma clínica odontológica…
- Escreva em uma frase qual é o seu pró-labore mensal — se você não tem um, esse é o seu primeiro projeto do…

`python -c "import pandas as pd; df = pd.read_csv('caixa_clinica.csv'); print('Entradas:', df['Entrada'].fillna(0).sum(), '| Saidas:', df['Saida'].fillna(0).sum()); print('OK: caixa conferido')"`

# Os Números da Clínica: Fluxo de Caixa, Ticket Médio e Custos

*Ensinar o dentista a reconhecer e organizar as fontes de dados financeiros da clínica: fluxo de caixa, DRE simplificado, ticket médio, custos fixos e…*

- Calcule o seu ticket médio dos últimos três meses e compare com o padrão do setor
- Monte o DRE do mês (receita bruta, deduções, custos, resultado, margem) na planilha
- Calcule o custo por sessão da sua cadeira
- Responda com o assistente de IA: "qual a minha necessidade de capital de giro se meu custo fixo mensal é R$ X…

`python -c "import pandas as pd; df = pd.read_csv('kpis_mensais.csv'); print(df[['mes','margem','inadimplencia']].to_string(index=False))"`

# IA na Bancada: Modelos Gratuitos e Planilhas

*Capacitar o dentista a usar ChatGPT, Gemini, Copilot e planilhas para montar controles financeiros: prompts de modelagem, fórmulas geradas, upload de dados e…*

- Abra o assistente gratuito e rode o prompt mestre de modelagem para o seu controle financeiro
- Aprove a arquitetura (ou peça ajustes) e gere a fórmula do ticket médio
- Anonimize uma planilha de pacientes de exemplo com o código do capítulo
- Se tiver um dado confidencial, rode a classificação de lançamentos no modelo local (Ollama)

`python -c "print('Gate: confira que pacientes_faturamento.csv tem apenas colunas anonimizadas (codigo, procedimento, valor, mes) antes de qualquer upload')"`

# Do Caos ao Comando: KPIs, Dashboards e Decisão

*Consolidar KPIs odontológicos (ticket médio, inadimplência, receita por cadeira, margem), dashboards gratuitos, alertas e o papel humano na decisão — fechando…*

- Calcule os KPIs dos seus últimos três meses (margem, ticket médio, inadimplência, custos fixos, receita por…
- Monte o semáforo do último mês com as regras do setor
- Crie o dashboard gratuito (Looker Studio ou Power BI) e conecte os dados
- Gere com a IA o resumo executivo do mês e confira cada número

`python -c "import pandas as pd; df = pd.read_csv('kpis_mensais.csv'); m = df['margem'].iloc[-1]; print('Margem do mes:', m, '%', '| Semafaro:', 'VERDE' if m >= 20 else 'AMARELO' if m >= 15 else 'VERMELHO')"`

# Próximo passo

**O Dentista Gestor: Finanças de Clínica com IA**

Leia a obra completa — https://seu-site.com.br/ia?utm_source=deck&utm_medium=slides&utm_campaign=analista-financeiro-futuro-odontologia
