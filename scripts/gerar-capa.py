#!/usr/bin/env python3
"""
Gerador unico de capa (livro e e-book), padrao Editora Agentica.

Substitui scripts/gerar-capa-ebook-padrao.py (Playwright/HTML antigo, so
ebook), scripts/gerar-capa-ebooks.py (Pillow, dimensao 1:1,6 divergente),
scripts/testar_capa_marketing.py e scripts/gerar_capas_demais_ebooks.py
(CONFIGS_SERIE hardcoded — agora em output/_series.json via series_capa.py).

Ver docs/superpowers/specs/2026-08-06-capas-padronizadas-design.md.

Uso (1 obra, resolvendo tudo a partir dos arquivos da propria obra):
    python scripts/gerar-capa.py livros/meu-livro
    python scripts/gerar-capa.py ebooks/meu-livro--eb-01-titulo

Uso (titulo/subtitulo/cor explicitos, sem depender de arquivos da obra):
    python scripts/gerar-capa.py livros/meu-livro --tipo livro \
        --titulo "MEU TITULO" --subtitulo "Meu subtitulo" --cor "#58a6ff"

Uso (migracao em lote — regenera todas as obras existentes):
    python scripts/gerar-capa.py --todos
"""
import argparse
import importlib
import json
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("[ERRO] playwright nao instalado")
    sys.exit(1)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from series_capa import resolver_cor, resolver_serie_key  # noqa: E402

_validar_mod = importlib.import_module("validar-capa-texto")
validar_capa = _validar_mod.validar_capa

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

AUTOR_PADRAO = "Heverton Eduardo Peres"
QUALIFICACAO_PADRAO = "Especialista em Marketing e Desenvolvimento de Soluções"

DIMENSOES = {"livro": (1600, 2263), "ebook": (1200, 1600)}


def _destacar_ultima_palavra(titulo, cor_acento):
    palavras = titulo.strip().split()
    if len(palavras) < 2:
        return titulo
    resto, ultima = " ".join(palavras[:-1]), palavras[-1]
    return f'{resto} <span class="highlight">{ultima}</span>'


def _gerar_html(titulo, subtitulo, cor_acento, autor, qualificacao, badge_texto,
                 ilustracao_relpath, largura, altura):
    titulo_html = _destacar_ultima_palavra(titulo, cor_acento)
    bloco_ilustracao = (
        f'<div class="ilustracao"><img src="{ilustracao_relpath}" alt=""></div>'
        if ilustracao_relpath else ""
    )
    bloco_badge = f'<div class="badge">{badge_texto}</div>' if badge_texto else ""
    bloco_subtitulo = f'<div class="subtitle">{subtitulo}</div>' if subtitulo else ""

    return f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: {largura}px; height: {altura}px;
    background: #0d1117;
    font-family: 'Inter', Arial, sans-serif;
    position: relative;
    overflow: hidden;
  }}
  .top-bar {{ position: absolute; top: 0; left: 0; width: 100%; height: 8px; background: {cor_acento}; }}
  .bottom-bar {{ position: absolute; bottom: 0; left: 0; width: 100%; height: 6px; background: {cor_acento}; }}
  .content {{
    position: absolute; top: 50px; bottom: 50px; left: 80px; right: 80px;
    display: flex; flex-direction: column;
  }}
  .header {{ display: flex; align-items: center; gap: 12px; margin-bottom: 24px; flex-shrink: 0; }}
  .editora-icon {{
    width: 44px; height: 44px; border: 2px solid {cor_acento}; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; color: {cor_acento}; font-weight: 700; font-family: monospace;
  }}
  .editora-text {{ font-size: 14px; font-weight: 600; color: #8b949e; letter-spacing: 3px; text-transform: uppercase; }}
  .ilustracao {{ flex: 1; display: flex; align-items: center; justify-content: center; min-height: 0; margin-bottom: 24px; }}
  .ilustracao img {{ max-width: 100%; max-height: 100%; object-fit: contain; }}
  .title {{ font-size: 72px; font-weight: 900; color: #e6edf3; line-height: 1.05; letter-spacing: -1px; margin-bottom: 16px; flex-shrink: 0; }}
  .title .highlight {{ color: {cor_acento}; }}
  .subtitle {{ font-size: 22px; font-weight: 300; color: #8b949e; margin-bottom: 20px; flex-shrink: 0; }}
  .badge {{ display: inline-block; background: {cor_acento}; color: #0d1117; padding: 8px 20px; border-radius: 18px; font-weight: 700; font-size: 15px; margin-bottom: 20px; align-self: flex-start; flex-shrink: 0; }}
  .divider {{ width: 80px; height: 4px; background: {cor_acento}; margin-bottom: 16px; flex-shrink: 0; }}
  .author-name {{ font-size: 20px; font-weight: 600; color: #e6edf3; margin-bottom: 4px; flex-shrink: 0; }}
  .author-role {{ font-size: 12px; color: {cor_acento}; letter-spacing: 2px; text-transform: uppercase; font-weight: 600; flex-shrink: 0; }}
</style>
</head>
<body>
  <div class="top-bar"></div>
  <div class="bottom-bar"></div>
  <div class="content">
    <div class="header">
      <div class="editora-icon">&gt;_</div>
      <div class="editora-text">Editora Agêntica</div>
    </div>
    {bloco_ilustracao}
    <div class="title">{titulo_html}</div>
    {bloco_subtitulo}
    {bloco_badge}
    <div class="divider"></div>
    <div class="author-name">{autor}</div>
    <div class="author-role">{qualificacao}</div>
  </div>
</body>
</html>'''


def gerar_capa(titulo, subtitulo, dir_saida, tipo="livro", cor_acento="#58a6ff",
               autor=AUTOR_PADRAO, qualificacao=QUALIFICACAO_PADRAO,
               badge_texto=None, ilustracao_relpath=None):
    dir_saida = Path(dir_saida)
    largura, altura = DIMENSOES[tipo]

    resultado = validar_capa(titulo, subtitulo, tipo)
    for campo in ("titulo", "subtitulo"):
        r = resultado[campo]
        if not r["ok"]:
            print(f"[AVISO] {campo} viola a regra de quebra de linha: {r['motivo']}")

    if ilustracao_relpath and not (dir_saida / ilustracao_relpath).exists():
        ilustracao_relpath = None

    html = _gerar_html(titulo, subtitulo, cor_acento, autor, qualificacao,
                        badge_texto, ilustracao_relpath, largura, altura)

    dir_saida.mkdir(parents=True, exist_ok=True)
    (dir_saida / "imagens").mkdir(exist_ok=True)
    html_file = dir_saida / "capa.html"
    html_file.write_text(html, encoding="utf-8")

    png_file = dir_saida / "imagens" / "capa.png"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": largura, "height": altura})
        page.goto(f"file:///{html_file.resolve().as_posix()}")
        page.wait_for_timeout(1500)
        page.screenshot(path=str(png_file))
        browser.close()

    print(f"[OK] {png_file.relative_to(DIR_PROJETO)} ({png_file.stat().st_size // 1024} KB)")
    return png_file


def _ler_json(caminho):
    if caminho.exists():
        try:
            return json.loads(caminho.read_text(encoding="utf-8"))
        except ValueError:
            return {}
    return {}


def gerar_capa_da_obra(slug, tipo_forcado=None):
    """Resolve titulo/subtitulo/cor/ilustracao a partir dos arquivos da propria obra."""
    dir_obra = DIR_OUTPUT / slug
    config_obra = _ler_json(dir_obra / "config_obra.json")
    sumario = _ler_json(dir_obra / "sumario_macro.json")
    meta_ebook = _ler_json(dir_obra / "ebook_metadados.json")

    tipo = tipo_forcado or ("ebook" if slug.startswith("ebooks/") else "livro")
    titulo = (meta_ebook.get("titulo") or sumario.get("titulo_obra") or Path(slug).name).upper()
    subtitulo = meta_ebook.get("subtitulo") or sumario.get("subtitulo") or ""

    serie_key = resolver_serie_key(config_obra, slug)
    cor_acento = resolver_cor(serie_key, slug)

    ilustracao_relpath = "imagens/capa_ilustracao.png"

    return gerar_capa(
        titulo=titulo,
        subtitulo=subtitulo,
        dir_saida=dir_obra,
        tipo=tipo,
        cor_acento=cor_acento,
        ilustracao_relpath=ilustracao_relpath,
    )


def main():
    ap = argparse.ArgumentParser(description="Gerador unico de capa (livro/ebook)")
    ap.add_argument("slug", nargs="?", help="ex.: livros/meu-livro ou ebooks/meu-livro--eb-01-titulo")
    ap.add_argument("--tipo", choices=["livro", "ebook"], default=None)
    ap.add_argument("--titulo")
    ap.add_argument("--subtitulo", default="")
    ap.add_argument("--cor")
    ap.add_argument("--badge")
    ap.add_argument("--todos", action="store_true",
                     help="regenera todas as obras em output/livros e output/ebooks")
    args = ap.parse_args()

    if args.todos:
        alvos = []
        if (DIR_OUTPUT / "livros").exists():
            alvos += [f"livros/{d.name}" for d in (DIR_OUTPUT / "livros").iterdir() if d.is_dir()]
        if (DIR_OUTPUT / "ebooks").exists():
            alvos += [f"ebooks/{d.name}" for d in (DIR_OUTPUT / "ebooks").iterdir() if d.is_dir()]
        falhas = []
        for slug in sorted(alvos):
            try:
                gerar_capa_da_obra(slug)
            except Exception as exc:  # noqa: BLE001 — nao travar o lote por 1 obra ruim
                print(f"[ERRO] {slug}: {exc}")
                falhas.append(slug)
        if falhas:
            print(f"\n[AVISO] {len(falhas)} obra(s) falharam: {falhas}")
        return 0

    if not args.slug:
        print("[ERRO] informe <slug> ou use --todos")
        return 1

    if args.titulo:
        config_obra = _ler_json(DIR_OUTPUT / args.slug / "config_obra.json")
        cor = args.cor or resolver_cor(resolver_serie_key(config_obra, args.slug), args.slug)
        gerar_capa(args.titulo, args.subtitulo, DIR_OUTPUT / args.slug,
                   tipo=args.tipo or "livro", cor_acento=cor, badge_texto=args.badge)
    else:
        gerar_capa_da_obra(args.slug, tipo_forcado=args.tipo)
    return 0


if __name__ == "__main__":
    sys.exit(main())
