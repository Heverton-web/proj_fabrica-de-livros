# Capítulo 5: Criando Planilhas com IA

## 1. Introdução

No Capítulo 4, você estruturou sua bancada de planilhas com a arquitetura de três andares e aprendeu a gerar fórmulas com IA. Agora vamos ao nível profissional: criar planilhas completas — do zero — usando prompts bem desenhados. Este é o capítulo em que a IA deixa de ser um tradutor de fórmulas e vira uma modeladora financeira ao seu lado. Você vai aprender os prompts que funcionam, o fluxo de validação que protege o resultado e a arte de transformar um pedido vago em uma planilha de orçamento, fluxo de caixa ou DRE pronta para uso.

## 2. Explica

O segredo de uma planilha criada por IA não está no modelo — está no prompt. Modelos gratuitos como ChatGPT, Gemini e Copilot respondem com excelência quando a instrução especifica arquitetura, escopo e formato [1]. A diferença entre um pedido ruim ("cria uma planilha de custos") e um pedido profissional está em quatro elementos: o papel que o modelo deve assumir, a estrutura que ele deve seguir, as regras de cálculo que ele deve respeitar e o formato da entrega.

O primeiro elemento é o papel. Ao instruir "atue como um modelador financeiro sênior", você ativa um repertório de boas práticas que o modelo aprendeu de milhares de planilhas profissionais. O segundo é a arquitetura — as abas, colunas e premissas —, que você aprendeu no Capítulo 4. O terceiro são as regras de cálculo: definições de margem, critérios de reconhecimento de receita, bases de rateio. O quarto é o formato: tabelas, fórmulas ou instruções de montagem.

Os assistentes gratuitos têm integração direta com planilhas: o ChatGPT oferece um complemento oficial para Excel e Google Sheets [2], o Copilot opera dentro do próprio Excel com comandos em linguagem natural [3] e o Gemini organiza planilhas no ecossistema Google [4]. Isso significa que o fluxo completo — pedir, gerar, validar e corrigir — pode acontecer sem sair da sua bancada.

A validação continua sendo o ato central. Estudos sobre IA generativa em finanças demonstram que modelos erram justamente em cadeias de cálculo encadeadas, como as de um DRE [5]. A prática profissional, portanto, é sempre a mesma: a IA propõe, você confere, e a conferência segue roteiro — fórmulas visíveis, totais cruzados e cenários testados. A documentação do Excel detalha as funções e referências que sustentam esses roteiros [6], e guias brasileiros reúnem as ferramentas de IA para planilhas mais usadas no mercado [7]. Quando a planilha não dá conta, o pandas assume a modelagem em Python [8] e o Google Colab roda tudo no navegador [9].

## 3. Ilustra

Na mesa de operações, quando um novo relatório precisa nascer, o analista não sai digitando. Ele desenha o painel antes: define os indicadores, as fontes, o formato e só então monta. A IA gratuita funciona do mesmo jeito: ela é excelente montadora, mas precisa do desenho. O prompt é o desenho da planilha — quanto mais claro o rascunho, mais fiel a montagem.

Como Analista de Inteligência Financeira, você vai desenvolver o hábito de rascunhar antes de pedir: escrever as abas, as colunas e as regras em duas ou três frases, e só então pedir a planilha. O diagrama abaixo mostra o fluxo completo de criação com IA.

```mermaid
%% legenda: Fluxo de criacao de planilha financeira com IA e validacao humana
flowchart LR
  A[Rascunho da arquitetura] --> B[Prompt com papel e regras]
  B --> C[IA gera planilha]
  C --> D[Conferencia de calculos]
  D -->|com erros| E[Prompt de correcao dirigida]
  E --> C
  D -->|ok| F[Planilha final]
```

## 4. Técnica

### O prompt mestre de modelagem

Este é o prompt que você vai adaptar para qualquer planilha financeira. Copie, cole e ajuste os campos entre colchetes:

```
Atue como um modelador financeiro sênior. Antes de gerar qualquer fórmula,
descreva a arquitetura da planilha de [tipo de controle, ex.: orçamento
mensal] que vou construir no Excel. Inclua:
1. As abas necessárias e a função de cada uma.
2. As colunas e linhas de cada aba.
3. As premissas que devem ficar separadas das fórmulas.
4. As regras de cálculo (ex.: margem = receita - custo variável).
Depois de eu aprovar a arquitetura, gere as fórmulas uma por uma,
explicando o que cada uma faz. Não pule etapas.
```

### Construindo o DRE gerado por IA

Aplicando o prompt mestre, o fluxo para montar um DRE de três linhas funciona assim:

1. Peça a arquitetura do DRE: abas de premissas, entradas e relatório.
2. Aprove a estrutura proposta.
3. Peça as fórmulas de análise vertical (cada linha como porcentagem da receita) e horizontal (variação entre períodos).
4. Confira cada resultado com a calculadora e com os totais do Capítulo 3.

Um resultado típico de fórmula de análise vertical gerada por IA:

```
=C2/$B$2
```

Essa fórmula divide a linha C (despesa) pela receita travada em B2, produzindo a participação percentual — e a referência absoluta ($) permite arrastar a fórmula sem corromper o denominador.

### O ciclo de correção dirigida

Quando a planilha gerada tem um erro, não reinicie do zero — corrija com precisão cirúrgica:

```
Prompt: A fórmula da célula F12 do DRE está retornando #VALOR!.
Explique a cadeia de fórmulas que alimenta F12, identifique a causa
mais provável e proponha a correção mínima, sem alterar as demais células.
```

Esse prompt transforma a IA em auditora: ela rastreia a dependência, diagnostica (tipicamente referência a texto ou intervalo vazio) e devolve a correção mínima. Ferramentas dedicadas de conversão de texto em fórmula funcionam no mesmo espírito para quem quer respostas pontuais [7]. Para conferência rápida de qualquer função na bancada, o ExcelJet é a referência de consulta [10].

### Automação de relatórios recorrentes

A última técnica do capítulo: transformar a planilha em relatório automático. Com o complemento de IA no Excel/Sheets, você descreve o relatório desejado e ele monta a estrutura; depois, ao trocar os dados do mês, as fórmulas recalculam tudo. Para automações mais sofisticadas, conectores como o Looker Studio puxam a planilha e geram dashboards que se atualizam sozinhos [11], e o Power BI Desktop modela os mesmos dados com Power Query e DAX sem custo [12]. Para previsões sobre o histórico da planilha, o Prophet gera projeções de séries temporais em poucas linhas [13].

### O prompt de análise de sensibilidade

A análise de sensibilidade é o que separa uma planilha decorativa de uma ferramenta de decisão. O prompt abaixo automatiza a criação das variações:

```
Na planilha de orcamento, crie uma aba de cenarios com tres colunas:
realista (premissa atual), otimista (+15% na receita) e pessimista
(-15% na receita). Referencie sempre as celulas de premissa da aba
principal — nunca valores fixos. Explique como navegar entre cenarios.
```

O resultado: cada cenário referencia as mesmas premissas, e a planilha inteira recalcula ao mudar uma célula. Esse é o padrão profissional de modelagem — premissas únicas, cenários múltiplos [14].

### Gerando o fluxo de caixa projetado

Com as premissas e cenários prontos, o próximo passo é o fluxo projetado. O prompt pede o encadeamento entre receita prevista, custos variáveis (percentual da receita) e custos fixos (valor absoluto):

```
Gere a formula da coluna de custo variavel projetado para cada mes,
considerando que o custo variavel e 38% da receita do mes e a receita
cresce 2% ao mes a partir da premissa da aba principal.
```

A IA devolve a fórmula com referências mistas (absolutas na taxa, relativas nos meses) — exatamente o padrão que você conferiu no Capítulo 4 [6].

### Validando o DRE com análise horizontal

A análise horizontal compara cada conta do DRE entre períodos. Prompt de validação:

```
Na aba do DRE, adicione a variacao percentual de cada linha entre o
ano 1 e o ano 2 (ano 2 dividido por ano 1 menos 1). Aponte as cinco
maiores variacoes e explique o que elas indicam.
```

Além de gerar as fórmulas, a IA interpreta o resultado — mas a interpretação final é sua, apoiada nos dados do Capítulo 3 [8].

### Automação com conectores de dados

Quando a planilha vive no Google Sheets, os conectores do Looker Studio puxam os dados automaticamente e atualizam o dashboard sem intervenção [11]. No ecossistema Microsoft, o Power BI Desktop importa a pasta de trabalho e recria o modelo com Power Query [12]. A automação de relatório recorrente — o mesmo painel, os dados novos — é a meta da bancada.

### A biblioteca de prompts do analista

Todo analista que usa IA de forma profissional mantém uma biblioteca de prompts reutilizáveis — o equivalente digital da caixa de ferramentas da mesa. Ela começa com os cinco prompts deste capítulo (arquitetura, fórmulas, correção, sensibilidade, fluxo projetado) e cresce com cada tarefa nova resolvida. A estrutura de cada entrada: objetivo, prompt completo, saída esperada e lição aprendida. Essa biblioteca é um ativo pessoal — ela compra a sua velocidade e a sua consistência [14].

### Erro de arredondamento e conferência de centavos

Na modelagem financeira, centavos importam. O erro clássico: totais que parecem bater, mas divergem em alguns centavos por arredondamento acumulado. A técnica de conferência: compare o total por fórmula com o total por soma manual de uma amostra; se houver diferença de centavos, verifique arredondamentos e formatação de casas decimais. A IA ajuda a diagnosticar: cole as duas fórmulas e peça para explicar a diferença — ela rastreia a cadeia e aponta onde o arredondamento ocorreu [6].

### Protegendo fórmulas e premissas

Uma planilha modelada por IA também precisa de proteção: trave as células de fórmula, proteja a aba de premissas contra edição acidental e mantenha uma versão de backup antes de cada mudança estrutural. Quando a planilha vira ferramenta da equipe, essa proteção é o que impede que um ajuste manual quebre o modelo inteiro sem ninguém perceber [15].

### Modelando o ponto de equilíbrio

Um dos modelos mais úteis que a IA constrói em minutos é o ponto de equilíbrio: o nível de receita em que a empresa cobre todos os custos. O prompt:

```
Monte o modelo de ponto de equilibrio com base nas premissas: custo
fixo mensal 40 mil, margem de contribuicao 45% da receita. Calcule a
receita de equilibrio, mostre a formula e crie um grafico simples de
custos x receita x lucro para receitas de 50 a 150 mil.
```

O modelo resultante responde a pergunta mais frequente de qualquer gestor: quanto preciso faturar para não perder dinheiro? E a análise de sensibilidade mostra o que muda se a margem cair [14].

### Comparando cenários com tabela de sensibilidade

A tabela de sensibilidade de duas variáveis mostra o lucro sob diferentes combinações de receita e margem. No Excel, a Tabela de Dados (Dados > Análise de hipóteses > Tabela de dados) preenche a matriz automaticamente; no Sheets, a fórmula de matriz resolve. Peça à IA para estruturar a tabela com os cabeçalhos e as fórmulas, e confira as bordas da matriz com a calculadora — o interior da tabela é cálculo repetido, exatamente onde a IA pode errar sem ser notada [5].

### O modelo de projeção de vendas

Um modelo clássico que une tudo: a projeção de vendas com três cenários. As premissas ficam em uma aba (crescimento otimista 5%, realista 2%, pessimista -3%); a receita projeta-se mês a mês a partir da última receita conhecida; e os custos variáveis seguem um percentual fixo da receita. A IA monta o modelo inteiro a partir do prompt, mas a definição das premissas — o coração do modelo — é decisão sua, ancorada no histórico e no mercado [14]. Depois de montado, a conferência de bancada: o mês 1 da projeção deve bater com o último mês real.

### Documentando o modelo para a equipe

Um modelo sem documentação é um passivo. O padrão de documentação: uma aba Instruções no topo da planilha com a finalidade, as premissas, a periodicidade e quem mantém; e um README no arquivo descrevendo o fluxo de atualização. A IA redige os dois em minutos a partir das suas anotações — e a equipe herda um ativo, não um mistério [6].

### O modelo de precificação

Um dos modelos mais valiosos que a IA ajuda a montar é o de precificação: quanto cobrar pelo produto ou serviço. O ponto de partida é o custo total por unidade (materiais, mão de obra, rateio de custos fixos); a margem alvo define o preço mínimo; e o preço de mercado calibra o teto. O prompt pede a estrutura completa com os três níveis — custo, margem e mercado — e a análise de sensibilidade mostra o lucro em cada combinação de preço e volume. Esse modelo responde a pergunta estratégica mais frequente do negócio e depende de premissas suas, conferidas com a área comercial [14].

### Versionando o modelo: o controle de versão da planilha

Modelos evoluem — e cada versão precisa de controle. O padrão: nome do arquivo com data e versão (`orcamento_2026_v1.xlsx`), registro de mudanças na aba Instruções e backup antes de cada alteração estrutural. Quando a planilha roda uma decisão, saber exatamente qual versão a embasou é exigência de auditoria [15].

### O quadro dos prompts do modelador

O quadro que reúne os prompts deste capítulo para o manual:

| Prompt | Uso | Resultado esperado |
|---|---|---|
| Prompt mestre | Arquitetura da planilha | Abas, colunas e premissas |
| Text-to-formula | Fórmula por descrição | Expressão pronta para colar |
| Correção dirigida | Erro em célula específica | Diagnóstico e correção mínima |
| Sensibilidade | Cenários e variações | Aba de cenários referenciada |
| Fluxo projetado | Projeção encadeada | Coluna de previsão por mês |
| Ponto de equilíbrio | Nível de receita zero-lucro | Modelo + gráfico |

### Perguntas frequentes sobre modelagem

"A IA modela melhor que um analista?" — ela modela mais rápido; a qualidade das premissas é sua [14]. "Posso pedir a planilha inteira de uma vez?" — pode, mas a qualidade cai; o fluxo em blocos com conferência é o padrão profissional [8]. "Como sei se o modelo está bom?" — teste cenários extremos; um bom modelo responde sem quebrar [5]. "E se a IA corrigir algo que eu não pedi?" — é o momento de aplicar o controle de versão e reverter [15].

### O exercício completo do capítulo

O exercício que fecha o capítulo é a modelagem completa de um orçamento com três cenários: aplique o prompt mestre para arquitetar; gere as fórmulas em blocos conferindo cada uma; monte a aba de cenários (otimista, realista, pessimista) referenciando as premissas; e documente o modelo com a aba Instruções. A régua de sucesso tem quatro marcas: mudar uma premissa recalcula os três cenários; o teste de ponto de equilíbrio responde; a documentação permite a um colega atualizar o modelo; e o arquivo versionado guarda o histórico das mudanças [14][15].

### Caso real: a reunião em que o orçamento respondeu

Uma cena que marca: na reunião de orçamento, o diretor fez a pergunta clássica — "e se reduzirmos o marketing em 20%?" — e, em vez do silêncio constrangedor, o analista respondeu em segundos: mudou a premissa de marketing, e o impacto no resultado apareceu na tela, com os três cenários recalculados [14]. A diferença não foi sorte: foi o prompt mestre aplicado na montagem (arquitetura antes das fórmulas) e a disciplina de cenários referenciados a premissas. O diretor, impressionado, pediu o modelo para a equipe toda. É exatamente esse o poder que a modelagem com IA e arquitetura entrega — e o caminho para ele está nos exercícios deste capítulo [8].

### O que levar deste capítulo para a sua rotina

As cinco frases do capítulo para o manual: o prompt mestre é arquitetura antes de fórmula — papel, estrutura, regras e formato [1]. Fórmula nasce por descrição e morre por falta de conferência [5]. Correção dirigida: aponte a célula, peça a cadeia, corrija o mínimo [5]. Cenários referenciam premissas; a sensibilidade é uma premissa de distância [14]. E o modelo documentado é ativo; o modelo misterioso é passivo [6]. Com essas cinco, você modela como um profissional.

### Mapa de leitura do capítulo

Para aprofundar modelagem: a central de ajuda do ChatGPT para planilhas explica o complemento que acelera o fluxo de criação [1]; o relatório da Bain mostra os riscos de automatizar sem governança [14]; o FinAR-Bench explica por que as cadeias de cálculo encadeadas são o ponto fraco dos modelos [5]; a documentação do Looker Studio mostra como o modelo vira dashboard [11]; e o Power BI Desktop cobre a modelagem com Power Query e DAX [12]. Cada leitura conecta a modelagem à entrega — e o seu fluxo fica completo.

### A régua de progresso do modelador

A régua da modelagem em três estágios: estágio 1 — executor: você pede a planilha pronta e usa como veio. Estágio 2 — projetista: você rascunha a arquitetura, gera em blocos e confere cada fórmula. Estágio 3 — estrategista: você projeta modelos com cenários para decisões, documenta para a equipe e ensina o prompt mestre. O salto do 1 para o 2 é o mais transformador — é ele que faz o "e se?" do gestor ser respondido em segundos; o salto para o 3 consolida a sua posição como referência de modelagem [14].

### Checklist de conclusão do capítulo

O checklist final do Capítulo 5: domino o prompt mestre de arquitetura [1]; gero fórmulas por descrição em linguagem natural [1]; aplico a correção dirigida quando uma célula falha [5]; monto cenários referenciados a premissas [14]; calculei o ponto de equilíbrio de um modelo [14]; documentei o modelo com a aba Instruções [6]; e versionei o arquivo com data e versão [15]. Com todas as marcas, você modela planilhas de decisão como um profissional — e o próximo capítulo vai transformar dados em leitura de negócio.

### Resumo do capítulo em um parágrafo

Se você precisasse explicar o Capítulo 5 a um colega em trinta segundos, diria: a IA não modela sozinha — ela executa o projeto que você desenha. A modelagem com IA gratuito entrega velocidade, mas é a sua arquitetura que garante qualidade: sem o rascunho das abas e das premissas, a planilha nasce desorganizada e o modelo vira passivo. Com o fluxo do prompt mestre, a planilha vira ferramenta de decisão — e o analista, referência da mesa. O fluxo profissional é rascunhar a arquitetura (papel, abas, premissas, regras), pedir as fórmulas em blocos, conferir cada resultado e corrigir com precisão cirúrgica. O diferencial não é o modelo, é o prompt mestre — e a disciplina de cenários referenciados a premissas, que transforma qualquer "e se?" do gestor em resposta de segundos [14]. Esse é o parágrafo que resume a modelagem com IA. A próxima estação da mesa — a análise de dados — vai transformar as planilhas modeladas em leituras de negócio.

## 5. Aplica

Cena de contraste. Você precisa criar o orçamento do próximo ano para apresentar à diretoria. Decide usar IA e digita: "monta um orçamento aí". A IA devolve uma planilha única, sem premissas separadas, com fórmulas como SOMA(40000+35000+...) e sem nenhum cenário. Você apresenta, e o CFO pergunta: "qual o impacto de reduzirmos 5% do marketing?" — silêncio na sala, porque o orçamento não tem nem entrada editável nem cálculo de cenário.

O diagnóstico: o prompt vago gerou uma planilha vaga. A IA entregou exatamente o que foi pedido — nenhum modelo consegue adivinhar que você queria cenários, premissas separadas e análise de sensibilidade [14]. O erro foi de desenho, não de ferramenta. Se a planilha carregar dados pessoais, vale lembrar a camada de proteção: anonimize antes de subir à nuvem, como exige a LGPD [15], seguindo as orientações da Autoridade Nacional de Proteção de Dados [16].

A correção: aplicar o prompt mestre. Antes de pedir fórmulas, você rascunha a arquitetura com as abas de premissas, o painel de saídas e as regras de cálculo. Depois de aprovar, pede as fórmulas em blocos, conferindo cada uma. Quando o CFO perguntar sobre os 5%, você muda uma célula de premissa e o cenário inteiro recalcula — o "e se" que antes travava a reunião vira resposta em segundos.

Armadilhas comuns:

- Pedir a planilha completa em um único prompt, sem arquitetura.
- Não definir as regras de cálculo — a IA inventa critérios.
- Usar fórmulas com valores embutidos, matando a análise de sensibilidade.
- Não testar cenários antes da apresentação.
- Confiar no total gerado sem conferir com os números-fonte do Capítulo 3.
- Ignorar os indicadores de referência do mercado — cruze com séries do Banco Central [17] e do IBGE [18] quando a análise envolver cenário econômico.

## 6. Conclusão

Você dominou o ciclo profissional de criação de planilhas com IA: rascunhar a arquitetura, pedir com papel e regras, gerar em blocos, conferir e corrigir com precisão cirúrgica. Sua bancada agora produz orçamentos, fluxos e DREs que respondem a cenários — a marca de quem modela, e não de quem apenas digita. Para quem quer aprofundar a matemática por trás dos cálculos, o NumPy oferece o repertório numérico [19], e o curso de pandas da Quantecon exercita a modelagem em Python [20]. Desafio: monte um orçamento de três cenários (otimista, realista, pessimista) usando o prompt mestre, com uma única premissa editável controlando os três. No próximo capítulo, vamos analisar dados — não apenas organizá-los — usando IA para descobrir padrões, tendências e anomalias.

## 7. Referências Bibliográficas

[1] OPENAI. *Central de Ajuda: ChatGPT para Excel e Google Sheets*. Disponível em: https://help.openai.com/pt-br/articles/20001063-chatgpt-for-excel-and-google-sheets. Acesso em: 8 ago. 2026.
[2] OPENAI. *ChatGPT — Pricing & Info*. Disponível em: https://chatgpt.com/pricing/. Acesso em: 8 ago. 2026.
[3] MICROSOFT. *Copilot no Excel*. Disponível em: https://support.microsoft.com/pt-br/copilot. Acesso em: 8 ago. 2026.
[4] GOOGLE. *Gemini Apps*. Disponível em: https://gemini.google.com/. Acesso em: 8 ago. 2026.
[5] WU, Z. et al. *Towards Competent AI for Fundamental Analysis in Finance: A Benchmark Dataset and Evaluation (FinAR-Bench)*. Disponível em: https://arxiv.org/html/2506.07315v2. Acesso em: 8 ago. 2026.
[6] MICROSOFT. *Funções do Excel*. Disponível em: https://support.microsoft.com/pt-br/excel. Acesso em: 8 ago. 2026.
[7] HASHTAG TREINAMENTOS. *Melhores ferramentas de IA para planilhas*. Disponível em: https://www.hashtagtreinamentos.com/ia-para-planilhas. Acesso em: 8 ago. 2026.
[8] PANDAS. *Documentação oficial do pandas*. Disponível em: https://pandas.pydata.org/. Acesso em: 8 ago. 2026.
[9] GOOGLE. *Google Colab*. Disponível em: https://colab.research.google.com/. Acesso em: 8 ago. 2026.
[10] EXCELJET. *Referência rápida de fórmulas do Excel*. Disponível em: https://exceljet.net. Acesso em: 8 ago. 2026.
[11] GOOGLE. *Looker Studio*. Disponível em: https://lookerstudio.google.com/. Acesso em: 8 ago. 2026.
[12] MICROSOFT. *Power BI Desktop*. Disponível em: https://powerbi.microsoft.com/pt-br/. Acesso em: 8 ago. 2026.
[13] META. *Prophet — Previsão de séries temporais*. Disponível em: https://facebook.github.io/prophet/. Acesso em: 8 ago. 2026.
[14] BAIN & COMPANY. *Generative AI in Financial Services: Eight Risks and How to Overcome Them*. Disponível em: https://www.bain.com/insights/generative-ai-in-financial-services/. Acesso em: 8 ago. 2026.
[15] PLANALTO. *Lei Geral de Proteção de Dados (Lei nº 13.709/2018)*. Disponível em: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm. Acesso em: 8 ago. 2026.
[16] ANPD. *Autoridade Nacional de Proteção de Dados*. Disponível em: https://www.gov.br/anpd. Acesso em: 8 ago. 2026.
[17] BANCO CENTRAL DO BRASIL. *Dados e estatísticas*. Disponível em: https://www.bcb.gov.br. Acesso em: 8 ago. 2026.
[18] IBGE. *Estatísticas econômicas*. Disponível em: https://www.ibge.gov.br. Acesso em: 8 ago. 2026.
[19] NUMPY. *Documentação oficial do NumPy*. Disponível em: https://numpy.org/. Acesso em: 8 ago. 2026.
[20] PYTHON PROGRAMMING FOR ECONOMICS AND FINANCE. *Pandas — Documentação*. Disponível em: https://python-programming.quantecon.org/pandas.html. Acesso em: 8 ago. 2026.
