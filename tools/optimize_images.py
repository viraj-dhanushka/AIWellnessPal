#!/usr/bin/env python3
"""Generates the web-optimized images the pages use (needs Pillow).

Run from the repo root after adding or replacing screenshots:
    python3 tools/optimize_images.py

- assets/screens/<name>.jpg  ->  assets/screens/w/<name>-300.webp and -600.webp
  (the pages show screenshots 190-280px wide, so these cover 1x-2x screens).
- assets/icon-source.png (full-bleed 512px app icon) -> site icons:
  icon.png (512, used in structured data), icon-96/-192 (.webp/.png) for the
  header and CTA, apple-touch-icon.png (180, full-bleed: iOS rounds it),
  favicon.png (64, rounded corners), icon-maskable-512.png (web manifest).
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
SCREENS = ROOT / 'assets' / 'screens'
OUT = SCREENS / 'w'
OUT.mkdir(exist_ok=True)


def screens():
    for jpg in sorted(SCREENS.glob('*.jpg')):
        im = Image.open(jpg).convert('RGB')
        for w in (300, 600):
            h = round(im.height * w / im.width)
            dst = OUT / f'{jpg.stem}-{w}.webp'
            im.resize((w, h), Image.LANCZOS).save(dst, 'WEBP', quality=80, method=6)
    print('screens:', len(list(OUT.glob('*.webp'))), 'webp files')


def rounded(im, radius_ratio=0.225):
    size = im.size[0]
    mask = Image.new('L', im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size - 1, size - 1), int(size * radius_ratio), fill=255)
    out = Image.new('RGBA', im.size, (0, 0, 0, 0))
    out.paste(im, (0, 0), mask)
    return out


def icons():
    src = Image.open(ROOT / 'assets' / 'icon-source.png').convert('RGBA')
    sq = lambda n: src.resize((n, n), Image.LANCZOS)
    sq(512).convert('RGB').save(ROOT / 'assets' / 'icon.png', optimize=True)
    for n in (96, 192):
        sq(n).save(ROOT / 'assets' / f'icon-{n}.webp', 'WEBP', quality=88, method=6)
        sq(n).convert('RGB').save(ROOT / 'assets' / f'icon-{n}.png', optimize=True)
    sq(180).convert('RGB').save(ROOT / 'assets' / 'apple-touch-icon.png', optimize=True)
    rounded(sq(64)).save(ROOT / 'assets' / 'favicon.png', optimize=True)
    # Maskable icon: art inside the central safe zone on the icon's own colours.
    canvas = sq(512).convert('RGB')
    inner = src.resize((410, 410), Image.LANCZOS)
    canvas.paste(inner, (51, 51), inner)
    canvas.save(ROOT / 'assets' / 'icon-maskable-512.png', optimize=True)
    print('icons written')


if __name__ == '__main__':
    screens()
    icons()
