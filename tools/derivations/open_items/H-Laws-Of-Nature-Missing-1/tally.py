"""Tally the standing and priority columns of TABLE.md (integers only, no float)."""
import sys
from collections import Counter

path = sys.argv[1]
rows = []
for line in open(path, encoding="ascii"):
    if not line.startswith("| "):
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) != 8 or not cells[0].isdigit():
        continue
    rows.append(cells)

standing = Counter(r[7] for r in rows)
priority = Counter(r[6] for r in rows)
print("rows", len(rows))
print("standing: clause and row (CR)", standing["CR"])
print("standing: clause, no row (CN)", standing["CN"])
print("standing: no clause, no row (NN)", standing["NN"])
print("standing: a finding, the law refuses or reads differently (F)", standing["F"])
for p in ("1", "2", "3", "0"):
    print("priority", p, priority[p])
print("verdict column, rows whose state names SHOWN on at least one record",
      sum(1 for r in rows if "SHOWN on" in r[4] and not r[4].startswith("NOT")) )
print("verdict column, rows with no row of the gates (none)",
      sum(1 for r in rows if r[3].startswith("none")))
print("the first list (NN), by number:", ", ".join(r[0] + " " + r[1] for r in rows if r[7] == "NN"))
print("the second list (CN), by number:", ", ".join(r[0] + " " + r[1] for r in rows if r[7] == "CN"))
print("the fourth list (F), by number:", ", ".join(r[0] + " " + r[1] for r in rows if r[7] == "F"))
