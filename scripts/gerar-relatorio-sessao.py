#!/usr/bin/env python3
"""
Gera o relatório de sessão da Fábrica (convenção V5.2) em Markdown + PDF.

Convenção (AGENTS.md, Fluxo Operacional, "Entrega de Sessão (V5.2)"):
    relatorios/<YYYY-MM-DD>-<tema-da-sessao>.md
    relatorios/<YYYY-MM-DD>-<tema-da-sessao>.pdf

Conteúdo mínimo: contexto, bugs descobertos/corrigidos (causa → fix), arquivos
alterados, validações (testes/verificações), commits feitos e resumo de entregas.

Uso:
    python scripts/gerar-relatorio-sessao.py --tema "maquina-vendas-checkout" \
        --titulo "Correções de Fluxo na Máquina de Vendas" \
        --contexto "..." --entregas "fix rota checkout" "18 testes" \
        --bugs "causa|fix|arquivo" \
        --validacoes "445 testes passando" \
        --commits "089b135 feat(...)"

Flags:
    --md-apenas   Gera só o .md (sem PDF)
    --pdf-only    Gera só o PDF a partir de um .md já existente
"""

import argparse
import shutil
import subprocess
import sys
import unicodedata
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RELATORIOS_DIR = BASE_DIR / "relatorios"
PANDOC = shutil.which("pandoc") or "pandoc"
TYPST = shutil.which("typst") or "typst"


def console_utf8():
    """Impede que um caractere fora do cp1252 derrube o script no console Windows."""
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def slug_tema(tema: str) -> str:
    """Normaliza o tema para nome de arquivo seguro (kebab-case ASCII)."""
    texto = unicodedata.normalize("NFKD", (tema or "").lower())
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    slug = "".join(c if c.isalnum() else "-" for c in texto)
    return "-".join(p for p in slug.split("-") if p)


def escapar(texto: str) -> str:
    """Escapa caracteres que o Pandoc interpretaria como markdown."""
    return texto.replace("|", "\\|").replace("\n", " ")


def montar_markdown(titulo, contexto, bugs, arquivos, validacoes, commits, entregas) -> str:
    data = date.today().isoformat()

    md = [
        f"# RELATÓRIO DE SESSÃO — {titulo}",
        "",
        f"> **Data:** {data}",
        f"> **Projeto:** Fábrica Agêntica de Publicações",
        "",
        "---",
        "",
        "## 1. Contexto",
        "",
        contexto or "_Não informado._",
        "",
        "---",
        "",
        "## 2. Bugs Descobertos e Corrigidos",
        "",
    ]

    if bugs:
        for b in bugs:
            if "|" in b:
                causa, fix, arquivo = (p.strip() for p in b.split("|", 2))
                md += [
                    f"### {causa}",
                    "",
                    f"- **Causa:** {escapar(causa)}",
                    f"- **Fix:** {escapar(fix)}",
                    f"- **Arquivo:** `{arquivo}`",
                    "",
                ]
            else:
                md += [f"- {escapar(b)}", ""]
    else:
        md += ["_Nenhum bug registrado._", ""]

    md += [
        "---",
        "",
        "## 3. Arquivos Alterados",
        "",
    ]
    if arquivos:
        md += [f"- `{a}`" for a in arquivos] + [""]
    else:
        md += ["_Não informado._", ""]

    md += [
        "---",
        "",
        "## 4. Validações",
        "",
    ]
    if validacoes:
        md += [f"- {escapar(v)}" for v in validacoes] + [""]
    else:
        md += ["_Não informado._", ""]

    md += [
        "---",
        "",
        "## 5. Commits",
        "",
    ]
    if commits:
        md += [f"- `{c}`" for c in commits] + [""]
    else:
        md += ["_Não informado._", ""]

    md += [
        "---",
        "",
        "## 6. Resumo de Entregas",
        "",
    ]
    if entregas:
        md += [f"- {escapar(e)}" for e in entregas] + [""]
    else:
        md += ["_Não informado._", ""]

    md += [
        "---",
        "",
        f"*Relatório gerado em {data} — Fábrica Agêntica de Publicações*",
        "",
    ]

    return "\n".join(md)


def gerar_pdf(md_path: Path, pdf_path: Path) -> int:
    """Converte MD → PDF via Pandoc→Typst (sem figuras, seguro)."""
    cmd = [
        PANDOC,
        str(md_path),
        "-o",
        str(pdf_path),
        "--pdf-engine=typst",
        "--toc",
        "--toc-depth=2",
        "-V",
        "papersize=a4",
        "-V",
        "margin-x=2cm",
        "-V",
        "margin-y=2cm",
        "-V",
        "fontsize=10pt",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode


def main():
    console_utf8()
    parser = argparse.ArgumentParser(
        description="Gera relatório de sessão da fábrica em MD + PDF (convenção V5.2)")
    parser.add_argument("--tema", required=True, help="Tema da sessão (vira nome de arquivo)")
    parser.add_argument("--titulo", help="Título do relatório (default: Tema)")
    parser.add_argument("--contexto", help="Contexto da sessão")
    parser.add_argument("--bugs", nargs="*", help="Bugs: 'causa|fix|arquivo'")
    parser.add_argument("--arquivos", nargs="*", help="Arquivos alterados")
    parser.add_argument("--validacoes", nargs="*", help="Validações rodadas")
    parser.add_argument("--commits", nargs="*", help="Commits feitos")
    parser.add_argument("--entregas", nargs="*", help="Resumo de entregas")
    parser.add_argument("--md-apenas", action="store_true", help="Não gerar PDF")
    parser.add_argument("--pdf-only", action="store_true", help="Gerar só PDF de .md existente")
    args = parser.parse_args()

    RELATORIOS_DIR.mkdir(exist_ok=True)
    data = date.today().isoformat()
    nome_base = f"{data}-{slug_tema(args.tema)}"
    md_path = RELATORIOS_DIR / f"{nome_base}.md"
    pdf_path = RELATORIOS_DIR / f"{nome_base}.pdf"

    if args.pdf_only:
        if not md_path.exists():
            print(f"  ✗ {md_path} não existe para gerar PDF")
            sys.exit(1)
        print(f"  → Gerando PDF de {md_path.name}...")
        rc = gerar_pdf(md_path, pdf_path)
        if rc != 0:
            print(f"  ✗ Falha na conversão (rc={rc})")
            sys.exit(rc)
        print(f"  ✅ PDF gerado: {pdf_path.name}")
        return

    titulo = args.titulo or args.tema.title()
    md = montar_markdown(
        titulo=titulo,
        contexto=args.contexto,
        bugs=args.bugs or [],
        arquivos=args.arquivos or [],
        validacoes=args.validacoes or [],
        commits=args.commits or [],
        entregas=args.entregas or [],
    )
    md_path.write_text(md, encoding="utf-8")
    print(f"  ✅ Markdown gerado: {md_path.name} ({len(md)} chars)")

    if args.md_apenas:
        print("  → --md-apenas: PDF pulado")
        return

    rc = gerar_pdf(md_path, pdf_path)
    if rc != 0:
        print(f"  ⚠️  PDF falhou (rc={rc}) — .md foi salvo; rode com --pdf-only depois")
        sys.exit(rc)
    print(f"  ✅ PDF gerado: {pdf_path.name}")

    print(f"\n  📁 {RELATORIOS_DIR}")


if __name__ == "__main__":
    main()
