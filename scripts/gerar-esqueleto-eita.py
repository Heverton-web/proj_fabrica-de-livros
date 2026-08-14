#!/usr/bin/env python3
"""
Esqueleto EITA-V2 determinístico (7 headers fixos).

Hoje o `redator-eita`/`subagente-redator-capitulo` recria os 7 cabeçalhos
numerados a cada capítulo por conta própria — risco real e já documentado de
heading malformado (sem número, nome divergente) quebrar
`validar-escala.py`/`validar-metricas.py` (que dependem do contrato
`## N. Nome` de `secoes_eita.dividir_secoes`). A estrutura das 7 seções é
100% fixa (`templates/template_eita.md`) — este script grava o esqueleto
pronto; a LLM só escreve o conteúdo dentro de cada seção.

Uso:
    python scripts/gerar-esqueleto-eita.py <slug> <numero_capitulo> --titulo "..."
    python scripts/gerar-esqueleto-eita.py <slug> 3 --titulo "Memória Distribuída" --forcar

Grava: <dir_obra>/capitulos/cap_<numero_capitulo>.md
"""

import argparse
import sys
from pathlib import Path

import tipos_obra as TO
from tipos_obra import console_utf8

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

# (numero, nome oficial, placeholder do que a LLM deve escrever ali)
SECOES = [
    (1, "Introdução",
     "<!-- Contextualize o tema, a ponte com o capítulo anterior (callback "
     "nomeado) e o que o leitor será capaz de fazer. Máximo 2 parágrafos. -->"),
    (2, "Explica",
     "<!-- Desconstrução teórica: causa raiz, mecânica, definições. "
     "Citações [N] obrigatórias para afirmações factuais. -->"),
    (3, "Ilustra",
     "<!-- Analogia do motivo condutor da obra + no mínimo 1 bloco "
     "```mermaid com `%% legenda:` na primeira linha. -->"),
    (4, "Técnica",
     "<!-- Núcleo de valor: código real executável com linguagem declarada, "
     "arquitetura, passos. Mínimo 60% do capítulo. Citações [N] para "
     "técnicas/benchmarks/estatísticas. -->"),
    (5, "Aplica",
     "<!-- Cena de contraste (erro comum vs. prática correta, em 2ª pessoa) "
     "+ cenário corporativo real com métricas de sucesso/fracasso. -->\n\n"
     "### Exercício\n- [ ] _(a completar)_"),
    (6, "Conclusão",
     "<!-- Recapitule os 3 pontos principais em 1 parágrafo, desafio "
     "opcional, ponte para o próximo capítulo. -->"),
    (7, "Referências Bibliográficas",
     "<!-- [N] SOBRENOME, Nome. *Título*. Disponível em: URL. Acesso em: "
     "DD mês. AAAA. Mínimo 3 referências — apenas as citadas [N] no "
     "capítulo, ordem alfabética por título. -->"),
]


def montar_esqueleto(numero_capitulo, titulo_capitulo):
    """Gera o .md com os 7 headers fixos `## N. Nome` (contrato de
    `secoes_eita.dividir_secoes`) + placeholder de conteúdo por seção."""
    linhas = [f"# Capítulo {numero_capitulo}: {titulo_capitulo}", ""]
    for numero, nome, placeholder in SECOES:
        linhas.append(f"## {numero}. {nome}")
        linhas.append("")
        linhas.append(placeholder)
        linhas.append("")
    return "\n".join(linhas).rstrip() + "\n"


def main():
    console_utf8()
    ap = argparse.ArgumentParser(description="Gera o esqueleto EITA-V2 (7 headers fixos) de 1 capítulo")
    ap.add_argument("slug")
    ap.add_argument("numero_capitulo", type=int)
    ap.add_argument("--titulo", required=True, help="título do capítulo")
    ap.add_argument("--forcar", action="store_true", help="sobrescreve cap_<n>.md existente")
    args = ap.parse_args()

    dir_obra = TO.dir_obra(args.slug, DIR_OUTPUT)
    destino = dir_obra / "capitulos" / f"cap_{args.numero_capitulo}.md"

    if destino.exists() and not args.forcar:
        print(f"[gerar-esqueleto-eita] já existe: {destino} (use --forcar para sobrescrever)")
        return 1

    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(montar_esqueleto(args.numero_capitulo, args.titulo), encoding="utf-8")
    print(f"[gerar-esqueleto-eita] gravado {destino} (7 seções EITA-V2, headers fixos)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
