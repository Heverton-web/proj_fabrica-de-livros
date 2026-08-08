#!/usr/bin/env python3
"""
V5 — Compilador PPTX do SLIDE DECK (writer nativo do Pandoc, dependencia zero).

O deck ja sai em PDF 16:9 pelo Typst. Este script entrega o SEGUNDO artefato: um
`.pptx` EDITAVEL, que e o que a maior parte do publico corporativo espera receber.
Nao substitui o PDF — os dois convivem (`extensoes_saida` do tipo deck).

Identidade visual: o writer pptx do Pandoc nao le o template Typst. Ela vem do
`--reference-doc`. Este script cria o reference a partir do default do Pandoc na
primeira execucao e INJETA a cor de acento da colecao no tema (ppt/theme/theme1.xml),
para que o PPTX saia com a mesma cor do PDF e da capa.

Uso:
    python scripts/gerar-pptx.py decks/<slug>--deck
    python scripts/gerar-pptx.py decks/<slug>--deck --recriar-reference
    python scripts/gerar-pptx.py --todos
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import tipos_obra as TO

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"
DIR_TEMPLATES = DIR_PROJETO / "templates"

PANDOC = "pandoc"
SLIDE_LEVEL = 1          # cada `# Titulo` do deck.md abre um slide
TIMEOUT = 120

# accent1 do tema Office; e a cor que os placeholders de titulo/realce herdam.
RE_ACCENT1 = re.compile(rb'(<a:accent1>\s*<a:srgbClr val=")[0-9A-Fa-f]{6}(")')


def _ler_json(caminho, padrao=None):
    if caminho.exists():
        try:
            return json.loads(caminho.read_text(encoding="utf-8"))
        except ValueError:
            return padrao if padrao is not None else {}
    return padrao if padrao is not None else {}


def _hex_limpo(cor, padrao="2ECC9A"):
    """'#a855f7' -> 'A855F7'. Devolve o padrao se a cor for invalida."""
    bruto = (cor or "").strip().lstrip("#").upper()
    return bruto if re.fullmatch(r"[0-9A-F]{6}", bruto) else padrao


def criar_reference(destino, recriar=False):
    """Extrai o reference.pptx padrao do Pandoc. Idempotente."""
    destino = Path(destino)
    if destino.exists() and not recriar:
        return destino
    destino.parent.mkdir(parents=True, exist_ok=True)
    resultado = subprocess.run(
        [PANDOC, "--print-default-data-file", "reference.pptx"],
        capture_output=True, timeout=TIMEOUT,
    )
    if resultado.returncode != 0 or not resultado.stdout:
        raise RuntimeError(
            "pandoc nao devolveu o reference.pptx padrao: "
            f"{(resultado.stderr or b'').decode('utf-8', 'replace')[-300:]}")
    destino.write_bytes(resultado.stdout)
    return destino


def aplicar_cor_no_tema(origem, destino, cor_hex):
    """Reescreve o .pptx trocando accent1 do tema pela cor da colecao.

    Um .pptx e um zip; o tema vive em ppt/theme/theme1.xml. Reescrever o zip
    inteiro (em vez de editar in-place) mantem a operacao deterministica e
    reexecutavel. Devolve True se a substituicao ocorreu."""
    origem, destino = Path(origem), Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    substituiu = False

    with zipfile.ZipFile(origem, "r") as zin:
        itens = [(i, zin.read(i.filename)) for i in zin.infolist()]

    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as zout:
        for info, dados in itens:
            if info.filename.startswith("ppt/theme/") and info.filename.endswith(".xml"):
                novos, n = RE_ACCENT1.subn(rb"\g<1>" + cor_hex.encode() + rb"\g<2>", dados)
                if n:
                    dados, substituiu = novos, True
            zout.writestr(info, dados)
    return substituiu


def compilar(slug, recriar_reference=False):
    dir_deck = DIR_OUTPUT / slug
    md = dir_deck / "deck.md"
    if not md.exists():
        print(f"[ERRO] deck.md nao encontrado em {dir_deck}")
        return None

    config = _ler_json(dir_deck / "config_obra.json")
    sumario = _ler_json(dir_deck / "sumario_macro.json")
    tipo = config.get("tipo_obra") or TO.tipo_por_prefixo(slug) or "deck"

    referencia = TO.referencia_pptx(tipo) or (DIR_TEMPLATES / "reference_deck.pptx")
    try:
        criar_reference(referencia, recriar=recriar_reference)
    except (RuntimeError, OSError, subprocess.SubprocessError) as exc:
        print(f"[AVISO] reference.pptx indisponivel ({exc}); seguindo com o tema padrao")
        referencia = None

    # Cor da colecao no tema — mesma resolucao usada pela capa e pelo PDF
    cor = ""
    try:
        from series_capa import resolver_cor, resolver_serie_key
        cor = resolver_cor(resolver_serie_key(config, slug), slug)
    except Exception:  # noqa: BLE001 — cor e cosmetica, nao bloqueia a compilacao
        cor = ""

    if referencia is not None and cor:
        tematizado = dir_deck / "_reference_tematizado.pptx"
        try:
            if aplicar_cor_no_tema(referencia, tematizado, _hex_limpo(cor)):
                referencia = tematizado
            else:
                print("[AVISO] accent1 nao encontrado no tema; usando reference original")
        except (zipfile.BadZipFile, OSError) as exc:
            print(f"[AVISO] nao foi possivel tematizar o reference ({exc})")

    pptx = dir_deck / f"{Path(slug).name}.pptx"
    comando = [
        PANDOC, str(md), "-o", str(pptx),
        "--slide-level", str(SLIDE_LEVEL),
        "--from", "markdown-citations",
        "--resource-path", str(dir_deck),
    ]
    if referencia is not None:
        comando += ["--reference-doc", str(referencia)]

    resultado = subprocess.run(comando, capture_output=True, text=True, timeout=TIMEOUT)
    if not pptx.exists() or pptx.stat().st_size == 0:
        erro = (resultado.stderr or resultado.stdout or "").strip()[-400:]
        print(f"[ERRO] pandoc nao gerou o PPTX: {erro}")
        return None

    # O reference tematizado e intermediario, como o .typ — nao e entregavel.
    tmp = dir_deck / "_reference_tematizado.pptx"
    if tmp.exists():
        tmp.unlink()

    return {
        "slug": slug,
        "pptx": str(pptx.relative_to(DIR_OUTPUT)),
        "kb": pptx.stat().st_size // 1024,
        "slides_declarados": sumario.get("total_slides"),
        "cor_acento": cor,
    }


def main():
    TO.console_utf8()
    ap = argparse.ArgumentParser(description="Compila o deck em PPTX editavel (Pandoc)")
    ap.add_argument("slug", nargs="?", help="ex.: decks/meu-livro--deck")
    ap.add_argument("--todos", action="store_true", help="compila todos em output/decks/")
    ap.add_argument("--recriar-reference", action="store_true",
                    help="regrava templates/reference_deck.pptx a partir do padrao do Pandoc")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if shutil.which(PANDOC) is None:
        print("[ERRO] pandoc nao encontrado no PATH")
        return 1

    if args.todos:
        raiz = DIR_OUTPUT / TO.raiz_output("deck")
        alvos = [f"decks/{d.name}" for d in sorted(raiz.iterdir()) if d.is_dir()] \
            if raiz.exists() else []
    elif args.slug:
        alvos = [args.slug]
    else:
        print("[ERRO] informe <slug> ou use --todos")
        return 1

    metas = []
    for alvo in alvos:
        meta = compilar(alvo, recriar_reference=args.recriar_reference)
        if meta:
            metas.append(meta)
            if not args.json:
                print(f"[OK] {meta['pptx']} ({meta['kb']} KB, "
                      f"{meta['slides_declarados']} slides, cor {meta['cor_acento']})")

    if args.json:
        print(json.dumps(metas, ensure_ascii=False, indent=2))
    return 0 if len(metas) == len(alvos) else 1


if __name__ == "__main__":
    sys.exit(main())
