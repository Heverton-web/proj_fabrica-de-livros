// ── Template SLIDE DECK (V5) ──────────────────────────────────────────────────
// Pagina 16:9 em paisagem. Cada `# Titulo` do Markdown abre um slide novo
// (pagebreak no heading de nivel 1). Texto grande, pouca densidade — o gate
// scripts/validar-deck.py cobra <= 6 bullets e <= 140 caracteres por bullet.

#let cor-acento = {
  let c = "$cor_acento$"
  if c == "" { rgb("#2ecc9a") } else { rgb(c) }
}
#let cor-fundo = rgb("#0d1117")
#let cor-tinta = rgb("#e6edf3")
#let cor-suave = rgb("#8b949e")

#set document(title: "$title$", author: "$author$")

#set page(
  width: 33.87cm, height: 19.05cm,     // 16:9
  margin: (top: 1.8cm, bottom: 1.6cm, left: 2.4cm, right: 2.4cm),
  fill: cor-fundo,
  footer: context {
    if counter(page).get().first() > 1 {
      set text(size: 10pt, fill: cor-suave)
      grid(columns: (1fr, auto),
        align(left)[$title$],
        align(right)[#counter(page).display("1")])
    }
  },
)

#set text(font: ("Inter", "Liberation Sans", "Arial", "sans-serif"),
          size: 17pt, fill: cor-tinta, lang: "pt", region: "BR")
#set par(justify: false, leading: 0.85em, spacing: 1.3em)

#show raw.where(block: true): block.with(
  width: 100%, fill: rgb("#161b22"), stroke: (left: 4pt + cor-acento),
  inset: 12pt, radius: 3pt)
#show raw.where(block: false): box.with(
  fill: rgb("#161b22"), inset: (x: 5pt, y: 1pt), outset: (y: 4pt), radius: 3pt)
#show raw: set text(size: 14pt, fill: cor-acento.lighten(25%))

#set image(width: 62%, fit: "contain")
#show figure: it => { align(center, it) }

#set list(marker: text(fill: cor-acento)[▸], spacing: 1.4em)

// ── Slide de capa ─────────────────────────────────────────────────────────────
#page(footer: none)[
  #v(1fr)
  #block(width: 120pt, height: 6pt, fill: cor-acento)
  #v(0.9cm)
  #text(size: 46pt, weight: 900)[$title$]
  $if(subtitle)$
  #v(0.5cm)
  #text(size: 20pt, fill: cor-suave)[$subtitle$]
  $endif$
  $if(badge_nivel)$
  #v(0.8cm)
  #box(fill: cor-acento, inset: (x: 16pt, y: 8pt), radius: 16pt)[
    #text(size: 12pt, weight: 700, fill: cor-fundo)[$badge_nivel$]
  ]
  $endif$
  #v(1fr)
  #text(size: 16pt, weight: 600)[$author$]
  $if(livro_mae)$
  #v(0.2cm)
  #text(size: 12pt, fill: cor-suave)[Baseado em $livro_mae$]
  $endif$
]

// ── Cada H1 abre um slide ─────────────────────────────────────────────────────
#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  v(0.2cm)
  text(size: 32pt, weight: 900, fill: cor-tinta)[#it.body]
  v(-6pt)
  block(width: 90pt, height: 5pt, fill: cor-acento)
  v(0.7cm)
}

#show heading.where(level: 2): it => {
  v(0.4cm)
  text(size: 21pt, weight: 700, fill: cor-acento)[#it.body]
  v(0.15cm)
}

#show heading.where(level: 3): it => {
  v(0.3cm)
  text(size: 17pt, weight: 700, fill: cor-suave)[#it.body]
}

#show quote: it => block(
  width: 100%, inset: (left: 14pt), stroke: (left: 4pt + cor-acento),
  text(size: 16pt, fill: cor-suave)[#it])

#set table(stroke: 0.6pt + cor-suave.darken(30%))
#show table.cell.where(y: 0): set text(weight: 700, fill: cor-acento)

$body$
