# Relatório de Entrega — Livro 4 "A Pilha Agêntica"

**Obra:** *MCP na prática: conectando agentes ao mundo real*
**Slug:** `livros/mcp-na-pratica-conectando-agentes-ao-mundo-real`
**Data:** 5 de agosto de 2026
**Fluxo:** `/esbocar` → `/criar-livro` → auditoria → PDF ABNT → distribuição

---

## 1. Entregáveis principais

```
OBRA: MCP na prática (livro, tamanho G)
  Principal    : output/livros/mcp-na-pratica-conectando-agentes-ao-mundo-real/livro_final.pdf
                 — 192 páginas, 2,9 MB, ABNT (Pandoc → Typst) — veredito CONFORME
  Capítulos    : 10 (5 Partes) — 375.582 caracteres (~150 pág.)
  Referências  : 20 ABNT por capítulo (dossiê com 22 fontes reais)
  Diagramas    : 10/10 Mermaid válidos e renderizados
  Código       : 27 blocos, taxa 100% (0 falhas no CI de sintaxe)
  Capa         : A4 flat 2D Editora Agêntica (1600×2263px) + thumbnail
  Distribuição : output/<slug>/distribuicao/ (README.md, LICENSE, capa, thumbnail, livro_final.pdf)
  Pendências   : nenhuma
```

## 2. Estrutura da obra

| Parte | Título | Capítulos |
|---|---|---|
| 1 | O Protocolo que Conectou os Agentes ao Mundo | 1. O agente isolado e a explosão dos conectores proprietários · 2. Arquitetura MCP: host, client e server |
| 2 | Transportes e Primitivas | 3. Transportes: do stdio ao Streamable HTTP · 4. As três primitivas: tools, resources e prompts |
| 3 | Construindo e Consumindo Servidores | 5. Servidor MCP do zero em TypeScript · 6. Servidores em Python: da tipagem ao deploy · 7. Registro oficial e ecossistema |
| 4 | Segurança: a Porta de Entrada Não Revisada | 8. Least-privilege, OAuth e capability tokens · 9. Prompt injection, tool poisoning e SSRF |
| 5 | MCP Engineering como Disciplina | 10. A disciplina de expor o mundo ao agente |

## 3. Fontes do dossiê (22)

Especificações oficiais do MCP (2025-11-25 e 2026-07-28: Architecture, Transports, Tools, Resources, Security Best Practices), SDKs TypeScript e Python, Quickstart, MCP Registry, GitHub MCP Registry, CSA Agentic MCP Security Guide, Invariant Labs Tool Poisoning, Simon Willison prompt injection, MCPLib (Tsinghua/Ant Group, arXiv), CISA, CIS Companion Guide, NSA e PulseMCP.

## 4. Caminho completo do fluxo

Esboço (config + dossiê indexado + sumário macro) ✅ → 10 capítulos em lotes ✅ → pool 10/10 ✅ → expansão a 375.582 caracteres ✅ → auditoria CONFORME (R2–R15) ✅ → capa Editora Agêntica ✅ → PDF ABNT 192 páginas ✅ → distribuição ✅ → parecer + relatório ✅.

## 5. Pendências e recomendações

- **Pendências:** nenhuma.
- **Recomendação:** revisão de copidesque futura para tratar alertas de estilo (parágrafos sobrepostos entre capítulos e grafias inconsistentes) — não bloqueantes.
- **Próximo passo da série:** Livro 5 da Parte II (camada de contexto) ou avanço para a Parte III (harness), conforme o planejamento editorial.
