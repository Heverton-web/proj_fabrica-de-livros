# Relatório Consolidado — IA Agêntica Desbloqueada

> Um guia para projetar, construir e implantar sistemas de IA autônomos — com o projeto prático **OrquestraIA** do início ao fim.
> Autor: Heverton Eduardo Peres · Nível: **Intermediário** · Tamanho: **XG** · Data: 07/08/2026

## 1. Livro (XG)

- **5 Partes · 20 capítulos** no framework EITA-V2 (Introdução, Explica, Ilustra, Técnica, Aplica, Conclusão, Referências)
- **502.654 caracteres** no `livro_final.md` (meta XG ≥ 500.000 cumprida com folga)
- **33 refs ABNT únicas por capítulo** (média), **20 diagramas Mermaid** validados (`renderizar-diagramas.py` 20/20 OK)
- **50 blocos de código Python** com sintaxe validada
- **Auditoria estrita: VEREDITO CONFORME** (11/11 regras R1-R15 aplicáveis) — Fase 2.5
- **Parecer do revisor técnico: CONFORME** (`revisao/parecer_revisao.md`) — 0 não conformidades residuais, código e diagramas com exit 0
- Capa gráfica 2D com badge **NÍVEL INTERMEDIÁRIO** (gate `validar-capa-nivel.py` aprovado), CIP/ISBN/CDD com paginação real
- **PDF final: `livro_final.pdf` (4.062 KB, 264 páginas)** via Pandoc→Typst

### Partes e capítulos
| Parte | Capítulos | Tema |
|---|---|---|
| I — Fundamentos da Autonomia | 1–4 | O que é IA agêntica, o agent loop, arquiteturas e fundamentos científicos (ReAct, memória, planejamento) |
| II — Projetando o Sistema | 5–8 | Design de agentes, memória, ferramentas/function calling, planejamento de tarefas |
| III — Construindo o OrquestraIA | 9–12 | Núcleo do orquestrador, MCP/APIs, multiagentes na prática |
| IV — Governança e Qualidade | 13–16 | Avaliação (evals), segurança, supervisão humana (HITL), observabilidade e custos |
| V — Implantação e Operação | 17–20 | Deploy, operação contínua, monitoramento e o engenheiro de sistemas agênticos |

Fio condutor: o projeto prático **OrquestraIA** (sistema multiagente real: suporte ao cliente, vendas e análise de dados) atravessa os 20 capítulos, do primeiro agent loop à operação em produção.

## 2. Artigos Científicos (3, IMRaD — NBR 6024/10520/6023)

Todos **CONFORMES** na auditoria (`--tipo artigo`), com **20+ refs autor-data por seção**, citações (SOBRENOME, ano) sem órfãs, resumo/abstract em `artigo_metadados.json` e PDF via `templates/template_artigo.typ`:

| # | Artigo | PDF |
|---|---|---|
| 1 | O que é IA Agêntica e o agent loop: definição, arquitetura e implicações | 129 KB |
| 2 | Ferramentas, function calling e planejamento de tarefas: as mãos e a bússola | 128 KB |
| 3 | Avaliação, segurança e supervisão humana: a governança dos sistemas autônomos | 131 KB |

## 3. E-books (5, EPUB + PDF + capa 1:1,6 com badge)

Todos **CONFORMES** na auditoria (`--tipo ebook`, regra EBOOK-LEN ≥ 45.000 chars), adaptação de tom comercial-leve dos capítulos do livro-mãe com CTA final e seção "Para se aprofundar" (R-EBK-5):

| # | E-book | Chars | EPUB | PDF |
|---|---|---|---|---|
| 1 | Fundamentos da Autonomia | 82.588 | 98 KB | 647 KB |
| 2 | Projetando o Sistema de IA Agêntica | 80.081 | 99 KB | 653 KB |
| 3 | Construindo o OrquestraIA na Prática | 75.254 | 103 KB | 625 KB |
| 4 | Governança e Qualidade para Agentes | 76.540 | 100 KB | 647 KB |
| 5 | Implantação e Operação Contínua | 77.050 | 99 KB | 639 KB |

## 4. Distribuição

Pacote autocontido em `output/livros/ia-agentica-desbloqueada/distribuicao/`:

- `livro_final.pdf` (4.066 KB)
- `artigos/artigo_1..3.pdf`
- `ebooks/ebook_1..5.epub` + `.pdf` + `capas/capa_ebook_N.png` + `thumbnail_ebook_N.png`
- `README.md` + `LICENSE` (todos os direitos reservados)

## 5. Estatísticas finais da obra

- Caracteres do livro: **505.099** (XG)
- Total de capítulos: **20** (livro) + **12** (3 artigos × 4 seções) + **20** (5 e-books × 4 capítulos)
- Referências ABNT: **33 por capítulo** (livro) · 23–25 por artigo
- Diagramas Mermaid: **20/20 válidos** · Blocos de código: **50** com CI
- Auditorias: **livro CONFORME** · **3/3 artigos CONFORME** · **5/5 e-books CONFORME**
