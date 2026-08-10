# Edições Hashline: Precisão com Menos Tokens

## O problema que consome recursos

No estaleiro digital onde construímos harnesses de IA, existe um problema antigo que consome recursos como um motor sem eficiência: **redundantemente enviamos o código completo** toda vez que queremos fazer uma pequena alteração.

Imagine um mestre de estaleiro que, para trocar um parafuso no casco, precisasse reconstruir todo o navio. Isso seria absurdo — e é exatamente o que acontece quando usamos métodos tradicionais de edição.

O **hashline edit** é a âncora que estabiliza nossa navegação. Em vez de enviar o conteúdo completo de um arquivo, o sistema gera um **hash** (uma impressão digital criptográfica) de cada bloco de código.

Quando queremos modificar algo, bastamos referenciar o hash — como um GPS que diz exatamente onde estamos no oceano digital, sem precisar descrever toda a rota.

## O fluxo tradicional: tokens desperdiçados

Quando um agente de IA edita código, o fluxo tradicional é:

```
1. Ler o arquivo completo (N tokens)
2. Identificar o que mudar
3. Reescrever o arquivo inteiro (N tokens)
```

Isso significa que, para uma alteração de 10 linhas em um arquivo de 500 linhas, pagamos **1000 tokens** — o dobro do necessário. No estaleiro naval, seria como pintar todo o casco para trocar uma única tinta.

## A solução: hashes como âncoras

O hashline edit transforma esse fluxo.

```
1. Gerar hashes dos blocos existentes (custo: zero)
2. Referenciar o hash do bloco-alvo (custo: ~10 tokens)
3. Enviar apenas a alteração (custo: M tokens)
```

Agora, para aquela mesma alteração de 10 linhas, pagamos apenas **~10 tokens** — uma redução de **99%** no custo de edição.

## Como funciona o hash

O hash é gerado a partir do conteúdo do bloco. Se o bloco não mudou, o hash permanece idêntico. Isso cria um sistema de **referência estável**.

**Antes:** "Edite a função `processar_dados()` na linha 42"

**Depois:** "Edite o bloco com hash `a1b2c3d4`"

A vantagem é que o hash não depende de números de linha (que mudam com edições) nem do conteúdo completo (que consome tokens).

## Comparação com str_replace

O método `str_replace` (substituição de strings) é como tentar encontrar uma agulha no palheiro.

| Método | Tokens por Edição | Confiabilidade | Colisões |
|--------|-------------------|----------------|----------|
| Conteúdo completo | ~1000 | Alta | Zero |
| str_replace | ~200 | Média | Possíveis |
| Hashline | ~50 | Alta | Criptograficamente improváveis |

O `str_replace` pode falhar quando o mesmo texto aparece múltiplas vezes, quando o texto contém caracteres especiais, ou quando o contexto é ambíguo.

O hash resolve isso porque cada bloco único gera um hash único — como um GPS que mostra coordenadas exatas, não descrições vagas.

## A economia por modelo

Os números são impressionantes.

| Modelo | Tokens Antes | Tokens Depois | Redução |
|--------|--------------|---------------|---------|
| Grok 4 Fast | 10.000 | 3.900 | **61%** |
| Grok Code Fast 1 | 10.000 | 3.170 | **68.3%** |
| Gemini 3 Flash | 10.000 | 5.200 | **48%** |

A métrica chave: o Grok Code Fast 1 apresentou um **10x lift** — a taxa de sucesso em edições subiu de 6.7% (com str_replace) para 68.3% (com hashline).

## Estrutura de um hash

O hash no Oh My Pi segue o padrão `#//<hash-8-chars>`.

Exemplo de blocos com hashes.

```python
#//a1b2c3d4
def processar_dados(dados):
    resultado = []
    for item in dados:
        if item.get("valido"):
            resultado.append(transformar(item))
    return resultado
#//a1b2c3d4
```

## Sintaxe de edição

Para editar um bloco, o agente envia.

```
#//a1b2c3d4 (replace: <hash-do-bloco-novo>)
def processar_dados(dados):
    resultado = []
    for item in dados:
        if item.get("valido") and item.get("prioridade") > 5:
            resultado.append(transformar(item))
    return resultado
#//nova1234
```

## Exemplo prático

**Cenário:** Queremos adicionar validação de tipos na função.

**Método Tradicional (str_replace):**
```
Substituir:
def processar_dados(dados):
    resultado = []
    for item in dados:
        if item.get("valido"):
            resultado.append(transformar(item))
    return resultado

Por:
def processar_dados(dados: list[dict]) -> list:
    resultado = []
    for item in dados:
        if item.get("valido"):
            resultado.append(transformar(item))
    return resultado
```
**Custo:** ~150 tokens

**Método Hashline:**
```
#//a1b2c3d4 (replace: <hash-do-bloco-novo>)
def processar_dados(dados: list[dict]) -> list:
    resultado = []
    for item in dados:
        if item.get("valido"):
            resultado.append(transformar(item))
    return resultado
#//f1e2d3c4
```
**Custo:** ~80 tokens

## Implementação no Oh My Pi

```python
import hashlib

def gerar_hash(conteudo: str) -> str:
    """Gera hash curto de 8 caracteres para um bloco de código."""
    return hashlib.sha256(conteudo.encode()).hexdigest()[:8]

def identificar_blocos(arquivo: str) -> dict:
    """Identifica blocos delimitados por hashes e retorna mapeamento."""
    blocos = {}
    linhas = arquivo.split("\n")
    hash_atual = None
    inicio = 0
    
    for i, linha in enumerate(linhas):
        if linha.startswith("#//") and len(linha) == 11:
            if hash_atual is None:
                hash_atual = linha[3:]
                inicio = i + 1
            else:
                blocos[hash_atual] = {
                    "inicio": inicio,
                    "fim": i,
                    "conteudo": "\n".join(linhas[inicio:i])
                }
                hash_atual = None
    
    return blocos
```

## Quando usar hashline edits

| Cenário | Recomendação |
|---------|--------------|
| Edição de função existente | ✅ Hashline |
| Adição de nova função | ✅ Hashline |
| Modificação de múltiplos blocos | ✅ Hashline |
| Reescrita completa do arquivo | ❌ Conteúdo completo |
| Busca e substituição simples | ⚠️ str_replace pode bastar |

## Caso de uso: refatoração de código

Imagine que você é o mestre de estaleiro e precisa modernizar o motor do navio.

**Antes (Código Legado):**
```python
#//motor001
def calcular_velocidade(distancia, tempo):
    return distancia / tempo
#//motor001
```

**Depois (Código Modernizado com Hashline):**
```python
#//motor001 (replace: <novo-hash>)
def calcular_velocidade(distancia: float, tempo: float) -> float:
    """Calcula a velocidade média em km/h.
    
    Args:
        distancia: Distância percorrida em km
        tempo: Tempo gasto em horas
    
    Returns:
        Velocidade média em km/h
    
    Raises:
        ValueError: Se tempo for zero ou negativo
    """
    if tempo <= 0:
        raise ValueError("Tempo deve ser positivo")
    return distancia / tempo
#//motor-novo
```

**Economia:** Em vez de enviar todo o arquivo (que pode ter centenas de linhas), enviamos apenas o hash do bloco (~8 tokens) + a alteração (~50 tokens) = ~58 tokens, em vez de ~500+ tokens.

## Dicas do Mestre de Estaleiro

**Seja preciso.** Um hash errado edita o bloco errado. Sempre verifique antes de enviar.

**Prefira blocos pequenos.** Blocos menores = hashes mais específicos = menos ambiguidade.

**Use para iterações rápidas.** Quando você está testando múltiplas versões, hashline reduz o custo drasticamente.

**Combine com outras ferramentas.** Use hashline para edições pontuais e outros métodos para reestruturações maiores.

## Próximos Passos

Assim como um mestre de estaleiro experiente sabe exatamente qual parte do casco precisa de reparo sem precisar desmontar todo o navio, o hashline edit permite que agentes de IA façam edições precisas com o mínimo de recursos.

Os números falam por si: **61% menos tokens** com o Grok 4 Fast, **10x de melhoria** na acurácia com o Grok Code Fast 1, e **5 pontos percentuais** de vantagem sobre str_replace com o Gemini 3 Flash.

No próximo capítulo, vamos explorar como integrar essas edições em fluxos de trabalho mais complexos, combinando hashline com outras técnicas de otimização.

Lembre-se: no estaleiro digital, **precisão é mais valiosa que quantidade**. Cada token economizado é um nó a mais no cabo que segura o navio no porto.

Acesse a documentação completa: https://omp.sh/docs

Siga-nous nas redes sociais para dicas, tutoriais e novidades sobre o Oh My Pi.
