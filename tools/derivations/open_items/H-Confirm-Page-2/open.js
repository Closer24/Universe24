const { chromium } = require('playwright'); const path = process.argv[2];
(async () => { const b = await chromium.launch(); const p = await b.newPage(); let errors = 0, warnings = 0, pageerrors = 0;
p.on('console', m => { if (m.type() === 'error') { errors++; console.log('CONSOLE ERROR:', m.text().slice(0, 200)); } else if (m.type() === 'warning') warnings++; });
p.on('pageerror', e => { pageerrors++; console.log('PAGE ERROR:', String(e).slice(0, 200)); });
await p.goto('file://' + path, { waitUntil: 'load' }); await p.waitForTimeout(3000);
const n = await p.evaluate(() => ({ canvases: document.querySelectorAll('canvas').length, labels: document.querySelectorAll('.label').length, title: document.title, header: (document.querySelector('#header') || {}).textContent || '' }));
console.log(JSON.stringify({ errors, warnings, pageerrors, ...n, header: n.header.slice(0, 400) })); await b.close(); })().catch(e => { console.log('FAIL', String(e)); process.exit(2); });
