# Capítulo 9: Combustível: Economia de Tokens e Custo de Contexto

## Introdução

No Capítulo 8, você fez o debriefing do voo e aprendeu a transformar incidentes em skill, teste canônico e spec revisada. Agora você entra na Parte V — e na disciplina que decide se o voo chega ao destino: o combustível. Tokens são o recurso escasso do SDLC AI-first, e a economia de contexto é a engenharia que mantém o ciclo vivo dentro dos limites de uma sessão.

Este capítulo ensina a tratar tokens, rate limits e custo de contexto como variáveis de projeto: medir o consumo, comprimir o que é ruído, delegar a subagentes enxutos e projetar handoffs que estendem a vida útil do ciclo. Você vai sair com um orçamento de contexto — e os instrumentos para não estourá-lo.

## Explica

Um token é a unidade básica que um modelo de linguagem processa — aproximadamente uma sílaba de uma palavra em português, uma fração de palavra em inglês. Cada interação com um agente consome tokens de entrada (o contexto que você envia) e de saída (a resposta que ele produz). Quando a conversa cresce, o contexto cresce junto — e o custo de cada turno seguinte também.

O rate limit é a parede dura: cada provedor impõe um teto de tokens por minuto e por dia. Quando a sessão do agente estoura o teto, a execução trava — e o trabalho em andamento fica órfão. No SDLC AI-first, o rate limit não é um problema de infraestrutura; é uma **restrição de design do ciclo de vida**: cada fase deve caber no orçamento de contexto disponível.

A janela de contexto é o espaço da sessão: quantos tokens o modelo "lembra" em uma conversa. Sessões longas degeneram de duas formas: o contexto enche (e o agente esquece o início) ou o custo explode (cada turno reprocessa todo o histórico). A economia de contexto é a engenharia que evita as duas — mantendo a sessão magra e o histórico no lugar certo.

A primeira técnica é a **seleção cirúrgica**: carregar no contexto apenas o que a fase precisa. Antes de ler um arquivo, busque (grep) o que procura; antes de injetar um relatório, injete o resumo; antes de dar o código inteiro ao agente, dê a interface. O princípio é o mesmo do lean manufacturing: nada de estoque (contexto) parado.

A segunda técnica é a **compressão de logs**: saídas de comando com mais de algumas linhas são reduzidas a um resumo representativo — cabeçalho e rodapé — preservando o sinal e descartando o ruído. Logs de build, testes e infraestrutura são os maiores consumidores silenciosos de contexto; comprimi-los é a maior economia imediata.

A terceira técnica é a **comunicação telegráfica entre agentes**: subagentes se reportam ao orquestrador com resumos compactos, não com transcrições. A delegação caveman — instruções mínimas, relatórios mínimos — reduz o contexto em uma ordem de grandeza quando há muitos subagentes em paralelo.

A quarta técnica é o **handoff**: quando a sessão está perto do limite, o trabalho é compactado em um documento de transferência — contexto, decisões, pendências — e um novo agente/sessão continua de onde parou. O handoff transforma o limite da janela de contexto de uma fatalidade em uma transição de projeto.

Por fim, a quinta técnica é o **subagente enxuto**: tarefas de busca e edição extensa são delegadas a subagentes que retornam apenas o resultado, não o processo. O orquestrador nunca vê os bastidores — economizando dezenas de milhares de tokens por delegação.

## Ilustra

Um voo comercial calcula combustível com precisão cirúrgica: o combustível necessário para a rota, mais a reserva legal, mais o alternate. Nenhum piloto enche o tanque "só por garantia" — excesso de peso custa caro. E nenhum piloto decola com combustível de menos — o alternate existe para o caso de desvio.

O contexto é o combustível do voo agêntico. O necessário para a rota é o contexto mínimo da fase. A reserva é a margem para correções inesperadas. E o alternate é o handoff — o plano de desvio quando a sessão não alcança o destino.

_[Diagrama do capítulo omitido neste formato.]_

Como Comandante de Operações de Software, você adota a régua do combustível: carregar o necessário, reservar a margem e sempre ter o alternate desenhado.

## Técnica

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

A métrica por fase alimenta a Fase 8 (Evoluir): a spec que consumiu 48 mil tokens de entrada pode ser redigida com um contexto mais enxuto na próxima iteração.

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

O padrão grep-antes-de-read reduz o contexto de arquivos grandes em uma ordem de grandeza — e é a técnica com melhor retorno por esforço.

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

O resultado: 59 linhas viram 9 — o sinal (início e erro no fim) preservado, o ruído descartado.

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

O handoff é o alternate: o voo desvia, mas não cai — a sessão nova decola do ponto exato.

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

O orçamento declarado transforma o rate limit de fatalidade em projeto: a esteira sabe, antes de começar, quantos tokens cada fase pode gastar — e onde parar com dignidade, em vez de morrer no meio.

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

O cache é o reservatório da torre: o que já foi processado não é reprocessado — economizando os tokens que seriam gastos recalculando o mesmo resultado.

### O Custo do Contexto como Decisão de Fronteira

A economia de contexto também intersecta a cartografia do Capítulo 4: fronteiras bem desenhadas são a forma estrutural de economizar tokens. Quando cada módulo expõe uma interface pequena, o agente que o consome carrega apenas a interface — não o módulo inteiro. A economia não é só tática (comprimir logs); é arquitetural (não precisar carregar o que não importa). O Comandante de Operações de Software desenha fronteiras pensando no combustível desde o design.

### A Contabilidade da Sessão

A disciplina do combustível exige contabilidade: cada sessão registra entrada, saída e o que ficou de fora. O orçamento de contexto de uma fase não é só o teto de tokens — é a lista explícita do que a fase **não** carrega. Essa contabilidade vira insumo do debriefing do Capítulo 8: a sessão que gastou 50 mil tokens em contexto desnecessário é uma falha de processo, não de infraestrutura.

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

A economia de 85% não é mágica — é seleção cirúrgica aplicada: o agente só vê o que precisa para decidir, e o resto fica no repositório, não no contexto.

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

O perfil por fase transforma a economia de contexto de intuição em engenharia: cada fase sabe, antes de começar, onde o combustível será gasto — e onde cortar sem perder sinal.

### O Modelo de Priorização do Corte de Contexto

Quando o orçamento aperta, o Comandante corta com método — não por intuição. O modelo abaixo prioriza o que comprimir:

| Prioridade | O que cortar | Exemplo | Impacto no sinal |
|------------|-------------|---------|------------------|
| 1 | Logs de build e teste | Saída do pytest | Nenhum (sinal no fim) |
| 2 | Histórico de iteração | Versões antigas de diffs | Nenhum (estado no handoff) |
| 3 | Implementação de módulos | Corpo do código | Baixo (interface basta) |
| 4 | Relatórios intermediários | Dossiês completos | Médio (resumo basta) |
| 5 | Conteúdo de domínio | Prosa da spec | **Nunca cortar** |

A prioridade 5 é a regra de ouro do capítulo: o conteúdo de domínio — a prosa que carrega decisão — nunca é comprimido. O corte disciplinado preserva o sinal e elimina o ruído, exatamente na ordem que o modelo define.

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

A curva de custo revela onde a economia rende mais: o build domina o orçamento — e é lá que a seleção cirúrgica e o test-first pagam o maior dividendo. O Comandante aloca disciplina onde o custo é maior, não onde é mais visível.

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

O documento de transferência já apareceu no Capítulo 5 — aqui você vê o momento exato de usá-lo. O handoff não é falha da sessão; é o alternate planejado, o aeroporto reserva para o desvio.

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

O relatório é o painel de combustível retrospectivo: a pesquisa estourou 24% (dossiê inteiro no contexto em vez de RAG), o build estourou 8% (grep-antes-de-read negligenciado). A calibração do próximo ciclo parte desses números — não da intuição.

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

O monitor é o indicador de combustível da cabine: quando o consumo cruza 70%, a tripulação muda de comportamento — comprime, simplifica ou prepara o handoff. Nunca descobre o estouro depois.

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

A economia de contexto tem limite: comprimir conteúdo de negócio para economizar tokens destrói o valor que o conteúdo carrega. A régua é clara — comprima ruído técnico (logs, outputs de build, repetições), nunca a prosa do domínio (spec, requisitos, decisões de arquitetura). O Comandante distingue o que é sinal do que é ruído antes de comprimir: a regra de ouro da economia de contexto é não economizar no que você precisa ler para decidir.

### O Hábito do Custo Antes da Ação

O orçamento de contexto só funciona se o hábito estiver instalado: antes de qualquer leitura, estimar o custo; antes de qualquer busca, formular o alvo; antes de delegar, comparar com o custo de fazer direto. O hábito não é natural — é treinado com o monitor de sessão mostrando o consumo em tempo real. Nas primeiras semanas o time olha o medidor com culpa; depois de um mês, a estimativa de custo precede a ação sem esforço. Economia de contexto é um músculo, não uma regra.

### Passos para Implantar o Orçamento de Contexto

1. **Meça** o consumo por fase em todas as sessões.
2. **Aplique grep-antes-de-read** em arquivos grandes.
3. **Comprima logs** com o padrão 3+4.
4. **Use subagentes enxutos** para busca e edição extensa.
5. **Desenhe o handoff** antes de cada sessão longa.

## Aplica

Cena real, em segunda pessoa. Sua equipe delegou a um agente a refatoração de um módulo legado de 40 mil linhas. Na sessão 1, o agente carrega o arquivo inteiro, os relatórios inteiros e os logs inteiros no contexto. Na sessão 3, o contexto estoura no meio da refatoração — e o agente perde o fio. O time recomeça do zero, com um agente novo, e o ciclo se repete três vezes antes de alguém perguntar por quê.

O erro não foi o tamanho do módulo. O erro foi a ausência de orçamento de contexto. Cada sessão gastou o combustível inteiro no primeiro trecho do voo, sem reserva e sem alternate. O handoff — o documento que salvaria o estado entre sessões — nunca foi escrito porque ninguém planejou a possibilidade de estouro.

O diagnóstico, ligado à teoria: sessão sem orçamento é voo sem cálculo de combustível. A correção prática:

1. **Meça antes de delegar**: estime o contexto do módulo (arquivos, relatórios, logs) antes da sessão 1.
2. **Carregue cirurgicamente**: interface em vez de implementação, resumo em vez de relatório, grep antes de read.
3. **Desenhe o handoff na decolagem**: o documento de transferência existe antes da sessão começar, não quando ela estoura.
4. **Delegue o pesado a subagentes enxutos**: a varredura do módulo legado é trabalho de subagente que retorna só o mapa — não o território inteiro.

Armadilhas comuns: achar que contexto é ilimitado porque a janela cresce (o custo cresce junto); comprimir conteúdo de negócio em vez de log (comprima ruído técnico, nunca a prosa do domínio); e tratar o rate limit como "problema de provedor" (é problema de design do ciclo).

## Conclusão

Você dominou o combustível. Três marcos: primeiro, tokens e rate limits como variáveis de projeto — cada fase cabe no orçamento ou não decola; segundo, as técnicas de economia — seleção cirúrgica, compressão de logs, comunicação telegráfica e subagentes enxutos; terceiro, o handoff como alternate — o estado compactado que estende a vida útil da sessão em vez de deixá-la morrer.

Como desafio, registre o consumo de contexto da próxima sessão do seu time, fase a fase, e identifique os três maiores consumidores silenciosos. Corte-os e meça de novo.

No último capítulo, você sobe ao posto definitivo: maturidade, riscos e o futuro do SDLC AI-first — o que separa o Comandante do passageiro.

## Por que este capítulo importa

Se você chegou até aqui, já percebeu que debriefing: o loop de aprendizado que evolui o ciclo & combustível: economia de tokens e custo de contexto. Este capítulo — *Capítulo 9: Combustível: Economia de Tokens e Custo de Contexto* — é um convite para parar de usar IA como ferramenta de autocomplete e começar a tratá-la como parte estrutural do seu processo de desenvolvimento. A diferença entre as duas posturas é exatamente o que separa quem apenas acelera o que já fazia de quem repensa o que é possível.

Vamos explorar isso com exemplos práticos, código real e um passo a passo que você pode aplicar ainda hoje, sem esperar por infraestrutura nova ou aprovação de comitê. A ideia é simples: cada seção termina com algo que você pode executar em menos de uma hora.

## Conceitos-chave deste capítulo

- **O contrato antes da execução:** antes de deixar qualquer agente trabalhar, defina o que significa "feito" em termos verificáveis.
- **Evidência antes de afirmação:** o que não pode ser verificado não pode ser delegado com segurança.
- **Aprendizado contínuo:** cada entrega, boa ou ruim, é matéria-prima para o próximo ciclo.

Esses três conceitos aparecem, de formas diferentes, em todas as seções a seguir. Mantê-los em mente enquanto você lê vai transformar exemplos isolados em um padrão que você reconhece na sua própria rotina.

## Checklist para aplicar hoje

1. Escolha uma tarefa pequena e bem definida do seu backlog.
2. Escreva o critério de aceite em uma frase verificável.
3. Delegue a execução a um agente, mantendo a verificação em suas mãos.
4. Registre o que funcionou e o que não funcionou.
5. Transforme o aprendizado em um procedimento reutilizável.

Se você fizer apenas o primeiro item, já estará à frente da maioria das equipes — que continua discutindo IA em reuniões sem nunca definir o que quer que ela faça.

## Perguntas que você deve se fazer

1. Qual fase do meu processo consome mais tempo hoje — e por quê?
2. O que eu delegaria a um agente amanhã se tivesse certeza de que o resultado seria verificado?
3. Qual informação eu poderia registrar hoje que tornaria a próxima iteração mais barata?
4. Quem no meu time revisa o trabalho de quem — e com qual critério?
5. O que eu faria se o custo de cada tentativa caísse para quase zero?

Essas perguntas não têm resposta certa, mas têm uma propriedade em comum: elas forçam você a sair da conversa abstrata sobre IA e entrar no terreno do seu processo real. E é exatamente nesse terreno que o SDLC AI-first produz resultado.

## Glossário rápido

- **Agente:** programa que usa um modelo de linguagem para planejar e executar tarefas com acesso a ferramentas.
- **Harness:** a camada que conecta o agente ao ambiente — arquivos, comandos, testes e regras.
- **Spec executável:** especificação cujos critérios podem ser verificados por máquina.
- **Verificação adversarial:** camada que refuta o trabalho produzido, em vez de apenas confirmá-lo.
- **Contexto:** a janela de informação que o modelo enxerga a cada passo — o recurso mais caro do ciclo.

Dominar esses cinco termos é suficiente para acompanhar qualquer discussão séria sobre desenvolvimento orientado a agentes.

## O erro mais comum nesta fase

A maioria das equipes comete o mesmo erro: adota a ferramenta e mantém o processo. O agente entra no fluxo como um autocomplete sofisticado, e todo o potencial de transformação se perde em pequenas conveniências. O antídoto é simples e desconfortável: mude o processo primeiro, depois traga a ferramenta. Defina o contrato, o critério de aceite e a verificação antes de permitir que o agente produza em escala. É contra intuitivo, mas é o que separa as equipes que capturam valor das que apenas geram volume.

## Um exemplo concreto para fixar

Imagine uma pequena feature de faturamento. No fluxo tradicional, um desenvolvedor recebe a tarefa, interpreta a intenção, escreve o código e um revisor confia na leitura. No fluxo orientado a agentes, a mesma feature começa com uma frase verificável: "o valor total deve considerar o desconto aplicado antes dos impostos". O agente implementa, os testes verificam a regra, e o humano revisa a evidência — não o código linha a linha, mas o comportamento observado. Perceba o deslocamento: o humano deixa de ler tudo para auditar o essencial, e o agente deixa de adivinhar para executar contra um critério. É essa troca que o restante do livro explora em profundidade.

## A rotina de quem já opera assim

Uma semana de trabalho em uma equipe que já adotou o ciclo orientado a agentes não parece uma revolução — parece um fluxo calmo e bem definido. Na segunda-feira, a especificação da semana é revisada em uma reunião curta: cada critério de aceite é lido em voz alta e qualquer ambiguidade é resolvida antes de tocar em código. Na terça, os agentes executam as tarefas em isolamento, enquanto os humanos revisam a arquitetura e os contratos. Na quarta, a verificação roda: testes, revisão adversarial e a decisão de merge apoiada em evidência. Na quinta, o que passou vai para produção em canário, com observabilidade ligada. Na sexta, o debriefing transforma os incidentes da semana em lições e skills. Nenhum dia é heroico; todos os dias são previsíveis. E é exatamente essa previsibilidade — não a velocidade máxima — que define a alta performance.

## O que não fazer: os anti-padrões mais comuns

Se você quer destruir o valor do desenvolvimento orientado a agentes, aqui estão as receitas mais eficientes. Primeiro, o prompt-and-pray: gere o código, olhe por cima, e peça desculpas quando quebrar. Funciona em demos, falha em produção. Segundo, a spec decorativa: escreva documentos longos que ninguém verifica e que o agente não consegue executar — o pior dos dois mundos. Terceiro, a auto-verificação: deixe que quem escreveu valide o próprio trabalho, sem revisor independente; é a forma mais rápida de transformar confiança em acidente. Quarto, a delegação sem observabilidade: conceda autonomia sem instrumentar o comportamento. Todos esses padrões têm uma origem comum — a pressa em capturar o ganho sem construir o controle. E todos têm o mesmo antídoto: contrato antes de execução, evidência antes de afirmação, e revisão independente em toda entrega.

## Como medir o progresso na prática

Uma dúvida legítima é: como saber se a adoção está dando certo? Métricas tradicionais de velocidade podem enganar — um time pode entregar mais rápido e acumular dívida técnica invisível. O indicador mais confiável no ciclo orientado a agentes é a estabilidade: quantos incidentes em produção, quanto tempo de retrabalho, quantas correções de emergência. Um segundo indicador é o custo de contexto: quantos tokens cada fase consome, e onde o desperdício se concentra. Um terceiro é a taxa de aceite na primeira verificação: se os agentes precisam de muitas rodadas de refutação, o contrato está fraco — o problema não é o agente, é a spec. Com esses três números na mesa, a conversa de progresso deixa de ser anedótica e vira análise de processo.

## O papel do líder neste capítulo

Nada do que este capítulo descreve acontece por acaso — alguém precisa criar as condições para que o processo exista. Esse alguém é o líder técnico, o líder de equipe ou o arquiteto que decidiu tratar o ciclo orientado a agentes como uma mudança de processo, não como a instalação de uma ferramenta. O trabalho do líder aqui tem quatro frentes. A primeira é a modelagem do contrato: garantir que cada fase tem entrada, saída e critério definidos. A segunda é a calibragem da confiança: decidir o que pode ser delegado e o que exige decisão humana, e documentar essa decisão. A terceira é a defesa do tempo de verificação: em uma cultura que celebra velocidade, o líder precisa defender o orçamento de revisão como quem defende o seguro do prédio. A quarta é o exemplo: o líder que pede evidência antes de afirmar, em toda reunião, ensina mais do que qualquer documento de processo.

## Perguntas frequentes honestas

P: Isso não vai tirar o emprego dos desenvolvedores? R: A história do ciclo de vida nunca foi sobre menos trabalho humano, mas sobre trabalho mais valioso. O que muda é a natureza da tarefa: escrever código repetitivo deixa de ser o centro, e a especificação, a verificação e o desenho de contratos ocupam o lugar. P: Precisamos de um time de especialistas em IA para começar? R: Não. Precisa-se de disciplina de processo e de vontade de medir. As ferramentas evoluem rápido; o processo é o que permanece. P: E se o agente produzir código que ninguém entende? R: Essa é a pergunta certa — e a resposta é a verificação: se o código passa nos testes, na revisão adversarial e na observabilidade em produção, o fato de ter sido escrito por um agente é irrelevante. O critério não é a origem, é a evidência. P: Quanto tempo leva para ver resultado? R: Na primeira semana você já vê o efeito de escrever critérios de aceite verificáveis, independentemente de agentes. Os ganhos estruturais aparecem em um a dois ciclos.

## Um convite para a prática deliberada

Conhecimento sem prática é entretenimento disfarçado de aprendizado. Este capítulo termina com um convite para a prática deliberada: escolha um artefato real do seu trabalho — uma spec, um teste, um release — e aplique deliberadamente um dos conceitos aqui descritos. Anote o antes e o depois. Repita por quatro semanas. No fim do mês, compare: o processo está mais previsível? O custo de contexto caiu? A estabilidade melhorou? Esse experimento pessoal, pequeno e mensurável, vale mais do que qualquer curso. É assim que o ciclo orientado a agentes deixa de ser um conceito que você explica para outras pessoas e se torna uma capacidade que você demonstra.

## Síntese para levar com você

Se você guardar apenas uma ideia deste capítulo, que seja esta: no ciclo orientado a agentes, o contrato precede a execução, a evidência precede a afirmação e a revisão independente precede a entrega. Tudo o mais — as ferramentas, os modelos, os fluxos — muda rápido e pode ser aprendido conforme a necessidade. O que não muda é a disciplina: sem ela, a IA é um gerador de volume; com ela, é um multiplicador de capacidade. O resto do livro é a expansão dessa disciplina em cada fase do ciclo de vida.

## De onde veio a necessidade desta mudança

Vale a pena entender por que este capítulo existe — e por que ele não foi escrito dez anos atrás. A resposta está na economia do desenvolvimento de software. Durante décadas, o custo dominante de produzir software foi o trabalho humano: escrever, revisar, corrigir. Todo o ciclo de vida clássico foi desenhado em torno dessa escassez — processos, papéis e artefatos existem para coordenar pessoas e evitar retrabalho caro. O que mudou nos últimos anos foi a emergência de modelos capazes de gerar, revisar e executar código com custo marginal próximo de zero. De repente, a escassez dominante não é mais a mão de obra: é a capacidade de especificar, orquestrar e verificar. Esse deslocamento — de horas-homem para tokens e contexto — é a raiz de tudo o que este capítulo descreve. Quem entende essa mudança de economia entende por que o processo precisa mudar junto com a ferramenta.

## Conversando com quem resiste

Em toda equipe há quem resista à mudança — e a resistência quase nunca é preguiça, é uma pergunta legítima sem resposta. As objeções mais comuns são três. "Já tentamos automação e quebrou": a resposta é que a automação anterior quebrou porque o processo não tinha contrato nem verificação; é exatamente isso que o novo ciclo constrói antes de automatizar. "IA gera código que ninguém entende": a resposta é que o critério de entendimento mudou — o que importa não é a origem do código, mas se ele passa na verificação; e a revisão de contrato e arquitetura continua humana. "Isso é modismo": a resposta mais honesta é que pode ser, mas o processo que este capítulo descreve — especificar, delegar, verificar, aprender — melhora o ciclo com ou sem IA. A disciplina é o investimento à prova de modismo.

## O dia a dia no detalhe

Para tornar concreto o que este capítulo descreve, vale percorrer o dia a dia de uma tarefa típica, passo a passo. A manhã começa com a revisão da intenção: o produto explica o que quer, o time traduz em requisitos com critérios verificáveis e ninguém toca em código antes de a spec estar aprovada. Na sequência, o trabalho é despachado: cada tarefa vai para um contexto isolado, com seu contrato anexado. A execução produz artefatos — código, testes, diagramas — e cada artefato carrega a evidência de como foi produzido. A tarde é de verificação: testes automáticos, revisão adversarial e a leitura humana do que é crítico. O que passa, segue; o que não passa, volta com o parecer anexado — sem discussão de opinião, porque o critério já estava escrito. O fim do dia é de registro: o que foi aprendido, o que custou em contexto, o que deve mudar no processo. Esse fluxo parece simples, mas cada passo exige disciplina — e é exatamente a simplicidade do ritmo que o torna sustentável.

## O custo invisível que decide tudo

Há um recurso que atravessa todos os exemplos deste capítulo e que raramente aparece nas discussões: o contexto. Cada interação com um modelo de linguagem consome uma janela de informação — e essa janela é limitada e cara. Uma spec mal escrita gasta contexto em ciclos de correção. Um log inteiro no contexto gasta contexto que poderia servir à verificação. Uma busca redundante gasta contexto sem produzir informação. Quem ignora esse custo descobre, cedo ou tarde, que a automação ficou mais cara que o trabalho manual que pretendia substituir. Por isso a disciplina de contexto não é um detalhe de economia — é uma decisão de arquitetura do ciclo. Medir o consumo por fase, comprimir o que é ruído e injetar apenas o necessário são práticas que determinam se o SDLC AI-first se sustenta em escala. Este capítulo toca nesse tema; os capítulos finais do livro o desdobram em técnica.

## Uma visão de longo prazo

A adoção do ciclo orientado a agentes não é um projeto com data de fim — é uma trajetória que se desenrola ao longo de anos, e vale a pena olhar para a frente. No primeiro trimestre, o foco é o contrato: as equipes aprendem a especificar e a verificar, e os ganhos vêm da clareza, não da automação. No segundo trimestre, a delegação supervisionada entra em produção em áreas de baixo risco, e as métricas começam a mostrar onde o ciclo ganha e onde perde. No segundo ano, o ciclo adversarial se consolida: verificação automática, observabilidade do comportamento agêntico e aprendizado organizacional rodando como rotina. No terceiro ano, a organização opera em um nível de maturidade em que a IA é parte estrutural do processo, e a pergunta deixa de ser "como adotar" e passa a ser "como evoluir". Quem inicia com o processo antes da ferramenta chega a esse destino com estabilidade; quem inverte a ordem, chega com dívida. A escolha é sua.
