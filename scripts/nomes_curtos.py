#!/usr/bin/env python3
"""
V5.1 — Nomenclatura curta de pastas e artefatos.

Motivacao: os nomes da V5 ("ai-driven-development-do-zero-ao-deploy-v2--lm-01-
armadilhas", repetido na pasta E no arquivo) produziam caminhos de ~197
caracteres. O MAX_PATH do Windows e 260: qualquer copia para uma pasta mais
funda, um zip ou um OneDrive quebrava a abertura do arquivo.

Convencao:
    output/<raiz>/<codigo-obra>/<prefixo>-<seq>-<nome>/<prefixo>-<seq>-<nome>.<ext>

    codigo-obra   ate 2 palavras significativas da obra-mae (<= 16 chars)
    prefixo       codigo curto do tipo (lm, pbk, dck, eml)
    seq           1, 2, 3... (1 quando o tipo e unico por obra)
    nome          ate 3 palavras separadas por "-"

Exemplo:
    output/lead-magnets/ai-driven/lm-1-armadilhas/lm-1-armadilhas.pdf   (~60)
    contra
    output/lead-magnets/ai-driven-development-do-zero-ao-deploy-v2--lm-01-armadilhas/
        ai-driven-development-do-zero-ao-deploy-v2--lm-01-armadilhas.pdf (~120)

Escopo: vale para os tipos da V5 (playbook, lead-magnet, deck, emails). Artigos e
e-books mantem a nomenclatura V4 — ja existem artefatos compilados no disco e
renomea-los os deixaria orfaos.
"""

import re
import sys
import unicodedata
from pathlib import Path

DIR_PROJETO = Path(__file__).resolve().parent.parent

MAX_PALAVRAS_NOME = 3
MAX_CHARS_CODIGO = 16
MAX_CHARS_PALAVRA = 10
MAX_CHARS_NOME = 26

# Preposicoes/artigos nao carregam identidade e so gastam caracteres
IRRELEVANTES = {
    "a", "o", "as", "os", "e", "de", "da", "do", "das", "dos", "em", "no", "na",
    "nos", "nas", "ao", "aos", "com", "por", "para", "um", "uma", "the", "of",
    "to", "and", "zero", "v1", "v2", "v3", "v4", "v5",
}


def _sem_acento(texto):
    texto = unicodedata.normalize("NFKD", texto or "")
    return "".join(c for c in texto if not unicodedata.combining(c))


def palavras(texto):
    """Palavras significativas, em minusculas e sem acento."""
    bruto = re.split(r"[^A-Za-z0-9]+", _sem_acento(texto or "").lower())
    return [p for p in bruto if p and p not in IRRELEVANTES]


def codigo_obra(slug_ou_titulo, maximo=MAX_CHARS_CODIGO):
    """Codigo curto e estavel da obra-mae: ate 2 palavras significativas.

    'ai-driven-development-do-zero-ao-deploy-v2' -> 'ai-driven'
    'sistemas-agenticos'                         -> 'sistemas-agentic'
    """
    if not palavras(slug_ou_titulo):
        return "obra"
    return nome_curto(slug_ou_titulo, max_palavras=2, maximo=maximo)


def nome_curto(texto, max_palavras=MAX_PALAVRAS_NOME, maximo=MAX_CHARS_NOME):
    """Ate 3 palavras significativas separadas por '-'.

    Corta palavras INTEIRAS, nunca no meio: 'ai-driven-developmen' e um nome
    quebrado, 'ai-driven' nao."""
    ps = palavras(texto)[:max_palavras]
    if not ps:
        return "material"
    escolhidas = []
    for p in ps:
        candidato = "-".join(escolhidas + [p])
        if escolhidas and len(candidato) > maximo:
            break
        escolhidas.append(p)
    return "-".join(escolhidas)[:maximo].rstrip("-")


def codigos_unicos(nomes, maximo=MAX_CHARS_CODIGO):
    """Codigos curtos GARANTIDAMENTE unicos para um conjunto de nomes.

    `codigo_obra` sozinho colide: "ai-driven-development" (o TCC) e
    "ai-driven-development-do-zero-ao-deploy-v2" (o livro) viram ambos
    "ai-driven" — e um pacote sobrescrevia o do outro silenciosamente. Ao
    detectar colisao, estende com mais uma palavra significativa; se ainda
    colidir, acrescenta um sufixo numerico estavel (ordem alfabetica do nome
    completo, para o resultado nao depender da ordem de varredura)."""
    resultado, usados = {}, {}
    for nome in sorted(nomes):
        base = codigo_obra(nome, maximo=maximo)
        candidato = base
        if candidato in usados:
            # 2a tentativa: mais uma palavra
            estendido = nome_curto(nome, max_palavras=3, maximo=maximo + 10)
            candidato = estendido if estendido not in usados else base
        if candidato in usados:
            n = 2
            while f"{base}-{n}" in usados:
                n += 1
            candidato = f"{base}-{n}"
        usados[candidato] = nome
        resultado[nome] = candidato
    return resultado


def nome_material(prefixo, sequencia, nome):
    """'lm', 1, 'armadilhas' -> 'lm-1-armadilhas'."""
    return f"{prefixo}-{int(sequencia)}-{nome_curto(nome)}"


def caminho_material(raiz_output, codigo, nome_do_material):
    """Caminho RELATIVO a output/: '<raiz>/<codigo>/<material>'."""
    return f"{raiz_output}/{codigo}/{nome_do_material}"


def migrar_prefixo_underscore(caminho_novo):
    """Renomeia o vizinho legado com prefixo "_" para o nome novo, se existir.

    Nenhum arquivo ou pasta gerado pela fabrica usa prefixo "_": em varios
    contextos (glob de shell, listagem de nuvem, empacotamento) ele e tratado
    como oculto ou interno. A migracao e automatica e idempotente — sem ela,
    perder `_series.json` faria as capas re-sortearem a cor da colecao.

    Devolve True quando migrou de fato."""
    caminho_novo = Path(caminho_novo)
    if caminho_novo.exists():
        return False
    # Tenta "_<nome>" e tambem a variante com "_" no lugar do "-": alguns nomes
    # trocaram o separador junto com o prefixo (_pool_estado -> pool-estado).
    candidatos = [
        caminho_novo.with_name("_" + caminho_novo.name),
        caminho_novo.with_name("_" + caminho_novo.name.replace("-", "_")),
    ]
    for legado in candidatos:
        if legado.exists():
            caminho_novo.parent.mkdir(parents=True, exist_ok=True)
            legado.rename(caminho_novo)
            return True
    return False


def excede_max_path(caminho, folga=40):
    """True quando o caminho absoluto se aproxima do MAX_PATH do Windows.

    A folga cobre o que vem depois: copia para `distribuicao/`, compactacao,
    sincronizacao em nuvem."""
    return len(str(Path(caminho).resolve())) + folga > 260


def diagnosticar(caminho):
    absoluto = str(Path(caminho).resolve())
    return {
        "caminho": absoluto,
        "chars": len(absoluto),
        "limite_windows": 260,
        "arriscado": excede_max_path(caminho),
    }


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Nomenclatura curta (V5.1)")
    ap.add_argument("texto", nargs="?", help="slug ou titulo da obra")
    ap.add_argument("--codigo", action="store_true")
    ap.add_argument("--nome", action="store_true")
    ap.add_argument("--medir", default=None, help="mede um caminho contra o MAX_PATH")
    args = ap.parse_args()

    if args.medir:
        d = diagnosticar(args.medir)
        marca = "ARRISCADO" if d["arriscado"] else "OK"
        print(f"[{marca}] {d['chars']} chars (limite {d['limite_windows']})")
        print(d["caminho"])
        return 1 if d["arriscado"] else 0

    if not args.texto:
        print("[ERRO] informe um texto ou use --medir")
        return 1
    if args.nome:
        print(nome_curto(args.texto))
    else:
        print(codigo_obra(args.texto))
    return 0


if __name__ == "__main__":
    sys.exit(main())
