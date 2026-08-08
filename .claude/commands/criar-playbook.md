---
description: Gera o PLAYBOOK prático de um livro já compilado — extração determinística das §4 Técnica + §5 Aplica (custo ~0 token). Contrato em SPEC_PLAYBOOK.md.
---

# /criar-playbook `<prefixo>/<slug>`

**Pré-condição:** `output/<prefixo>/<slug>/capitulos/cap_*.md` existem e a obra
passou pela Fase 2.5 (`auditar-obra.py` CONFORME).

## Passo 1 — Esqueleto (0 token)

```
python scripts/fatiar-obra.py <prefixo>/<slug> --playbook
```

Cria `output/playbooks/<slug>--pbk/`, herda `senioridade_obra`, `serie` e
`motivo_condutor`, e grava a seção `playbooks` em `derivados.json`.

## Passo 2 — Extração determinística (0 token)

```
python scripts/extrair-passos-praticos.py <prefixo>/<slug> --relatorio
```

Produz 1 `passos/passo_NN.json` por capítulo + `playbook.md` + o relatório de
lacunas. **Leia o relatório: ele é a lista de trabalho do Passo 3.**

## Passo 3 — Polimento por LLM (apenas as lacunas)

Escreva **somente** o que o relatório apontou:

1. `objetivo_material` no `sumario_macro.json` (1 parágrafo, máx. 15 linhas)
2. Ligações entre estágios usando o `vocabulario` do `motivo_condutor`
3. Passos com `lacunas` — complete a parte faltante lendo **apenas** a seção
   correspondente do `cap_NN.md` (LeanCTX: nunca leia o capítulo inteiro)

Obra com mais de 12 capítulos: polir em lotes de 5 via
`pool-capitulos.py --manifesto`.

**Proibido (R-PBK-0):** copiar prosa das §1, §2, §3 ou §7. O gate reprova por
similaridade.

## Passo 4 — Identidade visual

```
python scripts/gerar-capa.py playbooks/<slug>--pbk --tipo playbook
python scripts/validar-capa-nivel.py output/playbooks/<slug>--pbk
```

Ilustração de capa: `subagente-ilustrador` (Modo Capa), briefing =
`motivo_condutor.descricao` do livro-mãe → `imagens/capa_ilustracao.png`.

## Passo 5 — Gate (até 2 rodadas de correção)

```
python scripts/validar-playbook.py playbooks/<slug>--pbk --estrito
```

## Passo 6 — PDF

```
python compilar-para-pdf.py playbooks/<slug>--pbk --tipo playbook
```

## Passo 7 — Registro na coleção

```
python scripts/colecao.py --sincronizar --slug <prefixo>/<slug>
```

## Passo 8 — Relatório telegráfico (REGRA 2)

Número de passos, lacunas restantes, veredito do gate, caminho do PDF.
Sem preâmbulo.

## Verificação de entrega (sempre)

```
python scripts/validar-artefatos.py --todos --estrito
```

Gerar o arquivo não prova que ele abre. Este passo confere assinatura, integridade
e comprimento de caminho (MAX_PATH do Windows). Só depois:

```
python scripts/empacotar-colecao.py "<coleção>"
```
