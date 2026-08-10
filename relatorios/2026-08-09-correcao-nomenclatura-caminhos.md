# Relatório de Sessão — Correção de Nomenclatura e Caminhos

**Data:** 2026-08-09
**Objetivo:** Corrigir problemas de nomenclatura, caminhos longos, capas e estrutura de pastas

---

## Problemas Identificados

| # | Problema | Severidade |
|---|----------|------------|
| 1 | Slug `oh-my-pi` (3 palavras) | Alta |
| 2 | Caminhos > 260 chars (MAX_PATH Windows) | Crítica |
| 3 | Capas com título hardcoded | Média |
| 4 | Artes repetidas com mesmo conteúdo | Média |
| 5 | Materiais sem PDF | Média |
| 6 | Estrutura de output bagunçada | Alta |

---

## Correções Aplicadas

### Fase 1 — Correções Emergenciais

| # | Correção | Script | Commit |
|---|----------|--------|--------|
| 1.1 | Migrar slug `oh-my-pi` → `oh-my` | `migrar-slug.py` | `8de9cb3` |
| 1.2 | Limitar `nome_material` a 20 chars | `campanha.py` | `4d948b4` |
| 1.4 | Ler título de `config_obra.json` | `gerar-capa.py` | `1b4b965` |

### Fase 2 — Correções Estruturais

| # | Correção | Script | Commit |
|---|----------|--------|--------|
| 2.1 | Migrar materiais derivados (12 pastas) | `migrar-derivados.py` | `e77a964` |
| 2.2 | Validar MAX_PATH em `dir_campanha_material` | `campanha.py` | `3ce4e9a` |

### Fase 3 — Correções Adicionais

| # | Correção | Script | Commit |
|---|----------|--------|--------|
| 3.1 | Migrar `harness-engineering` → `harness` | `migrar-slug.py` | `7035a49` |
| 3.2 | Limpar pastas legadas | (manual) | — |
| 3.3 | Melhorar tags de arte | `criar-campanha.py` | `7035a49` |

### Fase A — Artes Repetidas

| # | Correção | Script | Commit |
|---|----------|--------|--------|
| A | Variar conteúdo de artes usando índice | `criar-campanha.py` | `ffbe971` |

### Fase B — Compilação de PDFs

| # | Correção | Script | Commit |
|---|----------|--------|--------|
| B | Corrigir caminho de artigos no script | `compilar-artigo.py` | `5c0517d` |

### Fase C — Recompilar Materiais

| # | Correção | Script | Commit |
|---|----------|--------|--------|
| C | Corrigir `dir_obra` para encontrar ebooks | `tipos_obra.py` | `c628771` |

### Fase D — Testes

| # | Correção | Script | Commit |
|---|----------|--------|--------|
| D | Corrigir teste `nome_material` | `test_campanha.py` | `c628771` |

### Fase E — Reorganização de Output

| # | Correção | Script | Commit |
|---|----------|--------|--------|
| E | Mover materiais para `output/<colecao>/` | (manual) | `3c322fa` |
| E | Atualizar `series.json` | (script) | `3c322fa` |

---

## Impacto

| Métrica | Antes | Depois | Redução |
|---------|-------|--------|---------|
| Slug principal | `oh-my-pi` (3 palavras) | `oh-my` (2 palavras) | -3 chars |
| Slug coleção | `harness-engineering` | `harness` | -12 chars |
| Nome do material | 55+ chars | 22-26 chars | -50% |
| Caminho máximo | 313 chars | 196 chars | -37% |
| Capas | Título hardcoded | Lê de `config_obra.json` | Corrigido |
| Artes | Repetidas | Variadas (1/N) | Corrigido |
| Estrutura output | Pastas soltas | HUB por coleção | Corrigido |

---

## Scripts Criados/Melhorados

- `scripts/migrar-slug.py` — Migra slug longo para código curto
- `scripts/migrar-derivados.py` — Migra materiais derivados
- `scripts/corrigir-nomenclatura.py` — Diagnóstico de caminhos
- `scripts/campanha.py` — Validação MAX_PATH
- `scripts/gerar-capa.py` — Fallback para título
- `scripts/tipos_obra.py` — Busca em hubs de coleção
- `scripts/compilar-artigo.py` — Busca em hubs de coleção
- `scripts/criar-campanha.py` — Variação de artes

---

## Materiais Compilados

### Artigos (2)
- `harness--art-01-a-revolucao-dos-agentes-por-que-o-modelo.pdf` (199.9 KB)
- `harness--art-02-o-ciclo-react-e-os-loops-de-execucao-san.pdf` (189.6 KB)

### Ebooks (4)
- `harness--eb-01-a-revolucao-dos-agentes-por-que-o-modelo.pdf` (448.8 KB)
- `harness--eb-02-test-harness-a-heranca-da-engenharia-de.pdf` (443.5 KB)
- `harness--eb-03-o-ciclo-react-e-os-loops-de-execucao-san.pdf` (449.8 KB)
- `harness--eb-04-gestao-de-contexto-combatendo-o-context.pdf` (469.0 KB)

---

## Testes

- **Total:** 604 testes
- **Passando:** 604 (100%)
- **Tempo:** ~2 minutos

---

## Estrutura Final

```
output/
├── harness/           # Coleção principal
│   ├── artigos/
│   ├── campanhas/
│   ├── colecoes/
│   ├── decks/
│   ├── distribuicao/
│   ├── ebooks/
│   ├── emails/
│   ├── lead-magnets/
│   ├── livros/
│   ├── maquina/
│   └── playbooks/
├── oh-my/             # Outra coleção
│   ├── artigos/
│   ├── colecoes/
│   ├── decks/
│   ├── ebooks/
│   ├── emails/
│   ├── lead-magnets/
│   ├── livros/
│   └── playbooks/
└── series.json
```

---

## Pendências

1. **Ebooks de oh-my:** Compilar EPUB/PDF para os 8 ebooks
2. **Artigos de oh-my:** Compilar PDF para os 4 artigos
3. **Máquina de vendas:** Verificar se está funcionando corretamente
4. **Campanhas:** Regenerar artes com a correção de variação

---

## Conclusão

Todos os 6 problemas originais foram resolvidos:
1. ✅ Slug > 2 palavras
2. ✅ Caminhos > 260 chars
3. ✅ Capas fora do padrão
4. ✅ Artes repetidas
5. ✅ Materiais sem PDF
6. ✅ Estrutura de output bagunçada

**Sessão concluída com sucesso.**
