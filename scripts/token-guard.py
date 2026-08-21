#!/usr/bin/env python3
"""
Token Guard — Circuit breaker de gasto (cross-check com ccusage).

Mede gasto real via `npx ccusage@latest daily` como camada de auditoria
independente do auto-relato em `.agents/session-cost.jsonl`.

NÃO é um bloqueador rígido: é ferramenta de observabilidade. Se ccusage
falhar ou divergir, relatório sinaliza; não interrompe o fluxo.

Uso:
    python scripts/token-guard.py --data 2026-08-21
    python scripts/token-guard.py --data today
    python scripts/token-guard.py                    # default: hoje
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_AGENTS = DIR_PROJETO / ".agents"


def custo_ccusage(data_str="today"):
    """Consulta ccusage para o dia e retorna total_cost ou None se falhar."""
    if data_str == "today":
        data_str = datetime.now().strftime("%Y-%m-%d")

    try:
        r = subprocess.run(
            ["npx", "ccusage@latest", "daily", "--json", "--since", data_str, "--until", data_str],
            capture_output=True,
            text=True,
            timeout=30
        )
        if r.returncode != 0:
            return None, f"ccusage saída: {r.stderr}"

        dados = json.loads(r.stdout)
        custo_total = dados.get("totalCost", 0)
        return custo_total, None
    except FileNotFoundError:
        return None, "ccusage não encontrado (npm não instalado?)"
    except json.JSONDecodeError:
        return None, "ccusage retornou JSON inválido"
    except subprocess.TimeoutExpired:
        return None, "ccusage timeout (>30s)"
    except Exception as e:
        return None, f"erro: {e}"


def custo_auto_relato(data_str):
    """Soma tokens do session-cost.jsonl para o dia (estimativa de custo)."""
    session_cost = DIR_AGENTS / "session-cost.jsonl"
    if not session_cost.exists():
        return 0, "session-cost.jsonl não encontrado"

    total = 0
    try:
        with open(session_cost, "r", encoding="utf-8") as f:
            for linha in f:
                if not linha.strip():
                    continue
                try:
                    evento = json.loads(linha)
                    ts = evento.get("timestamp", "")
                    if ts.startswith(data_str):
                        # Estimar custo: (input_tokens * 0.003 + output_tokens * 0.015) / 1000 USD
                        # Padrão Anthropic para modelos 3.5
                        inp = evento.get("tokens_in", 0)
                        out = evento.get("tokens_out", 0)
                        custo = (inp * 0.003 + out * 0.015) / 1_000_000
                        total += custo
                except json.JSONDecodeError:
                    pass
    except Exception as e:
        return 0, f"erro ao ler session-cost: {e}"

    return total, None


def main():
    ap = argparse.ArgumentParser(
        description="Token Guard: cross-check de gasto ccusage vs auto-relato")
    ap.add_argument("--data", default="today", help="data no formato YYYY-MM-DD ou 'today'")
    ap.add_argument("--json", action="store_true", help="saída em JSON")
    args = ap.parse_args()

    custo_cc, erro_cc = custo_ccusage(args.data)
    custo_auto, erro_auto = custo_auto_relato(args.data)

    resultado = {
        "data": args.data if args.data != "today" else datetime.now().strftime("%Y-%m-%d"),
        "ccusage": {"custo": custo_cc, "erro": erro_cc},
        "auto_relato": {"custo": custo_auto, "erro": erro_auto},
        "status": "OK"
    }

    if custo_cc is not None:
        # Calcular divergência (% de diferença)
        base = max(custo_cc, custo_auto, 0.001)  # Evitar divisão por zero
        divergencia = abs(custo_cc - custo_auto) / base
        resultado["divergencia_pct"] = round(divergencia * 100, 1)

        if divergencia > 0.2:  # >20%
            resultado["status"] = "DIVERGENCIA"
            resultado["alerta"] = f"Divergência >20%: ccusage ${custo_cc:.4f} vs auto ${custo_auto:.4f}"
    else:
        resultado["status"] = "CCUSAGE_INDISPONIVEL"

    if args.json:
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    else:
        print(f"[{resultado['status']}] Gasto {resultado['data']}")
        if custo_cc is not None:
            print(f"  ccusage: ${custo_cc:.4f}")
            print(f"  auto-relato: ${custo_auto:.4f}")
            if "alerta" in resultado:
                print(f"  ⚠️  {resultado['alerta']}")
        else:
            print(f"  ⚠️  {erro_cc}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
