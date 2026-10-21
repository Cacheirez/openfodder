"""Run one recorded campaign twice; compare the actual game-state traces.
The deliberate corruption test changes only an analysis copy of a real trace,
never the game's state or replay input. GPL-3.0-or-later.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from compare_gameplay_traces import compare, TraceError
from audit_replays import parse_log, signature


def sha_manifest(directory):
    files = sorted(directory.rglob("*.ofd"))
    if not files:
        raise RuntimeError(f"No .ofd fixtures under {directory}")
    digest = hashlib.sha256()
    for path in files:
        digest.update(path.relative_to(directory).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest(), len(files)


def run_once(exe, data, out, campaign, fixture_hash, settings_hash, timeout):
    out.mkdir(parents=True, exist_ok=False)
    traces = out / "traces"
    traces.mkdir()
    env = dict(os.environ,
               OPENFODDER_TRACE_DIR=str(traces.resolve()),
               OPENFODDER_TRACE_REPLAY_SHA256=fixture_hash,
               OPENFODDER_TRACE_SETTINGS_SHA256=settings_hash)
    cmd = [str(exe), "--appveyor", "--unit-test-headless", "--campaign", campaign]
    try:
        with (out / "engine.log").open("wb") as log:
            proc = subprocess.run(cmd, cwd=data, env=env, stdout=log,
                                  stderr=subprocess.STDOUT, timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"Replay timed out: {out}") from exc
    report = parse_log((out / "engine.log").read_text(encoding="utf-8", errors="replace"))
    if proc.returncode or report["errors"] or report["skipped"] or report["phases_passed"] <= 0:
        raise RuntimeError(f"Replay did not complete: {out}, exit={proc.returncode}, report={report}")
    paths = {p.name: p for p in traces.glob("*.jsonl")}
    if len(paths) != report["phases_passed"]:
        raise RuntimeError(f"Expected {report['phases_passed']} traces, got {len(paths)}")
    return report, paths


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--exe", type=Path, required=True)
    p.add_argument("--data", type=Path, required=True)
    p.add_argument("--campaign", default="PC Format")
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--timeout", type=int, default=600)
    args = p.parse_args()
    exe = args.exe.resolve()
    data = args.data.resolve()
    if not exe.is_file() or not (data / "Tests").is_dir():
        p.error("Executable or Tests folder missing")
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    fixtures, fixture_count = sha_manifest(data / "Tests")
    command_profile = json.dumps({"campaign": args.campaign,
                                  "flags": ["--appveyor", "--unit-test-headless"],
                                  "fixture_count": fixture_count},
                                 sort_keys=True, separators=(",", ":"))
    settings = hashlib.sha256(command_profile.encode("utf-8")).hexdigest()
    results = {"campaign": args.campaign, "fixture_count": fixture_count,
               "fixtures_sha256": fixtures, "settings_sha256": settings,
               "executable_sha256": hashlib.sha256(exe.read_bytes()).hexdigest(),
               "verdict": "FAIL", "compared_phases": 0, "compared_ticks": 0}
    try:
        a, aa = run_once(exe, data, out / "run1", args.campaign, fixtures, settings, args.timeout)
        b, bb = run_once(exe, data, out / "run2", args.campaign, fixtures, settings, args.timeout)
        if signature(a) != signature(b) or set(aa) != set(bb):
            raise RuntimeError("Different missions or test outcomes in the two runs")
        for name in sorted(aa):
            mismatch = compare(aa[name], bb[name])
            if mismatch:
                raise RuntimeError(f"State divergence in {name}: {mismatch}")
            with aa[name].open(encoding="utf-8") as fp:
                n = sum(1 for _ in fp) - 1
            results["compared_ticks"] += n
            results["compared_phases"] += 1

        # Mutation test over an actual emitted trace: alter a genuine tracked
        # value ONLY in an analysis copy. No gameplay, input or source mutation.
        first = sorted(aa)[0]
        source = aa[first]
        records = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines()]
        records[1]["state"]["game"]["kills_home"] += 1
        tampered = out / "mutated_analysis_copy.jsonl"
        tampered.write_text("".join(json.dumps(r, separators=(",", ":")) + "\n" for r in records),
                            encoding="utf-8")
        detected = compare(source, tampered)
        if not detected or detected[1] != "state.game.kills_home":
            raise RuntimeError(f"Comparator failed actual-trace field mutation test: {detected}")
        results["mutation_detected"] = list(detected)
        results["verdict"] = "PASS"
    except (RuntimeError, TraceError, OSError, ValueError) as exc:
        results["failure"] = str(exc)
    (out / "report.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2))
    return 0 if results["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
