"""Losslessly archive replay logs/traces with shared bodies and exact file hashes.
GPL-3.0-or-later. Run after timing; JSONL metadata is retained separately.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    archive = {'format': 'openfodder-replay-shared-bodies-v1', 'files': [], 'bodies': {}}
    for path in sorted(a.source.rglob('*')):
        if not path.is_file() or path.suffix not in ('.log', '.jsonl'):
            continue
        raw = path.read_bytes()
        prefix, body = b'', raw
        if path.suffix == '.jsonl':
            first, separator, body = raw.partition(b'\n')
            prefix = first+separator
        key = digest(body)
        archive['bodies'][key] = body.decode('utf-8')
        archive['files'].append(dict(path=path.relative_to(a.source).as_posix(),
                                     sha256=digest(raw), prefix=prefix.decode('utf-8'), body_sha256=key))
    if not archive['files']:
        raise ValueError('No logs or traces to preserve')
    with gzip.GzipFile(filename=str(a.out), mode='wb', mtime=0) as zipped:
        zipped.write(json.dumps(archive, ensure_ascii=False, separators=(',', ':')).encode('utf-8'))
    with gzip.open(a.out, 'rt', encoding='utf-8') as zipped:
        restored = json.load(zipped)
    for item in restored['files']:
        body = restored['bodies'][item['body_sha256']].encode('utf-8')
        assert digest(body) == item['body_sha256']
        raw = item['prefix'].encode('utf-8')+body
        assert digest(raw) == item['sha256']
        assert raw == (a.source/item['path']).read_bytes()
    print(json.dumps(dict(verdict='PASS', files=len(restored['files']),
                          unique_bodies=len(restored['bodies']), bytes=a.out.stat().st_size,
                          sha256=digest(a.out.read_bytes()))))


if __name__ == '__main__':
    main()
