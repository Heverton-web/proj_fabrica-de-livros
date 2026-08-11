# Playbook de Campanhas — Fábrica Agêntica (Marketing na Era Digital)

Este playbook consolida as diretrizes fundamentais do livro *"Marketing na Era Digital: Conceitos, Plataformas e Estratégias"* (Martha Gabriel & Rafael Kiso) e as traduz para o modelo operacional V5.3 do projeto **fabrica-de-livros**.

Ele serve como o "molde mestre" para que a IA (e operadores) gerem campanhas coerentes, persuasivas e multicanal, sem escrever código nesta etapa.

---

## 1. Princípios Diretores (O *Mindset* da Era Digital)

As campanhas geradas pela fábrica não podem ser "panfletagem digital". Elas devem respeitar 3 leis inegociáveis do livro:
1. **Presença Omnichannel (Plataformas):** O usuário tem experiências fragmentadas. A mensagem deve ser fluida entre Redes Sociais, E-mails e a Máquina de Vendas (Next.js/FastAPI).
2. **Inbound & Geração de Valor (Conceitos):** Cada conteúdo deve resolver uma dor real (educar) antes de pedir uma ação (vender). O Lead Magnet é a porta de entrada.
3. **Mensuração Contínua (Estratégias):** O uso rigoroso de CTAs rastreáveis e gatilhos de dados (`/api/leads`).

## 2. A Arquitetura do Funil (Regra V5.3 da Fábrica)

As campanhas deverão ser geradas respeitando as três fases da janela de atenção exigidas pelo `AGENTS.md`. Nenhuma campanha é uma lista seca de posts; todas seguem o modelo rico.

| Fase do Funil | Objetivo (`fase_da_janela`) | Abordagem (Copy) | Ação Desejada (CTA) |
|---|---|---|---|
| **0. Gancho** | Atrair a atenção e gerar reconhecimento do problema (Awareness). | Perguntas provocativas, dados estatísticos, quebra de senso comum. | Baixar Lead Magnet, Ler Artigo. |
| **1. Aprofundamento** | Educar o lead e apresentar a metodologia (Consideration). | Estudo de caso, trechos em profundidade do livro/playbook, "Como fazer". | Interagir com o conteúdo, Responder E-mail. |
| **2. Urgência / CTA** | Converter a atenção em decisão (Decision). | Gatilhos de escassez, prova social ("centenas de pessoas"), oferta clara. | Checkout na Máquina de Vendas (`/api/checkout`). |

## 3. Matriz de Criação de Artefatos (O Quê, Por Que, Como, Quando)

Para evitar cronogramas "secos", a geração de qualquer campanha para a Fábrica deverá estruturar rigorosamente quatro dimensões:

*   **O Quê (O Artefato):** Qual material exato será entregue? (Ex: Arte PNG + Legenda no IG, Texto de WhatsApp, E-mail seq 01). Usar contadores sequenciais (`email-01`, `email-02`) e não posições do dia.
*   **Por Quê (O Objetivo Tático):** Alinhado à *Fase do Funil* acima (ex: Gancho para captura de lead frio).
*   **Como (O Formato/Copy):** O texto e a direção de arte. Aplicar *Copywriting* baseado na persona mapeada (Autor Digital, Profissional Técnico, etc). **Requisito:** A copy genérica de template DEVE ser reescrita usando os dados reais da coleção.
*   **Quando (Cronograma e Pausas):** Dia e horário (D+1, D+3). Dias de silêncio estratégico entram como `[PAUSA]`.

### Exemplo de Template de Execução

```markdown
### Dia 01: [E-mail] O Despertar da Audiência
- **O quê:** `email-01.md` (Texto de e-mail boas-vindas)
- **Por que:** Fase 0 (Gancho). Conectar a dor principal do autor com a solução da nossa coleção.
- **Como:** Linha de Assunto curta ("Por que seu livro não vende?"). Corpo focado em 1 história real e 1 link para o Lead Magnet.
- **Quando:** Imediatamente após o opt-in na Máquina de Vendas.
```

## 4. Integração com a Coleção e Máquina de Vendas

Segundo o livro, a estratégia digital precisa de um *Hub* forte. Na Fábrica, esse Hub é a Coleção (`output/<slug-colecao>/maquina/`).

*   **Ponto de Conversão:** Todas as URLs das campanhas devem apontar para a Máquina de Vendas do nicho específico (e nunca genéricas).
*   **Teste de Fluxo Obrigatório:** Toda campanha desenhada deve prever o teste do `POST /api/checkout` garantindo que a promessa da campanha aterrize no funil certo.

## 5. Diretrizes de SEO e Posicionamento (Conteúdo Estático)
*   **Artigos e E-books Secundários:** O tráfego orgânico recomendado por Martha Gabriel será sustentado pelos artigos gerados pelo `redator-academico`. O Playbook define que a campanha deve extrair "Pílulas de SEO" das H2s e H3s dos livros gerados, distribuindo-os em canais como LinkedIn e Blog.
