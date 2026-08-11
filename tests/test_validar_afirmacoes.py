"""Testes para scripts/validar-afirmacoes.py (gate F2 — dados com citação)."""

import importlib.util
import sys
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "validar_afirmacoes",
    Path(__file__).resolve().parent.parent / "scripts" / "validar-afirmacoes.py",
)
va = importlib.util.module_from_spec(_spec)
sys.modules["validar_afirmacoes"] = va
_spec.loader.exec_module(va)


def _md(secoes):
    """Monta markdown EITA com pares (numero, titulo, corpo)."""
    partes = ["# Capítulo 1\n"]
    for num, titulo, corpo in secoes:
        partes.append(f"\n## {num}. {titulo}\n\n{corpo}")
    return "\n".join(partes) + "\n"


class TestTemDisparador:
    def test_percentual(self):
        assert va._tem_disparador("40% das empresas usam IA")

    def test_unidade_de_medida(self):
        assert va._tem_disparador("a latência caiu para 200 ms")

    def test_monetario(self):
        assert va._tem_disparador("o custo é de R$ 0,002 por token")

    def test_superlativo_mercado(self):
        assert va._tem_disparador("a maior plataforma de agentes")

    def test_prosa_comum_nao_dispara(self):
        assert not va._tem_disparador("A IA agêntica transforma a operação")
        assert not va._tem_disparador("o agente decide com base na descrição")

    def test_enfase_nao_dispara(self):
        """'o mais importante' é ênfase, não dado factual — não dispara."""
        assert not va._tem_disparador("Este é o mais importante dos critérios")

    def test_maioria_nao_dispara(self):
        """'a maioria' não é superlativo de liderança (substring bug: 'a maior')."""
        assert not va._tem_disparador("a maioria dos times comete esse erro")

    def test_unico_identificador_nao_dispara(self):
        """'único' como unicidade técnica (identificador único) não é dado factual."""
        assert not va._tem_disparador("o identificador deve ser curto e único")

    def test_primeiro_arquivo_nao_dispara(self):
        """'primeiro arquivo' não é reivindicação de pioneirismo ('primeiro a lançar')."""
        assert not va._tem_disparador("o README é o primeiro arquivo que se lê")

    def test_primeiro_a_verbo_dispara(self):
        """'primeiro a lançar' é reivindicação de pioneirismo — dispara."""
        assert va._tem_disparador("foi o primeiro a lançar agentes autônomos")


class TestValidarCapitulo:
    def test_dado_sem_citacao_viola(self):
        texto = _md([
            (1, "Introdução", "40% das empresas usam IA agêntica."),
        ])
        violacoes = va.validar_capitulo(texto, "cap_1")
        assert len(violacoes) == 1
        assert violacoes[0]["regra"] == "R-AF-1"

    def test_dado_com_citacao_passa(self):
        texto = _md([
            (1, "Introdução", "40% das empresas usam IA agêntica [3]."),
        ])
        assert va.validar_capitulo(texto, "cap_1") == []

    def test_citacao_multipla_passa(self):
        texto = _md([
            (1, "Introdução", "Reduz 30% do custo e 2x o throughput [1, 4]."),
        ])
        assert va.validar_capitulo(texto, "cap_1") == []

    def test_dado_em_codigo_nao_viola(self):
        texto = _md([
            (1, "Introdução", "Exemplo:\n\n```python\n# 30% de desconto\nx = 0.30\n```"),
        ])
        assert va.validar_capitulo(texto, "cap_1") == []

    def test_secao_referencias_nao_viola(self):
        """Seção 7 (referências) não exige [N] — o dado é o próprio registro."""
        texto = _md([
            (7, "Referências", "FULANO. Título. 2026. 40% dos casos relatados."),
        ])
        assert va.validar_capitulo(texto, "cap_1") == []

    def test_desafio_nao_viola(self):
        """Exercício do autor: números pertencem ao livro, não à fonte externa."""
        texto = _md([
            (6, "Conclusão", "**Desafio opcional**: meça com 20 perguntas e R$ 30 de limite."),
        ])
        assert va.validar_capitulo(texto, "cap_1") == []

    def test_tabela_nao_viola(self):
        texto = _md([
            (3, "Ilustra", "| Métrica | Valor |\n|---------|-------|\n| p95 | 200 ms |"),
        ])
        assert va.validar_capitulo(texto, "cap_1") == []
