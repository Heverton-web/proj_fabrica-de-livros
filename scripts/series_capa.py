#!/usr/bin/env python3
"""
Padronizacao de capas — resolucao de identidade de cor por serie/colecao.

Uma obra (livro ou ebook) resolve sua "serie_key" nesta ordem:
  1. config_obra.json["serie"]      (colecao declarada pelo operador, /esbocar)
  2. config_obra.json["livro_mae"]  (ebook/artigo derivado herda do livro-mae,
                                      chave gravada por scripts/fatiar-obra.py)
  3. o nome-base do proprio slug    (standalone, ex.: "livros/foo" -> "foo")

A cor de accent de uma serie_key e estavel: na primeira vez que aparece,
escolhe deterministicamente (hash) uma cor da paleta curada e grava no
registro output/series.json (migrado de _series.json); nas proximas vezes,
reusa a cor gravada.

Ver docs/superpowers/specs/2026-08-06-capas-padronizadas-design.md (secao 4).

Uso como biblioteca:
    from series_capa import resolver_serie_key, resolver_cor

Uso como CLI (inspecao/migracao manual):
    python scripts/series_capa.py livros/meu-livro --json
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nomes_curtos import migrar_prefixo_underscore  # noqa: E402
import tipos_obra as TO  # noqa: E402

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"
CAMINHO_REGISTRO = DIR_OUTPUT / "series.json"

# Paleta curada — consolida os hex ja em uso hoje nos scripts de capa anteriores
PALETA_ACCENT = [
    "#2ecc9a", "#58a6ff", "#a855f7", "#f0b429",
    "#37c3d6", "#f0933b", "#e05d5d", "#7c6cf0",
]


def carregar_registro():
    migrar_prefixo_underscore(CAMINHO_REGISTRO)   # _series.json -> series.json
    if CAMINHO_REGISTRO.exists():
        try:
            return json.loads(CAMINHO_REGISTRO.read_text(encoding="utf-8"))
        except ValueError:
            return {}
    return {}


def salvar_registro(registro):
    DIR_OUTPUT.mkdir(parents=True, exist_ok=True)
    CAMINHO_REGISTRO.write_text(
        json.dumps(registro, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def resolver_serie_key(config_obra, slug):
    """config_obra: dict de config_obra.json (ou {} se ausente/nao encontrado)."""
    serie = (config_obra or {}).get("serie")
    if serie:
        return serie
    livro_mae = (config_obra or {}).get("livro_mae")
    if livro_mae:
        return livro_mae
    return Path(slug).name


def _escolher_cor_deterministica(serie_key):
    digest = hashlib.sha1(serie_key.encode("utf-8")).digest()
    return PALETA_ACCENT[digest[0] % len(PALETA_ACCENT)]


def resolver_cor(serie_key, slug=None):
    """Retorna a cor de accent estavel da serie_key, gravando/atualizando o registro."""
    registro = carregar_registro()
    entrada = registro.get(serie_key)
    if entrada is None:
        entrada = {"cor": _escolher_cor_deterministica(serie_key), "membros": []}
    if slug and slug not in entrada["membros"]:
        entrada["membros"].append(slug)
    registro[serie_key] = entrada
    salvar_registro(registro)
    return entrada["cor"]


def _ler_json(caminho):
    if caminho.exists():
        try:
            return json.loads(caminho.read_text(encoding="utf-8"))
        except ValueError:
            return {}
    return {}


def reindexar_membros(base=None):
    """Reconstroi `membros` do registro com os slugs REAIS no disco (HUB).

    Preserva as cores ja gravadas (chave de cada entrada) e remove os membros
    orfaos de layouts antigos (ex.: destinos planos `livros/<slug>` de antes da
    reorg por colecao). Chaves sem material no disco ficam com `membros` vazio —
    a cor permanece reservada para a colecao. Entradas novas (colecao no disco
    sem registro previo) ganham cor deterministica.
    """
    base = Path(base) if base is not None else DIR_OUTPUT
    registro = carregar_registro()

    pares_reais = []  # (serie_key, slug real)
    for tipo in TO.TIPOS:
        for slug in TO.listar_materiais(tipo, base):
            config_obra = _ler_json(TO.dir_obra(slug, base) / "config_obra.json")
            pares_reais.append((resolver_serie_key(config_obra, slug), slug))

    novo = {}
    for serie_key, entrada in registro.items():
        cor = entrada.get("cor") if isinstance(entrada, dict) else None
        membros = sorted({slug for k, slug in pares_reais if k == serie_key})
        novo[serie_key] = {
            "cor": cor or _escolher_cor_deterministica(serie_key),
            "membros": membros,
        }
    chaves_disco = {k for k, _ in pares_reais}
    for serie_key in sorted(chaves_disco - set(novo)):
        novo[serie_key] = {
            "cor": _escolher_cor_deterministica(serie_key),
            "membros": sorted({slug for k, slug in pares_reais
                               if k == serie_key}),
        }
    salvar_registro(novo)
    return novo


def main():
    ap = argparse.ArgumentParser(description="Resolucao de cor de serie por obra")
    ap.add_argument("slug", nargs="?",
                    help="ex.: livros/meu-livro ou ebooks/meu-livro--eb-01-titulo")
    ap.add_argument("--reindexar", action="store_true",
                    help="reconstroi `membros` do registro com os slugs reais "
                         "no disco, preservando as cores (remove orfaos)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.reindexar:
        novo = reindexar_membros()
        total_membros = sum(len(e["membros"]) for e in novo.values())
        print(f"[OK] series.json reindexado: {len(novo)} colecao(ões), "
              f"{total_membros} membro(s) reais no disco")
        if args.json:
            print(json.dumps(novo, ensure_ascii=False, indent=2))
        return 0

    if not args.slug:
        ap.error("informe um slug ou use --reindexar")

    config_obra = _ler_json(TO.dir_obra(args.slug, DIR_OUTPUT) / "config_obra.json")
    serie_key = resolver_serie_key(config_obra, args.slug)
    cor = resolver_cor(serie_key, args.slug)

    if args.json:
        print(json.dumps({"serie_key": serie_key, "cor": cor}, ensure_ascii=False))
    else:
        print(f"serie_key: {serie_key}")
        print(f"cor      : {cor}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
