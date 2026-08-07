# SPEC: Aplicar Token Economy em Qualquer Projeto

**Versão:** 1.0
**Data:** 2026-08-07
**Status:** Ativo

---

## 1. Objetivo

Criar um comando único que aplica infraestrutura completa de economia de tokens
em QUALQUER projeto (novo ou existente), de QUALQUER categoria, via QUALQUER
ferramenta de IA.

## 2. Escopo

### O que é aplicado

| Componente | O que faz | Onde vai |
|---|---|---|
| Submodule `.token-economy/` | 9 skills + configs | Raiz do projeto |
| Skills de economia | lean-ctx, headroom, caveman, etc. | `.claude/skills/` (symlink) |
| Code Review Graph | Grafo de navegação | `.code-review-graph/` |
| Arquivo de instruções | Regras do projeto | Hardlink multi-IDE |
| Junctions multi-IDE | Portabilidade | `.agents/`, `agentic/` |
| pytest.ini | Config de testes | Raiz do projeto |
| requirements.txt | Dependências | Raiz do projeto |

### Tipos de projeto suportados

- Web (React, Vue, Angular, Next.js, etc.)
- Backend (Node.js, Python, Go, Rust, Java, etc.)
- Mobile (React Native, Flutter, Swift, Kotlin, etc.)
- Data (pipelines, ML, analytics, etc.)
- AI/ML (LLMs, RAG, agents, etc.)
- Embedded (C, C++, Arduino, etc.)
- Qualquer outro

### Ferramentas de IA suportadas

Claude Code, Cursor, Windsurf, Copilot, Codex, OpenClaw, MiMoCode,
Cline, Roo Code, Augment, Continue, Aider, e qualquer outra que leia
arquivos de instrução na raiz.

## 3. Comando

```
/aplicar-token-economy [caminho-do-projeto]
```

Se omitido `[caminho-do-projeto]`, usa o diretório atual.

## 4. Fluxo Autônomo

```
1. Detectar tipo de projeto (linguagem, framework, testes)
2. Clonar/inicializar submodule .token-economy/
3. Criar symlinks/junctions para skills
4. Configurar code-review-graph
5. Criar/atualizar arquivo de instruções (multi-IDE)
6. Criar pytest.ini e requirements.txt (se não existem)
7. Rodar validação (testes + grafo)
8. Reportar resultado
```

## 5. Requisitos

- Git instalado
- Python 3.8+ (para code-review-graph)
- Acesso a git@github.com:Heverton-web/token-economy-shared.git
- Permissão de escrita no projeto alvo

## 6. Saída Esperada

```
=== Token Economy Aplicado ===

Projeto: /caminho/do/projeto
Tipo: python/nextjs/go/etc
Framework: django/react/fastapi/etc

Componentes instalados:
  [OK] Submodule .token-economy/
  [OK] 9 skills de economia
  [OK] Code Review Graph (357 nós)
  [OK] Arquivo de instruções (multi-IDE)
  [OK] Junctions .agents/ e agentic/
  [OK] pytest.ini
  [OK] requirements.txt

Economia estimada: 25-35% de tokens
```

## 7. Idempotência

O comando é 100% idempotente — pode ser rodado múltiplas vezes sem efeito colateral.
Se um componente já existe, é pulado. Se está corrompido, é recriado.

## 8. Rollback

Para desfazer:
```bash
git submodule deinit -f .token-economy
git rm -f .token-economy
rm -rf .git/modules/.token-economy
rm -f pytest.ini requirements.txt
# Junctions/symlinks são removidos manualmente
```
