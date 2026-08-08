"""Fixtures compartilhadas dos testes da V5.

Garante que `scripts/` esteja no sys.path (os modulos da fabrica se importam
entre si por nome simples) e oferece um helper para carregar scripts cujo nome
tem hifen (nao importaveis por `import`).
"""

import importlib.util
import sys
from pathlib import Path

import pytest

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_SCRIPTS = DIR_PROJETO / "scripts"

if str(DIR_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(DIR_SCRIPTS))


def carregar_script(nome_arquivo, nome_modulo=None):
    """Importa scripts/<nome_arquivo> mesmo com hifen no nome."""
    nome_modulo = nome_modulo or nome_arquivo.replace("-", "_").removesuffix(".py")
    if nome_modulo in sys.modules:
        return sys.modules[nome_modulo]
    spec = importlib.util.spec_from_file_location(nome_modulo, DIR_SCRIPTS / nome_arquivo)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nome_modulo] = mod
    spec.loader.exec_module(mod)
    return mod


# ── Fixtures de conteudo ──────────────────────────────────────────────────────

CAPITULO_EITA = """# Capítulo 1 — Fundação do Projeto

## 1. Introdução

Este capítulo abre o canteiro de obras. O leitor entende por que a fundação
sustenta tudo o que vem depois, e qual é o custo de errar aqui [1].

## 2. Explica

A fundação de um projeto agêntico é o conjunto de contratos que o restante do
sistema assume como verdade. Sem contrato explícito, cada camada inventa o seu.

## 3. Ilustra

Pense no mestre de obras conferindo a planta antes da primeira viga.

```mermaid
graph TD
  A[Planta] --> B[Fundação]
```

## 4. Técnica

### Criar o arquivo de contrato

Grave o contrato em `scripts/contrato.py` e o schema em `config/schema.json`.

```bash
python scripts/contrato.py --iniciar
python scripts/validar-contrato.py --estrito
```

### Registrar no índice

O índice vive em `output/indice.json`.

```python
registro = {"versao": 1}
```

## 5. Aplica

### Exercício Prático

- Criar o arquivo `scripts/contrato.py` com a função `iniciar()`
- Rodar `validar-contrato.py` e obter exit 0
- Registrar a versão 1 no índice
- Confirmar que o índice tem exatamente 1 entrada

### Armadilhas Comuns

- Gravar o contrato fora de `scripts/`, quebrando o import por nome simples
- Esquecer de versionar o schema, o que torna a migração impossível
- Rodar o validador sem `--estrito` e ignorar a falha

## 6. Conclusão

A fundação está pronta e verificável.

## 7. Referências

[1] AUTOR, A. Fundamentos. Editora, 2025.
"""

CAPITULO_SEM_TECNICA = """# Capítulo 2 — Teoria Pura

## 1. Introdução

Abertura do capítulo.

## 2. Explica

Explicação longa sem nenhuma prática associada ao tema.

## 5. Aplica

Nada a executar aqui.

## 6. Conclusão

Fim.
"""


@pytest.fixture
def sumario_macro():
    return {
        "titulo_obra": "A Obra em Construção",
        "introducao": "Um percurso do alicerce à entrega das chaves.",
        "motivo_condutor": {
            "nome": "A Obra em Construção",
            "descricao": "O leitor é o Mestre de Obras de um projeto real.",
            "vocabulario": ["fundação", "estrutura", "acabamento"],
            "persona_leitor": "Mestre de Obras",
        },
        "partes": [
            {
                "parte": "I",
                "titulo_parte": "Alicerce",
                "capitulos": [
                    {"capitulo": "1", "titulo": "Fundação do Projeto",
                     "objetivo": "Estabelecer os contratos que sustentam o sistema",
                     "pilares_previstos": ["Contrato", "Schema", "Índice"]},
                    {"capitulo": "2", "titulo": "Teoria Pura",
                     "objetivo": "Compreender o modelo conceitual",
                     "pilares_previstos": ["Modelo"]},
                ],
            },
        ],
    }


@pytest.fixture
def livro_falso(tmp_path, monkeypatch, sumario_macro):
    """Monta um output/ isolado com um livro-mae de 2 capitulos.

    Redireciona DIR_OUTPUT de todos os modulos da fabrica para o tmp_path, de
    modo que nenhum teste toque em output/ real."""
    import json

    dir_output = tmp_path / "output"
    dir_livro = dir_output / "livros" / "obra-teste"
    (dir_livro / "capitulos").mkdir(parents=True)
    (dir_livro / "imagens").mkdir(parents=True)

    (dir_livro / "capitulos" / "cap_01.md").write_text(CAPITULO_EITA, encoding="utf-8")
    (dir_livro / "capitulos" / "cap_02.md").write_text(CAPITULO_SEM_TECNICA, encoding="utf-8")
    (dir_livro / "sumario_macro.json").write_text(
        json.dumps(sumario_macro, ensure_ascii=False), encoding="utf-8")
    (dir_livro / "config_obra.json").write_text(json.dumps({
        "tema": "A Obra em Construção", "tipo_obra": "livro",
        "min_referencias_por_capitulo": 5, "tamanho_obra": "P",
        "senioridade_obra": "intermediario", "serie": "Colecao Teste",
    }, ensure_ascii=False), encoding="utf-8")

    import tipos_obra
    monkeypatch.setattr(tipos_obra, "DIR_OUTPUT", dir_output, raising=False)

    return {"raiz": dir_output, "slug": "livros/obra-teste", "dir_livro": dir_livro,
            "tmp_path": tmp_path}


@pytest.fixture
def redirecionar_output(monkeypatch):
    """Devolve uma funcao que aponta o DIR_OUTPUT de um modulo para um caminho."""
    def _aplicar(modulo, raiz):
        monkeypatch.setattr(modulo, "DIR_OUTPUT", raiz, raising=False)
        return modulo
    return _aplicar
