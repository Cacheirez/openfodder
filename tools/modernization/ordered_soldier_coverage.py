"""Summarize actual ordered SDL transactions; never award visual acceptance.

Opt in with OPENFODDER_ORDERED_COVERAGE=1. Each input must be one process log.
Truncated or inconsistent evidence is an error, never a successful publication.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import re

OUTCOMES = {'published', 'missing-variant', 'no-body', 'manifest-invalid',
            'classic-recovered', 'recovery-failed', 'interrupted'}
COMMAND = {'attempt', 'scene', 'interval', 'order', 'slot', 'generation', 'type',
           'sheet', 'frame', 'key', 'decision', 'density'}
RESULT = {'attempt', 'outcome', 'expected', 'observed', 'replace', 'keep', 'missing', 'density'}


def report(paths):
    outcomes, variants, entities = Counter(), {}, {}
    commands, published_commands = set(), set()
    attempts = published_draws = unresolved = 0
    for log_index, path in enumerate(paths):
        transactions = {}
        with Path(path).open() as stream:
            for line in stream:
                kind = next((k for k in ('COMMAND', 'RESULT') if f'SOLDIER_ORDERED_{k}: ' in line), None)
                if kind is None:
                    continue
                payload = line.split(f'SOLDIER_ORDERED_{kind}: ', 1)[1].strip().split()
                pairs = [part.split('=', 1) for part in payload]
                if any(len(p) != 2 for p in pairs):
                    raise ValueError('malformed ordered coverage record')
                row = dict(pairs)
                if len(row) != len(pairs) or row.keys() != (COMMAND if kind == 'COMMAND' else RESULT):
                    raise ValueError('incomplete or duplicate ordered coverage fields')
                for key in row.keys() - {'key', 'decision', 'outcome'}:
                    row[key] = int(row[key])
                    if key not in {'type', 'sheet', 'frame'} and row[key] < 0:
                        raise ValueError('negative ordered coverage counter')
                if row['density'] not in (8, 12):
                    raise ValueError('invalid ordered density')
                transaction = transactions.setdefault(row['attempt'], {'rows': [], 'result': None})
                if kind == 'COMMAND':
                    if not re.fullmatch('[0-9a-f]{64}', row['key']) or row['decision'] not in {'replace', 'keep', 'missing'}:
                        raise ValueError('invalid ordered variant/decision')
                    if transaction['result'] is not None:
                        raise ValueError('command after transaction result')
                    transaction['rows'].append(row)
                else:
                    if transaction['result'] is not None or row['outcome'] not in OUTCOMES:
                        raise ValueError('duplicate/invalid ordered transaction result')
                    transaction['result'] = row
        for transaction in transactions.values():
            result, rows = transaction['result'], transaction['rows']
            if result is None:
                raise ValueError('truncated ordered transaction')
            counts = Counter(r['decision'] for r in rows)
            if (len(rows) != result['observed'] or len({r['order'] for r in rows}) != len(rows)
                    or any(r['density'] != result['density'] for r in rows)
                    or result['observed'] > result['expected']
                    or any(counts[k] != result[k] for k in ('replace', 'keep', 'missing'))):
                raise ValueError('inconsistent ordered transaction census')
            published = result['outcome'] == 'published'
            complete = result['expected'] == result['observed']
            if published and (not complete or not result['replace'] or result['missing']):
                raise ValueError('publication without complete replacement census')
            attempts += 1
            outcomes[result['outcome']] += 1
            unresolved += result['expected'] - result['observed']
            for r in rows:
                identity = (log_index, r['scene'], r['interval'], r['order'])
                commands.add(identity)
                v = variants.setdefault((r['key'], r['density']), Counter())
                entity = (log_index, r['scene'], r['slot'], r['generation'], r['type'],
                          r['sheet'], r['frame'], r['key'], r['density'])
                e = entities.setdefault(entity, Counter())
                v['resolution_' + r['decision']] += 1
                e['resolution_' + r['decision']] += 1
                if published and r['decision'] == 'replace':
                    published_draws += 1
                    published_commands.add((*identity, r['key'], r['density']))
                    v['published_presentations'] += 1
                    e['published_presentations'] += 1
                else:
                    v['unpublished_presentations'] += 1
                    e['unpublished_presentations'] += 1
    return dict(schema=1, verdict='PENDING', scope='ordered transaction evidence; no global art/visual/CD32 acceptance',
                attempts=attempts, outcomes=dict(sorted(outcomes.items())),
                unique_producer_commands=len(commands), published_command_presentations=published_draws,
                unique_published_variant_commands=len(published_commands), unresolved_commands=unresolved,
                variants=[dict(key=k, density=d, **v) for (k, d), v in sorted(variants.items())],
                entity_states=[dict(zip(('log', 'scene', 'slot', 'generation', 'type', 'sheet',
                                         'frame', 'key', 'density'), key), **counts)
                               for key, counts in sorted(entities.items())])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--log', action='append', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = report(args.log)
    args.out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in {'variants', 'entity_states'}}))


if __name__ == '__main__':
    main()
