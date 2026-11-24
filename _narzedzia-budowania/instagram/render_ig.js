// avatar 1080x1080 + highlight covers 1080x1920, rendered with the site's fonts
const { chromium } = require('playwright');
const out = process.argv[2];
const css = `@import url("file:///home/user/madry-portfel/assets/fonts/fonts.css");
body{margin:0} .a{width:1080px;height:1080px;display:flex;align-items:center;justify-content:center;background:radial-gradient(700px 700px at 70% 25%, #2a6b4a 0%, #14261c 60%, #0d1310 100%)}
.h{width:1080px;height:1920px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:60px;background:#14261c}
.ring{width:880px;height:880px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:radial-gradient(circle at 50% 35%, #1f3a2c, #14261c 70%)}
.lbl{font-family:"Inter",sans-serif;font-weight:600;font-size:72px;color:#eef2ef;letter-spacing:.02em}`;
const logo = s => `<svg width="${s}" height="${s}" viewBox="0 0 24 24" fill="none" stroke="#3ad889" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><polyline points="7.5 13.5 10.5 10.5 13 12.5 16.5 8.5"/><polyline points="14 8.5 16.5 8.5 16.5 11"/><circle cx="18.6" cy="6.4" r="0.75" fill="#e0a63f" stroke="none"/></svg>`;
const icons = {
  kalkulatory: '<rect x="5" y="3" width="14" height="18" rx="2"/><line x1="8" y1="7" x2="16" y2="7"/><circle cx="8.5" cy="11.5" r=".6"/><circle cx="12" cy="11.5" r=".6"/><circle cx="15.5" cy="11.5" r=".6"/><circle cx="8.5" cy="15" r=".6"/><circle cx="12" cy="15" r=".6"/><circle cx="15.5" cy="15" r=".6"/><circle cx="8.5" cy="18" r=".6"/><circle cx="12" cy="18" r=".6"/><circle cx="15.5" cy="18" r=".6"/>',
  pensja: '<rect x="3" y="6" width="18" height="12" rx="2"/><circle cx="12" cy="12" r="2.6"/><line x1="6" y1="9" x2="6" y2="9"/><line x1="18" y1="15" x2="18" y2="15"/>',
  kalendarz: '<rect x="3" y="5" width="18" height="16" rx="2"/><line x1="3" y1="10" x2="21" y2="10"/><line x1="8" y1="3" x2="8" y2="7"/><line x1="16" y1="3" x2="16" y2="7"/><path d="M8 15l2.5 2.5L16 13"/>',
  oszczedzanie: '<path d="M19 9c1.5 0 2 1 2 2v2c0 1-.5 2-2 2l-1 3h-3v-2h-5v2H7l-1-3c-2-1-3-3-3-5 0-3 3-6 8-6 2 0 4 .5 5.5 1.5L19 4v5z"/><circle cx="15.5" cy="10" r=".8"/>',
  podatki: '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="9" y1="12" x2="15" y2="12"/><path d="M9.5 16h5"/>',
};
const labels = {kalkulatory:'Kalkulatory', pensja:'Pensja', kalendarz:'Kalendarz', oszczedzanie:'Oszczędzanie', podatki:'Podatki'};
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1080 } });
  await p.setContent(`<html><head><style>${css}</style></head><body><div class="a">${logo(760)}</div></body></html>`);
  await p.evaluate(() => document.fonts.ready); await p.screenshot({ path: out + '/profilowe.png' });
  await p.setViewportSize({ width: 1080, height: 1920 });
  for (const k of Object.keys(icons)) {
    await p.setContent(`<html><head><style>${css}</style></head><body><div class="h"><div class="ring"><svg width="540" height="540" viewBox="0 0 24 24" fill="none" stroke="#3ad889" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round">${icons[k]}</svg></div></div></body></html>`);
    await p.evaluate(() => document.fonts.ready); await p.screenshot({ path: out + '/wyroznione-' + k + '.png' });
  }
  console.log('ok'); await b.close();
})();
