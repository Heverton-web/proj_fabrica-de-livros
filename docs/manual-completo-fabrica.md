# MANUAL COMPLETO — FÁBRICA AGÊNTICA DE PUBLICAÇÕES

**Criação de Materiais | Transmutação | Campanhas | Máquina de Vendas | Automação**

> Manual do usuário — tudo o que é possível criar e fazer com a Fábrica Agêntica de Publicações, explicado passo a passo com seções detalhadas de **Storytelling** para cada processo.
>
> **Autor:** Heverton Eduardo Peres — Especialista em Marketing e Desenvolvimento de Soluções  
> **Versão do projeto:** V5.3 (HUB por Coleção / Camada Campanha / Transmutação / Gates F1-F2)  
> **Atualizado em:** 2026-08-10

---

# PARTE 1 — VISÃO GERAL E FILOSOFIA AGÊNTICA

## 1. O que é a Fábrica

A **Fábrica Agêntica de Publicações** é um sistema orquestrado por agentes de IA e scripts determinísticos que produz, de forma autônoma e rigorosa, uma família completa de materiais de publicação a partir de um único tema.

Um único tema inserido na esteira se transforma em uma **Coleção Completa**:
- Livro Comercial (formato ABNT, capas 2D profissionais, PDF + EPUB).
- TCC ou Artigo Científico (padrão ABNT NBR 14724 / NBR 6022).
- E-books de Recorte Comercial.
- Playbooks Práticos com cards de bancada executáveis.
- Lead Magnets (Checklists, Cheat-sheets, Mapas Mentais).
- Slide Decks 16:9 (HTML navegável + PDF).
- Sequência Nutritiva de E-mails com UTMs e Cronogramas.
- Peças de Campanhas para Redes Sociais e Canais de Comunicação.
- Máquina de Vendas Full-Stack (Next.js + FastAPI + SQLite) pronta para deploy.

### 📖 Storytelling: A Jornada de uma Ideia Bruta até o Ecossistema

Imagine um especialista técnico que possui vasta experiência em uma tecnologia complexa, mas não dispõe de meses para escrever livros, formatar normas ABNT, desenhar apresentações e criar funis de vendas.

No fluxo tradicional, esse especialista gastaria mais de 600 horas entre pesquisa, redação, design gráfico, formatação ABNT e configuração de servidores de vendas.

Na Fábrica Agêntica, o especialista fornece apenas um tema central (ex: *Oh My Position — Agentes de Código de Alta Performance*). A esteira entra em ação:
1. **O Pesquisador** vasculha e sintetiza evidências reais.
2. **O Arquiteto** desenha a estrutura lógica de capítulos e seções.
3. **O Squad de Redação** constrói o texto aplicando frameworks de aprendizagem.
4. **Os Gates de Auditoria** testam se os códigos funcionam e se as referências bibliográficas são reais.
5. **O Compilador Pandoc+Typst** gera os livros e PDFs impecáveis.
6. **O Gerador de Campanhas e Máquina de Vendas** ergue a loja virtual e o funil de marketing.

Em poucas horas, a ideia bruta se transforma em um ecossistema completo de publicações prontas para o mercado.

---

## 2. A Regra Intocável: HUB por Coleção

A partir da versão V5.3, toda a organização do diretório `output/` obedece rigorosamente à estrutura **HUB por Coleção**:

```
output/<slug-colecao>/
├── livros/             # Livro-mãe compilado (PDF, EPUB, capítulos)
├── tccs/               # Monografia ou TCC derivado
├── artigos/            # Artigos científicos IMRaD
├── ebooks/             # E-books temáticos de corte comercial
├── playbooks/          # Playbooks de bancada com cards executáveis
├── lead-magnets/       # Iscas digitais (Checklist, Mapas, Cheat-sheets)
├── decks/              # Apresentações 16:9 HTML + PDF
├── emails/             # Sequência nutritiva de e-mails
├── campanhas/          # Peças de divulgação (Instagram, LinkedIn, WhatsApp)
├── distribuicao/       # Acervo central de PDFs compilados para entrega
├── maquina/            # Máquina de vendas Full-Stack (Next.js + FastAPI)
└── colecoes/<nome>.json # Manifesto sincronizado do ecossistema
```

### 📖 Storytelling: A Casa Unificada do Conhecimento

Antes da versão V5.3, os arquivos ficavam espalhados em diretórios globais planos (`output/livros/`, `output/ebooks/`). Isso dificultava saber quais e-books pertenciam a qual livro ou onde ficavam as campanhas daquela obra específica.

Com o **HUB por Coleção**, cada tema ganha sua própria "estância" unificada. Se você quiser empacotar ou vender a coleção *Oh My Position*, tudo o que pertence a ela — do livro-mãe ao código do checkout do site — reside sob a pasta `output/oh-my/`. É a garantia de portabilidade, organização e controle absoluto de marca.

---

# PARTE 2 — TIPOS DE OBRA E MATERIAIS DA COLEÇÃO

A Fábrica suporta 8 tipos de obra declarativos definidos em `scripts/tipos_obra.py`:

| Tipo | Natureza | Custo LLM | Saídas | Motor de Compilação |
|---|---|---|---|---|
| **Livro** | Geração | Alto | `.pdf`, `.epub` | Pandoc → Typst (ABNT) |
| **TCC** | Geração | Alto | `.pdf` | Pandoc → Typst (NBR 14724) |
| **Artigo** | Compressão | Baixo | `.pdf` | Pandoc → Typst (NBR 6022) |
| **E-book** | Compressão | Baixo | `.pdf`, `.epub` | Pandoc → Typst |
| **Playbook** | Extração | Zero | `.pdf` | Pandoc → Typst (`template_playbook.typ`) |
| **Lead Magnet** | Extração | Zero | `.pdf`, `.png` | Pandoc → Typst / HTML+CSS → Chromium |
| **Slide Deck** | Extração | Zero | `.html`, `.pdf` | HTML+CSS → Chromium (Navegável) |
| **E-mails** | Extração | Baixo | `.md`, `.pdf` | Pandoc → Typst |

### 📖 Storytelling: Adaptando a Mensagem para cada Formato de Leitor

Nem todo leitor consome informação da mesma maneira:
- O **Executivo ou Acadêmico** exige a profundidade e o rigor formal do **Livro** ou **TCC**.
- O **Engenheiro de Campo** quer abrir o **Playbook** no segundo monitor e executar passo a passo o card de bancada.
- O **Lead Indeciso** prefere baixar um **Checklist** rápido de 2 páginas antes de comprar a obra completa.
- O **Palestrante** precisa do **Slide Deck** 16:9 pronto para projetar na conferência sem refazer layouts.

Ao invés de reescrever manualmente o conteúdo para cada público, a fábrica extrai e remodela a mesma essência técnica em múltiplos formatos de leitura.

---

# PARTE 3 — O FLUXO EDITORIAL DE PRODUÇÃO

## 1. Fase 1: Mineração & Arquitetura Macro
- **Skills:** `pesquisador`, `arquiteto`
- **Scripts:** `indexar-dossie.py`
- **O que faz:** Varre repositórios, documentações e referências técnicas, indexando o dossiê RAG em SQLite e construindo o `sumario_macro.json`.

### 📖 Storytelling: O Alicerce sem Alucinações
Antes de escrever uma única linha de código ou texto, a fábrica constrói uma "biblioteca blindada" de fatos e dados técnicos. O **Pesquisador** lê fontes confiáveis e o **Arquiteto** desenha a estrutura do livro dividida em Partes, Capítulos e Marcos EITA (Introdução, Explica, Ilustra, Técnica, Aplica). Esse alicerce impede que a IA invente informações ou perca o foco temático.

---

## 2. Fase 2: Manufatura & Redação em Lotes
- **Skills:** `estrategista`, `redator-eita`, `redator-academico`, `redator-ebook`
- **Scripts:** `pool-capitulos.py`, `secoes_eita.py`
- **O que faz:** O `estrategista` cria o plano de 3 pilares para cada capítulo. O `redator` expande o texto final aplicando rigorosamente a estrutura pedagógica EITA-V2.

### 📖 Storytelling: A Linha de Montagem de Capítulos
A redação não ocorre em um único bloco gigante e propenso a esquecimentos. Ela opera como uma linha de montagem: capítulos são processados em lotes controlados. Cada capítulo recebe métricas obrigatórias, código executável, testes de verificação e limites claros de escala.

---

## 3. Fase 2.5: Auditoria Estrita & Gates de Conteúdo
- **Skills:** `revisor-tecnico`
- **Scripts:** `auditar-obra.py --estrito`, `validar-codigo.py --executar`
- **Gates de Conteúdo F1/F2:**
  1. `validar-referencias.py` (R-RF): Checa se URLs e DOIs citados existem de fato (4xx/DNS reprova).
  2. `validar-metricas.py` (R-MT): Exige métricas com valor + unidade + citação por capítulo.
  3. `validar-escala.py` (R-ES): Garante que a seção *Aplica* traz limites e contornos claros.
  4. `validar-afirmacoes.py` (R-AF): Reprova dados factuais que não possuam citação `[N]`.
  5. `validar-fontes.py` (R-FT): Exige pelo menos 70% de fontes classificadas como reputação A ou B no dossiê.

### 📖 Storytelling: O Revisor Desconfiado
Imagine um revisor técnico extremamente rigoroso que não aceita nada sem provar. Ele pega cada link do livro e faz um teste de ping real na internet. Ele pega cada trecho de código Python ou Bash e executa em um ambiente seguro para garantir que não haverá erros de sintaxe. Se uma fonte falhar ou se o código quebrar, o capítulo é devolvido para correção antes de ir para a gráfica.

---

## 4. Fase 3 & 4: Compilação, Capas 2D e Extração da Coleção
- **Scripts:** `compilar-para-pdf.py`, `gerar-capa.py`, `gerar-epub.py`, `extrair-passos-praticos.py`, `gerar-lead-magnet-pdf.py`, `gerar-deck-html.py`, `gerar-sequencia-emails.py`.
- **O que faz:** Junta os capítulos finalizados, gera capas gráficas 2D com a badge de nível exigida pela Regra R5, compila os livros via Pandoc+Typst, extrai os Playbooks, Lead Magnets, Decks e E-mails da coleção.

---

# PARTE 4 — REESCRITA E TRANSMUTAÇÃO DE MATERIAIS

## 1. Transmutação entre Tipos de Obra
- **Script:** `scripts/transmutar-obra.py`
- **Comandos:** `/reescrever`, `/refinar`, `/reescrever-como`, `/reescrever-capitulo`
- **O que faz:** Permite metamorfosear uma obra existente em outro tipo sem perder o histórico nem as referências.
  - Exemplo: Transmutar um **Livro** em **TCC**, ou um **Playbook** em **E-book**.

### 📖 Storytelling: A Metamorfose do Conhecimento
Muitas vezes, um livro técnico de sucesso precisa ser transformado em um trabalho acadêmico (TCC) para defesa institucional, ou em um E-book leve para leitura rápida no celular.

Em vez de copiar e colar manualmente, o script de transmutação faz o recorte inteligente da estrutura de origem, aplica o novo layout e cria um backup em `revisao/backups/timestamp/`. O conteúdo ganha um novo reframing mantendo 100% da integridade bibliográfica.

---

# PARTE 5 — A CAMADA CAMPANHA (V5.3)

## 1. Geração de Peças de Marketing e Cronogramas
- **Scripts:** `scripts/criar-campanha.py`, `scripts/campanha.py`, `scripts/validar-campanha.py`
- **Comandos:** `/campanha <slug>` ou `/campanha-completa [colecao]`
- **Localização:** `output/<colecao>/campanhas/<material-slug>/`
  - `redes-sociais/`: Instagram (cards 1080x1350) + LinkedIn (artigos e posts).
  - `canais-comunicacao/`: E-mails de lançamento + disparos WhatsApp.
  - `cronograma.md`: Calendário estruturado em 4 dimensões (*O quê / Por quê / Como / Quando*).

### 📖 Storytelling: O Eco no Mercado
De nada adianta ter um livro espetacular se ninguém souber que ele existe. A camada **Campanha** transforma os principais ensinamentos da obra em pílulas diárias de conteúdo.

O script calcula as datas reais de publicação e gera as artes visuais em PNG diretamente dos moldes HTML/CSS. Quando a campanha é lançada, o autor sabe exatamente o que postar na segunda-feira às 09h00 no LinkedIn e qual mensagem enviar no grupo VIP do WhatsApp na quarta-feira.

---

# PARTE 6 — MÁQUINA DE VENDAS 1:1 (V5.3)

## 1. Arquitetura Full-Stack Deployável
- **Script:** `scripts/criar-maquina-vendas.py <slug-colecao>`
- **Comando:** `/criar-maquina <slug-colecao>`
- **Localização:** `output/<slug-colecao>/maquina/`
- **Tecnologias:**
  - **Frontend:** Next.js (App Router, TailwindCSS, TypeScript, Zod).
  - **Backend:** FastAPI (Python, validação Pydantic, rotas REST).
  - **Banco de Dados:** SQLite (`data/vendas.db`).

### 2. Funcionalidades Nativas da Máquina:
1. **Landing Page Comercial:** Apresenta a coleção, depoimentos, capítulos e garantias.
2. **Captura de Leads:** Formulário com download imediato do Lead Magnet.
3. **Checkout Integrado (`/api/checkout`):** Rota REST validada com Zod, registrando compradores e enviando dados para `/api/leads/`.
4. **Snapshot das Campanhas:** Pasta `maquina/campanhas/` trazendo todas as artes e e-mails para rápida consulta do operador da loja.

### 📖 Storytelling: A Loja Aberta 24 Horas por Dia
Quando o leitor clica no link do anúncio do Instagram, ele é direcionado para a **Máquina de Vendas** da coleção. Ele visualiza a capa 3D do livro, os cards do Playbook e o botão de checkout. Ao digitar seu e-mail e nome, o sistema registra o pedido no banco SQLite local e libera imediatamente o download do PDF. A máquina opera de forma 100% autônoma.

---

# PARTE 7 — AUDITORIA, ENTREGA DE SESSÃO E COMANDOS

## 1. Protocolo de Entrega de Sessão V5.2
Toda sessão de trabalho na Fábrica é encerrada com um **Relatório de Sessão** obrigatório em `relatorios/`:
- `relatorios/<YYYY-MM-DD>-<tema-da-sessao>.md`
- `relatorios/<YYYY-MM-DD>-<tema-da-sessao>.pdf`

Gerado automaticamente via:
```bash
python scripts/gerar-relatorio-sessao.py "Tema da Sessão"
```

## 2. Validação Global de Artefatos
Para garantir que nenhum PDF ou arquivo esteja corrombido antes do empacotamento:
```bash
python scripts/validar-artefatos.py --todos --estrito
```

## 3. Script de Resolução Autônoma em Lote
Para compilar e resolver pendências da obra de forma rápida:
```powershell
.\scripts\executar_oh_my.ps1
```

### 📖 Storytelling: O Selo de Qualidade no Encerramento do Dia
No final de cada dia de desenvolvimento ou escrita, a fábrica não deixa pontas soltas. É rodada a suíte de testes unitários (`pytest`), verificada a integridade de abertura de todos os PDFs gerados, sincronizado o manifesto da coleção e gravado o relatório de sessão. O trabalho é selado com commit e push para o repositório remotos com a garantia de 100% de luz verde.
