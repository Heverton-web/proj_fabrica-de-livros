"""Testes para scripts/validar-codigo.py"""

import ast
import importlib.util
import json
import re
import sys
from pathlib import Path

import pytest

_spec = importlib.util.spec_from_file_location(
    "validar_codigo",
    Path(__file__).resolve().parent.parent / "scripts" / "validar-codigo.py",
)
vc = importlib.util.module_from_spec(_spec)
sys.modules["validar_codigo"] = vc
_spec.loader.exec_module(vc)


class TestNormLang:
    """Testa a normalizacao de aliases de linguagem."""

    def test_alias_py(self):
        assert vc.norm_lang("py") == "python"
        assert vc.norm_lang("python3") == "python"

    def test_alias_js(self):
        assert vc.norm_lang("js") == "javascript"
        assert vc.norm_lang("node") == "javascript"
        assert vc.norm_lang("mjs") == "javascript"
        assert vc.norm_lang("jsx") == "javascript"

    def test_alias_ts(self):
        assert vc.norm_lang("ts") == "typescript"
        assert vc.norm_lang("tsx") == "typescript"

    def test_alias_sh(self):
        assert vc.norm_lang("sh") == "bash"
        assert vc.norm_lang("shell") == "bash"
        assert vc.norm_lang("zsh") == "bash"

    def test_alias_ps1(self):
        assert vc.norm_lang("ps1") == "powershell"
        assert vc.norm_lang("pwsh") == "powershell"

    def test_alias_yml(self):
        assert vc.norm_lang("yml") == "yaml"

    def test_alias_json(self):
        assert vc.norm_lang("jsonc") == "json"
        assert vc.norm_lang("json5") == "json"

    def test_unknown_passthrough(self):
        assert vc.norm_lang("ruby") == "ruby"
        assert vc.norm_lang("go") == "go"

    def test_empty(self):
        assert vc.norm_lang("") == ""
        assert vc.norm_lang(None) == ""

    def test_case_insensitive(self):
        assert vc.norm_lang("Python") == "python"
        assert vc.norm_lang("JSON") == "json"


class TestRegexBloco:
    """Testa o regex de extracao de blocos de codigo."""

    def test_bloco_python(self):
        texto = "Texto antes.\n```python\nprint('hello')\n```\nTexto depois."
        matches = list(vc.RE_BLOCO.finditer(texto))
        assert len(matches) == 1
        assert matches[0].group("lang") == "python"
        assert "print('hello')" in matches[0].group("code")

    def test_bloco_sem_linguagem(self):
        texto = "```\ncodigo generico\n```"
        matches = list(vc.RE_BLOCO.finditer(texto))
        assert len(matches) == 1
        assert matches[0].group("lang") == ""

    def test_multiplos_blocos(self):
        texto = "```python\na = 1\n```\n\n```javascript\nb = 2\n```"
        matches = list(vc.RE_BLOCO.finditer(texto))
        assert len(matches) == 2

    def test_bloco_vazio(self):
        texto = "```\n```"
        matches = list(vc.RE_BLOCO.finditer(texto))
        assert len(matches) == 1

    def test_codigo_com_backticks_internos(self):
        """Blocos com ```dentro devem ser capturados corretamente."""
        texto = "```markdown\nUse ``code`` here\n```"
        matches = list(vc.RE_BLOCO.finditer(texto))
        assert len(matches) >= 1


class TestValidadoresPython:
    """Testa a validacao de sintaxe Python."""

    def test_codigo_valido(self):
        codigo = "x = 1\ny = x + 2\nprint(y)"
        try:
            ast.parse(codigo)
            valido = True
        except SyntaxError:
            valido = False
        assert valido is True

    def test_codigo_invalido(self):
        codigo = "def foo(:\n  pass"
        try:
            ast.parse(codigo)
            valido = True
        except SyntaxError:
            valido = False
        assert valido is False


class TestValidadoresJSON:
    """Testa a validacao de sintaxe JSON."""

    def test_json_valido(self):
        dados = '{"chave": "valor", "numero": 42}'
        result = json.loads(dados)
        assert result["chave"] == "valor"

    def test_json_invalido(self):
        dados = '{"chave": "valor",}'
        with pytest.raises(json.JSONDecodeError):
            json.loads(dados)
