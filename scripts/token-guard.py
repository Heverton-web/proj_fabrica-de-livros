#!/usr/bin/env python3
"""
Item B (condicional) — melhorias/21-08-2026-plano-acao-tokens-sob-pericia.md.

Cross-check de gasto: compara o auto-relato de custo em
`.agents/session-cost.jsonl` (skill `calcular-gastos-sessao`) contra a fonte
independente `ccusage` (Capítulo 6 do livro "Tokens Sob Perícia"), que lê o
histórico REAL gravado localmente pelo Claude Code.

Pré-requisito confirmado em 21-08-2026 nesta máquina: `npx ccusage@latest
--version` funciona e `npx ccusage@latest daily --json` de fato reporta
`agent: "claude"` com custo real do dia — por isso este script foi
implementado (o plano determinava ficar em NÃO_VERIFICÁVEL se qualquer um
dos dois falhasse).

Este script é ADITIVO/BEST-EFFORT, nunca um gate bloqueante: a fábrica não
tem "fallback para modelo local" (R6 usa `model: inherit`, sem multi-provider
para desviar tráfego), então não há circuit breaker de verdade para abrir —
só um alerta de divergência entre o que foi auto-relatado e o que o ccusage
mede de fato, para o operador decidir.

Uso:
    python scripts/token-guard.py                       # hoje, cross-check completo
    python scripts/token-guard.py --data 2026-08-20      # dia especifico
    python scripts/token-guard.py --json
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from tipos_obra import console_utf8

DIR_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_AUTORRELATO = DIR_PROJETO / ".agents" / "session-cost.jsonl"
LIMIAR_DIVERGENCIA = 0.20  # 20%: acima disso, sinaliza — nunca bloqueia


def _data_hoje():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def custo_ccusage_do_dia(data=None, timeout_segundos=30):
    """Consulta `npx ccusage@latest daily --json` para o dia informado.

    Retorna (custo_usd, erro). custo_usd e None quando a consulta falhou
    (ccusage ausente, sem rede, sem historico) — NUNCA levanta excecao: e
    cross-check best-effort, nao pode derrubar o fechamento de sessao.
    """
    data = data or _data_hoje()
    sem_hifen = data.replace("-", "")
    comando = ["npx", "ccusage@latest", "daily", "--json",
               "--since", sem_hifen, "--until", sem_hifen]
    try:
        resultado = subprocess.run(
            comando, capture_output=True, text=True,
            timeout=timeout_segundos, shell=(sys.platform == "win32"))
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return None, f"ccusage indisponivel: {exc}"

    if resultado.returncode != 0:
        return None, f"ccusage retornou erro: {resultado.stderr.strip()[:200]}"

    try:
        dados = json.loads(resultado.stdout)
    except json.JSONDecodeError as exc:
        return None, f"saida do ccusage nao e JSON valido: {exc}"

    dias = dados.get("daily") or []
    if not dias:
        return 0.0, None  # sem uso registrado no dia — nao e erro
    total = sum(d.get("totalCost", 0.0) for d in dias if d.get("period") == data)
    return total, None


def custo_autorrelato_do_dia(data=None, caminho=CAMINHO_AUTORRELATO):
    """Soma o campo 'cost' de .agents/session-cost.jsonl para o dia informado.

    Retorna (custo_usd, n_linhas). Arquivo ausente (clone novo, nenhuma acao
    registrada ainda) devolve (0.0, 0) — nao e erro.
    """
    data = data or _data_hoje()
    if not caminho.exists():
        return 0.0, 0

    total, n = 0.0, 0
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha:
            continue
        try:
            registro = json.loads(linha)
        except json.JSONDecodeError:
            continue
        if str(registro.get("ts", "")).startswith(data):
            total += float(registro.get("cost", 0) or 0)
            n += 1
    return total, n


def comparar(data=None, limiar=LIMIAR_DIVERGENCIA):
    """Cross-check completo: {data, ccusage, autorrelato, diverge, motivo}."""
    data = data or _data_hoje()
    custo_real, erro = custo_ccusage_do_dia(data)
    custo_relatado, n_acoes = custo_autorrelato_do_dia(data)

    if custo_real is None:
        return {
            "data": data, "ccusage_usd": None, "autorrelato_usd": custo_relatado,
            "acoes_autorrelatadas": n_acoes, "diverge": None,
            "motivo": erro or "ccusage indisponivel — cross-check NAO_VERIFICAVEL",
        }

    base = max(custo_real, 0.01)  # evita divisao por zero em dia sem gasto real
    divergencia_relativa = abs(custo_real - custo_relatado) / base
    diverge = divergencia_relativa > limiar

    return {
        "data": data,
        "ccusage_usd": round(custo_real, 4),
        "autorrelato_usd": round(custo_relatado, 4),
        "acoes_autorrelatadas": n_acoes,
        "divergencia_relativa": round(divergencia_relativa, 3),
        "diverge": diverge,
        "motivo": (
            f"auto-relato diverge {divergencia_relativa:.0%} do ccusage "
            f"(limiar {limiar:.0%}) — .agents/session-cost.jsonl pode estar "
            f"desatualizado" if diverge else None
        ),
    }


def main():
    ap = argparse.ArgumentParser(
        description="Cross-check de gasto: auto-relato vs ccusage (best-effort, nao bloqueante)")
    ap.add_argument("--data", help="dia a comparar, formato YYYY-MM-DD (default: hoje)")
    ap.add_argument("--json", action="store_true", help="imprime o resultado em JSON")
    args = ap.parse_args()

    resultado = comparar(args.data)

    if args.json:
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
        return 0

    print(f"Cross-check de gasto - {resultado['data']}")
    if resultado["ccusage_usd"] is None:
        print(f"  [NAO_VERIFICAVEL] {resultado['motivo']}")
        print(f"  autorrelato (.agents/session-cost.jsonl): "
              f"${resultado['autorrelato_usd']:.4f} ({resultado['acoes_autorrelatadas']} acoes)")
        return 0

    print(f"  ccusage (fonte real)     : ${resultado['ccusage_usd']:.4f}")
    print(f"  autorrelato (session log): ${resultado['autorrelato_usd']:.4f} "
          f"({resultado['acoes_autorrelatadas']} acoes)")
    if resultado["diverge"]:
        print(f"  [AVISO] {resultado['motivo']}")
    else:
        print(f"  [OK] divergencia {resultado['divergencia_relativa']:.0%} dentro do limiar")
    return 0


if __name__ == "__main__":
    console_utf8()
    sys.exit(main())
