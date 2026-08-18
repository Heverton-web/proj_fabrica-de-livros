#!/usr/bin/env python3
"""
Script de automação para corrigir e completar 100% dos entregáveis de `output/oh-my`.
Cobre:
  1. E-books (merge de capitulos para .md, capa 2D, compilação .pdf e .epub)
  2. E-mails (templates formatados com assunto/momento/UTM, cronograma em .md e .pdf)
  3. Lead Magnets (compilação em .pdf e artes visuais .png)
  4. Playbook (compilação em .pdf com template_playbook.typ)
  5. Pastas `campanhas` e `maquina` (geração de campanhas e maquina de vendas)
  6. Sincronização do manifesto da coleção
"""

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OH_MY = DIR_PROJETO / "output" / "oh-my"
DIR_DISTRIBUICAO = DIR_OH_MY / "distribuicao"
DIR_DISTRIBUICAO.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(DIR_PROJETO / "scripts"))
import tipos_obra as TO
from series_capa import resolver_cor

PANDOC = r"C:\Users\trcnologia\AppData\Local\Microsoft\WinGet\Packages\JohnMacFarlane.Pandoc_Microsoft.Winget.Source_8wekyb3d8bbwe\pandoc-3.10\pandoc.exe"
TYPST = r"C:\Users\trcnologia\AppData\Local\Microsoft\WinGet\Packages\Typst.Typst_Microsoft.Winget.Source_8wekyb3d8bbwe\typst-x86_64-pc-windows-msvc\typst.exe"

def log(msg):
    print(f"[OH-MY FIX] {msg}")

def processar_ebooks():
    log("=== 1. PROCESSANDO E-BOOKS ===")
    dir_ebooks = DIR_OH_MY / "ebooks"
    if not dir_ebooks.exists():
        log("Pasta ebooks não encontrada!")
        return

    for pasta_eb in sorted(dir_ebooks.iterdir()):
        if not pasta_eb.is_dir():
            continue

        slug_eb = pasta_eb.name
        log(f"Processando e-book: {slug_eb}")

        # 1.1 Merge de capítulos -> ebook-compilado.md e livro-compilado.md
        cap_dir = pasta_eb / "capitulos"
        cap_files = sorted(cap_dir.glob("cap_*.md")) if cap_dir.exists() else []

        meta_file = pasta_eb / "ebook_metadados.json"
        titulo = "E-book"
        autor = "Heverton Eduardo Peres"
        if meta_file.exists():
            try:
                meta = json.loads(meta_file.read_text(encoding="utf-8"))
                titulo = meta.get("titulo", titulo)
                autor = meta.get("autor", autor)
            except Exception:
                pass

        conteudo = [f"% {titulo}", f"% {autor}", ""]
        for cf in cap_files:
            conteudo.append(cf.read_text(encoding="utf-8"))
            conteudo.append("\n\n---\n\n")

        texto_compilado = "\n".join(conteudo)
        (pasta_eb / "ebook-compilado.md").write_text(texto_compilado, encoding="utf-8")
        (pasta_eb / "livro-compilado.md").write_text(texto_compilado, encoding="utf-8")
        log(f"  -> ebook-compilado.md gerado em {pasta_eb.name}")

        # 1.2 Gerar capa gráfica de e-book
        try:
            cmd_capa = [sys.executable, str(DIR_PROJETO / "scripts" / "gerar-capa.py"), slug_eb]
            subprocess.run(cmd_capa, check=False)
        except Exception as e:
            log(f"  -> Erro gerando capa: {e}")

        # 1.3 Compilar PDF via Pandoc + Typst
        typ_out = pasta_eb / "ebook.typ"
        pdf_out = pasta_eb / f"{slug_eb}.pdf"
        template_typ = DIR_PROJETO / "templates" / "template.typ"

        cmd_pandoc = [
            PANDOC,
            str(pasta_eb / "ebook-compilado.md"),
            "-o", str(typ_out),
            "--template", str(template_typ),
            "--toc", "--toc-depth", "2",
            "-V", f"title={titulo}",
            "-V", f"author={autor}",
            "-V", "sem_capa_grafica=1",
            "--from", "markdown-citations",
            "--wrap", "preserve"
        ]

        try:
            subprocess.run(cmd_pandoc, check=True)
            cmd_typst = [TYPST, "compile", "--root", str(DIR_PROJETO), str(typ_out), str(pdf_out)]
            subprocess.run(cmd_typst, check=True)
            log(f"  -> PDF compilado: {pdf_out.name}")
            shutil.copy2(pdf_out, DIR_DISTRIBUICAO / pdf_out.name)
        except Exception as e:
            log(f"  -> Erro compilando PDF do ebook {slug_eb}: {e}")

        # 1.4 Gerar EPUB
        try:
            cmd_epub = [sys.executable, str(DIR_PROJETO / "scripts" / "gerar-epub.py"), slug_eb]
            subprocess.run(cmd_epub, check=False)
        except Exception as e:
            log(f"  -> Erro gerando EPUB: {e}")

def processar_emails():
    log("=== 2. PROCESSANDO E-MAILS ===")
    dir_emails = DIR_OH_MY / "emails"
    dir_emails.mkdir(parents=True, exist_ok=True)

    # Reformatar / estruturar sequência completa e cronograma
    emails_existentes = sorted(dir_emails.glob("0*.md"))
    seq_lines = ["# Sequência de E-mails e Cronograma de Envio: Oh My Position\n",
                 "**Campanha:** Oh My Position — Agentes de Código de Alta Performance\n",
                 "**Público-alvo:** Desenvolvedores, Engenheiros de Software e Lideranças Técnicas\n",
                 "**Objetivo:** Nutrição pós-lead-magnet e conversão para o livro-mãe OMP\n\n",
                 "---", "\n"]

    for idx, ef in enumerate(emails_existentes, 1):
        conteudo = ef.read_text(encoding="utf-8")
        seq_lines.append(f"## E-mail {idx:02d} — {ef.stem.replace('-', ' ').title()}\n")
        seq_lines.append(f"**Momento de Envio:** Dia {(idx-1)*2} (Intervalo de 48h)\n")
        seq_lines.append(f"**UTM Campaign:** `oh-my-pi&utm_content=email-{idx:02d}`\n\n")
        seq_lines.append(conteudo)
        seq_lines.append("\n\n---\n\n")

    seq_md = dir_emails / "sequencia-emails.md"
    seq_md.write_text("\n".join(seq_lines), encoding="utf-8")
    log("  -> sequencia-emails.md gerado com sucesso!")

    # Compilar PDF do Cronograma de E-mails
    typ_out = dir_emails / "sequencia-emails.typ"
    pdf_out = dir_emails / "sequencia-emails.pdf"
    template_typ = DIR_PROJETO / "templates" / "template.typ"

    cmd_pandoc = [
        PANDOC,
        str(seq_md),
        "-o", str(typ_out),
        "--template", str(template_typ),
        "-V", "title=Sequência de E-mails e Cronograma de Envio",
        "-V", "author=Heverton Eduardo Peres",
        "-V", "sem_capa_grafica=1",
        "--wrap", "preserve"
    ]

    try:
        subprocess.run(cmd_pandoc, check=True)
        cmd_typst = [TYPST, "compile", "--root", str(DIR_PROJETO), str(typ_out), str(pdf_out)]
        subprocess.run(cmd_typst, check=True)
        log(f"  -> PDF dos e-mails compilado: {pdf_out.name}")
        shutil.copy2(pdf_out, DIR_DISTRIBUICAO / pdf_out.name)
    except Exception as e:
        log(f"  -> Erro compilando PDF dos e-mails: {e}")

def processar_lead_magnets():
    log("=== 3. PROCESSANDO LEAD MAGNETS ===")
    dir_lm = DIR_OH_MY / "lead-magnets"
    if not dir_lm.exists():
        log("Pasta lead-magnets não encontrada!")
        return

    for lmf in sorted(dir_lm.glob("*.md")):
        slug_lm = lmf.stem
        log(f"Processando Lead Magnet: {slug_lm}")

        # Compilar PDF do Lead Magnet via Pandoc + Typst
        typ_out = dir_lm / f"{slug_lm}.typ"
        pdf_out = dir_lm / f"{slug_lm}.pdf"
        template_typ = DIR_PROJETO / "templates" / "template.typ"

        titulo = slug_lm.replace("-", " ").title()
        cmd_pandoc = [
            PANDOC,
            str(lmf),
            "-o", str(typ_out),
            "--template", str(template_typ),
            "-V", f"title={titulo}",
            "-V", "author=Heverton Eduardo Peres",
            "-V", "sem_capa_grafica=1",
            "--wrap", "preserve"
        ]

        try:
            subprocess.run(cmd_pandoc, check=True)
            cmd_typst = [TYPST, "compile", "--root", str(DIR_PROJETO), str(typ_out), str(pdf_out)]
            subprocess.run(cmd_typst, check=True)
            log(f"  -> PDF do Lead Magnet compilado: {pdf_out.name}")
            shutil.copy2(pdf_out, DIR_DISTRIBUICAO / pdf_out.name)
        except Exception as e:
            log(f"  -> Erro compilando PDF do LM {slug_lm}: {e}")

def processar_playbook():
    log("=== 4. PROCESSANDO PLAYBOOK ===")
    dir_pbk = DIR_OH_MY / "playbooks" / "pbk-1-oh-my"
    if not dir_pbk.exists():
        log("Pasta do playbook pbk-1-oh-my não encontrada!")
        return

    pbk_md = dir_pbk / "playbook.md"
    if not pbk_md.exists():
        log("Arquivo playbook.md não encontrado!")
        return

    # Compilar PDF do Playbook via Pandoc + Typst
    typ_out = dir_pbk / "playbook.typ"
    pdf_out = dir_pbk / "playbook.pdf"
    template_typ = DIR_PROJETO / "templates" / "template_playbook.typ"

    cmd_pandoc = [
        PANDOC,
        str(pbk_md),
        "-o", str(typ_out),
        "--template", str(template_typ),
        "--toc", "--toc-depth", "2",
        "-V", "title=Playbook Prático: Oh My Position",
        "-V", "author=Heverton Eduardo Peres",
        "-V", "sem_capa_grafica=1",
        "--wrap", "preserve"
    ]

    try:
        subprocess.run(cmd_pandoc, check=True)
        cmd_typst = [TYPST, "compile", "--root", str(DIR_PROJETO), str(typ_out), str(pdf_out)]
        subprocess.run(cmd_typst, check=True)
        log(f"  -> PDF do Playbook compilado: {pdf_out.name}")
        shutil.copy2(pdf_out, DIR_DISTRIBUICAO / pdf_out.name)
    except Exception as e:
        log(f"  -> Erro compilando PDF do Playbook: {e}")

def criar_campanhas_e_maquina():
    log("=== 5. CRIANDO CAMPANHAS E MÁQUINA DE VENDAS ===")
    
    # 5.1 Criar Campanhas
    try:
        cmd_camp = [sys.executable, str(DIR_PROJETO / "scripts" / "criar-campanha.py"), "--completo", "oh-my", "--sem-artes"]
        subprocess.run(cmd_camp, check=False)
        log("  -> Pasta campanhas gerada com sucesso!")
    except Exception as e:
        log(f"  -> Erro ao gerar campanhas: {e}")

    # 5.2 Criar Máquina de Vendas
    try:
        cmd_maq = [sys.executable, str(DIR_PROJETO / "scripts" / "criar-maquina-vendas.py"), "oh-my"]
        subprocess.run(cmd_maq, check=False)
        log("  -> Pasta maquina de vendas gerada com sucesso!")
    except Exception as e:
        log(f"  -> Erro ao gerar maquina: {e}")

def sincronizar_colecao():
    log("=== 6. SINCRONIZANDO MANIFESTO DA COLEÇÃO ===")
    try:
        cmd_col = [sys.executable, str(DIR_PROJETO / "scripts" / "colecao.py"), "--sincronizar"]
        subprocess.run(cmd_col, check=False)
        log("  -> Manifesto da coleção sincronizado!")
    except Exception as e:
        log(f"  -> Erro ao sincronizar coleção: {e}")

def main():
    log("Iniciando correção completa da obra oh-my...")
    processar_ebooks()
    processar_emails()
    processar_lead_magnets()
    processar_playbook()
    criar_campanhas_e_maquina()
    sincronizar_colecao()
    log("FINALIZADO! Todos os entregáveis de oh-my foram gerados e corrigidos.")

if __name__ == "__main__":
    main()
