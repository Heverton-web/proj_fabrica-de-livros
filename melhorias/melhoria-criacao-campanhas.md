# Plano de Melhoria: Criação de Campanhas (Baseado em Martha Gabriel)

Este plano descreve como reestruturar a fase de "Criação de Campanhas" (`/campanha` e `/campanha-completa`) do projeto **fabrica-de-livros** para alinhar-se com as melhores práticas descritas em *Marketing na Era Digital* (Martha Gabriel & Rafael Kiso) e o *Playbook Estratégico* recentemente gerado.

> [!IMPORTANT]  
> Conforme solicitado, isto é um **Plano de Melhoria** que visa repensar a arquitetura atual sem modificar a lógica operacional agora. 

## 1. Visão Geral da Melhoria

Atualmente (conforme `AGENTS.md` V5.3), a geração de campanhas cria artefatos genéricos ou os agrupa de forma simplificada em `output/<colecao>/campanhas/`. A melhoria fundamental é criar um **ecossistema de mídia própria, ganha e paga (PESO model - Martha Gabriel)** através de um *scaffold* (estrutura de diretórios) robusto e declarativo. 

Isso resolve o problema de cronogramas ricos ("o que, por que, como, quando") ficarem perdidos em texto livre, forçando os agentes a preencherem metadados rastreáveis.

## 2. Nova Estrutura de Pastas (Scaffold da Campanha)

O modelo antigo de arquivos soltos será substituído pelo seguinte padrão em `output/<slug-colecao>/campanhas/<material-slug>/`:

```text
campanhas/<material-slug>/
├── hub_campanha.json           # [NOVO] Manifesto central da campanha (objetivos, persona, links)
├── cronograma_mestre.md        # [MODIFICADO] Visão temporal consolidada do "O Quê/Por Quê/Quando"
├── inbound_emails/             # Fase: Aprofundamento / Relacionamento
│   ├── email-01-boas-vindas.md
│   └── email-02-oferta.md
├── social_organico/            # Fase: Gancho / Awareness (Redes Sociais)
│   ├── post-01-dor.md          # Copy rica (texto)
│   ├── post-01-dor.png         # [Arte Chromium baseada no molde HTML]
│   └── ...
├── ads_pago/                   # [NOVO] Tráfego Pago (Baseado no livro: impulsionamento focado)
│   ├── facebook_ad_01.md       # Molde AIDA (Atenção, Interesse, Desejo, Ação)
│   └── search_ad_01.txt        # Copy para Google Ads (títulos e descrições curtas)
└── distribuicao_semeadura/     # [NOVO] Fóruns, LinkedIn Articles, Grupos (Semear conteúdo)
    └── artigo_linkedin_01.md
```

## 3. Materiais e Formatos Gerados

### A. Manifesto da Campanha (`hub_campanha.json`)
*   **O que é:** O cérebro da campanha. Contém as tags SEO (da metodologia Gabriel), a URL da máquina de vendas e o rastreamento (UTMs).
*   **Formato:** `.json`.
*   **Objetivo:** Permitir que o framework Python da fábrica audite se a campanha tem começo, meio e fim (Fases 0, 1 e 2).

### B. Artefatos de Redes Sociais (`social_organico/*.md` e `*.png`)
*   **O que é:** Combinação de legenda longa educacional e arte visual impactante. 
*   **Formato:** Legendas em `.md` (usando *Markdown* para negritos nas redes que suportam) e artes em `.png` (renderizadas no Chromium via HTML templates).
*   **A Melhoria:** Cada arquivo terá um rótulo indicando a etapa do funil (Gancho, Aprofundamento, CTA), coibindo duplicatas no design.

### C. Réguas de E-mail (`inbound_emails/*.md`)
*   **O que é:** O fluxo de automação para relacionamento aprofundado e nutrição. 
*   **Formato:** `.md` formatado para envio direto via plataformas de automação, contendo marcadores como `[NOME-DO-LEAD]`.
*   **A Melhoria:** A copy não pode ser focada só em venda. O e-mail 01 DEVE trazer valor imediato antes de ofertar, ancorado na teoria de Inbound de Martha Gabriel.

## 4. O Fluxo de Execução Recomendado (Para Implementação Futura)

1.  **Etapa de Planejamento (IA Analítica):** O `estrategista` lê o `sumario_macro` e o `hub_campanha.json` é inicializado com as métricas que deverão ser batidas.
2.  **Etapa de Extração (IA Criativa):** Redatores quebram os *highlights* do livro gerando as *copys* para `social_organico` e `ads_pago`.
3.  **Etapa de Design Automático:** O Chromium interpola os templates HTML e salva as artes `.png`.
4.  **Etapa de Validação (IA Revisora):** Um novo gate R-CP-7 valida se as URLs de destino contêm UTMs válidas mapeando a origem orgânica ou paga, conforme recomendação do livro.
