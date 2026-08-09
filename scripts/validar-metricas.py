#!/usr/bin/env python3
"""
F1 — Gate de MENSURABILIDADE (R-MT-1 a R-MT-3).

Todo capítulo precisa carregar ao menos uma métrica concreta (número + unidade)
e, quando o sumário macro declara métricas obrigatórias, o texto do capítulo
deve reproduzir o valor E citar a fonte ([N]) no mesmo parágrafo. Impede o modo
de falha de livros cheios de prosa e vazios de dados.

R-MT-1: todo capítulo tem >= 1 métrica (número + unidade) fora de código.
R-MT-2: métrica declarada em metricas_obrigatorias aparece no capítulo.
R-MT-3: métrica declarada tem citação [N] no mesmo parágrafo (fonte adjacente).

Declaração (opcional) no sumario_macro.json:
    "metricas_obrigatorias": {
      "1": [{"metrica": "latencia p95", "valor": "200 ms"}],
      "7": [{"metrica": "custo por token", "valor": "R$ 0,002"}]
    }
Sem declaração, o gate roda em modo heurístico (só R-MT-1).

Uso:
    python scripts/validar-metricas.py <slug>
    python scripts/validar-metricas.py <slug> --capitulo 7
    python scripts/validar-metricas.py <slug> --md docs/x.md
    python scripts/validar-metricas.py <slug> --estrito   # exit 1 se falha
    python scripts/validar-metricas.py <slug> --json

Relatório: output/<slug>/validacao/relatorio_metricas.json
"""

import argparse
import json
import re
import sys
from pathlib import Path

from secoes_eita import dividir_secoes, sem_codigo

import tipos_obra as TO
from tipos_obra import console_utf8

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

# Número (inteiro ou decimal, vírgula ou ponto) + unidade conhecida.
RE_METRICA = re.compile(
    r"\b\d+(?:[.,]\d+)?\s*"
    r"(?:%|ms|s|min|h|dias?|horas?|segundos?|GB|MB|KB|TB|GHz|MHz|Hz|"
    r"rps|qps|req/s|tps|ops|tokens?|reqs?|vezes|×|x\b|R\$\s?\d+|\$\s?\d+|"
    r"de usuários?|usuários?|clientes?|empresas?|países?|"
    r"pontos?|passos?|etapas?|camadas?|agentes?|modelos?|"
    r"milh[õo]es?|bilh[õo]es?|trilh[õo]es?)",
    re.IGNORECASE,
)
RE_CITACAO = re.compile(r"\[(?:\d+(?:\s*,\s*\d+)*|\d+\s*-\s*\d+)\]")

REGRAS = {
    "R-MT-1": "todo capítulo tem ao menos 1 métrica (número + unidade)",
    "R-MT-2": "métrica declarada em metricas_obrigatorias aparece no capítulo",
    "R-MT-3": "métrica declarada tem citação [N] no mesmo parágrafo",
}


def _ler_json(caminho, padrao=None):
    if caminho.exists():
        try:
            return json.loads(caminho.read_text(encoding="utf-8"))
        except ValueError:
            return padrao if padrao is not None else {}
    return padrao if padrao is not None else {}


def metricas_no_texto(texto):
    """Número de métricas distintas encontradas fora de blocos de código."""
    limpo = sem_codigo(texto or "")
    return len(RE_METRICA.findall(limpo))


def _paragrafos(texto):
    return [p.strip() for p in re.split(r"\n\s*\n", texto or "") if p.strip()]


def _valor_normalizado(valor):
    """'200 ms' e '200ms' são o mesmo valor para fins de busca."""
    return re.sub(r"\s+", " ", (valor or "").strip().lower())


def _encontrar_paragrafo_do_valor(texto, valor):
    alvo = _valor_normalizado(valor)
    texto_limpo = sem_codigo(texto or "")
    for p in _paragrafos(texto_limpo):
        if alvo and alvo in _valor_normalizado(p):
            return p
    return None


def validar_capitulo(texto, numero, metricas_declaradas):
    corpo = sem_codigo(texto)
    violacoes = []

    # R-MT-1 — heurística: ao menos uma métrica no corpo.
    if not RE_METRICA.search(corpo):
        violacoes.append({
            "regra": "R-MT-1", "enunciado": REGRAS["R-MT-1"],
            "detalhe": "nenhuma métrica (número + unidade) encontrada no capítulo"})

    # R-MT-2 / R-MT-3 — exigências declaradas no sumário macro.
    for decl in metricas_declaradas or []:
        valor = decl.get("valor")
        metrica = decl.get("metrica", "")
        if valor is not None:
            paragrafo = _encontrar_paragrafo_do_valor(texto, valor)
            if paragrafo is None:
                violacoes.append({
                    "regra": "R-MT-2", "enunciado": REGRAS["R-MT-2"],
                    "detalhe": f"valor '{valor}' ({metrica}) não aparece no capítulo"})
            elif not RE_CITACAO.search(paragrafo):
                violacoes.append({
                    "regra": "R-MT-3", "enunciado": REGRAS["R-MT-3"],
                    "detalhe": f"'{valor}' ({metrica}) sem citação [N] no parágrafo"})
        else:
            # Declarou só a métrica (nome), sem valor: exige o nome no texto.
            nome = _valor_normalizado(metrica)
            if nome and nome not in _valor_normalizado(corpo):
                violacoes.append({
                    "regra": "R-MT-2", "enunciado": REGRAS["R-MT-2"],
                    "detalhe": f"métrica '{metrica}' não aparece no capítulo"})

    return violacoes


def metricas_do_sumario(sumario, numero):
    """Metricas obrigatorias declaradas para o capitulo N (dict -> lista)."""
    bloco = (sumario or {}).get("metricas_obrigatorias") or {}
    for chave in (str(numero), numero):
        if chave in bloco:
            valor = bloco[chave]
            return valor if isinstance(valor, list) else [valor]
    return []


def main():
    ap = argparse.ArgumentParser(
        description="Gate F1 de mensurabilidade: métricas com valor, unidade e citação")
    ap.add_argument("slug")
    ap.add_argument("--capitulo", help="valida apenas o capitulo N")
    ap.add_argument("--md", help="valida um markdown especifico em vez dos capitulos")
    ap.add_argument("--estrito", action="store_true", help="exit 1 se houver falha")
    ap.add_argument("--json", action="store_true", help="imprime relatorio JSON completo")
    args = ap.parse_args()

    dir_livro = TO.dir_obra(args.slug, DIR_OUTPUT)
    if not dir_livro.exists():
        print(f"[ERRO] Obra nao encontrada: {dir_livro}")
        return 1
    sumario = _ler_json(dir_livro / "sumario_macro.json")

    alvos = []
    if args.md:
        p = Path(args.md)
        if not p.exists():
            print(f"[ERRO] Arquivo nao encontrado: {p}")
            return 1
        alvos.append((p, p.name, None))
    else:
        caps = sorted((dir_livro / "capitulos").glob("cap_*.md"),
                      key=lambda p: int(re.search(r"cap_(\d+)", p.stem).group(1)))
        if args.capitulo:
            caps = [c for c in caps
                    if re.search(r"cap_(\d+)", c.stem).group(1).lstrip("0")
                    == str(args.capitulo).lstrip("0")]
        if not caps:
            print(f"[ERRO] Nenhum capitulo encontrado em {dir_livro / 'capitulos'}")
            return 1
        alvos = [(c, c.stem,
                  int(re.search(r"cap_(\d+)", c.stem).group(1))) for c in caps]

    todos = []
    for caminho, rotulo, numero in alvos:
        texto = caminho.read_text(encoding="utf-8", errors="replace")
        declaradas = metricas_do_sumario(sumario, numero) if numero else []
        violacoes = validar_capitulo(texto, numero, declaradas)
        for v in violacoes:
            v["origem"] = rotulo
        todos.extend(violacoes)

    # Conta também métricas por capítulo (info para o relatório).
    metricas_por_capitulo = {}
    for caminho, rotulo, numero in alvos:
        texto = caminho.read_text(encoding="utf-8", errors="replace")
        metricas_por_capitulo[rotulo] = metricas_no_texto(texto)

    relatorio = {
        "slug": args.slug,
        "capitulos": len(alvos),
        "metricas_por_capitulo": metricas_por_capitulo,
        "total_violacoes": len(todos),
        "regras": REGRAS,
        "violacoes": todos,
    }
    dir_val = dir_livro / "validacao"
    dir_val.mkdir(exist_ok=True)
    (dir_val / "relatorio_metricas.json").write_text(
        json.dumps(relatorio, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Gate de Mensurabilidade - {args.slug}")
    print(f"  capitulos analisados : {len(alvos)}")
    print(f"  metricas por capitulo:")
    for rotulo, n in metricas_por_capitulo.items():
        print(f"    {rotulo:<12}: {n}")
    print(f"  violacoes            : {len(todos)}")

    if todos:
        print("\n[FALHA] Violações:")
        for v in todos[:20]:
            print(f"  - {v.get('origem')}: {v['regra']} — {v['detalhe']}")
        if len(todos) > 20:
            print(f"  ... e mais {len(todos) - 20}")
    else:
        print("\n[OK] Todos os capítulos mensuráveis conforme o gate")

    print(f"\nRelatorio: {(dir_val / 'relatorio_metricas.json').relative_to(DIR_PROJETO)}")

    if args.json:
        print(json.dumps(relatorio, ensure_ascii=False, indent=2))

    if args.estrito and todos:
        return 1
    return 0


if __name__ == "__main__":
    console_utf8()
    sys.exit(main())
