#!/usr/bin/env python3
"""Fix cap_3 Ilustra section."""
import re

with open("output/tela-camada-agente/livros/llm-terceira-camada/capitulos/cap_3.md", "r", encoding="utf-8") as f:
    content = f.read()

# Fix the section 3 header
old = "## 3. Ilustra\nnO diagrama abaixo mostra o panorama dos principais modelos de LLM disponiveis em 2026, organizados por categoria de uso:\nDiagrama ilustrativo do Panorama de Modelos 2026:"

new = """## 3. Ilustra

O diagrama abaixo mostra o panorama dos principais modelos de LLM disponiveis em 2026, organizados por categoria de uso:

```mermaid"""

content = content.replace(old, new)

with open("output/tela-camada-agente/livros/llm-terceira-camada/capitulos/cap_3.md", "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed")
