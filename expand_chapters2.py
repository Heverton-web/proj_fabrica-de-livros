#!/usr/bin/env python3
"""Expand LLM book chapters part 2."""
import os

BASE = "output/tela-camada-agente/livros/llm-terceira-camada/capitulos"

additions = {
    "cap_1.md": """

### Guia de Preco por Modelo (Agosto 2026)

Tabela completa de precos para ajudar na decisao:

| Modelo | Input/MTok | Output/MTok | Cache Input/MTok | Context Window |
|--------|-----------|-------------|------------------|----------------|
| Claude Opus 4.8 | $5.00 | $25.00 | $0.50 | 1M |
| Claude Sonnet 5 | $3.00 | $15.00 | $0.30 | 1M |
| Claude Haiku 4.5 | $0.25 | $1.25 | $0.025 | 200K |
| GPT-5.6 | $5.00 | $25.00 | N/A | 1M |
| Gemini 3 Pro | $1.25 | $5.00 | N/A | 2M |
| Llama 4 | Open source | Open source | N/A | 128K |

### Exemplos de Tokens na Pratica

| Conteudo | Tokens Aproximados |
|----------|-------------------|
| Email curto (200 palavras) | ~250 tokens |
| Artigo de blog (1000 palavras) | ~1.300 tokens |
| Capitulo de livro (5000 palavras) | ~6.500 tokens |
| Documento tecnico (10.000 palavras) | ~13.000 tokens |
| Codigo Python (500 linhas) | ~3.000 tokens |
| JSON complexo (1KB) | ~400 tokens |
| System prompt medio | ~500 tokens |

### LLMs e o Mercado Brasileiro

1. **Custo em BRL**: com dolar a R$5.42 (ago/2026), Sonnet a $3.00/MTok custa ~R$16.26/MTok
2. **Tokenizacao PT-BR**: palavras acentuadas gastam mais tokens que equivalentes em ingles
3. **Latencia**: servidores da Anthropic estao na America do Norte
4. **Alternativas Locais**: Llama 4, Mistral, e modelos brasileiros (MARIA, Aya)
5. **Regulacao**: Marco Legal da IA (PL 2338/2023) pode afetar uso em setores regulados

### LLMs no Ecossistema Open Source

| Modelo | Params | Licenca | Melhor Para |
|--------|--------|---------|-------------|
| Llama 4 | 400B | Llama License | Geral |
| Mistral Large | 123B | Apache 2.0 | Europeu, multilingual |
| Qwen 2.5 | 72B | Apache 2.0 | Chines, multimodal |
| DeepSeek V3 | 671B | MIT | Codigo, raciocinio |
| Mixtral | 8x22B | Apache 2.0 | Mixture of Experts |

### A Evolucao do Context Window

| Ano | Modelo | Context Window |
|-----|--------|----------------|
| 2020 | GPT-3 | 4K tokens |
| 2023 | GPT-4 | 128K tokens |
| 2024 | Claude 3 | 200K tokens |
| 2025 | Claude 4 | 1M tokens |
| 2026 | Gemini 3 Pro | 2M tokens |
""",
    "cap_2.md": """

### Context Engineering para Agentes em Loop

Quando o agente opera em loop (multi-turn), a gestao de contexto e ainda mais critica:

```python
class AgentContextManager:
    def __init__(self, max_tokens=100000, compact_threshold=0.85):
        self.max_tokens = max_tokens
        self.compact_threshold = compact_threshold
        self.messages = []
        self.system_prompt = ''
        self.working_memory = {}
    
    def add_turn(self, user_msg, assistant_msg, tool_results=None):
        self.messages.append({'role': 'user', 'content': user_msg})
        self.messages.append({'role': 'assistant', 'content': assistant_msg})
        if tool_results:
            for result in tool_results:
                self.messages.append({
                    'role': 'user',
                    'content': [{'type': 'tool_result', **result}]
                })
        self._maybe_compact()
    
    def _maybe_compact(self):
        if self._estimate_tokens() > self.max_tokens * self.compact_threshold:
            self._compact()
    
    def _compact(self):
        summary = self._summarize_half()
        self.working_memory['last_summary'] = summary
        self.messages = self._keep_recent_half()
    
    def _summarize_half(self):
        half = self.messages[:len(self.messages)//2]
        return self._llm_summarize(half)
    
    def _keep_recent_half(self):
        return self.messages[len(self.messages)//2:]
    
    def _estimate_tokens(self):
        total = len(self.system_prompt) // 4
        for msg in self.messages:
            total += len(str(msg.get('content', ''))) // 4
        return total
```

### Prompt Engineering para Diferentes Modelos

**Claude (Anthropic):**
- Responde bem a XML tags: `<instructions>`, `<context>`
- Gosta de estrutura clara e hierarquica
- Funciona bem com "Voce e..." no system prompt

**GPT (OpenAI):**
- Responde bem a Markdown: `## Headers`, `**bold**`
- Prefere instrucoes diretas e imperativas
- Funciona bem com role definitions

**Gemini (Google):**
- Responde bem a listas e tabelas
- Prefere concisao
- Funciona bem com examples inline

### Anti-Padroes de Context Engineering

1. **Context Flooding**: jogar 50.000 tokens quando 5.000 bastam
2. **Prompt Pollution**: misturar instrucoes com dados no mesmo nivel
3. **Example Overload**: 50 examples quando 3 bastam
4. **Instruction Contradiction**: regras conflitantes no system prompt
5. **Static Context**: nao atualizar contexto com novos dados
6. **Blame the Model**: culpar o LLM quando o problema e o contexto
7. **Over-Engineering**: prompts complexos quando simples bastam

### Context Engineering em Equipas

1. **Template de System Prompt**: todos usam o mesmo formato
2. **Repository de Examples**: exemplos compartilhados e versionados
3. **Style Guide de Prompts**: convencoes de nomenclatura e estrutura
4. **Code Review de Prompts**: revisar mudancas em system prompts
5. **Testing Framework**: testar prompts como codigo
""",
    "cap_3.md": """

### Decisoes de Arquitetura: Model Selection Strategy

| Criterio | Peso | Como Avaliar |
|----------|------|--------------|
| Acuracia | 40% | Benchmark na tarefa especifica |
| Custo | 25% | Custo estimado por 1M requests |
| Latencia | 20% | P95 latency |
| Seguranca | 10% | Data retention, compliance |
| Comunidade | 5% | Docs, SDK, suporte |

```python
def evaluate_model(model, criteria_weights):
    scores = {
        'accuracy': benchmark_score(model) * criteria_weights['accuracy'],
        'cost': cost_score(model) * criteria_weights['cost'],
        'latency': latency_score(model) * criteria_weights['latency'],
        'security': security_score(model) * criteria_weights['security'],
        'community': community_score(model) * criteria_weights['community']
    }
    return sum(scores.values())

weights = {'accuracy': 0.4, 'cost': 0.25, 'latency': 0.2, 'security': 0.1, 'community': 0.05}
sonnet_score = evaluate_model('claude-sonnet-5', weights)
opus_score = evaluate_model('claude-opus-4-8', weights)
haiku_score = evaluate_model('claude-haiku-4-5', weights)
```

### Gerenciamento de Custo em Producao

```python
class CostTracker:
    def __init__(self):
        self.costs = []
    
    def log(self, model, input_tokens, output_tokens):
        cost = calculate_cost(model, input_tokens, output_tokens)
        self.costs.append({
            'model': model,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'cost': cost,
            'timestamp': time.time()
        })
    
    def daily_report(self):
        today = time.time() - 86400
        today_costs = [c for c in self.costs if c['timestamp'] > today]
        return {
            'total_cost': sum(c['cost'] for c in today_costs),
            'total_requests': len(today_costs),
            'avg_cost_per_request': sum(c['cost'] for c in today_costs) / max(len(today_costs), 1),
            'by_model': self._group_by_model(today_costs)
        }
```

### Benchmarking Customizado

1. **Colete dados reais**: 100-500 requests de producao
2. **Label manual**: avalie qualidade das respostas
3. **Compare modelos**: rode os mesmos prompts em diferentes modelos
4. **Meça latencia**: p50, p95, p99
5. **Calcule custo real**: inclua cache hits e retries
""",
    "cap_4.md": """

### Monorepo vs Multi-Repo para Agentes

**Monorepo:**
- Todos os agentes em um repositorio
- Facil compartilhar codigo e dependencias
- CI/CD complexo
- Bom para equipas pequenas (<10 devs)

**Multi-Repo:**
- Cada agente em um repositorio separado
- Independencia total
- Compartilhamento via packages
- Bom para equipas grandes (>10 devs)

### Agentes e Seguranca

1. **Prompt Injection**: usuario malicioso injeta instrucoes no input
   - Mitigacao: sanitizacao de input, sandboxing

2. **Data Exfiltration**: agente envia dados sensiveis para fora
   - Mitigacao: DLP (Data Loss Prevention), monitoring

3. **Tool Abuse**: agente usa tools de forma maliciosa
   - Mitigacao: permissoes granulares, audit logging

4. **Model Theft**: extrair modelo proprietario via queries
   - Mitigacao: rate limiting, watermarking

5. **Hallucination em Producao**: agente toma decisoes baseadas em informacoes inventadas
   - Mitigacao: fact-checking, human-in-the-loop

### Checklist de Deploy

```
SEGURANCA
[ ] Input sanitization implementada
[ ] Output validation ativa
[ ] Rate limiting configurado
[ ] API keys em secrets manager
[ ] Audit logging habilitado

PERFORMANCE
[ ] Latencia p95 < target
[ ] Throughput >= demanda esperada
[ ] Cache hit rate monitorado
[ ] Circuit breaker configurado

CUSTO
[ ] Budget alerts configurados
[ ] Model routing ativo
[ ] Caching otimizado
[ ] Cost tracking funcionando

RESILIENCIA
[ ] Retry com backoff implementado
[ ] Fallback chain testado
[ ] Graceful degradation verificado
[ ] Health checks ativos

MONITORAMENTO
[ ] Dashboards criados
[ ] Alerts configurados
[ ] Logging estruturado
[ ] Tracing habilitado

TESTES
[ ] Unit tests passando
[ ] Integration tests passando
[ ] Load test executado
[ ] Chaos engineering testado
```
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
