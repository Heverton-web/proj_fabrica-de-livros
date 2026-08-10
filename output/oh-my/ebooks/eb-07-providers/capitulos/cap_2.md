# Time-Traveling Stream Rules: Course-Correction Inteligente

## GPS que corrige a rota em tempo real

No capítulo anterior, você dominou o roteamento inteligente de modelos — fallback chains, path-scoped models e round-robin credentials que garantem que o modelo certo atenda a cada tarefa.

Mas e se o próprio modelo, mesmo sendo o certo para a tarefa, starts a gerar algo fora do script? E se, no meio de um stream de saída, você pudesse detectar o desvio e corrigir o modelo antes que ele terminasse a frase — como um timoneiro que ajusta o leme no instante em que o navio começa a sair da rota?

É exatamente isso que o OMP oferece com as Time-Traveling Stream Rules.

## O Problema: Modelos que Saem do Script

Todo modelo de linguagem tem moments de desvio. Você configura o roteamento perfeito — Claude para raciocínio, Grok para código, Gemini para visão — e mesmo assim o modelo começa a gerar o que não deveria. Talvez ele ignore uma regra de estilo, comece a usar uma API deprecada, ou starts a produzir código sem tratamento de erros.

Até agora, a solução era reforçar o system prompt com mais regras — mas isso tem um custo. Cada regra adicionada ao system prompt consome tokens em cada turno, mesmo quando o modelo não precisa dela. É como manter todos os equipamentos do estaleiro ligados o tempo todo, mesmo quando só precisa de um martelo.

## A Solução: Stream Rules — Regras que Dormem até Serem Necessárias

As stream rules do OMP funcionam de forma fundamentalmente diferente. Em vez de serem injetadas no system prompt (pagando token a cada turno), elas ficam dormientes — monitorando o stream de saída em tempo real. Quando o modelo gera algo que casa com o regex pattern da regra, a regra "acorda" e age.

O mecanismo tem três passos.

**Regex Match:** o OMP aplica os patterns de regex ao stream de tokens conforme são gerados. Não é preciso esperar o turno inteiro — o match acontece token a token.

**Abort Mid-Token:** quando um match é encontrado, o OMP aborta o stream imediatamente, no meio do token que está sendo gerado. O modelo não termina a frase errada.

**Retry com System Reminder:** o OMP injeta a stream rule como um system reminder no contexto e faz retry a partir do ponto anterior ao desvio. O modelo recebe a correção e continua de onde parou — agora na rota correta.

O custo? Zero tokens adicionais em turns normais. As regras só consomem tokens quando são ativadas — quando o modelo realmente precisa da correção.

## Dois Modos de Correção

As stream rules oferecem dois modos de ação, cada um adequado a um tipo de desvio.

**Abort + Retry (correção dura):** o stream é abortado, a regra é injetada como system reminder, e o modelo refaz a saída. Usado quando o desvio é grave — como gerar código sem tratamento de erros ou usar uma API deprecada.

**Inject-Only (lembrete suave):** a regra é injetada como system reminder sem abortar o stream. O modelo continua gerando, mas agora tem a informação da regra no contexto. Usado quando o desvio é leve — como uma convenção de nomenclatura que o modelo esqueceu.

A escolha entre um e outro depende da gravidade do desvio. Abort é cirúrgico; inject é preventivo.

## A metáfora do navio em oceano

Imagine que você está navegando com um navio de carga pelo oceano. O compás aponta a rota correta, mas de vez em quando uma corrente marinha forte começa a empurrar o navio para fora do curso.

Sem monitoramento, o navio só descobre o desvio quando chega ao porto errado — aí já gastou combustível, tempo e dinheiro.

Agora imagine que o navio tem um sistema de monitoramento que verifica a posição a cada instante. No momento em que a corrente começa a desviar o navio, o sistema dispara um alarme, o timoneiro ajusta o leme imediatamente, e o navio volta à rota — sem nem perceber que esteve perto de sair do curso.

As stream rules são esse sistema de monitoramento. O regex pattern é o sensor que detecta a corrente. O abort é o alarme que para o navio no meio da manobra. O system reminder é a instrução que o timoneiro recebe para corrigir o rumo.

## Estrutura de uma Stream Rule

Uma stream rule é declarada na seção `streamRules` do `config.yml` do OMP. Cada regra tem quatro campos essenciais.

```yaml
streamRules:
  - name: "bloquear-codigo-sem-error-handling"
    pattern: '(?i)(try|catch|except|raise|throw)\s*\{?\s*\}'
    action: "abort"
    reminder: |
      Você começou a gerar um bloco try-catch vazio. Todo tratamento de erros
      DEVE ter pelo menos um log ou re-throw. Corrija o bloco antes de continuar.
```

**name:** identificador único da regra (para debug e logs). **pattern:** regex pattern aplicado ao stream de tokens. **action:** `"abort"` para correção dura, `"inject"` para lembrete suave. **reminder:** o texto do system reminder que será injetado quando a regra disparar.

## Regras com Múltiplos Patterns

Para cenários mais complexos, você pode declarar múltiplos patterns em uma única regra.

```yaml
streamRules:
  - name: "proibir-imports-deprecados"
    patterns:
      - 'from\s+RPi\.GPIO\s+import'
      - 'import\s+RPi\.GPIO'
      - 'import\s+RPi\.GPIO\s+as\s+GPIO'
    action: "abort"
    reminder: |
      Você está usando RPi.GPIO, que está deprecada e não suporta o Pi 5/RP1.
      Use gpiozero em vez dele.
```

Quando qualquer um dos patterns casa, a regra dispara. Isso permite cobrir variações de uma mesma proibição sem duplicar regras.

## Regras com Escopo de Path

Assim como os path-scoped models, as stream rules podem ser restritas a diretórios específicos.

```yaml
streamRules:
  - name: "proibir-var-global-em-modulos"
    pattern: '^(?:var|let|const)\s+\w+\s*=\s*.*(?:process\.env|require)'
    action: "inject"
    reminder: |
      Evite variáveis globais com process.env em módulos compartilhados.
      Passe a configuração como parâmetro ou use um módulo de config centralizado.
    paths:
      - "src/shared/**"
      - "src/utils/**"
```

A regra só é monitorada quando o modelo está editando arquivos dentro dos paths listados.

## Monitoramento em Tempo Real

O OMP não precisa esperar o turno inteiro para detectar o desvio. Conforme o modelo gera tokens, o OMP acumula um buffer interno. A cada token, o buffer é testado contra todos os patterns das stream rules ativas.

Se um match é encontrado, o OMP envia um sinal de abort para o provider API. O stream é interrompido imediatamente — o modelo não gera mais tokens. O system reminder da regra é injetado no contexto da sessão. E o OMP faz retry do prompt anterior ao desvio, agora com a correção no contexto.

O tempo entre o match e o abort é menor que um token — o modelo não tem chance de completar a frase errada.

## Regras Persistentes vs. Regras de Sessão

As stream rules podem ser declaradas em dois níveis.

**Persistentes (config.yml):** ficam ativas em todas as sessões. São ideais para regras de qualidade universal — como proibir imports deprecados ou exigir tratamento de erros.

**De sessão (inline):** declaradas via `/rule` durante uma sessão. São ideais para correções pontuais — como uma regra específica para o módulo que você está trabalhando agora.

```bash
# Criar uma regra de sessão
/rule add --name "evitar-console-log-em-prod" \
  --pattern 'console\.(log|debug|info)\(' \
  --action inject \
  --reminder "Em produção, use um logger estruturado em vez de console.log"

# Listar regras ativas
/rule list

# Remover uma regra
/rule remove "evitar-console-log-em-prod"
```

## Armadilhas comuns

**Regex muito amplo.** Se o pattern casa com coisas que não são desvios, a regra dispara atoa e interrompe o stream desnecessário. Teste seus patterns com exemplos reais antes de ativar.

**Reminder vago.** Se o system reminder não explica o que o modelo deve fazer em vez da ação proibida, o modelo pode simplesmente parar de gerar — e você perde mais tokens com a hesitação do que com o desvio original.

**Muitas regras ativas.** Cada regra consome processamento (regex match token a token). Mais de 10-15 regras ativas simultaneamente pode introduzir latência perceptível no stream.

## Próximos Passos

Você agora domina três pilares das Time-Traveling Stream Rules do OMP. Regex Match e Abort — o mecanismo que detecta desvios em tempo real e interrompe o stream antes que o erro se propague. Injeção de System Reminders sob demanda — o sistema que injeta correções apenas quando o modelo precisa delas, sem poluir o contexto em turns normais. E Sobrevivência a Compaction — a garantia de que as correções injetadas persistem mesmo quando o contexto é compactado.

No próximo capítulo, você vai descobrir como o OMP lida com memória entre sessões — como o agente lembra do que aprendeu, curta fatos relevantes e mantém o conhecimento acumulado ao longo do tempo.

Acesse a documentação completa: https://omp.sh/docs

Siga-nous nas redes sociais para dicas, tutoriais e novidades sobre o Oh My Pi.
