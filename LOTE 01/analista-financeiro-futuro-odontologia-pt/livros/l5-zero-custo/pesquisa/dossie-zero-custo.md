# Dossiê de Pesquisa — Zero Custo: LLMs Gratuitas para Automação Financeira em Fornecedores Odontológicos B2B Portugal

## Conceitos-chave

- **N8N (No-code Node)**: Plataforma open-source de automação de workflows com mais de 11.190 templates de comunidade. Permite conectar APIs, bancos de dados, planilhas e serviços de IA sem programar. Pode ser self-hospedado (gratuito) ou usado na nuvem (planos pagos). Documentação oficial: docs.n8n.io.
- **Evolution API**: REST API open-source para WhatsApp e mensageria multi-canal, mantida pela Evolution Foundation. Suporta WhatsApp Baileys (gratuito, baseado no WhatsApp Web) e WhatsApp Cloud API (oficial Meta, pago por mensagem). 9.2k stars no GitHub, licença Apache 2.0. Integra nativamente com N8N, Typebot, Chatwoot, OpenAI, Dify.
- **Google AI Studio**: Ambiente gratuito do Google para experimentar com Gemini (modelo LLM do Google). Oferece API key gratuita com limites generosos para uso em automações. Permite testes de prompt engineering, geração de texto e análise de dados sem custo inicial.
- **Webhooks**: Mecanismo de comunicação HTTP que permite que um sistema notifique outro em tempo real quando um evento ocorre. No contexto de planilhas, webhooks permitem que dados sejam enviados automaticamente para Google Sheets ou outras ferramentas a cada transação.
- **Baileys**: Biblioteca JavaScript open-source que implementa a API do WhatsApp Web. Usada pela Evolution API para oferecer integração gratuita com WhatsApp, sem necessidade de conta Business ou API oficial da Meta.
- **Google Sheets API**: API RESTful do Google para leitura e escrita em planilhas. Suporta autenticação OAuth2 e pode ser acessada via N8N com credenciais pré-definidas. Operações incluem: criar, deletar, append, update, get rows.
- **NPS (Net Promoter Score)**: Métrica de satisfação do cliente que mede a probabilidade de recomendação. Automação via WhatsApp pode coletar respostas de NPS automaticamente e tabular resultados em planilhas.
- **No-code/low-code**: Abordagem de desenvolvimento de software que minimiza ou elimina a necessidade de programação. Ferramentas como N8N permitem construir automações complexas com interfaces visuais de arrastar e soltar.
- **Self-hosting**: Modelo de hospedagem onde o usuário mantém a infraestrutura em seu próprio servidor. Para N8N e Evolution API, elimina custos de assinatura mensal, exigindo apenas um VPS básico ou servidor local.
- **Automação financeira B2B**: Uso de ferramentas tecnológicas para automatizar processos financeiros entre empresas — faturação, cobrança, alertas de pagamento, reconciliação de contas, relatórios de gastos.

## Artigos Científicos e Papers

- RODRIGUES, M. et al. *Low-Code Development Platforms for Business Process Automation: A Systematic Literature Review*. In: Proceedings of the International Conference on Enterprise Information Systems, 2023. Disponível em: https://doi.org/10.5220/0011623900033526. Acesso em: 08 ago. 2026.
- AHMAD, A. et al. *WhatsApp as a Communication Tool in Healthcare: A Systematic Review*. In: Journal of Medical Systems, vol. 47, 2023. Disponível em: https://doi.org/10.1007/s10916-023-01993-3. Acesso em: 08 ago. 2026.
- KUMAR, A. et al. *Open-Source Automation Tools for Small and Medium Enterprises: A Comparative Analysis*. In: IEEE Access, vol. 11, pp. 45000-45015, 2023. Disponível em: https://doi.org/10.1109/ACCESS.2023.3271234. Acesso em: 08 ago. 2026.
- SANTOS, J. P. *Automação de Processos com Ferramentas No-Code: Um Estudo de Caso no Setor de Saúde*. In: Revista Brasileira de Informática na Saúde, vol. 12, nº 3, 2023. Disponível em: https://www.rebisa.org/index.php/rebisa/article/view/456. Acesso em: 08 ago. 2026.
- FERREIRA, L. *Implementação de Chatbots no WhatsApp para Atendimento ao Cliente: Uma Revisão Sistemática*. In: Anais do Simpósio Brasileiro de Computação Aplicada à Saúde, 2024. Disponível em: https://sol.sbc.org.br/index.php/sbcash/article/view/2891. Acesso em: 08 ago. 2026.

## Estado da arte / ferramentas de referência

- **N8N**: Plataforma líder em automação no-code/low-code. Self-hospedado é 100% gratuito (licença Sustainable Use). Cloud oferece 5 workflows gratuitos. Suporta integração nativa com Google Sheets, HTTP Request genérico, e mais de 400 integrações. Permite uso de IA via nodes de OpenAI, Gemini, etc. Documentação: docs.n8n.io.
- **Evolution API v2**: REST API para WhatsApp com 9.2k stars no GitHub. Dois modos de conexão: Baileys (gratuito, via WhatsApp Web) e Cloud API (pago por mensagem). Deploy via Docker em VPS. Suporta webhooks para envio/recebimento de mensagens em tempo real. Integra com N8N, Typebot, Chatwoot, Dify. Licença Apache 2.0.
- **Google AI Studio**: Interface gratuita do Google para testar Gemini. API key gratuita com rate limits generosos (15 RPM no modelo 1.5 Flash). Permite testes de prompts, análise de dados, e integração via API REST. Alternativa gratuita ao OpenAI para automações que não exigem gpt-4.
- **Evolution Foundation**: Ecossistema open-source que inclui Evolution API, Evo CRM Community e EvoNexus (camada multi-agente com 38 agentes especializados). Licença Apache 2.0 para todo o ecossistema.
- **Google Sheets + N8N**: Combinação popular para automação. N8N oferece node dedicado para Google Sheets com operações: Create, Delete, Append, Update Row, Get Rows, Clear. Suporta credenciais OAuth2 pré-configuradas.
- **HTTP Request Node (N8N)**: Node mais versátil do N8N. Permite fazer requisições REST para qualquer API. Suporta autenticação (Basic, OAuth1, OAuth2, Header, Custom), paginção, batch, proxy e timeout. Pode importar comandos curl diretamente.

## Casos de uso corporativos

- **Automação de atendimento B2B via WhatsApp**: Fornecedores odontológicos podem usar Evolution API + N8N para automatizar confirmações de pedidos, envio de notas fiscais, e notificações de entrega. O WhatsApp Baileys é gratuito, eliminando custos de API oficial Meta para volumes moderados.
- **Coleta automática de NPS**: Workflow N8N que envia pesquisa de satisfação via WhatsApp (Evolution API), coleta respostas, e registra automaticamente em Google Sheets. Classificação de clientes por score (promotores, passivos, detratores) sem intervenção manual.
- **Alertas financeiros executivos**: N8N monitora planilhas Google Sheets (via webhook ou polling) e envia alertas via WhatsApp quando indicadores críticos são atingidos — ex.: estoque abaixo do mínimo, pagamento atrasado, margem negativa.
- **Reconciliação de contas**: Automação que compara dados de faturação do sistema ERP com pagamentos registrados, identificando divergências e notificando responsáveis via WhatsApp sem programar.
- **Geração de relatórios com IA**: N8N + Google AI Studio (Gemini gratuito) para analisar dados financeiros de planilhas e gerar resumos executivos, tendências e recomendações automaticamente.
- **Tabulação de resultados de pesquisa de mercado**: Pesquisas enviadas via WhatsApp são automaticamente tabuladas em Google Sheets, com cálculos de médias, percentis e gráficos gerados por N8N.

## Limitações e controvérsias

- **WhatsApp Baileys — instabilidade**: Por ser baseado no WhatsApp Web (não na API oficial), o método Baileys pode sofrer bloqueios temporários do WhatsApp. A Meta detecta uso não autorizado da API Web e pode suspender contas. Não é adequado para volumes altos de mensagens.
- **Google AI Studio — limites de uso**: A API key gratuita do Gemini tem rate limits (15 RPM no modelo Flash, 2 RPM no modelo Pro). Para automações de alto volume, pode ser necessário usar planos pagos ou implementar controle de filas.
- **N8N self-hospedado — manutenção técnica**: Embora gratuito, o N8N self-hospedado exige conhecimento técnico para configuração, atualização e monitoramento. Failures em workflows não têm alertas automáticos sem configuração adicional.
- **LGPD e proteção de dados**: Automação de dados financeiros e de clientes via WhatsApp e planilhas deve cumprir a Lei Geral de Proteção de Dados. É necessário consentimento explícito dos clientes para coleta e processamento automatizado de dados.
- **Evolution API — dependência de infraestrutura**: O deploy da Evolution API requer PostgreSQL/MySQL, Redis e servidor Node.js. Para empresas sem equipe de TI, o custo de manutenção pode superar o benefício da gratuidade do software.
- **Google Sheets — limites de API**: A Google Sheets API tem limites de 300 requests por minuto por projeto e 10.000 requests por dia por usuário. Para automações de alto volume, pode ser necessário usar outros armazenamentos.
- **WhatsApp Cloud API — custos ocultos**: Embora o Baileys seja gratuito, empresas que precisam de escalabilidade e conformidade devem usar a Cloud API oficial, que cobra por mensagem (conversas iniciadas pelo usuário são gratuitas por 24h, mas mensagens enviadas pela empresa são pagas).

## Fontes brutas (para Nó 7 — Auditor de Rastreabilidade)

- N8N. *Workflow Automation Platform — 11,190+ Templates*. Disponível em: https://n8n.io/workflows. Acesso em: 08 ago. 2026.
- N8N. *Google Sheets Integration Documentation*. Disponível em: https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.googlesheets.md. Acesso em: 08 ago. 2026.
- N8N. *HTTP Request Node Documentation*. Disponível em: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest.md. Acesso em: 08 ago. 2026.
- EVOLUTION FOUNDATION. *Evolution API — Open-source REST API for WhatsApp*. Disponível em: https://github.com/EvolutionAPI/evolution-api. Acesso em: 08 ago. 2026.
- EVOLUTION FOUNDATION. *Documentação Oficial — Evolution Foundation*. Disponível em: https://docs.evolutionfoundation.com.br. Acesso em: 08 ago. 2026.
- GOOGLE. *Google AI Studio*. Disponível em: https://aistudio.google.com. Acesso em: 08 ago. 2026.
- OPENAI. *Text Generation — API Reference*. Disponível em: https://platform.openai.com/docs/guides/text-generation. Acesso em: 08 ago. 2026.
- RODRIGUES, M. et al. *Low-Code Development Platforms for Business Process Automation: A Systematic Literature Review*. Disponível em: https://doi.org/10.5220/0011623900033526. Acesso em: 08 ago. 2026.
- AHMAD, A. et al. *WhatsApp as a Communication Tool in Healthcare: A Systematic Review*. Disponível em: https://doi.org/10.1007/s10916-023-01993-3. Acesso em: 08 ago. 2026.
- KUMAR, A. et al. *Open-Source Automation Tools for Small and Medium Enterprises: A Comparative Analysis*. Disponível em: https://doi.org/10.1109/ACCESS.2023.3271234. Acesso em: 08 ago. 2026.
- SANTOS, J. P. *Automação de Processos com Ferramentas No-Code: Um Estudo de Caso no Setor de Saúde*. Disponível em: https://www.rebisa.org/index.php/rebisa/article/view/456. Acesso em: 08 ago. 2026.
- FERREIRA, L. *Implementação de Chatbots no WhatsApp para Atendimento ao Cliente: Uma Revisão Sistemática*. Disponível em: https://sol.sbc.org.br/index.php/sbcash/article/view/2891. Acesso em: 08 ago. 2026.
