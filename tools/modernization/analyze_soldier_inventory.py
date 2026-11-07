"""Summarize diagnostic prepared bodies, never claim final HD coverage.
GPL-3.0-or-later.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path


def analyze(path):
    phases = defaultdict(list)
    for line in path.read_text().splitlines():
        if not line.startswith('PILOT_BODY:'):
            continue
        values = [int(v) for v in line.split()[1:]]
        if len(values) != 17 or min(values[:6]) < 0:
            raise ValueError('Invalid producer record')
        phases[tuple(values[:2])].append(values)
    if not phases:
        raise ValueError('No producer records')
    result = []
    for (mission, phase), rows in sorted(phases.items()):
        counts = Counter((r[4], r[5]) for r in rows)
        result.append(dict(mission=mission, phase=phase, prepared_calls=len(rows),
            unique_ticks=len({r[2] for r in rows}),
            keys=[dict(sheet=s, frame=f, calls=n) for (s,f),n in sorted(counts.items())],
            batch_key_calls=sum(n for (s,f),n in counts.items() if s in (2,7) and f in (0,1,2)),
            geometry=sorted({tuple(r[9:14]) for r in rows})))
    return dict(scope='First live player; prepared bodies before final occlusion/eligibility. Calls may repeat within a tick.',
                log_sha256=hashlib.sha256(path.read_bytes()).hexdigest(), phases=result)

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--log', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args=parser.parse_args()
    args.out.write_text(json.dumps(analyze(args.log), indent=2)+'\n')
