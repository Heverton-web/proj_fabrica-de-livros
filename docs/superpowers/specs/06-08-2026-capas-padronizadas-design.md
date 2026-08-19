# Padronização de Capas — Livro e E-book

Data: 2026-08-06
Status: Aprovado (aguardando plano de implementação)

## 1. Problema

A geração de capas está fragmentada em 5 scripts com dimensões e estilos
divergentes, além de HTMLs bespoke feitos à mão por obra:

| Arquivo | Dimensão | Tecnologia | Observação |
|---|---|---|---|
| `scripts/gerar-capa-ebook-padrao.py` | 1200×1600 | Playwright/HTML | Único documentado na REGRA 5 (CLAUDE.md) hoje |
| `scripts/gerar-capa-ebooks.py` | 1600×2560 (1:1,6) | Pillow | Dimensão diferente da REGRA 5 |
| `scripts/testar_capa_marketing.py` | — | Playwright/HTML | Script de teste manual único, ad-hoc |
| `scripts/gerar_capas_demais_ebooks.py` | — | Playwright/HTML | `CONFIGS_SERIE` hardcoded (3 séries) |
| `scripts/sincronizar-capas-distribuicao.py` | — | — | Cópia para pasta de distribuição (fora do escopo de geração) |
| `output/livros/code-review-graph/capa.html` | 1200×1600 | HTML manual | Título em 3 linhas ("GRAPH" isolada) — viola a nova regra de linha |

Nenhum dos geradores produz a ilustração temática pedida, nenhum valida
quebra de linha de título/subtítulo, e a identidade de "série" (mesma cor
para obras relacionadas) só existe como dict hardcoded em 1 script.

## 2. Escopo

Aplica-se exclusivamente a **Livro** e **E-book**. TCC e Artigo Científico
mantêm a capa sóbria ABNT já existente (`template_tcc.typ`/`template_artigo.typ`)
— fora deste escopo.

## 3. Layout visual padrão

Fundo `#0d1117` (matte escuro, fixo, independente de obra/série), topo→base:

1. Faixa superior — 8px, cor de accent da obra/série
2. Chancela `>_ EDITORA AGÊNTICA` — ícone+texto CSS puro (sem arquivo de imagem), topo esquerda
3. Ilustração temática — PNG gerado pelo `subagente-ilustrador`, área central fixa
4. Título — branco (`#e6edf3`), Inter 900 72px, **máx. 2 linhas, nenhuma linha com 1 palavra só**, última palavra do título destacada na cor de accent (mesmo mecanismo do `.highlight` já usado no exemplo `code-review-graph`)
5. Subtítulo — Inter 300 18–24px, cinza `#8b949e`, **máx. 2 linhas, nenhuma linha com 1 palavra só**, objetivo (sem prolixidade)
6. Badge de Nível — **OBRIGATÓRIO (inegociável)**: pill com o nível da obra,
   derivado exclusivamente do campo `senioridade_obra` do `config_obra.json`
   (preenchido pelo `/esbocar` — nunca texto livre). Rótulos fixos:
   `iniciante` → "PARA INICIANTES", `intermediario`/`intermediário` →
   "NÍVEL INTERMEDIÁRIO", `avancado`/`avançado` → "NÍVEL AVANÇADO". Cor de
   accent. Ausência do campo ou do badge reprova a geração e a compilação.
7. Divider — faixa fina decorativa, cor de accent
8. Autor — **Heverton Eduardo Peres** (fixo, todas as capas)
9. Qualificação — **Especialista em Marketing e Desenvolvimento de Soluções** (fixo, todas as capas, substitui cargos variáveis como "Engenheiro de Software & Maker")
10. Faixa inferior — 6px, cor de accent

Dimensões: **1600×2263px** (livro, proporção A4) / **1200×1600px** (ebook) —
mantém exatamente os valores já documentados na REGRA 5 do `CLAUDE.md`.

Removido do padrão anterior: terminal à esquerda com comandos + código
flutuante à direita (itens e/f da REGRA 5 vigente antes desta spec).

## 4. Cor de accent e identidade de série

**Paleta curada** (consolida os hex já em uso hoje nos vários scripts):
`#2ecc9a #58a6ff #a855f7 #f0b429 #37c3d6 #f0933b #e05d5d #7c6cf0`

**Resolução da `serie_key`** de uma obra, em ordem de prioridade:
1. Campo `serie` explícito em `config_obra.json` (nome de coleção declarado pelo operador)
2. `slug_livro_mae` (ebook/artigo derivado herda a série do livro-mãe)
3. O próprio slug da obra (standalone)

**Cor:** se a `serie_key` já existe em `output/_series.json`, reusa a cor
registrada. Senão, escolhe deterministicamente (hash SHA-1 da `serie_key`)
uma cor da paleta curada e grava no registro. Isso garante que a mesma
série sempre produza a mesma cor (mesmo sem paleta explícita) e que refazer
a mesma obra não troque sua cor a cada execução.

**Registro `output/_series.json`** (raiz de `output/`, cross-tipo):
```json
{
  "<serie_key>": {
    "cor": "#58a6ff",
    "membros": ["livros/slug-a", "ebooks/slug-b--eb-01-titulo"]
  }
}
```
Semeado na migração inicial com as 3 séries já conhecidas hoje
(`ai-driven-development`: `#2ecc9a`, `marketing-na-era-digital`: `#f0933b`,
`sdlc-ai-first`: `#37c3d6`), preservando as cores atualmente em uso.

## 5. Schema — `config_obra.json`

Novo campo opcional:
```json
"serie": "<nome-da-serie> | null"
```
`null`/ausente = obra standalone (cor por hash do próprio slug) ou, se for
derivada (ebook/artigo), herda a série do livro-mãe via `slug_livro_mae`.

## 6. Fase 0 (`/esbocar`) — nova pergunta

Rodada 2 (condicional) ganha uma 4ª linha, dentro do limite de 4 opções do
`AskUserQuestion`:

| Header | Pergunta | Condição | Opções |
|---|---|---|---|
| Série | Esta obra faz parte de uma série/coleção? | sempre | Não, standalone (Recommended) \| Other (nome da série) |

## 7. Integração no pipeline de compilação

**Livro** — dentro do `compilador-abnt`, no mesmo Nó que hoje chama
`metadados_livro.py` (paleta/CIP/sinopse):
1. Invoca `subagente-ilustrador` → gera ilustração temática (PNG)
2. Invoca `scripts/gerar-capa.py --tipo livro` (resolve cor via
   `_series.json`, usa título/subtítulo derivados, embute a ilustração;
   aborta com erro fatal se `senioridade_obra` estiver ausente)
3. Invoca `scripts/validar-capa-texto.py` sobre título/subtítulo renderizado
4. Se reprovar (mais de 2 linhas ou linha de 1 palavra): encurta e tenta de
   novo (REGRA 4, máx. 3 tentativas — mesmo padrão de retry do pool de
   capítulos). Esgotadas as tentativas, segue com a melhor versão e registra
   não conformidade (REGRA 3, não trava a esteira).
5. Invoca `scripts/validar-capa-nivel.py` — **gate INEGOCIÁVEL**: reprovação
   (badge ausente ou incoerente com `senioridade_obra`) BLOQUEIA a compilação
   do PDF; o squad corrige o `config_obra.json`/regenera a capa (REGRA 4) e só
   então o PDF sai. A capa NUNCA entra no PDF fora do padrão.
6. Resultado grava `imagens/capa.png`, consumido pelo `template.typ` via
   o mecanismo `capa_imagem` que já existe.

**Ebook** — mesmo fluxo (passos 1-4), dentro do `subagente-adaptador-ebook`,
chamando `scripts/gerar-capa.py --tipo ebook`.

**Falha da ilustração:** se `subagente-ilustrador` falhar ou expirar, a
capa é gerada sem ilustração (área central vazia) em vez de travar a
esteira — registrado como não conformidade.

## 8. Validação determinística de texto

**Novo `scripts/validar-capa-texto.py`** — evidência determinística, mesmo
espírito de `validar-codigo.py`/`auditar-obra.py` (script decide, agente não
"julga" visualmente):
- Entrada: string de título ou subtítulo + fonte/peso/tamanho + largura da
  caixa de texto (derivada do layout: 1600/1200px menos padding lateral).
- Mede a largura real de cada palavra via Pillow `ImageFont` (fonte Inter
  local; fallback Arial se Inter não estiver instalada no sistema).
- Simula a quebra de linha exatamente como o CSS faria (greedy wrap).
- Reprova se: mais de 2 linhas, OU qualquer linha resultante com exatamente
  1 palavra.
- Modo standalone (`--validar --texto "..."`) e função importável, chamada
  automaticamente pelo gerador antes de renderizar a versão final.

**Novo `scripts/validar-capa-nivel.py`** — gate do badge de nível:
- Lê `senioridade_obra` de `config_obra.json` e o `<div class="badge">` do
  `capa.html` renderizado.
- Aprova somente se o badge for exatamente o rótulo fixo do nível (ex.:
  `senioridade_obra=iniciante` ⇒ badge "PARA INICIANTES").
- Reprova: obra sem o campo, nível inválido, badge ausente ou divergente.
- Reprovação bloqueia a compilação do PDF (chamado pela cadeia de capa).

## 9. Consolidação de arquivos

| Arquivo | Ação |
|---|---|
| `scripts/gerar-capa-ebook-padrao.py` | Renomeado → `scripts/gerar-capa.py`. Ganha `--tipo livro\|ebook`, fontes locais (`'Inter', Arial, sans-serif` — remove `@import` do Google Fonts, elimina dependência de rede em lote), integração com ilustração e com `_series.json` |
| `scripts/gerar-capa-ebooks.py` | **Removido** (Pillow, dimensão 1:1,6 divergente) |
| `scripts/testar_capa_marketing.py` | **Removido** (script de teste manual único) |
| `scripts/gerar_capas_demais_ebooks.py` | **Removido** (`CONFIGS_SERIE` migra para `output/_series.json`) |
| `scripts/sincronizar-capas-distribuicao.py` | Mantido sem mudança |
| `scripts/validar-capa-texto.py` | **Novo** |
| `scripts/validar-capa-nivel.py` | **Novo** — gate do badge de nível (REGRA 5/Capa, item h) |
| `output/_series.json` | **Novo**, semeado com as 3 séries já em uso |
| `output/livros/code-review-graph/capa.html` e demais bespoke | Regenerados via `scripts/gerar-capa.py --todos` |
| `CLAUDE.md` REGRA 5 (+ 6 espelhos: `AGENTS.md`, `.clinerules`, `.windsurfrules`, `.windsurf/rules/fabrica-agentica.md`, `.cursor/rules/fabrica-agentica.mdc`, `.github/copilot-instructions.md`) | Reescrita: remove itens de terminal/código, adiciona ilustração temática, badge, qualificação fixa, campo `serie`, registro `_series.json` |

## 10. Migração das capas existentes

`scripts/gerar-capa.py --todos` varre `output/livros/*/config_obra.json` e
`output/ebooks/*/config_obra.json`, resolve `serie_key` de cada, popula
`output/_series.json` e regenera `imagens/capa.png` de todas as obras
existentes no padrão novo — incluindo a correção do título de 3 linhas do
`code-review-graph`.

## 11. Plano de teste

- Rodar `gerar-capa.py --todos` sobre o `output/` real; inspecionar
  visualmente ao menos 3 PNGs resultantes (1 livro, 1 ebook standalone, 1
  par mãe+derivado de série) antes de considerar concluído.
- Testar `validar-capa-texto.py` com títulos propositalmente inválidos (3
  linhas; linha de 1 palavra) para confirmar que reprova corretamente, e com
  títulos válidos para confirmar que aprova.

## 12. Decisões registradas (não re-abrir sem novo pedido explícito)

- Fundo fixo `#0d1117` sempre, independente de accent/série.
- Logo = ícone+texto CSS atual (`>_ EDITORA AGÊNTICA`), sem arquivo de imagem.
- Dimensões mantidas: 1600×2263 (livro) / 1200×1600 (ebook) — descarta a
  proporção 1:1,6 do script Pillow removido.
- **Badge de nível OBRIGATÓRIO** (inegociável): derivado exclusivamente de
  `config_obra.json.senioridade_obra` — rótulos fixos: `iniciante`→
  "PARA INICIANTES", `intermediario`→"NÍVEL INTERMEDIÁRIO", `avancado`→
  "NÍVEL AVANÇADO". Ausência do campo = erro fatal na geração e gate de
  validação (`validar-capa-nivel.py`) que BLOQUEIA a compilação do PDF.
- Qualificação do autor é fixa em 100% das capas, sem exceção por tema.
- Escopo restrito a Livro e E-book; TCC/Artigo fora.
