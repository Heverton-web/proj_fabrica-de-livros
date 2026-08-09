# Capítulo 10: Do Zero ao Deploy: Integrando Agentes no CI/CD com Portão de Aprovação Humana

## 1. Introdução

No Capítulo 9, você desceu ao porão do estaleiro e aprendeu a disciplina de combustível do Engenheiro Agêntico: grep antes de busca semântica, compaction de contexto e comunicação telegráfica para operar uma tripulação inteira sem afundar em custo e latência [7]. Essa disciplina não foi um capítulo isolado sobre economia — foi o combustível que permite rodar agentes em cada pull request, em cada build, em cada verificação pós-deploy, sem que o orçamento de tokens da sua esteira exploda antes mesmo de o código chegar à água.

Este é o último capítulo da obra, e ele fecha o arco que abriu na doca seca: da quilha assentada ao casco erguido, da ponte de comando à sala de máquinas, sua embarcação agêntica está pronta para deixar o estaleiro. Falta apenas a etapa mais delicada de toda a jornada — a botadura, o momento em que o que você construiu toca a água da produção. Este capítulo projeta o pipeline completo de CI/CD conduzido por agentes, do scaffold ao deploy, e resolve a pergunta que resume tudo o que veio antes: quem, exatamente, autoriza a botadura?

## 2. Explica

A literatura técnica de 2026 mapeia cinco pontos de integração de agentes de IA em pipelines de CI/CD, e cada um resolve um problema distinto do ciclo de entrega: revisão de pull request, seleção e reparo de testes, triagem de falhas de build, remediação de segurança e verificação pós-deploy [1]. Não é um único agente genérico "que cuida do CI/CD" — é uma sequência de postos especializados, cada um com escopo e critério de aceite próprios, que juntos substituem o que antes era trabalho manual disperso entre times diferentes [2].

Times técnicos que já rodam essa esteira em produção — DeployHQ, Spacelift e Teamvoy documentam casos reais — descrevem um padrão recorrente: o agente de revisão comenta inline no diff e responde perguntas sobre impacto a jusante, o agente de testes prioriza o que o diff realmente afeta antes de rodar a suíte inteira, e o agente de build produz diagnóstico estruturado assim que uma etapa falha, em vez de apenas repetir a tentativa [3]. Essa especialização por posto reflete uma migração de mercado mais ampla, que a Forrester já descreve como a passagem definitiva de assistentes pontuais de código para agentes orquestrados de SDLC completo [20].

Pesquisa acadêmica converge para a mesma leitura por outro caminho: um framework de planejamento, codificação, testes e implantação autônomos, com pontos de checagem explícitos entre fases [18]. Trabalhos mais recentes mapeiam esse mesmo ciclo diretamente sobre o vocabulário de agentes especializados por etapa do SDLC, o que dá sustentação formal à divisão em cinco postos descrita acima [21]. Vale um contraponto que a euforia em torno de "cinco postos automatizados" costuma esconder: especializar cada posto reduz o escopo de raciocínio que cada agente precisa cobrir, mas também multiplica o número de pontos de falha coordenados que a esteira inteira precisa monitorar — cinco agentes bem calibrados individualmente ainda podem produzir um resultado ruim coletivamente se o posto de testes aprovar rápido demais o que o posto de build deveria ter rejeitado, ou se o posto de segurança rodar em paralelo com o de build em vez de depois dele. A especialização por posto não é grátis; ela troca o risco de um agente genérico sobrecarregado pelo risco, mais sutil, de lacunas na transição entre postos que ninguém desenhou para cobrir.

Na fase de scaffolding — a construção material do casco de deploy — agentes geram os quatro artefatos que sustentam qualquer entrega moderna: o arquivo YAML do pipeline (GitHub Actions ou GitLab CI), a definição de containers, a configuração de gerenciamento de segredos e os gatilhos de rollback automático [1]. Guias de configuração de revisão de código agêntica insistem num ponto que parece óbvio, mas é sistematicamente ignorado: o scaffold gerado precisa ser tão auditável quanto o código de aplicação que ele empacota, porque um pipeline mal desenhado é, na prática, uma nova superfície de ataque [4]. Essa exigência tem um custo real que equipes sob pressão de prazo tendem a subestimar: revisar um YAML de pipeline linha a linha, com a mesma atenção que se dedica a um pull request de lógica de negócio, consome tempo humano que a promessa de "scaffold automático" prometia eliminar. A resposta correta não é dispensar a revisão — é reconhecer que o scaffold gerado por agente desloca o esforço humano, não o elimina: menos tempo escrevendo YAML repetitivo, mais tempo revisando o que foi gerado antes de ele ganhar permissão de tocar produção. É o mesmo raciocínio que fundamentou a arquitetura de quatro camadas do Capítulo 2 — o agente decide o que tentar, mas o scaffold que ele produz precisa passar pelo mesmo portão de permissão de qualquer outra saída de ferramenta.

O terceiro ponto é onde a esteira deixa de ser conveniência e passa a ser risco gerido com rigor. Práticas de segurança recomendadas para agentes em CI/CD incluem credenciais de curta duração e privilégio mínimo, limite de gasto de tokens por execução, testes em sandbox isolado e limiares de confiança antes de qualquer ação consequente [14]. Riscos documentados incluem alucinação de correções — o agente propõe um patch sintaticamente plausível que não resolve a causa raiz —, repetição de ações e comportamento não-determinístico entre execuções idênticas [6].

O paper "GitInject" formaliza o risco mais contraintuitivo de todos: ataques reais de injeção de prompt embutidos em títulos de pull request, descrições de issue e comentários de código, que sequestram o raciocínio do agente já dentro do próprio pipeline de build, sem que nenhuma "conversa suspeita" tenha ocorrido [5]. A OWASP documenta o mesmo padrão estrutural em servidores MCP — dado de origem tratado como confiável vira vetor de ataque [8] —, e a Microsoft descreve esse mesmo vetor de injeção indireta em guias voltados especificamente à proteção de integrações MCP [25].

Pesquisadores independentes já demonstraram publicamente esse vetor em ferramentas conectadas via protocolo aberto, mostrando que a descrição de uma tool ou o corpo de um PR podem instruir um agente a agir sem que o usuário perceba qualquer desvio na conversa [9]. Uma avaliação sistemática de segurança em diferentes paradigmas de implantação de agente chega à mesma conclusão por outro caminho: onde o efeito real acontece é o que define o que precisa ser validado, nunca o quanto o modelo "parece" confiável [10]. Pesquisa sobre supervisão humana graduada em geração de código agêntico em domínios regulados converge para o mesmo ponto pela via da governança: autonomia crescente exige, na mesma proporção, mecanismos formais de checagem — nunca menos controle, e sim controle redesenhado [19]. Essa graduação importa porque nem toda mudança carrega o mesmo risco: um ajuste de texto em um arquivo de documentação não exige o mesmo escrutínio que uma alteração em política de rotação de segredos, e tratar as duas com o mesmo nível de aprovação humana tem um custo real — ou a esteira fica lenta demais para mudanças triviais, ou a equipe humana, sobrecarregada de aprovações de baixo risco, começa a aprovar por hábito em vez de examinar de fato, o que devolve na prática o mesmo risco que o portão deveria eliminar. A graduação correta calibra o rigor da checagem pelo que a mudança realmente toca — segredos, infraestrutura crítica, dados de produção —, não pela confiança abstrata que se deposita no agente que a propôs.

Por isso a literatura converge, sem exceção, para um único desenho de controle: o agente abre o PR, o CI valida testes e build, um humano aprova o merge, e só então o pipeline de deploy dispara automaticamente — o agente nunca faz deploy direto em produção sem revisão humana [11]. Esse desenho não é burocracia residual de uma era pré-IA — é a mesma lógica de guardrail estrutural que a própria comunidade de TDD já defende para conter código sintaticamente plausível, mas incorreto [23], formalizada por frameworks mais recentes como o TDAD, que usam análise de impacto baseada em grafos para reduzir regressões introduzidas por agentes de codificação [24].

## 3. Ilustra

### Os Cinco Postos de Guarda do Cais

Imagine o cais de lançamento do seu estaleiro dividido em cinco postos de guarda, dispostos em sequência entre a doca e a água. No primeiro posto, um agente-vigia lê cada peça de casco recém-soldada — o pull request — e deixa suas observações registradas antes de liberar passagem. No segundo, outro vigia confere se os testes de integridade da junta ainda se sustentam ou precisam de reparo. No terceiro, um vigia examina qualquer falha na linha de montagem e escreve um diagnóstico, não apenas um alarme. No quarto, um vigia de segurança rascunha o reparo de qualquer trinca encontrada. No quinto e último posto, já com a peça na água, um vigia final confere se ela realmente flutua como projetado. Cada posto escreve sua parte no diário de bordo antes de a peça seguir para o próximo.

```mermaid
%% legenda: Cinco postos de guarda do cais de lancamento, do PR aberto ao registro no diario de bordo
flowchart LR
  A[PR aberto pela tripulacao] --> B[Posto 1: revisao de PR]
  B --> C[Posto 2: selecao e reparo de testes]
  C --> D[Posto 3: triagem de falhas de build]
  D --> E[Posto 4: remediacao de seguranca]
  E --> F[Posto 5: verificacao pos-deploy]
  F --> G[Diario de bordo do estaleiro]
```

### A Lacuna Entre os Postos de Guarda

Um posto de guarda bem treinado, sozinho, não garante que a peça de casco chegue inteira à água. Imagine que o segundo posto — o que confere se os testes de integridade da junta ainda se sustentam — aprova a peça porque, isoladamente, todos os testes que ele conhece continuam passando; o terceiro posto nunca chega a ser acionado, porque, do ponto de vista dele, não houve nenhuma falha de build para triar. Nenhum dos dois postos errou a própria tarefa. O problema mora no intervalo entre eles: nenhum dos dois foi desenhado para perguntar "os testes que continuam passando cobrem de fato o que esta mudança alterou, ou só cobrem o que já cobriam antes dela?" Esse tipo de lacuna não aparece numa auditoria de posto isolado — só aparece quando alguém audita explicitamente a costura entre dois postos consecutivos, o que exige um sexto papel, não listado na sequência original: alguém (ou algum processo) responsável por conferir que a saída de um posto realmente satisfaz o que o próximo posto vai assumir como verdade.

```mermaid
%% legenda: Lacuna de cobertura entre dois postos de guarda consecutivos, mesmo com cada posto individualmente correto
flowchart LR
  A[Mudanca no diff] --> B[Posto 2: testes existentes continuam passando]
  B --> C{Testes existentes cobrem o que o diff mudou?}
  C -->|sim| D[Posto 3 nao precisa agir: seguranca real]
  C -->|nao verificado| E[Posto 3 nunca e acionado: falsa sensacao de seguranca]
  E --> F[Peca segue para o cais com lacuna nao detectada]
```

### A Doca Onde o Casco de Deploy é Soldado

O segundo pilar ganha corpo numa cena anterior ao lançamento propriamente dito: a doca onde a tripulação de agentes solda as quatro peças do casco de deploy antes de qualquer coisa se mover em direção ao cais. Uma peça é o YAML do pipeline — o roteiro que a esteira inteira vai seguir. Outra é o próprio casco do container, empacotando a aplicação de forma reproduzível. A terceira é o cofre de segredos, que nunca fica exposto na superfície do casco. A quarta é a âncora de rollback, presa ao casco antes mesmo da botadura, pronta para puxar a embarcação de volta se algo falhar na água. Nenhuma dessas quatro peças segue para o cais sem antes ser testada na doca seca. E as quatro peças não são independentes entre si: o cofre de segredos precisa ser referenciado corretamente pelo YAML do pipeline, a âncora de rollback precisa saber exatamente qual health-check do casco do container consultar, e um erro de acoplamento entre duas dessas peças — não em nenhuma delas isoladamente — é o tipo de falha que só aparece quando a doca seca testa o conjunto soldado, nunca quando testa cada peça isolada contra sua própria especificação.

```mermaid
%% legenda: Doca seca onde a tripulacao solda as quatro pecas do casco de deploy antes do lancamento
flowchart TB
  P[Ponte de Comando emite ordem de scaffold] --> Y[YAML do pipeline]
  P --> C[Casco do container]
  P --> S[Cofre de segredos]
  P --> R[Ancora de rollback]
  Y --> D[Doca seca: peca testada]
  C --> D
  S --> D
  R --> D
  D --> K[Casco de deploy pronto para o cais]
```

### O Portão do Cais: Fluxo Saudável e Fluxo Sabotado

O terceiro pilar é o mais denso do capítulo e merece duas imagens complementares — uma para a mecânica geral do fluxo, outra para o ponto mais difícil de aceitar. A primeira imagem é o fluxo saudável: o agente abre o PR, o CI confere testes e build, um humano no cais examina o que está prestes a tocar a água e só então autoriza — a botadura acontece depois, nunca antes, do sinal humano.

```mermaid
%% legenda: Fluxo saudavel do portao de aprovacao humana, do PR aberto a botadura em producao
flowchart LR
  A[Agente abre PR] --> B[CI valida testes e build]
  B --> C{Humano aprova o merge?}
  C -->|sim| D[Pipeline de deploy dispara]
  C -->|nao| E[PR devolvido com diagnostico]
  D --> F[Cais de lancamento: portao final]
  F --> G[Botadura: producao]
```

A segunda imagem é o ponto realmente contraintuitivo, e é aqui que o conceito exige uma segunda camada de analogia: o mesmo fluxo pode ser sabotado sem que nenhum alarme convencional dispare. Imagine que uma instrução maliciosa não chega pela ponte de comando nem por nenhuma conversa da tripulação — ela chega embutida na própria etiqueta de carga afixada na peça de casco, escrita por quem submeteu o pull request. O agente lê essa etiqueta como faria com qualquer especificação legítima de carga, porque, do ponto de vista do seu raciocínio, ler dados do próprio repositório é um passo esperado do fluxo. Sem um portão determinístico no cais, a peça sabotada segue direto para a água. Com o portão, o humano que inspeciona a carga antes da botadura é a última barreira capaz de reconhecer que aquela etiqueta nunca fez parte da ordem de serviço original.

```mermaid
%% legenda: Fluxo sabotado por instrucao oculta em dado de repositorio, tipo GitInject, e o portao humano como ultima barreira
flowchart TD
  A[Titulo do PR ou issue contem instrucao oculta] --> B[Agente le dado do repositorio como contexto confiavel]
  B --> C[Agente tenta aplicar acao disfarcada de correcao legitima]
  C --> D{Portao de aprovacao humana no cais}
  D -->|sem blindagem| E[Botadura comprometida]
  D -->|com blindagem| F[Humano recusa: instrucao suspeita barrada]
  F --> G[Diario de bordo registra a tentativa]
```

## 4. Técnica

Esta seção fabrica, em código, as três peças descritas acima: o YAML dos cinco postos de guarda, o script de scaffold que solda as quatro peças do casco de deploy, e o portão de aprovação humana como função de política executável — cada posto pensado para rodar de forma confiável em tarefas longas e repetidas, o mesmo requisito documentado para harnesses de agentes de execução estendida [22].

### Os Cinco Postos de Guarda em YAML

O primeiro artefato materializa a esteira da seção Ilustra como um workflow real de GitHub Actions, com um job nomeado para cada um dos cinco pontos de integração documentados pela literatura [1].

```yaml
name: Esteira do Estaleiro - CI/CD com Agentes

on:
  pull_request:
    branches: [main]

jobs:
  revisao_pr:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Agente revisa o diff
        run: |
          echo "Agente inspeciona o PR, deixa comentarios inline e sinaliza risco de regressao a jusante"
          python scripts/agente_revisor.py --pr "${{ github.event.pull_request.number }}"

  testes:
    needs: revisao_pr
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Agente seleciona e repara testes
        run: |
          echo "Agente prioriza testes afetados pelo diff; nunca apaga teste que falha para o build ficar verde"
          pytest --maxfail=1 --disable-warnings

  build:
    needs: testes
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Triagem de falha de build pelo agente
        run: |
          echo "Se o build falhar, o agente redige diagnostico estruturado antes de qualquer nova tentativa"
          docker build -t estaleiro-app:${{ github.sha }} .

  remediacao_seguranca:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Scanner de seguranca e patch do agente
        run: |
          echo "Agente rascunha patch; scanner reexecuta no branch do patch para confirmar a correcao"
          trivy image estaleiro-app:${{ github.sha }}

  verificacao_pos_deploy:
    needs: remediacao_seguranca
    runs-on: ubuntu-latest
    environment:
      name: producao
    steps:
      - uses: actions/checkout@v4
      - name: Portao de aprovacao humana antes da botadura
        run: echo "Aguardando aprovacao humana registrada no ambiente 'producao' do GitHub Actions"
      - name: Verificacao pos-deploy
        run: |
          echo "Agente confere health-check, taxa de erro e latencia apos a botadura"
          curl -f https://app.estaleiro.exemplo/health
```

Repare que `verificacao_pos_deploy` está condicionado ao ambiente `producao` do GitHub Actions, o mecanismo nativo de "environment protection rule" que já impõe um humano registrado antes de qualquer job avançar — é a materialização, em plataforma real, do desenho de controle descrito na seção Explica [5]. Documentação recente sobre revisão de código agêntica reforça o mesmo ponto: cada posto deve poder ser auditado isoladamente, sem depender do posto anterior ter "confiado" corretamente [4]. Note também que a cadeia de `needs` entre os cinco jobs — `testes` depende de `revisao_pr`, `build` depende de `testes`, e assim sucessivamente — é o que torna a lacuna descrita na Ilustra visível em vez de invisível: se um posto precisasse produzir apenas um sinal binário de "passou/falhou" sem que o próximo posto pudesse inspecionar o que exatamente foi verificado, a costura entre `testes` e `build` seria opaca por construção. Expor `arquivos_sem_cobertura` como parte da saída do job de testes, em vez de apenas um booleano de sucesso, é o que permite ao próximo posto — ou a um humano revisando o log — perceber a lacuna antes que ela vire uma botadura comprometida.

### Soldando o Casco de Deploy na Doca

O segundo artefato gera, programaticamente, as quatro peças da seção Ilustra: Dockerfile, workflow de CI com segredos geridos pelo provedor (nunca em texto plano) e o gatilho de rollback condicionado a falha de health-check.

```python
import os
import textwrap


def gerar_dockerfile(caminho: str = "Dockerfile") -> None:
    """Gera o casco do container: imagem minima e reproduzivel."""
    conteudo = textwrap.dedent("""\
        FROM python:3.12-slim
        WORKDIR /app
        COPY requirements.txt .
        RUN pip install --no-cache-dir -r requirements.txt
        COPY . .
        HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1
        CMD ["python", "app.py"]
    """)
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)


def gerar_workflow_ci(caminho: str = ".github/workflows/estaleiro.yml") -> None:
    """Gera o YAML do pipeline com segredos via cofre do provedor de CI."""
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    conteudo = textwrap.dedent("""\
        name: Esteira do Estaleiro
        on:
          push:
            branches: [main]
        jobs:
          deploy:
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@v4
              - name: Login no registro de containers
                env:
                  REGISTRY_TOKEN: ${{ secrets.REGISTRY_TOKEN }}
                run: echo "Autenticando com token injetado pelo cofre de segredos, nunca em texto plano"
              - name: Build e push da imagem
                run: docker build -t estaleiro-app . && docker push estaleiro-app
              - name: Rollback condicionado a falha de health-check
                run: bash scripts/rollback_se_falha.sh
    """)
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)


def gerar_gatilho_rollback(caminho: str = "scripts/rollback_se_falha.sh") -> None:
    """Gera a ancora de rollback: reverte a botadura se o health-check falhar."""
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    conteudo = textwrap.dedent("""\
        #!/usr/bin/env bash
        set -euo pipefail
        if ! curl -sf https://app.estaleiro.exemplo/health; then
          echo "Health-check pos-deploy falhou: revertendo para a ultima versao estavel"
          kubectl rollout undo deployment/estaleiro-app
          exit 1
        fi
        echo "Health-check aprovado: botadura mantida"
    """)
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)


if __name__ == "__main__":
    gerar_dockerfile()
    gerar_workflow_ci()
    gerar_gatilho_rollback()
```

Cada função tem uma única responsabilidade e escreve um único artefato — o mesmo princípio de simplicidade deliberada já defendido no Capítulo 2 para orquestração de agentes se aplica, ponto a ponto, à geração de scaffold: cobrir a tarefa real sem multiplicar peças que ninguém vai auditar de fato [11]. Casos documentados de SDLC "AI-first" ponta a ponta, como o da Fujitsu, mostram esse mesmo scaffold sendo gerado como parte de um ciclo contínuo entre requisitos, implementação e testes de integração [12], e a Microsoft descreve, em conjunto com o GitHub, uma esteira equivalente construída sobre Azure [13].

### O Portão de Lançamento como Função de Política

O terceiro artefato é o mais crítico do capítulo: a função que decide, de forma determinística, se uma solicitação de deploy pode avançar até a botadura — independentemente de quão convincente tenha sido o raciocínio do agente que a originou.

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class SolicitacaoDeploy:
    autor: str
    toca_infraestrutura_critica: bool
    toca_segredos: bool
    testes_passaram: bool
    aprovacao_humana_token: Optional[str] = None


class PortaoBarradoError(Exception):
    """Levantada quando a botadura e recusada pelo portao de aprovacao humana."""


def portao_de_lancamento(solicitacao: SolicitacaoDeploy, diario_de_bordo: list) -> dict:
    """Unico ponto de decisao entre o pipeline de CI e a botadura em producao.

    Nenhuma mudanca que toque infraestrutura critica ou segredos avanca sem um
    token de aprovacao humana explicito, mesmo que todos os testes tenham
    passado: alucinacao de correcao e comportamento nao-deterministico do
    agente nao sao filtrados por nenhum teste automatizado.
    """
    exige_aprovacao = solicitacao.toca_infraestrutura_critica or solicitacao.toca_segredos

    if exige_aprovacao and not solicitacao.aprovacao_humana_token:
        registro = {
            "autor": solicitacao.autor,
            "decisao": "bloqueado",
            "motivo": "mudanca sensivel sem token de aprovacao humana",
            "timestamp": datetime.utcnow().isoformat(),
        }
        diario_de_bordo.append(registro)
        raise PortaoBarradoError("Botadura recusada: aprovacao humana obrigatoria e ausente")

    if not solicitacao.testes_passaram:
        registro = {
            "autor": solicitacao.autor,
            "decisao": "bloqueado",
            "motivo": "testes nao passaram",
            "timestamp": datetime.utcnow().isoformat(),
        }
        diario_de_bordo.append(registro)
        raise PortaoBarradoError("Botadura recusada: testes falharam")

    registro = {
        "autor": solicitacao.autor,
        "decisao": "liberado",
        "aprovador": solicitacao.aprovacao_humana_token or "automatico_baixo_risco",
        "timestamp": datetime.utcnow().isoformat(),
    }
    diario_de_bordo.append(registro)
    return registro


if __name__ == "__main__":
    diario = []
    tentativa = SolicitacaoDeploy(
        autor="agente-scaffold-01",
        toca_infraestrutura_critica=True,
        toca_segredos=False,
        testes_passaram=True,
        aprovacao_humana_token=None,
    )
    try:
        portao_de_lancamento(tentativa, diario)
    except PortaoBarradoError as erro:
        print(f"Bloqueado como esperado: {erro}")
    print(diario)
```

Nenhuma linha desta função consulta o raciocínio do agente para decidir se confia nele — a decisão depende apenas de três fatos verificáveis: o que a mudança toca, se os testes passaram e se existe um token de aprovação humana registrado. É exatamente essa independência do raciocínio do modelo que a literatura de segurança de agentes recomenda como controle real contra alucinação e comportamento não-determinístico [14], e é o mesmo padrão arquitetural já defendido para servidores MCP no Capítulo 8: controles eficazes vivem fora do contexto do modelo, nunca dentro dele [15]. Frameworks de confiabilidade de agentes de produção chegam à mesma conclusão por outro caminho, tratando "humano no loop para ações irreversíveis" como um dos fatores estruturais de um agente pronto para produção, não um acessório opcional [16].

### Fechando a Lacuna Entre Postos: Verificação de Cobertura Real do Diff

O quarto artefato materializa o sexto papel descrito na Ilustra: uma checagem explícita de que os arquivos alterados pelo diff estão de fato cobertos pelos testes que "continuaram passando" — em vez de assumir que teste verde equivale a mudança verificada.

```python
from dataclasses import dataclass, field


@dataclass
class VerificacaoCoberturaDiff:
    arquivos_alterados: list = field(default_factory=list)
    arquivos_cobertos_por_teste: list = field(default_factory=list)

    def lacunas(self) -> list:
        """Retorna arquivos alterados sem nenhum teste que os exercite."""
        return [
            arquivo for arquivo in self.arquivos_alterados
            if arquivo not in self.arquivos_cobertos_por_teste
        ]

    def cobertura_suficiente(self) -> bool:
        """Barra a transicao 'testes passaram' -> 'seguro para build' quando
        existe arquivo alterado que nenhum teste conhecido exercita - fecha
        exatamente a lacuna entre o Posto 2 e o Posto 3 descrita na Ilustra."""
        return len(self.lacunas()) == 0


def gate_pos_testes(verificacao: VerificacaoCoberturaDiff) -> dict:
    if not verificacao.cobertura_suficiente():
        return {
            "decisao": "bloqueado",
            "motivo": "arquivos alterados sem cobertura de teste",
            "arquivos_sem_cobertura": verificacao.lacunas(),
        }
    return {"decisao": "liberado_para_build"}


if __name__ == "__main__":
    verificacao = VerificacaoCoberturaDiff(
        arquivos_alterados=["politica_rotacao_segredos.py", "health_check.py"],
        arquivos_cobertos_por_teste=["health_check.py"],
    )
    print(gate_pos_testes(verificacao))
```

O exemplo acima bloqueia deliberadamente: `politica_rotacao_segredos.py` foi alterado, mas nenhum teste conhecido o exercita, então o gate recusa a transição automática para o Posto 3 mesmo que a suíte existente esteja inteiramente verde. Essa checagem não substitui os cinco postos da seção Ilustra — ela audita a costura entre dois deles, exatamente o papel que a literatura de revisão agêntica recomenda quando descreve auditabilidade posto a posto como requisito, não como bônus [4].

## 5. Aplica

Você lidera a squad de plataforma do estaleiro digital e configurou, semanas atrás, uma regra de conveniência: pull requests marcados pelo próprio agente de revisão como `risco: baixo` pulam a fila de aprovação humana e disparam deploy automático assim que o CI fica verde. Um pull request chega com o título "fix: corrige timeout intermitente no health-check (baixo risco, apenas config)". O agente de revisão lê o título, concorda com a classificação, aplica a label `risco: baixo`, o CI passa, e o deploy dispara sozinho — exatamente como você configurou.

O erro só aparece no diário de bordo horas depois: a mudança "de baixo risco" alterava também a política de rotação de segredos do serviço, e o título do PR foi escrito deliberadamente para convencer o próprio agente classificador de que aquilo era uma configuração trivial. Nada na conversa com o usuário foi suspeito — a instrução veio embutida no dado de repositório que o agente trata como contexto legítimo desde o momento em que o PR foi aberto, o mesmo vetor que o paper "GitInject" documenta em pipelines reais de CI/CD [5]. O diagnóstico correto não é "o agente raciocinou mal" — é que você deixou o mesmo agente que lê dados não confiáveis do repositório decidir, sozinho, se uma mudança sensível merecia ou não passar pelo portão humano. Confiança circular: quem classifica o risco não pode ser quem dispensa a checagem daquele risco.

A correção é estrutural, não um ajuste de prompt: a label de risco gerada pelo agente vira apenas um sinal informativo no diário de bordo, nunca um insumo da decisão de aprovação. O `portao_de_lancamento` da seção Técnica passa a decidir com base em fatos verificáveis sobre o que o diff realmente toca — segredos, infraestrutura crítica — e não com base na etiqueta que o próprio agente afixou na carga. A verificação de cobertura de diff da seção Técnica fecha o segundo ângulo do mesmo incidente: mesmo que a política de rotação de segredos tivesse sido classificada corretamente como sensível, nada garantiria que os testes existentes de fato exercitassem aquele arquivo — a lacuna entre "os testes passaram" e "os testes que passaram cobrem o que mudou" é exatamente o tipo de intervalo entre postos que nenhum posto isolado foi desenhado para fechar sozinho. Como Engenheiro Agêntico, seu trabalho nunca foi confiar menos no agente em abstrato — foi garantir que a classificação de risco e a autorização de deploy nunca dependam da mesma fonte de raciocínio.

O erro de configuração original — pular a fila de aprovação humana para PRs marcados como `risco: baixo` — nasceu de uma intenção legítima: reduzir atrito para mudanças genuinamente triviais. O problema nunca foi essa intenção, foi delegar a própria classificação de risco ao mesmo agente cuja leitura de dados de repositório não confiáveis é, estruturalmente, o vetor de ataque documentado desde o Capítulo 8. Qualquer atalho de conveniência que reduza fricção de aprovação precisa nascer amarrado a uma fonte de decisão que o próprio dado manipulável não consegue influenciar.

Armadilhas recorrentes na integração de agentes em CI/CD, na prática de mercado:

- Deixar o mesmo agente que lê título, issue e comentários do PR também decidir, sem checagem externa, se aquela mudança é sensível o suficiente para exigir aprovação humana [8].
- Tratar "os testes passaram" como sinônimo de "seguro para produção" — testes automatizados não capturam alucinação de correção nem comportamento não-determinístico entre execuções [6].
- Gerar YAML de pipeline e Dockerfile via agente sem revisão, assumindo que scaffold é território de baixo risco por não ser "lógica de negócio" [4].
- Medir sucesso da esteira agêntica apenas por velocidade de merge, ignorando que 76,6% das organizações já usam IA ativamente em desenvolvimento [17] — e a maioria delas ainda está calibrando exatamente esse equilíbrio entre velocidade e portão de aprovação.
- Assumir que "os cinco postos estão todos configurados" equivale a "a esteira está segura", sem auditar a costura entre postos consecutivos — um posto de testes que aprova cobertura antiga e um posto de build que nunca é acionado por falta de gatilho podem, juntos, deixar passar exatamente o que cada um isoladamente foi desenhado para barrar [4].

## 6. Conclusão

Três pontos fecham este capítulo. Primeiro: CI/CD agêntico não é um agente genérico solto na esteira — são cinco postos de guarda especializados, cada um com escopo e critério de aceite próprios, do PR à verificação pós-deploy. Segundo: o scaffold que sustenta o deploy — pipeline, container, segredos, rollback — precisa da mesma auditabilidade que você já exige do código de aplicação, porque um scaffold mal desenhado é, ele mesmo, superfície de ataque. Terceiro, e mais urgente: nenhum deploy é 100% autônomo, porque os riscos documentados — GitInject, alucinação de correção, comportamento não-determinístico — não são filtrados por teste automatizado nenhum. O portão de aprovação humana no cais de lançamento não é resquício de um mundo pré-IA; é a peça de engenharia que torna a autonomia do resto da esteira segura o suficiente para existir.

E este ponto fecha também a obra inteira. Você começou na doca seca do Capítulo 1 aprendendo a diferença entre vibe coding — cada rebite aprovado manualmente — e agentic coding, uma tripulação autônoma soldando o casco inteiro com um diário de bordo auditável por trás. Capítulo a capítulo, você ergueu essa embarcação: entendeu as quatro camadas que compõem qualquer agente, equipou a ponte de comando com skills, MCPs e regras escritas com precisão, blindou a sala de máquinas com permissões e hooks, fabricou suas próprias ferramentas resistentes a manual adulterado, e aprendeu a operar tudo isso sem afundar em custo de contexto. Nada disso mudou a conclusão à qual toda essa jornada converge: autonomia agêntica madura não é ausência de humano — é autonomia supervisionada, com guardrails em cada camada e um humano no portão final entre o que o agente construiu e a água. Como Engenheiro Agêntico, seu estaleiro está pronto para a botadura. O leme, a partir daqui, continua com você.

## 7. Referências Bibliográficas

[1] DEPLOYHQ. *AI Agents in CI/CD Pipelines: From GitHub Issue to Production Deploy*. Disponível em: https://www.deployhq.com/blog/ai-agents-cicd-pipelines-github-issue-to-production-deploy. Acesso em: 02 ago. 2026.

[2] SPACELIFT. *Where Do AI Agents Fit in CI/CD Pipelines?*. Disponível em: https://spacelift.io/blog/agentic-cicd. Acesso em: 02 ago. 2026.

[3] TEAMVOY. *AI Agents in CI/CD Pipelines: A Guide for Tech Leads*. Disponível em: https://teamvoy.com/blog/building-ai-agents-into-your-ci-cd-pipeline-a-playbook-for-tech-leads/. Acesso em: 02 ago. 2026.

[4] AUGMENT CODE. *How to Set Up AI Code Review in Your CI/CD Pipeline*. Disponível em: https://www.augmentcode.com/guides/ai-code-review-ci-cd-pipeline. Acesso em: 02 ago. 2026.

[5] ARXIV.ORG. *GitInject: Real-World Prompt Injection Attacks in AI-Powered CI/CD Pipelines*. Disponível em: https://arxiv.org/pdf/2606.09935. Acesso em: 02 ago. 2026.

[6] ARXIV.ORG. *Vibe Coding vs. Agentic Coding: Fundamentals and Practical Implications of Agentic AI*. Disponível em: https://arxiv.org/pdf/2505.19443. Acesso em: 02 ago. 2026.

[7] ANTHROPIC. *Effective context engineering for AI agents*. Disponível em: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents. Acesso em: 02 ago. 2026.

[8] OWASP FOUNDATION. *MCP Tool Poisoning*. Disponível em: https://owasp.org/www-community/attacks/MCP_Tool_Poisoning. Acesso em: 02 ago. 2026.

[9] WILLISON, Simon. *Model Context Protocol has prompt injection security problems*. Disponível em: https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/. Acesso em: 02 ago. 2026.

[10] ARXIV.ORG. *Bridging AI and Software Security: A Comparative Vulnerability Assessment of LLM Agent Deployment Paradigms*. Disponível em: https://arxiv.org/pdf/2507.06323. Acesso em: 02 ago. 2026.

[11] ANTHROPIC. *Building Effective AI Agents*. Disponível em: https://www.anthropic.com/research/building-effective-agents. Acesso em: 02 ago. 2026.

[12] FUJITSU. *Fujitsu automates entire software development lifecycle with new AI-Driven Software Development Platform*. Disponível em: https://global.fujitsu/en-global/pr/news/2026/02/17-01. Acesso em: 02 ago. 2026.

[13] MICROSOFT. *An AI led SDLC: Building an End-to-End Agentic Software Development Lifecycle with Azure and GitHub*. Disponível em: https://techcommunity.microsoft.com/blog/appsonazureblog/an-ai-led-sdlc-building-an-end-to-end-agentic-software-development-lifecycle-wit/4491896. Acesso em: 02 ago. 2026.

[14] CLOUD SECURITY ALLIANCE. *Agentic MCP Security Best Practices Guide*. Disponível em: https://labs.cloudsecurityalliance.org/agentic/agentic-mcp-security-best-practices-v1/. Acesso em: 02 ago. 2026.

[15] GENERAL ANALYSIS. *Anthropic Claude Code Security Best Practices: Permissions, Hooks, MCP, Sandboxing, and CI/CD*. Disponível em: https://generalanalysis.com/guides/anthropic-claude-code-security-best-practices. Acesso em: 02 ago. 2026.

[16] HUMANLAYER. *12-Factor Agents — Principles for Building Reliable LLM Applications*. Disponível em: https://www.humanlayer.dev/12-factor-agents. Acesso em: 02 ago. 2026.

[17] FUTURUM GROUP. *AI Reaches 97% of Software Development Organizations*. Disponível em: https://futurumgroup.com/press-release/ai-reaches-97-of-software-development-organizations/. Acesso em: 02 ago. 2026.

[18] RESEARCHGATE. *AI-First Software Development Lifecycle: An Agent-Driven Framework for Autonomous Planning, Coding, Testing, and Deployment*. Disponível em: https://www.researchgate.net/publication/403670772_AI-First_Software_Development_Lifecycle_An_Agent-Driven_Framework_for_Autonomous_Planning_Coding_Testing_and_Deployment. Acesso em: 02 ago. 2026.

[19] ARXIV.ORG. *Governed AI-Assisted Engineering: Graduated Human Oversight for Agentic Code Generation in Regulated Domains*. Disponível em: https://arxiv.org/pdf/2606.22484. Acesso em: 02 ago. 2026.

[20] FORRESTER. *Agentic Software Development Takes The Lead: From Code Assistants To Orchestrated SDLC Agents*. Disponível em: https://www.forrester.com/blogs/agentic-software-development-takes-the-lead-from-code-assistants-to-orchestrated-sdlc-agents/. Acesso em: 02 ago. 2026.

[21] ARXIV.ORG. *Agentic AI in the Software Development Lifecycle*. Disponível em: https://arxiv.org/pdf/2604.26275. Acesso em: 02 ago. 2026.

[22] ANTHROPIC. *Effective harnesses for long-running agents*. Disponível em: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents. Acesso em: 02 ago. 2026.

[23] EXADEL. *Test-Driven Development & AI Coding: Why TDD Matter*. Disponível em: https://exadel.com/news/test-driven-development-ai-coding. Acesso em: 02 ago. 2026.

[24] ARXIV.ORG. *TDAD: Test-Driven Agentic Development — Reducing Code Regressions in AI Coding Agents via Graph-Based Impact Analysis*. Disponível em: https://arxiv.org/html/2603.17973v1. Acesso em: 02 ago. 2026.

[25] MICROSOFT. *Protecting against indirect prompt injection attacks in MCP*. Disponível em: https://developer.microsoft.com/blog/protecting-against-indirect-injection-attacks-mcp/. Acesso em: 02 ago. 2026.
