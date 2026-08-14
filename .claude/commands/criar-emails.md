---
description: Gera a SEQUÊNCIA DE E-MAILS de nutrição (1 por card do playbook + abertura + oferta), fechando o funil aberto pelo lead magnet. Contrato em SPEC_EMAILS.md.
---

# /criar-emails `<prefixo>/<slug>` `[--intervalo N]`

**Pré-condição:** playbook existente **ou** livro com capítulos EITA.
**CTA obrigatório** (R-EM-2) — pergunte a URL se o operador não informou.

## Passo 1 — Esqueleto + cronograma (0 token)

```
python scripts/gerar-sequencia-emails.py <prefixo>/<slug> --cta-url <url> --intervalo 2
```

Gera `emails/email_NN.md`, `sequencia.md` e `plano.json` (índice, tipo, dia).

## Passo 2 — Polimento de copy (opcional — a frase de ligação já nasce pronta)

A frase de ligação (promessa do lead magnet / armadilha → passo prático /
recapitulação) já sai por rodízio determinístico de template
(`FRASES_LIGACAO_*` em `gerar-sequencia-emails.py`) — não há mais marcador
`POLIMENTO-LLM` pendente por default. Só reescreva a mão se o tom ficar
repetitivo entre sequências da mesma coleção (risco documentado do rodízio
fixo). Se precisar reescrever, restrições duras:

- máx. 250 palavras por e-mail (R-EM-4)
- **exatamente 1** link por e-mail — não acrescente um segundo (R-EM-2)
- assunto ≤ 60 caracteres (R-EM-1)
- segunda pessoa, sem saudação genérica (R2)

Não invente conteúdo: cada e-mail já traz a armadilha, o objetivo e o gate do
card correspondente. O polimento é ligação, não geração.

## Passo 3 — Gate

```
python scripts/validar-emails.py emails/<slug>--eml --estrito
```

## Passo 4 — Coleção

```
python scripts/colecao.py --sincronizar --slug <prefixo>/<slug>
```

## Passo 5 — Relatório telegráfico

Total de e-mails, duração da sequência em dias, veredito do gate.

## Verificação de entrega (sempre)

```
python scripts/validar-artefatos.py --todos --estrito
```

Gerar o arquivo não prova que ele abre. Este passo confere assinatura, integridade
e comprimento de caminho (MAX_PATH do Windows). Só depois:

```
python scripts/empacotar-colecao.py "<coleção>"
```
