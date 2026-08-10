# O Mundo Real — Entrega das Chaves


# Capítulo 17: Preparando a entrega: build, CI/CD e pipelines

# Capítulo 17: Preparando a entrega: build, CI/CD e pipelines

## Introdução

No Capítulo 16 você assumiu o orçamento da obra — a economia de tokens que mantém projetos longos viáveis. A TorreDeControle está com a fundação, a estrutura, as instalações e a qualidade prontas. Falta o que separa um software de um produto: o **caminho do código até o usuário** — o build reproduzível, a integração contínua e o pipeline de entrega. É aqui que o canteiro ganha a rampa de entrega: o caminho padronizado pelo qual cada fatia aprovada sai do depósito e chega ao destino final.

Este capítulo constrói essa rampa: o build que qualquer máquina pode reproduzir; o CI/CD com gates automatizados — os portões que o Capítulo 14 instalou no local, agora em escala de pipeline; e o desenho do pipeline da TorreDeControle, do commit ao artefato pronto para o deploy. Ao final, cada commit na branch principal dispara a esteira de qualidade automaticamente — e a obra só avança quando todos os portões abrem.

## Explica

### Build reproduzível: o mesmo prédio em qualquer canteiro

A primeira peça da entrega é o **build reproduzível**: o processo de gerar o artefato executável — o pacote, a imagem, o bundle — que produz o mesmo resultado em qualquer máquina, em qualquer dia. A reprodutibilidade é o que o DORA chama de base da entrega confiável: se o build depende do laptop de alguém, a entrega depende do laptop de alguém — e laptops quebram, mudam e desaparecem.

Três elementos garantem a reprodutibilidade:

1. **Dependências fixadas**: as versões exatas de cada biblioteca, registradas num arquivo de lock — nunca "instale a última versão", sempre "instale a versão X registrada". O lock é a receita exata do prédio.
2. **Ambiente declarado**: o que o build precisa — runtime, variáveis, ferramentas — declarado num arquivo de configuração, não na memória de quem roda o build.
3. **Entrada única e verificável**: o build é função do código + config — mesmo commit, mesmo ambiente, mesmo artefato. Sem estado escondido, sem "funciona na minha máquina".

A regra de ouro da reprodutibilidade: **se você não consegue reconstruir o artefato a partir do repositório, você não tem um artefato — tem um acidente**. O build reproduzível é o que transforma "deu certo uma vez" em "dá certo sempre".

### CI: a integração contínua como esteira de qualidade

A **integração contínua (CI)** é a prática de integrar cada mudança ao tronco principal continuamente — em vez de acumular mudanças e integrar "quando estiver tudo pronto" (a integração que sempre explode). No fluxo agêntico, a CI tem um papel ainda mais central: é o portão que recebe o código gerado pelo agente e prova — a cada commit — que ele não quebrou nada.

O pipeline de CI é uma esteira de verificações, em ordem de custo (as baratas primeiro, para falhar cedo e barato):

1. **Sintaxe e estrutura**: o código compila (o `ci_sintaxe.sh` do Capítulo 14, agora na esteira).
2. **Testes unitários**: a suíte rápida de regras de negócio.
3. **Testes de integração**: API + service + modelo.
4. **Auditoria determinística**: cobertura, duplicação, consistência (o auditor do Capítulo 15).
5. **Empacotamento**: o build reproduzível gera o artefato.

Cada etapa é um **gate**: se falha, a esteira para e o commit é marcado como quebrado — o código nem chega ao repositório principal sem os portões abertos. A esteira é a versão em escala do porteiro do Capítulo 13: não confia, mede.

### CD: a entrega contínua como rampa de deploy

A **entrega contínua (CD)** estende a esteira até a rampa: o artefato aprovado é preparado para deploy — empacotado, versionado, pronto — e o deploy em si pode ser automático (entrega contínua com deploy contínuo) ou com aprovação (entrega contínua com deploy manual). A distinção importa: a esteira garante que o artefato *pode* ir a produção; a governança do Capítulo 13 decide *quando* ele vai.

No fluxo da TorreDeControle, o desenho é: CI roda em todo commit; CD prepara o artefato quando a branch principal passa; e o deploy para produção exige aprovação — o estágio 2 do espectro de autonomia, que você promoveu com consciência no Capítulo 13.

### Gates automatizados: a cadeia de portões

A soma de tudo são os **gates automatizados**: a cadeia de condições que uma mudança precisa atravessar antes de virar entrega. Cada gate é uma verificação determinística — e a cadeia é o que permite velocidade com segurança: o agente pode gerar rápido, mas a esteira garante que só o que passa chega ao usuário. Os gates principais da cadeia:

1. **Gate de sintaxe**: compila.
2. **Gate de testes**: a suíte passa.
3. **Gate de auditoria**: sem duplicação grosseira, terminologia consistente, cobertura de regras.
4. **Gate de revisão**: o veredito do Capítulo 15 — APROVADO ou APROVADO COM RESSALVAS.
5. **Gate de build**: o artefato é produzido e verificável.

A cadeia é o que o DORA chama de "deslocar a detecção para a esquerda": o erro é pego no ponto mais barato da cadeia — e o ponto mais barato é o primeiro.

## Ilustra

### A Rampa de Entrega do Canteiro

Volte ao canteiro. Quando o prédio está pronto para os acabamentos, a obra constrói a **rampa de entrega**: o caminho padronizado pelo qual material, móveis e equipamentos sobem do depósito até cada andar. A rampa não é um corredor qualquer: tem largura certa para o palete padrão, piso antiderrapante, e cada trecho é inspecionado antes de o material subir. Sem a rampa, cada entrega é uma improvisação — e cada improvisação é um risco de queda.

O pipeline de CI/CD é essa rampa. O código não sobe "pela escada, se der": ele sobe pela rampa — o caminho padronizado com inspeção em cada trecho. O commit entra no depósito, sobe pela esteira de verificações (os trechos inspecionados) e chega ao andar do deploy apenas se cada trecho foi aprovado. A rampa transforma a entrega de improviso em rotina — e rotina é o que torna a entrega confiável e rápida ao mesmo tempo.

```mermaid
%% legenda: Pipeline CI CD da TorreDeControle: do commit ao artefato com gates automatizados
flowchart LR
  A[Commit na branch principal] --> B[Gate 1: sintaxe e estrutura]
  B -->|falha| B1[Esteira para: commit marcado quebrado]
  B -->|passa| C[Gate 2: testes unitarios]
  C -->|falha| B1
  C -->|passa| D[Gate 3: auditoria deterministica]
  D -->|falha| B1
  D -->|passa| E[Gate 4: build reproduzivel]
  E -->|falha| B1
  E -->|passa| F[Artefato pronto: CD prepara o deploy]
  F --> G{Aprovacao humana para producao}
  G -->|aprova| H[Deploy em producao]
  G -->|aguarda| I[Artefato em espera versionado]
```

### A Escada Improvisada: Por Que Gates São a Rampa

Aqui está o ponto contraintuitivo — a segunda camada de analogia. A primeira mostrou a rampa de entrega. A segunda é sobre a diferença entre a rampa inspecionada e a escada improvisada — e por que a escada parece mais rápida até a primeira queda.

Imagine duas obras entregando móveis ao 10º andar. A primeira construiu a rampa: o palete sobe pelo caminho padrão, inspecionado em cada trecho, e qualquer trecho danificado para a entrega até o conserto. A segunda entrega pela escada: cada funcionário sobe com o móvel nas costas — parece mais rápido no primeiro dia, porque não gastou tempo construindo a rampa. Na segunda semana, um móvel cai da escada, quebra e atinge quem estava embaixo: a "economia" da escada vira o custo do acidente, mais o conserto, mais a parada.

Com CI/CD é idêntico: o pipeline parece burocracia até o dia em que o código quebrado chega ao usuário — e a "economia" de não ter portões vira o custo do incidente. Como Mestre de Obras, a rampa não é papelada: é a garantia de que o material sobe inteiro — e que, se algo está danificado, a esteira para *antes* da queda, no trecho onde o dano nasceu.

## Técnica

### Passo 1: Fixando as Dependências do Build

O primeiro passo é a reprodutibilidade: fixar as dependências da TorreDeControle num arquivo de lock. O `requirements.txt` do Capítulo 8 ganha versões exatas, e um segundo arquivo registra o hash da árvore completa:

```bash
# 1. Gere o lock a partir do requirements.txt (versoes exatas resolvidas)
#    (na pratica: pip freeze > requirements.lock.txt num ambiente limpo)
cat > requirements.lock.txt << 'EOF'
fastapi==0.115.0
uvicorn==0.30.0
pydantic==2.9.0
pytest==8.3.0
httpx==0.27.0
EOF

# 2. O build declara o ambiente: runtime + como instalar
cat > Dockerfile << 'EOF'
FROM python:3.12-slim

WORKDIR /app

# Instala apenas as dependencias fixadas (reproducibilidade)
COPY requirements.lock.txt .
RUN pip install --no-cache-dir -r requirements.lock.txt

# Copia o codigo da aplicacao
COPY app/ ./app/
COPY frontend/ ./frontend/

# Comando padrao de execucao
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF
```

O `Dockerfile` é o ambiente declarado: a imagem começa da mesma base, instala as mesmas versões e roda o mesmo comando — em qualquer máquina, qualquer dia. A receita exata do prédio, versionada no repositório.

### Passo 2: O Pipeline de CI em YAML

O segundo passo é o pipeline de CI — a esteira declarada num arquivo de configuração. Este é o pipeline da TorreDeControle para a plataforma de CI (GitHub Actions ou equivalente):

```yaml
name: ci-torrecontrole

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  qualidade:
    runs-on: ubuntu-latest
    steps:
      - name: checkout
        uses: actions/checkout@v4

      - name: setup python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: instalar dependencias fixadas
        run: pip install -r requirements.lock.txt

      - name: gate 1 - sintaxe e estrutura
        run: |
          python -m compileall -q app/
          python scripts/verificar_esqueleto.py

      - name: gate 2 - testes unitarios e de integracao
        run: python -m pytest tests/ -q

      - name: gate 3 - auditoria deterministica
        run: python scripts/auditar_repositorio.py

      - name: gate 4 - build do artefato
        run: |
          docker build -t torrecontrole:${{ github.sha }} .
          echo "artefato construido com sucesso"
```

Cada `run` é um gate: se falha, o job falha e o commit é marcado. A esteira é declarada — qualquer pessoa pode ver o que acontece a cada commit, sem depender de quem configurou.

### Passo 3: O Verificador do Pipeline Local

Para que a esteira não seja só remota, o mesmo fluxo roda localmente — o verificador que espelha os gates do CI:

```bash
#!/usr/bin/env bash
# pipeline_local.sh — Espelha os gates do CI localmente
set -euo pipefail

echo "== GATE 1: sintaxe e estrutura =="
python -m compileall -q app/
python scripts/verificar_esqueleto.py

echo "== GATE 2: testes =="
python -m pytest tests/ -q

echo "== GATE 3: auditoria =="
python scripts/auditar_repositorio.py

echo "== GATE 4: build (verificacao de dependencias) =="
pip check

echo "== PIPELINE LOCAL OK: todos os gates abertos =="
```

O `pipeline_local.sh` é o ensaio do canteiro: antes de commitar, você roda os mesmos portões que a esteira remota vai rodar — e descobre o problema no ensaio, não no palco.

### Passo 4: O Empaquetador do Artefato

O quarto passo é o empacotamento — a produção do artefato entregável, com versão e verificação de integridade:

```python
# empacotar_artefato.py — Empacota o artefato da TorreDeControle
import hashlib
import json
from datetime import date
from pathlib import Path

def gerar_manifiesto() -> dict: """Gera o manifest do artefato: versao, arquivos e hashes.""" arquivos = sorted( list(Path("app").rglob("*.py")) + list(Path("frontend").rglob("*")) ) hashes = {} for arquivo in arquivos: if arquivo.is_file(): digest = hashlib.sha256(arquivo.read_bytes()).hexdigest() hashes[str(arquivo)] = digest[:16] return { "projeto": "torrecontrole", "versao": f"1.0.0-{date.today().isoformat()}", "arquivos": len(hashes), "hashes": hashes, }

def main() -> None: """Gera o manifest e salva junto ao artefato.""" manifest = gerar_manifiesto() destino = Path("dist") destino.mkdir(exist_ok=True) (destino / "manifest.json").write_text( json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8" ) print(f"Artefato manifestado: {manifest['versao']} com {manifest['arquivos']} arquivos") print("Verifique a integridade antes do deploy: compare os hashes no destino.")

if __name__ == "__main__":
    main()
```

O manifest é a etiqueta do palete: versão, arquivos e hashes que permitem verificar, em qualquer ponto da rampa, que o artefato chegou inteiro.

### Passo 5: O Teste do Pipeline Completo

O quinto passo é a prova da esteira: um script que simula o caminho completo — commit, gates, artefato — e confirma que cada portão funciona de verdade:

```python
# testar_pipeline.py — Prova os gates do pipeline local
import subprocess
import sys

GATES = [
    ("gate 1 - sintaxe", ["python", "-m", "compileall", "-q", "app"]),
    ("gate 2 - testes", ["python", "-m", "pytest", "tests/", "-q"]),
    ("gate 3 - auditoria", ["python", "scripts/auditar_repositorio.py"]),
    ("gate 4 - dependencias", ["pip", "check"]),
]

def rodar_gates() -> None: """Roda todos os gates em ordem e para no primeiro que falhar.""" for nome, comando in GATES: print(f"== {nome} ==") resultado = subprocess.run(comando, capture_output=True, text=True) if resultado.returncode != 0: print(resultado.stdout[-800:]) print(resultado.stderr[-400:]) print(f"FALHOU no {nome}: esteira interrompida") sys.exit(1) print("OK") print("ESTEIRA COMPLETA: todos os gates abertos, artefato pronto")

def main() -> None:
    rodar_gates()

if __name__ == "__main__":
    main()
```

O teste do pipeline é a prova de carga da rampa: a esteira inteira rodando de uma vez, com o primeiro gate que falhar parando tudo — exatamente como em produção.

### O Protocolo de Entrega Contínua

Para fechar, o protocolo de entrega — como uma mudança viaja do commit ao artefato:

1. **Commit em branch de feature** (ou direto na main para o fluxo do projeto): o CI roda os gates em todo push.
2. **Aprovação da revisão**: o veredito do Capítulo 15 — APROVADO ou com ressalvas registradas.
3. **Merge para a main**: a esteira roda de novo; se tudo abre, o build gera o artefato.
4. **CD prepara o deploy**: o artefato é versionado e manifestado.
5. **Aprovação do deploy**: a governança do Capítulo 13 decide quando o artefato vai a produção.
6. **Deploy e observação**: o Capítulo 19 acompanha o que aconteceu.

## Aplica

### A Cena de Contraste: O Build do Laptop do João

Imagine a TorreDeControle prestes a ser entregue — e o deploy agendado para sexta-feira. O build "funciona" apenas no laptop do João: foi ele que configurou as dependências na sua máquina, na sua versão do Python, com uma biblioteca instalada "de brincadeira" que o requirements.txt não registra. Na quinta, o João fica doente. O deploy para: ninguém reproduz o build, o requirements.txt é incompleto, e a sexta vira uma reconstituição arqueológica — "o que o João tinha instalado?" — enquanto o produto espera.

O diagnóstico: build não reproduzível — o artefato dependia do laptop de uma pessoa. A entrega não tinha rampa; tinha a escada do João, e a escada desapareceu com ele.

A correção: você adota a cadeia completa — requirements.lock.txt com versões fixas, Dockerfile declarando o ambiente, pipeline de CI com os quatro gates e o manifest do artefato. Na semana seguinte, qualquer máquina reproduz o build: mesmo commit, mesmo lock, mesmo artefato — e o deploy não depende de quem está presente. A lição: build que depende de máquina não é build — é acidente esperando para acontecer; a rampa versionada é o que torna a entrega independente de pessoa.

### Armadilhas Comuns em Build e CI/CD

- **Dependências flutuantes**: "instale a última versão" quebra o build no dia seguinte. Lock com versões exatas.
- **Build na máquina local**: se o build só roda no seu laptop, a entrega depende do seu laptop. Container ou ambiente declarado.
- **CI sem gates**: esteira que roda testes mas ignora falhas é decorativa. Cada gate falho para a esteira.
- **Pipeline não espelhado localmente**: descobrir o erro no CI remoto custa ciclos. `pipeline_local.sh` ensaia antes.
- **Artefato sem manifest**: sem versão e hashes, ninguém verifica a integridade na rampa. Manifest obrigatório.
- **Deploy sem aprovação**: a CD automática sem o portão da governança salta o estágio de autonomia. Aprovação antes de produção (Capítulo 13).

### Exercício Prático

Crie o `requirements.lock.txt` e o `Dockerfile` da TorreDeControle, escreva o pipeline de CI com os quatro gates, rode `testar_pipeline.py` até a esteira completa passar e gere o manifest do artefato com `empacotar_artefato.py`. Registre no diário o caminho completo do commit ao artefato.

### Aprofundamento: Estratégias de Deploy (Blue-Green e Canário)

O pipeline do Capítulo 17 entrega o artefato — mas a forma como o artefato entra em produção tem estratégias, e as duas mais importantes para o seu repertório são o deploy blue-green e o deploy canário:

**Deploy Blue-Green**: duas versões do ambiente convivem — a azul (atual) e a verde (nova). O roteador aponta para a azul; quando a verde passa nos testes, o roteador troca o tráfego para a verde; se algo der errado, o roteador volta para a azul em segundos. O rollback do Capítulo 18 vira uma troca de roteador, não um redeploy. O custo: dois ambientes mantidos — o preço da reversão instantânea.

**Deploy Canário**: a versão nova recebe uma fração do tráfego (1%, depois 10%, depois 50%) enquanto as métricas do Capítulo 19 monitoram. Se a taxa de erro sobe, o canário é cortado e o tráfego volta para a versão estável. O custo: mais complexidade de roteamento — o preço da validação com tráfego real.

| Estratégia | Reversão | Validação com tráfego real | Complexidade |
|---|---|---|---|
| Blue-green | Instantânea (troca de roteador) | Limitada (tudo de uma vez) | Média |
| Canário | Rápida (corta a fração) | Gradual (percentual crescente) | Alta |
| Redeploy simples | Lenta (redeploy da anterior) | Nenhuma | Baixa |

A decisão de estratégia segue a matriz de risco: para a TorreDeControle em início de operação, o blue-green com aprovação humana (o gate do Capítulo 13) é o equilíbrio certo — reversão instantânea sem a complexidade do roteamento percentual. O canário entra quando o tráfego cresce e o custo de uma falha total supera a complexidade do roteamento. A regra que une tudo: a estratégia de deploy é uma decisão de risco, não de moda — e as métricas do Capítulo 19 são o instrumento que decide quando mudar de estratégia.

## Conclusão

Neste capítulo você construiu a rampa de entrega da obra: entendeu o build reproduzível — a receita exata que qualquer máquina refaz; dominou a integração contínua — a esteira de gates que prova cada commit; aprendeu a entrega contínua — a preparação do artefato com aprovação de deploy; e montou a cadeia completa — lock, Dockerfile, pipeline, manifest e o teste da esteira. A lição central: a rampa transforma a entrega de improviso em rotina — e a rotina inspecionada é o que permite ao agente gerar rápido sem quebrar o usuário.

Seu desafio: a esteira completa da TorreDeControle — lock, Dockerfile, pipeline com gates, `testar_pipeline.py` passando e o artefato manifestado.

No Capítulo 18, vamos dar o salto final: o deploy do projeto prático na nuvem — variáveis de ambiente, migrações e o momento em que a TorreDeControle deixa o canteiro e começa a operar para usuários reais.

# Capítulo 18: Do código à nuvem: deploy do projeto prático

# Capítulo 18: Do código à nuvem: deploy do projeto prático

## Introdução

No Capítulo 17 você construiu a rampa de entrega — o build reproduzível, o pipeline de CI/CD e os gates automatizados que levam cada fatia aprovada do commit ao artefato. Agora chegou o momento que o título deste livro promete desde a primeira página: **o deploy** — o instante em que a TorreDeControle deixa o canteiro de obras e começa a operar na nuvem, para usuários reais, 24 horas por dia. É a entrega das chaves.

Este capítulo é o guia completo do deploy do projeto prático: a escolha da plataforma de nuvem, as variáveis de ambiente e o gerenciamento de segredos, as migrações de banco de dados em produção, o deploy do artefato construído no Capítulo 17 e a verificação do sistema no ar. Ao final, a TorreDeControle estará publicada — e você terá feito, ponta a ponta, o percurso do zero ao deploy que este livro ensina.

## Explica

### O que significa "estar em produção"

Antes dos comandos, o conceito: **estar em produção** significa que o sistema opera para usuários reais, com dados reais, disponibilidade esperada e responsabilidade real. Três coisas mudam em relação ao desenvolvimento:

1. **Disponibilidade**: o sistema precisa estar no ar — não "quando você abre o servidor local", mas sempre. A plataforma de nuvem cuida disso com processos gerenciados.
2. **Dados persistentes**: os dados não podem morrer com o laptop — o banco de produção é gerenciado, com backup e recuperação.
3. **Segredos**: senhas, chaves de API e tokens não podem estar no código — vivem em gerenciadores de segredos da plataforma.

A transição de desenvolvimento para produção é a mesma do canteiro: o prédio que estava sob construção — com operários, ferramentas e improvisos permitidos — passa a ser habitado. As regras mudam: o que era aceitável no canteiro (testar no laje, caminho improvisado) é inaceitável no prédio habitado.

### Plataformas de nuvem e o modelo de deploy

Em 2026, o deploy de uma aplicação como a TorreDeControle segue um dos três modelos:

- **Plataforma como serviço (PaaS)**: a plataforma gerencia runtime, escala e banco — você faz deploy do código ou do container e a plataforma cuida do resto. O caminho de menor atrito para projetos como o nosso.
- **Containers gerenciados**: você sobe a imagem do Capítulo 17; a plataforma orquestra execução e escala. Mais controle, um pouco mais de configuração.
- **Infraestrutura como serviço (IaaS)**: você gerencia servidores, rede e tudo mais. O controle total e o custo operacional máximo — desnecessário para este projeto.

A escolha certa para a TorreDeControle é o caminho de menor atrito com o controle necessário: subir o container do Capítulo 17 numa plataforma gerenciada, com banco gerenciado separado. A regra de decisão: **escolha a plataforma que mantém o seu foco no produto, não na infraestrutura** — a menos que o requisito de escala ou regulação exija o contrário.

### Variáveis de ambiente e segredos

O ponto mais sensível do deploy é o gerenciamento de segredos. A regra é absoluta: **nada de segredo no código, no repositório ou na imagem** — os segredos vivem em variáveis de ambiente configuradas na plataforma, fora do controle de versão. A TorreDeControle precisa de três famílias de configuração:

1. **Configuração não sensível** (pública): porta, nível de log, URL pública — pode viver em defaults do código.
2. **Configuração sensível** (segredo): chave de assinatura de token, credenciais do banco, chaves de API externa — vivem em variáveis de ambiente protegidas.
3. **Configuração por ambiente**: valores diferentes para desenvolvimento, staging e produção — resolvidos no momento do deploy.

O padrão prático: um arquivo `.env.example` no repositório (com campos em branco, sem valores reais) documenta as variáveis; a plataforma recebe os valores reais via painel ou CLI; e o código lê tudo de variáveis de ambiente — nunca de constantes embutidas no código.

### Migrações de banco em produção

A segunda área crítica é a **migração de banco**: a evolução do schema em produção sem perda de dados. A TorreDeControle chega ao deploy com o modelo do Capítulo 7 — e a migração inicial cria as tabelas; as migrações futuras alteram o schema com segurança. As regras de ouro:

1. **Migração versionada**: cada mudança de schema é um arquivo com número e descrição, aplicado em ordem — nunca mudanças ad hoc.
2. **Migração idempotente e reversível**: aplicada uma vez, com rollback planejado.
3. **Migração testada em staging**: o que roda em produção rodou antes em ambiente de teste — o gate do Capítulo 17 aplicado ao banco.

A migração é a parte do deploy que mais derruba sistemas em produção — e a que mais se beneficia da disciplina do canteiro: testar antes, aplicar em ordem, reverter com segurança.

## Ilustra

### A Entrega das Chaves

Volte ao canteiro — o último dia da obra. O prédio está pronto: estrutura vistoriada, instalações testadas, acabamento aprovado. Chega o momento da **entrega das chaves**: o mestre entrega ao dono o prédio com tudo que foi combinado na planta — e o dono passa a morar nele. A partir daquele instante, o prédio não é mais uma obra: é uma residência, com moradores, contas de luz e responsabilidades. O mestre não some: fica disponível para manutenção — mas o regime mudou.

O deploy é a entrega das chaves da TorreDeControle. O código não é mais um projeto no seu laptop: é um serviço na nuvem, com usuários reais, banco gerenciado e segredos protegidos. A planta (especificação), a vistoria (revisão) e a rampa (CI/CD) garantiram que o prédio está pronto — e a entrega das chaves é o ato final da construção e o primeiro dia da operação.

```mermaid
%% legenda: Fluxo do deploy na nuvem: artefato, variaveis, banco, publicacao e verificacao
flowchart TB
  A[Artefato do Cap 17: imagem e manifest] --> B[Plataforma: subir a imagem]
  B --> C[Configurar variaveis de ambiente e segredos]
  C --> D[Banco gerenciado: aplicar migracoes]
  D --> E[Publicar: URL publica no ar]
  E --> F[Verificacao pos deploy: smoke test em producao]
  F -->|falhou| G[Rollback para a versao anterior]
  F -->|passou| H[Entrega das chaves: sistema operando]
```

### O Prédio Entregue Sem Chaves: Por Que o Deploy é Mais que Subir Código

Aqui está o ponto contraintuitivo — a segunda camada de analogia. A primeira mostrou a entrega das chaves. A segunda é sobre a diferença entre "o código está no ar" e "o prédio está habitável" — e por que a segunda é o que de fato importa.

Imagine o mestre entregando o prédio "pronto" — mas sem a chave do quadro de luz, sem o registro do banheiro no condomínio e com a porta do porão trancada e ninguém sabendo onde está a chave. O prédio está de pé — mas não é habitável: o morador não liga a energia, não regulariza nada e não acessa um terço da área. O prédio "no ar" não é o prédio entregue.

Com o deploy é idêntico: subir o código não é entregar o serviço — é preciso as variáveis certas (as chaves), o banco migrado (a regularização) e a verificação do sistema no ar (a habitabilidade). Como Mestre de Obras, o momento da entrega exige o checklist completo: sem chaves, sem migração e sem verificação, o que está "no ar" é uma casca — e casca não é prédio habitado.

## Técnica

### Passo 1: O Código Lendo Variáveis de Ambiente

O primeiro passo técnico é preparar o código para produção: a configuração lida de variáveis de ambiente, nunca de constantes. Este é o módulo de configuração da TorreDeControle:

```python
# app/config.py — Configuracao da aplicacao lida de variaveis de ambiente
import os
from dataclasses import dataclass

def _ler_obrigatoria(nome: str) -> str: """Le uma variavel de ambiente obrigatoria; falha com mensagem clara.""" valor = os.environ.get(nome) if not valor: raise RuntimeError( f"Variavel de ambiente {nome} ausente. Configure antes do deploy." ) return valor

def _ler_opcional(nome: str, padrao: str) -> str:
    """Le uma variavel de ambiente opcional com valor padrao."""
    return os.environ.get(nome, padrao)

@dataclass class Config: ambiente: str url_publica: str chave_assinatura: str banco_url: str nivel_log: str porta: int

def carregar_config() -> Config:
    """Carrega a configuracao da aplicacao a partir do ambiente.

Segredos (chave_assinatura, banco_url) sao obrigatorios e nunca tem default no codigo: a plataforma os injeta como variaveis de ambiente. """ return Config( ambiente=_ler_opcional("APP_AMBIENTE", "desenvolvimento"), url_publica=_ler_opcional("APP_URL_PUBLICA", "http://localhost:8000"), chave_assinatura=_ler_obrigatoria("APP_CHAVE_ASSINATURA"), banco_url=_ler_obrigatoria("APP_BANCO_URL"), nivel_log=_ler_opcional("APP_NIVEL_LOG", "info"), porta=int(_ler_opcional("APP_PORTA", "8000")), )

def main() -> None: """Exemplo: carregar a config e mostrar o que e publico.""" config = carregar_config() print(f"Ambiente: {config.ambiente}") print(f"URL publica: {config.url_publica}") print(f"Nivel de log: {config.nivel_log}") print("Segredos carregados (sem exibir valores).")

if __name__ == "__main__":
    main()
```

Repare no padrão: o que é segredo é obrigatório e sem default; o que é público tem default razoável. A plataforma injeta os segredos — o código nunca os contém.

### Passo 2: O Arquivo .env.example (documentação, sem segredos)

O segundo passo é documentar as variáveis — com o arquivo de exemplo versionado, sem valores reais:

```bash
# .env.example — DOCUMENTA as variaveis de ambiente (NUNCA coloque valores reais aqui)
# Copie para a plataforma de deploy e preencha com os valores reais la.

# Ambiente: desenvolvimento | staging | producao
APP_AMBIENTE=producao

# URL publica do servico apos o deploy
APP_URL_PUBLICA=https://torrecontrole.exemplo.com

# SEGREDO: chave de assinatura dos tokens JWT (gerar com: python -c "import secrets; print(secrets.token_hex(32))")
APP_CHAVE_ASSINATURA=

# SEGREDO: URL de conexao do banco gerenciado
# Exemplo: postgresql://usuario:senha@host:5432/torrecontrole
APP_BANCO_URL=

# Nivel de log: debug | info | warning | error
APP_NIVEL_LOG=info

# Porta do servico
APP_PORTA=8000
```

A regra é sagrada: o `.env.example` versiona os *nomes* das variáveis; os *valores* reais só existem na plataforma. O repositório nunca vê um segredo.

### Passo 3: A Migração Inicial do Banco

O terceiro passo é a migração — a criação do schema em produção, versionada e testada. Este é o esqueleto do sistema de migração:

```python
# scripts/migrar.py — Sistema de migracao de banco simples e versionado
import json
import sqlite3
from pathlib import Path

MIGRACOES = [ { "versao": 1, "descricao": "cria tabelas iniciais do dominio (Cap 7)", "sql": """ CREATE TABLE IF NOT EXISTS usuarios ( id TEXT PRIMARY KEY, email TEXT UNIQUE NOT NULL, nome TEXT NOT NULL, senha_hash TEXT NOT NULL ); CREATE TABLE IF NOT EXISTS projetos ( id TEXT PRIMARY KEY, nome TEXT NOT NULL, descricao TEXT, criado_por TEXT NOT NULL, FOREIGN KEY (criado_por) REFERENCES usuarios(id) ); CREATE TABLE IF NOT EXISTS tarefas ( id TEXT PRIMARY KEY, titulo TEXT NOT NULL, descricao TEXT, status TEXT NOT NULL DEFAULT 'a_fazer', prioridade TEXT NOT NULL DEFAULT 'media', projeto_id TEXT NOT NULL, responsavel_id TEXT, FOREIGN KEY (projeto_id) REFERENCES projetos(id), FOREIGN KEY (responsavel_id) REFERENCES usuarios(id) ); CREATE TABLE IF NOT EXISTS atividades ( id TEXT PRIMARY KEY, tarefa_id TEXT NOT NULL, tipo TEXT NOT NULL, descricao TEXT, autor_id TEXT NOT NULL, criada_em TEXT NOT NULL, FOREIGN KEY (tarefa_id) REFERENCES tarefas(id), FOREIGN KEY (autor_id) REFERENCES usuarios(id) ); """, }, ]

def aplicar_migracoes(caminho_banco: str) -> None: """Aplica as migracoes pendentes em ordem, registrando a versao aplicada.""" conexao = sqlite3.connect(caminho_banco) cursor = conexao.cursor() cursor.execute( "CREATE TABLE IF NOT EXISTS _migracoes (versao INTEGER PRIMARY KEY, aplicada_em TEXT)" ) aplicadas = { linha for linha in cursor.execute("SELECT versao FROM _migracoes").fetchall() } for migracao in MIGRACOES: versao = migracao["versao"] if versao in aplicadas: continue print(f"Aplicando migracao {versao}: {migracao['descricao']}") cursor.executescript(migracao["sql"]) cursor.execute( "INSERT INTO _migracoes (versao, aplicada_em) VALUES (?, datetime('now'))", (versao,), ) conexao.commit() conexao.close() print("Migracoes em dia.")

def main() -> None: """Aplica as migracoes no banco apontado por APP_BANCO_URL (ou arquivo local).""" import os url = os.environ.get("APP_BANCO_URL", "data/torrecontrole.db") if url.startswith("sqlite:///"): url = url.removeprefix("sqlite:///") Path(url).parent.mkdir(parents=True, exist_ok=True) aplicar_migracoes(url)

if __name__ == "__main__":
    main()
```

A migração versionada é a regra do canteiro aplicada ao banco: cada mudança de schema é um arquivo, aplicada em ordem, registrada — e a tabela `_migracoes` é o diário de bordo do banco.

### Passo 4: O Deploy na Prática (Plataforma Gerenciada)

O quarto passo é o deploy em si — os comandos conceituais de subir a aplicação numa plataforma gerenciada. O fluxo completo, do artefato à publicação:

```bash
# 1. Configure a plataforma (CLI) apontando para o repositorio/imagem
#    (exemplos conceituais; os comandos exatos variam por plataforma)
plataforma login
plataforma apps:create torrecontrole

# 2. Injete as variaveis de ambiente (segredos NAO vao para o repositorio)
plataforma config:set APP_AMBIENTE=producao
plataforma config:set APP_URL_PUBLICA=https://torrecontrole.exemplo.com
plataforma config:set APP_CHAVE_ASSINATURA="$(python -c 'import secrets; print(secrets.token_hex(32))')"
plataforma config:set APP_BANCO_URL="postgresql://usuario:senha@host:5432/torrecontrole"
plataforma config:set APP_NIVEL_LOG=info

# 3. Provisione o banco gerenciado e rode a migracao no ambiente de deploy
plataforma db:create torrecontrole
plataforma run "python scripts/migrar.py"

# 4. Faca o deploy do artefato (a rampa do Cap 17 entrega a imagem)
plataforma deploy

# 5. Verifique o sistema no ar
curl -s https://torrecontrole.exemplo.com/health
```

Cada passo tem uma função: a criação da app declara o serviço; as variáveis entregam as chaves; o banco provisionado e migrado regulariza o terreno; o deploy sobe a imagem; e o curl final é a vistoria — o sistema respondendo no ar.

### Passo 5: O Smoke Test de Produção

O quinto passo é a verificação pós-deploy — o teste de fumaça em produção, provando que o sistema entregue está habitável:

```python
# scripts/smoke_test_producao.py — Verifica o sistema no ar pos deploy
import os
import sys
import urllib.request

def verificar_endpoint(url: str) -> None: """Faz uma requisicao GET e falha se a resposta nao for 200.""" try: with urllib.request.urlopen(url, timeout=10) as resposta: status = resposta.status print(f"GET {url} -> {status}") if status != 200: sys.exit(f"FALHA: {url} retornou {status}") except Exception as erro: sys.exit(f"FALHA: {url} indisponivel -> {erro}")

def main() -> None: """Roda o smoke test de producao da TorreDeControle.""" base = os.environ.get("APP_URL_PUBLICA", "http://localhost:8000") print(f"Smoke test em {base}") verificar_endpoint(f"{base}/health") verificar_endpoint(f"{base}/") print("SMOKE TEST OK: sistema no ar e respondendo")

if __name__ == "__main__":
    main()
```

O smoke test é a vistoria final da entrega das chaves: se o endpoint de saúde e a página inicial respondem, o prédio está habitável — e o deploy está completo.

### O Protocolo de Rollback

Para fechar, o protocolo de rollback — a rede de segurança quando algo dá errado no ar:

1. **Versão anterior pronta**: o artefato anterior fica disponível na plataforma (o Capítulo 17 versiona cada artefato).
2. **Rollback declarado**: a plataforma reverte para a versão anterior — os dados do banco permanecem (migrações são progressivas; rollback de código, não de dados).
3. **Migração reversível**: se a falha envolveu banco, a migração tem o passo reverso documentado.
4. **Registro no diário**: o incidente e o rollback viram entrada no diário de decisões — e o Capítulo 19 transforma o incidente em melhoria.

O rollback não é sinal de fracasso: é o mecanismo que torna o deploy seguro — a certeza de que, se algo der errado, a obra volta para a versão anterior sem pânico.

## Aplica

### A Cena de Contraste: O Segredo no Repositório

Imagine a madrugada do primeiro deploy da TorreDeControle. Na pressa, você cola a chave de assinatura e a senha do banco direto no `config.py` — "só para o deploy funcionar hoje, depois eu corrijo". O deploy sobe, o sistema funciona, e o código vai para o repositório com os segredos embutidos. Três dias depois, o repositório é tornado público (ou um colaborador externo ganha acesso), e os segredos estão lá — no histórico, para sempre. A chave de assinatura permite forjar tokens; a senha do banco permite ler todos os dados. O incidente não é um bug: é uma brecha de segurança aberta na pressa.

O diagnóstico: segredo no código — a violação da regra absoluta do deploy. A pressa fez o que o protocolo proíbe, e o custo é uma brecha permanente no histórico do repositório.

A correção: você rotaciona os segredos (gera chaves novas, troca a senha do banco), remove os valores do histórico (ou reescreve a história), e adota o padrão correto: `.env.example` documenta os nomes; a plataforma injeta os valores; o `config.py` lê do ambiente. Na semana seguinte, o deploy é refeito pelo caminho certo — e o repositório não contém nenhum segredo, em nenhum commit. A lição: segredo no código é brecha com data marcada — e a regra de variáveis de ambiente é a cerca que a impede.

### Armadilhas Comuns no Deploy

- **Segredo hardcoded**: a brecha mais comum e mais cara. Variáveis de ambiente sempre.
- **Deploy sem migração**: o sistema sobe sem banco → erro na primeira query. Migração antes da publicação.
- **Deploy sem smoke test**: "está no ar" sem verificação não é estar no ar. Smoke test obrigatório.
- **Banco de produção sem backup**: o primeiro incidente de dados sem backup é o último projeto. Backup configurado pela plataforma.
- **Rollback não planejado**: sem versão anterior pronta, o erro em produção vira caos. Artefato versionado sempre.
- **Deploy manual repetido**: deploy manual é erro esperando para acontecer. O pipeline do Capítulo 17 automatiza — o humano só aprova.

### Exercício Prático

Prepare a TorreDeControle para produção: crie o `config.py` lendo do ambiente, o `.env.example` com as variáveis documentadas, a migração inicial do banco e o smoke test. Se tiver acesso a uma plataforma de nuvem, execute o deploy completo do Passo 4 — e registre no diário o checklist da entrega das chaves.

### Aprofundamento: O Checklist Completo da Entrega das Chaves

O deploy do Capítulo 18 tem uma versão condensada em checklist — a lista que você percorre antes de cada publicação, garantindo que nenhuma chave ficou de fora. Este é o checklist completo da entrega:

**Antes do deploy (preparação):**
1. [ ] O pipeline do Capítulo 17 passou em staging (todos os gates abertos).
2. [ ] O artefato está versionado e com manifest (Capítulo 17).
3. [ ] As variáveis de ambiente estão configuradas na plataforma (nada hardcoded).
4. [ ] As migrações foram testadas em staging e a ordem está documentada.
5. [ ] O protocolo de rollback está definido (versão anterior identificada).

**Durante o deploy:**
6. [ ] Migrações aplicadas em produção (na ordem, uma a uma).
7. [ ] Aplicação publicada com a aprovação humana (gate do Capítulo 13).
8. [ ] Smoke test de produção executado (o script do Capítulo 18).

**Depois do deploy (verificação):**
9. [ ] Métricas essenciais verificadas (latência, erros — Capítulo 19).
10. [ ] Logs estruturados confirmam o tráfego real chegando.
11. [ ] Diário de decisões registra a publicação (versão, data, observações).
12. [ ] Incidente posterior tem o protocolo do Capítulo 13 pronto.

O checklist é o mesmo instrumento de toda a obra — verificação determinística no lugar de confiança — aplicado ao momento mais caro do ciclo. Ele não impede todos os problemas (nenhum checklist impede): ele garante que os problemas conhecidos não passem por esquecimento, e que os imprevistos encontrem um processo, não um improviso. A regra prática: se um item do checklist não faz sentido para o seu projeto, remova-o *conscientemente* — nunca pule por pressa, porque a pressa é exatamente o que o checklist existe para neutralizar.

## Conclusão

Neste capítulo você entregou as chaves da TorreDeControle: entendeu o que significa estar em produção — disponibilidade, dados persistentes e segredos protegidos; escolheu o caminho de menor atrito na nuvem; preparou o código para variáveis de ambiente com a regra absoluta de segredos fora do repositório; escreveu a migração versionada do banco; executou o deploy e o smoke test de produção; e montou o protocolo de rollback. A lição central: o deploy é a entrega das chaves — o momento em que o canteiro vira moradia, e a disciplina do canteiro (variáveis, migração, verificação) é o que garante a habitabilidade.

Seu desafio: a TorreDeControle no ar — configurada por ambiente, banco migrado, smoke test passando e o checklist da entrega registrado no diário.

No Capítulo 19, vamos acompanhar o prédio habitado: monitoramento, observabilidade e o loop de iteração — métricas, logs e o ciclo contínuo de melhoria após o deploy.

# Capítulo 19: Monitoramento, observabilidade e iteração

# Capítulo 19: Monitoramento, observabilidade e iteração

## Introdução

No Capítulo 18 você entregou as chaves — a TorreDeControle está no ar, operando na nuvem para usuários reais. Mas a entrega das chaves não é o fim da obra: é o início da **operação**. Um prédio habitado precisa de portaria, de leitura de medidores e de manutenção contínua; um serviço em produção precisa de monitoramento, observabilidade e do loop de iteração que transforma dados em melhorias.

Este capítulo é o curso de operação do projeto prático: a instrumentação do sistema com logs estruturados e métricas; as métricas de engenharia que o DORA consagrou — as quatro que medem o desempenho real da entrega; e o loop de iteração — o ciclo contínuo em que os dados de produção alimentam a próxima rodada de melhorias, com o agente participando do diagnóstico e da correção. Ao final, a TorreDeControle não será apenas um sistema no ar: será um sistema *entendido* — com visibilidade do que acontece, métricas do que importa e um ciclo de melhoria contínua funcionando.

## Explica

### Observabilidade: ver dentro do sistema

O conceito central da operação é a **observabilidade**: a capacidade de entender o estado interno de um sistema a partir das suas saídas externas — logs, métricas e rastreios. Um sistema observável é um sistema sobre o qual você consegue responder perguntas: "por que esta requisição foi lenta?", "quantas tarefas foram criadas ontem?", "qual endpoint mais falha?" — sem adivinhar.

Os três pilares da observabilidade:

1. **Logs**: eventos discretos com contexto — "tarefa X movida por Y às Z". Logs estruturados (JSON) são buscáveis e filtráveis — a diferença entre o diário legível e a pilha de papéis.
2. **Métricas**: números agregados no tempo — requisições por segundo, latência percentil, taxa de erro. Métricas respondem "quanto?" e "como está tendendo?".
3. **Rastreios (traces)**: o caminho de uma requisição através dos componentes — quanto tempo em cada camada. Rastreios respondem "onde está o gargalo?".

O princípio prático: comece com logs estruturados e métricas essenciais; rastreios entram quando o sistema cresce. A instrumentação mínima do primeiro dia é melhor que a instrumentação perfeita do dia em que o incidente acontece — porque o incidente não espera.

### As métricas de engenharia (o que o DORA mede)

O DORA, o estudo de alta performance de engenharia que acompanha milhares de equipes, consolidou quatro métricas que medem o desempenho da entrega de software — e elas são o painel da TorreDeControle:

1. **Frequência de deploy**: com que frequência a equipe publica — quanto maior a frequência (com qualidade), maior a capacidade de entrega.
2. **Lead time de mudança**: quanto tempo entre o commit e o deploy — a velocidade da rampa do Capítulo 17.
3. **Taxa de falha de mudança**: quantos deploys causam incidentes em produção — a qualidade do que sai pela rampa.
4. **Tempo de recuperação (MTTR)**: quanto tempo para restaurar o serviço após um incidente — a eficácia do rollback e do diagnóstico.

A métrica mais importante para o fluxo agêntico é a taxa de falha de mudança: ela mede se a velocidade da geração está saindo cara. E o alvo não é "zero falha" (irreal) — é falha baixa e recuperação rápida: o DORA mostra que as equipes de elite têm falha baixa *e* recuperação rápida, não falha zero.

### O loop de iteração: dados → diagnóstico → correção

A observabilidade não é um fim — é o combustível do **loop de iteração**: o ciclo contínuo em que os dados de produção alimentam melhorias. O loop tem quatro etapas:

1. **Observar**: métricas e logs mostram o que acontece — um endpoint lento, um erro recorrente, uma queda de uso.
2. **Diagnosticar**: os dados apontam a causa — e aqui o agente entra: com o contexto do Capítulo 15, ele analisa logs e propõe hipóteses.
3. **Corrigir**: o fix passa pelo fluxo completo da obra — spec, fatia, testes, revisão, pipeline (os Capítulos 7-17 em um ciclo).
4. **Verificar**: as métricas confirmam a melhoria — o mesmo instrumento que apontou o problema mede a correção.

O loop é a diferença entre operar e apenas rodar: rodar é o sistema no ar; operar é o sistema melhorando continuamente com base em evidência.

### A iteração agêntica em produção

A iteração em produção tem uma forma própria no fluxo agêntico: o agente participa do diagnóstico (lê logs, cruza dados, propõe causas) e da correção (implementa a fatia com os testes do Capítulo 14) — mas a *decisão* de mudar um sistema em produção é humana, porque envolve risco de usuário real. O fluxo seguro: o agente investiga e propõe; o humano aprova; o pipeline entrega; a métrica confirma. É o espectro de autonomia do Capítulo 13 aplicado à operação: autonomia na análise, controle na decisão.

## Ilustra

### A Portaria e os Medidores do Prédio

Volte ao prédio habitado. A entrega das chaves não deixou o prédio sem supervisão: há a **portaria**, que registra quem entra e sai (os logs); há os **medidores** — de energia, água, gás — que acumulam números no tempo (as métricas); e há o **zelador**, que cruza as informações: "o consumo de água subiu de quinta para sexta — algo vazou no andar 5" (o diagnóstico). O prédio sem portaria e sem medidores não é abandonado — é *cego*: os moradores podem até estar felizes, mas ninguém sabe o que está acontecendo até o vazamento alagar o subsolo.

A TorreDeControle em produção precisa da mesma tríade: logs estruturados (a portaria registrando eventos), métricas (os medidores acumulando números) e o loop de iteração (o zelador cruzando dados e agindo). Um serviço sem observabilidade não é um serviço — é uma caixa preta que ninguém entende até quebrar.

```mermaid
%% legenda: Loop de iteracao em producao: observar, diagnosticar, corrigir e verificar com metricas
flowchart LR
  A[Metricas e logs em producao] --> B[Observar: painel do sistema]
  B --> C[Diagnosticar: agente analisa logs e propoe causas]
  C --> D[Corrigir: fatia + testes + pipeline aprovado pelo humano]
  D --> E[Verificar: metricas confirmam a melhoria]
  E --> A
```

### O Prédio Sem Medidores: Por Que Observabilidade é Ver, Não Adivinhar

Aqui está o ponto contraintuitivo — a segunda camada de analogia. A primeira mostrou a portaria e os medidores. A segunda é sobre a diferença entre o prédio com medidores e o prédio que "parece estar bem" — e por que a aparência de saúde é o estado mais perigoso.

Imagine dois prédios habitados. O primeiro tem medidores em cada andar e um zelador que lê os números semanalmente: quando o consumo de água sobe 20% num andar, ele descobre o vazamento antes de ele alagar. O segundo prédio não tem medidores — mas os moradores dizem que "está tudo bem, ninguém reclamou". Na verdade, há um vazamento lento no 4º andar há semanas: ninguém reclamou porque ninguém percebeu o aumento gradual — e quando o teto desaba, o "tudo bem" vira a maior obra de emergência do ano.

Com software é idêntico: a ausência de reclamação não é saúde — é ausência de medição. A degradação gradual (o endpoint que fica 200ms mais lento por semana, o erro que sobe de 0,1% para 1% aos poucos) não gera reclamação imediata — gera colapso futuro. Como Mestre de Obras em regime de operação, a lição é a mais valiosa do capítulo: medir é ver; não medir é adivinhar — e o prédio habitado se administra com medidores, não com palpite.

## Técnica

### Passo 1: Logs Estruturados

O primeiro passo é a instrumentação: logs estruturados no lugar de prints soltos. Este é o módulo de logging da TorreDeControle:

```python
# app/logging_config.py — Logs estruturados (JSON) para producao
import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any

class JsonFormatter(logging.Formatter):
    """Formata os registros de log como JSON de linha unica, buscaivel."""

def format(self, registro: logging.LogRecord) -> str: payload: dict[str, Any] = { "timestamp": datetime.now(timezone.utc).isoformat(), "nivel": registro.levelname, "logger": registro.name, "mensagem": registro.getMessage(), } if getattr(registro, "evento", None): payload["evento"] = registro.evento if getattr(registro, "dados", None): payload["dados"] = registro.dados if registro.exc_info: payload["excecao"] = self.formatException(registro.exc_info) return json.dumps(payload, ensure_ascii=False)

def configurar_logging(nivel: str = "info") -> logging.Logger: """Configura o logger raiz com formato JSON e retorna o logger da app.""" handler = logging.StreamHandler(sys.stdout) handler.setFormatter(JsonFormatter()) raiz = logging.getLogger("torrecontrole") raiz.setLevel(nivel.upper()) raiz.handlers = [handler] return raiz

def evento(logger: logging.Logger, nome: str, **dados: Any) -> None:
    """Registra um evento de dominio com contexto estruturado."""
    logger.info("evento", extra={"evento": nome, "dados": dados})

def main() -> None:
    """Exemplo de uso dos logs estruturados."""
    logger = configurar_logging()
    evento(logger, "tarefa_movida", tarefa_id="t1", de="a_fazer", para="em_andamento")
    logger.error("falha na integracao", extra={"evento": "api_externa_falhou"})

if __name__ == "__main__":
    main()
```

O log estruturado é a portaria do prédio: cada evento com timestamp, nível, contexto — buscável e filtrável. A diferença entre "algo aconteceu" (print solto) e "o que, onde, quando, com quais dados" (JSON estruturado).

### Passo 2: O Coletor de Métricas

O segundo passo é o coletor de métricas — os medidores do prédio. Este é o módulo que registra os números essenciais:

```python
# app/metricas.py — Coletor de metricas essenciais da aplicacao
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable

@dataclass
class Metricas:
    """Coletor simples de metricas: contadores e medias por operacao."""

    contadores: dict[str, int] = field(default_factory=dict)
    tempos: dict[str, list[float]] = field(default_factory=dict)

    def incrementar(self, nome: str, valor: int = 1) -> None:
        """Incrementa um contador (ex.: requisicoes por endpoint)."""
        self.contadores[nome] = self.contadores.get(nome, 0) + valor

    def registrar_tempo(self, operacao: str, segundos: float) -> None:
        """Registra o tempo de uma operacao para calculo de latencia."""
        self.tempos.setdefault(operacao, []).append(segundos)

def relatorio(self) -> dict[str, float | int]: """Gera o relatorio agregado: contadores e latencias percentil 95.""" relatorio: dict[str, float | int] = dict(self.contadores) for operacao, amostras in self.tempos.items(): ordenadas = sorted(amostras) indice = max(0, int(len(ordenadas) * 0.95) - 1) relatorio[f"latencia_p95_{operacao}"] = round(ordenadas[indice], 3) return relatorio

def main() -> None: """Exemplo de uso do coletor de metricas.""" metricas = Metricas() metricas.incrementar("requisicoes_criar_tarefa") metricas.incrementar("requisicoes_criar_tarefa") metricas.registrar_tempo("criar_tarefa", 0.12) metricas.registrar_tempo("criar_tarefa", 0.09) print(metricas.relatorio())

if __name__ == "__main__":
    main()
```

As métricas essenciais do primeiro dia: contadores por operação (quantas vezes cada endpoint rodou) e latência p95 (o tempo que 95% das requisições não ultrapassam). Com esses dois números, você já responde "quanto?" e "está lento?".

### Passo 3: O Endpoint de Saúde e o Painel

O terceiro passo é o endpoint de saúde e o painel mínimo — a superfície visível da observabilidade:

```python
# app/api/health.py — Endpoint de saude e status para monitoramento
import time
from typing import Any

def gerar_status( metricas: dict[str, Any], banco_ok: bool = True, versao: str = "1.0.0", ) -> dict[str, Any]: """Gera o payload de saude do servico para o monitor externo.""" return { "status": "ok" if banco_ok else "degradado", "versao": versao, "tempo_resposta_ms": round(time.time() * 1000) % 1000, "metricas": metricas, }

def main() -> None: """Exemplo do payload de saude retornado pelo endpoint /health.""" metricas = { "requisicoes_criar_tarefa": 1240, "latencia_p95_criar_tarefa": 0.14, "taxa_erro_percentual": 0.2, } print(gerar_status(metricas))

if __name__ == "__main__":
    main()
```

O endpoint `/health` — que o smoke test do Capítulo 18 já consultava — agora retorna o estado completo: status, versão e métricas. É o painel mínimo que a ferramenta de monitoramento da plataforma consome.

### Passo 4: O Relatório de Métricas de Engenharia

O quarto passo traduz os dados em decisão — o relatório das quatro métricas do DORA. O script coleta os números da semana e gera o veredito:

```python
# scripts/relatorio_dora.py — Relatorio semanal das 4 metricas DORA
from dataclasses import dataclass

@dataclass class Semana: deploys: int lead_time_dias: float falhas: int mttr_horas: float total_changes: int

SEMANAS = [
    Semana(deploys=14, lead_time_dias=1.2, falhas=1, mttr_horas=0.8, total_changes=14),
    Semana(deploys=18, lead_time_dias=0.9, falhas=2, mttr_horas=1.1, total_changes=18),
]

def taxa_falha(semana: Semana) -> float:
    """Percentual de mudancas que causaram falha em producao."""
    return 100 * semana.falhas / semana.total_changes if semana.total_changes else 0.0

def avaliar(semana: Semana) -> str: """Classifica o desempenho segundo os limiares DORA (elite/alto/medio/baixo).""" falha = taxa_falha(semana) if semana.lead_time_dias < 1 and falha < 15: return "ELITE" if semana.lead_time_dias < 7 and falha < 45: return "ALTO" if falha < 45: return "MEDIO" return "BAIXO"

def main() -> None: """Exibe o relatorio das metricas de engenharia da semana.""" print("RELATORIO DORA (metricas de engenharia):") for i, semana in enumerate(SEMANAS, 1): print(f"  Semana {i}: deploys={semana.deploys}, lead={semana.lead_time_dias}d, " f"falha={taxa_falha(semana):.1f}%, mttr={semana.mttr_horas}h -> {avaliar(semana)}") print("Meta: frequencia alta com falha baixa e recuperacao rapida (elite).")

if __name__ == "__main__":
    main()
```

O relatório DORA é o painel de decisão do mestre em operação: cada semana, quatro números dizem se a entrega está saudável — e o veredito (ELITE/ALTO/MÉDIO/BAIXO) sinaliza onde ajustar.

### Passo 5: O Loop de Iteração com o Agente

O quinto passo é o loop completo em ação — o diagnóstico assistido por agente. O prompt que você usa quando uma métrica aponta problema:

```markdown
## Papel e contexto
Você é o engenheiro de operações da TorreDeControle. As métricas da semana
mostram: latencia p95 de "criar_tarefa" subiu de 0.14s para 0.9s; taxa de
erro em "mover_tarefa" subiu de 0.2% para 4%.

## Tarefa específica
Diagnostique as possíveis causas usando os logs estruturados e o código.
Proponha hipóteses ordenadas por probabilidade, cada uma com o dado que a
suporta e o teste que a confirmaria.

## Restrições e regras
- NÃO modifique código de produção.
- Use evidência dos logs (evento, dados) — não suposição.
- Para cada hipótese, indique a métrica que a confirmaria ou refutaria.

## Formato de saída
Lista de hipóteses: {hipotese, evidencia, teste_para_confirmar, risco}.

## Critérios de aceite
1. Pelo menos 3 hipóteses distintas com evidência de log.
2. Nenhuma hipótese sem teste de confirmação.
3. Nenhuma proposta de mudança direta em produção.
```

O loop com agente: os dados apontam, o agente investiga, você decide a correção, o pipeline entrega, a métrica confirma. Autonomia na análise, controle na decisão — o espectro do Capítulo 13 em operação.

### O Protocolo de Operação Contínua

Para fechar, o protocolo de operação — a rotina semanal do mestre em regime de operação:

1. **Ler o painel**: métricas essenciais (requisições, latência p95, taxa de erro) e o relatório DORA da semana.
2. **Investigar anomalias**: qualquer pico é uma pergunta — o agente ajuda no diagnóstico com os logs.
3. **Priorizar correções**: o que melhora a métrica mais importante primeiro (taxa de falha de mudança é a régua).
4. **Iterar pelo fluxo completo**: toda correção passa pela rampa do Capítulo 17 — nada de mudança direta em produção.
5. **Registrar aprendizados**: incidentes e correções viram entradas na memória do Capítulo 16 — o prédio aprende.

## Aplica

### A Cena de Contraste: A Queda Silenciosa

Imagine o primeiro mês da TorreDeControle em produção — sem observabilidade, "porque funciona". Os usuários usam, ninguém reclama, e você assume que está tudo bem. Na verdade, há um padrão silencioso: a cada semana, um endpoint fica um pouco mais lento (um índice de banco faltando, revelado pelo crescimento dos dados), e a taxa de erro em um fluxo secundário sobe devagar. Ninguém reclama — porque a degradação é gradual. No dia em que o volume dobra, o endpoint colapsa, o erro vira generalizado, e a caixa preta — que nunca foi instrumentada — é investigada no escuro, com usuários reais no meio do apagão.

O diagnóstico: a ausência de reclamação foi interpretada como saúde — o prédio sem medidores do Capítulo 3 da operação. O colapso não foi súbito: foi a soma de degradações graduais que ninguém media.

A correção: você instrumenta o sistema — logs estruturados, métricas essenciais, endpoint de saúde e o relatório DORA semanal. Três semanas depois, o mesmo padrão de degradação aparece nos medidores: a latência p95 subindo, o erro subindo devagar — e o diagnóstico assistido por agente aponta o índice faltante antes do colapso. A correção passa pelo fluxo completo, o deploy sai pela rampa, e a métrica confirma a volta aos padrões. A lição: operar sem medir é apostar — e o prédio habitado se administra com medidores, não com sorte.

### Armadilhas Comuns na Operação

- **Logs sem estrutura**: print solto não é buscável. Log JSON com evento e dados.
- **Métricas sem ação**: colecionar números sem o loop de iteração é burocracia. Métrica aponta → diagnóstico → correção → verificação.
- **Painel sem leitor**: instrumentar sem ler o relatório semanal é gasto sem retorno. Rotina de leitura.
- **Diagnóstico no escuro**: investigar incidente sem logs é arqueologia. Instrumentação mínima desde o dia um.
- **Correção direta em produção**: mudar código no servidor vivo quebra a rampa. Toda correção passa pelo pipeline.
- **Ignorar a taxa de falha de mudança**: a métrica que mede se a velocidade está saindo cara. A régua do fluxo agêntico.

### Exercício Prático

Instrumente a TorreDeControle: configure os logs estruturados (`logging_config.py`), o coletor de métricas (`metricas.py`), o endpoint de saúde (`health.py`) e o relatório DORA (`relatorio_dora.py`). Simule uma anomalia (uma métrica fora do padrão) e rode o prompt de diagnóstico assistido por agente — documentando as hipóteses e o teste de confirmação de cada uma.

### Aprofundamento: O Painel Semanal de Operação

A operação do Capítulo 19 funciona com rotina — e a rotina tem um instrumento: o painel semanal de operação. Este é o modelo do painel que você preenche toda segunda-feira, em dez minutos:

```markdown
# Painel Semanal de Operação — TorreDeControle (semana de <data>)

## Saúde do serviço
- Disponibilidade: <99.x%> (meta: 99.5%)
- Latência p95 de criar_tarefa: <0.15s> (tendência: subindo/estável/descendo)
- Taxa de erro: <0.3%> (tendência: ...)

## Métricas DORA
- Frequência de deploy: <N> deploys na semana.
- Lead time de mudança: <X dias> (commit -> produção).
- Taxa de falha de mudança: <Y%> (deploys que causaram incidente).
- MTTR: <Z horas> (tempo médio de recuperação).

## Incidentes e aprendizados
- <incidente 1> -> causa, correção, aprendizado registrado na memória.
- <nenhum> -> semana limpa.

## Decisões da semana
- <decisão 1> -> registrada no diário de decisões (Cap. 5).

## Próximos passos
- <item 1> -> fatia pequena, testes, pipeline.
```

O painel tem três funções: (1) *obriga a medição* — o que não está no painel não está sendo medido; (2) *cria a linha de base* — a tendência importa mais que o número isolado, e o painel acumula o histórico; (3) *alimenta o loop* — cada número anômalo do painel dispara o diagnóstico assistido por agente do Capítulo 19. A disciplina do painel é a mesma do diário de decisões: dez minutos semanais que economizam horas de reação. E quando o painel mostra três semanas de saúde estável, é o sinal de que o sistema atingiu a maturidade operacional — e que você pode subir o nível de autonomia pelo protocolo do Capítulo 13, porque a evidência (não a confiança) sustenta a promoção.

## Conclusão

Neste capítulo você assumiu a operação do prédio habitado: entendeu a observabilidade — os três pilares de logs, métricas e rastreios; dominou as quatro métricas do DORA — frequência de deploy, lead time, taxa de falha e tempo de recuperação; instrumentou a TorreDeControle com logs estruturados, coletor de métricas e endpoint de saúde; e fechou o loop de iteração — dados → diagnóstico assistido por agente → correção pela rampa → verificação pela métrica. A lição central: operar não é rodar — é medir, entender e melhorar continuamente; e o prédio habitado se administra com medidores, não com palpite.

Seu desafio: a TorreDeControle instrumentada — logs estruturados, métricas coletadas, relatório DORA da semana e um ciclo completo de diagnóstico assistido por agente documentado.

No Capítulo 20, o último da obra: o engenheiro do futuro — a mentalidade AIDD, o portfólio do Mestre de Obras e como se posicionar no mercado de 2026 com a jornada completa que você percorreu.

# Capítulo 20: O engenheiro do futuro: carreira e mentalidade AIDD

# Capítulo 20: O engenheiro do futuro: carreira e mentalidade AIDD

## Introdução

O prédio está de pé. A TorreDeControle nasceu como um terreno baldio no Capítulo 1 e agora opera na nuvem, monitorada, com um pipeline que entrega melhorias contínuas. Mas há um último andar que nenhum capítulo anterior construiu: **você**. A obra que você ergueu nestas vinte etapas foi, em paralelo, a construção de uma carreira — e é sobre essa construção que este capítulo final trata.

O mercado de 2026 está redesenhando o perfil do desenvolvedor em torno do AIDD — e a pesquisa é clara: o valor não está em quem digita mais rápido, mas em quem projeta, audita e comanda sistemas agênticos. Este capítulo fecha a jornada do Mestre de Obras: o mapa das competências do engenheiro AIDD, o portfólio que prova a jornada (e a TorreDeControle é a sua peça central), e a mentalidade e a ética que sustentam o profissional do futuro. Ao final, você terá o plano concreto de posicionamento — e a certeza de que a jornada que percorreu é o ativo mais valioso do seu currículo.

## Explica

#### O novo mapa de competências

O relatório DORA e a análise de mercado convergem num ponto: as habilidades que separam profissionais no fluxo agêntico não são as do autocomplete — são as do sistema ao redor do modelo. O mapa tem cinco grupos:

1. **Engenharia de contexto**: arquitetar o que o modelo recebe — manual de bordo, memória, recuperação sob demanda (Capítulos 5-6, 16). O grupo mais valioso e mais raro.
2. **Engenharia de especificação**: transformar intenção em contrato verificável — spec-driven development (Capítulo 7). A ponte entre negócio e código.
3. **Governança e segurança**: hooks, permissões, blindagem de ferramentas (Capítulos 11, 13). O que transforma autonomia em responsabilidade.
4. **Verificação**: testes, revisão autônoma, auditorias (Capítulos 14-15). O que transforma velocidade em confiança.
5. **Orquestração**: subagentes, pipelines, operação (Capítulos 12, 17-19). O que transforma esforço em sistema.

Repare no padrão: nenhum dos cinco grupos é "escrever código mais rápido". O código o modelo escreve; o valor humano está em tudo que *cerca* o código — e é exatamente isso que este livro construiu, capítulo a capítulo.

### O engenheiro AIDD vs. o usuário de IA

A distinção que resume o livro inteiro: **o usuário de IA consome o modelo; o engenheiro AIDD projeta o sistema ao redor dele**. O usuário abre o chat e pede; o engenheiro especifica, governa, verifica e opera. A diferença não é técnica — é de método: o usuário trata o modelo como oráculo; o engenheiro trata o modelo como componente de um sistema que ele projeta.

Essa distinção tem consequência de mercado: conforme a adoção de IA se universaliza (97% do mercado em algum grau, como você viu no Capítulo 1), a commodity é "saber usar IA" — e o escasso é "saber construir o sistema que a torna confiável". A escassez é o seu espaço: é o engenheiro do futuro, e é você.

### Portfólio: provar a jornada, não prometê-la

O portfólio do engenheiro AIDD não é uma lista de projetos — é a **evidência da jornada**: cada projeto prova que o candidato domina o método, não apenas a ferramenta. A TorreDeControle é o portfólio perfeito porque contém, em um artefato, todos os capítulos: a especificação viva (Capítulo 7), o manual de bordo (Capítulo 6), as skills (Capítulo 9), as ferramentas blindadas (Capítulo 11), a governança (Capítulo 13), os testes (Capítulo 14), o pipeline (Capítulo 17) e a operação monitorada (Capítulo 19).

O portfólio eficaz tem quatro peças, e a TorreDeControle as preenche todas:

1. **O repositório**: código real, com histórico limpo, convenções e documentação — legível por um avaliador em minutos.
2. **O diário de decisões**: o registro do *porquê* — as decisões de arquitetura, os erros corrigidos (o ADR do Capítulo 5). É o que separa o portfólio do "código que funciona" do "engenheiro que decide".
3. **A demonstração**: o produto no ar (Capítulo 18), com a URL pública — o avaliador não precisa acreditar, pode ver.
4. **A narrativa**: a história da jornada — do zero ao deploy — contada em poucos parágrafos, com métricas: capítulos, testes, pipeline, métricas DORA.

### A ética do desenvolvimento dirigido por IA

O último pilar conceitual é a **ética** — a responsabilidade que acompanha a autonomia. Quatro princípios sustentam o engenheiro AIDD responsável:

1. **Responsabilidade final humana**: o agente executa; o humano responde. Autonomia crescente exige controle redesenhado na mesma proporção — a lição do Capítulo 13 em escala de carreira.
2. **Transparência de uso**: o que foi gerado por IA e o que foi revisado por humano — em código, em avaliações, em decisões. A honestidade é o ativo de reputação.
3. **Segurança como dever**: blindar ferramentas, proteger segredos, não expor dados de usuário — a ética do Capítulo 11 vira postura profissional.
4. **Aprendizado contínuo**: o campo muda em meses; a competência é a capacidade de re-aprender — a memória externa do Capítulo 16 vira hábito de carreira.

## Ilustra

### O Mestre de Obras Diplomado

Volte ao canteiro — o último dia, agora em retrospectiva. O mestre que você era no Capítulo 1 conhecia o terreno baldio; o mestre que você é agora entregou o prédio, e a diferença entre os dois não está nas mãos — está no **método**. No dia um, você sabia assentar tijolo (programar); hoje você sabe *dirigir uma obra inteira*: planta (spec), placa de regras (manual), equipes (subagentes), máquinas (tools), porteiro (governança), medidores (observabilidade) e rampa (pipeline).

O mercado de 2026 está cheio de pedreiros competentes — profissionais que sabem "usar IA". Está vazio de mestres de obras — profissionais que sabem dirigir sistemas agênticos do zero ao deploy. E é exatamente essa raridade que este livro construiu: não um curso de ferramenta, mas a diplomação do método.

```mermaid
%% legenda: A jornada do Mestre de Obras: do terreno baldio a entrega das chaves e a operacao
flowchart LR
  A[Cap 1-4: fundamentos e primeira fatia] --> B[Cap 5-8: contexto, manual, spec e esqueleto]
  B --> C[Cap 9-12: skills, MCP, tools e subagentes]
  C --> D[Cap 13-16: governanca, testes, revisao e economia]
  D --> E[Cap 17-19: pipeline, deploy e operacao]
  E --> F[Cap 20: o Mestre de Obras diplomado]
  F --> G[Proxima obra: o metodo se repete]
  G --> B
```

### O Pedreiro que Virou Mestre: Por Que o Método é o Diferencial

Aqui está o ponto contraintuitivo do capítulo final — a segunda camada de analogia. A primeira mostrou a diplomação do mestre. A segunda é sobre por que o método, e não a ferramenta, é o ativo que não envelhece.

Imagine dois profissionais em 2024, quando o autocomplete reinava. O primeiro dominou a ferramenta da época com perfeição: conhecia cada atalho, cada extensão, cada truque do autocomplete. O segundo investiu no método: especificação, revisão, testes, arquitetura. Em 2026, a ferramenta do primeiro virou commodity — o autocomplete morreu engolido pelos agentes, e o conhecimento dele virou obsoleto da noite para o dia. O segundo — que nunca dependeu da ferramenta — migrou para os agentes com o método intacto: especificação, revisão e testes continuam sendo a essência, com outra ferramenta no centro.

A lição é a mais importante do livro: **ferramentas envelhecem; métodos persistem**. O autocomplete deu lugar aos agentes; os agentes de hoje darão lugar a algo novo; e o método — especificar, governar, verificar, operar — atravessa todas as eras. Como Mestre de Obras, o seu ativo não é o harness que você usa em 2026: é o método que você construiu nestas vinte etapas e que funciona com qualquer ferramenta, em qualquer era.

## Técnica

### Passo 1: O Mapa de Competências Pessoal

O primeiro passo técnico é o auto-diagnóstico: mapear onde você está nos cinco grupos de competências — e onde precisa investir. Este é o modelo do mapa, com a autoavaliação:

```markdown
# Mapa de Competências — <Seu Nome> (data)

#### 1. Engenharia de contexto
- [x] Escrevo CLAUDE.md/AGENTS.md (Cap. 6)
- [x] Arquitetura de contexto em 3 niveis (Cap. 5)
- [ ] Economia severa de tokens em sessões longas (Cap. 16)
- Nivel: iniciante | intermediario | avancado

#### 2. Engenharia de especificação
- [x] Spec viva com criterios de aceite (Cap. 7)
- [ ] Traduzir critérios em testes (Cap. 14)
- Nivel: ...

#### 3. Governança e segurança
- [x] Hooks e permissoes (Cap. 13)
- [x] Blindagem de tools (Cap. 11)
- [ ] Auditoria de servidores MCP de terceiros
- Nivel: ...

#### 4. Verificação
- [x] Testes de regras de negocio (Cap. 14)
- [x] Revisao autonoma em 2 camadas (Cap. 15)
- Nivel: ...

#### 5. Orquestração
- [x] Subagentes e lotes (Cap. 12)
- [x] Pipeline CI/CD (Cap. 17)
- [ ] Operacao com metricas DORA (Cap. 19)
- Nivel: ...

## Plano de investimento (proximos 90 dias)
- Fortalecer: <grupo 1>
- Aprender: <grupo 2>
- Provar com: <projeto/artefato>
```

O mapa é o instrumento da carreira: ele transforma "estou aprendendo AIDD" em "estou em X dos cinco grupos, com plano para Y". É a mesma disciplina de especificação que você aplicou à TorreDeControle — agora aplicada a você.

### Passo 2: O Documento da Jornada (narrativa de portfólio)

O segundo passo é a narrativa — o documento que conta a jornada em poucos parágrafos. Este é o modelo, pronto para preencher com os dados da sua TorreDeControle:

```markdown
# Projeto TorreDeControle — Jornada do Zero ao Deploy

## Resumo (2 frases)
Aplicativo web de gestão de tarefas construído inteiramente com AI Driven
Development, do terreno baldio ao deploy na nuvem, com o método completo:
especificação viva, manual de bordo, skills, ferramentas blindadas,
governança, testes, pipeline e operação monitorada.

## A jornada em números
- 20 capítulos de método aplicados (do conceito à operação).
- Spec com N requisitos e M regras de negócio (cada uma com teste).
- Pipeline com N gates: sintaxe, testes, auditoria, build.
- Métricas DORA: frequência de deploy X/semana, falha Y%, MTTR Z h.

## O que a jornada prova
1. Especificar antes de codar: o contrato que guiou todos os agentes.
2. Governar a autonomia: hooks, permissões e blindagem de ferramentas.
3. Verificar tudo: testes por regra, revisão em 2 camadas, pipeline.
4. Operar com dados: logs estruturados, métricas e loop de iteração.

## Como ver (links)
- Repositório: <url>
- Demonstração no ar: <url>
- Especificação e diário de decisões: <caminhos>
```

A narrativa é a peça que o avaliador lê primeiro — e ela conta a história do método, não da ferramenta. Cada afirmação tem um artefato por trás (o repositório, a URL, o diário): é a rastreabilidade do Capítulo 14 aplicada à carreira.

### Passo 3: O Gerador de Portfólio

O terceiro passo é o gerador que monta o portfólio a partir do repositório — a evidência organizada em um documento:

```python
# gerar_portfolio.py — Monta o sumario do portfolio a partir do repositorio
import json
from datetime import date
from pathlib import Path

def contar_testes() -> int:
    """Conta os arquivos de teste do projeto."""
    return len(list(Path("tests").glob("test_*.py"))) if Path("tests").exists() else 0

def contar_skills() -> int:
    """Conta as skills do projeto."""
    base = Path(".claude/skills")
    return len([p for p in base.iterdir() if (p / "SKILL.md").exists()]) if base.exists() else 0

def contar_subagentes() -> int:
    """Conta as definicoes de subagentes do projeto."""
    base = Path(".claude/agents")
    return len(list(base.glob("*.md"))) if base.exists() else 0

def gerar_manifesto_portfolio() -> dict: """Gera o manifesto do portfolio com os artefatos da jornada.""" return { "projeto": "TorreDeControle", "gerado_em": date.today().isoformat(), "artefatos": { "especificacao": str(Path("docs/especificacao.md")), "manual_de_bordo": str(Path("AGENTS.md")), "diario_de_decisoes": str(Path("docs/decisoes.md")), "mapa_de_contexto": str(Path("docs/mapa_contexto.md")), "mapa_de_permissoes": str(Path("docs/mapa_permissoes.md")), }, "evidencias": { "testes": contar_testes(), "skills": contar_skills(), "subagentes": contar_subagentes(), "pipeline": str(Path(".github/workflows")), }, }

def main() -> None:
    """Gera o manifesto do portfolio e imprime o resumo."""
    manifesto = gerar_manifesto_portfolio()
    print(json.dumps(manifesto, ensure_ascii=False, indent=2))
    print(f"\nTotal de evidencias: {len(manifesto['artefatos']) + len(manifesto['evidencias'])}")

if __name__ == "__main__":
    main()
```

O manifesto do portfólio é a prova organizada: artefatos (spec, manual, diário, mapas) e evidências (testes, skills, subagentes, pipeline) — cada item um capítulo do livro materializado.

### Passo 4: O Plano de Posicionamento de 90 Dias

O quarto passo é o plano concreto de posicionamento — as ações dos próximos 90 dias, com prazo e critério de conclusão:

```markdown
# Plano de Posicionamento — 90 dias

## Dias 1-30: consolidar a TorreDeControle
- [ ] Publicar o repositório (público ou com acesso controlado).
- [ ] Publicar a demo no ar (Cap. 18) e validar o smoke test.
- [ ] Completar o manifesto do portfólio (gerar_portfolio.py).
- Criterio: URL pública + repositório legível + manifesto completo.

## Dias 31-60: preencher lacunas do mapa
- [ ] Fortalecer o grupo mais fraco do mapa de competências (Passo 1).
- [ ] Criar um segundo projeto curto aplicando o método (ex.: uma skill
       nova, um servidor MCP próprio, uma automação de operação).
- Criterio: 1 artefato novo + 1 competência promovida de nivel.

## Dias 61-90: posicionamento no mercado
- [ ] Escrever o relato da jornada (Passo 2) e publicar.
- [ ] Conectar com o mapa: 1 post/relato por semana sobre o método.
- [ ] Aplicar para oportunidades com o método na frente do currículo.
- Criterio: relato publicado + rede ativa + N candidaturas enviadas.
```

O plano de 90 dias é a rampa da carreira: ações com prazo e critério — a mesma disciplina de fatias do Capítulo 8, agora aplicada ao posicionamento profissional.

### O Protocolo de Carreira Contínua

Para fechar, o protocolo que sustenta a carreira no longo prazo — o loop de iteração do Capítulo 19 aplicado à sua evolução:

1. **Medir**: o mapa de competências revisado a cada 90 dias — onde estou nos cinco grupos?
2. **Iterar**: cada lacuna vira um projeto pequeno que a preenche — o método do Capítulo 8 aplicado a você.
3. **Provar**: cada competência vira artefato público — o portfólio cresce com evidência, não com promessa.
4. **Aprender com o ciclo**: o campo muda; o re-aprendizado é rotina — a memória externa do Capítulo 16 como hábito de carreira.

## Aplica

### A Cena de Contraste: O Currículo de Promessas

Imagine a entrevista em que dois candidatos se apresentam. O primeiro mostra um currículo de promessas: "experiência com IA, ChatGPT, Claude, ferramentas de ponta", listas de ferramentas que "domina". O segundo abre o portfólio: o repositório da TorreDeControle com histórico limpo, a especificação viva com critérios de aceite, o diário de decisões com os porquês, a URL da demo no ar, e o relato da jornada em números — testes por regra, pipeline com gates, métricas DORA. O avaliador não precisa acreditar no segundo: pode ver.

O diagnóstico da diferença: o primeiro vendeu ferramenta (commodity, todo mundo tem); o segundo vendeu método (escasso, difícil de copiar). A entrevista não foi ganha na conversa — foi ganha no repositório, meses antes, quando o método foi aplicado.

A correção (para quem ainda está no primeiro perfil): aplicar o plano de 90 dias — consolidar a obra, preencher lacunas, posicionar com evidência. Em três meses, o currículo de promessas vira portfólio de prova — e a conversa de entrevista muda de "eu conheço X" para "aqui está o que o método produziu, e aqui está o porquê". A lição do capítulo final: no mercado do engenheiro do futuro, quem mostra vence quem promete — e a jornada que você completou é a prova que o mercado procura.

### Armadilhas Comuns na Carreira AIDD

- **Confundir ferramenta com método**: dominar o harness de 2026 sem o método é obsoletizar-se junto com ele. Método persiste; ferramenta envelhece.
- **Portfólio sem evidência**: lista de projetos sem artefatos legíveis é promessa. Repositório, diário, demo, narrativa.
- **Vender a ferramenta, não a jornada**: "usei X" é commodity; "projetei o sistema ao redor do modelo" é o diferencial.
- **Ignorar a ética**: autonomia sem responsabilidade é incidente de carreira. Transparência, segurança e responsabilidade final.
- **Parar de medir a própria evolução**: sem o mapa de competências, a carreira anda sem direção. Revisão a cada 90 dias.
- **Tratar o AIDD como fase**: o método é a constante; as ferramentas são as variáveis. Invista no que atravessa eras.

### Exercício Prático (o desafio final)

Complete as quatro peças do posicionamento: (1) o mapa de competências pessoal com o plano de 90 dias; (2) o documento da jornada da TorreDeControle com os números reais; (3) o manifesto do portfólio gerado pelo `gerar_portfolio.py`; e (4) a reflexão ética por escrito — suas respostas para os quatro princípios. Este exercício não tem veredito automático: é o início da próxima obra — você.

### Aprofundamento: O Elevator Pitch do Mestre de Obras

A jornada que você percorreu precisa ser contável em trinta segundos — o *elevator pitch* que você usa em entrevistas, networking e conversas de corredor. Este é o modelo, com a estrutura que qualquer avaliador entende em uma respirada:

> "Construí um aplicativo completo — da especificação ao deploy na nuvem — usando AI Driven Development como método, não como ferramenta. Em vez de aceitar código gerado por IA, eu projetei o sistema ao redor do modelo: especificação viva com critérios de aceite, manual de bordo que ensina o agente as regras do projeto, governança com hooks e permissões, testes para cada regra de negócio e um pipeline que prova cada commit. O resultado está no ar, monitorado, com métricas de engenharia — e o método se repete em qualquer projeto, com qualquer ferramenta."

A estrutura do pitch tem quatro tempos, espelhando o livro: (1) **o feito** — um aplicativo do zero ao deploy; (2) **a virada** — AIDD como método, não como ferramenta; (3) **a prova** — especificação, governança, testes, pipeline (as peças do portfólio); (4) **a generalização** — o método se repete. Cada tempo é uma frase — se o pitch passa de quatro frases, ele perde o impacto.

Três variações do pitch, conforme o interlocutor: para um **recrutador técnico**, enfatize a prova (testes por regra, gates de pipeline, métricas DORA); para um **líder de produto**, enfatize a confiabilidade (o que permite velocidade sem incidentes); para um **par desenvolvedor**, enfatize o método (como especificar, governar e verificar). O conteúdo é o mesmo; o peso muda — e é essa adaptação que mostra maturidade.

```bash
# Treino do pitch em 3 passos:
# 1. Escreva as 4 frases (feito, virada, prova, generalizacao)
# 2. Grave-se falando; corte o que passar de 30 segundos
# 3. Treine uma variacao por dia ate sair sem roteiro
```

O pitch é o resumo do portfólio em formato conversacional — e, como o portfólio, ele vende método, não ferramenta. Quando a conversa termina e o avaliador se lembra de "alguém que constrói sistemas agênticos do zero ao deploy", o pitch cumpriu o papel.

## Conclusão

Neste capítulo final você construiu o último andar: o mapa de competências do engenheiro AIDD — contexto, especificação, governança, verificação e orquestração; a distinção entre o usuário de IA e o engenheiro que projeta o sistema ao redor do modelo; o portfólio como evidência da jornada — repositório, diário, demo e narrativa; e a ética — responsabilidade final, transparência, segurança e aprendizado contínuo. A lição final do livro: ferramentas envelhecem, métodos persistem — e você, Mestre de Obras, agora carrega o método que atravessa todas as eras.

O desafio final: aplicar o plano de 90 dias e começar a próxima obra — porque o método que você construiu não é um fim: é a ferramenta que constrói todas as próximas construções. Do zero ao deploy, sempre.

# Para se aprofundar

Quer ir além? Estas são fontes confiáveis para continuar a jornada:

- **Model Context Protocol** — documentação oficial do protocolo que conecta agentes ao mundo real: https://modelcontextprotocol.io
- **SWE-bench** — benchmark de referência para avaliar agentes de codificação: https://www.swebench.com
- **DORA / Google Cloud** — relatórios de produtividade e ROI da engenharia com IA: https://dora.dev
- **Anthropic** — engenharia e boas práticas de agentes e contextos: https://www.anthropic.com
- **Sourcegraph** — guia prático de engenharia de contexto para agentes: https://sourcegraph.com/blog/context-engineering

E, claro, o livro completo **AI Driven Development: Do Zero ao Deploy** aprofunda cada um desses temas com o projeto TorreDeControle do início ao fim.

# Próximos Passos

Você acabou de percorrer o essencial de **AI Driven Development: Do Zero ao Deploy** — e o projeto **TorreDeControle**, que nasceu como um terreno baldio, agora está de pé.

Se este ebook foi útil, o livro completo leva a jornada muito mais longe: vinte capítulos, cinco partes e o projeto prático do início ao fim — do primeiro prompt à entrega das chaves em produção, com testes, revisão autônoma, CI/CD, deploy na nuvem e monitoramento.

**O que fazer agora:**

1. **Aplique hoje**: escolha uma ideia pequena e construa com o agente usando o que você aprendeu aqui. A prática consolida.
2. **Aprofunde**: siga para o próximo ebook da série ou para o livro completo *AI Driven Development: Do Zero ao Deploy*.
3. **Compartilhe**: se este conteúdo acelerou o seu aprendizado, indique para alguém que também está começando na jornada agêntica.

O terreno baldio da sua próxima ideia está esperando. Até a entrega das chaves!

**Heverton Eduardo Peres** — Especialista em Marketing e Desenvolvimento de Soluções

