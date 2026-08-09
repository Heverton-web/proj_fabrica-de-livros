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

# 4 Conclusão

## 4.1 Síntese dos Achados

Este artigo respondeu à questão de pesquisa — por que o modelo de linguagem, isoladamente, é insuficiente para um sistema agêntico confiável — demonstrando que a confiabilidade reside no harness, não no modelo. A revolução dos agentes é, na prática, a revolução da engenharia de harness: a OpenAI documenta que a qualidade do resultado é determinada pela camada de engenharia que envolve o agente (OPENAI, 2026), e a anatomia em cinco camadas — âncora, capacete, corpo, motor e trilha — emergiu de forma consistente nas fontes analisadas (TRIVEDY, 2026; DATABRICKS, 2026; NING et al., 2026).

A herança do test harness da engenharia de software fornece o arcabouço metodológico: testes de contrato determinísticos substituem a avaliação intuitiva do comportamento do agente (NING et al., 2026). O safety harness adiciona a dimensão de segurança, endereçando riscos documentados como injeção de prompts, servidores MCP não confiáveis e enganação de aprovações humanas (OWASP, 2025; RED HAT, 2025; UTESVSKY, 2025).

## 4.2 Contribuições

O artigo contribui com: (a) uma síntese organizada da literatura emergente de harness engineering, integrando fontes institucionais, acadêmicas e de segurança; (b) um modelo de cinco camadas que oferece vocabulário comum para equipes que operam agentes; e (c) implicações práticas acionáveis — zona declarada por ferramenta, testes de contrato e observabilidade como requisito.

## 4.3 Limitações e Trabalhos Futuros

As limitações decorrem da natureza documental da pesquisa. Trabalhos futuros devem: (a) conduzir experimentos controlados comparando harnesses diferentes sobre o mesmo modelo; (b) avaliar quantitativamente o impacto de cada camada na taxa de sucesso de tarefas; (c) investigar a evolução das vulnerabilidades de segurança em agentes; e (d) desenvolver frameworks de medição de custo e qualidade de harness em escala de produção, respondendo ao apelo de relatórios como o DORA para práticas de engenharia mensuráveis (DORA, 2024).

# Referências

AI-BOOST. *Awesome Harness Engineering*. 2026. Disponível em: https://github.com/ai-boost/awesome-harness-engineering. Acesso em: 09 ago. 2026.

ALEITHAN, Ali et al. *SWE-Bench+: Enhanced Coding Benchmark for LLMs*. 2024. Disponível em: https://arxiv.org/abs/2410.06992. Acesso em: 09 ago. 2026.

ANTHROPIC. *Introducing the Model Context Protocol*. 2024. Disponível em: https://www.anthropic.com/news/model-context-protocol. Acesso em: 09 ago. 2026.

BÖCKELER, Birgitta. *Harness engineering for coding agent users*. 2026. Disponível em: https://martinfowler.com/articles/harness-engineering.html. Acesso em: 09 ago. 2026.

DATABRICKS ENGINEERING. *What is an AI Agent Harness?* 2026. Disponível em: https://www.databricks.com/blog/ai-harness. Acesso em: 09 ago. 2026.

DORA. *Accelerate State of DevOps Report 2024*. 2024. Disponível em: https://dora.dev/research/2024/dora-report/. Acesso em: 09 ago. 2026.

EMBRACE THE RED. *MCP: Untrusted Servers and Confused Clients, Plus a Sneaky Exploit*. 2025. Disponível em: https://embracethered.com/blog/posts/2025/model-context-protocol-security-risks-and-exploits/. Acesso em: 09 ago. 2026.

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
