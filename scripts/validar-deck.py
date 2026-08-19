#!/usr/bin/env python3
"""
V5 — Gate do SLIDE DECK (R-DK-1 a R-DK-5).

Uso:
    python scripts/validar-deck.py decks/<slug>--deck
    python scripts/validar-deck.py decks/<slug>--deck --estrito --json
"""

import argparse
import json
import re
import sys
from pathlib import Path

from tipos_obra import console_utf8
import tipos_obra as TO

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

MAX_BULLETS_SLIDE = 6
MAX_CHARS_BULLET = 140
SLIDES_POR_DIAGRAMA = 5

REGRAS = {
    "R-DK-1": "1 slide por capitulo do livro-mae, sem lacuna",
    "R-DK-2": f"nenhum slide passa de {MAX_BULLETS_SLIDE} bullets nem de {MAX_CHARS_BULLET} caracteres por bullet",
    "R-DK-3": "slide final com CTA rastreavel (UTM)",
    "R-DK-4": f"ao menos 1 diagrama a cada {SLIDES_POR_DIAGRAMA} slides",
    "R-DK-5": "badge de nivel herdado da obra-mae (senioridade_obra)",
}

RE_ITEM = re.compile(r"^[ \t]*[-*+][ \t]+(.+?)[ \t]*$", re.MULTILINE)
RE_IMG = re.compile(r"!\[[^\]]*\]\([^)]+\)")


def _ler_json(caminho, padrao=None):
    if caminho.exists():
        try:
            return json.loads(caminho.read_text(encoding="utf-8"))
        except ValueError:
            return padrao if padrao is not None else {}
    return padrao if padrao is not None else {}


def _slides(texto):
    """Particiona o deck.md em slides (cada `# Titulo` de nivel 1 abre um slide)."""
    corpo = re.sub(r"\A---\n.*?\n---\n", "", texto, flags=re.DOTALL)
    marcas = list(re.finditer(r"^#[ \t]+(.+?)[ \t]*$", corpo, re.MULTILINE))
    saida = []
    for i, m in enumerate(marcas):
        fim = marcas[i + 1].start() if i + 1 < len(marcas) else len(corpo)
        saida.append({"titulo": m.group(1).strip(), "corpo": corpo[m.end():fim]})
    return saida


def validar(slug):
    dir_deck = TO.dir_obra(slug, DIR_OUTPUT)
    cfg = _ler_json(dir_deck / "config_obra.json")
    sumario = _ler_json(dir_deck / "sumario_macro.json")
    md = dir_deck / "deck.md"

    violacoes, avisos = [], []
    def falha(regra, detalhe):
        violacoes.append({"regra": regra, "enunciado": REGRAS[regra], "detalhe": detalhe})

    if not md.exists():
        falha("R-DK-1", f"deck.md inexistente em {dir_deck}")
        return {"slug": slug, "conforme": False, "violacoes": violacoes,
                "avisos": avisos, "regras": REGRAS}

    texto = md.read_text(encoding="utf-8", errors="replace")
    slides = _slides(texto)

    # R-DK-1 — cobertura de capitulos
    mae_simples = TO.resolver_slug_mae(cfg) or sumario.get("slug_livro_mae")
    dir_mae = None
    if mae_simples:
        # V5 (HUB POR COLECAO): o livro-mae vive em output/<colecao>/livros/<slug>,
        # nao em output/livros/<slug>. dir_obra resolve plano, por-obra e hub.
        for raiz in ("livros", "tccs"):
            candidato = TO.dir_obra(f"{raiz}/{mae_simples}", DIR_OUTPUT)
            if (candidato / "capitulos").exists():
                dir_mae = candidato
                break
    if dir_mae is not None:
        n_caps = len(list((dir_mae / "capitulos").glob("cap_*.md")))
        # capa + objetivo + mapa + divisores + capitulos + CTA
        if len(slides) < n_caps + 2:
            falha("R-DK-1", f"{len(slides)} slide(s) para {n_caps} capitulo(s)")
    else:
        avisos.append("livro-mae nao localizado — R-DK-1 nao verificado")

    # R-DK-2 — densidade
    estourados = []
    for s in slides:
        itens = RE_ITEM.findall(s["corpo"])
        if len(itens) > MAX_BULLETS_SLIDE:
            estourados.append(f"{s['titulo']!r}: {len(itens)} bullets")
        longos = [i for i in itens if len(i) > MAX_CHARS_BULLET]
        if longos:
            estourados.append(f"{s['titulo']!r}: {len(longos)} bullet(s) longo(s)")
    if estourados:
        falha("R-DK-2", "; ".join(estourados[:6]))

    # R-DK-3 — CTA
    if not (cfg.get("cta_url") or "").strip():
        falha("R-DK-3", "config_obra.json sem 'cta_url'")
    elif "utm_source=deck" not in texto:
        falha("R-DK-3", "slide final sem parametros UTM")

    # R-DK-4 — densidade visual
    diagramas = len(RE_IMG.findall(texto))
    minimo = max(1, len(slides) // SLIDES_POR_DIAGRAMA)
    if diagramas < minimo:
        avisos.append(f"{diagramas} diagrama(s) para {len(slides)} slides "
                      f"(recomendado >= {minimo}); rode renderizar-diagramas.py no livro-mae")

    # R-DK-5 — badge
    if not (cfg.get("senioridade_obra") or "").strip():
        falha("R-DK-5", "config_obra.json sem 'senioridade_obra'")

    return {"slug": slug, "total_slides": len(slides), "diagramas": diagramas,
            "conforme": not violacoes, "violacoes": violacoes,
            "avisos": avisos, "regras": REGRAS}


def main():
    console_utf8()
    ap = argparse.ArgumentParser(description="Gate do slide deck (R-DK-1 a R-DK-5)")
    ap.add_argument("slug", help="ex.: decks/meu-livro--deck")
    ap.add_argument("--estrito", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rel = validar(args.slug)
    dir_rev = TO.dir_obra(args.slug, DIR_OUTPUT) / "revisao"
    dir_rev.mkdir(parents=True, exist_ok=True)
    (dir_rev / "relatorio_gate.json").write_text(
        json.dumps(rel, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.json:
        print(json.dumps(rel, ensure_ascii=False, indent=2))
    else:
        estado = "CONFORME" if rel["conforme"] else "NAO CONFORME"
        print(f"[{estado}] {args.slug} — {rel.get('total_slides', 0)} slide(s), "
              f"{rel.get('diagramas', 0)} diagrama(s)")
        for v in rel["violacoes"]:
            print(f"  [{v['regra']}] {v['detalhe']}")
        for a in rel["avisos"]:
            print(f"  [AVISO] {a}")

    if args.estrito and not rel["conforme"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
