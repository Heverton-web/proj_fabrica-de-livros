#!/usr/bin/env python3
"""
Renomeia e-books com nomes comerciais curtos (max 30 chars).

Uso:
    python scripts/renomear-ebooks.py --dry-run
    python scripts/renomear-ebooks.py
"""
import json
import sys
from pathlib import Path

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

# Mapeamento de nomes longos -> nomes curtos comerciais
MAPEAMENTO_EBOOKS = {
    # Coleção harness
    "harness--eb-01-a-revolucao-dos-agentes-por-que-o-modelo": "eb-01-coding-agents",
    "harness--eb-02-test-harness-a-heranca-da-engenharia-de": "eb-02-test-harness",
    "harness--eb-03-o-ciclo-react-e-os-loops-de-execucao-san": "eb-03-ciclo-react",
    "harness--eb-04-gestao-de-contexto-combatendo-o-context": "eb-04-contexto",
    # Coleção oh-my (já ok, mas incluir para consistência)
    "oh-my--eb-01-que-coding": "eb-01-coding-agents",
    "oh-my--eb-02-instalacao-primeiros": "eb-02-instalacao",
    "oh-my--eb-03-31-ferramentas": "eb-03-ferramentas",
    "oh-my--eb-04-lsp-integrado": "eb-04-lsp",
    "oh-my--eb-05-subagentes-fan": "eb-05-subagentes",
    "oh-my--eb-06-colaboracao-vivo": "eb-06-colaboracao",
    "oh-my--eb-07-60-providers": "eb-07-providers",
    "oh-my--eb-08-memory-system": "eb-08-memory",
}


def renomear_ebooks(dry_run=False):
    """Renomeia e-books com nomes curtos."""
    renomeados = []
    erros = []
    
    for colecao in ["harness", "oh-my"]:
        dir_ebooks = DIR_OUTPUT / colecao / "ebooks"
        if not dir_ebooks.exists():
            continue
        
        for pasta in dir_ebooks.iterdir():
            if not pasta.is_dir():
                continue
            
            nome_atual = pasta.name
            if nome_atual in MAPEAMENTO_EBOOKS:
                nome_novo = MAPEAMENTO_EBOOKS[nome_atual]
                novo_caminho = pasta.parent / nome_novo
                
                if novo_caminho.exists():
                    print(f"  [AVISO] Já existe: {nome_novo}")
                    continue
                
                if dry_run:
                    print(f"  [DRY-RUN] {nome_atual} -> {nome_novo}")
                    renomeados.append(nome_atual)
                else:
                    try:
                        pasta.rename(novo_caminho)
                        print(f"  [OK] {nome_atual} -> {nome_novo}")
                        renomeados.append(nome_atual)
                    except Exception as e:
                        print(f"  [ERRO] {nome_atual}: {e}")
                        erros.append(nome_atual)
    
    return renomeados, erros


def atualizar_derivados(colecao, dry_run=False):
    """Atualiza referências em derivados.json."""
    derivados_path = DIR_OUTPUT / colecao / "livros" / colecao / "derivados.json"
    if not derivados_path.exists():
        return
    
    try:
        with open(derivados_path, "r", encoding="utf-8") as f:
            derivados = json.load(f)
    except (json.JSONDecodeError, OSError):
        return
    
    alterado = False
    for tipo in ["artigos", "ebooks"]:
        if tipo in derivados and "itens" in derivados[tipo]:
            for item in derivados[tipo]["itens"]:
                slug_atual = item.get("slug", "")
                if slug_atual in MAPEAMENTO_EBOOKS:
                    slug_novo = MAPEAMENTO_EBOOKS[slug_atual]
                    if not dry_run:
                        item["slug"] = slug_novo
                        if "diretorio" in item:
                            item["diretorio"] = item["diretorio"].replace(slug_atual, slug_novo)
                        alterado = True
                    print(f"  [DRY-RUN] {tipo}: {slug_atual} -> {slug_novo}")
    
    if alterado and not dry_run:
        with open(derivados_path, "w", encoding="utf-8") as f:
            json.dump(derivados, f, ensure_ascii=False, indent=2)
        print(f"  [OK] derivados.json atualizado")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Renomeia e-books com nomes curtos")
    parser.add_argument("--dry-run", action="store_true", help="Simula sem alterar")
    args = parser.parse_args()
    
    print("=== RENOMEAÇÃO DE EBOOKS ===\n")
    
    renomeados, erros = renomear_ebooks(dry_run=args.dry_run)
    
    print(f"\nRenomeados: {len(renomeados)}")
    if erros:
        print(f"Erros: {len(erros)}")
    
    if not args.dry_run and renomeados:
        print("\n=== ATUALIZANDO DERIVADOS ===")
        for colecao in ["harness", "oh-my"]:
            atualizar_derivados(colecao, dry_run=args.dry_run)
    
    return 0 if not erros else 1


if __name__ == "__main__":
    sys.exit(main())
