# Capítulo 6: Memória: curto prazo, longo prazo e vetorial

## 1. Introdução

No Capítulo 5 você aprendeu que o contexto é o palco do agente — e que a camada de recuperação é uma das mais importantes. Este capítulo constrói o que alimenta essa camada: o **sistema de memória**. Sem memória, o agente é um amnésico eloquente: trata cada interação como a primeira, esquece o cliente que preferiu e-mail, ignora a política atualizada, repete erros já corrigidos. Com memória bem projetada, o agente lembra, aprende e se adapta — o que separa o atendimento de "transação" do atendimento de "relacionamento" [17][22].

A memória de agentes é um dos campos que mais evoluiu: o que antes era "colocar tudo no histórico da conversa" virou uma disciplina com taxonomia, benchmarks e SDKs dedicados. A LangChain lançou o LangMem, um SDK específico para memória de longo prazo de agentes [17]; o ecossistema produz benchmarks de progresso da memória de agentes [22]; e a pesquisa acadêmica consolida a taxonomia de memória — curto prazo, longo prazo, de trabalho e episódica [23].

Ao final deste capítulo, você será capaz de desenhar o sistema de memória do OrquestraIA completo: a memória de curto prazo dentro da janela de contexto, a memória de longo prazo em banco vetorial com embeddings e recuperação por similaridade, e a memória episódica que registra o que aconteceu em cada missão. Você implementará cada camada e aprenderá as decisões de engenharia — o que persistir, como indexar, como recuperar, quando esquecer — que determinam se a memória ajuda ou atrapalha.

## 2. Explica

### A Taxonomia da Memória

A memória de um agente não é um único mecanismo: é um sistema com camadas, cada uma com propósito, custo e ciclo de vida próprios [23][22]:

**Memória de curto prazo (working memory)**: o conteúdo ativo da conversa — mensagens, observações, plano em execução — que vive na janela de contexto e morre ao fim da sessão. É a memória do loop (Capítulo 2). Barata de escrever, cara de manter (cada reenvio custa tokens), limitada pela janela. A decisão crítica: **o que fica na janela e o que é compactado** — o resumo da conversa é a técnica clássica para estender a janela sem estourar o custo [16].

**Memória de longo prazo (persistent memory)**: fatos que sobrevivem entre sessões — preferências do cliente, políticas, decisões. Vive em banco (vetorial ou relacional) e é recuperada seletivamente para o contexto. É o que o LangMem e o ecossistema de memória constroem [17][22]. A decisão crítica: **o que é digno de persistir** (nem tudo merece memória — persistir ruído polui a recuperação) e **como recuperar** (similaridade, não despejo).

**Memória episódica (episodic memory)**: o registro do que aconteceu — missões executadas, erros cometidos, resultados obtidos. É a base da melhoria contínua: sem memória episódica, o agente repete os mesmos erros; com ela, o sistema aprende com a própria operação [23]. A decisão crítica: **estrutura do registro** (evento, contexto, resultado, lição) para que a recuperação seja útil.

**Memória procedural (skills)**: o "como fazer" aprendido — workflows validados, melhores práticas descobertas. No estado da arte, a memória procedural é o próximo salto: agentes que codificam procedimentos bem-sucedidos para reutilização [23].

### O Problema da Recuperação

A qualidade da memória não está no acervo: está na recuperação. O sistema ideal recupera, para cada contexto, os fatos certos — nem mais, nem menos. Recuperar demais polui o contexto e degrada a resposta; recuperar de menos deixa o agente cego. O benchmark do ecossistema de memória mede exatamente isso: precisão da recuperação em cenários progressivos [22]. A lição prática: a memória é um sistema de busca, e a busca deve ser medida — o Capítulo 13 mostra como.

### O Ciclo da Memória

A memória opera em quatro momentos: **escrita** (o que o sistema decide lembrar), **indexação** (como o conteúdo é organizado para busca), **recuperação** (o que entra no contexto de cada iteração) e **revisão** (o que é atualizado ou esquecido). A maioria dos sistemas iniciantes implementa só a escrita — e esquece que memória sem recuperação seletiva é acervo morto, e memória sem revisão é acervo que envelhece mal [22].

## 3. Ilustra

### O Balcão de Atendimento da Padaria de Bairro

A padaria de bairro não usa ficha de clientes — usa a memória da dona. Ela lembra que o Sr. Carlos prefere o pão mais torrado (memória de longo prazo), lembra que hoje ele pediu o pão de forma às 7h (memória episódica da sessão) e aplica o procedimento de anotar pedidos por telefone (memória procedural). O balcão onde ela trabalha é a janela de contexto: o que está à vista na bancada é a memória de curto prazo — ela não precisa lembrar de cor o que está anotado no caderno do balcão.

A lição da padaria: a dona não anota tudo. Ela decide o que vale a pena lembrar (o gosto do cliente fiel, não o que o turista pediu uma vez), organiza (cada cliente tem sua "ficha mental"), recupera na hora certa (o gosto do Carlos entra na conversa quando ele chega) e atualiza (o Carlos mudou para integral — a memória antiga sai). Essa triagem é exatamente o ciclo escrever–indexar–recuperar–revisar que o sistema de memória do agente deve implementar [17][22].

```mermaid
%% legenda: o ciclo da memoria: escrever, indexar, recuperar e revisar
flowchart LR
  A[Escrever: decidir o que lembrar] --> B[Indexar: organizar para busca]
  B --> C[Recuperar: selecionar para o contexto]
  C --> D[Revisar: atualizar e esquecer]
  D --> A
```

### A Biblioteca sem Bibliotecária

A analogia inversa mostra o fracasso: a biblioteca sem bibliotecária. Todos os livros estão na estante (memória de longo prazo), mas não há catálogo (indexação), não há ninguém que recupere o livro certo (recuperação) e ninguém retira os volumes desatualizados (revisão). O leitor — o contexto do agente — caminha pela estante e pega livros aleatórios. Resultado: a biblioteca gigante é pior que a estante pequena e curada. É por isso que os benchmarks de memória avaliam a recuperação, não o tamanho do acervo: memória mal recuperada é pior que ausência de memória [22].

## 4. Técnica

### Memória de Curto Prazo com Compactação

A memória de curto prazo vive na janela de contexto. A técnica essencial é a **compactação**: quando a conversa cresce além do orçamento, o sistema resume o histórico antigo e mantém integral o recente:

```python
# memoria_curtoprazo.py — janela com compactacao de historico
from dataclasses import dataclass, field

@dataclass
class MemoriaCurtoPrazo:
    """Janela de contexto com compactacao automatica do historico antigo."""
    orcamento_mensagens: int = 10
    historico: list = field(default_factory=list)

    def adicionar(self, papel: str, conteudo: str) -> None:
        self.historico.append({"role": papel, "content": conteudo})
        self._compactar()

    def _compactar(self) -> None:
        """Se estourou o orcamento, resume o trecho mais antigo."""
        if len(self.historico) > self.orcamento_mensagens:
            antigas = self.historico[:-self.orcamento_mensagens]
            recentes = self.historico[-self.orcamento_mensagens:]
            # Resumo simples (no real: chamada LLM de sumarizacao)
            resumo = "RESUMO ANTERIOR: " + " ".join(
                m["content"][:60] for m in antigas)
            self.historico = [{"role": "system", "content": resumo}] + recentes

    def contexto(self) -> list:
        return self.historico

# Uso:
# janela = MemoriaCurtoPrazo(orcamento_mensagens=4)
# janela.adicionar("user", "O cliente quer o estoque do x-100")
# janela.adicionar("assistant", "Consultando...")
```

A compactação é a ponte entre a janela finita e as sessões longas: o resumo preserva o essencial e descarta o ruído — sempre com o cuidado de que o resumo não invente o que não foi dito (a sumarização por LLM deve ser instruída a ser fiel).

### Memória de Longo Prazo com Embeddings e Recuperação Vetorial

A memória de longo prazo do OrquestraIA usa banco vetorial: fatos viram vetores, e a recuperação encontra os mais similares à consulta. Implementamos com `sqlite` + similaridade de cosseno (com embeddings reais via API de embedding ou modelo local):

```python
# memoria_longoprazo.py — memória persistente vetorial com recuperação por cosseno
import sqlite3, math

class MemoriaVetorial:
    """Memoria de longo prazo: persistencia + embeddings + cosseno."""
    def __init__(self, caminho_db: str, gerar_embedding, dimensao: int = 384):
        self.con = sqlite3.connect(caminho_db)
        self.con.execute("""
            CREATE TABLE IF NOT EXISTS memorias (
                id INTEGER PRIMARY KEY,
                texto TEXT NOT NULL,
                categoria TEXT DEFAULT 'fato',
                vetor TEXT NOT NULL,
                criado_em TEXT DEFAULT CURRENT_TIMESTAMP
            )""")
        self.con.commit()
        self.gerar_embedding = gerar_embedding
        self.dimensao = dimensao

    def lembrar(self, texto: str, categoria: str = "fato") -> None:
        vetor = self.gerar_embedding(texto)
        self.con.execute(
            "INSERT INTO memorias (texto, categoria, vetor) VALUES (?, ?, ?)",
            (texto, categoria, repr(vetor)))
        self.con.commit()

    def _cosseno(self, a: list, b: list) -> float:
        return sum(x * y for x, y in zip(a, b)) / (
            math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)) or 1)

    def recuperar(self, consulta: str, topo: int = 3,
                  categoria: str = None) -> list:
        vetor_consulta = self.gerar_embedding(consulta)
        sql = "SELECT texto, categoria, vetor FROM memorias"
        if categoria:
            sql += " WHERE categoria = ?"
            linhas = self.con.execute(sql, (categoria,)).fetchall()
        else:
            linhas = self.con.execute(sql).fetchall()
        pontuadas = []
        for texto, cat, vetor_txt in linhas:
            vetor = eval(vetor_txt)  # no real: deserialize com json/safetensors
            pontuadas.append((self._cosseno(vetor_consulta, vetor), texto))
        pontuadas.sort(reverse=True, key=lambda x: x[0])
        return [t for _, t in pontuadas[:topo]]

# Uso (com embeddings reais):
# def embed(t): 
#     return modelo.encode(t).tolist()  # ex.: sentence-transformers
# memoria = MemoriaVetorial("orquestraia.db", embed)
# memoria.lembrar("Cliente Maria prefere contato por e-mail", "preferencia")
# memoria.lembrar("Pedido P-7841 atrasou por extravio na transportadora", "caso")
# print(memoria.recuperar("como prefere ser contatada a maria", topo=2))
```

Três decisões de engenharia aparecem: **categoria** (a memória é particionável — preferências, casos, políticas — o que melhora a precisão da recuperação), **representação do vetor** (serielizada; a leitura com `eval` é didática — em produção use JSON ou coluna BLOB), e **pontuação por cosseno com fallback** (a divisão por zero protegida).

### Memória Episódica: O Diário de Bordo

A memória episódica registra o que aconteceu — a matéria-prima da melhoria contínua. Estrutura: evento, contexto, resultado e lição:

```python
# memoria_episodica.py — registro episodico para melhoria continua
import sqlite3, time

class MemoriaEpisodica:
    """Diario de bordo: registra missoes, resultados e licoes."""
    def __init__(self, caminho_db: str):
        self.con = sqlite3.connect(caminho_db)
        self.con.execute("""
            CREATE TABLE IF NOT EXISTS episodios (
                id INTEGER PRIMARY KEY,
                timestamp TEXT, missao TEXT, resultado TEXT,
                licao TEXT DEFAULT '', sucesso INTEGER
            )""")
        self.con.commit()

    def registrar(self, missao: str, resultado: str, sucesso: bool,
                  licao: str = "") -> None:
        self.con.execute(
            "INSERT INTO episodios (timestamp, missao, resultado, sucesso, licao)"
            " VALUES (?, ?, ?, ?, ?)",
            (time.strftime("%Y-%m-%d %H:%M:%S"), missao, resultado,
             int(sucesso), licao))
        self.con.commit()

    def licoes_recentes(self, topo: int = 5) -> list:
        """Recupera as licoes aprendidas — base de revisao do sistema."""
        rows = self.con.execute(
            "SELECT missao, licao FROM episodios WHERE licao != ''"
            " ORDER BY id DESC LIMIT ?", (topo,)).fetchall()
        return [f"{m}: {l}" for m, l in rows]

# Uso:
# diario = MemoriaEpisodica("orquestraia.db")
# diario.registrar("atender pedido P-7841", "resolvido com reposicao",
#                  True, "extravio exige acionar reposicao imediatamente")
```

A memória episódica é o elo com o Capítulo 20: é dela que saem as lições que alimentam a evolução do sistema — o agente que registra lições e as consulta na próxima missão parecida.

### Checklist de Memória

- [ ] Curto prazo: janela com **compactação** do histórico antigo?
- [ ] Longo prazo: persistência com **categorias** e recuperação por similaridade?
- [ ] Episódica: registro estruturado com **lição** e resultado para melhoria contínua?
- [ ] Recuperação **selecionada** por orçamento e relevância (nunca despejo)?
- [ ] Política de **revisão**: o que é atualizado e o que é esquecido?

## 5. Aplica

### A Memória no Chão de Fábrica

A memória de longo prazo é o que transforma atendimento em relacionamento: agentes que lembram preferências entre sessões entregam satisfação que chatbots amnésicos não alcançam [27][10]. A memória episódica é o que transforma operação em aprendizado: sistemas que registram erros e lições melhoram com o tempo, enquanto sistemas amnésicos repetem os mesmos erros [23]. E a memória bem particionada por categoria reduz o custo: recuperar só a categoria certa custa menos tokens e melhora a precisão [22].

A confiança — o gargalo da adoção agêntica — também passa pela memória: um sistema que lembra o que foi prometido, registra o que foi feito e pode auditar o que aconteceu inspira mais confiança do que um que recomeça do zero a cada sessão [21].

### Armadilhas Comuns

1. **Memória como despejo**: persistir tudo e recuperar tudo. O acervo gigante sem seleção degrada a resposta — curadoria é parte da memória.
2. **Sem memória episódica**: o sistema nunca aprende com a própria operação — cada erro é a primeira vez.
3. **Compactação que inventa**: resumos de LLM sem instrução de fidelidade podem criar fatos falsos. Instrua a sumarização a não inventar.
4. **Sem política de revisão**: a memória que nunca esquece fica obsoleta — políticas antigas, preferências mudadas e decisões revogadas poluem a recuperação.

### Conexão com o OrquestraIA

A memória do OrquestraIA reúne as três camadas: `MemoriaCurtoPrazo` dentro de cada agente (Capítulo 2), `MemoriaVetorial` compartilhada entre especialistas (preferências e políticas) e `MemoriaEpisodica` como diário de bordo da operação — consumidas pelo `ConstrutorContexto` do Capítulo 5 e medidas pelos evals do Capítulo 13.

### Aprofundamento: A Política de Revisão e Esquecimento

A memória que nunca esquece envelhece mal — e a política de revisão é a parte mais negligenciada do sistema de memória. A prática recomendada tem quatro regras: **expiração por categoria** (preferências têm validade curta — o cliente pode mudar de opinião; políticas têm validade longa — mas ambas expiram, com tempos diferentes), **confirmação antes de persistir** (fatos de alto impacto — dados do cartão, decisões legais — exigem confirmação humana ou de fonte confiável antes de entrar na memória), **revisão periódica do acervo** (o processo do Capítulo 19 que audita o que está armazenado, removendo o obsoleto e o contraditório) e **rastro de origem** (cada fato registra de onde veio e quando — o material da auditoria do Capítulo 16) [22].

A implementação da política cabe no ciclo que o capítulo já apresentou: a fase de **revisar** ganha regras explícitas:

```python
# revisao_memoria.py — politica de expiracao e revisao do acervo
import sqlite3, time

class MemoriaComRevisao:
    """Memoria de longo prazo com expiracao por categoria e rastro."""
    VALIDADES = {"preferencia": 90, "politica": 365, "caso": 180}

    def __init__(self, caminho_db: str):
        self.con = sqlite3.connect(caminho_db)
        self.con.execute("""CREATE TABLE IF NOT EXISTS memorias (
            id INTEGER PRIMARY KEY, texto TEXT, categoria TEXT,
            origem TEXT, criado_em REAL, expira_em REAL)""")
        self.con.commit()

    def lembrar(self, texto: str, categoria: str, origem: str) -> None:
        agora = time.time()
        validade = self.VALIDADES.get(categoria, 180) * 86400
        self.con.execute(
            "INSERT INTO memorias (texto, categoria, origem, criado_em, expira_em)"
            " VALUES (?, ?, ?, ?, ?)",
            (texto, categoria, origem, agora, agora + validade))
        self.con.commit()

    def revisar(self) -> dict:
        """Remove o expirado e conta o que restou por categoria."""
        agora = time.time()
        removidos = self.con.execute(
            "DELETE FROM memorias WHERE expira_em < ?", (agora,)).rowcount
        contagem = self.con.execute(
            "SELECT categoria, COUNT(*) FROM memorias GROUP BY categoria").fetchall()
        return {"removidos": removidos, "por_categoria": dict(contagem)}

    def recuperar(self, consulta: str, topo: int = 3) -> list:
        linhas = self.con.execute(
            "SELECT texto FROM memorias ORDER BY expira_em DESC").fetchall()
        def pontuar(t):
            return sum(1 for p in consulta.lower().split() if p in t[0].lower())
        return [r[0] for r in sorted(linhas, key=pontuar, reverse=True)[:topo]]
```

A política de revisão fecha o ciclo da memória: sem ela, o acervo cresce com ruído e contradição, e a recuperação piora exatamente quando o sistema mais precisa dela — depois de meses de operação. A memória que revisa é a memória que sustenta a evolução do Capítulo 19 [22].

### Aprofundamento: A Memória Compartilhada entre Especialistas

O OrquestraIA é multiagente — e a memória tem uma decisão de arquitetura que os sistemas de um agente não enfrentam: **a memória é por agente ou compartilhada?** A prática recomendada é uma combinação deliberada: cada especialista tem a sua memória de **trabalho** (o estado da sessão atual — privado do agente, porque a sessão é dele) e todos compartilham a memória de **longo prazo** (os fatos do cliente, as políticas, as lições — públicas, porque qualquer especialista precisa delas) [22][1]. A partilha tem três regras: **escrita por categoria** (o especialista de vendas escreve na categoria de vendas; o de suporte, na de suporte — a categorização do Capítulo 6 é o que torna a partilha ordenada), **leitura seletiva** (cada especialista recupera a categoria do seu domínio — o atendente não precisa dos dados de pipeline de vendas na janela) e **conflito resolvido por autoridade** (o fato contraditório entre categorias é resolvido pela fonte de autoridade — a política vence a preferência; o Capítulo 14 define a hierarquia). A memória compartilhada é o que torna o multiagente coeso: o cliente que falou com o atendente ontem é reconhecido pelo vendedor hoje — o relacionamento atravessa os especialistas [1][22].

### O Orçamento de Memória: Quanto Lembrar Custa

A memória tem um custo que o Capítulo 16 mede e que aqui merece o desenho: **cada token de memória recuperado paga o preço do contexto** — e o orçamento de memória é a disciplina que mantém o custo sob controle sem perder a qualidade da recuperação. O orçamento tem três números: o **teto por recuperação** (o número máximo de fatos que entram no contexto por chamada — o `topo` do Capítulo 6, calibrado pela precisão do Capítulo 13), o **teto por sessão** (o custo total de memória da sessão — a compactação do Capítulo 6 mantém o histórico no orçamento) e o **teto por período** (o custo de memória do sistema por dia — o alerta de deriva do Capítulo 16 detecta o crescimento). A regra de ouro do orçamento: **recupere o mínimo que mantém a qualidade** — a precisão da recuperação medida (Capítulo 13) é o juiz de onde está o mínimo, e o orçamento é o que impede o excesso de degradar a resposta e o custo ao mesmo tempo [16][22].

## 6. Conclusão

Três pontos para levar: **primeiro**, a memória é um sistema em camadas — curto prazo na janela, longo prazo em banco vetorial, episódica como diário — e cada camada tem decisões de engenharia próprias. **Segundo**, a qualidade da memória está na recuperação seletiva, não no tamanho do acervo: recuperar errado é pior que não recuperar. **Terceiro**, o ciclo completo — escrever, indexar, recuperar, revisar — é o que transforma o agente de amnésico eloquente em sistema que aprende, com a memória episódica como base da evolução contínua.

O próximo capítulo dá as mãos ao agente: **ferramentas e function calling** — o contrato, a validação, a execução segura e a conexão com o mundo real via APIs, que transforma o agente de pensador em executor.

**Desafio opcional**: implemente a `MemoriaVetorial` com embeddings reais (ex.: `sentence-transformers` ou a API de embeddings do seu provedor) e carregue 30 fatos do seu domínio. Meça a precisão da recuperação em 10 perguntas com `topo` variando de 1 a 5. Depois, adicione a categoria e repita — o ganho de precisão é a sua evidência de que particionar compensa.

## 7. Referências

[1] ADIMULAM, A.; GUPTA, R.; KUMAR, S. *The Orchestration of Multi-Agent Systems: Architectures, Protocols, and Enterprise Adoption*. arXiv:2601.13671v1, 2026. Disponível em: https://arxiv.org/html/2601.13671v1. Acesso em: 07 ago. 2026.

[2] AMAZON WEB SERVICES (AWS). *Traditional agent architecture: perceive, reason, act*. AWS Prescriptive Guidance: Foundations of Agentic AI on AWS, 2026. Disponível em: https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-foundations/traditional-agents.html. Acesso em: 07 ago. 2026.

[3] ANTHROPIC. *Building Effective Agents*. 2024. Disponível em: https://www.anthropic.com/engineering/building-effective-agents. Acesso em: 07 ago. 2026.

[4] ANTHROPIC. *Demystifying Evals for AI Agents*. 2026. Disponível em: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents. Acesso em: 07 ago. 2026.

[5] DIGITAL APPLIED. *State of AI Agents 2026: 200+ Data Points Compiled*. 2026. Disponível em: https://www.digitalapplied.com/blog/state-of-ai-agents-2026-200-data-points. Acesso em: 07 ago. 2026.

[6] FIN.AI. *AI Agent ROI: Customer Support Returns*. 2026. Disponível em: https://fin.ai/blog/ai-agent-roi-customer-support. Acesso em: 07 ago. 2026.

[7] GALILEO. *How to Build Human-in-the-Loop Oversight for Production AI Agents*. 2026. Disponível em: https://galileo.ai/blog/human-in-the-loop-agent-oversight. Acesso em: 07 ago. 2026.

[8] GARTNER. *Gartner Predicts 40% of Enterprise Apps Will Feature Task-Specific AI Agents by 2026*. 2025. Disponível em: https://www.gartner.com/en/newsroom/press-releases/2025-08-26-gartner-predicts-40-percent-of-enterprise-apps-will-feature-task-specific-ai-agents-by-2026-up-from-less-than-5-percent-in-2025. Acesso em: 07 ago. 2026.

[9] GOOGLE CLOUD. *Choose a Design Pattern for Your Agentic AI System*. Cloud Architecture Center, 2026. Disponível em: https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system. Acesso em: 07 ago. 2026.

[10] GUO, Taicheng et al. *Large Language Model based Multi-Agents: A Survey of Progress and Challenges*. IJCAI, 2024. Disponível em: https://arxiv.org/abs/2402.01680. Acesso em: 07 ago. 2026.

[11] HONG, Sirui et al. *MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework*. ICLR, 2024. Disponível em: https://arxiv.org/abs/2308.00352. Acesso em: 07 ago. 2026.

[12] LANGCHAIN TEAM. *Context Engineering for Agents*. 2025. Disponível em: https://www.langchain.com/blog/context-engineering-for-agents. Acesso em: 07 ago. 2026.

[13] LANGCHAIN TEAM. *LangMem SDK for Agent Long-Term Memory*. 2025. Disponível em: https://www.langchain.com/blog/langmem-sdk-launch. Acesso em: 07 ago. 2026.

[14] LANGCHAIN. *The Best AI Agent Frameworks in 2026*. 2026. Disponível em: https://www.langchain.com/resources/ai-agent-frameworks. Acesso em: 07 ago. 2026.

[15] LIU, Xiao et al. *AgentBench: Evaluating LLMs as Agents*. ICLR, 2025. Disponível em: https://arxiv.org/abs/2308.03688. Acesso em: 07 ago. 2026.

[16] MCKINSEY & COMPANY. *State of AI Trust in 2026: Shifting to the Agentic Era*. 2026. Disponível em: https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/tech-forward/state-of-ai-trust-in-2026-shifting-to-the-agentic-era. Acesso em: 07 ago. 2026.

[17] MEM0 ENGINEERING TEAM. *AI Agent Memory 2026: Progress Benchmark Report Evaluations*. 2026. Disponível em: https://mem0.ai/blog/state-of-ai-agent-memory-2026. Acesso em: 07 ago. 2026.

[18] MICROSOFT AZURE ARCHITECTURE CENTER. *AI Agent Orchestration Patterns*. 2026. Disponível em: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns. Acesso em: 07 ago. 2026.

[19] ORACLE DEVELOPERS. *What Is the AI Agent Loop? The Core Architecture Behind Autonomous AI Systems*. 2026. Disponível em: https://blogs.oracle.com/developers/what-is-the-ai-agent-loop-the-core-architecture-behind-autonomous-ai-systems. Acesso em: 07 ago. 2026.

[20] QIAN, Chen et al. *ChatDev: Communicative Agents for Software Development*. ACL, 2024. Disponível em: https://arxiv.org/abs/2307.07924. Acesso em: 07 ago. 2026.

[21] SALESFORCE. *New Research: AI Service Agents Improve Customer Satisfaction*. 2026. Disponível em: https://www.salesforce.com/news/stories/ai-service-agents-improve-customer-satisfaction/. Acesso em: 07 ago. 2026.

[22] VALIDMIND. *Top 10 AI Risk Trends for 2026*. 2026. Disponível em: https://validmind.com/blog/10-ai-risk-trends-for-2026/. Acesso em: 07 ago. 2026.

[23] WANG, Lei et al. *A Survey on Large Language Model based Autonomous Agents*. arXiv:2308.11432, 2025. Disponível em: https://arxiv.org/abs/2308.11432. Acesso em: 07 ago. 2026.

[24] XI, Zhiheng et al. *The Rise and Potential of Large Language Model Based Agents: A Survey*. arXiv:2309.07864, 2023. Disponível em: https://arxiv.org/abs/2309.07864. Acesso em: 07 ago. 2026.

[25] YAO, Shunyu et al. *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR, 2023. Disponível em: https://arxiv.org/abs/2210.03629. Acesso em: 07 ago. 2026.

[26] ZENITY. *What Is the Model Context Protocol? Full Guide*. 2026. Disponível em: https://zenity.io/academy/model-context-protocol-explained. Acesso em: 07 ago. 2026.

[27] DORA / GOOGLE CLOUD. *DORA: State of AI-assisted Software Development 2025*. 2025. Disponível em: https://dora.dev/dora-report-2025/. Acesso em: 07 ago. 2026.

[28] BRAINTRUST. *AI Gateway Comparison: The 6 Best Ranked (2026)*. 2026. Disponível em: https://www.braintrust.dev/articles/ai-gateway-comparison-2026. Acesso em: 07 ago. 2026.

[29] CERBOS. *AI Agents, the Model Context Protocol, and the Future of Authorization Guardrails*. 2026. Disponível em: https://www.cerbos.dev/news/securing-ai-agents-model-context-protocol. Acesso em: 07 ago. 2026.

[30] COALITION FOR SECURE AI (CoSAI). *Securing the AI Agent Revolution: A Practical Guide to Model Context Protocol Security*. 2026. Disponível em: https://www.coalitionforsecureai.org/securing-the-ai-agent-revolution-a-practical-guide-to-mcp-security/. Acesso em: 07 ago. 2026.
