"""Testes do DECK, da SEQUENCIA DE E-MAILS e da COLECAO (V5)."""

import json

import pytest

import tipos_obra as TO
from conftest import carregar_script

extrator = carregar_script("extrair-passos-praticos.py")
gerador_lm = carregar_script("gerar-lead-magnet.py")
gerador_deck = carregar_script("gerar-deck.py")
gate_deck = carregar_script("validar-deck.py")
gerador_eml = carregar_script("gerar-sequencia-emails.py")
gate_eml = carregar_script("validar-emails.py")
colecao = carregar_script("colecao.py")

CTA = "https://exemplo.com/obra"


@pytest.fixture
def ambiente(livro_falso, monkeypatch):
    raiz = livro_falso["raiz"]
    for mod in (extrator, gerador_lm, gerador_deck, gate_deck,
                gerador_eml, gate_eml, colecao):
        monkeypatch.setattr(mod, "DIR_OUTPUT", raiz)
    monkeypatch.setattr(colecao, "DIR_COLECOES", raiz / "_colecoes")
    import series_capa
    monkeypatch.setattr(series_capa, "DIR_OUTPUT", raiz)
    monkeypatch.setattr(series_capa, "CAMINHO_REGISTRO", raiz / "_series.json")
    return livro_falso


# ── DECK ──────────────────────────────────────────────────────────────────────

class TestDeck:
    def test_gera_slides_para_capa_objetivo_mapa_parte_e_capitulos(self, ambiente):
        meta = gerador_deck.gerar(ambiente["slug"], cta_url=CTA)
        # objetivo + mapa + 1 divisor de parte + 2 capitulos + CTA
        assert meta["total_slides"] == 6

    def test_deck_md_tem_um_h1_por_slide(self, ambiente):
        meta = gerador_deck.gerar(ambiente["slug"], cta_url=CTA)
        md = (ambiente["raiz"] / meta["slug"] / "deck.md").read_text(encoding="utf-8")
        assert md.count("\n# ") + md.startswith("# ") >= 5

    def test_bullets_saem_dos_pilares_do_sumario(self, ambiente):
        meta = gerador_deck.gerar(ambiente["slug"], cta_url=CTA)
        md = (ambiente["raiz"] / meta["slug"] / "deck.md").read_text(encoding="utf-8")
        assert "- Contrato" in md and "- Schema" in md

    def test_slide_final_tem_utm_de_deck(self, ambiente):
        meta = gerador_deck.gerar(ambiente["slug"], cta_url=CTA)
        md = (ambiente["raiz"] / meta["slug"] / "deck.md").read_text(encoding="utf-8")
        assert "utm_source=deck" in md

    def test_config_herda_senioridade_e_serie(self, ambiente):
        meta = gerador_deck.gerar(ambiente["slug"], cta_url=CTA)
        cfg = json.loads((ambiente["raiz"] / meta["slug"] / "config_obra.json")
                         .read_text(encoding="utf-8"))
        assert cfg["tipo_obra"] == "deck"
        assert cfg["senioridade_obra"] == "intermediario"
        assert cfg["serie"] == "Colecao Teste"

    def test_obra_sem_sumario_devolve_none(self, ambiente):
        assert gerador_deck.gerar("livros/nao-existe") is None

    def test_gate_aprova_deck_gerado(self, ambiente):
        meta = gerador_deck.gerar(ambiente["slug"], cta_url=CTA)
        rel = gate_deck.validar(meta["slug"])
        assert rel["conforme"], rel["violacoes"]

    def test_gate_reprova_sem_cta(self, ambiente):
        meta = gerador_deck.gerar(ambiente["slug"])
        rel = gate_deck.validar(meta["slug"])
        assert "R-DK-3" in {v["regra"] for v in rel["violacoes"]}

    def test_gate_reprova_bullet_longo(self, ambiente):
        meta = gerador_deck.gerar(ambiente["slug"], cta_url=CTA)
        caminho = ambiente["raiz"] / meta["slug"] / "deck.md"
        caminho.write_text(caminho.read_text(encoding="utf-8") + "\n- " + "x" * 200,
                           encoding="utf-8")
        rel = gate_deck.validar(meta["slug"])
        assert "R-DK-2" in {v["regra"] for v in rel["violacoes"]}

    def test_gate_reprova_bullets_demais(self, ambiente):
        meta = gerador_deck.gerar(ambiente["slug"], cta_url=CTA)
        caminho = ambiente["raiz"] / meta["slug"] / "deck.md"
        extra = "\n# Slide cheio\n\n" + "\n".join(f"- bullet {i}" for i in range(9))
        caminho.write_text(caminho.read_text(encoding="utf-8") + extra, encoding="utf-8")
        rel = gate_deck.validar(meta["slug"])
        assert "R-DK-2" in {v["regra"] for v in rel["violacoes"]}

    def test_gate_reprova_sem_senioridade(self, ambiente):
        meta = gerador_deck.gerar(ambiente["slug"], cta_url=CTA)
        caminho = ambiente["raiz"] / meta["slug"] / "config_obra.json"
        cfg = json.loads(caminho.read_text(encoding="utf-8"))
        cfg["senioridade_obra"] = ""
        caminho.write_text(json.dumps(cfg), encoding="utf-8")
        assert "R-DK-5" in {v["regra"] for v in gate_deck.validar(meta["slug"])["violacoes"]}

    def test_encurtar_respeita_limite(self):
        assert len(gerador_deck._encurtar("palavra " * 60, limite=50)) <= 51


# ── SEQUENCIA DE E-MAILS ──────────────────────────────────────────────────────

class TestEmails:
    def test_sequencia_tem_abertura_nutricao_e_fechamento(self, ambiente):
        meta = gerador_eml.gerar(ambiente["slug"], cta_url=CTA)
        tipos = [p["tipo"] for p in meta["plano"]]
        assert tipos[0] == "abertura"
        assert tipos[-1] == "fechamento"
        assert tipos.count("nutricao") == 2
        assert meta["total_emails"] == 4

    def test_cronograma_usa_o_intervalo(self, ambiente):
        meta = gerador_eml.gerar(ambiente["slug"], cta_url=CTA, intervalo=3)
        assert meta["duracao_dias"] == 9
        assert [p["dia"] for p in meta["plano"]] == [0, 3, 6, 9]

    def test_cada_email_tem_exatamente_um_link_com_utm(self, ambiente):
        meta = gerador_eml.gerar(ambiente["slug"], cta_url=CTA)
        dir_eml = ambiente["raiz"] / meta["slug"] / "emails"
        for caminho in sorted(dir_eml.glob("email_*.md")):
            texto = caminho.read_text(encoding="utf-8")
            assert texto.count("](") == 1, caminho.name
            assert "utm_source=email" in texto

    def test_assunto_respeita_60_caracteres(self, ambiente):
        meta = gerador_eml.gerar(ambiente["slug"], cta_url=CTA)
        dir_eml = ambiente["raiz"] / meta["slug"] / "emails"
        for caminho in dir_eml.glob("email_*.md"):
            linha = next(l for l in caminho.read_text(encoding="utf-8").splitlines()
                         if l.startswith("**Assunto:**"))
            assert len(linha.replace("**Assunto:**", "").strip()) <= 60

    def test_email_de_nutricao_usa_armadilha_do_card(self, ambiente):
        meta = gerador_eml.gerar(ambiente["slug"], cta_url=CTA)
        texto = (ambiente["raiz"] / meta["slug"] / "emails" / "email_02.md") \
            .read_text(encoding="utf-8")
        assert "Gravar o contrato fora" in texto

    def test_grava_sequencia_concatenada(self, ambiente):
        meta = gerador_eml.gerar(ambiente["slug"], cta_url=CTA)
        assert (ambiente["raiz"] / meta["slug"] / "sequencia.md").exists()

    def test_gate_aprova_sequencia_gerada(self, ambiente):
        meta = gerador_eml.gerar(ambiente["slug"], cta_url=CTA)
        rel = gate_eml.validar(meta["slug"])
        assert rel["conforme"], rel["violacoes"]

    def test_gate_reprova_sem_cta(self, ambiente):
        meta = gerador_eml.gerar(ambiente["slug"])
        rel = gate_eml.validar(meta["slug"])
        assert "R-EM-2" in {v["regra"] for v in rel["violacoes"]}

    def test_gate_reprova_assunto_longo(self, ambiente):
        meta = gerador_eml.gerar(ambiente["slug"], cta_url=CTA)
        caminho = ambiente["raiz"] / meta["slug"] / "emails" / "email_02.md"
        texto = caminho.read_text(encoding="utf-8")
        linha = next(l for l in texto.splitlines() if l.startswith("**Assunto:**"))
        caminho.write_text(texto.replace(linha, "**Assunto:** " + "x" * 70),
                           encoding="utf-8")
        assert "R-EM-1" in {v["regra"] for v in gate_eml.validar(meta["slug"])["violacoes"]}

    def test_gate_reprova_segundo_link(self, ambiente):
        meta = gerador_eml.gerar(ambiente["slug"], cta_url=CTA)
        caminho = ambiente["raiz"] / meta["slug"] / "emails" / "email_02.md"
        caminho.write_text(caminho.read_text(encoding="utf-8") +
                           "\n[outro](https://outro.com)\n", encoding="utf-8")
        assert "R-EM-2" in {v["regra"] for v in gate_eml.validar(meta["slug"])["violacoes"]}

    def test_gate_reprova_email_longo(self, ambiente):
        meta = gerador_eml.gerar(ambiente["slug"], cta_url=CTA)
        caminho = ambiente["raiz"] / meta["slug"] / "emails" / "email_02.md"
        caminho.write_text(caminho.read_text(encoding="utf-8") + "\n" + "palavra " * 300,
                           encoding="utf-8")
        assert "R-EM-4" in {v["regra"] for v in gate_eml.validar(meta["slug"])["violacoes"]}

    def test_gate_reprova_sequencia_inexistente(self, ambiente):
        rel = gate_eml.validar("emails/nao-existe")
        assert rel["conforme"] is False
        assert "R-EM-3" in {v["regra"] for v in rel["violacoes"]}

    def test_marcador_de_polimento_vira_aviso(self, ambiente):
        meta = gerador_eml.gerar(ambiente["slug"], cta_url=CTA)
        rel = gate_eml.validar(meta["slug"])
        assert any("polimento" in a for a in rel["avisos"])


# ── COLECAO ───────────────────────────────────────────────────────────────────

class TestColecao:
    def test_varredura_agrupa_pela_serie_declarada(self, ambiente):
        colecoes = colecao.varrer()
        assert "Colecao Teste" in colecoes
        assert colecoes["Colecao Teste"][0]["tipo"] == "livro"

    def test_manifesto_identifica_o_nucleo(self, ambiente):
        manifestos = colecao.sincronizar()
        m = next(x for x in manifestos if x["colecao"] == "Colecao Teste")
        assert m["nucleo"]["tipo"] == "livro"
        assert m["nucleo"]["motivo_condutor"]["persona_leitor"] == "Mestre de Obras"

    def test_manifesto_lista_derivados_ausentes(self, ambiente):
        m = next(x for x in colecao.sincronizar() if x["colecao"] == "Colecao Teste")
        assert "playbook" in m["derivados_ausentes"]
        assert "lead-magnet" in m["derivados_ausentes"]

    def test_derivado_entra_na_colecao_da_mae(self, ambiente):
        gerador_deck.gerar(ambiente["slug"], cta_url=CTA)
        m = next(x for x in colecao.sincronizar() if x["colecao"] == "Colecao Teste")
        assert m["por_tipo"] == {"deck": 1, "livro": 1}
        assert "deck" not in m["derivados_ausentes"]

    def test_membro_sem_cta_e_sinalizado(self, ambiente):
        gerador_deck.gerar(ambiente["slug"])       # sem CTA
        m = next(x for x in colecao.sincronizar() if x["colecao"] == "Colecao Teste")
        assert m["membros_sem_cta"] == ["decks/obra-teste--deck"]

    def test_estado_do_membro_reflete_o_disco(self, ambiente):
        extrator.extrair(ambiente["slug"], montar=False)
        (ambiente["raiz"] / "playbooks" / "obra-teste--pbk" / "config_obra.json").write_text(
            json.dumps(TO.defaults_config("playbook", slug_mae_simples="obra-teste",
                                          extra={"serie": "Colecao Teste"}),
                       ensure_ascii=False), encoding="utf-8")
        m = next(x for x in colecao.sincronizar() if x["colecao"] == "Colecao Teste")
        estados = {x["tipo"]: x["estado"] for x in m["membros"]}
        assert estados["livro"] == "redigido"
        assert estados["playbook"] == "extraido"

    def test_grava_manifesto_em_arquivo_slugificado(self, ambiente):
        colecao.sincronizar()
        assert (ambiente["raiz"] / "_colecoes" / "colecao-teste.json").exists()

    def test_carregar_devolve_none_para_colecao_inexistente(self, ambiente):
        assert colecao.carregar("nao-existe") is None

    def test_sincronizar_com_slug_filtra_uma_colecao(self, ambiente):
        manifestos = colecao.sincronizar(slug=ambiente["slug"])
        assert len(manifestos) == 1
        assert manifestos[0]["colecao"] == "Colecao Teste"

    def test_sincronizacao_e_idempotente(self, ambiente):
        a = colecao.sincronizar()
        b = colecao.sincronizar()
        assert [x["por_tipo"] for x in a] == [x["por_tipo"] for x in b]
