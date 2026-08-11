---
description: Gera uma máquina de vendas deployável (Next.js + FastAPI) a partir de uma obra finalizada da Fábrica — 1 máquina por COLEÇÃO, com snapshot das campanhas e personalização obrigatória por nicho. Uso: /criar-maquina <slug-da-obra> [--tipo completo|parcial|landing|backend]
---

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
4. Gera projeto full-stack em `output/<slug-colecao>/maquina/`
   (**regra 1:1 — 1 máquina por COLEÇÃO**; o hub é derivado do slug da obra)
5. Copia as campanhas da coleção para `maquina/campanhas/` (snapshot)
6. **Personaliza por nicho** (ver seção abaixo)
7. Reporta estrutura gerada e próximos passos

## Personalização por nicho (OBRIGATÓRIA após gerar)

O template nasce com **copy genérica** ("Autor Digital", "centenas de pessoas").
Antes de publicar, substitua em todos os pontos abaixo pelos termos do nicho da obra:

### 1. Configs de negócio (`config/*.json`)
- `produtos.json` — escada de valor real do nicho (lead magnet → tripwire → core)
- `personas.json` — perfil real do comprador (dor, desejo, canais, tom)
- `funis.json` — nomes/assuntos dos funis do nicho
- `canais.json` — hashtags do nicho
- `email.json` — remetente e assinatura reais

### 2. Copy do frontend (`frontend/app/` e `components/`)
- `app/page.tsx` — home (dor/solução/CTA)
- `components/Hero.tsx` — headline e sub-headline
- `components/PricingCard.tsx` — produto e benefícios
- `app/layout.tsx` — metadata/OG
- `app/admin/layout.tsx` — título do admin
- `app/captura/page.tsx` — título e CTA da captura

### 3. E-mails e docs
- `templates/emails/*.html` — copy de boas-vindas/nutrição/venda/reativação
- `README.md` — apresentação da máquina no nicho

### 4. Verificação obrigatória
- `grep -rn 'Autor Digital\|centenas de pessoas' frontend/app frontend/components templates/ campanhas/ README.md` deve retornar **vazio**
- Testar `POST /api/checkout` (rota já nasce no template — não remover)

## Exemplos

```
/criar-maquina observabilidade-sistemas-distribuidos
/criar-maquina inteligencia-artificial-empreendedores --tipo landing
/criar-maquina marketing-digital-avancado --tipo completo
```

## Saída

Projeto completo em `output/<slug-colecao>/maquina/` com:
- Frontend Next.js (páginas de venda, captura, checkout, admin + API routes `/api/lead` e `/api/checkout`)
- Backend FastAPI (APIs de leads, e-mails, métricas)
- Database SQLite (schema + dados de exemplo)
- Scripts de automação (lead hunter, e-mail sender, monitor)
- Configs (produtos, funis, personas, roteamento LLM)
- **`campanhas/`** — snapshot dos artefatos de campanha da coleção (textos, artes, cronogramas)
- Deploy (docker-compose.yml, vercel.json)
- Docs (AGENTS.md, CLAUDE.md, SPEC.md, README.md)

## Após criação

```
cd output/<slug-colecao>/maquina
cat README.md           # Ler manual de deploy
cat config/produtos.json # Revisar escada de valor
cat campanhas/snapshot.json  # Vínculo com as campanhas da coleção
# Personalizar copy (seção acima) antes de publicar
bash scripts/deploy.sh  # Fazer deploy
```
