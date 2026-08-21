"""Testes para scripts/validar-comandos-cli.py (gate F2 — comandos/CLI verificados).

Aplica o protocolo pericial do livro "Tokens Sob Perícia" (melhorias/
21-08-2026-plano-acao-tokens-sob-pericia.md, item A): bloco de código marcado
`confere=false` reprova (R-CLI-1); sem marcação vira pendência, nunca reprova
sozinho — o mesmo princípio do livro ("NÃO_VERIFICÁVEL != aprovado").
"""

import json

import pytest

from conftest import carregar_script

gate = carregar_script("validar-comandos-cli.py")
PO = carregar_script("parametros_obra.py")


def _md(secoes):
    """Monta markdown EITA com pares (numero, titulo, corpo)."""
    partes = ["# Capítulo 1\n"]
    for num, titulo, corpo in secoes:
        partes.append(f"\n## {num}. {titulo}\n\n{corpo}")
    return "\n".join(partes) + "\n"


class TestAnalisarCapitulo:
    def test_bloco_confirmado(self):
        texto = _md([
            (4, "Técnica",
             "```bash\nnpx ccusage@latest daily\n```\n"
             "<!-- cli-check: fonte=B; confere=true -->"),
        ])
        blocos = gate.analisar_capitulo(texto, "cap_1")
        assert len(blocos) == 1
        assert blocos[0]["status"] == "confirmado"
        assert blocos[0]["fonte"] == "B"

    def test_bloco_fabricado(self):
        texto = _md([
            (4, "Técnica",
             "```bash\npipx install ccusage\n```\n"
             "<!-- cli-check: fonte=B; confere=false -->"),
        ])
        blocos = gate.analisar_capitulo(texto, "cap_1")
        assert len(blocos) == 1
        assert blocos[0]["status"] == "fabricado"

    def test_bloco_sem_marcacao_vira_nao_verificado(self):
        texto = _md([
            (4, "Técnica", "```bash\ngit status\n```"),
        ])
        blocos = gate.analisar_capitulo(texto, "cap_1")
        assert len(blocos) == 1
        assert blocos[0]["status"] == "nao_verificado"
        assert blocos[0]["fonte"] is None

    def test_marcacao_distante_nao_conta(self):
        """Marcacao so vale se vier IMEDIATAMENTE apos o fechamento do bloco —
        um paragrafo no meio nao "acha" uma marcacao mais adiante no texto."""
        texto = _md([
            (4, "Técnica",
             "```bash\ngit status\n```\n\n"
             "Algum texto explicativo entre o bloco e a marcacao.\n\n"
             "<!-- cli-check: fonte=B; confere=true -->"),
        ])
        blocos = gate.analisar_capitulo(texto, "cap_1")
        assert len(blocos) == 1
        assert blocos[0]["status"] == "nao_verificado"

    def test_mermaid_ignorado(self):
        texto = _md([
            (3, "Ilustra", "```mermaid\ngraph TD\n  A --> B\n```"),
        ])
        assert gate.analisar_capitulo(texto, "cap_1") == []

    def test_bloco_vazio_ignorado(self):
        texto = _md([
            (4, "Técnica", "```bash\n\n```"),
        ])
        assert gate.analisar_capitulo(texto, "cap_1") == []

    def test_multiplos_blocos_mesma_secao(self):
        texto = _md([
            (4, "Técnica",
             "```bash\nnpx ccusage@latest daily\n```\n"
             "<!-- cli-check: fonte=B; confere=true -->\n\n"
             "```bash\npipx install ccusage\n```\n"
             "<!-- cli-check: fonte=B; confere=false -->"),
        ])
        blocos = gate.analisar_capitulo(texto, "cap_1")
        assert len(blocos) == 2
        assert blocos[0]["status"] == "confirmado"
        assert blocos[1]["status"] == "fabricado"

    def test_secao_registrada_no_bloco(self):
        texto = _md([
            (2, "Explica", "```bash\ngit log\n```"),
        ])
        blocos = gate.analisar_capitulo(texto, "cap_1")
        assert blocos[0]["secao"] == 2


class TestObraCategoriaTecnica:
    def test_true_quando_config_declara(self, monkeypatch):
        monkeypatch.setattr(PO, "carregar_config",
                            lambda slug: {"categoria_tecnica": True})
        assert gate.obra_e_categoria_tecnica("qualquer/slug") is True

    def test_false_quando_ausente(self, monkeypatch):
        monkeypatch.setattr(PO, "carregar_config", lambda slug: {})
        assert gate.obra_e_categoria_tecnica("qualquer/slug") is False

    def test_false_por_padrao_retrocompativel(self, monkeypatch):
        """Obra V3/V5 anterior a este gate nao tem o campo — nunca falha por isso."""
        monkeypatch.setattr(PO, "carregar_config",
                            lambda slug: {"tipo_obra": "livro"})
        assert gate.obra_e_categoria_tecnica("qualquer/slug") is False


@pytest.fixture
def obra_tecnica(tmp_path, monkeypatch):
    """Obra minima com categoria_tecnica=true e 1 capitulo com 1 bloco fabricado."""
    raiz = tmp_path / "output"
    dir_livro = raiz / "livros" / "obra-teste"
    (dir_livro / "capitulos").mkdir(parents=True)
    (dir_livro / "config_obra.json").write_text(json.dumps({
        "tipo_obra": "livro", "categoria_tecnica": True,
    }), encoding="utf-8")
    texto = _md([
        (4, "Técnica",
         "```bash\npipx install ccusage\n```\n"
         "<!-- cli-check: fonte=B; confere=false -->"),
    ])
    (dir_livro / "capitulos" / "cap_1.md").write_text(texto, encoding="utf-8")

    # obra_e_categoria_tecnica le o config via parametros_obra.carregar_config,
    # que resolve o caminho com o PROPRIO DIR_OUTPUT do modulo PO — precisa
    # apontar para o mesmo tmp_path que o DIR_OUTPUT do gate.
    monkeypatch.setattr(gate, "DIR_OUTPUT", raiz)
    monkeypatch.setattr(PO, "DIR_OUTPUT", raiz)
    return {"raiz": raiz, "dir": dir_livro, "slug": "livros/obra-teste"}


class TestMainIntegracao:
    def test_estrito_reprova_com_bloco_fabricado(self, obra_tecnica, monkeypatch):
        monkeypatch.setattr(
            "sys.argv",
            ["validar-comandos-cli.py", obra_tecnica["slug"], "--estrito"])
        assert gate.main() == 1

        relatorio = json.loads(
            (obra_tecnica["dir"] / "validacao" / "relatorio_comandos_cli.json")
            .read_text(encoding="utf-8"))
        assert relatorio["fabricados"] == 1
        assert relatorio["confirmados"] == 0

    def test_corrigido_para_confere_true_aprova(self, obra_tecnica, monkeypatch):
        texto_corrigido = _md([
            (4, "Técnica",
             "```bash\nnpx ccusage@latest daily\n```\n"
             "<!-- cli-check: fonte=B; confere=true -->"),
        ])
        (obra_tecnica["dir"] / "capitulos" / "cap_1.md").write_text(
            texto_corrigido, encoding="utf-8")

        monkeypatch.setattr(
            "sys.argv",
            ["validar-comandos-cli.py", obra_tecnica["slug"], "--estrito"])
        assert gate.main() == 0

    def test_pula_obra_sem_categoria_tecnica(self, obra_tecnica, monkeypatch):
        (obra_tecnica["dir"] / "config_obra.json").write_text(json.dumps({
            "tipo_obra": "livro", "categoria_tecnica": False,
        }), encoding="utf-8")

        monkeypatch.setattr(
            "sys.argv",
            ["validar-comandos-cli.py", obra_tecnica["slug"], "--estrito"])
        assert gate.main() == 0
        assert not (obra_tecnica["dir"] / "validacao" / "relatorio_comandos_cli.json").exists()

    def test_sem_marcacao_nao_reprova_mas_reporta_pendencia(self, obra_tecnica, monkeypatch):
        texto_sem_marca = _md([
            (4, "Técnica", "```bash\ngit status\n```"),
        ])
        (obra_tecnica["dir"] / "capitulos" / "cap_1.md").write_text(
            texto_sem_marca, encoding="utf-8")

        monkeypatch.setattr(
            "sys.argv",
            ["validar-comandos-cli.py", obra_tecnica["slug"], "--estrito"])
        assert gate.main() == 0

        relatorio = json.loads(
            (obra_tecnica["dir"] / "validacao" / "relatorio_comandos_cli.json")
            .read_text(encoding="utf-8"))
        assert relatorio["nao_verificados"] == 1
        assert relatorio["fabricados"] == 0
