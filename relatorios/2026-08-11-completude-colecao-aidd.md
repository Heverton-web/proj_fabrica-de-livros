# RELATÓRIO DE SESSÃO — Completude da Coleção AIDD Engenharia Nativa — derivados, campanhas e máquina de vendas

> **Data:** 2026-08-11
> **Projeto:** Fábrica Agêntica de Publicações

---

## 1. Contexto

Sessao de completude da colecao AIDD Engenharia Nativa (4 volumes): geracao dos 24 lead magnets (fix de colisao de slugs por volume), 4 decks com fix de hub no validador, 40 e-mails com polimento deterministico, polimento dos 4 mini-guias, geracao dos 4 artigos e 4 ebooks por compressao fiel dos capitulos + PDF/EPUB/capas, sincronizacao da colecao (48 membros), empacotamento, 48 campanhas com fix de nome_material para hub multi-volume (V5.5) + copy final + gate R-CP estrito 48/48, e maquina de vendas personalizada por nicho (regra 12).

---

## 2. Bugs Descobertos e Corrigidos

### colisao de slugs de lead magnet por volume: lm-N-<tipo> identicos entre volumes

- **Causa:** colisao de slugs de lead magnet por volume: lm-N-<tipo> identicos entre volumes
- **Fix:** sufixo com a palavra distintiva do volume
- **Arquivo:** `scripts/gerar-lead-magnet.py`

### nome_material so desambiguava a chave da colecao: dck-1-*/eml-1-*/pbk-1-* e artigos com slug do volume colidiam em hub multi-volume

- **Causa:** nome_material so desambiguava a chave da colecao: dck-1-*/eml-1-*/pbk-1-* e artigos com slug do volume colidiam em hub multi-volume
- **Fix:** _volume_obra le obra_mae do config, remove prefixo do volume e anexa palavra distintiva, total cortado a 20 chars
- **Arquivo:** `scripts/campanha.py`

### validar-deck nao resolvia hub por colecao

- **Causa:** validar-deck nao resolvia hub por colecao
- **Fix:** replicado o fix do validar-playbook
- **Arquivo:** `scripts/validar-deck.py`

### mapa do lead magnet reprovava R-LM-7 com 2 estagios

- **Causa:** mapa do lead magnet reprovava R-LM-7 com 2 estagios
- **Fix:** contagem total de linhas do mapa (estagios + cards)
- **Arquivo:** `scripts/gerar-lead-magnet.py`

### artigos/ebooks com esqueletos vazios

- **Causa:** artigos/ebooks com esqueletos vazios
- **Fix:** compressao fiel das secoes reais dos capitulos + montagem do livro_final.md para EPUB
- **Arquivo:** `_tmp_gerar_artigos_ebooks.py + compilar-para-pdf.py`

### --completo de campanhas estourava timeout regenerando artes

- **Causa:** --completo de campanhas estourava timeout regenerando artes
- **Fix:** gerar_completo com com_artes=False reaproveitando artes existentes
- **Arquivo:** `scripts/criar-campanha.py`

### maquina de vendas nascia com copy generica

- **Causa:** maquina de vendas nascia com copy generica
- **Fix:** personalizacao por nicho em configs, frontend, e-mails e docs ate o gate da regra 12 ficar vazio
- **Arquivo:** `output/aidd-engenharia-nativa/maquina`

### moldes de campanha RASCUNHO com copy generica em 1248 arquivos

- **Causa:** moldes de campanha RASCUNHO com copy generica em 1248 arquivos
- **Fix:** polimento deterministico com ganchos reais do sumario + vocabulario condutor + recompilacao de PDFs
- **Arquivo:** `_tmp_polir_campanhas.py`

---

## 3. Arquivos Alterados

- `scripts/campanha.py`
- `scripts/gerar-lead-magnet.py`
- `scripts/validar-deck.py`
- `tests/test_campanha.py`
- `tests/test_lead_magnet.py`
- `output/aidd-engenharia-nativa/colecoes/aidd-engenharia-nativa.json`
- `output/aidd-engenharia-nativa/maquina`
- `AGENTS.md`

---

## 4. Validações

- 662 testes passando (pytest -q)
- validar-campanha --estrito: 48/48 campanhas conformes
- validar-artefatos --todos --estrito: 0 artefatos quebrados
- empacotar-colecao: 56 arquivos com maquina
- gate regra 12: zero ocorrencias de copy generica na maquina

---

## 5. Commits

- `pendente (fechamento da sessao)`

---

## 6. Resumo de Entregas

- 24 lead magnets com PDFs, capas e gate
- 4 decks com HTML/PDF e gate
- 40 e-mails polidos com gate
- 4 mini-guias polidos
- 4 artigos + 4 ebooks compilados (PDF/EPUB/capas)
- 48 campanhas com copy final e gate R-CP estrito
- maquina de vendas personalizada por nicho + snapshot de campanhas
- RTK: aprendizado nome_material multi-volume

---

*Relatório gerado em 2026-08-11 — Fábrica Agêntica de Publicações*
