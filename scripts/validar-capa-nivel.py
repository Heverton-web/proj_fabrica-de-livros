#!/usr/bin/env python3
"""
Validador deterministico do badge de nivel na capa (gate inegociavel).

Confere que o `capa.html` renderizado por `scripts/gerar-capa.py` contem o
badge de nivel obrigatorio (REGRA 5/Capa, item h) coerente com o campo
`senioridade_obra` de `config_obra.json`.

Uso:
    python scripts/validar-capa-nivel.py livros/<slug>
    python scripts/validar-capa-nivel.py ebooks/<slug>--eb-01-titulo

Exit code: 0 = conforme, 1 = reprovado (badge ausente/incoerente/obra sem o
campo senioridade_obra). Chamado pela cadeia de capa do compilador; qualquer
reprovacao BLOQUEIA a compilacao do PDF.
"""
import json
import re
import sys
from pathlib import Path

ROTULOS = {
    "iniciante": "PARA INICIANTES",
    "intermediario": "NÍVEL INTERMEDIÁRIO",
    "intermediário": "NÍVEL INTERMEDIÁRIO",
    "avancado": "NÍVEL AVANÇADO",
    "avançado": "NÍVEL AVANÇADO",
}


def rotulo_esperado(senioridade):
    return ROTULOS.get((senioridade or "").strip().lower())


def validar_capa_nivel(dir_obra):
    dir_obra = Path(dir_obra)
    config_path = dir_obra / "config_obra.json"
    html_path = dir_obra / "capa.html"
    if not config_path.exists():
        print(f"[REPROVADO] {config_path} nao existe — sem senioridade_obra nao ha capa valida")
        return 1
    config = json.loads(config_path.read_text(encoding="utf-8"))
    senioridade = (config.get("senioridade_obra") or "").strip()
    if not senioridade:
        print("[REPROVADO] config_obra.json sem 'senioridade_obra' — badge de nivel obrigatorio")
        return 1
    rotulo = rotulo_esperado(senioridade)
    if not rotulo:
        print(f"[REPROVADO] senioridade_obra invalida: '{senioridade}' "
              "(esperado iniciante | intermediario | avancado)")
        return 1
    if not html_path.exists():
        print(f"[REPROVADO] {html_path} nao existe — rode scripts/gerar-capa.py primeiro")
        return 1
    html = html_path.read_text(encoding="utf-8")
    m = re.search(r'<div class="badge">([^<]+)</div>', html)
    if not m:
        print(f"[REPROVADO] capa.html sem badge de nivel — esperado: {rotulo}")
        return 1
    badge = m.group(1).strip()
    if badge != rotulo:
        print(f"[REPROVADO] badge '{badge}' divergente do esperado para "
              f"senioridade_obra='{senioridade}': {rotulo}")
        return 1
    print(f"[OK] badge de nivel presente e coerente: {badge}")
    return 0


def main():
    if len(sys.argv) < 2:
        print("uso: python scripts/validar-capa-nivel.py <slug>")
        return 2
    slug = sys.argv[1].strip("/").strip("\\")
    if slug.startswith("output/"):
        slug = slug.replace("output/", "", 1)
    if not slug.startswith(("livros/", "ebooks/")):
        print("[REPROVADO] slug deve apontar para livros/ ou ebooks/")
        return 1
    dir_obra = Path(__file__).resolve().parent.parent / "output" / slug
    return validar_capa_nivel(dir_obra)


if __name__ == "__main__":
    sys.exit(main())
