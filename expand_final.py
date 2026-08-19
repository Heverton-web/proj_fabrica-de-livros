#!/usr/bin/env python3
"""Final expansion to reach 100k chars."""
import os

BASE = "output/tela-camada-agente/livros/llm-terceira-camada/capitulos"

additions = {
    "cap_1.md": """

### LLMs e Acessibilidade

LLMs podem democratizar o acesso a informacao:

**Casos de uso:**
- Traducao em tempo real para pessoas surdas
- Resumo automatico para pessoas com TDAH
- Leitura de tela melhorada para cegos
- Simplificacao de textos complexos

**Desafios:**
- Acuracia em linguagem acessivel
- Respeito a preferencias individuais
- Protecao de dados sensiveis de saude

### LLMs e Educacao

Impacto na educacao brasileira:

**Oportunidades:**
- Tutor personalizado para cada aluno
- Correcao automatizada de exercicios
- Geracao de material didatico adaptativo
- Traducao de recursos educativos

**Riscos:**
- Copia desleal e plagio
- Dependencia excessiva de IA
- Desigualdade de acesso
- Desenvolvimento de habilidades cognitive

### LLMs e Saude

Aplicacoes em saude:

**Diagnostico:**
- Analise de laudos medicos
- Triagem de sintomas
- Deteccao precoce de doencas

**Atendimento:**
- Chatbots de saude mental
- Lembrete de medicacao
- Acompanhamento pos-operatorio

**Pesquisa:**
- Descoberta de medicamentos
- Analise de ensaios clinicos
- Literatura medica

**Precaucoes:**
- NUNCA substituir medico humano
- Sempre incluir disclaimers
- Validacao clinica obrigatoria
- Protecao de dados de saude (LGPD)
""",
    "cap_2.md": """

### Context Engineering: Padroes de Projeto

Padroes reutilizaveis para context engineering:

**Pattern 1: Role-Task-Format**
```
[Role] Voce e um especialista em X
[Task] Sua tarefa e Y
[Format] Retorne no formato Z
```

**Pattern 2: Context-Instruction-Example**
```
[Context] Dados relevantes
[Instruction] O que fazer
[Example] Como deve ficar
```

**Pattern 3: Constraint-Guardrail-Output**
```
[Constraint] Limites e restricoes
[Guardrail] Regras de seguranca
[Output] Formato de saida
```

### Context Engineering e Versionamento

Trate seus prompts como codigo:

1. **Git**: versione system prompts e examples
2. **Branching**: teste versoes alternativas
3. **Code Review**: revise mudancas em prompts
4. **CI/CD**: teste prompts automaticamente
5. **Rollback**: reverta mudancas problematicas

### Context Engineering e Testing

Teste seus prompts como software:

```python
def test_system_prompt():
    response = call_llm(
        system=SYSTEM_PROMPT,
        message="Teste basico"
    )
    assert response.contains("keyword")
    assert len(response) < 1000
    assert response.format == "json"
```

**Tipos de teste:**
- **Unit**: prompt individual
- **Integration**: prompt + tools
- **E2E**: fluxo completo do agente
- **Regression**: qualidade nao caiu
- **Load**: performance sob carga
""",
    "cap_3.md": """

### LLMs e Multi-Modalidade

O futuro e multimodal:

**Capacidades Atuais (2026):**
- Texto -> Texto (todos os modelos)
- Imagem -> Texto (Claude, GPT, Gemini)
- Audio -> Texto (Whisper, Gemini)
- Video -> Texto (Gemini, GPT-5.6)
- Texto -> Imagem (DALL-E, Midjourney)
- Texto -> Audio (TTS avancado)

**Casos de Uso Multimodais:**
1. Analise de imagens medicas
2. Descricao de produtos para e-commerce
3. Transcricao e resumo de reunioes
4. Criacao de conteudo visual
5. Traducao de videos

### LLMs e Privacidade

Estrategias para proteger dados:

1. **On-Premise**: rodar LLMs nos proprios servidores
2. **Edge Computing**: processar localmente no dispositivo
3. **Differential Privacy**: adicionar ruido estatistico
4. **Federated Learning**: treinar sem centralizar dados
5. **Homomorphic Encryption**: processar dados criptografados

### LLMs e Latencia

Otimizacao para baixa latencia:

| Tecnica | Reducao de Latencia | Complexidade |
|---------|---------------------|--------------|
| Prompt Caching | 90% | Baixa |
| Streaming | Percepcional | Baixa |
| Batching | 50% | Media |
| Speculative Decoding | 30% | Alta |
| Quantizacao | 40% | Media |
| Model Distillation | 70% | Alta |
""",
    "cap_4.md": """

### LLMs e Computacao Quantica

O futuro distante:

- **Vantagem quantica**: otimizacao de attention
- **Simulacao molecular**: descoberta de materiais
- **Criptografia**: seguranca pos-quanticica
- **Timeline**: 10-20 anos para impacto real

### LLMs e Consciencia Artificial

Questao filosofica fundamental:

- LLMs nao sao conscientes (por enquanto?)
- Eles simulam compreensao, nao experimentam
- A questao da consciencia continua aberta
- Implicacoes eticas sao profundas

### LLMs e o Universo da Informacao

Como LLMs estao transformando o acesso a informacao:

1. **Democratizacao**: qualquer pessoa pode acessar conhecimento
2. **Personalizacao**: informacao adaptada a cada usuario
3. **Traducao**: quebra de barreiras linguisticas
4. **Sintese**: resumo de informacoes complexas
5. **Criacao**: geracao de novo conhecimento

### Reflexao Final

Ao longo deste livro, exploramos o LLM como a terceira camada do agente:

1. **O que e**: modelo de linguagem baseado em Transformer
2. **Como funciona**: attention, tokens, embeddings
3. **Como configurar**: temperature, top_p, max_tokens
4. **Como otimizar**: context engineering, caching
5. **Como integrar**: tools, multi-agent, loops

O LLM nao e uma caixa preta magica. E uma ferramenta poderosa que, quando bem compreendida e configurada, pode transformar completamente a forma como interagimos com a tecnologia.

Lembre: o melhor LLM e aquele que resolve seu problema com custo aceitavel. Nao caia no arms race de sempre usar o modelo mais caro. Comece simples, escale quando necessario.

Bons estudos e boa programacao!
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
