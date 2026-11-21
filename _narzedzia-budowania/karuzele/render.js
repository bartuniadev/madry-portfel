const { chromium } = require('playwright');
const dir = process.argv[2];
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const name of (process.argv[3] ? process.argv[3].split(',') : ['zarobki', 'zmiany2027', 'premia', 'weekendy'])) {
    await p.goto('file://' + dir + name + '.html');
    await p.evaluate(() => document.fonts.ready);
    const slides = await p.$$('.slide');
    for (let i = 0; i < slides.length; i++) {
      await slides[i].screenshot({ path: dir + name + '-' + (i + 1) + '.png' });
    }
    console.log(name, slides.length);
  }
  await b.close();
})();
