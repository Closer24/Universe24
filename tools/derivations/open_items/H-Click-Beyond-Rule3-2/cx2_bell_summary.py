"""H-Click-Beyond-Rule3-2: the Bell reader's output (bell_setting_bs2_copy.py's JSON lines) summed: per record, for the outcome `sense`, every setting's S as [num, den], S^2 against 4 den^2 and 8 den^2, the pairs used. Usage: python cx2_bell_summary.py <bell.stdout>"""
import json
import sys

for line in open(sys.argv[1]):
    line = line.strip()
    if not line.startswith("{"):
        continue
    d = json.loads(line)
    rows = d.get("readings") or d.get("rows") or []
    out = {"record": d.get("record"), "pairs": d.get("pairs clicked at both ends"), "twin_one_link": d.get("twin one Link away at both ends"), "sense": {}}
    for r in rows:
        if r.get("outcome") != "sense":
            continue
        labs = r.get("labellings", {})
        first = next(iter(labs.values())) if labs else {}
        s = first.get("S")
        out["sense"][r["setting"]] = {"pairs": r.get("pairs used"), "S": s, "band": first.get("band") or first.get("empty cell")}
    print(json.dumps(out))
