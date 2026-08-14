"""Testes para scripts/classificar-fonte.py (classificação A/B/C por domínio)."""

import importlib.util
import sys
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "classificar_fonte",
    Path(__file__).resolve().parent.parent / "scripts" / "classificar-fonte.py",
)
cf = importlib.util.module_from_spec(_spec)
sys.modules["classificar_fonte"] = cf
_spec.loader.exec_module(cf)


class TestClassificar:
    def test_arxiv_e_classe_a(self):
        assert cf.classificar("https://arxiv.org/abs/2302.00000") == "A"

    def test_acm_e_classe_a(self):
        assert cf.classificar("https://dl.acm.org/doi/10.1145/123") == "A"

    def test_docs_e_classe_b(self):
        assert cf.classificar("https://docs.anthropic.com/en/mcp") == "B"

    def test_gov_e_classe_b(self):
        assert cf.classificar("https://something.gov/report") == "B"

    def test_blog_path_e_classe_c(self):
        assert cf.classificar("https://empresa.com/blog/post-1") == "C"

    def test_medium_e_classe_c(self):
        assert cf.classificar("https://medium.com/@alguem/post") == "C"

    def test_dominio_desconhecido_e_ambiguo(self):
        assert cf.classificar("https://blogpessoaldesconhecido123.io/x") is None

    def test_url_vazia_e_ambigua(self):
        assert cf.classificar("") is None


class TestPreencherClasseNoTexto:
    def test_preenche_linha_reconhecida_sem_classe(self):
        texto = "- ANTHROPIC. *MCP*. Disponível em: https://arxiv.org/abs/1. Acesso em: 1 jan. 2026."
        novo, n_pre, n_amb = cf.preencher_classe_no_texto(texto)
        assert novo.rstrip().endswith("(A)")
        assert n_pre == 1
        assert n_amb == 0

    def test_nao_altera_linha_ja_classificada(self):
        texto = "- X. *Y*. Disponível em: https://arxiv.org/abs/1. Acesso em: 1 jan. 2026. (C)"
        novo, n_pre, n_amb = cf.preencher_classe_no_texto(texto)
        assert novo == texto
        assert n_pre == 0

    def test_conta_ambigua_sem_alterar(self):
        texto = "- X. *Y*. Disponível em: https://desconhecido123.io/a. Acesso em: 1 jan. 2026."
        novo, n_pre, n_amb = cf.preencher_classe_no_texto(texto)
        assert novo == texto
        assert n_amb == 1

    def test_ignora_linha_sem_url(self):
        texto = "- livro impresso sem url"
        novo, n_pre, n_amb = cf.preencher_classe_no_texto(texto)
        assert (n_pre, n_amb) == (0, 0)


class TestAplicarNaObra:
    def test_preenche_e_grava_arquivo(self, tmp_path):
        base = tmp_path / "output"
        dir_pesquisa = base / "livros" / "x" / "pesquisa"
        dir_pesquisa.mkdir(parents=True)
        arq = dir_pesquisa / "dossie_x.md"
        arq.write_text(
            "## Fontes brutas\n"
            "- A. *B*. Disponível em: https://arxiv.org/abs/1. Acesso em: 1 jan. 2026.\n",
            encoding="utf-8",
        )
        resumo = cf.aplicar_na_obra("livros/x", base=base)
        assert resumo["dossie_x.md"] == (1, 0)
        assert "(A)" in arq.read_text(encoding="utf-8")

    def test_sem_dossies_retorna_vazio(self, tmp_path):
        assert cf.aplicar_na_obra("livros/inexistente", base=tmp_path / "output") == {}
