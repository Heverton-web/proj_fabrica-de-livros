"""Testes para scripts/validar-fontes.py (gate F2 — hierarquia A/B/C do dossiê)."""

import importlib.util
import sys
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "validar_fontes",
    Path(__file__).resolve().parent.parent / "scripts" / "validar-fontes.py",
)
vf = importlib.util.module_from_spec(_spec)
sys.modules["validar_fontes"] = vf
_spec.loader.exec_module(vf)


class TestClassificarDossie:
    def test_marcador_no_fim_da_linha(self):
        texto = (
            "- AUTOR. Título. Disponível em: https://arxiv.org/abs/1. Acesso em: 10 ago. 2026. (A)\n"
            "- AUTOR2. Docs. Disponível em: https://docs.exemplo.com. Acesso em: 10 ago. 2026. (B)\n"
            "- BLOG. Post. Disponível em: https://blog.exemplo.com. Acesso em: 10 ago. 2026. (C)\n"
        )
        classes, linhas = vf.classificar_dossie(texto)
        assert classes == {"A": 1, "B": 1, "C": 1}
        assert linhas == 3

    def test_marcador_em_linha_propria(self):
        texto = (
            "- AUTOR. Título. Disponível em: https://x.org/1.\n"
            "**Classe:** A\n"
        )
        classes, _ = vf.classificar_dossie(texto)
        assert classes == {"A": 1, "B": 0, "C": 0}

    def test_sem_classificacao(self):
        texto = "- AUTOR. Título. Disponível em: https://x.org/1.\n"
        classes, linhas = vf.classificar_dossie(texto)
        assert classes == {"A": 0, "B": 0, "C": 0}
        assert linhas == 1


class TestValidar:
    def test_conforme_70_ab(self, tmp_path):
        dir_obra = tmp_path / "obra"
        (dir_obra / "pesquisa").mkdir(parents=True)
        (dir_obra / "pesquisa" / "dossie.md").write_text(
            "- A1. Disponível em: https://arxiv.org/1. (A)\n"
            "- A2. Disponível em: https://arxiv.org/2. (A)\n"
            "- B1. Disponível em: https://docs.exemplo.com. (B)\n"
            "- C1. Disponível em: https://blog.exemplo.com. (C)\n",
            encoding="utf-8")
        rel = vf.validar(dir_obra)
        assert rel["status"] == "conforme"
        assert rel["proporcao_ab"] >= 0.70
        assert rel["violacoes"] == []

    def test_falha_menos_de_70(self, tmp_path):
        dir_obra = tmp_path / "obra"
        (dir_obra / "pesquisa").mkdir(parents=True)
        (dir_obra / "pesquisa" / "dossie.md").write_text(
            "- B1. Disponível em: https://docs.exemplo.com. (B)\n"
            "- C1. Disponível em: https://blog.exemplo.com. (C)\n"
            "- C2. Disponível em: https://blog2.exemplo.com. (C)\n",
            encoding="utf-8")
        rel = vf.validar(dir_obra)
        assert rel["status"] == "falha"
        assert any(v["regra"] == "R-FT-1" for v in rel["violacoes"])

    def test_sem_classificacao_nao_reprova(self, tmp_path):
        """R-FT-2: dossiê antigo sem marcadores => nao_verificado, não falha."""
        dir_obra = tmp_path / "obra"
        (dir_obra / "pesquisa").mkdir(parents=True)
        (dir_obra / "pesquisa" / "dossie.md").write_text(
            "- AUTOR. Título. Disponível em: https://x.org/1.\n",
            encoding="utf-8")
        rel = vf.validar(dir_obra)
        assert rel["status"] == "nao_verificado"
        assert any(v["regra"] == "R-FT-2" for v in rel["violacoes"])

    def test_sem_dossie_nao_reprova(self, tmp_path):
        dir_obra = tmp_path / "obra"
        dir_obra.mkdir()
        rel = vf.validar(dir_obra)
        assert rel["status"] == "nao_verificado"

    def test_fontes_nao_classificadas_nao_contam(self, tmp_path):
        """R-FT-3: linha de fonte sem marcador não entra na proporção."""
        dir_obra = tmp_path / "obra"
        (dir_obra / "pesquisa").mkdir(parents=True)
        (dir_obra / "pesquisa" / "dossie.md").write_text(
            "- A1. Disponível em: https://arxiv.org/1. (A)\n"
            "- A2. Disponível em: https://arxiv.org/2. (A)\n"
            "- SEM MARCADOR. Disponível em: https://x.org/3.\n",
            encoding="utf-8")
        rel = vf.validar(dir_obra)
        assert rel["status"] == "conforme"
        assert rel["classificadas"] == 2
        assert rel["linhas_fonte_total"] == 3
