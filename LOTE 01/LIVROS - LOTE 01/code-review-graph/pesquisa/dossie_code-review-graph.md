# Dossiê: Code Review Graph

## Visão Geral

O **Code Review Graph (CRG)** é uma ferramenta open-source que constrói um mapa estrutural do código-fonte usando Tree-sitter, rastreia mudanças incrementalmente e fornece contexto preciso a assistentes de IA via MCP (Model Context Protocol), permitindo que leiam apenas o que importa.

**URL:** https://github.com/tirth8205/code-review-graph
**Licença:** MIT
**Autor:** tirth8205
**Estrelas:** 28.4k
**Downloads PyPI:** Disponível via `pip install code-review-graph`

## Problema que Resolve

Ferramentas de IA para code review gastam tokens desnecessários lendo partes grandes do repositório. O CRG resolve isso construindo um grafo de dependências que permite ao agente ler apenas os arquivos relevantes.

## Números Chave

| Métrica | Valor |
|---------|-------|
| Redução mediana de tokens | ~65x |
| Máximo de redução | 376x (fastapi) |
| Ferramentas MCP | 30 |
| Linguagens suportadas | 30+ |
| Precisão F1 média | 0.69 |

## Arquitetura

1. **Parseamento AST:** Tree-sitter converte código em árvore sintática
2. **Grafo SQLite:** Nós (funções, classes, imports) + Arestas (chamadas, herança, testes)
3. **Blast Radius:** Rastreia dependências afetadas por mudanças
4. **MCP Server:** Expõe ferramentas para assistentes de IA

## Funcionalidades Principais

### Blast Radius Analysis
- Rastreia chamadores, dependentes e testes afetados
- Retorna apenas arquivos relevantes para o agente
- Economia de 71x no Flask (143.594 → 2.196 tokens)

### Atualizações Incrementais
- Re-parseia apenas arquivos com hash alterado
- ~2.5s para edição de 2 arquivos em projeto de 3.000 arquivos
- Hooks e watch mode mantêm grafo atualizado

### Busca Semântica
- Embeddings via sentence-transformers, Google Gemini, MiniMax ou OpenAI
- Busca híbrida (keyword + similaridade vetorial)
- FTS5-powered full-text search

### Visualização Interativa
- D3.js force-directed graph
- Exportação: GraphML, Neo4j Cypher, Obsidian, SVG
- Detecção de hubs e bridges

### 30 Ferramentas MCP
- `get_impact_radius` - Blast radius
- `get_review_context` - Contexto otimizado
- `detect_changes` - Análise de impacto
- `query_graph` - Consultas ao grafo
- `semantic_search_nodes` - Busca semântica
- E mais 25 ferramentas

### GitHub Action
- Reviews automáticos em CI
- Comentários sticky em PRs
- Opção `fail-on-risk` como merge gate

## Plataformas Suportadas

Claude Code, Cursor, Windsurf, Copilot, Gemini CLI, Zed, Continue, OpenCode, Antigravity, Qwen, Qoder, Kiro, CodeBuddy, Codex

## Limitações

- Recall 1.0 é circular (derivado do próprio grafo)
- Pequenas mudanças em arquivo único podem ter overhead
- Qualidade de busca (MRR 0.35) precisa melhorar
- Detecção de fluxos (33% recall) precisa trabalho em JS/Go

## Referências

1. Repository: https://github.com/tirth8205/code-review-graph
2. Tree-sitter: https://tree-sitter.github.io/tree-sitter/
3. MCP: https://modelcontextprotocol.io/
4. PyPI: https://pypi.org/project/code-review-graph/
5. Website: https://code-review-graph.com
