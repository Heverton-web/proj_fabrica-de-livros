# Relatório FLUXO 2 — Campanhas — 2026-08-09

## Resumo Executivo
- **Status:** ⚠️ FALHA PARCIAL
- **Materiais processados:** 0/17
- **Coleção:** oh-my (Oh My Pi)

---

## Itens Criados

| Material | Instagram | LinkedIn | E-mails | WhatsApp | Status |
|----------|-----------|----------|---------|----------|--------|
| *(nenhum)* | — | — | — | — | ❌ |

---

## Itens NÃO Criados (e motivos)

| Material | Motivo | Ação Recomendada |
|----------|--------|------------------|
| Todos (17 materiais) | Script `criar-campanha.py` não foi executado nesta sessão | Rodar: `python scripts/criar-campanha.py --completo oh-my` |

---

## Validações Executadas

| Validação | Resultado |
|-----------|-----------|
| R-CP-1 (Artes suficientes) | — (não executado) |
| R-CP-2 (Textos completos) | — (não executado) |
| R-CP-3 (Artes por formato) | — (não executado) |
| R-CP-4 (Cronogramas completos) | — (não executado) |
| R-CP-5 (Cronogramas válidos) | — (não executado) |

---

## Estrutura Esperada (quando executado)

```text
output/oh-my/campanhas/
├── oh-my--art-01-que-coding/
│   ├── redes-sociais/instagram/ (7 posts + 7 stories)
│   ├── redes-sociais/linkedin/ (7 posts)
│   ├── canais-comunicacao/emails/ (5 e-mails)
│   └── canais-comunicacao/whatsapp/ (4 mensagens)
├── oh-my--eb-01-que-coding/
│   └── ...
└── (17 materiais no total)
```

---

## Pendências

| # | Pendência | Prioridade |
|---|-----------|------------|
| 1 | Executar `/campanha-completa oh-my` | ALTA |
| 2 | Validar com `validar-campanha.py --estrito` | ALTA |
| 3 | Personalizar copy (REGRA 12) | Média |

---

*Relatório gerado automaticamente pelo `/produzir-obra-completa`*
