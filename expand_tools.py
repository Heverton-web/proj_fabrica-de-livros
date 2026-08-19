#!/usr/bin/env python3
"""Expand TOOLS book chapters to 100k chars."""
import os

BASE = "output/tela-camada-agente/livros/tools-quarta-camada/capitulos"

additions = {
    "cap_1.md": """

### Evolucao das Tools: De APIs a MCP

A forma como nos conectamos a sistemas externos evoluiu dramaticamente:

| Epoca | Abordagem | Limitacao |
|-------|-----------|-----------|
| 2020 | APIs REST customizadas | Cada integracao unica |
| 2022 | Function Calling (OpenAI) | Lock-in de plataforma |
| 2024 | MCP (Anthropic) | Padrao aberto, multi-cliente |
| 2026 | MCP v2 + Tools nativas | Integracao universal |

O MCP representou um salto quantico — de integrações one-off para um ecossistema padronizado.

### Classificacao de Tools

Tools podem ser classificadas por several criterios:

**Por Tipo de Acao:**
| Tipo | Exemplo | Side Effects |
|------|---------|--------------|
| Leitura | read_file, search_web | Nao |
| Escrita | write_file, send_email | Sim |
| Computacao | calculate, transform | Nao |
| Integracao | update_crm, create_ticket | Sim |
| Navegacao | click_element, scroll | Sim |

**Por Fonte de Dados:**
| Fonte | Exemplo | Latencia |
|-------|---------|----------|
| Local | read_file, execute_code | Baixa |
| API Externa | search_web, fetch_url | Media |
| Database | query_sql, get_record | Media |
| Browser | screenshot, click | Alta |

**Por Seguranca:**
| Nivel | Exemplo | Permissao |
|-------|---------|-----------|
| Publico | search_web | Qualquer um |
| Autenticado | get_user_data | Usuario logado |
| Privilegiado | delete_account | Admin |
| Critico | execute_transfer | Auditoria obrigatoria |

### O Papel das Tools no Ciclo de Vida do Agente

```
Inicializacao → Selecao → Execucao → Observacao → Decisao → (repete)
     |              |          |           |            |
     v              v          v           v            v
  Carregar      Escolher   Rodar tool  Receber      Continuar
  catalogo      tool certa  externa    resultado    ou parar
```

Cada fase tem requisitos diferentes:
- **Inicializacao**: catalogo de tools disponiveis no contexto
- **Selecao**: LLM analisa descricao e escolhe tool correta
- **Execucao**: runtime valida input e executa
- **Observacao**: resultado e alimentado de volta no contexto
- **Decisao**: LLM decide se precisa de mais tools

### Metricas de Tool Use

Como medir a eficacia do uso de tools:

| Metrica | O que mede | Target |
|---------|-----------|--------|
| Tool Accuracy | % de tools escolhidas corretamente | >90% |
| Tool Efficiency | Tools chamadas / tarefas completadas | <3 |
| Error Rate | % de tools que falham | <5% |
| Latencia Media | Tempo medio por tool call | <2s |
| Custo por Tool | Custo medio por chamada | <target |

### Ferramentas de Desenvolvimento

Para desenvolver e testar tools:

**Local:**
- MCP Inspector: interface visual para testar servidores MCP
- Postman/Insomnia: testar APIs REST
- pytest: testes unitarios para tools

**Producao:**
- OpenTelemetry: tracing distribuido
- Grafana: dashboards de monitoramento
- Sentry: error tracking

**Documentacao:**
- Swagger/OpenAPI: documentacao de APIs
- MCP Spec: especificacao do protocolo
- README claro: instrucoes de uso

### Casos de Uso Reais

**Caso 1: E-commerce**
- Tools: search_product, add_to_cart, process_payment, track_order
- Padrão: Router (classifica intent, escolhe tool)
- Resultado: 40% redução no tempo de atendimento

**Caso 2: Fintech**
- Tools: check_balance, transfer_funds, get_statement, block_card
- Padrão: ReAct (transparencia em operacoes financeiras)
- Resultado: 60% automacao de consultas

**Caso 3: Healthcare**
- Tools: search_symptoms, check_appointments, get_lab_results
- Padrão: Planner-Execute (planejamento cuidadoso)
- Resultado: 30% reducao no tempo de triagem
""",
    "cap_2.md": """

### MCP vs Alternativas

Comparacao do MCP com outras abordagens:

| Abordagem | Padrao | Multi-Client | Complexidade |
|-----------|--------|--------------|--------------|
| MCP | Aberto | Sim | Media |
| Function Calling | Fechado (por provider) | Nao | Baixa |
| LangChain Tools | Framework | Via integracao | Alta |
| API REST | Universal | Sim | Baixa |

**Quando usar MCP:**
- Multi-cliente (Claude + Cursor + outros)
- Ecossistema de servers compartilhados
- Padronizacao de integracoes

**Quando NAO usar MCP:**
- Integracao unica (so um client)
- Prototipo rapido
- Time sem experiencia em protocolos

### Transportes em Detalhe

#### stdio (Standard Input/Output)

```python
# Server rodando como subprocess
import subprocess
import json

process = subprocess.Popen(
    ["python", "my_server.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)

# Enviar requisicao
request = json.dumps({
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {"name": "search", "args": {"query": "test"}},
    "id": 1
})
process.stdin.write(request + "\\n")
process.stdin.flush()

# Ler resposta
response = process.stdout.readline()
```

**Vantagens:** simples, sem rede, rapido.
**Desvantagens:** local apenas, sem autenticacao.

#### SSE (Server-Sent Events)

```python
# Server com SSE
from fastapi import FastAPI
from sse_starlette.sse import EventSourceResponse

app = FastAPI()

@app.get("/mcp")
async def mcp_endpoint():
    async def event_generator():
        while True:
            # Processar requisicoes MCP
            request = await get_next_request()
            response = await process_request(request)
            yield {"event": "message", "data": json.dumps(response)}
    
    return EventSourceResponse(event_generator())
```

**Vantagens:** remoto, streaming, HTTP padrao.
**Desvantagens:** unidirecional (server → client).

#### Streamable HTTP

```python
# Novo padrao 2026 - bidirecional
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/mcp")
async def mcp_endpoint(request: Request):
    body = await request.json()
    
    # Processar e retornar streaming
    async def process_stream():
        async for chunk in process_request_streaming(body):
            yield json.dumps(chunk) + "\\n"
    
    return StreamingResponse(process_stream())
```

**Vantagens:** bidirecional, streaming, producao.
**Desvantagens:** mais complexo.

### Seguranca em Profundidade

Camadas de seguranca para MCP:

```
┌─────────────────────────────────────┐
│  Camada 1: Autenticacao            │
│  API keys, OAuth, tokens           │
├─────────────────────────────────────┤
│  Camada 2: Autorizacao             │
│  Permissoes por tool/usuario       │
├─────────────────────────────────────┤
│  Camada 3: Rate Limiting           │
│  Controle de taxa por IP/usuario   │
├─────────────────────────────────────┤
│  Camada 4: Validacao               │
│  Input sanitization, output check  │
├─────────────────────────────────────┤
│  Camada 5: Audit                   │
│  Log de todas as chamadas          │
└─────────────────────────────────────┘
```

### Erros Comuns em MCP

1. **Credenciais em texto plano**: nunca faca isso
   - Fix: usar variaveis de ambiente

2. **Sem validacao de input**: server aceita qualquer coisa
   - Fix: Pydantic/JSON Schema para validacao

3. **Sem rate limiting**: server sobrecarregado
   - Fix: limitar chamadas por periodo

4. **Sem tratamento de erros**: server crasha
   - Fix: try/except com erros claros

5. **Sem logging**: impossivel debugar
   - Fix: audit log estruturado

### Exemplos de MCP Servers Populares

**GitHub MCP Server:**
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_..."
      }
    }
  }
}
```

**PostgreSQL MCP Server:**
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
    }
  }
}
```

**Filesystem MCP Server:**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
    }
  }
}
```
""",
    "cap_3.md": """

### Padroes de Nomenclatura Avancados

Além do basico (verbo_substantivo), existem padroes para contextos especificos:

**Para CRUD:**
- `create_resource`
- `read_resource`
- `update_resource`
- `delete_resource`

**Para Busca:**
- `search_<domain>` (busca ampla)
- `find_<domain>_by_<criteria>` (busca especifica)
- `get_<domain>_count` (contagem)

**Para Notificacao:**
- `send_<channel>_message` (email, slack, sms)
- `notify_<event>` (notificacao generica)

**Para Computacao:**
- `calculate_<operation>`
- `transform_<input>_to_<output>`
- `validate_<data_type>`

### Descricoes Niveis de Detalhe

**Nivel 1 - Minimo (ruim):**
```
"Busca dados"
```

**Nivel 2 - Basico (aceitavel):**
```
"Busca informacoes na web"
```

**Nivel 3 - Completo (bom):**
```
"Busca informacoes na web usando Google Search. Use quando precisar de dados atualizados ou informacoes que nao estao no contexto do agente. Nao use para busca em bases de dados internas ou para consultas que podem ser respondidas com dados ja disponiveis. Retorna lista de resultados com titulo, URL e snippet."
```

**Nivel 4 - Experto (otimo):**
```
"Busca informacoes na web usando Google Search API. Use quando: (1) precisa de dados em tempo real, (2) informacao nao esta no contexto, (3) precisa de fontes externas. Nao use quando: (1) dados ja estao disponiveis, (2) busca e em base interna, (3) query e muito vaga. Retorna: lista de ate N resultados com titulo, URL, snippet e data de publicacao. Limite: 100 buscas/minuto por API key."
```

### Schema Design Avancado

**Propriedades Computadas:**
```json
{
  "properties": {
    "start_date": {"type": "string", "format": "date"},
    "end_date": {"type": "string", "format": "date"},
    "duration_days": {
      "type": "integer",
      "description": "Calculado automaticamente: end_date - start_date"
    }
  }
}
```

**Schemas Condicionais:**
```json
{
  "properties": {
    "type": {"type": "string", "enum": ["email", "sms", "push"]},
    "email": {"type": "string", "format": "email"},
    "phone": {"type": "string", "pattern": "^\\\\+?[1-9]\\\\d{1,14}$"},
    "push_token": {"type": "string"}
  },
  "dependencies": {
    "email": ["type"],
    "phone": ["type"],
    "push_token": ["type"]
  }
}
```

### Testes de Tools

**Teste Unitario:**
```python
def test_search_web():
    result = search_web("python programming")
    assert result["status"] == "success"
    assert len(result["results"]) > 0
    assert all("title" in r for r in result["results"])

def test_search_web_invalid_query():
    result = search_web("")
    assert result["status"] == "error"
    assert "query" in result["message"].lower()
```

**Teste de Integracao:**
```python
def test_mcp_server_integration():
    # Iniciar server
    server = start_mcp_server()
    
    # Conectar client
    client = MCPClient(server.endpoint)
    
    # Chamar tool
    result = client.call_tool("search", {"query": "test"})
    
    # Verificar
    assert result is not None
    server.stop()
```

**Teste de Carga:**
```python
import concurrent.futures

def test_concurrent_tool_calls():
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(search_web, f"query_{i}")
            for i in range(100)
        ]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
    successes = sum(1 for r in results if r["status"] == "success")
    assert successes >= 95  # 95% success rate
```

### Monitoreamento de Tools em Producao

**Dashboard de Metricas:**
```
+-------------------+-------------------+
| Tool Calls/min    | Error Rate        |
| 1,234             | 2.3%              |
+-------------------+-------------------+
| Latencia Media    | Custo/hora        |
| 450ms             | $0.12             |
+-------------------+-------------------+
| Top Tools         | Tools com Erro    |
| 1. search_web: 45%| 1. send_email: 5% |
| 2. read_file: 30% | 2. deploy: 3%     |
| 3. query_db: 25%  |                   |
+-------------------+-------------------+
```

**Alertas:**
- Error rate > 5%: alerta critico
- Latencia > 5s: alerta de performance
- Custo > $1/hora: alerta de budget
- Tool nao usada em 7 dias: candidata a remocao
""",
    "cap_4.md": """

### Padrões de Resiliência em Tool Use

**Circuit Breaker Pattern:**
```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.last_failure_time = None
        self.state = "closed"
    
    def call(self, func, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.reset_timeout:
                self.state = "half-open"
            else:
                raise Exception("Circuit breaker is open")
        
        try:
            result = func(*args, **kwargs)
            if self.state == "half-open":
                self.state = "closed"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
            raise
```

**Retry with Exponential Backoff:**
```python
import time
import random

def retry_with_backoff(func, max_retries=3, base_delay=1, max_delay=60):
    def wrapper(*args, **kwargs):
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                delay = min(base_delay * (2 ** attempt) + random.uniform(0, 1), max_delay)
                time.sleep(delay)
    return wrapper
```

**Bulkhead Pattern:**
```python
import threading
from collections import defaultdict

class Bulkhead:
    def __init__(self, max_concurrent_per_tool=10):
        self.semaphores = defaultdict(lambda: threading.Semaphore(max_concurrent_per_tool))
    
    def execute(self, tool_name, func, *args, **kwargs):
        sem = self.semaphores[tool_name]
        if not sem.acquire(blocking=False):
            raise Exception(f"Too many concurrent calls to {tool_name}")
        try:
            return func(*args, **kwargs)
        finally:
            sem.release()
```

### Observabilidade Completa

**Distributed Tracing com OpenTelemetry:**
```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanExporter

provider = TracerProvider()
processor = BatchSpanExporter()
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

def tool_with_tracing(tool_name, func, *args, **kwargs):
    with tracer.start_as_current_span(f"tool.{tool_name}") as span:
        span.set_attribute("tool.name", tool_name)
        span.set_attribute("tool.args", str(args)[:500])
        
        try:
            result = func(*args, **kwargs)
            span.set_attribute("tool.status", "success")
            return result
        except Exception as e:
            span.set_attribute("tool.status", "error")
            span.set_attribute("tool.error", str(e))
            raise
```

**Structured Logging:**
```python
import structlog

logger = structlog.get_logger()

def tool_with_logging(tool_name, func, *args, **kwargs):
    log = logger.bind(tool=tool_name, args=str(args)[:200])
    
    log.info("tool.start")
    start_time = time.time()
    
    try:
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        log.info("tool.success", duration=duration, result_size=len(str(result)))
        return result
    except Exception as e:
        duration = time.time() - start_time
        log.error("tool.error", duration=duration, error=str(e))
        raise
```

### Multi-Agent Tool Sharing

Quando multiplos agentes compartilham tools:

```python
class ToolRegistry:
    def __init__(self):
        self.tools = {}
        self.permissions = {}
    
    def register(self, name, func, permissions=None):
        self.tools[name] = func
        self.permissions[name] = permissions or ["read"]
    
    def call(self, agent_id, tool_name, *args, **kwargs):
        # Verificar permissao
        if not self.has_permission(agent_id, tool_name):
            raise PermissionError(f"Agent {agent_id} not allowed to use {tool_name}")
        
        # Verificar rate limit
        if self.is_rate_limited(agent_id, tool_name):
            raise Exception("Rate limit exceeded")
        
        # Executar com tracing
        return self.execute_with_tracing(agent_id, tool_name, *args, **kwargs)
    
    def has_permission(self, agent_id, tool_name):
        # Implementar logica de permissao
        return True
    
    def is_rate_limited(self, agent_id, tool_name):
        # Implementar rate limiting
        return False
```

### Checklist Final de Tool Use

```
DESIGN
[ ] Nome claro (verbo_substantivo)
[ ] Descricao completa (o que, quando, quando nao)
[ ] Schema com defaults e validacao
[ ] Tratamento de erros implementado
[ ] Documentacao atualizada

SEGURANCA
[ ] Credenciais em env vars
[ ] Rate limiting configurado
[ ] Input sanitization ativo
[ ] Audit logging habilitado
[ ] Permissoes granulares

PERFORMANCE
[ ] Cache para tools lentas
[ ] Timeout configurado
[ ] Retry com backoff
[ ] Bulkhead para concorrencia
[ ] Circuit breaker ativo

MONITORAMENTO
[ ] Tracing distribuido
[ ] Metricas de uso
[ ] Alertas configurados
[ ] Dashboard funcional
[ ] Logs estruturados

TESTES
[ ] Unit tests passando
[ ] Integration tests passando
[ ] Load test executado
[ ] Chaos engineering testado
[ ] Security audit completo
```

### O Futuro das Tools (2027-2028)

Tendencias:

1. **Tools Autônomas**: agentes criando suas proprias tools
2. **Composicao**: tools que combinam automaticamente
3. **Aprendizado**: tools que melhoram com uso
4. **Seguranca Zero-Trust**: verificacao em cada chamada
5. **Edge Computing**: tools rodando no dispositivo
6. **Multimodal**: tools que processam texto + imagem + audio
7. **Federated**: tools distribuidas em multiplos servidores

### Conclusao Final da Serie

Ao longo dos 4 livros da serie 4 Camadas, construimos um conhecimento completo sobre agentes de IA:

1. **TELA**: O mixer que configura o comportamento
2. **HARNESS**: O sistema de seguranca que mantem limites
3. **LLM**: O cerebro que processa, decide e gera
4. **TOOLS**: As maos que executam acoes no mundo

Cada camada e independente, mas todas trabalham juntas. Dominar uma sem as outras e incompleto.

Parabéns por completar a serie! Agora voce tem o mapa completo para construir agentes de IA robustos, eficientes e seguros. Use esse conhecimento com sabedoria e responsabilidade.
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

total = 0
for f in ["cap_1.md", "cap_2.md", "cap_3.md", "cap_4.md"]:
    fpath = os.path.join(BASE, f)
    size = os.path.getsize(fpath)
    total += size
    print(f"{f}: {size} chars")
print(f"TOTAL: {total} chars")
