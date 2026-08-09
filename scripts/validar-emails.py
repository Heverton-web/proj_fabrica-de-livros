#!/usr/bin/env python3
"""
V5 — Gate da SEQUENCIA DE E-MAILS (R-EM-1 a R-EM-4).

Uso:
    python scripts/validar-emails.py emails/<slug>--eml
    python scripts/validar-emails.py emails/<slug>--eml --estrito --json
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

MAX_CHARS_ASSUNTO = 60
MAX_PALAVRAS_EMAIL = 250

REGRAS = {
    "R-EM-1": f"assunto presente e com no maximo {MAX_CHARS_ASSUNTO} caracteres",
    "R-EM-2": "exatamente 1 CTA rastreavel (UTM) por e-mail",
    "R-EM-3": "sequencia tem abertura (entrega) + nutricao + fechamento (oferta)",
    "R-EM-4": f"nenhum e-mail passa de {MAX_PALAVRAS_EMAIL} palavras",
}

RE_ASSUNTO = re.compile(r"^\*\*Assunto:\*\*[ \t]*(.+?)[ \t]*$", re.MULTILINE)
RE_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
RE_CODIGO = re.compile(r"^[ \t]*```.*?^[ \t]*```[ \t]*$", re.DOTALL | re.MULTILINE)
RE_COMENTARIO = re.compile(r"<!--.*?-->", re.DOTALL)


def _ler_json(caminho, padrao=None):
    if caminho.exists():
        try:
            return json.loads(caminho.read_text(encoding="utf-8"))
        except ValueError:
            return padrao if padrao is not None else {}
    return padrao if padrao is not None else {}


def validar(slug):
    dir_eml = TO.dir_obra(slug, DIR_OUTPUT)
    cfg = _ler_json(dir_eml / "config_obra.json")
    plano = _ler_json(dir_eml / "plano.json")
    arquivos = sorted((dir_eml / "emails").glob("email_*.md")) \
        if (dir_eml / "emails").exists() else []

    violacoes, avisos = [], []
    def falha(regra, detalhe, email=None):
        violacoes.append({"regra": regra, "enunciado": REGRAS[regra],
                          "email": email, "detalhe": detalhe})

    if not arquivos:
        falha("R-EM-3", f"nenhum email_NN.md em {dir_eml / 'emails'}")
        return {"slug": slug, "conforme": False, "total_emails": 0,
                "violacoes": violacoes, "avisos": avisos, "regras": REGRAS}

    for caminho in arquivos:
        nome = caminho.name
        texto = caminho.read_text(encoding="utf-8", errors="replace")

        m = RE_ASSUNTO.search(texto)
        if not m:
            falha("R-EM-1", "linha '**Assunto:**' ausente", nome)
        elif len(m.group(1)) > MAX_CHARS_ASSUNTO:
            falha("R-EM-1", f"{len(m.group(1))} caracteres no assunto", nome)

        links = [u for u in RE_LINK.findall(texto)]
        rastreaveis = [u for u in links if "utm_source=email" in u]
        if len(links) != 1:
            falha("R-EM-2", f"{len(links)} link(s) — a regra e exatamente 1 CTA", nome)
        elif not rastreaveis:
            falha("R-EM-2", f"CTA sem UTM: {links[0][:60]}", nome)

        limpo = RE_COMENTARIO.sub("", RE_CODIGO.sub("", texto))
        limpo = re.sub(r"^\*\*(Assunto|Momento):\*\*.*$", "", limpo, flags=re.MULTILINE)
        palavras = len(limpo.split())
        if palavras > MAX_PALAVRAS_EMAIL:
            falha("R-EM-4", f"{palavras} palavras", nome)

    tipos = {p.get("tipo") for p in plano.get("plano", [])}
    if not {"abertura", "fechamento"} <= tipos:
        falha("R-EM-3", f"tipos presentes: {sorted(tipos) or 'nenhum'}")
    if len(arquivos) < 3:
        falha("R-EM-3", f"apenas {len(arquivos)} e-mail(s) na sequencia")

    if not (cfg.get("cta_url") or "").strip():
        falha("R-EM-2", "config_obra.json sem 'cta_url'")

    pendentes = sum(len(re.findall(r"POLIMENTO-LLM", c.read_text(encoding="utf-8", errors="replace")))
                    for c in arquivos)
    if pendentes:
        avisos.append(f"{pendentes} marcador(es) de polimento pendente(s)")

    return {"slug": slug, "total_emails": len(arquivos), "conforme": not violacoes,
            "violacoes": violacoes, "avisos": avisos, "regras": REGRAS}


def main():
    console_utf8()
    ap = argparse.ArgumentParser(description="Gate da sequencia de e-mails (R-EM-1 a R-EM-4)")
    ap.add_argument("slug", help="ex.: emails/meu-livro--eml")
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
        print(f"[{estado}] {args.slug} — {rel['total_emails']} e-mail(s)")
        for v in rel["violacoes"]:
            alvo = v.get("email") or "sequencia"
            print(f"  [{v['regra']}] {alvo}: {v['detalhe']}")
        for a in rel["avisos"]:
            print(f"  [AVISO] {a}")

    if args.estrito and not rel["conforme"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
