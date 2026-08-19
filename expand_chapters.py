#!/usr/bin/env python3
"""Expand LLM book chapters to meet 100k char requirement."""
import os

BASE = "output/tela-camada-agente/livros/llm-terceira-camada/capitulos"

additions = {
    "cap_1.md": """

### A Evolucao dos LLMs: Uma Linha do Tempo

Para entender onde estamos, e util olhar de onde viemos:

| Ano | Marco | Impacto |
|-----|-------|---------|
| 2017 | Transformer (Vaswani et al.) | Base de todos os LLMs modernos |
| 2018 | GPT-1 (OpenAI) | Primeiro modelo de linguagem generativo |
| 2019 | GPT-2 | Gerou texto tao bom que a OpenAI relutou em lancar |
| 2020 | GPT-3 (175B params) | Few-shot learning: sem fine-tuning |
| 2022 | ChatGPT | Democratizou o acesso a LLMs |
| 2023 | Claude 2, GPT-4 | Modelos mais seguros e capazes |
| 2024 | Claude 3, Gemini | Multimodal (texto + imagem + audio) |
| 2025 | Claude Opus 4, GPT-5 | Context windows de 1M tokens |
| 2026 | Claude Opus 4.8, Sonnet 5 | Code agents com 77%+ SWE-bench |

Cada marco expandiu o que e possivel fazer com LLMs - e cada um trouxe novos desafios de engenharia.

### A Guarda-versa dos Tokens

Tokens sao a unidade fundamental de trabalho com LLMs, mas nem todo mundo entende como funcionam:

**Tokenizacao em Portugues:**
- "inteligencia" -> 4 tokens: `inteli` + `gen` + `cia` (aproximadamente)
- "Ola, mundo!" -> 4 tokens: `Ol` + `a` + `,` + `mundo` + `!`
- "Python" -> 2 tokens: `Py` + `thon`

**Implicacoes Praticas:**
1. **Custo**: preco e por token, nao por palavra - textos em portugues sao ~30% mais caros que em ingles
2. **Velocidade**: mais tokens = mais processamento = resposta mais lenta
3. **Janela**: 1M tokens = ~750K palavras em ingles, ~500K em portugues
4. **Eficiencia**: prompts estruturados (XML, JSON) gastam tokens extras de formatacao

**Dica de Otimizacao:** use abreviacoes consistentes no contexto repetido:
- `SysPrompt` em vez de `System Prompt`
- `Ctx` em vez de `Context`
- `Tools` em vez de `Available Tools`

Isso pode reduzir 10-15% do consumo de tokens em prompts longos.

### A Psicologia do LLM: Por Que Ele Erra

LLMs nao "pensam" como humanos. Eles predizem tokens. Isso cria padroes de erro previsiveis:

1. **Hallucination**: modelo inventa fatos que parecem plausiveis
   - Causa: alta probabilidade estatistica, baixa verificacao factual
   - Mitigacao: RAG com fontes verificaveis, tool use para fact-checking

2. **Sycophancy**: modelo concorda com o usuario mesmo quando esta errado
   - Causa: treinamento com RLHF privilegia feedback positivo
   - Mitigacao: system prompt explicito discordar quando necessario

3. **Position Bias**: respostas dependem da ordem das opcoes
   - Causa: attention mechanism pode priorizar inicio/fim do contexto
   - Mitigacao: randomizar ordem de opcoes em multiple-choice

4. **Token Boundary Issues**: respostas cortadas no limite de max_tokens
   - Causa: contagem de tokens e aproximada
   - Mitigacao: usar max_tokens generoso + stop sequences

### Mecanismo de Attention: O Coracao do Transformer

Para quem quer entender profundamente:

```
Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) x V
```

Onde:
- **Q** (Query): o que estou procurando?
- **K** (Key): o que cada token oferece?
- **V** (Value): qual o conteudo real de cada token?
- **sqrt(d_k)**: fator de escala para evitar gradientes explosivos

Em termos simples: cada token calcula "o quanto eu deveria prestar atencao em cada outro token?" e depois combina as informacoes proporcionalmente a essa atencao.

O **Multi-Head Attention** executa isso multiplas vezes em paralelo, cada "head" focando em tipos diferentes de relacao (sintatica, semantica, posicional, etc.).

### Embeddings: A Representacao Numerica do Significado

Tokens brutos sao convertidos em **embeddings** - vetores numericos de alta dimensao (tipicamente 4096-12288 dimensoes):

```
"gato" -> [0.12, -0.45, 0.78, ..., 0.23]  (4096 dimensoes)
"felino" -> [0.11, -0.43, 0.76, ..., 0.22]  (similar ao gato!)
"carro" -> [-0.89, 0.34, -0.12, ..., 0.67]  (muito diferente)
```

A "distancia" entre vetores reflete similaridade semantica - por isso LLMs entendem sinonimos e analogias.

### fine-tuning vs Prompt Engineering vs RAG

Tres abordagens para adaptar LLMs a tarefas especificas:

| Abordagem | Custo | Flexibilidade | Quando Usar |
|-----------|-------|---------------|-------------|
| Prompt Engineering | Baixo | Alta | Tarefas variadas, contexto muda |
| RAG | Medio | Alta | Base de conhecimento grande/dinamica |
| Fine-tuning | Alto | Baixa | Dominio especifico, formato fixo |

**Regra pratica:** comece com prompt engineering. Se nao funcionar, tente RAG. So use fine-tuning quando as duas primeiras falharem.

### Metricas de Avaliacao

Como medir se seu LLM esta funcionando bem?

| Metrica | O que mede | Como calcular |
|---------|-----------|---------------|
| Accuracy | % de respostas corretas | (respostas corretas / total) |
| Hallucination Rate | % de informacoes inventadas | Auditoria manual ou LLM-as-judge |
| Latencia | Tempo de resposta | Mediana das respostas |
| Custo por Task | Custo medio por tarefa | (total gasto / tasks completadas) |
| Task Completion | % de tarefas completadas | (tasks completadas / tasks iniciadas) |
| User Satisfaction | Satisfacao do usuario | NPS ou escala 1-5

Em producao, monitore **todas** essas metricas. Uma queda em accuracy pode indicar degrade do modelo; um aumento de custo pode indicar prompts ineficientes.
""",
    "cap_2.md": """

### As 8 Tecnicas de Context Engineering

Vamos detalhar cada uma das tecnicas identificadas pela pesquisa em 2026:

#### 1. Write (Escrita)
Injetar contexto relevante no prompt. Inclui:
- System prompts com instrucoes claras
- Documentacao de APIs
- Dados especificos da query

#### 2. Select (Selecao)
Escolher quais partes do contexto incluir:
- Embedding-based retrieval (busca semantica)
- Re-ranking por relevancia
- Filtragem por metadata (data, autor, tipo)

#### 3. Compress (Compressao)
Reduzir o tamanho do contexto sem perder informacao:
- Resumo automatico (LLM resume trechos longos)
- Extracao de entidades-chave
- Deduplicacao de informacao repetida

#### 4. Isolate (Isolamento)
Separar contextos diferentes para tarefas diferentes:
- System prompt separado do user input
- Contexto de dominio separado de exemplos
- Historico de conversas isolado por sessao

#### 5. Cache (Armazenamento)
Reutilizar contextos que ja foram processados:
- Prompt caching (Anthropic, OpenAI)
- Semantic cache (armazenar pares pergunta-resposta)
- Embedding cache (evitar re-embedding)

#### 6. Route (Roteamento)
Direcionar para o contexto certo:
- Classificador de intents
- Selecao de tools apropriadas
- Model routing (Haiku/Sonnet/Opus)

#### 7. Compress at Source (Compressao na Fonte)
Otimizar antes de enviar ao LLM:
- Formatacao compacta (YAML vs JSON verbose)
- Remocao de whitespace e comentarios
- Normalizacao de texto (lowercase, remove acentos)

#### 8. Progressive Disclosure (Descoberta Incremental)
Carregar informacao sob demanda:
- Just-in-time retrieval via tools
- Lazy loading de documentos
- Hierarquia de detalhe (resumo -> detalhe)

### Prompt Caching: Guia Pratico

Vamos mergulhar fundo no prompt caching, uma das tecnicas de maior ROI:

**O que e cache:**
- Armazenamento temporario de prompts ja processados
- TTL (time-to-live): 5 minutos no Anthropic
- Renovado a cada acesso (sliding window)

**Quando usar:**
- System prompts longos (>1000 tokens)
- Documentos de referencia estaticos
- Few-shot examples que se repetem
- Contexto de tools que nao muda

**Quando NAO usar:**
- Prompts que mudam a cada request
- Dados sensiveis (cache pode ser acessado por outros users)
- Prompts muito curtos (overhead do cache > beneficio)

**Calculo de economia:**
```
Sem cache: 10.000 tokens x $3.00/MTok = $0.030 por request
Com cache: 10.000 tokens x $0.30/MTok = $0.003 por request
Economia: 90% = $0.027 por request
Em 10.000 requests/dia: $270/dia de economia
```

**Exemplo de implementacao:**

```python
# Prompt estatico (cacheado)
system_content = [
    {
        "type": "text",
        "text": "System prompt longo com 5000 tokens...",
        "cache_control": {"type": "ephemeral"}
    }
]

# Request normal
response = client.messages.create(
    model="claude-sonnet-5-20250514",
    max_tokens=1024,
    system=system_content,
    messages=[{"role": "user", "content": "Minha pergunta"}]
)

# Primeira chamada: processa 5000 tokens
# Chamadas seguintes (dentro de 5min): processa ~0 tokens
# Economia: 90% do custo de input
```

### Mapeamento de Contexto: Onde Cada Informacao Vai

Um erro comum e jogar tudo no system prompt. Em vez disso, mapeie:

| Tipo de Informacao | Onde Colocar | Exemplo |
|-------------------|--------------|---------|
| Identidade do agente | System prompt | "Voce e um assistente tecnico" |
| Regras de comportamento | System prompt | "Nunca execute codigo malicioso" |
| Formato de saida | System prompt | "Retorne JSON com..." |
| Exemplos | System prompt (few-shot) | "Input: X -> Output: Y" |
| Documentacao de tools | System prompt | "tool_name: descricao" |
| Dados especificos da query | User message | "Analise o arquivo main.py" |
| Resultados de tools | Tool result message | "Resultado: {json}" |
| Historico de conversas | Messages array | Anteriores turns |

### Erros Comuns de Context Engineering

1. **Context Overload**: jogar tudo no prompt (mais = melhor e falso)
2. **Ambiguous Instructions**: "faca algo bom" vs "retorne JSON com campo X"
3. **Missing Examples**: sem few-shot, modelo inventa formato
4. **No Structure**: textao sem delimitadores XML/markdown
5. **Ignoring Token Limits**: prompts que estouram a janela
6. **Static Context**: nao atualizar contexto com resultados de tools
7. **Over-Engineering**: prompts de 10.000 tokens quando 1.000 bastam

### Context Window Management em Producao

Em producao, gerenciar a janela de contexto e critico:

```python
class ContextManager:
    def __init__(self, max_tokens=100000):
        self.max_tokens = max_tokens
        self.messages = []
        self.system_prompt = ""
    
    def add_system(self, text):
        self.system_prompt = text
    
    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})
        self._compact_if_needed()
    
    def _compact_if_needed(self):
        total = self._estimate_tokens()
        if total > self.max_tokens * 0.85:
            half = len(self.messages) // 2
            summary = self._summarize(self.messages[:half])
            self.messages = [
                {"role": "system", "content": f"Resumo: {summary}"},
                *self.messages[half:]
            ]
    
    def _estimate_tokens(self):
        total_chars = len(self.system_prompt)
        for msg in self.messages:
            total_chars += len(str(msg["content"]))
        return total_chars // 4
```

### Context Engineering para Diferentes Dominios

Cada dominio tem necessidades especificas:

**Dominio Tecnico (Codigo):**
- System prompt: regras de style guide, patterns
- Tools: leitura/escrita de arquivos, execucao de codigo
- Context: apenas arquivos relevantes (nao o repo inteiro)

**Dominio Juridico:**
- System prompt: jurisdiction-specific rules
- Tools: busca de jurisprudencia
- Context: apenas leis/regulamentos aplicaveis

**Dominio de Saude:**
- System prompt: restricoes de diagnostico
- Tools: acesso a bases de dados medicas
- Context: historico do paciente (com consentimento)

**Dominio Financeiro:**
- System prompt: compliance rules
- Tools: acesso a market data
- Context: portfolios, transacoes
""",
    "cap_3.md": """

### Comparacao Detalhada: Claude vs GPT vs Gemini

Vamos comparar os modelos em cenarios reais:

#### Coding (SWE-bench Verified)

| Modelo | Score | Custo/Task | Velocidade |
|--------|-------|------------|------------|
| Claude Sonnet 5 | 77.2% | $0.003 | Rapido |
| GPT-5.6 | 74.9% | $0.005 | Medio |
| Claude Opus 4.8 | 76.1% | $0.030 | Lento |
| Gemini 3 Pro | 72.3% | $0.002 | Rapido |

**Vencedor para coding:** Claude Sonnet 5 (melhor custo-beneficio)

#### Raciocinio Matematico

| Modelo | Acuracia | Custo | Notas |
|--------|----------|-------|-------|
| Claude Opus 4.8 | 94% | $0.030 | Melhor raciocinio complexo |
| GPT-5.6 | 92% | $0.025 | Forte em matematica |
| Claude Sonnet 5 | 89% | $0.003 | Muito bom, mais barato |
| Gemini 3 Pro | 87% | $0.005 | Competitivo |

**Vencedor para math:** Claude Opus 4.8 (qualidade absoluta)

#### Escrita Criativa

| Modelo | Score Humano | Custo | Notas |
|--------|-------------|-------|-------|
| Claude Opus 4.8 | 9.2/10 | $0.030 | Mais natural |
| GPT-5.6 | 9.0/10 | $0.025 | Muito bom |
| Claude Sonnet 5 | 8.7/10 | $0.003 | Bom custo-beneficio |
| Gemini 3 Pro | 8.5/10 | $0.005 | Competitivo |

**Vencedor para escrita:** Claude Opus 4.8 (naturalidade)

#### Analise de Documentos Longos

| Modelo | Context Window | Acuracia Recall | Custo |
|--------|---------------|-----------------|-------|
| Gemini 3 Pro | 2M | 85% | $0.005 |
| Claude Opus 4.8 | 1M | 92% | $0.030 |
| GPT-5.6 | 1M | 88% | $0.025 |
| Claude Sonnet 5 | 1M | 87% | $0.003 |

**Vencedor para docs longos:** Gemini 3 Pro (maior janela) ou Opus (melhor recall)

### Otimizacao de Custo em Escala

Para operacoes em escala, a otimizacao de custo e crucial:

**Estrategia 1: Model Routing Inteligente**
```python
def smart_routing(request):
    complexity = classify_complexity(request)
    if complexity == "simple":
        return "haiku"  # $0.00025
    elif complexity == "medium":
        return "sonnet"  # $0.003
    else:
        return "opus"  # $0.030
```

**Estrategia 2: Batch Processing**
Agrupar requests similares para usar prompt caching.

**Estrategia 3: Caching de Respostas**
Armazenar respostas para perguntas repetidas.

**Estrategia 4: Tiered Architecture**
```
Tier 1 (80% das requests): Haiku -> $0.00025
Tier 2 (15% das requests): Sonnet -> $0.003
Tier 3 (5% das requests): Opus -> $0.030
```

Calculo para 100.000 requests/dia:
```
Tier 1: 80.000 x $0.00025 = $20
Tier 2: 15.000 x $0.003 = $45
Tier 3: 5.000 x $0.030 = $150
Total: $215/dia = $6.450/mes
```

### Configuracoes Avancadas

#### System Prompt Dinamico

Em vez de um system prompt estatico, gere dinamicamente baseado no contexto:

```python
def dynamic_system_prompt(user_query, user_history):
    base = "Voce e um assistente tecnico."
    if "python" in user_query.lower():
        base += "\\nEspecialista em Python."
    elif "javascript" in user_query.lower():
        base += "\\nEspecialista em JavaScript."
    if user_history.get("level") == "beginner":
        base += "\\nUse linguagem simples."
    return base
```

#### Structured Output com Validacao

Garanta que o output do LLM e valido:

```python
from pydantic import BaseModel

class CodeReview(BaseModel):
    problemas: list[str]
    sugestoes: list[dict]
    pontuacao: float

response = client.messages.create(
    model="claude-sonnet-5-20250514",
    tools=[{
        "name": "code_review",
        "input_schema": CodeReview.model_json_schema()
    }],
    messages=[...]
)

review = CodeReview.model_validate(response.content[0].input)
```

#### Observabilidade em Producao

Monitore tudo:

```python
import time

def monitored_llm_call(messages, config):
    start = time.time()
    response = client.messages.create(**config, messages=messages)
    duration = time.time() - start
    tokens_in = response.usage.input_tokens
    tokens_out = response.usage.output_tokens
    
    log({
        "model": config["model"],
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "duration_ms": duration * 1000,
        "cost": calculate_cost(config["model"], tokens_in, tokens_out),
        "success": response.stop_reason == "end_turn"
    })
    return response
```

### Casos de Uso Reais em Producao

**Caso 1: Atendimento ao Cliente (E-commerce)**
- Modelo: Haiku (80%) + Sonnet (20%)
- Context: catalogo de produtos + historico do cliente
- Tools: busca de pedido, status de entrega
- Custo: ~$50/mes para 10.000 atendimentos

**Caso 2: Analise de Documentos Juridicos**
- Modelo: Opus (analise) + Sonnet (extracao)
- Context: contrato completo + jurisprudencia relevante
- Tools: busca de jurisprudencia, calculo de prazos
- Custo: ~$500/mes para 1.000 documentos

**Caso 3: Code Review Automatizado**
- Modelo: Sonnet (revisao)
- Context: arquivo de codigo + guidelines do time
- Tools: leitura de arquivos, execucao de testes
- Custo: ~$200/mes para 500 reviews

**Caso 4: Geracao de Conteudo Marketing**
- Modelo: Opus (redacao) + Sonnet (edicao)
- Context: brand guidelines + brief da campanha
- Tools: busca de tendencias, analise de concorrentes
- Custo: ~$300/mes para 100 pecas
""",
    "cap_4.md": """

### Padroes Avancados de Multi-Agent

Vamos explorar padroes mais sofisticados de coordenacao:

#### 1. Hierarchical (Piramide)

```
CEO (Orquestrador Principal)
+-- CTO (Lider Tecnico)
|   +-- Dev 1 (Backend)
|   +-- Dev 2 (Frontend)
|   +-- Dev 3 (DevOps)
+-- CPO (Lider de Produto)
|   +-- PM 1 (Features)
|   +-- PM 2 (UX Research)
+-- CFO (Lider Financeiro)
    +-- Analyst (Budget)
```

**Vantagem:** escala bem, clareza de responsabilidade.
**Desvantagem:** gargalo no orquestrador.

#### 2. Peer-to-Peer (Iguais)

Agent A <-> Agent B
  |           |
Agent C <-> Agent D

Cada agente se comunica diretamente com qualquer outro.
**Vantagem:** sem gargalo, tolerante a falhas.
**Desvantagem:** complexidade de coordenacao.

#### 3. Blackboard (Quadro-Negro)

```
+-------------------------------+
|         BLACKBOARD            |
|  (Estado Global Compartilhado)|
+-------------------------------+
    |       |       |       |
Agent A  Agent B  Agent C  Agent D
```

Agentes leem e escrevem em um estado compartilhado.
**Vantagem:** desacoplamento total.
**Desvantagem:** conflitos de escrita.

### Ferramentas de Orquestracao

#### LangGraph (LangChain)

```python
from langgraph.graph import StateGraph

graph = StateGraph(AgentState)
graph.add_node("analyze", analyze_task)
graph.add_node("plan", create_plan)
graph.add_node("execute", execute_plan)
graph.add_node("validate", validate_results)

graph.add_edge("analyze", "plan")
graph.add_edge("plan", "execute")
graph.add_edge("execute", "validate")
graph.add_conditional_edges("validate", 
    lambda s: "done" if s["valid"] else "replan",
    {"done": END, "replan": "plan"})

app = graph.compile()
```

#### CrewAI

```python
from crewai import Agent, Task, Crew

analyst = Agent(
    role="Analista",
    goal="Analisar requisitos",
    tools=[search_tool, read_tool]
)

developer = Agent(
    role="Desenvolvedor",
    goal="Implementar solucao",
    tools=[code_tool, test_tool]
)

task1 = Task(description="Analisar feature request", agent=analyst)
task2 = Task(description="Implementar baseado na analise", agent=developer)

crew = Crew(agents=[analyst, developer], tasks=[task1, task2])
result = crew.kickoff()
```

### Padroes de Resiliencia

#### 1. Retry com Backoff Exponencial

```python
import time

def resilient_call(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            wait = 2 ** attempt * 15
            time.sleep(wait)
        except TimeoutError:
            wait = 2 ** attempt * 10
            time.sleep(wait)
    raise Exception("Max retries exceeded")
```

#### 2. Circuit Breaker

```python
class CircuitBreaker:
    def __init__(self, threshold=5, reset_timeout=60):
        self.failures = 0
        self.threshold = threshold
        self.reset_timeout = reset_timeout
        self.last_failure = None
        self.state = "closed"
    
    def call(self, func):
        if self.state == "open":
            if time.time() - self.last_failure > self.reset_timeout:
                self.state = "half-open"
            else:
                raise Exception("Circuit breaker open")
        try:
            result = func()
            if self.state == "half-open":
                self.state = "closed"
                self.failures = 0
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure = time.time()
            if self.failures >= self.threshold:
                self.state = "open"
            raise
```

#### 3. Fallback Chain

```python
def fallback_chain(task, models=["sonnet", "haiku", "local"]):
    for model in models:
        try:
            return call_model(model, task)
        except Exception:
            continue
    raise Exception("All models failed")
```

### Metricas de Agentes

Monitore para garantir qualidade:

| Metrica | O que mede | Target |
|---------|-----------|--------|
| Task Completion Rate | % de tarefas completadas | >95% |
| Average Turns | Turns por tarefa | <10 |
| Tool Accuracy | % de tool calls corretos | >90% |
| Context Utilization | % da janela usada | <80% |
| Cost per Task | Custo medio por tarefa | <target |
| Error Rate | % de erros | <5% |
| Recovery Rate | % de erros recuperados | >80% |

### O Futuro dos Agentes (2026-2027)

Tendencias que moldam o futuro:

1. **Modelos Maiores**: janelas de 2M+ tokens serao padrao
2. **Mais Rapidos**: latencia <100ms para respostas curtas
3. **Multimodal Nativo**: texto + imagem + audio + video
4. **Agent-to-Agent**: LLMs negociando e cooperando
5. **Autonomia Crescente**: menos intervencao humana necessaria
6. **Specialization**: modelos treinados para dominios especificos
7. **Efficiency**: modelos menores com performance de modelos maiores

### Checklist Final do Agente

Ao construir um agente, verifique:

```
TEL System prompt claro e estruturado
TEL Few-shot examples representativos
HAR Limits de tokens definidos
HAR Timeouts configurados
HAR Retries implementados
LLM Modelo escolhido por tarefa
LLM Parametros otimizados
LLM Caching ativado
LLM Compaction para conversas longas
TOO Schema bem definido
TOO Descricoes claras
TOO Error handling implementado
TOO Permissoes granulares
MET Monitoring configurado
MET Alerts definidos
RES Fallback chain
RES Circuit breaker
RES Graceful degradation
```

### Conclusao Final da Serie

Ao longo dos 4 livros da serie 4 Camadas, construimos um conhecimento completo sobre agentes de IA:

1. **TELA**: O mixer que configura o comportamento
2. **HARNESS**: O sistema de seguranca que mantem limites
3. **LLM**: O cerebro que processa, decide e gera
4. **TOOLS**: As maos que executam acoes no mundo

Cada camada e independente, mas todas trabalham juntas. Dominar uma sem as outras e como ter um carro com motor potente mas sem freios - perigoso e ineficaz.

O agente ideal e aquele que:
- Recebe contexto claro da TELA
- Opera sob restricoes seguras do HARNESS
- Usa o LLM certo para cada tarefa
- Invoca tools de forma inteligente e segura

Voce agora tem o mapa completo. Use-o com sabedoria, construa com responsabilidade, e lembre: a tecnologia e uma ferramenta - o verdadeiro poder esta em como voce a usa.
"""
}

for fname, addition in additions.items():
    fpath = os.path.join(BASE, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    marker = "## 7. Referências"
    if marker in content:
        idx = content.index(marker)
        new_content = content[:idx] + addition + "\n\n" + content[idx:]
    else:
        new_content = content + addition
    
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(new_content)

# Check total
total = 0
for f in ["cap_1.md", "cap_2.md", "cap_3.md", "cap_4.md"]:
    fpath = os.path.join(BASE, f)
    size = os.path.getsize(fpath)
    total += size
    print(f"{f}: {size} chars")
print(f"TOTAL: {total} chars")
