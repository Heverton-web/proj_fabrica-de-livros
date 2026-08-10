---
title: "Zero Custo! Como fazer isso utilizando LLMs gratuitas ou de baixíssimo custo"
subtitle: "Apresentação · Engenheiro de Automação Financeira"
author: "Heverton Eduardo Peres"
lang: pt-BR
---

# Objetivo

Apresentar a promessa de construir um motor de inteligência financeira com custo zero — sem depender de TI, sem orçamento, com ferramentas que já existem.

# O caminho

- **Bancada** — capítulos 1, 2
- **Ferramenta** — capítulos 3, 4

# Arsenal e Fundamentos

> Estágio 1 de 2

# O Arsenal Gratuito do Analista

*Mapear e configurar as ferramentas de IA gratuitas disponíveis (Google AI Studio, Hugging Face) para análise financeira*

- Google AI Studio: tier gratuito generoso com Gemini (15 RPM no Flash)
- Hugging Face: 100+ modelos open-source gratuitos para classificação e extração
- Stack recomendado: Google Sheets + N8N + Evolution API + Google AI Studio

# O Poder dos Webhooks

*Ensinar o leitor a entender e configurar webhooks para conectar planilhas financeiras a serviços externos sem programar*

- Lógica de transmissão: escuta (webhook receiver) e disparo (webhook sender)
- N8N como orquestrador: node HTTP Request genérico conecta qualquer API REST
- Google Sheets como banco de dados leve: triggers e actions via N8N

`curl http://localhost:3000/webhook/log`

# Automação na Prática

> Estágio 2 de 2

# Automação Pós-Venda na Prática

*Criar um fluxo visual com N8N para automatizar pesquisa de satisfação (NPS) e tabular feedbacks dos dentistas automaticamente*

- N8N: 11.190+ templates, self-hospedado gratuito, 400+ integrações nativas
- Pipeline NPS: disparo → coleta → tabulação → alerta — tudo visual, sem código
- Casos reais: Vodafone (£2.2M savings), Huel (1.000h savings), Bordr ($100K solo founder)

`docker-compose up -d`

# Alertas Executivos

*Integrar a planilha finalizada a ferramentas de mensageria (Evolution API) para alertas automáticos no WhatsApp da diretoria*

- Evolution API: WhatsApp Baileys gratuito via Docker — ideal para volumes B2B moderados
- Alerta de grande venda: trigger no N8N quando faturamento ultrapassa limiar
- Risco e mitigação: bloqueio da Meta → plano B com Cloud API (pago por mensagem)

`docker-compose -f docker-compose-evolution.yml up -d`

# Próximo passo

**Zero Custo! Como fazer isso utilizando LLMs gratuitas ou de baixíssimo custo**

Leia a obra completa
