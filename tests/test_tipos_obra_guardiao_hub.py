"""Testes do guardiao de caminho (scripts/tipos_obra.py::_assert_dentro_do_hub).

Ver RTK 2026-08-13: `fatiar-obra.py --playbook` e `minerar-fontes-academicas.py`
ja gravaram artefato fora do hub da colecao por depender so da disciplina do
agente em usar `dir_obra`. Este guardiao estrutural substitui essa disciplina
por uma verificacao levantada em runtime.
"""

import pytest

import tipos_obra as TO


class TestAssertDentroDoHub:
    def test_permite_escrita_dentro_do_hub(self, tmp_path):
        base = tmp_path / "output"
        (base / "hub-x" / "livros").mkdir(parents=True)
        (base / "hub-x" / "livros" / "config_obra.json").write_text("{}", encoding="utf-8")

        # Nao deve levantar: artigos/... vive dentro do mesmo hub da mae.
        TO._assert_dentro_do_hub(base / "hub-x" / "artigos" / "algo", "livros/hub-x", base)

    def test_bloqueia_escrita_fora_do_hub(self, tmp_path):
        base = tmp_path / "output"
        (base / "hub-x" / "livros").mkdir(parents=True)
        (base / "hub-x" / "livros" / "config_obra.json").write_text("{}", encoding="utf-8")

        with pytest.raises(ValueError, match="fora do hub"):
            TO._assert_dentro_do_hub(base / "playbooks" / "algo", "livros/hub-x", base)

    def test_layout_plano_e_no_op(self, tmp_path):
        base = tmp_path / "output"
        (base / "livros" / "mae-plana").mkdir(parents=True)
        (base / "livros" / "mae-plana" / "config_obra.json").write_text("{}", encoding="utf-8")

        # Mae sem hub proprio: nao ha o que proteger, mesmo escrevendo numa
        # raiz de tipo diferente.
        TO._assert_dentro_do_hub(base / "artigos" / "algo", "livros/mae-plana", base)

    def test_mae_inexistente_nao_quebra(self, tmp_path):
        base = tmp_path / "output"
        base.mkdir(parents=True)
        # dir_obra cai no fallback plano (nao existe ainda) -> tratado como
        # layout plano, no-op.
        TO._assert_dentro_do_hub(base / "artigos" / "algo", "livros/nao-existe", base)


class TestResolverSlugMae:
    def test_prioriza_obra_mae(self):
        cfg = {"obra_mae": "livro-a", "livro_mae": "livro-b"}
        assert TO.resolver_slug_mae(cfg) == "livro-a"

    def test_fallback_para_livro_mae(self):
        cfg = {"livro_mae": "livro-b"}
        assert TO.resolver_slug_mae(cfg) == "livro-b"

    def test_none_quando_ausente(self):
        assert TO.resolver_slug_mae({}) is None
        assert TO.resolver_slug_mae(None) is None
