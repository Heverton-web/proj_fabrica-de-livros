#!/usr/bin/env python3
"""
Esqueleto macro P/M/G determinístico (arquiteto consome parametros_obra.py).

A tabela de partes/capítulos por tamanho (P/M/G/GG/XG) já vive em
`parametros_obra.TAMANHOS` — mas o SKILL.md do `arquiteto` reafirma a mesma
tabela em prosa solta, e é a LLM que "decide" a contagem lendo essa cópia
(risco real de drift entre as duas fontes). Este script gera o
`sumario_macro.json` já com N partes/capítulos vazios (números e distribuição
corretos por construção); a LLM só preenche título/objetivo/pilares de cada
capítulo, e o motivo condutor/persona da obra — que é criação editorial, não
regra fixa.

Uso:
    python scripts/gerar-esqueleto-macro.py <slug> --tamanho M
    python scripts/gerar-esqueleto-macro.py <slug>              # lê tamanho_obra do config_obra.json
    python scripts/gerar-esqueleto-macro.py <slug> --tamanho G --forcar

Grava: <dir_obra>/sumario_macro.json
"""

import argparse
import json
import sys
from pathlib import Path

import parametros_obra as PO
import tipos_obra as TO
from tipos_obra import console_utf8

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

ROMANOS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]


def distribuir_capitulos(total_capitulos, total_partes):
    """N capítulos em N partes o mais equilibrado possível (resto nas primeiras)."""
    base, resto = divmod(total_capitulos, total_partes)
    return [base + (1 if i < resto else 0) for i in range(total_partes)]


def montar_esqueleto(tamanho):
    minimos = PO.minimos_livro(tamanho)
    distribuicao = distribuir_capitulos(minimos["capitulos"], minimos["partes"])

    partes = []
    numero_capitulo = 1
    for indice, qtd in enumerate(distribuicao):
        capitulos = []
        for _ in range(qtd):
            capitulos.append({
                "capitulo": str(numero_capitulo),
                "titulo": "",
                "objetivo": "",
                "pilares_previstos": [],
            })
            numero_capitulo += 1
        partes.append({
            "parte": ROMANOS[indice] if indice < len(ROMANOS) else str(indice + 1),
            "titulo_parte": "",
            "capitulos": capitulos,
        })

    return {
        "titulo_obra": "",
        "subtitulo": "",
        "motivo_condutor": {
            "nome": "",
            "descricao": "",
            "vocabulario": [],
            "persona_leitor": "",
        },
        "partes": partes,
    }


def main():
    console_utf8()
    ap = argparse.ArgumentParser(description="Gera o esqueleto macro (partes/capítulos vazios) por tamanho P/M/G/GG/XG")
    ap.add_argument("slug")
    ap.add_argument("--tamanho", help="P|M|G|GG|XG (default: tamanho_obra do config_obra.json, ou M)")
    ap.add_argument("--forcar", action="store_true", help="sobrescreve sumario_macro.json existente")
    args = ap.parse_args()

    tamanho = args.tamanho
    if not tamanho:
        config = PO.carregar_config(args.slug)
        tamanho = config.get("tamanho_obra") or PO.TAMANHO_PADRAO

    dir_obra = TO.dir_obra(args.slug, DIR_OUTPUT)
    destino = dir_obra / "sumario_macro.json"
    if destino.exists() and not args.forcar:
        print(f"[gerar-esqueleto-macro] já existe: {destino} (use --forcar para sobrescrever)")
        return 1

    esqueleto = montar_esqueleto(tamanho)
    dir_obra.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(esqueleto, ensure_ascii=False, indent=2), encoding="utf-8")

    total_cap = sum(len(p["capitulos"]) for p in esqueleto["partes"])
    print(f"[gerar-esqueleto-macro] tamanho={tamanho.upper()} -> {len(esqueleto['partes'])} partes, "
          f"{total_cap} capítulos vazios")
    print(f"[gerar-esqueleto-macro] gravado {destino}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
