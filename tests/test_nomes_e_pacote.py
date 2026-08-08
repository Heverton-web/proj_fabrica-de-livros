"""Testes da V5.1: nomes curtos, verificacao de abertura e pacote da colecao."""

import json
import shutil
import zipfile

import pytest

import tipos_obra as TO
from conftest import carregar_script
from nomes_curtos import (codigo_obra, codigos_unicos, excede_max_path,
                          migrar_prefixo_underscore, nome_curto,
                          nome_material, palavras)

validar_art = carregar_script("validar-artefatos.py")
empacotar = carregar_script("empacotar-colecao.py")
colecao = carregar_script("colecao.py")
gerador_lm = carregar_script("gerar-lead-magnet.py")
gerador_deck = carregar_script("gerar-deck.py")
extrator = carregar_script("extrair-passos-praticos.py")
fatiar = carregar_script("fatiar-obra.py")

TEM_PANDOC = shutil.which("pandoc") is not None
CTA = "https://exemplo.com/obra"

PDF_OK = (b"%PDF-1.7\n" + b"/Type /Page \n" * 3 + b"x" * 2000 + b"\ntrailer\n%%EOF")
PDF_TRUNCADO = b"%PDF-1.7\n" + b"/Type /Page \n" + b"x" * 2000


# ── Nomes curtos ─────────────────────────────────────────────────────────────

class TestNomesCurtos:
    def test_palavras_descarta_irrelevantes(self):
        assert palavras("do zero ao deploy da obra") == ["deploy", "obra"]

    def test_palavras_remove_acento_e_caixa(self):
        assert palavras("Sistemas Agênticos") == ["sistemas", "agenticos"]

    def test_codigo_obra_usa_duas_palavras(self):
        assert codigo_obra("ai-driven-development-do-zero-ao-deploy-v2") == "ai-driven"

    def test_codigo_obra_e_estavel(self):
        alvo = "ai-driven-development-do-zero-ao-deploy-v2"
        assert codigo_obra(alvo) == codigo_obra(alvo)

    def test_codigo_obra_de_texto_vazio(self):
        assert codigo_obra("") == "obra"
        assert codigo_obra(None) == "obra"

    def test_nome_curto_tem_no_maximo_3_palavras(self):
        assert nome_curto("um dois tres quatro cinco").count("-") <= 2

    def test_nome_curto_nao_corta_palavra_ao_meio(self):
        """'ai-driven-developmen' e um nome quebrado; 'ai-driven' nao."""
        for texto in ("AI Driven Development", "Sistemas Agenticos Distribuidos",
                      "Engenharia de Harness Avancada"):
            for parte in nome_curto(texto).split("-"):
                assert parte in palavras(texto), f"{parte!r} nao e palavra inteira"

    def test_nome_curto_respeita_o_teto(self):
        assert len(nome_curto("desenvolvimento arquitetura infraestrutura")) <= 26

    def test_nome_material_monta_prefixo_seq_nome(self):
        assert nome_material("lm", 1, "armadilhas") == "lm-1-armadilhas"
        assert nome_material("pbk", 12, "Sistemas Agênticos") == "pbk-12-sistemas-agenticos"

    def test_codigos_unicos_desambigua_colisao(self):
        """O TCC "ai-driven-development" e o livro "ai-driven-development-do-zero-
        ao-deploy-v2" davam o mesmo codigo — e um pacote sobrescrevia o outro."""
        nomes = ["ai-driven-development", "ai-driven-development-do-zero-ao-deploy-v2"]
        codigos = codigos_unicos(nomes)
        assert len(set(codigos.values())) == 2
        assert all(v for v in codigos.values())

    def test_codigos_unicos_e_estavel_na_ordem_de_entrada(self):
        nomes = ["b-obra-uma", "a-obra-duas", "b-obra-tres"]
        assert codigos_unicos(nomes) == codigos_unicos(list(reversed(nomes)))

    def test_codigos_unicos_preserva_o_codigo_quando_nao_ha_colisao(self):
        codigos = codigos_unicos(["ai-driven-development-v2", "harness-engineering"])
        assert codigos["harness-engineering"] == codigo_obra("harness-engineering")

    def test_codigos_unicos_resolve_colisao_total(self):
        """Nomes que nao se distinguem nem com 3 palavras caem no sufixo numerico."""
        codigos = codigos_unicos(["obra x", "obra y"])
        assert len(set(codigos.values())) == 2

    def test_excede_max_path_detecta_caminho_longo(self):
        assert excede_max_path("C:/" + "a" * 250) is True
        assert excede_max_path("C:/curto.pdf") is False


class TestSemPrefixoUnderscore:
    """Nenhum arquivo ou pasta gerado pela fabrica pode comecar com "_": em glob
    de shell, listagem de nuvem e empacotamento ele e tratado como oculto."""

    CAMINHOS_GERADOS = (
        "colecoes", "distribuicao", "series.json", "pool-estado.json",
        "lead-magnet-render.html", "deck-corpo.md", "livro-compilado.md",
        "livro-compilado.typ", "livro-render.md", "ebook-compilado.typ",
        "reference-tematizado.pptx",
    )

    def test_nenhum_caminho_gerado_comeca_com_underscore(self):
        for nome in self.CAMINHOS_GERADOS:
            assert not nome.startswith("_"), nome

    def test_codigo_de_obra_nunca_comeca_com_underscore(self):
        for entrada in ("_oculto", "__dunder__", "_", "_ai-driven"):
            assert not codigo_obra(entrada).startswith("_"), entrada

    def test_nome_de_material_nunca_comeca_com_underscore(self):
        assert not nome_material("lm", 1, "_armadilhas").startswith("_")

    def test_slug_curto_nao_produz_segmento_com_underscore(self):
        s = TO.slug_curto("lead-magnet", "_obra_interna", 1, "_armadilhas")
        assert not any(seg.startswith("_") for seg in s.split("/")), s

    def test_migracao_renomeia_o_legado(self, tmp_path):
        (tmp_path / "_series.json").write_text("{}", encoding="utf-8")
        assert migrar_prefixo_underscore(tmp_path / "series.json") is True
        assert (tmp_path / "series.json").exists()
        assert not (tmp_path / "_series.json").exists()

    def test_migracao_aceita_troca_de_separador(self, tmp_path):
        """_pool_estado.json -> pool-estado.json (prefixo E separador mudaram)."""
        (tmp_path / "_pool_estado.json").write_text("{}", encoding="utf-8")
        assert migrar_prefixo_underscore(tmp_path / "pool-estado.json") is True
        assert (tmp_path / "pool-estado.json").exists()

    def test_migracao_preserva_o_conteudo(self, tmp_path):
        """Perder series.json faria as capas re-sortearem a cor da colecao."""
        (tmp_path / "_series.json").write_text('{"cor": "#a855f7"}', encoding="utf-8")
        migrar_prefixo_underscore(tmp_path / "series.json")
        assert "#a855f7" in (tmp_path / "series.json").read_text(encoding="utf-8")

    def test_migracao_e_idempotente_e_nao_sobrescreve(self, tmp_path):
        (tmp_path / "series.json").write_text('{"novo": 1}', encoding="utf-8")
        (tmp_path / "_series.json").write_text('{"velho": 1}', encoding="utf-8")
        assert migrar_prefixo_underscore(tmp_path / "series.json") is False
        assert '"novo"' in (tmp_path / "series.json").read_text(encoding="utf-8")

    def test_migracao_sem_legado_nao_faz_nada(self, tmp_path):
        assert migrar_prefixo_underscore(tmp_path / "series.json") is False

    def test_migracao_funciona_para_pasta(self, tmp_path):
        (tmp_path / "_colecoes").mkdir()
        (tmp_path / "_colecoes" / "x.json").write_text("{}", encoding="utf-8")
        assert migrar_prefixo_underscore(tmp_path / "colecoes") is True
        assert (tmp_path / "colecoes" / "x.json").exists()


class TestSlugsDoRegistro:
    def test_tipos_v51_usam_nomes_curtos(self):
        for tipo in ("playbook", "lead-magnet", "deck", "emails"):
            assert TO.usa_nomes_curtos(tipo), tipo

    def test_tipos_v4_mantem_nomenclatura_antiga(self):
        """Renomear artigo/ebook orfanaria artefatos ja compilados no disco."""
        for tipo in ("livro", "tcc", "artigo", "ebook"):
            assert not TO.usa_nomes_curtos(tipo), tipo

    def test_prefixo_curto_e_unico(self):
        prefixos = [TO.prefixo_curto(t) for t in TO.tipos_validos()]
        assert len(prefixos) == len(set(prefixos))

    def test_slug_curto_tem_tres_niveis(self):
        s = TO.slug_curto("lead-magnet", "ai-driven-development-v2", 1, "armadilhas")
        assert s == "lead-magnets/ai-driven/lm-1-armadilhas"

    def test_slug_curto_encurta_o_caminho_de_verdade(self):
        mae = "ai-driven-development-do-zero-ao-deploy-v2"
        antigo = f"lead-magnets/{mae}--lm-01-armadilhas/{mae}--lm-01-armadilhas.pdf"
        novo = TO.slug_curto("lead-magnet", mae, 1, "armadilhas")
        novo += f"/{TO.nome_arquivo(novo)}.pdf"
        assert len(novo) < len(antigo) / 2

    def test_nome_arquivo_pega_o_ultimo_segmento(self):
        assert TO.nome_arquivo("lead-magnets/ai-driven/lm-1-armadilhas") == "lm-1-armadilhas"


# ── Verificacao de abertura ──────────────────────────────────────────────────

class TestVerificarArquivo:
    def test_pdf_integro_abre(self, tmp_path):
        f = tmp_path / "a.pdf"; f.write_bytes(PDF_OK)
        r = validar_art.verificar_arquivo(f)
        assert r["abre"] and "3 pagina" in r["detalhe"]

    def test_pdf_truncado_nao_abre(self, tmp_path):
        f = tmp_path / "a.pdf"; f.write_bytes(PDF_TRUNCADO)
        assert validar_art.verificar_arquivo(f)["abre"] is False

    def test_pdf_sem_assinatura_nao_abre(self, tmp_path):
        f = tmp_path / "a.pdf"; f.write_bytes(b"nao sou pdf" + b"x" * 2000)
        assert validar_art.verificar_arquivo(f)["abre"] is False

    def test_arquivo_minusculo_e_suspeito(self, tmp_path):
        f = tmp_path / "a.pdf"; f.write_bytes(b"%PDF-1.7")
        r = validar_art.verificar_arquivo(f)
        assert r["abre"] is False and "vazio" in r["detalhe"]

    def test_arquivo_inexistente(self, tmp_path):
        r = validar_art.verificar_arquivo(tmp_path / "nao-existe.pdf")
        assert r["abre"] is False and "inexistente" in r["detalhe"]

    def test_html_completo_abre(self, tmp_path):
        f = tmp_path / "a.html"
        f.write_text("<html><body>" + "x" * 2000 + "</body></html>", encoding="utf-8")
        assert validar_art.verificar_arquivo(f)["abre"]

    def test_html_com_placeholder_de_template_nao_abre(self, tmp_path):
        """Template nao substituido = pandoc falhou e a saida velha ficou."""
        f = tmp_path / "a.html"
        f.write_text("<html><body>$body$" + "x" * 2000 + "</body></html>", encoding="utf-8")
        r = validar_art.verificar_arquivo(f)
        assert r["abre"] is False and "placeholder" in r["detalhe"]

    def test_html_sem_fechamento_nao_abre(self, tmp_path):
        f = tmp_path / "a.html"; f.write_text("<html><body>" + "x" * 2000, encoding="utf-8")
        assert validar_art.verificar_arquivo(f)["abre"] is False

    def test_zip_valido_como_pptx(self, tmp_path):
        f = tmp_path / "a.pptx"
        with zipfile.ZipFile(f, "w") as z:
            z.writestr("[Content_Types].xml", "<x/>" + "y" * 2000)
            z.writestr("ppt/presentation.xml", "<p/>")
        assert validar_art.verificar_arquivo(f)["abre"]

    def test_pptx_sem_membro_obrigatorio_nao_abre(self, tmp_path):
        f = tmp_path / "a.pptx"
        with zipfile.ZipFile(f, "w") as z:
            z.writestr("qualquer.xml", "<x/>" + "y" * 2000)
        assert validar_art.verificar_arquivo(f)["abre"] is False

    def test_epub_com_mimetype_errado_nao_abre(self, tmp_path):
        f = tmp_path / "a.epub"
        with zipfile.ZipFile(f, "w") as z:
            z.writestr("mimetype", "application/zip")
            z.writestr("META-INF/container.xml", "<c/>" + "y" * 2000)
        assert validar_art.verificar_arquivo(f)["abre"] is False

    def test_arquivo_corrompido_nao_derruba_o_verificador(self, tmp_path):
        f = tmp_path / "a.pptx"; f.write_bytes(b"lixo" * 600)
        assert validar_art.verificar_arquivo(f)["abre"] is False

    def test_md_vazio_nao_abre(self, tmp_path):
        f = tmp_path / "a.md"; f.write_text("   ", encoding="utf-8")
        assert validar_art.verificar_arquivo(f)["abre"] is False

    def test_md_com_polimento_abre_mas_avisa(self, tmp_path):
        f = tmp_path / "a.md"
        f.write_text("texto <!-- POLIMENTO-LLM -->", encoding="utf-8")
        r = validar_art.verificar_arquivo(f)
        assert r["abre"] and "polimento" in r["detalhe"]


class TestArtefatosDoSlug:
    def test_ignora_livro_final_quando_ha_copia_nomeada(self, tmp_path, monkeypatch):
        raiz = tmp_path / "output"
        d = raiz / "playbooks" / "cod" / "pbk-1-x"
        d.mkdir(parents=True)
        (d / "config_obra.json").write_text('{"tipo_obra": "playbook"}', encoding="utf-8")
        (d / "livro_final.pdf").write_bytes(PDF_OK)
        (d / "pbk-1-x.pdf").write_bytes(PDF_OK)
        monkeypatch.setattr(validar_art, "DIR_OUTPUT", raiz)
        nomes = [a.name for a in validar_art.artefatos_do_slug("playbooks/cod/pbk-1-x")]
        assert nomes == ["pbk-1-x.pdf"]

    def test_aceita_livro_final_quando_e_o_unico(self, tmp_path, monkeypatch):
        raiz = tmp_path / "output"
        d = raiz / "playbooks" / "cod" / "pbk-1-x"
        d.mkdir(parents=True)
        (d / "config_obra.json").write_text('{"tipo_obra": "playbook"}', encoding="utf-8")
        (d / "livro_final.pdf").write_bytes(PDF_OK)
        monkeypatch.setattr(validar_art, "DIR_OUTPUT", raiz)
        assert len(validar_art.artefatos_do_slug("playbooks/cod/pbk-1-x")) == 1


# ── Varredura em dois layouts ────────────────────────────────────────────────

class TestListarMateriais:
    @pytest.fixture
    def disco(self, tmp_path, monkeypatch):
        raiz = tmp_path / "output"
        # V5.1 aninhado
        for nome in ("lm-1-armadilhas", "lm-2-checklist"):
            d = raiz / "lead-magnets" / "cod" / nome
            d.mkdir(parents=True)
            (d / "config_obra.json").write_text('{"tipo_obra":"lead-magnet"}', encoding="utf-8")
        # V4 raso
        d = raiz / "artigos" / "obra--art-01-x"
        d.mkdir(parents=True)
        (d / "config_obra.json").write_text('{"tipo_obra":"artigo"}', encoding="utf-8")
        monkeypatch.setattr(TO, "DIR_OUTPUT", raiz)
        return raiz

    def test_encontra_material_aninhado(self, disco):
        assert TO.listar_materiais("lead-magnet") == [
            "lead-magnets/cod/lm-1-armadilhas", "lead-magnets/cod/lm-2-checklist"]

    def test_encontra_material_raso(self, disco):
        assert TO.listar_materiais("artigo") == ["artigos/obra--art-01-x"]

    def test_nao_confunde_pasta_de_codigo_com_material(self, disco):
        """A pasta <codigo> nao tem config_obra.json e nao pode virar 'material' —
        era isso que inventava uma colecao com o nome do codigo."""
        assert "lead-magnets/cod" not in TO.listar_materiais("lead-magnet")

    def test_tipo_sem_pasta_devolve_lista_vazia(self, disco):
        assert TO.listar_materiais("deck") == []


# ── Pacote da colecao ────────────────────────────────────────────────────────

class TestPacoteDaColecao:
    @pytest.fixture
    def ambiente(self, livro_falso, monkeypatch):
        raiz = livro_falso["raiz"]
        for mod in (extrator, gerador_lm, gerador_deck, fatiar, colecao,
                    validar_art, empacotar):
            monkeypatch.setattr(mod, "DIR_OUTPUT", raiz, raising=False)
        monkeypatch.setattr(colecao, "DIR_COLECOES", raiz / "colecoes")
        monkeypatch.setattr(empacotar, "DIR_PACOTES", raiz / "distribuicao")
        import series_capa
        monkeypatch.setattr(series_capa, "DIR_OUTPUT", raiz)
        monkeypatch.setattr(series_capa, "CAMINHO_REGISTRO", raiz / "series.json")

        cards, ctx, _ = gerador_lm.resolver_fonte(livro_falso["slug"])
        for f in ("checklist", "armadilhas"):
            meta = gerador_lm.gerar(livro_falso["slug"], f, cta_url=CTA,
                                    cards=cards, ctx=ctx)
            (raiz / meta["slug"] / f"{TO.nome_arquivo(meta['slug'])}.pdf").write_bytes(PDF_OK)
        # PDF do livro-mae, para ele tambem entrar no pacote
        (livro_falso["dir_livro"] / "livro_final.pdf").write_bytes(PDF_OK)
        return livro_falso

    def test_pacote_usa_codigo_curto_na_raiz(self, ambiente):
        meta = empacotar.empacotar("Colecao Teste")
        assert meta["pacote"].replace("\\", "/") == "distribuicao/colecao-teste"

    def test_copia_apenas_o_que_abre(self, ambiente):
        # Corrompe um dos lead magnets: ele nao pode entrar no pacote
        alvo = next((ambiente["raiz"] / "lead-magnets").rglob("*.pdf"))
        alvo.write_bytes(PDF_TRUNCADO)
        meta = empacotar.empacotar("Colecao Teste")
        assert any(e["tipo"] == "lead-magnet" for e in meta["excluidos"])

    def test_material_sem_artefato_fica_de_fora_com_motivo(self, ambiente):
        meta = empacotar.empacotar("Colecao Teste")
        motivos = [e["motivo"] for e in meta["excluidos"]]
        assert all(m for m in motivos), "todo excluido precisa de motivo"

    def test_sequencia_nao_repete_dentro_do_tipo(self, ambiente):
        empacotar.empacotar("Colecao Teste")
        pasta = ambiente["raiz"] / "distribuicao" / "colecao-teste" / "lead-magnets"
        nomes = sorted(p.stem for p in pasta.glob("*.pdf"))
        assert len(nomes) == len(set(nomes))

    def test_licenca_e_leia_me_sempre_presentes(self, ambiente):
        empacotar.empacotar("Colecao Teste")
        base = ambiente["raiz"] / "distribuicao" / "colecao-teste"
        assert (base / "LICENCA.txt").exists()
        assert (base / "LEIA-ME.md").exists()

    def test_licenca_declara_direitos_reservados(self, ambiente):
        empacotar.empacotar("Colecao Teste")
        texto = (ambiente["raiz"] / "distribuicao" / "colecao-teste" /
                 "LICENCA.txt").read_text(encoding="utf-8")
        assert "TODOS OS DIREITOS RESERVADOS" in texto
        assert "Heverton Eduardo Peres" in texto

    def test_leia_me_omite_a_secao_quando_nada_ficou_de_fora(self, ambiente):
        empacotar.empacotar("Colecao Teste")
        texto = (ambiente["raiz"] / "distribuicao" / "colecao-teste" /
                 "LEIA-ME.md").read_text(encoding="utf-8")
        assert "Não incluído nesta versão" not in texto

    def test_leia_me_lista_o_que_ficou_de_fora(self, ambiente):
        # Deck gerado mas NAO compilado: e exatamente o caso que o pacote tem de
        # deixar de fora e declarar no LEIA-ME.
        gerador_deck.gerar(ambiente["slug"], cta_url=CTA)
        colecao.sincronizar()
        meta = empacotar.empacotar("Colecao Teste")
        texto = (ambiente["raiz"] / "distribuicao" / "colecao-teste" /
                 "LEIA-ME.md").read_text(encoding="utf-8")
        assert "Não incluído nesta versão" in texto
        assert any(e["tipo"] == "deck" for e in meta["excluidos"])
        assert "sem artefato compilado" in texto

    def test_e_idempotente(self, ambiente):
        a = empacotar.empacotar("Colecao Teste")
        b = empacotar.empacotar("Colecao Teste")
        assert a["arquivos"] == b["arquivos"]

    def test_todo_caminho_do_pacote_abre_no_windows(self, ambiente):
        empacotar.empacotar("Colecao Teste")
        base = ambiente["raiz"] / "distribuicao" / "colecao-teste"
        longos = [p for p in base.rglob("*") if p.is_file() and excede_max_path(p)]
        assert not longos, f"caminhos arriscados no pacote: {longos}"

    def test_pacote_nao_contem_nada_com_prefixo_underscore(self, ambiente):
        empacotar.empacotar("Colecao Teste")
        base = ambiente["raiz"] / "distribuicao" / "colecao-teste"
        ocultos = [p.name for p in base.rglob("*") if p.name.startswith("_")]
        assert not ocultos, ocultos

    def test_pasta_de_pacotes_nao_tem_prefixo_underscore(self):
        assert not empacotar.DIR_PACOTES.name.startswith("_")

    def test_colecao_inexistente_devolve_none(self, ambiente):
        assert empacotar.empacotar("nao-existe") is None
