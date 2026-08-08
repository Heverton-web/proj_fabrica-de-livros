#!/usr/bin/env python3
"""
V5 — Compilador PDF do LEAD MAGNET (HTML+CSS -> Chromium via Playwright).

Peca de marketing pede controle fino de layout (gradiente, sobreposicao,
tipografia de campanha) — CSS entrega isso melhor que Typst. O HTML e camada
INTERMEDIARIA, equivalente ao `.typ` dos demais tipos: **o entregavel e o PDF**.

Sem Paged.js: o Chromium ja implementa `@page`, `break-*` e orphans/widows, e o
header/footer vem de `page.pdf(footerTemplate=...)`. Isso evita vendorizar ~200KB
de JS de terceiros e uma dependencia de rede na compilacao.

O CTA (R-LM-1) e injetado no rodape de TODAS as paginas via footerTemplate — nao
depende do autor lembrar de repeti-lo.

Uso:
    python scripts/gerar-lead-magnet-pdf.py lead-magnets/<slug>
    python scripts/gerar-lead-magnet-pdf.py --todos
    python scripts/gerar-lead-magnet-pdf.py <slug> --manter-html   # depuracao
"""

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tipos_obra as TO  # noqa: E402

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

PANDOC = "pandoc"
TIMEOUT = 120

MARGENS = {"top": "18mm", "bottom": "22mm", "left": "20mm", "right": "20mm"}
RE_UTM = re.compile(r"utm_source=lead-magnet")


def _ler_json(caminho, padrao=None):
    if caminho.exists():
        try:
            return json.loads(caminho.read_text(encoding="utf-8"))
        except ValueError:
            return padrao if padrao is not None else {}
    return padrao if padrao is not None else {}


def _url_com_utm(config, sumario):
    """Mesma UTM que gerar-lead-magnet.py escreve no bloco final do material."""
    url = (config.get("cta_url") or "").strip()
    if not url:
        return ""
    campanha = config.get("obra_mae") or config.get("livro_mae") \
        or sumario.get("slug_livro_mae", "")
    formato = config.get("formato_lm") or sumario.get("formato_lm", "")
    sep = "&" if "?" in url else "?"
    return (f"{url}{sep}utm_source=lead-magnet&utm_medium=pdf"
            f"&utm_campaign={campanha}&utm_content={formato}")


def montar_footer(cta_texto, cta_url, cor):
    """Rodape do Chromium. Estilos TEM de ser inline: o footerTemplate roda em um
    documento isolado, sem acesso ao CSS da pagina."""
    texto = html.escape(cta_texto or "")
    url = html.escape(cta_url or "")
    esquerda = f"{texto} — {url}" if url else texto
    return (
        '<div style="width:100%;font-family:Inter,Arial,sans-serif;font-size:7pt;'
        f'color:#616b78;padding:0 20mm;border-top:0.2mm solid {html.escape(cor)};'
        'padding-top:2mm;display:flex;justify-content:space-between;">'
        f'<span>{esquerda}</span>'
        '<span class="pageNumber"></span></div>'
    )


def md_para_html(dir_lm, md, variaveis):
    """Pandoc: lead_magnet.md -> _lead_magnet.html usando o template do tipo."""
    template = TO.template_html_de("lead-magnet")
    if template is None or not template.exists():
        raise FileNotFoundError(f"template HTML ausente: {template}")

    saida = dir_lm / "_lead_magnet.html"
    saida.unlink(missing_ok=True)   # nunca reaproveitar a rodada anterior
    comando = [
        PANDOC, str(md), "-o", str(saida),
        "--from", "markdown-citations",
        "--to", "html5",
        "--standalone",
        "--template", str(template),
        "--wrap", "preserve",
        "--resource-path", str(dir_lm),
    ]
    for chave, valor in variaveis.items():
        if valor:
            comando += ["-V", f"{chave}={valor}"]

    resultado = subprocess.run(comando, capture_output=True, text=True, timeout=TIMEOUT)
    if resultado.returncode != 0:
        raise RuntimeError(f"pandoc falhou ({resultado.returncode}): "
                           f"{(resultado.stderr or resultado.stdout or '').strip()[-400:]}")
    if not saida.exists() or saida.stat().st_size == 0:
        raise RuntimeError("pandoc terminou sem erro mas nao gerou o HTML")
    return saida


def html_para_pdf(html_path, pdf_path, cta_texto, cta_url, cor):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page()
        pagina.goto(f"file:///{html_path.resolve().as_posix()}",
                    wait_until="networkidle")
        pagina.emulate_media(media="print")
        pagina.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            margin=MARGENS,
            display_header_footer=True,
            header_template="<div></div>",           # sem cabecalho
            footer_template=montar_footer(cta_texto, cta_url, cor),
            prefer_css_page_size=False,
        )
        navegador.close()
    return pdf_path


def compilar(slug, manter_html=False):
    dir_lm = DIR_OUTPUT / slug
    md = dir_lm / "lead_magnet.md"
    if not md.exists():
        print(f"[ERRO] lead_magnet.md nao encontrado em {dir_lm}")
        return None

    config = _ler_json(dir_lm / "config_obra.json")
    sumario = _ler_json(dir_lm / "sumario_macro.json")

    # Metadados pelo coletor declarado no registro (mesma fonte do motor Typst)
    dados = {}
    try:
        import metadados_livro
        coletor = getattr(metadados_livro,
                          TO.campo("lead-magnet", "coletor_metadados") or "", None)
        if coletor:
            dados = coletor(slug, dir_livro=dir_lm)
    except Exception as exc:  # noqa: BLE001 — metadados sao complemento, nao bloqueio
        print(f"  [AVISO] metadados indisponiveis ({exc}); usando config/sumario")

    cor = dados.get("cor_acento") or "#2ecc9a"
    cta_url = _url_com_utm(config, sumario)
    cta_texto = (config.get("cta_texto") or "Quero a obra completa").strip()

    variaveis = {
        "cor_acento": cor,
        "promessa": dados.get("promessa") or sumario.get("subtitulo", ""),
        "badge_nivel": dados.get("badge_nivel", ""),
        "livro_mae": dados.get("livro_mae") or config.get("obra_mae", ""),
        "author": dados.get("autor") or "Heverton Eduardo Peres",
    }

    try:
        html_path = md_para_html(dir_lm, md, variaveis)
    except (FileNotFoundError, RuntimeError, subprocess.SubprocessError) as exc:
        print(f"[ERRO] {exc}")
        return None

    pdf_path = dir_lm / f"{Path(slug).name}.pdf"
    try:
        html_para_pdf(html_path, pdf_path, cta_texto, cta_url, cor)
    except Exception as exc:  # noqa: BLE001 — falha de render tem de ser reportada
        print(f"[ERRO] Chromium nao gerou o PDF: {exc}")
        return None
    finally:
        if not manter_html and html_path.exists():
            html_path.unlink()

    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        print(f"[ERRO] PDF vazio: {pdf_path}")
        return None

    return {
        "slug": slug,
        "pdf": str(pdf_path.relative_to(DIR_OUTPUT)),
        "kb": pdf_path.stat().st_size // 1024,
        "formato_lm": config.get("formato_lm", ""),
        "cta_no_rodape": bool(cta_url),
        "cor_acento": cor,
    }


def main():
    TO.console_utf8()
    ap = argparse.ArgumentParser(
        description="Compila o lead magnet em PDF (HTML+CSS -> Chromium)")
    ap.add_argument("slug", nargs="?", help="ex.: lead-magnets/obra--lm-01-checklist")
    ap.add_argument("--todos", action="store_true")
    ap.add_argument("--manter-html", action="store_true",
                    help="preserva _lead_magnet.html para depurar o layout")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if shutil.which(PANDOC) is None:
        print("[ERRO] pandoc nao encontrado no PATH")
        return 1

    if args.todos:
        alvos = TO.listar_materiais("lead-magnet")
    elif args.slug:
        alvos = [args.slug]
    else:
        print("[ERRO] informe <slug> ou use --todos")
        return 1

    metas = []
    for alvo in alvos:
        meta = compilar(alvo, manter_html=args.manter_html)
        if meta:
            metas.append(meta)
            if not args.json:
                cta = "CTA no rodape" if meta["cta_no_rodape"] else "SEM CTA"
                print(f"[OK] {meta['pdf']} ({meta['kb']} KB, "
                      f"{meta['formato_lm']}, {cta})")

    if args.json:
        print(json.dumps(metas, ensure_ascii=False, indent=2))
    elif len(metas) < len(alvos):
        print(f"\n[ERRO] {len(alvos) - len(metas)} de {len(alvos)} falharam")
    return 0 if len(metas) == len(alvos) else 1


if __name__ == "__main__":
    sys.exit(main())
