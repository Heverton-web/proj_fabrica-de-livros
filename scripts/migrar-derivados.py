#!/usr/bin/env python3
"""
Migra materiais derivados (artigos/ebooks) com nomes longos para nomes curtos.

Uso:
    python scripts/migrar-derivados.py --dry-run
    python scripts/migrar-derivados.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import nomes_curtos as NC

DIR_OUTPUT = Path(__file__).resolve().parent.parent / "output"


def encontrar_materiais_longos():
    """Encontra materiais derivados com nomes > 2 palavras."""
    materiais = []
    for tipo in ["artigos", "ebooks"]:
        dir_tipo = DIR_OUTPUT / tipo
        if dir_tipo.exists():
            for pasta in dir_tipo.iterdir():
                if pasta.is_dir():
                    palavras = NC.palavras(pasta.name)
                    if len(palavras) > 2:
                        materiais.append(pasta)
    return materiais


def gerar_nome_curto(slug_atual):
    """Gera nome curto para o material."""
    partes = slug_atual.split("--")
    if len(partes) < 2:
        return slug_atual
    
    prefixo = partes[0]  # ex: oh-my--art-01
    nome_completo = "--".join(partes[1:])
    
    # Gerar nome curto (max 35 chars total para preservar semantica)
    nome_curto = NC.nome_curto(nome_completo, max_palavras=4, maximo=35)
    return f"{prefixo}--{nome_curto}"


def migrar_pasta(pasta, novo_nome, dry_run=False):
    """Migra uma pasta para o novo nome."""
    novo_caminho = pasta.parent / novo_nome
    
    if novo_caminho.exists():
        print(f"  [AVISO] Ja existe: {novo_nome}")
        return False
    
    if dry_run:
        print(f"  [DRY-RUN] {pasta.name} -> {novo_nome}")
        return True
    
    pasta.rename(novo_caminho)
    print(f"  [OK] {pasta.name} -> {novo_nome}")
    return True


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Migra materiais derivados com nomes longos")
    parser.add_argument("--dry-run", action="store_true", help="Simula sem alterar")
    args = parser.parse_args()
    
    print("=== MIGRAÇÃO DE MATERIAIS DERIVADOS ===\n")
    
    materiais = encontrar_materiais_longos()
    print(f"Materiais encontrados: {len(materiais)}\n")
    
    if not materiais:
        print("Nenhum material para migrar.")
        return 0
    
    migrados = 0
    for pasta in materiais:
        novo_nome = gerar_nome_curto(pasta.name)
        if migrar_pasta(pasta, novo_nome, args.dry_run):
            migrados += 1
    
    print(f"\n=== RESUMO ===")
    print(f"Materiais migrados: {migrados}/{len(materiais)}")
    
    if args.dry_run:
        print("\n[DRY-RUN] Nenhuma alteracao foi feita. Execute sem --dry-run para aplicar.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
