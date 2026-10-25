"""cs7: the world files of the 4-cube with no sea at 400 and 800 intervals for every universe file in worlds/ (cs5's and cs6's files copied: K rows of one pair of den's circle), and the cycle patterns at 5 quanta at both mirrors and senses. Usage: python files_cs7.py worlds"""
import json, os, sys
out = sys.argv[1]
names = sorted(f for f in os.listdir(out) if f.startswith("universe_") and f.endswith(".json"))
made = 0
for name in names:
    stem = name[len("universe_"):-len(".json")]
    for n in (400, 800):
        p = f"{out}/empty4_{stem}_{n}.json"
        if not os.path.exists(p):
            json.dump({"universe": name, "shape": [4, 4, 4], "intervals": n, "seed": []}, open(p, "w"))
            made += 1
p1 = [0, 0, 1, 1, 2, 2, 3, 3, 1, 1, 0, 0, 3, 3, 2, 2]
for mirror in (0, 1):
    for sense in (1, -1):
        json.dump({"p1": p1, "cz": 1, "quanta": 5, "mirror": mirror, "sense": sense}, open(f"{out}/cycle_m5_m{mirror}_s{'p' if sense == 1 else 'm'}.json", "w"))
print("universe files", len(names), "world files made", made)
