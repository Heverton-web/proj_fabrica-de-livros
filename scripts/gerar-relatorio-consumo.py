#!/usr/bin/env python3
"""
Gera relatorio de consumo de CLIs de agente (ccusage npm + ccusage pip +
verificador multi-provedor) em MD + PDF + XLSX, salvos em rel-consumo/.

Fontes:
    npx ccusage@latest [agente] daily|monthly|session|blocks --json
        (tokens/custo por periodo, opcionalmente de 1 agente so)
    ccusage json
        (rate-limit atual da API Anthropic, pip)
    scripts/verificar-rate-limits.py
        (rate-limit dos outros 11 provedores configurados via env var)

Saida (nome varia com o filtro de periodo/agente aplicado):
    rel-consumo/<rotulo>-consumo-cli[-<agente>].md
    rel-consumo/<rotulo>-consumo-cli[-<agente>].pdf
    rel-consumo/<rotulo>-consumo-cli[-<agente>].xlsx

Uso:
    python scripts/gerar-relatorio-consumo.py
    python scripts/gerar-relatorio-consumo.py --dia 2026-08-15
    python scripts/gerar-relatorio-consumo.py --mes 2026-08
    python scripts/gerar-relatorio-consumo.py --semana 2026-08-20
    python scripts/gerar-relatorio-consumo.py --desde 2026-08-01 --ate 2026-08-31
    python scripts/gerar-relatorio-consumo.py --agente claude --mes 2026-08
    python scripts/gerar-relatorio-consumo.py --secoes diario,blocos
    python scripts/gerar-relatorio-consumo.py --md-apenas
    python scripts/gerar-relatorio-consumo.py --sem-rate-limit --sem-outros-provedores
"""

import argparse
import calendar
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
REL_DIR = BASE_DIR / "rel-consumo"
PANDOC = shutil.which("pandoc") or "pandoc"

TOPO_DIARIO = 25
TOPO_SESSAO = 20
TOPO_BLOCOS = 20

AGENTES_VALIDOS = [
    "claude", "codex", "opencode", "amp", "droid", "codebuff", "hermes", "pi",
    "goose", "kilo", "copilot", "gemini", "kimi", "qwen", "openclaw", "grok",
]

_RE_DIA = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_RE_MES = re.compile(r"^\d{4}-\d{2}$")

# Raw block Typst puro repassado sem alteracao pelo Pandoc.
# Por que existe: uma tabela cuja altura fica bem perto do limite da pagina
# faz o Typst desenhar a ultima linha DUAS VEZES sobrepostas em vez de
# quebrar para a proxima pagina (bug observado empiricamente, nao documentado:
# uma tabela de 6 linhas ficou perfeita, uma de 25 corrompeu a ultima linha
# mesmo comecando do topo de uma pagina em branco). Forcar quebra de pagina
# antes de cada tabela grande NAO basta sozinho — o limite e por ALTURA da
# tabela, nao por posicao na pagina.
QUEBRA_PAGINA = "\n```{=typst}\n#pagebreak()\n```\n"

# Linhas por bloco bem abaixo do limite onde o bug aparece (~23-24 linhas
# a 9pt/A4-retrato) — paginar manualmente em blocos pequenos e mais robusto
# do que calcular o limite exato, que muda com fonte/margem/conteudo.
LINHAS_POR_BLOCO = 15


def console_utf8():
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def _validar_data(valor, nome_flag):
    if not _RE_DIA.match(valor):
        print(f"  erro: {nome_flag} precisa estar no formato AAAA-MM-DD (recebido: {valor!r})")
        sys.exit(1)
    return valor


def resolver_periodo(args):
    """Resolve os flags de periodo em (rotulo, desde, ate).

    rotulo=None quando nenhum filtro foi pedido (comportamento padrao:
    pega tudo e corta pra exibicao com TOPO_*). Prioridade quando mais de
    um flag de periodo vier junto (nao ha validacao cruzada — o mais
    especifico definido primeiro no if/elif vence): --dia > --mes >
    --semana > --desde/--ate.
    """
    if args.dia is not None:
        valor = date.today().isoformat() if args.dia == "hoje" else _validar_data(args.dia, "--dia")
        return valor, valor, valor

    if args.mes is not None:
        if not _RE_MES.match(args.mes):
            print(f"  erro: --mes precisa estar no formato AAAA-MM (recebido: {args.mes!r})")
            sys.exit(1)
        ano, mes = (int(p) for p in args.mes.split("-"))
        ultimo_dia = calendar.monthrange(ano, mes)[1]
        return args.mes, f"{args.mes}-01", f"{args.mes}-{ultimo_dia:02d}"

    if args.semana is not None:
        fim = date.today().isoformat() if args.semana == "hoje" else _validar_data(args.semana, "--semana")
        inicio = (date.fromisoformat(fim) - timedelta(days=6)).isoformat()
        return f"semana-ate-{fim}", inicio, fim

    if args.desde or args.ate:
        if not (args.desde and args.ate):
            print("  erro: --desde e --ate precisam ser usados juntos")
            sys.exit(1)
        _validar_data(args.desde, "--desde")
        _validar_data(args.ate, "--ate")
        return f"{args.desde}_a_{args.ate}", args.desde, args.ate

    return None, None, None


def comando_ccusage(subcomando, agente=None, desde=None, ate=None) -> str:
    partes = ["npx", "ccusage@latest"]
    if agente:
        partes.append(agente)
    partes += [subcomando, "--json"]
    if desde:
        partes += ["--since", desde]
    if ate:
        partes += ["--until", ate]
    return " ".join(partes)


def rodar_json(cmd: str) -> dict:
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
    if proc.returncode != 0 or not proc.stdout.strip():
        print(f"  aviso: falha ao rodar `{cmd}` (rc={proc.returncode}): {proc.stderr.strip()[:200]}")
        return {}
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        print(f"  aviso: JSON invalido de `{cmd}`")
        return {}


_VERIFICADOR_RATE_LIMITS = None


def _verificador_rate_limits():
    """Carrega scripts/verificar-rate-limits.py via importlib (nome com
    hifen nao importa direto com `import`)."""
    global _VERIFICADOR_RATE_LIMITS
    if _VERIFICADOR_RATE_LIMITS is None:
        caminho = Path(__file__).resolve().parent / "verificar-rate-limits.py"
        spec = importlib.util.spec_from_file_location("verificar_rate_limits_mod", caminho)
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        _VERIFICADOR_RATE_LIMITS = modulo
    return _VERIFICADOR_RATE_LIMITS


def extrair_lista(dados: dict, *chaves) -> list:
    """`ccusage <cmd> --json` unificado usa a chave = nome do comando
    (`session`); `ccusage <agente> session --json` usa `sessions` (plural).
    Tenta cada chave em ordem e devolve a primeira que existir."""
    for chave in chaves:
        if chave in dados:
            return dados[chave]
    return []


def registros_para_df(registros: list, agente_fallback=None) -> pd.DataFrame:
    """Mapeia daily/monthly/weekly/session.

    O relatorio UNIFICADO (`ccusage daily`) traz `period`/`agent`. O
    relatorio POR AGENTE (`ccusage claude daily`) traz `date` em vez de
    `period` (daily/monthly) ou `sessionId` (session), e NAO tem campo
    `agent` (ja esta implicito no comando) — daí o fallback."""
    if not registros:
        return pd.DataFrame()
    linhas = []
    for r in registros:
        periodo = r.get("period") or r.get("date") or r.get("sessionId") or r.get("id")
        linhas.append({
            "periodo": periodo,
            "agente": r.get("agent") or agente_fallback or "all",
            "modelos": ", ".join(r.get("modelsUsed", [])),
            "tokens_entrada": r.get("inputTokens", 0),
            "tokens_saida": r.get("outputTokens", 0),
            "tokens_cache_criacao": r.get("cacheCreationTokens", 0),
            "tokens_cache_leitura": r.get("cacheReadTokens", 0),
            "tokens_total": r.get("totalTokens", 0),
            "custo_usd": round(r.get("totalCost", 0.0), 4),
        })
    return pd.DataFrame(linhas)


def blocos_para_df(registros: list, agente_fallback="all") -> pd.DataFrame:
    """`ccusage blocks --json` usa um schema proprio (id/costUSD/models/
    tokenCounts.*), diferente de daily/monthly/session (period/agent/
    modelsUsed/totalCost) — precisa de mapeamento a parte. Schema e IGUAL
    entre o unificado e o por-agente (`ccusage claude blocks`)."""
    if not registros:
        return pd.DataFrame()
    linhas = []
    for r in registros:
        tc = r.get("tokenCounts", {}) or {}
        linhas.append({
            "periodo": r.get("id") or r.get("startTime"),
            "agente": agente_fallback,
            "modelos": ", ".join(r.get("models", [])),
            "tokens_entrada": tc.get("inputTokens", 0),
            "tokens_saida": tc.get("outputTokens", 0),
            "tokens_cache_criacao": tc.get("cacheCreationInputTokens", 0),
            "tokens_cache_leitura": tc.get("cacheReadInputTokens", 0),
            "tokens_total": r.get("totalTokens", 0),
            "custo_usd": round(r.get("costUSD", 0.0) or 0.0, 4),
        })
    return pd.DataFrame(linhas)


def df_para_impressao(df: pd.DataFrame) -> pd.DataFrame:
    """Recorte de colunas para MD/PDF.

    O Typst calcula a largura de cada coluna da tabela proporcional ao
    conteudo mais largo daquela coluna. A coluna `modelos` (lista separada
    por virgula, ate 300+ chars numa unica celula) e periodos em UUID (36
    chars, coluna `sessao`) espremem as colunas numericas a quase zero de
    largura, sobrepondo os numeros. Fix: no MD/PDF mostrar so o essencial
    (periodo truncado, agente, contagem de modelos, total, custo); a lista
    completa de modelos e o breakdown de tokens continuam no .xlsx.
    """
    if df.empty:
        return df
    impressao = pd.DataFrame({
        "periodo": df["periodo"].apply(
            lambda s: str(s) if len(str(s)) <= 15 else str(s)[:12] + "..."),
        "agente": df["agente"],
        "n_modelos": df["modelos"].apply(
            lambda s: len([m for m in str(s).split(",") if m.strip()])),
        "tokens_total": df["tokens_total"].apply(lambda v: f"{v:,}".replace(",", ".")),
        "custo_usd": df["custo_usd"].apply(lambda v: f"{v:,.4f}"),
    })
    return impressao


def _escapar_arroba(df: pd.DataFrame) -> pd.DataFrame:
    """Escapa '@' pra Pandoc nao ler como citacao bibliografica (ex.: nomes
    de modelo tipo @cf/mistralai/... da Cloudflare Workers AI)."""
    df = df.copy()
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].astype(str).str.replace("@", "\\@", regex=False)
    return df


def df_para_md_tabela(df: pd.DataFrame) -> str:
    if df.empty:
        return "_Sem dados._\n"
    return _escapar_arroba(df_para_impressao(df)).to_markdown(index=False)


def dividir_em_blocos(df: pd.DataFrame, linhas=LINHAS_POR_BLOCO) -> list:
    if df.empty:
        return [df]
    return [df.iloc[i:i + linhas] for i in range(0, len(df), linhas)]


def tabela_em_blocos(df: pd.DataFrame) -> str:
    """Serie de tabelas menores separadas por quebra de pagina — evita o bug
    de sobreposicao de linha em tabelas grandes (ver QUEBRA_PAGINA)."""
    partes = [df_para_md_tabela(bloco) for bloco in dividir_em_blocos(df)]
    return f"\n{QUEBRA_PAGINA}\n".join(partes)


def _outros_provedores_df(outros_provedores: list) -> pd.DataFrame:
    linhas = []
    for r in outros_provedores:
        if r["status"] == "ok":
            detalhe = "; ".join(f"{k}={v}" for k, v in r["dados"].items())
        else:
            detalhe = r.get("mensagem", "")
        linhas.append({"provedor": r["provedor"], "status": r["status"], "detalhe": detalhe})
    return pd.DataFrame(linhas)


_STATUS_CURTO = {
    "ok": "OK",
    "sem_chave": "sem chave",
    "erro": "erro",
    "indisponivel_via_api": "indisponível",
}


def _tabela_outros_provedores_md(outros_provedores: list) -> str:
    """Versao de impressao: status vira rotulo curto e `detalhe` e truncado.

    Mesmo bug de largura de coluna do Typst/Pandoc (ver df_para_impressao) —
    aqui o gatilho e o status "indisponivel_via_api" (20 chars) ao lado de
    uma coluna `detalhe` bem mais larga (URLs de painel). O `.xlsx` continua
    com o texto completo via `_outros_provedores_df`."""
    if not outros_provedores:
        return "_Verificação pulada nesta execução (`--sem-outros-provedores`)._\n"
    df = _outros_provedores_df(outros_provedores)
    df["status"] = df["status"].map(_STATUS_CURTO).fillna(df["status"])
    df["detalhe"] = df["detalhe"].apply(lambda s: s if len(s) <= 70 else s[:67] + "...")
    return _escapar_arroba(df).to_markdown(index=False)


def montar_markdown(data_str, rotulo_periodo, agente, rate_limit, outros_provedores,
                     secoes_pedidas, df_mensal, df_diario, df_sessao, df_blocos) -> str:
    escopo = f"agente **{agente}**" if agente else "todos os agentes detectados"
    filtro_txt = f" — filtro: **{rotulo_periodo}**" if rotulo_periodo else ""

    md = [
        "# RELATÓRIO DE CONSUMO — CLIs de Agente",
        "",
        f"> **Data de geração:** {data_str}",
        f"> **Escopo:** {escopo}{filtro_txt}",
        "> **Fontes:** `npx ccusage@latest` (tokens/custo) + `ccusage` pip + verificador multi-provedor (rate limit)",
        "",
        "---",
        "",
        "## 1. Rate Limit Atual",
        "",
        "### Anthropic (via ccusage pip)",
        "",
    ]
    if rate_limit:
        sessao = rate_limit.get("session", {})
        sete_dias = rate_limit.get("7d", {})
        md += [
            f"- **Plano:** {rate_limit.get('plan', 'N/A')}",
            f"- **Sessão atual:** {sessao.get('pct', 'N/A')}% usado (reset em {sessao.get('resets_at', 'N/A')})",
            f"- **Janela 7 dias:** {sete_dias.get('pct', 'N/A')}% usado (reset em {sete_dias.get('resets_at', 'N/A')})",
            "",
        ]
    else:
        md += ["_Não disponível nesta execução._", ""]

    md += ["### Outros Provedores", "", _tabela_outros_provedores_md(outros_provedores), ""]

    secoes = []
    if "mensal" in secoes_pedidas:
        secoes.append(("Uso Mensal", df_para_md_tabela(df_mensal) + "\n"))

    if "diario" in secoes_pedidas:
        exibir = df_diario if rotulo_periodo else (
            df_diario.tail(TOPO_DIARIO) if not df_diario.empty else df_diario)
        titulo = (f"Uso Diário — {rotulo_periodo}" if rotulo_periodo
                  else f"Uso Diário (últimos {TOPO_DIARIO} dias)")
        corpo = tabela_em_blocos(exibir) + f"\n\n> Lista completa ({len(df_diario)} dias) no arquivo `.xlsx` anexo.\n"
        secoes.append((titulo, corpo))

    if "sessao" in secoes_pedidas:
        exibir = (df_sessao.sort_values("custo_usd", ascending=False).head(TOPO_SESSAO)
                  if not df_sessao.empty else df_sessao)
        titulo = f"Top {TOPO_SESSAO} Sessões por Custo"
        if rotulo_periodo:
            titulo += f" — {rotulo_periodo}"
        corpo = tabela_em_blocos(exibir) + f"\n\n> Lista completa ({len(df_sessao)} sessões) no arquivo `.xlsx` anexo.\n"
        secoes.append((titulo, corpo))

    if "blocos" in secoes_pedidas:
        exibir = df_blocos if rotulo_periodo else (
            df_blocos.tail(TOPO_BLOCOS) if not df_blocos.empty else df_blocos)
        titulo = (f"Blocos de Faturamento — {rotulo_periodo}" if rotulo_periodo
                  else f"Blocos de Faturamento (últimos {TOPO_BLOCOS})")
        corpo = tabela_em_blocos(exibir) + f"\n\n> Lista completa ({len(df_blocos)} blocos) no arquivo `.xlsx` anexo.\n"
        secoes.append((titulo, corpo))

    indice = 2
    for titulo, corpo in secoes:
        md += [QUEBRA_PAGINA, f"## {indice}. {titulo}", "", corpo]
        indice += 1

    md += [QUEBRA_PAGINA, f"## {indice}. Totais Consolidados", ""]
    df_totais_base = df_diario if not df_diario.empty else df_mensal
    if not df_totais_base.empty:
        total_tokens = int(df_totais_base["tokens_total"].sum())
        total_custo = round(df_totais_base["custo_usd"].sum(), 2)
        md += [
            f"- **Tokens totais:** {total_tokens:,}".replace(",", "."),
            f"- **Custo total estimado:** US$ {total_custo}",
            "",
        ]
    else:
        md += ["_Sem dados para consolidar._", ""]

    md += [
        "---",
        "",
        f"*Relatório gerado em {data_str} — Fábrica Agêntica de Publicações*",
        "",
    ]
    return "\n".join(md)


def gerar_pdf(md_path: Path, pdf_path: Path) -> int:
    """Compila em retrato (A4 padrao).

    Paisagem so era necessaria enquanto as tabelas de impressao tinham 9
    colunas (incluindo `modelos`, largura variavel). Desde que
    `df_para_impressao()` reduziu para 5 colunas enxutas (periodo/agente/
    n_modelos/tokens_total/custo_usd), retrato cabe sem sobreposicao e ainda
    da mais folga vertical por pagina (841pt de altura vs 595pt em paisagem)
    — testado visualmente (PyMuPDF) antes de reverter.
    """
    cmd = [
        PANDOC, str(md_path), "-o", str(pdf_path),
        "--pdf-engine=typst", "--toc", "--toc-depth=2",
        "-V", "papersize=a4", "-V", "margin-x=2cm", "-V", "margin-y=2cm",
        "-V", "fontsize=9pt",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stderr[-1500:])
    return proc.returncode


def gerar_xlsx(xlsx_path: Path, rate_limit, outros_provedores, df_mensal, df_diario, df_sessao, df_blocos):
    df_rate = pd.DataFrame([{
        "plano": rate_limit.get("plan"),
        "sessao_pct": rate_limit.get("session", {}).get("pct"),
        "sessao_reset": rate_limit.get("session", {}).get("resets_at"),
        "7d_pct": rate_limit.get("7d", {}).get("pct"),
        "7d_reset": rate_limit.get("7d", {}).get("resets_at"),
    }]) if rate_limit else pd.DataFrame()

    df_outros = _outros_provedores_df(outros_provedores)

    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        (df_rate if not df_rate.empty else pd.DataFrame({"aviso": ["sem dados"]})).to_excel(
            writer, sheet_name="rate_limit_anthropic", index=False)
        (df_outros if not df_outros.empty else pd.DataFrame({"aviso": ["sem dados"]})).to_excel(
            writer, sheet_name="rate_limit_outros", index=False)
        (df_mensal if not df_mensal.empty else pd.DataFrame({"aviso": ["sem dados"]})).to_excel(
            writer, sheet_name="mensal", index=False)
        (df_diario if not df_diario.empty else pd.DataFrame({"aviso": ["sem dados"]})).to_excel(
            writer, sheet_name="diario", index=False)
        (df_sessao if not df_sessao.empty else pd.DataFrame({"aviso": ["sem dados"]})).to_excel(
            writer, sheet_name="sessao", index=False)
        (df_blocos if not df_blocos.empty else pd.DataFrame({"aviso": ["sem dados"]})).to_excel(
            writer, sheet_name="blocos", index=False)


def main():
    console_utf8()
    parser = argparse.ArgumentParser(
        description="Relatorio de consumo de CLIs de agente (MD+PDF+XLSX)",
        epilog=f"Agentes suportados em --agente: {', '.join(AGENTES_VALIDOS)}",
    )
    parser.add_argument("--md-apenas", action="store_true", help="Gera só o .md")
    parser.add_argument("--sem-rate-limit", action="store_true", help="Pula ccusage pip (rate limit Anthropic)")
    parser.add_argument("--sem-outros-provedores", action="store_true",
                         help="Pula a verificação dos outros provedores (OpenRouter, OpenAI, Groq...)")

    grupo_periodo = parser.add_mutually_exclusive_group()
    grupo_periodo.add_argument("--dia", nargs="?", const="hoje", metavar="AAAA-MM-DD",
                                help="Filtra para 1 dia específico (sem valor = hoje)")
    grupo_periodo.add_argument("--mes", metavar="AAAA-MM", help="Filtra para 1 mês inteiro")
    grupo_periodo.add_argument("--semana", nargs="?", const="hoje", metavar="AAAA-MM-DD",
                                help="Filtra para os 7 dias terminando na data informada (sem valor = hoje)")
    grupo_periodo.add_argument("--desde", metavar="AAAA-MM-DD", help="Início do intervalo (usar com --ate)")
    parser.add_argument("--ate", metavar="AAAA-MM-DD", help="Fim do intervalo (usar com --desde)")

    parser.add_argument("--agente", metavar="NOME", help="Restringe o relatório a 1 agente específico")
    parser.add_argument("--secoes", metavar="LISTA", default="mensal,diario,sessao,blocos",
                         help="Seções a incluir, separadas por vírgula (padrão: todas)")
    args = parser.parse_args()

    if args.agente and args.agente not in AGENTES_VALIDOS:
        print(f"  erro: agente '{args.agente}' desconhecido. Opções: {', '.join(AGENTES_VALIDOS)}")
        sys.exit(1)

    secoes_validas = {"mensal", "diario", "sessao", "blocos"}
    secoes_pedidas = {s.strip() for s in args.secoes.split(",") if s.strip()}
    invalidas = secoes_pedidas - secoes_validas
    if invalidas:
        print(f"  erro: seção(ões) desconhecida(s): {', '.join(sorted(invalidas))}. "
              f"Opções: {', '.join(sorted(secoes_validas))}")
        sys.exit(1)

    rotulo, desde, ate = resolver_periodo(args)

    REL_DIR.mkdir(exist_ok=True)
    data_str = rotulo or date.today().isoformat()
    sufixo_agente = f"-{args.agente}" if args.agente else ""
    nome_base = f"{data_str}-consumo-cli{sufixo_agente}"
    md_path = REL_DIR / f"{nome_base}.md"
    pdf_path = REL_DIR / f"{nome_base}.pdf"
    xlsx_path = REL_DIR / f"{nome_base}.xlsx"

    print("  -> Coletando dados do ccusage (npm)...")
    df_mensal = df_diario = df_sessao = df_blocos = pd.DataFrame()
    if "mensal" in secoes_pedidas:
        dados = rodar_json(comando_ccusage("monthly", args.agente, desde, ate))
        df_mensal = registros_para_df(extrair_lista(dados, "monthly"), args.agente)
    if "diario" in secoes_pedidas:
        dados = rodar_json(comando_ccusage("daily", args.agente, desde, ate))
        df_diario = registros_para_df(extrair_lista(dados, "daily"), args.agente)
    if "sessao" in secoes_pedidas:
        dados = rodar_json(comando_ccusage("session", args.agente, desde, ate))
        df_sessao = registros_para_df(extrair_lista(dados, "session", "sessions"), args.agente)
    if "blocos" in secoes_pedidas:
        dados = rodar_json(comando_ccusage("blocks", args.agente, desde, ate))
        df_blocos = blocos_para_df(extrair_lista(dados, "blocks"), args.agente or "all")

    rate_limit = {}
    if not args.sem_rate_limit:
        print("  -> Coletando rate limit Anthropic (ccusage pip)...")
        rate_limit = rodar_json("ccusage json")

    outros_provedores = []
    if not args.sem_outros_provedores:
        print("  -> Verificando rate-limit dos outros provedores...")
        outros_provedores = _verificador_rate_limits().rodar_verificacoes()

    md = montar_markdown(data_str, rotulo, args.agente, rate_limit, outros_provedores,
                          secoes_pedidas, df_mensal, df_diario, df_sessao, df_blocos)
    md_path.write_text(md, encoding="utf-8")
    print(f"  OK Markdown: {md_path.name} ({len(md)} chars)")

    if args.md_apenas:
        print("  --md-apenas: PDF e XLSX pulados")
        return

    rc = gerar_pdf(md_path, pdf_path)
    if rc != 0:
        print(f"  AVISO: PDF falhou (rc={rc}) — .md foi salvo")
    else:
        print(f"  OK PDF: {pdf_path.name}")

    gerar_xlsx(xlsx_path, rate_limit, outros_provedores, df_mensal, df_diario, df_sessao, df_blocos)
    print(f"  OK XLSX: {xlsx_path.name}")

    print(f"\n  pasta: {REL_DIR}")


if __name__ == "__main__":
    main()
