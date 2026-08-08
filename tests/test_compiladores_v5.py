"""Testes dos compiladores de saida final da V5.

  gerar-pptx.py            deck.md      -> .pptx editavel (writer nativo do Pandoc)
  gerar-lead-magnet-pdf.py lead_magnet.md -> .html -> .pdf (Chromium/Playwright)

Os testes que dependem de `pandoc`/Chromium sao marcados e pulados quando as
ferramentas nao estao no ambiente — a logica pura (tema, UTM, rodape) e sempre
verificada.
"""

import json
import re
import shutil
import subprocess
import zipfile

import pytest

import tipos_obra as TO
from conftest import carregar_script


def _css_ativo():
    """CSS do template SEM os comentarios.

    Os comentarios documentam justamente as armadilhas que estes testes proibem
    ('nao use filter', 'nao use break-before: avoid') — assertar sobre o arquivo
    cru daria falso positivo no proprio texto explicativo."""
    css = TO.template_html_de("lead-magnet").read_text(encoding="utf-8")
    return re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)

pptx_mod = carregar_script("gerar-pptx.py")
lm_pdf = carregar_script("gerar-lead-magnet-pdf.py")
gerador_lm = carregar_script("gerar-lead-magnet.py")
gerador_deck = carregar_script("gerar-deck.py")
extrator = carregar_script("extrair-passos-praticos.py")

TEM_PANDOC = shutil.which("pandoc") is not None
precisa_pandoc = pytest.mark.skipif(not TEM_PANDOC, reason="pandoc ausente no PATH")


def _tem_chromium():
    if not TEM_PANDOC:
        return False
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

CTA = "https://exemplo.com/obra"


@pytest.fixture
def ambiente(livro_falso, monkeypatch):
    raiz = livro_falso["raiz"]
    for mod in (extrator, gerador_lm, gerador_deck, pptx_mod, lm_pdf):
        monkeypatch.setattr(mod, "DIR_OUTPUT", raiz)
    import series_capa
    monkeypatch.setattr(series_capa, "DIR_OUTPUT", raiz)
    monkeypatch.setattr(series_capa, "CAMINHO_REGISTRO", raiz / "_series.json")
    import metadados_livro
    monkeypatch.setattr(metadados_livro, "DIR_OUTPUT", raiz)
    return livro_falso


# ── Registro ─────────────────────────────────────────────────────────────────

class TestRegistroDeSaidas:
    def test_deck_declara_pdf_e_pptx(self):
        assert set(TO.campo("deck", "extensoes_saida")) == {".pdf", ".pptx"}

    def test_lead_magnet_usa_motor_chromium(self):
        assert TO.motor_pdf("lead-magnet") == "chromium"

    def test_demais_tipos_usam_typst(self):
        for tipo in TO.tipos_validos():
            if tipo != "lead-magnet":
                assert TO.motor_pdf(tipo) == "typst", tipo

    def test_lead_magnet_declara_compilador_proprio_existente(self):
        caminho = TO.compilador_de("lead-magnet")
        assert caminho is not None and caminho.exists()

    def test_tipos_sem_compilador_proprio_devolvem_none(self):
        assert TO.compilador_de("livro") is None
        assert TO.compilador_de("playbook") is None

    def test_template_html_do_lead_magnet_existe(self):
        caminho = TO.template_html_de("lead-magnet")
        assert caminho is not None and caminho.exists()

    def test_html_nunca_e_extensao_de_entrega(self):
        """O HTML e camada intermediaria — o entregavel e o PDF."""
        for tipo in TO.tipos_validos():
            assert ".html" not in TO.campo(tipo, "extensoes_saida", ())


# ── PPTX: logica pura ────────────────────────────────────────────────────────

class TestTemaPptx:
    def test_hex_limpo_normaliza(self):
        assert pptx_mod._hex_limpo("#a855f7") == "A855F7"
        assert pptx_mod._hex_limpo("2ecc9a") == "2ECC9A"

    def test_hex_limpo_cai_no_padrao_para_valor_invalido(self):
        assert pptx_mod._hex_limpo("azul") == "2ECC9A"
        assert pptx_mod._hex_limpo("") == "2ECC9A"
        assert pptx_mod._hex_limpo(None) == "2ECC9A"

    def test_regex_de_accent1_casa_o_tema_office(self):
        xml = b'<a:accent1><a:srgbClr val="4472C4"/></a:accent1>'
        novo, n = pptx_mod.RE_ACCENT1.subn(rb"\g<1>A855F7\g<2>", xml)
        assert n == 1
        assert b'val="A855F7"' in novo

    def test_regex_ignora_outros_accents(self):
        xml = b'<a:accent2><a:srgbClr val="4472C4"/></a:accent2>'
        assert pptx_mod.RE_ACCENT1.subn(rb"\g<1>A855F7\g<2>", xml)[1] == 0

    def test_aplicar_cor_reescreve_o_zip(self, tmp_path):
        origem = tmp_path / "ref.pptx"
        with zipfile.ZipFile(origem, "w") as z:
            z.writestr("ppt/theme/theme1.xml",
                       '<a:accent1><a:srgbClr val="4472C4"/></a:accent1>')
            z.writestr("ppt/presentation.xml", "<p:presentation/>")
        destino = tmp_path / "out.pptx"

        assert pptx_mod.aplicar_cor_no_tema(origem, destino, "A855F7") is True
        with zipfile.ZipFile(destino) as z:
            assert 'val="A855F7"' in z.read("ppt/theme/theme1.xml").decode()
            # nenhum outro membro pode ser perdido na reescrita
            assert set(z.namelist()) == {"ppt/theme/theme1.xml", "ppt/presentation.xml"}

    def test_aplicar_cor_devolve_false_sem_accent1(self, tmp_path):
        origem = tmp_path / "ref.pptx"
        with zipfile.ZipFile(origem, "w") as z:
            z.writestr("ppt/theme/theme1.xml", "<a:theme/>")
        assert pptx_mod.aplicar_cor_no_tema(origem, tmp_path / "o.pptx", "A855F7") is False

    def test_aplicar_cor_nao_toca_arquivos_fora_do_tema(self, tmp_path):
        origem = tmp_path / "ref.pptx"
        conteudo = '<a:accent1><a:srgbClr val="4472C4"/></a:accent1>'
        with zipfile.ZipFile(origem, "w") as z:
            z.writestr("ppt/theme/theme1.xml", conteudo)
            z.writestr("ppt/slides/slide1.xml", conteudo)   # mesmo texto, outro caminho
        destino = tmp_path / "out.pptx"
        pptx_mod.aplicar_cor_no_tema(origem, destino, "A855F7")
        with zipfile.ZipFile(destino) as z:
            assert 'val="4472C4"' in z.read("ppt/slides/slide1.xml").decode()


# ── PPTX: integracao ─────────────────────────────────────────────────────────

@precisa_pandoc
class TestCompilacaoPptx:
    @pytest.fixture
    def deck_pronto(self, ambiente):
        gerador_deck.gerar(ambiente["slug"], cta_url=CTA)
        return "decks/obra-teste--deck"

    def test_reference_padrao_e_um_pptx_valido(self, tmp_path):
        destino = pptx_mod.criar_reference(tmp_path / "ref.pptx")
        assert destino.exists() and destino.stat().st_size > 0
        with zipfile.ZipFile(destino) as z:
            assert any(n.startswith("ppt/theme/") for n in z.namelist())

    def test_criar_reference_e_idempotente(self, tmp_path):
        destino = tmp_path / "ref.pptx"
        pptx_mod.criar_reference(destino)
        marca = destino.stat().st_mtime_ns
        pptx_mod.criar_reference(destino)
        assert destino.stat().st_mtime_ns == marca

    def test_gera_pptx_do_deck(self, ambiente, deck_pronto):
        meta = pptx_mod.compilar(deck_pronto)
        assert meta is not None
        pptx = ambiente["raiz"] / meta["pptx"]
        assert pptx.exists() and pptx.stat().st_size > 0

    def test_pptx_tem_um_slide_por_titulo_de_nivel_1(self, ambiente, deck_pronto):
        meta = pptx_mod.compilar(deck_pronto)
        pptx = ambiente["raiz"] / meta["pptx"]
        with zipfile.ZipFile(pptx) as z:
            slides = [n for n in z.namelist()
                      if n.startswith("ppt/slides/slide") and n.endswith(".xml")]
        # capa do reference + os slides do deck.md
        assert len(slides) >= meta["slides_declarados"]

    def test_pptx_carrega_a_cor_da_colecao_no_tema(self, ambiente, deck_pronto):
        meta = pptx_mod.compilar(deck_pronto)
        esperado = pptx_mod._hex_limpo(meta["cor_acento"])
        pptx = ambiente["raiz"] / meta["pptx"]
        with zipfile.ZipFile(pptx) as z:
            temas = [z.read(n).decode("utf-8", "replace") for n in z.namelist()
                     if n.startswith("ppt/theme/") and n.endswith(".xml")]
        assert any(f'val="{esperado}"' in t for t in temas)

    def test_nao_deixa_reference_tematizado_no_diretorio(self, ambiente, deck_pronto):
        pptx_mod.compilar(deck_pronto)
        assert not (ambiente["raiz"] / deck_pronto / "_reference_tematizado.pptx").exists()

    def test_pptx_conta_como_artefato_do_tipo_deck(self, ambiente, deck_pronto):
        pptx_mod.compilar(deck_pronto)
        colecao = carregar_script("colecao.py")
        assert ".pptx" in TO.campo("deck", "extensoes_saida")
        artefatos = colecao._artefatos(ambiente["raiz"] / deck_pronto, "deck")
        assert any(a.endswith(".pptx") for a in artefatos)

    def test_deck_inexistente_devolve_none(self, ambiente):
        assert pptx_mod.compilar("decks/nao-existe") is None


# ── Lead magnet PDF: logica pura ─────────────────────────────────────────────

class TestRodapeEUtm:
    def test_url_recebe_utm_completa(self):
        url = lm_pdf._url_com_utm(
            {"cta_url": CTA, "obra_mae": "obra-teste", "formato_lm": "checklist"}, {})
        assert "utm_source=lead-magnet" in url
        assert "utm_medium=pdf" in url
        assert "utm_campaign=obra-teste" in url
        assert "utm_content=checklist" in url

    def test_url_preserva_query_existente(self):
        url = lm_pdf._url_com_utm({"cta_url": "https://x.com/a?b=1"}, {})
        assert url.startswith("https://x.com/a?b=1&utm_source=")

    def test_sem_cta_devolve_string_vazia(self):
        assert lm_pdf._url_com_utm({}, {}) == ""

    def test_footer_traz_texto_url_e_numero_de_pagina(self):
        rodape = lm_pdf.montar_footer("Quero o livro", "https://x.com", "#a855f7")
        assert "Quero o livro" in rodape
        assert "https://x.com" in rodape
        assert 'class="pageNumber"' in rodape

    def test_footer_usa_estilo_inline(self):
        """O footerTemplate roda isolado: sem CSS da pagina, so estilo inline."""
        rodape = lm_pdf.montar_footer("X", "https://x.com", "#a855f7")
        assert "style=" in rodape
        assert "<link" not in rodape and "<style" not in rodape

    def test_footer_escapa_html_do_texto(self):
        rodape = lm_pdf.montar_footer('<script>alert(1)</script>', "", "#000")
        assert "<script>" not in rodape
        assert "&lt;script&gt;" in rodape

    def test_footer_sem_url_nao_deixa_travessao_solto(self):
        assert "—" not in lm_pdf.montar_footer("Leia a obra", "", "#000")


# ── Lead magnet PDF: integracao ──────────────────────────────────────────────

@precisa_chromium
class TestCompilacaoLeadMagnetPdf:
    @pytest.fixture
    def lm_pronto(self, ambiente):
        cards, ctx, _ = gerador_lm.resolver_fonte(ambiente["slug"])
        meta = gerador_lm.gerar(ambiente["slug"], "mini-guia", cta_url=CTA,
                                cards=cards, ctx=ctx)
        return meta["slug"]

    def test_gera_pdf_nao_vazio(self, ambiente, lm_pronto):
        meta = lm_pdf.compilar(lm_pronto)
        assert meta is not None
        pdf = ambiente["raiz"] / meta["pdf"]
        assert pdf.exists() and pdf.stat().st_size > 5000

    def test_saida_e_um_pdf_de_verdade(self, ambiente, lm_pronto):
        meta = lm_pdf.compilar(lm_pronto)
        assert (ambiente["raiz"] / meta["pdf"]).read_bytes()[:5] == b"%PDF-"

    def test_html_intermediario_e_descartado(self, ambiente, lm_pronto):
        lm_pdf.compilar(lm_pronto)
        assert not (ambiente["raiz"] / lm_pronto / "_lead_magnet.html").exists()

    def test_manter_html_preserva_o_intermediario(self, ambiente, lm_pronto):
        lm_pdf.compilar(lm_pronto, manter_html=True)
        html = ambiente["raiz"] / lm_pronto / "_lead_magnet.html"
        assert html.exists()
        assert "<section class=\"capa\">" in html.read_text(encoding="utf-8")

    def test_html_recebe_a_cor_da_colecao(self, ambiente, lm_pronto):
        meta = lm_pdf.compilar(lm_pronto, manter_html=True)
        html = (ambiente["raiz"] / lm_pronto / "_lead_magnet.html").read_text(encoding="utf-8")
        assert meta["cor_acento"] in html

    def test_cta_vai_para_o_rodape(self, ambiente, lm_pronto):
        meta = lm_pdf.compilar(lm_pronto)
        assert meta["cta_no_rodape"] is True

    def test_pdf_satisfaz_r_lm_5_no_gate(self, ambiente, lm_pronto, monkeypatch):
        gate = carregar_script("validar-lead-magnet.py")
        monkeypatch.setattr(gate, "DIR_OUTPUT", ambiente["raiz"])
        lm_pdf.compilar(lm_pronto)
        rel = gate.validar(lm_pronto)
        assert not any("PDF ainda nao compilado" in a for a in rel["avisos"])

    def test_lead_magnet_inexistente_devolve_none(self, ambiente):
        assert lm_pdf.compilar("lead-magnets/nao-existe") is None


@precisa_chromium
class TestRegressoesDePaginacao:
    """Tres defeitos achados so ao medir os PDFs reais do livro AIDD v2.
    Nenhum deles aparece no Markdown — todos exigem renderizar e contar."""

    def _paginas(self, ambiente, slug):
        from metadados_livro import contar_paginas_pdf
        meta = lm_pdf.compilar(slug)
        assert meta is not None
        return contar_paginas_pdf(ambiente["raiz"] / meta["pdf"])

    @pytest.fixture
    def cards_ctx(self, ambiente):
        return gerador_lm.resolver_fonte(ambiente["slug"])[:2]

    def test_capa_ocupa_exatamente_uma_pagina(self, ambiente, cards_ctx):
        """A capa media 297mm com 40mm de margem do Playwright: transbordava
        para uma 2a pagina em TODO lead magnet."""
        cards, ctx = cards_ctx
        meta = gerador_lm.gerar(ambiente["slug"], "mini-guia", cta_url=CTA,
                                cards=cards, ctx=ctx)
        lm_pdf.compilar(meta["slug"], manter_html=True)
        html = ambiente["raiz"] / meta["slug"] / "_lead_magnet.html"

        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            navegador = p.chromium.launch()
            pagina = navegador.new_page()
            pagina.goto(f"file:///{html.resolve().as_posix()}", wait_until="networkidle")
            pagina.emulate_media(media="print")
            altura_mm = pagina.evaluate(
                "() => Math.round(document.querySelector('.capa')"
                ".getBoundingClientRect().height / (96/25.4))")
            navegador.close()
        assert altura_mm <= 257, f"capa com {altura_mm}mm transborda a area util"

    def test_primeiro_titulo_nao_gasta_pagina_em_branco(self, ambiente, cards_ctx):
        """O Chromium ignora `break-before: avoid`: a excecao do 1o h1 tem de
        estar no SELETOR (`:not(:first-of-type)`), nao numa regra sobrescrita."""
        css = _css_ativo()
        assert ":not(:first-of-type)" in css
        assert "break-before: avoid" not in css

    def test_tabela_longa_nao_e_empurrada_inteira(self, ambiente):
        """`break-inside: avoid` na TABELA jogava 20 linhas para a pagina
        seguinte, deixando paginas quase vazias. Proteger a LINHA, nao a tabela."""
        css = _css_ativo()
        corpo_table = css.split("table {", 1)[1].split("}", 1)[0]
        assert "break-inside: auto" in corpo_table
        assert re.search(r"\btr\s*\{[^}]*break-inside:\s*avoid", css)

    def test_css_nao_usa_filter_que_rasteriza(self):
        """`filter: brightness()` cria camada raster por elemento: com ~100 h2 o
        PDF foi de ~100KB para 6.6MB."""
        assert "filter:" not in _css_ativo()

    @pytest.mark.parametrize("formato", sorted(TO.FORMATOS_LM))
    def test_todo_formato_respeita_o_teto_de_paginas(self, ambiente, cards_ctx, formato):
        cards, ctx = cards_ctx
        meta = gerador_lm.gerar(ambiente["slug"], formato, cta_url=CTA,
                                cards=cards, ctx=ctx)
        paginas = self._paginas(ambiente, meta["slug"])
        teto = TO.FORMATOS_LM[formato]["max_paginas"]
        assert paginas <= teto, f"{formato}: {paginas}p acima do teto {teto}"

    @pytest.mark.parametrize("formato", sorted(TO.FORMATOS_LM))
    def test_todo_formato_respeita_o_peso_por_pagina(self, ambiente, cards_ctx, formato):
        gate = carregar_script("validar-lead-magnet.py")
        cards, ctx = cards_ctx
        meta = gerador_lm.gerar(ambiente["slug"], formato, cta_url=CTA,
                                cards=cards, ctx=ctx)
        lm_pdf.compilar(meta["slug"])
        pdf = next((ambiente["raiz"] / meta["slug"]).glob("*.pdf"))
        from metadados_livro import contar_paginas_pdf
        paginas = max(1, contar_paginas_pdf(pdf))
        kb_pagina = (pdf.stat().st_size // 1024) // paginas
        assert kb_pagina <= gate.MAX_KB_POR_PAGINA, \
            f"{formato}: {kb_pagina} KB/pagina"
