# CAMPANHAS — nova camada de materiais da COLEÇÃO

> Data: 2026-08-09 · Status: aprovado para implementação · Esforço: 1 sessão

## Problema

A COLEÇÃO entrega livros, TCCs, artigos, e-books, playbooks, lead magnets, decks e
e-mails — mas não dá à publicação **material de divulgação**: posts, artes para
redes sociais, sequências de WhatsApp/e-mail e cronogramas. Hoje cada autor teria
de escrever isso à mão, fora da fábrica.

## Objetivos

1. Cada COLEÇÃO tem sua **CAMPANHA exclusiva** (derivada do núcleo canônico e da
   identidade visual da coleção: cores, badge de nível, vocabulário condutor, CTA).
2. `/campanha <slug>` gera os artefatos de campanha de **um material** (livro, TCC,
   artigo, e-book, playbook, lead magnet, deck — materiais com `config_obra.json`).
3. `/campanha-completa [colecao]` gera os artefatos de campanha de **todos os
   materiais da coleção de uma vez** (via manifesto da coleção) + `campanha.json`.
4. Artefatos: textos (posts, respostas, sequências), **artes** (HTML+CSS→Chromium,
   custo zero, identidade 100% da coleção), templates e cronogramas.

## Decisões de design

- **Local:** `output/<slug-colecao>/campanhas/` — dentro do HUB por coleção
  (regra AGENTS.md: nada plano no topo). Empacotável por `empacotar-colecao.py`.
- **Artes:** HTML+CSS→Chromium (Playwright `page.screenshot`), mesmo motor do deck
  e do lead magnet. Custo zero, badge/cores/CTA da coleção garantidos.
- **Organização:** subpasta por material — `campanhas/<material-slug>/`, cada uma
  com a árvore `redes-sociais/` + `canais-comunicacao/` definida pelo operador.
- **Registro declarativo** em `scripts/campanha.py` (espelho do `tipos_obra.py`):
  canais, formatos, dimensões e natureza. Artefato novo = 1 linha no registro.
- **Campanha não é tipo de obra:** não entra em `tipos_obra.py` (não tem capa,
  PDF único nem dispatch de obra). É camada própria, como a máquina de vendas.
- **Textos:** o script gera **rascunhos determinísticos** (extraídos do
  `config_obra.json` + `sumario_macro.json` + manifesto: título, badge, 3
  benefícios, vocabulário condutor, CTA) em moldes `.md`; o comando orquestra o
  agente para reescrever a copy final com LLM (custo baixo). Gate anti-copy
  genérica (regra 12): `Autor Digital|centenas de pessoas` reprova.

## Estrutura gerada (por material)

```
output/<slug-colecao>/campanhas/
├── campanha.json                          # manifesto da campanha (por coleção)
└── <material-slug>/
    ├── redes-sociais/
    │   ├── instagram/
    │   │   ├── artes/feed-story/          # story-01.png (1080×1920)
    │   │   ├── artes/post/                # post-01.png (1080×1350)
    │   │   ├── textos/feed-story/         # rascunho.md (rascunho + molde)
    │   │   ├── textos/post/               # post-01.md .. post-03.md
    │   │   ├── textos/resposta-direct/    # resposta-direct.md
    │   │   ├── templates/                 # cópia do HTML de arte
    │   │   └── cronograma-divulgacao/     # cronograma-ig.md (14 dias)
    │   └── linkedin/
    │       ├── artes/post/                # post-01.png (1200×628)
    │       ├── textos/post/               # post-01.md, post-02.md
    │       ├── textos/resposta-direct/
    │       ├── templates/
    │       └── cronograma-divulgacao/     # cronograma-li.md (14 dias)
    └── canais-comunicacao/
        ├── emails/
        │   ├── sequencia-nutricao/        # templates/ + textos/ + cronograma (30 dias)
        │   └── sequencia-mkt/             # templates/ + textos/ + cronograma (30 dias)
        └── whatsapp/
            ├── sequencia-nutricao/        # artes/ + textos/ + cronograma (14 dias)
            └── sequencia-divulgacao/      # artes/ + textos/ + cronograma (14 dias)
```

## Registro declarativo (`scripts/campanha.py`)

```python
REDES_SOCIAIS = {
    "instagram": {
        "artes": {"feed-story": (1080, 1920), "post": (1080, 1350)},
        "textos": ["feed-story", "post", "resposta-direct"],
        "templates": True, "cronograma_dias": 14,
    },
    "linkedin": {
        "artes": {"post": (1200, 628)},
        "textos": ["post", "resposta-direct"],
        "templates": True, "cronograma_dias": 14,
    },
}
CANAIS_COMUNICACAO = {
    "emails": {
        "sequencia-nutricao": {"templates": True, "textos": 4, "cronograma_dias": 30},
        "sequencia-mkt":      {"templates": True, "textos": 3, "cronograma_dias": 30},
    },
    "whatsapp": {
        "sequencia-nutricao":  {"artes": 1, "textos": 4, "cronograma_dias": 14},
        "sequencia-divulgacao":{"artes": 1, "textos": 6, "cronograma_dias": 14},
    },
}
```

## Componentes

| Arquivo | Papel |
|---|---|
| `scripts/campanha.py` | registro declarativo + resolução (material → hub → pasta campanha) |
| `scripts/criar-campanha.py` | CLI: `--material`, `--completo [colecao]`, `--regenerar`, `--sem-artes` |
| `scripts/validar-campanha.py` | gates R-CP-1..5: estrutura, conteúdo, artes, mérito (`--estrito`), completude (`--completo`) |
| `templates/campanha/*.html` | artes: `arte-post-ig.html`, `arte-feed-story-ig.html`, `arte-post-linkedin.html`, `arte-whatsapp.html` (variáveis: titulo, beneficio, cor_accent, badge, cta, slug) |
| `.claude/commands/campanha.md` | `/campanha <slug>` — script → agente reescreve copy → gate → relatório |
| `.claude/commands/campanha-completa.md` | `/campanha-completa [colecao]` — itera manifesto + `campanha.json` |

## Fluxo

1. `/campanha <slug>`: `criar-campanha.py --material <slug>` → estrutura + rascunhos
   + artes (Chromium) + cronogramas (datas reais a partir de hoje).
2. Agente reescreve a copy dos moldes (LLM, tom de divulgação, vocabulário da coleção).
3. `validar-campanha.py --material <slug> --estrito` — reprova se copy genérica.
4. `/campanha-completa`: repete 1-3 para cada membro do manifesto + escreve
   `campanha.json` (coleção, identidade, materiais com status, data).

## Validação (`validar-campanha.py`)

- **R-CP-1** estrutura: árvore de pastas completa do registro por material.
- **R-CP-2** conteúdo: textos não vazios, sem placeholder de moldes, sem
  `Autor Digital|centenas de pessoas` (regra 12).
- **R-CP-3** artes: PNG com assinatura válida e tamanho mínimo; `--estrito`
  reabre via Chromium (screenshot smoke).
- **R-CP-4** mérito (`--estrito`): vocabulário condutor do manifesto presente na
  copy quando existir.
- **R-CP-5** cronogramas: presentes e com datas futuras.

## Testes

`tests/test_campanha.py` (padrão conftest: `carregar_script`, `livro_falso`,
monkeypatch de `DIR_OUTPUT`): registro, resolução material→pasta campanha,
criação de estrutura completa, `campanha.json` no `--completo`, gates aprovando
material íntegro e reprovando estrutura faltante/copy genérica.

## Integrações

- `colecao.py` **não muda** (campanha não é membro — é derivado da coleção).
- `empacotar-colecao.py`: incluir `campanhas/` se existir (passo de entrega).
- `AGENTS.md`: nota curta + RTK scratchpad.
