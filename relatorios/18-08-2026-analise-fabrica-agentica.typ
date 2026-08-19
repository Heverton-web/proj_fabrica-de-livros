// Template ABNT para Livros - Fabrica Agentica de Livros
// Compativel com Pandoc + Typst (testado em typst 0.15 / pandoc 3.10)
//
// Variaveis Pandoc suportadas (-V chave=valor):
//   title, subtitle, author            -> capa, folha de rosto e cabecalho
//   cor_acento                         -> hex (#rrggbb) da cor de accent da obra/serie,
//                                          mesma da capa grafica (scripts/series_capa.py)
//   cip_sobrenome, cip_nome            -> ficha catalografica (autoria invertida)
//   cip_cutter, cip_ano, cip_paginas   -> ficha catalografica
//   cip_palavras, cip_cdd, cip_isbn    -> ficha catalografica
//   cip_local, cip_editora             -> imprenta da folha de rosto e da CIP
//   sinopse                            -> texto da contracapa
//   capa_imagem                        -> PNG full-bleed como pagina-capa (padrao da serie)
//   sem_capa_grafica                   -> "1" desativa capa/contracapa graficas

#set document(
  title: "Análise da Fábrica Agêntica",
  author: "Heverton Eduardo Peres",
  date: datetime.today(),
)

// ── Cor cromatica da obra (derivada da mesma cor de accent da capa —
// REGRA 5 / scripts/series_capa.py — nunca mais uma paleta fixa isolada) ──
#let cor-acento-str = "#1e3a5c"
#let cor-acento = if cor-acento-str == "" { rgb("#58a6ff") } else { rgb(cor-acento-str) }
#let cor = (
  primaria: cor-acento.darken(55%),
  secundaria: cor-acento.darken(20%),
  destaque: cor-acento,
  clara: cor-acento.lighten(88%),
)

// ── Pagina, tipografia e paragrafos (ABNT) ────────────────────────
#set page(
  paper: "a4",
  margin: (top: 3cm, bottom: 2cm, left: 3cm, right: 2cm),
  header: context {
    if counter(page).get().first() > 1 {
      set text(size: 9pt, fill: gray)
      align(center, "Análise da Fábrica Agêntica")
    }
  },
  footer: context {
    set text(size: 9pt)
    align(center, [#counter(page).display("1") de #counter(page).final().first()])
  },
)

#set text(
  font: ("Times New Roman", "Liberation Serif"),
  size: 12pt,
  lang: "pt",
  region: "BR",
)

#set par(
  justify: true,
  leading: 0.75em,
  first-line-indent: 1.25cm,
)

// Definicao do horizontal rule (Pandoc gera #horizontalrule como texto)
#let horizontalrule = {
  v(1em)
  line(length: 100%, stroke: 1pt + cor.destaque)
  v(1em)
}

// Estilo de blocos de codigo (com borda na cor da paleta da capa)
#show raw.where(block: true): block.with(
  width: 100%,
  fill: cor.clara,
  stroke: 0.5pt + cor.secundaria,
  inset: 8pt,
  radius: 4pt,
)

// Estilo de codigo inline
#show raw.where(block: false): box.with(
  fill: cor.clara,
  inset: (x: 3pt, y: 0pt),
  outset: (y: 3pt),
  radius: 2pt,
)

// Estilo de citacoes (blockquote) com borda lateral na cor da paleta da capa
#show quote: it => block(
  width: 100%,
  fill: cor.clara,
  inset: (left: 12pt, right: 8pt, top: 8pt, bottom: 8pt),
  stroke: (left: 3pt + cor.destaque),
  radius: (right: 4pt),
  it,
)

// Figuras (diagramas Mermaid renderizados) — nunca extrapolam a mancha grafica
#set image(width: 88%, fit: "contain")
#show figure: it => {
  set par(first-line-indent: 0cm)
  v(0.6cm)
  align(center, it)
  v(0.6cm)
}
#show figure.caption: it => {
  set text(font: ("Inter", "Liberation Sans", "Arial"), size: 10pt, fill: cor.secundaria, weight: "bold")
  it
}

// Regra geral de titulos: sempre fonte INTER e cores da paleta da capa
#show heading: set text(font: ("Inter", "Liberation Sans", "Arial"))

// Estilo de titulos - nivel 1 (com suporte a Parte)
#show heading.where(level: 1): it => {
  set par(first-line-indent: 0cm)
  let isParte = type(it.body) == str and it.body.starts-with("Parte")
  pagebreak()
  if isParte {
    set text(font: ("Inter", "Liberation Sans", "Arial"), size: 20pt, weight: "bold", fill: cor.primaria)
    v(3cm)
    it
    v(0.3cm)
    line(length: 40%, stroke: 2.5pt + cor.destaque)
    v(2cm)
  } else {
    set text(font: ("Inter", "Liberation Sans", "Arial"), size: 16pt, weight: "bold", fill: cor.primaria)
    v(2cm)
    it
    v(0.2cm)
    line(length: 30%, stroke: 2pt + cor.destaque)
    v(1cm)
  }
}

// Estilo de titulos - nivel 2
#show heading.where(level: 2): it => {
  set text(font: ("Inter", "Liberation Sans", "Arial"), size: 14pt, weight: "bold", fill: cor.secundaria)
  set par(first-line-indent: 0cm)
  v(1cm)
  it
  v(0.2cm)
  line(length: 15%, stroke: 1.5pt + cor.destaque)
  v(0.4cm)
}

// Estilo de titulos - nivel 3
#show heading.where(level: 3): it => {
  set text(font: ("Inter", "Liberation Sans", "Arial"), size: 12pt, weight: "bold", fill: cor.secundaria)
  set par(first-line-indent: 0cm)
  v(0.75cm)
  it
  v(0.4cm)
}

// Estilo de titulos - nivel 4 em diante
#show heading.where(level: 4): it => {
  set text(font: ("Inter", "Liberation Sans", "Arial"), size: 11pt, weight: "bold", fill: cor.secundaria)
  set par(first-line-indent: 0cm)
  v(0.6cm)
  it
  v(0.3cm)
}

#let capa-grafica-ativa = "0" != "1"

// ── CAPA GRAFICA (Upgrade 5) ──────────────────────────────────────
#if capa-grafica-ativa {
  // Capa em imagem PNG (padrao visual da serie): pagina inteira, sem margens
  page(fill: rgb("#0b1020"), margin: 0cm, header: none, footer: none, numbering: none)[
    #image("imagens/capa-livro-analise-agentica.png", width: 100%, height: 100%, fit: "cover")
  ]
}

// ── FOLHA DE ROSTO (ABNT NBR 6029) ────────────────────────────────
#page(header: none, footer: none, numbering: none)[
  #set par(first-line-indent: 0cm, justify: false)
  #align(center)[
    #text(font: ("Inter", "Liberation Sans", "Arial"), size: 13pt, weight: "bold", fill: cor.secundaria)[Heverton Eduardo Peres]
    #v(3.5cm)
    #text(font: ("Inter", "Liberation Sans", "Arial"), size: 22pt, weight: "bold", fill: cor.primaria)[Análise da Fábrica Agêntica]
        #v(0.5cm)
    #text(font: ("Inter", "Liberation Sans", "Arial"), size: 14pt, fill: cor.secundaria)[Arquitetura Limpa | Código Limpo | Segurança | UI/UX]
      ]
  #v(4cm)
  #align(right, block(width: 8.5cm)[
    #set text(size: 10.5pt)
    #set par(justify: true, first-line-indent: 0cm)
    Obra técnica de literatura especializada, produzida e diagramada conforme as
    normas ABNT para publicação editorial.
  ])
  #v(1fr)
  #align(center)[
    #set text(size: 11pt)
    Brasil
    #linebreak()
    #datetime.today().display("[year]")
  ]
]

// ── VERSO DA FOLHA DE ROSTO: FICHA CATALOGRAFICA (CIP) ────────────

// ── SUMARIO ───────────────────────────────────────────────────────
#outline(title: [Sumário], indent: 1.5cm, depth: 3)

// ── CONTEUDO PRINCIPAL ────────────────────────────────────────────
= RELATÓRIO DE ANÁLISE --- FÁBRICA AGÊNTICA DE PUBLICAÇÕES
<relatório-de-análise-fábrica-agêntica-de-publicações>
#strong[Projeto:] `proj_fabrica-de-livros` \ #strong[Versão analisada:] V5 (coleção multi-formato) + evolução histórica V3→V5.5 \ #strong[Data:] 18/08/2026 \ #strong[Analisador:] Solar Pro 4 (via Hermes Agent) \ #strong[Escopo:] análise de arquitetura, código, segurança e UI/UX --- opinião técnica sem alteração de artefatos

#horizontalrule

== 1. ANÁLISE DE ARQUITETURA LIMPA
<análise-de-arquitetura-limpa>
=== 1.1 Visão geral
<visão-geral>
A fábrica é um #strong[sistema orquestrador de produção de conteúdo editorial] com tipificação declarativa (8 tipos de obra: Livro, TCC, Artigo, E-book, Playbook, Lead Magnet, Deck, E-mails), pipeline determinístico (scripts Python) + agentes LLM, geração de múltiplos formatos (PDF, EPUB, HTML, PPTX), camadas opcionais de campanha e máquina de vendas, e portabilidade multi-IDE via hardlinks/junctions.

=== 1.2 Pontos fortes
<pontos-fortes>
#figure(
  align(center)[#table(
    columns: (50%, 50%),
    align: (auto,auto,),
    table.header([Aspecto], [Observação],),
    table.hline(),
    [#strong[Registro declarativo central]], [`scripts/tipos_obra.py` é o único lugar para adicionar um tipo novo --- os 6 pontos de dispatch consultam o registro. Isso é decisão de design limpa: editar 1 arquivo, não 6.],
    [#strong[Separação de responsabilidades por fase]], [Fase 1 (P&D) → Fase 2 (manufatura paralela) → Fase 2.5 (peer review) → Fase 3 (acabamento) → Fase 4 (coleção derivada). Cada fase tem agentes/skill próprios e contratos de dados explícitos (JSON de estado, pool, auditoria).],
    [#strong[Deterministicismo onde importa]], [Scripts como `indexar-dossie.py`, `pool-capitulos.py`, `validar-codigo.py`, `auditar-obra.py`, `renderizar-diagramas.py` são determinísticos. Os gates de conteúdo (R-RF, R-MT, R-ES, R-AF, R-FT) adicionam verificação de mérito além da estrutura.],
    [#strong[Desenho multi-IDE sólido]], [Hardlinks (`AGENTS.md`↔`CLAUDE.md`), junctions (`agentic/*`, `.agents/*`, `.opencode/*` → `.claude/*`), scripts de sincronização de MCP (`sync-vscode-mcp.mjs`, `sync-opencode-mcp.mjs`). O `.git/hooks/pre-commit` é copiado, não linkado --- correto, pois `.git/hooks` não aceita junction confiável.],
    [#strong[Economia de tokens como princípio de arquitetura]], [Regras 0.1--0.12 documentadas e aplicadas (caveman, headroom, lean-ctx, delegação cavecrew). Pesquisa acadêmica V5.4 é custo-zero via APIs abertas. Artigos/ebooks reaproveitam dossiê indexado --- não pesquisam do zero.],
    [#strong[Estação resistente a falhas]], [Backoff exponencial por capítulo (máx. 3), pool registra falha e marca `esgotado`, Pandoc/Typst ausentes → Markdown expedido e pendência reportada (não bloqueia), mermaid-cli ausente → diagrama permanece como código no PDF.],
  )]
  , kind: table
  )

=== 1.3 Pontos de atenção / degenerações sintomáticas
<pontos-de-atenção-degenerações-sintomáticas>
+ #strong[Caminhos hardcoded de binaries (Windows-only)]
  - `compilar-para-pdf.py:97-98` fixa os paths do Pandoc e Typst derivados de uma instalação específica via WinGet. Isso quebra portabilidade (outro usuário/URL WinGet diferente) e impede execução em Linux/macOS sem edição. A arquitetura multi-IDE e multi-plataforma prometida no AGENTS.md §6 não se estende ao pipeline de compilação. O ideal: resolver via `shutil.which` com fallback para paths configuráveis, ou variável de ambiente.
+ #strong[Hardcodificação do autor no template]
  - `compilar-para-pdf.py:336`: `"-V", "author=Heverton Eduardo Peres"` --- fixo no código, não vem de `config_obra.json` nem de metadados. Para uma fábrica que produz obras de múltiplos autores, isso é um vazamento de responsabilidade: o autor deveria ser campo do registro de obra.
+ #strong[Imports relativos via `sys.path.insert`]
  - `compilar-para-pdf.py:26`: `sys.path.insert(0, str(Path(__file__).parent / "scripts"))` --- funciona, mas é menos limpo que um pacote Python instalável ou `PYTHONPATH`. Se o projeto crescer ou ganhar test coverage no script, isso fica frágil.
+ #strong[Dualidade plana vs.~hub por coleção ainda deixa rastros]
  - O AGENTS.md acrescentou um bloco RTK (l. 458-462) registrando que `fatiar-obra.py --playbook` gravou em `output/playbooks/` (fora do hub) e `minerar-fontes-academicas.py` gravou em `output/<slug>/pesquisa/` (fora do hub). Isso é um sintoma de que a regra "SEMPRE usar `tipos_obra.dir_obra(slug)`" não é verificada antes da gravação --- depende da disciplina do agente. Um guardião de caminho no `tipos_obra.py` (ex.: `_assert_dentro_do_hub`) seria mais robusto que confiar na memória do agente.
+ #strong[Subagente de expansão travou em 48 turns] (l. 440-444)
  - Registrado no RTK: spawnar 1 subagente para expandir 8 capítulos estoura o limite de turns. Isso não é falha de arquitetura, mas é evidência de que a granularidade da tarefa não foi calibrada. A prevenção sugerida (lotes de 2-3) é boa, mas é uma prevenção documental, não estrutural.
+ #strong[Código de configuração muito disperso entre scripts e JSONs]
  - `config_obra.json`, `tipos_obra.py`, `metadados_livro.py`, `parametros_obra.py`, `series_capa.py`, `colecao.py`, `campanha.py`, `scripts/hooks/pre-commit`, `puppeteer.config.cjs`, `opencode.json`, `.mcp.json`, templates Typst, templates HTML de campanha --- todos carregam pedaços da verdade. Não há um `config_schema` único ou um `json-schema` do contrato de estado. Quando surge um bug de derivação (ex.: `obra_mae` vs.~`serie`/`livro_mae`, l. 243), a raiz é que vários scripts leem campos com nomes diferentes e só a experiência mostra qual é o canônico.

#horizontalrule

== 2. ANÁLISE DE CÓDIGO LIMPO
<análise-de-código-limpo>
=== 2.1 Legibilidade
<legibilidade>
#strong[Positivos:]
\- Docstrings em português no início dos scripts explicando propósito, pipeline e modo de uso.
\- Funções com nomes declarativos: `converter_via_typst`, `variaveis_visuais`, `comando_pandoc`, `renderizar_diagramas`, `validar_playbook`.
\- Código de validação de código (`validar-codigo.py`) é bem estruturado: dicionário `VALIDADORES`, regex `RE_BLOCO`, separação clara entre validação estática e execução (`--executar`).

#strong[Atenções:]
\- `compilar-para-pdf.py` tem #strong[\~30 imports de `SLUGS_*` via try/except] (l. 41-92). Isso esconde a configuração real em 8 módulos opcionais que podem ou não existir --- dificulta saber quais livros serão compilados sem rastrear 8 arquivos. Uma lista única ou carregamento via JSON/manifest seria mais legível.
\- `compilar-para-pdf.py:524-531`: frontmatter YAML montado com string f.~Ok para o tamanho, mas se o autor/data/linguagem virarem campos do registro, esse trecho deve sair para `metadados_livro`.
\- `validar-codigo.py:229-238`: `detectar_linguagem` é heurística com regex --- aceitável para playbook cards sem tag, mas pode misclassificar. Não há teste visível para essa função.

=== 2.2 DRY / Coesão / Acoplamento
<dry-coesão-acoplamento>
#strong[O que está bom:]
\- `tipos_obra.py` como registro central remove duplicação de dispatch por tipo.
\- `validar-codigo.py` tem uma única função `validar_arquivo` e `validar_playbook` que compartilham a lógica de extração de blocos e aplicação de validadores.
\- `compilar-para-pdf.py` delega a `tipos_obra.compilador_de` para tipos com motor próprio --- evita `if/elif` por tipo.

#strong[O que sente-se repetitivo ou acoplado:]
\- Tratamento de imports opcionais (`try: import X except ImportError: X=None`) é repetido em `compilar-para-pdf.py` (métadados\_livro, parametros\_obra, tipos\_obra) e provavelmente em outros scripts. Uma função util `import_opcional(name)` ou um módulo `fabrica_imports` reduziria boilerplate.
\- Múltiplos scripts leem `config_obra.json` de forma independente --- se o schema mudar, há N lugares para atualizar. O `parametros_obra.py` parece ser o canônico, mas não é claro que todos os scripts passam por ele.
\- Template Typst e template HTML são mantidos separados --- OK, são mundos diferentes (PDF vs.~Chromium). Porém, a lógica de #strong[gable, paleta, ficha catalográfica] aparece em `metadados_livro.py` (Python) e nos templates Typst --- se a paleta mudar, há dois lugares.

=== 2.3 Testabilidade
<testabilidade>
- `pytest.ini` existe + `tests/` com testes (provavelmente `test_auditar_obra.py`, `test_parametros_obra_v5.py`, `test_campanha.py`, `test_colecao_hub.py`, `test_maquina_colecao.py`, conforme registrado no RTK).
- `validar-codigo.py` é testável por natureza --- função pura que recebe texto e devolve lista de registros.
- R16 (nunca commitar vermelho) é uma regra de processo sólida, e o hook `pre-commit` que bloqueia commit se `pytest -q` falhar é a mecanização correta.

#strong[Atenção:]
\- O script de compilação (`compilar-para-pdf.py`) depende de Pandoc e Typst instalados em paths específicos --- testes que dependem desses binaries são frágeis em qualquer máquina que não tenha a configuração exata. O RTK menciona `precisa_pandoc_typst` como skip em testes --- correto, mas indica que a cobertura do caminho de compilação real é limitada.

=== 2.4 Manejo de erros e limites
<manejo-de-erros-e-limites>
- `compilar-para-pdf.py` tem `try/except` bem colocado ao redor do `subprocess.run` com `TimeoutExpired` e `Exception` genérico, e reporta o erro com stdout/stderr truncado. Bom.
- `validar-codigo.py` tem `_rodar` com `FileNotFoundError`, `TimeoutExpired`, `Exception` --- cobertura adequada.
- Um ponto: `subprocess.run` com `capture_output=True` e timeout é usado em vários lugares, mas em `validar-codigo.py:269-271` o `cwd=td` (tempdir) está correto para sandbox leve. Para blocos bash arbitrários, um tempdir não é sandbox completo (o código pode ler arquivos absolutos) --- mas para o uso pretendido (smoke test de código de capítulo/playbook) é aceitável.

#horizontalrule

== 3. FALHAS E BUGS DE SEGURANÇA
<falhas-e-bugs-de-segurança>
Nota: "segurança" aqui é avaliada no contexto de #strong[sistema de produção de conteúdo editorial orquestrado por agentes], não como aplicação web voltada a usuário final (embora a máquina de vendas seja um caso parcial).

=== 3.1 Não mitigado / de design
<não-mitigado-de-design>
+ #strong[Execução de código arbitrário via `--executar`]
  - `validar-codigo.py:8-10`: "Com `--executar`, os blocos executáveis (python/javascript/bash) são também EXECUTADOS em sandbox leve".
  - `executar_bloco` (l. 241-283): executa python com `sys.executable -c`, node com `node -e`, bash com `bash -c`, em tempdir com env minimalista.
  - #strong[Risco:] qualquer agente/redator que injete um bloco de código malicioso (ou acidentalmente destrutivo) em um capítulo/playbook e passe `--executar` está a executar. O tempdir restringe gravações, mas o código pode ainda assim fazer leitura de arquivos sensíveis via caminhos absolutos, ou emitir rede se houver acesso. Para um projeto solo/perfeitamente confiável é baixo risco; para um projeto com múltiplos colaboradores ou com prompts genéricos de LLM, o risco sobe.
  - #strong[Mitigação recomendada:] deixar `--executar` explícito e documentado como "apenas para conteúdo de confiança"\; ou adicionar um allowlist de origem (só executar se o bloco vier de `output/<slug>/capitulos/` versionado, não de stdin/bruto).
+ #strong[Máquina de vendas com `POST /api/checkout` e armazenamento local]
  - Registro no RTK (l. 313-326 e 320-326): máquina Next.js + FastAPI, rota `POST /api/checkout` com zod, leads vão para `/api/leads/`, backend usa `backend/data/vendas.db`.
  - #strong[Risco:] é uma aplicação web exposta (se deployada). O registro fala em "testar `POST /api/checkout`" e "verificar que o lead chega em `/api/leads/`", mas não há menção a validação de entrada além de zod, rate limiting, proteção contra spam, CSRF, autenticação de administrador para acessar leads, ou criptografia do banco. Se a máquina for deployada na internet, ela vira um ponto de coleta de contato (e-mail/nome) --- a responsabilidade de proteção de dados é do operador, mas a fábrica não documenta expectativas mínimas de segurança para o deploy.
  - #strong[Mitigação recomendada:] adicionar uma seção no AGENTS.md ou no comando `/criar-maquina` com "checklist de segurança de deploy": autenticação no admin, rate limiting, HTTPS, não logar dados sensíveis, política de retenção dos leads.
+ #strong[Chaves/credenciais nos ambientes]
  - O projeto usa várias APIs (OpenAlex, Crossref, arXiv, Semantic Scholar, SciELO, PubMed --- V5.4), possível CloudConvert para fallback de PDF, MCP servers.
  - Não há visão de `.env` ou `config/secrets.json` neste analysis (não li tudo). O `requirements.txt` é minimalista. O risco é que credenciais possam estar hardcoded em algum script de pesquisa ou configuração de MCP. Recomenda-se varrer os scripts de `fontes_academicas.py`, `minerar-fontes-academicas.py` e `.mcp.json` para confirmar que não há chaves em texto puro.
+ #strong[Hardlinks e junctions como portabilidade]
  - O AGENTS.md descreve hardlinks (`AGENTS.md`→`CLAUDE.md`) e junctions (`.opencode/*` → `.claude/*`). Isso é ótimo para portabilidade multi-IDE, mas cria uma dependência da estrutura de arquivos: se alguém clonar e não rodar `scripts/setup-links.ps1`, vários agentes e comandos não carregam. O risco não é de segurança, mas de #strong[integridade operacional]: um repositório clonal pode parecer funcional mas ter agentes silenciosamente vazios.
+ #strong[Execução de comandos com paths absolutos do Windows]
  - `compilar-para-pdf.py:97-98` e `subprocess.run([PANDOC, ...])`: se o path do Pandoc/Typst mudar ou se o script for executado por um usuário diferente, falha silenciosamente com `[ERRO] Pandoc não encontrado`. Não é uma vulnerabilidade, mas é uma #strong[falha de confiabilidade] que pode levar o operador a pensar que a compilação funcionou (se o script for mal interpretado).

=== 3.2 Mitigado (bom trabalho documentado)
<mitigado-bom-trabalho-documentado>
- `validar-codigo.py` trata `FileNotFoundError` (ferramenta ausente), `TimeoutExpired` e `Exception` em `_rodar` --- não propaga falhas brutas.
- Sandbox leve com `tempfile.TemporaryDirectory` + env minimalista para execução de blocos.
- Smoke test dos cards do playbook (`validar-playbook`) com gate executável --- o gate vira comando executado, o que valida que o passo é realmente aplicável.
- `auditar-obra.py --estrito` encadeia gates de conteúdo offline (`--sem-rede`) --- referências rodam offline e são cacheadas, o que reduz dependência de rede no momento da auditoria.
- R16 (nunca commitar vermelho) + hook pre-commit bloqueia commit se pytest falhar --- impede que código com testes quebrados entre no repositório.
- Validação de URLs/DOI reais (`validar-referencias.py`) com reprovação de 4xx/DNS --- evita que referências inventadas ou quebradas vão para o livro final.

#horizontalrule

== 4. ANÁLISE DE UI/UX
<análise-de-uiux>
Aqui "UI/UX" é interpretado no contexto do sistema: interação do operador com a fábrica (comandos, relatórios, saídas geradas, máquina de vendas, campanhas).

=== 4.1 Interação operador ↔ fábrica
<interação-operador-fábrica>
#strong[Bom:]
\- `/esbocar <tema>` como #strong[único ponto de interação humana] (Fase 0) é decisão de UX excelente --- depois a fábrica roda autonomamente, o que reduz fricção. Perguntas condicionais (Q5 só se Livro, Q6 só se artigos = Sim) mostram cuidado com o fluxo.
\- Saída objetiva do `/esbocar` com linha única de próximo passo (`/produzir-obra-completa <slug>` ou comandos individuais) --- evita que o operador fique na dúvida.
\- Opção de comandos individuais (`/criar-livro`, `/criar-tcc`, `/criar-artigo`, `/criar-ebook`) + full (`/produzir-obra-completa`) dá ao operador controle granular ou atalho total.
\- Regra 17 (CAMPANHA e MÁQUINA são opcionais, gate `grep 'Autor Digital|centenas de pessoas'` vazio) --- a personalização não é opcional apenas no papel; há um gate real que reprova máquinas não personalizadas.

#strong[Atenção:]
\- #strong[V5.2 exige relatório MD+PDF por sessão] em `relatorios/`. Isso é ótimo para rastreabilidade, mas se a fábrica roda muitas sessões rápidas, o operador pode acumular muitos PDFs pequenos. Não há menção de retenção/arquivamento --- pode virar ruído.
\- Quando algo falha (ex.: Pandoc ausente, mermaid-cli ausente, timeout), o sistema reporta, mas o #strong[operador precisa interpretar] o relatório. Para um operador leigo, a diferença entre "Markdown expedido, pendência de PDF" e "falha de compilação" pode não ser óbvia sem ler o relatório.

=== 4.2 UI/UX dos entregáveis gerados
<uiux-dos-entregáveis-gerados>
- #strong[Livro (PDF via Pandoc+Typst):] template ABNT (`template.typ`), capa gráfica 2D plano, ficha CIP, sumário com `--toc-depth 3`, numeração de seções. Isso é UX editorial sólida --- o leitor final não vê a fábrica, vê um livro ABNT profissional.
- #strong[TCC (template\_tcc.typ):] folha de aprovação, resumo/abstract, numeração progressiva. Adequado à norma.
- #strong[Artigo (template\_artigo.typ):] layout compacto. Adequado.
- #strong[E-book (EPUB via Pandoc):] sumário clicável, capa 1:1,6, CTA no final. Adequado ao mercado.
- #strong[Lead magnet (HTML+CSS→Chromium→PDF):] A4 com CTA no rodapé. Boa escolha de motor para peça de marketing.
- #strong[Deck (HTML 16:9 navegável + PDF):] apresentação offline via navegador. Boa.
- #strong[Campanha (artes PNG via Chromium, cronogramas MD+PDF):] as artes são geradas por formato (Instagram, LinkedIn, WhatsApp) com variação por envio --- R-CP-6 (unicidade por MD5) garante que não são duplicadas. O cronograma tem 4 dimensões (o quê / por quê / como / quando) --- excelente UX de uso.

=== 4.3 Máquina de vendas
<máquina-de-vendas>
- Gerada por `/criar-maquina <slug>` com 1:1 por coleção, snapshot das campanhas, personalização por nicho (8 pontos) com gate real --- bom.
- O registro no RTK (l. 313-326) mostra que houve bugs reais no template inicial (campo `produto` default desconectado de `config/produtos.json`, checkout page sem campo de e-mail nomeando → 404, form urlencoded vazio → 500 no `request.json()`). Os bugs foram corrigidos, mas é um sinal de que a #strong[UX do desenvolvedor ao integrar a máquina] (qualidade do template inicial) teve falhas que só apareceram no uso.

=== 4.4 Pontos de fricção de UX
<pontos-de-fricção-de-ux>
+ #strong[Caminhos longos do Windows] --- `output/<raiz>/<código-obra>/<pfx>-<seq>-<nome>/` ainda pode chegar perto do MAX\_PATH (260) em hubs com coleções grandes. A regra V5.1 encurtou de \~197 para \~150 chars, mas em cenários de campanhas com 12 materiais e múltiplos volumes, o caminho completo pode voltar a ficar grande. A validação `nomes_curtos.py` existe, mas o operador pode ficar confuso quando um material "não é encontrado" por causa de path truncado no Windows.

+ #strong[Explicação de "coleção vs.~série vs.~hub"] --- O AGENTS.md tem um glossário (l. 173-177), mas é um conceito abstrato que o operador precisa internalizar para navegar no `output/` e entender comandos como `/colecao`, `colecao.py --sincronizar`. Para um operador novo, a estrutura de pastas pode parecer sobrenatural.

+ #strong[Relatórios em MD+PDF para cada sessão] --- boa prática, mas sem uma visão consolidada (ex.: index-page com todos os relatórios), o operador precisará navegar pela pasta `relatorios/` cronologicamente.

#horizontalrule

== 5. SÍNTESE
<síntese>
#figure(
  align(center)[#table(
    columns: (33.33%, 33.33%, 33.33%),
    align: (auto,auto,auto,),
    table.header([Dimensão], [Veredito], [Prioridade de atenção],),
    table.hline(),
    [#strong[Arquitetura Limpa]], [Sólida no núcleo (registro declarativo, separação de fases, deterministicismo, resiliência). Degenerescências: paths de binaries hardcoded, autor fixo no código, rastros de gravação fora do hub, necessidade de guardião de caminho.], [Média],
    [#strong[Código Limpo]], [Legível, docstrings, funções com nome, separação de validação/execução. Repetição de imports opcionais, montagem de frontmatter em string f, heurística de detecção de linguagem sem teste visível.], [Baixa],
    [#strong[Segurança]], [Boas práticas de sandbox leve, pre-commit, gates offline, validação de referências. Riscos: execução arbitrária via `--executar` (baixo para uso solo, subiria com colaboradores/prompts genéricos), máquina de vendas sem checklist de segurança de deploy documentado, possibilidade de credenciais hardcoded em scripts de pesquisa/MCP (não verificado neste analysis).], [Média (para o caso de deploy da máquina)],
    [#strong[UI/UX]], [Boa interação operador (Fase 0 interativa + autonomia + opção full/individual + gate de personalização). Entregáveis editoriais com qualidade. Fricções: conceito de hub/coleção/série abstrato, caminhos longos, relatórios por sessão sem index consolidado.], [Baixa],
  )]
  , kind: table
  )

#horizontalrule

== 6. O QUE NÃO ENTRA NESTE RELATÓRIO (por escopo)
<o-que-não-entra-neste-relatório-por-escopo>
- Análise de qualidade do conteúdo editorial (dossiê, sumários, capítulos) --- seria necessário ler obras específicas em `output/`.
- Análise da suíte de testes (`pytest`) com execução real --- não rodamos a suíte neste analysis.
- Varredura de `.env`, `.mcp.json`, scripts de `fontes_academicas`, `.claude/settings.json` em busca de credenciais.
- Análise de UI da máquina de vendas em si (Next.js + FastAPI) --- preciso ler o template gerado.

Se quiser, posso aprofundar qualquer um dos tópicos acima lendo os arquivos concretos que faltaram (ex.: `tipos_obra.py`, `scripts/hooks/pre-commit`, `templates/`, `skills/`, um livro pronto em `output/`).

// ── CONTRACAPA ────────────────────────────────────────────────────
#pagebreak()
