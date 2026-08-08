---
description: Sincroniza e inspeciona a COLEÇÃO — o conjunto de todos os artefatos derivados de um mesmo núcleo canônico (dossiê + sumário + motivo condutor).
---

# /colecao `[<nome>]` `[--sincronizar]`

**COLEÇÃO** = todos os artefatos derivados de um mesmo núcleo canônico
(dossiê + `sumario_macro` + `motivo_condutor`), compartilhando identidade
visual, vocabulário condutor, badge de nível e CTA.

A chave da coleção (`serie_key`) resolve nesta ordem:
`config_obra.serie` → `config_obra.livro_mae` → nome-base do slug.

## Sincronizar (manifesto é derivado, nunca editado à mão)

```
python scripts/colecao.py --sincronizar
python scripts/colecao.py --sincronizar --slug livros/<slug>
```

Varre `output/` inteiro e grava `output/_colecoes/<nome>.json`.

## Inspecionar

```
python scripts/colecao.py --listar
python scripts/colecao.py "<nome>" --status
python scripts/colecao.py "<nome>" --json
```

O status mostra, por membro: tipo, estado (`vazio` → `planejado` → `redigido`
/ `extraido` → `compilado`), custo de LLM do tipo e título. Além disso:

- `derivados_ausentes` — o que ainda dá para gerar a custo quase zero
- `membros_sem_cta` — lead magnets / decks / e-mails que vão reprovar no gate

## Quando rodar

Sempre depois de gerar qualquer derivado. Os comandos `/criar-playbook`,
`/criar-lead-magnet`, `/criar-deck` e `/criar-emails` já terminam chamando
`--sincronizar`.

## Matriz de derivação

```
python scripts/tipos_obra.py --matriz
```

Mostra quem deriva de quem, a natureza (geração / expansão / compressão /
extração) e o custo de LLM. **Regra:** cascateie onde comprime, faça fan-out
onde expande.
