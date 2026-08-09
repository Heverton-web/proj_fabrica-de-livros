# Capítulo 5: Linguagem ubíqua e descoberta colaborativa: DDD, event storming e critérios de aceitação

## 1. Introdução

No Capítulo 4, você aprendeu que a Specification by Example transforma conversas em exemplares executáveis — mas há um pré-requisito silencioso: todos os participantes da conversa precisam falar a mesma língua. É exatamente esse o tema deste capítulo: a matéria-prima da planta. Você vai aprender o conceito de linguagem ubíqua do Domain-Driven Design de Eric Evans, que estabelece um vocabulário único compartilhado entre negócio e tecnologia [1]; a técnica de descoberta colaborativa do event storming criada por Alberto Brandolini, que produz essa linguagem em horas em vez de meses [2]; e a ponte entre user stories, critérios de aceitação e Definition of Done — o ponto onde a conversa vira especificação executável [3]. Ao final, você saberá como conduzir a oficina de descoberta que alimenta os exemplares do Capítulo 4 com a matéria-prima certa.

## 2. Explica

### A linguagem ubíqua: o vocabulário que unifica o time

Eric Evans introduziu o conceito de linguagem ubíqua no livro Domain-Driven Design, em 2003, com uma observação que parece óbvia e é profunda: o time de software não fala a língua do negócio, e o negócio não fala a língua do time [1]. O negócio diz "devolução", "chargeback", "estornar"; o time diz "rollback", "refund", "update status". Essas diferenças não são triviais — cada uma delas é uma fronteira onde a intenção pode se perder. A linguagem ubíqua é a resposta disciplinada: um vocabulário único, deliberadamente construído, usado em TODOS os artefatos — conversas, histórias, código, testes, documentação — sem tradução. O termo é o mesmo em todas as camadas: se o negócio chama "estorno", o código chama `estorno`, a classe chama `Estorno`, o cenário Gherkin fala de estorno, e o campo no banco se chama `estorno` [1][4].

Você vai perceber que a linguagem ubíqua não é um glossário de parede — é uma prática viva. Ela nasce da conversa (a modelagem colaborativa), é consolidada em um modelo de domínio (o mapa dos conceitos e suas relações), e é continuamente ajustada quando se descobre que dois termos diferentes significam a mesma coisa (ambigüidade) ou que o mesmo termo significa duas coisas diferentes (polissemia) [5]. O glossário resultante é um dos artefatos mais valiosos da planta: ele define o vocabulário em que os exemplares vão ser escritos, e sem ele a Specification by Example produz exemplos que o negócio não reconhece — e que portanto não validam nada [6].

### O event storming: a oficina que produz a linguagem

O event storming, criado por Alberto Brandolini, é a técnica de descoberta colaborativa que materializa a linguagem ubíqua em sessões intensas e guiadas. O ponto de partida é uma sala com uma parede coberta de papel, post-its de várias cores e um grupo heterogêneo — especialistas de negócio, desenvolvedores, QA, operações. O facilitador propõe uma pergunta de partida ("como um pedido é processado hoje?") e o grupo narra o processo em eventos de domínio — post-its laranja, cada um com uma frase no passado: "pedido criado", "pagamento aprovado", "estoque reservado", "pedido expedido" [2]. A regra de ouro: eventos, não etapas — a conversa flui sobre o que aconteceu, não sobre o que o sistema "faz", porque eventos são fatos incontestáveis do domínio, enquanto etapas são interpretações de quem as nomeia [7].

A partir dos eventos, o grupo adiciona as camadas: comandos (post-its azuis — "reservar estoque", "aprovar pagamento"), atores (post-its amarelos — "cliente", "fraudes", "transportadora"), políticas e regras (post-its roxos — "se pagamento recusado, então pedido cancelado"), e, por fim, os agregados e bounded contexts que agrupam os conceitos (post-its verdes) [8]. O resultado em poucas horas é um mapa visual completo do fluxo de negócio, com TODAS as bordas, exceções e regras expostas na parede — e, mais importante, uma linguagem acordada: quando o grupo usa duas palavras para o mesmo evento, a divergência aparece na parede e é resolvida ali [9]. O event storming é a Descoberta do loop BDD em esteróides: ele não produz um exemplo — produz o mapa inteiro onde os exemplos vivem.

### O que o DDD ensina à especificação: o modelo de domínio como planta

O DDD contribui para a especificação muito além do vocabulário. Seu conceito central é o modelo de domínio: uma representação estruturada dos conceitos, regras e relações do negócio, que serve de referência para todo o design [1]. Para a especificação, isso significa que antes de escrever cenários, o time deve ter clareza sobre o modelo — quais são as entidades (conceitos com identidade e ciclo de vida), os value objects (conceitos descritivos sem identidade), os agregados (grupos de consistência transacional) e os bounded contexts (fronteiras onde um conceito tem um significado único) [10]. Cada cenário Gherkin exercita o modelo; cada termo do cenário deve ser um termo do modelo; e quando o cenário revela uma inconsistência no modelo, é o modelo que muda — não o cenário que contorna [11].

O bounded context merece destaque porque é a fonte mais comum de bugs de especificação: o mesmo termo tem significados diferentes em contextos diferentes [10]. "Pedido" no contexto de vendas tem um ciclo de vida; no contexto de logística, outro; no contexto financeiro, outro ainda. Uma especificação que não declara seu contexto produz o clássico desastre: o time de vendas "aprovando pedidos" que a logística considera "não expedíveis". A disciplina do DDD: cada contexto tem sua linguagem e suas regras; a especificação declara o contexto no início da feature; e os cenários falam a linguagem daquele contexto, sem misturar vocabulários [12].

### De user stories a critérios de aceitação

A ponte final entre conversa e especificação é a user story e seus critérios de aceitação. A user story, no formato padrão de Connextra "Como [papel], eu quero [funcionalidade], para [benefício]", é um cartão de intenção — um lembrete para a conversa, não uma especificação [3]. O que transforma a story em planta são os critérios de aceitação: as condições observáveis que definem quando a história está pronta, escritas de forma verificável — e, na prática madura, como cenários Gherkin [13]. A qualidade da story é governada pelo acrônimo INVEST: Independent (não acoplada), Negotiable (negociável), Valuable (valiosa), Estimable (estimável), Small (pequena) e Testable (testável) — e é exatamente o "T" de Testable que conecta a story ao SDD: uma história sem critérios testáveis não é uma história, é um desejo [14].

O Definition of Done (DoD) completa o quadro: a lista de condições que toda história deve satisfazer para ser considerada concluída — e, em um time SDD, o DoD inclui obrigatoriamente "os cenários de aceitação estão escritos, automatizados e verdes" [15]. Note a consequência: o DoD vira o habite-se da história. A história só recebe o habite-se quando a planta (cenários) está verde — não quando o código "parece funcionar". Essa é a transição cultural mais importante do SDD: a definição de pronto deixa de ser uma lista de formalismos e passa a ser a execução da planta [16].

## 3. Ilustra

Voltemos à construtora. O arquiteto percebeu que as disputas com os encarregados não eram sobre medidas — eram sobre palavras. "Área de serviço" significava uma coisa para o cliente, outra para o projetista, outra para o pedreiro. A solução da construtora foi o catálogo de termos: um dicionário vivo, fixado na parede do canteiro, onde cada termo tem UMA definição — "área de serviço: cômodo coberto, mínimo 2x2m, com ponto de água e esgoto; chamado de 'lavanderia' apenas quando houver máquina instalada". Toda conversa, todo contrato, todo pedido de material usa exatamente os termos do catálogo. Quando um fornecedor entrega "revestimento para área de serviço" que não serve, a culpa é rastreável: o termo estava definido, o material não cumpriu a definição — e não houve interpretação no meio [17].

```mermaid
%% legenda: A oficina de event storming produzindo linguagem ubiqua e especificacao
flowchart LR
  A[Eventos laranja] --> B[Comandos azuis]
  B --> C[Atores amarelos]
  C --> D[Politicas roxas]
  D --> E[Agregados verdes]
  E --> F[Linguagem ubiqua]
  F --> G[User stories]
  G --> H[Criterios de aceitacao]
  H --> I[Cenarios Gherkin executaveis]
  style F fill:#a855f7,color:#fff
  style H fill:#a855f7,color:#fff
  style I fill:#a855f7,color:#fff
```

O catálogo de termos é a linguagem ubíqua; a parede onde ele é fixado e revisado é o event storming; e os contratos que usam exclusivamente os termos do catálogo são os cenários Gherkin. A lição da metáfora: a planta não começa no desenho técnico — começa no vocabulário. Um prédio desenhado com termos que cada encarregado interpreta diferente produz um prédio incoerente, mesmo com desenhos perfeitos. Um software especificado com termos que cada membro do time interpreta diferente produz um sistema incoerente, mesmo com testes perfeitos — porque os testes verificam a interpretação local, não a intenção compartilhada [18]. Você, como Engenheiro de Software, já viveu o sintoma: o time de backend chama "cancelar", o time de billing chama "estornar", o time de logística chama "suspender" — e o mesmo evento real, o cliente cancelando a compra, gera três fluxos diferentes no sistema porque a linguagem nunca foi unificada.

## 4. Técnica

### Conduzindo uma sessão de event storming

A técnica de event storming tem variações (big picture, process level, design level), mas a essência prática é a mesma. Para a especificação, o formato mais útil é o process level: foco em um fluxo de negócio específico com o objetivo de produzir eventos, regras e, ao final, os candidatos a cenário. A sessão de quatro horas segue esta estrutura: aquecimento (20 min) — o facilitador apresenta a pergunta-guia e o time lista os primeiros eventos óbvios, quebrando o gelo; narrativa (60-90 min) — o grupo caminha pelo fluxo do início ao fim, adicionando eventos, comandos e atores, com o facilitador mediando conflitos de linguagem (quando dois termos aparecem para o mesmo evento, um é escolhido e anotado); bordas e exceções (60 min) — o facilitador provoca com os "e se...?" que o fluxo feliz esconde: e se o pagamento falhar? e se o estoque acabar? e se o cliente cancelar no meio?; e fechamento (30 min) — o mapa é fotografado, os termos escolhidos são consolidados no glossário, e os eventos mais críticos viram candidatos a cenários Gherkin [2][7].

```python
"""Registro de event storming: do mapa de eventos aos cenarios candidatos.

Estrutura de dados para capturar o resultado da oficina e exportar
os candidatos a feature Gherkin. Rode ao fim da sessao.
"""
from dataclasses import dataclass, field


@dataclass
class Evento:
    nome: str
    comando: str
    ator: str
    regra: str = ""
    borda: bool = False


@dataclass
class MapaEventos:
    dominio: str
    eventos: list[Evento] = field(default_factory=list)

    def glossario(self) -> list[str]:
        termos = {self.dominio}
        for ev in self.eventos:
            termos.add(ev.nome)
            termos.add(ev.comando)
            termos.add(ev.ator)
        return sorted(termos)

    def candidatos_cenarios(self) -> list[str]:
        saida = []
        for ev in self.eventos:
            base = f"{ev.ator} {ev.comando} -> {ev.nome}"
            saida.append(base if not ev.borda else f"[BORDA] {base} ({ev.regra})")
        return saida


if __name__ == "__main__":
    mapa = MapaEventos(dominio="pedido")
    mapa.eventos = [
        Evento("pedido criado", "criar pedido", "cliente"),
        Evento("pagamento aprovado", "aprovar pagamento", "fraudes"),
        Evento("estoque reservado", "reservar estoque", "logistica"),
        Evento("pagamento recusado", "aprovar pagamento", "fraudes",
               regra="se recusado, pedido cancelado", borda=True),
    ]
    print("GLOSSARIO:", ", ".join(mapa.glossario()))
    print("CENARIOS CANDIDATOS:")
    for c in mapa.candidatos_cenarios():
        print(" -", c)
```

### Consolidando o glossário ubíquo

O glossário ubíquo é o artefato de saída da oficina e o vocabulário dos cenários. Ele deve ser um arquivo simples, versionado com o código, com uma entrada por termo: termo canônico, definição, sinônimos proibidos e contexto. A disciplina é que qualquer cenário Gherkin novo só usa termos do glossário — e que qualquer termo novo no cenário exige uma entrada no glossário [6]. O glossário é vivo: quando a oficina descobre que "estorno" e "reembolso" são a mesma coisa, um vira canônico e o outro vira sinônimo proibido, e uma busca no repositório corrige os usos antigos. Abaixo, um exemplo do formato:

```markdown
# Glossário Ubíquo — domínio de Pedidos

Regra: todo cenário Gherkin usa somente termos deste glossário.
Termo novo em cenário => nova entrada aqui, aprovada pelo PO.

## pedido
Definição: solicitação de compra de um ou mais itens, com ciclo de vida
próprio (criado, pago, expedido, entregue, cancelado).
Sinônimos proibidos: ordem, compra, transação (no contexto de vendas).
Contexto: Vendas.

## estorno
Definição: devolução integral do valor pago ao cliente, após cancelamento
ou devolução de mercadoria.
Sinônimos proibidos: reembolso, refund, rollback.
Contexto: Financeiro.

## cancelamento
Definição: encerramento do pedido antes da expedição, por ação do cliente
ou da política antifraude.
Sinônimos proibidos: suspensão, anulação.
Contexto: Vendas.
```

### A modelagem colaborativa: como a linguagem ubíqua nasce de verdade

A linguagem ubíqua não nasce de uma reunião de nomeação de termos — nasce da modelagem colaborativa, a prática contínua de desenhar o modelo de domínio JUNTOS, com o negócio e a tecnologia na mesma mesa [1]. A oficina de event storming é a forma mais estruturada dessa modelagem, mas ela não termina na oficina: a linguagem é exercitada em todos os artefatos, e é exatamente aí que ela se consolida ou se corrompe. A regra prática de manutenção da linguagem: sempre que um termo novo aparece em uma conversa de refinamento, o facilitador pergunta "este termo é novo, ou é sinônimo de um existente?" — se é novo, entra no glossário com definição e contexto; se é sinônimo, é eliminado em favor do canônico, e a divergência vira item de correção [6].

O mecanismo mais eficaz de consolidação é o eco no código: quando o desenvolvedor nomeia classes, métodos e campos com os termos do glossário, a linguagem ubíqua passa a ser verificada pelo compilador — um termo fora do glossário que sobrevive no código é um bug de linguagem tão real quanto um bug de lógica, e a revisão de código deve pegá-lo [4][10]. É o mesmo princípio da cota na planta: o termo é a unidade de medida, e cada uso inconsistente é uma cota divergente. Times que consolidam essa prática descobrem um efeito colateral valioso: a linguagem ubíqua reduz o número de perguntas de interpretação — o novo desenvolvedor pergunta menos "o que você quis dizer com X?" porque X está definido no glossário, e a resposta está a um arquivo de distância [18].

### Event storming big picture: o mapa do negócio inteiro

A variação big picture do event storming é a ferramenta certa para um objetivo diferente: entender o negócio inteiro em um dia, antes de especificar qualquer parte. O big picture não detalha fluxos — desenha o mapa geral: os eventos de alto nível, os atores, as fronteiras entre contextos e as políticas que os conectam [8]. O uso prático do big picture na adoção do SDD: antes de escolher a primeira funcionalidade para o piloto (Capítulo 10), o time conduz um big picture para saber onde estão os contextos mais críticos e as regras mais caras — o mapa mostra o terreno antes de a primeira estaca ser cravada.

O big picture tem regras próprias: eventos em nível de negócio ("pedido entregue"), não de sistema ("update da tabela de pedidos"); atores como papeis, não como pessoas; e a saída principal é a identificação dos bounded contexts — as regiões do mapa onde um conceito tem um significado único e onde a linguagem ubíqua é local [10][12]. A identificação dos contextos é o pré-requisito da especificação por contexto (Capítulo 5): sem o mapa, o time não sabe onde "estorno" é o termo certo e onde é o errado; com o mapa, cada especificação declara seu contexto de partida e evita o incidente de "suspensão vs pausa" que você viu na seção Aplica [7][22].

### Critérios de aceitação que geram cenários executáveis

A tradução de critérios de aceitação em cenários Gherkin segue uma receita direta: cada critério deve ser escrito em linguagem observável ("o cliente vê a mensagem X" e não "o sistema processa X internamente"); cada critério deve ter um caso feliz e pelo menos um caso de borda; e o conjunto de critérios deve ser verificável por máquina [13]. A prática recomendada é escrever os critérios JÁ como Gherkin na própria história — o cartão da story contém os cenários, eliminando a tradução posterior:

```gherkin
# linguagem: pt
Funcionalidade: Cancelamento de pedido
  Como um cliente
  Eu quero cancelar um pedido
  Para não ser cobrado por uma compra que não quero

  Cenário: Cancelamento antes da expedição
    Dado um pedido no estado "pago"
    E que o pedido ainda não foi expedido
    Quando o cliente cancela o pedido
    Então o pedido passa para o estado "cancelado"
    E o valor é estornado ao cliente
    E o estoque dos itens é devolvido

  Cenário: Cancelamento após expedição
    Dado um pedido no estado "expedido"
    Quando o cliente tenta cancelar o pedido
    Então o sistema informa que o cancelamento não é mais possível
    E orienta o cliente a abrir uma solicitação de devolução
```

Note como o glossário aparece nos cenários: "estornado" (não "reembolsado"), "expedido" (não "enviado"), "cancelamento" (não "suspensão"). A coerência do vocabulário é o que torna esses cenários compreensíveis pelo negócio e executáveis pelo código — os dois lados reconhecem exatamente o que está sendo especificado [19].

### DoD como habite-se: integrando a especificação ao fluxo de entrega

A integração final do DoD: a lista de verificação de conclusão da história deve incluir, explicitamente: (1) critérios de aceitação escritos e aprovados pelo PO antes do desenvolvimento; (2) cenários automatizados e rodando em CI; (3) todos os cenários verdes; (4) glossário atualizado com qualquer termo novo; (5) revisão do PO baseada nos cenários, não em demonstração manual [15][16]. Essa lista muda o comportamento do time de forma mensurável: o desenvolvedor não pergunta mais "está pronto?" ao PO — ele mostra os cenários verdes; e o PO não responde mais por intuição — ele confere a suíte. O DoD vira o habite-se da história: a planta executável atesta a conformidade, e a revisão humana valida a adequação da planta à intenção (o que o PO aprovou) — dois atos distintos, ambos necessários [20].

## 5. Aplica

### A cena de contraste: a palavra "suspensão" que travou a operação

Você é o tech lead de um time em uma plataforma de assinaturas. Há seis meses, o time de billing implementou a funcionalidade de "suspender assinatura" para inadimplência — o código chama `suspender_assinatura`, e a regra congela o acesso até o pagamento. Há três semanas, o time de produto lançou o recurso de "pausar assinatura" para clientes que viajam — o código chama `pausar_assinatura`, e a regra congela o acesso por um período escolhido pelo cliente. Na última sexta-feira, o incidente: um cliente que viajou teve o acesso bloqueado permanentemente — o sistema de billing, ao detectar a inadimplência do mês, chamou a rotina que "suspende" — mas, por um bug de mapeamento na integração entre os serviços, a "suspensão" chamou a "pausa", e o acesso do cliente ficou congelado além da viagem, sem data de reativação [21].

O diagnóstico, dolorosamente claro para você: não foi um bug de código — foi um bug de linguagem. O time tinha DOIS termos ("suspender" e "pausar") para duas regras de negócio genuinamente diferentes, mas os dois serviços falavam "suspensão" de forma intercambiável, e nenhuma especificação existia declarando o contexto e a distinção. O glossário ubíquo teria pego a ambiguidade na oficina de descoberta — "espere, 'suspender' no billing é diferente de 'pausar' no produto?" — e os cenários de cada contexto teriam tornado as duas regras visíveis e verificáveis. A correção na hora é emergencial (mapear as duas rotinas e isolar a integração); a correção estrutural, que você lidera na sequência, é a oficina de event storming do fluxo de assinaturas, a consolidação do glossário com "suspender" e "pausar" como termos distintos de contextos distintos, e a reescrita das duas features com cenários que exercitam exatamente as bordas — incluindo o cenário do cliente inadimplente e viajante, que ninguém tinha especificado [22].

### Armadilhas comuns

As armadilhas desta camada são clássicas. A primeira é o glossário de parede: um dicionário criado uma vez e esquecido, que ninguém consulta — linguagem ubíqua sem uso não é linguagem ubíqua, é decoração; a regra é que todo cenário e toda revisão usem o glossário, e que ele seja versionado com o código. A segunda é o event storming de fachada: a oficina acontece, o mapa fica bonito na parede, e ninguém transforma os eventos em cenários — a descoberta sem formulação é um passeio, não um processo [7]. A terceira é o DDD puro e duro: times que investem meses em modelagem de domínio antes de escrever qualquer cenário, produzindo modelos abstratos que nunca são verificados contra o comportamento — o modelo só vale quando vira cenário executável. A quarta é a user story sem critérios: histórias aprovadas no refinamento sem nenhuma condição observável, delegando a especificação para o momento do desenvolvimento — o mesmo erro do Capítulo 1, em nova roupagem [3]. E a quinta é o DoD ornamental: a lista de verificação existe, mas ninguém a verifica de verdade — o time marca "cenários verdes" sem rodar a suíte, e o habite-se vira carimbo [23].

### A linguagem ubíqua e o custo da tradução

Todo time de software vive com um custo invisível: o custo da tradução entre a língua do negócio e a língua do código. Cada "aqui a gente chama de devolução, mas no sistema é refund" é uma tradução — e cada tradução é uma oportunidade de erro: o termo que o negócio usa tem um significado no contexto do negócio, e o termo que o sistema usa pode carregar outro [1][4]. A linguagem ubíqua elimina o custo da tradução ao eliminá-la: não existe mais "aqui a gente chama" — existe um termo único, usado pelos dois lados, em todos os artefatos [6]. O custo eliminado é real e mensurável: cada tradução é um ponto de divergência potencial, e os pontos de divergência são exatamente onde nascem os bugs de especificação do Capítulo 1 [18].

O custo da tradução tem uma segunda dimensão, temporal: a tradução é paga toda vez que alguém novo entra no time. O recém-contratado que não sabe que "devolução" e "refund" são a mesma coisa pergunta, erra, e aprende com o erro — cada aprendizado é uma micro-divergência que a linguagem ubíqua teria evitado ao tornar o termo único e documentado [22][24]. A economia de onboarding é o argumento de retorno mais claro para o glossário: o investimento de uma oficina de event storming (horas) paga o onboarding de cada novo membro (dias economizados) em semanas [10]. Quando o time internaliza essa conta, a linguagem ubíqua deixa de ser "disciplina de DDD" e vira a ferramenta de produtividade que ela é: o vocabulário único é a planta da comunicação, e a comunicação é a matéria-prima de tudo o que a obra construiu [16].

### Métricas de sucesso e fracasso

Sucesso: o glossário cresce organicamente e é consultado em refinamentos; as oficinas de event storming produzem candidatos a cenários que entram no backlog já formulados; e a definição de pronto passa a incluir cenários verdes executados — não marcados. Fracasso: o mesmo conceito com dois nomes sobrevivendo em produção (o sintoma do incidente de "suspensão"); histórias que chegam ao desenvolvimento sem um único critério de aceitação; e reuniões de refinamento que terminam em "está claro?" em vez de "quais são os cenários?" — se a conversa não produz exemplos, a planta não foi desenhada [24].

O roteiro de descoberta colaborativa que produz esses resultados tem cinco movimentos bem definidos. Movimento um — convide as pessoas certas: representantes do negócio que tomam decisão, não meros informantes; a ausência de quem decide é a causa número um de specs que nascem erradas. Movimento dois — faça o evento de descoberta no quadro (físico ou virtual), com a linguagem ubíqua como única língua permitida: todo termo técnico usado vira item do glossário ou é banido da sala; o glossário nasce aqui, não na documentação. Movimento três — desenhe o fluxo como um passeio pelo domínio, perguntando a cada passo "o que pode dar errado aqui?" e registrando as respostas como candidatos a cenários; a pergunta adversária é o motor do event storming, é ela que transforma o mapa feliz do fluxo no mapa real com as exceções. Movimento quatro — converta os candidatos em cenários no formato do capítulo anterior, na hora, com o dono do negócio corrigindo o português e o comportamento; o cenário escrito na reunião tem a autenticidade que o cenário reescrito depois perde. Movimento cinco — feche com a definição de pronto da descoberta: a sessão terminou quando o fluxo mapeado cabe em uma tela, os candidatos a cenários cobrem as exceções conhecidas, e o glossário tem entradas para os termos que apareceram mais de uma vez; fechar antes disso é aceitar planta incompleta para economizar vinte minutos. O teste ácido da sessão é uma única pergunta feita ao final: cada participante do negócio consegue explicar o que será construído para um colega que não participou, usando só as palavras do glossário? Se sim, a linguagem ubíqua funcionou — se não, a descoberta precisa de mais uma rodada antes de virar planta [24].

## 6. Conclusão

Neste capítulo, você completou a matéria-prima da planta: a linguagem ubíqua de Evans, que unifica o vocabulário entre negócio e tecnologia e dá a cada termo um único significado em cada contexto [1][5]; o event storming de Brandolini, a oficina que produz a linguagem e o mapa do fluxo em horas [2][7]; e a ponte entre user stories INVEST, critérios de aceitação e Definition of Done, que transforma a conversa em especificação executável [3][14][15]. O desafio: conduza uma sessão de event storming de quatro horas para o fluxo mais crítico do seu domínio e consolide o glossário resultante no repositório, junto com os primeiros cenários candidatos. No próximo capítulo, vamos juntar todas as peças do desenho da planta em um único artefato: a anatomia de uma boa spec — os seis elementos essenciais, o template SPEC.md como fonte da verdade, e os anti-padrões que fazem especificações morrerem no papel.

## 7. Referências Bibliográficas

[1] EVANS, Eric. *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Boston: Addison-Wesley, 2003.
[2] BRANDOLINI, Alberto. *Introducing EventStorming*. Leanpub, 2014.
[3] COHN, Mike. *User Stories Applied: For Agile Software Development*. Boston: Addison-Wesley, 2004.
[4] FOWLER, Martin. *Ubiquitous Language* (bliki). Disponível em: https://martinfowler.com/bliki/UbiquitousLanguage.html. Acesso em: 5 ago. 2026.
[5] VERNON, Vaughn. *Implementing Domain-Driven Design*. Boston: Addison-Wesley, 2013.
[6] ADZIC, Gojko. *Specification by Example: How Successful Teams Deliver the Right Software*. Shelter Island: Manning Publications, 2011.
[7] BRANDOLINI, Alberto. *EventStorming — Medium*. Disponível em: https://medium.com/domain-driven-design/eventstorming-9c323f0c2d5c. Acesso em: 5 ago. 2026.
[8] BRANDOLINI, Alberto. *EventStorming: Beyond the Big Picture*. Leanpub, 2019.
[9] KEOGH, Liz. *Behaviour Driven Development*. Disponível em: https://lizkeogh.com/behaviour-driven-development/. Acesso em: 5 ago. 2026.
[10] EVANS, Eric. *Domain-Driven Design Reference: Definitions and Pattern Summaries*. 2014. Disponível em: https://domainlanguage.com/ddd/. Acesso em: 5 ago. 2026.
[11] VERNON, Vaughn. *Domain-Driven Design Distilled*. Boston: Addison-Wesley, 2016.
[12] FOWLER, Martin. *BoundedContext* (bliki). Disponível em: https://martinfowler.com/bliki/BoundedContext.html. Acesso em: 5 ago. 2026.
[13] SMART, John Ferguson. *BDD in Action: Behavior-Driven Development for the Whole Software Lifecycle*. Shelter Island: Manning Publications, 2014.
[14] COHN, Mike. *Investigating Stories*. Mountain Goat Software. Disponível em: https://www.mountaingoatsoftware.com/blog/investing-in-stories. Acesso em: 5 ago. 2026.
[15] SCHWABER, Ken; SUTHERLAND, Jeff. *The Scrum Guide: The Definitive Guide to Scrum*. 2020. Disponível em: https://scrumguides.org. Acesso em: 5 ago. 2026.
[16] ADZIC, Gojko. *Living Documentation: Continuous Knowledge Sharing by Design*. Boston: Addison-Wesley, 2017.
[17] NORTH, Dan. *What's in a Story?* Dan North & Associates, 2007. Disponível em: https://dannorth.net/whats-in-a-story/. Acesso em: 5 ago. 2026.
[18] WEINBERG, Gerald M. *Quality Software Management: Systems Thinking*. New York: Dorset House, 1992.
[19] WYNNE, Matt; HELLESØY, Aslak. *The Cucumber Book: Behaviour-Driven Development for Testers and Developers*. 2. ed. Raleigh: Pragmatic Bookshelf, 2017.
[20] MARTIN, Robert C. *Agile Software Development: Principles, Patterns, and Practices*. Upper Saddle River: Prentice Hall, 2002.
[21] NEWMAN, Sam. *Building Microservices: Designing Fine-Grained Systems*. 2. ed. Sebastopol: O'Reilly Media, 2021.
[22] KLEPPMANN, Martin. *Designing Data-Intensive Applications*. Sebastopol: O'Reilly Media, 2017.
[23] COHN, Mike. *Succeeding with Agile: Software Development Using Scrum*. Boston: Addison-Wesley, 2009.
[24] ADZIC, Gojko. *Specification by Example, 10 years later*. 2020. Disponível em: https://gojko.net/2020/03/17/sbe-10-years.html. Acesso em: 5 ago. 2026.
