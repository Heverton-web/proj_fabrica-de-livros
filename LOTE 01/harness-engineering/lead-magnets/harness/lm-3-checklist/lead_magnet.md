---
title: "Checklist Mestre: Harness Engineering — Do Modelo ao Sistema Autônomo Confiável"
subtitle: "O checklist completo de 56 etapas para Harness Engineering — Do Modelo ao Sistema Autônomo Confiável"
author: "Heverton Eduardo Peres"
lang: pt-BR
---

# O checklist

São **56 verificações** distribuídas em 8 etapas. Marque cada uma antes de avançar — a ordem importa.

## Etapa 1 — A Revolução dos Agentes: Por Que o Modelo Não Basta

*Explicar por que LLMs sozinhos não produzem trabalho confiável e introduzir a equação Agente = Modelo + Harness, com o mapa do que será construído na obra.*

- [ ] Exercício 1 — Inventário do arnês.** Liste os cinco componentes de um harness (âncora
- [ ] Escreva uma frase dizendo qual falha do agente ele evita
- [ ] Use uma tabela como a abaixo
- [ ] Complete a função `executar_acao` para que o harness valide a ação antes de entregá-la ao modelo — a lição central do capítulo: quem executa é o harness
- [ ] Exercício 3 — Diagnóstico.** Um agente de suporte apagou um arquivo de produção porque o prompt do sistema dizia "você tem autonomia total"
- [ ] Aponte: (a) qual componente do harness deveria ter impedido
- [ ] (b) qual evidência a trilha deve conter para o pós-incidente

## Etapa 2 — Anatomia de um Harness: O Corpo Que Carrega o Cérebro

*Dissecar as camadas do harness — ambiente de execução, ferramentas, memória, estado e loops de feedback — mostrando cada peça com exemplo concreto.*

- [ ] Exercício 1 — Teste a âncora do capítulo.** Escreva testes parametrizados para a função de classificação abaixo
- [ ] O teste determinístico é a âncora que impede o agente de "funcionar" errando em silêncio
- [ ] Exercício 2 — Da observação ao caso de teste.** Pegue uma falha real que você já viu um agente cometer (uma resposta errada
- [ ] Transforme-a em três camadas: (a) o caso de teste que teria capturado
- [ ] (b) o assert que descreve o contrato
- [ ] (c) o gate de CI onde ele roda
- [ ] A disciplina de traduzir observação em teste é o que transforma harness em prática contínua

## Etapa 3 — Test Harness: A Herança da Engenharia de Software

*Apresentar o harness de teste — fixtures, execução determinística, linters e CI — como a primeira linha de verificação do trabalho do agente.*

- [ ] Exercício 1 — Crie sua régua de qualidade.** O capítulo mostrou a régua de referência
- [ ] Agora implemente uma versão mínima que pontua uma resposta do agente em quatro critérios: relevância
- [ ] O objetivo é tornar o julgamento explícito
- [ ] Exercício 2 — Defina seus critérios.** Para sua aplicação
- [ ] Liste quatro critérios de qualidade que um julgamento humano usaria
- [ ] Se um critério não puder ser automatizado
- [ ] Documente por quê — a régua honesta também sabe o que não mede

## Etapa 4 — Safety Harness e Guardrails: A Camada Que Impede a Queda

*Mostrar como proteger o sistema contra ações destrutivas do agente — aprovações humanas, limites de escopo, bloqueio de tool calls e princípio do menor privilégio.*

- [ ] Exercício 1 — Classificador de ações com fallback seguro.** Implemente um guardrail mínimo com a filosofia fail-closed: se a classificação não reconhecer a ação
- [ ] A regra de ouro do safety harness é errar para o lado seguro — nunca "deixar passar porque não sei" [20]
- [ ] Exercício 2 — Quebra do guardrail.** No Exercício 1
- [ ] Adicione uma regra para bloqueá-la
- [ ] Esse exercício reproduz a classe de vulnerabilidades de traversal que a OWASP destaca [20]
- [ ] Exercício 3 — Política de exceção.** Defina o fluxo de exceção do seu guardrail: quem autoriza uma ação bloqueada
- [ ] Sem esse fluxo

## Etapa 5 — O Ciclo ReAct e os Loops de Execução

*Construir o primeiro harness funcional: o loop Reason → Act → Observe com execução de ferramentas, tratamento de erro e iteração até o objetivo.*

- [ ] Exercício 1 — Loop com ferramenta real.** Substitua a calculadora do `HarnessReAct` deste capítulo por uma ferramenta que lê um arquivo JSON de configuração
- [ ] A observação deve voltar estruturada: sucesso
- [ ] Exercício 2 — O ciclo completo.** Expanda o loop do capítulo para usar a ferramenta do Exercício 1
- [ ] Rode três execuções: uma com arquivo válido
- [ ] Registre o histórico
- [ ] Descreva como o agente corrigiria o curso em cada caso
- [ ] Exercício 3 — Limite

## Etapa 6 — Sandboxes, Permissões e o Controle de Execução

*Implementar isolamento real de execução — contêineres, permissões por escopo e políticas — para que o agente faça muito sem poder fazer qualquer coisa.*

- [ ] Exercício 1 — Sandbox mínimo por política.** Implemente um sandbox conceitual que decide
- [ ] A separação política/execução é a lição central: o sandbox não decide o que é certo — ele aplica o que foi decidido [19]
- [ ] Exercício 2 — Inventário de superfície.** Liste as ferramentas do seu agente
- [ ] (b) exige ambiente real com aprovação
- [ ] (c) nunca deve ser oferecida ao agente
- [ ] Você terá a base do arquivo de política do seu harness
- [ ] Exercício 3 — Demonstração de dano.** Escolha uma ferramenta perigosa (por exemplo

## Etapa 7 — Gestão de Contexto: Combatendo o Context Rot

*Ensinar a manter o agente focado em tarefas longas — compactação, offloading de ferramentas, divulgação progressiva e o padrão do loop de longa duração.*

- [ ] Exercício 1 — Registro estruturado.** Implemente um logger que registra cada passo do agente em JSON estruturado: ação
- [ ] A trilha estruturada é o que torna o agente auditável — sem ela
- [ ] Exercício 2 — Caça à causa raiz.** Usando a trilha do Exercício 1
- [ ] Percorra os eventos
- [ ] Identifique a sequência exata de decisões que levou ao desvio —
- [ ] Exercício 3 — Métricas do arnês.** Defina três métricas para o seu harness (por exemplo: taxa de sucesso por tarefa
- [ ] Registre-as por uma semana

## Etapa 8 — Harness em Produção: Observabilidade, Evals e o Engenheiro Agêntico

*Fechar a obra com a operação de harnesses em escala — observabilidade, evals como testes de regressão do agente e o novo papel do engenheiro que desenha ambientes.*

- [ ] Exercício 1 — Runbook de incidente.** Escreva um runbook de 10 passos para um incidente de agente em produção: detecção
- [ ] Inclua o comando de kill-switch (pausar execuções)
- [ ] Exercício 2 — Custo
- [ ] Documente o fluxo: quem aprova
- [ ] O limiar transforma o custo em controle — a recomendação de cancelar projetos sem retorno claro que a Gartner publicou é o avesso dessa disciplina [10]
- [ ] Exercício 3 — Plano de rollback.** Liste os artefatos que o agente pode modificar (arquivos
- [ ] Se um artefato não tiver rollback


# Próximo passo

Este material é um recorte de **Harness Engineering — Do Modelo ao Sistema Autônomo Confiável**. A obra completa traz a teoria, os exemplos comentados e as referências.

> [**Quero a obra completa**](https://exemplo.com/obra?utm_source=lead-magnet&utm_medium=pdf&utm_campaign=checklist)