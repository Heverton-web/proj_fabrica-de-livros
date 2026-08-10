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

## Passo 0 — Preparação

1. Crie a pasta de relatórios:
   ```bash
   mkdir -p output/<colecao>/relatorios
   ```
2. Se `$ARGUMENTS` já for um slug com `output/<colecao>/config_obra.json`,
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

### 📄 Relatório do FLUXO 1 — Materiais

Após a conclusão do FLUXO 1, salve o relatório em `output/<colecao>/relatorios/`:

```markdown
# Relatório FLUXO 1 — Materiais — <data>

## Resumo Executivo
- **Status:** ✅ CONCLUÍDO | ⚠️ CONCLUÍDO COM RESSALVAS | ❌ FALHA
- **Duração:** <tempo estimado>

## Itens Criados

| Item | Status | Caminho | Observação |
|------|--------|---------|------------|
| Livro/TCC | ✅/❌ | output/<colecao>/livro_final.pdf | <detalhes> |
| Artigos | ✅/❌ | output/<colecao>/artigos/ | <N> gerados |
| E-books | ✅/❌ | output/<colecao>/ebooks/ | <N> gerados |
| Playbook | ✅/❌ | output/<colecao>/playbooks/ | <N> cards |
| Lead Magnets | ✅/❌ | output/<colecao>/lead-magnets/ | 4 formatos |
| Deck | ✅/❌ | output/<colecao>/decks/ | 16:9 |
| E-mails | ✅/❌ | output/<colecao>/emails/ | 5 sequência |
| Coleção | ✅/❌ | output/<colecao>/colecoes/ | manifesto |

## Itens NÃO Criados (e motivos)

| Item | Motivo | Ação Recomendada |
|------|--------|------------------|
| <item> | <motivo> | <ação> |

## Validações Executadas

| Validação | Resultado |
|-----------|-----------|
| auditar-obra.py | ✅/❌ |
| validar-codigo.py | ✅/❌ |
| validar-referencias.py | ✅/❌ |
| validar-metricas.py | ✅/❌ |

## Pendências
- <lista de pendências ou "nenhuma">
```

Salve como: `output/<colecao>/relatorios/fluxo1-materiais-<AAAA-MM-DD>.md`

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

### 📄 Relatório do FLUXO 2 — Campanhas

Após a conclusão do FLUXO 2, salve o relatório em `output/<colecao>/relatorios/`:

```markdown
# Relatório FLUXO 2 — Campanhas — <data>

## Resumo Executivo
- **Status:** ✅ CONCLUÍDO | ⚠️ FALHA PARCIAL | ❌ FALHA TOTAL
- **Materiais processados:** <N>/<M>

## Itens Criados

| Material | Instagram | LinkedIn | E-mails | WhatsApp | Status |
|----------|-----------|----------|---------|----------|--------|
| <material-1> | ✅ 7 posts + 7 stories | ✅ 7 posts | ✅ 5 e-mails | ✅ 4 msgs | ✅ |
| <material-2> | ✅ 7 posts + 7 stories | ✅ 7 posts | ✅ 5 e-mails | ✅ 4 msgs | ✅ |

## Itens NÃO Criados (e motivos)

| Material | Motivo | Ação Recomendada |
|----------|--------|------------------|
| <material> | <motivo> | <ação> |

## Validações Executadas

| Validação | Resultado |
|-----------|-----------|
| R-CP-1 (Artes suficientes) | ✅/❌ |
| R-CP-2 (Textos completos) | ✅/❌ |
| R-CP-3 (Artes por formato) | ✅/❌ |
| R-CP-4 (Cronogramas completos) | ✅/❌ |
| R-CP-5 (Cronogramas válidos) | ✅/❌ |

## Pendências
- <lista de pendências ou "nenhuma">
```

Salve como: `output/<colecao>/relatorios/fluxo2-campanhas-<AAAA-MM-DD>.md`

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

### 📄 Relatório do FLUXO 3 — Máquina de Vendas

Após a conclusão do FLUXO 3, salve o relatório em `output/<colecao>/relatorios/`:

```markdown
# Relatório FLUXO 3 — Máquina de Vendas — <data>

## Resumo Executivo
- **Status:** ✅ CONCLUÍDO | ⚠️ CONCLUÍDO COM RESSALVAS | ❌ FALHA
- **Caminho:** output/<colecao>/maquina/

## Componentes Criados

| Componente | Status | Detalhes |
|------------|--------|----------|
| Frontend Next.js | ✅/❌ | landing, checkout, admin |
| Backend FastAPI | ✅/❌ | leads, funil, e-mails |
| Banco SQLite | ✅/❌ | schema + seed |
| Automações | ✅/❌ | Lead Hunter, Email Sender, Funnel Monitor, auto_correct |
| Snapshot Campanhas | ✅/❌/⚠️ | <completo/parcial/ausente> |
| Docker Compose | ✅/❌ | pronto para deploy |
| vercel.json | ✅/❌ | deploy Vercel |

## Itens NÃO Criados (e motivos)

| Componente | Motivo | Ação Recomendada |
|------------|--------|------------------|
| <componente> | <motivo> | <ação> |

## Personalização Pendente

| Item | Status | Observação |
|------|--------|------------|
| config/produtos.json | ✅/❌ | <detalhes> |
| config/funis.json | ✅/❌ | <detalhes> |
| config/personas.json | ✅/❌ | <detalhes> |
| config/canais.json | ✅/❌ | <detalhes> |
| frontend/app/page.tsx | ✅/❌ | <detalhes> |
| templates/ | ✅/❌ | <detalhes> |
| .env | ✅/❌ | <detalhes> |

## Validações Executadas

| Validação | Resultado |
|-----------|-----------|
| Checkout (/api/checkout) | ✅/❌ |
| Build frontend (npm run build) | ✅/❌ |

## Pendências
- <lista de pendências ou "nenhuma">
```

Salve como: `output/<colecao>/relatorios/fluxo3-maquina-<AAAA-MM-DD>.md`

## Passo 5 — Distribuição

16. Empacote tudo para distribuição:
    ```bash
    python scripts/empacotar-distribuicao.py <slug>
    ```

## Passo 6 — Relatório Consolidado Final

17. Gere o relatório consolidado em `output/<colecao>/relatorios/`:

```markdown
# Relatório de Produção Completa — <data>

## Resumo Executivo
- **Obra:** <título> (<tipo_obra>, tamanho <P/M/G/GG/XG>)
- **Coleção:** <nome-colecao>
- **Status Geral:** ✅ CONCLUÍDO | ⚠️ CONCLUÍDO COM RESSALVAS | ❌ FALHA

---

## FLUXO 1 — MATERIAIS

| Item | Status | Caminho | Observação |
|------|--------|---------|------------|
| Livro/TCC | ✅/❌ | output/<colecao>/livro_final.pdf | <veredito> |
| Artigos | ✅/❌ | output/<colecao>/artigos/ | <N> gerados |
| E-books | ✅/❌ | output/<colecao>/ebooks/ | <N> gerados |
| Playbook | ✅/❌ | output/<colecao>/playbooks/ | <N> cards |
| Lead Magnets | ✅/❌ | output/<colecao>/lead-magnets/ | 4 formatos |
| Deck | ✅/❌ | output/<colecao>/decks/ | 16:9 |
| E-mails | ✅/❌ | output/<colecao>/emails/ | 5 sequência |
| Coleção | ✅/❌ | output/<colecao>/colecoes/ | manifesto |

**Relatório detalhado:** `fluxo1-materiais-<AAAA-MM-DD>.md`

---

## FLUXO 2 — CAMPANHAS

| Material | Instagram | LinkedIn | E-mails | WhatsApp | Status |
|----------|-----------|----------|---------|----------|--------|
| <mat-1> | ✅ 7+7 | ✅ 7 | ✅ 5 | ✅ 4 | ✅ |
| <mat-2> | ✅ 7+7 | ✅ 7 | ✅ 5 | ✅ 4 | ✅ |

**Status:** ✅ OK | ⚠️ FALHA PARCIAL | ❌ FALHA TOTAL

⚠️ **SE HOUVER FALHA:**
- CAMPANHAS: falha parcial — <N>/<M> materiais criados
- Máquina criada SEM snapshot de campanhas
- Para corrigir: `/campanha-completa <slug-colecao>`

**Relatório detalhado:** `fluxo2-campanhas-<AAAA-MM-DD>.md`

---

## FLUXO 3 — MÁQUINA DE VENDAS

| Componente | Status | Detalhes |
|------------|--------|----------|
| Frontend Next.js | ✅/❌ | landing, checkout, admin |
| Backend FastAPI | ✅/❌ | leads, funil, e-mails |
| Banco SQLite | ✅/❌ | schema + seed |
| Automações | ✅/❌ | 4 subagentes |
| Snapshot Campanhas | ✅/❌/⚠️ | <completo/parcial/ausente> |
| Deploy | ✅/❌ | Docker / Vercel / VPS |

**Relatório detalhado:** `fluxo3-maquina-<AAAA-MM-DD>.md`

---

## DISTRIBUIÇÃO

| Item | Caminho |
|------|---------|
| Pacote | output/<colecao>/distribuicao/ |
| README | output/<colecao>/distribuicao/README.md |
| LICENSE | output/<colecao>/distribuicao/LICENSE |

---

## PENDÊNCIAS

| # | Pendência | Fluxo | Prioridade |
|---|-----------|-------|------------|
| 1 | <pendência> | <fluxo> | <alta/média/baixa> |

---

## ARQUIVOS GERADOS

| Arquivo | Descrição |
|---------|-----------|
| `relatorios/fluxo1-materiais-<data>.md` | Relatório detalhado do Fluxo 1 |
| `relatorios/fluxo2-campanhas-<data>.md` | Relatório detalhado do Fluxo 2 |
| `relatorios/fluxo3-maquina-<data>.md` | Relatório detalhado do Fluxo 3 |
| `relatorios/relatorio-completo-<data>.md` | Este relatório consolidado |
```

18. **Salve os relatórios:**
    ```bash
    # Relatório consolidado (este arquivo)
    # Salve como: output/<colecao>/relatorios/relatorio-completo-<AAAA-MM-DD>.md

    # Gere o PDF do relatório consolidado
    python scripts/gerar-relatorio-sessao.py output/<colecao>/relatorios/relatorio-completo-<AAAA-MM-DD>.md
    ```

> **IMPORTANTE:** Cada relatório é salvo em `output/<colecao>/relatorios/`
> e pode ser consultado individualmente. O relatório consolidado referencia
> os 3 relatórios de fluxo para detalhes completos.

## Notas de Economia de Tokens

- A Fase 1 (pesquisa) roda **uma única vez**, no `/esbocar`.
- Cada lote respeita máximo de 4 subagentes simultâneos.
- Campanhas e Máquina são **determinísticas** (~0 LLM) — custo baixo.
- Se o operador só quer materiais, use `/criar-livro` (não este comando).
