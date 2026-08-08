"""Testes do parser canonico EITA (scripts/secoes_eita.py) — V5.

Este modulo e a fonte unica de verdade da extracao. Um bug aqui contamina
playbook, lead magnet e deck ao mesmo tempo.
"""

import pytest

from conftest import CAPITULO_EITA, CAPITULO_SEM_TECNICA
from secoes_eita import (blocos_de_codigo, caminhos_de_arquivo, comandos_executaveis,
                         dividir_secoes, itens_binarios, itens_de_lista, normalizar,
                         primeiro_paragrafo, secao_por_nome, sem_acento, sem_codigo,
                         subsecao, subtitulos, titulo_do_capitulo)


@pytest.fixture
def secoes():
    return dividir_secoes(CAPITULO_EITA)


class TestNormalizacao:
    def test_sem_acento_preserva_letras(self):
        assert sem_acento("Técnica") == "Tecnica"
        assert sem_acento("Conclusão") == "Conclusao"

    def test_normalizar_baixa_caixa_e_apara(self):
        assert normalizar("  Técnica  ") == "tecnica"

    def test_normalizar_aceita_none(self):
        assert normalizar(None) == ""


class TestDividirSecoes:
    def test_encontra_as_sete_secoes(self, secoes):
        assert sorted(secoes) == [1, 2, 3, 4, 5, 6, 7]

    def test_titulo_da_secao_preserva_acento(self, secoes):
        assert secoes[4]["titulo"] == "Técnica"

    def test_corpo_nao_vaza_para_a_secao_seguinte(self, secoes):
        assert "Exercício Prático" not in secoes[4]["corpo"]
        assert "Exercício Prático" in secoes[5]["corpo"]

    def test_capitulo_incompleto_nao_inventa_secoes(self):
        s = dividir_secoes(CAPITULO_SEM_TECNICA)
        assert 4 not in s
        assert 5 in s

    def test_texto_vazio_devolve_dict_vazio(self):
        assert dividir_secoes("") == {}


class TestSecaoPorNome:
    def test_resolve_por_apelido_sem_acento(self, secoes):
        assert "contrato.py" in secao_por_nome(secoes, "tecnica")

    def test_devolve_vazio_para_secao_ausente(self):
        s = dividir_secoes(CAPITULO_SEM_TECNICA)
        assert secao_por_nome(s, "tecnica") == ""

    def test_devolve_vazio_para_apelido_desconhecido(self, secoes):
        assert secao_por_nome(secoes, "inexistente") == ""

    def test_rejeita_secao_com_numero_certo_e_titulo_errado(self):
        texto = "## 4. Bibliografia\n\nconteudo qualquer\n"
        assert secao_por_nome(dividir_secoes(texto), "tecnica") == ""


class TestItensDeLista:
    def test_extrai_itens_do_exercicio(self, secoes):
        aplica = secao_por_nome(secoes, "aplica")
        itens = itens_de_lista(subsecao(aplica, "exercicio"))
        assert len(itens) == 4
        assert itens[0].startswith("Criar o arquivo")

    def test_ignora_itens_curtos(self):
        assert itens_de_lista("- ok\n- item com texto suficiente") == \
            ["item com texto suficiente"]

    def test_remove_duplicatas_preservando_ordem(self):
        texto = "- primeiro item aqui\n- segundo item aqui\n- primeiro item aqui"
        assert itens_de_lista(texto) == ["primeiro item aqui", "segundo item aqui"]

    def test_respeita_o_limite(self):
        texto = "\n".join(f"- item numero {i} do teste" for i in range(10))
        assert len(itens_de_lista(texto, limite=3)) == 3

    def test_aceita_checkbox_e_numeracao(self):
        texto = "- [ ] tarefa com checkbox\n1. tarefa numerada aqui"
        assert itens_de_lista(texto) == ["tarefa com checkbox", "tarefa numerada aqui"]

    def test_ignora_listas_dentro_de_codigo(self):
        texto = "```bash\n- nao e item de lista\n```\n- este e item de lista"
        assert itens_de_lista(texto) == ["este e item de lista"]


class TestItensBinarios:
    """O EITA nao obriga o Exercicio Pratico a ser lista — boa parte dos capitulos
    reais escreve uma frase imperativa encadeada. Sem esta quebra, o card sai com
    'Feito quando' vazio e o gate reprova o capitulo por R-PBK-4 injustamente."""

    def test_prefere_lista_quando_existe(self, secoes):
        aplica = secao_por_nome(secoes, "aplica")
        itens = itens_binarios(subsecao(aplica, "exercicio"))
        assert itens[0].startswith("Criar o arquivo")
        assert len(itens) == 4

    def test_quebra_prosa_imperativa_encadeada(self):
        prosa = ("Execute o prompt completo da TorreDeControle, verifique a entrega "
                 "com py_compile, faça o commit e responda no seu diário de projeto.")
        itens = itens_binarios(prosa)
        assert itens == [
            "Execute o prompt completo da TorreDeControle",
            "Verifique a entrega com py_compile",
            "Faça o commit",
            "Responda no seu diário de projeto",
        ]

    def test_nao_quebra_virgula_que_nao_abre_ordem(self):
        prosa = "Execute o teste, que roda em dois segundos, antes de seguir adiante."
        assert itens_binarios(prosa) == ["Execute o teste"]

    def test_separa_frases_distintas(self):
        prosa = "Crie o arquivo de contrato. Depois disso rode o validador estrito."
        itens = itens_binarios(prosa)
        assert len(itens) == 2
        assert itens[1].startswith("Depois disso")

    def test_capitaliza_a_primeira_letra(self):
        assert itens_binarios("rode o validador, verifique o resultado")[0] == \
            "Rode o validador"

    def test_ignora_conteudo_de_bloco_de_codigo(self):
        texto = "```bash\nexecute isto no shell\n```\nCrie o arquivo de contrato."
        assert itens_binarios(texto) == ["Crie o arquivo de contrato"]

    def test_respeita_o_limite(self):
        prosa = ". ".join(f"Crie o arquivo numero {i}" for i in range(10))
        assert len(itens_binarios(prosa, limite=3)) == 3

    def test_deduplica(self):
        prosa = "Crie o arquivo de contrato. Crie o arquivo de contrato."
        assert len(itens_binarios(prosa)) == 1

    def test_texto_vazio_devolve_lista_vazia(self):
        assert itens_binarios("") == []
        assert itens_binarios(None) == []


class TestBlocosDeCodigo:
    def test_extrai_linguagem_e_corpo(self, secoes):
        blocos = blocos_de_codigo(secao_por_nome(secoes, "tecnica"))
        assert [b["linguagem"] for b in blocos] == ["bash", "python"]

    def test_ignora_mermaid_por_padrao(self, secoes):
        blocos = blocos_de_codigo(secao_por_nome(secoes, "ilustra"))
        assert blocos == []

    def test_inclui_mermaid_quando_pedido(self, secoes):
        blocos = blocos_de_codigo(secao_por_nome(secoes, "ilustra"), ignorar_mermaid=False)
        assert len(blocos) == 1
        assert blocos[0]["linguagem"] == "mermaid"


class TestComandosExecutaveis:
    def test_extrai_apenas_comandos(self, secoes):
        comandos = comandos_executaveis(secao_por_nome(secoes, "tecnica"))
        assert comandos == ["python scripts/contrato.py --iniciar",
                            "python scripts/validar-contrato.py --estrito"]

    def test_ignora_atribuicao_python(self, secoes):
        comandos = comandos_executaveis(secao_por_nome(secoes, "tecnica"))
        assert not any("registro =" in c for c in comandos)

    def test_remove_prompt_de_shell(self):
        assert comandos_executaveis("```bash\n$ pytest -q\n```") == ["pytest -q"]

    def test_deduplica(self):
        texto = "```bash\npytest -q\npytest -q\n```"
        assert comandos_executaveis(texto) == ["pytest -q"]

    def test_respeita_limite(self):
        texto = "```bash\n" + "\n".join(f"python a{i}.py" for i in range(10)) + "\n```"
        assert len(comandos_executaveis(texto, limite=4)) == 4

    def test_texto_sem_bloco_nao_gera_comando(self):
        assert comandos_executaveis("python isso nao esta em bloco") == []


class TestCaminhosDeArquivo:
    def test_extrai_paths_em_crase(self, secoes):
        paths = caminhos_de_arquivo(secao_por_nome(secoes, "tecnica"))
        assert "scripts/contrato.py" in paths
        assert "config/schema.json" in paths
        assert "output/indice.json" in paths

    def test_ignora_url(self):
        assert caminhos_de_arquivo("veja `https://exemplo.com/a.py`") == []

    def test_ignora_texto_com_espaco(self):
        assert caminhos_de_arquivo("`arquivo com espaco.py`") == []

    def test_deduplica_ignorando_caixa(self):
        assert caminhos_de_arquivo("`a/b.py` e `A/B.PY`") == ["a/b.py"]

    def test_respeita_limite(self):
        texto = " ".join(f"`dir/a{i}.py`" for i in range(10))
        assert len(caminhos_de_arquivo(texto, limite=3)) == 3


class TestSubtitulosESubsecao:
    def test_lista_subtitulos_com_nivel(self, secoes):
        marcas = subtitulos(secao_por_nome(secoes, "tecnica"))
        assert marcas == [(3, "Criar o arquivo de contrato"), (3, "Registrar no índice")]

    def test_subsecao_encontra_por_apelido_sem_acento(self, secoes):
        corpo = subsecao(secao_por_nome(secoes, "aplica"), "exercicio")
        assert "Criar o arquivo" in corpo
        assert "Armadilhas" not in corpo

    def test_subsecao_para_no_proximo_subtitulo(self, secoes):
        corpo = subsecao(secao_por_nome(secoes, "aplica"), "armadilha")
        assert "quebrando o import" in corpo
        assert "Criar o arquivo" not in corpo

    def test_subsecao_inexistente_devolve_vazio(self, secoes):
        assert subsecao(secao_por_nome(secoes, "aplica"), "inexistente") == ""


class TestProsaEUtilitarios:
    def test_primeiro_paragrafo_ignora_titulo_e_codigo(self, secoes):
        p = primeiro_paragrafo(secao_por_nome(secoes, "introducao"))
        assert p.startswith("Este capítulo abre o canteiro")
        assert "[1]" not in p

    def test_primeiro_paragrafo_respeita_max_chars(self, secoes):
        p = primeiro_paragrafo(secao_por_nome(secoes, "introducao"), max_chars=40)
        assert len(p) <= 45

    def test_primeiro_paragrafo_de_texto_vazio(self):
        assert primeiro_paragrafo("") == ""

    def test_sem_codigo_remove_blocos(self, secoes):
        limpo = sem_codigo(secao_por_nome(secoes, "tecnica"))
        assert "python scripts/contrato.py" not in limpo
        assert "Grave o contrato" in limpo

    def test_titulo_do_capitulo_remove_numeracao(self):
        assert titulo_do_capitulo("# Capítulo 3 — Fundação") == "Fundação"
        assert titulo_do_capitulo(CAPITULO_EITA) == "Fundação do Projeto"

    def test_titulo_do_capitulo_usa_padrao_quando_ausente(self):
        assert titulo_do_capitulo("sem titulo", padrao="X") == "X"
