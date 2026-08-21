#!/usr/bin/env python3
"""
F2 — Gate de COMANDOS/CLI VERIFICADOS (R-CLI-1).

Aplica o protocolo pericial do livro "Tokens Sob Perícia" (hierarquia de fontes
A/B/C + veredito CONFIRMADO/FABRICADO/NÃO_VERIFICÁVEL) a blocos de código/CLI
citados em livros TÉCNICOS (sobre ferramentas, frameworks, DevOps, IA — o
próprio gênero de "Tokens Sob Perícia"). Só roda quando a obra declara
`categoria_tecnica: true` no config_obra.json (escolha do operador na
entrevista `/esbocar`, mesmo padrão de R17 para campanha/máquina) — em
qualquer outra obra, o gate é PULADO sem falhar (exit 0, sem violação).

Motivação (melhorias/21-08-2026-plano-acao-tokens-sob-pericia.md, item A):
o achado central do livro "Tokens Sob Perícia" é que "ferramenta real, sintaxe
fabricada" é o erro mais perigoso, porque o nome familiar desarma a checagem.
Nenhum gate atual da fábrica impede que um PRÓXIMO livro técnico repita esse
mesmo erro — este gate fecha essa lacuna.

Marcação aceita: comentário HTML logo após o fechamento do bloco de código
(só espaço/quebra de linha entre o fechamento e o comentário), na mesma
convenção de classe do dossiê (A/B/C):

    ```bash
    npx ccusage@latest daily
    ```
    <!-- cli-check: fonte=B; confere=true -->

  fonte    = classe da fonte que confirma o comando (A doc oficial do
             fornecedor; B repositório/pacote oficial; C terceiros)
  confere  = true  (sintaxe bate exatamente com a fonte)
             false (não bate — fabricado ou parcialmente correto; PRECISA
                    ser corrigido antes de publicar)

R-CLI-1: nenhum bloco marcado confere=false sobrevive ao --estrito. Bloco SEM
         marcação vira 'nao_verificado' — nunca reprova sozinho (mesma regra
         do livro: ausência de marcação != aprovação), mas aparece no
         relatório como pendência para o revisor-tecnico confirmar antes da
         publicação.

Uso:
    python scripts/validar-comandos-cli.py <slug>
    python scripts/validar-comandos-cli.py <slug> --capitulo 7
    python scripts/validar-comandos-cli.py <slug> --md docs/x.md
    python scripts/validar-comandos-cli.py <slug> --estrito   # exit 1 se falha
    python scripts/validar-comandos-cli.py <slug> --json

Relatório: output/<slug>/validacao/relatorio_comandos_cli.json
"""

import argparse
import json
import re
import sys
from pathlib import Path

from secoes_eita import RE_BLOCO_LING, dividir_secoes

import parametros_obra as PO
import tipos_obra as TO
from tipos_obra import console_utf8

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

# Comentario HTML imediatamente apos o fechamento do bloco de codigo — so
# espaco/quebra de linha entre os dois (nao "acha" uma marcacao distante).
RE_MARCA_CLI = re.compile(
    r"\A[ \t]*\n?[ \t]*<!--\s*cli-check:\s*fonte=([ABC])\s*;\s*confere=(true|false)\s*-->",
    re.IGNORECASE,
)

REGRAS = {
    "R-CLI-1": "bloco de código/CLI marcado confere=false (sintaxe fabricada ou "
               "parcialmente correta) reprova; sem marcação vira pendência, nunca reprova",
}


def _exibir(caminho):
    """Caminho relativo ao projeto quando possivel; absoluto caso contrario
    (mesma tolerancia de minerar-fontes-academicas.py._exibir — necessario
    quando DIR_OUTPUT aponta para fora de DIR_PROJETO, ex.: testes com tmp_path)."""
    try:
        return str(caminho.relative_to(DIR_PROJETO))
    except ValueError:
        return str(caminho)


def obra_e_categoria_tecnica(slug):
    """True quando o config_obra.json da obra declara categoria_tecnica=true.

    Retrocompatível: obras sem o campo (V3/V5 anteriores a este gate) devolvem
    False — o gate so se aplica quando o operador escolhe explicitamente.
    """
    config = PO.carregar_config(slug)
    return bool(config.get("categoria_tecnica", False))


def analisar_capitulo(texto, rotulo):
    """[{'origem','secao','linguagem','status','fonte','trecho'}] por bloco de código."""
    secoes = dividir_secoes(texto)
    blocos = []
    for numero, info in secoes.items():
        corpo = info.get("corpo") or ""
        for m in RE_BLOCO_LING.finditer(corpo):
            linguagem = (m.group(1) or "").lower()
            codigo = m.group(2) or ""
            if linguagem == "mermaid" or not codigo.strip():
                continue  # diagrama, nao comando/CLI

            resto = corpo[m.end():]
            marca = RE_MARCA_CLI.match(resto)
            if marca:
                fonte = marca.group(1).upper()
                confere = marca.group(2).lower() == "true"
                status = "confirmado" if confere else "fabricado"
            else:
                fonte, status = None, "nao_verificado"

            trecho = re.sub(r"\s+", " ", codigo.strip())[:160]
            blocos.append({
                "origem": rotulo, "secao": numero,
                "linguagem": linguagem or "text",
                "status": status, "fonte": fonte, "trecho": trecho,
            })
    return blocos


def main():
    ap = argparse.ArgumentParser(
        description="Gate F2 de comandos/CLI verificados: sintaxe fabricada em livro tecnico")
    ap.add_argument("slug")
    ap.add_argument("--capitulo", help="valida apenas o capitulo N")
    ap.add_argument("--md", help="valida um markdown especifico em vez dos capitulos")
    ap.add_argument("--estrito", action="store_true", help="exit 1 se houver falha")
    ap.add_argument("--json", action="store_true", help="imprime relatorio JSON completo")
    args = ap.parse_args()

    dir_livro = TO.dir_obra(args.slug, DIR_OUTPUT)
    if not dir_livro.exists():
        print(f"[ERRO] Obra nao encontrada: {dir_livro}")
        return 1

    if not obra_e_categoria_tecnica(args.slug):
        print(f"Gate de Comandos/CLI Verificados - {args.slug}")
        print("  [SKIP] categoria_tecnica != true no config_obra.json — gate nao "
              "aplicavel a esta obra (opt-in do operador, ver R-CLI-1).")
        return 0

    alvos = []
    if args.md:
        p = Path(args.md)
        if not p.exists():
            print(f"[ERRO] Arquivo nao encontrado: {p}")
            return 1
        alvos.append((p, p.name))
    else:
        caps = sorted((dir_livro / "capitulos").glob("cap_*.md"),
                      key=lambda p: int(re.search(r"cap_(\d+)", p.stem).group(1)))
        if args.capitulo:
            caps = [c for c in caps
                    if re.search(r"cap_(\d+)", c.stem).group(1).lstrip("0")
                    == str(args.capitulo).lstrip("0")]
        if not caps:
            print(f"[ERRO] Nenhum capitulo encontrado em {dir_livro / 'capitulos'}")
            return 1
        alvos = [(c, c.stem) for c in caps]

    todos = []
    for caminho, rotulo in alvos:
        texto = caminho.read_text(encoding="utf-8", errors="replace")
        todos.extend(analisar_capitulo(texto, rotulo))

    violacoes = [b for b in todos if b["status"] == "fabricado"]
    pendentes = [b for b in todos if b["status"] == "nao_verificado"]
    confirmados = [b for b in todos if b["status"] == "confirmado"]

    por_capitulo = {}
    for b in violacoes:
        por_capitulo.setdefault(b["origem"], 0)
        por_capitulo[b["origem"]] += 1

    relatorio = {
        "slug": args.slug,
        "capitulos": len(alvos),
        "total_blocos": len(todos),
        "confirmados": len(confirmados),
        "fabricados": len(violacoes),
        "nao_verificados": len(pendentes),
        "por_capitulo_com_falha": por_capitulo,
        "regras": REGRAS,
        "violacoes": violacoes,
        "pendentes": pendentes,
    }
    dir_val = dir_livro / "validacao"
    dir_val.mkdir(exist_ok=True)
    (dir_val / "relatorio_comandos_cli.json").write_text(
        json.dumps(relatorio, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Gate de Comandos/CLI Verificados - {args.slug}")
    print(f"  capitulos analisados : {len(alvos)}")
    print(f"  blocos de codigo     : {len(todos)}")
    print(f"    confirmados        : {len(confirmados)}")
    print(f"    fabricados         : {len(violacoes)}")
    print(f"    nao verificados    : {len(pendentes)}")

    if violacoes:
        print("\n[FALHA] Comandos marcados confere=false (sintaxe fabricada):")
        for v in violacoes[:15]:
            print(f"  - {v['origem']} §{v['secao']} ({v['linguagem']}): {v['trecho']}...")
        if len(violacoes) > 15:
            print(f"  ... e mais {len(violacoes) - 15}")
    else:
        print("\n[OK] Nenhum comando marcado como fabricado (confere=false)")

    if pendentes:
        print(f"\n[AVISO] {len(pendentes)} bloco(s) sem marcacao cli-check — "
              "pendente de confirmacao pelo revisor-tecnico (nao bloqueia --estrito).")

    print(f"\nRelatorio: {_exibir(dir_val / 'relatorio_comandos_cli.json')}")

    if args.json:
        print(json.dumps(relatorio, ensure_ascii=False, indent=2))

    if args.estrito and violacoes:
        return 1
    return 0


if __name__ == "__main__":
    console_utf8()
    sys.exit(main())
