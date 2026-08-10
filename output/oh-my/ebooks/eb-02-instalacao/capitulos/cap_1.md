# Instalação e Primeiros Passos

## O estaleiro está pronto — só falta ligar o motor

No capítulo anterior, você mergulhou na arquitetura do OMP — as 80.000 linhas de Rust, o pi-shell, os pi-natives, o pi-ast e os demais componentes que formam o esqueleto do harness.

Agora é hora de deixar a teoria de lado e colocar as mãos no casco. Como Mestre de Estaleiro Digital, você precisa primeiro instalar os equipamentos antes de zarpar.

## Por que quatro métodos de instalação?

O OMP é distribuído como binário compilado em Rust, o que significa que não depende de runtime como Node.js ou Python para funcionar. Cada método de instalação é apenas uma via diferente de entregar o mesmo binário no seu sistema.

**curl** — o método universal para Linux e macOS. Baixa o binário direto do GitHub Releases e coloca no seu PATH.

**Homebrew** — para quem já gerencia pacotes no macOS (ou Linux via Homebrew). Uma única linha, atualizações automáticas.

**Bun** — o gerenciador de pacotes do Bun permite instalar o OMP como complemento do ecossistema JavaScript.

**PowerShell** — o caminho nativo do Windows, sem necessidade de WSL. O OMP é nativo em Windows desde o início.

A escolha depende do seu ambiente. Se você já usa Homebrew, é a opção mais natural. Se está no Windows, o PowerShell evita a complexidade do WSL. Se quer o controle total, o curl entrega o binário sem intermediários.

## O que acontece depois de instalar?

Com o binário no sistema, o próximo passo é o `omp setup` — um assistente interativo que pergunta qual provider de LLM você quer usar, solicita a API key e grava os arquivos de configuração em `~/.omp/agent/`.

Esses dois arquivos — `config.yml` e `models.yml` — são o mapa de navegação do seu OMP: neles ficam definidos quais modelos estão disponíveis, quais ferramentas estão habilitadas e como o agente deve se comportar.

## A primeira sessão

Ao digitar `omp` no terminal, o TUI do OMP inicia e entra em modo idle — aguardando seu comando. Quando você envia um prompt, o agente interpreta a intenção, seleciona as ferramentas necessárias e começa a trabalhar.

Cada ação é visível no terminal: o agente lê arquivos, executa comandos, busca padrões — tudo de forma transparente.

## Instalação no Linux e macOS via curl

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

## Instalação no macOS via Homebrew

Para quem já gerencia pacotes com Homebrew, esta é a via mais elegante. O Homebrew cuida de atualizações automaticamente.

```bash
# macOS com Homebrew
brew tap can1357/tap
brew install oh-my-pi

# Verificar
omp --version
```

## Instalação via Bun

Se você já tem o Bun instalado (versão >= 1.3.14), pode instalar o OMP diretamente.

```bash
# Via Bun (requer Bun >= 1.3.14)
bun install -g oh-my-pi

# Verificar
omp --version
```

## Instalação no Windows via PowerShell

O OMP é nativo em Windows — não precisa de WSL. O PowerShell baixa e instala o binário automaticamente.

```powershell
# Windows (PowerShell)
powershell -c "iwr -useb omp.sh/install.ps1 | iex"

# Verificar
omp --version
```

## Configuração inicial com omp setup

Com o binário instalado, o assistente de configuração guia cada etapa.

```bash
# Iniciar o assistente de configuração
omp setup
```

O assistente pergunta:

**Qual provider usar?** — Anthropic (Claude), OpenAI (GPT), Google (Gemini), ou qualquer um dos 60+ providers suportados.

**Qual a API key?** — Chave de acesso do provider selecionado.

**Qual modelo padrão?** — Claude Sonnet 4, GPT-4o, Gemini 2.5 Pro, etc.

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

## Verificando a saúde do sistema

Antes de começar a trabalhar, verifique se tudo está funcionando.

```bash
# Diagnóstico completo
omp --doctor

# Listar providers configurados
omp --providers

# Listar modelos disponíveis
omp --models
```

## Primeira sessão interativa

Agora sim — o estaleiro está pronto. Inicie sua primeira sessão.

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

## O erro mais comum na instalação

Você instalou o OMP, configurou o Anthropic como provider e inaugurou sua primeira sessão. Tudo parece funcionar — até que o agente tenta ler um arquivo e retorna um erro de permissão.

Quando o OMP foi instalado via curl, o binário ficou no diretório `~/.local/bin/`, mas os arquivos de configuração foram gravados em `~/.omp/agent/`. Se o seu projeto está em um diretório com permissões restritivas, o agente pode falhar ao acessar arquivos.

A correção é simples — conceda permissão de leitura ao diretório do projeto.

```bash
# Conceder permissão ao diretório do projeto
chmod -R o+rX /caminho/para/seu/projeto
```

Outra armadilha comum: instalar o OMP mas esquecer de configurar a API key. O `omp setup` pode ser reexecutado a qualquer momento.

```bash
# Reconfigurar o provider
omp setup
```

A seção de configuração aceita múltiplos providers simultaneamente — você pode ter Anthropic para tarefas pesadas e OpenAI para tarefas leves, trocando com `/model` durante a sessão.

## Próximos Passos

Você completou três etapas fundamentais: instalou o OMP em qualquer plataforma, configurou o primeiro provider com `omp setup` e conduziu sua primeira sessão interativa.

O OMP nasce pronto para operar — mas a verdadeira potência emerge quando você domina a interface de comando. No próximo capítulo, você mergulhará no TUI: os cards, os atalhos de teclado, os modos de operação e tudo o que separa um usuário casual de um Mestre de Estaleiro que navega com precisão.

Acesse a documentação completa: https://omp.sh/docs

Siga-nous nas redes sociais para dicas, tutoriais e novidades sobre o Oh My Pi.
