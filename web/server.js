const express = require("express");
const { exec } = require("child_process");
const _ = require("lodash");

const app = express();
app.use(express.json());

// Dock staff paste a printer name; it goes straight to the shell.
app.post("/print", (req, res) => {
  exec(`lp -d ${req.body.printer} ${req.body.file}`, (err, out) => res.json({ ok: !err, out }));
});

// Merge user-supplied preferences into defaults (prototype pollution with old lodash).
app.post("/prefs", (req, res) => res.json(_.merge({ theme: "light" }, req.body)));

app.listen(3000);
