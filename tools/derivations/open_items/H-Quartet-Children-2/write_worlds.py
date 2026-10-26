"""The hand's worlds: universe_qc2.json (the toy universe with the quartet row at the third plane's pair) and the chiral seed on the 5-cube and the 3-cube, the hole seed, and the chiral with a standing quartet at the centre."""
import json
import sys
from pathlib import Path

root, out = Path(sys.argv[1]), Path(sys.argv[2])
uni = json.load(open(root / "tests" / "worlds" / "universe_toy.json"))
third = uni["rows"][2]["pair"]
uni["rows"].append({"shape": 8, "pair": third})
json.dump(uni, open(out / "universe_qc2.json", "w"))
nature = json.load(open(root / "tests" / "worlds" / "world_nature.json"))
hole = json.load(open(root / "tests" / "worlds" / "world_hole.json"))
nature["universe"] = hole["universe"] = "universe_qc2.json"
json.dump(nature, open(out / "world_qc2_chiral5.json", "w"))
json.dump(hole, open(out / "world_qc2_hole5.json", "w"))
three = dict(nature, shape=[3, 3, 3], seed=[dict(s, centre=[x % 3 for x in s["centre"]]) if "centre" in s else s for s in nature["seed"]])
json.dump(three, open(out / "world_qc2_chiral3.json", "w"))
standing = dict(nature, seed=nature["seed"] + [{"lay": "at", "row": len(uni["rows"]) - 1, "centre": [2, 2, 2], "width": 2, "quanta": 100, "vector": [1, -1, 0, 0, 1, 0, 0, 0]}])
json.dump(standing, open(out / "world_qc2_standing5.json", "w"))
print(json.dumps(uni["rows"][-1]), json.dumps(three["seed"]))
