"""bb2: the standing wave of R4's form at the drift's granularity, as the world file's lays alone (the three forms: at on the gap-0 row and hole; no sea): now = drift m(x), before = 0, m = (2P)(x)(2P)(y)(2P)(z) with 2P = (-1, 2, -1) about the centre of the 3-cube (cos(2 pi k / 3) doubled), the mode symmetric under the 48, zero-sum. m is 8 at the centre (an at of 8 quanta), -4 at the 6 face neighbours (4 holes each), 2 at the 12 edge neighbours (an at of 2), -1 at the 8 corners (1 hole each)."""
import json
import sys

centre = (1, 1, 1)
lays = []
for x in range(3):
    for y in range(3):
        for z in range(3):
            m = 1
            for c in (x, y, z):
                m *= 2 if c == 1 else -1
            if m > 0:
                lays.append({"lay": "at", "row": 0, "centre": [x, y, z], "quanta": m})
            else:
                for _ in range(-m):
                    lays.append({"lay": "hole", "at": [x, y, z]})
total = sum(l.get("quanta", -1) for l in lays)
world = {"universe": "universe_toy.json", "shape": [3, 3, 3], "intervals": int(sys.argv[1]), "seed": lays}
json.dump(world, open(sys.argv[2], "w"))
print(json.dumps({"lays": len(lays), "sum of m": total, "ats": sum(1 for l in lays if l["lay"] == "at"), "holes": sum(1 for l in lays if l["lay"] == "hole")}))
