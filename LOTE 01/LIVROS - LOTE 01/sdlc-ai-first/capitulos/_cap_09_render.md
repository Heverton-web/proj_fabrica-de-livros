# Capítulo 9: Combustível: Economia de Tokens e Custo de Contexto

## 1. Introdução

No Capítulo 8, você fez o debriefing do voo e aprendeu a transformar incidentes em skill, teste canônico e spec revisada. Agora você entra na Parte V — e na disciplina que decide se o voo chega ao destino: o combustível. Tokens são o recurso escasso do SDLC AI-first, e a economia de contexto é a engenharia que mantém o ciclo vivo dentro dos limites de uma sessão.

Este capítulo ensina a tratar tokens, rate limits e custo de contexto como variáveis de projeto: medir o consumo, comprimir o que é ruído, delegar a subagentes enxutos e projetar handoffs que estendem a vida útil do ciclo. Você vai sair com um orçamento de contexto — e os instrumentos para não estourá-lo.

## 2. Explica

Um token é a unidade básica que um modelo de linguagem processa — aproximadamente uma sílaba de uma palavra em português, uma fração de palavra em inglês. Cada interação com um agente consome tokens de entrada (o contexto que você envia) e de saída (a resposta que ele produz). Quando a conversa cresce, o contexto cresce junto — e o custo de cada turno seguinte também [1].

O rate limit é a parede dura: cada provedor impõe um teto de tokens por minuto e por dia. Quando a sessão do agente estoura o teto, a execução trava — e o trabalho em andamento fica órfão. No SDLC AI-first, o rate limit não é um problema de infraestrutura; é uma **restrição de design do ciclo de vida**: cada fase deve caber no orçamento de contexto disponível [2].

A janela de contexto é o espaço da sessão: quantos tokens o modelo "lembra" em uma conversa. Sessões longas degeneram de duas formas: o contexto enche (e o agente esquece o início) ou o custo explode (cada turno reprocessa todo o histórico). A economia de contexto é a engenharia que evita as duas — mantendo a sessão magra e o histórico no lugar certo [3].

A primeira técnica é a **seleção cirúrgica**: carregar no contexto apenas o que a fase precisa. Antes de ler um arquivo, busque (grep) o que procura; antes de injetar um relatório, injete o resumo; antes de dar o código inteiro ao agente, dê a interface. O princípio é o mesmo do lean manufacturing: nada de estoque (contexto) parado [4].

A segunda técnica é a **compressão de logs**: saídas de comando com mais de algumas linhas são reduzidas a um resumo representativo — cabeçalho e rodapé — preservando o sinal e descartando o ruído. Logs de build, testes e infraestrutura são os maiores consumidores silenciosos de contexto; comprimi-los é a maior economia imediata [5].

A terceira técnica é a **comunicação telegráfica entre agentes**: subagentes se reportam ao orquestrador com resumos compactos, não com transcrições. A delegação caveman — instruções mínimas, relatórios mínimos — reduz o contexto em uma ordem de grandeza quando há muitos subagentes em paralelo [6].

A quarta técnica é o **handoff**: quando a sessão está perto do limite, o trabalho é compactado em um documento de transferência — contexto, decisões, pendências — e um novo agente/sessão continua de onde parou. O handoff transforma o limite da janela de contexto de uma fatalidade em uma transição de projeto [7].

Por fim, a quinta técnica é o **subagente enxuto**: tarefas de busca e edição extensa são delegadas a subagentes que retornam apenas o resultado, não o processo. O orquestrador nunca vê os bastidores — economizando dezenas de milhares de tokens por delegação [8].

## 3. Ilustra

Um voo comercial calcula combustível com precisão cirúrgica: o combustível necessário para a rota, mais a reserva legal, mais o alternate. Nenhum piloto enche o tanque "só por garantia" — excesso de peso custa caro. E nenhum piloto decola com combustível de menos — o alternate existe para o caso de desvio.

O contexto é o combustível do voo agêntico. O necessário para a rota é o contexto mínimo da fase. A reserva é a margem para correções inesperadas. E o alternate é o handoff — o plano de desvio quando a sessão não alcança o destino.

![Orçamento de contexto de uma sessão agêntica](../imagens/diagramas/dia_09_01_7e34661b7f.png)

Como Comandante de Operações de Software, você adota a régua do combustível: carregar o necessário, reservar a margem e sempre ter o alternate desenhado [9].

## 4. Técnica

### Medindo o Consumo de Contexto

Nada de economia sem medição. O instrumento abaixo estima o custo de uma sessão com base em tokens e preço:

```python
from dataclasses import dataclass


@dataclass
class OrcamentoSessao:
    nome: str
    tokens_entrada: int = 0
    tokens_saida: int = 0

    def registrar(self, entrada: int, saida: int) -> None:
        self.tokens_entrada += entrada
        self.tokens_saida += saida

    def custo_estimado(self, preco_entrada_por_milhao: float = 0.25,
                       preco_saida_por_milhao: float = 1.25) -> float:
        custo_entrada = self.tokens_entrada / 1_000_000 * preco_entrada_por_milhao
        custo_saida = self.tokens_saida / 1_000_000 * preco_saida_por_milhao
        return round(custo_entrada + custo_saida, 4)

    def resumo(self) -> str:
        return (f"{self.nome}: {self.tokens_entrada + self.tokens_saida} tokens "
                f"(entrada={self.tokens_entrada}, saida={self.tokens_saida}) "
                f"custo=US$ {self.custo_estimado()}")


sessao = OrcamentoSessao("build-pagamentos")
sessao.registrar(entrada=48_000, saida=6_500)
print(sessao.resumo())
```

A métrica por fase alimenta a Fase 8 (Evoluir): a spec que consumiu 48 mil tokens de entrada pode ser redigida com um contexto mais enxuto na próxima iteração [10].

### Seleção Cirúrgica: Grep Antes de Read

A técnica mais barata é não carregar o que não precisa. O padrão operacional:

```bash
# EM VEZ DE: ler o arquivo inteiro (muitos tokens)
# FAÇA: buscar primeiro o que procura
grep -n "ProvedorPagamento" src/pagamentos/ -r | head -20

# EM VEZ DE: abrir o relatorio completo no contexto
# FAÇA: extrair apenas o resumo
python - <<'PY'
import json
with open("output/livros/sdlc-ai-first/revisao/relatorio_auditoria.json",
          encoding="utf-8") as f:
    relatorio = json.load(f)
for r in relatorio["requisitos"]:
    status = "OK" if r["conforme"] else "FALHA"
    print(f"[{status}] {r['id']} {r['nome']}")
PY
```

O padrão grep-antes-de-read reduz o contexto de arquivos grandes em uma ordem de grandeza — e é a técnica com melhor retorno por esforço [4].

### Compressão de Logs

Logs de build e teste são os maiores ruídos. A compressão 3+4 preserva o sinal:

```python
def comprimir_log(saida: str, cabeca: int = 3, cauda: int = 4) -> str:
    """Comprime log longo preservando inicio e fim (onde estao o resumo e o erro)."""
    linhas = [l for l in saida.splitlines() if l.strip()]
    if len(linhas) <= cabeca + cauda + 2:
        return saida
    return "\n".join(
        linhas[:cabeca] + [f"... ({len(linhas) - cabeca - cauda} linhas omitidas)"] + linhas[-cauda:]
    )


LOG_GRANDE = "\n".join(f"linha {i}" for i in range(1, 60))
print(comprimir_log(LOG_GRANDE))
```

O resultado: 59 linhas viram 9 — o sinal (início e erro no fim) preservado, o ruído descartado [5].

### Handoff: O Alternate da Sessão

Quando a sessão aproxima o limite, o handoff compacta o estado:

```markdown
# Handoff: build-pagamentos (sessao 3)

## Estado
- Spec aprovada (v2.1); interfaces definidas (contrato/interface.ts).
- Cap 3 e 4 concluidos; build em andamento no modulo de pagamentos.
- Evidencia: 4 testes verdes, 0 falhas; CI rodando.

## Decisoes
- Fatura versionada (ADR-007); nao atualizar in-place.
- Cupom nao acumulativo (spec R12).

## Pendencias
- Implementar estorno com idempotencia (ticket T7).
- Revisar cobertura do caso de borda fatura-duplicada.

## Instrucoes para o proximo agente
1. Retomar do ticket T7.
2. Consultar a skill verificar-cupons-nao-acumulativos antes de tocar em descontos.
3. Manter o mesmo vocabulario ubiquo (cliente, fatura, reembolso).
```

O handoff é o alternate: o voo desvia, mas não cai — a sessão nova decola do ponto exato [7].

### O Buffer de Rate Limit como Design

O rate limit diário é uma restrição de capacidade — como o tanque de combustível do avião. O design da esteira deve declarar o orçamento diário e distribuí-lo entre as fases, com buffer de emergência:

```json
{
  "orcamento_diario_tokens": 900000,
  "alocacao": {
    "pesquisa": 50000,
    "spec": 60000,
    "design": 40000,
    "build": 500000,
    "verificar": 100000,
    "derivados": 100000
  },
  "buffer_emergencia": 50000,
  "regras": [
    "fase excede alocacao -> interromper e handoff",
    "buffer de emergencia so com autorizacao humana",
    "rate limit atingido -> pausar com backoff, nunca abortar"
  ]
}
```

O orçamento declarado transforma o rate limit de fatalidade em projeto: a esteira sabe, antes de começar, quantos tokens cada fase pode gastar — e onde parar com dignidade, em vez de morrer no meio [18].

### O Modelo de Orçamento por Fase com Teto

O orçamento de contexto não é global — ele é distribuído por fase, com teto para cada uma. O modelo abaixo aloca o orçamento e recusa novas tarefas quando a fase estoura o teto:

```python
class OrcamentoPorFase:
    def __init__(self, tetos):
        self.tetos = tetos
        self.gastos = {f: 0 for f in tetos}

    def gastar(self, fase, tokens):
        if self.gastos[fase] + tokens > self.tetos[fase]:
            return {'permitido': False, 'teto': self.tetos[fase], 'gasto': self.gastos[fase]}
        self.gastos[fase] += tokens
        return {'permitido': True, 'restante': self.tetos[fase] - self.gastos[fase]}

    def relatorio(self):
        return {f: {'gasto': g, 'teto': self.tetos[f], 'uso': round(g / self.tetos[f], 2)} for f, g in self.gastos.items()}

orcamento = OrcamentoPorFase({'redacao': 120000, 'revisao': 40000, 'compilacao': 20000})
print(orcamento.gastar('redacao', 50000))
print(orcamento.gastar('redacao', 90000))
print(orcamento.relatorio())
```

O teto por fase impede o efeito dominó: se a redação estoura, a revisão e a compilação sofrem por tabela — mesmo que tenham orçamento próprio intacto. Quando o gastar() devolve permitido=False, o agente não improvisa: ele faz o handoff para a fase de corte com o relatório de consumo, e a priorização decide o que o contexto segura.

### O Custo do Contexto como Decisão de Fronteira

Nem todo contexto precisa ser reprocessado. O cache de contexto — resultados de fases anteriores reutilizados sem recarregar — é a técnica mais subestimada do AI-first:

```python
import hashlib
import json
from pathlib import Path
from typing import Optional


class CacheContexto:
    def __init__(self, raiz: Path) -> None:
        self.raiz = raiz
        self.raiz.mkdir(parents=True, exist_ok=True)

    def _chave(self, conteudo: str) -> str:
        return hashlib.sha256(conteudo.encode("utf-8")).hexdigest()[:16]

    def obter(self, conteudo: str) -> Optional[dict]:
        arquivo = self.raiz / f"{self._chave(conteudo)}.json"
        if arquivo.exists():
            return json.loads(arquivo.read_text(encoding="utf-8"))
        return None

    def gravar(self, conteudo: str, resultado: dict) -> None:
        arquivo = self.raiz / f"{self._chave(conteudo)}.json"
        arquivo.write_text(json.dumps(resultado, ensure_ascii=False),
                           encoding="utf-8")


cache = CacheContexto(Path(".cache_ctx"))
cache.gravar("spec-pagamentos-v2", {"resumo": "12 requisitos, 6 bordas", "tokens": 18400})
recuperado = cache.obter("spec-pagamentos-v2")
print(f"Cache hit: {recuperado}")
```

O cache é o reservatório da torre: o que já foi processado não é reprocessado — economizando os tokens que seriam gastos recalculando o mesmo resultado [19].

### O Custo do Contexto como Decisão de Fronteira

A economia de contexto também intersecta a cartografia do Capítulo 4: fronteiras bem desenhadas são a forma estrutural de economizar tokens [14]. Quando cada módulo expõe uma interface pequena, o agente que o consome carrega apenas a interface — não o módulo inteiro. A economia não é só tática (comprimir logs); é arquitetural (não precisar carregar o que não importa). O Comandante de Operações de Software desenha fronteiras pensando no combustível desde o design [15].

### A Contabilidade da Sessão

A disciplina do combustível exige contabilidade: cada sessão registra entrada, saída e o que ficou de fora. O orçamento de contexto de uma fase não é só o teto de tokens — é a lista explícita do que a fase **não** carrega [16]. Essa contabilidade vira insumo do debriefing do Capítulo 8: a sessão que gastou 50 mil tokens em contexto desnecessário é uma falha de processo, não de infraestrutura [17].

### O Modelo de Compressão Seletiva de Arquivos

Nem todo arquivo merece entrar inteiro no contexto. O modelo abaixo decide, por tipo de arquivo e fase, se o conteúdo entra integral, resumido ou nem entra:

```python
REGRAS_DE_COMPRESSAO = {
    'codigo_fonte': {'redacao': 'resumido', 'revisao': 'integral', 'compilacao': 'integral'},
    'json_estado': {'redacao': 'nao_entra', 'revisao': 'integral', 'compilacao': 'resumido'},
    'logs': {'redacao': 'nao_entra', 'revisao': 'cabecalho', 'compilacao': 'nao_entra'},
    'dossies': {'redacao': 'integral', 'revisao': 'resumido', 'compilacao': 'nao_entra'},
}

def decidir_leitura(tipo, fase):
    regra = REGRAS_DE_COMPRESSAO.get(tipo, {}).get(fase, 'resumido')
    return {'tipo': tipo, 'fase': fase, 'modo': regra}

for tipo in ['codigo_fonte', 'json_estado', 'logs', 'dossies']:
    print(decidir_leitura(tipo, 'redacao'))
```

A tabela materializa a seleção cirúrgica: na fase de redação, o dossiê entra integral (é a fonte das citações), o código entra resumido (só as assinaturas) e o log não entra (é barulho). Na fase de revisão, o código e o JSON de estado entram integrais porque é quando se verifica. A regra por fase é o que impede o agente de re-ler tudo a cada passo — o contexto é um recurso finito e cada leitura tem custo.

### O Exemplo Prático: Refatoração com Orçamento de Contexto

Vamos aplicar a economia de contexto em um caso real: refatorar um módulo legado de 40 mil linhas. A tentação é carregar tudo no contexto; a disciplina é carregar o mínimo. O plano de voo de contexto:

1. **Varredura por subagente enxuto**: um subagente mapeia o módulo (arquivos, dependências, funções públicas) e retorna apenas o mapa — nunca o código inteiro.
2. **Interface primeiro**: o agente de refatoração recebe as interfaces e os ADRs do módulo, não a implementação.
3. **RAG local**: consultas ao dossiê/índice retornam blocos específicos, nunca o arquivo inteiro.
4. **Handoff pré-desenhado**: o documento de transferência existe antes de a sessão começar.
5. **Monitor em tempo real**: o consumo por fase é exibido; ao cruzar 70% do teto, a sessão comprime.

O cálculo abaixo compara as duas abordagens:

```python
def comparar_abordagens(linhas_modulo: int, tokens_por_linha: float = 1.3) -> None:
    carga_integral = linhas_modulo * tokens_por_linha
    carga_cirurgica = carga_integral * 0.15  # interface + mapa + RAG
    economia = carga_integral - carga_cirurgica
    print(f"Carga integral : {carga_integral:,.0f} tokens".replace(",", "."))
    print(f"Carga cirurgica: {carga_cirurgica:,.0f} tokens".replace(",", "."))
    print(f"Economia       : {economia:,.0f} tokens ({economia/carga_integral*100:.0f}%)".replace(",", "."))


comparar_abordagens(linhas_modulo=40_000)
```

A economia de 85% não é mágica — é seleção cirúrgica aplicada: o agente só vê o que precisa para decidir, e o resto fica no repositório, não no contexto [23].

### O Alarme de Contexto no Ponto Certo

O alarme de contexto só ajuda se dispara no momento de decidir, não no momento do desastre. O ponto certo é antes da próxima ação cara: o alarme toca quando uma leitura grande está prestes a acontecer, quando uma nova busca vai começar ou quando a delegação vai ser disparada com o contexto cheio. Alarme que dispara no meio da ação inútil é ruído; alarme que dispara antes da decisão é conselho. O ajuste fino do ponto de disparo é feito com o histórico do monitor — o mesmo dado que mede o consumo ensina onde avisar.

### O Perfil de Consumo por Tipo de Fase

Nem toda fase consome o mesmo perfil de contexto. O Comandante conhece o perfil de cada fase para calibrar o orçamento:

| Fase | Perfil dominante | Estratégia de economia |
|------|------------------|------------------------|
| Pesquisa | Muitos tokens de entrada (fontes) | RAG local: busca por bloco, nunca o dossiê inteiro |
| Spec | Entrada média, escrita densa | Templates e glossário no contexto; nada de histórico |
| Build | Entrada e saída altas | Grep antes de read; interface em vez de implementação |
| Verificar | Entrada média (diffs) | Parecer estruturado; nunca o arquivo inteiro |
| Derivados | Entrada alta (obra-mãe) | Reaproveitar dossiê e sumário; nunca re-pesquisar |

O perfil por fase transforma a economia de contexto de intuição em engenharia: cada fase sabe, antes de começar, onde o combustível será gasto — e onde cortar sem perder sinal [20].

### O Modelo de Priorização do Corte de Contexto

Quando o orçamento aperta, o Comandante corta com método — não por intuição. O modelo abaixo prioriza o que comprimir:

| Prioridade | O que cortar | Exemplo | Impacto no sinal |
|------------|-------------|---------|------------------|
| 1 | Logs de build e teste | Saída do pytest | Nenhum (sinal no fim) |
| 2 | Histórico de iteração | Versões antigas de diffs | Nenhum (estado no handoff) |
| 3 | Implementação de módulos | Corpo do código | Baixo (interface basta) |
| 4 | Relatórios intermediários | Dossiês completos | Médio (resumo basta) |
| 5 | Conteúdo de domínio | Prosa da spec | **Nunca cortar** |

A prioridade 5 é a regra de ouro do capítulo: o conteúdo de domínio — a prosa que carrega decisão — nunca é comprimido. O corte disciplinado preserva o sinal e elimina o ruído, exatamente na ordem que o modelo define [26].

### O Modelo de Custo por Fase ao Longo do Ciclo

O custo de contexto não é uniforme ao longo do ciclo — e o Comandante conhece a curva para alocar combustível. O modelo abaixo projeta o custo por fase com base no perfil de consumo:

```python
def custo_por_fase(tokens_por_fase: dict, precos: dict = None) -> dict:
    precos = precos or {"entrada": 0.25, "saida": 1.25}
    custo = {}
    for fase, tokens in tokens_por_fase.items():
        entrada = tokens["entrada"] / 1_000_000 * precos["entrada"]
        saida = tokens["saida"] / 1_000_000 * precos["saida"]
        custo[fase] = round(entrada + saida, 3)
    return custo


TOKENS = {
    "pesquisa": {"entrada": 120_000, "saida": 15_000},
    "spec": {"entrada": 30_000, "saida": 10_000},
    "build": {"entrada": 400_000, "saida": 90_000},
    "verificar": {"entrada": 50_000, "saida": 12_000},
}

for fase, custo in custo_por_fase(TOKENS).items():
    print(f"{fase}: US$ {custo}")
```

A curva de custo revela onde a economia rende mais: o build domina o orçamento — e é lá que a seleção cirúrgica e o test-first pagam o maior dividendo. O Comandante aloca disciplina onde o custo é maior, não onde é mais visível [25].

### O Modelo de Custo de Leitura por Tipo de Arquivo

O custo de contexto se esconde nas leituras — e nem toda leitura custa o mesmo. O modelo abaixo estima o custo de ler cada tipo de arquivo, para que a decisão de leitura seja financeira:

```python
CUSTO_POR_TIPO = {
    'codigo_fonte': 0.9,   # tokens por caractere
    'json_estado': 1.2,
    'markdown': 0.8,
    'log': 1.5,
    'binario': 3.0,
}

def custo_leitura(caminho, tipo, tamanho_chars):
    fator = CUSTO_POR_TIPO.get(tipo, 1.0)
    custo = int(tamanho_chars * fator)
    return {'caminho': caminho, 'tipo': tipo, 'custo_estimado_tokens': custo}

print(custo_leitura('output/relatorio.json', 'json_estado', 8000))
print(custo_leitura('logs/debug.txt', 'log', 8000))
```

O mesmo tamanho, dois custos diferentes: o JSON de estado com formato denso custa 9.600 tokens; o log, 12.000. Quando o agente decide entre "ler o log inteiro" e "ler só o cabeçalho", o número torna a decisão óbvia — e a regra de compressão da seção anterior (log entra como cabeçalho na revisão) deixa de parecer arbitrária. Estimar custo antes de ler é o hábito que mantém a sessão dentro do orçamento.

### O Relatório de Consumo por Fase

Vamos ver o handoff funcionando em um caso real. A sessão do build de pagamentos está em 85% do orçamento — e o handoff, desenhado na decolagem, entra em ação:

1. **Sinal de alerta**: o monitor cruza 70% do teto.
2. **Compressão**: a sessão comprime o que resta — contexto mínimo, apenas o essencial.
3. **Decisão de handoff**: ao cruzar 90%, o estado é compactado no documento de transferência.
4. **Nova sessão**: retoma do ticket pendente, com o handoff como contexto inicial.
5. **Registro**: o consumo das duas sessões é somado no relatório da fase.

O documento de transferência já apareceu no Capítulo 5 — aqui você vê o momento exato de usá-lo. O handoff não é falha da sessão; é o alternate planejado, o aeroporto reserva para o desvio [24].

### O Relatório de Consumo por Fase

O orçamento de contexto só funciona com retrospectiva. O relatório de consumo por fase compara o alocado com o gasto — e alimenta a calibração do próximo ciclo:

```json
{
  "ciclo": "C-2026-04",
  "consumo_por_fase": [
    {"fase": "pesquisa", "alocado": 50000, "gasto": 62000, "desvio_pct": 24},
    {"fase": "spec", "alocado": 60000, "gasto": 41000, "desvio_pct": -32},
    {"fase": "build", "alocado": 500000, "gasto": 540000, "desvio_pct": 8},
    {"fase": "verificar", "alocado": 100000, "gasto": 88000, "desvio_pct": -12}
  ],
  "maior_consumidor": "build"
}
```

O relatório é o painel de combustível retrospectivo: a pesquisa estourou 24% (dossiê inteiro no contexto em vez de RAG), o build estourou 8% (grep-antes-de-read negligenciado). A calibração do próximo ciclo parte desses números — não da intuição [22].

### O Modelo de Threshold de Estouro com Ações

O monitor de sessão precisa reagir quando o estouro acontece — e a reação deve ser graduada. O modelo abaixo aplica ações progressivas conforme o consumo sobe:

```python
LIMIARES = [
    (0.6, 'compactar_logs'),
    (0.75, 'encerrar_tarefas_paralelas'),
    (0.85, 'congelar_buscas'),
    (0.95, 'emitir_handoff_urgente'),
]

def acao_no_limiar(uso_pct):
    acao = 'continuar'
    for limiar, a in LIMIARES:
        if uso_pct >= limiar:
            acao = a
    return {'uso_pct': uso_pct, 'acao': acao}

for uso in [0.5, 0.65, 0.8, 0.9, 0.97]:
    print(acao_no_limiar(uso))
```

As ações progressivas evitam o salto do nada para o pânico: aos 60% compacta-se os logs; aos 75% encerra-se o trabalho paralelo; aos 85% congela-se as buscas; aos 95% dispara-se o handoff urgente. Cada degrau é reversível — o trabalho retomado quando o uso cai — exceto o último, que é o momento de salvar a sessão. O monitor vira não apenas medidor, mas piloto automático de sobrevivência da sessão.

### O Monitor de Sessão em Tempo Real

O orçamento precisa de um medidor em tempo real — a esteira exibe o consumo corrente e o teto de cada fase. O código abaixo é o monitor mínimo:

```python
import time
from dataclasses import dataclass, field


@dataclass
class MonitorSessao:
    fase: str
    teto: int
    consumo: int = 0
    inicio: float = field(default_factory=time.time)

    def gastar(self, tokens: int) -> None:
        self.consumo += tokens
        pct = self.consumo / self.teto * 100
        status = "OK" if pct < 70 else ("ATENCAO" if pct < 90 else "CRITICO")
        print(f"[{status}] fase={self.fase} consumo={self.consumo}/{self.teto} "
              f"({pct:.0f}%)")


monitor = MonitorSessao("build-pagamentos", teto=60_000)
monitor.gastar(18_000)
monitor.gastar(24_000)
monitor.gastar(20_000)
```

O monitor é o indicador de combustível da cabine: quando o consumo cruza 70%, a tripulação muda de comportamento — comprime, simplifica ou prepara o handoff. Nunca descobre o estouro depois [21].

### O Modelo de Decisão entre Ler e Delegar

Economizar contexto tem limite: às vezes ler o arquivo inteiro é mais barato que delegar a tarefa. O modelo abaixo compara o custo das duas estratégias:

```python
def decidir_leitura_vs_delegacao(tamanho_arquivo, custo_delegacao, complexidade):
    custo_leitura = tamanho_arquivo * 0.001  # custo unitario por caractere
    if complexidade == 'alta':
        custo_delegacao *= 2
    return {'ler': round(custo_leitura, 2), 'delegar': round(custo_delegacao, 2),
            'melhor': 'ler' if custo_leitura < custo_delegacao else 'delegar'}

print(decidir_leitura_vs_delegacao(2000, 3.0, 'baixa'))
print(decidir_leitura_vs_delegacao(20000, 3.0, 'alta'))
```

O modelo explicita a troca: arquivo pequeno e tarefa simples, ler é mais barato que delegar — o overhead da delegação não compensa. Arquivo grande e tarefa complexa, delegar vence, porque a tarefa em si consome mais contexto que o custo de orquestração. A economia de contexto não é dogma — é otimização, e otimização começa e termina na comparação de custos.

### Quando a Economia é Contraproducente

A economia de contexto tem limite: comprimir conteúdo de negócio para economizar tokens destrói o valor que o conteúdo carrega [18]. A régua é clara — comprima ruído técnico (logs, outputs de build, repetições), nunca a prosa do domínio (spec, requisitos, decisões de arquitetura). O Comandante distingue o que é sinal do que é ruído antes de comprimir: a regra de ouro da economia de contexto é não economizar no que você precisa ler para decidir [19].

### O Hábito do Custo Antes da Ação

O orçamento de contexto só funciona se o hábito estiver instalado: antes de qualquer leitura, estimar o custo; antes de qualquer busca, formular o alvo; antes de delegar, comparar com o custo de fazer direto. O hábito não é natural — é treinado com o monitor de sessão mostrando o consumo em tempo real. Nas primeiras semanas o time olha o medidor com culpa; depois de um mês, a estimativa de custo precede a ação sem esforço. Economia de contexto é um músculo, não uma regra.

### Passos para Implantar o Orçamento de Contexto

1. **Meça** o consumo por fase em todas as sessões.
2. **Aplique grep-antes-de-read** em arquivos grandes.
3. **Comprima logs** com o padrão 3+4.
4. **Use subagentes enxutos** para busca e edição extensa.
5. **Desenhe o handoff** antes de cada sessão longa [11].

## 5. Aplica

Cena real, em segunda pessoa. Sua equipe delegou a um agente a refatoração de um módulo legado de 40 mil linhas. Na sessão 1, o agente carrega o arquivo inteiro, os relatórios inteiros e os logs inteiros no contexto. Na sessão 3, o contexto estoura no meio da refatoração — e o agente perde o fio. O time recomeça do zero, com um agente novo, e o ciclo se repete três vezes antes de alguém perguntar por quê.

O erro não foi o tamanho do módulo. O erro foi a ausência de orçamento de contexto. Cada sessão gastou o combustível inteiro no primeiro trecho do voo, sem reserva e sem alternate. O handoff — o documento que salvaria o estado entre sessões — nunca foi escrito porque ninguém planejou a possibilidade de estouro.

O diagnóstico, ligado à teoria: sessão sem orçamento é voo sem cálculo de combustível. A correção prática:

1. **Meça antes de delegar**: estime o contexto do módulo (arquivos, relatórios, logs) antes da sessão 1.
2. **Carregue cirurgicamente**: interface em vez de implementação, resumo em vez de relatório, grep antes de read.
3. **Desenhe o handoff na decolagem**: o documento de transferência existe antes da sessão começar, não quando ela estoura.
4. **Delegue o pesado a subagentes enxutos**: a varredura do módulo legado é trabalho de subagente que retorna só o mapa — não o território inteiro.

Armadilhas comuns: achar que contexto é ilimitado porque a janela cresce (o custo cresce junto); comprimir conteúdo de negócio em vez de log (comprima ruído técnico, nunca a prosa do domínio); e tratar o rate limit como "problema de provedor" (é problema de design do ciclo) [12].

## 6. Conclusão

Você dominou o combustível. Três marcos: primeiro, tokens e rate limits como variáveis de projeto — cada fase cabe no orçamento ou não decola; segundo, as técnicas de economia — seleção cirúrgica, compressão de logs, comunicação telegráfica e subagentes enxutos; terceiro, o handoff como alternate — o estado compactado que estende a vida útil da sessão em vez de deixá-la morrer.

Como desafio, registre o consumo de contexto da próxima sessão do seu time, fase a fase, e identifique os três maiores consumidores silenciosos. Corte-os e meça de novo.

No último capítulo, você sobe ao posto definitivo: maturidade, riscos e o futuro do SDLC AI-first — o que separa o Comandante do passageiro [13].

## 7. Referências Bibliográficas

[1] ANTHROPIC. *Building effective agents.* Disponível em: https://www.anthropic.com/research/building-effective-agents. Acesso em: 02 ago. 2026.
[2] GRÖPLER, Robin et al. *The Future of Generative AI in Software Engineering: A Vision from Industry and Academia in the European GENIUS Project.* IEEE/ACM AIware, 2025. Disponível em: https://arxiv.org/abs/2511.01348. Acesso em: 02 ago. 2026.
[3] JIN, Haolin et al. *From LLMs to LLM-based Agents for Software Engineering: A Survey of Current, Challenges and Future.* 2025. Disponível em: https://arxiv.org/abs/2408.02479. Acesso em: 02 ago. 2026.
[4] WANG, Yuchen; GUO, Shangxin; TAN, Chee Wei. *From Code Generation to Software Testing: AI Copilot with Context-Based RAG.* 2025. Disponível em: https://arxiv.org/abs/2504.01866. Acesso em: 02 ago. 2026.
[5] MOHAGHEGHI, Milad et al. *Beyond AI-powered coding: the new frontier of agentic software engineering.* 2025. Disponível em: https://arxiv.org/abs/2509.14838. Acesso em: 02 ago. 2026.
[6] GURGUL, Vincent; GUBELA, Robin; LESSMANN, Stefan. *The State of Generative AI in Software Development: Insights from Literature and a Developer Survey.* 2026. Disponível em: https://arxiv.org/abs/2603.16975. Acesso em: 02 ago. 2026.
[7] ROYCHOUDHURY, Abhik et al. *Agentic Software Engineering: state and perspectives.* 2025. Disponível em: https://arxiv.org/abs/2509.09893. Acesso em: 02 ago. 2026.
[8] YANG, John et al. *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering.* NeurIPS 2024. Disponível em: https://arxiv.org/abs/2405.15793. Acesso em: 02 ago. 2026.
[9] HODA, Rashina. *Toward Agentic Software Engineering Beyond Code: Framing Vision, Values, and Vocabulary.* ICSE 2026 Workshop. Disponível em: https://arxiv.org/abs/2510.19692. Acesso em: 02 ago. 2026.
[10] LEHMANN, Fabian et al. *Software Engineering in the Era of LLMs.* 2024. Disponível em: https://arxiv.org/abs/2403.09752. Acesso em: 02 ago. 2026.
[11] HINGEL, Paula. *How AI Changes the SDLC: A Six-Stage Guide.* Augment Code, 2026. Disponível em: https://www.augmentcode.com/guides/how-ai-changes-the-sdlc. Acesso em: 02 ago. 2026.
[12] GOOGLE CLOUD. *State of AI-assisted Software Development (DORA 2025).* Disponível em: https://dora.dev/research/. Acesso em: 02 ago. 2026.
[13] MICROSOFT. *An AI led SDLC: Building an End-to-End Agentic Software Development Lifecycle with Azure and GitHub.* Microsoft Tech Community, 2026. Disponível em: https://techcommunity.microsoft.com/blog/appsonazureblog/an-ai-led-sdlc-building-an-end-to-end-agentic-software-development-lifecycle-wit/4491896. Acesso em: 02 ago. 2026.
[14] OUSTERHOUT, John. *A Philosophy of Software Design.* 2. ed. Stanford: Yaknyam Press, 2021. Disponível em: https://web.stanford.edu/~ouster/cgi-bin/book.php. Acesso em: 02 ago. 2026.
[15] EVANS, Eric. *Domain-Driven Design: Tackling Complexity in the Heart of Software.* Boston: Addison-Wesley, 2003. Disponível em: https://www.informit.com. Acesso em: 02 ago. 2026.
[16] GRÖPLER, Robin et al. *The Future of Generative AI in Software Engineering: A Vision from Industry and Academia in the European GENIUS Project.* IEEE/ACM AIware, 2025. Disponível em: https://arxiv.org/abs/2511.01348. Acesso em: 02 ago. 2026.
[17] GURGUL, Vincent; GUBELA, Robin; LESSMANN, Stefan. *The State of Generative AI in Software Development: Insights from Literature and a Developer Survey.* 2026. Disponível em: https://arxiv.org/abs/2603.16975. Acesso em: 02 ago. 2026.
[18] WANG, Yuchen; GUO, Shangxin; TAN, Chee Wei. *From Code Generation to Software Testing: AI Copilot with Context-Based RAG.* 2025. Disponível em: https://arxiv.org/abs/2504.01866. Acesso em: 02 ago. 2026.
[19] HODA, Rashina. *Toward Agentic Software Engineering Beyond Code: Framing Vision, Values, and Vocabulary.* ICSE 2026 Workshop. Disponível em: https://arxiv.org/abs/2510.19692. Acesso em: 02 ago. 2026.
[20] LEHMANN, Fabian et al. *Software Engineering in the Era of LLMs.* 2024. Disponível em: https://arxiv.org/abs/2403.09752. Acesso em: 02 ago. 2026.
[21] JIN, Haolin et al. *From LLMs to LLM-based Agents for Software Engineering: A Survey of Current, Challenges and Future.* 2025. Disponível em: https://arxiv.org/abs/2408.02479. Acesso em: 02 ago. 2026.
[22] GRÖPLER, Robin et al. *The Future of Generative AI in Software Engineering: A Vision from Industry and Academia in the European GENIUS Project.* IEEE/ACM AIware, 2025. Disponível em: https://arxiv.org/abs/2511.01348. Acesso em: 02 ago. 2026.
[23] OUSTERHOUT, John. *A Philosophy of Software Design.* 2. ed. Stanford: Yaknyam Press, 2021. Disponível em: https://web.stanford.edu/~ouster/cgi-bin/book.php. Acesso em: 02 ago. 2026.
[24] JIN, Haolin et al. *From LLMs to LLM-based Agents for Software Engineering: A Survey of Current, Challenges and Future.* 2025. Disponível em: https://arxiv.org/abs/2408.02479. Acesso em: 02 ago. 2026.
[25] WANG, Yuchen; GUO, Shangxin; TAN, Chee Wei. *From Code Generation to Software Testing: AI Copilot with Context-Based RAG.* 2025. Disponível em: https://arxiv.org/abs/2504.01866. Acesso em: 02 ago. 2026.
[26] GRÖPLER, Robin et al. *The Future of Generative AI in Software Engineering: A Vision from Industry and Academia in the European GENIUS Project.* IEEE/ACM AIware, 2025. Disponível em: https://arxiv.org/abs/2511.01348. Acesso em: 02 ago. 2026.
