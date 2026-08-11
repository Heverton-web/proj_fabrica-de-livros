# Relatório de Sessão — Artes de Campanha Únicas por Envio (R-CP-6)

> Data: 2026-08-10 · Fábrica Agêntica · Camada CAMPANHA (V5.3)

## Contexto

O operador reportou um bug grave: as artes (PNG) da campanha do livro
`spec-driven-development` eram **a mesma imagem repetida** em todos os envios,
quando o conceito é **1 arte = 1 envio** (copy própria por envio, com título
curto de break scroll seguindo a sequência/cronograma). Antes de implementar,
foi apresentado o plano de mudanças ao operador, que aprovou com a ordem:
salvar o plano em `melhorias/` (MD + PDF), implementar uma etapa por vez com
testes a cada etapa, e ao final commit + push + regenerar toda a campanha.

## Bugs descobertos e corrigidos (causa → fix)

1. **WhatsApp com HTML interpolado 1× fora do loop** (`gerar_artes`):
   `_interpolar_arte` era chamado antes do `for`, gravando o MESMO html em
   `arte-01..06` (MD5 idêntico `35879491…`).
   → Fix: interpolar **dentro do loop**, com gancho/apoio/rótulo por envio.

2. **Posts/Stories com "variação" inócua**: `titulo_arte` repetia o título do
   material e o sufixo `(i/n)` era cortado pelo `[:64]` — post-01..07 e
   story-01..07 com MD5 idênticos.
   → Fix: `titulo_arte` = gancho curto (≤ 70 chars), `apoio_arte` = apoio,
   `rotulo_arte` = "Post 3/7" como elemento separado.

3. **Validador só contava quantidade** (R-CP-3), nunca unicidade — artes
   duplicadas "validavam 100%".
   → Fix: novo gate **R-CP-6** (PNGs repetidos por MD5 + HTML fonte repetido).

4. **`nome_material` colidia com o prefixo da coleção** (extra, descoberto ao
   regenerar): `spec-driven-development--eb-01-…` cortava para `spec-driven`
   → campanhas dos 2 e-books caíam na pasta do livro, sobrescrevendo moldes.
   → Fix: remover o prefixo da chave da coleção (com separador `--`/`-`)
   antes do `nome_curto` → pastas próprias `eb-01`, `eb-02`.

## Arquivos alterados

- `scripts/campanha.py` — `ganchos_arte`, `_temas_por_formato`,
  `_limpar_gancho`, `GANCHO_FALLBACK`, `nome_material` (desambiguação).
- `scripts/criar-campanha.py` — `variaveis_arte` (ROTULO/APOIO), `gerar_artes`
  (HTML por envio, WhatsApp dentro do loop).
- `templates/campanha/arte-post-ig.html`, `arte-feed-story-ig.html`,
  `arte-post-linkedin.html`, `arte-whatsapp.html` — `.rotulo` + `${APOIO}`.
- `scripts/validar-campanha.py` — gate R-CP-6 + `_artes_duplicadas`.
- `tests/test_campanha.py` — 12 testes novos/ajustados.
- `melhorias/2026-08-10-artes-campanha-unicas-por-envio.md` + `.pdf` (plano).

## Validações rodadas

- `pytest tests/test_campanha.py` → 51/51 (suíte de campanha).
- `pytest tests/test_campanha.py tests/test_nomes_e_pacote.py` → 115/115.
- **Suíte completa `pytest -q` → 652/652 verde** (antes e depois do review).
- Review técnico independente (`code-reviewer-deepseek-flash`): 4 pontos
  corrigidos (branch `startswith` sem separador, `?` do fallback, isolamento
  de teste, `base` param em `ganchos_arte`).

## Campanha do SDD regenerada

- 12 materiais × 31 artes = **372 PNGs, 0 grupos com duplicata** (MD5).
- E-books com campanhas próprias (`campanhas/eb-01`, `campanhas/eb-02`).
- `validar-campanha --material <livro>`: sem R-CP-3/R-CP-6 (só R-CP-2 molde
  RASCUNHO — copy final é escrita pelo agente depois).

## Commits

- (a registrar no commit da sessão)

## Resumo de entregas

Correção estrutural da camada de artes de campanha com validação automática
(R-CP-6), testes 100% verdes e campanha do SDD totalmente regenerada com copy
única por envio.
