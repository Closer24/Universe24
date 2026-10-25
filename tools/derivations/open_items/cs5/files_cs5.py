"""cs5: the universe files, every gapped pair a point of den's circle (worlds/circle.txt, cs3's; the loader refuses a pair off it): cs4's five files rebuilt from its text (toy, lift, l3, l4, c14), then this round's: one gapped plane beside the gap-0 plane for every one of the 26 circle points (p_<k>), the lift's pair listed twice, three and four times (lift2, lift3, lift4: records of one plane under distinct row indices, the crowd's key), and the lift beside the second light-side point (2p); the cycle patterns at 5, 6, 7, 8 and 10 quanta; the world files of the 4-cube with no sea at named lengths.
Usage: python files_cs5.py worlds"""
import json
import sys

sys.set_int_max_str_digits(0)
out = sys.argv[1]
den = 15162856759112389
ints = {"den": den, "node_clock": 1000, "quantum_action": 36000}
tail = [{"shape": 10, "pair": [15147693902353277, den]}, {"shape": 4, "pair": [den, den]}, {"shape": 1, "wall": 2}]
light = [{"shape": 2, "pair": [den, den]}]


def plane(n):
    return {"shape": 2, "pair": [n, den]}


circle = []
for line in open(f"{out}/circle.txt"):
    parts = line.split()
    if len(parts) >= 4 and parts[0] == "num":
        circle.append((int(parts[1]), int(parts[3])))
assert len(circle) == 26, len(circle)
lift = 15162854575528411
heavy = [2458210083751875, 2580388913625285]
three = [15162414850065661, 15162350539855939, 15162281862624061]
c14 = [lift] + heavy + [8137489624680, 115762739551980, 123899975345340, 132037175453340, 2450179891247805, 2466239568248445, 2572369751602395, 2588407332451035, 4960916831461980, 4968605748185340, 4976293233863340]
files = {
    "universe_toy.json": light + [plane(lift)] + [plane(h) for h in heavy],
    "universe_lift.json": light + [plane(lift)],
    "universe_l3.json": light + [plane(n) for n in three],
    "universe_l4.json": light + [plane(lift)] + [plane(n) for n in three],
    "universe_c14.json": light + [plane(n) for n in c14],
    "universe_lift2.json": light + [plane(lift), plane(lift)],
    "universe_lift3.json": light + [plane(lift)] * 3,
    "universe_lift4.json": light + [plane(lift)] * 4,
    "universe_2p.json": light + [plane(lift), plane(three[0])],
}
for k, (num, s) in enumerate(circle):
    files[f"universe_p{k:02d}.json"] = light + [plane(num)]
names = []
for name, rows in files.items():
    json.dump({"integers": dict(ints), "rows": rows + tail}, open(f"{out}/{name}", "w", encoding="utf-8"))
    names.append(name)
    stem = name[len("universe_"):-len(".json")]
    for n in (6, 50, 400, 800):
        json.dump({"universe": name, "shape": [4, 4, 4], "intervals": n, "seed": []}, open(f"{out}/empty4_{stem}_{n}.json", "w", encoding="utf-8"))
p1 = [0, 0, 1, 1, 2, 2, 3, 3, 1, 1, 0, 0, 3, 3, 2, 2]
for q in (5, 6, 7, 8, 10):
    json.dump({"p1": p1, "cz": 1, "quanta": q, "mirror": 1, "sense": 1}, open(f"{out}/cycle_m{q}.json", "w", encoding="utf-8"))
print("files", len(names), "circle points", len(circle), "lift at index", [k for k, (n, s) in enumerate(circle) if n == lift])
for k, (num, s) in enumerate(circle):
    print(f"p{k:02d}", num, s)
