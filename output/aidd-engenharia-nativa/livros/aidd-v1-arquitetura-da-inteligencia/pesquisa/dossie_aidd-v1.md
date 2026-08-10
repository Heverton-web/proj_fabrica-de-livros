# Dossiê de Pesquisa — Volume 1: A Arquitetura da Inteligência

## Conceitos-chave

- **AI Driven Development (AIDD)**: metodologia em que a IA não é assistente, mas o motor primário da geração e manutenção de código; o desenvolvedor transita de executor de código para **arquiteto de orquestração** que comanda um ecossistema de LLM, harness e protocolos.
- **Tela (Interface)**: ponto de contato humano-máquina — IDEs modernas, CLIs e chats especializados. É onde o desenvolvedor exerce controle cirúrgico sobre o fluxo.
- **Harness (A Armadura)**: camada de infraestrutura que envolve o LLM — gestão de contexto, memória de curto prazo, orquestração de chamadas e ferramentas. Harness engineering é a disciplina de desenhar essa armadura.
- **LLM (O Cérebro)**: os modelos de linguagem; critérios de seleção por tarefa, nuances de raciocínio e otimização de custo.
- **Tools (O Arsenal)**: como o agente interage com sistema de arquivos, terminal e APIs externas.
- **Context engineering**: otimizar a configuração de contexto (tokens) que alimenta o LLM para obter o comportamento desejado — a evolução natural do prompt engineering; trata contexto como recurso finito.
- **Economia severa de tokens**: estratégias para reduzir custo operacional sem perder densidade informativa (compaction, tool result clearing, notas estruturadas, carregamento just-in-time).
- **Compaction**: resumir a janela de contexto para preservar decisões arquiteturais e bugs não resolvidos, descartando saídas redundantes.
- **Harness coevolution**: harness e modelo evoluem juntos — componentes existem para compensar limitações do modelo e encolhem quando a limitação desaparece.

## Artigos Científicos e Papers

- LI, Jinzhe; WU, Yuan; CHANG, Yi. *Harness Engineering for LLM Agents: A Survey of Harness Component Taxonomy, Evaluation, and Model–Harness Coevolution*. 2026. Disponível em: https://doi.org/10.20944/preprints202606.2203.v1. Acesso em: 10 ago. 2026. (A)
- KIM, Jiun; HWANG, Hyuntae. *Harness Engineering: Deterministic Architectural Governance for AI-Driven Software Development*. 2026. Disponível em: https://doi.org/10.2139/ssrn.6372119. Acesso em: 10 ago. 2026. (A)
- CHEUNG, John. *Harness Resilience: From LLM Availability to Toolchain Continuity in Agentic AI Engineering*. 2026. Disponível em: https://doi.org/10.33774/coe-2026-4f53g. Acesso em: 10 ago. 2026. (A)
- MARCONATO, Emerson Alberto. *Modelo de arquitetura em camadas para interconexão de sistemas em SANT*. Disponível em: https://doi.org/10.11606/t.55.2017.tde-01022017-112311. Acesso em: 10 ago. 2026. (A)
- KAPFERER, Stefan; ZIMMERMANN, Olaf. *Domain-specific Language and Tools for Strategic Domain-driven Design, Context Mapping and Bounded Context Modeling*. In: Proceedings of the 8th International Conference on Model-Driven Engineering and Software Development. 2020. Disponível em: https://doi.org/10.5220/0008910502990306. Acesso em: 10 ago. 2026. (A)
- SEKAR, Srinivasan. *LLM-Centric Threats: Injection and Poisoning*. In: The MCP Standard. 2026. Disponível em: https://doi.org/10.1007/979-8-8688-2364-0_12. Acesso em: 10 ago. 2026. (A)

## Estado da arte / ferramentas de referência

- **Claude Code (Anthropic)**: agente de terminal que emprega a estratégia híbrida de contexto — CLAUDE.md carregado up front, glob/grep para navegação just-in-time. Disponível em: https://code.claude.com/docs/en/whats-new
- **Context engineering (Anthropic Engineering)**: guia oficial com compaction, note-taking estruturado e multi-agentes como técnicas de gestão de contexto. Disponível em: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- **Harness design (Anthropic Engineering)**: decomposição do build em pedaços tratáveis + artefatos estruturados para handoff de contexto entre sessões (planner/generator/evaluator). Disponível em: https://www.anthropic.com/engineering/harness-design-long-running-apps
- **Effective harnesses for long-running agents (Anthropic Engineering)**: padrões de harness para agentes de longa duração com context resets. Disponível em: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents

## Casos de uso corporativos

- **Agentes autônomos de codificação**: Claude Code e similares usam loop LLM-usando-ferramentas para análise, edição e teste de código em longas sessões.
- **Construção de aplicações full-stack multi-hora**: arquitetura de três agentes (planner, generator, evaluator) produz aplicações completas em sessões autônomas — caso real documentado pela Anthropic.
- **Operação com economia de tokens**: teams adotam compaction e carregamento just-in-time para cortar custo sem perder decisões de arquitetura.

## Limitações e controvérsias

- **Perda de coerência em tarefas longas**: o modelo degrada quando a janela de contexto enche; "context anxiety" faz agentes encerrar trabalho prematuramente.
- **Contexto é recurso finito**: desperdiçar tokens em ferramentas mal desenhadas ou busca em becos sem saída degrada a qualidade; a curadoria do contexto é o problema central.
- **Over-engineering de harness**: componentes compensam limitações do modelo; quando a limitação some, o componente vira peso morto — harness deve encolher (auditar premissas).
- **Injeção e envenenamento (LLM-Centric Threats)**: ameaças centradas no LLM exigem camadas de defesa no harness e nas tools.
- **Complexidade de harness não é trivial**: loops autônomos exigem condições de terminação explícitas, monitoramento de tokens e circuit breakers.

## Fontes brutas (para Nó 7 — Auditor de Rastreabilidade)

- LI, Jinzhe; WU, Yuan; CHANG, Yi. *Harness Engineering for LLM Agents: A Survey of Harness Component Taxonomy, Evaluation, and Model–Harness Coevolution*. Disponível em: https://doi.org/10.20944/preprints202606.2203.v1. Acesso em: 10 ago. 2026. (A)
- KIM, Jiun; HWANG, Hyuntae. *Harness Engineering: Deterministic Architectural Governance for AI-Driven Software Development*. Disponível em: https://doi.org/10.2139/ssrn.6372119. Acesso em: 10 ago. 2026. (A)
- CHEUNG, John. *Harness Resilience: From LLM Availability to Toolchain Continuity in Agentic AI Engineering*. Disponível em: https://doi.org/10.33774/coe-2026-4f53g. Acesso em: 10 ago. 2026. (A)
- MARCONATO, Emerson Alberto. *Modelo de arquitetura em camadas para interconexão de sistemas em SANT*. Disponível em: https://doi.org/10.11606/t.55.2017.tde-01022017-112311. Acesso em: 10 ago. 2026. (A)
- KAPFERER, Stefan; ZIMMERMANN, Olaf. *Domain-specific Language and Tools for Strategic Domain-driven Design, Context Mapping and Bounded Context Modeling*. Disponível em: https://doi.org/10.5220/0008910502990306. Acesso em: 10 ago. 2026. (A)
- SEKAR, Srinivasan. *LLM-Centric Threats: Injection and Poisoning*. Disponível em: https://doi.org/10.1007/979-8-8688-2364-0_12. Acesso em: 10 ago. 2026. (A)
- ANTHROPIC. *Effective context engineering for AI agents*. Disponível em: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents. Acesso em: 10 ago. 2026. (B)
- ANTHROPIC. *Harness design for long-running application development*. Disponível em: https://www.anthropic.com/engineering/harness-design-long-running-apps. Acesso em: 10 ago. 2026. (B)
- ANTHROPIC. *Effective harnesses for long-running agents*. Disponível em: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents. Acesso em: 10 ago. 2026. (B)
- ANTHROPIC. *Claude Code Documentation*. Disponível em: https://code.claude.com/docs/en/whats-new. Acesso em: 10 ago. 2026. (B)
