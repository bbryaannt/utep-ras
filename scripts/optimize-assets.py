"""Create responsive WebP copies; requires Pillow. Originals are never modified."""
from pathlib import Path
from PIL import Image, ImageOps
import json
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'dist/assets'
NAMES=['rover.jpg','garage-occupancy-sensor.jpg','rtx-pop-art.png','rover-magazine-cutout.png','rover-competition-team.jpg','rover-test-field.jpg']
manifest={}
for name in NAMES:
    original=ImageOps.exif_transpose(Image.open(ASSETS/name))
    original=original.convert('RGBA' if 'A' in original.getbands() else 'RGB')
    widths=[320,480,640,960] if 'cutout' in name else [320,480,640,960,1440]
    variants=[]
    for width in widths:
        if width>original.width:continue
        out=ASSETS/(Path(name).stem+'-'+str(width)+'.webp')
        resized=original.resize((width,round(original.height*width/original.width)),Image.Resampling.LANCZOS)
        resized.save(out,'WEBP',quality=72,method=6)
        avif=out.with_suffix('.avif')
        resized.save(avif,'AVIF',quality=55,speed=6)
        variants.append({'width':width,'path':'assets/'+out.name,'bytes':out.stat().st_size,'avif':'assets/'+avif.name,'avif_bytes':avif.stat().st_size})
    manifest['assets/'+name]={'width':original.width,'height':original.height,'original_bytes':(ASSETS/name).stat().st_size,'variants':variants}
(ROOT/'content/responsive-images.json').write_text(json.dumps(manifest,indent=2)+'\n')
for name,item in manifest.items():
    target=min(item['variants'],key=lambda x:abs(x['width']-960))
    print(f"{name}: {item['original_bytes']:,} → {target['bytes']:,} bytes (960px)")
