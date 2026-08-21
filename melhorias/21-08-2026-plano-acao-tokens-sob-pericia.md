---
titulo: Plano de Ação — Implementações identificadas a partir de "Tokens Sob Perícia"
data: 21-08-2026
relatorio_origem: melhorias/21-08-2026-analise-aplicabilidade-tokens-sob-pericia.md
---

# Plano de Ação

Cada seção corresponde a uma oportunidade do relatório de origem. Ordem = prioridade
sugerida (impacto x esforço).

---

## E. Blindagem de segredos no pre-commit hook

**Objetivo:** bloquear commit automático (R10 do CLAUDE.md) se o diff staged contiver
padrão de segredo.

**Arquivos afetados:**
- `scripts/hooks/pre-commit` (fonte versionada)
- `scripts/setup-links.ps1` / `setup-links.sh` (já copiam o hook — nenhuma mudança
  necessária ali, só re-rodar após editar a fonte)

**Passos:**
1. Adicionar ao `scripts/hooks/pre-commit`, antes do `pytest -q`, um bloco que roda
   `git diff --cached` contra uma lista de padrões: `sk-[a-zA-Z0-9_-]{20,}`,
   `-----BEGIN [A-Z ]*PRIVATE KEY-----`, `AKIA[0-9A-Z]{16}`, e opcionalmente
   `ghp_[a-zA-Z0-9]{36}` (token GitHub) e `xox[baprs]-[0-9a-zA-Z-]+` (Slack).
2. Se encontrar, imprimir `[BLOQUEADO] possível segredo em <arquivo>` e `exit 1`
   antes mesmo de rodar a suíte de testes (falha rápida, sem gastar tempo do
   pytest).
3. Rodar `scripts/setup-links.ps1` (Windows) para recopiar o hook para
   `.git/hooks/pre-commit`.
4. Testar com um commit de prova contendo uma string no padrão de chave (prefixo
   `sk-` seguido de 20+ caracteres alfanuméricos) staged — confirmar que o commit é
   bloqueado; remover a string e confirmar que passa. **Implementado e validado
   em 21-08-2026**: o próprio texto desta linha, na primeira redação deste plano,
   continha um exemplo concreto da string de teste e foi bloqueado pelo hook ao
   comitar este arquivo — a string de exemplo foi reescrita acima (descrita, não
   literal) exatamente por isso. Confirma que o gate funciona mesmo contra
   documentação que apenas *descreve* um padrão de segredo.
5. Documentar a extensão em `CLAUDE.md` §6 (Portabilidade Multi-IDE), na frase que já
   descreve o hook de pre-commit.

**Critério de aceite:** commit com padrão de segredo staged é bloqueado; commit limpo
passa normalmente; suíte de testes continua rodando após o gate de segredo.

**Risco:** falso positivo (ex.: hash SHA-256 de 40+ chars parecido com chave) — mitigar
com padrões suficientemente específicos (prefixo `sk-`, `AKIA`, cabeçalho PEM) em vez
de regex genérica de "string longa aleatória".

**Estimativa:** 30-45 min.

---

## D. Separar RTK scratchpad do CLAUDE.md

**Objetivo:** manter o corpo normativo de `CLAUDE.md` estável (prefixo de cache) e
isolar o conteúdo que cresce a cada sessão.

**Arquivos afetados:**
- `CLAUDE.md` (remover corpo da seção "## 7. RTK SCRATCHPAD" e da segunda seção
  duplicada "## RTK SCRATCHPAD" mais abaixo — atualmente há DUAS seções com esse
  nome no arquivo, uma delas provavelmente resultado de merge/edição duplicada,
  vale unificar de qualquer forma)
- Novo arquivo `RTK-SCRATCHPAD.md` (raiz do projeto)
- Junctions/hardlinks (`.cursor/rules/fabrica-agentica.mdc`, `.windsurfrules`,
  `.clinerules`, `.github/copilot-instructions.md`) — não precisam mudar, pois são
  hardlink do `CLAUDE.md` que passa a ser menor; o `RTK-SCRATCHPAD.md` é novo e não
  precisa de link cruzado a menos que se decida depois.

**Passos:**
1. Confirmar com `grep -n "RTK SCRATCHPAD" CLAUDE.md` que existem duas seções (§7 e
   uma seção solta "## RTK SCRATCHPAD" mais adiante) — decidir se unificar em uma só
   ao migrar.
2. Criar `RTK-SCRATCHPAD.md` com todo o conteúdo das entradas datadas
   (`- **2026-08-XX ...**`) hoje embutido no `CLAUDE.md`.
2b. **Ferramenta recomendada para esta migração:** `Skill(caveman-compress)` ou
    edição manual assistida — não é uma tarefa de reescrita de conteúdo, é corte e
    colagem preservando literalmente cada entrada.
3. No `CLAUDE.md`, substituir a seção RTK SCRATCHPAD inteira por uma única linha de
   referência: `## RTK SCRATCHPAD` seguida de `> Aprendizados de sessões anteriores:
   ver RTK-SCRATCHPAD.md (arquivo externo, não lido automaticamente pelo agente —
   consultar sob demanda).`
4. Atualizar a skill `rtk-memory` (que hoje presumivelmente grava direto no
   `CLAUDE.md`) para gravar novas entradas em `RTK-SCRATCHPAD.md` em vez do
   `CLAUDE.md` — checar `.claude/skills/rtk-memory/SKILL.md` antes de editar, para
   ajustar o caminho de escrita nela.
5. Rodar `scripts/setup-links.ps1` para garantir que os hardlinks de `CLAUDE.md`
   continuem consistentes (o arquivo mudou de tamanho, os hardlinks apontam para o
   mesmo inode, então isso é automático — só confirmar com
   `Get-Item CLAUDE.md,.cursor/rules/fabrica-agentica.mdc | Select Length`).
6. Medir o tamanho antes/depois (`wc -c CLAUDE.md`) e registrar a redução no
   relatório de sessão desta implementação.

**Critério de aceite:** `CLAUDE.md` cai para bem abaixo de 51KB (corpo normativo
apenas); `RTK-SCRATCHPAD.md` contém 100% das entradas antigas sem perda; hardlinks
continuam funcionando (`.cursor/rules/fabrica-agentica.mdc` reflete o novo
`CLAUDE.md` menor).

**Risco:** se alguma automação (hook, skill) ler `CLAUDE.md` esperando encontrar as
entradas RTK inline (ex.: para grep de aprendizados passados), ela vai parar de
encontrar — buscar por `grep -rn "RTK SCRATCHPAD\|RTK-SCRATCHPAD" .claude scripts`
antes de migrar, para achar dependências.

**Estimativa:** 1-2h (a maior parte é conferência de que nada mais depende do
conteúdo inline).

---

## C. Resiliência de rede em `fontes_academicas.py` e `validar-referencias.py`

**Objetivo:** paralelizar com teto de concorrência + aplicar backoff com jitter nas
chamadas HTTP, sem exigir nenhuma biblioteca nova (só `concurrent.futures`/`time`/
`random`, já na stdlib).

**Arquivos afetados:**
- `scripts/fontes_academicas.py` (função `_http_get`, linha ~165)
- `scripts/minerar-fontes-academicas.py` (função `minerar`, loop `for fonte in
  fontes`, linha ~40)
- `scripts/validar-referencias.py` (bloco de checagem de URL/DOI, linha ~107-115)
- `tests/test_fontes_academicas.py`, `tests/test_validar_referencias.py` (ou
  equivalentes) — adicionar teste do backoff/retry com mock de falha transitória

**Passos:**
1. Em `_http_get` (`fontes_academicas.py`), envolver o `urlopen` existente com um
   retry simples: 2-3 tentativas, espera `0.5 * (2 ** tentativa) + random.uniform(0,
   0.3)` segundos entre elas, só para erros que indicam instabilidade transitória
   (`HTTPError` com status 429/502/503, `URLError` de timeout) — nunca para 404/erro
   definitivo.
2. Em `minerar-fontes-academicas.py`, trocar o loop sequencial `for fonte in fontes`
   por `concurrent.futures.ThreadPoolExecutor(max_workers=3)` (teto pequeno — são
   APIs públicas com rate limit próprio, 3 é suficiente para ganhar tempo sem
   estourar limite de nenhuma delas) mantendo a agregação de resultados na mesma
   ordem que hoje (usar `executor.map` ou coletar futures e ordenar por índice
   original, para não quebrar a reprodutibilidade dos testes existentes).
3. Em `validar-referencias.py`, aplicar o mesmo padrão de retry com backoff à
   checagem de cada URL/DOI (linha ~107-115); avaliar paralelizar também
   (`ThreadPoolExecutor`) se o número de referências por obra for grande (>20) —
   medir tempo antes/depois com uma obra real via `time python scripts/
  validar-referencias.py <slug>`.
4. Preservar o modo `--sem-rede` existente intocado (retry/paralelismo só entram em
   caminho de rede real).
5. Rodar a suíte completa (`python -m pytest -q`) — por R16 do CLAUDE.md, só commitar
   com 100% verde.

**Critério de aceite:** suíte 100% verde; uma falha simulada (mock de 429 na
primeira tentativa, sucesso na segunda) é absorvida sem quebrar o resultado final;
tempo de execução da mineração/validação em uma obra de referência (múltiplas
fontes/URLs) reduz de forma mensurável.

**Risco:** paralelismo pode disparar rate limit se `max_workers` for alto demais —
manter conservador (2-3) e documentar no próprio código por quê.

**Estimativa:** 2-3h incluindo testes.

---

## A. Gate de verificação de comandos/CLI citados em capítulos técnicos

**Objetivo:** novo gate de conteúdo, no padrão dos existentes (`validar-fontes.py`,
`validar-referencias.py`), que sinaliza comandos/flags/caminhos de configuração
citados num capítulo como CONFIRMADO / PARCIALMENTE_CORRETO / FABRICADO / NÃO_VERIFICÁVEL, reaproveitando a classe A/B/C do dossiê.

**Arquivos afetados (novos):**
- `scripts/validar-comandos-cli.py`
- `tests/test_validar_comandos_cli.py`

**Arquivos afetados (integração):**
- `scripts/tipos_obra.py` — adicionar ao campo `gates_conteudo` do tipo `livro`
  (só quando a obra tiver uma flag de config indicando tema técnico/tooling — ver
  passo 2)
- `scripts/auditar-obra.py` — encadear o novo gate no `--estrito`
- `docs/referencia-*` ou `CLAUDE.md` §1 (tabela de gates) — documentar

**Passos:**
1. Definir o formato de marcação no capítulo: um comando citado com âncora
   verificável usa a mesma convenção de classe do dossiê — ex. bloco de código
   seguido de uma linha `<!-- cli-check: fonte=B; confere=true -->` (comentário
   Markdown, não aparece no PDF), preenchida pelo redator/revisor durante a escrita,
   análogo a como o dossiê já marca `(A)`/`(B)`/`(C)` ao fim da linha.
2. Adicionar em `scripts/tipos_obra.py` um campo opcional no `config_obra.json`
   (`categoria_tecnica: true`) que ativa este gate só para livros sobre
   ferramentas/CLIs/frameworks (não faz sentido rodar em livros de outros nichos) —
   operador escolhe isso na entrevista `/esbocar`, mesmo padrão de `gerar_campanha`/
   `gerar_maquina` (R17).
3. Implementar `validar-comandos-cli.py`:
   - reaproveitar `dividir_secoes`/`secao_por_nome` de `secoes_eita.py` (já usado por
     `validar-escala.py`/`validar-metricas.py`) para localizar blocos de código por
     capítulo;
   - extrair marcações `cli-check` inline;
   - contar: total de comandos marcados, quantos sem marcação nenhuma (viram
     `nao_verificado`, não reprovam — mesmo espírito de R-FT-2), quantos marcados
     `confere=false` (reprovam sempre — indica que o revisor já sabe que está errado
     e não corrigiu);
   - gate mínimo sugerido: nenhum comando com `confere=false` sobrevive ao
     `--estrito`; comandos sem marcação geram aviso no relatório mas não bloqueiam
     (replicando a política gradual de R-FT-2/R-FT-3).
4. Gerar relatório em `output/<slug>/validacao/relatorio_comandos_cli.json`, mesmo
   padrão de `relatorio_fontes.json`.
5. Encadear em `scripts/auditar-obra.py --estrito`, só quando
   `categoria_tecnica: true`.
6. Escrever `tests/test_validar_comandos_cli.py` cobrindo: capítulo com comando
   confirmado (passa), capítulo com comando `confere=false` (reprova em `--estrito`),
   capítulo sem nenhuma marcação (não reprova, mas relatório sinaliza).
7. Atualizar a skill `revisor-tecnico` (`.claude/skills/revisor-tecnico/SKILL.md` ou
   agent equivalente) para incluir, no processo de revisão de livros técnicos, a
   checagem manual de comandos citados contra `--help`/doc oficial antes de marcar
   `cli-check` como `confere=true` — isto é, o próprio protocolo do Capítulo 1/7 do
   livro vira instrução operacional do revisor-tecnico.
8. Rodar suíte completa; só commitar com 100% verde (R16).

**Critério de aceite:** gate roda em obra de teste com pelo menos 1 comando
confirmado e 1 fabricado (marcado manualmente `confere=false`); `--estrito` reprova
a obra com o comando fabricado e aprova a versão corrigida; suíte 100% verde.

**Risco:** exigir marcação manual de todo comando pode ser trabalho extra para o
redator/revisor em capítulos com muito código — mitigar tornando o gate
não-bloqueante por padrão (só bloqueia o que foi explicitamente marcado como
incorreto), e o operador decide ativar `categoria_tecnica` apenas para livros do
gênero DevOps/IA/frameworks.

**Estimativa:** 4-6h (maior peça do plano — novo gate completo com testes e
integração em 3 pontos de dispatch).

---

## B. token-guard — circuit breaker de gasto (condicional)

**Objetivo:** medir gasto real de uma sessão via ferramenta independente do
auto-relato já existente (`.agents/session-cost.jsonl`), como camada de
cross-check, não substituição.

**Pré-requisito obrigatório (fazer ANTES de qualquer código):** confirmar, no
ambiente real de uso (Windows + Claude Code local desta máquina), se:
1. `npx ccusage@latest --version` roda sem erro (precisa de Node/npx instalado);
2. o Claude Code local de fato grava histórico JSONL num caminho que o `ccusage`
   reconheça (`~/.claude/projects/**` ou equivalente no Windows).

Se qualquer um dos dois falhar, **este item fica em NÃO_VERIFICÁVEL** — não
implementar nada além de registrar a tentativa e o resultado no relatório de sessão,
por analogia direta com a regra do próprio livro ("NÃO_VERIFICÁVEL não é sinônimo de
aprovado" nem de "implementar mesmo assim").

**Arquivos afetados (se pré-requisito confirmado):**
- Novo `scripts/token-guard.ps1` (ambiente é Windows — adaptar o `.sh` do livro para
  PowerShell, ou Python puro para portabilidade)
- `.claude/skills/calcular-gastos-sessao/SKILL.md` — adicionar seção "Cross-check
  com ccusage" documentando quando/como rodar a comparação

**Passos (só após pré-requisito confirmado):**
1. Escrever função `custo-do-dia` chamando `npx ccusage@latest daily --json --since
   <hoje> --until <hoje>` e somando `totalCost`.
2. Comparar contra o total acumulado em `.agents/session-cost.jsonl` do dia — se a
   divergência for grande (>20%), sinalizar no relatório de sessão que o auto-relato
   pode estar desatualizado (não travar nada automaticamente; é uma ferramenta de
   auditoria, não um circuit breaker rígido, dado que a fábrica não expõe um botão
   de "trocar para fallback local" — R6 usa `model: inherit`, não há para onde
   fazer fallback).
3. Adicionar essa comparação como passo opcional na skill `gerar-relatorio-sessao`
   (que já fecha toda sessão com relatório) — não como gate bloqueante.

**Critério de aceite:** comparação roda e produz um número (ou justificativa clara
de por que não rodou); nenhuma automação passa a depender de `ccusage` como
requisito obrigatório (mantém-se opcional/best-effort, dado o item ser condicional).

**Risco:** se tratado como obrigatório e o ambiente não suportar, quebra o fluxo de
fechamento de sessão — por isso o desenho aqui é estritamente aditivo/best-effort,
nunca um gate que impede commit/push.

**Estimativa:** 30 min para o teste do pré-requisito; 1-2h para a implementação
completa, somente se o pré-requisito passar.
