#!/usr/bin/env python3
"""
Compila artigo científico para PDF via Pandoc -> .typ -> Typst.

Uso:
    python scripts/compilar-artigo.py <slug_artigo>

Exemplo:
    python scripts/compilar-artigo.py oh-my-pi--art-01-o-que-e-um-coding-agent-e-por-que-voce-p
"""

import json
import subprocess
import sys
from pathlib import Path

# Adicionar diretório de scripts ao path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from pdf_typst import executar


def compilar_artigo(slug_artigo: str) -> bool:
    """Compila um artigo para PDF.

    V5.1: procura em output/<colecao>/artigos/ e output/artigos/."""
    # Tentar primeiro no hub por colecao
    dir_artigo = None
    for hub in Path("output").iterdir():
        if hub.is_dir() and hub.name not in ("artigos", "ebooks", "livros", "tccs"):
            candidato = hub / "artigos" / slug_artigo
            if candidato.exists():
                dir_artigo = candidato
                break
    # Fallback para layout plano
    if dir_artigo is None:
        dir_artigo = Path("output") / "artigos" / slug_artigo
    dir_capitulos = dir_artigo / "capitulos"
    metadados_path = dir_artigo / "artigo_metadados.json"
    
    # Verificar se diretório existe
    if not dir_artigo.exists():
        print(f"ERRO: Diretório não encontrado: {dir_artigo}")
        return False
    
    # Ler metadados
    if not metadados_path.exists():
        print(f"ERRO: artigo_metadados.json não encontrado em {dir_artigo}")
        return False
    
    with open(metadados_path, "r", encoding="utf-8") as f:
        metadados = json.load(f)
    
    # Ler seções do artigo
    secoes = []
    for i in range(1, 5):
        cap_path = dir_capitulos / f"cap_{i}.md"
        if cap_path.exists():
            with open(cap_path, "r", encoding="utf-8") as f:
                secoes.append(f.read())
        else:
            print(f"AVISO: Seção {i} não encontrada: {cap_path}")
    
    if not secoes:
        print(f"ERRO: Nenhuma seção encontrada em {dir_capitulos}")
        return False
    
    # Merge das seções
    conteudo = "\n\n".join(secoes)
    
    # Remover cabeçalhos duplicados de seções
    # O template já adiciona o título do artigo
    linhas = conteudo.split("\n")
    linhas_filtradas = []
    for linha in linhas:
        # Pular linhas que são apenas "# 1 Introdução", "# 2 Metodologia", etc.
        if linha.startswith("# ") and any(secao in linha for secao in ["Introdução", "Metodologia", "Resultados", "Conclusão", "Referências"]):
            continue
        linhas_filtradas.append(linha)
    
    conteudo_final = "\n".join(linhas_filtradas)
    
    # Salvar markdown final
    md_final = dir_artigo / "livro_final.md"
    with open(md_final, "w", encoding="utf-8") as f:
        f.write(conteudo_final)
    
    print(f"Markdown final salvo em: {md_final}")
    
    # Preparar metadados para o template
    title = metadados.get("title", slug_artigo.replace("--", ": ").replace("-", " ").title())
    author = metadados.get("author", "Autor não especificado")
    resumo = metadados.get("resumo", "")
    palavras_chave = metadados.get("palavras_chave", [])
    abstract_en = metadados.get("abstract_en", "")
    keywords_en = metadados.get("keywords_en", [])
    
    # Converter listas para string
    if isinstance(palavras_chave, list):
        palavras_chave = ", ".join(palavras_chave)
    if isinstance(keywords_en, list):
        keywords_en = ", ".join(keywords_en)
    
    # Criar arquivo .meta para pandoc
    meta_content = f"""---
title: "{title}"
author: "{author}"
resumo: "{resumo}"
palavras_chave: "{palavras_chave}"
abstract_en: "{abstract_en}"
keywords_en: "{keywords_en}"
---
"""
    
    md_com_meta = dir_artigo / "_artigo_meta.md"
    with open(md_com_meta, "w", encoding="utf-8") as f:
        f.write(meta_content + "\n" + conteudo_final)
    
    # Caminho do template
    template_path = Path("templates") / "template_artigo.typ"
    if not template_path.exists():
        print(f"ERRO: Template não encontrado: {template_path}")
        return False
    
    # Caminho do PDF de saída
    pdf_path = dir_artigo / f"{slug_artigo}.pdf"
    
    # Comando pandoc
    cmd = [
        "pandoc",
        str(md_com_meta),
        "--template", str(template_path),
        "-o", str(pdf_path),
        "--pdf-engine", "typst",
        "-V", f"paleta=indigo",
    ]
    
    print(f"Compilando PDF: {pdf_path}")
    print(f"Comando: {' '.join(cmd)}")
    
    # Executar compilação
    resultado = executar(
        cmd,
        pdf_path,
        dir_artigo,
        "typst",
        timeout=600
    )
    
    if resultado.returncode != 0:
        print(f"ERRO na compilação:")
        print(f"  stdout: {resultado.stdout}")
        print(f"  stderr: {resultado.stderr}")
        return False
    
    if pdf_path.exists():
        tamanho_kb = pdf_path.stat().st_size / 1024
        print(f"PDF gerado com sucesso: {pdf_path} ({tamanho_kb:.1f} KB)")
        return True
    else:
        print(f"ERRO: PDF não foi gerado")
        return False


def main():
    if len(sys.argv) < 2:
        print("Uso: python scripts/compilar-artigo.py <slug_artigo>")
        print("Exemplo: python scripts/compilar-artigo.py oh-my-pi--art-01-o-que-e-um-coding-agent-e-por-que-voce-p")
        sys.exit(1)
    
    slug_artigo = sys.argv[1]
    
    # Listar artigos se solicitado
    if slug_artigo == "--listar":
        dir_artigos = Path("output") / "artigos"
        if dir_artigos.exists():
            for d in dir_artigos.iterdir():
                if d.is_dir() and "oh-my-pi" in d.name:
                    print(d.name)
        return
    
    sucesso = compilar_artigo(slug_artigo)
    sys.exit(0 if sucesso else 1)


if __name__ == "__main__":
    main()