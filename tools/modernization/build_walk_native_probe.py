"""Emit a diagnostic WindowHD copy for native artwork review; never edit the engine.
GPL-3.0-or-later. Snapshot output includes original pixels: do not commit it.
"""
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NEEDLE = 'const auto key=openfodder::SoldierVariantKey(command,current.indexed.colors);'


def build():
    source = (ROOT/'Source/WindowHD.cpp').read_text()
    if source.count(NEEDLE) != 1:
        raise ValueError('WindowHD resolver changed; inspect before generating diagnostic copy')
    return '#include "walk_native_probe.hpp"\n' + source.replace(NEEDLE, NEEDLE +
        '\n                openfodder::ExportWalkNativeSnapshot(command,current.indexed.colors,key);')


def project(directory, headers):
    directory.mkdir(parents=True, exist_ok=False)
    (directory/'include').mkdir()
    (directory/'WindowHD.cpp').write_text(build())
    (directory/'include/gitver.hpp').write_text('const char* gitversion = "diagnostic-native-walk";\n')
    sources = [p for p in (ROOT/'Source').rglob('*.cpp') if p.name not in
               ('Sound_PC.cpp', 'Sound_PC2.cpp', 'Start_Emscripten.cpp', 'WindowHD.cpp')]
    sources.append(directory/'WindowHD.cpp')
    def quoted(path):
        return '"'+path.as_posix()+'"'
    cmake = ('cmake_minimum_required(VERSION 3.16)\nproject(native_probe LANGUAGES C CXX)\n'
             'set(CMAKE_CXX_STANDARD 14)\nfind_package(SDL3 CONFIG REQUIRED)\nfind_package(Threads REQUIRED)\n'
             'add_executable(native_probe\n'+''.join(quoted(p)+'\n' for p in sources)+')\n'
             'target_include_directories(native_probe PRIVATE '+
             ' '.join(quoted(p) for p in (ROOT/'Source', directory/'include', headers, ROOT/'tools/modernization'))+')\n'
             'target_compile_definitions(native_probe PRIVATE OPENFODDER_NO_MIXER)\n'
             'target_link_libraries(native_probe PRIVATE SDL3::SDL3 Threads::Threads)\n')
    (directory/'CMakeLists.txt').write_text(cmake)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--emit', type=Path)
    group.add_argument('--project', type=lambda s: Path(s).resolve())
    parser.add_argument('--headers', type=lambda s: Path(s).resolve(), help='Existing generated C01/pilot headers; required with --project')
    args = parser.parse_args()
    if args.project:
        if not args.headers:
            parser.error('--project requires --headers')
        project(args.project, args.headers)
    else:
        args.emit.write_text(build())
