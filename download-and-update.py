import json
import os
import re
import time
import urllib.request

photos_by_title = json.load(open('photos-by-title.json', encoding='utf-8'))
works = json.load(open('data.json', encoding='utf-8'))

by_title = {w['title']: w for w in works}

opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

downloaded = 0
skipped = 0
failed = []

for w in works:
    title = w['title']
    photos = photos_by_title.get(title, [])
    if not photos:
        continue
    # slug derived from existing cover path "images/<slug>.<ext>"
    m = re.match(r'images/(.+)\.(\w+)$', w['image'])
    slug = m.group(1) if m else re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

    local_paths = []
    for i, url in enumerate(photos):
        ext_match = re.search(r'\.(jpe?g|png|webp)$', url, re.IGNORECASE)
        ext = ext_match.group(1).lower().replace('jpeg', 'jpg') if ext_match else 'jpg'
        filename = f'{slug}.{ext}' if i == 0 else f'{slug}-{i+1}.{ext}'
        local_path = f'images/{filename}'
        full_path = os.path.join('.', local_path)
        if not os.path.exists(full_path):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=20) as resp, open(full_path, 'wb') as f:
                    f.write(resp.read())
                downloaded += 1
                time.sleep(0.05)
            except Exception as e:
                failed.append((title, url, str(e)))
                continue
        else:
            skipped += 1
        local_paths.append(local_path)

    if local_paths:
        w['image'] = local_paths[0]
        w['images'] = local_paths

print(f'Downloaded: {downloaded}, already existed: {skipped}, failed: {len(failed)}')
for f in failed:
    print('FAILED:', f)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(works, f, ensure_ascii=False, indent=2)
print('Updated data.json with images[] arrays')
