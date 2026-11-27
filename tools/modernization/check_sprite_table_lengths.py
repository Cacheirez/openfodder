"""Check actual source frame array lengths and generated metadata (GPL-3.0-or-later)."""
import re
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ARRAY=re.compile(r"(?:^|\n)\s*(?:const\s+)?sSpriteSheet\s+(\w+)\s*\[\s*(\d*)\s*\]\s*=\s*\{([\s\S]*?)\};")
TABLE=re.compile(r"const\s+sSpriteSheet\s*\*\s*(mSpriteSheetTypes_\w+)\s*\[\s*\]\s*=\s*\{([\s\S]*?)\};")
COUNT=re.compile(r"const\s+std::size_t\s+(mSpriteSheetTypes_\w+)_FrameCounts\[\]\s*=\s*\{([\s\S]*?)\};")
EXTENT=re.compile(r"sizeof\((\w+)\)\s*/\s*sizeof\(\1\[0\]\)")
COMMENT=re.compile(r"//[^\n]*|/\*[\s\S]*?\*/")
def check(text):
    arrays={}
    for name,explicit,data in ARRAY.findall(text):
        frames=len(re.findall(r"\{\s*[-\w]",data))
        if explicit and frames != int(explicit): raise ValueError(name+": explicit extent mismatch")
        arrays[name]=frames
    tables={n:[v.strip() for v in COMMENT.sub("",body).split(",") if v.strip()] for n,body in TABLE.findall(text)}
    counts={n:EXTENT.findall(COMMENT.sub("",body)) for n,body in COUNT.findall(text)}
    if not tables or set(tables)!=set(counts): raise ValueError("Missing sprite frame metadata group")
    for name,refs in tables.items():
        if refs != counts[name]: raise ValueError(name+": incorrect frame metadata order")
        if any(ref not in arrays or arrays[ref]<1 for ref in refs): raise ValueError(name+": missing/empty frame array")
    return arrays,tables
def main():
    total=0
    for platform,expected in (("Amiga",768),("PC",541)):
        source=(ROOT/"Source"/platform/f"SpriteData_{platform}.hpp").read_text(encoding="utf-8")
        arrays,tables=check(source)
        entries=sum(map(len,tables.values()))
        if entries != expected: raise ValueError(f"{platform}: unexpected {entries} frame groups")
        graphics=(ROOT/"Source"/platform/f"Graphics_{platform}.cpp").read_text(encoding="utf-8")
        for name in tables:
            if name == "mSpriteSheetTypes_InGame_Amiga_CF2":
                if f"SetActiveSpriteSheetPtr({name}," not in graphics:
                    raise ValueError("Missing CF2 sprite bounds helper")
                amiga2=(ROOT/"Source"/"Amiga"/"Graphics_Amiga2.cpp").read_text(encoding="utf-8")
                if "SetActiveCF2SpriteSheet();" not in amiga2:
                    raise ValueError("CF2 subclass does not use bounded activation")
                continue
            if f"SetActiveSpriteSheetPtr({name}, {name}_FrameCounts)" not in graphics:
                raise ValueError("Missing bounds activation for "+name)
        print(f"PASS {platform}: {len(arrays)} arrays, {len(tables)} pointer tables, {entries} sheets")
        total += entries
    print(f"PASS total {total} source-derived frame extents")
if __name__=="__main__":
    try: main()
    except ValueError as e:
        print("FAIL:",e,file=sys.stderr);sys.exit(1)
