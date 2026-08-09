#!/usr/bin/env python3
"""
V5 — COLECAO como unidade de primeira classe.

Ate a V4 "serie" era apenas uma chave de cor de capa (series_capa.py). A V5
promove o conceito: uma COLECAO e o conjunto de TODOS os artefatos derivados de
um mesmo nucleo canonico (dossie + sumario_macro + motivo_condutor),
compartilhando identidade visual, vocabulario condutor, badge de nivel e CTA.

O manifesto e derivado (nunca editado a mao): varre output/ inteiro, agrupa por
serie_key e grava em <obra>/colecoes/<colecao>.json — o hub da colecao (fallback
plano output/colecoes/ apenas quando nenhum hub existe; ver _dir_colecoes).

Uso:
    python scripts/colecao.py --sincronizar            # todas as colecoes
    python scripts/colecao.py --sincronizar --slug livros/meu-livro
    python scripts/colecao.py --listar
    python scripts/colecao.py <colecao> --status
    python scripts/colecao.py <colecao> --json
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

import tipos_obra as TO
from nomes_curtos import migrar_prefixo_underscore
from series_capa import resolver_cor, resolver_serie_key

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"


_RAIZES_ESTRUTURAIS = frozenset(
    {TO.raiz_output(t) for t in TO.tipos_validos()}
    | {"marketing", "distribuicao", "colecoes"}
)


def _dir_colecoes():
    """Dir padrao (fallback) dos manifestos de colecao.

    Desde a reorg por HUB (V5.2) cada colecao grava o manifesto no hub da
    propria colecao (ver `_dir_colecoes_da`). Este dir e usado apenas para
    colecoes sem hub (layout plano `output/<tipo>/<slug>`) e como default
    monkeypatchavel nos testes."""
    return DIR_OUTPUT / "colecoes"


DIR_COLECOES = _dir_colecoes()


def _hub_da_colecao(membros):
    """Slug do hub onde a colecao mora, ou None (layout plano / misto).

    O hub e o primeiro segmento comum dos slugs de membro que nao seja raiz de
    tipo nem pasta estrutural (ex.: 'analista-financeiro-...-pt/livros/l1'
    -> hub 'analista-financeiro-...-pt'). Mais de um hub distinto ou nenhum
    -> None (fallback plano)."""
    hubs = set()
    for m in membros:
        if "/" in m["slug"]:
            primeira = m["slug"].split("/", 1)[0]
            if primeira and primeira not in _RAIZES_ESTRUTURAIS:
                hubs.add(primeira)
    return next(iter(hubs)) if len(hubs) == 1 else None


def _dir_colecoes_da(chave, membros):
    """Dir dos manifestos da colecao: o hub dela (HUB POR COLEÇÃO) ou o fallback
    plano `output/colecoes/` quando nao ha hub."""
    hub = _hub_da_colecao(membros)
    if hub:
        return DIR_OUTPUT / hub / "colecoes"
    return DIR_COLECOES


def _info_maquina(hub):
    """(maquina, legadas) da colecao do hub — regra 1:1 (V5.3).

    A maquina canonica vive em output/<hub>/maquina (manifesto.json +
    campanhas/snapshot.json). `legadas` lista pastas de marketing/ do hub
    (máquinas antigas por obra) — aviso nao destrutivo para o operador decidir.
    """
    if not hub:
        return None, []
    base_hub = DIR_OUTPUT / hub
    info = None
    man = _ler_json(base_hub / "maquina" / "manifesto.json")
    if man:
        snap = _ler_json(base_hub / "maquina" / "campanhas" / "snapshot.json")
        campanha = _ler_json(base_hub / "campanhas" / "campanha.json")
        desatualizada = bool(
            campanha.get("atualizado_em") and snap
            and snap.get("atualizado_em") != campanha.get("atualizado_em"))
        info = {
            "slug": man.get("slug", ""),
            "titulo": man.get("titulo", ""),
            "status": man.get("status", ""),
            "criada_em": man.get("criada_em", ""),
            "obra_origem": man.get("obra_origem", ""),
            "campanhas": {
                "snapshot": bool(snap),
                "atualizado_em": (snap or {}).get("atualizado_em", ""),
                "desatualizada": desatualizada,
            },
        }
    legadas = []
    mkt = base_hub / "marketing"
    if mkt.is_dir():
        legadas = sorted(p.name for p in mkt.iterdir() if p.is_dir())
    return info, legadas


def _todos_dirs_manifestos():
    """Todos os dirs que podem conter manifestos: fallback plano + hubs.

    Varre `DIR_OUTPUT/*/colecoes` do proprio modulo (monkeypatchavel nos
    testes) — nao depende do DIR_OUTPUT interno de tipos_obra."""
    dirs = {DIR_COLECOES}
    if DIR_OUTPUT.exists():
        for cand in DIR_OUTPUT.glob("*/colecoes"):
            if cand.is_dir():
                dirs.add(cand)
    return dirs


def _metadados_ricos(chave, membros, caminho_atual):
    """Metadados ricos da colecao a fundir no manifesto, idempotente.

    Fonte 1: <hub>/series.json (artefato legado de metadados — nome/subtitulo/
    tema/objetivo/livros/metricas — criado fora dos scripts; o series.json da
    RAIZ de output/ e o registro de cores e nao e tocado). Fonte 2: os
    metadados ja fundidos no manifesto anterior no disco (idempotencia apos a
    fusao). Devolve (dados, caminho_legado|None); o legado e apagado pelo
    chamador DEPOIS de gravar o manifesto com sucesso."""
    hub = _hub_da_colecao(membros)
    if hub:
        legado = DIR_OUTPUT / hub / "series.json"
        if legado.exists():
            return _ler_json(legado), legado
    if caminho_atual.exists():
        antigo = _ler_json(caminho_atual)
        if isinstance(antigo, dict) and antigo.get("metadados"):
            return antigo["metadados"], None
    return {}, None


def _ler_json(caminho, padrao=None):
    if caminho.exists():
        try:
            return json.loads(caminho.read_text(encoding="utf-8"))
        except ValueError:
            return padrao if padrao is not None else {}
    return padrao if padrao is not None else {}


def _slug_arquivo(nome):
    return re.sub(r"[^a-z0-9]+", "-", (nome or "").lower()).strip("-") or "colecao"


def _artefatos(dir_obra, tipo):
    extensoes = TO.campo(tipo, "extensoes_saida", (".pdf",))
    saida = []
    for ext in extensoes:
        saida += [p.name for p in sorted(dir_obra.glob(f"*{ext}"))]
    return saida


def _estado(dir_obra, tipo, artefatos):
    if artefatos:
        return "compilado"
    if (dir_obra / "capitulos").exists() and any((dir_obra / "capitulos").glob("*.md")):
        return "redigido"
    if (dir_obra / "passos").exists() and any((dir_obra / "passos").glob("*.json")):
        return "extraido"
    if (dir_obra / "sumario_macro.json").exists():
        return "planejado"
    return "vazio"


def varrer():
    """Percorre output/ e devolve {serie_key: [membro, ...]}."""
    colecoes = {}
    for tipo in TO.tipos_validos():
        # `listar_materiais` conhece os dois layouts: V4 raso (<raiz>/<slug>) e
        # V5.1 aninhado (<raiz>/<codigo>/<material>). Varrer com `iterdir()` direto
        # encontrava a pasta de CODIGO no lugar do material e, como ela nao tem
        # config_obra.json, inventava uma colecao com o nome do codigo.
        for slug in TO.listar_materiais(tipo, DIR_OUTPUT):
            dir_obra = TO.dir_obra(slug, DIR_OUTPUT)
            config = _ler_json(dir_obra / "config_obra.json")
            sumario = _ler_json(dir_obra / "sumario_macro.json")
            # O tipo declarado no config manda; o prefixo e so o fallback.
            tipo_real = config.get("tipo_obra") or tipo
            chave = resolver_serie_key(config, slug)
            artefatos = _artefatos(dir_obra, tipo_real)
            colecoes.setdefault(chave, []).append({
                "slug": slug,
                "tipo": tipo_real,
                "rotulo": TO.campo(tipo_real, "rotulo", tipo_real),
                "titulo": sumario.get("titulo_obra") or config.get("tema") or dir_obra.name,
                "obra_mae": config.get("obra_mae") or config.get("livro_mae"),
                "natureza": TO.campo(tipo_real, "natureza", "?"),
                "custo_llm": TO.campo(tipo_real, "custo_llm", "?"),
                "senioridade": config.get("senioridade_obra", ""),
                "cta_url": config.get("cta_url", ""),
                "estado": _estado(dir_obra, tipo_real, artefatos),
                "artefatos": artefatos,
            })
    return colecoes


def montar_manifesto(chave, membros, metadados=None):
    raizes = [m for m in membros if not TO.campo(m["tipo"], "derivado_de", ())]
    nucleo = raizes[0] if raizes else (membros[0] if membros else {})
    motivo = {}
    if nucleo:
        motivo = _ler_json(TO.dir_obra(nucleo["slug"], DIR_OUTPUT) / "sumario_macro.json") \
            .get("motivo_condutor", {})

    faltantes = [t for t in TO.tipos_derivados()
                 if t not in {m["tipo"] for m in membros}]
    sem_cta = [m["slug"] for m in membros
               if TO.campo(m["tipo"], "exige_cta") and not m["cta_url"]]
    maquina, maquinas_legadas = _info_maquina(_hub_da_colecao(membros))

    manifesto = {
        "colecao": chave,
        "cor_accent": resolver_cor(chave),
        "atualizado_em": date.today().isoformat(),
        "nucleo": {
            "slug": nucleo.get("slug", ""),
            "tipo": nucleo.get("tipo", ""),
            "titulo": nucleo.get("titulo", ""),
            "senioridade": nucleo.get("senioridade", ""),
            "motivo_condutor": motivo,
        },
        "total_membros": len(membros),
        "por_tipo": {t: sum(1 for m in membros if m["tipo"] == t)
                     for t in sorted({m["tipo"] for m in membros})},
        "membros": sorted(membros, key=lambda m: (m["tipo"], m["slug"])),
        "derivados_ausentes": faltantes,
        "membros_sem_cta": sem_cta,
        "maquina": maquina,
        "maquinas_legadas": maquinas_legadas,
    }
    if metadados:
        manifesto["metadados"] = metadados
    return manifesto


def sincronizar(slug=None):
    migrar_prefixo_underscore(DIR_COLECOES)       # _colecoes -> colecoes
    colecoes = varrer()
    if slug:
        alvo = resolver_serie_key(_ler_json(TO.dir_obra(slug, DIR_OUTPUT) / "config_obra.json"), slug)
        colecoes = {k: v for k, v in colecoes.items() if k == alvo}

    # Limpeza global: sem ela, um manifesto de uma chave que deixou de existir
    # (renomeacao de pasta, mudanca de `serie`) sobrevive no disco e reaparece
    # em --listar como se a colecao ainda existisse. Varre o fallback plano E
    # todos os hubs.
    if slug is None:
        vivos = {f"{_slug_arquivo(k)}.json" for k in colecoes}
        for dir_manifestos in _todos_dirs_manifestos():
            if not dir_manifestos.exists():
                continue
            for antigo in dir_manifestos.glob("*.json"):
                if antigo.name not in vivos:
                    antigo.unlink()

    manifestos = []
    for chave, membros in sorted(colecoes.items()):
        destino = _dir_colecoes_da(chave, membros)
        destino.mkdir(parents=True, exist_ok=True)
        caminho = destino / f"{_slug_arquivo(chave)}.json"
        metadados, legado = _metadados_ricos(chave, membros, caminho)
        manifesto = montar_manifesto(chave, membros, metadados)
        caminho.write_text(
            json.dumps(manifesto, ensure_ascii=False, indent=2), encoding="utf-8")
        if legado is not None:
            legado.unlink()     # fundido no manifesto; series.json do hub nao existe mais
        manifestos.append(manifesto)
    return manifestos


def carregar(chave):
    """Manifesto da colecao, ou None se ela ainda nao foi sincronizada."""
    migrar_prefixo_underscore(DIR_COLECOES)
    nome = f"{_slug_arquivo(chave)}.json"
    for dir_manifestos in _todos_dirs_manifestos():
        caminho = dir_manifestos / nome
        if caminho.exists():
            return _ler_json(caminho)
    return None


def _imprimir(manifesto):
    print(f"\nCOLECAO: {manifesto['colecao']}  ({manifesto['cor_accent']})")
    n = manifesto["nucleo"]
    print(f"  Nucleo : {n.get('titulo', '')} [{n.get('tipo', '')}] {n.get('slug', '')}")
    motivo = n.get("motivo_condutor") or {}
    if motivo.get("nome"):
        print(f"  Motivo : {motivo['nome']} — persona: {motivo.get('persona_leitor', '?')}")
    print(f"  {'TIPO':<13} {'ESTADO':<11} {'CUSTO':<7} TITULO")
    print("  " + "-" * 66)
    for m in manifesto["membros"]:
        print(f"  {m['tipo']:<13} {m['estado']:<11} {m['custo_llm']:<7} {m['titulo'][:38]}")
    if manifesto["derivados_ausentes"]:
        print(f"  [i] Derivados ausentes: {', '.join(manifesto['derivados_ausentes'])}")
    if manifesto["membros_sem_cta"]:
        print(f"  [!] Sem CTA: {', '.join(manifesto['membros_sem_cta'])}")
    maquina = manifesto.get("maquina")
    if maquina:
        camp = maquina.get("campanhas") or {}
        flag = " [campanha desatualizada]" if camp.get("desatualizada") else ""
        print(f"  [OK] Maquina: {maquina.get('slug', '?')} ({maquina.get('status', '?')})"
              f"{flag}")
    legadas = manifesto.get("maquinas_legadas") or []
    if legadas:
        print(f"  [!] Maquinas legadas em marketing/: {', '.join(legadas)}")


def main():
    TO.console_utf8()
    ap = argparse.ArgumentParser(description="Colecao como unidade de primeira classe (V5)")
    ap.add_argument("colecao", nargs="?", help="nome da colecao (serie_key)")
    ap.add_argument("--sincronizar", action="store_true", help="varre output/ e regrava os manifestos")
    ap.add_argument("--slug", default=None, help="limita a sincronizacao a colecao desta obra")
    ap.add_argument("--listar", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.sincronizar:
        manifestos = sincronizar(slug=args.slug)
        if args.json:
            print(json.dumps(manifestos, ensure_ascii=False, indent=2))
            return 0
        dirs_usados = sorted(
            {str(p.relative_to(DIR_PROJETO)) for p in _todos_dirs_manifestos()
             if p.exists() and any(p.glob("*.json"))})
        onde = ", ".join(dirs_usados) or str(DIR_COLECOES)
        print(f"[OK] {len(manifestos)} colecao(oes) sincronizada(s) em {onde}")
        for m in manifestos:
            print(f"  {m['colecao']:<34} {m['total_membros']:>3} membro(s)  {m['por_tipo']}")
        return 0

    if args.listar or (not args.colecao):
        manifestos = []
        for dir_manifestos in _todos_dirs_manifestos():
            if dir_manifestos.exists():
                manifestos += [_ler_json(p)
                               for p in sorted(dir_manifestos.glob("*.json"))]
        manifestos = [m for m in manifestos if isinstance(m, dict)]
        if not manifestos:
            print("[i] Nenhum manifesto. Rode: python scripts/colecao.py --sincronizar")
            return 0
        if args.json:
            print(json.dumps(manifestos, ensure_ascii=False, indent=2))
            return 0
        print(f"{'COLECAO':<34} {'MEMBROS':>7}  COMPOSICAO")
        print("-" * 78)
        for m in manifestos:
            print(f"{m['colecao']:<34} {m['total_membros']:>7}  {m['por_tipo']}")
        return 0

    manifesto = carregar(args.colecao)
    if manifesto is None:
        print(f"[ERRO] colecao nao encontrada: {args.colecao}. "
              f"Rode --sincronizar primeiro.")
        return 1
    if args.json:
        print(json.dumps(manifesto, ensure_ascii=False, indent=2))
        return 0
    _imprimir(manifesto)
    return 0


if __name__ == "__main__":
    sys.exit(main())
