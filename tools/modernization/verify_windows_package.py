"""Check a downloaded Windows Actions package against its digest and Git tree.
GPL-3.0-or-later. Reads ZIP in place; does not run executable or extract assets.
"""
import argparse, hashlib, json, re, subprocess, zipfile
from pathlib import Path, PurePosixPath
from stage_windows import DEMO_DIRS
ROOT=Path(__file__).resolve().parents[2]
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--zip',type=Path,required=True)
    ap.add_argument('--expected-sha256',required=True)
    ap.add_argument('--commit',required=True)
    ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args()
    digest=hashlib.sha256(a.zip.read_bytes()).hexdigest()
    assert digest==a.expected_sha256.removeprefix('sha256:'),'ZIP digest mismatch'
    with zipfile.ZipFile(a.zip) as z:
        assert z.testzip() is None,'ZIP CRC error'
        names=z.namelist();assert len(names)==len(set(names)),'duplicate ZIP entries'
        for name in names:
            p=PurePosixPath(name)
            assert not p.is_absolute() and '..' not in p.parts and '\\' not in name and ':' not in name,'unsafe name'
            assert '.git' not in p.parts and '__pycache__' not in p.parts
        files={n for n in names if not n.endswith('/')}
        required={'COPYING','DATOS_DEMOS.md','openfodder.exe','SDL3.dll','SDL3_mixer.dll','VERSION.txt','PRUEBAS.json','INICIAR.cmd','PROBAR_OPCIONES_H5.cmd','LEEME.md','VALIDAR_RATON_H5.md'}
        assert required<=files,'missing root package files'
        assert {p.name for p in ROOT.glob('COPYING*')}<=files,'missing license'
        assert not any(n.startswith('Saves/') for n in files),'package has saved games'
        assert {PurePosixPath(n).parts[1] for n in files if n.startswith('Data/')}==set(DEMO_DIRS),'unexpected demo data directories'
        assert not any(n.lower().endswith(('.ofsave','.sav','.ini','.pending','.log')) for n in files),'unexpected user/config/log file'
        version=z.read('VERSION.txt').decode().strip();assert re.fullmatch('[0-9a-f]{40}',version)
        tree=git('rev-parse',a.commit+'^{tree}').decode().strip()
        assert git('rev-parse',version+'^{tree}').decode().strip()==tree,'VERSION tree mismatch; fetch version commit first'
        report=json.loads(z.read('PRUEBAS.json'))
        assert report['verdict']=='PASS' and report['phases_passed']==29 and report['skipped']==0
        assert z.read('openfodder.exe')[:2]==b'MZ','not a PE executable'
        exe=hashlib.sha256(z.read('openfodder.exe')).hexdigest()
        assert exe==report['executable_sha256'],'tested executable differs from packaged executable'
        for name in files:
            if name.endswith('.cmd') and name!='INICIAR.cmd':
                assert z.read(name).replace(b'\r\n',b'\n')==git('show',a.commit+':tools/modernization/windows/'+name),name
        assert z.read('INICIAR.cmd')==b'@echo off\r\ncd /d "%~dp0"\r\nopenfodder.exe --window --skipintro\r\nif errorlevel 1 pause\r\n'
        assert b'OPENFODDER_OPTIONS_TRACE=1' in z.read('PROBAR_OPCIONES_H5.cmd')
        for name,path in [('LEEME.md','docs/modernization/PRIMER_ARRANQUE_WINDOWS.md'),('VALIDAR_RATON_H5.md','docs/modernization/VALIDAR_RATON_WINDOWS_H5.md')]:
            assert z.read(name).replace(b'\r\n',b'\n')==git('show',a.commit+':'+path),name
        result={'verdict':'PASS','tested_commit':a.commit,'tested_tree':tree,'sha256':digest,'exe_sha256':exe,
          'entries':len(names),'files':len(files),'version':version,'temporary_pr_merge':version!=a.commit,
          'version_tree_matches':True,'phases_passed':29,'skipped':0,'save_fix_source_tree_included':True,
          'options_trace_launcher_matches':True,'demo_directories':list(DEMO_DIRS),
          'manifest':[{'path':n,'size':z.getinfo(n).file_size,'sha256':hashlib.sha256(z.read(n)).hexdigest()} for n in sorted(files)]}
        a.out.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:v for k,v in result.items() if k!='manifest'},indent=2))
if __name__=='__main__':main()
