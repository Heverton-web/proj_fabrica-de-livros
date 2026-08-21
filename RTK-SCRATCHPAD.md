---
titulo: RTK Scratchpad — Aprendizados de Sessões
descricao: Aprendizados da fábrica capturados e isolados do CLAUDE.md para estabilidade de cache
atualizado_em: 2026-08-21
---

## 7. RTK SCRATCHPAD

*(Espaço para registro de aprendizados pela skill `rtk-memory`)*

- **2026-08-11 Produção completa série 5 (coleção `agentic-design-patterns`):**
  causa: série 5 da proposta (Agentic Design Patterns — o "Gang of Four" dos
  fluxos agênticos) exigia fluxo FULL com livro, derivados, campanhas e máquina;
  3 lições reais. Fix/lições: (1) **pasta `campanhas/material/` é o nome
  CANÔNICO da campanha do livro-raiz** — `nome_material` do slug
  `<chave>/livros/<chave>-v1` trunca para `v1` e o fallback de `nome_curto`
  vira `material`; NÃO apagar (parece lixo, é a campanha do livro; as pastas
  dos derivados são `dck-1-design`, `eb-01-design` etc. com desambiguação V5.4);
  (2) `criar-campanha --completo` com 12 materiais estoura timeout (~590s) —
  rodar `--completo` e completar materiais restantes com `--material <slug>`
  individual (32 artes cada); (3) moldes de campanha nascem `Status: RASCUNHO`
  e R-CP-2 reprova — promover a `FINAL` com sed em massa e marcar `status:
  completa` no `campanha.json` (o flag `--marcar-completa` junto de
  `--completo` REGENERA tudo e estoura timeout; editar o JSON direto).
  Resultado: livro 68 pág CONFORME, 12 membros, campanhas 12/12 com 384 artes
  únicas (R-CP-6), máquina personalizada (gate regra 12 vazio), suíte 662/662.
  Arquivos: `output/agentic-design-patterns/**`,
  `relatorios/11-08--producao-completa-agentic-design-patterns.md/.pdf`.

- **2026-08-11 Cheatsheet vazio + R-PBK-5 em playbook de livro P (fluxo FULL MAS):** causa: (1) `gerar-lead-magnet.py --todos` gerava cheatsheet com 0 itens — `montar_cheatsheet` lê `card.comandos` no NÍVEL do card (ou `card.gate`), não dentro de `execucao[]`, e o `extrair-passos-praticos.py` só preenche `execucao[].codigo`; (2) `validar-playbook.py` R-PBK-5 conta a soma de linhas de TODOS os blocos de `execucao` (`sum(len(codigo)+2)`), então múltiplos blocos de código de capítulo estouram 25 linhas; (3) R2 do livro P exige ~100.000 chars (40 pág.) — 4 capítulos de ~20k chars ficam ~20% abaixo. Fix: adicionar `comandos` no topo dos cards do playbook (11 comandos → cheatsheet CONFORME); compactar `execucao` para 1 bloco de ≤18 linhas por card (truncar mantendo docstring+assinaturas); expandir capítulos com seções técnicas reais (votação do enxame, validação de contrato, retry com backoff, roteador, dual-mode, monitor de custo, calibração por amostra). Prevenção: cheatsheet = agregador de `card.comandos`/`card.gate` do playbook — se o playbook nasce sem comandos, o LM cheatsheet nasce vazio; validar playbook ANTES de gerar LMs; R2 = estimar chars por capítulo na escrita (mín. 25k por capítulo de livro P). Resultado: livro MAS 100.000+ chars/54 pág PDF CONFORME, playbook 4 passos CONFORME, 6 LMs CONFORME, suíte 662/662. Arquivos: `output/…/playbooks/pbk-1-sistemas-multiagentes/passos/*.json`.

### [2026-08-13] RUNTIME: Subagente de expansão travou em 48 turns
- **Causa**: spawnar 1 subagente para expandir 8 capítulos (de ~12k para ~25k chars cada = ~100k chars de expansão total) estourou o limite de turns. Tarefa monolítica demais para um único subagente geral.
- **Fix**: cancelado (actor cancel). Expansão ficou pendente.
- **Arquivo**: actor general-10 (expansão de conteúdo livros/orca-ide)
- **Prevenção**: em expansion tasks, dividir em lotes de 2-3 capítulos por subagente, nunca 8 de uma vez. Se a tarefa envolver rewrite de múltiplos arquivos grandes, usar subagentes paralelos com escopo delimitado.

### [2026-08-13] PADRÃO: Playbook extraído de capítulos com refs faltantes
- **Causa**: `extrair-passos-praticos.py` extrai dados dos capítulos, mas 3 capítulos (2,3,7) tinham seção 7 (Referências) vazia. O gate R4 (mín 8 refs) falhou na auditoria.
- **Fix**: subagente revisor adicionou 3 refs ABNT a cada capítulo afetado.
- **Arquivo**: output/livros/orca-ide/capitulos/cap_{2,3,7}.md
- **Prevenção**: validar refs na seção 7 DEPOIS da escrita de cada capítulo (auto-validação do subagente-redator-capitulo deve checar contagem de refs, não apenas existência). Rodar `auditar-obra.py` imediatamente após cada lote, não só no final.

### [2026-08-13] CONFIG: Livro M ficou com 99k chars (mínimo 200k)
- **Causa**: capítulos escritos com ~12k chars em média, mas o mínimo para tamanho M (~80 páginas) é ~25k chars por capítulo. Subagentes produziram conteúdo válido mas curto demais.
- **Fix**: pendente — conteúdo precisa ser expandido.
- **Arquivo**: output/orca-ide/livros/orca-ide/capitulos/cap_*.md
- **Prevenção**: no prompt do subagente-redator-capitulo, incluir meta explícita de tamanho mínimo por seção (ex.: "seção Explica: mínimo 3000 caracteres"). Incluir contagem de caracteres no relatório de auto-validação.

### [2026-08-13] ESTRUTURA: Diretórios soltos fora do hub da coleção
- **Causa**: `fatiar-obra.py --playbook` gravou em `output/playbooks/` e o minerador acadêmico gravou em `output/orca-ide/pesquisa/` — ambos fora do hub `output/orca-ide/`. O orquestrador não validou a localização antes de prosseguir. Além disso, `colecao.py --sincronizar` criou `output/colecoes/` como fallback quando o hub não existia.
- **Fix**: movido manualmente para `output/orca-ide/livros/orca-ide/` e `output/orca-ide/playbooks/pbk-1-orca-ide-manual/`. Limpos diretórios órfãos `output/livros/`, `output/playbooks/` e `output/colecoes/`.
- **Arquivo**: output/orca-ide/ (hub), output/livros/ (removido), output/playbooks/ (removido), output/colecoes/ (removido)
- **Prevenção**: SEMPRE usar `tipos_obra.dir_obra(slug)` para resolver caminhos — nunca criar diretórios manualmente. Após `fatiar-obra.py`, validar que os artefatos ficaram dentro do hub com `ls output/<hub>/<tipo>/`. Se estiverem soltos, MOVER antes de qualquer operação seguinte. Rodar `colecao.py --sincronizar` após cada movimentação. O fallback `output/colecoes/` do `colecao.py` é legado — NÃO deve ser usado; o manifesto sempre vai em `<hub>/colecoes/<slug>.json`.
