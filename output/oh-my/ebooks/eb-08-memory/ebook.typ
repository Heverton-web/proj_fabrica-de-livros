// Template ABNT para Livros - Fabrica Agentica de Livros
// Compativel com Pandoc + Typst (testado em typst 0.15 / pandoc 3.10)
//
// Variaveis Pandoc suportadas (-V chave=valor):
//   title, subtitle, author            -> capa, folha de rosto e cabecalho
//   cor_acento                         -> hex (#rrggbb) da cor de accent da obra/serie,
//                                          mesma da capa grafica (scripts/series_capa.py)
//   cip_sobrenome, cip_nome            -> ficha catalografica (autoria invertida)
//   cip_cutter, cip_ano, cip_paginas   -> ficha catalografica
//   cip_palavras, cip_cdd, cip_isbn    -> ficha catalografica
//   cip_local, cip_editora             -> imprenta da folha de rosto e da CIP
//   sinopse                            -> texto da contracapa
//   capa_imagem                        -> PNG full-bleed como pagina-capa (padrao da serie)
//   sem_capa_grafica                   -> "1" desativa capa/contracapa graficas

#set document(
  title: "Memory System: Memória que o Agente Curata & Hiper-Personalização: OMP ao Seu Jeito",
  author: "Heverton Eduardo Peres",
  date: datetime.today(),
)

// ── Cor cromatica da obra (derivada da mesma cor de accent da capa —
// REGRA 5 / scripts/series_capa.py — nunca mais uma paleta fixa isolada) ──
#let cor-acento-str = ""
#let cor-acento = if cor-acento-str == "" { rgb("#58a6ff") } else { rgb(cor-acento-str) }
#let cor = (
  primaria: cor-acento.darken(55%),
  secundaria: cor-acento.darken(20%),
  destaque: cor-acento,
  clara: cor-acento.lighten(88%),
)

// ── Pagina, tipografia e paragrafos (ABNT) ────────────────────────
#set page(
  paper: "a4",
  margin: (top: 3cm, bottom: 2cm, left: 3cm, right: 2cm),
  header: context {
    if counter(page).get().first() > 1 {
      set text(size: 9pt, fill: gray)
      align(center, "Memory System: Memória que o Agente Curata & Hiper-Personalização: OMP ao Seu Jeito")
    }
  },
  footer: context {
    set text(size: 9pt)
    align(center, [#counter(page).display("1") de #counter(page).final().first()])
  },
)

#set text(
  font: ("Times New Roman", "Liberation Serif"),
  size: 12pt,
  lang: "pt",
  region: "BR",
)

#set par(
  justify: true,
  leading: 0.75em,
  first-line-indent: 1.25cm,
)

// Definicao do horizontal rule (Pandoc gera #horizontalrule como texto)
#let horizontalrule = {
  v(1em)
  line(length: 100%, stroke: 1pt + cor.destaque)
  v(1em)
}

// Estilo de blocos de codigo (com borda na cor da paleta da capa)
#show raw.where(block: true): block.with(
  width: 100%,
  fill: cor.clara,
  stroke: 0.5pt + cor.secundaria,
  inset: 8pt,
  radius: 4pt,
)

// Estilo de codigo inline
#show raw.where(block: false): box.with(
  fill: cor.clara,
  inset: (x: 3pt, y: 0pt),
  outset: (y: 3pt),
  radius: 2pt,
)

// Estilo de citacoes (blockquote) com borda lateral na cor da paleta da capa
#show quote: it => block(
  width: 100%,
  fill: cor.clara,
  inset: (left: 12pt, right: 8pt, top: 8pt, bottom: 8pt),
  stroke: (left: 3pt + cor.destaque),
  radius: (right: 4pt),
  it,
)

// Figuras (diagramas Mermaid renderizados) — nunca extrapolam a mancha grafica
#set image(width: 88%, fit: "contain")
#show figure: it => {
  set par(first-line-indent: 0cm)
  v(0.6cm)
  align(center, it)
  v(0.6cm)
}
#show figure.caption: it => {
  set text(font: ("Inter", "Liberation Sans", "Arial"), size: 10pt, fill: cor.secundaria, weight: "bold")
  it
}

// Regra geral de titulos: sempre fonte INTER e cores da paleta da capa
#show heading: set text(font: ("Inter", "Liberation Sans", "Arial"))

// Estilo de titulos - nivel 1 (com suporte a Parte)
#show heading.where(level: 1): it => {
  set par(first-line-indent: 0cm)
  let isParte = type(it.body) == str and it.body.starts-with("Parte")
  pagebreak()
  if isParte {
    set text(font: ("Inter", "Liberation Sans", "Arial"), size: 20pt, weight: "bold", fill: cor.primaria)
    v(3cm)
    it
    v(0.3cm)
    line(length: 40%, stroke: 2.5pt + cor.destaque)
    v(2cm)
  } else {
    set text(font: ("Inter", "Liberation Sans", "Arial"), size: 16pt, weight: "bold", fill: cor.primaria)
    v(2cm)
    it
    v(0.2cm)
    line(length: 30%, stroke: 2pt + cor.destaque)
    v(1cm)
  }
}

// Estilo de titulos - nivel 2
#show heading.where(level: 2): it => {
  set text(font: ("Inter", "Liberation Sans", "Arial"), size: 14pt, weight: "bold", fill: cor.secundaria)
  set par(first-line-indent: 0cm)
  v(1cm)
  it
  v(0.2cm)
  line(length: 15%, stroke: 1.5pt + cor.destaque)
  v(0.4cm)
}

// Estilo de titulos - nivel 3
#show heading.where(level: 3): it => {
  set text(font: ("Inter", "Liberation Sans", "Arial"), size: 12pt, weight: "bold", fill: cor.secundaria)
  set par(first-line-indent: 0cm)
  v(0.75cm)
  it
  v(0.4cm)
}

// Estilo de titulos - nivel 4 em diante
#show heading.where(level: 4): it => {
  set text(font: ("Inter", "Liberation Sans", "Arial"), size: 11pt, weight: "bold", fill: cor.secundaria)
  set par(first-line-indent: 0cm)
  v(0.6cm)
  it
  v(0.3cm)
}

#let capa-grafica-ativa = "1" != "1"

// ── CAPA GRAFICA (Upgrade 5) ──────────────────────────────────────
#if capa-grafica-ativa {
    page(fill: cor.primaria, margin: 0cm, header: none, footer: none, numbering: none)[
    #set par(first-line-indent: 0cm, justify: false, leading: 0.55em)
    #place(top + right, dx: -2.2cm, rect(width: 0.35cm, height: 100%, fill: cor.secundaria))
    #place(top + left, rect(width: 100%, height: 1.2cm, fill: cor.destaque))
    #place(bottom + left, rect(width: 100%, height: 4.5cm, fill: cor.secundaria))
    #place(bottom + left, dy: -4.5cm, rect(width: 100%, height: 0.15cm, fill: cor.destaque))

    #place(top + left, dx: 2.5cm, dy: 6.5cm, block(width: 14.5cm)[
      #text(font: ("Inter", "Liberation Sans", "Arial"), size: 34pt, weight: "bold", fill: white)[Memory System: Memória que o Agente Curata & Hiper-Personalização: OMP ao Seu Jeito]
          ])

    #place(bottom + left, dx: 2.5cm, dy: -1.6cm, block(width: 15cm)[
      #text(font: ("Inter", "Liberation Sans", "Arial"), size: 15pt, weight: "bold", fill: white)[Heverton Eduardo Peres]
      #v(0.2cm)
      #text(size: 10pt, fill: cor.clara)[#datetime.today().display("[year]")]
    ])
  ]
  }

// ── FOLHA DE ROSTO (ABNT NBR 6029) ────────────────────────────────
#page(header: none, footer: none, numbering: none)[
  #set par(first-line-indent: 0cm, justify: false)
  #align(center)[
    #text(font: ("Inter", "Liberation Sans", "Arial"), size: 13pt, weight: "bold", fill: cor.secundaria)[Heverton Eduardo Peres]
    #v(3.5cm)
    #text(font: ("Inter", "Liberation Sans", "Arial"), size: 22pt, weight: "bold", fill: cor.primaria)[Memory System: Memória que o Agente Curata & Hiper-Personalização: OMP ao Seu Jeito]
      ]
  #v(4cm)
  #align(right, block(width: 8.5cm)[
    #set text(size: 10.5pt)
    #set par(justify: true, first-line-indent: 0cm)
    Obra técnica de literatura especializada, produzida e diagramada conforme as
    normas ABNT para publicação editorial.
  ])
  #v(1fr)
  #align(center)[
    #set text(size: 11pt)
    Brasil
    #linebreak()
    #datetime.today().display("[year]")
  ]
]

// ── VERSO DA FOLHA DE ROSTO: FICHA CATALOGRAFICA (CIP) ────────────

// ── SUMARIO ───────────────────────────────────────────────────────
#outline(title: [Sumário], indent: 1.5cm, depth: 3)

// ── CONTEUDO PRINCIPAL ────────────────────────────────────────────
= Memory System: Memória que o Agente Curata
<memory-system-memória-que-o-agente-curata>
== O diário de bordo inteligente
<o-diário-de-bordo-inteligente>
No capítulo anterior, você dominou as stream rules --- aquelas regras que interceptam o modelo no meio da geração e o colocam de volta nos trilhos. Agora, imagine que cada viagem que você faz pelo código deixa registros no casco do navio: onde ancorou, quais rotas funcionaram, quais equipamentos falharam.

Sem esses registros, a próxima viagem começa do zero. É exatamente isso que o sistema de memória do Oh My Pi resolve: ele permite que o agente recorde decisões técnicas, erros já corrigidos e lições aprendidas entre sessões.

== As Cinco Ferramentas de Memória
<as-cinco-ferramentas-de-memória>
O Oh My Pi dispõe de cinco ferramentas que trabalham juntas para criar um ciclo completo de conhecimento.

#strong[retain] --- Armazena fatos duradouros no banco de memória ativo. É como registrar no diário de bordo que o porto de Santos tem uma rota específica para descarga de containers.

#strong[recall] --- Busca memórias brutas no banco. Equivale a consultar o arquivo náutico para ver quais rotas já foram testadas com sucesso.

#strong[reflect] --- Sintetiza uma resposta sobre memórias recuperadas. É o capitão que revisa todos os registros anteriores e extrai uma conclusão sobre a melhor rota.

#strong[memory\_edit] --- Atualiza, esquece ou invalida memórias armazenadas por ID. Útil quando uma informação se torna desatualizada --- como quando uma rota é fechada por obras.

#strong[learn] --- Captura uma lição reutilizável e opcionalmente a promove para uma skill gerenciada. É como criar um manual permanente para a tripulação baseado em experiências reais.

== Os Três Backends de Armazenamento
<os-três-backends-de-armazenamento>
O Oh My Pi permite escolher entre três backends, cada um com características específicas.

#strong[local] --- Armazena resumos e lições gerados a partir de sessões persistidas no projeto. É o diário de bordo que fica guardado no próprio navio.

#strong[hindsight] --- Backend remoto com escopo por banco. Funciona como um arquivo náutico centralizado na base naval, acessível por diferentes navios.

#strong[mnemopi] --- Backend local baseado em SQLite. Oferece recall polifônico (vetorial, grafos, fatos, temporal) e é o mais completo para uso individual.

== Escopo por Projeto
<escopo-por-projeto>
Cada backend suporta diferentes modos de escopo.

#strong[global] --- Um banco compartilhado para todos os projetos. É como um arquivo náutico central que todos os navios da frota consultam.

#strong[per-project] --- Memória isolada por projeto. Cada navio tem seu próprio diário de bordo privado.

#strong[per-project-tagged] --- Escrita local com visibilidade global. O navio registra em seu diário, mas pode consultar o arquivo central da frota.

== Pipeline de Compressão de Sessões
<pipeline-de-compressão-de-sessões>
O sistema local implementa um pipeline de duas fases para consolidar o conhecimento.

#strong[Fase 1 --- Extração por sessão:] Para cada sessão passada, um modelo lê o histórico e extrai sinal duradouro: decisões técnicas, restrições, falhas resolvidas e fluxos de trabalho recorrentes.

#strong[Fase 2 --- Consolidação:] Um segundo modelo lê todas as extrações e produz três saídas: `MEMORY.md` (documento de memória de longo prazo curado), `memory_summary.md` (texto compacto injetado no início da sessão), e `skills/` (playbooks procedimentais reutilizáveis).

== A Metáfora do Estaleiro
<a-metáfora-do-estaleiro>
Imagine que você é o mestre de um estaleiro digital. Cada navio que sai para o mar coleta dados sobre as condições do oceano, portos visitados e equipamentos utilizados. Quando o navio retorna ao estaleiro, os dados são processados.

retain é como anotar no diário de bordo: "O porto de Santos exige autorização prévia para containers de 40 pés". recall é consultar o arquivo de rotas anteriores quando o navio precisa ir a Santos novamente. reflect é o capitão revisando todos os registros e decidindo: "Baseado nas últimas 5 viagens, a melhor rota para Santos passa por Angra dos Reis". memory\_edit é atualizar o diário quando uma rota é fechada. learn é criar um manual permanente: "Procedimento padrão para descarga em portos com maré alta".

== Configuração Básica do Backend Local
<configuração-básica-do-backend-local>
Para ativar o backend de memória local, adicione ao seu `config.yml`.

```yaml
memory:
  backend: local

autolearn:
  enabled: true
```

Com essa configuração, o Oh My Pi ativará o pipeline de memória que gera resumos e lições entre sessões. O backend local é ideal para quem está começando, pois não requer configuração de servidores externos.

== Configuração do Backend Mnemopi
<configuração-do-backend-mnemopi>
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

== Uso das Ferramentas de Memória
<uso-das-ferramentas-de-memória>
Durante uma sessão, o agente pode usar as ferramentas de memória.

#strong[Retain --- Armazenar um fato importante:]

```python
retain(
    content="O projeto usa Node.js v20 LTS com npm como gerenciador de pacotes",
    tags=["configuracao", "nodejs", "projeto"]
)
```

#strong[Recall --- Buscar memórias relevantes:]

```python
recall(
    query="configuração do projeto e dependências",
    limit=5
)
```

#strong[Reflect --- Sintetizar informações:]

```python
reflect(
    query="quais são as melhores práticas de configuração para este projeto?"
)
```

#strong[Memory\_edit --- Atualizar memória desatualizada:]

```python
memory_edit(
    id="mem_123",
    action="update",
    content="O projeto migrou de npm para pnpm v9"
)
```

#strong[Learn --- Capturar uma lição reutilizável:]

```python
learn(
    content="Sempre usar pnpm em projetos com workspaces para evitar conflitos de dependências",
    context="Descoberto após problemas com npm em monorepo com 15 pacotes"
)
```

== Parâmetros Importantes de Configuração
<parâmetros-importantes-de-configuração>
#figure(
  align(center)[#table(
    columns: (36.67%, 26.67%, 36.67%),
    align: (auto,auto,auto,),
    table.header([Parâmetro], [Padrão], [Descrição],),
    table.hline(),
    [`memories.maxRolloutAgeDays`], [30], [Sessões mais antigas não são processadas],
    [`memories.minRolloutIdleHours`], [12], [Sessões ativas recentemente são ignoradas],
    [`memories.maxRolloutsPerStartup`], [64], [Limite de sessões processadas por inicialização],
    [`memories.summaryInjectionTokenLimit`], [5000], [Limite de tokens para injeção de resumo],
  )]
  , kind: table
  )

Para o Mnemopi, parâmetros adicionais.

#figure(
  align(center)[#table(
    columns: (36.67%, 26.67%, 36.67%),
    align: (auto,auto,auto,),
    table.header([Parâmetro], [Padrão], [Descrição],),
    table.hline(),
    [`mnemopi.polyphonicRecall`], [false], [Ativa recall em 4 vozes],
    [`mnemopi.retainEveryNTurns`], [4], [Número mínimo de turns entre retentions automáticas],
    [`mnemopi.recallLimit`], [8], [Máximo de memórias recuperadas no prompt],
  )]
  , kind: table
  )

== Gerenciamento de Memória via Slash Commands
<gerenciamento-de-memória-via-slash-commands>
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

== Cena de contraste: o navio sem memória vs.~com memória
<cena-de-contraste-o-navio-sem-memória-vs.-com-memória>
Você está trabalhando em um projeto de API REST com FastAPI. Na segunda-feira, descobriu que o banco de dados precisa de uma configuração específica de connection pooling para suportar 100 requisições simultâneas. Você documentou isso em um arquivo `NOTAS.md`.

Na terça-feira, uma nova sessão começa. O agente de IA não tem contexto sobre a descoberta de segunda-feira. Ele sugere uma configuração padrão que causa timeout em produção. Você perde 30 minutos debugando o problema.

Agora, imagine que o sistema de memória estava ativo. Na segunda-feira, quando você descobriu a configuração correta, o agente usou `retain` para armazenar: "FastAPI com SQLAlchemy precisa de pool\_size=20 e max\_overflow=10 para 100 requisições simultâneas". Na terça-feira, na primeira interação, o agente usou `recall` e encontrou essa memória. Ele aplicou automaticamente a configuração correta, evitando o problema.

== Armadilhas comuns
<armadilhas-comuns>
#strong[Backend não configurado.] Muitos iniciantes esquecem de ativar o backend. Sem `memory.backend: local`, as ferramentas de memória não ficam disponíveis.

#strong[Limite de tokens excedido.] O resumo injetado no início da sessão tem limite de 5000 tokens. Se a memória acumulada for grande demais, informações importantes podem ser truncadas.

#strong[Memória desatualizada.] Se o código muda drasticamente entre sessões, a memória pode conter informações obsoletas. Use `memory_edit` para atualizar ou invalidar memórias antigas.

#strong[Escopo inadequado.] Usar `global` quando deveria ser `per-project` pode vazar informações sensíveis de um projeto para outro.

== Métricas de eficiência
<métricas-de-eficiência>
Com o sistema de memória ativo, você pode esperar redução de tempo de setup de \~5 minutos (re-explicar contexto) para \~0 segundos (injeção automática), consistência de configurações com 100% das configurações importantes preservadas entre sessões, e velocidade de onboarding com novos membros da equipe herdando o conhecimento acumulado automaticamente.

== Próximos Passos
<próximos-passos>
Neste capítulo, você explorou o sistema de memória do Oh My Pi --- a âncora que mantém o conhecimento do agente firme entre sessões. Cinco ferramentas complementares --- retain, recall, reflect, memory\_edit e learn criam um ciclo completo de captura, busca e síntese de conhecimento. Três backends flexíveis --- local para uso individual, Hindsight para equipes, e Mnemopi para funcionalidades avançadas. E um pipeline inteligente de compressão que extrai e consolida automaticamente o conhecimento mais relevante das sessões passadas.

Experimente ativar o backend local em um projeto real. Comece com `memory.backend: local` e `autolearn.enabled: true`. Após algumas sessões, use `/memory view` para ver o que o agente aprendeu.

No próximo capítulo, você descobrirá como o Oh My Pi integra editores de código diretamente no agente --- a ferramenta ACP que permite ao modelo ler e escrever no buffer que você está visualizando.

Acesse a documentação completa: https:/\/omp.sh/docs

Siga-nous nas redes sociais para dicas, tutoriais e novidades sobre o Oh My Pi.

#horizontalrule

= Hiper-Personalização: OMP ao Seu Jeito
<hiper-personalização-omp-ao-seu-jeito>
== Montando o painel de comando completo
<montando-o-painel-de-comando-completo>
No capítulo anterior, você configurou o sistema de memória do OMP --- aquela âncora que mantém o agente lembrando de fatos, lições e preferências entre sessões. Mas a memória é apenas uma peça do quebra-cabeça.

O verdadeiro poder do OMP aparece quando você personaliza cada aspecto do harness: escolhe qual modelo roda em cada papel, quais ferramentas ficam habilitadas, quais regras guiam o comportamento e como tudo isso se integra ao editor que você já usa todos os dias.

== Config.yml: o painel de instrumentos do navio
<config.yml-o-painel-de-instrumentos-do-navio>
Todo estaleiro funcional tem um painel central --- um lugar onde o mestre ajusta motor, leme, instrumentos e comunicações. No OMP, esse painel é o arquivo `~/.omp/agent/config.yml`. Nele, você define três coisas fundamentais: quais modelos rolam em cada papel (modelRoles), quais ferramentas estão habilitadas (tools) e como a memória persiste entre sessões (memory).

O config.yml é lido quando o OMP inicia. Qualquer alteração nele exige reiniciar a sessão para ter efeito. Pense nele como o manual de operações do seu navio --- ajustar o leme em alto-mar é possível, mas o ideal é calibrar tudo antes de zarpar.

== ModelRoles: 10 papéis, 10 motores
<modelroles-10-papéis-10-motores>
O OMP não trata todos os turnos da mesma forma. Ele diferencia 10 papéis distintos, cada um com suas necessidades de velocidade, raciocínio e custo.

#figure(
  align(center)[#table(
    columns: (22.22%, 18.52%, 59.26%),
    align: (auto,auto,auto,),
    table.header([Role], [Uso], [Característica],),
    table.hline(),
    [`default`], [Turnos normais], [Equilíbrio entre custo e qualidade],
    [`smol`], [Fan-out de subagentes], [Modelo leve e barato para tarefas paralelas],
    [`slow`], [Raciocínio profundo], [Modelo potente para problemas complexos],
    [`plan`], [Modo plano], [Focado em planejamento, não execução],
    [`commit`], [Changelogs], [Geração de mensagens de commit],
    [`vision`], [Análise de imagens], [Processamento visual],
    [`designer`], [Design de interfaces], [Geração de layouts],
    [`task`], [Orquestração], [Coordenação de tarefas],
    [`advisor`], [Revisão inline], [Segundo olho em cada turno],
    [`tiny`], [Tarefas leves], [Rápido e econômico para operações simples],
  )]
  , kind: table
  )

A mágica está em mapear cada papel ao modelo certo. Você pode usar um modelo potente e caro para `slow` (problemas difíceis) e um modelo leve e barato para `smol` (dezenas de subagentes trabalhando em paralelo). Isso reduz custos sem sacrificar qualidade onde ela importa.

== Tools: o arsenal sob seu controle
<tools-o-arsenal-sob-seu-controle>
O OMP vem com 31 ferramentas built-in, mas nem todas precisam estar ativas o tempo todo. O campo `tools` no config.yml permite habilitar ou desabilitar ferramentas específicas. Se você não trabalha com browser automation, pode desligar a ferramenta `browser` e reduzir o consumo de tokens por turno. Se seu projeto não usa debug nativo, desative `debug`.

== Memory: a memória que você cura
<memory-a-memória-que-você-cura>
No Capítulo 15, você viu como o sistema de memória funciona. Agora, no config.yml, você escolhe o backend (local, Hindsight ou Mnemopi) e o escopo (projeto ou global). Essa escolha afeta onde os dados persistem e com quem são compartilhados.

== Configurando o config.yml
<configurando-o-config.yml>
Vamos montar um config.yml completo.

```yaml
# ~/.omp/agent/config.yml

modelRoles:
  default: anthropic/claude-sonnet-4-20250514
  slow: anthropic/claude-opus-4-0
  smol: openai/gpt-4o-mini
  advisor: anthropic/claude-sonnet-4-20250514
  plan: anthropic/claude-sonnet-4-20250514

tools:
  enabled:
    - read
    - write
    - edit
    - bash
    - grep
    - glob
    - lsp
    - debug
    - task
    - browser
  disabled:
    - security_scan
    - generate_image

memory:
  backend: local
  scope: project
```

== Configurando o models.yml
<configurando-o-models.yml>
Agora o models.yml --- a oficina de motores. Aqui definimos providers customizados, incluindo modelos locais.

```yaml
# ~/.omp/agent/models.yml

providers:
  spark:
    baseUrl: http://192.168.10.223:8000/v1
    api: openai-completions
    apiKey: dummy
    models:
      - id: minimax-m3
        name: MiniMax M3
        contextWindow: 100000
        maxTokens: 32000

  anthropic:
    api: anthropic
    apiKey: <sua-chave-anthropic>
    models:
      - id: claude-sonnet-4-20250514
        name: Claude Sonnet 4
        contextWindow: 200000
        maxTokens: 8192
      - id: claude-opus-4-0
        name: Claude Opus 4
        contextWindow: 200000
        maxTokens: 32768

  openai:
    api: openai
    apiKey: <sua-chave-openai>
    models:
      - id: gpt-4o-mini
        name: GPT-4o Mini
        contextWindow: 128000
        maxTokens: 16384

modelRoles:
  default: spark/minimax-m3
  smol: openai/gpt-4o-mini
  slow: anthropic/claude-opus-4-0
  plan: anthropic/claude-sonnet-4-20250514
  advisor: anthropic/claude-sonnet-4-20250514
```

Observe que o `modelRoles` pode aparecer tanto no config.yml quanto no models.yml. Quando presente nos dois, o models.yml tem prioridade --- é ele que define o mapeamento final entre provider e papel.

== Magic Keywords: atalhos de poder
<magic-keywords-atalhos-de-poder>
O OMP reconhece três palavras mágicas que você pode incluir em qualquer mensagem para alterar o comportamento do agente. Essas keywords são processadas pelo harness antes de enviar ao modelo.

#figure(
  align(center)[#table(
    columns: (30%, 26.67%, 43.33%),
    align: (auto,auto,auto,),
    table.header([Keyword], [Efeito], [Quando usar],),
    table.hline(),
    [`ultrathink`], [Raciocínio multi-step cuidadoso], [Problemas complexos que exigem análise profunda],
    [`orchestrate`], [Fan-out paralelo com verificação], [Tarefas que se beneficiam de múltiplos workers],
    [`workflowz`], [Workflow determinístico multi-subagent], [Pipelines com etapas bem definidas],
  )]
  , kind: table
  )

#strong[Exemplo de uso:]

```
> ultrathink Analise a arquitetura deste módulo e proponha melhorias de performance
```

```
> orchestrate Refatore os 10 arquivos de teste em paralelo, garantindo que cada um passe no lint
```

```
> workflowz 1. Extraia dados do CSV 2. Valide schema 3. Gere relatório 4. Compile PDF
```

Cada keyword desencadeia um modo de operação diferente no harness. O `ultrathink` faz o agente pausar e pensar antes de agir. O `orchestrate` distribui trabalho entre subagentes. O `workflowz` cria uma pipeline determinística onde cada etapa alimenta a próxima.

== ACP: integração com editores
<acp-integração-com-editores>
O ACP (Agent Control Protocol) é o que permite rodar o OMP dentro de editores como Zed. Em vez de alternar entre terminal e editor, você mantém o agente integrado ao seu ambiente de trabalho.

```yaml
acp:
  enabled: true
  editor: zed
  save_path: /tmp/omp-acp-output
```

Quando o ACP está ativo, o OMP lê o buffer atual do editor, processa a instrução e escreve o resultado de volta. O fluxo é: você seleciona código no editor, envia um comando via ACP, o OMP lê o buffer, processa e gera a resposta, o resultado é escrito no save\_path, e o editor atualiza o buffer.

== A Falha na Esteira e a Correção Estrutural
<a-falha-na-esteira-e-a-correção-estrutural>
Você está trabalhando em um projeto grande com 15 módulos. Abre o terminal e inicia o OMP com a configuração padrão. O agente começa a trabalhar, mas algo está errado: ele está usando o modelo mais caro para tarefas simples de rename, e modelos baratos para problemas de arquitetura que exigem raciocínio profundo. O custo de tokens dispara e a qualidade cai nos pontos que mais importam.

O problema é que você não configurou as modelRoles. O OMP estava usando o mesmo modelo para tudo --- como um navio que navega em velocidade máxima mesmo em porto, gastando combustível à toa.

#strong[A correção:] você abre o models.yml e mapeia cada papel ao modelo certo.

```yaml
modelRoles:
  default: spark/minimax-m3      # Tarefas normais — barato e rápido
  slow: anthropic/claude-opus-4-0  # Problemas difíceis — potente
  smol: openai/gpt-4o-mini        # Subagentes — o mais econômico
```

Agora, quando o agente precisa de raciocínio profundo, ele sobe para o Opus. Quando distribui trabalho entre subagentes, usa o Mini. O custo cai significativamente sem sacrificar qualidade onde ela realmente importa.

== Armadilhas comuns
<armadilhas-comuns-1>
#strong[Esquecer de reiniciar a sessão após editar config.yml.] As alterações só têm efeito na próxima inicialização do OMP.

#strong[Mapear todos os papéis ao mesmo modelo.] Isso anula a vantagem de ter 10 roles distintos --- use modelos diferentes para papéis diferentes.

#strong[Habilitar ferramentas desnecessárias.] Cada ferramenta adiciona tokens ao system prompt. Se você não usa `browser`, desative-o.

#strong[Não usar magic keywords.] São gratuitas e podem transformar a qualidade do resultado em tarefas complexas. O `ultrathink` sozinho evita erros que o agente cometeria em modo padrão.

#strong[Configurar memory scope como `global` sem necessidade.] Dados globais vaziam o contexto em todos os projetos. Use `project` por padrão.

== Próximos Passos
<próximos-passos-1>
Neste capítulo, você montou o painel de comando completo do seu estaleiro digital. Os três pilares --- config.yml (instrumentos), models.yml (motores) e ACP + magic keywords (integração e atalhos) --- transformam o OMP de ferramenta genérica em uma extensão personalizada do seu fluxo de trabalho.

Escolheu qual modelo roda em cada papel, configurou quais ferramentas ficam habilitadas, definiu o backend de memória e integrou o agente ao seu editor. Essa é a diferença entre usar o OMP e comandá-lo --- e é exatamente o que separa um iniciante de um Mestre de Estaleiro Digital.

Acesse a documentação completa: https:/\/omp.sh/docs

Siga-nous nas redes sociais para dicas, tutoriais e novidades sobre o Oh My Pi. Junte-se a mais de 23.3k desenvolvedores que já estão usando o harness mais completo do mercado.

#horizontalrule

// ── CONTRACAPA ────────────────────────────────────────────────────
#pagebreak()
