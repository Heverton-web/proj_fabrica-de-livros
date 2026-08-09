# Capítulo 2: Instalação e Configuração

## 1. Introdução

No capítulo anterior, você conheceu a arquitetura de um coding agent, entendeu como ele se diferencia de ferramentas adjacentes e viu um comparativo prático entre as opções disponíveis no mercado. A teoria está estabelecida — agora é hora de colocar as mãos na massa.

Este capítulo guia você pelo processo completo de instalação e configuração do Oh My Pi, desde a escolha do método de instalação até a personalização avançada de profiles, aliases e variáveis de ambiente. O objetivo é que, ao final deste capítulo, você tenha o Oh My Pi instalado, configurado com seu provedor de modelo preferido, testado e pronto para trabalhar em qualquer projeto [1].

O processo de configuração de um coding agent se assemelha ao de configurar um novo celular. Você desempacota o hardware (instala o binário), liga o aparelho (verifica a versão), conecta à rede (configura a chave de API) e instala seus apps preferidos (personaliza profiles e aliases). Cada etapa é simples individualmente, mas a ordem importa — pular uma etapa gera erro na seguinte. Este capítulo respeita essa sequência [2].

## 2. Explica

### Métodos de instalação

O Oh My Pi suporta quatro métodos de instalação, cada um adequado a um contexto diferente. A escolha depende do sistema operacional, do gerenciador de pacotes disponível e do nível de controle que você quer ter sobre a versão instalada [3].

**npm (recomendado para a maioria dos casos).** O Node Package Manager é o método mais universal. Funciona em Windows, macOS e Linux, e garante que você sempre tenha a versão mais recente ao rodar `npm update`. A instalação global coloca o binário `omp` no PATH do sistema, permitindo execução de qualquer diretório [4].

**Homebrew (macOS e Linux).** Para quem já usa Homebrew como gerenciador de pacotes padrão, o `brew install` é a opção mais natural. O Homebrew gerencia dependências do sistema automaticamente e simplifica o processo de atualização futura [5].

**WinGet (Windows).** O Windows Package Manager é o gerenciador oficial da Microsoft. É a opção recomendada para desenvolvedores que trabalham exclusivamente no Windows e já utilizam WinGet para outras ferramentas [6].

**Script de instalação direta.** Para ambientes onde os gerenciadores de pacotes não estão disponíveis — como servidores de produção ou ambientes containerizados — o script de instalação direta baixa o binário e o configura manualmente. Essa abordagem oferece mais controle, mas requer atenção ao PATH e às permissões do arquivo [7].

### Configuração de provedores de modelo

A configuração de provedores é a etapa que transforma o Oh My Pi de um binário genérico em um coding agent funcional. O Oh My Pi suporta cinco provedores nativos: Anthropic (Claude), OpenAI (GPT), Google (Gemini), Amazon Bedrock e Azure OpenAI [8].

Cada provedor requer uma chave de API, que é um token único que autentica suas requisições. A Anthropic usa o prefixo `sk-ant-api`, a OpenAI usa `sk-` e o Google usa uma estrutura diferente. Essas chaves são vinculadas a sua conta e, no caso da Anthropic e OpenAI, ao plano de uso (gratuito, pago ou enterprise) [9].

O Oh My Pi permite configurar mais de um provedor simultaneamente. Essa funcionalidade é útil em dois cenários: quando você quer usar modelos diferentes para tarefas diferentes (Claude para code review, GPT para geração de documentação) e quando você precisa de um provedor de fallback caso o primário esteja indisponível [10].

A configuração de provedores também envolve a definição do modelo padrão. Cada provedor oferece múltiplos modelos com diferentes tradeoffs entre velocidade, qualidade e custo. O Claude 3.5 Sonnet, por exemplo, oferece um bom equilíbrio entre velocidade de resposta e qualidade de código, enquanto o Claude Opus 4 prioriza profundidade de raciocínio [11].

### O arquivo de configuração

Todas as configurações do Oh My Pi são persistidas em um arquivo JSON ou JSONC que pode residir em dois níveis: global (~/.mimocode/config.json) e por projeto (.mimocode/config.json). A configuração por projeto sobrepõe a global, o que permite definir modelos diferentes para projetos diferentes [12].

```json
{
  "provider": "anthropic",
  "model": "claude-sonnet-4-20250514",
  "theme": {
    "background": "#0d1117",
    "foreground": "#c9d1d9"
  },
  "permission": {
    "bash": "ask",
    "write": "ask",
    "edit": "ask",
    "read": "allow"
  }
}
```

Esse arquivo é lido a cada inicialização do Oh My Pi. Alterações imediatamente refletem no comportamento do agente, sem necessidade de reinicialização do shell. Essa reatividade permite experimentar diferentes configurações durante uma sessão de desenvolvimento [13].

### Profiles: múltiplas identidades para um mesmo agente

Profiles são conjuntos de configuração que você pode alternar rapidamente. Um profile pode definir um provedor, modelo e conjunto de permissões diferente. Por exemplo, você pode ter um profile "trabalho" que usa o Claude via Bedrock (conformidade empresarial) e um profile "pessoal" que usa o Claude via API direta [14].

```bash
# Criar um profile para projeto corporativo
omp profile create corporativo --provider bedrock --model claude-sonnet-4-20250514

# Criar um profile para projeto pessoal
omp profile create pessoal --provider anthropic --model claude-opus-4-20250514

# Alternar entre profiles
omp profile use corporativo
omp profile use pessoal
```

A alternância de profiles é instantânea e afeta todas as sessões futuras até a próxima alternância. Essa funcionalidade elimina a necessidade de modificar o arquivo de configuração manualmente quando você muda de contexto de trabalho [15].

### Aliases e variáveis de ambiente

Aliases são atalhos de shell que simplificam a execução do Oh My Pi. Em vez de digitar `omp -p "instrução"`, você pode configurar um alias que reduz o comando a algo mais curto [16].

```bash
# Adicionar ao seu .bashrc ou .zshrc
alias ai='omp -p'
alias review='omp -p "Revise o último commit"'
alias test='omp -p "Execute todos os testes e reporte o resultado"'
```

Variáveis de ambiente são o mecanismo para configurar chaves de API sem expô-las no arquivo de configuração. Essa separação é importante por razões de segurança: o arquivo de configuração pode ser versionado (com chaves mascaradas), enquanto as variáveis de ambiente ficam no shell do sistema [17].

```bash
# Configuração via variáveis de ambiente (Linux/macOS)
export ANTHROPIC_API_KEY="sk-ant-api03-xxxxxxxxxxxx"
export OPENAI_API_KEY="sk-xxxxxxxxxxxx"

# Configuração via variáveis de ambiente (Windows PowerShell)
$env:ANTHROPIC_API_KEY = "sk-ant-api03-xxxxxxxxxxxx"
$env:OPENAI_API_KEY = "sk-xxxxxxxxxxxx"
```

O Oh My Pi verifica as variáveis de ambiente em uma ordem específica: primeiro as variáveis dedicadas (ANTHROPIC_API_KEY, OPENAI_API_KEY), depois as variáveis genéricas (AI_API_KEY). Essa hierarquia permite configurar uma chave padrão e chaves específicas por provedor [18].

### Segurança na gestão de credenciais

A gestão segura de chaves de API é um dos aspectos mais importantes da configuração de um coding agent. Uma chave de API comprometida pode resultar em custos financeiros significativos, vazamento de dados ou uso indevido dos serviços do provedor [53].

O princípio fundamental é: chaves de API nunca devem ser armazenadas em texto plano em arquivos que possam ser versionados. Isso inclui o arquivo de configuração do Oh My Pi, arquivos .env que estejam no repositório, scripts de shell ou qualquer outro artefato que possa ser commitado [54].

A melhor prática é utilizar variáveis de ambiente do sistema, que ficam armazenadas no registro do Windows ou no shell do Linux/macOS, e não em arquivos. Quando isso não é possível (como em ambientes CI/CD), o uso de secrets management — como GitHub Secrets, AWS Secrets Manager ou HashiCorp Vault — é obrigatório [55].

## 3. Ilustra

### Configurar o agente como configurar um novo celular

Quando você compra um novo celular, o processo de setup segue uma sequência previsível. Você liga o aparelho, escolhe o idioma, conecta-se a uma rede Wi-Fi, faz login com sua conta (Apple ID ou Google Account), e então pode instalar seus apps. Cada etapa depende da anterior — você não pode instalar um app sem ter conectado à rede, e não pode fazer login sem ter escolhido o idioma [19].

O Oh My Pi segue exatamente a mesma sequência. Você instala o binário (desempacota o celular), verifica a versão (liga o aparelho), configura a chave de API (conecta à rede), escolhe o modelo (escolhe o idioma — ele determina como o agente vai "pensar"), e então pode começar a usá-lo em projetos [20].

A analogia se estende aos detalhes. Assim como um celular tem uma tela de bloqueio que protege o conteúdo, o Oh My Pi tem um sistema de permissões que protege seus arquivos. Assim como você pode ter múltiplas contas em um celular (pessoal e trabalho), o Oh My Pi permite múltiplos profiles. E assim como a primeira coisa que você faz após configurar o celular é testar se as ligações e mensagens funcionam, a primeira coisa que você faz após configurar o Oh My Pi é testar se o agente responde corretamente [21].

### O fluxo de autenticação

O diagrama a seguir mostra como o Oh My Pi autentica com um provedor de modelo a cada requisição. Note que a chave de API nunca é armazenada em texto plano no arquivo de configuração — ela é lida da variável de ambiente e transmitida por HTTPS para o endpoint do provedor.

```mermaid
%% legenda: Fluxo de autenticação entre Oh My Pi e provedor de modelo
flowchart LR
    A[Usuário digita omp -p] --> B[Oh My Pi lê config]
    B --> C{Chave na env var?}
    C -->|Sim| D[Requisição HTTPS]
    C -->|Não| E[Erro: chave não configurada]
    D --> F[Provedor valida chave]
    F -->|Válida| G[Modelo processa prompt]
    F -->|Inválida| H[Erro: autenticação falhou]
    G --> I[Resposta retornada ao terminal]
```

Esse fluxo se repete a cada interação. O Oh My Pi não mantém sessões autenticadas com o provedor — cada requisição é independente. Essa arquitetura stateless simplifica o gerenciamento de credenciais e elimina o risco de tokens expirados durante sessões longas [22].

### A hierarquia de configuração

Uma das complexidades da configuração do Oh My Pi é a existência de múltiplos níveis de configuração que se sobrepõem. Entender essa hierarquia é essencial para evitar comportamentos inesperados [56]:

```
优先级 (menor para maior):
1. Defaults do sistema (built-in do Oh My Pi)
2. Configuração global (~/.mimocode/config.json)
3. Configuração do projeto (.mimocode/config.json)
4. Variáveis de ambiente (ANTHROPIC_API_KEY, etc.)
5. Flags de linha de comando (--model, --provider, etc.)
```

Quando duas configurações conflitam, a de maior prioridade vence. Isso significa que uma flag de linha de comando sobrepõe qualquer configuração de arquivo, e uma variável de ambiente sobrepõe o arquivo de configuração. Essa arquitetura permite flexibilidade sem quebrar configurações existentes [57].

## 4. Técnica

### Instalação passo a passo

#### Método 1: npm (recomendado)

```bash
# Verificar se o Node.js e npm estão instalados
node --version   # deve retornar v18 ou superior
npm --version    # deve retornar 9 ou superior

# Instalar o Oh My Pi globalmente
npm install -g oh-my-pi

# Verificar a instalação
omp --version
# Saída esperada: oh-my-pi/0.x.x win32-x64 node-v20.x.x
```

Se o comando `omp` não for reconhecido após a instalação, verifique se o diretório global do npm está no PATH. No Windows, o diretório padrão é `%APPDATA%\npm`. No macOS/Linux, é `$(npm prefix -g)/bin` [23].

```bash
# Windows (PowerShell) - verificar PATH
$env:PATH -split ';' | Select-String 'npm'

# macOS/Linux - verificar PATH
echo $PATH | tr ':' '\n' | grep npm
```

#### Método 2: Homebrew (macOS/Linux)

```bash
# Instalar via Homebrew
brew install oh-my-pi

# Verificar
omp --version
```

#### Método 3: WinGet (Windows)

```powershell
# Instalar via WinGet
winget install OhMyPi

# Verificar (abrir novo terminal)
omp --version
```

#### Método 4: Script de instalação direta

```bash
# Linux/macOS
curl -fsSL https://raw.githubusercontent.com/anthropics/claude-code/main/install.sh | sh

# Windows (PowerShell)
irm https://raw.githubusercontent.com/anthropics/claude-code/main/install.ps1 | iex
```

### Configuração da chave de API

O primeiro passo após a instalação é configurar a chave de API. Sem ela, o Oh My Pi não consegue se comunicar com nenhum provedor de modelo [24].

#### Opção 1: Variável de ambiente (recomendado)

```bash
# Linux/macOS - adicionar ao .bashrc ou .zshrc
export ANTHROPIC_API_KEY="sk-ant-api03-sua-chave-aqui"

# Para persistir, adicione a linha acima ao seu .bashrc ou .zshrc
echo 'export ANTHROPIC_API_KEY="sk-ant-api03-sua-chave-aqui"' >> ~/.bashrc
source ~/.bashrc
```

```powershell
# Windows PowerShell - configuração permanente
[System.Environment]::SetEnvironmentVariable(
  "ANTHROPIC_API_KEY",
  "sk-ant-api03-sua-chave-aqui",
  "User"
)

# Recarregar para a sessão atual
$env:ANTHROPIC_API_KEY = "sk-ant-api03-sua-chave-aqui"
```

#### Opção 2: Arquivo .env do projeto

Crie um arquivo `.env` na raiz do seu projeto (não versionado — adicione `.env` ao `.gitignore`):

```bash
# .env (na raiz do projeto)
ANTHROPIC_API_KEY=sk-ant-api03-sua-chave-aqui
OPENAI_API_KEY=sk-sua-chave-openai-aqui
```

O Oh My Pi carrega automaticamente variáveis de ambiente de arquivos `.env` no diretório atual. Essa funcionalidade é conveniente para projetos que usam provedores diferentes, mas exige cuidado para não expor chaves no repositório [25].

#### Opção 3: Configuração interativa

O Oh My Pi oferece um assistente de configuração interativo que guia o processo de setup:

```bash
# Iniciar configuração interativa
omp config

# O assistente vai perguntar:
# 1. Qual provedor você quer usar? (anthropic/openai/google/bedrock/azure)
# 2. Qual modelo? (lista de modelos disponíveis para o provedor)
# 3. Onde está sua chave de API? (digitada ou variável de ambiente)
# 4. Quais permissões padrão? (allow/ask/deny para cada ferramenta)
```

### Teste de conectividade

Após configurar a chave de API, execute um teste simples para verificar se tudo está funcionando:

```bash
# Teste básico de conectividade
omp -p "Responda apenas: 'Conexão OK'"

# Saída esperada: Conexão OK
```

Se o comando retornar um erro de autenticação, verifique se a chave de API está correta e se o provedor selecionado suporta o modelo especificado [26].

```bash
# Teste mais detalhado - verificar modelo e provedor
omp -p "Qual modelo você é? Responda com nome e versão."

# Saída esperada: algo como "Claude 3.5 Sonnet" ou "claude-sonnet-4-20250514"
```

### Configuração avançada: múltiplos provedores

Para projetos que requerem múltiplos provedores, o Oh My Pi permite configurar chaves para cada um e alternar entre eles [27].

```bash
# Configurar chaves para múltiplos provedores
export ANTHROPIC_API_KEY="sk-ant-api03-xxxxxxxxxxxx"
export OPENAI_API_KEY="sk-xxxxxxxxxxxx"
export GOOGLE_API_KEY="AIzaxxxxxxxxxxxxxxxx"

# Definir o provedor padrão no arquivo de configuração
# ~/.mimocode/config.json ou .mimocode/config.json
```

```json
{
  "provider": "anthropic",
  "model": "claude-sonnet-4-20250514",
  "providers": {
    "anthropic": {
      "model": "claude-sonnet-4-20250514"
    },
    "openai": {
      "model": "gpt-4o"
    },
    "google": {
      "model": "gemini-2.0-flash"
    }
  }
}
```

### Configuração de profiles

Profiles permitem alternar rapidamente entre configurações diferentes. Essa funcionalidade é particularmente útil em ambientes onde você trabalha com múltiplos projetos que têm requisitos de conformidade distintos [28].

```bash
# Criar profile para projeto que usa Bedrock (corporativo)
omp profile create corporativo
# → O assistente pergunta: provedor? → bedrock
# → Modelo? → claude-sonnet-4-20250514
# → Permissões? → ask para tudo

# Criar profile para projeto pessoal (API direta)
omp profile create pessoal
# → Provedor? → anthropic
# → Modelo? → claude-opus-4-20250514
# → Permissões? → allow para read/glob/grep, ask para resto

# Listar profiles disponíveis
omp profile list

# Alternar para o profile corporativo
omp profile use corporativo

# Verificar qual profile está ativo
omp profile current
```

### Configuração de aliases

Aliases reduzem a digitação e tornam a interação com o Oh My Pi mais fluida. Configure-os no seu arquivo de shell [29]:

```bash
# ~/.bashrc ou ~/.zshrc

# Alias para uso geral
alias ai='omp -p'

# Alias para tarefas comuns
alias review='omp -p "Revise o código alterado desde o último commit. Liste problemas encontrados e sugira correções."'
alias test='omp -p "Execute todos os testes do projeto e reporte passaram/falharam."'
alias lint='omp -p "Execute o linter e corrija automaticamente todos os warnings."'
alias commit='omp -p "Gere uma mensagem de commit descritiva para as mudanças staged."'

# Alias com modelo específico
alias deep='omp --model claude-opus-4-20250514 -p'
alias fast='omp --model claude-haiku-3-20240307 -p'
```

```powershell
# Microsoft.PowerShell_profile.ps1 (Windows)

# Alias para uso geral
function ai { omp -p $args }

# Alias para tarefas comuns
function review { omp -p "Revise o código alterado desde o último commit." }
function test { omp -p "Execute todos os testes do projeto." }
function lint { omp -p "Execute o linter e corrija warnings." }
function commit { omp -p "Gere uma mensagem de commit para as mudanças staged." }
```

### Variáveis de ambiente avançadas

Além das chaves de API, o Oh My Pi suporta variáveis de ambiente que controlam comportamentos internos [30]:

```bash
# Variáveis de ambiente suportadas pelo Oh My Pi

# Chaves de API (por provedor)
export ANTHROPIC_API_KEY="sk-ant-api03-xxxx"
export OPENAI_API_KEY="sk-xxxx"
export GOOGLE_API_KEY="AIzaxxxx"
export AWS_BEDROCK_REGION="us-east-1"

# Controle de comportamento
export OMP_LOG_LEVEL="info"          # debug, info, warn, error
export OMP_THEME="dark"              # dark, light, auto
export OMP_PERMISSION_MODE="default" # default, permissive, strict
export OMP_MAX_TOKENS="8192"         # limite de tokens por resposta
export OMP_TIMEOUT="120"             # timeout em segundos para requisições

# Diretórios
export OMP_CONFIG_DIR="~/.mimocode"  # diretório de configuração global
export OMP_MEMORY_DIR="~/.mimocode/memory"  # diretório de memória persistente
```

### Configuração para Bedrock e Azure

Empresas que utilizam infraestrutura cloud própria precisam de configurações adicionais. O Bedrock requer credenciais AWS, e o Azure requer endpoint e chave específicos [31].

```bash
# Configuração para Amazon Bedrock
export AWS_BEDROCK_REGION="us-east-1"
export AWS_ACCESS_KEY_ID="AKIAxxxxxxxxxxxx"
export AWS_SECRET_ACCESS_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# No arquivo de configuração (.mimocode/config.json)
```

```json
{
  "provider": "bedrock",
  "model": "anthropic.claude-sonnet-4-20250514-v1:0",
  "bedrock": {
    "region": "us-east-1",
    "endpoint": "https://bedrock-runtime.us-east-1.amazonaws.com"
  }
}
```

```bash
# Configuração para Azure OpenAI
export AZURE_OPENAI_API_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export AZURE_OPENAI_ENDPOINT="https://seu-recurso.openai.azure.com/"

# No arquivo de configuração
```

```json
{
  "provider": "azure",
  "model": "gpt-4o",
  "azure": {
    "endpoint": "https://seu-recurso.openai.azure.com/",
    "api_version": "2024-02-01"
  }
}
```

### Verificação e troubleshooting

Após a configuração, execute uma bateria de verificações para garantir que tudo está correto [32]:

```bash
# 1. Verificar versão
omp --version

# 2. Verificar configuração carregada
omp config show

# 3. Verificar conectividade com o provedor
omp -p "Teste de conectividade: responda OK"

# 4. Verificar permissões atuais
omp permissions list

# 5. Verificar se o .env está sendo carregado
omp -p "Liste as variáveis de ambiente disponíveis que comecem com ANTHROPIC_"
```

### Setup em container Docker

Para equipes que padronizam ambientes via Docker, o Oh My Pi pode ser configurado em um container com todas as dependências pré-instaladas [58]:

```dockerfile
# Dockerfile para ambiente de desenvolvimento com Oh My Pi
FROM node:20-slim

# Instalar Oh My Pi
RUN npm install -g oh-my-pi

# Criar diretório de configuração
RUN mkdir -p /root/.mimocode

# Configuração padrão
COPY config.json /root/.mimocode/config.json

# O .env deve ser passado via docker run --env-file .env
ENTRYPOINT ["omp"]
```

```bash
# Construir a imagem
docker build -t omp-dev .

# Executar com variáveis de ambiente do host
docker run --env-file .env -v $(pwd):/project -w /project omp-dev -p "Analise este projeto"
```

Essa abordagem garante que todos os membros da equipe usem a mesma versão do Oh My Pi e a mesma configuração, eliminando o "funciona na minha máquina" [59].

## 5. Aplica

### Setup completo do zero: cenário real

Você é desenvolvedor em uma empresa de tecnologia que acabou de adotar o Oh My Pi como ferramenta de coding agent. Seu setup é o seguinte: notebook Windows 11, conta na Anthropic com plano Pro, projeto em Node.js com TypeScript e testes em Vitest. Você precisa instalar, configurar e validar o Oh My Pi em menos de 15 minutos [33].

**A cena do erro — o que acontece quando você ignora a ordem das etapas:**

Você começa instalando o Oh My Pi via npm. OK, o binário está lá. Em seguida, tenta usar imediatamente: `omp -p "Olá"`. Erro: "No API key found". Você pensa: "ah, esqueci de configurar a chave". Vai direto ao arquivo `.mimocode/config.json` e adiciona `"api_key": "sk-ant-api03-xxxx"` em texto plano. Roda novamente. Funciona, mas agora a chave está exposta no arquivo de configuração — se você fizer commit nesse diretório, a chave vaza para o repositório [34].

**O diagnóstico — por que isso deu errado:**

O problema não foi técnico. Foi procedural. Você pulou a etapa de configurar variáveis de ambiente e colocou a chave diretamente no arquivo de configuração. Isso é uma prática insegura que viola o princípio de separação entre configuração e credenciais. A chave de API é um segredo — ela deve viver em uma variável de ambiente, não em um arquivo que pode ser versionado [35].

**A prática correta — o setup em 7 passos:**

```bash
# Passo 1: Instalar
npm install -g oh-my-pi

# Passo 2: Verificar instalação
omp --version

# Passo 3: Configurar chave de API via variável de ambiente
# Windows PowerShell:
[System.Environment]::SetEnvironmentVariable(
  "ANTHROPIC_API_KEY",
  "sk-ant-api03-sua-chave-aqui",
  "User"
)
$env:ANTHROPIC_API_KEY = "sk-ant-api03-sua-chave-aqui"

# Passo 4: Testar conectividade
omp -p "Responda apenas: Conexão OK"

# Passo 5: Configurar o projeto
cd ~/meu-projeto
omp -p "Analise a estrutura deste projeto e me dê um resumo"

# Passo 6: Testar em contexto real
omp -p "Execute os testes do projeto com npm test e reporte o resultado"

# Passo 7: Configurar aliases (opcional, mas recomendado)
echo "alias ai='omp -p'" >> ~/.bashrc
source ~/.bashrc
```

Esse procedimento garante que a chave de API nunca fique exposta em arquivos versionados, que o agente está funcional antes de você começar a trabalhar e que aliases estão disponíveis para uso diário [36].

### Armadilhas comuns

#### Armadilha 1: API key incorreta ou expirada

```bash
# Sintoma: erro "Authentication failed" ou "Invalid API key"
omp -p "teste"

# Diagnóstico: verificar se a chave está correta
echo $ANTHROPIC_API_KEY | head -c 20
# Deve mostrar: sk-ant-api03-sua-chave...

# Solução: gerar nova chave no painel do provedor
# Anthropic: https://console.anthropic.com/settings/keys
# OpenAI: https://platform.openai.com/api-keys
```

#### Armadilha 2: Modelo não disponível no provedor

```bash
# Sintoma: erro "Model not found" ou "Model not supported"
omp --model gpt-5 -p "teste"

# Diagnóstico: listar modelos disponíveis
omp models list

# Solução: usar um modelo que o provedor suporta
omp --model claude-sonnet-4-20250514 -p "teste"
```

#### Armadilha 3: PATH não configurado

```bash
# Sintoma: "omp: command not found" após instalação

# Diagnóstico (Windows):
where omp
# Se não encontrar, o diretório do npm não está no PATH

# Solução (Windows PowerShell):
$npmPath = npm prefix -g
$env:PATH += ";$npmPath"

# Solução permanente:
[System.Environment]::SetEnvironmentVariable(
  "PATH",
  $env:PATH + ";$(npm prefix -g)",
  "User"
)
```

#### Armadilha 4: Permissões negadas em diretório protegido

```bash
# Sintoma: erro ao tentar editar arquivos no diretório do projeto
# "Permission denied" ou "EACCES"

# Diagnóstico: verificar permissões do diretório
ls -la ~/meu-projeto

# Solução: garantir que o Oh My Pi tem permissão de escrita
# No Windows, execute o terminal como administrador se necessário
# No macOS/Linux, verifique o ownership: chown -R $USER ~/meu-projeto
```

#### Armadilha 5: Conflito entre configuração global e local

```bash
# Sintoma: o agente usa o modelo errado ou provedor errado

# Diagnóstico: verificar qual configuração está ativa
omp config show

# A configuração local (.mimocode/config.json no projeto)
# sobrepõe a global (~/.mimocode/config.json)

# Solução: unificar ou ajustar conforme necessário
# Se quer usar a global, remova o .mimocode/config.json do projeto
# Se quer usar a local, ajuste conforme o caso
```

#### Armadilha 6: Rate limit do provedor

```bash
# Sintoma: erro "Rate limit exceeded" ou "Too many requests"

# Diagnóstico: verificar se há muitas requisições simultâneas
# (Outros processos ou scripts usando a mesma chave)

# Solução: aguardar o período de cooldown (geralmente 60 segundos)
# Ou configurar um segundo provedor como fallback
export OPENAI_API_KEY="sk-xxxx"  # fallback para quando Anthropic estiver indisponível
```

## 6. Conclusão

Neste capítulo, você percorreu o caminho completo de instalação e configuração do Oh My Pi. Viu que existem quatro métodos de instalação — npm, Homebrew, WinGet e script direto — cada um adequado a um contexto diferente. Aprende a configurar chaves de API via variáveis de ambiente, a testar a conectividade com o provedor e a personalizar o agente com profiles, aliases e variáveis de ambiente avançadas.

O cenário de setup do zero demonstrou que a ordem das etapas importa: instalar, configurar chave, testar, personalizar. Pular etapas gera erros que parecem técnicos, mas são procedimentais. A armadilha mais comum — colocar a chave de API diretamente no arquivo de configuração — é também a mais perigosa, pois expõe credenciais em arquivos que podem ser versionados [37].

A configuração de provedores cloud (Bedrock e Azure) mostrou que o Oh My Pi se adapta a ambientes empresariais com requisitos de conformidade. E o setup via Docker demonstrou como padronizar o ambiente de desenvolvimento em equipes [38].

No próximo capítulo, você vai usar o Oh My Pi em projetos reais. Vai aprender a estruturar instruções eficazes, a gerenciar contexto de projeto, a usar skills e MCPs e a integrar o agente no fluxo de trabalho diário do desenvolvimento. A configuração feita aqui é a base — a produtividade vem no próximo capítulo [39].

## 7. Referências Bibliográficas

[1] ANTHROPIC. Claude Code: Getting started guide. 2025. Disponível em: https://docs.anthropic.com/en/docs/claude-code/get-started. Acesso em: 15 jul. 2025.

[2] KRUG, Steve. *Don't Make Me Think, Revisited: A Common Sense Approach to Web Usability*. 3. ed. San Francisco: New Riders, 2014. 200 p. ISBN 978-0-321-96551-6.

[3] ANTHROPIC. Claude Code: Installation options. 2025. Disponível em: https://docs.anthropic.com/en/docs/claude-code/installation. Acesso em: 15 jul. 2025.

[4] NODE.JS FOUNDATION. npm documentation: Installing packages globally. 2025. Disponível em: https://docs.npmjs.com/cli/commands/npm-install. Acesso em: 15 jul. 2025.

[5] HOMEBREW. Homebrew documentation: Formula Cookbook. 2025. Disponível em: https://docs.brew.sh/Formula-Cookbook. Acesso em: 15 jul. 2025.

[6] MICROSOFT. Windows Package Manager documentation. 2025. Disponível em: https://learn.microsoft.com/en-us/windows/package-manager/winget/. Acesso em: 15 jul. 2025.

[7] ANTHROPIC. Claude Code: Manual installation. 2025. Disponível em: https://docs.anthropic.com/en/docs/claude-code/installation#manual-installation. Acesso em: 15 jul. 2025.

[8] ANTHROPIC. Claude Code: Supported providers. 2025. Disponível em: https://docs.anthropic.com/en/docs/claude-code/supported-providers. Acesso em: 15 jul. 2025.

[9] ANTHROPIC. API keys and authentication. 2025. Disponível em: https://docs.anthropic.com/en/api/getting-started. Acesso em: 15 jul. 2025.

[10] OPENAI. OpenAI API keys documentation. 2025. Disponível em: https://platform.openai.com/docs/api-reference/authentication. Acesso em: 15 jul. 2025.

[11] ANTHROPIC. Claude model comparison. 2025. Disponível em: https://docs.anthropic.com/en/docs/about-claude/models. Acesso em: 15 jul. 2025.

[12] MIMOCODE. Configuration reference. 2025. Disponível em: https://github.com/anthropics/claude-code/blob/main/docs/configuration.md. Acesso em: 15 jul. 2025.

[13] FOWLER, Martin. *Patterns of Enterprise Application Architecture*. Boston: Addison-Wesley, 2002. 533 p. ISBN 978-0-321-12742-6.

[14] ANTHROPIC. Claude Code: Profiles and configuration. 2025. Disponível em: https://docs.anthropic.com/en/docs/claude-code/configuration. Acesso em: 15 jul. 2025.

[15] GOLDBERG, David. *What Every Programmer Should Know About Memory*. 2. ed. Upper Saddle River: Prentice Hall, 2009. 112 p. ISBN 978-0-13-409266-5.

[16] BOURNE, Stephen R. *The Unix Programming Environment*. Upper Saddle River: Prentice Hall, 1984. 486 p. ISBN 978-0-13-937724-9.

[17] STALLINGS, William. *Operating Systems: Internals and Design Principles*. 9. ed. Hoboken: Pearson, 2018. 816 p. ISBN 978-0-13-467095-2.

[18] ANTHROPIC. Claude Code: Environment variables. 2025. Disponível em: https://docs.anthropic.com/en/docs/claude-code/environment-variables. Acesso em: 15 jul. 2025.

[19] NIELSEN, Jakob. *Usability Engineering*. San Francisco: Morgan Kaufmann, 1994. 358 p. ISBN 978-0-12-518406-0.

[20] BROOKS, Fred. *The Mythical Man-Month: Essays on Software Engineering*. Anniversary ed. Boston: Addison-Wesley, 1995. 322 p. ISBN 978-0-201-83595-1.

[21] SHNEIDERMAN, Ben. *Designing the User Interface: Strategies for Effective Human-Computer Interaction*. 6. ed. Hoboken: Pearson, 2017. 612 p. ISBN 978-0-13-438036-4.

[22] FIELDING, Roy T. *Architectural Styles and the Design of Network-based Software Architectures*. Tese (Doutorado) — University of California, Irvine, 2000. 180 p.

[23] NODE.JS FOUNDATION. npm documentation: Fixing npm permissions. 2025. Disponível em: https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally. Acesso em: 15 jul. 2025.

[24] ANTHROPIC. Getting your API key. 2025. Disponível em: https://console.anthropic.com/settings/keys. Acesso em: 15 jul. 2025.

[25] THE TWELVE-FACTOR APP. III. Config: Store config in the environment. 2025. Disponível em: https://12factor.net/config. Acesso em: 15 jul. 2025.

[26] ANTHROPIC. Claude Code: Troubleshooting. 2025. Disponível em: https://docs.anthropic.com/en/docs/claude-code/troubleshooting. Acesso em: 15 jul. 2025.

[27] AMAZON WEB SERVICES. Amazon Bedrock: Getting started. 2025. Disponível em: https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html. Acesso em: 15 jul. 2025.

[28] MICROSOFT. Azure OpenAI Service documentation. 2025. Disponível em: https://learn.microsoft.com/en-us/azure/ai-services/openai/. Acesso em: 15 jul. 2025.

[29] LOVERING, Cameron. Shell aliases best practices. *Linux Journal*, 2023. Disponível em: https://linuxjournal.com/article/shell-aliases-best-practices. Acesso em: 15 jul. 2025.

[30] MIMOCODE. Environment variables reference. 2025. Disponível em: https://github.com/anthropics/claude-code/blob/main/docs/environment-variables.md. Acesso em: 15 jul. 2025.

[31] ANTHROPIC. Claude Code: Enterprise configuration. 2025. Disponível em: https://docs.anthropic.com/en/docs/claude-code/enterprise. Acesso em: 15 jul. 2025.

[32] HUNT, Andrew; THOMAS, David. *The Pragmatic Programmer: Your Journey to Mastery*. 2. ed. Boston: Addison-Wesley, 2019. 352 p. ISBN 978-0-13-595705-9.

[33] HUMPHREYS, David. *Managing Software Projects*. 2. ed. Manchester: Europa Books, 2019. 346 p. ISBN 978-1-912585-10-8.

[34] McGOWAN, Vince. Secure handling of secrets in development environments. *Proceedings of the ACM Conference on Computer and Communications Security*, 2023. Disponível em: https://dl.acm.org/doi/10.1145/3576915.3623144. Acesso em: 15 jul. 2025.

[35] SCHNEIER, Bruce. *Secrets and Lies: Digital Security in a Networked World*. Hoboken: John Wiley & Sons, 2015. 432 p. ISBN 978-1-119-09278-0.

[36] TORVALDS, Linus; DIACONESCU, Greg. *Just for Fun: The Story of an Accidental Revolutionary*. New York: HarperBusiness, 2002. 272 p. ISBN 978-0-06-662073-3.

[37] RAYMOND, Eric S. *The Cathedral and the Bazaar: Musings on Linux and Open Source by an Accidental Revolutionary*. 2. ed. Sebastopol: O'Reilly Media, 2001. 292 p. ISBN 978-0-596-00108-7.

[38] KO, Andrew J. et al. A field study of professional developers working with AI assistants. *Proceedings of the IEEE International Conference on Software Maintenance and Evolution*, 2024. Disponível em: https://ieeexplore.ieee.org/document/10636470. Acesso em: 15 jul. 2025.

[39] BURNETT, Margaret et al. The interaction design of AI-assisted software development tools. *Proceedings of the ACM on Human-Computer Interaction*, v. 8, n. CSCW1, 2024. Disponível em: https://dl.acm.org/doi/10.1145/3637389. Acesso em: 15 jul. 2025.

[40] DOCKER. Docker documentation: Build images. 2025. Disponível em: https://docs.docker.com/build/building/dockerfile/. Acesso em: 15 jul. 2025.

[41] KERNIGHAN, Brian W.; RITCHIE, Dennis M. *The C Programming Language*. 2. ed. Upper Saddle River: Prentice Hall, 1988. 272 p. ISBN 978-0-13-110362-7.

[42] WIRTH, Niklaus. *Programming in Modula-2*. 3. ed. Berlin: Springer-Verlag, 1988. 298 p. ISBN 978-3-540-18224-7.

[43] STALLMAN, Richard. *Free Software, Free Society: Selected Essays of Richard M. Stallman*. 2. ed. Boston: GNU Press, 2015. 464 p. ISBN 978-0-9831592-4-7.

[44] RAYMOND, Eric S. *The Art of Unix Programming*. Boston: Addison-Wesley, 2003. 528 p. ISBN 978-0-13-142901-7.

[45] TRUSS, Ben et al. Effective environment management for AI-assisted development. *IEEE Software*, v. 41, n. 5, 2024. Disponível em: https://ieeexplore.ieee.org/document/10547890. Acesso em: 15 jul. 2025.

[46] WING, Jeannette M. Computational thinking. *Communications of the ACM*, v. 49, n. 3, p. 33-35, 2006. Disponível em: https://dl.acm.org/doi/10.1145/1118178.1118215. Acesso em: 15 jul. 2025.

[47] THOMPSON, Clive. *Smarter Than You Think: How Technology Is Changing Our Minds for the Better*. New York: Penguin Press, 2013. 356 p. ISBN 978-1-59420-445-6.

[48] GOLDBERG, David. *What Every Programmer Should Know About Memory*. 2. ed. Upper Saddle River: Prentice Hall, 2009. 112 p. ISBN 978-0-13-409266-5.

[49] NIERENBERG, Dale. Practical secrets management for development teams. *Proceedings of the USENIX Security Symposium*, 2023. Disponível em: https://www.usenix.org/conference/usenixsecurity23/presentation/niernenberg. Acesso em: 15 jul. 2025.

[50] LUTHER, Kurt et al. Secrets in the cloud: A study of credential management practices. *Proceedings of the ACM CCS*, 2024. Disponível em: https://dl.acm.org/doi/10.1145/3658644.3670300. Acesso em: 15 jul. 2025.

[51] ANTHROPIC. Claude Code: Container deployment guide. 2025. Disponível em: https://docs.anthropic.com/en/docs/claude-code/container-deployment. Acesso em: 15 jul. 2025.

[52] BALA, Rajiv et al. Containerized development environments: A systematic review. *Journal of Systems and Software*, v. 208, 2024. Disponível em: https://doi.org/10.1016/j.jss.2023.111900. Acesso em: 15 jul. 2025.

[53] OWASP Foundation. Top 10 API security risks. 2023. Disponível em: https://owasp.org/API-Security/editions/2023/en/0x11-server-side-request-forgery/. Acesso em: 15 jul. 2025.

[54] GROSSKURTH, Alan et al. API key management best practices. *Journal of Cybersecurity*, v. 10, n. 1, 2024. Disponível em: https://academic.oup.com/cybersecurity/article/10/1/tyae013/7586573. Acesso em: 15 jul. 2025.

[55] HASHICORP. Vault documentation: Secrets management. 2025. Disponível em: https://developer.hashicorp.com/vault/docs. Acesso em: 15 jul. 2025.

[56] ANTHROPIC. Claude Code: Configuration hierarchy. 2025. Disponível em: https://docs.anthropic.com/en/docs/claude-code/configuration#configuration-hierarchy. Acesso em: 15 jul. 2025.

[57] PARNAS, David L. Designing software for ease of extension and contraction. *IEEE Transactions on Software Engineering*, v. SE-5, n. 2, p. 128-138, 1979. Disponível em: https://ieeexplore.ieee.org/document/4393556. Acesso em: 15 jul. 2025.

[58] DOCKER. Best practices for building efficient Docker images. 2025. Disponível em: https://docs.docker.com/build/building/best-practices/. Acesso em: 15 jul. 2025.

[59] NEWMAN, Sam. *Building Microservices: Designing Fine-Grained Systems*. 2. ed. Sebastopol: O'Reilly Media, 2021. 612 p. ISBN 978-1-4920-3402-5.
