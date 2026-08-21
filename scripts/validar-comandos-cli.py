#!/usr/bin/env python3
"""
F2 — Gate de COMANDOS/CLI (R-CLI).

Valida blocos de código em capítulos técnicos contra marcações de verificação.
Comandos citados com âncora verificável (comentário HTML `<!-- cli-check: ... -->`)
são classificados por fonte (A/B/C) e veredicto (CONFIRMADO/PARCIALMENTE_CORRETO/FABRICADO/NÃO_VERIFICÁVEL).

Somente ativa para obras com `categoria_tecnica: true` (livros sobre ferramentas/CLIs).

Marcação no capítulo:
    ```bash
    pipx install ai-gateway
    ```
    <!-- cli-check: fonte=B; confere=true -->

Parser extraí:
  - fonte: classificação A/B/C do dossiê
  - confere: true (validado) / false (sabidamente incorreto) / null (não marcado)

Gate mínimo:
  - Nenhum comando com `confere=false` passa em --estrito
  - Comandos sem marcação geram aviso (não reprova)

Relatório: output/<slug>/validacao/relatorio_comandos_cli.json

Uso:
    python scripts/validar-comandos-cli.py <slug>
    python scripts/validar-comandos-cli.py <slug> --estrito
    python scripts/validar-comandos-cli.py <slug> --json
"""

import argparse
import json
import re
import sys
from pathlib import Path

import tipos_obra as TO
from secoes_eita import dividir_secoes
from tipos_obra import console_utf8

RE_CLI_CHECK = re.compile(r'<!--\s*cli-check:\s*fonte=([A-C]);\s*confere=(true|false)\s*-->')
RE_BLOCO_CODIGO = re.compile(r'```(?:bash|sh|python|js|typescript|powershell)?\s*\n(.*?)\n```', re.DOTALL)


def validar_capitulo(arquivo, capitulo_num):
    """Valida comandos em um capítulo; retorna (comandos_marcados, nao_marcados, fabricados)."""
    try:
        texto = arquivo.read_text(encoding="utf-8")
    except Exception as e:
        return None, None, None, f"erro ao ler {arquivo}: {e}"

    comandos_marcados, nao_marcados, fabricados = [], [], []

    # Encontrar blocos de código
    for m_bloco in RE_BLOCO_CODIGO.finditer(texto):
        bloco_inicio = m_bloco.start()
        bloco_fim = m_bloco.end()
        bloco_codigo = m_bloco.group(1)

        # Procurar por cli-check logo após este bloco
        busca_pos = bloco_fim
        m_check = RE_CLI_CHECK.search(texto, busca_pos, busca_pos + 200)  # Dentro de ~200 chars

        if m_check:
            fonte = m_check.group(1)
            confere = m_check.group(2) == 'true'
            primeira_linha = bloco_codigo.split('\n')[0].strip()[:60]

            if confere:
                comandos_marcados.append({
                    "comando": primeira_linha,
                    "fonte": fonte,
                    "confere": True,
                    "linha": texto[:bloco_inicio].count('\n') + 1
                })
            else:
                fabricados.append({
                    "comando": primeira_linha,
                    "fonte": fonte,
                    "confere": False,
                    "linha": texto[:bloco_inicio].count('\n') + 1
                })
        else:
            primeira_linha = bloco_codigo.split('\n')[0].strip()[:60]
            nao_marcados.append({
                "comando": primeira_linha,
                "linha": texto[:bloco_inicio].count('\n') + 1
            })

    return comandos_marcados, nao_marcados, fabricados, None


def validar_obra(slug, categoria_tecnica, relatorio_dir=None):
    """Valida comandos/CLI de uma obra; retorna (veredicto, resultado_json)."""
    dir_obra = TO.dir_obra(slug, TO.DIR_OUTPUT)
    dir_capitulos = dir_obra / "capitulos"

    if not dir_capitulos.exists():
        return "OK", {"obra": slug, "capitulos": [], "veredicto": "OK", "motivo": "sem capitulos"}

    if not categoria_tecnica:
        return "OK", {"obra": slug, "capitulos": [], "veredicto": "OK", "motivo": "categoria_tecnica=false"}

    capitulos = sorted(dir_capitulos.glob("cap_*.md"))
    resultado = {
        "obra": slug,
        "capitulos": [],
        "resumo_geral": {"total": 0, "confirmado": 0, "nao_verificado": 0, "fabricado": 0},
        "veredicto": "OK"
    }

    for cap_arquivo in capitulos:
        cap_num = int(cap_arquivo.stem.split('_')[1])
        cmd_ok, cmd_sem, cmd_fab, erro = validar_capitulo(cap_arquivo, cap_num)

        if erro:
            resultado["capitulos"].append({
                "num": cap_num,
                "arquivo": cap_arquivo.name,
                "erro": erro
            })
            continue

        cap_resumo = {
            "num": cap_num,
            "arquivo": cap_arquivo.name,
            "comandos": cmd_ok + cmd_sem + cmd_fab,
            "resumo": {
                "total": len(cmd_ok) + len(cmd_sem) + len(cmd_fab),
                "confirmado": len(cmd_ok),
                "nao_verificado": len(cmd_sem),
                "fabricado": len(cmd_fab)
            }
        }
        resultado["capitulos"].append(cap_resumo)

        # Agregar resumo geral
        resultado["resumo_geral"]["total"] += cap_resumo["resumo"]["total"]
        resultado["resumo_geral"]["confirmado"] += cap_resumo["resumo"]["confirmado"]
        resultado["resumo_geral"]["nao_verificado"] += cap_resumo["resumo"]["nao_verificado"]
        resultado["resumo_geral"]["fabricado"] += cap_resumo["resumo"]["fabricado"]

        # Se há fabricado, marcar veredicto
        if len(cmd_fab) > 0:
            resultado["veredicto"] = "REPROVADO"

    # Salvar relatório
    if relatorio_dir is None:
        relatorio_dir = dir_obra / "validacao"
    relatorio_dir.mkdir(parents=True, exist_ok=True)
    relatorio_arquivo = relatorio_dir / "relatorio_comandos_cli.json"
    relatorio_arquivo.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")

    return resultado["veredicto"], resultado


def main():
    ap = argparse.ArgumentParser(
        description="Gate F2 de comandos/CLI: valida blocos de código em capítulos técnicos")
    ap.add_argument("slug", help="obra alvo")
    ap.add_argument("--estrito", action="store_true", help="exit 1 se houver fabricado")
    ap.add_argument("--json", action="store_true", help="imprime relatório JSON completo")
    args = ap.parse_args()

    # Ler config da obra
    try:
        dir_obra = TO.dir_obra(args.slug, TO.DIR_OUTPUT)
        config_arquivo = dir_obra / "config_obra.json"
        if config_arquivo.exists():
            config = json.loads(config_arquivo.read_text(encoding="utf-8"))
            categoria_tecnica = config.get("categoria_tecnica", False)
        else:
            categoria_tecnica = False
    except Exception as e:
        print(f"[ERRO] Não consegui ler config: {e}", file=sys.stderr)
        return 1

    veredicto, resultado = validar_obra(args.slug, categoria_tecnica)

    if args.json:
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    else:
        print(f"[{veredicto}] Comandos/CLI: {resultado['resumo_geral']}")

    if args.estrito and veredicto == "REPROVADO":
        return 1
    return 0


if __name__ == "__main__":
    console_utf8()
    sys.exit(main())
