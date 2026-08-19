#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Roteador Inteligente de LLMs Gratuitas por Tipo de Tarefa.

Detecta o tipo de tarefa pelo prompt, seleciona o melhor provedor gratuito
disponível, e faz fallback automático quando a cota esgota.

Uso:
    python scripts/task_router.py "debug this Python function"
    → export ORCA_PROVIDER=groq ORCA_MODEL=llama-3.3-70b-versatile

    eval $(python scripts/task_router.py "escreva um poema")
    → define ORCA_PROVIDER + ORCA_MODEL no shell

Compatível com qualquer harness (Claude Code, Orca, Aider, Continue, Cursor, etc.)
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime, timezone

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv opcional

# ─── Quota tracker ────────────────────────────────────────────────────────────
QUOTA_DIR = Path.home() / ".task_router"
QUOTA_FILE = QUOTA_DIR / "quota.json"
QUOTA_LOG = QUOTA_DIR / "usage.log"

def _carregar_quota():
    """Carrega estado de quotas do disco."""
    QUOTA_DIR.mkdir(parents=True, exist_ok=True)
    if QUOTA_FILE.exists():
        try:
            return json.loads(QUOTA_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}

def _salvar_quota(estado):
    """Salva estado de quotas no disco."""
    QUOTA_DIR.mkdir(parents=True, exist_ok=True)
    QUOTA_FILE.write_text(json.dumps(estado, indent=2, ensure_ascii=False), encoding="utf-8")

def _registrar_uso(provider):
    """Registra uso de um provedor."""
    estado = _carregar_quota()
    agora = datetime.now(timezone.utc).isoformat()
    if provider not in estado:
        estado[provider] = {"uses": 0, "last": agora}
    estado[provider]["uses"] += 1
    estado[provider]["last"] = agora
    _salvar_quota(estado)

    # Log em texto legível
    QUOTA_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(QUOTA_LOG, "a", encoding="utf-8") as f:
        f.write(f"{agora} | {provider} | use #{estado[provider]['uses']}\n")

def _provider_bloqueado(provider):
    """Verifica se provedor está bloqueado por quota."""
    estado = _carregar_quota()
    info = estado.get(provider, {})
    uses = info.get("uses", 0)
    # Limite diário por provedor (estimativa conservadora)
    LIMITES = {
        "groq": 14400,
        "cerebras": 1000000,
        "google": 1500,
        "openrouter": 50,
        "nvidia": 1000,
        "siliconflow": 1000,
        "huggingface": 1000,
        "cohere": 1000,
        "fireworks": 1000,
        "cloudflare": 10000,
        "mistral": 1000,
        "sambanova": 1000,
        "github": 1000,
    }
    limite = LIMITES.get(provider, 1000)
    return uses >= limite

# ─── Deteção de tarefa ────────────────────────────────────────────────────────

TASK_KEYWORDS = {
    "coding": [
        "code", "debug", "function", "class", "api", "script", "programa",
        "código", "bug", "erro", "refactor", "implement", "test", "pytest",
        "python", "javascript", "typescript", "rust", "go", "java",
        "compilar", "build", "deploy", "git", "commit", "merge", "branch",
        "sql", "query", "database", "endpoint", "route", "middleware",
    ],
    "reasoning": [
        "analyze", "reason", "logic", "solve", "think", "raciocínio",
        "lógica", "resolver", "prova", "dedução", "hipótese", "teorema",
        "explique", "por que", "por que não", "compare", "tradeoff",
        "decisão", "avaliar", "pontos fortes", "pontos fracos",
    ],
    "creative": [
        "write", "create", "story", "poem", "design", "escreva", "crie",
        "história", "poema", "texto", "copy", "landing page", "headline",
        "anúncio", "copywriting", "blog", "artigo", "newsletter",
        "roteiro", "roteirizar", "narrativa", "conto", "crônica",
    ],
    "analysis": [
        "analyze", "summarize", "extract", "compare", "analise", "resuma",
        "extraia", "compare", "relatório", "dashboard", "métrica",
        "kpi", "benchmark", "tendência", "padrão", "estatística",
        "dados", "dataset", "csv", "json", "xml",
    ],
    "chat": [
        "chat", "talk", "conversation", "help", "converse", "ajuda",
        "pergunta", "dúvida", "qual", "como", "onde", "quando",
        "bom dia", "boa tarde", "obrigado", "por favor",
    ],
    "embedding": [
        "embed", "vector", "similarity", "search", "embedding", "vetor",
        "similaridade", "busca semântica", "rag", "retrieval",
        "indexar", "cluster", "semantic", " cosine",
    ],
    "vision": [
        "image", "picture", "visual", "screenshot", "imagem", "print",
        "captura", "foto", "visual", "diagrama", "gráfico", "chart",
        "tela", "ui", "ux", "mockup", "wireframe",
    ],
}

def detectar_tarefa(prompt: str) -> str:
    """Detecta tipo de tarefa baseado em palavras-chave do prompt."""
    prompt_lower = prompt.lower()
    scores = {}
    for task, kws in TASK_KEYWORDS.items():
        scores[task] = sum(1 for kw in kws if kw in prompt_lower)
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "chat"

# ─── Roteamento por provedor ──────────────────────────────────────────────────

TASK_ROUTES = {
    "coding":       ["groq", "cerebras", "google", "openrouter", "nvidia"],
    "reasoning":    ["google", "groq", "nvidia", "openrouter", "cerebras"],
    "creative":     ["openrouter", "google", "groq", "siliconflow", "nvidia"],
    "analysis":     ["google", "groq", "cerebras", "openrouter", "nvidia"],
    "chat":         ["groq", "google", "openrouter", "huggingface", "siliconflow"],
    "embedding":    ["huggingface", "siliconflow", "cohere", "nvidia", "fireworks"],
    "vision":       ["google", "openrouter", "nvidia", "siliconflow", "fireworks"],
}

# Modelos gratuitos por provedor (melhor primeiro)
PROVIDER_MODELS = {
    "groq":          ["llama-3.3-70b-versatile", "mixtral-8x7b-32768", "gemma2-9b-it"],
    "google":        ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.5-flash-8b"],
    "cerebras":      ["llama3.1-70b", "llama3.1-8b"],
    "openrouter":    ["meta-llama/llama-3.3-70b-instruct:free", "google/gemini-2.0-flash-exp:free"],
    "nvidia":        ["nvidia/nemotron-ultra-253b"],
    "siliconflow":   ["Qwen/Qwen2.5-72B-Instruct", "meta-llama/Llama-3.3-70B-Instruct"],
    "huggingface":   ["microsoft/Phi-3.5-mini-instruct", "meta-llama/Llama-3.2-3B-Instruct"],
    "cohere":        ["command-r-plus", "command-r"],
    "fireworks":     ["accounts/fireworks/models/llama-v3p1-70b-instruct"],
    "cloudflare":    ["@cf/meta/llama-3.1-8b-instruct", "@cf/meta/llama-3.1-70b-instruct"],
    "mistral":       ["mistral-large-latest", "mistral-small-latest"],
    "sambanova":     ["Meta-Llama-3.1-70B-Instruct", "Meta-Llama-3.1-8B-Instruct"],
    "github":        ["gpt-4o-mini", "gpt-4o"],
}

# Variáveis de ambiente por provedor
ENV_VARS = {
    "groq":          "GROQ_API_KEY",
    "google":        "GEMINI_API_KEY",
    "cerebras":      "CEREBRAS_API_KEY",
    "openrouter":    "OPENROUTER_API_KEY",
    "nvidia":        "NVIDIA_API_KEY",
    "siliconflow":   "SILICONFLOW_API_KEY",
    "huggingface":   "HF_API_KEY",
    "cohere":        "COHERE_API_KEY",
    "fireworks":     "FIREWORKS_API_KEY",
    "cloudflare":    "CLOUDFLARE_API_TOKEN",
    "mistral":       "MISTRAL_API_KEY",
    "sambanova":     "SAMBANOVA_API_KEY",
    "github":        "GITHUB_TOKEN",
}

def _chave_disponivel(provider: str) -> bool:
    """Verifica se o provedor tem API key configurada E não está bloqueado."""
    env_var = ENV_VARS.get(provider)
    if not env_var:
        return False
    val = os.getenv(env_var, "").strip()
    if not val or len(val) < 5:
        return False
    if _provider_bloqueado(provider):
        return False
    return True

def _melhor_modelo(provider: str) -> str:
    """Retorna melhor modelo gratuito do provedor."""
    modelos = PROVIDER_MODELS.get(provider, [])
    return modelos[0] if modelos else "unknown"

def rotear(prompt: str) -> dict:
    """
    Roteia prompt para melhor provedor/modelo.
    Retorna: {"task": str, "provider": str, "model": str, "fallback": bool}
    """
    tarefa = detectar_tarefa(prompt)
    candidatos = TASK_ROUTES.get(tarefa, TASK_ROUTES["chat"])

    # Procura provedor disponível na ordem de preferência
    for p in candidatos:
        if _chave_disponivel(p):
            _registrar_uso(p)
            return {
                "task": tarefa,
                "provider": p,
                "model": _melhor_modelo(p),
                "fallback": False,
            }

    # Fallback: qualquer provedor configurado (ignora quota)
    for p, env in ENV_VARS.items():
        val = os.getenv(env, "").strip()
        if val and len(val) >= 5:
            _registrar_uso(p)
            return {
                "task": tarefa,
                "provider": p,
                "model": _melhor_modelo(p),
                "fallback": True,
            }

    # Último recurso: openrouter (tem modelo free sem chave)
    return {
        "task": tarefa,
        "provider": "openrouter",
        "model": "meta-llama/llama-3.3-70b-instruct:free",
        "fallback": True,
    }

# ─── Output ───────────────────────────────────────────────────────────────────

def formatar_saida(resultado: dict, fmt: str = "shell") -> str:
    """Formata resultado para diferentes contextos."""
    if fmt == "shell":
        lines = [
            f"export ORCA_PROVIDER={resultado['provider']}",
            f"export ORCA_MODEL={resultado['model']}",
        ]
        return "\n".join(lines)
    elif fmt == "json":
        return json.dumps(resultado, indent=2, ensure_ascii=False)
    elif fmt == "info":
        fb = " (FALLBACK)" if resultado["fallback"] else ""
        return (
            f"Task: {resultado['task']}\n"
            f"Provider: {resultado['provider']}{fb}\n"
            f"Model: {resultado['model']}"
        )
    else:
        return json.dumps(resultado, ensure_ascii=False)

# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(
            "Uso: python scripts/task_router.py \"seu prompt\"\n"
            "\n"
            "Opções:\n"
            "  --json    Saída em JSON\n"
            "  --info    Saída legível (PT-BR)\n"
            "  --shell   Saída em export shell (padrão)\n"
            "  --status  Mostra quotas e provedores ativos\n"
            "  --reset   Reseta quotas de todos os provedores\n"
            "\n"
            "Exemplo:\n"
            "  eval $(python scripts/task_router.py \"debug code\")\n"
            "  python scripts/task_router.py \"escreva um poema\" --json\n"
            "  python scripts/task_router.py --status\n",
            file=sys.stderr
        )
        sys.exit(0)

    # Comandos especiais
    if sys.argv[1] == "--status":
        _cmd_status()
        return
    if sys.argv[1] == "--reset":
        _cmd_reset()
        return

    prompt = " ".join(sys.argv[1:]).strip()

    # Detecta formato de saída
    fmt = "shell"
    if "--json" in sys.argv:
        fmt = "json"
        prompt = prompt.replace("--json", "").strip()
    elif "--info" in sys.argv:
        fmt = "info"
        prompt = prompt.replace("--info", "").strip()
    elif "--shell" in sys.argv:
        fmt = "shell"
        prompt = prompt.replace("--shell", "").strip()

    if not prompt:
        print("Erro: prompt vazio", file=sys.stderr)
        sys.exit(1)

    resultado = rotear(prompt)
    print(formatar_saida(resultado, fmt))

def _cmd_status():
    """Mostra status dos provedores e quotas."""
    print("=" * 60)
    print("  ROTEADOR INTELIGENTE — STATUS DOS PROVEDORES")
    print("=" * 60)

    quota = _carregar_quota()
    total = 0
    for p, env in sorted(ENV_VARS.items()):
        val = os.getenv(env, "").strip()
        ativo = val and len(val) >= 5
        bloqueado = _provider_bloqueado(p) if ativo else False
        uso = quota.get(p, {}).get("uses", 0)

        if ativo:
            if bloqueado:
                status = "🟡 BLOQUEADO"
            else:
                status = "🟢 ATIVO"
            total += 1
        else:
            status = "🔴 INATIVO"

        modelos = PROVIDER_MODELS.get(p, [])
        modelo_str = modelos[0] if modelos else "?"
        print(f"  {status:16s} | {p:14s} | uso: {uso:5d} | modelo: {modelo_str}")

    print("=" * 60)
    print(f"  Total ativos: {total}/{len(ENV_VARS)}")
    print("=" * 60)

def _cmd_reset():
    """Reseta quotas de todos os provedores."""
    QUOTA_DIR.mkdir(parents=True, exist_ok=True)
    QUOTA_FILE.write_text("{}", encoding="utf-8")
    if QUOTA_LOG.exists():
        QUOTA_LOG.unlink()
    print("Quotas resetadas com sucesso.", file=sys.stderr)

if __name__ == "__main__":
    main()
