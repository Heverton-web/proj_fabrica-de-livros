# Debug com DAP: O Agente como Debugger

## Diagnóstico profundo do motor

No capítulo anterior, você dominou o LSP integrado — 14 operações que dão ao agente a inteligência do seu IDE. Agora vamos um passo além: não apenas ler e renomear código, mas pausar sua execução no exato ponto onde o problema acontece, inspecionar variáveis em tempo real e corrigir o bug na raiz.

Imagine que, em vez de apenas olhar para o casco do navio por fora, você pudesse abrir uma escotilha, descer ao porão e examinar cada parafuso do motor enquanto ele ainda está ligado. É exatamente isso que o Debug Adapter Protocol (DAP) permite ao agente fazer.

## O que é o DAP e por que ele existe

Antes do DAP, cada IDE precisava escrever sua própria integração com cada debugger. O VS Code tinha uma forma de falar com o GDB, o Vim tinha outra, e os debuggers precisavam suportar dezenas de protocolos diferentes.

Foi como se cada estaleiro tivesse seu próprio sistema de comunicação interna — a tripulação não conseguia falar entre si quando trocava de navio.

O DAP resolve isso criando um protocolo único. Assim como um standard de encaixe permite que qualquer equipamento de qualquer fabricante se conecte ao mesmo casco, o DAP permite que qualquer IDE fale com qualquer debugger usando a mesma linguagem.

O OMP implementa as 28 operações desse protocolo, o que significa que ele pode dirigir debuggers de verdade — não simuladores, não print statements, debuggers reais que pausam a execução e permitem inspeção completa do estado.

## Os três debuggers do OMP

O OMP se conecta a três engines de debug diferentes, cada um especializado em uma linguagem.

**lldb-dap**: o debugger da família LLVM/Clang, otimizado para C, C++ e Objective-C. Ele é o equipamento pesado do estaleiro, capaz de examinar memória bruta, registros da CPU e estruturas de dados de baixo nível.

**dlv (Delve)**: o debugger nativo da Go. Se o lldb é o guindaste de casco, o dlv é o scanner de motor — ele entende goroutines, canais e o runtime da Go, coisas que um debugger genérico simplesmente não enxerga.

**debugpy**: o debugger do Python, compatível com o protocolo DAP. Ele permite pausar scripts Python, inspecionar objetos dinâmicos e avaliar expressões em tempo de execução — como um instrumento de medição que se adapta automaticamente ao tipo de peça que está analisando.

## O fluxo de uma sessão de debug

Toda sessão de debug segue um ciclo comum.

Primeiro, o agente inicializa a sessão DAP, informando ao debugger quais capabilities ele suporta. Depois, ele pode lançar um novo processo ou se anexar a um processo já em execução.

Uma vez conectado, o agente define pontos de parada, dá o comando de continuação e espera o debugger reportar que atingiu um desses pontos.

É nesse momento que a mágica acontece: o agente pode ler variáveis, caminhar pela pilha de chamadas e até mesmo avaliar expressões arbitrárias no contexto do programa pausado.

## O debugger como um câmbio lento

Pense no debugging como inspecionar um navio em construção no estaleiro. Quando você constrói um navio, às vezes ele não funciona como esperado — o motor faz um barulho estranho, a rota desvia, ou uma peça simplesmente não encaixa.

Na vida real, você desligaria o motor, abriria a cobertura e examinaria cada componente com uma lanterna e um multímetro.

O DAP faz exatamente isso, mas no mundo digital. Em vez de desligar o motor inteiramente, o debugger coloca um "câmbio lento" — ele pausa a execução no ponto exato que você quer examinar, sem matar o processo.

É como congelar o tempo dentro do navio para que a tripulação possa caminhar pelo casco e verificar cada solda, cada parafuso, cada fio elétrico sem que o motor pare de funcionar quando o tempo voltar ao normal.

O OMP, nesse cenário, é o Mestre de Estaleiro que comanda essa inspeção. Ele decide onde colocar os pontos de verificação (breakpoints), quando avançar um passo (step), e quais instrumentos usar para medir (scopes e variables).

## Inicializando a sessão DAP

A ferramenta `debug` do OMP é a porta de entrada para tudo. Quando você pede ao agente que debugge algo, ele abre uma sessão DAP e se conecta ao debugger apropriado.

```python
# Exemplo: como o OMP se conecta ao debugpy para Python
debug_session = {
    "command": "initialize",
    "arguments": {
        "clientID": "omp",
        "adapterID": "debugpy",
        "supportsProgressReporting": True,
        "supportsRunInTerminalRequest": True
    }
}
```

O debugger responde com suas capabilities — quais tipos de breakpoints ele suporta, se aceita eval de expressões, se pode listar threads. Essa negociação é automática; o OMP cuida de tudo para você.

## Conectando a um processo Python com debugpy

Vamos ver como o OMP debuga um script Python. Primeiro, você precisa que o debugpy esteja instalado no seu ambiente. Depois, o agente pode lançar o script ou se anexar a um processo que já está rodando.

```python
# script_com_bug.py
def calcular_media(notas):
    total = 0
    for nota in notas:
        total += nota
    media = total / len(notas)  # Bug: divisao por zero se notas for vazio
    return media

# Chamada que causa o erro
resultado = calcular_media([])
print(f"Media: {resultado}")
```

Quando o OMP detecta esse bug, ele pode lançar uma sessão de debug automaticamente. O agente diz ao debugpy para pausar na linha da divisão e, quando o programa atinge esse ponto, inspeciona a variável `notas` — descobrindo que é uma lista vazia, o que causa a divisão por zero.

```python
# Comando debug que o OMP envia ao debugpy
set_breakpoints = {
    "command": "setBreakpoints",
    "arguments": {
        "source": {"path": "/caminho/para/script_com_bug.py"},
        "breakpoints": [
            {"line": 5, "condition": "len(notas) == 0"}
        ]
    }
}

# Quando o breakpoint e atingido, o agente inspeciona
evaluate_expr = {
    "command": "evaluate",
    "arguments": {
        "expression": "notas",
        "frameId": 1,
        "context": "watch"
    }
}
# Retorna: {"result": "[]", "type": "list"}
```

## Debugando C com lldb-dap

Para código nativo, o OMP usa o lldb-dap. A diferença principal é que você precisa compilar o binário com símbolos de debug (`-g`) antes de iniciar a sessão.

```bash
# Compilar com simbolos de debug
gcc -g -o meu_programa meu_programa.c
```

Uma vez rodando, o agente pode definir breakpoints em funções específicas, examinar o frame da pilha e ler variáveis locais — tudo em código nativo, sem precisar de um IDE gráfico.

## Debugando Go com dlv

O Delve (dlv) é o debugger nativo da Go e entende profundamente o runtime da linguagem. Ele pode pausar goroutines individuais, inspecionar canais e examinar o estado do garbage collector.

```go
// main.go
package main

import "fmt"

func processarDados(dados []int) int {
    resultado := 0
    for i, d := range dados {
        resultado += d / dados[i+1]  // Bug: index out of range
    }
    return resultado
}

func main() {
    dados := []int{10, 20, 30, 0}
    fmt.Println(processarDados(dados))
}
```

O OMP detecta o panic e lança uma sessão dlv. O agente pode, então, listar todas as goroutines em execução, inspecionar o frame onde o panic aconteceu e ver o valor de `i` e `dados[i+1]` no momento exato do erro.

## As 28 operações DAP em detalhe

O DAP define um conjunto completo de operações que o OMP implementa.

| Categoria | Operações | O que fazem |
|---|---|---|
| **Sessão** | initialize, launch, attach, disconnect | Criam e encerram a sessão de debug |
| **Breakpoints** | setBreakpoints, setFunctionBreakpoints, setInstructionBreakpoints, setExceptionBreakpoints, clearBreakpoints | Definem onde o programa deve pausar |
| **Controle** | continue, next, stepIn, stepOut, stepBack, reverseContinue, pause | Movem a execução pelo código |
| **Estado** | threads, stackTrace, scopes, variables, modules | Examinam o estado interno do programa |
| **Avaliação** | evaluate | Rodam expressões no contexto do programa |
| **Exceção** | setExceptionBreakpoints | Configuram pausa em erros |
| **Dados** | dataBreakpoint, instructionBreakpoints | Breakpoints em mudança de dados |

Essas 28 operações dão ao agente controle total sobre o programa.

## A falha silenciosa em produção

Você está trabalhando em uma API Go que processa pedidos de um e-commerce. Em desenvolvimento, tudo funciona perfeitamente. Mas em produção, o serviço começa a travar aleatoriamente — sem erro, sem log, simplesmente para de responder.

Você suspeita de um deadlock entre goroutines, mas como encontrar o ponto exato onde os canais travam?

O erro comum seria adicionar `fmt.Println` por todo o código, compilar, rodar novamente e torcer para capturar o momento do travamento. É como tentar encontrar um parafuso solto em um navio em movimento, chutando cada equipamento até ouvir um barulho diferente.

A prática correta com o OMP é diferente. O agente se anexa ao processo Go em execução usando dlv, sem reiniciar nada. Ele lista todas as goroutines ativas e identifica quais estão bloqueadas em operações de canal.

Em seguida, ele examina os frames de cada goroutine bloqueada, encontrando o ponto exato onde o canal está esperando uma mensagem que nunca chega — talvez porque uma goroutine morreu silenciosamente antes de enviar.

O resultado é preciso: em vez de adivinhar, você tem o estado completo do programa no momento do travamento.

## Armadilhas comuns ao usar DAP

**Esquecer símbolos de debug.** Ao compilar código C/C++, sem `-g` o lldb não consegue mapear endereços de memória para linhas de código. O agente vê endereços hexadecimais em vez de nomes de funções.

**Anexar com atraso.** Em processos de alta performance, pausar para inspecionar pode causar timeouts. Use breakpoints condicionais em vez de pausar em todas as iterações.

**Avaliar expressões com efeitos colaterais.** O DAP permite avaliar expressões arbitrárias, mas chamar funções que modificam estado durante debug pode causar comportamento inesperado. Use `context: "watch"` para avaliações sem efeito colateral.

## Próximos Passos

Neste capítulo, você viu como o DAP transforma o OMP de um leitor de código em um debugger autônomo. As 28 operações do protocolo dão ao agente controle total sobre a execução do programa — desde inicializar uma sessão até avaliar expressões no contexto de um breakpoint.

Os três debuggers suportados (lldb-dap, dlv e debugpy) cobrem C, C++, Go e Python, permitindo que o Mestre de Estaleiro Digital inspecione qualquer equipamento do estaleiro com precisão cirúrgica.

O mais importante não é apenas a quantidade de operações, mas a integração: o agente não precisa que você abra um IDE separado, configure um plugin ou copie cole comandos. Tudo acontece dentro do fluxo do OMP.

No próximo capítulo, vamos expandir ainda mais o poder do estaleiro: Subagentes. Você aprenderá a dividir trabalho complexo entre workers paralelos, cada um com seu próprio contexto e resultados tipados.

Acesse a documentação completa: https://omp.sh/docs

Siga-nous nas redes sociais para dicas, tutoriais e novidades sobre o Oh My Pi.
