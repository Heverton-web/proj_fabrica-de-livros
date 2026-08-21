"""Testes para scripts/token-guard.py (item B — melhorias/21-08-2026-plano-acao-
tokens-sob-pericia.md, cross-check de gasto auto-relato vs ccusage).

Best-effort/aditivo: NUNCA levanta excecao, mesmo com ccusage ausente/quebrado
ou .agents/session-cost.jsonl inexistente — o mesmo espirito do livro de nao
tratar ausencia de dado como aprovacao nem como erro fatal.
"""

import json
import subprocess

import pytest

from conftest import carregar_script

TG = carregar_script("token-guard.py")


class _ProcessoFake:
    def __init__(self, stdout="", stderr="", returncode=0):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode


class TestCustoCcusageDoDia:
    def test_soma_totalcost_do_dia(self, monkeypatch):
        saida = json.dumps({
            "daily": [{"period": "2026-08-20", "totalCost": 12.5}],
        })

        def _run(comando, **kwargs):
            return _ProcessoFake(stdout=saida, returncode=0)

        monkeypatch.setattr(subprocess, "run", _run)
        custo, erro = TG.custo_ccusage_do_dia("2026-08-20")
        assert custo == 12.5
        assert erro is None

    def test_sem_uso_no_dia_devolve_zero(self, monkeypatch):
        def _run(comando, **kwargs):
            return _ProcessoFake(stdout=json.dumps({"daily": []}), returncode=0)

        monkeypatch.setattr(subprocess, "run", _run)
        custo, erro = TG.custo_ccusage_do_dia("2026-08-20")
        assert custo == 0.0
        assert erro is None

    def test_ccusage_ausente_nao_levanta(self, monkeypatch):
        def _run(comando, **kwargs):
            raise FileNotFoundError("npx nao encontrado")

        monkeypatch.setattr(subprocess, "run", _run)
        custo, erro = TG.custo_ccusage_do_dia("2026-08-20")
        assert custo is None
        assert "indisponivel" in erro

    def test_timeout_nao_levanta(self, monkeypatch):
        def _run(comando, **kwargs):
            raise subprocess.TimeoutExpired(cmd="npx", timeout=30)

        monkeypatch.setattr(subprocess, "run", _run)
        custo, erro = TG.custo_ccusage_do_dia("2026-08-20")
        assert custo is None
        assert erro is not None

    def test_saida_invalida_nao_levanta(self, monkeypatch):
        def _run(comando, **kwargs):
            return _ProcessoFake(stdout="isto nao e json", returncode=0)

        monkeypatch.setattr(subprocess, "run", _run)
        custo, erro = TG.custo_ccusage_do_dia("2026-08-20")
        assert custo is None
        assert "JSON" in erro

    def test_exit_code_diferente_de_zero_nao_levanta(self, monkeypatch):
        def _run(comando, **kwargs):
            return _ProcessoFake(stderr="rate limit", returncode=1)

        monkeypatch.setattr(subprocess, "run", _run)
        custo, erro = TG.custo_ccusage_do_dia("2026-08-20")
        assert custo is None
        assert "erro" in erro.lower()


class TestCustoAutorrelatoDoDia:
    def test_soma_apenas_do_dia_informado(self, tmp_path):
        caminho = tmp_path / "session-cost.jsonl"
        caminho.write_text(
            '{"ts": "2026-08-20T10:00:00Z", "cost": 1.5}\n'
            '{"ts": "2026-08-20T14:00:00Z", "cost": 2.5}\n'
            '{"ts": "2026-08-19T10:00:00Z", "cost": 99.0}\n',
            encoding="utf-8")
        custo, n = TG.custo_autorrelato_do_dia("2026-08-20", caminho=caminho)
        assert custo == 4.0
        assert n == 2

    def test_arquivo_ausente_devolve_zero(self, tmp_path):
        custo, n = TG.custo_autorrelato_do_dia(
            "2026-08-20", caminho=tmp_path / "nao-existe.jsonl")
        assert custo == 0.0
        assert n == 0

    def test_linha_invalida_e_ignorada(self, tmp_path):
        caminho = tmp_path / "session-cost.jsonl"
        caminho.write_text(
            '{"ts": "2026-08-20T10:00:00Z", "cost": 1.0}\n'
            "linha quebrada nao json\n"
            "\n",
            encoding="utf-8")
        custo, n = TG.custo_autorrelato_do_dia("2026-08-20", caminho=caminho)
        assert custo == 1.0
        assert n == 1


class TestComparar:
    def test_sem_divergencia_relevante(self, monkeypatch, tmp_path):
        monkeypatch.setattr(TG, "custo_ccusage_do_dia",
                            lambda data, **kw: (10.0, None))
        monkeypatch.setattr(TG, "custo_autorrelato_do_dia",
                            lambda data, caminho=None: (10.5, 3))
        resultado = TG.comparar("2026-08-20")
        assert resultado["diverge"] is False
        assert resultado["ccusage_usd"] == 10.0

    def test_divergencia_acima_do_limiar_sinaliza(self, monkeypatch):
        monkeypatch.setattr(TG, "custo_ccusage_do_dia",
                            lambda data, **kw: (50.0, None))
        monkeypatch.setattr(TG, "custo_autorrelato_do_dia",
                            lambda data, caminho=None: (1.0, 1))
        resultado = TG.comparar("2026-08-20")
        assert resultado["diverge"] is True
        assert "diverge" in resultado["motivo"]

    def test_ccusage_indisponivel_marca_nao_verificavel(self, monkeypatch):
        monkeypatch.setattr(TG, "custo_ccusage_do_dia",
                            lambda data, **kw: (None, "npx ausente"))
        monkeypatch.setattr(TG, "custo_autorrelato_do_dia",
                            lambda data, caminho=None: (3.0, 2))
        resultado = TG.comparar("2026-08-20")
        assert resultado["ccusage_usd"] is None
        assert resultado["diverge"] is None
        assert "NAO_VERIFICAVEL" in resultado["motivo"] or "npx ausente" in resultado["motivo"]


class TestMainCli:
    def test_json_mode_nao_levanta_sem_ccusage(self, monkeypatch, capsys):
        monkeypatch.setattr(TG, "custo_ccusage_do_dia",
                            lambda data, **kw: (None, "sem rede"))
        monkeypatch.setattr(TG, "custo_autorrelato_do_dia",
                            lambda data, caminho=None: (0.0, 0))
        monkeypatch.setattr("sys.argv", ["token-guard.py", "--data", "2026-08-20", "--json"])
        assert TG.main() == 0
        saida = json.loads(capsys.readouterr().out)
        assert saida["ccusage_usd"] is None
