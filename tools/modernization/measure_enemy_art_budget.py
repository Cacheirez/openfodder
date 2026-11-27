"""Measure the enemy art scope from retained native audit metadata.

This planning report never creates runtime bindings or approves artwork. Native
pixels stay outside the repository. All aliases are explicit and checked in
every retained format where the destination actually writes pixels.
"""
import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

from inventory_enemy_states import inventory


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def explicit_aliases():
    return [((0x51, 0), (0x49, 0), 'grenade preparation uses walking pose'),
            ((0x51, 2), (0x49, 1), 'grenade recovery uses walking passing pose'),
            *[((0xb8+i, 0), (0x72+i//3, i%3),
               'native falling table aliases the first eight low-mode rows') for i in range(8)],
            ((0xda, 1), (0xd9, 1), 'leader idle reuses leader walking passing pose')]


def measure(catalog, audit, player):
    by = {(r['format'], r['type'], r['sheet'], r['frame']): r for r in audit}
    assert len(by) == len(audit), 'Duplicate retained native contract'
    selected = {}
    formats = {}
    no_writes = []
    for fmt, name in enumerate(('PC', 'Amiga')):
        rows = catalog['platforms'][name]['slots']
        assert {(fmt, s['actor_type'], s['sheet'], s['frame']) for s in rows} == {
            k for k in by if k[0] == fmt}, 'Audit/catalog drift'
        groups = defaultdict(list)
        bodies = 0
        for s in rows:
            key = (fmt, s['actor_type'], s['sheet'], s['frame'])
            r = by[key]
            assert r['width'] > 0 and r['height'] > 0
            if not s['produced'] or s['actor_type'] not in (5, 36, 106):
                continue
            if not r['opaque_pixels']:
                no_writes.append(dict(format=fmt, type=r['type'], sheet=r['sheet'], frame=r['frame'],
                                      resource_sha256=r['resource_sha256'], native_signature=r['native_signature']))
                continue
            bodies += 1
            selected[key] = r
            groups[(r['native_signature'], r['width'], r['height'])].append(key)
        formats[name] = dict(opaque_body_contracts=bodies, exact_raster_groups=len(groups),
                             distinct_body_poses=len({k[2:] for g in groups.values() for k in g}))
    aliases = []
    for destination, source, reason in explicit_aliases():
        proofs = []
        for key, r in sorted(selected.items()):
            fmt, actor, sheet, frame = key
            if (sheet, frame) != destination:
                continue
            # Rocket enemies share the AI injury/fall body, but their normal
            # controller never produces mode-zero frames. The reference is
            # explicitly the ordinary AI enemy, not an invented type36 state.
            source_actor = 106 if actor == 106 else 5
            original = selected.get((fmt, source_actor, *source))
            assert original, 'Alias source is not a produced opaque body'
            assert all(r[k] == original[k] for k in ('width', 'height', 'native_signature', 'resource_sha256')), \
                'Explicit alias native raster differs'
            proofs.append(dict(format=fmt, type=actor, source_type=source_actor, resource_sha256=r['resource_sha256'],
                               native_signature=r['native_signature']))
        assert proofs, 'Alias has no retained opaque proof'
        aliases.append(dict(destination=list(destination), source=list(source), reason=reason,
                            proofs=proofs, status='verified native reuse candidate; no automatic runtime binding'))
    poses = {}
    for (_, _, sheet, frame), r in selected.items():
        geometry = (r['width'], r['height'])
        if (sheet, frame) in poses:
            assert poses[sheet, frame] == geometry, 'Cross-format geometry needs separate modern assets'
        poses[sheet, frame] = geometry
    # All selected body slots currently share 16x14. Do not infer a new width or
    # fit incompatible future formats into one asset to make a budget pass.
    assert set(poses.values()) == {(16, 14)}
    budget = 64*1024*1024
    estimates = {}
    for density in (8, 12):
        existing = sum(r['width']*r['height']*density*density*4
                       for r in player['assets'] if r['density'] == density)
        enemy = sum(width*height*density*density*4 for width, height in poses.values())
        total = existing + enemy
        estimates[str(density)] = dict(player_bytes=existing, enemy_body_upper_bound_bytes=enemy,
                                       combined_bytes=total, remaining_bytes=budget-total,
                                       fits=total <= budget)
    both = sum(r['combined_bytes'] for r in estimates.values())
    # Reserve three 16x14 enemy independent shadow assets as a conservative
    # geometry upper bound; no native shadow is invented by this accounting.
    reserve = {str(d): 3*16*14*d*d*4 for d in (8, 12)}
    assert all(estimates[str(d)]['combined_bytes']+reserve[str(d)] <= budget for d in (8, 12))
    return dict(schema=1, catalog_revision=catalog['revision'], native_formats=formats,
                distinct_opaque_body_poses=len(poses),
                verified_reuse_candidates=aliases,
                resource_specific_no_write_bodies=no_writes,
                budget_bytes=budget, density_estimates=estimates,
                independent_shadow_reserve_bytes=reserve,
                both_densities=dict(bytes=both, fits=both <= budget),
                decision='Load only the explicitly selected density; preserve 64 MiB preflight and legacy manifests.',
                limits=['Estimates, not loaded runtime coverage or gameplay acceptance.',
                        'Opaque body estimate includes all produced poses without alias savings.',
                        'Leader native marker remains an independent verified native draw.',
                        'Empty resources need resource-specific signature and no-write proof at runtime.',
                        'No aliases, unknown keys or unproduced rows are activated by this report.'])


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--audit', type=Path, required=True)
    p.add_argument('--player-manifest', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    report = measure(inventory(), json.loads(a.audit.read_text(encoding='utf-8')),
                     json.loads(a.player_manifest.read_text(encoding='utf-8')))
    report['inputs'] = dict(native_audit_sha256=sha(a.audit), player_manifest_sha256=sha(a.player_manifest))
    a.out.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(poses=report['distinct_opaque_body_poses'], aliases=len(report['verified_reuse_candidates']),
                          both_densities=report['both_densities'], estimates=report['density_estimates'])))
