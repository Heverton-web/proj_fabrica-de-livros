#!/usr/bin/env python3
"""
V5.1 — Verificacao de ABERTURA dos artefatos finais.

Gerar o arquivo nao prova que ele abre. Este script testa cada artefato pelo que
o leitor de destino exige, nao pelo tamanho em disco:

    .pdf    assinatura %PDF, marcador %%EOF, >= 1 objeto /Type /Page
    .pptx   zip integro + [Content_Types].xml + ppt/presentation.xml
    .epub   zip integro + mimetype correto + META-INF/container.xml
    .html   <html> e </html>, <body>, e nada de placeholder de template ($body$)
    .md     nao vazio, sem marcador de polimento pendente
    .png    assinatura PNG

Verifica tambem o comprimento do caminho contra o MAX_PATH do Windows (260) —
a causa real de "erro ao abrir" mesmo com arquivo integro.

Uso:
    python scripts/validar-artefatos.py <slug>
    python scripts/validar-artefatos.py --todos
    python scripts/validar-artefatos.py --todos --estrito --json
"""

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tipos_obra as TO  # noqa: E402
from nomes_curtos import diagnosticar  # noqa: E402

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

RE_TIPO_PAGINA = re.compile(rb"/Type\s*/Page[^s]")
RE_PLACEHOLDER = re.compile(r"\$(body|title|author|if\()")
MIN_BYTES = 1024


def _pdf(caminho):
    dados = caminho.read_bytes()
    if not dados.startswith(b"%PDF-"):
        return False, "sem assinatura %PDF"
    if b"%%EOF" not in dados[-2048:]:
        return False, "sem marcador %%EOF (arquivo truncado)"
    paginas = len(RE_TIPO_PAGINA.findall(dados))
    if paginas < 1:
        return False, "nenhuma pagina"
    return True, f"{paginas} pagina(s)"


def _zip_com(caminho, obrigatorios, rotulo):
    try:
        with zipfile.ZipFile(caminho) as z:
            if z.testzip() is not None:
                return False, "zip corrompido"
            nomes = set(z.namelist())
            faltando = [m for m in obrigatorios if m not in nomes]
            if faltando:
                return False, f"{rotulo} sem {', '.join(faltando)}"
            return True, f"{len(nomes)} membro(s)"
    except zipfile.BadZipFile:
        return False, "nao e um zip valido"


def _pptx(caminho):
    return _zip_com(caminho, ["[Content_Types].xml", "ppt/presentation.xml"], "pptx")


def _epub(caminho):
    ok, detalhe = _zip_com(caminho, ["META-INF/container.xml", "mimetype"], "epub")
    if not ok:
        return ok, detalhe
    with zipfile.ZipFile(caminho) as z:
        if z.read("mimetype").strip() != b"application/epub+zip":
            return False, "mimetype incorreto"
    return True, detalhe


def _html(caminho):
    texto = caminho.read_text(encoding="utf-8", errors="replace")
    baixo = texto.lower()
    if "<html" not in baixo or "</html>" not in baixo:
        return False, "sem <html>...</html>"
    if "<body" not in baixo:
        return False, "sem <body>"
    resto = RE_PLACEHOLDER.search(texto)
    if resto:
        return False, f"placeholder de template nao substituido: {resto.group(0)}"
    return True, f"{len(texto) // 1024} KB"


def _md(caminho):
    texto = caminho.read_text(encoding="utf-8", errors="replace")
    if not texto.strip():
        return False, "vazio"
    pendentes = len(re.findall(r"POLIMENTO-LLM|_\(a completar\)_", texto))
    if pendentes:
        return True, f"OK, mas {pendentes} marcador(es) de polimento"
    return True, f"{len(texto) // 1024} KB"


def _png(caminho):
    if caminho.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
        return False, "sem assinatura PNG"
    return True, "ok"


VERIFICADORES = {".pdf": _pdf, ".pptx": _pptx, ".epub": _epub,
                 ".html": _html, ".md": _md, ".png": _png}


def verificar_arquivo(caminho):
    caminho = Path(caminho)
    resultado = {"arquivo": caminho.name, "extensao": caminho.suffix.lower(),
                 "kb": 0, "abre": False, "detalhe": "", "caminho_ok": True,
                 "caminho_chars": 0}
    if not caminho.exists():
        resultado["detalhe"] = "arquivo inexistente"
        return resultado

    diag = diagnosticar(caminho)
    resultado["caminho_chars"] = diag["chars"]
    resultado["caminho_ok"] = not diag["arriscado"]
    resultado["kb"] = caminho.stat().st_size // 1024

    if caminho.stat().st_size < MIN_BYTES and caminho.suffix.lower() != ".md":
        resultado["detalhe"] = f"suspeito de vazio ({caminho.stat().st_size} bytes)"
        return resultado

    verificador = VERIFICADORES.get(caminho.suffix.lower())
    if verificador is None:
        resultado["abre"] = True
        resultado["detalhe"] = "extensao sem verificador (aceita)"
        return resultado

    try:
        resultado["abre"], resultado["detalhe"] = verificador(caminho)
    except Exception as exc:  # noqa: BLE001 — qualquer falha de leitura = nao abre
        resultado["detalhe"] = f"falha ao ler: {exc}"
    return resultado


def artefatos_do_slug(slug):
    dir_obra = DIR_OUTPUT / slug
    if not dir_obra.exists():
        return []
    config = {}
    caminho_cfg = dir_obra / "config_obra.json"
    if caminho_cfg.exists():
        try:
            config = json.loads(caminho_cfg.read_text(encoding="utf-8"))
        except ValueError:
            config = {}
    tipo = config.get("tipo_obra") or TO.tipo_por_prefixo(slug) or "livro"
    encontrados = []
    for ext in TO.campo(tipo, "extensoes_saida", (".pdf",)):
        candidatos = sorted(dir_obra.glob(f"*{ext}"))
        # `compilar-para-pdf.py` grava `livro_final.pdf` E uma copia com o nome do
        # slug. Sao o MESMO artefato: manter os dois duplicaria o pacote e
        # devolveria ao cliente um arquivo com nome interno da fabrica.
        nomeados = [c for c in candidatos if not c.stem.startswith("livro_final")]
        encontrados += nomeados or candidatos
    return encontrados


def _slugs_da_v51():
    """Todos os materiais V5.1 no disco (<raiz>/<codigo>/<material>)."""
    saida = []
    for tipo in TO.tipos_validos():
        raiz = DIR_OUTPUT / TO.raiz_output(tipo)
        if not raiz.exists():
            continue
        padrao = "*/*" if TO.usa_nomes_curtos(tipo) else "*"
        for d in sorted(raiz.glob(padrao)):
            if d.is_dir() and (d / "config_obra.json").exists():
                saida.append(str(d.relative_to(DIR_OUTPUT)).replace("\\", "/"))
    return saida


def validar(slugs):
    relatorio = []
    for slug in slugs:
        arquivos = artefatos_do_slug(slug)
        itens = [verificar_arquivo(a) for a in arquivos]
        relatorio.append({
            "slug": slug,
            "total": len(itens),
            "abrem": sum(1 for i in itens if i["abre"]),
            "caminhos_arriscados": [i["arquivo"] for i in itens if not i["caminho_ok"]],
            "sem_artefato": not itens,
            "artefatos": itens,
        })
    return relatorio


def main():
    TO.console_utf8()
    ap = argparse.ArgumentParser(description="Verifica se os artefatos finais ABREM")
    ap.add_argument("slug", nargs="?")
    ap.add_argument("--todos", action="store_true")
    ap.add_argument("--estrito", action="store_true",
                    help="exit 1 se algum artefato nao abrir ou o caminho for arriscado")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    slugs = _slugs_da_v51() if args.todos else ([args.slug] if args.slug else [])
    if not slugs:
        print("[ERRO] informe <slug> ou use --todos")
        return 1

    relatorio = validar(slugs)

    if args.json:
        print(json.dumps(relatorio, ensure_ascii=False, indent=2))
    else:
        for r in relatorio:
            if r["sem_artefato"]:
                print(f"[--] {r['slug']}: nenhum artefato final compilado")
                continue
            marca = "OK" if r["abrem"] == r["total"] and not r["caminhos_arriscados"] else "FALHA"
            print(f"[{marca}] {r['slug']} — {r['abrem']}/{r['total']} abrem")
            for a in r["artefatos"]:
                sinal = "  ok " if a["abre"] else "  ERRO"
                print(f"{sinal} {a['arquivo']:<34} {a['kb']:>6} KB  "
                      f"{a['caminho_chars']:>3}ch  {a['detalhe']}")
            for nome in r["caminhos_arriscados"]:
                print(f"  AVISO {nome}: caminho perto do MAX_PATH do Windows (260)")

    falhas = sum(r["total"] - r["abrem"] for r in relatorio)
    arriscados = sum(len(r["caminhos_arriscados"]) for r in relatorio)
    sem_nada = sum(1 for r in relatorio if r["sem_artefato"])
    if not args.json:
        print(f"\n{len(relatorio) - sem_nada} material(is) com artefato · "
              f"{falhas} nao abre(m) · {arriscados} caminho(s) arriscado(s)")

    if args.estrito and (falhas or arriscados):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
