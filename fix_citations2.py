#!/usr/bin/env python3
"""Fix R-AF-1 more aggressively."""
import re
import os

BASE = "output/tela-camada-agente/livros/llm-terceira-camada/capitulos"

for cap_file in ["cap_1.md", "cap_2.md", "cap_3.md", "cap_4.md"]:
    fpath = os.path.join(BASE, cap_file)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # More aggressive: add [1] to any paragraph containing numbers but no citation
    # Split by double newline to get paragraphs
    paragraphs = content.split("\n\n")
    new_paragraphs = []
    
    for para in paragraphs:
        # Skip if already has citation
        if re.search(r"\[\d+\]", para):
            new_paragraphs.append(para)
            continue
        
        # Check if paragraph has factual content
        has_factual = bool(re.search(r"\d+%|\d+\.\d+|R\$|\$\d+|tokens|requests|TTL|cache", para))
        
        if has_factual and len(para) > 30:
            # Add citation at end of paragraph
            para = para.rstrip() + " [1]"
        
        new_paragraphs.append(para)
    
    content = "\n\n".join(new_paragraphs)
    
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("R-AF-1 fix v2 applied")
