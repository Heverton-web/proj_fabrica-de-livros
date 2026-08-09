---
title: "Mapa de Entregas: Harness Engineering — Do Modelo ao Sistema Autônomo Confiável"
subtitle: "Todos os artefatos que você produz em Harness Engineering — Do Modelo ao Sistema Autônomo Confiável"
author: "Heverton Eduardo Peres"
lang: pt-BR
---

# O que você produz

Cada etapa do harness entrega artefatos concretos e verificáveis. Esta é a lista completa — use como inventário do seu projeto. Se a entrega não existe, a etapa não terminou.

| # | Etapa | Entrega | Verificação |
|---|---|---|---|
| 1 | A Revolução dos Agentes | `AGENTS.md` com a equação Agente = Modelo + Harness e o inventário de riscos | `grep -c "harness" AGENTS.md` > 0 |
| 2 | Anatomia de um Harness | `config/harness.yaml` declarando ferramentas, memória e estado | arquivo parseia com YAML |
| 3 | Test Harness | `tests/test_contrato.py` com a âncora determinística da tarefa crítica | `pytest tests/ -q` verde |
| 4 | Safety Harness e Guardrails | `config/guardrails.yaml` com zona de atuação e regras fail-closed | `validar-codigo --playbook` OK |
| 5 | Ciclo ReAct | `loop/reat.py` com observação-razão-ação e teto de iterações | smoke test de 1 tarefa roda |
| 6 | Sandboxes e Permissões | `config/zonas.json` mapeando ação → zona → política | cada ação destrutiva exige humano |
| 7 | Gestão de Contexto | `trilha/contexto.py` com poda e sumarização automática | trilha sob 90% do contexto em 5 rodadas |
| 8 | Harness em Produção | `trilha/metricas.json` + evals de regressão no CI | 1 métrica por passo + alerta de drift |

**Regra de ouro:** toda entrega tem verificação. Se não dá para conferir, não é entrega — é intenção.

# Próximo passo

Este material é um recorte de **Harness Engineering — Do Modelo ao Sistema Autônomo Confiável**. A obra completa traz a teoria, os exemplos comentados e as referências.

> [**Quero a obra completa**](https://exemplo.com/obra?utm_source=lead-magnet&utm_medium=pdf&utm_campaign=entregas)
