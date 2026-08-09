# 3 Resultados e Discussão

## 3.1 A Insuficiência do Modelo Isolado

A análise documental confirma que o modelo de linguagem, isoladamente, é insuficiente para a operação agêntica confiável. A OpenAI argumenta que o harness é o determinante da qualidade do resultado: o mesmo modelo, dentro de harnesses diferentes, produz resultados com qualidade diferente (OPENAI, 2026). Essa tese é corroborada pelo benchmark SWE-bench, que demonstrou que sistemas que combinam raciocínio e ação superam abordagens que usam apenas um dos modos (JIM et al., 2023). A explicação é arquitetural: o modelo propõe ações, mas quem executa é o harness — e é na execução que o sistema encontra o mundo real, não determinístico (BÖCKELER, 2026; HU, 2026).

## 3.2 A Anatomia do Harness em Cinco Camadas

A síntese das fontes revelou consistência na descrição de cinco camadas do harness, corroborada por múltiplos autores independentes (TRIVEDY, 2026; DATABRICKS, 2026; NING et al., 2026):

1. **Âncora (testes determinísticos)**: casos de teste que definem o comportamento esperado do agente e bloqueiam regressões antes da execução em produção. A herança vem do test harness da engenharia de software, que há décadas automatiza a verificação de comportamento.
2. **Capacete (guardrails)**: políticas automáticas que classificam ações como permitidas, controladas ou sensíveis, bloqueando as fora de escopo. A OWASP inclui o controle inadequado de ações entre os principais riscos de aplicações de LLM (OWASP, 2025).
3. **Corpo (gestão de contexto)**: o contexto do agente é um recurso finito que precisa ser gerenciado — selecionar o que entra, o que sai e o que é sumarizado a cada iteração (NING et al., 2026).
4. **Motor (loop de execução)**: o ciclo ReAct de raciocínio, ação e observação, com política de retentativa e escalação para humano (YAO et al., 2022).
5. **Trilha (observabilidade)**: registro estruturado de cada passo — ação, observação, custo e decisão — que permite auditoria e diagnóstico (LANGCHAIN, 2026).

## 3.3 A Herança do Test Harness

A análise revelou que o harness de agentes é, em grande medida, uma extensão do test harness clássico da engenharia de software. A diferença fundamental é o objeto sob teste: em vez de funções com entradas e saídas determinísticas, o objeto é um agente cujo comportamento é probabilístico. Isso exige testes de contrato — entrada canônica, saída verificável, efeitos colaterais esperados e comportamento de erro — em vez de simples testes de igualdade (NING et al., 2026). A literatura de qualidade de software reforça que o teste é o que torna o agente auditável: sem âncora determinística, o agente "funciona" até o dia em que erra em silêncio (BÖCKELER, 2026).

## 3.4 O Safety Harness e a Segurança

A discussão de segurança ocupa posição central na literatura. A OWASP destaca a injeção de prompts e a confiança excessiva em saídas do modelo entre os riscos mais críticos (OWASP, 2025). O Model Context Protocol, adotado como padrão para conectar agentes a ferramentas, apresenta riscos documentados de servidores não confiáveis e clientes confusos (RED HAT, 2025). A pesquisa de segurança demonstrou vulnerabilidades reais em agentes de codificação, incluindo a enganação dos prompts de aprovação humana (UTESVSKY, 2025) e o envenenamento de ferramentas MCP. Esses achados sustentam a tese de que o safety harness — a camada que impede a queda — não é opcional, mas componente estrutural da arquitetura.

## 3.5 Implicações Práticas

As implicações práticas derivam diretamente dos achados. Em primeiro lugar, organizações que adotam agentes devem tratar o harness como produto, com fila de melhorias e métricas, e não como tarefa pontual (LANGCHAIN, 2026). Em segundo lugar, a classificação de ações em zonas (segura, controlada, sensível) deve ser declarada nas ferramentas, antes da execução, e não decidida na conversa — separando a intenção do modelo da declaração do engenheiro (UTESVSKY, 2025; HU, 2026). Em terceiro lugar, a observabilidade deve ser tratada como requisito de primeira classe: 89% das organizações que operam agentes em produção priorizam essa camada (LANGCHAIN, 2026).

# Referências

AI-BOOST. *Awesome Harness Engineering*. 2026. Disponível em: https://github.com/ai-boost/awesome-harness-engineering. Acesso em: 09 ago. 2026.

ALEITHAN, Ali et al. *SWE-Bench+: Enhanced Coding Benchmark for LLMs*. 2024. Disponível em: https://arxiv.org/abs/2410.06992. Acesso em: 09 ago. 2026.

ANTHROPIC. *Introducing the Model Context Protocol*. 2024. Disponível em: https://www.anthropic.com/news/model-context-protocol. Acesso em: 09 ago. 2026.

BÖCKELER, Birgitta. *Harness engineering for coding agent users*. 2026. Disponível em: https://martinfowler.com/articles/harness-engineering.html. Acesso em: 09 ago. 2026.

DATABRICKS ENGINEERING. *What is an AI Agent Harness?* 2026. Disponível em: https://www.databricks.com/blog/ai-harness. Acesso em: 09 ago. 2026.

DORA. *Accelerate State of DevOps Report 2024*. 2024. Disponível em: https://dora.dev/research/2024/dora-report/. Acesso em: 09 ago. 2026.

EMBRACE THE RED. *MCP: Untrusted Servers and Confused Clients, Plus a Sneaky Exploit*. 2025. Disponível em: https://embracethered.com/blog/posts/2025/model-context-protocol-security-risks-and-exploits/. Acesso em: 09 ago. 2026.

GARTNER. 2025. *Gartner Predicts Over 40 Percent of Agentic AI Projects Will Be Canceled by End of 2027*. Disponível em: https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027. Acesso em: 09 ago. 2026.

GARTNER. 2025. *Gartner Predicts 40 Percent of Enterprise Apps Will Feature Task-Specific AI Agents by 2026*. Disponível em: https://www.gartner.com/en/newsroom/press-releases/2025-08-26-gartner-predicts-40-percent-of-enterprise-apps-will-feature-task-specific-ai-agents-by-2026-up-from-less-than-5-percent-in-2025. Acesso em: 09 ago. 2026.

HU, W. *Architectural Design Decisions in AI Agent Harnesses*. 2026. Disponível em: https://arxiv.org/html/2604.18071v1. Acesso em: 09 ago. 2026.

JIM, Carlos et al. *SWE-bench: Can Language Models Resolve Real-world GitHub Issues?* 2023. Disponível em: https://arxiv.org/abs/2310.06770. Acesso em: 09 ago. 2026.

LANGCHAIN. *State of Agent Engineering 2026*. 2026. Disponível em: https://www.langchain.com/state-of-agent-engineering. Acesso em: 09 ago. 2026.

LASSO SECURITY (OXENBERG, O.; SUISA, E.). *Claude Code Security: Protect Autonomous Coding Agents*. 2025. Disponível em: https://www.lasso.security/blog/claude-code-security. Acesso em: 09 ago. 2026.

NING, X. et al. *Code as Agent Harness: Toward Executable, Verifiable, and Stateful Agent Systems*. 2026. Disponível em: https://arxiv.org/html/2605.18747v1. Acesso em: 09 ago. 2026.

OPENAI. *Harness engineering: leveraging Codex in an agent-first world*. 2026. Disponível em: https://openai.com/index/harness-engineering/. Acesso em: 09 ago. 2026.

OWASP FOUNDATION. *OWASP Top 10 for Large Language Model Applications*. 2025. Disponível em: https://owasp.org/www-project-top-10-for-large-language-model-applications/. Acesso em: 09 ago. 2026.

RED HAT PRODUCT SECURITY (CANO GABARDA, F.). *Model Context Protocol (MCP): Understanding security risks and controls*. 2025. Disponível em: https://www.redhat.com/en/blog/model-context-protocol-mcp-understanding-security-risks-and-controls. Acesso em: 09 ago. 2026.

TRIVEDY, Vivek. *The Anatomy of an Agent Harness*. 2026. Disponível em: https://www.langchain.com/blog/the-anatomy-of-an-agent-harness. Acesso em: 09 ago. 2026.

UTESVSKY, Roy. *SymJack: The approval prompt is lying to you*. 2025. Disponível em: https://adversa.ai/blog/the-approval-prompt-is-lying-to-you-symlink-rce-in-five-ai-coding-agents-claude-code-cursor-antigravity-copilot-grok-build/. Acesso em: 09 ago. 2026.

WIKIPEDIA. *Model Context Protocol*. 2024. Disponível em: https://en.wikipedia.org/wiki/Model_Context_Protocol. Acesso em: 09 ago. 2026.

YAO, Shunyu et al. *ReAct: Synergizing Reasoning and Acting in Language Models*. 2022. Disponível em: https://arxiv.org/abs/2210.03629. Acesso em: 09 ago. 2026.
