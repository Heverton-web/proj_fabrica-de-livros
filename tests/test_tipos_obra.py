"""Testes do registro declarativo de tipos (scripts/tipos_obra.py) — V5.

O registro e o alicerce da V5: se ele estiver incoerente, os 6 pontos de dispatch
herdam a incoerencia. Estes testes cobram a coerencia interna do registro, nao
apenas a presenca dos campos.
"""

import pytest

import tipos_obra as TO

CAMPOS_OBRIGATORIOS = (
    "rotulo", "raiz_output", "sufixo_slug", "derivado_de", "natureza",
    "custo_llm", "extensoes_saida", "min_refs_padrao", "numerar_secoes",
    "exige_cta", "membro_colecao", "perguntavel_na_fase0",
)

NATUREZAS = {"geracao", "expansao", "compressao", "extracao"}
CUSTOS = {"alto", "medio", "baixo", "zero"}


class TestIntegridadeDoRegistro:
    def test_todos_os_tipos_tem_todos_os_campos(self):
        for tipo, d in TO.TIPOS.items():
            faltando = [c for c in CAMPOS_OBRIGATORIOS if c not in d]
            assert not faltando, f"{tipo} sem campos: {faltando}"

    def test_raiz_output_e_unica_por_tipo(self):
        raizes = [d["raiz_output"] for d in TO.TIPOS.values()]
        assert len(raizes) == len(set(raizes)), "raiz_output duplicada entre tipos"

    def test_sufixo_slug_e_unico_entre_derivados(self):
        sufixos = [d["sufixo_slug"] for d in TO.TIPOS.values() if d["sufixo_slug"]]
        assert len(sufixos) == len(set(sufixos))

    def test_natureza_e_custo_em_dominio_valido(self):
        for tipo, d in TO.TIPOS.items():
            assert d["natureza"] in NATUREZAS, f"{tipo}: {d['natureza']}"
            assert d["custo_llm"] in CUSTOS, f"{tipo}: {d['custo_llm']}"

    def test_derivado_de_referencia_apenas_tipos_existentes(self):
        for tipo, d in TO.TIPOS.items():
            for mae in d["derivado_de"]:
                assert mae in TO.TIPOS, f"{tipo} deriva de tipo inexistente {mae!r}"

    def test_tipo_raiz_nao_tem_sufixo_e_derivado_tem(self):
        for tipo, d in TO.TIPOS.items():
            if d["derivado_de"]:
                assert d["sufixo_slug"], f"{tipo} e derivado mas nao tem sufixo_slug"
            else:
                assert d["sufixo_slug"] is None, f"{tipo} e raiz mas tem sufixo_slug"

    def test_nao_ha_ciclo_de_derivacao(self):
        def ancestrais(tipo, vistos=None):
            vistos = vistos or set()
            for mae in TO.TIPOS[tipo]["derivado_de"]:
                assert mae not in vistos, f"ciclo de derivacao envolvendo {tipo}"
                ancestrais(mae, vistos | {tipo})
        for tipo in TO.TIPOS:
            ancestrais(tipo)

    def test_apenas_tipos_raiz_sao_perguntaveis_na_fase0(self):
        for tipo, d in TO.TIPOS.items():
            if d["perguntavel_na_fase0"]:
                assert not d["derivado_de"], f"{tipo} e derivado mas perguntavel na Fase 0"

    def test_tipos_de_extracao_declaram_validador(self):
        for tipo, d in TO.TIPOS.items():
            if d["natureza"] == "extracao":
                assert d["validador"], f"{tipo} e extracao mas nao declara validador"

    def test_validadores_declarados_existem_no_disco(self):
        for tipo in TO.tipos_validos():
            caminho = TO.validador_de(tipo)
            if caminho is not None:
                assert caminho.exists(), f"{tipo}: validador ausente em {caminho}"

    def test_templates_declarados_existem_no_disco(self):
        for tipo in TO.tipos_validos():
            caminho = TO.template_de(tipo)
            if caminho is not None:
                assert caminho.exists(), f"{tipo}: template ausente em {caminho}"


class TestApiDoRegistro:
    def test_descritor_levanta_para_tipo_desconhecido(self):
        with pytest.raises(KeyError):
            TO.descritor("nao-existe")

    def test_campo_e_tolerante_para_tipo_desconhecido(self):
        assert TO.campo("nao-existe", "rotulo", "padrao") == "padrao"

    def test_tipos_raiz_e_derivados_particionam_o_registro(self):
        assert set(TO.tipos_raiz()) | set(TO.tipos_derivados()) == set(TO.tipos_validos())
        assert not set(TO.tipos_raiz()) & set(TO.tipos_derivados())

    def test_derivaveis_de_livro_inclui_playbook_e_ebook(self):
        derivaveis = TO.derivaveis_de("livro")
        assert "playbook" in derivaveis
        assert "ebook" in derivaveis
        assert "deck" in derivaveis

    def test_validar_derivacao_aceita_livro_para_playbook(self):
        assert TO.validar_derivacao("playbook", "livro") == []

    def test_validar_derivacao_rejeita_tcc_para_playbook(self):
        erros = TO.validar_derivacao("playbook", "tcc")
        assert len(erros) == 1
        assert "livro" in erros[0]

    def test_validar_derivacao_rejeita_obra_raiz(self):
        erros = TO.validar_derivacao("livro", "tcc")
        assert "raiz" in erros[0]

    def test_slug_completo_usa_raiz_do_registro(self):
        assert TO.slug_completo("playbook", "x--pbk") == "playbooks/x--pbk"
        assert TO.slug_completo("lead-magnet", "x--lm") == "lead-magnets/x--lm"

    def test_slug_derivado_sem_indice(self):
        assert TO.slug_derivado("playbook", "obra") == "obra--pbk"

    def test_slug_derivado_com_indice_e_titulo(self):
        assert TO.slug_derivado("lead-magnet", "obra", indice=3,
                                sufixo_titulo="checklist") == "obra--lm-03-checklist"

    def test_tipo_por_prefixo_resolve_ida_e_volta(self):
        for tipo in TO.tipos_validos():
            slug = TO.slug_completo(tipo, "x")
            assert TO.tipo_por_prefixo(slug) == tipo

    def test_tipo_por_prefixo_devolve_none_sem_prefixo(self):
        assert TO.tipo_por_prefixo("solto") is None

    def test_dimensoes_social_so_no_lead_magnet(self):
        assert TO.dimensoes_capa("lead-magnet", variante="social") == (1080, 1350)
        assert TO.dimensoes_capa("playbook", variante="social") is None

    def test_exige_referencias_reflete_min_refs(self):
        assert TO.exige_referencias("livro") is True
        assert TO.exige_referencias("playbook") is False

    def test_usa_citacao_autor_data(self):
        assert TO.usa_citacao_autor_data("tcc") is True
        assert TO.usa_citacao_autor_data("artigo") is True
        assert TO.usa_citacao_autor_data("livro") is False
        assert TO.usa_citacao_autor_data("playbook") is False


class TestDefaultsConfig:
    def test_defaults_config_traz_tipo_e_derivados_v5(self):
        cfg = TO.defaults_config("playbook", slug_mae_simples="obra")
        assert cfg["tipo_obra"] == "playbook"
        assert cfg["livro_mae"] == "obra"      # chave historica (series_capa.py)
        assert cfg["obra_mae"] == "obra"
        assert cfg["min_referencias_por_capitulo"] == 0

    def test_defaults_config_sem_mae_nao_cria_chaves_de_mae(self):
        cfg = TO.defaults_config("livro")
        assert "livro_mae" not in cfg
        assert "obra_mae" not in cfg

    def test_extra_sobrepoe_defaults(self):
        cfg = TO.defaults_config("artigo", extra={"min_referencias_por_capitulo": 12})
        assert cfg["min_referencias_por_capitulo"] == 12


class TestFormatosLeadMagnet:
    def test_todos_os_formatos_tem_campos_obrigatorios(self):
        for chave, f in TO.FORMATOS_LM.items():
            for campo in ("rotulo", "campo_card", "titulo_padrao", "promessa",
                          "min_itens", "max_paginas"):
                assert campo in f, f"{chave} sem {campo}"

    def test_formato_padrao_existe(self):
        assert TO.FORMATO_LM_PADRAO in TO.FORMATOS_LM

    def test_titulo_e_promessa_aceitam_tema_e_n(self):
        for chave, f in TO.FORMATOS_LM.items():
            assert f["titulo_padrao"].format(tema="X", n=7)
            assert f["promessa"].format(tema="X", n=7)

    def test_max_paginas_e_positivo_e_plausivel(self):
        for chave, f in TO.FORMATOS_LM.items():
            assert 1 <= f["max_paginas"] <= 12, f"{chave}: {f['max_paginas']}"


class TestMatrizDerivacao:
    def test_matriz_cobre_todos_os_tipos(self):
        tipos_na_matriz = {filho for _mae, filho, _n, _c in TO.matriz_derivacao()}
        assert tipos_na_matriz == set(TO.tipos_validos())

    def test_extracao_sempre_tem_custo_baixo_ou_zero(self):
        for _mae, filho, natureza, custo in TO.matriz_derivacao():
            if natureza == "extracao":
                assert custo in ("zero", "baixo"), f"{filho}: extracao com custo {custo}"

    def test_geracao_sempre_tem_custo_alto(self):
        for _mae, filho, natureza, custo in TO.matriz_derivacao():
            if natureza == "geracao":
                assert custo == "alto", f"{filho}: geracao com custo {custo}"
