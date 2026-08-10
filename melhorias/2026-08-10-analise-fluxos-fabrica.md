---
title: Plano de Correção e Melhoria de Fluxos
subtitle: Análise de Materiais, Campanha e Máquina de Vendas
author: Antigravity IDE (Fábrica V5)
date: 2026-08-10
---

# 1. Mapeamento de Fluxos

## 1.1 MATERIAIS DERIVADOS (Playbook, Lead Magnet, Deck, E-mails)
- **INPUTS:**
  - Conteúdo gerado e validado (`livros/<slug>`, `tccs/<slug>`), com seções estruturadas via EITA/ACAD.
  - Metadados nos arquivos `config_obra.json` e `sumario_macro.json`.
- **PROCESSAMENTOS:**
  - `extrair-passos-praticos.py`: Extrai os *cards* do playbook puxando `tecnica` e `aplica`, além de extrair blocos de código e comandos de execução (gates). Transmuta listas de validação (fallback: lista binária).
  - `gerar-lead-magnet.py`: Consome os *cards* extraídos, aplica sistema de *rodízio* para gerar variações temáticas distribuindo itens do livro de forma equitativa (Checklist, Mapa, Cheatsheet). O HTML resultante vai para Chromium via script auxiliar.
  - `gerar-deck.py`: Consolida a parte de apresentação (`.html`), simplificando os bullets.
- **OUTPUTS:**
  - `output/<colecao>/playbooks/<nome>.pdf`
  - `output/<colecao>/lead-magnets/...` (Múltiplos formatos em PDF)
  - `output/<colecao>/decks/...` (HTML navegável e export PDF)

## 1.2 CAMPANHA (V5.3)
- **INPUTS:**
  - Hub do material (manifestos e artefatos).
  - Dossiê e matriz de cores persistidas em `output/series.json`.
- **PROCESSAMENTOS:**
  - `criar-campanha.py` cria o cronograma da campanha (3 fases: gancho, aprofundamento, urgência/CTA).
  - Interpolamento determinístico (`escrever_moldes`) com rascunhos injetados que depois o LLM refina.
  - Geração de Artes HTML convertidas para PNG via Chromium.
- **OUTPUTS:**
  - Diretórios: `output/<colecao>/campanhas/<slug>/redes-sociais/` e `canais-comunicacao/`.
  - Hub `campanha.json` sincronizado, artes (PNG), rascunhos (MD) e PDF compilado.

## 1.3 MÁQUINA DE VENDAS
- **INPUTS:**
  - Manifesto da Coleção (`output/<colecao>/colecoes/<nome>.json`).
  - Template `templates/maquina/` (Next.js + FastAPI).
  - Snapshot gerado do fluxo de Campanha.
- **PROCESSAMENTOS:**
  - `criar-maquina-vendas.py` gera cópia do template para a pasta do hub.
  - Personalização de placeholders baseada nos metadados.
  - Hook de validação (gate `grep 'Autor Digital'`) para barrar copies genéricas.
- **OUTPUTS:**
  - Repositório local deployável em `output/<colecao>/maquina/` com ambiente isolado.

---

# 2. Diagnóstico e Plano de Correções

### GAP 1: Risco de Perda de Copy na Campanha
- **Causa:** O script `criar-campanha.py` escreve rascunhos (`.md`). Quando chamado com `--regenerar`, sobrepõe arquivos `.md` e `.pdf` antigos.
- **Risco:** Perda irreversível de conteúdo redigido manualmente ou refinado com custo de API.
- **Solução/Implementação:** Alterar `escrever_moldes` para forçar um backup em `revisao/backups/<ts>/` dos `.md` atuais antes de reescrevê-los.

### GAP 2: Extração de Fallback Imperativa para Playbook
- **Causa:** Em EITA, `aplica/exercicio` pode vir em prosa não-listada. `extrair-passos-praticos.py` tem `itens_binarios` como fallback, mas alucinações geram cards com `lacuna: feito_quando_insuficiente`.
- **Solução/Implementação:** Adicionar hard constraint no prompt de `redator-eita` forçando que "Feito Quando / Exercício" possua sempre lista demarcada de validação (`- [ ]`). Inserir um warning verbal no extrator para reprovar cards no ato, forçando gate F1/F2.

### GAP 3: Gate de Nicho Fraco na Máquina de Vendas
- **Causa:** Substituição na máquina (`copiar_template()`) é feita com simples `.replace()`.
- **Risco:** O gate da Regra 12 exige personalização de nicho, mas se não varrer corretamente as páginas (`app/page.tsx`), a máquina nascerá com placeholder genérico (Autor Digital).
- **Solução/Implementação:** `criar-maquina-vendas.py` deve fazer validação pós-replace (ex. `grep` embutido) bloqueando sucesso caso localize a copy padrão.

### GAP 4: Encoding UTF-8 em Scripts
- **Causa:** Regra 11 demanda stdout UTF-8 no Windows, porém alguns extratores ainda quebram no console com emojis.
- **Solução/Implementação:** Garantir chamada a `sys.stdout.reconfigure(encoding="utf-8")` na função `main` de:
  - `gerar-lead-magnet.py`
  - `gerar-deck.py`
  - `criar-campanha.py`
