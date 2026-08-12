"""Testes para scripts/validar-capa-nivel.py"""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

# Import dinamico (hifen no nome do arquivo impede import direto)
_spec = importlib.util.spec_from_file_location(
    "validar_capa_nivel",
    Path(__file__).resolve().parent.parent / "scripts" / "validar-capa-nivel.py",
)
vcn = importlib.util.module_from_spec(_spec)
sys.modules["validar_capa_nivel"] = vcn
_spec.loader.exec_module(vcn)


class TestRotuloEsperado:
    """Testa a funcao rotulo_esperado() que mapeia senioridade -> rotulo do badge."""

    def test_iniciante(self):
        assert vcn.rotulo_esperado("iniciante") == "PARA INICIANTES"

    def test_intermediario_sem_acento(self):
        assert vcn.rotulo_esperado("intermediario") == "NÍVEL INTERMEDIÁRIO"

    def test_intermediario_com_acento(self):
        assert vcn.rotulo_esperado("intermediário") == "NÍVEL INTERMEDIÁRIO"

    def test_avancado_sem_acento(self):
        assert vcn.rotulo_esperado("avancado") == "NÍVEL AVANÇADO"

    def test_avancado_com_acento(self):
        assert vcn.rotulo_esperado("avançado") == "NÍVEL AVANÇADO"

    def test_case_insensitive(self):
        assert vcn.rotulo_esperado("INICIANTE") == "PARA INICIANTES"
        assert vcn.rotulo_esperado("Avancado") == "NÍVEL AVANÇADO"

    def test_com_espacos(self):
        assert vcn.rotulo_esperado("  intermediario  ") == "NÍVEL INTERMEDIÁRIO"

    def test_invalido_retorna_none(self):
        assert vcn.rotulo_esperado("expert") is None
        assert vcn.rotulo_esperado("junior") is None
        assert vcn.rotulo_esperado("") is None
        assert vcn.rotulo_esperado(None) is None


class TestValidarCapaNivel:
    """Testa a funcao validar_capa_nivel() com fixtures temporarias."""

    def test_config_ausente(self, tmp_path):
        result = vcn.validar_capa_nivel(tmp_path)
        assert result == 1

    def test_senioridade_ausente(self, tmp_path):
        config = {"titulo": "Teste"}
        (tmp_path / "config_obra.json").write_text(json.dumps(config), encoding="utf-8")
        result = vcn.validar_capa_nivel(tmp_path)
        assert result == 1

    def test_senioridade_invalida(self, tmp_path):
        config = {"senioridade_obra": "expert"}
        (tmp_path / "config_obra.json").write_text(json.dumps(config), encoding="utf-8")
        result = vcn.validar_capa_nivel(tmp_path)
        assert result == 1

    def test_capa_html_ausente(self, tmp_path):
        config = {"senioridade_obra": "iniciante"}
        (tmp_path / "config_obra.json").write_text(json.dumps(config), encoding="utf-8")
        result = vcn.validar_capa_nivel(tmp_path)
        assert result == 1

    def test_badge_ausente_no_html(self, tmp_path):
        config = {"senioridade_obra": "iniciante"}
        (tmp_path / "config_obra.json").write_text(json.dumps(config), encoding="utf-8")
        (tmp_path / "capa.html").write_text("<html><body>Sem badge</body></html>", encoding="utf-8")
        result = vcn.validar_capa_nivel(tmp_path)
        assert result == 1

    def test_badge_incorreto(self, tmp_path):
        config = {"senioridade_obra": "iniciante"}
        (tmp_path / "config_obra.json").write_text(json.dumps(config), encoding="utf-8")
        (tmp_path / "capa.html").write_text(
            '<html><body><div class="badge">NÍVEL AVANÇADO</div></body></html>',
            encoding="utf-8",
        )
        result = vcn.validar_capa_nivel(tmp_path)
        assert result == 1

    def test_badge_correto(self, tmp_path):
        config = {"senioridade_obra": "iniciante"}
        (tmp_path / "config_obra.json").write_text(json.dumps(config), encoding="utf-8")
        (tmp_path / "capa.html").write_text(
            '<html><body><div class="badge">PARA INICIANTES</div></body></html>',
            encoding="utf-8",
        )
        result = vcn.validar_capa_nivel(tmp_path)
        assert result == 0

    def test_todas_as_senioridades(self, tmp_path):
        for sen, badge_esperado in [
            ("iniciante", "PARA INICIANTES"),
            ("intermediario", "NÍVEL INTERMEDIÁRIO"),
            ("avancado", "NÍVEL AVANÇADO"),
        ]:
            config = {"senioridade_obra": sen}
            (tmp_path / "config_obra.json").write_text(json.dumps(config), encoding="utf-8")
            (tmp_path / "capa.html").write_text(
                f'<html><body><div class="badge">{badge_esperado}</div></body></html>',
                encoding="utf-8",
            )
            result = vcn.validar_capa_nivel(tmp_path)
            assert result == 0, f"Falhou para senioridade={sen}"


class TestMainResolveHub:
    """Regressao (RTK Scratchpad 2026-08-09): main() so validava o layout plano
    output/livros/<slug> e nunca resolvia a obra no HUB POR COLECAO
    output/<colecao>/livros/<slug> — tipo_por_prefixo(slug) devolve None quando
    o 1o segmento do slug e a colecao, nao o tipo, e main() precisa cair no
    fallback de ler tipo_obra do config_obra.json (R5: badge so livro/ebook)."""

    def _obra(self, tmp_path, *partes, senioridade="iniciante", tipo_obra="livro",
              badge="PARA INICIANTES", com_capa=True):
        dir_obra = tmp_path.joinpath(*partes)
        dir_obra.mkdir(parents=True)
        config = {"senioridade_obra": senioridade, "tipo_obra": tipo_obra}
        (dir_obra / "config_obra.json").write_text(json.dumps(config), encoding="utf-8")
        if com_capa:
            (dir_obra / "capa.html").write_text(
                f'<html><body><div class="badge">{badge}</div></body></html>',
                encoding="utf-8",
            )
        return dir_obra

    def test_resolve_layout_hub_por_colecao(self, tmp_path, monkeypatch):
        self._obra(tmp_path, "minha-colecao", "livros", "obra-x")
        monkeypatch.setattr(vcn.TO, "DIR_OUTPUT", tmp_path)
        monkeypatch.setattr(sys, "argv", ["validar-capa-nivel.py", "minha-colecao/livros/obra-x"])
        assert vcn.main() == 0

    def test_resolve_layout_plano_continua_funcionando(self, tmp_path, monkeypatch):
        self._obra(tmp_path, "livros", "obra-x")
        monkeypatch.setattr(vcn.TO, "DIR_OUTPUT", tmp_path)
        monkeypatch.setattr(sys, "argv", ["validar-capa-nivel.py", "livros/obra-x"])
        assert vcn.main() == 0

    def test_escopo_r5_reprova_tipo_fora_de_livro_ebook_no_hub(self, tmp_path, monkeypatch):
        self._obra(tmp_path, "minha-colecao", "tccs", "tcc-x", tipo_obra="tcc", com_capa=False)
        monkeypatch.setattr(vcn.TO, "DIR_OUTPUT", tmp_path)
        monkeypatch.setattr(sys, "argv", ["validar-capa-nivel.py", "minha-colecao/tccs/tcc-x"])
        assert vcn.main() == 1
