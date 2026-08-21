## 5. Evals e Testing: Qualidade Garantida

### 5.1 Introdução

Nos capítulos anteriores, construímos um assistente de IA completo: chat com persistência, API REST, RAG para conhecimento e fine-tuning para personalização. Mas como ter certeza de que ele funciona **corretamente** antes de colocar em produção?

**Evals (avaliações)** são o processo de testar sistematicamente a qualidade de um sistema de IA [1]. Diferente de testes tradicionais onde "funcionar" significa "não dar erro", em IA "funcionar" significa "gerar respostas úteis, precisas e seguras".

**O que você vai construir:**
- Framework de avaliação automatizada
- Métricas relevantes para sistemas de IA
- Benchmarking contínuo
- CI/CD para qualidade de IA

**Por que evals importam:**
- Um chatbot que responde informações erradas pode causar danos reais
- Regressões de qualidade são difícis de detectar sem evals
- Métricas objetivas substituem "feeling" na avaliação
- Evals automáticos permitem iteração rápida

### 5.2 Explica

#### Por que Testes Tradicionais Não Funcionam para IA

Em software tradicional, um teste verifica se uma função retorna o valor esperado:
```python
# Teste tradicional
def test_soma():
    assert soma(2, 3) == 5  # Sempre retorna 5

# Teste de IA
def test_resposta():
    resposta = assistente.responder("O que é Python?")
    # O que é "correto" aqui? Pode variar!
```

Em IA, a "resposta correta" pode variar dependendo de:
- Contexto da conversa
- Formato esperado
- Nível de detalhe
- Fonte citada
- Tom de voz

Por isso, evals de IA usam **métricas probabilísticas** em vez de asserts exatos [2].

#### Métricas Relevantes para IA

| Métrica | O que mede | Como calcular |
|---------|------------|---------------|
| **Faithfulness** | A resposta é fiel ao contexto? | LLM julga se cada afirmação é suportada |
| **Relevancy** | A resposta é relevante para a pergunta? | LLM julga se a resposta endereça a pergunta |
| **Answer Correctness** | A resposta está factualmente correta? | Comparação com ground truth |
| **Context Precision** | Os documentos recuperados são relevantes? | Precisão dos top-K resultados |
| **Context Recall** | Todos os documentos relevantes foram recuperados? | Recall da recuperação |

#### Framework de Avaliação

Um bom framework de evals tem [3]:

1. **Dataset de teste:** Perguntas com respostas esperadas
2. **Métricas:** Definições objetivas de qualidade
3. **Execução automática:** Roda evals sem intervenção humana
4. **Relatórios:** Visualização clara dos resultados
5. **Alertas:** Notificação quando a qualidade cai

#### Benchmarking Contínuo

Benchmarking não é algo que você faz uma vez — é um processo contínuo [4]:

```
Cada mudança no código → Rodar evals → Comparar com baseline → Decidir se promove
```

Isso é especialmente importante em sistemas de IA porque:
- Modelos de API podem mudar sem aviso
- Dados de treino podem ficar desatualizados
- Novos cenários podem surgir
- Performance pode degradar com o tempo

### 5.3 Ilustra

#### Framework de Evals

```python
# evals/metrics.py
"""
Métricas de avaliação para sistemas de IA.
"""
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum

class MetricType(Enum):
    FAITHFULNESS = "faithfulness"
    RELEVANCY = "relevancy"
    ANSWER_CORRECTNESS = "answer_correctness"
    CONTEXT_PRECISION = "context_precision"
    CONTEXT_RECALL = "context_recall"

@dataclass
class MetricResult:
    """Resultado de uma métrica."""
    tipo: MetricType
    score: float  # 0.0 a 1.0
    detalhes: Dict = field(default_factory=dict)

class MetricCalculator:
    """Calcula métricas de avaliação."""
    
    def __init__(self, llm_client):
        self.client = llm_client
    
    def faithfulness(self, resposta: str, contexto: str) -> MetricResult:
        """
        Mede se a resposta é fiel ao contexto fornecido.
        Cada afirmação na resposta deve ser suportada pelo contexto.
        """
        prompt = """Analise se cada afirmação na RESPOSTA é suportada pelo CONTEXTO.

CONTEXTO:
{contexto}

RESPOSTA:
{resposta}

Para cada afirmação na resposta, indique se é:
- SUPPORTED: afirmação suportada pelo contexto
- NOT_SUPPORTED: afirmação não encontrada no contexto
- CONTRADICTED: afirmação contradiz o contexto

Responda em JSON:
{{
  "afirmacoes": [
    {{"texto": "...", "status": "SUPPORTED|NOT_SUPPORTED|CONTRADICTED"}}
  ],
  "score": 0.0 a 1.0 (proporção de afirmações suportadas)
}}""".format(contexto=contexto, resposta=resposta)
        
        resultado = self.client.enviar([{"role": "user", "content": prompt}])
        
        import json
        try:
            data = json.loads(resultado)
            return MetricResult(
                tipo=MetricType.FAITHFULNESS,
                score=data.get("score", 0.0),
                detalhes=data,
            )
        except json.JSONDecodeError:
            return MetricResult(tipo=MetricType.FAITHFULNESS, score=0.0)
    
    def relevancy(self, pergunta: str, resposta: str) -> MetricResult:
        """Mede se a resposta é relevante para a pergunta."""
        prompt = """Avalie se a resposta é relevante para a pergunta.

PERGUNTA: {pergunta}
RESPOSTA: {resposta}

Dê um score de 0.0 a 1.0:
- 1.0: Resposta completamente relevante
- 0.7: Resposta parcialmente relevante
- 0.3: Resposta pouco relevante
- 0.0: Resposta completamente irrelevante

Responda em JSON: {{"score": 0.0, "justificativa": "..."}}""".format(
            pergunta=pergunta, resposta=resposta
        )
        
        resultado = self.client.enviar([{"role": "user", "content": prompt}])
        
        import json
        try:
            data = json.loads(resultado)
            return MetricResult(
                tipo=MetricType.RELEVANCY,
                score=data.get("score", 0.0),
                detalhes=data,
            )
        except json.JSONDecodeError:
            return MetricResult(tipo=MetricType.RELEVANCY, score=0.0)
    
    def answer_correctness(self, pergunta: str, resposta: str, 
                          ground_truth: str) -> MetricResult:
        """Compara a resposta com a resposta esperada."""
        prompt = """Compare a RESPOSTA com a RESPOSTA ESPERADA.

PERGUNTA: {pergunta}
RESPOSTA: {resposta}
ESPERADA: {ground_truth}

Dê um score de 0.0 a 1.0 baseado em:
- Precisão factual (informações corretas)
- Completude (todas as informações importantes)
- Concisão (sem informações irrelevantes)

Responda em JSON: {{"score": 0.0, "justificativa": "..."}}""".format(
            pergunta=pergunta, resposta=resposta, ground_truth=ground_truth
        )
        
        resultado = self.client.enviar([{"role": "user", "content": prompt}])
        
        import json
        try:
            data = json.loads(resultado)
            return MetricResult(
                tipo=MetricType.ANSWER_CORRECTNESS,
                score=data.get("score", 0.0),
                detalhes=data,
            )
        except json.JSONDecodeError:
            return MetricResult(tipo=MetricType.ANSWER_CORRECTNESS, score=0.0)

    def context_precision(self, query: str, documentos: List[str]) -> MetricResult:
        """Mede a precisão dos documentos recuperados."""
        # Implementação simplificada
        # Em produção, usaria LLM para avaliar relevância de cada doc
        
        n_relevantes = 0
        for doc in documentos[:5]:  # Top 5
            prompt = f"""O documento a seguir é relevante para a query?
            
QUERY: {query}
DOCUMENTO: {doc[:500]}

Responda APENAS com "SIM" ou "NAO"."""
            
            resposta = self.client.enviar([{"role": "user", "content": prompt}])
            if "SIM" in resposta.upper():
                n_relevantes += 1
        
        score = n_relevantes / min(len(documentos), 5) if documentos else 0
        
        return MetricResult(
            tipo=MetricType.CONTEXT_PRECISION,
            score=score,
            detalhes={"documentos_avalaiados": min(len(documentos), 5)},
        )
```

#### Evaluator Automatizado

```python
# evals/evaluator.py
"""
Evaluator que roda múltiplas métricas e gera relatório.
"""
import json
from typing import List, Dict, Optional
from dataclasses import dataclass
from pathlib import Path
from evals.metrics import MetricCalculator, MetricType

@dataclass
class CasoTeste:
    """Um caso de teste para avaliação."""
    pergunta: str
    resposta_esperada: str
    contexto_esperado: Optional[str] = None
    tags: List[str] = None

@dataclass
class ResultadoCaso:
    """Resultado da avaliação de um caso de teste."""
    caso: CasoTeste
    resposta_obtida: str
    metricas: Dict[str, float]
    score_geral: float

class Evaluator:
    """Avalia sistematicamente um sistema de IA."""
    
    def __init__(self, assistente, metric_calculator: MetricCalculator):
        self.assistente = assistente
        self.calculator = metric_calculator
        self.resultados: List[ResultadoCaso] = []
    
    def avaliar_caso(self, caso: CasoTeste) -> ResultadoCaso:
        """Avalia um único caso de teste."""
        # Obter resposta do assistente
        resposta = self.assistente.responder(caso.pergunta)
        
        # Calcular métricas
        metricas = {}
        
        # Faithfulness (se tem contexto)
        if caso.contexto_esperado:
            faith = self.calculator.faithfulness(resposta, caso.contexto_esperado)
            metricas["faithfulness"] = faith.score
        
        # Relevancy
        relev = self.calculator.relevancy(caso.pergunta, resposta)
        metricas["relevancy"] = relev.score
        
        # Answer correctness
        correct = self.calculator.answer_correctness(
            caso.pergunta, resposta, caso.resposta_esperada
        )
        metricas["answer_correctness"] = correct.score
        
        # Score geral (média ponderada)
        pesos = {"faithfulness": 0.3, "relevancy": 0.3, "answer_correctness": 0.4}
        score_geral = sum(metricas.get(k, 0) * v for k, v in pesos.items())
        
        resultado = ResultadoCaso(
            caso=caso,
            resposta_obtida=resposta,
            metricas=metricas,
            score_geral=score_geral,
        )
        
        self.resultados.append(resultado)
        return resultado
    
    def avaliar_dataset(self, casos: List[CasoTeste]) -> Dict:
        """Avalia um dataset completo de casos de teste."""
        for i, caso in enumerate(casos):
            print(f"Avaliando caso {i+1}/{len(casos)}...")
            self.avaliar_caso(caso)
        
        # Calcular métricas agregadas
        scores = [r.score_geral for r in self.resultados]
        
        return {
            "total_casos": len(self.resultados),
            "score_medio": sum(scores) / len(scores) if scores else 0,
            "score_minimo": min(scores) if scores else 0,
            "score_maximo": max(scores) if scores else 0,
            "aprovados": sum(1 for s in scores if s >= 0.7),
            "reprovados": sum(1 for s in scores if s < 0.7),
            "por_metrica": {
                "faithfulness": self._media_metrica("faithfulness"),
                "relevancy": self._media_metrica("relevancy"),
                "answer_correctness": self._media_metrica("answer_correctness"),
            },
        }
    
    def _media_metrica(self, metrica: str) -> float:
        """Calcula a média de uma métrica."""
        scores = [r.metricas.get(metrica, 0) for r in self.resultados]
        return sum(scores) / len(scores) if scores else 0
    
    def gerar_relatorio(self, caminho: str):
        """Gera um relatório detalhado."""
        relatorio = {
            "resumo": self.avaliar_dataset([]),  # Só métricas, sem re-executar
            "detalhes": [
                {
                    "pergunta": r.caso.pergunta,
                    "resposta_esperada": r.caso.resposta_esperada,
                    "resposta_obtida": r.resposta_obtida,
                    "metricas": r.metricas,
                    "score_geral": r.score_geral,
                }
                for r in self.resultados
            ],
        }
        
        Path(caminho).parent.mkdir(parents=True, exist_ok=True)
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(relatorio, f, ensure_ascii=False, indent=2)
        
        print(f"Relatório salvo em: {caminho}")
```

#### Benchmark Runner

```python
# evals/runner.py
"""
Executor de benchmarks que compara versões do sistema.
"""
import json
from typing import Dict, List
from pathlib import Path
from datetime import datetime

class BenchmarkRunner:
    """Executa benchmarks e compara resultados."""
    
    def __init__(self, evaluator):
        self.evaluator = evaluator
        self.benchmarks: List[Dict] = []
    
    def executar_benchmark(self, nome: str, dataset: List) -> Dict:
        """Executa um benchmark e salva o resultado."""
        resultado = self.evaluator.avaliar_dataset(dataset)
        
        benchmark = {
            "nome": nome,
            "timestamp": datetime.now().isoformat(),
            "resultado": resultado,
        }
        
        self.benchmarks.append(benchmark)
        
        # Salvar individual
        caminho = f"evals/benchmarks/{nome}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        Path(caminho).parent.mkdir(parents=True, exist_ok=True)
        with open(caminho, 'w') as f:
            json.dump(benchmark, f, ensure_ascii=False, indent=2)
        
        return benchmark
    
    def comparar_benchmarks(self, benchmark1: Dict, benchmark2: Dict) -> Dict:
        """Compara dois benchmarks."""
        r1 = benchmark1["resultado"]
        r2 = benchmark2["resultado"]
        
        return {
            "benchmark1": benchmark1["nome"],
            "benchmark2": benchmark2["nome"],
            "diferenca_score": r2["score_medio"] - r1["score_medio"],
            "aprovados_antes": r1["aprovados"],
            "aprovados_depois": r2["aprovados"],
            "melhoria": r2["aprovados"] - r1["aprovados"],
        }
    
    def listar_benchmarks(self) -> List[Dict]:
        """Lista todos os benchmarks salvos."""
        caminho = Path("evals/benchmarks")
        if not caminho.exists():
            return []
        
        benchmarks = []
        for arquivo in caminho.glob("*.json"):
            with open(arquivo) as f:
                benchmarks.append(json.load(f))
        
        return sorted(benchmarks, key=lambda x: x["timestamp"])
```

#### Testes do Framework

```python
# tests/test_evals.py
"""
Testes para o framework de avaliação.
"""
import pytest
from unittest.mock import Mock
from evals.metrics import MetricCalculator, MetricType
from evals.evaluator import Evaluator, CasoTeste

@pytest.fixture
def mock_client():
    """Mock do cliente de IA."""
    client = Mock()
    client.enviar.return_value = '{"score": 0.85, "justificativa": "Boa resposta"}'
    return client

@pytest.fixture
def calculator(mock_client):
    return MetricCalculator(mock_client)

@pytest.fixture
def evaluator(mock_client):
    assistente = Mock()
    assistente.responder.return_value = "Python é uma linguagem de programação."
    return Evaluator(assistente, MetricCalculator(mock_client))

def test_relevancy(calculator):
    resultado = calculator.relevancy(
        pergunta="O que é Python?",
        resposta="Python é uma linguagem de programação."
    )
    
    assert resultado.tipo == MetricType.RELEVANCY
    assert 0.0 <= resultado.score <= 1.0

def test_avaliar_caso(evaluator):
    caso = CasoTeste(
        pergunta="O que é Python?",
        resposta_esperada="Linguagem de programação.",
    )
    
    resultado = evaluator.avaliar_caso(caso)
    
    assert resultado.caso == caso
    assert 0.0 <= resultado.score_geral <= 1.0
    assert "relevancy" in resultado.metricas

#### CI/CD para Sistemas de IA

CI/CD (Continuous Integration / Continuous Deployment) para IA é diferente de software tradicional [7]. Além de testar código, você precisa testar **qualidade de respostas**:

```yaml
# .github/workflows/ia-quality.yml
name: IA Quality Gate

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  quality-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run unit tests
        run: pytest tests/ -v
      
      - name: Run evals
        run: |
          python -m evals.runner --dataset evals/datasets/test.jsonl --threshold 0.7
        env:
          DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
      
      - name: Check eval results
        if: failure()
        run: echo "❌ Quality gate failed — evals abaixo do threshold"
```

**Componentes do CI/CD para IA:**

1. **Testes unitários:** Código funciona?
2. **Testes de integração:** Componentes se comunicam?
3. **Evals:** Respostas são de qualidade?
4. **Segurança:** Não há vulnerabilidades?
5. **Performance:** Latência aceitável?
6. **Custo:** Orçamento não estourado?

**Métricas de qualidade no CI:**

| Métrica | Threshold | Ação se falhar |
|---------|-----------|----------------|
| Faithfulness | ≥ 0.8 | Bloquear merge |
| Relevancy | ≥ 0.7 | Bloquear merge |
| Latência P95 | ≤ 2s | Warning |
| Custo por req | ≤ $0.01 | Warning |

**Rollback automático:**
Se os evals caírem após um deploy, o CI deve:
1. Detectar a regressão
2. Notificar o time
3. automaticamente reverter para a versão anterior
4. Criar issue para investigação


#### Criando um Dataset de Teste Robusto

Um bom dataset de teste é a base de evals confiáveis [8]. Aqui está como criá-lo:

**Estrutura do dataset:**
```json
[
  {
    "id": "test-001",
    "pergunta": "O que é Python?",
    "resposta_esperada": "Python é uma linguagem de programação de alto nível, interpretada e de propósito geral.",
    "contexto": "Python foi criado por Guido van Rossum em 1991.",
    "tags": ["conceito-basico", "programacao"],
    "dificuldade": "facil"
  },
  {
    "id": "test-002",
    "pergunta": "Como faço login no sistema?",
    "resposta_esperada": "Para fazer login: 1. Acesse o site 2. Clique em 'Entrar' 3. Insira seu e-mail e senha",
    "contexto": null,
    "tags": ["suporte", "login"],
    "dificuldade": "facil"
  }
]
```

**Dicas para criar bons datasets:**

1. **Diversidade:** Cubra diferentes tipos de perguntas
   - Perguntas factuais ("O que é X?")
   - Perguntas procedimentais ("Como faço Y?")
   - Perguntas de opinião ("O que você acha de Z?")
   - Perguntas impossíveis ("Qual é a senha do banco?")

2. **Casos de borda:**
   - Perguntas vazias ou muito curtas
   - Perguntas muito longas (>5000 chars)
   - Perguntas em outros idiomas
   - Perguntas com erros de digitação

3. **Ground truth:**
   - Respostas devem ser verificáveis
   - Incluir fontes quando relevante
   - Atualizar quando o conhecimento muda

4. **Manutenção:**
   - Revisar trimestralmente
   - Adicionar novos cenários quando surgem bugs
   - Remover testes obsoletos

**Automação de geração de datasets:**
```python
# scripts/gerar_dataset_teste.py
"""
Gera dataset de teste a partir de logs de produção.
"""
import json
from typing import List

def extrair_casos_de_logs(logs: List[Dict]) -> List[Dict]:
    """Extrai casos de teste de logs de produção."""
    casos = []
    
    for log in logs:
        if log.get("satisfacao", 0) >= 4:  # Apenas interações positivas
            casos.append({
                "id": f"prod-{log['id']}",
                "pergunta": log["pergunta"],
                "resposta_esperada": log["resposta"],
                "tags": ["producao"],
                "dificuldade": "media",
            })
    
    return casos
```


#### Métricas Avançadas e Dashboards

Além das métricas básicas, sistemas de IA em produção precisam de métricas avançadas [9]:

**Métricas de negócio:**
- **Satisfação do usuário:** Média de ratings (1-5) após respostas
- **Taxa de resolução:** % de perguntas respondidas sem intervenção humana
- **Tempo para primeira resposta:** Latência percebida pelo usuário
- **Retenção:** Usuários que voltam a usar o assistente

**Métricas de qualidade:**
- **Hallucination rate:** % de respostas com informações inventadas
- **Citation accuracy:** % de respostas com fontes corretas
- **Format compliance:** % de respostas no formato esperado
- **Safety score:** % de respostas que passam no filtro de segurança

**Dashboard de Evals:**
```python
# evals/dashboard.py
"""
Dashboard de métricas de qualidade.
"""
from typing import Dict, List
from datetime import datetime, timedelta

class EvalDashboard:
    """Gera dashboards de métricas de qualidade."""
    
    def __init__(self, evaluator):
        self.evaluator = evaluator
    
    def gerar_dashboard(self, periodo_dias: int = 7) -> Dict:
        """Gera dashboard para o período especificado."""
        # Buscar evals do período
        evals = self._buscar_evals_periodo(periodo_dias)
        
        # Calcular métricas
        metricas = {
            "periodo": f"Últimos {periodo_dias} dias",
            "total_evals": len(evals),
            "score_medio": self._calcular_media(evals),
            "tendencia": self._calcular_tendencia(evals),
            "por_categoria": self._agrupar_por_categoria(evals),
            "alertas": self._detectar_anomalias(evals),
        }
        
        return metricas
    
    def _buscar_evals_periodo(self, dias: int) -> List[Dict]:
        """Busca evals do período."""
        # Implementação simplificada
        return []
    
    def _calcular_media(self, evals: List[Dict]) -> float:
        """Calcula média de scores."""
        if not evals:
            return 0.0
        return sum(e.get("score", 0) for e in evals) / len(evals)
    
    def _calcular_tendencia(self, evals: List[Dict]) -> str:
        """Calcula tendência (crescendo, estável, caindo)."""
        if len(evals) < 2:
            return "insuficiente"
        
        # Comparar primeira e segunda metade
        mid = len(evals) // 2
        primeira = sum(e.get("score", 0) for e in evals[:mid]) / mid
        segunda = sum(e.get("score", 0) for e in evals[mid:]) / (len(evals) - mid)
        
        diff = segunda - primeira
        if diff > 0.05:
            return "crescendo"
        elif diff < -0.05:
            return "caindo"
        return "estavel"
    
    def _agrupar_por_categoria(self, evals: List[Dict]) -> Dict:
        """Agrupa métricas por categoria."""
        categorias = {}
        for e in evals:
            cat = e.get("categoria", "geral")
            if cat not in categorias:
                categorias[cat] = []
            categorias[cat].append(e.get("score", 0))
        
        return {
            cat: sum(scores) / len(scores) if scores else 0
            for cat, scores in categorias.items()
        }
    
    def _detectar_anomalias(self, evals: List[Dict]) -> List[str]:
        """Detecta anomalias nas métricas."""
        alertas = []
        
        # Verificar se score médio caiu muito
        media = self._calcular_media(evals)
        if media < 0.7:
            alertas.append(f"Score médio baixo: {media:.2f}")
        
        # Verificar tendência de queda
        tendencia = self._calcular_tendencia(evals)
        if tendencia == "caindo":
            alertas.append("Tendência de queda detectada")
        
        return alertas
```

**Integração com Slack/Teams:**
```python
# integrations/slack.py
"""
Notificações de evals para Slack.
"""
import requests
from typing import Dict

class SlackNotifier:
    """Envia notificações de qualidade para Slack."""
    
    def __init__(self, webhook_url: str):
        self.webhook = webhook_url
    
    def enviar_alerta(self, titulo: str, mensagem: str, 
                      cor: str = "#ff0000"):
        """Envia alerta formatado para Slack."""
        payload = {
            "attachments": [{
                "color": cor,
                "title": titulo,
                "text": mensagem,
                "footer": "IA Quality Monitor",
            }]
        }
        
        requests.post(self.webhook, json=payload)
    
    def enviar_relatorio_diario(self, dashboard: Dict):
        """Envia relatório diário de qualidade."""
        metricas = dashboard.get("metricas", {})
        
        mensagem = f"""
📊 *Relatório Diário de Qualidade*

*Score Médio:* {metricas.get('score_medio', 0):.2f}
*Tendência:* {metricas.get('tendencia', 'N/A')}
*Total Evals:* {metricas.get('total_evals', 0)}

*Alertas:*
{chr(10).join(dashboard.get('alertas', ['Nenhum']))}
"""
        
        self.enviar_alerta(
            titulo="Relatório Diário de IA",
            mensagem=mensagem,
            cor="#36a64f" if not dashboard.get("alertas") else "#ff9900"
        )
```

