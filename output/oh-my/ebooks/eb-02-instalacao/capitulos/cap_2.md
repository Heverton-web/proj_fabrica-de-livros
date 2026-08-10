# O TUI: Sua Interface de Comando

## A ponte de comando do navio

No capítulo anterior, você completou a instalação do OMP e rodou sua primeira sessão. Agora é hora de dominar a interface que será seu centro de comando permanente — o TUI (Terminal User Interface).

Assim como um mestre de estaleiro precisa conhecer cada alavanca, cada mostrador e cada instrumento do painel de controle do navio antes de zarpar, você precisa entender a fundo os componentes visuais, os atalhos e os modos de operação do OMP.

Essa familiaridade é o que separa quem apenas usa o agente de quem realmente o comanda.

## Componentes visuais do TUI

O TUI do OMP é a camada visual que traduz o que o agente de IA está pensando e fazendo em uma linguagem que o desenvolvedor pode acompanhar, auditar e controlar.

Diferente de interfaces de chat genéricas onde o texto flui sem estrutura, o OMP organiza cada ação em componentes visuais discretos — **cards** — que se acumulam formando um histórico navegable da sessão.

### Cards

No topo e ao longo do scroll, os cards representam cada interação: prompts do usuário, respostas do modelo, chamadas de ferramentas com seus resultados, edições propostas com preview, e erros. Cada card tem um ícone que identifica seu tipo — um lápis para edições, um terminal para bash, um olho para leituras.

Isso permite que você escaneie visualmente a história da sessão sem ler cada linha.

### Footer

Na parte inferior, o footer exibe informações em tempo real sobre a sessão: o modelo ativo, o papel (role) que ele está desempenhando, o custo acumulado da sessão e a contagem de tokens.

É ali que você vê, por exemplo, se o agente está usando o modelo `default` ou se ele mudou para `smol` durante um fan-out de subagentes.

### Status Bar

A status bar — a linha mais abaixo da tela — mostra o estado do agente: se está processando uma requisição, se está aguardando input, ou se há uma operação em background rodando.

Quando o agente trava ou leva tempo para responder, essa barra é seu primeiro indicador de diagnóstico.

## Os cards em detalhe

Cada card de ferramenta segue um padrão consistente.

Quando o agente lê um arquivo, aparece um card com o caminho do arquivo e um resumo do conteúdo — não o conteúdo bruto, que poderia inundar a tela.

Quando ele faz uma edição, o card mostra um diff: o que vai sair (em vermelho) e o que vai entrar (em verde), com o número de linhas afetadas.

Para ferramentas de busca como `grep` e `ast_grep`, os resultados aparecem com numeração de linha e trechos destacados.

O mais importante: edições nunca são aplicadas silenciosamente. O agente propõe a mudança, o TUI exibe o preview, e só então a edição é gravada. Essa separação entre proposta e execução é um dos diferenciais de segurança do OMP — você sempre vê o que vai acontecer antes de acontecer.

## O sistema de ask

Quando o agente encontra uma ambiguidade — por exemplo, múltiplos arquivos que correspondem a um padrão, ou uma decisão que depende de preferência sua — ele invoca a ferramenta `ask`.

Essa ferramenta renderiza um **option picker** na tela: uma lista de escolhas com navegação por setas, uma opção marcada como "(Recommended)" quando aplicável, e um footer que explica os atalhos: "up/down navigate · enter select · esc cancel".

Esse mecanismo é o que torna o modo interativo do OMP genuinamente interativo. Em vez de o agente adivinhar sua intenção e seguir em frente, ele para, mostra as opções, e espera sua decisão.

É a diferença entre um passageiro e um piloto.

## Atalhos de teclado essenciais

O TUI do OMP responde a uma série de atalhos que aceleram a navegação e o controle da sessão.

| Atalho | Função |
|--------|--------|
| `Ctrl+P` | Cicla entre os modelos configurados para o papel ativo |
| `Alt+A` | Abre o Agent Hub para monitorar subagentes |
| `Ctrl+C` | Cancela a geração atual do modelo |
| `Ctrl+L` | Limpa a tela mantendo o histórico |
| `Tab` | Aceita a opção sugerida no option picker |
| `Esc` | Cancela o picker ou fecha um card expandido |

O `Ctrl+P` é particularmente útil quando você quer testar rapidamente como um mesmo prompt se comporta com modelos diferentes. Ao pressioná-lo, o footer atualiza imediatamente mostrando o novo modelo selecionado.

## Comandos slash

Além dos atalhos de teclado, o OMP expõe comandos slash que modificam o comportamento da sessão. Eles são digitados diretamente no prompt.

**`/model`** — Abre o seletor de modelo para trocar o modelo ativo no meio da sessão. Você pode escolher entre dezenas de providers configurados.

**`/vibe`** — Entra no modo Vibe, onde o agente atua como um diretor que comanda workers persistentes com ferramentas de leitura apenas. Útil para sessões onde você quer que o agente planeje antes de executar.

**`/fresh`** — Reseta o estado do stream do provider (cache de prompt obsoleto, stream travado) sem alterar o transcript local. Quando o agente parece travado ou responde com lixo, `/fresh` é o primeiro remédio.

**`/collab`** — Inicia uma sessão de colaboração ao vivo, gerando um link e um QR code para que um colega se junte. Pode ser read-write (par programming) ou read-only (observação).

**`/review`** — Dispara subagentes de code review que varrem branches, commits ou trabalho não commitado em paralelo, classificando issues de P0 a P3.

**`/advisor`** — Configura e gerencia o modelo advisor — um segundo modelo que observa cada turno do agente principal e injeta notas, concerns ou blockers.

**`/debug`** — Abre ferramentas de depuração, relatórios e profiling.

## Magic keywords

Três palavras mágicas, escritas em lowercase no meio do prompt, ativam comportamentos especializados do agente. Elas funcionam apenas em prosa — não dentro de blocos de código, identificadores ou caminhos de arquivo.

**`ultrathink`** — Solicita raciocínio cuidadoso multi-etapa e o maior esforço de thinking automático suportado pelo modelo. Use quando a tarefa exige análise profunda.

**`orchestrate`** — Executa trabalho independente substancial através de subagentes paralelos e verifica cada fase. Ative quando a tarefa pode ser decomposta em partes independentes.

**`workflowz`** — Constrói um workflow determinístico multi-subagentes com a ferramenta `task`. Para automações complexas que exigem controle preciso do fluxo.

```bash
# Exemplo: usando uma magic keyword no prompt
omp -p "ultrathink analise a arquitetura deste projeto e sugira melhorias"

# Exemplo: modo one-shot com orchestrate
omp -p "orchestrate refatore o módulo de autenticação e execute todos os testes"
```

## Os 4 modos de operação

O motor do OMP é o mesmo, mas ele pode ser acessado de quatro maneiras diferentes, cada uma otimizada para um caso de uso distinto.

### Modo 1: Interactive (TUI padrão)

Quando você digita `omp` sem argumentos, o TUI abre. É o modo mais completo: cards renderizados, edits com preview, o option picker do `ask`, footer com custos, e navegação por atalhos. É aqui que você passa a maior parte do tempo.

```bash
# Iniciar sessão interativa
omp

# Resumir sessão anterior
omp --resume
```

### Modo 2: One-shot (`omp -p`)

Para quando você quer uma resposta rápida sem abrir a interface completa. O `-p` recebe um prompt, o agente processa, imprime a resposta e encerra. Ideal para scripts, CI/CD, ou perguntas pontuais.

```bash
# Pergunta rápida e saída
omp -p "liste todos os arquivos .ts na pasta src/"

# Com modelo específico
omp -p --model anthropic/claude-sonnet-4.5 "explique este erro"
```

### Modo 3: RPC (`omp --mode rpc`)

Para quando você quer controlar o OMP de outro programa. O motor recebe comandos NDJSON via stdio e responde com frames de evento. Não há TUI — o controle é total via código.

```bash
# Iniciar em modo RPC sem sessão persistente
omp --mode rpc --no-session

# Enviar um prompt via NDJSON
> {"id":"r1","type":"prompt","message":"liste arquivos .ts"}
< {"id":"r1","type":"response", ...}
```

### Modo 4: ACP (`omp acp`)

O Agent Client Protocol é o protocolo de integração com editores. Quando o OMP roda em modo ACP, ele se comunica com o editor via JSON-RPC, e as ferramentas são roteadas pelo editor.

```bash
# Iniciar em modo ACP (geralmente acionado pelo editor)
omp acp
```

## Os 10 roles de modelo

O OMP roteia trabalho por intenção através de 10 papéis (roles) de modelo. Cada role pode apontar para um provider e modelo diferente, permitindo otimização por custo e qualidade.

| Role | Uso |
|------|-----|
| `default` | Turnos normais |
| `smol` | Fan-out barato de subagentes |
| `slow` | Raciocínio profundo |
| `plan` | Modo planejamento |
| `commit` | Geração de changelogs |
| `vision` | Análise de imagens |
| `designer` | Geração de arte |
| `task` | Coordenação de tarefas |
| `advisor` | Revisão inline |
| `tiny` | Tarefas triviais |

## O picker que captura o teclado

Imagine que você acabou de instalar o OMP e está ansioso para testá-lo. Você abre o terminal, digita `omp`, e a tela se preenche com cards coloridos, um footer com informações que não reconhece, e um prompt piscando.

Sua primeira reação é digitar algo e ver o que acontece. O agente responde, faz algumas buscas, e então para: "Encontrei 3 arquivos que correspondem ao padrão. Qual deles você quer que eu analise?" Aparece um picker com três opções.

Aqui é onde o erro mais comum acontece: você ignora o picker, tenta digitar algo no prompt, e nada acontece. O picker captura o foco do teclado — você precisa usar as setas para navegar e Enter para selecionar, ou Esc para cancelar.

É um detalhe pequeno, mas que confunde 9 em cada 10 iniciantes.

O diagnóstico é direto: o TUI do OMP funciona em modalidades. Quando o option picker está ativo, ele captura todos os inputs de teclado. A solução é simples — olhe para o footer do picker, ele sempre mostra os atalhos disponíveis.

No caso do `ask`, são "up/down navigate · enter select · esc cancel". Ao dominar essa interação, você percebe que o TUI não está te bloqueando: está te protegendo de decisões precipitadas.

## Erros comuns e suas correções

| Erro comum | Diagnóstico | Correção |
|-----------|------------|----------|
| Picker captura teclado e o usuário não consegue digitar | Modalidade ativa | Use setas + Enter, ou Esc para cancelar |
| `omp -p` não mostra opções nem pede confirmação | Modo one-shot é non-interactive | Use `omp` (TUI) para tarefas interativas |
| Agente travado, sem resposta | Stream do provider obsoleto | Digite `/fresh` para resetar o stream |
| Footer mostra modelo errado | Role diferente do esperado | Use `Ctrl+P` para ciclar ou `/model` para trocar |

## Próximos Passos

Três pontos devem ficar gravados neste capítulo.

Primeiro, o TUI do OMP é uma superfície de controle projetada para transparência: cada ação do agente aparece como um card, cada edição tem preview, e ambiguidades são resolvidas via option picker — nunca por adivinhação.

Segundo, os atalhos e comandos slash não são decoração: `Ctrl+P`, `Alt+A`, `/fresh` e `/collab` são ferramentas de produtividade que transformam a experiência de usar o agente.

Terceiro, os quatro modos de operação — interactive, one-shot, RPC e ACP — garantem que o OMP se adapte a qualquer cenário, do script de CI ao pair programming ao vivo.

O desafio que fica: abra o OMP agora, inicie uma sessão interativa, e experimente cada um dos comandos slash pelo menos uma vez. Troque de modelo com `/model`, inicie um `/collab view`, e veja como o Agent Hub (`Alt+A`) mostra os subagentes trabalhando.

Essa familiaridade prática é o que transforma um instrumento desconhecido em uma extensão da sua mão de obra.

No próximo capítulo, você mergulhará no arsenal completo de ferramentas built-in do OMP — as 31 ferramentas que compõem o equipamento do estaleiro.

Acesse a documentação completa: https://omp.sh/docs

Siga-nous nas redes sociais para dicas, tutoriais e novidades sobre o Oh My Pi. Junte-se a mais de 23.3k desenvolvedores que já estão usando o harness mais completo do mercado.
