"""Testes da matriz de TRANSMUTACAO (reescrita entre tipos) — V5.2.

O campo `reescrever_de` separa a cascata raiz->derivado (derivado_de) da
reescrita de material existente para outro tipo. Estes testes cobram a
coerencia da matriz e o comportamento de `validar_reescrita`/`reescreviveis_de`/
`matriz_reescrita`.
"""

import tipos_obra as TO


class TestReescreverDe:
    def test_todo_tipo_declara_reescrever_de(self):
        # so os 4 destinos de reescrita declaram o campo; extracao usa
        # .get("reescrever_de", ()) vazio (nenhum destino aceita reescrita).
        for tipo in ("livro", "tcc", "ebook", "artigo"):
            assert "reescrever_de" in TO.TIPOS[tipo], \
                f"{tipo} sem campo reescrever_de"

    def test_reescrever_de_referencia_apenas_tipos_existentes(self):
        for tipo, d in TO.TIPOS.items():
            for origem in d.get("reescrever_de", ()):
                assert origem in TO.TIPOS, \
                    f"{tipo} reescreve-se de tipo inexistente {origem!r}"

    def test_raizes_de_reescrita_tem_pelo_menos_um_destino(self):
        # livros/tcc/ebook/artigo aceitam reescrita; extracao (playbook, LM,
        # deck, emails) nao tem reescrita como destino.
        for tipo in ("livro", "tcc", "ebook", "artigo"):
            assert TO.TIPOS[tipo]["reescrever_de"], f"{tipo} sem origens de reescrita"
        for tipo in ("playbook", "lead-magnet", "deck", "emails"):
            assert not TO.TIPOS[tipo].get("reescrever_de", ()), \
                f"{tipo} e extracao e nao deveria aceitar reescrita"


class TestValidarReescrita:
    def test_pares_validos_da_matriz(self):
        pares = [
            ("ebook", "livro"), ("livro", "playbook"), ("artigo", "livro"),
            ("tcc", "livro"), ("livro", "tcc"), ("ebook", "tcc"),
            ("livro", "artigo"), ("tcc", "artigo"), ("ebook", "artigo"),
            ("livro", "ebook"), ("tcc", "ebook"), ("playbook", "ebook"),
        ]
        # convencao: (destino, origem) — par valido quando origem -> destino
        pares = [
            ("ebook", "livro"), ("ebook", "tcc"), ("ebook", "playbook"),
            ("tcc", "livro"), ("tcc", "ebook"),
            ("artigo", "livro"), ("artigo", "tcc"), ("artigo", "ebook"),
            ("livro", "ebook"), ("livro", "playbook"),
            ("livro", "artigo"), ("livro", "tcc"),
        ]
        for destino, origem in pares:
            assert TO.validar_reescrita(destino, origem) == [], \
                f"{origem} -> {destino} deveria ser permitido"

    def test_par_invalido_para_destino(self):
        erros = TO.validar_reescrita("tcc", "artigo")
        assert erros, "tcc a partir de artigo deveria ser bloqueado"
        assert "tcc" in erros[0]

    def test_mesmo_tipo_e_invalido(self):
        for tipo in ("livro", "tcc", "ebook", "artigo"):
            assert TO.validar_reescrita(tipo, tipo), \
                f"{tipo} -> {tipo} deveria ser bloqueado"

    def test_destino_de_extracao_nao_aceita_reescrita(self):
        assert TO.validar_reescrita("playbook", "livro"), \
            "playbook nao deveria ser destino de reescrita"

    def test_tipo_desconhecido_levanta(self):
        import pytest
        with pytest.raises(Exception):
            TO.validar_reescrita("tipo-fantasma", "livro")


class TestReescreviveisDe:
    def test_destinos_aceitos_por_origem(self):
        assert set(TO.reescreviveis_de("livro")) >= {"tcc", "ebook", "artigo"}
        assert set(TO.reescreviveis_de("ebook")) >= {"livro", "tcc", "artigo"}
        assert set(TO.reescreviveis_de("playbook")) >= {"livro", "ebook"}
        assert "playbook" not in TO.reescreviveis_de("livro")

    def test_simetrica_a_validar_reescrita(self):
        for origem in TO.TIPOS:
            for destino in TO.TIPOS:
                esperado = TO.validar_reescrita(destino, origem) == []
                assert (destino in TO.reescreviveis_de(origem)) == esperado, \
                    f"assimetria em {origem} -> {destino}"


class TestMatrizReescrita:
    def test_matriz_lista_pares_ordenados(self):
        matriz = TO.matriz_reescrita()
        assert matriz, "matriz vazia"
        for item in matriz:
            origem, destino, natureza, custo = item
            assert destino in TO.reescreviveis_de(origem), \
                f"par {origem} -> {destino} fora da matriz"

    def test_natureza_e_custo_vem_do_destino(self):
        for origem, destino, natureza, custo in TO.matriz_reescrita():
            d = TO.TIPOS[destino]
            assert natureza == d["natureza"], f"{destino}: natureza errada"
            assert custo == d["custo_llm"], f"{destino}: custo errado"

    def test_expansao_para_livro_tem_custo_alto(self):
        for origem, destino, natureza, custo in TO.matriz_reescrita():
            if destino == "livro":
                assert custo == "alto", f"{origem} -> livro com custo {custo}"
