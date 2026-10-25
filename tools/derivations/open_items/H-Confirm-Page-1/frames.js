const { chromium } = require('playwright');
(async () => {
  const [, , page, out, ...ivs] = process.argv;
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 960 } });
  await p.goto('file://' + page); await p.waitForTimeout(1200);
  for (const iv of ivs) {
    await p.evaluate((k) => { playing = false; t = seek(k); draw(); }, parseInt(iv, 10));
    await p.waitForTimeout(300);
    await p.screenshot({ path: out + '_' + String(iv).padStart(3, '0') + '.png' });
  }
  await b.close();
})();
