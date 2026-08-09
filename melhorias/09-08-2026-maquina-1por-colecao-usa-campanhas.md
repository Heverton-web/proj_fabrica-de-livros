# MÁQUINA DE VENDAS — 1 POR COLEÇÃO, USANDO OS ARTEFATOS DE CAMPANHAS

> Data: 2026-08-09 · Status: aprovado para implementação · Esforço: 1 sessão

## Problema

1. **Sem cardinalidade:** a regra "cada COLEÇÃO tem apenas 1 MÁQUINA DE VENDAS"
   não existe no código. O gerador (`criar-maquina-vendas.py`) escreve em
   `marketing/maquinas/<slug>` (raiz do projeto — caminho morto) e aceita 1
   máquina por OBRA. O hub `analista-financeiro-futuro-odontologia-pt` tem 5
   máquinas em `output/<hub>/marketing/lN-*/`, todas sem vínculo com a coleção.
2. **Máquina ignora campanhas:** a máquina nasce com copy genérica ("Fábrica de
   Livros", "livro-autor-digital", `pay.hotmart.com/XXXXX`) enquanto a coleção
   gera campanhas personalizadas em `output/<hub>/campanhas/` (textos, artes,
   cronogramas, sequências de e-mail/WhatsApp) — que a máquina nunca vê.

## Objetivos

1. **Regra 1:1 implementada no código:** a máquina da COLEÇÃO vive em
   `output/<slug-colecao>/maquina`; uma segunda obra do mesmo hub é recusada.
2. **Máquina consome campanhas:** o gerador copia `output/<hub>/campanhas/` →
   `maquina/campanhas/` (snapshot com `snapshot.json`), tornando os artefatos de
   campanha parte da máquina deployável. O material âncora (a obra passada ao
   gerador) fica registrado no manifesto para o operador usar na personalização.
3. **Coleção registra a máquina:** `colecao.py --sincronizar` grava o campo
   `maquina` no manifesto (slug, status, obra_origem, snapshot de campanhas) e
   lista `maquinas_legadas` (pastas `marketing/` do hub) — aviso não destrutivo.
4. **Pacote de distribuição carrega a máquina** (`empacotar-colecao.py`).

## Decisões de design

- **Destino canônico:** `output/<slug-colecao>/maquina`. O slug-colecao é o HUB
  (primeiro segmento do slug da obra que não seja raiz de tipo nem pasta
  estrutural). Para layout plano (`livros/obra-teste`) o hub é o nome da obra.
- **Cardinalidade 1:1:** se `maquina/` já existe com `obra_origem` DIFERENTE →
  erro sem sobrescrever (a máquina pertence a outra obra do mesmo hub). Mesma
  obra → confirmação de sobrescrever (comportamento atual).
- **Campanha como fonte; máquina como consumidora:** o gerador faz SNAPSHOT
  integral (`maquina/campanhas/`), não link — a máquina deplora fora do repo da
  fábrica (VPS/Vercel) e precisa de cópia. O mapeamento fino com o motor
  (templates/emails, posts, dm) é feito na personalização por nicho, usando o
  material âncora registrado no manifesto.
- **Manifesto da máquina** ganha: `colecao`, `maquina_em`, `campanhas`
  (`snapshot`, `atualizado_em`, `material_ancora`).
- **Migração não destrutiva:** máquinas legadas em `output/<hub>/marketing/`
  não são apagadas; aparecem em `maquinas_legadas` no manifesto da coleção para
  o operador decidir.
- **Consolidação de e-mails** (3 fontes hoje: `templates/emails/` do template,
  `campanhas/*/canais-comunicacao/emails/`, `output/<hub>/emails/`): decisão
  registrada — campanhas é a fonte única para a máquina; `output/<hub>/emails/`
  alimenta campanhas. Execução em sessão futura (não bloqueia esta entrega).

## Estrutura gerada

```
output/<slug-colecao>/maquina/            # 1 por coleção (regra 1:1)
├── manifesto.json                        # + colecao, maquina_em, campanhas
├── frontend/  backend/  database/  config/  scripts/  templates/
└── campanhas/                            # snapshot de output/<hub>/campanhas/
    ├── campanha.json
    ├── snapshot.json                     # origem, atualizado_em, materiais, copiado_em
    └── <material-slug>/…
```

## Componentes

| Arquivo | Papel |
|---|---|
| `scripts/criar-maquina-vendas.py` | destino `output/<hub>/maquina`, regra 1:1, snapshot de campanhas |
| `scripts/colecao.py` | campo `maquina` + `maquinas_legadas` no manifesto |
| `scripts/empacotar-colecao.py` | copia `maquina/` para o pacote de distribuição |
| `.claude/commands/criar-maquina.md` | caminho novo, regra 1:1, uso de campanhas no gate R12 |
| `.claude/skills/sincronizar-maquina-vendas/SKILL.md` | caminho novo + passo de re-snapshot de campanhas |
| `.github/copilot-instructions.md` | estrutura do hub (item máquina) + scratchpad RTK |
| `SPEC_MAQUINA_VENDAS.md`, `docs/guia-execucao-maquina-vendas.md`, `docs/manual-completo-fabrica.md` | caminhos atualizados |

## Fluxo

1. `/criar-maquina <slug-da-obra>`: `criar-maquina-vendas.py <slug>`.
2. Resolve o hub da coleção a partir do slug → `output/<hub>/maquina`.
3. Se `maquina/` existe com outra `obra_origem` → erro (regra 1:1).
4. Copia template → manifesto → conteúdo da obra → banco → `.mcp.json`.
5. Se `output/<hub>/campanhas/` existe → snapshot em `maquina/campanhas/` +
   `snapshot.json`; `material_ancora` = nome da obra no manifesto.
6. Personalização por nicho usa o snapshot (gate regra 12 vira:
   `grep -rn 'Autor Digital\|centenas de pessoas' frontend/ templates/ campanhas/ README.md`
   → vazio).
7. `colecao.py --sincronizar` registra `maquina` + `maquinas_legadas`.
8. `empacotar-colecao.py` inclui `maquina/` no pacote.

## Validação

- **R-MQ-1** destino canônico: máquina criada em `output/<hub>/maquina/` (nunca
  `marketing/maquinas`).
- **R-MQ-2** cardinalidade 1:1: segunda obra do mesmo hub → recusa sem
  sobrescrever.
- **R-MQ-3** snapshot: `maquina/campanhas/` espelha `output/<hub>/campanhas/` e
  tem `snapshot.json` com `atualizado_em` da campanha.
- **R-MQ-4** manifesto da coleção: campo `maquina` preenchido e `maquinas_legadas`
  listando pastas `marketing/` do hub.
- **R-MQ-5** empacotamento: `maquina/manifesto.json` dentro do pacote.

## Testes

- `tests/test_maquina_checkout.py` — atualizado: gerador grava no novo destino
  (monkeypatch de `tipos_obra.DIR_OUTPUT`).
- `tests/test_maquina_colecao.py` (novo, padrão conftest):
  destino no hub; recusa 1:1; snapshot de campanhas; `maquina` no manifesto da
  coleção; `maquinas_legadas`; máquina no pacote.

## Integrações

- `colecao.py` — `montar_manifesto` lê `output/<hub>/maquina/manifesto.json` +
  `campanhas/snapshot.json` (idempotente: sem máquina → `maquina: null`).
- `empacotar-colecao.py` — copia `maquina/` ignorando `node_modules`, `.next`,
  `*.db` (runtime); LEIA-ME ganha seção quando há máquina.
- `AGENTS.md` (fonte: `.github/copilot-instructions.md`) — nota curta + RTK
  scratchpad.
