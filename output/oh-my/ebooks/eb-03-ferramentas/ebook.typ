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
  title: "As 31 Ferramentas Built-in: O Arsenal Completo & Edições Hashline: Precisão com Menos Tokens",
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
      align(center, "As 31 Ferramentas Built-in: O Arsenal Completo & Edições Hashline: Precisão com Menos Tokens")
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
      #text(font: ("Inter", "Liberation Sans", "Arial"), size: 34pt, weight: "bold", fill: white)[As 31 Ferramentas Built-in: O Arsenal Completo & Edições Hashline: Precisão com Menos Tokens]
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
    #text(font: ("Inter", "Liberation Sans", "Arial"), size: 22pt, weight: "bold", fill: cor.primaria)[As 31 Ferramentas Built-in: O Arsenal Completo & Edições Hashline: Precisão com Menos Tokens]
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
= As 31 Ferramentas Built-in: O Arsenal Completo
<as-31-ferramentas-built-in-o-arsenal-completo>
== Abrindo o arsenal do estaleiro
<abrindo-o-arsenal-do-estaleiro>
No capítulo anterior, você dominou o TUI --- a interface de comando que traduz cada ação do agente em cards navegáveis. Agora é hora de abrir o arsenal completo: as 31 ferramentas built-in que o agente usa para ler, escrever, buscar, executar, depurar e até controlar seu computador.

Assim como um estaleiro de navios não se constrói com apenas um martelo e uma chave inglesa, um coding agent não se limita a ler e escrever arquivos.

O OMP equipa seu agente com um arsenal completo de equipamentos especializados --- cada um afiado para uma tarefa específica na construção de software.

== Três categorias de ferramentas
<três-categorias-de-ferramentas>
As 31 ferramentas do OMP são organizadas em três grandes categorias, cada uma com um conjunto de responsabilidades que se complementa. Essa organização não é apenas conceitual --- ela define como o agente acessa, usa e combina as ferramentas durante uma sessão.

== Ferramentas de Arquivo (7 ferramentas)
<ferramentas-de-arquivo-7-ferramentas>
O casco de qualquer projeto de software são seus arquivos. O OMP oferece sete ferramentas dedicadas a manipular esse casco com precisão cirúrgica.

#strong[read] --- A ferramenta de leitura mais completa do mercado. Não apenas lê arquivos inteiros: suporta offsets (linha inicial) e limits (quantidade de linhas), permitindo que o agente leia apenas a seção que precisa. Quando lê um diretório, retorna a lista de entradas. Para arquivos binários e PDFs, renderiza como anexo.

É a lupa do estaleiro --- quando você precisa inspecionar uma viga específica na quilha, não precisa levantar o navio inteiro.

#strong[write] --- Gravação direta de conteúdo. Sobrescreve arquivos existentes ou cria novos. O agente deve usar read antes de write em arquivos existentes --- isso garante que ele conhece o estado atual antes de modificá-lo.

É a fundição do estaleiro: quando uma peça precisa ser refeita do zero.

#strong[edit] --- Edições por substituição de string exata. O agente especifica old\_string (o texto atual) e new\_string (o texto desejado), e a ferramenta localiza e substitui. Se houver múltiplas ocorrências, o agente precisa fornecer mais contexto.

É a soldadora de precisão --- corta exatamente onde deve, sem afetar a estrutura ao redor.

#strong[ast\_edit] --- Edições por âncoras de hash em vez de conteúdo completo. Em vez de enviar todo o bloco de código como old\_string, o agente referencia um hash que identifica o bloco. Isso reduz drasticamente os tokens consumidos --- blocos de código estável não precisam ser reenviados a cada edição.

É a âncora do estaleiro: segura a peça no lugar sem precisar descrevê-la inteira a cada ajuste.

#strong[grep] --- Busca por conteúdo dentro de arquivos usando regex. Retorna caminhos, numeração de linha e trechos destacados. O agente pode filtrar por padrão de arquivo.

É o sonar do estaleiro --- varre o casco inteiro procurando uma solda específica.

#strong[glob] --- Busca por padrão de nome de arquivo. Encontra todos os arquivos que correspondem a uma expressão glob. Retorna caminhos ordenados por data de modificação.

É o inventário do estaleiro --- lista todas as peças disponíveis por tipo e tamanho.

#strong[ast\_grep] --- Busca semântica em AST (Abstract Syntax Tree). Diferente do grep que busca texto bruto, o ast\_grep entende a estrutura do código. Você pode buscar por padrões como "toda função que retorna Promise" ou "toda classe que herda de Error".

É o raio-X do estaleiro --- vê a estrutura interna do metal, não apenas a superfície.

== Ferramentas de Runtime (2 ferramentas)
<ferramentas-de-runtime-2-ferramentas>
Enquanto as ferramentas de arquivo operam sobre o casco estático do projeto, as ferramentas de runtime são o motor --- elas fazem o código realmente rodar.

#strong[bash] --- Execução de comandos shell. Suporta timeout configurável, captura completa de stdout/stderr, e modos interativos para comandos que precisam de input do usuário. É o motor principal do estaleiro --- quando você precisa rodar um build, executar testes ou instalar dependências.

#strong[eval] --- Avaliação inline de código Python ou JavaScript. Diferente do bash que executa comandos externos, o eval executa código diretamente no contexto do agente. Ideal para transformações de dados, cálculos rápidos ou prototipação de lógica antes de gravá-la em um arquivo.

== Ferramentas Avançadas (5+ ferramentas)
<ferramentas-avançadas-5-ferramentas>
Aqui está onde o OMP se diferencia de qualquer outro harness. Essas ferramentas transformam o agente de um assistente de código em um verdadeiro engenheiro autônomo.

#strong[LSP] --- Language Server Protocol integrado. Oferece 14 operações de inteligência de código: rename, diagnostics, code actions, completions, hover, e mais. Quando o agente renomeia uma função, ele não apenas faz busca-e-substitui --- ele atualiza todas as referências, imports e tipos que dependem dela.

É o radar do estaleiro --- detecta problemas antes que eles se tornem falhas estruturais.

#strong[debug] --- Debug Adapter Protocol (DAP). 28 operações de depuração: attach em processos, breakpoints condicionais, stepping (step over/into/out), inspection de variáveis, evaluation de expressões. O agente pode anexar a um processo Python, Go ou C++ e depurá-lo como faria um humano --- só que mais rápido.

#strong[task] --- Sistema de fan-out para subagentes. Permite que o agente decomponha tarefas complexas em workers paralelos, cada um com seu escopo e schema de resultado validado. É a tripulação do estaleiro --- quando o projeto é grande demais para um único engenheiro.

#strong[browser] --- Automação de browser headless via Puppeteer e CDP (Chrome DevTools Protocol). Navega em páginas, preenche formulários, extrai dados, tira screenshots. Modo stealth disponível via relay extension para evitar detecção.

É o mergulhador do estaleiro --- entra na água para inspecionar partes que o olho humano não alcança.

#strong[computer] --- Controle nativo do desktop. Gerencia janelas, captura screenshots do screen inteiro, lê a AX tree (árvore de acessibilidade) para entender a UI, e envia input nativo (teclado e mouse).

É o guindaste do estaleiro --- move, posiciona e opera peças que estão fora do escopo do casco.

== As 31 ferramentas em detalhe
<as-31-ferramentas-em-detalhe>
A tabela completa lista todas as ferramentas built-in do OMP, organizadas por categoria.

#figure(
  align(center)[#table(
    columns: (6.12%, 22.45%, 22.45%, 22.45%, 26.53%),
    align: (auto,auto,auto,auto,auto,),
    table.header([\#], [Ferramenta], [Categoria], [Descrição], [Caso de Uso],),
    table.hline(),
    [1], [`read`], [Arquivo], [Leitura de arquivos com offset/limit], [Inspecionar código em linhas específicas],
    [2], [`write`], [Arquivo], [Gravação direta de conteúdo], [Criar ou sobrescrever arquivos],
    [3], [`edit`], [Arquivo], [Edição por str\_replace], [Corrigir bugs, refatorar trechos],
    [4], [`ast_edit`], [Arquivo], [Edição por âncoras de hash], [Editar blocos grandes com menos tokens],
    [5], [`grep`], [Arquivo], [Busca por conteúdo (regex)], [Encontrar chamadas de função, padrões],
    [6], [`glob`], [Arquivo], [Busca por padrão de nome], [Listar arquivos por tipo ou local],
    [7], [`ast_grep`], [Arquivo], [Busca semântica em AST], [Encontrar padrões estruturais no código],
    [8], [`bash`], [Runtime], [Execução de comandos shell], [Builds, testes, instalações],
    [9], [`eval`], [Runtime], [Avaliação inline de Python/JS], [Transformação de dados, cálculos],
    [10], [`LSP`], [Avançada], [14 operações de inteligência de código], [Rename seguro, diagnósticos, code actions],
    [11], [`debug`], [Avançada], [28 operações DAP], [Depuração de processos nativos],
    [12], [`task`], [Avançada], [Fan-out de subagentes], [Decomposição de tarefas complexas],
    [13], [`browser`], [Avançada], [Automação de browser headless], [Scraping, testes UI, automação web],
    [14], [`computer`], [Avançada], [Controle nativo do desktop], [Automação de desktop, screenshots],
    [15], [`ask`], [Interação], [Picker de opções interativo], [Decisões que dependem do usuário],
    [16], [`web_search`], [Conhecimento], [Busca na web], [Pesquisa de documentação, APIs],
    [17], [`web_fetch`], [Conhecimento], [Fetch de conteúdo web], [Leitura de páginas, docs online],
    [18], [`memory`], [Conhecimento], [Gerenciamento de memória], [Retenção de contexto entre sessões],
    [19], [`retain`], [Conhecimento], [Armazenamento de contexto], [Salvar descobertas importantes],
    [20], [`recall`], [Conhecimento], [Recuperação de contexto], [Buscar informações salvas],
    [21], [`reflect`], [Conhecimento], [Reflexão sobre a sessão], [Análise de padrões e aprendizados],
    [22], [`learn`], [Conhecimento], [Aprendizado persistente], [Registrar regras e preferências],
    [23], [`mcp`], [Integração], [Servidores MCP], [Acesso a ferramentas externas],
    [24], [`pr`], [Integração], [GitHub Pull Requests], [Criar, revisar, comentar PRs],
    [25], [`issue`], [Integração], [GitHub Issues], [Criar, listar, comentar issues],
    [26], [`ssh`], [Integração], [Conexões SSH], [Execução remota em servidores],
    [27], [`git`], [Integração], [Operações Git], [Commits, branches, merges],
    [28], [`npm`], [Integração], [Gerenciamento de pacotes], [Instalar, atualizar dependências],
    [29], [`docker`], [Integração], [Containers Docker], [Build, run, manage containers],
    [30], [`calendar`], [Integração], [Calendário], [Agendar, verificar compromissos],
    [31], [`email`], [Integração], [Envio de e-mails], [Comunicação, notificações],
  )]
  , kind: table
  )

== Os 16 esquemas internos de URI
<os-16-esquemas-internos-de-uri>
Além das ferramentas, o OMP utiliza 16 esquemas de URI internos para referenciar recursos de forma padronizada. Esses esquemas permitem que o agente acesse diferentes tipos de recursos com uma sintaxe unificada.

#strong[pr:/\/] --- Referência a Pull Requests no GitHub.

#strong[issue:/\/] --- Referência a Issues no GitHub.

#strong[agent:/\/] --- Referência a subagentes em execução.

#strong[skill:/\/] --- Referência a skills instaladas.

#strong[ssh:/\/] --- Conexões SSH para execução remota.

#strong[file:/\/] --- Referência a arquivos locais.

#strong[url:/\/] --- Referência a URLs externas.

#strong[mcp:/\/] --- Referência a servidores MCP conectados.

E outros 8 esquemas para recursos internos do harness.

Esses esquemas são como os diferentes tipos de documentos de um estaleiro --- cada um tem sua formatação, seu protocolo de acesso, e sua finalidade específica.

== Fluxo de uso combinado
<fluxo-de-uso-combinado>
O poder real das ferramentas do OMP está na combinação. Veja um fluxo típico de refatoração.

```bash
# 1. Descobrir onde a função é usada
grep "processarPedido" --include "*.ts"

# 2. Ver a estrutura do código
ast_grep "function processarPedido($$$) { $$$ }"

# 3. Ler o arquivo completo
read src/services/pedido.ts

# 4. Fazer a edição com ast_edit (menos tokens)
ast_edit --hash "a3f8c2" --new "function processarPedido(dados: PedidoDTO): Promise<Resultado>"

# 5. Rodar testes para validar
bash "npm test -- --grep 'processarPedido'"

# 6. Verificar se o LSP aprovou
LSP diagnostics src/services/pedido.ts
```

Cada passo usa a ferramenta mais adequada para a tarefa. O agente não usa bash para tudo --- ele escolhe a ferramenta certa para cada etapa, economizando tokens e aumentando a precisão.

== Economia de tokens na prática
<economia-de-tokens-na-prática>
Note como cada ferramenta foi escolhida para minimizar o consumo de tokens.

#figure(
  align(center)[#table(
    columns: (6.98%, 48.84%, 32.56%, 11.63%),
    align: (auto,auto,auto,auto,),
    table.header([Ação], [Ferramenta Alternativa (menos eficiente)], [Ferramenta OMP (eficiente)], [Economia],),
    table.hline(),
    [Encontrar tipo], [bash + grep manual], [`grep` built-in], [\~40% menos tokens],
    [Ler trecho específico], [read arquivo inteiro], [read com offset/limit], [\~70% menos tokens],
    [Editar bloco], [edit com old\_string completo], [ast\_edit com hash], [\~61% menos tokens],
    [Validar], [bash + tsc manual], [LSP diagnostics], [\~50% menos tokens],
  )]
  , kind: table
  )

O resultado é uma sessão que consome menos tokens, é mais precisa, e produz menos erros. É a diferença entre um estaleiro que usa ferramentas manuais e um que usa equipamentos hidráulicos de precisão.

== Próximos Passos
<próximos-passos>
Neste capítulo, você abriu o arsenal completo do OMP. As 31 ferramentas built-in não são apenas uma lista de funcionalidades --- são o equipamento que transforma uma IA de conversação em um engenheiro de software autônomo.

Cada ferramenta tem seu papel, cada uma é otimizada para sua tarefa, e juntas elas cobrem todo o ciclo de vida do desenvolvimento: de inspecionar código existente a depurar processos em execução.

No próximo capítulo, você mergulhará fundo no sistema de hashline edits --- o mecanismo que reduz tokens de saída em até 61% e que é o coração da eficiência do OMP.

Acesse a referência completa de ferramentas: https:/\/omp.sh/docs/tools

Siga-nous nas redes sociais para dicas, tutoriais e novidades sobre o Oh My Pi.

#horizontalrule

= Edições Hashline: Precisão com Menos Tokens
<edições-hashline-precisão-com-menos-tokens>
== O problema que consome recursos
<o-problema-que-consome-recursos>
No estaleiro digital onde construímos harnesses de IA, existe um problema antigo que consome recursos como um motor sem eficiência: #strong[redundantemente enviamos o código completo] toda vez que queremos fazer uma pequena alteração.

Imagine um mestre de estaleiro que, para trocar um parafuso no casco, precisasse reconstruir todo o navio. Isso seria absurdo --- e é exatamente o que acontece quando usamos métodos tradicionais de edição.

O #strong[hashline edit] é a âncora que estabiliza nossa navegação. Em vez de enviar o conteúdo completo de um arquivo, o sistema gera um #strong[hash] (uma impressão digital criptográfica) de cada bloco de código.

Quando queremos modificar algo, bastamos referenciar o hash --- como um GPS que diz exatamente onde estamos no oceano digital, sem precisar descrever toda a rota.

== O fluxo tradicional: tokens desperdiçados
<o-fluxo-tradicional-tokens-desperdiçados>
Quando um agente de IA edita código, o fluxo tradicional é:

```
1. Ler o arquivo completo (N tokens)
2. Identificar o que mudar
3. Reescrever o arquivo inteiro (N tokens)
```

Isso significa que, para uma alteração de 10 linhas em um arquivo de 500 linhas, pagamos #strong[1000 tokens] --- o dobro do necessário. No estaleiro naval, seria como pintar todo o casco para trocar uma única tinta.

== A solução: hashes como âncoras
<a-solução-hashes-como-âncoras>
O hashline edit transforma esse fluxo.

```
1. Gerar hashes dos blocos existentes (custo: zero)
2. Referenciar o hash do bloco-alvo (custo: ~10 tokens)
3. Enviar apenas a alteração (custo: M tokens)
```

Agora, para aquela mesma alteração de 10 linhas, pagamos apenas #strong[\~10 tokens] --- uma redução de #strong[99%] no custo de edição.

== Como funciona o hash
<como-funciona-o-hash>
O hash é gerado a partir do conteúdo do bloco. Se o bloco não mudou, o hash permanece idêntico. Isso cria um sistema de #strong[referência estável].

#strong[Antes:] "Edite a função `processar_dados()` na linha 42"

#strong[Depois:] "Edite o bloco com hash `a1b2c3d4`"

A vantagem é que o hash não depende de números de linha (que mudam com edições) nem do conteúdo completo (que consome tokens).

== Comparação com str\_replace
<comparação-com-str_replace>
O método `str_replace` (substituição de strings) é como tentar encontrar uma agulha no palheiro.

#figure(
  align(center)[#table(
    columns: 4,
    align: (auto,auto,auto,auto,),
    table.header([Método], [Tokens por Edição], [Confiabilidade], [Colisões],),
    table.hline(),
    [Conteúdo completo], [\~1000], [Alta], [Zero],
    [str\_replace], [\~200], [Média], [Possíveis],
    [Hashline], [\~50], [Alta], [Criptograficamente improváveis],
  )]
  , kind: table
  )

O `str_replace` pode falhar quando o mesmo texto aparece múltiplas vezes, quando o texto contém caracteres especiais, ou quando o contexto é ambíguo.

O hash resolve isso porque cada bloco único gera um hash único --- como um GPS que mostra coordenadas exatas, não descrições vagas.

== A economia por modelo
<a-economia-por-modelo>
Os números são impressionantes.

#figure(
  align(center)[#table(
    columns: 4,
    align: (auto,auto,auto,auto,),
    table.header([Modelo], [Tokens Antes], [Tokens Depois], [Redução],),
    table.hline(),
    [Grok 4 Fast], [10.000], [3.900], [#strong[61%]],
    [Grok Code Fast 1], [10.000], [3.170], [#strong[68.3%]],
    [Gemini 3 Flash], [10.000], [5.200], [#strong[48%]],
  )]
  , kind: table
  )

A métrica chave: o Grok Code Fast 1 apresentou um #strong[10x lift] --- a taxa de sucesso em edições subiu de 6.7% (com str\_replace) para 68.3% (com hashline).

== Estrutura de um hash
<estrutura-de-um-hash>
O hash no Oh My Pi segue o padrão `#//<hash-8-chars>`.

Exemplo de blocos com hashes.

```python
#//a1b2c3d4
def processar_dados(dados):
    resultado = []
    for item in dados:
        if item.get("valido"):
            resultado.append(transformar(item))
    return resultado
#//a1b2c3d4
```

== Sintaxe de edição
<sintaxe-de-edição>
Para editar um bloco, o agente envia.

```
#//a1b2c3d4 (replace: <hash-do-bloco-novo>)
def processar_dados(dados):
    resultado = []
    for item in dados:
        if item.get("valido") and item.get("prioridade") > 5:
            resultado.append(transformar(item))
    return resultado
#//nova1234
```

== Exemplo prático
<exemplo-prático>
#strong[Cenário:] Queremos adicionar validação de tipos na função.

#strong[Método Tradicional (str\_replace):]

```
Substituir:
def processar_dados(dados):
    resultado = []
    for item in dados:
        if item.get("valido"):
            resultado.append(transformar(item))
    return resultado

Por:
def processar_dados(dados: list[dict]) -> list:
    resultado = []
    for item in dados:
        if item.get("valido"):
            resultado.append(transformar(item))
    return resultado
```

#strong[Custo:] \~150 tokens

#strong[Método Hashline:]

```
#//a1b2c3d4 (replace: <hash-do-bloco-novo>)
def processar_dados(dados: list[dict]) -> list:
    resultado = []
    for item in dados:
        if item.get("valido"):
            resultado.append(transformar(item))
    return resultado
#//f1e2d3c4
```

#strong[Custo:] \~80 tokens

== Implementação no Oh My Pi
<implementação-no-oh-my-pi>
```python
import hashlib

def gerar_hash(conteudo: str) -> str:
    """Gera hash curto de 8 caracteres para um bloco de código."""
    return hashlib.sha256(conteudo.encode()).hexdigest()[:8]

def identificar_blocos(arquivo: str) -> dict:
    """Identifica blocos delimitados por hashes e retorna mapeamento."""
    blocos = {}
    linhas = arquivo.split("\n")
    hash_atual = None
    inicio = 0
    
    for i, linha in enumerate(linhas):
        if linha.startswith("#//") and len(linha) == 11:
            if hash_atual is None:
                hash_atual = linha[3:]
                inicio = i + 1
            else:
                blocos[hash_atual] = {
                    "inicio": inicio,
                    "fim": i,
                    "conteudo": "\n".join(linhas[inicio:i])
                }
                hash_atual = None
    
    return blocos
```

== Quando usar hashline edits
<quando-usar-hashline-edits>
#figure(
  align(center)[#table(
    columns: 2,
    align: (auto,auto,),
    table.header([Cenário], [Recomendação],),
    table.hline(),
    [Edição de função existente], [✅ Hashline],
    [Adição de nova função], [✅ Hashline],
    [Modificação de múltiplos blocos], [✅ Hashline],
    [Reescrita completa do arquivo], [❌ Conteúdo completo],
    [Busca e substituição simples], [⚠️ str\_replace pode bastar],
  )]
  , kind: table
  )

== Caso de uso: refatoração de código
<caso-de-uso-refatoração-de-código>
Imagine que você é o mestre de estaleiro e precisa modernizar o motor do navio.

#strong[Antes (Código Legado):]

```python
#//motor001
def calcular_velocidade(distancia, tempo):
    return distancia / tempo
#//motor001
```

#strong[Depois (Código Modernizado com Hashline):]

```python
#//motor001 (replace: <novo-hash>)
def calcular_velocidade(distancia: float, tempo: float) -> float:
    """Calcula a velocidade média em km/h.
    
    Args:
        distancia: Distância percorrida em km
        tempo: Tempo gasto em horas
    
    Returns:
        Velocidade média em km/h
    
    Raises:
        ValueError: Se tempo for zero ou negativo
    """
    if tempo <= 0:
        raise ValueError("Tempo deve ser positivo")
    return distancia / tempo
#//motor-novo
```

#strong[Economia:] Em vez de enviar todo o arquivo (que pode ter centenas de linhas), enviamos apenas o hash do bloco (\~8 tokens) + a alteração (\~50 tokens) = \~58 tokens, em vez de \~500+ tokens.

== Dicas do Mestre de Estaleiro
<dicas-do-mestre-de-estaleiro>
#strong[Seja preciso.] Um hash errado edita o bloco errado. Sempre verifique antes de enviar.

#strong[Prefira blocos pequenos.] Blocos menores = hashes mais específicos = menos ambiguidade.

#strong[Use para iterações rápidas.] Quando você está testando múltiplas versões, hashline reduz o custo drasticamente.

#strong[Combine com outras ferramentas.] Use hashline para edições pontuais e outros métodos para reestruturações maiores.

== Próximos Passos
<próximos-passos-1>
Assim como um mestre de estaleiro experiente sabe exatamente qual parte do casco precisa de reparo sem precisar desmontar todo o navio, o hashline edit permite que agentes de IA façam edições precisas com o mínimo de recursos.

Os números falam por si: #strong[61% menos tokens] com o Grok 4 Fast, #strong[10x de melhoria] na acurácia com o Grok Code Fast 1, e #strong[5 pontos percentuais] de vantagem sobre str\_replace com o Gemini 3 Flash.

No próximo capítulo, vamos explorar como integrar essas edições em fluxos de trabalho mais complexos, combinando hashline com outras técnicas de otimização.

Lembre-se: no estaleiro digital, #strong[precisão é mais valiosa que quantidade]. Cada token economizado é um nó a mais no cabo que segura o navio no porto.

Acesse a documentação completa: https:/\/omp.sh/docs

Siga-nous nas redes sociais para dicas, tutoriais e novidades sobre o Oh My Pi.

#horizontalrule

// ── CONTRACAPA ────────────────────────────────────────────────────
#pagebreak()
