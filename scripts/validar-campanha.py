#!/usr/bin/env python3
"""
Validar-Campanha (V5.3) — gates da camada CAMPANHA (R-CP-1 a R-CP-5).

R-CP-1 estrutura: arvore de pastas do registro existe por material.
R-CP-2 conteudo: textos nao vazios, sem copy generica (regra 12) e sem molde
    RASCUNHO pendente.
R-CP-3 artes: PNG valido (assinatura + tamanho minimo); HTML fonte ao lado.
R-CP-4 merito (--estrito): vocabulario condutor da colecao presente na copy.
R-CP-5 cronogramas: presentes, com datas futuras e PDF ao lado.
R-CP-C1 (--completo): todo material da colecao tem campanha com status completa.

Uso:
    python scripts/validar-campanha.py --material <slug> [--estrito]
    python scripts/validar-campanha.py --completo <colecao> [--estrito]
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path

import campanha as CP
import tipos_obra as TO

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

COPY_GENERICA = re.compile(r"Autor Digital|centenas de pessoas")
RASCUNHO = re.compile(r"Status:\s*RASCUNHO")
MIN_PNG = 5 * 1024


def _cronograma_primeira_data(arquivo):
    """Primeira data ISO (D+1...) encontrada no cronograma, ou None."""
    try:
        texto = Path(arquivo).read_text(encoding="utf-8")
    except OSError:
        return None
    m = re.search(r"\d{4}-\d{2}-\d{2}", texto)
    return date.fromisoformat(m.group(0)) if m else None


def _textos_da_pasta(pasta):
    return sorted(p for p in pasta.rglob("*.md") if p.is_file())


def validar_material(slug, estrito=False, base=None):
    """Gates R-CP-1..5 para um material. Retorna dict no padrao dos validadores."""
    base = Path(base) if base is not None else DIR_OUTPUT
    violacoes = []
    raiz = CP.dir_campanha_material(slug, base)

    # R-CP-1 — estrutura
    ctx = CP.contexto_material(slug, base)
    esperadas = set(CP.estrutura_material(ctx))
    existentes = set()
    if raiz.exists():
        for pasta in raiz.rglob("*"):
            if pasta.is_dir():
                existentes.add(str(pasta.relative_to(raiz)).replace("\\", "/"))
    for esperada in sorted(esperadas - existentes):
        violacoes.append({"regra": "R-CP-1", "detalhe": f"pasta ausente: {esperada}"})

    if raiz.exists():
        # R-CP-2 — conteudo
        for arquivo in _textos_da_pasta(raiz):
            eh_cronograma = arquivo.name.startswith("cronograma-")
            try:
                texto = arquivo.read_text(encoding="utf-8")
            except OSError as exc:
                violacoes.append({"regra": "R-CP-2",
                                  "detalhe": f"{arquivo.relative_to(raiz)}: {exc}"})
                continue
            if not texto.strip():
                violacoes.append({"regra": "R-CP-2",
                                  "detalhe": f"texto vazio: {arquivo.relative_to(raiz)}"})
            if COPY_GENERICA.search(texto):
                violacoes.append({"regra": "R-CP-2",
                                  "detalhe": f"copy generica em {arquivo.relative_to(raiz)}"})
            if RASCUNHO.search(texto):
                violacoes.append({"regra": "R-CP-2",
                                  "detalhe": f"molde RASCUNHO pendente: "
                                             f"{arquivo.relative_to(raiz)}"})
            if not eh_cronograma:
                pdf = arquivo.with_suffix(".pdf")
                if not pdf.exists() or pdf.stat().st_size == 0:
                    violacoes.append({"regra": "R-CP-2",
                                      "detalhe": f"sem PDF ao lado de "
                                                 f"{arquivo.relative_to(raiz)}"})

        # R-CP-3 — artes
        for png in sorted(raiz.rglob("*.png")):
            try:
                dados = png.read_bytes()
            except OSError as exc:
                violacoes.append({"regra": "R-CP-3",
                                  "detalhe": f"{png.relative_to(raiz)}: {exc}"})
                continue
            if not dados.startswith(b"\x89PNG") or len(dados) < MIN_PNG:
                violacoes.append({"regra": "R-CP-3",
                                  "detalhe": f"PNG invalido: {png.relative_to(raiz)}"})

        # R-CP-5 — cronogramas
        for crono in sorted(raiz.rglob("cronograma-*.md")):
            primeira = _cronograma_primeira_data(crono)
            if primeira is None:
                violacoes.append({"regra": "R-CP-5",
                                  "detalhe": f"sem data em {crono.relative_to(raiz)}"})
            elif primeira < date.today():
                violacoes.append({"regra": "R-CP-5",
                                  "detalhe": f"data passada em {crono.relative_to(raiz)}"})
            pdf = crono.with_suffix(".pdf")
            if not pdf.exists() or pdf.stat().st_size == 0:
                violacoes.append({"regra": "R-CP-5",
                                  "detalhe": f"sem PDF ao lado de {crono.relative_to(raiz)}"})

        # R-CP-4 — merito (vocabulario da colecao na copy)
        if estrito and ctx.get("vocabulario"):
            textos = "\n".join(t.read_text(encoding="utf-8", errors="ignore")
                               for t in _textos_da_pasta(raiz))
            termos = [v for v in ctx["vocabulario"] if len(v) > 3]
            achados = [v for v in termos if v.lower() in textos.lower()]
            if not achados:
                violacoes.append({
                    "regra": "R-CP-4",
                    "detalhe": "vocabulario condutor ausente da copy: "
                               + ", ".join(termos[:5])})

    return {"slug": slug, "conforme": not violacoes, "violacoes": violacoes}


def validar_completo(chave, estrito=False, base=None):
    """R-CP-C1: todos os materiais do manifesto com campanha 'completa'."""
    base = Path(base) if base is not None else DIR_OUTPUT
    violacoes = []
    manifesto = CP.carregar_manifesto_colecao(chave, base)
    if not manifesto:
        return {"colecao": chave, "conforme": False,
                "violacoes": [{"regra": "R-CP-C1",
                               "detalhe": f"manifesto da colecao ausente: {chave}"}]}
    estado = CP.carregar_estado(chave, base)
    por_slug = {m["slug"]: m for m in estado.get("materiais", [])}
    detalhes = []
    for membro in manifesto.get("membros", []):
        slug = membro["slug"]
        item = por_slug.get(slug, {})
        if item.get("status") != "completa":
            detalhes.append(f"{slug} ({item.get('status', 'sem campanha')})")
        else:
            rel = validar_material(slug, estrito=estrito, base=base)
            if not rel["conforme"]:
                detalhes.append(f"{slug}: " + "; ".join(
                    f"{v['regra']} {v['detalhe']}" for v in rel["violacoes"]))
    if detalhes:
        violacoes.append({"regra": "R-CP-C1",
                          "detalhe": "; ".join(detalhes)})
    return {"colecao": chave, "conforme": not violacoes, "violacoes": violacoes}


def _imprimir(rel):
    if rel["conforme"]:
        print("[OK] campanha conforme")
        return
    print("[REPROVADO]")
    for v in rel["violacoes"]:
        print(f"  {v['regra']}: {v['detalhe']}")


def main():
    TO.console_utf8()
    ap = argparse.ArgumentParser(description="Gates da campanha (R-CP-1 a R-CP-5)")
    alvo = ap.add_mutually_exclusive_group(required=True)
    alvo.add_argument("--material", metavar="SLUG")
    alvo.add_argument("--completo", metavar="COLECAO")
    ap.add_argument("--estrito", action="store_true",
                    help="habilita R-CP-4 (vocabulario condutor)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.material:
        rel = validar_material(args.material, estrito=args.estrito)
    else:
        rel = validar_completo(args.completo, estrito=args.estrito)
    if args.json:
        print(__import__("json").dumps(rel, ensure_ascii=False, indent=2))
    else:
        _imprimir(rel)
    sys.exit(0 if rel["conforme"] else 1)


if __name__ == "__main__":
    main()
