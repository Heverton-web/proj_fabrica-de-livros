# Dossiê Técnico — Livro 8: Spec-Driven Development: da intenção ao código verificável

> Dossiê bruto de pesquisa (Nó 0A) — fontes primárias em formato ABNT para
> reaproveitamento direto nas referências dos capítulos. O RAG local indexa
> este arquivo em blocos (TF-IDF) — consulte por `--buscar`, nunca carregue
> o arquivo inteiro no contexto.

## 1. Tema e recorte

- **Tema:** Spec-Driven Development (SDD) — a especificação como artefato primário
  que orienta, valida e documenta a implementação de código, do legado formal
  (Design by Contract, métodos formais) ao BDD/ATDD e à nova onda de SDD agêntico
  (specs como contratos entre humano e agente de IA).
- **Metáfora-mestra (motivo condutor):** a especificação como **planta de engenharia /
  contrato de construção** — nenhuma obra começa sem projeto aprovado; a verificação
  é o "habite-se" que atesta que o edifício cumpre a planta.
- **Persona do leitor:** Engenheiro de Software / Tech Lead que quer transformar
  intenção em código verificável, com ou sem agentes de IA.
- **Fontes coletadas:** 4 frentes de pesquisa (metodologia clássica, ferramentas,
  SDD agêntico, teoria/história) — 30+ fontes primárias.

## 2. Frente 1 — Metodologia: SDD, BDD, ATDD e Specification by Example

### 2.1 Dan North — origem do BDD e o ensaio clássico

- **Fato:** Dan North criou o Behavior-Driven Development (c. 2003-2006), o JBehave
  (2004) e cunhou com Chris Matts o formato Given-When-Then. O ensaio "BDD is like
  TDD if..." argumenta que o TDD clássico funciona quando a equipe é só de
  programadores; com múltiplos stakeholders (analistas, testadores, especialistas),
  é preciso unificar a linguagem — origem da comunicação por comportamento.
- **Referência ABNT (bruta):** NORTH, Dan. *BDD is like TDD if...*. Dan North &
  Associates, 2006. Disponível em: https://dannorth.net/blog/bdd-is-like-tdd-if/
  Acesso em: 5 ago. 2026.
- **Pontos para o capítulo:** a troca da palavra "teste" por "comportamento";
  o público-alvo multidisciplinar; o problema que o BDD resolve é de comunicação,
  não de técnica.

### 2.2 Liz Keogh — histórico de ATDD vs BDD e conexão com DDD

- **Fato:** Liz Keogh, co-criadora do JBehave, documentou a história de ATDD vs BDD
  e conecta BDD ao Domain-Driven Design (ubiquitous language) e ao framework Cynefin
  para lidar com incerteza na especificação.
- **Referência ABNT (bruta):** KEOGH, Liz. *ATDD vs. BDD, and a potted history of
  some related stuff*. Liz Keogh's blog, 2011. Disponível em:
  https://lizkeogh.com/2011/06/27/atdd-vs-bdd-and-a-potted-history-of-some-related-stuff/
  Acesso em: 5 ago. 2026.
- **Referência ABNT (bruta):** KEOGH, Liz. *Behaviour Driven Development*. Disponível
  em: https://lizkeogh.com/behaviour-driven-development/ Acesso em: 5 ago. 2026.
- **Pontos para o capítulo:** ATDD foca em critérios de aceitação; BDD foca em
  comportamento e linguagem ubíqua; Cynefin como lente para saber QUANDO especificar
  a priori (domínio complicado) vs explorar (complexo).

### 2.3 Gojko Adzic — Specification by Example e Living Documentation

- **Fato:** O livro "Specification by Example" (2011) sintetiza estudos de caso de
  equipes de alta performance. Conceitos-chave: exemplares (exemplars), especificação
  executável, documentação viva (living documentation) — a spec nunca desatualiza
  porque, se o comportamento muda, o teste quebra. Pesquisa de adoção: o formato
  Given-When-Then é usado por mais de 70% das equipes que adotam especificação por
  exemplos.
- **Referência ABNT (bruta):** ADZIC, Gojko. *Specification by Example: How Successful
  Teams Deliver the Right Software*. Shelter Island: Manning Publications, 2011.
- **Referência ABNT (bruta):** ADZIC, Gojko. *Specification by Example, 10 years later*.
  Gojko.net, 2020. Disponível em: https://gojko.net/2020/03/17/sbe-10-years.html
  Acesso em: 5 ago. 2026.
- **Referência ABNT (bruta):** ADZIC, Gojko. *Living Documentation: Continuous Knowledge
  Sharing by Design*. Boston: Addison-Wesley, 2017.
- **Pontos para o capítulo:** o pipeline "descoberta colaborativa → captura de
  exemplos → especificação executável → automação red-green-refactor → verificação
  contínua"; a documentação viva como anti-podre.

### 2.4 Quadro comparativo TDD vs BDD/SDD (extraído das fontes)

| Dimensão | TDD clássico | SDD/BDD/ATDD |
|---|---|---|
| Público | Desenvolvedores | Equipe multidisciplinar (PO, QA, Devs) |
| Foco | Unidade/módulo, design interno | Comportamento, valor de negócio, linguagem ubíqua |
| Vocabulário | assertNull, assertEquals | Given/When/Then, cenários legíveis |
| Origem do artefato | Programador | Conversas colaborativas antes do código |

### 2.5 Gherkin — gramática formal

- **Fato:** Gherkin formaliza a especificação com as palavras-chave Given (contexto),
  When (ação), Then (resultado observável) + And/But/Background/Scenario Outline/
  Examples para parametrização.
- **Referência ABNT (bruta):** CUCUMBER. *Gherkin Reference*. Cucumber Documentation.
  Disponível em: https://cucumber.io/docs/gherkin/reference/ Acesso em: 5 ago. 2026.

## 3. Frente 2 — Ferramentas de especificação executável e contract testing

### 3.1 BDD / Specification by Example (ferramentas)

- **Cucumber** — BDD mais popular, Gherkin em arquivos `.feature`, step definitions
  em várias linguagens. URL: https://cucumber.io/
  Referência ABNT (bruta): CUCUMBER. *Cucumber — BDD Tool*. Disponível em:
  https://cucumber.io/ Acesso em: 5 ago. 2026.
- **SpecFlow / Reqnroll** — padrão .NET; a comunidade migrou para Reqnroll (open
  source) após mudança de licença. URLs: https://reqnroll.net/ e https://specflow.org/
  Referência ABNT (bruta): REQNROLL. *Reqnroll — SpecFlow-compatible BDD for .NET*.
  Disponível em: https://reqnroll.net/ Acesso em: 5 ago. 2026.
- **Gauge** — ThoughtWorks; specs em Markdown, paralelização nativa, multi-linguagem.
  URL: https://www.gauge.org/
  Referência ABNT (bruta): GAUGE. *Gauge — Lightweight cross-platform test automation*.
  Disponível em: https://www.gauge.org/ Acesso em: 5 ago. 2026.
- **Concordion** — Specification by Example em HTML para Java/.NET; documentação viva
  rica. URL: https://concordion.org/
  Referência ABNT (bruta): CONCORDION. *Concordion — Executable Specifications*.
  Disponível em: https://concordion.org/ Acesso em: 5 ago. 2026.
- **FitNesse** — wiki servidora de teste de aceitação; tabelas executáveis. URL:
  https://fitnesse.org/
  Referência ABNT (bruta): FIXTNESS (sic). *FitNesse — Acceptance testing wiki*.
  Disponível em: https://fitnesse.org/ Acesso em: 5 ago. 2026.
- **JGiven** — BDD para Java com API fluente no próprio código, sem arquivos Gherkin.
  URL: https://jgiven.org/
  Referência ABNT (bruta): JGVEN (sic). *JGiven — BDD in plain Java*. Disponível em:
  https://jgiven.org/ Acesso em: 5 ago. 2026.

### 3.2 Contract testing e schema-first

- **Pact** — consumer-driven contract testing; o consumidor define expectativas,
  gera pacto JSON que o provedor valida. URL: https://docs.pact.io/
  Referência ABNT (bruta): PACT. *Pact — Consumer-Driven Contract Testing*.
  Disponível em: https://docs.pact.io/ Acesso em: 5 ago. 2026.
- **Spring Cloud Contract** — contratos YAML/Groovy gerando stubs automáticos na JVM.
  URL: https://spring.io/projects/spring-cloud-contract
  Referência ABNT (bruta): SPRING. *Spring Cloud Contract*. Disponível em:
  https://spring.io/projects/spring-cloud-contract Acesso em: 5 ago. 2026.
- **OpenAPI/Swagger** — padrão-ouro para especificação REST; schema-first design.
  URLs: https://www.openapis.org/ e https://swagger.io/
  Referência ABNT (bruta): OPENAPI INITIATIVE. *OpenAPI Specification*. Disponível em:
  https://www.openapis.org/ Acesso em: 5 ago. 2026.
- **JSON Schema** — vocabulário de validação estrutural de payloads JSON. URL:
  https://json-schema.org/
  Referência ABNT (bruta): JSON SCHEMA. *JSON Schema — A Media Type for Describing JSON
  Documents*. Disponível em: https://json-schema.org/ Acesso em: 5 ago. 2026.
- **Apache Avro** — serialização com esquemas JSON, evolução de schema (Kafka). URL:
  https://avro.apache.org/
  Referência ABNT (bruta): APACHE AVRO. *Apache Avro*. Disponível em:
  https://avro.apache.org/ Acesso em: 5 ago. 2026.
- **Protocol Buffers / gRPC** — contratos `.proto` independentes de linguagem; RPC de
  alta performance. URL: https://protobuf.dev/
  Referência ABNT (bruta): GOOGLE. *Protocol Buffers Documentation*. Disponível em:
  https://protobuf.dev/ Acesso em: 5 ago. 2026.

### 3.3 Design by Contract, lógica de Hoare e verificação formal

- **Design by Contract (DbC)** — Bertrand Meyer, linguagem Eiffel: pré-condições,
  pós-condições e invariantes como contratos formais entre chamador e rotina. URL:
  https://www.eiffel.org/doc/solutions/design_by_contract
  Referência ABNT (bruta): MEYER, Bertrand. *Object-Oriented Software Construction*.
  2. ed. Upper Saddle River: Prentice Hall, 1997.
- **Lógica de Hoare** — triplos {P} C {Q}; base para verificação moderna. URL:
  https://plato.stanford.edu/entries/hoare-logic/
  Referência ABNT (bruta): HOARE, C. A. R. An Axiomatic Basis for Computer Programming.
  Communications of the ACM, v. 12, n. 10, p. 576-580, 1969.
- **TLA+** — Leslie Lamport; modelagem de sistemas concorrentes/distribuídos; usada na
  AWS e Microsoft. URL: https://lamport.azurewebsites.net/tla/tla.html
  Referência ABNT (bruta): LAMPORT, Leslie. *Specifying Systems: The TLA+ Language and
  Tools for Hardware and Software Engineers*. Boston: Addison-Wesley, 2002.
- **Alloy** — lógica relacional de primeira ordem + analyzer (MIT). URL:
  https://alloytools.org/
  Referência ABNT (bruta): JACKSON, Daniel. *Software Abstractions: Logic, Language, and
  Analysis*. Cambridge: MIT Press, 2006.
- **Dafny** — linguagem com verificação formal integrada (prover Z3). URL:
  https://dafny.org/
  Referência ABNT (bruta): LEINO, K. Rustan M. *Dafny: An Automatic Program Verifier for
  Functional Correctness*. In: LPAR-16, 2010.

## 4. Frente 3 — SDD agêntico (specs como contrato humano ↔ agente de IA)

### 4.1 Conceito e níveis de SDD (Fowler/Thoughtworks)

- **Fato:** Martin Fowler distingue três níveis de SDD com IA: (1) **Spec-First** —
  a spec orienta a tarefa atual do agente; (2) **Spec-Anchored** — a spec vive no
  repositório guiando evolução contínua; (3) **Spec-As-Source** — a spec é o artefato
  primário editável por humanos e o código é gerado automaticamente (sem humanos
  editando código).
- **Referência ABNT (bruta):** FOWLER, Martin. *Understanding Spec-Driven Development*
  (Exploring Gen AI — SDD tools). Martin Fowler, 2025. Disponível em:
  https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
  Acesso em: 5 ago. 2026.

### 4.2 Os 6 elementos de uma spec para agentes de IA

1. **Outcomes** — o que o sistema deve fazer ao final (foco em valor/comportamento);
2. **Fronteiras (in-scope/out-of-scope)** — o que NÃO deve ser feito;
3. **Restrições e premissas** — stack, versões, limites de APIs;
4. **Decisões já tomadas** — arquitetura pré-aprovada, schemas;
5. **Task breakdown** — decomposição em subtarefas atômicas paralelizáveis;
6. **Critérios de verificação** — cenários de teste/condições de sucesso validados por
   agente verificador ou CI.
- **Referência ABNT (bruta):** AUGMENT CODE. *What is Spec-Driven Development?* Augment
  Code Guides. Disponível em: https://www.augmentcode.com/guides/what-is-spec-driven-development
  Acesso em: 5 ago. 2026.

### 4.3 Ferramentas do ecossistema agêntico

- **GitHub Spec Kit** — CLI com comandos `/speckit.specify`, `/speckit.plan`,
  `/speckit.tasks`, `/speckit.implement`; usa `constitution.md` como regras imutáveis.
  URL: https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
  Referência ABNT (bruta): GITHUB. *Spec-Driven Development with AI — get started with
  a new open source toolkit*. GitHub Blog, 2025. Disponível em: URL acima.
  Acesso em: 5 ago. 2026.
- **Kiro** — IDE baseada em VS Code: fluxo Requirements (User Stories + Gherkin GWT) →
  Design → Tasks.
- **Tessl** — framework spec-anchored/spec-as-source; engenharia reversa de código
  para spec; validação de contratos de componentes.
- **Addy Osmani** — guia de escrita de specs enxutas para agentes de IA; estrutura
  inspirada em PRD; uso de Plan Mode.
  Referência ABNT (bruta): OSMANI, Addy. *How to Write a Good Spec for AI Agents*.
  Addy Osmani's blog, 2025. Disponível em: https://addyosmani.com/blog/good-spec/
  Acesso em: 5 ago. 2026.

### 4.4 Padrão de agente adversarial (Coordinator/Implementor/Verifier)

- **Fato:** padrão de três papéis — Coordinator analisa a spec e divide o trabalho;
  Implementor escreve código e testes; Verifier (modelo mais barato/rápido) audita o
  código gerado contra a spec original, caçando desvios (drift) e falhas lógicas.
- **Relação com a esteira da Fábrica:** o mesmo padrão do squad da Fábrica Agêntica
  (orquestrador → subagente-redator → revisor/auditor) — o Livro 8 pode citar a
  arquitetura local como estudo de caso.

## 5. Frente 4 — Teoria e história: de VDM/Z a DDD e event storming

- **Fatos:** métodos formais dos anos 1960-70 (VDM, Notação Z, programação estruturada
  de Dijkstra) são a pré-história do SDD. Eric Evans formalizou a ubiquitous language
  e o Domain-Driven Design (2003). Event storming (Alberto Brandolini) é a técnica de
  descoberta colaborativa que alimenta especificações. Acceptance criteria derivam de
  user stories INVEST e do Definition of Done (Scrum).
- **Referências ABNT (brutas):**
  - EVANS, Eric. *Domain-Driven Design: Tackling Complexity in the Heart of Software*.
    Boston: Addison-Wesley, 2003.
  - BRANDOLINI, Alberto. *Introducing EventStorming*. Leanpub, 2014.
  - BECK, Kent. *Test-Driven Development: By Example*. Boston: Addison-Wesley, 2002.
  - MARTIN, Robert C. *Agile Software Development: Principles, Patterns, and Practices*.
    Upper Saddle River: Prentice Hall, 2002.
  - DIJKSTRA, Edsger W. *A Discipline of Programming*. Englewood Cliffs: Prentice Hall,
    1976.
  - SCHWABER, Ken; SUTHERLAND, Jeff. *The Scrum Guide* (Definition of Done). 2020.
    Disponível em: https://scrumguides.org/ Acesso em: 5 ago. 2026.

## 6. Linha do tempo consolidada (para o capítulo de história)

- 1960-70 — VDM, Notação Z, programação estruturada (Dijkstra).
- 1969 — Lógica de Hoare (prova axiomática de corretude).
- 1986-97 — Design by Contract (Bertrand Meyer, Eiffel); método formal TLA+ (Lamport,
  publicado em livro 2002).
- 2000-02 — TDD de Kent Beck; DDD de Eric Evans.
- 2003-06 — BDD de Dan North; JBehave; Given-When-Then com Chris Matts; ensaio
  "BDD is like TDD if...".
- 2004 — FitNesse (teste de aceitação wiki); JBehave 1.0.
- 2006-08 — Cucumber (Ruby), ATDD consolidado; Specification by Example popularizado.
- 2011 — Livro Specification by Example (Adzic); Alloy (Jackson).
- 2014 — Event Storming (Brandolini); Pact (contract testing).
- 2017 — Living Documentation (Adzic).
- 2023-26 — SDD agêntico: SPEC.md como contrato humano↔agente; GitHub Spec Kit, Kiro,
  Tessl; níveis spec-first/spec-anchored/spec-as-source (Fowler); padrão
  Coordinator/Implementor/Verifier.

## 7. Estudos de caso e referências de apoio (para Aplica)

- **AWS e TLA+:** Newcombe et al. *How Amazon Web Services Uses Formal Methods*.
  Communications of the ACM, v. 58, n. 4, p. 66-73, 2015.
- **Specification by Example em escala:** Adzic 2011 (34 equipes estudadas).
- **Mutation testing para validar specs:** OFFSETT, Jeff. *Mutation Testing for the New
  Century*. Norwell: Kluwer, 2001.
- **Fábrica Agêntica local (estudo de caso):** SPEC.md/SPEC_TCC.md/SPEC_ARTIGO.md/
  SPEC_EBOOK.md como contratos de manufatura; auditar-obra.py como verificador
  determinístico (fonte primária interna).

## 8. Notas de uso para os capítulos (EITA-V2)

- Cada capítulo DEVE citar ≥ 20 fontes distintas (mín. configurado) com rastreabilidade
  `[N]` ligada à seção Referências do capítulo.
- As referências acima já estão em formato bruto ABNT — o redator pode compor a lista
  final do capítulo a partir delas sem reescrever.
- Diagrama Mermaid obrigatório na seção Ilustra (ex.: fluxo "intenção → spec →
  testes → código → verificação"; mapa de níveis spec-first/anchored/source).
- Blocos de código validáveis na seção Técnica (Gherkin, YAML de contract, TLA+,
  Dafny, JSON Schema, protobuf).
