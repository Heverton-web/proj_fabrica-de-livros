---
name: gerar-relatorio-sessao
description: >
  Orquestra o fechamento completo de uma sessão de trabalho da Fábrica
  (convenção V5.2 do AGENTS.md): gera o relatório de sessão em MD + PDF via
  scripts/gerar-relatorio-sessao.py, roda a suíte de testes, valida que o
  working tree está coerente, commita e pusha tudo.
  Use no FINAL de qualquer sessão que produziu mudanças — sintomas:
  "encerrar sessão", "fechar sessão", "gerar relatório da sessão",
  "relatório + commit + push", "entregar a sessão".
  Triggers: "gerar relatorio da sessao", "fechar sessao", "relatorio final",
  "entrega de sessao", "encerrar trabalho do dia", "commit e push de tudo"
---

# Gerar Relatório de Sessão

Fluxo único de encerramento de sessão: **relatório → testes → commit → push**.
Cada sessão de trabalho da Fábrica termina com um relatório versionado em
`relatorios/` (convenção V5.2), com tudo o que foi feito, e com o trabalho
publicado no repositório.

## Quando usar

| Situação | O que fazer |
|----------|------------|
| Fim de sessão com mudanças feitas | Relatório + testes + commit + push |
| Só falta o relatório (mudanças já commitadas) | Gerar relatório e commitar só ele |
| Revisão/conserto após feedback | Registrar o ciclo no relatório e re-validar |

## Passo a passo

> **Diretório de trabalho:** todos os passos rodam da **raiz do projeto**
> (`<raiz-do-projeto>`). Execute os `cd` indicados se estiver em subpasta.

1. **Coletar o contexto da sessão** — antes de gerar o relatório, levante:
   - **Contexto**: o que a sessão fez (obra, feature, correção)
   - **Bugs**: cada bug no formato `causa|fix|arquivo` (o que acontecia, o que
     corrigiu, onde)
   - **Arquivos alterados**: `git status --short` (lista os M/A)
   - **Validações**: testes rodados, scripts de validação executados
   - **Commits**: `git log --oneline -5` (o que já foi commitado)
   - **Entregas**: resumo em bullets (o que ficou pronto)

2. **Gerar o relatório MD + PDF** (da raiz do projeto):
   ```bash
   python scripts/gerar-relatorio-sessao.py \
     --tema "<tema-da-sessao>" \
     --titulo "<Título da Sessão>" \
     --contexto "<contexto>" \
     --bugs "causa|fix|arquivo" "causa2|fix2|arquivo2" \
     --arquivos "scripts/foo.py" "tests/test_foo.py" \
     --validacoes "451 testes passando" \
     --commits "abc123 feat(...)" \
     --entregas "fix aplicado" "testes criados"
   ```
   - Saída: `relatorios/<YYYY-MM-DD>-<tema>.md` + `.pdf` (Pandoc→Typst)
   - O tema vira nome de arquivo: acentos removidos, hífens colapsados
   - Se só o PDF falhar, rode `--pdf-only` com o mesmo `--tema` depois

3. **Validar o relatório** (abre e tem o conteúdo esperado):
   ```bash
   python -c "import pypdf; r=pypdf.PdfReader('relatorios/<arquivo>.pdf'); \
   t=''.join(p.extract_text() or '' for p in r.pages); print(len(r.pages), 'pag'); \
   print('tem tema:', '<Título>' in t)"
   ```

4. **Rodar a suíte de testes** (garante que nada quebrou):
   ```bash
   python -m pytest -q 2>&1 | tail -3
   ```
   Se falhar: **NÃO commitar** — corrigir primeiro, rodar de novo e registrar o
   bug no relatório (regenerar com `--md-apenas` + `--pdf-only`).

5. **Atualizar o RTK scratchpad** (se a sessão gerou aprendizado novo): registrar
   em `RTK-SCRATCHPAD.md` (raiz do projeto, arquivo EXTERNO ao `CLAUDE.md` desde
   21-08-2026 — item D de `melhorias/21-08-2026-plano-acao-tokens-sob-pericia.md`)
   no formato telegráfico `causa/fix/prevenção/arquivo`. NUNCA gravar de volta
   no `CLAUDE.md`/`AGENTS.md` — isso reintroduz o prefixo instável que a
   migração corrigiu.

5.1. **(Opcional) Cross-check de gasto** — se `npx`/`ccusage` estiverem
   disponíveis no ambiente, rode `python scripts/token-guard.py` e inclua o
   resultado no relatório se houver divergência (`diverge: true`) entre o
   auto-relato de `.agents/session-cost.jsonl` e o `ccusage` real. Best-effort,
   nunca bloqueia o fechamento da sessão.

6. **Commit + push** (da raiz do projeto):
   ```bash
   git add -A
   git commit -F _commit_msg.txt   # mensagem em arquivo para evitar escaping
   git push origin main
   ```
   - Convenção de mensagem: `docs(relatorios): relatorio da sessao <tema>`
   - **Apagar `_commit_msg.txt` ANTES do `git add -A`** (ou usar
     `git rm --cached` + `git commit --amend` se vazar para o commit)
   - Verificar: `git status --short` vazio e `git log origin/main -1` == local

## Armadilhas

- **Nunca commitar sem rodar os testes**: relatório de sessão com teste quebrado
  não é entrega final. Corrigir → re-testar → registrar no relatório.
- **`_commit_msg.txt` vaza fácil**: `git add -A` pega arquivos temporários.
  Remover o arquivo antes do add, ou limpar com `git rm --cached` + amend.
- **Mensagem com acentos/quebras de linha quebra o `-m`**: usar sempre `-F
  <arquivo>` com mensagem em arquivo temporário.
- **Pandoc ausente**: o `.md` é sempre salvo; o PDF falha com rc≠0. Rodar
  `--pdf-only` depois ou informar que o PDF ficou pendente.
- **Não regenerar o relatório por cima sem intenção**: mesmo tema no mesmo dia
  sobrescreve o arquivo (`YYYY-MM-DD-tema.md`). Revisar o conteúdo antes de
  regenerar se houver relatório existente.
- **Não commitar node_modules/.next/bancos**: `.gitignore` já cobre; conferir
  `git status --short` antes do `git add -A` se `marketing/` estiver no repo.

## Referência

- Script: `scripts/gerar-relatorio-sessao.py` (MD + PDF, convenção V5.2)
- Testes do script: `tests/test_gerar_relatorio_sessao.py`
- Convenção V5.2: `AGENTS.md` → Fluxo Operacional → "Entrega de Sessão (V5.2)"
- Exemplos: `relatorios/relatorio-sessao-maquina-vendas-checkout-2026-08-09.md`
