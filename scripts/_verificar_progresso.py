# -*- coding: utf-8 -*-
"""Conta artes com tags novas (tecnicas) vs antigas (metafora) por material."""
from pathlib import Path

CAMPANHAS = Path('output/harness/campanhas')
TOTAL_NOVO = 0
TOTAL_META = 0
for pasta in sorted(CAMPANHAS.iterdir()):
    if not pasta.is_dir():
        continue
    htmls = list(pasta.rglob('artes/**/*.html')) + list(pasta.rglob('artes/*.html'))
    novo = sum(1 for h in htmls if 'Sistema Autônomo' in h.read_text(encoding='utf-8', errors='ignore'))
    meta = sum(1 for h in htmls if 'arnês' in h.read_text(encoding='utf-8', errors='ignore'))
    TOTAL_NOVO += novo
    TOTAL_META += meta
    if novo or meta:
        print(f'{pasta.name:44s} novo={novo:3d} meta={meta:3d}')
print(f'=== TOTAIS: novo={TOTAL_NOVO} meta={TOTAL_META} ===')
