# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, 'scripts')
import campanha as CP

BASE = Path('output')
for slug in ['harness-engineering/livros/harness-engineering',
             'harness-engineering/artigos/harness-engineering--art-01-a-revolucao-dos-agentes-por-que-o-modelo',
             'harness-engineering/playbooks/pbk-1-harness-engineering-modelo']:
    d = CP.dir_campanha_material(slug, BASE)
    print(f'{slug.split("/")[-1][:30]:32s} -> {d}')
    print(f'    existe: {d.exists()}')

# tags derivadas pelo contexto atual
for slug in ['harness-engineering/livros/harness-engineering',
             'harness-engineering/playbooks/pbk-1-harness-engineering-modelo',
             'harness-engineering/lead-magnets/lm-1-armadilhas']:
    ctx = CP.contexto_material(slug, BASE)
    print(f'tags {slug.split("/")[-1][:24]:26s}: {ctx.get("tags_arte")}')
