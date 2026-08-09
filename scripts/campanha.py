#!/usr/bin/env python3
"""
CAMPANHA (V5.3) — registro declarativo da camada de divulgacao da colecao.

Uma CAMPANHA e a camada de materiais de divulgacao derivada de uma COLECAO
(nucleo canonico + identidade visual: cor_accent, badge de nivel, vocabulario
condutor e CTA). Vive em output/<slug-colecao>/campanhas/, com uma subpasta por
material-alvo (livro, tcc, artigo, ebook, playbook, lead-magnet, deck).

Artefato novo de campanha = 1 linha nos registros REDES_SOCIAIS/CANAIS_COMUNICACAO.
Nao e tipo de obra: nao entra no molde do tipos_obra.py (sem capa/PDF/dispatch).

Uso (orquestrado pelos comandos /campanha e /campanha-completa):
    python scripts/criar-campanha.py --material <slug>
    python scripts/criar-campanha.py --completo [<colecao>]
    python scripts/validar-campanha.py --material <slug> --estrito
"""

import json
import re
from pathlib import Path

import tipos_obra as TO
from series_capa import resolver_cor, resolver_serie_key

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"
DIR_TEMPLATES = DIR_PROJETO / "templates" / "campanha"

# ── Registro: REDES SOCIAIS ─────────────────────────────────────────────────
# artes: formato -> (largura, altura) em px
# textos: pasta de texto -> quantidade de arquivos (rascunho)
# templates: copia o HTML da arte para o material
# cronograma_dias: janela de divulgacao em dias (datas reais a partir de amanha)
REDES_SOCIAIS = {
    "instagram": {
        "rotulo": "Instagram",
        "artes": {"feed-story": (1080, 1920), "post": (1080, 1350)},
        "textos": {"feed-story": 2, "post": 3, "resposta-direct": 1},
        "templates": True,
        "cronograma_dias": 14,
    },
    "linkedin": {
        "rotulo": "LinkedIn",
        "artes": {"post": (1200, 628)},
        "textos": {"post": 2, "resposta-direct": 1},
        "templates": True,
        "cronograma_dias": 14,
    },
}

# ── Registro: CANAIS DE COMUNICACAO ─────────────────────────────────────────
# sequencia -> {artes: n, templates: bool, textos: n, cronograma_dias: n}
CANAIS_COMUNICACAO = {
    "emails": {
        "rotulo": "E-mails",
        "sequencias": {
            "sequencia-nutricao": {"templates": True, "textos": 4, "cronograma_dias": 30},
            "sequencia-mkt": {"templates": True, "textos": 3, "cronograma_dias": 30},
        },
    },
    "whatsapp": {
        "rotulo": "WhatsApp",
        "sequencias": {
            "sequencia-nutricao": {"artes": 1, "textos": 4, "cronograma_dias": 14},
            "sequencia-divulgacao": {"artes": 1, "textos": 6, "cronograma_dias": 14},
        },
    },
}

# Template HTML de arte por formato (dimensoes fixas por arquivo)
TEMPLATES_ARTE = {
    "feed-story": "arte-feed-story-ig.html",
    "post_ig": "arte-post-ig.html",
    "post_linkedin": "arte-post-linkedin.html",
    "whatsapp": "arte-whatsapp.html",
}

def roteiro_rede(rede, dias=None):
    """Formato de conteudo por dia (post/feed-story/direct) do cronograma da rede.

    Usa os MESMOS nomes de formato do registro `artes` (ex.: instagram tem
    'feed-story', nao 'story') para que a contagem de n_artes_redes bata."""
    dias = dias or REDES_SOCIAIS[rede].get("cronograma_dias", 14)
    return ["post" if i % 2 == 0 else
            ("feed-story" if rede == "instagram" else "direct")
            for i in range(dias)]


def n_artes_redes(rede):
    """Artes necessarias por formato para SUPRE o cronograma da rede.

    Ex.: instagram com 14 dias alterna post/story -> 7 posts e 7 stories;
    linkedin alterna post/direct -> 7 posts (direct e texto, sem arte).
    """
    roteiro = roteiro_rede(rede)
    return {formato: roteiro.count(formato)
            for formato in REDES_SOCIAIS[rede].get("artes", {})}


def n_artes_whatsapp(sequencia):
    """Artes da sequencia de WhatsApp = numero de mensagens (envios) dela."""
    conf = CANAIS_COMUNICACAO["whatsapp"]["sequencias"].get(sequencia, {})
    return conf.get("textos", 0) or conf.get("artes", 0)


# ── Cronograma rico: o que / por que / como / quando ───────────────────────
# Objetivos (por que publicar) rotativos por fase do funil na janela:
# 0 = gancho/curiosidade, 1 = aprofundamento/confianca, 2 = urgencia/CTA.
OBJETIVOS_FASE = {
    0: [
        "Ativar a curiosidade: apresente o gancho central do material em uma frase que provoque o clique e gere reconhecimento imediato.",
        "Marcar presenca: mostre ao leitor ideal que o tema do material e o problema que ele enfrenta hoje.",
    ],
    1: [
        "Aprofundar a solucao: conecte um caminho pratico do material com a dor do leitor e sustente com um dado ou resultado.",
        "Educar e gerar confianca: entregue um insight aplicavel do material, provando que o conteudo e denso e pratico.",
    ],
    2: [
        "Urgencia e conversao: feche com o CTA direto e o proximo passo obvio, reaproveitando o que ja foi apresentado na janela.",
        "Fechamento: lembre o leitor do que ele ainda nao tem (o material completo) e traga o CTA com destaque.",
    ],
}

# Instrucao de publicacao (como) por formato. {arte}/{texto}/{cta} interpolados
# no gerador (criar-campanha.py).
COMO_FORMATO = {
    "post": ("Publique a arte {arte} no feed com a legenda {texto} (pasta textos/). "
              "Coloque o link na bio, use 5-8 hashtags do nicho e finalize com o "
              "CTA: {cta}."),
    "feed-story": ("Poste o story {arte} com sticker de enquete/duvida para puxar "
                    "interacao; responda quem responder e leve a conversa para o "
                    "direct. CTA: {cta}."),
    "direct": ("Responda a DM com o texto {texto}, personalize a primeira linha "
                "com o nome da pessoa e pergunte qual duvida ela quer resolver. "
                "CTA: {cta}."),
    "email": ("Envie o e-mail {texto} com o assunto ja definido no arquivo; "
               "revise pre-header e o link do CTA ({cta}) antes de disparar."),
    "msg": ("Envie a mensagem {texto} em horario comercial; se houver arte {arte}, "
             "envie logo depois do texto inicial. CTA: {cta}."),
    "pausa": ("Use o dia para responder interacoes pendentes, repostar stories "
               "recebidos e deixar o proximo envio pronto (texto revisado, link "
               "testado, horario agendado)."),
}

# Horario sugerido (quando) por formato.
HORARIO_FORMATO = {
    "post": "9h (feed, maior alcance em tecnologia)",
    "feed-story": "12h ou 18h30 (pico de stories)",
    "direct": "imediato - responda em ate 2h",
    "email": "9h (segunda a quinta)",
    "msg": "10h-11h (horario comercial)",
}

PAUSA_PORQUE = ("Frequencia calculada para nao cansar a audiencia: o proximo envio "
                 "tera mais impacto se este dia ficar em silencio.")


def fase_da_janela(dia, dias):
    """Fase do funil pela fracao do dia na janela: 0=gancho, 1=aprofundamento, 2=urgencia."""
    if dias <= 0:
        return 0
    fracao = (dia - 1) / dias
    if fracao < 0.35:
        return 0
    if fracao < 0.75:
        return 1
    return 2


def objetivo_do_dia(dia, dias):
    """Objetivo (por que publicar) do dia: rotativo dentro da fase do funil."""
    fase = fase_da_janela(dia, dias)
    variacoes = OBJETIVOS_FASE[fase]
    return variacoes[(dia - 1) % len(variacoes)]


def como_utilizar(formato, arte=None, texto=None, cta=""):
    """Instrucao 'como publicar' interpolada para um formato."""
    molde = COMO_FORMATO.get(formato, COMO_FORMATO["post"])
    return molde.format(arte=arte or "(sem arte)",
                        texto=texto or "(sem texto)",
                        cta=cta or "Saiba mais")


def horario_utilizar(formato):
    return HORARIO_FORMATO.get(formato, "9h")


# ── Tags das artes de divulgacao ────────────────────────────────────────────
# As artes (post/story/whatsapp) usam termos TECNICOS do dominio do material
# (derivados dos pilares/capitulos/tema), NUNCA o vocabulario condutor
# metaforico (ex.: arnes, mosquetao — bom no livro, estranho na arte).
TAGS_TECNICAS = {
    # IA agêntica / engenharia de software
    "agente", "agentes", "agêntica", "modelo", "llm", "prompt", "harness",
    "guardrail", "guardrails", "sandbox", "sandboxes", "contexto", "react",
    "loop", "loops", "ferramenta", "ferramentas", "memória", "estado",
    "evals", "observabilidade", "trace", "traces", "log", "logs", "métrica",
    "métricas", "automação", "workflow", "pipeline", "deploy", "produção",
    "gates", "teste", "testes", "erro", "retry", "permissão",
    "permissões", "token", "tokens", "docker", "auditoria", "isolamento",
    "api", "apis", "dados", "avaliação", "sistema", "sistemas", "software",
    "código", "segurança", "qualidade", "confiabilidade", "arquitetura",
    "design", "produto", "escalabilidade", "performance", "integração",
    "devops", "cloud", "autônomo", "autônomos", "inteligência", "raciocínio",
    "governança", "inteligência artificial", "sistema autônomo", "aprendizado",
    "contrato", "schema", "índice", "backend", "frontend", "interface",
    "banco de dados", "testes automatizados", "versionamento", "repositório",
    "documentação", "metodologia", "entregas", "requisitos",
    # finanças / negócios / saúde
    "finanças", "financeiro", "gestão", "clínica", "odontologia", "receita",
    "custo", "custos", "lucro", "investimento", "orçamento", "planejamento",
    "marketing", "vendas", "estratégia", "indicadores", "fluxo de caixa",
    "precificação", "cobrança", "paciente", "pacientes", "agenda", "escala",
}


def _normalizar_texto(texto):
    return re.sub(r"[^a-zà-ú0-9 ]", " ", (texto or "").lower())


def derivar_tags_arte(sumario, config):
    """Termos tecnicos do dominio (ate 4) presentes no material, para as artes.

    Prioriza titulo_obra/tema/projeto_pratico; completa com pilares e titulos
    de capitulos. Nunca devolve a metafora condutora. Fallback: lista vazia
    (o gerador usa o vocabulario condutor)."""
    sumario = sumario or {}
    config = config or {}
    prioritarias = [
        sumario.get("titulo_obra", ""), config.get("tema", ""),
        config.get("projeto_pratico", ""), sumario.get("introducao", ""),
    ]
    complementares = []
    for parte in sumario.get("partes", []):
        complementares.append(parte.get("titulo_parte", ""))
        for cap in parte.get("capitulos", []):
            complementares.append(cap.get("titulo", ""))
            complementares.extend(cap.get("pilares_previstos", []))
    complementares.append(sumario.get("conclusao", ""))

    def _coletar(fontes):
        texto = _normalizar_texto(" ".join(fontes))
        achadas = []
        # multi-palavra e termos mais especificos primeiro (comprimento desc);
        # pula termos que sao substring de outro ja aceito (evita
        # 'sistema autônomo' + 'sistema' + 'autônomo' e 'agentes' + 'agente')
        for termo in sorted(TAGS_TECNICAS, key=len, reverse=True):
            if any(t in termo or termo in t for t in achadas):
                continue
            # borda de palavra: evita falso positivo ('ci' dentro de 'tecnicas')
            if re.search(r"\b" + re.escape(termo) + r"\b", texto):
                achadas.append(termo)
            if len(achadas) >= 4:
                break
        return [t.title() for t in achadas]

    tags = _coletar(prioritarias)
    if len(tags) < 4:
        for t in _coletar(complementares):
            if t.lower() not in {x.lower() for x in tags}:
                tags.append(t)
            if len(tags) >= 4:
                break
    return tags[:4]


# Frases de CTA padrao por tipo de material (usadas quando o manifesto nao tem cta_url)
CTA_PADRAO = {
    "livro": "Garanta o livro completo",
    "tcc": "Acesse o TCC completo",
    "artigo": "Leia o artigo completo",
    "ebook": "Baixe o e-book completo",
    "playbook": "Baixe o playbook",
    "lead-magnet": "Baixe o material gratuito",
    "deck": "Baixe o deck completo",
}


def console_utf8():
    TO.console_utf8()


def _ler_json(caminho, padrao=None):
    try:
        return json.loads(Path(caminho).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return padrao


def nome_material(slug):
    """'livros/obra-teste' ou 'output/.../livros/obra-teste' -> 'obra-teste'.

    V5.1: limita a 20 chars para evitar caminhos que excedem MAX_PATH (260)."""
    import nomes_curtos as NC
    nome_completo = Path(str(slug).replace("\\", "/")).name
    return NC.nome_curto(nome_completo, max_palavras=2, maximo=20)


def chave_colecao(slug_material, base=None):
    """Chave (serie_key) da colecao a que o material pertence."""
    base = Path(base) if base is not None else DIR_OUTPUT
    config = _ler_json(TO.dir_obra(slug_material, base) / "config_obra.json")
    return resolver_serie_key(config, slug_material)


def dir_campanhas(slug_material, base=None):
    """Hub de campanhas da colecao: output/<colecao>/campanhas (HUB por colecao)."""
    base = Path(base) if base is not None else DIR_OUTPUT
    return base / chave_colecao(slug_material, base) / "campanhas"


def dir_campanha_material(slug_material, base=None):
    """Pasta da campanha de UM material: <hub>/campanhas/<nome-material>.

    V5.1: valida MAX_PATH antes de retornar."""
    import nomes_curtos as NC
    caminho = dir_campanhas(slug_material, base) / nome_material(slug_material)
    if NC.excede_max_path(caminho):
        print(f"[AVISO] Caminho excede MAX_PATH: {len(str(caminho.resolve()))} chars")
        print(f"  {caminho}")
    return caminho


def carregar_manifesto_colecao(chave, base=None):
    """Manifesto da colecao: <hub>/colecoes/<chave>.json (fallback plano).

    O arquivo e gravado pelo colecao.py com o slug normalizado de `chave`
    (mesmo padrao de _slug_arquivo: minusculas, separador '-').
    """
    base = Path(base) if base is not None else DIR_OUTPUT
    slug = re.sub(r"[^a-z0-9]+", "-", (chave or "").lower()).strip("-") or "colecao"
    hub = base / chave / "colecoes" / f"{slug}.json"
    if hub.exists():
        return _ler_json(hub)
    return _ler_json(base / "colecoes" / f"{slug}.json")


def contexto_material(slug_material, base=None):
    """Dados do material para gerar copy/artes: config_obra + sumario + manifesto."""
    base = Path(base) if base is not None else DIR_OUTPUT
    dir_obra = TO.dir_obra(slug_material, base)
    config = _ler_json(dir_obra / "config_obra.json", {})
    sumario = _ler_json(dir_obra / "sumario_macro.json", {})
    chave = resolver_serie_key(config, slug_material)
    manifesto = carregar_manifesto_colecao(chave, base) or {}
    nucleo = manifesto.get("nucleo", {})
    motivo = nucleo.get("motivo_condutor", {}) or sumario.get("motivo_condutor", {})
    vocabulario = motivo.get("vocabulario", [])
    tipo = config.get("tipo_obra", TO.tipo_por_prefixo(slug_material) or "material")
    return {
        "slug": slug_material,
        "nome": nome_material(slug_material),
        "tipo": tipo,
        "colecao": chave,
        "titulo": (config.get("titulo_obra") or config.get("tema")
                   or nucleo.get("titulo") or nome_material(slug_material)),
        "subtitulo": config.get("subtitulo") or "",
        "projeto_pratico": config.get("projeto_pratico") or "",
        "senioridade": (config.get("senioridade_obra")
                        or nucleo.get("senioridade") or ""),
        "vocabulario": vocabulario,
        "tags_arte": derivar_tags_arte(sumario, config),
        "cor_accent": resolver_cor(chave, slug_material),
        "cta_url": next((m.get("cta_url") for m in manifesto.get("membros", [])
                         if m.get("slug") == slug_material), None),
        "cta": CTA_PADRAO.get(tipo, "Saiba mais"),
        "membros": manifesto.get("membros", []),
    }


def texto_nome(pasta, indice, sequencia=None):
    """Nome de arquivo de texto por pasta: post-01.md, story-01.md,
    resposta-direct.md, email-01-nutricao.md, msg-02-divulgacao.md."""
    base = {"post": "post", "feed-story": "story", "resposta-direct": "resposta-direct"}
    if pasta == "resposta-direct":
        return "resposta-direct.md"
    prefixo = base.get(pasta, pasta)
    if sequencia:
        return f"{prefixo}-{indice:02d}-{sequencia}.md"
    return f"{prefixo}-{indice:02d}.md"


def pasta_de_texto(prefixo, sequencia):
    """Pasta final onde um texto de sequencia vive (textos/<sequencia>/...)."""
    return f"textos/{sequencia}" if sequencia else f"textos/{prefixo}"


def cronograma_nome(redes, dias=None):
    """cronograma-ig.md / cronograma-li.md / cronograma-30d-emails.md ..."""
    if redes == "instagram":
        return "cronograma-ig.md"
    if redes == "linkedin":
        return "cronograma-li.md"
    canal, _, sequencia = redes.partition(":")
    return f"cronograma-{dias}d-{canal}-{sequencia}.md"


def carregar_estado(chave, base=None):
    """campanha.json da colecao (estado: materiais + status + identidade)."""
    base = Path(base) if base is not None else DIR_OUTPUT
    return _ler_json(base / chave / "campanhas" / "campanha.json", {})


def salvar_estado(chave, estado, base=None):
    base = Path(base) if base is not None else DIR_OUTPUT
    destino = base / chave / "campanhas" / "campanha.json"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(estado, ensure_ascii=False, indent=2),
                       encoding="utf-8")
    return destino


def estrutura_material(ctx):
    """Caminhos (relativos a pasta do material) de todas as pastas do registro."""
    pastas = []
    for rede, dados in REDES_SOCIAIS.items():
        raiz = f"redes-sociais/{rede}"
        for formato in dados.get("artes", {}):
            pastas.append(f"{raiz}/artes/{formato}")
        for pasta_texto in dados.get("textos", {}):
            pastas.append(f"{raiz}/{pasta_de_texto(pasta_texto, None)}")
        if dados.get("templates"):
            pastas.append(f"{raiz}/templates")
        pastas.append(f"{raiz}/cronograma-divulgacao")
    for canal, dados in CANAIS_COMUNICACAO.items():
        for sequencia, conf in dados.get("sequencias", {}).items():
            raiz = f"canais-comunicacao/{canal}/{sequencia}"
            if conf.get("templates"):
                pastas.append(f"{raiz}/templates")
            pastas.append(f"{raiz}/textos")
            if conf.get("artes"):
                pastas.append(f"{raiz}/artes")
            pastas.append(f"{raiz}/cronograma-divulgacao")
    return sorted(set(pastas))
