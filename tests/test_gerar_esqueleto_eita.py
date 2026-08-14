"""Testes para scripts/gerar-esqueleto-eita.py (esqueleto EITA-V2 fixo)."""

import importlib.util
import sys
from pathlib import Path

DIR_PROJETO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR_PROJETO / "scripts"))

_spec = importlib.util.spec_from_file_location(
    "gerar_esqueleto_eita", DIR_PROJETO / "scripts" / "gerar-esqueleto-eita.py"
)
ge = importlib.util.module_from_spec(_spec)
sys.modules["gerar_esqueleto_eita"] = ge
_spec.loader.exec_module(ge)

import secoes_eita as SE
import tipos_obra as TO


class TestMontarEsqueleto:
    def test_contem_titulo_do_capitulo(self):
        texto = ge.montar_esqueleto(3, "Memória Distribuída")
        assert texto.startswith("# Capítulo 3: Memória Distribuída")

    def test_7_secoes_reconhecidas_por_secoes_eita(self):
        texto = ge.montar_esqueleto(1, "Título Qualquer")
        secoes = SE.dividir_secoes(texto)
        assert set(secoes.keys()) == {1, 2, 3, 4, 5, 6, 7}

    def test_secao_por_nome_reconhece_todas(self):
        texto = ge.montar_esqueleto(1, "X")
        secoes = SE.dividir_secoes(texto)
        for apelido in ("introducao", "explica", "ilustra", "tecnica", "aplica", "conclusao", "referencias"):
            assert SE.secao_por_nome(secoes, apelido) != ""

    def test_exercicio_checklist_presente_na_aplica(self):
        texto = ge.montar_esqueleto(1, "X")
        secoes = SE.dividir_secoes(texto)
        assert "- [ ]" in SE.secao_por_nome(secoes, "aplica")


class TestMain:
    def test_grava_arquivo_no_dir_obra(self, tmp_path, monkeypatch):
        base = tmp_path / "output"
        (base / "livros" / "meu-livro" / "capitulos").mkdir(parents=True)
        monkeypatch.setattr(ge, "DIR_OUTPUT", base)
        monkeypatch.setattr(sys, "argv", ["gerar-esqueleto-eita.py", "livros/meu-livro", "1", "--titulo", "Início"])
        assert ge.main() == 0
        destino = base / "livros" / "meu-livro" / "capitulos" / "cap_1.md"
        assert destino.is_file()
        assert "# Capítulo 1: Início" in destino.read_text(encoding="utf-8")

    def test_nao_sobrescreve_sem_forcar(self, tmp_path, monkeypatch):
        base = tmp_path / "output"
        dir_cap = base / "livros" / "x" / "capitulos"
        dir_cap.mkdir(parents=True)
        (dir_cap / "cap_1.md").write_text("conteudo original", encoding="utf-8")
        monkeypatch.setattr(ge, "DIR_OUTPUT", base)
        monkeypatch.setattr(sys, "argv", ["gerar-esqueleto-eita.py", "livros/x", "1", "--titulo", "T"])
        assert ge.main() == 1
        assert (dir_cap / "cap_1.md").read_text(encoding="utf-8") == "conteudo original"

    def test_forcar_sobrescreve(self, tmp_path, monkeypatch):
        base = tmp_path / "output"
        dir_cap = base / "livros" / "x" / "capitulos"
        dir_cap.mkdir(parents=True)
        (dir_cap / "cap_1.md").write_text("conteudo original", encoding="utf-8")
        monkeypatch.setattr(ge, "DIR_OUTPUT", base)
        monkeypatch.setattr(sys, "argv", ["gerar-esqueleto-eita.py", "livros/x", "1", "--titulo", "Novo", "--forcar"])
        assert ge.main() == 0
        assert "Novo" in (dir_cap / "cap_1.md").read_text(encoding="utf-8")
