# Design — CAMPANHA e MÁQUINA opcionais + versionamento (R17)

> Regra intocável registrada em `CLAUDE.md` §1 como **R17**. Este documento
> desenha a implementação técnica dessa regra.

## Problema

Hoje `/produzir-obra-completa` trata FLUXO 2 (CAMPANHA) e FLUXO 3 (MÁQUINA)
como **OBRIGATÓRIOS**. Não existe:

1. Uma pergunta na entrevista inicial (`/esbocar`) para o operador optar por
   não gerar CAMPANHA e/ou MÁQUINA.
2. Um fluxo para adicionar CAMPANHA/MÁQUINA depois, a uma coleção já existente,
   sem risco de sobrescrever silenciosamente o que já existe.
3. Uma forma de manter a CAMPANHA/MÁQUINA anterior quando o operador quer
   gerar de novo (hoje é sobrescrita ou recusa, nunca "as duas coexistem").

## Regra (R17, CLAUDE.md §1)

1. CAMPANHA e MÁQUINA são **opcionais**, decididas na entrevista (`/esbocar`),
   persistidas em `config_obra.json` (`gerar_campanha`, `gerar_maquina`).
   `/produzir-obra-completa` pula o fluxo quando `false` — isso não é falha.
2. Independente da entrevista, o operador pode disparar `/campanha`,
   `/campanha-completa` ou `/criar-maquina` a qualquer momento para uma
   coleção já existente.
3. Se já existir CAMPANHA/MÁQUINA para a coleção, o sistema **sempre** oferece
   a escolha: **Criar Nova** (versiona a existente) ou **Sobrescrever
   Existente**. Nunca decidir isso silenciosamente.

## Escopo desta implementação

### 1. `config_obra.json` — 2 campos novos

Em `scripts/parametros_obra.py`, `DERIVADOS_V5` ganha:

```python
"gerar_campanha": False,
"gerar_maquina": False,
```

Já é aplicado retroativamente pelo loop `setdefault` existente em
`carregar_config` (obras antigas sem os campos herdam `False` — comportamento
correto: nada muda para obras já em andamento, R17 é opt-in). Nenhuma faixa de
validação extra em `validar_config` — são flags booleanas simples, mesmo
padrão de `gerar_deck`/`gerar_emails`.

### 2. `/esbocar` — nova pergunta na Rodada 1

Duas perguntas novas (`AskUserQuestion`, sempre perguntadas, default Não):

| Header | Pergunta | Opções |
|---|---|---|
| Campanha | Deseja incluir a etapa de CAMPANHA de divulgação no fluxo desta coleção? | Sim \| Não (Recommended) |
| Máquina | Deseja incluir a etapa de MÁQUINA DE VENDAS no fluxo desta coleção? | Sim \| Não (Recommended) |

Gravadas em `config_obra.json` como `gerar_campanha`/`gerar_maquina`. Passo 4
(relatório) do `/esbocar` passa a listar os comandos `/campanha-completa` e
`/criar-maquina` como "disponíveis a qualquer momento", não como parte
obrigatória do funil.

### 3. `/produzir-obra-completa` — fluxos condicionais

- Diagrama do topo: rótulos "OBRIGATÓRIO" nos Fluxos 2 e 3 trocam para
  "OPCIONAL (config_obra.gerar_campanha / gerar_maquina)".
- Passo 3 (Fluxo 2): antes de rodar `criar-campanha.py --completo`, ler
  `gerar_campanha` de `config_obra.json`. Se `false`: pular o fluxo inteiro,
  registrar no relatório consolidado como `⏭️ PULADO — operador optou por não
  incluir CAMPANHA na entrevista (/campanha-completa <slug> para adicionar
  depois)` — nunca como falha/warning.
- Passo 4 (Fluxo 3): mesmo padrão com `gerar_maquina` e `/criar-maquina`.
- Se ambos os fluxos forem pulados, o relatório final marca Status Geral como
  ✅ CONCLUÍDO normalmente (materiais é o único fluxo que continua obrigatório).

### 4. Detecção de existente + escolha Nova/Sobrescrever

A escolha via `AskUserQuestion` só pode ocorrer na camada do orquestrador
(comando), nunca dentro dos scripts determinísticos. Protocolo único,
referenciado pelos 3 comandos (evita repetir prosa):

**Detecção** (comando faz a checagem de arquivo, sem custo de LLM):
- CAMPANHA por material: `output/<colecao>/campanhas/<material-slug>/` já tem
  conteúdo.
- CAMPANHA da coleção (`--completo`): `output/<colecao>/campanhas/campanha.json`
  existe.
- MÁQUINA: `output/<colecao>/maquina/manifesto.json` existe.

**Se existir**, pergunte (uma só vez, por operação):

| Header | Pergunta | Opções |
|---|---|---|
| Ação | Já existe {CAMPANHA\|MÁQUINA} para a coleção '<colecao>'. O que deseja fazer? | Criar Nova (Recommended) — mantém a existente arquivada em `versoes/` e a nova passa a ser a atual \| Sobrescrever Existente — substitui no lugar; a versão anterior é perdida |

- **Criar Nova** → script roda com a flag `--versionar`.
- **Sobrescrever Existente** → script roda com `--regenerar` (campanha, já
  existe) ou `--forcar` (máquina, novo — pula o `input()` interativo que hoje
  bloqueia execução não-interativa).

Se **não existir** nada ainda, roda normal, sem perguntar (a pergunta só
existe quando há algo a preservar ou perder).

### 5. Versionamento em disco

Pasta sibling nova, **sem prefixo `_`** (regra de empacotamento existente):
`output/<colecao>/versoes/`.

- Coleção completa: `versoes/campanhas-v{N}/` (move de `campanhas/` inteiro,
  incl. `campanha.json`).
- Material único: `versoes/campanhas-<material-slug>-v{N}/` (move de
  `campanhas/<material-slug>/`).
- Máquina: `versoes/maquina-v{N}/` (move de `maquina/` inteiro).

`N` = 1 + maior versão já arquivada daquele tipo/material (scan de
`versoes/<prefixo>-v*`, começa em 1 se não houver nenhuma). Depois do move, a
criação roda normalmente no caminho canônico (agora vazio) — nenhum outro
script (`colecao.py`, `empacotar-colecao.py`, `validar-campanha.py`, etc.)
precisa saber sobre versionamento: eles continuam lendo só o caminho canônico
`campanhas/`/`maquina/`.

### 6. Scripts

- `scripts/criar-campanha.py`: nova flag `--versionar` (arquiva antes de
  gerar; funciona tanto com `--material` quanto `--completo`). `--regenerar`
  já cobre "Sobrescrever" — sem mudança nesse caminho.
- `scripts/criar-maquina-vendas.py`: duas flags novas — `--versionar` (arquiva
  o `maquina/` existente para `versoes/maquina-v{N}/` em vez de
  `shutil.rmtree`) e `--forcar` (pula o `input("Sobrescrever? (s/N)")`, vai
  direto para o overwrite). A checagem "Regra 1:1 — outra obra" permanece
  intacta (protege contra colisão entre obras diferentes da mesma coleção;
  ortogonal a versionar/sobrescrever da MESMA obra).
- `scripts/colecao.py`: `_RAIZES_ESTRUTURAIS` ganha `"versoes"` (não é
  membro/hub). Manifesto passa a listar `versoes_arquivadas` (campo
  **derivado**, escaneado do disco em `--sincronizar` — nunca escrito à mão
  pelos scripts de criação, mesmo princípio de "manifesto é sempre derivado"
  já usado para `maquinas_legadas`).
- `scripts/empacotar-colecao.py`: exclui `versoes/` do pacote final; nota no
  `LEIA-ME.md` gerado ("versões anteriores de campanha/máquina ficam fora do
  pacote — consulte `output/<colecao>/versoes/` se precisar delas").

### 7. Docs

Atualizar `.claude/commands/esbocar.md`, `produzir-obra-completa.md`,
`campanha.md`, `campanha-completa.md`, `criar-maquina.md` para refletir as
seções 2-4 acima.

### 8. Testes (R16 — suíte 100% antes de commit)

- `tests/test_campanha.py`: versionar material único (2 chamadas seguidas →
  `versoes/campanhas-<mat>-v1/` depois `v2/`, canônico sempre fresco);
  versionar `--completo`; `--regenerar` continua sobrescrevendo em lugar.
- `tests/test_maquina_colecao.py`: `--versionar` arquiva `maquina/` existente
  para `versoes/maquina-v1/`; `--forcar` sobrescreve sem `input()`; a recusa
  "Regra 1:1 outra obra" continua funcionando.
- Teste de `colecao.py --sincronizar`: `versoes/` nunca aparece como membro;
  manifesto lista `versoes_arquivadas` corretamente.
- `parametros_obra.py`: `carregar_config` de obra V3 (sem os campos) devolve
  `gerar_campanha=False`/`gerar_maquina=False`; obra com os campos explícitos
  preserva o valor gravado.

## Fora de escopo (YAGNI)

- Restaurar (`--restaurar`) uma versão arquivada para canônico — não pedido;
  o operador pode mover manualmente se precisar. Se vier a ser pedido, é um
  design incremental separado.
- Limite de quantas versões ficam arquivadas — sem limite por ora (custo
  determinístico ~0, disco é do operador).
