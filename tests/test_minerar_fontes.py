"""Testes para scripts/minerar-fontes-academicas.py (minerador academico V5.4)."""

import json

import fontes_academicas as FA
from conftest import carregar_script

MIN = carregar_script("minerar-fontes-academicas.py")
VF = carregar_script("validar-fontes.py")


def _registro(titulo, doi=None, fonte="openalex"):
    return {"titulo": titulo, "doi": doi, "url": f"https://doi.org/{doi}" if doi
            else f"https://x.org/{titulo}", "fonte": fonte, "fonte_nome": fonte,
            "classe": "A", "autores": ["Ana Silva"], "ano": 2024, "resumo": None,
            "citacoes": 1, "periodico": None}


class TestMinerar:
    def test_ok_popula_cache(self, monkeypatch):
        def _buscar(fonte, tema, max_por=None):
            return [_registro(f"{fonte}-obra", doi=f"10.1/{fonte}")]
        monkeypatch.setattr(FA, "buscar", _buscar)
        unicos, cobertura, cache = MIN.minerar(
            "tema", ["openalex", "arxiv"], None, False, {})
        assert len(unicos) == 2
        assert cobertura["openalex"]["status"] == "ok"
        assert cobertura["arxiv"]["status"] == "ok"
        assert "openalex|tema" in cache
        assert "arxiv|tema" in cache

    def test_dedup_entre_fontes(self, monkeypatch):
        def _buscar(fonte, tema, max_por=None):
            return [_registro("mesma obra", doi="10.1/igual")]
        monkeypatch.setattr(FA, "buscar", _buscar)
        unicos, _, _ = MIN.minerar(
            "tema", ["openalex", "crossref"], None, False, {})
        assert len(unicos) == 1

    def test_erro_de_fonte_nao_aborta(self, monkeypatch):
        def _buscar(fonte, tema, max_por=None):
            if fonte == "scielo":
                raise FA.FonteIndisponivel("HTTP 403")
            return [_registro(f"{fonte}-obra")]
        monkeypatch.setattr(FA, "buscar", _buscar)
        unicos, cobertura, _ = MIN.minerar(
            "tema", ["openalex", "scielo", "arxiv"], None, False, {})
        assert len(unicos) == 2
        assert cobertura["scielo"]["status"] == "erro"
        assert "403" in cobertura["scielo"]["erro"]
        assert cobertura["openalex"]["status"] == "ok"

    def test_sem_rede_usa_cache(self):
        cache = {"openalex|tema": {"em": "10 ago. 2026",
                                   "registros": [_registro("do cache")]}}
        unicos, cobertura, _ = MIN.minerar(
            "tema", ["openalex"], None, True, cache)
        assert cobertura["openalex"]["status"] == "cache"
        assert len(unicos) == 1

    def test_sem_rede_sem_cache(self):
        unicos, cobertura, _ = MIN.minerar(
            "tema", ["openalex"], None, True, {})
        assert cobertura["openalex"]["status"] == "sem-rede"
        assert unicos == []

    def test_erro_interno_inesperado(self, monkeypatch):
        def _buscar(fonte, tema, max_por=None):
            raise RuntimeError("boom")
        monkeypatch.setattr(FA, "buscar", _buscar)
        _, cobertura, _ = MIN.minerar(
            "tema", ["openalex"], None, False, {})
        assert cobertura["openalex"]["status"] == "erro"
        assert "boom" in cobertura["openalex"]["erro"]


class TestEscreverArtefatos:
    def test_gera_json_e_md(self, tmp_path):
        base = tmp_path / "mineracao_teste"
        unicos = [_registro("Obra Um", doi="10.1/a"),
                  _registro("Obra Dois", doi=None)]
        cobertura = {"openalex": {"status": "ok", "erro": None, "n": 2}}
        json_alvo, md_alvo = MIN.escrever_artefatos(
            base, "meu tema", unicos, cobertura, "10 ago. 2026")

        dados = json.loads(json_alvo.read_text(encoding="utf-8"))
        assert dados["tema"] == "meu tema"
        assert dados["total_unicos"] == 2
        assert dados["cobertura"]["openalex"]["status"] == "ok"

        md = md_alvo.read_text(encoding="utf-8")
        assert "## Fontes brutas" in md
        assert "- SILVA, Ana. *Obra Um*. 2024. Disponível em: https://doi.org/10.1/a." in md
        assert "Acesso em: 10 ago. 2026. (A)" in md
        assert "- OpenAlex: 2 resultados (ok)" in md

    def test_md_aceito_pelo_gate_de_fontes(self, tmp_path):
        """O .md do minerador casa com o contrato do validar-fontes.py (R-FT)."""
        base = tmp_path / "mineracao"
        unicos = [_registro("Obra", doi="10.1/a")]
        cobertura = {"openalex": {"status": "ok", "erro": None, "n": 1}}
        _, md_alvo = MIN.escrever_artefatos(
            base, "tema", unicos, cobertura, "10 ago. 2026")
        classes, linhas = VF.classificar_dossie(md_alvo.read_text(encoding="utf-8"))
        assert classes == {"A": 1, "B": 0, "C": 0}
        assert linhas == 1


class TestMinerarParalelismo:
    """Confirma que as fontes rodam em paralelo de fato (nao so 'nao quebrou')
    — melhorias/21-08-2026-plano-acao-tokens-sob-pericia.md, item C."""

    def test_tempo_de_parede_menor_que_soma_sequencial(self, monkeypatch):
        import time as time_mod

        atraso_por_fonte = 0.2

        def _buscar_lento(fonte, tema, max_por=None):
            time_mod.sleep(atraso_por_fonte)
            return [_registro(f"{fonte}-obra")]

        monkeypatch.setattr(FA, "buscar", _buscar_lento)

        fontes = ["openalex", "crossref", "arxiv", "semantic_scholar",
                  "scielo", "pubmed"]
        inicio = time_mod.perf_counter()
        unicos, cobertura, _ = MIN.minerar("tema", fontes, None, False, {})
        duracao = time_mod.perf_counter() - inicio

        soma_sequencial = len(fontes) * atraso_por_fonte
        assert duracao < soma_sequencial * 0.7, (
            f"esperava paralelismo real (~{soma_sequencial/3:.2f}s), "
            f"levou {duracao:.2f}s (sequencial seria {soma_sequencial:.2f}s)")
        assert len(unicos) == len(fontes)
        assert all(c["status"] == "ok" for c in cobertura.values())

    def test_ordem_de_cobertura_preservada(self, monkeypatch):
        """Mesmo em paralelo, cobertura/dedup mantem a ordem de `fontes`."""
        def _buscar(fonte, tema, max_por=None):
            return [_registro(f"{fonte}-obra")]
        monkeypatch.setattr(FA, "buscar", _buscar)

        fontes = ["scielo", "arxiv", "openalex"]
        _, cobertura, _ = MIN.minerar("tema", fontes, None, False, {})
        assert list(cobertura.keys()) == fontes
