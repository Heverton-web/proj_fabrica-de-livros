#!/usr/bin/env python3
"""
Correção emergencial de nomenclatura e caminhos longos.

Resolve:
1. Slugs com mais de 2 palavras -> codigo curto
2. Caminhos que excedem MAX_PATH (260 chars)
3. Materiais com nomes muito longos
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import nomes_curtos as NC

DIR_OUTPUT = Path(__file__).resolve().parent.parent / "output"


def diagnosticar_caminhos():
    """Lista caminhos que excedem ou aproximam do MAX_PATH."""
    problemas = []
    for caminho in DIR_OUTPUT.rglob("*"):
        if caminho.is_file():
            diag = NC.diagnosticar(caminho)
            if diag["arriscado"]:
                problemas.append(diag)
    return sorted(problemas, key=lambda x: x["chars"], reverse=True)


def sugerir_codigo(slug):
    """Sugere o código curto para um slug."""
    codigo = NC.codigo_obra(slug)
    return {
        "slug_original": slug,
        "codigo_sugerido": codigo,
        "economia": len(slug) - len(codigo),
    }


def listar_slugs_longos():
    """Encontra pastas de obra com mais de 2 palavras."""
    slugs = []
    for tipo in ["livros", "tccs", "artigos", "ebooks", "playbooks", "lead-magnets"]:
        dir_tipo = DIR_OUTPUT / tipo
        if dir_tipo.exists():
            for pasta in dir_tipo.iterdir():
                if pasta.is_dir():
                    palavras = NC.palavras(pasta.name)
                    if len(palavras) > 2:
                        slugs.append({
                            "tipo": tipo,
                            "slug": pasta.name,
                            "palavras": len(palavras),
                            "sugerido": NC.codigo_obra(pasta.name),
                        })
    return slugs


def main():
    print("=== DIAGNÓSTICO DE NOMENCLATURA ===\n")
    
    # 1. Slugs longos
    slugs = listar_slugs_longos()
    if slugs:
        print(f"[ALERTA] {len(slugs)} pastas com slug > 2 palavras:")
        for s in slugs:
            print(f"  - {s['tipo']}/{s['slug']} ({s['palavras']} palavras)")
            print(f"    Sugerido: {s['sugerido']}")
        print()
    
    # 2. Caminhos longos
    problemas = diagnosticar_caminhos()
    if problemas:
        print(f"[ALERTA] {len(problemas)} arquivos com caminho ARRISCADO (>220 chars):")
        for p in problemas[:10]:  # Top 10
            print(f"  - {p['chars']} chars: ...{p['caminho'][-60:]}")
        print()
    
    # 3. Sugestões para o slug atual
    print("=== SUGESTÕES PARA SLUGS ===")
    for slug_teste in ["oh-my-pi", "harness-engineering", "ia-agentica-desbloqueada"]:
        sug = sugerir_codigo(slug_teste)
        print(f"  {sug['slug_original']} -> {sug['codigo_sugerido']} (economia: {sug['economia']} chars)")
    
    return 0 if not slugs and not problemas else 1


if __name__ == "__main__":
    sys.exit(main())
