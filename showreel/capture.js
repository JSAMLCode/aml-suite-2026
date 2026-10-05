const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs');
(async () => {
  const mode = process.argv[2] || 'test';
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--allow-file-access-from-files'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('pageerror', e => console.log('PAGEERR', e.message));
  await page.goto('file://' + process.cwd() + '/index.html');
  await page.waitForFunction('window.ready === true');
  const el = await page.$('#c');
  if (mode === 'test') {
    fs.mkdirSync('test', { recursive: true });
    for (const t of [1.0, 1.9, 3.6, 4.6, 6.8, 7.8, 9.9, 10.6, 12.2, 14.2]) {
      await page.evaluate(t => render(t), t);
      await el.screenshot({ path: `test/t${t.toFixed(1)}.png` });
    }
  } else {
    fs.mkdirSync('frames', { recursive: true });
    for (let f = 0; f < 450; f++) {
      await page.evaluate(t => render(t), f / 30);
      await el.screenshot({ path: `frames/f${String(f).padStart(4, '0')}.png` });
    }
  }
  await browser.close();
})();
