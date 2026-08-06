# Plano de Adaptação do Método EITA para Níveis de Senioridade

## 1. Visão Geral
Este plano especifica as diretrizes de design, a matriz de adaptação pedagógica do método **EITA** (Explica, Ilustra, Técnica, Aplica) e o plano de ação de engenharia para integrar os diferentes níveis de senioridade (Iniciante, Intermediário, Avançado, Técnico) na esteira automatizada de produção de livros e publicações da fábrica de livros.

A adaptação por senioridade permite que a esteira modele dinamicamente o tom de comunicação, a profundidade conceitual, o nível de complexidade do código e a natureza das analogias e aplicações práticas de acordo com o público-alvo escolhido pelo operador na Fase 0 (`/esbocar`).

---

## 2. Matriz de Adaptação do Método EITA

| Senioridade | LINGUAGEM | EXPLICA | ILUSTRA | TÉCNICA | APLICA |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Iniciante** | Simples, direta, sem jargões desnecessários, analogias cotidianas e tom amigável. | Conceitos explicados do zero ("tim-tim por tim-tim"), desmistificando o assunto de forma didática. | Diagramas de fluxo conceituais super simplificados, focados no fluxo lógico de alto nível, metáforas cotidianas. | Sem códigos complexos, foco em "o que é" e comandos simples prontos para uso. | Aplicações diárias básicas, automatizações de rotina pessoal ou profissional comum. |
| **Intermediário** | Profissional, objetiva, jargões técnicos explicados sucintamente se novos. | Foco nas pontes entre teoria e prática (como funciona sob o capô de forma conceitual). | Diagramas de blocos, processos e fluxogramas estruturais de média complexidade. | Exemplos em pseudocódigo, scripts estruturados comentados passo a passo. | Problemas reais de times, cenários de automação e integrações práticas de sistemas. |
| **Avançado** | Direta, focada em resultados, performance e termos de nível profissional de mercado. | Assume conhecimento da base. Foco em trade-offs, gargalos de performance e escolhas de arquitetura. | Diagramas de arquitetura detalhados, diagramas de sequência, topologia de rede/sistemas. | Código pronto para produção, tratamento de erros robusto, padrões de design e otimização. | Cenários de alta escala, tolerância a falhas, migrações complexas e segurança. |
| **Técnico** *(Acadêmico)* | Formal, acadêmica, rigorosa, impessoal (terceira pessoa), sem uso de humor. | Fundamentação teórica profunda, estado da arte, referências cruzadas e rigor científico. | Gráficos matemáticos, diagramas de blocos formais (UML, etc.) e mapeamento metodológico. | Demonstrações matemáticas, pseudocódigos acadêmicos, algoritmos puros ou análise estatística rigorosa. | Validação experimental, teses acadêmicas, contribuição científica e soluções de pesquisa teórica/prática rigorosa. |

---

## 3. Detalhamento Técnico das Senioridades

### 3.1 Iniciante
- **Público**: Estudantes, entusiastas ou profissionais transitando de área sem nenhuma base no assunto.
- **Objetivo**: Conduzir o leitor de forma acolhedora, reduzindo a ansiedade diante da complexidade técnica.
- **Linguagem**: Extremamente dialógica e empática. Exemplos de vida cotidiana (ex.: "Pense em uma fila de banco para entender filas de mensagens").
- **Técnica**: Blocos curtos de código executável com resultados visuais ou retornos imediatos.

### 3.2 Intermediário
- **Público**: Desenvolvedores ou profissionais júnior/pleno que já dominam os fundamentos e buscam consolidar conhecimento.
- **Objetivo**: Conectar a sintaxe e a lógica básica com estruturas e padrões de uso real de mercado.
- **Linguagem**: Vocabulário técnico de mercado ("deploy", "payload", "pipeline") sem mistificação.
- **Técnica**: Programação modular, scripts reutilizáveis, conceitos de Clean Code e introdução a testes unitários básicos.

### 3.3 Avançado
- **Público**: Desenvolvedores seniores, tech leads e arquitetos buscando domínio profundo e melhores práticas de produção.
- **Objetivo**: Desafiar o leitor a projetar soluções resilientes, performáticas e escaláveis de nível enterprise.
- **Linguagem**: Altamente focada em decisões de engenharia, custos de infraestrutura, mitigação de riscos e análise pós-mortem de falhas.
- **Técnica**: Código multi-threaded/assíncrono, tratamento de exceções avançado, desacoplamento de serviços, segurança de dados e padrões arquiteturais complexos.

### 3.4 Técnico (Acadêmico/Científico - TCC/Artigo)
- **Público**: Pesquisadores, revisores acadêmicos, PhDs e estudantes em processo de formação científica de nível superior.
- **Objetivo**: Contribuir para o estado da arte e fundamentar de maneira irrefutável os conceitos abordados.
- **Linguagem**: Estilo acadêmico formal e objetivo. Uso do plural majestático ou voz passiva impessoal.
- **Técnica**: Algoritmos formais, provas de conceitos puros, pseudocódigos, análise matemática de complexidade ($O(n)$) e validação de hipóteses experimentais.

---

## 4. Plano de Ação para Integração na Esteira

O plano de integração cobre quatro fases do ciclo de desenvolvimento de publicações.

```
Fase 0 (Escolha)  ──>  Fase 1 (Arquitetura)  ──>  Fase 2 (Manufatura)  ──>  Fase 2.5 (Qualidade)
       │                         │                        │                          │
       ▼                         ▼                        ▼                          ▼
Elicitar senioridade       Ajustar sumário          Estrategista / EITA        Revisor Técnico
e salvar na config.        macro com termos.        modulam código/tom.        audita público-alvo.
```

### Passo 1 — Atualização da Fase 0 (Elicitação e Validação)
*   **Ação**: Atualizar o script de elicitação interativa `.claude/commands/esbocar.md` para perguntar a senioridade na Rodada 1 e salvar o parâmetro `"senioridade_obra": "iniciante | intermediario | avancado | tecnico"` em `config_obra.json`.
*   **Ação**: Atualizar o script `scripts/parametros_obra.py` para incluir o domínio de valores de senioridade aceitos e definir os fallbacks automáticos (Livro V3 = `iniciante`; TCC/Artigo = `tecnico`).

### Passo 2 — Ajuste na Geração do Sumário Macro
*   **Ação**: Atualizar a skill `arquiteto` (`.claude/skills/arquiteto/SKILL.md`) para que a proposição dos títulos dos capítulos, objetivos e o motivo condutor alinhem-se com o nível de senioridade selecionado.

### Passo 3 — Modulação da Manufatura e Redação
*   **Ação**: Atualizar `.claude/agents/subagente-redator-capitulo.md` para que o subagente leia `senioridade_obra` e instrua as skills estratégicas com esse limitador.
*   **Ação**: Adaptar a skill `estrategista` (`.claude/skills/estrategista/SKILL.md`) para modular as entregas técnicas (complexidade do código) e a âncora visual (Mermaid) conforme a senioridade.
*   **Ação**: Adaptar a skill `redator-eita` (`.claude/skills/redator-eita/SKILL.md`) e o template `templates/template_eita.md` para embutir as restrições de estilo (matriz EITA por senioridade).

### Passo 4 — Validação e Revisão
*   **Ação**: Ajustar a skill `revisor-tecnico` (`.claude/skills/revisor-tecnico/SKILL.md`) e o script `scripts/auditar-obra.py` para validar a consistência com o público-alvo, impedindo contradições pedagógicas (ex.: capítulos "Iniciantes" com código de nível "Avançado" sem o devido apoio).

---

## 5. Próximos Passos
1. Obter aprovação formal do operador sobre este plano de modelagem e arquitetura.
2. Proceder com a alteração sequencial dos arquivos de configuração e scripts listados no Plano de Ação.
3. Testar a geração de um esboco com cada uma das quatro senioridades para comprovar a coerência textual.
