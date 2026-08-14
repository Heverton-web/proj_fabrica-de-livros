"""Testes para scripts/personalizar-nicho.py (banco de nichos declarativo)."""

import importlib.util
import json
import sys
from pathlib import Path

DIR_PROJETO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR_PROJETO / "scripts"))

_spec = importlib.util.spec_from_file_location(
    "personalizar_nicho", DIR_PROJETO / "scripts" / "personalizar-nicho.py"
)
pn = importlib.util.module_from_spec(_spec)
sys.modules["personalizar_nicho"] = pn
_spec.loader.exec_module(pn)


class TestCarregarNichos:
    def test_carrega_nichos_reais_do_banco(self):
        nichos = pn.carregar_nichos()
        segmentos = {n["segmento"] for n in nichos}
        assert "engenharia-de-software" in segmentos
        assert "negocios-e-produtividade" in segmentos

    def test_diretorio_inexistente_devolve_vazio(self, tmp_path):
        assert pn.carregar_nichos(tmp_path / "nao-existe") == []


class TestMelhorNicho:
    NICHOS = [
        {"segmento": "a", "termos_match": ["devops", "arquitetura"]},
        {"segmento": "b", "termos_match": ["vendas", "marketing"]},
    ]

    def test_escolhe_maior_sobreposicao(self):
        vocab = ["DevOps", "Arquitetura", "Pipeline"]
        assert pn.melhor_nicho(vocab, self.NICHOS)["segmento"] == "a"

    def test_sem_sobreposicao_devolve_none(self):
        assert pn.melhor_nicho(["Culinária"], self.NICHOS) is None

    def test_vocabulario_vazio_devolve_none(self):
        assert pn.melhor_nicho([], self.NICHOS) is None


class TestAplicarNicho:
    NICHO = {
        "segmento": "x", "nome_produto_pilar": "Guia X", "publico": "engenheiros",
        "persona": {"nome": "Persona X", "descricao": "d", "dor_principal": "dor",
                     "desejo_principal": "desejo", "objecoes": [], "canais_preferidos": [],
                     "tom_comunicacao": "t"},
        "hashtags": ["tagx"],
    }

    def _maquina_falsa(self, tmp_path):
        destino = tmp_path / "maquina"
        (destino / "config").mkdir(parents=True)
        (destino / "frontend" / "app" / "captura").mkdir(parents=True)
        (destino / "frontend" / "app").mkdir(exist_ok=True)
        (destino / "frontend" / "components").mkdir(parents=True)
        (destino / "config" / "produtos.json").write_text(
            json.dumps({"produtos": [{"nome": "Livro: O Autor Digital"}]}), encoding="utf-8")
        (destino / "config" / "funis.json").write_text(
            json.dumps({"subject": "30% OFF no Autor Digital"}), encoding="utf-8")
        (destino / "frontend" / "app" / "captura" / "page.tsx").write_text(
            "Descubra o método que já ajudou centenas de pessoas.", encoding="utf-8")
        (destino / "frontend" / "app" / "layout.tsx").write_text(
            "description: já ajudou centenas de pessoas.", encoding="utf-8")
        (destino / "frontend" / "components" / "Hero.tsx").write_text(
            "já ajudou centenas de pessoas a mudar de vida.", encoding="utf-8")
        (destino / "config" / "personas.json").write_text(
            json.dumps({"personas": [{"slug": "generica", "nome": "Genérica", "ativo": True}]}),
            encoding="utf-8")
        (destino / "config" / "canais.json").write_text(
            json.dumps({"instagram": {"hashtags": ["existente"]}}), encoding="utf-8")
        return destino

    def test_substitui_produto_pilar(self, tmp_path):
        destino = self._maquina_falsa(tmp_path)
        pn.aplicar_nicho(destino, self.NICHO)
        assert "Autor Digital" not in (destino / "config" / "produtos.json").read_text(encoding="utf-8")
        assert "Guia X" in (destino / "config" / "produtos.json").read_text(encoding="utf-8")

    def test_substitui_prova_social_nas_3_paginas(self, tmp_path):
        destino = self._maquina_falsa(tmp_path)
        pn.aplicar_nicho(destino, self.NICHO)
        for rel in ("frontend/app/captura/page.tsx", "frontend/app/layout.tsx",
                    "frontend/components/Hero.tsx"):
            texto = (destino / rel).read_text(encoding="utf-8")
            assert "centenas de pessoas" not in texto
            assert "centenas de engenheiros" in texto

    def test_prepend_persona_desativa_antigas(self, tmp_path):
        destino = self._maquina_falsa(tmp_path)
        pn.aplicar_nicho(destino, self.NICHO)
        dados = json.loads((destino / "config" / "personas.json").read_text(encoding="utf-8"))
        assert dados["personas"][0]["nome"] == "Persona X"
        assert dados["personas"][0]["ativo"] is True
        assert dados["personas"][1]["ativo"] is False

    def test_adiciona_hashtag_sem_duplicar(self, tmp_path):
        destino = self._maquina_falsa(tmp_path)
        pn.aplicar_nicho(destino, self.NICHO)
        dados = json.loads((destino / "config" / "canais.json").read_text(encoding="utf-8"))
        assert dados["instagram"]["hashtags"] == ["existente", "tagx"]

    def test_restantes_genericos_vazio_apos_aplicar(self, tmp_path):
        destino = self._maquina_falsa(tmp_path)
        pn.aplicar_nicho(destino, self.NICHO)
        assert pn.restantes_genericos(destino) == []

    def test_restantes_genericos_reporta_antes_de_aplicar(self, tmp_path):
        destino = self._maquina_falsa(tmp_path)
        assert len(pn.restantes_genericos(destino)) > 0


class TestHubEDirMaquina:
    def test_hub_da_obra_com_prefixo_de_tipo(self):
        assert pn._hub_da_obra("livros/minha-colecao") == "minha-colecao"

    def test_hub_da_obra_layout_plano(self):
        assert pn._hub_da_obra("minha-obra") == "minha-obra"

    def test_dir_maquina_resolve_sob_hub(self, tmp_path):
        assert pn.dir_maquina("livros/x", base=tmp_path) == tmp_path / "x" / "maquina"
