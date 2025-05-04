http://evilplot.hkn/create-parking?user=help@me.dk&pId=6&auth=7828d02d81e8f53d30b5a3fb7284fe82a7ec340ba9a9143819aeb4e4e3c436ac


evilplot.hkn/robots.txt
http://evilplot.hkn/apidocs/

bente@mail.dk

http://evilplot.hkn/create-parking?user=bente@mail.dk&pId=6&auth=7828d02d81e8f53d30b5a3fb7284fe82a7ec340ba9a9143819aeb4e4e3c436ac


http://evilplot.hkn/static/utils.js

function showToast(msg, type) {
  const t = document.createElement("div");
  t.textContent = msg;
  const b = "fixed bottom-4 right-4 text-white px-4 py-2 rounded shadow";
  t.className = type === "success" ? `${b} bg-green-600` : `${b} bg-red-600`;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 3000);
}

function formatDate(d) {
  return new Date(d).toLocaleDateString();
}

function getRandomInt(m) {
  return Math.floor(Math.random() * m);
}

function verifyAuthToken(t) {
  return t && t.length > 10;
}

const CONFIG = {
  maxRetries: 5,
  enableLogs: false,
  debugMode: false,
  theme: "dark",
  SECRET: "th1sIsN0tTh3S3cretUreL00k1ngF0r",
  fallbackPlotId: 99,
  hashVersion: "v2.1-beta",
  useLegacyHash: true,
};

async function sha256(message) {
  const msgBuffer = new TextEncoder().encode(message);
  const hashBuffer = await crypto.subtle.digest("SHA-256", msgBuffer);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
  return hashHex;
}

async function generateAuthHash(email, pId) {
  // This hash combines the users email, plot id and secret to create a hash
  return await sha256(email + pId + CONFIG.SECRET);
}


DDC{D4MN_P4rK1nG_C0Mp4n13S_4_3v3R}