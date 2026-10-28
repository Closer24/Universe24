"""Draft B's outputs: each probe's raw JSON lines (one per run) written out as text, one block per run.
Usage: python -I bsummary.py <out.txt> <title> <raw1> [<raw2> ...]"""

import json
import sys

out, title, raws = sys.argv[1], sys.argv[2], sys.argv[3:]
lines = [title, "=" * len(title), ""]
for raw in raws:
    for line in open(raw):
        line = line.strip()
        if not line.startswith("{"):
            continue
        r = json.loads(line)
        course = r.pop("course", None)
        lines.append("- " + "; ".join(f"{k}: {v}" for k, v in r.items()))
        for row in course or []:
            lines.append("    " + "; ".join(f"{k}: {v}" for k, v in row.items()))
    lines.append("")
open(out, "w").write("\n".join(lines) + "\n")
print(out, len(lines), "lines")
