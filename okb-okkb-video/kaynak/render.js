// usage: node render.js <worker> <nworkers> <fps> [maxFrames]
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const [W, N, FPS, MAXF] = process.argv.slice(2).map(Number);
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve('index.html'));
  await page.evaluate(() => document.fonts.ready);
  const total = await page.evaluate(() => window.__TOTAL);
  let nFrames = Math.round(total * FPS);
  if (MAXF) nFrames = Math.min(nFrames, MAXF);
  const per = Math.ceil(nFrames / N);
  const a = W * per, b = Math.min(nFrames, a + per);
  const ff = spawn('ffmpeg', ['-y','-loglevel','error','-f','image2pipe','-framerate',String(FPS),'-c:v','png','-i','-',
    '-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p','-tune','animation','-r',String(FPS), `segs/seg_${W}.mp4`], { stdio: ['pipe','inherit','inherit'] });
  const t0 = Date.now();
  for (let f = a; f < b; f++) {
    await page.evaluate(t => window.__seek(t), f / FPS);
    const buf = await page.screenshot({ type: 'png' });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if ((f - a) % 300 === 0) console.log(`w${W} ${f - a}/${b - a} ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  console.log(`w${W} done frames ${a}-${b} in ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  await browser.close();
})();
