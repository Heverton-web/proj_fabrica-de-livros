#!/usr/bin/env python3
"""
V5.1 — Compilador do DECK: HTML autocontido + PDF 16:9, da MESMA fonte.

Substitui o Typst no deck. Motivo: o PPTX do writer do Pandoc sai correto mas
sem design (o reference doc do Office nao carrega identidade), e o Typst nao
alcanca o acabamento visual que uma apresentacao pede. CSS alcanca.

Aqui — ao contrario do lead magnet — o **.html E entregavel**: abre no navegador,
apresenta em tela cheia, navega pelo teclado e funciona offline. O PDF sai do
MESMO HTML pelo Chromium, entao apresentacao e distribuicao ficam identicas.

    deck.md --(pandoc --section-divs)--> secoes --> HTML autocontido --> PDF 16:9

Uso:
    python scripts/gerar-deck-html.py decks/<codigo>/dck-1-<nome>
    python scripts/gerar-deck-html.py --todos
    python scripts/gerar-deck-html.py <slug> --sem-pdf
"""

import argparse
import html as _html
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
TIMEOUT = 180
LARGURA, ALTURA = 1280, 720

RE_SECAO = re.compile(
    r'<section[^>]*class="[^"]*\blevel1\b[^"]*"[^>]*>(.*?)</section>',
    re.DOTALL | re.IGNORECASE)
RE_H1 = re.compile(r"<h1[^>]*>(.*?)</h1>", re.DOTALL | re.IGNORECASE)


def _ler_json(caminho, padrao=None):
    if caminho.exists():
        try:
            return json.loads(caminho.read_text(encoding="utf-8"))
        except ValueError:
            return padrao if padrao is not None else {}
    return padrao if padrao is not None else {}


def md_para_secoes(md_path, dir_deck):
    """Converte deck.md em fragmentos HTML, um por `# Titulo`.

    `--section-divs` faz o Pandoc envolver cada nivel 1 em <section class="level1">
    — uma fronteira previsivel, bem mais robusta que cortar o Markdown na mao."""
    comando = [
        PANDOC, str(md_path), "-t", "html5",
        "--from", "markdown-citations",
        "--section-divs", "--wrap", "preserve",
        "--resource-path", str(dir_deck),
    ]
    resultado = subprocess.run(comando, capture_output=True, text=True,
                               encoding="utf-8", timeout=TIMEOUT)
    if resultado.returncode != 0:
        raise RuntimeError(f"pandoc falhou: {(resultado.stderr or '')[-300:]}")

    secoes = []
    for corpo in RE_SECAO.findall(resultado.stdout):
        m = RE_H1.search(corpo)
        titulo = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else ""
        conteudo = RE_H1.sub("", corpo, count=1).strip()
        secoes.append({"titulo": titulo, "html": conteudo})
    return secoes


def montar_slides(secoes, meta):
    """Monta os <section class="slide">, com a capa em markup proprio."""
    total = len(secoes) + 1        # +1 = capa
    partes = [_slide_capa(meta, total)]
    for i, secao in enumerate(secoes, start=2):
        partes.append(_slide(secao, i, total, meta))
    return "\n".join(partes)


def _rodape(indice, total, meta):
    return (
        '<div class="rodape-slide">'
        f'<span>{_html.escape(meta["titulo"])}</span>'
        f'<span>{indice} / {total}</span>'
        "</div>"
    )


def _slide_capa(meta, total):
    L = ['<section class="slide capa ativo">',
         '<div class="marca">Editora Agêntica</div>',
         f'<h1>{_html.escape(meta["titulo"])}</h1>']
    if meta.get("subtitulo"):
        L.append(f'<blockquote>{_html.escape(meta["subtitulo"])}</blockquote>')
    if meta.get("badge_nivel"):
        L.append(f'<span class="badge">{_html.escape(meta["badge_nivel"])}</span>')
    L.append('<div class="rodape">'
             f'<div class="autor">{_html.escape(meta["autor"])}</div>')
    if meta.get("livro_mae"):
        L.append(f'<div class="origem">Baseado em {_html.escape(meta["livro_mae"])}</div>')
    L += ["</div>", _rodape(1, total, meta), "</section>"]
    return "\n".join(L)


def _slide(secao, indice, total, meta):
    return "\n".join([
        '<section class="slide">',
        f'<h1>{_html.escape(secao["titulo"])}</h1>',
        f'<div class="corpo">{secao["html"]}</div>',
        _rodape(indice, total, meta),
        "</section>",
    ])


def envolver_no_template(dir_deck, corpo_html, meta):
    """Aplica o template do tipo. Passa o HTML montado como bloco bruto para o
    Pandoc — assim a linguagem de template ($if$, $for$) continua sendo do Pandoc,
    sem reimplementa-la aqui."""
    template = TO.template_html_de("deck")
    if template is None or not template.exists():
        raise FileNotFoundError(f"template HTML ausente: {template}")

    entrada = dir_deck / "deck-corpo.md"
    entrada.write_text(corpo_html, encoding="utf-8")
    saida = dir_deck / f"{TO.nome_arquivo(str(dir_deck))}.html"
    # Remover a saida ANTES: se o pandoc falhar, o arquivo da rodada anterior
    # nao pode ficar para tras se passando por resultado novo.
    saida.unlink(missing_ok=True)

    comando = [
        PANDOC, str(entrada), "-o", str(saida),
        "--from", "html", "--to", "html5",
        "--standalone", "--template", str(template),
        "--wrap", "preserve",
        "--resource-path", str(dir_deck),
        "-V", f"title={meta['titulo']}",
        "-V", f"author={meta['autor']}",
    ]
    for chave in ("cor_acento", "badge_nivel", "livro_mae"):
        if meta.get(chave):
            comando += ["-V", f"{chave}={meta[chave]}"]

    resultado = subprocess.run(comando, capture_output=True, text=True,
                               encoding="utf-8", timeout=TIMEOUT)
    entrada.unlink(missing_ok=True)
    # Conferir o RETURNCODE, nao so a existencia do arquivo: um erro de compilacao
    # de template (ex.: cifrao-chave num comentario do JS) faz o pandoc sair com
    # erro sem escrever nada — e a versao antiga no disco seria reportada como
    # sucesso, escondendo a falha por rodadas inteiras.
    if resultado.returncode != 0:
        raise RuntimeError(f"pandoc falhou ({resultado.returncode}): "
                           f"{(resultado.stderr or resultado.stdout or '').strip()[-400:]}")
    if not saida.exists() or saida.stat().st_size == 0:
        raise RuntimeError("pandoc terminou sem erro mas nao gerou o HTML")
    return saida


def html_para_pdf(html_path, pdf_path):
    """Um slide por pagina, 1280x720. `emulate_media('print')` liga a regra que
    revela TODOS os slides (na tela so o ativo aparece)."""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page(viewport={"width": LARGURA, "height": ALTURA})
        pagina.goto(f"file:///{html_path.resolve().as_posix()}", wait_until="networkidle")
        pagina.emulate_media(media="print")
        pagina.pdf(path=str(pdf_path), width=f"{LARGURA}px", height=f"{ALTURA}px",
                   print_background=True,
                   margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        navegador.close()
    return pdf_path


def compilar(slug, com_pdf=True):
    dir_deck = TO.dir_obra(slug, DIR_OUTPUT)
    md = dir_deck / "deck.md"
    if not md.exists():
        print(f"[ERRO] deck.md nao encontrado em {dir_deck}")
        return None

    config = _ler_json(dir_deck / "config_obra.json")
    sumario = _ler_json(dir_deck / "sumario_macro.json")

    dados = {}
    try:
        import metadados_livro
        coletor = getattr(metadados_livro, TO.campo("deck", "coletor_metadados") or "", None)
        if coletor:
            dados = coletor(slug, dir_livro=dir_deck)
    except Exception as exc:  # noqa: BLE001
        print(f"  [AVISO] metadados indisponiveis ({exc})")

    meta = {
        "titulo": sumario.get("titulo_obra") or config.get("tema") or Path(slug).name,
        "subtitulo": sumario.get("subtitulo", ""),
        "autor": dados.get("autor") or "Heverton Eduardo Peres",
        "cor_acento": dados.get("cor_acento") or "#2ecc9a",
        "badge_nivel": dados.get("badge_nivel", ""),
        "livro_mae": dados.get("livro_mae") or config.get("obra_mae", ""),
    }

    try:
        secoes = md_para_secoes(md, dir_deck)
        if not secoes:
            print("[ERRO] deck.md sem nenhum `# Titulo` — nada a montar")
            return None
        html_path = envolver_no_template(dir_deck, montar_slides(secoes, meta), meta)
    except (FileNotFoundError, RuntimeError, subprocess.SubprocessError) as exc:
        print(f"[ERRO] {exc}")
        return None

    pdf_path = None
    if com_pdf:
        pdf_path = dir_deck / f"{TO.nome_arquivo(slug)}.pdf"
        try:
            html_para_pdf(html_path, pdf_path)
        except Exception as exc:  # noqa: BLE001
            print(f"[ERRO] Chromium nao gerou o PDF: {exc}")
            return None

    return {
        "slug": slug,
        "html": str(html_path.relative_to(DIR_OUTPUT)),
        "pdf": str(pdf_path.relative_to(DIR_OUTPUT)) if pdf_path else None,
        "slides": len(secoes) + 1,
        "kb_html": html_path.stat().st_size // 1024,
        "kb_pdf": pdf_path.stat().st_size // 1024 if pdf_path else 0,
    }


def main():
    TO.console_utf8()
    ap = argparse.ArgumentParser(description="Compila o deck em HTML autocontido + PDF 16:9")
    ap.add_argument("slug", nargs="?", help="ex.: decks/ai-driven/dck-1-ai-driven")
    ap.add_argument("--todos", action="store_true")
    ap.add_argument("--sem-pdf", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if shutil.which(PANDOC) is None:
        print("[ERRO] pandoc nao encontrado no PATH")
        return 1

    if args.todos:
        alvos = [s for s in TO.listar_materiais("deck", DIR_OUTPUT)
                 if (TO.dir_obra(s, DIR_OUTPUT) / "deck.md").exists()]
    elif args.slug:
        alvos = [args.slug]
    else:
        print("[ERRO] informe <slug> ou use --todos")
        return 1

    metas = []
    for alvo in alvos:
        meta = compilar(alvo, com_pdf=not args.sem_pdf)
        if meta:
            metas.append(meta)
            if not args.json:
                print(f"[OK] {meta['slides']} slides — {meta['html']} "
                      f"({meta['kb_html']} KB)"
                      + (f" + {meta['pdf']} ({meta['kb_pdf']} KB)" if meta["pdf"] else ""))

    if args.json:
        print(json.dumps(metas, ensure_ascii=False, indent=2))
    return 0 if len(metas) == len(alvos) else 1


if __name__ == "__main__":
    sys.exit(main())
