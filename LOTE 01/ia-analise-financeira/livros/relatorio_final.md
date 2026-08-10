# Relatório Final — Coleção IA no Trabalho Financeiro

**Autor:** Heverton Eduardo Peres · **Data:** 2026-08-08 · **Motivo condutor:** Mesa de Operações · **Persona:** Analista de Inteligência Financeira · **Badge:** Iniciante

## Escopo

Como usar IA **gratuita** no trabalho de análise do setor financeiro: criação e análise de planilhas, KPIs e análise de dados com ChatGPT, Gemini, Copilot, Claude e modelos open-source locais (Ollama/Llama/Gemma).

## Entregas da coleção (12 membros)

| # | Tipo | Material | Arquivos |
|---|---|---|---|
| 1 | Livro | IA no Trabalho Financeiro (8 caps, 200k chars, R1–R15 CONFORME) | `livro_final.pdf` + capa + 8 diagramas |
| 2 | E-book | Fundamentos: O Que É e Por Que Importa (caps 1–4) | `.epub` + `.pdf` + capa |
| 3 | E-book | Na Prática: A IA na Bancada (caps 5–8) | `.epub` + `.pdf` + capa |
| 4 | Playbook | 8 cards de bancada (R-PBK-0 a R-PBK-8 CONFORME) | `playbook.md` + `.pdf` + capa |
| 5–10 | Lead magnets | Armadilhas, Cheat Sheet, Checklist, Entregas, Mapa, Mini-guia (6/6 CONFORME) | `.pdf` + `card_social.png` |
| 11 | Deck | 14 slides navegável (HTML + PDF) | `.html` + `.pdf` |
| 12 | E-mails | Sequência de 10 e-mails em 18 dias | `sequencia.md` + 10 `email_*.md` |

## Validações

- **Auditoria da obra** (auditar-obra.py --estrito): **CONFORME** — R1–R15, 200.000+ caracteres, 20+ refs ABNT por capítulo em ordem numérica, diagramas Mermaid renderizados, código Python compilável.
- **CI de código** (validar-codigo.py --estrito): **100% aprovado**.
- **Playbook** (validar-playbook.py --estrito): **CONFORME** (0 violações).
- **Lead magnets** (validar-lead-magnet.py --estrito): **6/6 CONFORME**.
- **Deck** (validar-deck.py --estrito): **CONFORME** (13+1 slides).
- **E-mails** (validar-emails.py --estrito): **CONFORME** (10 e-mails).
- **E-books** (auditar-obra.py --tipo ebook): **CONFORME** (EBOOK-LEN: 103k e 97k chars, piso 45k).
- **Artefatos** (validar-artefatos.py --todos --estrito): **41 materiais, 0 não abrem**.

## Pacote de distribuição

`output/distribuicao/ia-analise/` — 15 arquivos, 4,8 MB, com `LEIA-ME.md` + `LICENCA.txt`.

CTA provisório em todos os derivados: `https://seu-site.com.br/ia` (substituir pelo link real e regenerar com `--cta-url`).

## Observações de reexecução

- Para reextrair o playbook após editar capítulos: `python scripts/extrair-passos-praticos.py livros/ia-analise-financeira` e revalidar.
- Para regenerar derivados com CTA real: `--cta-url <url>` em `gerar-lead-magnet.py`, `gerar-deck.py` e `gerar-sequencia-emails.py`.
