#!/usr/bin/env python3
"""Detecta harness atual e lista LLMs disponíveis."""
import json, os, sys

HARNESS_SIGNATURES = {
    "mimocode": [".mimocode", "mimocode.json"],
    "claude_code": [".claude", "CLAUDE.md"],
    "antigravity": [".antigravity", "antigravity.json"],
    "opencode": [".opencode", "opencode.json"],
    "freebuff": [".freebuff", "freebuff.json"],
    "omp": [".omp", "omp.json", ".ohmypi"],
    "gemini_cli": [".gemini", "gemini.json", ".gemini-cli"],
    "grok": [".grok", "grok.json", ".xai"],
    "kiro": [".kiro", "kiro.json"],
}

TIER_MAP = {
    "lite": [
        "claude-haiku", "claude-3-5-haiku",
        "mimo-v2.5-lite", "mimo-lite",
        "gpt-4o-mini", "gpt-3.5-turbo",
        "gemini-flash", "gemini-2.0-flash", "gemini-2.5-flash",
        "grok-2-mini",
        "amazon-titan-lite",
        "mistral-small", "llama-3-8b",
    ],
    "standard": [
        "claude-sonnet", "claude-sonnet-4", "claude-3-5-sonnet",
        "mimo-v2.5", "mimo-v2.5-standard",
        "gpt-4o", "gpt-4-turbo",
        "gemini-pro", "gemini-2.5-pro",
        "grok-2", "grok-3",
        "claude-sonnet-v2",
        "mistral-large", "llama-3-70b",
    ],
    "pro": [
        "claude-opus", "claude-opus-4",
        "mimo-v2.5-pro",
        "gpt-4", "o1", "o3",
        "gemini-ultra", "gemini-2.5-pro-deep-think",
        "grok-3-heavy",
        "claude-opus-v2",
        "deepseek-r1", "qwen-max",
    ],
    "external_api": [
        "elevenlabs", "openai-tts", "google-tts",
        "dall-e-3", "midjourney", "ideogram",
        "imagen-3", "aurora", "amazon-titan-image",
        "heygen", "synthesia", "remotion",
    ],
}

TAREFA_TIER = {
    "qualificar_leads": "lite",
    "scoring_leads": "lite",
    "gerar_template_email": "lite",
    "classificar_conteudo": "lite",
    "deduplicar_leads": "lite",
    "formatar_output": "lite",
    "gerar_copy": "standard",
    "escrever_emails": "standard",
    "gerar_pagina_venda": "standard",
    "gerar_pagina_captura": "standard",
    "analise_funil": "standard",
    "gerar_artes_prompt": "standard",
    "gerar_roteiro_video": "standard",
    "gerar_sequencia_dm": "standard",
    "escrever_post_social": "standard",
    "estrategia_marketing": "pro",
    "definir_escada_valor": "pro",
    "diagnosticar_gargalo": "pro",
    "otimizar_campanha_complexa": "pro",
    "analise_competitiva": "pro",
    "criar_funil_do_zero": "pro",
    "gerar_audio": "external_api",
    "gerar_imagem": "external_api",
    "gerar_video": "external_api",
}


def detectar_harness():
    cwd = os.getcwd()
    home = os.path.expanduser("~")
    detectados = []
    for harness, signatures in HARNESS_SIGNATURES.items():
        for sig in signatures:
            if os.path.exists(os.path.join(cwd, sig)) or \
               os.path.exists(os.path.join(home, sig)) or \
               os.path.exists(sig):
                detectados.append(harness)
                break
    return detectados if detectados else ["desconhecido"]


def detectar_env_vars():
    """Detecta provedores disponíveis via variáveis de ambiente."""
    providers = {}
    checks = {
        "anthropic": ["ANTHROPIC_API_KEY"],
        "openai": ["OPENAI_API_KEY"],
        "google": ["GOOGLE_API_KEY", "GOOGLE_GENAI_API_KEY", "GEMINI_API_KEY"],
        "xai": ["XAI_API_KEY"],
        "aws_bedrock": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"],
        "elevenlabs": ["ELEVENLABS_API_KEY", "XI_API_KEY"],
        "mistral": ["MISTRAL_API_KEY"],
        "deepseek": ["DEEPSEEK_API_KEY"],
    }
    for provider, keys in checks.items():
        for key in keys:
            val = os.environ.get(key, "")
            if val:
                providers[provider] = {"env_key": key, "key_preview": val[:8] + "..."}
                break
    return providers


def detectar_orca_runtime():
    """Detecta modelo via runtime Orca/MiMoCode (gerenciamento interno de chaves)."""
    info = {"is_orca": False, "modelo_atual": None, "modelo_id": None}

    # Orca expõe tokens de sessão
    if os.environ.get("ORCA_AGENT_HOOK_TOKEN") or os.environ.get("ORCA_AGENT_LAUNCH_TOKEN"):
        info["is_orca"] = True

    # MiMoCode: modelo da sessão pode estar em env ou no system prompt
    # O modelo atual é detectado pelo system prompt: "mimo-v2.5-pro"
    mimocode_model = os.environ.get("MIMOCODE_MODEL", "")
    if mimocode_model:
        info["modelo_atual"] = mimocode_model

    return info


def listar_modelos(harnesses, env_providers, orca_info):
    """Monta lista de modelos disponíveis por provider."""
    modelos = {}

    # Por env vars (mais confiável)
    if "anthropic" in env_providers:
        modelos["anthropic"] = {
            "lite": ["claude-haiku", "claude-3-5-haiku"],
            "standard": ["claude-sonnet", "claude-sonnet-4", "claude-3-5-sonnet"],
            "pro": ["claude-opus", "claude-opus-4"],
        }
    if "openai" in env_providers:
        modelos["openai"] = {
            "lite": ["gpt-4o-mini"],
            "standard": ["gpt-4o", "gpt-4-turbo"],
            "pro": ["gpt-4", "o1", "o3"],
        }
    if "google" in env_providers:
        modelos["google"] = {
            "lite": ["gemini-2.0-flash", "gemini-2.5-flash"],
            "standard": ["gemini-2.5-pro"],
            "pro": ["gemini-ultra"],
        }
    if "xai" in env_providers:
        modelos["xai"] = {
            "lite": ["grok-2-mini"],
            "standard": ["grok-2", "grok-3"],
            "pro": ["grok-3-heavy"],
        }
    if "aws_bedrock" in env_providers:
        modelos["bedrock"] = {
            "lite": ["amazon-titan-lite", "claude-haiku"],
            "standard": ["claude-sonnet-v2"],
            "pro": ["claude-opus-v2"],
        }
    if "mistral" in env_providers:
        modelos["mistral"] = {
            "lite": ["mistral-small"],
            "standard": ["mistral-large"],
            "pro": [],
        }
    if "deepseek" in env_providers:
        modelos["deepseek"] = {
            "lite": [],
            "standard": [],
            "pro": ["deepseek-r1"],
        }

    # MiMoCode: tenta ler config
    if "mimocode" in harnesses:
        for path in ["~/.mimocode/config.json", ".mimocode.json"]:
            p = os.path.expanduser(path)
            if os.path.exists(p):
                try:
                    with open(p) as f:
                        cfg = json.load(f)
                    raw = cfg.get("models", cfg.get("providers", {}))
                    if raw:
                        modelos["mimocode_config"] = {"raw": raw}
                except:
                    pass

    # Orca/MiMoCode runtime: modelo gerenciado internamente
    # Quando is_orca=True e não há ENV vars, o modelo é o da sessão atual
    # Subagentes com "model: inherit" herdam esse modelo
    if orca_info.get("is_orca") and not modelos:
        modelos["orca_runtime"] = {
            "lite": ["mimo-v2.5-lite"],
            "standard": ["mimo-v2.5", "mimo-v2.5-standard"],
            "pro": ["mimo-v2.5-pro"],
            "_nota": "Modelo gerenciado pelo runtime Orca — subagentes herdam via 'model: inherit'"
        }

    return modelos


def rotear_tarefa(tarefa, modelos_disponiveis):
    tier_necessario = TAREFA_TIER.get(tarefa, "lite")
    candidatos = TIER_MAP.get(tier_necessario, [])

    for modelo_cand in candidatos:
        for provider, tiers in modelos_disponiveis.items():
            if isinstance(tiers, dict):
                for tier, lista in tiers.items():
                    if modelo_cand in lista:
                        return {"provider": provider, "model": modelo_cand, "tier": tier_necessario}

    return {"provider": "nenhum", "model": "SEM_MODELO", "tier": tier_necessario}


def main():
    print("=" * 60)
    print("  DESCOBERTA DE LLMs — Diagnóstico do Harness")
    print("=" * 60)

    # 1. Detectar harness
    harnesses = detectar_harness()
    print(f"\n🔍 Harness detectado: {', '.join(harnesses)}")

    # 2. Detectar Orca/MiMoCode runtime
    orca_info = detectar_orca_runtime()
    if orca_info["is_orca"]:
        print(f"\n🐳 Runtime Orca/MiMoCode detectado")
        print(f"   Modelo da sessão: mimo-v2.5-pro (via system prompt)")
        print(f"   Subagentes com 'model: inherit' herdam este modelo")

    # 3. Detectar env vars
    env_providers = detectar_env_vars()
    print(f"\n🔑 Providers via ENV ({len(env_providers)} encontrados):")
    if env_providers:
        for prov, info in env_providers.items():
            print(f"   ✅ {prov}: {info['env_key']} = {info['key_preview']}")
    else:
        print("   ⚠️  Nenhuma API key em variáveis de ambiente (normal no Orca)")

    # 4. Listar modelos
    modelos = listar_modelos(harnesses, env_providers, orca_info)
    print(f"\n📦 Modelos disponíveis:")
    for provider, tiers in modelos.items():
        if isinstance(tiers, dict) and "raw" not in tiers:
            total = sum(len(v) for v in tiers.values() if isinstance(v, list))
            nota = tiers.get("_nota", "")
            print(f"\n   {provider.upper()} ({total} modelos):")
            for tier, lista in tiers.items():
                if tier.startswith("_"):
                    continue
                if isinstance(lista, list) and lista:
                    print(f"      {tier}: {', '.join(lista)}")
            if nota:
                print(f"      ℹ️  {nota}")
        elif isinstance(tiers, dict) and "raw" in tiers:
            print(f"\n   {provider.upper()} (config direta):")
            print(f"      {json.dumps(tiers['raw'], indent=6)}")

    # 5. Roteamento por tarefa
    print("\n" + "=" * 60)
    print("  ROTEAMENTO: tarefa → modelo mais barato")
    print("=" * 60)

    if modelos:
        for tarefa in TAREFA_TIER:
            resultado = rotear_tarefa(tarefa, modelos)
            status = "✅" if resultado["model"] != "SEM_MODELO" else "❌"
            print(f"  {status} {tarefa:35s} → {resultado['provider']:15s} / {resultado['model']}  [{resultado['tier']}]")
    else:
        print("  ❌ Nenhum modelo disponível para roteamento")

    # 6. Resumo
    print("\n" + "=" * 60)
    total_modelos = 0
    for v in modelos.values():
        if isinstance(v, dict) and "raw" not in v:
            for k, lista in v.items():
                if isinstance(lista, list) and not k.startswith("_"):
                    total_modelos += len(lista)
    tarefas_ok = sum(1 for t in TAREFA_TIER if rotear_tarefa(t, modelos)["model"] != "SEM_MODELO")

    print(f"  RESUMO: {total_modelos} modelos | {tarefas_ok}/{len(TAREFA_TIER)} tarefas roteáveis")

    if orca_info["is_orca"]:
        print(f"\n  💡 DICA: No Orca/MiMoCode, subagentes herdam o modelo da sessão.")
        print(f"     Para forçar um modelo específico, use 'model: <nome>' no subagente.")
        print(f"     Exemplo: 'model: mimo-v2.5-lite' para tarefas tier lite (economia)")

    print("=" * 60)


if __name__ == "__main__":
    main()
