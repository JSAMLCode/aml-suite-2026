// uso: node capture.js <html> <h|v> <test|full> [outdir]
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs');
(async () => {
  const [file = 'cinematic.html', ver = 'h', mode = 'test', dir = `frames_${ver}`] = process.argv.slice(2);
  const vert = ver === 'v', W = vert ? 1080 : 1920, H = vert ? 1920 : 1080;
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--allow-file-access-from-files'] });
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  page.on('pageerror', e => console.log('PAGEERR', e.message));
  await page.goto(`file://${process.cwd()}/${file}${vert ? '?v=1' : ''}`);
  await page.waitForFunction('window.ready === true');
  const el = await page.$('#c');
  fs.mkdirSync(dir, { recursive: true });
  const times = mode === 'test'
    ? (process.env.TIMES || '0.3,1.2,2.2,3.15,3.9,4.95,5.1,6.2,7.0,8.0,9.0,10.3,11.1,11.7,12.2,12.8,13.2,14.2').split(',').map(Number)
    : Array.from({ length: 450 }, (_, f) => f / 30);
  for (let i = 0; i < times.length; i++) {
    await page.evaluate(t => render(t), times[i]);
    const name = mode === 'test' ? `t${times[i].toFixed(2)}.png` : `f${String(i).padStart(4, '0')}.png`;
    await el.screenshot({ path: `${dir}/${name}` });
  }
  await browser.close();
})();
