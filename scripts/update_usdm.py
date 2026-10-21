#!/usr/bin/env python3
"""Refresh the drought map in index.html with a new U.S. Drought Monitor file.

Usage:
    python scripts/update_usdm.py path/to/usdm_current.json "Oct 20, 2026"

The first argument is the GeoJSON from
https://droughtmonitor.unl.edu/data/json/usdm_current.json and the second is
the map's "valid" date (the Tuesday printed on the USDM site). The script
simplifies the shapes with mapshaper (run through npx, so Node.js is needed),
embeds the result in index.html and updates the date shown on the page.
"""
import json
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src = pathlib.Path(sys.argv[1]).resolve()
    valid = sys.argv[2].strip()
    if not src.is_file():
        sys.exit(f"File not found: {src}")

    with tempfile.TemporaryDirectory() as tmp:
        out = pathlib.Path(tmp) / "usdm.topo.json"
        subprocess.run(
            ["npx", "--yes", "mapshaper@0.6.102", str(src),
             "-filter-fields", "DM",
             "-simplify", "10%", "weighted", "keep-shapes",
             "-rename-layers", "usdm",
             "-o", str(out), "format=topojson", "quantization=30000"],
            check=True,
            shell=sys.platform == "win32",
        )
        topo = out.read_text().strip()

    levels = sorted(g["properties"]["DM"] for g in json.loads(topo)["objects"]["usdm"]["geometries"])
    html = INDEX.read_text(encoding="utf-8")

    html, n = re.subn(
        r'(<script id="usdmData" type="application/json">).*?(</script>)',
        lambda m: m.group(1) + topo + m.group(2),
        html, count=1, flags=re.S)
    if n != 1:
        sys.exit("Could not find the usdmData block in index.html")

    old = re.search(r"const USDM_VALID = '([^']*)';", html)
    if not old:
        sys.exit("Could not find USDM_VALID in index.html")
    html = html.replace(old.group(1), valid)

    INDEX.write_text(html, encoding="utf-8")
    print(f"Updated index.html: levels {levels}, valid {valid} (was {old.group(1)}), {len(topo) // 1024} KB of map data")


if __name__ == "__main__":
    main()
