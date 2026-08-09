# Dossiê de Pesquisa — Do Zero ao Código Assistido

Tema: guia prático de Inteligência Artificial para iniciantes absolutos, da história da tecnologia ao uso de harnesses gratuitos e modelos de custo zero para construir projetos reais. Motivo condutor da obra: o desencantamento produtivo — o iniciante chega vendo a IA como caixa-preta mágica no navegador e termina operando um sistema de 4 camadas (Tela, Harness, LLM, Tools) que ele mesmo configurou sem pagar nada. Persona: o Aprendiz de Construtor, que quer entender e fazer, não apenas consumir.

---

## 1. Módulo 1 — História e evolução da IA (capítulos 1 a 3)

### 1.1 As origens: lógica simbólica e os primeiros modelos estatísticos

O campo da IA nasce formalmente em 1956, na conferência de Dartmouth, quando John McCarthy, Marvin Minsky, Nathaniel Rochester e Claude Shannon propuseram um verão de pesquisa sobre "como fazer máquinas usar linguagem, formar abstrações e melhorar a si mesmas" [1]. Mas as raízes são anteriores: em 1943, Warren McCulloch e Walter Pitts demonstraram que redes de neurônios artificiais simples poderiam, em tese, computar qualquer função lógica [2]; em 1950, Alan Turing publicou "Computing Machinery and Intelligence", propondo o teste que leva seu nome e a pergunta "as máquinas podem pensar?" [3]. Em 1956, o Logic Theorist de Newell e Simon provou teoremas de lógica [4]. Em 1958, Frank Rosenblatt criou o Perceptron, um classificador de padrões com pesos ajustáveis [5]. Em 1959, Arthur Samuel cunhou o termo "machine learning" ao ensinar um programa de damas a melhorar com a prática [6].

O entusiasmo inicial colidiu com os limites da abordagem simbólica: em 1969, Minsky e Papert mostraram matematicamente que o Perceptron simples não conseguia resolver problemas não lineares, como o XOR [7]. Seguiram-se os chamados invernos da IA, períodos de cortes de financiamento. A resposta prática veio em duas frentes. Na frente simbólica, os sistemas especialistas (expert systems) codificavam o conhecimento de especialistas humanos em regras se-então: o DENDRAL (química) e o MYCIN (diagnóstico médico) dos anos 1970 demonstraram valor comercial real [8]. Na frente estatística, a década de 1980 consolidou o aprendizado de máquina clássico: árvores de decisão, regressão logística, máquinas de vetores de suporte e, com a retomada da retropropagação (backpropagation) por Rumelhart, Hinton e Williams em 1986, as redes neurais multicamadas voltaram ao centro do palco [9]. A distinção central que o iniciante precisa reter: sistemas baseados em regras são programados explicitamente por humanos; sistemas de aprendizado estatístico aprendem padrões a partir de dados, ajustando milhões (depois bilhões) de parâmetros numéricos.

Referências-chave do módulo: TURING (1950), MCCARTHY et al. (1955), ROSENBLATT (1958), MINSKY; PAPERT (1969), RUMELHART; HINTON; WILLIAMS (1986), RUSSELL; NORVIG (2021), GOODFELLOW et al. (2016), NILSSON (1980), SHORTLIFFE (1976).

### 1.2 Deep learning: redes neurais em escala e o divisor de águas Transformer

O aprendizado profundo (deep learning) é o aprendizado de máquina com redes neurais de muitas camadas, viabilizado por três fatores: dados massivos, GPUs para computação paralela e algoritmos eficientes. Marcos: a arquitetura LeNet-5 (1998) de LeCun para reconhecimento de dígitos [10]; o ressurgimento das redes profundas com Hinton e Salakhutdinov (2006) [11]; o divisor de águas AlexNet de Krizhevsky, Sutskever e Hinton (2012), que venceu o ImageNet por ampla margem usando GPU e dropout [12]. Redes convolucionais (CNNs) dominaram visão; redes recorrentes (RNNs, LSTMs) processaram sequências, mas sofriam com sequências longas [13]. A atenção — a ideia de ponderar partes relevantes da entrada — surgiu primeiro em tradução automática [14].

Em 2017, o artigo "Attention Is All You Need", de Vaswani e colegas do Google, propôs o Transformer, uma arquitetura baseada apenas em mecanismos de atenção (multi-head self-attention) e camadas de feed-forward, eliminando a recorrência e permitindo treinamento altamente paralelo [15]. O Transformer é o divisor de águas do PLN moderno: deu origem ao BERT (2018, codificador bidirecional) [16] e à família GPT (2018 em diante, decodificadores autorregressivos) [17]. O dimensionamento seguiu leis de escala: Kaplan et al. (2020) mostraram que desempenho melhora previsivelmente com mais parâmetros, dados e computação [18]; Hoffmann et al. (2022) refinaram a relação ótima entre dados e parâmetros [19]. LeCun, Bengio e Hinton publicaram o artigo-síntese "Deep Learning" na Nature em 2015 [20].

### 1.3 LLMs e agentes autônomos: do chat à ação

Os grandes modelos de linguagem (LLMs) são modelos Transformer treinados em trilhões de tokens. GPT-3 (2020) demonstrou aprendizado em contexto (in-context learning) com poucos exemplos [21]; a alinhamento por RLHF, descrita no artigo do InstructGPT (2022), ensinou os modelos a seguir instruções [22]; o lançamento do ChatGPT em novembro de 2022 levou o paradigma a centenas de milhões de usuários [23]. No mesmo caminho, surgiram Claude (Anthropic, com foco em segurança e treinamento constitucional) [24] e Gemini (Google, multimodal por projeto) [25]. A capacidade de agentes vem de três avanços: (a) chain-of-thought, que melhora o raciocínio ao gerar passos intermediários [26]; (b) o uso de ferramentas — Toolformer (2023) mostrou LLMs aprendendo a chamar APIs [27]; (c) o padrão ReAct (2023), que alterna raciocínio e ação em loop [28]. Surgiram surveys consolidando a área de agentes baseados em LLM [29][30] e a indústria padronizou a chamada de funções (function calling) nas APIs [31]. A Anthropic publicou o guia canônico "Building Effective Agents" (2024), que descreve os padrões de design — prompt chaining, routing, parallelization, orchestrator-workers e evaluator-optimizer [32].

---

## 2. Módulo 2 — A arquitetura em 4 camadas (capítulos 4 e 5)

### 2.1 Por que a IA não é só um chat no navegador

O chat no navegador é uma porta de entrada, mas tem limites: contexto efêmero, sem acesso ao sistema de arquivos do usuário, sem execução de código, sem memória de projeto. O desenvolvedor precisa que a IA leia o repositório, edite arquivos, rode testes e terminal. É por isso que a IA produtiva vive dentro de editores (VS Code), terminais e interfaces de linha de comando. Dados de adoção: pesquisa da Stack Overflow (2024) mostrou que a maioria dos desenvolvedores já usa ou planeja usar ferramentas de IA [33]; levantamento da GitHub (2023) indicou que 92% dos desenvolvedores dos EUA já usam ferramentas de IA em algum momento [34]; a Gartner previu que até 2028 a maioria dos engenheiros de software usará assistentes de código por IA [35]; estudo da Microsoft (Peng et al., 2023) mediu ganho de ~56% em velocidade numa tarefa com assistente de programação [36].

### 2.2 As 4 camadas

O modelo das 4 camadas organiza todo o ecossistema:

1. **A Tela (UI/interface)** — onde o usuário digita e visualiza resultados: VS Code, terminais, interfaces web, apps desktop. É a camada de entrada/saída perceptível.
2. **O Harness (orquestrador)** — o ambiente que gerencia o contexto (quais arquivos, quais regras, qual histórico), prepara as instruções, chama o modelo, recebe a resposta e executa as ferramentas; mantém a memória de trabalho da sessão [32][37]. Exemplos: Claude Code, Cursor, OpenCode, Freebuff.
3. **A LLM (cérebro)** — o modelo de linguagem que raciocina, gera texto, planeja ações e produz código. Não age diretamente: gera texto que o harness interpreta como ações.
4. **As Tools (braços)** — as ferramentas que o harness disponibiliza ao modelo: terminal, execução de código, busca web, leitura/escrita de arquivos, chamadas de API [38]. A Anthropic publicou o guia "Writing Effective Tools" (2025) com princípios de design de ferramentas [39], e o Model Context Protocol (MCP) padronizou a integração de ferramentas externas [40]. A engenharia de contexto — o que entra na janela, em que ordem, com que compressão — virou disciplina própria (Anthropic, 2025) [41].

---

## 3. Módulo 3 — Harnesses (capítulos 6 e 7)

### 3.1 O que é um harness e por que é essencial

Conversar com uma LLM pura (API ou chat) dá ao usuário apenas texto. O harness adiciona o loop agêntico: lê a estrutura de arquivos, injeta regras do projeto (arquivos de instrução como CLAUDE.md/AGENTS.md), decide quais ferramentas chamar, rastreia alterações (diff), mantém memória de trabalho entre mensagens e valida resultados [32][37][41]. A qualidade da "peça" (harness) importa tanto quanto o modelo: dois harnesses com a mesma LLM produzem resultados muito diferentes.

### 3.2 Ecossistema em 2025-2026

- **Claude Code** — harness oficial de terminal da Anthropic; profundo, integrado aos modelos Claude (Sonnet/Opus), com loops de planejamento, edição multi-arquivo e git; uso via assinaturas Pro/Max da Anthropic ou créditos de API [42].
- **Cursor** — IDE baseada em VS Code; autocomplete Tab, chat e agente Composer multi-arquivo; plano Hobby gratuito sem cartão de crédito com limites mensais; pago a partir de US$ 20/mês [43].
- **Antigravity** (Google) — plataforma agêntica lançada em novembro de 2025; dois modos (Editor e Manager); agentes usam navegador e terminal; preview público gratuito para pessoas físicas com limites generosos [44].
- **OpenCode** (sst/opencode) — harness de terminal open source (MIT), model-agnostic, com mais de 75 provedores via ecossistema Models.dev, incluindo modelos locais via Ollama; sessões paralelas, LSP nativo; privacidade: sem retenção de código em servidor remoto [45].
- **MiMo Code** (Xiaomi) — fork do OpenCode focado em tarefas longas (long-horizon, 200+ passos); memória persistente em SQLite FTS5, checkpoints, compressão dinâmica de contexto; open source MIT; canal anônimo MiMo Auto gratuito [46].
- **Freebuff** — ecossistema gratuito de agentes de codificação (CLI, Desktop, Web builder e Cloud sandbox), financiado por anúncios discretos; agrega modelos de fronteira gratuitos (DeepSeek, MiniMax, Kimi); sem necessidade de chaves próprias ou cartão de crédito [47].

Perfil: iniciante pode começar por Freebuff, Cursor Hobby ou OpenCode + modelos gratuitos; avançado prefere Claude Code ou Antigravity.

---

## 4. Módulo 4 — Modelos gratuitos e configuração custo zero (capítulos 8 e 9)

### 4.1 APIs e provedores de roteamento

Uma API de LLM é uma interface HTTP que recebe seu prompt e devolve a resposta do modelo. Provedores de roteamento agregam vários modelos atrás de uma única API. **OpenRouter**: agregador com centenas de modelos; modelos gratuitos marcados com sufixo `:free` e o roteador automático `openrouter/free`; chave gratuita criada no painel; limites por dia/minuto para contas sem saldo [48]. **Groq**: inferência ultrarrápida via hardware LPU; API compatível com OpenAI (base URL `https://api.groq.com/openai/v1`); tier gratuito com limites por modelo — por exemplo, Llama 3.1 8B na casa de ~30 RPM, ~6.000 TPM e ~14.400 RPD, com modelos maiores mais restritos [49]. **Hugging Face**: hub de modelos; Inference Providers oferecem inferência serverless com créditos mensais gratuitos para testes [50]. **Ollama**: execução local, sem limites de nuvem — roda em `http://localhost:11434` e serve modelos abertos como llama3.x, qwen2.5-coder e deepseek-r1 no próprio hardware [51].

### 4.2 Modelos abertos relevantes

- **Llama 3.x (Meta)** — famílias 8B (leve, roda local) e 70B (potente via Groq/OpenRouter), com suporte a tool calling [52].
- **DeepSeek (V3/R1 e DeepSeek-Coder)** — arquiteturas MoE eficientes e modelos de raciocínio; competem com proprietários em lógica e código [53].
- **Qwen (Alibaba)** — Qwen2.5-Coder otimizado para programação, contextos de até 128K+ tokens, excelente em múltiplas linguagens e correção de bugs [54].

Custo zero real: chaves gratuitas de OpenRouter/Groq + harness gratuito (OpenCode/Freebuff) + modelos abertos. Padrão de configuração em ferramentas OpenAI-compatible: provider, base URL, API key e nome do modelo [55].

---

## 5. Módulo 5 — Fluxo de trabalho prático (capítulos 10 a 12)

### 5.1 Engenharia de instruções para iniciantes

Princípios consolidados pelos guias oficiais da Anthropic e OpenAI: (a) contexto rico — o modelo não sabe do seu projeto, forneça o contexto [56][57]; (b) restrições positivas — diga o que fazer, não apenas o que evitar [56]; (c) delimitadores — tags XML (`<instructions>`, `<context>`) na Anthropic, separadores na OpenAI [56][57]; (d) exemplos few-shot (3-5 exemplos) para consistência de formato [57]; (e) chain-of-thought para raciocínio passo a passo [26][58]. Redução de alucinações: fornecer fontes (RAG) [59], exigir citações, temperatura baixa em tarefas factuais, permitir que o modelo declare que não sabe [56][60].

### 5.2 Segurança e privacidade

OWASP Top 10 para aplicações LLM (2025): LLM01 prompt injection (direta e indireta), LLM02 divulgação de informações sensíveis, LLM05 tratamento inadequado de saídas (XSS/SQL injection), LLM06 agência excessiva (permissões demais ao agente), LLM09 desinformação, LLM10 consumo desordenado [61]. NIST AI RMF 1.0 organiza a gestão de risco em quatro funções: Govern, Map, Measure e Manage [62]. Boas práticas para agentes de código: princípio do menor privilégio nas ferramentas, nunca expor chaves de API nos prompts/contexto, fluxos de aprovação humana (human-in-the-loop) para comandos destrutivos ou produção, sandboxes para execução [61][63]. O cenário regulatório inclui o EU AI Act (Regulamento (UE) 2024/1689) [64] e o AI Index da Stanford para acompanhar tendências [65].

---

## 6. Fontes primárias para referências

- TURING, Alan. Computing Machinery and Intelligence. Mind, v. 59, n. 236, 1950.
- MCCARTHY, J. et al. A Proposal for the Dartmouth Summer Research Project on Artificial Intelligence, 1955.
- VASWANI, A. et al. Attention Is All You Need. NeurIPS, 2017.
- RUMELHART, D.; HINTON, G.; WILLIAMS, R. Learning Representations by Back-Propagating Errors. Nature, v. 323, 1986.
- BROWN, T. et al. Language Models are Few-Shot Learners. NeurIPS, 2020.
- OUYANG, L. et al. Training Language Models to Follow Instructions with Human Feedback. NeurIPS, 2022.
- WEI, J. et al. Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. NeurIPS, 2022.
- YAO, S. et al. ReAct: Synergizing Reasoning and Acting in Language Models. ICLR, 2023.
- SCHICK, T. et al. Toolformer. NeurIPS, 2023.
- ANTHROPIC. Building Effective Agents. 2024. Disponível em: https://www.anthropic.com/research/building-effective-agents.
- ANTHROPIC. Effective Context Engineering for AI Agents. 2025. Disponível em: https://www.anthropic.com/research/effective-context-engineering-for-ai-agents.
- ANTHROPIC. Writing Effective Tools. 2025. Disponível em: https://www.anthropic.com/research/writing-effective-tools.
- ANTHROPIC. Model Context Protocol. 2024. Disponível em: https://modelcontextprotocol.io/.
- OPENAI. Best Practices for Prompt Engineering. Disponível em: https://help.openai.com/en/articles/6654000.
- ANTHROPIC. Prompt Engineering Overview. Disponível em: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview.
- OWASP. Top 10 for Large Language Model Applications. 2025. Disponível em: https://genai.owasp.org/llm-top-10/.
- NIST. AI Risk Management Framework 1.0. 2023. Disponível em: https://www.nist.gov/itl/ai-risk-management-framework.
- OPENROUTER. Docs. Disponível em: https://openrouter.ai/docs.
- GROQ. Console Docs — Rate Limits. Disponível em: https://console.groq.com/docs/rate-limits.
- HUGGING FACE. Inference Providers. Disponível em: https://huggingface.co/docs/inference-providers/.
- OLLAMA. Docs. Disponível em: https://ollama.com/.
- OPENCODE. Docs. Disponível em: https://opencode.ai/.
- CURSOR. Pricing. Disponível em: https://cursor.com/pricing.
- GOOGLE. Build with Google Antigravity. 2025. Disponível em: https://developers.googleblog.com/.
- XIAOMI MIMO. MiMo-Code. Disponível em: https://github.com/XiaomiMiMo/MiMo-Code.
- FREEBUFF. Disponível em: https://freebuff.com/.
- META. Llama 3. 2024. Disponível em: https://ai.meta.com/blog/meta-llama-3/.
- DEEPSEEK. DeepSeek-R1. 2025. Disponível em: https://github.com/deepseek-ai/DeepSeek-R1.
- ALIBABA. Qwen2.5-Coder. 2024. Disponível em: https://qwenlm.github.io/blog/qwen2.5-coder-family/.
- RUSSELL, S.; NORVIG, P. Artificial Intelligence: A Modern Approach. 4. ed. Pearson, 2021.
- GOODFELLOW, I. et al. Deep Learning. MIT Press, 2016.
- STANFORD. AI Index Report. Disponível em: https://aiindex.stanford.edu/.
- STACK OVERFLOW. Developer Survey 2024. Disponível em: https://survey.stackoverflow.co/2024/.
- GITHUB. Survey: AI Coding Tools. 2023.
- PENG, S. et al. The Impact of AI on Developer Productivity. arXiv:2302.06590, 2023.
- GARTNER. Prediction: AI Code Assistants. 2023.
- LIU, N. et al. Lost in the Middle. TACL, 2023.
- LEWIS, P. et al. Retrieval-Augmented Generation. NeurIPS, 2020.
- HUANG, L. et al. A Survey on Hallucination in Large Language Models. 2023.
- EU. Regulamento (UE) 2024/1689 (EU AI Act). 2024.
