"""Testes da extensao --executar/--playbook de scripts/validar-codigo.py."""

import importlib.util
import json
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


class TestDetectarLinguagem:
    def test_python(self):
        assert vc.detectar_linguagem("import os\nprint(os.name)") == "python"
        assert vc.detectar_linguagem("def main():\n    pass") == "python"

    def test_javascript(self):
        assert vc.detectar_linguagem("console.log('oi')") == "javascript"
        assert vc.detectar_linguagem("const x = 1;") == "javascript"

    def test_bash(self):
        assert vc.detectar_linguagem("#!/bin/bash\necho oi") == "bash"
        assert vc.detectar_linguagem("mkdir -p build") == "bash"

    def test_default_python(self):
        assert vc.detectar_linguagem("x = 1") == "python"


class TestExecutarBloco:
    def test_python_ok(self):
        ok, detalhe = vc.executar_bloco("x = 1 + 1\nassert x == 2", "python")
        assert ok is True
        assert detalhe == ""

    def test_python_falha(self):
        ok, detalhe = vc.executar_bloco("raise ValueError('boom')", "python")
        assert ok is False
        assert "boom" in detalhe

    def test_python_timeout(self):
        ok, detalhe = vc.executar_bloco("import time\ntime.sleep(30)", "python", timeout=1)
        assert ok is False
        assert "timeout" in detalhe

    def test_javascript_ok(self):
        if not vc.shutil.which("node"):
            pytest.skip("node ausente")
        ok, _ = vc.executar_bloco("console.log(1 + 1)", "javascript")
        assert ok is True

    def test_linguagem_sem_executor(self):
        ok, detalhe = vc.executar_bloco("x", "powershell")
        assert ok is None
        assert "sem executor" in detalhe


class TestValidarPlaybook:
    def _montar_playbook(self, tmp_path):
        dir_passos = tmp_path / "passos"
        dir_passos.mkdir()
        card = {
            "numero": 1,
            "titulo": "Card de teste",
            "execucao": [
                {"titulo": "snippet", "linguagem": "python",
                 "codigo": "def soma(a, b):\n    return a + b\nassert soma(1, 2) == 3"},
            ],
            "gate": "python -c \"print('gate ok')\"",
            "feito_quando": ["o snippet roda"],
        }
        (dir_passos / "passo_01.json").write_text(
            json.dumps(card, ensure_ascii=False), encoding="utf-8")
        return tmp_path

    def test_playbook_sintaxe_sem_executar(self, tmp_path):
        dir_pbk = self._montar_playbook(tmp_path)
        resultados = vc.validar_playbook(dir_pbk, ignorar_fragmentos=False,
                                         executar=False)
        assert len(resultados) == 2  # 1 execucao + 1 gate
        assert resultados[0]["status"] == "ok"
        assert resultados[1]["status"] == "ok"  # gate presente, nao executado

    def test_playbook_executa_gate(self, tmp_path):
        dir_pbk = self._montar_playbook(tmp_path)
        resultados = vc.validar_playbook(dir_pbk, ignorar_fragmentos=False,
                                         executar=True)
        execucao = resultados[0]
        gate = resultados[1]
        assert execucao["status"] == "ok"
        assert execucao.get("execucao") == "ok"
        if vc.shutil.which("bash"):
            assert gate["status"] == "ok"
            assert gate.get("execucao") == "ok"

    def test_playbook_falha_de_execucao(self, tmp_path):
        dir_passos = tmp_path / "passos"
        dir_passos.mkdir()
        card = {"numero": 1, "titulo": "Card ruim",
                "execucao": [{"titulo": "snippet", "linguagem": "python",
                              "codigo": "raise ValueError('quebrou')"}]}
        (dir_passos / "passo_01.json").write_text(
            json.dumps(card), encoding="utf-8")
        resultados = vc.validar_playbook(tmp_path, ignorar_fragmentos=False,
                                         executar=True)
        assert resultados[0]["status"] == "falha_execucao"

    def test_playbook_json_invalido(self, tmp_path):
        dir_passos = tmp_path / "passos"
        dir_passos.mkdir()
        (dir_passos / "passo_01.json").write_text("{ nao é json", encoding="utf-8")
        resultados = vc.validar_playbook(tmp_path, ignorar_fragmentos=False,
                                         executar=False)
        assert resultados[0]["status"] == "falha"


class TestValidarArquivoComExecucao:
    def test_executa_bloco_ok(self, tmp_path):
        md = tmp_path / "cap.md"
        md.write_text("```python\nprint(2 ** 4)\n```\n", encoding="utf-8")
        resultados = vc.validar_arquivo(md, "cap_1", ignorar_fragmentos=False,
                                        executar=True)
        assert resultados[0]["status"] == "ok"
        assert resultados[0].get("execucao") == "ok"

    def test_execucao_falha_marca_falha_execucao(self, tmp_path):
        md = tmp_path / "cap.md"
        md.write_text("```python\n1 / 0\n```\n", encoding="utf-8")
        resultados = vc.validar_arquivo(md, "cap_1", ignorar_fragmentos=False,
                                        executar=True)
        assert resultados[0]["status"] == "falha_execucao"

    def test_sem_executar_nao_roda(self, tmp_path):
        md = tmp_path / "cap.md"
        md.write_text("```python\n1 / 0\n```\n", encoding="utf-8")
        resultados = vc.validar_arquivo(md, "cap_1", ignorar_fragmentos=False,
                                        executar=False)
        assert resultados[0]["status"] == "ok"  # sintaxe ok, sem execucao
        assert "execucao" not in resultados[0]
