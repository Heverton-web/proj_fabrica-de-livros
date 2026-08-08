# SPEC_PLAYBOOK — Contrato do Playbook (V5)

> Tipo derivado de **extração determinística**. Custo alvo: **0 token de LLM**
> na extração; polimento por LLM apenas nas lacunas apontadas pelo relatório.

## 1. Definição

Documento de **bancada** que reúne, na ordem do livro-mãe, os passos práticos
extraídos das seções **§4 Técnica** e **§5 Aplica** de cada capítulo EITA-V2.

O playbook **não é um resumo do livro**. É o livro sem a teoria.

## 2. Fonte de derivação

| Item | Origem determinística |
|---|---|
| Cards | `output/livros/<slug>/capitulos/cap_NN.md` §4 + §5 |
| Objetivo de cada passo | `sumario_macro.partes[].capitulos[].objetivo` |
| Nome dos estágios | `sumario_macro.motivo_condutor.vocabulario[]` |
| Persona | `sumario_macro.motivo_condutor.persona_leitor` |
| Badge de nível | `config_obra.senioridade_obra` (herdado) |
| Cor de acento | `series_capa.resolver_cor(serie_key)` (herdado) |

Derivação permitida: **livro → playbook**. Validada por
`tipos_obra.validar_derivacao("playbook", <tipo_mae>)`.

## 3. Anatomia do card (7 partes)

| # | Parte | Campo JSON | Extração |
|---|---|---|---|
| ① | Objetivo do passo | `objetivo` | `sumario_macro` (fallback: §1 primeiro parágrafo) |
| ② | Pré-requisito | `pre_requisito` | card anterior |
| ③ | Entregas | `entregas` | paths em crase na §4 |
| ④ | Execução | `execucao` | subtítulos `###` + blocos de código da §4 |
| ⑤ | Verificação / Gate | `gate` | 1º comando executável (prioriza `validar`/`pytest`) |
| ⑥ | Feito quando… | `feito_quando` | itens do "Exercício Prático" da §5 |
| ⑦ | Armadilhas | `armadilhas` | itens de "Armadilhas Comuns" da §5 |

## 4. Regras (gate: `scripts/validar-playbook.py`)

| Regra | Enunciado |
|---|---|
| **R-PBK-0** | O playbook **não repete teoria**: §1, §2, §3 e §7 do livro nunca entram. Cobrado por similaridade de Jaccard (limiar 0,25) do card contra a teoria do capítulo-fonte. |
| **R-PBK-1** | Todo card tem as 7 partes preenchidas (① a ⑦) |
| **R-PBK-2** | Todo card cita ao menos 1 entrega com caminho de arquivo |
| **R-PBK-3** | Todo card tem 1 comando de verificação executável |
| **R-PBK-4** | "Feito quando…" tem de 3 a 7 itens binários |
| **R-PBK-5** | Nenhuma parte do card excede 25 linhas (documento de bancada) |
| **R-PBK-6** | Capa com badge de nível + ilustração no motivo condutor (herda REGRA 5) |
| **R-PBK-7** | 1 card por capítulo do livro-mãe, **na mesma ordem**, sem lacuna |
| **R-PBK-8** | Vocabulário do `motivo_condutor` presente nos nomes de estágio |

## 5. Estrutura de saída

```
output/playbooks/<slug-mae>--pbk/
├── config_obra.json          tipo_obra=playbook, obra_mae, senioridade herdada
├── sumario_macro.json        titulo, motivo_condutor herdado, estagios[]
├── passos/passo_NN.json      1 card por capítulo
├── playbook.md               documento montado
├── imagens/                  capa + ilustração condutora
└── revisao/
    ├── relatorio_extracao.json    lacunas por passo (lista de trabalho do LLM)
    └── relatorio_playbook.json    saída do gate
```

## 6. Pipeline

```bash
python scripts/fatiar-obra.py livros/<slug> --playbook
python scripts/extrair-passos-praticos.py livros/<slug> --relatorio
python scripts/gerar-capa.py playbooks/<slug>--pbk --tipo playbook
python scripts/validar-playbook.py playbooks/<slug>--pbk --estrito
python compilar-para-pdf.py playbooks/<slug>--pbk --tipo playbook
```

## 7. Custo em tokens

| Etapa | Natureza | Custo |
|---|---|---|
| Fatiamento + extração dos cards | Script | **0** |
| Objetivo do Material + ligações de estágio | LLM | ~3k |
| Polimento de lacunas apontadas | LLM | ~1k por card com lacuna |
| Capa/ilustração | Playwright/HTML | **0** (sem API) |
| Compilação | Pandoc+Typst | **0** (isento por `CLAUDE.md` §0.5) |

Livro XG (20 capítulos): **5–12k tokens** — cerca de 1/10 do custo de um e-book.

## 8. Definição de pronto

- [ ] 1 `passo_NN.json` por capítulo, sem lacuna crítica
- [ ] `validar-playbook.py --estrito` retorna 0
- [ ] Capa com badge aprovada por `validar-capa-nivel.py`
- [ ] PDF gerado por `compilar-para-pdf.py --tipo playbook`
- [ ] Registrado em `derivados.json` do livro-mãe e no manifesto da coleção
