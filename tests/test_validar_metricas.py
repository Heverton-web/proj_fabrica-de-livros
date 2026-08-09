"""Testes para scripts/validar-metricas.py (gate F1 — mensurabilidade)."""

import importlib.util
import sys
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "validar_metricas",
    Path(__file__).resolve().parent.parent / "scripts" / "validar-metricas.py",
)
vm = importlib.util.module_from_spec(_spec)
sys.modules["validar_metricas"] = vm
_spec.loader.exec_module(vm)


TEXTO_SEM_METRICA = """# Capítulo 1

## Introdução

A IA agêntica transforma a operação das empresas.

## Aplica

Use agentes para automatizar tarefas repetitivas.
"""

TEXTO_COM_METRICA = """# Capítulo 1

## Introdução

A IA agêntica reduz o tempo de atendimento para 200 ms [1].

## Aplica

A solução escala até 10 mil agentes por cluster.
"""

TEXTO_METRICA_DECLARADA_COM_CITACAO = """# Capítulo 1

## Introdução

A latência p95 caiu para 200 ms [3]. A fonte é o paper de referência.

## Aplica

Use com cuidado acima de 50 req/s.
"""

TEXTO_METRICA_DECLARADA_SEM_CITACAO = """# Capítulo 1

## Introdução

A latência p95 caiu para 200 ms. O sistema ficou mais rápido.

## Aplica

Use com cuidado acima de 50 req/s.
"""


class TestMetricasNoTexto:
    def test_sem_metrica(self):
        assert vm.metricas_no_texto(TEXTO_SEM_METRICA) == 0

    def test_com_metrica(self):
        assert vm.metricas_no_texto(TEXTO_COM_METRICA) >= 1

    def test_ignora_codigo(self):
        texto = "Prosa sem número.\n\n```python\nx = 300 ms\n```"
        assert vm.metricas_no_texto(texto) == 0


class TestValidarCapitulo:
    def test_r_mt_1_sem_metrica(self):
        violacoes = vm.validar_capitulo(TEXTO_SEM_METRICA, 1, [])
        regras = [v["regra"] for v in violacoes]
        assert "R-MT-1" in regras

    def test_r_mt_1_conforme(self):
        violacoes = vm.validar_capitulo(TEXTO_COM_METRICA, 1, [])
        assert violacoes == []

    def test_r_mt_2_valor_ausente(self):
        declaradas = [{"metrica": "custo por token", "valor": "R$ 0,002"}]
        violacoes = vm.validar_capitulo(TEXTO_COM_METRICA, 1, declaradas)
        regras = [v["regra"] for v in violacoes]
        assert "R-MT-2" in regras

    def test_r_mt_2_valor_presente_com_citacao(self):
        declaradas = [{"metrica": "latencia p95", "valor": "200 ms"}]
        assert vm.validar_capitulo(TEXTO_METRICA_DECLARADA_COM_CITACAO, 1, declaradas) == []

    def test_r_mt_3_valor_sem_citacao_no_paragrafo(self):
        declaradas = [{"metrica": "latencia p95", "valor": "200 ms"}]
        violacoes = vm.validar_capitulo(TEXTO_METRICA_DECLARADA_SEM_CITACAO, 1, declaradas)
        regras = [v["regra"] for v in violacoes]
        assert "R-MT-2" not in regras  # o valor está lá
        assert "R-MT-3" in regras      # mas sem [N] no mesmo parágrafo

    def test_declaracao_sem_valor_exige_nome(self):
        declaradas = [{"metrica": "taxa de sucesso"}]
        violacoes = vm.validar_capitulo(TEXTO_COM_METRICA, 1, declaradas)
        assert any(v["regra"] == "R-MT-2" for v in violacoes)


class TestMetricasDoSumario:
    def test_chave_por_str_e_int(self):
        sumario = {"metricas_obrigatorias": {"1": [{"metrica": "a", "valor": "1 s"}]}}
        assert len(vm.metricas_do_sumario(sumario, 1)) == 1
        assert len(vm.metricas_do_sumario(sumario, "1")) == 1

    def test_sem_declaracao(self):
        assert vm.metricas_do_sumario({}, 1) == []
        assert vm.metricas_do_sumario({"metricas_obrigatorias": {"2": []}}, 1) == []

    def test_valor_nao_lista_vira_lista(self):
        sumario = {"metricas_obrigatorias": {"7": {"metrica": "a", "valor": "1 s"}}}
        assert isinstance(vm.metricas_do_sumario(sumario, 7), list)
