#!/usr/bin/env python3
"""Expand LLM book chapters part 3."""
import os

BASE = "output/tela-camada-agente/livros/llm-terceira-camada/capitulos"

additions = {
    "cap_1.md": """

### LLMs e Etica

O uso de LLMs levanta questoes eticas importantes:

1. **Vies de Dados**: LLMs refletem vieses dos dados de treinamento
   - Mitigacao: diverse training data, bias testing, human oversight

2. **Desinformacao**: LLMs podem gerar noticias falsas convincentes
   - Mitigacao: watermarking, fact-checking, source attribution

3. **Privacidade**: LLMs podem memorizar e revelar dados sensiveis
   - Mitigacao: differential privacy, data anonymization

4. **Impacto no Emprego**: automacao de tarefas cognitivas
   - Mitigacao: re-skilling, augmentation vs replacement

5. **Responsabilidade**: quem e responsavel por decisoes tomadas por LLMs?
   - Mitigacao: human-in-the-loop, audit trails, regulatory frameworks

### LLMs no Brasil: Panorama Atual (2026)

O ecossistema brasileiro de IA esta em rapida evolucao:

**Empresas Brasileiras com IA:**
- TOTVS: integracao LLMs em ERP
- iFood: agentes de atendimento ao cliente
- Nubank: analise de risco com IA
- Stone: automacao de processos financeiros

**Desafios Especificos:**
1. Custo: precos em USD sao caros para startups brasileiras
2. Linguagem: modelos em PT-BR ainda inferiores aos de EN
3. Infraestrutura: falta de GPUs disponiveis no Brasil
4. Regulacao: Marco Legal da IA em discussao no Congresso
5. Talento: escassez de profissionais especializados

### Roadmap de Aprendizagem

Para quem quer se especializar em LLMs:

**Nivel 1: Fundamentos (1-2 meses)**
- Entender o que e um LLM
- Aprender sobre tokens, context windows, temperature
- Fazer suas primeiras chamadas de API
- Ler a documentacao da Anthropic/OpenAI

**Nivel 2: Intermediario (2-4 meses)**
- Dominar prompt engineering
- Aprender context engineering
- Implementar RAG basico
- Construir um agente simples

**Nivel 3: Avancado (4-6 meses)**
- Multi-agent systems
- Fine-tuning de modelos
- Otimizacao de custo em producao
- Seguranca de agentes

**Nivel 4: Especialista (6-12 meses)**
- Arquitetura de sistemas de IA
- Observabilidade e monitoring
- Contribuicao para open source
- Publicacao de pesquisas
""",
    "cap_2.md": """

### Context Engineering: Metricas e KPIs

Como medir a eficacia do seu context engineering:

| Metrica | O que mede | Target |
|---------|-----------|--------|
| Context Efficiency | Tokens uteis / tokens totais | >70% |
| Instruction Following | % de instrucoes seguidas | >95% |
| Format Compliance | % de saidas no formato correto | >90% |
| Context Utilization | % da janela util usada | 50-80% |
| Prompt Stability | Variacao de qualidade entre versoes | <5% |

### Context Engineering para Diferentes Publicos

**Para Desenvolvedores:**
- Foco em technical accuracy
- Exemplos de codigo funcionais
- Referencias a documentacao oficial

**Para Negocios:**
- Foco em clareza e simplicidade
- Evitar jargao tecnico
- Exemplos praticos do dominio

**Para Pesquisadores:**
- Foco em rigor academico
- Citacoes e referencias
- Metodologia detalhada
""",
    "cap_3.md": """

### Casos de Estudo Reais

**Caso 1: Startup de EdTech**

Problema: plataforma de ensino quer usar IA para personalizar aprendizado.

Solucao:
- Haiku para quiz interativo (respostas rapidas, baixo custo)
- Sonnet para explicacoes detalhadas (qualidade media, custo moderado)
- Opus para geracao de material didatico (qualidade alta, custo alto)

Resultado: custo de $0.02 por aluno/mes para 100K alunos.

**Caso 2: Fintech de Pagamentos**

Problema: analise automatizada de transacoes suspeitas.

Solucao:
- Sonnet para classificacao de transacoes (acuracia critica)
- Haiku para pre-filtros (80% das transacoes sao normais)
- Opus para investigacao de casos complexos

Resultado: reducao de 70% no tempo de analise, custo de $500/mes.

**Caso 3: E-commerce de Moda**

Problema: recomandacao personalizada de roupas.

Solucao:
- Haiku para matching de estilo (classificacao simples)
- Sonnet para descricoes de produto (escrita criativa)
- Multimodal (GPT-5.6) para analise de imagens

Resultado: aumento de 25% no CTR de recomendacoes.
""",
    "cap_4.md": """

### LLMs e o Futuro do Trabalho

Impactos esperados ate 2030:

**Tarefas que serao automatizadas (>50%):**
- Classificacao de emails
- Triagem de documentos
- Respostas padronizadas ao cliente
- Analise basica de dados
- Geracao de relatorios

**Tarefas que serao augmentadas (20-50%):**
- Escrita de codigo
- Analise de mercado
- Criacao de conteudo
- Decisoes de negocio
- Pesquisa academica

**Tarefas que permanecerao humanas (<20%):**
- Relacionamento interpessoal
- Tomada de decisao etica
- Criatividade original
- Lideranca e gestao
- Cuidado com pessoas

### Governanca de Agentes IA

Framework para governanca:

1. **Comite de IA**: grupo multidisciplinar que revisa uso de IA
2. **Politicas de Uso**: regras claras do que e permitido
3. **Auditoria Regular**: revisao periodica de agentes em producao
4. **Incident Response**: plano para quando algo der errado
5. **Transparencia**: documentar como agentes tomam decisoes

### Glossario de Termos Avancados

| Termo | Definicao |
|-------|-----------|
| RLHF | Reinforcement Learning from Human Feedback |
| DPO | Direct Preference Optimization |
| LoRA | Low-Rank Adaptation (fine-tuning eficiente) |
| Quantizacao | Reducao de precision (FP16, INT8, INT4) |
| Speculative Decoding | Decodificacao antecipada para acelerar |
| KV Cache | Cache de Key-Value para eficiencia |
| Flash Attention | Implementacao otimizada de attention |
| MoE | Mixture of Experts (arquitetura eficiente) |
| RAG | Retrieval-Augmented Generation |
| Embedding | Representacao vetorial de texto |
| Chunking | Divisao de texto em pedacos para RAG |
| Reranking | Reordenacao de resultados por relevancia |
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
