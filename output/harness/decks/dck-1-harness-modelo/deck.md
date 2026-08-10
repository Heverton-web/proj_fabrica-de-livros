---
title: "Harness Engineering — Do Modelo ao Sistema Autônomo Confiável"
subtitle: "Apresentação · Escalador de Harnesses"
author: "Heverton Eduardo Peres"
lang: pt-BR
---

# Objetivo

Introdução de impacto: o dia em que o modelo errou sozinho — e ninguém tinha um arnês. Apresenta a máxima Agente = Modelo + Harness e o que o leitor será capaz de construir ao final da obra.

# O caminho

- **Arnês** — capítulos 1, 2, 3, 4
- **Corda** — capítulos 5, 6, 7, 8

# Fundamentos — O Equipamento Essencial

> Estágio 1 de 2

# A Revolução dos Agentes: Por Que o Modelo Não Basta

*Explicar por que LLMs sozinhos não produzem trabalho confiável e introduzir a equação Agente = Modelo + Harness, com o mapa do que será construído na obra*

- O que um agente realmente é (modelo + arcabouço)
- Onde os sistemas sem harness quebram em produção
- O retorno medido: dados de adoção e os riscos do agente solto

`python scripts/validar-codigo.py livros/harness-engineering --capitulo 1 --executar`

# Anatomia de um Harness: O Corpo Que Carrega o Cérebro

*Dissecar as camadas do harness — ambiente de execução, ferramentas, memória, estado e loops de feedback — mostrando cada peça com exemplo concreto*

- As camadas do harness e suas responsabilidades
- Ferramentas, sistema de arquivos e integração com o mundo
- Estado e memória: o que o agente lembra e o que o harness guarda

`python scripts/validar-codigo.py livros/harness-engineering --capitulo 2 --executar`

# Test Harness: A Herança da Engenharia de Software

*Apresentar o harness de teste — fixtures, execução determinística, linters e CI — como a primeira linha de verificação do trabalho do agente*

- O conceito clássico de test harness e sua transposição para agentes
- Execução determinística: o que o código prova que o agente acertou
- CI e gates automatizados como rede de segurança do fluxo

`python scripts/validar-codigo.py livros/harness-engineering --capitulo 3 --executar`

# Safety Harness e Guardrails: A Camada Que Impede a Queda

*Mostrar como proteger o sistema contra ações destrutivas do agente — aprovações humanas, limites de escopo, bloqueio de tool calls e princípio do menor…*

- O que os guardrails interceptam e por quê
- Approval gates e a fadiga de consentimento
- Menor privilégio, sandboxes e o blast radius controlado

`python scripts/validar-codigo.py livros/harness-engineering --capitulo 4 --executar`

# Na Prática — Instalando o Arnês e Escalando

> Estágio 2 de 2

# O Ciclo ReAct e os Loops de Execução

*Construir o primeiro harness funcional: o loop Reason → Act → Observe com execução de ferramentas, tratamento de erro e iteração até o objetivo*

- O loop ReAct passo a passo com código executável
- Execução de ferramentas: terminal, busca e APIs no harness
- Tratamento de erro e retry: o harness decide quando o agente tenta de novo

`python scripts/validar-codigo.py livros/harness-engineering --capitulo 5 --executar`

# Sandboxes, Permissões e o Controle de Execução

*Implementar isolamento real de execução — contêineres, permissões por escopo e políticas — para que o agente faça muito sem poder fazer qualquer coisa*

- Isolamento de execução: Docker, microVMs e a intenção da sandbox
- Políticas de permissão e tokens de escopo restrito
- Trilhas de auditoria: saber exatamente o que o agente fez

`python scripts/validar-codigo.py livros/harness-engineering --capitulo 6 --executar`

# Gestão de Contexto: Combatendo o Context Rot

*Ensinar a manter o agente focado em tarefas longas — compactação, offloading de ferramentas, divulgação progressiva e o padrão do loop de longa duração*

- O problema do context rot em tarefas longas
- Compactação, offloading e progressive disclosure
- Ralph Wiggum Loop: o agente revisando o próprio trabalho até satisfazer critérios

`python scripts/validar-codigo.py livros/harness-engineering --capitulo 7 --executar`

# Harness em Produção: Observabilidade, Evals e o Engenheiro Agêntico

*Fechar a obra com a operação de harnesses em escala — observabilidade, evals como testes de regressão do agente e o novo papel do engenheiro que desenha…*

- Observabilidade do agente: traces, logs e métricas da execução
- Evals e LLM-as-a-judge: o teste de regressão do comportamento
- O engenheiro agêntico: desenhar ambientes e especificar intenção

`python scripts/validar-codigo.py livros/harness-engineering --capitulo 8 --executar`

# Próximo passo

**Harness Engineering — Do Modelo ao Sistema Autônomo Confiável**

Quero a obra completa — https://exemplo.com/obra?utm_source=deck&utm_medium=slides&utm_campaign=harness-engineering
