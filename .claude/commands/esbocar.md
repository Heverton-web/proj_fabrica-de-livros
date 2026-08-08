---
description: Fase 0 (V4) da Fábrica Agêntica de Publicações — elicitação interativa que decide tipo de obra (Livro/TCC), tamanho, mínimo de referências e se gera artigos/ebooks derivados. Único ponto de interação humana; depois disso a esteira roda 100% autônoma (REGRA 3).
---

Você é o Orquestrador Mestre. O operador disparou `/esbocar` com o tema em `$ARGUMENTS`.
Esta é a **Fase 0** — a única rodada de perguntas de toda a esteira.

## Passo 0 — Preparação
1. Slug em kebab-case a partir do tema. Se `output/livros/<slug>/` ou
   `output/tccs/<slug>/` já existir com conteúdo, use sufixo `-v2`.
2. A pasta raiz da obra (`output/livros/<slug>/` ou `output/tccs/<slug>/`, conforme
   o tipo escolhido no Passo 1) só é criada no Passo 2, quando o tipo já é conhecido —
   livros, TCCs, artigos e e-books vivem em raízes separadas no topo de `output/`
   (`output/livros/`, `output/tccs/`, `output/artigos/`, `output/ebooks/`); artigos e
   e-books derivados de uma obra não ficam aninhados dentro da pasta da obra-mãe,
   apenas referenciam o slug dela via `slug_livro_mae`.

## Passo 1 — Elicitação (2 rodadas de `AskUserQuestion`)

**Rodada 1 — sempre perguntar (até 4 perguntas por chamada):**

| Header | Pergunta | Opções |
|---|---|---|
| Tipo | Qual o tipo de obra a ser escrita? | Livro (Recommended) \| TCC |
| Senioridade | Qual o nível de senioridade principal do público-alvo? | Iniciante \| Intermediário (Recommended) \| Avançado \| Técnico |
| Refs | Mínimo de referências por capítulo? | 5 \| 8 \| 12 \| 16 \| 20 |
| Artigos | Deseja gerar artigos científicos a partir do tema? | Sim \| Não (Recommended) |

**Rodada 2 — só as perguntas aplicáveis às respostas da Rodada 1:**

| Header | Pergunta | Condição | Opções |
|---|---|---|---|
| Tamanho | Qual o tamanho do livro? | Tipo = Livro | P — 1 Parte, 4 capítulos, ~40 páginas \| M — 2 Partes, 8 capítulos, ~80 páginas (Recommended) \| G — 3 Partes, 12 capítulos, ~120 páginas \| GG — 4 Partes, 16 capítulos, ~160 páginas |
| Ebooks | Deseja gerar e-books a partir da obra? | Tipo = Livro | Sim \| Não (Recommended) |
| Qtd. Artigos | Quantos artigos científicos? | Artigos = Sim | 1 \| 2 \| 3 \| 4 \| 5 |
| Qtd. Ebooks | Quantos e-books? | Ebooks = Sim | 1-3 \| 4-6 \| 7-10 |
| Série | Esta obra faz parte de uma série/coleção? | sempre | Não, standalone (Recommended) \| Other (nome da série) |

**Rodada 3 (V5) — COLEÇÃO: derivados de extração (custo ~0 token):**

| Header | Pergunta | Condição | Opções |
|---|---|---|---|
| Derivados | Quais materiais de extração gerar? (múltipla) | Tipo = Livro | Playbook (Recommended) \| Lead magnets \| Slide deck \| Sequência de e-mails |
| Formatos LM | Quais formatos de lead magnet? (múltipla) | Lead magnets = Sim | Checklist (Recommended) \| Armadilhas \| Cheat sheet \| Mapa |
| CTA | URL de destino do CTA (rastreável) | Lead magnets, Deck ou E-mails = Sim | Other (URL) |

`multiSelect: true` nas duas primeiras. A pergunta **CTA é obrigatória** quando
qualquer um dos três tipos de conversão foi escolhido — sem `cta_url` os gates
R-LM-1 / R-DK-3 / R-EM-2 reprovam. Formatos válidos completos:
`checklist, armadilhas, cheatsheet, mapa, entregas, mini-guia`
(`python scripts/tipos_obra.py --formatos-lm`).

O `AskUserQuestion` aceita no máximo 4 opções por pergunta. Para o tier **XG — 5
Partes, 20 capítulos, ~200 páginas** (o maior da tabela, acima de GG), o operador
seleciona "Other" na pergunta Tamanho e digita `XG`.

Se "Qtd. Ebooks" vier como faixa, use o valor médio da faixa (2, 5 ou 8) como `qtd_ebooks`.
Se o operador selecionar "Other" em qualquer pergunta, use o valor livre fornecido,
respeitando os limites: refs 5-20, artigos 1-5, ebooks 1-10, tamanho P/M/G/GG/XG,
senioridade: iniciante/intermediario/avancado/tecnico,
série: qualquer texto livre (ou `null` se "Não, standalone").

## Passo 2 — Gravar `config_obra.json`

Com o `tipo_obra` já respondido no Passo 1, defina `prefixo = "livros"` (tipo_obra=livro)
ou `prefixo = "tccs"` (tipo_obra=tcc) e crie `output/<prefixo>/<slug>/`.

Grave `output/<prefixo>/<slug>/config_obra.json` (raiz da obra, sem subpasta `esboco/`)
no schema:
```json
{
  "tema": "$ARGUMENTS",
  "tipo_obra": "livro | tcc",
  "min_referencias_por_capitulo": 5,
  "tamanho_obra": "P | M | G | GG | XG | null",
  "senioridade_obra": "iniciante | intermediario | avancado | tecnico",
  "serie": "<nome-da-serie> | null",
  "gerar_artigos": true,
  "qtd_artigos": 3,
  "gerar_ebooks": true,
  "qtd_ebooks": 5,

  "gerar_playbook": true,
  "gerar_lead_magnets": true,
  "formatos_lm": ["checklist", "armadilhas"],
  "gerar_deck": false,
  "gerar_emails": false,
  "cta_url": "https://exemplo.com/obra",
  "cta_texto": "Quero a obra completa",

  "modo_producao": "obra-unica",
  "obra_raiz": null
}
```

> `modo_producao` aceita `obra-unica` (padrão) ou `cascata`. Em `cascata`,
> preencha `obra_raiz` com `livro` ou `tcc` — a raiz é gerada primeiro e os
> derivados de **compressão/extração** saem dela. Nunca cascateie uma
> **expansão** (TCC → livro): ali o custo é de geração, não de reescrita.
Valide com:
```bash
python scripts/parametros_obra.py <prefixo>/<slug> --validar
```
Se inválido, corrija os valores fora de faixa antes de prosseguir (nunca pergunte de novo — REGRA 3).

## Passo 3 — Gerar o esboço (sem pausa)

3. Invoque `subagente-pesquisador` com o tema. Dossiê em `output/<prefixo>/<slug>/pesquisa/`.
4. Indexe o dossiê: `python scripts/indexar-dossie.py <prefixo>/<slug> --indexar`.
5. Invoque `arquiteto` passando `tipo_obra` e `tamanho_obra` de `config_obra.json` — o
   sumário macro gerado deve respeitar os mínimos de `scripts/parametros_obra.py`
   (tabela `TAMANHOS` para livro; TCC usa 1 "parte" com as seções do framework ACAD
   como "capítulos" — ver `SPEC_TCC.md`).
6. Se `gerar_artigos=true`: `python scripts/fatiar-obra.py <prefixo>/<slug> --artigos --qtd <qtd_artigos>`
   — particiona o sumário macro em `qtd_artigos` recortes temáticos (1-2 capítulos
   cada, sem sobreposição), cria cada `output/artigos/<slug>--art-NN-<titulo>/` e
   grava `output/<prefixo>/<slug>/derivados.json` (seção `artigos`).
7. Se `gerar_ebooks=true`: `python scripts/fatiar-obra.py <prefixo>/<slug> --ebooks --qtd <qtd_ebooks>`
   — mesmo princípio, cria cada `output/ebooks/<slug>--eb-NN-<titulo>/` e grava a
   seção `ebooks` do mesmo `derivados.json` (preserva a seção `artigos` já gravada).
8. Se `gerar_playbook=true`: `python scripts/fatiar-obra.py <prefixo>/<slug> --playbook`
   — cria o esqueleto em `output/playbooks/<slug>--pbk/`. A extração dos cards só
   roda depois que os capítulos existirem (`/criar-playbook`).
9. `python scripts/colecao.py --sincronizar --slug <prefixo>/<slug>` — registra a
   obra e seus derivados no manifesto `output/colecoes/<serie>.json`.

> Lead magnets, deck e e-mails **não** são fatiados aqui: dependem dos capítulos
> prontos. Ficam registrados no `config_obra.json` e são disparados na Fase 3
> por `/criar-lead-magnet`, `/criar-deck` e `/criar-emails`.

## Passo 4 — Relatório objetivo (REGRA 2, sem metatexto)

Exiba: slug completo (`<prefixo>/<slug>`), tipo de obra, tamanho (se livro),
quantidade de capítulos planejados, quantidade de artigos/ebooks planejados (se
solicitados), e a lista de comandos disponíveis para prosseguir:

```
/produzir-obra-completa <prefixo>/<slug>     — dispara tudo encadeado/paralelo
/criar-livro <prefixo>/<slug>                — só o livro/TCC
/criar-artigo <prefixo>/<slug>               — só os artigos (requer livro-mãe com dossiê+sumário)
/criar-ebook <prefixo>/<slug>                — só os ebooks (requer livro-mãe compilado)
/criar-playbook <prefixo>/<slug>             — só o playbook (extração, ~0 token)
/criar-lead-magnet <prefixo>/<slug> --todos  — família de lead magnets (~0 token)
/criar-deck <prefixo>/<slug>                 — slide deck 16:9 (~0 token)
/criar-emails <prefixo>/<slug>               — sequência de nutrição
/colecao --sincronizar                       — manifesto da coleção
```

Nenhuma pergunta adicional é feita a partir daqui — a esteira é 100% autônoma
(REGRA 3) até a entrega final de qualquer um dos comandos acima.
