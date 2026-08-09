"""Testes do scripts/series_capa.py --reindexar (V5.2, HUB POR COLEÇÃO).

A reindexação reconstrói `membros` do registro de cores com os slugs REAIS no
disco (varredura via tipos_obra.listar_materiais), preservando as cores já
gravadas e eliminando membros órfãos de layouts antigos (ex.: destinos planos
`livros/<slug>`). Chaves sem material no disco mantêm a cor reservada com
membros vazios.
"""

import json
from pathlib import Path

import pytest

import series_capa as sc


@pytest.fixture
def hub_falso(tmp_path, monkeypatch):
    """Output isolado com 2 hubs: um com 2 materiais na mesma coleção e um
    standalone (sem serie) que deve entrar como chave nova no registro."""
    raiz = tmp_path / "output"
    raiz.mkdir()

    def _material(rel, config):
        p = raiz / rel
        p.mkdir(parents=True)
        (p / "config_obra.json").write_text(
            json.dumps(config, ensure_ascii=False), encoding="utf-8")

    _material("minha-colecao/livros/obra-a", {"serie": "minha-colecao"})
    _material("minha-colecao/ebooks/obra-a--eb-01-x", {"serie": "minha-colecao"})
    _material("outra-colecao/tccs/tcc-x", {})

    monkeypatch.setattr(sc, "DIR_OUTPUT", raiz)
    monkeypatch.setattr(sc, "CAMINHO_REGISTRO", raiz / "series.json")
    (raiz / "series.json").write_text(json.dumps({
        "minha-colecao": {"cor": "#58a6ff", "membros": ["livros/obra-antiga"]},
        "colecao-morta": {"cor": "#2ecc9a", "membros": ["livros/orfao"]},
    }, ensure_ascii=False), encoding="utf-8")
    return raiz


class TestReindexar:
    def test_preserva_cores_e_substitui_membros(self, hub_falso):
        novo = sc.reindexar_membros(hub_falso)
        assert novo["minha-colecao"]["cor"] == "#58a6ff"
        assert novo["minha-colecao"]["membros"] == [
            "minha-colecao/ebooks/obra-a--eb-01-x",
            "minha-colecao/livros/obra-a",
        ]

    def test_membro_orfao_eliminado(self, hub_falso):
        novo = sc.reindexar_membros(hub_falso)
        for entrada in novo.values():
            for m in entrada["membros"]:
                assert (hub_falso / m / "config_obra.json").exists(), \
                    f"membro orfao na reindexacao: {m}"

    def test_chave_sem_material_fica_com_membros_vazios_e_cor(self, hub_falso):
        novo = sc.reindexar_membros(hub_falso)
        assert novo["colecao-morta"]["cor"] == "#2ecc9a"
        assert novo["colecao-morta"]["membros"] == []

    def test_entrada_nova_para_material_sem_registro(self, hub_falso):
        novo = sc.reindexar_membros(hub_falso)
        # config sem "serie"/"livro_mae" -> serie_key = nome do slug
        assert novo["tcc-x"]["membros"] == ["outra-colecao/tccs/tcc-x"]
        assert novo["tcc-x"]["cor"] in sc.PALETA_ACCENT

    def test_idempotente(self, hub_falso):
        primeiro = sc.reindexar_membros(hub_falso)
        segundo = sc.reindexar_membros(hub_falso)
        assert primeiro == segundo
