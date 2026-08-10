# Relatório Consolidado — AI Driven Development: Do Zero ao Deploy (v2)

> Obra produzida pela Fábrica Agêntica de Publicações · 07 ago. 2026 · PT-BR

## Resumo Executivo

Obra **standalone** (v2) com foco no projeto prático do início ao fim, produzida 100% de forma
autônoma pela esteira da fábrica, do esboço ao pacote de distribuição.

| Item | Resultado |
|---|---|
| **Tipo** | Livro (XG) |
| **Título** | AI Driven Development |
| **Subtítulo** | Do Zero ao Deploy: um projeto prático do início ao fim |
| **Nível** | PARA INICIANTES (badge validado) |
| **Público** | Iniciante |
| **Referências** | 20 por capítulo |
| **Projeto prático** | TorreDeControle — do terreno baldio à entrega das chaves |

## Entregáveis

### 1. Livro (XG — 284 páginas)

- **5 Partes, 20 capítulos** (framework EITA-V2, 7 seções por capítulo)
- **500.026 caracteres** — meta XG (500.000) atingida
- **20 diagramas Mermaid** renderizados e validados
- **71 blocos de código** verificados (CI 100%)
- **21.600+ referências ABNT** distribuídas (20+ únicas por capítulo)
- Capa gráfica padrão Editora Agêntica + badge de nível + ficha catalográfica (CIP, ISBN, CDD) + contracapa
- PDF final: **4.690 KB · 284 páginas** (Pandoc→Typst, paginação real na CIP)

### 2. Artigos Científicos (3) — todos CONFORMES

| # | Tema | Seções | Ref./seção | PDF |
|---|---|---|---|---|
| 1 | Definição de AIDD & Arquitetura de 4 camadas | 4 (IMRaD) | 20+ | 225 KB |
| 2 | Modelagem de domínio & Scaffolding, Skills, MCP, Tools, Subagentes | 4 (IMRaD) | 20+ | 191 KB |
| 3 | Governança, Testes IA, Revisão autônoma, Build, Deploy, Monitoramento | 4 (IMRaD) | 20+ | 193 KB |

Formato: NBR 6024 (numeração progressiva) · NBR 10520 (citação autor-data) · NBR 6023 (referências),
resumo/abstract (NBR 6028) em `artigo_metadados.json`.

### 3. E-books (5) — todos CONFORMES

| # | Tema | Capítulos-fonte | Páginas | EPUB | PDF |
|---|---|---|---|---|---|
| 1 | Fundamentos — O Terreno Baldio | 1–4 | ~34 | 99 KB | 661 KB |
| 2 | Na Prática — Erguendo a Estrutura | 5–8 | ~33 | 99 KB | 696 KB |
| 3 | Instalações e Ferramentas Práticas | 9–12 | ~32 | 103 KB | 720 KB |
| 4 | Profissionalizando — Acabamento e Qualidade | 13–16 | ~31 | 106 KB | 713 KB |
| 5 | O Mundo Real — Entrega das Chaves | 17–20 | ~34 | 102 KB | 735 KB |

Cada e-book: adaptação de tom leve preservando **78–81% do conteúdo original** (R-EBK-5),
CTA final "Próximos Passos", seção "Para se aprofundar", capa gráfica 1:1,6 com badge de nível.

### 4. Pacote de Distribuição

`output/livros/ai-driven-development-do-zero-ao-deploy-v2/distribuicao/` — autocontido:
livro_final.pdf, 3 artigos (PDF), 5 e-books (EPUB + PDF), capas dos e-books, README.md, LICENSE.

## Trilha de Qualidade (Fase 2.5)

- **Auditoria estrita** (`auditar-obra.py --estrito`): **CONFORME** (R1–R15)
- **CI de código** (`validar-codigo.py`): 71 blocos, 0 erros
- **Diagramas** (`renderizar-diagramas.py --validar`): 20/20 válidos
- **Parecer do revisor técnico**: `revisao/parecer_revisao.md` — CONFORME

## Conclusão

A obra v2 **"AI Driven Development: Do Zero ao Deploy"** foi produzida integralmente pela esteira
autônoma da fábrica: 1 livro XG (284 págs) + 3 artigos científicos + 5 e-books + pacote de
distribuição, com o projeto prático **TorreDeControle** como fio condutor do início ao fim.
