from __future__ import annotations
import datetime as dt
import html
import json
from pathlib import Path
from .. import APP_NAME, APP_VERSION, AUTHOR
from ..core.paths import reports_dir


def write_json_report(name: str, data: dict) -> Path:
    out = reports_dir() / f"{name}.json"
    payload = {
        "tool": APP_NAME,
        "version": APP_VERSION,
        "author": AUTHOR,
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "data": data,
    }
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return out


def write_html_lab_report(name: str, data: dict, notes: str = "") -> Path:
    out = reports_dir() / f"{name}.html"
    artifacts = data.get("artifacts", [])
    rows = ""
    for a in artifacts:
        rows += f"<tr><td><code>{html.escape(str(a))}</code></td></tr>"

    doc = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>LABYRINTH Report</title>
<style>
body{{background:#05070b;color:#e8f6ff;font-family:Consolas,Segoe UI,Arial;padding:32px}}
h1,h2{{color:#ff304f}} .card{{background:#0b1018;border:1px solid #1d2a3c;border-radius:16px;padding:18px;margin:18px 0}}
table{{width:100%;border-collapse:collapse}} td,th{{border-bottom:1px solid #1d2a3c;padding:10px;text-align:left}}
code{{color:#d6f7ff}} .muted{{color:#9fb1c7}}
</style>
</head>
<body>
<h1>LABYRINTH</h1>
<p class="muted">Local Defensive Training Lab · xtr4ng3 · {dt.datetime.now().isoformat(timespec="seconds")}</p>
<div class="card">
<h2>{html.escape(str(data.get("name","Lab Case")))}</h2>
<p><b>Lab ID:</b> <code>{html.escape(str(data.get("lab_id","")))}</code></p>
<p><b>Objective:</b> {html.escape(str(data.get("objective","")))}</p>
<p><b>Difficulty:</b> {html.escape(str(data.get("difficulty","")))}</p>
<p><b>Category:</b> {html.escape(str(data.get("category","")))}</p>
</div>
<div class="card">
<h2>Artifacts</h2>
<table>{rows}</table>
</div>
<div class="card">
<h2>Notes</h2>
<pre>{html.escape(notes)}</pre>
</div>
</body>
</html>"""
    out.write_text(doc, encoding="utf-8")
    return out
