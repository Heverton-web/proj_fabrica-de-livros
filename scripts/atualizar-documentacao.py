#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atualizar-documentacao.py — Mantém os manuais (MD + PDF + capa) sincronizados.

Recompila apenas o que mudou (compara mtime do .md com o .pdf) e regenera a
capa gráfica quando ela não existe. Usado pelos hooks do .claude/settings.json
e manualmente pelos comandos abaixo.

Uso:
    python scripts/atualizar-documentacao.py                # só o que mudou
    python scripts/atualizar-documentacao.py --forcar       # recompila tudo
    python scripts/atualizar-documentacao.py --se-sujo      # só se o working tree estiver sujo
    python scripts/atualizar-documentacao.py --silencioso   # sem prints de progresso
    python scripts/atualizar-documentacao.py docs/manual-completo-fabrica.md   # 1 arquivo

Regras do projeto aplicadas:
  - Pandoc -> .typ -> typst compile (nunca --pdf-engine=typst com figuras no Windows)
  - Capa via scripts/gerar-capa.py (gerar_capa), padrão REGRA 5 (2D plano, badge)
  - UTF-8 no console Windows (sys.stdout.reconfigure)
  - Hooks nunca bloqueiam (|| exit 0)
"""

from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_SCRIPTS = DIR_PROJETO / "scripts"
DIR_DOCS = DIR_PROJETO / "docs"
DIR_TEMPLATES = DIR_PROJETO / "templates"

AUTOR = "Heverton Eduardo Peres"
QUALIFICACAO = "Especialista em Marketing e Desenvolvimento de Soluções"

# Registro dos manuais mantidos por este script.
# chave: nome do .md dentro de docs/ (sem extensão)
MANUAIS = {
    "manual-completo-fabrica": {
        "titulo": "MANUAL COMPLETO",
        "subtitulo": "FÁBRICA AGÊNTICA DE PUBLICAÇÕES — CRIAÇÃO DE MATERIAIS | CRIAÇÃO DE MÁQUINA DE VENDAS",
        "cor_acento": "#58a6ff",
        "badge": "NÍVEL AVANÇADO",
    },
    "guia-execucao-maquina-vendas": {
        "titulo": "GUIA DE EXECUÇÃO",
        "subtitulo": "MÁQUINA DE VENDAS — PASSO A PASSO: CRIAR, PERSONALIZAR, TESTAR, PUBLICAR E OPERAR",
        "cor_acento": "#f0933b",
        "badge": "NÍVEL INTERMEDIÁRIO",
    },
    "guia-execucao-detectar-llms-gratuitas": {
        "titulo": "GUIA DE EXECUÇÃO",
        "subtitulo": "DETECTOR UNIVERSAL DE LLMs GRATUITAS — MAPEAMENTO DE HARNESS, PROVEDORES E MODELOS ATIVOS",
        "cor_acento": "#a855f7",
        "badge": "NÍVEL INTERMEDIÁRIO",
    },
}


def carregar_gerar_capa():
    """Importa gerar_capa() de scripts/gerar-capa.py (nome com hífen não é importável)."""
    caminho = DIR_SCRIPTS / "gerar-capa.py"
    spec = importlib.util.spec_from_file_location("gerar_capa_mod", caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod.gerar_capa


def precisa_atualizar(md: Path, pdf: Path, forcar: bool) -> bool:
    if forcar:
        return True
    if not pdf.exists():
        return True
    return md.stat().st_mtime > pdf.stat().st_mtime


def git_sujo() -> bool:
    try:
        r = subprocess.run(
            ["git", "status", "--porcelain"], cwd=DIR_PROJETO,
            capture_output=True, text=True, timeout=15,
        )
        return bool(r.stdout.strip())
    except Exception:
        return True  # sem git: assume sujo (não bloqueia)


def gerar_capa_manual(nome, meta, forcar, silencioso):
    """Gera docs/imagens/capa_<nome>.png se faltar (ou --forcar)."""
    dir_imagens = DIR_DOCS / "imagens"
    dir_imagens.mkdir(exist_ok=True)
    png = dir_imagens / f"capa_{nome}.png"
    if png.exists() and not forcar:
        return png
    if not silencioso:
        print(f"[capa] gerando {png.name} ...")
    gerar_capa = carregar_gerar_capa()
    return gerar_capa(
        titulo=meta["titulo"],
        subtitulo=meta["subtitulo"],
        dir_saida=DIR_DOCS,
        tipo="livro",
        cor_acento=meta["cor_acento"],
        autor=AUTOR,
        qualificacao=QUALIFICACAO,
        badge_texto=meta["badge"],
        nome_arquivo=png.name,
    )


def compilar_pdf(nome, meta, silencioso):
    """pandoc -> .typ -> typst compile, com capa gráfica e cor de accent."""
    md = DIR_DOCS / f"{nome}.md"
    pdf = DIR_DOCS / f"{nome}.pdf"
    capa = DIR_DOCS / "imagens" / f"capa_{nome}.png"

    cmd = [
        "pandoc", str(md.relative_to(DIR_PROJETO)),
        "-o", str(pdf.relative_to(DIR_PROJETO)),
        "--pdf-engine=typst",
        f"--template={DIR_TEMPLATES / 'template.typ'}",
        # sem --toc: o template.typ já renderiza #outline (sumário);
        # --toc do pandoc geraria labels com número de seção que não existem.
        "--number-sections",
        f"-Vcapa_imagem={capa.relative_to(DIR_PROJETO).as_posix()}",
        f"-Vcor_acento={meta['cor_acento']}",
        f"-Vtitle={meta['titulo']}",
        f"-Vsubtitle={meta['subtitulo']}",
        f"-Vauthor={AUTOR}",
    ]
    if not silencioso:
        print(f"[pdf] {md.name} -> {pdf.name}")
    r = subprocess.run(cmd, cwd=DIR_PROJETO, capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        print(f"[ERRO] pandoc {md.name}: {r.stderr[-2000:]}", file=sys.stderr)
        return False
    if not silencioso:
        print(f"[OK] {pdf.name} ({pdf.stat().st_size // 1024} KB)")
    return True


def main():
    ap = argparse.ArgumentParser(description="Mantém os manuais (MD+PDF+capa) sincronizados.")
    ap.add_argument("alvo", nargs="*", help="nomes ou paths dos manuais (default: todos)")
    ap.add_argument("--forcar", action="store_true", help="recompila tudo, ignorando mtime")
    ap.add_argument("--se-sujo", action="store_true", help="só processa se o working tree estiver sujo")
    ap.add_argument("--silencioso", action="store_true", help="sem prints de progresso")
    args = ap.parse_args()

    alvos = []
    for a in args.alvo:
        p = Path(a)
        alvos.append(p.stem if p.suffix == ".md" else p.name)
    alvos = [a for a in alvos if a in MANUAIS] or list(MANUAIS)

    if args.se_sujo and not git_sujo():
        if not args.silencioso:
            print("[i] working tree limpo — nada a fazer")
        return 0

    erros = 0
    for nome in alvos:
        meta = MANUAIS[nome]
        md = DIR_DOCS / f"{nome}.md"
        pdf = DIR_DOCS / f"{nome}.pdf"
        if not md.exists():
            print(f"[ERRO] {md} não existe", file=sys.stderr)
            erros += 1
            continue
        if not precisa_atualizar(md, pdf, args.forcar):
            if not args.silencioso:
                print(f"[i] {nome}: PDF atualizado, nada a fazer (--forcar para recompilar)")
            continue
        try:
            gerar_capa_manual(nome, meta, args.forcar, args.silencioso)
            if not compilar_pdf(nome, meta, args.silencioso):
                erros += 1
        except Exception as e:  # noqa: BLE001 — hook não pode derrubar a sessão
            print(f"[ERRO] {nome}: {e}", file=sys.stderr)
            erros += 1

    if erros:
        print(f"[FALHA] {erros} manual(ns) com erro", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
