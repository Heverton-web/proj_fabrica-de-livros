#!/usr/bin/env python3
"""
V5 — Gate do LEAD MAGNET (R-LM-1 a R-LM-7).

O que separa um lead magnet de um PDF curto qualquer: CTA rastreavel, promessa no
titulo, teto de paginas e zero teoria. Este gate cobra os quatro.

Uso:
    python scripts/validar-lead-magnet.py lead-magnets/<slug>--lm-01-checklist
    python scripts/validar-lead-magnet.py lead-magnets/<slug>--lm-01-checklist --estrito
    python scripts/validar-lead-magnet.py --todos --estrito
"""

import argparse
import json
import re
import sys
from pathlib import Path

import tipos_obra as TO
from tipos_obra import FORMATOS_LM
from secoes_eita import dividir_secoes, normalizar, secao_por_nome, sem_codigo

from tipos_obra import console_utf8

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"
DIR_LM = DIR_OUTPUT / "lead-magnets"

# Calibrado contra os PDFs reais da V5 (750-1400 chars/pagina no layout A4 do
# template). O valor antigo (2500, densidade de livro) subestimava as paginas em
# 2-3x e fazia R-LM-3 aprovar material que estourava o teto.
CHARS_POR_PAGINA = 900
MAX_KB_POR_PAGINA = 250    # R-LM-8: peso de download

RE_TIPO_PAGINA = re.compile(rb"/Type\s*/Page[^s]")
LIMIAR_TEORIA = 0.15    # mais estrito que o playbook: lead magnet nao tem prosa nenhuma

# R-LM-2: a promessa tem de estar no titulo (numero, "como", ou substantivo-formato)
RE_PROMESSA = re.compile(
    r"(\b\d{1,3}\b|\bcomo\b|checklist|mapa|cheat\s*sheet|guia|passo a passo|"
    r"armadilha|template|folha)", re.IGNORECASE)

REGRAS = {
    "R-LM-1": "CTA final com URL rastreavel (UTM) para a obra-mae",
    "R-LM-2": "promessa explicita no titulo (numero, 'como' ou formato)",
    "R-LM-3": "teto de paginas do formato respeitado",
    "R-LM-4": "zero teoria — nao recicla prosa das secoes §1-§3 do livro-mae",
    "R-LM-5": "par de saidas: PDF (A4) + PNG (card social)",
    "R-LM-6": "badge de nivel + cor da colecao herdados da obra-mae",
    "R-LM-7": "quantidade minima de itens do formato atingida",
    "R-LM-8": f"peso do PDF sob {MAX_KB_POR_PAGINA} KB por pagina",
}


def paginas_reais(dir_lm):
    """Numero de paginas do PDF compilado, ou None se ainda nao ha PDF.

    Medir vale mais que estimar: a estimativa por caracteres nao enxerga a
    densidade do layout e ja aprovou material com o dobro do teto."""
    pdfs = sorted(dir_lm.glob("*.pdf"))
    if not pdfs:
        return None, None
    dados = pdfs[0].read_bytes()
    return len(RE_TIPO_PAGINA.findall(dados)) or None, pdfs[0].stat().st_size // 1024


def _ler_json(caminho, padrao=None):
    if caminho.exists():
        try:
            return json.loads(caminho.read_text(encoding="utf-8"))
        except ValueError:
            return padrao if padrao is not None else {}
    return padrao if padrao is not None else {}


def shingles(texto, n=6):
    palavras = normalizar(sem_codigo(texto)).split()
    if len(palavras) < n:
        return set()
    return {" ".join(palavras[i:i + n]) for i in range(len(palavras) - n + 1)}


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _teoria_do_livro_mae(mae_simples, limite_caps=6):
    for raiz in ("livros", "tccs"):
        dir_mae = TO.dir_obra(f"{raiz}/{mae_simples}", DIR_OUTPUT)
        if not (dir_mae / "capitulos").exists():
            continue
        trechos = []
        for cap in sorted((dir_mae / "capitulos").glob("cap_*.md"))[:limite_caps]:
            secoes = dividir_secoes(cap.read_text(encoding="utf-8", errors="replace"))
            trechos += [secao_por_nome(secoes, a) for a in ("introducao", "explica", "ilustra")]
        return "\n".join(trechos)
    return ""


def validar(slug, limiar_teoria=LIMIAR_TEORIA):
    dir_lm = TO.dir_obra(slug, DIR_OUTPUT)
    cfg = _ler_json(dir_lm / "config_obra.json")
    sumario = _ler_json(dir_lm / "sumario_macro.json")
    md_path = dir_lm / "lead_magnet.md"

    violacoes, avisos = [], []
    def falha(regra, detalhe):
        violacoes.append({"regra": regra, "enunciado": REGRAS[regra], "detalhe": detalhe})

    if not md_path.exists():
        falha("R-LM-3", f"lead_magnet.md inexistente em {dir_lm}")
        return {"slug": slug, "conforme": False, "violacoes": violacoes,
                "avisos": avisos, "regras": REGRAS}

    texto = md_path.read_text(encoding="utf-8", errors="replace")
    formato = cfg.get("formato_lm") or sumario.get("formato_lm") or ""
    spec = FORMATOS_LM.get(formato, {})
    titulo = sumario.get("titulo_obra", "")

    # R-LM-1 — CTA rastreavel
    if not (cfg.get("cta_url") or "").strip():
        falha("R-LM-1", "config_obra.json sem 'cta_url'")
    elif "utm_source=" not in texto:
        falha("R-LM-1", "CTA presente mas sem parametros UTM no corpo do material")
    if "# Próximo passo" not in texto and "# Proximo passo" not in texto:
        falha("R-LM-1", "bloco de CTA final ausente do lead_magnet.md")

    # R-LM-2 — promessa no titulo
    if not RE_PROMESSA.search(titulo):
        falha("R-LM-2", f"titulo sem promessa mensuravel: {titulo!r}")

    # R-LM-3 — teto de paginas (medido no PDF quando existe; estimado antes disso)
    corpo = re.sub(r"\A---\n.*?\n---\n", "", texto, flags=re.DOTALL)
    reais, kb = paginas_reais(dir_lm)
    estimadas = max(1, round(len(corpo) / CHARS_POR_PAGINA))
    paginas = reais or estimadas
    medido = reais is not None
    teto = spec.get("max_paginas", 12)
    if paginas > teto:
        origem = "medidas no PDF" if medido else "estimadas (PDF ainda nao compilado)"
        falha("R-LM-3", f"{paginas} paginas {origem}, teto do formato {formato} e {teto}")

    # R-LM-4 — zero teoria
    mae_simples = TO.resolver_slug_mae(cfg) or sumario.get("slug_livro_mae")
    if mae_simples:
        teoria = _teoria_do_livro_mae(mae_simples)
        if teoria:
            sim = round(jaccard(shingles(corpo), shingles(teoria)), 3)
            if sim > limiar_teoria:
                falha("R-LM-4", f"similaridade com a teoria do livro-mae = {sim} "
                                f"(limiar {limiar_teoria})")
        else:
            avisos.append("livro-mae sem capitulos legiveis — R-LM-4 nao verificado")
    else:
        avisos.append("config sem obra_mae — R-LM-4 e R-LM-6 nao verificados")

    # R-LM-5 — par de saidas
    tem_png = (dir_lm / "imagens" / "card_social.png").exists()
    if not medido:
        avisos.append("PDF ainda nao compilado — rode scripts/gerar-lead-magnet-pdf.py")
    if not tem_png:
        avisos.append("card social ainda nao gerado — rode gerar-capa.py --tipo lead-magnet --social")

    # R-LM-8 — peso: lead magnet vai por e-mail e download, nao pode ser pesado
    if medido and kb and paginas:
        kb_por_pagina = kb // paginas
        if kb_por_pagina > MAX_KB_POR_PAGINA:
            falha("R-LM-8", f"{kb} KB em {paginas} paginas ({kb_por_pagina} KB/pagina, "
                            f"teto {MAX_KB_POR_PAGINA}) — procure CSS que rasteriza "
                            f"(filter, box-shadow, opacity em texto)")

    # R-LM-6 — badge de nivel
    if not (cfg.get("senioridade_obra") or "").strip():
        falha("R-LM-6", "config_obra.json sem 'senioridade_obra' (badge obrigatorio)")

    # R-LM-7 — minimo de itens
    itens = sumario.get("itens", 0)
    minimo = spec.get("min_itens", 1)
    if itens < minimo:
        falha("R-LM-7", f"{itens} item(ns) agregado(s), minimo do formato {formato} e {minimo}")

    # Marcadores de polimento pendentes
    pendentes = len(re.findall(r"POLIMENTO-LLM|_\(a completar\)_", texto))
    if pendentes:
        avisos.append(f"{pendentes} marcador(es) de polimento pendente(s)")

    return {
        "slug": slug, "formato": formato, "titulo": titulo,
        "paginas": paginas, "paginas_medidas": medido,
        "paginas_estimadas": estimadas, "kb": kb, "itens": itens,
        "conforme": not violacoes, "violacoes": violacoes,
        "avisos": avisos, "regras": REGRAS,
    }


def _imprimir(rel):
    estado = "CONFORME" if rel["conforme"] else "NAO CONFORME"
    prefixo = "" if rel.get("paginas_medidas") else "~"
    peso = f", {rel['kb']} KB" if rel.get("kb") else ""
    print(f"[{estado}] {rel['slug']} ({rel.get('formato', '?')}) — "
          f"{prefixo}{rel.get('paginas', '?')}p, {rel.get('itens', '?')} itens{peso}")
    for v in rel["violacoes"]:
        print(f"  [{v['regra']}] {v['detalhe']}")
    for a in rel["avisos"]:
        print(f"  [AVISO] {a}")


def main():
    console_utf8()
    ap = argparse.ArgumentParser(description="Gate do lead magnet (R-LM-1 a R-LM-7)")
    ap.add_argument("slug", nargs="?", help="ex.: lead-magnets/meu-livro--lm-01-checklist")
    ap.add_argument("--todos", action="store_true", help="valida todos em output/lead-magnets/")
    ap.add_argument("--limiar-teoria", type=float, default=LIMIAR_TEORIA)
    ap.add_argument("--estrito", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.todos:
        alvos = TO.listar_materiais("lead-magnet", DIR_OUTPUT)
    elif args.slug:
        alvos = [args.slug]
    else:
        print("[ERRO] informe <slug> ou use --todos")
        return 1

    relatorios = []
    for alvo in alvos:
        rel = validar(alvo, limiar_teoria=args.limiar_teoria)
        dir_rev = TO.dir_obra(alvo, DIR_OUTPUT) / "revisao"
        dir_rev.mkdir(parents=True, exist_ok=True)
        (dir_rev / "relatorio_gate.json").write_text(
            json.dumps(rel, ensure_ascii=False, indent=2), encoding="utf-8")
        relatorios.append(rel)
        if not args.json:
            _imprimir(rel)

    if args.json:
        print(json.dumps(relatorios, ensure_ascii=False, indent=2))

    reprovados = [r for r in relatorios if not r["conforme"]]
    if not args.json:
        print(f"\n{len(relatorios) - len(reprovados)}/{len(relatorios)} conforme(s)")
    if args.estrito and reprovados:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
