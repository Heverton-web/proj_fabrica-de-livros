---
title: "Playbook — O Uso de IA em Análise Financeira no Setor Odontológico"
subtitle: "Guia de bancada · 4 passos práticos"
author: "Heverton Eduardo Peres"
lang: pt-BR
---

# Objetivo do Material

Apresentar a IA não como ameaça, mas como copiloto que amplifica a capacidade analítica do profissional financeiro do setor odontológico.

# Como usar este playbook

Você é o **Analista com Copiloto IA**. Cada passo é um card independente com sete partes: objetivo, pré-requisito, entregas, execução, gate de verificação, critério de conclusão e armadilhas.

Este documento **não repete a teoria** do livro. Quando precisar do porquê, siga a referência cruzada do card para o capítulo correspondente.

# Mapa dos Estágios

| # | Estágio | Passos |
|---|---|---|
| 1 | Copiloto | 1, 2 |
| 2 | Comando | 3, 4 |

# Passos Práticos

## Passo 1 — Preparando o Terreno Seguro

> **Estágio:** Copiloto  ·  **Origem:** Cap. 1 — Preparando o Terreno Seguro

### ① Objetivo do passo

Ensinar o leitor a anonimizar e limpar dados financeiros antes de subir para ferramentas de IA pública, garantindo conformidade com RGPD.

### ② Pré-requisito

Nenhum — este é o ponto de partida

### ③ Entregas

- _(a completar)_

### ④ Execução

**4.1 Arquitetura Básica de um Sistema de Análise Financeira com IA**

```text
┌─────────────────────────────────────────────────┐
│              CAMADA DE APRESENTAÇÃO              │
│    (Dashboard, Relatórios, Alertas, Chat IA)     │
├─────────────────────────────────────────────────┤
│              CAMADA DE INTELIGÊNCIA              │
│   (Modelos de ML, LLM para análise, Regras)     │
├─────────────────────────────────────────────────┤
│              CAMADA DE PROCESSAMENTO             │
│    (ETL, Validação, Normalização, Cache)         │
├─────────────────────────────────────────────────┤
│              CAMADA DE DADOS                     │
│   (ERP Clínica, Bancos, Planilhas, APIs)         │
└─────────────────────────────────────────────────┘
```

**4.2 Camada de Dados: Conectando às Fontes**

```python
# camada_dados.py — Conector multi-fonte para dados financeiros da clínica
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import hashlib


class ConectorDadosFinanceiros:
    """
    Coleta dados de múltiplas fontes da clínica odontológica
    e os normaliza para processamento pelo copiloto IA.
    """
    
    def __init__(self, config_path: str):
        """
        Inicializa o conector com configuração de fontes.
        
        Args:
            config_path: Caminho para JSON de configuração das fontes
        """
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.fontes = self.config.get('fontes', [])
        self.cache = {}
        self.ultima_sincronizacao = None
    
    def coletar_dados(self, periodo_dias: int = 30) -> Dict[str, pd.DataFrame]:
        """
        Coleta dados de todas as fontes configuradas para o período especificado.
        
        Args:
            periodo_dias: Número de dias para retroceder na coleta
            
        Returns:
            Dicionário com DataFrames normalizados por categoria
        """
        data_inicio = datetime.now() - timedelta(days=periodo_dias)
        dados_brutos = {}
        
        for fonte in self.fontes:
            tipo = fonte['tipo']
            nome = fonte['nome']
            
            print(f"[COLETA] Processando fonte: {nome} (tipo: {tipo})")
            
            if tipo == 'csv':
                dados_brutos[nome] = self._ler_csv(fonte, data_inicio)
     
```

**4.3 Camada de Processamento: ETL Inteligente**

```python
# processamento_etl.py — Pipeline de processamento com validação de qualidade
import pandas as pd
import numpy as np
from typing import Dict, Tuple, List
from dataclasses import dataclass, field
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ETL_Clinica")


@dataclass
class ResultadoQualidade:
    """ Armazena resultados da validação de qualidade dos dados. """
    fonte: str
    total_registros: int
    registros_validos: int
    registros_com_erro: int
    alertas: List[str] = field(default_factory=list)
    score_qualidade: float = 0.0


class ProcessadorETL:
    """
    Pipeline de ETL com validação de qualidade e detecção de anomalias.
    Cada etapa gera logs detalhados para rastreabilidade.
    """
    
    # Regras de validação por tipo de dado
    REGRAS_VALIDACAO = {
        'valor': {
            'minimo': -1000000,  # Crédito pode ser negativo (estorno)
            'maximo': 5000000,
            'tipo': 'numerico'
        },
        'data': {
            'minimo': '2020-01-01',
            'tipo': 'data'
        },
        'categoria': {
            'permitidos': [
                'consultas', 'proteses', 'ortodontia', 'cirurgia',
                'implantes', 'estetica', 'preventiva', 'laboratorio',
                'aluguel', 'salarios', 'insumos', 'equipamentos',
                'marketing', 'administrativo', 'impostos', 'outros'
            ]
        },
        'natureza': {
            'permitidos': ['receita', 'despesa', 'investimento']
        }
    }
    
    def __init__(self):
        sel
```

**4.4 Camada de Inteligência: O Copiloto em Ação**

```python
# copiloto_ia.py — Motor de análise inteligente para clínica odontológica
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum


class NivelAlerta(Enum):
    """ Níveis de severidade dos alertas do copiloto. """
    INFO = "info"
    ALERTA = "alerta"
    CRITICO = "critico"


@dataclass
class InsightFinanceiro:
    """ Representa um insight gerado pelo copiloto IA. """
    titulo: str
    descricao: str
    nivel: NivelAlerta
    metrica: str
    valor_atual: float
    valor_esperado: Optional[float]
    recomendacao: str
    impacto_estimado: str
    confianca: float  # 0.0 a 1.0


class CopilotoFinanceiro:
    """
    Motor de análise financeira inteligente.
    Monitora indicadores e gera insights automáticos.
    """
    
    # Benchmarks do setor odontológico (fonte: ABCD 2024)
    BENCHMARKS = {
        'margem_operacional': {'minimo': 0.15, 'ideal': 0.25, 'excelente': 0.35},
        'inadimplencia': {'maximo': 0.08, 'ideal': 0.03, 'critico': 0.15},
        'custo_por_procedimento': {'maximo': 0.60, 'ideal': 0.45},
        'ticket_medio': {'minimo': 250, 'ideal': 400, 'excelente': 600},
        'taxa_ocupacao': {'minimo': 0.60, 'ideal': 0.80, 'excelente': 0.90},
        'prazo_recebimento': {'maximo': 30, 'ideal': 15},
    }
    
    def __init__(self, dados: pd.DataFrame):
        """
        Inicializa o copiloto com dados processados.
        
        Args:
            dados: DataFrame consolidado com colunas padronizadas
        """
        s
```

### ⑤ Verificação / Gate

_(a completar)_

### ⑥ Feito quando…

- [ ] O Analista com Copiloto Você está na segunda-feira de manhã
- [ ] Ele abre a planilha do contador
- [ ] "Faturamos R$ 180 mil este mês
- [ ] Quem me explicar onde foi o dinheiro?" O contador
- [ ] Não consigo saber se isso é normal ou se estou gastando demais
- [ ] Ninguém me dá um número de referência." Agora muda a cena
- [ ] Você senta na cadeira do analista financeiro — mas agora tem um copiloto digital

### ⑦ Armadilhas

- _(a completar)_

## Passo 2 — Engenharia de Prompts Financeiros (Copie e Cole)

> **Estágio:** Copiloto  ·  **Origem:** Cap. 2 — Engenharia de Prompts Financeiros (Copie e Cole)

### ① Objetivo do passo

Entregar comandos estruturados prontos que fazem a IA atuar como um Diretor Financeiro (CFO) analisando tabelas de despesas e receitas.

### ② Pré-requisito

Passo 1 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**Template 1: Análise de Despesas Odontológicas**

```markdown
**PAPEL:** Você é um CFO especialista em clínicas odontológicas com 20 anos de experiência em gestão financeira.

**CONTEXTO:** Recebi o extrato financeiro da clínica [NOME DA CLÍNICA] referente ao período [MÊS/ANO]. As principais categorias de despesas são:
- Materiais odontológicos: R$ [VALOR]
- Equipamentos: R$ [VALOR]
- Pessoal técnico: R$ [VALOR]
- Marketing: R$ [VALOR]
- Aluguel e infraestrutura: R$ [VALOR]

**TAREFA:** Analise essas despesas e identifique:
1. As três maiores categorias em termos percentuais
2. Comparação com benchmarks do setor (15-20% materiais, 25-30% pessoal)
3. Recomendações específicas para otimização de custos

**FORMATO:** Apresente em tabela comparativa com colunas: Categoria | Valor | % Total | Benchmark | Status | Recomendação

**RESTRIÇÕES:**
- Considere sazonalidade da odontologia (alta em janeiro e agosto)
- Mantenha anonimização de dados sensíveis
- Foque em ações implementáveis em 30 dias

**RACIOCÍNIO (PoT):** Primeiro, calcule os percentuais de cada categoria. Depois, compare com benchmarks. Por fim, priorize recomendações por impacto financeiro.
```

**Template 2: Previsão de Receita Mensal**

```markdown
**PAPEL:** Você é um analista financeiro sênior especializado em projeções para clínicas odontológicas.

**CONTEXTO:** Histórico de receita dos últimos 6 meses:
- Janeiro: R$ [VALOR]
- Fevereiro: R$ [VALOR]
- Março: R$ [VALOR]
- Abril: R$ [VALOR]
- Maio: R$ [VALOR]
- Junho: R$ [VALOR]

Fatores que impactam a receita:
- Campanha de implantes em andamento
- Novo ortodontista contratado em março
- Sazonalidade típica do setor

**TAREFA:** Gere uma previsão para os próximos 3 meses (julho, agosto, setembro) considerando:
1. Tendência histórica
2. Impacto das novidades
3. Sazonalidade do setor

**FORMATO:**
- Tabela com: Mês | Previsão | Cenário Otimista | Cenário Pessimista
- Gráfico de tendência (solicite representação visual)
- Resumo executivo em 3 parágrafos

**RESTRIÇÕES:**
- Use intervalos de confiança de 80%
- Considere retenção de clientes de 85%
- Não ultrapasse capacidade instalada atual

**RACIOCÍNIO (PoT):** Calcule média móvel, aplique fator sazonal, ajuste por eventos específicos, gere intervalos.
```

**Template 3: Relatório Executivo Mensal**

```markdown
**PAPEL:** Você é o Diretor Financeiro que prepara relatórios para o conselho de administração de uma rede de clínicas odontológicas.

**CONTEXTO:** Dados consolidados do mês de [MÊS]:
- Receita total: R$ [VALOR]
- Despesas operacionais: R$ [VALOR]
- Lucro líquido: R$ [VALOR]
- Número de atendimentos: [NÚMERO]
- Ticket médio: R$ [VALOR]
- Inadimplência: [PERCENTUAL]

**TAREFA:** Elabore um relatório executivo que inclua:
1. Resumo performático (KPIs principais)
2. Análise de variação vs. mês anterior e vs. meta
3. Pontos de atenção e riscos
4. Recomendações estratégicas para o próximo mês

**FORMATO:**
- Estrutura: 1. Resumo Executivo | 2. Performance Financeira | 3. Análise de Resultados | 4. Recomendações
- Use linguagem executiva, objetiva
- Inclua indicadores visuais (▲ para crescimento, ▼ para queda, → para estabilidade)

**RESTRIÇÕES:**
- Máximo 2 páginas
- Dados anonimizados conforme LGPD
- Foco em informações acionáveis
- Tom profissional para investidores

**RACIOCÍNIO (CoT):** Primeiro, organize os KPIs. Depois, calcule variações. Em seguida, identifique padrões. Por fim, formule recomendações baseadas em evidências.
```

**Template 4: Análise de Custos por Procedimento**

```markdown
**PAPEL:** Você é um consultor financeiro especializado em odontologia, com foco em precificação de procedimentos.

**CONTEXTO:** A clínica [NOME] realiza mensalmente os seguintes procedimentos:
- Limpeza: [QUANTIDADE] unidades
- Restauração: [QUANTIDADE] unidades
- Implante: [QUANTIDADE] unidades
- Clareamento: [QUANTIDADE] unidades
- Prótese: [QUANTIDADE] unidades

Custo médio por procedimento (materiais + mão de obra):
- Limpeza: R$ [VALOR]
- Restauração: R$ [VALOR]
- Implante: R$ [VALOR]
- Clareamento: R$ [VALOR]
- Prótese: R$ [VALOR]

Preço cobrado ao paciente:
- Limpeza: R$ [VALOR]
- Restauração: R$ [VALOR]
- Implante: R$ [VALOR]
- Clareamento: R$ [VALOR]
- Prótese: R$ [VALOR]

**TAREFA:** Calcule a margem de lucro por procedimento e identifique:
1. Quais procedimentos têm margem acima de 60% (alta lucratividade)
2. Quais procedimentos têm margem abaixo de 40% (revisar precificação)
3. Impacto financeiro de realocar 20% da capacidade do baixo para o alto margem

**FORMATO:** Tabela com: Procedimento | Custo | Preço | Margem% | Classificação | Recomendação

**RACIOCÍNIO (PoT):** Calcule margens, classifique por faixa, projete impacto de realocação.
```

### ⑤ Verificação / Gate

_(a completar)_

### ⑥ Feito quando…

- [ ] Imagine a situação: você é o analista financeiro da Clínica OdontoPrime
- [ ] O proprietário pede uma análise de despesas do primeiro trimestre até o fim do dia
- [ ] Você abre a planilha
- [ ] O erro que acontece primeiro:** você cola na IA um prompt genérico: "Analise minhas despesas
- [ ] Você perde 15 minutos
- [ ] O proprietário pergunta se está pronto
- [ ] Você diz "quase"

### ⑦ Armadilhas

- _(a completar)_

## Passo 3 — Identificando Sinais de Inadimplência

> **Estágio:** Comando  ·  **Origem:** Cap. 3 — Identificando Sinais de Inadimplência

### ① Objetivo do passo

Usar IA para detectar padrões de comportamento de clínicas prestes a se tornar inadimplentes, transformando alertas em ações preventivas.

### ② Pré-requisito

Passo 2 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**4.1 Estrutura de Dados para Dashboard Financeiro**

```python
# modelo_kpis.py — Definição dos KPIs do dashboard financeiro
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json


class StatusKPI(Enum):
    """ Status visual de um KPI no dashboard. """
    OTIMO = "otimo"        # Verde escuro: acima do ideal
    BOM = "bom"            # Verde: dentro do esperado
    ATENCAO = "atencao"    # Amarelo: abaixo do ideal
    CRITICO = "critico"    # Vermelho: requer ação imediata
    SEM_DADOS = "sem_dados"


@dataclass
class KPI:
    """ Define um Indicador-Chave de Desempenho. """
    nome: str
    descricao: str
    valor_atual: float
    unidade: str  # 'R$', '%', 'dias', 'unidade'
    meta: float
    minimo_aceitavel: float
    maximo_aceitavel: Optional[float] = None
    tendencia: str = "estavel"  # 'crescendo', 'caindo', 'estavel'
    variacao_percentual: float = 0.0
    status: StatusKPI = StatusKPI.SEM_DADOS
    fonte_dados: str = ""
    ultima_atualizacao: str = ""
    comparativo_setor: Optional[float] = None
    recomendacao_ia: str = ""


@dataclass
class AlertaDashboard:
    """ Define um alerta gerado pelo copiloto IA. """
    titulo: str
    mensagem: str
    nivel: str  # 'info', 'alerta', 'critico'
    kpi_origem: str
    acao_sugerida: str
    prazo_sugerido: str
    impacto_estimado: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class GeradorKPIs:
    """
    Gera KPIs financeiros a partir de dados processados.
    Cada KPI é calculado
```

**4.2 Motor de Recomendações da IA**

```python
# motor_recomendacoes.py — Gerador de recomendações estratégicas para clínica
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class PrioridadeRecomendacao(Enum):
    """ Prioridade da recomendação. """
    URGENTE = 1      # Ação necessária em 24h
    ALTA = 2         # Ação necessária em 7 dias
    MEDIA = 3        # Ação necessária em 30 dias
    BAIXA = 4        # Ação opcional, melhorias contínuas


@dataclass
class RecomendacaoIA:
    """ Uma recomendação gerada pelo motor de IA. """
    titulo: str
    descricao: str
    prioridade: PrioridadeRecomendacao
    categoria: str  # 'receita', 'custo', 'processo', 'paciente'
    acao_especifica: str
    kpi_impactado: str
    impacto_estimado: str
    prazo_implementacao: str
    nivel_dificuldade: str  # 'facil', 'medio', 'dificil'
    evidencia: str


class MotorRecomendacoes:
    """
    Gera recomendações estratégicas baseadas nos KPIs e dados da clínica.
    Cada recomendação tem ação específica, impacto estimado e prioridade.
    """
    
    def __init__(self, kpis: List, dados: pd.DataFrame):
        """
        Args:
            kpis: Lista de objetos KPI calculados
            dados: DataFrame consolidado da clínica
        """
        self.kpis = {kpi.nome: kpi for kpi in kpis}
        self.dados = dados
        self.recomendacoes: List[RecomendacaoIA] = []
    
    def gerar_recomendacoes(self) -> List[RecomendacaoIA]:
        """ Gera todas as recomendações baseadas no estado atual. """

```

### ⑤ Verificação / Gate

_(a completar)_

### ⑥ Feito quando…

- [ ] O Dashboard que Muda Decisões Sexta-feira
- [ ] É o relatório mensal: 12 páginas de tabelas Excel impressas em PDF
- [ ] Ela olha as primeiras linhas
- [ ] "Pelo menos não foi prejuízo." Fecha o PDF
- [ ] Na segunda-feira seguinte
- [ ] Tivemos lucro!" Dra
- [ ] Fernanda não entende

### ⑦ Armadilhas

- _(a completar)_

## Passo 4 — Extração de Dados de Notas e Contratos

> **Estágio:** Comando  ·  **Origem:** Cap. 4 — Extração de Dados de Notas e Contratos

### ① Objetivo do passo

Extrair valores, taxas de IVA e prazos de pagamento de documentos PDF de forma automatizada usando comandos simples de IA.

### ② Pré-requisito

Passo 3 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**Template de Prompt para Notas Fiscais**

```text
PROMPT: EXTRACAO_NOTA_FISCAL

Você é um assistente especializado em extração de dados fiscais odontológicos.
Leia o PDF anexo e extraia os campos obrigatórios abaixo.

SCHEMA DE SAÍDA (JSON):
{
  "nota_fiscal": {
    "numero": "string — Número da nota",
    "data_emissao": "YYYY-MM-DD",
    "fornecedor": {
      "nome": "string — Razão social",
      "cnpj": "XX.XXX.XXX/XXXX-XX",
      "uf": "UF — Estado"
    },
    "itens": [
      {
        "descricao": "string — Descrição do item",
        "quantidade": "number",
        "valor_unitario": "number — Em R$",
        "valor_total": "number — Em R$",
        "cups": "string — Código CUPS (se aplicável)"
      }
    ],
    "valor_total": "number — Em R$",
    "aliquota_iva": "number — Em %",
    "valor_iva": "number — Em R$",
    "data_vencimento": "YYYY-MM-DD",
    "condicao_pagamento": "string — Ex: 30/60/90 dias"
  }
}

REGRAS:
1. Se um campo não for encontrado, retorne null
2. Para múltiplos itens, crie array na chave "itens"
3. Valores monetários: apenas números (sem R$ ou pontos de milhar)
4. Datas: sempre formato YYYY-MM-DD
5. IVA: calcular se não estiver explícito (valor_total × alíquota)
```

**Template de Prompt para Contratos**

```text
PROMPT: EXTRACAO_CONTRATO

Você é um assistente especializado em contratos de fornecedores odontológicos.
Leia o PDF anexo e extraia os campos obrigatórios abaixo.

SCHEMA DE SAÍDA (JSON):
{
  "contrato": {
    "numero": "string — Número do contrato",
    "data_assinatura": "YYYY-MM-DD",
    "data_vigencia_inicio": "YYYY-MM-DD",
    "data_vigencia_fim": "YYYY-MM-DD",
    "partes": {
      "contratada": {
        "nome": "string — Razão social",
        "cnpj": "XX.XXX.XXX/XXXX-XX"
      },
      "contratante": {
        "nome": "string — Nome da clínica",
        "cnpj": "XX.XXX.XXX/XXXX-XX"
      }
    },
    "objeto": "string — Descrição do objeto contratual",
    "valor_mensal": "number — Em R$ (se aplicável)",
    "valor_total": "number — Em R$",
    "condicoes_pagamento": "string",
    "clausulas_relevantes": [
      "string — Cláusulas que impactam finanças"
    ]
  }
}

REGRAS:
1. Extraia apenas cláusulas com impacto financeiro direto
2. Para contratos de repasse, inclua percentuais e valores
3. Se houver reajuste, extraia o índice e periodicidade
```

**Template de Prompt para Validação Cruzada**

```text
PROMPT: VALIDACAO_CRUZADA

Você é um auditor financeiro especializado em odontologia.
Compare a nota fiscal extraída com os dados do contrato vigente.

DADOS DA NOTA:
{nota_fiscal_json}

DADOS DO CONTRATO:
{contrato_json}

REGRAS DE VALIDAÇÃO:
1. Valor da nota vs. valor mensal do contrato (tolerância: 15%)
2. Data de vencimento vs. prazo contratual
3. CNPJ do fornecedor vs. CNPJ contratado
4. Descrição dos itens vs. objeto contratual

RETORNO (JSON):
{
  "validacao": {
    "status": "APROVADO | REPROVADO | ALERTA",
    "itens_verificados": [
      {
        "campo": "string",
        "resultado": "OK | INCOMPATIVEL",
        "detalhes": "string"
      }
    ],
    "observacoes": "string"
  }
}
```

**Exemplo de Saída: Nota Fiscal Extraída**

```json
{
  "nota_fiscal": {
    "numero": "NF-e 000.123.456",
    "data_emissao": "2026-03-15",
    "fornecedor": {
      "nome": "DentalSupply Brasil Ltda.",
      "cnpj": "12.345.678/0001-90",
      "uf": "SP"
    },
    "itens": [
      {
        "descricao": "Resina Acrílica Autopolimerizável 500g",
        "quantidade": 10,
        "valor_unitario": 89.90,
        "valor_total": 899.00,
        "cups": "09.04.001"
      },
      {
        "descricao": "Luva Procedimento P (Caixa c/100)",
        "quantidade": 5,
        "valor_unitario": 45.50,
        "valor_total": 227.50,
        "cups": null
      }
    ],
    "valor_total": 1126.50,
    "aliquota_iva": 18,
    "valor_iva": 202.77,
    "data_vencimento": "2026-04-14",
    "condicao_pagamento": "30 dias"
  }
}
```

### ⑤ Verificação / Gate

_(a completar)_

### ⑥ Feito quando…

- [ ] Anonimização**: os dados sensíveis (nomes de pacientes, CPFs) foram removidos dos PDFs? (Capítulo 1)
- [ ] Contratos cadastrados**: os contratos vigentes estão em uma pasta acessível ao pipeline?
- [ ] Chave de API**: a chave do VLM está configurada e com créditos suficientes?
- [ ] Regras de negócio**: as tolerâncias de validação (15% para valor, 0 dias para vencimento) estão corretas para sua clínica?
- [ ] Pasta de saída**: o diretório de resultado existe e tem permissão de escrita?

### ⑦ Armadilhas

- _(a completar)_

# Checklist Mestre

**Passo 1 — Preparando o Terreno Seguro**

- [ ] O Analista com Copiloto Você está na segunda-feira de manhã
- [ ] Ele abre a planilha do contador
- [ ] "Faturamos R$ 180 mil este mês
- [ ] Quem me explicar onde foi o dinheiro?" O contador
- [ ] Não consigo saber se isso é normal ou se estou gastando demais
- [ ] Ninguém me dá um número de referência." Agora muda a cena
- [ ] Você senta na cadeira do analista financeiro — mas agora tem um copiloto digital

**Passo 2 — Engenharia de Prompts Financeiros (Copie e Cole)**

- [ ] Imagine a situação: você é o analista financeiro da Clínica OdontoPrime
- [ ] O proprietário pede uma análise de despesas do primeiro trimestre até o fim do dia
- [ ] Você abre a planilha
- [ ] O erro que acontece primeiro:** você cola na IA um prompt genérico: "Analise minhas despesas
- [ ] Você perde 15 minutos
- [ ] O proprietário pergunta se está pronto
- [ ] Você diz "quase"

**Passo 3 — Identificando Sinais de Inadimplência**

- [ ] O Dashboard que Muda Decisões Sexta-feira
- [ ] É o relatório mensal: 12 páginas de tabelas Excel impressas em PDF
- [ ] Ela olha as primeiras linhas
- [ ] "Pelo menos não foi prejuízo." Fecha o PDF
- [ ] Na segunda-feira seguinte
- [ ] Tivemos lucro!" Dra
- [ ] Fernanda não entende

**Passo 4 — Extração de Dados de Notas e Contratos**

- [ ] Anonimização**: os dados sensíveis (nomes de pacientes, CPFs) foram removidos dos PDFs? (Capítulo 1)
- [ ] Contratos cadastrados**: os contratos vigentes estão em uma pasta acessível ao pipeline?
- [ ] Chave de API**: a chave do VLM está configurada e com créditos suficientes?
- [ ] Regras de negócio**: as tolerâncias de validação (15% para valor, 0 dias para vencimento) estão corretas para sua clínica?
- [ ] Pasta de saída**: o diretório de resultado existe e tem permissão de escrita?
