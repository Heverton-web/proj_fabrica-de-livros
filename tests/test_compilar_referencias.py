"""Testes para scripts/compilar-referencias.py (No 7 - dedup determinístico)."""

import importlib.util
import sys
from pathlib import Path

import pytest

_spec = importlib.util.spec_from_file_location(
    "compilar_referencias",
    Path(__file__).resolve().parent.parent / "scripts" / "compilar-referencias.py",
)
cr = importlib.util.module_from_spec(_spec)
sys.modules["compilar_referencias"] = cr
_spec.loader.exec_module(cr)


class TestNormalizarUrl:
    def test_ignora_protocolo(self):
        assert cr.normalizar_url("https://x.com/a") == cr.normalizar_url("http://x.com/a")

    def test_ignora_barra_final(self):
        assert cr.normalizar_url("https://x.com/a/") == cr.normalizar_url("https://x.com/a")

    def test_ignora_maiusculas(self):
        assert cr.normalizar_url("https://X.com/A") == cr.normalizar_url("https://x.com/a")


class TestParsearLinha:
    def test_linha_completa_com_classe(self):
        linha = (
            "- ANTHROPIC. *Introducing the Model Context Protocol*. "
            "Disponível em: https://www.anthropic.com/news/model-context-protocol. "
            "Acesso em: 28 jul. 2026. (B)"
        )
        fonte = cr.parsear_linha(linha)
        assert fonte["autor"] == "ANTHROPIC"
        assert fonte["titulo"] == "Introducing the Model Context Protocol"
        assert fonte["url"] == "https://www.anthropic.com/news/model-context-protocol"
        assert fonte["acesso"] == "28 jul. 2026"
        assert fonte["classe"] == "B"

    def test_linha_sem_classe(self):
        linha = "- PRINCETON UNIVERSITY. *SWE-bench*. Disponível em: https://www.swebench.com. Acesso em: 28 jul. 2026."
        fonte = cr.parsear_linha(linha)
        assert fonte["classe"] == ""
        assert fonte["url"] == "https://www.swebench.com"

    def test_linha_fora_do_formato_retorna_none(self):
        assert cr.parsear_linha("- link solto sem formato ABNT") is None

    def test_linha_vazia_retorna_none(self):
        assert cr.parsear_linha("") is None


class TestExtrairSecaoFontes:
    def test_isola_secao_ate_eof(self):
        texto = (
            "## Conceitos-chave\n- x\n\n"
            "## Fontes brutas (para Nó 7)\n"
            "- A. *B*. Disponível em: https://a.com. Acesso em: 1 jan. 2026.\n"
        )
        secao = cr.extrair_secao_fontes(texto)
        assert "Fontes brutas" not in secao
        assert "https://a.com" in secao

    def test_isola_secao_antes_do_proximo_heading(self):
        texto = (
            "## Fontes brutas\n"
            "- A. *B*. Disponível em: https://a.com. Acesso em: 1 jan. 2026.\n"
            "## Outra Coisa\n- ignorar isso\n"
        )
        secao = cr.extrair_secao_fontes(texto)
        assert "https://a.com" in secao
        assert "ignorar isso" not in secao

    def test_sem_secao_retorna_vazio(self):
        assert cr.extrair_secao_fontes("# Dossiê\nsem fontes aqui") == ""


class TestDeduplicar:
    def _fonte(self, url, classe=""):
        return {"autor": "A", "titulo": "T", "url": url, "acesso": "1 jan. 2026", "classe": classe}

    def test_remove_duplicata_por_url_normalizada(self):
        fontes = [self._fonte("https://x.com/a"), self._fonte("http://x.com/a/")]
        assert len(cr.deduplicar(fontes)) == 1

    def test_mantem_fontes_distintas(self):
        fontes = [self._fonte("https://x.com/a"), self._fonte("https://x.com/b")]
        assert len(cr.deduplicar(fontes)) == 2

    def test_promove_classe_da_duplicata(self):
        fontes = [self._fonte("https://x.com/a", classe=""), self._fonte("https://x.com/a", classe="A")]
        unicas = cr.deduplicar(fontes)
        assert len(unicas) == 1
        assert unicas[0]["classe"] == "A"

    def test_nao_sobrescreve_classe_ja_definida(self):
        fontes = [self._fonte("https://x.com/a", classe="B"), self._fonte("https://x.com/a", classe="A")]
        assert cr.deduplicar(fontes)[0]["classe"] == "B"


class TestOrdenarAlfabetico:
    def test_ordena_por_autor_depois_titulo(self):
        fontes = [
            {"autor": "ZETA", "titulo": "T", "url": "u1", "acesso": "a", "classe": ""},
            {"autor": "ALFA", "titulo": "T", "url": "u2", "acesso": "a", "classe": ""},
        ]
        ordenadas = cr.ordenar_alfabetico(fontes)
        assert [f["autor"] for f in ordenadas] == ["ALFA", "ZETA"]


class TestCompilarIntegracao:
    def test_dedup_entre_dois_dossies(self, tmp_path, monkeypatch):
        base = tmp_path / "output"
        dir_obra = base / "livros" / "meu-livro"
        dir_pesquisa = dir_obra / "pesquisa"
        dir_pesquisa.mkdir(parents=True)

        (dir_pesquisa / "dossie_a.md").write_text(
            "## Fontes brutas\n"
            "- ANTHROPIC. *MCP*. Disponível em: https://anthropic.com/mcp. Acesso em: 1 jan. 2026. (B)\n",
            encoding="utf-8",
        )
        (dir_pesquisa / "dossie_b.md").write_text(
            "## Fontes brutas\n"
            "- ANTHROPIC. *MCP*. Disponível em: https://anthropic.com/mcp/. Acesso em: 2 jan. 2026.\n"
            "- OUTRA FONTE. *X*. Disponível em: https://outra.com/x. Acesso em: 2 jan. 2026. (A)\n",
            encoding="utf-8",
        )

        import tipos_obra as TO
        monkeypatch.setattr(TO, "DIR_OUTPUT", base)
        monkeypatch.setattr(cr, "DIR_OUTPUT", base)

        unicas, nao_parseadas, total_bruto = cr.compilar("livros/meu-livro", base=base)

        assert total_bruto == 3
        assert len(unicas) == 2
        assert nao_parseadas == []
        anthropic = next(f for f in unicas if f["autor"] == "ANTHROPIC")
        assert anthropic["classe"] == "B"  # promovida da 1a ocorrencia

    def test_reporta_linha_nao_parseada(self, tmp_path):
        base = tmp_path / "output"
        dir_pesquisa = base / "livros" / "x" / "pesquisa"
        dir_pesquisa.mkdir(parents=True)
        (dir_pesquisa / "dossie_x.md").write_text(
            "## Fontes brutas\n- fonte fora do formato\n", encoding="utf-8"
        )
        unicas, nao_parseadas, total_bruto = cr.compilar("livros/x", base=base)
        assert total_bruto == 0
        assert len(nao_parseadas) == 1
