# Capítulo 9: Economia Severa de Tokens: Caveman, RTK-Memory, Lean-CTX e Headroom

## 1. Introdução

No Capítulo 8 você blindou os Guindastes do Cais por fora — schema como manual de operação, e três anteparas contra um manual adulterado por sabotagem. Seu estaleiro agora resiste a ataque. Mas um estaleiro pode estar perfeitamente seguro e ainda assim afundar por um motivo mais silencioso: falta de combustível, ou pior, combustível queimado sem necessidade. É disso que trata este capítulo.

Todo guindaste que opera, todo oficial de rota que decide, toda tripulação que investiga um problema — tudo isso consome o mesmo recurso finito: tokens. Como Engenheiro Agêntico, você já aprendeu a proteger seu estaleiro de sabotagem externa. Agora você aprende a protegê-lo de si mesmo, da própria voracidade de um agente que lê mais do que precisa, busca do jeito mais caro possível e esquece no turno seguinte o que descobriu com esforço no turno anterior. Dominar essa disciplina é o que separa a operação que escala de forma sustentável da que definha sob a própria fatura.

## 2. Explica

Em qualquer fluxo de agente que se estende por múltiplos turnos — exploração de código, investigação de um bug, orquestração de subagentes — existe um fato que a maioria dos operadores subestima: o processamento de contexto, não a geração da resposta final, domina o custo total da operação [1]. Cada arquivo lido, cada saída de ferramenta despejada de volta na janela, cada resultado de busca intermediário é combustível que o modelo precisa processar e sobre o qual precisa raciocinar antes de chegar à próxima decisão — e esse combustível é cobrado independentemente de ter sido útil ou não [2].

Esse é o fundamento por trás do princípio de *context engineering*: tratar o gerenciamento da janela de contexto como disciplina de engenharia central, não como detalhe de implementação. Na prática, isso se materializa em algumas técnicas complementares. Retrieval ranqueado e filtragem de distintividade semântica selecionam apenas os poucos trechos mais relevantes para uma tarefa específica, descartando redundância entre documentos que dizem a mesma coisa de formas diferentes [3]. *Few-shot* dinâmico trata exemplos como dados recuperáveis, escolhendo apenas os mais similares à consulta atual em vez de anexar um catálogo fixo de exemplos a cada chamada [4]. E quando, ainda assim, o histórico de uma sessão longa se aproxima do limite da janela, entra em cena a *compaction*: o histórico de conversa e tarefa é sumarizado, preservando decisões críticas e descartando saídas de ferramenta redundantes e raciocínio já superado — a mesma abordagem que a própria equipe de engenharia por trás do Claude Code usa internamente em sessões longas de codificação [5].

Vale registrar que essa não é uma preocupação apenas prática — há um corpo crescente de pesquisa formalizando o problema. O framework *SkillReducer* propõe otimizar explicitamente as *skills* de agentes LLM para eficiência de token, tratando a economia de contexto como parte do próprio design da skill, não como otimização posterior [6]. Na mesma direção, "The Efficiency Frontier" formaliza um framework unificado de otimização custo-desempenho para gerenciamento de contexto em LLMs, situando *compaction*, retrieval seletivo e compressão de saída como pontos de uma mesma curva de trade-off entre precisão e custo [7]. Um estudo anterior sobre otimização de custos de uso de LLM já havia mapeado a mesma tensão: mais contexto quase sempre melhora a qualidade da resposta, até o ponto em que o ganho marginal deixa de compensar o custo marginal — e esse ponto de virada chega muito antes do limite físico da janela [8]. Vale um contraponto que a disciplina de economia de tokens não pode ignorar: cortar contexto agressivamente demais também tem custo, só que ele aparece depois, não no momento da chamada. Um agente que recebe menos contexto do que precisa não fica "mais barato" — fica mal-informado, e um agente mal-informado tende a errar a primeira tentativa, gerar uma segunda rodada de investigação para compensar a lacuna, e terminar consumindo mais tokens no total do que teria consumido se o contexto certo tivesse sido fornecido de uma vez. A meta nunca é o menor contexto possível; é o contexto mínimo suficiente para a tarefa específica — um alvo que se desloca conforme a complexidade da tarefa muda, e que nenhuma regra fixa de corte substitui por completo. Documentação de infraestrutura de produção reforça o efeito colateral concreto de ignorar esse ponto: janelas de contexto estouradas não falham graciosamente, elas produzem respostas truncadas, erros silenciosos de aplicação e, em pipelines de agente, decisões tomadas sobre um histórico incompleto sem que nada avise o operador [9]. Guias práticos de gerenciamento de contexto para aplicações de LLM em produção convergem para a mesma recomendação central: instrumentar o ponto de estouro antes que ele aconteça, não depois [10]. A própria *compaction* carrega um risco simétrico ao do porão que transborda: comprimir cedo demais, ou de forma grosseira demais, pode descartar um detalhe que só se revela importante turnos depois — um valor específico de configuração, uma decisão de arquitetura mencionada de passagem, um número de versão citado uma única vez. É por isso que a distinção entre turno `critico` e turno descartável não pode ser deixada para uma heurística vaga de "resumir tudo que parece repetitivo": ela precisa ser uma decisão explícita, tomada no momento em que o fato entra no porão, não recuperada às cegas no momento em que a válvula de compaction já está prestes a agir.

Essa disciplina deixa de ser opcional no momento em que o estaleiro passa a operar vários guindastes em paralelo — quando um Orquestrador Mestre despacha um lote de subagentes para trabalhar simultaneamente em partes distintas do casco, o mesmo desperdício de contexto que era incômodo em uma sessão única se multiplica pelo número de tripulações trabalhando ao mesmo tempo [16]. A orientação corrente para orquestração de subagentes em escala trata justamente essa multiplicação de custo como o principal risco de operar em lotes, não a coordenação em si [17]. Guias de produção sobre subagentes convergem para a mesma prioridade: cada subagente do lote deve carregar apenas o contexto mínimo da sua própria tarefa, nunca o histórico completo do Orquestrador [18], e relatos de operação em escala mostram que o ganho de paralelismo desaparece rapidamente se cada tripulação do lote reabrir o mesmo porão de arquivos que a anterior já vasculhou [19]. Isso não significa que lotear sempre em mais subagentes seja a resposta certa: cada subagente adicional soma seu próprio custo fixo de inicialização de contexto — instruções do sistema, ferramentas disponíveis, formato de retorno esperado — antes mesmo de tocar na tarefa real, e um lote grande demais para uma tarefa pequena demais paga esse custo fixo várias vezes sem ganho proporcional de paralelismo. A pergunta correta nunca é "quantos subagentes o estaleiro consegue despachar de uma vez", é "quantos capítulos independentes o lote realmente tem para dividir sem que a coordenação entre eles custe mais do que economiza" — o mesmo cálculo de custo-benefício que já apareceu na escolha entre Oficina A e Oficina B do capítulo anterior, agora aplicado à granularidade do próprio lote de trabalho, não à granularidade de uma tool isolada. É por isso que a economia severa de tokens não vive apenas na disciplina individual de um agente — ela também pode e deve ser aplicada automaticamente, via configuração persistente do harness (`settings.json`) e via *hooks* que disparam compressão ou bloqueiam leitura redundante em pontos fixos do ciclo de execução, sem depender da lembrança do operador a cada sessão [20]. Documentação de referência sobre hooks do Claude Code descreve exatamente esse papel: regras determinísticas acopladas a eventos do ciclo de vida do agente, aplicadas de forma consistente independentemente de quem está operando a tripulação naquele turno [21]. Guias abrangentes de configuração do harness reforçam o mesmo princípio de fábrica: a disciplina que funciona só quando o operador se lembra de aplicá-la não escala — a que é fixada em configuração e hook, escala [22].

Um último ponto de nuance fecha a Explica: economia severa de tokens não é uma métrica única a maximizar, é um portfólio de quatro disciplinas complementares, cada uma cobrindo uma fase diferente do ciclo do combustível. Compaction atua sobre o que já está no porão, decidindo o que permanece e o que é resumido [3]; retrieval seletivo e filtragem de redundância semântica trabalham lado a lado com ela, reduzindo o que entra no resumo antes mesmo de ele ser gerado [5]. Lean-ctx atua antes disso, na admissão: decide o que sequer entra no porão, preferindo o sonar barato do grep à leitura cara de arquivo inteiro sempre que a tarefa permitir [12], reservando o instrumento mais caro — busca semântica, LSP — para o resíduo de casos que realmente exigem precisão cirúrgica [15]. Headroom atua na saída do outro lado do pipeline, comprimindo o que a tripulação devolve à Ponte de Comando depois de executar um comando, para que um log de quatrocentas linhas não vire, ele mesmo, um novo barril de lastro morto [2]. E caveman, por fim, atua na própria comunicação entre tripulação e Oficial de Rota — cada instrução, cada relatório de status, cada confirmação de tarefa concluída consome tokens que competem pelo mesmo porão, e reduzir esse volume sem perder precisão técnica libera espaço que, de outra forma, seria ocupado por cortesia verbal sem função [6]. Tratar essas quatro disciplinas como intercambiáveis — "já fiz compaction, não preciso de mais nada" — é o erro mais comum de quem aplica economia de tokens pela metade: elas atuam em pontos diferentes do mesmo pipeline, e a ausência de qualquer uma deixa uma fresta por onde o desperdício volta a entrar. Um estaleiro maduro nesta disciplina não escolhe uma técnica favorita; instrumenta as quatro, cada uma no ponto do pipeline onde ela é mais barata de aplicar [7], e revisita periodicamente se alguma delas ficou desatualizada em relação ao volume real de tráfego que o harness processa em produção, ajustando limiares de compaction e regras de hook antes que o desperdício volte a se acumular silenciosamente [20]. Nenhuma dessas quatro disciplinas exige reescrever o harness do zero — todas cabem como configuração incremental sobre o que o estaleiro já tem instalado, o que é, na prática, o maior argumento a favor de adotá-las cedo em vez de esperar a primeira fatura de token que doer o suficiente para justificar a mudança — cedo é sempre mais barato do que depois, e o depois sempre chega mais rápido do que o estaleiro espera.

## 3. Ilustra

### O Porão de Combustível do Estaleiro

Pense na janela de contexto como o porão de combustível do seu estaleiro. Cada leitura de arquivo, cada saída de comando, cada resultado de busca que sobe da Sala de Máquinas para a Ponte de Comando é um barril despejado nesse porão. O porão tem um medidor de nível visível — e, diferente de um tanque de combustível comum, aqui todo litro carregado já foi pago no momento em que entrou, esteja ele sendo usado ou apenas ocupando espaço como lastro morto. Quando o medidor se aproxima da linha vermelha, uma válvula de compactação entra em ação: em vez de deixar o porão transbordar, ela drena o conteúdo bruto para um barril concentrado — um resumo que preserva as decisões que importam e descarta o que já foi processado e superado.

```mermaid
%% legenda: Porao de combustivel do estaleiro enchendo a cada leitura ate a valvula de compaction agir
flowchart TB
  A[Leitura de arquivo] --> T[Tanque de contexto]
  B[Saida de ferramenta] --> T
  C[Resultado de busca] --> T
  T --> M{Medidor perto da linha vermelha?}
  M -->|nao| T
  M -->|sim| V[Valvula de compaction]
  V --> R[Barril concentrado: resumo da sessao]
  R --> T
```

Esse é o ponto mais denso do capítulo, e merece uma segunda imagem para o detalhe que costuma escapar mesmo a quem já entende o princípio geral: o custo de um litro de combustível não é uniforme. Um barril despejado no porão logo no início do turno, quando a tripulação ainda vai raciocinar sobre ele dez vezes ao longo da investigação, tem um custo por uso muito menor do que um barril despejado por engano — um arquivo lido inteiro quando bastava uma linha, um log de 400 linhas quando bastavam sete. O segundo barril paga o mesmo preço de admissão no porão, mas devolve zero valor de raciocínio. É esse segundo tipo de barril que a disciplina de economia de tokens existe para eliminar antes que ele sequer entre no porão — e é exatamente o assunto do próximo pilar. A implicação prática é que dois estaleiros podem gastar exatamente o mesmo número de tokens numa mesma tarefa e ainda assim ter desempenhos muito diferentes: o que separa um do outro não é o volume total de combustível queimado, é a proporção de barris de alto valor — aqueles que efetivamente mudaram uma decisão — dentro desse total. Medir apenas "quantos tokens a sessão consumiu" esconde essa proporção; medir "quantos desses tokens sustentaram uma decisão real" é a métrica que importa, ainda que seja mais difícil de instrumentar automaticamente do que um simples contador de uso.

### Vários Porões, Um Mesmo Estaleiro: o Custo que se Multiplica em Lote

Quando o Orquestrador Mestre despacha um lote de tripulações para trabalhar em paralelo — cada uma em seu próprio guindaste, seu próprio compartimento do casco — cada tripulação chega com o porão vazio e precisa reabastecer sozinha os fatos básicos que qualquer trabalho no estaleiro exige: onde fica a Ponte de Comando, quais ferramentas estão disponíveis, qual é o formato esperado do relatório final. Se quatro tripulações trabalham ao mesmo tempo e cada uma reabastece esse mesmo lastro básico do zero, o estaleiro paga quatro vezes por um combustível que poderia ter sido carregado uma única vez e compartilhado. Pior ainda: se a primeira tripulação já vasculhou um compartimento do casco em busca de um padrão e não deixou registro no diário de bordo, a segunda tripulação do mesmo lote pode reabrir exatamente o mesmo compartimento sem saber que o trabalho já foi feito — o paralelismo, nesse caso, não multiplica a velocidade do estaleiro, multiplica o desperdício.

```mermaid
%% legenda: Quatro tripulacoes em lote reabastecendo o mesmo lastro basico sem memoria compartilhada
flowchart TB
  O[Orquestrador Mestre despacha o lote] --> T1[Tripulacao 1: porao vazio]
  O --> T2[Tripulacao 2: porao vazio]
  O --> T3[Tripulacao 3: porao vazio]
  O --> T4[Tripulacao 4: porao vazio]
  T1 --> L1[Reabastece lastro basico do zero]
  T2 --> L2[Reabastece o mesmo lastro basico do zero]
  T3 --> L3[Reabastece o mesmo lastro basico do zero]
  T4 --> L4[Reabastece o mesmo lastro basico do zero]
  L1 --> D[Diario de bordo compartilhado evita a repeticao na proxima rodada]
  L2 --> D
  L3 --> D
  L4 --> D
```

## 4. Técnica

Esta seção fabrica, em código, os três instrumentos que colocam a economia de contexto em prática dentro do estaleiro: um medidor de combustível com válvula de compaction automática, um pipeline de busca que varre o porão antes de abrir qualquer compartimento, e o diário de bordo que impede a tripulação de redescobrir o mesmo erro em todo turno.

### O Medidor de Combustível e a Válvula de Compaction

O primeiro artefato estima o consumo de tokens de um histórico de sessão e decide, de forma determinística, quando disparar a compactação — sem depender do modelo perceber sozinho que está perto do limite.

```python
from dataclasses import dataclass, field

CARACTERES_POR_TOKEN_APROX = 4
LIMITE_TOKENS_JANELA = 20000
LIMIAR_COMPACTACAO = 0.75  # dispara compaction ao atingir 75% da janela


@dataclass
class TurnoSessao:
    origem: str          # ex.: "leitura_arquivo", "saida_ferramenta", "raciocinio"
    conteudo: str
    critico: bool = False  # decisao/fato que a compaction nao pode descartar


@dataclass
class MedidorDeCombustivel:
    historico: list = field(default_factory=list)

    def registrar(self, turno: TurnoSessao) -> None:
        self.historico.append(turno)

    def tokens_estimados(self) -> int:
        total_caracteres = sum(len(t.conteudo) for t in self.historico)
        return total_caracteres // CARACTERES_POR_TOKEN_APROX

    def nivel_do_medidor(self) -> float:
        return self.tokens_estimados() / LIMITE_TOKENS_JANELA

    def precisa_compactar(self) -> bool:
        return self.nivel_do_medidor() >= LIMIAR_COMPACTACAO

    def compactar(self) -> str:
        """Drena o porao: mantem turnos criticos, resume o resto em uma linha."""
        criticos = [t.conteudo for t in self.historico if t.critico]
        descartaveis = len(self.historico) - len(criticos)
        resumo = (
            f"[Compaction aplicada: {descartaveis} turnos nao-criticos condensados] "
            + " | ".join(criticos)
        )
        self.historico = [TurnoSessao(origem="compaction", conteudo=resumo, critico=True)]
        return resumo


if __name__ == "__main__":
    medidor = MedidorDeCombustivel()
    medidor.registrar(TurnoSessao("leitura_arquivo", "conteudo grande de log " * 500))
    medidor.registrar(TurnoSessao("raciocinio", "decisao: usar cache semantico", critico=True))
    if medidor.precisa_compactar():
        print(medidor.compactar())
```

Note que `critico=True` é uma decisão explícita de arquitetura, não uma heurística do modelo — o barril de decisão ("usar cache semântico") sobrevive à drenagem, o log bruto de 500 repetições não [11]. Esse é o mesmo espírito da *compaction* descrita na seção Explica: perder o registro literal, nunca perder o fato que orienta a próxima decisão [5].

### Grep Antes de Read: Varrendo o Porão com o Sonar Antes do Bisturi

O segundo artefato demonstra o pipeline lean-ctx na prática: uma varredura ampla e barata (grep/ripgrep) antes de qualquer leitura completa de arquivo — reservando a leitura integral, o instrumento caro, apenas para o candidato que a varredura já apontou como mais provável.

```bash
#!/usr/bin/env bash
# lean-ctx: varre o porao (grep) antes de abrir qualquer compartimento (read)
set -euo pipefail

TERMO_BUSCA="$1"
DIRETORIO="${2:-.}"

echo "Fase 1 - sonar de largo espectro (ripgrep, so nomes de arquivo e linha):"
CANDIDATOS=$(rg --files-with-matches --ignore-case "$TERMO_BUSCA" "$DIRETORIO" || true)

if [ -z "$CANDIDATOS" ]; then
  echo "Nenhum candidato encontrado no porao. Encerrando sem leitura completa."
  exit 0
fi

echo "Candidatos localizados pelo sonar:"
echo "$CANDIDATOS"

MELHOR_CANDIDATO=$(echo "$CANDIDATOS" | head -n 1)
echo ""
echo "Fase 2 - bisturi de precisao (read completo, so no melhor candidato):"
echo "Abrindo compartimento: $MELHOR_CANDIDATO"
grep -n "$TERMO_BUSCA" "$MELHOR_CANDIDATO"
```

Vale um contraponto: grep não é infalível, e tratá-lo como sonar universal seria trocar um exagero pelo outro. Uma busca textual não encontra uma função renomeada por sinônimo semântico, não segue um alias de importação, e não entende que duas strings diferentes descrevem o mesmo conceito de negócio — é exatamente aí que uma camada de busca semântica ou o LSP entram como complemento, nunca como primeira tentativa. A disciplina lean-ctx não escolhe grep por dogma; escolhe grep primeiro porque, na distribuição real de tarefas de exploração, a maioria das buscas tem uma pista textual literal suficiente, e reservar a ferramenta mais cara para o resíduo de casos que realmente precisam dela é o que mantém o custo médio baixo sem abrir mão de precisão quando ela é necessária.

O porquê disso não é estilístico. Grep retorna um cluster de conceitos — a partir do qual o próprio modelo já infere organização de repositório, convenções de nomenclatura e distribuição de arquivos relacionados — a um custo de token próximo de zero, sem exigir índice vetorial nem etapa de embedding [12]. O LSP (Language Server Protocol) entra depois, como camada de operação de precisão cirúrgica sobre um símbolo já localizado — não como substituto da varredura ampla [13]. É por isso que, mesmo com a maturidade atual de busca semântica, agentes de codificação de produção continuam usando grep como espinha dorsal da fase exploratória [14]. Pesquisa recente que avalia diretamente essa questão chega a uma resposta qualificada: para tarefas de geração de hipótese ampla, grep sozinho já resolve a maior parte do trabalho que buscas semânticas mais caras prometem resolver [15]. A skill `headroom`, por sua vez, aplica o mesmo princípio do outro lado do pipeline — não na busca, mas na leitura: qualquer saída de comando com mais de sete linhas é comprimida, mantendo as três primeiras e as quatro últimas, porque a informação que decide o próximo passo quase sempre mora nas bordas de um output longo, não no meio [2].

### O Diário de Bordo que Impede Retrabalho: RTK-Memory

O terceiro artefato formaliza o schema de uma entrada de diário de bordo no padrão rtk-memory: um registro estruturado de erro/padrão, pronto para ser consultado por um agente futuro sem repetir a investigação do zero.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "EntradaDiarioDeBordoRTK",
  "type": "object",
  "required": ["data", "sintoma", "causa_raiz", "correcao", "arquivos_afetados"],
  "properties": {
    "data": {
      "type": "string",
      "format": "date",
      "description": "Data em que o padrao ou erro foi descoberto pela tripulacao."
    },
    "sintoma": {
      "type": "string",
      "description": "O que foi observado, em termos telegraficos (modo caveman)."
    },
    "causa_raiz": {
      "type": "string",
      "description": "Explicacao direta da causa, sem prosa desnecessaria."
    },
    "correcao": {
      "type": "string",
      "description": "O que resolveu, de forma reaplicavel por outro agente."
    },
    "arquivos_afetados": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Caminhos absolutos tocados pela correcao."
    },
    "reincidencia_evitada": {
      "type": "boolean",
      "default": true,
      "description": "Marca se este registro ja evitou retrabalho em turno posterior."
    }
  }
}
```

Uma entrada real preenchida contra esse schema soa como o próprio modo caveman recomenda: "build quebra em X. causa: import circular. fix: mover Y pra modulo Z. arquivos: a.py, b.py." — nenhuma palavra sobra, nenhum dado falta [16]. É essa combinação — comunicação telegráfica na saída, registro estruturado persistente na memória — que a literatura acadêmica recente sobre eficiência de skills de agente sustenta teoricamente: cortar o supérfluo da comunicação de turno a turno sem cortar o dado que decide a próxima ação [6], e ancorar esse corte em um mecanismo de memória que evita que o custo de descoberta seja pago duas vezes pela mesma causa raiz [7]. Um detalhe de manutenção que costuma ser negligenciado: um diário de bordo que só cresce, sem nunca ser podado, acaba recriando o mesmo problema que resolve — em algum momento, encontrar a entrada certa entre centenas de registros antigos custa quase tanto quanto reinvestigar do zero. A disciplina completa do rtk-memory inclui também arquivar ou consolidar entradas obsoletas (um bug corrigido por uma reescrita posterior, uma causa raiz que deixou de existir porque o módulo inteiro foi substituído), mantendo o diário pequeno o suficiente para ser varrido por um grep rápido, e não ele mesmo virar um novo porão que precisa de compaction.

### Dimensionando o Lote: Quando Mais Tripulações Custam Mais do que Economizam

O quarto artefato formaliza o cálculo informal descrito na Ilustra: uma função que decide, a partir do custo fixo de inicialização por tripulação e do número de tarefas realmente independentes, se vale a pena despachar mais um subagente ou se o lote já passou do ponto em que paralelismo adicional deixa de compensar.

```python
from dataclasses import dataclass

CUSTO_FIXO_INICIALIZACAO_TOKENS = 1500  # lastro basico por tripulacao despachada


@dataclass
class EstimativaLote:
    tarefas_independentes: int
    custo_medio_por_tarefa_tokens: int
    tamanho_lote_proposto: int

    def custo_total_sequencial(self) -> int:
        return self.tarefas_independentes * self.custo_medio_por_tarefa_tokens

    def custo_total_em_lote(self) -> int:
        overhead_lote = self.tamanho_lote_proposto * CUSTO_FIXO_INICIALIZACAO_TOKENS
        return self.custo_total_sequencial() + overhead_lote

    def vale_a_pena_lotear(self) -> bool:
        """Compara o overhead fixo do lote contra o ganho estimado de paralelismo.

        Regra simples e deterministica: lotear so compensa quando o numero de
        tarefas independentes e maior que o tamanho do proprio lote proposto -
        caso contrario, o custo fixo por tripulacao supera qualquer ganho real.
        """
        return self.tarefas_independentes > self.tamanho_lote_proposto


if __name__ == "__main__":
    lote_pequeno_demais = EstimativaLote(
        tarefas_independentes=2, custo_medio_por_tarefa_tokens=8000, tamanho_lote_proposto=4
    )
    print("Vale lotear 4 tripulacoes para 2 tarefas?", lote_pequeno_demais.vale_a_pena_lotear())

    lote_adequado = EstimativaLote(
        tarefas_independentes=12, custo_medio_por_tarefa_tokens=8000, tamanho_lote_proposto=4
    )
    print("Vale lotear 4 tripulacoes para 12 tarefas?", lote_adequado.vale_a_pena_lotear())
```

O primeiro cenário retorna `False`: despachar quatro tripulações para apenas duas tarefas independentes paga o custo fixo de inicialização duas vezes a mais do que o necessário, exatamente o desperdício ilustrado na cena dos quatro porões. O segundo cenário retorna `True`: doze tarefas independentes diluem o mesmo custo fixo por tripulação o suficiente para o paralelismo compensar. Nenhum número aqui é universal — cada estaleiro deve calibrar `CUSTO_FIXO_INICIALIZACAO_TOKENS` contra o próprio harness em uso —, mas o princípio de comparar overhead fixo contra ganho real de paralelismo, em vez de lotear por hábito, é o que a orientação de mercado sobre orquestração de subagentes em escala recomenda como prática permanente [17].

## 5. Aplica

Você está investigando, pela terceira vez neste mês, o mesmo erro de timeout em um deploy — só que da última vez que isso aconteceu, o agente que resolveu o problema simplesmente encerrou a sessão sem deixar rastro do que descobriu. Você abre uma sessão nova, pede para o agente investigar, e ele faz exatamente o que fez nas duas vezes anteriores: lê o arquivo de configuração inteiro, depois o arquivo de deploy inteiro, depois três logs de execução completos, procurando por um padrão que — você vai descobrir de novo, em vinte minutos — está numa única variável de ambiente mal configurada. O porão enche de barris que não geram nenhum litro de raciocínio novo, e você paga a mesma fatura de descoberta pela terceira vez.

O diagnóstico correto não é "o agente raciocinou mal" — o agente fez exatamente o que qualquer busca sem disciplina faria: preferiu ler tudo a arriscar não ler o suficiente. O problema estrutural é que não existia diário de bordo entre a primeira investigação e esta. Some a isso um segundo agravante, mais fácil de não perceber: se essa mesma investigação tivesse sido delegada a um lote de subagentes "para ir mais rápido", sem calcular se havia de fato tarefas independentes o suficiente para justificar o lote, o estaleiro teria pago o custo fixo de inicialização de cada tripulação extra em cima do próprio desperdício de releitura — dois problemas de disciplina se multiplicando em vez de se cancelarem. A correção é dupla e seguindo exatamente os instrumentos da seção Técnica: primeiro, antes de qualquer leitura completa, um grep direcionado no arquivo de configuração pelo nome da variável suspeita — sonar antes de bisturi; segundo, e mais importante, a primeira vez que esse erro for resolvido, uma entrada no diário de bordo no formato rtk-memory registra sintoma, causa raiz e correção, para que a próxima sessão comece consultando o diário em vez de reabrindo o porão inteiro. Como Engenheiro Agêntico, o ponto de controle nunca é "confiar que o próximo agente vai ser mais eficiente" — é garantir que ele nem precise ser, porque o conhecimento já está registrado fora da sessão que o descobriu.

Armadilhas recorrentes na prática de economia de tokens, no mercado:

- Tratar `compaction` como algo que só acontece quando o modelo "decide" resumir, em vez de instrumentar um gatilho determinístico de limiar, como o medidor de combustível construído acima [9].
- Usar busca semântica como primeira e única ferramenta de exploração, pagando custo de embedding e latência onde um grep resolveria com um décimo do custo [15].
- Deixar saídas de comando de centenas de linhas subirem inteiras ao contexto, sem aplicar a compressão de bordas que a skill `headroom` automatiza [2].
- Encerrar uma sessão de investigação sem registrar o padrão descoberto, condenando a próxima sessão a pagar de novo o mesmo custo de descoberta [6].
- Deixar o diário de bordo crescer indefinidamente sem podar entradas obsoletas, até que consultá-lo custe quase tanto quanto reinvestigar do zero — a mesma disciplina de compaction que se aplica ao porão de contexto de uma sessão precisa ser aplicada, periodicamente, à própria memória persistente entre sessões [7].
- Lotear um número fixo de subagentes por hábito, sem calcular se o número de tarefas realmente independentes justifica aquele tamanho de lote — pagando o custo fixo de inicialização de cada tripulação extra sem nenhum ganho proporcional de paralelismo [17].

## 6. Conclusão

Três pontos fecham este capítulo. Primeiro: em qualquer fluxo de agente estendido, o processamento de contexto — não a resposta final — domina o custo, e por isso o porão de combustível precisa de um medidor com gatilho determinístico de compaction, nunca de bom senso esperado do modelo. Segundo: grep antes de busca semântica não é economia de preguiça, é o fundamento técnico correto para exploração ampla — o sonar de largo espectro que barateia tudo o que vem depois, com o LSP reservado para o corte de precisão que ele realmente faz bem. Terceiro, e talvez o mais estratégico a longo prazo: comunicação telegráfica (caveman) e memória persistente de padrões (rtk-memory) não são economia cosmética — são o que impede seu estaleiro de pagar a mesma fatura de descoberta em cada turno, sessão após sessão. Um quarto fio, mais operacional, amarra os três: nenhuma dessas disciplinas se aplica de graça quando o estaleiro passa a despachar tripulações em lote — o mesmo cálculo de custo-benefício que evita desperdício num agente único precisa ser recalculado, explicitamente, toda vez que a unidade de trabalho passa de "um agente investigando" para "N agentes despachados ao mesmo tempo", sob pena de o paralelismo custar mais do que economiza.

Com o combustível sob disciplina, seu estaleiro fecha a Parte IV pronto para o desafio final: a Parte V trata da botadura — o lançamento em produção da embarcação inteira, do zero ao deploy. Vale levar adiante uma última constatação: segurança de ferramenta (Capítulo 8) e economia de contexto (este capítulo) parecem preocupações distintas, mas convergem no mesmo tipo de solução — controles determinísticos, fixados fora do raciocínio do modelo, que não dependem de o modelo "perceber" sozinho nem o ataque nem o desperdício. É esse mesmo padrão de engenharia, aplicado agora ao portão que autoriza a botadura, que fecha o arco da obra no capítulo final.

## 7. Referências Bibliográficas

[1] LUHARUKA, Shubham. *Context Optimization: A Comprehensive Framework for Reducing Large Language Model Token Usage*. Disponível em: https://luharuka.medium.com/context-optimization-a-comprehensive-framework-for-reducing-large-language-model-token-usage-fed8d9229e30. Acesso em: 02 ago. 2026.

[2] AGENTA. *Top techniques to Manage Context Lengths in LLMs*. Disponível em: https://agenta.ai/blog/top-6-techniques-to-manage-context-length-in-llms. Acesso em: 02 ago. 2026.

[3] ANTHROPIC. *Effective context engineering for AI agents*. Disponível em: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents. Acesso em: 02 ago. 2026.

[4] ANTHROPIC. *Agent Skills — Claude Platform Docs*. Disponível em: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview. Acesso em: 02 ago. 2026.

[5] ANTHROPIC. *Effective harnesses for long-running agents*. Disponível em: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents. Acesso em: 02 ago. 2026.

[6] ARXIV.ORG. *SkillReducer: Optimizing LLM Agent Skills for Token Efficiency*. Disponível em: https://arxiv.org/pdf/2603.29919. Acesso em: 02 ago. 2026.

[7] ARXIV.ORG. *The Efficiency Frontier: A Unified Framework for Cost-Performance Optimization in LLM Context Management*. Disponível em: https://arxiv.org/pdf/2605.23071. Acesso em: 02 ago. 2026.

[8] ARXIV.ORG. *Towards Optimizing the Costs of LLM Usage*. Disponível em: https://arxiv.org/pdf/2402.01742. Acesso em: 02 ago. 2026.

[9] REDIS. *Context Window Overflow in 2026: Fix LLM Errors Fast*. Disponível em: https://redis.io/blog/context-window-overflow/. Acesso em: 02 ago. 2026.

[10] REDIS. *Context Window Management for LLM Apps: Dev Guide*. Disponível em: https://redis.io/blog/context-window-management-llm-apps-developer-guide/. Acesso em: 02 ago. 2026.

[11] ARXIV.ORG. *Practical Considerations for Agentic LLM Systems*. Disponível em: https://arxiv.org/pdf/2412.04093. Acesso em: 02 ago. 2026.

[12] YAGE.AI. *Why Coding Agents Still Use grep as Their Search Backbone*. Disponível em: https://yage.ai/share/why-coding-agents-still-use-grep-en-20260327.html. Acesso em: 02 ago. 2026.

[13] CODEANT. *Why Your Coding Agent Should Use ripgrep (rg) Instead of grep*. Disponível em: https://codeant.ai/blogs/why-coding-agents-should-use-ripgrep. Acesso em: 02 ago. 2026.

[14] ANTHROPIC. *Building Effective AI Agents*. Disponível em: https://www.anthropic.com/research/building-effective-agents. Acesso em: 02 ago. 2026.

[15] ARXIV.ORG. *Is Grep All You Need? How Agent Harnesses Reshape Agentic Search*. Disponível em: https://arxiv.org/pdf/2605.15184. Acesso em: 02 ago. 2026.

[16] MCP MARKET. *Subagent Orchestration Guide — Claude Code Skill*. Disponível em: https://mcpmarket.com/tools/skills/subagent-orchestration-guide-1. Acesso em: 02 ago. 2026.

[17] ANTHROPIC. *Orchestrate subagents at scale with dynamic workflows — Claude Code Docs*. Disponível em: https://code.claude.com/docs/en/workflows. Acesso em: 02 ago. 2026.

[18] KONISHI, Hidekazu. *Claude Code Subagents and Multi-Agent Orchestration Guide*. Disponível em: https://hidekazu-konishi.com/entry/claude_code_subagents_and_orchestration_guide.html. Acesso em: 02 ago. 2026.

[19] TOTALUM. *Claude Code subagents: the 2026 production playbook*. Disponível em: https://www.totalum.app/blog/claude-code-subagents-totalum. Acesso em: 02 ago. 2026.

[20] EXPLAINX.AI. *Claude Code settings.json: Every Option Explained*. Disponível em: https://www.explainx.ai/blog/claude-code-settings-json-complete-reference-2026. Acesso em: 02 ago. 2026.

[21] ANTHROPIC. *Hooks reference — Claude Code Docs*. Disponível em: https://code.claude.com/docs/en/hooks. Acesso em: 02 ago. 2026.

[22] DEV.TO. *The Complete Claude Code Power User Guide: Slash Commands, Hooks, Skills & More*. Disponível em: https://dev.to/numbpill3d/the-complete-claude-code-power-user-guide-slash-commands-hooks-skills-more-6ep. Acesso em: 02 ago. 2026.
