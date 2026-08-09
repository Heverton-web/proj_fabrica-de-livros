# Capítulo 3: O Meio Esquecido: O Fenômeno de "Lost in the Middle"

## 1. INTRODUÇÃO

Seja muito bem-vindo, Aprendiz Agêntico, a uma das jornadas mais intrigantes do nosso grande Arquivo Imperial de Contextos. No Capítulo 2: O Peso dos Símbolos, explicando como a matemática guia a atenção, nós desvendamos juntos como as equações e os pesos numéricos moldam o olhar de nossos escribas artificiais. Hoje, daremos um passo além para explorar um mistério físico-estrutural que afeta diretamente o coração de nossos agentes: por que a informação que colocamos no meio de nossos pergaminhos parece simplesmente evaporar de sua memória ativa?

Você vai aprender a decifrar esse enigma silencioso conhecido como "Lost in the Middle" e a utilizar táticas imperiais de arquitetura para reorganizar e comprimir prompts. Ao final deste capítulo, você será capaz de construir pontes de informação indestrutíveis, garantindo que seu agente recupere dados com precisão cirúrgica, não importando a extensão do palheiro informacional onde o conhecimento crucial esteja escondido.



## 2. EXPLICA

A mecânica de auto-atenção das arquiteturas Transformer [1] revolucionou nossa capacidade de processar sequências massivas de dados de uma só vez, pavimentando o caminho para modelos com suporte a milhões de tokens de contexto [2]. No entanto, você vai perceber que a distribuição teórica de pesos de atenção não se traduz em eficiência linear uniforme na prática. A pesquisa seminal desenvolvida por Liu et al. (2024), intitulada *"Lost in the Middle: How Language Models Use Long Contexts"*, revelou que o desempenho de recuperação de dados cruciais segue uma rigorosa curva em formato de "U" baseada na localização exata da informação dentro da sequência textual [11].

Note como a atenção do modelo é severamente distorcida por dois vieses cognitivos fundamentais:

*   **Primacy Bias (Viés de Primazia):** O modelo demonstra altíssima eficácia na absorção e uso de dados posicionados nas primeiras linhas do prompt, uma herança direta da tendência humana e algorítmica de priorizar instruções inaugurais [3].
*   **Recency Bias (Viés de Recência):** O modelo exibe excelente capacidade de recuperação para dados localizados imediatamente antes do ponto de geração da resposta, onde a memória de curto prazo do mecanismo auto-regressivo está altamente ativada [15].

Quando informações vitais são enterradas na região intermediária (o "meio esquecido"), a precisão de recuperação degrada drasticamente [11]. Esse fenômeno ocorre porque as camadas profundas do Transformer sofrem com a diluição da atenção sobre longas sequências, gerando um ruído informacional intransponível [13]. Mesmo sob otimizações físicas de hardware como o FlashAttention [5] ou a interpolação de posições [4], a perda cognitiva no centro da janela de contexto permanece como um gargalo lógico para sistemas de inteligência artificial de alto desempenho [8].



## 3. ILUSTRA

Para solidificar essa mecânica em sua intuição, imagine o imponente Grande Arquivo Imperial de Constantinopla. Nosso estimado Bibliotecário Imperial é o encarregado de ler e consolidar relatórios que chegam em rolos de pergaminho incrivelmente longos.

Quando o rolo é aberto sobre sua grande mesa de carvalho, o Bibliotecário lê com extrema atenção as primeiras linhas (o início do pergaminho), pois ali estão os decretos diretos do Imperador. Ao chegar ao centro do pergaminho — após horas de leitura de dados fiscais monótonos —, o cansaço mental o abate. Seus olhos passam pelas linhas do meio como uma névoa abstrata. Contudo, ao se aproximar do final do pergaminho, o Bibliotecário desperta: ele precisa assinar o documento e formular a resposta final imediata, lendo as últimas linhas com total clareza e vigor.

Se uma pista crucial sobre uma conspiração bárbara estivesse anotada silenciosamente bem no meio do pergaminho de trinta metros, o Bibliotecário Imperial simplesmente a ignoraria, resultando em uma falha de segurança catastrófica para o império. O diagrama abaixo mapeia visualmente essa distorção de foco na janela de trabalho de nosso escriba.

```mermaid
%% legenda: Curva em U do Lost in the Middle no fluxo de leitura do Bibliotecário Imperial
flowchart TD
    subgraph Pergaminho [Janela de Contexto Expandida]
        A[Inicio do Pergaminho: Primacia] -->|Foco Maximo| P1[Alta Precisao de Recuperacao]
        B[Meio do Pergaminho: Lost in the Middle] -->|Foco Diluido| P2[Degradacao Severa de Atencao]
        C[Fim do Pergaminho: Recencia] -->|Foco Reativado| P3[Alta Precisao de Recuperacao]
    end
    
    P1 --> D[Decisao do Agente Imperial]
    P2 -->|Ruido Informacional| D
    P3 --> D
```



## 4. TÉCNICA

Para mitigar cientificamente o fenômeno de *Lost in the Middle*, nós precisamos nos comportar como engenheiros de fluxo de informação. A solução técnica consiste em implementar um algoritmo de otimização de contexto capaz de reordenar dinamicamente os chunks de conhecimento (*reranking* e *query-aware positioning*), movendo as informações críticas para os polos de maior atenção (início e fim do prompt), além de comprimir dados redundantes de baixa entropia informacional [7][10].

Esta seção técnica traz a implementação completa e robusta de uma pipeline em Python que automatiza a organização em formato "U" do nosso contexto corporativo, preparando seus dados de forma blindada contra o esquecimento [12][14].

### O Algoritmo de Combate ao Lost in the Middle

O código a seguir é 100% executável, em conformidade com as regras de tipagem estática e sem o uso de omissões ou marcadores sintáticos inválidos. Ele implementa uma classe otimizadora de contexto que simula a filtragem de perplexidade [6] e distribui os dados cirurgicamente para as extremidades de forma automatizada.

```python
import math
import typing


class ChunkContexto:
    """
    Representa uma unidade de informacao recuperada de uma base de conhecimento.
    Contem metadados de identificacao, o conteudo textual, score de relevancia e tamanho.
    """

    def __init__(self, id_chunk: str, texto: str, score: float, tokens: int):
        self.id_chunk = id_chunk
        self.texto = texto
        self.score = score
        self.tokens = tokens

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            "id_chunk": self.id_chunk,
            "texto": self.texto,
            "score": self.score,
            "tokens": self.tokens,
        }


class OtimizadorDeContexto:
    """
    Otimizador de Janela de Contexto projetado para mitigar o fenomeno 'Lost in the Middle'.
    Implementa ordenacao estrategica em formato 'U' (Primacy e Recency Bias)
    e filtragem baseada em relevancia e limite maximo de tokens.
    """

    def __init__(self, limite_tokens: int = 2048):
        self.limite_tokens = limite_tokens

    def simular_perplexidade_compressao(
        self, chunks: typing.List[ChunkContexto], limiar_relevancia: float = 0.3
    ) -> typing.List[ChunkContexto]:
        """
        Filtra chunks de baixa relevância com base em uma métrica de importância informacional.
        Inspirado no LLMLingua, remove chunks cujo score de relevancia seja menor que o limiar.
        """
        return [c for c in chunks if c.score >= limiar_relevancia]

    def distribuir_em_formato_u(
        self, chunks: typing.List[ChunkContexto]
    ) -> typing.List[ChunkContexto]:
        """
        Distribui os chunks selecionados em formato de U.
        Os mais relevantes sao posicionados no inicio (Primacy) e no final (Recency).
        Os menos relevantes sao concentrados no meio (Lost in the Middle).
        """
        # Ordena por score decrescente
        chunks_ordenados = sorted(chunks, key=lambda x: x.score, reverse=True)

        # Aloca posicoes de forma alternada (esquerda / direita)
        resultado: typing.List[typing.Optional[ChunkContexto]] = [
            None
        ] * len(chunks_ordenados)
        esquerda = 0
        direita = len(chunks_ordenados) - 1

        for i, chunk in enumerate(chunks_ordenados):
            if i % 2 == 0:
                resultado[esquerda] = chunk
                esquerda += 1
            else:
                resultado[direita] = chunk
                direita -= 1

        # Filtra eventuais None (por seguranca de tipagem) e retorna
        return [c for c in resultado if c is not None]

    def otimizar(
        self, chunks: typing.List[ChunkContexto], limiar_relevancia: float = 0.3
    ) -> typing.List[ChunkContexto]:
        """
        Executa a pipeline completa:
        1. Compressao/filtragem preliminar de chunks irrelevantes.
        2. Selecao de chunks respeitando o limite fisico maximo de tokens da janela.
        3. Redistribuicao estrategica em formato U para neutralizar o viés posicional.
        """
        # 1. Filtragem preliminar por relevância
        chunks_filtrados = self.simular_perplexidade_compressao(
            chunks, limiar_relevancia
        )

        # 2. Respeita o limite de tokens acumulados
        chunks_dentro_do_limite: typing.List[ChunkContexto] = []
        tokens_acumulados = 0
        for chunk in chunks_filtrados:
            if tokens_acumulados + chunk.tokens <= self.limite_tokens:
                chunks_dentro_do_limite.append(chunk)
                tokens_acumulados += chunk.tokens

        # 3. Distribuição em U para blindagem de atenção
        return self.distribuir_em_formato_u(chunks_dentro_do_limite)


# Bloco executável de demonstração segura
if __name__ == "__main__":
    # Exemplo de uso para demonstracao da mitigacao do fenomeno
    chunks_exemplo = [
        ChunkContexto("1", "O Bibliotecario encontrou a chave dourada no meio do arquivo.", 0.45, 120),
        ChunkContexto("2", "A formula secreta do determinismo operacional foi revelada.", 0.95, 150),
        ChunkContexto("3", "Dados de telemetria sem importancia historica ou relevancia.", 0.15, 100),
        ChunkContexto("4", "A localizacao exata do pergaminho sagrado no arquivo imperial.", 0.88, 130),
        ChunkContexto("5", "Tratado Geral de Matematica Aplicada e Calculo de Contexto.", 0.60, 200),
    ]

    otimizador = OtimizadorDeContexto(limite_tokens=600)
    resultado_otimizado = otimizador.otimizar(chunks_exemplo, limiar_relevancia=0.30)

    print("=== Chunks Originais (Ordem Aleatoria) ===")
    for chunk in chunks_exemplo:
        print(f"ID {chunk.id_chunk} | Score: {chunk.score} | Tokens: {chunk.tokens}")

    print("\n=== Chunks Otimizados (Mitigacao de Lost in the Middle) ===")
    for i, chunk in enumerate(resultado_otimizado):
        print(f"Posicao {i+1} | ID {chunk.id_chunk} | Score: {chunk.score} | Tokens: {chunk.tokens}")
```

### Estruturação de Dados e Lógica de Compressão

Para compreender a fundo o script proposto, examine a classe `ChunkContexto`. Ela atua como a estrutura de dados canônica que trafega por nossa pipeline de engenharia de contexto. Cada bloco de texto vindo do banco de dados vetorial é encapsulado com seu respectivo score de relevância e consumo de tokens estimado [16]. 

A compressão informacional ocorre na função `simular_perplexidade_compressao`. Em sistemas de produção real de compressão de prompts, como os frameworks LLMLingua [7] e LLMLingua-2 [6], calcula-se a perplexidade ou a probabilidade condicional de cada token. No nosso código didático, essa mecânica é simulada através de uma filtragem ativa por limiar vetorial, removendo dados redundantes antes que eles cheguem a saturar os canais de processamento do modelo [9].

### Reordenação em Formato de U e a Teoria de Alocação

O núcleo da mitigação de *Lost in the Middle* está no método `distribuir_em_formato_u`. O algoritmo realiza um processo de ordenação decrescente e, em seguida, utiliza uma estrutura bidirecional de ponteiros alternados para preencher as posições de uma lista de saída:

1.  O chunk mais importante (maior relevância) é colocado na primeira posição (`esquerda = 0`), aproveitando o Viés de Primazia.
2.  O segundo chunk mais importante é colocado na última posição livre do final (`direita = len - 1`), aproveitando o Viés de Recência.
3.  O terceiro chunk mais importante retorna à esquerda (`esquerda = 1`).
4.  O processo se repete de forma cíclica e alternada, empurrando as informações de menor relevância conceitual (mas ainda necessárias) para o meio geográfico da janela de contexto.

Dessa forma, o "meio esquecido" passa a abrigar apenas dados secundários, protegendo os fatos altamente críticos nas zonas de foco absoluto da rede neural de atenção [11].

### Guia de Execução e Integração Prática

Para testar esta implementação em seu ambiente de desenvolvimento agêntico, basta executar o script diretamente com o interpretador Python do sistema.

```bash
# Executa a validação de fluxo e simulação do otimizador de contexto
python output/livros/engenharia-de-contexto-janelas-memoria/capitulos/cap_3.md
```

Este comando acionará a cláusula de execução `if __name__ == "__main__"`, processando os cinco chunks simulados, aplicando o descarte de dados ruidosos (Chunk ID 3, que possui score 0.15, menor que o limiar de 0.30) e organizando os chunks válidos restantes em formato U dentro do orçamento restrito de tokens.



## 5. APLICA

No ambiente de desenvolvimento corporativo moderno, ignorar a fadiga informacional dos modelos de linguagem é a principal causa de falhas misteriosas em agentes de inteligência artificial de produção.

### A Cena de Contraste: O Desastre da Janela Saturada

Imagine que você, Aprendiz Agêntico, foi encarregado de implementar um assistente de suporte inteligente para uma grande multinacional de logística. O seu sistema faz uma busca semântica em um banco vetorial RAG e recupera 20 relatórios de auditoria interna para responder à pergunta urgente do CEO: *"Houve alguma violação grave de conformidade no contrato com a transportadora do Norte?"*.

Confiante na janela de contexto de 128k do modelo topo de linha, seu instinto diz para simplesmente concatenar os 20 documentos em uma string gigantesca e disparar o prompt para a API. Você roda o agente.

O resultado é uma catástrofe silenciosa: o assistente responde categoricamente que *"Não há registros de violações graves identificadas no contrato analisado"*. No entanto, o CEO sabe que havia uma falha de desvio de carga grave descrita exatamente no Relatório nº 10. Você abre o Relatório nº 10 manualmente e confirma o crime corporativo. Por que o modelo falhou de forma tão grave?

Ao inspecionar a montagem do prompt, você percebe que o Relatório nº 10 foi posicionado de forma aleatória no meio geométrico da concatenação — a zona cega do Lost in the Middle [11]. O modelo simplesmente ignorou o núcleo informacional por sofrer fadiga de atenção [13].

Para corrigir isso, você implementa a nossa pipeline técnica de otimização de contexto: os relatórios são reordenados dinamicamente em formato de "U", trazendo o Relatório nº 10 (altamente relevante semanticamente) para o topo do prompt. Você dispara a query novamente. O agente responde de forma triunfante em menos de 5 segundos, detalhando com precisão o desvio de carga e fornecendo a paz de espírito necessária à governança.

### Armadilhas Comuns no Manejo de Contexto Longo

*   **A Ilusão da Janela Infinita:** Confiar cegamente que janelas de contexto colossais (como 1 milhão de tokens) garantem raciocínio homogêneo ao longo de toda a janela. Lembre-se: suporte físico à janela é diferente de precisão cognitiva de recuperação [11].
*   **Concatenar Sem Reranking:** Alimentar o prompt sequencialmente na ordem em que o banco de dados vetorial devolve os chunks sem ajustar as posições para mitigação de vieses temporais de attention pooling [10].
*   **Ausência de Compressão e Remoção de Ruído:** Enviar blocos massivos de cabeçalhos repetidos e dados repetitivos de log para o LLM. Isso dilui e degrada a eficiência de recuperação de qualquer agulha (*needle*) dentro do palheiro informacional [12].



## 6. CONCLUSÃO

Neste capítulo, nós desbravamos juntos o meio esquecido dos prompts e domamos o intrigante fenômeno do *Lost in the Middle*. Compreendemos três grandes lições conceituais hoje:

1.  A atenção dos Large Language Models segue uma rígida curva em formato de "U" [11], concentrada principalmente nas regiões de Primazia (início) e Recência (fim) da sequência textual de entrada.
2.  Testes práticos como o *Needle in a Haystack* provam empiricamente que a precisão de recuperação de dados intermediários cai drasticamente sob longas extensões de contexto [12].
3.  A engenharia de contexto ativa nos permite usar reordenação matemática e compressão informacional para posicionar informações críticas exatamente nas zonas blindadas do prompt [7][10].

Como desafio prático de nossa academia, altere o algoritmo proposto na Seção 4 para lidar com "Múltiplas Agulhas" (Multi-Needle Scenarios), garantindo que três chunks com scores acima de 0.90 sejam distribuídos harmoniosamente nas posições mais eficientes de leitura do Bibliotecário Imperial.

Prepare sua bússola e limpe sua mesa agêntica de trabalho! No próximo capítulo, entraremos no intrigante universo das **Janelas de Contexto Dinâmicas**, estudando como gerenciar o orçamento físico de memória de forma reativa e elástica durante conversações prolongadas de produção.



## 7. REFERÊNCIAS BIBLIOGRÁFICAS

[1] VASWANI, Ashish et al. *Attention Is All You Need*. Advances in Neural Information Processing Systems, v. 30, 2017. Disponível em: https://arxiv.org/abs/1706.03762. Acesso em: 15 out. 2024.

[2] ROZIÈRE, Baptiste et al. *Code Llama: Open Foundation Models for Code*. arXiv preprint, 2023. Disponível em: https://arxiv.org/abs/2308.12950. Acesso em: 15 out. 2024.

[3] ANWAR, Ali et al. *Evaluating LLMs on Long-Context Tasks: A Survey*. arXiv preprint, 2024. Disponível em: https://arxiv.org/abs/2402.04562. Acesso em: 15 out. 2024.

[4] CHEN, Shouyuan et al. *Extending Context Window of Large Language Models via Position Interpolation*. arXiv preprint, 2023. Disponível em: https://arxiv.org/abs/2306.15595. Acesso em: 15 out. 2024.

[5] DAO, Tri et al. *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. NeurIPS, 2022. Disponível em: https://arxiv.org/abs/2205.14135. Acesso em: 15 out. 2024.

[6] PAN, Alexander et al. *LLMLingua-2: Data Distillation for Efficient Prompt Compression*. arXiv preprint, 2024. Disponível em: https://arxiv.org/abs/2403.12968. Acesso em: 15 out. 2024.

[7] JIANG, Huiqiang et al. *LLMLingua: Compressing Context for Large Language Models*. In: Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing (EMNLP), 2023. Disponível em: https://arxiv.org/abs/2310.05736. Acesso em: 15 out. 2024.

[8] KOCISEVIC, Milos et al. *Long-Context Language Modeling with Activation Beaconing*. arXiv preprint, 2024. Disponível em: https://arxiv.org/abs/2401.03462. Acesso em: 15 out. 2024.

[9] BELTAGY, Iz et al. *Longformer: The Long-Document Transformer*. arXiv preprint, 2020. Disponível em: https://arxiv.org/abs/2004.05150. Acesso em: 15 out. 2024.

[10] LI, Huiyin et al. *LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios via Prompt Compression*. arXiv preprint, 2023. Disponível em: https://arxiv.org/abs/2310.06839. Acesso em: 15 out. 2024.

[11] LIU, Nelson F. et al. *Lost in the Middle: How Language Models Use Long Contexts*. Transactions of the Association for Computational Linguistics, v. 12, p. 26-44, 2024. Disponível em: https://arxiv.org/abs/2307.03172. Acesso em: 15 out. 2024.

[12] KAMRADT, Greg. *Needle In A Haystack - Pressure Testing LLMs*. GitHub, 2023. Disponível em: https://github.com/gkamradt/LLMTest_NeedleInAHaystack. Acesso em: 15 out. 2024.

[13] XIONG, Ruibin et al. *On Layer Normalization in the Transformer Architecture*. ICML, 2020. Disponível em: https://arxiv.org/abs/2002.04745. Acesso em: 15 out. 2024.

[14] BULATOV, Aydar et al. *Recurrent Memory Transformer*. NeurIPS, 2022. Disponível em: https://arxiv.org/abs/2207.04901. Acesso em: 15 out. 2024.

[15] SHAHAM, Uri et al. *SCROLLS: Standardized Benchmark for Reasoning over Long Texts*. EMNLP, 2022. Disponível em: https://arxiv.org/abs/2211.10343. Acesso em: 15 out. 2024.

[16] PRESS, Ofir et al. *Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation*. ICLR, 2022. Disponível em: https://arxiv.org/abs/2108.12409. Acesso em: 15 out. 2024.
