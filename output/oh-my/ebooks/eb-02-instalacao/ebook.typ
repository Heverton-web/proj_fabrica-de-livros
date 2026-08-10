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
  title: "Instalação e Primeiros Passos & O TUI: Sua Interface de Comando",
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
      align(center, "Instalação e Primeiros Passos & O TUI: Sua Interface de Comando")
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
      #text(font: ("Inter", "Liberation Sans", "Arial"), size: 34pt, weight: "bold", fill: white)[Instalação e Primeiros Passos & O TUI: Sua Interface de Comando]
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
    #text(font: ("Inter", "Liberation Sans", "Arial"), size: 22pt, weight: "bold", fill: cor.primaria)[Instalação e Primeiros Passos & O TUI: Sua Interface de Comando]
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
= Instalação e Primeiros Passos
<instalação-e-primeiros-passos>
== O estaleiro está pronto --- só falta ligar o motor
<o-estaleiro-está-pronto-só-falta-ligar-o-motor>
No capítulo anterior, você mergulhou na arquitetura do OMP --- as 80.000 linhas de Rust, o pi-shell, os pi-natives, o pi-ast e os demais componentes que formam o esqueleto do harness.

Agora é hora de deixar a teoria de lado e colocar as mãos no casco. Como Mestre de Estaleiro Digital, você precisa primeiro instalar os equipamentos antes de zarpar.

== Por que quatro métodos de instalação?
<por-que-quatro-métodos-de-instalação>
O OMP é distribuído como binário compilado em Rust, o que significa que não depende de runtime como Node.js ou Python para funcionar. Cada método de instalação é apenas uma via diferente de entregar o mesmo binário no seu sistema.

#strong[curl] --- o método universal para Linux e macOS. Baixa o binário direto do GitHub Releases e coloca no seu PATH.

#strong[Homebrew] --- para quem já gerencia pacotes no macOS (ou Linux via Homebrew). Uma única linha, atualizações automáticas.

#strong[Bun] --- o gerenciador de pacotes do Bun permite instalar o OMP como complemento do ecossistema JavaScript.

#strong[PowerShell] --- o caminho nativo do Windows, sem necessidade de WSL. O OMP é nativo em Windows desde o início.

A escolha depende do seu ambiente. Se você já usa Homebrew, é a opção mais natural. Se está no Windows, o PowerShell evita a complexidade do WSL. Se quer o controle total, o curl entrega o binário sem intermediários.

== O que acontece depois de instalar?
<o-que-acontece-depois-de-instalar>
Com o binário no sistema, o próximo passo é o `omp setup` --- um assistente interativo que pergunta qual provider de LLM você quer usar, solicita a API key e grava os arquivos de configuração em `~/.omp/agent/`.

Esses dois arquivos --- `config.yml` e `models.yml` --- são o mapa de navegação do seu OMP: neles ficam definidos quais modelos estão disponíveis, quais ferramentas estão habilitadas e como o agente deve se comportar.

== A primeira sessão
<a-primeira-sessão>
Ao digitar `omp` no terminal, o TUI do OMP inicia e entra em modo idle --- aguardando seu comando. Quando você envia um prompt, o agente interpreta a intenção, seleciona as ferramentas necessárias e começa a trabalhar.

Cada ação é visível no terminal: o agente lê arquivos, executa comandos, busca padrões --- tudo de forma transparente.

== Instalação no Linux e macOS via curl
<instalação-no-linux-e-macos-via-curl>
O método mais direto. Funciona em qualquer distribuição Linux e no macOS.

```bash
# Linux e macOS
curl -fsSL https://omp.sh/install.sh | bash

# Verificar instalação
omp --version
```

Se o comando `omp` não for encontrado após a instalação, adicione o diretório de instalação ao PATH.

```bash
# Adicionar ao PATH (adicione ao ~/.bashrc ou ~/.zshrc)
export PATH="$HOME/.local/bin:$PATH"
```

== Instalação no macOS via Homebrew
<instalação-no-macos-via-homebrew>
Para quem já gerencia pacotes com Homebrew, esta é a via mais elegante. O Homebrew cuida de atualizações automaticamente.

```bash
# macOS com Homebrew
brew tap can1357/tap
brew install oh-my-pi

# Verificar
omp --version
```

== Instalação via Bun
<instalação-via-bun>
Se você já tem o Bun instalado (versão \>= 1.3.14), pode instalar o OMP diretamente.

```bash
# Via Bun (requer Bun >= 1.3.14)
bun install -g oh-my-pi

# Verificar
omp --version
```

== Instalação no Windows via PowerShell
<instalação-no-windows-via-powershell>
O OMP é nativo em Windows --- não precisa de WSL. O PowerShell baixa e instala o binário automaticamente.

```powershell
# Windows (PowerShell)
powershell -c "iwr -useb omp.sh/install.ps1 | iex"

# Verificar
omp --version
```

== Configuração inicial com omp setup
<configuração-inicial-com-omp-setup>
Com o binário instalado, o assistente de configuração guia cada etapa.

```bash
# Iniciar o assistente de configuração
omp setup
```

O assistente pergunta:

#strong[Qual provider usar?] --- Anthropic (Claude), OpenAI (GPT), Google (Gemini), ou qualquer um dos 60+ providers suportados.

#strong[Qual a API key?] --- Chave de acesso do provider selecionado.

#strong[Qual modelo padrão?] --- Claude Sonnet 4, GPT-4o, Gemini 2.5 Pro, etc.

Após responder, o OMP grava dois arquivos de configuração.

```yaml
# ~/.omp/agent/config.yml (gerado pelo setup)
tools:
  enabled:
    - read
    - write
    - edit
    - bash
    - grep
    - glob

memory:
  backend: local
  scope: project
```

```yaml
# ~/.omp/agent/models.yml (gerado pelo setup)
providers:
  anthropic:
    apiKey: "<sua-api-key>"

modelRoles:
  default: anthropic/claude-sonnet-4-20250514
  smol: anthropic/claude-haiku-3-5-20241022
```

== Verificando a saúde do sistema
<verificando-a-saúde-do-sistema>
Antes de começar a trabalhar, verifique se tudo está funcionando.

```bash
# Diagnóstico completo
omp --doctor

# Listar providers configurados
omp --providers

# Listar modelos disponíveis
omp --models
```

== Primeira sessão interativa
<primeira-sessão-interativa>
Agora sim --- o estaleiro está pronto. Inicie sua primeira sessão.

```bash
# Iniciar sessão interativa
omp
```

O TUI aparece com a barra de status, o card do modelo ativo e o prompt aguardando seu comando. Experimente.

```
> Leia o arquivo README.md deste projeto e resuma o que ele faz
```

O agente vai usar a ferramenta `read` para carregar o README.md, analisar o conteúdo e resumir em linguagem clara.

Outros comandos úteis na primeira sessão.

```
/model                # Trocar o modelo ativo
/fresh                # Resetar o estado do provider
/vibe                 # Ativar modo Vibe (workers persistentes)
```

Para encerrar a sessão, pressione `Ctrl+C` ou digite `/exit`.

== O erro mais comum na instalação
<o-erro-mais-comum-na-instalação>
Você instalou o OMP, configurou o Anthropic como provider e inaugurou sua primeira sessão. Tudo parece funcionar --- até que o agente tenta ler um arquivo e retorna um erro de permissão.

Quando o OMP foi instalado via curl, o binário ficou no diretório `~/.local/bin/`, mas os arquivos de configuração foram gravados em `~/.omp/agent/`. Se o seu projeto está em um diretório com permissões restritivas, o agente pode falhar ao acessar arquivos.

A correção é simples --- conceda permissão de leitura ao diretório do projeto.

```bash
# Conceder permissão ao diretório do projeto
chmod -R o+rX /caminho/para/seu/projeto
```

Outra armadilha comum: instalar o OMP mas esquecer de configurar a API key. O `omp setup` pode ser reexecutado a qualquer momento.

```bash
# Reconfigurar o provider
omp setup
```

A seção de configuração aceita múltiplos providers simultaneamente --- você pode ter Anthropic para tarefas pesadas e OpenAI para tarefas leves, trocando com `/model` durante a sessão.

== Próximos Passos
<próximos-passos>
Você completou três etapas fundamentais: instalou o OMP em qualquer plataforma, configurou o primeiro provider com `omp setup` e conduziu sua primeira sessão interativa.

O OMP nasce pronto para operar --- mas a verdadeira potência emerge quando você domina a interface de comando. No próximo capítulo, você mergulhará no TUI: os cards, os atalhos de teclado, os modos de operação e tudo o que separa um usuário casual de um Mestre de Estaleiro que navega com precisão.

Acesse a documentação completa: https:/\/omp.sh/docs

Siga-nous nas redes sociais para dicas, tutoriais e novidades sobre o Oh My Pi.

#horizontalrule

= O TUI: Sua Interface de Comando
<o-tui-sua-interface-de-comando>
== A ponte de comando do navio
<a-ponte-de-comando-do-navio>
No capítulo anterior, você completou a instalação do OMP e rodou sua primeira sessão. Agora é hora de dominar a interface que será seu centro de comando permanente --- o TUI (Terminal User Interface).

Assim como um mestre de estaleiro precisa conhecer cada alavanca, cada mostrador e cada instrumento do painel de controle do navio antes de zarpar, você precisa entender a fundo os componentes visuais, os atalhos e os modos de operação do OMP.

Essa familiaridade é o que separa quem apenas usa o agente de quem realmente o comanda.

== Componentes visuais do TUI
<componentes-visuais-do-tui>
O TUI do OMP é a camada visual que traduz o que o agente de IA está pensando e fazendo em uma linguagem que o desenvolvedor pode acompanhar, auditar e controlar.

Diferente de interfaces de chat genéricas onde o texto flui sem estrutura, o OMP organiza cada ação em componentes visuais discretos --- #strong[cards] --- que se acumulam formando um histórico navegable da sessão.

=== Cards
<cards>
No topo e ao longo do scroll, os cards representam cada interação: prompts do usuário, respostas do modelo, chamadas de ferramentas com seus resultados, edições propostas com preview, e erros. Cada card tem um ícone que identifica seu tipo --- um lápis para edições, um terminal para bash, um olho para leituras.

Isso permite que você escaneie visualmente a história da sessão sem ler cada linha.

=== Footer
<footer>
Na parte inferior, o footer exibe informações em tempo real sobre a sessão: o modelo ativo, o papel (role) que ele está desempenhando, o custo acumulado da sessão e a contagem de tokens.

É ali que você vê, por exemplo, se o agente está usando o modelo `default` ou se ele mudou para `smol` durante um fan-out de subagentes.

=== Status Bar
<status-bar>
A status bar --- a linha mais abaixo da tela --- mostra o estado do agente: se está processando uma requisição, se está aguardando input, ou se há uma operação em background rodando.

Quando o agente trava ou leva tempo para responder, essa barra é seu primeiro indicador de diagnóstico.

== Os cards em detalhe
<os-cards-em-detalhe>
Cada card de ferramenta segue um padrão consistente.

Quando o agente lê um arquivo, aparece um card com o caminho do arquivo e um resumo do conteúdo --- não o conteúdo bruto, que poderia inundar a tela.

Quando ele faz uma edição, o card mostra um diff: o que vai sair (em vermelho) e o que vai entrar (em verde), com o número de linhas afetadas.

Para ferramentas de busca como `grep` e `ast_grep`, os resultados aparecem com numeração de linha e trechos destacados.

O mais importante: edições nunca são aplicadas silenciosamente. O agente propõe a mudança, o TUI exibe o preview, e só então a edição é gravada. Essa separação entre proposta e execução é um dos diferenciais de segurança do OMP --- você sempre vê o que vai acontecer antes de acontecer.

== O sistema de ask
<o-sistema-de-ask>
Quando o agente encontra uma ambiguidade --- por exemplo, múltiplos arquivos que correspondem a um padrão, ou uma decisão que depende de preferência sua --- ele invoca a ferramenta `ask`.

Essa ferramenta renderiza um #strong[option picker] na tela: uma lista de escolhas com navegação por setas, uma opção marcada como "\(Recommended)" quando aplicável, e um footer que explica os atalhos: "up/down navigate · enter select · esc cancel".

Esse mecanismo é o que torna o modo interativo do OMP genuinamente interativo. Em vez de o agente adivinhar sua intenção e seguir em frente, ele para, mostra as opções, e espera sua decisão.

É a diferença entre um passageiro e um piloto.

== Atalhos de teclado essenciais
<atalhos-de-teclado-essenciais>
O TUI do OMP responde a uma série de atalhos que aceleram a navegação e o controle da sessão.

#figure(
  align(center)[#table(
    columns: 2,
    align: (auto,auto,),
    table.header([Atalho], [Função],),
    table.hline(),
    [`Ctrl+P`], [Cicla entre os modelos configurados para o papel ativo],
    [`Alt+A`], [Abre o Agent Hub para monitorar subagentes],
    [`Ctrl+C`], [Cancela a geração atual do modelo],
    [`Ctrl+L`], [Limpa a tela mantendo o histórico],
    [`Tab`], [Aceita a opção sugerida no option picker],
    [`Esc`], [Cancela o picker ou fecha um card expandido],
  )]
  , kind: table
  )

O `Ctrl+P` é particularmente útil quando você quer testar rapidamente como um mesmo prompt se comporta com modelos diferentes. Ao pressioná-lo, o footer atualiza imediatamente mostrando o novo modelo selecionado.

== Comandos slash
<comandos-slash>
Além dos atalhos de teclado, o OMP expõe comandos slash que modificam o comportamento da sessão. Eles são digitados diretamente no prompt.

#strong[`/model`] --- Abre o seletor de modelo para trocar o modelo ativo no meio da sessão. Você pode escolher entre dezenas de providers configurados.

#strong[`/vibe`] --- Entra no modo Vibe, onde o agente atua como um diretor que comanda workers persistentes com ferramentas de leitura apenas. Útil para sessões onde você quer que o agente planeje antes de executar.

#strong[`/fresh`] --- Reseta o estado do stream do provider (cache de prompt obsoleto, stream travado) sem alterar o transcript local. Quando o agente parece travado ou responde com lixo, `/fresh` é o primeiro remédio.

#strong[`/collab`] --- Inicia uma sessão de colaboração ao vivo, gerando um link e um QR code para que um colega se junte. Pode ser read-write (par programming) ou read-only (observação).

#strong[`/review`] --- Dispara subagentes de code review que varrem branches, commits ou trabalho não commitado em paralelo, classificando issues de P0 a P3.

#strong[`/advisor`] --- Configura e gerencia o modelo advisor --- um segundo modelo que observa cada turno do agente principal e injeta notas, concerns ou blockers.

#strong[`/debug`] --- Abre ferramentas de depuração, relatórios e profiling.

== Magic keywords
<magic-keywords>
Três palavras mágicas, escritas em lowercase no meio do prompt, ativam comportamentos especializados do agente. Elas funcionam apenas em prosa --- não dentro de blocos de código, identificadores ou caminhos de arquivo.

#strong[`ultrathink`] --- Solicita raciocínio cuidadoso multi-etapa e o maior esforço de thinking automático suportado pelo modelo. Use quando a tarefa exige análise profunda.

#strong[`orchestrate`] --- Executa trabalho independente substancial através de subagentes paralelos e verifica cada fase. Ative quando a tarefa pode ser decomposta em partes independentes.

#strong[`workflowz`] --- Constrói um workflow determinístico multi-subagentes com a ferramenta `task`. Para automações complexas que exigem controle preciso do fluxo.

```bash
# Exemplo: usando uma magic keyword no prompt
omp -p "ultrathink analise a arquitetura deste projeto e sugira melhorias"

# Exemplo: modo one-shot com orchestrate
omp -p "orchestrate refatore o módulo de autenticação e execute todos os testes"
```

== Os 4 modos de operação
<os-4-modos-de-operação>
O motor do OMP é o mesmo, mas ele pode ser acessado de quatro maneiras diferentes, cada uma otimizada para um caso de uso distinto.

=== Modo 1: Interactive (TUI padrão)
<modo-1-interactive-tui-padrão>
Quando você digita `omp` sem argumentos, o TUI abre. É o modo mais completo: cards renderizados, edits com preview, o option picker do `ask`, footer com custos, e navegação por atalhos. É aqui que você passa a maior parte do tempo.

```bash
# Iniciar sessão interativa
omp

# Resumir sessão anterior
omp --resume
```

=== Modo 2: One-shot (`omp -p`)
<modo-2-one-shot-omp--p>
Para quando você quer uma resposta rápida sem abrir a interface completa. O `-p` recebe um prompt, o agente processa, imprime a resposta e encerra. Ideal para scripts, CI/CD, ou perguntas pontuais.

```bash
# Pergunta rápida e saída
omp -p "liste todos os arquivos .ts na pasta src/"

# Com modelo específico
omp -p --model anthropic/claude-sonnet-4.5 "explique este erro"
```

=== Modo 3: RPC (`omp --mode rpc`)
<modo-3-rpc-omp---mode-rpc>
Para quando você quer controlar o OMP de outro programa. O motor recebe comandos NDJSON via stdio e responde com frames de evento. Não há TUI --- o controle é total via código.

```bash
# Iniciar em modo RPC sem sessão persistente
omp --mode rpc --no-session

# Enviar um prompt via NDJSON
> {"id":"r1","type":"prompt","message":"liste arquivos .ts"}
< {"id":"r1","type":"response", ...}
```

=== Modo 4: ACP (`omp acp`)
<modo-4-acp-omp-acp>
O Agent Client Protocol é o protocolo de integração com editores. Quando o OMP roda em modo ACP, ele se comunica com o editor via JSON-RPC, e as ferramentas são roteadas pelo editor.

```bash
# Iniciar em modo ACP (geralmente acionado pelo editor)
omp acp
```

== Os 10 roles de modelo
<os-10-roles-de-modelo>
O OMP roteia trabalho por intenção através de 10 papéis (roles) de modelo. Cada role pode apontar para um provider e modelo diferente, permitindo otimização por custo e qualidade.

#figure(
  align(center)[#table(
    columns: 2,
    align: (auto,auto,),
    table.header([Role], [Uso],),
    table.hline(),
    [`default`], [Turnos normais],
    [`smol`], [Fan-out barato de subagentes],
    [`slow`], [Raciocínio profundo],
    [`plan`], [Modo planejamento],
    [`commit`], [Geração de changelogs],
    [`vision`], [Análise de imagens],
    [`designer`], [Geração de arte],
    [`task`], [Coordenação de tarefas],
    [`advisor`], [Revisão inline],
    [`tiny`], [Tarefas triviais],
  )]
  , kind: table
  )

== O picker que captura o teclado
<o-picker-que-captura-o-teclado>
Imagine que você acabou de instalar o OMP e está ansioso para testá-lo. Você abre o terminal, digita `omp`, e a tela se preenche com cards coloridos, um footer com informações que não reconhece, e um prompt piscando.

Sua primeira reação é digitar algo e ver o que acontece. O agente responde, faz algumas buscas, e então para: "Encontrei 3 arquivos que correspondem ao padrão. Qual deles você quer que eu analise?" Aparece um picker com três opções.

Aqui é onde o erro mais comum acontece: você ignora o picker, tenta digitar algo no prompt, e nada acontece. O picker captura o foco do teclado --- você precisa usar as setas para navegar e Enter para selecionar, ou Esc para cancelar.

É um detalhe pequeno, mas que confunde 9 em cada 10 iniciantes.

O diagnóstico é direto: o TUI do OMP funciona em modalidades. Quando o option picker está ativo, ele captura todos os inputs de teclado. A solução é simples --- olhe para o footer do picker, ele sempre mostra os atalhos disponíveis.

No caso do `ask`, são "up/down navigate · enter select · esc cancel". Ao dominar essa interação, você percebe que o TUI não está te bloqueando: está te protegendo de decisões precipitadas.

== Erros comuns e suas correções
<erros-comuns-e-suas-correções>
#figure(
  align(center)[#table(
    columns: (33.33%, 36.36%, 30.3%),
    align: (auto,auto,auto,),
    table.header([Erro comum], [Diagnóstico], [Correção],),
    table.hline(),
    [Picker captura teclado e o usuário não consegue digitar], [Modalidade ativa], [Use setas + Enter, ou Esc para cancelar],
    [`omp -p` não mostra opções nem pede confirmação], [Modo one-shot é non-interactive], [Use `omp` (TUI) para tarefas interativas],
    [Agente travado, sem resposta], [Stream do provider obsoleto], [Digite `/fresh` para resetar o stream],
    [Footer mostra modelo errado], [Role diferente do esperado], [Use `Ctrl+P` para ciclar ou `/model` para trocar],
  )]
  , kind: table
  )

== Próximos Passos
<próximos-passos-1>
Três pontos devem ficar gravados neste capítulo.

Primeiro, o TUI do OMP é uma superfície de controle projetada para transparência: cada ação do agente aparece como um card, cada edição tem preview, e ambiguidades são resolvidas via option picker --- nunca por adivinhação.

Segundo, os atalhos e comandos slash não são decoração: `Ctrl+P`, `Alt+A`, `/fresh` e `/collab` são ferramentas de produtividade que transformam a experiência de usar o agente.

Terceiro, os quatro modos de operação --- interactive, one-shot, RPC e ACP --- garantem que o OMP se adapte a qualquer cenário, do script de CI ao pair programming ao vivo.

O desafio que fica: abra o OMP agora, inicie uma sessão interativa, e experimente cada um dos comandos slash pelo menos uma vez. Troque de modelo com `/model`, inicie um `/collab view`, e veja como o Agent Hub (`Alt+A`) mostra os subagentes trabalhando.

Essa familiaridade prática é o que transforma um instrumento desconhecido em uma extensão da sua mão de obra.

No próximo capítulo, você mergulhará no arsenal completo de ferramentas built-in do OMP --- as 31 ferramentas que compõem o equipamento do estaleiro.

Acesse a documentação completa: https:/\/omp.sh/docs

Siga-nous nas redes sociais para dicas, tutoriais e novidades sobre o Oh My Pi. Junte-se a mais de 23.3k desenvolvedores que já estão usando o harness mais completo do mercado.

#horizontalrule

// ── CONTRACAPA ────────────────────────────────────────────────────
#pagebreak()
