#!/usr/bin/env python3
"""
V5 — Gerador de LEAD MAGNET (custo ~0 token).

Um lead magnet e uma QUERY DE AGREGACAO sobre os cards do playbook: cinco dos
seis formatos saem de `json -> template`, sem nenhuma chamada de LLM.

    checklist   agrega ⑥ 'Feito quando' de todos os cards
    armadilhas  agrega ⑦ 'Armadilhas'
    cheatsheet  agrega ④ 'Execucao' (comandos)
    entregas    agrega ③ 'Entregas'
    mapa        sumario_macro (estagios + objetivos) — nao usa cards
    mini-guia   1 card completo + esqueleto para polimento por LLM

O que diferencia lead magnet de todo o resto da fabrica: CTA rastreavel
obrigatorio (R-LM-1). Sem `cta_url`, o gate reprova.

Fonte: playbooks/<slug>--pbk (preferida) ou livros/<slug> (extrai na hora).
Saida: output/lead-magnets/<slug-mae>--lm-NN-<formato>/lead_magnet.md

Uso:
    python scripts/gerar-lead-magnet.py livros/<slug> --formato checklist
    python scripts/gerar-lead-magnet.py livros/<slug> --todos
    python scripts/gerar-lead-magnet.py playbooks/<slug>--pbk --formato armadilhas \
        --cta-url https://exemplo.com/livro --cta-texto "Leia o livro completo"
"""

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

import tipos_obra as TO
from tipos_obra import FORMATOS_LM
from secoes_eita import normalizar

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

MAX_PAGINAS_ITENS = {"checklist": 60, "armadilhas": 40, "cheatsheet": 45,
                     "entregas": 45, "mapa": 30, "mini-guia": 1}
UTM_PADRAO = {"utm_source": "lead-magnet", "utm_medium": "pdf"}


def _ler_json(caminho, padrao=None):
    if caminho.exists():
        try:
            return json.loads(caminho.read_text(encoding="utf-8"))
        except ValueError:
            return padrao if padrao is not None else {}
    return padrao if padrao is not None else {}


def _slugificar(texto, max_len=40):
    t = normalizar(texto)
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t[:max_len].rstrip("-") or "lm"


def _nome_material(formato, mae_simples):
    """Nome do material desambiguado por volume em hub multi-livro (serie).

    'lm-1-armadilhas' colide quando a colecao tem varios volumes (o 2o
    sobrescreve o 1o silenciosamente — bug real na serie AIDD). Com varios
    livros no hub, o codigo curto do volume entra no nome:
    'lm-1-armadilhas-aidd-arquitetura'. Livro unico mantem o nome curto
    (contrato dos testes e da colecao single-book)."""
    from nomes_curtos import codigo_obra
    obra = TO._obra_raiz(mae_simples, DIR_OUTPUT)
    if obra is None:
        return formato
    mae = str(mae_simples).replace("\\", "/").split("/")[-1]
    for raiz in TO._raizes_tipo():
        dir_mae = obra / raiz / mae
        if dir_mae.exists():
            irmaos = [d for d in (obra / raiz).iterdir() if d.is_dir()]
            if len(irmaos) > 1:
                # Sufixo de UMA palavra: `nome_curto` limita a 3 palavras e
                # "mini-guia" + "aidd-arsenal" (4 palavras) truncava para
                # "mini-guia-aidd" — colidindo de novo entre volumes.
                vol = codigo_obra(mae_simples).split("-")[-1]
                return f"{formato}-{vol}"
            return formato
    return formato


def _importar_extrator():
    """Importa o extrator (nome com hifen). Reusa a instancia ja carregada — recarregar
    descartaria qualquer estado ja configurado no modulo."""
    if "extrair_passos_praticos" in sys.modules:
        return sys.modules["extrair_passos_praticos"]
    caminho = DIR_PROJETO / "scripts" / "extrair-passos-praticos.py"
    spec = importlib.util.spec_from_file_location("extrair_passos_praticos", caminho)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["extrair_passos_praticos"] = mod
    spec.loader.exec_module(mod)
    return mod


def resolver_fonte(slug):
    """Devolve (cards, contexto, slug_mae). Aceita slug de playbook ou de livro."""
    extrator = _importar_extrator()

    if slug.startswith("playbooks/"):
        dir_pbk = TO.dir_obra(slug, DIR_OUTPUT)
        cards = [_ler_json(p) for p in sorted((dir_pbk / "passos").glob("passo_*.json"))]
        cfg = _ler_json(dir_pbk / "config_obra.json")
        mae_simples = cfg.get("obra_mae") or cfg.get("livro_mae")
        slug_mae = None
        for raiz in ("livros", "tccs"):
            if mae_simples and TO.dir_obra(f"{raiz}/{mae_simples}", DIR_OUTPUT).exists():
                slug_mae = f"{raiz}/{mae_simples}"
                break
        contexto = extrator.contexto_da_obra(slug_mae) if slug_mae else {
            "slug_mae": slug, "slug_mae_simples": mae_simples or Path(slug).name,
            "titulo_obra": _ler_json(dir_pbk / "sumario_macro.json").get("titulo_obra", ""),
            "introducao": "", "motivo_condutor": {}, "persona": "Praticante",
            "vocabulario": [], "senioridade": cfg.get("senioridade_obra", ""),
            "serie": cfg.get("serie"), "mapa": {}, "estagios": [],
        }
        if not cards:
            print(f"[ERRO] Playbook sem cards: {dir_pbk / 'passos'}")
            return None, None, None
        return cards, contexto, slug_mae or slug

    # Slug de livro/TCC: usa o playbook se ja existir, senao extrai na hora.
    contexto = extrator.contexto_da_obra(slug)
    slug_pbk = TO.slug_curto("playbook", contexto["slug_mae_simples"],
                             nome=contexto.get("titulo_obra", ""))
    dir_pbk = TO.dir_obra(slug_pbk, DIR_OUTPUT)
    cards = [_ler_json(p) for p in sorted((dir_pbk / "passos").glob("passo_*.json"))] \
        if (dir_pbk / "passos").exists() else []
    if not cards:
        print(f"  [i] Playbook ausente — extraindo passos de {slug} na hora (0 token)")
        res = extrator.extrair(slug, montar=False)
        if res is None:
            return None, None, None
        cards, contexto = res["cards"], res["contexto"]
    return cards, contexto, slug


# ── Montagem por formato ──────────────────────────────────────────────────────

def _cta(cfg, slug_mae_simples, formato):
    url = (cfg.get("cta_url") or "").strip()
    texto = (cfg.get("cta_texto") or "").strip() or "Quero a obra completa"
    if url:
        sep = "&" if "?" in url else "?"
        params = dict(UTM_PADRAO, utm_campaign=slug_mae_simples, utm_content=formato)
        url = url + sep + "&".join(f"{k}={v}" for k, v in params.items())
    return url, texto


def _bloco_cta(url, texto, titulo_obra):
    L = ["", "# Próximo passo", "",
         f"Este material é um recorte de **{titulo_obra}**. "
         "A obra completa traz a teoria, os exemplos comentados e as referências.", ""]
    L.append(f"> **{texto}** — {url}" if url else f"> **{texto}**")
    L.append("")
    return "\n".join(L)


def _frontmatter(titulo, subtitulo):
    return ["---", f'title: "{titulo}"', f'subtitle: "{subtitulo}"',
            'author: "Heverton Eduardo Peres"', "lang: pt-BR", "---", ""]


def montar_checklist(cards, ctx, teto=None):
    teto = teto or FORMATOS_LM["checklist"]["max_itens"]
    selecionados = _rodizio(cards, "feito_quando", teto)
    por_card = {}
    for num, _titulo, item in selecionados:
        por_card.setdefault(num, []).append(item)
    itens = len(selecionados)

    L = ["# O checklist", "",
         f"São **{itens} verificações** distribuídas em {len(por_card)} etapas. "
         "Marque cada uma antes de avançar — a ordem importa.", ""]
    for c in cards:
        seus = por_card.get(int(c["numero"]))
        if not seus:
            continue
        L.append(f"## Etapa {int(c['numero'])} — {c['titulo']}")
        L.append("")
        if c.get("objetivo"):
            L += [f"*{c['objetivo']}*", ""]
        for item in seus:
            L.append(f"- [ ] {item}")
        if c.get("gate"):
            L += ["", f"**Verificação automática:** `{c['gate']}`"]
        L.append("")
    return L, itens


def _truncar(texto, limite):
    """Encurta na fronteira de palavra e neutraliza o pipe (quebraria a tabela MD)."""
    t = re.sub(r"\s+", " ", (texto or "")).strip().replace("|", "/")
    if len(t) <= limite:
        return t
    return t[:limite].rsplit(" ", 1)[0] + "…"


def _rodizio(cards, campo, teto):
    """Seleciona ate `teto` itens em RODIZIO entre os cards.

    Cortar pelos primeiros N concentraria o material nos primeiros capitulos; o
    rodizio mantem a cobertura espalhada pela obra inteira. Devolve
    [(numero_card, titulo_card, item)] na ordem dos capitulos."""
    listas = [(c, list(c.get(campo, []))) for c in cards]
    escolhidos, rodada = [], 0
    while len(escolhidos) < teto:
        avancou = False
        for card, itens in listas:
            if rodada < len(itens):
                escolhidos.append((int(card["numero"]), card["titulo"], itens[rodada]))
                avancou = True
                if len(escolhidos) >= teto:
                    break
        if not avancou:
            break
        rodada += 1
    escolhidos.sort(key=lambda t: t[0])
    return escolhidos


def montar_armadilhas(cards, ctx, teto=None):
    teto = teto or FORMATOS_LM["armadilhas"]["max_itens"]
    disponiveis = sum(len(c.get("armadilhas", [])) for c in cards)
    todas = _rodizio(cards, "armadilhas", teto)

    L = ["# As armadilhas", "",
         f"São **{len(todas)} erros** que aparecem com mais frequência em quem está "
         "percorrendo este caminho pela primeira vez. Cada um traz a etapa em que costuma "
         "aparecer.", ""]
    for i, (num, titulo, texto) in enumerate(todas, 1):
        L += [f"## {i}. {texto}", "",
              f"**Onde aparece:** Etapa {num} — {titulo}", ""]
    if disponiveis > len(todas):
        L += [f"*Selecionamos as {len(todas)} mais frequentes, distribuídas por todas "
              f"as etapas. A obra completa cataloga {disponiveis}.*", ""]
    return L, len(todas)


def montar_cheatsheet(cards, ctx, teto=None):
    teto = teto or FORMATOS_LM["cheatsheet"]["max_itens"]
    total = 0
    L = ["# Folha de bancada", "",
         "Todos os comandos, na ordem de execução. Imprima e deixe ao lado do teclado.", ""]
    for c in cards:
        comandos = c.get("comandos") or ([c["gate"]] if c.get("gate") else [])
        comandos = comandos[:max(0, teto - total)]
        if not comandos:
            continue
        total += len(comandos)
        L += [f"## Etapa {int(c['numero'])} — {c['titulo']}", "", "```bash"]
        L += comandos
        L += ["```", ""]
        if c.get("gate"):
            L += [f"*Verificação:* `{c['gate']}`", ""]
        if total >= teto:
            break
    return L, total


def montar_entregas(cards, ctx, teto=None):
    teto = teto or FORMATOS_LM["entregas"]["max_itens"]
    selecionados = _rodizio(cards, "entregas", teto)
    gates = {int(c["numero"]): c.get("gate") for c in cards}

    L = ["# O que você produz", "",
         "Cada etapa entrega artefatos concretos. Esta é a lista completa — "
         "use como inventário do projeto.", "",
         "| Etapa | Entrega | Verificação |", "|---|---|---|"]
    for num, _titulo, entrega in selecionados:
        gate = f"`{gates.get(num)}`" if gates.get(num) else "—"
        L.append(f"| {num} | `{entrega}` | {gate} |")
    L.append("")
    return L, len(selecionados)


def montar_mapa(cards, ctx, teto=None):
    """Uma folha, nao um indice comentado.

    A versao com um `##` + paragrafo por capitulo rendia 7 paginas num livro de
    20 capitulos — quase o dobro do teto do formato. Tabela compacta cabe em 2-3."""
    estagios = ctx.get("estagios") or []
    L = ["# O mapa", "",
         f"A rota completa, do início ao fim. Você é o **{ctx.get('persona', 'praticante')}**.", ""]
    if estagios:
        L += ["| # | Estágio | Etapas |", "|---|---|---|"]
        for e in estagios:
            caps = ", ".join(str(int(c)) for c in e["capitulos"]) or "—"
            L.append(f"| {e['indice']} | {e['nome']} | {caps} |")
        L.append("")

    # Um mapa mostra ONDE as coisas estao, nao o que cada uma faz. A coluna
    # "Objetivo" ocupava 227mm (uma pagina inteira) e fazia o formato estourar o
    # proprio teto — o objetivo de cada etapa ja vive no checklist e no mini-guia.
    # Uma linha por etapa, sem quebra de texto.
    teto = teto or FORMATOS_LM["mapa"]["max_itens"]
    L += ["## As etapas", "", "| # | Etapa | Estágio |", "|---|---|---|"]
    for c in cards[:teto]:
        L.append(f"| {int(c['numero'])} | {_truncar(c['titulo'], 58)} "
                 f"| {_truncar(c.get('estagio') or '—', 22)} |")
    L.append("")
    # O mapa renderiza as DUAS tabelas (estagios + etapas): o contador tem de
    # refletir o total de linhas. Contar so `estagios` reprovava R-LM-7 em
    # obras com 2 estagios e 8 etapas (serie AIDD) — mapa rico, contador raso.
    return L, len(estagios) + len(cards)


def montar_mini_guia(cards, ctx, teto=None):
    c = cards[0]
    L = [f"# {c['titulo']}", "",
         "## Por que esta etapa existe", "",
         c.get("objetivo") or "_(a completar no polimento)_", "",
         "<!-- POLIMENTO-LLM: 2 parágrafos de contexto condensados da §2 Explica do "
         f"capítulo {int(c['numero'])} do livro-mãe. Máx. 180 palavras. -->", "",
         "## O que você vai produzir", ""]
    L += [f"- `{e}`" for e in c.get("entregas", [])] or ["- _(a completar)_"]
    L += ["", "## Passo a passo", ""]
    for bloco in c.get("execucao", []):
        L += [f"### {bloco['titulo']}", "", f"```{bloco['linguagem']}",
              bloco["codigo"], "```", ""]
    if c.get("gate"):
        L += ["## Como saber se deu certo", "", f"```bash\n{c['gate']}\n```", ""]
    if c.get("feito_quando"):
        L += ["Está pronto quando:", ""] + [f"- [ ] {i}" for i in c["feito_quando"]] + [""]
    if c.get("armadilhas"):
        L += ["## Armadilhas desta etapa", ""] + [f"- {a}" for a in c["armadilhas"]] + [""]
    return L, 1


MONTADORES = {
    "checklist": montar_checklist,
    "armadilhas": montar_armadilhas,
    "cheatsheet": montar_cheatsheet,
    "entregas": montar_entregas,
    "mapa": montar_mapa,
    "mini-guia": montar_mini_guia,
}


def indice_do_formato(formato):
    """Indice ESTAVEL do formato no slug (`--lm-05-mapa`).

    Precisa derivar do formato, nao da posicao no laco: com indice posicional,
    `--formato mapa` sozinho gerava `--lm-01-mapa` ao lado do `--lm-05-mapa`
    ja existente, duplicando o material em vez de reescreve-lo."""
    return sorted(FORMATOS_LM).index(formato) + 1


def gerar(slug, formato, indice=None, cta_url=None, cta_texto=None, cards=None,
          ctx=None, max_itens=None):
    if formato not in FORMATOS_LM:
        print(f"[ERRO] formato desconhecido: {formato}. "
              f"Validos: {', '.join(FORMATOS_LM)}")
        return None
    indice = indice_do_formato(formato) if indice is None else indice

    if cards is None or ctx is None:
        cards, ctx, _ = resolver_fonte(slug)
        if cards is None:
            return None

    spec = FORMATOS_LM[formato]
    corpo, n_itens = MONTADORES[formato](cards, ctx, teto=max_itens)

    tema = ctx.get("titulo_obra") or ctx.get("slug_mae_simples", "")
    titulo = spec["titulo_padrao"].format(tema=tema, n=n_itens)
    promessa = spec["promessa"].format(tema=tema, n=n_itens)

    mae_simples = ctx["slug_mae_simples"]
    slug_lm = TO.slug_curto("lead-magnet", mae_simples, sequencia=indice,
                            nome=_nome_material(formato, mae_simples),
                            base=DIR_OUTPUT)
    dir_lm = TO.dir_obra(slug_lm, DIR_OUTPUT)
    for sub in ("imagens", "revisao"):
        (dir_lm / sub).mkdir(parents=True, exist_ok=True)

    cfg_existente = _ler_json(dir_lm / "config_obra.json")
    cfg = TO.defaults_config("lead-magnet", slug_mae_simples=mae_simples, extra={
        "tema": titulo,
        "formato_lm": formato,
        "senioridade_obra": ctx.get("senioridade") or "intermediario",
        "cta_url": cta_url or cfg_existente.get("cta_url", ""),
        "cta_texto": cta_texto or cfg_existente.get("cta_texto", ""),
    })
    if ctx.get("serie"):
        cfg["serie"] = ctx["serie"]
    (dir_lm / "config_obra.json").write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")

    (dir_lm / "sumario_macro.json").write_text(json.dumps({
        "titulo_obra": titulo, "subtitulo": promessa, "tipo_obra": "lead-magnet",
        "formato_lm": formato, "slug_livro_mae": mae_simples,
        "motivo_condutor": ctx.get("motivo_condutor") or {},
        "itens": n_itens,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    url, texto_cta = _cta(cfg, mae_simples, formato)
    md = _frontmatter(titulo, promessa) + corpo
    md.append(_bloco_cta(url, texto_cta, tema))
    (dir_lm / "lead_magnet.md").write_text("\n".join(md), encoding="utf-8")

    meta = {"slug": slug_lm, "formato": formato,
            "titulo": titulo, "promessa": promessa, "itens": n_itens,
            "abaixo_do_minimo": n_itens < spec["min_itens"],
            "cta_configurado": bool(url)}
    (dir_lm / "revisao" / "relatorio_lead_magnet.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    marca = "!" if meta["abaixo_do_minimo"] else "OK"
    print(f"  [{marca}] {formato:<11} {n_itens:>3} item(ns) — {meta['slug']}")
    return meta


def main():
    TO.console_utf8()
    ap = argparse.ArgumentParser(description="Gera lead magnets a partir dos cards do playbook")
    ap.add_argument("slug", help="ex.: livros/meu-livro ou playbooks/meu-livro--pbk")
    ap.add_argument("--formato", choices=sorted(FORMATOS_LM), default=None)
    ap.add_argument("--todos", action="store_true", help="gera todos os formatos")
    ap.add_argument("--cta-url", default=None)
    ap.add_argument("--cta-texto", default=None)
    ap.add_argument("--max-itens", type=int, default=None,
                    help="corta o teto de itens do formato (R-LM-3: ajuste fino de paginas)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not args.formato and not args.todos:
        args.formato = TO.FORMATO_LM_PADRAO

    cards, ctx, _ = resolver_fonte(args.slug)
    if cards is None:
        return 1

    formatos = sorted(FORMATOS_LM) if args.todos else [args.formato]
    metas = []
    for formato in formatos:
        meta = gerar(args.slug, formato, cta_url=args.cta_url,
                     cta_texto=args.cta_texto, cards=cards, ctx=ctx,
                     max_itens=args.max_itens)
        if meta:
            metas.append(meta)

    if args.json:
        print(json.dumps(metas, ensure_ascii=False, indent=2))
    else:
        sem_cta = [m["slug"] for m in metas if not m["cta_configurado"]]
        print(f"\n[OK] {len(metas)} lead magnet(s) gerado(s)")
        if sem_cta:
            print(f"[AVISO] {len(sem_cta)} sem CTA (R-LM-1 vai reprovar). "
                  f"Rode de novo com --cta-url <url>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
