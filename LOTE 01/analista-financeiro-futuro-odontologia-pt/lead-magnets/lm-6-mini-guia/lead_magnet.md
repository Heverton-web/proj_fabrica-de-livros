---
title: "Mini-guia: O Dentista Gestor: Finanças de Clínica com IA"
subtitle: "O primeiro passo de O Dentista Gestor: Finanças de Clínica com IA, do início ao fim"
author: "Heverton Eduardo Peres"
lang: pt-BR
---

# O Dentista que Virou Gestor

## Por que esta etapa existe

Apresentar o problema estrutural da gestão financeira odontológica (mortalidade de clínicas, falta de formação em gestão) e posicionar a IA gratuita como o novo colega de bancada do dentista.

<!-- POLIMENTO-LLM: 2 parágrafos de contexto condensados da §2 Explica do capítulo 1 do livro-mãe. Máx. 180 palavras. -->

## O que você vai produzir

- `caixa_clinica.csv`
- `contas_a_pagar.csv`
- `pacientes_faturamento.csv`
- `kpis_mensais.csv`

## Passo a passo

### O primeiro controle: a planilha do caixa da clínica

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

### Pedindo a planilha ao assistente

```text
Atue como um consultor financeiro de clinicas odontologicas.
Vou colar abaixo os lancamentos do fluxo de caixa da minha clinica.
1. Calcule o total de entradas e o total de saidas do mes.
2. Calcule o saldo final do caixa.
3. Separe as despesas por categoria (Custo fixo, Suprimento, Pessoal, Equipamento).
4. Identifique qual categoria mais consome o caixa.
5. Mostre os calculos passo a passo, sem pular etapas.
```

### Automatizando com Python sem instalar nada

```python
import pandas as pd

```

## Como saber se deu certo

```bash
python -c "import pandas as pd; df = pd.read_csv('caixa_clinica.csv'); print('Entradas:', df['Entrada'].fillna(0).sum(), '| Saidas:', df['Saida'].fillna(0).sum()); print('OK: caixa conferido')"
```

Está pronto quando:

- [ ] Liste as três despesas fixas da sua clínica (ou da clínica que você vai montar) e seus valores mensais
- [ ] Calcule o ticket médio do último mês: faturamento ÷ pacientes atendidos. Se você não tem o número, estime com os dados que tiver
- [ ] Abra o assistente de IA gratuito e peça: "monte uma planilha de fluxo de caixa para uma clínica odontológica com as colunas Data, Descrição, Categoria, Entrada, Saída e as categorias Procedimento, Plano, Custo fixo, Suprimento, Pessoal, Equipamento. Explique cada coluna."
- [ ] Escreva em uma frase qual é o seu pró-labore mensal — se você não tem um, esse é o seu primeiro projeto do livro

## Armadilhas desta etapa

- Misturar as contas da clinica com as pessoais — inviabiliza qualquer leitura financeira
- Pular a conferência do número gerado pela IA — chute vira decisão
- Enviar dados de pacientes para a nuvem sem anonimizar (LGPD)
- Aceitar a primeira resposta do chat sem pedir o cálculo


# Próximo passo

Este material é um recorte de **O Dentista Gestor: Finanças de Clínica com IA**. A obra completa traz a teoria, os exemplos comentados e as referências.

> **Quero a obra completa** — https://seu-site.com.br/ia?utm_source=lead-magnet&utm_medium=pdf&utm_campaign=analista-financeiro-futuro-odontologia&utm_content=mini-guia
