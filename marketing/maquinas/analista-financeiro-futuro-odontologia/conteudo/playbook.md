---
title: "Playbook — O Dentista Gestor: Finanças de Clínica com IA"
subtitle: "Guia de bancada · 4 passos práticos"
author: "Heverton Eduardo Peres"
lang: pt-BR
---

# Objetivo do Material

O cirurgião-dentista é formado para clinicar, não para gerir. Entre a última consulta do dia e a primeira do amanhã existe um expediente invisível: o dos números. Este livro ensina o dentista dono de clínica a assumir esse expediente com ferramentas de IA gratuitas — planilhas, chats e dashboards — para transformar caos financeiro em comando. Cada capítulo combina teoria curta, exemplo prático, código executável e referências verificáveis.

# Como usar este playbook

Você é o **Gestor de Clínica Odontológica**. Cada passo é um card independente com sete partes: objetivo, pré-requisito, entregas, execução, gate de verificação, critério de conclusão e armadilhas.

Este documento **não repete a teoria** do livro. Quando precisar do porquê, siga a referência cruzada do card para o capítulo correspondente.

# Mapa dos Estágios

| # | Estágio | Passos |
|---|---|---|
| 1 | Fim de expediente | 1, 2, 3, 4 |

# Passos Práticos

## Passo 1 — O Dentista que Virou Gestor

> **Estágio:** Fim de expediente  ·  **Origem:** Cap. 1 — O Dentista que Virou Gestor

### ① Objetivo do passo

Apresentar o problema estrutural da gestão financeira odontológica (mortalidade de clínicas, falta de formação em gestão) e posicionar a IA gratuita como o novo colega de bancada do dentista.

### ② Pré-requisito

Nenhum — este é o ponto de partida

### ③ Entregas

- `caixa_clinica.csv`
- `contas_a_pagar.csv`
- `pacientes_faturamento.csv`
- `kpis_mensais.csv`

### ④ Execução

**O primeiro controle: a planilha do caixa da clínica**

```csv
Data,Descricao,Categoria,Entrada,Saida
2026-01-05,Consulta limpeza,Procedimento,250.00,
2026-01-08,Restauracao,Procedimento,350.00,
2026-01-10,Compra material,Suprimento,,180.00
2026-01-12,Aluguel,Custo fixo,,3200.00
2026-01-15,Plano odontologico repasse,Plano,4200.00,
2026-01-20,Auxiliar salario,Pessoal,,2400.00
2026-01-25,Implantoproteses,Procedimento,4800.00,
2026-01-28,Conta de energia,Custo fixo,,620.00
2026-01-30,Autoclave manutencao,Equipamento,,450.00
```

**Pedindo a planilha ao assistente**

```text
Atue como um consultor financeiro de clinicas odontologicas.
Vou colar abaixo os lancamentos do fluxo de caixa da minha clinica.
1. Calcule o total de entradas e o total de saidas do mes.
2. Calcule o saldo final do caixa.
3. Separe as despesas por categoria (Custo fixo, Suprimento, Pessoal, Equipamento).
4. Identifique qual categoria mais consome o caixa.
5. Mostre os calculos passo a passo, sem pular etapas.
```

**Automatizando com Python sem instalar nada**

```python
import pandas as pd

```

### ⑤ Verificação / Gate

```bash
python -c "import pandas as pd; df = pd.read_csv('caixa_clinica.csv'); print('Entradas:', df['Entrada'].fillna(0).sum(), '| Saidas:', df['Saida'].fillna(0).sum()); print('OK: caixa conferido')"
```

### ⑥ Feito quando…

- [ ] Liste as três despesas fixas da sua clínica (ou da clínica que você vai montar) e seus valores mensais
- [ ] Calcule o ticket médio do último mês: faturamento ÷ pacientes atendidos. Se você não tem o número, estime com os dados que tiver
- [ ] Abra o assistente de IA gratuito e peça: "monte uma planilha de fluxo de caixa para uma clínica odontológica com as colunas Data, Descrição, Categoria, Entrada, Saída e as categorias Procedimento, Plano, Custo fixo, Suprimento, Pessoal, Equipamento. Explique cada coluna."
- [ ] Escreva em uma frase qual é o seu pró-labore mensal — se você não tem um, esse é o seu primeiro projeto do livro

### ⑦ Armadilhas

- Misturar as contas da clinica com as pessoais — inviabiliza qualquer leitura financeira
- Pular a conferência do número gerado pela IA — chute vira decisão
- Enviar dados de pacientes para a nuvem sem anonimizar (LGPD)
- Aceitar a primeira resposta do chat sem pedir o cálculo

## Passo 2 — Os Números da Clínica: Fluxo de Caixa, Ticket Médio e Custos

> **Estágio:** Fim de expediente  ·  **Origem:** Cap. 2 — Os Números da Clínica: Fluxo de Caixa, Ticket Médio e Custos

### ① Objetivo do passo

Ensinar o dentista a reconhecer e organizar as fontes de dados financeiros da clínica: fluxo de caixa, DRE simplificado, ticket médio, custos fixos e variáveis, com padrões de mercado do setor.

### ② Pré-requisito

Passo 1 concluído

### ③ Entregas

- `caixa_clinica.csv`
- `kpis_mensais.csv`

### ④ Execução

**Montando o DRE simplificado na planilha**

```text
Monte uma planilha de DRE simplificado para uma clinica odontologica
com as seguintes linhas e formulas:
1. Receita bruta (soma das entradas de Procedimento e Plano).
2. Deducoes: 8% de impostos sobre a receita bruta (simulacao de Simples Nacional).
3. Receita liquida = Receita bruta - Deducoes.
4. Custos variaveis (Suprimento).
5. Custos fixos (Custo fixo + Pessoal + Equipamento).
6. Resultado = Receita liquida - Custos variaveis - Custos fixos.
7. Margem = Resultado / Receita liquida, em percentual.
Explique cada linha em uma frase.
```

**Automatizando a apuração com Python**

```python
import pandas as pd

df = pd.read_csv("caixa_clinica.csv")

# Receita bruta: procedimentos + planos
receita_bruta = df[df["Categoria"].isin(["Procedimento", "Plano"])]["Entrada"].fillna(0).sum()

# Custos
custos_variaveis = df[df["Categoria"] == "Suprimento"]["Saida"].fillna(0).sum()
custos_fixos = df[df["Categoria"].isin(["Custo fixo", "Pessoal", "Equipamento"])]["Saida"].fillna(0).sum()

```

### ⑤ Verificação / Gate

```bash
python -c "import pandas as pd; df = pd.read_csv('kpis_mensais.csv'); print(df[['mes','margem','inadimplencia']].to_string(index=False))"
```

### ⑥ Feito quando…

- [ ] Calcule o seu ticket médio dos últimos três meses e compare com o padrão do setor
- [ ] Monte o DRE do mês (receita bruta, deduções, custos, resultado, margem) na planilha
- [ ] Calcule o custo por sessão da sua cadeira
- [ ] Responda com o assistente de IA: "qual a minha necessidade de capital de giro se meu custo fixo mensal é R$ X e meus recebimentos de convênio levam 45 dias?"
- [ ] Registre tudo no `kpis_mensais.csv` — o Capítulo 4 vai transformar esses números em um painel

### ⑦ Armadilhas

- Precificar sem o custo real por sessão — preço do concorrente ignora sua estrutura
- Decidir com um mês isolado — a sazonalidade engana
- Tratar fluxo de caixa como lucro — parcelamentos presos no caixa
- Ignorar o capital de giro — atraso de convênio vira emergência

## Passo 3 — IA na Bancada: Modelos Gratuitos e Planilhas

> **Estágio:** Fim de expediente  ·  **Origem:** Cap. 3 — IA na Bancada: Modelos Gratuitos e Planilhas

### ① Objetivo do passo

Capacitar o dentista a usar ChatGPT, Gemini, Copilot e planilhas para montar controles financeiros: prompts de modelagem, fórmulas geradas, upload de dados e anonimização (LGPD).

### ② Pré-requisito

Passo 2 concluído

### ③ Entregas

- `pacientes_faturamento.csv`

### ④ Execução

**O prompt mestre de modelagem**

```text
Atue como um consultor financeiro senior de clinicas odontologicas.
Antes de gerar qualquer formula, descreva a arquitetura da planilha de
[controle financeiro mensal da clinica] que vou construir no Excel.
Inclua:
1. As abas necessarias e a funcao de cada uma (ex.: Caixa, DRE, Pacientes, KPIs).
2. As colunas e linhas de cada aba.
3. As premissas que devem ficar separadas das formulas (ex.: aliquota do Simples).
4. As regras de calculo (ex.: ticket medio = receita / pacientes).
Depois de eu aprovar a arquitetura, gere as formulas uma por uma,
explicando o que cada uma faz. Nao pule etapas.
```

**Gerando fórmulas específicas**

```text
No Excel, quero calcular o ticket medio mensal: a receita total (soma
da coluna B da aba Caixa, filtrada pelo mes) dividida pelo numero de
pacientes atendidos (contagem na aba Pacientes). Escreva a formula,
explique o que ela faz e aponte onde usar referencias absolutas.
```

**O ciclo de correção dirigida**

```text
A formula da celula F12 do meu DRE esta retornando #VALOR!.
Explique a cadeia de formulas que alimenta F12, identifique a causa
mais provavel e proponha a correcao minima, sem alterar as demais
celulas. Mostre a formula corrigida e o que ela faz.
```

### ⑤ Verificação / Gate

```bash
python -c "print('Gate: confira que pacientes_faturamento.csv tem apenas colunas anonimizadas (codigo, procedimento, valor, mes) antes de qualquer upload')"
```

### ⑥ Feito quando…

- [ ] Abra o assistente gratuito e rode o prompt mestre de modelagem para o seu controle financeiro
- [ ] Aprove a arquitetura (ou peça ajustes) e gere a fórmula do ticket médio
- [ ] Anonimize uma planilha de pacientes de exemplo com o código do capítulo
- [ ] Se tiver um dado confidencial, rode a classificação de lançamentos no modelo local (Ollama)
- [ ] Escreva em uma linha: "o que pode ir à nuvem e o que fica na clínica" — e cumpra

### ⑦ Armadilhas

- Enviar planilha com nome, CPF e prontuário ao chat sem anonimizar
- Pedir a planilha inteira em um único prompt, sem arquitetura
- Aceitar fórmula com valores fixos embutidos — quebra a sensibilidade
- Tratar a IA como oráculo — ela inventa com confiança (alucinação)

## Passo 4 — Do Caos ao Comando: KPIs, Dashboards e Decisão

> **Estágio:** Fim de expediente  ·  **Origem:** Cap. 4 — Do Caos ao Comando: KPIs, Dashboards e Decisão

### ① Objetivo do passo

Consolidar KPIs odontológicos (ticket médio, inadimplência, receita por cadeira, margem), dashboards gratuitos, alertas e o papel humano na decisão — fechando com conformidade (CNES, Simples Nacional, LGPD).

### ② Pré-requisito

Passo 3 concluído

### ③ Entregas

- `caixa_clinica.csv`
- `kpis_mensais.csv`

### ④ Execução

**Montando o painel de KPIs com Python**

```python
import pandas as pd

# Dados mensais (arquivo kpis_mensais.csv do capitulo 2)
df = pd.read_csv("kpis_mensais.csv")

# KPIs por mes
df["margem"] = (df["resultado"] / df["receita_liquida"]) * 100
df["custo_fixo_pct"] = (df["custo_fixo"] / df["receita_bruta"]) * 100
df["ticket_medio"] = df["receita_bruta"] / df["pacientes"]
df["receita_por_cadeira"] = df["receita_bruta"] / df["cadeiras"]

print(df[["mes", "margem", "custo_fixo_pct", "ticket_medio", "receita_por_cadeira"]].to_string(index=False))

# Semafaro (regras de mercado do setor)
def semaforo(margem, inadimplencia):
    if margem >= 20 and inadimplencia < 5:
        return "VERDE"
    if margem >= 15 and inadimplencia < 10:
        return "AMARELO"
    return "VERMELHO"

ultimo = df.iloc[-1]
print(f"\nSemafaro do mes: {semaforo(ultimo['margem'], ultimo['inadimplencia'])}")
```

### ⑤ Verificação / Gate

```bash
python -c "import pandas as pd; df = pd.read_csv('kpis_mensais.csv'); m = df['margem'].iloc[-1]; print('Margem do mes:', m, '%', '| Semafaro:', 'VERDE' if m >= 20 else 'AMARELO' if m >= 15 else 'VERMELHO')"
```

### ⑥ Feito quando…

- [ ] Calcule os KPIs dos seus últimos três meses (margem, ticket médio, inadimplência, custos fixos, receita por cadeira)
- [ ] Monte o semáforo do último mês com as regras do setor
- [ ] Crie o dashboard gratuito (Looker Studio ou Power BI) e conecte os dados
- [ ] Gere com a IA o resumo executivo do mês e confira cada número
- [ ] Escreva a sua única ação da semana com base no painel

### ⑦ Armadilhas

- Mostrar 50 KPIs sem hierarquia — ninguém lê, ninguém decide
- Ignorar os semáforos — o painel deixa de guiar o olhar
- Delegar a decisão à IA — a responsabilidade é do gestor
- Suspender a rotina na correria — o método morre na primeira semana

# Checklist Mestre

**Passo 1 — O Dentista que Virou Gestor**

- [ ] Liste as três despesas fixas da sua clínica (ou da clínica que você vai montar) e seus valores mensais
- [ ] Calcule o ticket médio do último mês: faturamento ÷ pacientes atendidos. Se você não tem o número, estime com os dados que tiver
- [ ] Abra o assistente de IA gratuito e peça: "monte uma planilha de fluxo de caixa para uma clínica odontológica com as colunas Data, Descrição, Categoria, Entrada, Saída e as categorias Procedimento, Plano, Custo fixo, Suprimento, Pessoal, Equipamento. Explique cada coluna."
- [ ] Escreva em uma frase qual é o seu pró-labore mensal — se você não tem um, esse é o seu primeiro projeto do livro

**Passo 2 — Os Números da Clínica: Fluxo de Caixa, Ticket Médio e Custos**

- [ ] Calcule o seu ticket médio dos últimos três meses e compare com o padrão do setor
- [ ] Monte o DRE do mês (receita bruta, deduções, custos, resultado, margem) na planilha
- [ ] Calcule o custo por sessão da sua cadeira
- [ ] Responda com o assistente de IA: "qual a minha necessidade de capital de giro se meu custo fixo mensal é R$ X e meus recebimentos de convênio levam 45 dias?"
- [ ] Registre tudo no `kpis_mensais.csv` — o Capítulo 4 vai transformar esses números em um painel

**Passo 3 — IA na Bancada: Modelos Gratuitos e Planilhas**

- [ ] Abra o assistente gratuito e rode o prompt mestre de modelagem para o seu controle financeiro
- [ ] Aprove a arquitetura (ou peça ajustes) e gere a fórmula do ticket médio
- [ ] Anonimize uma planilha de pacientes de exemplo com o código do capítulo
- [ ] Se tiver um dado confidencial, rode a classificação de lançamentos no modelo local (Ollama)
- [ ] Escreva em uma linha: "o que pode ir à nuvem e o que fica na clínica" — e cumpra

**Passo 4 — Do Caos ao Comando: KPIs, Dashboards e Decisão**

- [ ] Calcule os KPIs dos seus últimos três meses (margem, ticket médio, inadimplência, custos fixos, receita por cadeira)
- [ ] Monte o semáforo do último mês com as regras do setor
- [ ] Crie o dashboard gratuito (Looker Studio ou Power BI) e conecte os dados
- [ ] Gere com a IA o resumo executivo do mês e confira cada número
- [ ] Escreva a sua única ação da semana com base no painel
