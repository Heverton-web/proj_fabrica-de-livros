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
import functools
import json
import re
import shutil
import string
import sys
from datetime import date, datetime, timedelta
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
    """Variaveis comuns de interpolacao dos templates HTML de arte.

    V5.4: suporta titulo_arte (gancho curto de break scroll), apoio_arte
    (linha de apoio do envio) e rotulo_arte (progresso 'Post 3/7') como
    elementos SEPARADOS — nunca colados/cortados do titulo. 1 arte = 1 envio."""
    # Tags TECNICAS do dominio (derivadas dos capitulos/tema) primeiro; o
    # vocabulario condutor metaforico (arnes, mosquetao) fica fora das artes.
    vocab = (ctx.get("tags_arte") or ctx.get("vocabulario") or [])
    tags = "".join(f'<span class="tag">{t}</span>' for t in vocab[:4])
    if not tags:
        tags = f'<span class="tag">{ctx["colecao"]}</span>'
    # Gancho curto da arte (titulo_arte) ou titulo do material como fallback
    titulo = ctx.get("titulo_arte") or ctx.get("titulo") or ctx["colecao"]
    # Linha de apoio do envio (apoio_arte) ou subtitulo do material
    apoio = (ctx.get("apoio_arte") or ctx.get("subtitulo")
             or ctx.get("projeto_pratico") or ctx["colecao"])
    return {
        "TITULO": titulo[:70],
        "APOIO": apoio[:110],
        "ROTULO": ctx.get("rotulo_arte") or "",
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

LIMIAR_CHARS_APROVACAO = 100

STATUS_RASCUNHO = (
    "Status: RASCUNHO — reescreva a copy final com LLM (tom de divulgacao,"
    " vocabulario da colecao) antes de validar."
)
STATUS_FINAL_AUTO = (
    "Status: FINAL (auto-aprovado deterministico — tamanho, CTA+URL e"
    " vocabulario da colecao presentes, sem placeholder). Revise o tom antes"
    " de publicar; reescreva com LLM se quiser um texto mais autoral."
)


def avaliar_rascunho(ctx, corpo):
    """Heurística objetiva: True se o rascunho já atende ao gate R-CP-2 sem
    precisar de reescrita por LLM (tamanho mínimo, CTA+URL citados,
    vocabulário/título da coleção presentes, sem copy genérica/placeholder).
    Nunca aprova sozinha — é só a base para decidir o `Status` do cabeçalho;
    o operador pode sempre reescrever manualmente."""
    texto = (corpo or "").strip()
    if len(texto) < LIMIAR_CHARS_APROVACAO:
        return False
    if CP.COPY_GENERICA.search(texto):
        return False
    if "[TEXTO DO ANUNCIO]" in texto or "_(a completar)_" in texto:
        return False

    texto_lower = texto.lower()
    cta = (ctx.get("cta") or "").strip().lower()
    if cta and cta not in texto_lower:
        return False
    cta_url = ctx.get("cta_url")
    if cta_url and cta_url not in texto:
        return False

    termos_alvo = [t.lower() for t in (ctx.get("vocabulario") or []) if t]
    if ctx.get("titulo"):
        termos_alvo.append(ctx["titulo"].lower())
    if termos_alvo and not any(t in texto_lower for t in termos_alvo):
        return False
    return True


def _molde_cabecalho(ctx, formato, corpo="", extra=""):
    """Cabecalho de contexto do molde de texto. O `Status` é decidido por
    heurística objetiva (`avaliar_rascunho`) — só cai para RASCUNHO quando o
    corpo realmente precisa de reescrita por LLM."""
    vocabulario = ", ".join(ctx.get("vocabulario") or [])
    status = STATUS_FINAL_AUTO if avaliar_rascunho(ctx, corpo) else STATUS_RASCUNHO
    return (
        "<!--\n"
        "CAMPANHA {colecao} — material {nome} ({tipo})\n"
        "Formato: {formato}\n"
        "{status}\n"
        "Contexto: titulo={titulo}\n"
        "Subtítulo: {subtitulo}\n"
        "Vocabulário: {vocabulario}\n"
        "CTA: {cta} {cta_url}\n"
        "{extra}"
        "-->\n\n"
    ).format(
        colecao=ctx["colecao"], nome=ctx["nome"], tipo=ctx["tipo"],
        formato=formato, status=status, titulo=ctx["titulo"], subtitulo=ctx.get("subtitulo"),
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


def _pdf_atualizado(arquivo):
    """PDF ao lado do .md se ausente ou mais antigo que o .md (copy final)."""
    pdf = arquivo.with_suffix(".pdf")
    if not arquivo.exists():
        return None
    if not pdf.exists() or pdf.stat().st_mtime <= arquivo.stat().st_mtime:
        return compilar_markdown_pdf(arquivo)
    return pdf


def _backup_arquivo(arquivo):
    """Cria backup do arquivo antes de sobrescrever (regra contra perda de copy)."""
    if not arquivo.exists():
        return
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dir_backups = arquivo.parent / "revisao" / "backups" / ts
    dir_backups.mkdir(parents=True, exist_ok=True)
    destino = dir_backups / arquivo.name
    shutil.copy2(arquivo, destino)
    # Copiar PDF correspondente se existir
    pdf = arquivo.with_suffix(".pdf")
    if pdf.exists():
        shutil.copy2(pdf, dir_backups / pdf.name)


def escrever_moldes(ctx, base):
    """Moldes de texto para redes sociais e canais (nao sobrescreve edits).

    Cada molde .md ganha um .pdf ao lado (mesmo nome) quando escrito ou
    quando o .md foi editado depois do PDF (reflete a copy final)."""
    escritos = []
    for rede, dados in CP.REDES_SOCIAIS.items():
        raiz = CP.dir_campanha_material(ctx["slug"], base) / f"social_organico/{rede}"
        for pasta, quantidade in dados.get("textos", {}).items():
            for i in range(1, quantidade + 1):
                arquivo = raiz / CP.pasta_de_texto(pasta, None) / CP.texto_nome(pasta, i)
                escreveu = False
                if not (arquivo.exists() and not ctx.get("__regenerar__")):
                    # Backup antes de sobrescrever (GAP 1: proteção contra perda de copy)
                    if ctx.get("__regenerar__") and arquivo.exists():
                        _backup_arquivo(arquivo)
                    formato = "feed-story" if pasta == "feed-story" else pasta
                    corpo_titulo = ("# Post {i} — {titulo}\n\n" if pasta == "post"
                             else "# Story {i} — {titulo}\n\n" if pasta == "feed-story"
                             else "# Resposta Direct\n\n").format(i=i, titulo=ctx["titulo"])
                    texto_corpo = corpo_titulo + _rascunho(ctx, formato)
                    arquivo.parent.mkdir(parents=True, exist_ok=True)
                    arquivo.write_text(
                        _molde_cabecalho(ctx, f"{rede}/{pasta}", texto_corpo) + texto_corpo + "\n",
                        encoding="utf-8")
                    escreveu = True
                if arquivo.exists():
                    _pdf_atualizado(arquivo)
                if escreveu:
                    escritos.append(arquivo)
    for canal, dados in CP.CANAIS_COMUNICACAO.items():
        for sequencia, conf in dados.get("sequencias", {}).items():
            prefixo = "email" if canal == "emails" else "msg"
            quantidade = conf.get("textos", 0)
            pasta = f"inbound_emails/{sequencia}/textos" if canal == "emails" else f"canais-comunicacao/{canal}/{sequencia}/textos"
            raiz = CP.dir_campanha_material(ctx["slug"], base) / pasta
            for i in range(1, quantidade + 1):
                arquivo = raiz / CP.texto_nome(prefixo, i, sequencia)
                escreveu = False
                if not (arquivo.exists() and not ctx.get("__regenerar__")):
                    # Backup antes de sobrescrever (GAP 1: proteção contra perda de copy)
                    if ctx.get("__regenerar__") and arquivo.exists():
                        _backup_arquivo(arquivo)
                    titulo_bloco = f"# {prefixo.title()} {i} — {sequencia.replace('-', ' ')}\n\n"
                    texto_corpo = titulo_bloco + _rascunho(ctx, f"{prefixo}-{i}")
                    arquivo.parent.mkdir(parents=True, exist_ok=True)
                    arquivo.write_text(
                        _molde_cabecalho(ctx, f"{canal}/{sequencia}", texto_corpo) + texto_corpo + "\n",
                        encoding="utf-8")
                    escreveu = True
                if arquivo.exists():
                    _pdf_atualizado(arquivo)
                if escreveu:
                    escritos.append(arquivo)
                    
    # Scaffold Ads Pago
    for rede, dados in CP.ADS_PAGO.items():
        raiz = CP.dir_campanha_material(ctx["slug"], base) / f"ads_pago/{rede}"
        for pasta, quantidade in dados.get("textos", {}).items():
            for i in range(1, quantidade + 1):
                arquivo = raiz / "textos" / f"{pasta}-0{i}-{rede}.md"
                escreveu = False
                if not (arquivo.exists() and not ctx.get("__regenerar__")):
                    if ctx.get("__regenerar__") and arquivo.exists():
                        _backup_arquivo(arquivo)
                    arquivo.parent.mkdir(parents=True, exist_ok=True)
                    arquivo.write_text(f"# Anuncio {i}\n\n[TEXTO DO ANUNCIO]", encoding="utf-8")
                    escreveu = True
                if arquivo.exists():
                    _pdf_atualizado(arquivo)
                if escreveu:
                    escritos.append(arquivo)

    # Scaffold Distribuicao Semeadura
    for rede, dados in CP.DISTRIBUICAO_SEMEADURA.items():
        raiz = CP.dir_campanha_material(ctx["slug"], base) / "distribuicao_semeadura"
        for pasta, quantidade in dados.get("textos", {}).items():
            for i in range(1, quantidade + 1):
                arquivo = raiz / "textos" / f"{pasta}-0{i}-{rede}.md"
                escreveu = False
                if not (arquivo.exists() and not ctx.get("__regenerar__")):
                    if ctx.get("__regenerar__") and arquivo.exists():
                        _backup_arquivo(arquivo)
                    arquivo.parent.mkdir(parents=True, exist_ok=True)
                    arquivo.write_text(f"# Distribuicao {i}\n\n[TEXTO DA DISTRIBUICAO]", encoding="utf-8")
                    escreveu = True
                if arquivo.exists():
                    _pdf_atualizado(arquivo)
                if escreveu:
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
    """Artes PNG (post/story/arte) por material, na quantidade que SUPRE o
    cronograma da rede/canal. HTML interpolado fica ao lado como fonte
    editavel da arte.

    V5.4: cada arte usa UM gancho proprio (titulo curto de break scroll +
    apoio + rotulo de progresso) — 1 arte = 1 envio, nunca repetida."""
    geradas = []
    for rede, dados in CP.REDES_SOCIAIS.items():
        raiz = CP.dir_campanha_material(ctx["slug"], base) / f"social_organico/{rede}"
        quantidades = CP.n_artes_redes(rede)
        for formato, dim in dados.get("artes", {}).items():
            nome_template = CP.TEMPLATES_ARTE[
                "post_ig" if (rede, formato) == ("instagram", "post")
                else "post_linkedin" if rede == "linkedin"
                else "feed-story" if formato == "feed-story"
                else "post_ig"]
            prefixo = "post" if formato == "post" else "story"
            rotulo_base = "Post" if formato == "post" else "Story"
            quantidade = max(1, quantidades.get(formato, 1))
            ganchos = CP.ganchos_arte(ctx, formato, quantidade)
            for i in range(1, quantidade + 1):
                item = ganchos[i - 1]
                ctx_variado = ctx.copy()
                ctx_variado["titulo_arte"] = item["titulo"]
                ctx_variado["apoio_arte"] = item["apoio"]
                ctx_variado["rotulo_arte"] = f"{rotulo_base} {i}/{quantidade}"
                html = _interpolar_arte(nome_template, ctx_variado)
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
                        print(f"[AVISO] arte nao renderizada ({rede}/{formato}-{i:02d}): {exc}")
    for canal, dados in CP.CANAIS_COMUNICACAO.items():
        if canal != "whatsapp":
            continue
        for sequencia, conf in dados.get("sequencias", {}).items():
            quantidade = CP.n_artes_whatsapp(sequencia)
            if not quantidade:
                continue
            raiz = (CP.dir_campanha_material(ctx["slug"], base)
                    / f"canais-comunicacao/whatsapp/{sequencia}/artes")
            raiz.mkdir(parents=True, exist_ok=True)
            ganchos = CP.ganchos_arte(ctx, "whatsapp", quantidade)
            for i in range(1, quantidade + 1):
                # HTML interpolado DENTRO do loop: 1 copy por envio
                item = ganchos[i - 1]
                ctx_variado = ctx.copy()
                ctx_variado["titulo_arte"] = item["titulo"]
                ctx_variado["apoio_arte"] = item["apoio"]
                ctx_variado["rotulo_arte"] = f"Mensagem {i}/{quantidade}"
                html = _interpolar_arte(CP.TEMPLATES_ARTE["whatsapp"], ctx_variado)
                destino = raiz / f"arte-{i:02d}.html"
                png = raiz / f"arte-{i:02d}.png"
                destino.write_text(html, encoding="utf-8")
                if com_artes:
                    try:
                        _renderizar_png(html, png, (1080, 1080))
                        geradas.append(png)
                    except Exception as exc:  # noqa: BLE001
                        print(f"[AVISO] arte nao renderizada (whatsapp/{sequencia}-{i:02d}): {exc}")

    # Scaffold Ads Pago
    for rede, dados in CP.ADS_PAGO.items():
        raiz = CP.dir_campanha_material(ctx["slug"], base) / f"ads_pago/{rede}"
        for formato, dim in dados.get("artes", {}).items():
            nome_template = CP.TEMPLATES_ARTE["post_ig"]
            quantidade = 1
            ganchos = CP.ganchos_arte(ctx, formato, quantidade)
            for i in range(1, quantidade + 1):
                item = ganchos[i - 1] if ganchos else {"titulo": "Anuncio", "apoio": ""}
                ctx_variado = ctx.copy()
                ctx_variado["titulo_arte"] = item["titulo"]
                ctx_variado["apoio_arte"] = item.get("apoio", "")
                ctx_variado["rotulo_arte"] = f"Anuncio {i}"
                html = _interpolar_arte(nome_template, ctx_variado)
                destino = raiz / f"artes/{formato}"
                destino.mkdir(parents=True, exist_ok=True)
                base_html = destino / f"anuncio-{i:02d}.html"
                png = destino / f"anuncio-{i:02d}.png"
                base_html.write_text(html, encoding="utf-8")
                if com_artes:
                    try:
                        _renderizar_png(html, png, dim)
                        geradas.append(png)
                    except Exception as exc:  # noqa: BLE001
                        print(f"[AVISO] arte nao renderizada (ads/{formato}-{i:02d}): {exc}")

    return geradas


# ── Cronogramas ──────────────────────────────────────────────────────────────

@functools.lru_cache(maxsize=1)
def _binarios_pdf():
    """Pandoc/Typst: PATH primeiro; fallback WinGet (mesmos do compilar-para-pdf.py)."""
    import shutil
    pandoc = shutil.which("pandoc") or (
        r"C:\Users\trcnologia\AppData\Local\Microsoft\WinGet\Packages"
        r"\JohnMacFarlane.Pandoc_Microsoft.Winget.Source_8wekyb3d8bbwe"
        r"\pandoc-3.10\pandoc.exe")
    typst = shutil.which("typst") or (
        r"C:\Users\trcnologia\AppData\Local\Microsoft\WinGet\Packages"
        r"\Typst.Typst_Microsoft.Winget.Source_8wekyb3d8bbwe"
        r"\typst-x86_64-pc-windows-msvc\typst.exe")
    return pandoc, typst


def compilar_markdown_pdf(md_path):
    """Gera o PDF ao lado de um .md de campanha (Pandoc -> .typ -> Typst).

    Usado para cronogramas e moldes de texto: cada fonte .md ganha um .pdf de
    mesmo nome para impressao/divulgacao direta. Tolerante a falha: se
    pandoc/typst nao existirem ou a compilacao falhar, imprime aviso e devolve
    None (os gates R-CP reprovam ate o PDF existir). Usa o fluxo .typ
    intermediario do pdf_typst para evitar o bug de caminho absoluto do
    `pandoc --pdf-engine=typst` no Windows.
    """
    md_path = Path(md_path)
    pandoc, typst = _binarios_pdf()
    if not Path(pandoc).exists() or not Path(typst).exists():
        print(f"[AVISO] pandoc/typst indisponiveis — PDF de {md_path.name} nao gerado")
        return None
    try:
        from pdf_typst import executar
    except ImportError:
        print(f"[AVISO] pdf_typst nao importavel — PDF de {md_path.name} nao gerado")
        return None
    pdf_path = md_path.with_suffix(".pdf")
    comando = [pandoc, str(md_path), "-o", str(pdf_path),
               "--from", "markdown", "--to", "typst", "--standalone"]
    try:
        resultado = executar(comando, pdf_path, md_path.parent, typst, timeout=120)
    except Exception as exc:  # noqa: BLE001
        print(f"[AVISO] compilacao do .md falhou ({md_path.name}): {exc}")
        return None
    if pdf_path.exists() and pdf_path.stat().st_size > 0:
        return pdf_path
    print(f"[AVISO] PDF nao gerado para {md_path.name}: "
          f"{(resultado.stderr or '').strip()[-200:]}")
    return None


# Retrocompatibilidade: nome antigo usado por scripts/operador e testes.
compilar_cronograma_pdf = compilar_markdown_pdf


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


def _bloco_dia(quando, oque, porque, como):
    """Bloco markdown de um dia: o que / por que / como / quando."""
    return (f"**O quê:** {oque}\n\n"
            f"**Por quê:** {porque}\n\n"
            f"**Como:** {como}\n\n"
            f"**Quando:** {quando}\n")


def _bloco_pausa(data_quando):
    """Bloco de dia sem envio (pausa estrategica)."""
    return _bloco_dia(
        quando=data_quando,
        oque="Pausa estrategica — nenhum envio.",
        porque=CP.PAUSA_PORQUE,
        como=CP.como_utilizar("pausa"),
    )


def _bloco_rede(rede, dia, data, semana, formato, contadores, dias, cta):
    """Bloco rico de um dia de rede social, apontando os arquivos exatos."""
    raiz_rede = f"social_organico/{rede}"
    objetivo = CP.objetivo_do_dia(dia, dias)
    if formato == "post":
        n = contadores["post"] = contadores.get("post", 0) + 1
        arte = f"artes/post/post-{n:02d}.png"
        legenda = f"textos/post/post-{n:02d}.md"
        oque = (f"Post do {rede.title()} — arte `{raiz_rede}/{arte}` com a "
                f"legenda `{raiz_rede}/{legenda}`.")
        quando = f"D+{dia} — {data} ({semana}), as {CP.horario_utilizar(formato)}."
        return _bloco_dia(quando, oque, objetivo,
                          CP.como_utilizar(formato, arte=arte, texto=legenda, cta=cta))
    if formato == "feed-story":
        n = contadores["feed-story"] = contadores.get("feed-story", 0) + 1
        arte = f"artes/feed-story/story-{n:02d}.png"
        oque = (f"Story do Instagram — arte `{raiz_rede}/{arte}` (dica rapida, "
                f"bastidor do material).")
        quando = f"D+{dia} — {data} ({semana}), as {CP.horario_utilizar(formato)}."
        return _bloco_dia(quando, oque, objetivo,
                          CP.como_utilizar(formato, arte=arte, cta=cta))
    # direct (sem arte)
    texto_direct = "textos/resposta-direct/resposta-direct.md"
    oque = (f"Resposta Direct — use o texto `{raiz_rede}/{texto_direct}` "
            f"(engajamento pos-interacao).")
    quando = f"D+{dia} — {data} ({semana}), {CP.horario_utilizar('direct')}."
    return _bloco_dia(quando, oque, objetivo,
                      CP.como_utilizar("direct", texto=texto_direct, cta=cta))


def _bloco_canal(canal, sequencia, dia, data, semana, item, dias, cta):
    """Bloco rico de um dia de canal (email/whatsapp). item='-' = pausa."""
    raiz = f"canais-comunicacao/{canal}/{sequencia}"
    quando = f"D+{dia} — {data} ({semana}), as {CP.horario_utilizar('email' if canal == 'emails' else 'msg')}."
    if item == "-":
        return _bloco_pausa(f"— (dia de silencio, D+{dia})")
    objetivo = CP.objetivo_do_dia(dia, dias)
    rotulo = "E-mail" if canal == "emails" else "Mensagem WhatsApp"
    arquivo = f"textos/{item}.md"
    oque = f"{rotulo} — arquivo `{raiz}/{arquivo}` (pasta textos/)."
    formato = "email" if canal == "emails" else "msg"
    arte = f"artes/arte-{item.split('-')[1]}.png" if canal == "whatsapp" else None
    como = CP.como_utilizar(formato, arte=arte, texto=arquivo, cta=cta)
    return _bloco_dia(quando, oque, objetivo, como)


def _cabecalho_cronograma(titulo, ctx, dias, resumo):
    return (f"# {titulo}\n\n"
            f"> Colecao: {ctx['colecao']} · Material: {ctx['nome']} "
            f"({ctx['tipo']}) · Janela: {dias} dias · Gerado em {date.today()}\n\n"
            f"## Como usar\n\n"
            f"Cada dia indica **o quê** publicar (arquivo exato da arte/texto), "
            f"**por quê** (objetivo daquele envio no funil), **como** (passo a "
            f"passo do formato) e **quando** (data e horario). Os dias sem envio "
            f"sao pausas estrategicas: nao publique, use para interagir e preparar "
            f"o proximo envio.\n\n"
            f"**Roteiro ({dias} dias):** {resumo}\n\n"
            f"## Agenda\n")


def gerar_cronogramas(ctx, base):
    """Cronogramas ricos (o que/por que/como/quando) com datas reais.

    Cada dia vira um bloco com as 4 dimensoes de uso, apontando os arquivos
    exatos (arte PNG + texto MD). Cada cronograma sai em .md (fonte editavel)
    e .pdf (Pandoc->Typst, mesmo nome) para impressao/divulgacao direta."""
    gerados = []
    hoje = date.today()
    cta = ctx.get("cta") or "Saiba mais"
    for rede, dados in CP.REDES_SOCIAIS.items():
        dias = dados.get("cronograma_dias", 14)
        roteiro = CP.roteiro_rede(rede, dias)
        contadores = {}
        blocos = []
        for dia, data, semana in _datas(hoje, dias):
            bloco = _bloco_rede(rede, dia, data, semana, roteiro[dia - 1],
                                contadores, dias, cta)
            blocos.append(f"### D+{dia} — {semana}, {data}\n\n{bloco}")
        # Ordem fixa de formatos no resumo (post, story...) em vez de alfabetica
        n_artes = CP.n_artes_redes(rede)
        ordem = [f for f in ("post", "feed-story", "direct") if f in n_artes]
        resumo = ", ".join(f"{n_artes[f]} {f}" for f in ordem)
        texto = (_cabecalho_cronograma(
                     f"Cronograma de divulgacao — {rede} — {ctx['nome']}",
                     ctx, dias, resumo)
                 + "\n\n".join(blocos) + "\n")
        destino = (CP.dir_campanha_material(ctx["slug"], base)
                   / f"social_organico/{rede}/cronograma-divulgacao"
                   / CP.cronograma_nome(rede))
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(texto, encoding="utf-8")
        gerados.append(destino)
        pdf = compilar_markdown_pdf(destino)
        if pdf:
            gerados.append(pdf)
    for canal, dados in CP.CANAIS_COMUNICACAO.items():
        for sequencia, conf in dados.get("sequencias", {}).items():
            dias = conf.get("cronograma_dias", 14)
            quantidade = conf.get("textos", 0) or conf.get("artes", 0)
            prefixo = "email" if canal == "emails" else "msg"
            num = _itens_distribuidos(quantidade, dias)
            blocos = []
            n_envios = 0
            for dia, data, semana in _datas(hoje, dias):
                indice = next((i for i in num if i == dia), None)
                if indice is not None:
                    n_envios += 1
                    item = f"{prefixo}-{n_envios:02d}-{sequencia}"
                else:
                    item = "-"
                bloco = _bloco_canal(canal, sequencia, dia, data, semana, item,
                                     dias, cta)
                rotulo = (f"D+{dia} — {semana}, {data}" if item != "-"
                          else f"D+{dia} — {semana}, {data} — PAUSA")
                blocos.append(f"### {rotulo}\n\n{bloco}")
            resumo = f"{quantidade} envios ({prefixo}-01..{prefixo}-{quantidade:02d})"
            texto = (_cabecalho_cronograma(
                         f"Cronograma — {canal} — {sequencia} — {ctx['nome']}",
                         ctx, dias, resumo)
                     + "\n\n".join(blocos) + "\n")
            pasta = f"inbound_emails/{sequencia}" if canal == "emails" else f"canais-comunicacao/{canal}/{sequencia}"
            destino = (CP.dir_campanha_material(ctx["slug"], base)
                       / pasta
                       / "cronograma-divulgacao"
                       / CP.cronograma_nome(f"{canal}:{sequencia}", dias))
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_text(texto, encoding="utf-8")
            gerados.append(destino)
            pdf = compilar_markdown_pdf(destino)
            if pdf:
                gerados.append(pdf)
                
    # Gerar Cronograma Mestre
    destino = CP.dir_campanha_material(ctx["slug"], base) / "cronograma_mestre.md"
    if not (destino.exists() and not ctx.get("__regenerar__")):
        destino.write_text("# Cronograma Mestre\n\nTodos os envios orquestrados.", encoding="utf-8")
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
                   / f"social_organico/{rede}/templates")
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
            pasta = f"inbound_emails/{sequencia}/templates" if canal == "emails" else f"canais-comunicacao/{canal}/{sequencia}/templates"
            destino = (CP.dir_campanha_material(ctx["slug"], base) / pasta)
            destino.mkdir(parents=True, exist_ok=True)
            for nome in ("arte-post-ig.html", "arte-feed-story-ig.html",
                         "arte-post-linkedin.html", "arte-whatsapp.html"):
                fonte = origem / nome
                alvo = destino / nome
                if fonte.exists():
                    alvo.write_text(fonte.read_text(encoding="utf-8"),
                                    encoding="utf-8")
                    copiados.append(alvo)
                    
    # Templates Ads Pago
    for rede, dados in CP.ADS_PAGO.items():
        if not dados.get("templates"):
            continue
        destino = (CP.dir_campanha_material(ctx["slug"], base) / f"ads_pago/{rede}/templates")
        destino.mkdir(parents=True, exist_ok=True)
        for nome in ("arte-post-ig.html", "arte-feed-story-ig.html"):
            fonte = origem / nome
            alvo = destino / nome
            if fonte.exists():
                alvo.write_text(fonte.read_text(encoding="utf-8"), encoding="utf-8")
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
    n_cronos_md = len([c for c in cronogramas if c.suffix == ".md"])
    n_cronos_pdf = len(cronogramas) - n_cronos_md
    n_moldes_pdf = len([p for p in raiz.rglob("*.md")
                        if not p.name.startswith("cronograma-")
                        and p.with_suffix(".pdf").exists()])
    print(f"[campanha] {raiz} — {len(criadas)} pastas, {len(moldes)} moldes "
          f"(+{n_moldes_pdf} PDF), {n_cronos_md} cronogramas (+{n_cronos_pdf} PDF), "
          f"{len(templates)} templates, {len(artes)} artes")
    return {"raiz": raiz, "pastas": len(criadas), "moldes": len(moldes),
            "moldes_pdf": n_moldes_pdf,
            "cronogramas": n_cronos_md, "cronogramas_pdf": n_cronos_pdf,
            "artes": len(artes)}


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
