// node dom.js <page.html> <out_prefix> <intervals...>: opens the page headless, seeks each interval (playing=false; t=seek(k); draw()),
// reads the readout, the labels, the bar's names and eras, collects console and page errors, saves a PNG per interval and one JSON.
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const [, , page, out, ...ivs] = process.argv;
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 960 } });
  const console_lines = [], errors = [];
  p.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') console_lines.push(m.type() + ': ' + m.text()); });
  p.on('pageerror', e => errors.push(String(e)));
  await p.goto('file://' + page); await p.waitForTimeout(1200);
  const fixed = await p.evaluate(() => ({
    bytes_of_data: document.getElementById('data').textContent.length,
    clicks_first_three: D.clicks.slice(0, 3), bangs_found: bangs, n_lines: n, stride: D.stride,
    bar_names: Array.from(document.querySelectorAll('#bar .name')).map(e => e.textContent),
    eras: Array.from(document.querySelectorAll('#bar .era')).map(e => e.title),
    ticks: document.querySelectorAll('#bar .tick').length,
    header: document.getElementById('head').textContent,
  }));
  const frames = [];
  for (const iv of ivs) {
    const k = parseInt(iv, 10);
    const got = await p.evaluate((k) => { playing = false; t = seek(k); draw();
      return { asked: k, readout: document.getElementById('where').textContent,
        labels: Array.from(document.querySelectorAll('#labels .label')).map(e => e.innerText.replace(/\n/g, ' | ')) }; }, k);
    await p.waitForTimeout(300);
    const png = out + '_' + String(k).padStart(3, '0') + '.png';
    await p.screenshot({ path: png }); got.png = png; frames.push(got);
  }
  fs.writeFileSync(out + '.dom.json', JSON.stringify({ fixed, frames, console_lines, errors }, null, 1));
  console.log(JSON.stringify({ errors, console_lines, frames: frames.map(f => ({ asked: f.asked, readout: f.readout, labels: f.labels })), bar_names: fixed.bar_names, eras: fixed.eras, ticks: fixed.ticks, clicks_first_three: fixed.clicks_first_three, bangs_found: fixed.bangs_found }, null, 1));
  await b.close();
})();
