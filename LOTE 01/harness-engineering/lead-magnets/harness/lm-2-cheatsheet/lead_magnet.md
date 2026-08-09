---
title: "Cheat Sheet: Harness Engineering — Do Modelo ao Sistema Autônomo Confiável"
subtitle: "Os 12 comandos essenciais de Harness Engineering — Do Modelo ao Sistema Autônomo Confiável em uma folha de bancada"
author: "Heverton Eduardo Peres"
lang: pt-BR
---

# Folha de bancada

Os 12 comandos essenciais, na ordem de execução. Imprima e deixe ao lado do teclado.

## 1. Inventariar o arnês

```bash
grep -rn "harness" AGENTS.md | head
```

## 2. Declarar as ferramentas

```bash
cat config/harness.yaml | yq '.ferramentas | keys'
```

## 3. Ancorar a tarefa crítica em teste

```bash
pytest tests/test_contrato.py -q --maxfail=1
```

## 4. Rodar a régua de qualidade

```bash
python scripts/validar-codigo.py livros/harness-engineering --executar
```

## 5. Verificar guardrails fail-closed

```bash
python scripts/validar-codigo.py --playbook
```

## 6. Executar o loop ReAct com teto

```bash
python loop/reat.py --tarefa "resumo do sprint" --max-iteracoes 5
```

## 7. Conferir as zonas de permissão

```bash
cat config/zonas.json | jq '.zonas | to_entries[] | "\(.key): \(.value.politica)"'
```

## 8. Podar o contexto

```bash
python trilha/contexto.py --poda --janela 4000
```

## 9. Medir a telemetria do passo

```bash
python trilha/metricas.py --passo 12 --json
```

## 10. Rodar evals de regressão

```bash
python evals/regua.py --suite todas --limiar 0.7
```

## 11. Auditar a obra inteira

```bash
python scripts/auditar-obra.py livros/harness-engineering --estrito
```

## 12. Validar artefatos finais

```bash
python scripts/validar-artefatos.py --todos --estrito
```

**Regra de ouro:** se o comando não existe, a etapa não terminou — o harness é feito de verificações executáveis.

# Próximo passo

Este material é um recorte de **Harness Engineering — Do Modelo ao Sistema Autônomo Confiável**. A obra completa traz a teoria, os exemplos comentados e as referências.

> [**Quero a obra completa**](https://exemplo.com/obra?utm_source=lead-magnet&utm_medium=pdf&utm_campaign=cheatsheet)
