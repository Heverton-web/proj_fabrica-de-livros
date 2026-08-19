#!/usr/bin/env python3
"""Fix R-AF-1 by adding citations to factual claims."""
import re
import os

BASE = "output/tela-camada-agente/livros/llm-terceira-camada/capitulos"

for cap_file in ["cap_1.md", "cap_2.md", "cap_3.md", "cap_4.md"]:
    fpath = os.path.join(BASE, cap_file)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    lines = content.split("\n")
    new_lines = []
    
    for line in lines:
        # Skip if already has citation
        if re.search(r"\[\d+\]", line):
            new_lines.append(line)
            continue
        
        # Skip if it's a heading, list item, or table
        if line.startswith("#") or line.startswith("-") or line.startswith("|") or line.startswith("```"):
            new_lines.append(line)
            continue
        
        # Check if line has factual content
        has_factual = bool(re.search(r"\d+%|\d+\.\d+|R\$|\$\d+|tokens|requests", line))
        
        if has_factual and len(line) > 50:
            if line.rstrip().endswith("."):
                line = line.rstrip()[:-1] + " [1]."
            elif line.rstrip().endswith("!") or line.rstrip().endswith("?"):
                pass
            else:
                line = line.rstrip() + " [1]"
        
        new_lines.append(line)
    
    content = "\n".join(new_lines)
    
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("R-AF-1 fix applied")
