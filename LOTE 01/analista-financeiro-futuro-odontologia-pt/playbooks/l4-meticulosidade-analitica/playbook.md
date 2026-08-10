---
title: "Playbook — Meticulosidade Analítica - O que só as IAs enxergam"
subtitle: "Guia de bancada · 4 passos práticos"
author: "Heverton Eduardo Peres"
lang: pt-BR
---

# Objetivo do Material

Apresentar o poder da IA para cruzar milhares de linhas de faturamento e encontrar erros que o olho humano jamais veria — a promessa da meticulosidade analítica.

# Como usar este playbook

Você é o **Detetive de Dados Financeiros**. Cada passo é um card independente com sete partes: objetivo, pré-requisito, entregas, execução, gate de verificação, critério de conclusão e armadilhas.

Este documento **não repete a teoria** do livro. Quando precisar do porquê, siga a referência cruzada do card para o capítulo correspondente.

# Mapa dos Estágios

| # | Estágio | Passos |
|---|---|---|
| 1 | Pista | 1, 2 |
| 2 | Vestígio | 3, 4 |

# Passos Práticos

## Passo 1 — Caçando Descontos Ocultos

> **Estágio:** Pista  ·  **Origem:** Cap. 1 — Caçando Descontos Ocultos

### ① Objetivo do passo

Ensinar o leitor a cruzar duas grandes bases de dados para auditar descontos não autorizados pela equipe comercial.

### ② Pré-requisito

Nenhum — este é o ponto de partida

### ③ Entregas

- _(a completar)_

### ④ Execução

_(a completar)_

### ⑤ Verificação / Gate

_(a completar)_

### ⑥ Feito quando…

- [ ] Limiar muito baixo**: Se você sinalizar desvio acima de 0.5%, terá milhares de falsos positivos. Comece com 2-3% e ajuste conforme a sensibilidade desejada
- [ ] Ignorar variações sazonais**: Descontos maiores ao final de trimestres podem ser legítimos (meta de vendas). Inclua contexto temporal na análise
- [ ] Não cruzar por período**: Uma fatura de janeiro comparada com um contrato de março gera falso positivo. Sempre cruze por mês de referência
- [ ] Esquecer de projectar**: O impacto de 3 meses não é o impacto anual. Projete sempre para 12 meses para dar dimensão ao problema [4]

### ⑦ Armadilhas

- Limiar muito baixo**: Se você sinalizar desvio acima de 0.5%, terá milhares de falsos positivos. Comece com 2-3% e ajuste conforme a sensibilidade desejada
- Ignorar variações sazonais**: Descontos maiores ao final de trimestres podem ser legítimos (meta de vendas). Inclua contexto temporal na análise
- Não cruzar por período**: Uma fatura de janeiro comparada com um contrato de março gera falso positivo. Sempre cruze por mês de referência
- Esquecer de projectar**: O impacto de 3 meses não é o impacto anual. Projete sempre para 12 meses para dar dimensão ao problema [4]

## Passo 2 — Limpeza e Higienização de Dados (Regex)

> **Estágio:** Pista  ·  **Origem:** Cap. 2 — Limpeza e Higienização de Dados (Regex)

### ① Objetivo do passo

Usar IA para criar expressões regulares que padronizam instantaneamente milhares de cadastros e telefones de clínicas portuguesas.

### ② Pré-requisito

Passo 1 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**Fundamentos de Regex em Python**

```python
import re
import pandas as pd
import numpy as np
from typing import Optional, Tuple

# ========================================
# MÓDULO 1: REGEX BÁSICA PARA DADOS ODONTOLÓGICOS
# ========================================

class PadronizadorDados:
    """
    Classe para padronização de dados de cadastros odontológicos.
    Utiliza regex para validação e transformação de telefones, NIFs e moradas.
    """
    
    def __init__(self):
        # Regex para telefones portugueses
        # Formato aceito: +351 912 345 678, (912) 345-678, 912345678, etc.
        self.REGEX_TELEFONE = re.compile(
            r'^(\+351)?\s*[\(]?[29][\)]?\s*\d{3}[\s.\-]?\d{3}[\s.\-]?\d{3}$'
        )
        
        # Regex para NIF (9 dígitos)
        self.REGEX_NIF = re.compile(r'^\d{9}$')
        
        # Regex para moradas portuguesas
        # Captura: Rua/Avenida/Travessa + nome + número + opcional andar/sala
        self.REGEX_MORADA = re.compile(
            r'^(Rua|Av\.|Avenida|Travessa|Largo|Praça|Estrada|Beco)\s+'
            r'[A-Za-zÀ-ÿ\s]+,?\s*\d+[A-Za-zºª]?\s*'
            r'(\d+[ºª]?\s*[A-Za-z]?\s*)?$',
            re.IGNORECASE
        )
    
    def extrair_telefone(self, texto: str) -> Optional[str]:
        """
        Extrai e normaliza um telefone português de um texto.
        
        Retorna o telefone no formato padronizado: +351 XXX XXX XXX
        ou None se não for encontrado um telefone válido.
        """
        if not isinstance(texto, str):
            return None
        
        # Remover caracteres não numéricos para validação
        numeros = re.sub(r'[^\d]'
```

**Pipeline de Limpeza em Lote**

```python
# ========================================
# MÓDULO 2: PIPELINE DE LIMPEZA EM LOTE
# ========================================

def gerar_dados_sujos(n_registros=5000):
    """
    Gera dados sintéticos de cadastros odontológicos com sujeira intencional.
    Simula os problemas reais encontrados em bases de dados portuguesas.
    """
    np.random.seed(42)
    
    # Templates de telefones (variantes sujas)
    templatesTelefone = [
        lambda d: f"{d}",                           # 912345678
        lambda d: f"+351 {d[:3]} {d[3:6]} {d[6:]}", # +351 912 345 678
        lambda d: f"({d[:3]}) {d[3:6]}-{d[6:]}",    # (912) 345-678
        lambda d: f"{d[:3]}.{d[3:6]}.{d[6:]}",      # 912.345.678
        lambda d: f"+351{d}",                        # +351912345678
        lambda d: f"00351 {d[:3]} {d[3:6]} {d[6:]}",# 00351 912 345 678
        lambda d: f"00{d}",                          # 00912345678
    ]
    
    # Templates de NIFs (variantes sujas)
    templates_nif = [
        lambda n: f"{n}",           # 123456789
        lambda n: f"{n[:3]}.{n[3:6]}.{n[6:]}",  # 123.456.789
        lambda n: f"PT-{n}",        # PT-123456789
        lambda n: f"NIF {n}",       # NIF 123456789
    ]
    
    # Templates de moradas (variantes sujas)
    moradas_sujas = [
        "Rua das Flores 123 3ºDto",
        "AV. DA REPUBLICA 456",
        "travessa do sol,789",
        "Rua 123",
        "Av da Liberdade, 1000 2ºEsq",
        "TRAVESSA  SANTO  ANTÓNIO  45",
        "Rua da Paz, 78 s/b",
    ]
    
    clinicas = [
        "Clínica Alpha Dental", "Clínica Beta Smile", "Clínica Gam
```

**Aplicação da Limpeza e Métricas de Impacto**

```python
# ========================================
# MÓDULO 3: APLICAÇÃO DA LIMPEZA E MÉTRICAS
# ========================================

def limpar_base_completa(df_sujos, padronizador):
    """
    Aplica a limpeza em toda a base de dados e retorna métricas de impacto.
    """
    df_limpo = df_sujos.copy()
    
    # Inicializar colunas de resultado
    df_limpo['telefone_limpo'] = None
    df_limpo['telefone_valido'] = False
    df_limpo['nif_limpo'] = None
    df_limpo['nif_valido'] = False
    df_limpo['morada_limpa'] = None
    df_limpo['morada_valida'] = False
    
    # Aplicar limpeza
    for idx, row in df_limpo.iterrows():
        # Telefone
        tel_limpo = padronizador.extrair_telefone(row['telefone'])
        if tel_limpo:
            df_limpo.at[idx, 'telefone_limpo'] = tel_limpo
            df_limpo.at[idx, 'telefone_valido'] = True
        
        # NIF
        nif_limpo = padronizador.padronizar_nif(row['nif'])
        if nif_limpo:
            df_limpo.at[idx, 'nif_limpo'] = nif_limpo
            df_limpo.at[idx, 'nif_valido'] = True
        
        # Morada
        morada_limpa = padronizador.limpar_morada(row['morada'])
        if morada_limpa:
            df_limpo.at[idx, 'morada_limpa'] = morada_limpa
            df_limpo.at[idx, 'morada_valida'] = True
    
    return df_limpo

# Executar limpeza
pad = PadronizadorDados()
df_limpo = limpar_base_completa(df_sujos, pad)

# Calcular métricas de impacto
total = len(df_limpo)
tel_validos = df_limpo['telefone_valido'].sum()
nif_validos = df_limpo['nif_valido'].sum()
moradas_validas = df_limpo['morada_valida
```

**Prompt para IA: Geração de Regex Sob Medida**

```python
# ========================================
# MÓDULO 4: PROMPT ESTRUTURADO PARA GERAÇÃO DE REGEX
# ========================================

PROMPT_REGEX_TEMPLATE = """
# CONTEXTO
Sou analista financeiro de uma distribuidora de materiais odontológicos em Portugal.
Preciso de expressões regulares para limpar e validar dados de cadastro de clínicas.

# DADOS DE EXEMPLO (dos meus dados reais)
## Telefones encontrados na base:
{exemplos_telefone}

## NIFs encontrados na base:
{exemplos_nif}

## Moradas encontradas na base:
{exemplos_morada}

# REQUISITOS
1. A regex deve aceitar TODOS os formatos válidos acima
2. A regex deve REJEITAR formatos inválidos
3. Para telefones: aceitar formatos com/sem +351, com/sem espaços, com/sem parênteses
4. Para NIFs: exatamente 9 dígitos numéricos
5. Para moradas: aceitar abreviações (Rua, Av., Tv., Lg., Pç., Est., Bc.)

# SAÍDA DESEJADA
Forneça:
1. A regex para cada campo
2. 5 exemplos que DEVEM ser aceitos (true positives)
3. 5 exemplos que DEVEM ser rejeitados (true negatives)
4. Uma função Python que aplica a regex

# FORMATO
Responda em Python com a classe completa.
"""

# Exemplo de uso do prompt
exemplos_telefone = """
912345678
+351 912 345 678
(912) 345-678
912.345.678
+351912345678
00351 912 345 678
213456789
"""

exemplos_nif = """
123456789
987654321
PT-123456789
NIF 123456789
123.456.789
"""

exemplos_morada = """
Rua das Flores, 123 3ºDto
AV. DA REPUBLICA, 456
travessa do sol,789
Rua 123
Av da Liberdade, 1000 2ºEsq
"""

prompt_final = PROMPT_REGEX_TEMPLATE.format(
    exemplos_telefone=exemplos_telefone,
    exemplos_nif=exemplos_n
```

### ⑤ Verificação / Gate

_(a completar)_

### ⑥ Feito quando…

- [ ] Regex que rejeita dados válidos**: Uma regex para telefones que exige +351 vai rejeitar todos os números locais sem código do país. Sempre teste com exemplos do mundo real antes de aplicar em produção
- [ ] Não validar após limpar**: Limpar não é o mesmo que validar. Um telefone pode ser "normalizado" para um formato que a regex não aceita. Valide sempre depois de limpar
- [ ] Esquecer que regex é específica por país**: Uma regex para telefones portugueses não funciona para telefones brasileiros. Adapte sempre ao contexto [4]
- [ ] Não projectar o custo da sujeira**: €8.200 anuais em frete incorreto parece pouco, mas em 5 anos são €41.000. A regex é um investimento, não um custo

### ⑦ Armadilhas

- Regex que rejeita dados válidos**: Uma regex para telefones que exige +351 vai rejeitar todos os números locais sem código do país. Sempre teste com exemplos do mundo real antes de aplicar em produção
- Não validar após limpar**: Limpar não é o mesmo que validar. Um telefone pode ser "normalizado" para um formato que a regex não aceita. Valide sempre depois de limpar
- Esquecer que regex é específica por país**: Uma regex para telefones portugueses não funciona para telefones brasileiros. Adapte sempre ao contexto [4]
- Não projectar o custo da sujeira**: €8.200 anuais em frete incorreto parece pouco, mas em 5 anos são €41.000. A regex é um investimento, não um custo

## Passo 3 — A Análise da Cesta de Compras

> **Estágio:** Vestígio  ·  **Origem:** Cap. 3 — A Análise da Cesta de Compras

### ① Objetivo do passo

Instruir a IA a analisar históricos de compras para descobrir correlações invisíveis entre produtos odontológicos.

### ② Pré-requisito

Passo 2 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

_(a completar)_

### ⑤ Verificação / Gate

_(a completar)_

### ⑥ Feito quando…

- [ ] Confundir correlação com causalidade**: Lift > 1 não significa que um produto CAUSA a compra do outro — significa que eles são comprados juntos mais que o esperado. A ação comercial é a mesma, mas a interpretação é diferente
- [ ] Ignorar o suporte**: Uma regra com lift = 5.0 mas suporte = 0.1% atinge pouquíssimos clientes. Priorize regras com lift > 1.5 E suporte > 3%
- [ ] Não atualizar periodicamente**: Padrões de compra mudam. Rodar a análise trimestralmente garante que as recomendações estejam atuais [4]
- [ ] Esquecer o contexto sazonal**: Implantes podem ter sazonalidade (mais vendas em janeiro e setembro). Análises temporais complementares evitam conclusões enviesadas

### ⑦ Armadilhas

- Confundir correlação com causalidade**: Lift > 1 não significa que um produto CAUSA a compra do outro — significa que eles são comprados juntos mais que o esperado. A ação comercial é a mesma, mas a interpretação é diferente
- Ignorar o suporte**: Uma regra com lift = 5.0 mas suporte = 0.1% atinge pouquíssimos clientes. Priorize regras com lift > 1.5 E suporte > 3%
- Não atualizar periodicamente**: Padrões de compra mudam. Rodar a análise trimestralmente garante que as recomendações estejam atuais [4]
- Esquecer o contexto sazonal**: Implantes podem ter sazonalidade (mais vendas em janeiro e setembro). Análises temporais complementares evitam conclusões enviesadas

## Passo 4 — O Relatório de Recuperação de Lucro

> **Estágio:** Vestígio  ·  **Origem:** Cap. 4 — O Relatório de Recuperação de Lucro

### ① Objetivo do passo

Transformar anomalias encontradas pela IA em um relatório executivo de uma página focado na recuperação de margem de lucro.

### ② Pré-requisito

Passo 3 concluído

### ③ Entregas

- _(a completar)_

### ④ Execução

**Implementação do Isolation Forest**

```python
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

# ========================================
# MÓDULO 1: ISOLATION FOREST PARA FATURAMENTO
# ========================================

def gerar_dados_faturamento_odontologico(n_transacoes=5000):
    """
    Gera dados de faturamento odontológico com anomalias植入adas.
    
    Dimensões: preço, quantidade, desconto, margem, frequência de compra.
    Anomalias: preços abaixo do custo, descontos excessivos, quantidades atípicas.
    """
    np.random.seed(42)
    
    # Base de dados normais
    dados = []
    
    for i in range(n_transacoes):
        # Determinar se é anomalia (10% da base)
        is_anomalia = np.random.random() < 0.10
        
        if is_anomalia:
            # Tipo de anomalia
            tipo_anomalia = np.random.choice([
                'preco_baixo', 'desconto_excessivo', 
                'quantidade_atipica', 'margem_negativa'
            ])
            
            if tipo_anomalia == 'preco_baixo':
                preco = np.random.uniform(5, 30)  # Muito abaixo do normal
                quantidade = np.random.randint(1, 10)
                desconto = np.random.uniform(5, 15)
            elif tipo_anomalia == 'desconto_excessivo':
                preco = np.random.uniform(100, 400)
                quantidade = np.random.randint(1, 20)
                desconto = np.random.uniform(20, 35)
```

**Implementação do Autoencoder**

```python
# ========================================
# MÓDULO 2: AUTOENCODER PARA ANOMALIAS
# ========================================

# Nota: Implementação com numpy puro para evitar dependência de TensorFlow
# Em produção, use keras/tensorflow

class AutoencoderSimples:
    """
    Autoencoder simplificado implementado com numpy.
    Treina para reconstruir dados normais; anomalias têm erro alto.
    """
    
    def __init__(self, input_dim, encoding_dim=3, learning_rate=0.01):
        self.input_dim = input_dim
        self.encoding_dim = encoding_dim
        self.lr = learning_rate
        
        # Inicializar pesos aleatoriamente
        np.random.seed(42)
        self.W_encode = np.random.randn(input_dim, encoding_dim) * 0.1
        self.b_encode = np.zeros(encoding_dim)
        self.W_decode = np.random.randn(encoding_dim, input_dim) * 0.1
        self.b_decode = np.zeros(input_dim)
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def forward(self, X):
        """Forward pass: encode → decode."""
        # Encode
        self.encoded = self.sigmoid(X @ self.W_encode + self.b_encode)
        # Decode
        self.decoded = self.sigmoid(self.encoded @ self.W_decode + self.b_decode)
        return self.decoded
    
    def backward(self, X):
        """Backward pass: atualizar pesos via gradiente descendente."""
        m = X.shape[0]
        
        # Erro de reconstrução
        error = self.decoded - X
        
        # Gradientes do decoder
        dW_decode = self.encoded.T @ error / m
        db_decode = np.mean(error, ax
```

**Consolidação dos Dois Métodos**

```python
# ========================================
# MÓDULO 3: CONSOLIDAÇÃO E RANKING
# ========================================

def consolidar_anomalias(df, threshold_iso=0.5, threshold_ae_percentil=90):
    """
    Consolida anomalias do Isolation Forest e Autoencoder.
    
    Estratégia: se pelo menos um método detecta, marca como suspeita.
    Prioriza por score combinado.
    """
    
    df_consol = df.copy()
    
    # Score combinado (normalizado 0-1)
    score_iso_norm = (
        df_consol['score_anomalia'] - df_consol['score_anomalia'].min()
    ) / (df_consol['score_anomalia'].max() - df_consol['score_anomalia'].min())
    
    score_ae_norm = (
        df_consol['score_reconstrucao'] - df_consol['score_reconstrucao'].min()
    ) / (df_consol['score_reconstrucao'].max() - df_consol['score_reconstrucao'].min())
    
    df_consol['score_combinado'] = (score_iso_norm * 0.5 + score_ae_norm * 0.5)
    
    # Detecção consolidada
    df_consol['anomalia_consolidada'] = (
        (df_consol['anomalia_iso'] == 1) | (df_consol['anomalia_ae'] == 1)
    ).astype(int)
    
    # Classificação por severidade
    df_consol['severidade'] = pd.cut(
        df_consol['score_combinado'],
        bins=[0, 0.3, 0.6, 0.8, 1.0],
        labels=['Baixa', 'Média', 'Alta', 'Crítica']
    )
    
    # Ranking por impacto financeiro
    df_consol['impacto_financeiro'] = np.where(
        df_consol['anomalia_consolidada'] == 1,
        df_consol['valor_total'] * df_consol['desconto_pct'] / 100,
        0
    )
    
    return df_consol

# Consolidar
df_consolidado = consolidar_anomalias(df_fatu
```

### ⑤ Verificação / Gate

_(a completar)_

### ⑥ Feito quando…

- [ ] Começar pelo método em vez do problema**: Executivos querem saber O QUE está errado, não COMO você descobriu. Comece pelo problema, depois pela evidência
- [ ] Não projetar para 12 meses**: O impacto de 3 meses parece pequeno. Projetar para um ano dá a dimensão real do problema
- [ ] Esquecer o ROI**: Se a correção custa €5.000 e recupera €108.000, o ROI é de 2.060%. Sempre inclua essa métrica
- [ ] Não incluir responsáveis e prazos**: "Implementar automação" não é uma ação — é uma ideia. "O TI implementa na semana 1-2" é uma ação [3]

### ⑦ Armadilhas

- Começar pelo método em vez do problema**: Executivos querem saber O QUE está errado, não COMO você descobriu. Comece pelo problema, depois pela evidência
- Não projetar para 12 meses**: O impacto de 3 meses parece pequeno. Projetar para um ano dá a dimensão real do problema
- Esquecer o ROI**: Se a correção custa €5.000 e recupera €108.000, o ROI é de 2.060%. Sempre inclua essa métrica
- Não incluir responsáveis e prazos**: "Implementar automação" não é uma ação — é uma ideia. "O TI implementa na semana 1-2" é uma ação [3]

# Checklist Mestre

**Passo 1 — Caçando Descontos Ocultos**

- [ ] Limiar muito baixo**: Se você sinalizar desvio acima de 0.5%, terá milhares de falsos positivos. Comece com 2-3% e ajuste conforme a sensibilidade desejada
- [ ] Ignorar variações sazonais**: Descontos maiores ao final de trimestres podem ser legítimos (meta de vendas). Inclua contexto temporal na análise
- [ ] Não cruzar por período**: Uma fatura de janeiro comparada com um contrato de março gera falso positivo. Sempre cruze por mês de referência
- [ ] Esquecer de projectar**: O impacto de 3 meses não é o impacto anual. Projete sempre para 12 meses para dar dimensão ao problema [4]

**Passo 2 — Limpeza e Higienização de Dados (Regex)**

- [ ] Regex que rejeita dados válidos**: Uma regex para telefones que exige +351 vai rejeitar todos os números locais sem código do país. Sempre teste com exemplos do mundo real antes de aplicar em produção
- [ ] Não validar após limpar**: Limpar não é o mesmo que validar. Um telefone pode ser "normalizado" para um formato que a regex não aceita. Valide sempre depois de limpar
- [ ] Esquecer que regex é específica por país**: Uma regex para telefones portugueses não funciona para telefones brasileiros. Adapte sempre ao contexto [4]
- [ ] Não projectar o custo da sujeira**: €8.200 anuais em frete incorreto parece pouco, mas em 5 anos são €41.000. A regex é um investimento, não um custo

**Passo 3 — A Análise da Cesta de Compras**

- [ ] Confundir correlação com causalidade**: Lift > 1 não significa que um produto CAUSA a compra do outro — significa que eles são comprados juntos mais que o esperado. A ação comercial é a mesma, mas a interpretação é diferente
- [ ] Ignorar o suporte**: Uma regra com lift = 5.0 mas suporte = 0.1% atinge pouquíssimos clientes. Priorize regras com lift > 1.5 E suporte > 3%
- [ ] Não atualizar periodicamente**: Padrões de compra mudam. Rodar a análise trimestralmente garante que as recomendações estejam atuais [4]
- [ ] Esquecer o contexto sazonal**: Implantes podem ter sazonalidade (mais vendas em janeiro e setembro). Análises temporais complementares evitam conclusões enviesadas

**Passo 4 — O Relatório de Recuperação de Lucro**

- [ ] Começar pelo método em vez do problema**: Executivos querem saber O QUE está errado, não COMO você descobriu. Comece pelo problema, depois pela evidência
- [ ] Não projetar para 12 meses**: O impacto de 3 meses parece pequeno. Projetar para um ano dá a dimensão real do problema
- [ ] Esquecer o ROI**: Se a correção custa €5.000 e recupera €108.000, o ROI é de 2.060%. Sempre inclua essa métrica
- [ ] Não incluir responsáveis e prazos**: "Implementar automação" não é uma ação — é uma ideia. "O TI implementa na semana 1-2" é uma ação [3]
