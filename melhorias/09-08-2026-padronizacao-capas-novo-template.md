# Melhoria — Padronização de Capas com Novo Template

**Data:** 2026-08-09
**Status:** PENDENTE
**Prioridade:** ALTA
**Referência:** `LOTE 01/ai-driven-development-do-zero-ao-deploy-v2/livros/.../capa-refinada.html`

---

## Premissas

1. **MANTER** as dimensões originais de cada tipo de material (tipos_obra.py)
2. **PADRONIZAR** todas as capas para seguir o novo template (capa-refinada.html)
3. **RESPEITAR** a identidade de cada coleção (cores de accent via series.json)

---

## Análise do Template Atual vs Novo

| Aspecto | Template Atual (`gerar-capa.py`) | Novo Template (`capa-refinada.html`) |
|---------|----------------------------------|-------------------------------------|
| **Fundo** | `#0d1117` (flat) | `#07090f` + 4 camadas decorativas |
| **Fontes** | Inter, Arial | Inter (300-900) + **JetBrains Mono** |
| **Barras accent** | Top + Bottom | Top (6px) + Bottom (4px) + **Left (3px)** |
| **Header** | Logo + nome | Logo + nome + **tagline** + **edition-tag** |
| **Título** | 72px, 1 linha | **96px, 3 linhas** (branco/gradiente/branco) |
| **Badges** | 1 badge | **3 badges** (main + 2 secondary) |
| **Divisor** | Linha simples | Linha + **3 dots** em escala decrescente |
| **Rodapé** | Nome + cargo | Nome + cargo + **mini-stats** (3 colunas) |
| **Ilustração** | Sem efeito | **Halo + drop-shadow glow** |
| **Código decorativo** | Não existe | **Opacity 3.5%** no fundo |
| **Categoria** | Não existe | **Label mono** antes do título |

---

## Dimensões por Tipo (MANTIDAS)

| Tipo | Dimensões | Arquivo |
|------|-----------|---------|
| livro | 1600 × 2263 | `tipos_obra.py:76` |
| tcc | 1600 × 2263 | `tipos_obra.py:112` |
| ebook | 1200 × 1600 | `tipos_obra.py:161` |
| playbook | 1600 × 2263 | `tipos_obra.py:187` |
| lead-magnet | 2480 × 3508 | `tipos_obra.py:209` |
| lead-magnet social | 1080 × 1350 | `tipos_obra.py:210` |
| deck | 1920 × 1080 | `tipos_obra.py:238` |

---

## Identidade por Coleção (MANTIDA)

Cada coleção tem sua `cor_accent` definida em `output/series.json`:

```json
{
  "oh-my": {
    "cor": "#58a6ff",
    "membros": ["oh-my/livros/oh-my", ...]
  },
  "harness": {
    "cor": "#a855f7",
    "membros": ["harness/livros/harness", ...]
  }
}
```

A cor é resolvida por `series_capa.py:resolver_cor()` e aplicada em:
- Barras de accent (top/bottom/left)
- Badge principal
- Título gradiente (line2)
- Dots do divisor
- Mini-stats no rodapé

---

## PLANO DE AÇÃO

### Fase 1: Criar template HTML externo

| # | Ação | Arquivo | Descrição |
|---|------|---------|-----------|
| 1.1 | Criar `templates/capa-refinada.html` | `templates/` | Template base com placeholders `{{VARIAVEL}}` |
| 1.2 | Definir variáveis do template | — | titulo, subtitulo, cor, badge, stats, categoria, edition-tag |
| 1.3 | Testar renderização manual | — | Abrir HTML no browser, verificar layout |

**Variáveis do template:**
```
{{TITULO_LINHA1}}    — primeira linha do título (branco)
{{TITULO_LINHA2}}    — segunda linha (gradiente cor)
{{TITULO_LINHA3}}    — terceira linha (branco menor)
{{SUBTITULO}}        — subtítulo com <strong>
{{CATEGORIA}}        — label mono antes do título
{{COR}}              — cor de accent da coleção
{{BADGE_PRINCIPAL}}  — badge sólido (ex: "Para Iniciantes")
{{BADGE_SECUNDARIO1}} — badge borda (ex: "16 capítulos")
{{BADGE_SECUNDARIO2}} — badge borda (ex: "projetos práticos")
{{STAT1_NUMERO}}     — número do stat 1
{{STAT1_LABEL}}      — label do stat 1
{{STAT2_NUMERO}}     — número do stat 2
{{STAT2_LABEL}}      — label do stat 2
{{STAT3_NUMERO}}     — número do stat 3
{{STAT3_LABEL}}      — label do stat 3
{{AUTOR}}            — nome do autor
{{QUALIFICACAO}}     — cargo/qualificação
{{EDITION_TAG}}      — tag de versão (ex: "v2.0 · 2025")
{{ILUSTRCACAO}}      — caminho da ilustração (opcional)
{{LARGURA}}          — largura em px
{{ALTURA}}           — altura em px
```

### Fase 2: Atualizar script `gerar-capa.py`

| # | Ação | O que muda | Linhas |
|---|------|------------|--------|
| 2.1 | **Ler template externo** | Substituir `_gerar_html()` por leitura de `templates/capa-refinada.html` | 66-139 |
| 2.2 | **Corrigir prioridade de metadados** | Para livros: sumário > ebook_metadados | 210-211 |
| 2.3 | **Injetar variáveis dinâmicas** | Calcular stats (capítulos, páginas) a partir de `sumario_macro.json` | Nova função |
| 2.4 | **Adicionar parâmetro `categoria`** | Derivar de `sumario_macro.json.motivo_condutor` ou config | Nova função |
| 2.5 | **Adicionar parâmetro `edition_tag`** | Versão + ano atual | Nova função |
| 2.6 | **Manter dimensões por tipo** | Usar `TO.dimensoes_capa(tipo)` (já implementado) | 147-149 |

**Código simplificado da mudança:**

```python
def gerar_capa(titulo, subtitulo, dir_saida, tipo="livro", cor_acento="#58a6ff",
               autor=AUTOR_PADRAO, qualificacao=QUALIFICACAO_PADRAO,
               badge_texto=None, ilustracao_relpath=None, variante=None,
               nome_arquivo=None, categoria=None, stats=None, edition_tag=None):
    
    # Ler template externo
    template_path = DIR_PROJETO / "templates" / "capa-refinada.html"
    template_html = template_path.read_text(encoding="utf-8")
    
    # Calcular stats se não fornecidos
    if stats is None:
        stats = calcular_stats(dir_saida)
    
    # Substituir variáveis
    html = template_html.replace("{{TITULO_LINHA1}}", titulo_linha1)
    html = html.replace("{{TITULO_LINHA2}}", titulo_linha2)
    html = html.replace("{{TITULO_LINHA3}}", titulo_linha3)
    html = html.replace("{{COR}}", cor_acento)
    # ... etc
    
    # Renderizar com Playwright (mantido)
    # ...
```

### Fase 3: Atualizar chamadas existentes

| # | Arquivo | O que mudar |
|---|---------|------------|
| 3.1 | `gerar-capa.py:gerar_capa_da_obra()` | Adicionar cálculo de stats e categoria |
| 3.2 | `compilador-abnt/SKILL.md` | Atualizar documentação |
| 3.3 | `criar-livro.md` | Atualizar instruções de capa |
| 3.4 | `criar-playbook.md` | Atualizar instruções de capa |
| 3.5 | `criar-lead-magnet.md` | Atualizar instruções de capa |

### Fase 4: Gerar novas capas

| # | Ação | Comando |
|---|------|---------|
| 4.1 | Regenerar TODAS as capas | `python scripts/gerar-capa.py --todos` |
| 4.2 | Validar badges | `python scripts/validar-capa-nivel.py` |
| 4.3 | Validar texto | `python scripts/validar-capa-texto.py` |
| 4.4 | Testar abertura PNGs | Abrir em visualizador |

### Fase 5: Atualizar documentação

| # | Ação | Arquivo |
|---|------|---------|
| 5.1 | Atualizar manual | `docs/manual-completo-fabrica.md` |
| 5.2 | Atualizar spec de design | `docs/referencia-capa-design.md` |
| 5.3 | Atualizar skill compilador-abnt | `.claude/skills/compilador-abnt/SKILL.md` |

---

## Estimativa de Esforço

| Fase | Esforço | Dependências |
|------|---------|--------------|
| Fase 1 | ~2h | Nenhuma |
| Fase 2 | ~3h | Fase 1 |
| Fase 3 | ~1h | Fase 2 |
| Fase 4 | ~1h | Fase 3 |
| Fase 5 | ~30min | Fase 4 |
| **Total** | **~7h30** | — |

---

## Ordem de Execução

```
Fase 1 (template) → Fase 2 (script) → Fase 3 (chamadas) → Fase 4 (gerar) → Fase 5 (docs)
```

---

## Riscos

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| Template não renderiza bem em todas as dimensões | Alto | Testar com cada tipo (livro, ebook, etc.) |
| Variáveis não substituídas | Médio | Validação pós-geração |
| Cores da coleção não aplicadas | Alto | Testar com 2+ coleções |
| Performance (Playwright lento) | Baixo | Cache de template |
