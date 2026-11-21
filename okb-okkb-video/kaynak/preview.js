const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const errs = [];
  page.on('pageerror', e => errs.push(e.message));
  page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await page.goto('file://' + path.resolve('index.html'));
  await page.evaluate(() => document.fonts.ready);
  const scenes = await page.evaluate(() => window.__SCENES);
  const total = await page.evaluate(() => window.__TOTAL);
  console.log('TOTAL', total, 'errors', errs);
  const only = process.argv[2];
  for (const s of scenes) {
    if (only && !s.id.includes(only)) continue;
    const t = s.start + s.d - 0.8;
    await page.evaluate(t => window.__seek(t), t);
    await page.screenshot({ path: `prev/${String(scenes.indexOf(s)).padStart(2,'0')}_${s.id}.png` });
  }
  // overflow check: elements extending beyond stage
  await browser.close();
})();
