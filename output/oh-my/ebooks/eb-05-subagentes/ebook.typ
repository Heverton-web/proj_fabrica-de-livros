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
  title: "Subagentes: Fan-out Paralelo de Tarefas & O Advisor Model: Um Revisor a Cada Turno",
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
      align(center, "Subagentes: Fan-out Paralelo de Tarefas & O Advisor Model: Um Revisor a Cada Turno")
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
      #text(font: ("Inter", "Liberation Sans", "Arial"), size: 34pt, weight: "bold", fill: white)[Subagentes: Fan-out Paralelo de Tarefas & O Advisor Model: Um Revisor a Cada Turno]
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
    #text(font: ("Inter", "Liberation Sans", "Arial"), size: 22pt, weight: "bold", fill: cor.primaria)[Subagentes: Fan-out Paralelo de Tarefas & O Advisor Model: Um Revisor a Cada Turno]
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
= Subagentes: Fan-out Paralelo de Tarefas
<subagentes-fan-out-paralelo-de-tarefas>
== Escalando para múltiplos workers
<escalando-para-múltiplos-workers>
No capítulo anterior, você dominou o debug com DAP --- 28 operações que transformam o agente em um debugger autônomo capaz de pausar processos, inspecionar variáveis e corrigir bugs na raiz.

Agora vamos escalar: em vez de um único agente fazendo tudo sequencialmente, vamos lançar múltiplos workers em paralelo --- cada um isolado, com sua própria memória e resultado tipado.

== O que são subagentes e por que existem
<o-que-são-subagentes-e-por-que-existem>
Quando você trabalha com um coding agent sozinho, existe um limite natural de produtividade: o agente pode fazer apenas uma coisa por vez. Se sua tarefa requer analisar 50 arquivos de código, revisar 10 pull requests ou migrar um projeto inteiro de uma framework para outro, um único agente vai levar tempo demais --- e o contexto dele vai encher antes de terminar.

Subagentes resolvem esse problema dividindo o trabalho. Cada subagente é um worker isolado que recebe uma tarefa específica, executa de forma autônoma e retorna um resultado tipado.

É como transformar um único estaleiro com um único operador em um estaleiro com múltiplas equipes especializadas trabalhando em paralelo.

== O sistema de tasks do OMP
<o-sistema-de-tasks-do-omp>
O OMP implementa subagentes através da ferramenta `task`, que suporta três operações principais.

#strong[create] --- cria uma nova tarefa com um ID único (T1, T2, T3…) e um resumo do que precisa ser feito.

#strong[spawn] --- lança um subagente para executar a tarefa, que roda em background e retorna um actor\_id.

#strong[collect] --- aguarda o resultado do subagente e valida seu output contra um schema.

A hierarquia de tasks permite criar estruturas complexas: uma tarefa pai pode ter múltiplas subtarefas (T1.1, T1.2, T1.3), cada uma com seu próprio subagente. Essa é a base do fan-out paralelo --- lançar vários workers simultaneamente para cobrir diferentes aspectos de um problema.

== Schema validation: resultados tipados
<schema-validation-resultados-tipados>
Uma das features mais poderosas do sistema é a validação de schema. Quando você cria uma task, pode definir um `output_schema` que especifica exatamente quais campos o subagente deve retornar.

Isso garante que cada subagente retorna exatamente o que foi pedido, erros de formato são detectados antes de você processar o resultado, e múltiplos subagentes podem ser comparados diretamente porque seguem o mesmo formato.

É como se cada equipe do estaleiro tivesse um formulário padrão de reporte. Sem essa padronização, você teria que interpretar relatórios livres de cada especialista.

== O Agent Hub: painel de controle central
<o-agent-hub-painel-de-controle-central>
Enquanto os subagentes trabalham em paralelo, o Agent Hub fornece visibilidade total sobre o que está acontecendo. Você pode ver quais subagentes estão rodando, pendentes ou completados, monitorar o progresso de cada um em tempo real, cancelar subagentes que estão demorando ou falhando, e ajustar timeouts e limits de recursos.

O Agent Hub é o equivalente ao painel de controle do estaleiro --- onde o mestre vê todas as equipes trabalhando e pode intervir quando necessário.

== O ciclo de vida de uma task
<o-ciclo-de-vida-de-uma-task>
Cada task passa por um ciclo de vida bem definido. Ela começa como `open`, vai para `in_progress` quando um worker é spawned, e pode terminar como `done` ou `failed`. Se uma tarefa depender de outra, ela fica `blocked` até a dependência ser resolvida.

Esse ciclo garante que você sempre saiba o estado de cada tarefa. Se um worker falhar, a task volta para `open` e pode ser retomada.

== Fan-out/Fan-in: o padrão clássico
<fan-outfan-in-o-padrão-clássico>
O padrão mais comum de subagentes é o fan-out/fan-in.

Primeiro, você distribui uma tarefa grande entre múltiplos workers --- por exemplo, revisar 10 arquivos diferentes. Depois, cada worker processa sua parte independentemente. Por fim, você coleta todos os resultados e os consolida.

É como um estaleiro que distribui a construção do navio entre equipes especializadas --- cada uma monta sua parte em paralelo, e no final todas as peças se encaixam perfeitamente porque seguem o mesmo schema de fabricação.

== Criando sua primeira task
<criando-sua-primeira-task>
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

== Spawning um subagente
<spawning-um-subagente>
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

== Fan-out com múltiplos workers
<fan-out-com-múltiplos-workers>
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

== Collecting resultados
<collecting-resultados>
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

== Caso de uso: code review paralelo
<caso-de-uso-code-review-paralelo>
Imagine que você tem um pull request com 10 arquivos modificados e precisa revisar todos antes de mergear. Em vez de revisar sequencialmente (o que levaria 30+ minutos), você distribui entre 5 workers.

Em vez de 30 minutos sequenciais, você resolve em 5 minutos paralelos --- 6x mais rápido.

== Caso de uso: migração de framework
<caso-de-uso-migração-de-framework>
Migrar um projeto de uma framework para outra é trabalhoso e propenso a erros. Subagentes tornam isso gerenciável.

Cada worker opera isolado em seu módulo --- não há conflitos de edição porque cada um trabalha em arquivos diferentes.

== Caso de uso: refactoring distribuído
<caso-de-uso-refactoring-distribuído>
Refactoring em grande escala pode ser assustador. Subagentes permitem dividir o trabalho entre especialistas.

Cada worker foca em um tipo específico de melhoria --- type hints, logging, testes --- e todos trabalham em paralelo sem conflitos.

== Próximos Passos
<próximos-passos>
Neste capítulo, você aprendeu a transformar um único agente em uma equipe inteira de workers paralelos. O sistema de subagentes do OMP oferece três capacidades fundamentais.

Fan-out com schema validation: você distribui trabalho entre múltiplos workers, cada um retornando resultados tipados que garantem consistência e facilitam consolidação.

Agent Hub para monitoramento ao vivo: você mantém visibilidade total sobre seus subagentes --- sabendo quando intervenir, quando cancelar e quando coletar resultados.

Padrões de uso prático: code review paralelo, migração de framework e refactoring distribuído são apenas alguns dos casos de uso que se beneficiam do fan-out paralelo.

No próximo capítulo, veremos como o Advisor Model funciona como um revisor a cada turno --- um segundo olhar que garante qualidade antes que cada peça seja montada no casco.

Acesse a documentação completa: https:/\/omp.sh/docs

Siga-nous nas redes sociais para dicas, tutoriais e novidades sobre o Oh My Pi.

#horizontalrule

= O Advisor Model: Um Revisor a Cada Turno
<o-advisor-model-um-revisor-a-cada-turno>
== O inspetor de casco digital
<o-inspetor-de-casco-digital>
No capítulo anterior, você dominou sub-agentes: aprendeu a criar tarefas com `task`, a spawnar workers, a coordenar execução paralela e a construir workflows completos. O agente agora delega --- mas delegar tarefas não é o mesmo que receber feedback sobre seu próprio trabalho.

Existe uma diferença fundamental entre dizer "faça isso para mim" e ouvir "olha, o que você fez tem um problema aqui". O advisor model é exatamente essa segunda capacidade: um segundo modelo LLM que observa cada turno do agente principal e emite notas qualificadas sobre a qualidade, segurança e coerência do que está sendo produzido.

== O que é um Advisor Model
<o-que-é-um-advisor-model>
Um advisor model é um segundo LLM configurado especificamente para revisar o trabalho do agente principal. Enquanto o agente principal foca em executar tarefas (ler código, editar arquivos, rodar comandos), o advisor foca em avaliar a qualidade, segurança e coerência do que está sendo feito.

A mecânica é simples: a cada turno, o agente principal envia seu contexto atual para o advisor. O advisor analisa esse contexto e retorna notas estruturadas --- preocupações (concerns), bloqueios (blockers) ou sugestões (suggestions). O agente principal então decide se incorpora essas notas ao seu trabalho ou as descarta.

Essa separação de papéis é fundamental. O agente principal é o operário do estaleiro --- ele constrói, edita, executa. O advisor é o inspetor --- ele verifica, aponta, recomenda. Nenhum dos dois faz o trabalho do outro.

== Como o advisor observa e injeta notas
<como-o-advisor-observa-e-injeta-notas>
O advisor recebe três tipos de informação: o histórico de turnos (o que o agente já fez), o plano atual (o que o agente vai fazer agora) e o código afetado (os arquivos que serão modificados). Com base nesses dados, o advisor emite notas em formato estruturado.

#strong[Concern] (preocupação): algo que não bloqueia a execução, mas que merece atenção. Exemplo: "A função `processar_pedido` não valida entrada --- pode causar bugs em dados inválidos". O agente pode decidir corrigir agora ou registrar para depois.

#strong[Blocker] (bloqueio): algo que impede a continuação segura. Exemplo: "Este comando vai deletar o arquivo de configuração de produção". O agente DEVE parar e resolver o blocker antes de prosseguir.

#strong[Suggestion] (sugestão): melhoria opcional que aumenta qualidade. Exemplo: "Considere adicionar um try/except aqui --- esta operação pode falhar em rede instável". O agente decide se incorpora.

== Configuração de modelo advisor separado
<configuração-de-modelo-advisor-separado>
A escolha do modelo advisor é estratégica. O advisor precisa de três características que o agente principal pode não ter: foco em análise crítica, conhecimento de padrões de segurança e qualidade, e capacidade de emitir julgamentos concisos.

Um modelo grande e geral (como Claude Opus ou GPT-4o) funciona bem como agente principal, mas um modelo menor e mais focado (como Claude Haiku ou GPT-4o-mini) pode ser mais eficiente como advisor --- porque o advisor não precisa gerar código, apenas avaliar.

== Protocolo de decisão
<protocolo-de-decisão>
A integração entre agente principal e advisor segue um protocolo definido. O agente não é obrigado a obedecer ao advisor --- ele é obrigado a CONSIDERAR o que o advisor diz. Essa distinção é crucial: o advisor é um consultor, não um comandante.

O protocolo de decisão funciona assim.

#strong[Blocker recebido:] o agente PARA. Analisa o blocker. Se concorda, corrige o problema. Se discorda, registra a justificativa e continua --- mas o registro fica no log para auditoria futura.

#strong[Concern recebido:] o agente ANOTA. Continua trabalhando, mas mantém o concern em mente. Pode resolver agora ou deixar para depois --- dependendo da prioridade.

#strong[Suggestion recebida:] o agente AVALIA. Se a suggestion melhora significativamente o código, incorpora. Se não, ignora. Não há obrigação de aceitar suggestions.

O valor do advisor não está em impedir erros --- está em REDUZIR a taxa de erros que passam despercebidos. Estudos mostram que agentes com advisor reduzem bugs de segurança em 40-60% comparados a agentes sem revisão.

== A metáfora do estaleiro
<a-metáfora-do-estaleiro>
Imagine seu estaleiro digital. Você é o Mestre de Estaleiro --- responsável por construir navios. Cada navio tem um casco, um motor, equipamento de navegação e uma tripulação. Você coordena tudo, toma decisões rápidas, ajusta rotas quando necessário.

Mas existe um problema: quando você está construindo o casco, suas mãos estão ocupadas soldando. Quando está calibrando o motor, seus olhos estão no gauge de pressão. Você não consegue, ao mesmo tempo, CONSTRUIR e VERIFICAR.

É aí que entra o inspetor de casco --- o advisor model. O inspetor não solda, não calibra, não navega. Ele anda pelo estaleiro, examina cada trabalho que você faz e aponta: "essa solda está fraca", "essa viga está torta", "esse cabo está solto". Você decide se para para corrigir ou continua --- mas o inspetor garante que você SABE dos problemas antes de zarpar.

== Configurando seu primeiro advisor model
<configurando-seu-primeiro-advisor-model>
Para configurar um advisor model no Oh My Pi, você precisa de dois arquivos: a configuração do modelo advisor e o hook que integra o advisor ao fluxo do agente principal.

```yaml
# Arquivo: .ohmypi/advisor-config.yaml

advisor:
  model: "claude-haiku-4-20250414"
  temperature: 0.1
  
  system_prompt: |
    Você é um revisor de código especializado em segurança e qualidade.
    Sua única tarefa é analisar ações do agente e emitir notas estruturadas.
    
    Regras:
    - SEMPRE emite BLOCKER quando detectar risco de segurança
    - SEMPRE emite BLOCKER quando detectar destruição de dados
    - Emite CONCERN quando detectar violação de padrão
    - Emite SUGGESTION quando detectar melhoria significativa
    - NÃO emite nota para estilo ou formatação
  
  thresholds:
    blocker: 0.9
    concern: 0.7
    suggestion: 0.5
```

== Integração com o agente principal
<integração-com-o-agente-principal>
A integração usa o hook `pre_tool_call` do Oh My Pi. O hook intercepta cada chamada de ferramenta antes que ela seja executada, envia o contexto para o advisor e processa a nota recebida.

```python
@hook("pre_tool_call")
def advisor_hook(tool_name: str, arguments: dict, context: dict) -> dict:
    advisor_context = {
        "turno": context.get("turn_count", 0),
        "ferramenta": tool_name,
        "argumentos": arguments,
        "codigo_afetado": context.get("affected_files", []),
        "plano": context.get("current_plan", "N/A")
    }
    
    resultado = call_model(
        model="claude-haiku-4-20250414",
        prompt=advisor_prompt,
        temperature=0.1
    )
    
    nota = json.loads(resultado.get("content", '{"tipo": "ok"}'))
    
    if nota["tipo"] == "blocker":
        return {"action": "deny", "reason": f"Advisor bloqueou: {nota['mensagem']}"}
    elif nota["tipo"] == "concern":
        context.setdefault("advisor_concerns", []).append(nota)
        return {"action": "allow", "advisor_note": nota}
    else:
        return {"action": "allow"}
```

== A cena de contraste
<a-cena-de-contraste>
Imagine que você está desenvolvendo uma API de e-commerce. O agente principal está criando a rota de checkout --- uma das partes mais críticas do sistema.

Sem advisor, o agente gera o código rapidamente: uma função que recebe o pedido, debita o estoque, cobra o cartão e envia o e-mail de confirmação. O código funciona nos testes. Você faz deploy. Na primeira compra real, o cartão é cobrado, mas o estoque não é debitado --- porque o agente esqueceu de colocar a operação dentro de uma transação atômica.

Agora imagine o mesmo cenário COM advisor. O agente gera a mesma função. Antes de executar, o advisor analisa e emite um blocker: "A operação de débito de estoque e cobrança do cartão não está em uma transação atômica. Se uma falhar, a outra fica órfã." O agente para, analisa o blocker, concorda e envolve a operação em uma transação bancária. O bug é pego ANTES do deploy.

A diferença não é o código gerado --- é o MOMENTO em que o problema é detectado. Sem advisor, o bug aparece em produção. Com advisor, o bug aparece no estaleiro, quando ainda é barato corrigir.

== Armadilhas comuns do advisor model
<armadilhas-comuns-do-advisor-model>
#strong[Confundir advisor com substituto humano.] O advisor é uma camada adicional de defesa, não uma garantia. Ele reduz a taxa de erros, não a elimina.

#strong[Ignorar o advisor quando ele discorda.] Se você ignora todos os blockers do advisor, por que configurou um advisor?

#strong[Não ter plano B.] Quando o advisor trava (modelo indisponível, timeout), o agente precisa continuar funcionando, não parar tudo.

#strong[Configurar o advisor errado.] Um advisor com regras muito restritivas bloqueia tudo; um advisor com regras muito permissivas não detecta nada. A calibração é chave.

== Métricas de sucesso com advisor
<métricas-de-sucesso-com-advisor>
Um time que usa advisor model se mede por quatro indicadores.

#strong[Taxa de bloqueios por advisor] --- quantas vezes o advisor bloqueou uma ação perigosa (meta: 5-15% das ações).

#strong[Tempo médio de resolução de blocker] --- quanto tempo o agente leva para resolver um blocker (meta: \< 2 turnos).

#strong[Redução de bugs em produção] --- comparar antes e depois do advisor (meta: 30-50% de redução).

#strong[Custo do advisor] --- tokens consumidos pelo advisor em relação ao agente principal (meta: \< 20% do custo total).

== Próximos Passos
<próximos-passos-1>
Neste capítulo, você adicionou uma camada fundamental de qualidade ao seu agente: o advisor model. Entendeu como o advisor observa cada turno e emite notas estruturadas --- concerns, blockers e suggestions. Configurou um modelo advisor separado com system prompt especializado e thresholds de confiança. E dominou o protocolo de decisão --- quando obedecer ao advisor, quando discordar, quando escalar.

O advisor model não é um luxo --- é uma necessidade em projetos que usam agentes autônomos. Um agente sem advisor é como um navio sem inspetor de casco: pode zarpar, mas não há garantia de que vai chegar ao porto.

No próximo capítulo, vamos trazer um colega sentado ao seu lado no estaleiro digital: colaboração ao vivo com /collab.

Acesse a documentação completa: https:/\/omp.sh/docs

Siga-nous nas redes sociais para dicas, tutoriais e novidades sobre o Oh My Pi.

#horizontalrule

// ── CONTRACAPA ────────────────────────────────────────────────────
#pagebreak()
