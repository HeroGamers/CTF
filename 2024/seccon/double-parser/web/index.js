import fastify from "fastify";
import * as cheerio from "cheerio";
import fs from "node:fs";

const app = fastify();
const DEBUG = false;

// Do not use dangerous tags.
const validateTags = ($) => {
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
  const selected = $(DANGEROUS_TAGS.join(","));

  if (selected.length > 0 && DEBUG) {
    // print selected tags for debugging
    console.log("selected tags:\t\t\t", selected.toArray().map((el) => el.name));
  }

  return selected.length === 0;
};

const validate = (html0) => {
  // newline for debug
  if (DEBUG) console.log();
  if (DEBUG) console.log("html0:\t\t\t\t", html0);

  if (typeof html0 !== "string") throw "Invalid type";
  if (html0.length > 1024) throw "Too long";
  // get invalid characters for debugging
  
  const invalidChars = html0.match(/[^\r\n\x20-\x7e]/);
  if (invalidChars && DEBUG) console.log("invalidChars:\t\t\t", invalidChars);

  if (/[^\r\n\x20-\x7e]/.test(html0)) throw "Invalid characters";

  // Parser 1: parse5
  // ref. https://cheerio.js.org/docs/advanced/configuring-cheerio#parsing-html-with-parse5
  const $1 = cheerio.load(html0);
  const html1 = $1.html();

  // debug
  const _alt_html1 = cheerio.load(html0, { xml: { xmlMode: false } }).html();
  if (html1 !== _alt_html1 && DEBUG) console.log("[debug] html1 (htmlparser2):\t", _alt_html1);
  if (DEBUG) console.log("html1 (parse5):\t\t", html1);

  // Parser 2: htmlparser2
  // ref. https://cheerio.js.org/docs/advanced/configuring-cheerio#using-htmlparser2-for-html
  const $2 = cheerio.load(html1, { xml: { xmlMode: false } });
  const html2 = $2.html();
  if (html2 !== html1 && DEBUG) console.log("html2 (htmlparser2):\t\t", html2);

  if (!validateTags($1) && !validateTags($2)) throw "Invalid tags: Parser 1 & Parser 2";
  if (!validateTags($1)) throw "Invalid tags: Parser 1";
  if (!validateTags($2)) throw "Invalid tags: Parser 2";

  if (DEBUG) console.log("success");

  return html2;
};

const defaultHtml = fs.readFileSync("index.html", { encoding: "utf8" });

app.get("/", async (req, reply) => {
  try {
    const html = validate(req.query.html ?? defaultHtml);
    reply
      .type("text/html; charset=utf-8")
      .header("Content-Security-Policy", "script-src 'self'")
      .send(html);
  } catch (err) {
    reply.type("text/plain").code(400).send(err);
  }
});

app.get("/fuzz", async (req, reply) => {
  const results = [];

  // Load the "payload-list.txt" file, and try to run validate() with each line.
  const payloads = fs.readFileSync("payload-list.txt", { encoding: "utf8" }).split("\n");
  for (const payload of payloads) {
    if (payload.length === 0) continue;
    try {
      const result = validate(payload);
      // if not start with <html><head>, add it
      //if (!result.startsWith("<html")) {
        results.push({ payload, result });
      //}
    } catch (err) {
      //results.push(err);
    }
  }

  reply.type("application/json").send(results);
});

app.listen({ port: 3000, host: "0.0.0.0" });
