## 4. Fine-Tuning: Personalizando o Modelo

### 4.1 Introdução

Nos capítulos anteriores, construímos um assistente com chat, persistência, API e RAG. O sistema funciona bem, mas ainda depende completamente do modelo genérico. O que acontece quando você precisa de um modelo que:

- Fale o jargão específico da sua empresa
- Entenda o contexto do seu domínio (saúde, jurídico, financeiro)
- Responda em um formato padronizado
- Reduza custos de tokens (respostas mais curtas e precisas)

**Fine-tuning** é o processo de **treinar um modelo existente** com dados específicos do seu domínio [1]. Em vez de criar um modelo do zero (que custaria milhões de dólares), você adapta um modelo já treinado para sua necessidade.

**O que você vai aprender:**
- Quando fazer fine-tuning vs. usar RAG
- Preparação de dados de treino
- Técnicas de fine-tuning eficientes (LoRA, QLoRA)
- Avaliação do modelo fine-tuned
- Custos e trade-offs

**Aviso importante:** Fine-tuning NÃO substitui RAG. Eles servem para propósitos diferentes:
- **RAG:** Knowledge base atualizável, respostas com fontes
- **Fine-tuning:** Comportamento, estilo, formato, conhecimento fixo

### 4.2 Explica

#### Quando Fazer Fine-Tuning

Fine-tuning é valioso quando [2]:

1. **Formato específico:** Você precisa que as respostas sigam um formato rígido (JSON, tabelas, código)
2. **Jargão de domínio:** O modelo precisa entender termos técnicos específicos
3. **Comportamento consistente:** Todas as respostas devem seguir um padrão
4. **Redução de custo:** Respostas mais curtas = menos tokens = menos dinheiro
5. **Latência:** Modelo fine-tuned pode ser menor e mais rápido

**Quando NÃO fazer fine-tuning:**

| Situação | Usar RAG | Usar Fine-Tuning |
|----------|----------|------------------|
| Conhecimento muda frequentemente | ✅ | ❌ |
| Precisa citar fontes | ✅ | ❌ |
| Formato de resposta rígido | ❌ | ✅ |
| Jargão de domínio | Parcial | ✅ |
| Custo é prioridade | ❌ | ✅ |

#### Preparação de Dados de Treino

O dataset de fine-tuning segue o formato de conversas [3]:

```json
{
  "messages": [
    {"role": "system", "content": "Você é um suporte técnico da empresa X."},
    {"role": "user", "content": "Meu login não funciona"},
    {"role": "assistant", "content": "Vou ajudá-lo com o login. Primeiro, verifique se..."}
  ]
}
```

**Dicas de preparação:**

1. **Qualidade > Quantidade:** 500 exemplos de alta qualidade > 5000 exemplos ruins
2. **Diversidade:** Cubra todos os cenários que o modelo encontrará
3. **Consistência:** Todas as respostas devem seguir o mesmo padrão
4. **Limpeza:** Remova dados sensíveis, erros de digitação, respostas inconsistentes

#### LoRA: Fine-Tuning Eficiente

LoRA (Low-Rank Adaptation) é uma técnica que treina apenas uma small fraction dos parâmetros do modelo [4]. Em vez de ajustar bilhões de parâmetros, LoRA treina matrizes de baixa dimensão:

```
Modelo original: 7 bilhões de parâmetros
LoRA: ~0.1% dos parâmetros = ~7 milhões
```

**Vantagens do LoRA:**
- Treina em GPUs modestas (mesmo com 8GB de VRAM)
- É rápido (minutos vs horas)
- Pode ser compartilhado (adaptador leve)
- Não degrada o modelo original

**QLoRA** é ainda mais eficiente — quantiza o modelo para 4 bits durante o treino [5]:

```
LoRA:    16 bits por parâmetro → ~14GB para modelo 7B
QLoRA:    4 bits por parâmetro → ~4GB para modelo 7B
```

#### Métricas de Avaliação

Como saber se o fine-tuning funcionou? Métricas comuns [6]:

1. **Perplexity:** Mede quão "surpreso" o modelo fica com texto novo (menor = melhor)
2. **BLEU/ROUGE:** Comparação com respostas de referência
3. **Avaliação humana:** Pessoas avaliam a qualidade das respostas
4. **Avaliação automática:** Outro LLM (GPT-4) julga as respostas
5. **Métricas de domínio:** Acurácia em tarefas específicas

### 4.3 Ilustra

#### Preparação do Dataset

```python
# finetune/dataset.py
"""
Preparação de dados para fine-tuning.
"""
import json
from typing import List, Dict
from pathlib import Path
from dataclasses import dataclass

@dataclass
class ExemploFineTuning:
    """Um exemplo de treino no formato conversacional."""
    sistema: str
    usuario: str
    assistente: str
    
    def to_dict(self) -> Dict:
        return {
            "messages": [
                {"role": "system", "content": self.sistema},
                {"role": "user", "content": self.usuario},
                {"role": "assistant", "content": self.assistente},
            ]
        }

class DatasetPreparer:
    """Prepara dados para fine-tuning."""
    
    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt
        self.exemplos: List[ExemploFineTuning] = []
    
    def adicionar_exemplo(self, pergunta: str, resposta: str):
        """Adiciona um exemplo ao dataset."""
        exemplo = ExemploFineTuning(
            sistema=self.system_prompt,
            usuario=pergunta,
            assistente=resposta,
        )
        self.exemplos.append(exemplo)
    
    def carregar_de_json(self, caminho: str):
        """Carrega exemplos de um arquivo JSON."""
        with open(caminho, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        for item in dados:
            self.adicionar_exemplo(
                pergunta=item["pergunta"],
                resposta=item["resposta"]
            )
    
    def salvar_jsonl(self, caminho: str):
        """Salva o dataset no formato JSONL para fine-tuning."""
        Path(caminho).parent.mkdir(parents=True, exist_ok=True)
        
        with open(caminho, 'w', encoding='utf-8') as f:
            for exemplo in self.exemplos:
                f.write(json.dumps(exemplo.to_dict(), ensure_ascii=False) + '\n')
    
    def dividir_treino_validacao(self, ratio: float = 0.8):
        """Divide o dataset em treino e validação."""
        import random
        random.shuffle(self.exemplos)
        
        split_idx = int(len(self.exemplos) * ratio)
        treino = self.exemplos[:split_idx]
        validacao = self.exemplos[split_idx:]
        
        return treino, validacao
    
    def estatisticas(self) -> Dict:
        """Retorna estatísticas do dataset."""
        total = len(self.exemplos)
        avg_user_len = sum(len(e.usuario) for e in self.exemplos) / total
        avg_assistant_len = sum(len(e.assistente) for e in self.exemplos) / total
        
        return {
            "total_exemplos": total,
            "avg_tamanho_usuario": avg_user_len,
            "avg_tamanho_assistente": avg_assistant_len,
        }
```

#### Script de Fine-Tuning

```python
# finetune/train.py
"""
Script de fine-tuning com LoRA usando PEFT e Hugging Face.
"""
import os
import json
import torch
from pathlib import Path
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
)
from peft import LoraConfig, get_peft_model, TaskType
from datasets import load_dataset

class LoRATuner:
    """Fine-tuning com LoRA para modelos de linguagem."""
    
    def __init__(self, model_name: str = "deepseek-ai/deepseek-llm-7b-chat"):
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"Carregando modelo: {model_name}")
        print(f"Device: {self.device}")
    
    def carregar_modelo(self):
        """Carrega o modelo e tokenizer."""
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
        # Adicionar padding token se não existir
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto" if self.device == "cuda" else None,
        )
        
        # Configurar LoRA
        lora_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            r=8,  # rank
            lora_alpha=32,
            lora_dropout=0.1,
            target_modules=["q_proj", "v_proj"],  # Módulos para aplicar LoRA
        )
        
        self.model = get_peft_model(self.model, lora_config)
        
        # Mostrar parâmetros treináveis
        trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        total_params = sum(p.numel() for p in self.model.parameters())
        print(f"Parâmetros treináveis: {trainable_params:,} ({100 * trainable_params / total_params:.2f}%)")
    
    def treinar(self, dataset_path: str, output_dir: str,
                epochs: int = 3, batch_size: int = 4, learning_rate: float = 2e-4):
        """Executa o fine-tuning."""
        # Carregar dataset
        dataset = load_dataset("json", data_files=dataset_path, split="train")
        
        # Tokenizar
        def tokenize(examples):
            return self.tokenizer(
                examples["text"],
                truncation=True,
                padding="max_length",
                max_length=512,
            )
        
        tokenized_dataset = dataset.map(tokenize, batched=True)
        
        # Configurar treino
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            learning_rate=learning_rate,
            warmup_steps=100,
            logging_steps=10,
            save_strategy="epoch",
            fp16=self.device == "cuda",
        )
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=tokenized_dataset,
        )
        
        # Treinar
        print("Iniciando fine-tuning...")
        trainer.train()
        
        # Salvar adaptador LoRA
        self.model.save_pretrained(output_dir)
        self.tokenizer.save_pretrained(output_dir)
        
        print(f"Modelo salvo em: {output_dir}")
    
    def prever(self, pergunta: str, max_tokens: int = 200) -> str:
        """Gera uma previsão usando o modelo fine-tuned."""
        inputs = self.tokenizer(pergunta, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
            )
        
        resposta = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return resposta
```

#### Script de Avaliação

```python
# finetune/evaluate.py
"""
Avaliação do modelo fine-tuned.
"""
import json
from typing import List, Dict
from pathlib import Path
from dataclasses import dataclass

@dataclass
class ResultadoAvaliacao:
    """Resultado de uma avaliação."""
    pergunta: str
    resposta_esperada: str
    resposta_obtida: str
    score: float  # 0-1
    metricas: Dict

class AvaliadorFineTuning:
    """Avalia a qualidade do fine-tuning."""
    
    def __init__(self):
        self.resultados: List[ResultadoAvaliacao] = []
    
    def avaliar_resposta(self, pergunta: str, resposta_esperada: str,
                        resposta_obtida: str) -> ResultadoAvaliacao:
        """Avalia uma única resposta."""
        # Métrica simples: similaridade de palavras
        palavras_esperada = set(resposta_esperada.lower().split())
        palavras_obtida = set(resposta_obtida.lower().split())
        
        if not palavras_esperada:
            score = 0.0
        else:
            intersecao = palavras_esperada & palavras_obtida
            score = len(intersecao) / len(palavras_esperada)
        
        resultado = ResultadoAvaliacao(
            pergunta=pergunta,
            resposta_esperada=resposta_esperada,
            resposta_obtida=resposta_obtida,
            score=score,
            metricas={
                "palavras_esperadas": len(palavras_esperada),
                "palavras_obtidas": len(palavras_obtida),
                "intersecao": len(palavras_esperada & palavras_obtida),
            }
        )
        
        self.resultados.append(resultado)
        return resultado
    
    def avaliar_dataset(self, modelo, dataset: List[Dict]) -> Dict:
        """Avalia o modelo em um dataset completo."""
        scores = []
        
        for item in dataset:
            resultado = self.avaliar_resposta(
                pergunta=item["pergunta"],
                resposta_esperada=item["resposta"],
                resposta_obtida=modelo.prever(item["pergunta"]),
            )
            scores.append(resultado.score)
        
        return {
            "total": len(scores),
            "score_medio": sum(scores) / len(scores) if scores else 0,
            "score_minimo": min(scores) if scores else 0,
            "score_maximo": max(scores) if scores else 0,
            "aprovados": sum(1 for s in scores if s >= 0.7),
            "reprovados": sum(1 for s in scores if s < 0.7),
        }
    
    def salvar_relatorio(self, caminho: str):
        """Salva o relatório de avaliação."""
        relatorio = {
            "total_avaliacoes": len(self.resultados),
            "score_medio": sum(r.score for r in self.resultados) / len(self.resultados) if self.resultados else 0,
            "resultados": [
                {
                    "pergunta": r.pergunta,
                    "score": r.score,
                    "metricas": r.metricas,
                }
                for r in self.resultados
            ]
        }
        
        Path(caminho).parent.mkdir(parents=True, exist_ok=True)
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(relatorio, f, ensure_ascii=False, indent=2)
```

#### Exemplo de Dataset de Treino

```json
[
  {
    "pergunta": "Como configurar o VPN?",
    "resposta": "Para configurar o VPN:\n1. Acesse Configurações > Rede\n2. Selecione 'Adicionar VPN'\n3. Preencha os dados do servidor\n4. Clique em 'Conectar'\n\nPrecisa de ajuda com algum passo específico?"
  },
  {
    "pergunta": "Meu e-mail não está sincronizando",
    "resposta": "Vou ajudá-lo com a sincronização de e-mail:\n1. Verifique sua conexão com a internet\n2. Reinicie o aplicativo de e-mail\n3. Se persistir, reconfigure a conta\n\nQual dispositivo você está usando?"
  },
  {
    "pergunta": "Esqueci minha senha",
    "resposta": "Para redefinir sua senha:\n1. Acesse a página de login\n2. Clique em 'Esqueci minha senha'\n3. Informe seu e-mail corporativo\n4. Verifique sua caixa de entrada\n\nA senha temporária expira em 24 horas."
  }
]
```

#### docker-compose.yml (atualizado com GPU)

```yaml
# docker-compose.yml (atualizado para fine-tuning)
version: '3.8'

services:
  finetune:
    build:
      context: .
      dockerfile: Dockerfile.finetune
    runtime: nvidia  # Requer NVIDIA Container Toolkit
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
    volumes:
      - ./data:/app/data
      - ./models:/app/models
    command: python finetune/train.py
```

### 4.4 Técnica

#### Configuração do LoRA

```yaml
# configs/training.yaml
model:
  name: "deepseek-ai/deepseek-llm-7b-chat"
  max_length: 512

lora:
  r: 8
  lora_alpha: 32
  lora_dropout: 0.1
  target_modules:
    - q_proj
    - v_proj
    - k_proj
    - o_proj

training:
  epochs: 3
  batch_size: 4
  learning_rate: 0.0002
  warmup_steps: 100
  weight_decay: 0.01
  
evaluation:
  metric: "accuracy"
  threshold: 0.7
  dataset_size: 100
```

#### Custos de Fine-Tuning

```python
# finetune/cost_calculator.py
"""
Calculadora de custos de fine-tuning.
"""
from dataclasses import dataclass

@dataclass
class CustoFineTuning:
    """Estimativa de custos de fine-tuning."""
    
    @staticmethod
    def estimar_custo(
        num_exemplos: int,
        avg_tokens_por_exemplo: int,
        epochs: int,
        custo_gpu_hora: float = 0.50,  # USD por hora (T4)
    ) -> Dict:
        """Estima o custo total do fine-tuning."""
        # Estimativa de tokens totais
        total_tokens = num_exemplos * avg_tokens_por_exemplo * epochs
        
        # Estimativa de tempo (baseado em GPU T4)
        # Aproximadamente 1000 tokens/segundo em T4
        tempo_segundos = total_tokens / 1000
        tempo_horas = tempo_segundos / 3600
        
        custo_total = tempo_horas * custo_gpu_hora
        
        return {
            "total_tokens": total_tokens,
            "tempo_estimado_horas": tempo_horas,
            "custo_total_usd": custo_total,
            "custo_por_exemplo": custo_total / num_exemplos if num_exemplos else 0,
        }
```

#### Testes

```python
# tests/test_finetuning.py
"""
Testes para o pipeline de fine-tuning.
"""
import pytest
from finetune.dataset import DatasetPreparer, ExemploFineTuning

def test_dataset_preparer():
    """Testa preparação de dataset."""
    preparer = DatasetPreparer(
        system_prompt="Você é um assistente de suporte."
    )
    
    preparer.adicionar_exemplo(
        pergunta="Como faço login?",
        resposta="Acesse o site e clique em 'Entrar'."
    )
    
    assert len(preparer.exemplos) == 1
    assert preparer.exemplos[0].usuario == "Como faço login?"

def test_dividir_treino_validacao():
    """Testa divisão do dataset."""
    preparer = DatasetPreparer(system_prompt="Teste")
    
    for i in range(10):
        preparer.adicionar_exemplo(f"Pergunta {i}", f"Resposta {i}")
    
    treino, validacao = preparer.dividir_treino_validacao(ratio=0.8)
    
    assert len(treino) == 8
    assert len(validacao) == 2

def test_estatisticas():
    """Testa cálculo de estatísticas."""
    preparer = DatasetPreparer(system_prompt="Teste")
    preparer.adicionar_exemplo("Pergunta curta", "Resposta curta")
    preparer.adicionar_exemplo("Outra pergunta muito mais longa", "Outra resposta também muito mais longa")
    
    stats = preparer.estatisticas()
    
    assert stats["total_exemplos"] == 2
    assert stats["avg_tamanho_usuario"] > 0
    assert stats["avg_tamanho_assistente"] > 0
```

### 4.5 Aplica

#### Exercício Prático: Fine-Tuning Completo

1. **Prepare o dataset:**
```python
from finetune.dataset import DatasetPreparer

preparer = DatasetPreparer(
    system_prompt="Você é um suporte técnico da Empresa X."
)

# Adicione exemplos reais do seu domínio
preparer.adicionar_exemplo(
    pergunta="Como configuro o email?",
    resposta="Para configurar o email:\n1. Abra o Outlook\n2. Vá em Arquivo > Configurações\n3. Adicione sua conta corporativa\n4. Use as configurações IMAP"
)

# Salve o dataset
preparer.salvar_jsonl("data/treino.jsonl")
```

2. **Execute o fine-tuning:**
```bash
python finetune/train.py --config configs/training.yaml
```

3. **Avalie o modelo:**
```python
from finetune.evaluate import AvaliadorFineTuning

avaliador = AvaliadorFineTuning()
# Execute avaliação...
```

4. **Compare com o modelo base:**
- Teste as mesmas perguntas com o modelo original e fine-tuned
- Avalie qualidade, formato e custo

### 4.6 Conclusão

Neste capítulo, você aprendeu a personalizar modelos de IA com fine-tuning. O projeto agora tem:

- **Pipeline de preparação de dados** para fine-tuning
- **Fine-tuning com LoRA** que funciona em GPUs modestas
- **Avaliação automatizada** da qualidade do modelo
- **Calculadora de custos** para planejamento

No próximo capítulo, vamos implementar um **sistema de evals** — avaliações automatizadas que garantem que o assistente responde corretamente antes de ir para produção.

### 4.7 Referências

[1] OpenAI. "Fine-tuning Guide." OpenAI Platform Documentation, 2024. Disponível em: https://platform.openai.com/docs/guides/fine-tuning

[2] Huyen, Chip. "Designing Machine Learning Systems." O'Reilly Media, 2022. ISBN: 978-1098107963.

[3] Hugging Face. "PEFT Library — Parameter-Efficient Fine-Tuning." Hugging Face Documentation, 2024. Disponível em: https://huggingface.co/docs/peft

[4] Hu, E.J. et al. "LoRA: Low-Rank Adaptation of Large Language Models." arXiv:2106.09685, 2021.

[5] Dettmers, T. et al. "QLoRA: Efficient Finetuning of Quantized Language Models." Advances in Neural Information Processing Systems, vol. 35, 2022.

[6] DeepEval. "LLM Evaluation Framework." DeepEval Documentation, 2024. Disponível em: https://docs.confident-ai.com/

[7] Microsoft. "GenAI Operations with MLOps." Azure Architecture Center, 2024. Disponível em: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/

[8] AWS. "Machine Learning Lens — Well-Architected Framework." Amazon Web Services, 2024. Disponível em: https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/

[9] Google Cloud. "ML System Design Patterns." Google Cloud Architecture Center, 2023. Disponível em: https://cloud.google.com/architecture/ml-design-patterns

[10] DeepSeek. "API Documentation." DeepSeek API Docs, 2024. Disponível em: https://api-docs.deepseek.com/

[11] LangChain. "Fine-tuning Guide." LangChain Documentation, 2024. Disponível em: https://python.langchain.com/docs/

[12] Hugging Face. "Transformers Library." Hugging Face Documentation, 2024. Disponível em: https://huggingface.co/docs/transformers

[13] PyTorch. "PyTorch Documentation." PyTorch Project, 2024. Disponível em: https://pytorch.org/docs/

[14] NVIDIA. "NVIDIA Container Toolkit." NVIDIA Documentation, 2024. Disponível em: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/

[15] Docker. "GPU Support with NVIDIA Container Toolkit." Docker Documentation, 2024. Disponível em: https://docs.docker.com/gpu-support/

[16] OWASP. "Top 10 for Large Language Model Applications." OWASP Foundation, 2024. Disponível em: https://owasp.org/www-project-top-10-for-large-language-model-applications/

[17] NIST. "Artificial Intelligence Risk Management Framework." National Institute of Standards and Technology, 2024. Disponível em: https://www.nist.gov/artificial-intelligence/risk-management-framework

[18] Microsoft Azure Architecture Center. "Get Started with AI Architecture Design." Microsoft Learn, 2024. Disponível em: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/ai-get-started

[19] Pinecone. "What is RAG?" Pinecone Learning Center, 2024. Disponível em: https://www.pinecone.io/learn/retrieval-augmented-generation/

[20] Prometheus. "Monitoring Best Practices." Prometheus Documentation, 2024. Disponível em: https://prometheus.io/docs/

#### Comparação de Técnicas de Fine-Tuning

Entender quando usar cada técnica é crucial para otimizar custos e qualidade [6]:

| Técnica | Parâmetros Treináveis | VRAM Necessária | Tempo | Qualidade |
|---------|----------------------|-----------------|-------|-----------|
| Full Fine-Tuning | 100% | 40GB+ | Horas | Máxima |
| LoRA | 0.1-1% | 8-16GB | Minutos | Alta |
| QLoRA | 0.1-1% | 4-8GB | Minutos | Alta |
| Prompt Tuning | <0.01% | 4GB | Segundos | Média |
| In-Context Learning | 0% | N/A | N/A | Variável |

**Full Fine-Tuning:**
- Treina TODOS os parâmetros do modelo
- Melhor qualidade, mas caro e lento
- Requer GPU com muita VRAM (A100, H100)
- Usar quando: dataset grande, qualidade é prioridade

**LoRA (Low-Rank Adaptation):**
- Treina apenas matrizes de baixa dimensão
- 99% menos parâmetros que full fine-tuning
- Funciona em GPUs modestas (T4, V100)
- Usar quando: orçamento limitado, qualidade aceitável

**QLoRA:**
- LoRA + quantização 4 bits
- Ainda mais eficiente que LoRA
- Funciona em GPUs com 4GB de VRAM
- Usar quando: hardware muito limitado

**Prompt Tuning:**
- Aprende um "prompt" contínuo (não texto)
- Extremamente leve
- Qualidade inferior a LoRA
- Usar quando: muitas tarefas, poucos dados

**In-Context Learning:**
- Não treina nada, só usa exemplos no prompt
- Zero custo de treino
- Qualidade depende dos exemplos
- Usar quando: prototipagem rápida

**Fluxo de decisão:**

```
Dataset grande (>10k exemplos)?
├── Sim → Full Fine-Tuning (se tiver GPU A100)
│         ou LoRA (se GPU modesta)
└── Não → Dataset médio (1k-10k)?
    ├── Sim → LoRA (recomendado)
    └── Não → Dataset pequeno (<1k)?
        ├── Sim → Prompt Tuning ou In-Context Learning
        └── Não → Revisar qualidade dos dados primeiro
```

**Erros comuns de iniciantes:**
1. **Fine-tuning com dados ruins:** Qualidade > Quantidade
2. **Esquecer de avaliar:** Sem evals, você não sabe se melhorou
3. **Overfitting:** Modelo decora exemplos em vez de aprender padrões
4. **Ignorar custos:** Fine-tuning custa GPU, não é grátis
5. **Não testar em produção:** Lab ≠ Produção

