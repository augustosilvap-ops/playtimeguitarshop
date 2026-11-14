// Renderiza cada elemento .art[data-out] de um HTML em PNG no tamanho exato.
// Uso: node render.js pecas/01_custos.html [outros.html...]
// O caminho de saída (data-out) é relativo à pasta augusto/.
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 2000 }, deviceScaleFactor: 1 });
  for (const f of process.argv.slice(2)) {
    await page.goto('file://' + path.resolve(f));
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(300);
    const arts = await page.$$('.art[data-out]');
    for (const el of arts) {
      const out = path.resolve(__dirname, '..', await el.getAttribute('data-out'));
      fs.mkdirSync(path.dirname(out), { recursive: true });
      const transp = (await el.getAttribute('data-transparent')) === '1';
      await page.evaluate(t => { document.documentElement.style.background = t ? 'transparent' : ''; document.body.style.background = t ? 'transparent' : ''; }, transp);
      await el.screenshot({ path: out, omitBackground: transp });
      console.log('ok', path.relative(path.resolve(__dirname, '..'), out));
    }
  }
  await browser.close();
})();
