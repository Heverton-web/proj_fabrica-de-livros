# Dossiê Técnico — Engenharia de Software e Desenvolvimento Agêntico

> Obra: livro (tamanho GG — 10 partes, 50 capítulos, ~1000 páginas, mínimo 100
> referências/capítulo). Este dossiê é o material bruto de pesquisa para o
> Arquiteto desenhar o sumário macro e para os redatores lastrearem cada
> capítulo. Cobre dois grandes eixos que a obra funde: (A) fundamentos clássicos
> de engenharia de software (internet, camadas de aplicação, tecnologias de
> mercado por camada) e (B) engenharia agêntica / AI Driven Development (as 4
> camadas Tela-Harness-Tools-LLM, contexto, arquivos de configuração de agentes,
> economia de tokens), fechando com um projeto prático fim-a-fim.

---

## 1. Como a internet funciona (protocolos, transporte, resolução de nomes)

### 1.1 Modelo de camadas: OSI vs. TCP/IP

A pilha de protocolos da internet é explicada por dois modelos concorrentes: o
modelo OSI, de 7 camadas (Física, Enlace, Rede, Transporte, Sessão,
Apresentação, Aplicação), criado pela ISO nos anos 1980 como referência
didática e não diretamente implementável; e o modelo TCP/IP, de 4 camadas
(Interface de Rede, Internet, Transporte, Aplicação), originado do projeto
DARPA/ARPANET nos anos 1970 e efetivamente usado na internet real. O TCP/IP
agrupa em uma única camada de Aplicação o que o OSI separa em Aplicação,
Apresentação e Sessão (FORTINET; A1 DIGITAL). Este é o ponto de partida
conceitual do capítulo "como a internet funciona": o leitor precisa entender
que todo protocolo do livro (HTTP, TLS, DNS, WebSocket) se encaixa em uma
dessas camadas.

### 1.2 Resolução de nomes: DNS

O DNS traduz nomes de domínio legíveis (`exemplo.com`) em endereços IP. O fluxo
de resolução passa por: verificação de cache local, resolvedor recursivo
(recursive resolver), servidor raiz, servidor de TLD e servidor autoritativo,
até a resposta final ser devolvida ao cliente (FREECODECAMP; NEW RELIC;
CLOUDNS). Vale abordar também os tipos de registro (A, AAAA, CNAME, MX, TXT),
TTL de cache e por que DNS é frequentemente o primeiro ponto de falha
diagnosticado em produção.

### 1.3 Transporte confiável: TCP/IP e o papel do UDP

TCP garante entrega ordenada e confiável via handshake de 3 vias, controle de
congestionamento e retransmissão; UDP é sem conexão e sem garantia de entrega,
usado historicamente para DNS, streaming e, mais recentemente, como base do
QUIC/HTTP-3 (CLOUDFLARE, "What is HTTP/3?"). Entender por que HTTP/3 abandonou
TCP em favor de UDP+QUIC é um dos pontos mais didáticos para conectar
"fundamentos de rede" com "por que meu site está lento".

### 1.4 Segurança de transporte: TLS 1.3

TLS 1.3 (RFC 8446, IETF/RFC EDITOR) reduziu o handshake para 1-RTT (metade do
TLS 1.2), removeu cifras legadas, passou a exigir AEAD com forward secrecy em
toda sessão e cifrou a maior parte do próprio handshake para ganho de
privacidade (THE SSL STORE; LOGICMONITOR). É a base de "cadeado verde no
browser" e de HTTPS como padrão de mercado.

### 1.5 HTTP: semântica, versões e evolução

RFC 9110 (HTTP Semantics) separa formalmente a semântica do HTTP (métodos,
cabeçalhos, códigos de status) da sintaxe de cada versão de transporte
(RFC EDITOR). HTTP/1.1 abre conexões paralelas; HTTP/2 multiplexa múltiplos
fluxos em uma única conexão TCP; HTTP/3 roda sobre QUIC/UDP e resolve o
head-of-line blocking que HTTP/2 ainda sofre em nível de TCP (CLOUDFLARE
BLOG, "Comparing HTTP/3 vs. HTTP/2 Performance"; CLOUDFLARE, "HTTP/3: From
root to tip"). O capítulo de fundamentos de rede deve mostrar essa evolução
como narrativa de otimização de latência.

### 1.6 Comunicação bidirecional: WebSockets

RFC 6455 define o protocolo WebSocket: um handshake de upgrade HTTP seguido de
um framing leve full-duplex sobre uma única conexão TCP, usado para chat,
notificações em tempo real e dashboards ao vivo (RFC EDITOR; WEBSOCKET.ORG).
Extensões relevantes: compressão (RFC 7692), bootstrapping sobre HTTP/2
(RFC 8441) e HTTP/3 (RFC 9220).

### 1.7 CDN e a distribuição geográfica de conteúdo

Uma CDN mantém cópias cacheadas de ativos estáticos em pontos de presença
distribuídos globalmente; a requisição do cliente é roteada para a borda mais
próxima, que responde do cache ou busca no servidor de origem
(CLOUDFLARE, "Content Delivery Network (CDN) Reference Architecture"). Isso
conecta diretamente com o eixo de deploy/performance do projeto prático final.

### 1.8 Modelo cliente-servidor e o ciclo requisição-resposta

A documentação do MDN descreve o modelo cliente-servidor como a base
conceitual de toda a web: clientes enviam requisições, servidores devolvem
respostas (MDN WEB DOCS, "How the Web works"; MDN WEB DOCS, "Overview of
HTTP"). Esse é o gancho para introduzir, no capítulo seguinte, a arquitetura
em camadas (frontend/backend/API/banco de dados) como uma elaboração desse
ciclo básico.

---

## 2. Arquitetura em camadas do software

### 2.1 Visão geral: frontend, backend, banco de dados, API

Uma arquitetura em camadas típica separa: (1) frontend — interface visual que
envia requisições e gerencia estado do cliente; (2) backend — lógica de
negócio, validação e orquestração, intermediário entre frontend e dados; (3)
banco de dados — camada de persistência; (4) API — contrato de comunicação
entre as camadas, com toda requisição atravessando validação, autorização,
lógica de negócio e acesso a dados (MEDIUM, "Common Architectural Patterns in
Full-Stack Web Development"; WEWEB DOCS, "APIs and databases: the critical
connection"; substack "Make Your Backend Layer As Thin As Possible"). Convém
enfatizar a camada de repositório/DAO como isolamento do acesso a dados
(GOALIST BLOG, "Three Layer Architecture in Backend Development").

### 2.2 Camada de Frontend

**Frameworks e bibliotecas.** React (Meta) organiza a UI em componentes
reutilizáveis e é hoje o framework com maior fatia de mercado; Vue.js aposta em
sintaxe de template acessível para times pequenos/médios; Angular (Google)
oferece estrutura opinativa e injeção de dependência para times grandes; Svelte
compila em tempo de build e produz os menores bundles (REACT.DEV, "Quick
Start"; ASCENDIENT LEARNING, "React vs. Angular vs. Vue"; PHAROS PRODUCTION,
"Frontend Framework Comparison 2026"). Next.js (Vercel) adiciona roteamento
por sistema de arquivos, App Router, Server Components e Route Handlers sobre
o React (NEXT.JS DOCS, "App Router: Getting Started").

**Ferramentas de build.** Vite serve módulos ES nativos em desenvolvimento
(HMR quase instantâneo) e empacota para produção via Rolldown; Webpack é o
bundler histórico, mais configurável e mais lento em HMR por reavaliar todo o
grafo de dependências a cada mudança (VITE.DEV, "Why Vite"; LOGROCKET BLOG,
"Vite vs. Webpack for react apps").

**TypeScript.** Adiciona tipagem estática sobre JavaScript; o TypeScript
Handbook é a referência canônica para tipos, generics, narrowing e módulos
(TYPESCRIPT DOCS, "Handbook").

**Renderização e desempenho.** Server-Side Rendering (SSR) entrega HTML já
renderizado no primeiro carregamento (melhor SEO e first paint), enquanto
Client-Side Rendering (CSR) processa tudo no navegador; abordagens híbridas
combinam SSR inicial com hidratação client-side (PIXELFREESTUDIO, "The Role
of SSR in Progressive Web Apps"). Progressive Web Apps (PWA) usam Service
Workers como proxy de rede para cache de ativos e funcionamento offline
(GOOGLE FOR DEVELOPERS, "Progressive Web Apps: Service Worker Includes"; MDN
WEB DOCS, "Structural overview of progressive web apps").

**WebAssembly (WASM).** Formato binário, alvo de compilação para C/C++/Rust/Go,
usado para tarefas computacionalmente pesadas no navegador (jogos, edição de
imagem/vídeo, inferência de ML, CAD) rodando a velocidade quase nativa ao lado
do JavaScript (WEBASSEMBLY.ORG, "Use Cases"; MDN WEB DOCS, "WebAssembly").

**Acessibilidade.** WCAG (W3C) define 4 princípios — perceptível, operável,
compreensível, robusto — e 3 níveis de conformidade (A, AA, AAA); WCAG 2.2 é a
versão vigente recomendada pelo W3C (W3C, "WCAG 2 Overview"; W3C, "Web Content
Accessibility Guidelines (WCAG) 2.2").

### 2.3 Camada de Backend

**Runtimes e linguagens.** Node.js é um runtime JavaScript assíncrono e
orientado a eventos sobre o V8, adequado para I/O concorrente (NODE.JS DOCS,
"About this documentation"). Python oferece Django (framework "baterias
inclusas", ORM e admin nativos) e FastAPI (alto desempenho via Starlette e
Pydantic, tipagem nativa do Python, documentação interativa automática)
(FASTAPI DOCS, "FastAPI"). Java/Spring Boot elimina boilerplate de
configuração XML e oferece autoconfiguração para bancos SQL/NoSQL (SPRING
DOCS, "Spring Boot Reference Documentation"). Go, criado no Google, tem
concorrência nativa via goroutines e é hoje uma das linguagens mais procuradas
para backend por seu runtime leve e binários estáticos (GO.DEV, "Documentation
- The Go Programming Language").

**Padrões arquiteturais.** MVC separa Model/View/Controller e serve bem CRUDs
com baixa complexidade; Arquitetura Hexagonal (Ports & Adapters) isola o
núcleo de domínio da infraestrutura via portas e adaptadores; Clean
Architecture (Robert C. Martin, 2012) combina hexagonal e onion em camadas
concêntricas, recomendada para domínios complexos que exigem alta
testabilidade (WIKIPEDIA, "Hexagonal architecture (software)"; DEV.TO,
"Hexagonal Architecture and Clean Architecture (with examples)";
PRECISIONAIACADEMY, "Software Architecture Patterns in 2026").

**Monolito vs. microsserviços vs. arquitetura orientada a eventos.** Monolitos
são simples de iniciar mas viram gargalo em escala (deploys arriscados, código
emaranhado); microsserviços decompõem em componentes menores comunicando-se
por API/mensageria, permitindo deploy independente por time; arquitetura
orientada a eventos desacopla ainda mais ao fazer serviços publicarem eventos
de mudança de estado sem conhecer os consumidores (DESIGNGURUS, "Monolithic vs
Microservices vs SOA"; EQUAL EXPERTS, "Understanding event-driven architecture
and microservices in comparison to a monolith"; KUBESIMPLIFY, "Event-Driven
Architecture Simplified").

**Mensageria.** Kafka é uma plataforma de streaming de eventos distribuída de
alta vazão, voltada a replay e processamento em larga escala; RabbitMQ é um
broker de mensagens tradicional, com roteamento flexível via exchanges,
melhor para request-response e roteamento complexo (REDPANDA, "RabbitMQ vs.
Kafka"; BAELDUNG, "Pub-Sub vs. Message Queues").

**Princípios de design.** SOLID (Responsabilidade Única, Aberto/Fechado,
Substituição de Liskov, Segregação de Interface, Inversão de Dependência) e os
23 padrões do Gang of Four (Design Patterns, Gamma/Helm/Johnson/Vlissides,
1994), organizados em criacionais, estruturais e comportamentais, seguem sendo
o vocabulário comum de design orientado a objetos (DIGITALOCEAN, "Gang of Four
(GoF) Design Patterns"; LAWS OF SOFTWARE ENGINEERING, "SOLID Principles").

**Metodologia de app cloud-native.** A metodologia Twelve-Factor App
(codebase única, dependências explícitas, config no ambiente, processos sem
estado, portas expostas, admin processes etc.) permanece aplicável mesmo em
arquiteturas serverless como AWS Lambda (AWS COMPUTE BLOG, "Applying the
Twelve-Factor App Methodology to Serverless Applications").

### 2.4 Camada de Banco de Dados

**Relacional (SQL).** PostgreSQL é o banco open-source de referência,
documentado exaustivamente em postgresql.org/docs (POSTGRESQL GLOBAL
DEVELOPMENT GROUP, "PostgreSQL: Documentation"). ACID (Atomicidade,
Consistência, Isolamento, Durabilidade) garante confiabilidade transacional
(MONGODB, "ACID Transactions in DBMS Explained"; MOTHERDUCK, "ACID
Transactions Explained"). Normalização organiza dados em formas normais (1NF,
2NF, 3NF, BCNF, 4NF, 5NF) para eliminar redundância e anomalias de
inserção/atualização/remoção (DIGITALOCEAN, "Database Normalization"; IBM,
"What Is Database Normalization?").

**Não relacional (NoSQL).** MongoDB é orientado a documentos (JSON/BSON),
com suporte a transações ACID multi-documento; Redis é um armazenamento
chave-valor em memória, otimizado para cache, filas e contadores, sem ACID
nativo completo (MONGODB, "MongoDB vs. Redis Comparison"; AWS, "Redis OSS vs
MongoDB").

**Sistemas distribuídos.** O Teorema CAP (Brewer) afirma que um sistema
distribuído não pode garantir simultaneamente Consistência, Disponibilidade e
Tolerância a Partição — apenas duas das três. Replicação copia dados entre nós
para disponibilidade/tolerância a falhas; sharding particiona dados entre
servidores para escalar horizontalmente, geralmente sacrificando alguma
garantia de consistência (PINGCAP, "Understanding the CAP Theorem in
Distributed Systems"; MEDIUM, "Databases Deep Dive: Replication, Sharding,
Partitioning, and the CAP Theorem").

### 2.5 Camada de API

**REST.** Definido por Roy Fielding em sua tese de doutorado (2000) como um
estilo arquitetural de 6 restrições (interface uniforme, stateless,
cacheável, sistema em camadas, código sob demanda, cliente-servidor); Fielding
esclareceu em 2008 que uma API só é verdadeiramente RESTful se for
hypertext-driven (HATEOAS) (OLEB.NET, "Roy Fielding's REST dissertation";
RESTFULAPI.NET, "REST API Best Practices").

**GraphQL.** Linguagem de consulta e runtime de servidor open-sourced em 2015,
hoje sob a GraphQL Foundation (Linux Foundation); permite ao cliente pedir
exatamente os campos que precisa, evitando over-fetching/under-fetching
(GRAPHQL.ORG; GRAPHQL SPECIFICATION).

**gRPC e Protocol Buffers.** gRPC é um sistema RPC open-source do Google que
usa Protocol Buffers como IDL e formato de serialização binário, mais
compacto e rápido que JSON, com forte tipagem e geração de código em múltiplas
linguagens (GRPC.IO, "Introduction to gRPC"; PROTOBUF.DEV, "Overview").

**Documentação de API.** OpenAPI Specification (ex-Swagger, doado à OpenAPI
Initiative em 2015) é o formato padrão para descrever APIs REST de forma
legível por máquina e humano; o ecossistema Swagger (Editor, UI, Codegen)
constrói ferramentas sobre essa especificação (SWAGGER, "OpenAPI
Specification - Version 3.1.0").

**Autenticação e autorização.** OAuth 2.0 padroniza autorização ("o que você
pode acessar"); OpenID Connect (OIDC) é uma camada de identidade sobre o OAuth
2.0 que adiciona autenticação ("quem é você") via ID Token em formato JWT
(CONNECT2ID, "OpenID Connect explained"; MEDIUM, "The Complete Guide to OAuth
2.0, OpenID Connect, and JWT Token Verification").

**Segurança de API e aplicações web.** O OWASP Top 10 é o documento de
consenso sobre os riscos mais críticos de segurança em aplicações web,
atualizado periodicamente pela OWASP Foundation; a edição em preparação
enfatiza segurança de cadeia de suprimentos, configuração incorreta e design
seguro (OWASP FOUNDATION, "OWASP Top Ten Web Application Security Risks").
Hashing de senha deve usar funções lentas e com salt (bcrypt, Argon2id) —
nunca hash rápido isolado como SHA-256 puro (KINDE, "Guide to Bcrypt
Hashing").

### 2.6 Segurança aprofundada: criptografia, TLS avançado e vulnerabilidades web

**Criptografia simétrica e assimétrica.** Criptografia simétrica usa uma única
chave compartilhada tanto para cifrar quanto para decifrar — AES é hoje o
padrão de mercado, com AES-256 considerado computacionalmente inviável de
quebrar por força bruta em qualquer hardware clássico previsível; criptografia
assimétrica usa par de chaves pública/privada — RSA (mínimo 2048 bits, 4096
recomendado) e ECC (Elliptic Curve Cryptography, que atinge segurança
equivalente ao RSA com chaves muito menores — 256 bits ECC ≈ 3072 bits RSA —
sendo preferida em mobile, IoT e TLS 1.3) (IBM, "What is Asymmetric
Encryption?"; DESTCERT, "Asymmetric Cryptography: RSA, ECC & PKI Explained").
Na prática, sistemas reais combinam as duas abordagens em esquema híbrido:
assimétrico para troca segura de chave de sessão, simétrico (AES) para cifrar
o volume de dados em alta velocidade.

**Certificate pinning.** Técnica client-side que restringe a confiança do
cliente a um certificado, chave pública ou CA específicos, em vez de aceitar
qualquer certificado validado pela cadeia de confiança padrão do sistema
operacional — mitiga ataques man-in-the-middle mesmo que uma CA seja
comprometida, mas exige governança rigorosa do ciclo de vida do certificado no
backend e pinos de backup para não quebrar o app numa rotação de certificado.
A recomendação de mercado em 2026 é usar pinning seletivamente (conexões
cliente-servidor fechadas e de alto valor), não como padrão universal — HPKP
(HTTP Public Key Pinning, via cabeçalho HTTP) está obsoleto nos browsers
modernos, substituído por Certificate Transparency (OWASP FOUNDATION,
"Certificate and Public Key Pinning"; SSL.COM, "What Is Certificate
Pinning?"; PALO ALTO NETWORKS, "What Is Certificate Pinning?").

**CORS.** Cross-Origin Resource Sharing é o mecanismo baseado em cabeçalhos
HTTP (`Access-Control-Allow-Origin` e correlatos) pelo qual um servidor
autoriza explicitamente que um navegador carregue seus recursos a partir de
uma origem diferente — sem CORS, a same-origin policy do browser bloquearia
por padrão toda requisição cross-origin feita via `fetch`/`XMLHttpRequest`;
requisições não triviais disparam antes uma requisição "preflight" (`OPTIONS`)
que verifica se o servidor autoriza o método e os cabeçalhos pretendidos (MDN
WEB DOCS, "Cross-Origin Resource Sharing (CORS)"; PORTSWIGGER, "What is
CORS?"). Configuração incorreta de CORS — refletir dinamicamente qualquer
`Origin` recebido, ou confiar em subdomínios que podem ser sequestrados — é
classificada dentro do risco A05 (Security Misconfiguration) do OWASP Top 10,
com o CWE-942 cobrindo especificamente CORS excessivamente permissivo (OWASP
FOUNDATION, "A05:2021 – Security Misconfiguration").

**CSRF.** Cross-Site Request Forgery força o navegador autenticado da vítima a
executar, sem seu consentimento, uma requisição de estado (transferência,
troca de e-mail etc.) contra um site em que ela já tem sessão ativa — funciona
porque o browser anexa automaticamente os cookies de sessão a toda requisição
para aquele domínio; as defesas de mercado são cookies `SameSite`, tokens CSRF
sincronizados (synchronizer token pattern) e cabeçalhos customizados
verificados no servidor (OWASP FOUNDATION, "Cross Site Request Forgery
(CSRF)"; OWASP CHEAT SHEET SERIES, "Cross-Site Request Forgery Prevention
Cheat Sheet").

**XSS em profundidade.** A OWASP classifica Cross-Site Scripting em três
variantes: refletido (o payload malicioso vem na própria requisição —
URL/query string — e é ecoado de volta pelo servidor sem sanitização,
executando ao clique em um link malicioso), armazenado (o payload é
persistido no servidor — banco, campo de comentário — e servido a qualquer
usuário que acesse o recurso comprometido) e baseado em DOM (o próprio script
client-side manipula o DOM de forma insegura, sem que o payload nunca trafegue
pelo servidor). Em qualquer variante, o efeito é o mesmo: o atacante ganha
controle completo da sessão do navegador da vítima (OWASP FOUNDATION, "Cross
Site Scripting (XSS)"; OWASP FOUNDATION, "Types of XSS").

**Fundamentos de pentest.** Teste de penetração formaliza a simulação
controlada de um ataque real contra um sistema, seguindo metodologias como
OSSTMM (pré-teste, teste, pós-teste) ou PTES; o modelo de cinco estágios mais
citado no mercado é reconhecimento → varredura (scanning, com ferramentas como
Nmap) → avaliação/exploração de vulnerabilidades (Metasploit, Burp Suite) →
escalonamento de privilégio/manutenção de acesso → relatório final com
evidência e recomendação de remediação (IMPERVA, "What is Penetration
Testing"; EC-COUNCIL, "5 Penetration Testing Phases").

### 2.7 Arquitetura de dados avançada e comunicação em tempo real

**Event sourcing e CQRS.** Event sourcing persiste o estado da aplicação como
uma sequência ordenada e imutável de eventos, em vez de sobrescrever uma linha
de tabela a cada mudança — permite reconstruir o estado de qualquer entidade
em qualquer ponto do tempo e produz trilha de auditoria nativa; CQRS (Command
Query Responsibility Segregation) separa o caminho de escrita (comandos, que
mutam estado) do caminho de leitura (queries, otimizadas para consulta,
geralmente como projeções pré-computadas) (MICROSOFT LEARN, "Event Sourcing
pattern"; MICROSOFT LEARN, "CQRS Pattern"; MICROSERVICES.IO, "Pattern: Event
sourcing"). Os dois padrões costumam ser combinados em arquiteturas de
microsserviços para escalar leitura e escrita de forma independente, ao custo
de consistência eventual entre os dois lados — trade-off que o livro deve
deixar explícito como decisão consciente, não acidente de design.

**WebRTC.** Protocolo/conjunto de APIs open-source para comunicação
peer-to-peer em tempo real de áudio, vídeo e dados diretamente entre
navegadores, sem plugin — usa servidores STUN para descobrir o IP/porta
público do cliente atrás de NAT e servidores TURN como relay quando a conexão
direta não é possível; toda mídia e canal de dados trafega cifrado nativamente
(PUBNUB, "What is WebRTC (Peer-to-Peer Technology)"; ABLY, "What is WebRTC?").

**Feature flags.** Técnica que permite ligar/desligar uma funcionalidade em
produção sem novo deploy, controlando o código no runtime — usos centrais
incluem kill switch/circuit breaker (desativar uma feature instável sem
rollback), rollout progressivo, experimentação (A/B) e trunk-based development
(evita branches de feature de vida longa); boas práticas de mercado: desenhar
a flag desde o início (não como remendo), evitar flags aninhadas, e eliminar
flags obsoletas rapidamente para não acumular dívida de complexidade
condicional (LAUNCHDARKLY, "Feature Flags 101: Use Cases, Benefits, and Best
Practices"; LAUNCHDARKLY, "7 Feature Flag Best Practices for Short-Term and
Permanent Flags").

**Edge computing.** Modelo de computação distribuída que move processamento e
armazenamento para a borda da rede, fisicamente mais perto do usuário final,
reduzindo latência e uso de banda — difere de uma CDN tradicional (que só
cacheia e entrega conteúdo estático) por também executar lógica de aplicação
(edge functions) próxima ao usuário; funções de borda servem tipicamente para
personalização, autenticação e transformação de resposta sem o round-trip até
um datacenter central (GEEKSFORGEEKS, "CDN Vs Edge Server - System Design";
FASTPIX, "Edge Computing vs. CDN").

---

## 3. Engenharia Agêntica e AI Driven Development

### 3.1 Definição: do "vibe coding" à engenharia agêntica

Andrej Karpathy cunhou "vibe coding" para descrever prompt-aceitar-rodar sem
revisão rigorosa (elevando o "piso" de quem pode programar) e distingue disso
a "engenharia agêntica": orquestrar múltiplos agentes contra uma especificação
formal, com avaliações (evals), observabilidade e responsabilidade humana
mantida sobre segurança, regressões e manutenibilidade (elevando o "teto" do
que engenheiros profissionais conseguem entregar) (SUBSTACK, "From Vibe Coding
to Agentic Engineering: Andrej Karpathy's Vision"; FRANK'S WORLD, "Andrej
Karpathy on the Evolution from Vibe Coding to Agentic Engineering"). Karpathy
também descreve "Software 3.0": programar deixa de ser "escrever código" e
passa a ser "escrever contexto", com o LLM como intérprete e a janela de
contexto como a alavanca central (LITTLEX, "Software 3.0 — From Vibe Coding to
Agentic Engineering"). Definições complementares de mercado descrevem
engenharia agêntica como a disciplina em que humanos definem metas,
restrições e padrões de qualidade, enquanto agentes autônomos executam a
implementação sob supervisão (SMARTDEV, "What is Agentic Engineering?"; IBM,
"What is Agentic Engineering?").

### 3.2 As quatro camadas do AI Driven Development

A obra organiza o "engenheiro agêntico" em torno de quatro camadas
funcionais — Tela, Harness, Tools e LLM — que se empilham entre a intenção
humana e a execução real de código.

#### 3.2.1 Camada Tela (interface de interação humana)

A "Tela" é a superfície onde o humano formula intenção: IDEs com IA embutida
(Cursor, Windsurf, VS Code+extensões), CLIs agênticas (Claude Code) e
aplicações web de chat. Cursor exige uso da IDE proprietária (fork do VS
Code) com fluxo de colaboração controlada, decisão do desenvolvedor a cada
passo; Windsurf mantém experiência consistente em 40+ IDEs via plugin e
prioriza acesso ilimitado a agentes (WINDSURF, "Windsurf vs Cursor"; QODO,
"Windsurf vs Cursor: Which AI IDE Tool is Better?"). Prompt engineering — a
técnica central da camada Tela — é definida pela Anthropic como comunicação:
falar a linguagem que ajuda o modelo a entender a intenção com clareza,
preferindo a estrutura mínima necessária sobre prompts longos, usando
few-shot examples e um ciclo iterativo de rascunho→teste→refinamento
(ANTHROPIC/CLAUDE, "Prompt engineering best practices for 2026"; CLAUDE
PLATFORM DOCS, "Prompting best practices").

#### 3.2.2 Camada Harness (motor de execução do agente)

O harness é "tudo que fica entre o modelo de linguagem e o mundo real" —
decide o que o texto gerado pode efetivamente tocar. O Claude Code expõe
cerca de 19 ferramentas com permissionamento granular (leitura/edição de
arquivo, execução de shell, operações Git, fetch web, edição de notebook,
chamadas MCP), cuidando de despacho de ferramentas, permissões, gestão de
contexto, persistência de sessão e recuperação de erro — poupando o
desenvolvedor de construir seu próprio loop de agente (WAVESPEED BLOG, "Claude
Code Agent Harness: Architecture Breakdown"; GITHUB, "ai-boost/awesome-harness-
engineering"). A multiplicidade de harnesses no mercado (Claude Code, Cursor,
Windsurf, Zed, GitHub Copilot Workspace) reflete apostas distintas de UX,
integração de ferramentas e modelo de precificação — não uma diferença de
capacidade fundamental do LLM subjacente. O conceito de "meta-harness" —
orquestrar múltiplos agentes/harnesses coordenados contra uma especificação
comum, cada um aplicando estratégias diferentes de engenharia de contexto —
aparece no sistema de pesquisa multiagente da própria Anthropic, que superou
um único agente Opus 4 em 90,2% em tarefas de pesquisa ampla (ANTHROPIC
ENGINEERING, "Effective context engineering for AI agents"). Frameworks de
orquestração multiagente de terceiros incluem LangGraph (grafos de estado com
nós/arestas, DAG explícito, mais previsível sob casos de borda) e AutoGen da
Microsoft (colaboração via conversação estruturada entre agentes) (LATENODE,
"LangGraph Multi-Agent Orchestration"; MEDIUM, "Agent Orchestration: When to
Use LangChain, LangGraph, AutoGen"). Além desses dois, o mercado de 2026
consolidou outras três apostas de meta-harness/orquestração multiagente:
OpenAI Agents SDK, que trata agentes como primitivas leves de orquestração —
cada um definido por instruções, modelo e ferramentas — conectadas por
transferência explícita de controle entre agentes ("handoffs"); Google Agent
Development Kit (ADK), framework open-source e agnóstico de modelo, otimizado
para o ecossistema Gemini mas compatível com outros frameworks, com suporte
nativo à composição de times de agentes especializados que colaboram e
delegam tarefas entre si; e Microsoft AutoGen/AG2 (fork open-source liderado
pela comunidade, compatível com o estilo legado "GroupChat" v0.2), que resolve
colaboração via conversação estruturada entre agentes — a própria Microsoft já
recomenda o Microsoft Agent Framework mais recente para novos projetos de
longo prazo, sinalizando que mesmo dentro de um único fornecedor o panorama de
harnesses de orquestração está em consolidação ativa, não estabilizado (OPENAI,
"Agents SDK"; OPENAI, "openai-agents-python"; GOOGLE, "Agent Development Kit
(ADK) - Technical Overview"; MICROSOFT, "autogen: A programming framework for
agentic AI").

#### 3.2.3 Camada Tools (ferramentas acessíveis ao agente)

"Tool use"/"function calling" é o protocolo estruturado pelo qual um LLM
solicita a execução de uma função externa durante a inferência, recebendo o
resultado de volta para raciocinar sobre ele; todo grande provedor (OpenAI,
Anthropic, Google) suporta o padrão, com nomenclatura e schemas distintos —
Anthropic chama de "tool use" e enfatiza schemas agnósticos de modelo,
enquanto OpenAI usa "function calling" com tipagem mais rígida (QVERIS,
"Function Calling: OpenAI vs Anthropic vs Google (2026)"). O Model Context
Protocol (MCP), introduzido pela Anthropic em novembro de 2024, é um padrão
aberto — descrito como "USB-C para IA" — que permite qualquer aplicação de IA
(cliente MCP) se conectar a qualquer fonte de dados ou serviço (servidor MCP)
via um protocolo único de mensagens (Requests, Results, Errors,
Notifications) sobre stdio ou HTTP+SSE (ANTHROPIC, "Introducing the Model
Context Protocol"; ANTHROPIC ENGINEERING, "Code execution with MCP: building
more efficient AI agents"). Skills (Agent Skills) são pacotes de capacidade
baseados em sistema de arquivos — pastas com instruções, scripts e recursos
que o modelo carrega dinamicamente só quando a tarefa exige, complementando
(não substituindo) tanto tool use nativo quanto servidores MCP (CLAUDE
PLATFORM DOCS, "Agent Skills - Overview"; GITHUB, "anthropics/skills").
Distinção prática que o livro deve deixar clara: MCP conecta o agente a
sistemas/dados externos (servidores rodando fora do processo do modelo);
Skills são conhecimento procedural empacotado que o próprio agente carrega
como contexto sob demanda; ambos contam como "Tools" na camada, mas resolvem
problemas diferentes — acesso a dados/serviços vs. instrução repetível de
como fazer uma tarefa.

#### 3.2.4 Camada LLM (o modelo de linguagem)

O panorama de mercado 2026 inclui três famílias fechadas líderes — Claude
(Anthropic, com os níveis Opus/Sonnet/Haiku), GPT (OpenAI, família GPT-5.x) e
Gemini (Google, família Gemini 3, com janela de contexto de até 1 milhão de
tokens) — e alternativas abertas como Llama, Mistral e DeepSeek, executáveis
localmente via Ollama, vLLM ou llama.cpp para cenários de privacidade/custo
(CLAUDE PLATFORM DOCS, "Models overview"; AI.GOOGLE.DEV, "Using the latest
Gemini models"; HUGGING FACE, "The Best Open Source and Open-Weight LLM Models
to Run Locally"). O SWE-bench (e suas variantes Verified, Lite, Pro) é hoje o
benchmark padrão de mercado para avaliar agentes de codificação em tarefas
reais de GitHub, medindo se o patch gerado faz os testes FAIL_TO_PASS e
PASS_TO_PASS passarem (DEMANDSPHERE, "SWE-bench Verified - AI Benchmark
Explained"). Escolha de modelo, na prática, é uma decisão de trade-off entre
capacidade de raciocínio/código, custo por token, latência e disponibilidade
via API/nuvem própria — não existe "o melhor modelo" universal, existe o
modelo adequado à tarefa e ao orçamento de tokens.

**Painel comparativo com fontes primárias (ago. 2026).** Consultando apenas a
documentação oficial de cada provedor (sem agregador de terceiros e sem nome
de modelo não-oficial): a documentação oficial da Anthropic lista os níveis
Haiku 4.5 (US$ 1/US$ 5 por milhão de tokens de input/output), Sonnet 5 (preço
introdutório de US$ 2/US$ 10 até 31 de agosto de 2026, subindo depois para
US$ 3/US$ 15) e Opus 5 (US$ 5/US$ 25), com leitura de prompt cache cobrada a
10% do preço-base de input e a Batch API concedendo 50% de desconto em input
e output (CLAUDE PLATFORM DOCS, "Pricing"). A documentação oficial da OpenAI
lista a família GPT-5.6 (Sol, Terra, Luna) com janela de contexto de
aproximadamente 1,05 milhão de tokens, máximo de 128 mil tokens de saída e
knowledge cutoff de fevereiro de 2026 (OPENAI, "Models"; OPENAI, "Pricing"). A
documentação oficial do Google lista a família Gemini 3 (3.6 Flash, 3.5 Flash,
3.5 Flash-Lite, 3.1 Pro em preview), também com 50% de desconto via Batch API,
e mantém fichas técnicas (model cards) publicadas separadamente pelo Google
DeepMind para os modelos de ponta da linha Pro (GOOGLE AI FOR DEVELOPERS,
"Gemini models"; GOOGLE AI FOR DEVELOPERS, "Gemini API Pricing"; GOOGLE
DEEPMIND, "Gemini 3 Pro Model Card"). Nenhuma das três famílias diverge
fundamentalmente em suporte a tool use/function calling — a diferença de
mercado está em custo por token, tamanho de janela de contexto e política de
cache/batch, reforçando que escolha de modelo é engenharia de custo-benefício,
não torcida de marca.

### 3.3 Contexto e engenharia de contexto

A janela de contexto é análoga a "RAM" do LLM — grande, mas finita; tokens são
frações de palavra (~3/4 de palavra em média) (MEDIUM, "LLM Context
Engineering: a practical guide"). Engenharia de contexto é a curadoria do que
entra nessa janela limitada a partir de um universo de informação em constante
mudança, organizando quatro estratégias (write, select, compress, isolate)
para lidar com "context rot" — a degradação da capacidade de recall do modelo
à medida que mais tokens são adicionados ao contexto (ANTHROPIC ENGINEERING,
"Effective context engineering for AI agents"; BLOG.BYTEBYTEGO, "A Guide to
Context Engineering for LLMs"). RAG (Retrieval-Augmented Generation) reduz o
número de tokens processados ao recuperar apenas o trecho mais relevante para
cada consulta via banco vetorial, em vez de carregar todo o corpo de
conhecimento na janela (GOOGLE CLOUD, "What is Retrieval-Augmented Generation
(RAG)?"; CONFLUENT, "What is Retrieval Augmented Generation (RAG)?").
Embeddings são representações vetoriais de tokens que capturam relação
semântica (o vetor de "rei" fica matematicamente próximo de "rainha"); bancos
vetoriais armazenam esses embeddings e permitem busca por significado, não só
por palavra-chave exata (THE NEW STACK, "The Building Blocks of LLMs: Vectors,
Tokens and Embeddings").

### 3.4 Arquivos de configuração do engenheiro agêntico

O livro precisa desfazer a confusão comum de mercado entre esses termos —
cada um resolve um problema diferente na pilha de configuração de um agente:

- **CLAUDE.md / AGENTS.md** — "memória" textual em Markdown, lida pelo agente
  no início de cada sessão, contendo convenções do projeto, comandos de
  build/teste e regras de estilo. AGENTS.md tornou-se um padrão aberto formal
  em agosto de 2025 (liderado pela OpenAI, com Google/Cursor/Factory), doado à
  Linux Foundation Agentic AI Foundation em dezembro de 2025, hoje adotado por
  mais de 60 mil projetos open-source e suportado por 20+ ferramentas — sem
  estrutura obrigatória, é Markdown livre (AGENTS.MD; GITHUB,
  "agentsmd/agents.md"). CLAUDE.md é o equivalente específico da Anthropic,
  editável via `/init` e `/memory` no Claude Code (CLAUDE CODE DOCS,
  "Commands"). **Erro comum de mercado:** tratar esses arquivos como "prompt
  mágico" — na prática funcionam melhor como documentação objetiva e concisa
  (comandos reais, não aspiração de comportamento).
- **SKILLS** — pastas com instruções + scripts + recursos carregadas sob
  demanda (ver 3.2.3); diferem de CLAUDE.md por serem modulares e carregadas
  apenas quando relevantes, não em toda sessão.
- **MCPs** — servidores externos (processo separado) que expõem ferramentas e
  dados via protocolo padronizado (ver 3.2.3); não são arquivos de
  configuração de prompt, são integrações de sistema.
- **SPECS** — documentos formais de especificação tratados como artefato
  primário e executável de um projeto; o código é saída regenerável derivada
  do spec por humanos, agentes ou ambos — resposta direta à falha de "vibe
  coding" sem verificação (THE BCMS, "Spec-Driven Development (SDD): The
  Definitive 2026 Guide"; GITHUB BLOG, "Spec-driven development with AI").
- **COMMANDS** — arquivos Markdown com frontmatter YAML em
  `.claude/commands/<nome>.md`, definindo prompts reutilizáveis invocados via
  `/nome` dentro de uma sessão (CLAUDE CODE DOCS, "Commands").
- **HOOKS** — comandos shell disparados pelo harness em pontos fixos do ciclo
  de vida da sessão (PreToolUse, PostToolUse, Stop, Notification); são o
  mecanismo de maior alavancagem para impor regras de forma determinística —
  por exemplo, bloquear uma chamada de ferramenta antes que ela execute
  (código de saída 2 em PreToolUse) (CLAUDE CODE DOCS, "Claude Code settings";
  EXPLAINX.AI, "Claude Code settings.json: Every Option Explained").
- **RULES** — regras de projeto (ex.: `.cursor/rules/*.mdc`, `.windsurfrules`,
  ou seções normativas dentro do próprio CLAUDE.md/AGENTS.md) que restringem
  comportamento do agente por convenção declarativa, sem executar código —
  complementam hooks (que são imperativos/executáveis).
- **SCRIPTS** — automação determinística invocada pelo agente ou por hooks
  (linters, geradores, validadores); a diferença crucial para o livro é que
  scripts produzem veredito objetivo (sai um JSON/exit code), enquanto prompts
  produzem texto que ainda precisa ser interpretado — daí a importância de
  scripts para qualquer verificação que precise ser confiável em escala.
- **MEMORY.MD / arquivos de memória contínua** — complementam CLAUDE.md/
  AGENTS.md guardando aprendizados de sessão a sessão (decisões, erros
  conhecidos), tema pouco documentado oficialmente mas cada vez mais comum em
  harnesses de produção.
- **CONFIG.JSON / settings.json** — configuração estrutural do harness em si
  (permissões, modelos padrão, hooks registrados) — não é memória nem
  instrução de projeto, é configuração de comportamento do runtime do agente
  (CLAUDE CODE DOCS, "Claude Code settings").

### 3.5 Economia real de tokens (sem enrolação)

Técnicas com efeito mensurável e documentado, por ordem de impacto:

1. **Prompt caching** — armazena a representação processada de um prefixo de
   prompt estável; leituras de cache custam ~10% do preço normal de input
   (desconto de até 90%), e escrita custa 1,25x o normal; reduz também
   latência em até 85% (CLAUDE PLATFORM DOCS, "Prompt caching"; NGROK BLOG,
   "Prompt caching: 10x cheaper LLM tokens, but how?"). Prática: organizar o
   prompt em um prefixo estático cacheável (system prompt, definições de
   ferramentas, base de conhecimento) seguido da parte dinâmica da requisição.
2. **Batching** — processamento em lote é cerca de 50% mais barato em todos
   os modelos; agrupar N consultas com contexto compartilhado em uma única
   chamada evita pagar o mesmo system prompt de 2.000 tokens N vezes
   (MORPHLLM, "LLM Cost Optimization: 5 Levers to Cut API Spend 70-85%").
3. **RAG em vez de contexto integral** — recuperar só o trecho relevante via
   busca vetorial/TF-IDF, em vez de carregar um dossiê/documento inteiro no
   prompt (o próprio padrão adotado por este projeto via
   `scripts/indexar-dossie.py`) (GOOGLE CLOUD, "What is Retrieval-Augmented
   Generation (RAG)?").
4. **Roteamento de modelo por tarefa** — usar o modelo mais barato/rápido
   (ex.: Haiku) para tarefas simples de alto volume e reservar o modelo mais
   caro (Opus) para raciocínio complexo — cinco alavancas combinadas (caching,
   batching, compressão de prompt, seleção de modelo, cache de resposta)
   cortam gasto em 70-85% sem trocar o que o agente produz (MORPHLLM, "LLM
   Cost Optimization"; TECHSY, "12 Ways to Reduce LLM API Costs by 80%").
5. **Compressão de saída de terminal/logs** (o que este próprio projeto chama
   de "headroom"/"rtk") — nunca aplicável a conteúdo de obra/negócio, apenas a
   saída efêmera de build/teste/CLI — é uma técnica de engenharia de contexto
   do lado do harness, não do provedor de LLM.
6. **Evitar recontagem de histórico completo** — nem toda mensagem de um
   agente de longa duração precisa do histórico integral; sumarização
   periódica e "scratchpads" externos (grava plano/notas fora da janela de
   contexto) evitam custo linear crescente por turno (ANTHROPIC ENGINEERING,
   "Effective context engineering for AI agents").

**O que raramente é divulgado ao público convencional:** a maior parte do
"desperdício" de tokens em produção não vem do modelo, vem do harness —
system prompts redundantes reenviados a cada chamada, ferramentas descritas
em excesso de detalhe, e ausência de cache de prefixo. Cortar aqui tem efeito
maior que qualquer técnica de "prompt enxuto" isolada.

---

## 4. Projeto prático fim-a-fim (arquitetura → testes → deploy/containerização)

### 4.1 Da especificação ao código

Aplicando spec-driven development: escrever a especificação (requisitos,
contratos de API via OpenAPI, modelo de dados) antes de gerar implementação
com agente, evitando o modo de falha do "vibe coding" sem verificação
(ADDYOSMANI.COM, "How to write a good spec for AI agents").

### 4.2 Testes: pirâmide e TDD

A pirâmide de testes recomenda muitos testes unitários na base, menos testes
de integração no meio, e poucos testes end-to-end no topo — proporção comum
de ~70/20/10; TDD (escrever o teste antes do código) tende a produzir uma
suíte unitária mais robusta naturalmente (QASE, "The test pyramid: A complete
guide"; MOMENTIC, "The Software Testing Pyramid: Unit, Integration, and E2E
Testing Explained").

### 4.3 Controle de versão e CI/CD

Git Flow usa 5 tipos de branch (main, develop, feature, release, hotfix);
GitHub Flow simplifica para branch de produção + feature branches revisadas
via PR; trunk-based development favorece integração contínua em um único
branch principal (ATLASSIAN, "A Guide to Optimal Branching Strategies in
Git"). GitHub Actions automatiza build/teste/deploy via arquivos YAML em
`.github/workflows`, disparados por eventos como push ou pull request (GITHUB
DOCS, "Quickstart for GitHub Actions").

### 4.4 Containerização

Boas práticas de Docker: imagens base mínimas (ex.: Alpine), builds
multi-stage, tags de versão precisas (nunca `latest` em produção), usuário
não-root no container, `.dockerignore` abrangente e scanner de vulnerabilidade
(Trivy/Clair) (DOCKER DOCS, "Building best practices"; BETTER STACK, "Docker
Security: 14 Best Practices You Should Know").

### 4.5 Orquestração e infraestrutura como código

Kubernetes orquestra containers em produção; pipelines CI/CD Kubernetes-native
(Tekton, Argo CD, Jenkins X) integram build→teste→deploy com estratégias
blue-green/canary para rollout de baixo risco (DEVTRON.AI, "CI/CD Pipeline for
Kubernetes: The Ultimate Guide"). Terraform (HashiCorp) declara infraestrutura
como código via HCL, com providers para AWS/Azure/GCP e mais de 1.000
integrações no Terraform Registry (HASHICORP DEVELOPER, "What is
Infrastructure as Code with Terraform?").

### 4.6 API Gateway, service mesh e observabilidade

Istio atua como service mesh com Gateway como load balancer na borda da malha,
podendo encadear com ingress controllers de terceiros (ISTIO.IO, "Istio /
Gateway"). Prometheus coleta métricas como séries temporais via scraping;
Grafana consome essas séries para dashboards de observabilidade (GRAFANA
DOCS, "What is Prometheus?"). Essa camada fecha o ciclo de "deploy visível" do
projeto prático — não basta subir o container, é preciso observar o sistema em
produção.

---

## 5. Fontes brutas

- ANTHROPIC. *Introducing the Model Context Protocol*. Disponível em: https://www.anthropic.com/news/model-context-protocol. Acesso em: 03 ago. 2026.
- ANTHROPIC. *Effective context engineering for AI agents*. Disponível em: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents. Acesso em: 03 ago. 2026.
- ANTHROPIC. *Code execution with MCP: building more efficient AI agents*. Disponível em: https://www.anthropic.com/engineering/code-execution-with-mcp. Acesso em: 03 ago. 2026.
- CLAUDE (ANTHROPIC). *Prompt engineering best practices for 2026*. Disponível em: https://claude.com/blog/best-practices-for-prompt-engineering. Acesso em: 03 ago. 2026.
- CLAUDE PLATFORM DOCS. *Prompting best practices*. Disponível em: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices. Acesso em: 03 ago. 2026.
- CLAUDE PLATFORM DOCS. *Models overview*. Disponível em: https://platform.claude.com/docs/en/about-claude/models/overview. Acesso em: 03 ago. 2026.
- CLAUDE PLATFORM DOCS. *Agent Skills - Overview*. Disponível em: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview. Acesso em: 03 ago. 2026.
- CLAUDE PLATFORM DOCS. *Prompt caching*. Disponível em: https://platform.claude.com/docs/en/build-with-claude/prompt-caching. Acesso em: 03 ago. 2026.
- CLAUDE CODE DOCS. *Commands*. Disponível em: https://code.claude.com/docs/en/commands. Acesso em: 03 ago. 2026.
- CLAUDE CODE DOCS. *Claude Code settings*. Disponível em: https://code.claude.com/docs/en/settings. Acesso em: 03 ago. 2026.
- GITHUB. *anthropics/skills: Public repository for Agent Skills*. Disponível em: https://github.com/anthropics/skills. Acesso em: 03 ago. 2026.
- GITHUB. *ai-boost/awesome-harness-engineering*. Disponível em: https://github.com/ai-boost/awesome-harness-engineering. Acesso em: 03 ago. 2026.
- WAVESPEED. *Claude Code Agent Harness: Architecture Breakdown*. Disponível em: https://wavespeed.ai/blog/posts/claude-code-agent-harness-architecture/. Acesso em: 03 ago. 2026.
- AGENTS.MD. *AGENTS.md*. Disponível em: https://agents.md/. Acesso em: 03 ago. 2026.
- GITHUB. *agentsmd/agents.md: AGENTS.md — a simple, open format for guiding coding agents*. Disponível em: https://github.com/agentsmd/agents.md. Acesso em: 03 ago. 2026.
- INFOQ. *AGENTS.md Emerges as Open Standard for AI Coding Agents*. Disponível em: https://www.infoq.com/news/2025/08/agents-md/. Acesso em: 03 ago. 2026.
- MORPHLLM. *AGENTS.md Spec (2026): Recommended Sections*. Disponível em: https://www.morphllm.com/agents-md-guide. Acesso em: 03 ago. 2026.
- GITHUB BLOG. *Spec-driven development with AI: Get started with a new open source toolkit*. Disponível em: https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/. Acesso em: 03 ago. 2026.
- THE BCMS. *Spec-Driven Development (SDD): The Definitive 2026 Guide*. Disponível em: https://www.thebcms.com/blog/spec-driven-development/. Acesso em: 03 ago. 2026.
- OSMANI, Addy. *How to write a good spec for AI agents*. Disponível em: https://addyosmani.com/blog/good-spec/. Acesso em: 03 ago. 2026.
- WIKIPEDIA. *Spec-driven development*. Disponível em: https://en.wikipedia.org/wiki/Spec-driven_development. Acesso em: 03 ago. 2026.
- SMARTDEV. *What is Agentic Engineering? Definition, How It Works & When*. Disponível em: https://smartdev.com/glossary-agentic-engineering/. Acesso em: 03 ago. 2026.
- IBM. *What is Agentic Engineering?*. Disponível em: https://www.ibm.com/think/topics/agentic-engineering. Acesso em: 03 ago. 2026.
- MINDSTUDIO. *What Is Agentic Engineering? The Shift Beyond Vibe Coding*. Disponível em: https://www.mindstudio.ai/blog/what-is-agentic-engineering. Acesso em: 03 ago. 2026.
- GLIDEAPPS. *Agentic Engineering Glossary: Understanding key terms and technologies in AI-assisted coding*. Disponível em: https://www.glideapps.com/blog/agentic-engineering-glossary. Acesso em: 03 ago. 2026.
- AIAGENTSSIMPLIFIED (SUBSTACK). *From Vibe Coding to Agentic Engineering: Andrej Karpathy's Vision for the Future of Software*. Disponível em: https://aiagentssimplified.substack.com/p/from-vibe-coding-to-agentic-engineering. Acesso em: 03 ago. 2026.
- FRANK'S WORLD. *Andrej Karpathy on the Evolution from Vibe Coding to Agentic Engineering*. Disponível em: https://www.franksworld.com/2026/05/01/andrej-karpathy-on-the-evolution-from-vibe-coding-to-agentic-engineering/. Acesso em: 03 ago. 2026.
- LITTLEX. *Software 3.0 — From Vibe Coding to Agentic Engineering: Karpathy's Software Revolution Manifesto*. Disponível em: https://littlex.org/en/research/sequoia-karpathy-software3-20260502/. Acesso em: 03 ago. 2026.
- DEALROOM.CO. *Vibe Coding Was Just the Warmup — Andrej Karpathy on the Dawn of Software 3.0*. Disponível em: https://app.dealroom.co/news/note/vibe-coding-was-just-the-warmup-andrej-karpathy-on-the-dawn-of-software-3-0. Acesso em: 03 ago. 2026.
- QVERIS. *Function Calling: OpenAI vs Anthropic vs Google (2026)*. Disponível em: https://qveris.ai/guides/function-calling/. Acesso em: 03 ago. 2026.
- SUHASBHAIRAV. *Structured Tool Invocation Across LLMs: OpenAI Function Calling vs Anthropic Tool Use*. Disponível em: https://suhasbhairav.com/blog/openai-function-calling-vs-anthropic-tool-use-structured-tool-invocation-across-llms. Acesso em: 03 ago. 2026.
- LATENODE. *LangGraph Multi-Agent Orchestration: Complete Framework Guide + Architecture Analysis 2025*. Disponível em: https://latenode.com/blog/ai-frameworks-technical-infrastructure/langgraph-multi-agent-orchestration/langgraph-multi-agent-orchestration-complete-framework-guide-architecture-analysis-2025. Acesso em: 03 ago. 2026.
- SINHA, Akanksha. *Agent Orchestration: When to Use LangChain, LangGraph, AutoGen — or Build an Agentic RAG System*. Disponível em: https://medium.com/@akankshasinha247/agent-orchestration-when-to-use-langchain-langgraph-autogen-or-build-an-agentic-rag-system-cc298f785ea4. Acesso em: 03 ago. 2026.
- WINDSURF. *Windsurf vs Cursor | AI IDE Comparison*. Disponível em: https://windsurf.com/compare/windsurf-vs-cursor. Acesso em: 03 ago. 2026.
- QODO. *Windsurf vs Cursor: Which AI IDE Tool is Better?*. Disponível em: https://www.qodo.ai/blog/windsurf-vs-cursor/. Acesso em: 03 ago. 2026.
- GETUNBLOCKED. *Cut AI Token Costs 50-90%: 7 Techniques*. Disponível em: https://getunblocked.com/blog/reduce-ai-token-costs/. Acesso em: 03 ago. 2026.
- MORPHLLM. *LLM Cost Optimization: 5 Levers to Cut API Spend 70-85%*. Disponível em: https://www.morphllm.com/llm-cost-optimization. Acesso em: 03 ago. 2026.
- TECHSY. *12 Ways to Reduce LLM API Costs by 80% (2026)*. Disponível em: https://techsy.io/en/blog/reduce-llm-api-costs-guide. Acesso em: 03 ago. 2026.
- NGROK. *Prompt caching: 10x cheaper LLM tokens, but how?*. Disponível em: https://ngrok.com/blog/prompt-caching. Acesso em: 03 ago. 2026.
- THE LOW END DISRUPTOR (MEDIUM). *LLM Context Engineering: a practical guide*. Disponível em: https://medium.com/the-low-end-disruptor/llm-context-engineering-a-practical-guide-248095d4bf71. Acesso em: 03 ago. 2026.
- BYTEBYTEGO. *A Guide to Context Engineering for LLMs*. Disponível em: https://blog.bytebytego.com/p/a-guide-to-context-engineering-for. Acesso em: 03 ago. 2026.
- GOOGLE CLOUD. *What is Retrieval-Augmented Generation (RAG)?*. Disponível em: https://cloud.google.com/use-cases/retrieval-augmented-generation. Acesso em: 03 ago. 2026.
- CONFLUENT. *What is Retrieval Augmented Generation (RAG)?*. Disponível em: https://www.confluent.io/learn/retrieval-augmented-generation-rag/. Acesso em: 03 ago. 2026.
- THE NEW STACK. *The Building Blocks of LLMs: Vectors, Tokens and Embeddings*. Disponível em: https://thenewstack.io/the-building-blocks-of-llms-vectors-tokens-and-embeddings/. Acesso em: 03 ago. 2026.
- DEMANDSPHERE. *SWE-bench Verified - AI Benchmark Explained*. Disponível em: https://www.demandsphere.com/research/demandsphere-radar/ai-frontier-model-tracker/benchmarks/swe-bench/. Acesso em: 03 ago. 2026.
- AI.GOOGLE.DEV. *Using the latest Gemini models*. Disponível em: https://ai.google.dev/gemini-api/docs/latest-model. Acesso em: 03 ago. 2026.
- OPENAI. *OpenAI API Platform Documentation*. Disponível em: https://developers.openai.com/api/docs. Acesso em: 03 ago. 2026.
- HUGGING FACE. *The Best Open Source and Open-Weight LLM Models to Run Locally in 2026*. Disponível em: https://huggingface.co/blog/daya-shankar/open-source-llm-models-to-run-locally. Acesso em: 03 ago. 2026.
- BETTER STACK. *Ollama: How to Run Any Open-Source LLM Locally with Your Existing Tools*. Disponível em: https://betterstack.com/community/guides/ai/ollama-local-llm/. Acesso em: 03 ago. 2026.
- RFC EDITOR. *RFC 9110: HTTP Semantics*. Disponível em: https://www.rfc-editor.org/rfc/rfc9110.html. Acesso em: 03 ago. 2026.
- HTTP WORKING GROUP. *HTTP Documentation*. Disponível em: https://httpwg.org/specs/. Acesso em: 03 ago. 2026.
- RFC EDITOR. *RFC 8446: The Transport Layer Security (TLS) Protocol Version 1.3*. Disponível em: https://datatracker.ietf.org/doc/html/rfc8446. Acesso em: 03 ago. 2026.
- THE SSL STORE. *TLS 1.3 is finally published by the IETF as RFC 8446*. Disponível em: https://www.thesslstore.com/blog/tls-1-3-approved/. Acesso em: 03 ago. 2026.
- LOGICMONITOR. *TLS 1.2 vs. 1.3—Handshake, Performance, and Other Improvements*. Disponível em: https://www.logicmonitor.com/deep-dive/http3-vs-http2/tls1-2-vs-1-3. Acesso em: 03 ago. 2026.
- RFC EDITOR. *RFC 6455: The WebSocket Protocol*. Disponível em: https://www.rfc-editor.org/info/rfc6455/. Acesso em: 03 ago. 2026.
- WEBSOCKET.ORG. *WebSocket Standards: RFC 6455, Extensions & Browser Support*. Disponível em: https://websocket.org/standards/. Acesso em: 03 ago. 2026.
- WEBSOCKET.ORG. *WebSocket Protocol: RFC 6455 Handshake, Frames & More*. Disponível em: https://websocket.org/guides/websocket-protocol/. Acesso em: 03 ago. 2026.
- CLOUDFLARE. *What is HTTP/3?*. Disponível em: https://www.cloudflare.com/learning/performance/what-is-http3/. Acesso em: 03 ago. 2026.
- CLOUDFLARE. *Comparing HTTP/3 vs. HTTP/2 Performance*. Disponível em: https://blog.cloudflare.com/http-3-vs-http-2/. Acesso em: 03 ago. 2026.
- CLOUDFLARE. *HTTP/3: From root to tip*. Disponível em: https://blog.cloudflare.com/http-3-from-root-to-tip/. Acesso em: 03 ago. 2026.
- CLOUDFLARE. *Content Delivery Network (CDN) Reference Architecture*. Disponível em: https://developers.cloudflare.com/reference-architecture/architectures/cdn/. Acesso em: 03 ago. 2026.
- FORTINET. *TCP/IP Model vs. OSI Model: Similarities and Differences*. Disponível em: https://www.fortinet.com/resources/cyberglossary/tcp-ip-model-vs-osi-model. Acesso em: 03 ago. 2026.
- A1 DIGITAL. *OSI and TCP/IP model: Differences explained*. Disponível em: https://www.a1.digital/knowledge-hub/osi-and-tcp-ip-model-differences-explained/. Acesso em: 03 ago. 2026.
- FREECODECAMP. *How DNS Works: A Guide to Understanding the Internet's Address Book*. Disponível em: https://www.freecodecamp.org/news/how-dns-works-the-internets-address-book/. Acesso em: 03 ago. 2026.
- NEW RELIC. *What Is DNS Resolution? How It Works & Best Practices*. Disponível em: https://newrelic.com/blog/apm/dns-resolution-a-comprehensive-guide. Acesso em: 03 ago. 2026.
- MDN WEB DOCS. *How the web works - Learn web development*. Disponível em: https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Web_standards/How_the_web_works. Acesso em: 03 ago. 2026.
- MDN WEB DOCS. *Overview of HTTP*. Disponível em: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview. Acesso em: 03 ago. 2026.
- MDN WEB DOCS. *Client-server overview - Learn web development*. Disponível em: https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/First_steps/Client-Server_overview. Acesso em: 03 ago. 2026.
- MDN WEB DOCS. *WebAssembly*. Disponível em: https://developer.mozilla.org/en-US/docs/WebAssembly. Acesso em: 03 ago. 2026.
- MDN WEB DOCS. *Structural overview of progressive web apps*. Disponível em: https://mdn2.netlify.app/en-us/docs/web/progressive_web_apps/structural_overview/. Acesso em: 03 ago. 2026.
- WEBASSEMBLY.ORG. *Use Cases*. Disponível em: https://webassembly.org/docs/use-cases/. Acesso em: 03 ago. 2026.
- GOOGLE FOR DEVELOPERS. *Progressive Web Apps: Service Worker Includes*. Disponível em: https://developers.google.com/codelabs/pwa-training/pwa06--service-worker-includes. Acesso em: 03 ago. 2026.
- PIXELFREESTUDIO. *The Role of SSR in Progressive Web Apps*. Disponível em: https://blog.pixelfreestudio.com/the-role-of-ssr-in-progressive-web-apps/. Acesso em: 03 ago. 2026.
- W3C. *WCAG 2 Overview*. Disponível em: https://www.w3.org/WAI/standards-guidelines/wcag/. Acesso em: 03 ago. 2026.
- W3C. *Web Content Accessibility Guidelines (WCAG) 2.2*. Disponível em: https://www.w3.org/TR/WCAG22/. Acesso em: 03 ago. 2026.
- REACT.DEV. *Quick Start*. Disponível em: https://react.dev/learn. Acesso em: 03 ago. 2026.
- MDN WEB DOCS. *Getting started with React*. Disponível em: https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Frameworks_libraries/React_getting_started. Acesso em: 03 ago. 2026.
- NEXT.JS DOCS. *App Router: Getting Started*. Disponível em: https://nextjs.org/docs/app/getting-started. Acesso em: 03 ago. 2026.
- ASCENDIENT LEARNING. *React vs. Angular vs. Vue: A Practical Comparison for 2026*. Disponível em: https://www.ascendientlearning.com/blog/comparing-angular-react-vue-svelte. Acesso em: 03 ago. 2026.
- PHAROS PRODUCTION. *Frontend Framework Comparison 2026*. Disponível em: https://pharosproduction.com/insights/engineering/frontend-framework-comparison-2026/. Acesso em: 03 ago. 2026.
- VITE.DEV. *Why Vite*. Disponível em: https://vite.dev/guide/why. Acesso em: 03 ago. 2026.
- LOGROCKET. *Vite vs. Webpack for react apps in 2025: A senior engineer's perspective*. Disponível em: https://blog.logrocket.com/vite-vs-webpack-react-apps-2025-senior-engineer/. Acesso em: 03 ago. 2026.
- TYPESCRIPT DOCS. *Handbook - The TypeScript Handbook*. Disponível em: https://www.typescriptlang.org/docs/handbook/intro.html. Acesso em: 03 ago. 2026.
- NODE.JS. *About this documentation*. Disponível em: https://nodejs.org/api/documentation.html. Acesso em: 03 ago. 2026.
- NODE.JS. *About Node.js*. Disponível em: https://nodejs.org/en/about. Acesso em: 03 ago. 2026.
- FASTAPI. *FastAPI*. Disponível em: https://fastapi.tiangolo.com/. Acesso em: 03 ago. 2026.
- REAL PYTHON. *Get Started With FastAPI*. Disponível em: https://realpython.com/get-started-with-fastapi/. Acesso em: 03 ago. 2026.
- SPRING. *Spring Boot Reference Documentation*. Disponível em: https://docs.spring.io/spring-boot/docs/current/reference/html/documentation.html. Acesso em: 03 ago. 2026.
- GO.DEV. *Documentation - The Go Programming Language*. Disponível em: https://go.dev/doc/. Acesso em: 03 ago. 2026.
- POSTGRESQL GLOBAL DEVELOPMENT GROUP. *PostgreSQL: Documentation*. Disponível em: https://www.postgresql.org/docs/. Acesso em: 03 ago. 2026.
- MONGODB. *ACID Transactions in DBMS Explained*. Disponível em: https://www.mongodb.com/resources/basics/databases/acid-transactions. Acesso em: 03 ago. 2026.
- MONGODB. *MongoDB vs. Redis Comparison: Pros and Cons*. Disponível em: https://www.mongodb.com/resources/compare/mongodb-vs-redis. Acesso em: 03 ago. 2026.
- AWS. *Redis OSS vs MongoDB - Difference Between NoSQL Databases*. Disponível em: https://aws.amazon.com/compare/the-difference-between-redis-and-mongodb/. Acesso em: 03 ago. 2026.
- MOTHERDUCK. *ACID Transactions Explained: Atomicity, Consistency, Isolation & Durability*. Disponível em: https://motherduck.com/learn/acid-transactions-sql/. Acesso em: 03 ago. 2026.
- DIGITALOCEAN. *Database Normalization: 1NF, 2NF, 3NF & BCNF Examples*. Disponível em: https://www.digitalocean.com/community/tutorials/database-normalization. Acesso em: 03 ago. 2026.
- IBM. *What Is Database Normalization?*. Disponível em: https://www.ibm.com/think/topics/database-normalization. Acesso em: 03 ago. 2026.
- PINGCAP. *Understanding the CAP Theorem in Distributed Systems*. Disponível em: https://www.pingcap.com/article/understanding-cap-theorem-basics-in-distributed-systems/. Acesso em: 03 ago. 2026.
- OLEB.NET. *Roy Fielding's REST dissertation*. Disponível em: https://oleb.net/2018/rest/. Acesso em: 03 ago. 2026.
- RESTFULAPI.NET. *REST API Best Practices*. Disponível em: https://restfulapi.net/rest-api-best-practices/. Acesso em: 03 ago. 2026.
- GRAPHQL FOUNDATION. *GraphQL | The query language for modern APIs*. Disponível em: https://graphql.org/. Acesso em: 03 ago. 2026.
- GRAPHQL FOUNDATION. *GraphQL Specification*. Disponível em: https://spec.graphql.org/October2021/. Acesso em: 03 ago. 2026.
- GRPC AUTHORS. *Introduction to gRPC*. Disponível em: https://grpc.io/docs/what-is-grpc/introduction/. Acesso em: 03 ago. 2026.
- PROTOCOL BUFFERS. *Overview*. Disponível em: https://protobuf.dev/overview/. Acesso em: 03 ago. 2026.
- SWAGGER (SMARTBEAR). *OpenAPI Specification - Version 3.1.0*. Disponível em: https://swagger.io/specification/. Acesso em: 03 ago. 2026.
- SWAGGER (SMARTBEAR). *What Is OpenAPI?*. Disponível em: https://swagger.io/docs/specification/v3_0/about/. Acesso em: 03 ago. 2026.
- OWASP FOUNDATION. *OWASP Top Ten Web Application Security Risks*. Disponível em: https://owasp.org/www-project-top-ten/. Acesso em: 03 ago. 2026.
- CONNECT2ID. *OpenID Connect explained*. Disponível em: https://connect2id.com/learn/openid-connect. Acesso em: 03 ago. 2026.
- KINDE. *Guide to Bcrypt Hashing*. Disponível em: https://www.kinde.com/learn/authentication/passwords/bcrypt-hashing-guide/. Acesso em: 03 ago. 2026.
- MEDIUM (GOALIST BLOG). *Three Layer Architecture in Backend Development*. Disponível em: https://medium.com/goalist-blog/three-layer-architecture-in-backend-development-c3e52c0d6682. Acesso em: 03 ago. 2026.
- WEWEB DOCS. *APIs and databases: the critical connection*. Disponível em: https://docs.weweb.io/web-development-basics/apis-and-databases.html. Acesso em: 03 ago. 2026.
- WIKIPEDIA. *Hexagonal architecture (software)*. Disponível em: https://en.wikipedia.org/wiki/Hexagonal_architecture_(software). Acesso em: 03 ago. 2026.
- DEV.TO (NIBER, Dyarle). *Hexagonal Architecture and Clean Architecture (with examples)*. Disponível em: https://dev.to/dyarleniber/hexagonal-architecture-and-clean-architecture-with-examples-48oi. Acesso em: 03 ago. 2026.
- PRECISIONAIACADEMY. *Software Architecture Patterns in 2026: MVC, MVVM, Clean Architecture, and More*. Disponível em: https://precisionaiacademy.com/blog/software-architecture-patterns-guide. Acesso em: 03 ago. 2026.
- DESIGNGURUS. *Monolithic vs Microservices vs SOA – Architecture Comparison Guide*. Disponível em: https://www.designgurus.io/blog/monolithic-service-oriented-microservice-architecture. Acesso em: 03 ago. 2026.
- EQUAL EXPERTS. *Understanding event-driven architecture and microservices in comparison to a monolith*. Disponível em: https://www.equalexperts.com/blog/our-thinking/understanding-event-driven-architecture-and-microservices-in-comparison-to-a-monolith/. Acesso em: 03 ago. 2026.
- KUBESIMPLIFY. *Event-Driven Architecture Simplified: Monolith to Microservices*. Disponível em: https://blog.kubesimplify.com/event-driven-architecture-simplified-monolith-to-microservices. Acesso em: 03 ago. 2026.
- REDPANDA. *RabbitMQ vs. Kafka*. Disponível em: https://www.redpanda.com/guides/kafka-tutorial-rabbitmq-vs-kafka. Acesso em: 03 ago. 2026.
- BAELDUNG. *Pub-Sub vs. Message Queues*. Disponível em: https://www.baeldung.com/pub-sub-vs-message-queues. Acesso em: 03 ago. 2026.
- DIGITALOCEAN. *Gang of Four (GoF) Design Patterns Explained: Creational, Structural, and Behavioral*. Disponível em: https://www.digitalocean.com/community/tutorials/gangs-of-four-gof-design-patterns. Acesso em: 03 ago. 2026.
- LAWS OF SOFTWARE ENGINEERING. *SOLID Principles*. Disponível em: https://lawsofsoftwareengineering.com/laws/solid-principles/. Acesso em: 03 ago. 2026.
- AWS. *Applying the Twelve-Factor App Methodology to Serverless Applications*. Disponível em: https://aws.amazon.com/blogs/compute/applying-the-twelve-factor-app-methodology-to-serverless-applications/. Acesso em: 03 ago. 2026.
- QASE. *The test pyramid: A complete guide*. Disponível em: https://www.qase.io/blog/test-pyramid/. Acesso em: 03 ago. 2026.
- MOMENTIC. *The Software Testing Pyramid: Unit, Integration, and E2E Testing Explained*. Disponível em: https://momentic.ai/blog/software-testing-pyramid-guide. Acesso em: 03 ago. 2026.
- ATLASSIAN. *A Guide to Optimal Branching Strategies in Git*. Disponível em: https://www.atlassian.com/agile/software-development/branching. Acesso em: 03 ago. 2026.
- GITHUB DOCS. *Quickstart for GitHub Actions*. Disponível em: https://docs.github.com/en/actions/get-started/quickstart. Acesso em: 03 ago. 2026.
- DOCKER. *Building best practices*. Disponível em: https://docs.docker.com/build/building/best-practices/. Acesso em: 03 ago. 2026.
- BETTER STACK. *Docker Security: 14 Best Practices You Should Know*. Disponível em: https://betterstack.com/community/guides/scaling-docker/docker-security-best-practices/. Acesso em: 03 ago. 2026.
- DEVTRON.AI. *CI/CD Pipeline for Kubernetes: The Ultimate Guide*. Disponível em: https://devtron.ai/blog/ci-cd-pipeline-for-kubernetes/. Acesso em: 03 ago. 2026.
- HASHICORP DEVELOPER. *What is Infrastructure as Code with Terraform?*. Disponível em: https://developer.hashicorp.com/terraform/tutorials/aws-get-started/infrastructure-as-code. Acesso em: 03 ago. 2026.
- ISTIO. *Istio / Gateway*. Disponível em: https://istio.io/latest/docs/reference/config/networking/gateway/. Acesso em: 03 ago. 2026.
- GRAFANA LABS. *What is Prometheus?*. Disponível em: https://grafana.com/docs/grafana/latest/fundamentals/intro-to-prometheus/. Acesso em: 03 ago. 2026.
- GRAFANA LABS. *Get started with Grafana and Prometheus*. Disponível em: https://grafana.com/docs/grafana/latest/fundamentals/getting-started/first-dashboards/get-started-grafana-prometheus/. Acesso em: 03 ago. 2026.
- GETPANTO. *GitHub Copilot Statistics 2026 — Users, Revenue & Adoption*. Disponível em: https://www.getpanto.ai/blog/github-copilot-statistics. Acesso em: 03 ago. 2026.
- GITHUB. *Introducing GitHub Copilot: your AI pair programmer*. Disponível em: https://github.blog/news-insights/product-news/introducing-github-copilot-ai-pair-programmer/. Acesso em: 03 ago. 2026.
- STACKSHARE. *npm vs pip | What are the differences?*. Disponível em: https://stackshare.io/stackups/npm-vs-pip. Acesso em: 03 ago. 2026.

### Fontes brutas — complemento (rodada 2: segurança aprofundada, LLMs, meta-harness, dados avançados)

- IBM. *What is Asymmetric Encryption?*. Disponível em: https://www.ibm.com/think/topics/asymmetric-encryption. Acesso em: 03 ago. 2026.
- DESTCERT. *Asymmetric Cryptography: RSA, ECC & PKI Explained*. Disponível em: https://destcert.com/resources/asymmetric-cryptography/. Acesso em: 03 ago. 2026.
- OWASP FOUNDATION. *Certificate and Public Key Pinning*. Disponível em: https://owasp.org/www-community/controls/Certificate_and_Public_Key_Pinning. Acesso em: 03 ago. 2026.
- SSL.COM. *What Is Certificate Pinning?*. Disponível em: https://www.ssl.com/blogs/what-is-certificate-pinning/. Acesso em: 03 ago. 2026.
- PALO ALTO NETWORKS. *What Is Certificate Pinning? Benefits, Risks & Best Practices*. Disponível em: https://www.paloaltonetworks.com/cyberpedia/what-is-certificate-pinning. Acesso em: 03 ago. 2026.
- MDN WEB DOCS. *Cross-Origin Resource Sharing (CORS)*. Disponível em: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS. Acesso em: 03 ago. 2026.
- PORTSWIGGER. *What is CORS (cross-origin resource sharing)? Tutorial & Examples*. Disponível em: https://portswigger.net/web-security/cors. Acesso em: 03 ago. 2026.
- OWASP FOUNDATION. *A05:2021 – Security Misconfiguration*. Disponível em: https://owasp.org/Top10/2021/A05_2021-Security_Misconfiguration/. Acesso em: 03 ago. 2026.
- OWASP FOUNDATION. *Cross Site Request Forgery (CSRF)*. Disponível em: https://owasp.org/www-community/attacks/csrf. Acesso em: 03 ago. 2026.
- OWASP CHEAT SHEET SERIES. *Cross-Site Request Forgery Prevention Cheat Sheet*. Disponível em: https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html. Acesso em: 03 ago. 2026.
- OWASP FOUNDATION. *Cross Site Scripting (XSS)*. Disponível em: https://owasp.org/www-community/attacks/xss/. Acesso em: 03 ago. 2026.
- OWASP FOUNDATION. *Types of XSS*. Disponível em: https://owasp.org/www-community/Types_of_Cross-Site_Scripting. Acesso em: 03 ago. 2026.
- IMPERVA. *What is Penetration Testing | Step-By-Step Process & Methods*. Disponível em: https://www.imperva.com/learn/application-security/penetration-testing/. Acesso em: 03 ago. 2026.
- EC-COUNCIL. *5 Penetration Testing Phases: Key Steps, Tools & Benefits*. Disponível em: https://www.eccouncil.org/cybersecurity-exchange/penetration-testing/penetration-testing-phases/. Acesso em: 03 ago. 2026.
- MICROSOFT LEARN. *Event Sourcing pattern*. Disponível em: https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing. Acesso em: 03 ago. 2026.
- MICROSOFT LEARN. *CQRS Pattern*. Disponível em: https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs. Acesso em: 03 ago. 2026.
- MICROSERVICES.IO. *Pattern: Event sourcing*. Disponível em: https://microservices.io/patterns/data/event-sourcing.html. Acesso em: 03 ago. 2026.
- PUBNUB. *What is WebRTC (Peer-to-Peer Technology)*. Disponível em: https://www.pubnub.com/blog/what-is-webrtc/. Acesso em: 03 ago. 2026.
- ABLY. *What is WebRTC? (Explanation, use cases, and features)*. Disponível em: https://ably.com/blog/what-is-webrtc. Acesso em: 03 ago. 2026.
- LAUNCHDARKLY. *Feature Flags 101: Use Cases, Benefits, and Best Practices*. Disponível em: https://launchdarkly.com/blog/what-are-feature-flags/. Acesso em: 03 ago. 2026.
- LAUNCHDARKLY. *7 Feature Flag Best Practices for Short-Term and Permanent Flags*. Disponível em: https://launchdarkly.com/blog/best-practices-short-term-permanent-flags/. Acesso em: 03 ago. 2026.
- GEEKSFORGEEKS. *CDN Vs Edge Server - System Design*. Disponível em: https://www.geeksforgeeks.org/system-design/cdn-vs-edge-server-system-design/. Acesso em: 03 ago. 2026.
- FASTPIX. *Edge Computing vs. CDN: Identifying Their Roles in Data Delivery*. Disponível em: https://www.fastpix.io/blog/edge-computing-vs-cdn-identifying-their-roles-in-data-delivery. Acesso em: 03 ago. 2026.
- CLAUDE PLATFORM DOCS. *Pricing*. Disponível em: https://platform.claude.com/docs/en/about-claude/pricing. Acesso em: 03 ago. 2026.
- OPENAI. *Pricing*. Disponível em: https://developers.openai.com/api/docs/pricing. Acesso em: 03 ago. 2026.
- OPENAI. *Models*. Disponível em: https://developers.openai.com/api/docs/models. Acesso em: 03 ago. 2026.
- GOOGLE AI FOR DEVELOPERS. *Gemini models*. Disponível em: https://ai.google.dev/gemini-api/docs/models. Acesso em: 03 ago. 2026.
- GOOGLE AI FOR DEVELOPERS. *Gemini API Pricing*. Disponível em: https://ai.google.dev/gemini-api/docs/pricing. Acesso em: 03 ago. 2026.
- GOOGLE DEEPMIND. *Gemini 3 Pro Model Card*. Disponível em: https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-Pro-Model-Card.pdf. Acesso em: 03 ago. 2026.
- OPENAI. *Agents SDK*. Disponível em: https://developers.openai.com/api/docs/guides/agents. Acesso em: 03 ago. 2026.
- OPENAI. *openai-agents-python*. Disponível em: https://github.com/openai/openai-agents-python. Acesso em: 03 ago. 2026.
- GOOGLE. *Agent Development Kit (ADK) - Technical Overview*. Disponível em: https://google.github.io/adk-docs/get-started/about/. Acesso em: 03 ago. 2026.
- MICROSOFT. *autogen: A programming framework for agentic AI*. Disponível em: https://github.com/microsoft/autogen. Acesso em: 03 ago. 2026.

