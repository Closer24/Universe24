"""THE UNIVERSE'S TWIST TABLE, generated once into the families file's integers block
(ALGEBRA.md #the-transport, #the-primitives; the one stroke, commit 4).

The angle unit is theta_unit = 1 / (4 Gamma 2^16) radians per unit of the twist k. The
transport composes two triples per Port: the FINE table holds the 2^10 triples of the angles
k_0 theta_unit (k_0 in [0, 2^10)) and the COARSE table the triples of the angles k_1 2^10
theta_unit (k_1 in [0, 2^15)); each triple (c, s, d) is the nearest the engine's loader
accepts (`twist_triple`: n / m nearest tan(angle / 2) with d = m^2 + n^2 at most 10^9), so
the loader's check of every identity and every angle passes by construction. HOST: the
generator's floats end here; the file holds integers and the engine reads integers.

Run from the repository root: python examples/events/make_universe.py
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

# the generator's own numbers (HOST): the twist's unit scale 2^16, 2^10 fine and 2^15 coarse triples, the triples' d bound 10^9
TWIST_UNIT_SCALE = 1 << 16
TWIST_FINE_BITS = 10
TWIST_COARSE_MOST = 1 << 15
TWIST_TRIPLE_BOUND = 10**9


def twist_triple(k: int, unit: int) -> tuple[int, int, int]:
    """THE NEAREST TRIPLE of the angle k / unit radians (ALGEBRA.md #the-transport, #the-primitives): n / m nearest tan(angle / 2) with m at most the root of the d bound, the triple (m^2 - n^2, 2 m n, m^2 + n^2) in lowest terms, (1, 0, 1) at angle 0; HOST, the loader checks the identities and the angles' order."""
    ratio = Fraction(math.tan(k / (2 * unit))).limit_denominator(math.isqrt(TWIST_TRIPLE_BOUND))
    n, m = ratio.numerator, ratio.denominator
    c, s, d = m * m - n * n, 2 * m * n, m * m + n * n
    g = math.gcd(math.gcd(c, s), d)
    return c // g, s // g, d // g


FAMILIES_FILE = ROOT / "examples" / "events" / "universe.json"  # the universe file (record 2128 (3))


def twist_table(node_clock: int) -> dict[str, object]:
    """The table for the universe's Gamma: the unit 4 Gamma 2^16, the fine and the coarse
    triples (ALGEBRA.md #the-primitives)."""
    unit = 4 * node_clock * TWIST_UNIT_SCALE
    fine = [list(twist_triple(k, unit)) for k in range(1 << TWIST_FINE_BITS)]
    coarse = [list(twist_triple(k << TWIST_FINE_BITS, unit)) for k in range(TWIST_COARSE_MOST)]
    return {"unit": unit, "fine": fine, "coarse": coarse}


def main() -> None:
    document = json.loads(FAMILIES_FILE.read_text(encoding="utf-8"))
    document["integers"]["twist_table"] = twist_table(int(document["integers"]["node_clock"]))
    # one triple per line (indent=1 would give three lines per triple)
    table = document["integers"]["twist_table"]
    marks = {name: f"@@{name}@@" for name in ("fine", "coarse")}
    rows = {name: table[name] for name in marks}
    for name, mark in marks.items():
        table[name] = mark
    text = json.dumps(document, indent=1)
    for name, mark in marks.items():
        body = ",\n".join("    " + json.dumps(row) for row in rows[name])
        text = text.replace(json.dumps(mark), "[\n" + body + "\n   ]")
        table[name] = rows[name]
    FAMILIES_FILE.write_text(text + "\n", encoding="utf-8")
    print(f"wrote {FAMILIES_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
