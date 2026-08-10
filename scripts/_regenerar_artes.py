# -*- coding: utf-8 -*-
"""Regenera HTML+PNG das artes com tags tecnicas, na ESTRUTURA NOVA da
migracao V5.1 (output/harness/campanhas/<nome>). Bypass de
dir_campanha_material (o campanha.json ainda tem slugs antigos que nao
resolvem). Aceita filtro por nome de pasta: python _regenerar_artes.py harness
"""
import sys
from pathlib import Path
import importlib.util

sys.path.insert(0, 'scripts')
import campanha as CP

_spec = importlib.util.spec_from_file_location('criar_campanha',
                                               'scripts/criar-campanha.py')
CC = importlib.util.module_from_spec(_spec)
sys.modules['criar_campanha'] = CC
_spec.loader.exec_module(CC)

BASE = Path('output')
HUB = 'harness'
CAMPANHAS = BASE / HUB / 'campanhas'

def _dir_campanha_material_bypass(slug, base=None):
    """Pasta de campanha na estrutura NOVA: <hub>/campanhas/<nome-curto>."""
    base = Path(base) if base is not None else BASE
    nome = Path(str(slug).replace("\\", "/")).name
    return base / HUB / 'campanhas' / nome

CP.dir_campanha_material = _dir_campanha_material_bypass

def _achar_obra(nome):
    for tipo in ('livros', 'artigos', 'ebooks', 'playbooks',
                 'lead-magnets', 'decks', 'emails'):
        cand = BASE / HUB / tipo / nome
        if (cand / 'config_obra.json').exists():
            return f'{HUB}/{tipo}/{nome}'
    return None

alvos = sys.argv[1:]
total = 0
for pasta in sorted(CAMPANHAS.iterdir()):
    if not pasta.is_dir() or (alvos and pasta.name not in alvos):
        continue
    obra = _achar_obra(pasta.name)
    if not obra:
        print(f'  [skip] {pasta.name}: sem obra correspondente')
        continue
    try:
        ctx = CP.contexto_material(obra, BASE)
        geradas = CC.gerar_artes(ctx, BASE, com_artes=True)
        total += len(geradas)
        print(f'  {pasta.name}: {len(geradas)} artes | tags: {ctx.get("tags_arte")}')
    except Exception as exc:  # noqa: BLE001
        print(f'  [ERRO] {pasta.name}: {exc}')
print(f'=== total: {total} PNGs ===')
