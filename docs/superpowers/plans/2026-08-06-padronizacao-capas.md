# Padronização de Capas (Livro/E-book) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Consolidar 5 scripts de capa fragmentados em 1 gerador único (livro + ebook), com identidade de cor por série, ilustração temática e validação determinística de quebra de linha de título/subtítulo.

**Architecture:** `scripts/series_capa.py` (resolução de cor por série, registro `output/_series.json`) + `scripts/validar-capa-texto.py` (validador de quebra de linha via métricas reais de fonte) são consumidos por `scripts/gerar-capa.py` (gerador único Playwright/HTML, substitui 4 scripts antigos). `subagente-ilustrador` ganha um "Modo Capa" para a ilustração temática. `compilador-abnt` e `subagente-adaptador-ebook` passam a chamar essa cadeia na Fase 3. `/esbocar` ganha o campo `serie`.

**Tech Stack:** Python 3 (stdlib + Pillow para métricas de fonte + Playwright para renderização HTML→PNG), Markdown (skills/agents/CLAUDE.md).

## Global Constraints

- Fundo da capa é sempre `#0d1117` fixo, independente de obra/série (spec §3, §12).
- Dimensões: 1600×2263px para `livro`, 1200×1600px para `ebook` (spec §3) — nenhuma outra proporção.
- Autor é sempre `Heverton Eduardo Peres`; qualificação é sempre `Especialista em Marketing e Desenvolvimento de Soluções`, em 100% das capas, sem exceção por tema (spec §3, §12).
- Logo é o ícone+texto CSS `>_ EDITORA AGÊNTICA` — nunca um arquivo de imagem (spec §12).
- Título e subtítulo: máximo 2 linhas, nenhuma linha com exatamente 1 palavra (spec §3, §8).
- Escopo é só Livro e E-book — nunca tocar `template_tcc.typ`/`template_artigo.typ` (spec §2, §12).
- Sem dependência de rede durante a geração (remover `@import` do Google Fonts) — fontes locais com fallback Arial (spec §9).
- PT-BR estrito em toda prosa/skill/agent tocada (REGRA 1 do `CLAUDE.md`).

---

## Task 1: `scripts/series_capa.py` — resolução de cor por série

**Files:**
- Create: `scripts/series_capa.py`
- Test: manual via CLI (ver Step 2/4 abaixo — este projeto não usa pytest; os próprios scripts em `scripts/` são auto-testáveis via `--json`/exit code, seguindo o padrão de `scripts/parametros_obra.py`)

**Interfaces:**
- Produces: `resolver_serie_key(config_obra: dict, slug: str) -> str`, `resolver_cor(serie_key: str, slug: str | None = None) -> str`, `carregar_registro() -> dict`, `salvar_registro(registro: dict) -> None`. Consumido pela Task 3 (`gerar-capa.py`).

- [ ] **Step 1: Escrever o módulo**

Crie `scripts/series_capa.py`:

```python
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
registro output/_series.json; nas proximas vezes, reusa a cor gravada.

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

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"
CAMINHO_REGISTRO = DIR_OUTPUT / "_series.json"

# Paleta curada — consolida os hex ja em uso hoje nos scripts de capa anteriores
PALETA_ACCENT = [
    "#2ecc9a", "#58a6ff", "#a855f7", "#f0b429",
    "#37c3d6", "#f0933b", "#e05d5d", "#7c6cf0",
]


def carregar_registro():
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


def main():
    ap = argparse.ArgumentParser(description="Resolucao de cor de serie por obra")
    ap.add_argument("slug", help="ex.: livros/meu-livro ou ebooks/meu-livro--eb-01-titulo")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    config_obra = _ler_json(DIR_OUTPUT / args.slug / "config_obra.json")
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
```

- [ ] **Step 2: Testar resolução standalone (sem config_obra.json)**

Run: `python scripts/series_capa.py livros/obra-inexistente-teste --json`
Expected: imprime um JSON `{"serie_key": "obra-inexistente-teste", "cor": "#<algum hex da PALETA_ACCENT>"}` e cria/atualiza `output/_series.json` com essa entrada.

- [ ] **Step 3: Testar estabilidade (rodar de novo)**

Run: `python scripts/series_capa.py livros/obra-inexistente-teste --json` (de novo)
Expected: retorna a **mesma** cor da Step 2 (prova que o registro persiste e é reusado, não sorteado de novo).

- [ ] **Step 4: Remover a entrada de teste do registro**

Edite `output/_series.json` manualmente e remova a chave `"obra-inexistente-teste"` (era só para validar o mecanismo, não deve sobrar no repositório).

- [ ] **Step 5: Commit**

```bash
git add scripts/series_capa.py
git commit -m "feat: resolucao de cor de accent por serie (output/_series.json)"
```

---

## Task 2: `scripts/validar-capa-texto.py` — validador de quebra de linha

**Files:**
- Create: `scripts/validar-capa-texto.py`

**Interfaces:**
- Consumes: nada de outra task.
- Produces: `validar_capa(titulo: str, subtitulo: str, tipo: str = "livro") -> dict` (chaves `ok`, `titulo`, `subtitulo`, cada uma com `ok`/`linhas`/`motivo`). Consumido pela Task 3.

- [ ] **Step 1: Escrever o módulo**

Crie `scripts/validar-capa-texto.py`:

```python
#!/usr/bin/env python3
"""
Validador deterministico de quebra de linha para titulo/subtitulo de capa.

Regra (docs/superpowers/specs/2026-08-06-capas-padronizadas-design.md, secao 8):
  - Maximo 2 linhas.
  - Nenhuma linha resultante pode ter exatamente 1 palavra.

Mede a largura real de cada palavra com uma fonte concreta (tenta Inter em
assets/fonts/ ou nas fontes do Windows; cai para Arial Bold/Regular quando
Inter nao estiver instalada) e simula a quebra de linha "greedy" — o mesmo
algoritmo que o navegador usa para quebrar texto numa caixa de largura fixa.

Uso como biblioteca:
    from validar_capa_texto import validar_capa

Uso como CLI:
    python scripts/validar-capa-texto.py --titulo "CODE REVIEW GRAPH" --tipo livro
"""
import argparse
import sys
from pathlib import Path

from PIL import ImageFont

FONT_DIR_WINDOWS = Path(r"C:\Windows\Fonts")
DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_FONTES_PROJETO = DIR_PROJETO / "assets" / "fonts"

# Caixa de texto = largura da capa menos padding lateral (80px de cada lado)
LARGURA_CAIXA = {"livro": 1600 - 2 * 80, "ebook": 1200 - 2 * 80}

FONTES_TITULO = ["Inter-Black.ttf", "Inter-ExtraBold.ttf"]
FONTES_SUBTITULO = ["Inter-Light.ttf"]
FALLBACK_TITULO = "arialbd.ttf"
FALLBACK_SUBTITULO = "arial.ttf"

TAMANHO_TITULO = 72
TAMANHO_SUBTITULO = 22


def _carregar_fonte(nomes_preferidos, fallback, tamanho):
    for nome in nomes_preferidos:
        for base in (DIR_FONTES_PROJETO, FONT_DIR_WINDOWS):
            caminho = base / nome
            if caminho.exists():
                return ImageFont.truetype(str(caminho), tamanho)
    caminho_fallback = FONT_DIR_WINDOWS / fallback
    if caminho_fallback.exists():
        return ImageFont.truetype(str(caminho_fallback), tamanho)
    return ImageFont.load_default()


def quebrar_linhas(texto, fonte, largura_caixa):
    """Simula quebra de linha 'greedy', igual a uma caixa CSS de largura fixa."""
    palavras = texto.split()
    linhas, atual = [], []
    for palavra in palavras:
        candidata = " ".join(atual + [palavra])
        if not atual or fonte.getlength(candidata) <= largura_caixa:
            atual.append(palavra)
        else:
            linhas.append(atual)
            atual = [palavra]
    if atual:
        linhas.append(atual)
    return linhas


def validar_texto(texto, fonte, largura_caixa, max_linhas=2):
    """Retorna (ok: bool, linhas: list[list[str]], motivo: str | None)."""
    if not texto or not texto.strip():
        return True, [], None
    linhas = quebrar_linhas(texto, fonte, largura_caixa)
    if len(linhas) > max_linhas:
        return False, linhas, f"{len(linhas)} linhas (maximo {max_linhas})"
    for linha in linhas:
        if len(linha) == 1:
            return False, linhas, f"linha com 1 palavra so: {linha[0]!r}"
    return True, linhas, None


def validar_capa(titulo, subtitulo, tipo="livro"):
    largura = LARGURA_CAIXA[tipo]
    fonte_titulo = _carregar_fonte(FONTES_TITULO, FALLBACK_TITULO, TAMANHO_TITULO)
    fonte_subtitulo = _carregar_fonte(FONTES_SUBTITULO, FALLBACK_SUBTITULO, TAMANHO_SUBTITULO)

    ok_t, linhas_t, motivo_t = validar_texto(titulo, fonte_titulo, largura)
    ok_s, linhas_s, motivo_s = validar_texto(subtitulo, fonte_subtitulo, largura)

    return {
        "ok": ok_t and ok_s,
        "titulo": {"ok": ok_t, "linhas": [" ".join(l) for l in linhas_t], "motivo": motivo_t},
        "subtitulo": {"ok": ok_s, "linhas": [" ".join(l) for l in linhas_s], "motivo": motivo_s},
    }


def main():
    ap = argparse.ArgumentParser(description="Valida quebra de linha de titulo/subtitulo de capa")
    ap.add_argument("--titulo", default="")
    ap.add_argument("--subtitulo", default="")
    ap.add_argument("--tipo", choices=["livro", "ebook"], default="livro")
    args = ap.parse_args()

    resultado = validar_capa(args.titulo, args.subtitulo, args.tipo)
    for campo in ("titulo", "subtitulo"):
        r = resultado[campo]
        status = "[OK]" if r["ok"] else "[ERRO]"
        extra = f" — {r['motivo']}" if r["motivo"] else ""
        print(f"{status} {campo}: {r['linhas']}{extra}")
    return 0 if resultado["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Testar um título inválido (3 linhas, última com 1 palavra)**

Run: `python scripts/validar-capa-texto.py --titulo "CODE REVIEW GRAPH" --tipo livro`
Expected: exit code `1`, imprime `[ERRO] titulo: ['CODE REVIEW', 'GRAPH']` (ou 3 linhas, dependendo da fonte disponível) com motivo de violação — a chamada real do `code-review-graph` atual (3 linhas, última com a palavra isolada "GRAPH") deve reprovar.

- [ ] **Step 3: Testar um título válido (2 linhas, sem linha de 1 palavra)**

Run: `python scripts/validar-capa-texto.py --titulo "CODE REVIEW GRAPH GUIA" --subtitulo "Guia definitivo para revisar codigo com IA" --tipo livro`
Expected: exit code `0`, ambos `[OK]`.

- [ ] **Step 4: Testar subtítulo com linha de 1 palavra isolada**

Run: `python scripts/validar-capa-texto.py --titulo "TITULO CURTO" --subtitulo "Um subtitulo qualquer que force uma quebra estranha aqui palavra"`
Expected: se a quebra resultar em alguma linha de 1 palavra, `[ERRO] subtitulo: ...` com motivo `linha com 1 palavra so: '...'`. (Ajuste o texto de teste se a fonte de fallback não produzir a quebra esperada — o objetivo do step é confirmar que o caminho de reprovação por linha de 1 palavra dispara com *algum* texto.)

- [ ] **Step 5: Commit**

```bash
git add scripts/validar-capa-texto.py
git commit -m "feat: validador deterministico de quebra de linha para capa"
```

---

## Task 3: `subagente-ilustrador` — Modo Capa

**Files:**
- Modify: `.claude/agents/subagente-ilustrador.md`

**Interfaces:**
- Consumes: nada de código (é um agente, não script).
- Produces: contrato de saída `output/<slug>/imagens/capa_ilustracao.png` (1000×600px), consumido pela Task 6/7 (chamadas de pipeline) e pela Task 4 (`gerar-capa.py` embute esse arquivo se existir).

- [ ] **Step 1: Adicionar seção "Modo Capa" ao agente**

No arquivo `.claude/agents/subagente-ilustrador.md`, após a seção `## Formato de Naming` (linha 87-89 hoje) e antes de `## Estilo Visual`, insira:

```markdown
## Modo Capa (ilustração da capa da obra)

Além de ilustrar capítulos, este subagente também gera **a ilustração
temática da capa** da obra (livro ou ebook) — invocado pelo `compilador-abnt`
(livro) e pelo `subagente-adaptador-ebook` (ebook) na Fase 3, antes de rodar
`scripts/gerar-capa.py`.

### Entrada (Modo Capa)
- `output/<slug>/sumario_macro.json` — título e temas gerais da obra (não um
  capítulo específico)
- Cor de accent da obra/série, informada pelo orquestrador (resultado de
  `python scripts/series_capa.py <slug> --json`)

### Saída (Modo Capa)
- `output/<slug>/imagens/capa_ilustracao.png` — **1000×600px**, fundo `#0d1117`
  (idêntico ao fundo da capa, para não deixar borda visível quando embutida)

### Procedimento (Modo Capa)
1. Leia `sumario_macro.json` e identifique o **tema central** da obra inteira
   (não um capítulo isolado) — normalmente o assunto do título/subtítulo e os
   títulos das Partes.
2. Gere 1 ilustração simples e representativa do tema (mesmos princípios do
   modo capítulo: flat 2D, sem sombras 3D, sem fotos, sem texto extenso
   embutido na imagem).
3. Use a **cor de accent recebida** (não o `#2ecc9a` fixo do modo capítulo)
   como acento principal desta ilustração, para casar com as faixas e o
   destaque do título na capa.
4. Renderize com o mesmo procedimento Playwright já usado no modo capítulo
   (viewport `1000x600`), salvando em `output/<slug>/imagens/capa_ilustracao.png`.
5. Se não for possível produzir algo relevante ao tema (assunto muito
   abstrato), é aceitável pular este passo — a capa é gerada sem ilustração
   em vez de travar a esteira (REGRA 3).
```

- [ ] **Step 2: Commit**

```bash
git add .claude/agents/subagente-ilustrador.md
git commit -m "feat: modo capa no subagente-ilustrador (ilustracao tematica da obra)"
```

---

## Task 4: `scripts/gerar-capa.py` — gerador único

**Files:**
- Create: `scripts/gerar-capa.py`
- Delete: `scripts/gerar-capa-ebook-padrao.py` (conteúdo migra para o novo arquivo)

**Interfaces:**
- Consumes: `series_capa.resolver_serie_key`/`resolver_cor` (Task 1), `validar_capa_texto.validar_capa` (Task 2, importado como `validar_capa_texto` — nome de módulo com hífen precisa de `importlib`, ver Step 1).
- Produces: `gerar_capa(titulo, subtitulo, dir_saida, tipo="livro", cor_acento=None, autor=AUTOR_PADRAO, qualificacao=QUALIFICACAO_PADRAO, badge_texto=None, ilustracao_relpath=None) -> Path` e `gerar_capa_da_obra(slug, tipo_forcado=None) -> Path`. Consumido pela Task 6 (compilador-abnt), Task 7 (subagente-adaptador-ebook) e Task 9 (migração `--todos`).

- [ ] **Step 1: Escrever o gerador**

Crie `scripts/gerar-capa.py` (novo arquivo — o antigo `gerar-capa-ebook-padrao.py` será removido no Step 4):

```python
#!/usr/bin/env python3
"""
Gerador unico de capa (livro e e-book), padrao Editora Agentica.

Substitui scripts/gerar-capa-ebook-padrao.py (Playwright/HTML antigo, so
ebook), scripts/gerar-capa-ebooks.py (Pillow, dimensao 1:1,6 divergente),
scripts/testar_capa_marketing.py e scripts/gerar_capas_demais_ebooks.py
(CONFIGS_SERIE hardcoded — agora em output/_series.json via series_capa.py).

Ver docs/superpowers/specs/2026-08-06-capas-padronizadas-design.md.

Uso (1 obra, resolvendo tudo a partir dos arquivos da propria obra):
    python scripts/gerar-capa.py livros/meu-livro
    python scripts/gerar-capa.py ebooks/meu-livro--eb-01-titulo

Uso (titulo/subtitulo/cor explicitos, sem depender de arquivos da obra):
    python scripts/gerar-capa.py livros/meu-livro --tipo livro \
        --titulo "MEU TITULO" --subtitulo "Meu subtitulo" --cor "#58a6ff"

Uso (migracao em lote — regenera todas as obras existentes):
    python scripts/gerar-capa.py --todos
"""
import argparse
import importlib
import json
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("[ERRO] playwright nao instalado")
    sys.exit(1)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from series_capa import resolver_cor, resolver_serie_key  # noqa: E402

_validar_mod = importlib.import_module("validar-capa-texto")
validar_capa = _validar_mod.validar_capa

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_OUTPUT = DIR_PROJETO / "output"

AUTOR_PADRAO = "Heverton Eduardo Peres"
QUALIFICACAO_PADRAO = "Especialista em Marketing e Desenvolvimento de Soluções"

DIMENSOES = {"livro": (1600, 2263), "ebook": (1200, 1600)}


def _destacar_ultima_palavra(titulo, cor_acento):
    palavras = titulo.strip().split()
    if len(palavras) < 2:
        return titulo
    resto, ultima = " ".join(palavras[:-1]), palavras[-1]
    return f'{resto} <span class="highlight">{ultima}</span>'


def _gerar_html(titulo, subtitulo, cor_acento, autor, qualificacao, badge_texto,
                 ilustracao_relpath, largura, altura):
    titulo_html = _destacar_ultima_palavra(titulo, cor_acento)
    bloco_ilustracao = (
        f'<div class="ilustracao"><img src="{ilustracao_relpath}" alt=""></div>'
        if ilustracao_relpath else ""
    )
    bloco_badge = f'<div class="badge">{badge_texto}</div>' if badge_texto else ""
    bloco_subtitulo = f'<div class="subtitle">{subtitulo}</div>' if subtitulo else ""

    return f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: {largura}px; height: {altura}px;
    background: #0d1117;
    font-family: 'Inter', Arial, sans-serif;
    position: relative;
    overflow: hidden;
  }}
  .top-bar {{ position: absolute; top: 0; left: 0; width: 100%; height: 8px; background: {cor_acento}; }}
  .bottom-bar {{ position: absolute; bottom: 0; left: 0; width: 100%; height: 6px; background: {cor_acento}; }}
  .content {{
    position: absolute; top: 50px; bottom: 50px; left: 80px; right: 80px;
    display: flex; flex-direction: column;
  }}
  .header {{ display: flex; align-items: center; gap: 12px; margin-bottom: 24px; flex-shrink: 0; }}
  .editora-icon {{
    width: 44px; height: 44px; border: 2px solid {cor_acento}; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; color: {cor_acento}; font-weight: 700; font-family: monospace;
  }}
  .editora-text {{ font-size: 14px; font-weight: 600; color: #8b949e; letter-spacing: 3px; text-transform: uppercase; }}
  .ilustracao {{ flex: 1; display: flex; align-items: center; justify-content: center; min-height: 0; margin-bottom: 24px; }}
  .ilustracao img {{ max-width: 100%; max-height: 100%; object-fit: contain; }}
  .title {{ font-size: 72px; font-weight: 900; color: #e6edf3; line-height: 1.05; letter-spacing: -1px; margin-bottom: 16px; flex-shrink: 0; }}
  .title .highlight {{ color: {cor_acento}; }}
  .subtitle {{ font-size: 22px; font-weight: 300; color: #8b949e; margin-bottom: 20px; flex-shrink: 0; }}
  .badge {{ display: inline-block; background: {cor_acento}; color: #0d1117; padding: 8px 20px; border-radius: 18px; font-weight: 700; font-size: 15px; margin-bottom: 20px; align-self: flex-start; flex-shrink: 0; }}
  .divider {{ width: 80px; height: 4px; background: {cor_acento}; margin-bottom: 16px; flex-shrink: 0; }}
  .author-name {{ font-size: 20px; font-weight: 600; color: #e6edf3; margin-bottom: 4px; flex-shrink: 0; }}
  .author-role {{ font-size: 12px; color: {cor_acento}; letter-spacing: 2px; text-transform: uppercase; font-weight: 600; flex-shrink: 0; }}
</style>
</head>
<body>
  <div class="top-bar"></div>
  <div class="bottom-bar"></div>
  <div class="content">
    <div class="header">
      <div class="editora-icon">&gt;_</div>
      <div class="editora-text">Editora Agêntica</div>
    </div>
    {bloco_ilustracao}
    <div class="title">{titulo_html}</div>
    {bloco_subtitulo}
    {bloco_badge}
    <div class="divider"></div>
    <div class="author-name">{autor}</div>
    <div class="author-role">{qualificacao}</div>
  </div>
</body>
</html>'''


def gerar_capa(titulo, subtitulo, dir_saida, tipo="livro", cor_acento="#58a6ff",
               autor=AUTOR_PADRAO, qualificacao=QUALIFICACAO_PADRAO,
               badge_texto=None, ilustracao_relpath=None):
    dir_saida = Path(dir_saida)
    largura, altura = DIMENSOES[tipo]

    resultado = validar_capa(titulo, subtitulo, tipo)
    for campo in ("titulo", "subtitulo"):
        r = resultado[campo]
        if not r["ok"]:
            print(f"[AVISO] {campo} viola a regra de quebra de linha: {r['motivo']}")

    if ilustracao_relpath and not (dir_saida / ilustracao_relpath).exists():
        ilustracao_relpath = None

    html = _gerar_html(titulo, subtitulo, cor_acento, autor, qualificacao,
                        badge_texto, ilustracao_relpath, largura, altura)

    dir_saida.mkdir(parents=True, exist_ok=True)
    (dir_saida / "imagens").mkdir(exist_ok=True)
    html_file = dir_saida / "capa.html"
    html_file.write_text(html, encoding="utf-8")

    png_file = dir_saida / "imagens" / "capa.png"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": largura, "height": altura})
        page.goto(f"file:///{html_file.resolve().as_posix()}")
        page.wait_for_timeout(1500)
        page.screenshot(path=str(png_file))
        browser.close()

    print(f"[OK] {png_file.relative_to(DIR_PROJETO)} ({png_file.stat().st_size // 1024} KB)")
    return png_file


def _ler_json(caminho):
    if caminho.exists():
        try:
            return json.loads(caminho.read_text(encoding="utf-8"))
        except ValueError:
            return {}
    return {}


def gerar_capa_da_obra(slug, tipo_forcado=None):
    """Resolve titulo/subtitulo/cor/ilustracao a partir dos arquivos da propria obra."""
    dir_obra = DIR_OUTPUT / slug
    config_obra = _ler_json(dir_obra / "config_obra.json")
    sumario = _ler_json(dir_obra / "sumario_macro.json")
    meta_ebook = _ler_json(dir_obra / "ebook_metadados.json")

    tipo = tipo_forcado or ("ebook" if slug.startswith("ebooks/") else "livro")
    titulo = (meta_ebook.get("titulo") or sumario.get("titulo_obra") or Path(slug).name).upper()
    subtitulo = meta_ebook.get("subtitulo") or sumario.get("subtitulo") or ""

    serie_key = resolver_serie_key(config_obra, slug)
    cor_acento = resolver_cor(serie_key, slug)

    ilustracao_relpath = "imagens/capa_ilustracao.png"

    return gerar_capa(
        titulo=titulo,
        subtitulo=subtitulo,
        dir_saida=dir_obra,
        tipo=tipo,
        cor_acento=cor_acento,
        ilustracao_relpath=ilustracao_relpath,
    )


def main():
    ap = argparse.ArgumentParser(description="Gerador unico de capa (livro/ebook)")
    ap.add_argument("slug", nargs="?", help="ex.: livros/meu-livro ou ebooks/meu-livro--eb-01-titulo")
    ap.add_argument("--tipo", choices=["livro", "ebook"], default=None)
    ap.add_argument("--titulo")
    ap.add_argument("--subtitulo", default="")
    ap.add_argument("--cor")
    ap.add_argument("--badge")
    ap.add_argument("--todos", action="store_true",
                     help="regenera todas as obras em output/livros e output/ebooks")
    args = ap.parse_args()

    if args.todos:
        alvos = []
        if (DIR_OUTPUT / "livros").exists():
            alvos += [f"livros/{d.name}" for d in (DIR_OUTPUT / "livros").iterdir() if d.is_dir()]
        if (DIR_OUTPUT / "ebooks").exists():
            alvos += [f"ebooks/{d.name}" for d in (DIR_OUTPUT / "ebooks").iterdir() if d.is_dir()]
        falhas = []
        for slug in sorted(alvos):
            try:
                gerar_capa_da_obra(slug)
            except Exception as exc:  # noqa: BLE001 — nao travar o lote por 1 obra ruim
                print(f"[ERRO] {slug}: {exc}")
                falhas.append(slug)
        if falhas:
            print(f"\n[AVISO] {len(falhas)} obra(s) falharam: {falhas}")
        return 0

    if not args.slug:
        print("[ERRO] informe <slug> ou use --todos")
        return 1

    if args.titulo:
        config_obra = _ler_json(DIR_OUTPUT / args.slug / "config_obra.json")
        cor = args.cor or resolver_cor(resolver_serie_key(config_obra, args.slug), args.slug)
        gerar_capa(args.titulo, args.subtitulo, DIR_OUTPUT / args.slug,
                   tipo=args.tipo or "livro", cor_acento=cor, badge_texto=args.badge)
    else:
        gerar_capa_da_obra(args.slug, tipo_forcado=args.tipo)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Testar geração explícita (sem depender de obra existente)**

Run:
```bash
mkdir -p output/livros/_teste-capa
python scripts/gerar-capa.py livros/_teste-capa --tipo livro --titulo "TESTE DE CAPA PADRAO" --subtitulo "Validando o gerador unico" --cor "#58a6ff"
```
Expected: exit code `0`, imprime `[OK] output/livros/_teste-capa/imagens/capa.png (... KB)`, e o arquivo `output/livros/_teste-capa/imagens/capa.png` existe com 1600×2263px.

- [ ] **Step 3: Inspecionar visualmente**

Abra `output/livros/_teste-capa/imagens/capa.png` e confirme visualmente: fundo escuro, faixas superior/inferior na cor `#58a6ff`, chancela `>_ EDITORA AGÊNTICA`, título branco com a última palavra ("PADRAO") em azul, subtítulo cinza, divider azul, "Heverton Eduardo Peres" / "ESPECIALISTA EM MARKETING E DESENVOLVIMENTO DE SOLUÇÕES".

- [ ] **Step 4: Remover a obra de teste e o script antigo**

```bash
rm -rf output/livros/_teste-capa
git rm scripts/gerar-capa-ebook-padrao.py
```

- [ ] **Step 5: Commit**

```bash
git add scripts/gerar-capa.py
git commit -m "feat: gerador unico de capa (livro/ebook), substitui gerar-capa-ebook-padrao.py"
```

---

## Task 5: Remover os 3 scripts de capa obsoletos restantes

**Files:**
- Delete: `scripts/gerar-capa-ebooks.py`
- Delete: `scripts/testar_capa_marketing.py`
- Delete: `scripts/gerar_capas_demais_ebooks.py`

**Interfaces:**
- Consumes: nenhuma (a Task 9 assume o papel de regeneração em lote que `gerar_capas_demais_ebooks.py` cumpria, via `gerar-capa.py --todos`).
- Produces: nenhuma.

- [ ] **Step 1: Confirmar que nada mais importa esses módulos**

Run: `grep -rn "gerar-capa-ebooks\|testar_capa_marketing\|gerar_capas_demais_ebooks" --include="*.py" --include="*.md" .`
Expected: nenhuma ocorrência fora dos próprios arquivos que serão removidos (se aparecer alguma referência em `.claude/agents/subagente-adaptador-ebook.md`, ela será corrigida na Task 7 — confirme que essa correção já foi feita antes deste step, ou rode esta Task depois da Task 7).

- [ ] **Step 2: Remover os arquivos**

```bash
git rm scripts/gerar-capa-ebooks.py scripts/testar_capa_marketing.py scripts/gerar_capas_demais_ebooks.py
```

- [ ] **Step 3: Commit**

```bash
git commit -m "chore: remove scripts de capa obsoletos (consolidados em gerar-capa.py)"
```

---

## Task 6: Pipeline do livro — `compilador-abnt` (Nó 9.6)

**Files:**
- Modify: `.claude/skills/compilador-abnt/SKILL.md`

**Interfaces:**
- Consumes: `subagente-ilustrador` (Modo Capa, Task 3), `scripts/gerar-capa.py` (Task 4), `scripts/validar-capa-texto.py` (Task 2).
- Produces: instrução de pipeline consumida por quem executa a Fase 3 de um livro.

- [ ] **Step 1: Atualizar a seção "Nó 9.6" do método manual**

Em `.claude/skills/compilador-abnt/SKILL.md`, substitua o bloco:

```markdown
### Nó 9.6 — Capa e ficha catalográfica (Upgrade 5)
7.2 Confira os metadados visuais derivados da obra:
    ```bash
    python scripts/metadados_livro.py <slug>
    ```
```

por:

```markdown
### Nó 9.6 — Capa gráfica e ficha catalográfica (Upgrade 5 + Padronização de Capas)
7.2 Gere a capa gráfica ANTES de derivar os metadados (o passo seguinte
    detecta `imagens/capa.png` e injeta como `capa_imagem` no Typst):
    1. Invoque `subagente-ilustrador` (Modo Capa) para gerar
       `imagens/capa_ilustracao.png` a partir do tema geral da obra
       (`sumario_macro.json`) — passo best-effort, não trava a esteira se falhar.
    2. Gere a capa no padrão único:
       ```bash
       python scripts/gerar-capa.py <slug> --tipo livro
       ```
    3. Se o passo anterior imprimir `[AVISO] titulo/subtitulo viola a regra
       de quebra de linha`, encurte o título/subtítulo no `sumario_macro.json`
       (REGRA 4) e repita o passo 2 — no máximo 3 tentativas; esgotadas,
       siga com a melhor versão e registre a não conformidade.
7.3 Confira os demais metadados visuais derivados da obra (paleta interna,
    CIP, sinopse — **não afeta a capa gráfica**, que já foi gerada no 7.2):
    ```bash
    python scripts/metadados_livro.py <slug>
    ```
```

- [ ] **Step 2: Atualizar a linha "Capa gráfica" da tabela do Template ABNT**

Substitua a linha (dentro da tabela `| Elemento | Especificação |`):
```
| **Capa gráfica** | Página colorida (6 paletas determinísticas por slug), título, subtítulo, autor, ano |
```
por:
```
| **Capa gráfica** | PNG gerado por `scripts/gerar-capa.py --tipo livro` (padrão Editora Agêntica, ver REGRA 5), embutido full-bleed via `capa_imagem`; fallback Typst nativo (6 paletas por slug) só se a geração falhar |
```

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/compilador-abnt/SKILL.md
git commit -m "feat: compilador-abnt gera a capa grafica padronizada no No 9.6"
```

---

## Task 7: Pipeline do ebook — `subagente-adaptador-ebook`

**Files:**
- Modify: `.claude/agents/subagente-adaptador-ebook.md`

**Interfaces:**
- Consumes: `subagente-ilustrador` (Modo Capa, Task 3), `scripts/gerar-capa.py` (Task 4).
- Produces: instrução de pipeline consumida por quem executa a Fase 3 de um ebook.

- [ ] **Step 1: Substituir o passo 5 (geração de capa)**

Em `.claude/agents/subagente-adaptador-ebook.md`, substitua:

```markdown
5. Gere a capa no padrão Editora Agêntica (flat 2D, 1200×1600px) — passo
   **obrigatório**, nunca manual, nunca pulado:
   ```bash
   python scripts/gerar-capa-ebook-padrao.py <titulo> <subtitulo> --cor <cor> --cmd <comando> --output <dir_ebook>
   ```
   Exemplo:
   ```bash
   python scripts/gerar-capa-ebook-padrao.py "FUNDAMENTOS" "O Problema dos Tokens" --cor "#58a6ff" --cmd "code-review-graph build" --output output/ebooks/meu-ebook
   ```
```

por:

```markdown
5. Gere a capa no padrão único Editora Agêntica (flat 2D, 1200×1600px) — passo
   **obrigatório**, nunca manual, nunca pulado:
   1. Invoque `subagente-ilustrador` (Modo Capa) para gerar
      `output/<slug_ebook>/imagens/capa_ilustracao.png` a partir do tema do
      ebook — best-effort, não bloqueia se falhar.
   2. Gere a capa:
      ```bash
      python scripts/gerar-capa.py <slug_ebook> --tipo ebook
      ```
   3. Se imprimir `[AVISO]` de quebra de linha inválida, encurte
      título/subtítulo em `ebook_metadados.json` e repita (máx. 3 tentativas).
```

- [ ] **Step 2: Commit**

```bash
git add .claude/agents/subagente-adaptador-ebook.md
git commit -m "feat: subagente-adaptador-ebook usa o gerador unico de capa (gerar-capa.py)"
```

---

## Task 8: `/esbocar` — campo `serie`

**Files:**
- Modify: `.claude/commands/esbocar.md`

**Interfaces:**
- Produces: campo `serie` em `config_obra.json`, consumido por `series_capa.resolver_serie_key` (Task 1).

- [ ] **Step 1: Adicionar a pergunta "Série" na Rodada 2**

Em `.claude/commands/esbocar.md`, na tabela da "Rodada 2", adicione uma linha (a Rodada 2 hoje tem 4 linhas — Tamanho, Qtd. Artigos, Qtd. Ebooks — cabe 1 mais dentro do limite de 4 opções por pergunta do `AskUserQuestion`, sendo esta pergunta sempre aplicável, não condicional):

```markdown
| Série | Esta obra faz parte de uma série/coleção? | sempre | Não, standalone (Recommended) \| Other (nome da série) |
```

- [ ] **Step 2: Atualizar o schema `config_obra.json`**

No bloco de schema JSON do Passo 2, adicione o campo depois de `"tamanho_obra"`:

```json
{
  "tema": "$ARGUMENTS",
  "tipo_obra": "livro | tcc",
  "min_referencias_por_capitulo": 5,
  "tamanho_obra": "P | M | G | GG | XG | null",
  "serie": "<nome-da-serie> | null",
  "gerar_artigos": true,
  "qtd_artigos": 3,
  "gerar_ebooks": true,
  "qtd_ebooks": 5
}
```

- [ ] **Step 3: Documentar a resolução de "Other"**

Na frase "Se o operador selecionar 'Other' em qualquer pergunta, use o valor livre fornecido, respeitando os limites: refs 5-20, artigos 1-5, ebooks 1-10, tamanho P/M/G/GG/XG.", adicione ao final: ", série: qualquer texto livre (ou `null` se 'Não, standalone')."

- [ ] **Step 4: Commit**

```bash
git add .claude/commands/esbocar.md
git commit -m "feat: campo serie em config_obra.json via /esbocar"
```

---

## Task 9: `CLAUDE.md` REGRA 5 — reescrita (+ 6 espelhos, cada um com seu próprio texto de origem)

**Descoberta importante (drift pré-existente, não causado por este plano):** os 6
espelhos (`AGENTS.md`, `.clinerules`, `.windsurfrules`,
`.windsurf/rules/fabrica-agentica.md`, `.cursor/rules/fabrica-agentica.mdc`,
`.github/copilot-instructions.md`) não são mais hardlinks reais de `CLAUDE.md` (o
projeto foi extraído/copiado em algum momento e os links quebraram) e estão numa
versão **mais antiga da numeração de regras**: neles a capa está em duas regras
separadas — **REGRA 7 (Capa Padrão Editora Agêntica)** e **REGRA 8 (Cores
Unificadas)** — não em "REGRA 5" como no `CLAUDE.md` atual (que em algum momento
consolidou REGRA 7+8 em uma única REGRA 5 mais detalhada, sem propagar aos
espelhos). Os 6 espelhos são idênticos entre si (confirmado: mesma contagem de
linhas), então o mesmo texto de origem/substituição vale para todos.

**Files:**
- Modify: `CLAUDE.md` (bloco REGRA 5), `AGENTS.md` + `.clinerules` +
  `.windsurfrules` + `.windsurf/rules/fabrica-agentica.md` +
  `.cursor/rules/fabrica-agentica.mdc` + `.github/copilot-instructions.md`
  (bloco REGRA 7 + REGRA 8, texto idêntico nos 6)

**Interfaces:**
- Nenhuma (documentação).

- [ ] **Step 1a: Substituir o bloco da REGRA 5 em `CLAUDE.md`**

Em `CLAUDE.md`, localize o bloco que começa em
`- **REGRA 5 (Identidade Visual da Editora Agêntica — Padrão 2D Plano):**` e
termina em `n) **Salvar:** \`imagens/capa.png\` (PNG)`, e substitua por:

```markdown
- **REGRA 5 (Identidade Visual da Editora Agêntica — Padrão 2D Plano):** Aplica-se a
  Livro e E-book (TCC/Artigo usam capa sóbria ABNT própria, fora desta regra). As
  capas DEVEM ser geradas exclusivamente como arte gráfica 2D plana retangular da
  página frontal (flat 2D front cover page), sendo estritamente PROIBIDO a inclusão
  de mockups 3D, bordas de lombada simuladas, faixas laterais de encadernação,
  sombras de efeito livro ou estética amadora de "IA 3D neon". O padrão oficial exige:
  a) **Fundo Matte Sóbrio:** #0d1117 (matte escuro, fixo, independente de obra/série)
  b) **Barras de Accent:** topo (8px) + rodapé (6px) na cor de accent da obra/série
  c) **Padding Lateral:** 80px mínimo
  d) **Chancela:** `>_ EDITORA AGÊNTICA` (ícone + texto CSS, topo esquerda)
  e) **Ilustração temática:** gerada pelo `subagente-ilustrador` (Modo Capa), remete
     ao tema central da obra, área central fixa do layout
  f) **Título:** branco (#e6edf3), Inter 900 72px, **máx. 2 linhas, nenhuma linha
     com 1 palavra só** (validado por `scripts/validar-capa-texto.py`), última
     palavra destacada na cor de accent
  g) **Subtítulo:** Inter 300 18-24px, cor #8b949e, **máx. 2 linhas, nenhuma linha
     com 1 palavra só**, objetivo (sem prolixidade)
  h) **Badge (opcional):** pill de texto com 1 frase de destaque, cor de accent
  i) **Divider:** faixa fina decorativa, cor de accent
  j) **Autor:** Heverton Eduardo Peres (fixo, Inter 600 18-20px, cor #e6edf3)
  k) **Qualificação:** "Especialista em Marketing e Desenvolvimento de Soluções"
     (fixo em TODAS as capas, Inter 600 11-12px, cor do accent — nunca varia por tema)
  l) **Cor de accent por Série:** obras da mesma série (campo `serie` em
     `config_obra.json`, ou mãe+derivados via `livro_mae`) compartilham a mesma cor,
     resolvida e persistida em `output/_series.json` (ver `scripts/series_capa.py`)
  m) **Dimensões:** 1200x1600px (ebooks), 1600x2263px (livros A4)
  n) **Script:** `scripts/gerar-capa.py --tipo livro|ebook` (HTML/CSS + Playwright,
     único gerador — substitui as variantes anteriores)
  o) **Salvar:** `imagens/capa.png` (PNG)
```

- [ ] **Step 1b: Substituir o bloco REGRA 7 + REGRA 8 nos 6 espelhos**

Nos 6 arquivos espelho, localize o bloco que começa em
`- **REGRA 7 (Capa Padrão Editora Agêntica):**` e termina em
`Exemplo: ebook verde usa #2ecc9a em tudo.` (REGRA 7 + REGRA 8 completas), e
substitua pelo mesmo texto novo do Step 1a, **renumerando para "REGRA 7"**
(mantendo a numeração local desses arquivos, que não tem a REGRA 5 unificada
do `CLAUDE.md`) e removendo a REGRA 8 (seu conteúdo — cor unificada por
obra/série — já está incorporado no item l) do novo texto):

```markdown
- **REGRA 7 (Capa Padrão Editora Agêntica — Padrão 2D Plano):** Aplica-se a Livro
  e E-book (TCC/Artigo usam capa sóbria ABNT própria, fora desta regra). As capas
  DEVEM ser geradas exclusivamente como arte gráfica 2D plana retangular da página
  frontal (flat 2D front cover page), sendo estritamente PROIBIDO a inclusão de
  mockups 3D, bordas de lombada simuladas, faixas laterais de encadernação,
  sombras de efeito livro ou estética amadora de "IA 3D neon". O padrão oficial exige:
  - **Fundo Matte Sóbrio:** #0d1117 (matte escuro, fixo, independente de obra/série)
  - **Barras de Accent:** topo (8px) + rodapé (6px) na cor de accent da obra/série
  - **Padding Lateral:** 80px mínimo
  - **Chancela:** `>_ EDITORA AGÊNTICA` (ícone + texto CSS, topo esquerda)
  - **Ilustração temática:** gerada pelo `subagente-ilustrador` (Modo Capa), remete
    ao tema central da obra, área central fixa do layout
  - **Título:** branco (#e6edf3), Inter 900 72px, **máx. 2 linhas, nenhuma linha
    com 1 palavra só** (validado por `scripts/validar-capa-texto.py`), última
    palavra destacada na cor de accent
  - **Subtítulo:** Inter 300 18-24px, cor #8b949e, **máx. 2 linhas, nenhuma linha
    com 1 palavra só**, objetivo (sem prolixidade)
  - **Badge (opcional):** pill de texto com 1 frase de destaque, cor de accent
  - **Divider:** faixa fina decorativa, cor de accent
  - **Autor:** Heverton Eduardo Peres (fixo, Inter 600 18-20px, cor #e6edf3)
  - **Qualificação:** "Especialista em Marketing e Desenvolvimento de Soluções"
    (fixo em TODAS as capas, Inter 600 11-12px, cor do accent — nunca varia por tema)
  - **Cor de accent por Série:** obras da mesma série (campo `serie` em
    `config_obra.json`, ou mãe+derivados via `livro_mae`) compartilham a mesma cor,
    resolvida e persistida em `output/_series.json` (ver `scripts/series_capa.py`)
  - **Dimensões:** 1200x1600px (ebooks), 1600x2263px (livros A4)
  - **Script:** `scripts/gerar-capa.py --tipo livro|ebook` (HTML/CSS + Playwright,
    único gerador — substitui `gerar-capa-ebook-padrao.py` e demais variantes)
  - **Salvar:** `imagens/capa.png` (PNG)
```

- [ ] **Step 2: Verificar que os 6 espelhos ficaram idênticos entre si no trecho novo**

Run: `diff <(sed -n '/REGRA 7 (Capa Padrão/,/Salvar.*capa.png/p' AGENTS.md) <(sed -n '/REGRA 7 (Capa Padrão/,/Salvar.*capa.png/p' .clinerules)`
Expected: sem diferenças (saída vazia). Repita comparando `AGENTS.md` contra os outros 4 espelhos.

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md AGENTS.md .clinerules .windsurfrules .windsurf/rules/fabrica-agentica.md .cursor/rules/fabrica-agentica.mdc .github/copilot-instructions.md
git commit -m "docs: padroniza regra de capa (livro/ebook) em CLAUDE.md e nos 6 espelhos"
```

> Nota separada (fora deste plano): os 6 espelhos têm outras divergências de
> numeração/conteúdo com `CLAUDE.md` além da regra de capa (o projeto foi
> extraído/copiado e os hardlinks quebraram — ver seção 6 do `CLAUDE.md`). Esse
> problema mais amplo não é resolvido aqui; considerar `scripts/setup-links.ps1`
> num momento separado, com aprovação explícita, já que ele exige apagar os 6
> arquivos antes de recriar os hardlinks.

---

## Task 10: Migração das capas existentes

**Files:**
- Nenhum arquivo de código novo — usa `scripts/gerar-capa.py --todos` (Task 4) e `scripts/series_capa.py` (Task 1).
- Modify (dado, não código): `output/_series.json` (seed inicial), `output/livros/*/imagens/capa.png`, `output/ebooks/*/imagens/capa.png` (regenerados).

**Interfaces:**
- Consumes: Task 1, Task 3, Task 4.

- [ ] **Step 1: Semear `output/_series.json` com as 3 séries já conhecidas**

Antes de rodar `--todos`, grave manualmente (ou via um Python one-off) as 3 entradas que hoje só existiam como `CONFIGS_SERIE` hardcoded em `scripts/gerar_capas_demais_ebooks.py` (removido na Task 5), para preservar as cores já em uso:

```bash
python -c "
import sys; sys.path.insert(0, 'scripts')
from series_capa import resolver_cor, carregar_registro, salvar_registro
registro = carregar_registro()
registro['ai-driven-development'] = {'cor': '#2ecc9a', 'membros': registro.get('ai-driven-development', {}).get('membros', [])}
registro['marketing-na-era-digital'] = {'cor': '#f0933b', 'membros': registro.get('marketing-na-era-digital', {}).get('membros', [])}
registro['sdlc-ai-first'] = {'cor': '#37c3d6', 'membros': registro.get('sdlc-ai-first', {}).get('membros', [])}
salvar_registro(registro)
print('[OK] seed gravado')
"
```
Expected: `[OK] seed gravado`, e `output/_series.json` contém as 3 chaves com as cores certas.

- [ ] **Step 2: (Agente) Gerar ilustrações temáticas para obras que ainda não têm**

Este passo requer julgamento de um agente (não é scriptável): para cada
`output/livros/<slug>/` e `output/ebooks/<slug>/` que ainda não tenha
`imagens/capa_ilustracao.png`, invoque `subagente-ilustrador` em Modo Capa
(Task 3) para gerá-la. Obras sem ilustração ainda funcionam no Step 3 (a
capa é gerada sem a área de ilustração), então este step pode ser feito
incrementalmente depois, sem bloquear a migração.

- [ ] **Step 3: Rodar a migração em lote**

Run: `python scripts/gerar-capa.py --todos`
Expected: uma linha `[OK] output/livros/<slug>/imagens/capa.png (... KB)` (ou `ebooks/...`) por obra existente, incluindo `output/livros/code-review-graph/` e seus ebooks derivados; qualquer falha aparece como `[ERRO] <slug>: <motivo>` sem interromper o restante do lote.

- [ ] **Step 4: Inspecionar visualmente pelo menos 3 resultados**

Abra manualmente:
- `output/livros/code-review-graph/imagens/capa.png` — confirme que o título agora respeita 2 linhas / sem linha de 1 palavra (o exemplo original tinha "GRAPH" isolado — se o título original ainda violar a regra mesmo após a tentativa automática, sinalize para revisão manual do título em `sumario_macro.json`).
- 1 ebook standalone (sem `livro_mae` nem `serie`) — confirme cor estável e coerente com o slug.
- 1 par mãe+derivado de uma série conhecida (ex. `ai-driven-development` e um de seus e-books) — confirme que **ambos usam a mesma cor** `#2ecc9a`.

- [ ] **Step 5: Commit do estado final do registro de série**

```bash
git add output/_series.json
git commit -m "chore: migra capas existentes para o padrao unico e semeia output/_series.json"
```

> Nota: `output/livros/*/imagens/capa.png` e `output/ebooks/*/imagens/capa.png`
> regenerados não são commitados aqui a menos que o repositório já versione
> artefatos de `output/` (confira `git status` antes do Step 5 — se esses PNGs
> aparecerem como modificados/novos e o projeto normalmente os versiona,
> inclua-os no mesmo commit; se `output/` estiver no `.gitignore`, ignore).

---

## Self-Review (registrado aqui para rastreabilidade)

**Cobertura da spec:** seções 3 (layout) → Task 4; 4 (série/cor) → Task 1; 5
(schema) → Task 8; 6 (pergunta `/esbocar`) → Task 8; 7 (integração pipeline)
→ Tasks 6/7; 8 (validador) → Task 2; 9 (consolidação de arquivos) → Tasks
4/5; 10 (migração) → Task 10; 12 (decisões registradas) → refletidas nos
Global Constraints e na REGRA 5 reescrita (Task 9). Nenhuma seção da spec
ficou sem task correspondente.

**Consistência de tipos/nomes:** `gerar_capa()` e `gerar_capa_da_obra()`
(Task 4) são os únicos pontos de entrada usados pelas Tasks 6/7/10 — mesma
assinatura em todas as referências. `resolver_serie_key`/`resolver_cor`
(Task 1) usados identicamente em Task 4 e Task 10. `validar_capa()` (Task 2)
é a única função de validação referenciada nas Tasks 4/6/7.

**Sem placeholders:** todas as steps de código têm o conteúdo completo do
arquivo, não fragmentos "similares a"; todas as steps de teste têm o comando
exato e o resultado esperado.
