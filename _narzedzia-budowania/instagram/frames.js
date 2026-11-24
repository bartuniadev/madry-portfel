// composes 1080x1920 reel frames: headline band + carousel slide + footer band
const { chromium } = require('playwright'); const fs = require('fs');
const [kdir, outdir] = [process.argv[2], process.argv[3]];
const SETS = { weekendy: [6, 'Jak mieć 28 dni wolnego za 11 dni urlopu w 2027?'], niedziele: [4, 'Kiedy sklepy są otwarte w grudniu?'],
               godziny: [4, 'Ile godzin pracujesz na nowy smartfon?'], l4: [5, 'Ile naprawdę dostaniesz na L4?'] };
const css = `@import url("file:///home/user/madry-portfel/assets/fonts/fonts.css");
body{margin:0} .f{width:1080px;height:1920px;background:#14261c;display:flex;flex-direction:column;align-items:center}
.top{height:285px;width:100%;box-sizing:border-box;padding:0 70px;display:flex;align-items:center;justify-content:center;text-align:center;
 font-family:"Fraunces",serif;font-weight:600;font-size:60px;line-height:1.12;color:#fff;text-wrap:balance}
.top em{font-style:normal;color:#3ad889}
img{width:1080px;height:1350px;display:block}
.bot{height:285px;display:flex;align-items:center;justify-content:center;font-family:"Inter",sans-serif;font-weight:600;font-size:40px;color:#a8b6ae}
.bot b{color:#3ad889;font-weight:600}`;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const [name, [n, head]] of Object.entries(SETS)) {
    for (let i = 1; i <= n; i++) {
      const tmp = `${outdir}/_frame.html`;
      fs.writeFileSync(tmp, `<html><head><meta charset="utf-8"><style>${css}</style></head><body><div class="f"><div class="top">${head}</div><img src="file://${kdir}/${name}-${i}.png"><div class="bot">Zapisz na później · <b>&nbsp;link w bio</b></div></div></body></html>`);
      await p.goto('file://' + tmp);
      await p.evaluate(() => document.fonts.ready); await p.waitForFunction(() => document.querySelector('img').complete);
      await p.screenshot({ path: `${outdir}/${name}-${i}.png` });
    }
  }
  console.log('frames ok'); await b.close();
})();
