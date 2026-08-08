#!/usr/bin/env python3
"""
Orquestrador: cria máquina de vendas completa a partir de uma obra finalizada.
Gera projeto full-stack deployável (Next.js + FastAPI + SQLite).

Uso:
    python scripts/criar-maquina-vendas.py <slug> [--tipo completo|parcial|landing|backend]
"""
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
TEMPLATE_DIR = BASE_DIR / "templates" / "maquina"
OUTPUT_BASE = BASE_DIR / "marketing" / "maquinas"
OBRA_BASE = BASE_DIR / "output"


def slug_para_titulo(slug: str) -> str:
    return slug.replace("-", " ").replace("_", " ").title()


def verificar_obra_existe(slug: str) -> dict:
    """Verifica se a obra existe e retorna seus metadados."""
    possible_dirs = [
        OBRA_BASE / "livros" / slug,
        OBRA_BASE / "tccs" / slug,
        OBRA_BASE / "ebooks" / slug,
        OBRA_BASE / "artigos" / slug,
        OBRA_BASE / "playbooks" / slug,
        OBRA_BASE / "lead-magnets" / slug,
        OBRA_BASE / "decks" / slug,
    ]
    for d in possible_dirs:
        if d.exists():
            meta_file = d / "config_obra.json"
            meta = {}
            if meta_file.exists():
                with open(meta_file, encoding="utf-8") as f:
                    meta = json.load(f)
            return {"path": str(d), "tipo": d.parent.name, "meta": meta}
    return {}


def copiar_template(src: Path, dst: Path, replacements: dict):
    """Copia template substituindo placeholders."""
    if src.is_dir():
        dst.mkdir(parents=True, exist_ok=True)
        for item in src.iterdir():
            copiar_template(item, dst / item.name, replacements)
    elif src.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True)
        content = src.read_text(encoding="utf-8", errors="replace")
        for key, value in replacements.items():
            content = content.replace(key, value)
        dst.write_text(content, encoding="utf-8")


def gerar_manifesto(slug: str, titulo: str, obra_info: dict, tipo: str) -> dict:
    """Gera manifesto da máquina de vendas."""
    return {
        "id": f"mv-{datetime.now().strftime('%Y%m%d')}-{slug}",
        "slug": slug,
        "titulo": titulo,
        "obra_origem": obra_info.get("path", ""),
        "tipo_obra": obra_info.get("tipo", "desconhecido"),
        "tipo_maquina": tipo,
        "criada_em": datetime.now().isoformat(),
        "status": "criada",
        "stack": {
            "frontend": "nextjs-14",
            "backend": "fastapi",
            "database": "sqlite",
            "deploy": "docker-vercel",
        },
        "escada_valor": {
            "nivel_0": {"tipo": "lead_magnet", "preco": 0},
            "nivel_1": {"tipo": "tripwire", "preco": 37},
            "nivel_2": {"tipo": "core", "preco": 97},
            "nivel_3": {"tipo": "obra_completa", "preco": 297},
        },
        "metricas": {
            "leads": 0,
            "vendas": 0,
            "receita": 0.0,
            "taxa_conversao": 0.0,
        },
    }


def criar_maquina(slug: str, tipo: str = "completo"):
    """Função principal: cria a máquina de vendas."""
    titulo = slug_para_titulo(slug)
    obra_info = verificar_obra_existe(slug)
    destino = OUTPUT_BASE / slug

    print(f"\n{'='*60}")
    print(f"  CRIANDO MÁQUINA DE VENDAS: {titulo}")
    print(f"  Tipo: {tipo}")
    print(f"  Destino: {destino}")
    print(f"{'='*60}\n")

    if destino.exists():
        resp = input(f"  ⚠️  Diretório {destino} já existe. Sobrescrever? (s/N): ")
        if resp.lower() != "s":
            print("  Cancelado.")
            return
        shutil.rmtree(destino)

    # Placeholders para substituição nos templates
    replacements = {
        "{{SLUG}}": slug,
        "{{TITULO}}": titulo,
        "{{TITULO_UPPER}}": titulo.upper(),
        "{{PRECO}}": "R$ 97",
        "{{PRECO_CORE}}": "97",
        "{{PRECO_TRIPWIRE}}": "37",
        "{{PRECO_OBRA_COMPLETA}}": "297",
        "{{DESCRICAO}}": f"Livro completo sobre {titulo}",
        "{{DESCRICAO_LONGA}}": f"Obra completa gerada pela Fábrica Agêntica de Publicações sobre {titulo}",
        "{{AUTOR}}": "Fábrica Agêntica",
        "{{EMAIL_CONTATO}}": f"contato@{slug[:20]}.com.br",
        "{{DATA}}": datetime.now().strftime("%Y-%m-%d"),
        "{{ANO}}": str(datetime.now().year),
    }

    # 1. Copiar template completo
    print("  [1/6] Copiando estrutura de templates...")
    copiar_template(TEMPLATE_DIR, destino, replacements)

    # 2. Gerar manifesto
    print("  [2/6] Gerando manifesto...")
    manifesto = gerar_manifesto(slug, titulo, obra_info, tipo)
    manifesto_path = destino / "manifesto.json"
    with open(manifesto_path, "w", encoding="utf-8") as f:
        json.dump(manifesto, f, indent=2, ensure_ascii=False)

    # 3. Copiar conteúdo da obra (se existir)
    if obra_info.get("path"):
        print("  [3/6] Copiando conteúdo da obra...")
        obra_dest = destino / "conteudo"
        obra_dest.mkdir(exist_ok=True)
        obra_src = Path(obra_info["path"])
        for item in obra_src.glob("*.md"):
            shutil.copy2(item, obra_dest / item.name)
        # Copiar artes se existirem
        artes_src = obra_src / "artes"
        if artes_src.exists():
            artes_dest = destino / "frontend" / "public" / "artes"
            artes_dest.mkdir(parents=True, exist_ok=True)
            for item in artes_src.iterdir():
                if item.suffix in [".png", ".jpg", ".jpeg", ".webp", ".svg"]:
                    shutil.copy2(item, artes_dest / item.name)
    else:
        print("  [3/6] Obra não encontrada localmente (pode ter sido gerada em outro diretório)")

    # 4. Inicializar banco de dados
    print("  [4/6] Inicializando banco de dados...")
    db_dir = destino / "database"
    schema_file = db_dir / "schema.sql"
    db_file = db_dir / "maquina.db"
    if schema_file.exists():
        try:
            import sqlite3
            conn = sqlite3.connect(str(db_file))
            conn.executescript(schema_file.read_text(encoding="utf-8"))
            seed_file = db_dir / "seed.sql"
            if seed_file.exists():
                conn.executescript(seed_file.read_text(encoding="utf-8"))
            conn.close()
            print(f"    ✅ Banco criado: {db_file}")
        except Exception as e:
            print(f"    ⚠️  Erro ao criar banco: {e}")

    # 5. Gerar .mcp.json
    print("  [5/6] Gerando .mcp.json...")
    mcp_config = {
        "mcpServers": {
            "db_state": {
                "command": "node",
                "args": [
                    str(BASE_DIR / ".claude" / "mcp-servers" / "deps" / "node_modules" / "mcp-server-sqlite-npx" / "dist" / "index.js"),
                    str(destino / "database" / "maquina.db"),
                ],
            },
            "file_writer": {
                "command": "node",
                "args": [
                    str(BASE_DIR / ".claude" / "mcp-servers" / "deps" / "node_modules" / "@modelcontextprotocol" / "server-filesystem" / "dist" / "index.js"),
                    str(destino),
                ],
            },
        }
    }
    mcp_path = destino / ".mcp.json"
    with open(mcp_path, "w", encoding="utf-8") as f:
        json.dump(mcp_config, f, indent=2, ensure_ascii=False)

    # 6. Resumo
    print("  [6/6] Gerando resumo...")
    total_files = sum(1 for _ in destino.rglob("*") if _.is_file())
    print(f"\n{'='*60}")
    print(f"  ✅ MÁQUINA CRIADA COM SUCESSO!")
    print(f"  📁 {destino}")
    print(f"  📄 {total_files} arquivos gerados")
    print(f"\n  PRÓXIMOS PASSOS:")
    print(f"  1. cd {destino}")
    print(f"  2. Revisar config/*.json (produtos, funis, personas)")
    print(f"  3. Configurar .env (copiar de .env.example)")
    print(f"  4. cd frontend && npm install && npm run dev")
    print(f"  5. cd backend && pip install -r requirements.txt && uvicorn app.main:app")
    print(f"  6. Deploy: bash scripts/deploy.sh")
    print(f"{'='*60}\n")

    return destino


def main():
    if len(sys.argv) < 2:
        print("Uso: python scripts/criar-maquina-vendas.py <slug> [--tipo completo|parcial|landing|backend]")
        print("\nExemplo:")
        print("  python scripts/criar-maquina-vendas.py observabilidade-sistemas-distribuidos")
        sys.exit(1)

    slug = sys.argv[1]
    tipo = "completo"

    if "--tipo" in sys.argv:
        idx = sys.argv.index("--tipo")
        if idx + 1 < len(sys.argv):
            tipo = sys.argv[idx + 1]

    criar_maquina(slug, tipo)


if __name__ == "__main__":
    main()
