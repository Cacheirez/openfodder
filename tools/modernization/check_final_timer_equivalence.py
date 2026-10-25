"""Compare the real legacy and refactored retail timer bodies in isolation.

Requires git history for the accepted H2.6 baseline and a C++14 compiler.
No commercial data, SDL, or new gameplay baseline is used.
Graphics methods are recording stubs: this checks timer state and draw cadence,
not graphical output. GPL-3.0-or-later.
"""
import argparse
from pathlib import Path
import subprocess
import tempfile

BASELINE = "5e6a4f3834a0a491468ea659f45f8e5f4fb785a8"

from audit_contract import without_audit

def function(source, signature, preserve_audit=False):
    if not preserve_audit:
        source = without_audit(source)
    start = source.index(signature)
    opening = source.index("{", start)
    depth = 0
    for i in range(opening, len(source)):
        if source[i] == "{":
            depth += 1
        elif source[i] == "}":
            depth -= 1
            if depth == 0:
                return source[start:i + 1]
    raise ValueError("Unclosed function: " + signature)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compiler", default="g++")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    path = "Source/GUI_Element.cpp"
    old = subprocess.check_output(["git", "show", BASELINE + ":" + path], cwd=root, text=True)
    current = (root / path).read_text()
    legacy = function(old, "void cFodder::Mission_Final_TimeToDie()").replace(
        "cFodder::Mission_Final_TimeToDie()", "cFodder::LegacyTimeToDie()", 1)
    update = function(current, "bool cFodder::Mission_Final_TimeToDie_Update()")
    wrapper = function(current, "void cFodder::Mission_Final_TimeToDie()")
    harness = r"""
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>
using int16 = int16_t;
struct Version {
    bool retail, cf1;
    bool isRetail() const { return retail; }
    bool isCannonFodder1() const { return cf1; }
};
struct Params { bool mDisableVideo; };
struct cFodder {
    Version* mVersionCurrent;
    Params* mParams;
    struct { int mMission_Number, mMission_Phase; } mGame_Data;
    int16 mMission_Final_TimeToDie_Ticker, mMission_Final_TimeRemain;
    int16 mGUI_Sidebar_TroopList_Name_BreakOnSpace = 5;
    std::array<uint8_t, 0x1600> mSidebar_Screen_Buffer;
    std::vector<int> drawCalls;
    void GUI_Sidebar_TroopList_Name_Draw(int, int, int, const char*) {
        drawCalls.push_back(mGUI_Sidebar_TroopList_Name_BreakOnSpace);
    }
    void GUI_Sidebar_Number_Draw(int n, int, int, int, int) {
        drawCalls.push_back(n);
    }
    bool Mission_Final_TimeToDie_Update();
    void Mission_Final_TimeToDie();
    void LegacyTimeToDie();
};
"""
    harness += legacy + "\n" + update + "\n" + wrapper
    harness += r"""
int main() {
    size_t checks = 0;
    for (bool retail : {false, true})
    for (bool cf1 : {false, true})
    for (bool disabled : {false, true})
    for (int mission : {23, 24, 25})
    for (int phase : {5, 6, 7})
    for (int ticker : {0, 38, 39, 40})
    for (int remaining : {0, 1, 2, 90}) {
        Version version{retail, cf1};
        Params params{disabled};
        cFodder old{}, current{};
        old.mVersionCurrent = &version;
        old.mParams = &params;
        old.mGame_Data = {mission, phase};
        old.mMission_Final_TimeToDie_Ticker = ticker;
        old.mMission_Final_TimeRemain = remaining;
        old.mSidebar_Screen_Buffer.fill(0xAB);
        current = old;
        for (int tick = 0; tick < 160; ++tick) {
            old.LegacyTimeToDie();
            current.Mission_Final_TimeToDie();
            ++checks;
            if (old.mMission_Final_TimeToDie_Ticker != current.mMission_Final_TimeToDie_Ticker ||
                old.mMission_Final_TimeRemain != current.mMission_Final_TimeRemain ||
                old.mGUI_Sidebar_TroopList_Name_BreakOnSpace != current.mGUI_Sidebar_TroopList_Name_BreakOnSpace ||
                old.mSidebar_Screen_Buffer != current.mSidebar_Screen_Buffer ||
                old.drawCalls != current.drawCalls) {
                std::cerr << "FAIL: retail timer diverged at tick " << tick << '\n';
                return 1;
            }
        }
    }
    std::cout << "PASS: " << checks << " retail timer transitions match H2.6, including video-off and draw calls\n";
}
"""
    with tempfile.TemporaryDirectory(prefix="openfodder-timer-") as directory:
        source = Path(directory) / "timer.cpp"
        binary = Path(directory) / "timer"
        source.write_text(harness)
        subprocess.run([args.compiler, "-std=c++14", "-O1", "-fsanitize=undefined",
                        "-fno-sanitize-recover=all", str(source), "-o", str(binary)], check=True)
        subprocess.run([str(binary)], check=True)

if __name__ == "__main__":
    main()
