import json

with open("data.json", encoding="utf-8") as f:
    works = json.load(f)

# Section mapping per Sasha's structure (subset shown in prototype — thematic best-guess from
# available titles, NOT Sasha's authoritative list. Needs his confirmation, see plan TODO.)
SECTIONS = {
    "The Witnessing Wood": ["The Wing", "Calvary", "Tablets of Stone", "Prayer", "Tree of life, Bahrain",
                             "Apollo's Lyre", "Embrace of Zeus", "Grace", "Venice Solo", "Ocean Spirit", "Rebirth"],
    "Meditations in Wood": ["Sun Temple", "Vessel of Light", "Before Words", "Evening Light", "Only Love",
                             "Open Heart", "Within", "Turning of Time", "Shadow of Form", "Spirit of Time",
                             "Whole", "Waiting for Wings"],
    "Light Sculptures": ["Light of the Torah", "Wings of Light", "Wings of Soulrise", "The Grand Menorah",
                          "Ancient Torah Pages (Hanukkiah)", "Maccabee Flames", "Menorah Vintage", "Menorah",
                          "Seven lights", "Eight Flames of Miracle", "Menorah sunrise", "Mehorah Imperial",
                          "Menorah Lite", "Oak Arc Menorah", "Artwork Menorah Rainbow", "Joy of light (hanukkah)"],
    "Animal Forms": ["Wild Cat the Jaguar", "The Boar", "The Rhino", "Bullfighting", "The Owl of Athens",
                      "The legend of the falcon", "Dragon dance", "Varan and dragonfly", "Cachalot's Shadow",
                      "Bird of paradise", "Lurking Lizard", "Gold Fish", "Vigilance"],
    "Organic Forms": ["Wild forms", "Wave of luck", "Dance of Fire", "Touch of the ocean", "Rising moon",
                       "Crescent Moon", "Mirage", "Vertical", "The Echo of the jungle",
                       "Abduction of Europa", "Ascension", "Cave paintings", "Embrace", "Night Flight",
                       "Openwork", "Paradise tree", "Sacred Oak", "Shell of Hera",
                       "The Golden Fleece"],
    "Architectural Objects": ["As-salam wall clock", "Trophy Clock", "Royal Clock Tower in Mecca. Hommage.",
                               "Burj Khalifa. Hommage.", "Wall street", "Golden bar", "Guardian of the State"],
    "Seasonal Works": ["The Christmas Tree", "Christmas Trinity"],
}
SECTIONS["Light Sculptures"] += ["Angel with a candle", "Cave Flames", "Cave of Light", "Line of Light",
                                  "The Joker's Smile"]

by_title = {w["title"]: w for w in works}

ru_nav = {
    "The Witnessing Wood": "Свидетельствующее дерево",
    "Meditations in Wood": "Размышления в дереве",
    "Light Sculptures": "Световые скульптуры",
    "Animal Forms": "Образы животных",
    "Organic Forms": "Органические формы",
    "Architectural Objects": "Архитектурные объекты",
    "Seasonal Works": "Сезонные работы",
}
STATUS_RU = {"Available": "В наличии", "Sold": "Продано", "Not available for purchase": "Не продаётся"}

section_html = []
for section, titles in SECTIONS.items():
    tiles = []
    for t in titles:
        w = by_title.get(t)
        if not w:
            continue
        status_class = "available" if w["status"] == "Available" else ("sold" if w["status"] == "Sold" else "na")
        desc = (w.get("description") or "").replace('"', '&quot;')
        desc_ru = (w.get("description_ru") or w.get("description") or "").replace('"', '&quot;')
        dims = w.get("dimensions") or "—"
        images_attr = json.dumps(w.get("images") or [w["image"]]).replace('"', '&quot;')
        tiles.append(f'''
        <div class="tile" data-title="{w['title'].lower()}" onclick="openCard(this)"
             data-en="{desc}" data-ru="{desc_ru}" data-status-en="{w['status']}" data-status-ru="{STATUS_RU.get(w['status'], w['status'])}"
             data-dims="{dims}" data-images="{images_attr}">
          <img src="{w['image']}" alt="{w['title']}" loading="lazy">
          <div class="tile-overlay">
            <div class="tile-title">{w['title']}</div>
            <div class="tile-status {status_class}" data-en="{w['status']}" data-ru="{STATUS_RU.get(w['status'], w['status'])}">{w['status']}</div>
          </div>
        </div>''')
    section_html.append(f'''
    <section class="gallery-section" id="{section.lower().replace(' ', '-').replace(chr(39),'')}" data-nav-en="{section}" data-nav-ru="{ru_nav.get(section, section)}">
      <div class="section-header">
        <div class="section-label">Section</div>
        <h2 class="section-title" data-en="{section}" data-ru="{ru_nav.get(section, section)}">{section}</h2>
      </div>
      <div class="tile-grid">{''.join(tiles)}</div>
    </section>''')

# Works in Interior — same 12 Meditations in Wood images, shown again as plain interior shots
# (no status/price/card), per plan: this section is not separate works, just an alternate view.
viz_titles = SECTIONS["Meditations in Wood"]
viz_tiles = []
for i, t in enumerate(viz_titles, 1):
    w = by_title.get(t)
    if not w:
        continue
    viz_tiles.append(f'''
    <div class="viz-tile">
      <img src="{w['image']}" alt="Interior Visualization {i:02d}" loading="lazy">
    </div>''')

viz_section = f'''
<section class="gallery-section" id="works-in-interior" data-nav-en="Works in Interior" data-nav-ru="Работы в интерьере">
  <div class="section-header">
    <div class="section-label">Section</div>
    <h2 class="section-title" data-en="Works in Interior" data-ru="Работы в интерьере">Works in Interior</h2>
  </div>
  <div class="tile-grid viz-grid">{''.join(viz_tiles)}</div>
</section>'''

nav_links = '<a href="#about" data-en="About" data-ru="О художнике">About</a>' + ''.join(
    f'<a href="#{s.lower().replace(" ", "-").replace(chr(39),"")}" data-en="{s}" data-ru="{ru_nav.get(s,s)}">{s}</a>'
    for s in SECTIONS
) + '<a href="#works-in-interior" data-en="Works in Interior" data-ru="Работы в интерьере">Works in Interior</a><a href="#exhibitions" data-en="Exhibitions" data-ru="Выставки">Exhibitions</a><a href="#contacts" data-en="Contacts" data-ru="Контакты">Contacts</a>'

ABOUT_EN = "I create sculptural objects from centuries-old wood shaped by time and natural forces. The material comes from oak trees that lived for hundreds of years before becoming fragments — many from regions crossed by Napoleon Bonaparte's 1812 campaign. I do not alter their form. I work with what already exists, preserving natural relief, fractures, and traces of age. My intervention is minimal: wax, metal, and light are used only to stabilize and clarify the structure. Each work is unique."
ABOUT_RU = "Я создаю скульптурные объекты из многовековой древесины, сформированной временем и природными силами. Материал — дубы, простоявшие сотни лет, многие из регионов, через которые проходила кампания Наполеона 1812 года. Я не изменяю их форму. Я работаю с тем, что уже существует, сохраняя естественный рельеф, трещины и следы возраста. Моё вмешательство минимально: воск, металл и свет используются только для стабилизации и прояснения структуры. Каждая работа уникальна."

EXHIBITIONS = [
    ("2019", "The Art of Nature, Alpert Gallery, Moscow"),
    ("2019", "INDECOR Moscow, Crocus Expo, Moscow"),
    ("2020", "The Art of Nature, State Museum of Sergey Andriyaki, Moscow"),
    ("2020", "Maison & Objet, International Exhibition, Paris"),
    ("2021", "Qatar International Art Festival, Doha"),
    ("2021", "Textures & Patterns, Las Laguna Art Gallery, California, USA"),
    ("2021", "Bentley Motors — Autumn Tour, Russia"),
    ("2024", "The Original Miami Beach Antique Show, Miami Beach Convention Center, USA"),
    ("2024", "Palm Beach Fine Craft Show, Palm Beach, Florida, USA"),
    ("2024", "ARTEXPO New York, Pier 36, New York, USA"),
    ("2025–2026", "Hanukkah Sculptures Exhibition, Chabad of South Dade / Coconut Grove, Florida, USA"),
]
exhibitions_html = ''.join(f'<div class="exh-row"><strong>{y}</strong><span>{e}</span></div>' for y, e in EXHIBITIONS)

about_section = f'''
<section class="text-section" id="about">
  <div class="section-header"><div class="section-label">About</div><h2 class="section-title" data-en="About the Artist" data-ru="О художнике">About the Artist</h2></div>
  <p class="prose" data-en="{ABOUT_EN}" data-ru="{ABOUT_RU}">{ABOUT_EN}</p>
</section>'''

exhibitions_section = f'''
<section class="text-section" id="exhibitions">
  <div class="section-header"><div class="section-label">Exhibitions</div><h2 class="section-title" data-en="Exhibition History" data-ru="История выставок">Exhibition History</h2></div>
  <div class="exh-list">{exhibitions_html}</div>
</section>'''

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cheglakov Art — Museum Noir Prototype</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:#0a0908; color:#e8d9bd; font-family:Georgia,'Times New Roman',serif; }}
  header {{ display:flex; align-items:center; justify-content:space-between; padding:18px 28px; border-bottom:1px solid #2a231c; position:sticky; top:0; background:#0a0908; z-index:10; flex-wrap:wrap; gap:12px; }}
  .logo {{ font-size:15px; letter-spacing:3px; }}
  nav {{ display:flex; gap:18px; font-size:11px; letter-spacing:1px; color:#a8916b; flex-wrap:wrap; }}
  nav a {{ color:#a8916b; text-decoration:none; text-transform:uppercase; }}
  nav a:hover {{ color:#c9a468; }}
  .controls {{ display:flex; gap:12px; align-items:center; }}
  #search {{ background:#1c1815; border:1px solid #3a2f24; color:#e8d9bd; font-size:12px; padding:7px 12px; border-radius:3px; width:180px; }}
  #search::placeholder {{ color:#6b5d49; }}
  .icon-btn {{ border:1px solid #c9a468; color:#c9a468; border-radius:50%; width:28px; height:28px; display:flex; align-items:center; justify-content:center; font-size:12px; cursor:pointer; background:none; }}
  .icon-btn.muted {{ opacity:0.4; }}
  #lang-toggle {{ border:1px solid #5a4d3c; color:#a8916b; background:none; font-size:11px; padding:5px 10px; cursor:pointer; letter-spacing:1px; }}
  .section-header {{ padding:40px 28px 8px; }}
  .section-label {{ font-size:11px; letter-spacing:2px; color:#c9a468; text-transform:uppercase; }}
  .section-title {{ font-size:28px; font-style:italic; margin-top:6px; }}
  .tile-grid {{ column-count:6; column-gap:5px; padding:16px 28px; }}
  .tile {{ position:relative; overflow:hidden; background:#1c1815; cursor:pointer; margin-bottom:5px; break-inside:avoid; }}
  .tile img {{ width:100%; height:auto; display:block; filter:brightness(0.75) sepia(0.15); transition:filter 0.3s, transform 0.4s; }}
  .tile:hover img {{ filter:brightness(0.95) sepia(0.1); transform:scale(1.1); }}
  .tile-overlay {{ position:absolute; bottom:0; left:0; right:0; padding:10px; background:linear-gradient(transparent, rgba(10,9,8,0.92)); }}
  .tile-title {{ font-size:12px; color:#e8d9bd; }}
  .tile-status {{ font-size:9px; letter-spacing:1px; text-transform:uppercase; margin-top:2px; }}
  .tile-status.available {{ color:#8fae8a; }}
  .tile-status.sold {{ color:#a87a6b; }}
  .tile-status.na {{ color:#6b5d49; }}
  .tile.hidden {{ display:none; }}
  .viz-tile {{ position:relative; overflow:hidden; background:#1c1815; margin-bottom:5px; break-inside:avoid; }}
  .viz-tile img {{ width:100%; height:auto; display:block; filter:brightness(0.75) sepia(0.15); }}
  footer {{ text-align:center; padding:32px; font-size:10px; letter-spacing:2px; color:#5a4d3c; border-top:1px solid #2a231c; margin-top:24px; }}
  .text-section {{ padding-bottom:20px; border-bottom:1px solid #2a231c; }}
  .prose {{ padding:0 28px; max-width:700px; line-height:1.7; color:#cdbf9e; font-size:14px; }}
  .exh-list {{ padding:0 28px 20px; }}
  .exh-row {{ display:flex; gap:16px; padding:6px 0; font-size:13px; color:#cdbf9e; border-bottom:1px solid #1c1815; }}
  .exh-row strong {{ color:#c9a468; min-width:90px; }}
  .modal-bg {{ display:none; position:fixed; inset:0; background:rgba(0,0,0,0.85); z-index:50; align-items:center; justify-content:center; }}
  .modal-bg.open {{ display:flex; }}
  .modal-card {{ background:#0a0908; border:1px solid #3a2f24; width:min(1300px, 95vw); max-height:95vh; overflow-y:auto; padding:28px; position:relative; }}
  .modal-close {{ position:absolute; top:10px; right:14px; cursor:pointer; color:#a8916b; font-size:24px; z-index:2; background:rgba(10,9,8,0.6); width:34px; height:34px; border-radius:50%; display:flex; align-items:center; justify-content:center; }}
  .modal-carousel {{ position:relative; background:#000; margin:-28px -28px 18px; }}
  #modal-img {{ width:100%; max-height:75vh; object-fit:contain; display:block; background:#000; }}
  .carousel-arrow {{ position:absolute; top:50%; transform:translateY(-50%); background:rgba(10,9,8,0.6); border:1px solid #c9a468; color:#c9a468; width:48px; height:48px; border-radius:50%; cursor:pointer; font-size:22px; display:flex; align-items:center; justify-content:center; }}
  .carousel-prev {{ left:16px; }}
  .carousel-next {{ right:16px; }}
  .carousel-counter {{ position:absolute; bottom:14px; right:18px; font-size:13px; color:#e8d9bd; background:rgba(10,9,8,0.65); padding:4px 11px; border-radius:10px; letter-spacing:1px; }}
  #modal-title {{ font-size:22px; font-style:italic; color:#c9a468; margin-bottom:10px; }}
  #modal-desc {{ font-size:13px; line-height:1.6; color:#cdbf9e; margin-bottom:10px; }}
  #modal-meta {{ font-size:11px; color:#8a7a5f; letter-spacing:1px; }}
  a {{ transition:color 0.2s, letter-spacing 0.2s; }}
  nav a, .icon-btn, #lang-toggle, .modal-close, footer a {{ transition:color 0.25s, transform 0.25s, opacity 0.25s; }}
  nav a:hover {{ color:#f0dcae; letter-spacing:2px; }}
  .icon-btn:hover {{ transform:scale(1.15); opacity:1; }}
  #lang-toggle:hover {{ color:#f0dcae; border-color:#f0dcae; }}
  .modal-close:hover {{ color:#f0dcae; transform:scale(1.2); }}
  footer {{ display:flex; flex-direction:column; gap:10px; align-items:center; }}
  footer a {{ color:#c9a468; text-decoration:none; font-size:11px; letter-spacing:1px; }}
  footer a:hover {{ color:#f0dcae; text-decoration:underline; }}
  .footer-links {{ display:flex; gap:18px; }}
  @media (max-width: 768px) {{
    .tile-grid {{ column-count:3; column-gap:3px; padding:10px; }}
    .tile {{ margin-bottom:3px; }}
    nav {{ order:3; width:100%; justify-content:center; }}
    #search {{ width:130px; }}
  }}
</style>
</head>
<body>

<header>
  <div class="logo">CHEGLAKOV ART</div>
  <nav>{nav_links}</nav>
  <div class="controls">
    <input id="search" type="text" placeholder="Search work..." oninput="filterTiles(this.value)">
    <button id="lang-toggle" onclick="toggleLang()">RU / EN</button>
    <button class="icon-btn" id="sound-btn" onclick="toggleSound()">&#9834;</button>
  </div>
</header>

{about_section}

{''.join(section_html)}

{viz_section}

{exhibitions_section}

<footer id="contacts">
  <a href="mailto:info@cheglakovart.com">info@cheglakovart.com</a>
  <div class="footer-links">
    <a href="https://www.instagram.com/cheglakov.art" target="_blank">Instagram</a>
    <a href="https://www.pinterest.com/Cheglakovart/" target="_blank">Pinterest</a>
    <a href="https://www.facebook.com/cheglakovart" target="_blank">Facebook</a>
  </div>
</footer>

<div class="modal-bg" id="modal-bg" onclick="if(event.target===this)closeCard()">
  <div class="modal-card">
    <span class="modal-close" onclick="closeCard()">&times;</span>
    <div class="modal-carousel">
      <img id="modal-img" src="" alt="">
      <button class="carousel-arrow carousel-prev" onclick="shiftImage(-1)">&#8249;</button>
      <button class="carousel-arrow carousel-next" onclick="shiftImage(1)">&#8250;</button>
      <div id="modal-counter" class="carousel-counter"></div>
    </div>
    <div id="modal-title"></div>
    <div id="modal-desc"></div>
    <div id="modal-meta"></div>
  </div>
</div>

<script>
let lang = 'en';
const translations = {{
  search: {{ en: 'Search work...', ru: 'Поиск работы...' }}
}};

function toggleLang() {{
  lang = lang === 'en' ? 'ru' : 'en';
  document.querySelectorAll('[data-en]:not(.tile)').forEach(el => {{
    el.textContent = el.getAttribute('data-' + lang);
  }});
  document.getElementById('search').placeholder = translations.search[lang];
}}

let currentImages = [];
let currentIndex = 0;

function renderImage() {{
  document.getElementById('modal-img').src = currentImages[currentIndex] || '';
  const multi = currentImages.length > 1;
  document.getElementById('modal-counter').textContent = multi ? (currentIndex + 1) + ' / ' + currentImages.length : '';
  document.querySelectorAll('.carousel-arrow').forEach(a => a.style.display = multi ? 'flex' : 'none');
}}

function shiftImage(delta) {{
  if (!currentImages.length) return;
  currentIndex = (currentIndex + delta + currentImages.length) % currentImages.length;
  renderImage();
}}

function openCard(tile) {{
  currentImages = JSON.parse(tile.getAttribute('data-images') || '[]');
  currentIndex = 0;
  renderImage();
  document.getElementById('modal-title').textContent = tile.querySelector('.tile-title').textContent;
  document.getElementById('modal-desc').textContent = tile.getAttribute('data-' + lang);
  document.getElementById('modal-meta').textContent =
    (lang === 'en' ? 'Status: ' : 'Статус: ') + tile.getAttribute('data-status-' + lang) +
    ' — ' + (lang === 'en' ? 'Dimensions: ' : 'Размеры: ') + tile.getAttribute('data-dims');
  document.getElementById('modal-bg').classList.add('open');
}}
function closeCard() {{ document.getElementById('modal-bg').classList.remove('open'); }}

let soundOn = true;
let actx;
function beep(freq, dur, vol, type) {{
  if (!soundOn) return;
  if (!actx) actx = new (window.AudioContext || window.webkitAudioContext)();
  const pitch = freq * (0.94 + Math.random() * 0.12);
  const o = actx.createOscillator(), g = actx.createGain();
  o.frequency.value = pitch; o.type = type || 'sine';
  g.gain.setValueAtTime(vol, actx.currentTime);
  g.gain.exponentialRampToValueAtTime(0.001, actx.currentTime + dur);
  o.connect(g); g.connect(actx.destination);
  o.start(); o.stop(actx.currentTime + dur);
}}
document.addEventListener('click', (e) => {{
  if (e.target.closest('.carousel-arrow')) beep(900, 0.07, 0.14, 'triangle');
  else if (e.target.closest('.modal-close')) beep(360, 0.09, 0.13, 'triangle');
  else if (e.target.closest('.tile')) beep(720, 0.1, 0.15);
  else if (e.target.closest('a, button')) beep(540, 0.07, 0.12);
}});

function toggleSound() {{
  const btn = document.getElementById('sound-btn');
  btn.classList.toggle('muted');
  soundOn = !btn.classList.contains('muted');
}}

function filterTiles(query) {{
  query = query.toLowerCase();
  document.querySelectorAll('.tile').forEach(tile => {{
    const match = tile.dataset.title.includes(query);
    tile.classList.toggle('hidden', !match);
  }});
}}
</script>

</body>
</html>'''

with open("prototype-museum-noir.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Generated prototype with {sum(len(v) for v in SECTIONS.values())} works across {len(SECTIONS)} sections")
