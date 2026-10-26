"""Check freshness and references of the partial CD32 vehicle review, not gameplay.
GPL-3.0-or-later. No original resources or runtime simulation required.
"""
import hashlib
import json
from pathlib import Path
import re

from check_sprite_table_lengths import check as check_tables

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = 'docs/modernization/evidence/cd32-vehicle-capabilities.json'
CENSUS = 'docs/modernization/evidence/cd32-sprite-census.json'


def validate(review, census, read):
    if review['schema'] != 1 or review['evidence'] != 'static_review_only':
        raise ValueError('Unsupported review scope')
    for source in review['sources']:
        data = read(source['path'])
        if hashlib.sha256(data).hexdigest() != source['sha256']:
            raise ValueError('Source changed; review required: ' + source['path'])
        for symbol in source['functions']:
            if not re.search(r'\b' + re.escape(symbol) + r'\s*\(', data.decode()):
                raise ValueError('Missing source symbol: ' + symbol)
    phases = {p['map']: p for p in census['phases']}
    if len(phases) != census['phase_count']:
        raise ValueError('Ambiguous census phases')
    seen = set()
    for scenario in review['scenarios']:
        name = scenario['map']
        if name in seen or name not in phases:
            raise ValueError('Duplicate or missing phase: ' + name)
        seen.add(name)
        phase = phases[name]
        if scenario['execution'] != 'pending':
            raise ValueError('This static manifest cannot certify runtime coverage')
        if any(scenario[k] != phase[k] for k in ('mission', 'phase', 'resources')):
            raise ValueError('Scenario metadata differs: ' + name)
        if any(phase['counts'].get(str(t), 0) < 1 for t in scenario['types']):
            raise ValueError('Scenario type absent from SPT: ' + name)
    if {s['resources']['base_tileset'] for s in review['scenarios']} != {'jun', 'des', 'ice', 'mor', 'int'}:
        raise ValueError('Five resource environments are not represented')
    text = read('Source/Amiga/SpriteData_Amiga.hpp').decode()
    arrays, tables = check_tables(text)
    table = tables['mSpriteSheetTypes_InGame_Amiga']
    for component in review['components']:
        if table[component['sheet']] != component['array']:
            raise ValueError('Component points to another frame array')
        if arrays[component['array']] != component['frames']:
            raise ValueError('Component frame count differs')
    return len(review['sources']), len(review['scenarios']), len(review['components'])


def main():
    review = json.loads((ROOT / MANIFEST).read_text())
    census = json.loads((ROOT / CENSUS).read_text())
    sources, scenarios, components = validate(review, census, lambda p: (ROOT / p).read_bytes())
    print(f'PASS static references: {sources} sources, {scenarios} scenarios, {components} components; runtime pending')


if __name__ == '__main__':
    main()
