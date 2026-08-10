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

V5 (HUB POR COLECAO): o caminho real e resolvido por tipos_obra.dir_obra, que
aceita tanto o layout plano (output/livros/x) quanto o hub
(output/<colecao>/livros/x) e os slugs curtos de nomes-curtos V5.1.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tipos_obra as TO  # noqa: E402

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
    # Aceita o padrao atual do template (badge-main, com prefixo decorativo
    # "◆ &nbsp;") e o legado (class="badge")
    m = re.search(r'<div class="badge(?:-main)?">([^<]+)</div>', html)
    if not m:
        print(f"[REPROVADO] capa.html sem badge de nivel — esperado: {rotulo}")
        return 1
    badge = re.sub(r"^[^A-ZÀ-Ý]*", "", m.group(1)).strip()
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
    if slug.startswith(("output/", "output\\")):
        slug = slug.split("/", 1)[-1].split("\\", 1)[-1]
    tipo = TO.tipo_por_prefixo(slug)
    dir_obra = TO.dir_obra(slug)
    if not dir_obra.exists():
        print(f"[REPROVADO] obra nao encontrada: {slug} (resolvido: {dir_obra})")
        return 1
    if tipo not in ("livro", "ebook"):
        print("[REPROVADO] slug deve apontar para livros/ ou ebooks/ "
              "(badge de nivel obrigatorio so em Livro/E-book, REGRA 5)")
        return 1
    return validar_capa_nivel(dir_obra)


if __name__ == "__main__":
    sys.exit(main())
