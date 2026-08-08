"""Testes do extrator deterministico do PLAYBOOK (scripts/extrair-passos-praticos.py).

Criterio de aceite da Fase B: rodar sobre um livro EITA produz 1 card por
capitulo, com objetivo/execucao/gate preenchidos, e o relatorio aponta com
precisao os capitulos incompletos.
"""

import json

import pytest

from conftest import carregar_script

extrator = carregar_script("extrair-passos-praticos.py")


@pytest.fixture
def extraido(livro_falso, monkeypatch):
    monkeypatch.setattr(extrator, "DIR_OUTPUT", livro_falso["raiz"])
    res = extrator.extrair(livro_falso["slug"])
    assert res is not None
    return res


class TestContextoDaObra:
    def test_mapeia_capitulos_para_estagios(self, livro_falso, monkeypatch):
        monkeypatch.setattr(extrator, "DIR_OUTPUT", livro_falso["raiz"])
        ctx = extrator.contexto_da_obra(livro_falso["slug"])
        assert ctx["mapa"]["01"]["titulo"] == "Fundação do Projeto"
        assert ctx["mapa"]["01"]["estagio"] == "Fundação"      # vocabulario, R-PBK-8

    def test_herda_persona_e_senioridade(self, livro_falso, monkeypatch):
        monkeypatch.setattr(extrator, "DIR_OUTPUT", livro_falso["raiz"])
        ctx = extrator.contexto_da_obra(livro_falso["slug"])
        assert ctx["persona"] == "Mestre de Obras"
        assert ctx["senioridade"] == "intermediario"
        assert ctx["serie"] == "Colecao Teste"

    def test_estagio_cai_para_titulo_da_parte_sem_vocabulario(self, tmp_path, monkeypatch):
        raiz = tmp_path / "output"
        dir_livro = raiz / "livros" / "v3"
        (dir_livro / "capitulos").mkdir(parents=True)
        (dir_livro / "sumario_macro.json").write_text(json.dumps({
            "titulo_obra": "Obra V3",
            "partes": [{"titulo_parte": "Parte Um",
                        "capitulos": [{"capitulo": "1", "titulo": "C1"}]}],
        }), encoding="utf-8")
        monkeypatch.setattr(extrator, "DIR_OUTPUT", raiz)
        ctx = extrator.contexto_da_obra("livros/v3")
        assert ctx["estagios"][0]["nome"] == "Parte Um"


class TestCardCompleto:
    def test_gera_um_card_por_capitulo(self, extraido):
        assert len(extraido["cards"]) == 2
        assert [c["numero"] for c in extraido["cards"]] == ["01", "02"]

    def test_card_1_tem_as_sete_partes(self, extraido):
        c = extraido["cards"][0]
        assert c["objetivo"].startswith("Estabelecer os contratos")
        assert c["pre_requisito"] == "Nenhum — este é o ponto de partida"
        assert "scripts/contrato.py" in c["entregas"]
        assert c["execucao"]
        assert c["gate"]
        assert len(c["feito_quando"]) == 4
        assert len(c["armadilhas"]) == 3

    def test_gate_prioriza_comando_de_validacao(self, extraido):
        assert extraido["cards"][0]["gate"] == "python scripts/validar-contrato.py --estrito"

    def test_execucao_preserva_subtitulos_da_tecnica(self, extraido):
        titulos = [b["titulo"] for b in extraido["cards"][0]["execucao"]]
        assert titulos == ["Criar o arquivo de contrato", "Registrar no índice"]

    def test_pre_requisito_encadeia_do_card_anterior(self, extraido):
        assert extraido["cards"][1]["pre_requisito"] == "Passo 1 concluído"

    def test_referencia_cruzada_aponta_o_capitulo(self, extraido):
        assert extraido["cards"][0]["referencia_cruzada"] == "Cap. 1 — Fundação do Projeto"

    def test_card_nao_carrega_prosa_da_teoria(self, extraido):
        """R-PBK-0 na origem: nada da §2 Explica entra no card."""
        c = extraido["cards"][0]
        blob = json.dumps(c, ensure_ascii=False)
        assert "conjunto de contratos que o restante" not in blob


class TestCapituloIncompleto:
    def test_capitulo_sem_tecnica_gera_lacunas_nomeadas(self, extraido):
        c = extraido["cards"][1]
        assert "sem_secao_tecnica" in c["lacunas"]
        assert "sem_entregas" in c["lacunas"]
        assert "sem_gate" in c["lacunas"]

    def test_capitulo_incompleto_ainda_gera_card(self, extraido):
        c = extraido["cards"][1]
        assert c["numero"] == "02"
        assert c["objetivo"]      # veio do sumario, mesmo sem §4

    def test_relatorio_lista_lacunas_criticas(self, extraido):
        rel = extraido["relatorio"]
        assert "sem_secao_tecnica" in rel["lacunas_criticas"]
        assert [p["passo"] for p in rel["passos_com_lacuna"]] == ["02"]

    def test_cobertura_reflete_apenas_o_capitulo_bom(self, extraido):
        c = extraido["relatorio"]["cobertura"]
        assert c["com_entregas"] == 1
        assert c["com_gate"] == 1
        assert c["com_feito_quando"] == 1
        assert c["com_armadilhas"] == 1


class TestArtefatosGravados:
    def test_grava_um_json_por_passo(self, extraido):
        arquivos = sorted(p.name for p in (extraido["dir"] / "passos").glob("*.json"))
        assert arquivos == ["passo_01.json", "passo_02.json"]

    def test_grava_relatorio_de_extracao(self, extraido):
        caminho = extraido["dir"] / "revisao" / "relatorio_extracao.json"
        assert json.loads(caminho.read_text(encoding="utf-8"))["total_passos"] == 2

    def test_monta_playbook_md_com_as_sete_partes(self, extraido):
        md = (extraido["dir"] / "playbook.md").read_text(encoding="utf-8")
        for marcador in ("① Objetivo", "② Pré-requisito", "③ Entregas",
                         "④ Execução", "⑤ Verificação", "⑥ Feito quando",
                         "⑦ Armadilhas"):
            assert marcador in md

    def test_playbook_md_traz_mapa_de_estagios(self, extraido):
        md = (extraido["dir"] / "playbook.md").read_text(encoding="utf-8")
        assert "# Mapa dos Estágios" in md
        assert "Fundação" in md

    def test_playbook_md_traz_checklist_mestre(self, extraido):
        md = (extraido["dir"] / "playbook.md").read_text(encoding="utf-8")
        assert "# Checklist Mestre" in md

    def test_sem_montar_nao_cria_o_markdown(self, livro_falso, monkeypatch):
        monkeypatch.setattr(extrator, "DIR_OUTPUT", livro_falso["raiz"])
        res = extrator.extrair(livro_falso["slug"], montar=False)
        assert not (res["dir"] / "playbook.md").exists()

    def test_e_idempotente(self, livro_falso, monkeypatch):
        monkeypatch.setattr(extrator, "DIR_OUTPUT", livro_falso["raiz"])
        a = extrator.extrair(livro_falso["slug"])
        b = extrator.extrair(livro_falso["slug"])
        assert a["cards"] == b["cards"]


class TestNomenclaturaDeCapitulo:
    """A fabrica grava cap_1.md (sem zero) e cap_01.md — os dois tem de funcionar,
    e a ordem tem de ser NUMERICA (cap_10 depois de cap_2, nao antes)."""

    @pytest.fixture
    def livro_sem_zero(self, livro_falso, monkeypatch):
        from conftest import CAPITULO_EITA
        dir_caps = livro_falso["dir_livro"] / "capitulos"
        for antigo in dir_caps.glob("cap_*.md"):
            antigo.unlink()
        for n in (1, 2, 10):
            (dir_caps / f"cap_{n}.md").write_text(
                CAPITULO_EITA.replace("Capítulo 1", f"Capítulo {n}"), encoding="utf-8")
        monkeypatch.setattr(extrator, "DIR_OUTPUT", livro_falso["raiz"])
        return livro_falso

    def test_ordem_e_numerica_e_numero_e_normalizado(self, livro_sem_zero):
        res = extrator.extrair(livro_sem_zero["slug"], montar=False)
        assert [c["numero"] for c in res["cards"]] == ["01", "02", "10"]

    def test_arquivos_de_passo_saem_com_dois_digitos(self, livro_sem_zero):
        res = extrator.extrair(livro_sem_zero["slug"], montar=False)
        nomes = sorted(p.name for p in (res["dir"] / "passos").glob("*.json"))
        assert nomes == ["passo_01.json", "passo_02.json", "passo_10.json"]

    def test_ignora_arquivos_auxiliares_com_underscore(self, livro_sem_zero):
        (livro_sem_zero["dir_livro"] / "capitulos" / "_cap_rascunho.md").write_text(
            "rascunho", encoding="utf-8")
        res = extrator.extrair(livro_sem_zero["slug"], montar=False)
        assert len(res["cards"]) == 3


class TestFalhas:
    def test_obra_sem_capitulos_devolve_none(self, tmp_path, monkeypatch):
        monkeypatch.setattr(extrator, "DIR_OUTPUT", tmp_path / "output")
        assert extrator.extrair("livros/inexistente") is None
