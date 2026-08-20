# Manual de Comandos CLI — ccusage (pip), ccusage (npm) e agenttrace

> Guia de referência rápida. Copie e cole os comandos conforme a necessidade.

## ccusage (pip) — status de rate limit da API Anthropic

```bash
ccusage status
```
Mostra o status atual (% da sessão e % da janela de 7 dias usados, com hora de reset) em tabela legível.

```bash
ccusage json
```
Mesma informação, em JSON — usado pelo `gerar-relatorio-consumo.py` e bom pra script.

```bash
ccusage refresh
```
Força buscar dado novo da API agora e atualiza o arquivo de cache local (ignora o cache existente).

```bash
ccusage daemon
```
Roda em loop no terminal, atualizando o cache periodicamente sozinho (deixar rodando em background/outra aba).

```bash
ccusage statusline
```
Lê stdin + cache e imprime uma linha compacta — pensado pra plugar como statusline do Claude Code.

```bash
ccusage install
```
Imprime as instruções de setup (ex.: como registrar a statusline no `settings.json` do Claude Code).

---

## ccusage (npm) — relatório de tokens/custo por período

> Comando `ccusage` puro está ocupado pela versão pip. Use sempre via `npx`.

### Comandos básicos (todos os agentes agregados)

```bash
npx ccusage@latest daily
```
Uso por dia, todos os CLIs de agente detectados juntos.

```bash
npx ccusage@latest monthly
```
Uso por mês.

```bash
npx ccusage@latest weekly
```
Uso por semana.

```bash
npx ccusage@latest session
```
Uso por sessão de conversa (1 linha por `session_id`).

```bash
npx ccusage@latest blocks
```
Uso por bloco de faturamento (janelas de 5h da Anthropic, por padrão).

```bash
npx ccusage@latest statusline
```
Status line compacta pra usar como hook do Claude Code.

### Filtrar por dia, mês ou intervalo específico

`--since`/`--until` funcionam em `daily`, `monthly`, `weekly`, `session` e
`blocks`, aceitando `YYYY-MM-DD` ou `YYYYMMDD` (inclusive nos dois limites).

```bash
npx ccusage@latest daily --since 2026-08-15 --until 2026-08-15
```
Um dia específico (15/08/2026).

```bash
npx ccusage@latest daily --since 2026-08-01 --until 2026-08-31
```
Um mês inteiro (agosto/2026), quebrado por dia.

```bash
npx ccusage@latest monthly --since 2026-01-01 --until 2026-12-31
```
Todo o ano, agrupado por mês.

```bash
npx ccusage@latest daily --since 2026-08-11 --until 2026-08-17
```
Uma semana específica (intervalo arbitrário de datas).

```bash
npx ccusage@latest daily --last 7
```
Últimos 7 dias (atalho, sem precisar calcular `--since`).

```bash
npx ccusage@latest monthly --last 3
```
Últimos 3 meses.

```bash
npx ccusage@latest weekly --last 4
```
Últimas 4 semanas.

### Sessão e blocos — filtros próprios

```bash
npx ccusage@latest session --id 3bdac6ed-12cd-4fa6-8520-cbe0bfa2ee84
```
Uma sessão específica pelo ID.

```bash
npx ccusage@latest blocks --active
```
Só o bloco de faturamento ATIVO agora, com projeção de custo.

```bash
npx ccusage@latest blocks --recent
```
Blocos dos últimos 3 dias (inclui o ativo).

```bash
npx ccusage@latest blocks --breakdown
```
Blocos com detalhamento de custo por modelo dentro de cada bloco.

```bash
npx ccusage@latest blocks --token-limit 500000
```
Blocos com aviso de quota ao passar de 500k tokens no bloco.

```bash
npx ccusage@latest blocks --session-length 8
```
Recalcula os blocos usando janelas de 8h em vez das 5h padrão.

### Saída, formatação e performance

```bash
npx ccusage@latest daily --json
```
Saída em JSON (pra script/pipe — é o que `gerar-relatorio-consumo.py` usa).

```bash
npx ccusage@latest daily --by-agent
```
Inclui detalhamento por agente dentro de cada linha (quando `--json`).

```bash
npx ccusage@latest daily --sections daily,monthly,session,blocks
```
Emite várias seções de uma vez, lendo os logs uma única vez (mais rápido que rodar os 4 comandos separados).

```bash
npx ccusage@latest daily --no-cost
```
Esconde a coluna de custo (só tokens).

```bash
npx ccusage@latest daily --breakdown
```
Detalhamento por modelo dentro de cada linha (`daily`/`monthly`/`weekly`/`session`).

```bash
npx ccusage@latest daily --order desc
```
Ordena do mais recente/caro pro mais antigo/barato (`blocks` e afins).

```bash
npx ccusage@latest daily --timezone America/Sao_Paulo
```
Agrupa os dias/semanas no fuso horário de Brasília em vez de UTC/local da máquina.

```bash
npx ccusage@latest daily --offline
```
Usa preço em cache em vez de buscar tabela de preços atualizada (mais rápido, útil sem internet).

```bash
npx ccusage@latest daily --compact
```
Tabela compacta (boa pra terminal estreito ou print/screenshot).

### Por agente específico (16 CLIs suportados)

Cada agente tem os mesmos subcomandos (`daily`/`monthly`/`weekly`/`session`/`blocks`) e aceita os mesmos filtros acima:

```bash
npx ccusage@latest claude daily
```
**Claude Code** (Anthropic) — o CLI oficial da Anthropic.

```bash
npx ccusage@latest codex daily
```
**Codex CLI** (OpenAI).

```bash
npx ccusage@latest opencode daily
```
**OpenCode** (sst/opencode) — o harness multi-modelo/multi-provedor.

```bash
npx ccusage@latest amp daily
```
**Amp** (Sourcegraph).

```bash
npx ccusage@latest droid daily
```
**Droid** (Factory AI).

```bash
npx ccusage@latest codebuff daily
```
**Codebuff**.

```bash
npx ccusage@latest hermes daily
```
**Hermes**.

```bash
npx ccusage@latest pi daily
```
**pi-agent**.

```bash
npx ccusage@latest goose daily
```
**Goose** (Block/Square).

```bash
npx ccusage@latest kilo daily
```
**Kilo Code**.

```bash
npx ccusage@latest copilot daily
```
**GitHub Copilot CLI**.

```bash
npx ccusage@latest gemini daily
```
**Gemini CLI** (Google).

```bash
npx ccusage@latest kimi daily
```
**Kimi** (Moonshot AI).

```bash
npx ccusage@latest qwen daily
```
**Qwen Code** (Alibaba).

```bash
npx ccusage@latest openclaw daily
```
**OpenClaw**.

```bash
npx ccusage@latest grok daily
```
**Grok Build CLI** (xAI).

### Extras exclusivos do `claude` (projeto/instância)

```bash
npx ccusage@latest claude daily --instances
```
Detalha o uso por projeto/instância do Claude Code.

```bash
npx ccusage@latest claude daily --project meu-projeto
```
Filtra pra um projeto específico.

```bash
npx ccusage@latest claude daily --project-aliases "ccusage=Fabrica de Livros,outro=Outro Projeto"
```
Renomeia os projetos na saída pra nomes mais legíveis.

```bash
npx ccusage@latest --help
```
Lista todos os comandos e agentes suportados.

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

Gera um relatório consolidado (rate limit de todos os provedores + uso
mensal/diário/sessão/blocos) em `rel-consumo/<rotulo>-consumo-cli[-<agente>].{md,pdf,xlsx}`
— o nome do arquivo reflete o filtro aplicado.

```bash
python scripts/gerar-relatorio-consumo.py
```
Padrão: todos os agentes, últimos 25 dias, nome do arquivo = data de hoje.

```bash
python scripts/gerar-relatorio-consumo.py --dia 2026-08-15
```
Relatório de 1 dia específico (sem valor = hoje: `--dia`).

```bash
python scripts/gerar-relatorio-consumo.py --mes 2026-08
```
Relatório de 1 mês inteiro.

```bash
python scripts/gerar-relatorio-consumo.py --semana 2026-08-20
```
Últimos 7 dias terminando na data informada (sem valor = hoje: `--semana`).

```bash
python scripts/gerar-relatorio-consumo.py --desde 2026-08-01 --ate 2026-08-31
```
Intervalo arbitrário de datas.

```bash
python scripts/gerar-relatorio-consumo.py --agente claude --mes 2026-08
```
Restringe a 1 agente específico (`--agente`), combinável com qualquer filtro de período.

```bash
python scripts/gerar-relatorio-consumo.py --secoes diario,blocos
```
Só as seções escolhidas, separadas por vírgula (opções: `mensal,diario,sessao,blocos`).

```bash
python scripts/gerar-relatorio-consumo.py --md-apenas
```
Gera só o `.md` (pula PDF e XLSX — mais rápido pra testar).

```bash
python scripts/gerar-relatorio-consumo.py --sem-rate-limit
```
Pula o rate limit da Anthropic (`ccusage` pip).

```bash
python scripts/gerar-relatorio-consumo.py --sem-outros-provedores
```
Pula a checagem dos outros 11 provedores (`verificar-rate-limits.py`) — deixa só o rate limit da Anthropic.

```bash
python scripts/gerar-relatorio-consumo.py --help
```
Lista todos os agentes suportados em `--agente`.

---

## Rate-limit multi-provedor (OpenRouter, OpenAI, Anthropic, Groq, HF, Cerebras, NVIDIA, Grok/xAI, ZenMux, Gemini, Cloudflare, OpenCode Zen)

Verifica rate-limit/quota atual de cada provedor configurado (via variável
de ambiente com a chave). Provedor sem chave configurada é pulado com aviso,
não trava o script.

```bash
python scripts/verificar-rate-limits.py
```

```bash
python scripts/verificar-rate-limits.py --json
```

Variáveis de ambiente (todas opcionais):

```
OPENROUTER_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY, GROQ_API_KEY,
HF_TOKEN, CEREBRAS_API_KEY, NVIDIA_API_KEY, XAI_API_KEY,
ZENMUX_MANAGEMENT_API_KEY (chave de MANAGEMENT do ZenMux, não a de inferência)
```

Cobertura por provedor:
- **Endpoint dedicado de quota** (dado estruturado): OpenRouter (`GET /api/v1/key`), Hugging Face (`GET /api/whoami-v2`, headers `RateLimit`/`RateLimit-Policy` padrão IETF)
- **Headers de rate-limit documentados oficialmente** (lidos via `GET /v1/models`): OpenAI (`x-ratelimit-*`), Anthropic (`anthropic-ratelimit-*`), Groq (`x-ratelimit-*`, igual OpenAI)
- **Best-effort** (compatível com OpenAI mas sem nomes de header confirmados — script captura qualquer header com `ratelimit` no nome): Cerebras, NVIDIA, Grok/xAI
- **Sem API pública de quota** (script reporta `indisponivel_via_api` + link do painel manual, sem tentar adivinhar): Google Gemini/AI Studio (quota é por projeto, não por chave), Cloudflare Workers AI (analytics existe mas não devolve neurons restantes), OpenCode Zen (sem doc de rate-limit)
- **ZenMux**: tem endpoint de saldo (`GET /api/v1/management/payg/balance`), mas exige uma Management API Key separada da chave normal de inferência (gerar em zenmux.ai console > Management)

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
- **`ccusage <agente> daily/monthly/session --json` tem schema diferente do
  unificado `ccusage daily/monthly/session --json`:** o relatório por-agente
  (ex.: `ccusage claude daily`) usa `date` em vez de `period` (daily/monthly),
  `sessionId` em vez de `period` (session), NÃO tem campo `agent` (já está
  implícito no comando), e o top-level de `session` vem como `sessions`
  (plural) em vez de `session` (singular) — reaproveitar o mapeador do
  unificado sem ajuste gerava `periodo=None`/`agente=nan` e a seção de
  sessões saía vazia, silenciosamente. Fix: `registros_para_df()` tenta
  `period or date or sessionId or id`, aceita um `agente_fallback` (nome do
  agente passado em `--agente`), e `extrair_lista()` tenta múltiplas chaves
  (`session`, `sessions`) antes de desistir. `blocks` por-agente usa o MESMO
  schema do unificado (id/costUSD/models/tokenCounts.\*) — não precisou de
  ajuste. Lição repetida: todo endpoint novo do `ccusage` precisa ter o JSON
  real inspecionado antes de reaproveitar um mapeador — "parece a mesma
  estrutura" não é o mesmo que "é a mesma estrutura".
- **Mesmo bug de largura de coluna (ver item anterior) apareceu de novo na
  tabela "Outros Provedores":** status `indisponivel_via_api` (20 chars) ao
  lado de uma coluna `detalhe` bem mais larga (URLs de painel) sobrepôs o
  texto de novo — o gatilho é sempre "1 coluna com string bem mais longa que
  as demais no mesmo eixo", não importa qual seção. Fix: rótulos curtos
  (`sem_chave`→"sem chave", `indisponivel_via_api`→"indisponível") +
  truncar `detalhe` a 70 chars na versão de impressão; texto completo
  continua no `.xlsx`. Regra consolidada: QUALQUER tabela nova indo pro
  PDF precisa passar pelo mesmo tratamento (contagem/truncamento em vez de
  texto livre), não só as tabelas de token/custo já existentes.
- **`ccusage blocks --json` tem schema diferente de daily/monthly/session:**
  usa `id`/`costUSD`/`models`/`tokenCounts.{inputTokens,outputTokens,
  cacheCreationInputTokens,cacheReadInputTokens}` em vez de `period`/
  `totalCost`/`modelsUsed`/campos soltos — reaproveitar o mapeamento genérico
  para blocks gerava `periodo=None`, `agente=nan`, `custo_usd=0`
  silenciosamente (sem erro, só dado errado). Fix: função dedicada
  `blocos_para_df()`. Lição: sempre inspecionar o JSON real de cada
  subcomando antes de reusar um mapeador entre eles.
