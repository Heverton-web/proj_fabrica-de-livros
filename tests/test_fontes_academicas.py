"""Testes para scripts/fontes_academicas.py (registro declarativo de bases academicas)."""

import importlib.util
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

_spec = importlib.util.spec_from_file_location(
    "fontes_academicas",
    Path(__file__).resolve().parent.parent / "scripts" / "fontes_academicas.py",
)
FA = importlib.util.module_from_spec(_spec)
sys.modules["fontes_academicas"] = FA
_spec.loader.exec_module(FA)


class TestRegistro:
    def test_fontes_validas_incluem_bases_core(self):
        validas = FA.fontes_validas()
        for esperada in ("openalex", "crossref", "arxiv",
                         "semantic_scholar", "scielo", "pubmed"):
            assert esperada in validas

    def test_todas_as_fontes_tem_campos_minimos(self):
        for fonte, d in FA.FONTES_ACADEMICAS.items():
            for campo in ("nome", "classificacao", "max_padrao",
                          "fetch", "parser", "cobre"):
                assert campo in d, f"{fonte} sem {campo}"
            assert d["fetch"] in FA.FUNCOES_FETCH, f"{fonte}: fetch inexistente"
            assert d["parser"] in FA.PARSERS, f"{fonte}: parser inexistente"
            assert d["classificacao"] in ("A", "B", "C")

    def test_descriptor_desconhecido_levanta(self):
        with pytest.raises(KeyError):
            FA.descritor("base-inexistente")

    def test_todas_classificacao_a(self):
        assert all(d["classificacao"] == "A"
                   for d in FA.FONTES_ACADEMICAS.values())


class TestNomeAbnt:
    def test_nome_simples(self):
        assert FA._nome_abnt("Carlos E. Jimenez") == "JIMENEZ, Carlos E."

    def test_nome_ja_com_familia(self):
        assert FA._nome_abnt("Martinez-Fernandez, Silverio") == \
            "MARTINEZ-FERNANDEZ, Silverio"

    def test_nome_com_escape_latex(self):
        assert FA._nome_abnt(r"Mart\'inez-Fern\'andez, Silverio") == \
            "MARTINEZ-FERNANDEZ, Silverio"

    def test_nome_sobrenome_unico(self):
        assert FA._nome_abnt("OpenAI") == "OPENAI"


class TestFormatoAbnt:
    def test_um_autor(self):
        r = {"titulo": "Titulo da Obra", "autores": ["Carlos E. Jimenez"],
             "ano": 2024, "url": "https://arxiv.org/abs/1", "classe": "A"}
        linha = FA.formato_abnt(r, data_acesso="10 ago. 2026")
        assert linha == ("- JIMENEZ, Carlos E. *Titulo da Obra*. 2024. "
                         "Disponível em: https://arxiv.org/abs/1. "
                         "Acesso em: 10 ago. 2026. (A)")

    def test_muitos_autores_et_al(self):
        r = {"titulo": "Obra", "autores": ["Ana Silva", "Bruno Costa",
                                           "Carlos Dias", "Diana Reis"],
             "ano": 2020, "url": "https://doi.org/10.1/x", "classe": "A"}
        linha = FA.formato_abnt(r, data_acesso="10 ago. 2026")
        assert linha.startswith("- SILVA, Ana et al.")
        assert "et al.." not in linha

    def test_sem_autores(self):
        r = {"titulo": "Obra", "autores": [], "ano": None,
             "url": "https://x.org/1", "classe": "A"}
        linha = FA.formato_abnt(r, data_acesso="10 ago. 2026")
        assert linha.startswith("- AUTOR. *Obra*.")

    def test_com_periodico_e_doi(self):
        r = {"titulo": "Obra", "autores": ["Ana Silva"], "ano": 2021,
             "doi": "10.1000/abc", "url": "https://doi.org/10.1000/abc",
             "periodico": "Revista X", "classe": "A"}
        linha = FA.formato_abnt(r, data_acesso="10 ago. 2026")
        assert "In: Revista X." in linha
        assert "Disponível em: https://doi.org/10.1000/abc." in linha


class TestDeduplicar:
    def test_dedup_por_doi(self):
        regs = [
            {"titulo": "A", "doi": "10.1/a", "fonte": "crossref"},
            {"titulo": "A (mesmo DOI)", "doi": "10.1/a", "fonte": "openalex"},
        ]
        unicos = FA.deduplicar(regs)
        assert len(unicos) == 1
        assert unicos[0]["fonte"] == "crossref"

    def test_dedup_por_titulo_sem_doi(self):
        regs = [
            {"titulo": "Obra Importante!", "doi": None, "fonte": "arxiv"},
            {"titulo": "Obra importante", "doi": None, "fonte": "crossref"},
        ]
        unicos = FA.deduplicar(regs)
        assert len(unicos) == 1

    def test_mantem_distintos(self):
        regs = [
            {"titulo": "A", "doi": "10.1/a", "fonte": "c"},
            {"titulo": "B", "doi": "10.1/b", "fonte": "c"},
        ]
        assert len(FA.deduplicar(regs)) == 2


class TestParsers:
    def test_parse_openalex(self):
        payload = [{"results": [{
            "title": "Software Engineering for AI-Based Systems: A Survey",
            "publication_year": 2021,
            "doi": "https://doi.org/10.1145/3487043",
            "cited_by_count": 310,
            "primary_location": {
                "landing_page_url": "http://arxiv.org/abs/2105.01984",
                "source": {"display_name": "arXiv (Cornell University)"}},
            "authorships": [
                {"author": {"display_name": r"Mart\'inez-Fern\'andez, Silverio"}},
                {"author": {"display_name": "Justus Bogner"}}],
            "abstract_inverted_index": {"Software": [0], "engenharia": [1]},
        }]}]
        regs = FA._parse_openalex(payload)
        assert len(regs) == 1
        r = regs[0]
        assert r["doi"] == "10.1145/3487043"
        assert r["ano"] == 2021
        assert r["citacoes"] == 310
        assert r["periodico"] == "arXiv (Cornell University)"
        assert r["url"] == "http://arxiv.org/abs/2105.01984"
        assert r["resumo"] == "Software engenharia"
        assert "Martinez-Fernandez" in r["autores"][0]

    def test_parse_crossref(self):
        payload = [{"message": {"items": [{
            "title": ["AI Agents + Automation"],
            "author": [{"family": "Ponce", "given": "Julio, author"},
                       {"family": "Soto", "given": "A Willy"}],
            "DOI": "10.1002/abc",
            "URL": "https://doi.org/10.1002/abc",
            "issued": {"date-parts": [[2026, 1, 23]]},
            "container-title": ["Untangling AI"],
            "is-referenced-by-count": 5,
        }]}}]
        regs = FA._parse_crossref(payload)
        r = regs[0]
        assert r["titulo"] == "AI Agents + Automation"
        assert r["autores"] == ["Ponce, Julio", "Soto, A Willy"]
        assert r["ano"] == 2026
        assert r["doi"] == "10.1002/abc"
        assert r["citacoes"] == 5

    def test_parse_arxiv(self):
        xml_ = """<?xml version="1.0"?>
        <feed xmlns="http://www.w3.org/2005/Atom"
              xmlns:arxiv="http://arxiv.org/schemas/atom">
          <entry>
            <title>Agent-Driven Software Improvement</title>
            <author><name>Fernando Vallecillos Ruiz</name></author>
            <published>2024-06-15T00:00:00Z</published>
            <id>http://arxiv.org/abs/2406.16739</id>
            <summary>Resumo do trabalho.</summary>
            <arxiv:doi>10.48550/arXiv.2406.16739</arxiv:doi>
          </entry>
        </feed>"""
        regs = FA._parse_arxiv([ET.fromstring(xml_)])
        r = regs[0]
        assert r["titulo"] == "Agent-Driven Software Improvement"
        assert r["autores"] == ["Fernando Vallecillos Ruiz"]
        assert r["ano"] == 2024
        assert r["url"] == "http://arxiv.org/abs/2406.16739"
        assert r["doi"] == "10.48550/arXiv.2406.16739"
        assert r["periodico"] == "arXiv"

    def test_parse_semantic_scholar(self):
        payload = [{"data": [{
            "title": "ReAct",
            "authors": [{"name": "Shunyu Yao"}, {"name": "Anonymo"}],
            "year": 2023, "venue": "ICLR",
            "externalIds": {"DOI": "10.48550/arXiv.2210.03629"},
            "url": "https://www.semanticscholar.org/paper/1",
            "citationCount": 1200,
        }]}]
        r = FA._parse_semantic_scholar(payload)[0]
        assert r["titulo"] == "ReAct"
        assert r["ano"] == 2023
        assert r["citacoes"] == 1200
        assert r["doi"] == "10.48550/arXiv.2210.03629"

    def test_parse_scielo_dict_e_lista(self):
        dict_shape = [{"records": {"records": [
            {"title": ["Artigo em PT"], "author": ["Fulano, A."],
             "year": "2022", "doi": "10.1590/1",
             "url": "https://doi.org/10.1590/1",
             "journal_title": ["Revista Científica"]}]}}]
        r = FA._parse_scielo(dict_shape)[0]
        assert r["titulo"] == "Artigo em PT"
        assert r["ano"] == 2022

        list_shape = [{"records": [
            {"title": "Outro", "authors": ["Ciclano, B."],
             "publication_year": 2021, "uri": "https://x.org/2"}]}]
        r2 = FA._parse_scielo(list_shape)[0]
        assert r2["titulo"] == "Outro"
        assert r2["url"] == "https://x.org/2"

    def test_parse_pubmed(self):
        esearch = {"esearchresult": {"idlist": ["123", "456"]}}
        esummary = {"result": {
            "123": {"title": "Estudo de Saude", "pubdate": "2023-05-01",
                    "fulljournalname": "Rev Med",
                    "authors": [{"name": "Carla Souza"}],
                    "articleids": [{"idtype": "doi", "value": "10.10/med"}]},
            "456": {"title": "Sem DOI", "pubdate": "2020",
                    "authors": []},
        }}
        regs = FA._parse_pubmed([esearch, esummary])
        assert len(regs) == 2
        assert regs[0]["doi"] == "10.10/med"
        assert regs[0]["url"] == "https://pubmed.ncbi.nlm.nih.gov/123/"
        assert regs[0]["ano"] == 2023
        assert regs[1]["autores"] == []


class TestBuscar:
    def test_buscar_anexa_fonte_e_classe(self, monkeypatch):
        payload = [{"results": [{
            "title": "Obra", "publication_year": 2024,
            "primary_location": {"source": {"display_name": None}},
            "authorships": []}]}]
        monkeypatch.setattr(FA, "FUNCOES_FETCH", {
            "_fetch_openalex": lambda q, n: payload})
        regs = FA.buscar("openalex", "tema")
        assert len(regs) == 1
        assert regs[0]["fonte"] == "openalex"
        assert regs[0]["fonte_nome"] == "OpenAlex"
        assert regs[0]["classe"] == "A"

    def test_buscar_sem_doi_sem_url_anexa_doi_org(self, monkeypatch):
        payload = [{"results": [{
            "title": "Obra", "publication_year": 2024,
            "doi": "https://doi.org/10.1/x",
            "primary_location": {"source": {"display_name": None}},
            "authorships": []}]}]
        monkeypatch.setattr(FA, "FUNCOES_FETCH", {
            "_fetch_openalex": lambda q, n: payload})
        r = FA.buscar("openalex", "tema")[0]
        assert r["url"] == "https://doi.org/10.1/x"

    def test_buscar_fonte_indisponivel(self, monkeypatch):
        def _falha(q, n):
            raise FA.FonteIndisponivel("HTTP 429")
        monkeypatch.setattr(FA, "FUNCOES_FETCH", {
            "_fetch_semantic_scholar": _falha})
        with pytest.raises(FA.FonteIndisponivel):
            FA.buscar("semantic_scholar", "tema")


class TestFetchArxiv:
    def _capturar(self, monkeypatch):
        urls = []
        def _capturar(url):
            urls.append(url)
            return ET.fromstring("<feed xmlns='http://www.w3.org/2005/Atom'/>")
        monkeypatch.setattr(FA, "_http_get_atom", _capturar)
        return urls

    def test_arxiv_une_termos_com_and(self, monkeypatch):
        urls = self._capturar(monkeypatch)
        FA._fetch_arxiv("agentes inteligencia artificial", 5)
        assert urls and "search_query=all:agentes+AND+all:inteligencia" in urls[0]
        assert "de" not in urls[0]

    def test_arxiv_query_vazia_apos_stopwords(self, monkeypatch):
        urls = self._capturar(monkeypatch)
        FA._fetch_arxiv("de e em", 3)
        assert "search_query=all:de+e+em" in urls[0]
