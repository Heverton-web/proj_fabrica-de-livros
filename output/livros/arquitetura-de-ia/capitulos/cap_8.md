## 8. Arquitetura Avançada: Escalando o Sistema

### 8.1 Introdução

Neste último capítulo, vamos transformar nosso assistente de IA funcional em um **sistema de produção escalável**. Nos capítulos anteriores, construímos cada componente individualmente. Agora, vamos conectá-los com uma arquitetura que suporta:

- **Milhares de usuários** simultâneos
- **Múltiplos modelos** com fallback automático
- **Cache inteligente** para reduzir custos
- **Multi-tenancy** para isolamento de clientes
- **Orquestração** de pipelines complexos

**O que você vai construir:**
- Orquestrador de modelos com fallback
- Cache de respostas semântico
- Sistema multi-tenant completo
- Pipeline de processamento avançado
- Otimização de custos

**Por que esta arquitetura importa:**
- Sistemas reais não usam um único modelo
- Cada centavo conta quando você processa milhões de requisições
- Isolamento de dados é obrigatório em enterprise
- Fallback garante disponibilidade mesmo com falhas

### 8.2 Explica

#### Padrões de Arquitetura Avançada

A Microsoft identificou padrões comuns em sistemas de IA em produção [1]:

**1. Gateway Pattern:** Um gateway roteia requisições para múltiplos backends de modelo. Benefícios:
- Balanceamento de carga
- Cache centralizado
- Rate limiting unificado
- Observabilidade consolidada

**2. Circuit Breaker Pattern:** Quando um modelo falha, o sistema automaticamente muda para outro. Benefícios:
- Disponibilidade mesmo com falhas
- Degradção graciosa
- Prevenção de cascata de falhas

**3. Strangler Fig Pattern:** Migrar gradualmente de um modelo para outro. Benefícios:
- Zero downtime
- Rollback fácil
- Comparação A/B em produção

#### Cache Semântico

Cache tradicional usa chaves exatas. Cache semântico usa **similaridade** [2]:

```
Cache tradicional:
  Chave: "O que é Python?" → Valor: "Python é uma linguagem..."
  Query: "O que é a linguagem Python?" → CACHE MISS ❌

Cache semântico:
  Query: "O que é a linguagem Python?" → Embedding similar → CACHE HIT ✅
```

**Como funciona:**
1. Cada pergunta é convertida em embedding
2. Antes de chamar a IA, busca no cache por similaridade
3. Se encontrar algo similar o suficiente (cosine > 0.95), retorna a resposta cacheada
4. Se não, chama a IA e salva no cache

**Economia típica:** 30-50% de redução em chamadas à API

#### Multi-Tenancy

Multi-tenancy permite que múltiplos clientes usem o mesmo sistema com dados isolados [3]:

```
Tenant A (Empresa X):
  - Seus documentos no RAG
  - Seus dados de conversa
  - Seus limites de uso
  - Seus modelos configurados

Tenant B (Empresa Y):
  - Seus documentos (separados)
  - Seus dados (separados)
  - Seus limites
  - Seus modelos
```

**Níveis de multi-tenancy:**

| Nível | Isolamento | Custo | Complexidade |
|-------|------------|-------|--------------|
| Shared DB, Shared Schema | Baixo | Baixo | Baixa |
| Shared DB, Separate Schema | Médio | Médio | Média |
| Separate Database | Alto | Alto | Alta |
| Separate Infrastructure | Máximo | Máximo | Máxima |

Para a maioria dos casos, **Shared DB com Row-Level Security** é suficiente.

#### Orquestração de Modelos

Em produção, você não usa um único modelo. Usa múltiplos para diferentes tarefas [4]:

```
Pergunta simples → DeepSeek-V4-Flash (barato, rápido)
Pergunta complexa → DeepSeek-V4-Pro (caro, preciso)
Raciocínio → DeepSeek-R1 (thinking model)
Código → DeepSeek-Coder (especializado)
```

O orquestrador decide qual modelo usar baseado em:
- Tipo de tarefa
- Complexidade estimada
- Custo disponível
- Disponibilidade do modelo

### 8.3 Ilustra

#### Orquestrador de Modelos

```python
# architecture/orchestrator.py
"""
Orquestrador de modelos com fallback e routing inteligente.
"""
from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
from src.client import IAClient

class ModelTier(Enum):
    """Hierarquia de modelos por custo/qualidade."""
    FLASH = "flash"      # Barato, rápido
    PRO = "pro"          # Padrão
    PREMIUM = "premium"  # Caro,高质量
    REASONING = "reasoning"  # Raciocínio

@dataclass
class ModelConfig:
    """Configuração de um modelo."""
    name: str
    tier: ModelTier
    cost_per_1k_tokens: float
    max_tokens: int
    supports_streaming: bool = True

class ModelOrchestrator:
    """Orquestra múltiplos modelos com fallback."""
    
    def __init__(self):
        self.models: Dict[str, IAClient] = {}
        self.configs: Dict[str, ModelConfig] = {}
        self.fallback_chain: List[str] = []
    
    def registrar_modelo(self, nome: str, client: IAClient, config: ModelConfig):
        """Registra um modelo disponível."""
        self.models[nome] = client
        self.configs[nome] = config
    
    def definir_fallback(self, chain: List[str]):
        """Define a cadeia de fallback (do mais barato ao mais caro)."""
        self.fallback_chain = chain
    
    def selecionar_modelo(self, complexidade: str = "baixa", 
                          custo_maximo: float = None) -> str:
        """Seleciona o melhor modelo para a tarefa."""
        for nome in self.fallback_chain:
            config = self.configs[nome]
            
            # Verificar custo
            if custo_maximo and config.cost_per_1k_tokens > custo_maximo:
                continue
            
            # Verificar complexidade
            if complexidade == "alta" and config.tier in [ModelTier.FLASH]:
                continue
            
            return nome
        
        # Fallback para o último da cadeia
        return self.fallback_chain[-1] if self.fallback_chain else None
    
    def enviar(self, mensagens: List[Dict], complexidade: str = "baixa",
               custo_maximo: float = None) -> tuple:
        """Envia requisição com fallback automático."""
        modelo_selecionado = self.selecionar_modelo(complexidade, custo_maximo)
        
        if not modelo_selecionado:
            raise Exception("Nenhum modelo disponível")
        
        # Tentar com o modelo selecionado
        for modelo_nome in self.fallback_chain[self.fallback_chain.index(modelo_selecionado):]:
            try:
                client = self.models[modelo_nome]
                resposta, metricas = client.enviar(mensagens)
                metricas["modelo_usado"] = modelo_nome
                return resposta, metricas
            except Exception as e:
                print(f"Modelo {modelo_nome} falhou: {e}")
                continue
        
        raise Exception("Todos os modelos falharam")
```

#### Cache Semântico

```python
# architecture/cache.py
"""
Cache semântico para respostas de IA.
"""
import json
import time
from typing import Optional, Dict, List
from pathlib import Path
import chromadb
from rag.embedder import Embedder

class SemanticCache:
    """Cache que usa similaridade semântica em vez de chaves exatas."""
    
    def __init__(self, persist_dir: str = "./data/cache", 
                 similarity_threshold: float = 0.95,
                 ttl_seconds: int = 3600):
        """
        Args:
            similarity_threshold: Limiar de similaridade para cache hit
            ttl_seconds: Tempo de vida do cache
        """
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.embedder = Embedder()
        self.threshold = similarity_threshold
        self.ttl = ttl_seconds
        
        self.collection = self.client.get_or_create_collection(
            name="response_cache",
            metadata={"hnsw:space": "cosine"}
        )
    
    def buscar(self, pergunta: str) -> Optional[Dict]:
        """Busca no cache por similaridade."""
        # Embedding da pergunta
        embedding = self.embedder.embed_texto(pergunta)
        
        # Buscar no cache
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=1,
        )
        
        if not results["documents"][0]:
            return None
        
        # Verificar similaridade
        distance = results["distances"][0][0]
        similarity = 1 - distance  # Converter distância para similaridade
        
        if similarity < self.threshold:
            return None
        
        # Verificar TTL
        metadata = results["metadatas"][0][0]
        timestamp = metadata.get("timestamp", 0)
        if time.time() - timestamp > self.ttl:
            return None
        
        return {
            "resposta": results["documents"][0][0],
            "metadata": metadata,
            "similarity": similarity,
        }
    
    def salvar(self, pergunta: str, resposta: str, metadata: Dict = None):
        """Salva uma resposta no cache."""
        embedding = self.embedder.embed_texto(pergunta)
        
        cache_metadata = {
            "timestamp": time.time(),
            "pergunta": pergunta[:200],  # Salvar preview
            **(metadata or {}),
        }
        
        # Usar hash da pergunta como ID
        import hashlib
        cache_id = hashlib.md5(pergunta.encode()).hexdigest()
        
        self.collection.upsert(
            documents=[resposta],
            embeddings=[embedding],
            ids=[cache_id],
            metadatas=[cache_metadata],
        )
    
    def estatisticas(self) -> Dict:
        """Retorna estatísticas do cache."""
        return {
            "total_entradas": self.collection.count(),
            "limiar_similaridade": self.threshold,
            "ttl_segundos": self.ttl,
        }
    
    def limpar_expirados(self):
        """Remove entradas expiradas do cache."""
        # Implementação simplificada
        # Em produção, usar jobs periódicos
        pass
```

#### Multi-Tenancy

```python
# architecture/tenant.py
"""
Sistema multi-tenant para isolamento de clientes.
"""
from typing import Dict, Optional
from dataclasses import dataclass
from uuid import UUID

@dataclass
class Tenant:
    """Representa um cliente/tenant."""
    id: UUID
    nome: str
    config: Dict
    limits: Dict
    models: List[str]  # Modelos disponíveis para este tenant

class TenantManager:
    """Gerencia múltiplos tenants."""
    
    def __init__(self):
        self.tenants: Dict[UUID, Tenant] = {}
    
    def criar_tenant(self, nome: str, config: Dict = None, 
                     limits: Dict = None) -> Tenant:
        """Cria um novo tenant."""
        from uuid import uuid4
        
        tenant = Tenant(
            id=uuid4(),
            nome=nome,
            config=config or {},
            limits=limits or {"max_requests": 1000, "max_tokens": 100000},
            models=["deepseek-v4-flash"],  # Padrão
        )
        
        self.tenants[tenant.id] = tenant
        return tenant
    
    def obter_tenant(self, tenant_id: UUID) -> Optional[Tenant]:
        """Obtém um tenant por ID."""
        return self.tenants.get(tenant_id)
    
    def verificar_limite(self, tenant_id: UUID, tipo: str, valor: int) -> bool:
        """Verifica se o tenant pode usar mais recursos."""
        tenant = self.obter_tenant(tenant_id)
        if not tenant:
            return False
        
        limite = tenant.limits.get(f"max_{tipo}", float('inf'))
        return valor < limite
    
    def listar_tenants(self) -> List[Tenant]:
        """Lista todos os tenants."""
        return list(self.tenants.values())

# Middleware de multi-tenancy
class TenantMiddleware:
    """Middleware que extrai o tenant da requisição."""
    
    def __init__(self, tenant_manager: TenantManager):
        self.manager = tenant_manager
    
    async def __call__(self, request, call_next):
        # Extrair tenant do header ou token
        tenant_id = request.headers.get("X-Tenant-ID")
        
        if tenant_id:
            from uuid import UUID
            tenant = self.manager.obter_tenant(UUID(tenant_id))
            if tenant:
                request.state.tenant = tenant
        
        response = await call_next(request)
        return response
```

#### Pipeline de Processamento

```python
# architecture/pipeline.py
"""
Pipeline de processamento avançado.
"""
from typing import List, Dict, Callable
from dataclasses import dataclass

@dataclass
class PipelineStep:
    """Um passo do pipeline."""
    nome: str
    func: Callable
    condicao: Callable = None  # Se True, executa o passo

class ProcessingPipeline:
    """Pipeline configurável de processamento."""
    
    def __init__(self):
        self.steps: List[PipelineStep] = []
    
    def adicionar_passo(self, nome: str, func: Callable, 
                        condicao: Callable = None):
        """Adiciona um passo ao pipeline."""
        self.steps.append(PipelineStep(nome, func, condicao))
    
    def executar(self, contexto: Dict) -> Dict:
        """Executa o pipeline completo."""
        for step in self.steps:
            # Verificar condição
            if step.condicao and not step.condicao(contexto):
                continue
            
            # Executar passo
            resultado = step.func(contexto)
            contexto.update(resultado)
        
        return contexto

# Exemplo de uso
def preprocessar(contexto):
    """Pré-processamento da mensagem."""
    mensagem = contexto["mensagem"]
    mensagem_limpa = mensagem.strip()[:5000]  # Limitar tamanho
    return {"mensagem_limpa": mensagem_limpa}

def verificar_seguranca(contexto):
    """Verificação de segurança."""
    from auth.prompt_guard import PromptGuard
    guard = PromptGuard()
    threat = guard.verificar(contexto["mensagem_limpa"])
    return {"seguro": threat.is_safe, "threats": threat.threats}

def buscar_contexto_rag(contexto):
    """Busca contexto no RAG."""
    if not contexto.get("seguro", True):
        return {"contexto_rag": ""}
    
    # Lógica de busca RAG
    return {"contexto_rag": "contexto encontrado"}

def gerar_resposta(contexto):
    """Gera resposta usando IA."""
    # Lógica de geração
    return {"resposta": "resposta gerada"}

# Pipeline padrão
pipeline_padrao = ProcessingPipeline()
pipeline_padrao.adicionar_passo("preprocessar", preprocessar)
pipeline_padrao.adicionar_passo("seguranca", verificar_seguranca)
pipeline_padrao.adicionar_passo("rag", buscar_contexto_rag, 
                                 lambda ctx: ctx.get("seguro", True))
pipeline_padrao.adicionar_passo("resposta", gerar_resposta)
```

#### Otimização de Custos

```python
# architecture/cost_optimizer.py
"""
Otimizador de custos para chamadas de IA.
"""
from dataclasses import dataclass
from typing import Dict

@dataclass
class CustoModelo:
    """Custo por modelo."""
    input_per_1k: float
    output_per_1k: float

class CostOptimizer:
    """Otimiza escolha de modelos por custo."""
    
    def __init__(self):
        self.costs: Dict[str, CustoModelo] = {
            "deepseek-v4-flash": CustoModelo(input_per_1k=0.27, output_per_1k=1.10),
            "deepseek-v4-pro": CustoModelo(input_per_1k=0.54, output_per_1k=2.19),
        }
        self.budget_diario: float = 100.0  # USD
        self.gasto_hoje: float = 0.0
    
    def estimar_custo(self, modelo: str, input_tokens: int, 
                      output_tokens: int) -> float:
        """Estima o custo de uma requisição."""
        if modelo not in self.costs:
            return 0.0
        
        custo = self.costs[modelo]
        return (input_tokens / 1000 * custo.input_per_1k + 
                output_tokens / 1000 * custo.output_per_1k)
    
    def pode_usar_modelo(self, modelo: str, input_tokens: int, 
                         output_tokens: int) -> bool:
        """Verifica se o orçamento permite usar o modelo."""
        custo_estimado = self.estimar_custo(modelo, input_tokens, output_tokens)
        return (self.gasto_hoje + custo_estimado) <= self.budget_diario
    
    def registrar_gasto(self, modelo: str, input_tokens: int, 
                        output_tokens: int):
        """Registra o gasto de uma requisição."""
        custo = self.estimar_custo(modelo, input_tokens, output_tokens)
        self.gasto_hoje += custo
    
    def relatorio(self) -> Dict:
        """Gera relatório de custos."""
        return {
            "budget_diario": self.budget_diario,
            "gasto_hoje": self.gasto_hoje,
            "restante": self.budget_diario - self.gasto_hoje,
            "percentual_usado": (self.gasto_hoje / self.budget_diario * 100) if self.budget_diario > 0 else 0,
        }
```

### 8.4 Técnica

#### Integração Completa

```python
# architecture/complete_system.py
"""
Sistema completo integrando todos os componentes.
"""
from typing import Dict
from architecture.orchestrator import ModelOrchestrator
from architecture.cache import SemanticCache
from architecture.tenant import TenantManager, Tenant
from architecture.pipeline import ProcessingPipeline
from architecture.cost_optimizer import CostOptimizer

class CompleteSystem:
    """Sistema de IA completo e escalável."""
    
    def __init__(self):
        self.orchestrator = ModelOrchestrator()
        self.cache = SemanticCache()
        self.tenant_manager = TenantManager()
        self.pipeline = ProcessingPipeline()
        self.cost_optimizer = CostOptimizer()
    
    def processar(self, tenant_id: str, pergunta: str) -> Dict:
        """Processa uma requisição completa."""
        # 1. Verificar cache
        cache_hit = self.cache.buscar(pergunta)
        if cache_hit:
            return {
                "resposta": cache_hit["resposta"],
                "fonte": "cache",
                "custo": 0.0,
            }
        
        # 2. Preparar contexto
        contexto = {"mensagem": pergunta, "tenant_id": tenant_id}
        contexto = self.pipeline.executar(contexto)
        
        if not contexto.get("seguro", True):
            return {"erro": "Mensagem bloqueada por segurança"}
        
        # 3. Selecionar modelo
        modelo = self.orchestrator.selecionar_modelo(
            complexidade=contexto.get("complexidade", "baixa")
        )
        
        # 4. Verificar orçamento
        if not self.cost_optimizer.pode_usar_modelo(modelo, len(pergunta), 500):
            modelo = "deepseek-v4-flash"  # Fallback para modelo mais barato
        
        # 5. Gerar resposta
        resposta, metricas = self.orchestrator.enviar(
            [{"role": "user", "content": pergunta}],
            complexidade=contexto.get("complexidade", "baixa")
        )
        
        # 6. Registrar gasto
        self.cost_optimizer.registrar_gasto(
            modelo,
            metricas.get("tokens_entrada", 0),
            metricas.get("tokens_saida", 0),
        )
        
        # 7. Salvar no cache
        self.cache.salvar(pergunta, resposta, {"modelo": modelo})
        
        return {
            "resposta": resposta,
            "fonte": "ia",
            "modelo": modelo,
            "custo": self.cost_optimizer.estimar_custo(
                modelo,
                metricas.get("tokens_entrada", 0),
                metricas.get("tokens_saida", 0),
            ),
            "metricas": metricas,
        }
```

### 8.5 Aplica

#### Checklist Final do Projeto

Ao final deste livro, seu assistente de IA tem:

**Capítulo 1:** Chat básico com API ✓
**Capítulo 2:** Persistência + API REST ✓
**Capítulo 3:** RAG com ChromaDB ✓
**Capítulo 4:** Fine-tuning com LoRA ✓
**Capítulo 5:** Sistema de evals ✓
**Capítulo 6:** Auth + Rate Limiting ✓
**Capítulo 7:** Docker + Monitoramento ✓
**Capítulo 8:** Arquitetura avançada ✓

**Stack completa:**
- Python 3.11+ / FastAPI
- PostgreSQL + Redis
- ChromaDB (vetor)
- OpenAI/DeepSeek API
- Docker + docker-compose
- Prometheus + Grafana
- JWT + OAuth2
- LoRA/QLoRA (fine-tuning)

**Arquitetura:**
```
┌─────────────────────────────────────────────────────────┐
│                    API Gateway                           │
│  (Rate Limiting + Auth + Routing)                        │
├─────────────────────────────────────────────────────────┤
│                    Processing Pipeline                   │
│  (Preprocess → Security → RAG → Response)                │
├─────────────────────────────────────────────────────────┤
│              Model Orchestrator                           │
│  (Flash → Pro → Premium → Reasoning)                     │
├─────────────────────────────────────────────────────────┤
│              Semantic Cache                              │
│  (ChromaDB + Similarity Search)                          │
├─────────────────────────────────────────────────────────┤
│              Data Layer                                  │
│  (PostgreSQL + Redis + ChromaDB)                          │
├─────────────────────────────────────────────────────────┤
│              Monitoring                                  │
│  (Prometheus + Grafana + Structured Logs)                 │
└─────────────────────────────────────────────────────────┘
```

### 8.6 Conclusão

Parabéns! Você construiu um sistema de IA completo e profissional. Cada capítulo adicionou uma camada real ao projeto, e agora você tem:

1. **Conhecimento técnico** para construir sistemas de IA
2. **Arquitetura escalável** que suporta crescimento
3. **Boas práticas** de segurança, monitoramento e custos
4. **Projeto portfolio** que demonstra suas habilidades

**Próximos passos:**
- Deploy em produção real (AWS, GCP, Azure)
- Integração com frontends (React, Next.js)
- Pipelines de CI/CD automatizados
- Contribuição para projetos open-source de IA

Lembre-se: todo grande sistema começa com uma chamada simples que funciona. Você deu o primeiro passo no capítulo 1 e agora tem um sistema completo. Continue construindo!

### 8.7 Referências

[1] Microsoft. "AI Agent Orchestration Patterns." Azure Architecture Center, 2024. Disponível em: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/

[2] Google Cloud. "Caching Strategies for ML Systems." Google Cloud Architecture Center, 2023. Disponível em: https://cloud.google.com/architecture/ml-design-patterns

[3] AWS. "Multi-Tenant Architecture on AWS." Amazon Web Services, 2024. Disponível em: https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/

[4] LangChain. "Model Router Pattern." LangChain Documentation, 2024. Disponível em: https://python.langchain.com/docs/

[5] DeepSeek. "API Documentation." DeepSeek API Docs, 2024. Disponível em: https://api-docs.deepseek.com/

[6] Huyen, Chip. "Designing Machine Learning Systems." O'Reilly Media, 2022. ISBN: 978-1098107963.

[7] Prometheus. "Monitoring Best Practices." Prometheus Documentation, 2024. Disponível em: https://prometheus.io/docs/

[8] Grafana. "Dashboard Design." Grafana Documentation, 2024. Disponível em: https://grafana.com/docs/

[9] Docker. "Containerization Best Practices." Docker Documentation, 2024. Disponível em: https://docs.docker.com/

[10] FastAPI. "Production Deployment." FastAPI Documentation, 2024. Disponível em: https://fastapi.tiangolo.com/deployment/

[11] OWASP. "Top 10 for Large Language Model Applications." OWASP Foundation, 2024. Disponível em: https://owasp.org/www-project-top-10-for-large-language-model-applications/

[12] NIST. "Artificial Intelligence Risk Management Framework." National Institute of Standards and Technology, 2024. Disponível em: https://www.nist.gov/artificial-intelligence/risk-management-framework

[13] Microsoft Azure Architecture Center. "Get Started with AI Architecture Design." Microsoft Learn, 2024. Disponível em: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/ai-get-started

[14] Pinecone. "What is RAG?" Pinecone Learning Center, 2024. Disponível em: https://www.pinecone.io/learn/retrieval-augmented-generation/

[15] OpenAI. "Fine-tuning Guide." OpenAI Platform Documentation, 2024. Disponível em: https://platform.openai.com/docs/guides/fine-tuning

[16] Hugging Face. "PEFT Library." Hugging Face Documentation, 2024. Disponível em: https://huggingface.co/docs/peft

[17] DeepEval. "LLM Evaluation Framework." DeepEval Documentation, 2024. Disponível em: https://docs.confident-ai.com/

[18] RAGAS. "RAG Evaluation Framework." RAGAS Documentation, 2024. Disponível em: https://docs.ragas.io/

[19] Kubernetes. "Production-Grade Container Orchestration." Kubernetes Documentation, 2024. Disponível em: https://kubernetes.io/docs/

[20] Redis. "Redis Documentation." Redis Ltd., 2024. Disponível em: https://redis.io/docs/
