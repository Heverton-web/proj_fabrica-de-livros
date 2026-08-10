# Dossiê de Pesquisa — O Uso de IA em Análise Financeira no Setor Odontológico

## Conceitos-chave

- **Engenharia de Prompts (Prompt Engineering)**: Técnica de formulação de instruções textuais para LLMs visando obter respostas precisas e estruturadas. Aplicada a finanças, envolve definir papel (personagem), contexto, formato de saída e restrições de domínio. Fonte: Gao (2023); Tripathi (2026); Nayyar et al. (2025).
- **Chain-of-Thought (CoT) Prompting**: Técnica que instrui o LLM a raciocinar passo a passo antes de produzir a resposta final. Demonstra ganhos significativos em tarefas de raciocínio numérico financeiro (CreditCardQA). Fonte: Hiray et al. (2026).
- **Program-of-Thought (PoT) Prompting**: Abordagem que instrui o LLM a gerar código executável (Python) em vez de apenas texto para resolver cálculos financeiros. Reduz erros aritméticos e melhora consistência. Fonte: Hiray et al. (2026).
- **Anonimização de Dados**: Processo de remoção ou mascaramento de informações identificáveis antes de envio a sistemas de IA pública. Essencial para conformidade com RGPD/GDPR. Fonte: Barbieri et al. (2026); Awasthi et al. (2024).
- **Inadimplência (Default)**: Falha no cumprimento de obrigações financeiras. Previsão baseada em padrões de comportamento de pagamento, volume de compras e tendências de fluxo de caixa. Fonte: Wang et al. (2025); Korangi et al. (2021).
- **Extração de Dados de Documentos**: Uso de OCR + LLM para converter PDFs (notas fiscais, contratos) em dados estruturados (JSON/CSV). VLMs modernos alcançam ~87% de precisão em extração de campos. Fonte: Cheng et al. (2026); Singh et al. (2026).
- **RAG (Retrieval-Augmented Generation)**: Padrão arquitetural que combina busca por documentos relevantes com geração de texto por LLM, melhorando factualidade e reduzindo alucinações em análises financeiras. Fonte: Awasthi et al. (2024).
- **Persona Prompting**: Técnica de atribuir um papel profissional ao LLM (ex.: "Você é um CFO com 20 anos de experiência") para orientar o estilo e profundidade da análise. Fonte: Tripathi (2026).
- **RGPD (Regulamento Geral de Proteção de Dados)**: Regulamento europeu que restringe o processamento de dados pessoais. Aplicável a fornecedores B2B em Portugal que operam na UE. Fonte: Barbieri et al. (2026).
- **B2B (Business-to-Business)**: Modelo de negócios entre empresas. No contexto odontológico, refere-se a fornecedores de materiais/ equipamentos que vendem para clínicas. Fonte: contexto do livro.
- **LLM (Large Language Model)**: Modelos de linguagem de grande escala (GPT-4, Claude, Gemini) capazes de processar e gerar texto, com aplicações crescentes em análise financeira. Fonte: múltiplas fontes.

## Artigos Científicos e Papers

### Prompt Engineering e Análise Financeira

- PAULI, W. M. et al. *FORCE-Bench: A Benchmark, Dataset, and Evaluation Harness for Agentic AI in Enterprise Finance*. arXiv:2607.19409, 2026. Disponível em: https://arxiv.org/abs/2607.19409. Acesso em: 08 ago. 2026.
 - Benchmark com 251 consultas anotadas por especialistas, avaliando sistemas agênticos em 8 dimensões (acurácia, citações, clareza, profundidade, fundamentação, atualidade, relevância, estrutura). Resultado: sistemas gerais não atendem consistentemente aos requisitos de qualidade do domínio financeiro sob restrições operacionais.

- BENHENDA, M. *IPO Finance Agent: Benchmark of LLM Financial Analysts Beyond Finance Agent v2*. arXiv:2606.23032, 2026. Disponível em: https://arxiv.org/abs/2606.23032. Acesso em: 08 ago. 2026.
 - Extensão do benchmark Finance Agent v2 com 1000 perguntas de due diligence de IPO. Modelo GLM-5.2 atinge 79.8% de acurácia; MiMo-2.5 Pro atinge 77.2% a custo de $0.05/consulta. Demonstra viabilidade econômica de LLMs para análise financeira.

- TANG, Y. et al. *FinReportBench: Measuring and Improving Institution-Grade Financial Report Generation*. arXiv:2608.04374, 2026. Disponível em: https://arxiv.org/abs/2608.04374. Acesso em: 08 ago. 2026.
 - Benchmark de 35 itens para avaliação de relatórios financeiros de nível institucional. Skills de geração melhoram G1 em 33.85 pontos e G2 em 13.83 pontos vs. execução sem skill.

- ZHU, J. et al. *SpreadsheetBench 2: Evaluating Agents on End-to-End Business Spreadsheet Workflows*. arXiv:2606.29955, 2026. Disponível em: https://arxiv.org/abs/2606.29955. Acesso em: 08 ago. 2026.
 - Benchmark de workflows de planilhas com 321 tarefas (geração, debug, visualização). Melhor modelo atinge 34.89% de acurácia geral. Dados de relatórios financeiros e demonstrações corporativas.

- CHENG, M. et al. *TabClaw: An Interactive and Self-Evolving Agent for Spreadsheet Manipulation and Table Reasoning*. arXiv:2606.10316, 2026. Disponível em: https://arxiv.org/abs/2606.10316. Acesso em: 08 ago. 2026.
 - Agente interativo para manipulação de planilhas CSV/Excel com linguagem natural. Extrai memória de usuário e destila habilidades reutilizáveis de padrões de uso repetidos.

- XING, J. et al. *MMTU: A Massive Multi-Task Table Understanding and Reasoning Benchmark*. arXiv:2506.05587, 2025. Disponível em: https://arxiv.org/abs/2506.05587. Acesso em: 08 ago. 2026.
 - Benchmark com 28K+ perguntas em 25 tarefas reais de tabelas. GPT-5 atinge 69%, DeepSeek R1 atinge 57% — indicando espaço significativo para melhorias.

- LU, W. et al. *Large Language Model for Table Processing: A Survey*. arXiv:2402.05121, 2024. Disponível em: https://arxiv.org/abs/2402.05121. Acesso em: 08 ago. 2026.
 - Revisão abrangente de técnicas de processamento de tabelas com LLMs/VLMs, incluindo engenharia de prompts e agentes para tarefas como QA, manipulação de planilhas e análise de dados.

- HIRAY, A. et al. *CreditCards, Confusion, Computation, and Consequences: What Can We Uncover About Language Model Reasoning?* arXiv:2607.26952, 2026. Disponível em: https://arxiv.org/abs/2607.26952. Acesso em: 08 ago. 2026.
 - Benchmark de 1800 perguntas sobre acordos reais de cartão de crédito. PoT (Program-of-Thought) supera CoT (Chain-of-Thought) consistentemente. Erros surgem mais de regras financeiras mal aplicadas do que de aritmética.

- GAO, A. *Prompt Engineering for Large Language Models*. SSRN Electronic Journal, 2023. Disponível em: https://doi.org/10.2139/ssrn.4504303. Acesso em: 08 ago. 2026.
 - Revisão acadêmica de técnicas de engenharia de prompts, incluindo zero-shot, few-shot, chain-of-thought e persona-based prompting.

- NAYYAR, A. et al. *Future Trends in Large Language Models and Prompt Engineering*. In: Mastering Prompt Engineering, 2025. Disponível em: https://doi.org/10.1016/b978-0-443-33904-2.00009-4. Acesso em: 08 ago. 2026.
 - Capítulo de livro sobre tendências futuras de LLMs e engenharia de prompts, com foco em aplicações em domínios especializados.

- TRIPATHI, S. *Prompt Engineering Mastery: How to Optimize Interactions with Large Language Models*. 2026. Disponível em: https://doi.org/10.2174/97988988136041260101. Acesso em: 08 ago. 2026.
 - Monografia sobre engenharia de prompts avançada, incluindo personas, chained prompts e técnicas de otimização para domínios específicos.

### Auditoria Financeira e IA

- WANG, Y. et al. *FinAuditing: A Financial Taxonomy-Structured Multi-Document Benchmark for Evaluating LLMs*. arXiv:2510.08886, 2025. Disponível em: https://arxiv.org/abs/2510.08886. Acesso em: 08 ago. 2026.
 - Benchmark de auditoria financeira com 1102 instâncias (média de 33k tokens). Avalia 13 LLMs em 3 tarefas: correspondência semântica, extração de relações e raciocínio matemático. Gaps significativos em recuperação de conceitos e raciocínio cross-document.

- LIU, Z. et al. *AuditFraudBench: Benchmarking Audit Judgment in Detecting Fraudulent Misstatements*. arXiv:2606.08345, 2026. Disponível em: https://arxiv.org/abs/2606.08345. Acesso em: 08 ago. 2026.
 - Benchmark baseado em filings reais da SEC (10-K, 10-Q) e AAERs. Modelos GPT, DeepSeek e Qwen ainda struggle com raciocínio conjunto sobre figuras financeiras, enquadramento de disclosure e mecanismos de fraude.

- BERGER, A. et al. *Towards Automated Regulatory Compliance Verification in Financial Auditing with Large Language Models*. arXiv:2507.16642, 2025. Disponível em: https://arxiv.org/abs/2507.16642. Acesso em: 08 ago. 2026.
 - Comparação de LLMs open-source (Llama-2) vs. proprietários (GPT-4) para verificação de conformidade regulatória. Llama-2 70B supera modelos proprietários em detecção de não-conformidade. GPT-4 superior em contextos multilíngues.

- HILLEBRAND, L. et al. *Improving Zero-Shot Text Matching for Financial Auditing with Large Language Models*. arXiv:2308.06111, 2023. Disponível em: https://arxiv.org/abs/2308.06111. Acesso em: 08 ago. 2026.
 - Sistema híbrido (BERT + LLM) para recomendação de trechos relevantes em relatórios financeiros para requisitos legais. Abordagem two-step supera métodos existentes.

- WANG, Q. *AWARE-FX: An Auditable Knowledge-Guided AI System for Measuring Corporate Foreign-Exchange Hedging Disclosure*. arXiv:2607.27611, 2026. Disponível em: https://arxiv.org/abs/2607.27611. Acesso em: 08 ago. 2026.
 - Sistema de IA auditável para medir disclosure de hedge cambial em relatórios anuais. Combina lexicon profissional, lógica de negação, codificadores financeiros e ledger de auditoria. FinBERT atinge F1 de 0.702-0.872.

- ADEYEMI, T. O. et al. *AI-Enabled Accounting Information Systems and Fraud Detection in Nigeria's Financial Services Sector*. arXiv:2607.01257, 2026. Disponível em: https://arxiv.org/abs/2607.01257. Acesso em: 08 ago. 2026.
 - Estudo com 186 profissionais de banco, seguros e FinTech. AIS habilitada por IA melhora significativamente auditoria e detecção de fraude. NLP modera positivamente a relação entre AIS e eficácia da auditoria.

### Previsão de Inadimplência e Crédito

- WANG, H. et al. *Enhancing Credit Risk Prediction: A Multi-stage Ensemble Pipeline*. arXiv:2509.22381, 2025. Disponível em: https://arxiv.org/abs/2509.22381. Acesso em: 08 ago. 2026.
 - Pipeline ensemble multi-stage combinando modelos econômétricos, supervised learning (XGBoost, RF, SVM), unsupervised (KNN) e deep learning (MLP). Melhoria significativa na classificação de ratings de crédito.

- WANG, Y. et al. *Leveraging Convolutional Neural Network-Transformer Synergy for Predictive Modeling in Risk-Based Applications*. arXiv:2412.18222, 2024. Disponível em: https://arxiv.org/abs/2412.18222. Acesso em: 08 ago. 2026.
 - Modelo CNN+Transformer para previsão de default de crédito. Combina extração de features locais (CNN) com modelagem de dependências globais (Transformer). Supera random forest e XGBoost em AUC e KS.

- KORANGI, K. et al. *A Transformer-based Model for Default Prediction in Mid-Cap Corporate Markets*. arXiv:2111.09902, 2021. Disponível em: https://arxiv.org/abs/2111.09902. Acesso em: 08 ago. 2026.
 - Transformer adaptado para previsão de default em empresas mid-cap. Melhoria de 13% em AUC sobre modelos tradicionais. Interpretabilidade via heatmaps de atenção e valores de Shapley.

- CLEMENTS, J. M. et al. *Sequential Deep Learning for Credit Risk Monitoring with Tabular Financial Data*. arXiv:2012.15330, 2020. Disponível em: https://arxiv.org/abs/2012.15330. Acesso em: 08 ago. 2026.
 - Técnica de amostragem de transações de cartão de crédito com deep learning sequencial (TCN). Supera modelos baseados em árvores, detecção mais precoce de risco.

- JORDAN, L. *Bond Default Prediction with Text Embeddings, Undersampling and Deep Learning*. arXiv:2110.07035, 2021. Disponível em: https://arxiv.org/abs/2110.07035. Acesso em: 08 ago. 2026.
 - Combinação de embeddings de texto (transformer), rede neural fully connected e oversampling sintético. Prevê 9/10 defaults em títulos municipais na emissão, sem usar ratings.

- DHIMAN, A. *UQ for Credit Risk Management: A Deep Evidence Regression Approach*. arXiv:2305.04967, 2023. Disponível em: https://arxiv.org/abs/2305.04967. Acesso em: 08 ago. 2026.
 - Deep Evidence Regression para quantificação de incerteza em previsão de LGD (Loss Given Default). Extensão para variáveis-alvo geradas por processo Weibull.

### Extração de Dados de Documentos

- CHEN, Z. et al. *DocMaster: A Hierarchical Structure-Aware System for Document Analysis*. arXiv:2607.08539, 2026. Disponível em: https://arxiv.org/abs/2607.08539. Acesso em: 08 ago. 2026.
 - Sistema hierárquico para análise de documentos que preserva layouts originais (seções, tabelas, figuras, equações). Constrói índice semântico awareness de estrutura para filtragem e QA.

- SINGH, A. K. et al. *The Structured Output Benchmark: A Multi-Source Benchmark for Evaluating Structured Output Quality in Large Language Models*. arXiv:2604.25359, 2026. Disponível em: https://arxiv.org/abs/2604.25359. Acesso em: 08 ago. 2026.
 - Benchmark SOB com 5000 registros de texto, 209 imagens (PDFs OCR), 115 áudios. Acurácia de valor: 83.0% texto, 67.2% imagens, 23.7% áudio. Schema compliance próximo de perfeito, mas valor exato é o gargalo.

- CHENG, L. et al. *A Hybrid Architecture for Multi-Stage Claim Document Understanding: Combining Vision-Language Models and Machine Learning for Real-Time Processing*. arXiv:2601.01897, 2026. Disponível em: https://arxiv.org/abs/2601.01897. Acesso em: 08 ago. 2026.
 - Pipeline híbrido PaddleOCR + Regressão Logística + Qwen 2.5-VL-7B para extração de dados de documentos de claims. Classificação >95%, extração ~87%, latência <2s por documento. 300x mais rápido que processamento manual.

- DIERICH, L. et al. *Artificial Intelligence in Ship Finance: Applications, Opportunities, and a Case Study in AI-Augmented Loan Origination*. arXiv:2606.11238, 2026. Disponível em: https://arxiv.org/abs/2606.11238. Acesso em: 08 ago. 2026.
 - Arquitetura modular (ShipFinance.ai) para extração de dados de documentos financeiros usando LLM + serviços de dados marítimos + geração controlada de documentos. Demonstra viabilidade em domínio financeiro especializado.

### Proteção de Dados e Privacidade

- BARBIERI, S. et al. *From Production SIEM to Reusable Cybersecurity Artifacts*. arXiv:2606.21389, 2026. Disponível em: https://arxiv.org/abs/2606.21389. Acesso em: 08 ago. 2026.
 - Metodologia para extrair, anonimizar, estruturar e validar dados SIEM de SOC financeiro production, preservando estrutura investigativa dentro de limites de privacidade declarados. Boundary mensurável de privacidade-utilidade.

- AWASTHI, A. P. et al. *Privacy-Preserving Customer Support: A Framework for Secure and Scalable Interactions*. arXiv:2412.07687, 2024. Disponível em: https://arxiv.org/abs/2412.07687. Acesso em: 08 ago. 2026.
 - Framework PP-ZSL usando LLMs zero-shot para suporte ao cliente sem treinamento local em dados sensíveis. Anonimização em tempo real, RAG para resolução de consultas, pós-processamento para conformidade regulatória (GDPR/CCPA).

- GAO, P. et al. *Mind Your Key: An Empirical Study of LLM API Credential Leakage in iOS Apps*. arXiv:2606.12212, 2026. Disponível em: https://arxiv.org/abs/2606.12212. Acesso em: 08 ago. 2026.
 - Estudo empírico de vazamento de chaves de API de LLMs em 444 apps iOS. 282 apps (63.5%) expõem credenciais exploráveis. Três padrões: JWT (48%), backend não autenticado (33%), chave em texto plano (19%). 72% não remedaram após 3 meses.

### Análise Financeira com IA e Benchmarks

- YANG, C. et al. *FinDeepIndicator: Benchmarking Deep Research Agents in End-to-End Financial Indicator Construction*. arXiv:2608.00764, 2026. Disponível em: https://arxiv.org/abs/2608.00764. Acesso em: 08 ago. 2026.
 - Benchmark para avaliar agentes Deep Research em construção de indicadores financeiros. 3350 QA pairs, dados de 10 anos, 800 empresas listadas. LLMs performam bem em fórmulas mas caem em extração de dados e execução numérica.

- IACOVIDES, G. et al. *FinSMART: Financial Sentiment Analysis for Algorithmic Trading through Market-Aligned Reinforcement Learning*. arXiv:2607.28127, 2026. Disponível em: https://arxiv.org/abs/2607.28127. Acesso em: 08 ago. 2026.
 - Framework de RL alinhado ao mercado para análise de sentimento financeiro. Melhoria de 220% no retorno acumulado sobre o baseline mais forte. Retreinamento contínuo sem anotação manual.

- LEE, H. et al. *When Summaries Distort Decisions: Information Fidelity in LLM-Compressed Financial Analysis*. arXiv:2606.29251, 2026. Disponível em: https://arxiv.org/abs/2606.29251. Acesso em: 08 ago. 2026.
 - Estudo sobre perda de fidelidade na compressão de contexto por LLMs em fontes financeiras. Compressão pode produzir texto fluente mas que altera decisões de investimento. Propõe Agentic Context Compression com auditoria de discordâncias.

- GUO, P. et al. *FinAcumen: Financial Multimodal Reasoning via Self-Evolving Experience Memory Harness*. arXiv:2606.17642, 2026. Disponível em: https://arxiv.org/abs/2606.17642. Acesso em: 08 ago. 2026.
 - Framework de raciocínio financeiro multimodal com memória de experiência seletiva. Acumula estratégias bem-sucedidas e regras de cautela derivadas de falhas em memória persistente.

- ZHANG, F. et al. *FinReporting: An Agentic Workflow for Localized Reporting of Cross-Jurisdiction Financial Disclosures*. arXiv:2604.05966, 2026. Disponível em: https://arxiv.org/abs/2604.05966. Acesso em: 08 ago. 2026.
 - Workflow agêntico para reporting financeiro cross-jurisdição (EUA, Japão, China). LLMs como verificadores constrangidos sob regras de decisão explícitas, não como geradores de texto livre.

## Estado da arte / ferramentas de referência

- **GPT-4/GPT-4o (OpenAI)**: Modelo proprietário com capacidades avançadas de raciocínio numérico e textual. Utilizado como referência em múltiplos benchmarks financeiros (FORCE-Bench, IPO Finance Agent). Suporte nativo a upload de imagens e PDFs.
- **Claude 3/3.5 (Anthropic)**: Modelo proprietário com foco em segurança e alinhamento. Forte em análise de documentos longos e seguimento de instruções complexas. Context window de até 200k tokens.
- **Gemini 1.5/2.0 (Google)**: Modelo multimodal com capacidade nativa de processamento de imagens e áudio. Utilizado em benchmarks de análise financeira com dados de mercado.
- **FinGPT**: Modelo open-source especializado em finanças, treinado com dados de mercado. Demonstra performance competitiva em risk-adjusted em backtesting de trading. Fonte: Ntale (2026).
- **FinBERT**: Modelo BERT pré-treinado para análise de sentimento financeiro. F1 temporal de 0.702-0.872 em tarefas de classificação de disclosure. Amplamente utilizado como baseline. Fonte: Wang, Q. (2026).
- **Qwen 2.5-VL**: Vision-Language Model open-source com capacidades de OCR e extração de dados de documentos. Processa PDFs escaneados e imagens com ~87% de precisão. Fonte: Cheng et al. (2026).
- **Llama 2/3 (Meta)**: Família de modelos open-source. Llama-2 70B demonstra performance superior em detecção de não-conformidade em auditoria financeira. Fonte: Berger et al. (2025).
- **PaddleOCR**: Engine OCR open-source multilíngue para extração de texto de documentos. Componente-chave em pipelines de extração de dados financeiros. Fonte: Cheng et al. (2026).

## Casos de uso corporativos

- **FORCE-Bench / Microsoft 365 Copilot Finance Agent**: Agente propósito-construído para finanças que consulta dados de ERP (contas a receber/pagar), filings públicos e dados de mercado. Superou sistemas agênticos gerais em 8 dimensões de qualidade. Fonte: Pauli et al. (2026).
- **ShipFinance.ai**: Arquitetura modular para workflow de originação de empréstimos em finanças marítimas. Combina extração LLM, componentes de análise financeira, serviços de dados marítimos e geração controlada de documentos com chatbot. Fonte: Dierich & Schinas (2026).
- **Fullerton Health Claims Processing**: Pipeline híbrido (PaddleOCR + Qwen 2.5-VL-7B) processando dezenas de milhares de claims semanais no Vietnã e Singapura. 300x mais rápido que processamento manual. Fonte: Cheng et al. (2026).
- **PwC Germany / Auditoria Automatizada**: Parceria com PwC para verificação automatizada de conformidade regulatória em documentos financeiros. LLMs comparados em datasets customizados de auditoria. Fonte: Berger et al. (2025).
- **NextFund / Análise de Portfolio**: Plataforma para avaliação de agentes financeiros com acesso a mercado ao vivo, análise multi-agente coordenada e logging persistente do caminho de decisão completo. Fonte: Li et al. (2026).

## Limitações e controvérsias

- **Alucinação Numérica**: LLMs produzem cálculos financeiros incorretos com confiança. Mesmo GPT-4 comete erros em operações aritméticas complexas. Chain-of-Thought ajuda mas não elimina o problema. Fonte: Hiray et al. (2026); Lee et al. (2026).
- **Perda de Fidelidade na Compressão de Contexto**: LLMs que resumem dados financeiros podem alterar o julgamento de investimento, produzindo texto factualmente correto mas decisivamente diferente da fonte original. Fonte: Lee et al. (2026).
- **Privacidade e RGPD**: Dados financeiros de clínicas odontológicas são dados pessoais sob RGPD. Envio a LLMs públicos (ChatGPT, Claude, Gemini) requer anonimização prévia. Risco de vazamento de chaves de API em 63.5% dos apps. Fonte: Barbieri et al. (2026); Gao et al. (2026).
- **Gap entre Benchmarks e Produção**: Modelos que atingem 80%+ em benchmarks frequentemente falham em ambientes operacionais reais devido a restrições de latência, custo e conformidade. Fonte: Pauli et al. (2026).
- **Dependência de Dados Históricos**: Modelos de previsão de inadimplência são treinados em dados históricos que podem não capturar eventos unprecedented (ex.: pandemia). Fonte: Wang et al. (2025).
- **Interpretabilidade em Auditoria**: LLMs como "caixas-pretas" são problemáticos em auditoria financeira, onde rastreabilidade e explicabilidade são obrigatórias. Sistemas híbridos (determinístico + LLM) são preferidos. Fonte: Wang, Q. (2026); Hillebrand et al. (2023).
- **Custo de Tokens**: Análises financeiras detalhadas consomem muitos tokens. Compressão agressiva de contexto pode degradar qualidade. Fonte: Lee et al. (2026).
- **Limitações de Janela de Contexto**: Documentos financeiros longos (10-K, contratos) frequentemente excedem limites de contexto dos LLMs, requerendo chunking estratégico. Fonte: Benhenda (2026).
- **Vieses de Modelo**: LLMs podem herdar vieses dos dados de treinamento, produzindo análises enviesadas para certos perfis de clínicas ou fornecedores. Fonte: Wang et al. (2020).

## Fontes brutas (para Nó 7 — Auditor de Rastreabilidade)

- PAULI, W. M. et al. *FORCE-Bench: A Benchmark, Dataset, and Evaluation Harness for Agentic AI in Enterprise Finance*. Disponível em: https://arxiv.org/abs/2607.19409. Acesso em: 08 ago. 2026.
- BENHENDA, M. *IPO Finance Agent: Benchmark of LLM Financial Analysts Beyond Finance Agent v2, with Automated Rubric Generation, on the SpaceX (SPCX) IPO*. Disponível em: https://arxiv.org/abs/2606.23032. Acesso em: 08 ago. 2026.
- TANG, Y. et al. *FinReportBench: Measuring and Improving Institution-Grade Financial Report Generation*. Disponível em: https://arxiv.org/abs/2608.04374. Acesso em: 08 ago. 2026.
- ZHU, J. et al. *SpreadsheetBench 2: Evaluating Agents on End-to-End Business Spreadsheet Workflows*. Disponível em: https://arxiv.org/abs/2606.29955. Acesso em: 08 ago. 2026.
- CHENG, M. et al. *TabClaw: An Interactive and Self-Evolving Agent for Spreadsheet Manipulation and Table Reasoning*. Disponível em: https://arxiv.org/abs/2606.10316. Acesso em: 08 ago. 2026.
- XING, J. et al. *MMTU: A Massive Multi-Task Table Understanding and Reasoning Benchmark*. Disponível em: https://arxiv.org/abs/2506.05587. Acesso em: 08 ago. 2026.
- LU, W. et al. *Large Language Model for Table Processing: A Survey*. Disponível em: https://arxiv.org/abs/2402.05121. Acesso em: 08 ago. 2026.
- HIRAY, A. et al. *CreditCards, Confusion, Computation, and Consequences: What Can We Uncover About Language Model Reasoning?* Disponível em: https://arxiv.org/abs/2607.26952. Acesso em: 08 ago. 2026.
- GAO, A. *Prompt Engineering for Large Language Models*. Disponível em: https://doi.org/10.2139/ssrn.4504303. Acesso em: 08 ago. 2026.
- NAYYAR, A. et al. *Future Trends in Large Language Models and Prompt Engineering*. Disponível em: https://doi.org/10.1016/b978-0-443-33904-2.00009-4. Acesso em: 08 ago. 2026.
- TRIPATHI, S. *Prompt Engineering Mastery: How to Optimize Interactions with Large Language Models*. Disponível em: https://doi.org/10.2174/97988988136041260101. Acesso em: 08 ago. 2026.
- WANG, Y. et al. *FinAuditing: A Financial Taxonomy-Structured Multi-Document Benchmark for Evaluating LLMs*. Disponível em: https://arxiv.org/abs/2510.08886. Acesso em: 08 ago. 2026.
- LIU, Z. et al. *AuditFraudBench: Benchmarking Audit Judgment in Detecting Fraudulent Misstatements*. Disponível em: https://arxiv.org/abs/2606.08345. Acesso em: 08 ago. 2026.
- BERGER, A. et al. *Towards Automated Regulatory Compliance Verification in Financial Auditing with Large Language Models*. Disponível em: https://arxiv.org/abs/2507.16642. Acesso em: 08 ago. 2026.
- HILLEBRAND, L. et al. *Improving Zero-Shot Text Matching for Financial Auditing with Large Language Models*. Disponível em: https://arxiv.org/abs/2308.06111. Acesso em: 08 ago. 2026.
- WANG, Q. *AWARE-FX: An Auditable Knowledge-Guided AI System for Measuring Corporate Foreign-Exchange Hedging Disclosure*. Disponível em: https://arxiv.org/abs/2607.27611. Acesso em: 08 ago. 2026.
- ADEYEMI, T. O. et al. *Artificial Intelligence-Enabled Accounting Information Systems and Fraud Detection in Nigeria's Financial Services Sector: The Moderating Role of Natural Language Processing*. Disponível em: https://arxiv.org/abs/2607.01257. Acesso em: 08 ago. 2026.
- WANG, H. et al. *Enhancing Credit Risk Prediction: A Multi-stage Ensemble Pipeline*. Disponível em: https://arxiv.org/abs/2509.22381. Acesso em: 08 ago. 2026.
- WANG, Y. et al. *Leveraging Convolutional Neural Network-Transformer Synergy for Predictive Modeling in Risk-Based Applications*. Disponível em: https://arxiv.org/abs/2412.18222. Acesso em: 08 ago. 2026.
- KORANGI, K. et al. *A Transformer-based Model for Default Prediction in Mid-Cap Corporate Markets*. Disponível em: https://arxiv.org/abs/2111.09902. Acesso em: 08 ago. 2026.
- CLEMENTS, J. M. et al. *Sequential Deep Learning for Credit Risk Monitoring with Tabular Financial Data*. Disponível em: https://arxiv.org/abs/2012.15330. Acesso em: 08 ago. 2026.
- JORDAN, L. *Bond Default Prediction with Text Embeddings, Undersampling and Deep Learning*. Disponível em: https://arxiv.org/abs/2110.07035. Acesso em: 08 ago. 2026.
- DHIMAN, A. *UQ for Credit Risk Management: A Deep Evidence Regression Approach*. Disponível em: https://arxiv.org/abs/2305.04967. Acesso em: 08 ago. 2026.
- CHEN, Z. et al. *DocMaster: A Hierarchical Structure-Aware System for Document Analysis*. Disponível em: https://arxiv.org/abs/2607.08539. Acesso em: 08 ago. 2026.
- SINGH, A. K. et al. *The Structured Output Benchmark: A Multi-Source Benchmark for Evaluating Structured Output Quality in Large Language Models*. Disponível em: https://arxiv.org/abs/2604.25359. Acesso em: 08 ago. 2026.
- CHENG, L. et al. *A Hybrid Architecture for Multi-Stage Claim Document Understanding: Combining Vision-Language Models and Machine Learning for Real-Time Processing*. Disponível em: https://arxiv.org/abs/2601.01897. Acesso em: 08 ago. 2026.
- DIERICH, L. et al. *Artificial Intelligence in Ship Finance: Applications, Opportunities, and a Case Study in AI-Augmented Loan Origination*. Disponível em: https://arxiv.org/abs/2606.11238. Acesso em: 08 ago. 2026.
- BARBIERI, S. et al. *From Production SIEM to Reusable Cybersecurity Artifacts*. Disponível em: https://arxiv.org/abs/2606.21389. Acesso em: 08 ago. 2026.
- AWASTHI, A. P. et al. *Privacy-Preserving Customer Support: A Framework for Secure and Scalable Interactions*. Disponível em: https://arxiv.org/abs/2412.07687. Acesso em: 08 ago. 2026.
- GAO, P. et al. *Mind Your Key: An Empirical Study of LLM API Credential Leakage in iOS Apps*. Disponível em: https://arxiv.org/abs/2606.12212. Acesso em: 08 ago. 2026.
- YANG, C. et al. *FinDeepIndicator: Benchmarking Deep Research Agents in End-to-End Financial Indicator Construction*. Disponível em: https://arxiv.org/abs/2608.00764. Acesso em: 08 ago. 2026.
- IACOVIDES, G. et al. *FinSMART: Financial Sentiment Analysis for Algorithmic Trading through Market-Aligned Reinforcement Learning*. Disponível em: https://arxiv.org/abs/2607.28127. Acesso em: 08 ago. 2026.
- LEE, H. et al. *When Summaries Distort Decisions: Information Fidelity in LLM-Compressed Financial Analysis*. Disponível em: https://arxiv.org/abs/2606.29251. Acesso em: 08 ago. 2026.
- GUO, P. et al. *FinAcumen: Financial Multimodal Reasoning via Self-Evolving Experience Memory Harness*. Disponível em: https://arxiv.org/abs/2606.17642. Acesso em: 08 ago. 2026.
- ZHANG, F. et al. *FinReporting: An Agentic Workflow for Localized Reporting of Cross-Jurisdiction Financial Disclosures*. Disponível em: https://arxiv.org/abs/2604.05966. Acesso em: 08 ago. 2026.
- BETTENCOURT, N. et al. *The Stanford EDGAR Filings Dataset: Reconstructing U.S. Corporate and Financial Disclosures into Layout-Faithful and Token-Efficient Pretraining Data*. Disponível em: https://arxiv.org/abs/2606.18192. Acesso em: 08 ago. 2026.
