#!/usr/bin/env python3
"""
V5 — Gerador de SLIDE DECK (custo ~0 token).

Monta a apresentacao a partir de tres fontes ja existentes, sem LLM:
    sumario_macro.json      -> titulo, estagios (divisores), objetivos
    §3 Ilustra do capitulo  -> diagramas Mermaid ja renderizados em imagens/diagramas/
    cards do playbook       -> bullets acionaveis (⑥ Feito quando / ③ Entregas)

Um slide por capitulo + um divisor por Parte + capa + objetivo + mapa + CTA.

Saida: output/decks/<slug-mae>--deck/deck.md (+ imagens/ com os diagramas copiados)

Uso:
    python scripts/gerar-deck.py livros/<slug>
    python scripts/gerar-deck.py livros/<slug> --max-bullets 4 --cta-url https://...
"""

import argparse
import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path

import tipos_obra as TO
from secoes_eita import dividir_secoes, primeiro_paragrafo, secao_por_nome

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

MAX_BULLETS = 4
MAX_CHARS_BULLET = 110
RE_IMAGEM = re.compile(r"!\[[^\]]*\]\(([^)]+\.(?:png|svg|jpg))\)")


def _ler_json(caminho, padrao=None):
    if caminho.exists():
        try:
            return json.loads(caminho.read_text(encoding="utf-8"))
        except ValueError:
            return padrao if padrao is not None else {}
    return padrao if padrao is not None else {}


def _importar_extrator():
    """Reusa a instancia ja carregada (ver nota em gerar-lead-magnet.py)."""
    if "extrair_passos_praticos" in sys.modules:
        return sys.modules["extrair_passos_praticos"]
    caminho = DIR_PROJETO / "scripts" / "extrair-passos-praticos.py"
    spec = importlib.util.spec_from_file_location("extrair_passos_praticos", caminho)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["extrair_passos_praticos"] = mod
    spec.loader.exec_module(mod)
    return mod


def _encurtar(texto, limite=MAX_CHARS_BULLET):
    t = re.sub(r"\s+", " ", (texto or "").strip()).rstrip(".")
    t = re.sub(r"\[\d{1,3}\]", "", t).strip()
    if len(t) <= limite:
        return t
    return t[:limite].rsplit(" ", 1)[0] + "…"


def _bullets(cap_meta, card, max_bullets):
    """Prioridade: pilares do sumario -> 'Feito quando' do card -> entregas."""
    fonte = [p for p in (cap_meta.get("pilares_previstos") or []) if p]
    if len(fonte) < 2 and card:
        fonte = card.get("feito_quando", []) or [f"Entrega: {e}" for e in card.get("entregas", [])]
    return [_encurtar(b) for b in fonte[:max_bullets] if b]


def gerar(slug, max_bullets=MAX_BULLETS, cta_url=None, cta_texto=None):
    dir_mae = DIR_OUTPUT / slug
    sumario = _ler_json(dir_mae / "sumario_macro.json")
    config = _ler_json(dir_mae / "config_obra.json")
    if not sumario.get("partes"):
        print(f"[ERRO] sumario_macro.json ausente ou sem partes: {dir_mae}")
        return None

    extrator = _importar_extrator()
    ctx = extrator.contexto_da_obra(slug)

    # Cards do playbook, se existirem (nao obrigatorios)
    slug_pbk = TO.slug_curto("playbook", ctx["slug_mae_simples"],
                             nome=ctx.get("titulo_obra", ""))
    dir_passos = DIR_OUTPUT / slug_pbk / "passos"
    cards = {c.get("numero"): c for c in
             (_ler_json(p) for p in sorted(dir_passos.glob("passo_*.json")))} \
        if dir_passos.exists() else {}

    titulo = sumario.get("titulo_obra", ctx["slug_mae_simples"])
    slug_deck = TO.slug_curto("deck", ctx["slug_mae_simples"], nome=titulo)
    dir_deck = DIR_OUTPUT / slug_deck
    (dir_deck / "imagens" / "diagramas").mkdir(parents=True, exist_ok=True)
    (dir_deck / "revisao").mkdir(parents=True, exist_ok=True)

    L = ["---", f'title: "{titulo}"',
         f'subtitle: "Apresentação · {ctx.get("persona", "")}"'.replace(' · "', '"'),
         'author: "Heverton Eduardo Peres"', "lang: pt-BR", "---", ""]

    total_slides, diagramas_copiados = 0, 0

    # Slide 2 — Objetivo
    L += ["# Objetivo", "",
          ctx.get("introducao") or primeiro_paragrafo(sumario.get("introducao", "")) or
          f"Percorrer {titulo} do início ao fim.", ""]
    total_slides += 1

    # Slide 3 — Mapa
    if ctx.get("estagios"):
        L += ["# O caminho", ""]
        for e in ctx["estagios"]:
            caps = ", ".join(str(int(c)) for c in e["capitulos"]) or "—"
            L.append(f"- **{e['nome']}** — capítulos {caps}")
        L.append("")
        total_slides += 1

    # Slides por Parte / capitulo
    for i, parte in enumerate(sumario.get("partes", [])):
        estagio = ctx["estagios"][i] if i < len(ctx["estagios"]) else {}
        nome_parte = parte.get("titulo_parte") or estagio.get("nome") or f"Parte {i + 1}"
        L += [f"# {nome_parte}", "",
              f"> Estágio {i + 1} de {len(sumario['partes'])}", ""]
        total_slides += 1

        for cap in parte.get("capitulos", []):
            num = str(cap.get("capitulo")).zfill(2)
            card = cards.get(num)
            L += [f"# {cap.get('titulo', 'Capítulo ' + num)}", ""]
            if cap.get("objetivo"):
                L += [f"*{_encurtar(cap['objetivo'], 160)}*", ""]
            for b in _bullets(cap, card, max_bullets):
                L.append(f"- {b}")
            L.append("")

            # Diagrama da §3 Ilustra, se ja renderizado. A fabrica grava tanto
            # cap_1.md quanto cap_01.md — aceite os dois.
            cap_path = next((p for p in (dir_mae / "capitulos" / f"cap_{num}.md",
                                         dir_mae / "capitulos" / f"cap_{int(num)}.md")
                             if p.exists()), None)
            if cap_path is not None:
                secoes = dividir_secoes(cap_path.read_text(encoding="utf-8", errors="replace"))
                ilustra = secao_por_nome(secoes, "ilustra")
                m = RE_IMAGEM.search(ilustra)
                if m:
                    origem = (dir_mae / "capitulos" / m.group(1)).resolve()
                    if origem.exists():
                        destino = dir_deck / "imagens" / "diagramas" / origem.name
                        shutil.copy2(origem, destino)
                        diagramas_copiados += 1
                        L += [f"![](imagens/diagramas/{origem.name})", ""]
            if card and card.get("gate"):
                L += [f"`{card['gate']}`", ""]
            total_slides += 1

    # Slide final — CTA
    cfg_existente = _ler_json(dir_deck / "config_obra.json")
    url = (cta_url or cfg_existente.get("cta_url") or "").strip()
    texto_cta = (cta_texto or cfg_existente.get("cta_texto") or "Leia a obra completa").strip()
    if url:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}utm_source=deck&utm_medium=slides&utm_campaign={ctx['slug_mae_simples']}"
    L += ["# Próximo passo", "", f"**{titulo}**", ""]
    L.append(f"{texto_cta} — {url}" if url else texto_cta)
    L.append("")
    total_slides += 1

    (dir_deck / "deck.md").write_text("\n".join(L), encoding="utf-8")

    cfg = TO.defaults_config("deck", slug_mae_simples=ctx["slug_mae_simples"], extra={
        "tema": titulo,
        "senioridade_obra": config.get("senioridade_obra", "intermediario"),
        "cta_url": cta_url or cfg_existente.get("cta_url", ""),
        "cta_texto": texto_cta,
    })
    if ctx.get("serie"):
        cfg["serie"] = ctx["serie"]
    (dir_deck / "config_obra.json").write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    (dir_deck / "sumario_macro.json").write_text(json.dumps({
        "titulo_obra": titulo, "tipo_obra": "deck",
        "slug_livro_mae": ctx["slug_mae_simples"],
        "motivo_condutor": ctx.get("motivo_condutor") or {},
        "total_slides": total_slides,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    meta = {"slug": slug_deck, "total_slides": total_slides,
            "diagramas": diagramas_copiados, "cta_configurado": bool(url)}
    (dir_deck / "revisao" / "relatorio_deck.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return meta


def main():
    TO.console_utf8()
    ap = argparse.ArgumentParser(description="Gera slide deck a partir do sumario + diagramas + cards")
    ap.add_argument("slug", help="ex.: livros/meu-livro")
    ap.add_argument("--max-bullets", type=int, default=MAX_BULLETS)
    ap.add_argument("--cta-url", default=None)
    ap.add_argument("--cta-texto", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    meta = gerar(args.slug, max_bullets=args.max_bullets,
                 cta_url=args.cta_url, cta_texto=args.cta_texto)
    if meta is None:
        return 1
    if args.json:
        print(json.dumps(meta, ensure_ascii=False, indent=2))
    else:
        print(f"[OK] {meta['total_slides']} slide(s), {meta['diagramas']} diagrama(s) — {meta['slug']}")
        if not meta["cta_configurado"]:
            print("[AVISO] sem CTA (R-DK-3 vai reprovar). Rode de novo com --cta-url <url>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
