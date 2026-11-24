"""Export a portable static site with only referenced assets; no Sites runtime required."""
from pathlib import Path
import re, zipfile
ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
files={p for p in DIST.iterdir() if p.is_file()}
for path in list(files):
    if path.suffix in ('.html','.css','.js','.xml','.txt'):
        for asset in re.findall(r'assets/[A-Za-z0-9_./-]+',path.read_text()):
            target=DIST/asset
            if target.is_file():files.add(target)
# Retain the licenses when fonts are copied into an export or container.
files.update((DIST/'assets/fonts').glob('*OFL.txt'))
out=ROOT/'exports/utep-ras-static.zip';out.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(files):z.write(p,p.relative_to(DIST))
print(f'{out}: {len(files)} files, {out.stat().st_size:,} bytes')
