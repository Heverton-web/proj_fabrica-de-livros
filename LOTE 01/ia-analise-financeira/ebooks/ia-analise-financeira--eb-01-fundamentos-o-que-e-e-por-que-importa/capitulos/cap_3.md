# Capítulo 3: Dados Financeiros: Os Sinais da Praça

## 1. Introdução

No Capítulo 2, você montou sua bancada de terminais de IA e aprendeu a escolher o modelo certo pelo dado. Mas há uma pergunta anterior: que dados são esses, afinal? Neste capítulo, você vai aprender a reconhecer e organizar a matéria-prima do trabalho financeiro — as demonstrações contábeis, as séries temporais e os dados tabulares — e vai descobrir que a qualidade do que entra na IA determina a qualidade do que sai. Ao final, você será capaz de montar um dossiê de dados limpo e pronto para análise, com anonimização e rastreabilidade.

## 2. Explica

Todo trabalho de análise financeira começa com uma pergunta: de onde vêm os números? No Brasil, as empresas geram três demonstrações fundamentais: a Demonstração do Resultado do Exercício (DRE), que mostra receitas, custos e lucros de um período; o balanço patrimonial, que registra ativos, passivos e patrimônio líquido em uma data; e a demonstração de fluxo de caixa, que explica a variação do dinheiro entre períodos. Juntas, elas contam a história completa de um negócio — e são a base dos indicadores que você vai calcular com IA.

Além das demonstrações, o analista lida com séries temporais: receitas por mês, vendas por dia, taxas por trimestre. Uma série temporal é simplesmente uma sequência de observações ordenadas no tempo, e é o formato ideal para previsão e detecção de tendência. O tratamento desses dados tabulares — planilhas e tabelas — é exatamente o terreno onde a IA gratuita mais ajuda, pois a estrutura tabular é o formato que os assistentes melhor entendem quando recebem arquivos CSV ou XLSX [1]. Os indicadores que você vai calcular — margens, liquidez, EBITDA — nascem dessas demonstrações e são formalizados pela contabilidade; o SEBRAE disponibiliza guias práticos desses indicadores para pequenos negócios [8].

A regra de ouro deste capítulo: lixo entra, lixo sai. Se a planilha que você envia à IA tem células mescladas, textos ambíguos, valores com moeda misturada ou linhas duplicadas, a resposta virá contaminada — e a culpa não será da IA. Estudos sobre modelos aplicados a finanças mostram que a qualidade da entrada é o principal fator de qualidade da saída em tarefas de extração e resumo [2]. Por isso, antes de qualquer análise, o dado precisa passar por limpeza: padronização de formatos, tratamento de valores ausentes e remoção de duplicatas. Para séries temporais, o Prophet oferece previsão gratuita e bem documentada a partir de histórico limpo [9].

Há também a camada de sensibilidade. Dados financeiros de empresas e clientes são protegidos pela LGPD [3], e o envio deles a serviços de nuvem exige anonimização ou a escolha de modelos locais. A boa notícia: anonimizar é simples — substitua nomes por códigos, apague colunas desnecessárias e arredonde valores quando o objetivo for entender padrões, não auditar transações. No mercado de capitais, a CVM regula as informações divulgadas pelas companhias [10] e a B3 educa sobre o funcionamento do mercado [11] — fontes essenciais de referência para quem analisa o setor financeiro.

## 3. Ilustra

Voltemos à mesa de operações. Na praça — o mercado — chegam sinais de todos os lados: preços, notícias, relatórios. O operador experiente não consome tudo cru; ele filtra, padroniza e organiza antes de tomar decisão. O dado financeiro bruto é o sinal da praça: chega bagunçado, em formatos diferentes, com ruído. Seu trabalho na mesa é transformar esse sinal bruto em informação organizada — e só então colocá-la no terminal de IA.

Como Analista de Inteligência Financeira, você é o filtro entre a praça e a IA. O diagrama abaixo mostra o caminho completo: da fonte bruta ao dado pronto para análise.

```mermaid
%% legenda: Pipeline de dados financeiros da fonte bruta a analise com IA
flowchart LR
  A[Fonte bruta] --> B[Extracao]
  B --> C[Limpeza]
  C --> D[Padronizacao]
  D --> E[Anonimizacao se necessario]
  E --> F[Dado pronto]
  F --> G[IA: chat, planilha ou dashboard]
```

## 4. Técnica

### Montando a estrutura de dados do fluxo de caixa

Vamos construir, do zero, o dado que você usará nas análises dos próximos capítulos: um fluxo de caixa mensal. Comece pela versão em planilha (CSV), que você pode gerar no Excel, no Google Sheets ou até no bloco de notas:

```csv
Competencia,Entradas,Saidas_Operacionais,Saidas_Financeiras
2026-01,150000,98000,12000
2026-02,163000,101000,14000
2026-03,158000,99000,13500
2026-04,171000,105000,15000
2026-05,182000,108000,15500
2026-06,176000,106000,16000
```

### Limpeza e padronização com pandas

O código abaixo é o seu funil de qualidade: ele lê o arquivo, converte tipos, verifica valores ausentes e duplicatas e prepara a base para análise — tudo de forma reproduzível:

```python
import pandas as pd

# Leitura do arquivo bruto
df = pd.read_csv("fluxo_caixa.csv")

# Padroniza nomes de colunas
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

# Converte competencia para datetime e ordena
df["competencia"] = pd.to_datetime(df["competencia"], format="%Y-%m")
df = df.sort_values("competencia")

# Verifica qualidade
print("Valores ausentes por coluna:")
print(df.isna().sum())
print("\nLinhas duplicadas:", df.duplicated().sum())

# Calcula o saldo mensal
df["saldo"] = df["entradas"] - df["saidas_operacionais"] - df["saidas_financeiras"]

# Salva a base limpa
df.to_csv("fluxo_caixa_limpo.csv", index=False)
print("\nBase limpa salva com", len(df), "registros.")
```

Este é o padrão que você vai repetir em todas as análises: ler, padronizar, validar, calcular, salvar. A documentação do pandas detalha cada uma dessas operações [4], e o curso livre de pandas da Quantecon oferece exercícios práticos em português e inglês [12]. Para a visualização dos resultados, o Matplotlib gera gráficos profissionais gratuitamente [13] e o scikit-learn oferece modelos de regressão e classificação prontos para uso [14].

### Anonimizando dados sensíveis

Quando a base contém informações pessoais — nomes de clientes, CPF, endereços — aplique a anonimização antes de qualquer envio a serviços de nuvem:

```python
import hashlib
import pandas as pd

df = pd.read_csv("clientes_bruto.csv")

# Substitui identificadores por codigos hash (irreversivel na pratica)
df["cliente_id"] = df["nome"].apply(
    lambda nome: hashlib.sha256(nome.encode()).hexdigest()[:12]
)
df = df.drop(columns=["nome", "cpf", "endereco"])

df.to_csv("clientes_anonimizado.csv", index=False)
```

Esse procedimento reduz drasticamente o risco regulatório no tratamento de dados protegidos pela LGPD [3]. Para bases ainda mais sensíveis, o caminho definitivo é o modelo local do Capítulo 2.

### Consultando fontes oficiais

Quando você precisar de dados econômicos de referência, as fontes oficiais brasileiras oferecem séries gratuitas e confiáveis: o Banco Central publica séries de taxas e estatísticas [5], o IBGE disponibiliza estatísticas econômicas [6] e o IPEA organiza dados de pesquisa aplicada [7]. Alimentar sua IA com dados oficiais é a forma mais rápida de transformar uma análise caseira em análise com lastro. Para perguntas em linguagem natural sobre DataFrames, o PandasAI integra IA aos seus dados sem sair do Python [15], e o Google Cloud documenta casos de IA aplicada a finanças e relatórios [16].

### Consolidando múltiplas fontes em uma única base

No trabalho real, os dados raramente chegam em um único arquivo — chegam em três: um CSV do sistema de vendas, uma planilha do financeiro e um relatório em PDF. A técnica de consolidação resolve isso com concatenação e padronização de chaves:

```python
import pandas as pd

# Base de vendas (CSV do sistema)
vendas = pd.read_csv("vendas.csv")
vendas = vendas.rename(columns={"data": "competencia", "total": "entradas"})

# Base do financeiro (planilha)
financeiro = pd.read_excel("financeiro.xlsx")
financeiro = financeiro.rename(columns={"data_lancamento": "competencia", "valor": "saidas"})

# Converte chaves e concatena
vendas["competencia"] = pd.to_datetime(vendas["competencia"])
financeiro["competencia"] = pd.to_datetime(financeiro["competencia"])

consolidado = pd.merge(vendas, financeiro, on="competencia", how="outer")
print(consolidado.head())
```

### Construindo o dicionário de dados

Todo fluxo profissional mantém um dicionário de dados — a documentação de cada coluna, seu tipo e sua origem. Isso é o que transforma uma base particular em um ativo da empresa:

| Coluna | Tipo | Origem | Descrição |
|---|---|---|---|
| competencia | data | CSV vendas | Mês de referência |
| entradas | número | CSV vendas | Receita do mês |
| saidas_operacionais | número | Planilha financeiro | Custos operacionais |
| saidas_financeiras | número | Planilha financeiro | Juros e despesas financeiras |
| saldo | calculado | pandas | Entradas - saídas |

### Versionando a base limpa

A última prática do capítulo: guarde cada versão da base limpa com data no nome (`fluxo_caixa_2026_08.csv`), nunca sobrescrevendo a anterior. Auditoria, rastreabilidade e reprodução de análises dependem dessa disciplina — e é ela que permite responder, meses depois, "de onde veio este número?".

### Validação de tipos e domínios

Antes de considerar a base pronta, valide tipos e domínios — a última camada do funil de qualidade. O código abaixo verifica se cada coluna tem o tipo esperado e se os valores estão dentro de faixas plausíveis:

```python
import pandas as pd

# Carrega e valida a base limpa
df = pd.read_csv("fluxo_caixa_limpo.csv")

# 1. Tipos esperados
esperados = {"competencia": "datetime64[ns]", "entradas": "float64"}
for coluna, tipo in esperados.items():
    tipo_atual = str(df[coluna].dtype)
    status = "ok" if tipo_atual == tipo else "atencao"
    print(f"{coluna}: {tipo_atual} [{status}]")

# 2. Dominios plausiveis (valores negativos chamam atencao)
for coluna in ["entradas", "saidas_operacionais", "saidas_financeiras"]:
    negativos = (df[coluna] < 0).sum()
    print(f"{coluna}: {negativos} valor(es) negativo(s)")

# 3. Faixa de datas
print("Periodo:", df["competencia"].min(), "ate", df["competencia"].max())
```

Esse controle de qualidade automatizado é a ponte entre o dado cru e o dado que pode alimentar decisões — e é exatamente o tipo de rotina que a IA gratuita ajuda a escrever e manter [17].

### De onde vêm os dados oficiais brasileiros

Para o analista do setor financeiro, conhecer as fontes oficiais é parte do ofício. O Banco Central publica séries de taxas de juros, câmbio e estatísticas bancárias [5]; o IBGE fornece inflação (IPCA), PIB e pesquisas econômicas [6]; o IPEA organiza dados de pesquisa aplicada e políticas públicas [7]; a CVM regula e divulga informações das companhias abertas [10]; a B3 educa sobre o funcionamento do mercado de capitais [11]; e o SEBRAE orienta indicadores para pequenos negócios [8]. Cada fonte tem formato e periodicidade próprios — e a limpeza que você aprendeu neste capítulo é o que adapta esses dados oficiais ao seu fluxo de análise.

### A rotina semanal de higiene de dados

A higiene de dados não é evento único — é rotina. O padrão semanal do analista: um horário fixo para baixar as fontes, rodar o funil de limpeza, atualizar a base versionada e conferir os totais. Com a IA, essa rotina vira um script reutilizável: o prompt pede a automação da limpeza e o código gerado roda toda semana, deixando o analista livre para o que importa — a interpretação [15].

### Tratando valores ausentes com critério

Valores ausentes são inevitáveis — a questão é tratá-los com critério, não no automático. As opções, da mais segura à mais arriscada: excluir a linha (quando a ausência é pontual), preencher com a mediana (quando o dado é central), preencher com a média (cuidado com outliers) ou deixar e tratar na análise (quando a ausência carrega significado). O erro típico é pedir à IA para "preencher os vazios" sem critério — ela usa um método qualquer e o resultado vira uma falsa precisão. Sempre declare o critério no prompt e documente a decisão [2].

### O protocolo de versionamento de dados

O versionamento profissional segue uma convenção clara: nome base, período e estado — por exemplo, `fluxo_caixa_2026_bruto.csv`, `fluxo_caixa_2026_limpo.csv` e `fluxo_caixa_2026_analise.csv`. Cada estágio do funil tem seu arquivo, e o estado anterior nunca é sobrescrito. Esse protocolo permite responder, a qualquer momento, de onde veio cada número de uma análise — a base da auditoria e da confiança no trabalho [18].

### Extraindo dados de PDF e documentos

Muitos dados financeiros chegam em PDF: faturas, extratos, contratos. A extração com IA é uma das maiores economias de tempo da bancada: o assistente lê o PDF, identifica os campos relevantes e devolve uma tabela estruturada pronta para a limpeza. O fluxo prático: suba o PDF, peça "extraia data, fornecedor, valor e vencimento de cada fatura em uma tabela CSV", confira uma amostra linha a linha com o documento e salve como `faturas_bruto.csv`. A conferência é obrigatória — o reconhecimento de campos ainda erra, e o erro vira dado sujo [17].

### A conferência de totais com a fonte oficial

A conferência final de qualquer base de referência é o cruzamento com a fonte oficial: se você baixou a inflação do IBGE [6], confira o total do período com o índice publicado; se usou taxas do Banco Central [5], compare com o painel oficial. Esse cruzamento é a última linha de defesa contra dado errado — e é uma prática que os reguladores e auditores esperam do analista profissional [10].

### O quadro das demonstrações financeiras

O quadro que organiza a matéria-prima da análise:

| Demonstração | O que mostra | Pergunta que responde |
|---|---|---|
| DRE | Receitas, custos e lucros do período | A empresa está lucrando? |
| Balanço patrimonial | Ativos, passivos e patrimônio em uma data | A empresa consegue pagar? |
| Fluxo de caixa | Entradas e saídas de dinheiro | De onde vem e para onde vai o caixa? |
| Séries temporais | Observações ordenadas no tempo | Qual a tendência e a sazonalidade? |

### Perguntas frequentes sobre dados

"Posso usar dados de qualquer fonte?" — não; priorize as oficiais e confiáveis, e documente a origem [5][6]. "Meus dados precisam ser 100% limpos?" — o suficiente para a análise; a perfeição é cara e desnecessária [1]. "Anonimizar sempre?" — sempre que houver dado pessoal; o custo é baixo e o risco eliminado [3]. "Qual formato usar para a IA?" — CSV é o mais simples e universal; XLSX funciona com múltiplas abas [17].

### O exercício completo do capítulo

O exercício que fecha o capítulo é a construção do funil de dados completo de uma base real: escolha uma planilha do seu trabalho, aplique as cinco etapas do funil (ler, padronizar, validar, calcular, salvar), anonimize as colunas sensíveis com o código da seção Técnica e escreva o dicionário de dados da base. A régua de sucesso tem quatro marcas: a base limpa abre sem erro em qualquer ferramenta; os tipos e domínios foram validados; a base versionada existe com nome claro; e um colega consegue reproduzir a limpeza seguindo o dicionário [19].

### Caso real: o número que quase foi para a diretoria

Uma história que mostra o valor do funil: uma analista precisava do total de despesas do trimestre para o comitê de resultados. Colou a planilha diretamente no assistente e recebeu um total confiante. Por sorte, o checklist de conferência do Capítulo 1 fez ela cruzar com a soma manual — e a diferença era grande: células mescladas e valores com formato misto ("R$ 12,5 mil" junto de "12500") tinham confundido a interpretação [2]. Com o funil deste capítulo, o problema sumiu: base em CSV, uma linha por registro, valores numéricos puros, totais cruzados. O número que chegou à diretoria era o número certo — e a analista ganhou a reputação de quem "sempre confere". É essa a reputação que o funil constrói [15].

### O que levar deste capítulo para a sua rotina

As cinco frases do capítulo para o manual: demonstração financeira é a fonte; série temporal é o padrão de análise [8]. Lixo entra, lixo sai — a qualidade da entrada determina a da saída [2]. O funil de dados tem cinco etapas: ler, padronizar, validar, calcular, salvar [1]. Dado pessoal anonimiza antes de subir à nuvem [3]. E a base versionada é o ativo: todo número de uma análise responde "de onde veio?" [18]. Com essas cinco, sua matéria-prima está pronta para a bancada.

### Mapa de leitura do capítulo

Para aprofundar dados e fontes: a documentação do pandas ensina as operações do funil de limpeza [1]; o FinAR-Bench mostra por que a qualidade da entrada determina a qualidade da extração [2]; o portal do Banco Central oferece as séries oficiais de referência [5]; o IBGE detalha a metodologia das estatísticas econômicas [6]; o IPEA organiza dados de pesquisa aplicada [7]; e o SEBRAE apresenta os indicadores para pequenos negócios [8]. A cada leitura, você amplia o repertório de fontes confiáveis da sua bancada — e cada fonte nova é uma possibilidade nova de análise.

### A régua de progresso do dado

A régua dos dados em três estágios: estágio 1 — coletor: você junta arquivos e planilhas sem critério. Estágio 2 — higienista: você aplica o funil de limpeza e versiona as bases. Estágio 3 — curador: você define padrões de qualidade para a equipe e mantém o dicionário de dados vivo. O salto do estágio 1 para o 2 acontece em uma semana de prática; do 2 para o 3, quando a sua base passa a ser usada por outros sem erro. É nesse estágio que o dado deixa de ser arquivo e vira ativo da empresa [18].

### Checklist de conclusão do capítulo

O checklist final do Capítulo 3: reconheço as demonstrações financeiras e séries temporais como matéria-prima [8]; apliquei o funil de cinco etapas numa base real [1]; validei tipos e domínios com o código da seção Técnica [19]; anonimizei colunas sensíveis antes de qualquer uso [3]; escrevi o dicionário de dados da base [19]; versionei a base com nomes claros [18]; e cruzei um total com a fonte oficial [5][6]. Com todas as marcas, a matéria-prima da sua mesa está pronta — e nenhum número errado vai entrar na análise.

### Resumo do capítulo em um parágrafo

O resumo do Capítulo 3 em trinta segundos: o dado financeiro é o sinal da praça — chega bagunçado, e o seu trabalho é filtrar. O funil de cinco etapas (ler, padronizar, validar, calcular, salvar) transforma o sinal bruto em informação confiável, e a anonimização protege o que é sensível antes de qualquer uso em nuvem. Base limpa, versionada e documentada é o ativo que sustenta toda a análise da obra — lixo entra, lixo sai [2]. Esse é o parágrafo que resume os dados.

## 5. Aplica

Cena de contraste. Você precisa de uma previsão de vendas para o orçamento do trimestre e decide usar o ChatGPT. Com pressa, você copia a planilha de vendas — que tem cabeçalhos mesclados, valores como "R$ 12,5 mil" misturados com "12500" e três linhas duplicadas — e cola tudo em um parágrafo. A IA devolve uma previsão confiante. Você apresenta ao diretor, e na reunião seguinte descobre que a previsão não bate com o histórico real em 30%.

O diagnóstico: você alimentou o terminal com sinal sujo. Células mescladas viram texto quebrado, valores em formatos diferentes confundem a interpretação numérica e duplicatas inflam a base. A IA não tem como saber que "R$ 12,5 mil" e "12500" são a mesma coisa — ela interpreta literalmente o que recebe [2]. Guias práticos sobre automação de dados em finanças, como os da Parseur sobre IA em finanças, confirmam que a extração estruturada é o passo decisivo para análises confiáveis [17].

A correção: aplicar o funil da seção Técnica. Salve os dados em CSV com uma linha por registro, uma coluna por atributo, valores numéricos puros e sem cabeçalho mesclado. Rode a limpeza com pandas, confira os totais e só então envie o arquivo limpo ao assistente. A previsão continuará exigindo conferência — mas sairá de um dado confiável, não de uma sopa de texto.

Armadilhas comuns:

- Colar dados de planilhas formatadas como texto em vez de subir o arquivo.
- Misturar moedas e unidades sem padronizar.
- Ignorar valores ausentes — a IA pode "preencher" com suposições.
- Enviar dados pessoais sem anonimizar [3].
- Não guardar a versão limpa — refazer limpeza toda vez é desperdício.
- Usar dados de fontes não oficiais sem cruzar com as séries do Banco Central [5] ou do IBGE [6].
- Não versionar a base limpa — impossibilita reproduzir análises e auditar resultados. A metodologia de padronização documental da ABNT serve de referência para organizar os artefatos de dados [18].
- Não validar tipos e domínios antes da análise — um texto no lugar de número quebra o cálculo silenciosamente. A documentação do pandas detalha os tipos de dados disponíveis [19].

## 6. Conclusão

Neste capítulo, você aprendeu a reconhecer as demonstrações financeiras e as séries temporais, montou o funil de qualidade do dado — ler, padronizar, validar, calcular, salvar — e aprendeu a anonimizar dados sensíveis antes de enviá-los à IA. Você agora entende que o dado limpo é o primeiro ativo de qualquer análise. Para treinar na prática, o curso de pandas da Quantecon oferece exercícios progressivos de manipulação de séries econômicas [20]. Desafio: pegue uma planilha real do seu trabalho e aplique o funil completo de limpeza, documentando cada transformação. No próximo capítulo, vamos à ferramenta que vai receber esses dados: a planilha, sua bancada de trabalho.

## 7. Referências Bibliográficas

[1] PANDAS. *Documentação oficial do pandas*. Disponível em: https://pandas.pydata.org/. Acesso em: 8 ago. 2026.
[2] WU, Z. et al. *Towards Competent AI for Fundamental Analysis in Finance: A Benchmark Dataset and Evaluation (FinAR-Bench)*. Disponível em: https://arxiv.org/html/2506.07315v2. Acesso em: 8 ago. 2026.
[3] PLANALTO. *Lei Geral de Proteção de Dados (Lei nº 13.709/2018)*. Disponível em: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm. Acesso em: 8 ago. 2026.
[4] PANDAS. *Documentação oficial do pandas*. Disponível em: https://pandas.pydata.org/. Acesso em: 8 ago. 2026.
[5] BANCO CENTRAL DO BRASIL. *Dados e estatísticas*. Disponível em: https://www.bcb.gov.br. Acesso em: 8 ago. 2026.
[6] IBGE. *Estatísticas econômicas*. Disponível em: https://www.ibge.gov.br. Acesso em: 8 ago. 2026.
[7] IPEA. *Instituto de Pesquisa Econômica Aplicada*. Disponível em: https://www.ipea.gov.br. Acesso em: 8 ago. 2026.
[8] SEBRAE. *Indicadores financeiros para pequenos negócios*. Disponível em: https://sebrae.com.br. Acesso em: 8 ago. 2026.
[9] META. *Prophet — Previsão de séries temporais*. Disponível em: https://facebook.github.io/prophet/. Acesso em: 8 ago. 2026.
[10] CVM. *Comissão de Valores Mobiliários*. Disponível em: https://www.gov.br/cvm. Acesso em: 8 ago. 2026.
[11] B3 EDUCA. *Educação financeira e mercado de capitais*. Disponível em: https://www.b3.com.br/pt_br/educacao. Acesso em: 8 ago. 2026.
[12] PYTHON PROGRAMMING FOR ECONOMICS AND FINANCE. *Pandas — Documentação*. Disponível em: https://python-programming.quantecon.org/pandas.html. Acesso em: 8 ago. 2026.
[13] MATPLOTLIB. *Documentação oficial do Matplotlib*. Disponível em: https://matplotlib.org/. Acesso em: 8 ago. 2026.
[14] SCIKIT-LEARN. *Documentação oficial do scikit-learn*. Disponível em: https://scikit-learn.org/. Acesso em: 8 ago. 2026.
[15] PANDASAI. *Inteligência Artificial para Business Intelligence*. Disponível em: https://pandas-ai.com/. Acesso em: 8 ago. 2026.
[16] GOOGLE CLOUD. *Finance AI*. Disponível em: https://cloud.google.com/discover/finance-ai. Acesso em: 8 ago. 2026.
[17] PARSEUR. *IA em Finanças*. Disponível em: https://parseur.com/pt/blog/ia-em-financas. Acesso em: 8 ago. 2026.
[18] ABNT. *Normas técnicas*. Disponível em: https://www.abnt.org.br. Acesso em: 8 ago. 2026.
[19] PANDAS. *Documentação oficial do pandas*. Disponível em: https://pandas.pydata.org/. Acesso em: 8 ago. 2026.
[20] PYTHON PROGRAMMING FOR ECONOMICS AND FINANCE. *Pandas — Documentação*. Disponível em: https://python-programming.quantecon.org/pandas.html. Acesso em: 8 ago. 2026.
