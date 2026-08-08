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
6. Copia conteúdo da obra (markdown, artes)
7. Inicializa banco SQLite com schema + seed
8. Gera `.mcp.json` com MCPS necessários
9. Reporta resumo e próximos passos
