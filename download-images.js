const fs = require('fs');
const path = require('path');
const { execFile } = require('child_process');
const { promisify } = require('util');
const execFileAsync = promisify(execFile);

const manifest = JSON.parse(fs.readFileSync(path.join(__dirname, 'download-manifest.json'), 'utf8'));
const rawDir = path.join(__dirname, 'images-raw');
const outDir = path.join(__dirname, 'images');
fs.mkdirSync(rawDir, { recursive: true });
fs.mkdirSync(outDir, { recursive: true });

async function downloadOne(item) {
  const rawPath = path.join(rawDir, item.filename);
  const outPath = path.join(outDir, item.filename);
  if (fs.existsSync(outPath)) return { ok: true, skipped: true, filename: item.filename };

  const res = await fetch(item.url);
  if (!res.ok) return { ok: false, filename: item.filename, error: `HTTP ${res.status}` };
  const buf = Buffer.from(await res.arrayBuffer());
  fs.writeFileSync(rawPath, buf);

  try {
    await execFileAsync('ffmpeg', [
      '-y', '-i', rawPath,
      '-vf', "scale='min(1100,iw)':'-2'",
      '-q:v', '4',
      outPath,
    ]);
  } catch (e) {
    return { ok: false, filename: item.filename, error: e.message };
  } finally {
    fs.unlinkSync(rawPath);
  }
  return { ok: true, filename: item.filename };
}

async function run() {
  const concurrency = 6;
  let idx = 0;
  const results = [];
  async function worker() {
    while (idx < manifest.length) {
      const item = manifest[idx++];
      const r = await downloadOne(item).catch(e => ({ ok: false, filename: item.filename, error: e.message }));
      results.push(r);
      process.stdout.write(`${results.length}/${manifest.length} ${r.ok ? 'OK' : 'FAIL'} ${r.filename}${r.error ? ' - ' + r.error : ''}\n`);
    }
  }
  await Promise.all(Array.from({ length: concurrency }, worker));
  fs.rmSync(rawDir, { recursive: true, force: true });
  const failed = results.filter(r => !r.ok);
  console.log(`\nDone. ${results.length - failed.length}/${results.length} succeeded.`);
  if (failed.length) console.log('Failed:', JSON.stringify(failed, null, 2));
}

run();
