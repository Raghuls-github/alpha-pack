const express = require("express");
const { execFile } = require("child_process");

const app = express();
app.use(express.json());

const SAFE_ARG = /^[A-Za-z0-9._\/][A-Za-z0-9._\/-]*$/;

// Dock staff paste a printer name; it is passed as an argv entry, never through a shell.
app.post("/print", (req, res) => {
  const { printer, file } = req.body || {};
  if (typeof printer !== "string" || typeof file !== "string" || !SAFE_ARG.test(printer) || !SAFE_ARG.test(file)) {
    return res.status(400).json({ ok: false, error: "invalid printer or file" });
  }
  execFile("lp", ["-d", printer, file], (err, out) => res.json({ ok: !err, out }));
});

const UNSAFE_KEYS = new Set(["__proto__", "constructor", "prototype"]);
function stripUnsafeKeys(value) {
  if (Array.isArray(value)) return value.map(stripUnsafeKeys);
  if (value === null || typeof value !== "object") return value;
  const out = {};
  for (const key of Object.keys(value)) {
    if (!UNSAFE_KEYS.has(key)) out[key] = stripUnsafeKeys(value[key]);
  }
  return out;
}

// Overlay user-supplied preferences on defaults (defaults are flat), dropping prototype-polluting keys.
app.post("/prefs", (req, res) => res.json({ theme: "light", ...stripUnsafeKeys(req.body) }));

app.listen(3000);
