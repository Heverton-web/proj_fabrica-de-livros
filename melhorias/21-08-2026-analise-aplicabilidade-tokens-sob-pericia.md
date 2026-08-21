---
titulo: Análise de Aplicabilidade — Livro "Tokens Sob Perícia" na Fábrica Agêntica
data: 21-08-2026
fonte: output/otimizacao-tokens-ide-agentica/livros/otimizacao-tokens-ide-agentica/otimizacao-tokens-ide-agentica.pdf
---

# Análise de Aplicabilidade — "Tokens Sob Perícia"

## 1. Contexto e objetivo

O livro "Tokens Sob Perícia" (8 capítulos, produzido pela própria fábrica) audita um
manual de terceiros sobre economia de tokens em IDEs agênticas, aplicando um método
pericial: hierarquia de fontes classe A/B/C, quatro veredictos (CONFIRMADO,
PARCIALMENTE_CORRETO, FABRICADO, NÃO_VERIFICÁVEL) e um conjunto de técnicas de
engenharia que passaram na própria perícia sem ressalva (cache de prompt, paralelismo
controlado, circuit breaker, backoff exponencial, compressão de prompt, cache
semântico, orçamento/fallback).

Este relatório verifica, **contra o código real do projeto** (não de memória — seguindo
o próprio método do livro), quais desses conceitos/técnicas têm aplicação concreta na
Fábrica Agêntica de Publicações, por que valem a pena, e como implementar.

## 2. Metodologia

Antes de recomendar qualquer coisa, o código-fonte relevante foi lido:
`scripts/validar-fontes.py`, `scripts/hooks/pre-commit`, `scripts/minerar-fontes-academicas.py`,
`scripts/validar-referencias.py`, `scripts/fontes_academicas.py`,
`.claude/skills/calcular-gastos-sessao/SKILL.md` e `CLAUDE.md` (tamanho atual: 463
linhas / ~51.000 caracteres). As afirmações abaixo estão ancoradas nessa leitura —
quando o gap é real, cito o arquivo/linha; quando a prática já existe, digo isso
explicitamente em vez de "descobrir" um problema que não existe.

## 3. Oportunidades identificadas

### A. Gate de verificação de comandos/CLI citados em capítulos (novo)

**O que implementar:** um gate de conteúdo `validar-comandos-cli.py`, no mesmo
espírito de `validar-referencias.py` (R-RF) e `validar-fontes.py` (R-FT), que aplica
o classificador de evidência do Capítulo 1 (`Evidencia` → `classificar_fonte` →
CONFIRMADO/PARCIALMENTE_CORRETO/FABRICADO/NÃO_VERIFICÁVEL) a **blocos de código/CLI
citados em capítulos de livros sobre ferramentas técnicas** (DevOps, IA, frameworks —
exatamente o gênero que a fábrica já produziu: MCP, Agentic Design Patterns,
Autonomous DevOps, e este próprio "Tokens Sob Perícia").

**Por que:** é o achado central do livro — "ferramenta real, sintaxe fabricada" é o
erro mais perigoso porque o nome familiar desarma a checagem. A fábrica **já
produziu** um livro inteiro sobre esse risco; ironicamente, nenhum gate atual impede
que um *próximo* livro técnico da coleção repita o mesmo erro (nome de comando
correto, flag inventada). `validar-fontes.py` classifica a **classe da fonte no
dossiê**, mas não verifica se um comando citado no capítulo (ex.: `pipx install X`,
`--cache-prompts`, um caminho `~/.config/...`) bate com o que a fonte realmente
documenta. É uma lacuna de mérito exatamente do tipo que os gates F1/F2 existem para
fechar (R-AF já cobre "dado factual sem `[N]`"; este seria o análogo para "comando
sem confirmação de fonte primária").

**Como implementar:** ver plano de ação (Seção A).

### B. Circuit breaker de gasto — `token-guard` para sessões da fábrica

**O que implementar:** um script de orçamento diário (`scripts/token-guard.py` ou
`.sh`) que mede o gasto real via `npx ccusage@latest daily/session --json` (se o
Claude Code local gravar JSONL, o que deve ser confirmado no ambiente antes de
depender disso) e interrompe/alerta antes de estourar um teto configurável, com o
mesmo desenho de três estados (CLOSED/OPEN/HALF_OPEN) do Capítulo 5/6 do livro.

**Por que:** `CLAUDE.md` (regra 0) trata economia de tokens como "PRIORIDADE
MÁXIMA" e já existe a skill `calcular-gastos-sessao`, mas ela funciona por
**auto-relato**: cada agente precisa lembrar de appendar `tokens_in`/`tokens_out`
em `.agents/session-cost.jsonl` manualmente após cada ação — não há medição
independente que confirme o auto-relato. Um livro inteiro produzido nesta fábrica
(este mesmo) tem como tese central que auto-relato/documentação de memória diverge
da fonte primária. `ccusage` (quando aplicável ao ambiente) seria a "fonte primária"
de gasto, cross-checando o `.agents/session-cost.jsonl` em vez de confiar só nele.

**Como implementar:** ver plano de ação (Seção B). **Ressalva pericial**: a
existência de `ccusage` e o formato exato do JSONL do Claude Code precisam ser
confirmados no ambiente real (Windows + Claude Code local) antes de depender disso
em produção — não tratar como certo só porque o livro documenta.

### C. Resiliência de rede nos scripts de pesquisa/validação

**O que implementar:** aplicar semáforo (paralelismo controlado), backoff
exponencial com jitter, e opcionalmente um circuit breaker leve às chamadas HTTP de
`scripts/fontes_academicas.py` (`_http_get`, usada por `_fetch_openalex`,
`_fetch_crossref`, `_fetch_arxiv`, `_fetch_semantic_scholar`, `_fetch_scielo`,
`_fetch_pubmed`) e de `scripts/validar-referencias.py` (checagem de URL/DOI, linha
~107-115).

**Por que (confirmado no código):** `_http_get` (fontes_academicas.py:165) faz um
único `urlopen` com timeout fixo, sem retry — se uma API estiver com rate limit
momentâneo ou instável, a fonte inteira é descartada (`FonteIndisponivel`) mesmo
que uma segunda tentativa com espera curta resolvesse. As 6 fontes acadêmicas são
consultadas **sequencialmente**, uma por vez (`minerar-fontes-academicas.py:40`,
loop `for fonte in fontes`), o que é desnecessariamente lento quando não há
dependência entre elas. O mesmo padrão sequencial existe em
`validar-referencias.py` para dezenas de URLs por obra. Isso é exatamente o
Capítulo 5/6 do livro: paralelismo com teto de concorrência + backoff com jitter é
técnica que "passou na perícia sem ressalva" — não depende de nenhuma ferramenta
fabricada, só da biblioteca padrão (`asyncio`/`concurrent.futures`).

**Como implementar:** ver plano de ação (Seção C).

### D. Estabilidade de cache do CLAUDE.md (separar o RTK scratchpad)

**O que implementar:** mover a seção "RTK SCRATCHPAD" (que hoje cresce
indefinidamente, appended a cada sessão, dentro do próprio `CLAUDE.md`) para um
arquivo externo referenciado (ex.: `RTK-SCRATCHPAD.md`, citado por link/instrução
no `CLAUDE.md` principal), mantendo o corpo normativo do `CLAUDE.md` estável.

**Por que (confirmado):** `CLAUDE.md` tem hoje 463 linhas / ~51KB, e a seção RTK
SCRATCHPAD (que documenta aprendizados de sessões passadas) já responde por boa
parte disso e cresce a cada sessão nova. O Capítulo 2 do livro documenta, com fonte
primária da Anthropic, que o cache de prompt exige prefixo **byte-a-byte idêntico**
e que qualquer alteração no texto anterior a um ponto invalida o cache a partir
dali. Um arquivo que é lido automaticamente em toda sessão (`CLAUDE.md`) e que
recebe edições frequentes no meio/fim do documento é o cenário exato que o
Capítulo 2 descreve como "prefixo instável" — cada sessão nova paga reescrita de
cache para uma fração crescente do arquivo, além do próprio custo de tokens de
contexto que aumenta a cada entrada nova no scratchpad (o arquivo não tem teto).

**Como implementar:** ver plano de ação (Seção D).

### E. Blindagem de segredos no hook de pre-commit

**O que implementar:** estender `scripts/hooks/pre-commit` (fonte versionada) com
uma varredura de padrões de segredo (`sk-[a-zA-Z0-9_-]{20,}`, chaves privadas PEM,
`AKIA[0-9A-Z]{16}`, etc.) sobre o diff staged, bloqueando o commit se encontrar
algo — nos mesmos moldes do `blindar-commit.sh` do Capítulo 8.

**Por que (confirmado):** o `pre-commit` atual (lido integralmente) só roda
`pytest -q` (R16) e o `code-review-graph`; não há nenhuma varredura de segredo.
`CLAUDE.md` regra 10 determina auto-commit/push como parte do fluxo normal da
fábrica (não é uma ação manual revisada por humano a cada vez), e os scripts da
fábrica já lidam com credenciais reais em pelo menos um ponto documentado (chave de
API em templates de máquina de vendas, `.env` de backend). Auto-commit automático
sem grep de segredo é exatamente o cenário que o Capítulo 8 do livro trata como
lacuna de segurança básica antes de qualquer publicação de repositório.

**Como implementar:** ver plano de ação (Seção E).

### F. Validação positiva — não é gap, é confirmação

A hierarquia de fontes A/B/C que sustenta o método pericial do livro inteiro **já
está implementada corretamente** neste projeto, de forma independente, em
`scripts/validar-fontes.py` (R-FT-1/2/3, limiar de 70% A+B) — inclusive com a mesma
ideia de "não classificado não é sinônimo de aprovado" (R-FT-2: sem classificação
vira `nao_verificado`, não reprova, mas também não conta como aprovado). Não há ação
a tomar aqui além de **não duplicar** essa lógica ao implementar o item A — o novo
gate de comandos (A) deve reaproveitar as mesmas convenções de classe (A/B/C) e o
mesmo padrão de relatório JSON já usado por `validar-fontes.py`, para consistência
entre gates.

## 4. Itens do livro considerados e descartados (com justificativa)

| Técnica do livro | Por que NÃO priorizar agora |
|---|---|
| Cache semântico (GPTCache) para pesquisa | A mineração acadêmica já é "custo LLM zero" (APIs determinísticas + cache local via `--sem-rede`), documentado no `CLAUDE.md`. Cache semântico resolve reuso de *perguntas a um LLM*, não de chamadas a APIs REST determinísticas — não há LLM no caminho de `fontes_academicas.py`. |
| Compressão de prompt (LLMLingua) no RAG do dossiê | Risco real de cortar exatamente o token que sustenta uma citação `[N]` ou um trecho de código — o projeto tem gates estritos (R-AF, R-FT) que dependem de precisão textual. Aplicável só em modo conservador (rate 0.7-0.8) e nunca em blocos de código/citação; não é prioridade frente aos itens A-E. |
| Fallback para modelo local (Ollama/vLLM) | A fábrica roda com `model: inherit` sobre Claude Code — não há múltiplos provedores/gateway a gerenciar como no cenário do livro (OpenCode Zen, Hermes). Sem caso de uso imediato. |
| Versionamento de dotfiles (chezmoi) | Aplicável a ambiente pessoal do operador, não ao repositório do projeto (que já é versionado via Git). Fora de escopo. |
| Protocolo de verificação de catálogo de modelos (Cap. 3) | Não há catálogo de modelos gratuitos rotativo sendo consumido pela fábrica (regra R6 é `model: inherit`, sem seleção de modelo por nome). Não aplicável. |

## 5. Priorização sugerida (impacto x esforço)

| Item | Impacto | Esforço | Prioridade |
|---|---|---|---|
| E — Blindagem de segredos no pre-commit | Alto (risco de vazamento) | Baixo | **1 — imediato** |
| D — Separar RTK scratchpad do CLAUDE.md | Médio-alto (custo de contexto recorrente) | Baixo | **2 — curto prazo** |
| C — Resiliência de rede (pesquisa/validação) | Médio (robustez + velocidade) | Médio | **3 — curto prazo** |
| A — Gate de comandos/CLI (novo) | Alto (qualidade editorial, categoria de livros técnicos) | Médio-alto | **4 — médio prazo** |
| B — token-guard (circuit breaker de gasto) | Médio (depende de `ccusage` ser viável no ambiente) | Médio (+ verificação prévia) | **5 — médio prazo, condicional** |

O plano de ação detalhado para cada item está em
`melhorias/21-08-2026-plano-acao-tokens-sob-pericia.md`.
