# CLAUDE.md — Regras do Agente para Máquina de Vendas

> Este arquivo define as regras que qualquer agente IA deve seguir ao
> trabalhar neste projeto. Hardlink de AGENTS.md.

## Regras Globais

1. **Idioma:** PT-BR estrito em toda comunicação, código-comentários e artefatos.
2. **Autonomia:** após configuração inicial, a máquina roda 100% autônoma.
3. **Correção:** desvios são corrigidos internamente antes de notificar o operador.
4. **Segurança:** nunca exponha tokens, senhas ou dados sensíveis em logs ou outputs.
5. **Fidelidade:** dados de leads e métricas são intocáveis — nunca delete sem confirmação.

## Estrutura do Projeto

```
maquina/
├── AGENTS.md              # Este orquestrador
├── CLAUDE.md              # Regras do agente
├── SPEC.md                # Especificação completa
├── README.md              # Documentação
├── docker-compose.yml     # Infraestrutura
├── vercel.json            # Deploy frontend
├── .env.example           # Template de variáveis
├── config/                # Configurações JSON
│   ├── produtos.json      # Catálogo de produtos
│   ├── funis.json         # Funis de vendas
│   ├── personas.json      # Personas-alvo
│   ├── canais.json        # Canais de aquisição
│   ├── email.json         # Configuração SMTP
│   ├── pagamento.json     # Webhooks de pagamento
│   ├── roteamento_modelos.json  # Modelos LLM
│   └── subagentes.json    # Configuração de agentes
├── scripts/               # Scripts Python
│   ├── lead_hunter.py     # Busca de leads
│   ├── email_sender.py    # Envio de e-mails
│   ├── funnel_monitor.py  # Métricas
│   ├── auto_correct.py    # Testes A/B
│   └── deploy.sh          # Deploy script
├── templates/             # Templates de conteúdo
│   ├── emails/            # Templates de e-mail
│   ├── posts/             # Templates de posts
│   └── dm/                # Templates de DM
├── backend/               # API FastAPI
├── frontend/              # Dashboard React/Next.js
└── database/              # SQLite + backups
```

## Convenções de Código

- Python 3.11+ com type hints.
- JSON para configuração, nunca YAML.
- SQLite para persistência local (leads, métricas, experimentos).
- Templates usam sintaxe `{{VARIAVEL}}`.
- Logs seguem formato: `%(asctime)s [%(levelname)s] %(name)s: %(message)s`.

## O que NÃO fazer

- NUNCA commitar `.env` ou credenciais.
- NUNCA deletar leads do banco sem confirmação do operador.
- NUNCA enviar e-mails fora do horário configurado.
- NUNCA exceder rate limits das APIs externas.
- NUNCA alterar templates de e-mail sem revisão.
