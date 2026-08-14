"""Testes para scripts/gerar-esqueleto-macro.py (esqueleto P/M/G determinístico)."""

import importlib.util
import json
import sys
from pathlib import Path

DIR_PROJETO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR_PROJETO / "scripts"))

_spec = importlib.util.spec_from_file_location(
    "gerar_esqueleto_macro", DIR_PROJETO / "scripts" / "gerar-esqueleto-macro.py"
)
gm = importlib.util.module_from_spec(_spec)
sys.modules["gerar_esqueleto_macro"] = gm
_spec.loader.exec_module(gm)

import parametros_obra as PO


class TestDistribuirCapitulos:
    def test_divisao_exata(self):
        assert gm.distribuir_capitulos(8, 2) == [4, 4]

    def test_resto_vai_para_as_primeiras_partes(self):
        assert gm.distribuir_capitulos(4, 1) == [4]
        assert gm.distribuir_capitulos(20, 5) == [4, 4, 4, 4, 4]

    def test_capitulos_menor_que_partes_nao_gera_negativo(self):
        assert sum(gm.distribuir_capitulos(4, 4)) == 4


class TestMontarEsqueleto:
    def test_bate_com_parametros_obra_para_cada_tamanho(self):
        for tamanho in ("P", "M", "G", "GG", "XG"):
            esqueleto = gm.montar_esqueleto(tamanho)
            minimos = PO.minimos_livro(tamanho)
            assert len(esqueleto["partes"]) == minimos["partes"]
            total_cap = sum(len(p["capitulos"]) for p in esqueleto["partes"])
            assert total_cap == minimos["capitulos"]

    def test_numeracao_de_capitulo_e_sequencial_entre_partes(self):
        esqueleto = gm.montar_esqueleto("M")
        numeros = [c["capitulo"] for p in esqueleto["partes"] for c in p["capitulos"]]
        assert numeros == [str(n) for n in range(1, len(numeros) + 1)]

    def test_partes_em_numeral_romano(self):
        esqueleto = gm.montar_esqueleto("G")
        assert [p["parte"] for p in esqueleto["partes"]] == ["I", "II", "III"]

    def test_titulos_e_motivo_condutor_vazios_para_llm_preencher(self):
        esqueleto = gm.montar_esqueleto("P")
        assert esqueleto["titulo_obra"] == ""
        assert esqueleto["motivo_condutor"]["nome"] == ""
        assert esqueleto["partes"][0]["capitulos"][0]["titulo"] == ""


class TestMain:
    def test_grava_com_tamanho_explicito(self, tmp_path, monkeypatch):
        base = tmp_path / "output"
        (base / "livros" / "x").mkdir(parents=True)
        monkeypatch.setattr(gm, "DIR_OUTPUT", base)
        monkeypatch.setattr(sys, "argv", ["gerar-esqueleto-macro.py", "livros/x", "--tamanho", "P"])
        assert gm.main() == 0
        destino = base / "livros" / "x" / "sumario_macro.json"
        dados = json.loads(destino.read_text(encoding="utf-8"))
        assert len(dados["partes"]) == 1
        assert sum(len(p["capitulos"]) for p in dados["partes"]) == 4

    def test_nao_sobrescreve_sem_forcar(self, tmp_path, monkeypatch):
        base = tmp_path / "output"
        dir_obra = base / "livros" / "x"
        dir_obra.mkdir(parents=True)
        (dir_obra / "sumario_macro.json").write_text('{"ja_existe": true}', encoding="utf-8")
        monkeypatch.setattr(gm, "DIR_OUTPUT", base)
        monkeypatch.setattr(sys, "argv", ["gerar-esqueleto-macro.py", "livros/x", "--tamanho", "M"])
        assert gm.main() == 1
        assert json.loads((dir_obra / "sumario_macro.json").read_text(encoding="utf-8")) == {"ja_existe": True}

    def test_usa_tamanho_do_config_obra_quando_nao_informado(self, tmp_path, monkeypatch):
        base = tmp_path / "output"
        dir_obra = base / "livros" / "x"
        (dir_obra / "esboco").mkdir(parents=True)
        dir_obra.mkdir(parents=True, exist_ok=True)
        (dir_obra / "config_obra.json").write_text(
            json.dumps({"tamanho_obra": "G"}), encoding="utf-8"
        )
        monkeypatch.setattr(gm, "DIR_OUTPUT", base)
        monkeypatch.setattr(PO, "DIR_OUTPUT", base)
        monkeypatch.setattr(sys, "argv", ["gerar-esqueleto-macro.py", "livros/x"])
        assert gm.main() == 0
        dados = json.loads((dir_obra / "sumario_macro.json").read_text(encoding="utf-8"))
        assert len(dados["partes"]) == 3
