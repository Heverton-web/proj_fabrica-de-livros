# 1 Introdução

## 1.1 Contextualização do Problema

Entre 2024 e 2026, a engenharia de software atravessa uma mudança estrutural: modelos de linguagem de grande porte (LLMs) deixam de operar apenas como assistentes de autocomplete e passam a atuar como agentes autônomos capazes de planejar, executar e testar tarefas completas do ciclo de engenharia. A OpenAI documentou a transição para um "mundo agêntico" no qual a unidade fundamental de trabalho deixa de ser a chamada única ao modelo e passa a ser a execução orientada a tarefas, com o harness — a camada de engenharia que envolve o agente — assumindo o papel central de controle (OPENAI, 2026). Essa mudança é corroborada por dados de adoção: a LangChain reporta que 57% das organizações pesquisadas já possuem agentes em produção e que 89% priorizam observabilidade como requisito de operação (LANGCHAIN, 2026).

O problema de pesquisa decorre de uma lacuna conceitual: a difusão de ferramentas agênticas (Claude Code, Codex, Cursor) ocorre sem que a arquitetura interna que sustenta a autonomia desses sistemas seja amplamente compreendida por quem os adota. A distinção entre "ter um LLM" e "ter um agente confiável" é estrutural, não incidental: sem a camada de controle, a saída do modelo passa no teste de plausibilidade, mas falha em produção (BÖCKELER, 2026). A literatura emergente propõe tratar o harness como objeto de engenharia de primeira classe — uma coleção de práticas que inclui testes determinísticos, guardrails, gestão de contexto e observabilidade (TRIVEDY, 2026).

## 1.2 Objetivos

O objetivo geral deste artigo é analisar a revolução dos agentes e a anatomia do harness como artefato de engenharia, respondendo à questão: por que o modelo de linguagem, isoladamente, é insuficiente para garantir um sistema agêntico confiável? Os objetivos específicos são: (a) descrever a transição paradigmática do autocomplete para o agente; (b) detalhar as camadas do harness — âncora de testes, guardrails, corpo de contexto e trilha de observabilidade; (c) apresentar a herança do test harness da engenharia de software; e (d) discutir o papel do safety harness na prevenção de falhas de segurança.

## 1.3 Justificativa

A justificativa é dupla. Em termos práticos, a Gartner projeta que mais de 40% dos projetos de IA agêntica serão cancelados até 2027 por falta de retorno claro, e que 40% dos aplicativos empresariais contarão com agentes específicos de tarefa até 2026 — o que evidencia a urgência de critérios objetivos de engenharia para agentes (GARTNER, 2025). Em termos teóricos, o framework de "código como harness" propõe sistemas agênticos executáveis, verificáveis e com estado — uma agenda de pesquisa que ancora este trabalho (NING et al., 2026). O recorte adota o livro Harness Engineering — Do Modelo ao Sistema Autônomo Confiável como fonte primária, sintetizando seus quatro primeiros capítulos.

## 1.4 Delimitação

O estudo delimita-se à análise conceitual e arquitetural do harness, com foco em agentes de codificação e automação de engenharia. Não abrange a comparação empírica entre modelos de linguagem específicos, nem a avaliação de benchmarks de desempenho de agentes, que pertencem a trabalhos futuros.

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
