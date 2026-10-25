"""bg1's FLAGGED COPY of the engine (2026-10-25), written by this script from src/event_universe by exact text replacements, never by
hand; the copy sits under tools/derivations/open_items/H-Bang-Return-1/engine/event_universe. The flag is the environment variable BG1 (the hand's control,
no key of the files, no name in the spec); BG1 absent, every path is David's bit for bit (checked by the state hash on the records).
Candidates (the brief's (a), (b), (c) and the hand's derived (d)):
 a: the write's source at the carrier's unit (PM-S1 carried into the write): forms and trace weighed by X div Gamma;
 b: the riding wall's power a^2 (the conformal action): the ride's level Y = largest_below(X Gamma) in place of X at the mean wall,
    the kick and the carrier's write wall for the riders (Y = Gamma a^2 to the unit where X = Gamma a^4);
 c: the swap's trigger where the Node's own velocity turns sign (a strict rise then a strict fall), the flat top and the rest's dip
    not a top;
 d: the write per proper interval once: the lapse p_0 is already inside the ride's forms (u the velocity per board interval at the
    wall w X), so the numerator's trailing p_0 is Gamma: 4 X (forms 54 den Gamma^2 - trace p_0^2) Gamma.
Run: python make_copy.py (refuses unless every replacement matches exactly once)."""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, "..", "..", "..", "src", "event_universe"))
DST = os.path.join(HERE, "engine", "event_universe")

if os.path.exists(os.path.join(HERE, "engine")):
    shutil.rmtree(os.path.join(HERE, "engine"))
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))

REPLACEMENTS = {
    "interval.py": [
        # 0. the flag
        ("from typing import TYPE_CHECKING, Any\n",
         "from typing import TYPE_CHECKING, Any\nimport os  # bg1's flagged copy: BG1 in the environment names the candidate; absent, David's path bit for bit\n"),
        ("from event_universe.core.rule3 import division_forward, half, held_numerator, quotient\n",
         "from event_universe.core.rule3 import division_forward, half, held_numerator, largest_below, quotient\n"),
        # 1. the ride's level (candidate b)
        ("def laid_on(node: Node, line: Line, levels: Any) -> None:",
         "def ride_level(level: Any, gamma: int) -> Any:\n"
         "    \"\"\"bg1 (b): the level the riding wall weighs: X (David's), or under BG1=b the conformal level Y = largest_below(X Gamma), Gamma a^2 to the unit.\"\"\"\n"
         "    if os.environ.get(\"BG1\") != \"b\":\n"
         "        return level\n"
         "    return np.vectorize(lambda x: largest_below(int(x) * gamma), otypes=[object])(np.asarray(level, dtype=object))\n\n\n"
         "def laid_on(node: Node, line: Line, levels: Any) -> None:"),
        ("        return self.w_half * (self.carrier.lines[0].before + self.carrier.lines[0].now)\n",
         "        return self.w_half * (ride_level(self.carrier.lines[0].before, self.node.gamma) + ride_level(self.carrier.lines[0].now, self.node.gamma))\n"),
        ("        d = 2 * node.w * self.x_now\n",
         "        y_now = ride_level(self.x_now, node.gamma)  # bg1 (b)\n        d = 2 * node.w * y_now\n"),
        ("                p + self.direction * self.x_now * f for p, f in zip(p_side, self.force[k], strict=True)\n",
         "                p + self.direction * y_now * f for p, f in zip(p_side, self.force[k], strict=True)\n"),
        ("        self.w_div = self.w_half * (xc.before + xc.now)\n",
         "        self.w_div = self.w_half * (ride_level(xc.before, node.gamma) + ride_level(xc.now, node.gamma))\n"),
        # 2. the write's source (candidates a and d)
        ("        numerators = [\n            held_numerator(TRACE, self.x_now, self.forms, self.trace, self.p0, node.den, node.gamma)\n        ]\n",
         "        flag = os.environ.get(\"BG1\")  # bg1: the candidates a and d on the carrier's time line\n"
         "        forms, trace = self.forms, self.trace\n"
         "        if flag == \"a\":\n"
         "            forms, trace = quotient(forms * self.x_now, node.gamma), quotient(trace * self.x_now, node.gamma)\n"
         "        if flag == \"d\":\n"
         "            numerators = [4 * self.x_now * (forms * TRACE * node.den * node.gamma**2 - trace * self.p0 * self.p0) * node.gamma]\n"
         "        else:\n"
         "            numerators = [held_numerator(TRACE, self.x_now, forms, trace, self.p0, node.den, node.gamma)]\n"),
    ],
    "node.py": [
        ("        wall = half(self.w) * (carrier.before + carrier.now)\n",
         "        wall = half(self.w) * (interval.ride_level(carrier.before, self.gamma) + interval.ride_level(carrier.now, self.gamma))  # bg1 (b)\n"),
        ("            lambda a, b, c: (\n                int(a) <= int(b) and int(c) <= int(b) and (int(a) < int(b) or int(c) < int(b))\n            ),\n",
         "            lambda a, b, c: (\n                (int(a) < int(b) and int(c) < int(b)) if os.environ.get(\"BG1\") == \"c\"  # bg1 (c): the velocity's sign turns\n"
         "                else (int(a) <= int(b) and int(c) <= int(b) and (int(a) < int(b) or int(c) < int(b)))\n            ),\n"),
        ("import hashlib\n", "import hashlib\nimport os  # bg1's flagged copy\n"),
    ],
}

for name, pairs in REPLACEMENTS.items():
    path = os.path.join(DST, name)
    text = open(path, encoding="utf-8").read()
    for old, new in pairs:
        if text.count(old) != 1:
            raise SystemExit(f"{name}: a replacement matches {text.count(old)} times, not once: {old[:60]!r}")
        text = text.replace(old, new)
    open(path, "w", encoding="utf-8").write(text)
    print(f"{name}: {len(pairs)} replacements")
print("written", DST)
