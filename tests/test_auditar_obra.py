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


class TestDividirSecoesIgnoraCodeFences:
    """Cabecalhos `## N.` dentro de code fences NAO contam como secao EITA.

    Bug real: cap_2 do V3 governanca embute exemplos de requirements.md com
    "## 1. Requisitos Funcionais" dentro de ```markdown — o dicionario de
    secoes era sobrescrito e o capitulo acusado como incompleto (R3/R11/R12).
    """

    def test_cabecalho_dentro_de_code_fence_ignorado(self):
        texto = ("## 1. Introdução\n\nTexto da introdução.\n\n"
                 "## 2. Explica\n\nTexto da explicação.\n\n"
                 "```markdown\n"
                 "## 1. Requisitos Funcionais\n"
                 "## 2. Requisitos Não Funcionais\n"
                 "## 3. Restrições\n"
                 "```\n\n"
                 "## 3. Ilustra\n\nTexto da ilustração.\n")
        secoes = ao.dividir_secoes(texto)
        assert set(secoes.keys()) == {1, 2, 3}
        assert "introdu" in secoes[1]["titulo"].lower()
        assert "explica" in secoes[2]["titulo"].lower()
        assert "ilustra" in secoes[3]["titulo"].lower()

    def test_cabecalho_fora_de_code_fence_mantido(self):
        texto = ("## 1. Introdução\n\nTexto.\n\n"
                 "## 2. Explica\n\nMais texto.\n")
        secoes = ao.dividir_secoes(texto)
        assert "introdu" in secoes[1]["titulo"].lower()
        assert "explica" in secoes[2]["titulo"].lower()

    def test_corpo_da_secao_preserva_code_fence(self):
        texto = ("## 1. Introdução\n\nIntro.\n\n"
                 "## 4. Técnica\n\nAqui um exemplo:\n\n"
                 "```python\nprint(1)\n```\n")
        secoes = ao.dividir_secoes(texto)
        assert "```python" in secoes[4]["corpo"]
        assert len(ao.RE_CODIGO.findall(secoes[4]["corpo"])) == 1


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


def _cap_dict(**kwargs):
    base = {
        "capitulo": "1", "arquivo": "cap_1.md", "caracteres": 25000,
        "palavras": 4000, "secoes_faltantes": [], "referencias": 20,
        "citacoes_inline": 5, "diagramas_ilustra": 1, "diagramas_total": 2,
        "blocos_codigo_tecnica": 0, "artefatos_tecnica": 0,
        "horizontal_rules": 0, "pendencias": [], "truncado": False,
        "ultima_linha": "fim.", "refs_orfas": [], "refs_nao_citadas": [],
        "refs_ordem_correta": True, "citacoes_empilhadas": [],
        "vocabulario_fora_ilustra": None, "callback_presente": True,
        "ritmo": None, "sobreposicao": 0.0, "terminologia": [],
    }
    base.update(kwargs)
    return base


class TestR12EstiloTecnica:
    """R12 modular por estilo_tecnica: codigo/hibrido exigem bloco; operacional
    aceita artefato (bloco, diagrama ou passos numerados)."""

    def _requisito_r12(self, capitulos, estilo):
        reqs = ao.montar_requisitos_livro(
            capitulos, caracteres_obra=25000, min_capitulos=1,
            min_caracteres=25000, min_refs=1, estilo_tecnica=estilo)
        return next(r for r in reqs if r["id"] == "R12")

    def test_operacional_aceita_artefato_sem_bloco(self):
        # Tecnica com tabela de decisao (passos/artefato), sem bloco de codigo
        caps = [_cap_dict(blocos_codigo_tecnica=0, artefatos_tecnica=1)]
        assert self._requisito_r12(caps, "operacional")["conforme"]

    def test_codigo_reprova_sem_bloco_mas_com_artefato(self):
        caps = [_cap_dict(blocos_codigo_tecnica=0, artefatos_tecnica=1)]
        assert not self._requisito_r12(caps, "codigo")["conforme"]

    def test_codigo_aceita_bloco(self):
        caps = [_cap_dict(blocos_codigo_tecnica=1, artefatos_tecnica=1)]
        assert self._requisito_r12(caps, "codigo")["conforme"]

    def test_operacional_reprova_sem_artefato(self):
        caps = [_cap_dict(blocos_codigo_tecnica=0, artefatos_tecnica=0)]
        assert not self._requisito_r12(caps, "operacional")["conforme"]
