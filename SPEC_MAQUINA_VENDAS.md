# SPEC — Comando `/criar-maquina`: Geração de Máquina de Vendas Deployável

Especifica o processo disparado pelo comando `/criar-maquina <slug>`, que gera um
projeto full-stack completo (Next.js + FastAPI + SQLite) a partir de uma obra
finalizada pela Fábrica Agêntica de Publicações.

## 1. REQUISITOS

| # | Requisito | Validação |
|---|-----------|-----------|
| R1 | Frontend Next.js 14 funcional | `npm run build` sem erros |
| R2 | Backend FastAPI funcional | `uvicorn app.main:app` inicia sem erros |
| R3 | Database SQLite com schema aplicado | `maquina.db` existe com 6 tabelas |
| R4 | Página de venda renderizada | `/` retorna HTML 200 |
| R5 | Página de captura funcional | `/captura` retorna HTML 200, formulário presente |
| R6 | API de leads funcional | `POST /api/leads` retorna 201 |
| R7 | Docker compose funcional | `docker-compose up` sobe todos os serviços |
| R8 | Configs JSON válidos | `python -m json.tool config/*.json` sem erros |
| R9 | AGENTS.md e CLAUDE.md presentes | Arquivos existem e não estão vazios |
| R10 | Manifesto gerado | `manifesto.json` com todos os campos obrigatórios |
| R11 | Rota `/api/checkout` presente e funcional | `POST /api/checkout` retorna 200 e registra o lead no backend (`/api/leads/`) |
| R12 | Copy personalizada por nicho | `grep -rn 'Autor Digital\|centenas de pessoas' frontend/ templates/ README.md` retorna vazio |
| R13 | `.env.example` com `BACKEND_URL` | Rota de checkout lê `BACKEND_URL`/`NEXT_PUBLIC_BACKEND_URL` com fallback `http://127.0.0.1:8000` |

## 2. Sintaxe

```
/criar-maquina <slug> [--tipo completo|parcial|landing|backend]
```

## 3. Tipos de máquina

| Tipo | Componentes | Quando usar |
|------|-------------|-------------|
| `completo` | Frontend + Backend + DB + Scripts + Deploy | Padrão — máquina full-stack |
| `parcial` | Frontend + Backend + DB | Sem scripts de automação |
| `landing` | Apenas Frontend | Landing page + captura sem backend |
| `backend` | Apenas Backend + DB | API pura sem frontend |

## 4. Fluxo

1. Verifica se obra existe em `output/`
2. Pergunta confirmação ao operador
3. Copia template de `templates/maquina/` para `marketing/maquinas/{slug}/`
4. Substitui placeholders ({{SLUG}}, {{TITULO}}, {{PRECO}}, etc.)
5. Gera `manifesto.json` com metadados
6. Copia conteúdo da obra (markdown, PDF, EPUB, artes, capa)
7. Inicializa banco SQLite com schema + seed
8. Gera `.mcp.json` com MCPS necessários
9. Reporta resumo e próximos passos

## 5. Personalização por nicho (pós-geração, obrigatória)

O template nasce com copy genérica de demonstração. Antes de publicar a máquina,
personalizar obrigatoriamente:

| Área | Arquivos | O que trocar |
|------|----------|-------------|
| Configs | `config/produtos.json`, `personas.json`, `funis.json`, `canais.json`, `email.json` | Escada de valor, persona, funis, hashtags e remetente do nicho |
| Frontend | `app/page.tsx`, `components/Hero.tsx`, `PricingCard.tsx`, `app/layout.tsx`, `admin/layout.tsx`, `captura/page.tsx` | Headline, dor/solução, CTA, metadata |
| E-mails | `templates/emails/*.html` | Copy de boas-vindas, nutrição, venda, reativação |
| Docs | `README.md` | Apresentação no nicho |

**Gate de verificação:** `grep -rn 'Autor Digital\|centenas de pessoas' frontend/ templates/ README.md`
retorna vazio (R12).

## 6. Endpoints do frontend

| Rota | Método | Função |
|------|--------|--------|
| `/api/lead` | POST | Captura lead no funil (valida com zod) |
| `/api/checkout` | POST | Registra pedido + lead no backend, devolve link de pagamento (R11) |
| `/api/health` | GET | Health check |
| `/api/webhook` | POST | Webhook de pagamento (stub) |
