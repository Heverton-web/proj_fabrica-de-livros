#!/usr/bin/env python3
"""
Transmutacao (V5.2) — reescreve um material EXISTENTE de um tipo para outro.

Cria o esqueleto do material DESTINO a partir do recorte da ORIGEM (titulos e
objetivos das unidades), preservando motivo_condutor, serie, senioridade e o
dossie da origem (reuso de fontes — o redator nao pesquisa do zero). O conteudo
em si e trabalho dos subagentes redatores (skill do tipo DESTINO, Modo
Transmutacao), despachados pelo comando /reescrever-como.

Valida o par contra a matriz `reescrever_de` do registro de tipos e registra o
material novo em `derivados.json` da origem. A ORIGEM nunca e alterada.

Uso:
    python scripts/transmutar-obra.py <slug-origem> --tipo <destino> [--slug <novo>]
    python scripts/transmutar-obra.py livros/meu-livro --tipo tcc
    python scripts/transmutar-obra.py ebooks/meu-livro--eb-01-x --tipo livro

Recortes suportados (origem -> unidade):
    livro/tcc/artigo/ebook  -> capitulos do sumario_macro.json (ou cap_*.md)
    playbook                -> cards passos/passo_*.json

Slug do destino: <origem-simples><sufixo> (--liv / --tcc / --ebk / --art),
criado no layout plano output/<raiz-do-destino>/<slug>.
"""

import argparse
import importlib.util
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

import tipos_obra as TO

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

# Sufixos de slug da transmutacao (destinos raiz nao tem `sufixo_slug` proprio;
# derivados ja usam o deles, ex. --eb/--art, entao a transmutacao usa outro
# sufixo para o mesmo tipo-destino).
SUFIXO_TRANSMUTACAO = {
    "livro": "--liv",
    "tcc": "--tcc",
    "ebook": "--ebk",
    "artigo": "--art",
}


def console_utf8():
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def _exibir(caminho):
    try:
        return caminho.relative_to(DIR_PROJETO)
    except ValueError:
        return caminho


def tipo_da_origem(slug, dir_origem):
    """Tipo da origem: pelo prefixo do slug ou pelo config_obra.json."""
    tipo = TO.tipo_por_prefixo(slug)
    if tipo:
        return tipo
    cfg = dir_origem / "config_obra.json"
    if cfg.exists():
        try:
            return json.loads(cfg.read_text(encoding="utf-8")).get("tipo_obra")
        except ValueError:
            pass
    return None


def _titulo_de_arquivo(caminho):
    """Primeira linha de cabecalho '# ...' de um capítulo .md."""
    try:
        texto = caminho.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return caminho.stem
    for linha in texto.splitlines()[:5]:
        if linha.startswith("#"):
            return linha.lstrip("# ").strip()
    return caminho.stem


def unidades_da_origem(tipo, dir_origem, sumario):
    """Recorta a origem em unidades {titulo, objetivo} para o destino."""
    if tipo == "playbook":
        passos = sorted((dir_origem / "passos").glob("passo_*.json")) \
            if (dir_origem / "passos").exists() else []
        unidades = []
        for p in passos:
            try:
                card = json.loads(p.read_text(encoding="utf-8"))
            except ValueError:
                continue
            unidades.append({
                "titulo": card.get("titulo") or p.stem,
                "objetivo": card.get("objetivo_material", ""),
            })
        return unidades

    if sumario and sumario.get("partes"):
        unidades = []
        for parte in sumario["partes"]:
            for cap in parte.get("capitulos", []):
                unidades.append({
                    "capitulo": str(cap.get("capitulo")),
                    "titulo": cap.get("titulo", ""),
                    "objetivo": cap.get("objetivo", ""),
                })
        if unidades:
            return unidades

    # Fallback: capítulos no disco (ebook/artigo com sumario sem "partes").
    caps = sorted((dir_origem / "capitulos").glob("cap_*.md")) \
        if (dir_origem / "capitulos").exists() else []
    unidades = []
    for p in caps:
        num = re.search(r"cap_(\d+)", p.stem)
        unidades.append({
            "capitulo": num.group(1) if num else p.stem,
            "titulo": _titulo_de_arquivo(p),
            "objetivo": "",
        })
    return unidades


def slug_transmutado(slug_origem_simples, tipo_destino):
    sufixo = SUFIXO_TRANSMUTACAO.get(tipo_destino, f"--{tipo_destino[:4]}")
    return f"{slug_origem_simples}{sufixo}"


def _copiar_dossie(dir_origem, dir_destino):
    """Reusa as fontes da origem no destino (melhor esforco, nunca falha)."""
    origem = dir_origem / "pesquisa"
    if not origem.exists():
        return 0
    destino = dir_destino / "pesquisa"
    destino.mkdir(parents=True, exist_ok=True)
    copiados = 0
    for f in origem.glob("dossie_*.md"):
        shutil.copy2(f, destino / f.name)
        copiados += 1
    return copiados


def _carregar_fatiar():
    """Carrega fatiar-obra.py (nome com hifen) via importlib — convencao dos testes."""
    caminho = Path(__file__).with_name("fatiar-obra.py")
    spec = importlib.util.spec_from_file_location("fatiar_obra", caminho)
    modulo = importlib.util.module_from_spec(spec)
    sys.modules["fatiar_obra"] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def transmutar(slug_origem, tipo_destino, novo_slug=None, base=None):
    """Recorta a origem e cria o esqueleto do destino. Retorna dict de resultado."""
    base = Path(base) if base is not None else DIR_OUTPUT
    dir_origem = TO.dir_obra(slug_origem, base)
    if not dir_origem.exists():
        return {"erro": f"origem nao encontrada: {slug_origem}"}

    tipo_origem = tipo_da_origem(slug_origem, dir_origem)
    if not tipo_origem:
        return {"erro": f"nao foi possivel determinar o tipo da origem {slug_origem}"}
    if tipo_destino not in TO.TIPOS:
        return {"erro": f"tipo-destino desconhecido: {tipo_destino} "
                        f"(validos: {', '.join(TO.TIPOS)})"}
    if tipo_origem == tipo_destino:
        return {"erro": f"destino igual a origem ({tipo_origem} -> {tipo_origem}); "
                        "use /reescrever para reescrever no mesmo tipo"}

    erros = TO.validar_reescrita(tipo_destino, tipo_origem)
    if erros:
        return {"erro": erros[0]}

    sumario = None
    caminho_sumario = dir_origem / "sumario_macro.json"
    if caminho_sumario.exists():
        try:
            sumario = json.loads(caminho_sumario.read_text(encoding="utf-8"))
        except ValueError:
            sumario = None

    unidades = unidades_da_origem(tipo_origem, dir_origem, sumario)
    if not unidades:
        return {"erro": f"origem {slug_origem} nao tem unidades para recortar "
                        "(sem capitulos nem cards)"}

    config_origem = {}
    cfg_path = dir_origem / "config_obra.json"
    if cfg_path.exists():
        try:
            config_origem = json.loads(cfg_path.read_text(encoding="utf-8"))
        except ValueError:
            config_origem = {}

    titulo_origem = (sumario or {}).get("titulo_obra") or config_origem.get("tema") \
        or Path(slug_origem).name
    rotulo_destino = TO.campo(tipo_destino, "rotulo", tipo_destino)
    titulo_destino = f"{titulo_origem} — {rotulo_destino}"

    slug_origem_simples = str(slug_origem).replace("\\", "/").split("/")[-1]
    slug_destino = novo_slug or slug_transmutado(slug_origem_simples, tipo_destino)
    dir_destino = base / TO.raiz_output(tipo_destino) / slug_destino
    for sub in ("capitulos", "revisao", "imagens"):
        (dir_destino / sub).mkdir(parents=True, exist_ok=True)
    dossie_copiados = _copiar_dossie(dir_origem, dir_destino)

    motivo = (sumario or {}).get("motivo_condutor") or {}
    partes = [{
        "parte": "I",
        "titulo_parte": "Parte Única" if len(unidades) <= 8 else "Parte I",
        "capitulos": [
            {"capitulo": str(i + 1),
             "titulo": u.get("titulo") or f"Unidade {i + 1}",
             "objetivo": u.get("objetivo", "")}
            for i, u in enumerate(unidades)
        ],
    }]
    (dir_destino / "sumario_macro.json").write_text(json.dumps({
        "titulo_obra": titulo_destino,
        "tipo_obra": tipo_destino,
        "slug_origem": slug_origem,
        "tipo_origem": tipo_origem,
        "motivo_condutor": motivo,
        "partes": partes,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    cfg = TO.defaults_config(tipo_destino, slug_mae_simples=slug_origem_simples, extra={
        "tema": titulo_destino,
        "slug_origem": slug_origem,
        "tipo_origem": tipo_origem,
        "modo_producao": "transmutacao",
    })
    if config_origem.get("serie"):
        cfg["serie"] = config_origem["serie"]
    if config_origem.get("senioridade_obra"):
        cfg["senioridade_obra"] = config_origem["senioridade_obra"]
    (dir_destino / "config_obra.json").write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")

    # Registro na origem: derivados.json (preserva secoes existentes).
    try:
        fatiar = _carregar_fatiar()
        derivados = fatiar.carregar_derivados(dir_origem, slug_origem_simples)
        fatiar.gravar_derivados(dir_origem, derivados, tipo_destino, [{
            "indice": 1,
            "titulo": titulo_destino,
            "slug": slug_destino,
            "diretorio": f"{TO.raiz_output(tipo_destino)}/{slug_destino}",
            "tipo_origem": tipo_origem,
            "transmutacao": True,
        }], slug_origem_simples)
    except Exception as exc:  # noqa: BLE001 — registro e conveniencia
        print(f"[AVISO] falha ao registrar em derivados.json da origem: {exc}")

    resultado = {
        "slug_origem": slug_origem,
        "tipo_origem": tipo_origem,
        "tipo_destino": tipo_destino,
        "slug_destino": f"{TO.raiz_output(tipo_destino)}/{slug_destino}",
        "diretorio": str(_exibir(dir_destino)),
        "titulo": titulo_destino,
        "unidades": len(unidades),
        "dossie_copiados": dossie_copiados,
        "criado_em": datetime.now().isoformat(timespec="seconds"),
    }
    (dir_destino / "revisao" / "relatorio_transmutacao.json").write_text(
        json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    return resultado


def main():
    console_utf8()
    ap = argparse.ArgumentParser(description="Transmutacao: reescreve material "
                                             "de um tipo para outro (V5.2)")
    ap.add_argument("slug", help="slug da origem (ex.: livros/meu-livro)")
    ap.add_argument("--tipo", required=True, help="tipo-destino (livro, tcc, ebook, artigo)")
    ap.add_argument("--slug-novo", dest="novo_slug", default=None,
                    help="slug simples do destino (padrao: <origem><sufixo>)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    resultado = transmutar(args.slug, args.tipo, novo_slug=args.novo_slug)
    if "erro" in resultado:
        print(f"[ERRO] {resultado['erro']}")
        return 1

    if args.json:
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
        return 0

    print(f"TRANSMUTACAO - {resultado['slug_origem']} -> {resultado['tipo_destino']}")
    print(f"  destino    : {resultado['diretorio']}")
    print(f"  titulo     : {resultado['titulo']}")
    print(f"  unidades   : {resultado['unidades']}")
    print(f"  dossie     : {resultado['dossie_copiados']} arquivo(s) reusado(s)")
    print(f"\nProximo passo (subagentes do tipo {resultado['tipo_destino']}):")
    print(f"  despache os redatores com as unidades do sumario como base "
          f"(skill {resultado['tipo_destino']}, Modo Transmutacao).")
    print("  Gates do DESTINO obrigatorios apos a redacao "
          "(auditar-obra.py --estrito + validar-codigo.py --executar).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
