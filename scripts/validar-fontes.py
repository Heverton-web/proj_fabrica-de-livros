#!/usr/bin/env python3
"""
F2 — Gate de HIERARQUIA DE FONTES (R-FT-1 a R-FT-3).

O dossiê de pesquisa (Fase 1) deve classificar cada fonte pela hierarquia A/B/C
e o conjunto precisa ser >= 70% de fontes A (peer-reviewed/primária) e B
(documentação oficial). Fontes C (blogs/superficiais) entram com moderação.

Hierarquia (contrato com a skill pesquisador):
  (A) — peer-reviewed: papers arXiv/ACM/IEEE/Springer/SciELO, benchmarks,
        surveys, relatórios institucionais auditados (DORA, Gartner Research)
  (B) — documentação oficial: docs.anthropic.com, arxiv.org, repo de referência,
        normas (RFC, ISO), documentação de ferramentas
  (C) — blog, marketing, conteúdo superficial, post de opinião sem dado

Marcação aceita no dossiê:
  - final da linha: `... Disponível em: URL. Acesso em: 10 ago. 2026. (A)`
  - linha própria:  `**Classe:** B`  ou  `Classe: C`

R-FT-1: >= 70% das fontes com classificação explícita são A ou B.
R-FT-2: sem classificação explícita no dossiê => nao_verificado (não reprova;
        o dossiê antigo fica pendente de reclassificação, não é bloqueado).
R-FT-3: fontes não classificadas não contam na proporção (informadas no
        relatório para o revisor).

Uso:
    python scripts/validar-fontes.py <slug>
    python scripts/validar-fontes.py <slug> --estrito   # exit 1 se falha
    python scripts/validar-fontes.py <slug> --json

Relatório: output/<slug>/validacao/relatorio_fontes.json
"""

import argparse
import json
import re
import sys
from pathlib import Path

import tipos_obra as TO
from tipos_obra import console_utf8

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

LIMIAR_AB = 0.70  # R-FT-1

RE_CLASSE_FIM_LINHA = re.compile(r"\(([ABC])\)\s*$", re.MULTILINE)
RE_CLASSE_LINHA = re.compile(r"^\**Classe:\**\s*([ABC])\s*$", re.MULTILINE)

REGRAS = {
    "R-FT-1": ">= 70% das fontes com classificação explícita são A ou B",
    "R-FT-2": "dossiê sem classificação explícita => nao_verificado (não reprova)",
    "R-FT-3": "fontes não classificadas não contam na proporção",
}


def classificar_dossie(texto):
    """Retorna (classes, total_linhas_fonte).

    classes: dict {A: n, B: n, C: n} das linhas com marcador explícito.
    total_linhas_fonte: linhas de item de fonte (referência bibliográfica)
    presentes no dossiê, para dimensionar a cobertura da classificação.
    """
    classes = {"A": 0, "B": 0, "C": 0}
    for m in RE_CLASSE_FIM_LINHA.finditer(texto or ""):
        classes[m.group(1)] += 1
    for m in RE_CLASSE_LINHA.finditer(texto or ""):
        classes[m.group(1)] += 1
    linhas_fonte = sum(
        1 for linha in (texto or "").splitlines()
        if re.search(r"Disponível em:\s*https?://", linha)
        or re.search(r"Disponível em:\s*<", linha))
    return classes, linhas_fonte


def validar(dir_obra):
    """Valida os dossiês de pesquisa da obra; retorna dict de relatório."""
    dir_pesquisa = dir_obra / "pesquisa"
    dossies = sorted(dir_pesquisa.glob("*.md")) if dir_pesquisa.exists() else []
    classes_totais = {"A": 0, "B": 0, "C": 0}
    linhas_fonte_total = 0
    por_dossie = []

    for d in dossies:
        texto = d.read_text(encoding="utf-8", errors="replace")
        classes, linhas_fonte = classificar_dossie(texto)
        for k in classes:
            classes_totais[k] += classes[k]
        linhas_fonte_total += linhas_fonte
        por_dossie.append({
            "arquivo": d.name,
            "classes": classes,
            "linhas_fonte": linhas_fonte,
        })

    classificadas = sum(classes_totais.values())
    ab = classes_totais["A"] + classes_totais["B"]
    proporcao_ab = (ab / classificadas) if classificadas else None

    violacoes = []
    status = "conforme"
    if not dossies or classificadas == 0:
        status = "nao_verificado"
        violacoes.append({
            "regra": "R-FT-2", "enunciado": REGRAS["R-FT-2"],
            "detalhe": ("nenhuma fonte com classificação (A)/(B)/(C) no dossiê — "
                        "reclassificar com a skill pesquisador V5.3")})
    elif proporcao_ab < LIMIAR_AB:
        status = "falha"
        violacoes.append({
            "regra": "R-FT-1", "enunciado": REGRAS["R-FT-1"],
            "detalhe": (f"{ab}/{classificadas} fontes A+B = "
                        f"{proporcao_ab:.0%} (mínimo {LIMIAR_AB:.0%})")})

    return {
        "dossies": [p["arquivo"] for p in por_dossie],
        "por_dossie": por_dossie,
        "classes": classes_totais,
        "linhas_fonte_total": linhas_fonte_total,
        "classificadas": classificadas,
        "proporcao_ab": round(proporcao_ab, 3) if proporcao_ab is not None else None,
        "status": status,
        "violacoes": violacoes,
        "regras": REGRAS,
    }


def main():
    ap = argparse.ArgumentParser(
        description="Gate F2 de hierarquia de fontes (A/B/C) do dossiê de pesquisa")
    ap.add_argument("slug")
    ap.add_argument("--estrito", action="store_true", help="exit 1 se houver falha")
    ap.add_argument("--json", action="store_true", help="imprime relatorio JSON completo")
    args = ap.parse_args()

    dir_obra = TO.dir_obra(args.slug, DIR_OUTPUT)
    if not dir_obra.exists():
        print(f"[ERRO] Obra nao encontrada: {dir_obra}")
        return 1

    relatorio = validar(dir_obra)
    relatorio["slug"] = args.slug

    dir_val = dir_obra / "validacao"
    dir_val.mkdir(exist_ok=True)
    (dir_val / "relatorio_fontes.json").write_text(
        json.dumps(relatorio, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Gate de Hierarquia de Fontes - {args.slug}")
    print(f"  dossies               : {', '.join(relatorio['dossies']) or '(nenhum)'}")
    print(f"  linhas de fonte       : {relatorio['linhas_fonte_total']}")
    print(f"  classificacoes        : {relatorio['classificadas']}"
          f" (A={relatorio['classes']['A']}, B={relatorio['classes']['B']}, "
          f"C={relatorio['classes']['C']})")
    if relatorio["proporcao_ab"] is not None:
        print(f"  proporcao A+B         : {relatorio['proporcao_ab']:.0%}"
              f" (minimo {LIMIAR_AB:.0%})")
    print(f"  status                : {relatorio['status']}")

    if relatorio["violacoes"]:
        for v in relatorio["violacoes"]:
            print(f"  [FALHA] {v['regra']} — {v['detalhe']}")
    elif relatorio["status"] == "conforme":
        print("\n[OK] Proporcao de fontes A/B acima do limiar")

    print(f"\nRelatorio: {(dir_val / 'relatorio_fontes.json').relative_to(DIR_PROJETO)}")

    if args.json:
        print(json.dumps(relatorio, ensure_ascii=False, indent=2))

    if args.estrito and relatorio["status"] == "falha":
        return 1
    return 0


if __name__ == "__main__":
    console_utf8()
    sys.exit(main())
