# RELATÓRIO DE SESSÃO — Pacote kit-fundacao-aidd: 5 Praticas de Engenharia Generalizadas

> **Data:** 2026-08-12
> **Projeto:** Fábrica Agêntica de Publicações

---

## 1. Contexto

Extracao e generalizacao das decisoes de engenharia documentadas em docs/plano-adaptacao-metodo-eita-senioridade.md (confirmado aplicado: 'senioridade' em 48 arquivos da esteira) e docs/manual-replicar-praticas-acima-media.md (Builder!=Critic, critico deterministico, registro declarativo, hook nunca-vermelho, postmortem-que-vira-teste - todas com implementacao real confirmada nesta fabrica). Empacotadas num repositorio proprio (kit-fundacao-aidd, privado no GitHub) instalavel via submodule em qualquer projeto novo ou existente, com instalador ADITIVO: nunca remove/sobrescreve arquivo ja configurado, sempre explica antes de gravar, dry-run por padrao. Doc da matriz de senioridade tratado como caso de uso da Peca 3 (registro declarativo aplicado a um eixo perfil/tier), sem virar modulo proprio.

---

## 2. Bugs Descobertos e Corrigidos

### candidatos_registro_declarativo do analisador incluia __name__ (idiom if __name__=="__main__": presente em quase todo script Python)

- **Causa:** candidatos_registro_declarativo do analisador incluia __name__ (idiom if __name__=="__main__": presente em quase todo script Python)
- **Fix:** adicionado filtro VARS_IGNORADAS + teste de regressao test_ignora_idiom_name_main_como_falso_positivo
- **Arquivo:** `tooling/kit-fundacao-aidd/analisar-projeto.py`

---

## 3. Arquivos Alterados

- `melhorias/12-08--kit-fundacao-aidd.md`
- `.gitmodules`
- `tooling/kit-fundacao-aidd (submodule novo, repo https://github.com/Heverton-web/kit-fundacao-aidd)`

---

## 4. Validações

- kit-fundacao-aidd: 21/21 testes (pytest) apos o fix do falso-positivo
- proj_fabrica-de-livros: 665/665 testes (pytest) apos adicionar o submodule
- analisar-projeto.py rodado neste repo em modo diagnostico: nao propos nenhuma acao destrutiva, reconheceu hook pre-commit existente (so pode anexar), convencao .claude/agents e postmortem no CLAUDE.md

---

## 5. Commits

- `95b002b feat: kit-fundacao-aidd - 5 praticas de engenharia generalizadas`
- `e99d3c1 fix: ignora idiom __name__ como falso-positivo`

---

## 6. Resumo de Entregas

- Repo privado github.com/Heverton-web/kit-fundacao-aidd com as 5 pecas generalizadas (agents/, scripts/, hooks/, templates/, skills/) + analisar-projeto.py (diagnostico read-only) + instalar.py (aditivo, dry-run por padrao, nunca sobrescreve)
- Submodule registrado em tooling/kit-fundacao-aidd
- Suite de aceite rodada neste projeto sem propor nenhuma remocao/sobrescrita

---

*Relatório gerado em 2026-08-12 — Fábrica Agêntica de Publicações*
