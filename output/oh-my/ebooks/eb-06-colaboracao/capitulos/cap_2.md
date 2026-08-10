# Browser e Desktop: Além do Código

## O estaleiro se estende ao oceano digital

Até agora, você aprendeu a comandar o estaleiro de dentro do terminal — editando arquivos, rodando comandos, depurando binários e colaborando com teammates em tempo real.

Mas e se o navio precisasse sair do estaleiro? E se, em vez de construir o casco, você precisasse navegar pelos mares — interagir com portos (websites), inspecionar cargas (dados de páginas) e pilotar o convés (desktop) inteiro a partir de uma ponte de comando unificada?

É exatamente isso que o OMP oferece com suas ferramentas `browser` e `computer`.

## A Browser Tool: Navegando pelos Portos Digitais

A ferramenta `browser` do OMP é muito mais que um simples automatizador de web. Ela combina três modos de operação que a tornam flexível para diferentes cenários.

**Puppeteer tabs sobre Chromium headless:** o OMP lança um navegador invisível que navega, clica, preenche formulários e extrai dados sem que você veja nada acontecer. É como um navio autônomo que navega pelos portos sozinho, coletando amostras de carga.

**CDP-attached apps:** o Protocolo de Depuração do Chrome permite que o OMP se conecte a qualquer aplicação Electron — Slack, VS Code, Discord, Teams — e leia/interaja com ela como se fosse uma página web. Aponte o browser tool para o Slack e o agente lê suas DMs da mesma forma que lê a web.

**Browser relay extension:** o modo mais poderoso. Em vez de lançar um novo navegador, o OMP se conecta às tabs que você já tem abertas no Chrome, sem roubar foco. O agente pode navegar, clicar e extrair dados das suas páginas reais — como um copiloto que assume temporariamente a rota do navio enquanto você observa.

## Stealth Mode: Navegando Sem Ser Detectado

A maioria dos sites detecta automações de browser e bloqueia o acesso. O OMP resolve isso com o Stealth mode ativado por padrão. Ao contrário de headless browsers tradicionais que são identificáveis por headers como `navigator.webdriver`, o Stealth mode faz o agente parecer um usuário humano comum — com viewport real, user-agent legítimo e comportamento de navegação natural.

Isso significa que o agente pode acessar sites que bloqueiam bots, realizar scraping sem ser bloqueado, e testar interfaces de usuário como um humano faria.

## Computer Tool: As Mãos no Desktop

Enquanto o browser tool trabalha na web, o `computer` tool trabalha no desktop real do seu sistema operacional. Ele executa JavaScript persistente contra o host e oferece acesso a:

**Janelas e displays:** enumerar todas as janelas abertas, seus títulos, posições e tamanhos. É como ter um radar que mostra todos os navios no porto.

**Screenshots:** capturar a tela inteira ou regiões específicas para análise visual.

**Input nativo:** enviar cliques, teclas e movimentos de mouse diretamente no sistema operacional — não em um navegador, mas no desktop real.

**AX tree (Árvore de Acessibilidade):** a ferramenta mais subestimada. A AX tree é uma representação estrutural de toda a interface do usuário, incluindo botões, campos de texto, menus e elementos gráficos — tudo acessível programaticamente. É como ter um mapa de todas as âncoras, cabos e equipamentos do navio, organizados por função.

**Clipboard:** ler e escrever na área de transferência do sistema.

## A Diferença entre Browser e Computer

| Aspecto | Browser Tool | Computer Tool |
|---------|-------------|---------------|
| Escopo | Web (páginas, apps Electron) | Desktop inteiro |
| Protocolo | Puppeteer / CDP | JS persistente + APIs do OS |
| Stealth | Sim (por padrão) | Não aplicável |
| AX Tree | DOM (árvore de acessibilidade web) | AX Tree nativo do OS |
| Input | Cliques/teclas no DOM | Cliques/teclas no desktop |
| Uso típico | Scraping, testing web | Automação de apps desktop |

## Configurando a Browser Tool

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

## Relay Extension: Controlando Tabs Existentes

A extensão de relay é o modo mais poderoso. Em vez de lançar um novo navegador, ela se conecta ao Chrome que você já está usando.

Primeiro, instale a extensão "OMP Browser Relay" do Chrome Web Store. Depois, clique no ícone da extensão para ativar o relay. No OMP, use o browser tool normalmente — ele detectará as tabs abertas.

O relay permite que o agente leia o conteúdo de tabs que você já tem abertas, navegue entre elas, clique e interaja sem roubar foco, e extraia dados de páginas reais.

## Computer Tool: Controle do Desktop

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

## AX Tree: Navegação por Acessibilidade

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

## Caso de uso: monitoramento de preços

Imagine que você precisa monitorar preços de um produto em múltiplos sites. Com o browser tool e Stealth mode, o agente navega para cada site de e-commerce, extrai preços, disponibilidade e avaliações, salva os dados em formato estruturado, e repete diariamente sem ser bloqueado.

Sem Stealth mode, a maioria dos sites bloquearia o acesso após algumas requisições. Com Stealth, o agente se comporta como um usuário humano comum.

## Caso de uso: testing visual de UI

Ao desenvolver uma interface web, você pode usar o browser tool para navegar para a página em desenvolvimento, tirar screenshots de cada estado, comparar com o design esperado e reportar diferenças visuais.

Isso é especialmente útil para detectar regressões visuais que testes unitários não pegam.

## Caso de uso: automação de desktop para DevOps

Um administrador de sistemas pode usar o computer tool para verificar janelas abertas em servidores remotos, executar ações em aplicações GUI que não têm CLI, capturar screenshots para documentação, e automatizar configurações em interfaces gráficas legadas.

## Caso de uso: pesquisa web assistida por IA

Combine browser tool com o LLM para pesquisa avançada. O agente navega para fontes acadêmicas, extrai abstracts e dados-chave, o LLM analisa e sintetiza as informações, e gera um relatório estruturado com citações.

O browser tool cuida da navegação; o LLM cuida da análise. É como ter um navegador que não apenas acessa páginas, mas também entende o que encontra.

## Erros comuns ao usar browser e computer

**Esquecer o Stealth mode.** Sites modernos detectam headless browsers. O Stealth mode do OMP resolve isso por padrão, mas verifique se está habilitado.

**Usar computer quando browser basta.** Se a interação é apenas com web, use browser tool. Computer é para desktop real.

**Não usar AX tree.** Navegar por screenshots é lento e frágil. AX tree é mais confiável e rápido.

**Ignorar permissões.** Browser e computer têm acesso sensível. Use sandboxing adequado em ambientes de produção.

## Próximos Passos

Neste capítulo, você descobriu que o estaleiro do OMP não para na beira do cais — ele se estende por toda a superfície do oceano digital.

Browser tool oferece três modos de operação — Puppeteer headless, CDP-attached apps e relay extension — com Stealth mode ativado por padrão para navegar sem ser detectado.

Computer tool controla o desktop real: janelas, screenshots, input nativo, AX tree e clipboard. A AX tree é o mapa de acessibilidade que permite ao agente navegar por qualquer interface sem conhecer sua estrutura visual.

Casos de uso combinados — de scraping com stealth a testing visual, de automação de desktop a pesquisa web assistida por IA — mostram que o OMP transforma o terminal em uma ponte de comando completa para o mundo digital.

No próximo capítulo, você vai mergulhar na configuração avançada do OMP: 60+ providers de LLM, roteamento inteligente por role e fallback chains.

Acesse a documentação completa: https://omp.sh/docs

Siga-nous nas redes sociais para dicas, tutoriais e novidades sobre o Oh My Pi.
