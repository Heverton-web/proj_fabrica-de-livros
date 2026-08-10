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