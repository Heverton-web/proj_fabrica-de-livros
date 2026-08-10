# Hiper-Personalização: OMP ao Seu Jeito

## Montando o painel de comando completo

No capítulo anterior, você configurou o sistema de memória do OMP — aquela âncora que mantém o agente lembrando de fatos, lições e preferências entre sessões. Mas a memória é apenas uma peça do quebra-cabeça.

O verdadeiro poder do OMP aparece quando você personaliza cada aspecto do harness: escolhe qual modelo roda em cada papel, quais ferramentas ficam habilitadas, quais regras guiam o comportamento e como tudo isso se integra ao editor que você já usa todos os dias.

## Config.yml: o painel de instrumentos do navio

Todo estaleiro funcional tem um painel central — um lugar onde o mestre ajusta motor, leme, instrumentos e comunicações. No OMP, esse painel é o arquivo `~/.omp/agent/config.yml`. Nele, você define três coisas fundamentais: quais modelos rolam em cada papel (modelRoles), quais ferramentas estão habilitadas (tools) e como a memória persiste entre sessões (memory).

O config.yml é lido quando o OMP inicia. Qualquer alteração nele exige reiniciar a sessão para ter efeito. Pense nele como o manual de operações do seu navio — ajustar o leme em alto-mar é possível, mas o ideal é calibrar tudo antes de zarpar.

## ModelRoles: 10 papéis, 10 motores

O OMP não trata todos os turnos da mesma forma. Ele diferencia 10 papéis distintos, cada um com suas necessidades de velocidade, raciocínio e custo.

| Role | Uso | Característica |
|------|-----|----------------|
| `default` | Turnos normais | Equilíbrio entre custo e qualidade |
| `smol` | Fan-out de subagentes | Modelo leve e barato para tarefas paralelas |
| `slow` | Raciocínio profundo | Modelo potente para problemas complexos |
| `plan` | Modo plano | Focado em planejamento, não execução |
| `commit` | Changelogs | Geração de mensagens de commit |
| `vision` | Análise de imagens | Processamento visual |
| `designer` | Design de interfaces | Geração de layouts |
| `task` | Orquestração | Coordenação de tarefas |
| `advisor` | Revisão inline | Segundo olho em cada turno |
| `tiny` | Tarefas leves | Rápido e econômico para operações simples |

A mágica está em mapear cada papel ao modelo certo. Você pode usar um modelo potente e caro para `slow` (problemas difíceis) e um modelo leve e barato para `smol` (dezenas de subagentes trabalhando em paralelo). Isso reduz custos sem sacrificar qualidade onde ela importa.

## Tools: o arsenal sob seu controle

O OMP vem com 31 ferramentas built-in, mas nem todas precisam estar ativas o tempo todo. O campo `tools` no config.yml permite habilitar ou desabilitar ferramentas específicas. Se você não trabalha com browser automation, pode desligar a ferramenta `browser` e reduzir o consumo de tokens por turno. Se seu projeto não usa debug nativo, desative `debug`.

## Memory: a memória que você cura

No Capítulo 15, você viu como o sistema de memória funciona. Agora, no config.yml, você escolhe o backend (local, Hindsight ou Mnemopi) e o escopo (projeto ou global). Essa escolha afeta onde os dados persistem e com quem são compartilhados.

## Configurando o config.yml

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

## Configurando o models.yml

Agora o models.yml — a oficina de motores. Aqui definimos providers customizados, incluindo modelos locais.

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

Observe que o `modelRoles` pode aparecer tanto no config.yml quanto no models.yml. Quando presente nos dois, o models.yml tem prioridade — é ele que define o mapeamento final entre provider e papel.

## Magic Keywords: atalhos de poder

O OMP reconhece três palavras mágicas que você pode incluir em qualquer mensagem para alterar o comportamento do agente. Essas keywords são processadas pelo harness antes de enviar ao modelo.

| Keyword | Efeito | Quando usar |
|---------|--------|-------------|
| `ultrathink` | Raciocínio multi-step cuidadoso | Problemas complexos que exigem análise profunda |
| `orchestrate` | Fan-out paralelo com verificação | Tarefas que se beneficiam de múltiplos workers |
| `workflowz` | Workflow determinístico multi-subagent | Pipelines com etapas bem definidas |

**Exemplo de uso:**

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

## ACP: integração com editores

O ACP (Agent Control Protocol) é o que permite rodar o OMP dentro de editores como Zed. Em vez de alternar entre terminal e editor, você mantém o agente integrado ao seu ambiente de trabalho.

```yaml
acp:
  enabled: true
  editor: zed
  save_path: /tmp/omp-acp-output
```

Quando o ACP está ativo, o OMP lê o buffer atual do editor, processa a instrução e escreve o resultado de volta. O fluxo é: você seleciona código no editor, envia um comando via ACP, o OMP lê o buffer, processa e gera a resposta, o resultado é escrito no save_path, e o editor atualiza o buffer.

## A Falha na Esteira e a Correção Estrutural

Você está trabalhando em um projeto grande com 15 módulos. Abre o terminal e inicia o OMP com a configuração padrão. O agente começa a trabalhar, mas algo está errado: ele está usando o modelo mais caro para tarefas simples de rename, e modelos baratos para problemas de arquitetura que exigem raciocínio profundo. O custo de tokens dispara e a qualidade cai nos pontos que mais importam.

O problema é que você não configurou as modelRoles. O OMP estava usando o mesmo modelo para tudo — como um navio que navega em velocidade máxima mesmo em porto, gastando combustível à toa.

**A correção:** você abre o models.yml e mapeia cada papel ao modelo certo.

```yaml
modelRoles:
  default: spark/minimax-m3      # Tarefas normais — barato e rápido
  slow: anthropic/claude-opus-4-0  # Problemas difíceis — potente
  smol: openai/gpt-4o-mini        # Subagentes — o mais econômico
```

Agora, quando o agente precisa de raciocínio profundo, ele sobe para o Opus. Quando distribui trabalho entre subagentes, usa o Mini. O custo cai significativamente sem sacrificar qualidade onde ela realmente importa.

## Armadilhas comuns

**Esquecer de reiniciar a sessão após editar config.yml.** As alterações só têm efeito na próxima inicialização do OMP.

**Mapear todos os papéis ao mesmo modelo.** Isso anula a vantagem de ter 10 roles distintos — use modelos diferentes para papéis diferentes.

**Habilitar ferramentas desnecessárias.** Cada ferramenta adiciona tokens ao system prompt. Se você não usa `browser`, desative-o.

**Não usar magic keywords.** São gratuitas e podem transformar a qualidade do resultado em tarefas complexas. O `ultrathink` sozinho evita erros que o agente cometeria em modo padrão.

**Configurar memory scope como `global` sem necessidade.** Dados globais vaziam o contexto em todos os projetos. Use `project` por padrão.

## Próximos Passos

Neste capítulo, você montou o painel de comando completo do seu estaleiro digital. Os três pilares — config.yml (instrumentos), models.yml (motores) e ACP + magic keywords (integração e atalhos) — transformam o OMP de ferramenta genérica em uma extensão personalizada do seu fluxo de trabalho.

Escolheu qual modelo roda em cada papel, configurou quais ferramentas ficam habilitadas, definiu o backend de memória e integrou o agente ao seu editor. Essa é a diferença entre usar o OMP e comandá-lo — e é exatamente o que separa um iniciante de um Mestre de Estaleiro Digital.

Acesse a documentação completa: https://omp.sh/docs

Siga-nous nas redes sociais para dicas, tutoriais e novidades sobre o Oh My Pi. Junte-se a mais de 23.3k desenvolvedores que já estão usando o harness mais completo do mercado.
