---
title: Kit de Fundação AIDD — Pacote Generalizado de Práticas de Engenharia
subtitle: Plano de extração das decisões arquiteturais desta fábrica para submodule reutilizável
author: Fábrica Agêntica de Publicações
date: 2026-08-12
---

# 1. Contexto

Dois documentos descrevem decisões de arquitetura/engenharia já **aplicadas e
verificadas** neste projeto:

- `docs/plano-adaptacao-metodo-eita-senioridade.md` — matriz de adaptação por
  senioridade (iniciante/intermediário/avançado/técnico) integrada em 4 pontos
  da esteira (`esbocar.md`, `parametros_obra.py`, `arquiteto`/`estrategista`/
  `redator-eita`, `revisor-tecnico`/`auditar-obra.py`). Confirmado: `senioridade`
  aparece em 48 arquivos do repositório.
- `docs/manual-replicar-praticas-acima-media.md` — 5 práticas de engenharia
  genéricas já usadas nesta fábrica: (1) Builder ≠ Critic, (2) Crítico
  determinístico, (3) Registro declarativo, (4) Nunca commitar vermelho como
  gate mecânico, (5) Postmortem que vira teste. Confirmado: todas têm
  implementação real (`subagente-redator-capitulo`/`subagente-revisor-tecnico`,
  `validar-*.py`, `tipos_obra.py`, `scripts/hooks/pre-commit`, seção 7 do
  `CLAUDE.md`).

**Decisão:** doc 1 não vira módulo próprio — é tratado como *caso de uso* da
Peça 3 (registro declarativo aplicado a um eixo "perfil/tier" em vez de "tipo
de obra"). O pacote generaliza só as 5 peças do doc 2, documentando o caso de
uso do doc 1 como exemplo dentro da doc da Peça 3.

# 2. Objetivo

Empacotar as 5 peças, **desacopladas de vocabulário de livro/EITA/capítulo**,
num repositório próprio (`kit-fundacao-aidd`), distribuído como git submodule
— mesmo padrão já usado neste repositório para `code-review-graph` e
`impeccable` (`.gitmodules`).

# 3. Arquitetura do pacote

```
kit-fundacao-aidd/
├── README.md
├── analisar-projeto.py          Passo 0: diagnóstico não-destrutivo do projeto-alvo
├── instalar.py                  Aplica peças escolhidas — aditivo, nunca remove/sobrescreve
├── skills/kit-fundacao-aidd/SKILL.md   Versão interativa (Claude Code) do instalador
├── agents/
│   ├── builder.md.template      Peça 1 — gera artefato, nunca julga
│   └── critic.md.template       Peça 1 — tools: Read (travado, só leitura)
├── hooks/
│   └── pre-commit.template      Peça 4 — roda test runner detectado, bloqueia commit vermelho
├── scripts/
│   ├── validar_template.py.template     Peça 2 — esqueleto de gate determinístico
│   ├── registro_declarativo_scaffold.py Peça 3 — gera TIPOS={} + dispatch
│   └── postmortem_para_teste.py         Peça 5 — converte bloco "Prevenção:" em stub de teste
├── templates/
│   └── POSTMORTEM.md            molde data/causa/fix/prevenção/arquivos
└── tests/                       o pacote testa a si mesmo (dogfooding da Peça 4)
```

# 4. Regras inegociáveis do instalador (feedback do operador, 2026-08-12)

1. **Nunca remove ou sobrescreve** arquivo/skill/hook já configurado no
   projeto-alvo. Colisão → mescla não-destrutiva (ex.: hook ganha bloco extra
   no fim) ou pausa e pergunta — nunca decide sozinho.
2. **Sempre explica antes de aplicar**: uma frase do que vai ser criado/
   alterado e por quê, antes do diff de confirmação (diff sozinho não basta).
3. Reexecução é idempotente — peça já presente é reportada como "já presente,
   nada a fazer", nunca "corrigida".

# 5. Distribuição

```bash
# no repo kit-fundacao-aidd (standalone)
gh repo create kit-fundacao-aidd --private --source=. --push

# no projeto-alvo (novo ou existente)
git submodule add <url> tooling/kit-fundacao-aidd
git submodule update --init --recursive
python tooling/kit-fundacao-aidd/analisar-projeto.py .      # só relatório
python tooling/kit-fundacao-aidd/instalar.py . --dry-run    # explica + diff, nada grava
```

# 6. Critério de aceite

Rodar `analisar-projeto.py` neste próprio repositório (`proj_fabrica-de-livros`)
deve reconhecer as 5 peças já nativas (ou reportar divergência de convenção
sem propor remoção/substituição) — é o teste de aceitação real, já que aqui as
peças já existem por implementação original, não pelo pacote.

# 7. Ciclo de execução

Implementar → testar (`pytest -q` no pacote) → validar (100% verde, nunca
commitar vermelho — R16) → se `<100%`, corrigir causa raiz e repetir o ciclo
até fechar. Depois: registrar submodule, rodar suite completa do projeto-alvo,
relatório de sessão, commit + push.
