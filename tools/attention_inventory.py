"""List everything on each preview page that still needs attention.

Reads preview/*.src.html and prints, per page, every:
  - cx-verify  (yellow "to confirm" copy)
  - cx-blank   (a ____ fact only Catalyst has)
  - cx-ph      (missing photo/asset/link placeholder)
  - cx-temp    (temporary stock image)
Usage: python3 tools/attention_inventory.py [--json]
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def spans(src: str, cls: str) -> list[str]:
    """Text of each element whose class list contains cls (handles nesting)."""
    out = []
    for m in re.finditer(r'<(\w+)[^>]*class="[^"]*\b%s\b[^"]*"[^>]*>' % cls, src):
        tag, depth, i = m.group(1), 1, m.end()
        pat = re.compile(r"<(/?)%s\b[^>]*>" % tag)
        while depth and (n := pat.search(src, i)):
            depth += -1 if n.group(1) else 1
            i = n.end()
        text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", src[m.end():i]))
        out.append(html.unescape(text.replace("</" + tag + ">", "")).strip())
    return out


report = {}
for f in sorted((ROOT / "preview").glob("*.src.html")):
    s = f.read_text()
    report[f.stem.replace(".src", "")] = {
        "to_confirm": spans(s, "cx-verify"),
        "placeholders": spans(s, "cx-ph"),
        "temp_images": len(re.findall(r'class="[^"]*\bcx-temp\b', s)),
    }

if "--json" in sys.argv:
    print(json.dumps(report, indent=2, ensure_ascii=False))
else:
    for page, r in report.items():
        print(f"\n## {page}  ({len(r['to_confirm'])} to confirm, {len(r['placeholders'])} placeholders, {r['temp_images']} temp images)")
        for t in r["to_confirm"]:
            print("  - [confirm]", t[:160])
        for t in r["placeholders"]:
            print("  - [asset]  ", t[:160])
