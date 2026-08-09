---
name: sincronizar-maquina-vendas
description: >
  Sincroniza uma máquina de vendas já existente (output/<hub>/maquina, 1 por
  coleção) com o template corrigido (templates/maquina/), propagando o fix da
  rota /api/checkout, o checkout com nome/e-mail via fetch, o produto default
  alinhado ao config/produtos.json, o BACKEND_URL no .env.example e o
  re-snapshot das campanhas da coleção (maquina/campanhas/).
  Use quando uma máquina for gerada ANTES da correção do checkout — sintomas:
  rota /api/checkout inexistente (404 no botão PAGAR), checkout page com
  <form action method="POST"> sem campos, ou copy genérica de nicho.
  Triggers: "sincronizar maquina", "atualizar maquina de vendas", "fix checkout
  maquina", "máquina com checkout quebrado", "replicar template na maquina"
---

# Sincronizar Máquina de Vendas

Propaga as correções do template para uma máquina de vendas existente, sem
perder a personalização por nicho já feita.

## Quando usar

| Sintoma | Causa raiz |
|---------|-----------|
| `/checkout` dá 404 ao clicar PAGAR | Rota `/api/checkout` ausente (máquina gerada antes do fix) |
| Checkout retorna 500 sempre | `checkout/page.tsx` antigo posta form urlencoded vazio — quebra no `request.json()` |
| Produto errado no funil/analytics | `produto` default da rota não alinhado ao `config/produtos.json` |
| Copy genérica ("Autor Digital") | Máquina não personalizada por nicho |

## Passo a passo

> **Diretório de trabalho:** os passos 2–3 rodam da **raiz do projeto**; os
> passos 4–7 rodam de dentro da máquina. Execute os `cd` indicados.

1. **Identificar a máquina**: `output/<slug-colecao>/maquina/` (o hub é o
   primeiro segmento do slug da obra — ex.: `livros/ia-agentica-desbloqueada`
   → `output/ia-agentica-desbloqueada/maquina/`).
2. **Sincronizar a rota** (da raiz do projeto, se ausente ou antiga):
   ```bash
   cd <raiz-do-projeto>
   cp templates/maquina/frontend/app/api/checkout/route.ts output/<slug-colecao>/maquina/frontend/app/api/checkout/
   ```
   Substituir o `produto` default pelo slug real do produto core (passo 4).
3. **Sincronizar a página de checkout** (da raiz do projeto):
   ```bash
   cp templates/maquina/frontend/app/checkout/page.tsx output/<slug-colecao>/maquina/frontend/app/checkout/
   ```
   **Manter a copy personalizada do nicho** (título, benefícios, preço) — o
   template é genérico.
4. **Alinhar o produto default** (dentro da máquina):
   ```bash
   cd output/<slug-colecao>/maquina
   python -c "import json; d=json.load(open('config/produtos.json',encoding='utf-8')); \
   [print(p['slug'], '|', p['tipo'], '|', p['preco']) for p in d['produtos']]"
   ```
   Editar `frontend/app/api/checkout/route.ts`: o `default(...)` do campo
   `produto` deve ser o slug do produto core (ex.: `dentista-gestor-livro`).
5. **Garantir BACKEND_URL no .env.example** (se ausente): adicionar
   `BACKEND_URL=http://127.0.0.1:8000` e `NEXT_PUBLIC_BACKEND_URL=...`.
6. **Re-snapshot das campanhas** (campanhas mudaram desde a geração?):
   ```bash
   python scripts/criar-maquina-vendas.py <slug-da-obra> --tipo completo
   # resposta "s" para sobrescrever a MESMA obra — recria com campanhas atuais
   ```
   Alternativa manual (só o snapshot):
   ```bash
   rm -rf output/<slug-colecao>/maquina/campanhas
   cp -r output/<slug-colecao>/campanhas output/<slug-colecao>/maquina/campanhas
   ```
   Depois conferir `campanhas/snapshot.json` (atualizado_em da campanha).
7. **Documentar a rota no README.md** da máquina (tabela de rotas + aviso para
   não remover `/api/checkout`).
8. **Verificar** (com frontend e backend no ar):
   ```bash
   curl -s -X POST http://localhost:3000/api/checkout \
     -H "Content-Type: application/json" \
     -d '{"nome":"Teste","email":"teste@exemplo.com"}'
   # Esperado: {"success":true,...,"valor":97}
   curl http://localhost:8000/api/leads   # lead criado com produto correto
   ```

## Armadilhas

- **Não usar `<form action method="POST">`**: a rota lê `request.json()`; form
  urlencoded vazio sempre retorna 500. Usar client component com `fetch`.
- **Não deixar o `produto` default com o slug da obra**: alinhar ao slug de
  `config/produtos.json` senão o funil agrupa errado.
- **Leads de teste poluem o banco do backend**: ficam em
  `backend/data/vendas.db` (NÃO em `database/maquina.db`) — limpar após validar:
  ```bash
  python -c "import sqlite3; c=sqlite3.connect('backend/data/vendas.db'); \
  c.execute(\"DELETE FROM leads WHERE email LIKE '%teste@exemplo.com'\"); c.commit()"
  ```
- **Não apagar a personalização por nicho**: o template nasce genérico; a
  sincronização deve trocar SÓ os arquivos de checkout, preservando copy do nicho.

## Referência

- Rota corrigida: `templates/maquina/frontend/app/api/checkout/route.ts`
- Página corrigida: `templates/maquina/frontend/app/checkout/page.tsx`
- Testes de contrato: `tests/test_maquina_checkout.py`
- Spec: `SPEC_MAQUINA_VENDAS.md` (R11/R12/R13)
