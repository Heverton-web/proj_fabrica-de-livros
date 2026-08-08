"""Testes do gate do PLAYBOOK (scripts/validar-playbook.py) — R-PBK-0 a R-PBK-8.

Cada regra tem caso positivo e negativo. R-PBK-0 e a mais importante: e ela que
impede o playbook de virar um resumo do livro.
"""

import json

import pytest

from conftest import CAPITULO_EITA, carregar_script

extrator = carregar_script("extrair-passos-praticos.py")
gate = carregar_script("validar-playbook.py")


def _card_valido(numero="01", **sobrepor):
    card = {
        "numero": numero,
        "titulo": "Fundação do Projeto",
        "estagio": "Fundação",
        "objetivo": "Estabelecer os contratos que sustentam o sistema",
        "pre_requisito": "Nenhum — este é o ponto de partida",
        "entregas": ["scripts/contrato.py"],
        "execucao": [{"titulo": "Criar", "linguagem": "bash",
                      "comandos": ["python scripts/contrato.py"],
                      "codigo": "python scripts/contrato.py"}],
        "gate": "python scripts/validar-contrato.py --estrito",
        "comandos": ["python scripts/validar-contrato.py --estrito"],
        "feito_quando": ["Arquivo criado", "Validador em zero", "Índice atualizado"],
        "armadilhas": ["Gravar fora de scripts/"],
        "referencia_cruzada": "Cap. 1",
        "lacunas": [],
    }
    card.update(sobrepor)
    return card


@pytest.fixture
def playbook(tmp_path, monkeypatch):
    """Playbook minimo e VALIDO, sem livro-mae (R-PBK-0/7 viram aviso)."""
    raiz = tmp_path / "output"
    dir_pbk = raiz / "playbooks" / "obra--pbk"
    (dir_pbk / "passos").mkdir(parents=True)
    (dir_pbk / "imagens").mkdir(parents=True)
    (dir_pbk / "config_obra.json").write_text(json.dumps({
        "tipo_obra": "playbook", "senioridade_obra": "intermediario",
        "obra_mae": "obra",
    }), encoding="utf-8")
    (dir_pbk / "sumario_macro.json").write_text(json.dumps({
        "titulo_obra": "Playbook", "motivo_condutor": {"vocabulario": ["fundação"]},
    }, ensure_ascii=False), encoding="utf-8")
    (dir_pbk / "passos" / "passo_01.json").write_text(
        json.dumps(_card_valido(), ensure_ascii=False), encoding="utf-8")

    monkeypatch.setattr(gate, "DIR_OUTPUT", raiz)
    return {"raiz": raiz, "dir": dir_pbk, "slug": "playbooks/obra--pbk"}


def _regravar(playbook, card):
    (playbook["dir"] / "passos" / f"passo_{card['numero']}.json").write_text(
        json.dumps(card, ensure_ascii=False), encoding="utf-8")


def _regras(rel):
    return {v["regra"] for v in rel["violacoes"]}


class TestPlaybookConforme:
    def test_playbook_minimo_e_conforme(self, playbook):
        rel = gate.validar(playbook["slug"])
        assert rel["conforme"], rel["violacoes"]

    def test_avisa_quando_livro_mae_nao_existe(self, playbook):
        rel = gate.validar(playbook["slug"])
        assert any("livro-mae" in a for a in rel["avisos"])


class TestR_PBK_1:
    @pytest.mark.parametrize("campo,vazio", [
        ("objetivo", ""), ("pre_requisito", ""), ("entregas", []),
        ("execucao", []), ("gate", ""), ("feito_quando", []), ("armadilhas", []),
    ])
    def test_parte_vazia_reprova(self, playbook, campo, vazio):
        _regravar(playbook, _card_valido(**{campo: vazio}))
        rel = gate.validar(playbook["slug"])
        assert "R-PBK-1" in _regras(rel)


class TestR_PBK_2_3:
    def test_sem_entrega_reprova_r2(self, playbook):
        _regravar(playbook, _card_valido(entregas=[]))
        assert "R-PBK-2" in _regras(gate.validar(playbook["slug"]))

    def test_sem_gate_reprova_r3(self, playbook):
        _regravar(playbook, _card_valido(gate=""))
        assert "R-PBK-3" in _regras(gate.validar(playbook["slug"]))


class TestR_PBK_4:
    def test_poucos_itens_reprova(self, playbook):
        _regravar(playbook, _card_valido(feito_quando=["um", "dois"]))
        assert "R-PBK-4" in _regras(gate.validar(playbook["slug"]))

    def test_itens_demais_reprova(self, playbook):
        _regravar(playbook, _card_valido(feito_quando=[f"item {i}" for i in range(9)]))
        assert "R-PBK-4" in _regras(gate.validar(playbook["slug"]))

    def test_limites_inclusivos_passam(self, playbook):
        for n in (3, 7):
            _regravar(playbook, _card_valido(feito_quando=[f"item {i}" for i in range(n)]))
            assert "R-PBK-4" not in _regras(gate.validar(playbook["slug"]))


class TestR_PBK_5:
    def test_parte_longa_reprova(self, playbook):
        _regravar(playbook, _card_valido(
            entregas=[f"scripts/a{i}.py" for i in range(30)]))
        assert "R-PBK-5" in _regras(gate.validar(playbook["slug"]))

    def test_execucao_longa_reprova(self, playbook):
        codigo = "\n".join(f"linha {i}" for i in range(40))
        _regravar(playbook, _card_valido(execucao=[
            {"titulo": "X", "linguagem": "bash", "comandos": [], "codigo": codigo}]))
        assert "R-PBK-5" in _regras(gate.validar(playbook["slug"]))


class TestR_PBK_6:
    def test_sem_senioridade_reprova(self, playbook):
        (playbook["dir"] / "config_obra.json").write_text(
            json.dumps({"tipo_obra": "playbook"}), encoding="utf-8")
        assert "R-PBK-6" in _regras(gate.validar(playbook["slug"]))

    def test_capa_ausente_e_aviso_nao_violacao(self, playbook):
        rel = gate.validar(playbook["slug"])
        assert any("capa" in a for a in rel["avisos"])
        assert "R-PBK-6" not in _regras(rel)


class TestR_PBK_8:
    def test_estagio_sem_vocabulario_reprova(self, playbook):
        _regravar(playbook, _card_valido(estagio="Capítulo Um"))
        assert "R-PBK-8" in _regras(gate.validar(playbook["slug"]))

    def test_obra_sem_vocabulario_vira_aviso(self, playbook):
        (playbook["dir"] / "sumario_macro.json").write_text(
            json.dumps({"titulo_obra": "P", "motivo_condutor": {}}), encoding="utf-8")
        rel = gate.validar(playbook["slug"])
        assert "R-PBK-8" not in _regras(rel)
        assert any("motivo_condutor" in a for a in rel["avisos"])


class TestComLivroMae:
    @pytest.fixture
    def com_mae(self, playbook):
        dir_mae = playbook["raiz"] / "livros" / "obra"
        (dir_mae / "capitulos").mkdir(parents=True)
        (dir_mae / "capitulos" / "cap_01.md").write_text(CAPITULO_EITA, encoding="utf-8")
        return playbook

    def test_r7_conforme_quando_ha_1_card_por_capitulo(self, com_mae):
        rel = gate.validar(com_mae["slug"])
        assert "R-PBK-7" not in _regras(rel)

    def test_r7_reprova_com_capitulo_sem_card(self, com_mae):
        dir_caps = com_mae["raiz"] / "livros" / "obra" / "capitulos"
        (dir_caps / "cap_02.md").write_text(CAPITULO_EITA, encoding="utf-8")
        rel = gate.validar(com_mae["slug"])
        assert "R-PBK-7" in _regras(rel)
        assert "faltando" in [v["detalhe"] for v in rel["violacoes"]
                              if v["regra"] == "R-PBK-7"][0]

    def test_r0_reprova_card_que_recicla_teoria(self, com_mae):
        teoria = ("A fundação de um projeto agêntico é o conjunto de contratos que o "
                  "restante do sistema assume como verdade. Sem contrato explícito, "
                  "cada camada inventa o seu.")
        _regravar(com_mae, _card_valido(objetivo=teoria))
        rel = gate.validar(com_mae["slug"])
        assert "R-PBK-0" in _regras(rel)

    def test_r0_aprova_card_pratico(self, com_mae):
        rel = gate.validar(com_mae["slug"])
        assert "R-PBK-0" not in _regras(rel)

    def test_encontra_capitulo_gravado_sem_zero_a_esquerda(self, com_mae):
        """A fabrica grava cap_1.md; o gate nao pode deixar R-PBK-0 mudo por isso."""
        dir_caps = com_mae["raiz"] / "livros" / "obra" / "capitulos"
        (dir_caps / "cap_01.md").rename(dir_caps / "cap_1.md")
        teoria = ("A fundação de um projeto agêntico é o conjunto de contratos que o "
                  "restante do sistema assume como verdade. Sem contrato explícito, "
                  "cada camada inventa o seu.")
        _regravar(com_mae, _card_valido(objetivo=teoria))
        assert "R-PBK-0" in _regras(gate.validar(com_mae["slug"]))

    def test_r7_ignora_arquivos_auxiliares(self, com_mae):
        dir_caps = com_mae["raiz"] / "livros" / "obra" / "capitulos"
        (dir_caps / "_cap_rascunho.md").write_text("x", encoding="utf-8")
        assert "R-PBK-7" not in _regras(gate.validar(com_mae["slug"]))


class TestPontaAPonta:
    def test_extracao_real_passa_no_gate_no_capitulo_completo(self, livro_falso, monkeypatch):
        monkeypatch.setattr(extrator, "DIR_OUTPUT", livro_falso["raiz"])
        monkeypatch.setattr(gate, "DIR_OUTPUT", livro_falso["raiz"])
        res = extrator.extrair(livro_falso["slug"])

        # Config do playbook (normalmente gravado por fatiar-obra.py --playbook)
        (res["dir"] / "config_obra.json").write_text(json.dumps({
            "tipo_obra": "playbook", "senioridade_obra": "intermediario",
            "obra_mae": "obra-teste",
        }), encoding="utf-8")

        rel = gate.validar("playbooks/obra-teste--pbk")
        regras = _regras(rel)
        # cap_02 e incompleto de proposito -> R-PBK-1/2/3/4 acusam nele
        assert {v["passo"] for v in rel["violacoes"] if v["passo"]} == {"02"}
        assert "R-PBK-0" not in regras       # nada de teoria reciclada
        assert "R-PBK-8" not in regras       # estagio veio do vocabulario


class TestPastaAusente:
    def test_playbook_sem_pasta_de_passos(self, tmp_path, monkeypatch):
        monkeypatch.setattr(gate, "DIR_OUTPUT", tmp_path / "output")
        rel = gate.validar("playbooks/nao-existe")
        assert rel["conforme"] is False
        assert "R-PBK-7" in _regras(rel)
