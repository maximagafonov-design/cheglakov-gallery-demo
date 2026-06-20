import json
import os
from PIL import Image

DATA_PATH = 'data.json'


def ahash(path, size=8):
    img = Image.open(path).convert('L').resize((size, size), Image.LANCZOS)
    pixels = list(img.getdata())
    avg = sum(pixels) / len(pixels)
    bits = 0
    for p in pixels:
        bits = (bits << 1) | (1 if p > avg else 0)
    return bits


def hamming(a, b):
    return bin(a ^ b).count('1')


THRESHOLD = 4  # out of 64 bits - strict, only near-identical frames

works = json.load(open(DATA_PATH, encoding='utf-8'))

total_removed = 0
works_affected = []

for w in works:
    imgs = w.get('images') or []
    if len(imgs) < 2:
        continue
    hashes = []
    for p in imgs:
        try:
            hashes.append(ahash(p))
        except Exception as e:
            hashes.append(None)

    kept_imgs = []
    kept_hashes = []
    for p, h in zip(imgs, hashes):
        if h is None:
            kept_imgs.append(p)
            kept_hashes.append(h)
            continue
        is_dup = any(kh is not None and hamming(h, kh) <= THRESHOLD for kh in kept_hashes)
        if is_dup:
            continue
        kept_imgs.append(p)
        kept_hashes.append(h)

    if len(kept_imgs) != len(imgs):
        removed = len(imgs) - len(kept_imgs)
        total_removed += removed
        works_affected.append((w['title'], len(imgs), len(kept_imgs)))
        w['images'] = kept_imgs
        w['image'] = kept_imgs[0]

print(f'Works affected: {len(works_affected)}, total photos removed: {total_removed}')
for t, before, after in works_affected:
    print(f'  {t}: {before} -> {after}')

with open(DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(works, f, ensure_ascii=False, indent=2)
print('Saved data.json')
