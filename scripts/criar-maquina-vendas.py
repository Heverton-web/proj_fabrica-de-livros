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

import tipos_obra as TO

BASE_DIR = Path(__file__).parent.parent
TEMPLATE_DIR = BASE_DIR / "templates" / "maquina"

# Regra 1:1 — 1 máquina por COLEÇÃO, em output/<slug-colecao>/maquina (V5.3).
# Caminhos de output resolvem via tipos_obra.DIR_OUTPUT (redirecionável nos
# testes); nada vive mais em marketing/maquinas (raiz, caminho morto).
_RAIZES_ESTRUTURAIS = frozenset(
    {TO.raiz_output(t) for t in TO.tipos_validos()}
    | {"marketing", "distribuicao", "colecoes", "campanhas"}
)


def _hub_da_obra(slug):
    """Hub da coleção da obra = 1º segmento do slug que não seja raiz estrutural.

    'livros/ia-agentica-desbloqueada' -> 'ia-agentica-desbloqueada';
    'obra-teste' (layout plano)       -> 'obra-teste' (obra é sua própria coleção).
    """
    for parte in str(slug).replace("\\", "/").split("/"):
        if parte and parte not in _RAIZES_ESTRUTURAIS:
            return parte
    return Path(str(slug).replace("\\", "/")).name


def dir_maquina(slug, base=None):
    """Destino canônico da máquina: output/<slug-colecao>/maquina."""
    base = Path(base) if base is not None else TO.DIR_OUTPUT
    return base / _hub_da_obra(slug) / "maquina"

_TIPOS_FLAT = ("livros", "tccs", "ebooks", "artigos", "playbooks", "lead-magnets", "decks")


def slug_para_titulo(slug: str) -> str:
    return slug.replace("-", " ").replace("_", " ").title()


def _ler_json(caminho, padrao=None):
    """Lê JSON com tolerância: arquivo ausente ou inválido vira `padrao`."""
    if caminho.exists():
        try:
            return json.loads(caminho.read_text(encoding="utf-8"))
        except ValueError:
            return padrao if padrao is not None else {}
    return padrao if padrao is not None else {}


def verificar_obra_existe(slug: str) -> dict:
    """Verifica se a obra existe e retorna seus metadados (série-aware).

    Aceita slug no formato atual (`livros/<obra>`) e no flat legado (`<obra>`).
    Resolve via tipos_obra.dir_obra (output/<obra>/<tipo>/...) com fallback
    para o layout plano antigo (output/<tipo>/<slug>).
    """
    # 1) Resolução série-aware (layout canônico desde V5.1)
    try:
        d = TO.dir_obra(slug, TO.DIR_OUTPUT)
    except Exception:
        d = None
    if d is not None and d.exists():
        return _montar_obra_info(d, slug)
    # 2) Fallback flat legado
    slug_limpo = Path(str(slug).replace("\\", "/")).name
    for d in [TO.DIR_OUTPUT / t / slug_limpo for t in _TIPOS_FLAT]:
        if d.exists():
            return _montar_obra_info(d, slug)
    return {}


def _montar_obra_info(d: Path, slug: str) -> dict:
    """Lê config_obra.json do dir da obra (single-book: sobe para <obra>/livros)."""
    if not (d / "config_obra.json").exists() and (d / "livros").exists():
        d = d / "livros"
    meta = {}
    meta_file = d / "config_obra.json"
    if meta_file.exists():
        with open(meta_file, encoding="utf-8") as f:
            meta = json.load(f)
    return {"path": str(d), "tipo": _tipo_da_obra(d, slug), "meta": meta}


def _tipo_da_obra(d: Path, slug: str) -> str:
    """Deriva o tipo da obra do slug (ex.: 'livros/...' -> 'livros') ou do dir."""
    partes = str(slug).replace("\\", "/").split("/")
    if partes and partes[0] in _TIPOS_FLAT:
        return partes[0]
    for cand in (d.name, d.parent.name):
        if cand in _TIPOS_FLAT:
            return cand
    return "livros"


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


def _validar_pos_replace(destino: Path) -> list:
    """Valida se placeholders foram substituidos corretamente (GAP 3).

    Retorna lista de problemas encontrados. Lista vazia = tudo OK.
    """
    problemas = []
    padroes_genericos = [
        "Autor Digital",
        "centenas de pessoas",
        "{{SLUG}}",
        "{{TITULO}}",
        "{{PRECO}}",
        "{{EMAIL_CONTATO}}",
    ]
    # Arquivos para validar (frontend apenas)
    arquivos_validar = []
    frontend = destino / "frontend"
    if frontend.exists():
        for ext in ("*.tsx", "*.ts", "*.jsx", "*.js", "*.html"):
            arquivos_validar.extend(frontend.rglob(ext))
    for arq in arquivos_validar:
        try:
            conteudo = arq.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for padrao in padroes_genericos:
            if padrao in conteudo:
                problemas.append(f"{arq.relative_to(destino)}: contem '{padrao}'")
    return problemas


def _hex_para_rgb(hex_cor):
    """Converte hex (#rrggbb) para tuple (r, g, b)."""
    hex_cor = str(hex_cor or "").strip().lstrip("#")
    if len(hex_cor) != 6 or not all(c in "0123456789abcdefABCDEF" for c in hex_cor):
        return (59, 130, 246)  # fallback azul
    return tuple(int(hex_cor[i:i + 2], 16) for i in (0, 2, 4))


def _gerar_shades(hex_cor):
    """Gera 10 shades (50-950) a partir de uma cor hex."""
    r, g, b = _hex_para_rgb(hex_cor)
    shades = {}
    # Shades 50-400 (mais claros)
    for i, pct in enumerate([0.95, 0.90, 0.80, 0.65, 0.50]):
        shade = 50 + i * 100
        sr = int(r + (255 - r) * pct)
        sg = int(g + (255 - g) * pct)
        sb = int(b + (255 - b) * pct)
        shades[shade] = f"#{sr:02x}{sg:02x}{sb:02x}"
    # Shade 500 (original)
    shades[500] = f"#{r:02x}{g:02x}{b:02x}"
    # Shades 600-900 (mais escuros)
    for i, pct in enumerate([0.15, 0.30, 0.45, 0.60]):
        shade = 600 + i * 100
        sr = int(r * (1 - pct))
        sg = int(g * (1 - pct))
        sb = int(b * (1 - pct))
        shades[shade] = f"#{sr:02x}{sg:02x}{sb:02x}"
    return shades


def _aplicar_identidade_visual(destino: Path, cor_acento: str):
    """Propaga cor_acento do manifesto para tailwind.config.ts (GAP 5)."""
    tailwind_path = destino / "frontend" / "tailwind.config.ts"
    if not tailwind_path.exists():
        return
    try:
        content = tailwind_path.read_text(encoding="utf-8")
        shades = _gerar_shades(cor_acento)
        # Gerar bloco de cores primary baseado na cor_acento
        primary_lines = []
        for shade in sorted(shades.keys()):
            primary_lines.append(f'          {shade}: "{shades[shade]}"')
        primary_block = "primary: {\n" + ",\n".join(primary_lines) + ",\n        }"
        # Substituir o bloco primary existente
        import re
        pattern = r"primary:\s*\{[^}]+\}"
        replacement = "primary: {\n" + ",\n".join(primary_lines) + ",\n        }"
        content = re.sub(pattern, replacement, content)
        tailwind_path.write_text(content, encoding="utf-8")
        print(f"    ✅ Identidade visual propagada: cor {cor_acento}")
    except Exception as e:
        print(f"    ⚠️  Erro ao propagar identidade visual: {e}")


def gerar_manifesto(slug: str, titulo: str, obra_info: dict, tipo: str,
                    snapshot=None) -> dict:
    """Gera manifesto da máquina de vendas (regra 1:1 por coleção)."""
    return {
        "id": f"mv-{datetime.now().strftime('%Y%m%d')}-{slug}",
        "slug": slug,
        "titulo": titulo,
        "obra_origem": obra_info.get("path", ""),
        "tipo_obra": obra_info.get("tipo", "desconhecido"),
        "tipo_maquina": tipo,
        "criada_em": datetime.now().isoformat(),
        "status": "criada",
        "colecao": _hub_da_obra(slug),
        "maquina_em": f"output/{_hub_da_obra(slug)}/maquina",
        "campanhas": {
            "snapshot": bool(snapshot),
            "atualizado_em": (snapshot or {}).get("atualizado_em", ""),
            "material_ancora": Path(str(slug).replace("\\", "/")).name,
        },
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


def vincular_campanhas(destino: Path, slug: str, base=None):
    """Snapshot de output/<hub>/campanhas -> maquina/campanhas + snapshot.json.

    A máquina deplora fora do repo da fábrica (VPS/Vercel), então recebe cópia
    integral — campanha é fonte, máquina é consumidora. Sem campanhas no hub
    retorna None (máquina funciona; o snapshot entra quando a campanha existir).
    """
    base = Path(base) if base is not None else TO.DIR_OUTPUT
    hub = _hub_da_obra(slug)
    origem = base / hub / "campanhas"
    if not origem.is_dir():
        print("    (sem campanhas no hub — máquina sem snapshot de campanhas)")
        return None
    snap_dest = destino / "campanhas"
    if snap_dest.exists():
        shutil.rmtree(snap_dest)
    shutil.copytree(origem, snap_dest)
    estado = _ler_json(origem / "campanha.json")
    snapshot = {
        "origem": str(origem.relative_to(base)).replace("\\", "/"),
        "atualizado_em": estado.get("atualizado_em", ""),
        "materiais": len([p for p in origem.iterdir() if p.is_dir()]),
        "copiado_em": datetime.now().isoformat(),
    }
    (snap_dest / "snapshot.json").write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"    ✅ Snapshot de campanhas: maquina/campanhas/ "
          f"({snapshot['materiais']} material(is), campanha de "
          f"{snapshot['atualizado_em'] or 'data desconhecida'})")
    return snapshot


def criar_maquina(slug: str, tipo: str = "completo"):
    """Função principal: cria a máquina de vendas."""
    # UTF-8 no Windows (cp1252 quebra emojis do banner) — não depender só do main()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    titulo = slug_para_titulo(slug)
    obra_info = verificar_obra_existe(slug)
    destino = dir_maquina(slug)
    hub = _hub_da_obra(slug)

    print(f"\n{'='*60}")
    print(f"  CRIANDO MÁQUINA DE VENDAS: {titulo}")
    print(f"  Tipo: {tipo}")
    print(f"  Coleção (hub): {hub}")
    print(f"  Destino: {destino}")
    print(f"{'='*60}\n")

    if destino.exists():
        # Regra 1:1 — a máquina do hub pertence a UMA obra. Outra obra da mesma
        # coleção NÃO pode sobrescrever; mesma obra segue com confirmação.
        man_existente = _ler_json(destino / "manifesto.json")
        obra_anterior = man_existente.get("obra_origem", "")
        obra_atual = obra_info.get("path", "")
        if obra_anterior and obra_atual and obra_anterior != obra_atual:
            print(f"  ⛔ Regra 1:1 — a coleção '{hub}' já tem máquina de outra obra:")
            print(f"     existente: {obra_anterior}")
            print(f"     solicitada: {obra_atual}")
            print(f"  (1 máquina por coleção em output/<slug-colecao>/maquina — "
                  f"use outra coleção ou remova a existente)")
            return None
        resp = input(f"  ⚠️  Diretório {destino} já existe. Sobrescrever? (s/N): ")
        if resp.lower() != "s":
            print("  Cancelado.")
            return None
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
    print("  [1/7] Copiando estrutura de templates...")
    copiar_template(TEMPLATE_DIR, destino, replacements)

    # 1.1 Validar se placeholders foram substituidos (GAP 3)
    problemas = _validar_pos_replace(destino)
    if problemas:
        print(f"  ⚠️  [GAP 3] Problemas de personalizacao encontrados:")
        for p in problemas[:5]:  # Mostrar max 5
            print(f"     - {p}")
        if len(problemas) > 5:
            print(f"     ... e mais {len(problemas) - 5} problemas")
        print("  (A maquina pode ter copy generica - revise manualmente)")

    # 1.2 Propagar identidade visual do manifesto (GAP 5)
    config_obra = obra_info.get("meta", {})
    cor_acento = config_obra.get("cor_acento")
    if not cor_acento:
        # Tentar resolver via series_capa
        try:
            from series_capa import resolver_cor
            from tipos_obra import resolver_serie_key
            serie_key = resolver_serie_key(config_obra, slug)
            cor_acento = resolver_cor(serie_key, slug)
        except Exception:
            cor_acento = "#3b82f6"  # fallback azul
    _aplicar_identidade_visual(destino, cor_acento)

    # 2. Copiar conteúdo da obra (se existir)
    if obra_info.get("path"):
        print("  [2/7] Copiando conteúdo da obra...")
        obra_dest = destino / "conteudo"
        obra_dest.mkdir(exist_ok=True)
        obra_src = Path(obra_info["path"])
        # Markdown (obra, playbook) + PDF + EPUB
        for pattern in ["*.md", "*.pdf", "*.epub"]:
            for item in obra_src.glob(pattern):
                shutil.copy2(item, obra_dest / item.name)
        # Derivados da mesma coleção também alimentam a máquina.
        # Fonte confiável: manifesto da coleção (output/<obra>/colecoes/<nome>.json)
        # — lista membros reais com slug relativo a output/ (nomenclatura curta V5.1).
        obra_curta = Path(str(slug).replace("\\", "/")).name
        colecao_manifesto = TO.DIR_OUTPUT / obra_curta / "colecoes" / f"{obra_curta}.json"
        if not colecao_manifesto.exists():
            colecao_manifesto = TO.DIR_OUTPUT / "colecoes" / f"{slug}.json"  # fallback flat
        membros_copiados = set()
        if colecao_manifesto.exists():
            try:
                dados_colecao = json.loads(colecao_manifesto.read_text(encoding="utf-8"))
                for membro in dados_colecao.get("membros", []):
                    slug_membro = membro.get("slug", "") if isinstance(membro, dict) else str(membro)
                    if not slug_membro:
                        continue
                    m_dir = TO.DIR_OUTPUT / slug_membro
                    if not m_dir.exists():
                        m_dir = TO.dir_obra(slug_membro, TO.DIR_OUTPUT)
                    if not m_dir.exists():
                        continue
                    artefatos = membro.get("artefatos", []) if isinstance(membro, dict) else []
                    fontes = ([m_dir / a for a in artefatos] if artefatos
                              else list(m_dir.rglob("*")))
                    for item in fontes:
                        if not item.is_file() or item.suffix.lower() not in (".md", ".pdf", ".epub"):
                            continue
                        # Evitar duplicar nomes comuns (ex.: livro_final.md de outro membro)
                        if item.name in membros_copiados:
                            continue
                        membros_copiados.add(item.name)
                        shutil.copy2(item, obra_dest / item.name)
            except (KeyError, TypeError, OSError) as e:
                print(f"    ⚠️  Coleção lida com erro ({e}) — derivados não copiados")
        elif not membros_copiados:
            # Fallback: materiais derivados cujo caminho contém a 1ª palavra do slug
            primeira_palavra = obra_curta.split("-")[0]
            for tipo in ("playbook", "ebook", "deck", "lead-magnet"):
                for slug_material in TO.listar_materiais(tipo, TO.DIR_OUTPUT):
                    if primeira_palavra not in slug_material:
                        continue
                    m_dir = TO.dir_obra(slug_material, TO.DIR_OUTPUT)
                    if not m_dir.exists():
                        continue
                    for item in m_dir.rglob("*"):
                        if not item.is_file() or item.suffix.lower() not in (".md", ".pdf", ".epub"):
                            continue
                        if item.name in membros_copiados:
                            continue
                        membros_copiados.add(item.name)
                        shutil.copy2(item, obra_dest / item.name)
        # Copiar artes se existirem
        artes_src = obra_src / "artes"
        if artes_src.exists():
            artes_dest = destino / "frontend" / "public" / "artes"
            artes_dest.mkdir(parents=True, exist_ok=True)
            for item in artes_src.iterdir():
                if item.suffix in [".png", ".jpg", ".jpeg", ".webp", ".svg"]:
                    shutil.copy2(item, artes_dest / item.name)
        # Capa/imagens alternativas (imagens/ ou capa.*)
        capa_dest = destino / "frontend" / "public" / "artes"
        capa_dest.mkdir(parents=True, exist_ok=True)
        for pat in ("imagens/capa.png", "imagens/capa.jpg", "capa.png", "capa.jpg"):
            f = obra_src / pat
            if f.exists():
                shutil.copy2(f, capa_dest / f.name)
                break
    else:
        print("  [2/7] Obra não encontrada localmente (pode ter sido gerada em outro diretório)")

    # 3. Vincular campanhas da coleção (snapshot) — regra: máquina usa campanhas
    print("  [3/7] Vinculando campanhas da coleção...")
    snapshot = vincular_campanhas(destino, slug)

    # 4. Gerar manifesto (com vínculo de campanhas)
    print("  [4/7] Gerando manifesto...")
    manifesto = gerar_manifesto(slug, titulo, obra_info, tipo, snapshot)
    manifesto_path = destino / "manifesto.json"
    with open(manifesto_path, "w", encoding="utf-8") as f:
        json.dump(manifesto, f, indent=2, ensure_ascii=False)

    # 5. Inicializar banco de dados
    print("  [5/7] Inicializando banco de dados...")
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

    # 6. Gerar .mcp.json
    print("  [6/7] Gerando .mcp.json...")
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

    # 7. Resumo
    print("  [7/7] Gerando resumo...")
    total_files = sum(1 for _ in destino.rglob("*") if _.is_file())
    tem_campanhas = (destino / "campanhas" / "snapshot.json").exists()
    print(f"\n{'='*60}")
    print(f"  ✅ MÁQUINA CRIADA COM SUCESSO!")
    print(f"  📁 {destino}")
    print(f"  📄 {total_files} arquivos gerados")
    if tem_campanhas:
        print(f"  📣 Snapshot de campanhas em maquina/campanhas/ (fonte da copy de divulgação)")
    print(f"\n  PRÓXIMOS PASSOS:")
    print(f"  1. cd {destino}")
    print(f"  2. PERSONALIZAR por nicho: config/*.json (produtos, funis, personas, canais, email)")
    print(f"     + copy do frontend (app/page.tsx, Hero, PricingCard, layout, admin)")
    print(f"     + e-mails (templates/emails/*.html) + README.md")
    print(f"     + campanhas/ (textos, artes e cronogramas da coleção — use o material âncora)")
    print(f"     (o template nasce com copy genérica — substitua pelos termos do nicho)")
    print(f"  3. Configurar .env (copiar de .env.example — inclui BACKEND_URL)")
    print(f"  4. cd frontend && npm install && npm run dev")
    print(f"  5. cd backend && pip install -r requirements.txt && uvicorn app.main:app")
    print(f"  6. Testar /api/checkout: curl -X POST http://localhost:3000/api/checkout ...")
    print(f"  7. Deploy: bash scripts/deploy.sh")
    print(f"{'='*60}\n")

    return destino


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
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
