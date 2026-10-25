"""pm2's flagged COPY of src/event_universe (engine-5.0-test af06713db), written by this script and never by hand, under tools/derivations/pm2/src_pm2/event_universe. The flag: the world file's key `pm2_weight` with the value "carrier"; absent, every file is David's bit for bit but for the key's plumbing (the loader admits the key, the Node holds it, the interval keeps the carrier's start level), which changes no integer of the run. Under the flag every count at the Node is read at the carrier's weight: the share of every row (readings.share, the V-D branch), the lay of one quantum (take.lay_amplitude) and the exact take (take.fall_of) divide at 4 Gamma^3 G^2 with the form times the carrier's level X at the interval's start in the numerator (p^2 = Gamma^3 / X to the roundings), the same factor X on every row and every reading. Every replacement must match the source text exactly once, else the script refuses. Run: python make_copy.py"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "..", "src", "event_universe")
DST_ROOT = os.path.join(HERE, "src_pm2")
DST = os.path.join(DST_ROOT, "event_universe")

if os.path.isdir(DST_ROOT):
    shutil.rmtree(DST_ROOT)
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))

REPLACEMENTS = {
    "loader/world.py": [
        (
            'WORLD_KEYS = frozenset({"universe", "shape", "intervals", "seed"})',
            'WORLD_KEYS = frozenset({"universe", "shape", "intervals", "seed", "pm2_weight"})  # pm2: the hand\'s flag key',
        ),
    ],
    "node.py": [
        (
            "        self.cube, self.shape = shape[0], shape\n",
            "        self.cube, self.shape = shape[0], shape\n        self.weight_kind = world.get(\"pm2_weight\")  # pm2: None is David's path bit for bit; \"carrier\" reads every count at the carrier's weight\n        self.start_x = None  # pm2: the carrier's level at the interval's start, kept by the interval's readings\n",
        ),
    ],
    "interval.py": [
        (
            "        self.x_now = self.at(self.carrier.lines[0])\n",
            "        self.x_now = self.at(self.carrier.lines[0])\n        node.start_x = self.x_now  # pm2: the carrier's start level for the counts' weight\n",
        ),
    ],
    "readings.py": [
        (
            "    pace = paces.link_pace_of(node.gamma, node.start_content) if pace is None else pace\n    sq = (node.gamma * node.gamma) if vacuum else pace * pace\n    wall = 4 * sq * node.G * node.G + (sq == 0)\n    return np.asarray(division_forward(found, wall, 0)[0])\n",
            "    if vacuum and getattr(node, \"weight_kind\", None) == \"carrier\":  # pm2: the carrier's weight, found X over 4 Gamma^3 G^2\n        x = node.start_x if node.start_x is not None else node.row(CARRIER).lines[0].now\n        return np.asarray(division_forward(found * x, 4 * node.gamma**3 * node.G * node.G, 0)[0])\n    pace = paces.link_pace_of(node.gamma, node.start_content) if pace is None else pace\n    sq = (node.gamma * node.gamma) if vacuum else pace * pace\n    wall = 4 * sq * node.G * node.G + (sq == 0)\n    return np.asarray(division_forward(found, wall, 0)[0])\n",
        ),
    ],
    "take.py": [
        (
            "    pace = int(np.asarray(paces.link_pace_of(node.gamma, node.start_content), dtype=object)[at])\n    weight = 2 * pace * pace * node.G * node.G + (1 if pace == 0 else 0)\n\n    def fall(s: int) -> int:\n        return int(\n            quotient(w * (now * now - (now + t * s) ** 2) - t * s * (own * before + reached), weight)\n        )\n",
            "    pace = int(np.asarray(paces.link_pace_of(node.gamma, node.start_content), dtype=object)[at])\n    weight = 2 * pace * pace * node.G * node.G + (1 if pace == 0 else 0)\n    scale = 1  # pm2: the numerator's factor, 1 on David's path\n    if getattr(node, \"weight_kind\", None) == \"carrier\":  # pm2: the carrier's weight, the fall times X over 2 Gamma^3 G^2\n        scale = int(node.start_x[at]) if node.start_x is not None else int(node.row(CARRIER).lines[0].now[at])\n        weight = 2 * node.gamma**3 * node.G * node.G\n\n    def fall(s: int) -> int:\n        return int(\n            quotient(scale * (w * (now * now - (now + t * s) ** 2) - t * s * (own * before + reached)), weight)\n        )\n",
        ),
        (
            "    for s in rule3.least_root(-w, -(2 * w * now + own * before + reached) * t, walls * weight, dist):\n",
            "    for s in rule3.least_root(-w * scale, -(2 * w * now + own * before + reached) * t * scale, walls * weight, dist):  # pm2: the root's quadratic scaled alike\n",
        ),
        (
            "    pc = int(np.asarray(pace, dtype=object)[at])\n    target = node.units[s] * 4 * pc * pc * node.G * node.G\n    if weight <= 0:\n        return node.A\n",
            "    pc = int(np.asarray(pace, dtype=object)[at])\n    target = node.units[s] * 4 * pc * pc * node.G * node.G\n    if getattr(node, \"weight_kind\", None) == \"carrier\":  # pm2: the carrier's weight, (2 D + SUM R) A^2 X >= unit 4 Gamma^3 G^2\n        x = int(node.start_x[at]) if node.start_x is not None else int(node.row(CARRIER).lines[0].now[at])\n        weight, target = weight * x, node.units[s] * 4 * node.gamma**3 * node.G * node.G\n    if weight <= 0:\n        return node.A\n",
        ),
    ],
}

for name, pairs in REPLACEMENTS.items():
    path = os.path.join(DST, name)
    text = open(path, encoding="utf-8").read()
    for old, new in pairs:
        if text.count(old) != 1:
            sys.exit(f"REFUSED: {name}: the text occurs {text.count(old)} times, not once:\n{old}")
        text = text.replace(old, new)
    open(path, "w", encoding="utf-8").write(text)
    print(f"{name}: {len(pairs)} replacement(s)")
# take.py imports CARRIER for the fallback read
path = os.path.join(DST, "take.py")
text = open(path, encoding="utf-8").read()
old = "from event_universe.rows import PLANE, Line\n"
if text.count(old) != 1:
    sys.exit("REFUSED: take.py import line")
open(path, "w", encoding="utf-8").write(text.replace(old, "from event_universe.rows import CARRIER, PLANE, Line  # pm2: CARRIER for the fallback read of X\n"))
print("take.py: the import")
print("written", DST)
