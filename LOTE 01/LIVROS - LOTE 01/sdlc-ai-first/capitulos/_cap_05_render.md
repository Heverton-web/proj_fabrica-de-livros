# Capítulo 5: Os Motores: Harness, Skills, MCPs e Worktrees

## 1. Introdução

No Capítulo 4, você desenhou a cartografia do domínio: vocabulário ubíguo, interfaces primeiro e ADRs — o mapa que orienta os agentes. Agora chegou a hora de conhecer os motores que colocam o mapa em movimento: o harness agêntico que orquestra, as skills que especializam, os MCPs que conectam ferramentas e as worktrees que isolam territórios de trabalho.

Este capítulo é o mais operacional da Parte III. Você vai aprender a arquitetura harness → LLM → ferramentas, entender como skills empacotam procedimentos reutilizáveis, como MCPs exponibilizam ferramentas via protocolo padrão, e como worktrees permitem despacho paralelo seguro de agentes. Você vai sair com um laboratório de motores configurável — e o hábito de test-first como régua do build.

## 2. Explica

Um harness agêntico é o ambiente de execução que dá ao LLM a capacidade de **agir**, não apenas de responder. A distinção é estrutural: um chat responde; um harness executa um loop — o modelo propõe uma ação, a ferramenta executa, o resultado volta para o modelo, que propõe a próxima ação. É esse loop de execução com feedback que transforma um LLM em um agente [1].

O framework conceitual é sempre o mesmo: harness → LLM → ferramentas. O harness é o processo que gerencia o loop (bash, edição de arquivos, testes, navegação). O LLM é o cérebro que decide as ações dentro do loop. E as ferramentas são os músculos — comandos, scripts, APIs — que o LLM aciona. A pesquisa da Anthropic demonstrou que a qualidade do scaffolding do harness (as ferramentas e sua interface) tem impacto tão grande quanto o modelo na resolução de problemas reais [2].

As skills são o próximo nível: procedimentos empacotados que especializam o agente. Uma skill é um conjunto de instruções reutilizáveis — um fluxo de trabalho, regras de domínio, templates — que o agente carrega quando o contexto exige. No SDLC AI-first, as skills são os operários especializados: a skill de redação, a skill de revisão, a skill de testes. Elas codificam o conhecimento que uma equipe humana levaria anos para acumular [3].

Os MCPs (Model Context Protocol) resolvem um problema de conectividade: como o agente acessa os sistemas de dados e ferramentas da organização. Antes do MCP, cada integração era um adaptador customizado. Com o MCP, um protocolo padrão conecta o harness a qualquer fonte — repositório, banco de dados, sistema de tickets — com autenticação e contexto seguros [4]. Para o ciclo de vida, o MCP é o sistema de radar da torre: conecta o agente aos dados de que ele precisa sem arrastar o mundo inteiro para o contexto.

As worktrees de git são o instrumento de isolamento. Cada agente — ou cada lote de agentes — trabalha em uma cópia isolada do repositório (uma worktree), e os resultados são integrados por merge controlado. Isso elimina a classe inteira de conflitos de edição concorrente que derrubam equipes agênticas [5]. Worktree não é conveniência; é a célula de contenção do build paralelo.

O test-first completa o quadro operacional. A régua do build é: escrever o teste vermelho antes do código que o faz passar. No contexto agêntico, o teste é o contrato de conclusão: o agente termina quando a suíte passa, não quando ele acha que está pronto. A verificação deixa de ser opinião e vira execução — um diffs cujo critério de pronto é mensurável [6].

A combinação dos quatro instrumentos é o que separa o laboratório do caos: harness gerencia o loop, skills especializam o comportamento, MCPs conectam os dados e worktrees isolam a execução. Cada um resolve uma classe específica de falha, e juntos definem o ambiente onde o SDLC AI-first opera de verdade [7].

## 3. Ilustra

A torre de controle moderna não é só um prédio com radar — é uma arquitetura de sistemas. O radar (MCP) conecta a torre aos dados de voo. Os procedimentos operacionais padrão (skills) dizem ao controlador exatamente o que fazer em cada situação. As cabines de controle (worktrees) isolam cada controlador em seu setor, com suas telas e seus dados — ninguém edita a tela do vizinho. E a torre em si (harness) orquestra tudo, rodando o loop de observar-decidir-agir continuamente.

![Arquitetura de motores do SDLC AI-first](../imagens/diagramas/dia_05_01_aa8480e58c.png)

Como Comandante de Operações de Software, você percebe o padrão: cada motor responde a uma pergunta operacional. O harness responde "como o agente age?". As skills respondem "o que o agente sabe fazer?". Os MCPs respondem "a que o agente tem acesso?". As worktrees respondem "onde o agente pode pisar?" [8].

## 4. Técnica

### O Loop do Harness em Código

O coração do harness é o loop agêntico. A implementação abaixo — deliberadamente minimalista — mostra a anatomia: o modelo propõe, a ferramenta executa, o resultado volta.

```python
from dataclasses import dataclass, field
from typing import Callable, Dict, List


@dataclass
class Tool:
    nome: str
    funcao: Callable[[str], str]
    descricao: str = ""


class HarnessSimples:
    def __init__(self, ferramentas: List[Tool]) -> None:
        self.ferramentas: Dict[str, Tool] = {t.nome: t for t in ferramentas}
        self.historico: List[str] = field(default_factory=list)

    def agir(self, acao: str, argumento: str) -> str:
        if acao not in self.ferramentas:
            return f"ERRO: ferramenta '{acao}' inexistente"
        self.historico.append(f"{acao}({argumento})")
        return self.ferramentas[acao].funcao(argumento)

    def loop(self, modelo_acao) -> List[str]:
        """Simula o loop: modelo -> ferramenta -> feedback -> proxima acao."""
        resultado = ""
        passos = 0
        while passos < 10:
            acao, argumento = modelo_acao(resultado)
            if acao == "FIM":
                break
            resultado = self.agir(acao, argumento)
            passos += 1
        return self.historico


def ler_arquivo(caminho: str) -> str:
    try:
        with open(caminho, encoding="utf-8") as f:
            return f.read()[:200]
    except OSError as exc:
        return f"ERRO: {exc}"


def escrever_arquivo(conteudo: str) -> str:
    return f"OK: {len(conteudo)} caracteres em buffer (nao gravado neste exemplo)"


harness = HarnessSimples([
    Tool("ler", ler_arquivo, "le um arquivo"),
    Tool("escrever", escrever_arquivo, "escreve conteudo"),
])

# Simulacao de um "modelo" burro mas funcional
def modelo_exemplo(ultimo_resultado: str):
    if "erro" in ultimo_resultado.lower():
        return "FIM", ""
    return "ler", "README.md"


print(harness.loop(modelo_exemplo))
```

A moral do trecho: o harness não é mágica — é um loop disciplinado de ação e feedback. É essa estrutura que permite ao agente tentar, falhar e corrigir dentro de um ambiente controlado [9].

### Configuração de Ferramentas com MCP

O MCP padroniza a conexão com dados. A configuração abaixo, no formato `.mcp.json`, registra servidores MCP de arquivos e banco de dados:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/projeto/codigo",
        "/projeto/specs"
      ]
    },
    "sqlite": {
      "command": "npx",
      "args": ["-y", "mcp-server-sqlite", "/projeto/data/estado.db"]
    }
  }
}
```

A vantagem prática para o ciclo de vida: o agente consulta o banco de estado da esteira (fase atual, artefatos produzidos) via MCP, sem que o orquestrador carregue tudo no contexto. O protocolo faz a entrega sob demanda — a essência do lean context [10].

### Skills como Procedimentos Empacotados

Uma skill é um arquivo de instruções que o agente carrega sob demanda. O esqueleto abaixo mostra a anatomia:

```markdown
# Skill: revisor-espec

## Quando usar
Quando um artefato de spec for produzido na Fase 2 do ciclo.

## Procedimento
1. Leia a spec e extraia os requisitos R1..Rn.
2. Para cada requisito, verifique se existe criterio de aceite testavel.
3. Se algum requisito nao tiver criterio, reprove com a lista de falhas.
4. Se todos tiverem, aprove e registre o parecer com evidencia.

## Regras
- Nunca reescreva a spec; apenas aprove ou reprove com lista objetiva.
- Evidencia antes de afirmacao: cite a linha do criterio em cada parecer.
```

O valor da skill está na reutilização: o mesmo procedimento roda em todas as specs, com a mesma régua — eliminando a variação entre revisores [11].

### Worktrees em Ação

O isolamento de território por worktree é trivial no git, mas muda o jogo agêntico:

```bash
# criar worktree isolada para o agente A (modulo de pagamentos)
git worktree add ../wt-pagamentos -b feature/pagamentos main

# criar worktree isolada para o agente B (modulo de inventario)
git worktree add ../wt-inventario -b feature/inventario main

# ao concluir, cada agente abre um PR; o merge e controlado na raiz
git worktree list
```

Cada worktree é um repositório completo com branch própria. Dois agentes nunca editam o mesmo arquivo físico. E o merge — autorizado pelo controlador humano — é o ponto único de integração [5].

### O Manifesto de Skills do Time

Skills precisam de descoberta: o agente precisa saber qual skill carregar em cada fase. O manifesto abaixo declara o catálogo de skills — quando usar, qual fase serve e qual artefato produz.

```json
{
  "skills": [
    {
      "nome": "revisor-espec",
      "fase": "spec",
      "disparo": "artefato spec_executavel produzido",
      "artefato_saida": "parecer_espec.md"
    },
    {
      "nome": "estrategista-pilares",
      "fase": "design",
      "disparo": "capitulo de design iniciado",
      "artefato_saida": "pilares.json"
    },
    {
      "nome": "redator-eita",
      "fase": "build",
      "disparo": "pilares aprovados",
      "artefato_saida": "capitulo.md"
    },
    {
      "nome": "verificador-adversarial",
      "fase": "verificar",
      "disparo": "diff do build",
      "artefato_saida": "parecer_verificacao.md"
    }
  ],
  "regra": "uma skill por fase; o orquestrador consulta o manifesto antes de delegar"
}
```

O manifesto é o catálogo de procedimentos da torre: quando o controlador precisa de um procedimento, consulta o catálogo — nunca improvisa [19].

### O Modelo de Sequenciamento de Skills

As skills não agem isoladas — elas se encadeiam em um fluxo. O modelo de sequenciamento declara a ordem e as dependências entre skills de uma fase:

| Skill | Fase | Depende de | Alimenta |
|-------|------|------------|----------|
| Estrategista | Design | Cartografia | Redator |
| Redator | Build | Estrategista | Verificador |
| Verificador | Verificar | Redator | Revisor |
| Revisor | Verificar | Verificador | Compilador |

O sequenciamento evita o erro clássico do despacho: a skill que roda antes de sua entrada existir. A esteira consulta o sequenciamento antes de cada ativação — a skill só carrega quando o que ela precisa está pronto [27].

### O Modelo de Avaliação de Ferramentas por Critério Ponderado

O laboratório precisa comparar ferramentas de forma justa — e a comparação exige critérios ponderados, não impressão. O modelo abaixo pontua cada ferramenta em cinco dimensões e devolve o ranking:

```python
CRITERIOS = {
    'qualidade_saida': 0.3,
    'custo_contexto': 0.25,
    'confiabilidade': 0.2,
    'facilidade_uso': 0.15,
    'comunidade': 0.1,
}

def rankear_ferramentas(ferramentas):
    resultado = []
    for nome, notas in ferramentas.items():
        score = sum(notas[c] * CRITERIOS[c] for c in CRITERIOS)
        resultado.append({'ferramenta': nome, 'score': round(score, 2)})
    return sorted(resultado, key=lambda x: x['score'], reverse=True)

ferramentas = {
    'harness-alpha': {'qualidade_saida': 4, 'custo_contexto': 3, 'confiabilidade': 4, 'facilidade_uso': 3, 'comunidade': 2},
    'harness-beta': {'qualidade_saida': 3, 'custo_contexto': 4, 'confiabilidade': 3, 'facilidade_uso': 4, 'comunidade': 4},
}
print(rankear_ferramentas(ferramentas))
```

O ranking por score substitui o debate de opinião pela tabela: se o harness-alpha ganha por pouco em qualidade de saída, mas consome muito contexto e tem comunidade pequena, o harness-beta pode ser a escolha de longo prazo. Os pesos são calibrados pela própria organização — uma equipe pequena valoriza facilidade de uso mais que comunidade. O ranking é um ponto de partida para conversa, não um veredito automático, mas obriga a conversa a ser sobre os números.

### O Estudo de Caso: Montando o Laboratório de Motores

A escolha do harness é uma decisão de arquitetura — e o Comandante a faz com critérios explícitos. O modelo abaixo é a matriz de avaliação que compara opções antes de investir:

| Critério | Peso | O que avalia |
|----------|------|--------------|
| Loop de execução | 30% | Ferramentas persistentes, feedback ao modelo, retry |
| Conectividade MCP | 25% | Facilidade de registrar servidores de dados |
| Skills | 20% | Suporte a procedimentos empacotados sob demanda |
| Worktrees | 15% | Isolamento nativo de território de execução |
| Custo/contexto | 10% | Eficiência de tokens por operação |

A matriz vira score — e o score vira decisão:

```python
def avaliar_harness(criterios: dict) -> dict:
    pesos = {"loop": 0.30, "mcp": 0.25, "skills": 0.20,
             "worktrees": 0.15, "custo": 0.10}
    total = sum(criterios.get(k, 0) * pesos[k] for k in pesos)
    return {"score": round(total, 2), "veredito": "adotar" if total >= 0.7 else "avaliar mais"}


HARNESS_A = avaliar_harness({"loop": 0.9, "mcp": 0.8, "skills": 0.9,
                             "worktrees": 0.7, "custo": 0.6})
HARNESS_B = avaliar_harness({"loop": 0.6, "mcp": 0.5, "skills": 0.4,
                             "worktrees": 0.3, "custo": 0.8})
print(f"Harness A: {HARNESS_A}")
print(f"Harness B: {HARNESS_B}")
```

A avaliação por critérios evita o erro clássico de escolher harness por moda ou por preço — o loop de execução pesa três vezes mais que o custo, porque é o coração do agente [26].

### O Benchmark de Motores como Rotina Contínua

O laboratório de motores não se monta uma vez — ele precisa de benchmark contínuo porque os motores mudam, os prompts mudam e o desempenho degrada. O script abaixo roda um conjunto fixo de tarefas contra cada motor e gera um placar comparativo:

```python
import json

TAREFAS_BENCHMARK = [
    {'id': 'T1', 'tipo': 'refatoracao', 'criticidade': 'media'},
    {'id': 'T2', 'tipo': 'testes', 'criticidade': 'alta'},
    {'id': 'T3', 'tipo': 'documentacao', 'criticidade': 'baixa'},
    {'id': 'T4', 'tipo': 'debug', 'criticidade': 'alta'},
]

def rodar_benchmark(motor, resultados):
    placar = {t['id']: resultados.get(motor, {}).get(t['id']) for t in TAREFAS_BENCHMARK}
    taxa = sum(1 for v in placar.values() if v == 'ok') / len(placar)
    return {'motor': motor, 'taxa_sucesso': taxa, 'por_tarefa': placar}

print(rodar_benchmark('motor-alpha', {'motor-alpha': {'T1': 'ok', 'T2': 'ok', 'T3': 'falha', 'T4': 'ok'}}))
```

O placar vira dado de governança: quando um motor novo entra no laboratório, ele é avaliado contra o mesmo benchmark — nada de comparar maçãs com laranjas. E quando a taxa de sucesso de um motor cai abaixo do limiar, o protocolo dispara: ou o prompt do contrato precisa de atualização, ou o motor saiu do padrão. O benchmark também protege contra a síndrome do novo brinquedo: a organização troca de motor por evidência, não por hype.

### O Protocolo de Registro de MCPs

Vamos montar o laboratório de motores do zero, em sequência operacional. O cenário: uma equipe de 5 engenheiros que quer começar o SDLC AI-first sem quebrar o que já funciona.

1. **Semana 1 — Harness**: escolher o harness, configurar o loop de execução (bash, edição, testes) e o MCP de filesystem com escopo de leitura.
2. **Semana 2 — Test-first**: adotar o teste vermelho antes do código em um fluxo piloto — a régua do build.
3. **Semana 3 — Worktrees**: configurar worktree por agente e o merge controlado.
4. **Semana 4 — Skill piloto**: empacotar o procedimento de revisão de spec como skill e registrar no manifesto.
5. **Semana 5 — Radar**: adicionar o revisor adversarial independente nos PRs dos agentes.

A sequência é deliberada: cada semana constrói sobre a anterior, e nenhum passo exige derrubar o processo existente. O laboratório nasce paralelo à operação — e a operação adota os motores quando eles provam valor [25].

### O Protocolo de Registro de MCPs

O acesso a dados via MCP precisa de protocolo — quem pode conectar a qual fonte, com qual escopo. O registro abaixo é o contrato de conectividade do ecossistema:

```yaml
mcp_registro:
  filesystem:
    escopo_leitura: [specs, contratos, dossie]
    escopo_escrita: []
    agentes_permitidos: [analista, arquiteto]
  banco_estado:
    escopo_leitura: [fase, artefatos, metricas]
    escopo_escrita: [transicao_fase]
    agentes_permitidos: [orquestrador]
  repositorio:
    escopo_leitura: [codigo, testes]
    escopo_escrita: [worktree_do_agente]
    agentes_permitidos: [agente-build, agente-revisor]
```

O registro de MCPs é o mapa de acesso da torre: cada ferramenta tem escopo de leitura e escrita declarado — e o agente que tenta ler além do escopo é bloqueado pelo harness. A conectividade vira governança, não burocracia [23].

### O Modelo de Decisão de Aquisição de Ferramentas

O laboratório acumula ferramentas com facilidade — e cada uma cobra manutenção em contexto e configuração. O modelo abaixo é o gate de aquisição: antes de instalar uma nova ferramenta, a equipe responde a cinco perguntas e o modelo devolve o veredito:

```python
def avaliar_ferramenta(nome, resolve_problema, substitutos, custo_contexto, curva_aprendizado):
    pontos = 0
    if resolve_problema:
        pontos += 3
    if not substitutos:
        pontos += 2
    if custo_contexto == 'baixo':
        pontos += 1
    if curva_aprendizado == 'curta':
        pontos += 1
    veredito = 'adquirir' if pontos >= 4 else 'avaliar' if pontos >= 2 else 'recusar'
    return {'ferramenta': nome, 'pontos': pontos, 'veredito': veredito}

print(avaliar_ferramenta('linter-ai', resolve_problema=True, substitutos=['ruff'], custo_contexto='alto', curva_aprendizado='longa'))
```

O modelo é um antídoto para o acúmulo: ferramenta que resolve problema real, sem substituto, com custo de contexto baixo e curva curta entra direto; ferramenta redundante ou pesada fica de fora. A regra não é proibitiva — é seletiva. O laboratório deve ter poucas ferramentas excelentes, não muitas ferramentas medíocres, porque cada ferramenta instalada cobra aluguel em todo prompt futuro.

### O Playbook de Diagnóstico de Motores

Quando o ecossistema falha, o Comandante diagnostica com método — não com tentativa e erro. O playbook abaixo é o roteiro de diagnóstico:

1. **Harness não executa?** Verifique o loop: ferramenta existe? Retorno chega ao modelo? Timeout?
2. **Skill não carrega?** Verifique o manifesto: o disparo bate com a fase? O arquivo existe?
3. **MCP não conecta?** Verifique o registro: escopo permite? Servidor está de pé? Autenticação?
4. **Merge conflita?** Verifique as worktrees: os agentes editaram o mesmo arquivo físico?
5. **Sessão estoura?** Verifique o orçamento: fase gastou além da alocação?

O playbook é o checklist do mecânico: cada sintoma mapeia uma causa provável e uma ação — o tempo de diagnóstico cai de horas para minutos [24].

### O Modelo de Inventário de Skills com Custos

O ecossistema de skills cresce sem controle se ninguém mede. O modelo abaixo mantém o inventário de skills com custo de ativação e frequência de uso — o que expõe as skills que ninguém usa:

```python
class InventarioDeSkills:
    def __init__(self):
        self.skills = {}

    def registrar(self, nome, custo_ativacao, categoria):
        self.skills[nome] = {'custo_ativacao': custo_ativacao, 'categoria': categoria, 'usos': 0}

    def usar(self, nome):
        if nome in self.skills:
            self.skills[nome]['usos'] += 1

    def custo_total(self):
        return sum(s['custo_ativacao'] * s['usos'] for s in self.skills.values())

    def obsoletas(self, limiar_usos=1):
        return {n: s for n, s in self.skills.items() if s['usos'] <= limiar_usos}

inv = InventarioDeSkills()
inv.registrar('redigir-spec', 200, 'documentacao')
inv.registrar('auditor-legado', 1500, 'analise')
inv.usar('redigir-spec')
print(inv.obsoletas())
print(inv.custo_total())
```

A skill de auditoria legado com custo de ativação de 1500 tokens e zero usos é um desperdício vivo: cada prompt que a carrega sem usá-la é custo puro. O inventário responde duas perguntas: quanto o ecossistema custa por sessão (custo_total) e quais skills merecem revisão ou aposentadoria (obsoletas). O ecossistema enxuto não é sobre quantidade — é sobre relação custo-uso de cada skill registrada.

### O Registro de Ativação de Skills

O manifesto declara o catálogo; o registro de ativação mede o uso. Cada carregamento de skill gera um evento — e o agregado desses eventos alimenta a governança do ecossistema:

```json
{
  "ativacoes": [
    {
      "timestamp": "2026-08-02T10:12:00Z",
      "skill": "revisor-espec",
      "fase": "spec",
      "artefato": "spec_autenticacao.json",
      "resultado": "aprovado",
      "tokens_gastos": 4200
    },
    {
      "timestamp": "2026-08-02T11:47:00Z",
      "skill": "revisor-espec",
      "fase": "spec",
      "artefato": "spec_pagamentos.json",
      "resultado": "reprovado",
      "tokens_gastos": 5100
    }
  ]
}
```

O registro responde perguntas que o manifesto não responde: qual skill é usada de verdade, qual falha com frequência, quanto custa cada ativação. É o contador de combustível da torre — a skill que custa caro e não entrega é candidata a revisão [21].

### O Test-First Como Régua do Harness

O harness só está configurado de verdade quando o test-first é a régua: o agente abre o build pelo teste vermelho. O fluxo operacional é inegociável:

1. **Escreva o teste** que define o comportamento esperado (vermelho).
2. **Rode o teste** e registre a saída — a evidência do vermelho.
3. **Delegue a implementação** ao agente, com o teste como contrato.
4. **Rode de novo** — o verde é a prova de conclusão.
5. **Registre o par** (teste, saída) como evidência do merge.

O trecho abaixo é o esqueleto do contrato test-first que o harness valida antes de aceitar um build como concluído:

```python
import subprocess
from pathlib import Path


def rodar_teste_com_contrato(teste: str, raiz: Path) -> dict:
    resultado = subprocess.run(
        ["python", "-m", "pytest", teste, "--quiet"],
        capture_output=True, text=True, cwd=str(raiz))
    return {
        "teste": teste,
        "exit_code": resultado.returncode,
        "saida": (resultado.stdout or resultado.stderr)[:200],
        "verde": resultado.returncode == 0,
    }


contrato = rodar_teste_com_contrato("testes/test_login.py", Path("."))
print(f"Teste {contrato['teste']}: {'VERDE' if contrato['verde'] else 'VERMELHO'}")
print(f"Saida: {contrato['saida']}")
```

O contrato é simples, mas muda o jogo: o agente não decide quando terminou — o teste decide [22].

### O Ciclo de Vida de uma Skill

Skills não são eternas — nascem, são usadas, são criticadas e evoluem (você verá esse ciclo no Capítulo 8). O ciclo de vida técnico segue o mesmo padrão do SDLC que as skills governam:

| Estágio | Ação | Evidência |
|---------|------|-----------|
| Nascimento | Procedimento capturado de um incidente ou prática | Registro de origem |
| Uso | Skill carregada sob demanda em fases correspondentes | Log de ativação |
| Crítica | Taxa de sucesso medida por fase | Métrica de desempenho |
| Evolução | Skill revisada quando a taxa cai | Nova versão com changelog |
| Aposentadoria | Skill substituída por MCP ou procedimento superior | Registro de descontinuação |

Cada skill no manifesto carrega essas métricas — a skill que falha três vezes seguidas vira insumo do debriefing, não dogma mantido [20].

### O Modelo de Custo Total do Laboratório

O laboratório tem custo recorrente — e o comandante precisa do número. O modelo abaixo soma os custos de motor, ferramentas e contexto por sessão:

```python
def custo_laboratorio(custo_motor_sessao, custo_ferramentas, tokens_por_sessao):
    custo_tokens = tokens_por_sessao / 1000 * 0.002
    total = custo_motor_sessao + custo_ferramentas + custo_tokens
    return {'motor': custo_motor_sessao, 'ferramentas': custo_ferramentas,
            'tokens': round(custo_tokens, 3), 'total_sessao': round(total, 3)}

print(custo_laboratorio(custo_motor_sessao=0.10, custo_ferramentas=0.02, tokens_por_sessao=50000))
```

O número total por sessão alimenta duas decisões: quanto o laboratório custa por entrega e se a automação realmente compensa. Quando o custo por sessão supera o custo do trabalho manual que substitui, o laboratório virou passatempo caro — e o benchmark de motores da seção anterior é o que aponta onde cortar. Medir o custo é a disciplina que mantém o laboratório uma ferramenta, não uma despesa.

### A Governança do Ecossistema

Quatro motores resolvem a execução, mas quem governa a combinação deles? A resposta é o contrato de delegação que você viu no Capítulo 2: cada motor tem um dono, uma régua e um ponto de auditoria. O harness é de quem opera a esteira; as skills são de quem mantém o procedimento; os MCPs são de quem administra o acesso a dados; as worktrees são de quem controla o merge [15]. Sem essa governança, o ecossistema vira caos de ferramentas — o problema que o MCP justamente veio resolver ao padronizar o acesso [16].

### O Radar do Ecossistema

A operação dos motores também precisa de observação. Métricas simples respondem se o ecossistema está saudável: taxa de sucesso por skill, latência por chamada MCP, conflitos por merge de worktree e tokens consumidos por sessão de harness [17]. Essas métricas alimentam o debriefing do Capítulo 8 — o motor que falha três vezes seguidas vira skill revisada, não dogma mantido [18].

### O Ecossistema em Números

Um laboratório de motores se avalia com números, não com opinião. Três indicadores mínimos: taxa de aprovação de código no CI (o harness está entregando sintaxe válida?), taxa de sucesso das skills (o procedimento empacotado está cumprindo o papel?) e conflitos por merge (as worktrees estão isolando de verdade?) [19]. Cada indicador alimenta o debriefing da Fase 8 — um motor que falha de forma consistente é candidato a skill revisada ou MCP substituído, nunca a costume mantido por inércia [20].

### O Protocolo de Entrada de Nova Ferramenta

Nenhuma ferramenta entra no laboratório sem protocolo. O protocolo tem cinco etapas fixas: demonstrar que resolve problema real, comparar com os substitutos existentes, medir o custo de contexto por sessão, testar em um projeto piloto de baixo risco e documentar o caso de uso no inventário. As cinco etapas são obrigatórias e nessa ordem — a demonstração antes da instalação evita o entusiasmo prematuro, e o piloto de baixo risco evita que a estreia da ferramenta aconteça na entrega crítica. O protocolo não atrasa a adoção de boas ferramentas; ele só filtra as que não se sustentam.

### Passos para Montar o Laboratório de Motores

1. **Escolha o harness** e configure o loop de execução (bash, edição, testes).
2. **Registre as ferramentas essenciais** como MCPs (filesystem, banco de estado).
3. **Empacote seus procedimentos em skills** — comece pelas duas de maior retorno: revisão de spec e verificação adversarial.
4. **Configure worktrees por agente** — um território por executante.
5. **Adote test-first como régua**: todo build começa pelo teste vermelho [12].

## 5. Aplica

Cena real, em segunda pessoa. Você lidera uma equipe de plataforma que decidiu delegar uma sprint inteira a agentes. A empolgação inicial vira caos na quarta-feira: dois agentes editam o mesmo arquivo de configuração e corrompem o build; o agente do front-end não encontra a API porque nenhum MCP conecta o harness ao serviço de documentação; e a revisão de código vira um gargalo porque o revisor humano precisa ler tudo sem ajuda.

O erro não foi usar agentes em paralelo. O erro foi montar os motores pela metade. Faltaram os quatro instrumentos do capítulo: worktrees (os agentes pisaram no mesmo território), MCPs (os agentes não tinham acesso aos dados), skills (cada agente improvisou seu procedimento de revisão) e a régua test-first (os agentes "terminaram" quando acharam que estava pronto, não quando os testes passaram).

O diagnóstico, ligado à teoria: motores faltantes viram conflito de execução. A correção prática:

1. **Pare a sprint e reconfigure**: uma worktree por agente, com branch própria e diretório próprio.
2. **Registre os MCPs de dados**: banco de estado, documentação, repositórios — o radar conectado.
3. **Empacote a skill de revisão** e a skill de build, e injete-as no contexto de cada agente.
4. **Exija teste vermelho antes de código**: o agente que não abre com teste não decola.

Armadilhas comuns: achar que harness é só o IDE (o harness é o loop, não a interface); registrar MCPs demais e transformar o contexto em colcha de retalhos (só o que a fase precisa); skills monolíticas que tentam cobrir tudo (skill especializada é skill que funciona); e worktrees sem merge controlado (isolamento sem integração é acúmulo de ilhas) [13].

## 6. Conclusão

Você ligou os motores. Três marcos: primeiro, o harness como loop de execução com feedback — a anatomia que transforma LLM em agente; segundo, as skills e MCPs como especialização e conectividade — procedimentos empacotados e dados sob demanda via protocolo padrão; terceiro, as worktrees como célula de contenção do build paralelo e o test-first como régua mensurável de conclusão.

Como desafio, configure uma worktree isolada para o seu próximo experimento agêntico e escreva o teste vermelho da feature antes de qualquer prompt ao agente.

No próximo capítulo, você aciona o radar: verificação adversarial e evidência — a camada que separa o SDLC AI-first de um caos com boa intenção [14].

## 7. Referências Bibliográficas

[1] ANTHROPIC. *Building effective agents.* Disponível em: https://www.anthropic.com/research/building-effective-agents. Acesso em: 02 ago. 2026.
[2] ANTHROPIC. *Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet.* Disponível em: https://www.anthropic.com/news/swe-bench-sonnet. Acesso em: 02 ago. 2026.
[3] JIN, Haolin et al. *From LLMs to LLM-based Agents for Software Engineering: A Survey of Current, Challenges and Future.* 2025. Disponível em: https://arxiv.org/abs/2408.02479. Acesso em: 02 ago. 2026.
[4] ANTHROPIC. *Introducing the Model Context Protocol.* Disponível em: https://www.anthropic.com/news/model-context-protocol. Acesso em: 02 ago. 2026.
[5] CHACON, Scott; STRAUB, Ben. *Pro Git.* 2. ed. Nova York: Apress, 2014. Disponível em: https://git-scm.com/book. Acesso em: 02 ago. 2026.
[6] BECK, Kent. *Test-Driven Development: By Example.* Boston: Addison-Wesley, 2002. Disponível em: https://www.informit.com. Acesso em: 02 ago. 2026.
[7] MOHAGHEGHI, Milad et al. *Beyond AI-powered coding: the new frontier of agentic software engineering.* 2025. Disponível em: https://arxiv.org/abs/2509.14838. Acesso em: 02 ago. 2026.
[8] ROYCHOUDHURY, Abhik et al. *Agentic Software Engineering: state and perspectives.* 2025. Disponível em: https://arxiv.org/abs/2509.09893. Acesso em: 02 ago. 2026.
[9] YANG, John et al. *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering.* NeurIPS 2024. Disponível em: https://arxiv.org/abs/2405.15793. Acesso em: 02 ago. 2026.
[10] CLARKE, Peter et al. *Model Context Protocol: overview e adoção.* 2025. Disponível em: https://arxiv.org/abs/2504.11423. Acesso em: 02 ago. 2026.
[11] GRÖPLER, Robin et al. *The Future of Generative AI in Software Engineering: A Vision from Industry and Academia in the European GENIUS Project.* IEEE/ACM AIware, 2025. Disponível em: https://arxiv.org/abs/2511.01348. Acesso em: 02 ago. 2026.
[12] HINGEL, Paula. *How AI Changes the SDLC: A Six-Stage Guide.* Augment Code, 2026. Disponível em: https://www.augmentcode.com/guides/how-ai-changes-the-sdlc. Acesso em: 02 ago. 2026.
[13] GURGUL, Vincent; GUBELA, Robin; LESSMANN, Stefan. *The State of Generative AI in Software Development: Insights from Literature and a Developer Survey.* 2026. Disponível em: https://arxiv.org/abs/2603.16975. Acesso em: 02 ago. 2026.
[14] MICROSOFT. *An AI led SDLC: Building an End-to-End Agentic Software Development Lifecycle with Azure and GitHub.* Microsoft Tech Community, 2026. Disponível em: https://techcommunity.microsoft.com/blog/appsonazureblog/an-ai-led-sdlc-building-an-end-to-end-agentic-software-development-lifecycle-wit/4491896. Acesso em: 02 ago. 2026.
[15] ROYCHOUDHURY, Abhik et al. *Agentic Software Engineering: state and perspectives.* 2025. Disponível em: https://arxiv.org/abs/2509.09893. Acesso em: 02 ago. 2026.
[16] CLARKE, Peter et al. *Model Context Protocol: overview e adoção.* 2025. Disponível em: https://arxiv.org/abs/2504.11423. Acesso em: 02 ago. 2026.
[17] HODA, Rashina. *Toward Agentic Software Engineering Beyond Code: Framing Vision, Values, and Vocabulary.* ICSE 2026 Workshop. Disponível em: https://arxiv.org/abs/2510.19692. Acesso em: 02 ago. 2026.
[18] JIN, Haolin et al. *From LLMs to LLM-based Agents for Software Engineering: A Survey of Current, Challenges and Future.* 2025. Disponível em: https://arxiv.org/abs/2408.02479. Acesso em: 02 ago. 2026.
[19] FORSGREN, Nicole; HUMBLE, Jez; KIM, Gene. *Accelerate: The Science of Lean Software and DevOps.* Portland: IT Revolution Press, 2018. Disponível em: https://itrevolution.com. Acesso em: 02 ago. 2026.
[20] GURGUL, Vincent; GUBELA, Robin; LESSMANN, Stefan. *The State of Generative AI in Software Development: Insights from Literature and a Developer Survey.* 2026. Disponível em: https://arxiv.org/abs/2603.16975. Acesso em: 02 ago. 2026.
[21] BECK, Kent. *Test-Driven Development: By Example.* Boston: Addison-Wesley, 2002. Disponível em: https://www.informit.com. Acesso em: 02 ago. 2026.
[22] HODA, Rashina. *Toward Agentic Software Engineering Beyond Code: Framing Vision, Values, and Vocabulary.* ICSE 2026 Workshop. Disponível em: https://arxiv.org/abs/2510.19692. Acesso em: 02 ago. 2026.
[23] CLARKE, Peter et al. *Model Context Protocol: overview e adoção.* 2025. Disponível em: https://arxiv.org/abs/2504.11423. Acesso em: 02 ago. 2026.
[24] GRÖPLER, Robin et al. *The Future of Generative AI in Software Engineering: A Vision from Industry and Academia in the European GENIUS Project.* IEEE/ACM AIware, 2025. Disponível em: https://arxiv.org/abs/2511.01348. Acesso em: 02 ago. 2026.
[25] ROYCHOUDHURY, Abhik et al. *Agentic Software Engineering: state and perspectives.* 2025. Disponível em: https://arxiv.org/abs/2509.09893. Acesso em: 02 ago. 2026.
[26] YANG, John et al. *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering.* NeurIPS 2024. Disponível em: https://arxiv.org/abs/2405.15793. Acesso em: 02 ago. 2026.
[27] CHACON, Scott; STRAUB, Ben. *Pro Git.* 2. ed. Nova York: Apress, 2014. Disponível em: https://git-scm.com/book. Acesso em: 02 ago. 2026.
