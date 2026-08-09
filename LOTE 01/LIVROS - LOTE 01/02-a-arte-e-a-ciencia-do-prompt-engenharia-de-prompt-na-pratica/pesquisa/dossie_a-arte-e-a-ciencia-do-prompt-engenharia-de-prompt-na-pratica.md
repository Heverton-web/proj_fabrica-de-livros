# Dossiê de Pesquisa — Livro 2: A arte e a ciência do prompt

**Obra:** A arte e a ciência do prompt: engenharia de prompt na prática
**Série:** A Pilha Agêntica (Livro 2) — AI-Driven Development
**Eixo:** Parte I — Fundação (Livros 1-2)
**Data:** 5 de agosto de 2026

---

## 1. Conceitos-chave e definições

A engenharia de prompt é a disciplina de projetar deliberadamente as instruções enviadas a um modelo de linguagem para obter saídas previsíveis e corretas. Embora seja a camada mais antiga da pilha agêntica, permanece indispensável: todo sistema de IA conversa com o modelo por meio de prompts — inclusive os agentes autônomos que a série aborda nos volumes seguintes.

A anatomia de um bom prompt divide-se em cinco blocos:

1. **Identidade e papel** — quem o modelo deve "ser" e o escopo da atuação.
2. **Instruções** — regras determinísticas sobre o que fazer e evitar.
3. **Contexto** — dados de suporte, variáveis de tempo de execução e informações de fundo.
4. **Exemplos** — demonstrações few-shot que ancoram o comportamento.
5. **Formato de saída** — restrições rígidas de estrutura (JSON Schema, Markdown estrito) para consumo programático.

## 2. Estado da arte

A literatura oficial das principais empresas de IA (OpenAI, Anthropic, Google) converge: prompts estruturados com delimitação sintática clara superam comandos textuais difusos. As técnicas principais são:

- **Few-shot prompting** — fornecer pares de entrada-saída esperada antes da tarefa real; reduz ambiguidade semântica sem exigir fine-tuning.
- **Chain-of-thought (CoT)** — induzir o modelo a gerar passos intermediários de raciocínio antes da resposta final; habilidade emergente em modelos de grande escala.
- **Zero-shot CoT** — a frase "Vamos pensar passo a passo" elicia raciocínio sem exemplos.
- **Self-consistency** — amostrar múltiplos caminhos de raciocínio e agregar por votação majoritária.
- **Prompts de sistema vs. usuário** — separação arquitetural entre instruções diretivas de alta autoridade e entrada dinâmica transacional.

## 3. O problema da escala

Prompt engineering sozinha não escala em produção por quatro razões:

1. **Estocasticidade** — o mesmo prompt gera saídas diferentes; reprodutibilidade exige controle.
2. **Versionamento** — mudanças sutis causam regressões silenciosas; prompts precisam de imutabilidade e golden datasets.
3. **Teste** — sem testes automatizados, regressões passam despercebidas até a produção.
4. **Consistência entre equipes** — múltiplos times editando prompts sem esteira de promoção (dev, staging, prod) gera caos de governança.

A avaliação manual de respostas enfrenta o fenômeno das respostas plausíveis-porém-erradas: textos gramaticalmente perfeitos com falhas factuais graves. Rubricas estruturadas, golden answers e LLM-as-a-judge são as metodologias padrão.

## 4. Casos de uso reais

- Suporte ao cliente com prompts de sistema rígidos + few-shot para classificação de tickets.
- Extração de dados estruturados com JSON Schema obrigatório.
- Raciocínio aritmético e lógico com CoT em modelos de grande escala.
- Pipelines de produção com versionamento de prompts e CI/CD para LLMs.

## 5. Riscos e limitações

- **Limites da disciplina** — o gargalo dos agentes de longo horizonte deixou de ser a redação estática do prompt e passou a ser a gestão dinâmica do orçamento de atenção: compactação, memória externa e recuperação sob demanda. É a ponte para a Context Engineering (Livro 3 da série).
- **Injeção de prompt** — entradas de usuário podem tentar sobrepor instruções de sistema; a hierarquia de mensagens (developer > user) é a defesa arquitetural.
- **Alucinação** — saída fluente sem âncora factual (estudada no Livro 1, Capítulo 8).

## 6. Fontes brutas com URLs (22 fontes rastreáveis)

### Eixo 1 — Anatomia de um bom prompt
1. OPENAI. Prompt engineering. Disponível em: https://developers.openai.com/api/docs/guides/prompt-engineering
2. OPENAI. Best practices for prompt engineering with the OpenAI API. Disponível em: https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api
3. ANTHROPIC. Effective context engineering for AI agents. Disponível em: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
4. ANTHROPIC. Building Effective AI Agents. Disponível em: https://www.anthropic.com/engineering/building-effective-agents

### Eixo 2 — Few-shot
5. BROWN, Tom B. et al. Language Models are Few-Shot Learners. Disponível em: https://arxiv.org/abs/2005.14165
6. EDULAPALLE, Santosh. Prompt Engineering 201: Best Practices for Getting Consistent, Accurate, and Scalable Results. Disponível em: https://medium.com/@SantoshEdulapalle/prompt-engineering-201-best-practices-for-getting-consistent-accurate-and-scalable-results-52d2273c0416
7. OPENAI. Best practices for prompt engineering (seção Few-Shot). Disponível em: https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api

### Eixo 3 — Chain-of-Thought
8. WEI, Jason et al. Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. Disponível em: https://arxiv.org/abs/2201.11903
9. KOJIMA, Takeshi et al. Large Language Models are Zero-Shot Reasoners. Disponível em: https://arxiv.org/abs/2205.11916
10. WANG, Xuezhi et al. Self-Consistency Improves Chain of Thought Reasoning in Language Models. Disponível em: https://arxiv.org/abs/2203.11171

### Eixo 4 — System vs. User prompt
11. OPENAI. Model guidance. Disponível em: https://developers.openai.com/api/docs/guides/latest-model
12. ANTHROPIC. System prompts (documentação Claude). Disponível em: https://docs.anthropic.com/claude/docs/system-prompts
13. GOOGLE CLOUD. Generative AI Prompt Design Guide. Disponível em: https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/prompt-design

### Eixo 5 — Escala e produção
14. BRAINTRUST. What is prompt versioning? Best practices for iteration without breaking production. Disponível em: https://www.braintrust.dev/articles/what-is-prompt-versioning
15. PAN, Tian. Prompt Versioning in Production: The Engineering Discipline Teams Learn the Hard Way. Disponível em: https://tianpan.co/blog/2026-04-09-prompt-versioning-production-llm
16. LAUNCHDARKLY. Prompt Versioning & Management Guide for Building AI Features. Disponível em: https://launchdarkly.com/blog/prompt-versioning-and-management/

### Eixo 6 — Avaliação manual
17. LANGCHAIN. Evaluating LLM Systems: Metrics and Best Practices. Disponível em: https://blog.langchain.dev/evaluating-llm-platforms/
18. CHANG, Yupeng et al. A Survey on Evaluation of Large Language Models. Disponível em: https://arxiv.org/abs/2307.03109
19. GROWTHBOOK. How to test multiple prompts in production (without chaos). Disponível em: https://www.growthbook.io/insights/how-test-multiple-prompts-production-without-chaos

### Eixo 7 — Limites e Context Engineering
20. ANTHROPIC. Effective context engineering for AI agents. Disponível em: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
21. ANTHROPIC. Context engineering: memory, compaction, and tool clearing. Disponível em: https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools
22. LANGCHAIN. Context Engineering for AI Agents. Disponível em: https://www.langchain.com/blog/context-engineering-for-agents

## 7. Referências bibliográficas (formato ABNT)

1. BROWN, Tom B.; et al. Language Models are Few-Shot Learners. 2020. Disponível em: https://arxiv.org/abs/2005.14165. Acesso em: 5 ago. 2026.
2. WEI, Jason; et al. Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. 2022. Disponível em: https://arxiv.org/abs/2201.11903. Acesso em: 5 ago. 2026.
3. KOJIMA, Takeshi; et al. Large Language Models are Zero-Shot Reasoners. 2022. Disponível em: https://arxiv.org/abs/2205.11916. Acesso em: 5 ago. 2026.
4. WANG, Xuezhi; et al. Self-Consistency Improves Chain of Thought Reasoning in Language Models. 2022. Disponível em: https://arxiv.org/abs/2203.11171. Acesso em: 5 ago. 2026.
5. CHANG, Yupeng; et al. A Survey on Evaluation of Large Language Models. 2023. Disponível em: https://arxiv.org/abs/2307.03109. Acesso em: 5 ago. 2026.
