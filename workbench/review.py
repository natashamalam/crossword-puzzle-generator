"""Build a local review page: review.py <prefix|book> <out.html>  (e.g. hard generated_content/hard_review.html, or book for the applied puzzles)"""
import sys, json, glob, html, os
prefix, out = sys.argv[1], sys.argv[2]
files = sorted(glob.glob("data/puzzles/*.json")) if prefix == "book" else sorted(glob.glob(f"drafts/{prefix}-[0-9][0-9].json"))
start = 0 if prefix == "book" else len(glob.glob("data/puzzles/*.json"))  # drafts become the next puzzle numbers, in order
base = os.path.dirname(os.path.abspath(out))
rel = lambda p: os.path.relpath(os.path.abspath(p), base)
h = ["<!doctype html><meta charset=utf-8><title>Draft review</title><style>body{font:15px system-ui;max-width:1100px;margin:20px auto;padding:0 16px}",
     "h2{margin:36px 0 8px;border-top:2px solid #333;padding-top:12px}.row{display:flex;gap:24px;flex-wrap:wrap}",
     "table.g{border-collapse:collapse}table.g td{width:34px;height:34px;border:1px solid #bbb;text-align:center;font-weight:700;position:relative;padding:0}",
     "table.g td.f{background:#fff}table.g td.e{background:#333;border-color:#333}table.g td sup{position:absolute;left:2px;top:0;font-size:9px;font-weight:400}",
     ".cards{display:flex;flex-wrap:wrap;gap:10px}.c{width:150px;font-size:12px}.c img{width:150px;height:150px;border:1px solid #ccc}",
     ".c b{display:block}</style>"]
for k, f in enumerate(files, 1):
    d = json.load(open(f)); pid = f"Puzzle {start + k}"
    n = d["size"]; cells = d["cells"]; st = {tuple(s) for s in d["starters"]}
    num = {(p["row"], p["col"]): p["number"] for p in d["placed"]}
    h.append(f"<h2>{pid} &middot; {len(d['placed'])} words</h2><div class=row>")
    h.append("<table class=g>")
    for r in range(n):
        h.append("<tr>")
        for c in range(n):
            ch = cells[r][c]
            if ch == ".": h.append("<td class=e></td>"); continue
            sup = f"<sup>{num[(r,c)]}</sup>" if (r, c) in num else ""
            h.append(f"<td class=f>{sup}{ch if (r,c) in st else ''}</td>")
        h.append("</tr>")
    h.append("</table><div class=cards>")
    for p in sorted(d["placed"], key=lambda p: p["number"]):
        d_ = "across" if p["across"] else "down"
        h.append(f"<div class=c><img src='{html.escape(rel(p['image']))}'><b>{p['number']} {d_} ({len(p['word'])})</b>{html.escape(p['word'])}<br><i>{html.escape(p['category'])}</i>: {html.escape(p['clue'])}</div>")
    h.append("</div></div>")
os.makedirs(base, exist_ok=True)
open(out, "w").write("\n".join(h)); print(out, len(files))
