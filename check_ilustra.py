#!/usr/bin/env python3
"""Check Ilustra section for mermaid diagrams."""
import re

RE_CODIGO = re.compile(r'^[ \t]*```.*?^[ \t]*```[ \t]*$', re.DOTALL | re.MULTILINE)
RE_MERMAID = re.compile(r'^[ \t]*```[ \t]*mermaid', re.MULTILINE | re.IGNORECASE)

with open('output/tela-camada-agente/livros/llm-terceira-camada/capitulos/cap_3.md', 'r', encoding='utf-8') as f:
    texto = f.read()

# Mask code blocks
def _mascarar_codigo(m):
    return ''.join('\n' if c == '\n' else ' ' for c in m.group(0))

mascara = RE_CODIGO.sub(_mascarar_codigo, texto)

# Find sections
secoes = {}
marcas = []
for m in re.finditer(r'^##\s*(\d)[\.\)]?\s*(.+)$', mascara, re.MULTILINE):
    marcas.append((int(m.group(1)), m.group(2).strip(), m.start(), m.end()))

for i, (num, titulo, _ini, fim) in enumerate(marcas):
    prox = marcas[i + 1][2] if i + 1 < len(marcas) else len(texto)
    secoes[num] = {'titulo': titulo, 'corpo': texto[fim:prox]}

# Check Ilustra section
secao_ilustra = secoes.get(3, {}).get('corpo', '')
diagramas = RE_MERMAID.findall(secao_ilustra)
print(f'cap_3 Ilustra section body length: {len(secao_ilustra)}')
print(f'Mermaid blocks in Ilustra: {len(diagramas)}')
print(f'First 200 chars of Ilustra body: {secao_ilustra[:200]}')
