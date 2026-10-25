"""em2's flagged COPY of src/event_universe (engine-5.0-test 5e94fd4b6), written by this script and never by hand, under tools/derivations/open_items/H-Emission-2/src_em2/event_universe.
The flag: the environment variable EM2_EMISSION set to "quantum"; absent, every file is David's bit for bit (the two replaced lines read the default path when the flag is absent, the same integers).
Under the flag the emission's write (W-S1 as built, interval.Interval.writes and unwrite) lays on the massless row's re line, at its write wall T with the carried remainder, the numerator
2 x drift x odd_rounded(emission, W_div) in place of quotient(emission, W_div): one drift (largest_below(T), the seed's level of one massless quantum) per charge quantum T div 2 of the
planes' Wronskian's change over the interval (EM-S1, the derivation in em2_REPORT.md section 1); the odd rounding of the signed numerator in place of the floor (the law's one rounding of a
signed coefficient). Every replacement must match the source text exactly once, else the script refuses. Run: python make_copy_em2.py"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "..", "src", "event_universe")
DST_ROOT = os.path.join(HERE, "src_em2")
DST = os.path.join(DST_ROOT, "event_universe")

if os.path.isdir(DST_ROOT):
    shutil.rmtree(DST_ROOT)
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))

REPLACEMENTS = {
    "interval.py": [
        (
            "from event_universe import readings\n",
            "import os  # em2: the flag is read from the environment, EM2_EMISSION\n\nfrom event_universe import readings\n",
        ),
        (
            "        node.write(self.lines(self.gap0)[0], quotient(self.emission, self.mean_wall()), -1)\n",
            "        node.write(self.lines(self.gap0)[0], emission_numerator(node, self.emission, self.mean_wall()), -1)  # em2: EM-S1 under the flag\n",
        ),
        (
            "        node.write(laid_line, quotient(self.emission, self.w_div), 1)\n",
            "        node.write(laid_line, emission_numerator(node, self.emission, self.w_div), 1)  # em2: EM-S1 under the flag\n",
        ),
        (
            "class Interval:\n",
            "def emission_numerator(node: Node, emission: Any, wall: Any) -> Any:\n"
            "    \"\"\"em2: the emission's numerator for the massless line's write at its wall T. The flag absent: David's quotient(emission, W_div) bit for bit (W-S1 as built: the change of the planes' Wronskian over T). Under EM2_EMISSION=quantum (EM-S1): 2 x drift x odd_rounded(emission, W_div), one drift (the seed's level of one massless quantum, largest_below(T)) per charge quantum T div 2 of the Wronskian's change, the signed numerator rounded once by the law's odd rounding.\"\"\"\n"
            "    if os.environ.get(\"EM2_EMISSION\") != \"quantum\":\n"
            "        return quotient(emission, wall)\n"
            "    return 2 * node.drift * paces.odd_rounded(emission, wall)\n\n\nclass Interval:\n",
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
print("written", DST)
