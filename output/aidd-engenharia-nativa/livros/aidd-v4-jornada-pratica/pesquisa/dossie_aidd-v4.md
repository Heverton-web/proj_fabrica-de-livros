# Dossiê de Pesquisa — Volume 4: A Jornada Prática

## Conceitos-chave

- **Projeto real de ponta a ponta**: a aplicação integral do AIDD — do setup das camadas (Tela/Harness/LLM/Tools) e primeiras Specs, até funcionalidades via Skills/MCPs e deploy automatizado.
- **CI/CD agentic**: pipelines que integram agentes como cidadãos de primeira classe — diagnóstico de causa raiz, correção autônoma de falhas e gates de avaliação antes do merge.
- **Self-healing pipelines**: agentes que não só reportam falhas como corrigem (Azure OpenAI + AI Foundry; GitLab Duo Workflow).
- **Agent Gates**: camada de julgamento de IA sobre CI/CD — triagem de issues, code review, detecção de drift de documentação, investigação de falha de CI.
- **DevSecOps**: integração de segurança ao pipeline com SAST, DAST e SCA; gate de segurança antes do deploy.
- **Eval gates**: para agentes, o CI/CD de 2026 usa eval gates (conjuntos dourados), canary rollouts e regression suites.
- **Spec-alignment no pipeline**: pipeline agente-aware valida alinhamento com a spec e consistência comportamental antes de produção.

## Artigos Científicos e Papers

- BHOITE, Harshraj. *Autonomous AI Agents for End-to-End Data Engineering Pipelines Deployment: Enhancing CI/CD Pipelines*. 2025. Disponível em: https://doi.org/10.36227/techrxiv.174662424.46301311/v1. Acesso em: 10 ago. 2026. (A)
- KONERU, Naga Murali Krishna. *Integrating Security into CI/CD Pipelines: A DevSecOps Approach with SAST, DAST, and SCA Tools*. In: International Journal of Science and Research Archive. 2021. Disponível em: https://doi.org/10.30574/ijsra.2021.3.1.0080. Acesso em: 10 ago. 2026. (A)
- SARSCHAR, Mahja; ZHANG, Gefei; NOWAK, Annika. *PACGBI: A CI/CD Pipeline for LLM-assisted Code Generation of Web Front End*. In: Proceedings of the 2025 7th World Symposium on Software Engineering. 2025. Disponível em: https://doi.org/10.1145/3779657.3779672. Acesso em: 10 ago. 2026. (A)
- MUÑOZ, Antonio et al. *P2ISE: Preserving Project Integrity in CI/CD Based on Secure Elements*. In: Information. 2021. Disponível em: https://doi.org/10.3390/info12090357. Acesso em: 10 ago. 2026. (A)
- KREUZBERGER, Dominik; KÜHL, Niklas; HIRSCHL, Sebastian. *Machine Learning Operations (MLOps): Overview, Definition, and Architecture*. In: IEEE Access. 2023. Disponível em: https://doi.org/10.1109/access.2023.3262138. Acesso em: 10 ago. 2026. (A)
- MODALAVALASA, Godavari. *The Role of DevOps in Streamlining Software Delivery: Key Practices for Seamless CI/CD*. In: International Journal of Advanced Research in Science Communication and Technology. 2021. Disponível em: https://doi.org/10.48175/ijarsct-8978c. Acesso em: 10 ago. 2026. (A)
- MYLLYNEN, Teemu et al. *Review of Advances in AI-Powered Monitoring and Diagnostics for CI/CD Pipelines*. In: International Journal of Multidisciplinary Research and Growth Evaluation. 2024. Disponível em: https://doi.org/10.54660/.ijmrge.2024.5.1.1119-1130. Acesso em: 10 ago. 2026. (A)
- AMGOTHU, Sudheer. *An End-to-End CI/CD Pipeline Solution Using Jenkins and Kubernetes*. In: International Journal of Science and Research (IJSR). 2024. Disponível em: https://doi.org/10.21275/sr24826231120. Acesso em: 10 ago. 2026. (A)
- KUMAR, Ashok. *AI-Driven Deployment Pipelines for Multi-Cloud Environments in E-commerce Retail through Intelligent Continuous Integration and Continuous Deployment (CI/CD)*. In: AI and Machine Learning Advances. 2025. Disponível em: https://doi.org/10.64220/amla.v2i1.003. Acesso em: 10 ago. 2026. (A)
- CLARK, Tommy. *Implementing CI/CD Safely*. In: Apress Pocket Guides. 2025. Disponível em: https://doi.org/10.1007/979-8-8688-1209-5_4. Acesso em: 10 ago. 2026. (A)

## Estado da arte / ferramentas de referência

- **GitLab Duo Workflow**: agente autônomo embutido que gera código, roda jobs de CI, diagnóstica falhas e cria MRs. Disponível em: https://docs.gitlab.com/user/ai_features/
- **GitHub Agentic Workflows (Continuous AI)**: agentes de IA embutidos no merge pipeline — triagem, review, detecção de drift e investigação de falha autônoma. Disponível em: https://github.com/features/copilot
- **Red Hat — CI/CD para agentic AI**: padrões para integrar CI/CD ao processo agentic de desenvolvimento. Disponível em: https://developers.redhat.com/articles/2026/05/18/ci-cd-delivery-agentic-ai
- **Augment Intent / Auggie CLI**: ambiente spec-driven com Coordinator Agent que drafsta spec viva, gera tasks e delega; CLI headless para pipelines. Disponível em: https://docs.augmentcode.com
- **Self-healing pipelines (Microsoft)**: agentes com Azure OpenAI em CI/CD que corrigem falhas autonomamente. Disponível em: https://techcommunity.microsoft.com/blog/azureinfrastructureblog/from-pipelines-to-agents-self-healing-cicd-workflow/4519494

## Casos de uso corporativos

- **GitLab Duo em data engineering**: agente trabalha o plano, gera/reescreve código, garante que passa em todos os testes de CI e corrige falhas antes do MR (caso real documentado em techrxiv).
- **Copilot coding agent**: roda suíte de validação completa no PR — CodeQL, checagem de vulnerabilidades de dependência, secret scanning e code review nativo.
- **Pipeline de 2026**: agentes observam, raciocinam e agem no pipeline em tempo real — diagnóstico de causa raiz, correção e aprendizado a cada run, dentro de limites definidos.
- **DevSecOps**: gates de SAST/DAST/SCA no pipeline asseguram segurança antes do deploy em produção.

## Limitações e controvérsias

- **34% da capacidade de times consumida por falhas de pipeline** (DORA 2025) — agentes ajudam mas não eliminam a manutenção.
- **Risco de auto-aprovação**: agentes que corrigem e aprovam podem criar falsa confiança; revisão humana nos primeiros estágios é essencial (calibrar confiança no codebase).
- **Aplicações de alto risco**: deploy em produção, migrações de banco e trabalho criativo não são bons candidatos a loops totalmente autônomos.
- **Eval gates ainda imaturos**: conjuntos dourados e judges automatizados consolidam; sem padronização, o gate pode reprovar/aprovar incorretamente.
- **Segurança do pipeline**: agentes com acesso ao pipeline exigem OAuth/token auth, escopo de permissão e auditabilidade (P2ISE).

## Fontes brutas (para Nó 7 — Auditor de Rastreabilidade)

- BHOITE, Harshraj. *Autonomous AI Agents for End-to-End Data Engineering Pipelines Deployment: Enhancing CI/CD Pipelines*. Disponível em: https://doi.org/10.36227/techrxiv.174662424.46301311/v1. Acesso em: 10 ago. 2026. (A)
- KONERU, Naga Murali Krishna. *Integrating Security into CI/CD Pipelines: A DevSecOps Approach with SAST, DAST, and SCA Tools*. Disponível em: https://doi.org/10.30574/ijsra.2021.3.1.0080. Acesso em: 10 ago. 2026. (A)
- SARSCHAR, Mahja; ZHANG, Gefei; NOWAK, Annika. *PACGBI: A CI/CD Pipeline for LLM-assisted Code Generation of Web Front End*. Disponível em: https://doi.org/10.1145/3779657.3779672. Acesso em: 10 ago. 2026. (A)
- MUÑOZ, Antonio et al. *P2ISE: Preserving Project Integrity in CI/CD Based on Secure Elements*. Disponível em: https://doi.org/10.3390/info12090357. Acesso em: 10 ago. 2026. (A)
- KREUZBERGER, Dominik; KÜHL, Niklas; HIRSCHL, Sebastian. *Machine Learning Operations (MLOps): Overview, Definition, and Architecture*. Disponível em: https://doi.org/10.1109/access.2023.3262138. Acesso em: 10 ago. 2026. (A)
- MODALAVALASA, Godavari. *The Role of DevOps in Streamlining Software Delivery: Key Practices for Seamless CI/CD*. Disponível em: https://doi.org/10.48175/ijarsct-8978c. Acesso em: 10 ago. 2026. (A)
- MYLLYNEN, Teemu et al. *Review of Advances in AI-Powered Monitoring and Diagnostics for CI/CD Pipelines*. Disponível em: https://doi.org/10.54660/.ijmrge.2024.5.1.1119-1130. Acesso em: 10 ago. 2026. (A)
- AMGOTHU, Sudheer. *An End-to-End CI/CD Pipeline Solution Using Jenkins and Kubernetes*. Disponível em: https://doi.org/10.21275/sr24826231120. Acesso em: 10 ago. 2026. (A)
- KUMAR, Ashok. *AI-Driven Deployment Pipelines for Multi-Cloud Environments in E-commerce Retail through Intelligent Continuous Integration and Continuous Deployment (CI/CD)*. Disponível em: https://doi.org/10.64220/amla.v2i1.003. Acesso em: 10 ago. 2026. (A)
- CLARK, Tommy. *Implementing CI/CD Safely*. Disponível em: https://doi.org/10.1007/979-8-8688-1209-5_4. Acesso em: 10 ago. 2026. (A)
- GITLAB. *GitLab Duo Workflow — autonomous AI agent*. Disponível em: https://docs.gitlab.com/user/ai_features/. Acesso em: 10 ago. 2026. (B)
- GITHUB. *GitHub Copilot coding agent / Agentic Workflows*. Disponível em: https://github.com/features/copilot. Acesso em: 10 ago. 2026. (B)
- RED HAT. *Continuous integration and continuous delivery for agentic AI*. Disponível em: https://developers.redhat.com/articles/2026/05/18/ci-cd-delivery-agentic-ai. Acesso em: 10 ago. 2026. (B)
- AUGMENT CODE. *CI/CD for AI Agents — Intent e Auggie CLI*. Disponível em: https://docs.augmentcode.com. Acesso em: 10 ago. 2026. (B)
- MICROSOFT. *From Pipelines to Agents: Self-Healing CI/CD Workflow*. Disponível em: https://techcommunity.microsoft.com/blog/azureinfrastructureblog/from-pipelines-to-agents-self-healing-cicd-workflow/4519494. Acesso em: 10 ago. 2026. (C)
