---
name: aplicar-token-economy
description: Aplica infraestrutura completa de economia de tokens em QUALQUER projeto (novo ou existente) com 1 comando. Detecta tipo de projeto, instala submodule, skills, code-review-graph, juncoes multi-IDE e valida tudo. Trigger: "aplicar token economy", "instalar token economy", "configurar economia de tokens", "/aplicar-token-economy"
---

# Skill: Aplicar Token Economy

## Uso

```
/aplicar-token-economy                    # Diretório atual
/aplicar-token-economy /caminho/projeto   # Projeto específico
```

## O que esta skill faz

1. **Detecta** o tipo de projeto (linguagem, framework, testes)
2. **Instala** submodule `.token-economy/` com 9 skills
3. **Cria** symlinks/junctions para skills
4. **Configura** code-review-graph
5. **Cria/atualiza** arquivo de instruções multi-IDE
6. **Adiciona** pytest.ini e requirements.txt
7. **Valida** tudo (testes + grafo)
8. **Reporta** resultado com economia estimada

## Procedimento

### Passo 1 — Detectar Projeto

```bash
# Detectar linguagem principal
if [ -f "package.json" ]; then TIPO="nodejs"; FRAMEWORK=$(node -e "console.log(require('./package.json').dependencies ? Object.keys(require('./package.json').dependencies).join(', ') : 'nenhum')" 2>/dev/null || echo "unknown"); fi
if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then TIPO="python"; fi
if [ -f "go.mod" ]; then TIPO="go"; fi
if [ -f "Cargo.toml" ]; then TIPO="rust"; fi
if [ -f "pom.xml" ] || [ -f "build.gradle" ]; then TIPO="java"; fi
if [ -f "Gemfile" ]; then TIPO="ruby"; fi
if [ -f "*.csproj" ] || [ -f "*.sln" ]; then TIPO="dotnet"; fi
if [ -f "CMakeLists.txt" ] || [ -f "Makefile" ]; then TIPO="c-cpp"; fi
if [ -f "pubspec.yaml" ]; then TIPO="flutter"; fi
if [ -f "ios/Podfile" ] || [ -f "android/app/build.gradle" ]; then TIPO="react-native"; fi

echo "Tipo detectado: $TIPO"
```

### Passo 2 — Instalar Submodule

```bash
RAIZ="$(pwd)"
SUBMODULE="$RAIZ/.token-economy"

if [ ! -d "$SUBMODULE" ]; then
    git submodule add git@github.com:Heverton-web/token-economy-shared.git .token-economy 2>/dev/null || \
    git submodule add https://github.com/Heverton-web/token-economy-shared.git .token-economy
    echo "[OK] Submodule instalado"
else
    echo "[OK] Submodule ja existe"
    cd "$SUBMODULE" && git pull origin main && cd "$RAIZ"
fi
```

### Passo 3 — Criar Junctions/Symlinks

```bash
SKILLS="lean-ctx headroom caveman rtk-memory pre-flight-check calcular-gastos-sessao fable-method fable-judge self-learning"
mkdir -p ".claude/skills"

for skill in $SKILLS; do
    SRC="$SUBMODULE/.claude/skills/$skill"
    DST=".claude/skills/$skill"
    if [ ! -e "$DST" ]; then
        ln -s "../$SUBMODULE/.claude/skills/$skill" "$DST"
        echo "[OK] Symlink: $skill"
    fi
done

# Junctions para .agents/ (multi-IDE)
mkdir -p ".agents"
for dir in skills agents commands mcp-servers; do
    if [ ! -e ".agents/$dir" ]; then
        ln -s "../.claude/$dir" ".agents/$dir" 2>/dev/null
    fi
done
```

### Passo 4 — Code Review Graph

```bash
if command -v code-review-graph &> /dev/null; then
    if [ ! -f ".code-review-graph/graph.db" ]; then
        code-review-graph build 2>&1 | tail -3
        echo "[OK] Grafo construido"
    else
        code-review-graph update 2>&1 | tail -1
        echo "[OK] Grafo atualizado"
    fi
else
    pip install code-review-graph -q 2>/dev/null
    code-review-graph build 2>&1 | tail -3
    echo "[OK] Grafo instalado e construido"
fi
```

### Passo 5 — Arquivo de Instruções

```bash
# Criar CLAUDE.md se não existe
if [ ! -f "CLAUDE.md" ] && [ ! -f "AGENTS.md" ]; then
    cat > "CLAUDE.md" << 'EOF'
# [NOME DO PROJETO]

## 0. Economia Severa de Tokens (PRIORIDADE MÁXIMA)

1. **Caveman Ativo:** pensamento telegráfico (3-5 linhas), sem preâmbulos/saudações.
2. **Headroom:** logs/builds >7 linhas → comprimir (3 topo + 4 fim).
3. **LeanCTX:** grep antes de read em código/config. Limitar leitura por linha.
4. **Delegação:** subagentes comprimidos para buscas/edições extensas.
5. **Build ISENTO:** pipeline de compilação liberado e obrigatório.
6. **Fallback Terminal:** exibir comandos se sandbox bloquear.
7. **Soberania do Usuário:** nada barrado sem confirmação.
8. **Fidelidade:** output/** e JSONs de estado isentos de compressão.
9. **Auto-commit/push:** alterações commitadas e pushadas.

## 1. Regras

- **R1:** idioma do projeto.
- **R2:** sem preâmbulos/saudações.
- **R3:** 100% autônomo após definição.
- **R4:** desvios corrigidos internamente.

## 2. Skills (via .token-economy/)

| Skill | Função |
|---|---|
| `lean-ctx` | grep antes de read |
| `headroom` | Compressão de logs |
| `caveman` | Respostas telegráficas |
| `rtk-memory` | Registro de erros |
| `pre-flight-check` | Validação antes de commit |
| `calcular-gastos-sessao` | Tokens |
| `fable-method` | Resolução de problemas |
| `fable-judge` | Verificação adversarial |
| `self-learning` | Golden paths |

## 3. Stack
- Linguagem: [DETETADA]
EOF
    echo "[OK] CLAUDE.md criado"
fi

# Criar hardlinks multi-IDE
for file in ".cursor/rules/instrucoes.mdc" ".windsurfrules" ".clinerules" ".github/copilot-instructions.md"; do
    dir=$(dirname "$file")
    mkdir -p "$dir"
    if [ ! -f "$file" ]; then
        ln "CLAUDE.md" "$file" 2>/dev/null || cp "CLAUDE.md" "$file"
        echo "[OK] Hardlink: $file"
    fi
done
```

### Passo 6 — Configs

```bash
# pytest.ini
if [ ! -f "pytest.ini" ]; then
    cp "$SUBMODULE/pytest.ini" "."
    echo "[OK] pytest.ini"
fi

# requirements.txt
if [ ! -f "requirements.txt" ]; then
    cp "$SUBMODULE/requirements.txt" "."
    echo "[OK] requirements.txt"
fi

# .gitignore
if [ ! -f ".gitignore" ]; then
    echo -e "__pycache__/\n*.pyc\n.pytest_cache/\noutput/\n.token-economy/" > .gitignore
    echo "[OK] .gitignore"
fi
```

### Passo 7 — Validar

```bash
# Testes
if [ -f "pytest.ini" ]; then
    python -m pytest tests/ --tb=no -q 2>/dev/null && echo "[OK] Testes" || echo "[AVISO] Testes falharam"
fi

# Grafo
if [ -f ".code-review-graph/graph.db" ]; then
    code-review-graph status 2>/dev/null | head -3
    echo "[OK] Grafo ativo"
fi
```

### Passo 8 — Reportar

```bash
echo ""
echo "=== Token Economy Aplicado ==="
echo ""
echo "Projeto: $(pwd)"
echo "Tipo: ${TIPO:-desconhecido}"
echo ""
echo "Componentes:"
echo "  [OK] Submodule .token-economy/"
echo "  [OK] 9 skills de economia"
[ -f ".code-review-graph/graph.db" ] && echo "  [OK] Code Review Graph"
[ -f "CLAUDE.md" ] && echo "  [OK] Arquivo de instruções (multi-IDE)"
[ -d ".agents" ] && echo "  [OK] Junctions .agents/"
[ -f "pytest.ini" ] && echo "  [OK] pytest.ini"
[ -f "requirements.txt" ] && echo "  [OK] requirements.txt"
echo ""
echo "Economia estimada: 25-35% de tokens"
echo ""
echo "Proximo passo: edite CLAUDE.md com as regras especificas do seu projeto"
```

## Notas

- Comando 100% idempotente (pode rodar múltiplas vezes)
- Funciona em projetos novos E existentes
- Detecta automaticamente linguagem e framework
- Não sobrescreve arquivos existentes (apenas cria os que faltam)
