import json
import re

KNOWN_TITLES = ["Sun Temple","Vessel of Light","Before Words","Evening Light","Only Love","Open Heart",
    "Within","Turning of Time","Shadow of Form","Spirit of Time","Whole","Waiting for Wings","Gold Fish",
    "Wild forms","The Joker's Smile","Wave of luck","Dance of Fire","Shell of Hera","Embrace of Zeus",
    "Apollo's Lyre","Tree of life, Bahrain","The Wing","Wings of Light","Wings of Soulrise",
    "The Grand Menorah","Ancient Torah Pages (Hanukkiah)","Maccabee Flames","Tablets of Stone","Calvary",
    "Vigilance","Light of the Torah","Grace","Venice Solo","Ocean Spirit","Rebirth","The Golden Fleece",
    "Abduction of Europa","Bird of paradise","Guardian of the State","Ascension","Wild Cat the Jaguar",
    "The Boar","The Rhino","Bullfighting","The Owl of Athens","The legend of the falcon","Dragon dance",
    "Varan and dragonfly","Touch of the ocean","Cachalot's Shadow","Night Flight","Rising moon",
    "Crescent Moon","Mirage","Vertical","Prayer","Sacred Oak","Paradise tree","Angel with a candle",
    "Embrace","Line of Light","Openwork","Menorah Vintage","Menorah sunrise","Menorah","Mehorah Imperial",
    "Menorah Lite","Oak Arc Menorah","Artwork Menorah Rainbow","Joy of light (hanukkah)","Seven lights",
    "Talk to me","Golden bar","Wall street","As-salam wall clock","Trophy Clock",
    "Royal Clock Tower in Mecca. Hommage.","Burj Khalifa. Hommage.","The Christmas Tree",
    "Christmas Trinity","Cave paintings","Cave Flames","Cave of Light","Lurking Lizard",
    "The Echo of the jungle","Eight Flames of Miracle"]

META_RE = re.compile(r'itemprop="image" content="([^"]+)"')


def real_gallery(metas):
    """The static HTML duplicates each work's gallery once per responsive breakpoint, so the
    sequence near a title looks like [junk...][P1,P2,...,Pn,P1,P2,...,Pn]. Find the longest
    trailing [A,A] split — that's the work's own (deduped, ordered) photo list."""
    n = len(metas)
    best = metas[:] if n else []
    k = 2
    while k <= n:
        half = k // 2
        suffix = metas[-k:]
        if suffix[:half] == suffix[half:]:
            best = suffix[:half]
        k += 2
    return best


def extract(html, titles):
    pattern = '|'.join(re.escape(t) for t in sorted(titles, key=len, reverse=True))
    matches = list(re.finditer(pattern, html))
    result = {}
    prev_end = 0
    for m in matches:
        title = m.group(0)
        # Some descriptions start with the same word as the title (e.g. "Whole — Wood Art
        # Object..."), which re-matches right after the real title and would otherwise
        # overwrite the correct (first) match with an empty gallery. Keep first match only.
        if title not in result:
            chunk = html[prev_end:m.start()]
            metas = META_RE.findall(chunk)
            result[title] = real_gallery(metas)
        prev_end = m.end()
    return result


main_html = open('cheglakov-main.html', encoding='utf-8').read()
archive_html = open('cheglakov-archive.html', encoding='utf-8').read()

main_result = extract(main_html, KNOWN_TITLES)
archive_result = extract(archive_html, KNOWN_TITLES)

merged = {}
for title in KNOWN_TITLES:
    if title in main_result and main_result[title]:
        merged[title] = main_result[title]
    elif title in archive_result and archive_result[title]:
        merged[title] = archive_result[title]
    elif title in main_result:
        merged[title] = main_result[title]
    elif title in archive_result:
        merged[title] = archive_result[title]
    else:
        merged[title] = []

missing = [t for t, photos in merged.items() if not photos]
print('Total titles:', len(KNOWN_TITLES))
print('Found with photos:', sum(1 for p in merged.values() if p))
print('Missing/empty:', missing)

with open('photos-by-title.json', 'w', encoding='utf-8') as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)
print('Saved photos-by-title.json')
