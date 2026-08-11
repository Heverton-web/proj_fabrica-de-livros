"""Testes do LEAD MAGNET: gerador (agregacao dos cards) + gate R-LM-1 a R-LM-7."""

import json

import pytest

import tipos_obra as TO
from conftest import carregar_script

extrator = carregar_script("extrair-passos-praticos.py")
gerador = carregar_script("gerar-lead-magnet.py")
gate = carregar_script("validar-lead-magnet.py")

CTA = "https://exemplo.com/obra"


@pytest.fixture
def ambiente(livro_falso, monkeypatch):
    raiz = livro_falso["raiz"]
    for mod in (extrator, gerador, gate):
        monkeypatch.setattr(mod, "DIR_OUTPUT", raiz)
    monkeypatch.setattr(gate, "DIR_LM", raiz / "lead-magnets")
    return livro_falso


@pytest.fixture
def cards_ctx(ambiente):
    cards, ctx, _ = gerador.resolver_fonte(ambiente["slug"])
    return cards, ctx


class TestResolverFonte:
    def test_extrai_na_hora_quando_nao_ha_playbook(self, ambiente):
        cards, ctx, slug = gerador.resolver_fonte(ambiente["slug"])
        assert len(cards) == 2
        assert ctx["titulo_obra"] == "A Obra em Construção"

    def test_reaproveita_playbook_existente(self, ambiente, monkeypatch):
        res = extrator.extrair(ambiente["slug"], montar=False)
        slug_pbk = str(res["dir"].relative_to(ambiente["raiz"])).replace("\\", "/")
        cards, _ctx, _ = gerador.resolver_fonte(slug_pbk)
        assert [c["numero"] for c in cards] == ["01", "02"]

    def test_livro_inexistente_devolve_none(self, ambiente):
        cards, _ctx, _ = gerador.resolver_fonte("livros/nao-existe")
        assert cards is None


class TestMontadores:
    def test_checklist_agrega_feito_quando(self, cards_ctx):
        cards, ctx = cards_ctx
        _corpo, n = gerador.montar_checklist(cards, ctx)
        assert n == sum(len(c["feito_quando"]) for c in cards)

    def test_armadilhas_agrega_armadilhas(self, cards_ctx):
        cards, ctx = cards_ctx
        corpo, n = gerador.montar_armadilhas(cards, ctx)
        assert n == 3
        assert any("Onde aparece" in linha for linha in corpo)

    def test_cheatsheet_agrega_comandos(self, cards_ctx):
        cards, ctx = cards_ctx
        _corpo, n = gerador.montar_cheatsheet(cards, ctx)
        assert n == 2

    def test_entregas_monta_tabela(self, cards_ctx):
        cards, ctx = cards_ctx
        corpo, n = gerador.montar_entregas(cards, ctx)
        assert n == 3
        assert "| Etapa | Entrega | Verificação |" in corpo

    def test_mapa_usa_estagios_do_motivo_condutor(self, cards_ctx):
        cards, ctx = cards_ctx
        corpo, n = gerador.montar_mapa(cards, ctx)
        # O mapa renderiza as DUAS tabelas (estagios + etapas): o contador e o
        # total de linhas — nao so os estagios. Bug real: obra com 2 estagios
        # e 8 etapas reprovava R-LM-7 (mapa rico, contador raso).
        assert n == len(ctx.get("estagios", [])) + len(cards)
        assert n >= 1
        assert any("Fundação" in l for l in corpo)

    def test_mini_guia_usa_o_primeiro_card_e_marca_polimento(self, cards_ctx):
        cards, ctx = cards_ctx
        corpo, n = gerador.montar_mini_guia(cards, ctx)
        assert n == 1
        assert any("POLIMENTO-LLM" in l for l in corpo)

    def test_todo_formato_tem_montador(self):
        assert set(gerador.MONTADORES) == set(TO.FORMATOS_LM)


class TestGeracao:
    def test_gera_arquivos_e_config(self, ambiente, cards_ctx):
        cards, ctx = cards_ctx
        meta = gerador.gerar(ambiente["slug"], "checklist", cta_url=CTA,
                             cards=cards, ctx=ctx)
        dir_lm = ambiente["raiz"] / meta["slug"]
        assert (dir_lm / "lead_magnet.md").exists()
        cfg = json.loads((dir_lm / "config_obra.json").read_text(encoding="utf-8"))
        assert cfg["tipo_obra"] == "lead-magnet"
        assert cfg["formato_lm"] == "checklist"
        assert cfg["cta_url"] == CTA

    def test_utm_e_montada_com_campanha_e_formato(self, ambiente, cards_ctx):
        cards, ctx = cards_ctx
        meta = gerador.gerar(ambiente["slug"], "armadilhas", cta_url=CTA,
                             cards=cards, ctx=ctx)
        md = (ambiente["raiz"] / meta["slug"] / "lead_magnet.md").read_text(encoding="utf-8")
        assert "utm_source=lead-magnet" in md
        assert "utm_campaign=obra-teste" in md
        assert "utm_content=armadilhas" in md

    def test_bloco_de_cta_final_sempre_presente(self, ambiente, cards_ctx):
        cards, ctx = cards_ctx
        meta = gerador.gerar(ambiente["slug"], "mapa", cta_url=CTA, cards=cards, ctx=ctx)
        md = (ambiente["raiz"] / meta["slug"] / "lead_magnet.md").read_text(encoding="utf-8")
        assert "# Próximo passo" in md

    def test_herda_serie_e_senioridade_da_obra_mae(self, ambiente, cards_ctx):
        cards, ctx = cards_ctx
        meta = gerador.gerar(ambiente["slug"], "checklist", cta_url=CTA,
                             cards=cards, ctx=ctx)
        cfg = json.loads((ambiente["raiz"] / meta["slug"] / "config_obra.json")
                         .read_text(encoding="utf-8"))
        assert cfg["serie"] == "Colecao Teste"
        assert cfg["senioridade_obra"] == "intermediario"

    def test_formato_invalido_devolve_none(self, ambiente, cards_ctx):
        cards, ctx = cards_ctx
        assert gerador.gerar(ambiente["slug"], "inexistente", cards=cards, ctx=ctx) is None

    def test_slug_traz_indice_e_formato(self, ambiente, cards_ctx):
        cards, ctx = cards_ctx
        meta = gerador.gerar(ambiente["slug"], "cheatsheet", indice=4, cta_url=CTA,
                             cards=cards, ctx=ctx)
        assert meta["slug"] == TO.slug_curto("lead-magnet", "obra-teste", 4, "cheatsheet")
        assert meta["slug"].endswith("/lm-4-cheatsheet")


class TestIndiceEstavel:
    """Gerar um formato isolado tem de REESCREVER o material existente, nao criar
    um diretorio paralelo. Com indice posicional, `--formato mapa` sozinho gerava
    `--lm-01-mapa` ao lado do `--lm-05-mapa` do lote anterior."""

    def test_indice_deriva_do_formato_nao_da_posicao(self):
        for i, formato in enumerate(sorted(TO.FORMATOS_LM), 1):
            assert gerador.indice_do_formato(formato) == i

    def test_geracao_isolada_cai_no_mesmo_slug_do_lote(self, ambiente, cards_ctx):
        cards, ctx = cards_ctx
        do_lote = {f: gerador.gerar(ambiente["slug"], f, cta_url=CTA,
                                    cards=cards, ctx=ctx)["slug"]
                   for f in sorted(TO.FORMATOS_LM)}
        for formato, slug_lote in do_lote.items():
            isolado = gerador.gerar(ambiente["slug"], formato, cta_url=CTA,
                                    cards=cards, ctx=ctx)
            assert isolado["slug"] == slug_lote, formato

    def test_lote_completo_nao_deixa_diretorio_orfao(self, ambiente, cards_ctx):
        cards, ctx = cards_ctx
        for formato in sorted(TO.FORMATOS_LM):
            gerador.gerar(ambiente["slug"], formato, cta_url=CTA, cards=cards, ctx=ctx)
        gerador.gerar(ambiente["slug"], "mapa", cta_url=CTA, cards=cards, ctx=ctx)
        dirs = [d for d in (ambiente["raiz"] / "lead-magnets").glob("*/*") if d.is_dir()]
        assert len(dirs) == len(TO.FORMATOS_LM)


class TestTetoDeItens:
    """Sem teto, um livro XG rende "As 100 Armadilhas de X": 16 paginas e longe
    demais para ser acionavel."""

    def test_todo_formato_declara_teto_coerente(self):
        for formato, spec in TO.FORMATOS_LM.items():
            assert spec["max_itens"] >= spec["min_itens"], formato

    def test_rodizio_espalha_entre_os_cards(self):
        cards = [{"numero": "01", "titulo": "A", "armadilhas": ["a1", "a2", "a3"]},
                 {"numero": "02", "titulo": "B", "armadilhas": ["b1", "b2"]}]
        escolhidos = gerador._rodizio(cards, "armadilhas", 3)
        assert [t[2] for t in escolhidos] == ["a1", "a2", "b1"]

    def test_rodizio_nao_concentra_no_primeiro_card(self):
        cards = [{"numero": "01", "titulo": "A", "armadilhas": [f"a{i}" for i in range(10)]},
                 {"numero": "02", "titulo": "B", "armadilhas": ["b1"]}]
        numeros = {t[0] for t in gerador._rodizio(cards, "armadilhas", 3)}
        assert numeros == {1, 2}

    def test_rodizio_respeita_o_teto(self):
        cards = [{"numero": "01", "titulo": "A", "armadilhas": [f"a{i}" for i in range(50)]}]
        assert len(gerador._rodizio(cards, "armadilhas", 7)) == 7

    def test_rodizio_para_quando_esgota(self):
        cards = [{"numero": "01", "titulo": "A", "armadilhas": ["a1"]}]
        assert len(gerador._rodizio(cards, "armadilhas", 99)) == 1

    def test_rodizio_devolve_em_ordem_de_capitulo(self):
        cards = [{"numero": "02", "titulo": "B", "armadilhas": ["b1"]},
                 {"numero": "01", "titulo": "A", "armadilhas": ["a1"]}]
        assert [t[0] for t in gerador._rodizio(cards, "armadilhas", 9)] == [1, 2]

    def test_armadilhas_corta_no_teto_e_avisa_o_total(self):
        cards = [{"numero": str(i).zfill(2), "titulo": f"C{i}",
                  "armadilhas": [f"erro {i}.{j}" for j in range(5)]} for i in range(1, 11)]
        corpo, n = gerador.montar_armadilhas(cards, {}, teto=8)
        assert n == 8
        assert any("A obra completa cataloga 50" in l for l in corpo)

    def test_armadilhas_sem_corte_nao_avisa(self):
        cards = [{"numero": "01", "titulo": "C1", "armadilhas": ["erro um", "erro dois"]}]
        corpo, n = gerador.montar_armadilhas(cards, {}, teto=25)
        assert n == 2
        assert not any("A obra completa cataloga" in l for l in corpo)

    def test_mapa_nao_traz_coluna_objetivo(self, ambiente, cards_ctx):
        """A coluna Objetivo ocupava 227mm (1 pagina) e estourava o teto."""
        cards, ctx = cards_ctx
        corpo, _n = gerador.montar_mapa(cards, ctx)
        cabecalho = next(l for l in corpo if l.startswith("| # | Etapa"))
        assert "Objetivo" not in cabecalho
        assert "Estágio" in cabecalho

    def test_truncar_neutraliza_pipe_da_tabela(self):
        assert "|" not in gerador._truncar("a | b", 40)

    def test_truncar_corta_na_fronteira_de_palavra(self):
        assert gerador._truncar("palavra outra terceira", 12) == "palavra…"


class TestGate:
    def _gerar(self, ambiente, cards_ctx, formato="checklist", **kw):
        cards, ctx = cards_ctx
        return gerador.gerar(ambiente["slug"], formato, cards=cards, ctx=ctx, **kw)

    def test_lead_magnet_completo_e_conforme(self, ambiente, cards_ctx):
        # `mini-guia` exige 1 item — e o unico formato que a obra de teste
        # (2 capitulos, 1 deles incompleto) consegue satisfazer sem tropecar
        # em R-LM-7. Os demais formatos sao cobertos regra a regra abaixo.
        meta = self._gerar(ambiente, cards_ctx, formato="mini-guia", cta_url=CTA)
        rel = gate.validar(meta["slug"])
        assert rel["conforme"], rel["violacoes"]

    def test_obra_rasa_reprova_por_falta_de_itens(self, ambiente, cards_ctx):
        """Gate cumprindo seu papel: livro-mae pobre nao vira checklist."""
        meta = self._gerar(ambiente, cards_ctx, formato="checklist", cta_url=CTA)
        rel = gate.validar(meta["slug"])
        assert {v["regra"] for v in rel["violacoes"]} == {"R-LM-7"}

    def test_r_lm_1_reprova_sem_cta(self, ambiente, cards_ctx):
        meta = self._gerar(ambiente, cards_ctx)     # sem cta_url
        rel = gate.validar(meta["slug"])
        assert "R-LM-1" in {v["regra"] for v in rel["violacoes"]}

    def test_r_lm_2_reprova_titulo_sem_promessa(self, ambiente, cards_ctx):
        meta = self._gerar(ambiente, cards_ctx, cta_url=CTA)
        caminho = ambiente["raiz"] / meta["slug"] / "sumario_macro.json"
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        dados["titulo_obra"] = "Material sobre o assunto"
        caminho.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
        rel = gate.validar(meta["slug"])
        assert "R-LM-2" in {v["regra"] for v in rel["violacoes"]}

    def test_r_lm_3_reprova_acima_do_teto_de_paginas(self, ambiente, cards_ctx):
        meta = self._gerar(ambiente, cards_ctx, formato="mapa", cta_url=CTA)
        caminho = ambiente["raiz"] / meta["slug"] / "lead_magnet.md"
        caminho.write_text(caminho.read_text(encoding="utf-8") + "x" * 30_000,
                           encoding="utf-8")
        rel = gate.validar(meta["slug"])
        assert "R-LM-3" in {v["regra"] for v in rel["violacoes"]}

    def test_r_lm_4_reprova_teoria_reciclada(self, ambiente, cards_ctx):
        meta = self._gerar(ambiente, cards_ctx, cta_url=CTA)
        cap = (ambiente["dir_livro"] / "capitulos" / "cap_01.md").read_text(encoding="utf-8")
        caminho = ambiente["raiz"] / meta["slug"] / "lead_magnet.md"
        caminho.write_text(caminho.read_text(encoding="utf-8") + "\n" + cap * 3,
                           encoding="utf-8")
        rel = gate.validar(meta["slug"])
        assert "R-LM-4" in {v["regra"] for v in rel["violacoes"]}

    def test_r_lm_6_reprova_sem_senioridade(self, ambiente, cards_ctx):
        meta = self._gerar(ambiente, cards_ctx, cta_url=CTA)
        caminho = ambiente["raiz"] / meta["slug"] / "config_obra.json"
        cfg = json.loads(caminho.read_text(encoding="utf-8"))
        cfg["senioridade_obra"] = ""
        caminho.write_text(json.dumps(cfg, ensure_ascii=False), encoding="utf-8")
        rel = gate.validar(meta["slug"])
        assert "R-LM-6" in {v["regra"] for v in rel["violacoes"]}

    def test_r_lm_7_reprova_abaixo_do_minimo_de_itens(self, ambiente, cards_ctx):
        meta = self._gerar(ambiente, cards_ctx, cta_url=CTA)
        caminho = ambiente["raiz"] / meta["slug"] / "sumario_macro.json"
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        dados["itens"] = 1
        caminho.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
        rel = gate.validar(meta["slug"])
        assert "R-LM-7" in {v["regra"] for v in rel["violacoes"]}

    def test_r_lm_5_pdf_e_png_ausentes_sao_aviso(self, ambiente, cards_ctx):
        meta = self._gerar(ambiente, cards_ctx, cta_url=CTA)
        rel = gate.validar(meta["slug"])
        assert any("PDF" in a for a in rel["avisos"])
        assert any("card social" in a for a in rel["avisos"])

    def test_marcador_de_polimento_vira_aviso(self, ambiente, cards_ctx):
        meta = self._gerar(ambiente, cards_ctx, formato="mini-guia", cta_url=CTA)
        rel = gate.validar(meta["slug"])
        assert any("polimento" in a for a in rel["avisos"])

    def test_arquivo_ausente_reprova(self, ambiente):
        rel = gate.validar("lead-magnets/nao-existe")
        assert rel["conforme"] is False
