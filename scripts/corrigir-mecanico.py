#!/usr/bin/env python3
"""
Correções mecânicas do revisor-tecnico (Fase 2.5).

`auditar-obra.py` já LOCALIZA com precisão 4 classes de defeito (linha/capítulo);
hoje a LLM do `revisor-tecnico` reescreve o capítulo para corrigir todas elas,
mas 3 são puramente mecânicas — zero julgamento envolvido:

  R9  — horizontal rule (`---`/`***`/`___`) solta fora do frontmatter: remove.
  R14 — citação [N] <-> referência com numeração gapada/fora de ordem, mas em
        bijeção exata (mesmo conjunto de números citados e listados): renumera
        1..K sequencial. Órfãs/não citadas de verdade (sem correspondência)
        NUNCA são "corrigidas" aqui — ficam reportadas para julgamento humano/LLM,
        porque resolver isso exige saber qual fonte falta ou o que cortar.
  Grafia — termo grafado de formas diferentes entre capítulos: canonicaliza
        para a forma mais frequente na obra, fora de blocos de código.

Uso:
    python scripts/corrigir-mecanico.py <slug>                 # aplica em todos os capítulos
    python scripts/corrigir-mecanico.py <slug> --capitulo 3     # só 1 capítulo
    python scripts/corrigir-mecanico.py <slug> --dry-run        # só reporta, não grava
"""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

import tipos_obra as TO
from secoes_eita import RE_CODIGO, dividir_secoes, sem_acento
from tipos_obra import console_utf8

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

RE_HR = re.compile(r"^[ \t]*(-{3,}|\*{3,}|_{3,})[ \t]*$", re.MULTILINE)
RE_CITACAO = re.compile(r"\[(\d{1,3})\]")
RE_FRONTMATTER = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)

# Cópia mínima deliberada de `auditar-obra.detectar_inconsistencia_terminologica`
# (mesma heurística) — não importa a CLI de auditar-obra.py para não acoplar
# este script a um módulo com argparse/efeitos de topo.
RE_TERMO = re.compile(r"\b[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ0-9]*(?:[-\.][A-Za-zÀ-ÿ0-9]+)*\b")


def remover_hr_solto(texto):
    """Remove linhas que são só `---`/`***`/`___` fora do frontmatter e fora
    de blocos de código. Retorna (texto_novo, n_removidas)."""
    m = RE_FRONTMATTER.match(texto)
    cabecalho, corpo = (texto[: m.end()], texto[m.end():]) if m else ("", texto)

    blocos_codigo = [(b.start(), b.end()) for b in RE_CODIGO.finditer(corpo)]

    def dentro_de_codigo(pos):
        return any(ini <= pos < fim for ini, fim in blocos_codigo)

    n_removidas = 0
    linhas_novas = []
    pos = 0
    for linha in corpo.splitlines(keepends=True):
        if RE_HR.match(linha.rstrip("\n")) and not dentro_de_codigo(pos):
            n_removidas += 1
        else:
            linhas_novas.append(linha)
        pos += len(linha)
    return cabecalho + "".join(linhas_novas), n_removidas


def renumerar_citacoes(texto):
    """Renumera [N] em todo o capítulo para 1..K sequencial (ordem de 1a
    aparição no corpo), SOMENTE quando o conjunto de números citados no corpo
    (seções 1-6) é idêntico ao conjunto de números listados na seção 7
    (bijeção exata — nada órfão, nada não citado). Caso contrário, não altera
    nada e devolve os conjuntos órfão/não-citado para revisão humana/LLM.

    Retorna dict: {"texto": str, "renumerado": bool, "mapa": {old:new},
                   "orfas": [...], "nao_citadas": [...]}."""
    secoes = dividir_secoes(texto)
    corpo_refs = secoes.get(7, {}).get("corpo", "")
    corpo_texto = texto[: texto.find(corpo_refs)] if corpo_refs else texto

    numeros_refs_vistos = set()
    ordem_refs = []
    for m in re.finditer(r"^\[(\d{1,3})\]", corpo_refs, re.MULTILINE):
        n = int(m.group(1))
        if n not in numeros_refs_vistos:
            numeros_refs_vistos.add(n)
            ordem_refs.append(n)

    numeros_inline_ordenados = []
    vistos_inline = set()
    for m in RE_CITACAO.finditer(RE_CODIGO.sub("", corpo_texto)):
        n = int(m.group(1))
        if n not in vistos_inline:
            vistos_inline.add(n)
            numeros_inline_ordenados.append(n)

    orfas = sorted(vistos_inline - numeros_refs_vistos)
    nao_citadas = sorted(numeros_refs_vistos - vistos_inline)

    if orfas or nao_citadas or not numeros_inline_ordenados:
        return {"texto": texto, "renumerado": False, "mapa": {},
                "orfas": orfas, "nao_citadas": nao_citadas}

    mapa = {antigo: novo for novo, antigo in enumerate(numeros_inline_ordenados, start=1)}
    if all(antigo == novo for antigo, novo in mapa.items()):
        return {"texto": texto, "renumerado": False, "mapa": {},
                "orfas": [], "nao_citadas": []}

    texto_novo = RE_CITACAO.sub(lambda m: f"[{mapa[int(m.group(1))]}]", texto)
    return {"texto": texto_novo, "renumerado": True, "mapa": mapa,
            "orfas": [], "nao_citadas": []}


def detectar_variantes_termo(textos, minimo_ocorrencias=4):
    """[(chave_normalizada, {variante: contagem})] entre múltiplos capítulos."""
    variantes = defaultdict(lambda: defaultdict(int))
    for texto in textos:
        limpo = RE_CODIGO.sub("", texto)
        for m in RE_TERMO.finditer(limpo):
            termo = m.group(0)
            if len(termo) < 4 or termo.isdigit():
                continue
            chave = sem_acento(termo).lower().replace("-", "").replace(".", "")
            variantes[chave][termo] += 1

    achados = []
    for chave, formas in variantes.items():
        if len(formas) < 2 or sum(formas.values()) < minimo_ocorrencias:
            continue
        if len({f.lower() for f in formas}) == 1:
            continue  # so variacao de caixa inicial de frase - nao e inconsistencia
        achados.append((chave, dict(formas)))
    return achados


def canonicalizar_termo(formas):
    """Forma mais frequente; empate resolvido pela primeira em ordem alfabética
    (determinístico — nunca escolha 'aleatória' entre empates)."""
    maior = max(formas.values())
    candidatas = sorted(f for f, n in formas.items() if n == maior)
    return candidatas[0]


def aplicar_grafia_canonica(texto, achados):
    """Substitui, fora de blocos de código, cada variante minoritária pela
    forma canônica (mais frequente na obra). Retorna (texto_novo, n_trocas)."""
    n_trocas = 0
    blocos = [(b.start(), b.end()) for b in RE_CODIGO.finditer(texto)]

    for _chave, formas in achados:
        canonico = canonicalizar_termo(formas)
        for variante in formas:
            if variante == canonico:
                continue
            padrao = re.compile(r"\b" + re.escape(variante) + r"\b")

            def _trocar(m):
                nonlocal n_trocas
                if any(ini <= m.start() < fim for ini, fim in blocos):
                    return m.group(0)
                n_trocas += 1
                return canonico

            texto = padrao.sub(_trocar, texto)
    return texto, n_trocas


def corrigir_capitulo(caminho, dry_run=False):
    """Aplica remover_hr_solto + renumerar_citacoes a 1 arquivo. Retorna relatório."""
    original = caminho.read_text(encoding="utf-8")
    texto, n_hr = remover_hr_solto(original)
    resultado_cit = renumerar_citacoes(texto)
    texto = resultado_cit["texto"]

    if texto != original and not dry_run:
        caminho.write_text(texto, encoding="utf-8")

    return {
        "arquivo": caminho.name,
        "hr_removidas": n_hr,
        "citacoes_renumeradas": resultado_cit["renumerado"],
        "orfas": resultado_cit["orfas"],
        "nao_citadas": resultado_cit["nao_citadas"],
    }


def corrigir_obra(slug, capitulo=None, dry_run=False, base=None):
    dir_cap = TO.dir_obra(slug, base or DIR_OUTPUT) / "capitulos"
    if not dir_cap.exists():
        return {"capitulos": [], "grafia": {}}

    padrao = f"cap_{capitulo}.md" if capitulo else "cap_*.md"
    arquivos = sorted(dir_cap.glob(padrao))

    relatorios = [corrigir_capitulo(a, dry_run=dry_run) for a in arquivos]

    # Grafia: heuristica cruza TODOS os capitulos (nao so o filtrado por --capitulo),
    # senao a forma canonica calculada seria enviesada por um subconjunto da obra.
    todos = sorted(dir_cap.glob("cap_*.md"))
    textos = {a: a.read_text(encoding="utf-8") for a in todos}
    achados = detectar_variantes_termo(list(textos.values()))

    grafia = {}
    if achados:
        for a in arquivos:
            novo, n_trocas = aplicar_grafia_canonica(textos[a], achados)
            if n_trocas and not dry_run:
                a.write_text(novo, encoding="utf-8")
            if n_trocas:
                grafia[a.name] = n_trocas

    return {"capitulos": relatorios, "grafia": grafia, "termos_detectados": len(achados)}


def main():
    console_utf8()
    ap = argparse.ArgumentParser(description="Correções mecânicas do revisor-tecnico (R9/R14/grafia)")
    ap.add_argument("slug")
    ap.add_argument("--capitulo", type=int, help="corrige só este número de capítulo")
    ap.add_argument("--dry-run", action="store_true", help="só reporta, não grava")
    args = ap.parse_args()

    resultado = corrigir_obra(args.slug, capitulo=args.capitulo, dry_run=args.dry_run)

    for rel in resultado["capitulos"]:
        partes = []
        if rel["hr_removidas"]:
            partes.append(f"{rel['hr_removidas']} horizontal rule(s) removida(s)")
        if rel["citacoes_renumeradas"]:
            partes.append("citações renumeradas")
        if rel["orfas"]:
            partes.append(f"ÓRFÃS (revisar manualmente): {rel['orfas']}")
        if rel["nao_citadas"]:
            partes.append(f"NÃO CITADAS (revisar manualmente): {rel['nao_citadas']}")
        if partes:
            print(f"[corrigir-mecanico] {rel['arquivo']}: " + "; ".join(partes))
        else:
            print(f"[corrigir-mecanico] {rel['arquivo']}: nada a corrigir")

    for arquivo, n_trocas in resultado["grafia"].items():
        print(f"[corrigir-mecanico] {arquivo}: {n_trocas} grafia(s) canonicalizada(s)")

    if args.dry_run:
        print("[corrigir-mecanico] --dry-run: nenhum arquivo foi gravado")
    return 0


if __name__ == "__main__":
    sys.exit(main())
