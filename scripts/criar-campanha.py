#!/usr/bin/env python3
"""
Criar-Campanha (V5.3) — gera a camada CAMPANHA de uma colecao.

Deterministico (custo zero de LLM): estrutura de pastas, moldes de texto com
rascunho extraido do material (config_obra + sumario_macro + manifesto da
colecao), artes HTML+CSS->Chromium (PNG) e cronogramas com datas reais. A copy
final e escrita pelo agente (comando /campanha) sobre os moldes.

Uso:
    python scripts/criar-campanha.py --material <slug> [--regenerar] [--sem-artes]
    python scripts/criar-campanha.py --material <slug> --marcar-completa
    python scripts/criar-campanha.py --completo [<colecao>] [--regenerar] [--sem-artes]
    python scripts/criar-campanha.py --listar
"""

import argparse
import json
import re
import string
import sys
from datetime import date, timedelta
from pathlib import Path

import campanha as CP
import tipos_obra as TO
from series_capa import resolver_cor

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

SEMANAS = ["segunda-feira", "terca-feira", "quarta-feira", "quinta-feira",
           "sexta-feira", "sabado", "domingo"]

NIVEL_ROTULO = {"iniciante": "Iniciante", "intermediario": "Intermediario",
                "avancado": "Avancado", "especialista": "Especialista"}


def _ler_json(caminho, padrao=None):
    try:
        return json.loads(Path(caminho).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return padrao


# ── Helpers de identidade visual ─────────────────────────────────────────────

def _hex_para_rgb(hex_cor):
    hex_cor = str(hex_cor or "").strip().lstrip("#")
    if len(hex_cor) != 6 or not re.fullmatch(r"[0-9a-fA-F]{6}", hex_cor):
        return (46, 204, 113)  # verde padrao
    return tuple(int(hex_cor[i:i + 2], 16) for i in (0, 2, 4))


def cor2(hex_cor):
    """Versao escurecida da cor de accent (gradiente do CTA)."""
    r, g, b = _hex_para_rgb(hex_cor)
    return f"#{int(r * .45):02x}{int(g * .45):02x}{int(b * .45):02x}"


def cor_soft(hex_cor, alpha=0.30):
    r, g, b = _hex_para_rgb(hex_cor)
    return f"rgba({r}, {g}, {b}, {alpha})"


def nivel_rotulo(senioridade):
    return NIVEL_ROTULO.get((senioridade or "").lower(), "Nivel")


def variaveis_arte(ctx):
    """Variaveis comuns de interpolacao dos templates HTML de arte."""
    vocab = ctx.get("vocabulario") or []
    tags = "".join(f'<span class="tag">{t}</span>' for t in vocab[:4])
    if not tags:
        tags = f'<span class="tag">{ctx["colecao"]}</span>'
    return {
        "TITULO": (ctx["titulo"] or ctx["colecao"])[:64],
        "SUBTITULO": (ctx.get("subtitulo") or ctx.get("projeto_pratico")
                      or ctx["colecao"])[:110],
        "NIVEL": nivel_rotulo(ctx.get("senioridade")),
        "COR": ctx.get("cor_accent") or "#2ecc71",
        "COR2": cor2(ctx.get("cor_accent") or "#2ecc71"),
        "COR_SOFT": cor_soft(ctx.get("cor_accent") or "#2ecc71"),
        "TAGS": tags,
        "CTA": ctx.get("cta") or "Saiba mais",
        "COLECAO": ctx["colecao"],
        "SLUG": ctx["nome"],
    }


# ── Moldes de texto ──────────────────────────────────────────────────────────

def _molde_cabecalho(ctx, formato, extra=""):
    """Cabecalho de contexto do molde de texto."""
    vocabulario = ", ".join(ctx.get("vocabulario") or [])
    return (
        "<!--\n"
        "CAMPANHA {colecao} — material {nome} ({tipo})\n"
        "Formato: {formato}\n"
        "Status: RASCUNHO — reescreva a copy final com LLM (tom de divulgacao,"
        " vocabulario da colecao) antes de validar.\n"
        "Contexto: titulo={titulo}\n"
        "Subtítulo: {subtitulo}\n"
        "Vocabulário: {vocabulario}\n"
        "CTA: {cta} {cta_url}\n"
        "{extra}"
        "-->\n\n"
    ).format(
        colecao=ctx["colecao"], nome=ctx["nome"], tipo=ctx["tipo"],
        formato=formato, titulo=ctx["titulo"], subtitulo=ctx.get("subtitulo"),
        vocabulario=vocabulario, cta=ctx.get("cta"),
        cta_url=ctx.get("cta_url") or "", extra=extra,
    ).rstrip() + "\n"


def _rascunho(ctx, formato):
    """Corpo determinístico do molde: derivado do material, nunca vazio."""
    titulo = ctx["titulo"]
    subtitulo = ctx.get("subtitulo") or ctx.get("projeto_pratico") or ctx["colecao"]
    cta = f"{ctx.get('cta')}{' — ' + ctx['cta_url'] if ctx.get('cta_url') else ''}"
    vocabulario = ", ".join(ctx.get("vocabulario") or []) or ctx["colecao"]
    if formato == "resposta-direct":
        return (f"Olá! Obrigado pelo contato. O material de hoje fala sobre "
                f"{subtitulo.lower()} — um guia direto para quem quer entender "
                f"{vocabulario.lower()} na prática. {cta}. Posso te ajudar com "
                f"alguma dúvida específica sobre o conteúdo?")
    if formato.startswith("email"):
        return (f"Assunto: {titulo}: o guia que você estava esperando\n\n"
                f"Oi, tudo bem?\n\nSe você acompanha {ctx['colecao']}, sabe que "
                f"{subtitulo.lower()} é um dos temas que mais transformam "
                f"resultados. Neste material, você encontra o caminho completo: "
                f"{vocabulario.lower()} aplicado na prática, sem teoria solta.\n\n"
                f"Leia agora e leve o aprendizado para o seu dia a dia: {cta}.")
    if formato.startswith("msg"):
        return (f"{titulo} chegou! {subtitulo.capitalize()}. Resumo prático em "
                f"3 pontos: {vocabulario.lower()}. Quer o detalhe? {cta}.")
    return (f"{titulo}: {subtitulo.lower()}. Conteúdo prático sobre "
            f"{vocabulario.lower()} — feito para aplicar hoje mesmo. {cta}.")


def escrever_moldes(ctx, base):
    """Moldes de texto para redes sociais e canais (nao sobrescreve edits)."""
    escritos = []
    for rede, dados in CP.REDES_SOCIAIS.items():
        raiz = CP.dir_campanha_material(ctx["slug"], base) / f"redes-sociais/{rede}"
        for pasta, quantidade in dados.get("textos", {}).items():
            for i in range(1, quantidade + 1):
                arquivo = raiz / CP.pasta_de_texto(pasta, None) / CP.texto_nome(pasta, i)
                if arquivo.exists() and not ctx.get("__regenerar__"):
                    continue
                formato = "feed-story" if pasta == "feed-story" else pasta
                corpo = ("# Post {i} — {titulo}\n\n" if pasta == "post"
                         else "# Story {i} — {titulo}\n\n" if pasta == "feed-story"
                         else "# Resposta Direct\n\n")
                arquivo.parent.mkdir(parents=True, exist_ok=True)
                arquivo.write_text(
                    _molde_cabecalho(ctx, f"{rede}/{pasta}") + corpo.format(
                        i=i, titulo=ctx["titulo"]) + _rascunho(ctx, formato) + "\n",
                    encoding="utf-8")
                escritos.append(arquivo)
    for canal, dados in CP.CANAIS_COMUNICACAO.items():
        for sequencia, conf in dados.get("sequencias", {}).items():
            prefixo = "email" if canal == "emails" else "msg"
            quantidade = conf.get("textos", 0)
            raiz = (CP.dir_campanha_material(ctx["slug"], base)
                    / f"canais-comunicacao/{canal}/{sequencia}/textos")
            for i in range(1, quantidade + 1):
                arquivo = raiz / CP.texto_nome(prefixo, i, sequencia)
                if arquivo.exists() and not ctx.get("__regenerar__"):
                    continue
                arquivo.parent.mkdir(parents=True, exist_ok=True)
                arquivo.write_text(
                    _molde_cabecalho(ctx, f"{canal}/{sequencia}") +
                    f"# {prefixo.title()} {i} — {sequencia.replace('-', ' ')}\n\n"
                    + _rascunho(ctx, f"{prefixo}-{i}") + "\n",
                    encoding="utf-8")
                escritos.append(arquivo)
    return escritos


# ── Artes (HTML -> Chromium -> PNG) ──────────────────────────────────────────

def _interpolar_arte(nome_template, ctx):
    caminho = CP.DIR_TEMPLATES / nome_template
    html = caminho.read_text(encoding="utf-8")
    return string.Template(html).safe_substitute(**variaveis_arte(ctx))


def _renderizar_png(html, png_path, dim):
    """Playwright Chromium: viewport = dimensao do formato, screenshot do corpo."""
    from playwright.sync_api import sync_playwright
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        tmp_html = Path(tmp) / "arte.html"
        tmp_html.write_text(html, encoding="utf-8")
        with sync_playwright() as p:
            navegador = p.chromium.launch()
            pagina = navegador.new_page(viewport={"width": dim[0], "height": dim[1]})
            pagina.goto(f"file:///{tmp_html.resolve().as_posix()}",
                        wait_until="networkidle")
            pagina.screenshot(path=str(png_path))
            navegador.close()
    return png_path


def gerar_artes(ctx, base, com_artes=True):
    """Artes PNG (post/story/arte) por material. HTML interpolado fica ao lado
    como fonte editavel da arte."""
    geradas = []
    for rede, dados in CP.REDES_SOCIAIS.items():
        raiz = CP.dir_campanha_material(ctx["slug"], base) / f"redes-sociais/{rede}"
        for formato, dim in dados.get("artes", {}).items():
            nome_template = CP.TEMPLATES_ARTE[
                "post_ig" if (rede, formato) == ("instagram", "post")
                else "post_linkedin" if rede == "linkedin"
                else "feed-story" if formato == "feed-story"
                else "post_ig"]
            prefixo = "post" if formato == "post" else "story"
            html = _interpolar_arte(nome_template, ctx)
            for i in (1,):
                destino = raiz / f"artes/{formato}"
                destino.mkdir(parents=True, exist_ok=True)
                base_html = destino / f"{prefixo}-{i:02d}.html"
                png = destino / f"{prefixo}-{i:02d}.png"
                base_html.write_text(html, encoding="utf-8")
                if com_artes:
                    try:
                        _renderizar_png(html, png, dim)
                        geradas.append(png)
                    except Exception as exc:  # noqa: BLE001
                        print(f"[AVISO] arte nao renderizada ({rede}/{formato}): {exc}")
    for canal, dados in CP.CANAIS_COMUNICACAO.items():
        if canal != "whatsapp":
            continue
        for sequencia, conf in dados.get("sequencias", {}).items():
            quantidade = conf.get("artes", 0)
            if not quantidade:
                continue
            raiz = (CP.dir_campanha_material(ctx["slug"], base)
                    / f"canais-comunicacao/whatsapp/{sequencia}/artes")
            raiz.mkdir(parents=True, exist_ok=True)
            html = _interpolar_arte(CP.TEMPLATES_ARTE["whatsapp"], ctx)
            for i in range(1, quantidade + 1):
                destino = raiz / f"arte-{i:02d}.html"
                png = raiz / f"arte-{i:02d}.png"
                destino.write_text(html, encoding="utf-8")
                if com_artes:
                    try:
                        _renderizar_png(html, png, (1080, 1080))
                        geradas.append(png)
                    except Exception as exc:  # noqa: BLE001
                        print(f"[AVISO] arte nao renderizada (whatsapp/{sequencia}): {exc}")
    return geradas


# ── Cronogramas ──────────────────────────────────────────────────────────────

def _datas(hoje, dias):
    """[(dia, data_iso, dia_semana)] a partir de amanha."""
    return [(i + 1, (hoje + timedelta(days=i + 1)).isoformat(),
             SEMANAS[(hoje + timedelta(days=i + 1)).weekday()])
            for i in range(dias)]


def _itens_distribuidos(quantidade, dias):
    """Indices (1-based) espacados uniformemente na janela de dias."""
    if quantidade <= 0 or dias <= 0:
        return []
    if quantidade == 1:
        return [1]
    passo = (dias - 1) / (quantidade - 1)
    return [min(dias, 1 + round(i * passo)) for i in range(quantidade)]


def gerar_cronogramas(ctx, base):
    """Cronogramas de divulgacao com datas reais (janela do registro)."""
    gerados = []
    hoje = date.today()
    for rede, dados in CP.REDES_SOCIAIS.items():
        dias = dados.get("cronograma_dias", 14)
        roteiro = ["post" if i % 2 == 0 else
                   ("story" if rede == "instagram" else "direct")
                   for i in range(dias)]
        conteudos = {
            "post": f"Post — {ctx['titulo']}",
            "story": "Story — bastidores e dica rapida",
            "direct": "Resposta Direct — engajamento",
        }
        linhas = [f"- D+{dia} ({data}, {semana}): {conteudos[roteiro[dia - 1]]}"
                  for dia, data, semana in _datas(hoje, dias)]
        texto = (f"# Cronograma de divulgacao — {rede} — {ctx['nome']}\n\n"
                 f"> Colecao: {ctx['colecao']} · Material: {ctx['nome']} "
                 f"({ctx['tipo']}) · Janela: {dias} dias · Gerado em {hoje}\n\n"
                 + "\n".join(linhas) + "\n")
        destino = (CP.dir_campanha_material(ctx["slug"], base)
                   / f"redes-sociais/{rede}/cronograma-divulgacao"
                   / CP.cronograma_nome(rede))
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(texto, encoding="utf-8")
        gerados.append(destino)
    for canal, dados in CP.CANAIS_COMUNICACAO.items():
        for sequencia, conf in dados.get("sequencias", {}).items():
            dias = conf.get("cronograma_dias", 14)
            quantidade = conf.get("textos", 0) or conf.get("artes", 0)
            prefixo = "email" if canal == "emails" else "mensagem"
            linhas = []
            for dia, data, semana in _datas(hoje, dias):
                num = _itens_distribuidos(quantidade, dias)
                item = next((f"{prefixo}-{i:02d}-{sequencia}" for i in num
                             if i == dia), "—")
                linhas.append(f"- D+{dia} ({data}, {semana}): {item}")
            texto = (f"# Cronograma — {canal} — {sequencia} — {ctx['nome']}\n\n"
                     f"> Colecao: {ctx['colecao']} · Material: {ctx['nome']} "
                     f"({ctx['tipo']}) · Janela: {dias} dias · Gerado em {hoje}\n\n"
                     + "\n".join(linhas) + "\n")
            destino = (CP.dir_campanha_material(ctx["slug"], base)
                       / f"canais-comunicacao/{canal}/{sequencia}"
                       / "cronograma-divulgacao"
                       / CP.cronograma_nome(f"{canal}:{sequencia}", dias))
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_text(texto, encoding="utf-8")
            gerados.append(destino)
    return gerados


def copiar_templates_artes(ctx, base):
    """Copias dos HTML base nas pastas templates/ (edicao livre do design)."""
    copiados = []
    origem = CP.DIR_TEMPLATES
    for rede, dados in CP.REDES_SOCIAIS.items():
        if not dados.get("templates"):
            continue
        destino = (CP.dir_campanha_material(ctx["slug"], base)
                   / f"redes-sociais/{rede}/templates")
        destino.mkdir(parents=True, exist_ok=True)
        for nome in ("arte-post-ig.html", "arte-feed-story-ig.html",
                     "arte-post-linkedin.html", "arte-whatsapp.html"):
            fonte = origem / nome
            alvo = destino / nome
            if fonte.exists():
                alvo.write_text(fonte.read_text(encoding="utf-8"), encoding="utf-8")
                copiados.append(alvo)
    for canal, dados in CP.CANAIS_COMUNICACAO.items():
        for sequencia, conf in dados.get("sequencias", {}).items():
            if not conf.get("templates"):
                continue
            destino = (CP.dir_campanha_material(ctx["slug"], base)
                       / f"canais-comunicacao/{canal}/{sequencia}/templates")
            destino.mkdir(parents=True, exist_ok=True)
            for nome in ("arte-post-ig.html", "arte-feed-story-ig.html",
                         "arte-post-linkedin.html", "arte-whatsapp.html"):
                fonte = origem / nome
                alvo = destino / nome
                if fonte.exists():
                    alvo.write_text(fonte.read_text(encoding="utf-8"),
                                    encoding="utf-8")
                    copiados.append(alvo)
    return copiados


# ── Manifesto da campanha ────────────────────────────────────────────────────

def carregar_estado(chave, base=None):
    return CP.carregar_estado(chave, base)


def salvar_estado(chave, estado, base=None):
    return CP.salvar_estado(chave, estado, base)


def gerar_completo(chave, base=None, regenerar=False, com_artes=True):
    """Campanha de TODA a colecao: itera os membros do manifesto + campanha.json."""
    base = Path(base) if base is not None else DIR_OUTPUT
    manifesto = CP.carregar_manifesto_colecao(chave, base)
    if not manifesto:
        print(f"[ERRO] manifesto da colecao '{chave}' nao encontrado. "
              f"Rode 'python scripts/colecao.py --sincronizar' primeiro.")
        return None
    nucleo = manifesto.get("nucleo", {})
    identidade = {
        "cor_accent": manifesto.get("cor_accent"),
        "nivel": nucleo.get("senioridade", ""),
        "vocabulario": (nucleo.get("motivo_condutor", {}) or {}).get("vocabulario", []),
    }
    estado = carregar_estado(chave, base)
    materiais = {m["slug"]: m for m in estado.get("materiais", [])}
    hoje = date.today().isoformat()
    for membro in manifesto.get("membros", []):
        slug = membro["slug"]
        print(f"[campanha] material {slug} ({membro.get('tipo')})")
        try:
            resultado = gerar_material(slug, base=base, regenerar=regenerar,
                                       com_artes=com_artes)
        except Exception as exc:  # noqa: BLE001
            print(f"[ERRO] campanha de {slug}: {exc}")
            continue
        anterior = materiais.get(slug, {})
        materiais[slug] = {
            "slug": slug,
            "tipo": membro.get("tipo", ""),
            "status": anterior.get("status", "estrutura"),
            "atualizado_em": hoje,
        }
    estado = {
        "colecao": chave,
        "atualizado_em": hoje,
        "identidade": identidade,
        "materiais": sorted(materiais.values(), key=lambda m: m["slug"]),
        "total_materiais": len(materiais),
    }
    destino = salvar_estado(chave, estado, base)
    print(f"[campanha] manifesto da campanha: {destino}")
    return estado


def gerar_material(slug, base=None, regenerar=False, com_artes=True):
    """Campanha de UM material: estrutura + moldes + artes + cronogramas."""
    base = Path(base) if base is not None else DIR_OUTPUT
    dir_obra = TO.dir_obra(slug, base)
    if not (dir_obra / "config_obra.json").exists():
        print(f"[ERRO] material nao encontrado: {slug}")
        return None
    ctx = CP.contexto_material(slug, base)
    ctx["__regenerar__"] = regenerar
    raiz = CP.dir_campanha_material(slug, base)
    criadas = []
    for pasta in CP.estrutura_material(ctx):
        destino = raiz / pasta
        destino.mkdir(parents=True, exist_ok=True)
        criadas.append(destino)
    moldes = escrever_moldes(ctx, base)
    cronogramas = gerar_cronogramas(ctx, base)
    templates = copiar_templates_artes(ctx, base)
    artes = gerar_artes(ctx, base, com_artes=com_artes)
    print(f"[campanha] {raiz} — {len(criadas)} pastas, {len(moldes)} moldes, "
          f"{len(cronogramas)} cronogramas, {len(templates)} templates, "
          f"{len(artes)} artes")
    return {"raiz": raiz, "pastas": len(criadas), "moldes": len(moldes),
            "cronogramas": len(cronogramas), "artes": len(artes)}


def marcar_completa(slug, base=None):
    """Registra que a copy final de um material foi validada (--estrito)."""
    base = Path(base) if base is not None else DIR_OUTPUT
    chave = CP.chave_colecao(slug, base)
    estado = carregar_estado(chave, base)
    achou = False
    for m in estado.get("materiais", []):
        if m["slug"] == slug:
            m["status"] = "completa"
            m["atualizado_em"] = date.today().isoformat()
            achou = True
    if not achou:
        estado.setdefault("materiais", []).append({
            "slug": slug,
            "tipo": TO.tipo_por_prefixo(slug) or "",
            "status": "completa",
            "atualizado_em": date.today().isoformat(),
        })
    estado["atualizado_em"] = date.today().isoformat()
    salvar_estado(chave, estado, base)
    return achou


def listar_campanhas(base=None):
    """Colecoes com pasta campanhas/ + status por material."""
    base = Path(base) if base is not None else DIR_OUTPUT
    saida = []
    if not base.exists():
        return saida
    for colecao in sorted(p for p in base.iterdir()
                          if p.is_dir() and (p / "campanhas").exists()):
        estado = _ler_json(colecao / "campanhas" / "campanha.json", {})
        saida.append({"colecao": colecao.name,
                      "materiais": estado.get("materiais", [])})
    return saida


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    TO.console_utf8()
    ap = argparse.ArgumentParser(description="Camada CAMPANHA da colecao (V5.3)")
    alvo = ap.add_mutually_exclusive_group(required=True)
    alvo.add_argument("--material", metavar="SLUG",
                      help="slug do material (ex.: livros/obra-teste)")
    alvo.add_argument("--completo", nargs="?", const=None, metavar="COLECAO",
                      help="campanha de TODOS os materiais da colecao")
    alvo.add_argument("--listar", action="store_true",
                      help="colecoes com campanha e status dos materiais")
    ap.add_argument("--regenerar", action="store_true",
                    help="sobrescreve moldes ja editados")
    ap.add_argument("--sem-artes", action="store_true",
                    help="nao renderiza PNGs (apenas HTML fonte das artes)")
    ap.add_argument("--marcar-completa", action="store_true",
                    help="status do material -> completa (apos gate --estrito)")
    args = ap.parse_args()

    if args.listar:
        for c in listar_campanhas():
            print(f"{c['colecao']}: {len(c['materiais'])} material(ais)")
            for m in c["materiais"]:
                print(f"  {m['slug']}: {m['status']}")
        return

    if args.material:
        if args.marcar_completa:
            ok = marcar_completa(args.material)
            print(f"[campanha] {args.material} marcado como completa (ja existia: {ok})")
            return
        gerar_material(args.material, regenerar=args.regenerar,
                       com_artes=not args.sem_artes)
        return

    colecao = args.completo
    if colecao is None:
        # sem argumento: descobre a colecao pela pasta de campanhas existente
        # ou pede para informar quando houver mais de uma
        chaves = [c["colecao"] for c in listar_campanhas()]
        if len(chaves) == 1:
            colecao = chaves[0]
        elif not chaves:
            print("[ERRO] informe a colecao (nenhuma campanha existe ainda)")
            return
        else:
            print("[ERRO] informe a colecao entre: " + ", ".join(chaves))
            return
    gerar_completo(colecao, regenerar=args.regenerar,
                   com_artes=not args.sem_artes)


if __name__ == "__main__":
    main()
