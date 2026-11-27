"""Explicit PC-only authoring for audited empty Amiga enemy commands."""
import hashlib
import json
from inventory_enemy_states import ROOT


def empty_signature(width, height):
    return hashlib.sha256(b'CF1POSE\x01' + width.to_bytes(8, 'little') +
                          height.to_bytes(8, 'little') + bytes(width * height)).hexdigest()


def audited_pc_only(pose):
    actor, sheet, frame = (pose[k] for k in ('type', 'sheet', 'frame'))
    return ((actor == 5 and sheet == 0xdc and frame == 0) or
            (actor == 106 and ((sheet in (0xd8, 0xd9) and 0 <= frame < 24) or
                              (sheet == 0xda and 0 <= frame < 3))))


def source_art_formats(pose, export, expected_formats):
    """Return drawn formats only after checking complete native provenance."""
    rows = export['native']
    drawn = {n['format'] for n in rows}
    assert len(rows) == len(drawn), 'Duplicate native format'
    no_write = export.get('native_no_write', [])
    if not no_write:
        assert drawn == expected_formats, 'Enemy native source-format coverage'
        return drawn
    assert audited_pc_only(pose), 'No-write authoring outside audited enemy scope'
    assert expected_formats == {0, 1} and drawn == {0}, 'Only audited PC-only art'
    assert len(no_write) == 1, 'One signed empty Amiga resource required'
    n = no_write[0]
    assert n['format'] == 1 and n['segment'] == 0, 'Unknown empty source format/segment'
    assert n['logical_size'] == [16, 14] and n['bbox'] is None and n['opaque_pixels'] == 0, 'Empty native geometry'
    assert n['native_signature'] == empty_signature(16, 14), 'Native no-write signature is not empty'
    audit = json.loads((ROOT / 'docs/modernization/evidence/enemy-source-native-audit.json').read_text(encoding='utf-8'))
    resources = audit['private_reference_summary']['resources']
    assert any((r['format'], r['segment'], r['sha256']) ==
               (n['format'], n['segment'], n['resource_sha256']) for r in resources), 'Unknown empty native resource'
    return drawn
