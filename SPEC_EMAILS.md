# SPEC_EMAILS — Contrato da Sequência de E-mails (V5)

> Fecha o funil que o lead magnet abre. Esqueleto determinístico + polimento de
> copy marcado por `<!-- POLIMENTO-LLM -->` (custo baixo, em lote).

## 1. Estrutura da sequência

| Posição | Tipo | Fonte | Momento |
|---|---|---|---|
| 1 | **Abertura** (entrega do material) | promessa do lead magnet | imediato |
| 2..N-1 | **Nutrição** (1 por card do playbook) | ⑦ armadilha + ① objetivo + ⑤ gate + ③ entrega | dia `(i-1) × intervalo` |
| N | **Fechamento** (oferta) | obra-mãe | último dia |

Intervalo padrão: **2 dias**. Livro G (12 capítulos) → 14 e-mails / 26 dias.

## 2. Regras (gate: `scripts/validar-emails.py`)

| Regra | Enunciado |
|---|---|
| **R-EM-1** | Assunto presente e com no máximo 60 caracteres |
| **R-EM-2** | **Exatamente 1** CTA por e-mail, com UTM (`utm_source=email`) |
| **R-EM-3** | Sequência tem abertura + nutrição + fechamento (mín. 3 e-mails) |
| **R-EM-4** | Nenhum e-mail passa de 250 palavras (código e comentários não contam) |

Um CTA por e-mail é regra dura, não estilo: dois links dividem o clique.

## 3. Saída

```
output/emails/<slug-mae>--eml/
├── config_obra.json    tipo_obra=emails, cta_url, intervalo_dias
├── plano.json          cronograma (índice, tipo, dia, passo_fonte)
├── emails/email_NN.md  1 arquivo por e-mail
├── sequencia.md        todos concatenados (revisão em 1 leitura)
└── revisao/
```

## 4. Pipeline

```bash
python scripts/gerar-sequencia-emails.py livros/<slug> --cta-url https://exemplo.com/livro
python scripts/validar-emails.py emails/<slug>--eml --estrito
```

Polimento: buscar `POLIMENTO-LLM` nos `email_NN.md` e reescrever em lote —
1 chamada por lote de 5 e-mails, não 1 por e-mail.

## 5. Custo

| Etapa | Custo |
|---|---|
| Esqueleto + cronograma + UTMs | **0** |
| Polimento de copy | ~600 tokens por e-mail |
