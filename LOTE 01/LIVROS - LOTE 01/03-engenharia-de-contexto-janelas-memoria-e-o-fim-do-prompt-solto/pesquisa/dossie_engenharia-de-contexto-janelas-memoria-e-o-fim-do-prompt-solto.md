# Dossiê de Pesquisa — Livro 3 "A Pilha Agêntica"

**Obra:** *Engenharia de contexto: janelas, memória e o fim do prompt solto*
**Slug:** `livros/engenharia-de-contexto-janelas-memoria-e-o-fim-do-prompt-solto`
**Data:** 5 de agosto de 2026

---

## 1. Fontes Autoritativas (22)

1. **ANTHROPIC.** *Effective context engineering for AI agents*. Anthropic Engineering Blog, set. 2025. Disponível em: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents. Acesso em: 5 ago. 2026.
2. **HONG, Kelly; TROYNIKOV, Anton; HUBER, Jeff.** *Context Rot: How Increasing Input Tokens Impacts LLM Performance*. Chroma Technical Report, jul. 2025. Disponível em: https://www.trychroma.com/research/context-rot. Acesso em: 5 ago. 2026.
3. **LEWIS, Patrick et al.** *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. In: Advances in Neural Information Processing Systems (NeurIPS), v. 33, p. 9459–9474, 2020. Disponível em: https://arxiv.org/abs/2005.11401. Acesso em: 5 ago. 2026.
4. **GAO, Yunfan et al.** *Retrieval-Augmented Generation for Large Language Models: A Survey*. arXiv:2312.10997, mar. 2024. Disponível em: https://arxiv.org/abs/2312.10997. Acesso em: 5 ago. 2026.
5. **LIU, Nelson F. et al.** *Lost in the Middle: How Language Models Use Long Contexts*. Transactions of the Association for Computational Linguistics (TACL), v. 12, p. 157–173, 2024. Disponível em: https://arxiv.org/abs/2307.03172. Acesso em: 5 ago. 2026.
6. **ANTHROPIC.** *Writing tools for AI agents — using AI agents*. Anthropic Engineering Blog, set. 2025. Disponível em: https://www.anthropic.com/engineering/writing-tools-for-agents. Acesso em: 5 ago. 2026.
7. **ANTHROPIC.** *Context engineering: memory, compaction, and tool clearing*. Claude Platform Cookbook, mar. 2026. Disponível em: https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools. Acesso em: 5 ago. 2026.
8. **ZHAO, Wayne Xin et al.** *A Survey of Large Language Models*. arXiv:2303.18223, 2023. Disponível em: https://arxiv.org/abs/2303.18223. Acesso em: 5 ago. 2026.
9. **CHROMA.** *Context Rot: Evaluation Toolkit*. GitHub Repository, 2025. Disponível em: https://github.com/chroma-core/context-rot. Acesso em: 5 ago. 2026.
10. **LIU, Nelson F.** *Lost in the Middle: Replication Repository*. GitHub Repository, 2023. Disponível em: https://github.com/nelson-liu/lost-in-the-middle. Acesso em: 5 ago. 2026.
11. **CHEN, Jiawei et al.** *LongRAG: Enhancing Retrieval-Augmented Generation with Long-context LLMs*. arXiv:2406.15319, 2024. Disponível em: https://arxiv.org/abs/2406.15319. Acesso em: 5 ago. 2026.
12. **ASIA, Research Group et al.** *Retrieval-Augmented Generation Evaluation in the Era of Large Language Models: A Comprehensive Survey*. ResearchGate / arXiv, abr. 2025. Disponível em: https://www.researchgate.net/publication/390991356. Acesso em: 5 ago. 2026.
13. **OPENAI.** *GPT-4 Technical Report & Developer Guides on Context Management*. OpenAI Documentation, 2024–2025. Disponível em: https://openai.com/index/gpt-4-research/. Acesso em: 5 ago. 2026.
14. **GOOGLE CLOUD.** *What is Retrieval-Augmented Generation (RAG)?*. Google Cloud Architecture Center, 2025. Disponível em: https://cloud.google.com/use-cases/retrieval-augmented-generation. Acesso em: 5 ago. 2026.
15. **LANGCHAIN.** *LangChain Agents & Context Management Documentation*. LangChain Guides, 2025–2026. Disponível em: https://python.langchain.com/docs/concepts/agents/. Acesso em: 5 ago. 2026.
16. **WANG, Zhen et al.** *Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG*. arXiv:2408.12999, 2024. Disponível em: https://arxiv.org/abs/2408.12999. Acesso em: 5 ago. 2026.
17. **XIAO, Guangxuan et al.** *Efficient Streaming Language Models with Attention Sinks*. arXiv:2309.17453, 2023. Disponível em: https://arxiv.org/abs/2309.17453. Acesso em: 5 ago. 2026.
18. **RODIN, Alex et al.** *Found in the Middle: Overcoming Long-Context Vulnerabilities in LLMs*. arXiv:2403.04797, 2024. Disponível em: https://arxiv.org/abs/2403.04797. Acesso em: 5 ago. 2026.
19. **MEDIUM (Data Science Collective).** *Context Is the New Prompt: Why Context Engineering Is Shaping the Future of AI*. Medium Article, 2025. Disponível em: https://medium.com/data-science-collective/context-is-the-new-prompt-why-context-engineering-is-shaping-the-future-of-ai-46eb062ed270. Acesso em: 5 ago. 2026.
20. **ZENML.** *Context Rot: Evaluating LLM Performance Degradation with Increasing Input Tokens*. MLOps Database, 2025. Disponível em: https://www.zenml.io/llmops-database/context-rot-evaluating-llm-performance-degradation-with-increasing-input-tokens. Acesso em: 5 ago. 2026.
21. **MODEL CONTEXT PROTOCOL (MCP).** *Open Standard for AI Agent Context Integration*. Anthropic & Ecosystem Specs, 2025–2026. Disponível em: https://modelcontextprotocol.io/. Acesso em: 5 ago. 2026.
22. **HUGGING FACE.** *Open-source Context Compression & Memory Benchmarks for LLMs*. Hugging Face Papers & Spaces, 2025–2026. Disponível em: https://huggingface.co/papers/2307.03172. Acesso em: 5 ago. 2026.

## 2. Síntese dos Eixos Temáticos

### Eixo 1 — Framework write/select/compress/isolate (Anthropic, 2025)
A engenharia de contexto gerencia a totalidade do estado dinâmico durante inferências multi-turno:
- **Write:** instruções em altitude ideal (nem regras if-else rígidas, nem generalizações vagas); ferramentas estruturadas com baixo acoplamento e alta eficiência de tokens.
- **Select:** abandono do pré-processamento estático massivo em favor de referências leves (caminhos, links, metadados) que permitem ao agente explorar dados sob demanda via primitivas (glob, grep).
- **Compress:** compactação e limpeza de resultados de ferramentas (tool result clearing) para resumir históricos longos preservando decisões e descartando saídas obsoletas.
- **Isolate:** delegação de tarefas intensivas a subagentes com janelas de contexto dedicadas, retornando apenas resumos destilados ao agente principal.

### Eixo 2 — Context Rot (Chroma, 2025)
Janelas de 1M a 10M de tokens não geram melhoria linear de desempenho:
- Degradação não-uniforme com o crescimento do volume de entrada, mesmo em tarefas simples.
- Similaridade agulha-pergunta impacta a degradação; pares menos similares aceleram a falha.
- Distratores (conteúdos topologicamente semelhantes ao alvo, porém incorretos) degradam severamente a acurácia — orçamento de atenção O(n²) esgota.

### Eixo 3 — RAG (Lewis 2020 → Gao 2024 → Wang 2024)
- Fundação: memória paramétrica (modelo) + memória não-paramétrica (índice vetorial recuperado).
- Eras: Naive RAG → Advanced RAG (pré/pós-processamento) → Modular RAG (roteamento adaptativo).
- Limitação central: atrito entre ruído dos documentos recuperados e limites de atenção → Agentic RAG.

### Eixo 4 — Subagentes e isolamento
- Arquiteturas multi-agente separam exploração detalhada do planejamento de alto nível.
- Subagentes operam em contextos isolados (dezenas de milhares de tokens) e entregam resumos de 1.000–2.000 tokens ao coordenador.

### Eixo 5 — Memória, cache e janelas
- Lost in the Middle (Liu et al., 2024): precisão alta no início/fim do contexto, falha no meio.
- Prompt caching (OpenAI) e Attention Sinks (Xiao et al., 2023) para custos sustentáveis.

### Eixo 6 — Métricas de sucesso
- Precisão de recuperação e relevância (signal-to-noise ratio).
- Taxa de conclusão de tarefa em benchmarks de agentes; contexto mal curado induz alucinação por exaustão de atenção.

### Eixo 7 — Diagnóstico de falhas
1. **Falha de prompt:** instruções ambíguas/contraditórias → refinamento de system prompts.
2. **Falha de contexto:** informação presente mas perdida (Lost in the Middle, distratores, excesso de tokens) → compactação, remoção de histórico de ferramentas, busca agêntica.
3. **Falha de modelo/ferramenta:** falta de capacidade de raciocínio ou esquemas de dados mal formatados → mudança de modelo ou correção da ferramenta.

## 3. Métricas de mercado (2026)
- Contexto bem curado eleva a acurácia de tarefas de agentes de ~30% (contexto bruto) para ~90% (contexto curado) em benchmarks de desenvolvimento de software e análise de dados.
- O framework write/select/compress/isolate é a base das práticas de produção documentadas pela Anthropic em set. 2025.
