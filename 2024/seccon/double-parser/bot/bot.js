import puppeteer from "puppeteer";

const FLAG = process.env.FLAG ?? console.log("No flag") ?? process.exit(1);

const APP_HOST = "web";
const APP_PORT = "3000";
export const APP_URL = `http://${APP_HOST}:${APP_PORT}`;

// Flag format
if (!/^SECCON{\w+}$/.test(FLAG)) {
  console.log("Bad flag");
  process.exit(1);
}

const sleep = async (ms) => new Promise((resolve) => setTimeout(resolve, ms));

export const visit = async (url) => {
  console.log(`start: ${url}`);

  const browser = await puppeteer.launch({
    headless: "new",
    executablePath: "/usr/bin/chromium",
    args: [
      "--no-sandbox",
      "--disable-dev-shm-usage",
      "--disable-gpu",
      '--js-flags="--noexpose_wasm"',
    ],
  });

  const context = await browser.createBrowserContext();

  try {
    const page = await context.newPage();
    await page.setCookie({
      name: "FLAG",
      value: FLAG,
      domain: APP_HOST,
      path: "/",
    });
    await page.goto(url, { timeout: 3_000 });
    await sleep(5_000);
    await page.close();
  } catch (e) {
    console.error(e);
  }

  await context.close();
  await browser.close();

  console.log(`end: ${url}`);
};


export const fuzz = async () => {
  // get payloads and results from the web server as JSON on the /fuzz endpoint
  const res = await fetch(`${APP_URL}/fuzz`);
  // result is a list of dict with "payload" and "result" keys
  const results = await res.json();

  console.log(`starting fuzzing: ${results.length} urls`);
  //console.log(results);

  const browser = await puppeteer.launch({
    headless: "new",
    executablePath: "/usr/bin/chromium",
    args: [
      "--no-sandbox",
      "--disable-dev-shm-usage",
      "--disable-gpu",
      '--js-flags="--noexpose_wasm"',
    ],
  });

  const context = await browser.createBrowserContext();

  for (const result of results) {
    console.log();
    console.log("start:\t\t", result.payload);
    //console.log();
    try {
      const page = await context.newPage();
      await page.setCookie({
        name: "FLAG",
        value: FLAG,
        domain: APP_HOST,
        path: "/",
      });

      const url_safe_html = encodeURIComponent(result.payload);
      await page.goto(`${APP_URL}?html=${url_safe_html}`, { timeout: 3_000 });

      // instead of sleeping, wait for the page to load, but max 5 seconds
      await page.waitForSelector("html", { timeout: 5_000 });

      // for debugging, print the page content
      const content = await page.content();
      console.log("content:\t", content);

      // If a script element or an iframe element is found, report it
      const hasDangerousTag = await page.evaluate(() => {
        const DANGEROUS_TAGS = [
          "script",
          "noscript",
          "iframe",
          "frame",
          "object",
          "embed",
          "template",
          "meta",
          "svg",
          "math",
        ];
        const selected = DANGEROUS_TAGS.some((tag) => document.querySelector(tag));
        return selected;
      });

      // and not "Invalid cha"
      if (hasDangerousTag) {
        console.log(`Dangerous tag found in: ${result.payload} - ${content}`);
      }

      await page.close();
    } catch (e) {
      console.log(`Error for: ${result.payload}`);
      console.error(e);
    }
    //console.log(`end: ${html}`);
  }

  console.log("end fuzzing");

  await context.close();
  await browser.close();
};