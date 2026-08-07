"""Testes para scripts/auditar-obra.py — regex de pendencia e termos."""

import importlib.util
import re
import sys
from pathlib import Path

import pytest

_spec = importlib.util.spec_from_file_location(
    "auditar_obra",
    Path(__file__).resolve().parent.parent / "scripts" / "auditar-obra.py",
)
ao = importlib.util.module_from_spec(_spec)
sys.modules["auditar_obra"] = ao
_spec.loader.exec_module(ao)


class TestRegexPendenciaMaiuscula:
    """Testa RE_PENDENCIA_MAIUSCULA — case-sensitive, so TODO/FIXME/TBD/XXX."""

    def test_todo_maiuscula_casa(self):
        assert ao.RE_PENDENCIA_MAIUSCULA.search("Precisa de TODO o trabalho")

    def test_todo_minuscula_nao_casa(self):
        # "todo" em portugues NAO deve casar (falso-positivo historicamente)
        assert not ao.RE_PENDENCIA_MAIUSCULA.search("nem todo sistema funciona")

    def test_todo_maiuscula_isolado(self):
        assert ao.RE_PENDENCIA_MAIUSCULA.search("TODO: implementar")

    def test_todo_no_inicio(self):
        assert ao.RE_PENDENCIA_MAIUSCULA.search("TODO implementar isso")

    def test_fixme_casa(self):
        assert ao.RE_PENDENCIA_MAIUSCULA.search("FIXME: bug")

    def test_tbd_casa(self):
        assert ao.RE_PENDENCIA_MAIUSCULA.search("TBD")

    def test_xxx_casa(self):
        assert ao.RE_PENDENCIA_MAIUSCULA.search("XXX")

    def test_mixed_case_nao_casa(self):
        assert not ao.RE_PENDENCIA_MAIUSCULA.search("todo ok")
        assert not ao.RE_PENDENCIA_MAIUSCULA.search("fixme bug")
        assert not ao.RE_PENDENCIA_MAIUSCULA.search("tbd")


class TestRegexPendenciaGenerica:
    """Testa RE_PENDENCIA_GENERICA — placeholder, lorem ipsum, etc."""

    def test_placeholder_casa(self):
        assert ao.RE_PENDENCIA_GENERICA.search("placeholder texto")

    def test_lorem_ipsum_casa(self):
        assert ao.RE_PENDENCIA_GENERICA.search("lorem ipsum dolor")

    def test_inserir_casa(self):
        assert ao.RE_PENDENCIA_GENERICA.search("[inserir conteudo aqui]")

    def test_completar_casa(self):
        assert ao.RE_PENDENCIA_GENERICA.search("[completar]")

    def test_continua_proximo_casa(self):
        assert ao.RE_PENDENCIA_GENERICA.search("continua no próximo capítulo")

    def test_a_ser_escrito_casa(self):
        assert ao.RE_PENDENCIA_GENERICA.search("a ser escrito")

    def test_case_insensitive(self):
        assert ao.RE_PENDENCIA_GENERICA.search("LOREM IPSUM")
        assert ao.RE_PENDENCIA_GENERICA.search("Placeholder")


class TestPendenciaMatcher:
    """Testa o combinador _PendenciaMatcher que junta os dois regex."""

    def test_todo_maiuscula_encontrado(self):
        matches = list(ao.RE_PENDENCIA.finditer("texto com TODO aqui"))
        assert len(matches) >= 1
        assert any("TODO" in m.group() for m in matches)

    def test_todo_minuscula_nao_encontrado(self):
        matches = list(ao.RE_PENDENCIA.finditer("nem todo sistema funciona"))
        assert len(matches) == 0

    def test_placeholder_encontrado(self):
        matches = list(ao.RE_PENDENCIA.finditer("insira placeholder"))
        assert len(matches) >= 1

    def test_texto_limpo_sem_matches(self):
        texto = "Este capitulo esta completo e bem escrito."
        matches = list(ao.RE_PENDENCIA.finditer(texto))
        assert len(matches) == 0
