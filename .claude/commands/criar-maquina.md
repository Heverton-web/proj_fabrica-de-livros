# Comando: /criar-maquina

Gera uma máquina de vendas deployável a partir de uma obra finalizada.

## Sintaxe

```
/criar-maquina <slug-da-obra> [--tipo completo|parcial|landing|backend]
```

## Fluxo

1. Verifica se a obra existe em `output/`
2. Exibe resumo da obra e pergunta confirmação
3. Executa `python scripts/criar-maquina-vendas.py <slug> --tipo <tipo>`
4. Gera projeto full-stack em `marketing/maquinas/{slug}/`
5. Reporta estrutura gerada e próximos passos

## Exemplos

```
/criar-maquina observabilidade-sistemas-distribuidos
/criar-maquina inteligencia-artificial-empreendedores --tipo landing
/criar-maquina marketing-digital-avancado --tipo completo
```

## Saída

Projeto completo em `marketing/maquinas/{slug}/` com:
- Frontend Next.js (páginas de venda, captura, admin)
- Backend FastAPI (APIs de leads, e-mails, métricas)
- Database SQLite (schema + dados de exemplo)
- Scripts de automação (lead hunter, e-mail sender, monitor)
- Configs (produtos, funis, personas, roteamento LLM)
- Deploy (docker-compose.yml, vercel.json)
- Docs (AGENTS.md, CLAUDE.md, SPEC.md, README.md)

## Após criação

```
cd marketing/maquinas/{slug}
cat README.md           # Ler manual de deploy
cat config/produtos.json # Revisar escada de valor
bash scripts/deploy.sh  # Fazer deploy
```
