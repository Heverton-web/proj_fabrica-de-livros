# Manual: Roteador Inteligente de LLMs Gratuitas

**Arquivo:** `scripts/task_router.py`
**Versão:** 1.0.0
**Data:** 2026-08-17
**Compatível com:** Orca/MiMoCode, Claude Code, Aider, Cursor, Windsurf, Continue

---

## O que é

O roteador inteligente detecta o tipo de tarefa pelo seu prompt e escolhe automaticamente o melhor provedor de LLM gratuito disponível. Se um provedor estourar a cota, ele faz fallback para o próximo.

---

## Pré-requisitos

1. **Python 3.8+** instalado
2. **Arquivo `.env`** com as chaves dos provedores (já existe no projeto)
3. **python-dotenv** (opcional, mas recomendado):
   ```bash
   pip install python-dotenv
   ```

---

## Passo 1 — Verificar provedores ativos

```bash
cd D:\Backup_C_trcnologia_2026-08-14\Desktop\01_Projetos_e_Desenvolvimento\proj_fabrica-de-livros
python scripts/task_router.py --status
```

**Saída esperada:**
```
============================================================
  ROTEADOR INTELIGENTE — STATUS DOS PROVEDORES
============================================================
  🟢 ATIVO | groq | uso: 0 | modelo: llama-3.3-70b-versatile
  🟢 ATIVO | google | uso: 0 | modelo: gemini-1.5-pro
  ...
  Total ativos: 13/13
============================================================
```

Se algum provedor aparecer como `🔴 INATIVO`, adicione a chave no `.env`.

---

## Passo 2 — Testar o roteamento

### Teste rápido (shell)

```bash
python scripts/task_router.py "debug this Python function"
```

**Saída:**
```
export ORCA_PROVIDER=groq
export ORCA_MODEL=llama-3.3-70b-versatile
```

### Teste em JSON

```bash
python scripts/task_router.py "escreva um poema" --json
```

**Saída:**
```json
{
  "task": "creative",
  "provider": "openrouter",
  "model": "meta-llama/lama-3.3-70b-instruct:free",
  "fallback": false
}
```

### Teste legível (PT-BR)

```bash
python scripts/task_router.py "analise estes dados" --info
```

**Saída:**
```
Task: analysis
Provider: google
Model: gemini-1.5-pro
```

---

## Passo 3 — Usar no shell (recomendado)

### Git Bash / Linux / Mac

Adicione ao `~/.bashrc` ou `~/.zshrc`:

```bash
# Roteador inteligente de LLMs
alias ai='eval $(python D:/Backup_C_trcnologia_2026-08-14/Desktop/01_Projetos_e_Desenvolvimento/proj_fabrica-de-livros/scripts/task_router.py)'
```

Depois recarregue:
```bash
source ~/.bashrc
```

**Uso:**
```bash
ai "debug this function"
# → export ORCA_PROVIDER=groq
# → export ORCA_MODEL=llama-3.3-70b-versatile

orca  # inicia com groq configurado
```

### PowerShell

Adicione ao `$PROFILE`:

```powershell
function ai {
    $result = python D:\Backup_C_trcnologia_2026-08-14\Desktop\01_Projetos_e_Desenvolvimento\proj_fabrica-de-livros\scripts\task_router.py $args
    $result | ForEach-Object {
        if ($_ -match 'export (\w+)=(.+)') {
            [Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process")
        }
    }
    Write-Host "Provider: $env:ORCA_PROVIDER | Model: $env:ORCA_MODEL"
}
```

**Uso:**
```powershell
ai "escreva um poema"
# Provider: openrouter | Model: meta-llama/llama-3.3-70b-instruct:free

orca
```

---

## Passo 4 — Integrar com Orca/MiMoCode

### Método A: Pré-sessão (recomendado)

1. Abra o terminal
2. Rote o comando:
   ```bash
   eval $(python scripts/task_router.py "sua tarefa aqui")
   ```
3. Inicie o Orca:
   ```bash
   orca
   ```
4. O Orca usará o provedor/modelo definidos

### Método B: Wrapper

Crie um script `start-ai.sh`:

```bash
#!/bin/bash
cd D:/Backup_C_trcnologia_2026-08-14/Desktop/01_Projetos_e_Desenvolvimento/proj_fabrica-de-livros
eval $(python scripts/task_router.py "$*")
echo "Provider: $ORCA_PROVIDER | Model: $ORCA_MODEL"
orca
```

Uso:
```bash
./start-ai.sh "debug this Python function"
```

### Método C: Usar o router como referência

Se não quiser automação, rode o router e use a informação manualmente:

```bash
python scripts/task_router.py "minha tarefa" --info
# → Provider: groq | Model: llama-3.3-70b-versatile
# → Then select groq in Orca UI → Settings → Providers
```

---

## Passo 5 — Gerenciar quotas

### Ver quanto já usou

```bash
python scripts/task_router.py --status
```

Mostra `uso: N` para cada provedor.

### Resetar quotas

Se um provedor bloqueou por quota mas já liberou:

```bash
python scripts/task_router.py --reset
```

### Onde fica o estado

```
~/.task_router/quota.json    ← estado de quotas
~/.task_router/usage.log     ← log de uso (append)
```

---

## Tabela de Roteamento

| Tarefa | Provedores (ordem) | Modelo |
|--------|-------------------|--------|
| **coding** | groq → cerebras → google → openrouter → nvidia | llama-3.3-70b-versatile |
| **reasoning** | google → groq → nvidia → openrouter → cerebras | gemini-1.5-pro |
| **creative** | openrouter → google → groq → siliconflow → nvidia | llama-3.3-70b-instruct:free |
| **analysis** | google → groq → cerebras → openrouter → nvidia | gemini-1.5-pro |
| **chat** | groq → google → openrouter → huggingface → siliconflow | llama-3.3-70b-versatile |
| **embedding** | huggingface → siliconflow → cohere → nvidia → fireworks | Phi-3.5-mini-instruct |
| **vision** | google → openrouter → nvidia → siliconflow → fireworks | gemini-1.5-pro |

---

## Comandos de Referência

| Comando | Descrição |
|---------|-----------|
| `python scripts/task_router.py "prompt"` | Roteia e imprime export shell |
| `python scripts/task_router.py "prompt" --json` | Saída em JSON |
| `python scripts/task_router.py "prompt" --info` | Saída legível PT-BR |
| `python scripts/task_router.py --status` | Mostra provedores ativos e quotas |
| `python scripts/task_router.py --reset` | Reseta todas as quotas |
| `python scripts/task_router.py --help` | Mostra ajuda |

---

## Solução de Problemas

### "Provider: openrouter | fallback: true"

Significa que nenhum provedor da lista preferida tem chave. Verifique o `.env`.

### Provedor bloqueado mas cota já liberou

```bash
python scripts/task_router.py --reset
```

### python-dotenv não carrega o .env

Instale:
```bash
pip install python-dotenv
```

Ou exporte manualmente:
```bash
export $(cat .env | xargs)
```

### Modelo não é suportado pelo Orca

O router define `ORCA_MODEL`, mas o Orca só aceita modelos da sua lista interna. Nesse caso, use `--info` e selecione manualmente no Orca UI → Settings → Providers.

---

## Arquivos Relacionados

| Arquivo | Descrição |
|---------|-----------|
| `scripts/task_router.py` | Script principal |
| `scripts/detectar_llms_gratuitas.py` | Detector de provedores (anterior) |
| `.env` | Chaves dos provedores |
| `~/.task_router/quota.json` | Estado de quotas |
| `melhorias/2026-08-17-roteador-inteligente-llm.md` | Plano de implementação |
