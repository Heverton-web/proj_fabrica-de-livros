#!/usr/bin/env python3
"""
Banco de nichos declarativo (V5.3) — personalização determinística da
máquina de vendas por segmento.

Hoje "personalizar por nicho" é 100% delegado a um agente/humano livre — o
script só imprime a instrução e checa reativamente via grep (regra 12). Este
script aplica um nicho de `config/nichos/<segmento>.json` (termos, persona,
produto-pilar, hashtags) nos pontos concretos que hoje nascem com copy
genérica ("Autor Digital", "centenas de pessoas"): `config/produtos.json`,
`config/funis.json`, `config/canais.json`, `config/personas.json` (nova
persona prepend, as antigas ficam `ativo: false` para referência) e as 3
páginas de frontend que citam "centenas de pessoas" literalmente.

Nunca substitui a frase de gancho final por conta própria — cobre o
esqueleto (termos/estrutura/CTA), não a copy persuasiva de verdade. O que
sobrar de genérico após aplicar é reportado para reescrita manual/LLM.

Uso:
    python scripts/personalizar-nicho.py <slug-da-obra>                # auto: casa por vocabulário
    python scripts/personalizar-nicho.py <slug-da-obra> --nicho engenharia-de-software
    python scripts/personalizar-nicho.py <slug-da-obra> --listar-nichos
"""

import argparse
import json
import sys
from pathlib import Path

import tipos_obra as TO
from tipos_obra import console_utf8

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"
DIR_NICHOS = DIR_PROJETO / "config" / "nichos"

MARCADOR_PRODUTO = "Autor Digital"
MARCADOR_PROVA_SOCIAL = "centenas de pessoas"

# Mesma resolução de hub usada por `criar-maquina-vendas.dir_maquina` — cópia
# mínima deliberada (script hifenizado não é importado como módulo).
_RAIZES_ESTRUTURAIS = {
    "livros", "tccs", "ebooks", "artigos", "playbooks", "lead-magnets",
    "decks", "emails",
}


def _hub_da_obra(slug):
    for parte in str(slug).replace("\\", "/").split("/"):
        if parte and parte not in _RAIZES_ESTRUTURAIS:
            return parte
    return Path(str(slug).replace("\\", "/")).name


def dir_maquina(slug, base=None):
    base = Path(base) if base is not None else DIR_OUTPUT
    return base / _hub_da_obra(slug) / "maquina"


def vocabulario_da_obra(slug, base=None):
    caminho = TO.dir_obra(slug, base or DIR_OUTPUT) / "sumario_macro.json"
    if not caminho.exists():
        return []
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    return [v for v in (dados.get("motivo_condutor") or {}).get("vocabulario") or [] if v]


def carregar_nichos(dir_nichos=None):
    """[nicho_dict] de config/nichos/*.json. Nunca lança se o diretório não existir."""
    dir_nichos = Path(dir_nichos) if dir_nichos else DIR_NICHOS
    if not dir_nichos.exists():
        return []
    nichos = []
    for arq in sorted(dir_nichos.glob("*.json")):
        nichos.append(json.loads(arq.read_text(encoding="utf-8")))
    return nichos


def melhor_nicho(vocabulario_obra, nichos):
    """Nicho com maior sobreposição de termos com o vocabulário condutor da
    obra. None se nenhum nicho tiver sobreposição (nunca "chuta" um nicho
    sem relação — melhor ficar sem personalização automática do que aplicar
    a errada)."""
    if not vocabulario_obra or not nichos:
        return None
    termos_obra = {v.lower() for v in vocabulario_obra}
    melhor, maior_score = None, 0
    for nicho in nichos:
        termos_nicho = {t.lower() for t in nicho.get("termos_match", [])}
        score = len(termos_obra & termos_nicho)
        if score > maior_score:
            melhor, maior_score = nicho, score
    return melhor


def _substituir_no_arquivo(caminho, de, para):
    """Substitui `de` por `para` no arquivo; retorna True se alterou algo."""
    if not caminho.exists():
        return False
    texto = caminho.read_text(encoding="utf-8")
    if de not in texto:
        return False
    caminho.write_text(texto.replace(de, para), encoding="utf-8")
    return True


def _prepend_persona(caminho_personas, persona):
    """Adiciona a persona do nicho no topo de personas.json; desativa
    (ativo=false) as personas genéricas do template — nunca as remove."""
    if not caminho_personas.exists():
        return False
    dados = json.loads(caminho_personas.read_text(encoding="utf-8"))
    lista = dados.get("personas", [])
    for p in lista:
        p["ativo"] = False
    nova = {
        "slug": persona.get("nome", "").lower().replace(" ", "-"),
        "nome": persona.get("nome", ""),
        "descricao": persona.get("descricao", ""),
        "dor_principal": persona.get("dor_principal", ""),
        "desejo_principal": persona.get("desejo_principal", ""),
        "objecoes": persona.get("objecoes", []),
        "gatilhos": [],
        "canais_preferidos": persona.get("canais_preferidos", []),
        "tom_comunicacao": persona.get("tom_comunicacao", ""),
        "ativo": True,
    }
    dados["personas"] = [nova] + lista
    caminho_personas.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
    return True


def _adicionar_hashtags(caminho_canais, hashtags):
    if not caminho_canais.exists() or not hashtags:
        return False
    dados = json.loads(caminho_canais.read_text(encoding="utf-8"))
    instagram = dados.get("instagram", {})
    atuais = instagram.get("hashtags", [])
    novas = [h for h in hashtags if h not in atuais]
    if not novas:
        return False
    instagram["hashtags"] = atuais + novas
    caminho_canais.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
    return True


def aplicar_nicho(destino, nicho):
    """Aplica o nicho na máquina em `destino`. Retorna [arquivos alterados]."""
    destino = Path(destino)
    alterados = []

    nome_produto = nicho.get("nome_produto_pilar") or ""
    prova_social = f"centenas de {nicho.get('publico')}" if nicho.get("publico") else ""

    if nome_produto:
        for rel in ("config/produtos.json", "config/funis.json"):
            if _substituir_no_arquivo(destino / rel, MARCADOR_PRODUTO, nome_produto):
                alterados.append(rel)

    if prova_social:
        for rel in ("frontend/app/captura/page.tsx", "frontend/app/layout.tsx",
                    "frontend/components/Hero.tsx"):
            if _substituir_no_arquivo(destino / rel, MARCADOR_PROVA_SOCIAL, prova_social):
                alterados.append(rel)

    if nicho.get("persona") and _prepend_persona(destino / "config" / "personas.json", nicho["persona"]):
        alterados.append("config/personas.json")

    if _adicionar_hashtags(destino / "config" / "canais.json", nicho.get("hashtags", [])):
        alterados.append("config/canais.json")

    return alterados


def restantes_genericos(destino):
    """O que ainda ficou genérico após aplicar o nicho (para LLM/manual)."""
    destino = Path(destino)
    achados = []
    for rel in ("config/produtos.json", "config/funis.json",
                "frontend/app/captura/page.tsx", "frontend/app/layout.tsx",
                "frontend/components/Hero.tsx"):
        caminho = destino / rel
        if not caminho.exists():
            continue
        texto = caminho.read_text(encoding="utf-8", errors="ignore")
        if MARCADOR_PRODUTO in texto or MARCADOR_PROVA_SOCIAL in texto:
            achados.append(rel)
    return achados


def main():
    console_utf8()
    ap = argparse.ArgumentParser(description="Aplica um nicho do banco declarativo na máquina de vendas")
    ap.add_argument("slug", nargs="?", help="slug da obra (resolve a máquina via hub)")
    ap.add_argument("--nicho", help="segmento a forçar (default: casa por vocabulário da obra)")
    ap.add_argument("--listar-nichos", action="store_true", help="lista os nichos do banco e sai")
    args = ap.parse_args()

    nichos = carregar_nichos()

    if args.listar_nichos:
        for n in nichos:
            print(f"{n['segmento']}: {n.get('rotulo', '')}")
        return 0

    if not args.slug:
        ap.error("informe o slug da obra ou use --listar-nichos")

    nicho = None
    if args.nicho:
        nicho = next((n for n in nichos if n["segmento"] == args.nicho), None)
        if nicho is None:
            print(f"[personalizar-nicho] nicho '{args.nicho}' não encontrado em config/nichos/")
            return 1
    else:
        vocabulario = vocabulario_da_obra(args.slug)
        nicho = melhor_nicho(vocabulario, nichos)
        if nicho is None:
            print("[personalizar-nicho] nenhum nicho do banco casou com o vocabulário da obra "
                  "— personalize manualmente ou adicione um nicho em config/nichos/")
            return 1
        print(f"[personalizar-nicho] nicho casado automaticamente: {nicho['segmento']}")

    destino = dir_maquina(args.slug)
    if not destino.exists():
        print(f"[personalizar-nicho] máquina não encontrada em {destino} — rode /criar-maquina antes")
        return 1

    alterados = aplicar_nicho(destino, nicho)
    for a in alterados:
        print(f"[personalizar-nicho] atualizado: {a}")

    restantes = restantes_genericos(destino)
    if restantes:
        print("[personalizar-nicho] ainda genérico (revisar manualmente/LLM):")
        for r in restantes:
            print(f"  - {r}")
    else:
        print("[personalizar-nicho] nenhum marcador genérico restante nos pontos cobertos pelo banco")
    return 0


if __name__ == "__main__":
    sys.exit(main())
