"""Bundle the offline review page with the unchanged C01 PNG; no image editing.
GPL-3.0-or-later.
"""
from pathlib import Path
import argparse
import base64
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

def build():
    source = ROOT/'assets/modernization/soldier-c01/source.png'
    manifest = json.loads(source.with_name('manifest.json').read_text())
    data = source.read_bytes()
    if hashlib.sha256(data).hexdigest() != manifest['source_sha256']:
        raise ValueError('Original C01 hash does not match the preserved manifest')
    folder = ROOT/'tools/modernization/density-preview'
    html = (folder/'index.html').read_text()
    code = (folder/'model.js').read_text()+'\n'+(folder/'preview.js').read_text()
    code = code.replace("../../../assets/modernization/soldier-c01/source.png",
                        'data:image/png;base64,'+base64.b64encode(data).decode('ascii'))
    if '</script' in code.lower():
        raise ValueError('Unexpected script terminator')
    html = html.replace('<script src="model.js"></script><script src="preview.js"></script>',
                        '<script>'+code+'</script>')
    # Preserve useful links when opening this single downloaded file anywhere.
    html = html.replace('href="../../../',
        'href="https://github.com/Cacheirez/openfodder/blob/modernization/windows-foundation/')
    return html

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(build(), encoding='utf-8')
