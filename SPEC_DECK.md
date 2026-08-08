# SPEC_DECK — Contrato do Slide Deck (V5)

> Tipo derivado de **extração determinística**. Custo alvo: **0 token**.
> Destrava aula, palestra e treinamento corporativo a partir de obra já pronta.

## 1. Fonte de derivação

| Elemento do slide | Origem |
|---|---|
| Sequência e títulos | `sumario_macro.partes[].capitulos[]` |
| Divisores de seção | Estágios (`motivo_condutor.vocabulario`) ou Partes |
| Bullets | `pilares_previstos` → fallback ⑥ `feito_quando` do card → ③ `entregas` |
| Imagens | Diagramas Mermaid **já renderizados** da §3 *Ilustra* |
| Comando de fecho | ⑤ `gate` do card |
| Slide final | CTA rastreável |

Derivação permitida: **livro → deck**, **tcc → deck**.
O playbook é opcional: se existir, enriquece os bullets; se não, o deck sai só
do sumário.

## 2. Regras (gate: `scripts/validar-deck.py`)

| Regra | Enunciado |
|---|---|
| **R-DK-1** | 1 slide por capítulo do livro-mãe, sem lacuna |
| **R-DK-2** | Nenhum slide passa de 6 bullets nem de 140 caracteres por bullet |
| **R-DK-3** | Slide final com CTA rastreável (`utm_source=deck`) |
| **R-DK-4** | Ao menos 1 diagrama a cada 5 slides (aviso, não bloqueia) |
| **R-DK-5** | Badge de nível herdado da obra-mãe |

## 3. Dois entregáveis

| Artefato | Motor | Comando |
|---|---|---|
| `.html` autocontido | HTML+CSS (`template_deck.html`) | `gerar-deck-html.py` |
| `.pdf` 16:9 | O **mesmo** HTML, via Chromium | `gerar-deck-html.py` |
| `.pptx` (opcional) | Writer nativo do Pandoc | `gerar-pptx.py` |

**O `.html` é entregável** — e aqui está a diferença para o lead magnet, onde o
HTML é camada intermediária. Um deck HTML abre no navegador, apresenta em tela
cheia (`F`), navega pelo teclado e funciona offline, sem biblioteca externa. O
PDF sai do **mesmo** arquivo, então apresentação e distribuição são idênticas.

O PPTX continua disponível para quem precisa editar no PowerPoint, mas **não
entra em `extensoes_saida` nem no pacote**: o writer do Pandoc entrega estrutura
correta e design genérico — não carrega a identidade da coleção.

### Armadilha do Pandoc no template

O template HTML passa pelo Pandoc, que trata `cifrão-chave` como variável dele.
Um template literal de JS com interpolação — **inclusive dentro de comentário** —
faz o Pandoc abortar a compilação. Use concatenação de strings.

## 4. Saída

```
output/decks/<slug-mae>--deck/
├── config_obra.json     tipo_obra=deck, cta_url, cta_texto
├── sumario_macro.json   total_slides
├── deck.md              cada `# Título` abre um slide
├── imagens/diagramas/   PNGs copiados do livro-mãe
└── revisao/
```

Formato de página: **16:9 (33,87 × 19,05 cm)**, fundo escuro, definido em
`templates/template_deck.typ`.

## 4. Pipeline

```bash
python scripts/renderizar-diagramas.py livros/<slug> --capitulos
python scripts/gerar-deck.py livros/<slug> --cta-url https://exemplo.com/livro
python scripts/validar-deck.py decks/<slug>--deck --estrito
python compilar-para-pdf.py decks/<slug>--deck --tipo deck
```

> Rodar `renderizar-diagramas.py` **antes** do `gerar-deck.py`: o deck copia
> apenas diagramas já renderizados (R-DK-4 vira aviso se não houver).
