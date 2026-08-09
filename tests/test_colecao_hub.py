"""Testes da resolucao de manifestos por HUB (V5.2) do scripts/colecao.py.

Cada colecao grava o manifesto no hub da propria colecao
(output/<hub>/colecoes/<nome>.json); colecoes sem hub usam o fallback plano
(DIR_COLECOES). Os metadados ricos do artefato legado <hub>/series.json sao
fundidos no manifesto e o arquivo e removido (idempotente).
"""

import json

import pytest

import series_capa as sc
from conftest import carregar_script

import tipos_obra as TO

colecao = carregar_script("colecao.py")


@pytest.fixture
def ambiente(tmp_path, monkeypatch):
    raiz = tmp_path / "output"
    raiz.mkdir()

    def _material(rel, config):
        p = raiz / rel
        p.mkdir(parents=True)
        (p / "config_obra.json").write_text(
            json.dumps(config, ensure_ascii=False), encoding="utf-8")
        (p / "sumario_macro.json").write_text(
            json.dumps({"titulo_obra": rel.split("/")[-1],
                        "motivo_condutor": {"nome": "O Fio"}}),
            encoding="utf-8")

    # Colecao com hub proprio (2 materiais no mesmo hub)
    _material("meu-hub/livros/l1-x", {"serie": "Minha Coleção"})
    _material("meu-hub/ebooks/ebk-1-x", {"serie": "Minha Coleção"})
    # Colecao sem hub (layout plano)
    _material("livros/l2-y", {"serie": "Colecao Plana"})
    # Metadados ricos legados dentro do hub
    (raiz / "meu-hub" / "series.json").write_text(json.dumps({
        "nome": "Minha Coleção",
        "subtitulo": "Subtítulo",
        "slug": "meu-hub",
        "tema": "Tema da coleção",
        "objetivo": "Objetivo",
        "livros": [{"indice": 1, "slug": "l1-x"}],
        "metricas": {"total_livros": 1},
    }, ensure_ascii=False), encoding="utf-8")

    monkeypatch.setattr(colecao, "DIR_OUTPUT", raiz)
    monkeypatch.setattr(colecao, "DIR_COLECOES", raiz / "colecoes")
    monkeypatch.setattr(sc, "DIR_OUTPUT", raiz)
    monkeypatch.setattr(sc, "CAMINHO_REGISTRO", raiz / "series.json")
    return raiz


class TestManifestoPorHub:
    def test_manifesto_da_colecao_vai_para_o_proprio_hub(self, ambiente):
        colecao.sincronizar()
        caminho = ambiente / "meu-hub" / "colecoes" / f"{colecao._slug_arquivo('Minha Coleção')}.json"
        assert caminho.exists(), "manifesto deveria viver no hub da colecao"
        manifesto = json.loads(caminho.read_text(encoding="utf-8"))
        assert manifesto["colecao"] == "Minha Coleção"
        assert manifesto["total_membros"] == 2
        assert manifesto["por_tipo"] == {"ebook": 1, "livro": 1}

    def test_colecao_sem_hub_usa_fallback_plano(self, ambiente):
        colecao.sincronizar()
        caminho = ambiente / "colecoes" / "colecao-plana.json"
        assert caminho.exists()
        assert json.loads(caminho.read_text(encoding="utf-8"))["colecao"] == "Colecao Plana"

    def test_metadados_ricos_fundidos_e_legado_removido(self, ambiente):
        colecao.sincronizar()
        manifesto = json.loads(
            (ambiente / "meu-hub" / "colecoes" / f"{colecao._slug_arquivo('Minha Coleção')}.json")
            .read_text(encoding="utf-8"))
        assert manifesto["metadados"]["nome"] == "Minha Coleção"
        assert manifesto["metadados"]["metricas"]["total_livros"] == 1
        assert not (ambiente / "meu-hub" / "series.json").exists(), \
            "series.json do hub deve sumir apos a fusao"

    def test_idempotente_sem_legado(self, ambiente):
        colecao.sincronizar()
        primeiro = json.loads(
            (ambiente / "meu-hub" / "colecoes" / f"{colecao._slug_arquivo('Minha Coleção')}.json")
            .read_text(encoding="utf-8"))
        colecao.sincronizar()
        segundo = json.loads(
            (ambiente / "meu-hub" / "colecoes" / f"{colecao._slug_arquivo('Minha Coleção')}.json")
            .read_text(encoding="utf-8"))
        assert segundo["metadados"] == primeiro["metadados"], \
            "metadados devem sobreviver ao 2o sincronizar (sem series.json no hub)"

    def test_carregar_acha_manifesto_no_hub(self, ambiente):
        colecao.sincronizar()
        manifesto = colecao.carregar("Minha Coleção")
        assert manifesto is not None
        assert manifesto["nucleo"]["slug"] == "meu-hub/livros/l1-x"

    def test_limpeza_global_remove_manifesto_de_chave_morta(self, ambiente):
        (ambiente / "colecoes").mkdir(parents=True, exist_ok=True)
        (ambiente / "colecoes" / "colecao-morta.json").write_text(
            json.dumps({"colecao": "Colecao Morta"}), encoding="utf-8")
        (ambiente / "meu-hub" / "colecoes").mkdir(parents=True, exist_ok=True)
        (ambiente / "meu-hub" / "colecoes" / "outra-morta.json").write_text(
            json.dumps({"colecao": "Outra Morta"}), encoding="utf-8")
        colecao.sincronizar()
        assert not (ambiente / "colecoes" / "colecao-morta.json").exists()
        assert not (ambiente / "meu-hub" / "colecoes" / "outra-morta.json").exists()
