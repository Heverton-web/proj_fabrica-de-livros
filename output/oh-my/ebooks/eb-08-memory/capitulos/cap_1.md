# Memory System: Memória que o Agente Curata

## O diário de bordo inteligente

No capítulo anterior, você dominou as stream rules — aquelas regras que interceptam o modelo no meio da geração e o colocam de volta nos trilhos. Agora, imagine que cada viagem que você faz pelo código deixa registros no casco do navio: onde ancorou, quais rotas funcionaram, quais equipamentos falharam.

Sem esses registros, a próxima viagem começa do zero. É exatamente isso que o sistema de memória do Oh My Pi resolve: ele permite que o agente recorde decisões técnicas, erros já corrigidos e lições aprendidas entre sessões.

## As Cinco Ferramentas de Memória

O Oh My Pi dispõe de cinco ferramentas que trabalham juntas para criar um ciclo completo de conhecimento.

**retain** — Armazena fatos duradouros no banco de memória ativo. É como registrar no diário de bordo que o porto de Santos tem uma rota específica para descarga de containers.

**recall** — Busca memórias brutas no banco. Equivale a consultar o arquivo náutico para ver quais rotas já foram testadas com sucesso.

**reflect** — Sintetiza uma resposta sobre memórias recuperadas. É o capitão que revisa todos os registros anteriores e extrai uma conclusão sobre a melhor rota.

**memory_edit** — Atualiza, esquece ou invalida memórias armazenadas por ID. Útil quando uma informação se torna desatualizada — como quando uma rota é fechada por obras.

**learn** — Captura uma lição reutilizável e opcionalmente a promove para uma skill gerenciada. É como criar um manual permanente para a tripulação baseado em experiências reais.

## Os Três Backends de Armazenamento

O Oh My Pi permite escolher entre três backends, cada um com características específicas.

**local** — Armazena resumos e lições gerados a partir de sessões persistidas no projeto. É o diário de bordo que fica guardado no próprio navio.

**hindsight** — Backend remoto com escopo por banco. Funciona como um arquivo náutico centralizado na base naval, acessível por diferentes navios.

**mnemopi** — Backend local baseado em SQLite. Oferece recall polifônico (vetorial, grafos, fatos, temporal) e é o mais completo para uso individual.

## Escopo por Projeto

Cada backend suporta diferentes modos de escopo.

**global** — Um banco compartilhado para todos os projetos. É como um arquivo náutico central que todos os navios da frota consultam.

**per-project** — Memória isolada por projeto. Cada navio tem seu próprio diário de bordo privado.

**per-project-tagged** — Escrita local com visibilidade global. O navio registra em seu diário, mas pode consultar o arquivo central da frota.

## Pipeline de Compressão de Sessões

O sistema local implementa um pipeline de duas fases para consolidar o conhecimento.

**Fase 1 — Extração por sessão:** Para cada sessão passada, um modelo lê o histórico e extrai sinal duradouro: decisões técnicas, restrições, falhas resolvidas e fluxos de trabalho recorrentes.

**Fase 2 — Consolidação:** Um segundo modelo lê todas as extrações e produz três saídas: `MEMORY.md` (documento de memória de longo prazo curado), `memory_summary.md` (texto compacto injetado no início da sessão), e `skills/` (playbooks procedimentais reutilizáveis).

## A Metáfora do Estaleiro

Imagine que você é o mestre de um estaleiro digital. Cada navio que sai para o mar coleta dados sobre as condições do oceano, portos visitados e equipamentos utilizados. Quando o navio retorna ao estaleiro, os dados são processados.

retain é como anotar no diário de bordo: "O porto de Santos exige autorização prévia para containers de 40 pés". recall é consultar o arquivo de rotas anteriores quando o navio precisa ir a Santos novamente. reflect é o capitão revisando todos os registros e decidindo: "Baseado nas últimas 5 viagens, a melhor rota para Santos passa por Angra dos Reis". memory_edit é atualizar o diário quando uma rota é fechada. learn é criar um manual permanente: "Procedimento padrão para descarga em portos com maré alta".

## Configuração Básica do Backend Local

Para ativar o backend de memória local, adicione ao seu `config.yml`.

```yaml
memory:
  backend: local

autolearn:
  enabled: true
```

Com essa configuração, o Oh My Pi ativará o pipeline de memória que gera resumos e lições entre sessões. O backend local é ideal para quem está começando, pois não requer configuração de servidores externos.

## Configuração do Backend Mnemopi

Para usar o Mnemopi, que oferece funcionalidades mais avançadas como recall polifônico.

```yaml
memory:
  backend: mnemopi

mnemopi:
  scoping: per-project-tagged
  autoRecall: true
  autoRetain: true
  polyphonicRecall: true
  retainEveryNTurns: 4
  recallLimit: 8
```

## Uso das Ferramentas de Memória

Durante uma sessão, o agente pode usar as ferramentas de memória.

**Retain — Armazenar um fato importante:**

```python
retain(
    content="O projeto usa Node.js v20 LTS com npm como gerenciador de pacotes",
    tags=["configuracao", "nodejs", "projeto"]
)
```

**Recall — Buscar memórias relevantes:**

```python
recall(
    query="configuração do projeto e dependências",
    limit=5
)
```

**Reflect — Sintetizar informações:**

```python
reflect(
    query="quais são as melhores práticas de configuração para este projeto?"
)
```

**Memory_edit — Atualizar memória desatualizada:**

```python
memory_edit(
    id="mem_123",
    action="update",
    content="O projeto migrou de npm para pnpm v9"
)
```

**Learn — Capturar uma lição reutilizável:**

```python
learn(
    content="Sempre usar pnpm em projetos com workspaces para evitar conflitos de dependências",
    context="Descoberto após problemas com npm em monorepo com 15 pacotes"
)
```

## Parâmetros Importantes de Configuração

| Parâmetro | Padrão | Descrição |
|-----------|--------|-----------|
| `memories.maxRolloutAgeDays` | 30 | Sessões mais antigas não são processadas |
| `memories.minRolloutIdleHours` | 12 | Sessões ativas recentemente são ignoradas |
| `memories.maxRolloutsPerStartup` | 64 | Limite de sessões processadas por inicialização |
| `memories.summaryInjectionTokenLimit` | 5000 | Limite de tokens para injeção de resumo |

Para o Mnemopi, parâmetros adicionais.

| Parâmetro | Padrão | Descrição |
|-----------|--------|-----------|
| `mnemopi.polyphonicRecall` | false | Ativa recall em 4 vozes |
| `mnemopi.retainEveryNTurns` | 4 | Número mínimo de turns entre retentions automáticas |
| `mnemopi.recallLimit` | 8 | Máximo de memórias recuperadas no prompt |

## Gerenciamento de Memória via Slash Commands

```bash
# Ver a injeção de memória atual
/memory view

# Ver estatísticas do backend
/memory stats

# Diagnosticar problemas
/memory diagnose

# Limpar dados de memória
/memory clear

# Forçar consolidação
/memory enqueue
```

## Cena de contraste: o navio sem memória vs. com memória

Você está trabalhando em um projeto de API REST com FastAPI. Na segunda-feira, descobriu que o banco de dados precisa de uma configuração específica de connection pooling para suportar 100 requisições simultâneas. Você documentou isso em um arquivo `NOTAS.md`.

Na terça-feira, uma nova sessão começa. O agente de IA não tem contexto sobre a descoberta de segunda-feira. Ele sugere uma configuração padrão que causa timeout em produção. Você perde 30 minutos debugando o problema.

Agora, imagine que o sistema de memória estava ativo. Na segunda-feira, quando você descobriu a configuração correta, o agente usou `retain` para armazenar: "FastAPI com SQLAlchemy precisa de pool_size=20 e max_overflow=10 para 100 requisições simultâneas". Na terça-feira, na primeira interação, o agente usou `recall` e encontrou essa memória. Ele aplicou automaticamente a configuração correta, evitando o problema.

## Armadilhas comuns

**Backend não configurado.** Muitos iniciantes esquecem de ativar o backend. Sem `memory.backend: local`, as ferramentas de memória não ficam disponíveis.

**Limite de tokens excedido.** O resumo injetado no início da sessão tem limite de 5000 tokens. Se a memória acumulada for grande demais, informações importantes podem ser truncadas.

**Memória desatualizada.** Se o código muda drasticamente entre sessões, a memória pode conter informações obsoletas. Use `memory_edit` para atualizar ou invalidar memórias antigas.

**Escopo inadequado.** Usar `global` quando deveria ser `per-project` pode vazar informações sensíveis de um projeto para outro.

## Métricas de eficiência

Com o sistema de memória ativo, você pode esperar redução de tempo de setup de ~5 minutos (re-explicar contexto) para ~0 segundos (injeção automática), consistência de configurações com 100% das configurações importantes preservadas entre sessões, e velocidade de onboarding com novos membros da equipe herdando o conhecimento acumulado automaticamente.

## Próximos Passos

Neste capítulo, você explorou o sistema de memória do Oh My Pi — a âncora que mantém o conhecimento do agente firme entre sessões. Cinco ferramentas complementares — retain, recall, reflect, memory_edit e learn criam um ciclo completo de captura, busca e síntese de conhecimento. Três backends flexíveis — local para uso individual, Hindsight para equipes, e Mnemopi para funcionalidades avançadas. E um pipeline inteligente de compressão que extrai e consolida automaticamente o conhecimento mais relevante das sessões passadas.

Experimente ativar o backend local em um projeto real. Comece com `memory.backend: local` e `autolearn.enabled: true`. Após algumas sessões, use `/memory view` para ver o que o agente aprendeu.

No próximo capítulo, você descobrirá como o Oh My Pi integra editores de código diretamente no agente — a ferramenta ACP que permite ao modelo ler e escrever no buffer que você está visualizando.

Acesse a documentação completa: https://omp.sh/docs

Siga-nous nas redes sociais para dicas, tutoriais e novidades sobre o Oh My Pi.
