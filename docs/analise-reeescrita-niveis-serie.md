# Análise: Reescrita por Nível de Senioridade e Criação de Séries

> **Data:** 2026-08-07 | **Versão:** 1.0
> **Objeto:** Avaliar se o fluxo atual da Fábrica Agêntica suporta reescrever um livro para níveis diferentes e criar séries com elevação de nível a partir de uma mesma obra-base.

---

## 1. Diagnóstico do Estado Atual

### 1.1 O que JÁ existe

| Mecanismo | Status | Onde | Reaproveitamento |
|-----------|--------|------|------------------|
| **Matriz EITA por senioridade** | Planejado (não implementado) | `docs/plano-adaptacao-metodo-eita-senioridade.md` | — |
| **Derivação de E-books** | Implementado e operacional | `SPEC_EBOOK.md`, `redator-ebook`, `subagente-adaptador-ebook`, `fatiar-obra.py` | Reescreve tom a partir de capítulos já prontos (sem nova pesquisa) |
| **Derivação de Artigos** | Implementado e operacional | `SPEC_ARTIGO.md`, `fatiar-obra.py --artigos` | Fatia livro-mãe em artigos IMRaD |
| **Manifesto de derivados** | Implementado | `output/livros/<slug>/derivados.json` | Rastreia ebooks e artigos derivados |
| **RAG local do dossiê** | Implementado | `indexar-dossie.py` (TF-IDF puro) | Permite consultas sem reindexar |
| **Índice RAG persistido** | Implementado | `output/<slug>/pesquisa/indice_dossie.json` | Reutilizável entre sessões |
| **`config_obra.json` com `senioridade_obra`** | Planejado (não implementado) | `parametros_obra.py` | — |

### 1.2 O que NÃO existe (gaps)

1. **Comando `/recriar-livro`** — Não há comando para reescrever um livro existente em outro nível.
2. **Skill `adaptador-nivel`** — Não há skill que aplique a matriz de senioridade sobre capítulos existentes.
3. **Subagente de reescrita** — Não há subagente que leia capítulos prontos e reescreva para outro nível.
4. **Integração da senioridade no `arquiteto`** — A skill não ajusta títulos/objetivos por nível.
5. **Integração da senioridade no `estrategista`/`redator-eita`** — Não modular tom/complexidade por nível.
6. **Integração da senioridade no `revisor-tecnico`/`auditar-obra.py`** — Não validam consistência de nível.
7. **Manifesto de séries** — Não há campo `series` no `derivados.json`.

---

## 2. Resposta às Perguntas-Chave

### 2.1 É possível reescrever um livro para um nível diferente?

**SIM.** O mecanismo de derivação de e-books já prova o conceito: capítulos prontos são lidos e reescritos com tom diferente. A reescrita por nível segue o mesmo padrão, mas modula **profundidade conceitual, complexidade de código e tipo de analogia** em vez de apenas "tom leve".

### 2.2 É necessária uma nova busca (Fase 1)?

**Depende do nível-alvo:**

| Transição | Nova pesquisa? | Justificativa |
|-----------|---------------|---------------|
| Iniciante → Intermediário | **NÃO** | Mesma base factual, só muda profundidade |
| Intermediário → Avançado | **NÃO** | Mesma base, aprofunda trade-offs |
| Avançado → Técnico | **PARCIAL** | Pode precisar de papers acadêmicos extras (arXiv, IEEE) para fundamentação teórica |
| Qualquer → Qualquer (mesmo tema) | **NÃO** (padrão) | O dossiê RAG já cobre o espectro factual |

**Economia estimada:** Reaproveitar Fase 1 economiza **~30-40% do custo total de tokens** de uma obra.

### 2.3 Há reaproveitamento de buscas já realizadas?

**SIM, em 3 camadas:**

1. **Dossiê bruto** (`pesquisa/dossie_<slug>.md`) — 100% reaproveitável. Contém fatos, fontes e papers.
2. **Índice RAG** (`pesquisa/indice_dossie.json`) — 100% reaproveitável. O subagente de reescrita pode consultar via `indexar-dossie.py --buscar` sem reindexar.
3. **Sumário macro** — **Parcialmente reaproveitável.** A estrutura de partes/capítulos pode ser reutilizada, mas títulos e objetivos devem ser ajustados pelo `arquiteto` conforme a matriz de senioridade.

### 2.4 É possível criar uma série com elevação de nível?

**SIM, e é a aplicação mais valiosa.** Exemplo:

```
"Sistemas Agenticos — Guia Iniciante"      (nível 1)
"Sistemas Agenticos — Nível Intermediário"  (nível 2)
"Sistemas Agenticos — Avançado"             (nível 3)
```

Todas nascem do mesmo livro-mãe, compartilhando:
- Dossiê de pesquisa (Fase 1)
- Índice RAG
- Estrutura conceitual base (partes/temas)

Cada uma difere em:
- Sumário macro (títulos, objetivos, escopo por capítulo)
- Estratégia didática (pilares do `estrategista`)
- Redação (tom, complexidade de código, tipo de diagrama)
- Metadados da capa (badge de nível)

### 2.5 O processo precisa ser mudado?

**O processo atual NÃO precisa ser alterado na sua base.** O que precisa é **adicionar uma nova via de derivação** (similar ao que já foi feito para e-books e artigos). A esteira original continua intacta.

---

## 3. Análise de Custo de Tokens

### 3.1 Custo relativo por fase (estimativa para livro de 16 capítulos)

| Fase | % do custo total | Reaproveitável? | Custo na reescrita |
|------|-----------------|-----------------|-------------------|
| Fase 0 (Preparação) | ~2% | — | ~2% (nova config) |
| Fase 1 (Pesquisa + RAG + Arquitetura) | ~35% | **SIM (dossiê + RAG)** | ~5% (só ajuste de sumário) |
| Fase 2 (Manufatura) | ~45% | **NÃO** | ~45% (redação nova por nível) |
| Fase 2.5 (Revisão) | ~10% | **NÃO** | ~10% |
| Fase 3 (Compilação) | ~8% | **Parcial** (template, capa) | ~6% |
| **TOTAL** | 100% | — | **~68% do custo original** |

**Economia por reescrita: ~32% de tokens** (eliminação completa da Fase 1).

### 3.2 Custo de uma série completa (3 níveis)

| Cenário | Custo relativo | Observação |
|---------|---------------|------------|
| 3 livros independentes (temas iguais) | 300% | Pesquisa triplicada |
| 1 livro + 2 reescritas (série) | 100% + 68% + 68% = **236%** | Economia de ~64% vs. independente |
| 1 livro + 2 reescritas (com RAG compartilhado) | ~**220%** | Otimização adicional no pool |

---

## 4. Arquitetura Proposta

### 4.1 Novo comando: `/recriar-livro`

```
/recriar-livro <slug-livro-mae> --nivel <iniciante|intermediario|avancado>
```

**Fluxo:**

```
[Livro-mãe já compilado em output/livros/<slug>/]
         │
         ▼
[Passo 0 — Validação]
   - Verifica se livro-mãe existe e tem capítulos compilados
   - Lê config_obra.json do livro-mãe
   - Define slug: <slug-mae>--<nivel>
         │
         ▼
[Passo 1 — Reaproveitamento de Pesquisa (Fase 1 enxuta)]
   - Copia dossiê + índice RAG do livro-mãe
   - SE nivel == "tecnico": executa pesquisa complementar (papers acadêmicos)
   - Skill `arquiteto` gera novo sumário_macro com títulos/objetivos ajustados ao nível
         │
         ▼
[Passo 2 — Manufatura com Modulação de Nível]
   - `estrategista` lê senioridade_obra e ajusta pilares (complexidade do código, tipo de diagrama)
   - `redator-eita` aplica matriz EITA por senioridade
   - Pool de capítulos em lotes de 4 (idêntico ao fluxo normal)
         │
         ▼
[Passo 2.5 — Peer Review com Validação de Nível]
   - `auditar-obra.py --nivel <X>` valida consistência de tom/complexidade
   - `revisor-tecnico` corrige inconsistências
         │
         ▼
[Passo 3 — Compilação]
   - Capa com badge de nível (Iniciante/Intermediário/Avançado)
   - Compilação PDF idêntica
         │
         ▼
[Registro em derivados.json]
   - Campo "series" além de "ebooks" e "artigos"
```

### 4.2 Novo comando: `/criar-serie`

```
/criar-serie <slug-livro-mae> --niveis <iniciante,intermediario,avancado>
```

Executa `/recriar-livro` sequencialmente para cada nível, produzindo a série completa.

### 4.3 Alterações em arquivos existentes

| Arquivo | Alteração necessária |
|---------|---------------------|
| `CLAUDE.md` | Adicionar `/recriar-livro` e `/criar-serie` na tabela de tipos de obra |
| `.claude/commands/` | Novos comandos `recriar-livro.md` e `criar-serie.md` |
| `scripts/parametros_obra.py` | Adicionar campo `senioridade_obra` com fallback |
| `.claude/skills/arquiteto/SKILL.md` | Modular sumário por senioridade |
| `.claude/skills/estrategista/SKILL.md` | Modular pilares por senioridade |
| `.claude/skills/redator-eita/SKILL.md` | Aplicar matriz EITA por senioridade |
| `.claude/skills/revisor-tecnico/SKILL.md` | Validar consistência de nível |
| `scripts/auditar-obra.py` | Flag `--nivel` para validar tom/complexidade |
| `templates/template_eita.md` | Variáveis por senioridade |
| `output/livros/<slug>/derivados.json` | Campo `series[]` |

### 4.4 Novos arquivos

| Arquivo | Função |
|---------|--------|
| `SPEC_REESCRITA.md` | Especificação do comando `/recriar-livro` |
| `SPEC_SERIE.md` | Especificação do comando `/criar-serie` |
| `.claude/skills/adaptador-nivel/SKILL.md` | Skill de reescrita por nível (análoga ao `redator-ebook`) |
| `.claude/agents/subagente-adaptador-nivel.md` | Subagente de reescrita em lotes |

---

## 5. Plano de Ação (Ordem de Implementação)

### Fase A — Fundação (sem quebrar nada existente)

| # | Ação | Arquivo | Esforço |
|---|------|---------|---------|
| A1 | Atualizar `parametros_obra.py` para aceitar `senioridade_obra` | `scripts/parametros_obra.py` | Baixo |
| A2 | Integrar senioridade na skill `arquiteto` (títulos por nível) | `.claude/skills/arquiteto/SKILL.md` | Baixo |
| A3 | Integrar senioridade na skill `estrategista` (pilares por nível) | `.claude/skills/estrategista/SKILL.md` | Baixo |
| A4 | Integrar senioridade na skill `redator-eita` (matriz EITA) | `.claude/skills/redator-eita/SKILL.md` | Baixo |
| A5 | Adicionar `--nivel` no `auditar-obra.py` | `scripts/auditar-obra.py` | Médio |

### Fase B — Derivação por Nível

| # | Ação | Arquivo | Esforço |
|---|------|---------|---------|
| B1 | Criar `SPEC_REESCRITA.md` | `SPEC_REESCRITA.md` | Médio |
| B2 | Criar skill `adaptador-nivel` | `.claude/skills/adaptador-nivel/SKILL.md` | Médio |
| B3 | Criar subagente `subagente-adaptador-nivel` | `.claude/agents/subagente-adaptador-nivel.md` | Médio |
| B4 | Criar comando `/recriar-livro` | `.claude/commands/recriar-livro.md` | Baixo |
| B5 | Estender `derivados.json` com campo `series[]` | Documentação + template | Baixo |

### Fase C — Séries

| # | Ação | Arquivo | Esforço |
|---|------|---------|---------|
| C1 | Criar `SPEC_SERIE.md` | `SPEC_SERIE.md` | Baixo |
| C2 | Criar comando `/criar-serie` | `.claude/commands/criar-serie.md` | Baixo |
| C3 | Atualizar `CLAUDE.md` com novos tipos de obra | `CLAUDE.md` | Baixo |

### Fase D — Validação

| # | Ação | Esforço |
|---|------|---------|
| D1 | Testar `/recriar-livro` com livro existente (1 nível) | — |
| D2 | Testar `/criar-serie` completa (3 níveis) | — |
| D3 | Validar economia de tokens vs. livro independente | — |

---

## 6. Decisões Pendentes (Aguardando Operador)

| # | Decisão | Opções | Recomendação |
|---|---------|--------|-------------|
| 1 | Níveis suportados na V1 | `iniciante, intermediario, avancado` ou incluir `tecnico`? | V1 com 3 níveis; `tecnico` já é coberto por TCC/Artigo |
| 2 | Derivação automática ou manual? | Ao criar livro, gerar série automaticamente? | Manual (`/criar-serie`) — mais controle |
| 3 | Reaproveitar capítulos ou reescrever do zero? | Adaptar capítulos existentes (como e-book) ou gerar novos? | **Reescrever do zero** reaproveitando dossiê — qualidade superior |
| 4 | Badge visual na capa? | Badge de nível na capa 2D? | Sim — já existe mecanismo similar para e-books |

---

## 7. Conclusão

| Pergunta | Resposta |
|----------|---------|
| O fluxo suporta reescrita hoje? | **NÃO diretamente**, mas os mecanismos de derivação (e-book/artigo) provam o padrão |
| É necessária nova busca? | **NÃO** (padrão). O dossiê RAG é reaproveitável. Pesquisa complementar só para nível Técnico |
| Há reaproveitamento? | **SIM** — ~32% de economia de tokens por reescrita (Fase 1 eliminada) |
| É possível criar série? | **SIM** — via novo comando `/criar-serie` |
| O processo muda? | **NÃO na base** — adição de nova via de derivação (como já feito para e-books) |
| O que precisa ser criado? | 2 SPECs, 2 comandos, 1 skill, 1 subagente + integração em 5 arquivos existentes |

**Esforço total estimado:** Médio (Fase A = 1 sessão, Fase B = 2 sessões, Fase C = 1 sessão, Fase D = validação)
