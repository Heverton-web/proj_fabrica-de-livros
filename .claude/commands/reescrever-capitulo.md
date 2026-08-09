---
description: Reescreve UM capítulo específico de um livro/TCC existente, com backup automático e reauditoria dos gates (F1/F2). Uso: /reescrever-capitulo <slug> <n> [motivo]
---

Você é o Orquestrador Mestre. O operador disparou `/reescrever-capitulo` com
`$ARGUMENTS` = `<slug> <n> [motivo]` (ex.: `livros/ia-agentica-desbloqueada 5
"aprofundar a seção Técnica com mais código"`).

Objetivo: regravar APENAS o capítulo `n`, preservando o restante da obra.

## Passo 0 — Pré-condições (LeanCTX: grep antes de read)
1. Confirme que `output/<slug>/capitulos/cap_<n>.md` existe.
2. Marque o capítulo para reescrita (faz backup em `revisao/backups/<ts>/` e
   volta a `pendente`):
   ```bash
   python scripts/pool-capitulos.py <slug> --reescrever <n>
   ```
   Registre o caminho do backup exibido — ele é a BASE da reescrita.

## Passo 1 — Redação (1 subagente, com base)
3. Despache `subagente-redator-capitulo` SOMENTE para o capítulo `n`, com
   instruções explícitas:
   - **Base = backup**: releia `revisao/backups/<ts>/cap_<n>.md` e reescreva a
     partir dele (não do zero).
   - **Preserve**: numeração de referências `[N]` válidas (não renumere sem
     conferir a seção 7), diagramas Mermaid reutilizáveis, dados factuais já
     citados.
   - **Motivo** (se informado): aplique-o como critério dominante da reescrita.
   - Skill `redator-eita`, Modo Reescrita.

## Passo 2 — Reauditoria do capítulo (gates)
4. Estrutura + código:
   ```bash
   python scripts/validar-codigo.py <slug> --capitulo <n> --estrito --executar
   ```
5. Gates de conteúdo do capítulo (referências offline; com rede se possível):
   ```bash
   python scripts/validar-referencias.py <slug> --capitulo <n>
   python scripts/validar-metricas.py <slug> --capitulo <n>
   python scripts/validar-escala.py <slug> --capitulo <n>
   python scripts/validar-afirmacoes.py <slug> --capitulo <n>
   ```
6. Se reprovar: corrija o capítulo (auto-correção, REGRA 4) e re-rode até passar.
7. Registre no pool:
   ```bash
   python scripts/pool-capitulos.py <slug> --registrar <n> --sucesso
   ```

## Passo 3 — Relatório telegráfico (REGRA 2)
Capítulo, backup (caminho), motivo, vereditos dos gates, caracteres antes/depois.
Sem preâmbulo.
