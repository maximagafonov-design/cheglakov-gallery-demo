const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');

function load(file) {
  return JSON.parse(JSON.parse(fs.readFileSync(path.join(root, file), 'utf8')));
}

function parseDescr(html) {
  let text = html
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<a[^>]*>(.*?)<\/a>/gi, '$1')
    .replace(/<[^>]+>/g, '')
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&');

  const lines = text.split('\n').map(l => l.trim()).filter(Boolean);

  let dimensions = null, weight = null, status = null, price = null;
  const descrLines = [];

  for (const line of lines) {
    let m;
    if ((m = line.match(/^Dimensions:\s*(.*)$/i))) { dimensions = m[1].trim(); continue; }
    if ((m = line.match(/^Weight:\s*(.*)$/i))) { weight = m[1].trim(); continue; }
    if ((m = line.match(/^Status:\s*(.*)$/i))) { status = m[1].trim(); continue; }
    if ((m = line.match(/^Price:\s*(.*)$/i))) { price = m[1].trim(); continue; }
    descrLines.push(line);
  }

  return {
    description: descrLines.join(' '),
    dimensions: dimensions && dimensions !== '—' ? dimensions : null,
    weight: weight && weight !== '—' ? weight : null,
    status: status || null,
    price: price || null,
  };
}

function slugify(title, usedSlugs) {
  let slug = title
    .toLowerCase()
    .normalize('NFKD').replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
  if (!slug) slug = 'work';
  let finalSlug = slug;
  let i = 2;
  while (usedSlugs.has(finalSlug)) {
    finalSlug = `${slug}-${i}`;
    i++;
  }
  usedSlugs.add(finalSlug);
  return finalSlug;
}

const mainWorks = load('works-main.json').map(w => ({ ...w, section: 'main' }));
const archiveWorks = load('works-archive.json').map(w => ({ ...w, section: 'archive' }));
const all = [...mainWorks, ...archiveWorks];

const usedSlugs = new Set();
const downloadManifest = [];

const data = all.map(w => {
  const parsed = parseDescr(w.descrHtml);
  const slug = slugify(w.title, usedSlugs);
  const ext = (w.cover.match(/\.(jpe?g|png|webp)$/i) || ['', 'jpg'])[1].toLowerCase().replace('jpeg', 'jpg');
  const filename = `${slug}.${ext || 'jpg'}`;
  downloadManifest.push({ url: w.cover, filename });
  return {
    title: w.title,
    image: `images/${filename}`,
    ...parsed,
    status: parsed.status || 'Available',
  };
});

fs.writeFileSync(path.join(__dirname, 'data.json'), JSON.stringify(data, null, 2));
fs.writeFileSync(path.join(__dirname, 'download-manifest.json'), JSON.stringify(downloadManifest, null, 2));

console.log('Works:', data.length);
console.log('Sample:', JSON.stringify(data[0], null, 2));
console.log('Sample with no dims:', JSON.stringify(data.find(d => !d.dimensions), null, 2));
