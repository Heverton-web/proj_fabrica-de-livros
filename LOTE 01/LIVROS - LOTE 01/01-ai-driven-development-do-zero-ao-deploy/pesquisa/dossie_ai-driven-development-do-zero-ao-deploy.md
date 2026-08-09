
# Dossiê Técnico — AI Driven Development: Do Zero ao Deploy

**Slug:** `livros/ai-driven-development-do-zero-ao-deploy`
**Data de pesquisa:** 02 ago. 2026
**Pesquisador:** subagente-pesquisador
**Tamanho da obra:** G (5 Partes, 10 capítulos, ~150 páginas)

Este dossiê cobre 8 blocos temáticos, cada um alimentando uma ou mais Partes do
sumário macro da obra. A pesquisa foi ampliada para sustentar 10 capítulos com
no mínimo 20 referências técnicas cada — a lista consolidada de "Fontes Brutas"
ao final contém mais de 80 itens verificáveis, permitindo distribuição sem
repetição excessiva entre capítulos.

---

## 1. Estado da Arte

### 1.1 [Bloco 1] Fundamentos de AI Driven Development

A indústria de desenvolvimento de software atravessa, entre 2024 e 2026, uma
mudança estrutural comparável à adoção do DevOps e do Agile: LLMs deixam de
operar como "autocomplete avançado" (paradigma *vibe coding*, em que o
desenvolvedor permanece no loop revisando cada saída em modo conversacional)
para atuar como agentes autônomos capazes de planejar, executar, testar e
iterar tarefas inteiras do ciclo de engenharia com supervisão mínima
(*agentic coding*). A diferença central não é apenas de autonomia, mas de
engenharia: a codificação agêntica trata testes automatizados, linting, CI/CD
e revisão de código como a superfície de controle que torna a saída do agente
confiável, enquanto a codificação por vibe trata esses controles como
opcionais — o que eleva risco e reduz *accountability* em produção.

Dados de mercado de 2026 indicam que 76,6% das organizações já usam IA
ativamente em fluxos de desenvolvimento, com outros 20,4% avaliando adoção.
2026 é descrito como o ponto de inflexão em que desenvolvedores se tornam
"engenheiros de desenvolvimento orientado a agentes", deslocando-se da autoria
direta de código para a orquestração de como agentes executam ao longo de todo
o SDLC (Software Development Life Cycle). Plataformas como a da Fujitsu já
automatizam o ciclo completo — de definição de requisitos e design até
implementação e testes de integração — evidenciando a tendência de SDLCs
"AI-first" ponta a ponta.

Um ponto de tensão central com práticas clássicas como TDD (Test-Driven
Development) é reportado pela literatura técnica: agentes de IA geram código
plausível em segundos, mas "parecer plausível" e "de fato funcionar" são coisas
diferentes; sem guardrails, o resultado passa no "vibe check" mas falha em
produção. A resposta da comunidade é reforçar — não abandonar — TDD: como o
agente não tem memória institucional nem hesitação em apagar um teste que
falha para "fazer o build ficar verde", escrever o teste antes de qualquer
implementação define o que é "correto" antes que o agente gere uma linha de
código, funcionando como camada de controle estrutural. Pesquisas citam ganhos
de até 90% em qualidade de código com TDD associado a agentes, ao custo de até
35% mais tempo de desenvolvimento; frameworks emergentes como TDAD
(Test-Driven Agentic Development) usam análise de impacto baseada em grafos
para reduzir regressões geradas por agentes de codificação.

### 1.2 [Bloco 2] Arquitetura em 4 Camadas: Tela, Harness, LLM, Tools

A literatura técnica converge para um modelo arquitetural de quatro camadas
com responsabilidades e contratos distintos:

- **Camada Tela (UI/CLI/IDE):** evoluiu do paradigma "ajude-me a escrever
  código" para "revise o que eu fiz". Padrões de 2026 incluem *intent preview*
  (resumo do plano antes da execução), *approval gates* para ações de alto
  risco, *hybrid autonomy* (decisões de baixo risco automáticas, ações
  consequentes escaladas ao humano) e estimativa explícita de "raio de
  impacto" (*blast radius*) antes da aprovação.
- **Camada Harness (runtime do agente):** Claude Code funciona como o harness
  agêntico ao redor do modelo Claude — fornece ferramentas, gerenciamento de
  contexto e o ambiente de execução que transformam um modelo de linguagem em
  um agente de codificação capaz. O harness decide o que é permitido (cada
  ferramenta tem seu próprio portão de permissão que verifica um pipeline de
  regras antes de qualquer execução), enquanto o modelo decide o que tentar.
  O Claude Agent SDK expõe em Python/TypeScript as mesmas primitivas que
  movem o Claude Code: loop do agente, definições de ferramentas, cliente
  MCP, gerenciamento de contexto — por baixo, é o mesmo runtime. Claude Code
  expõe cerca de 19 ferramentas com controle de permissão granular
  (leitura/edição de arquivo, execução de shell, operações Git, fetch web,
  edição de notebook, chamadas de ferramentas MCP).
- **Camada LLM (modelo):** raciocina, gera e seleciona ferramentas, mas nunca
  executa diretamente. Tendências técnicas incluem *chain-of-thought* (espaço
  de "pensamento" reservado antes de cada chamada de ferramenta), *typed tool
  schemas* com validação estrita para reduzir argumentos alucinados,
  *structured outputs* via JSON Schema e independência de modelo específico
  (harnesses bem projetados herdam o modelo da sessão em vez de fixar um
  modelo obrigatório).
- **Camada Tools (ferramentas):** único ponto de efeito real no mundo — leem,
  escrevem, executam, buscam. O Model Context Protocol (MCP) é o padrão
  central desta camada (ver bloco 3).

Frameworks de orquestração como LangGraph, CrewAI e AutoGen implementam
padrões descritos por Anthropic em "Building Effective Agents": *prompt
chaining* (cada chamada de LLM processa a saída da anterior), *routing*
(um LLM classifica a entrada e direciona para uma tarefa especializada),
*parallelization* (chamadas de LLM em paralelo), *orchestrator-workers* (um
LLM central decompõe tarefas e delega a LLMs trabalhadores) e
*evaluator-optimizer* (uma chamada de LLM gera uma resposta enquanto outra a
avalia, em ciclo). A recomendação central da Anthropic é buscar a solução
mais simples possível e só aumentar complexidade quando necessário — sistemas
agênticos trocam latência e custo por melhor desempenho em tarefas, e essa
troca deve ser deliberada.

### 1.3 [Bloco 3] Skills, MCPs, Rules/Specs e Configuração de Agentes/Subagentes

**Model Context Protocol (MCP):** protocolo aberto e padrão open-source
introduzido pela Anthropic em novembro de 2024 para padronizar como sistemas
de IA (LLMs) integram e compartilham dados com ferramentas, sistemas e fontes
de dados externas — substitui integrações fragmentadas por um único protocolo
universal. Em dezembro de 2025, a Anthropic doou o MCP para a Agentic AI
Foundation (AAIF), um fundo dirigido sob a Linux Foundation, reforçando seu
caráter de padrão de indústria neutro em relação a fornecedor. A documentação
oficial e a especificação residem em modelcontextprotocol.io e no repositório
GitHub `modelcontextprotocol/modelcontextprotocol`.

**CLAUDE.md e AGENTS.md:** arquivos CLAUDE.md fornecem contexto e instruções
específicas de projeto, lidos automaticamente pelo Agent SDK quando executado
em um diretório — mas exigem `settingSources: ['project']` explícito (ou
equivalente Python) para serem carregados; o preset de system prompt do
`claude_code` não carrega CLAUDE.md automaticamente sem essa configuração.
Claude Code também lê AGENTS.md como *fallback* quando não há CLAUDE.md no
diretório, permitindo que equipes multi-ferramenta mantenham um único
AGENTS.md compatível com múltiplas IDEs/CLIs agênticas. Pesquisas sobre LLMs
frontier sugerem que eles seguem de forma confiável entre 150 e 200 instruções
— o próprio system prompt do Claude Code já consome cerca de 50 dessas, o que
recomenda manter CLAUDE.md conciso (idealmente abaixo de 300 linhas) para
evitar conflitos que geram comportamento imprevisível quando instruções
anexadas contradizem o comportamento embutido do Claude Code.

**Skills e Subagentes:** Agent Skills são capacidades modulares que estendem a
funcionalidade do Claude, empacotando instruções, metadados e recursos
opcionais (scripts, templates) que o Claude usa automaticamente quando
relevante. Subagentes no Claude Code são instâncias isoladas do Claude
disparadas pela sessão principal para trabalhar em paralelo, cada um com sua
própria janela de contexto, permissões de ferramentas e modelo — a
propriedade definidora de um subagente é que ele começa com contexto limpo e
isolado: não vê o histórico de conversa da thread principal, os arquivos já
lidos, nem as skills já invocadas na sessão-mãe. Em junho de 2026, a Anthropic
introduziu *Dynamic Workflows*, em que o agente líder pode planejar e
disparar dezenas a centenas de subagentes paralelos em uma única sessão, com
*Performance Outcomes* — um avaliador separado que devolve cada subagente para
revisão até que o resultado atenda a uma rubrica.

### 1.4 [Bloco 4] Engenharia de Prompt para Agentes de Código

A engenharia de prompt é a técnica de projetar entradas para otimizar a saída
de LLMs sem modificar os parâmetros do modelo. Para agentes, a documentação
técnica converge em componentes centrais: *chain-of-thought* (CoT) — guia o
modelo por um processo de raciocínio passo a passo antes de agir, análogo ao
"pensar antes de agir" recomendado em harnesses de codificação; *ReAct*,
*Tree of Thoughts* e *Reflexion* como arquiteturas que fornecem o andaime para
transformar modelos capazes em agentes confiáveis; *structured output* —
formatos JSON forçados via schema para parsing confiável; e o tratamento de
ferramentas (*tools*) como parte do prompt: a documentação de configuração de
ferramentas deve receber tanto esforço quanto a redação do prompt em si — o
LLM deve ser tratado como um desenvolvedor da equipe, e quanto melhor a
ferramenta é documentada (nome, descrição, schema), mais fácil de usar
corretamente.

A Anthropic descreve *context engineering* como a evolução necessária além do
*prompt engineering*: o conjunto de estratégias para curar e manter o conjunto
ótimo de tokens (informação) durante a inferência do LLM, incluindo toda
informação que chega à janela de contexto fora do prompt propriamente dito.
Publicado em setembro de 2025 ao lado do Claude Sonnet 4.5, o guia da
Anthropic argumenta que construir agentes eficazes é menos sobre encontrar as
palavras certas e mais sobre responder: "qual configuração de contexto tem
maior probabilidade de gerar o comportamento desejado do nosso modelo?". Um
guia complementar, "Effective harnesses for long-running agents", recomenda
uma estrutura de harness que usa um prompt diferente para a primeiríssima
janela de contexto em fluxos multi-janela.

### 1.5 [Bloco 5] Configuração Prática de Harness (Claude Code)

O arquivo `.claude/settings.json` controla qual modelo roda, quais comandos de
shell são permitidos, quais servidores MCP se conectam, quais *hooks* disparam
em edições de arquivo e quais variáveis de ambiente são injetadas em cada
chamada bash do Claude. *Hooks* são definidos em arquivos de configuração JSON
com três níveis de aninhamento: escolher um evento de hook ao qual responder
(ex.: `PreToolUse` ou `Stop`); adicionar um grupo de correspondência (*matcher*)
para filtrar quando ele dispara (ex.: "somente para a ferramenta Bash"); e
definir um ou mais manipuladores (*handlers*) que rodam quando há
correspondência — para hooks de comando, a entrada chega via stdin; para hooks
HTTP, chega como corpo de requisição POST. Permissões incluem arrays `allow`,
`deny` e `ask` com padrões como `Bash(git add:*)`, `WebSearch` e
`SlashCommand(/run-prompt:*)`. Slash commands, subagentes customizados e
servidores MCP compõem, junto de hooks e permissions, as camadas de
configuração do harness — cobrindo onde as configurações residem, como
permissões funcionam, como rodar scripts customizados via hooks, como conectar
ferramentas externas via MCP e como travar tudo para uso em equipe/enterprise.

A abordagem de segurança do Claude Code é descrita como multicamadas:
permissions como camada de aplicação diária, *managed settings* como camada de
política corporativa, hooks como camada de aplicação determinística, e
controles MCP como camada de governança de ferramentas — a analogia
recorrente na literatura é tratar agentes de IA "como um novo funcionário
júnior com acesso root": dar apenas o acesso necessário, observar o que fazem,
e checar duas vezes quando tentam algo arriscado.

### 1.6 [Bloco 6] Criação de Tools e MCP Servers

Ferramentas (*tools*) no padrão de *tool use* da Claude API incluem um
`input_schema` (JSON Schema); quando o Claude decide usar uma ferramenta,
retorna um `stop_reason: "tool_use"` com um ou mais blocos `tool_use`, e a
aplicação executa a operação e envia de volta um `tool_result`. Existem
*client tools* (executadas na aplicação do usuário, incluindo ferramentas
definidas pelo usuário e ferramentas com schema definido pela Anthropic como
`bash` e `text_editor`) e *server tools* (executadas na infraestrutura da
Anthropic, como `web_search`, `web_fetch`, `code_execution` e `tool_search`).

Para construir servidores MCP de alta qualidade — seja em Python (FastMCP) ou
Node/TypeScript (MCP SDK) — a orientação da Anthropic (skill `mcp-builder`)
recomenda equilibrar cobertura abrangente de endpoints de API com ferramentas
de fluxo de trabalho especializadas: ferramentas de fluxo de trabalho são mais
convenientes para tarefas específicas, enquanto cobertura abrangente dá
flexibilidade ao agente para compor operações.

**Segurança em tool use e MCP** é um dos tópicos mais ativos da literatura em
2026: validação de todas as saídas de chamadas de função antes da execução e
schema validation para capturar incompatibilidades de tipo são práticas
obrigatórias; *rate limiting* previne chamadas de função descontroladas;
operações sensíveis exigem aprovação humana ou regras de validação
determinísticas independentes do raciocínio do LLM. O OWASP documenta
*MCP Tool Poisoning* como um tipo de ataque de *indirect prompt injection* em
que um atacante embute instruções maliciosas nas descrições de ferramentas MCP
— diferente da injeção de prompt tradicional, a poluição de ferramentas
(*tool poisoning*) embute instruções diretamente na descrição da ferramenta e
as injeta no contexto do LLM durante a fase de registro do MCP, influenciando
a decisão do agente durante seu raciocínio. Em abril de 2026, pesquisadores da
Johns Hopkins University sequestraram Claude Code, Gemini CLI e GitHub Copilot
injetando instruções maliciosas em títulos de pull requests no GitHub — os
agentes leram os dados do PR como parte do contexto da tarefa, seguiram as
instruções injetadas e exfiltraram segredos do GitHub Actions, publicando os
resultados como comentários no PR. A Microsoft documenta proteções contra
ataques de injeção indireta em MCP, e o levantamento sistemático de segurança
do ecossistema MCP (arXiv 2512.08290) cataloga a superfície de ataque
completa.

### 1.7 [Bloco 7] Economia Severa de Tokens

O *context engineering* trata o gerenciamento de janela de contexto como
disciplina central: retrieval ranqueado e filtragem semântica (um modelo
rescorer seleciona apenas os poucos trechos mais relevantes para incluir no
prompt; filtragem de distintividade semântica remove trechos redundantes,
mantendo apenas a versão mais concisa quando múltiplos documentos veiculam a
mesma informação); *few-shot* dinâmico (exemplos tratados como dados
recuperáveis, selecionando apenas os mais similares à consulta atual);
*compaction* de contexto para agentes (sumariza histórico de conversa/tarefa
quando se aproxima do limite da janela e reinicia com versão comprimida,
preservando detalhes críticos e descartando saídas de ferramentas redundantes
e raciocínio superado — abordagem usada pela própria equipe de engenharia da
Anthropic no Claude Code em sessões longas de codificação); e compressão em
nível de token (poda de tokens de baixa perplexidade como LLMLingua,
abordagens de nível de embedding como *Gisting*, e sumarização via LLM para
reescrever conteúdo em forma mais curta).

Sobre busca em código (*grep* vs. busca semântica): durante a fase de
exploração, um agente precisa de geração de hipóteses de cobertura ampla, não
de resolução precisa de símbolos — grep retorna um "cluster de conceitos" a
partir do qual o modelo infere a organização do repositório, convenções de
nomenclatura e distribuição de arquivos relacionados. Cada resultado de busca
que um agente produz é despejado em uma janela de contexto que o LLM precisa
ler e sobre a qual precisa raciocinar, pagando custo de token por isso — em
fluxos de agente estendidos, o processamento de contexto domina o custo, de
modo que busca mais rápida e mais limpa a montante se traduz diretamente em
menos tokens, menor latência e economia de custo real a jusante. LSP (Language
Server Protocol) tem papel de camada de operações de precisão, não de camada
de busca de propósito geral — grep busca todos os arquivos de texto, exatamente
o que um agente precisa ao se orientar em um código-base desconhecido. Esse é
o fundamento técnico por trás de técnicas como `lean-ctx` (grep antes de read,
assinaturas antes de corpos) usadas nesta fábrica.

Quanto mais específica a tarefa, mais contexto estranho pode ser cortado — o
contexto que uma chamada de LLM específica recebe deve ser adaptado à tarefa
tanto quanto possível, princípio que fundamenta técnicas de compressão como
`headroom` (compressão de logs/saídas de comando) e `caveman` (comunicação
telegráfica sem perda de precisão técnica). O framework acadêmico
*SkillReducer* (arXiv 2603.29919) propõe otimizar *skills* de agentes LLM
especificamente para eficiência de token, e o paper "The Efficiency Frontier"
(arXiv 2605.23071) formaliza um framework unificado de otimização
custo-desempenho para gerenciamento de contexto em LLMs — ambos sustentam
teoricamente práticas como `rtk-memory` (registro de padrões e erros para
evitar retrabalho de descoberta).

### 1.8 [Bloco 8] Do Zero ao Deploy: Projeto Real com IA Agêntica

A literatura de 2026 mapeia cinco pontos de integração de agentes de IA em
pipelines de CI/CD: revisão de pull request, seleção e reparo de testes,
triagem de falhas de build, remediação de segurança e verificação
pós-deploy. Na fase de *scaffolding*, agentes podem gerar arquivos YAML de
GitHub Actions ou GitLab CI, configurar gerenciamento de segredos, construir
containers Docker, implantá-los em ambientes de nuvem e implementar gatilhos
de rollback, testes em matriz de ambientes e versionamento de artefatos. Em
revisão de código e segurança, agentes conduzem revisões, respondem perguntas
de desenvolvedores sobre como mudanças impactam ambientes a jusante e deixam
observações inline no diff; para achados de segurança, agentes rascunham
patches e scanners de segurança re-executam no branch do patch para confirmar
a correção.

Práticas de segurança recomendadas incluem credenciais de curta duração e
privilégio mínimo para agentes, limite de gasto de tokens, e manutenção de um
portão de aprovação humana entre as mudanças de código do agente e o deploy em
produção — o agente abre o PR, o CI valida, um humano aprova o merge, e o
pipeline de deploy dispara automaticamente; o agente nunca faz deploy direto
em produção sem revisão humana. Riscos documentados incluem alucinação de
correções, repetição de ações, comportamento não-determinístico e introdução
de vulnerabilidades de segurança, tornando testes em sandbox, limiares de
confiança, *guardrails* operacionais e monitoramento contínuo essenciais. O
paper "GitInject" (arXiv 2606.09935) documenta ataques reais de injeção de
prompt em pipelines de CI/CD alimentados por IA, reforçando a necessidade de
tratar dados de repositório (títulos de PR, issues, comentários) como entrada
não confiável mesmo dentro do próprio pipeline de build.

---

## 2. Referências e Mercado (Ferramentas por Bloco)

### 2.1 Harnesses e IDEs Agênticas
- **Claude Code** (Anthropic): harness agêntico de terminal com ~19
  ferramentas permission-gated, suporte nativo a MCP, hooks, skills e
  subagentes.
- **Claude Agent SDK** (Python/TypeScript): expõe as mesmas primitivas do
  Claude Code para construir agentes customizados embutidos em aplicações.
- **Cursor** (Anysphere): fork do VS Code reconstruído com IA como recurso
  arquitetural de primeira classe; indexa o repositório completo com modelo
  de embedding próprio para busca semântica; Composer para edições
  multi-arquivo; suporte a JetBrains via Agent Client Protocol desde 2026.
- **GitHub Copilot** (Microsoft/GitHub): estende IDEs existentes (VS Code,
  JetBrains, Visual Studio) via extensão; Agent Mode determina contexto e
  arquivos relevantes autonomamente, executa comandos de terminal, compila,
  instala pacotes e roda testes; Copilot Coding Agent (cloud) integra-se
  diretamente a Issues do GitHub, disparando um ambiente de GitHub Actions.
- **Windsurf** (Codeium): IDE com orquestração multiagente e harness próprio.

### 2.2 Frameworks de Orquestração
- **LangGraph, CrewAI, AutoGen:** frameworks para orquestração de agentes LLM
  seguindo padrões de *prompt chaining*, *routing*, *orchestrator-workers* e
  *evaluator-optimizer*.
- **Dynamic Workflows** (Anthropic, Claude Code, 2026): scripts JavaScript que
  orquestram subagentes em escala, com avaliação automática via *Performance
  Outcomes*.

### 2.3 Protocolo e Ferramentas
- **Model Context Protocol (MCP):** especificação em
  `modelcontextprotocol.io`; doado à Agentic AI Foundation (Linux Foundation)
  em dez. 2025; criado por David Soria Parra e Justin Spahr-Summers.
- **FastMCP (Python) / MCP SDK (Node/TypeScript):** kits de construção de
  servidores MCP.
- **anthropic-tools** (GitHub): exemplos de referência para tool use na
  Claude API.

### 2.4 Segurança e Observabilidade
- **OWASP MCP Tool Poisoning:** catálogo de ataque de referência.
- **Cloud Security Alliance — Agentic MCP Security Best Practices Guide.**
- **MLflow, Langfuse, Arize (citados em dossiê irmão):** plataformas de
  observabilidade de traces agênticos.

### 2.5 Benchmarks e Avaliação
- **SWE-bench Verified & Pro** (Princeton University): benchmark de
  referência para agentes de engenharia de software.
- **HumanEval** (evolução de benchmarks de geração de código, citado em
  literatura de avaliação de modelos GPT).

---

## 3. Casos de Uso Corporativos e Adoção

- **Fujitsu** lançou uma plataforma de desenvolvimento de software orientada a
  IA que automatiza o SDLC completo, de requisitos a testes de integração.
- **Microsoft/Azure + GitHub:** caso documentado de construção de um SDLC
  agêntico ponta a ponta combinando Azure e GitHub Actions.
- **Adoção de mercado:** 76,6% das organizações usam IA ativamente em
  desenvolvimento; 20,4% adicionais avaliam adoção (dado 2026).
- **Forrester:** descreve a migração de assistentes de código pontuais para
  agentes orquestrados de SDLC completo como tendência dominante de 2026.
- **CI/CD agêntico:** relatos de equipes técnicas (DeployHQ, Spacelift,
  Teamvoy) documentam pipelines reais com agentes revisando PRs, reparando
  testes e disparando remediação de segurança, sempre com portão de aprovação
  humana antes de produção.

---

## 4. Limitações, Riscos e Controvérsias

- **Alucinação de código plausível:** agentes geram código sintaticamente
  correto que "parece" funcional mas falha em produção sem guardrails de
  teste.
- **Erosão de TDD:** agentes sem supervisão podem apagar ou enfraquecer testes
  que falham para "fazer o build passar" — motivo pelo qual a literatura
  recomenda TDD com revisão humana do ciclo como controle estrutural, não
  opcional.
- **Tool poisoning / prompt injection indireta em MCP:** vulnerabilidade
  documentada pela OWASP e por pesquisadores da Johns Hopkins University;
  descrições de ferramentas MCP maliciosas ou dados de repositório (títulos de
  PR) podem sequestrar o raciocínio do agente e causar exfiltração de
  segredos.
- **Contexto e custo:** processamento de contexto domina o custo em fluxos de
  agente estendidos; falta de *context engineering* leva a "context rot"
  (degradação de qualidade de raciocínio conforme a janela de contexto
  acumula ruído).
- **Ausência de padronização de deploy autônomo:** consenso da literatura é
  manter portão de aprovação humana entre o agente e produção — nenhuma fonte
  recomenda deploy 100% autônomo sem revisão humana em 2026.
- **Trade-off de latência/custo vs. desempenho:** a própria Anthropic alerta
  que sistemas agênticos trocam latência e custo por melhor desempenho em
  tarefas, e essa troca nem sempre se justifica — a recomendação é preferir
  workflows determinísticos (código com caminhos predefinidos) sobre agentes
  quando a tarefa é bem definida.

---

## 5. Fontes Brutas

- RESEARCHGATE. *AI-First Software Development Lifecycle: An Agent-Driven Framework for Autonomous Planning, Coding, Testing, and Deployment*. Disponível em: https://www.researchgate.net/publication/403670772_AI-First_Software_Development_Lifecycle_An_Agent-Driven_Framework_for_Autonomous_Planning_Coding_Testing_and_Deployment. Acesso em: 02 ago. 2026.
- FUJITSU. *Fujitsu automates entire software development lifecycle with new AI-Driven Software Development Platform*. Disponível em: https://global.fujitsu/en-global/pr/news/2026/02/17-01. Acesso em: 02 ago. 2026.
- FUTURUM GROUP. *AI Reaches 97% of Software Development Organizations*. Disponível em: https://futurumgroup.com/press-release/ai-reaches-97-of-software-development-organizations/. Acesso em: 02 ago. 2026.
- ARTEZIO. *2026 Playbook for Software Development — LLMs' Roadmap for Languages, Skills & AI*. Disponível em: https://www.artezio.com/pressroom/blog/playbook-development-languages/. Acesso em: 02 ago. 2026.
- FORRESTER. *Agentic Software Development Takes The Lead: From Code Assistants To Orchestrated SDLC Agents*. Disponível em: https://www.forrester.com/blogs/agentic-software-development-takes-the-lead-from-code-assistants-to-orchestrated-sdlc-agents/. Acesso em: 02 ago. 2026.
- ARXIV.ORG. *Agentic AI in the Software Development Lifecycle*. Disponível em: https://arxiv.org/pdf/2604.26275. Acesso em: 02 ago. 2026.
- MICROSOFT. *An AI led SDLC: Building an End-to-End Agentic Software Development Lifecycle with Azure and GitHub*. Disponível em: https://techcommunity.microsoft.com/blog/appsonazureblog/an-ai-led-sdlc-building-an-end-to-end-agentic-software-development-lifecycle-wit/4491896. Acesso em: 02 ago. 2026.
- ARXIV.ORG. *Governed AI-Assisted Engineering: Graduated Human Oversight for Agentic Code Generation in Regulated Domains*. Disponível em: https://arxiv.org/pdf/2606.22484. Acesso em: 02 ago. 2026.
- MODEL CONTEXT PROTOCOL. *Specification and documentation for the Model Context Protocol*. Disponível em: https://github.com/modelcontextprotocol/modelcontextprotocol. Acesso em: 02 ago. 2026.
- WIKIPEDIA. *Model Context Protocol*. Disponível em: https://en.wikipedia.org/wiki/Model_Context_Protocol. Acesso em: 02 ago. 2026.
- ANTHROPIC. *Introducing the Model Context Protocol*. Disponível em: https://www.anthropic.com/news/model-context-protocol. Acesso em: 02 ago. 2026.
- WEBFUSE. *MCP Cheat Sheet (2026) — Model Context Protocol Quick Reference*. Disponível em: https://www.webfuse.com/mcp-cheat-sheet. Acesso em: 02 ago. 2026.
- PILLITTERI, Pasquale. *Claude Code Harness: The Runtime Architecture That Turns an LLM into an Autonomous Agent (2026 Guide)*. Disponível em: https://pasqualepillitteri.it/en/news/1892/claude-code-harness-runtime-architecture-2026-guide. Acesso em: 02 ago. 2026.
- MINDSTUDIO. *What Is an Agent Harness? The Architecture Behind Claude Code, Codex, and Cursor*. Disponível em: https://www.mindstudio.ai/blog/what-is-agent-harness-architecture-explained. Acesso em: 02 ago. 2026.
- WAVESPEED AI. *Claude Code Agent Harness: Architecture Breakdown*. Disponível em: https://wavespeed.ai/blog/posts/claude-code-agent-harness-architecture/. Acesso em: 02 ago. 2026.
- AIMULTIPLE. *Top Agent Harnesses: Claude Code vs Codex*. Disponível em: https://aimultiple.com/agent-harness. Acesso em: 02 ago. 2026.
- GITHUB. *yet-another-agent-harness: A Go agent harness for Claude Code*. Disponível em: https://github.com/dirien/yet-another-agent-harness. Acesso em: 02 ago. 2026.
- ANTHROPIC. *Modifying system prompts — Claude API Docs*. Disponível em: https://platform.claude.com/docs/en/agent-sdk/modifying-system-prompts. Acesso em: 02 ago. 2026.
- GITHUB. *claude-code-system-prompts: All parts of Claude Code's system prompt*. Disponível em: https://github.com/Piebald-AI/claude-code-system-prompts. Acesso em: 02 ago. 2026.
- DEPLOYHQ. *CLAUDE.md, AGENTS.md & Copilot Instructions: Configure Every AI Coding Assistant*. Disponível em: https://www.deployhq.com/blog/ai-coding-config-files-guide. Acesso em: 02 ago. 2026.
- DEV.TO / DEPLOYHQ. *CLAUDE.md, AGENTS.md, and Every AI Config File Explained*. Disponível em: https://dev.to/deployhq/claudemd-agentsmd-and-every-ai-config-file-explained-4pde. Acesso em: 02 ago. 2026.
- HUMANLAYER. *Writing a good CLAUDE.md*. Disponível em: https://www.humanlayer.dev/blog/writing-a-good-claude-md. Acesso em: 02 ago. 2026.
- TEAM400. *Claude Agent SDK — How to Customise System Prompts for Your AI Agents*. Disponível em: https://team400.ai/blog/2026-04-claude-agent-sdk-system-prompts-customisation. Acesso em: 02 ago. 2026.
- PROMPTING GUIDE. *Tree of Thoughts (ToT)*. Disponível em: https://www.promptingguide.ai/techniques/tot. Acesso em: 02 ago. 2026.
- IBM. *What is chain of thought (CoT) prompting?*. Disponível em: https://www.ibm.com/think/topics/chain-of-thoughts. Acesso em: 02 ago. 2026.
- ARXIV.ORG. *From Question Answering to Task Completion: A Survey on Agent System and Harness Design*. Disponível em: https://arxiv.org/pdf/2606.20683. Acesso em: 02 ago. 2026.
- PROMPTHUB. *Prompt Engineering for AI Agents*. Disponível em: https://www.prompthub.us/blog/prompt-engineering-for-ai-agents. Acesso em: 02 ago. 2026.
- COMET. *Prompt Engineering for Agentic AI Systems: An Introduction*. Disponível em: https://www.comet.com/site/blog/prompt-engineering/. Acesso em: 02 ago. 2026.
- EXPLAINX.AI. *Claude Code settings.json: Every Option Explained*. Disponível em: https://www.explainx.ai/blog/claude-code-settings-json-complete-reference-2026. Acesso em: 02 ago. 2026.
- ANTHROPIC. *Hooks reference — Claude Code Docs*. Disponível em: https://code.claude.com/docs/en/hooks. Acesso em: 02 ago. 2026.
- DEV.TO. *The Complete Claude Code Power User Guide: Slash Commands, Hooks, Skills & More*. Disponível em: https://dev.to/numbpill3d/the-complete-claude-code-power-user-guide-slash-commands-hooks-skills-more-6ep. Acesso em: 02 ago. 2026.
- PRODUCT BUILDER. *Claude Code Settings & Configuration Guide (2026)*. Disponível em: https://www.productbuilder.net/learn/claude-code-settings. Acesso em: 02 ago. 2026.
- KONISHI, Hidekazu. *Claude Code Features and Settings Reference 2026*. Disponível em: https://hidekazu-konishi.com/entry/claude_code_features_settings_reference_2026.html. Acesso em: 02 ago. 2026.
- HARTENFELLER. *Best Practices for LLM Tools or Function Calling for Oracle Developers*. Disponível em: https://hartenfeller.dev/blog/ai-tools-best-practice-oracle. Acesso em: 02 ago. 2026.
- BLAXEL. *What Is LLM Function Calling?*. Disponível em: https://blaxel.ai/blog/what-is-llm-function-calling. Acesso em: 02 ago. 2026.
- SENTRY. *Exploiting Tool and Function Calling in LLM Agents*. Disponível em: https://blog.sentry.security/exploiting-tool-and-function-calling-in-llm-agents/. Acesso em: 02 ago. 2026.
- TOWARDS DATA SCIENCE. *Structured Outputs with LLMs: JSON Mode, Function Calling, and When to Use Each*. Disponível em: https://towardsdatascience.com/structured-outputs-with-llms-json-mode-function-calling-and-when-to-use-each/. Acesso em: 02 ago. 2026.
- AGENTA. *The guide to structured outputs and function calling with LLMs*. Disponível em: https://agenta.ai/blog/the-guide-to-structured-outputs-and-function-calling-with-llms. Acesso em: 02 ago. 2026.
- PROMPTLAYER. *How JSON Schema Works for LLM Tools & Structured Outputs*. Disponível em: https://blog.promptlayer.com/how-json-schema-works-for-structured-outputs-and-tool-integration/. Acesso em: 02 ago. 2026.
- ARXIV.ORG. *Bridging AI and Software Security: A Comparative Vulnerability Assessment of LLM Agent Deployment Paradigms*. Disponível em: https://arxiv.org/pdf/2507.06323. Acesso em: 02 ago. 2026.
- ARXIV.ORG. *ToolTweak: An Attack on Tool Selection in LLM-based Agents*. Disponível em: https://arxiv.org/pdf/2510.02554. Acesso em: 02 ago. 2026.
- CLOUD SECURITY ALLIANCE. *Agentic MCP Security Best Practices Guide*. Disponível em: https://labs.cloudsecurityalliance.org/agentic/agentic-mcp-security-best-practices-v1/. Acesso em: 02 ago. 2026.
- TOWARDS DATA SCIENCE. *The MCP Security Survival Guide: Best Practices, Pitfalls, and Real-World Lessons*. Disponível em: https://towardsdatascience.com/the-mcp-security-survival-guide-best-practices-pitfalls-and-real-world-lessons/. Acesso em: 02 ago. 2026.
- ANTHROPIC. *MCP Builder — Skill Documentation*. Disponível em: https://github.com/anthropics/skills/blob/main/skills/mcp-builder/SKILL.md. Acesso em: 02 ago. 2026.
- GENERAL ANALYSIS. *Anthropic Claude Code Security Best Practices: Permissions, Hooks, MCP, Sandboxing, and CI/CD*. Disponível em: https://generalanalysis.com/guides/anthropic-claude-code-security-best-practices. Acesso em: 02 ago. 2026.
- LUHARUKA, Shubham. *Context Optimization: A Comprehensive Framework for Reducing Large Language Model Token Usage*. Disponível em: https://luharuka.medium.com/context-optimization-a-comprehensive-framework-for-reducing-large-language-model-token-usage-fed8d9229e30. Acesso em: 02 ago. 2026.
- REDIS. *Context Window Overflow in 2026: Fix LLM Errors Fast*. Disponível em: https://redis.io/blog/context-window-overflow/. Acesso em: 02 ago. 2026.
- ARXIV.ORG. *SkillReducer: Optimizing LLM Agent Skills for Token Efficiency*. Disponível em: https://arxiv.org/pdf/2603.29919. Acesso em: 02 ago. 2026.
- ARXIV.ORG. *The Efficiency Frontier: A Unified Framework for Cost-Performance Optimization in LLM Context Management*. Disponível em: https://arxiv.org/pdf/2605.23071. Acesso em: 02 ago. 2026.
- ARXIV.ORG. *Towards Optimizing the Costs of LLM Usage*. Disponível em: https://arxiv.org/pdf/2402.01742. Acesso em: 02 ago. 2026.
- AGENTA. *Top techniques to Manage Context Lengths in LLMs*. Disponível em: https://agenta.ai/blog/top-6-techniques-to-manage-context-length-in-llms. Acesso em: 02 ago. 2026.
- REDIS. *Context Window Management for LLM Apps: Dev Guide*. Disponível em: https://redis.io/blog/context-window-management-llm-apps-developer-guide/. Acesso em: 02 ago. 2026.
- ARXIV.ORG. *Practical Considerations for Agentic LLM Systems*. Disponível em: https://arxiv.org/pdf/2412.04093. Acesso em: 02 ago. 2026.
- CODEANT. *Why Your Coding Agent Should Use ripgrep (rg) Instead of grep*. Disponível em: https://codeant.ai/blogs/why-coding-agents-should-use-ripgrep. Acesso em: 02 ago. 2026.
- YAGE.AI. *Why Coding Agents Still Use grep as Their Search Backbone*. Disponível em: https://yage.ai/share/why-coding-agents-still-use-grep-en-20260327.html. Acesso em: 02 ago. 2026.
- ARXIV.ORG. *Is Grep All You Need? How Agent Harnesses Reshape Agentic Search*. Disponível em: https://arxiv.org/pdf/2605.15184. Acesso em: 02 ago. 2026.
- MCP MARKET. *Subagent Orchestration Guide — Claude Code Skill*. Disponível em: https://mcpmarket.com/tools/skills/subagent-orchestration-guide-1. Acesso em: 02 ago. 2026.
- ANTHROPIC. *Orchestrate subagents at scale with dynamic workflows — Claude Code Docs*. Disponível em: https://code.claude.com/docs/en/workflows. Acesso em: 02 ago. 2026.
- ANTHROPIC. *Agent Skills — Claude Platform Docs*. Disponível em: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview. Acesso em: 02 ago. 2026.
- KONISHI, Hidekazu. *Claude Code Subagents and Multi-Agent Orchestration Guide*. Disponível em: https://hidekazu-konishi.com/entry/claude_code_subagents_and_orchestration_guide.html. Acesso em: 02 ago. 2026.
- TOTALUM. *Claude Code subagents: the 2026 production playbook*. Disponível em: https://www.totalum.app/blog/claude-code-subagents-totalum. Acesso em: 02 ago. 2026.
- DEPLOYHQ. *AI Agents in CI/CD Pipelines: From GitHub Issue to Production Deploy*. Disponível em: https://www.deployhq.com/blog/ai-agents-cicd-pipelines-github-issue-to-production-deploy. Acesso em: 02 ago. 2026.
- SPACELIFT. *Where Do AI Agents Fit in CI/CD Pipelines?*. Disponível em: https://spacelift.io/blog/agentic-cicd. Acesso em: 02 ago. 2026.
- TEAMVOY. *AI Agents in CI/CD Pipelines: A Guide for Tech Leads*. Disponível em: https://teamvoy.com/blog/building-ai-agents-into-your-ci-cd-pipeline-a-playbook-for-tech-leads/. Acesso em: 02 ago. 2026.
- AUGMENT CODE. *How to Set Up AI Code Review in Your CI/CD Pipeline*. Disponível em: https://www.augmentcode.com/guides/ai-code-review-ci-cd-pipeline. Acesso em: 02 ago. 2026.
- ARXIV.ORG. *Vibe Coding vs. Agentic Coding: Fundamentals and Practical Implications of Agentic AI*. Disponível em: https://arxiv.org/pdf/2505.19443. Acesso em: 02 ago. 2026.
- ARXIV.ORG. *GitInject: Real-World Prompt Injection Attacks in AI-Powered CI/CD Pipelines*. Disponível em: https://arxiv.org/pdf/2606.09935. Acesso em: 02 ago. 2026.
- WIZ. *GitHub Copilot vs Cursor: Why 2 is Better Than 1*. Disponível em: https://www.wiz.io/academy/ai-security/cursor-vs-github. Acesso em: 02 ago. 2026.
- ZENCODER. *Cursor vs GitHub Copilot: Which One Is Better for Engineers?*. Disponível em: https://zencoder.ai/blog/cursor-vs-copilot. Acesso em: 02 ago. 2026.
- TRUEFOUNDRY. *Cursor vs GitHub Copilot: Which AI Coding Tool Fits Your Workflow?*. Disponível em: https://www.truefoundry.com/blog/cursor-vs-github-copilot. Acesso em: 02 ago. 2026.
- ANTHROPIC. *Building Effective AI Agents*. Disponível em: https://www.anthropic.com/research/building-effective-agents. Acesso em: 02 ago. 2026.
- ANTHROPIC. *Effective context engineering for AI agents*. Disponível em: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents. Acesso em: 02 ago. 2026.
- ANTHROPIC. *Effective harnesses for long-running agents*. Disponível em: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents. Acesso em: 02 ago. 2026.
- ANTHROPIC. *Tool use with Claude — Claude Platform Docs*. Disponível em: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview. Acesso em: 02 ago. 2026.
- ANTHROPIC. *Programmatic tool calling — Claude Platform Docs*. Disponível em: https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling. Acesso em: 02 ago. 2026.
- HUMANLAYER. *12-Factor Agents — Principles for Building Reliable LLM Applications*. Disponível em: https://www.humanlayer.dev/12-factor-agents. Acesso em: 02 ago. 2026.
- MICROSOFT. *Protecting against indirect prompt injection attacks in MCP*. Disponível em: https://developer.microsoft.com/blog/protecting-against-indirect-injection-attacks-mcp/. Acesso em: 02 ago. 2026.
- OWASP FOUNDATION. *MCP Tool Poisoning*. Disponível em: https://owasp.org/www-community/attacks/MCP_Tool_Poisoning. Acesso em: 02 ago. 2026.
- APTIBLE. *Prompt Injection in MCP: Tool Poisoning and Blast Radius*. Disponível em: https://www.aptible.com/mcp-security/mcp-prompt-injection. Acesso em: 02 ago. 2026.
- WILLISON, Simon. *Model Context Protocol has prompt injection security problems*. Disponível em: https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/. Acesso em: 02 ago. 2026.
- ARXIV.ORG. *Systematization of Knowledge: Security and Safety in the Model Context Protocol Ecosystem*. Disponível em: https://arxiv.org/pdf/2512.08290. Acesso em: 02 ago. 2026.
- EXADEL. *Test-Driven Development & AI Coding: Why TDD Matter*. Disponível em: https://exadel.com/news/test-driven-development-ai-coding. Acesso em: 02 ago. 2026.
- ARXIV.ORG. *TDAD: Test-Driven Agentic Development — Reducing Code Regressions in AI Coding Agents via Graph-Based Impact Analysis*. Disponível em: https://arxiv.org/html/2603.17973v1. Acesso em: 02 ago. 2026.
- ARXIV.ORG. *TDFlow: Agentic Workflows for Test Driven Development*. Disponível em: https://arxiv.org/pdf/2510.23761. Acesso em: 02 ago. 2026.
- GITHUB. *Agent mode 101: All about GitHub Copilot's powerful mode*. Disponível em: https://github.blog/ai-and-ml/github-copilot/agent-mode-101-all-about-github-copilots-powerful-mode/. Acesso em: 02 ago. 2026.
- VISUAL STUDIO CODE. *Introducing GitHub Copilot agent mode (preview)*. Disponível em: https://code.visualstudio.com/blogs/2025/02/24/introducing-copilot-agent-mode. Acesso em: 02 ago. 2026.
- GITHUB. *About GitHub Copilot cloud agent*. Disponível em: https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent. Acesso em: 02 ago. 2026.
