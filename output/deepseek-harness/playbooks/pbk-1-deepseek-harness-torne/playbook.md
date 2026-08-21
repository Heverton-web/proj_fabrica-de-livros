---
title: "Playbook — DeepSeek Harness: Torne-se um Especialista"
subtitle: "Guia de bancada · 8 passos práticos"
author: "Heverton Eduardo Peres"
lang: pt-BR
---

# Objetivo do Material

Dominar o ecossistema DeepSeek — modelos, API, Harness, plugins, inferência e deploy — em 8 passos práticos, de iniciante a engenheiro de IA capaz de construir soluções completas.

# Como usar este playbook

Você é o **Engenheiro de IA**. Cada passo é um card independente com sete partes: objetivo, pré-requisito, entregas, execução, gate de verificação, critério de conclusão e armadilhas.

# Mapa dos Estágios

| # | Estágio | Passos |
|---|---------|--------|
| 1 | Fundamentos | 1, 2, 3, 4 |
| 2 | Domínio | 5, 6, 7, 8 |

# Passos Práticos

## Passo 1 — Instalar e Configurar o Ecossistema

> **Estágio:** Fundamentos · **Origem:** Cap. 1

### ① Objetivo

Configurar o ambiente de desenvolvimento com DeepSeek Harness, API key e verificação de integração.

### ② Pré-requisito

Node.js 18+, Python 3.10+, conta em platform.deepseek.com

### ③ Entregas

- Harness rodando em http://127.0.0.1:3080
- API key configurada como variável de ambiente
- Script de verificação do ecossistema rodando

### ④ Execução

```bash
npx @deepseek-ai/dsh web
export DEEPSEEK_API_KEY="sk-sua-chave"
curl -s https://api.deepseek.com/models -H "Authorization: Bearer ${DEEPSEEK_API_KEY}"
```

### ⑤ Gate

Harness retorna `{"status":"ok"}` e API lista modelos disponíveis.

### ⑥ Concluído quando

Web UI acessível, API respondendo, variável de ambiente persistida no `.bashrc`.

### ⑦ Armadilhas

- Usar endpoint `/anthropic` no lugar do endpoint `/` (formato errado = erro 400)
- Esquecer `DEEPSEEK_API_KEY` no `.bashrc` (some entre sessões)

---

## Passo 2 — Fazer as Primeiras Chamadas à API

> **Estágio:** Fundamentos · **Origem:** Cap. 2

### ① Objetivo

Realizar chamadas de chat, streaming e thinking mode com os três modelos disponíveis.

### ② Pré-requisito

API key configurada (Passo 1)

### ③ Entregas

- Script Python com chat simples, streaming e thinking mode
- Comparação de latência entre v4-flash e v4-pro

### ④ Execução

```python
from openai import OpenAI
c = OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
r = c.chat.completions.create(model="deepseek-v4-flash", messages=[{"role":"user","content":"Olá"}])
```

### ⑤ Gate

Resposta recebida sem erro, latência < 3s para flash.

### ⑥ Concluído quando

Três chamadas funcionando (flash, pro, streaming) com tratamento de erros.

### ⑦ Armadilhas

- Usar thinking mode com v4-flash (recurso limitado, usar v4-pro)
- Não tratar `RateLimitError` (backoff exponencial necessário)

---

## Passo 3 — Integrar com Ferramentas de Coding

> **Estágio:** Fundamentos · **Origem:** Cap. 3

### ① Objetivo

Configurar DeepSeek como backend no Claude Code, Cline ou OpenCode.

### ② Pré-requisito

Ferramenta de coding instalada, API key configurada

### ③ Entregas

- Ferramenta configurada com DeepSeek como backend
- Teste de code completion funcionando

### ④ Execução

```bash
export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
export ANTHROPIC_API_KEY="${DEEPSEEK_API_KEY}"
claude  # Inicia Claude Code com DeepSeek
```

### ⑤ Gate

Ferramenta responde usando modelo DeepSeek (verificar no log).

### ⑥ Concluído quando

Code completion e chat funcionando na ferramenta escolhida.

### ⑦ Armadilhas

- Misturar endpoints OpenAI/Anthropic (cada ferramenta usa um formato)
- Não configurar `ANTHROPIC_API_KEY` alongside `ANTHROPIC_BASE_URL`

---

## Passo 4 — Dominar Prompt Engineering

> **Estágio:** Fundamentos · **Origem:** Cap. 4

### ① Objetivo

Criar prompts otimizados para diferentes tarefas com thinking mode e few-shot.

### ② Pré-requisito

API funcionando (Passo 2)

### ③ Entregas

- Biblioteca de prompts reutilizáveis (5 tarefas)
- Prompt com thinking mode para problemas complexos
- Exemplos de few-shot para classificação

### ④ Execução

```python
r = c.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[{"role":"user","content":"Revise este código..."}],
    extra_body={"thinking":{"type":"enabled"}},
    reasoning_effort="high"
)
```

### ⑤ Gate

Resposta com raciocínio visível (thinking tokens) para problemas complexos.

### ⑥ Concluído quando

Prompts para 5 tarefas diferentes gerando respostas de qualidade consistente.

### ⑦ Armadilhas

- Usar temperature alta para código (usar 0.0-0.2)
- Não incluir formato de saída (respostas genéricas)

---

## Passo 5 — Explorar a Arquitetura do Harness

> **Estágio:** Domínio · **Origem:** Cap. 5

### ① Objetivo

Entender a arquitetura de plugins do Cordis e o ciclo de vida dos componentes.

### ② Pré-requisito

Harness instalado e rodando (Passo 1)

### ③ Entregas

- Lista de plugins ativos identificada
- Diagrama de comunicação entre plugins documentado

### ④ Execução

```bash
npx @deepseek-ai/dsh web --plugins token-counter
# Na Web UI: enviar mensagem e observar logs do plugin
```

### ⑤ Gate

Plugin token-counter loga contagem de tokens para cada mensagem.

### ⑥ Concluído quando

Consegue descrever o ciclo activate → onMessage → deactivate de um plugin.

### ⑦ Armadilhas

- Desligar um plugin essencial (chat/modelo) sem perceber
- Não tratar exceções no onMessage (derruba o sistema)

---

## Passo 6 — Criar um Plugin Personalizado

> **Estágio:** Domínio · **Origem:** Cap. 6

### ① Objetivo

Desenvolver, testar e publicar um plugin TypeScript para o Harness.

### ② Pré-requisito

Conhecimento da arquitetura (Passo 5), TypeScript básico

### ③ Entregas

- Plugin funcional com activate/onMessage/deactivate
- Testes unitários passando
- Publicado no npm com tag `dsh-plugin`

### ④ Execução

```bash
mkdir dsh-plugin-meu && cd dsh-plugin-meu
npm init -y && npm install typescript vitest
# Criar src/index.ts com o plugin
npm run build && npm test
```

### ⑤ Gate

`npm test` retorna 100% de testes passando.

### ⑥ Concluído quando

Plugin instalado no Harness e processando mensagens corretamente.

### ⑦ Armadilhas

- Esquecer `peerDependencies` do `@deepseek-ai/dsh`
- Não adicionar tag `dsh-plugin` no GitHub (não aparece na descoberta)

---

## Passo 7 — Otimizar Inferência com FlashMLA e DeepEP

> **Estágio:** Domínio · **Origem:** Cap. 7

### ① Objetivo

Instalar e benchmarkar FlashMLA para kernels de atenção otimizados.

### ② Pré-requisito

GPU SM90+ (Hopper/Blackwell), CUDA 12.8+, PyTorch 2.0+

### ③ Entregas

- FlashMLA compilado e instalado
- Benchmark de throughput documentado
- Comparação FP8 vs BF16 em uso de memória

### ④ Execução

```bash
git clone https://github.com/deepseek-ai/FlashMLA.git
cd flash-mla && pip install -v .
python tests/test_flash_mla_dense_decoding.py
```

### ⑤ Gate

Benchmark retorna throughput > 100 TFLOPS em GPU suportada.

### ⑥ Concluído quando

FlashMLA rodando e demonstrando melhoria de performance sobre pytorch padrão.

### ⑦ Armadilhas

- Rodar em GPU SM80 (A100) — FlashMLA requer SM90+ (H100/H200)
- CUDA version mismatch (requer 12.8+)

---

## Passo 8 — Deploy e Otimização de Custo

> **Estágio:** Domínio · **Origem:** Cap. 8

### ① Objetivo

Configurar deploy local com SGLang e implementar cache de respostas.

### ② Pré-requisito

GPU disponível, Docker instalado (opcional)

### ③ Entregas

- Servidor SGLang rodando com DeepSeek-V4-Flash
- Script de monitoramento de custos
- Cache de respostas implementado

### ④ Execução

```bash
pip install sglang[all]
python3 -m sglang.launch_server --model deepseek-ai/DeepSeek-R1-Distill-Qwen-32B --tp 2
```

### ⑤ Gate

Servidor responde em `http://localhost:30000/v1/chat/completions`.

### ⑥ Concluído quando

Custo mensal estimado documentado e cache reduzindo chamadas em >30%.

### ⑦ Armadilhas

- DeepSeek-V3 precisa 8× H100 (não roda em 1× A100)
- Esquecer `--tp` (tensor parallelism) para modelos grandes
