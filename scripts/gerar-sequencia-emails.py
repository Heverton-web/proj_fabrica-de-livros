#!/usr/bin/env python3
"""
V5 — Gerador da SEQUENCIA DE E-MAILS (nutricao pos-lead-magnet).

Fecha o funil que o lead magnet abre: 1 e-mail por card do playbook, mais o
e-mail de entrega (abertura) e o de oferta (fechamento). O esqueleto sai
deterministico dos cards; o polimento de copy fica marcado com
`<!-- POLIMENTO-LLM -->` para a skill de redacao tratar em lote.

Saida: output/emails/<slug-mae>--eml/emails/email_NN.md + sequencia.md + plano.json

Uso:
    python scripts/gerar-sequencia-emails.py livros/<slug> --cta-url https://...
    python scripts/gerar-sequencia-emails.py playbooks/<slug>--pbk --intervalo 2
"""

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

import tipos_obra as TO

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

MAX_CHARS_ASSUNTO = 60
MAX_PALAVRAS_EMAIL = 250
INTERVALO_PADRAO = 2      # dias entre e-mails


def _ler_json(caminho, padrao=None):
    if caminho.exists():
        try:
            return json.loads(caminho.read_text(encoding="utf-8"))
        except ValueError:
            return padrao if padrao is not None else {}
    return padrao if padrao is not None else {}


def _importar(nome_arquivo, nome_modulo):
    """Reusa a instancia ja carregada (ver nota em gerar-lead-magnet.py)."""
    if nome_modulo in sys.modules:
        return sys.modules[nome_modulo]
    caminho = DIR_PROJETO / "scripts" / nome_arquivo
    spec = importlib.util.spec_from_file_location(nome_modulo, caminho)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nome_modulo] = mod
    spec.loader.exec_module(mod)
    return mod


def _assunto(texto, limite=MAX_CHARS_ASSUNTO):
    t = re.sub(r"\s+", " ", (texto or "").strip()).rstrip(".")
    if len(t) <= limite:
        return t
    return t[:limite - 1].rsplit(" ", 1)[0] + "…"


def _url_utm(base, campanha, indice):
    base = (base or "").strip()
    if not base:
        return ""
    sep = "&" if "?" in base else "?"
    return (f"{base}{sep}utm_source=email&utm_medium=sequencia"
            f"&utm_campaign={campanha}&utm_content=email-{indice:02d}")


def _email_abertura(ctx, url, indice):
    titulo = ctx.get("titulo_obra", "")
    L = [f"# E-mail {indice:02d} — Entrega do material", "",
         f"**Assunto:** {_assunto('Seu material chegou: ' + titulo)}",
         "**Momento:** imediato (dupla confirmação)", "",
         "---", "",
         f"Aqui está o material que você pediu sobre **{titulo}**.", "",
         "<!-- POLIMENTO-LLM: 2 frases lembrando a promessa do lead magnet e "
         "dizendo o que vem nos próximos e-mails. -->", ""]
    L.append(f"[Baixar o material]({url})" if url else "[Baixar o material](CTA_URL)")
    L += ["", "---", ""]
    return "\n".join(L)


def _email_card(card, ctx, url, indice, total):
    armadilha = (card.get("armadilhas") or [""])[0]
    entrega = (card.get("entregas") or [""])[0]
    base = armadilha or card.get("titulo", "")
    L = [f"# E-mail {indice:02d} — {card.get('titulo', '')}", "",
         f"**Assunto:** {_assunto(base)}",
         f"**Momento:** dia {(indice - 1) * INTERVALO_PADRAO}", "",
         "---", ""]
    if armadilha:
        L += [f"A armadilha desta etapa: **{armadilha}**", ""]
    if card.get("objetivo"):
        L += [card["objetivo"], ""]
    L += ["<!-- POLIMENTO-LLM: 1 parágrafo conectando a armadilha ao passo prático. "
          "Máx. 90 palavras, segunda pessoa. -->", ""]
    if card.get("gate"):
        L += ["O teste de uma linha que confirma que deu certo:", "",
              f"```bash\n{card['gate']}\n```", ""]
    if entrega:
        L += [f"Entrega desta etapa: `{entrega}`", ""]
    L.append(f"[Ver o passo completo]({url})" if url else "[Ver o passo completo](CTA_URL)")
    L += ["", f"*Passo {indice - 1} de {total - 2} da sequência.*", "", "---", ""]
    return "\n".join(L)


def _email_fechamento(ctx, url, indice):
    titulo = ctx.get("titulo_obra", "")
    L = [f"# E-mail {indice:02d} — Oferta", "",
         f"**Assunto:** {_assunto('A obra completa de ' + titulo)}",
         f"**Momento:** dia {(indice - 1) * INTERVALO_PADRAO}", "",
         "---", "",
         "<!-- POLIMENTO-LLM: 1 parágrafo de recapitulação do que a pessoa já "
         "executou + 1 parágrafo de oferta. Máx. 140 palavras. -->", "",
         f"**{titulo}** traz a teoria por trás de cada passo, os exemplos "
         "comentados e as referências completas.", ""]
    L.append(f"[Quero a obra completa]({url})" if url else "[Quero a obra completa](CTA_URL)")
    L += ["", "---", ""]
    return "\n".join(L)


def gerar(slug, cta_url=None, intervalo=INTERVALO_PADRAO):
    lm = _importar("gerar-lead-magnet.py", "gerar_lead_magnet")
    cards, ctx, _ = lm.resolver_fonte(slug)
    if cards is None:
        return None

    slug_eml = TO.slug_curto("emails", ctx["slug_mae_simples"],
                             nome=ctx.get("titulo_obra", ""))
    dir_eml = DIR_OUTPUT / slug_eml
    (dir_eml / "emails").mkdir(parents=True, exist_ok=True)
    (dir_eml / "revisao").mkdir(parents=True, exist_ok=True)

    cfg_existente = _ler_json(dir_eml / "config_obra.json")
    base_url = cta_url or cfg_existente.get("cta_url", "")
    campanha = ctx["slug_mae_simples"]

    total = len(cards) + 2
    blocos, plano = [], []

    corpo = _email_abertura(ctx, _url_utm(base_url, campanha, 1), 1)
    blocos.append(corpo)
    plano.append({"indice": 1, "tipo": "abertura", "dia": 0})

    for i, card in enumerate(cards, start=2):
        corpo = _email_card(card, ctx, _url_utm(base_url, campanha, i), i, total)
        blocos.append(corpo)
        plano.append({"indice": i, "tipo": "nutricao", "dia": (i - 1) * intervalo,
                      "passo_fonte": card.get("numero")})

    corpo = _email_fechamento(ctx, _url_utm(base_url, campanha, total), total)
    blocos.append(corpo)
    plano.append({"indice": total, "tipo": "fechamento", "dia": (total - 1) * intervalo})

    for bloco, meta in zip(blocos, plano):
        (dir_eml / "emails" / f"email_{meta['indice']:02d}.md").write_text(
            bloco, encoding="utf-8")

    (dir_eml / "sequencia.md").write_text(
        f"---\ntitle: \"Sequência de e-mails — {ctx.get('titulo_obra', '')}\"\n"
        f"lang: pt-BR\n---\n\n" + "\n".join(blocos), encoding="utf-8")

    cfg = TO.defaults_config("emails", slug_mae_simples=ctx["slug_mae_simples"], extra={
        "tema": f"Sequência — {ctx.get('titulo_obra', '')}",
        "senioridade_obra": ctx.get("senioridade") or "intermediario",
        "cta_url": base_url,
        "cta_texto": cfg_existente.get("cta_texto", "Quero a obra completa"),
        "intervalo_dias": intervalo,
    })
    if ctx.get("serie"):
        cfg["serie"] = ctx["serie"]
    (dir_eml / "config_obra.json").write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")

    meta = {"slug": slug_eml, "total_emails": total,
            "intervalo_dias": intervalo, "duracao_dias": (total - 1) * intervalo,
            "cta_configurado": bool(base_url), "plano": plano}
    (dir_eml / "plano.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return meta


def main():
    TO.console_utf8()
    ap = argparse.ArgumentParser(description="Gera a sequencia de e-mails a partir dos cards")
    ap.add_argument("slug", help="ex.: livros/meu-livro ou playbooks/meu-livro--pbk")
    ap.add_argument("--cta-url", default=None)
    ap.add_argument("--intervalo", type=int, default=INTERVALO_PADRAO,
                    help="dias entre e-mails (padrao 2)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    meta = gerar(args.slug, cta_url=args.cta_url, intervalo=args.intervalo)
    if meta is None:
        return 1
    if args.json:
        print(json.dumps(meta, ensure_ascii=False, indent=2))
    else:
        print(f"[OK] {meta['total_emails']} e-mail(s) em {meta['duracao_dias']} dias — {meta['slug']}")
        if not meta["cta_configurado"]:
            print("[AVISO] sem CTA (R-EM-2 vai reprovar). Rode de novo com --cta-url <url>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
