# Dossiê Técnico — Livro 10: Eval Engineering e revisão autônoma entre harness

> Obra: Eval Engineering e revisão autônoma entre harness: garantindo confiança em sistemas de IA
> Parte IV — Mestria e carreira | Tamanho G | 20 refs/capítulo | Pesquisa em 4 frentes (ago. 2026)

## Tese central

A confiança em sistemas de IA não é uma propriedade que se declara — é uma propriedade que se
constrói, mede e mantém por engenharia. A disciplina que faz isso é a Eval Engineering: o
equivalente moderno da engenharia de testes, adaptado à natureza probabilística dos modelos de
linguagem. Em agentes autônomos, porém, avaliar a resposta final não basta: é preciso auditar a
trajetória inteira (perceber, raciocinar, agir, observar) e usar revisores autônomos — outros
harnesses, outros agentes, LLM-as-a-judge calibrados — para detectar o que a resposta final
esconde. O livro ensina a construir essa camada de garantia: dos tipos de evals e golden sets ao
red-teaming automatizado, do CI/CD com evals à revisão autônoma entre harnesses, da calibração de
juízes de IA à governança de confiança em produção. O motivo condutor é o relógio de aferição do
maquinista: toda locomotiva (agente) precisa de um relógio e de um painel de instrumentos que
digam a verdade sobre o estado da viagem — e de um inspetor independente que audite o percurso.

## Frente 1 — Eval Engineering: a disciplina de medir agentes

1. ANTHROPIC. *Demystifying evals for AI agents*. 2026. Disponível em:
   https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents. Acesso em: 06 ago. 2026.
   — Framework prático para avaliação de agentes multi-turnos; divide tarefas, tentativas, graders
   (code-based, model-based, human) e transcrições/trajetórias; métricas pass@k e pass^k.

2. ANTHROPIC. *Building effective agents*. 2024. Disponível em:
   https://www.anthropic.com/engineering/building-effective-agents. Acesso em: 06 ago. 2026.
   — Padrões arquiteturais de agentes (workflows vs. agentes autônomos); importância do
   Agent-Computer Interface (ACI) e do design de ferramentas testáveis.

3. OPENAI. *How evals drive the next chapter in AI for businesses*. 2025. Disponível em:
   https://openai.com/index/evals-drive-next-chapter-of-ai/. Acesso em: 06 ago. 2026.
   — Metodologia de três passos: Specify → Measure → Improve; golden sets gerados por especialistas.

4. LANGCHAIN. *LangSmith evaluation concepts*. 2026. Disponível em:
   https://docs.smith.langchain.com/evaluation. Acesso em: 06 ago. 2026.
   — Evals offline (pré-deploy, datasets) vs. online (monitores de produção baseados em traces);
   filas de anotação humana.

5. LANGFUSE. *LLM evaluation: methods, best practices, and a practical roadmap*. 2025. Disponível em:
   https://langfuse.com/blog/2025-11-12-evals. Acesso em: 06 ago. 2026.
   — Code evaluators nativos, LLM-as-a-judge assíncrono, CI/CD com GitHub Actions bloqueando PRs.

6. PROMPTFOO. *Introduction and docs*. 2026. Disponível em:
   https://www.promptfoo.dev/docs/intro/. Acesso em: 06 ago. 2026.
   — Test-driven prompt engineering; matrizes de comparação de prompts; red-teaming local.

7. CONFIDENT AI. *DeepEval: LLM evaluation unit testing in CI/CD*. 2026. Disponível em:
   https://deepeval.com/docs/evaluation-unit-testing-in-ci-cd. Acesso em: 06 ago. 2026.
   — Testes unitários de LLM com pytest e deepeval test run; instrumentação de LangChain,
   LangGraph, LlamaIndex, Pydantic AI.

8. BRAINTRUST. *Eval-driven development*. 2026. Disponível em:
   https://www.braintrust.dev/articles/eval-driven-development. Acesso em: 06 ago. 2026.
   — Eval como oráculo; linhagem de dados e prompts; gates de regressão em pipelines de promoção.

## Frente 2 — Revisão autônoma entre harnesses: LLM-as-a-judge e auto-correção

9. SHINN, Noah; CASSANO, Federico; NARASIMHAN, Karthik et al. *Reflexion: language agents with
   verbal reinforcement learning*. Princeton/MIT, 2023. Disponível em:
   https://arxiv.org/abs/2303.11366. Acesso em: 06 ago. 2026.
   — Auto-correção por feedback verbal; reflexões textuais em memória episódica; melhorias em
   HumanEval sem fine-tuning de pesos.

10. YU, Fangyi et al. *When AIs judge AIs: the rise of agent-as-a-judge evaluation for LLMs*.
    Stanford/Scale AI, 2025. Disponível em: https://arxiv.org/html/2508.02994v1. Acesso em:
    06 ago. 2026.
    — Transição de LLM-as-a-judge para agent-as-a-judge com raciocínio passo a passo, uso de
    ferramentas e acesso ao log de ações; arcabouços multi-agentes (ChatEval, DEBATE, CourtEval).

11. BOUSETOUANE, Fouad. *Human-on-the-bridge: scalable evaluation for AI agents*. ProofAgent/UChicago,
    2026. Disponível em: https://arxiv.org/html/2606.16871v1. Acesso em: 06 ago. 2026.
    — Red-team traps curados por humanos a montante; harnesses assimétricos (revisores menores
    auditam agentes complexos); detecção de falhas procedimentais invisíveis na resposta final.

12. BRAINTRUST. *What is an LLM-as-a-judge? When to use it (and when to use deterministic evals)*.
    2026. Disponível em: https://www.braintrust.dev/articles/what-is-llm-as-a-judge. Acesso em:
    06 ago. 2026.
    — Armadilhas de juízes de IA (viés de posição, viés de verbosidade, recompensa hacking);
    calibração humana, chain-of-thought no julgamento, agregações múltiplas.

13. CHASE, Harrison. *Aligning LLM-as-a-judge with human preferences*. LangChain, 2024.
    Disponível em: https://www.langchain.com/blog/aligning-llm-as-a-judge-with-human-preferences.
    Acesso em: 06 ago. 2026.
    — Auto-aperfeiçoamento de avaliadores; correções humanas viram exemplos few-shot do juiz.

## Frente 3 — Confiança, qualidade e segurança em produção

14. OWASP FOUNDATION. *OWASP GenAI security project (top 10 for LLM applications)*. 2026.
    Disponível em: https://owasp.org/www-project-top-10-for-large-language-model-applications/.
    Acesso em: 06 ago. 2026.
    — Prompt injection direto/indireto, excessive agency, supply chain, improper output handling;
    estratégias de red-teaming adversarial.

15. NIST. *AI risk management framework (AI RMF 1.0)*. 2023. Disponível em:
    https://www.nist.gov/itl/ai-risk-management-framework. Acesso em: 06 ago. 2026.
    — Funções Govern, Map, Measure, Manage; características de IA confiável (válida, segura,
    resiliente, explicável, privada, justa, responsável).

16. CLOUD SECURITY ALLIANCE. *Agentic NIST AI RMF profile*. 2025/2026. Disponível em:
    https://labs.cloudsecurityalliance.org/agentic/agentic-nist-ai-rmf-profile-v1/. Acesso em:
    06 ago. 2026.
    — Adaptação do NIST AI RMF aos riscos de autonomia e agência em sistemas multi-agentes.

17. EPOCH AI. *SWE-bench verified evaluation methodology*. 2026. Disponível em:
    https://epoch.ai/benchmarks/swe-bench-verified. Acesso em: 06 ago. 2026.
    — Benchmark padrão para agentes de engenharia de software; problemas reais de repositórios
    Python validados por testes unitários em Docker.

18. EVIDENTLY AI. *OWASP top 10 LLM and testing methodologies*. 2025/2026. Disponível em:
    https://www.evidentlyai.com/blog/owasp-top-10-llm. Acesso em: 06 ago. 2026.
    — Traduzir riscos OWASP em testes automatizados, red-teaming e monitoramento em produção.

## Frente 4 — Evals no ciclo de vida: CI/CD, regressão e EDD

19. LATITUDE. *The ultimate CI/CD LLM evaluation guide*. 2026. Disponível em:
    https://latitude.so/blog/ultimate-ci-cd-llm-evaluation-guide. Acesso em: 06 ago. 2026.
    — Arquiteturas de avaliação em camadas (regex/JSON, heurísticas, LLM-based); versionamento
    rigoroso de prompts em repositórios.

20. BRONSDON, Conor. *Continuous integration (CI) for AI: fundamentals*. Galileo AI, 2025.
    Disponível em: https://galileo.ai/blog/continuous-integration-ci-ai-fundamentals. Acesso em:
    06 ago. 2026.
    — Por que o CI tradicional falha em sistemas não determinísticos; métricas de agentes
    (precisão de seleção de ferramentas, coerência de raciocínio, alucinação, deriva).

21. SAMUYLOVA, Elena; DRAL, Emeli. *LLM unit testing in CI/CD with GitHub Actions*. Evidently AI,
    2025. Disponível em: https://www.evidentlyai.com/blog/llm-unit-testing-ci-cd-github-actions.
    Acesso em: 06 ago. 2026.
    — Evals reference-based e reference-free em datasets estruturados; captura de falhas silenciosas
    no primeiro commit.

22. NIST. *Artificial Intelligence Risk Management Framework: Generative AI Profile (AI RMF
    GenAI Profile)*. 2024. Disponível em: https://www.nist.gov/itl/ai-risk-management-framework.
    Acesso em: 06 ago. 2026.
    — Riscos específicos da IA generativa: alucinação, dados sintéticos, informações confidenciais,
    integração em cadeias de ferramentas.

23. ANTHROPIC. *Writing effective tools and tool use*. 2024. Disponível em:
    https://www.anthropic.com/engineering/writing-effective-tools. Acesso em: 06 ago. 2026.
    — Design de ferramentas com feedback de erro legível e testes; a ACI como superfície de ação.

24. LANGGRAPH / LANGCHAIN. *LangGraph: orchestration and testing of agentic workflows*. 2026.
    Disponível em: https://langchain-ai.github.io/langgraph/. Acesso em: 06 ago. 2026.
    — Orquestração de grafos de agentes; testes de fluxo, estado e recuperação de falhas.
