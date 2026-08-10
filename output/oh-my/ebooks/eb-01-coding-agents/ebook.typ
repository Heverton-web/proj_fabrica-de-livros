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
  title: "O Que é um Coding Agent e Por Que Você Precisa de Um & Arquitetura do OMP: 80.000 Linhas de Rust",
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
      align(center, "O Que é um Coding Agent e Por Que Você Precisa de Um & Arquitetura do OMP: 80.000 Linhas de Rust")
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
      #text(font: ("Inter", "Liberation Sans", "Arial"), size: 34pt, weight: "bold", fill: white)[O Que é um Coding Agent e Por Que Você Precisa de Um & Arquitetura do OMP: 80.000 Linhas de Rust]
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
    #text(font: ("Inter", "Liberation Sans", "Arial"), size: 22pt, weight: "bold", fill: cor.primaria)[O Que é um Coding Agent e Por Que Você Precisa de Um & Arquitetura do OMP: 80.000 Linhas de Rust]
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
= O Que é um Coding Agent e Por Que Você Precisa de Um
<o-que-é-um-coding-agent-e-por-que-você-precisa-de-um>
== Você já usou autocomplete inteligente?
<você-já-usou-autocomplete-inteligente>
Provavelmente sim. Aquele que sugere a próxima linha de código enquanto você digita. Ou talvez um assistente de IA que responde perguntas sobre programação.

Mas e se existisse algo muito diferente disso?

Algo que não apenas sugere ou responde --- mas que pega a tarefa nas mãos, navega pelo seu projeto, edita arquivos, roda testes e entrega um resultado completo?

É exatamente isso um #strong[coding agent].

== Como funciona um coding agent?
<como-funciona-um-coding-agent>
Imagine que você pede para um colega desenvolvedor corrigir um bug. O que ele faz?

Ele lê o código, entende o contexto, localiza o problema, escreve a correção, roda os testes e verifica se tudo funciona.

Um #strong[coding agent] faz exatamente isso --- mas de forma autônoma, usando um modelo de linguagem como "cérebro" e um conjunto de ferramentas como "mãos".

== A diferença crucial: assistente vs.~agente
<a-diferença-crucial-assistente-vs.-agente>
Muita gente confunde três categorias completamente diferentes.

#strong[Autocomplete] sugere a próxima linha ou bloco de código. Você aceita ou rejeita. É o Copilot no VS Code.

#strong[Assistente de chat] responde perguntas sobre código, explica conceitos, gora trechos. Você precisa copiar e colar o resultado. É o ChatGPT para programação.

#strong[Coding agent] recebe uma tarefa e executa sozinho --- lendo, editando, testando, corrigindo até entregar.

A diferença não é sutil. É como a diferença entre um amigo que te dá dicas de navegação por telefone e um piloto automático que conduz o navio inteiro ao porto.

== Por que o harness importa
<por-que-o-harness-importa>
Aqui entra um conceito que vai guiar tudo: o #strong[harness].

O harness é toda a infraestrutura que conecta o LLM ao mundo real --- as ferramentas, a permissão para usá-las, o sistema de arquivos, os protocolos de comunicação.

Mario Zechner, criador do Pi (o coding agent original), publicou um post intitulado "The Harness Problem" onde argumenta que o gargalo da programação assistida por IA não é mais o modelo em si --- é o que conecta o modelo ao código.

Pare e sinta o tamanho disso.

Com modelos como GPT-4o, Claude Opus e Gemini Ultra disponíveis, o problema não é inteligência artificial faltando. O problema é ter o estaleiro completo para transformar essa inteligência em código funcional.

É como ter o melhor motor do mundo mas não ter leme, âncora ou instrumentos de navegação no navio.

== O Oh My Pi como resposta
<o-oh-my-pi-como-resposta>
O OMP nasceu exatamente para resolver esse problema.

Fork avançado do Pi de Mario Zechner, o OMP transformou o conceito de coding agent em algo que o próprio Zechner descreveu como "o harness mais completo do mercado".

São aproximadamente 80.000 linhas de Rust, suporte a mais de 60 providers de LLM e 31 ferramentas built-in que cobrem desde edição de arquivos até debug de binários nativos e automação de browser.

Quando o repositório can1357/oh-my-pi atingiu 23.3k estrelas no GitHub, não foi apenas um número --- foi a comunidade de desenvolvedores reconhecendo que o harness, e não o modelo, é o que faz a diferença na prática do dia a dia.

== O Estaleiro de Navios
<o-estaleiro-de-navios>
Imagine que você é o mestre de estaleiro de um estaleiro digital. Seu trabalho é transformar chapas de aço bruto em navios capazes de cruzar oceanos.

Um assistente de código é como um estagiário no estaleiro: ele te dá sugestões pontuais --- "talvez essa solda ficasse melhor aqui" --- mas você precisa fazer todo o trabalho manual.

Um coding agent, por outro lado, é como uma tripulação inteira e autônoma: ele pega a chapa de aço, corta, solda, instala o motor, monta a instrumentação e entrega o navio pronto para navegar.

Mas aqui está o ponto crucial: o harness é o estaleiro inteiro. Não é apenas o motor (o LLM). São as ferramentas de corte (edição de código), os equipamentos de solda (execução de comandos), o compás (regras e permissões), o GPS (busca em código), e o sistema de comunicação (protocolos entre ferramentas).

Sem o estaleiro completo, o melhor motor do mundo não constrói nenhum navio.

== A arquitetura de um coding agent
<a-arquitetura-de-um-coding-agent>
Um coding agent moderno tem quatro camadas fundamentais:

```yaml
coding_agent:
  cerebro:              # O LLM que decide o que fazer
    provider: openai
    model: gpt-4o
    
  ferramentas:          # As "maos" do agente
    - read: ler arquivos
    - write: criar arquivos
    - edit: editar arquivos existentes
    - bash: executar comandos
    - grep: buscar em codigo
    - glob: buscar arquivos por padrao
    
  permissoes:           # O "compas" do agente
    allow_read: true
    allow_write: true
    allow_network: false
    
  loop:                 # O "ciclo de navegacao"
    - observar: ler o estado atual
    - planejar: decidir proxima acao
    - agir: executar a ferramenta
    - verificar: checar resultado
    - repetir ate entregar
```

== O OMP em números
<o-omp-em-números>
O OMP vai muito além dessa estrutura básica. Veja os números que o diferenciam.

#strong[80.000 linhas de Rust:] performance nativa, sem overhead de interpretadores.

#strong[60+ providers de LLM:] de APIs frontier (OpenAI, Anthropic, Google) a modelos locais (Ollama, vLLM).

#strong[31 ferramentas built-in:] incluindo LSP (14 operações), DAP/debug (28 operações), browser automation e desktop control.

#strong[23.3k estrelas no GitHub:] a maior base de usuários entre harnesses open-source.

== Como o OMP executa uma tarefa
<como-o-omp-executa-uma-tarefa>
O ciclo de execução do OMP segue o padrão "observe-planifique-agir-verifique".

#strong[Observar:] o agente lê o estado atual do projeto --- arquivos, erros, contexto.

#strong[Planejar:] o LLM decide quais ferramentas usar e em que ordem.

#strong[Agir:] cada ferramenta é executada com permissões controladas pelo harness.

#strong[Verificar:] o resultado é checado --- código compila? testes passam?

#strong[Repetir:] se algo falhou, o agente adapta o plano e tenta novamente.

Esse ciclo é o que transforma um LLM --- que sozinho apenas gera texto --- em um agente que realmente constrói software. O harness é a diferença entre um motor na prateleira e um navio no oceano.

== O erro que todo iniciante comete
<o-erro-que-todo-iniciante-comete>
Você acabou de instalar um coding agent. Animado, abre o terminal e digita: "Me ajude a corrigir esse bug".

O agente responde com uma explicação bonita sobre o que pode estar errado, talvez até sugira uma correção. Você copia, cola, testa… e não funciona. Por quê?

Porque você tratou um coding agent como um assistente de chat. Essa é a armadilha mais comum para quem está começando: pedir "ajuda" em vez de pedir "ação".

O agente não quer te explicar o bug --- ele quer corrigir o bug. A diferença é sutil mas transformadora.

Quando você diz "corrija o bug na função `processar_pedido` que retorna `undefined` ao invés de `null` quando o carrinho está vazio", o agente faz exatamente isso: lê o arquivo, encontra a função, corrige o retorno, roda os testes e entrega o resultado.

Você não precisou copiar nada. Não precisou colar nada. O estaleiro inteiro trabalhou para você.

== Armadilhas comuns ao usar coding agents
<armadilhas-comuns-ao-usar-coding-agents>
#strong[Delegar sem contexto suficiente.] O agente precisa saber o que você quer. Dê requisitos claros, não apenas "faça isso funcionar".

#strong[Não verificar o resultado.] O agente entrega código, mas você deve revisar. Ele é autônomo, não infalível.

#strong[Ignorar o custo de tokens.] Features como advisor model e subagentes aumentam o consumo. Saiba quando usar cada um.

#strong[Esquecer o sandboxing.] Browser automation e desktop control expõem superfície de ataque. Use permissões adequadas.

== Métricas reais de impacto
<métricas-reais-de-impacto>
Se você ainda trata a IA como um extra opcional no seu fluxo, saiba que 23.3k desenvolvedores já escolheram o OMP como ferramenta principal --- e o número cresce a cada semana.

O harness completo não é mais luxo; é infraestrutura padrão para quem leva desenvolvimento a sério em 2026.

== Resumo
<resumo>
Um coding agent é mais que um assistente. Ele combina LLM com ferramentas reais para executar tarefas de programação de ponta a ponta --- ler, editar, testar e entregar código.

O harness é o gargalo, não o modelo. Conforme Mario Zechner argumentou em "The Harness Problem", a infraestrutura que conecta o LLM ao código importa mais que a inteligência do modelo em si.

O OMP resolve o harness problem. Com 80.000 linhas de Rust, 60+ providers e 31 ferramentas, o OMP é o estaleiro mais completo disponível --- e é por isso que 23.3k+ desenvolvedores já o adotaram.

== Próximos Passos
<próximos-passos>
Você acabou de descobrir o que é um coding agent e por que o harness é o verdadeiro gargalo da programação assistida por IA. Mas isso é apenas o início.

No próximo capítulo, vamos mergulhar na arquitetura técnica do OMP --- as 80.000 linhas de Rust que formam o casco, o motor e toda a instrumentação do estaleiro.

Quer saber mais? Acesse o repositório oficial do OMP no GitHub: https:/\/github.com/can1357/oh-my-pi

Siga-nous nas redes sociais para dicas, tutoriais e novidades sobre o Oh My Pi. Junte-se a mais de 23.3k desenvolvedores que já estão usando o harness mais completo do mercado.

#horizontalrule

= Arquitetura do OMP: 80.000 Linhas de Rust
<arquitetura-do-omp-80.000-linhas-de-rust>
== Abrindo as portas do estaleiro
<abrindo-as-portas-do-estaleiro>
No capítulo anterior, você descobriu o que é um coding agent e por que o harness --- e não o modelo LLM --- é o verdadeiro gargalo da programação assistida por IA.

Agora é hora de abrir as portas do estaleiro e olhar para dentro. Quais são as peças que compõem esse navio, como elas se encaixam e por que foram forjadas em Rust.

== Os 6 blocos de construção
<os-6-blocos-de-construção>
Um crate, no universo Rust, é como um módulo independente --- uma peça do estaleiro que tem sua própria função e se conecta às outras por interfaces definidas. O OMP é dividido em 6 crates principais.

#strong[pi-natives:] o arsenal de ferramentas. São as 31 ferramentas built-in do OMP --- read, write, edit, bash, grep, glob, lsp, debug, task, browser e muitas outras. Cada ferramenta é uma peça de equipamento do estaleiro, pronta para ser acionada pelo agente.

#strong[pi-shell:] o orquestrador. É ele que recebe o pedido do usuário, gerencia o ciclo de conversa com o LLM, despacha chamadas de ferramentas e coordena o fluxo completo. Pense nele como o painel de controle do estaleiro --- onde todas as informações convergem e todas as decisões são tomadas.

#strong[pi-ast:] o manipulador de código-fonte. Este crate entende a estrutura sintática dos arquivos --- árvores sintáticas abstratas (AST) --- permitindo edições precisas como ast\_edit e ast\_grep. Em vez de editar texto cru, o pi-ast navega pela estrutura do código como um engenheiro que lê uma planta em vez de adivinhar onde cortar.

#strong[pi-iso:] o isolador. Responsável por sandboxes e isolamento de execução, garantindo que comandos rodem em ambientes controlados. É o sistema de segurança do estaleiro --- as câmaras de prova que impedem que um erro em uma peça comprometa o navio inteiro.

#strong[pi-voice:] a interface com o LLM. Este crate gerencia a comunicação com mais de 60 providers de modelo --- OpenAI, Anthropic, Google, modelos locais e qualquer API compatível com OpenAI. É a voz do estaleiro: traduz intenções humanas em instruções que o motor entende.

#strong[pi-walker:] o explorador de código. Responsável por navegar pela estrutura de diretórios, indexar arquivos e manter o mapa do projeto atualizado. É o GPS do estaleiro --- sem ele, o agente estaria perdido em um mar de arquivos.

== Por que Rust?
<por-que-rust>
A pergunta que qualquer desenvolvedor faz ao ver um harness de 80.000 linhas é: por que não Python? Por que não Go? Por que não Node.js?

A resposta tem a ver com três requisitos que nenhum outro atende simultaneamente.

=== Segurança de memória sem garbage collector
<segurança-de-memória-sem-garbage-collector>
Rust garante segurança de memória em tempo de compilação --- sem GC interrompendo a execução, sem memory leaks silenciosos. Para um harness que roda por horas em sessões longas de código, isso não é luxo, é necessidade.

Um memory leak em Python pode derrubar uma sessão de 3 horas no minuto 179. Em Rust, isso simplesmente não acontece.

=== Performance nativa
<performance-nativa>
O OMP precisa processar árvores sintáticas, compilar expressões regex, gerenciar subprocessos e serializar dados em tempo real. Rust entrega performance comparável a C/C++ com muito menos risco de bugs.

Num harness onde cada milissegundo de latência se acumula em milhares de turns, a velocidade de compilação de código nativo faz diferença real.

=== Zero-fork: tudo em um binário
<zero-fork-tudo-em-um-binário>
Esta é talvez a decisão mais importante. O OMP é distribuído como um único binário executável. Não depende de Node.js instalado. Não depende de Python. Não depende de nada além do sistema operacional.

Isso significa que o estaleiro inteiro --- casco, motor, equipamento, instrumentação --- cabe em um arquivo que você baixa e roda. Sem instalação de dependências. Sem conflitos de versão. Sem "funciona na minha máquina".

== O volume de código
<o-volume-de-código>
Para colocar em perspectiva: 80.000 linhas de Rust no core do OMP correspondem ao tamanho de um projeto de engenharia de software de médio a grande porte.

Mas o OMP não para aí --- ele incorpora cerca de 80.000 linhas adicionais de código vendored, que incluem reimplementações de ferramentas clássicas do Unix em Rust. São 58 command-line utilities portadas de bash e coreutils para Rust nativo, garantindo que cada ferramenta que o agente executa rode com performance máxima e sem dependências externas.

Isso transforma o OMP em um estaleiro autocontido: ele não precisa pedir emprestado equipamento de outros estaleiros. Tudo está a bordo.

== A planta baixa do estaleiro
<a-planta-baixa-do-estaleiro>
Imagine que você está olhando para a planta baixa do estaleiro mais avançado do mundo. Cada área tem uma função específica, e todas se conectam por corredores bem definidos.

#strong[A Doca (pi-natives):] onde ficam todas as ferramentas de construção --- guindastes, soldadoras, cortadoras. Cada peça de equipamento está catalogada e pronta para uso.

#strong[O Painel de Controle (pi-shell):] o centro nervoso. Aqui o mestre de estaleiro envia ordens, e o sistema as distribui para as áreas corretas.

#strong[A Fundição (pi-ast):] onde o código-fonte é moldado. Em vez de cortar chapas no escuro, o engenheiro vê cada peça em 3D --- a árvore sintática --- e faz cortes precisos.

#strong[As Câmaras de Prova (pi-iso):] onde testes de segurança são feitos. Nenhuma peça entra no navio sem passar por aqui primeiro.

#strong[A Rádio (pi-voice):] a estação de comunicação que conecta o estaleiro ao mundo exterior --- neste caso, ao LLM que fornece a inteligência.

#strong[O Mapa-Múndi (pi-walker):] onde fica a planta do projeto inteiro. O engenheiro consulta este mapa para saber onde está cada arquivo e como eles se relacionam.

== O pi-shell: como o orquestrador funciona
<o-pi-shell-como-o-orquestrador-funciona>
O pi-shell é o coração do OMP. Veja como ele gerencia o ciclo de conversa.

```rust
// Simplificacao do ciclo de execucao do pi-shell
pub async fn run_turn(user_input: &str) -> Result<String> {
    // 1. O shell recebe o input do usuario
    let messages = build_messages(user_input);
    
    // 2. Envia para o LLM via pi-voice
    let response = pi_voice::chat_completion(messages).await?;
    
    // 3. Se o LLM chama uma ferramenta, despacha para pi-natives
    match response.tool_call {
        Some(call) => {
            let result = pi_natives::execute(call).await?;
            // 4. Alimenta o resultado de volta ao LLM
            messages.push(tool_result(result));
            run_turn("").await // repete ate o LLM finalizar
        }
        None => Ok(response.text)
    }
}
```

Esse loop --- receber, consultar o LLM, executar ferramenta, retornar resultado --- é o ciclo de vida básico de toda interação no OMP. Cada iteração é um turno de conversa entre o estaleiro (harness) e o motor (LLM).

== O pi-ast: editando código como um engenheiro
<o-pi-ast-editando-código-como-um-engenheiro>
Enquanto a maioria dos harnesses edita código como texto cru (encontrar linha X, substituir por Y), o pi-ast trabalha com a estrutura sintática.

As #strong[hashline edits] são o que reduz tokens de saída em até 61% comparado a edições por str\_replace tradicionais. Em vez de enviar centenas de linhas de contexto, o agente aponta um hash e diz "edite aqui".

É como marcar uma peça na planta do estaleiro com um código de barras em vez de descrever sua posição por GPS.

== O pi-natives: o arsenal completo
<o-pi-natives-o-arsenal-completo>
O pi-natives expõe 31 ferramentas organizadas em categorias.

#strong[Arquivo:] read, write, edit, ast\_edit, ast\_grep, grep, glob.

#strong[Runtime:] bash, eval\_python, eval\_js.

#strong[Inteligência:] lsp (14 operações), debug (28 operações DAP), task.

#strong[Automação:] browser (Puppeteer + CDP), computer (controle de desktop).

#strong[Comunicação:] subagent (fan-out paralelo), advisor (modelo revisor).

Cada ferramenta é implementada como um módulo dentro do pi-natives, com assinatura padronizada que o pi-shell usa para despacho. É o catálogo de equipamentos do estaleiro --- e com 31 opções, há uma ferramenta para cada tarefa.

== O pi-voice: conectando a mais de 60 providers
<o-pi-voice-conectando-a-mais-de-60-providers>
O pi-voice abstrai a comunicação com LLMs. Em vez de escrever código específico para cada provider, ele usa uma interface comum.

O diferencial é que o OMP não se prende a um único ecossistema. Você pode usar GPT-4o para decisões rápidas, Claude Opus para raciocínio profundo e um modelo local para tarefas baratas --- tudo no mesmo harness, sem trocar de ferramenta.

== O pi-iso: o sandbox que protege
<o-pi-iso-o-sandbox-que-protege>
Toda execução de comando passa pelo pi-iso, que garante isolamento. É a camada de segurança que permite ao agente executar código arbitrário sem comprometer o sistema do usuário.

== O pi-walker: o GPS do projeto
<o-pi-walker-o-gps-do-projeto>
O pi-walker mantém um mapa atualizado do projeto. Essa indexação permite que o agente navegue pelo projeto com eficiência --- encontrar arquivos por padrão, buscar conteúdo por regex, entender a hierarquia de diretórios.

Sem o pi-walker, o agente estaria perdido em projetos grandes.

== A analogia do casco em Rust
<a-analogia-do-casco-em-rust>
Pense no OMP como um submarino. Um submarino em Python seria como um barco de borracha --- funcional, mas com limites claros de profundidade e pressão. Um submarino em Go seria como um barco de fibra de vidro --- mais resistente, mas ainda com pontos de fragilidade na solda.

Um submarino em Rust? É um casco de aço titânio: testado em compile-time para resistir a cada pressão que encontrará no oceano profundo do desenvolvimento de software real.

== O erro que todo arquiteto comete
<o-erro-que-todo-arquiteto-comete>
Você está configurando um novo projeto e decide usar um coding agent. Instala o agente, configura o provider e começa a trabalhar. Tudo parece bem --- até que o agente precisa editar um arquivo de configuração de 500 linhas.

Ele lê o arquivo inteiro, envia para o LLM, e o LLM responde com a edição. Mas a edição está incorreta: ele trocou a linha errada porque o contexto era confuso demais.

O que aconteceu? O harness que você escolheu não tem LSP integrado, não tem hashline edits, não tem ast\_edit. Ele está tentando editar código como se fosse texto corrido --- como um estaleiro que tenta soldar peças sem ver a planta.

Quando você migra para o OMP, o mesmo cenário se transforma: o pi-ast analisa a estrutura do arquivo, o pi-walker fornece o mapa do projeto, o pi-shell despacha a edição com hash de conteúdo, e o resultado é preciso.

== Armadilhas comuns ao arquitetar com harnesses
<armadilhas-comuns-ao-arquitetar-com-harnesses>
#strong[Ignorar o custo de tokens por crate.] Cada crate gera overhead de comunicação. Usar o advisor model dobra o custo de tokens por turno. Saiba quando ativar e quando desativar.

#strong[Não configurar sandbox adequado.] O pi-iso existe por um motivo. Executar comandos sem restrições de rede ou filesystem é como abrir as comportas do estaleiro para o mar --- qualquer coisa pode entrar.

#strong[Esquecer que o harness é o gargalo.] Mesmo com o OMP, se o seu LLM é fraco, o resultado será fraco. O harness potencializa o modelo, não compensa deficiências dele.

#strong[Não explorar os 31 nativos.] Muitos usuários ficam em read/write/edit e nunca descobrem que o OMP tem browser automation, desktop control e debug adapter nativo.

== Métricas que importam
<métricas-que-importam>
Ao avaliar a arquitetura de um harness, três números contam a história completa: quantidade de ferramentas built-in (quanto mais, menos dependências externas), número de providers suportados (quanto mais, mais flexibilidade) e se o binário é autocontido (zero-fork = zero dependências).

O OMP lidera nos três: 31 ferramentas, 60+ providers e um binário único em Rust.

== Próximos Passos
<próximos-passos-1>
Você agora conhece os 6 crates do OMP e entendeu por que Rust foi a escolha certa para construir o harness mais completo do mercado. A teoria do estaleiro ficou clara.

No próximo capítulo, vamos sair da planta baixa e colocar as mãos na massa: instalação, configuração do provider e sua primeira sessão interativa com o OMP.

Para mais detalhes técnicos, acesse a documentação oficial: https:/\/omp.sh/docs

Siga-nous nas redes sociais para dicas, tutoriais e novidades sobre o Oh My Pi. Junte-se a mais de 23.3k desenvolvedores que já estão usando o harness mais completo do mercado.

#horizontalrule

// ── CONTRACAPA ────────────────────────────────────────────────────
#pagebreak()
