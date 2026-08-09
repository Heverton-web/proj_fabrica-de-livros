# 2 Metodologia

## 2.1 Natureza da Pesquisa

A pesquisa é de natureza qualitativa, exploratória e bibliográfica, com procedimento de análise de conteúdo sobre fontes primárias e secundárias publicadas entre 2022 e 2026. O corpus analisado inclui documentação oficial de ferramentas de agentes, artigos de engenharia de harness, relatórios institucionais de mercado e publicações de segurança de sistemas agênticos.

## 2.2 Coleta de Dados

A coleta seguiu três eixos complementares. O primeiro eixo compreende fontes institucionais: a documentação da OpenAI sobre harness engineering (OPENAI, 2026), o blog da LangChain sobre a anatomia do harness de agentes (TRIVEDY, 2026) e a análise da Databricks sobre o conceito de AI agent harness (DATABRICKS, 2026). O segundo eixo abrange a literatura acadêmica: o framework ReAct de raciocínio e ação (YAO et al., 2022), o benchmark SWE-bench para resolução de issues reais do GitHub (JIM et al., 2023), o SWE-Bench+ como extensão do benchmark (ALEITHAN et al., 2024) e a proposta de código como harness (NING et al., 2026). O terceiro eixo cobre segurança: o Top 10 da OWASP para aplicações de LLM (OWASP, 2025), a análise de riscos do Model Context Protocol (RED HAT, 2025) e as vulnerabilidades documentadas em agentes de codificação (UTESVSKY, 2025).

## 2.3 Critérios de Inclusão

Foram incluídas fontes que (a) tratam diretamente de arquitetura de agentes, harness, guardrails ou segurança de sistemas agênticos; (b) foram publicadas por organizações reconhecidas ou em veículos com revisão; e (c) possuem URL verificável. Fontes exclusivamente comerciais sem conteúdo técnico foram descartadas.

## 2.4 Procedimento de Análise

A análise estruturou-se em três etapas. Na primeira, o material coletado foi organizado por tema em um dossiê de pesquisa com hierarquia de fontes (primárias A, secundárias B e terciárias C). Na segunda, os conceitos foram mapeados para as cinco camadas do harness: âncora (testes determinísticos), capacete (guardrails), corpo (gestão de contexto), motor (loop de execução) e trilha (observabilidade). Na terceira, procedeu-se à síntese comparativa entre as abordagens documentadas, seguindo o método ACAD de contextualização, referencial teórico, análise e síntese parcial (NING et al., 2026; HU, 2026).

## 2.5 Limitações

A pesquisa limita-se à análise documental; não foram conduzidos experimentos controlados com agentes reais. A rápida evolução do campo implica que parte das fontes de 2025 e 2026 pode se tornar obsoleta em curto prazo, o que é mitigado pela triangulação entre fontes de naturezas distintas.

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
