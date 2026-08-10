# Subagentes: Fan-out Paralelo de Tarefas

## Escalando para múltiplos workers

No capítulo anterior, você dominou o debug com DAP — 28 operações que transformam o agente em um debugger autônomo capaz de pausar processos, inspecionar variáveis e corrigir bugs na raiz.

Agora vamos escalar: em vez de um único agente fazendo tudo sequencialmente, vamos lançar múltiplos workers em paralelo — cada um isolado, com sua própria memória e resultado tipado.

## O que são subagentes e por que existem

Quando você trabalha com um coding agent sozinho, existe um limite natural de produtividade: o agente pode fazer apenas uma coisa por vez. Se sua tarefa requer analisar 50 arquivos de código, revisar 10 pull requests ou migrar um projeto inteiro de uma framework para outro, um único agente vai levar tempo demais — e o contexto dele vai encher antes de terminar.

Subagentes resolvem esse problema dividindo o trabalho. Cada subagente é um worker isolado que recebe uma tarefa específica, executa de forma autônoma e retorna um resultado tipado.

É como transformar um único estaleiro com um único operador em um estaleiro com múltiplas equipes especializadas trabalhando em paralelo.

## O sistema de tasks do OMP

O OMP implementa subagentes através da ferramenta `task`, que suporta três operações principais.

**create** — cria uma nova tarefa com um ID único (T1, T2, T3...) e um resumo do que precisa ser feito.

**spawn** — lança um subagente para executar a tarefa, que roda em background e retorna um actor_id.

**collect** — aguarda o resultado do subagente e valida seu output contra um schema.

A hierarquia de tasks permite criar estruturas complexas: uma tarefa pai pode ter múltiplas subtarefas (T1.1, T1.2, T1.3), cada uma com seu próprio subagente. Essa é a base do fan-out paralelo — lançar vários workers simultaneamente para cobrir diferentes aspectos de um problema.

## Schema validation: resultados tipados

Uma das features mais poderosas do sistema é a validação de schema. Quando você cria uma task, pode definir um `output_schema` que especifica exatamente quais campos o subagente deve retornar.

Isso garante que cada subagente retorna exatamente o que foi pedido, erros de formato são detectados antes de você processar o resultado, e múltiplos subagentes podem ser comparados diretamente porque seguem o mesmo formato.

É como se cada equipe do estaleiro tivesse um formulário padrão de reporte. Sem essa padronização, você teria que interpretar relatórios livres de cada especialista.

## O Agent Hub: painel de controle central

Enquanto os subagentes trabalham em paralelo, o Agent Hub fornece visibilidade total sobre o que está acontecendo. Você pode ver quais subagentes estão rodando, pendentes ou completados, monitorar o progresso de cada um em tempo real, cancelar subagentes que estão demorando ou falhando, e ajustar timeouts e limits de recursos.

O Agent Hub é o equivalente ao painel de controle do estaleiro — onde o mestre vê todas as equipes trabalhando e pode intervir quando necessário.

## O ciclo de vida de uma task

Cada task passa por um ciclo de vida bem definido. Ela começa como `open`, vai para `in_progress` quando um worker é spawned, e pode terminar como `done` ou `failed`. Se uma tarefa depender de outra, ela fica `blocked` até a dependência ser resolvida.

Esse ciclo garante que você sempre saiba o estado de cada tarefa. Se um worker falhar, a task volta para `open` e pode ser retomada.

## Fan-out/Fan-in: o padrão clássico

O padrão mais comum de subagentes é o fan-out/fan-in.

Primeiro, você distribui uma tarefa grande entre múltiplos workers — por exemplo, revisar 10 arquivos diferentes. Depois, cada worker processa sua parte independentemente. Por fim, você coleta todos os resultados e os consolida.

É como um estaleiro que distribui a construção do navio entre equipes especializadas — cada uma monta sua parte em paralelo, e no final todas as peças se encaixam perfeitamente porque seguem o mesmo schema de fabricação.

## Criando sua primeira task

A ferramenta `task` é a porta de entrada para subagentes.

```python
# Exemplo: criar uma task para revisar um arquivo
task_create = {
    "tool": "task",
    "input": {
        "action": "create",
        "summary": "Revisar o arquivo main.py e identificar bugs",
        "output_schema": {
            "type": "object",
            "properties": {
                "bugs_encontrados": {"type": "array", "items": {"type": "string"}},
                "severidade": {"type": "string", "enum": ["baixa", "media", "alta"]},
                "recomendacoes": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["bugs_encontrados", "severidade"]
        }
    }
}
```

Quando você envia essa task, o OMP retorna um ID (ex: T1) que você usa para rastrear o progresso.

## Spawning um subagente

Depois de criar a task, você lança um subagente para executá-la.

```python
# Exemplo: spawn um subagente para a task T1
task_spawn = {
    "tool": "task",
    "input": {
        "action": "spawn",
        "task_id": "T1",
        "prompt": "Analise o arquivo main.py. Procure por: bugs lógicos, erros de tratamento de exceção, código morto, e potential race conditions.",
        "context": "full"
    }
}
```

O subagente roda em background e retorna um `actor_id` que você usa para monitorar seu progresso.

## Fan-out com múltiplos workers

Para distribuir trabalho entre vários workers, crie múltiplas tasks e spawne um subagente para cada uma.

```python
# Exemplo: fan-out para revisar 3 arquivos diferentes
files_to_review = ["src/auth.py", "src/api.py", "src/models.py"]

for i, file in enumerate(files_to_review, 1):
    task_id = f"T{i}"
    # Criar task
    task_create = {
        "tool": "task",
        "input": {
            "action": "create",
            "task_id": task_id,
            "summary": f"Revisar {file} para bugs e más práticas"
        }
    }
    
    # Spawn worker
    task_spawn = {
        "tool": "task",
        "input": {
            "action": "spawn",
            "task_id": task_id,
            "prompt": f"Analise o arquivo {file}. Identifique bugs, código morto, e oportunidades de refactoring."
        }
    }
```

Agora três workers estão rodando em paralelo, cada um analisando um arquivo diferente.

## Collecting resultados

Quando todos os workers terminarem, você coleta os resultados.

```python
# Exemplo: aguardar e coletar resultados
task_collect = {
    "tool": "task",
    "input": {
        "action": "collect",
        "task_ids": ["T1", "T2", "T3"],
        "timeout_ms": 60000
    }
}

# Resultado consolidado
resultado = {
    "T1": {"bugs": ["SQL injection em login"], "severidade": "alta"},
    "T2": {"bugs": ["Race condition em /api/users"], "severidade": "media"},
    "T3": {"bugs": [], "severidade": "baixa"}
}
```

O Agent Hub coleta todos os resultados e os apresenta de forma consolidada.

## Caso de uso: code review paralelo

Imagine que você tem um pull request com 10 arquivos modificados e precisa revisar todos antes de mergear. Em vez de revisar sequencialmente (o que levaria 30+ minutos), você distribui entre 5 workers.

Em vez de 30 minutos sequenciais, você resolve em 5 minutos paralelos — 6x mais rápido.

## Caso de uso: migração de framework

Migrar um projeto de uma framework para outra é trabalhoso e propenso a erros. Subagentes tornam isso gerenciável.

Cada worker opera isolado em seu módulo — não há conflitos de edição porque cada um trabalha em arquivos diferentes.

## Caso de uso: refactoring distribuído

Refactoring em grande escala pode ser assustador. Subagentes permitem dividir o trabalho entre especialistas.

Cada worker foca em um tipo específico de melhoria — type hints, logging, testes — e todos trabalham em paralelo sem conflitos.

## Próximos Passos

Neste capítulo, você aprendeu a transformar um único agente em uma equipe inteira de workers paralelos. O sistema de subagentes do OMP oferece três capacidades fundamentais.

Fan-out com schema validation: você distribui trabalho entre múltiplos workers, cada um retornando resultados tipados que garantem consistência e facilitam consolidação.

Agent Hub para monitoramento ao vivo: você mantém visibilidade total sobre seus subagentes — sabendo quando intervenir, quando cancelar e quando coletar resultados.

Padrões de uso prático: code review paralelo, migração de framework e refactoring distribuído são apenas alguns dos casos de uso que se beneficiam do fan-out paralelo.

No próximo capítulo, veremos como o Advisor Model funciona como um revisor a cada turno — um segundo olhar que garante qualidade antes que cada peça seja montada no casco.

Acesse a documentação completa: https://omp.sh/docs

Siga-nous nas redes sociais para dicas, tutoriais e novidades sobre o Oh My Pi.
