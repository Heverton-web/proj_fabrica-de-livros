# Parecer de Revisão Técnica — Livro 11

**Obra:** O engenheiro(a) AIDD acima da média: arquitetura de sistemas, portfólio e mercado em 2026
**Slug:** `livros/11-engenheiro-aidd-acima-da-media-arquitetura-de-sistemas-portfolio-e-mercado-em-2026`
**Data:** 06/08/2026
**Tipo:** Livro (tamanho G) — Série Técnica, Parte IV — Mestria e carreira

## 1. Escopo da auditoria

- `scripts/auditar-obra.py <slug>` — requisitos R1–R15 automatizáveis
- `scripts/validar-codigo.py <slug>` — CI de blocos de código
- `scripts/renderizar-diagramas.py <slug> --validar` — sintaxe Mermaid
- Rastreabilidade manual: citações `[N]` ↔ seção 7 de referências

## 2. Resultado: CONFORME

| Regra | Verificação | Status |
|---|---|---|
| R1 | Mínimo 12 capítulos | OK (12) |
| R2 | Mínimo 120 páginas (~300.000 caracteres) | OK (300.696) |
| R3 | 7 seções EITA-V2 por capítulo | OK |
| R4 | Mínimo 20 referências ABNT por capítulo | OK (20/cap) |
| R9 | Ausência de horizontal rules | OK |
| R10 | Mínimo 3 citações inline `[N]` por capítulo | OK |
| R11 | Mínimo 1 diagrama Mermaid na seção Ilustra | OK (12/12 válidos) |
| R12 | Bloco de código na seção Técnica | OK |
| R13 | Sem truncamento nem pendências | OK |
| R14 | Rastreabilidade `[N]` texto ↔ referências | OK (sem órfãs) |
| R15 | Referências em ordem numérica ascendente (NBR 6023) | OK |
| CI | Sintaxe de blocos de código | OK (100%) |

## 3. Correções aplicadas durante a revisão

1. **Normalização de referências** — deduplicação por conteúdo e renumeração pela ordem de
   primeira citação (script `_normalizar_refs_livro11.py`), eliminando refs duplicadas.
2. **Citações órfãs** — blocos de síntese citavam `[108]/[109]` além das entradas novas;
   remapeadas para entradas não citadas e novas fontes do dossiê
   (script `_corrigir_refs_livro11.py`).
3. **Entradas não citadas** — frases de síntese finais citando refs `[19]/[20]` antes da
   Conclusão (script `_sintese_final_livro11.py`), garantindo R14 sem órfãs nem refs mortas.
4. **Volume (R2)** — duas rodadas de expansão (subseções `### Aprofundamento` + parágrafos
   finais) elevando o corpo de 212.256 → 300.696 caracteres, citando apenas refs existentes.

## 4. Métricas finais

- **12 capítulos** EITA-V2, 4 Partes (Mudança de Papel, Arquitetura, Portfólio, Mercado)
- **300.696 caracteres** de corpo (auditoria) — ~120 páginas
- **20 referências ABNT por capítulo**, todas citadas, nenhuma órfã
- **12 diagramas Mermaid** válidos; **10 ilustrações 2D flat** (accent `#f0a500`)
- **CI de código: 100%**

## 5. Conclusão

A obra atende integralmente às regras da Fábrica (REGRA 3 — autonomia total; REGRA 6 —
capítulo EITA obrigatório; REGRA 7/8 — capa padrão e cores unificadas) e está **aprovada
para compilação ABNT e exportação em PDF**.
