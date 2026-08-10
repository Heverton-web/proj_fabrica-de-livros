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
  title: "Colaboração ao Vivo com /collab & Browser e Desktop: Além do Código",
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
      align(center, "Colaboração ao Vivo com /collab & Browser e Desktop: Além do Código")
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
      #text(font: ("Inter", "Liberation Sans", "Arial"), size: 34pt, weight: "bold", fill: white)[Colaboração ao Vivo com /collab & Browser e Desktop: Além do Código]
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
    #text(font: ("Inter", "Liberation Sans", "Arial"), size: 22pt, weight: "bold", fill: cor.primaria)[Colaboração ao Vivo com /collab & Browser e Desktop: Além do Código]
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
= Colaboração ao Vivo com /collab
<colaboração-ao-vivo-com-collab>
== Um colega sentado ao seu lado
<um-colega-sentado-ao-seu-lado>
No capítulo anterior, você configurou o advisor model --- um revisor que observa cada turno e injeta notas inline, como um inspetor de qualidade que acompanha a construção do navio sem tocar em nenhuma ferramenta.

Mas e se, em vez de apenas um revisor distante, você pudesse ter um colega sentado ao seu lado no estaleiro, vendo exatamente o que você vê, apontando para o mesmo casco, e até mesmo segurando a chave de boca junto com você?

É exatamente isso que o comando `/collab` transforma em realidade.

== O que é o /collab e como ele funciona
<o-que-é-o-collab-e-como-ele-funciona>
Imagine que você está construindo um navio no estaleiro e quer mostrar o progresso para um colega que está em outro porto. Você poderia tirar fotos e enviar por e-mail, mas isso é lento e desatualizado. Ou poderia ligar uma câmera ao vivo --- aí o colega vê tudo em tempo real, sem atraso.

O `/collab` é essa câmera ao vivo para a sua sessão OMP.

Quando você digita `/collab` no terminal, o OMP inicia um processo de relay: ele cria um servidor local temporário que compartilha a tela do terminal com quem tiver o link. Não é um streaming de vídeo --- é uma conexão bidirecional onde o teammate pode ver tudo o que acontece na sessão e, dependendo do modo, até participar ativamente.

== Dois modos, dois papéis
<dois-modos-dois-papéis>
O OMP oferece dois modos de acesso para a colaboração.

#strong[Read-write:] o teammate pode não apenas ver, mas também digitar comandos, enviar mensagens ao agente e interagir com a sessão como se estivesse no seu terminal. É como entregar a chave do estaleiro para o colega --- ele pode usar qualquer equipamento.

#strong[Read-only:] o teammate apenas observa. Ele vê cada comando que você digita, cada resposta do agente, cada edição de arquivo --- mas não pode intervir. É como colocar uma câmera de segurança no estaleiro: a tripulação trabalha normalmente, mas o observador vê tudo sem tocar em nada.

A escolha entre um e outro depende do cenário. Para um code review, o read-only pode ser suficiente. Para um pair programming onde vocês dois precisam editar o mesmo arquivo, o read-write é essencial.

== Como o link é gerado
<como-o-link-é-gerado>
O fluxo é simples. Você digita `/collab`, o OMP gera um link da forma `http://localhost:<porta>/collab` e exibe um QR code no terminal. Seu teammate escaneia o QR code com o celular ou abre o link no navegador. A partir desse momento, ele está conectado à sua sessão.

Não há necessidade de criar contas, configurar permissões ou instalar plugins. O link é temporário --- assim como a sessão, ele expira quando você encerra o collab.

== Segurança: o que sai da sua máquina
<segurança-o-que-sai-da-sua-máquina>
Essa é a pergunta que todo Mestre de Estaleiro Digital faz antes de abrir as portas do estaleiro: "o que o visitingante pode ver?"

O OMP protege a sessão usando um mecanismo chamado #strong[frames sealed client-side]. Cada frame de dados --- cada mensagem que o teammate vê --- é selado no seu computador antes de ser transmitido. Isso significa que o conteúdo é criptografado no ponto de origem e só pode ser descriptografado no ponto de destino.

O que isso implica na prática? Chaves de API, tokens de autenticação, variáveis de ambiente sensíveis --- nada disso vaza para o teammate. O OMP filtra automaticamente o que pode e o que não pode ser compartilhado.

É como ter um estaleiro com vidros opacos: a tripulação vê tudo por dentro, mas o visitingante só vê o que está exposto no convés.

== Ativando a colaboração
<ativando-a-colaboração>
O comando para iniciar uma sessão de colaboração é direto.

```bash
/collab
```

O OMP responderá com um link e um QR code. O formato do link é `http://localhost:<porta>/collab`. A porta é atribuída automaticamente pelo OMP --- você não precisa configurar nada.

== Escolhendo o modo de acesso
<escolhendo-o-modo-de-acesso>
Quando o teammate abre o link, ele vê uma tela de boas-vindas com duas opções.

#strong[Entrar como observador (read-only):] clique no botão "Entrar como observador". A partir desse momento, ele vê tudo o que acontece na sessão, mas não pode digitar nada.

#strong[Entrar como colaborador (read-write):] clique no botão "Entrar como colaborador". Agora ele pode digitar comandos, enviar mensagens ao agente e editar arquivos --- exatamente como você.

No terminal do anfitrião, aparece uma notificação indicando quem entrou e em qual modo.

== O que o teammate vê
<o-que-o-teammate-vê>
Independentemente do modo, o teammate visualiza o terminal inteiro --- cada comando digitado, cada resposta do agente, cada erro que aparece. As edições de arquivo --- quando o agente modifica um arquivo, o teammate vê a diff em tempo real. E os pensamentos do agente --- se o agente estiver usando modo verbose, o teammate vê o raciocínio por trás de cada ação.

O que o teammate não vê: variáveis de ambiente (tokens, senhas, chaves de API), arquivos sensíveis (.env, credenciais), e processos internos do OMP.

Essa separação é automática e transparente --- você não precisa configurar filtros manualmente.

== Encerrando a sessão collab
<encerrando-a-sessão-collab>
Quando o trabalho estiver pronto, basta digitar.

```bash
/collab --stop
```

O servidor relay é encerrado, o link expira e o teammate perde a conexão imediatamente. Não há dados persistentes --- tudo o que aconteceu na sessão fica no seu terminal, não no servidor relay.

== Cenário prático: code review ao vivo
<cenário-prático-code-review-ao-vivo>
Imagine que você acabou de implementar uma funcionalidade complexa. Você quer que um colega mais experiente revise o código antes de commitar. Em vez de enviar um diff por e-mail e esperar horas pelo feedback, você faz o seguinte.

Primeiro, digita `/collab` no terminal. Depois, escaneia o QR code com o celular e envia o link para o colega pelo Slack. O colega abre o link no browser e entra como observador (read-only). Enquanto você explica o código, o colega vê cada linha, cada variável, cada decisão de arquitetura.

Ele aponta: "na linha 47, aquele `try/except` deveria capturar `ConnectionError` especificamente, não `Exception`". Você corrige na hora, o colega confirma, e o código está pronto para commit.

O tempo total? Minutos, não horas. E o nível de detalhe é o mesmo de estarem sentados lado a lado no estaleiro.

== Armadilhas comuns
<armadilhas-comuns>
#strong[Esquecer de encerrar o collab.] Se você deixar o servidor relay rodando depois de terminar o trabalho, o link continua válido. Sempre digite `/collab --stop` ao final da sessão.

#strong[Usar read-write sem necessidade.] Se o teammate só precisa observar, não dê acesso de escrita. Mais permissões do que o necessário são sempre um risco --- mesmo com o sealed client-side, é melhor prevenir.

#strong[Confundir collab com compartilhamento de tela.] O collab não é um streaming de vídeo --- é uma conexão direta ao terminal. O teammate vê os comandos, não a sua tela de desktop.

#strong[Até onde escala:] o collab funciona bem para sessões de 2 a 5 pessoas. Acima disso, a latência de conexão e a quantidade de dados transmitidos podem degradar a experiência.

== Próximos Passos
<próximos-passos>
Neste capítulo, você viu como o `/collab` transforma o terminal em um espaço de trabalho compartilhado. Dois modos de acesso --- read-write para colaboração ativa, read-only para observação segura. Segurança por design --- frames sealed client-side garantem que dados sensíveis nunca saiam da sua máquina. E simplicidade de uso --- um comando, um QR code, um link.

O `/collab` fecha o ciclo de colaboração que começou com o advisor model. Enquanto o advisor é um revisor autônomo que trabalha nos bastidores, o collab traz um ser humano real para a equação --- com opinião, julgamento e a capacidade de dizer "para, isso vai dar problema".

No próximo capítulo, vamos além do código: browser e desktop automation.

Acesse a documentação completa: https:/\/omp.sh/docs

Siga-nous nas redes sociais para dicas, tutoriais e novidades sobre o Oh My Pi.

#horizontalrule

= Browser e Desktop: Além do Código
<browser-e-desktop-além-do-código>
== O estaleiro se estende ao oceano digital
<o-estaleiro-se-estende-ao-oceano-digital>
Até agora, você aprendeu a comandar o estaleiro de dentro do terminal --- editando arquivos, rodando comandos, depurando binários e colaborando com teammates em tempo real.

Mas e se o navio precisasse sair do estaleiro? E se, em vez de construir o casco, você precisasse navegar pelos mares --- interagir com portos (websites), inspecionar cargas (dados de páginas) e pilotar o convés (desktop) inteiro a partir de uma ponte de comando unificada?

É exatamente isso que o OMP oferece com suas ferramentas `browser` e `computer`.

== A Browser Tool: Navegando pelos Portos Digitais
<a-browser-tool-navegando-pelos-portos-digitais>
A ferramenta `browser` do OMP é muito mais que um simples automatizador de web. Ela combina três modos de operação que a tornam flexível para diferentes cenários.

#strong[Puppeteer tabs sobre Chromium headless:] o OMP lança um navegador invisível que navega, clica, preenche formulários e extrai dados sem que você veja nada acontecer. É como um navio autônomo que navega pelos portos sozinho, coletando amostras de carga.

#strong[CDP-attached apps:] o Protocolo de Depuração do Chrome permite que o OMP se conecte a qualquer aplicação Electron --- Slack, VS Code, Discord, Teams --- e leia/interaja com ela como se fosse uma página web. Aponte o browser tool para o Slack e o agente lê suas DMs da mesma forma que lê a web.

#strong[Browser relay extension:] o modo mais poderoso. Em vez de lançar um novo navegador, o OMP se conecta às tabs que você já tem abertas no Chrome, sem roubar foco. O agente pode navegar, clicar e extrair dados das suas páginas reais --- como um copiloto que assume temporariamente a rota do navio enquanto você observa.

== Stealth Mode: Navegando Sem Ser Detectado
<stealth-mode-navegando-sem-ser-detectado>
A maioria dos sites detecta automações de browser e bloqueia o acesso. O OMP resolve isso com o Stealth mode ativado por padrão. Ao contrário de headless browsers tradicionais que são identificáveis por headers como `navigator.webdriver`, o Stealth mode faz o agente parecer um usuário humano comum --- com viewport real, user-agent legítimo e comportamento de navegação natural.

Isso significa que o agente pode acessar sites que bloqueiam bots, realizar scraping sem ser bloqueado, e testar interfaces de usuário como um humano faria.

== Computer Tool: As Mãos no Desktop
<computer-tool-as-mãos-no-desktop>
Enquanto o browser tool trabalha na web, o `computer` tool trabalha no desktop real do seu sistema operacional. Ele executa JavaScript persistente contra o host e oferece acesso a:

#strong[Janelas e displays:] enumerar todas as janelas abertas, seus títulos, posições e tamanhos. É como ter um radar que mostra todos os navios no porto.

#strong[Screenshots:] capturar a tela inteira ou regiões específicas para análise visual.

#strong[Input nativo:] enviar cliques, teclas e movimentos de mouse diretamente no sistema operacional --- não em um navegador, mas no desktop real.

#strong[AX tree (Árvore de Acessibilidade):] a ferramenta mais subestimada. A AX tree é uma representação estrutural de toda a interface do usuário, incluindo botões, campos de texto, menus e elementos gráficos --- tudo acessível programaticamente. É como ter um mapa de todas as âncoras, cabos e equipamentos do navio, organizados por função.

#strong[Clipboard:] ler e escrever na área de transferência do sistema.

== A Diferença entre Browser e Computer
<a-diferença-entre-browser-e-computer>
#figure(
  align(center)[#table(
    columns: 3,
    align: (auto,auto,auto,),
    table.header([Aspecto], [Browser Tool], [Computer Tool],),
    table.hline(),
    [Escopo], [Web (páginas, apps Electron)], [Desktop inteiro],
    [Protocolo], [Puppeteer / CDP], [JS persistente + APIs do OS],
    [Stealth], [Sim (por padrão)], [Não aplicável],
    [AX Tree], [DOM (árvore de acessibilidade web)], [AX Tree nativo do OS],
    [Input], [Cliques/teclas no DOM], [Cliques/teclas no desktop],
    [Uso típico], [Scraping, testing web], [Automação de apps desktop],
  )]
  , kind: table
  )

== Configurando a Browser Tool
<configurando-a-browser-tool>
Para usar a browser tool, basta habilitá-la na configuração do OMP. O Stealth mode já vem ativado por padrão.

```yaml
# ~/.omp/agent/config.yml
tools:
  enabled:
    - read
    - write
    - edit
    - bash
    - browser
    - computer
```

== Relay Extension: Controlando Tabs Existentes
<relay-extension-controlando-tabs-existentes>
A extensão de relay é o modo mais poderoso. Em vez de lançar um novo navegador, ela se conecta ao Chrome que você já está usando.

Primeiro, instale a extensão "OMP Browser Relay" do Chrome Web Store. Depois, clique no ícone da extensão para ativar o relay. No OMP, use o browser tool normalmente --- ele detectará as tabs abertas.

O relay permite que o agente leia o conteúdo de tabs que você já tem abertas, navegue entre elas, clique e interaja sem roubar foco, e extraia dados de páginas reais.

== Computer Tool: Controle do Desktop
<computer-tool-controle-do-desktop>
O computer tool oferece acesso direto ao sistema operacional.

```bash
# Exemplos de comandos do computer tool:

# Listar todas as janelas abertas
# computer windows

# Capturar screenshot da tela inteira
# computer screenshot

# Enviar tecla para o sistema
# computer key "ctrl+c"

# Enviar texto para o campo focado
# computer type "Olá, mundo!"

# Mover o mouse para coordenadas
# computer move 500 300

# Clicar nas coordenadas atuais
# computer click
```

== AX Tree: Navegação por Acessibilidade
<ax-tree-navegação-por-acessibilidade>
A AX tree é a forma mais confiável de interagir com interfaces complexas.

```bash
# Obter a árvore de acessibilidade completa
# computer ax-tree

# Buscar um elemento por role
# computer ax-tree --role button

# Buscar por nome
# computer ax-tree --name "Submit"

# Interagir com um elemento da AX tree
# computer ax-interact --ref "button-submit" --action click
```

== Caso de uso: monitoramento de preços
<caso-de-uso-monitoramento-de-preços>
Imagine que você precisa monitorar preços de um produto em múltiplos sites. Com o browser tool e Stealth mode, o agente navega para cada site de e-commerce, extrai preços, disponibilidade e avaliações, salva os dados em formato estruturado, e repete diariamente sem ser bloqueado.

Sem Stealth mode, a maioria dos sites bloquearia o acesso após algumas requisições. Com Stealth, o agente se comporta como um usuário humano comum.

== Caso de uso: testing visual de UI
<caso-de-uso-testing-visual-de-ui>
Ao desenvolver uma interface web, você pode usar o browser tool para navegar para a página em desenvolvimento, tirar screenshots de cada estado, comparar com o design esperado e reportar diferenças visuais.

Isso é especialmente útil para detectar regressões visuais que testes unitários não pegam.

== Caso de uso: automação de desktop para DevOps
<caso-de-uso-automação-de-desktop-para-devops>
Um administrador de sistemas pode usar o computer tool para verificar janelas abertas em servidores remotos, executar ações em aplicações GUI que não têm CLI, capturar screenshots para documentação, e automatizar configurações em interfaces gráficas legadas.

== Caso de uso: pesquisa web assistida por IA
<caso-de-uso-pesquisa-web-assistida-por-ia>
Combine browser tool com o LLM para pesquisa avançada. O agente navega para fontes acadêmicas, extrai abstracts e dados-chave, o LLM analisa e sintetiza as informações, e gera um relatório estruturado com citações.

O browser tool cuida da navegação; o LLM cuida da análise. É como ter um navegador que não apenas acessa páginas, mas também entende o que encontra.

== Erros comuns ao usar browser e computer
<erros-comuns-ao-usar-browser-e-computer>
#strong[Esquecer o Stealth mode.] Sites modernos detectam headless browsers. O Stealth mode do OMP resolve isso por padrão, mas verifique se está habilitado.

#strong[Usar computer quando browser basta.] Se a interação é apenas com web, use browser tool. Computer é para desktop real.

#strong[Não usar AX tree.] Navegar por screenshots é lento e frágil. AX tree é mais confiável e rápido.

#strong[Ignorar permissões.] Browser e computer têm acesso sensível. Use sandboxing adequado em ambientes de produção.

== Próximos Passos
<próximos-passos-1>
Neste capítulo, você descobriu que o estaleiro do OMP não para na beira do cais --- ele se estende por toda a superfície do oceano digital.

Browser tool oferece três modos de operação --- Puppeteer headless, CDP-attached apps e relay extension --- com Stealth mode ativado por padrão para navegar sem ser detectado.

Computer tool controla o desktop real: janelas, screenshots, input nativo, AX tree e clipboard. A AX tree é o mapa de acessibilidade que permite ao agente navegar por qualquer interface sem conhecer sua estrutura visual.

Casos de uso combinados --- de scraping com stealth a testing visual, de automação de desktop a pesquisa web assistida por IA --- mostram que o OMP transforma o terminal em uma ponte de comando completa para o mundo digital.

No próximo capítulo, você vai mergulhar na configuração avançada do OMP: 60+ providers de LLM, roteamento inteligente por role e fallback chains.

Acesse a documentação completa: https:/\/omp.sh/docs

Siga-nous nas redes sociais para dicas, tutoriais e novidades sobre o Oh My Pi.

#horizontalrule

// ── CONTRACAPA ────────────────────────────────────────────────────
#pagebreak()
