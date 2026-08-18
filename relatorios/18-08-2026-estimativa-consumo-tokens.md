# Relatório de Sessão — Estimativa de Consumo de Tokens de um Turno Completo

- **Data:** 18-08-2026
- **Tema:** Estimativa de consumo de tokens e custo de um turno completo da Fábrica Agêntica de Publicações
- **Método:** Análise do fluxo operacional (AGENTS.md), tamanhos contratados de obra (`parametros_obra.py`), tamanho real dos prompts dos subagentes (`.claude/agents/*.md`) e dados históricos do RTK Scratchpad. Sem medição real por sessão — estimativa por fase.

## 1. Contexto

A fábrica produz coleções completas (livro + derivados + campanha + máquina) via
orquestrador + subagentes especializados + scripts determinísticos. Pergunta do
operador: quanto uma produção FULL consome de tokens?

## 2. Parâmetros adotados

- **Obra base:** livro tamanho M (padrão) — 8 capítulos, 200.000 caracteres (`TAMANHOS` em `parametros_obra.py`).
- **Coleção:** ~12 materiais (livro, playbook, lead magnets, decks, e-mails, derivados).
- **Ratio PT-BR:** ~3,5–4 caracteres por token → capítulo M (~25k chars) ≈ 6–7k tokens de output.
- **Retentativa média:** ~1,3× por capítulo (máx. 3 tentativas, backoff no `pool-capitulos.py`).
- **Modelo:** indefinido (`model: inherit`) — custo calculado por faixa de preço.

## 3. Estimativa por fase

| Fase | LLM | Input | Output | Total |
|---|---|---|---|---|
| Pesquisa (pesquisador + arquiteto) | alto | ~200k | ~30k | ~230k |
| Estratégia (drafts × 8 caps) | médio | ~400k | ~40k | ~440k |
| Redação (subagentes × 8, c/ retentativa) | alto | ~3–4M | ~350k | ~3,5–4,5M |
| Revisão técnica (revisor-tecnico) | médio | ~600k–1M | ~100–200k | ~700k–1,2M |
| Compilação ABNT (merge + refs + prefácio) | médio | ~300–600k | ~50–100k | ~350–700k |
| Derivados (ebooks/artigos/TCC) | médio | ~500k–1M | ~150–300k | ~650k–1,3M |
| Campanha (copy dos moldes, 12 materiais) | baixo | ~300–600k | ~100–200k | ~400–800k |
| Máquina de vendas (personalização) | baixo–médio | ~150–300k | ~50–100k | ~200–400k |
| Playbook / LM / Deck / E-mails / mineração / auditorias / PDF | **zero** (determinístico) | — | — | 0 |
| Orquestração (roteador, leituras, QA) | variável | ~500k–1,5M | ~100–300k | ~600k–1,8M |

## 4. Totais

- **Coleção M típica: ~7–11M tokens** (input + output)
- Coleção P enxuta: ~4–5M
- G/GG ou retentativas altas: ~12–20M

### Custo estimado (modelo da sessão)

| Modelo | 10M in + 1,5M out | BRL (câmbio 5,5) |
|---|---|---|
| Fallback Sonnet 4 ($3/$15) | ~US$ 52 | ~R$ 290 |
| DeepSeek V3 ($0,5/$2) | ~US$ 8 | ~R$ 45 |
| Modelo free (ex.: roteador free) | — | R$ 0 |

## 5. Onde o peso morre

1. **Redação de capítulos ≈ 55–60%** — subagente multi-turno re-envia contexto (dossiê RAG + draft + skill) a cada turno; input ≫ output (~10:1).
2. **Orquestração ≈ 15–20%** — pior quando o operador acompanha turno a turno.
3. **Retentativas** — cada falha re-spawna o contexto inteiro do subagente.

## 6. Redutores já ativos

- `pool-capitulos.py` — lote 4 + backoff exponencial limita re-spawn em paralelo.
- Stack token-economy (LeanCTX, Headroom, Cavecrew) — corta reenvio de logs/contexto.
- Fases determinísticas isentam ~30% do fluxo (custos LLM zero).
- RTK Scratchpad — evita re-análise de bugs já resolvidos.

## 7. Conclusão

Turno completo M ≈ **7–11M tokens**; custo de R$ 45 a R$ 290 conforme o modelo
(ou R$ 0 em modelo free). Metade do consumo é input repetido na redação de
capítulos — alavanca principal de redução é o tamanho/lote do contexto dos
subagentes-redator, não o modelo.

## 8. Validação

- Nenhum código alterado nesta sessão — apenas relatório e compilação PDF.
- Suíte de testes: não aplicável (sem mudança em código).
- Compilação PDF verificada (cabeçalho `%PDF` + tamanho não-zero).

## 9. Arquivos

- `relatorios/18-08--estimativa-consumo-tokens.md`
- `relatorios/18-08--estimativa-consumo-tokens.pdf`