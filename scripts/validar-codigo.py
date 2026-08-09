#!/usr/bin/env python3
"""
Upgrade 3 — CI de Codigo dos Capitulos (Fabrica Agentica de Livros).

Extrai todos os blocos de codigo dos capitulos e valida a sintaxe de cada um em
processo isolado. Por padrao e analise estatica apenas (nada de rede, arquivos
ou side effects). Com --executar, os blocos executaveis (python/javascript/
bash) sao tambem EXECUTADOS em sandbox leve (cwd temporaria, env minimo,
timeout) — o modo que transforma "aplicavel" em "aplicado de verdade" e o gate
do playbook em smoke test.

Validadores por linguagem:
  python        -> ast.parse (compilador do proprio CPython)
  json          -> json.loads
  javascript    -> node --check (arquivo .mjs quando ha import/export)
  typescript    -> tsc --noEmit (se disponivel), senao NAO VERIFICADO
  bash/sh       -> bash -n
  powershell    -> parser do PowerShell (se disponivel)
  yaml          -> yaml.safe_load (se PyYAML disponivel)
  toml          -> tomllib
  html/xml      -> parser tolerante do stdlib
  sql/dockerfile/text/mermaid/diff/console -> NAO APLICAVEL (ignorado)

Uso:
    python scripts/validar-codigo.py <slug>
    python scripts/validar-codigo.py <slug> --capitulo 7
    python scripts/validar-codigo.py <slug> --md output/<slug>/livro_final.md
    python scripts/validar-codigo.py <slug> --estrito     # exit 1 se houver falha
    python scripts/validar-codigo.py <slug> --executar    # roda python/js/bash
    python scripts/validar-codigo.py <slug> --json
    python scripts/validar-codigo.py <slug-do-playbook> --playbook --executar
        # smoke test dos cards do playbook (execucao[].codigo + gate)

Relatorio: output/<slug>/validacao/relatorio_codigo.json
"""

import argparse
import ast
import json
import re
import shutil
import subprocess
import sys
import tempfile
import tipos_obra as TO
from pathlib import Path

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

RE_BLOCO = re.compile(
    r"^[ \t]*```[ \t]*(?P<lang>[A-Za-z0-9_+#\-\.]*)[ \t]*\n(?P<code>.*?)^[ \t]*```[ \t]*$",
    re.DOTALL | re.MULTILINE,
)

ALIASES = {
    "py": "python", "python3": "python",
    "js": "javascript", "node": "javascript", "mjs": "javascript", "cjs": "javascript",
    "jsx": "javascript",
    "ts": "typescript", "tsx": "typescript",
    "sh": "bash", "shell": "bash", "zsh": "bash",
    "ps1": "powershell", "pwsh": "powershell",
    "yml": "yaml",
    "jsonc": "json", "json5": "json",
}

NAO_APLICAVEL = {
    "", "text", "txt", "texto", "plaintext", "console", "output", "saida", "log",
    "diff", "patch", "sql", "dockerfile", "docker", "makefile", "ini", "cfg",
    "conf", "env", "mermaid", "plantuml", "markdown", "md", "csv", "tsv", "http",
    "graphql", "regex", "bnf", "pseudo", "pseudocodigo", "pseudocode", "asciiart",
    "tree", "terminal", "cmd", "prompt", "resultado", "tabela", "ascii",
}

# Marcadores de trecho intencionalmente incompleto — reportados como fragmento
RE_FRAGMENTO = re.compile(
    r"(^\s*\.\.\.\s*$)|(\.\.\.\s*(#|//)\s*)|(<seu[-_ ])|(<SEU[-_ ])|(\{\{\s*\w+\s*\}\})",
    re.MULTILINE,
)


def norm_lang(lang):
    lang = (lang or "").strip().lower()
    return ALIASES.get(lang, lang)


def _rodar(comando, entrada_arquivo=None, timeout=45):
    try:
        r = subprocess.run(comando, capture_output=True, text=True, timeout=timeout)
        if r.returncode == 0:
            return True, ""
        saida = (r.stderr or r.stdout or "").strip()
        return False, saida.split("\n")[0][:240] if saida else f"exit {r.returncode}"
    except FileNotFoundError:
        return None, "ferramenta ausente"
    except subprocess.TimeoutExpired:
        return False, f"timeout de {timeout}s"
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)[:240]


def _temp(codigo, sufixo):
    fh = tempfile.NamedTemporaryFile("w", suffix=sufixo, delete=False, encoding="utf-8")
    fh.write(codigo)
    fh.close()
    return Path(fh.name)


def validar_python(codigo):
    try:
        ast.parse(codigo)
        return True, ""
    except SyntaxError as exc:
        return False, f"linha {exc.lineno}: {exc.msg}"


def validar_json(codigo):
    try:
        json.loads(codigo)
        return True, ""
    except ValueError as exc:
        return False, str(exc)[:240]


def validar_javascript(codigo):
    node = shutil.which("node")
    if not node:
        return None, "node ausente"
    esm = re.search(r"^\s*(import\s|export\s|export\{|await\s)", codigo, re.MULTILINE)
    arq = _temp(codigo, ".mjs" if esm else ".js")
    try:
        return _rodar([node, "--check", str(arq)])
    finally:
        arq.unlink(missing_ok=True)


def validar_typescript(codigo):
    tsc = shutil.which("tsc") or shutil.which("tsc.cmd")
    if not tsc:
        return None, "tsc ausente (npm i -g typescript para habilitar)"
    arq = _temp(codigo, ".ts")
    try:
        return _rodar([tsc, "--noEmit", "--skipLibCheck", "--target", "es2022",
                       "--moduleResolution", "bundler", "--module", "esnext", str(arq)])
    finally:
        arq.unlink(missing_ok=True)


def validar_bash(codigo):
    bash = shutil.which("bash")
    if not bash:
        return None, "bash ausente"
    arq = _temp(codigo, ".sh")
    try:
        return _rodar([bash, "-n", str(arq)])
    finally:
        arq.unlink(missing_ok=True)


def validar_powershell(codigo):
    ps = shutil.which("powershell") or shutil.which("pwsh")
    if not ps:
        return None, "powershell ausente"
    arq = _temp(codigo, ".ps1")
    script = (
        "$ErrorActionPreference='Stop';"
        "$t=$null;$e=$null;"
        f"[System.Management.Automation.Language.Parser]::ParseFile('{arq.as_posix()}',"
        "[ref]$t,[ref]$e) > $null;"
        "if($e.Count -gt 0){[Console]::Error.WriteLine($e[0].Message); exit 1}; exit 0"
    )
    try:
        return _rodar([ps, "-NoProfile", "-NonInteractive", "-Command", script])
    finally:
        arq.unlink(missing_ok=True)


def validar_yaml(codigo):
    try:
        import yaml  # type: ignore
    except ImportError:
        return None, "PyYAML ausente (pip install pyyaml para habilitar)"
    try:
        list(yaml.safe_load_all(codigo))
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, str(exc).split("\n")[0][:240]


def validar_toml(codigo):
    try:
        import tomllib
    except ImportError:
        return None, "tomllib ausente"
    try:
        tomllib.loads(codigo)
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)[:240]


def validar_xml(codigo):
    from xml.etree import ElementTree
    try:
        ElementTree.fromstring(codigo)
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)[:240]


VALIDADORES = {
    "python": validar_python,
    "json": validar_json,
    "javascript": validar_javascript,
    "typescript": validar_typescript,
    "bash": validar_bash,
    "powershell": validar_powershell,
    "yaml": validar_yaml,
    "toml": validar_toml,
    "xml": validar_xml,
}

# Linguagens cujo bloco pode ser EXECUTADO de fato (--executar / --playbook).
EXECUTAVEIS = ("python", "javascript", "bash")

EXEC_TIMEOUT = 20  # segundos por bloco executado


def detectar_linguagem(codigo):
    """Fallback heurístico para blocos sem tag de linguagem (cards do playbook)."""
    cabeca = codigo.lstrip()[:400]
    if re.search(r"^\s*(import |from |def |class |@dataclass|print\()", cabeca, re.MULTILINE):
        return "python"
    if re.search(r"(console\.(log|error)|const |let |function |=>\s*\{|require\()", cabeca):
        return "javascript"
    if re.search(r"^(#!|set -|echo |curl |mkdir |cd |python |npm |git )", cabeca, re.MULTILINE):
        return "bash"
    return "python"


def executar_bloco(codigo, linguagem, timeout=EXEC_TIMEOUT):
    """Executa o bloco em sandbox leve: cwd temporaria, env minimo, timeout.

    Retorna (True, "") em sucesso, (False, detalhe) em falha de execucao e
    (None, detalhe) quando a ferramenta de execucao nao existe.
    """
    import os
    env = {
        "PATH": os.environ.get("PATH", ""),
        "PYTHONNOUSERSITE": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
        "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""),
    }
    if linguagem == "python":
        comando = [sys.executable, "-c", codigo]
    elif linguagem == "javascript":
        node = shutil.which("node")
        if not node:
            return None, "node ausente (nao executado)"
        comando = [node, "-e", codigo]
    elif linguagem == "bash":
        bash = shutil.which("bash")
        if not bash:
            return None, "bash ausente (nao executado)"
        comando = [bash, "-c", codigo]
    else:
        return None, f"linguagem '{linguagem}' sem executor"
    try:
        with tempfile.TemporaryDirectory(prefix="fabrica_exec_") as td:
            r = subprocess.run(comando, capture_output=True, text=True,
                               timeout=timeout, cwd=td, env=env)
    except subprocess.TimeoutExpired:
        return False, f"timeout de {timeout}s na execucao"
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)[:240]
    if r.returncode == 0:
        return True, ""
    saida = (r.stderr or r.stdout or "").strip()
    if not saida:
        return False, f"exit {r.returncode}"
    # Para tracebacks Python, a última linha carrega a mensagem real do erro.
    linhas = [l for l in saida.splitlines() if l.strip()]
    return False, linhas[-1][:240]


def linha_do_offset(texto, offset):
    return texto.count("\n", 0, offset) + 1


def validar_arquivo(caminho, rotulo, ignorar_fragmentos, executar=False):
    texto = caminho.read_text(encoding="utf-8", errors="replace")
    resultados = []
    for m in RE_BLOCO.finditer(texto):
        lang = norm_lang(m.group("lang"))
        codigo = m.group("code")
        registro = {
            "origem": rotulo,
            "linha": linha_do_offset(texto, m.start()),
            "linguagem": lang or "(sem tag)",
            "linhas_codigo": codigo.count("\n") + 1,
        }
        if lang in NAO_APLICAVEL:
            registro.update(status="nao_aplicavel", detalhe="linguagem sem validador")
            resultados.append(registro)
            continue
        if ignorar_fragmentos and RE_FRAGMENTO.search(codigo):
            registro.update(status="fragmento", detalhe="trecho com placeholder/elipse")
            resultados.append(registro)
            continue
        validador = VALIDADORES.get(lang)
        if validador is None:
            registro.update(status="nao_verificado", detalhe=f"sem validador para '{lang}'")
            resultados.append(registro)
            continue
        ok, detalhe = validador(codigo)
        if ok is None:
            registro.update(status="nao_verificado", detalhe=detalhe)
        elif ok:
            registro.update(status="ok", detalhe="")
            if executar and lang in EXECUTAVEIS:
                ex_ok, ex_detalhe = executar_bloco(codigo, lang)
                if ex_ok:
                    registro["execucao"] = "ok"
                elif ex_ok is None:
                    registro["execucao"] = "nao_executado"
                    registro["detalhe_execucao"] = ex_detalhe
                else:
                    registro["execucao"] = "falha"
                    registro["detalhe_execucao"] = ex_detalhe
                    registro.update(status="falha_execucao",
                                    detalhe=f"execucao: {ex_detalhe}")
        else:
            registro.update(status="falha", detalhe=detalhe)
        resultados.append(registro)
    return resultados


def validar_playbook(dir_pbk, ignorar_fragmentos, executar=False):
    """Smoke test dos cards do playbook: execucao[].codigo + gate por card.

    Cada bloco de codigo de execucao passa pelo validador de sintaxe e, com
    --executar, roda de verdade. O 'gate' do card (comando de verificacao,
    R-PBK-3) e executado como smoke test quando nao vazio.
    """
    import os
    dir_passos = dir_pbk / "passos"
    resultados = []
    if not dir_passos.exists():
        return resultados
    for p in sorted(dir_passos.glob("passo_*.json"),
                    key=lambda p: int(re.search(r"passo_(\d+)", p.stem).group(1))):
        try:
            card = json.loads(p.read_text(encoding="utf-8"))
        except ValueError:
            resultados.append({"origem": p.stem, "linha": 1, "linguagem": "json",
                               "linhas_codigo": 0, "status": "falha",
                               "detalhe": "card com JSON invalido"})
            continue
        rotulo = f"{p.stem} ({card.get('titulo', '')[:40]})"
        for item in card.get("execucao") or []:
            codigo = item.get("codigo") or ""
            if not codigo.strip():
                continue
            lang = norm_lang(item.get("linguagem") or "") or detectar_linguagem(codigo)
            registro = {"origem": rotulo, "linha": 1, "linguagem": lang,
                        "linhas_codigo": codigo.count("\n") + 1}
            if lang in NAO_APLICAVEL:
                registro.update(status="nao_aplicavel", detalhe="linguagem sem validador")
                resultados.append(registro)
                continue
            if ignorar_fragmentos and RE_FRAGMENTO.search(codigo):
                registro.update(status="fragmento", detalhe="trecho com placeholder/elipse")
                resultados.append(registro)
                continue
            validador = VALIDADORES.get(lang)
            if validador is None:
                registro.update(status="nao_verificado",
                                detalhe=f"sem validador para '{lang}'")
                resultados.append(registro)
                continue
            ok, detalhe = validador(codigo)
            if ok is None:
                registro.update(status="nao_verificado", detalhe=detalhe)
            elif ok:
                registro.update(status="ok", detalhe="")
                if executar and lang in EXECUTAVEIS:
                    ex_ok, ex_detalhe = executar_bloco(codigo, lang)
                    if ex_ok:
                        registro["execucao"] = "ok"
                    elif ex_ok is None:
                        registro["execucao"] = "nao_executado"
                        registro["detalhe_execucao"] = ex_detalhe
                    else:
                        registro["execucao"] = "falha"
                        registro["detalhe_execucao"] = ex_detalhe
                        registro.update(status="falha_execucao",
                                        detalhe=f"execucao: {ex_detalhe}")
            else:
                registro.update(status="falha", detalhe=detalhe)
            resultados.append(registro)
        # Gate do card (R-PBK-3): comando de verificacao executavel.
        gate = (card.get("gate") or "").strip()
        if gate:
            registro = {"origem": f"{rotulo} (gate)", "linha": 1, "linguagem": "bash",
                        "linhas_codigo": gate.count("\n") + 1}
            if not executar:
                registro.update(status="ok", detalhe="gate presente (nao executado)")
            else:
                bash = shutil.which("bash")
                if not bash:
                    registro.update(status="nao_verificado", detalhe="bash ausente")
                else:
                    env = {"PATH": os.environ.get("PATH", ""),
                           "PYTHONNOUSERSITE": "1",
                           "PYTHONDONTWRITEBYTECODE": "1",
                           "SYSTEMROOT": os.environ.get("SYSTEMROOT", "")}
                    try:
                        with tempfile.TemporaryDirectory(prefix="fabrica_gate_") as td:
                            r = subprocess.run([bash, "-c", gate], capture_output=True,
                                               text=True, timeout=EXEC_TIMEOUT,
                                               cwd=td, env=env)
                        if r.returncode == 0:
                            registro.update(status="ok", execucao="ok",
                                            detalhe="")
                        else:
                            saida = (r.stderr or r.stdout or "").strip()
                            registro.update(
                                status="falha_execucao", execucao="falha",
                                detalhe=(saida.split("\n")[0][:240]
                                         if saida else f"exit {r.returncode}"))
                    except subprocess.TimeoutExpired:
                        registro.update(status="falha_execucao", execucao="falha",
                                        detalhe=f"timeout de {EXEC_TIMEOUT}s no gate")
                    except Exception as exc:  # noqa: BLE001
                        registro.update(status="falha_execucao", execucao="falha",
                                        detalhe=str(exc)[:240])
            resultados.append(registro)
    return resultados


def main():
    ap = argparse.ArgumentParser(
        description="Valida a sintaxe (e opcionalmente executa) os blocos de codigo")
    ap.add_argument("slug")
    ap.add_argument("--capitulo", help="valida apenas o capitulo N")
    ap.add_argument("--md", help="valida um markdown especifico em vez dos capitulos")
    ap.add_argument("--ignorar-fragmentos", action="store_true",
                    help="classifica trechos com placeholders como 'fragmento' em vez de validar")
    ap.add_argument("--estrito", action="store_true", help="exit 1 se houver qualquer falha")
    ap.add_argument("--json", action="store_true", help="imprime relatorio JSON completo")
    ap.add_argument("--executar", action="store_true",
                    help="executa blocos python/javascript/bash em sandbox leve "
                         "(transforma sintaxe em smoke test)")
    ap.add_argument("--playbook", action="store_true",
                    help="valida os cards do playbook (passos/*.json) em vez dos capitulos: "
                         "sintaxe + execucao + gate como smoke test")
    args = ap.parse_args()

    dir_livro = TO.dir_obra(args.slug, DIR_OUTPUT)
    if not dir_livro.exists():
        print(f"[ERRO] Obra nao encontrada: {dir_livro}")
        return 1

    if args.playbook:
        todos = validar_playbook(dir_livro, args.ignorar_fragmentos, args.executar)
    else:
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
            todos.extend(validar_arquivo(caminho, rotulo, args.ignorar_fragmentos,
                                         executar=args.executar))

    resumo = {}
    for r in todos:
        resumo[r["status"]] = resumo.get(r["status"], 0) + 1
    por_linguagem = {}
    for r in todos:
        chave = r["linguagem"]
        por_linguagem.setdefault(chave, {"total": 0, "ok": 0, "falha": 0})
        por_linguagem[chave]["total"] += 1
        if r["status"] == "ok":
            por_linguagem[chave]["ok"] += 1
        elif r["status"] in ("falha", "falha_execucao"):
            por_linguagem[chave]["falha"] += 1

    falhas = [r for r in todos if r["status"] in ("falha", "falha_execucao")]
    verificados = resumo.get("ok", 0) + len(falhas)
    taxa = (resumo.get("ok", 0) / verificados * 100) if verificados else 100.0

    relatorio = {
        "slug": args.slug,
        "modo": "playbook" if args.playbook else "capitulos",
        "executado": args.executar,
        "total_blocos": len(todos),
        "resumo": resumo,
        "por_linguagem": por_linguagem,
        "taxa_aprovacao_pct": round(taxa, 1),
        "blocos": todos,
    }

    dir_val = dir_livro / "validacao"
    dir_val.mkdir(exist_ok=True)
    (dir_val / "relatorio_codigo.json").write_text(
        json.dumps(relatorio, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"CI de Codigo - {args.slug} ({relatorio['modo']}"
          f"{', executando' if args.executar else ''})")
    print(f"  blocos analisados : {len(todos)}")
    for status in ("ok", "falha", "falha_execucao", "nao_verificado",
                   "nao_aplicavel", "fragmento"):
        if status in resumo:
            print(f"  {status:<17}: {resumo[status]}")
    print(f"  taxa de aprovacao : {taxa:.1f}% (sobre {verificados} blocos verificaveis)")

    if falhas:
        print(f"\n[FALHA] {len(falhas)} bloco(s) reprovado(s):")
        for f in falhas[:20]:
            print(f"  - {f['origem']}:{f['linha']} [{f['linguagem']}] {f['detalhe']}")
        if len(falhas) > 20:
            print(f"  ... e mais {len(falhas) - 20}")
    else:
        print("\n[OK] Nenhum erro de sintaxe/execucao nos blocos verificaveis")

    print(f"\nRelatorio: {(dir_val / 'relatorio_codigo.json').relative_to(DIR_PROJETO)}")

    if args.json:
        print(json.dumps(relatorio, ensure_ascii=False, indent=2))

    if args.estrito and falhas:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
