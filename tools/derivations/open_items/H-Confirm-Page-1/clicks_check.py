"""The page's embedded clicks against the record's birth and credit lines, field by field: [interval, Node index, row, levels taken, taken row or -1, a birth's two children or 0]."""
import json, re, sys
from pathlib import Path
out, name = Path(sys.argv[1]), sys.argv[2]
record = json.loads((out / f"{name}.json").read_text(encoding="utf-8"))
text = (out / f"{name}.html").read_text(encoding="utf-8")
data = json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>', text, re.S).group(1))
cube = int(record["cube"])
index = lambda n: int(n[0]) * cube * cube + int(n[1]) * cube + int(n[2])
lines = [e for e in record["log"] if e["event"] in ("birth", "credit")]
clicks = data["clicks"]
print(f"{name}: record birth+credit lines {len(lines)} (births {sum(e['event']=='birth' for e in lines)}, credits {sum(e['event']=='credit' for e in lines)}); page clicks {len(clicks)}")
names = ["interval", "node index", "row", "levels", "taken row", "children"]
mismatch = [0] * 6
for e, k in zip(lines, clicks):
    want = [e["i"], index(e["node"]), e["line"] if "line" in e else e.get("line_pair", 0), int(e.get("levels", 0)),
            e["taken_row"] if "taken_row" in e else -1, [index(e["minus"]), index(e["plus"])] if e["event"] == "birth" else 0]
    for f in range(6):
        if want[f] != k[f]:
            mismatch[f] += 1
            if sum(mismatch) <= 5: print("  mismatch", names[f], "record", want[f], "page", k[f], "at interval", e["i"])
print("  lengths equal:", len(lines) == len(clicks), "; mismatches per field:", dict(zip(names, mismatch)))
print("  intervals in order:", all(clicks[j][0] <= clicks[j + 1][0] for j in range(len(clicks) - 1)))
print("  credits carry levels:", sum("levels" in e for e in lines if e["event"] == "credit"), "of", sum(e["event"] == "credit" for e in lines), "; credits carry taken_row:", sum("taken_row" in e for e in lines if e["event"] == "credit"))
print("  births carry line:", sum("line" in e for e in lines if e["event"] == "birth"), "; births carry line_pair:", sum("line_pair" in e for e in lines if e["event"] == "birth"))
print("  bangs on the page:", data["bangs"], "; births' intervals in the record:", sorted({e["i"] for e in lines if e["event"] == "birth"}))
print("  stride:", data["stride"], "; node lines on the page:", len(data["nodes"]), "of", len(record["nodes"]))
