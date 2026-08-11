# Artes de Campanha Únicas por Envio (R-CP-6)

> Data: 2026-08-10 · Camada: CAMPANHA (V5.3) · Escopo: `scripts/campanha.py`,
> `scripts/criar-campanha.py`, `templates/campanha/*.html`,
> `scripts/validar-campanha.py`, `tests/test_campanha.py`

## Problema

As artes (PNG) de campanha eram **a mesma imagem repetida** em todos os envios
da sequência/cronograma. O conceito esperado: **1 arte = 1 envio**, com copy
própria (título curto de break scroll + apoio) seguindo a sequência de envios.

Evidências (MD5 idênticos na campanha de `spec-driven-development`):

- `redes-sociais/instagram/artes/post/post-01..07.png` → mesmo hash `f5d29f98…`
- `redes-sociais/instagram/artes/feed-story/story-01..07.png` → mesmo hash `84188b7a…`
- `canais-comunicacao/whatsapp/*/artes/arte-01..06.png` → mesmo hash `35879491…`
- No total: **62 PNGs, apenas 8 MD5 únicos**.

## Causa raiz (3 bugs encadeados)

1. **WhatsApp — HTML interpolado 1× fora do loop** (`gerar_artes` em
   `scripts/criar-campanha.py`):

   ```python
   html = _interpolar_arte(CP.TEMPLATES_ARTE["whatsapp"], ctx)   # 1x só
   for i in range(1, quantidade + 1):
       destino.write_text(html, ...)   # o MESMO html em arte-01..arte-06
   ```

2. **Posts/Stories — "variação" é só `(i/n)` colado ao título e cortado**:

   ```python
   ctx_variado["titulo_arte"] = f"{ctx['titulo']}"       # mesmo título p/ todas
   ctx_variado["sufixo_arte"] = f"({i}/{quantidade})"    # "(1/7)" ...
   return {"TITULO": titulo[:64], ...}                    # ...cortado nos 64 chars
   ```

   Todas as artes mostram o título do material; o sufixo `(1/7)` cai fora do
   `[:64]` (título longo) ou vira texto invisível.

3. **Validador só conta quantidade, nunca unicidade** (`validar-campanha.py`,
   gate R-CP-3): `len(dir_artes.glob("*.png")) >= esperado` aprova mesmo com
   artes duplicadas → a campanha "validava 100%" com 31 artes idênticas.

## Mudanças implementadas

### 1. `scripts/campanha.py` — derivação determinística de ganchos

- `ganchos_arte(ctx, formato, n, base=None)` → `[{titulo, apoio}]` por envio.
- Fonte primária: títulos de capítulos + `objetivo` + `pilares_previstos` do
  `sumario_macro` do material (post prioriza capítulos; story/whatsapp
  priorizam pilares como dica curta).
- Gancho ≤ 70 chars (break scroll); `apoio` ≤ 90 chars (1 linha).
- Fallback determinístico: `GANCHO_FALLBACK` (moldes com o tema da obra),
  preservando o `?` final dos ganchos de pergunta.
- `_limpar_gancho` corta em palavra completa e preserva a interrogação final.

### 2. `scripts/criar-campanha.py` — corrigir `gerar_artes`

- WhatsApp: `_interpolar_arte` **dentro do loop** → 1 HTML distinto por envio.
- Posts/Stories: `titulo_arte` = gancho[i] (curto), `apoio_arte` = apoio[i],
  `rotulo_arte` = "Post 3/7" / "Story 2/7" / "Mensagem 4/6" como **elemento
  separado** (nunca colado/cortado do título).
- `variaveis_arte`: expõe `ROTULO` e `APOIO` (novos); `SUBTITULO` mantido por
  retrocompatibilidade.

### 3. `templates/campanha/*.html` (4 arquivos)

- Novo elemento `.rotulo` (progresso: "Post 3 de 7" / "Mensagem 2 de 6"),
  discreto e centralizado no cabeçalho.
- `.subtitulo` agora renderiza `${APOIO}` (linha de apoio do envio).
- Título grande permanece (já é break scroll).

### 4. `scripts/validar-campanha.py` — gate R-CP-6 (artes únicas)

- `_artes_duplicadas(dir_artes)` → PNGs repetidos (MD5) e HTMLs fonte
  repetidos dentro de um formato/sequência.
- Aplicado a cada formato de rede e cada sequência de WhatsApp: 2+ PNGs
  idênticos → REPROVA listando os duplicados.

### 5. `scripts/campanha.py` — desambiguação do `nome_material` (extra)

Bug real descoberto ao regenerar: `nome_material` corta o nome do diretório
nas 2 primeiras palavras (`nome_curto(max_palavras=2, maximo=20)`) e
`spec-driven-development--eb-01-…` virava `spec-driven` — **a campanha dos
2 e-books caía na mesma pasta do livro**, sobrescrevendo moldes e artes.

Fix: remove o prefixo da chave da coleção (com separador explícito `--`/`-`)
antes do `nome_curto` → e-books ganham pastas próprias `eb-01`, `eb-02`.
Sem separador não trunca (material que apenas compartilha prefixo com a chave
não é afetado).

## Testes (`tests/test_campanha.py`)

- `TestGanchosArte` (7): quantidade, título ≤ 70, priorização por formato,
  unicidade quando fonte suficiente, ciclagem sem quebra, fallback com tema,
  determinismo.
- `test_artes_png_unicos_por_formato`: render mock (PNG = hash do HTML) →
  nenhum PNG repetido por formato/sequência.
- `test_artes_html_fonte_distintos_e_titulo_curto`: 7 ganchos distintos, com
  rótulo de progresso e título curto no HTML fonte.
- `test_artes_whatsapp_interpola_html_dentro_do_loop`: 6 copies distintas +
  rótulos `1/6..6/6` (regressão do bug original).
- Gate R-CP-6 (3): aprova artes únicas; reprova PNG repetido; reprova HTML
  fonte repetido.
- `test_nome_material_desambiguado_da_colecao`: livro/eb-01/eb-02 sem colisão.

## Resultado na campanha do SDD (regenerada)

- 12 materiais × 31 artes = **372 PNGs, 0 grupos com duplicata**.
- E-books com campanhas próprias (`campanhas/eb-01`, `campanhas/eb-02`).
- Ganchos reais (livro): Post 1/7 "Por que especificar antes de codificar"
  (apoio: "O problema do código como única fonte de verdade"); Post 7/7 "O
  canteiro de ferramentas do SDD"; WhatsApp 1/6 "O problema do código como
  única fonte de verdade".
- `validar-campanha --material <livro>`: só R-CP-2 (molde RASCUNHO pendente —
  copy final é escrita pelo agente depois); **sem R-CP-3 nem R-CP-6**.

## Validação (critérios de aceite)

1. ✅ 372 artes do SDD com MD5 distintos dentro de cada formato/sequência.
2. ✅ Título de cada arte ≤ 70 chars e presente no HTML fonte.
3. ✅ Gate R-CP-6 reprova artes duplicadas (teste unitário).
4. ✅ `pytest -q` completo = **652/652 verde**.
5. ✅ Campanha regenerada; validador sem violações de artes (R-CP-3/R-CP-6).
