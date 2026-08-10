# Melhoria — Correção de Materiais Pendentes

**Data:** 2026-08-10
**Status:** PENDENTE
**Prioridade:** ALTA

---

## Problemas Identificados

### 1. DECK: PDF não gerado a partir do HTML
- **Situação**: HTML existe (`dck-1-harness-engineering-modelo.html`), mas PDF não foi gerado automaticamente
- **Causa**: Script `gerar-deck-html.py` gera HTML mas não gera PDF automaticamente
- **Solução**: Adicionar geração de PDF após HTML

### 2. DISTRIBUIÇÃO: Materiais não organizados
- **Situação**: Pacote de distribuição não contém todos os materiais organizados
- **Causa**: Script `empacotar-distribuicao.py` não copia todos os tipos
- **Solução**: Atualizar script para copiar livros, artigos, ebooks, lead magnets, decks, playbooks

### 3. EBOOKS: Nomenclatura longa demais
- **Situação**: Nomes como `harness--eb-01-a-revolucao-dos-agentes-por-que-o-modelo`
- **Causa**: Script de geração usa slug completo
- **Solução**: Usar nomenclatura comercial atrativa (max 30 chars)

### 4. EBOOKS/LEAD MAGNETS: Padrão ABNT em vez de comercial
- **Situação**: Títulos seguem padrão acadêmico
- **Causa**: Metadados herdados do livro-mãe
- **Solução**: Gerar títulos comerciais para materiais derivados

### 5. PLAYBOOK: Capa não gerada (VERIFICADO: OK)
- **Situação**: A capa foi gerada ✅ (815 KB)
- **Nota**: Não há problema neste item

---

## PLANO DE AÇÃO

### Fase 1: Corrigir nomenclatura de materiais derivados

| # | Ação | Script |
|---|------|--------|
| 1.1 | Criar script de renomeação de e-books | `scripts/renomear-ebooks.py` |
| 1.2 | Renomear e-books para padrão comercial | Execução manual |
| 1.3 | Atualizar referências em `derivados.json` | Script automático |

**Padrão de nomenclatura comercial:**
```
ANTES:  harness--eb-01-a-revolucao-dos-agentes-por-que-o-modelo
DEPOIS: eb-01-coding-agents
```

### Fase 2: Gerar PDF para decks

| # | Ação | Script |
|---|------|--------|
| 2.1 | Atualizar `gerar-deck-html.py` para gerar PDF | Script modificado |
| 2.2 | Regenerar decks com PDF | `python scripts/gerar-deck-html.py --todos` |
| 2.3 | Verificar geração de PDF | Listagem |

### Fase 3: Corrigir distribuição

| # | Ação | Script |
|---|------|--------|
| 3.1 | Atualizar `empacotar-distribuicao.py` | Script modificado |
| 3.2 | Adicionar cópia de artigos, ebooks, decks | Função atualizada |
| 3.3 | Re-empacotar coleção | `python scripts/empacotar-distribuicao.py oh-my` |
| 3.4 | Verificar organização | Listagem |

### Fase 4: Títulos comerciais para derivados

| # | Ação | Script |
|---|------|--------|
| 4.1 | Criar função de geração de títulos comerciais | `scripts/titulos_comerciais.py` |
| 4.2 | Atualizar `ebook_metadados.json` dos e-books | Script automático |
| 4.3 | Atualizar `ebook_metadados.json` dos lead magnets | Script automático |
| 4.4 | Regenerar capas com novos títulos | `python scripts/gerar-capa.py --todos` |

### Fase 5: Validar identidade visual

| # | Ação | Verificação |
|---|------|-------------|
| 5.1 | Verificar cores por coleção | `output/series.json` |
| 5.2 | Verificar badges | `validar-capa-nivel.py` |
| 5.3 | Verificar títulos | `validar-capa-texto.py` |

---

## Estimativa de Esforço

| Fase | Esforço |
|------|---------|
| Fase 1 | ~1h |
| Fase 2 | ~1h |
| Fase 3 | ~1h |
| Fase 4 | ~1h |
| Fase 5 | ~30min |
| **Total** | **~4h30** |

---

## Nomenclatura Comercial Proposta

### E-books (antes → depois)

| Antes | Depois |
|-------|--------|
| `harness--eb-01-a-revolucao-dos-agentes-por-que-o-modelo` | `eb-01-coding-agents` |
| `harness--eb-02-test-harness-a-heranca-da-engenharia-de` | `eb-02-test-harness` |
| `harness--eb-03-o-ciclo-react-e-os-loops-de-execucao-san` | `eb-03-ciclo-react` |
| `harness--eb-04-gestao-de-contexto-combatendo-o-context` | `eb-04-contexto` |

### Lead Magnets (já ok)
- `lm-1-armadilhas` ✅
- `lm-2-cheatsheet` ✅
- `lm-3-checklist` ✅
- `lm-4-entregas` ✅
- `lm-5-mapa` ✅
- `lm-6-mini-guia` ✅

### Playbooks (já ok)
- `pbk-1-harness-modelo` ✅

### Decks (precisa de PDF)
- `dck-1-harness-modelo` → gerar PDF a partir do HTML

---

## Identidade Visual por Coleção

Cada coleção tem sua `cor_accent` definida em `output/series.json`:

```json
{
  "harness": {
    "cor": "#a855f7",  // roxo
    "membros": [...]
  },
  "oh-my": {
    "cor": "#58a6ff",  // azul
    "membros": [...]
  }
}
```

**Aplicação da cor:**
- Barras de accent (top/bottom/left)
- Badge principal
- Título gradiente (line2)
- Dots do divisor
- Mini-stats no rodapé
- Fundo decorativo (grid, glow, código)

---

## Riscos

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| Renomeação quebra referências | Alto | Atualizar `derivados.json` |
| PDF de deck falha | Médio | Testar com 1 deck antes |
| Títulos comerciais inconsistentes | Baixo | Usar templates predefinidos |
