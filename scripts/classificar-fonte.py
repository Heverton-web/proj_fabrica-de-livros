#!/usr/bin/env python3
"""
Classificador determinístico de hierarquia de fontes A/B/C (complementa
validar-fontes.py, gate R-FT-1).

Hoje a LLM decide "(A)/(B)/(C)" na hora de escrever o dossiê para TODA fonte,
mesmo quando o dominio ja identifica a classe sem ambiguidade (arxiv.org e
sempre A; docs.anthropic.com e sempre B). Este script classifica por
dominio/padrão de URL e so deixa para julgamento humano/LLM os casos
realmente ambíguos (retorna None).

Uso:
    python scripts/classificar-fonte.py <url>                  # 1 URL
    python scripts/classificar-fonte.py --aplicar <slug>        # preenche
        classe ausente nos dossies de <slug> (nunca sobrescreve classe já
        marcada; linhas ambíguas ficam intactas para revisão)
"""

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import tipos_obra as TO
from tipos_obra import console_utf8

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

# (A) peer-reviewed/primário: papers, benchmarks, relatórios institucionais auditados.
DOMINIOS_A = {
    "arxiv.org", "dl.acm.org", "ieeexplore.ieee.org", "link.springer.com",
    "semanticscholar.org", "pubmed.ncbi.nlm.nih.gov", "ncbi.nlm.nih.gov",
    "dora.dev", "swebench.com",
}
SUFIXOS_A = (".scielo.br", "scielo.org")

# (B) documentação oficial de fornecedor, repositório de referência, normas.
DOMINIOS_B = {
    "rfc-editor.org", "iso.org", "w3.org", "github.com", "anthropic.com",
    "openai.com",
}
PREFIXOS_B = ("docs.", "developer.", "developers.")
SUFIXOS_B = (".gov",)

# (C) conteúdo superficial: blog, marketing, opinião sem dado.
DOMINIOS_C = {"medium.com", "substack.com", "dev.to", "blogspot.com"}


def _dominio(url):
    return (urlparse(url).netloc or "").lower().removeprefix("www.")


def classificar(url):
    """Retorna 'A'|'B'|'C' quando o domínio/padrão é reconhecido, ou None
    quando é ambíguo (cabe a julgamento humano/LLM)."""
    dominio = _dominio(url)
    caminho = (urlparse(url).path or "").lower()
    if not dominio:
        return None

    if dominio in DOMINIOS_A or any(dominio.endswith(s) for s in SUFIXOS_A):
        return "A"
    if dominio in DOMINIOS_C or "/blog/" in caminho:
        return "C"
    if (
        dominio in DOMINIOS_B
        or dominio.startswith(PREFIXOS_B)
        or dominio.endswith(SUFIXOS_B)
        or "/docs/" in caminho
    ):
        return "B"
    return None


RE_LINHA_FONTE = re.compile(r"^-\s.+Dispon[ií]vel em:\s*\S+.*$")
RE_URL = re.compile(r"https?://[^\s)\]}>\"'`]+")
RE_CLASSE_FIM = re.compile(r"\(([ABC])\)\s*$")


def preencher_classe_no_texto(texto):
    """Preenche '(A)/(B)/(C)' ao final de linhas de fonte sem classe explícita
    e cuja URL o classificador reconhece. Retorna (texto_novo, n_preenchidas,
    n_ambiguas). Nunca altera linha que já termina em (A)/(B)/(C)."""
    n_preenchidas = n_ambiguas = 0
    linhas_novas = []
    for linha in texto.splitlines():
        if RE_LINHA_FONTE.match(linha.strip()) and not RE_CLASSE_FIM.search(linha.strip()):
            m = RE_URL.search(linha)
            classe = classificar(m.group(0)) if m else None
            if classe:
                linha = linha.rstrip() + f" ({classe})"
                n_preenchidas += 1
            else:
                n_ambiguas += 1
        linhas_novas.append(linha)
    return "\n".join(linhas_novas), n_preenchidas, n_ambiguas


def aplicar_na_obra(slug, base=None):
    """Preenche classe ausente em todos os dossie*.md de <slug>. Retorna
    resumo {arquivo: (n_preenchidas, n_ambiguas)}."""
    dir_pesquisa = TO.dir_obra(slug, base or DIR_OUTPUT) / "pesquisa"
    resumo = {}
    if not dir_pesquisa.exists():
        return resumo
    for arq in sorted(dir_pesquisa.glob("dossie*.md")):
        texto = arq.read_text(encoding="utf-8", errors="replace")
        novo, n_pre, n_amb = preencher_classe_no_texto(texto)
        if n_pre:
            arq.write_text(novo, encoding="utf-8")
        resumo[arq.name] = (n_pre, n_amb)
    return resumo


def main():
    console_utf8()
    ap = argparse.ArgumentParser(description="Classificador determinístico de fonte A/B/C")
    ap.add_argument("url", nargs="?", help="1 URL para classificar")
    ap.add_argument("--aplicar", metavar="SLUG", help="preenche classe ausente nos dossies da obra")
    args = ap.parse_args()

    if args.aplicar:
        resumo = aplicar_na_obra(args.aplicar)
        if not resumo:
            print(f"[classificar-fonte] nenhum dossie encontrado para '{args.aplicar}'")
            return 0
        for arq, (n_pre, n_amb) in resumo.items():
            print(f"[classificar-fonte] {arq}: {n_pre} classificadas automaticamente, {n_amb} ambíguas (revisar)")
        return 0

    if not args.url:
        ap.error("informe uma URL ou use --aplicar <slug>")
    classe = classificar(args.url)
    print(classe or "ambiguo")
    return 0


if __name__ == "__main__":
    sys.exit(main())
