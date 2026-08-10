# LSP Integrado: Inteligência de Código em Cada Escrita

## Inteligência embarcada no estaleiro

No capítulo anterior, você dominou as edições hashline — o sistema que permite ao agente apontar para blocos de código usando hashes em vez de retratar linhas inteiras, economizando até 61% de tokens de saída.

Mas edits precisos não são suficientes quando o agente precisa ENTENDER o código antes de mexer nele. É aqui que entra o LSP — o Language Server Protocol — a mesma tecnologia que faz o VS Code autocompletar, mostrar erros em tempo real e renomear símbolos em todo o projeto.

## O que é o LSP e por que ele importa

O Language Server Protocol (LSP) é um protocolo padronizado que separa a inteligência de código do editor. Antes do LSP, cada editor precisava implementar sua própria integração com cada linguagem — um trabalho hercúleo e duplicado. Com o LSP, um único servidor de linguagem serve qualquer editor que suporte o protocolo.

Pense no LSP como um conjunto de especialistas embarcados no estaleiro. Cada um conhece profundamente uma linguagem e pode responder perguntas como: "Onde essa função é definida?", "Quais arquivos usam esse símbolo?", "Esse código tem erros?", "Como posso renomear isso de forma segura?".

Antes do LSP, esses especialistas só existiam dentro do IDE. No OMP, eles estão disponíveis para o agente em cada interação.

## As 14 operações LSP

O OMP expõe 14 operações LSP organizadas em duas categorias: operações de documento (que analisam um arquivo específico) e operações de workspace (que varrem o projeto inteiro).

### Operações de documento

1. **diagnostics** — erros e warnings em tempo real, como um inspetor que sinaliza falhas estruturais no casco.

2. **hover** — informações sobre um símbolo ao passar o cursor, como uma placa de especificações de um equipamento.

3. **definition** — localiza onde um símbolo é definido, como um mapa mostrando a origem de cada peça.

4. **implementation** — encontra todas as implementações de uma interface, como um inventário de todas as variantes de um componente.

5. **typeDefinition** — mostra o tipo de um símbolo, como a ficha técnica detalhada de um material.

6. **completion** — sugere código contextualmente, como um catálogo de peças compatíveis.

7. **signatureHelp** — mostra os parâmetros de uma função durante a digitação, como um manual aberto na página certa.

8. **formatting** — formata o código conforme padrões, como um alinhador que deixa tudo no padrão do estaleiro.

9. **codeLens** — exibe informações contextuais inline (número de referências, testes), como indicadores painel no navio.

10. **documentSymbol** — lista todos os símbolos de um arquivo, como o índice de peças de um navio.

### Operações de workspace

11. **references** — encontra todas as ocorrências de um símbolo no projeto, como um radar que detecta todas as dependências.

12. **workspaceSymbol** — busca símbolos em todo o workspace, como um sistema de GPS que localiza qualquer componente.

13. **rename** — renomeia um símbolo em todos os arquivos de forma segura, como um engenheiro que atualiza todos os registros antes de mudar o nome de uma peça.

14. **codeAction** — sugere correções e refactorings, como um consultor que recomenda melhorias com base no estado atual.

## A magia do rename com willRenameFiles

O rename é provavelmente a operação LSP mais poderosa no dia a dia do agente. Quando o OMP pede um rename, o fluxo não é apenas "trocar o nome em todos os arquivos".

O protocolo workspace/willRenameFiles garante que re-exports, barrel files e imports com alias sejam atualizados ANTES do arquivo ser movido.

Isso é fundamental: sem willRenameFiles, um rename poderia quebrar imports em módulos que o agente nem conhece. Com o protocolo, o servidor LSP percorre toda a cadeia de dependências e ajusta tudo antes que a mudança aconteça.

É como ter um engenheiro que verifica todos os navios afetados antes de remover uma peça do estaleiro.

## Auto-detecção e configuração

O OMP não exige configuração manual para a maioria dos cenários. O sistema de auto-detecção verifica duas condições.

Primeiro, o diretório de trabalho contém pelo menos um dos `rootMarkers` do servidor (como `package.json` para TypeScript, `Cargo.toml` para Rust, `go.mod` para Go).

Segundo, o binário do servidor está disponível — primeiro em diretórios locais do projeto (`node_modules/.bin/`, ambientes virtuais Python), depois no `$PATH`.

Quando ambas as condições são atendidas, o servidor inicia automaticamente. Para projetos que precisam de ajustes, a hierarquia de configuração permite overrides em diferentes níveis.

**Global:** `~/.lsp.json` ou `~/.omp/agent/lsp.json`

**Projeto:** `<cwd>/.omp/lsp.json`

**Raiz:** `<cwd>/lsp.json`

Cada nível herda do anterior e sobrepõe apenas os campos especificados — configuração merge shallow por servidor.

## Diagnostics: inspeção em tempo real

Quando o agente precisa saber se um arquivo tem erros, ele chama diagnostics. O servidor LSP analisa o arquivo e retorna uma lista de problemas — erros de sintaxe, warnings de tipos, inconsistências de formatação.

```json
{
  "operation": "diagnostics",
  "file": "src/main.rs"
}
```

O resultado contém a severidade (error, warning, info), a posição exata e a mensagem. É como ter um inspetor de quality assurance trabalhando 24/7 no estaleiro.

## Hover: especificações de um símbolo

Ao passar o cursor sobre um símbolo, o hover retorna o tipo, a documentação e a assinatura. No OMP, isso se traduz em uma chamada que o agente pode fazer antes de decidir como usar uma função.

```json
{
  "operation": "hover",
  "file": "src/utils.rs",
  "line": 42,
  "character": 15
}
```

É como consultar a ficha técnica de uma peça antes de instalá-la — você sabe exatamente o que está mexendo.

## Definition e References: mapeando dependências

Definition encontra onde um símbolo é definido. References encontra onde ele é usado. Juntos, eles dão ao agente o mapa completo de dependências.

No estaleiro, é como ter um sistema de rastreamento que mostra de onde veio cada peça e quais navios ela afeta — informação crucial antes de qualquer modificação.

## Rename: a operação mais poderosa

O rename é onde a integração do OMP realmente brilha. Quando o agente pede um rename, o servidor LSP usa workspace/willRenameFiles para garantir que todos os arquivos afetados sejam atualizados ANTES da mudança.

```json
{
  "operation": "rename",
  "file": "src/utils/format.ts",
  "line": 5,
  "character": 10,
  "newName": "formatBytes"
}
```

O resultado é uma lista de edits — cada um correspondendo a um arquivo que precisa ser alterado. Re-exports, barrel files, imports com alias, tudo atualizado de forma atômica.

## CodeAction: correções inteligentes

CodeAction analisa um trecho de código e sugere correções. Pode ser desde "importar o símbolo que está faltando" até "extrair método" ou "adicionar tipo de retorno".

```json
{
  "operation": "codeAction",
  "file": "src/main.ts",
  "line": 15,
  "character": 5,
  "endLine": 20,
  "endCharacter": 1,
  "only": ["quickfix", "refactor"]
}
```

É como ter um consultor sênior que olha para o código e diz: "Essa função poderia ser simplificada", "Esse import está faltando", "Esse tipo deveria ser explícito".

## Completion e SignatureHelp: assistência contextual

Completion oferece sugestões de código baseadas no contexto. SignatureHelp mostra os parâmetros de uma função enquanto o agente digita.

No estaleiro, é como ter um catálogo de peças que se atualiza automaticamente mostrando quais componentes são compatíveis com o que já está instalado.

## Configurando LSP servers

Para linguagens não suportadas pela auto-detecção, ou para projetos com necessidades específicas, a configuração é direta.

```json
{
  "servers": {
    "my-custom-lsp": {
      "command": "my-lsp-server",
      "args": ["--stdio"],
      "fileTypes": [".xyz"],
      "rootMarkers": [".xyz-project", ".git"]
    }
  }
}
```

Para desabilitar um servidor built-in em um projeto específico, basta adicionar `disabled: true` na configuração do projeto.

Para ajustar configurações de um servidor existente, basta sobrescrever os campos desejados — a configuração faz merge shallow.

## O rename que quebrou tudo vs. o rename seguro

Imagine que você pediu ao agente para renomear uma função `processData` para `transformPayload` em um projeto TypeScript com 15 arquivos.

Sem LSP, o agente faria um find-and-replace simples — trocando o nome em todos os arquivos. Mas e se um arquivo re-exporta a função com um alias? E se um barrel file indexa o módulo? E se um import usa `import { processData as pd }`? O find-and-replace simples ignora tudo isso e quebra o projeto silenciosamente.

Agora veja o que acontece com o LSP integrado do OMP. O agente chama a operação rename, o servidor LSP usa workspace/willRenameFiles para mapear TODAS as dependências — incluindo re-exports com alias, barrel files e imports dinâmicos — e gera uma lista de edits atômicos.

Cada arquivo é atualizado corretamente antes que o próximo seja processado. O resultado? Zero quebras, zero imports órfãos, zero erros de compilação.

Essa é a diferença entre ter um estagiário que faz find-and-replace e ter um engenheiro de confiabilidade que percorre toda a cadeia de dependências antes de mudar qualquer coisa.

## Armadilhas comuns

**Auto-detecção não encontrou o servidor.** Verifique se o `rootMarker` do servidor existe na raiz do projeto. Se o projeto usa uma estrutura não padrão, crie um `.omp/lsp.json` com os rootMarkers corretos.

**Conflito entre servidores para a mesma linguagem.** O OMP aceita múltiplos servidores para a mesma linguagem. Para evitar conflitos, desabilite o que não usa via `disabled: true` na configuração do projeto.

**Rename quebra imports dinâmicos.** O rename LSP não consegue rastrear imports dinâmicos (`import()`) — eles dependem de strings em runtime. Nesses casos, o agente deve complementar com grep para localizar e ajustar manualmente.

**Servidor não inicializa.** Se o binário do servidor não está no PATH nem nos diretórios locais do projeto, a auto-detecção falha silenciosamente. Use `lsp` com a operação `diagnostics` em um arquivo para verificar se o servidor está ativo.

## Próximos Passos

Neste capítulo, você conheceu as 14 operações LSP integradas ao OMP — desde diagnostics e hover até rename e codeAction — e entendeu como elas transformam a capacidade do agente de entender e modificar código com precisão.

Os três pontos que você deve levar deste capítulo: o LSP dá ao agente a mesma inteligência que o IDE — diagnósticos, navegação, renames seguros; a integração com willRenameFiles é o que separa um rename confiável de um quebrador de projeto; e a auto-detecção e a configuração hierárquica tornam o setup praticamente transparente para a maioria dos projetos.

No próximo capítulo, você vai dar um passo além da leitura e escrita de código: vamos explorar como o OMP dirige debuggers reais — lldb para C, dlv para Go, debugpy para Python — através da ferramenta DAP.

Acesse a documentação completa: https://omp.sh/docs

Siga-nous nas redes sociais para dicas, tutoriais e novidades sobre o Oh My Pi.
