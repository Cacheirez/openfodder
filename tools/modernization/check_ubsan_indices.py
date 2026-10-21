"""Strict ASan and UBSan gate for full OpenFodder demo regressions.
Any sanitizer finding fails the build. GPL-3.0-or-later.
"""
import argparse
import json
from pathlib import Path
import re
import sys

INDEX_WARNING = re.compile(r"runtime error:\s*index\s+.+?out of bounds", re.I)
OTHER_UBSAN = re.compile(r"runtime error:(?!\s*index\s+.+?out of bounds).+", re.I)
FATAL_ASAN = re.compile(r"ERROR:\s*AddressSanitizer|SUMMARY:\s*AddressSanitizer")

def assess(report, log):
    defects = []
    if (report.get("verdict") != "PASS" or report.get("phases_passed") != 29
            or report.get("skipped") != 0 or report.get("returncode") != 0):
        defects.append("Full 29-phase sanitized regression did not complete cleanly")
    bad_indices = [line for line in log.splitlines() if INDEX_WARNING.search(line)]
    if bad_indices:
        defects.append(f"{len(bad_indices)} UBSan array-index warnings")
    if FATAL_ASAN.search(log):
        defects.append("Fatal AddressSanitizer finding")
    other = [line for line in log.splitlines() if OTHER_UBSAN.search(line)]
    if other:
        defects.append(f"{len(other)} additional UBSan runtime errors")
    return defects, bad_indices, other

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--log", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = json.loads(args.report.read_text(encoding="utf-8"))
        log = args.log.read_text(encoding="utf-8", errors="replace")
    except (OSError, ValueError) as exc:
        print("FAIL: missing/corrupt sanitizer evidence:", exc, file=sys.stderr)
        return 1
    defects, bad_indices, other = assess(report, log)
    for bad in bad_indices:
        print("INDEX ERROR:", bad, file=sys.stderr)
    for bad in other:
        print("UBSAN ERROR:", bad, file=sys.stderr)
    print(f"ASan/UBSan report: phases={report.get('phases_passed')}; "
          f"index_UBSan={len(bad_indices)}; other_UBSan={len(other)}")
    if defects:
        print("FAIL:", "; ".join(defects), file=sys.stderr)
        return 1
    print("PASS: full sanitized replay; no ASan or UBSan findings")
    return 0

if __name__ == "__main__":
    sys.exit(main())
