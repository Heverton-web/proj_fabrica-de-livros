---
name: pdf-pandoc-typst
description: >
  Stack padrão de conversão Markdown -> PDF via Pandoc + Typst — gratuito, rápido
  (<1s de compilação) e leve (~50MB), preferido a LaTeX/wkhtmltopdf/Puppeteer para
  qualquer documento .md que precise virar PDF neste ou em outro projeto.
  Triggers: "gerar pdf", "converter markdown para pdf", "compilar documento",
  "pandoc", "typst", "md para pdf", "exportar relatório em pdf"
---

# PDF via Pandoc + Typst

Motor padrão de PDF de qualquer projeto: Pandoc converte o `.md`, Typst renderiza
(10-50x mais rápido que LaTeX, binário único, sem gigabytes de TeX Live).
Ver ranking comparativo completo em `docs/opcoes-conversao-md-pdf.md`.

## Instalação

```bash
# Windows
winget install JohnMacFarlane.Pandoc
winget install Typst.Typst

# macOS
brew install pandoc typst

# Linux
sudo apt install pandoc   # ou o pacote da distro
cargo install typst-cli   # ou baixe o binário em github.com/typst/typst/releases
```

## Caso simples: documento sem figuras/imagens

Conversão direta, um comando:

```bash
pandoc arquivo.md -o arquivo.pdf \
  --pdf-engine=typst \
  --toc --number-sections \
  -V mainfont="Times New Roman" \
  -V geometry:margin=3cm
```

## Caso com figuras/imagens (livros, relatórios ilustrados)

**NUNCA** use `pandoc --pdf-engine=typst` direto quando o documento tem
`![](caminho/imagem.png)` — no Windows, o Pandoc grava o path da imagem como
absoluto no `.typ` intermediário e o Typst falha ao resolvê-lo. Gere o `.typ`
primeiro e compile com `--root` explícito:

```bash
# 1. Gerar o .typ (fica na MESMA pasta do markdown/imagens)
pandoc arquivo.md -o arquivo.typ --toc --number-sections

# 2. Compilar com --root apontando pra pasta (resolve as imagens por caminho relativo)
typst compile --root . arquivo.typ arquivo.pdf
```

## Template customizado (ABNT, capa, tipografia própria)

```bash
pandoc arquivo.md -o arquivo.pdf \
  --pdf-engine=typst \
  --template=template.typ \
  --toc --number-sections \
  -V mainfont="Times New Roman" \
  -V geometry:margin=3cm \
  -V fontsize=12pt
```

## Diretrizes

1. **Build/compilação é isento de economia de tokens** — Pandoc+Typst roda sem
   restrição de log/output (matches a regra "Build ISENTO" do prompt mestre de
   token economy).
2. **Figuras = sempre 2 passos** (`.typ` intermediário + `--root`) — o atalho de
   1 comando só é seguro sem imagens.
3. **Verifique o PDF gerado**: cabeçalho `%PDF-1.x` presente e tamanho não-zero
   antes de reportar a tarefa como concluída.
4. **Nomeie o `.md`/`.pdf` com o mesmo nome-base** — mantém o par rastreável no
   `git status` e evita órfãos.
