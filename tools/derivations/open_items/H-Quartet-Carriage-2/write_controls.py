"""H-Quartet-Carriage-2: the control worlds (the seed's one-Node lay of one quartet quantum, the lay at the Link's two ends as the born pair, and the same pair laid moving apart, MV-S1's wave), on the chiral 3-cube seed at 60, per candidate pair; the vectors the flagged copy's gram.spin_vector (the child's own lay vector per axis and sign).
Usage: python write_controls.py <src of the flagged copy> <worlds folder>"""
import json, sys, copy
sys.path.insert(0, sys.argv[1])
from event_universe import gram  # noqa: E402

folder = sys.argv[2]
chiral3 = json.load(open(f"{folder}/world_chiral3_60_lift3.json"))
vz = [int(x) for x in gram.spin_vector(8, 2, 1)]
vym, vyp = [int(x) for x in gram.spin_vector(8, 1, -1)], [int(x) for x in gram.spin_vector(8, 1, 1)]
print("vectors z+", vz, "y-", vym, "y+", vyp)
for name, qrow in (("lift1", 7), ("p3", 7), ("lift3", 7), ("mid", 6)):
    base = copy.deepcopy(chiral3); base["universe"] = f"universe_{name}.json"
    one = copy.deepcopy(base)
    one["seed"].append({"lay": "at", "row": qrow, "centre": [1, 1, 1], "quanta": 1, "vector": vz, "sense": 1})
    json.dump(one, open(f"{folder}/world_one3_60_{name}.json", "w"))
    pair = copy.deepcopy(base)
    pair["seed"].append({"lay": "at", "row": qrow, "centre": [1, 1, 0], "quanta": 1, "vector": vym, "sense": -1})
    pair["seed"].append({"lay": "at", "row": qrow, "centre": [1, 2, 0], "quanta": 1, "vector": vyp, "sense": 1})
    json.dump(pair, open(f"{folder}/world_pairrest3_60_{name}.json", "w"))
    wave = copy.deepcopy(base)
    wave["seed"].append({"lay": "at", "row": qrow, "centre": [1, 1, 0], "quanta": 1, "vector": vym, "sense": -1, "wave": [0, -1, 0]})
    wave["seed"].append({"lay": "at", "row": qrow, "centre": [1, 2, 0], "quanta": 1, "vector": vyp, "sense": 1, "wave": [0, 1, 0]})
    json.dump(wave, open(f"{folder}/world_pairwave3_60_{name}.json", "w"))
print("written")
