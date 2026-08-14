"""Testes para scripts/corrigir-mecanico.py (correções mecânicas do revisor-tecnico)."""

import importlib.util
import sys
from pathlib import Path

DIR_PROJETO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR_PROJETO / "scripts"))

_spec = importlib.util.spec_from_file_location(
    "corrigir_mecanico", DIR_PROJETO / "scripts" / "corrigir-mecanico.py"
)
cm = importlib.util.module_from_spec(_spec)
sys.modules["corrigir_mecanico"] = cm
_spec.loader.exec_module(cm)


class TestRemoverHrSolto:
    def test_remove_hr_solto_no_corpo(self):
        texto = "## 1. Introdução\n\ntexto\n\n---\n\nmais texto\n"
        novo, n = cm.remover_hr_solto(texto)
        assert n == 1
        assert "---" not in novo

    def test_preserva_frontmatter(self):
        texto = "---\ntitulo: x\n---\n\n## 1. Introdução\ntexto\n"
        novo, n = cm.remover_hr_solto(texto)
        assert n == 0
        assert novo.startswith("---\ntitulo: x\n---\n")

    def test_preserva_hr_dentro_de_bloco_de_codigo(self):
        texto = "## 4. Técnica\n```text\n---\n```\n"
        novo, n = cm.remover_hr_solto(texto)
        assert n == 0
        assert "---" in novo

    def test_remove_varias_ocorrencias(self):
        texto = "a\n---\nb\n***\nc\n___\nd\n"
        novo, n = cm.remover_hr_solto(texto)
        assert n == 3


class TestRenumerarCitacoes:
    def _capitulo(self, corpo_intro, refs):
        return (
            f"## 1. Introdução\n{corpo_intro}\n\n"
            f"## 7. Referências Bibliográficas\n{refs}\n"
        )

    def test_renumera_bijecao_com_gap(self):
        texto = self._capitulo(
            "Fato citado [1] e outro [4].",
            "[1] A. *X*.\n[4] B. *Y*.",
        )
        r = cm.renumerar_citacoes(texto)
        assert r["renumerado"] is True
        assert r["mapa"] == {1: 1, 4: 2}
        assert "[2]" in r["texto"]
        assert "[4]" not in r["texto"]

    def test_nao_altera_quando_ja_sequencial(self):
        texto = self._capitulo("[1] e [2]", "[1] A. *X*.\n[2] B. *Y*.")
        r = cm.renumerar_citacoes(texto)
        assert r["renumerado"] is False
        assert r["texto"] == texto

    def test_reporta_orfa_sem_alterar(self):
        texto = self._capitulo("[1] e [5]", "[1] A. *X*.")
        r = cm.renumerar_citacoes(texto)
        assert r["renumerado"] is False
        assert r["orfas"] == [5]
        assert r["texto"] == texto

    def test_reporta_nao_citada_sem_alterar(self):
        texto = self._capitulo("[1]", "[1] A. *X*.\n[2] B. *Y*.")
        r = cm.renumerar_citacoes(texto)
        assert r["renumerado"] is False
        assert r["nao_citadas"] == [2]


class TestDetectarVariantesTermo:
    def test_detecta_grafia_inconsistente(self):
        textos = [
            "O sistema híbrido é ótimo. hibrido também aparece aqui. "
            "híbrido mais uma vez. E hibrido de novo.",
        ]
        achados = cm.detectar_variantes_termo(textos, minimo_ocorrencias=4)
        chaves = [c for c, _ in achados]
        assert "hibrido" in chaves

    def test_ignora_variacao_de_caixa_inicial_de_frase(self):
        textos = ["Python é ótimo. Python continua ótimo. Python de novo. Python outra vez."]
        achados = cm.detectar_variantes_termo(textos, minimo_ocorrencias=4)
        assert achados == []

    def test_ignora_termo_raro(self):
        textos = ["Kubernetes e kubernetes aparecem só 1 vez cada."]
        achados = cm.detectar_variantes_termo(textos, minimo_ocorrencias=4)
        assert achados == []


class TestAplicarGrafiaCanonica:
    def test_substitui_pela_forma_mais_frequente(self):
        achados = [("mcp", {"MCP": 5, "Mcp": 1})]
        texto = "Hoje o Mcp é usado. O MCP é o padrão. MCP MCP MCP."
        novo, n = cm.aplicar_grafia_canonica(texto, achados)
        assert "Mcp" not in novo
        assert n == 1

    def test_nao_altera_dentro_de_bloco_de_codigo(self):
        achados = [("mcp", {"MCP": 5, "Mcp": 1})]
        texto = "Texto MCP MCP MCP MCP.\n```python\nvar = Mcp\n```\n"
        novo, n = cm.aplicar_grafia_canonica(texto, achados)
        assert "var = Mcp" in novo
        assert n == 0


class TestCorrigirObra:
    def test_corrige_hr_e_grava_arquivo(self, tmp_path):
        base = tmp_path / "output"
        dir_cap = base / "livros" / "x" / "capitulos"
        dir_cap.mkdir(parents=True)
        (dir_cap / "cap_1.md").write_text(
            "## 1. Introdução\ntexto\n\n---\n\nmais\n\n## 7. Referências Bibliográficas\n[1] A. *X*.\n",
            encoding="utf-8",
        )
        resultado = cm.corrigir_obra("livros/x", base=base)
        assert resultado["capitulos"][0]["hr_removidas"] == 1
        assert "---" not in (dir_cap / "cap_1.md").read_text(encoding="utf-8")

    def test_dry_run_nao_grava(self, tmp_path):
        base = tmp_path / "output"
        dir_cap = base / "livros" / "x" / "capitulos"
        dir_cap.mkdir(parents=True)
        original = "## 1. Introdução\ntexto\n\n---\n\nmais\n"
        (dir_cap / "cap_1.md").write_text(original, encoding="utf-8")
        cm.corrigir_obra("livros/x", dry_run=True, base=base)
        assert (dir_cap / "cap_1.md").read_text(encoding="utf-8") == original

    def test_filtro_por_capitulo_so_toca_1_arquivo(self, tmp_path):
        base = tmp_path / "output"
        dir_cap = base / "livros" / "x" / "capitulos"
        dir_cap.mkdir(parents=True)
        texto_com_hr = "## 1. Introdução\ntexto\n\n---\n\nmais\n"
        (dir_cap / "cap_1.md").write_text(texto_com_hr, encoding="utf-8")
        (dir_cap / "cap_2.md").write_text(texto_com_hr, encoding="utf-8")
        cm.corrigir_obra("livros/x", capitulo=1, base=base)
        assert "---" not in (dir_cap / "cap_1.md").read_text(encoding="utf-8")
        assert "---" in (dir_cap / "cap_2.md").read_text(encoding="utf-8")

    def test_sem_capitulos_devolve_vazio(self, tmp_path):
        resultado = cm.corrigir_obra("livros/inexistente", base=tmp_path / "output")
        assert resultado["capitulos"] == []
