"""Check recorded gameplay states against the pinned pre-modernization baseline.

Unlike comparing two runs of the same executable, this catches regressions
introduced by a code change. Preserve platform metadata separately.
GPL-3.0-or-later.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--traces", type=Path, nargs="+", required=True,
                        help="One or more directories containing one phase JSONL file each")
    args = parser.parse_args()
    reference = json.loads(args.baseline.read_text(encoding="utf-8"))
    actual = {}
    for directory in args.traces:
        if not directory.is_dir():
            parser.error(f"Missing traces directory: {directory}")
        for path in directory.glob("*.jsonl"):
            if path.name in actual:
                parser.error(f"Duplicate phase: {path.name}")
            actual[path.name] = path
    expected = {item["file"]: item for item in reference["phases"]}
    if not expected or set(expected) != set(actual):
        print("FAIL: phase coverage differs from reference")
        print("Missing:", sorted(set(expected) - set(actual)))
        print("Unexpected:", sorted(set(actual) - set(expected)))
        return 1
    samples = 0
    for name, info in sorted(expected.items()):
        # Normalize OS line terminators, not logical data.
        raw = actual[name].read_bytes().replace(b"\r\n", b"\n")
        if b"\n" not in raw:
            print(f"FAIL: missing metadata header {name}")
            return 1
        meta, payload = raw.split(b"\n", 1)
        try:
            header = json.loads(meta)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            print(f"FAIL: bad metadata {name}: {exc}")
            return 1
        if header.get("kind") != "meta" or header.get("schema_version") != 1:
            print(f"FAIL: unsupported schema {name}")
            return 1
        count = payload.count(b"\n")
        digest = hashlib.sha256(payload).hexdigest()
        if count != info["samples"] or digest != info["logical_sha256"]:
            print(f"FAIL: changed logical state {name}: samples={count}, hash={digest}")
            return 1
        samples += count
    if samples != reference["total_samples"]:
        print(f"FAIL: total samples changed: {samples}")
        return 1
    print(f"PASS: {len(expected)} demo phases, {samples} canonical states match pinned baseline")
    return 0

if __name__ == "__main__":
    sys.exit(main())
