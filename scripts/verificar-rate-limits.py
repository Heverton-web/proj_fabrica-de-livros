#!/usr/bin/env python3
"""
Verifica rate-limit/quota atual em varios provedores de LLM, um por chave de
API configurada em variavel de ambiente. Cada provedor expoe isso de um jeito
diferente (endpoint dedicado, headers de resposta, ou nada via API) — ver
`comandos-cli/comandos-cli.md` para as fontes/documentacao usada por tras de
cada implementacao.

Provedores com endpoint dedicado (dado estruturado):
    OpenRouter, Hugging Face

Provedores sem endpoint dedicado, headers de rate-limit documentados
oficialmente (lidos numa chamada leve tipo GET /v1/models):
    OpenAI, Anthropic, Groq

Provedores compativeis com formato OpenAI mas SEM nomes de header
confirmados oficialmente — best-effort, captura qualquer header cujo nome
contenha "ratelimit":
    Cerebras, NVIDIA, Grok/xAI

Provedores sem API publica de quota/rate-limit (reportados como
indisponiveis, com o link do painel onde checar manualmente):
    Google Gemini (AI Studio), Cloudflare Workers AI, OpenCode Zen

Caso especial (exige uma chave DIFERENTE da chave normal de inferencia):
    ZenMux — precisa de uma Management API Key (console > Management)

Variaveis de ambiente esperadas (todas opcionais — provedor sem a variavel
configurada aparece como "sem chave" no relatorio, nao como erro):
    OPENROUTER_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY, GROQ_API_KEY,
    HF_TOKEN, CEREBRAS_API_KEY, NVIDIA_API_KEY, XAI_API_KEY,
    ZENMUX_MANAGEMENT_API_KEY

Uso:
    python scripts/verificar-rate-limits.py
    python scripts/verificar-rate-limits.py --json
"""

import argparse
import json
import os
import sys

import requests

TIMEOUT = 15


def console_utf8():
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def _headers_ratelimit_genericos(headers) -> dict:
    """Captura qualquer header cujo nome contenha 'ratelimit' — usado quando
    o provedor e compativel com OpenAI mas nao tem nomes de header
    documentados oficialmente (Cerebras, NVIDIA, Grok/xAI)."""
    return {k: v for k, v in headers.items() if "ratelimit" in k.lower()}


def _headers_estilo_openai(headers) -> dict:
    campos = [
        "x-ratelimit-limit-requests", "x-ratelimit-remaining-requests", "x-ratelimit-reset-requests",
        "x-ratelimit-limit-tokens", "x-ratelimit-remaining-tokens", "x-ratelimit-reset-tokens",
    ]
    return {c: headers[c] for c in campos if c in headers}


def _headers_anthropic(headers) -> dict:
    campos = [
        "anthropic-ratelimit-requests-limit", "anthropic-ratelimit-requests-remaining", "anthropic-ratelimit-requests-reset",
        "anthropic-ratelimit-tokens-limit", "anthropic-ratelimit-tokens-remaining", "anthropic-ratelimit-tokens-reset",
        "anthropic-ratelimit-input-tokens-limit", "anthropic-ratelimit-input-tokens-remaining",
        "anthropic-ratelimit-output-tokens-limit", "anthropic-ratelimit-output-tokens-remaining",
        "retry-after",
    ]
    return {c: headers[c] for c in campos if c in headers}


def _get(url, headers) -> requests.Response:
    return requests.get(url, headers=headers, timeout=TIMEOUT)


def checar_openrouter(chave):
    resp = _get("https://openrouter.ai/api/v1/key", {"Authorization": f"Bearer {chave}"})
    resp.raise_for_status()
    dados = resp.json().get("data", {})
    return {
        "limite": dados.get("limit"),
        "restante": dados.get("limit_remaining"),
        "reset": dados.get("limit_reset"),
        "uso_total": dados.get("usage"),
        "uso_diario": dados.get("usage_daily"),
        "free_tier": dados.get("is_free_tier"),
    }


def checar_huggingface(token):
    resp = _get("https://huggingface.co/api/whoami-v2", {"Authorization": f"Bearer {token}"})
    resp.raise_for_status()
    corpo = resp.json()
    return {
        "conta": corpo.get("name"),
        "tipo_plano": corpo.get("type"),
        "RateLimit": resp.headers.get("RateLimit"),
        "RateLimit-Policy": resp.headers.get("RateLimit-Policy"),
    }


def checar_openai(chave):
    resp = _get("https://api.openai.com/v1/models", {"Authorization": f"Bearer {chave}"})
    resp.raise_for_status()
    return _headers_estilo_openai(resp.headers)


def checar_anthropic(chave):
    resp = _get("https://api.anthropic.com/v1/models", {
        "x-api-key": chave, "anthropic-version": "2023-06-01",
    })
    resp.raise_for_status()
    return _headers_anthropic(resp.headers)


def checar_groq(chave):
    resp = _get("https://api.groq.com/openai/v1/models", {"Authorization": f"Bearer {chave}"})
    resp.raise_for_status()
    return _headers_estilo_openai(resp.headers)


def checar_cerebras(chave):
    resp = _get("https://api.cerebras.ai/v1/models", {"Authorization": f"Bearer {chave}"})
    resp.raise_for_status()
    achados = _headers_ratelimit_genericos(resp.headers)
    return achados or {"aviso": "sem headers de rate-limit na resposta (nao documentado oficialmente)"}


def checar_nvidia(chave):
    resp = _get("https://integrate.api.nvidia.com/v1/models", {"Authorization": f"Bearer {chave}"})
    resp.raise_for_status()
    achados = _headers_ratelimit_genericos(resp.headers)
    return achados or {"aviso": "sem headers de rate-limit na resposta (nao documentado oficialmente)"}


def checar_grok(chave):
    resp = _get("https://api.x.ai/v1/models", {"Authorization": f"Bearer {chave}"})
    resp.raise_for_status()
    achados = _headers_ratelimit_genericos(resp.headers)
    return achados or {"aviso": "sem headers de rate-limit na resposta (nao documentado oficialmente)"}


def checar_zenmux(chave_management):
    resp = _get("https://zenmux.ai/api/v1/management/payg/balance",
                {"Authorization": f"Bearer {chave_management}"})
    resp.raise_for_status()
    return resp.json()


# (provedor, env_var, funcao_checagem | None, url_painel_manual | None)
PROVEDORES = [
    ("OpenRouter", "OPENROUTER_API_KEY", checar_openrouter, None),
    ("Hugging Face", "HF_TOKEN", checar_huggingface, None),
    ("OpenAI", "OPENAI_API_KEY", checar_openai, None),
    ("Anthropic", "ANTHROPIC_API_KEY", checar_anthropic, None),
    ("Groq", "GROQ_API_KEY", checar_groq, None),
    ("Cerebras", "CEREBRAS_API_KEY", checar_cerebras, None),
    ("NVIDIA", "NVIDIA_API_KEY", checar_nvidia, None),
    ("Grok (xAI)", "XAI_API_KEY", checar_grok, None),
    ("ZenMux", "ZENMUX_MANAGEMENT_API_KEY", checar_zenmux,
     "https://zenmux.ai/platform/subscription (precisa de Management API Key, nao a chave normal de inferencia)"),
    ("Google Gemini (AI Studio)", None, None,
     "https://aistudio.google.com/ (quota e por PROJETO, nao por chave — sem API publica de consulta)"),
    ("Cloudflare Workers AI", None, None,
     "https://dash.cloudflare.com/ > Workers AI > Usage (API de analytics existe mas nao devolve neurons restantes)"),
    ("OpenCode Zen", None, None,
     "sem API publica de rate-limit/quota documentada (opencode.ai/docs/zen)"),
]


def rodar_verificacoes() -> list:
    resultados = []
    for nome, env_var, funcao, painel_manual in PROVEDORES:
        if funcao is None:
            resultados.append({
                "provedor": nome, "status": "indisponivel_via_api",
                "mensagem": f"Verificar manualmente: {painel_manual}",
            })
            continue

        chave = os.environ.get(env_var)
        if not chave:
            resultados.append({
                "provedor": nome, "status": "sem_chave",
                "mensagem": f"Variavel de ambiente {env_var} nao configurada — pulado.",
            })
            continue

        try:
            dados = funcao(chave)
            resultados.append({"provedor": nome, "status": "ok", "dados": dados})
        except requests.HTTPError as e:
            resultados.append({
                "provedor": nome, "status": "erro",
                "mensagem": f"HTTP {e.response.status_code}: {e.response.text[:200]}",
            })
        except requests.RequestException as e:
            resultados.append({"provedor": nome, "status": "erro", "mensagem": str(e)})

    return resultados


def imprimir_relatorio(resultados):
    for r in resultados:
        print(f"\n=== {r['provedor']} ===")
        if r["status"] == "ok":
            for k, v in r["dados"].items():
                print(f"  {k}: {v}")
        else:
            print(f"  [{r['status']}] {r['mensagem']}")


def main():
    console_utf8()
    parser = argparse.ArgumentParser(description="Verifica rate-limit/quota de varios provedores de LLM")
    parser.add_argument("--json", action="store_true", help="Saida em JSON em vez de texto")
    args = parser.parse_args()

    resultados = rodar_verificacoes()

    if args.json:
        print(json.dumps(resultados, indent=2, ensure_ascii=False))
    else:
        imprimir_relatorio(resultados)


if __name__ == "__main__":
    main()
