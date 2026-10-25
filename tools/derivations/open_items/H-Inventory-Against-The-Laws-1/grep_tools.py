"""Inventory of tools/: line counts per file, float and division hits, LATTICE and interval readers."""
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
TOOLS = ROOT / "tools"
FLOAT = re.compile(
    r"math\.(log|exp|sqrt|log2|log10)|np\.(log|exp|sqrt|log2|log10|float64|float_)|"
    r"\bfloat\(|\bfloat\b|\bsqrt\b|\bexp\(|\blog\(|\blog2\(|\blog10\(|\bround\(|"
    r"\bFraction\b|\bDecimal\b"
)
SLASH = re.compile(r"[^/\"'#*]\s/\s[^/\"']|[A-Za-z0-9_\)\]]\s*/\s*[A-Za-z0-9_\(]")  # a true division, not // and not a comment or a URL
LATTICE = re.compile(r"LATTICE|\"lattice\"|'lattice'|\binterval\b")
WORLDS = re.compile(r"\bslits?\b|\batom\b|\bbell\b|\bghz\b|\bclicks\b|\bbodies\b|\bpackets?\b|node_detectors|\bdetector", re.I)
rows = []
for path in sorted(TOOLS.rglob("*.py")):
    if "__pycache__" in path.parts:
        continue
    text = path.read_text(errors="replace")
    lines = text.splitlines()
    code = [l for l in lines]
    flo = [i + 1 for i, l in enumerate(lines) if FLOAT.search(l.split("#")[0])]
    sla = [
        i + 1
        for i, l in enumerate(lines)
        if "/" in l.split("#")[0]
        and "//" not in l.split("#")[0]
        and "http" not in l
        and '"""' not in l
        and SLASH.search(l.split("#")[0])
    ]
    lat = [i + 1 for i, l in enumerate(lines) if LATTICE.search(l)]
    wor = [i + 1 for i, l in enumerate(lines) if WORLDS.search(l)]
    rows.append((str(path.relative_to(ROOT)), len(lines), len(flo), len(sla), len(lat), len(wor), flo[:8], sla[:8]))
tot = [0] * 5
for r in rows:
    for k in range(5):
        tot[k] += r[1 + k]
print("file | lines | float-hits | slash-div | LATTICE/interval | worlds-words | float lines | slash lines")
for r in rows:
    print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} | {r[7]}")
print("TOTAL", tot)
# non-py files under tools: count lines by folder
by_dir: dict[str, list[int]] = {}
for path in sorted(TOOLS.rglob("*")):
    if path.is_file() and path.suffix != ".py" and "__pycache__" not in path.parts:
        key = str(path.parent.relative_to(ROOT))
        n = sum(1 for _ in path.open(errors="replace"))
        by_dir.setdefault(key, [0, 0])
        by_dir[key][0] += 1
        by_dir[key][1] += n
print("NON-PY by folder: folder | files | lines")
for k, (f, n) in sorted(by_dir.items()):
    print(f"{k} | {f} | {n}")
