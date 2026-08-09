"""Testes para scripts/validar-escala.py (gate F1 — limites na seção Aplica)."""

import importlib.util
import sys
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "validar_escala",
    Path(__file__).resolve().parent.parent / "scripts" / "validar-escala.py",
)
ve = importlib.util.module_from_spec(_spec)
sys.modules["validar_escala"] = ve
_spec.loader.exec_module(ve)


Aplica_SEM_ESCALA = """Use a arquitetura descrita neste capítulo no seu próximo projeto. Ela melhora
a produtividade do time de forma geral.
"""

Aplica_COM_LIMITE = """O orquestrador escala até 50 agentes por nó; acima disso o gargalo passa a ser
o banco de estados. Para cargas maiores, separe por domínio.
"""

Aplica_TERMO_SEM_CONTEXTO = """A solução escala para qualquer tamanho de empresa, sem perder qualidade. É a
plataforma mais escalável do mercado.
"""


def _md_com_aplica(aplica):
    return ("# Capítulo 1\n\n"
            "## 1. Introdução\n\nTexto.\n\n"
            "## 5. Aplica\n\n" + aplica + "\n")


class TestValidarAplica:
    def test_sem_termo_escala_reprova(self):
        violacoes = ve.validar_aplica(_md_com_aplica(Aplica_SEM_ESCALA), "cap_1")
        regras = [v["regra"] for v in violacoes]
        assert "R-ES-1" in regras

    def test_termo_com_limite_passa(self):
        assert ve.validar_aplica(_md_com_aplica(Aplica_COM_LIMITE), "cap_1") == []

    def test_termo_sem_contexto_reprova(self):
        """R-ES-2: 'escala para qualquer tamanho' sem contorno é prosa de marketing."""
        violacoes = ve.validar_aplica(_md_com_aplica(Aplica_TERMO_SEM_CONTEXTO), "cap_1")
        regras = [v["regra"] for v in violacoes]
        assert "R-ES-2" in regras

    def test_sem_secao_aplica_reprova(self):
        texto = "# Capítulo 1\n\n## 1. Introdução\n\nTexto sem seção Aplica.\n"
        violacoes = ve.validar_aplica(texto, "cap_1")
        assert any(v["regra"] == "R-ES-1" for v in violacoes)

    def test_termo_dentro_de_codigo_ignorado(self):
        """Termo de escala dentro de bloco de código não satisfaz o gate."""
        texto = ("# Capítulo 1\n\n## 1. Introdução\n\nProsa.\n\n"
                 "## 5. Aplica\n\nProsa curta.\n\n"
                 "```python\n# escala até 100 nós\npass\n```\n")
        violacoes = ve.validar_aplica(texto, "cap_1")
        assert any(v["regra"] == "R-ES-1" for v in violacoes)
