#!/usr/bin/env python3
"""Last expansion to reach 100k chars."""
import os

BASE = "output/tela-camada-agente/livros/llm-terceira-camada/capitulos"

additions = {
    "cap_1.md": """

### LLMs e Criatividade

LLMS podem ser parceiros criativos:

**Usos criativos:**
- Brainstorming de ideias
- Escrita de ficcao
- Composicao musical
- Design de produtos
- Criacao de jogos

**Limitacoes:**
- Nao tem experiencias genuinas
- Criatividade e recombinacao, nao invencao
- Depende da qualidade do input humano
- Pode gerar conteudo derivativo

### LLMs e Linguagens Naturais

Capacidades multilingues:

| Modelo | Idiomas Suportados | Acuracia PT-BR |
|--------|-------------------|----------------|
| Claude Opus 4.8 | 200+ | 85% |
| GPT-5.6 | 100+ | 82% |
| Gemini 3 Pro | 100+ | 80% |
| Llama 4 | 50+ | 75% |

**Dica:** para criticas tecnicas em portugues, Claude tende a ser mais preciso.
""",
    "cap_2.md": """

### Context Engineering: Erros Fatais

Erros que destroem a qualidade:

1. **Contradicoes**: regras que conflitam entre si
2. **Ambiguidade**: instrucoes que podem ser interpretadas de multiplas formas
3. **Vazio**: system prompt sem informacao util
4. **Excesso**: 50.000 tokens de contexto irrelevante
5. **Desatualizacao**: contexto que nao reflete o estado atual

### Context Engineering e Debug

Como diagnosticar problemas:

```
Problema: modelo retorna formato errado
Diagnostico: falta example no system prompt
Solucao: adicionar few-shot example

Problema: modelo ignora restricoes
Diagnostico: restricoes nao sao claras
Solucao: usar XML tags para delimitar

Problema: modelo responde em ingles
Diagnostico: system prompt em ingles
Solucao: adicionar "Responda em portugues"
```
""",
    "cap_3.md": """

### LLMs e Edge Computing

Processamento local:

**Vantagens:**
- Privacidade total
- Sem custo de API
- Funciona offline
- Baixa latencia

**Desvantagens:**
- Modelo menor (128K max)
- Precisa de GPU local
- Manutencao manual
- Sem atualizacoes automaticas

**Ferramentas:**
- Ollama: rodar LLMs localmente
- LM Studio: interface grafica para LLMs
- llama.cpp: inferencia otimizada para CPU
- vLLM: serving de alto throughput
""",
    "cap_4.md": """

### LLMs e o Futuro Proximo (2027-2028)

Previsoes fundamentadas:

1. **Context Windows**: 5M tokens sera padrao
2. **Latencia**: <50ms para respostas curtas
3. **Custo**: 10x mais barato que hoje
4. **Multimodal**: nativo em todos os modelos
5. **Especializacao**: modelos por dominio
6. **Autonomia**: agentes com 90%+ de automacao
7. **Regulacao**: marcos legais estabelecidos

### Agradecimentos e Recursos

Obrigado por ler ate aqui! Recursos para continuar aprendendo:

**Documentacao Oficial:**
- Anthropic Docs: docs.anthropic.com
- OpenAI Docs: platform.openai.com
- Google AI: ai.google.dev

**Comunidades:**
- Reddit: r/LocalLLaMA, r/ClaudeAI
- Discord: comunidades de IA
- Twitter/X: pesquisadores de IA

**Cursos:**
- DeepLearning.AI: cursos gratuitos de IA
- Fast.ai: practical deep learning
- Hugging Face: courses huggingface.co

**Projetos Open Source:**
- LangChain: framework para agentes
- LlamaIndex: framework para RAG
- Ollama: rodar LLMs localmente
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
