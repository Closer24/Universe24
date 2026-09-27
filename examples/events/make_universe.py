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
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

from generator_numbers import (  # noqa: E402
    TWIST_COARSE_MOST,
    TWIST_FINE_BITS,
    TWIST_UNIT_SCALE,
    twist_triple,
)

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
