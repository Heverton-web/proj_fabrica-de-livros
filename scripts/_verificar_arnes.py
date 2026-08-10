# -*- coding: utf-8 -*-
from pathlib import Path
import re

for pasta, nome in [('pbk-1-harness-modelo', 'post-01.html'),
                    ('lm-6-mini-guia', 'post-01.html'),
                    ('harness--eb-01-a-revolucao-dos-agentes-por-que-o-modelo', 'post-01.html')]:
    base = Path('output/harness/campanhas') / pasta / 'redes-sociais/instagram/artes/post'
    f = base / nome
    if not f.exists():
        print(f'--- {pasta}: {nome} NAO EXISTE')
        continue
    html = f.read_text(encoding='utf-8', errors='ignore')
    print(f'--- {pasta}:')
    for m in re.finditer(r'arnês', html):
        ctx = html[max(0, m.start()-60):m.end()+60].replace('\n', ' ')
        print(f'    ...{ctx}...')
        break
    tags = re.findall(r'class="tag">([^<]+)<', html)
    print(f'    TAGS: {tags}')
    # e-books: pasta existe?
    if pasta.startswith('harness--eb'):
        print(f'    htmls: {len(list(Path("output/harness/campanhas") / pasta / "redes-sociais/instagram/artes/post").glob("*.html")) if (Path("output/harness/campanhas") / pasta / "redes-sociais/instagram/artes/post").exists() else 0}')
