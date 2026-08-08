// ── Template PLAYBOOK (V5) ────────────────────────────────────────────────────
// Documento de bancada: capa grafica + objetivo + cards de passo.
// NAO tem ficha catalografica, folha de rosto nem secao de referencias — o
// playbook nao e obra catalogada (ver SPEC_PLAYBOOK.md, R-PBK-0).

#let cor-acento = {
  let c = "$cor_acento$"
  if c == "" { rgb("#2ecc9a") } else { rgb(c) }
}
#let cor-tinta = rgb("#1a1f26")
#let cor-suave = rgb("#5b6470")
#let cor-clara = rgb("#f2f5f7")

#set document(title: "$title$", author: "$author$")

#set page(
  paper: "a4",
  margin: (top: 2.2cm, bottom: 2cm, left: 2.2cm, right: 2.2cm),
  header: context {
    if counter(page).get().first() > 1 {
      set text(size: 8.5pt, fill: cor-suave)
      grid(columns: (1fr, auto),
        align(left)[$title$],
        align(right)[$badge_nivel$])
      v(-6pt)
      line(length: 100%, stroke: 0.6pt + cor-acento)
    }
  },
  footer: context {
    if counter(page).get().first() > 1 {
      set text(size: 8.5pt, fill: cor-suave)
      align(center)[#counter(page).display("1") / #counter(page).final().first()]
    }
  },
)

#set text(font: ("Inter", "Liberation Sans", "Arial", "sans-serif"),
          size: 10.5pt, lang: "pt", region: "BR")
#set par(justify: false, leading: 0.68em)

#show raw.where(block: true): block.with(
  width: 100%, fill: cor-clara, stroke: (left: 2.5pt + cor-acento),
  inset: 8pt, radius: 2pt,
)
#show raw.where(block: false): box.with(
  fill: cor-clara, inset: (x: 3pt, y: 0pt), outset: (y: 3pt), radius: 2pt)

#set image(width: 82%, fit: "contain")
#show figure: it => { v(0.5em); align(center, it); v(0.5em) }

// ── Capa grafica ──────────────────────────────────────────────────────────────
$if(capa_imagem)$
#page(margin: 0pt, header: none, footer: none)[
  #image("$capa_imagem$", width: 100%, height: 100%, fit: "cover")
]
$else$
#page(margin: (x: 2.5cm, y: 4cm), header: none, footer: none)[
  #v(3cm)
  #block(width: 100%, height: 5pt, fill: cor-acento)
  #v(1.2cm)
  #text(size: 34pt, weight: 900, fill: cor-tinta)[$title$]
  #v(0.5cm)
  #text(size: 13pt, fill: cor-suave)[$subtitle$]
  #v(0.8cm)
  $if(badge_nivel)$
  #box(fill: cor-acento, inset: (x: 12pt, y: 6pt), radius: 12pt)[
    #text(size: 9pt, weight: 700, fill: white)[$badge_nivel$]
  ]
  $endif$
  #v(1fr)
  #text(size: 12pt, weight: 600, fill: cor-tinta)[$author$]
]
$endif$

// ── Objetivo do material ──────────────────────────────────────────────────────
$if(objetivo_material)$
#page(header: none)[
  #v(1.5cm)
  #text(size: 20pt, weight: 800, fill: cor-tinta)[Objetivo do Material]
  #v(-4pt)
  #block(width: 60pt, height: 3.5pt, fill: cor-acento)
  #v(0.8cm)
  #text(size: 12pt)[$objetivo_material$]
  #v(1cm)
  #block(width: 100%, fill: cor-clara, inset: 12pt, radius: 3pt)[
    #set text(size: 9.5pt, fill: cor-suave)
    $if(livro_mae)$*Obra-mãe:* $livro_mae$ \ $endif$
    $if(total_passos)$*Passos práticos:* $total_passos$ \ $endif$
    $if(persona)$*Você é:* $persona$$endif$
  ]
]
$endif$

// ── Sumario ───────────────────────────────────────────────────────────────────
$if(toc)$
#outline(title: [Sumário], depth: 2, indent: auto)
#pagebreak()
$endif$

// ── Estilos de titulo (cards) ─────────────────────────────────────────────────
// H1 = secao do playbook (Objetivo, Mapa, Passos, Checklist)
#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  v(0.4cm)
  text(size: 20pt, weight: 800, fill: cor-tinta)[#it.body]
  v(-4pt)
  block(width: 60pt, height: 3.5pt, fill: cor-acento)
  v(0.5cm)
}

// H2 = CARD de passo — caixa com filete na cor de acento
#show heading.where(level: 2): it => {
  v(0.7cm)
  block(
    width: 100%, fill: cor-acento.lighten(88%),
    stroke: (left: 4pt + cor-acento), inset: (x: 10pt, y: 8pt), radius: 2pt,
    text(size: 14pt, weight: 800, fill: cor-tinta)[#it.body],
  )
  v(0.3cm)
}

// H3 = parte do card (① a ⑦)
#show heading.where(level: 3): it => {
  v(0.35cm)
  text(size: 10.5pt, weight: 700, fill: cor-acento.darken(25%))[#it.body]
  v(0.1cm)
}

#show quote: it => block(
  width: 100%, fill: cor-clara, inset: 9pt, radius: 2pt,
  stroke: (left: 2.5pt + cor-suave), text(size: 9.5pt, fill: cor-suave)[#it],
)

#set table(stroke: 0.5pt + cor-suave.lighten(50%))
#show table.cell.where(y: 0): set text(weight: 700, fill: cor-tinta)

$body$
