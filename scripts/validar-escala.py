#!/usr/bin/env python3
"""
F1 — Gate de ESCALABILIDADE HONESTA (R-ES-1 e R-ES-2).

A seção Aplica (5) de cada capítulo precisa declarar os LIMITES da solução:
até onde escala, onde quebra, quando não usar. Impede o modo de falha do livro
que promete "escala para qualquer tamanho" sem contorno nenhum.

R-ES-1: a seção Aplica contém ao menos 1 termo de escala/limite.
R-ES-2: algum desses termos está em contexto de ADVERTÊNCIA (limite, condição
        de contorno, quando não usar) — prosa de marketing sem contorno reprova.

Termos de escala (gatilhos): escala, escalar, escalabilidade, limite, limiar,
teto, gargalo, contorno, saturação, throughput, capacidade, até quando, até
onde, quando não, quando nao, não funciona, nao funciona, trade-off, tradeoff,
cuidado, evite, degradação, fallback, threshold, bom até, funciona até.

Contexto de advertência: a frase que contém o termo também contém um marcador
de limite (até, quando, limite, não, nao, cuidado, evite, acima, abaixo,
apenas, somente, se, menos que, mais que, depender, desaconselha).

Uso:
    python scripts/validar-escala.py <slug>
    python scripts/validar-escala.py <slug> --capitulo 7
    python scripts/validar-escala.py <slug> --md docs/x.md
    python scripts/validar-escala.py <slug> --estrito   # exit 1 se falha
    python scripts/validar-escala.py <slug> --json

Relatório: output/<slug>/validacao/relatorio_escala.json
"""

import argparse
import json
import re
import sys
from pathlib import Path

from secoes_eita import dividir_secoes, secao_por_nome, sem_codigo

import tipos_obra as TO
from tipos_obra import console_utf8

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

TERMOS_ESCALA = (
    "escala", "escalar", "escalabilidade", "escalável", "escalavel",
    "limite", "limiar", "threshold", "teto", "gargalo", "contorno",
    "saturação", "saturacao", "throughput", "capacidade",
    "até quando", "ate quando", "até onde", "ate onde",
    "quando não", "quando nao", "não funciona", "nao funciona",
    "trade-off", "tradeoff", "cuidado", "evite", "degradação", "degradacao",
    "fallback", "bom até", "bom ate", "funciona até", "funciona ate",
    "desaconselha", "não recomendo", "nao recomendo", "limitação", "limitacao",
)
MARCADORES_LIMITE = (
    "até", "ate", "quando", "limite", "não", "nao", "cuidado", "evite",
    "acima", "abaixo", "apenas", "somente", "se ", "menos que", "mais que",
    "depender", "desaconselha", "evitar", "precisa", "exige", "requer",
    "acima de", "abaixo de", "nunca", "sempre", "após", "apos", "depois",
)

REGRAS = {
    "R-ES-1": "seção Aplica contém ao menos 1 termo de escala/limite",
    "R-ES-2": "termo de escala em contexto de advertência (limite/contorno)",
}


def _termos(texto):
    baixo = sem_codigo(texto or "").lower()
    return [t for t in TERMOS_ESCALA if t in baixo]


def _em_contexto_de_limite(texto, termo):
    """A frase que contém o termo também carrega um marcador de limite."""
    baixo = sem_codigo(texto or "").lower()
    frases = re.split(r"(?<=[.!?])\s+|\n", baixo)
    for frase in frases:
        if termo in frase and any(m in frase for m in MARCADORES_LIMITE):
            return frase.strip()[:160]
    return None


def validar_aplica(texto_capitulo, rotulo):
    secoes = dividir_secoes(texto_capitulo)
    aplica = secao_por_nome(secoes, "aplica") or ""
    violacoes = []

    termos = _termos(aplica)
    if not termos:
        violacoes.append({
            "regra": "R-ES-1", "enunciado": REGRAS["R-ES-1"],
            "detalhe": "seção Aplica sem nenhum termo de escala/limite"})
        return violacoes

    com_contexto = [t for t in termos if _em_contexto_de_limite(aplica, t)]
    if not com_contexto:
        violacoes.append({
            "regra": "R-ES-2", "enunciado": REGRAS["R-ES-2"],
            "detalhe": (f"termos de escala presentes ({', '.join(termos[:4])}) "
                        "mas nenhum em contexto de limite/advertência")})
    return violacoes


def main():
    ap = argparse.ArgumentParser(
        description="Gate F1 de escalabilidade: limites declarados na seção Aplica")
    ap.add_argument("slug")
    ap.add_argument("--capitulo", help="valida apenas o capitulo N")
    ap.add_argument("--md", help="valida um markdown especifico em vez dos capitulos")
    ap.add_argument("--estrito", action="store_true", help="exit 1 se houver falha")
    ap.add_argument("--json", action="store_true", help="imprime relatorio JSON completo")
    args = ap.parse_args()

    dir_livro = TO.dir_obra(args.slug, DIR_OUTPUT)
    if not dir_livro.exists():
        print(f"[ERRO] Obra nao encontrada: {dir_livro}")
        return 1

    alvos = []
    if args.md:
        p = Path(args.md)
        if not p.exists():
            print(f"[ERRO] Arquivo nao encontrado: {p}")
            return 1
        alvos.append((p, p.name))
    else:
        caps = sorted((dir_livro / "capitulos").glob("cap_*.md"),
                      key=lambda p: int(re.search(r"cap_(\d+)", p.stem).group(1)))
        if args.capitulo:
            caps = [c for c in caps
                    if re.search(r"cap_(\d+)", c.stem).group(1).lstrip("0")
                    == str(args.capitulo).lstrip("0")]
        if not caps:
            print(f"[ERRO] Nenhum capitulo encontrado em {dir_livro / 'capitulos'}")
            return 1
        alvos = [(c, c.stem) for c in caps]

    todos = []
    for caminho, rotulo in alvos:
        texto = caminho.read_text(encoding="utf-8", errors="replace")
        violacoes = validar_aplica(texto, rotulo)
        for v in violacoes:
            v["origem"] = rotulo
        todos.extend(violacoes)

    relatorio = {
        "slug": args.slug,
        "capitulos": len(alvos),
        "total_violacoes": len(todos),
        "regras": REGRAS,
        "violacoes": todos,
    }
    dir_val = dir_livro / "validacao"
    dir_val.mkdir(exist_ok=True)
    (dir_val / "relatorio_escala.json").write_text(
        json.dumps(relatorio, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Gate de Escalabilidade - {args.slug}")
    print(f"  capitulos analisados : {len(alvos)}")
    print(f"  violacoes            : {len(todos)}")

    if todos:
        print("\n[FALHA] Violações:")
        for v in todos[:20]:
            print(f"  - {v.get('origem')}: {v['regra']} — {v['detalhe']}")
        if len(todos) > 20:
            print(f"  ... e mais {len(todos) - 20}")
    else:
        print("\n[OK] Todos os capítulos declaram limites de escala")

    print(f"\nRelatorio: {(dir_val / 'relatorio_escala.json').relative_to(DIR_PROJETO)}")

    if args.json:
        print(json.dumps(relatorio, ensure_ascii=False, indent=2))

    if args.estrito and todos:
        return 1
    return 0


if __name__ == "__main__":
    console_utf8()
    sys.exit(main())
