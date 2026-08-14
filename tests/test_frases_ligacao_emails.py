"""Testes para o rodízio determinístico de frases de ligação (gerar-sequencia-emails.py)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from conftest import carregar_script

geml = carregar_script("gerar-sequencia-emails.py")


class TestFraseLigacao:
    def test_rotacao_deterministica_por_indice(self):
        banco = ["a{x}", "b{x}", "c{x}"]
        assert geml._frase_ligacao(banco, 1, x="!") == "a!"
        assert geml._frase_ligacao(banco, 2, x="!") == "b!"
        assert geml._frase_ligacao(banco, 3, x="!") == "c!"
        assert geml._frase_ligacao(banco, 4, x="!") == "a!"  # volta ao início

    def test_mesmo_indice_sempre_devolve_o_mesmo(self):
        banco = ["x{t}", "y{t}"]
        r1 = geml._frase_ligacao(banco, 5, t="tema")
        r2 = geml._frase_ligacao(banco, 5, t="tema")
        assert r1 == r2

    def test_email_abertura_sem_marcador_polimento(self):
        texto = geml._email_abertura({"titulo_obra": "Meu Livro"}, "https://x.com", 1)
        assert "POLIMENTO-LLM" not in texto
        assert "Meu Livro" in texto

    def test_email_card_sem_marcador_polimento(self):
        card = {"titulo": "Passo 1", "armadilhas": ["ignorar testes"], "entregas": ["script.py"]}
        texto = geml._email_card(card, {"titulo_obra": "Meu Livro"}, "https://x.com", 2, 5)
        assert "POLIMENTO-LLM" not in texto
        assert "ignorar testes" in texto

    def test_email_fechamento_sem_marcador_polimento(self):
        texto = geml._email_fechamento({"titulo_obra": "Meu Livro"}, "https://x.com", 5)
        assert "POLIMENTO-LLM" not in texto
        assert "Meu Livro" in texto
