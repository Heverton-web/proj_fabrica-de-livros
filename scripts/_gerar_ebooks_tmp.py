#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Adapta capitulos-fonte do livro para ebooks (tom comercial-leve)."""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path("output/ai-driven-development")
LIVRO = BASE / "livros" / "ai-driven-development"
CAPS = {}
for c in sorted((LIVRO / "capitulos").glob("cap_*.md"),
                key=lambda p: int(re.search(r"cap_(\d+)", p.stem).group(1))):
    n = re.search(r"cap_(\d+)", c.stem).group(1)
    CAPS[n] = c.read_text(encoding="utf-8")

# slug_dir -> (caps, titulo)
EBOOKS = [
    ("ai-driven-development--eb-01-o-que-e-ai-driven-development-e-o-que-na",
     ["1", "2"], "O que é AI Driven Development"),
    ("ai-driven-development--eb-02-configurando-o-canteiro-ambiente-e-ferra",
     ["3", "4"], "Configurando o canteiro: ambiente e ferramentas"),
    ("ai-driven-development--eb-03-engenharia-de-prompt-aplicada-ao-codigo",
     ["5", "6"], "Engenharia de prompt aplicada ao código"),
    ("ai-driven-development--eb-04-testes-a-rede-de-seguranca-da-obra-depur",
     ["7", "8"], "Testes e depuração: a rede de segurança da obra"),
    ("ai-driven-development--eb-05-planejando-o-projeto-real-requisitos-e-a",
     ["9", "10"], "Planejando o projeto real: requisitos e arquitetura"),
    ("ai-driven-development--eb-06-erguendo-as-funcionalidades-o-dia-a-dia",
     ["11", "12"], "Erguendo as funcionalidades: do dia a dia ao deploy"),
    ("ai-driven-development--eb-07-agentes-de-codigo-autonomos-conectando-a",
     ["13", "14"], "Agentes autônomos e MCP: a IA conectada ao mundo"),
    ("ai-driven-development--eb-08-seguranca-e-riscos-nao-confie-no-guindas",
     ["15", "16"], "Segurança, riscos e escala: liderando com IA"),
]

def adaptar(num, texto, titulo_cap):
    """Converte capitulo EITA para formato ebook (tom leve)."""
    corpo = re.sub(r"^---\n.*?\n---\n", "", texto, flags=re.DOTALL)
    # remove secao 7 (referencias ABNT)
    corpo = re.sub(r"^## 7\. Referências Bibliográficas.*$", "", corpo, flags=re.DOTALL | re.MULTILINE)
    # titulo: promove para nivel 1 com numero do capitulo do ebook
    corpo = re.sub(r"^# .*$", f"# {titulo_cap}", corpo, count=1, flags=re.MULTILINE)
    # secoes EITA viram subtitulos amigaveis
    mapa = {
        "1. Introdução": f"{num}.1 Para começar",
        "2. Explica": f"{num}.2 O que você precisa entender",
        "3. Ilustra": f"{num}.3 Na prática, como funciona",
        "4. Técnica": f"{num}.4 Mãos na massa",
        "5. Aplica": f"{num}.5 Aplicando no seu projeto",
        "6. Conclusão": f"{num}.6 Resumo do capítulo",
    }
    for velho, novo in mapa.items():
        corpo = re.sub(rf"^##\s*{re.escape(velho)}", f"## {novo}", corpo, flags=re.MULTILINE)
    # remove citacoes numeradas [N]
    corpo = re.sub(r"\[\d+(?:\s*,\s*\d+)*(?:\s*-\s*\d+)?\]", "", corpo)
    # paragrafos ja sao curtos no livro; garante quebra apos blocos de codigo
    return corpo.strip()


for slug_dir, caps_fonte, titulo in EBOOKS:
    dir_eb = BASE / "ebooks" / slug_dir
    caps_dir = dir_eb / "capitulos"
    caps_dir.mkdir(exist_ok=True)
    sumario = json.loads((dir_eb / "sumario_macro.json").read_text(encoding="utf-8"))

    partes = []
    for i, n in enumerate(caps_fonte, 1):
        texto = CAPS.get(n, "")
        titulo_cap = "Parte " + str(i)
        # tenta pegar titulo real do capitulo do livro
        m = re.match(r"^#\s+(.+)$", texto, re.MULTILINE)
        if m:
            titulo_cap = m.group(1).strip()
        partes.append(adaptar(i, texto, titulo_cap))

    conteudo = "\n\n".join(partes)

    # CTA final
    conteudo += (
        "\n\n---\n\n"
        "# O próximo passo\n\n"
        "Você acabou de percorrer o essencial de **" + titulo +
        "**. Se este conteúdo acelerou o seu aprendizado, imagine o livro completo: "
        "**AI Driven Development: Do Zero ao Avançado — Tudo o que Ninguém Ensina de "
        "Graça, com Projeto Real** traz a teoria por trás de cada passo, os exemplos "
        "comentados, os diagramas e as referências completas — e um projeto real "
        "construído do zero, do requisito ao deploy.\n\n"
        "[Conhecer a obra completa](https://exemplo.com/ai-driven-development?utm_source=ebook&utm_medium=pdf&utm_campaign=ai-driven-development)\n"
    )

    # grava 1 arquivo por capitulo-fonte (para o auditor contar >=2 secoes) + md final
    for i, n in enumerate(caps_fonte, 1):
        texto = CAPS.get(n, "")
        titulo_cap = (re.match(r"^#\s+(.+)$", texto, re.MULTILINE) or [None, "Parte " + str(i)])
        t = titulo_cap.group(1).strip() if hasattr(titulo_cap, "group") else titulo_cap
        (caps_dir / f"cap_{i}.md").write_text(adaptar(i, texto, t), encoding="utf-8")
    (dir_eb / "ebook.md").write_text(conteudo, encoding="utf-8")
    print(f"{slug_dir[:30]}: {len(conteudo):,} chars ({len(partes)} partes)")
print("DONE")
