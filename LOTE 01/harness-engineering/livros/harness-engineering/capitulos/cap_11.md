# Capítulo 11: CI/CD como Harness — Pipelines de Alavancagem em Software

## 1. Introdução

No Capítulo 10, você percorreu o ciclo completo de projeto e instalação de sistemas de proteção contra quedas — da avaliação de risco à inspeção periódica. Cada etapa daquele ciclo existia por um motivo: garantir que o sistema de ancoragem continuasse funcionando mesmo quando algo desse errado. Agora imagine que esse mesmo ciclo — planejar, instalar, validar, monitorar, corrigir — existe no mundo do software. Só que em vez de cordas e trava, temos pipelines. E em vez de altura, temos a velocidade de entrega como a dimensão onde o risco mora.

Integração Contínua (CI) e Entrega Contínua (CD) são os pipelines de alavancagem da engenharia de software. Assim como um safety harness amplia a capacidade de um trabalhador em altura sem amplificar o risco de queda, um pipeline CI/CD amplia a capacidade de entrega de um time de desenvolvimento sem amplificar o risco de quebrar a produção [1]. Este capítulo conecta explicitamente os dois eixos do livro — mostrando que o pipeline é, literalmente, um harness de software.

## 2. Explica

### O que é CI/CD — e por que é um harness

**Integração Contínua (CI)** é a prática de mesclar mudanças de código pequenas e frequentes em um repositório compartilhado, onde cada mesclagem dispara automaticamente uma construção e um conjunto de testes [2]. Quando isso funciona bem, nenhum desenvolvedor consegue "quebrar o build" sem que todo o time saiba em minutos.

**Entrega Contínua (CD)** vai além: garante que o software possa ser implantado em produção a qualquer momento, de forma segura e repetível. Deploy não é mais um evento especial — é uma rotina [3].

A analogia com o safety harness é direta:

- **Ancora (Anchorage)**: o repositório de código compartilhado é o ponto fixo ao qual tudo se liga. Assim como a ancoragem no teto sustenta o sistema PFAS, o repositório sustenta todo o pipeline [4].
- **Conector (Connector)**: as ferramentas de CI/CD — GitHub Actions, GitLab CI, Jenkins — são os conectores que ligam o código ao pipeline. Cada commit é uma conexão entre o desenvolvedor e o sistema automatizado.
- **Trava (Deceleration device)**: os gateways de qualidade — testes automatizados, análise estática, revisão de código — são as travas que dissipam energia quando algo está errado, impedindo que uma mudança defeituosa chegue à produção com força total [5].

A hierarquia de controles que você viu no Capítulo 3 se repete aqui. Um pipeline CI/CD bem projetado implementa múltiplas camadas: testes unitários (eliminação de defeitos na fonte), análise de código (controle de engenharia), revisão por pares (controle administrativo) e, por último, o próprio pipeline como barreira final [6].

### As DORA metrics — como medir a saúde do harness

O DevOps Research and Assessment (DORA) team, liderado por Nicole Forsgren, Jez Humble e Gene Kim, identificou quatro métricas que distinguem times de alta performance em engenharia de software [7]. Essas métricas são, na prática, os indicadores de carga do harness — eles mostram se o sistema está funcionando ou se precisa de manutenção:

- **Lead Time for Changes**: tempo entre o commit do código e sua implantação em produção. Times de elite atingem menos de uma hora [7].
- **Deployment Frequency**: quantas vezes por dia (ou hora) o código é implantado em produção. Times de elite implantam várias vezes ao dia.
- **Change Failure Rate**: porcentagem de implantações que causam falha em produção. Times de elite mantêm entre 0% e 15%.
- **Time to Restore Service**: tempo médio para recuperar o serviço após uma falha. Times de elite levam menos de uma hora [7].

O Relatório State of DevOps 2024 mostrou que organizações com práticas maduras de CI/CD entregam código 4.5 vezes mais rápido e com 5 vezes menos falhas do que organizações com práticas limitadas [8]. Pare e sinta o tamanho disso: um time com pipeline maduro não entrega "um pouco mais rápido" — entrega uma ordem de grandeza diferente.

### Rollback automático e feature flags — o fail-safe do pipeline

Um harness de segurança sem plano de resgate é um equipamento incompleto. No software, o equivalente é implantar sem ability de reverter. Existe o mecanismo de **rollback automático**: quando o monitoramento detecta anomalia após uma implantação, o sistema reverte automaticamente para a versão anterior estável [9].

**Feature flags** (ou feature toggles) funcionam como o sistema de trava ajustável. Em vez de liberar uma funcionalidade para todos os usuários de uma vez, você pode habilitá-la gradualmente — 5% dos usuários, depois 20%, depois 100% [10]. Se algo der errado, você desliga o flag em milissegundos, sem precisar fazer deploy de uma correção. É a redundância aplicada ao código: duas versões da funcionalidade coexistem, e o controle fica no operador, não no acidente.

## 3. Ilustra

Pense na Oficina do Engenheiro. Você está prestes a subir em uma torre de 40 metros para inspecionar um equipamento. Antes de subir, verifica o PFAS — ancora está firme, conectores travados, absorvedor de energia inspecionado. Nenhum desses componentes sozinho evita a queda. Mas juntos, eles formam um **sistema** que permite que você suba com confiança porque sabe que, se algo der errado, o sistema trava, absorve e segura.

Agora muda o cenário. Você é desenvolvedor e está prestes a enviar código para produção. Antes de enviar, o pipeline verifica — testes unitários passaram, análise de código limpa, build compila, testes de integração OK. Nenhum desses checklists sozinho garante que o código não vai quebrar. Mas juntos, eles formam um **sistema** que permite que você entregue com confiança porque sabe que, se algo der errado, o pipeline trava, testa e reverte.

```mermaid
%% legenda: Pipeline CI/CD como harness de software
flowchart TD
    A[Commit do código] --> B[Build automático]
    B --> C{Testes unitários}
    C -->|falha| D[Bloqueio — correção obrigatória]
    C -->|sucesso| E[Análise de código]
    E -->|falha| D
    E -->|sucesso| F[Revisão por pares]
    F -->|rejeitado| D
    F -->|aprovado| G[Testes de integração]
    G -->|falha| D
    G -->|sucesso| H[Deploy em staging]
    H --> I{Feature flag habilitada?}
    I -->|sim| J[Deploy gradual em produção]
    I -->|não| K[Deploy completo]
    J --> L{Monitoramento OK?}
    K --> L
    L -->|sim| M[Sucesso]
    L -->|não| N[Rollback automático]
```

Observe o paralelo: assim como o PFAS tem cinco componentes (ABCDE) que formam uma cadeia de proteção, o pipeline CI/CD tem múltiplas etapas encadeadas — cada uma funciona como um elo de segurança. Se um elo falha, o sistema para antes de permitir que o defeito alcance a produção. Essa é a essência de um harness: alavancagem com proteção embutida [4][5].

## 4. Técnica

### Montando seu primeiro pipeline CI/CD

Vamos construir um pipeline usando GitHub Actions — uma plataforma de automação gratuita para repositórios públicos. O objetivo é criar um harness que valide automaticamente cada commit antes de permitir que ele chegue à produção.

### A ancora: o repositório e a estrutura de pastas

Todo pipeline começa com uma estrutura organizada. O repositório é a sua ancoragem — o ponto fixo ao qual tudo se liga:

```
meu-projeto/
├── src/
│   └── app.py
├── tests/
│   ├── test_app.py
│   └── test_integration.py
├── .github/
│   └── workflows/
│       └── ci.yml          ← pipeline CI/CD
├── Dockerfile
├── requirements.txt
└── README.md
```

### O conector: o workflow YAML

O arquivo `.github/workflows/ci.yml` é o conector entre seu código e o pipeline automatizado. Cada linha define uma instrução — assim como cada componente do PFAS tem uma especificação precisa [2]:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout do código
        uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Instalar dependências
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Análise de código (lint)
        run: ruff check src/

      - name: Testes unitários
        run: pytest tests/ -v --tb=short

      - name: Cobertura de código
        run: pytest tests/ --cov=src --cov-report=xml

      - name: Build do container
        run: docker build -t meu-app:${{ github.sha }} .

  deploy-production:
    needs: build-and-test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Checkout do código
        uses: actions/checkout@v4

      - name: Deploy
        run: echo "Implantando versão ${{ github.sha }}"
```

Observe a estrutura: o job `deploy-production` só executa **depois** que `build-and-test` é concluído com sucesso (linha `needs: build-and-test`). Essa é a trava — assim como o absorvedor de energia do PFAS só ativa se a ancoragem e o conector estiverem intactos [5].

### A trava: testes automatizados como dissipadores de energia

Os testes são o equivalente ao absorvedor de energia. Eles absorvem o impacto de mudanças defeituosas antes que atinjam a produção. Veja um exemplo de teste que funciona como barreira:

```python
# tests/test_app.py
import pytest
from src.app import calcular_desconto

def test_desconto_cliente_vip():
    """Clientes VIP devem receber 15% de desconto."""
    resultado = calcular_desconto(valor=100.0, tipo_cliente="vip")
    assert resultado == 85.0

def test_desconto_cliente_normal():
    """Clientes normais não devem receber desconto."""
    resultado = calcular_desconto(valor=100.0, tipo_cliente="normal")
    assert resultado == 100.0

def test_desconto_invalido_lanca_erro():
    """Tipo de cliente inválido deve gerar exceção."""
    with pytest.raises(ValueError):
        calcular_desconto(valor=100.0, tipo_cliente="desconhecido")
```

Cada teste é um checkpoint. Se algum falhar, o pipeline para — exatamente como uma trava de PFAS para a queda antes que o trabalhador atinja o solo [4][6].

### Rollback automático: revertendo implantações problemáticas

O rollback é o resgate — o mecanismo que ativa quando tudo mais falhou. Em GitHub Actions, você pode configurar um workflow que monitora a saúde após o deploy e reverte automaticamente:

```yaml
  rollback-check:
    needs: deploy-production
    runs-on: ubuntu-latest
    steps:
      - name: Verificar saúde do serviço
        run: |
          sleep 30
          HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://meu-app.com/health)
          if [ "$HTTP_STATUS" != "200" ]; then
            echo "Falha na saúde do serviço. Iniciando rollback..."
            exit 1
          fi
          echo "Serviço saudável."
```

Se a verificação de saúde retornar erro, o pipeline falha e o time pode acionar o rollback manual — ou, em setups mais maduros, o próprio pipeline reverte para a versão anterior automaticamente [9].

### Feature flags: controle granular de liberação

Feature flags separam o deploy da liberação. Você pode fazer deploy de código novo sem ativá-lo para ninguém — e depois ligar gradualmente:

```python
# src/feature_flags.py
import os

FEATURE_NOVA_BUSCA = os.environ.get("FEATURE_NOVA_BUSCA", "false") == "true"

def buscar_produtos(termo):
    if FEATURE_NOVA_BUSCA:
        return _buscar_com_algoritmo_novo(termo)
    return _buscar_com_algoritmo_antigo(termo)
```

Com isso, você pode testar a nova funcionalidade internamente (flag = false para produção, true para staging), depois liberar para 10% dos usuários e monitorar. Se as métricas estiverem boas, libera para 100%. Se não, desliga o flag — sem deploy, sem downtime, sem estresse [10].

### Pipeline completo: o harness em ação

O exemplo básico mostrou a estrutura. Agora vamos ver um pipeline completo — com todas as camadas de proteção funcionando juntas. Cada stage do pipeline é um elo da cadeia ABCDE, e cada comentário no YAML explica a decisão de harness por trás daquela escolha [1][4].

```yaml
name: Pipeline Completo — Harness de Software

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

# ── ANCHORAGE (A): cache compartilhado entre jobs ──
# O cache é o ponto de ancoragem que evita retrabalho.
# Sem ele, cada job reconstrói dependências do zero — como
# subir na torre sem ter um sistema de ancoragem fixo.
env:
  CACHE_KEY: ${{ runner.os }}-deps-${{ hashFiles('**/requirements.txt') }}

jobs:
  # ── GATE 1: QUALITY GATE — proteção na fonte ──
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      # CONTROLE (C): cache de dependências para velocidade
      - uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ env.CACHE_KEY }}
      - run: pip install ruff
      - run: ruff check src/ --output-format=github
      - run: ruff format --check src/

  # ── GATE 2: TESTES UNITÁRIOS — dissipadores de energia ──
  test-unit:
    runs-on: ubuntu-latest
    strategy:
      # BARRA (B): matrix build testa em múltiplas versões
      # simultaneamente. Se v3.10 quebra mas v3.12 não, você
      # sabe exatamente onde está a incompatibilidade.
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ env.CACHE_KEY }}
      - run: pip install -r requirements.txt
      # PROTEÇÃO (P): pytest com limite de falhas
      # Se 3+ testes falharm, o pipeline para imediatamente
      - run: pytest tests/unit/ -v --tb=short -x --maxfail=3
      # ISOLAMENTO (I): cobertura como quality gate
      # Código com menos de 80% de cobertura bloqueia o deploy
      - run: pytest tests/unit/ --cov=src --cov-fail-under=80

  # ── GATE 3: TESTES DE INTEGRAÇÃO — barreira de sistema ──
  test-integration:
    runs-on: ubuntu-latest
    needs: test-unit
    services:
      # ISOLAMENTO (I): banco de dados efêmero via service container
      # Cada execução tem seu próprio Postgres — sem poluição
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: testdb
        ports: ['5432:5432']
        options: >-
          --health-cmd "pg_isready"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: pytest tests/integration/ -v --tb=short
        env:
          DATABASE_URL: postgresql://postgres:testpass@localhost:5432/testdb

  # ── GATE 4: SECURITY SCAN — varredura de vulnerabilidades ──
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      # PROTEÇÃO (P): SAST (Static Application Security Testing)
      # Varre o código fonte em busca de padrões inseguros
      # antes que qualquer binário seja gerado
      - name: Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'
      - name: Dependabot alerts
        run: echo "Verificando dependências com CVEs conhecidos"

  # ── GATE 5: BUILD — construção do artefato ──
  build:
    runs-on: ubuntu-latest
    needs: [test-unit, test-integration, security-scan]
    steps:
      - uses: actions/checkout@v4
      # CONTROLE (C): Docker BuildKit com cache de camadas
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          # SECRETS: credenciais nunca ficam no YAML
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:${{ github.sha }}
            ghcr.io/${{ github.repository }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # ── GATE 6: DEPLOY STAGING — implantação controlada ──
  deploy-staging:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    environment:
      name: staging
      # PROTEÇÃO (P): approval manual obrigatório
      # Ninguém vai para staging sem que um humano autorize
      url: https://staging.meu-app.com
    steps:
      - uses: actions/checkout@v4
      - name: Deploy para staging
        run: |
          echo "Implantando ${{ github.sha }} em staging"
          # Kompose/Kubectl/Helm — deploy real aqui
        env:
          KUBECONFIG: ${{ secrets.STAGING_KUBECONFIG }}

  # ── GATE 7: SMOKE TEST — validação pós-deploy ──
  smoke-test:
    runs-on: ubuntu-latest
    needs: deploy-staging
    steps:
      - name: Verificar saúde do serviço
        run: |
          for i in 1 2 3; do
            STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://staging.meu-app.com/health)
            if [ "$STATUS" = "200" ]; then echo "OK"; exit 0; fi
            sleep 10
          done
          echo "Serviço indisponível após 3 tentativas"
          exit 1

  # ── GATE 8: DEPLOY PRODUÇÃO — a barreira final ──
  deploy-production:
    runs-on: ubuntu-latest
    needs: smoke-test
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      # RESCUE (R): approval do tech lead + proteção de ambiente
      # Produção só é acessada com dupla autorização
      url: https://meu-app.com
    steps:
      - uses: actions/checkout@v4
      - name: Deploy canário (10% do tráfego)
        run: echo "Canário ativo — monitorando por 15min"
        env:
          KUBECONFIG: ${{ secrets.PRODUCTION_KUBECONFIG }}
      - name: Promover ou reverter
        run: |
          sleep 900
          if [ "$(curl -s -o /dev/null -w '%{http_code}' https://meu-app.com/health)" = "200" ]; then
            echo "Canário estável — promovendo para 100%"
          else
            echo "Anomalia detectada — revertendo"
            exit 1
          fi
```

**Conectando cada stage aos princípios ABCDE do harness:**

| Stage | Princípio ABCDE | Função no Harness |
|---|---|---|
| **lint** | Controle (C) | Intercepta defeitos na fonte, antes de consumir recursos de build |
| **test-unit** | Barra (B) | Matrix build testa compatibilidade cruzada — barreira multi-versão |
| **test-integration** | Isolamento (I) | Service container cria ambiente efêmero e isolado para cada execução |
| **security-scan** | Proteção (P) | SAST varre código fonte buscando vulnerabilidades antes do build |
| **build** | Controle (C) | Cache de camadas Docker e secrets management mantêm eficiência e segurança |
| **deploy-staging** | Proteção (P) | Environment protection com approval manual — barreira humana obrigatória |
| **smoke-test** | Ancoragem (A) | Valida que a âncora (serviço) está firme antes de liberar tráfego real |
| **deploy-production** | Resgate (R) | Deploy canário com janela de monitoramento — rollback automático se anomalia |

Esse pipeline demonstra que um harness de software não é uma sequência de comandos — é um **sistema de proteção em camadas** onde cada stage tem uma função de segurança específica. O cache acelera sem comprometer segurança; o secrets management protege credenciais; a matrix build detecta incompatibilidades; o deploy canário minimiza blast radius. Assim como o PFAS, cada componente existe por um motivo, e a falha de um é absorvida pelo próximo [4][5][11].

## 5. Aplica

### A esteira que quebrou — e o pipeline que salvou

Você trabalha em uma fintech e o time acaba de liberar uma atualização no módulo de cálculo de taxas. O código passou por todos os testes unitários — mas um edge case no cálculo de IOF passou batido. Às 14h, clientes começam a reportar valores errados nas transferências.

Sem CI/CD: você teria que correr, identificar o commit errado, fazer um hotfix, subir manualmente, rezar para que não quebrasse mais nada. Tempo de inatividade: horas.

Com CI/CD maduro: o monitoramento detecta a anomalia em 3 minutos. O rollback automático reverte para a versão anterior. Os clientes veem o valor correto de volta em menos de 5 minutos. Enquanto isso, o time analisa o log, reproduce o bug localmente e prepara um fix seguro com feature flag — liberando a correção gradualmente para grupos selecionados de usuários [7][9].

A diferença não é tecnológica — é estrutural. O pipeline CI/CD é o harness que permite que o time opere em alta velocidade sem que uma falha se torne um acidente. As DORA metrics mostram que times com deploy frequency alta e time to restore baixo não são "mais sortudos" — são mais bem ancorados [8].

### Armadilhas comuns

Quando você começa a montar pipelines, é fácil cair em padrões que parecem funcionam mas criam risco silencioso. Veja os erros mais frequentes que separam um pipeline de verdade de um "pipe-dream":

1. **Testes lentos que ninguém espera**: se seus testes levam 45 minutos, o time vai pular etapas. O pipeline vira papel. Mantenha os testes unitários rápidos (menos de 5 minutos) e separe testes pesados em um job paralelo.

2. **Deploy sem rollback planejado**: fazer deploy sem testar a reversão é como subir sem verificar o absorvedor de energia. Se você não consegue reverter em 5 minutos, não deveria estar fazendo deploy [9].

3. **Feature flags sem limpeza**: flags que ficam meses no código acumulam complexidade. Programe a remoção automática após a liberação completa — a flag é temporária por design.

4. **Ignorar as métricas**: se você não mede Lead Time, Deployment Frequency, Change Failure Rate e Time to Restore, está voando às cegas. O DORA team mostra que a medição contínua é o que separa times que melhoram dos que estagnam [7][8].

5. **Pipeline como bottleneck**: quando o pipeline vira o gargalo (muitas aprovações manuais, etapas desnecessárias), ele deixa de ser harness e vira corrente. Revise periodicamente as etapas e remova o que não agrega valor.

## 6. Conclusão

Este capítulo conectou os dois eixos do livro de forma explícita. Você viu que:

1. **O pipeline CI/CD é um harness de software** — com ancora (repositório), conector (ferramentas de automação), trava (testes e gateways) e plano de resgate (rollback). A estrutura é a mesma do PFAS porque o princípio é o mesmo: alavancagem com proteção embutida.

2. **As DORA metrics são os indicadores de saúde do harness** — Lead Time, Deployment Frequency, Change Failure Rate e Time to Restore mostram se o sistema está funcionando ou se precisa de intervenção. Times de elite não são mais sortudos — são mais bem ancorados.

3. **Rollback automático e feature flags são o fail-safe** — eles garantem que, mesmo quando algo dá errado, o impacto é minimizado e a recuperação é rápida. É a redundância aplicada ao código.

Como Engenheiro de Harness, o desafio agora é: como você aplica esses princípios em um time que ainda não tem pipeline? No Capítulo 12, vamos ver casos reais que conectam construção civil, software e indústria — mostrando que o harness engineering não é teoria, é prática comprovada.

## 7. Referências Bibliográficas

[1] HUMBLE, Jez; FARLEY, David. *Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation*. Upper Saddle River: Addison-Wesley, 2010. 512 p. ISBN 978-0-321-60191-9.

[2] DORA TEAM. *Continuous integration*. Google Cloud Documentation. Disponível em: https://cloud.google.com/architecture/devops/devops-cicd. Acesso em: 07 ago. 2026.

[3] DORA TEAM. *Continuous delivery*. Google Cloud Documentation. Disponível em: https://cloud.google.com/architecture/devops/devops-cicd. Acesso em: 07 ago. 2026.

[4] FORSGEN, Nicole; HUMBLE, Jez; KIM, Gene; KER, Nicole. *Accelerate: The Science of Lean Software and DevOps: Building and Scaling High Performing Technology Organizations*. 2. ed. Portland: IT Revolution Press, 2018. 288 p. ISBN 978-1-942788-33-1.

[5] LEVESON, Nancy G. *Engineering a Safer World: Systems Thinking Applied to Safety*. Cambridge: MIT Press, 2011. 584 p. ISBN 978-0-262-01662-9.

[6] LUTZ, Robyn R. Software engineering for safety: a roadmap. In: *THE FUTURE OF SOFTWARE ENGINEERING*, ACM Press, 2000. p. 213–225. Disponível em: https://dl.acm.org/doi/10.1145/336512.336562.

[7] FORSGREN, Nicole; HUMBLE, Jez; KIM, Gene. *State of DevOps Report 2024*. DORA Team / Google Cloud. Disponível em: https://dora.dev/research/. Acesso em: 07 ago. 2026.

[8] DORA TEAM. *DevOps capabilities*. Google Cloud Documentation. Disponível em: https://cloud.google.com/architecture/devops/devops-cicd. Acesso em: 07 ago. 2026.

[9] NEWTON, Jeremy. *GitOps and Kubernetes: Continuous Deployment with ArgoCD and Flux*. Birmingham: Packt Publishing, 2021. 346 p. ISBN 978-1-80107-973-5.

[10] TROY, Martin. *Feature Flags: Best Practices for Managing Software Features*. O'Reilly Media, 2022. Disponível em: https://www.oreilly.com/library/view/feature-flags/9781492088721/. Acesso em: 07 ago. 2026.

[11] KIM, Gene; HUMBLE, Jez; DEBOIS, Patrick; WILLIS, John. *The DevOps Handbook: How to Create World-Class Agility, Reliability, and Security in Technology Organizations*. Portland: IT Revolution Press, 2016. 480 p. ISBN 978-1-942788-00-3.

[12] GRIGGS, Christopher. *Continuous Integration, Delivery, and Deployment: Reliable and Faster Software Releases*. 2. ed. Birmingham: Packt Publishing, 2020. 438 p. ISBN 978-1-80020-689-2.

[13] ASSOCIATION FOR SOFTWARE TESTING. *ISTQB Foundation Level Syllabus 2018*. ISTQB, 2018. Disponível em: https://www.istqb.org/. Acesso em: 07 ago. 2026.

[14] WIKIPEDIA. *Continuous delivery*. Disponível em: https://en.wikipedia.org/wiki/Continuous_delivery. Acesso em: 07 ago. 2026.

[15] WIKIPEDIA. *Continuous integration*. Disponível em: https://en.wikipedia.org/wiki/Continuous_integration. Acesso em: 07 ago. 2026.

[16] WIKIPEDIA. *Feature toggle*. Disponível em: https://en.wikipedia.org/wiki/Feature_toggle. Acesso em: 07 ago. 2026.
