#!/usr/bin/env python3
"""
V5 — Registro declarativo de TIPOS DE OBRA (substitui o dispatch `if tipo == ...`).

Antes da V5 cada tipo novo exigia editar 6 arquivos (parametros_obra, fatiar-obra,
auditar-obra, gerar-capa, metadados_livro, compilar-para-pdf). Agora um tipo novo e
UMA entrada de dicionario aqui; os 6 scripts consultam este registro.

Campos do descritor:
  rotulo                 nome humano (PT-BR)
  raiz_output            pasta de topo em output/ (ex.: "playbooks")
  sufixo_slug            marcador do slug derivado (ex.: "--pbk"); None = obra raiz
  derivado_de            tupla de tipos-mae aceitos; () = obra raiz (nasce da pesquisa)
  natureza               "geracao" | "expansao" | "compressao" | "extracao"
  custo_llm              "alto" | "medio" | "baixo" | "zero"  (guia de token economy)
  dimensoes_capa         (largura, altura) em px, ou None se nao tem capa propria
  template_typ           nome do arquivo em templates/, ou None (usa template.typ)
  validador              script de gate em scripts/, ou None
  extensoes_saida        artefatos finais esperados
  min_refs_padrao        minimo de referencias por capitulo/secao
  citacao                "numerica" | "autor-data" | None
  numerar_secoes         passa --number-sections ao Pandoc
  coletor_metadados      nome da funcao em metadados_livro.py (ou None)
  variaveis_pandoc       nome da funcao de variaveis em metadados_livro.py (ou None)
  exige_cta              exige cta_url/cta_texto em config_obra.json
  membro_colecao         entra no manifesto da colecao
  perguntavel_na_fase0   /esbocar pode oferecer como obra raiz

Uso como biblioteca:
    from tipos_obra import TIPOS, descritor, tipos_validos, raiz_output, slug_completo

Uso como CLI:
    python scripts/tipos_obra.py --listar
    python scripts/tipos_obra.py playbook --json
    python scripts/tipos_obra.py --matriz        # matriz de derivacao
"""

import argparse
import json
import sys
from pathlib import Path

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"


def console_utf8():
    """Impede que um caractere fora do cp1252 derrube um script no console Windows.

    Os relatorios da V5 usam ①..⑦ (partes do card) e travessoes. Escrever isso no
    console padrao do Windows levanta UnicodeEncodeError e mata o processo no meio
    de um gate — o relatorio JSON ja foi gravado, mas o exit code se perde."""
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError):   # fluxo redirecionado/nao reconfiguravel
            pass


TIPOS = {
    # ── OBRAS RAIZ (nascem da pesquisa; custo alto) ────────────────────────────
    "livro": {
        "rotulo": "Livro",
        "raiz_output": "livros",
        "sufixo_slug": None,
        "derivado_de": (),
        "natureza": "geracao",
        "custo_llm": "alto",
        "dimensoes_capa": (1600, 2263),
        "template_typ": "template.typ",
        "validador": None,
        "extensoes_saida": (".pdf", ".epub"),
        "min_refs_padrao": 3,
        "citacao": "numerica",
        "numerar_secoes": True,
        "coletor_metadados": "coletar",
        "variaveis_pandoc": "variaveis_pandoc",
        "exige_cta": False,
        "membro_colecao": True,
        "perguntavel_na_fase0": True,
    },
    "tcc": {
        "rotulo": "TCC",
        "raiz_output": "tccs",
        "sufixo_slug": None,
        "derivado_de": (),
        "natureza": "geracao",
        "custo_llm": "alto",
        "dimensoes_capa": (1600, 2263),
        "template_typ": "template_tcc.typ",
        "validador": "validar-abnt-tcc.py",
        "extensoes_saida": (".pdf",),
        "min_refs_padrao": 8,
        "citacao": "autor-data",
        "numerar_secoes": False,
        "coletor_metadados": "coletar_tcc",
        "variaveis_pandoc": "variaveis_pandoc_tcc",
        "exige_cta": False,
        "membro_colecao": True,
        "perguntavel_na_fase0": True,
    },

    # ── DERIVADOS POR COMPRESSAO (custo baixo) ────────────────────────────────
    "artigo": {
        "rotulo": "Artigo Científico",
        "raiz_output": "artigos",
        "sufixo_slug": "--art",
        "derivado_de": ("livro", "tcc"),
        "natureza": "compressao",
        "custo_llm": "baixo",
        "dimensoes_capa": None,
        "template_typ": "template_artigo.typ",
        "validador": None,
        "extensoes_saida": (".pdf",),
        "min_refs_padrao": 5,
        "citacao": "autor-data",
        "numerar_secoes": False,
        "coletor_metadados": "coletar_artigo",
        "variaveis_pandoc": "variaveis_pandoc_artigo",
        "exige_cta": False,
        "membro_colecao": True,
        "perguntavel_na_fase0": False,
    },
    "ebook": {
        "rotulo": "E-book",
        "raiz_output": "ebooks",
        "sufixo_slug": "--eb",
        "derivado_de": ("livro",),
        "natureza": "compressao",
        "custo_llm": "baixo",
        "dimensoes_capa": (1200, 1600),
        "template_typ": "template.typ",
        "validador": None,
        "extensoes_saida": (".epub", ".pdf"),
        "min_refs_padrao": 0,
        "citacao": "numerica",
        "numerar_secoes": False,
        "coletor_metadados": "coletar",
        "variaveis_pandoc": "variaveis_pandoc",
        "exige_cta": False,
        "membro_colecao": True,
        "perguntavel_na_fase0": False,
    },

    # ── DERIVADOS POR EXTRACAO DETERMINISTICA (custo ~zero) ────────────────────
    "playbook": {
        "rotulo": "Playbook",
        "raiz_output": "playbooks",
        "sufixo_slug": "--pbk",
        "derivado_de": ("livro",),
        "natureza": "extracao",
        "custo_llm": "zero",
        "dimensoes_capa": (1600, 2263),
        "template_typ": "template_playbook.typ",
        "validador": "validar-playbook.py",
        "extensoes_saida": (".pdf",),
        "min_refs_padrao": 0,
        "citacao": None,
        "numerar_secoes": False,
        "coletor_metadados": "coletar_playbook",
        "variaveis_pandoc": "variaveis_pandoc_playbook",
        "exige_cta": False,
        "membro_colecao": True,
        "perguntavel_na_fase0": False,
    },
    "lead-magnet": {
        "rotulo": "Lead Magnet",
        "raiz_output": "lead-magnets",
        "sufixo_slug": "--lm",
        "derivado_de": ("playbook", "livro"),
        "natureza": "extracao",
        "custo_llm": "zero",
        "dimensoes_capa": (2480, 3508),      # A4 @ 300dpi
        "dimensoes_social": (1080, 1350),    # card de anuncio/feed
        "template_typ": "template_lead_magnet.typ",
        "validador": "validar-lead-magnet.py",
        "extensoes_saida": (".pdf", ".png"),
        "min_refs_padrao": 0,
        "citacao": None,
        "numerar_secoes": False,
        "coletor_metadados": "coletar_lead_magnet",
        "variaveis_pandoc": "variaveis_pandoc_lead_magnet",
        "exige_cta": True,
        "membro_colecao": True,
        "perguntavel_na_fase0": False,
    },
    "deck": {
        "rotulo": "Slide Deck",
        "raiz_output": "decks",
        "sufixo_slug": "--deck",
        "derivado_de": ("livro", "tcc"),
        "natureza": "extracao",
        "custo_llm": "zero",
        "dimensoes_capa": (1920, 1080),
        "template_typ": "template_deck.typ",
        "validador": "validar-deck.py",
        "extensoes_saida": (".pdf",),
        "min_refs_padrao": 0,
        "citacao": None,
        "numerar_secoes": False,
        "coletor_metadados": "coletar_deck",
        "variaveis_pandoc": "variaveis_pandoc_deck",
        "exige_cta": True,
        "membro_colecao": True,
        "perguntavel_na_fase0": False,
    },
    "emails": {
        "rotulo": "Sequência de E-mails",
        "raiz_output": "emails",
        "sufixo_slug": "--eml",
        "derivado_de": ("playbook", "livro"),
        "natureza": "extracao",
        "custo_llm": "baixo",
        "dimensoes_capa": None,
        "template_typ": None,
        "validador": "validar-emails.py",
        "extensoes_saida": (".md",),
        "min_refs_padrao": 0,
        "citacao": None,
        "numerar_secoes": False,
        "coletor_metadados": None,
        "variaveis_pandoc": None,
        "exige_cta": True,
        "membro_colecao": True,
        "perguntavel_na_fase0": False,
    },
}


# ── Formatos de LEAD MAGNET ───────────────────────────────────────────────────
# Cada formato e uma QUERY DE AGREGACAO sobre os campos dos cards do playbook.
# `campo_card` None = nao vem dos cards (usa sumario_macro).
FORMATOS_LM = {
    "checklist": {
        "rotulo": "Checklist Mestre",
        "campo_card": "feito_quando",
        "titulo_padrao": "Checklist Mestre: {tema}",
        "promessa": "O checklist completo de {n} etapas para {tema}",
        "min_itens": 8,
        "max_paginas": 8,
    },
    "armadilhas": {
        "rotulo": "Guia de Armadilhas",
        "campo_card": "armadilhas",
        "titulo_padrao": "As {n} Armadilhas de {tema}",
        "promessa": "Os {n} erros que travam quem está começando em {tema}",
        "min_itens": 6,
        "max_paginas": 10,
    },
    "cheatsheet": {
        "rotulo": "Cheat Sheet de Comandos",
        "campo_card": "execucao",
        "titulo_padrao": "Cheat Sheet: {tema}",
        "promessa": "Todos os comandos de {tema} em uma folha de bancada",
        "min_itens": 6,
        "max_paginas": 6,
    },
    "mapa": {
        "rotulo": "Mapa de Estágios",
        "campo_card": None,
        "titulo_padrao": "O Mapa de {tema}",
        "promessa": "A rota completa de {tema} em uma única folha",
        "min_itens": 3,
        "max_paginas": 4,
    },
    "entregas": {
        "rotulo": "Mapa de Entregas",
        "campo_card": "entregas",
        "titulo_padrao": "Mapa de Entregas: {tema}",
        "promessa": "Todos os artefatos que você produz em {tema}",
        "min_itens": 6,
        "max_paginas": 6,
    },
    "mini-guia": {
        "rotulo": "Mini-guia",
        "campo_card": None,
        "titulo_padrao": "Mini-guia: {tema}",
        "promessa": "O primeiro passo de {tema}, do início ao fim",
        "min_itens": 1,
        "max_paginas": 12,
    },
}

FORMATO_LM_PADRAO = "checklist"


# ── API ───────────────────────────────────────────────────────────────────────

def tipos_validos():
    return tuple(TIPOS.keys())


def descritor(tipo):
    """Descritor do tipo; KeyError explicito se desconhecido."""
    d = TIPOS.get(tipo)
    if d is None:
        raise KeyError(
            f"tipo_obra desconhecido: {tipo!r}. Validos: {', '.join(tipos_validos())}"
        )
    return d


def campo(tipo, nome, padrao=None):
    """Leitura tolerante de um campo do descritor (nao levanta se tipo ausente)."""
    return TIPOS.get(tipo, {}).get(nome, padrao)


def raiz_output(tipo):
    return descritor(tipo)["raiz_output"]


def tipos_raiz():
    """Tipos que nascem da pesquisa (nao derivam de ninguem)."""
    return tuple(t for t, d in TIPOS.items() if not d["derivado_de"])


def tipos_derivados():
    return tuple(t for t, d in TIPOS.items() if d["derivado_de"])


def derivaveis_de(tipo_mae):
    """Tipos que podem ser gerados a partir de `tipo_mae`."""
    return tuple(t for t, d in TIPOS.items() if tipo_mae in d["derivado_de"])


def validar_derivacao(tipo_filho, tipo_mae):
    """Retorna lista de erros (vazia = derivacao permitida)."""
    d = descritor(tipo_filho)
    if not d["derivado_de"]:
        return [f"{tipo_filho} e obra raiz — nao deriva de {tipo_mae}"]
    if tipo_mae not in d["derivado_de"]:
        return [f"{tipo_filho} deriva de {' ou '.join(d['derivado_de'])}, "
                f"nao de {tipo_mae}"]
    return []


def slug_completo(tipo, slug_simples):
    """'playbook', 'meu-livro--pbk' -> 'playbooks/meu-livro--pbk'."""
    return f"{raiz_output(tipo)}/{slug_simples}"


def slug_derivado(tipo, slug_mae_simples, indice=None, sufixo_titulo=None):
    """Monta o slug simples de um derivado seguindo a convencao <mae>--<sfx>[-NN][-titulo]."""
    sufixo = descritor(tipo)["sufixo_slug"]
    if sufixo is None:
        return slug_mae_simples
    partes = [f"{slug_mae_simples}{sufixo}"]
    if indice is not None:
        partes.append(f"{indice:02d}")
    if sufixo_titulo:
        partes.append(sufixo_titulo)
    return "-".join(partes)


def tipo_por_prefixo(slug):
    """'playbooks/foo--pbk' -> 'playbook'. None se o prefixo nao for de nenhum tipo."""
    prefixo = Path(slug).parts[0] if "/" in slug or "\\" in slug else None
    if prefixo is None:
        return None
    for tipo, d in TIPOS.items():
        if d["raiz_output"] == prefixo:
            return tipo
    return None


def dir_obra(slug):
    return DIR_OUTPUT / slug


def template_de(tipo):
    """Caminho do template Typst; cai no template.typ do livro se o proprio nao existir."""
    nome = campo(tipo, "template_typ")
    if not nome:
        return None
    caminho = DIR_PROJETO / "templates" / nome
    if caminho.exists():
        return caminho
    return DIR_PROJETO / "templates" / "template.typ"


def validador_de(tipo):
    nome = campo(tipo, "validador")
    return (DIR_PROJETO / "scripts" / nome) if nome else None


def dimensoes_capa(tipo, variante=None):
    """variante=None -> capa padrao; variante='social' -> card 1080x1350."""
    chave = "dimensoes_social" if variante == "social" else "dimensoes_capa"
    return campo(tipo, chave)


def usa_citacao_autor_data(tipo):
    return campo(tipo, "citacao") == "autor-data"


def exige_referencias(tipo):
    return bool(campo(tipo, "min_refs_padrao", 0))


def defaults_config(tipo, slug_mae_simples=None, extra=None):
    """config_obra.json minimo e coerente para um tipo (usado por fatiar-obra.py)."""
    d = descritor(tipo)
    cfg = {
        "tipo_obra": tipo,
        "min_referencias_por_capitulo": d["min_refs_padrao"],
        "tamanho_obra": None,
        "gerar_artigos": False, "qtd_artigos": 0,
        "gerar_ebooks": False, "qtd_ebooks": 0,
        "gerar_playbook": False,
        "gerar_lead_magnets": False, "formatos_lm": [],
        "gerar_deck": False,
        "gerar_emails": False,
    }
    if slug_mae_simples:
        cfg["livro_mae"] = slug_mae_simples      # chave historica (series_capa.py)
        cfg["obra_mae"] = slug_mae_simples
    if extra:
        cfg.update(extra)
    return cfg


def matriz_derivacao():
    """Lista [(mae, filho, natureza, custo)] para relatorio/documentacao."""
    linhas = []
    for filho, d in TIPOS.items():
        for mae in d["derivado_de"] or ("(raiz)",):   # ASCII: console Windows
            linhas.append((mae, filho, d["natureza"], d["custo_llm"]))
    return linhas


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    console_utf8()
    ap = argparse.ArgumentParser(description="Registro declarativo de tipos de obra (V5)")
    ap.add_argument("tipo", nargs="?", help="tipo a inspecionar (ex.: playbook)")
    ap.add_argument("--listar", action="store_true", help="lista todos os tipos")
    ap.add_argument("--matriz", action="store_true", help="matriz de derivacao mae -> filho")
    ap.add_argument("--formatos-lm", action="store_true", help="lista formatos de lead magnet")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.matriz:
        if args.json:
            print(json.dumps(matriz_derivacao(), ensure_ascii=False, indent=2))
            return 0
        print(f"{'MAE':<12} {'FILHO':<14} {'NATUREZA':<12} CUSTO LLM")
        print("-" * 52)
        for mae, filho, natureza, custo in matriz_derivacao():
            print(f"{mae:<12} {filho:<14} {natureza:<12} {custo}")
        return 0

    if args.formatos_lm:
        if args.json:
            print(json.dumps(FORMATOS_LM, ensure_ascii=False, indent=2))
            return 0
        for chave, f in FORMATOS_LM.items():
            fonte = f["campo_card"] or "sumario_macro"
            print(f"{chave:<12} {f['rotulo']:<26} fonte: {fonte}")
        return 0

    if args.listar or not args.tipo:
        if args.json:
            print(json.dumps(TIPOS, ensure_ascii=False, indent=2))
            return 0
        print(f"{'TIPO':<14} {'RAIZ':<14} {'DERIVA DE':<18} {'NATUREZA':<12} CUSTO")
        print("-" * 70)
        for tipo, d in TIPOS.items():
            deriva = ", ".join(d["derivado_de"]) or "(raiz)"
            print(f"{tipo:<14} {d['raiz_output']:<14} {deriva:<18} "
                  f"{d['natureza']:<12} {d['custo_llm']}")
        return 0

    try:
        d = descritor(args.tipo)
    except KeyError as exc:
        print(f"[ERRO] {exc}")
        return 1

    if args.json:
        print(json.dumps(d, ensure_ascii=False, indent=2))
        return 0
    for k, v in d.items():
        print(f"{k:<22}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
