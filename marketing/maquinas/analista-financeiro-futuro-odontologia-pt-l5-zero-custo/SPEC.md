# SPEC.md — Especificação Completa da Máquina de Vendas

## 1. Visão Geral

Máquina de vendas automatizada que capta leads via Instagram, nutre por e-mail,
e converte em vendas de produtos digitais. Opera 24/7 com correção automática
de testes A/B e monitoramento de métricas em tempo real.

## 2. Objetivos

| Objetivo | Métrica | Meta |
|----------|---------|------|
| Captura de leads | Leads/dia | 50-100 |
| Nutrição | Taxa de abertura | >35% |
| Conversão | Taxa de venda | >2% |
| Reativação | Leads reengajados | >10% |
| Autonomia | Intervenção manual | <1h/semana |

## 3. Personas

### 3.1 Aspirante a Autor (primária)
- **Faixa:** 28-55 anos
- **Dor:** Não sabe como começar a escrever/publicar
- **Desejo:** Ter livro publicado e gerar renda passiva
- **Canais:** Instagram, E-mail
- **Tom:** Motivacional, acolhedor, prático

### 3.2 Empreendedor Digital
- **Faixa:** 25-45 anos
- **Dor:** Funil não converte, lista parada
- **Desejo:** Automatizar vendas e escalar receita
- **Canais:** Instagram, E-mail, LinkedIn
- **Tom:** Direto, dados, prova social

### 3.3 Coach / Consultor
- **Faixa:** 30-55 anos
- **Dor:** Depende só de hora-aula
- **Desejo:** Criar produtos escaláveis
- **Canais:** Instagram, E-mail, LinkedIn
- **Tom:** Profissional, inspirador, estratégico

## 4. Funis de Vendas

### 4.1 Funil Nutrição → Livro
```
Lead novo → Boas-vindas (imediato)
         → Nutrição (+24h)
         → Venda (+48h)
         → Reativação (+72h, se inativo)
```

### 4.2 Funil Reativação
```
Lead frio → Reativação (imediato)
         → Venda (+48h, se abriu)
```

### 4.3 Funil Upsell
```
Comprador → Upsell Masterclass (+48h)
```

## 5. Produtos

| Produto | Preço | Tipo | Entrega |
|---------|-------|------|---------|
| Livro: O Autor Digital | R$ 47,00 | Ebook | Instantânea |
| Funil Masterclass | R$ 197,00 | Curso | Plataforma |
| Bundle Marketing Digital | R$ 67,00 | Bundle | Instantânea |

## 6. Canais de Aquisição

### 6.1 Instagram (ativo)
- Busca por hashtags do nicho
- Análise de bio para matching de persona
- Score automático (0-100)
- Rate limit: 100 leads/dia

### 6.2 E-mail (ativo)
- Sequências automatizadas por funil
- Tracking de abertura e clique
- A/B test de assuntos
- Rate limit: 200 envios/dia

### 6.3 LinkedIn (fase 2)
### 6.4 WhatsApp (fase 2)
### 6.5 YouTube (fase 3)

## 7. Automação

### 7.1 Lead Hunter
- **Trigger:** Cron diário 08:00
- **Input:** Hashtags do `config/canais.json`
- **Processo:** Busca → Filtra → Score → Persiste
- **Output:** Novos leads no banco

### 7.2 Email Sender
- **Trigger:** Contínuo (15min)
- **Input:** Leads pendentes em `email_sequence`
- **Processo:** Renderiza template → Envia → Atualiza step
- **Output:** E-mails enviados, steps avançados

### 7.3 Funnel Monitor
- **Trigger:** Daemon (5min)
- **Input:** Banco de dados
- **Processo:** Coleta métricas → Exporta JSON → Alertas
- **Output:** `metrics.json`, alertas webhook

### 7.4 Auto-Correct
- **Trigger:** Horário
- **Input:** Resultados de experimentos
- **Processo:** Teste Z → p-value → Redistribui tráfego
- **Output:** Tráfego ajustado automaticamente

## 8. Testes A/B

### 8.1 Metodologia
- Teste Z para proporções (two-tailed)
- Nível de significância: 95% (p < 0.05)
- Amostra mínima: 30 por variante
- Correção automática quando significativo

### 8.2 Regras de Correção
| Lift | Ação | Tráfego |
|------|------|---------|
| >20% | Promovido | 100% vencedor |
| 10-20% | Ajustado | 80/20 |
| <10% | Ajustado leve | 70/30 |

## 9. Métricas Monitoradas

| Métrica | Frequência | Alerta |
|---------|------------|--------|
| Leads novos/semana | Contínuo | <10 |
| Taxa de abertura | Por envio | <20% |
| Taxa de clique | Por envio | <3% |
| Taxa de conversão | Diária | <1% |
| Leads frios | Diária | >50% do total |

## 10. Segurança e Compliance

- LGPD: consentimento explícito, direito ao esquecimento
- CAN-SPAM: unsubscribe em todos os e-mails
- Rate limits: proteção contra abuso de APIs
- Backup: diário automático do banco de dados
- Criptografia: TLS para SMTP, HTTPS para API

## 11. Deploy

### Produção
```bash
bash scripts/deploy.sh full
```

### Staging
```bash
bash scripts/deploy.sh docker
```

### Rollback
```bash
bash scripts/deploy.sh rollback v1.0.0
```

## 12. Roadmap

- [x] Fase 1: Instagram + E-mail + Monitor
- [ ] Fase 2: LinkedIn + WhatsApp + Dashboard
- [ ] Fase 3: YouTube + Ads + CRM
- [ ] Fase 4: IA generativa para personalização em massa
