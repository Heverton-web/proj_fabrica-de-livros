// ── Template LEAD MAGNET (V5) ─────────────────────────────────────────────────
// A4, uma coluna, muita respiracao. CTA fixo no rodape de TODA pagina (R-LM-1)
// e pagina de CTA no fim. Teto de paginas cobrado por scripts/validar-lead-magnet.py.

#let cor-acento = {
  let c = "$cor_acento$"
  if c == "" { rgb("#2ecc9a") } else { rgb(c) }
}
#let cor-tinta = rgb("#151a20")
#let cor-suave = rgb("#616b78")
#let cor-clara = rgb("#f4f7f9")

#let cta-texto = "$cta_texto$"
#let cta-url = "$cta_url$"

#set document(title: "$title$", author: "$author$")

#set page(
  paper: "a4",
  margin: (top: 2.4cm, bottom: 2.6cm, left: 2.6cm, right: 2.6cm),
  header: context {
    if counter(page).get().first() > 1 {
      set text(size: 8pt, fill: cor-suave)
      align(right)[$title$]
      v(-5pt)
      line(length: 100%, stroke: 0.5pt + cor-acento.lighten(45%))
    }
  },
  // R-LM-1: o CTA acompanha o leitor em todas as paginas, nao so na ultima.
  footer: context {
    if counter(page).get().first() > 1 {
      line(length: 100%, stroke: 0.5pt + cor-acento.lighten(45%))
      v(3pt)
      set text(size: 8pt, fill: cor-suave)
      grid(columns: (1fr, auto),
        align(left)[#if cta-url != "" [#cta-texto — #link(cta-url)[#cta-url]] else [#cta-texto]],
        align(right)[#counter(page).display("1")])
    }
  },
)

#set text(font: ("Inter", "Liberation Sans", "Arial", "sans-serif"),
          size: 11pt, lang: "pt", region: "BR")
#set par(justify: false, leading: 0.78em, spacing: 1.1em)

#show raw.where(block: true): block.with(
  width: 100%, fill: cor-clara, stroke: (left: 3pt + cor-acento),
  inset: 9pt, radius: 2pt)
#show raw.where(block: false): box.with(
  fill: cor-clara, inset: (x: 3pt, y: 0pt), outset: (y: 3pt), radius: 2pt)

#set image(width: 78%, fit: "contain")

// ── Capa ──────────────────────────────────────────────────────────────────────
$if(capa_imagem)$
#page(margin: 0pt, header: none, footer: none)[
  #image("$capa_imagem$", width: 100%, height: 100%, fit: "cover")
]
$else$
#page(margin: (x: 3cm, y: 4cm), header: none, footer: none)[
  #v(2.5cm)
  #block(width: 100%, height: 6pt, fill: cor-acento)
  #v(1.4cm)
  #text(size: 36pt, weight: 900, fill: cor-tinta)[$title$]
  $if(promessa)$
  #v(0.7cm)
  #text(size: 14pt, fill: cor-suave)[$promessa$]
  $endif$
  $if(badge_nivel)$
  #v(1cm)
  #box(fill: cor-acento, inset: (x: 14pt, y: 7pt), radius: 14pt)[
    #text(size: 9pt, weight: 700, fill: white)[$badge_nivel$]
  ]
  $endif$
  #v(1fr)
  #text(size: 12pt, weight: 600, fill: cor-tinta)[$author$]
  $if(livro_mae)$
  #v(0.2cm)
  #text(size: 9pt, fill: cor-suave)[Um recorte de $livro_mae$]
  $endif$
]
$endif$

// ── Titulos ───────────────────────────────────────────────────────────────────
#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  v(0.3cm)
  text(size: 24pt, weight: 900, fill: cor-tinta)[#it.body]
  v(-2pt)
  block(width: 70pt, height: 4pt, fill: cor-acento)
  v(0.6cm)
}

#show heading.where(level: 2): it => {
  v(0.7cm)
  text(size: 14pt, weight: 800, fill: cor-acento.darken(28%))[#it.body]
  v(0.15cm)
}

#show heading.where(level: 3): it => {
  v(0.45cm)
  text(size: 11pt, weight: 700, fill: cor-tinta)[#it.body]
  v(0.1cm)
}

// Checkbox mais legivel em documento de bancada
#show "- [ ]": box(width: 11pt, height: 11pt,
                   stroke: 1pt + cor-acento, radius: 1.5pt, baseline: 1.5pt)

#show quote: it => block(
  width: 100%, fill: cor-acento.lighten(90%), inset: 12pt, radius: 3pt,
  stroke: (left: 4pt + cor-acento), text(size: 11pt, weight: 600)[#it])

#set table(stroke: 0.5pt + cor-suave.lighten(55%))
#show table.cell.where(y: 0): set text(weight: 700, fill: cor-tinta)

$body$
