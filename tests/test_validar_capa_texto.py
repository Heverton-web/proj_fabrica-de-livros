"""Testes para scripts/validar-capa-texto.py"""

import importlib.util
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

_spec = importlib.util.spec_from_file_location(
    "validar_capa_texto",
    Path(__file__).resolve().parent.parent / "scripts" / "validar-capa-texto.py",
)
vct = importlib.util.module_from_spec(_spec)
sys.modules["validar_capa_texto"] = vct
_spec.loader.exec_module(vct)


class TestQuebrarLinhas:
    """Testa a simulacao de quebra de linha greedy."""

    def _fonte_mock(self, largura_max=500):
        """Cria um mock de fonte que mede largura por len(palavra) * 10."""
        fonte = MagicMock()
        def getlength(texto):
            return sum(len(p) * 10 for p in texto.split())
        fonte.getlength = getlength
        return fonte

    def test_texto_curto_uma_linha(self):
        fonte = self._fonte_mock()
        linhas = vct.quebrar_linhas("Ola Mundo", fonte, 500)
        assert len(linhas) == 1
        assert linhas[0] == ["Ola", "Mundo"]

    def test_texto_longo_multiplas_linhas(self):
        fonte = self._fonte_mock(largura_max=30)
        linhas = vct.quebrar_linhas("Uma frase bem longa para testar", fonte, 30)
        assert len(linhas) > 1

    def test玩家朋友_vazio(self):
        fonte = self._fonte_mock()
        linhas = vct.quebrar_linhas("", fonte, 500)
        assert linhas == []

    def test_uma_só_palavra(self):
        fonte = self._fonte_mock()
        linhas = vct.quebrar_linhas("Python", fonte, 500)
        assert len(linhas) == 1
        assert linhas[0] == ["Python"]


class TestValidarTexto:
    """Testa a validacao de quebra de linha (max 2 linhas, sem linha de 1 palavra)."""

    def _fonte_mock(self, largura_max=500):
        fonte = MagicMock()
        def getlength(texto):
            return sum(len(p) * 10 for p in texto.split())
        fonte.getlength = getlength
        return fonte

    def test_texto_vazio_ok(self):
        fonte = self._fonte_mock()
        ok, linhas, motivo = vct.validar_texto("", fonte, 500)
        assert ok is True

    def test_texto_curto_ok(self):
        fonte = self._fonte_mock()
        ok, linhas, motivo = vct.validar_texto("Code Review Graph", fonte, 500)
        assert ok is True

    def test_mais_de_2_linhas_reprova(self):
        fonte = self._fonte_mock(largura_max=20)
        ok, linhas, motivo = vct.validar_texto("Uma frase muito longa que vai quebrar", fonte, 20)
        assert ok is False
        assert "linhas" in motivo

    def test_linha_com_1_palavra_reprova(self):
        """Se a ultima linha tem so 1 palavra, reprova."""
        fonte = self._fonte_mock(largura_max=200)
        # Mock: getlength = sum(len(p) * 10 for p in texto.split())
        # "Code Review" = 110, "Code Review Graph" = 150
        # Com largura 120: "Code Review" (110) cabe, "Graph" (50) na linha 2
        ok, linhas, motivo = vct.validar_texto("Code Review Graph", fonte, 120)
        assert len(linhas) == 2
        assert ok is False
        assert "1 palavra" in motivo

    def test_2_linhas_2_palavras_ok(self):
        fonte = self._fonte_mock(largura_max=100)
        # "Desenvolvimento Guiado" = 120 > 100, "por" = 30, "Testes" = 60
        # Com largura 100: "Desenvolvimento" (150) sozinha ja passa...
        # Precisamos de palavras menores
        # "Code Review" = 70, "Graph Tool" = 90
        ok, linhas, motivo = vct.validar_texto("Code Review Graph Tool", fonte, 100)
        # "Code Review" (70) = linha 1, "Graph Tool" (90) = linha 2
        # Ambas com 2 palavras -> ok
        assert ok is True
        assert len(linhas) == 2


class TestConstantes:
    """Verifica que as constantes de layout estao corretas."""

    def test_largura_caixa_livro(self):
        assert vct.LARGURA_CAIXA["livro"] == 1600 - 2 * 80

    def test_largura_caixa_ebook(self):
        assert vct.LARGURA_CAIXA["ebook"] == 1200 - 2 * 80

    def test_tamanhos_fonte(self):
        assert vct.TAMANHO_TITULO == 72
        assert vct.TAMANHO_SUBTITULO == 22
