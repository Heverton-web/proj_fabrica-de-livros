---
title: "Playbook — Dashboards Impressionantes - Utilizando Cérebros Criativos (LLMs)"
subtitle: "Guia de bancada · 4 passos práticos"
author: "Heverton Eduardo Peres"
lang: pt-BR
---

# Objetivo do Material

Apresentar o problema da poluição de dados nos relatórios financeiros e a promessa de dashboards que a diretoria lê em 5 segundos.

# Como usar este playbook

Você é o **Piloto Financeiro**. Cada passo é um card independente com sete partes: objetivo, pré-requisito, entregas, execução, gate de verificação, critério de conclusão e armadilhas.

Este documento **não repete a teoria** do livro. Quando precisar do porquê, siga a referência cruzada do card para o capítulo correspondente.

# Mapa dos Estágios

| # | Estágio | Passos |
|---|---|---|
| 1 | Painel | 1, 2 |
| 2 | Instrumento | 3, 4 |

# Passos Práticos

## Passo 1 — O Design da Clareza Analítica

> **Estágio:** Painel  ·  **Origem:** Cap. 1 — O Design da Clareza Analítica

### ① Objetivo do passo

Ensinar o leitor a pedir para a IA desenhar o esqueleto perfeito do dashboard, com dados em formato de lista para leitura rápida.

### ② Pré-requisito

Nenhum — este é o ponto de partida

### ③ Entregas

- _(a completar)_

### ④ Execução

**Construindo a Representação Intermediária com Python**

```python
import json
from datetime import datetime

# === DADOS BRUTOS (simulando export de ERP) ===
vendas_brutas = [
    {"data": "2026-01-15", "cliente": "Clínica Sorriso", "produto": "Pontas Escovadas", "valor": 2400, "quantidade": 120},
    {"data": "2026-01-20", "cliente": "OdontoVida", "produto": "Limas Endodônticas", "valor": 1800, "quantidade": 60},
    {"data": "2026-02-03", "cliente": "Clínica Sorriso", "produto": "Resina Composta", "valor": 3200, "quantidade": 200},
    {"data": "2026-02-10", "cliente": "Dental Premium", "produto": "Agulhas Descartáveis", "valor": 950, "quantidade": 500},
    {"data": "2026-02-18", "cliente": "OdontoVida", "produto": "Pontas Escovadas", "valor": 2100, "quantidade": 105},
    {"data": "2026-03-05", "cliente": "Clínica Sorriso", "produto": "Limas Endodônticas", "valor": 2700, "quantidade": 90},
    {"data": "2026-03-12", "cliente": "Dental Premium", "produto": "Resina Composta", "valor": 4100, "quantidade": 260},
    {"data": "2026-03-20", "cliente": "OdontoVida", "produto": "Agulhas Descartáveis", "valor": 1200, "quantidade": 600},
]

# === REPRESENTAÇÃO INTERMEDIÁRIA ===
def gerar_ir(vendas):
    """Gera estrutura intermediária de dashboard a partir de dados brutos."""
    
    # KPIs consolidados
    faturacao_total = sum(v["valor"] for v in vendas)
    num_pedidos = len(vendas)
    ticket_medio = faturacao_total / num_pedidos if num_pedidos > 0 else 0
    
    # Único cliente (para demonstração — em produção, agrupar por cliente)
    clientes_unicos = list(set(v["cliente"] for v in vendas))
    
    # Primeiro e último pedido (formato 
```

**Prompt Template para IA Gerar Esqueleto de Dashboard**

```markdown
# Prompt: Esqueleto de Dashboard em Formato Lista

Você é um analista financeiro especializado em dashboards executivos.
Receba os seguintes dados em formato lista e gere um esqueleto de dashboard
que um Diretor Financeiro possa ler em 5 segundos.

## Dados de Entrada
[Liste aqui seus dados em formato de tabela ou lista simples]

## Regras de Design (OBRIGATÓRIAS)
1. Formato: LISTA VERTICAL (nunca lado a lado)
2. Máximo 5 KPIs visíveis simultaneamente
3. Cores semânticas: verde = acima da meta, vermelho = abaixo, amarelo = atenção
4. Sem gráficos 3D — apenas barras, linhas ou cards simples
5. Sem legendas — cada dado deve ser autoexplicativo
6. Se precisa de legenda, o design está errado

## Saída Esperada
- JSON com a estrutura do dashboard
- Cada KPI com: nome, valor, tendência, cor sugerida
- Ordem de leitura de cima para baixo
- Indicação de qual KPI é o mais importante (destaque visual)
```

### ⑤ Verificação / Gate

_(a completar)_

### ⑥ Feito quando…

- [ ] Pedir à IA para gerar o dashboard completo de uma vez.** A IA gera código que você não controla. Use a IR: peça a estrutura, valide, depois renderize
- [ ] Ignorar a validação humana.** A IA erra — às vezes coloca o dado certo no lugar errado. Sempre revise antes de enviar ao painel
- [ ] Copiar layout de dashboards genéricos.** Cada empresa tem seus KPIs. O que funciona para um SaaS não funciona para uma distribuidora odontológica B2B

### ⑦ Armadilhas

- _(a completar)_

## Passo 2 — Substituindo a Complexidade pela Praticidade

> **Estágio:** Painel  ·  **Origem:** Cap. 2 — Substituindo a Complexidade pela Praticidade

### ① Objetivo do passo

Eliminar cálculos temporais complexos e substituí-los por cartões visuais diretos mostrando data do primeiro e último pedido.

### ② Pré-requisito

Passo 1 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**Função Python: Convertendo Cálculos Complexos em Cartões**

```python
from datetime import datetime, timedelta
from collections import defaultdict

# === DADOS BRUTOS (export de ERP odontológico) ===
pedidos = [
    {"data": "2023-03-10", "cliente": "Clínica Sorriso", "valor": 2400},
    {"data": "2023-06-22", "cliente": "Clínica Sorriso", "valor": 3100},
    {"data": "2023-09-15", "cliente": "Clínica Sorriso", "valor": 2800},
    {"data": "2024-01-08", "cliente": "Clínica Sorriso", "valor": 3500},
    {"data": "2024-05-20", "cliente": "Clínica Sorriso", "valor": 2900},
    {"data": "2024-09-12", "cliente": "Clínica Sorriso", "valor": 3200},
    {"data": "2025-02-18", "cliente": "Clínica Sorriso", "valor": 4100},
    {"data": "2025-07-05", "cliente": "Clínica Sorriso", "valor": 3800},
    {"data": "2025-11-20", "cliente": "Clínica Sorriso", "valor": 2600},
    {"data": "2026-03-12", "cliente": "Clínica Sorriso", "valor": 4500},
    {"data": "2023-04-05", "cliente": "OdontoVida", "valor": 1800},
    {"data": "2023-08-18", "cliente": "OdontoVida", "valor": 2200},
    {"data": "2024-03-10", "cliente": "OdontoVida", "valor": 1500},
    {"data": "2025-01-25", "cliente": "OdontoVida", "valor": 2000},
]

def calcular_status_pedido(data_str, dias_limite_critico=90):
    """Retorna status: verde (ativo), amarelo (atenção), vermelho (risco)."""
    hoje = datetime.now()
    data_pedido = datetime.strptime(data_str, "%Y-%m-%d")
    dias_desde = (hoje - data_pedido).days
    
    if dias_desde <= 60:
        return "verde", f"Ativo ({dias_desde}d)"
    elif dias_desde <= dias_limite_critico:
        return "amarelo", f"Atenção ({dias_desde}d)"
    else:

```

**Prompt Template para IA Extrair Métricas em Linguagem Natural**

```markdown
# Prompt: Extração de Métricas para KPI Cards

Você é um analista financeiro especializado em dashboards B2B.
Receba a base de dados abaixo e extraia as seguintes métricas
em formato de KPI Cards:

## Métricas Solicitadas
1. Ticket Médio por cliente (Faturação Total ÷ Nº de Pedidos)
2. Data do Primeiro Pedido
3. Data do Último Pedido
4. Volume Total por cliente

## Dados de Entrada
[Liste seus dados aqui]

## Formato de Saída (OBRIGATÓRIO)
Para cada cliente, retorne:
- Nome do cliente
- Ticket Médio: €X.XXX
- Primeiro Pedido: DD/MM/AAAA
- Último Pedido: DD/MM/AAAA
- Volume Total: €XX.XXX
- Status: Verde (ativo) / Amarelo (atenção) / Vermelho (risco)

## Regras de Status
- Verde: último pedido nos últimos 60 dias
- Amarelo: último pedido entre 60-90 dias
- Vermelho: último pedido há mais de 90 dias
```

### ⑤ Verificação / Gate

_(a completar)_

### ⑥ Feito quando…

- [ ] Adicionar mais métricas para "completar" o painel.** Se você tem 15 cartões, não é um dashboard — é uma lista de compras. Mantenha no máximo 5-7 indicadores visíveis
- [ ] Usar cores decorativas em vez de semânticas.** Azul escuro, azul claro e azul médio não comunicam nada. Verde, amarelo e vermelho comunicam status instantaneamente
- [ ] Confundir "simples" com "simplório".** Um cartão com primeiro pedido, último pedido e volume total não é simplório — é cirúrgico. A sofisticação está nos dados que ele comunica, não na quantidade de pixels

### ⑦ Armadilhas

- _(a completar)_

## Passo 3 — Fórmulas Complexas em Segundos

> **Estágio:** Instrumento  ·  **Origem:** Cap. 3 — Fórmulas Complexas em Segundos

### ① Objetivo do passo

Ensinar o leitor a pedir para a IA escrever rotinas VBA e fórmulas de Google Sheets (QUERY, VLOOKUP) para consolidar bases de dados.

### ② Pré-requisito

Passo 2 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**Prompt 1: Macro VBA para Consolidação de Vendas**

```markdown
# Prompt: Macro VBA para Consolidação

Crie uma macro VBA para o Excel que faça o seguinte:
1. Abra todas as planilhas da pasta "Vendas" (formato .xlsx)
2. Copie os dados de cada planilha (exceto cabeçalho) para a aba "Consolidado"
3. Adicione uma coluna "Fonte" com o nome do arquivo de origem
4. Formate o cabeçalho da aba "Consolidado" em negrito com fundo cinza
5. Auto-ajuste a largura das colunas

Planilhas de origem têm estas colunas:
A: Data | B: Cliente | C: Produto | D: Quantidade | E: Valor Unitário | F: Valor Total
```

**Prompt 2: QUERY Google Sheets para Vendas por Período**

```markdown
# Prompt: QUERY para Faturação por Cliente

Tenho uma aba "Pedidos" no Google Sheets com estas colunas:
A: Data do Pedido (formato DD/MM/AAAA)
B: Nome do Cliente
C: Produto
D: Quantidade
E: Valor Total (€)

Preciso de uma QUERY que mostre:
- Faturação total por cliente
- Apenas dos últimos 6 meses
- Ordenada do maior para o menor valor
- Incluindo o número de pedidos de cada cliente
```

**Script Google Apps Script: Consolidação Automática**

```javascript
/**
 * Consolida dados de múltiplas abas em uma aba "Resumo"
 * com QUERY gerada por IA e validação de integridade.
 */
function consolidarDados() {
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var abas = spreadsheet.getSheets();
  var abaResumo = spreadsheet.getSheetByName("Resumo");
  
  // Criar aba Resumo se não existir
  if (!abaResumo) {
    abaResumo = spreadsheet.insertSheet("Resumo");
  } else {
    abaResumo.clear();
  }
  
  // Cabeçalho
  abaResumo.getRange("A1:E1").setValues([["Data", "Cliente", "Produto", "Quantidade", "Valor Total"]]);
  abaResumo.getRange("A1:E1").setFontWeight("bold").setBackground("#C8C8C8");
  
  var linhaAtual = 2;
  
  // Percorrer todas as abas (exceto Resumo)
  for (var i = 0; i < abas.length; i++) {
    var aba = abas[i];
    if (aba.getName() === "Resumo") continue;
    
    var dados = aba.getDataRange().getValues();
    
    // Pular cabeçalho (linha 0)
    for (var j = 1; j < dados.length; j++) {
      if (dados[j][0] !== "" && dados[j][0] !== null) {
        abaResumo.getRange(linhaAtual, 1, 1, 5).setValues([dados[j].slice(0, 5)]);
        linhaAtual++;
      }
    }
  }
  
  // Auto-ajustar
  abaResumo.autoResizeColumns(1, 5);
  
  // Validação de integridade
  var totalRegistros = linhaAtual - 2;
  Logger.log("Consolidação concluída: " + totalRegistros + " registros.");
  
  // Verificar se há dados duplicados (validação básica)
  var range = abaResumo.getRange("A2:E" + (linhaAtual - 1));
  var valores = range.getValues();
  
  var vistos = {};
  var duplicatas = 0;
  
  for (var k = 0; k < valores.length; k++)
```

**Prompt 3: VLOOKUP entre Abas para Dashboard**

```markdown
# Prompt: VLOOKUP para Enriquecimento de Dados

Tenho duas abas no Google Sheets:

Aba "Pedidos":
A: Data | B: ID_Cliente | C: Produto | D: Valor

Aba "Clientes":
A: ID_Cliente | B: Nome | C: Cidade | D: Segmento

Preciso de uma QUERY na aba "Pedidos" que traga automaticamente
o Nome, Cidade e Segmento do cliente para cada pedido,
usando o ID_Cliente como chave.
```

### ⑤ Verificação / Gate

_(a completar)_

### ⑥ Feito quando…

- [ ] Colar a fórmula sem testar.** A IA pode gerar uma QUERY que funciona perfeitamente para os dados de exemplo, mas falha para dados reais com formatação diferente (datas em formato americano, vírgula como separador decimal). Sempre teste com uma amostra
- [ ] Delegar regras de negócio sem explicar.** Se sua empresa tem regras como "considere apenas pedidos acima de €500" ou "desconte devoluções", essas regras precisam estar no prompt. A IA não adivinha
- [ ] Esquecer de validar dados duplicados.** Quando você consolida dados de múltiplas fontes, duplicatas acontecem. Sempre inclua uma verificação de integridade após a consolidação

### ⑦ Armadilhas

- _(a completar)_

## Passo 4 — Seu Primeiro Painel de Saúde do Cliente B2B

> **Estágio:** Instrumento  ·  **Origem:** Cap. 4 — Seu Primeiro Painel de Saúde do Cliente B2B

### ① Objetivo do passo

Montar um painel de KPIs (Ticket Médio, CAC, Taxa de Recompra) conectando os blocos criados nos capítulos anteriores.

### ② Pré-requisito

Passo 3 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**Passo 1: QUERY de Consolidação de Dados**

```excel
=QUERY(Pedidos!A:G;
  "SELECT B, SUM(G), COUNT(A), MIN(A), MAX(A) 
   WHERE A >= date '"&TEXT(TODAY()-365;"yyyy-mm-dd")&"' 
   GROUP BY B 
   ORDER BY SUM(G) DESC 
   LABEL B 'Cliente', 
         SUM(G) 'Faturação Total (€)', 
         COUNT(A) 'Nº Pedidos', 
         MIN(A) 'Primeiro Pedido', 
         MAX(A) 'Último Pedido'"; 1)
```

**Passo 2: Fórmulas dos 5 KPIs no Google Sheets**

```excel
// Ticket Médio (coluna F)
=IFERROR(E2/D2; "N/A")

// CAC — precisa de uma aba "Marketing" com coluna B = investimento e C = novos clientes
// Na aba "Resumo", coluna G:
=IFERROR(
  SUM(Marketing!B:B) / SUM(Marketing!C:C);
  "N/A"
)

// LTV — precisa de dados históricos
// Ticket Médio × Frequência (pedidos/mês) × Vida Média (meses)
=IFERROR(
  (E2/D2) * (D2/12) * 36;
  "N/A"
)
// Nota: 36 meses = 3 anos de vida média (ajuste conforme seu setor)

// Taxa de Recompra (coluna H)
// Precisa de uma aba "Clientes" com coluna A = cliente, B = total de pedidos
=IFERROR(
  COUNTIF(Clientes!B:B; ">="&2) / COUNTA(Clientes!A:A) * 100;
  "N/A"
)

// NPS — precisa de uma aba "Pesquisa NPS" com coluna A = cliente, B = nota (0-10)
=IFERROR(
  (COUNTIF(Pesquisa_NPS!B:B; ">=9") / COUNTA(Pesquisa_NPS!A:A) * 100) -
  (COUNTIF(Pesquisa_NPS!B:B; "<=6") / COUNTA(Pesquisa_NPS!A:A) * 100);
  "N/A"
)
```

**Passo 4: Validação com MisVisFix (Prompt para IA)**

```markdown
# Prompt: Validação de Dashboard contra Visualizações Enganosas

Você é um auditor de visualização de dados. Analise o dashboard abaixo
e verifique os seguintes pontos:

## Checklist de Validação (MisVisFix)
1. EIXO TRUNCADO: O eixo Y começa em zero? Se não, o gráfico distorce magnitudes.
2. ESCALA INCONSISTENTE: Grandezas diferentes estão sendo comparadas no mesmo eixo?
3. CORES ENGANOSAS: Cores estão sendo usadas para manipular percepção (ex.: vermelho para queda pequena)?
4. DESTAQUE SELETIVO: Apenas dados que confirmam a narrativa estão sendo mostrados?
5. PROPORÇÃO CORRETA: Barras e áreas representam proporcionalmente os valores?

## Dashboard Analisado
[Descreva seu dashboard aqui: tipo de gráfico, valores, eixos, cores]

## Saída Esperada
Para cada ponto do checklist:
- Status: OK / ALERTA / ERRO
- Justificativa: por que passou ou falhou
- Sugestão de correção (se aplicável)
```

**Script Completo: Dashboard HTML com KPI Cards**

```python
import json
from datetime import datetime

# === KPIs CALCULADOS (simulando output das QUERYs) ===
kpis = {
    "ticket_medio": {"valor": 3450, "moeda": "EUR", "trend": "+8%", "status": "verde"},
    "cac": {"valor": 1800, "moeda": "EUR", "trend": "-12%", "status": "verde"},
    "ltv": {"valor": 41400, "moeda": "EUR", "trend": "+15%", "status": "verde"},
    "taxa_recompra": {"valor": 72, "unidade": "%", "trend": "+3%", "status": "verde"},
    "nps": {"valor": 58, "unidade": "pts", "trend": "+5", "status": "verde"},
}

def gerar_dashboard_html(kpis):
    """Gera dashboard HTML com KPI Cards em formato lista."""
    
    cores_status = {
        "verde": "#2ecc71",
        "amarelo": "#f39c12",
        "vermelho": "#e74c3c"
    }
    
    html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Painel de Saúde do Cliente B2B</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', sans-serif; 
            background: #1a1a2e; 
            color: #fff; 
            padding: 20px;
        }
        .dashboard { max-width: 600px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { font-size: 1.5em; color: #eee; }
        .header p { color: #888; font-size: 0.9em; }
        .kpi-card {
            background: #16213e;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            border-left: 5px solid;
    
```

### ⑤ Verificação / Gate

_(a completar)_

### ⑥ Feito quando…

- [ ] Calcular os 5 KPIs sem contextualizar.** Um Ticket Médio de €3.000 é bom ou ruim? Depende do setor. No odontológico B2B, é saudável. Em outro setor, pode ser baixo. Sempre compare com benchmarks do seu mercado
- [ ] Ignorar a validação MisVisFix.** Um dashboard com eixo truncado pode fazer uma queda de 3% parecer uma catastrofe. Sempre verifique se as escalas são honestas
- [ ] Entregar o dashboard sem teste de 5 segundos.** Mostre para alguém que não participou da criação e cronometre. Se em 5 segundos a pessoa não entender o status do negócio, volte e simplifique
- [ ] Esquecer de atualizar.** Um dashboard que não se atualiza automaticamente vira um relatório estático. Use as QUERYs reativas do Google Sheets para manter tudo em tempo real

### ⑦ Armadilhas

- _(a completar)_

# Checklist Mestre

**Passo 1 — O Design da Clareza Analítica**

- [ ] Pedir à IA para gerar o dashboard completo de uma vez.** A IA gera código que você não controla. Use a IR: peça a estrutura, valide, depois renderize
- [ ] Ignorar a validação humana.** A IA erra — às vezes coloca o dado certo no lugar errado. Sempre revise antes de enviar ao painel
- [ ] Copiar layout de dashboards genéricos.** Cada empresa tem seus KPIs. O que funciona para um SaaS não funciona para uma distribuidora odontológica B2B

**Passo 2 — Substituindo a Complexidade pela Praticidade**

- [ ] Adicionar mais métricas para "completar" o painel.** Se você tem 15 cartões, não é um dashboard — é uma lista de compras. Mantenha no máximo 5-7 indicadores visíveis
- [ ] Usar cores decorativas em vez de semânticas.** Azul escuro, azul claro e azul médio não comunicam nada. Verde, amarelo e vermelho comunicam status instantaneamente
- [ ] Confundir "simples" com "simplório".** Um cartão com primeiro pedido, último pedido e volume total não é simplório — é cirúrgico. A sofisticação está nos dados que ele comunica, não na quantidade de pixels

**Passo 3 — Fórmulas Complexas em Segundos**

- [ ] Colar a fórmula sem testar.** A IA pode gerar uma QUERY que funciona perfeitamente para os dados de exemplo, mas falha para dados reais com formatação diferente (datas em formato americano, vírgula como separador decimal). Sempre teste com uma amostra
- [ ] Delegar regras de negócio sem explicar.** Se sua empresa tem regras como "considere apenas pedidos acima de €500" ou "desconte devoluções", essas regras precisam estar no prompt. A IA não adivinha
- [ ] Esquecer de validar dados duplicados.** Quando você consolida dados de múltiplas fontes, duplicatas acontecem. Sempre inclua uma verificação de integridade após a consolidação

**Passo 4 — Seu Primeiro Painel de Saúde do Cliente B2B**

- [ ] Calcular os 5 KPIs sem contextualizar.** Um Ticket Médio de €3.000 é bom ou ruim? Depende do setor. No odontológico B2B, é saudável. Em outro setor, pode ser baixo. Sempre compare com benchmarks do seu mercado
- [ ] Ignorar a validação MisVisFix.** Um dashboard com eixo truncado pode fazer uma queda de 3% parecer uma catastrofe. Sempre verifique se as escalas são honestas
- [ ] Entregar o dashboard sem teste de 5 segundos.** Mostre para alguém que não participou da criação e cronometre. Se em 5 segundos a pessoa não entender o status do negócio, volte e simplifique
- [ ] Esquecer de atualizar.** Um dashboard que não se atualiza automaticamente vira um relatório estático. Use as QUERYs reativas do Google Sheets para manter tudo em tempo real
