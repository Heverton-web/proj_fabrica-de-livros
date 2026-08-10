# Dossiê Técnico — IA no Trabalho para Análise do Setor Financeiro

> Obra: Como usar a IA no trabalho para análise do setor financeiro: planilhas, KPIs e análise de dados com modelos gratuitos.
> Público: iniciante | Tamanho: M (2 partes, 8 capítulos) | Refs mínimas por capítulo: 20.

## 1. Conceitos-chave e definições

- **IA generativa (GenAI):** classe de modelos que gera texto, código, tabelas e imagens a partir de instruções em linguagem natural. No trabalho financeiro, o uso dominante é o de **copiloto**: o profissional mantém o julgamento e a IA acelera a redação, a modelagem e a análise.
- **LLM (Large Language Model):** modelo de linguagem de grande escala treinado em trilhões de tokens; base dos assistentes ChatGPT, Gemini, Copilot e Claude.
- **Modelos gratuitos:** os planos free de ChatGPT, Google Gemini, Microsoft Copilot e Claude (janelas de 5h com cotas), além de modelos open-source (Llama, Mistral, Gemma, Qwen) executáveis localmente via Ollama, LM Studio ou llama.cpp — estes últimos sem cota, limitados apenas pelo hardware local.
- **Planilha assistida por IA:** três vias — IA nativa (Copilot no Excel, Gemini no Sheets), chat com planilha (add-ins do ChatGPT para Excel/Sheets) e funções de célula de terceiros (Numerous.ai, Ajelix, SheetAI).
- **KPI financeiro:** indicador quantitativo de desempenho — margem bruta, margem operacional, margem líquida, liquidez corrente, liquidez seca, EBITDA, DRE, fluxo de caixa, burn rate, runway, orçado vs realizado (Budget vs Actual).
- **Análise de dados:** pipeline de limpeza, transformação, exploração (EDA), visualização e modelagem. Ferramentas gratuitas: Python com pandas, Looker Studio (grátis), Power BI Desktop (grátis), Google Sheets, Excel.
- **RAG (Retrieval-Augmented Generation):** técnica que injeta documentos próprios no contexto do modelo para respostas fundamentadas; essencial para usar IA em dados sensíveis sem treinar o modelo.
- **Alucinação:** resposta factualmente incorreta produzida com aparência de segurança — o principal risco em finanças, onde erros numéricos têm consequência direta.
- **Text-to-SQL / Text-to-formula:** tradução de perguntas em linguagem natural para consultas SQL ou fórmulas de planilha executáveis.

## 2. Estado da arte (2024-2026)

- **ChatGPT (free):** conversas ilimitadas com modelos atuais, busca na web, upload de arquivos (CSV/XLSX/PDF) e ferramenta de Data Analysis que executa Python em ambiente isolado — permite limpeza de dados, estatística descritiva e gráficos sem instalar nada.
- **Google Gemini (free):** forte integração com Workspace (Docs, Drive, Sheets), multimodalidade nativa, janela de contexto ~32k tokens no free, cotas renováveis a cada 5h; Deep Research é pago.
- **Microsoft Copilot (free):** integrado ao Edge/Windows e apps Office na nuvem; ~15 boosts de imagem por dia; sem automação profunda do M365 pago.
- **Claude (free):** alta precisão lógica e de código; Artifacts para visualizar código/painéis; cotas de 15-40 mensagens por janela de 5h.
- **Open-source local (Llama, Mistral, Gemma, Qwen):** 7B-32B de parâmetros rodam em hardware doméstico com Ollama/LM Studio; garantem privacidade total (LGPD/GDPR) para dados financeiros sensíveis; suportam tool calling e text-to-SQL local.
- **Finanças com LLMs:** extração de demonstrativos financeiros (10-K, DRE), análise de sentimento de notícias, previsão de mercado com RAG+CoT, assistentes de finanças pessoais (ex.: caso Klarna), sumarização de relatórios e auditoria regulatória.
- **Dashboards gratuitos:** Looker Studio (grátis para criar e compartilhar; integração nativa com Sheets) e Power BI Desktop (grátis; Power Query + DAX; compartilhamento web exige licença).
- **Python/pandas:** padrão ouro para séries temporais e tabelas; PandasAI adiciona perguntas em linguagem natural aos DataFrames.

## 3. Boas práticas de modelagem com IA

1. **Peça a arquitetura antes das fórmulas** — instrua a IA a descrever abas, colunas e premissas antes de gerar a planilha.
2. **Separe premissas, entradas e saídas** — viabiliza análise de sensibilidade e cenários.
3. **Valide sempre** — a IA erra; confira com auditoria de cross-footing (somas cruzadas) e balanço fechado.
4. **Diagnóstico de erro dirigido:** peça para explicar a cadeia de fórmulas de uma célula com erro (#VALOR!, #DIV/0!) antes de corrigir.
5. **Cenários de estresse:** "crie aba pessimista com queda de 25% nas receitas e liste o impacto no EBITDA".
6. **Anonimize dados sensíveis** antes de enviar a nuvem; para dados confidenciais, use modelo local.

## 4. Riscos e limitações

- **Alucinação e erro numérico:** até a maioria dos engenheiros de ML relata sinais de alucinação em GenAI; decisões financeiras automáticas com base em alucinação podem gerar perdas e violar conformidade.
- **Vieses:** modelos treinados em dados históricos reproduzem vieses sistêmicos (crédito, scoring, risco) — risco regulatório e de discriminação.
- **Privacidade:** dados financeiros confidenciais não devem ir a APIs públicas sem anonimização; GDPR/LGPD criam conflito com dados absorvidos em treinamento.
- **Benchmark FinAR-Bench:** LLMs são competentes em extração de informação, mas ainda falham em cálculos complexos de indicadores (ROE, liquidez, margens) — reforça a necessidade de conferência humana.
- **Custo oculto do free:** cotas por janela de tempo, degradação em pico e limites de contexto.

## 5. Casos de uso reais

- Analista de controladoria: automação de DRE com análise vertical/horizontal via IA + verificação humana.
- Gestor de PME: dashboard mensal de KPIs no Looker Studio alimentado por planilha com fórmulas geradas por IA.
- Analista de crédito: extração de demonstrativos de PDF para planilha estruturada (ETL com IA).
- Finanças pessoais: assistente que categoriza gastos e sugere orçamento (Klarna como caso de escala).
- Conformidade: sumarização de relatórios regulatórios com RAG sobre documentos próprios.

## 6. Fontes brutas

- OPENAI. *ChatGPT — Pricing & Info*. Disponível em: https://chatgpt.com/pricing/. Acesso em: 8 ago. 2026.
- OPENAI. *Central de Ajuda: ChatGPT para Excel e Google Sheets*. Disponível em: https://help.openai.com/pt-br/articles/20001063-chatgpt-for-excel-and-google-sheets. Acesso em: 8 ago. 2026.
- GOOGLE. *Gemini Apps*. Disponível em: https://gemini.google.com/. Acesso em: 8 ago. 2026.
- GOOGLE. *Gemini Apps Support & Usage Limits*. Disponível em: https://support.google.com/gemini/answer/16275805. Acesso em: 8 ago. 2026.
- MICROSOFT. *Microsoft Copilot*. Disponível em: https://www.microsoft.com/en-us/microsoft-copilot. Acesso em: 8 ago. 2026.
- ANTHROPIC. *Claude AI*. Disponível em: https://claude.ai/. Acesso em: 8 ago. 2026.
- OLLAMA. *Ollama Library*. Disponível em: https://ollama.com/library. Acesso em: 8 ago. 2026.
- GOOGLE. *Gemma — Get Started*. Disponível em: https://ai.google.dev/gemma/docs/get_started. Acesso em: 8 ago. 2026.
- HUGGING FACE. *Open-Source Models*. Disponível em: https://huggingface.co/. Acesso em: 8 ago. 2026.
- PYTHON PROGRAMMING FOR ECONOMICS AND FINANCE. *Pandas — Documentação*. Disponível em: https://python-programming.quantecon.org/pandas.html. Acesso em: 8 ago. 2026.
- PANDASAI. *Inteligência Artificial para Business Intelligence*. Disponível em: https://pandas-ai.com/. Acesso em: 8 ago. 2026.
- PANDAS. *Documentação oficial do pandas*. Disponível em: https://pandas.pydata.org/. Acesso em: 8 ago. 2026.
- DATASIGHTS. *Looker Studio Financial Dashboard*. Disponível em: https://datasights.co/looker-studio-financial-dashboard/. Acesso em: 8 ago. 2026.
- CHILLMETRICS. *Looker Studio vs Power BI — Comparativo*. Disponível em: https://chillmetrics.co/en/blog/looker-studio-vs-power-bi-comparison/. Acesso em: 8 ago. 2026.
- COUPLER.IO. *Looker Studio Dashboard Examples*. Disponível em: https://blog.coupler.io/looker-studio-dashboard-examples/. Acesso em: 8 ago. 2026.
- GOOGLE CLOUD. *Finance AI*. Disponível em: https://cloud.google.com/discover/finance-ai. Acesso em: 8 ago. 2026.
- ADAPTA. *IA para Planilhas: ferramentas e como aplicar*. Disponível em: https://adapta.org/blog/ia-para-planilhas-ferramentas-e-como-aplicar. Acesso em: 8 ago. 2026.
- HASHTAG TREINAMENTOS. *Melhores ferramentas de IA para planilhas*. Disponível em: https://www.hashtagtreinamentos.com/ia-para-planilhas. Acesso em: 8 ago. 2026.
- PARSEUR. *IA em Finanças*. Disponível em: https://parseur.com/pt/blog/ia-em-financas. Acesso em: 8 ago. 2026.

## 7. Fontes complementares (documentação oficial, reguladores e dados)

- MICROSOFT. *Copilot no Excel*. Disponível em: https://support.microsoft.com/pt-br/copilot. Acesso em: 8 ago. 2026.
- GOOGLE. *Google Sheets — Lista de funções*. Disponível em: https://support.google.com/docs/table/25273. Acesso em: 8 ago. 2026.
- MICROSOFT. *Power BI Desktop*. Disponível em: https://powerbi.microsoft.com/pt-br/. Acesso em: 8 ago. 2026.
- GOOGLE. *Looker Studio*. Disponível em: https://lookerstudio.google.com/. Acesso em: 8 ago. 2026.
- NUMPY. *Documentação oficial do NumPy*. Disponível em: https://numpy.org/. Acesso em: 8 ago. 2026.
- MATPLOTLIB. *Documentação oficial do Matplotlib*. Disponível em: https://matplotlib.org/. Acesso em: 8 ago. 2026.
- SCIKIT-LEARN. *Documentação oficial do scikit-learn*. Disponível em: https://scikit-learn.org/. Acesso em: 8 ago. 2026.
- STATSMODELS. *Documentação oficial do statsmodels*. Disponível em: https://www.statsmodels.org/. Acesso em: 8 ago. 2026.
- META. *Prophet — Previsão de séries temporais*. Disponível em: https://facebook.github.io/prophet/. Acesso em: 8 ago. 2026.
- MICROSOFT. *Funções do Excel*. Disponível em: https://support.microsoft.com/pt-br/excel. Acesso em: 8 ago. 2026.
- SEBRAE. *Indicadores financeiros para pequenos negócios*. Disponível em: https://sebrae.com.br. Acesso em: 8 ago. 2026.
- B3 EDUCA. *Educação financeira e mercado de capitais*. Disponível em: https://www.b3.com.br/pt_br/educacao. Acesso em: 8 ago. 2026.
- CVM. *Comissão de Valores Mobiliários*. Disponível em: https://www.gov.br/cvm. Acesso em: 8 ago. 2026.
- BANCO CENTRAL DO BRASIL. *Dados e estatísticas*. Disponível em: https://www.bcb.gov.br. Acesso em: 8 ago. 2026.
- IBGE. *Estatísticas econômicas*. Disponível em: https://www.ibge.gov.br. Acesso em: 8 ago. 2026.
- IPEA. *Instituto de Pesquisa Econômica Aplicada*. Disponível em: https://www.ipea.gov.br. Acesso em: 8 ago. 2026.
- PLANALTO. *Lei Geral de Proteção de Dados (Lei nº 13.709/2018)*. Disponível em: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm. Acesso em: 8 ago. 2026.
- ANPD. *Autoridade Nacional de Proteção de Dados*. Disponível em: https://www.gov.br/anpd. Acesso em: 8 ago. 2026.
- EXCELJET. *Referência rápida de fórmulas do Excel*. Disponível em: https://exceljet.net. Acesso em: 8 ago. 2026.
- ABNT. *Normas técnicas*. Disponível em: https://www.abnt.org.br. Acesso em: 8 ago. 2026.

## 8. Artigos científicos (ABNT)

- DESAI, A. P. et al. *Generative-AI in Finance: Opportunities and Challenges*. arXiv:2410.15653. Disponível em: https://arxiv.org/html/2410.15653v3. Acesso em: 8 ago. 2026.
- LOPEZ-LIRA, A. et al. *Bridging Language Models and Financial Analysis*. arXiv:2503.22693. Disponível em: https://arxiv.org/html/2503.22693v1. Acesso em: 8 ago. 2026.
- WU, Z. et al. *Towards Competent AI for Fundamental Analysis in Finance: A Benchmark Dataset and Evaluation (FinAR-Bench)*. arXiv:2506.07315. Disponível em: https://arxiv.org/html/2506.07315v2. Acesso em: 8 ago. 2026.
- BAIN & COMPANY. *Generative AI in Financial Services: Eight Risks and How to Overcome Them*. Disponível em: https://www.bain.com/insights/generative-ai-in-financial-services/. Acesso em: 8 ago. 2026.
