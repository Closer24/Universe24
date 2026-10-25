"""Grep src for the terms the laws forbid; print file:line counts per term."""
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
SRC = ROOT / "src" / "event_universe"
TERMS = {
    "family.wronskian": r"\.wronskian\b",
    "family.quanta": r"\.quanta\b",
    "family.motion_volume": r"motion_volume",
    "world.seed": r"\bseed\b",
    "registry": r"\bregistry\.",
    "FamilyRule": r"FamilyRule",
    "families": r"\bfamilies\b",
    "family": r"\bfamily\b",
    "identity": r"\bidentity\b",
    "names": r"\bnames?\b",
    "reads": r"\breads\b",
    "weights": r"\bweights?\b",
    "held": r"\bheld\b",
    "sources": r"\bsources\b",
    "dimension": r"\bdimension\b",
    "exchange": r"\bexchange\b",
    "senses": r"\bsenses\b",
    "bodies": r"\bbod(y|ies)\b",
    "packets": r"\bpackets?\b",
    "node_detectors": r"node_detectors|detector",
    "lay": r"\blay\b|\blaid\b",
    "faces": r"\bfaces?\b",
    "boundary": r"\bboundary\b",
    "face_depth": r"face_depth",
    "receding": r"\breceding\b",
    "mode": r"\bmode\b",
    "GONE": r"GONE",
    "link_unit": r"link_unit",
    "slits/atom/bell/ghz/clicks": r"\bslits?\b|\batom\b|\bbell\b|\bghz\b|clicks_world",
    "float": r"\bfloat\b|math\.(log|exp|sqrt)|np\.(log|exp|sqrt)|\bsqrt\b",
    "circle": r"circle",
    "lift": r"\blifts?\b",
    "species": r"species",
    "record": r"\brecords?\b",
    "periodic": r"periodic",
    "shear": r"shear",
    "emission": r"emission|emitted",
    "charge": r"\bcharge",
    "LATTICE": r"LATTICE",
    "interval key": r'"interval"',
}
files = sorted(p for p in SRC.rglob("*.py") if "__pycache__" not in p.parts)
per_term: dict[str, dict[str, list[int]]] = {t: {} for t in TERMS}
for path in files:
    lines = path.read_text().splitlines()
    rel = str(path.relative_to(ROOT))
    for term, rx in TERMS.items():
        pat = re.compile(rx)
        hits = [i + 1 for i, line in enumerate(lines) if pat.search(line)]
        if hits:
            per_term[term][rel] = hits
for term in TERMS:
    total = sum(len(v) for v in per_term[term].values())
    print(f"== {term}: {total} lines in {len(per_term[term])} files")
    for rel, hits in sorted(per_term[term].items()):
        shown = ",".join(str(h) for h in hits[:14])
        more = "" if len(hits) <= 14 else f",... ({len(hits)})"
        print(f"   {rel}: {shown}{more}")
