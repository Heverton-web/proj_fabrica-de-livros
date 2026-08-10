# Colaboração ao Vivo com /collab

## Um colega sentado ao seu lado

No capítulo anterior, você configurou o advisor model — um revisor que observa cada turno e injeta notas inline, como um inspetor de qualidade que acompanha a construção do navio sem tocar em nenhuma ferramenta.

Mas e se, em vez de apenas um revisor distante, você pudesse ter um colega sentado ao seu lado no estaleiro, vendo exatamente o que você vê, apontando para o mesmo casco, e até mesmo segurando a chave de boca junto com você?

É exatamente isso que o comando `/collab` transforma em realidade.

## O que é o /collab e como ele funciona

Imagine que você está construindo um navio no estaleiro e quer mostrar o progresso para um colega que está em outro porto. Você poderia tirar fotos e enviar por e-mail, mas isso é lento e desatualizado. Ou poderia ligar uma câmera ao vivo — aí o colega vê tudo em tempo real, sem atraso.

O `/collab` é essa câmera ao vivo para a sua sessão OMP.

Quando você digita `/collab` no terminal, o OMP inicia um processo de relay: ele cria um servidor local temporário que compartilha a tela do terminal com quem tiver o link. Não é um streaming de vídeo — é uma conexão bidirecional onde o teammate pode ver tudo o que acontece na sessão e, dependendo do modo, até participar ativamente.

## Dois modos, dois papéis

O OMP oferece dois modos de acesso para a colaboração.

**Read-write:** o teammate pode não apenas ver, mas também digitar comandos, enviar mensagens ao agente e interagir com a sessão como se estivesse no seu terminal. É como entregar a chave do estaleiro para o colega — ele pode usar qualquer equipamento.

**Read-only:** o teammate apenas observa. Ele vê cada comando que você digita, cada resposta do agente, cada edição de arquivo — mas não pode intervir. É como colocar uma câmera de segurança no estaleiro: a tripulação trabalha normalmente, mas o observador vê tudo sem tocar em nada.

A escolha entre um e outro depende do cenário. Para um code review, o read-only pode ser suficiente. Para um pair programming onde vocês dois precisam editar o mesmo arquivo, o read-write é essencial.

## Como o link é gerado

O fluxo é simples. Você digita `/collab`, o OMP gera um link da forma `http://localhost:<porta>/collab` e exibe um QR code no terminal. Seu teammate escaneia o QR code com o celular ou abre o link no navegador. A partir desse momento, ele está conectado à sua sessão.

Não há necessidade de criar contas, configurar permissões ou instalar plugins. O link é temporário — assim como a sessão, ele expira quando você encerra o collab.

## Segurança: o que sai da sua máquina

Essa é a pergunta que todo Mestre de Estaleiro Digital faz antes de abrir as portas do estaleiro: "o que o visitingante pode ver?"

O OMP protege a sessão usando um mecanismo chamado **frames sealed client-side**. Cada frame de dados — cada mensagem que o teammate vê — é selado no seu computador antes de ser transmitido. Isso significa que o conteúdo é criptografado no ponto de origem e só pode ser descriptografado no ponto de destino.

O que isso implica na prática? Chaves de API, tokens de autenticação, variáveis de ambiente sensíveis — nada disso vaza para o teammate. O OMP filtra automaticamente o que pode e o que não pode ser compartilhado.

É como ter um estaleiro com vidros opacos: a tripulação vê tudo por dentro, mas o visitingante só vê o que está exposto no convés.

## Ativando a colaboração

O comando para iniciar uma sessão de colaboração é direto.

```bash
/collab
```

O OMP responderá com um link e um QR code. O formato do link é `http://localhost:<porta>/collab`. A porta é atribuída automaticamente pelo OMP — você não precisa configurar nada.

## Escolhendo o modo de acesso

Quando o teammate abre o link, ele vê uma tela de boas-vindas com duas opções.

**Entrar como observador (read-only):** clique no botão "Entrar como observador". A partir desse momento, ele vê tudo o que acontece na sessão, mas não pode digitar nada.

**Entrar como colaborador (read-write):** clique no botão "Entrar como colaborador". Agora ele pode digitar comandos, enviar mensagens ao agente e editar arquivos — exatamente como você.

No terminal do anfitrião, aparece uma notificação indicando quem entrou e em qual modo.

## O que o teammate vê

Independentemente do modo, o teammate visualiza o terminal inteiro — cada comando digitado, cada resposta do agente, cada erro que aparece. As edições de arquivo — quando o agente modifica um arquivo, o teammate vê a diff em tempo real. E os pensamentos do agente — se o agente estiver usando modo verbose, o teammate vê o raciocínio por trás de cada ação.

O que o teammate não vê: variáveis de ambiente (tokens, senhas, chaves de API), arquivos sensíveis (.env, credenciais), e processos internos do OMP.

Essa separação é automática e transparente — você não precisa configurar filtros manualmente.

## Encerrando a sessão collab

Quando o trabalho estiver pronto, basta digitar.

```bash
/collab --stop
```

O servidor relay é encerrado, o link expira e o teammate perde a conexão imediatamente. Não há dados persistentes — tudo o que aconteceu na sessão fica no seu terminal, não no servidor relay.

## Cenário prático: code review ao vivo

Imagine que você acabou de implementar uma funcionalidade complexa. Você quer que um colega mais experiente revise o código antes de commitar. Em vez de enviar um diff por e-mail e esperar horas pelo feedback, você faz o seguinte.

Primeiro, digita `/collab` no terminal. Depois, escaneia o QR code com o celular e envia o link para o colega pelo Slack. O colega abre o link no browser e entra como observador (read-only). Enquanto você explica o código, o colega vê cada linha, cada variável, cada decisão de arquitetura.

Ele aponta: "na linha 47, aquele `try/except` deveria capturar `ConnectionError` especificamente, não `Exception`". Você corrige na hora, o colega confirma, e o código está pronto para commit.

O tempo total? Minutos, não horas. E o nível de detalhe é o mesmo de estarem sentados lado a lado no estaleiro.

## Armadilhas comuns

**Esquecer de encerrar o collab.** Se você deixar o servidor relay rodando depois de terminar o trabalho, o link continua válido. Sempre digite `/collab --stop` ao final da sessão.

**Usar read-write sem necessidade.** Se o teammate só precisa observar, não dê acesso de escrita. Mais permissões do que o necessário são sempre um risco — mesmo com o sealed client-side, é melhor prevenir.

**Confundir collab com compartilhamento de tela.** O collab não é um streaming de vídeo — é uma conexão direta ao terminal. O teammate vê os comandos, não a sua tela de desktop.

**Até onde escala:** o collab funciona bem para sessões de 2 a 5 pessoas. Acima disso, a latência de conexão e a quantidade de dados transmitidos podem degradar a experiência.

## Próximos Passos

Neste capítulo, você viu como o `/collab` transforma o terminal em um espaço de trabalho compartilhado. Dois modos de acesso — read-write para colaboração ativa, read-only para observação segura. Segurança por design — frames sealed client-side garantem que dados sensíveis nunca saiam da sua máquina. E simplicidade de uso — um comando, um QR code, um link.

O `/collab` fecha o ciclo de colaboração que começou com o advisor model. Enquanto o advisor é um revisor autônomo que trabalha nos bastidores, o collab traz um ser humano real para a equação — com opinião, julgamento e a capacidade de dizer "para, isso vai dar problema".

No próximo capítulo, vamos além do código: browser e desktop automation.

Acesse a documentação completa: https://omp.sh/docs

Siga-nous nas redes sociais para dicas, tutoriais e novidades sobre o Oh My Pi.
