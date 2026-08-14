"""Testes para o reforço da regra 12 em criar-maquina-vendas.py.

`_validar_pos_replace` (GAP 3) só reprova string genérica exata ("Autor
Digital") — substituir por qualquer string aleatória passa o gate. Este
reforço exige que as páginas centrais citem ao menos 1 termo do vocabulário
do nicho/coleção (`sumario_macro.json.motivo_condutor.vocabulario`).
"""

import json
import sys
from pathlib import Path

from conftest import carregar_script

gerador = carregar_script("criar-maquina-vendas.py")


class TestVocabularioDaObra:
    def test_le_vocabulario_do_sumario_macro(self, tmp_path, monkeypatch):
        base = tmp_path / "output"
        dir_obra = base / "livros" / "x"
        dir_obra.mkdir(parents=True)
        (dir_obra / "sumario_macro.json").write_text(
            json.dumps({"motivo_condutor": {"vocabulario": ["fundação", "estrutura"]}}),
            encoding="utf-8",
        )
        monkeypatch.setattr(gerador.TO, "DIR_OUTPUT", base)
        assert gerador._vocabulario_da_obra("livros/x") == ["fundação", "estrutura"]

    def test_sem_sumario_macro_devolve_vazio(self, tmp_path, monkeypatch):
        base = tmp_path / "output"
        (base / "livros" / "x").mkdir(parents=True)
        monkeypatch.setattr(gerador.TO, "DIR_OUTPUT", base)
        assert gerador._vocabulario_da_obra("livros/x") == []

    def test_sem_motivo_condutor_devolve_vazio(self, tmp_path, monkeypatch):
        base = tmp_path / "output"
        dir_obra = base / "livros" / "x"
        dir_obra.mkdir(parents=True)
        (dir_obra / "sumario_macro.json").write_text(json.dumps({}), encoding="utf-8")
        monkeypatch.setattr(gerador.TO, "DIR_OUTPUT", base)
        assert gerador._vocabulario_da_obra("livros/x") == []


class TestValidarVocabularioNicho:
    def test_sem_vocabulario_nao_bloqueia(self, tmp_path):
        assert gerador._validar_vocabulario_nicho(tmp_path, []) == []

    def test_sem_paginas_centrais_nao_bloqueia(self, tmp_path):
        assert gerador._validar_vocabulario_nicho(tmp_path, ["fundação"]) == []

    def test_reprova_pagina_sem_termo_do_vocabulario(self, tmp_path):
        frontend = tmp_path / "frontend" / "app"
        frontend.mkdir(parents=True)
        (frontend / "page.tsx").write_text(
            "export default function Page() { return <div>Copy generica qualquer</div> }",
            encoding="utf-8",
        )
        problemas = gerador._validar_vocabulario_nicho(tmp_path, ["fundação", "estrutura"])
        assert len(problemas) == 1
        assert "page.tsx" in problemas[0]

    def test_aprova_pagina_que_cita_vocabulario(self, tmp_path):
        frontend = tmp_path / "frontend" / "app"
        frontend.mkdir(parents=True)
        (frontend / "page.tsx").write_text(
            "export default function Page() { return <div>Domine a fundação do seu negócio</div> }",
            encoding="utf-8",
        )
        assert gerador._validar_vocabulario_nicho(tmp_path, ["fundação", "estrutura"]) == []

    def test_verifica_paginas_de_email(self, tmp_path):
        emails = tmp_path / "backend" / "emails"
        emails.mkdir(parents=True)
        (emails / "boas-vindas-email.html").write_text("<p>Copy generica sem nicho</p>", encoding="utf-8")
        problemas = gerador._validar_vocabulario_nicho(tmp_path, ["fundação"])
        assert any("email" in p for p in problemas)
