#let horizontalrule = line(start: (25%,0%), end: (75%,0%))

#show terms.item: it => block(breakable: false)[
  #text(weight: "bold")[#it.term]
  #block(inset: (left: 1.5em, top: -0.4em))[#it.description]
]

#set table(
  inset: 6pt,
  stroke: none
)

#show figure.where(
  kind: table
): set figure.caption(position: top)

#show figure.where(
  kind: image
): set figure.caption(position: bottom)

#let content-to-string(content) = {
  if content.has("text") {
    content.text
  } else if content.has("children") {
    content.children.map(content-to-string).join("")
  } else if content.has("body") {
    content-to-string(content.body)
  } else if content == [ ] {
    " "
  }
}
#let conf(
  title: none,
  subtitle: none,
  authors: (),
  keywords: (),
  date: none,
  abstract-title: none,
  abstract: none,
  thanks: none,
  cols: 1,
  margin: (x: 1.25in, y: 1.25in),
  paper: "us-letter",
  lang: "en",
  region: "US",
  font: none,
  fontsize: 11pt,
  mathfont: none,
  codefont: none,
  linestretch: 1,
  sectionnumbering: none,
  linkcolor: none,
  citecolor: none,
  filecolor: none,
  pagenumbering: "1",
  doc,
) = {
  set document(
    title: title,
    keywords: keywords,
  )
  set document(
      author: authors.map(author => content-to-string(author.name)).join(", ", last: " & "),
  ) if authors != none and authors != ()
  set page(
    paper: paper,
    margin: margin,
    numbering: pagenumbering,
    columns: cols
  )

  set par(
    justify: true,
    leading: linestretch * 0.65em
  )
  set text(lang: lang,
           region: region,
           size: fontsize)

  set text(font: font) if font != none
  show math.equation: set text(font: mathfont) if mathfont != none
  show raw: set text(font: codefont) if codefont != none

  set heading(numbering: sectionnumbering)

  show link: set text(fill: rgb(content-to-string(linkcolor))) if linkcolor != none
  show ref: set text(fill: rgb(content-to-string(citecolor))) if citecolor != none
  show link: this => {
    if filecolor != none and type(this.dest) == label {
      text(this, fill: rgb(content-to-string(filecolor)))
    } else {
      text(this)
    }
  }

  if title != none {
    place(top, float: true, scope: "parent", clearance: 4mm, block(below: 1em, width: 100%)[
      #if title != none {
        align(center, block[
            #text(weight: "bold", size: 1.5em, hyphenate: false)[#title #if thanks != none {
                footnote(thanks, numbering: "*")
                counter(footnote).update(n => n - 1)
              }]
            #(
              if subtitle != none {
                parbreak()
                text(weight: "bold", size: 1.25em, hyphenate: false)[#subtitle]
              }
             )])
      }

      #if authors != none and authors != [] {
        let count = authors.len()
        let ncols = calc.min(count, 3)
        grid(
          columns: (1fr,) * ncols,
          row-gutter: 1.5em,
          ..authors.map(author => align(center)[
            #author.name \
            #author.affiliation \
            #author.email
          ])
        )
      }

      #if date != none {
        align(center)[#block(inset: 1em)[
            #date
          ]]
      }

      #if abstract != none {
        block(inset: 2em)[
          #text(weight: "semibold")[#abstract-title] #h(1em) #abstract
        ]
      }
    ])
  }
  doc
}
#show: doc => conf(
  abstract-title: [Abstract],
  pagenumbering: "1",
  cols: 1,
  doc,
)


= Roteador Inteligente de LLMs Gratuitas por Tipo de Tarefa
<roteador-inteligente-de-llms-gratuitas-por-tipo-de-tarefa>
#strong[Data:] 2026-08-17 #strong[Status:] IMPLEMENTADO
#strong[Arquivo:] `scripts/task_router.py`

#horizontalrule

== 1. Problema
<problema>
O `detectar_llms_gratuitas.py` mapeia provedores ativos mas #strong[não
decide qual usar]. O operador precisa: 1. Escolher manualmente o
provedor certo para cada tarefa 2. Trocar de provedor quando a cota
acaba 3. Configurar o modelo correto no harness

== 2. Solução: Roteador por Tipo de Tarefa
<solução-roteador-por-tipo-de-tarefa>
Criar `scripts/task_router.py` que: - #strong[Detecta tipo de tarefa]
(coding, reasoning, creative, chat, embedding, vision) por keywords do
prompt - #strong[Seleciona melhor provedor] para aquela tarefa (ordem de
preferência por latência/qualidade) - #strong[Fallback automático]
quando o provedor primário não tem chave configurada - #strong[Quota
tracking] em `~/.task_router_quota.json` --- provedor que estourou cota
é temporariamente bloqueado - #strong[Output shell]
(`export ORCA_PROVIDER=... ORCA_MODEL=...`) para integração com qualquer
harness

== 3. Mapeamento Tarefa → Provedor
<mapeamento-tarefa-provedor>
#figure(
  align(center)[#table(
    columns: (17.39%, 41.3%, 41.3%),
    align: (auto,auto,auto,),
    table.header([Tarefa], [Provedores (ordem)], [Modelo Recomendado],),
    table.hline(),
    [#strong[coding]], [groq → cerebras → google → openrouter →
    nvidia], [llama-3.3-70b-versatile],
    [#strong[reasoning]], [google → groq → nvidia → openrouter →
    cerebras], [gemini-1.5-pro],
    [#strong[creative]], [openrouter → google → groq → siliconflow →
    nvidia], [meta-llama/llama-3.3-70b-instruct:free],
    [#strong[analysis]], [google → groq → cerebras → openrouter →
    nvidia], [gemini-1.5-pro],
    [#strong[chat]], [groq → google → openrouter → huggingface →
    siliconflow], [llama-3.3-70b-versatile],
    [#strong[embedding]], [huggingface → siliconflow → cohere → nvidia →
    fireworks], [BGE-M3 / embed-v4],
    [#strong[vision]], [google → openrouter → nvidia → siliconflow →
    fireworks], [gemini-1.5-pro],
  )]
  , kind: table
  )

== 4. Uso
<uso>
```bash
# Linha de comando
python scripts/task_router.py "debug this Python function"
# → export ORCA_PROVIDER=groq ORCA_MODEL=llama-3.3-70b-versatile

# Integrado ao shell
eval $(python scripts/task_router.py "escreva um poema")
# Define ORCA_PROVIDER + ORCA_MODEL automaticamente

# Comando Orca em seguida
orca "continue a implementação"
# Usa groq + llama-3.3-70b-versatile
```

== 5. Arquivos
<arquivos>
#figure(
  align(center)[#table(
    columns: (45%, 55%),
    align: (auto,auto,),
    table.header([Arquivo], [Descrição],),
    table.hline(),
    [`scripts/task_router.py`], [Script principal --- roteador + quota
    tracker],
    [`~/.task_router_quota.json`], [Estado de quotas por provedor
    (auto-gerenciado)],
  )]
  , kind: table
  )

== 6. Integração com Orca/MiMoCode
<integração-com-orcamimocode>
O MiMoCode já tem `ai-router`, `orcarouter`, `openrouter`, `unorouter`,
`fastrouter`, `trustedrouter` no cache de modelos. O `task_router.py`
seta `ORCA_PROVIDER` e `ORCA_MODEL` que o Orca respeita quando
definidos.

== 7. Quota Tracking
<quota-tracking>
O script mantém `~/.task_router_quota.json` com:

```json
{
  "groq": {"remaining": 14400, "reset": "2026-08-18T00:00:00Z"},
  "cerebras": {"remaining": 1000000, "reset": "2026-08-18T00:00:00Z"}
}
```

Quando `remaining` chega a 0, o provedor é bloqueado até `reset`.

== 8. Verificação
<verificação>
+ `python scripts/task_router.py "debug code"` → groq +
  llama-3.3-70b-versatile
+ `python scripts/task_router.py "write a poem"` → openrouter +
  llama-3.3-70b:free
+ `python scripts/task_router.py "analyze data"` → google +
  gemini-1.5-pro
+ `python scripts/task_router.py "embed search"` → huggingface + BGE-M3
+ `python scripts/task_router.py "describe image"` → google +
  gemini-1.5-pro

#horizontalrule

#strong[Decisão:] Boring/safe --- usa `.env` + python-dotenv (já
funcionando), não inventa middleware nem dependência externa. Roteamento
por keyword + fallback em cascade. Quota tracking em JSON local (sem
banco).
