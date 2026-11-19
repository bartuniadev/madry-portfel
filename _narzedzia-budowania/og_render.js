const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const items = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  await p.goto('file://' + process.argv[3]); await p.evaluate(() => document.fonts.ready);
  for (const it of items) {
    await p.evaluate(([e, t, s]) => window.render(e, t, s), [it.eyebrow, it.title, it.sub]);
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: it.out, type: 'png' });
  }
  console.log('rendered', items.length); await b.close();
})();
