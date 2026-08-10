# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, 'scripts')
import campanha as CP

BASE = Path('output')

# mapear pastas reais de campanha -> obra
for pasta in sorted((BASE / 'harness' / 'campanhas').iterdir()):
    if not pasta.is_dir():
        continue
    nome = pasta.name
    # encontrar a obra correspondente: output/harness/<tipo>/<nome>?
    obra = None
    for tipo in ('livros', 'artigos', 'ebooks', 'playbooks', 'lead-magnets', 'decks', 'emails'):
        cand = BASE / 'harness' / tipo / nome
        if (cand / 'config_obra.json').exists():
            obra = f'harness/{tipo}/{nome}'
            break
    if obra:
        try:
            ctx = CP.contexto_material(obra, BASE)
            print(f'{nome:44s} -> obra={obra} tags={ctx.get("tags_arte")}')
        except Exception as exc:  # noqa: BLE001
            print(f'{nome:44s} -> obra={obra} ERRO={exc}')
    else:
        print(f'{nome:44s} -> (sem obra correspondente)')
