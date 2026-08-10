# 60+ Providers: Roteamento Inteligente de Modelos

## Uma frota de motores para cada tarefa

No capítulo anterior, você dominou a browser tool e a computer tool — o estaleiro se estendeu por toda a superfície do oceano digital, de portos (websites) ao convés do desktop.

Agora vamos mais fundo: e se cada tarefa pudesse ser executada pelo motor certo do navio? Imagine que seu estaleiro tivesse acesso a dezenas de motores diferentes — cada um com uma potência, um custo e uma eficiência distintos. Tarefa leve? Motor econômico. Raciocínio profundo? Motor pesado. Análise de imagem? Motor especializado.

É exatamente isso que o OMP oferece com seus mais de 60 providers de LLM.

## O Universo dos Providers

Um provider é simplesmente uma fonte de modelos de linguagem. Cada provider oferece um ou mais modelos, cada um com suas características — custo por token, velocidade de resposta, janela de contexto e qualidade de raciocínio.

O OMP categoriza os providers em três grandes grupos.

### Frontier APIs

As grandes plataformas que hospedam modelos de ponta. OpenAI (GPT-4o, GPT-4.1, o3-mini, o4-mini), Anthropic (Claude Opus 4, Claude Sonnet 4, Claude Haiku), Google (Gemini 2.5 Pro, Gemini 2.5 Flash), xAI (Grok 4, Grok 4 Fast), DeepSeek (DeepSeek R1, DeepSeek V3), e Mistral (Mistral Large, Codestral).

Essas APIs são acessadas via chave de API — você paga por token consumido. É como alugar um motor de um estaleiro externo: você usa quando precisa, paga pelo tempo de uso e devolve quando termina.

### Coding Plans

Assinaturas que incluem acesso a modelos. OpenAI Pro, Anthropic Max, Google AI Ultra. São como ter um contrato de manutenção com o estaleiro: você paga uma taxa fixa e tem acesso garantido a qualquer motor da frota.

### Run-it-yourself

Modelos que rodam na sua própria infraestrutura. Ollama (modelos locais como Llama, Mistral, Qwen sem custo por token), vLLM (servidor de inferência para equipes com GPUs dedicadas), e LiteLLM (proxy unificado que converte qualquer provider em formato OpenAI).

É como construir seu próprio motor no estaleiro: custo inicial maior, mas controle total e custo marginal zero. Para um iniciante, Ollama é a porta de entrada — basta instalar, baixar um modelo e apontar o OMP para `localhost:11434`.

## Por Que Ter Mais de Um Provider?

Cada modelo tem pontos fortes e fracos. O Claude Opus 4 é excepcional em raciocínio profundo, mas custa mais. O Gemini Flash é barato e rápido, mas menos preciso em tarefas complexas. O GPT-4o equilibra custo e qualidade. Ter apenas um provider é como ter um navio com um único motor: se ele quebra ou fica caro demais, toda a operação para.

O OMP resolve isso com quatro mecanismos de roteamento: Model Roles, Fallback Chains, Path-Scoped Models e Round-Robin Credentials.

## Os 10 Roles de Modelo

O OMP define 10 funções que cada modelo pode assumir. Cada role mapeia para um modelo diferente no seu `models.yml`.

| Role | Função | Exemplo de Uso |
|------|--------|----------------|
| `default` | Turnos normais de conversa | Editar código, responder perguntas |
| `smol` | Fan-out barato de subagentes | Tarefas paralelas simples |
| `slow` | Raciocínio profundo | Arquitetura complexa, debug difícil |
| `plan` | Modo plano (planejamento) | Criar roadmaps, analisar arquitetura |
| `commit` | Geração de changelogs | Mensagens de commit, PR descriptions |
| `vision` | Análise de imagens | Screenshots, mockups, diagramas |
| `designer` | Design de interfaces | Layout, componentes, CSS |
| `task` | Orquestração de tarefas | Gerenciar subagentes, coordenar |
| `advisor` | Revisor inline | Segundo olho em cada turno |
| `tiny` | Tarefas leves | Validação, formatação, lint |

Esses roles são a intelligence do roteamento. Quando você define `smol: openai/gpt-4o-mini`, está dizendo: "tarefas baratas e paralelas vão para o modelo mais econômico". Quando define `slow: anthropic/claude-opus-4-0`, está dizendo: "raciocínio profundo vai para o modelo mais inteligente".

## Configurando seu Primeiro Provider

Vamos começar pelo básico: configurar um provider frontier. O arquivo de configuração de modelos do OMP fica em `~/.omp/agent/models.yml`.

```yaml
# ~/.omp/agent/models.yml

providers:
  openai:
    apiKey: "<sua-chave-openai>"
    api: openai-completions
    models:
      - id: gpt-4o
        name: GPT-4o
        contextWindow: 128000
        maxTokens: 16384
      - id: gpt-4o-mini
        name: GPT-4o Mini
        contextWindow: 128000
        maxTokens: 16384

  anthropic:
    apiKey: "<sua-chave-anthropic>"
    api: anthropic-messages
    models:
      - id: claude-sonnet-4-20250514
        name: Claude Sonnet 4
        contextWindow: 200000
        maxTokens: 16000

modelRoles:
  default: openai/gpt-4o
  smol: openai/gpt-4o-mini
  slow: anthropic/claude-sonnet-4-20250514
```

Com essa configuração, o OMP já roda com três modelos diferentes. Quando você conversa normalmente, usa o GPT-4o (role `default`). Quando o OMP spawna subagentes para tarefas simples, usa o GPT-4o Mini (role `smol`). Quando precisa de raciocínio profundo, usa o Claude Sonnet 4 (role `slow`).

## Adicionando Ollama: Self-Hosting Gratuito

Para rodar modelos locais sem custo por token, instale o Ollama e configure-o no OMP.

```yaml
providers:
  ollama:
    baseUrl: http://localhost:11434/v1
    api: openai-completions
    apiKey: dummy
    models:
      - id: llama3.1
        name: Llama 3.1 8B
        contextWindow: 128000
        maxTokens: 4096
      - id: qwen2.5-coder
        name: Qwen 2.5 Coder 7B
        contextWindow: 32000
        maxTokens: 4096

modelRoles:
  default: ollama/llama3.1
  smol: ollama/qwen2.5-coder
  tiny: ollama/qwen2.5-coder
```

Agora seu estaleiro tem um motor local (Ollama) e pode funcionar mesmo sem internet. Para tarefas que exigem mais potência, você mantém os providers frontier como alternativa.

## Montando uma Fallback Chain

O verdadeiro poder do roteamento emerge quando você configura fallback chains. Imagine que você depende do Claude Sonnet 4 para tarefas importantes, mas ele pode ficar indisponível ou atingir rate limit. A fallback chain garante que outra opção entre em ação.

```yaml
modelRoles:
  slow:
    - anthropic/claude-sonnet-4-20250514
    - openai/gpt-4o
    - ollama/llama3.1

  default:
    - openai/gpt-4o
    - anthropic/claude-sonnet-4-20250514
    - ollama/llama3.1
```

Quando o modelo principal da role `slow` falha, o OMP automaticamente tenta o próximo da lista. É como ter um navio com motor principal e dois reservas — se um quebra, o próximo liga sem intervenção manual.

## Path-Scoped Models

Outro knob de roteamento poderoso é o path-scoped model — definir modelos diferentes dependendo de onde o agente está trabalhando. Por exemplo, código Python pode usar um modelo especializado em Python, enquanto documentação usa um modelo barato.

```yaml
modelRouting:
  - path: "**/*.py"
    model: anthropic/claude-sonnet-4-20250514

  - path: "**/*.md"
    model: openai/gpt-4o-mini

  - path: "**/*.yml"
    model: ollama/qwen2.5-coder
```

É como ter equipamentos diferentes no estaleiro para cada tipo de material — cortadores de aço para o casco, soldadores especiais para o motor, pintores refinados para a cabine.

## Round-Robin de Credenciais

Se você tem múltiplas chaves de API do mesmo provider, o OMP suporta round-robin — rotação automática entre as chaves.

```yaml
providers:
  openai:
    apiKeys:
      - "<chave-conta-1>"
      - "<chave-conta-2>"
      - "<chave-conta-3>"
    api: openai-completions
    models:
      - id: gpt-4o
```

O OMP distribui as requisições entre as três chaves ciclicamente. Se uma chave atinge o rate limit, as outras duas continuam disponíveis.

## Os 4 Knobs de Roteamento

| Knob | O que faz | Quando usar |
|------|-----------|-------------|
| **Model Roles** | Mapeia funções para modelos | Sempre — é a configuração base |
| **Fallback Chains** | Lista ordenada de alternativas | Quando depende de APIs externas |
| **Path-Scoped Models** | Modelos diferentes por tipo de arquivo | Quando projetos misturam linguagens |
| **Round-Robin** | Rotação de chaves de API | Quando tem múltiplas contas |

## Cena de contraste: o navio que ficou parado

Imagine que você configurou seu OMP com um único provider — o Claude Sonnet 4 da Anthropic. Tudo funciona perfeitamente até segunda-feira às 9h, quando toda a equipe começa a usar o mesmo modelo para code review. O rate limit é atingido em minutos.

Seu OMP começa a retornar erros 429. O agente congela. Você fica sem resposta por 20 minutos — o tempo necessário para o rate limit resetar. O navio ficou parado no meio do oceano, sem motor reserva.

Agora veja como seria com fallback chain configurada. Quando o Claude atinge rate limit, o OMP detecta o erro automaticamente e muda para o GPT-4o em milissegundos. Se o OpenAI também estiver sobrecarregado, o agente cai no Ollama local — sem custo, sem rate limit, sem downtime. O navio nunca para de navegar.

## Armadilhas comuns

**Esquecer de configurar fallback para roles críticos.** Se só o `default` tem fallback e o `slow` não, uma falha no modelo de raciocínio profundo trava todas as tarefas complexas.

**Usar o mesmo modelo para todos os roles.** Se `smol` e `slow` apontam para o mesmo modelo, você desperdiça dinheiro — tarefas baratas rodam no modelo caro.

**Não testar a fallback chain.** Configure, teste, quebre de propósito. Desative o provider principal e veja se o backup funciona. É como testar o motor reserva antes de zarpar.

**Ignorar o Ollama para tarefas leves.** Modelos locais de 7-8B são perfeitos para `tiny` e `smol` — tarefas de validação, formatação e lint não precisam de modelos frontier.

**Deixar chaves de API no models.yml sem variável de ambiente.** Em produção, use `${OPENAI_API_KEY}` em vez de colocar a chave diretamente no arquivo.

## Próximos Passos

Neste capítulo, você descobriu que o estaleiro do OMP pode operar com uma frota inteira de motores. Frontier APIs, coding plans e self-hosting oferecem três caminhos para acessar modelos. Custom providers em models.yml dão controle total sobre quais modelos estão disponíveis. E fallback chains, path-scoped models e round-robin são os quatro knobs de roteamento que garantem que seu agente nunca fique parado.

No próximo capítulo, você vai aprender sobre Time-Traveling Stream Rules — regras inteligentes que injetam correções mid-stream quando o modelo começa a desviar.

Acesse a documentação completa: https://omp.sh/docs

Siga-nous nas redes sociais para dicas, tutoriais e novidades sobre o Oh My Pi.
