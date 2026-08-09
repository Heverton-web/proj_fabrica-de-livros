#!/usr/bin/env python3
"""
Migra slug longo para código curto em todas as pastas de output.

Uso:
    python scripts/migrar-slug.py oh-my-pi oh-my
    python scripts/migrar-slug.py --dry-run oh-my-pi oh-my
"""
import sys
import json
from pathlib import Path

DIR_OUTPUT = Path(__file__).resolve().parent.parent / "output"


def encontrar_pastas(slug_antigo):
    """Encontra todas as pastas que contêm o slug antigo."""
    pastas = []
    for caminho in DIR_OUTPUT.rglob(f"*{slug_antigo}*"):
        if caminho.is_dir():
            pastas.append(caminho)
    return sorted(pastas, key=lambda p: len(str(p)), reverse=True)


def renomear_pasta(caminho, slug_antigo, slug_novo, dry_run=False):
    """Renomeia uma pasta substituindo o slug."""
    novo_nome = caminho.name.replace(slug_antigo, slug_novo)
    novo_caminho = caminho.parent / novo_nome
    
    if novo_caminho.exists():
        print(f"  [AVISO] Já existe: {novo_caminho}")
        return False
    
    if dry_run:
        print(f"  [DRY-RUN] {caminho.name} -> {novo_nome}")
        return True
    
    caminho.rename(novo_caminho)
    print(f"  [OK] {caminho.name} -> {novo_nome}")
    return True


def atualizar_config(slug_antigo, slug_novo, dry_run=False):
    """Atualiza referências ao slug antigo em arquivos de configuração."""
    arquivos_config = [
        "config_obra.json",
        "derivados.json",
        "sumario_macro.json",
    ]
    
    atualizados = 0
    for config_file in arquivos_config:
        for caminho in DIR_OUTPUT.rglob(config_file):
            try:
                conteudo = caminho.read_text(encoding="utf-8")
                if slug_antigo in conteudo:
                    novo_conteudo = conteudo.replace(slug_antigo, slug_novo)
                    if dry_run:
                        print(f"  [DRY-RUN] Atualizar: {caminho}")
                    else:
                        caminho.write_text(novo_conteudo, encoding="utf-8")
                        print(f"  [OK] Atualizado: {caminho}")
                    atualizados += 1
            except Exception as e:
                print(f"  [ERRO] {caminho}: {e}")
    
    return atualizados


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Migra slug longo para código curto")
    parser.add_argument("slug_antigo", help="Slug atual (ex: oh-my-pi)")
    parser.add_argument("slug_novo", help="Código curto (ex: oh-my)")
    parser.add_argument("--dry-run", action="store_true", help="Simula sem alterar")
    args = parser.parse_args()
    
    print(f"=== MIGRAÇÃO: {args.slug_antigo} -> {args.slug_novo} ===\n")
    
    # 1. Encontrar pastas
    pastas = encontrar_pastas(args.slug_antigo)
    print(f"Pastas encontradas: {len(pastas)}\n")
    
    if not pastas:
        print("Nenhuma pasta para migrar.")
        return 0
    
    # 2. Renomear pastas
    print("--- Renomeando pastas ---")
    renomeadas = 0
    for pasta in pastas:
        if renomear_pasta(pasta, args.slug_antigo, args.slug_novo, args.dry_run):
            renomeadas += 1
    
    print(f"\nPastas renomeadas: {renomeadas}/{len(pastas)}")
    
    # 3. Atualizar configs
    print("\n--- Atualizando configurações ---")
    configs = atualizar_config(args.slug_antigo, args.slug_novo, args.dry_run)
    print(f"\nConfigs atualizadas: {configs}")
    
    # 4. Resumo
    print(f"\n=== RESUMO ===")
    print(f"Slug antigo: {args.slug_antigo}")
    print(f"Slug novo: {args.slug_novo}")
    print(f"Economia por caminho: {len(args.slug_antigo) - len(args.slug_novo)} chars")
    print(f"Pastas renomeadas: {renomeadas}")
    print(f"Configs atualizadas: {configs}")
    
    if args.dry_run:
        print("\n[DRY-RUN] Nenhuma alteração foi feita. Execute sem --dry-run para aplicar.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
