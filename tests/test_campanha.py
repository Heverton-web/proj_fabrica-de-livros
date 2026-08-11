"""Testes da camada CAMPANHA (V5.3): registro, gerador, gates R-CP e --completo."""

import json
import re
import shutil
from pathlib import Path

import pytest

import campanha as CP
from conftest import carregar_script

criador = carregar_script("criar-campanha.py")
gate = carregar_script("validar-campanha.py")
colecao = carregar_script("colecao.py")

COLECAO = "Colecao Teste"


def _tem_chromium():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return False
    try:
        with sync_playwright() as p:
            p.chromium.launch().close()
        return True
    except Exception:  # noqa: BLE001 — navegador nao instalado
        return False


TEM_CHROMIUM = _tem_chromium()
precisa_chromium = pytest.mark.skipif(
    not TEM_CHROMIUM, reason="Chromium do Playwright indisponivel")

TEM_PANDOC_TYPST = bool(shutil.which("pandoc") and shutil.which("typst"))
precisa_pandoc_typst = pytest.mark.skipif(
    not TEM_PANDOC_TYPST, reason="pandoc/typst indisponiveis")

MIN_PNG_BYTES = 5 * 1024


@pytest.fixture
def ambiente(livro_falso, monkeypatch):
    """output/ isolado com livro-mae + ebook derivado e manifesto da colecao."""
    raiz = livro_falso["raiz"]
    ebook = raiz / "ebooks" / "obra-teste--eb"
    ebook.mkdir(parents=True)
    (ebook / "config_obra.json").write_text(json.dumps({
        "tema": "E-book da Obra", "tipo_obra": "ebook",
        "senioridade_obra": "intermediario", "serie": COLECAO,
    }, ensure_ascii=False), encoding="utf-8")
    for mod in (CP, criador, gate):
        monkeypatch.setattr(mod, "DIR_OUTPUT", raiz, raising=False)
    monkeypatch.setattr(colecao, "DIR_OUTPUT", raiz, raising=False)
    monkeypatch.setattr(colecao, "DIR_COLECOES", raiz / "colecoes")
    import series_capa
    monkeypatch.setattr(series_capa, "DIR_OUTPUT", raiz, raising=False)
    monkeypatch.setattr(series_capa, "CAMINHO_REGISTRO", raiz / "series.json")

    # Compilacao PDF deterministica nos testes: placeholder %PDF ao lado do .md
    # (os gates R-CP so exigem a existencia do arquivo).
    def _pdf_placeholder(md_path):
        pdf = md_path.with_suffix(".pdf")
        pdf.write_bytes(b"%PDF-1.4\nplaceholder\n%%EOF")
        return pdf

    monkeypatch.setattr(criador, "compilar_markdown_pdf", _pdf_placeholder)
    monkeypatch.setattr(criador, "compilar_cronograma_pdf", _pdf_placeholder)

    # Renderizacao PNG deterministica sem Chromium: o PNG deriva do conteudo
    # do HTML (hash), entao artes com copy diferente geram PNGs diferentes —
    # habilita os testes de unicidade (1 arte = 1 envio) e continua valido
    # para R-CP-3 (assinatura + tamanho + contagem).
    def _png_placeholder(html, png_path, dim):
        import hashlib
        png_path = Path(png_path)
        png_path.parent.mkdir(parents=True, exist_ok=True)
        digest = hashlib.sha256(html.encode("utf-8")).digest()
        corpo = b"\x89PNG\r\n\x1a\n" + digest * (MIN_PNG_BYTES // 32)
        png_path.write_bytes(corpo[:MIN_PNG_BYTES])
        return png_path

    livro_falso["_renderizar_png_real"] = criador._renderizar_png
    monkeypatch.setattr(criador, "_renderizar_png", _png_placeholder)

    colecao.sincronizar()
    return livro_falso


def _finalizar_moldes(slug, base=None):
    """Simula a reescrita do agente: marca todos os moldes como FINAL."""
    raiz = CP.dir_campanha_material(slug, base)
    for arquivo in raiz.rglob("*.md"):
        texto = arquivo.read_text(encoding="utf-8")
        arquivo.write_text(texto.replace("Status: RASCUNHO", "Status: FINAL"),
                           encoding="utf-8")


def _raiz(slug, base=None):
    return CP.dir_campanha_material(slug, base)


# ── Registro ─────────────────────────────────────────────────────────────────

class TestRegistro:
    def test_estrutura_de_pastas_do_registro(self, ambiente):
        ctx = CP.contexto_material(ambiente["slug"])
        pastas = CP.estrutura_material(ctx)
        # Novo Scaffold Baseado no Playbook
        assert "social_organico/instagram/artes/post" in pastas
        assert "social_organico/linkedin/artes/post" in pastas
        assert "social_organico/instagram/textos/resposta-direct" in pastas
        assert "inbound_emails/sequencia-nutricao/textos" in pastas
        assert "ads_pago/facebook/artes/anuncio" in pastas
        assert "distribuicao_semeadura/textos/artigo" in pastas

    def test_dimensoes_de_artes(self):
        assert CP.REDES_SOCIAIS["instagram"]["artes"]["post"] == (1080, 1350)
        assert CP.REDES_SOCIAIS["instagram"]["artes"]["feed-story"] == (1080, 1920)
        assert CP.REDES_SOCIAIS["linkedin"]["artes"]["post"] == (1200, 628)

    def test_texto_nome_por_pasta(self):
        assert CP.texto_nome("post", 1) == "post-01.md"
        assert CP.texto_nome("feed-story", 2) == "story-02.md"
        assert CP.texto_nome("resposta-direct", 1) == "resposta-direct.md"
        assert CP.texto_nome("email", 3, "sequencia-mkt") == "email-03-sequencia-mkt.md"
        assert CP.texto_nome("msg", 4, "sequencia-divulgacao") == "msg-04-sequencia-divulgacao.md"

    def test_nome_material_pega_ultimo_segmento(self, monkeypatch):
        # isola do disco: nome_material consulta a chave da colecao
        monkeypatch.setattr(CP, "chave_colecao",
                            lambda slug, base=None: "Colecao Teste")
        assert CP.nome_material("livros/obra-teste") == "obra-teste"
        # V5.1: nome_material limita a 20 chars para evitar caminhos longos
        assert CP.nome_material("ebooks/obra-teste--eb") == "obra-teste"

    def test_nome_material_desambiguado_da_colecao(self, monkeypatch):
        """Derivados com prefixo do slug da colecao nao colidem com o raiz.

        Bug real: 'spec-driven-development--eb-01-...' cortava para
        'spec-driven' (mesma pasta de campanha do livro)."""
        monkeypatch.setattr(CP, "chave_colecao",
                            lambda slug, base=None: "spec-driven-development")
        assert CP.nome_material(
            "spec-driven-development/livros/spec-driven-development") == "spec-driven"
        assert CP.nome_material(
            "spec-driven-development/ebooks/spec-driven-development--eb-01-a-planta-baixa-fundamentos") == "eb-01"
        assert CP.nome_material(
            "spec-driven-development/ebooks/spec-driven-development--eb-02-o-canteiro-de-obras-o-projeto-do-inicio") == "eb-02"
        nomes = [
            CP.nome_material("spec-driven-development/livros/spec-driven-development"),
            CP.nome_material("spec-driven-development/ebooks/spec-driven-development--eb-01-a-planta-baixa-fundamentos"),
            CP.nome_material("spec-driven-development/ebooks/spec-driven-development--eb-02-o-canteiro-de-obras-o-projeto-do-inicio"),
        ]
        assert len(set(nomes)) == 3, f"colisao de nomes: {nomes}"


# ── Gerador ──────────────────────────────────────────────────────────────────

class TestGerador:
    def test_gera_estrutura_moldes_e_cronogramas(self, ambiente):
        rel = criador.gerar_material(ambiente["slug"], com_artes=False)
        raiz = _raiz(ambiente["slug"])
        for pasta in CP.estrutura_material(CP.contexto_material(ambiente["slug"])):
            assert (raiz / pasta).is_dir(), pasta
        assert (raiz / "social_organico/instagram/textos/post/post-01.md").exists()
        assert (raiz / "social_organico/instagram/textos/resposta-direct/resposta-direct.md").exists()
        assert (raiz / "social_organico/linkedin/textos/post/post-02.md").exists()
        assert (raiz / "inbound_emails/sequencia-nutricao/textos/email-01-sequencia-nutricao.md").exists()
        assert (raiz / "inbound_emails/sequencia-mkt/textos/email-03-sequencia-mkt.md").exists()
        assert (raiz / "ads_pago/facebook/textos/anuncio-01-facebook.md").exists()
        assert (raiz / "cronograma_mestre.md").exists()
        assert not list(raiz.rglob("*.png"))

    def test_moldes_tem_contexto_e_rascunho(self, ambiente):
        criador.gerar_material(ambiente["slug"], com_artes=False)
        molde = (_raiz(ambiente["slug"])
                 / "social_organico/instagram/textos/post/post-01.md")
        texto = molde.read_text(encoding="utf-8")
        assert "Status: RASCUNHO" in texto
        assert "Colecao Teste" in texto
        assert "fundação" in texto  # vocabulario condutor no rascunho
        assert "A Obra em Construção" in texto

    def test_moldes_nao_sobrescrevem_edits(self, ambiente):
        criador.gerar_material(ambiente["slug"], com_artes=False)
        alvo = (_raiz(ambiente["slug"])
                / "social_organico/instagram/textos/post/post-01.md")
        alvo.write_text("Status: FINAL — copy final do agente", encoding="utf-8")
        criador.gerar_material(ambiente["slug"], com_artes=False)
        assert "copy final do agente" in alvo.read_text(encoding="utf-8")
        criador.gerar_material(ambiente["slug"], com_artes=False, regenerar=True)
        assert "Status: RASCUNHO" in alvo.read_text(encoding="utf-8")

    def test_artes_escrevem_html_fonte_sem_chromium(self, ambiente):
        criador.gerar_material(ambiente["slug"], com_artes=False)
        raiz = _raiz(ambiente["slug"])
        html = (raiz / "social_organico/instagram/artes/post/post-01.html") \
            .read_text(encoding="utf-8")
        ctx = CP.contexto_material(ambiente["slug"])
        assert ctx["cor_accent"].lstrip("#") in html
        # gancho curto do capitulo 1 + rotulo de progresso da sequencia
        assert "Fundação do Projeto" in html
        assert "Post 1/7" in html
        # tags TECNICAS (pilares do dominio), nao o vocabulario metaforico
        assert any(t in html for t in ("Contrato", "Schema", "Modelo", "Índice"))

    def test_tags_arte_sao_tecnicas_nao_metafora(self, ambiente):
        criador.gerar_material(ambiente["slug"], com_artes=False)
        html = (_raiz(ambiente["slug"])
                / "social_organico/instagram/artes/post/post-01.html") \
            .read_text(encoding="utf-8")
        # vocabulario condutor (metafora: fundacao/estrutura/acabamento) NAO
        # aparece como tag na arte — so as tags tecnicas do dominio
        for metafora in ("fundação", "estrutura", "acabamento"):
            assert metafora not in html, f"metafora {metafora} na arte"

    def test_derivar_tags_arte_usa_glossario_tecnico(self):
        sumario = {
            "titulo_obra": "Harness Engineering — Do Modelo ao Sistema Autônomo",
            "partes": [{"parte": "I", "titulo_parte": "Base", "capitulos": [
                {"capitulo": "1", "titulo": "O que um agente realmente é",
                 "pilares_previstos": ["Harness", "Guardrails", "Produção"]},
            ]}],
        }
        config = {"tema": "Harness Engineering"}
        tags = CP.derivar_tags_arte(sumario, config)
        assert tags, "deveria derivar tags tecnicas"
        assert all(t.lower() in CP.TAGS_TECNICAS for t in tags)
        # nenhuma palavra da metafora condutora
        assert not any(t.lower() in ("arnês", "mosquetão", "corda", "cume")
                       for t in tags)
        # sem redundancia de substring (sistema autonomo nao gera 'sistema')
        baixas = [t.lower() for t in tags]
        assert len(set(baixas)) == len(baixas)

    def test_derivar_tags_arte_vazio_faz_fallback_vocabulario(self, ambiente):
        # material sem termos do glossario -> tags_arte vazio -> gerador usa
        # o vocabulario condutor (comportamento antigo, nunca quebra)
        sumario = {"titulo_obra": "Tema sem palavras tecnicas reconhecidas"}
        assert CP.derivar_tags_arte(sumario, {"tema": ""}) == []
        # e o varivel de arte ainda emite tags (fallback)
        ctx = CP.contexto_material(ambiente["slug"])
        variaveis = criador.variaveis_arte(ctx)
        assert variaveis["TAGS"]

    def test_artes_templates_copiados(self, ambiente):
        criador.gerar_material(ambiente["slug"], com_artes=False)
        raiz = _raiz(ambiente["slug"])
        assert (raiz / "social_organico/instagram/templates/arte-post-ig.html").exists()
        assert (raiz / "inbound_emails/sequencia-nutricao/templates/arte-whatsapp.html").exists()

    def test_cronograma_tem_datas_futuras(self, ambiente):
        criador.gerar_material(ambiente["slug"], com_artes=False)
        crono = (_raiz(ambiente["slug"])
                 / "social_organico/instagram/cronograma-divulgacao/cronograma-ig.md")
        texto = crono.read_text(encoding="utf-8")
        import re
        from datetime import date, datetime
        datas = [date.fromisoformat(m) for m in re.findall(r"\d{4}-\d{2}-\d{2}", texto)]
        assert len(datas) >= 14
        assert all(d >= date.today() for d in datas)

    def test_cronograma_tem_quatro_dimensoes_de_uso(self, ambiente):
        criador.gerar_material(ambiente["slug"], com_artes=False)
        raiz = _raiz(ambiente["slug"])
        cronos = list(raiz.rglob("cronograma-*.md"))
        assert cronos, "nenhum cronograma gerado"
        for crono in cronos:
            texto = crono.read_text(encoding="utf-8")
            for dim in ("**O quê:**", "**Por quê:**", "**Como:**", "**Quando:**"):
                assert dim in texto, f"{crono.name} sem {dim}"
            # O 'o quê' aponta arquivos concretos (arte/texto)
            assert "artes/" in texto or "textos/" in texto, crono.name

    def test_cronograma_alterna_envio_e_pausa_nos_canais(self, ambiente):
        criador.gerar_material(ambiente["slug"], com_artes=False)
        crono = (_raiz(ambiente["slug"])
                 / "inbound_emails/sequencia-nutricao"
                 / "cronograma-divulgacao"
                 / "cronograma-30d-emails-sequencia-nutricao.md")
        texto = crono.read_text(encoding="utf-8")
        assert texto.count("**O quê:**") == 30  # um bloco por dia
        assert "PAUSA" in texto  # dias de silencio rotulados
        assert "email-01-sequencia-nutricao.md" in texto
        assert "email-04-sequencia-nutricao.md" in texto

    def test_cronograma_gera_pdf_ao_lado(self, ambiente):
        criador.gerar_material(ambiente["slug"], com_artes=False)
        raiz = _raiz(ambiente["slug"])
        for crono in raiz.rglob("cronograma-*.md"):
            pdf = crono.with_suffix(".pdf")
            assert pdf.exists(), pdf
            assert pdf.read_bytes().startswith(b"%PDF")
        assert (raiz / "social_organico/instagram/cronograma-divulgacao/cronograma-ig.pdf").exists()
        assert (raiz / "inbound_emails/sequencia-nutricao"
                / "cronograma-divulgacao"
                / "cronograma-30d-emails-sequencia-nutricao.pdf").exists()

    def test_textos_geram_pdf_ao_lado(self, ambiente):
        criador.gerar_material(ambiente["slug"], com_artes=False)
        raiz = _raiz(ambiente["slug"])
        for texto in raiz.rglob("*.md"):
            if texto.name.startswith("cronograma"):
                continue
            pdf = texto.with_suffix(".pdf")
            assert pdf.exists(), pdf
            assert pdf.read_bytes().startswith(b"%PDF")
        assert (raiz / "social_organico/instagram/textos/post/post-01.pdf").exists()
        assert (raiz / "social_organico/instagram/textos/feed-story/story-01.pdf").exists()
        assert (raiz / "social_organico/linkedin/textos/post/post-02.pdf").exists()
        assert (raiz / "social_organico/instagram/textos/resposta-direct/resposta-direct.pdf").exists()
        assert (raiz / "inbound_emails/sequencia-nutricao/textos"
                / "email-01-sequencia-nutricao.pdf").exists()
        assert (raiz / "canais-comunicacao/whatsapp/sequencia-divulgacao/textos"
                / "msg-06-sequencia-divulgacao.pdf").exists()

    @precisa_pandoc_typst
    def test_cronograma_pdf_real_compila(self, tmp_path):
        """Com pandoc/typst instalados, a funcao real gera um PDF valido."""
        crono = tmp_path / "cronograma-ig.md"
        crono.write_text("# Cronograma\n\n- D+1 (2026-08-10, segunda-feira): Post\n",
                         encoding="utf-8")
        pdf = criador.compilar_cronograma_pdf(crono)
        assert pdf is not None
        assert pdf.exists() and pdf.stat().st_size > 100
        assert pdf.read_bytes().startswith(b"%PDF")

    @precisa_chromium
    def test_artes_renderizam_png_reais(self, ambiente):
        """Chromium real renderiza PNGs na quantidade do cronograma."""
        real = ambiente["_renderizar_png_real"]
        original = criador._renderizar_png
        criador._renderizar_png = real
        try:
            criador.gerar_material(ambiente["slug"], com_artes=True)
        finally:
            criador._renderizar_png = original
        raiz = _raiz(ambiente["slug"])
        png = raiz / "social_organico/instagram/artes/post/post-01.png"
        assert png.exists()
        assert png.read_bytes().startswith(b"\x89PNG")
        assert (raiz / "social_organico/instagram/artes/post/post-07.png").exists()
        assert (raiz / "social_organico/instagram/artes/feed-story/story-07.png").exists()
        assert (raiz / "social_organico/linkedin/artes/post/post-07.png").exists()
        assert (raiz / "canais-comunicacao/whatsapp/sequencia-nutricao/artes/arte-04.png").exists()

    def test_artes_quantidade_supre_cronograma(self, ambiente):
        criador.gerar_material(ambiente["slug"], com_artes=True)
        raiz = _raiz(ambiente["slug"])
        # Instagram 14 dias: 7 posts + 7 stories
        assert (raiz / "social_organico/instagram/artes/post/post-01.png").exists()
        assert (raiz / "social_organico/instagram/artes/post/post-07.png").exists()
        assert (raiz / "social_organico/instagram/artes/feed-story/story-01.png").exists()
        assert (raiz / "social_organico/instagram/artes/feed-story/story-07.png").exists()
        assert not (raiz / "social_organico/instagram/artes/post/post-08.png").exists()
        # LinkedIn 14 dias: 7 posts (direct e texto, sem arte)
        assert (raiz / "social_organico/linkedin/artes/post/post-07.png").exists()
        assert not (raiz / "social_organico/linkedin/artes/post/post-08.png").exists()
        # WhatsApp: 1 arte por mensagem da sequencia (4 e 6)
        assert (raiz / "canais-comunicacao/whatsapp/sequencia-nutricao/artes/arte-04.png").exists()
        assert not (raiz / "canais-comunicacao/whatsapp/sequencia-nutricao/artes/arte-05.png").exists()
        assert (raiz / "canais-comunicacao/whatsapp/sequencia-divulgacao/artes/arte-06.png").exists()

    def test_artes_png_unicos_por_formato(self, ambiente):
        """1 arte = 1 envio: nenhum PNG repetido dentro de um formato/sequencia.

        A fixture deriva o PNG do conteudo do HTML, entao hashes iguais
        provariam copy repetida (o bug original)."""
        import hashlib
        criador.gerar_material(ambiente["slug"], com_artes=True)
        raiz = _raiz(ambiente["slug"])
        grupos = [
            "social_organico/instagram/artes/post",
            "social_organico/instagram/artes/feed-story",
            "social_organico/linkedin/artes/post",
            "canais-comunicacao/whatsapp/sequencia-nutricao/artes",
            "canais-comunicacao/whatsapp/sequencia-divulgacao/artes",
        ]
        for grupo in grupos:
            pngs = sorted((raiz / grupo).glob("*.png"))
            assert len(pngs) >= 2, grupo
            hashes = {hashlib.md5(p.read_bytes()).hexdigest() for p in pngs}
            assert len(hashes) == len(pngs), \
                f"artes repetidas em {grupo}: {len(hashes)}/{len(pngs)} unicas"

    def test_artes_html_fonte_distintos_e_titulo_curto(self, ambiente):
        """Cada arte tem gancho proprio <= MAX_GANCHO + rotulo de progresso."""
        criador.gerar_material(ambiente["slug"], com_artes=False)
        raiz = _raiz(ambiente["slug"])
        dir_post = raiz / "social_organico/instagram/artes/post"
        titulos = set()
        for html in sorted(dir_post.glob("post-*.html")):
            texto = html.read_text(encoding="utf-8")
            assert f"Post {int(html.stem.split('-')[1])}/7" in texto, html.name
            # titulo da arte (bloco <h1 ...>) tem gancho curto
            m = re.search(r"<h1 class=\"titulo\">([^<]+)</h1>", texto)
            assert m, html.name
            assert len(m.group(1)) <= CP.MAX_GANCHO, html.name
            titulos.add(m.group(1))
        assert len(titulos) == 7, f"7 ganchos distintos esperados, veio {titulos}"

    def test_artes_whatsapp_interpola_html_dentro_do_loop(self, ambiente):
        """Bug original: HTML interpolado 1x fora do loop -> artes identicas."""
        criador.gerar_material(ambiente["slug"], com_artes=False)
        raiz = _raiz(ambiente["slug"])
        dir_artes = raiz / "canais-comunicacao/whatsapp/sequencia-divulgacao/artes"
        textos = {html.read_text(encoding="utf-8")
                  for html in dir_artes.glob("arte-*.html")}
        assert len(textos) == 6, f"6 copies distintas esperadas, veio {len(textos)}"
        # rotulo de progresso presente e distinto em cada envio
        rotulos = set()
        for html in dir_artes.glob("arte-*.html"):
            m = re.search(r"Mensagem (\d/\d)", html.read_text(encoding="utf-8"))
            assert m
            rotulos.add(m.group(1))
        assert rotulos == {"1/6", "2/6", "3/6", "4/6", "5/6", "6/6"}

    def test_reprova_artes_insuficientes_para_cronograma(self, ambiente):
        criador.gerar_material(ambiente["slug"], com_artes=True)
        # Deleta posts do IG para ficar abaixo do exigido pelo cronograma
        raiz = _raiz(ambiente["slug"])
        dir_post = raiz / "social_organico/instagram/artes/post"
        for png in list(dir_post.glob("post-*.png")):
            if png.name != "post-01.png":
                png.unlink()
        rel = gate.validar_material(ambiente["slug"])
        assert "R-CP-3" in {v["regra"] for v in rel["violacoes"]}
        assert any("1/7 artes" in v["detalhe"] for v in rel["violacoes"])

    def test_reprova_artes_insuficientes_whatsapp(self, ambiente):
        criador.gerar_material(ambiente["slug"], com_artes=True)
        raiz = _raiz(ambiente["slug"])
        dir_artes = raiz / "canais-comunicacao/whatsapp/sequencia-nutricao/artes"
        for png in list(dir_artes.glob("arte-*.png")):
            if png.name != "arte-01.png":
                png.unlink()
        rel = gate.validar_material(ambiente["slug"])
        assert "R-CP-3" in {v["regra"] for v in rel["violacoes"]}
        assert any("1/4 artes" in v["detalhe"] for v in rel["violacoes"])

    def test_material_inexistente_devolve_none(self, ambiente):
        assert criador.gerar_material("livros/nao-existe") is None


# ── Ganchos de arte (1 arte = 1 envio) ───────────────────────────────────────

class TestGanchosArte:
    def test_devolve_n_itens_com_titulo_curto(self, ambiente):
        ctx = CP.contexto_material(ambiente["slug"])
        itens = CP.ganchos_arte(ctx, "post", 7)
        assert len(itens) == 7
        for item in itens:
            assert item["titulo"], "gancho vazio"
            assert item["apoio"], "apoio vazio"
            assert len(item["titulo"]) <= CP.MAX_GANCHO
            assert len(item["apoio"]) <= CP.MAX_APOIO

    def test_post_prioriza_capitulos_do_sumario(self, ambiente):
        ctx = CP.contexto_material(ambiente["slug"])
        itens = CP.ganchos_arte(ctx, "post", 4)
        titulos = [i["titulo"] for i in itens]
        assert "Fundação do Projeto" in titulos
        assert "Teoria Pura" in titulos
        # objetivos dos capitulos entram como fonte extra (variedade)
        assert "Estabelecer os contratos que sustentam o sistema" in titulos

    def test_story_prioriza_pilares(self, ambiente):
        ctx = CP.contexto_material(ambiente["slug"])
        itens = CP.ganchos_arte(ctx, "feed-story", 4)
        titulos = [i["titulo"] for i in itens]
        # pilares da fixture: Contrato, Schema, Índice, Modelo
        assert any(t in ("Contrato", "Schema", "Índice", "Modelo") for t in titulos)

    def test_unicos_quando_fonte_suficiente(self, ambiente):
        # fonte = capitulos + pilares (6) > n=5 -> todos distintos
        ctx = CP.contexto_material(ambiente["slug"])
        itens = CP.ganchos_arte(ctx, "post", 5)
        titulos = [i["titulo"] for i in itens]
        assert len(set(titulos)) == len(titulos)

    def test_cicla_sem_quebrar_quando_n_maior_que_fonte(self, ambiente):
        ctx = CP.contexto_material(ambiente["slug"])
        itens = CP.ganchos_arte(ctx, "post", 20)
        assert len(itens) == 20
        assert all(i["titulo"] and i["apoio"] for i in itens)

    def test_fallback_com_tema_quando_sem_sumario(self, ambiente):
        sumario = ambiente["dir_livro"] / "sumario_macro.json"
        backup = sumario.with_suffix(".json.bak")
        sumario.rename(backup)
        try:
            ctx = CP.contexto_material(ambiente["slug"])
            itens = CP.ganchos_arte(ctx, "whatsapp", 4)
            assert len(itens) == 4
            assert any("método" in i["titulo"] or "aposta" in i["titulo"]
                       for i in itens)
        finally:
            backup.rename(sumario)

    def test_mesmo_formato_gera_ganchos_iguais_deterministicos(self, ambiente):
        ctx = CP.contexto_material(ambiente["slug"])
        a = CP.ganchos_arte(ctx, "post", 5)
        b = CP.ganchos_arte(ctx, "post", 5)
        assert a == b


# ── Gate ─────────────────────────────────────────────────────────────────────

class TestGate:
    def test_reprova_molde_rascunho_pendente(self, ambiente):
        criador.gerar_material(ambiente["slug"], com_artes=False)
        rel = gate.validar_material(ambiente["slug"])
        assert not rel["conforme"]
        assert "R-CP-2" in {v["regra"] for v in rel["violacoes"]}

    def test_aprova_copy_final(self, ambiente):
        criador.gerar_material(ambiente["slug"], com_artes=True)
        _finalizar_moldes(ambiente["slug"])
        rel = gate.validar_material(ambiente["slug"], estrito=True)
        assert rel["conforme"], rel["violacoes"]

    def test_reprova_copy_generica(self, ambiente):
        criador.gerar_material(ambiente["slug"], com_artes=False)
        alvo = (_raiz(ambiente["slug"])
                / "social_organico/instagram/textos/post/post-01.md")
        alvo.write_text("Status: FINAL\n\nAutor Digital: o guia para centenas de pessoas",
                        encoding="utf-8")
        _finalizar_moldes(ambiente["slug"])
        rel = gate.validar_material(ambiente["slug"])
        assert any(v["regra"] == "R-CP-2" and "generica" in v["detalhe"]
                   for v in rel["violacoes"])

    def test_reprova_pasta_ausente(self, ambiente):
        criador.gerar_material(ambiente["slug"], com_artes=False)
        import shutil
        ausente = _raiz(ambiente["slug"]) / "social_organico/linkedin"
        shutil.rmtree(ausente)
        rel = gate.validar_material(ambiente["slug"])
        assert "R-CP-1" in {v["regra"] for v in rel["violacoes"]}

    def test_reprova_vocabulario_ausente_no_estrito(self, ambiente):
        criador.gerar_material(ambiente["slug"], com_artes=True)
        raiz = _raiz(ambiente["slug"])
        # Mantem cronogramas (R-CP-5) e apaga so os moldes de texto
        for md in list(raiz.rglob("*.md")):
            if md.name.startswith("cronograma-"):
                continue
            md.unlink()
        (raiz / "social_organico/instagram/textos/post").mkdir(parents=True, exist_ok=True)
        texto = raiz / "social_organico/instagram/textos/post/post-01.md"
        texto.write_text("Status: FINAL\n\nCopy sem termos da colecao.",
                         encoding="utf-8")
        texto.with_suffix(".pdf").write_bytes(b"%PDF-1.4\nplaceholder\n%%EOF")
        rel = gate.validar_material(ambiente["slug"], estrito=True)
        assert "R-CP-4" in {v["regra"] for v in rel["violacoes"]}
        rel_sem_estrito = gate.validar_material(ambiente["slug"])
        assert rel_sem_estrito["conforme"]

    def test_reprova_png_invalido(self, ambiente):
        criador.gerar_material(ambiente["slug"], com_artes=False)
        png = (_raiz(ambiente["slug"])
               / "social_organico/instagram/artes/post/post-01.png")
        png.write_bytes(b"lixo nao png")
        rel = gate.validar_material(ambiente["slug"])
        assert "R-CP-3" in {v["regra"] for v in rel["violacoes"]}

    def test_aprova_artes_unicas_no_cp6(self, ambiente):
        """Copy por envio: gerador emite artes unicas e R-CP-6 nao acusa."""
        criador.gerar_material(ambiente["slug"], com_artes=True)
        _finalizar_moldes(ambiente["slug"])
        rel = gate.validar_material(ambiente["slug"])
        assert "R-CP-6" not in {v["regra"] for v in rel["violacoes"]}, \
            rel["violacoes"]

    def test_reprova_pngs_repetidos_no_cp6(self, ambiente):
        """Mesma imagem em 2 envios (bug original) -> R-CP-6 reprova."""
        import shutil
        criador.gerar_material(ambiente["slug"], com_artes=True)
        raiz = _raiz(ambiente["slug"])
        dir_post = raiz / "social_organico/instagram/artes/post"
        shutil.copy2(dir_post / "post-01.png", dir_post / "post-02.png")
        rel = gate.validar_material(ambiente["slug"])
        violacoes = [v for v in rel["violacoes"] if v["regra"] == "R-CP-6"]
        assert any("PNGs repetidos" in v["detalhe"] and "post-02.png" in v["detalhe"]
                   for v in violacoes)

    def test_reprova_html_fonte_repetido_no_cp6(self, ambiente):
        """Copy identica em 2 envios -> R-CP-6 reprova o HTML fonte."""
        criador.gerar_material(ambiente["slug"], com_artes=True)
        raiz = _raiz(ambiente["slug"])
        dir_post = raiz / "social_organico/instagram/artes/post"
        html1 = (dir_post / "post-01.html").read_text(encoding="utf-8")
        (dir_post / "post-02.html").write_text(html1, encoding="utf-8")
        rel = gate.validar_material(ambiente["slug"])
        violacoes = [v for v in rel["violacoes"] if v["regra"] == "R-CP-6"]
        assert any("HTML fonte repetido" in v["detalhe"] and "post-02.html" in v["detalhe"]
                   for v in violacoes)

    def test_backup_rascunho_em_revisao_nao_reprova(self, ambiente):
        """revisao/backups guarda moldes RASCUNHO antigos (--regenerar);
        sao infra, nao copy de campanha — nao podem reprovar R-CP-2/R-CP-C1."""
        criador.gerar_material(ambiente["slug"], com_artes=True)
        _finalizar_moldes(ambiente["slug"])
        backup = (_raiz(ambiente["slug"]) / "revisao/backups/20260810_000000"
                  / "social_organico/instagram/textos/post/post-01.md")
        backup.parent.mkdir(parents=True, exist_ok=True)
        backup.write_text("Status: RASCUNHO — molde antigo de backup", encoding="utf-8")
        rel = gate.validar_material(ambiente["slug"], estrito=True)
        assert rel["conforme"], rel["violacoes"]

    def test_reprova_cronograma_sem_data(self, ambiente):
        criador.gerar_material(ambiente["slug"], com_artes=False)
        crono = (_raiz(ambiente["slug"])
                 / "social_organico/instagram/cronograma-divulgacao/cronograma-ig.md")
        crono.write_text("sem data aqui", encoding="utf-8")
        rel = gate.validar_material(ambiente["slug"])
        assert "R-CP-5" in {v["regra"] for v in rel["violacoes"]}

    def test_reprova_cronograma_sem_dimensoes(self, ambiente):
        criador.gerar_material(ambiente["slug"], com_artes=False)
        crono = (_raiz(ambiente["slug"])
                 / "social_organico/instagram/cronograma-divulgacao/cronograma-ig.md")
        crono.write_text("- D+1 (2026-08-10, segunda-feira): Post — titulo\n",
                         encoding="utf-8")
        rel = gate.validar_material(ambiente["slug"])
        assert "R-CP-5" in {v["regra"] for v in rel["violacoes"]}
        assert any("O quê" in v["detalhe"] for v in rel["violacoes"])

    def test_reprova_cronograma_sem_pdf(self, ambiente):
        criador.gerar_material(ambiente["slug"], com_artes=False)
        pdf = (_raiz(ambiente["slug"])
               / "social_organico/instagram/cronograma-divulgacao/cronograma-ig.pdf")
        pdf.unlink()
        rel = gate.validar_material(ambiente["slug"])
        assert "R-CP-5" in {v["regra"] for v in rel["violacoes"]}
        assert any("sem PDF" in v["detalhe"] for v in rel["violacoes"])

    def test_reprova_texto_sem_pdf(self, ambiente):
        criador.gerar_material(ambiente["slug"], com_artes=False)
        pdf = (_raiz(ambiente["slug"])
               / "social_organico/instagram/textos/post/post-01.pdf")
        pdf.unlink()
        rel = gate.validar_material(ambiente["slug"])
        assert "R-CP-2" in {v["regra"] for v in rel["violacoes"]}
        assert any("sem PDF" in v["detalhe"] for v in rel["violacoes"])


# ── Completo (colecao inteira) ───────────────────────────────────────────────

class TestCompleto:
    def test_completo_gera_campanha_json_para_todos(self, ambiente):
        estado = criador.gerar_completo(COLECAO, com_artes=False)
        assert estado["colecao"] == COLECAO
        assert estado["total_materiais"] == 2
        slugs = {m["slug"] for m in estado["materiais"]}
        assert slugs == {"livros/obra-teste", "ebooks/obra-teste--eb"}
        assert all(m["status"] == "estrutura" for m in estado["materiais"])
        manifesto = CP.carregar_estado(COLECAO)
        assert manifesto["identidade"]["nivel"] == "intermediario"

    def test_completo_gate_rcp_c1(self, ambiente):
        criador.gerar_completo(COLECAO, com_artes=True)
        rel = gate.validar_completo(COLECAO)
        assert not rel["conforme"]
        assert "R-CP-C1" in {v["regra"] for v in rel["violacoes"]}
        for m in ("livros/obra-teste", "ebooks/obra-teste--eb"):
            _finalizar_moldes(m)
            criador.marcar_completa(m)
        rel = gate.validar_completo(COLECAO, estrito=True)
        assert rel["conforme"], rel["violacoes"]

    def test_marcar_completa_atualiza_status(self, ambiente):
        criador.gerar_completo(COLECAO, com_artes=False)
        criador.marcar_completa("livros/obra-teste")
        estado = CP.carregar_estado(COLECAO)
        por_slug = {m["slug"]: m for m in estado["materiais"]}
        assert por_slug["livros/obra-teste"]["status"] == "completa"
        assert por_slug["ebooks/obra-teste--eb"]["status"] == "estrutura"

    def test_listar_campanhas(self, ambiente):
        assert criador.listar_campanhas() == []
        criador.gerar_completo(COLECAO, com_artes=False)
        listados = criador.listar_campanhas()
        assert len(listados) == 1
        assert listados[0]["colecao"] == COLECAO
        assert len(listados[0]["materiais"]) == 2

    def test_contexto_material_do_ebook(self, ambiente):
        ctx = CP.contexto_material("ebooks/obra-teste--eb")
        assert ctx["tipo"] == "ebook"
        assert ctx["colecao"] == COLECAO
        assert ctx["cta"] == "Baixe o e-book completo"
