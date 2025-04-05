const express = require('express');
const puppeteer = require('puppeteer');
const app = express();

const FLAG = process.env.FLAG || 'DDC{test_flag}';
app.use(express.json());

async function visitUrl(url) {
  const browser = await puppeteer.launch({
    headless: true,
    args: [
      '--disable-extensions',
      '--disable-gpu',
      '--disable-software-rasterizer',
      '--js-flags=--noexpose_wasm,--jitless',
      '--no-sandbox',
    ]
  });

  try {
    const page = await browser.newPage();
    await page.setCookie({
        name: 'flag',
        value: FLAG,
        domain: 'theblog.hkn:5000',
        path: '/',
        expires: Date.now() + 1000 * 60 * 60
    });
    await page.goto(url, {
      waitUntil: 'networkidle0',
    });

  } catch (err) {
    console.error('Error visiting page:', err);
  } finally {
    await browser.close();
  }
}

app.post('/report', async (req, res) => {
  const { url } = req.body;

  if (!url || typeof url !== 'string') {
    return res.status(400).json({ error: `Invalid URL. Url should be a string and start with ${XSS_DOMAIN}` });
  }

  try {
    await visitUrl(url);
    res.json({ success: true });
  } catch (err) {
    console.error('Error on /report', err);
    res.status(500).json({ error: 'Failed to visit URL' });
  }
});

const PORT = 5001;
app.listen(PORT, () => {
  console.log(`Adminbot listening on port ${PORT}`);
});