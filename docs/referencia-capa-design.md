# Referência: Regra 5 — Identidade Visual da Editora Agêntica

> Este arquivo contém os detalhes completos da REGRA 5 do AGENTS.md.
> O AGENTS.md referencia esta seção mas não a expande, economizando tokens.

## Padrão 2D Plano (Livro e E-book)

As capas DEVEM ser geradas como arte gráfica 2D plana retangular (flat 2D front cover page). PROIBIDO: mockups 3D, bordas de lombada, faixas laterais, sombras, estética "IA 3D neon".

### Especificações

| Elemento | Especificação |
|---|---|
| **Fundo** | Matte Sóbrio #0d1117 (fixo) |
| **Barras** | Accent topo 8px + rodapé 6px |
| **Padding** | 80px lateral mínimo |
| **Chancela** | `>_ EDITORA AGÊNTICA` (topo esquerda, ícone 72x72px borda 3px, glifo >_ 34px, texto 24px letter-spacing 4px) |
| **Ilustração** | Temática central, área fixa, gerada por `subagente-ilustrador` |
| **Título** | Branco #e6edf3, Inter 900 72px, máx. 2 linhas, sem linha de 1 palavra, última palavra em accent |
| **Subtítulo** | Inter 300 18-24px, #8b949e, máx. 2 linhas, sem linha de 1 palavra |
| **Badge Nível** | OBRIGATÓRIO. `iniciante`→"PARA INICIANTES", `intermediario`→"NÍVEL INTERMEDIÁRIO", `avancado`→"NÍVEL AVANÇADO". Cor accent |
| **Divider** | Faixa fina decorativa, cor accent |
| **Autor** | Heverton Eduardo Peres (fixo, Inter 600 30px, #e6edf3) |
| **Qualificação** | "Especialista em Marketing e Desenvolvimento de Soluções" (fixo, Inter 600 16px, cor accent) |
| **Cor Accent** | Por coleção (campo `serie` em `config_obra.json`), persistida em `output/series.json` |
| **Dimensões** | 1200x1600px (ebooks), 1600x2263px (livros A4) |
| **Script** | `scripts/gerar-capa.py --tipo livro\|ebook` (HTML/CSS + Playwright) |
| **Salvar** | `imagens/capa.png` |
| **Validação** | `validar-capa-texto.py` (título/subtítulo) + `validar-capa-nivel.py` (badge). Reprovação BLOQUEIA compilação |

### TCC e Artigo

Usam capa sóbria ABNT própria, fora desta regra.
