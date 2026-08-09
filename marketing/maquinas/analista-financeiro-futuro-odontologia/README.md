# Máquina de Vendas — O Dentista Gestor

Sistema automatizado de captura, nutrição e conversão de leads para o nicho **odontológico**: venda o livro "O Dentista Gestor: Finanças de Clínica com IA" e a escada de valor (checklist gratuito → planilha de fluxo de caixa → livro → programa de mentoria) para dentistas donos de clínica.

Obra de origem: `output/livros/analista-financeiro-futuro-odontologia` (conteúdo copiado em `conteudo/`).

## Início Rápido

```bash
# 1. Clone e configure
cp .env.example .env
# Preencha as variáveis no .env

# 2. Instale dependências
cd backend && pip install -r requirements.txt

# 3. Inicie com Docker
docker-compose up -d

# 4. Verifique status
bash scripts/deploy.sh status
```

## Arquitetura

```
Instagram ──→ Lead Hunter ──→ SQLite ←── Email Sender ──→ SMTP
                                ↑
           Funnel Monitor ←─────┘────→ Auto-Correct (A/B)
                ↓
           metrics.json → Dashboard → Webhooks (Slack/Discord)
```

## Estrutura

```
maquina/
├── config/              # Configurações JSON
│   ├── produtos.json    # Catálogo de produtos
│   ├── funis.json       # Funis de vendas e etapas
│   ├── personas.json    # Personas-alvo com critérios
│   ├── canais.json      # Canais de aquisição
│   ├── email.json       # Configuração SMTP
│   ├── pagamento.json   # Webhooks Hotmart
│   ├── roteamento_modelos.json  # Modelos LLM
│   └── subagentes.json  # Orquestração de agentes
├── scripts/             # Automação Python
│   ├── lead_hunter.py   # Busca leads Instagram
│   ├── email_sender.py  # Sequências automatizadas
│   ├── funnel_monitor.py # Métricas em tempo real
│   ├── auto_correct.py  # Testes A/B automáticos
│   └── deploy.sh        # Deploy e rollback
├── templates/           # Templates de conteúdo
│   ├── emails/          # HTML de e-mails
│   ├── posts/           # Posts para redes sociais
│   └── dm/              # Mensagens diretas
├── backend/             # API FastAPI
├── frontend/            # Dashboard Next.js
└── database/            # SQLite + backups
```

## Comandos

### Lead Hunter
```bash
# Buscar leads por hashtags
python scripts/lead_hunter.py --hashtags marketing digital ebook

# Ver estatísticas
python scripts/lead_hunter.py --stats

# Dry run (sem salvar)
python scripts/lead_hunter.py --hashtags odontologia --dry-run
```

### Email Sender
```bash
# Inscrever leads no funil
python scripts/email_sender.py --funil nutricao-livro --inscrever

# Executar envios pendentes
python scripts/email_sender.py --funil nutricao-livro --executar

# Filtrar por persona
python scripts/email_sender.py --funil nutricao-livro --inscrever --persona dentista-dono-clinica
```

### Funnel Monitor
```bash
# Executar uma vez
python scripts/funnel_monitor.py --once

# Modo daemon (contínuo)
python scripts/funnel_monitor.py --intervalo 120

# Saída JSON
python scripts/funnel_monitor.py --once --json
```

### Auto-Correct
```bash
# Criar experimento A/B
python scripts/auto_correct.py criar \
  --slug test-assunto-dentista-gestor \
  --nome "Teste Assunto E-mail Livro" \
  --variante-a "Sua clínica está no verde?" \
  --variante-b "📚 Parabéns, autor!"

# Registrar eventos
python scripts/auto_correct.py evento --experimento test-assunto-livro --variante A --tipo impressao
python scripts/auto_correct.py evento --experimento test-assunto-livro --variante A --tipo conversao

# Analisar e corrigir
python scripts/auto_correct.py analisar

# Corrigir funil (leads frios)
python scripts/auto_correct.py funil --frios --reativar --dias 7
```

### Deploy
```bash
# Deploy Docker (produção local)
bash scripts/deploy.sh docker

# Deploy completo (Docker + Vercel)
bash scripts/deploy.sh full

# Deploy VPS
VPS_HOST=seu-servidor bash scripts/deploy.sh vps

# Backup do banco
bash scripts/deploy.sh backup

# Status geral
bash scripts/deploy.sh status

# Rollback
bash scripts/deploy.sh rollback v1.0.0
```

## Frontend — Rotas de API

| Rota | Função |
|------|--------|
| `/api/lead` | POST — captura lead no funil |
| `/api/checkout` | POST — registra pedido + lead no backend, devolve link de pagamento (não remover: o `checkout/page.tsx` posta nela) |
| `/api/webhook` | POST — webhook de pagamento (stub) |
| `/api/health` | GET — health check |

> O `/api/checkout` lê `BACKEND_URL`/`NEXT_PUBLIC_BACKEND_URL` (fallback
> `http://127.0.0.1:8000`) e registra o lead em `/api/leads/`. O produto
> default é `dentista-gestor-livro` (slug real em `config/produtos.json`).

## Configuração

### Variáveis de Ambiente

Copie `.env.example` para `.env` e preencha:

| Variável | Obrigatória | Descrição |
|----------|-------------|-----------|
| `INSTAGRAM_ACCESS_TOKEN` | Sim | Token da Graph API |
| `SMTP_USER` | Sim | Usuário SMTP |
| `SMTP_PASSWORD` | Sim | Senha SMTP |
| `FROM_EMAIL` | Sim | E-mail remetente |
| `OPENAI_API_KEY` | Não | Para geração de copy |
| `HOTMART_WEBHOOK_SECRET` | Sim | Validação de pagamentos |

### Personas

Edite `config/personas.json` para definir critérios de busca:
- `bio_keywords` — palavras-chave na bio do Instagram
- `min_seguidores` / `max_seguidores` — faixa de seguidores
- `localizacoes` — cidades/estados alvo

### Funis

Edite `config/funis.json` para configurar sequências:
- `steps` — etapas com template e delay
- `metricas` — metas de abertura/clique/conversão

## Templates

Templates usam sintaxe `{{VARIAVEL}}`:

| Variável | Descrição |
|----------|-----------|
| `{{NOME}}` | Nome do lead |
| `{{USERNAME}}` | Username Instagram |
| `{{PRODUTO_NOME}}` | Nome do produto |
| `{{PRODUTO_PRECO}}` | Preço formatado |
| `{{DESCONTO_CODIGO}}` | Cupom de desconto |
| `{{DESCONTO_PORCENTO}}` | Porcentagem de desconto |
| `{{EMPRESA_NOME}}` | Nome da empresa |
| `{{UNSUBSCRIBE_URL}}` | Link de descadastro |

## Monitoramento

### Métricas Disponíveis

- Total de leads (e novos por período)
- Leads por estágio e persona
- Sequências de e-mail ativas/concluídas
- Taxa de conversão geral
- Score médio dos leads

### Alertas

Configure `webhook_alertas` em `config/funis.json`:
- Leads abaixo do mínimo semanal
- Taxa de conversão abaixo do threshold
- Falhas consecutivas de subagentes

## Segurança

- Tokens ficam em variáveis de ambiente (nunca no código)
- `.env` está no `.gitignore`
- Backup automático do banco de dados
- Rate limits em todas as APIs externas
- Unsubscribe obrigatório (LGPD/CAN-SPAM)
- TLS para SMTP, HTTPS para endpoints

## Stack

- **Backend:** Python 3.11+, FastAPI, SQLite
- **Frontend:** Next.js, React, Tailwind CSS
- **Infra:** Docker Compose, Nginx, Vercel
- **APIs:** Instagram Graph, SMTP, Hotmart, OpenAI

## Licença

Proprietary — Fábrica de Livros
