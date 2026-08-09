# Relatório de Produção — SDLC AI-first

**Slug:** `livros/sdlc-ai-first`
**Comando:** `/produzir-obra-completa livros/sdlc-ai-first`
**Data:** 02/08/2026
**Autor:** Heverton Eduardo Peres

---

## 1. Obra principal (Livro)

| Métrica | Valor |
|---|---|
| Título | SDLC AI-first: O Ciclo de Vida do Software na Era dos Agentes |
| Tamanho | G (5 Partes · 10 Capítulos) |
| Capítulos | 10 |
| Caracteres (`livro_final.md`) | 375.297 |
| Páginas estimadas | 150,1 |
| **Páginas do PDF** | **234** |
| Referências por capítulo | 20 (R4 ✅) |
| Diagramas Mermaid renderizados | 11 PNG |
| CI de código | 100% aprovado (146 blocos verificáveis) |
| **Veredito da auditoria** | **CONFORME** (R1-R4, R9-R15 ✅) |

**Artefatos:**
- `output/livros/sdlc-ai-first/livro_final.md`
- `output/livros/sdlc-ai-first/livro_final.pdf` (234 p., 3,4 MB)
- `output/livros/sdlc-ai-first/imagens/capa_livro.png` + `thumbnail_livro.png`

## 2. Artigos científicos (5)

| # | Título | Páginas | Veredito | PDF |
|---|---|---|---|---|
| 01 | Do SDLC Clássico ao AI-first + O Controlador de Voo | ~10,3 | CONFORME | ✅ 155 KB |
| 02 | Plano de Voo: Spec Executável + Design de Domínio | ~9,2 | CONFORME | ✅ 154 KB |
| 03 | Os Motores: Harness, Skills, MCPs e Worktrees + Radar | ~8,7 | CONFORME | ✅ |
| 04 | Autorização de Pouso: Release + Debriefing | ~8,5 | CONFORME | ✅ |
| 05 | Combustível: Economia de Tokens + Futuro do SDLC | ~8,5 | CONFORME | ✅ |

Estrutura IMRaD (4 seções), citação autor-data NBR 10520, 20 refs por seção, resumo/abstract PT+EN em `artigo_metadados.json`.

## 3. E-books (8)

| # | Título | Caracteres | EBOOK-LEN | EPUB |
|---|---|---|---|---|
| 01 | Do SDLC Clássico ao AI-first | 46.513 | ✅ | ✅ 134 KB |
| 02 | O Controlador de Voo | 46.295 | ✅ | ✅ 140 KB |
| 03 | Plano de Voo: Spec Executável | 46.603 | ✅ | ✅ 129 KB |
| 04 | Cartografia do Domínio | 46.561 | ✅ | ✅ 139 KB |
| 05 | Os Motores: Harness, Skills, MCPs | 45.846 | ✅ | ✅ 133 KB |
| 06 | O Radar: Verificação Adversarial | 46.211 | ✅ | ✅ 128 KB |
| 07 | Autorização de Pouso: Release | 45.064 | ✅ | ✅ 133 KB |
| 08 | Debriefing: Aprendizado Contínuo | 130.676 | ✅ | ✅ 202 KB |

Cada e-book com capa 1:1,6 + thumbnail e CTA final ("Próximos Passos").

## 4. Distribuição

**Pacote:** `output/livros/sdlc-ai-first/distribuicao/` (6,7 MB)

```
distribuicao/
├── livro_final.pdf          ← obra completa
├── capa.png / thumbnail.png
├── artigos/artigo_1..5.pdf  ← 5 artigos científicos
├── ebooks/ebook_1..8.epub   ← 8 e-books
├── ebooks/capas/            ← capas + thumbnails dos e-books
├── README.md
└── LICENSE
```

## 5. Checklist de requisitos (obra principal)

| Req | Descrição | Status |
|---|---|---|
| R1 | 10 capítulos | ✅ |
| R2 | 150+ páginas (375K caracteres) | ✅ 150,1 p. est. / 234 p. PDF |
| R3 | 7 seções EITA-V2 por capítulo | ✅ |
| R4 | 20 referências ABNT por capítulo | ✅ |
| R9 | Sem horizontal rules | ✅ |
| R10 | ≥3 citações inline [N] | ✅ |
| R11 | Diagrama Mermaid na Ilustra | ✅ |
| R12 | Código validado na Técnica | ✅ |
| R13 | Sem truncamento/pendências | ✅ |
| R14 | Rastreabilidade [N] ↔ refs | ✅ |
| R15 | Refs em ordem numérica (NBR 6023) | ✅ |

## 6. Observações

- **Metáfora condutora:** Torre de Controle de Tráfego Aéreo — cada fase é um voo que decola com plano aprovado e aterra com verificação.
- **Persona do leitor:** Comandante de Operações de Software.
- **Alertas não bloqueantes:** 14 pares de parágrafos com alta similaridade entre capítulos (referências bibliográficas compartilhadas, esperado em obra única); grafia inconsistente de termos acentuados em código/comentários (padrão técnico).
- **Pipeline:** Pandoc → `.typ` → Typst (100% local), com fallback CloudConvert disponível.

---

*Relatório gerado automaticamente pela esteira da Fábrica Agêntica de Publicações.*
