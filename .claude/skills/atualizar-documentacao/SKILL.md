---
name: atualizar-documentacao
description: Mantém os manuais do projeto (docs/manual-completo-fabrica.md/.pdf e docs/guia-execucao-maquina-vendas.md/.pdf) sincronizados com o estado real do projeto. Use quando os manuais estiverem desatualizados, quando algo do projeto mudar (scripts, comandos, layout do output, máquina de vendas), ou quando o usuário pedir para "atualizar os manuais", "recompilar os PDFs dos manuais", "atualizar a documentação". Também é acionada automaticamente pelos hooks do .claude/settings.json quando os fontes mudam.
---

# Atualizar Documentação (Manuais)

Recompila os manuais (MD → PDF com capa gráfica) sem regenerar nada que não
mudou. O gatilho é o `scripts/atualizar-documentacao.py`.

## Quando usar

- Manual/guia desatualizado após mudanças no projeto (scripts, comandos,
  layout série-aware, máquina de vendas, token economy, etc.).
- O usuário pedir "atualizar os manuais" ou "recompilar os PDFs".
- Depois de qualquer mudança estrutural relevante (novo script, novo comando,
  novo layout, novo tipo de obra).

## Como rodar

```bash
# Só o que mudou (comparação de mtime .md vs .pdf)
python scripts/atualizar-documentacao.py

# Recompilar tudo, ignorando mtime
python scripts/atualizar-documentacao.py --forcar

# Só se o working tree estiver sujo (usado pelos hooks)
python scripts/atualizar-documentacao.py --se-sujo --silencioso

# Um manual específico
python scripts/atualizar-documentacao.py docs/manual-completo-fabrica.md
```

## O que o script faz

1. **Capa gráfica** — `docs/imagens/capa_<manual>.png` via
   `scripts/gerar-capa.py::gerar_capa` (padrão REGRA 5: fundo matte, barras
   accent, chancela `>_ EDITORA AGÊNTICA`, badge de nível, autor e
   qualificação). Só regenera se faltar (ou `--forcar`).
2. **PDF** — `pandoc <md> -o <pdf> --pdf-engine=typst --template=templates/template.typ
   --toc --number-sections -Vcapa_imagem=... -Vcor_acento=...` e depois
   `typst compile` (nunca `pandoc --pdf-engine=typst` direto com figuras —
   bug de path absoluto no Windows).

## Registro dos manuais

Tudo em `MANUAIS` no topo do script. Para adicionar/alterar um manual, edite
o registro (título, subtítulo, `cor_acento`, `badge`) e rode
`python scripts/atualizar-documentacao.py --forcar`.

| Manual | Capa | Badge |
|---|---|---|
| `manual-completo-fabrica.md/.pdf` | `#58a6ff` (azul) | NÍVEL AVANÇADO |
| `guia-execucao-maquina-vendas.md/.pdf` | `#f0933b` (laranja) | NÍVEL INTERMEDIÁRIO |

## Regras ao editar o conteúdo dos manuais

- PT-BR estrito; sem preâmbulos/saudações (R2).
- Documente o layout **série-aware** (`output/<obra>/<tipo>/...`), sem junctions.
- Contagens (scripts/skills/comandos) devem bater com o inventário real
  (`ls scripts/`, `.claude/skills/`, `.claude/commands/`).
- A máquina de vendas: caminhos reais (`backend/app/`, `database/schema.sql`,
  `manifesto.json`, `.env` com `SMTP_PASSWORD`/`FROM_EMAIL`).
- Nunca edite o PDF à mão — edite o `.md` e rode o script.

## Hooks (automático)

O `.claude/settings.json` roda o script em `PostToolUse` quando um dos fontes
muda (`docs/*.md` dos manuais, `templates/template.typ`). Hooks nunca
bloqueiam (`|| true`). Se o script falhar, o erro aparece no log do hook —
corrija manualmente com `--forcar` e veja o stderr.
