#!/usr/bin/env python3
"""
Gera relatorio de consumo de CLIs de agente (ccusage npm + ccusage pip) em
MD + PDF + XLSX, salvos em rel-consumo/ na raiz do projeto.

Fontes:
    npx ccusage@latest daily|monthly|session|blocks --json   (tokens/custo por periodo)
    ccusage json                                             (rate-limit atual da API Anthropic, pip)

Saida:
    rel-consumo/<YYYY-MM-DD>-consumo-cli.md
    rel-consumo/<YYYY-MM-DD>-consumo-cli.pdf
    rel-consumo/<YYYY-MM-DD>-consumo-cli.xlsx

Uso:
    python scripts/gerar-relatorio-consumo.py
    python scripts/gerar-relatorio-consumo.py --md-apenas
    python scripts/gerar-relatorio-consumo.py --sem-rate-limit   (pula ccusage pip, ex.: sem API key)
"""

import argparse
import json
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
REL_DIR = BASE_DIR / "rel-consumo"
PANDOC = shutil.which("pandoc") or "pandoc"

TOPO_DIARIO = 25
TOPO_SESSAO = 20
TOPO_BLOCOS = 20

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
# a 9pt/A4-paisagem) — paginar manualmente em blocos pequenos e mais robusto
# do que calcular o limite exato, que muda com fonte/margem/conteudo.
LINHAS_POR_BLOCO = 15


def dividir_em_blocos(df: pd.DataFrame, linhas=LINHAS_POR_BLOCO) -> list:
    if df.empty:
        return [df]
    return [df.iloc[i:i + linhas] for i in range(0, len(df), linhas)]


def tabela_em_blocos(df: pd.DataFrame) -> str:
    """Serie de tabelas menores separadas por quebra de pagina — evita o bug
    de sobreposicao de linha em tabelas grandes (ver QUEBRA_PAGINA)."""
    partes = [df_para_md_tabela(bloco) for bloco in dividir_em_blocos(df)]
    return f"\n{QUEBRA_PAGINA}\n".join(partes)


def console_utf8():
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


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


def registros_para_df(registros: list) -> pd.DataFrame:
    if not registros:
        return pd.DataFrame()
    linhas = []
    for r in registros:
        linhas.append({
            "periodo": r.get("period"),
            "agente": r.get("agent"),
            "modelos": ", ".join(r.get("modelsUsed", [])),
            "tokens_entrada": r.get("inputTokens", 0),
            "tokens_saida": r.get("outputTokens", 0),
            "tokens_cache_criacao": r.get("cacheCreationTokens", 0),
            "tokens_cache_leitura": r.get("cacheReadTokens", 0),
            "tokens_total": r.get("totalTokens", 0),
            "custo_usd": round(r.get("totalCost", 0.0), 4),
        })
    return pd.DataFrame(linhas)


def blocos_para_df(registros: list) -> pd.DataFrame:
    """`ccusage blocks --json` usa um schema proprio (id/costUSD/models/
    tokenCounts.*), diferente de daily/monthly/session (period/agent/
    modelsUsed/totalCost) — precisa de mapeamento a parte."""
    if not registros:
        return pd.DataFrame()
    linhas = []
    for r in registros:
        tc = r.get("tokenCounts", {}) or {}
        linhas.append({
            "periodo": r.get("id") or r.get("startTime"),
            "agente": "all",
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


def df_para_md_tabela(df: pd.DataFrame) -> str:
    """Versao de exibicao em markdown: escapa '@' para o Pandoc nao ler como citacao."""
    if df.empty:
        return "_Sem dados._\n"
    exibicao = df_para_impressao(df)
    for col in exibicao.select_dtypes(include=["object", "string"]).columns:
        exibicao[col] = exibicao[col].astype(str).str.replace("@", "\\@", regex=False)
    return exibicao.to_markdown(index=False)


def montar_markdown(data_str, rate_limit, df_diario, df_mensal, df_sessao, df_blocos) -> str:
    md = [
        "# RELATÓRIO DE CONSUMO — CLIs de Agente",
        "",
        f"> **Data de geração:** {data_str}",
        f"> **Fontes:** `npx ccusage@latest` (tokens/custo) + `ccusage` pip (rate limit Anthropic)",
        "",
        "---",
        "",
        "## 1. Rate Limit Atual (Anthropic API)",
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

    md += [
        QUEBRA_PAGINA,
        "## 2. Uso Mensal",
        "",
        df_para_md_tabela(df_mensal),
        "",
        QUEBRA_PAGINA,
        f"## 3. Uso Diário (últimos {TOPO_DIARIO} dias)",
        "",
        tabela_em_blocos(df_diario.tail(TOPO_DIARIO) if not df_diario.empty else df_diario),
        "",
        f"> Lista completa ({len(df_diario)} dias) no arquivo `.xlsx` anexo.",
        "",
        QUEBRA_PAGINA,
        f"## 4. Top {TOPO_SESSAO} Sessões por Custo",
        "",
        tabela_em_blocos(
            df_sessao.sort_values("custo_usd", ascending=False).head(TOPO_SESSAO)
            if not df_sessao.empty else df_sessao
        ),
        "",
        f"> Lista completa ({len(df_sessao)} sessões) no arquivo `.xlsx` anexo.",
        "",
        QUEBRA_PAGINA,
        f"## 5. Blocos de Faturamento (últimos {TOPO_BLOCOS})",
        "",
        tabela_em_blocos(df_blocos.tail(TOPO_BLOCOS) if not df_blocos.empty else df_blocos),
        "",
        f"> Lista completa ({len(df_blocos)} blocos) no arquivo `.xlsx` anexo.",
        "",
        QUEBRA_PAGINA,
        "## 6. Totais Consolidados",
        "",
    ]

    if not df_diario.empty:
        total_tokens = int(df_diario["tokens_total"].sum())
        total_custo = round(df_diario["custo_usd"].sum(), 2)
        md += [
            f"- **Tokens totais (todo o período diário):** {total_tokens:,}".replace(",", "."),
            f"- **Custo total estimado (todo o período diário):** US$ {total_custo}",
            "",
        ]
    else:
        md += ["_Sem dados diários para consolidar._", ""]

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


def gerar_xlsx(xlsx_path: Path, rate_limit, df_diario, df_mensal, df_sessao, df_blocos):
    df_rate = pd.DataFrame([{
        "plano": rate_limit.get("plan"),
        "sessao_pct": rate_limit.get("session", {}).get("pct"),
        "sessao_reset": rate_limit.get("session", {}).get("resets_at"),
        "7d_pct": rate_limit.get("7d", {}).get("pct"),
        "7d_reset": rate_limit.get("7d", {}).get("resets_at"),
    }]) if rate_limit else pd.DataFrame()

    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        (df_rate if not df_rate.empty else pd.DataFrame({"aviso": ["sem dados"]})).to_excel(
            writer, sheet_name="rate_limit", index=False)
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
    parser = argparse.ArgumentParser(description="Relatorio de consumo de CLIs de agente (MD+PDF+XLSX)")
    parser.add_argument("--md-apenas", action="store_true", help="Gera só o .md")
    parser.add_argument("--sem-rate-limit", action="store_true", help="Pula ccusage pip (rate limit)")
    args = parser.parse_args()

    REL_DIR.mkdir(exist_ok=True)
    data_str = date.today().isoformat()
    nome_base = f"{data_str}-consumo-cli"
    md_path = REL_DIR / f"{nome_base}.md"
    pdf_path = REL_DIR / f"{nome_base}.pdf"
    xlsx_path = REL_DIR / f"{nome_base}.xlsx"

    print("  -> Coletando dados do ccusage (npm)...")
    dados_diario = rodar_json("npx ccusage@latest daily --json")
    dados_mensal = rodar_json("npx ccusage@latest monthly --json")
    dados_sessao = rodar_json("npx ccusage@latest session --json")
    dados_blocos = rodar_json("npx ccusage@latest blocks --json")

    df_diario = registros_para_df(dados_diario.get("daily", []))
    df_mensal = registros_para_df(dados_mensal.get("monthly", []))
    df_sessao = registros_para_df(dados_sessao.get("session", []))
    df_blocos = blocos_para_df(dados_blocos.get("blocks", []))

    rate_limit = {}
    if not args.sem_rate_limit:
        print("  -> Coletando rate limit (ccusage pip)...")
        rate_limit = rodar_json("ccusage json")

    md = montar_markdown(data_str, rate_limit, df_diario, df_mensal, df_sessao, df_blocos)
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

    gerar_xlsx(xlsx_path, rate_limit, df_diario, df_mensal, df_sessao, df_blocos)
    print(f"  OK XLSX: {xlsx_path.name}")

    print(f"\n  pasta: {REL_DIR}")


if __name__ == "__main__":
    main()
