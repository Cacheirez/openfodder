"""Strict comparison of OpenFodder gameplay-state JSONL traces (no engine mutation).
GPL-3.0-or-later. Python >= 3.10, standard library only.
"""
import argparse
import json
from pathlib import Path
import sys

META_FIELDS = ("schema_version", "campaign", "mission", "phase", "platform",
               "resource_platform", "replay_sha256", "settings_sha256",
               "seed", "sampling_point")
STATE_FIELDS = ("game", "controls", "rng", "sprites")


class TraceError(ValueError):
    pass


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise TraceError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def verify_values(value, context):
    if value is None or type(value) in (str, int, bool):
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            verify_values(item, f"{context}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            verify_values(item, f"{context}.{key}")
        return
    raise TraceError(f"{context}: invalid non-integer/unsupported value")


def read_trace(path):
    records = []
    try:
        with Path(path).open(encoding="utf-8") as stream:
            for index, line in enumerate(stream, 1):
                if not line.strip():
                    raise TraceError(f"{path}:{index}: blank line")
                value = json.loads(line, object_pairs_hook=unique_keys)
                if not isinstance(value, dict):
                    raise TraceError(f"{path}:{index}: expected object")
                verify_values(value, f"{path}:{index}")
                records.append(value)
    except (OSError, json.JSONDecodeError) as exc:
        raise TraceError(f"{path}: {exc}") from exc
    if len(records) < 2 or records[0].get("kind") != "meta":
        raise TraceError(f"{path}: missing header or ticks")
    meta = records[0]
    for field in META_FIELDS:
        if field not in meta:
            raise TraceError(f"{path}: missing meta.{field}")
    if meta["schema_version"] != 1 or meta["sampling_point"] != "post-phase-cycle":
        raise TraceError(f"{path}: incompatible trace schema or sampling point")
    if len(meta["seed"]) != 4 or not all(type(x) is int for x in meta["seed"]):
        raise TraceError(f"{path}: invalid seed")
    previous = -1
    for rec in records[1:]:
        n = rec.get("tick")
        if rec.get("kind") != "tick" or type(n) is not int or n <= previous:
            raise TraceError(f"{path}: nonmonotonic/missing tick identifier")
        previous = n
        state = rec.get("state")
        if not isinstance(state, dict) or any(
            field not in state for field in STATE_FIELDS
        ):
            raise TraceError(f"{path}: incomplete logical state")
        if not all(isinstance(state[field], dict) and state[field]
                   for field in ("game", "controls", "rng")):
            raise TraceError(f"{path}: missing logical state values")
        sprites = state["sprites"]
        if not isinstance(sprites, list):
            raise TraceError(f"{path}: invalid sprites")
        slots = [s.get("slot") for s in sprites if isinstance(s, dict)]
        if (len(slots) != len(sprites) or any(type(s) is not int for s in slots)
                or slots != sorted(set(slots))):
            raise TraceError(f"{path}: invalid sprite slots")
    return meta, records[1:]


def diff_value(a, b, path):
    if type(a) is not type(b):
        return (path, a, b)
    if isinstance(a, dict):
        for key in sorted(set(a) | set(b)):
            p = f"{path}.{key}"
            if key not in a or key not in b:
                return (p, a.get(key, "<missing>"), b.get(key, "<missing>"))
            found = diff_value(a[key], b[key], p)
            if found:
                return found
        return None
    if isinstance(a, list):
        if len(a) != len(b):
            return (path + ".length", len(a), len(b))
        for i, (x, y) in enumerate(zip(a, b)):
            found = diff_value(x, y, f"{path}[{i}]")
            if found:
                return found
        return None
    if a != b:
        return (path, a, b)
    return None


def compare(reference, candidate):
    meta_a, ticks_a = read_trace(reference)
    meta_b, ticks_b = read_trace(candidate)
    for field in META_FIELDS:
        if meta_a[field] != meta_b[field]:
            return ("metadata", f"meta.{field}", meta_a[field], meta_b[field])
    for index in range(max(len(ticks_a), len(ticks_b))):
        if index >= len(ticks_a) or index >= len(ticks_b):
            return ("coverage", f"tick_record[{index}]", len(ticks_a), len(ticks_b))
        x, y = ticks_a[index], ticks_b[index]
        if x["tick"] != y["tick"]:
            return ("coverage", f"tick_record[{index}].tick", x["tick"], y["tick"])
        found = diff_value(x["state"], y["state"], "state")
        if found:
            return (f"tick {x['tick']}",) + found
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", type=Path)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()
    try:
        found = compare(args.reference, args.candidate)
    except TraceError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if found:
        where, field, a, b = found
        print(f"FAIL {where}: {field}: {a!r} != {b!r}")
        return 1
    print("PASS: identical tracked gameplay states on every captured tick")
    return 0


if __name__ == "__main__":
    sys.exit(main())
