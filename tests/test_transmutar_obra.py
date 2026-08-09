"""Testes do scripts/transmutar-obra.py (V5.2, F5) — reescrita entre tipos.

Cobre: validacao do par contra a matriz, recorte das unidades da origem,
estrutura do destino (slug plano com sufixo), config com rastreabilidade
(slug_origem/modo_producao), copia do dossie, registro em derivados.json da
origem e nao-destruicao da origem.
"""

import json
from pathlib import Path

from conftest import carregar_script

SLUG = "livros/obra-teste"


def _modulo():
    return carregar_script("transmutar-obra.py")


def _ler(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def _playbook_fake(raiz):
    """Playbook origem com 2 cards (passos/passo_01.json e passo_02.json)."""
    dir_pbk = raiz / "playbooks" / "pbk-teste"
    (dir_pbk / "passos").mkdir(parents=True)
    for i, (titulo, objetivo) in enumerate(
            [("Ativar o agente", "Rodar o primeiro agente"),
             ("Validar o gate", "Conferir o smoke test")], 1):
        (dir_pbk / "passos" / f"passo_{i:02d}.json").write_text(
            json.dumps({"titulo": titulo, "objetivo_material": objetivo},
                       ensure_ascii=False), encoding="utf-8")
    return dir_pbk


class TestTransmutarValidacao:
    def test_origem_inexistente(self, livro_falso, redirecionar_output):
        m = _modulo()
        redirecionar_output(m, livro_falso["raiz"])
        r = m.transmutar("livros/obra-fantasma", "tcc",
                         base=livro_falso["raiz"])
        assert "erro" in r and "nao encontrada" in r["erro"]

    def test_par_invalido(self, livro_falso, redirecionar_output):
        m = _modulo()
        redirecionar_output(m, livro_falso["raiz"])
        r = m.transmutar(SLUG, "playbook", base=livro_falso["raiz"])
        assert "erro" in r
        assert "playbook" in r["erro"]

    def test_mesmo_tipo(self, livro_falso, redirecionar_output):
        m = _modulo()
        redirecionar_output(m, livro_falso["raiz"])
        r = m.transmutar(SLUG, "livro", base=livro_falso["raiz"])
        assert "erro" in r and "reescrever" in r["erro"]

    def test_tipo_desconhecido(self, livro_falso, redirecionar_output):
        m = _modulo()
        redirecionar_output(m, livro_falso["raiz"])
        r = m.transmutar(SLUG, "holograma", base=livro_falso["raiz"])
        assert "erro" in r


class TestTransmutarLivroParaTcc:
    def test_cria_estrutura_e_recorte(self, livro_falso, redirecionar_output):
        m = _modulo()
        redirecionar_output(m, livro_falso["raiz"])

        r = m.transmutar(SLUG, "tcc", base=livro_falso["raiz"])
        assert "erro" not in r, r.get("erro")
        assert r["tipo_destino"] == "tcc"
        assert r["slug_destino"] == "tccs/obra-teste--tcc"
        assert r["unidades"] == 2

        destino = livro_falso["raiz"] / "tccs" / "obra-teste--tcc"
        for sub in ("capitulos", "revisao", "imagens"):
            assert (destino / sub).is_dir(), f"falta {sub}/"

        sumario = _ler(destino / "sumario_macro.json")
        assert sumario["tipo_obra"] == "tcc"
        assert sumario["slug_origem"] == SLUG
        assert sumario["tipo_origem"] == "livro"
        titulos = [c["titulo"] for p in sumario["partes"] for c in p["capitulos"]]
        assert titulos == ["Fundação do Projeto", "Teoria Pura"]
        assert sumario["motivo_condutor"]["nome"] == "A Obra em Construção"

        cfg = _ler(destino / "config_obra.json")
        assert cfg["modo_producao"] == "transmutacao"
        assert cfg["slug_origem"] == SLUG
        assert cfg["tipo_origem"] == "livro"
        assert cfg["tipo_obra"] == "tcc"
        assert "A Obra em Construção" in cfg["tema"]
        assert cfg["serie"] == "Colecao Teste"
        assert cfg["senioridade_obra"] == "intermediario"

        relatorio = _ler(destino / "revisao" / "relatorio_transmutacao.json")
        assert relatorio["unidades"] == 2
        assert relatorio["slug_origem"] == SLUG

    def test_origem_intacta_e_derivados_registrados(self, livro_falso,
                                                    redirecionar_output):
        m = _modulo()
        redirecionar_output(m, livro_falso["raiz"])
        cap_01_antes = (livro_falso["dir_livro"] / "capitulos" / "cap_01.md") \
            .read_text(encoding="utf-8")

        m.transmutar(SLUG, "tcc", base=livro_falso["raiz"])

        # origem intacta
        assert (livro_falso["dir_livro"] / "capitulos" / "cap_01.md") \
            .read_text(encoding="utf-8") == cap_01_antes
        # registro no derivados.json da origem
        derivados = _ler(livro_falso["dir_livro"] / "derivados.json")
        itens = derivados["tccs"]["itens"]
        assert len(itens) == 1
        assert itens[0]["transmutacao"] is True
        assert itens[0]["slug"] == "obra-teste--tcc"
        assert itens[0]["diretorio"] == "tccs/obra-teste--tcc"

    def test_novo_slug_personalizado(self, livro_falso, redirecionar_output):
        m = _modulo()
        redirecionar_output(m, livro_falso["raiz"])
        r = m.transmutar(SLUG, "tcc", novo_slug="tcc-custom",
                         base=livro_falso["raiz"])
        assert r["slug_destino"] == "tccs/tcc-custom"
        assert (livro_falso["raiz"] / "tccs" / "tcc-custom" /
                "config_obra.json").exists()

    def test_dossie_copiado(self, livro_falso, redirecionar_output):
        m = _modulo()
        redirecionar_output(m, livro_falso["raiz"])
        (livro_falso["dir_livro"] / "pesquisa").mkdir(exist_ok=True)
        (livro_falso["dir_livro"] / "pesquisa" / "dossie_01.md").write_text(
            "# Dossie\nfonte real.", encoding="utf-8")

        r = m.transmutar(SLUG, "tcc", base=livro_falso["raiz"])
        assert r["dossie_copiados"] == 1
        destino = livro_falso["raiz"] / "tccs" / "obra-teste--tcc"
        assert (destino / "pesquisa" / "dossie_01.md").exists()


class TestTransmutarPlaybookParaLivro:
    def test_recorte_dos_cards(self, livro_falso, redirecionar_output):
        m = _modulo()
        redirecionar_output(m, livro_falso["raiz"])
        _playbook_fake(livro_falso["raiz"])

        r = m.transmutar("playbooks/pbk-teste", "livro",
                         base=livro_falso["raiz"])
        assert "erro" not in r, r.get("erro")
        assert r["slug_destino"] == "livros/pbk-teste--liv"
        assert r["unidades"] == 2

        destino = livro_falso["raiz"] / "livros" / "pbk-teste--liv"
        sumario = _ler(destino / "sumario_macro.json")
        titulos = [c["titulo"] for p in sumario["partes"] for c in p["capitulos"]]
        assert titulos == ["Ativar o agente", "Validar o gate"]
        objetivos = [c["objetivo"] for p in sumario["partes"]
                     for c in p["capitulos"]]
        assert objetivos == ["Rodar o primeiro agente", "Conferir o smoke test"]

        cfg = _ler(destino / "config_obra.json")
        assert cfg["modo_producao"] == "transmutacao"
        assert cfg["tipo_origem"] == "playbook"
