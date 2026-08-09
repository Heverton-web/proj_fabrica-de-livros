# 1 Introdução

## 1.1 Contextualização do Problema

O ciclo de execução é a unidade fundamental do trabalho agêntico. Diferentemente da chamada única a um modelo de linguagem, a operação de um agente em produção é um loop: raciocinar, agir, observar e repetir, com a observação realimentando o contexto da próxima decisão. O framework ReAct, formalizado por Yao e colaboradores, demonstrou que a alternância entre raciocínio e ação supera modos isolados em tarefas que exigem conhecimento externo e múltiplos passos (YAO et al., 2022). Essa constatação, combinada com a tese da OpenAI de que a qualidade do resultado é determinada pelo harness e não pelo modelo (OPENAI, 2026), coloca o loop de execução — e o controle do que o agente pode fazer — no centro da engenharia de sistemas agênticos.

A relevância do problema é quantificável: 57% das organizações pesquisadas já operam agentes em produção, e execuções únicas de longa duração — de até seis horas — são documentadas na operação real (LANGCHAIN, 2026; OPENAI, 2026). Nesse cenário, decisões de engenharia aparentemente menores — política de retentativa, tratamento de erro, permissões de execução, isolamento de ambiente — determinam se o agente conclui a tarefa, queima tokens em um loop infinito ou causa dano por executar fora do escopo (HU, 2026).

## 1.2 Objetivos

O objetivo geral deste artigo é analisar o ciclo ReAct e os mecanismos de sandbox, permissões e controle de execução como componentes do harness, respondendo à questão: como o harness garante que o agente execute tarefas longas de forma eficiente, segura e auditável? Os objetivos específicos são: (a) descrever a arquitetura do loop ReAct com observação estruturada; (b) analisar as políticas de retentativa com backoff, limite e escalação; (c) examinar os modelos de sandbox e zonas de execução; e (d) discutir a separação entre intenção do modelo e declaração de política do engenheiro.

## 1.3 Justificativa

A justificativa decorre do custo da ausência de controle. O relatório da LangChain indica que a observabilidade e o controle de execução são prioridades declaradas de 89% das organizações que operam agentes (LANGCHAIN, 2026). No campo da segurança, vulnerabilidades documentadas em agentes de codificação — incluindo a enganação de prompts de aprovação humana e o envenenamento de ferramentas MCP — demonstram que a execução sem isolamento e sem política é a principal superfície de ataque (UTESVSKY, 2025; RED HAT, 2025). A OWASP situa a confiança excessiva em saídas do modelo e o controle inadequado entre os riscos críticos de aplicações de LLM (OWASP, 2025).

## 1.4 Delimitação

O estudo delimita-se ao loop de execução e ao controle de execução de agentes de engenharia de software. Não aborda a comparação de eficiência entre modelos de linguagem, nem a avaliação de benchmarks de desempenho, que pertencem a trabalhos futuros.

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
