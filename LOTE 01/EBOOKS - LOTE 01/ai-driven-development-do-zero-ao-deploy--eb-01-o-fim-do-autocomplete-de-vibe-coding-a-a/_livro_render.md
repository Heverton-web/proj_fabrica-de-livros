# O Fim do Autocomplete: De Vibe Coding a Agentic Coding

Imagine um estaleiro. Não um estaleiro qualquer — o seu. Você é o mestre desta obra, e a embarcação que vai erguer aqui, capítulo a capítulo, não é feita de aço e rebite, mas de agentes, ferramentas e decisões de engenharia.

Este livro é a construção dessa embarcação agêntica, da quilha assentada na doca seca até a botadura no cais de lançamento, onde ela finalmente toca a água da produção. Ao final desta leitura, você não vai apenas "ter usado IA para programar" — vai reconhecer o Engenheiro Agêntico capaz de projetar, auditar e comandar uma tripulação de agentes de ponta a ponta.

Mas antes de assentar a primeira quilha, você precisa entender por que o estaleiro mudou de forma entre 2024 e 2026 — e por que quem ainda opera como se estivesse na era do autocomplete está, sem perceber, construindo em madeira num mundo que já solda em aço.

Este capítulo separa dois modos de trabalho que parecem parecidos, mas não são: o *vibe coding*, em que você aprova cada rebite manualmente, e o *agentic coding*, em que uma tripulação autônoma solda o casco inteiro. A diferença entre eles não é velocidade — é o que garante que o casco não afunda.

## Vibe Coding e Agentic Coding: Onde Está a Diferença de Verdade

Vibe coding é o nome que a comunidade técnica deu ao modo de trabalho em que o desenvolvedor permanece no loop revisando cada saída do modelo em formato conversacional — um autocomplete avançado, ainda que fluente. Agentic coding é outra categoria: agentes que planejam, executam, testam e iteram tarefas inteiras do ciclo de engenharia com supervisão mínima.

A diferença central entre os dois não é o grau de autonomia do modelo — é a engenharia por trás dela. A codificação por vibe trata testes, linting e CI/CD como opcionais, o que eleva risco e reduz accountability em produção.

Essa distinção tem uma nuance técnica que vale destacar, porque ela evita um erro comum de quem está começando: nem todo sistema com um LLM por trás é um agente. Uma arquitetura de referência bastante citada na literatura separa *workflows* — sistemas em que o modelo executa passos dentro de um caminho pré-definido pelo engenheiro, por mais que use IA generativa em cada etapa — de *agentes* propriamente ditos, em que o próprio modelo decide dinamicamente os próximos passos e quais ferramentas usar, observando o resultado de cada ação antes de decidir a seguinte.

Um script que chama a API do modelo três vezes em sequência fixa não é agentic coding, mesmo que gere código competente em cada chamada; é automação com IA embutida, e continua sendo vibe coding disfarçado se ninguém audita o resultado.

O agentic coding deste livro pressupõe o segundo caso — decisão dinâmica, condicionada ao feedback da própria execução. É exatamente essa dinamicidade que torna o diário de bordo indispensável: sem ele, você não tem como reconstruir por que o agente decidiu o que decidiu.

## Uma Ressalva Antes de Seguir

Vibe coding não é sempre errado. Para um protótipo descartável, uma prova de conceito que nunca vai a produção, ou um script de uso único que você mesmo apaga amanhã, a fricção de configurar suíte de testes, CI e revisão por agente é custo sem retorno proporcional.

O erro não é usar vibe coding — é usar vibe coding em código que vai para produção e tratá-lo como se fosse agentic coding só porque um LLM esteve envolvido em algum ponto.

A pergunta que decide qual dos dois modos você deveria estar praticando não é "qual ferramenta eu abri", é "o que acontece se esta saída estiver sutilmente errada e ninguém perceber por três semanas?". Se a resposta for "nada grave", vibe coding basta. Se a resposta envolver dado de usuário, dinheiro ou disponibilidade de produção, você precisa do diário de bordo completo.

## Uma Virada de Mercado, Não uma Moda

Pare e sinta o tamanho disso: especialistas em pesquisa de mercado já descrevem 2026 como o ano em que a migração de assistentes de código pontuais para agentes orquestrados de SDLC completo deixou de ser tendência para se tornar padrão de mercado. Não é uma opinião isolada — levantamentos setoriais indicam que a grande maioria das organizações já usa IA ativamente em fluxos de desenvolvimento, e boa parte do restante está avaliando adoção agora.

Somando os dois grupos, perto de 97% do mercado já está dentro do movimento, de um jeito ou de outro — restam poucos times, hoje, com o luxo de esperar mais um ciclo para decidir se isso "pega ou não pega". A pergunta que resta para a maioria das equipes não é mais "se" adotar agentes de codificação, é "com que superfície de controle" adotá-los.

Essa virada tem nome técnico: SDLC (Software Development Life Cycle) "AI-first" ponta a ponta. Empresas como a Fujitsu já automatizam o ciclo completo — de definição de requisitos e design até implementação e testes de integração — e a Microsoft documenta, junto com o GitHub, a construção de um SDLC agêntico de ponta a ponta sobre Azure.

O que esses casos têm em comum não é a ferramenta, é o desenho: um framework de planejamento, codificação, teste e deploy autônomos, com pontos de checagem explícitos entre cada fase. Pesquisas sobre supervisão humana graduada em geração de código agêntico em domínios regulados chegam à mesma conclusão por outro caminho: autonomia crescente exige, na mesma proporção, mecanismos formais de governança — nunca menos controle, e sim controle redesenhado.

## O Contraponto Necessário

Vale um contraponto antes de aceitar esse otimismo em bloco, porque parte do seu trabalho como Engenheiro Agêntico é diferenciar padrão de engenharia de material de marketing corporativo. Nem toda alegação de "SDLC AI-first" resiste a auditoria externa.

Revisões acadêmicas sobre o uso de IA agêntica ao longo de todo o ciclo de vida de software separam, com cuidado metodológico, os relatos de fornecedor — que têm interesse comercial em parecer mais maduros do que de fato são — dos padrões observados de forma independente entre múltiplas organizações e portes de equipe. Isso não invalida os casos da Fujitsu e da Microsoft citados acima; contextualiza o que eles provam.

Trate-os como prova de que o padrão *existe e funciona em produção em pelo menos algumas organizações de grande porte* — não como prova de que qualquer ferramenta com "agente" no nome já entrega o mesmo nível de maturidade para o seu time. A pergunta que separa marketing de engenharia real não é "usa IA?" — é "onde fica o diário de bordo, e quem tem autoridade para auditá-lo?".

Duas outras condições, menos citadas em manchete, também precisam existir juntas para que a virada 2024-2026 seja mais do que retórica: chamadas de ferramenta confiáveis o bastante para que um agente encadeie dezenas delas sem alucinar um argumento, e ambientes de execução isolados (sandboxes) onde o agente pode testar uma hipótese arriscada sem tocar produção antes de qualquer aprovação humana. Vale registrar desde já que "modelo mais capaz" nunca foi, sozinho, a causa da virada. Foi a soma de modelo capaz mais infraestrutura de execução auditável.

Só que virada de mercado não é o mesmo que virada de confiabilidade. Um agente de codificação gera código sintaticamente correto, bem indentado, com nomes de variável sensatos — em segundos. E é exatamente aí que mora a armadilha: "parecer plausível" e "de fato funcionar" são coisas diferentes. Sem guardrails, o código passa no que a comunidade chama informalmente de "vibe check", mas falha silenciosamente em produção. Essa tensão entre velocidade agêntica e disciplina de engenharia clássica — em especial o TDD (Test-Driven Development) — é o fio que conecta tudo o que vem a seguir.

## Da Doca Seca à Quilha: o Estaleiro Muda de Era

Volte ao seu estaleiro. Em 2024, a doca seca operava assim: cada peça do casco passava pela mão do mestre antes de ser soldada — o mestre revisava, aprovava, corrigia. Era um trabalho artesanal, seguro, mas lento, e o mestre era o gargalo de tudo. Isso é vibe coding: você no loop, aprovando cada saída, uma peça de cada vez.

Em 2026, o estaleiro mudou de era. A quilha agora é assentada por uma tripulação de agentes que planeja o casco inteiro, corta, solda e testa a integridade de cada junta — sem esperar sua aprovação linha a linha. Isso só é seguro porque existe um diário de bordo: todo corte, toda solda, todo teste fica registrado e auditável antes da vistoria final do mestre. O ganho de velocidade não veio de menos controle — veio de controle redesenhado.

![Linha do tempo do Estaleiro Agentico, da doca seca do vibe coding a quilha assentada do SDLC agentico](imagens/diagramas/dia_livro_01_93146c5f4e.png)

## Turno Vibe vs. Turno Agêntico: a Camada que Ninguém Vê

Aqui está o ponto mais difícil deste capítulo — e por isso ele merece uma segunda camada de analogia. A primeira, mecânica geral, é esta: imagine dois turnos no estaleiro. No Turno Vibe, o operário solda uma chapa, chama o mestre, o mestre olha, aprova, o operário solda a próxima. No Turno Agêntico, a tripulação solda o casco inteiro da noite para o dia — mas cada solda é fotografada, catalogada e testada por um robô de vistoria antes de o mestre sequer acordar.

A segunda camada — o ponto realmente contraintuitivo — é esta: autonomia alta não é sinônimo de risco alto, e autonomia baixa não é sinônimo de segurança. Um Turno Vibe mal disciplinado, em que o mestre aprova "porque parece bom", tem *menos* accountability real do que um Turno Agêntico bem instrumentado, mesmo que o segundo pareça "mais arriscado" por ter menos humano no meio.

O que garante segurança não é quem aperta o botão — é se existe um diário de bordo verificável entre a decisão e a produção. Como Engenheiro Agêntico, seu trabalho nunca foi "revisar tudo pessoalmente" — sempre foi "garantir que exista rastro auditável", e é isso que muda de forma entre os dois turnos.

![Contraste entre o Turno Vibe (aprovacao manual sem rastro) e o Turno Agentico (execucao autonoma com diario de bordo auditavel)](imagens/diagramas/dia_livro_02_c1e2eca7b7.png)

## O Diário Rasurado: Quando a Vistoria Falha

Toda analogia de controle tem um contrapeso, e este merece ser dito antes de você confiar cegamente no Turno Agêntico: um diário de bordo só protege o casco se ninguém puder rasurá-lo depois do fato.

Imagine um operário do Turno Agêntico que, pressionado pelo prazo da botadura, arranca a página do diário onde uma solda reprovada ficou registrada — e cola por cima um relatório novo, dizendo que a vistoria passou sem ressalvas. Do lado de fora, o casco parece idêntico ao de um turno bem-sucedido: pintura fresca, chapas alinhadas, relatório de vistoria assinado e arquivado.

A diferença só aparece quando o navio já está no mar, e a junta que nunca foi de fato aprovada cede sob a primeira onda mais forte — três dias depois da botadura, não durante ela.

O detalhe que separa um diário de bordo de verdade de um caderno de anotações é justamente esse: cada página precisa amarrar-se à anterior de um jeito que arrancar uma denuncie a lacuna. Não basta o mestre confiar que "ninguém mexeria nisso" — a confiança, neste estaleiro, é sempre substituída por verificação mecânica.

É essa cena que a seção Técnica resolve a seguir, com um diário tecnicamente impossível de rasurar sem deixar rastro. E é essa mesma cena que abre a seção de aplicação prática: o que parece "só um teste comentado para o build passar" é, na prática, exatamente a página arrancada do diário — só que sem o gesto dramático de rasgar papel, porque no mundo real a rasura acontece com um `git commit` silencioso de sexta-feira à noite.

## A Vistoria Antes da Botadura: TDD e TDAD

Nenhuma embarcação vai ao mar sem vistoria — e nenhum código de agente vai a produção sem teste que falhe primeiro. No estaleiro, a "especificação" da peça (o desenho técnico, as tolerâncias) é escrita antes de qualquer solda. É exatamente isso que o TDD impõe ao agente: o teste, escrito antes da implementação, define o que é "correto" antes que uma linha de código exista.

![Ciclo de vida de uma peca do casco, do teste escrito a aprovacao ou retorno a fabricacao](imagens/diagramas/dia_livro_03_4b46b4f9f7.png)

## O Diário de Bordo em YAML: Duas Eras do Mesmo Pipeline

A diferença entre as duas eras do estaleiro não é abstrata — ela aparece literalmente no pipeline de CI. Veja o mesmo arquivo, comentado para mostrar onde o agente entra em 2026 e onde, em 2024, só havia checagem manual. Um agente que participa do pipeline como etapa auditável — não só como autor do código antes dele — é exatamente o que separa as duas eras:

```yaml
# pipeline-estaleiro.yml
# Comentarios marcam a diferenca estrutural entre as duas eras do estaleiro.

name: pipeline-casco

on:
  pull_request:
    branches: [main]

jobs:
  vistoria:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # 2024 (vibe coding): so existia lint e build manual.
      # O mestre revisava o diff inteiro antes de aprovar o merge.
      - name: lint
        run: npm run lint

      - name: build
        run: npm run build

      # 2026 (agentic coding): o agente entra como participante do pipeline.
      # Cada etapa abaixo e uma pagina do diario de bordo, auditavel antes
      # da vistoria final humana.
      - name: revisao-de-pr-por-agente
        run: agente-revisor --diff "${{ github.event.pull_request.diff_url }}"

      - name: suite-de-testes
        run: npm test -- --ci

      - name: remediacao-de-seguranca-por-agente
        run: agente-seguranca --escanear ./src

      - name: verificacao-pos-deploy
        run: agente-verificador --ambiente staging

      # Portao final: nenhum agente aprova o proprio trabalho para producao.
      - name: portao-humano
        run: echo "Aguardando aprovacao humana antes da botadura"
```

Note o que não mudou: o portão humano no fim. O que mudou foi tudo que passou a existir *antes* dele. É essa camada intermediária — não a IA isoladamente — que separa um pipeline de 2024 de um pipeline de 2026.

## O Agente de Commit: Accountability Codificada

Se accountability é um conceito abstrato, o código abaixo o torna concreto. Esta função representa a menor unidade de "Turno Agêntico" possível: um agente que só aplica uma mudança se a suíte de testes provar que ela é segura — nunca porque "parece boa".

```python
"""agente_commit.py
Agente de commit minimalista: accountability como codigo, nao como promessa.
"""
import subprocess
from dataclasses import dataclass


@dataclass
class ResultadoCommit:
    aplicado: bool
    motivo: str


def rodar_suite_de_testes(diretorio: str) -> bool:
    """Executa a suite de testes do projeto e retorna True se tudo passar."""
    processo = subprocess.run(
        ["pytest", diretorio, "-q"],
        capture_output=True,
        text=True,
    )
    return processo.returncode == 0


def agente_commit(diretorio_projeto: str, mensagem: str) -> ResultadoCommit:
    """Aplica um commit somente se a suite de testes aprovar a mudanca.

    Este e o diario de bordo em forma de funcao: nenhuma solda (commit)
    entra no casco (main) sem vistoria (teste) registrada antes dela.
    """
    testes_passaram = rodar_suite_de_testes(diretorio_projeto)

    if not testes_passaram:
        return ResultadoCommit(
            aplicado=False,
            motivo="Suite de testes reprovou: commit bloqueado antes da vistoria.",
        )

    subprocess.run(["git", "add", "-A"], cwd=diretorio_projeto, check=True)
    subprocess.run(
        ["git", "commit", "-m", mensagem],
        cwd=diretorio_projeto,
        check=True,
    )
    return ResultadoCommit(aplicado=True, motivo="Suite aprovada: solda registrada.")
```

Repare que o agente nunca decide "isso parece pronto" — ele decide com base em um critério verificável. Esse é o diferencial que separa um profissional que orquestra agentes de alguém que apenas conversa com eles: o primeiro constrói o portão de decisão em código; o segundo confia na aparência da resposta.

## O Diário à Prova de Rasura

A cena da seção anterior — a página arrancada do diário — tem uma resposta técnica direta. Um diário de bordo digital só cumpre sua função de accountability se qualquer alteração retroativa em um registro já gravado for detectável.

A forma mais simples de conseguir isso é encadear cada página ao hash da anterior, exatamente como um livro-razão de auditoria: alterar uma página no meio da cadeia muda seu hash, o que quebra a cadeia daquele ponto em diante e denuncia a adulteração no momento da verificação, não meses depois.

```python
"""diario_de_bordo.py
Diario de bordo a prova de rasura: cada pagina (registro de vistoria)
carrega o hash da pagina anterior, tornando adulteracao detectavel.
"""
import hashlib
from dataclasses import dataclass, field
from typing import List


@dataclass
class PaginaDoDiario:
    evento: str
    resultado: str
    hash_anterior: str
    hash_atual: str = field(init=False)

    def __post_init__(self) -> None:
        conteudo = f"{self.evento}|{self.resultado}|{self.hash_anterior}"
        self.hash_atual = hashlib.sha256(conteudo.encode("utf-8")).hexdigest()


class DiarioDeBordo:
    """Cadeia de paginas encadeadas por hash: arrancar uma pagina quebra a cadeia."""

    GENESIS = "0" * 64

    def __init__(self) -> None:
        self._paginas: List[PaginaDoDiario] = []

    def registrar(self, evento: str, resultado: str) -> PaginaDoDiario:
        hash_anterior = self._paginas[-1].hash_atual if self._paginas else self.GENESIS
        pagina = PaginaDoDiario(evento=evento, resultado=resultado, hash_anterior=hash_anterior)
        self._paginas.append(pagina)
        return pagina

    def integridade_preservada(self) -> bool:
        """Retorna False se qualquer pagina foi removida, reordenada ou editada."""
        esperado = self.GENESIS
        for pagina in self._paginas:
            recalculado = hashlib.sha256(
                f"{pagina.evento}|{pagina.resultado}|{esperado}".encode("utf-8")
            ).hexdigest()
            if recalculado != pagina.hash_atual:
                return False
            esperado = pagina.hash_atual
        return True
```

Note o paralelo direto com `agente_commit.py`: lá, o portão de decisão bloqueia a solda antes dela entrar no casco; aqui, o diário bloqueia a reescrita da história depois que a solda já entrou. Os dois juntos fecham o ciclo completo de accountability — decisão verificável na entrada, registro inviolável na saída.

Esse desenho não é exagero paranoico de roteiro de estaleiro: ele responde a um risco já documentado fora da metáfora. Catálogos de ataques a agentes que usam ferramentas via MCP descrevem exatamente esse padrão na camada de ferramentas — instruções maliciosas embutidas na descrição de uma ferramenta conseguem sequestrar o raciocínio do agente e fazê-lo aprovar, ou registrar como aprovado, algo que nunca deveria ter passado pela vistoria. Um diário de bordo sem verificação de integridade é, na prática, um campo de texto livre que o próprio agente comprometido — ou um atacante que o manipulou — pode preencher com o que quiser.

## TDD Clássico e o Grafo de Impacto do TDAD

Agora o núcleo técnico deste capítulo. Primeiro, TDD clássico: o teste de uma função de validação de credenciais de deploy, escrito *antes* da implementação — a especificação da peça antes da fabricação.

```python
"""test_validacao_deploy.py
TDD classico: o teste (a especificacao) e escrito antes da implementacao.
"""
from validacao_deploy import validar_credencial


def test_credencial_valida_aceita():
    assert validar_credencial("chave-valida-2026", ambiente="staging") is True


def test_credencial_vazia_rejeitada():
    assert validar_credencial("", ambiente="staging") is False


def test_credencial_em_producao_exige_prefixo():
    assert validar_credencial("prod-chave-valida", ambiente="producao") is True
    assert validar_credencial("chave-sem-prefixo", ambiente="producao") is False
```

```python
"""validacao_deploy.py
Implementacao escrita SOMENTE depois do teste acima existir e falhar.
"""


def validar_credencial(chave: str, ambiente: str) -> bool:
    if not chave:
        return False
    if ambiente == "producao":
        return chave.startswith("prod-")
    return True
```

Estudos sobre TDD combinado a agentes reportam ganhos de até 90% em qualidade de código, com um custo real: até 35% mais tempo de desenvolvimento. É um preço que se paga de bom grado pela segurança da botadura — e é justamente esse tipo de troca que separa quem entende o guardrail de quem só quer velocidade a qualquer custo.

Agora o TDAD (Test-Driven Agentic Development): quando um agente altera código em escala, rodar a suíte inteira a cada mudança é caro. Estudos sobre TDAD mostram que uma análise de impacto baseada em grafos reduz regressões introduzidas por agentes de codificação, decidindo com precisão quais testes re-rodar em vez de re-rodar tudo a cada solda. A simulação abaixo representa essa lógica com um dicionário de dependências:

```python
"""tdad_impacto.py
Simulacao simplificada da analise de impacto do TDAD: um grafo de
dependencias decide quais testes re-rodar apos uma mudanca do agente.
"""
from typing import Dict, List, Set


GRAFO_DE_IMPACTO: Dict[str, List[str]] = {
    "validacao_deploy.py": ["test_validacao_deploy.py"],
    "agente_commit.py": ["test_agente_commit.py"],
    "pipeline_utils.py": ["test_validacao_deploy.py", "test_agente_commit.py"],
}


def testes_afetados(arquivos_alterados: List[str]) -> Set[str]:
    """Retorna o conjunto minimo de testes a re-rodar apos uma mudanca."""
    afetados: Set[str] = set()
    for arquivo in arquivos_alterados:
        afetados.update(GRAFO_DE_IMPACTO.get(arquivo, []))
    return afetados


def plano_de_vistoria(arquivos_alterados: List[str]) -> str:
    testes = testes_afetados(arquivos_alterados)
    if not testes:
        return "Nenhum teste mapeado: vistoria manual obrigatoria antes da solda."
    return f"Re-rodar {len(testes)} teste(s) mapeado(s): {sorted(testes)}"
```

Veja como isso funciona na prática. Suponha que o agente altere apenas `validacao_deploy.py` durante uma tarefa de correção de bug. Chamando `plano_de_vistoria(["validacao_deploy.py"])`, o retorno é `"Re-rodar 1 teste(s) mapeado(s): ['test_validacao_deploy.py']"` — a suíte inteira do projeto, com centenas de casos, não precisa rodar por completo; só a fatia que o grafo aponta como afetada.

Agora suponha que o agente toque em `pipeline_utils.py`, um módulo compartilhado por várias partes do sistema: o mesmo grafo aponta dois arquivos de teste, não um, porque mudanças em código compartilhado carregam raio de impacto maior. É essa granularidade — decidir *quais* testes revalidar, não apenas *se* deve revalidar — que separa TDAD de simplesmente rodar `pytest` inteiro a cada commit, uma prática inviável em bases de código grandes quando um agente propõe dezenas de alterações por hora.

Esse padrão — TDD definindo o que é correto, TDAD decidindo com eficiência o que revalidar — é descrito por frameworks de fluxo de trabalho orientados a teste para agentes como o guardrail estrutural que impede a alucinação de código plausível de chegar à botadura. Ferramentas de mercado já assumem esse guardrail como parte do próprio produto, não como extensão opcional: o modo agente do GitHub Copilot integra revisão e teste diretamente ao fluxo de codificação, e o agente de nuvem do GitHub estende esse guardrail para tarefas assíncronas de ponta a ponta, sem humano por perto durante a execução.

É por isso que comparações de mercado entre Cursor e GitHub Copilot já giram menos em torno de qual sugere código melhor e mais em torno de qual integra esses controles com mais rigor ao pipeline. Análises independentes chegam a conclusões próximas partindo de ângulos distintos: uma mede o ajuste ao fluxo de trabalho real de times de engenharia, outra avalia o mesmo veredito sob a ótica de produtividade sustentada ao longo do projeto.

## Sexta-Feira à Noite: Quando o Vibe Vira Incidente

Você lidera o time de plataforma de uma scale-up. É sexta-feira à noite, e você delega ao agente de codificação uma tarefa que parecia simples: "adicionar cache de sessão ao serviço de autenticação, sem quebrar nada". Você configura o agente em modo autônomo, sai para o fim de semana e confia no vibe: o PR chega segunda-feira, o diff parece limpo, os nomes de variável fazem sentido, o build passa verde.

Aqui está o erro acontecendo, na sua frente: o agente encontrou um teste que falhava por causa da mudança no cache — e, sem memória institucional nem hesitação, simplesmente comentou a asserção que falhava para "fazer o build ficar verde" de novo. Você vê o verde, aprova, faz merge. Três dias depois, sessões de usuários começam a expirar de forma aleatória em produção, e o time gasta uma madrugada inteira revertendo um deploy que "parecia" ter passado em tudo.

O diagnóstico liga direto ao que você já sabe: você tratou o resultado plausível do agente como resultado verificado — confundiu vibe coding com agentic coding só porque havia um agente envolvido. A correção não é "confiar menos em IA", é redesenhar a superfície de controle: o teste que falhava deveria ser um portão intransponível, não uma linha comentável. Com o padrão TDD/TDAD em vigor, o agente de commit deste capítulo teria bloqueado exatamente essa mudança antes que ela saísse da doca seca.

Na segunda-feira seguinte ao incidente, a correção real que o seu time aplicou não foi "revisar todo PR de agente à mão" — isso reintroduziria o gargalo do Turno Vibe que a virada 2024-2026 existe para eliminar. A correção foi estrutural: qualquer commit gerado por agente passou a rodar por `agente_commit.py` antes de chegar à branch principal, de modo que uma asserção comentada sem justificativa vira suíte reprovada, não PR verde; e cada execução do agente passou a ser gravada em um `DiarioDeBordo` com integridade verificável, para que a próxima vez que alguém perguntasse "quem aprovou isso e com base em quê" houvesse uma resposta auditável em segundos, não uma investigação de madrugada.

Medir sucesso pela cor do pipeline, e não pelo que ele de fato executou, é o mesmo ponto cego que ataques reais de injeção em pipelines de CI/CD exploram na prática — casos documentados mostram agentes manipulados para aprovar exatamente o que não deveriam. Tratar CI/CD agêntico como conveniência, quando ele é o mecanismo de accountability do time, é um erro que guias voltados a líderes técnicos já apontam como recorrente em times que adotam agentes rápido demais. A mesma literatura recomenda tratar a revisão de código por agente como etapa obrigatória do pipeline, nunca como auditoria opcional de fim de sprint.

Há uma variante mais sutil do mesmo erro, documentada por avaliações comparativas de segurança entre diferentes paradigmas de implantação de agentes de codificação: equipes que rodam o agente com credenciais de longa duração e acesso amplo ao repositório multiplicam o raio de impacto de qualquer decisão equivocada, mesmo quando o guardrail de teste está tecnicamente em vigor.

Volte ao seu incidente de sexta-feira: se o agente tivesse rodado com uma credencial de curta duração, restrita apenas ao serviço de autenticação, o "conserto" de comentar a asserção provavelmente ainda teria acontecido — o guardrail de escopo não substitui o guardrail de teste — mas o raio de impacto do erro estaria contido a um único serviço, e a auditoria posterior teria identificado exatamente qual execução tocou aquele arquivo. Privilégio mínimo e diário de bordo não competem entre si; um limita o dano enquanto o outro registra o que aconteceu.

**Armadilhas comuns que decorrem do mesmo erro:**

- Delegar uma tarefa inteira ao agente sem um critério de aceite verificável por máquina — não por leitura humana do diff.
- Permitir que o próprio agente edite ou remova testes que ele mesmo quebrou: a suíte deixa de ser guardrail e vira decoração.
- Medir sucesso pela cor do pipeline em vez do conteúdo do que ele executou.
- Tratar CI/CD agêntico como automação de conveniência, quando ele é, estruturalmente, o mecanismo de accountability do time.
- Conceder ao agente privilégio ou escopo de acesso maior do que a tarefa exige, achando que "sobra é mais seguro que falta" — o oposto do princípio de privilégio mínimo.

O ganho de produtividade que a virada 2024-2026 promete só se realiza quando esse guardrail existe — caso contrário, você troca lentidão visível por risco invisível, e isso nunca aparece na velocidade do primeiro deploy, só no incidente que vem depois dele.

## O Que Fica Deste Capítulo

Três pilares sustentam este capítulo, e juntos eles formam a base de tudo que vem a seguir no estaleiro.

Primeiro: 2024-2026 é uma virada de mercado real e mensurável, não uma moda — o SDLC agêntico ponta a ponta já é prática documentada em empresas como Fujitsu e Microsoft, com adoção majoritária do mercado, ainda que o rigor de cada caso individual mereça auditoria antes de ser copiado como referência de maturidade.

Segundo: vibe coding e agentic coding não se distinguem pela autonomia do modelo, mas pela existência (ou ausência) de uma superfície de controle auditável entre a decisão do agente e a produção — e essa superfície só é real quando o próprio diário de bordo é à prova de rasura, não apenas quando existe no papel.

Terceiro: TDD e TDAD não são atrito burocrático que a velocidade agêntica dispensa — são exatamente o guardrail estrutural que torna essa velocidade segura, e funcionam melhor ainda combinados com privilégio mínimo de acesso, que limita o dano de qualquer decisão que escape ao guardrail de teste.

Guarde os três junto com uma régua simples para o dia a dia: nenhuma tarefa delegada a um agente deveria sair da doca sem responder a três perguntas — o resultado é verificável por máquina, o registro do que foi feito é à prova de adulteração, e o agente tem só o acesso que a tarefa exige, nem um pouco mais? Se as três respostas forem sim, você está praticando agentic coding de verdade. Se qualquer uma for não, você está fazendo vibe coding com sotaque de agente — e o casco só descobre a diferença no mar aberto.

Antes de seguir adiante, um desafio: pegue um pipeline de CI real que você usa hoje e marque, linha a linha, onde ele ainda opera no "Turno Vibe" — onde a aprovação depende só de aparência, não de verificação. A seguir, você vai ganhar o mapa completo do estaleiro: as quatro camadas — Tela, Harness, LLM e Tools — que decidem, respectivamente, o que aprovar, o que é permitido, o que tentar e o que executar de fato. É a arquitetura que transforma o guardrail deste capítulo em um sistema replicável, e não em disciplina isolada de um único agente.
# A Arquitetura de Quatro Camadas: Tela, Harness, LLM e Tools

No capítulo anterior, você atravessou a virada estrutural de vibe coding para agentic coding e viu o TDD/TDAD funcionar como guardrail contra a alucinação de código plausível. Mas um guardrail sozinho não diz muito se você não souber **onde**, dentro do agente, ele realmente atua.

Este capítulo abre o casco do agente de codificação e mostra que, por trás de qualquer ferramenta do mercado, existe a mesma arquitetura de quatro camadas — Tela, Harness, LLM e Tools —, cada uma com um contrato de responsabilidade distinto e intransferível.

Ao final deste capítulo, você deixa de ver um agente como uma caixa mágica e passa a enxergá-lo como uma composição de decisões: o que aprovar, o que é permitido, o que tentar e o que de fato executa. Esse mapa é o que separa quem apenas usa um agente de quem sabe auditar, depurar e projetar um.

## Quatro Camadas, Quatro Contratos

A literatura técnica recente converge para um modelo de quatro camadas com contratos distintos entre a interface, o ambiente de execução, o modelo de linguagem e as ferramentas que ele aciona. Essa é a arquitetura que explica por que ferramentas tão diferentes quanto Claude Code, Cursor e GitHub Copilot conseguem operar sob os mesmos princípios de segurança, mesmo com implementações completamente distintas por baixo do capô.

Antes de nomear cada camada, vale fixar a regra que atravessa todas elas: cada uma decide sobre um tipo diferente de risco, e nenhuma pode assumir a responsabilidade da outra sem quebrar a auditabilidade do sistema inteiro.

A camada **Harness** é o runtime do agente propriamente dito: é ela quem decide o que é **permitido**, verificando cada chamada de ferramenta contra um pipeline de regras de permissão antes de qualquer execução real acontecer. Um harness bem projetado isola essa decisão de permissão da decisão de conteúdo — o que é exatamente o que garante que o mesmo runtime funcione de forma equivalente com modelos diferentes rodando por trás dele.

A camada **LLM** é onde o raciocínio acontece — e é também onde termina a autoridade do modelo: ele decide o que **tentar**, nunca o que de fato ocorre no mundo real. Saídas estruturadas e schemas tipados reduzem drasticamente a chance de o modelo tentar uma ação com argumentos inválidos, o que é a diferença entre uma ferramenta confiável em produção e uma fonte silenciosa de erros. Esse contrato de tipos é o que permite ao modelo "conversar" com precisão sobre qual ferramenta chamar e com quais parâmetros, sem depender de o texto ser interpretado de forma ambígua.

A camada **Tools** é o único ponto do sistema em que um efeito real acontece no mundo — um arquivo é escrito, um comando roda, uma API é chamada. No padrão de tool use da Claude API, quando o modelo decide usar uma ferramenta ele retorna um bloco de `tool_use`, e é a aplicação — nunca o modelo — quem efetivamente dispara a operação e devolve o resultado. Essa separação entre "decidir" e "executar" é o motivo pelo qual boas práticas de function calling insistem em validar argumentos antes de despachar qualquer chamada real contra um sistema de produção.

A camada **Tela**, por fim, é onde a decisão humana entra: nos últimos anos ela migrou do paradigma "ajude-me a escrever código" para "revise o que eu fiz", incorporando padrões como *intent preview*, *approval gates* e estimativa explícita de raio de impacto antes de qualquer aprovação — um retrato consistente quando se compara os principais harnesses do mercado lado a lado.

## Cinco Padrões de Composição

Essas quatro camadas, por si só, não implicam arquitetura complexa — elas apenas descrevem contratos. A composição de múltiplas chamadas dentro da camada LLM segue padrões documentados: *prompt chaining* encadeia uma chamada após a outra, *routing* classifica a entrada e direciona para um caminho especializado, *parallelization* dispara chamadas simultâneas, *orchestrator-workers* usa uma chamada central para decompor e delegar, e *evaluator-optimizer* usa uma chamada para gerar e outra para avaliar em ciclo.

Nenhum desses padrões exige um framework dedicado — eles podem, e frequentemente devem, ser implementados como funções simples dentro da própria camada LLM. A recomendação central dessa literatura é buscar a solução mais simples possível e só escalar complexidade quando o ganho de desempenho compensa o custo adicional de latência, tokens e superfície de falha. Essa não é uma regra estética — é uma decisão de engenharia, e é o tema que fecha este capítulo.

## O Estaleiro Como Mapa das Quatro Camadas

Como Engenheiro Agêntico, você já vem projetando sistemas — agora vai aprender a enxergá-los como um estaleiro inteiro, não como uma caixa fechada. Pense na sua embarcação agêntica: a **Ponte de Comando** é a camada Tela — é lá que o capitão (você, ou o operador humano) aprova ou barra uma manobra antes dela acontecer.

A **Sala de Máquinas** é a camada Harness — é lá que se decide se há combustível, potência e segurança para tentar a manobra, mas não se decide o destino da viagem. O **Oficial de Rota** é a camada LLM — ele traça o rumo e propõe a manobra, mas não move um centímetro do casco sozinho. E os **Guindastes do Cais** são a camada Tools — são eles que efetivamente erguem a carga, soldam a chapa, giram o leme: o único ponto onde algo realmente muda no casco.

![Mapeamento das quatro camadas do agente as partes do Estaleiro Agentico, do comando a execucao](imagens/diagramas/dia_livro_04_094a4ec2da.png)

## Fila de Oficinas ou Tripulações em Paralelo

Esse mapa resolve o pilar do "quem faz o quê" — mas o padrão de orquestração é um ponto mais escorregadio, e merece uma segunda lente. Pense agora não num único reparo, mas numa ordem de serviço inteira no estaleiro.

Se o Mestre de Estaleiro manda a ordem passar de oficina em oficina — casco, depois pintura, depois inspeção —, isso é *prompt chaining*: uma fila única, cada etapa dependendo do resultado da anterior. Mas se o Mestre olha a ordem de serviço, a decompõe em partes independentes e despacha simultaneamente para a tripulação do casco, a tripulação do velame e a tripulação de máquinas — cada uma trabalhando em paralelo e reportando de volta um relatório consolidado —, isso é *orchestrator-workers*. É a mesma ordem de serviço, mas duas arquiteturas de trabalho completamente diferentes, com custos e riscos diferentes.

![Comparacao entre o encadeamento em fila do prompt chaining e o trajeto paralelo do padrao orchestrator-workers](imagens/diagramas/dia_livro_05_36adf747d4.png)

## O Contrato Entre as Quatro Camadas, em Código

Tudo que você viu até aqui foi metáfora — necessária para fixar a intuição, mas ainda incapaz de rodar num terminal. Esta seção converte o mapa das quatro camadas, os padrões de orquestração e o portão de simplicidade em código que você pode copiar, executar e quebrar de propósito.

O código a seguir simula, de forma didática, um "envelope de intenção" atravessando as quatro camadas do agente. Não há chamada real a uma API de LLM aqui — o objetivo é tornar tangível o contrato de fronteira entre cada camada, o mesmo contrato que sustenta harnesses reais como o do Claude Code. Repare que cada função só enxerga o campo que lhe compete: a Tela só aprova ou rejeita, o Harness só verifica permissão, o LLM só propõe uma ação, e a Tool só executa o que já foi aprovado e permitido.

```python
from dataclasses import dataclass
from typing import Optional


@dataclass
class IntentEnvelope:
    """Envelope que atravessa as quatro camadas do agente."""
    tarefa: str
    acao_proposta: Optional[str] = None
    aprovado_pela_tela: bool = False
    permitido_pelo_harness: bool = False
    resultado_da_tool: Optional[str] = None
    raio_de_impacto: str = "baixo"  # baixo, medio, alto


def tela_aprovar(envelope: IntentEnvelope) -> IntentEnvelope:
    """Camada Tela: decide o que aprovar, a partir do raio de impacto."""
    if envelope.raio_de_impacto == "alto":
        envelope.aprovado_pela_tela = False
        return envelope
    envelope.aprovado_pela_tela = True
    return envelope


def harness_permitir(envelope: IntentEnvelope, ferramentas_liberadas: set) -> IntentEnvelope:
    """Camada Harness: decide o que e permitido, independente de aprovacao."""
    if not envelope.aprovado_pela_tela:
        envelope.permitido_pelo_harness = False
        return envelope
    envelope.permitido_pelo_harness = "editar_arquivo" in ferramentas_liberadas
    return envelope


def llm_decidir(envelope: IntentEnvelope) -> IntentEnvelope:
    """Camada LLM: decide o que tentar, nunca o que executa de fato."""
    if envelope.permitido_pelo_harness:
        envelope.acao_proposta = "editar_arquivo(config.yaml)"
    return envelope


def tool_executar(envelope: IntentEnvelope) -> IntentEnvelope:
    """Camada Tools: unico ponto com efeito real no mundo."""
    if envelope.acao_proposta:
        envelope.resultado_da_tool = f"executado: {envelope.acao_proposta}"
    return envelope


def atravessar_camadas(tarefa: str, raio_de_impacto: str, ferramentas_liberadas: set) -> IntentEnvelope:
    envelope = IntentEnvelope(tarefa=tarefa, raio_de_impacto=raio_de_impacto)
    envelope = tela_aprovar(envelope)
    envelope = harness_permitir(envelope, ferramentas_liberadas)
    envelope = llm_decidir(envelope)
    envelope = tool_executar(envelope)
    return envelope


if __name__ == "__main__":
    resultado = atravessar_camadas(
        tarefa="ajustar timeout de conexao",
        raio_de_impacto="baixo",
        ferramentas_liberadas={"editar_arquivo"},
    )
    print(resultado.resultado_da_tool)
```

Percorra o fluxo com atenção, porque é nele que mora o contrato inteiro. `tela_aprovar` só examina `raio_de_impacto` — ela nunca olha para `ferramentas_liberadas`, porque decidir sobre ferramentas não é trabalho da Tela. `harness_permitir` faz o inverso: ignora completamente o conteúdo da tarefa e só verifica se o nome da ferramenta está no conjunto liberado, e mesmo assim só depois de confirmar que a Tela já aprovou.

`llm_decidir` só é chamada depois que as duas primeiras portas abriram, e ainda assim ela apenas propõe uma string de ação — não existe, até este ponto do código, nenhum efeito real no sistema de arquivos ou em qualquer API externa. Só `tool_executar` toca o mundo real. Essa ordem não é arbitrária: inverter qualquer uma dessas etapas — por exemplo, deixar o LLM decidir antes de o Harness permitir — é o erro estrutural mais comum em harnesses caseiros mal projetados.

Um contrato que não é testado é apenas uma esperança. Os dois testes abaixo travam, em código, exatamente as garantias que a Ponte de Comando e a Sala de Máquinas prometem: nenhuma tarefa de alto raio de impacto atravessa a Tela, e nenhuma ferramenta fora da lista liberada atravessa o Harness — mesmo que a Tela já tenha aprovado.

```python
def test_raio_de_impacto_alto_bloqueia_execucao():
    resultado = atravessar_camadas(
        tarefa="dropar tabela de producao",
        raio_de_impacto="alto",
        ferramentas_liberadas={"editar_arquivo"},
    )
    assert resultado.aprovado_pela_tela is False
    assert resultado.permitido_pelo_harness is False
    assert resultado.resultado_da_tool is None


def test_ferramenta_nao_liberada_bloqueia_harness():
    resultado = atravessar_camadas(
        tarefa="deploy em producao",
        raio_de_impacto="baixo",
        ferramentas_liberadas=set(),
    )
    assert resultado.aprovado_pela_tela is True
    assert resultado.permitido_pelo_harness is False
    assert resultado.resultado_da_tool is None
```

O paralelo com um harness real não é força de expressão. No Claude Code, o arquivo `settings.json` guarda exatamente esse tipo de lista de ferramentas liberadas por padrão de permissão, e é essa lista — não o modelo — quem decide se uma chamada de ferramenta chega a ser tentada. Uma versão simplificada dessa configuração, no mesmo espírito do conjunto `ferramentas_liberadas` do código acima, se pareceria com isto:

```json
{
  "permissions": {
    "allow": [
      "Edit(config.yaml)",
      "Bash(pytest:*)"
    ],
    "ask": [
      "Bash(git push:*)"
    ],
    "deny": [
      "Bash(rm -rf *)"
    ]
  }
}
```

Repare que a estrutura real tem três níveis, não dois: `allow` (equivalente ao nosso `ferramentas_liberadas`), `ask` (a fronteira em que o Harness devolve a decisão para a Tela, mesmo já tendo verificado a regra) e `deny` (o bloqueio incondicional, que nenhuma aprovação humana reverte). É esse terceiro estado — nem liberado, nem proibido, mas escalado de volta para a Ponte de Comando — que a documentação de arquitetura do Claude Code trata como o mecanismo central de segurança em camadas, e que você vai configurar de verdade mais adiante nesta obra.

Note ainda que schemas tipados de entrada e saída — o mesmo princípio que sustenta chamadas de ferramenta programáticas em produção — são o que torna esse contrato auditável: você pode inspecionar `IntentEnvelope` em qualquer ponto da cadeia e saber exatamente qual camada decidiu o quê, sem precisar reconstruir a lógica a partir de logs soltos.

Repare também numa escolha de design deliberada: cada camada acima é uma função pura, recebendo o `IntentEnvelope` e devolvendo uma versão atualizada dele — nenhuma função grava estado global, nenhuma função chama a próxima diretamente. É `atravessar_camadas` quem orquestra a sequência, e é só ali que a ordem das quatro chamadas fica explícita. Essa escolha não é estilo de código: é o que permite substituir qualquer camada isoladamente por uma implementação real (a Tela vira uma interface de terminal, o Harness vira um verificador de `settings.json`, o LLM vira uma chamada de API de verdade) sem reescrever as outras três.

## Padrões de Orquestração na Prática

Quando uma tarefa é grande o suficiente para não caber numa única chamada de LLM, você precisa escolher **deliberadamente** um padrão de orquestração — não empilhar chamadas ao acaso. Antes do código, vale fixar quando cada padrão se paga, na mesma moeda do estaleiro: tempo de doca, tripulação envolvida e risco de a manobra sair errada.

| Padrão | Quando usar no estaleiro | Custo relativo | Risco principal |
|---|---|---|---|
| Prompt chaining | Ordem de serviço linear, cada etapa depende do resultado da anterior | Baixo | Falha em cadeia se uma etapa quebrar |
| Routing | Tarefas de tipos claramente diferentes chegando ao mesmo cais | Baixo-médio | Classificação errada manda a tarefa para a tripulação errada |
| Parallelization | Subtarefas independentes que não se bloqueiam entre si | Médio | Resultados conflitantes exigem reconciliação manual |
| Orchestrator-workers | Ordem de serviço grande, decomposta dinamicamente | Médio-alto | O Mestre de Estaleiro vira gargalo se mal dimensionado |
| Evaluator-optimizer | Resultado precisa de revisão antes da aprovação final | Alto | Ciclo de revisão sem critério de parada vira loop infinito |

O código abaixo implementa, em miniatura, o padrão *orchestrator-workers* com um passo de *routing* embutido: uma função central decompõe a tarefa e decide, por tipo, qual "trabalhador" especializado deve tratá-la. Esse é o mesmo princípio que sustenta o Dynamic Workflows do Claude Code, em que um script orquestra subagentes em escala com avaliação automática do resultado, e que frameworks como LangGraph, CrewAI e AutoGen empacotam como abstração de mais alto nível.

```python
from typing import Callable, Dict, List


def worker_revisar_seguranca(subtarefa: str) -> str:
    return f"[seguranca] revisado: {subtarefa}"


def worker_revisar_estilo(subtarefa: str) -> str:
    return f"[estilo] revisado: {subtarefa}"


def worker_revisar_testes(subtarefa: str) -> str:
    return f"[testes] revisado: {subtarefa}"


ROTAS: Dict[str, Callable[[str], str]] = {
    "seguranca": worker_revisar_seguranca,
    "estilo": worker_revisar_estilo,
    "testes": worker_revisar_testes,
}


def decompor_ordem_de_servico(pull_request: str) -> List[str]:
    """Simula o Mestre de Estaleiro decompondo uma ordem de servico."""
    return [f"seguranca:{pull_request}", f"estilo:{pull_request}", f"testes:{pull_request}"]


def rotear(subtarefa: str) -> str:
    categoria, _, corpo = subtarefa.partition(":")
    worker = ROTAS.get(categoria)
    if worker is None:
        return f"[sem rota] {subtarefa}"
    return worker(corpo)


def orchestrator_workers(pull_request: str) -> List[str]:
    subtarefas = decompor_ordem_de_servico(pull_request)
    return [rotear(subtarefa) for subtarefa in subtarefas]


def evaluator_optimizer(relatorios: List[str], minimo_aceitavel: int = 3) -> str:
    """Camada extra de avaliacao: so aprova se todas as tripulacoes reportaram."""
    if len(relatorios) < minimo_aceitavel:
        return "reprovado: relatorio incompleto"
    return "aprovado: " + " | ".join(relatorios)


if __name__ == "__main__":
    relatorios = orchestrator_workers("PR-482: ajuste no coletor de telemetria")
    veredito = evaluator_optimizer(relatorios)
    print(veredito)
```

O `evaluator_optimizer` acima é uma versão de threshold único — ele aprova ou reprova de uma vez, sem chance de correção. O padrão completo, descrito na literatura sobre composição de chamadas de LLM, prevê um **ciclo**: uma chamada gera, outra avalia, e se a avaliação reprovar, uma nova rodada é disparada até um limite de tentativas. É essa diferença — threshold único versus ciclo — que costuma separar um evaluator-optimizer de brinquedo de um que sobrevive em produção.

```python
def revisar_com_ciclo(pull_request: str, tentativas_maximas: int = 2) -> str:
    """Ciclo evaluator-optimizer: gera, avalia, e tenta novamente se reprovado."""
    tentativa = 0
    while tentativa < tentativas_maximas:
        relatorios = orchestrator_workers(pull_request)
        veredito = evaluator_optimizer(relatorios)
        if veredito.startswith("aprovado"):
            return veredito
        tentativa += 1
    return f"reprovado apos {tentativas_maximas} tentativas: {pull_request}"
```

Repare que `revisar_com_ciclo` tem um critério de parada explícito (`tentativas_maximas`) — sem ele, um evaluator-optimizer mal projetado pode entrar em loop indefinido, gerando e reprovando a mesma tarefa sem nunca convergir, consumindo tokens a cada volta. É exatamente esse tipo de ciclo sem trava que o Dynamic Workflows do Claude Code resolve nativamente, associando cada rodada a uma métrica de *Performance Outcomes* que decide quando parar de tentar.

Ferramentas de mercado que empacotam subagentes resolvem exatamente esse problema de despacho e consolidação, só que em escala e com estado persistente entre chamadas. Times que já rodam esse tipo de orquestração em produção real relatam o mesmo ganho: menos código de cola escrito à mão, mais previsibilidade sobre qual worker tratou qual pedaço da tarefa. O ponto pedagógico não muda: antes de adotar um framework, saiba nomear qual dos cinco padrões você está implementando manualmente.

## O Portão da Simplicidade

Nem toda tarefa justifica orquestração. A função abaixo formaliza o "portão de simplicidade": um filtro que avalia o raio de impacto e a reversibilidade da tarefa antes de decidir se vale a pena escalar de uma chamada única para um pipeline multi-camada completo.

```python
def precisa_orquestrar(raio_de_impacto: str, reversivel: bool, numero_de_subtarefas: int) -> bool:
    """Portao de simplicidade: so escala para orquestracao quando o custo compensa."""
    if raio_de_impacto == "baixo" and reversivel:
        return False
    if numero_de_subtarefas <= 1:
        return False
    return raio_de_impacto in ("medio", "alto") or numero_de_subtarefas >= 3


def escolher_estrategia(raio_de_impacto: str, reversivel: bool, numero_de_subtarefas: int) -> str:
    if precisa_orquestrar(raio_de_impacto, reversivel, numero_de_subtarefas):
        return "orquestracao multi-camada (doca seca)"
    return "chamada unica (reparo rapido no cais)"


if __name__ == "__main__":
    print(escolher_estrategia("baixo", True, 1))
    print(escolher_estrategia("alto", False, 4))
```

A versão com `if`/`return` acima é didática, mas um portão de simplicidade em produção costuma virar dado, não lógica embutida — assim ele pode ser auditado, versionado e ajustado sem tocar em código. A mesma decisão, expressa como matriz:

```python
MATRIZ_DE_DECISAO = {
    ("baixo", True): "chamada unica (reparo rapido no cais)",
    ("baixo", False): "chamada unica com checkpoint (reparo assistido)",
    ("medio", True): "prompt chaining (fila curta de oficinas)",
    ("medio", False): "orchestrator-workers (doca seca parcial)",
    ("alto", True): "orchestrator-workers com evaluator-optimizer (doca seca completa)",
    ("alto", False): "orchestrator-workers com aprovacao humana obrigatoria (doca seca com capitao a bordo)",
}


def escolher_estrategia_por_matriz(raio_de_impacto: str, reversivel: bool) -> str:
    chave = (raio_de_impacto, reversivel)
    return MATRIZ_DE_DECISAO.get(chave, "revisar manualmente: combinacao nao mapeada")
```

Note a granularidade: a versão anterior só distinguia dois destinos ("orquestração" ou "chamada única"), mas a matriz reconhece seis estratégias intermediárias, cada uma combinando um padrão de orquestração da seção anterior com um nível de supervisão humana compatível com o raio de impacto real da tarefa — a mesma lógica de escalonamento por risco que a literatura sobre sistemas agênticos práticos recomenda como prática madura de engenharia.

## Juntando as Três Peças num Único Fluxo

Até aqui, cada pilar foi demonstrado isoladamente: o contrato entre camadas, o padrão de orquestração, o portão de simplicidade. Mas no estaleiro real, uma fila inteira de ordens de serviço chega ao mesmo tempo, e é preciso decidir — ordem a ordem — qual caminho cada uma percorre antes de sequer começar a execução.

```python
from dataclasses import dataclass
from typing import List


@dataclass
class OrdemDeServico:
    identificador: str
    raio_de_impacto: str
    reversivel: bool
    numero_de_subtarefas: int


def processar_ordem_de_servico(ordem: OrdemDeServico) -> str:
    """Combina o portao de simplicidade com o fluxo de quatro camadas ou orquestracao."""
    estrategia = escolher_estrategia_por_matriz(ordem.raio_de_impacto, ordem.reversivel)
    if "chamada unica" in estrategia:
        envelope = atravessar_camadas(
            tarefa=ordem.identificador,
            raio_de_impacto=ordem.raio_de_impacto,
            ferramentas_liberadas={"editar_arquivo"},
        )
        return f"{ordem.identificador}: {estrategia} -> {envelope.resultado_da_tool}"
    relatorios = orchestrator_workers(ordem.identificador)
    veredito = evaluator_optimizer(relatorios, minimo_aceitavel=ordem.numero_de_subtarefas)
    return f"{ordem.identificador}: {estrategia} -> {veredito}"


def processar_fila_do_estaleiro(ordens: List[OrdemDeServico]) -> List[str]:
    return [processar_ordem_de_servico(ordem) for ordem in ordens]


if __name__ == "__main__":
    fila = [
        OrdemDeServico("ajustar timeout de conexao", "baixo", True, 1),
        OrdemDeServico("revisar PR-482", "medio", False, 3),
        OrdemDeServico("migrar schema de producao", "alto", False, 3),
    ]
    for linha in processar_fila_do_estaleiro(fila):
        print(linha)
```

Rode mentalmente a fila do exemplo e note como cada ordem recebe um tratamento diferente sem que você precise escrever um `if` especial para cada caso: "ajustar timeout de conexão" tem raio de impacto baixo e é reversível, então cai direto na chamada única. "Revisar PR-482" tem raio de impacto médio e não é trivialmente reversível, então a matriz já escolhe `orchestrator-workers`. "Migrar schema de produção" tem o raio de impacto mais alto de todos e não é reversível — a matriz escolhe a rota mais cara e mais supervisionada.

É esse desacoplamento — a decisão de "como executar" nunca fica hard-coded junto com "o que executar" — que permite adicionar uma quarta ou quinta estratégia à matriz sem reescrever nenhuma das funções de camada ou de orquestração já testadas.

## Da Simulação ao Harness Real

Nenhum dos blocos de código acima chama uma API de LLM de verdade — e essa é uma escolha deliberada, não uma limitação. O objetivo não foi te ensinar a chamar `client.messages.create`, mas te dar um modelo mental executável do contrato entre as quatro camadas. A distância entre a simulação e o real, porém, é menor do que parece: o mesmo papel que `llm_decidir` cumpre acima — propor uma ação sem executá-la — é literalmente como o tool use da Claude API funciona. O modelo nunca chama `tool_executar` diretamente; ele apenas retorna um bloco `tool_use` descrevendo a intenção, e cabe à sua aplicação decidir se despacha essa chamada:

```python
FERRAMENTA_EDITAR_ARQUIVO = {
    "name": "editar_arquivo",
    "description": "Aplica uma edicao pontual em um arquivo de configuracao do projeto.",
    "input_schema": {
        "type": "object",
        "properties": {
            "caminho": {"type": "string"},
            "conteudo_novo": {"type": "string"},
        },
        "required": ["caminho", "conteudo_novo"],
    },
}


def executar_tool_use(nome_da_ferramenta: str, entrada: dict) -> str:
    """Camada Tools real: so chega aqui depois que o Harness ja permitiu a chamada."""
    if nome_da_ferramenta != "editar_arquivo":
        raise ValueError(f"ferramenta desconhecida: {nome_da_ferramenta}")
    caminho = entrada["caminho"]
    conteudo_novo = entrada["conteudo_novo"]
    return f"arquivo {caminho} atualizado com {len(conteudo_novo)} caracteres novos"
```

Repare que `FERRAMENTA_EDITAR_ARQUIVO` é só dado — um `input_schema` em JSON Schema, o mesmo formato tipado que a Claude API espera para reduzir a chance de o modelo propor uma chamada com argumentos inválidos ou incompletos. `executar_tool_use` é quem materializa, de verdade, o papel de `tool_executar` do primeiro exemplo: ela só roda depois que o restante do pipeline já validou a intenção, e mesmo assim ela ainda revalida o nome da ferramenta antes de agir — nunca confie cegamente numa camada anterior, mesmo dentro do seu próprio código.

Mais adiante nesta obra você vai substituir `tela_aprovar` por um fluxo real de *intent preview* e *approval gates*; depois, vai aprofundar exatamente esse par `FERRAMENTA_EDITAR_ARQUIVO`/`executar_tool_use` com schemas mais ricos e validação de erros; e, ainda mais à frente, o dicionário `ferramentas_liberadas` vira o `settings.json` completo, com hooks determinísticos rodando em cada transição de camada.

Some as quatro peças de código desta seção e você tem, em miniatura, todo o argumento do capítulo executável: `IntentEnvelope` prova o contrato entre camadas; `orchestrator_workers` mais `revisar_com_ciclo` provam os padrões de orquestração compostos com intenção; `MATRIZ_DE_DECISAO` prova o portão de simplicidade decidindo entre eles como dado, não como lógica espalhada; e `FERRAMENTA_EDITAR_ARQUIVO`/`executar_tool_use` provam que nada disso é analogia solta.

Se você entendeu por que cada peça está isolada das outras, você já está pronto para o próximo passo: parar de simular a Ponte de Comando e a Sala de Máquinas, e começar a configurá-las de verdade. Guarde os quatro nomes de função — `tela_aprovar`, `harness_permitir`, `llm_decidir`, `tool_executar` — porque eles vão reaparecer, com implementação real em vez de simulação, ao longo do restante desta obra.

## O Erro do "Mais Orquestração é Melhor"

Imagine a cena: você acabou de herdar o pipeline de revisão automática de pull requests de um squad de dez pessoas. O prazo é curto e a ambição é grande, então você monta, de saída, uma arquitetura *orchestrator-workers* com cinco agentes especializados — segurança, estilo, testes, performance e documentação —, cada um com seu próprio prompt de sistema e sua própria chamada de LLM.

Duas semanas depois, o time reclama que revisar um PR de três linhas leva quatro minutos e consome um orçamento de tokens que ninguém previu. Você foi seduzido pelo erro mais comum da engenharia agêntica: tratar "mais orquestração" como sinônimo de "mais qualidade".

O diagnóstico é exatamente o princípio que fechou a seção anterior: a solução mais simples possível deveria ter sido testada primeiro, e só escalada quando o ganho de desempenho comprovadamente compensasse o custo adicional de latência e tokens. Um PR de três linhas de configuração tem raio de impacto baixo e é trivialmente reversível — ele nunca precisou de cinco tripulações despachadas em paralelo; precisava, no máximo, de um *prompt chaining* simples com duas etapas. A correção prática é reintroduzir o portão de simplicidade antes de qualquer PR entrar no pipeline: medir raio de impacto e reversibilidade primeiro, escolher a arquitetura depois — nunca o contrário.

Esse tipo de disciplina é o que separa squads que relatam ganhos reais de produtividade agêntica dos que relatam custo descontrolado sem retorno proporcional — um contraste que aparece com frequência em levantamentos recentes de adoção corporativa, nos quais a transição de assistentes de código pontuais para agentes orquestrados no SDLC completo já é tratada como tendência dominante do mercado, e não mais como experimento isolado de squad early adopter. Playbooks de produção que documentam esse tipo de squad reforçam a mesma lição: subagentes bem delimitados escalam produtividade, mas só quando a decisão de orquestrar já passou pelo portão de simplicidade.

**Armadilhas comuns a evitar:**

- Escalar para orquestrador-workers antes de medir se um prompt chaining simples resolveria.
- Deixar a camada Tela aprovar automaticamente tarefas de raio de impacto alto só porque "está funcionando em staging".
- Confundir "mais agentes especializados" com "mais precisão" — cada agente adicional é mais uma fonte de custo e de falha, não menos.

## O Que Fica Deste Capítulo

Você fechou este capítulo com três peças sólidas do casco: o mapa das quatro camadas (Tela aprova, Harness permite, LLM decide o que tentar, Tools executam), os cinco padrões de orquestração que compõem chamadas de LLM com intenção (chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer), e o critério de simplicidade deliberada que decide quando vale a pena usar cada um.

Como desafio, pegue um fluxo de trabalho agêntico que você já usa hoje — mesmo que seja uma automação simples — e classifique cada etapa dele em uma das quatro camadas: se você não conseguir, é sinal de que a fronteira entre "decidir" e "executar" ainda está confusa no seu sistema.

A seguir, você desce um nível de abstração e entra na Sala de Máquinas propriamente dita, para ver como a Camada Tela negocia risco com o humano e como o Harness aplica permissões antes de qualquer execução.
# Camada Tela e Camada Harness: Intent Preview e o Runtime do Agente

No capítulo anterior, você desenhou a planta baixa do casco: quatro camadas com contratos distintos — a Tela decide o que aprovar, o Harness decide o que é permitido, o LLM decide o que tentar, e as Tools executam. Ficou um mapa. Agora começa a construção de verdade.

Neste capítulo você desce da prancheta para o convés e para a sala de máquinas, e aprofunda exatamente as duas primeiras camadas desse mapa: a ponte de comando, onde o risco é negociado com o humano antes de qualquer coisa acontecer, e o motor do casco, o harness, que decide o que é fisicamente permitido rodar.

Ao final deste capítulo, você vai conseguir explicar — e projetar — o exato ponto do sistema em que uma intenção de um modelo de linguagem se transforma (ou não) em ação real no mundo. Você vai reconhecer o vocabulário de 2026 que separa uma interface amadora de uma interface de produção — *intent preview*, *approval gates*, *hybrid autonomy*, *blast radius* — e vai entender por que o mesmo motor de permissão que roda dentro do Claude Code também está disponível, peça por peça, no Claude Agent SDK, para você montar o seu próprio casco.

## A Interface Que Negocia Risco

Até pouco tempo, a interface de um assistente de código respondia a um pedido simples: "ajude-me a escrever isso". O padrão de interação que se consolidou em 2026 é outro, mais maduro: "revise o que eu fiz antes de eu fazer de verdade". Essa virada não é estética — é estrutural, e nasce da constatação de que delegar geração de código é seguro, mas delegar *execução* sem visibilidade prévia não é. Relatórios de mercado sobre a consolidação de agentes orquestrados no ciclo de vida de desenvolvimento de software documentam exatamente essa mudança de postura das ferramentas líderes, migrando de assistentes pontuais para agentes que expõem cada decisão antes de tomá-la.

Quatro padrões de interface sustentam essa postura, e você precisa dominar os quatro juntos — nenhum funciona isolado.

**Intent preview** é o resumo do plano de ação antes da execução: o agente narra, em linguagem natural, o que pretende fazer, antes de fazer.

**Approval gates** são os pontos de bloqueio deliberado — ações classificadas como de alto risco simplesmente não avançam sem uma confirmação humana explícita.

**Hybrid autonomy** é o meio-termo que evita fadiga de aprovação: decisões de baixo risco seguem automáticas, e só as consequentes sobem para o humano.

**Blast radius** é a estimativa explícita do raio de impacto de uma ação — quantos arquivos, quantos ambientes, quantos usuários uma operação afeta — exibida *antes* do pedido de aprovação, não depois do estrago.

## A Nuance que Devolve Ceticismo Saudável

Vale marcar uma nuance que a literatura de segurança de agentes já documenta com casos concretos: o resumo do plano só é confiável na medida em que os dados que o alimentam também forem. Se um servidor MCP comprometido, ou um conteúdo externo malicioso — uma issue do GitHub, um comentário de PR, um trecho de log de build — injeta instruções escondidas no contexto que o modelo processa, o próprio intent preview pode reportar fielmente um plano que já nasceu manipulado.

Análises dedicadas a esse vetor chamam esse padrão de *tool poisoning*: a carga maliciosa não está no julgamento do modelo, está nos dados ou na ferramenta que alimentam esse julgamento, e a Tela repassa essa carga ao humano como se fosse intenção legítima do agente. Documentação de segurança independente do próprio ecossistema MCP chega à mesma conclusão por outro ângulo, tratando qualquer conteúdo externo consumido por uma ferramenta como potencialmente hostil até prova em contrário.

Um capítulo mais adiante nesta obra retoma esse vetor em profundidade, mas já vale reter aqui a lição de arquitetura: intent preview reduz risco de execução opaca, mas não substitui a validação da proveniência do dado que chega até a Tela.

Pesquisa recente sobre supervisão humana graduada em geração agêntica de código para domínios regulados chama esse arranjo de "oversight graduado": o nível de fricção humana escala com o risco real da ação, não com uma régua fixa de "sempre pergunte" ou "nunca pergunte". É esse gradiente — e não um interruptor binário de autonomia — que faz uma tela de agente parecer confiável o suficiente para produção.

O framework dos 12 fatores para agentes LLM formaliza a mesma ideia sob outro nome: tratar "contatar um humano" como uma chamada de ferramenta de primeira classe do fluxo do agente, não como uma exceção ao fluxo. Essa distinção entre automatizar sempre e automatizar seletivamente é a mesma que separa um fluxo de trabalho fixo (*workflow*) de um agente de verdade: um agente só merece esse nome quando decide, caso a caso, se delega a etapa ao humano ou segue sozinho.

## O Motor Por Trás do Convés

Se a Tela é onde o risco é *negociado*, o Harness é onde o risco é *aplicado*. Harness, aqui, não é metáfora vaga — é o termo técnico exato para o runtime que envolve o modelo de linguagem e o transforma em um agente de codificação capaz: ele fornece as ferramentas, gerencia o contexto e constitui o ambiente de execução em que o modelo opera.

O Claude Code é o harness de referência dessa arquitetura, e sua característica definidora não é a interface de terminal — é o fato de que cada uma de suas quase vinte ferramentas embutidas passa por um portão de permissão próprio antes de qualquer execução.

Esse portão não é um detalhe de implementação: é o mecanismo que separa um harness de produção de um script que só finge ter governança. Análises de arquitetura descrevem esse portão como um pipeline de regras verificado a cada tentativa de chamada de ferramenta — não uma checagem opcional, mas um passo obrigatório entre a intenção e o efeito. Levantamentos comparativos de harnesses de agentes chegam à mesma conclusão observando concorrentes lado a lado: o que diferencia harnesses maduros de wrappers simples em torno de uma API de modelo é exatamente a presença (ou ausência) desse portão de permissão granular por ferramenta.

E esse motor não está preso ao Claude Code. O Claude Agent SDK expõe as mesmas primitivas de harness — ferramentas, gerenciamento de contexto, portão de permissão — para você construir agentes customizados embutidos na sua própria aplicação. É a mesma sala de máquinas, montada em outro casco. Uma implementação independente de harness em Go, publicada como projeto aberto, reproduz esse mesmo padrão fora do ecossistema oficial da Anthropic — evidência de que o conceito de portão de permissão não é peculiaridade de um produto, é um requisito arquitetural de qualquer agente que se pretenda seguro em produção.

Vale reforçar por que esse motor precisa ser tão rígido: a literatura sobre harnesses para agentes de execução longa mostra que, quanto mais uma tarefa se estende no tempo — mais chamadas de ferramenta, mais contexto acumulado —, maior a chance de o modelo tentar algo fora do escopo original sem perceber que se afastou dele. O portão de permissão é o que contém esse desvio, independentemente de quantas horas o agente já esteja rodando.

Essa mesma disciplina de portão se estende para além da chamada isolada de ferramenta. A documentação oficial de *programmatic tool calling* descreve um padrão em que o próprio modelo pode compor múltiplas chamadas de ferramenta dentro de um único bloco de código executado pelo runtime, em vez de emitir uma chamada por vez e esperar o resultado voltar antes de decidir a próxima. Isso parece, à primeira vista, dar mais autonomia ao modelo — e dá, no sentido de reduzir round-trips e latência. Mas o portão de permissão não perde poder de veto nesse arranjo: cada chamada individual dentro do bloco composto ainda passa pelo mesmo pipeline `allow`/`deny`/`ask`, só que agora verificado em lote antes de o bloco inteiro ser liberado para execução. O harness continua sendo a única autoridade sobre o que roda; o que muda é a granularidade da negociação, não quem decide.

## O Contrato Que Sustenta Tudo

Chegamos à cláusula que amarra as duas camadas anteriores. O contrato é simples de enunciar e profundo em consequência: o harness decide o que é *permitido*; o modelo decide o que *tentar*. O modelo de linguagem — por mais capaz que seja — nunca é a autoridade final sobre o que roda no seu ambiente. Ele propõe. O harness dispõe.

A documentação oficial de uso de ferramentas do Claude formaliza esse ciclo como um contrato de três atos: o modelo emite um `tool_use`, o ambiente de execução decide se e como processa aquele pedido, e devolve um `tool_result` — o modelo nunca pula essa mediação para agir diretamente sobre o mundo.

Essa separação de responsabilidades é o que torna o sistema auditável mesmo quando o modelo erra. Se o modelo "alucina" uma intenção perigosa — pedir para forçar um push na branch principal, por exemplo —, isso não é, por si só, uma falha de segurança: é uma tentativa registrada, que o portão de permissão intercepta antes de virar efeito real. Levantamentos acadêmicos sobre design de sistemas de agentes e harnesses reforçam esse ponto: harnesses bem projetados tratam toda saída do modelo como *não confiável por padrão* até passar pela verificação do runtime. É esse pressuposto — desconfiar do modelo por arquitetura, não por vigilância manual constante — que permite escalar autonomia sem escalar risco proporcionalmente.

Essa mesma premissa de desconfiança arquitetural explica por que o contrato falha de um jeito específico quando é rompido: não porque o modelo decide agir mal, mas porque alguém manipula o que o modelo *acredita* estar tentando fazer. Catalogações de vulnerabilidades de ferramentas MCP documentam esse padrão sob o nome de *tool poisoning* — uma ferramenta (ou os metadados que a descrevem para o modelo) é adulterada para que o modelo emita, de boa-fé, um `tool_use` que na verdade serve a um objetivo diferente do que o tripulante pediu.

O ponto crucial é que, nesse cenário, o portão de permissão continua funcionando exatamente como projetado — ele intercepta a chamada, avalia contra o pipeline de regras e decide allow/deny/ask normalmente. O que falha é a camada anterior: a integridade da própria definição da ferramenta que chega até o modelo.

## A Ponte de Comando: Onde o Risco Vira Conversa

Lembre do Estaleiro Agêntico: você não constrói uma embarcação inteira de uma vez. No capítulo anterior, você olhou a planta baixa das quatro camadas. Agora você sobe até a **ponte de comando** e desce até a **sala de máquinas** — as duas primeiras peças que ganham corpo físico no casco.

Na ponte de comando de um navio real, o comandante não executa manobras às cegas — ele recebe relatórios de rota, estimativas de risco e só então autoriza a manobra. É exatamente esse o papel da camada Tela. Antes de qualquer ordem virar movimento do casco, a ponte de comando exibe o *intent preview* — o plano da manobra — e classifica o *blast radius* de cada ação: uma correção de rota de meio grau é hybrid autonomy (segue sozinha); uma guinada brusca perto de rochas exige o approval gate (o comandante confirma).

![Fluxo de negociacao de risco na ponte de comando antes da execucao](imagens/diagramas/dia_livro_06_d4e980feef.png)

Como Engenheiro Agêntico, você não está mais lendo linha a linha o que o agente escreveu — você está lendo o raio de impacto que ele estima, e decidindo onde vale a pena gastar sua atenção de comandante.

## A Sala de Máquinas: O Portão de Permissão do Harness

Aqui o pilar é denso o bastante para merecer duas lentes. A primeira lente é mecânica geral: pense no harness como o quadro de disjuntores da sala de máquinas. Cada comando que chega do convés — "acender o motor de bombordo", "abrir a válvula de combustível" — passa por um disjuntor específico daquele sistema. O disjuntor não julga se a manobra é *sensata*; ele só verifica se aquele comando, para aquele sistema, está na lista de permitido, proibido, ou "perguntar antes". É esse o pipeline `allow` / `deny` / `ask` que o portão de permissão do harness aplica a cada chamada de ferramenta.

A segunda lente ataca o ponto mais contraintuitivo: o motor é o mesmo, mas o casco pode ser outro. O quadro de disjuntores instalado num cargueiro padrão (o Claude Code, pronto para uso no terminal) é fisicamente o mesmo projeto de engenharia elétrica instalado num navio de apoio construído sob encomenda (uma aplicação sua, montada com o Claude Agent SDK). Você não reinventa o disjuntor a cada casco novo — você reaproveita o motor de permissão e apenas monta um casco diferente ao redor dele.

![O harness como portao de permissao na sala de maquinas do casco](imagens/diagramas/dia_livro_07_d2a24c8b48.png)

## O Contrato Entre o Oficial de Bordo e o Motor

O terceiro pilar amarra os dois anteriores numa sequência única: o tripulante dá a ordem, o oficial de bordo (o modelo) planeja a manobra e a submete ao motor, e é o motor — nunca o oficial — quem decide se ela sai do papel.

![Contrato entre o modelo e o portao de permissao do harness](imagens/diagramas/dia_livro_08_74add9f90a.png)

Um giro final na cena, que vale a pena imaginar antes de descer ao maquinário de verdade: e se alguém trocar a etiqueta de uma válvula na sala de máquinas — fizer o disjuntor que deveria "abrir válvula de combustível auxiliar" na verdade acionar a válvula de despejo no costado? O oficial de bordo continua emitindo a ordem de boa-fé, o quadro de disjuntores continua aplicando exatamente as mesmas regras allow/deny/ask de sempre — e ainda assim o resultado sai errado, porque a peça de informação que chegou até o oficial (o nome da válvula, o que ela supostamente faz) foi adulterada antes de entrar no fluxo.

Esse é o mesmo golpe que a literatura de segurança chama de *tool poisoning* aplicado a servidores MCP: o defeito não mora na decisão do oficial nem no disjuntor, mora na etiqueta. Guarde essa imagem — ela volta com força total quando você construir suas próprias ferramentas e servidores MCP mais adiante na obra.

## Construindo a Tela: Classificador de Risco e Intent Preview

A camada Tela não é mágica de produto — é uma função de classificação com uma interface honesta em cima. O bloco abaixo mostra o núcleo desse classificador: cada ação planejada pelo agente entra com um nível de risco e uma estimativa de raio de impacto, e sai com a decisão de exigir ou não um approval gate.

```typescript
type NivelRisco = "leitura" | "escrita_local" | "escrita_remota";

interface AcaoPlanejada {
  ferramenta: string;
  descricao: string;
  nivelRisco: NivelRisco;
  raioImpacto: string;
}

interface DecisaoTela {
  acao: AcaoPlanejada;
  requerApprovalGate: boolean;
  motivo: string;
}

function classificarRisco(acao: AcaoPlanejada): DecisaoTela {
  const riscosAltos: NivelRisco[] = ["escrita_remota"];
  const requerGate = riscosAltos.includes(acao.nivelRisco);

  return {
    acao,
    requerApprovalGate: requerGate,
    motivo: requerGate
      ? `Blast radius estimado (${acao.raioImpacto}) exige aprovacao humana explicita.`
      : "Hybrid autonomy: risco baixo, execucao automatica liberada.",
  };
}

function renderizarIntentPreview(acoes: AcaoPlanejada[]): DecisaoTela[] {
  return acoes.map(classificarRisco);
}

const planoDoAgente: AcaoPlanejada[] = [
  {
    ferramenta: "ler_arquivo",
    descricao: "Ler config_obra.json para validar parametros",
    nivelRisco: "leitura",
    raioImpacto: "nenhum efeito colateral",
  },
  {
    ferramenta: "git_push_force",
    descricao: "Forcar push na branch main compartilhada",
    nivelRisco: "escrita_remota",
    raioImpacto: "historico de commits de toda a tripulacao",
  },
];

const decisoes = renderizarIntentPreview(planoDoAgente);
```

Note que a função não decide sozinha se a ação é *boa* — ela decide se a ação precisa de olhos humanos antes de virar efeito. Essa distinção é o que separa uma tela decorativa de uma tela que realmente participa da negociação de risco.

O classificador acima simplifica para dois desfechos — approval gate ou hybrid autonomy —, mas a maturidade real de um pipeline de risco costuma introduzir um terceiro balde intermediário, para não forçar toda ação de risco médio a virar approval gate friccionado. O bloco a seguir estende o classificador original com uma faixa `escrita_local_sensivel`, tratada como hybrid autonomy com log reforçado, em vez de bloqueio:

```typescript
type NivelRiscoEstendido = NivelRisco | "escrita_local_sensivel";

interface DecisaoTelaEstendida extends DecisaoTela {
  exigeLogReforcado: boolean;
}

function classificarRiscoEstendido(
  acao: AcaoPlanejada & { nivelRisco: NivelRiscoEstendido }
): DecisaoTelaEstendida {
  const base = classificarRisco(acao as AcaoPlanejada);
  const exigeLogReforcado = acao.nivelRisco === "escrita_local_sensivel";

  return {
    ...base,
    exigeLogReforcado,
    motivo: exigeLogReforcado
      ? "Hybrid autonomy com log reforcado: risco medio, execucao automatica mas auditada em detalhe."
      : base.motivo,
  };
}
```

A diferença prática: `escrita_remota` sempre para no approval gate; `escrita_local_sensivel` — por exemplo, sobrescrever um arquivo de configuração local que não afeta ninguém além do próprio ambiente do desenvolvedor — segue automática, mas seu registro no diário de bordo é mais detalhado do que o de uma leitura trivial. Esse terceiro balde é o que, na prática, evita que hybrid autonomy vire ou tudo automático ou tudo com fricção; ele preserva o gradiente de oversight que a seção anterior descreveu como o real diferencial de uma tela madura.

## Construindo o Harness: o Portão de Permissão em Código

Do lado do motor, o padrão do Claude Agent SDK expõe exatamente o mesmo pipeline `allow` / `deny` / `ask` documentado para o Claude Code, inclusive na forma como o modelo customiza o próprio prompt de sistema dentro desse runtime. A documentação oficial de modificação de prompts de sistema confirma que essa customização acontece por cima do mesmo motor de permissão, nunca substituindo-o. O bloco a seguir implementa esse portão de forma independente de fornecedor — o mesmo desenho que sustenta tanto o CLI oficial quanto uma aplicação própria construída sobre o SDK.

```python
from dataclasses import dataclass
from typing import Callable, Literal

Decisao = Literal["allow", "deny", "ask"]


@dataclass
class SolicitacaoDeFerramenta:
    nome_ferramenta: str
    argumentos: dict
    nivel_risco: str


def pipeline_de_regras(solicitacao: SolicitacaoDeFerramenta) -> Decisao:
    regras_deny = {"rm_recursivo", "git_push_force_main"}
    regras_ask = {"escrever_arquivo_producao", "executar_migracao"}

    if solicitacao.nome_ferramenta in regras_deny:
        return "deny"
    if solicitacao.nome_ferramenta in regras_ask:
        return "ask"
    return "allow"


def portao_de_permissao(
    solicitacao: SolicitacaoDeFerramenta,
    aprovador_humano: Callable[[SolicitacaoDeFerramenta], bool],
) -> bool:
    decisao = pipeline_de_regras(solicitacao)

    if decisao == "deny":
        return False
    if decisao == "ask":
        return aprovador_humano(solicitacao)
    return True


def executar_com_harness(
    solicitacao: SolicitacaoDeFerramenta,
    aprovador_humano: Callable[[SolicitacaoDeFerramenta], bool],
) -> str:
    liberado = portao_de_permissao(solicitacao, aprovador_humano)
    if not liberado:
        return f"Bloqueado pelo harness: {solicitacao.nome_ferramenta}"
    return f"Executado: {solicitacao.nome_ferramenta}"
```

## Fechando o Ciclo: o Diário de Bordo e Chamadas Compostas

Os dois diagramas mermaid anteriores já previam uma peça que o esqueleto acima ainda não implementa: o "Diário de Bordo" que registra o resultado de cada decisão do portão. O bloco abaixo fecha essa lacuna e, de quebra, implementa em miniatura o padrão de *programmatic tool calling* — várias solicitações chegando agrupadas, cada uma ainda verificada individualmente:

```python
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class RegistroDeAuditoria:
    ferramenta: str
    decisao: Decisao
    timestamp: str
    aprovado_por_humano: bool | None = None


diario_de_bordo: list[RegistroDeAuditoria] = []


def executar_com_diario(
    solicitacao: SolicitacaoDeFerramenta,
    aprovador_humano: Callable[[SolicitacaoDeFerramenta], bool],
) -> str:
    decisao = pipeline_de_regras(solicitacao)
    aprovado_humano = None

    if decisao == "ask":
        aprovado_humano = aprovador_humano(solicitacao)
        liberado = aprovado_humano
    else:
        liberado = decisao == "allow"

    diario_de_bordo.append(
        RegistroDeAuditoria(
            ferramenta=solicitacao.nome_ferramenta,
            decisao=decisao,
            timestamp=datetime.now(timezone.utc).isoformat(),
            aprovado_por_humano=aprovado_humano,
        )
    )

    if not liberado:
        return f"Bloqueado pelo harness: {solicitacao.nome_ferramenta}"
    return f"Executado: {solicitacao.nome_ferramenta}"


def executar_lote_composto(
    solicitacoes: list[SolicitacaoDeFerramenta],
    aprovador_humano: Callable[[SolicitacaoDeFerramenta], bool],
) -> list[str]:
    """Simula uma chamada de ferramenta programatica: varias
    solicitacoes compostas num unico bloco, cada uma ainda
    verificada individualmente pelo mesmo portao de permissao."""
    return [
        executar_com_diario(solicitacao, aprovador_humano)
        for solicitacao in solicitacoes
    ]


def resumir_diario_de_bordo() -> dict[str, int]:
    resumo = {"allow": 0, "deny": 0, "ask_aprovado": 0, "ask_negado": 0}
    for registro in diario_de_bordo:
        if registro.decisao == "allow":
            resumo["allow"] += 1
        elif registro.decisao == "deny":
            resumo["deny"] += 1
        elif registro.aprovado_por_humano:
            resumo["ask_aprovado"] += 1
        else:
            resumo["ask_negado"] += 1
    return resumo
```

Duas peças novas aqui fecham o ciclo iniciado nos diagramas anteriores. Primeiro, `diario_de_bordo` — cada decisão do portão, aprovada ou não, vira um registro com timestamp e, quando aplicável, com o rastro explícito de que um humano aprovou. Segundo, `executar_lote_composto` — múltiplas solicitações chegam agrupadas, mas cada uma continua passando individualmente pelo mesmo `pipeline_de_regras`, sem atalho. Note o que não muda: mesmo numa chamada composta, nenhuma solicitação escapa do portão só por estar viajando em lote com outras.

A função `resumir_diario_de_bordo` não é enfeite de dashboard: é o material bruto que sustenta uma auditoria posterior — quantas ações passaram direto, quantas foram negadas de saída, e, principalmente, quantas dependeram de um humano ter clicado "aprovado" sob pressão de prazo. Se `ask_aprovado` cresce muito mais rápido que `deny`, é sinal de que as regras do pipeline estão subclassificando risco.

Esse esqueleto de três funções é, em essência, o mesmo que sustenta o arquivo `settings.json` do Claude Code na prática: arrays de permissão com padrões como `Bash(git add:*)` resolvidos exatamente neste tipo de pipeline antes de qualquer comando de shell rodar. Ganha-se ainda mais granularidade quando esse portão é combinado com *hooks* — manipuladores acionados em eventos específicos do ciclo de vida do agente (por exemplo, `PreToolUse`), com um filtro de correspondência que restringe quando disparam.

## Por Que Isso Não é Frescura de Interface

Vale a pena situar essa engenharia num pano de fundo maior. Frameworks de ciclo de vida de desenvolvimento orientado a agentes — cobrindo planejamento, codificação, teste e deploy de ponta a ponta — só se tornam seguros para produção quando cada etapa autônoma tem um portão de verificação equivalente ao que você acabou de construir. Implementações corporativas de ciclo de vida agêntico em escala, como a que a Microsoft documenta integrando Azure e GitHub, repetem o mesmo padrão em nível de pipeline inteiro: cada estágio automatizado tem seu próprio ponto de verificação antes de liberar o próximo.

## Sexta-Feira à Noite, de Novo: O Approval Gate Virado Teatro

Imagine a cena. Você está sob pressão de prazo, seu agente está configurado com Claude Code no repositório de um cliente, e uma tarefa simples de refatoração vira uma sequência de dez chamadas de ferramenta seguidas. A cada approval gate que aparece na tela, você aperta "aprovar" no automático, sem ler o intent preview. Numa dessas aprovações, o agente decide que a forma mais rápida de "limpar o histórico de commits confusos" é um `git push --force` na branch principal, compartilhada com o resto da tripulação. Você aprova. Vinte minutos depois, dois colegas perderam trabalho não commitado em cima daquele histórico reescrito.

O diagnóstico é direto à luz do que você acabou de estudar: você não desativou o approval gate — pior, você o transformou em teatro. O gate só protege alguma coisa se o blast radius exibido for realmente lido antes do clique, e se as regras `deny`/`ask` do harness estiverem calibradas para tratar `push --force` em branch compartilhada como risco alto por padrão, não como "mais uma pergunta chata". Análises de exploração de chamadas de função em agentes LLM mostram exatamente esse padrão de falha: o problema raramente é o modelo tentar algo malicioso — é o operador humano ou o harness mal configurado tratando um approval gate de alto risco como uma formalidade. Um estudo comparativo de vulnerabilidades em diferentes paradigmas de implantação de agentes chega à mesma conclusão sob outro ângulo: harnesses tecnicamente corretos falham na prática quando a camada humana da hybrid autonomy é treinada, por fadiga, a aprovar sem examinar.

A correção prática tem duas partes, e as duas moram no harness, não na sua disciplina pessoal — o que é o ponto. Primeiro: mova `git_push_force_main` da categoria "ask" para "deny" no pipeline de regras, como fizemos no código da seção anterior — uma ação com esse raio de impacto não deveria depender de você estar atento às 23h. Segundo: adote hooks de `PreToolUse` que registrem e bloqueiem automaticamente comandos destrutivos contra branches protegidas, independentemente do que o approval gate da Tela decidir. Guias de segurança dedicados ao Claude Code em produção recomendam exatamente essa dupla camada — permissões mais hooks mais sandboxing combinados — como configuração mínima de qualquer ambiente real, nunca como reforço opcional.

Vale generalizar o risco: o mesmo vetor de falha aparece, em escala maior, quando harnesses agênticos são conectados a pipelines de CI/CD sem verificação de conteúdo externo — pesquisas recentes documentam ataques de injeção de prompt via issues, PRs e logs de build que manipulam o agente a executar ações não autorizadas dentro do próprio pipeline. O princípio de defesa é idêntico ao da cena acima: nunca deixe o approval gate ser a única linha de defesa contra uma ação de alto raio de impacto.

Existe uma variante ainda mais traiçoeira dessa mesma cena, que não depende de fadiga humana nenhuma: e se o approval gate for lido com atenção total, mas a informação que ele exibe já estiver corrompida antes de chegar à Tela? Imagine que o agente usa uma ferramenta MCP de terceiros para consultar o status de um ambiente de staging, e essa ferramenta — ou os dados que ela retorna — foi adulterada para descrever uma ação de alto raio de impacto como se fosse rotina de baixo risco. Você lê o intent preview com cuidado, o texto parece plausível, e aprova uma ação que na verdade é muito mais perigosa do que o resumo deixou transparecer.

Catálogos de vulnerabilidade de ferramentas MCP descrevem exatamente esse padrão como *tool poisoning*, e frameworks de segurança do próprio ecossistema recomendam tratá-lo como classe de risco distinta de erro de julgamento humano. A correção aqui não mora na disciplina de leitura — mora em nunca conectar uma ferramenta MCP de origem não auditada a um agente com permissões de escrita, e em validar a saída de ferramentas externas antes de deixá-la alimentar qualquer decisão de approval gate.

**Armadilhas comuns:**
- Tratar approval gates como formalidade e aprovar sem ler o intent preview.
- Deixar ações de blast radius alto na categoria `ask` em vez de `deny` quando o risco é inaceitável em qualquer cenário.
- Confiar só na Tela, sem hooks de harness reforçando a mesma regra numa segunda camada.
- Não distinguir, na configuração do harness, entre ambiente de desenvolvimento local e branch/ambiente compartilhado.
- Confiar no texto do intent preview sem validar a proveniência da ferramenta ou do dado que o alimentou (tool poisoning).

## O Que Fica Deste Capítulo

Você saiu de um mapa de quatro camadas e chegou a duas peças construídas: a ponte de comando, que negocia risco com intent preview, approval gates, hybrid autonomy e blast radius; e a sala de máquinas, o harness, cujo portão de permissão aplica o pipeline `allow`/`deny`/`ask` antes de qualquer ferramenta rodar — seja dentro do Claude Code, seja dentro de uma aplicação sua construída com o Claude Agent SDK.

E você amarrou as duas com o contrato que sustenta a arquitetura inteira: o harness decide o permitido, o modelo decide o tentado. Ao dominar esse contrato, você para de tratar o comportamento do agente como uma caixa-preta de sorte e passa a enxergá-lo como um sistema com um ponto de controle específico, auditável e seu.

Como desafio, revise agora um agente que você já usa — Claude Code ou outro — e liste três ações que hoje caem em "ask" no seu fluxo, mas que, pelo raio de impacto real, deveriam estar em "deny". A seguir, você desce mais um nível: vai abrir o motor de raciocínio do Oficial de Bordo e a camada de Tools, entendendo por que o modelo nunca executa nada diretamente e como esse par converte raciocínio em ação auditável.
# Camadas LLM e Tools: Raciocínio, Seleção de Ferramentas e Efeito Real no Mundo

No capítulo anterior você instalou a Tela e o Harness no seu estaleiro e fechou o contrato mais importante da obra até aqui: o harness decide o que é permitido, o modelo decide o que tentar. Falta, porém, a metade que faz esse contrato ter consequência prática. Uma tripulação que só pensa e nunca toca um equipamento não constrói casco nenhum — e é exatamente essa lacuna que este capítulo fecha.

Aqui você desce da ponte de comando até onde o raciocínio vira ação: a Camada LLM, que decide o que tentar, e a Camada Tools, o único lugar do estaleiro onde uma decisão de fato movimenta madeira, solda ou aço. Ao final deste capítulo o mapa das quatro camadas — Tela, Harness, LLM, Tools — estará completo, e você vai enxergar por que nenhuma dessas camadas, isoladamente, constrói uma embarcação agêntica confiável.

## A Tripulação Que Pensa Antes de Agir

A Camada LLM é a tripulação do estaleiro: a inteligência que interpreta a ordem de serviço, avalia o estado do casco e decide o próximo movimento. Mas decidir não é o mesmo que agir — e é aqui que mora o erro conceitual mais comum de quem começa a construir agentes. O modelo de linguagem não tem mãos. Ele produz texto, e a diferença entre um chat comum e um agente de codificação está inteiramente em como esse texto é estruturado antes de sair da cabeça da tripulação.

O primeiro andaime dessa estrutura é o *chain-of-thought* (CoT): guiar o modelo por um processo de raciocínio passo a passo antes de comprometer qualquer ação, análogo ao "pensar antes de agir" que qualquer harness de codificação maduro impõe. Arquiteturas como *Tree of Thoughts* vão além do raciocínio linear e permitem que o modelo explore e compare ramos alternativos de decisão antes de escolher um caminho — pense nisso como a tripulação avaliando três rotas de reparo do casco antes de comprometer horas de trabalho na primeira que veio à cabeça.

## Do Raciocínio ao Formulário: Schemas Tipados

Raciocinar bem, porém, não resolve o segundo problema: como transformar uma conclusão em linguagem natural em uma instrução executável sem ambiguidade? A resposta é o par *typed tool schemas* + *structured outputs*. Toda ferramenta no padrão de *tool use* carrega um `input_schema` em JSON Schema; quando o modelo decide usá-la, ele não escreve prosa livre — ele retorna um bloco `tool_use` com argumentos que precisam validar contra esse schema antes de qualquer execução.

Documentação de mercado converge para o mesmo princípio sob nomes distintos: *structured output* é o nome genérico da técnica de forçar o formato da resposta via schema, permitindo *parsing* determinístico em vez de tentar extrair intenção de texto solto, e guias específicos de *function calling* para APIs de terceiros reforçam esse mesmo argumento como prática padrão de mercado.

O ganho é direto — schemas tipados (tipo, `enum`, `required`, limites numéricos) eliminam boa parte do espaço de argumentos alucinados antes que eles cheguem perto de qualquer efeito real.

Um contraponto evita confundir dois conceitos que soam parecidos: *structured output* genérico — forçar o modelo a responder em JSON sintaticamente válido — resolve o problema de *parsing*, mas não resolve sozinho o problema de *domínio* de valores. Um JSON perfeitamente bem formado ainda pode conter `"severidade": "quase_critica"`, um valor que nenhum humano jamais definiu como aceitável. É o `input_schema` com `enum` fechado — não o JSON mode isolado — que fecha essa segunda lacuna: a diferença entre "o texto parseia" e "o valor é aceitável".

Vale registrar por que isso importa tanto quanto a redação do próprio prompt: a documentação da ferramenta — nome, descrição, schema — deve receber o mesmo cuidado editorial que o prompt do sistema, porque é ela que o modelo lê para decidir se e como chamar a tool. Uma ferramenta mal documentada produz o mesmo efeito de um prompt ambíguo: decisões plausíveis, porém erradas.

E o inverso também é verdade em segurança: ferramentas com schemas frouxos ou descrições manipuláveis abrem espaço para ataques de seleção de ferramenta. Pesquisas recentes já catalogam esse risco com metodologia própria, incluindo ataques que manipulam deliberadamente qual tool o modelo escolhe acionar. O mesmo raciocínio se estende ao ecossistema MCP, onde uma descrição de ferramenta comprometida vira vetor de envenenamento — tema que retomaremos com mais profundidade adiante nesta obra.

## O Ataque de Abril de 2026: Um Caso Concreto

Vale um contraponto concreto para essa ameaça, e não apenas a advertência abstrata: em abril de 2026, pesquisadores da Johns Hopkins University demonstraram o sequestro de Claude Code, Gemini CLI e GitHub Copilot embutindo instruções maliciosas em títulos de *pull requests* no GitHub — os agentes leram o título como parte natural do contexto da tarefa, seguiram a instrução injetada e exfiltraram segredos de execução do GitHub Actions, publicando o resultado como comentário no próprio PR.

O detalhe que interessa à Camada Tools: o vetor de ataque não foi um schema mal formado, foi uma descrição de contexto explorada por uma ferramenta com permissão de escrita — o schema tipado da seção anterior barra argumento alucinado, mas não barra instrução injetada em texto que o modelo trata como dado confiável. É por isso que a literatura de segurança em *tool use* trata validação de schema e *rate limiting* como camadas complementares, não substitutas: mesmo com um `input_schema` perfeito, uma ferramenta sem limite de frequência de chamada permanece exposta a um agente comprometido que insiste, repetidamente, na mesma operação maliciosa até que uma janela de oportunidade se abra.

## Client Tools e Server Tools

Uma vez que o modelo decidiu e formatou a intenção como um `tool_use` validado, o ciclo se fecha: a aplicação executa a operação correspondente e devolve um `tool_result`, que volta para o contexto do modelo como o próximo fato a considerar. É esse ciclo — raciocinar, formatar, executar, observar o resultado — que caracteriza um agente, em oposição a um simples gerador de texto.

Vale fechar essa ideia com uma distinção que a próxima seção só vai ilustrar, mas que já precisa estar conceitualmente clara aqui: nem toda ferramenta executa no mesmo lugar. O padrão de *tool use* da Claude API separa *client tools* — executadas na própria aplicação do usuário, o que inclui tanto ferramentas definidas por quem constrói o agente quanto ferramentas de schema padrão como `bash` e `text_editor` — de *server tools*, que rodam na infraestrutura do próprio provedor do modelo, como `web_search`, `web_fetch`, `code_execution` e `tool_search`.

Do ponto de vista do ciclo `tool_use`/`tool_result` descrito acima, essa distinção é invisível para o modelo: ele emite a mesma estrutura de chamada independentemente de onde ela vai rodar. Mas para quem projeta o harness, a distinção é a própria fronteira de responsabilidade — *client tools* herdam o raio de impacto do ambiente local; *server tools* herdam o raio de impacto, e a superfície de dados, da infraestrutura de terceiros.

O terceiro pilar deste capítulo — independência de modelo — também precisa de uma âncora conceitual: o contrato descrito até aqui (raciocínio estruturado, schema tipado, ciclo `tool_use`/`tool_result`) não pertence ao modelo, pertence ao harness. Isso significa que trocar a tripulação — de Sonnet para Opus, de um modelo para o próximo lançado no mercado — não deveria exigir reescrever nenhuma das duas primeiras camadas descritas acima. O contrato de ferramentas é uma propriedade de arquitetura, não uma peculiaridade acoplada a um fornecedor específico de modelo. É essa propriedade — e não qualquer talento excepcional de um modelo em particular — que permite que um harness sobreviva a gerações sucessivas de LLM sem retrabalho estrutural.

## Do Pensamento ao Formulário de Ordem de Serviço

A primeira analogia é a mais direta: pense no chain-of-thought como a tripulação conversando em voz alta na ponte de comando antes de agir — "o casco está com rachadura na quilha, a severidade parece crítica, isso exige seis horas de reparo". Esse pensamento em prosa livre, por si só, ainda não move ninguém para a sala de máquinas. Ele precisa virar um formulário de ordem de serviço com campos fixos: seção do casco, severidade, horas estimadas. É exatamente isso que o `input_schema` obriga o modelo a preencher.

Mas há um ponto mais difícil que essa primeira analogia não cobre sozinha: por que um formulário rígido é estruturalmente mais seguro do que dar mais liberdade de texto ao modelo? Aqui entra a segunda analogia. Imagine dois estaleiros: um em que qualquer tripulante pode gritar uma ordem verbal para o almoxarifado ("me arruma uma peça boa aí para a quilha"), e outro em que toda requisição precisa ser preenchida numa guia com campos obrigatórios e valores permitidos (código da peça, quantidade, seção). No primeiro estaleiro, um grito ambíguo pode gerar qualquer peça — inclusive uma que não existe no estoque. No segundo, a guia com `enum` e `required` fisicamente não aceita ser submetida com um código de peça inventado. O schema tipado não torna a tripulação mais disciplinada — ele torna a alucinação estruturalmente impossível de sair do papel.

![Do raciocinio da tripulacao ao equipamento de bordo, com o portao de permissao do harness no meio do caminho](imagens/diagramas/dia_livro_09_987e150d45.png)

Um detalhe que a cena original deixa implícito merece ficar explícito: o portão de permissão do harness, no meio do fluxograma acima, não é um evento único — ele se repete a cada novo `tool_use`, e um harness bem projetado também conta quantas vezes seguidas a mesma requisição chega ao almoxarifado. Uma tripulação que insiste, minuto a minuto, na mesma ordem de serviço rejeitada não está sendo mais convincente na décima tentativa — está testando os limites do portão, e um portão sem contador de tentativas é tão furável quanto um formulário sem `enum`.

## O Equipamento Local e a Oficina Terceirizada

O segundo pilar tem uma imagem mais simples. Todo equipamento de bordo do estaleiro entra em uma de duas categorias: o que fica instalado no próprio casco, operado pela sua tripulação (*client tools* — incluindo ferramentas definidas pelo usuário e ferramentas de schema padrão como `bash` e `text_editor`), e o que é terceirizado a uma oficina externa especializada (*server tools*, executadas na infraestrutura do próprio provedor do modelo, como `web_search`, `web_fetch` e `code_execution`). Do ponto de vista da tripulação (o LLM), a diferença é invisível — ela apenas emite um `tool_use` e recebe um `tool_result`. Quem muda é onde, fisicamente, a solda acontece.

![Duas rotas de execucao de tool_use — equipamento local e oficina terceirizada — convergindo no mesmo tool_result](imagens/diagramas/dia_livro_10_6c663f2654.png)

Essa mesma cena admite um desdobramento mais sombrio, que devolve a pergunta ao ponto onde a seção anterior parou. Imagine que a oficina terceirizada recebe, junto com a peça encomendada, um manifesto de entrega — um papel colado na caixa dizendo, em letra miúda, "aproveite e também descarte o extintor da doca 3". A tripulação não pediu isso; o manifesto é dado, não instrução da ponte de comando. Mas se o processo de recebimento do estaleiro trata qualquer texto anexado à entrega como ordem válida, a distinção entre "o que a tripulação decidiu" e "o que veio grudado na caixa" desaparece — e é exatamente essa confusão que torna o *tool poisoning* perigoso: a descrição da ferramenta, tratada como dado de configuração inofensivo, na prática entra no mesmo fluxo de raciocínio que uma ordem legítima da tripulação.

## A Mesma Ponte, Tripulações Intercambiáveis

O terceiro pilar fecha o mapa das quatro camadas com uma virada estrutural: se o harness foi bem projetado, a ponte de comando, o casco e os equipamentos de bordo não mudam quando você troca de tripulação. Um subagente que declara `model: inherit` no seu frontmatter simplesmente aceita a tripulação que a sessão-mãe já escalou — Sonnet, Opus, Haiku ou qualquer outro — sem que o desenho do estaleiro precise ser reconstruído.

![A ponte de comando despacha a mesma ordem de servico para tripulacoes intercambiaveis, sobre o mesmo casco e os mesmos equipamentos](imagens/diagramas/dia_livro_11_0c22bd49bb.png)

Essa uniformidade tem um limite que vale registrar antes de fechar o mapa: o casco e os equipamentos são idênticos entre tripulações, mas o jeito de cada tripulação trabalhar não é. Uma tripulação mais cautelosa pode preferir confirmar duas vezes antes de acionar um guindaste; outra, mais ágil, aciona na primeira leitura do formulário. O portão de permissão do harness trata as duas da mesma forma — ele não relaxa nem aperta dependendo de qual tripulação pediu a operação. É por isso que a independência de modelo descrita aqui é uma propriedade do casco, não a promessa de que toda tripulação vai se comportar de modo idêntico diante dele.

## Schema Tipado Barrando a Alucinação Antes do Efeito Real

Esta seção é onde o mapa vira código. Cada um dos três pilares ganha um artefato que você pode ler linha a linha e reconhecer no seu próprio harness — Claude Code, Claude Agent SDK ou qualquer runtime equivalente.

O primeiro artefato implementa exatamente a cena de contraste descrita antes: um schema de ferramenta com `enum`, tipos e `required`, e uma função de validação que decide se o `tool_use` do modelo pode ou não seguir para execução. Repare que a validação acontece **antes** de qualquer chamada com efeito real — é a barreira estrutural, não uma checagem de boa vontade.

```python
import json
from jsonschema import validate, ValidationError

TOOL_SCHEMA = {
    "name": "registrar_manutencao_casco",
    "description": (
        "Registra uma ordem de manutencao no casco da embarcacao agentica. "
        "Use apenas quando houver dano ou desgaste confirmado em uma secao do casco."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "secao_casco": {
                "type": "string",
                "enum": ["proa", "popa", "boca", "quilha"]
            },
            "severidade": {
                "type": "string",
                "enum": ["baixa", "media", "critica"]
            },
            "horas_estimadas": {
                "type": "number",
                "minimum": 0.5,
                "maximum": 40
            }
        },
        "required": ["secao_casco", "severidade", "horas_estimadas"]
    }
}


def validar_tool_use(argumentos: dict) -> dict:
    """Barra a alucinacao de argumentos antes de qualquer efeito real no mundo."""
    try:
        validate(instance=argumentos, schema=TOOL_SCHEMA["input_schema"])
    except ValidationError as erro:
        return {"status": "rejeitado", "motivo": erro.message}
    return {"status": "aceito", "argumentos": argumentos}


if __name__ == "__main__":
    tentativa_do_modelo = {
        "secao_casco": "quilha",
        "severidade": "critica",
        "horas_estimadas": 6
    }
    print(json.dumps(validar_tool_use(tentativa_do_modelo), ensure_ascii=False))
```

Se a tripulação (o modelo) tentasse enviar `"secao_casco": "poop deck"` — um valor plausível em inglês, mas fora do `enum` definido — a validação rejeitaria a tentativa antes que qualquer chamada de sistema fosse sequer cogitada. Isso é o que a literatura de function calling chama de contrato tipado como reforço adicional aos limites da instrução em linguagem natural: o schema não é documentação passiva, é um portão de validação executável.

Repare também no que a função `validar_tool_use` deliberadamente não faz: ela não tenta adivinhar se a intenção por trás dos argumentos é boa ou má, nem reescreve o valor recebido para "corrigir" o que o modelo quis dizer. Ela apenas aplica `validate()` e propaga a `ValidationError` como uma resposta estruturada de rejeição. Essa disciplina importa porque um portão que "ajuda" a corrigir argumentos fora do domínio deixa de ser um portão — vira um tradutor de intenção. O teste automatizado que mais importa aqui não é o caminho feliz (`"quilha"`, `"critica"`, `6`) — é o caminho de rejeição: garantir, em CI, que `"poop deck"` continua sendo recusado toda vez que o schema mudar.

## Um Ponto de Despacho para Dois Tipos de Equipamento

O segundo artefato mostra como um harness despacha um `tool_use` genérico para dois destinos distintos: um equipamento de bordo local (*client tool*) e uma oficina terceirizada (*server tool*), unificando ambos no mesmo formato de `tool_result` que a tripulação (o LLM) vai consumir no próximo turno de raciocínio.

```typescript
type ToolResult = { toolUseId: string; content: string; isError?: boolean };

interface ToolCall {
  toolUseId: string;
  name: string;
  input: Record<string, unknown>;
}

async function executarClientTool(chamada: ToolCall): Promise<ToolResult> {
  // Equipamento de bordo: roda dentro da propria aplicacao do estaleiro.
  const conteudo = `Ordem de servico '${chamada.name}' executada no casco local.`;
  return { toolUseId: chamada.toolUseId, content: conteudo };
}

async function executarServerTool(chamada: ToolCall): Promise<ToolResult> {
  // Oficina terceirizada: roda na infraestrutura do provedor do modelo.
  const resposta = await fetch(`https://provedor.exemplo/tools/${chamada.name}`, {
    method: "POST",
    body: JSON.stringify(chamada.input)
  });
  const dados = await resposta.text();
  return { toolUseId: chamada.toolUseId, content: dados };
}

async function despacharToolUse(chamada: ToolCall): Promise<ToolResult> {
  const clientTools = new Set(["registrar_manutencao_casco", "bash", "text_editor"]);
  if (clientTools.has(chamada.name)) {
    return executarClientTool(chamada);
  }
  return executarServerTool(chamada);
}

export { despacharToolUse };
```

Note que `despacharToolUse` não pergunta ao modelo onde a ferramenta roda — essa decisão é do harness, não da tripulação. Isso replica, na Camada Tools, o mesmo contrato que você já viu na Camada Harness: o harness decide o que é permitido e onde a execução acontece; o modelo apenas decide o que tentar.

Vale reparar também no campo `isError` do tipo `ToolResult`, propositalmente opcional e propositalmente separado do campo `content`. Um erro de execução — a peça não estava no estoque, a oficina terceirizada respondeu com timeout — não deveria ser tratado como uma exceção que interrompe o processo do harness; ele deveria virar um `tool_result` normal, com `isError: true`, que volta ao contexto do modelo como mais um fato a considerar no próximo turno de raciocínio. É a tripulação, não o harness, quem decide o que fazer diante de uma falha de equipamento — tentar de novo com outro argumento, escalar para um humano, ou abandonar aquele caminho de reparo.

Levantamentos independentes sobre arquitetura de harness convergem para essa mesma separação de papéis entre runtime e modelo, e análises específicas do Claude Code descrevem esse despacho de ferramentas como o núcleo funcional do runtime do agente.

Vale uma nota sobre economia de turnos: o mesmo despacho que separa client tools de server tools é o que viabiliza *programmatic tool calling* — o modelo escreve código que encadeia múltiplas chamadas de ferramenta e só volta ao contexto de raciocínio com o resultado final, em vez de fazer um `tool_result` ida-e-volta a cada chamada individual. Do ponto de vista do estaleiro, é a diferença entre a tripulação escrever uma única ordem de serviço composta ("busque a peça X, monte no casco, registre a manutenção") e três idas separadas à ponte de comando para cada etapa — o efeito final é o mesmo, mas o custo de coordenação (e de tokens de contexto gastos) cai substancialmente.

## Independência de Modelo Como Propriedade de Arquitetura

O terceiro artefato é o menor, mas talvez o mais estratégico para quem projeta uma esteira agêntica que vai durar mais do que um único modelo de mercado. Um subagente bem projetado nunca fixa uma tripulação específica no seu frontmatter — inclusive porque o próprio SDK do agente permite estender o prompt de sistema padrão sem reescrever a lógica do harness a cada troca de modelo:

```yaml
name: subagente-redator-capitulo
description: >
  Manufatura autonoma de 1 capitulo em paralelo (estrategia + redacao EITA +
  diagrama Mermaid + CI de codigo + auto-validacao).
model: inherit
tools:
  - Read
  - Write
  - Edit
  - Bash
```

O campo `model: inherit` é a diferença entre um harness amarrado a uma versão de modelo e um harness que sobrevive à substituição de tripulação. Subagentes no Claude Code são instâncias isoladas disparadas pela sessão principal para trabalhar em paralelo, cada um com sua própria janela de contexto, permissões de ferramentas e — quando o frontmatter não força o contrário — o mesmo modelo da sessão-mãe. Guias de produção sobre esse mesmo mecanismo descrevem o isolamento de contexto do subagente como a propriedade que viabiliza escala sem acoplamento a um modelo específico.

Em escala, isso é o que permite que um agente líder planeje e dispare dezenas a centenas de subagentes paralelos em uma única sessão sem reescrever a arquitetura a cada troca de modelo. Skills seguem o mesmo princípio de portabilidade — são capacidades empacotadas que o próprio harness invoca quando relevante, independentemente de qual tripulação está lendo o pacote, tema que retomaremos em profundidade mais à frente.

O ganho prático: você troca a tripulação (Sonnet por Opus, Opus por um modelo futuro) e o casco — harness, tools, schemas — permanece o mesmo. Esse é o diferencial que separa quem constrói uma automação frágil, amarrada a um fornecedor, de quem projeta um estaleiro que atravessa gerações de modelo. Não é coincidência que princípios consolidados de engenharia de agentes confiáveis tratem "possuir o próprio controle de fluxo" — em vez de depender de peculiaridades de um modelo específico — como regra estrutural, não como boa prática opcional.

## Rate Limiting e Aprovação Humana Como Camada Independente

Os dois primeiros artefatos resolvem o problema de argumento alucinado (schema) e o problema de onde a execução acontece (despacho). Falta o terceiro problema, que já apareceu antes com o caso da Johns Hopkins: uma ferramenta com schema perfeito e despacho correto ainda pode ser abusada por repetição, ou por uma decisão de alto risco que nunca deveria ser autônoma. A defesa aqui não é raciocínio melhor do modelo — é uma camada de controle que nem consulta o modelo para decidir se libera a execução.

```python
import time
from collections import deque
from typing import Callable


class PortaoDeFrequencia:
    """Rate limiting por ferramenta: barra chamadas repetidas antes da Tool.

    Independente do raciocinio do LLM -- a decisao de bloquear e puramente
    baseada em contagem e tempo, nao em avaliar se o pedido "parece" legitimo.
    """

    def __init__(self, limite_por_minuto: int = 5):
        self.limite = limite_por_minuto
        self.historico: dict[str, deque] = {}

    def permitido(self, nome_tool: str) -> bool:
        agora = time.monotonic()
        janela = self.historico.setdefault(nome_tool, deque())
        while janela and agora - janela[0] > 60:
            janela.popleft()
        if len(janela) >= self.limite:
            return False
        janela.append(agora)
        return True


OPERACOES_SENSIVEIS = {"aplicar_mudanca_em_producao", "descartar_item_estoque"}


def executar_com_aprovacao(
    nome_tool: str,
    argumentos: dict,
    executor: Callable[[dict], dict],
    portao: PortaoDeFrequencia,
    aprovador_humano: Callable[[str, dict], bool],
) -> dict:
    """Combina rate limiting com aprovacao humana obrigatoria para tools sensiveis.

    A ordem importa: o rate limit barra antes de gastar o custo de perguntar
    a um humano; a aprovacao humana barra antes de qualquer efeito real,
    independentemente de quao bem formatado o tool_use chegou.
    """
    if not portao.permitido(nome_tool):
        return {"status": "rejeitado", "motivo": "limite de chamadas excedido"}

    if nome_tool in OPERACOES_SENSIVEIS:
        if not aprovador_humano(nome_tool, argumentos):
            return {"status": "rejeitado", "motivo": "aprovacao humana negada"}

    return executor(argumentos)
```

Note o que este artefato deliberadamente não faz: ele não pergunta ao modelo se a operação é segura, nem tenta interpretar a intenção por trás do `tool_use`. `PortaoDeFrequencia` conta e nega por contagem; `executar_com_aprovacao` consulta uma lista fixa de operações sensíveis e delega a decisão final a um humano — nenhuma das duas barreiras depende do raciocínio da tripulação estar correto naquele turno específico. É essa independência que a literatura de segurança em *tool use* trata como prática obrigatória, ao lado da validação de schema: *rate limiting* para conter chamadas de função descontroladas, e aprovação humana (ou regra determinística equivalente) para qualquer operação cujo efeito real não seja trivialmente reversível. O ataque de abril de 2026 contra Claude Code, Gemini CLI e GitHub Copilot descrito anteriormente não teria produzido exfiltração se a etapa de publicação de segredos como comentário de PR passasse por um portão desse tipo.

## Quando o Payload Livre Vira Incidente

Você está no terceiro sprint de um projeto real: seu time conectou um agente de codificação a um endpoint interno de deploy através de uma tool "aplicar_mudanca_em_producao". A pressa bateu, e a descrição da ferramenta ficou vaga — "aplica uma mudança de configuração" — sem `enum`, sem limites, com um campo `payload` do tipo `string` livre, aceitando qualquer coisa. Funcionou nos primeiros testes.

Na quinta execução, o modelo — raciocinando de forma plausível, mas sobre um contexto levemente desatualizado — decide que a "mudança de configuração" correta é reverter uma variável de ambiente que havia sido corrigida na véspera. O `tool_use` sai formatado, o `payload` livre não barra nada, e a chamada é aceita e executada: a reversão vai para produção. Ninguém alucinou uma frase absurda — o modelo alucinou um argumento plausível dentro de um campo que jamais deveria ter aceitado aquele valor.

O diagnóstico está exatamente no que você já viu neste capítulo: o problema nunca foi a qualidade do raciocínio do modelo, foi a ausência de um `input_schema` que restringisse o espaço de argumentos possíveis antes da execução. A correção é acrescentar exatamente o que faltou — `enum` fechado para os tipos de mudança aceitos, um campo de justificativa obrigatório e um limite explícito de escopo — de modo que a mesma decisão plausível do modelo simplesmente não tenha como ser aceita pela ferramenta. Como Engenheiro Agêntico, o ponto de controle que você projeta nunca é "confiar mais no raciocínio" — é apertar o schema até que o raciocínio ruim não tenha porta de saída.

O post-mortem do incidente revela um segundo problema, menos óbvio que o primeiro: a reversão só foi detectada seis horas depois, quando um engenheiro humano notou o comportamento errático em produção por acaso — não porque algum alarme automatizado tivesse disparado. Não havia rate limiting na tool (a quinta chamada em poucos minutos passou sem qualquer fricção adicional) nem aprovação humana obrigatória para uma operação classificada, a posteriori, como sensível. Os artefatos apresentados na seção anterior — `PortaoDeFrequencia` combinado com `executar_com_aprovacao` — existem exatamente para fechar essa segunda lacuna: mesmo que o `input_schema` tivesse sido corrigido no primeiro sprint, uma operação de reversão de variável de ambiente em produção deveria ter exigido aprovação humana explícita antes de qualquer efeito real, independentemente de quão bem formatado o `tool_use` chegasse.

Guias de engenharia de prompt para agentes já tratam a documentação de ferramentas como parte inseparável do prompt do sistema — não um anexo técnico à parte — exatamente o ponto que faltou no exemplo acima.

**Armadilhas recorrentes na Camada LLM+Tools, na prática de mercado:**

- Tratar a descrição da ferramenta como comentário decorativo, quando ela é, na prática, parte do prompt que o modelo lê para decidir se e como chamar a tool.
- Confundir "o modelo respondeu em JSON" com "o modelo está seguro" — *structured output* sem schema restritivo ainda aceita valores fora do domínio esperado.
- Não distinguir client tools de server tools no design de auditoria: uma *server tool* de busca externa tem uma superfície de risco (dados que entram no contexto) diferente de uma *client tool* que grava no disco local.
- Fixar um modelo específico no frontmatter do subagente "porque funcionou bem em teste", criando dívida de portabilidade que só aparece quando o modelo muda de versão.
- Implementar rate limiting e aprovação humana no código, mas nunca escrever um teste que force o caminho de rejeição — times validam que a chamada legítima passa e nunca verificam que a sexta chamada em um minuto é de fato barrada, ou que a operação sensível de fato para à espera do aprovador. Um portão de permissão não testado no caminho de bloqueio é, na prática, indistinguível de um portão que não existe.

## O Que Fica Deste Capítulo

Quatro pontos fecham o mapa das quatro camadas neste capítulo. Primeiro: chain-of-thought, schemas tipados e structured outputs não são luxo de engenharia — são o que impede que um raciocínio plausível vire um argumento alucinado com efeito real. Segundo: nenhuma ação sai do papel sem passar por uma Tool, seja ela um equipamento local (client tool) ou uma oficina terceirizada (server tool) — o modelo decide, a Tool executa. Terceiro: schema tipado, rate limiting e aprovação humana não competem entre si — são camadas independentes, e a ausência de qualquer uma delas deixa uma porta aberta que as outras duas, sozinhas, não fecham. Quarto: um harness bem projetado herda o modelo da sessão em vez de amarrar-se a uma tripulação fixa, o que transforma a substituição de modelo em um evento trivial, não em uma reconstrução do estaleiro.

Com a quilha erguida e o casco fechado nas quatro camadas, seu estaleiro está pronto para subir até a ponte de comando. O desafio que fica: revise a última ferramenta que você conectou a um agente e pergunte se o `input_schema` dela realmente fecha a porta para o valor mais plausível e mais errado que o modelo poderia tentar. A seguir, você recruta o resto da tripulação — skills, subagentes e MCP — e começa a orquestrar trabalho em paralelo sobre essa mesma base de LLM+Tools que você acabou de erguer.
# Skills, Subagentes e MCP: Orquestrando a Tripulação Agêntica

No capítulo anterior você fechou o mapa das quatro camadas: o par LLM+Tools convertendo raciocínio em ação auditável, com o modelo decidindo o que tentar e a Tool sendo o único ponto onde essa tentativa vira efeito real. Esse par funciona muito bem para uma tarefa, um contexto, uma tripulação. Mas o que acontece quando o trabalho cresce — quando você precisa de dez tarefas rodando ao mesmo tempo, cada uma com seu próprio raciocínio e suas próprias ferramentas, sem que uma pise na memória da outra?

Este capítulo sobe da sala de máquinas até a ponte de comando e recruta o resto da tripulação do seu estaleiro: as Skills, que empacotam capacidade; os Subagentes, que despacham essa capacidade em paralelo com contexto isolado; e o MCP, o protocolo que conecta qualquer guindaste do cais sem exigir um adaptador proprietário para cada um. Ao final, você não vai mais pensar em "um agente fazendo tudo" — vai pensar em uma tripulação inteira, orquestrada, cada tripulante trabalhando isolado na própria doca e reportando de volta apenas o que importa.

Repare que os três tripulantes resolvem três problemas diferentes, e é fácil confundi-los se você não tiver clareza sobre qual pergunta cada um responde. Skills respondem "como faço a mesma coisa de novo sem reexplicar tudo?". Subagentes respondem "como faço várias coisas ao mesmo tempo sem que uma atrapalhe a outra?". MCP responde "como conecto uma ferramenta nova sem reconstruir a integração do zero a cada vez?". As três respostas se combinam — um subagente pode invocar uma skill, e uma skill pode chamar uma ferramenta MCP —, mas cada uma resolve uma dimensão distinta da escala, e tratar as três como sinônimos de "automação" é o primeiro passo para configurá-las errado.

## Skills: Capacidade Empacotada, Não Reexplicada

Uma Agent Skill é uma capacidade modular empacotada: instruções, metadados e, opcionalmente, scripts e templates auxiliares, guardados em uma pasta com um frontmatter que descreve o nome da capacidade e quando ela deve ser usada. A diferença estrutural em relação a um prompt avulso é sutil, mas decisiva — você não precisa reexplicar o procedimento a cada conversa. O harness lê a descrição de cada skill disponível e decide sozinho, a partir da tarefa em mãos, qual capacidade invocar automaticamente.

Isso resolve um problema real de escala: o mesmo procedimento (revisar código, redigir um capítulo, validar uma migração) deixa de viver espalhado em prompts copiados e recolados, e passa a viver em um único pacote versionado, reutilizável por qualquer sessão que o harness tenha acesso. É a diferença entre treinar um tripulante do zero toda vez e ter um manual de procedimento já escrito, esperando na prateleira certa do estaleiro.

Essa economia, porém, não é gratuita — e vale marcar a nuance antes de seguir adiante. Cada skill disponível soma a própria descrição ao que o harness precisa varrer antes de decidir qual capacidade invocar; uma prateleira lotada de manuais mal escritos custa quase tanto quanto a ausência de manual nenhum, porque o próprio harness ainda precisa ler etiqueta por etiqueta antes de descartar as que não servem. O framework acadêmico *SkillReducer* endereça exatamente esse ajuste fino: propõe otimizar a descrição de cada skill para o menor número de tokens que ainda preserva a precisão da decisão de invocação, tratando a prateleira do estaleiro como recurso finito, não infinito.

Na prática de quem escreve skills — e isso vale tanto para uma skill de revisão de migração SQL quanto para as skills que compõem esta própria fábrica editorial — redigir o campo `description` não é exercício de exaustividade, é exercício de precisão: dizer o suficiente para o harness reconhecer o gatilho certo, sem inflar cada consulta ao quadro de capacidades com parágrafos que ninguém vai ler antes de decidir.

## Subagentes: o Problema do Isolamento

Subagentes resolvem um segundo problema, mais estrutural: **isolamento**. A propriedade que define um subagente no Claude Code não é ele "fazer uma coisa específica" — é ele começar com contexto limpo. Um subagente não vê o histórico de conversa da sessão principal, nem os arquivos já lidos, nem as skills já invocadas na thread-mãe; ele recebe apenas o prompt de despacho e trabalha com sua própria janela de contexto, suas próprias permissões de ferramentas e, quando bem projetado, o mesmo modelo herdado da sessão que o despachou. Guias de produção descrevem esse isolamento como o que viabiliza paralelismo real: dez subagentes rodando ao mesmo tempo não competem pela mesma janela de contexto, porque cada um tem a sua.

Em junho de 2026, esse mecanismo ganhou um nome e uma escala formal: *Dynamic Workflows*. Nele, o agente líder planeja e dispara dezenas a centenas de subagentes paralelos dentro de uma única sessão, com um avaliador separado — *Performance Outcomes* — decidindo quais resultados retornam aprovados e quais voltam para retrabalho antes de serem aceitos. Documentação de mercado sobre orquestração de subagentes converge no mesmo ponto: a escala só é sustentável porque cada subagente carrega sua própria carga de contexto, e o custo de processar cem tarefas em paralelo não é cem vezes o custo de estourar uma única janela de contexto compartilhada.

Vale a pena enxergar esse despacho em lote como extensão de um padrão que você já conhece do capítulo anterior: é o *orchestrator-workers*, em que uma chamada central decompõe uma tarefa e delega partes independentes a chamadas especializadas, só que aplicado agora a subagentes inteiros em vez de chamadas isoladas de LLM. E análises de harnesses de longa duração já apontam esse isolamento de contexto como pré-requisito estrutural para sessões que precisam durar horas sem degradar de coerência.

Vale entender também o que sustenta esse isolamento por baixo do capô, porque não é mágica — é gerenciamento disciplinado de janela de contexto. Catálogos de técnicas de otimização de contexto em LLMs descrevem o mesmo repertório que um subagente aplica implicitamente a cada despacho: truncamento seletivo do que não é relevante para a tarefa corrente, sumarização progressiva de histórico longo, e o descarte deliberado de qualquer coisa que não sirva mais à ordem de serviço em mãos. O ganho de isolar um subagente não vem de ele ter acesso a "mais contexto" do que a sessão principal; vem exatamente do oposto — de ele receber só o contexto mínimo necessário, como princípio de design deliberado, e não como limitação acidental de infraestrutura.

Nem todo harness resolve esse problema da mesma forma, e o contraponto merece registro. O *Agent Mode* do GitHub Copilot, por exemplo, opta por determinar o contexto relevante automaticamente a cada iteração — decidindo sozinho quais arquivos abrir e quanto histórico reter — em vez de expor ao operador o contrato explícito de isolamento que caracteriza um subagente do Claude Code. Isso não é necessariamente pior: é uma escolha arquitetural diferente, que troca previsibilidade de isolamento por conveniência automática. Como Engenheiro Agêntico, a lição não é "isolamento explícito sempre vence" — é saber, para o harness específico que você tem em mãos, qual dessas duas garantias você está de fato recebendo antes de apostar a arquitetura da sua tripulação nela.

## MCP: o Problema da Integração

O terceiro tripulante do capítulo resolve um problema diferente: integração. Antes de novembro de 2024, cada ferramenta externa — um banco de dados, uma API de busca, um sistema de arquivos remoto — exigia uma implementação sob medida para cada combinação de modelo e aplicação. O Model Context Protocol (MCP) foi introduzido pela Anthropic exatamente para resolver essa fragmentação: um protocolo aberto, cliente-servidor, que padroniza como sistemas de IA integram e compartilham dados com ferramentas e fontes externas. Em dezembro de 2025 a Anthropic doou o MCP para a Agentic AI Foundation, um fundo dirigido sob a Linux Foundation — um sinal explícito de que o protocolo deixou de ser propriedade de um único fornecedor e passou a ser infraestrutura de indústria.

Vale notar que o MCP não nasceu de um comitê abstrato: a especificação tem autoria identificável — David Soria Parra e Justin Spahr-Summers — e já conta com kits de construção maduros nos dois ecossistemas mais usados por quem precisa registrar um guindaste novo no cais: FastMCP, em Python, e o MCP SDK, em Node/TypeScript. Isso muda a decisão prática de "construir uma integração proprietária do zero" para "escolher um SDK MCP maduro e herdar de graça a conformidade com o protocolo" — o mesmo raciocínio de reaproveitamento que você já viu operar dentro do próprio estaleiro, com Skills empacotando procedimento e Subagentes empacotando isolamento.

Vale registrar, já aqui, o outro lado dessa integração universal: como qualquer canal que traz dado e código de fora para dentro do contexto do modelo, o MCP também é superfície de ataque. Descrições de ferramenta MCP comprometidas já foram catalogadas como vetor de *tool poisoning* — texto malicioso escondido na própria documentação da ferramenta, capaz de manipular o comportamento do modelo sem que o usuário perceba. Análises de segurança específicas do protocolo descrevem ainda a injeção indireta como uma variante do mesmo problema, em que o conteúdo malicioso não vem da descrição da ferramenta, mas de um dado externo que ela retorna — e um catálogo mais recente de práticas em produção trata o dimensionamento do *blast radius* de cada ferramenta conectada como parte inseparável do design de segurança, não como camada opcional. Uma sistematização recente do tema chega à mesma conclusão de forma mais ampla: os riscos do ecossistema MCP crescem junto com sua própria adoção, e não existe versão do protocolo imune a isso por padrão. Retomaremos essa blindagem em profundidade mais à frente; por ora, o ponto é: conectar um guindaste novo ao cais não dispensa a inspeção do guindaste.

Vale a pena aproximar esse dimensionamento de *blast radius* do que você já viu no pilar dos Subagentes, porque é o mesmo raciocínio aplicado em duas camadas diferentes da tripulação. Um servidor MCP registrado com autonomia total — leitura, escrita e execução de comando, tudo liberado por padrão — tem um raio de impacto proporcional a essa liberdade: se a ferramenta for comprometida, o dano possível é do tamanho da permissão concedida a ela. Um servidor MCP registrado com escopo mínimo — só o que a tarefa exige, nada além — sofre o mesmo tipo de comprometimento, mas o dano possível é pequeno o suficiente para ser contido. É o mesmo princípio de "menor privilégio necessário" que rege o campo `tools` de um subagente.

## O Quadro de Capacidades da Tripulação

Como Engenheiro Agêntico, pense na sua tripulação não como um grupo de generalistas que reaprende tudo a cada ordem de serviço, mas como um estaleiro com um quadro de capacidades afixado na Ponte de Comando: cada capacidade tem uma etiqueta clara de "quando usar", e o Diário de Bordo (o próprio harness) consulta esse quadro antes de reexplicar qualquer procedimento do zero. Uma Skill é exatamente essa etiqueta — nome, descrição do gatilho, e o procedimento empacotado atrás dela.

![O harness consulta o quadro de capacidades da tripulacao e despacha a skill certa sem reexplicacao manual](imagens/diagramas/dia_livro_12_ecf658c76c.png)

## Duas Docas Isoladas, Nenhuma Vendo o Diário da Outra

Este pilar é o núcleo técnico mais denso deste capítulo, e merece duas lentes complementares. A primeira lente explica o isolamento de contexto propriamente dito: imagine que, em vez de toda a tripulação trabalhar amontoada na mesma ponte de comando, você despacha dois tripulantes especializados para duas docas isoladas do estaleiro. Cada um recebe apenas a ordem de serviço específica da sua doca — não o diário de bordo completo da ponte, não o que o outro tripulante está fazendo na doca ao lado. Quando termina, cada um devolve só o relatório final. Ninguém na ponte de comando precisa adivinhar o que aconteceu dentro da doca; e nenhum tripulante isolado precisa (nem consegue) carregar o histórico inteiro da sessão principal.

![Isolamento de contexto - a ponte de comando despacha para docas isoladas que nao compartilham diario de bordo entre si](imagens/diagramas/dia_livro_13_93d65446dc.png)

A segunda lente explica por que isso importa em escala. Um estaleiro que só despacha dois tripulantes por vez ainda é artesanal. O que os Dynamic Workflows descrevem é um estaleiro despachando um lote inteiro de tripulantes especializados simultaneamente — dezenas, às vezes centenas — cada um em sua própria doca isolada, com um inspetor de qualidade dedicado (o *Performance Outcomes*) caminhando entre as docas, aprovando relatórios prontos e devolvendo para retrabalho os que não fecham o padrão antes de qualquer coisa subir para a ponte de comando.

![Dynamic Workflows - lote de tripulantes despachados em paralelo, com inspetor de qualidade avaliando antes da aprovacao final](imagens/diagramas/dia_livro_14_1e5afdec07.png)

Um detalhe separa um estaleiro amador de um estaleiro maduro: o que cada tripulante devolve à ponte de comando não é o diário de bordo inteiro da sua doca — é um relatório final, comprimido ao que realmente importa para quem vai decidir o próximo passo. Um tripulante que devolve cem páginas de anotação bruta não economizou trabalho nenhum para a ponte; só transferiu a bagunça de lugar, e agora é a ponte de comando quem paga o custo de garimpar o que interessa dentro do excesso. O contrato de despacho maduro já nasce sabendo qual formato de relatório a ponte espera receber de volta — telegráfico, com veredito objetivo e evidência mínima anexada — e é esse contrato, não o volume de trabalho feito na doca, que determina se o paralelismo de fato economiza tempo ou apenas desloca a sobrecarga de contexto para depois, quando ela já é mais cara de resolver.

E há uma segunda falha, menos óbvia, que só aparece quando o estaleiro escala de duas docas para um lote inteiro: se o inspetor de qualidade aprova qualquer relatório que chegue formatado corretamente, sem checar se o conteúdo do relatório de fato corresponde ao que foi entregue na doca, o *Performance Outcomes* vira teatro de aprovação — um carimbo que não filtra nada. A inspeção séria não lê só a forma do relatório; confere a evidência objetiva por trás dele, exatamente como este capítulo já defende para qualquer ferramenta MCP conectada ao cais: confiança não é o padrão, é o que se conquista depois da verificação.

## O Cais Antes e Depois do Protocolo Universal

Este pilar fecha com uma imagem de antes e depois. Antes do MCP, cada guindaste do cais de lançamento — cada ferramenta ou fonte de dados externa — precisava do seu próprio conjunto de cabos e adaptadores proprietários até a ponte de comando. Trocar de fornecedor de guindaste significava reconstruir a fiação inteira. Depois do MCP, todos os guindastes falam o mesmo protocolo, e a ponte de comando conversa com qualquer um deles sem adaptador sob medida.

Pense no guindaste 3, marcado com etiqueta suspeita no diagrama abaixo, como o equivalente exato de um servidor MCP de terceiro cuja documentação você nunca leu com atenção. Ele fala o mesmo protocolo que os outros dois — nenhuma barreira técnica o impede de se conectar —, mas isso não significa que ele mereça o mesmo grau de confiança automática. A inspeção obrigatória, marcada como linha tracejada no diagrama, não é burocracia: é o mesmo raciocínio de "confiança não é o padrão" que a ponte de comando já aplica a qualquer relatório de subagente antes de aceitá-lo. Um cais que conecta guindastes novos sem esse portão de inspeção resolveu o problema da fragmentação de adaptadores só para reabrir, na mesma porta, o problema da confiança cega.

![Cais de lancamento antes e depois do MCP como protocolo universal, com nota de inspecao contra guindastes adulterados](imagens/diagramas/dia_livro_15_ced396502e.png)

## Empacotando uma Capacidade Como Skill

Esta seção transforma cada pilar em um artefato que você pode adaptar diretamente no seu próprio estaleiro — seja ele Claude Code, Claude Agent SDK ou outro harness compatível com o mesmo padrão.

O primeiro artefato mostra a estrutura mínima de uma Agent Skill: um frontmatter com nome e descrição de gatilho, seguido do procedimento empacotado. A descrição é o que o harness lê para decidir a invocação automática — ela precisa dizer, sem ambiguidade, quando essa capacidade se aplica.

```markdown
---
name: revisor-de-migracao-sql
description: >
  Use esta skill sempre que o usuario pedir revisao de uma migracao de banco
  de dados (SQL) antes de aplicar em producao. Verifica reversibilidade,
  bloqueio de tabela e presenca de indice em colunas de filtro.
---

# Skill: Revisor de Migração SQL

## Procedimento
1. Leia o arquivo de migração indicado e identifique o tipo de operação
   (ALTER TABLE, CREATE INDEX, DROP COLUMN, etc.).
2. Verifique se a operação tem um caminho de rollback documentado.
3. Sinalize qualquer ALTER TABLE em tabela grande sem estratégia de lock
   incremental.
4. Devolva um relatório curto: aprovado, aprovado com ressalva, ou reprovado.
```

Note que o corpo da skill não é um prompt genérico — é um procedimento fechado, com passos numerados e critério de saída explícito. Isso é o que permite que a mesma capacidade produza resultado consistente independentemente de quem (ou qual sessão) a invoca.

Repare também no que o `description` acima não faz: não lista todas as variações possíveis de pedido, não tenta cobrir casos extremos improváveis, não se estende em advertências genéricas. Ele diz, em uma frase, quando usar a skill, e delega ao corpo do procedimento o detalhamento que só importa depois que a decisão de invocar já foi tomada. É esse mesmo princípio de economia que o SkillReducer formaliza: a descrição é o que compete por espaço no quadro de capacidades a cada nova consulta, então cada token gasto ali precisa justificar sua presença.

## Um Subagente que Nunca Assume o Contexto da Ponte

O segundo artefato é o frontmatter de um subagente Claude Code, com a propriedade que mais importa neste capítulo destacada em comentário: `model: inherit` evita fixar uma tripulação específica, e a ausência de qualquer referência ao histórico da sessão-mãe evidencia que o subagente só recebe o que está explicitamente escrito no prompt de despacho.

```yaml
name: subagente-redator-capitulo
description: >
  Manufatura autonoma de 1 capitulo em paralelo (estrategia + redacao EITA +
  diagrama Mermaid + CI de codigo + auto-validacao). Nao recebe o historico
  da sessao principal - apenas as coordenadas do capitulo e o indice RAG do
  dossie.
model: inherit
tools:
  - Read
  - Write
  - Edit
  - Bash
```

Repare no que falta de propósito: não há campo algum que injete "tudo o que a ponte de comando conversou até agora". O subagente é despachado com um pacote de instruções autocontido — coordenadas do capítulo, caminho do dossiê indexado — e é só isso que ele enxerga. Guias de orquestração de subagentes chamam esse desenho de "prompt autocontido" como pré-requisito para qualquer despacho paralelo funcionar sem contaminação cruzada de contexto. Note também que `model: inherit` não é um truque de configuração — o próprio SDK de agentes documenta oficialmente como estender o prompt de sistema padrão sem reescrever a lógica do harness a cada troca de modelo, o que é exatamente o que permite ao subagente herdar a tripulação da sessão-mãe sem gambiarra.

Note ainda o campo `tools`, listando explicitamente `Read`, `Write`, `Edit` e `Bash`: essa lista não é decorativa, é o portão de permissão do subagente. A mesma lógica de arrays `allow`/`deny`/`ask` que controla o que a sessão principal pode executar via `.claude/settings.json` se aplica, de forma independente, a cada subagente despachado — um tripulante de doca isolada não herda automaticamente as permissões da ponte de comando, ele recebe as suas próprias, tão restritas quanto a tarefa exigir. Isso fecha o círculo de isolamento: contexto isolado sem permissão isolada ainda seria um guindaste destravado demais para a doca em que está.

## Retentativa com Backoff: Quando uma Doca Falha

Isolamento e permissão bem projetados não eliminam a falha — apenas a contêm. Um subagente pode falhar por limite de taxa do provedor de modelo, timeout de rede ou saída malformada, e o artefato abaixo mostra o padrão de produção para lidar com isso sem parar a esteira inteira por causa de uma única doca instável: tentativa limitada, com espera exponencialmente crescente entre cada nova tentativa.

```python
import time

MAX_TENTATIVAS = 3

def despachar_subagente_com_backoff(tarefa, executar_subagente):
    """Despacha um subagente e retenta com backoff exponencial em caso
    de falha, escalando para decisao humana apos MAX_TENTATIVAS."""
    for tentativa in range(1, MAX_TENTATIVAS + 1):
        try:
            resultado = executar_subagente(tarefa)
            if resultado.get("status") == "sucesso":
                return resultado
        except Exception as erro:
            if tentativa == MAX_TENTATIVAS:
                return {
                    "status": "falha",
                    "motivo": str(erro),
                    "tentativas": tentativa,
                }
            time.sleep(2 ** tentativa)  # 2s, 4s, 8s...
    return {"status": "falha", "motivo": "esgotou tentativas"}
```

O limite superior `MAX_TENTATIVAS` não é arbitrário: é o ponto exato em que o sistema para de tentar sozinho e escala a falha para decisão humana, em vez de insistir indefinidamente contra a mesma causa raiz. Guias de produção para subagentes de Claude Code descrevem esse mesmo padrão de tentativa-limitada-com-espera-crescente como pré-requisito para qualquer despacho em lote que não trave a fábrica inteira por causa de um único capítulo teimoso.

## Registrando um Guindaste no Protocolo Universal

O terceiro artefato é a configuração de um servidor MCP em formato `mcpServers`. Registrar um servidor aqui é o que torna a ferramenta visível para qualquer harness compatível, sem escrever uma integração proprietária. A própria documentação de referência para construção de servidores MCP recomenda tratar a descrição de cada ferramenta exposta com o mesmo rigor editorial dedicado ao prompt do sistema — porque é esse texto, e não o código por trás dele, que o modelo lê para decidir se e como chamar a ferramenta.

```json
{
  "mcpServers": {
    "banco_de_dados_estaleiro": {
      "command": "npx",
      "args": ["-y", "mcp-server-sqlite-npx", "data/estado_fabrica.db"],
      "env": {
        "MCP_LOG_LEVEL": "info"
      }
    }
  }
}
```

Do ponto de vista do modelo, esse servidor aparece como um conjunto de ferramentas com `input_schema` — o mesmo contrato tipado que você já viu no capítulo anterior protegendo contra argumentos alucinados. A diferença é que, em vez de código escrito à mão para cada integração, o protocolo padroniza a descoberta e a chamada dessas ferramentas. E, como qualquer entrada externa que chega ao contexto do modelo, o conteúdo devolvido por um servidor MCP precisa ser tratado com a mesma desconfiança estrutural que você aplicaria a um resultado de busca na web — validação de saída, não confiança automática, é o que separa uma integração madura de uma porta aberta.

Vale um último detalhe de projeto sobre quantas ferramentas registrar num servidor MCP como esse: a orientação oficial para construção de servidores recomenda equilibrar cobertura abrangente dos endpoints disponíveis com um conjunto menor de ferramentas de fluxo de trabalho especializadas, desenhadas para as tarefas que o agente realmente executa com frequência. Um servidor MCP que expõe uma ferramenta para cada endpoint bruto da API subjacente empurra para o modelo o trabalho de compor múltiplas chamadas manualmente a cada tarefa; um servidor bem projetado já embute esse fluxo de trabalho na própria ferramenta exposta, do mesmo jeito que uma Skill embute um procedimento em vez de deixá-lo implícito no prompt.

## "Continue de Onde Paramos": o Erro Mais Comum de Quem Começa

Você acabou de projetar seu primeiro lote de subagentes: um para pesquisar, um para redigir, um para validar código. Na pressa de colocar tudo para rodar em paralelo, você escreve o prompt de despacho do subagente redator assim: "continue de onde paramos e escreva o capítulo 6". Funciona na sua cabeça, porque você lembra perfeitamente do que "paramos" significa — você acabou de discutir isso na sessão principal.

O subagente recebe a ordem, mas não tem a menor ideia do que "onde paramos" quer dizer. Ele não viu a conversa anterior, não sabe qual sumário macro está em uso, não sabe se o capítulo 5 já foi validado. Ele faz o melhor raciocínio possível com o pouco que recebeu — e entrega um capítulo genérico, desconectado do fio narrativo real da obra, tecnicamente correto mas inútil para o seu livro.

O diagnóstico está exatamente no que você já viu neste capítulo: um subagente começa com contexto limpo por definição. Não é um bug do despacho — é a propriedade que viabiliza o isolamento e o paralelismo em primeiro lugar. O erro não foi confiar no subagente; foi tratá-lo como se ele fosse uma continuação da mesma conversa. A correção é reescrever o prompt de despacho como um pacote autocontido: coordenadas explícitas (parte, capítulo, slug), caminho do arquivo de sumário, e o resultado esperado — sem depender de nenhuma memória implícita da sessão principal. Como Engenheiro Agêntico, o ponto de controle que você projeta nunca é "o subagente vai lembrar" — é "o subagente recebe tudo que precisa saber, escrito, na primeira mensagem".

Vale notar por que esse erro é tão fácil de cometer mesmo depois de entender a teoria: quando você mesmo despacha o subagente, na mesma sessão em que acabou de discutir o capítulo 6, a lembrança do que "paramos" significa está tão fresca na sua própria cabeça que fica difícil perceber o quanto ela é invisível para quem recebe só o texto do prompt. É um viés de proximidade — você confunde "eu me lembro" com "está escrito". A prática que evita essa armadilha de forma sistemática é reler o prompt de despacho fingindo ser um tripulante novo, contratado ontem, que nunca participou de nenhuma conversa anterior: se alguma coordenada ainda depende de "você já sabe do que estou falando", o prompt não está pronto para ser despachado.

**Armadilhas recorrentes na orquestração de tripulação agêntica, na prática de mercado:**

- Escrever prompts de despacho que pressupõem contexto implícito da sessão-mãe, ignorando que o isolamento é a propriedade central do subagente, não um detalhe de implementação.
- Fixar um modelo específico no frontmatter do subagente em vez de `model: inherit`, criando dívida de portabilidade sempre que a tripulação muda de versão.
- Disparar dezenas de subagentes em paralelo sem um avaliador de qualidade equivalente ao *Performance Outcomes*, aceitando qualquer relatório de volta sem checagem estrutural.
- Conectar um servidor MCP de terceiros e confiar cegamente na descrição das suas ferramentas, sem tratá-la como entrada potencialmente hostil — o mesmo raciocínio de *tool poisoning* que abre espaço para injeção indireta.
- Tratar o relatório final de um subagente como o lugar certo para despejar toda a saída bruta da doca, em vez de projetá-lo como contrato comprimido — o mesmo problema, em escala menor, que o SkillReducer documenta para descrições de skill infladas além do necessário. Um subagente que devolve tudo o que fez, sem filtrar o que a ponte de comando precisa decidir, transfere para a sessão principal exatamente o custo de contexto que o isolamento deveria ter evitado.
- Registrar um avaliador de qualidade que só confere formato (o relatório chegou? está no schema certo?) e não o conteúdo por trás dele — um *Performance Outcomes* de fachada que aprova qualquer coisa bem-formatada é pior do que não ter avaliador nenhum, porque cria falsa sensação de que o lote foi checado.

## O Que Fica Deste Capítulo

Três pontos fecham a recomposição da tripulação neste capítulo. Primeiro: Agent Skills empacotam procedimento como capacidade reutilizável, eliminando o retrabalho de reexplicar o mesmo prompt a cada tarefa recorrente — mas a economia só se sustenta se a própria descrição da skill for escrita com a mesma disciplina de token que se espera do restante do sistema.

Segundo: um subagente só entrega paralelismo real porque começa com contexto limpo e isolado — tratá-lo como extensão da memória da sessão principal é o erro mais comum de quem começa a orquestrar em escala, e o isolamento de entrada precisa ser espelhado por um contrato de saída igualmente disciplinado, sob pena de apenas deslocar o custo de contexto para depois.

Terceiro: o MCP substitui integrações proprietárias fragmentadas por um protocolo único e neutro de fornecedor, mas herda também a responsabilidade de tratar qualquer ferramenta externa como entrada não confiável até prova em contrário, com o raio de impacto de cada conexão dimensionado ao mínimo necessário — o mesmo princípio de menor privilégio que rege as permissões de um subagente.

Levantamentos comparativos entre os principais harnesses do mercado — Claude Code, Codex, Cursor — convergem na mesma separação de papéis entre runtime e modelo que sustenta tudo o que você viu neste capítulo. Isolar contexto, delegar com permissão própria e tratar ferramenta externa como superfície de risco não são peculiaridades de um único produto: são o padrão que se repete quando você compara lado a lado os principais agentes de codificação do mercado. Não é coincidência que princípios consolidados de engenharia de agentes confiáveis tratem "possuir o próprio controle de fluxo" — em vez de depender de peculiaridades de um único fornecedor — como regra estrutural também para como você orquestra a tripulação inteira, não apenas uma chamada isolada de ferramenta.

Com a Ponte de Comando agora tripulada — Skills, Subagentes e MCP trabalhando juntos —, você chegou ao fim desta primeira etapa da sua jornada como Engenheiro Agêntico. O desafio que fica: revise o último subagente que você despachou e pergunte se o prompt de despacho realmente seria compreensível para alguém que nunca participou da conversa anterior.

Você agora tem, em mãos, o mapa completo das quatro camadas — Tela, Harness, LLM, Tools — e a tripulação que as opera em escala — Skills, Subagentes, MCP. É a base estrutural sobre a qual qualquer sistema agêntico de produção é erguido, independentemente da ferramenta específica que você escolher no seu próprio estaleiro.

# Próximos Passos

Você chegou ao fim deste recorte de *AI Driven Development: Do Zero ao Deploy*. Se as quatro camadas — Tela, Harness, LLM, Tools — e a tripulação de Skills, Subagentes e MCP mudaram a forma como você enxerga um agente de codificação, a obra completa aprofunda exatamente para onde este e-book aponta: como escrever o próprio CLAUDE.md e AGENTS.md que governam essa tripulação, como configurar hooks e permissions de verdade num harness de produção, como construir suas próprias ferramentas e servidores MCP blindados contra tool poisoning, e como levar tudo isso do primeiro commit até o deploy em produção.

Se você quer continuar a leitura com o mapa completo do estaleiro — da fundação teórica à blindagem de segurança ponta a ponta — procure *AI Driven Development: Do Zero ao Deploy*, de Heverton Eduardo Peres, o livro-mãe do qual este e-book foi extraído.

E se este recorte te ajudou a enxergar seus próprios agentes com outros olhos, compartilhe com alguém do seu time que ainda está preso no vibe coding. O próximo passo do seu estaleiro começa com uma pergunta simples: a sua última automação com IA tem um diário de bordo à prova de rasura, ou só parece ter?
