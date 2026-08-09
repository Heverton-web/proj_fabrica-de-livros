"""Testes da regra 1:1 (1 máquina por COLEÇÃO em output/<hub>/maquina) e do
vínculo com campanhas (snapshot maquina/campanhas/) — V5.3.

Cobre R-MQ-1..5 do plano `melhorias/09-08-2026-maquina-1por-colecao-usa-campanhas.md`:
destino canônico, cardinalidade, snapshot, manifesto da coleção, empacotamento.
"""

import json

import pytest

import tipos_obra as TO
from conftest import carregar_script

gerador = carregar_script("criar-maquina-vendas.py")
colecao = carregar_script("colecao.py")
empacotador = carregar_script("empacotar-colecao.py")


@pytest.fixture
def ambiente(tmp_path, monkeypatch):
    """output/ isolado com hub 'meu-hub': 2 livros + campanhas do hub."""
    raiz = tmp_path / "output"

    def _material(rel, tema):
        p = raiz / rel
        (p / "capitulos").mkdir(parents=True)
        (p / "capitulos" / "cap_01.md").write_text("# Cap 1\n\nConteudo.\n",
                                                   encoding="utf-8")
        (p / "config_obra.json").write_text(json.dumps({
            "tema": tema, "tipo_obra": "livro", "serie": "Minha Coleção",
        }, ensure_ascii=False), encoding="utf-8")
        (p / "sumario_macro.json").write_text(
            json.dumps({"titulo_obra": tema}), encoding="utf-8")

    _material("meu-hub/livros/l1-x", "Livro Um")
    _material("meu-hub/livros/l2-x", "Livro Dois")

    camp = raiz / "meu-hub" / "campanhas"
    post = camp / "l1-x" / "redes-sociais" / "instagram" / "textos" / "post"
    post.mkdir(parents=True)
    (post / "post-01.md").write_text("Post final da campanha", encoding="utf-8")
    (camp / "campanha.json").write_text(json.dumps({
        "colecao": "Minha Coleção", "atualizado_em": "2026-08-09",
        "materiais": [{"slug": "meu-hub/livros/l1-x"}], "total_materiais": 1,
    }, ensure_ascii=False), encoding="utf-8")

    monkeypatch.setattr(TO, "DIR_OUTPUT", raiz)
    return {"raiz": raiz}


@pytest.fixture
def colecao_redirecionada(ambiente, monkeypatch):
    """Aponta colecao.py/series_capa para o output isolado (padrão V5.2)."""
    import series_capa as sc
    raiz = ambiente["raiz"]
    monkeypatch.setattr(colecao, "DIR_OUTPUT", raiz)
    monkeypatch.setattr(colecao, "DIR_COLECOES", raiz / "colecoes")
    monkeypatch.setattr(sc, "DIR_OUTPUT", raiz)
    monkeypatch.setattr(sc, "CAMINHO_REGISTRO", raiz / "series.json")
    return raiz


def _manifesto_maquina(raiz):
    return json.loads((raiz / "meu-hub" / "maquina" / "manifesto.json")
                      .read_text(encoding="utf-8"))


# ── R-MQ-1: destino canônico ─────────────────────────────────────────────────

class TestDestinoCanonico:
    def test_maquina_vive_no_hub_da_colecao(self, ambiente):
        raiz = ambiente["raiz"]
        gerador.criar_maquina("meu-hub/livros/l1-x", tipo="completo")

        destino = raiz / "meu-hub" / "maquina"
        assert (destino / "manifesto.json").is_file()
        assert not (raiz / "marketing").exists(), (
            "nada em marketing/maquinas (raiz) — caminho morto")

        man = _manifesto_maquina(raiz)
        assert man["colecao"] == "meu-hub"
        assert man["maquina_em"] == "output/meu-hub/maquina"

    def test_obra_plana_vira_propria_colecao(self, ambiente):
        raiz = ambiente["raiz"]
        (raiz / "livros" / "obra-plana").mkdir(parents=True)
        gerador.criar_maquina("livros/obra-plana", tipo="completo")
        assert (raiz / "obra-plana" / "maquina" / "manifesto.json").is_file()


# ── R-MQ-2: cardinalidade 1:1 ────────────────────────────────────────────────

class TestCardinalidade:
    def test_1por1_recusa_segunda_obra_do_mesmo_hub(self, ambiente, monkeypatch):
        raiz = ambiente["raiz"]
        gerador.criar_maquina("meu-hub/livros/l1-x", tipo="completo")
        monkeypatch.setattr("builtins.input", lambda *a, **k: "s")

        assert gerador.criar_maquina("meu-hub/livros/l2-x", tipo="completo") is None
        man = _manifesto_maquina(raiz)
        assert "l1-x" in man["obra_origem"], (
            "manifesto original preservado — a 2ª obra não sobrescreveu")

    def test_mesma_obra_pode_sobrescrever(self, ambiente, monkeypatch):
        raiz = ambiente["raiz"]
        gerador.criar_maquina("meu-hub/livros/l1-x", tipo="completo")
        monkeypatch.setattr("builtins.input", lambda *a, **k: "s")
        destino = gerador.criar_maquina("meu-hub/livros/l1-x", tipo="completo")
        assert destino is not None
        assert (destino / "manifesto.json").is_file()


# ── R-MQ-3: snapshot de campanhas ────────────────────────────────────────────

class TestSnapshotCampanhas:
    def test_maquina_traz_snapshot_de_campanhas(self, ambiente):
        raiz = ambiente["raiz"]
        gerador.criar_maquina("meu-hub/livros/l1-x", tipo="completo")

        snap = raiz / "meu-hub" / "maquina" / "campanhas"
        assert (snap / "campanha.json").is_file()
        copia = snap / "l1-x" / "redes-sociais" / "instagram" / "textos" / "post"
        assert (copia / "post-01.md").is_file(), "artefato de campanha no snapshot"

        meta = json.loads((snap / "snapshot.json").read_text(encoding="utf-8"))
        assert meta["atualizado_em"] == "2026-08-09"
        assert meta["origem"] == "meu-hub/campanhas"

        man = _manifesto_maquina(raiz)
        assert man["campanhas"]["snapshot"] is True
        assert man["campanhas"]["material_ancora"] == "l1-x"

    def test_sem_campanhas_maquina_fica_sem_snapshot(self, ambiente):
        raiz = ambiente["raiz"]
        import shutil
        shutil.rmtree(raiz / "meu-hub" / "campanhas")
        gerador.criar_maquina("meu-hub/livros/l1-x", tipo="completo")
        assert not (raiz / "meu-hub" / "maquina" / "campanhas").exists()
        man = _manifesto_maquina(raiz)
        assert man["campanhas"]["snapshot"] is False


# ── R-MQ-4: manifesto da coleção ─────────────────────────────────────────────

class TestManifestoDaColecao:
    def test_colecao_registra_maquina(self, ambiente, colecao_redirecionada):
        raiz = ambiente["raiz"]
        gerador.criar_maquina("meu-hub/livros/l1-x", tipo="completo")
        colecao.sincronizar()

        man = colecao.carregar("Minha Coleção")
        assert man is not None
        assert man["maquina"]["slug"] == "meu-hub/livros/l1-x"
        assert man["maquina"]["status"] == "criada"
        assert man["maquina"]["campanhas"]["snapshot"] is True
        assert man["maquina"]["campanhas"]["desatualizada"] is False
        assert man["maquinas_legadas"] == []

    def test_maquinas_legadas_sinalizadas(self, ambiente, colecao_redirecionada):
        raiz = ambiente["raiz"]
        (raiz / "meu-hub" / "marketing" / "legada-1").mkdir(parents=True)
        gerador.criar_maquina("meu-hub/livros/l1-x", tipo="completo")
        colecao.sincronizar()

        man = colecao.carregar("Minha Coleção")
        assert man["maquinas_legadas"] == ["legada-1"]

    def test_sem_maquina_manifesto_diz_nulo(self, ambiente, colecao_redirecionada):
        colecao.sincronizar()
        man = colecao.carregar("Minha Coleção")
        assert man["maquina"] is None
        assert man["maquinas_legadas"] == []


# ── R-MQ-5: empacotamento ────────────────────────────────────────────────────

class TestEmpacotamento:
    def test_pacote_carrega_maquina(self, ambiente, colecao_redirecionada, monkeypatch):
        raiz = ambiente["raiz"]
        gerador.criar_maquina("meu-hub/livros/l1-x", tipo="completo")
        colecao.sincronizar()

        monkeypatch.setattr(empacotador, "DIR_OUTPUT", raiz)
        monkeypatch.setattr(empacotador, "DIR_PACOTES", raiz / "distribuicao")
        meta = empacotador.empacotar("Minha Coleção")
        assert meta is not None

        pacote = raiz / meta["pacote"]
        assert (pacote / "maquina" / "manifesto.json").is_file()
        assert (pacote / "maquina" / "campanhas" / "snapshot.json").is_file()
        leia_me = (pacote / "LEIA-ME.md").read_text(encoding="utf-8")
        assert "## Máquina de vendas" in leia_me
