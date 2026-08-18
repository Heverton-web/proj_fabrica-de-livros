# CAMPANHA e MÁQUINA Opcionais + Versionamento (R17) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tornar a geração de CAMPANHA e MÁQUINA de vendas opcionais (decidida na
entrevista `/esbocar`) e permitir gerá-las a qualquer momento para uma coleção
já existente, com escolha explícita entre **Criar Nova** (versiona a
existente) e **Sobrescrever Existente**, nunca decidido silenciosamente.

**Architecture:** Duas flags booleanas novas em `config_obra.json`
(`gerar_campanha`, `gerar_maquina`) tornam os Fluxos 2/3 de
`/produzir-obra-completa` condicionais. Um par de funções genéricas em
`tipos_obra.py` (`proxima_versao_arquivada`/`arquivar_para_versoes`) implementa
o versionamento: antes de recriar a pasta canônica (`campanhas/` ou
`maquina/`), ela é MOVIDA para uma pasta sibling `versoes/` com sufixo
`-v{N}`. Nenhum script existente (`colecao.py`, `empacotar-colecao.py`,
`validar-campanha.py`) precisa saber sobre versionamento — eles continuam lendo
só o caminho canônico. A escolha Nova/Sobrescrever é sempre feita pelo
orquestrador (comando `.md`, via `AskUserQuestion`) e passada aos scripts
como `--versionar` ou `--regenerar`/`--forcar`.

**Tech Stack:** Python 3 (scripts determinísticos da Fábrica), pytest,
Markdown (comandos `.claude/commands/*.md`).

## Global Constraints

- **R16 (CLAUDE.md):** depois de CADA task, a suíte completa (`python -m
  pytest -q`) tem que estar 100% verde antes de comitar. Suíte vermelha nunca é
  comitada; nunca contornar um teste para fazê-lo passar — corrigir a causa.
- **R17 (CLAUDE.md, regra intocável):** CAMPANHA e MÁQUINA são sempre
  opcionais; a escolha Nova/Sobrescrever quando já existirem é sempre do
  operador, nunca decidida silenciosamente pelo sistema.
- **Nenhum arquivo/pasta gerado usa prefixo `_`** (regra de empacotamento
  existente do projeto) — por isso a pasta de versionamento se chama
  `versoes/`, não `_versoes/`.
- Scripts da fábrica usam UTF-8 explícito em `print`/console (`TO.console_utf8()`
  ou `sys.stdout.reconfigure(encoding="utf-8")`) — não remover essas chamadas
  ao editar `main()`.
- Testes isolam `output/` real via `monkeypatch.setattr(<modulo>, "DIR_OUTPUT",
  tmp_path)` — nunca testar contra o `output/` do projeto.

## Desvios justificados do spec

Duas simplificações em relação a `docs/superpowers/specs/2026-08-14-campanha-maquina-opcionais-design.md`,
descobertas ao ler o código real antes de planejar (YAGNI — não adicionar
tratamento para cenário que não ocorre):

1. **`colecao.py` não precisa de `"versoes"` em `_RAIZES_ESTRUTURAIS`.** Essa
   constante só decide, a partir do 1º segmento de um slug de MEMBRO, se ele é
   um hub ou uma pasta estrutural (`varrer()`/`_hub_da_colecao`). `versoes/`
   nunca é o 1º segmento do slug de um membro — é uma pasta sibling de
   `campanhas/`/`maquina/` dentro do hub, nunca escaneada por
   `TO.listar_materiais`. Task 6 adiciona só a leitura derivada
   (`_versoes_arquivadas`), sem tocar `_RAIZES_ESTRUTURAIS`.
2. **`empacotar-colecao.py` não precisa de exclusão explícita de `versoes/`.**
   `empacotar()` já copia por WHITELIST (artefatos por tipo de membro +
   `maquina/` explicitamente) — nunca faz cópia cega do hub inteiro. `versoes/`
   já fica de fora hoje, sem nenhuma mudança de código. Task 6 adiciona um
   teste de regressão (`test_pacote_nao_inclui_versoes_arquivadas`) para
   travar esse comportamento, em vez de uma mudança de código que seria
   redundante.

---

### Task 1: `parametros_obra.py` — `gerar_campanha`/`gerar_maquina` opcionais

**Files:**
- Modify: `scripts/parametros_obra.py:61-71` (dict `DERIVADOS_V5`)
- Test: `tests/test_parametros_obra_v5.py` (classe `TestCarregarConfig`)

**Interfaces:**
- Consumes: nada novo (mesmo padrão de `gerar_deck`/`gerar_emails` já
  existente em `DERIVADOS_V5`).
- Produces: `PO.carregar_config(slug)["gerar_campanha"]` e
  `["gerar_maquina"]` — bool, default `False`. Consumido pela Task 7
  (`/produzir-obra-completa.md`, via leitura direta do JSON, não da API
  Python).

- [ ] **Step 1: Escrever os testes que falham**

Adicionar em `tests/test_parametros_obra_v5.py`, dentro de `class
TestCarregarConfig` (depois de `test_listas_padrao_nao_sao_compartilhadas`):

```python
    def test_gerar_campanha_e_gerar_maquina_default_false(self, tmp_path, monkeypatch):
        monkeypatch.setattr(PO, "DIR_OUTPUT", tmp_path)
        cfg = PO.carregar_config("livros/inexistente")
        assert cfg["gerar_campanha"] is False
        assert cfg["gerar_maquina"] is False

    def test_gerar_campanha_e_gerar_maquina_explicitos_sao_preservados(
            self, tmp_path, monkeypatch):
        monkeypatch.setattr(PO, "DIR_OUTPUT", tmp_path)
        dir_obra = tmp_path / "livros" / "obra"
        dir_obra.mkdir(parents=True)
        dados = config_livro()
        dados["gerar_campanha"] = True
        dados["gerar_maquina"] = True
        (dir_obra / "config_obra.json").write_text(
            json.dumps(dados), encoding="utf-8")
        cfg = PO.carregar_config("livros/obra")
        assert cfg["gerar_campanha"] is True
        assert cfg["gerar_maquina"] is True
```

- [ ] **Step 2: Rodar e confirmar falha**

Run: `python -m pytest tests/test_parametros_obra_v5.py -k gerar_campanha_e_gerar_maquina -v`
Expected: FAIL — `KeyError: 'gerar_campanha'`.

- [ ] **Step 3: Implementar**

Em `scripts/parametros_obra.py`, editar `DERIVADOS_V5` (linhas 61-71):

```python
DERIVADOS_V5 = {
    "gerar_playbook": False,
    "gerar_lead_magnets": False,
    "formatos_lm": [],
    "gerar_deck": False,
    "gerar_emails": False,
    "gerar_campanha": False,
    "gerar_maquina": False,
    "cta_url": "",
    "cta_texto": "",
    "modo_producao": "obra-unica",   # obra-unica | cascata
    "obra_raiz": None,               # preenchido quando modo_producao=cascata
}
```

Nenhuma outra mudança: `carregar_config` (linhas 112-144) já aplica
`DERIVADOS_V5` via `setdefault`/spread tanto no ramo V3 (sem arquivo) quanto no
ramo com `config_obra.json` existente — os dois testes do Step 1 exercitam
exatamente esses dois ramos.

- [ ] **Step 4: Rodar e confirmar sucesso**

Run: `python -m pytest tests/test_parametros_obra_v5.py -v`
Expected: PASS (todos, incluindo os 2 novos e os que já iteravam `DERIVADOS_V5`
genericamente).

- [ ] **Step 5: Suíte completa (R16) + commit**

Run: `python -m pytest -q`
Expected: 100% verde.

```bash
git add scripts/parametros_obra.py tests/test_parametros_obra_v5.py
git commit -m "feat: gerar_campanha/gerar_maquina opcionais em config_obra.json (R17)"
```

---

### Task 2: `tipos_obra.py` — helpers genéricos de versionamento

**Files:**
- Modify: `scripts/tipos_obra.py:43-46` (imports), inserir novo bloco antes de
  `# ── CLI ──` (linha 715)
- Test: Create `tests/test_tipos_obra_versionamento.py`

**Interfaces:**
- Consumes: nada (funções puras sobre `Path`/disco).
- Produces:
  - `TO.proxima_versao_arquivada(dir_versoes: Path, prefixo: str) -> int` — 1 +
    maior N já em `dir_versoes/<prefixo>-vN`, ou 1 se nenhuma existir.
  - `TO.arquivar_para_versoes(origem: Path, dir_versoes: Path, prefixo: str) ->
    Path | None` — move `origem` para `dir_versoes/<prefixo>-v{N}/`; `None` se
    `origem` não existe. Consumido pelas Tasks 4 e 5.

- [ ] **Step 1: Escrever os testes que falham**

Criar `tests/test_tipos_obra_versionamento.py`:

```python
"""Testes dos helpers genericos de versionamento (R17) de tipos_obra.py."""

import tipos_obra as TO


class TestProximaVersaoArquivada:
    def test_primeira_versao_e_v1(self, tmp_path):
        assert TO.proxima_versao_arquivada(tmp_path / "versoes", "campanhas") == 1

    def test_incrementa_a_maior_existente(self, tmp_path):
        dir_versoes = tmp_path / "versoes"
        dir_versoes.mkdir()
        (dir_versoes / "campanhas-v1").mkdir()
        (dir_versoes / "campanhas-v3").mkdir()
        assert TO.proxima_versao_arquivada(dir_versoes, "campanhas") == 4

    def test_prefixos_diferentes_nao_se_misturam(self, tmp_path):
        dir_versoes = tmp_path / "versoes"
        dir_versoes.mkdir()
        (dir_versoes / "maquina-v5").mkdir()
        assert TO.proxima_versao_arquivada(dir_versoes, "campanhas") == 1


class TestArquivarParaVersoes:
    def test_move_a_pasta_de_origem(self, tmp_path):
        origem = tmp_path / "campanhas"
        origem.mkdir()
        (origem / "campanha.json").write_text("{}", encoding="utf-8")

        destino = TO.arquivar_para_versoes(origem, tmp_path / "versoes", "campanhas")

        assert destino == tmp_path / "versoes" / "campanhas-v1"
        assert not origem.exists()
        assert (destino / "campanha.json").is_file()

    def test_chamadas_sucessivas_incrementam(self, tmp_path):
        dir_versoes = tmp_path / "versoes"
        for _ in range(2):
            origem = tmp_path / "campanhas"
            origem.mkdir()
            TO.arquivar_para_versoes(origem, dir_versoes, "campanhas")

        assert (dir_versoes / "campanhas-v1").is_dir()
        assert (dir_versoes / "campanhas-v2").is_dir()

    def test_sem_origem_devolve_none(self, tmp_path):
        resultado = TO.arquivar_para_versoes(
            tmp_path / "nao-existe", tmp_path / "versoes", "campanhas")
        assert resultado is None
```

- [ ] **Step 2: Rodar e confirmar falha**

Run: `python -m pytest tests/test_tipos_obra_versionamento.py -v`
Expected: FAIL — `AttributeError: module 'tipos_obra' has no attribute
'proxima_versao_arquivada'`.

- [ ] **Step 3: Implementar**

Em `scripts/tipos_obra.py`, trocar os imports do topo (linhas 43-46):

```python
import argparse
import json
import re
import shutil
import sys
from pathlib import Path
```

E inserir o bloco a seguir imediatamente antes de `# ── CLI
──────────────────────────────────────────────────────────────────────────────`
(linha 715 atual, logo depois de `matriz_reescrita()`):

```python
# ── Versionamento (R17 — CAMPANHA/MAQUINA sao opcionais e versionaveis) ────

def proxima_versao_arquivada(dir_versoes, prefixo):
    """1 + maior N ja em `dir_versoes/<prefixo>-vN` (1 se nao houver nenhuma)."""
    maior = 0
    padrao = re.compile(rf"^{re.escape(prefixo)}-v(\d+)$")
    dir_versoes = Path(dir_versoes)
    if dir_versoes.exists():
        for p in dir_versoes.iterdir():
            m = padrao.match(p.name)
            if m:
                maior = max(maior, int(m.group(1)))
    return maior + 1


def arquivar_para_versoes(origem, dir_versoes, prefixo):
    """Move a pasta `origem` para `dir_versoes/<prefixo>-v{N}/` (N seguinte).

    Usado pelo `--versionar` de criar-campanha.py/criar-maquina-vendas.py: a
    pasta canonica (campanhas/, maquina/) sai do caminho antes da nova
    criacao, sem que nenhum outro script precise saber sobre versionamento.
    Devolve o caminho da versao arquivada, ou None se `origem` nao existe."""
    origem = Path(origem)
    if not origem.exists():
        return None
    dir_versoes = Path(dir_versoes)
    n = proxima_versao_arquivada(dir_versoes, prefixo)
    dir_versoes.mkdir(parents=True, exist_ok=True)
    destino = dir_versoes / f"{prefixo}-v{n}"
    shutil.move(str(origem), str(destino))
    return destino
```

- [ ] **Step 4: Rodar e confirmar sucesso**

Run: `python -m pytest tests/test_tipos_obra_versionamento.py -v`
Expected: PASS (6 testes).

- [ ] **Step 5: Suíte completa (R16) + commit**

Run: `python -m pytest -q`
Expected: 100% verde.

```bash
git add scripts/tipos_obra.py tests/test_tipos_obra_versionamento.py
git commit -m "feat: helpers genericos de versionamento (arquivar_para_versoes) em tipos_obra"
```

---

### Task 3: `campanha.py` — `dir_versoes()`

**Files:**
- Modify: `scripts/campanha.py` (inserir depois de `dir_campanha_material`,
  linha 491)
- Test: `tests/test_campanha.py` (nova classe `TestDirVersoes`)

**Interfaces:**
- Consumes: `TO.arquivar_para_versoes` (Task 2, só na Task 4).
- Produces: `CP.dir_versoes(slug_material, base=None) -> Path` — sibling de
  `campanhas/` no hub da coleção (`<hub>/versoes`). Consumido pela Task 4.

- [ ] **Step 1: Escrever o teste que falha**

Em `tests/test_campanha.py`, adicionar (depois da classe `TestRegistro`, antes
do bloco de moldes — qualquer ponto no nível de módulo serve, mas manter perto
de outros testes de caminho):

```python
class TestDirVersoes:
    def test_dir_versoes_e_sibling_de_campanhas(self, ambiente):
        slug = ambiente["slug"]
        assert CP.dir_versoes(slug) == CP.dir_campanhas(slug).parent / "versoes"
```

- [ ] **Step 2: Rodar e confirmar falha**

Run: `python -m pytest tests/test_campanha.py -k test_dir_versoes_e_sibling_de_campanhas -v`
Expected: FAIL — `AttributeError: module 'campanha' has no attribute 'dir_versoes'`.

- [ ] **Step 3: Implementar**

Em `scripts/campanha.py`, imediatamente depois de `dir_campanha_material`
(linha 491, antes de `def carregar_manifesto_colecao`):

```python
def dir_versoes(slug_material, base=None):
    """Pasta de versoes arquivadas da colecao: <hub>/versoes (sibling de
    campanhas/). Usada por --versionar (R17) para NAO sobrescrever a
    campanha existente — ela e movida para ca antes da recriacao."""
    return dir_campanhas(slug_material, base).parent / "versoes"
```

- [ ] **Step 4: Rodar e confirmar sucesso**

Run: `python -m pytest tests/test_campanha.py -k test_dir_versoes_e_sibling_de_campanhas -v`
Expected: PASS.

- [ ] **Step 5: Suíte completa (R16) + commit**

Run: `python -m pytest -q`
Expected: 100% verde.

```bash
git add scripts/campanha.py tests/test_campanha.py
git commit -m "feat: campanha.dir_versoes() — pasta de versoes arquivadas do hub"
```

---

### Task 4: `criar-campanha.py` — flag `--versionar`

**Files:**
- Modify: `scripts/criar-campanha.py:733-763` (`gerar_material`), `:688-730`
  (`gerar_completo`), `:805-853` (`main`)
- Test: `tests/test_campanha.py` (nova classe `TestVersionar`)

**Interfaces:**
- Consumes: `TO.arquivar_para_versoes` (Task 2), `CP.dir_versoes`/
  `CP.nome_material` (Task 3 e já existente).
- Produces: `gerar_material(slug, base=None, regenerar=False, com_artes=True,
  versionar=False)` e `gerar_completo(chave, base=None, regenerar=False,
  com_artes=True, versionar=False)` — ambas aceitam o novo kwarg
  `versionar`. CLI ganha `--versionar`. Consumido pela Task 7 (comandos
  `/campanha`, `/campanha-completa`).

- [ ] **Step 1: Escrever os testes que falham**

Em `tests/test_campanha.py`, adicionar:

```python
class TestVersionar:
    def test_versionar_material_arquiva_e_recria_do_zero(self, ambiente):
        slug = ambiente["slug"]
        criador.gerar_material(slug, com_artes=False)
        raiz = CP.dir_campanha_material(slug)
        (raiz / "marca.txt").write_text("v1", encoding="utf-8")

        criador.gerar_material(slug, com_artes=False, versionar=True)

        assert raiz.exists()
        assert not (raiz / "marca.txt").exists(), "canonico recriado do zero"
        prefixo = f"campanhas-{CP.nome_material(slug)}"
        versao = CP.dir_versoes(slug) / f"{prefixo}-v1"
        assert (versao / "marca.txt").is_file()

    def test_versionar_material_duas_vezes_incrementa(self, ambiente):
        slug = ambiente["slug"]
        criador.gerar_material(slug, com_artes=False)
        criador.gerar_material(slug, com_artes=False, versionar=True)
        criador.gerar_material(slug, com_artes=False, versionar=True)

        prefixo = f"campanhas-{CP.nome_material(slug)}"
        base_versoes = CP.dir_versoes(slug)
        assert (base_versoes / f"{prefixo}-v1").is_dir()
        assert (base_versoes / f"{prefixo}-v2").is_dir()

    def test_versionar_sem_campanha_existente_nao_cria_versoes(self, ambiente):
        slug = ambiente["slug"]
        criador.gerar_material(slug, com_artes=False, versionar=True)
        assert not CP.dir_versoes(slug).exists()

    def test_versionar_completo_arquiva_toda_a_pasta_campanhas(self, ambiente):
        criador.gerar_completo(COLECAO, com_artes=False)
        raiz_campanhas = ambiente["raiz"] / COLECAO / "campanhas"
        assert raiz_campanhas.exists()

        criador.gerar_completo(COLECAO, com_artes=False, versionar=True)

        assert raiz_campanhas.exists(), "canonico recriado apos o versionamento"
        versao = ambiente["raiz"] / COLECAO / "versoes" / "campanhas-v1"
        assert (versao / "campanha.json").is_file()
```

- [ ] **Step 2: Rodar e confirmar falha**

Run: `python -m pytest tests/test_campanha.py -k TestVersionar -v`
Expected: FAIL — `TypeError: gerar_material() got an unexpected keyword
argument 'versionar'`.

- [ ] **Step 3: Implementar**

Em `scripts/criar-campanha.py`, editar a assinatura e o corpo de
`gerar_material` (linhas 733-742):

```python
def gerar_material(slug, base=None, regenerar=False, com_artes=True,
                   versionar=False):
    """Campanha de UM material: estrutura + moldes + artes + cronogramas."""
    base = Path(base) if base is not None else DIR_OUTPUT
    dir_obra = TO.dir_obra(slug, base)
    if not (dir_obra / "config_obra.json").exists():
        print(f"[ERRO] material nao encontrado: {slug}")
        return None
    ctx = CP.contexto_material(slug, base)
    ctx["__regenerar__"] = regenerar
    raiz = CP.dir_campanha_material(slug, base)
    if versionar and raiz.exists():
        prefixo = f"campanhas-{CP.nome_material(slug, base)}"
        arquivado = TO.arquivar_para_versoes(raiz, CP.dir_versoes(slug, base),
                                             prefixo)
        print(f"[campanha] versao anterior arquivada em {arquivado}")
    criadas = []
```

(o resto da função, a partir de `for pasta in CP.estrutura_material(ctx):`,
permanece igual.)

Editar a assinatura e o corpo de `gerar_completo` (linhas 688-696):

```python
def gerar_completo(chave, base=None, regenerar=False, com_artes=True,
                   versionar=False):
    """Campanha de TODA a colecao: itera os membros do manifesto + campanha.json."""
    base = Path(base) if base is not None else DIR_OUTPUT
    manifesto = CP.carregar_manifesto_colecao(chave, base)
    if not manifesto:
        print(f"[ERRO] manifesto da colecao '{chave}' nao encontrado. "
              f"Rode 'python scripts/colecao.py --sincronizar' primeiro.")
        return None
    raiz_campanhas = base / chave / "campanhas"
    if versionar and raiz_campanhas.exists():
        arquivado = TO.arquivar_para_versoes(
            raiz_campanhas, base / chave / "versoes", "campanhas")
        print(f"[campanha] versao anterior arquivada em {arquivado}")
    nucleo = manifesto.get("nucleo", {})
```

(o resto da função permanece igual — a partir de `identidade = {`.)

Editar `main()` (linhas 815-853): adicionar a flag e propagá-la nas duas
chamadas:

```python
    ap.add_argument("--regenerar", action="store_true",
                    help="sobrescreve moldes ja editados")
    ap.add_argument("--versionar", action="store_true",
                    help="arquiva a campanha existente em versoes/ antes de gerar uma nova (R17)")
    ap.add_argument("--sem-artes", action="store_true",
                    help="nao renderiza PNGs (apenas HTML fonte das artes)")
```

```python
    if args.material:
        if args.marcar_completa:
            ok = marcar_completa(args.material)
            print(f"[campanha] {args.material} marcado como completa (ja existia: {ok})")
            return
        gerar_material(args.material, regenerar=args.regenerar,
                       com_artes=not args.sem_artes, versionar=args.versionar)
        return
```

```python
    gerar_completo(colecao, regenerar=args.regenerar,
                   com_artes=not args.sem_artes, versionar=args.versionar)
```

- [ ] **Step 4: Rodar e confirmar sucesso**

Run: `python -m pytest tests/test_campanha.py -v`
Expected: PASS (toda a classe `TestVersionar` + todos os testes já existentes
no arquivo, sem regressão).

- [ ] **Step 5: Suíte completa (R16) + commit**

Run: `python -m pytest -q`
Expected: 100% verde.

```bash
git add scripts/criar-campanha.py tests/test_campanha.py
git commit -m "feat: --versionar em criar-campanha.py arquiva a campanha existente antes de recriar (R17)"
```

---

### Task 5: `criar-maquina-vendas.py` — flags `--versionar` e `--forcar`

**Files:**
- Modify: `scripts/criar-maquina-vendas.py:282-318` (`criar_maquina`),
  `:524-543` (`main`)
- Test: `tests/test_maquina_colecao.py` (nova classe
  `TestVersionarESobrescrever`)

**Interfaces:**
- Consumes: `TO.arquivar_para_versoes` (Task 2).
- Produces: `criar_maquina(slug, tipo="completo", versionar=False,
  forcar=False)`. CLI ganha `--versionar`/`--forcar`. Consumido pela Task 7
  (comando `/criar-maquina`).

- [ ] **Step 1: Escrever os testes que falham**

Em `tests/test_maquina_colecao.py`, adicionar:

```python
class TestVersionarESobrescrever:
    def test_versionar_arquiva_a_existente_e_recria_do_zero(self, ambiente):
        raiz = ambiente["raiz"]
        gerador.criar_maquina("meu-hub/livros/l1-x", tipo="completo")
        (raiz / "meu-hub" / "maquina" / "marca.txt").write_text(
            "v1", encoding="utf-8")

        destino = gerador.criar_maquina("meu-hub/livros/l1-x", tipo="completo",
                                        versionar=True)

        assert destino is not None
        assert not (destino / "marca.txt").exists(), "canonico recriado do zero"
        versao = raiz / "meu-hub" / "versoes" / "maquina-v1"
        assert (versao / "marca.txt").is_file()
        assert (versao / "manifesto.json").is_file()

    def test_versionar_duas_vezes_incrementa(self, ambiente):
        raiz = ambiente["raiz"]
        gerador.criar_maquina("meu-hub/livros/l1-x", tipo="completo")
        gerador.criar_maquina("meu-hub/livros/l1-x", tipo="completo",
                              versionar=True)
        gerador.criar_maquina("meu-hub/livros/l1-x", tipo="completo",
                              versionar=True)

        dir_versoes = raiz / "meu-hub" / "versoes"
        assert (dir_versoes / "maquina-v1").is_dir()
        assert (dir_versoes / "maquina-v2").is_dir()

    def test_forcar_sobrescreve_sem_perguntar(self, ambiente, monkeypatch):
        raiz = ambiente["raiz"]
        gerador.criar_maquina("meu-hub/livros/l1-x", tipo="completo")

        def _explode(*a, **k):
            raise AssertionError("input() nao deveria ser chamado com --forcar")
        monkeypatch.setattr("builtins.input", _explode)

        destino = gerador.criar_maquina("meu-hub/livros/l1-x", tipo="completo",
                                        forcar=True)

        assert destino is not None
        assert not (raiz / "meu-hub" / "versoes").exists(), "forcar nao versiona"

    def test_regra_1por1_vence_mesmo_com_versionar(self, ambiente):
        gerador.criar_maquina("meu-hub/livros/l1-x", tipo="completo")
        resultado = gerador.criar_maquina("meu-hub/livros/l2-x", tipo="completo",
                                          versionar=True)
        assert resultado is None
```

- [ ] **Step 2: Rodar e confirmar falha**

Run: `python -m pytest tests/test_maquina_colecao.py -k TestVersionarESobrescrever -v`
Expected: FAIL — `TypeError: criar_maquina() got an unexpected keyword
argument 'versionar'`.

- [ ] **Step 3: Implementar**

Em `scripts/criar-maquina-vendas.py`, editar a assinatura de `criar_maquina`
(linha 282) e o bloco `if destino.exists():` (linhas 282-318):

```python
def criar_maquina(slug: str, tipo: str = "completo", versionar: bool = False,
                  forcar: bool = False):
    """Função principal: cria a máquina de vendas."""
    # UTF-8 no Windows (cp1252 quebra emojis do banner) — não depender só do main()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    titulo = slug_para_titulo(slug)
    obra_info = verificar_obra_existe(slug)
    destino = dir_maquina(slug)
    hub = _hub_da_obra(slug)

    print(f"\n{'='*60}")
    print(f"  CRIANDO MÁQUINA DE VENDAS: {titulo}")
    print(f"  Tipo: {tipo}")
    print(f"  Coleção (hub): {hub}")
    print(f"  Destino: {destino}")
    print(f"{'='*60}\n")

    if destino.exists():
        # Regra 1:1 — a máquina do hub pertence a UMA obra. Outra obra da mesma
        # coleção NÃO pode sobrescrever; mesma obra segue com confirmação.
        man_existente = _ler_json(destino / "manifesto.json")
        obra_anterior = man_existente.get("obra_origem", "")
        obra_atual = obra_info.get("path", "")
        if obra_anterior and obra_atual and obra_anterior != obra_atual:
            print(f"  ⛔ Regra 1:1 — a coleção '{hub}' já tem máquina de outra obra:")
            print(f"     existente: {obra_anterior}")
            print(f"     solicitada: {obra_atual}")
            print(f"  (1 máquina por coleção em output/<slug-colecao>/maquina — "
                  f"use outra coleção ou remova a existente)")
            return None
        if versionar:
            arquivada = TO.arquivar_para_versoes(destino, destino.parent / "versoes",
                                                 "maquina")
            print(f"  📦 Versão anterior arquivada em {arquivada} (R17 — Criar Nova)")
        else:
            if not forcar:
                resp = input(f"  ⚠️  Diretório {destino} já existe. Sobrescrever? (s/N): ")
                if resp.lower() != "s":
                    print("  Cancelado.")
                    return None
            shutil.rmtree(destino)
```

(o resto da função, a partir de `# Placeholders para substituição nos
templates`, permanece igual.)

Editar `main()` (linhas 524-543):

```python
def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if len(sys.argv) < 2:
        print("Uso: python scripts/criar-maquina-vendas.py <slug> "
              "[--tipo completo|parcial|landing|backend] [--versionar|--forcar]")
        print("\nExemplo:")
        print("  python scripts/criar-maquina-vendas.py observabilidade-sistemas-distribuidos")
        sys.exit(1)

    slug = sys.argv[1]
    tipo = "completo"

    if "--tipo" in sys.argv:
        idx = sys.argv.index("--tipo")
        if idx + 1 < len(sys.argv):
            tipo = sys.argv[idx + 1]

    versionar = "--versionar" in sys.argv
    forcar = "--forcar" in sys.argv

    criar_maquina(slug, tipo, versionar=versionar, forcar=forcar)
```

- [ ] **Step 4: Rodar e confirmar sucesso**

Run: `python -m pytest tests/test_maquina_colecao.py -v`
Expected: PASS (toda a classe nova + todos os testes já existentes, sem
regressão — em especial `test_1por1_recusa_segunda_obra_do_mesmo_hub` e
`test_mesma_obra_pode_sobrescrever`, que exercitam o caminho SEM
`--versionar`/`--forcar`).

- [ ] **Step 5: Suíte completa (R16) + commit**

Run: `python -m pytest -q`
Expected: 100% verde.

```bash
git add scripts/criar-maquina-vendas.py tests/test_maquina_colecao.py
git commit -m "feat: --versionar e --forcar em criar-maquina-vendas.py (R17)"
```

---

### Task 6: `colecao.py` — `versoes_arquivadas` derivado no manifesto

**Files:**
- Modify: `scripts/colecao.py:81-116` (inserir `_versoes_arquivadas` perto de
  `_info_maquina`), `:217-253` (`montar_manifesto`), `:302-326` (`_imprimir`)
- Test: `tests/test_colecao_hub.py` (nova classe `TestVersoesArquivadas`),
  `tests/test_maquina_colecao.py` (novo teste em `TestEmpacotamento`)

**Interfaces:**
- Consumes: nada novo (lê disco direto, mesmo padrão de `_info_maquina`).
- Produces: `manifesto["versoes_arquivadas"]` — lista de nomes de pasta
  (`["campanhas-v1", "maquina-v1"]`, ordenada) ou `[]`.

- [ ] **Step 1: Escrever os testes que falham**

Em `tests/test_colecao_hub.py`, adicionar (usa a fixture `ambiente` já
existente no arquivo, que devolve `raiz` e tem o hub `meu-hub` com a coleção
`"Minha Coleção"` e a coleção plana `"Colecao Plana"`):

```python
class TestVersoesArquivadas:
    def test_sem_pasta_versoes_manifesto_lista_vazio(self, ambiente):
        colecao.sincronizar()
        man = colecao.carregar("Minha Coleção")
        assert man["versoes_arquivadas"] == []

    def test_versoes_arquivadas_aparecem_no_manifesto(self, ambiente):
        raiz = ambiente
        (raiz / "meu-hub" / "versoes" / "campanhas-v1").mkdir(parents=True)
        (raiz / "meu-hub" / "versoes" / "maquina-v1").mkdir(parents=True)
        colecao.sincronizar()
        man = colecao.carregar("Minha Coleção")
        assert man["versoes_arquivadas"] == ["campanhas-v1", "maquina-v1"]

    def test_colecao_sem_hub_nao_lista_versoes(self, ambiente):
        colecao.sincronizar()
        man = colecao.carregar("Colecao Plana")
        assert man["versoes_arquivadas"] == []
```

Em `tests/test_maquina_colecao.py`, adicionar dentro de `class
TestEmpacotamento`:

```python
    def test_pacote_nao_inclui_versoes_arquivadas(self, ambiente,
                                                   colecao_redirecionada,
                                                   monkeypatch):
        raiz = ambiente["raiz"]
        gerador.criar_maquina("meu-hub/livros/l1-x", tipo="completo")
        gerador.criar_maquina("meu-hub/livros/l1-x", tipo="completo",
                              versionar=True)
        colecao.sincronizar()

        monkeypatch.setattr(empacotador, "DIR_OUTPUT", raiz)
        monkeypatch.setattr(empacotador, "DIR_PACOTES", raiz / "distribuicao")
        meta = empacotador.empacotar("Minha Coleção")
        assert meta is not None

        pacote = raiz / meta["pacote"]
        assert not (pacote / "versoes").exists(), (
            "versoes arquivadas nao vao no pacote de distribuicao")
```

- [ ] **Step 2: Rodar e confirmar falha**

Run: `python -m pytest tests/test_colecao_hub.py -k TestVersoesArquivadas tests/test_maquina_colecao.py -k test_pacote_nao_inclui_versoes_arquivadas -v`
Expected: FAIL — `KeyError: 'versoes_arquivadas'` nos 3 testes de
`test_colecao_hub.py` (o teste do pacote já passa hoje, sem nenhuma mudança —
`empacotar-colecao.py` só copia artefatos da whitelist de membros/`maquina/`,
nunca a pasta inteira do hub; ele serve de guarda de regressão).

- [ ] **Step 3: Implementar**

Em `scripts/colecao.py`, inserir depois de `_info_maquina` (depois da linha
115, antes de `def _todos_dirs_manifestos():`):

```python
def _versoes_arquivadas(hub):
    """Versoes arquivadas de campanha/maquina no hub (output/<hub>/versoes/*).

    Campo DERIVADO (nunca escrito a mao): --versionar move a pasta canonica
    para ca antes de recriar; o manifesto so lista o que ja esta no disco."""
    if not hub:
        return []
    dir_versoes = DIR_OUTPUT / hub / "versoes"
    if not dir_versoes.is_dir():
        return []
    return sorted(p.name for p in dir_versoes.iterdir() if p.is_dir())
```

Em `montar_manifesto` (linhas 217-253), adicionar a chamada e o campo:

```python
def montar_manifesto(chave, membros, metadados=None):
    raizes = [m for m in membros if not TO.campo(m["tipo"], "derivado_de", ())]
    nucleo = raizes[0] if raizes else (membros[0] if membros else {})
    motivo = {}
    if nucleo:
        motivo = _ler_json(TO.dir_obra(nucleo["slug"], DIR_OUTPUT) / "sumario_macro.json") \
            .get("motivo_condutor", {})

    faltantes = [t for t in TO.tipos_derivados()
                 if t not in {m["tipo"] for m in membros}]
    sem_cta = [m["slug"] for m in membros
               if TO.campo(m["tipo"], "exige_cta") and not m["cta_url"]]
    hub = _hub_da_colecao(membros)
    maquina, maquinas_legadas = _info_maquina(hub)

    manifesto = {
        "colecao": chave,
        "cor_accent": resolver_cor(chave),
        "atualizado_em": date.today().isoformat(),
        "nucleo": {
            "slug": nucleo.get("slug", ""),
            "tipo": nucleo.get("tipo", ""),
            "titulo": nucleo.get("titulo", ""),
            "senioridade": nucleo.get("senioridade", ""),
            "motivo_condutor": motivo,
        },
        "total_membros": len(membros),
        "por_tipo": {t: sum(1 for m in membros if m["tipo"] == t)
                     for t in sorted({m["tipo"] for m in membros})},
        "membros": sorted(membros, key=lambda m: (m["tipo"], m["slug"])),
        "derivados_ausentes": faltantes,
        "membros_sem_cta": sem_cta,
        "maquina": maquina,
        "maquinas_legadas": maquinas_legadas,
        "versoes_arquivadas": _versoes_arquivadas(hub),
    }
    if metadados:
        manifesto["metadados"] = metadados
    return manifesto
```

(a única mudança de lógica é computar `hub` uma vez e reusar — antes
`_info_maquina(_hub_da_colecao(membros))` chamava `_hub_da_colecao` inline.)

Em `_imprimir` (depois do bloco `legadas`, linhas 323-325):

```python
    legadas = manifesto.get("maquinas_legadas") or []
    if legadas:
        print(f"  [!] Maquinas legadas em marketing/: {', '.join(legadas)}")
    versoes = manifesto.get("versoes_arquivadas") or []
    if versoes:
        print(f"  [i] Versoes arquivadas em versoes/: {', '.join(versoes)}")
```

- [ ] **Step 4: Rodar e confirmar sucesso**

Run: `python -m pytest tests/test_colecao_hub.py tests/test_maquina_colecao.py -v`
Expected: PASS (todos, incluindo os novos e os já existentes — em especial os
de `TestManifestoDaColecao` que já checam outras chaves do mesmo manifesto).

- [ ] **Step 5: Suíte completa (R16) + commit**

Run: `python -m pytest -q`
Expected: 100% verde.

```bash
git add scripts/colecao.py tests/test_colecao_hub.py tests/test_maquina_colecao.py
git commit -m "feat: versoes_arquivadas derivado no manifesto da colecao (R17)"
```

---

### Task 7: Docs — entrevista opcional + protocolo Nova/Sobrescrever

**Files:**
- Modify: `.claude/commands/esbocar.md`
- Modify: `.claude/commands/produzir-obra-completa.md`
- Modify: `.claude/commands/campanha.md`
- Modify: `.claude/commands/campanha-completa.md`
- Modify: `.claude/commands/criar-maquina.md`

**Interfaces:**
- Consumes: `config_obra.json["gerar_campanha"/"gerar_maquina"]` (Task 1),
  flags `--versionar` (Task 4), `--versionar`/`--forcar` (Task 5).
- Produces: nada consumido por código — são instruções para o orquestrador
  (LLM) seguir na próxima sessão de uso desses comandos.

Este task não tem teste automatizado próprio (são arquivos `.md` de prompt).
A verificação é: (1) suíte completa continua 100% verde (nada em `scripts/`
foi tocado); (2) checagem textual de que os termos-chave da R17 aparecem nos 5
arquivos.

- [ ] **Step 1: `.claude/commands/esbocar.md` — 2 perguntas novas na Rodada 1**

Na tabela da "Rodada 1" (depois da linha `| Artigos | Deseja gerar artigos
científicos a partir do tema? | Sim \| Não (Recommended) |`), adicionar:

```
| Campanha | Deseja incluir a etapa de CAMPANHA de divulgação no fluxo desta coleção? | Sim \| Não (Recommended) |
| Máquina | Deseja incluir a etapa de MÁQUINA DE VENDAS no fluxo desta coleção? | Sim \| Não (Recommended) |
```

No bloco JSON do "Passo 2" (schema de `config_obra.json`), depois da linha
`"cta_texto": "Quero a obra completa",`, adicionar:

```
  "gerar_campanha": false,
  "gerar_maquina": false,
```

No final do "Passo 4", depois da lista de comandos disponíveis, adicionar:

```
CAMPANHA e MÁQUINA são OPCIONAIS (R17, CLAUDE.md) — a escolha desta entrevista
vira `gerar_campanha`/`gerar_maquina` em `config_obra.json` e decide se
`/produzir-obra-completa` inclui esses fluxos automaticamente. Independente da
resposta, `/campanha-completa` e `/criar-maquina` podem ser disparados a
qualquer momento depois.
```

- [ ] **Step 2: `.claude/commands/produzir-obra-completa.md` — fluxos 2/3
  condicionais**

No diagrama do topo ("Visão Geral dos 3 Fluxos"), trocar:

```
│  FLUXO 2: CAMPANHAS (V5.3)                                  │
│  /campanha-completa → artes, textos, cronogramas             │
└───────────────────────────────┬─────────────────────────────┘
                                │
                                ▼ OBRIGATÓRIO
┌─────────────────────────────────────────────────────────────┐
│  FLUXO 3: MÁQUINA DE VENDAS (full-stack)                    │
```

por:

```
│  FLUXO 2: CAMPANHAS (V5.3)                                  │
│  /campanha-completa → artes, textos, cronogramas             │
└───────────────────────────────┬─────────────────────────────┘
                                │
                                ▼ OPCIONAL (config_obra.gerar_campanha, R17)
┌─────────────────────────────────────────────────────────────┐
│  FLUXO 3: MÁQUINA DE VENDAS (full-stack)                    │
```

E a seta que introduz o Fluxo 2 (linha `▼ OBRIGATÓRIO` acima de "FLUXO 2:
CAMPANHAS") por `▼ OPCIONAL (config_obra.gerar_campanha, R17)`.

Trocar o título "## Passo 3 — Campanhas (FLUXO 2: CAMPANHAS) ← OBRIGATÓRIO"
por "## Passo 3 — Campanhas (FLUXO 2: CAMPANHAS) ← OPCIONAL (R17)" e inserir,
como primeiro parágrafo do passo (antes do item numerado 10 já existente):

```
Antes de gerar, leia `gerar_campanha` de `config_obra.json`. Se `false`, pule
este passo inteiro e registre no relatório consolidado como `⏭️ PULADO —
operador optou por não incluir CAMPANHA na entrevista (/campanha-completa
<slug> para adicionar depois)` — isso NUNCA é tratado como falha. Se `true`,
continue abaixo.

Antes de rodar `criar-campanha.py --completo`, verifique se
`output/<colecao>/campanhas/campanha.json` já existe. Se existir, pergunte via
`AskUserQuestion` (header "Ação", pergunta "Já existe CAMPANHA para a coleção
'<colecao>'. O que deseja fazer?"): **Criar Nova** (Recommended — mantém a
existente arquivada em `versoes/` e a nova passa a ser a atual) ou
**Sobrescrever Existente** (substitui no lugar). Rode o comando com
`--versionar` (Criar Nova) ou `--regenerar` (Sobrescrever). Se não existir
nada ainda, rode normal, sem perguntar.
```

Trocar o título "## Passo 4 — Máquina de Vendas (FLUXO 3: MÁQUINA) ←
OBRIGATÓRIO" por "## Passo 4 — Máquina de Vendas (FLUXO 3: MÁQUINA) ←
OPCIONAL (R17)" e inserir, como primeiro parágrafo do passo (antes do item
numerado 13 já existente):

```
Antes de gerar, leia `gerar_maquina` de `config_obra.json`. Se `false`, pule
este passo inteiro e registre no relatório consolidado como `⏭️ PULADO —
operador optou por não incluir MÁQUINA na entrevista (/criar-maquina <slug>
para adicionar depois)` — isso NUNCA é tratado como falha. Se `true`,
continue abaixo.

Antes de rodar `criar-maquina-vendas.py`, verifique se
`output/<slug-colecao>/maquina/manifesto.json` já existe. Se existir,
pergunte via `AskUserQuestion` (header "Ação", pergunta "Já existe MÁQUINA
para a coleção '<colecao>'. O que deseja fazer?"): **Criar Nova**
(Recommended — mantém a existente arquivada em `versoes/` e a nova passa a
ser a atual) ou **Sobrescrever Existente** (substitui no lugar). Rode o
comando com `--versionar` (Criar Nova) ou `--forcar` (Sobrescrever). Se não
existir nada ainda, rode normal, sem perguntar.
```

Na seção "Notas de Economia de Tokens" (final do arquivo), trocar a última
linha:

```
- Se o operador só quer materiais, use `/criar-livro` (não este comando).
```

por:

```
- Campanha e Máquina são OPCIONAIS (R17) — se `gerar_campanha`/`gerar_maquina`
  forem `false` na entrevista, os Fluxos 2/3 são pulados sem custo e sem
  contar como falha.
- Se o operador só quer materiais, use `/criar-livro` (não este comando).
```

- [ ] **Step 3: `.claude/commands/campanha.md` — protocolo Nova/Sobrescrever**

Inserir uma nova seção "## Passo 0 — Já existe CAMPANHA para este material?"
antes do atual "## Passo 1 — Estrutura, moldes, artes e cronogramas (0
token)":

```
## Passo 0 — Já existe CAMPANHA para este material?

Verifique se `output/<colecao>/campanhas/<material-slug>/` já tem conteúdo.
Se existir, pergunte via `AskUserQuestion` (header "Ação", pergunta "Já existe
CAMPANHA para '<material-slug>'. O que deseja fazer?"): **Criar Nova**
(Recommended — arquiva a existente em `versoes/campanhas-<material-slug>-v{N}/`
e recria do zero) ou **Sobrescrever Existente** (substitui no lugar). Passe o
resultado ao Passo 1 como `--versionar` ou `--regenerar`. Se não existir nada
ainda, pule este passo e rode o Passo 1 normal.
```

- [ ] **Step 4: `.claude/commands/campanha-completa.md` — protocolo
  Nova/Sobrescrever**

Inserir a mesma seção, adaptada para a coleção inteira, antes do atual
"## Passo 1 — Estrutura, moldes, artes e cronogramas (0 token)":

```
## Passo 0 — Já existe CAMPANHA para esta coleção?

Verifique se `output/<colecao>/campanhas/campanha.json` já existe. Se existir,
pergunte via `AskUserQuestion` (header "Ação", pergunta "Já existe CAMPANHA
para a coleção '<colecao>'. O que deseja fazer?"): **Criar Nova**
(Recommended — arquiva a existente em `versoes/campanhas-v{N}/` e recria do
zero) ou **Sobrescrever Existente** (substitui no lugar). Passe o resultado ao
Passo 1 como `--versionar` ou `--regenerar`. Se não existir nada ainda, pule
este passo e rode o Passo 1 normal.
```

- [ ] **Step 5: `.claude/commands/criar-maquina.md` — protocolo
  Nova/Sobrescrever**

No "## Fluxo", entre o item 1 ("Verifica se a obra existe em `output/`") e o
item 2 ("Exibe resumo da obra e pergunta confirmação"), inserir um novo item:

```
2. Verifica se `output/<slug-colecao>/maquina/manifesto.json` já existe. Se
   existir, pergunta via `AskUserQuestion` (header "Ação", pergunta "Já
   existe MÁQUINA para a coleção '<colecao>'. O que deseja fazer?"):
   **Criar Nova** (Recommended — arquiva a existente em
   `versoes/maquina-v{N}/` e recria do zero) ou **Sobrescrever Existente**
   (substitui no lugar). Se não existir nada ainda, pula esta pergunta.
```

(renumerar os itens seguintes: o antigo item 2 vira 3, e assim por diante até
o antigo item 7 virar 8) e adicionar `--versionar`/`--forcar` na chamada do
item 3 (antigo 2):

```
3. Executa `python scripts/criar-maquina-vendas.py <slug> --tipo <tipo>
   [--versionar|--forcar]` (flag escolhida no item 2)
```

- [ ] **Step 6: Rodar a suíte completa (nenhum `.py` foi tocado)**

Run: `python -m pytest -q`
Expected: 100% verde (mesmo resultado da Task 6 — este task é doc-only).

- [ ] **Step 7: Checagem textual das 5 docs**

Run:
```bash
grep -l "OPCIONAL" .claude/commands/produzir-obra-completa.md
grep -l "gerar_campanha" .claude/commands/esbocar.md
grep -l "Criar Nova" .claude/commands/campanha.md .claude/commands/campanha-completa.md .claude/commands/criar-maquina.md
```
Expected: os 5 arquivos aparecem exatamente uma vez cada, sem erro.

- [ ] **Step 8: Commit**

```bash
git add .claude/commands/esbocar.md .claude/commands/produzir-obra-completa.md \
        .claude/commands/campanha.md .claude/commands/campanha-completa.md \
        .claude/commands/criar-maquina.md
git commit -m "docs: CAMPANHA/MAQUINA opcionais + protocolo Nova/Sobrescrever (R17)"
```

---

## Depois do Task 7

Rodar `git log --oneline -7` para confirmar os 7 commits, depois seguir o
fluxo de fechamento de sessão do projeto (`gerar-relatorio-sessao`, R16 já
satisfeita em cada task) antes do `git push`.
