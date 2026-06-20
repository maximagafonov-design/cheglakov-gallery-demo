import json
import os
import re

photos_by_title = json.load(open('photos-by-title.json', encoding='utf-8'))
works = json.load(open('data.json', encoding='utf-8'))

restored = 0
missing_files = []

for w in works:
    title = w['title']
    photos = photos_by_title.get(title, [])
    if not photos:
        continue
    m = re.match(r'images/(.+?)(?:-\d+)?\.(\w+)$', w['image'])
    slug = m.group(1) if m else re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

    local_paths = []
    for i, url in enumerate(photos):
        ext_match = re.search(r'\.(jpe?g|png|webp)$', url, re.IGNORECASE)
        ext = ext_match.group(1).lower().replace('jpeg', 'jpg') if ext_match else 'jpg'
        filename = f'{slug}.{ext}' if i == 0 else f'{slug}-{i+1}.{ext}'
        local_path = f'images/{filename}'
        if not os.path.exists(local_path):
            missing_files.append((title, local_path))
            continue
        local_paths.append(local_path)

    if local_paths:
        w['image'] = local_paths[0]
        w['images'] = local_paths
        restored += 1

print(f'Restored: {restored} works')
if missing_files:
    print('Missing files (kept whatever was already there for these slots):')
    for t, p in missing_files:
        print(' ', t, p)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(works, f, ensure_ascii=False, indent=2)
print('Saved data.json (dedup reverted, restored to ground-truth-validated source)')
