---
description: Fluxo FULL (V5.3) da Fábrica Agêntica de Publicações — executa os 3 fluxos de forma AUTÔNOMA e COMPLETA: MATERIAIS → CAMPANHAS → MÁQUINA DE VENDAS. Ponto de entrada único para produção completa.
---

Você é o Orquestrador Mestre. O operador disparou `/produzir-obra-completa` com o
tema (ou slug já esboçado) em `$ARGUMENTS`.

## Visão Geral dos 3 Fluxos

```
┌─────────────────────────────────────────────────────────────┐
│  FLUXO 1: MATERIAIS (Fases 0-4)                             │
│  /esbocar → /criar-livro → derivados → coleção              │
└───────────────────────────────┬─────────────────────────────┘
                                │
                                ▼ OBRIGATÓRIO
┌─────────────────────────────────────────────────────────────┐
│  FLUXO 2: CAMPANHAS (V5.3)                                  │
│  /campanha-completa → artes, textos, cronogramas             │
└───────────────────────────────┬─────────────────────────────┘
                                │
                                ▼ OBRIGATÓRIO
┌─────────────────────────────────────────────────────────────┐
│  FLUXO 3: MÁQUINA DE VENDAS (full-stack)                    │
│  /criar-maquina → Next.js + FastAPI + SQLite                │
└─────────────────────────────────────────────────────────────┘
```

## Passo 0 — Esboço (Fase 0)

1. Se `$ARGUMENTS` já for um slug com `output/<colecao>/config_obra.json`,
   pule para o Passo 1. Caso contrário, execute `/esbocar $ARGUMENTS`
   (elicitação + pesquisa + arquitetura + fatiamento).

## Passo 1 — Obra Principal (FLUXO 1: MATERIAIS)

2. Se `tipo_obra == "livro"`: execute `/criar-livro <slug>`.
3. Se `tipo_obra == "tcc"`: execute `/criar-tcc <slug>`.
4. Ao final: `output/<colecao>/livro_final.pdf` + veredito da auditoria.

## Passo 2 — Derivados em Paralelo (FLUXO 1: MATERIAIS)

```
                        [Livro/TCC compilado — Passo 1]
                                    │
    ┌──────────────┬────────────────┼────────────────┬──────────────┐
    ▼ COMPRESSÃO   ▼ COMPRESSÃO     ▼ EXTRAÇÃO       ▼ EXTRAÇÃO     ▼ EXTRAÇÃO
 /criar-artigo  /criar-ebook   /criar-playbook   /criar-deck   /criar-emails
 (RAG dossiê)  (reescrita tom)  (§4+§5, 0 token)  (0 token)     (esqueleto)
                                       │
                                       ▼ EXTRAÇÃO
                              /criar-lead-magnet --todos
```

5. Se `gerar_artigos=true`: `/criar-artigo <slug>`.
6. Se `gerar_ebooks=true`: `/criar-ebook <slug>` (paralelo ao 5).
7. Se `gerar_playbook=true`: `/criar-playbook <slug>` (ANTES dos LMs).
8. Se `gerar_lead_magnets=true`: `/criar-lead-magnet <slug> --todos`.
   Se `gerar_deck=true`: `/criar-deck <slug>`.
   Se `gerar_emails=true`: `/criar-emails <slug>`.
9. **(V5)** Sincronize a coleção:
   ```bash
   python scripts/colecao.py --sincronizar --slug <prefixo>/<slug>
   ```

## Passo 3 — Campanhas (FLUXO 2: CAMPANHAS) ← OBRIGATÓRIO

10. Depois que TODOS os materiais estiverem prontos (Passos 1-2), gere as
    campanhas de divulgação para CADA material da coleção:

    ```bash
    python scripts/criar-campanha.py --completo <slug-colecao>
    ```

    Isso cria automaticamente:
    - Artes PNG para Instagram (feed-story + post) e LinkedIn
    - Textos para copy (posts, e-mails, WhatsApp)
    - Cronogramas de divulgação (14-30 dias por material)
    - Moldes editáveis (HTML)

11. Valide as campanhas:
    ```bash
    python scripts/validar-campanha.py --completo <slug-colecao> --estrito
    ```

12. **(Opcional)** Se quiser personalizar a copy, reescreva os moldes
    em `output/<colecao>/campanhas/<material>/textos/` e marque como completa:
    ```bash
    python scripts/criar-campanha.py --material <slug-material> --marcar-completa
    ```

> **REGRA 12:** Copy genérica ("Autor Digital", "centenas de pessoas") é REPROVADA.
> O gate `grep 'Autor Digital|centenas de pessoas'` deve retornar vazio.

### ⚠️ Tratamento de Erros nas Campanhas (OPÇÃO C — Warning + Continua)

**Comportamento:** Se as campanhas falharem, a máquina de vendas CONTINUA
será gerada, mas com um **WARNING explícito** no relatório final.

**Por quê essa opção?**
1. Máquina PODE funcionar sem campanhas (código já suporta `return None`)
2. Campanhas são **marketing**, não funcionalidade core da máquina
3. Bloquear por falha de marketing é **excessivo**
4. Warning permite que o usuário **decida** se quer corrigir depois

**O que acontece em cada cenário:**

| Cenário | Campanha | Máquina | Snapshot | Relatório |
|---------|----------|---------|----------|-----------|
| Tudo OK | ✅ Criadas | ✅ Criada | ✅ Completo | ✅ Limpo |
| Falha parcial | ⚠️ Algumas | ✅ Criada | ⚠️ Parcial | ⚠️ Warning |
| Falha total | ❌ Nenhuma | ✅ Criada | ❌ Vazio | ⚠️ Warning |

**Se houver falha, o relatório final (Passo 6) exibirá:**
```
⚠️ CAMPANHAS: falha parcial — <N>/<M> materiais criados
   Máquina criada SEM snapshot de campanhas
   Para corrigir: /campanha-completa <slug-colecao>
```

## Passo 4 — Máquina de Vendas (FLUXO 3: MÁQUINA) ← OBRIGATÓRIO

13. Depois que a coleção estiver pronta (Passos 1-2), gere a máquina de
    vendas full-stack:

    ```bash
    python scripts/criar-maquina-vendas.py <slug-colecao>
    ```

    Isso cria em `output/<slug-colecao>/maquina/`:
    - Frontend Next.js 14 (landing, checkout, admin)
    - Backend FastAPI (APIs de leads, funil, e-mails)
    - Banco SQLite (leads, vendas, campanhas)
    - 4 automações (Lead Hunter, Email Sender, Funnel Monitor, auto_correct)
    - **Snapshot das campanhas** (SE existirem — ver tratamento de erros)
    - Docker Compose + vercel.json

14. **Personalização OBRIGATÓRIA (Regra 12):**
    - `config/produtos.json` — produto real, preço
    - `config/funis.json` — oferta, desconto, steps
    - `config/personas.json` — persona do nicho
    - `config/canais.json` — hashtags/localizações
    - `frontend/app/page.tsx` — headline do nicho
    - `templates/` — copy dos e-mails
    - `.env` — credenciais reais

15. Valide o checkout:
    ```bash
    cd output/<slug-colecao>/maquina/frontend && npm run dev
    # POST http://localhost:3000/api/checkout {"nome": "...", "email": "..."}
    ```

### ⚠️ Snapshot de Campanhas (Comportamento Tolerante)

A máquina **SEMPRE será criada**, mesmo sem campanhas. O script
`criar-maquina-vendas.py` tem esta lógica:

```python
def vincular_campanhas(destino, slug):
    if not origem.is_dir():
        print("(sem campanhas no hub — máquina sem snapshot)")
        return None  # ← MÁQUINA CONTINUA
    # ... copia campanhas se existirem
```

**Resultado:** Máquina funciona com ou sem campanhas. Se as campanhas
falharem, o snapshot fica vazio mas a máquina continua operacional.

## Passo 5 — Distribuição

16. Empacote tudo para distribuição:
    ```bash
    python scripts/empacotar-distribuicao.py <slug>
    ```

## Passo 6 — Relatório Consolidado Final

17. Exiba relatório completo dos 3 fluxos:

```
═══════════════════════════════════════════════════════════════
RELATÓRIO DE PRODUÇÃO COMPLETA — <data>
═══════════════════════════════════════════════════════════════

FLUXO 1 — MATERIAIS:
  Livro/TCC   : output/<colecao>/livro_final.pdf — <veredito>
  Artigos     : <N> gerado(s) — output/<colecao>/artigos/
  E-books     : <N> gerado(s) — output/<colecao>/ebooks/
  Playbook    : output/<colecao>/playbooks/
  Lead Magnets: output/<colecao>/lead-magnets/ (4 formatos)
  Deck        : output/<colecao>/decks/
  E-mails     : output/<colecao>/emails/ (5 sequência)
  Coleção     : output/<colecao>/colecoes/<nome>.json

FLUXO 2 — CAMPANHAS:
  Materiais   : <N> campanhas geradas
  Instagram   : <N> posts + <N> stories
  LinkedIn    : <N> posts
  E-mails     : <N> sequências de nutrição
  WhatsApp    : <N> mensagens
  Status      : <ok | parcial | falha>

  ⚠️ SE HOUVER FALHA:
  "CAMPANHAS: falha parcial — <N>/<M> materiais criados"
  "Máquina criada SEM snapshot de campanhas"
  "Para corrigir: /campanha-completa <slug-colecao>"

FLUXO 3 — MÁQUINA DE VENDAS:
  Frontend    : Next.js 14 (landing, checkout, admin)
  Backend     : FastAPI (leads, funil, e-mails)
  Banco       : SQLite
  Deploy      : Docker / Vercel / VPS
  Snapshot    : <completo | parcial | ausente>
  Status      : <pronta-pendente>

DISTRIBUIÇÃO:
  Pacote      : output/<colecao>/distribuicao/
  Arquivos    : <N> PDFs, <N> EPUBs, <N> PNGs

PENDÊNCIAS   : <lista objetiva, ou "nenhuma">
═══════════════════════════════════════════════════════════════
```

## Notas de Economia de Tokens

- A Fase 1 (pesquisa) roda **uma única vez**, no `/esbocar`.
- Cada lote respeita máximo de 4 subagentes simultâneos.
- Campanhas e Máquina são **determinísticas** (~0 LLM) — custo baixo.
- Se o operador só quer materiais, use `/criar-livro` (não este comando).
