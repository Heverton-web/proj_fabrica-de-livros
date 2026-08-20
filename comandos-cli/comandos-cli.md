# Manual de Comandos CLI — ccusage (pip), ccusage (npm) e agenttrace

> Guia de referência rápida. Copie e cole os comandos conforme a necessidade.

## ccusage (pip) — status de rate limit da API Anthropic

```bash
ccusage status
```

```bash
ccusage json
```

```bash
ccusage refresh
```

```bash
ccusage daemon
```

```bash
ccusage statusline
```

```bash
ccusage install
```

---

## ccusage (npm) — relatório de tokens/custo por período

> Comando `ccusage` puro está ocupado pela versão pip. Use sempre via `npx`.

```bash
npx ccusage@latest daily
```

```bash
npx ccusage@latest monthly
```

```bash
npx ccusage@latest weekly
```

```bash
npx ccusage@latest session
```

```bash
npx ccusage@latest blocks
```

```bash
npx ccusage@latest claude
```

```bash
npx ccusage@latest codex
```

```bash
npx ccusage@latest opencode
```

```bash
npx ccusage@latest statusline
```

```bash
npx ccusage@latest --help
```

---

## agenttrace (pip) — tracing/eval de agentes de IA

```bash
agenttrace start
```

```bash
agenttrace --help
```

Uso programático (Python):

```python
from agenttrace import TraceManager, TracerEval
```

---

## Relatório de consumo (MD + PDF + XLSX)

Gera um relatório consolidado (rate limit + uso diário/mensal/sessão/blocos)
em `rel-consumo/<data>-consumo-cli.{md,pdf,xlsx}`:

```bash
python scripts/gerar-relatorio-consumo.py
```

```bash
python scripts/gerar-relatorio-consumo.py --md-apenas
```

```bash
python scripts/gerar-relatorio-consumo.py --sem-rate-limit
```

---

## Observações

- `ccusage` (pip, autor wakamex) e `ccusage` (npm, autor ryoppippi) são projetos
  diferentes com o mesmo nome. No PATH deste ambiente, o comando `ccusage` puro
  resolve para a versão **pip**; a versão **npm** só é acessada via `npx ccusage@latest`.
- `agenttrace start` sobe o frontend do Tensorscope (visualizador de traces) —
  processo fica em primeiro plano até ser encerrado.
- **Nomes de modelo com `@` quebram o PDF:** o JSON do `ccusage` npm traz nomes
  de modelo tipo `@cf/mistralai/mistral-small-3.1-24b-instruct` (Cloudflare
  Workers AI). O Pandoc interpreta `@algo` como citação bibliográfica e o Typst
  falha com `the document does not contain a bibliography`. Fix: escapar `@` →
  `\@` só na tabela de EXIBIÇÃO (md/pdf) via `df_para_md_tabela`, mantendo o
  dado cru no `.xlsx`. Arquivo: `scripts/gerar-relatorio-consumo.py`.
- **PDF de tabela larga (9 colunas) fica ilegível em retrato A4:** o template
  padrão do Pandoc para Typst (`conf()`) só expõe `papersize`/`margin` como
  variáveis — não existe variável de "paisagem". Fix: injetar
  `#set page(flipped: true)` via `--include-in-header` (arquivo
  `scripts/typst-landscape-header.typ`) — esse `#set` sobrevive ao `#set page`
  interno do `conf()` porque no Typst `#set` só sobrescreve os campos citados,
  não reseta os demais. Confirmado com `pypdf`: MediaBox virou 841.89×595.27pt
  (A4 paisagem). Reaproveitável em qualquer relatório Pandoc→Typst com tabela
  larga — só apontar `-H scripts/typst-landscape-header.typ`.
  **Atualização:** revertido para retrato depois que as tabelas de impressão
  caíram para 5 colunas enxutas (ver item abaixo) — retrato coube sem
  sobreposição e ainda dá mais folga vertical por página (841pt de altura vs
  595pt em paisagem). O arquivo `typst-landscape-header.typ` continua no
  repo, sem uso no gerador atual, como referência para o próximo relatório
  que precisar de tabela larga de verdade.
- **Coluna com célula muito mais larga que as outras destrói a tabela inteira:**
  mesmo em paisagem, a tabela de "Uso Mensal" saiu com todas as colunas
  numéricas sobrepostas/ilegíveis. Causa raiz: a largura de coluna do
  Typst/Pandoc é proporcional ao conteúdo mais largo de cada coluna; a coluna
  `modelos` (lista separada por vírgula, uma célula com 15+ nomes = 300+
  chars) fez as colunas numéricas ficarem com largura ~0, sobrepondo os
  números. UUIDs de 36 chars na coluna `periodo` (sessões) causam o mesmo
  estouro. Fix: no MD/PDF mostrar só um recorte enxuto (`periodo` truncado a
  12 chars, `agente`, `n_modelos` como contagem em vez da lista, `tokens_total`
  e `custo_usd` formatados) via `df_para_impressao()` — a lista completa de
  modelos e o breakdown de tokens continuam no `.xlsx`. Regra geral: nunca
  colocar uma coluna de texto livre/lista na mesma tabela markdown→Typst que
  colunas numéricas apertadas.
- **Tabela grande demais para uma página duplica a última linha (bug do
  Typst, não documentado):** com ~25 linhas numa tabela A4-paisagem 9pt, a
  última linha renderiza DUAS VEZES sobrepostas, mesmo a tabela começando do
  topo de uma página em branco — não é posição na página, é a ALTURA total
  da tabela chegando perto do limite. Uma tabela de 6 linhas no mesmo
  documento saiu perfeita. Fix: parar de confiar em "quantas linhas cabem" e
  paginar manualmente em blocos de 15 linhas (`LINHAS_POR_BLOCO`), cada bloco
  virando uma tabela markdown separada por `#pagebreak()` — função
  `tabela_em_blocos()`. Diagnóstico feito renderizando o PDF para PNG com
  PyMuPDF (`fitz`) e inspecionando página a página — sem isso o bug não
  aparece só lendo o `.md` fonte.
- **`ccusage blocks --json` tem schema diferente de daily/monthly/session:**
  usa `id`/`costUSD`/`models`/`tokenCounts.{inputTokens,outputTokens,
  cacheCreationInputTokens,cacheReadInputTokens}` em vez de `period`/
  `totalCost`/`modelsUsed`/campos soltos — reaproveitar o mapeamento genérico
  para blocks gerava `periodo=None`, `agente=nan`, `custo_usd=0`
  silenciosamente (sem erro, só dado errado). Fix: função dedicada
  `blocos_para_df()`. Lição: sempre inspecionar o JSON real de cada
  subcomando antes de reusar um mapeador entre eles.
