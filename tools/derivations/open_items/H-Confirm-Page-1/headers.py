"""Prints the header line of each page (the text of the #head div) and the seed of its record, to read whether a lone lay's centre stands in the header."""
import json, re, sys
from pathlib import Path
out = Path(sys.argv[1])
for name in sys.argv[2:]:
    text = (out / f"{name}.html").read_text(encoding="utf-8")
    head = re.search(r'<div id="head">(.*?)</div>', text, re.S).group(1)
    world = json.loads((out / f"{name}.json").read_text(encoding="utf-8"))["world"]
    print(f"--- {name}")
    print("seed in the record:", json.dumps(world["seed"]))
    print("header's world line:", head.splitlines()[-1])
    centres = [lay["centre"] for lay in world["seed"] if "centre" in lay]
    shown = [c for c in centres if json.dumps(c) in head or str(c) in head]
    print(f"centres in the seed {len(centres)}, centres shown in the header {len(shown)}")
