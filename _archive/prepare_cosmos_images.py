"""Fetch the selected official images; requires requests and Pillow, only for asset refresh."""
from io import BytesIO
from pathlib import Path
import json
import requests
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
manifest = ROOT / 'cosmos-images.json'
images = json.loads(manifest.read_text(encoding='utf-8'))
destination = ROOT.parent / 'assets' / 'cosmos'
destination.mkdir(parents=True, exist_ok=True)
for item in images:
    response = requests.get(item['image_url'], timeout=60)
    response.raise_for_status()
    picture = ImageOps.exif_transpose(Image.open(BytesIO(response.content))).convert('RGB')
    if min(picture.size) < 200:
        raise ValueError(f"Unexpected thumbnail: {item['id']} {picture.size}")
    picture.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
    item['width'], item['height'] = picture.size
    picture.save(destination / f"{item['id']}.webp", 'WEBP', quality=88, method=6)
    print(f"{item['id']}: {item['width']} x {item['height']}")
manifest.write_text(json.dumps(images, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
