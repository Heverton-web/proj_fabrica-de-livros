# LLM vs. Determinismo — Onde a Fábrica Já Acertou e Onde Ainda Sobra Probabilidade Evitável

> Data: 2026-08-14 · Escopo: pipeline completo (Fases 0-3 editorial, materiais
> derivados V5, campanha V5.3, máquina de vendas) · Método: 3 auditorias
> paralelas sobre o código-fonte real (skills, subagentes, scripts).

## 1. Contexto e critério de análise

A fábrica já aplica o princípio "cascateie onde comprime, gere onde expande"
(CLAUDE.md §1) e tem exemplos maduros de conversão LLM→script: `validar-*.py`
(achar problema), `minerar-fontes-academicas.py` (pesquisa via API aberta,
custo zero), `extrair-passos-praticos.py`/`gerar-lead-magnet.py`/`gerar-deck.py`
(extração pura). Este relatório busca **o próximo lote** de etapas que hoje
ainda chamam LLM mas seguem regra fixa o suficiente para virar script/config/
template — e marca explicitamente o que **não** deve ser tocado.

Critério usado em cada item: (a) o que é hoje uma chamada de LLM, (b) o que
dessa tarefa é mecânico vs. o que exige julgamento editorial, (c) precedente
no próprio repositório que prova o padrão, (d) risco de determinizar demais.

## 2. Pipeline editorial (Fases 0-3)

| # | Etapa | Hoje (LLM) | Determinizar como | Precedente no repo |
|---|---|---|---|---|
| 1 | Esqueleto macro P/M/G (`arquiteto`) | LLM lê tabela de tamanhos **duplicada em prosa** no SKILL.md e decide nº de partes/capítulos | Script gera `sumario_macro.json` com N partes/capítulos vazios chamando `parametros_obra.minimos_livro(tamanho)`; LLM só preenche título/objetivo/motivo condutor/persona | `scripts/parametros_obra.py` já é fonte única — falta o arquiteto consumi-la em vez de reler a cópia solta |
| 2 | Correções mecânicas do `revisor-tecnico` | LLM reescreve capítulo para corrigir `---` solto (R9), citação `[N]` órfã (R14), grafia inconsistente | `corrigir-mecanico.py`: remove `^---$`, renumera `[N]` órfão sequencialmente, canonicaliza grafia pela forma mais frequente | `auditar-obra.py` já **localiza** exatamente linha/capítulo — falta fechar "achar→corrigir" para os subtipos sem ambiguidade |
| 3 | Dedup de referências (`compilador-abnt`) | Instrução em linguagem natural: "elimine duplicatas por URL normalizada" | Função Python de normalização de URL + set (fallback DOI/título via `fontes_academicas.py`), executada antes do merge | Zero julgamento — é string matching |
| 4 | Classificação de fonte A/B/C (pesquisador) | LLM decide "(A)/(B)/(C)" na hora de escrever o dossiê | Classificador por domínio/tipo (`arxiv.org`→A, `.gov`/RFC→B, blog→C); LLM só resolve casos ambíguos | Complementa `validar-fontes.py` (gate R-FT já mede ≥70% A+B) |
| 5 | Esqueleto de seções EITA/ACAD (`redator-eita`) | LLM recria os 7 cabeçalhos numerados a cada capítulo — risco documentado de heading malformado quebrar `validar-escala`/`validar-metricas` | Script gera `.md` com os 7 headers fixos + checklist vazio (`- [ ]`); LLM só escreve dentro de cada seção | `templates/template_eita.md` + `scripts/secoes_eita.py` já definem a estrutura canônica |

**Fora de escopo (confirmado):** decomposição de pilares (`estrategista`),
prosa transformacional do redator, resolução de overlap semântico e correção
de dados factuais divergentes — exigem julgamento editorial genuíno.

**Pesquisa (Fase 1):** já parcialmente convertida (`minerar-fontes-academicas.py`,
5 APIs, custo zero). O que resta 100% LLM é a *seleção* de relevância em bases
sem API — isso é, por natureza, probabilístico e não deve ser determinizado;
só a *classificação* pós-seleção (item 4) é candidata real.

## 3. Materiais derivados V5

| Material | Situação | Ação |
|---|---|---|
| Playbook | **100% script**, confirmado (`extrair-passos-praticos.py` linha 7 declara "nenhuma chamada de LLM") | Nenhuma — referência positiva |
| Deck | **100% script**, confirmado (`gerar-deck.py` linha 5) | Nenhuma |
| Lead Magnet | **~100% script** — 1 marcador `POLIMENTO-LLM` residual só no formato "mini-guia" (2 parágrafos de contexto), com gate próprio (`validar-lead-magnet.py`) | Já é o padrão-alvo: marcador explícito + gate que reprova se ficar pendente |
| E-mails (declarado "baixo") | Esqueleto 100% script (`gerar-sequencia-emails.py`), mas injeta **3 marcadores `POLIMENTO-LLM`** por sequência pedindo 1-2 frases de ligação (ex.: "lembrando a promessa do lead magnet") | Banco de 5-10 variações de frase de ligação por posição, interpoladas por template com hash do slug (mesmo padrão de rodízio do lead magnet) — elimina as 3 chamadas de LLM por sequência. Risco: texto mais repetitivo entre sequências — validar A/B antes de eliminar 100% |
| E-book (compressão) | Não é mecânico no geral (reescrita de tom real), mas a **conversão de citação `[N]` → atribuição narrativa** ("Segundo {autor}") é 100% resolvível puxando o autor do `.bib`/referências já estruturadas | Pré-processador que resolve `[N]`→autor antes de entregar o capítulo ao redator; reduz a carga da LLM só ao encurtamento de estilo |
| Artigo/Resumo (IMRaD) | Síntese analítica real — não mecânico | Resumo/abstract é candidato de *baixa prioridade* (sumarização extrativa determinística arriscaria qualidade acadêmica) — não recomendado agora |

## 4. Campanha (V5.3) e Máquina de Vendas

| # | Etapa | Hoje (LLM) | Determinizar como | Risco/limite |
|---|---|---|---|---|
| 1 | Rascunho de copy (`escrever_moldes`) | Rascunho já é 100% determinístico (`_rascunho`, monta de vocabulário/CTA/manifesto), mas o cabeçalho **sempre** grava `Status: RASCUNHO — reescreva com LLM`, forçando LLM mesmo quando o texto já basta | Script decide aprovação por heurística objetiva (tamanho mínimo, `{cta}`+`cta_url` presentes, vocabulário citado, sem placeholder); se passar, grava `Status: FINAL (auto-aprovado determinístico)` sem chamar LLM | `ads_pago`/`distribuicao_semeadura` ainda são `[TEXTO DO ANUNCIO]` puro — sempre vão exigir LLM (ou ganhar rascunho real primeiro) |
| 2 | Gate R-CP-2 | Regex só checa se a string "Status: RASCUNHO" ainda existe — não avalia qualidade, depende de convenção textual apagada manualmente | Gate objetivo (tamanho, CTA+URL, vocabulário do manifesto, sem placeholder) substitui a convenção textual e destrava o item 1 | — |
| 3 | Ganchos/artes (`ganchos_arte`) | Já 100% determinístico (deriva de `sumario_macro.json`) | Nenhuma — referência positiva, padrão a replicar nos itens 1 e 4 | — |
| 4 | Personalização por nicho da máquina | `copiar_template` só troca placeholders óbvios (nome/título/slug); a personalização real (dores, objeções, termos por segmento) é 100% livre por agente, checada só reativamente pelo gate regra 12 (grep) | Banco declarativo `config/nichos/<segmento>.json` (dores, personas, termos, objeções, ganchos) alimentado pelas tags já extraídas do manifesto; script aplica em todos os pontos (configs+frontend+e-mails+campanhas+README); LLM só entra quando o nicho não bate com o banco ou para o refino final de tom | Copy persuasiva de nicho não deve ficar 100% template — o banco cobre esqueleto/termos, não a frase de gancho final |
| 5 | Gate regra 12 | Só reprova string genérica exata ("Autor Digital") — substituir por qualquer string aleatória passa o gate | Gate adicional: exigir presença de termos do vocabulário do nicho/manifesto nas páginas centrais (landing, checkout, e-mails) | Fortalece o item 4 sem precisar de releitura por LLM |

## 5. Priorização recomendada

1. **Alto impacto / baixo risco (fazer primeiro):** itens 2, 3 e 5 do pipeline
   editorial (dedup de referências, classificação A/B/C, esqueleto EITA) —
   zero julgamento envolvido, precedente já existe no repo.
2. **Médio impacto:** rascunho auto-aprovado de campanha (itens 1-2 da seção 4)
   — reduz chamadas de LLM por material sem tocar na qualidade de copy que já
   passa no gate.
3. **Médio impacto, precisa de dado novo:** banco de nichos da máquina de
   vendas (item 4) — exige levantar o conteúdo do banco antes de valer a pena.
4. **Baixa prioridade / risco de regressão de qualidade:** frases de ligação
   de e-mail (testar A/B antes), resumo/abstract de artigo (não recomendado
   agora), correção de overlap semântico e dados factuais divergentes do
   revisor-tecnico (manter como LLM).

## 6. O que nunca deve virar regra fixa

Decomposição de pilares do `estrategista`, prosa transformacional dos
redatores, resolução de sobreposição semântica entre capítulos, correção de
divergência factual (exige reler a fonte), seleção de relevância de fontes de
pesquisa em bases sem API, e a frase de gancho final de qualquer copy
persuasiva — todos exigem julgamento que uma regra fixa substitui com perda
de qualidade.
