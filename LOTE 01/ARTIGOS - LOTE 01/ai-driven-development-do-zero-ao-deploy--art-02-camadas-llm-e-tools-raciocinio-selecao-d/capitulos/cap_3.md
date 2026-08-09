# 3 Resultados e Discussão

A síntese do dossiê-mãe aplicada a este recorte permite organizar os achados em três blocos que correspondem aos pilares anunciados na introdução: o raciocínio do LLM e a seleção de ferramentas com efeito real no mundo; a orquestração via skills, subagentes e MCP; e o contrato de configuração entre humano e agente.

## 3.1 Raciocínio, Seleção de Ferramentas e Efeito Real no Mundo

Anthropic descreve a construção de agentes eficazes como um problema de composição de blocos simples e testáveis, e não de arquiteturas monolíticas complexas (ANTHROPIC, 2024). Estruturas de raciocínio como chain-of-thought guiam o modelo por um processo de decomposição passo a passo antes de agir (IBM, 2026), enquanto ReAct, Tree of Thoughts e Reflexion fornecem o andaime que transforma um modelo capaz em um agente confiável, capaz de revisar sua própria trajetória de decisão (PROMPTING, 2026; PROMPTHUB, 2026; COMET, 2026). Esse raciocínio, porém, só produz efeito no mundo real quando acoplado a um mecanismo de chamada de função (function calling): a documentação técnica converge no ponto de que ferramentas devem ser tratadas como parte do prompt, com o mesmo esforço de especificação dedicado à redação do prompt em si — nome, descrição e esquema de cada ferramenta influenciam diretamente a taxa de acerto de seleção (HARTENFELLER, 2026; BLAXEL, 2026).

A saída estruturada (structured output), forçada por esquema JSON, emerge como prática obrigatória para tornar o parsing da decisão do modelo confiável (AGENTA, 2026; PROMPTLAYER, 2025), e a chamada de função programática — em que o modelo gera código que invoca ferramentas em vez de emitir uma única chamada por turno — reduz o número de idas e vindas entre modelo e ambiente de execução (PROGRAMMATIC, 2026). O ponto de maior tensão nesta camada, contudo, é de segurança: validação de toda saída de chamada de função antes da execução e checagem de esquema são práticas obrigatórias, não opcionais, porque operações sensíveis não podem depender exclusivamente do raciocínio do LLM para se autolimitar — exigem regras de validação determinísticas independentes (SENTRY, 2026). Pesquisa recente documenta ataques de manipulação da seleção de ferramentas, em que a ordem, nomenclatura ou descrição das ferramentas disponíveis é explorada para induzir o agente a escolher uma ferramenta diferente da pretendida (TOOLTWEAK, 2025), e uma avaliação comparativa de vulnerabilidade em paradigmas de implantação de agentes LLM aponta que o "efeito real no mundo" de uma chamada de ferramenta — gravar um arquivo, disparar um deploy, mover dinheiro — é exatamente o que torna esse subsistema o de maior custo de falha de toda a arquitetura (BRIDGING, 2025).

## 3.2 Skills, Subagentes e MCP: a Camada de Orquestração

A camada de orquestração resolve um problema distinto: como distribuir trabalho entre unidades especializadas sem que cada uma precise reconstruir o contexto do zero. Skills empacotam instruções, metadados e recursos opcionais que o modelo invoca automaticamente quando relevante (SKILLS, 2026), enquanto subagentes são instâncias isoladas disparadas pela sessão principal para trabalhar em paralelo, cada uma com sua própria janela de contexto, permissões e modelo — a propriedade definidora de um subagente é justamente começar com contexto limpo, sem acesso ao histórico da thread-mãe (TOTALUM, 2026; KONISHI, 2026). Em 2026, esse padrão evoluiu para *dynamic workflows*, nos quais um agente líder pode planejar e disparar dezenas a centenas de subagentes paralelos em uma única sessão, avaliados por um sistema separado de aferição de desempenho (ORCHESTRATE, 2026). Frameworks de orquestração mais amplos — LangGraph, CrewAI, AutoGen — formalizam padrões equivalentes de encadeamento de prompt, roteamento e composição orquestrador-trabalhadores (SUBAGENT, 2026).

O Model Context Protocol (MCP) é o padrão que amarra essa camada às ferramentas e fontes de dados externas, substituindo integrações fragmentadas por um protocolo único (MCP, 2026; WIKIPEDIA, 2026; WEBFUSE, 2026). Sua neutralidade em relação a fornecedor — reforçada pela doação do protocolo a uma fundação neutra sob a Linux Foundation — não elimina, contudo, um vetor de risco documentado extensivamente pela comunidade de segurança: o *tool poisoning*, em que instruções maliciosas são embutidas diretamente na descrição de uma ferramenta MCP e injetadas no contexto do LLM durante o registro, sem se assemelhar à injeção de prompt tradicional (OWASP, 2026). Esse achado é corroborado por múltiplas fontes independentes: análises de "raio de impacto" (blast radius) de servidores MCP comprometidos (APTIBLE, 2026), o relato pioneiro de Simon Willison sobre problemas estruturais de segurança do protocolo (WILLISON, 2025), um guia de boas práticas de segurança agêntica em MCP produzido pela Cloud Security Alliance (CLOUD, 2026) e uma sistematização acadêmica de conhecimento sobre segurança e salvaguardas no ecossistema MCP (SYSTEMATIZATION, 2025). A convergência dessas fontes sugere que a camada de orquestração, por multiplicar o número de pontos de entrada de ferramentas de terceiros, multiplica proporcionalmente a superfície de ataque disponível a um agente autônomo.

## 3.3 CLAUDE.md, AGENTS.md e o Contrato de Configuração

A terceira camada regula o que o agente pode e deve fazer dentro de um projeto específico. Arquivos CLAUDE.md fornecem contexto e instruções de projeto, mas exigem configuração explícita para ser carregados automaticamente; AGENTS.md funciona como padrão de fallback multi-ferramenta, permitindo que uma única especificação sirva a diferentes IDEs e CLIs agênticas (DEPLOYHQ, 2026). A convergência prática recomendada por múltiplas fontes é manter esses arquivos concisos — abaixo de algumas centenas de linhas —, porque a capacidade de seguimento confiável de instruções de um LLM frontier é finita, e o próprio prompt de sistema do harness já consome parcela relevante desse orçamento (HUMANLAYER, 2025; HOOKS, 2026; MODIFYING, 2026).

A engenharia de prompt para agentes de código, nesse contexto, deixou de ser apenas escolha de palavras: a Anthropic descreve a evolução necessária para *context engineering* — o conjunto de estratégias para curar e manter o conjunto ótimo de tokens durante a inferência, incluindo toda informação que chega à janela de contexto fora do prompt propriamente dito (ANTHROPIC, 2025). Um guia complementar sobre a construção de harnesses eficazes para agentes de longa duração recomenda estruturas de prompt diferenciadas entre a primeiríssima janela de contexto e janelas subsequentes em fluxos multi-janela (ANTHROPIC, 2026). Técnicas de gestão de comprimento de contexto — sumarização incremental, poda de histórico, recuperação seletiva — aparecem como resposta direta ao problema de *overflow* de janela em sessões longas (REDIS, 2026; REDIS, 2025; LUHARUKA, 2026), e a preferência documentada de agentes de codificação por ferramentas de busca leves como grep/ripgrep, em vez de indexação semântica pesada, ilustra como a economia de tokens se tornou um critério de design tão relevante quanto a precisão de busca (CODEANT, 2026; YAGE, 2026).

## 3.4 Discussão Integrada: onde as Três Camadas se Tocam

O achado transversal deste recorte é que as três camadas não operam isoladamente: uma configuração de CLAUDE.md mal escrita pode induzir o LLM a selecionar a ferramenta errada mesmo com raciocínio correto; uma skill mal documentada equivale, na prática, a uma ferramenta com esquema ambíguo, reproduzindo o mesmo risco de seleção incorreta descrito para function calling (TOOLTWEAK, 2025); e um servidor MCP comprometido explora exatamente a confiança que a camada de orquestração deposita nas descrições de ferramenta como parte do contrato entre humano e agente (OWASP, 2026; GITINJECT, 2026). Casos corporativos documentados de integração de agentes em CI/CD — revisão de pull request, reparo de testes, triagem de falhas de build e remediação de segurança — mantêm, em todos os relatos revisados, um portão de aprovação humana antes do deploy em produção precisamente porque nenhuma das três camadas, isoladamente, oferece garantia suficiente de segurança para dispensar essa checagem (GOVERNED, 2026; FORRESTER, 2026). Ferramentas concorrentes como o GitHub Copilot em modo agente adotam a mesma lógica de escalonamento de decisões consequentes ao humano (GITHUB, 2025; VISUAL STUDIO CODE, 2025), reforçando que a tensão entre autonomia e controle não é peculiaridade de uma única plataforma, mas uma característica estrutural da arquitetura de três camadas aqui descrita.

# Referências

AGENTA. *The guide to structured outputs and function calling with LLMs*. 2026. Disponível em: https://agenta.ai/blog/the-guide-to-structured-outputs-and-function-calling-with-llms. Acesso em: 02 ago. 2026.

ANTHROPIC. *Building Effective AI Agents*. 2024. Disponível em: https://www.anthropic.com/research/building-effective-agents. Acesso em: 02 ago. 2026.

ANTHROPIC. *Effective context engineering for AI agents*. 2025. Disponível em: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents. Acesso em: 02 ago. 2026.

ANTHROPIC. *Effective harnesses for long-running agents*. 2026. Disponível em: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents. Acesso em: 02 ago. 2026.

APTIBLE. *Prompt Injection in MCP: Tool Poisoning and Blast Radius*. 2026. Disponível em: https://www.aptible.com/mcp-security/mcp-prompt-injection. Acesso em: 02 ago. 2026.

BLAXEL. *What Is LLM Function Calling?*. 2026. Disponível em: https://blaxel.ai/blog/what-is-llm-function-calling. Acesso em: 02 ago. 2026.

BRIDGING AI and Software Security: A Comparative Vulnerability Assessment of LLM Agent Deployment Paradigms. ARXIV.ORG, 2025. Disponível em: https://arxiv.org/pdf/2507.06323. Acesso em: 02 ago. 2026.

CLOUD SECURITY ALLIANCE. *Agentic MCP Security Best Practices Guide*. 2026. Disponível em: https://labs.cloudsecurityalliance.org/agentic/agentic-mcp-security-best-practices-v1/. Acesso em: 02 ago. 2026.

CODEANT. *Why Your Coding Agent Should Use ripgrep (rg) Instead of grep*. 2026. Disponível em: https://codeant.ai/blogs/why-coding-agents-should-use-ripgrep. Acesso em: 02 ago. 2026.

COMET. *Prompt Engineering for Agentic AI Systems: An Introduction*. 2026. Disponível em: https://www.comet.com/site/blog/prompt-engineering/. Acesso em: 02 ago. 2026.

DEPLOYHQ. *CLAUDE.md, AGENTS.md & Copilot Instructions: Configure Every AI Coding Assistant*. 2026. Disponível em: https://www.deployhq.com/blog/ai-coding-config-files-guide. Acesso em: 02 ago. 2026.

FORRESTER. *Agentic Software Development Takes The Lead: From Code Assistants To Orchestrated SDLC Agents*. 2026. Disponível em: https://www.forrester.com/blogs/agentic-software-development-takes-the-lead-from-code-assistants-to-orchestrated-sdlc-agents/. Acesso em: 02 ago. 2026.

GITHUB. *Agent mode 101: All about GitHub Copilot's powerful mode*. 2025. Disponível em: https://github.blog/ai-and-ml/github-copilot/agent-mode-101-all-about-github-copilots-powerful-mode/. Acesso em: 02 ago. 2026.

GITINJECT: Real-World Prompt Injection Attacks in AI-Powered CI/CD Pipelines. ARXIV.ORG, 2026. Disponível em: https://arxiv.org/pdf/2606.09935. Acesso em: 02 ago. 2026.

GOVERNED AI-Assisted Engineering: Graduated Human Oversight for Agentic Code Generation in Regulated Domains. ARXIV.ORG, 2026. Disponível em: https://arxiv.org/pdf/2606.22484. Acesso em: 02 ago. 2026.

HARTENFELLER. *Best Practices for LLM Tools or Function Calling for Oracle Developers*. 2026. Disponível em: https://hartenfeller.dev/blog/ai-tools-best-practice-oracle. Acesso em: 02 ago. 2026.

HOOKS reference. ANTHROPIC, Claude Code Docs, 2026. Disponível em: https://code.claude.com/docs/en/hooks. Acesso em: 02 ago. 2026.

HUMANLAYER. *Writing a good CLAUDE.md*. 2025. Disponível em: https://www.humanlayer.dev/blog/writing-a-good-claude-md. Acesso em: 02 ago. 2026.

IBM. *What is chain of thought (CoT) prompting?*. 2026. Disponível em: https://www.ibm.com/think/topics/chain-of-thoughts. Acesso em: 02 ago. 2026.

KONISHI, Hidekazu. *Claude Code Subagents and Multi-Agent Orchestration Guide*. 2026. Disponível em: https://hidekazu-konishi.com/entry/claude_code_subagents_and_orchestration_guide.html. Acesso em: 02 ago. 2026.

LUHARUKA, Shubham. *Context Optimization: A Comprehensive Framework for Reducing Large Language Model Token Usage*. 2026. Disponível em: https://luharuka.medium.com/context-optimization-a-comprehensive-framework-for-reducing-large-language-model-token-usage-fed8d9229e30. Acesso em: 02 ago. 2026.

MCP. *Specification and documentation for the Model Context Protocol*. 2026. Disponível em: https://github.com/modelcontextprotocol/modelcontextprotocol. Acesso em: 02 ago. 2026.

MODIFYING system prompts. ANTHROPIC, Claude API Docs, 2026. Disponível em: https://platform.claude.com/docs/en/agent-sdk/modifying-system-prompts. Acesso em: 02 ago. 2026.

ORCHESTRATE subagents at scale with dynamic workflows. ANTHROPIC, Claude Code Docs, 2026. Disponível em: https://code.claude.com/docs/en/workflows. Acesso em: 02 ago. 2026.

OWASP FOUNDATION. *MCP Tool Poisoning*. 2026. Disponível em: https://owasp.org/www-community/attacks/MCP_Tool_Poisoning. Acesso em: 02 ago. 2026.

PROGRAMMATIC tool calling. ANTHROPIC, Claude Platform Docs, 2026. Disponível em: https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling. Acesso em: 02 ago. 2026.

PROMPTHUB. *Prompt Engineering for AI Agents*. 2026. Disponível em: https://www.prompthub.us/blog/prompt-engineering-for-ai-agents. Acesso em: 02 ago. 2026.

PROMPTING GUIDE. *Tree of Thoughts (ToT)*. 2026. Disponível em: https://www.promptingguide.ai/techniques/tot. Acesso em: 02 ago. 2026.

PROMPTLAYER. *How JSON Schema Works for LLM Tools & Structured Outputs*. 2025. Disponível em: https://blog.promptlayer.com/how-json-schema-works-for-structured-outputs-and-tool-integration/. Acesso em: 02 ago. 2026.

REDIS. *Context Window Overflow in 2026: Fix LLM Errors Fast*. 2026. Disponível em: https://redis.io/blog/context-window-overflow/. Acesso em: 02 ago. 2026.

REDIS. *Context Window Management for LLM Apps: Dev Guide*. 2025. Disponível em: https://redis.io/blog/context-window-management-llm-apps-developer-guide/. Acesso em: 02 ago. 2026.

SENTRY. *Exploiting Tool and Function Calling in LLM Agents*. 2026. Disponível em: https://blog.sentry.security/exploiting-tool-and-function-calling-in-llm-agents/. Acesso em: 02 ago. 2026.

SKILLS. Agent Skills — Claude Platform Docs. ANTHROPIC, 2026. Disponível em: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview. Acesso em: 02 ago. 2026.

SUBAGENT Orchestration Guide — Claude Code Skill. MCP MARKET, 2026. Disponível em: https://mcpmarket.com/tools/skills/subagent-orchestration-guide-1. Acesso em: 02 ago. 2026.

SYSTEMATIZATION of Knowledge: Security and Safety in the Model Context Protocol Ecosystem. ARXIV.ORG, 2025. Disponível em: https://arxiv.org/pdf/2512.08290. Acesso em: 02 ago. 2026.

TOOLTWEAK: An Attack on Tool Selection in LLM-based Agents. ARXIV.ORG, 2025. Disponível em: https://arxiv.org/pdf/2510.02554. Acesso em: 02 ago. 2026.

TOTALUM. *Claude Code subagents: the 2026 production playbook*. 2026. Disponível em: https://www.totalum.app/blog/claude-code-subagents-totalum. Acesso em: 02 ago. 2026.

VISUAL STUDIO CODE. *Introducing GitHub Copilot agent mode (preview)*. 2025. Disponível em: https://code.visualstudio.com/blogs/2025/02/24/introducing-copilot-agent-mode. Acesso em: 02 ago. 2026.

WEBFUSE. *MCP Cheat Sheet: Model Context Protocol Quick Reference*. 2026. Disponível em: https://www.webfuse.com/mcp-cheat-sheet. Acesso em: 02 ago. 2026.

WIKIPEDIA. *Model Context Protocol*. 2026. Disponível em: https://en.wikipedia.org/wiki/Model_Context_Protocol. Acesso em: 02 ago. 2026.

WILLISON, Simon. *Model Context Protocol has prompt injection security problems*. 2025. Disponível em: https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/. Acesso em: 02 ago. 2026.

YAGE.AI. *Why Coding Agents Still Use grep as Their Search Backbone*. 2026. Disponível em: https://yage.ai/share/why-coding-agents-still-use-grep-en-20260327.html. Acesso em: 02 ago. 2026.
