"""Add bounded scene/call metadata to an existing local diagnostic WindowHD copy.

Does not change recovery conditions, rendering or simulation. The input may contain
the pre-existing private native-snapshot exporter; no resources are published.
"""
import argparse
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    text = a.input.read_text(encoding='utf-8')
    changes = [
        ('    // Opt-in, bounded diagnostics: each distinct reason once per process.\n',
         '    // Local opt-in probe: at most 40 reasons per scene, 256 per process.\n'
         '    static uint64_t diagnosticCalls=0;\n'
         '    const auto diagnosticCall=++diagnosticCalls;\n'),
        ('        static const char* seen[40]={};static unsigned count=0;\n',
         '        static const char* seen[40]={};static unsigned count=0,total=0;\n'
         '        const uint64_t diagnosticScene=g_Fodder?g_Fodder->mPresentationScene:0;\n'
         '        static uint64_t lastDiagnosticScene=~uint64_t(0);\n'
         '        if(lastDiagnosticScene!=diagnosticScene){count=0;lastDiagnosticScene=diagnosticScene;}\n'),
        ('        if(count<40){seen[count++]=reason;std::fprintf(stderr,\n'
         '            "SOLDIER_HD_REASON: %s density=%s\\n",reason,option);',
         '        if(count<40 && total<256){seen[count++]=reason;++total;std::fprintf(stderr,\n'
         '            "SOLDIER_HD_REASON: %s density=%s scene=%llu call=%llu\\n",reason,option,\n'
         '            static_cast<unsigned long long>(diagnosticScene),static_cast<unsigned long long>(diagnosticCall));')
    ]
    for before, after in changes:
        assert text.count(before) == 1, 'Unexpected source; do not patch heuristically'
        text = text.replace(before, after)
    assert not a.out.exists(), 'Preserve existing diagnostic sources'
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(text, encoding='utf-8', newline='\n')
    # Reverse the exact substitutions to prove that no other source was changed.
    for before, after in reversed(changes):
        text = text.replace(after, before)
    assert text == a.input.read_text(encoding='utf-8')
    print('PASS diagnostic-only substitutions; guards/rendering unchanged; bounded 40/scene and 256/process')


if __name__ == '__main__':
    main()
