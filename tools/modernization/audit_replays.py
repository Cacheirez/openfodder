"""Run OpenFodder replays with coverage checks. Python 3.10+, standard library only.

This measures replay completion, NOT full state equivalence or graphical quality.
SPDX-License-Identifier: GPL-3.0-or-later
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time


def parse_log(log):
    records = []
    errors = []
    for line in log.splitlines():
        if line.startswith("::error::"):
            errors.append(line)
        match = re.fullmatch(r"::notice::Test (.+): (.*?) \(\d+ms\) \[(Passed|Skipped|Running)\]", line)
        if match:
            name, message, status = match.groups()
            records.append({"name": name, "message": message, "status": status})
    return {"records": records, "errors": errors,
            "phases_passed": sum(r["status"] == "Passed" and r["message"] == "Phase Complete" for r in records),
            "skipped": sum(r["status"] == "Skipped" for r in records)}


def signature(report):
    return Counter((r["name"], r["message"], r["status"]) for r in report["records"])


def evaluate(report, baseline=None, allow_skips=False):
    reasons = []
    if report["timed_out"]:
        reasons.append("Timeout: execution did not finish.")
    if report["returncode"] != 0:
        reasons.append("Process returned an error.")
    if report["errors"]:
        reasons.append("Engine reported errors.")
    if not report["phases_passed"]:
        reasons.append("No completed phase: empty coverage is not success.")
    if report["skipped"] and not allow_skips:
        reasons.append("Skipped tests: inspect coverage; --allow-skips is for an explicitly partial audit.")
    if any(r["status"] == "Running" for r in report["records"]):
        reasons.append("Unfinished test records.")
    if baseline is not None:
        if baseline.get("verdict") != "PASS":
            reasons.append("Reference report is not a passing baseline.")
        if report.get("campaign") != baseline.get("campaign"):
            reasons.append("Reference used a different campaign selection.")
        if signature(report) != signature(baseline):
            reasons.append("Replay names or outcomes differ from reference.")
    return reasons


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exe", required=True, type=Path)
    parser.add_argument("--data", required=True, type=Path, help="Working directory containing Data, Campaigns and Tests")
    parser.add_argument("--out", required=True, type=Path, help="New report directory (must not exist)")
    parser.add_argument("--campaign")
    parser.add_argument("--video", action="store_true", help="Exercise real video producers (SDL software/dummy supported)")
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--allow-skips", action="store_true")
    args = parser.parse_args()
    exe, data = args.exe.resolve(), args.data.resolve()
    if not exe.is_file() or not all((data / x).is_dir() for x in ("Data", "Campaigns", "Tests")):
        parser.error("Executable or required Data/Campaigns/Tests directories missing.")
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    baseline = json.loads(args.baseline.read_text(encoding="utf-8")) if args.baseline else None
    args.out.mkdir(parents=True, exist_ok=False)
    cmd = [str(exe), "--appveyor", "--unit-test" if args.video else "--unit-test-headless"]
    if args.video:
        cmd.append("--nosound")
    if args.campaign:
        cmd.extend(["--campaign", args.campaign])
    started = time.monotonic()
    timed_out = False
    with (args.out / "engine.log").open("wb") as log:
        try:
            result = subprocess.run(cmd, cwd=data, stdout=log, stderr=subprocess.STDOUT, timeout=args.timeout, check=False)
            returncode = result.returncode
        except subprocess.TimeoutExpired:
            timed_out, returncode = True, None
        except OSError as exc:
            log.write(str(exc).encode("utf-8"))
            returncode = -1
    report = parse_log((args.out / "engine.log").read_text(encoding="utf-8", errors="replace"))
    report.update(command=cmd, campaign=args.campaign, returncode=returncode, video_enabled=args.video,
                  timed_out=timed_out, seconds=round(time.monotonic()-started, 3),
                  executable_sha256=hashlib.sha256(exe.read_bytes()).hexdigest(),
                  coverage="partial" if report["skipped"] else "available campaigns only")
    report["reasons"] = evaluate(report, baseline, args.allow_skips)
    report["verdict"] = "FAIL" if report["reasons"] else "PASS"
    report["limitations"] = "Replay completion only; no state hashes, GPU, audio or Windows validation implied. Unavailable campaigns may not be enumerated."
    (args.out / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("verdict", "phases_passed", "skipped", "coverage", "reasons")}, indent=2))
    return 1 if report["reasons"] else 0


if __name__ == "__main__":
    sys.exit(main())
