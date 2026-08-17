#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Universal para Mapeamento de Provedores e LLMs Gratuitas.
Compatível com qualquer harness (Claude Code, Aider, Continue, Cursor, Windsurf, MiMoCode, etc.).
"""

import os
import sys
import json
import urllib.request

# Configuração de Provedores Gratuitos e de Baixo Custo / Free Trial
PROVIDERS_GRATUITOS = {
    "google": {
        "nome": "Google Gemini (Free tier)",
        "keys": ["GEMINI_API_KEY", "GOOGLE_API_KEY", "GOOGLE_GENAI_API_KEY"],
        "modelos": ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"],
        "info_url": "https://aistudio.google.com/"
    },
    "groq": {
        "nome": "Groq Cloud (Free tier c/ limites)",
        "keys": ["GROQ_API_KEY"],
        "modelos": ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it"],
        "info_url": "https://console.groq.com/"
    },
    "openrouter": {
        "nome": "OpenRouter (Free Models)",
        "keys": ["OPENROUTER_API_KEY"],
        "modelos": [
            "google/gemini-2.5-flash:free",
            "meta-llama/llama-3-8b-instruct:free",
            "mistralai/mistral-7b-instruct:free",
            "qwen/qwen-2-7b-instruct:free",
            "openrouter/auto-free"
        ],
        "info_url": "https://openrouter.ai/"
    },
    "github": {
        "nome": "GitHub Models (Free para Devs)",
        "keys": ["GITHUB_TOKEN", "GH_TOKEN"],
        "modelos": ["gpt-4o-mini", "meta-llama-3-8b-instruct", "phi-3-medium-instruct"],
        "info_url": "https://github.com/marketplace/models"
    },
    "sambanova": {
        "nome": "SambaNova Cloud (Generous Free tier)",
        "keys": ["SAMBANOVA_API_KEY"],
        "modelos": ["Meta-Llama-3.1-405B-Instruct", "Meta-Llama-3.1-70B-Instruct", "Meta-Llama-3.1-8B-Instruct"],
        "info_url": "https://cloud.sambanova.ai/"
    },
    "cerebras": {
        "nome": "Cerebras (Fast Free tier/credits)",
        "keys": ["CEREBRAS_API_KEY"],
        "modelos": ["llama3.1-8b", "llama3.1-70b"],
        "info_url": "https://cloud.cerebras.ai/"
    },
    "huggingface": {
        "nome": "Hugging Face (Serverless Free API)",
        "keys": ["HF_API_KEY", "HF_TOKEN"],
        "modelos": ["meta-llama/Llama-3.2-3B-Instruct", "mistralai/Mistral-7B-Instruct-v0.3"],
        "info_url": "https://huggingface.co/settings/tokens"
    },
    "cohere": {
        "nome": "Cohere (Free Trial Keys)",
        "keys": ["COHERE_API_KEY"],
        "modelos": ["command-r", "command-r-plus"],
        "info_url": "https://dashboard.cohere.com/"
    },
    "mistral": {
        "nome": "Mistral AI (Codestral Free)",
        "keys": ["MISTRAL_API_KEY"],
        "modelos": ["mistral-tiny", "codestral-mamba"],
        "info_url": "https://console.mistral.ai/"
    },
    "opencode_zen": {
        "nome": "OpenCode Zen (Free Models)",
        "keys": ["OPENCODE_ZEN_API_KEY"],
        "modelos": ["deepseek-v4-flash", "mimo-v2.5", "qwen-3.6-plus", "minimax-m3", "big-pickle"],
        "info_url": "https://opencode.ai/zen"
    },
    "cloudflare": {
        "nome": "Cloudflare Workers AI (Free)",
        "keys": ["CLOUDFLARE_API_TOKEN", "CLOUDFLARE_ACCOUNT_ID"],
        "modelos": ["llama-3.1-8b", "llama-3.1-70b", "qwen-2.5", "deepseek"],
        "info_url": "https://dash.cloudflare.com"
    },
    "siliconflow": {
        "nome": "SiliconFlow (Free Models)",
        "keys": ["SILICONFLOW_API_KEY"],
        "modelos": ["qwen3-8b", "deepseek-r1-distill-qwen-7b", "glm-4"],
        "info_url": "https://cloud.siliconflow.com"
    },
    "nvidia_nim": {
        "nome": "NVIDIA NIM (Developer Program)",
        "keys": ["NVIDIA_API_KEY"],
        "modelos": ["llama-3", "nemotron", "mistral-hosted", "qwen-hosted"],
        "info_url": "https://build.nvidia.com"
    },
    "fireworks": {
        "nome": "Fireworks AI (AMD Developer Program)",
        "keys": ["FIREWORKS_API_KEY"],
        "modelos": ["llama-3.3", "deepseek-v4", "qwen-3"],
        "info_url": "https://fireworks.ai"
    }
}


def detectar_harnesses():
    """Detecta quais harnesses/agentes estão presentes no diretório atual ou HOME."""
    cwd = os.getcwd()
    home = os.path.expanduser("~")
    
    harness_configs = {
        "Claude Code": [".claude", "CLAUDE.md", "settings.json", "settings.local.json"],
        "Aider": [".aider.conf.yml", ".aider.tags.cache.v3", ".aider"],
        "Continue": [".continue", os.path.join(home, ".continue", "config.json")],
        "Cursor": [".cursor", ".cursor/rules", ".cursor/mcp.json"],
        "Windsurf": [".windsurf", ".windsurfrules"],
        "Gemini CLI": [".gemini", "gemini.json", ".gemini-cli"],
        "MiMoCode / Orca": [".mimocode", "mimocode.json"],
        "Antigravity": [".antigravity", "antigravity.json"],
        "OpenCode": [".opencode", "opencode.json"],
        "Grok": [".grok", "grok.json"]
    }
    
    detectados = []
    for nome, sigs in harness_configs.items():
        for sig in sigs:
            path_cwd = os.path.join(cwd, sig)
            path_home = os.path.join(home, sig) if not os.path.isabs(sig) else sig
            if os.path.exists(path_cwd) or os.path.exists(path_home) or os.path.exists(sig):
                detectados.append(nome)
                break
    return sorted(list(set(detectados)))


def checar_ollama():
    """Verifica se Ollama está rodando e lista modelos instalados localmente."""
    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    if not host.startswith("http://") and not host.startswith("https://"):
        host = "http://" + host
    try:
        req = urllib.request.Request(f"{host}/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=1.5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                modelos = [m["name"] for m in data.get("models", [])]
                return True, host, modelos
    except Exception:
        pass
    return False, host, []


def checar_llama_cpp():
    """Verifica se há um servidor local Llama.cpp / compatível OpenAI rodando."""
    host = os.environ.get("LLAMACPP_HOST", "http://localhost:8080")
    if not host.startswith("http://") and not host.startswith("https://"):
        host = "http://" + host
    try:
        req = urllib.request.Request(f"{host}/v1/models", method="GET")
        with urllib.request.urlopen(req, timeout=1.5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                modelos = [m.get("id") for m in data.get("data", [])]
                return True, host, modelos
    except Exception:
        pass
    return False, host, []


def analisar_provedores():
    """Analisa as variáveis de ambiente para mapear provedores ativos e inativos."""
    relatorio = {}
    
    for key, info in PROVIDERS_GRATUITOS.items():
        chave_ativa = None
        for env_key in info["keys"]:
            val = os.environ.get(env_key, "").strip()
            if val and len(val) > 5:
                chave_ativa = env_key
                break
                
        relatorio[key] = {
            "nome": info["nome"],
            "ativo": chave_ativa is not None,
            "chave_detectada": chave_ativa,
            "modelos": info["modelos"],
            "info_url": info["info_url"]
        }
        
    return relatorio


def gerar_saida_textual(harnesses, provedores, ollama_status, llamacpp_status):
    """Imprime um relatório formatado e amigável em PT-BR."""
    print("=" * 70)
    print("   UNIVERSAL LLM MAPPER — MAPEAMENTO DE PROVEDORES E LLMs GRATUITAS")
    print("=" * 70)
    
    print(f"📁 Diretório Atual : {os.getcwd()}")
    print(f"🤖 Harnesses Ativos: {', '.join(harnesses) if harnesses else 'Nenhum harness específico detectado'}")
    print("=" * 70)
    
    # 1. Provedores de API Externos Gratuitos / Free Tier
    print("\n🌐 PROVEDORES EXTERNOS (FREE TIER / DEVEL TRIAL):")
    print("-" * 70)
    
    ativos = []
    inativos = []
    
    for prov_id, info in provedores.items():
        status_str = "🟢 ATIVO" if info["ativo"] else "🔴 INATIVO"
        chave_str = f"({info['chave_detectada']})" if info["ativo"] else "(Ausente)"
        
        print(f"  {status_str} | {info['nome']:40s} {chave_str}")
        print(f"           └─ Modelos: {', '.join(info['modelos'])}")
        if not info["ativo"]:
            print(f"           └─ Obter chave em: {info['info_url']}")
        print()
        
        if info["ativo"]:
            ativos.append(info)
        else:
            inativos.append(info)
            
    # 2. Serviços Locais Gratuitos
    print("=" * 70)
    print("💻 SERVIÇOS LOCAIS DE LLM (100% GRATUITOS E PRIVADOS):")
    print("-" * 70)
    
    # Ollama
    ollama_ok, ollama_url, ollama_models = ollama_status
    if ollama_ok:
        print(f"  🟢 ATIVO   | Ollama executando em {ollama_url}")
        if ollama_models:
            print(f"           └─ Modelos locais detectados: {', '.join(ollama_models)}")
        else:
            print("           └─ Nenhum modelo baixado no Ollama ainda. Rode: 'ollama run <modelo>'")
    else:
        print(f"  🔴 INATIVO | Ollama em {ollama_url}")
        print("           └─ Instale em: https://ollama.com e inicie o serviço.")
    print()
    
    # Llama.cpp / Local OpenAI Server
    lcpp_ok, lcpp_url, lcpp_models = llamacpp_status
    if lcpp_ok:
        print(f"  🟢 ATIVO   | Servidor Llama.cpp / OpenAI local em {lcpp_url}")
        if lcpp_models:
            print(f"           └─ Modelos ativos: {', '.join(lcpp_models)}")
    else:
        print(f"  🔴 INATIVO | Servidor Llama.cpp local em {lcpp_url}")
    
    print("=" * 70)
    
    # 3. Recomendações e Resumo
    print("💡 RESUMO E RECOMENDAÇÕES DE ATIVAÇÃO:")
    print("-" * 70)
    total_ativos = len(ativos) + (1 if ollama_ok else 0) + (1 if lcpp_ok else 0)
    print(f"  -> Fontes de LLM Gratuitas Prontas para Uso: {total_ativos}")
    
    if inativos:
        print("\n  Para expandir seu arsenal de LLMs sem gastar nada:")
        for inat in inativos[:3]: # Sugere os 3 primeiros
            print(f"  • {inat['nome']}: pegue sua chave gratuita em {inat['info_url']}")
            
    print("\n  No seu Harness, configure as chaves detectadas em suas variáveis de ambiente ou arquivo .env")
    print("=" * 70)


def main():
    harnesses = detectar_harnesses()
    ollama_status = checar_ollama()
    llamacpp_status = checar_llama_cpp()
    provedores = analisar_provedores()
    
    # Suporte para exportação JSON estruturada
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        data = {
            "workspace": os.getcwd(),
            "harnesses_detectados": harnesses,
            "provedores_externos": provedores,
            "servicos_locais": {
                "ollama": {
                    "ativo": ollama_status[0],
                    "host": ollama_status[1],
                    "modelos": ollama_status[2]
                },
                "llama_cpp": {
                    "ativo": llamacpp_status[0],
                    "host": llamacpp_status[1],
                    "modelos": llamacpp_status[2]
                }
            }
        }
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        gerar_saida_textual(harnesses, provedores, ollama_status, llamacpp_status)


if __name__ == "__main__":
    main()
