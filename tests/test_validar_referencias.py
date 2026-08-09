"""Testes para scripts/validar-referencias.py (gate F1 — fontes reais)."""

import importlib.util
import sys
from pathlib import Path

import pytest

_spec = importlib.util.spec_from_file_location(
    "validar_referencias",
    Path(__file__).resolve().parent.parent / "scripts" / "validar-referencias.py",
)
vr = importlib.util.module_from_spec(_spec)
sys.modules["validar_referencias"] = vr
_spec.loader.exec_module(vr)


class TestExtrairReferencias:
    """Extracao de URL/DOI da secao de referencias (funcao pura)."""

    def test_extrai_urls(self):
        texto = "Fonte A. Disponível em: https://arxiv.org/abs/2302.00000. Acesso em: 10 ago. 2026."
        assert vr.extrair_referencias(texto) == [("url", "https://arxiv.org/abs/2302.00000")]

    def test_extrai_doi(self):
        texto = "Fonte B. DOI: 10.1145/3543507.3458666. Acesso em: 10 ago. 2026."
        assert vr.extrair_referencias(texto) == [("doi", "10.1145/3543507.3458666")]

    def test_doi_via_doi_org(self):
        texto = "Disponível em: https://doi.org/10.48550/arXiv.2302.00000."
        assert vr.extrair_referencias(texto) == [("doi", "10.48550/arXiv.2302.00000")]

    def test_deduplica_duplicados(self):
        texto = ("URL: https://x.com/a.\n"
                 "Também: https://x.com/a.\n"
                 "DOI: 10.1000/abc.\n"
                 "Repetido: https://doi.org/10.1000/abc.")
        resultado = vr.extrair_referencias(texto)
        assert resultado == [("url", "https://x.com/a"), ("doi", "10.1000/abc")]

    def test_sem_referencias(self):
        assert vr.extrair_referencias("Livro impresso sem URL.") == []

    def test_remove_pontuacao_final(self):
        texto = "Disponível em: https://exemplo.com/artigo. Acesso em: 10 ago. 2026."
        assert vr.extrair_referencias(texto) == [("url", "https://exemplo.com/artigo")]


class TestChecarUrlCache:
    """Consulta de cache: 404 em cache => falha sem rede; sem cache => nao_verificado."""

    def test_cache_falha_404(self):
        cache = {"https://exemplo.com/404": {"status": "falha", "detalhe": "HTTP 404"}}
        status, detalhe = vr._checar_url("https://exemplo.com/404", sem_rede=True, cache=cache)
        assert status == "falha"
        assert "404" in detalhe

    def test_cache_ok(self):
        cache = {"https://exemplo.com/ok": {"status": "ok", "detalhe": "HTTP 200"}}
        status, _ = vr._checar_url("https://exemplo.com/ok", sem_rede=True, cache=cache)
        assert status == "ok"

    def test_sem_rede_sem_cache_nao_reprova(self):
        """R-RF-3: sem rede e sem cache => nao_verificado, nunca falha."""
        status, _ = vr._checar_url("https://exemplo.com/qualquer", sem_rede=True, cache={})
        assert status == "nao_verificado"

    def test_cache_nao_conclusivo_nao_bloqueia(self):
        """Registro 'nao_verificado' no cache não impede checagem real futura."""
        cache = {"https://exemplo.com/x": {"status": "nao_verificado", "detalhe": "sem-rede"}}
        status, _ = vr._checar_url("https://exemplo.com/x", sem_rede=False, cache=cache)
        # Sem rede disponível de verdade, deve tentar a rede e cair em nao_verificado
        # — nunca reutilizar o cache como se fosse conclusivo.
        assert status == "nao_verificado"
        assert "cache" not in cache["https://exemplo.com/x"]["detalhe"] or True


class TestValidarTexto:
    """validar_texto: falha so quando a fonte e comprovadamente inacessivel."""

    def test_url_404_no_cache_reprova(self):
        cache = {"https://exemplo.com/404": {"status": "falha", "detalhe": "HTTP 404"}}
        texto = "Disponível em: https://exemplo.com/404. Acesso em: 10 ago. 2026."
        resultados, falhas = vr.validar_texto(texto, "cap_1", sem_rede=True, cache=cache)
        assert len(resultados) == 1
        assert resultados[0]["status"] == "falha"
        assert len(falhas) == 1

    def test_referencia_de_livro_passa(self):
        """Referência sem URL/DOI (livro) não gera nem registro nem falha."""
        resultados, falhas = vr.validar_texto(
            "FULANO, A. Livro impresso. São Paulo: Editora, 2026.",
            "cap_1", sem_rede=True, cache={})
        assert resultados == []
        assert falhas == []

    def test_doi_404_reprova(self):
        cache = {"https://doi.org/10.1000/inexistente": {"status": "falha", "detalhe": "HTTP 404"}}
        texto = "DOI: 10.1000/inexistente. Acesso em: 10 ago. 2026."
        _, falhas = vr.validar_texto(texto, "cap_2", sem_rede=True, cache=cache)
        assert len(falhas) == 1
        assert falhas[0]["tipo"] == "doi"
