---
title: "As 25 Armadilhas de Harness Engineering — Do Modelo ao Sistema Autônomo Confiável"
subtitle: "Os 25 erros que travam quem está começando em Harness Engineering — Do Modelo ao Sistema Autônomo Confiável"
author: "Heverton Eduardo Peres"
lang: pt-BR
---

# As armadilhas

São **25 erros** que aparecem com mais frequência em quem está percorrendo este caminho pela primeira vez. Cada um traz a etapa em que costuma aparecer.

## 1. "O modelo é tão bom que não precisa de teste"**: o DORA 2024 mostrou exatamente o contrário — produtividade individual sem estabilidade de entrega é um custo escondido [9]

**Onde aparece:** Etapa 1 — A Revolução dos Agentes: Por Que o Modelo Não Basta

## 2. Permissão ampla "só por enquanto"**: tokens com escopo global e diretórios liberados são o vetor favorito de incidentes [17]

**Onde aparece:** Etapa 1 — A Revolução dos Agentes: Por Que o Modelo Não Basta

## 3. Autonomia total sem approval gates**: cancelar a confirmação humana "para acelerar" transfere o risco de erro para a escala — um erro repetido 100 vezes não é 100 vezes mais rápido, é 100 vezes mais caro [16]

**Onde aparece:** Etapa 1 — A Revolução dos Agentes: Por Que o Modelo Não Basta

## 4. Sem observabilidade**: agente que faz muito e não deixa rastro é um passivo de auditoria ambulante [12]

**Onde aparece:** Etapa 1 — A Revolução dos Agentes: Por Que o Modelo Não Basta

## 5. Ambiente compartilhado "para simplificar"**: rodar o agente com as mesmas permissões do operador transforma qualquer erro em incidente de segurança; o isolamento é a primeira linha [7][17]

**Onde aparece:** Etapa 2 — Anatomia de um Harness: O Corpo Que Carrega o Cérebro

## 6. Ferramentas ilimitadas**: cada ferramenta nova é superfície de ataque nova; comece com o mínimo e expanda sob demanda [13][14]

**Onde aparece:** Etapa 2 — Anatomia de um Harness: O Corpo Que Carrega o Cérebro

## 7. Memória só no prompt**: se o estado vive apenas na janela de contexto, uma execução interrompida perde tudo; persista o que importa [6][18]

**Onde aparece:** Etapa 2 — Anatomia de um Harness: O Corpo Que Carrega o Cérebro

## 8. Confiar na autoavaliação do modelo**: "o agente disse que completou" não é evidência; é narrativa [18]

**Onde aparece:** Etapa 3 — Test Harness: A Herança da Engenharia de Software

## 9. Testar a elegância em vez do contrato**: avaliações de "qualidade" subjetivas não substituem asserções verificáveis [2]

**Onde aparece:** Etapa 3 — Test Harness: A Herança da Engenharia de Software

## 10. Golden tests frágeis**: esperar a saída exata de um sistema probabilístico quebra o teste; teste propriedades e estruturas, não strings exatas [3]

**Onde aparece:** Etapa 3 — Test Harness: A Herança da Engenharia de Software

## 11. Segurança no prompt**: "por favor, não apague nada" não é guardrail; é sugestão [20]

**Onde aparece:** Etapa 4 — Safety Harness e Guardrails: A Camada Que Impede a Queda

## 12. Permitir por padrão**: bloquear só o que se conhece deixa o desconhecido livre; inverta para deny by default

**Onde aparece:** Etapa 4 — Safety Harness e Guardrails: A Camada Que Impede a Queda

## 13. Approval gate sem trilha**: aprovação sem registro é indecifrável depois; registre quem, o quê e quando [16]

**Onde aparece:** Etapa 4 — Safety Harness e Guardrails: A Camada Que Impede a Queda

## 14. Chamada única "direta ao modelo"**: sem loop, sem observação, sem correção de curso — o agente é um LLM com prompt bonito [4]

**Onde aparece:** Etapa 5 — O Ciclo ReAct e os Loops de Execução

## 15. Retry infinito**: falha permanente vira gasto infinito; sempre limite + backoff [19]

**Onde aparece:** Etapa 5 — O Ciclo ReAct e os Loops de Execução

## 16. Erro tratado como dado**: registrar "503" como conteúdo da resposta faz o agente raciocinar sobre um erro como se fosse fato [5]

**Onde aparece:** Etapa 5 — O Ciclo ReAct e os Loops de Execução

## 17. Credenciais do operador**: o agente com as permissões de quem o invoca é o incidente mais previsível do harness [17]

**Onde aparece:** Etapa 6 — Sandboxes, Permissões e o Controle de Execução

## 18. Sandbox de mentira**: restringir arquivos mas liberar rede (ou vice-versa) é contenção parcial; o escopo precisa cobrir todas as dimensões [19]

**Onde aparece:** Etapa 6 — Sandboxes, Permissões e o Controle de Execução

## 19. Token global "para o agente fazer tudo"**: a conveniência de hoje é o vazamento de amanhã; escopo por tarefa [17]

**Onde aparece:** Etapa 6 — Sandboxes, Permissões e o Controle de Execução

## 20. Jogar tudo no prompt**: o antídoto para "contexto pequeno" que envenena o contexto grande; divulgue progressivamente [6]

**Onde aparece:** Etapa 7 — Gestão de Contexto: Combatendo o Context Rot

## 21. Histórico bruto infinito**: cada observação fica para sempre, e a instrução se afoga; compacte por blocos [6]

**Onde aparece:** Etapa 7 — Gestão de Contexto: Combatendo o Context Rot

## 22. Estado só na conversa**: sem arquivos de progresso, uma interrupção ou um retry perde tudo; persista o estado [18]

**Onde aparece:** Etapa 7 — Gestão de Contexto: Combatendo o Context Rot

## 23. Observabilidade depois do incidente**: instrumentar a caixa preta quando ela já custou caro é o padrão mais caro do mercado; instrumente no primeiro dia [12]

**Onde aparece:** Etapa 8 — Harness em Produção: Observabilidade, Evals e o Engenheiro Agêntico

## 24. Eval de uma vez só**: medir o agente uma vez e nunca mais é tirar foto de quem precisa de exame periódico; eval é monitoramento de tendência [5]

**Onde aparece:** Etapa 8 — Harness em Produção: Observabilidade, Evals e o Engenheiro Agêntico

## 25. LLM-as-a-judge sem calibração**: o julgador tem viés; sem conferência humana periódica, o eval mede o viés do julgador [19]

**Onde aparece:** Etapa 8 — Harness em Produção: Observabilidade, Evals e o Engenheiro Agêntico

*Selecionamos as 25 mais frequentes, distribuídas por todas as etapas. A obra completa cataloga 40.*


# Próximo passo

Este material é um recorte de **Harness Engineering — Do Modelo ao Sistema Autônomo Confiável**. A obra completa traz a teoria, os exemplos comentados e as referências.

> [**Quero a obra completa**](https://exemplo.com/obra?utm_source=lead-magnet&utm_medium=pdf&utm_campaign=armadilhas)