#!/usr/bin/env python3
"""
Validador deterministico de quebra de linha para titulo/subtitulo de capa.

Regra (docs/superpowers/specs/2026-08-06-capas-padronizadas-design.md, secao 8):
  - Maximo 2 linhas.
  - Nenhuma linha resultante pode ter exatamente 1 palavra.

Mede a largura real de cada palavra com uma fonte concreta (tenta Inter em
assets/fonts/ ou nas fontes do Windows; cai para Arial Bold/Regular quando
Inter nao estiver instalada) e simula a quebra de linha "greedy" — o mesmo
algoritmo que o navegador usa para quebrar texto numa caixa de largura fixa.

Uso como biblioteca:
    from validar_capa_texto import validar_capa

Uso como CLI:
    python scripts/validar-capa-texto.py --titulo "CODE REVIEW GRAPH" --tipo livro
"""
import argparse
import sys
from pathlib import Path

from PIL import ImageFont

FONT_DIR_WINDOWS = Path(r"C:\Windows\Fonts")
DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_FONTES_PROJETO = DIR_PROJETO / "assets" / "fonts"

# Caixa de texto = largura da capa menos padding lateral (80px de cada lado).
# V5: derivada do registro de tipos, para que um tipo novo com capa propria
# (playbook, lead-magnet, deck) nao quebre a validacao com KeyError.
try:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import tipos_obra as _TO
    LARGURA_CAIXA = {t: _TO.dimensoes_capa(t)[0] - 2 * 80
                     for t in _TO.tipos_validos() if _TO.dimensoes_capa(t)}
except Exception:  # noqa: BLE001 — o validador precisa funcionar isolado
    LARGURA_CAIXA = {}
LARGURA_CAIXA.setdefault("livro", 1600 - 2 * 80)
LARGURA_CAIXA.setdefault("ebook", 1200 - 2 * 80)
LARGURA_CAIXA_PADRAO = LARGURA_CAIXA["livro"]

FONTES_TITULO = ["Inter-Black.ttf", "Inter-ExtraBold.ttf"]
FONTES_SUBTITULO = ["Inter-Light.ttf"]
FALLBACK_TITULO = "arialbd.ttf"
FALLBACK_SUBTITULO = "arial.ttf"

TAMANHO_TITULO = 72
TAMANHO_SUBTITULO = 22


def _carregar_fonte(nomes_preferidos, fallback, tamanho):
    for nome in nomes_preferidos:
        for base in (DIR_FONTES_PROJETO, FONT_DIR_WINDOWS):
            caminho = base / nome
            if caminho.exists():
                return ImageFont.truetype(str(caminho), tamanho)
    caminho_fallback = FONT_DIR_WINDOWS / fallback
    if caminho_fallback.exists():
        return ImageFont.truetype(str(caminho_fallback), tamanho)
    return ImageFont.load_default()


def quebrar_linhas(texto, fonte, largura_caixa):
    """Simula quebra de linha 'greedy', igual a uma caixa CSS de largura fixa."""
    palavras = texto.split()
    linhas, atual = [], []
    for palavra in palavras:
        candidata = " ".join(atual + [palavra])
        if not atual or fonte.getlength(candidata) <= largura_caixa:
            atual.append(palavra)
        else:
            linhas.append(atual)
            atual = [palavra]
    if atual:
        linhas.append(atual)
    return linhas


def validar_texto(texto, fonte, largura_caixa, max_linhas=2):
    """Retorna (ok: bool, linhas: list[list[str]], motivo: str | None)."""
    if not texto or not texto.strip():
        return True, [], None
    linhas = quebrar_linhas(texto, fonte, largura_caixa)
    if len(linhas) > max_linhas:
        return False, linhas, f"{len(linhas)} linhas (maximo {max_linhas})"
    for linha in linhas:
        if len(linha) == 1:
            return False, linhas, f"linha com 1 palavra so: {linha[0]!r}"
    return True, linhas, None


def validar_capa(titulo, subtitulo, tipo="livro"):
    largura = LARGURA_CAIXA.get(tipo, LARGURA_CAIXA_PADRAO)
    fonte_titulo = _carregar_fonte(FONTES_TITULO, FALLBACK_TITULO, TAMANHO_TITULO)
    fonte_subtitulo = _carregar_fonte(FONTES_SUBTITULO, FALLBACK_SUBTITULO, TAMANHO_SUBTITULO)

    ok_t, linhas_t, motivo_t = validar_texto(titulo, fonte_titulo, largura)
    ok_s, linhas_s, motivo_s = validar_texto(subtitulo, fonte_subtitulo, largura)

    return {
        "ok": ok_t and ok_s,
        "titulo": {"ok": ok_t, "linhas": [" ".join(l) for l in linhas_t], "motivo": motivo_t},
        "subtitulo": {"ok": ok_s, "linhas": [" ".join(l) for l in linhas_s], "motivo": motivo_s},
    }


def main():
    ap = argparse.ArgumentParser(description="Valida quebra de linha de titulo/subtitulo de capa")
    ap.add_argument("--titulo", default="")
    ap.add_argument("--subtitulo", default="")
    ap.add_argument("--tipo", choices=sorted(LARGURA_CAIXA), default="livro")
    args = ap.parse_args()

    resultado = validar_capa(args.titulo, args.subtitulo, args.tipo)
    for campo in ("titulo", "subtitulo"):
        r = resultado[campo]
        status = "[OK]" if r["ok"] else "[ERRO]"
        extra = f" — {r['motivo']}" if r["motivo"] else ""
        print(f"{status} {campo}: {r['linhas']}{extra}")
    return 0 if resultado["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
