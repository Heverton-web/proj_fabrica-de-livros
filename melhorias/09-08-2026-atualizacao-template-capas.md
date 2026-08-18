# Melhoria — Atualização do Template de Capas

**Data:** 2026-08-09
**Status:** PENDENTE
**Prioridade:** ALTA

---

## Problema

O script `gerar-capa.py` está gerando capas com template antigo (1200x1600, fundo flat, 1 badge)
enquanto existe um modelo refinado (1600x2263, fundo com camadas, 3 badges, stats).

## Modelo de Referência

Arquivo: `LOTE 01/ai-driven-development-do-zero-ao-deploy-v2/livros/.../capa-refinada.html`

---

## Plano de Ação

### Fase 1: Criar template externo (desacoplado do script)

| # | Ação | Arquivo | Prioridade |
|---|------|---------|------------|
| 1.1 | Criar `templates/capa-livro.html` com o novo design | `templates/capa-livro.html` | CRÍTICO |
| 1.2 | Criar `templates/capa-ebook.html` (variante para e-books) | `templates/capa-ebook.html` | ALTO |
| 1.3 | Criar `templates/capa-social.html` (card 1080x1350) | `templates/capa-social.html` | MÉDIO |

### Fase 2: Atualizar script `gerar-capa.py`

| # | Ação | O que muda |
|---|------|------------|
| 2.1 | Ler template externo em vez de HTML inline | `_gerar_html()` → `ler_template()` |
| 2.2 | Atualizar dimensões para 1600x2263 | `DIMENSOES` no registro `tipos_obra.py` |
| 2.3 | Injetar variáveis no template (titulo, cor, stats, etc.) | `string.Template` ou `jinja2` |
| 2.4 | Corrigir prioridade de metadados (sumário > ebook para livros) | Linha 210-211 |
| 2.5 | Adicionar parâmetros dinâmicos: categoria, stats, edition-tag | Novos parâmetros em `gerar_capa()` |

### Fase 3: Atualizar registro de tipos

| # | Ação | Arquivo |
|---|------|---------|
| 3.1 | Atualizar `dimensoes_capa()` para 1600x2263 | `scripts/tipos_obra.py` |
| 3.2 | Adicionar dimensões social (1080x1350) | `scripts/tipos_obra.py` |

### Fase 4: Gerar novas capas

| # | Ação | Comando |
|---|------|---------|
| 4.1 | Regenerar capas da coleção "oh-my" | `python scripts/gerar-capa.py --todos` |
| 4.2 | Validar capas | `scripts/validar-capa-nivel.py` |
| 4.3 | Testar abertura dos PNGs | Abrir em visualizador |

### Fase 5: Atualizar documentação

| # | Ação | Arquivo |
|---|------|---------|
| 5.1 | Documentar novo template no manual | `docs/manual-completo-fabrica.md` |
| 5.2 | Atualizar spec de design | `docs/referencia-capa-design.md` |

---

## Estimativa de Esforço

| Fase | Esforço |
|------|---------|
| Fase 1 | ~2h |
| Fase 2 | ~3h |
| Fase 3 | ~30min |
| Fase 4 | ~1h |
| Fase 5 | ~30min |
| **Total** | **~6h** |

---

## Especificação do Template Novo

### Dimensões
- Canvas: 1600 × 2263 px (A4 vertical 1:1,414)
- Fundo: `#07090f`

### Sistema de Cores
- Accent primary: `#a855f7` (roxo)
- Accent secondary: `#6366f1` (indigo)
- Accent tertiary: `#ec4899` (pink)
- Text primary: `#f0f6fc` (branco suave)
- Text secondary: `#c9d1d9` (cinza claro)

### Fontes
- Display: Inter (300/400/600/700/900)
- Mono: JetBrains Mono (400/700)

### Estrutura
1. Barras de accent (top 6px, bottom 4px, left 3px)
2. Fundo com 4 camadas (grid, glow-top, glow-bottom, bg-code)
3. Header (logo, nome, tagline, edition-tag)
4. Corpo (ilustração, categoria, título 3 linhas, subtítulo, badges, divisor)
5. Rodapé (autor, mini-stats)
