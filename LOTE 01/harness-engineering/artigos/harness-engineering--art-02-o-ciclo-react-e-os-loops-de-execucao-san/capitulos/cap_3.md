# 3 Resultados e Discussão

## 3.1 A Arquitetura do Loop ReAct

A análise confirma que o loop ReAct é o padrão canônico de execução agêntica. Em cada iteração, o agente recebe o contexto atual (instrução mais histórico de ações e observações), decide o próximo passo — raciocinar ou invocar uma ferramenta — e o harness executa a ação, devolvendo a observação estruturada como novo contexto (YAO et al., 2022). A decisão arquitetural central é que quem executa não é o modelo, mas o harness: o modelo propõe, o harness executa e devolve a realidade (OPENAI, 2026; BÖCKELER, 2026). Essa separação é o que permite observar, registrar e controlar cada ação.

Um achado relevante é a distinção entre observação estruturada e texto livre: o loop precisa diferenciar "a ferramenta respondeu 5" de "a ferramenta quebrou". A literatura de design de harnesses enfatiza o contrato estruturado de saída — sucesso, dados e erro separados — como condição para que o loop decida com informação (HU, 2026; NING et al., 2026). Erros tratados como dados (registrar "503" como conteúdo da resposta) fazem o agente raciocinar sobre um erro como se fosse fato, perpetuando o desvio.

## 3.2 Política de Retentativa e Escalação

O tratamento de erro é o teste real do harness. A análise identificou três componentes da política madura de retentativa: backoff exponencial para falhas transitórias, limite de tentativas para nunca gastar sem teto e escalação para humano quando o limite é atingido (HU, 2026). A ausência de política produz os dois erros opostos documentados na operação real: retry infinito em falha permanente, queimando tokens sem observação nova, e desistência precoce em falha transitória, entregando resultado incompleto (OPENAI, 2026). Execuções de até seis horas, documentadas em produção, só sobrevivem com política de erro robusta (OPENAI, 2026; LANGCHAIN, 2026).

## 3.3 Sandbox e Zonas de Execução

O segundo eixo do estudo — isolamento e permissões — revelou o modelo de três zonas como solução de referência: zona segura (execução livre), zona controlada (execução condicionada a políticas automáticas) e zona sensível (aprovação humana explícita e registrada) (HU, 2026; TRIVEDY, 2026). O achado mais importante é a separação entre intenção e declaração: a zona de uma ferramenta é declarada na configuração, antes da execução, e não decidida pela conversa. Essa separação impede o golpe de prompt — o adversário manipula a conversa, não a declaração — e torna o controle auditável (UTESVSKY, 2025; RED HAT, 2025).

## 3.4 Segurança da Execução

A literatura de segurança corrobora a necessidade do isolamento. O Model Context Protocol, adotado como padrão de conexão de ferramentas, apresenta riscos de servidores não confiáveis e clientes confusos que tornam a execução de ferramentas sem política um vetor de ataque (RED HAT, 2025; EMBRACE THE RED, 2025). Vulnerabilidades documentadas em cinco agentes de codificação demonstraram que prompts de aprovação podem ser enganados (UTESVSKY, 2025). A OWASP consolida o risco de confiança excessiva em saídas do modelo como um dos principais perigos de aplicações de LLM (OWASP, 2025). Esses achados sustentam que o controle de execução não é uma camada de conveniência, mas de segurança.

## 3.5 Implicações Práticas

As implicações práticas são diretas. Primeiro, toda execução de ferramenta deve passar por um ponto único controlado, com observação estruturada e registro (NING et al., 2026). Segundo, a política de retry deve combinar backoff, limite e escalação — nunca retry infinito (HU, 2026). Terceiro, a zona de cada ferramenta deve ser declarada na configuração, não decidida na conversa (UTESVSKY, 2025). Quarto, a trilha de execução deve permitir auditoria completa, com métricas de custo e sucesso — requisito declarado por 89% das organizações que operam agentes em produção (LANGCHAIN, 2026).

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
