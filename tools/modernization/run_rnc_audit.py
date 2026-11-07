"""Test the bounded RNC-1 reader using only the freely distributed demo data.

Compiles a standalone C++ sanitizer harness on Linux. Does not touch
commercial CD32 resources. GPL-3.0-or-later.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--data", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    project = Path(__file__).resolve().parents[2]
    candidates = [f for f in args.data.rglob("*") if f.is_file()
                  and not any(x.lower() == "amiga_cd" for x in f.parts)]
    files = []
    for file in candidates:
        with file.open("rb") as stream:
            if stream.read(4) == b"RNC\x01":
                files.append(str(file.resolve()))
    if not files:
        p.error("Zero RNC-1 demo resources; cannot assert success.")
    args.out.mkdir(parents=True, exist_ok=True)
    binary = args.out / "rnc_sanitizer_test"
    subprocess.run(["g++", "-std=c++14", "-O1", "-g", "-fsanitize=address,undefined",
                    "-fno-omit-frame-pointer", "-I"+str(project/"Source"),
                    str(project/"Source/Amiga/dernc_bounded.cpp"),
                    str(project/"tools/modernization/test_rnc_bounded.cpp"),
                    "-o", str(binary)], check=True)
    environment = dict(os.environ, ASAN_OPTIONS="detect_leaks=0")
    result = subprocess.run([str(binary)] + sorted(files), env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, check=False)
    report = {"resource_count":len(files),"returncode":result.returncode,
              "output":result.stdout,"verdict":"PASS" if result.returncode==0 else "FAIL",
              "limitations":"Demo resources only; not a substitute for whole-engine ASan."}
    (args.out/"report.json").write_text(json.dumps(report,indent=2)+"\n", encoding="utf-8")
    print(json.dumps(report,indent=2))
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())
