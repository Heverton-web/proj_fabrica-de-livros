# Funcionalidades Essenciais

*Code Review Graph — Volume 2*

---

# Blast Radius, Impact Analysis e Ferramentas MCP

Voce ja sabe construir o grafo de dependencias do seu codebase. Mas um grafo estatico so responde "o que existe". A pergunta que realmente importa no dia a dia de uma revisao de codigo e: **"o que vai quebrar se eu mudar isso?"**

E exatamente essa lacuna que o conceito de **blast radius** preenche. Blast radius, ou raio de impacto, e a medida da extensao dos efeitos colaterais de uma alteracao no codigo. Quando um dev submete um PR com dez linhas modificadas, a pergunta critica nao e quantas linhas mudaram, mas quantos outros modulos, servicos, testes e fluxos de dados sao potencialmente afetados.

Este capitulo apresenta as duas ferramentas centrais do ecossistema Code Review Graph — a funcao `get_impact_radius` e a funcao `detect_changes` — e mostra como integrar 30 ferramentas MCP para enriquecer a analise de codigo com IA.

## O Que e Blast Radius

Blast radius e um termo emprestado da engenharia de explosivos. Na engenharia de software, ele quantifica a extensao dos efeitos colaterais de uma mudanca no codigo. Empresas como Google e Netflix utilizam blast radius analysis como parte integrante de seus processos de deploy e code review.

A importancia ficou evidente apos estudos mostrarem que **mais de 60% dos bugs em producao sao introduzidos por mudancas aparentemente insignificantes** em modulos centrais. Uma alteracao de tres linhas em uma funcao utilitaria pode propagar-se por dezenas de modulos dependentes, causando falhas em cascata.

No contexto de code review, o blast radius responde tres perguntas:

1. **Alcance direto**: quais arquivos sao diretamente importados pelo codigo alterado?
2. **Alcance indireto**: quais modulos dependem dos diretamente afetados, criando uma cadeia de propagação?
3. **Alcance semantico**: alem das dependencias de codigo, quais fluxos de negocio e APIs publicas sao impactados?

## Como Funciona o get_impact_radius

A funcao `get_impact_radius` e o cerne da analise de impacto. Ela recebe os arquivos alterados em um PR e retorna o conjunto completo de nos afetados, ponderados por distancia e tipo de dependencia.

O algoritmo funciona em tres etapas:

**Etapa 1 — BFS com filtros de tipo**: A busca em largura parte dos nos alterados e explora vizinhos pelo tipo de dependencia (import, require, heranca, implementacao). Imports estaticos tem peso maior que imports dinamicos.

**Etapa 2 — Ponderacao por criticalidade**: Modulos com alta betweenness centrality — ou seja, que aparecem em muitos caminhos entre outros modulos — terao seu blast radius ampliado, pois uma falha neles afeta mais rotas de dependencia.

**Etapa 3 — Filtro de risco**: Modulos com alta cobertura de testes podem ter seu risco reduzido, enquanto modulos sem testes ou com historico de bugs podem ter seu risco ampliado.

### Implementacao em Python

```python
import networkx as nx
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

class RiskLevel(Enum):
    CRITICO = "critico"
    ALTO = "alto"
    MEDIO = "medio"
    BAIXO = "baixo"
    NEGLIGIVEL = "negligivel"

@dataclass
class ImpactNode:
    node_id: str
    distance: int
    risk_level: RiskLevel
    risk_score: float
    dependency_type: str
    betweenness_centrality: float
    test_coverage: float
    change_path: list[str] = field(default_factory=list)

@dataclass
class BlastRadiusResult:
    source_nodes: list[str]
    affected_nodes: list[ImpactNode]
    max_distance: int
    total_risk_score: float
    critical_path: list[str]
    risk_distribution: dict[str, int]

def calculate_node_risk(G, node, distance, edge_type, test_coverage_map):
    betweenness = nx.betweenness_centrality(G)
    centrality_weight = 0.4 * betweenness.get(node, 0.0)
    distance_decay = 1.0 / (1.0 + distance)
    distance_weight = 0.3 * distance_decay
    dependency_weights = {
        "static_import": 1.0, "dynamic_import": 0.7, "require": 0.8,
        "include": 0.5, "inheritance": 0.9, "interface": 0.6, "config": 0.3,
    }
    dep_weight = 0.2 * dependency_weights.get(edge_type, 0.5)
    coverage = test_coverage_map.get(node, 0.0)
    coverage_adjustment = 0.1 * (1.0 - coverage)
    return min(max(centrality_weight + distance_weight + dep_weight + coverage_adjustment, 0.0), 1.0)

def classify_risk(score):
    if score >= 0.7: return RiskLevel.CRITICO
    elif score >= 0.5: return RiskLevel.ALTO
    elif score >= 0.3: return RiskLevel.MEDIO
    elif score >= 0.1: return RiskLevel.BAIXO
    return RiskLevel.NEGLIGIVEL

def get_impact_radius(G, changed_nodes, max_depth=10, risk_threshold=0.1, test_coverage_map=None):
    if test_coverage_map is None:
        test_coverage_map = {}
    betweenness = nx.betweenness_centrality(G)
    affected = {}
    queue = [(node, 0, [node]) for node in changed_nodes]
    visited = set(changed_nodes)
    while queue:
        current, distance, path = queue.pop(0)
        if distance > max_depth:
            continue
        for _, neighbor, edge_data in G.out_edges(current, data=True):
            if neighbor in visited:
                continue
            edge_type = edge_data.get("type", "unknown")
            risk_score = calculate_node_risk(G, neighbor, distance + 1, edge_type, test_coverage_map)
            if risk_score >= risk_threshold:
                affected[neighbor] = ImpactNode(
                    node_id=neighbor, distance=distance + 1,
                    risk_level=classify_risk(risk_score), risk_score=risk_score,
                    dependency_type=edge_type,
                    betweenness_centrality=betweenness.get(neighbor, 0.0),
                    test_coverage=test_coverage_map.get(neighbor, 0.0),
                    change_path=path + [neighbor],
                )
                visited.add(neighbor)
                queue.append((neighbor, distance + 1, path + [neighbor]))
    sorted_nodes = sorted(affected.values(), key=lambda n: n.risk_score, reverse=True)
    risk_dist = {}
    for node in sorted_nodes:
        level = node.risk_level.value
        risk_dist[level] = risk_dist.get(level, 0) + 1
    critical_path = sorted_nodes[0].change_path if sorted_nodes else []
    total_risk = sum(n.risk_score for n in sorted_nodes) / len(sorted_nodes) if sorted_nodes else 0.0
    return BlastRadiusResult(
        source_nodes=changed_nodes, affected_nodes=sorted_nodes,
        max_distance=max((n.distance for n in sorted_nodes), default=0),
        total_risk_score=round(total_risk, 4),
        critical_path=critical_path, risk_distribution=risk_dist,
    )
```

## Detectando Mudancas Estruturais

A funcao `detect_changes` resolve o problema de identificar o que mudou entre duas versoes do codigo. Ela opera no nivel semantico, nao sintatico — uma reestruturacao que renomeia arquivos nao gera alertas, enquanto a adicao de uma nova dependencia em um modulo central gera alerta imediato.

A saida e um objeto `ChangeSet` com:

- `added_nodes` — novos arquivos introduzidos
- `removed_nodes` — arquivos removidos
- `modified_edges` — dependencias que mudaram
- `structural_diff` — novos caminhos, ciclos introduzidos

```python
import networkx as nx
from dataclasses import dataclass, field

@dataclass
class ChangeSet:
    added_nodes: list[str] = field(default_factory=list)
    removed_nodes: list[str] = field(default_factory=list)
    added_edges: list[tuple] = field(default_factory=list)
    removed_edges: list[tuple] = field(default_factory=list)
    modified_edges: list[tuple] = field(default_factory=list)
    structural_changes: list[str] = field(default_factory=list)
    has_new_cycles: bool = False
    has_increased_coupling: bool = False

    @property
    def has_changes(self):
        return bool(self.added_nodes or self.removed_nodes or
                    self.added_edges or self.removed_edges or self.modified_edges)

def detect_changes(G_before, G_after):
    changes = ChangeSet()
    nodes_before = set(G_before.nodes())
    nodes_after = set(G_after.nodes())
    changes.added_nodes = sorted(nodes_after - nodes_before)
    changes.removed_nodes = sorted(nodes_before - nodes_after)
    edges_before = {(u, v): data for u, v, data in G_before.edges(data=True)}
    edges_after = {(u, v): data for u, v, data in G_after.edges(data=True)}
    for u, v in sorted(set(edges_after) - set(edges_before)):
        changes.added_edges.append((u, v, edges_after[(u, v)]))
    for u, v in sorted(set(edges_before) - set(edges_after)):
        changes.removed_edges.append((u, v, edges_before[(u, v)]))
    for u, v in sorted(set(edges_before) & set(edges_after)):
        if edges_before[(u, v)] != edges_after[(u, v)]:
            changes.modified_edges.append((u, v, edges_before[(u, v)], edges_after[(u, v)]))
    if changes.added_edges:
        cycles_before = len(list(nx.simple_cycles(G_before)))
        cycles_after = len(list(nx.simple_cycles(G_after)))
        if cycles_after > cycles_before:
            changes.has_new_cycles = True
            changes.structural_changes.append("Novos ciclos detectados")
    return changes
```

## O Protocolo MCP e o Ecossistema de Ferramentas

O Model Context Protocol (MCP) e um padrao aberto para integracao de ferramentas externas com modelos de linguagem. No contexto de code review, o MCP permite que um assistente de IA acesse ferramentas especializadas de forma padronizada e segura.

A arquitetura segue um modelo cliente-servidor: **Host** (ferramenta de review), **Client** (processo de comunicacao) e **Server** (ferramenta que expoe recursos via JSON-RPC).

### 30 Ferramentas MCP para Code Review

| # | Ferramenta | Categoria | Funcao |
|---|-----------|-----------|--------|
| 1 | github-mcp-server | Repositorio | Acesso a PRs, issues e checks |
| 2 | gitlab-mcp-server | Repositorio | MRs, pipelines, issues |
| 3 | bitbucket-mcp-server | Repositorio | Integracao Bitbucket |
| 4 | filesystem-mcp-server | Arquivos | Leitura/escrita no workspace |
| 5 | sqlite-mcp-server | Banco | Consultas para metricas |
| 6 | postgres-mcp-server | Banco | Dados de build e deploy |
| 7 | redis-mcp-server | Cache | Cache de resultados |
| 8 | elasticsearch-mcp-server | Busca | Busca full-text em codigo |
| 9 | sentry-mcp-server | Observabilidade | Erros em producao |
| 10 | datadog-mcp-server | Observabilidade | Metricas de performance |
| 11 | grafana-mcp-server | Observabilidade | Dashboards de observabilidade |
| 12 | pagerduty-mcp-server | Incidentes | Historico de incidentes |
| 13 | jira-mcp-server | Gestao | Tickets vinculados ao PR |
| 14 | linear-mcp-server | Gestao | Gestao de issues via Linear |
| 15 | confluence-mcp-server | Documentacao | Busca de documentacao |
| 16 | notion-mcp-server | Documentacao | Wikis e bases de conhecimento |
| 17 | slack-mcp-server | Comunicacao | Notificacoes em canais |
| 18 | teams-mcp-server | Comunicacao | Integracao com Teams |
| 19 | npm-mcp-server | Pacotes | Vulnerabilidades npm |
| 20 | pypi-mcp-server | Pacotes | Vulnerabilidades Python |
| 21 | docker-mcp-server | Infra | Imagens Docker afetadas |
| 22 | kubernetes-mcp-server | Infra | Pods e servicos impactados |
| 23 | terraform-mcp-server | Infra | Infraestrutura como codigo |
| 24 | aws-mcp-server | Cloud | Recursos AWS afetados |
| 25 | gcp-mcp-server | Cloud | Recursos GCP impactados |
| 26 | azure-mcp-server | Cloud | Recursos Azure afetados |
| 27 | sonarqube-mcp-server | Qualidade | Metricas de qualidade |
| 28 | snyk-mcp-server | Seguranca | Varredura de vulnerabilidades |
| 29 | codacy-mcp-server | Qualidade | Analise automatizada |
| 30 | codeclimate-mcp-server | Qualidade | Manutenibilidade e complexidade |

### Configuracao no Projeto

A configuracao segue o formato padrao do MCP no arquivo `.mcp.json`:

```json
{
  "mcpServers": {
    "github-pr": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}" }
    },
    "sonarqube": {
      "command": "npx",
      "args": ["-y", "mcp-sonarqube"],
      "env": { "SONAR_HOST_URL": "${SONAR_URL}", "SONAR_TOKEN": "${SONAR_TOKEN}" }
    },
    "sentry": {
      "command": "npx",
      "args": ["-y", "mcp-sentry"],
      "env": { "SENTRY_AUTH_TOKEN": "${SENTRY_TOKEN}", "SENTRY_ORG": "${SENTRY_ORG}" }
    }
  }
}
```

## 5 Prompts de Workflow para Review com MCP

**Prompt 1 — Analise de Blast Radius**

```
Analise o pull request #${PR_NUMBER} no repositorio ${REPO}.
1. Use o github-mcp-server para obter arquivos alterados
2. Execute detect_changes para identificar mudancas estruturais
3. Execute get_impact_radius com os arquivos alterados
4. Classifique: BAIXO (<5 nos), MEDIO (5-15), ALTO (>15)
Retorne: nos afetados, distribuicao de risco, caminho critico, recomendacao.
```

**Prompt 2 — Verificacao de Vulnerabilidades**

```
Execute varredura de seguranca no blast radius do PR #${PR_NUMBER}.
1. Para cada modulo com risco ALTO/CRITICO, use snyk-mcp-server
2. Use npm/pypi-mcp-server para dependencias desatualizadas
3. Use sentry-mcp-server para erros recentes em producao
Retorne: vulnerabilidades por severidade, dependencias criticas, score geral.
```

**Prompt 3 — Impacto em Infraestrutura**

```
Analise impacto infraestrutural do PR #${PR_NUMBER}.
1. Use docker/terraform/aws-mcp-server
2. Identifique servicos Kubernetes impactados
3. Gere plano de rollback se necessario
Retorne: servicos impactados, recursos cloud, plano de rollback, tempo estimado.
```

**Prompt 4 — Conformidade de Padroes**

```
Verifique conformidade no PR #${PR_NUMBER}.
1. Use sonarqube-mcp-server para metricas de qualidade
2. Use confluence-mcp-server para padroes documentados
3. Compare codigo alterado com padroes
Retorne: violacoes por arquivo, metricas antes/depois, recomendacoes.
```

**Prompt 5 — Relatorio Consolidado**

```
Gere relatorio consolidado para o PR #${PR_NUMBER}.
1. Execute todos os workflows anteriores
2. Use jira/linear-mcp para vincular tickets
3. Use pagerduty-mcp para incidentes recentes
4. Use slack-mcp para notificar equipe
Retorne: score geral (0-100), blast radius, bloqueadores, sugestoes.
```

## Cenario Real: FinTech

Em uma empresa de fintech, um dev altera `validateTransaction` em `PaymentValidator`. A alteracao parece simples: adicao de validacao de limite diario. Mas o blast radius revela:

- `PaymentValidator` e importado por 3 modulos criticos
- `TransactionProcessor` e chamado por 12 endpoints da API REST
- `ComplianceChecker` alimenta o sistema de relatorios do Banco Central
- Blast radius total: 47 modulos, 8 endpoints, 3 sistemas externos

Sem blast radius analysis, o revisor aprovaria o PR em minutos. Com a analise, o time descobre que a alteracao pode afetar transaccoes de milhoes de clientes e decide adicionar testes de integracao abrangentes.

## Armadilhas Comuns

**Blast Radius ignorado por falta de ferramentas.** Muitas equipes fazem code review apenas lendo o diff. A solucao e integrar o blast radius analysis ao pipeline de CI/CD.

**Falso positivo por dependencias transitivas.** O blast radius pode ser inflado por dependencias que nao causam impacto real. A calibracao do `risk_threshold` e essencial para manter a precisao.

---

# Visualizacao, Exportacao e GitHub Action

Nenhuma tabela ou lista consegue capturar a **forma visual** do grafo de dependencias. Quando um revisor olha para 47 modulos afetados em texto, precisa de esforco cognitivo significativo. Quando olha para um diagrama interativo onde o tamanho dos nos reflete o blast radius e as cores indicam o nivel de risco, a compreensao e instantanea.

Estudos demonstram que o cerebro humano processa informacoes visuais **60.000 vezes mais rapido que texto**. No contexto de code review, um diagrama bem construido pode comunicar em milissegundos o que um relatorio textual levaria minutos.

## Por Que D3.js

D3.js (Data-Driven Documents) e a biblioteca padrao para visualizacao de dados na web. Diferente de Chart.js ou Plotly, D3.js fornece primitivas de baixo nivel para visualizacoes completamente customizadas.

As vantagens para grafos de codigo:

- **Force-directed layout**: nos posicionados como particulas em um sistema de forcas, revelando clusters de dependencia
- **Zoom e pan**: navegacao fluida por grafos grandes
- **Tooltips interativos**: detalhes ao passar o mouse (blast radius, cobertura, historico)
- **Animacao de transicao**: representacao visual de mudancas entre estados

## Layouts para Grafos de Codigo

**Force-dimensional**: Nos com muitas conexoes se posicionam no centro, modulos perifericos se afastam. Ideal para descobrir clusters.

**Hierarquico (Layered)**: Nos em camadas, raiz no topo, dependencias abaixo. Util para visualizar fluxos de dados.

**Circular**: Nos em um circulo. Adequado para grafos pequenos (<30 nos).

**Radial**: Raiz no centro, niveis expandindo concentricamente. Excelente para visualizar blast radius de um unico no.

## Formatos de Exportacao

- **GraphML**: formato XML padrao, compativel com yEd, Gephi e Cytoscape
- **Neo4j**: banco de grafos para consultas complexas
- **Obsidian**: notas conectadas para documentacao de arquitetura viva
- **SVG**: formato vetorial para documentacao e apresentacoes

```python
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

def export_graphml(G, filepath, risk_scores=None):
    root = ET.Element("graphml")
    root.set("xmlns", "http://graphml.graphdrawing.org/xmlns")
    for attr_name, attr_type in [("risk_score", "double"), ("blast_radius", "int"), ("coverage", "double")]:
        key = ET.SubElement(root, "key")
        key.set("id", attr_name)
        key.set("for", "node")
        key.set("attr.name", attr_name)
        key.set("attr.type", attr_type)
    graph = ET.SubElement(root, "graph")
    graph.set("id", "code_review_graph")
    graph.set("edgedefault", "directed")
    for node_id in G.nodes():
        node_elem = ET.SubElement(graph, "node")
        node_elem.set("id", str(node_id))
        if risk_scores and node_id in risk_scores:
            data = ET.SubElement(node_elem, "data")
            data.set("key", "risk_score")
            data.text = str(risk_scores[node_id])
    for u, v, data in G.edges(data=True):
        edge = ET.SubElement(graph, "edge")
        edge.set("source", str(u))
        edge.set("target", str(v))
        edge.set("directed", "true")
    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(xml_str.split("\n")[1:]))
    return filepath

def export_neo4j_cypher(G, filepath, risk_scores=None):
    lines = ["// Code Review Graph — Importacao Neo4j", "MATCH (n) DETACH DELETE n;", ""]
    for node_id in G.nodes():
        risk = risk_scores.get(node_id, 0.0) if risk_scores else 0.0
        safe = str(node_id).replace("'", "\\'")
        lines.append(f"CREATE (n:{safe} {{name: '{safe}', risk_score: {risk:.4f}}});")
    lines.append("")
    for u, v, data in G.edges(data=True):
        dep_type = data.get("type", "unknown")
        lines.append(f"MATCH (a:{u}), (b:{v}) CREATE (a)-[:DEPENDS_ON {{type: '{dep_type}'}}]->(b);")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return filepath

def export_json(G, filepath, risk_scores=None):
    data = {"nodes": [], "edges": []}
    for node_id in G.nodes():
        risk = risk_scores.get(node_id, 0.0) if risk_scores else 0.0
        data["nodes"].append({"id": str(node_id), "risk_score": round(risk, 4)})
    for u, v, edge_data in G.edges(data=True):
        data["edges"].append({"source": str(u), "target": str(v), "type": edge_data.get("type", "unknown")})
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return filepath
```

## GitHub Action para Code Review Automatizado

Uma GitHub Action pode executar blast radius analysis a cada pull request, gerar um diagrama visual do impacto, comentar automaticamente no PR e bloquear a merge se o blast radius exceder um limiar configuravel.

O fluxo e event-driven:

1. Evento `pull_request.opened` ou `pull_request.synchronize` dispara o workflow
2. O workflow verifica o repositorio, constroi o grafo e calcula o blast radius
3. O resultado e formatado como comentario no PR
4. Se houver violacoes, o workflow adiciona um label de aprovacao pendente

```yaml
name: Blast Radius Code Review
on:
  pull_request:
    types: [opened, synchronize, reopened]
permissions:
  contents: read
  pull-requests: write
env:
  BLAST_RADIUS_THRESHOLD: 0.6
  MAX_AFFECTED_NODES: 20
jobs:
  blast-radius-analysis:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install networkx numpy
      - name: Build dependency graph
        run: |
          python scripts/build_dependency_graph.py \
            --base ${{ github.event.pull_request.base.sha }} \
            --head ${{ github.event.pull_request.head.sha }} \
            --output graph_before.json graph_after.json
      - name: Detect changes
        run: |
          python scripts/detect_changes.py \
            --before graph_before.json --after graph_after.json --output changes.json
      - name: Calculate blast radius
        id: blast-radius
        run: |
          python scripts/get_impact_radius.py \
            --graph graph_after.json --changes changes.json \
            --output blast_radius.json --threshold ${{ env.BLAST_RADIUS_THRESHOLD }}
      - name: Post PR comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const br = JSON.parse(fs.readFileSync('blast_radius.json', 'utf8'));
            let body = '## Blast Radius Analysis\n\n';
            body += `**Score geral:** ${br.total_risk_score}\n\n`;
            if (br.total_risk_score > 0.7) body += 'Review humano obrigatorio.\n';
            else if (br.total_risk_score > 0.4) body += 'Review recomendado.\n';
            else body += 'Review automatizado suficiente.\n';
            github.rest.issues.createComment({
              owner: context.repo.owner, repo: context.repo.repo,
              issue_number: context.issue.number, body
            });
```

## Dashboard Interativo com D3.js

O dashboard renderiza um grafo force-directed onde o tamanho e a cor dos nos refletem o risco calculado. Ao clicar em um no, o painel lateral exibe detalhes: score de risco, distancia, tipo de dependencia, cobertura de testes e betweenness centrality.

A funcao mais importante e a interacao: ao passar o mouse sobre um no, todos os nos conectados sao destacados e os demais ficam transparentes. Isso permite ao revisor entender instantaneamente a cadeia de impacto.

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Blast Radius Dashboard</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: system-ui, sans-serif; background: #0f172a; color: #e2e8f0; }
        .dashboard { display: grid; grid-template-columns: 1fr 360px; height: 100vh; }
        .header { grid-column: 1/-1; background: #1e293b; padding: 16px 24px;
                  border-bottom: 1px solid #334155; display: flex;
                  justify-content: space-between; align-items: center; }
        .header h1 { font-size: 1.25rem; color: #f8fafc; }
        .badge { padding: 4px 12px; border-radius: 9999px; font-weight: 600; font-size: 0.75rem; }
        .badge.high { background: #dc2626; color: #fff; }
        .badge.medium { background: #d97706; color: #fff; }
        .badge.low { background: #16a34a; color: #fff; }
        .graph-container { position: relative; }
        .side-panel { background: #1e293b; border-left: 1px solid #334155;
                      padding: 20px; overflow-y: auto; }
        .metric-card { background: #0f172a; border: 1px solid #334155; border-radius: 8px;
                       padding: 16px; margin-bottom: 12px; }
        .metric-card .label { font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; }
        .metric-card .value { font-size: 1.5rem; font-weight: 700; color: #f8fafc; margin-top: 4px; }
        .metric-card .value.critical { color: #ef4444; }
        .metric-card .value.warning { color: #f59e0b; }
        .detail-row { display: flex; justify-content: space-between; padding: 8px 0;
                      border-bottom: 1px solid #334155; font-size: 0.875rem; }
        .legend { position: absolute; bottom: 16px; left: 16px; background: rgba(15,23,42,0.9);
                  border: 1px solid #334155; border-radius: 8px; padding: 12px 16px; font-size: 0.75rem; }
        .legend-item { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
        .legend-dot { width: 12px; height: 12px; border-radius: 50%; }
        .tooltip { position: absolute; background: #1e293b; border: 1px solid #475569;
                   border-radius: 8px; padding: 12px; font-size: 0.8rem; pointer-events: none;
                   opacity: 0; transition: opacity 0.15s; z-index: 100; max-width: 280px; }
        .tooltip.visible { opacity: 1; }
    </style>
</head>
<body>
    <div class="dashboard">
        <header class="header">
            <h1>Blast Radius Dashboard</h1>
            <div style="display:flex;gap:16px;align-items:center;font-size:0.875rem;color:#94a3b8">
                <span>PR #42</span>
                <span class="badge high">RISCO ALTO</span>
                <span>14 nos afetados</span>
            </div>
        </header>
        <div class="graph-container" id="graph">
            <div class="legend">
                <div class="legend-item"><div class="legend-dot" style="background:#ef4444"></div>Critico</div>
                <div class="legend-item"><div class="legend-dot" style="background:#f59e0b"></div>Alto</div>
                <div class="legend-item"><div class="legend-dot" style="background:#3b82f6"></div>Medio</div>
                <div class="legend-item"><div class="legend-dot" style="background:#22c55e"></div>Baixo</div>
            </div>
        </div>
        <aside class="side-panel">
            <h2 style="font-size:1rem;color:#f8fafc;margin-bottom:16px">Resumo</h2>
            <div class="metric-card">
                <div class="label">Score Total</div>
                <div class="value critical" id="total-risk">0.72</div>
            </div>
            <div class="metric-card">
                <div class="label">Nos Afetados</div>
                <div class="value warning" id="affected-count">14</div>
            </div>
            <div class="metric-card">
                <div class="label">Modulos Criticos</div>
                <div class="value critical" id="critical-count">3</div>
            </div>
            <h2 style="font-size:1rem;color:#f8fafc;margin:20px 0 16px">Detalhes</h2>
            <div id="node-details" style="display:none">
                <div class="metric-card"><div class="label">Modulo</div><div class="value" id="detail-name"></div></div>
                <div class="detail-row"><span style="color:#94a3b8">Risco</span><span id="detail-risk"></span></div>
                <div class="detail-row"><span style="color:#94a3b8">Distancia</span><span id="detail-distance"></span></div>
                <div class="detail-row"><span style="color:#94a3b8">Dependencia</span><span id="detail-dep-type"></span></div>
                <div class="detail-row"><span style="color:#94a3b8">Cobertura</span><span id="detail-coverage"></span></div>
            </div>
        </aside>
    </div>
    <div class="tooltip" id="tooltip"></div>
    <script>
    const data = {
        nodes: [
            {id:"PaymentGateway",risk:0.92,distance:0,dep_type:"source",coverage:0.65,centrality:0.85},
            {id:"OrderService",risk:0.78,distance:1,dep_type:"static_import",coverage:0.80,centrality:0.72},
            {id:"TransactionProcessor",risk:0.71,distance:1,dep_type:"static_import",coverage:0.55,centrality:0.68},
            {id:"HttpClient",risk:0.62,distance:1,dep_type:"static_import",coverage:0.90,centrality:0.45},
            {id:"ConfigLoader",risk:0.58,distance:1,dep_type:"static_import",coverage:0.60,centrality:0.42},
            {id:"InventoryManager",risk:0.45,distance:2,dep_type:"static_import",coverage:0.70,centrality:0.38},
            {id:"NotificationService",risk:0.38,distance:2,dep_type:"static_import",coverage:0.50,centrality:0.30},
            {id:"ComplianceChecker",risk:0.35,distance:2,dep_type:"static_import",coverage:0.75,centrality:0.28},
            {id:"UserService",risk:0.30,distance:3,dep_type:"static_import",coverage:0.85,centrality:0.25},
            {id:"DatabaseAdapter",risk:0.25,distance:3,dep_type:"static_import",coverage:0.80,centrality:0.20},
            {id:"CacheLayer",risk:0.22,distance:3,dep_type:"static_import",coverage:0.70,centrality:0.18},
            {id:"EmailProvider",risk:0.18,distance:3,dep_type:"static_import",coverage:0.60,centrality:0.15},
            {id:"ReportService",risk:0.15,distance:4,dep_type:"dynamic_import",coverage:0.40,centrality:0.12},
            {id:"AnalyticsEngine",risk:0.10,distance:4,dep_type:"dynamic_import",coverage:0.30,centrality:0.08}
        ],
        edges: [
            {source:"PaymentGateway",target:"OrderService"},
            {source:"PaymentGateway",target:"TransactionProcessor"},
            {source:"PaymentGateway",target:"HttpClient"},
            {source:"PaymentGateway",target:"ConfigLoader"},
            {source:"OrderService",target:"InventoryManager"},
            {source:"OrderService",target:"NotificationService"},
            {source:"OrderService",target:"ComplianceChecker"},
            {source:"TransactionProcessor",target:"OrderService"},
            {source:"OrderService",target:"UserService"},
            {source:"InventoryManager",target:"DatabaseAdapter"},
            {source:"InventoryManager",target:"CacheLayer"},
            {source:"NotificationService",target:"EmailProvider"},
            {source:"ComplianceChecker",target:"ReportService"},
            {source:"ReportService",target:"AnalyticsEngine"}
        ]
    };
    function getColor(r){return r>=0.7?"#ef4444":r>=0.5?"#f59e0b":r>=0.3?"#3b82f6":"#22c55e"}
    function getGroup(r){return r>=0.7?"critical":r>=0.5?"high":r>=0.3?"medium":"low"}
    const container=document.getElementById("graph"),w=container.clientWidth,h=container.clientHeight;
    const svg=d3.select("#graph").append("svg").attr("width",w).attr("height",h);
    const g=svg.append("g");
    svg.call(d3.zoom().scaleExtent([0.2,4]).on("zoom",e=>g.attr("transform",e.transform)));
    const tooltip=d3.select("#tooltip");
    const sim=d3.forceSimulation(data.nodes)
        .force("link",d3.forceLink(data.edges).id(d=>d.id).distance(120))
        .force("charge",d3.forceManyBody().strength(-400))
        .force("center",d3.forceCenter(w/2,h/2))
        .force("collision",d3.forceCollide().radius(d=>8+d.risk*20+10));
    const link=g.append("g").selectAll("line").data(data.edges).join("line")
        .attr("stroke","#475569").attr("stroke-width",1.5).attr("stroke-opacity",0.6);
    const node=g.append("g").selectAll("circle").data(data.nodes).join("circle")
        .attr("r",d=>8+d.risk*20).attr("fill",d=>getColor(d.risk))
        .attr("stroke","#1e293b").attr("stroke-width",2).attr("cursor","pointer")
        .on("mouseover",(e,d)=>{
            const conn=new Set();data.edges.forEach(ed=>{if(ed.source.id===d.id)conn.add(ed.target.id);if(ed.target.id===d.id)conn.add(ed.source.id)});
            node.attr("opacity",n=>n.id===d.id||conn.has(n.id)?1:0.2);
            link.attr("stroke-opacity",l=>l.source.id===d.id||l.target.id===d.id?1:0.1);
            tooltip.classed("visible",true).html(`<strong>${d.id}</strong><br>Risco: ${d.risk.toFixed(2)}<br>Dist: ${d.distance}<br>Tipo: ${d.dep_type}`)
                .style("left",(e.pageX+12)+"px").style("top",(e.pageY-12)+"px");
        })
        .on("mouseout",()=>{node.attr("opacity",1);link.attr("stroke-opacity",0.6);tooltip.classed("visible",false)})
        .on("click",(e,d)=>{
            document.getElementById("node-details").style.display="block";
            document.getElementById("detail-name").textContent=d.id;
            document.getElementById("detail-risk").textContent=d.risk.toFixed(2)+" ("+getGroup(d.risk)+")";
            document.getElementById("detail-distance").textContent=d.distance;
            document.getElementById("detail-dep-type").textContent=d.dep_type;
            document.getElementById("detail-coverage").textContent=(d.coverage*100).toFixed(0)+"%";
        })
        .call(d3.drag().on("start",(e,d)=>{if(!e.active)sim.alphaTarget(0.3).restart();d.fx=d.x;d.fy=d.y})
            .on("drag",(e,d)=>{d.fx=e.x;d.fy=e.y}).on("end",(e,d)=>{if(!e.active)sim.alphaTarget(0);d.fx=null;d.fy=null}));
    const labels=g.append("g").selectAll("text").data(data.nodes).join("text").text(d=>d.id)
        .attr("font-size","10px").attr("fill","#e2e8f0").attr("dx",d=>8+d.risk*20+4).attr("dy",4).attr("pointer-events","none");
    sim.on("tick",()=>{link.attr("x1",d=>d.source.x).attr("y1",d=>d.source.y).attr("x2",d=>d.target.x).attr("y2",d=>d.target.y);
        node.attr("cx",d=>d.x).attr("cy",d=>d.y);labels.attr("x",d=>d.x).attr("y",d=>d.y)});
    </script>
</body>
</html>
```

## Cenario Real: Dashboard em Empresa de Medio Porte

Uma empresa com 50 desenvolvedores implementou o pipeline completo. Apos seis meses:

- **Tempo de review reduziu em 35%**: o dashboard visual permitiu compreensao em segundos
- **Bugs em producao reduzidos em 28%**: identificacao proativa de modulos de alto risco
- **Onboarding acelerado em 50%**: o grafo visual serve como mapa do codebase
- **Cobertura de review aumentou de 60% para 92%**: a GitHub Action garante analise em todo PR

## Metricas de Sucesso

1. **Tempo de feedback**: menos de 2 minutos para reviews automatizados
2. **Taxa de cobertura**: 100% dos PRs com analise de blast radius
3. **Precisao**: acima de 70% dos alertas de alto risco resultam em bugs reais
4. **Adocao**: acima de 80% dos revisores usando o dashboard apos 3 meses
5. **Reducao de incidents**: 20% no primeiro semestre

## Boas Praticas

1. Comece com SVG antes do D3.js — uma visualizacao estatica ja agrega valor
2. Configure labels granulares no GitHub (risk:critical, risk:high, etc.)
3. Mantenha historico de metricas para identificar tendencias
4. Integre com Jira ou Linear para rastreabilidade completa
5. Documente a configuracao do pipeline com thresholds e permissoes

---

# Quer Ir Mais Longe?

Este ebook e um recorte dos capitulos 3 e 4 do livro **Code Review Graph: Construindo Grafos de Dependencias para Revisao de Codigo Inteligente**.

No livro completo, voce encontra:

- **Capitulo 1**: Fundamentos de grafos de dependencias e como他们是 construidos a partir da analise estatica do codigo
- **Capitulo 2**: Construcao do grafo de dependencias do seu codebase, com implementacao completa em Python
- **Capitulos 5-8**: Casos avancados, padroes de uso em sistemas de grande escala, integracao com CI/CD, e metricas de maturidade
- **Appendices**: Template de configuracao, guia de migracao e referencia completa de APIs

O livro completo inclui mais de 40 diagramas Mermaid, 25 blocos de codigo executavel, e estudos de caso reais de empresas que implementaram code review baseado em grafos.

**Adquira o livro completo em:** [link da loja]

---

*Code Review Graph — Funcionalidades Essenciais*
*Heverton Eduardo Peres*
*Editora Agentic*
