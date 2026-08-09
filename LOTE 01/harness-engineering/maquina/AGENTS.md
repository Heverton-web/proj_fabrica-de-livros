# AGENTS.md — Máquina de Vendas Agêntica

> Orquestrador central da máquina de vendas automatizada.
> Todos os agentes e subagentes seguem estas regras.

## 0. Princípios

1. **Autonomia total** — após configuração, a máquina roda sem intervenção.
2. **Correção automática** — erros são detectados e corrigidos internamente.
3. **Economia de tokens** — comunicação mínima, resultados máximos.
4. **Fidelidade de dados** — métricas e leads nunca são perdidos.
5. **PT-BR estrito** — toda comunicação e conteúdo em português brasileiro.

## 1. Arquitetura

```
┌─────────────────────────────────────────────────┐
│                   ORQUESTRADOR                   │
│  (subagentes.json → health check → dispatch)     │
├─────────┬──────────┬──────────┬─────────────────┤
│  Lead   │  Email   │ Funnel   │  Auto-Correct   │
│ Hunter  │ Sender   │ Monitor  │   (A/B Tests)   │
├─────────┴──────────┴──────────┴─────────────────┤
│              SQLite (leads.db)                    │
├─────────────────────────────────────────────────┤
│  Config JSON │ Templates │ Nginx │ Docker        │
└─────────────────────────────────────────────────┘
```

## 2. Subagentes

| Agente | Script | Frequência | Função |
|--------|--------|------------|--------|
| Lead Hunter | `scripts/lead_hunter.py` | Diária 08:00 | Busca leads no Instagram |
| Email Sender | `scripts/email_sender.py` | Contínua (15min) | Envia sequências de e-mail |
| Funnel Monitor | `scripts/funnel_monitor.py` | Daemon (5min) | Coleta métricas |
| Auto-Correct | `scripts/auto_correct.py` | Horária | Corrige testes A/B |

## 3. Fluxo de Dados

```
Instagram → lead_hunter.py → leads.db → email_sender.py → SMTP
                                          ↑
funnel_monitor.py → metrics.json ← auto_correct.py
```

## 4. Regras de Execução

- **R1:** Cada subagente tem retry máximo configurado em `config/subagentes.json`.
- **R2:** Falhas consecutivas (>3) disparam alerta via webhook.
- **R3:** Leads inativos >7 dias são marcados como 'frio' automaticamente.
- **R4:** Testes A/B são encerrados quando p-value < 0.05.
- **R5:** E-mails respeitam rate limits configurados em `config/email.json`.
- **R6:** Unsubscribe é obrigatório em todos os e-mails.
- **R7:** Horário de envio respeita fuso America/Sao_Paulo.

## 5. Comandos Disponíveis

```bash
# Lead Hunter
python scripts/lead_hunter.py --hashtags marketing digital --max-per-tag 50
python scripts/lead_hunter.py --stats

# Email Sender
python scripts/email_sender.py --funil nutricao-livro --inscrever
python scripts/email_sender.py --funil nutricao-livro --executar

# Funnel Monitor
python scripts/funnel_monitor.py --once
python scripts/funnel_monitor.py --intervalo 120

# Auto-Correct
python scripts/auto_correct.py criar --slug test-assunto --nome "Teste Assunto" --variante-a "Direto" --variante-b "Com emoji"
python scripts/auto_correct.py analisar
python scripts/auto_correct.py funil --frios --reativar

# Deploy
bash scripts/deploy.sh docker
bash scripts/deploy.sh status
bash scripts/deploy.sh backup
```

## 6. Segurança

- `.env` nunca é commitado.
- Tokens de API ficam em variáveis de ambiente.
- Webhook secrets validam payloads de pagamento.
- Banco de dados tem backup automático via `deploy.sh backup`.
- Rate limits previnem abuso de APIs externas.
