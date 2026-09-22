"""Write the worlds of series R, the quarks (the physicist's design
`docs/designs/quarks/QUARKS.md` section 4), beside this file: nucleons that are three free quark bodies at
adjacent Nodes, each holding one unit of the strong family `glue` (the
same binding the register's nucleons use: the strong column sigma 10000
per unit with the sign minus, the lifetime 3 as the range; BEAM_LAW note
31), bound or not by the one coupling over the columns and the contact
through the table; read at the bodies themselves (their `read` and
`contact` records, their steps, the border's clicks). Registered as series R on
the model owner's standing go (record 264); the expectations beside the
worlds (`expectations.json`) are derived by the design's `quark_numbers.py`
and compared by `tests/test_quarks_expectations.py`.

The base is series I's (`examples/events/nucleus/make_worlds.py`): an
open cube of 21^3 Nodes, K 2^20, N 64, `release` [1, 1], `suspension` 0,
the fan of the 290 primitive directions with |a| + |b| + |c| <= 6, 3000
intervals. The quark rows (QUARKS.md section 1, `quark_numbers.out`
section 1): `u` with 4 units of content and the charge per unit 1224 (the
whole charge 4896 = 2/3 of the register's proton 7344), `d` with 9 units
and -272 (the whole charge -2448); `glue` the strong family. The width
S = 2^37 keeps the step rule in series I's slow regime (W = 64 S M about
4 x 10^13 label units on a body of 5 units, the first attempt at a step
about sixteen intervals, section 6 of the numbers); the dressed world
holds 606 or 607 units of `glue` per quark at the value [10000, 606] and S = 2^30.

| world | what |
| --- | --- |
| `q1_proton_line` | u d u on the x axis (the odd quark in the middle) |
| `q2_neutron_line` | d u d on the x axis |
| `q3_proton_triangle` | u u d on the face-diagonal sublattice, mutual sqrt 2 (the shape whose stabiliser in the 48 is S_3) |
| `q4_deuteron_rectangle` | u d u over d u d at one Link (two lines stacked on y) |
| `q5_deuteron_line` | u d u d u d on the x axis (the two triples end to end) |
| `q6_proton_kick` | q1 with the end quark u kicked outward by 10^13 label units (what the law does not confine) |
| `q7_proton_dressed` | q1 with the glue 606, 607, 606 held at the value [10000, 606] (the read mass 1836 by declaration, the strong charge 10000 per body as in q1), width 2^30 |

    python examples/events/quarks/make_worlds.py [--out DIR]
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
Json = dict[str, object]

K = 1 << 20
N = 64
SIDE = 21
TICKS = 3000
WIDTH = 1 << 37
WIDTH_DRESSED = 1 << 30
UNITS = {"u": 4, "d": 9}
RHO = {"u": 1224, "d": -272}
STRONG = 10000
LIFETIME = 3
KICK = 10**13
FAN_REACH = 6
HEADINGS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
DRESSED = {"proton": (606, 606, 607)}


def fan(reach: int) -> list[tuple[int, int, int]]:
    """Every primitive direction (a, b, c) with 1 <= |a| + |b| + |c| <=
    reach, in a fixed order (290 for the reach 6)."""
    found = []
    for a in range(-reach, reach + 1):
        for b in range(-reach, reach + 1):
            for c in range(-reach, reach + 1):
                size = abs(a) + abs(b) + abs(c)
                if 0 < size <= reach and math.gcd(math.gcd(abs(a), abs(b)), abs(c)) == 1:
                    found.append((a, b, c))
    found.sort()
    return found


def quark(
    flavour: str,
    position: tuple[int, int, int],
    momentum: tuple[int, int, int] = (0, 0, 0),
    glue: int = 1,
) -> Json:
    """A quark body: its content under its own family, `glue` units of the
    strong family held, released on the whole fan."""
    body: Json = {
        "position": list(position),
        "family": flavour,
        "amount": UNITS[flavour],
        "held": {"glue": glue},
        "fixed": False,
    }
    if any(momentum):
        body["momentum"] = list(momentum)
    return body


def world(name: str, bodies: list[Json], width: int = WIDTH, strong: int | list[int] = STRONG) -> Json:
    """The world: `strong` the glue's value per unit of content, an integer
    or a pair (the dressed world's [10000, 606], so that 606 units held
    carry the strong charge 10000 as one unit at 10000 does)."""
    directions = fan(FAN_REACH)
    declared = [list(v) for v in directions if v not in HEADINGS]
    whole_fan = list(range(2, 8 + len(declared)))
    for body in bodies:
        body["directions"] = whole_fan
    return {
        "law": "beam",
        "model_id": f"beam-quarks-{name}-space-v1",
        "shape": [SIDE, SIDE, SIDE],
        "boundary": "open",
        "ticks": TICKS,
        "K": K,
        "N": N,
        "release": [1, 1],
        "suspension": 0,
        # The per-axis drive of history (the world key `per_axis_drive`;
        # since 2026-09-22 the line drive is the law's drive of a body,
        # docs/designs/drive_b/DEFAULT.md): series R's registered readings
        # were read under it and stand as registered until the series is
        # re-pinned under the law in the campaign of DEFAULT.md section (c).
        "per_axis_drive": True,
        "width": width,
        "directions": declared,
        "families": [
            {"name": "u", "quantum": 0, "charge": RHO["u"], "phase": False},
            {"name": "d", "quantum": 0, "charge": RHO["d"], "phase": False},
            {
                "name": "glue",
                "quantum": 0,
                "columns": {"strong": {"value": strong, "sign": -1}},
                "lifetime": LIFETIME,
                "phase": False,
            },
        ],
        "measured": bodies,
    }


def worlds() -> dict[str, Json]:
    c = SIDE // 2
    line_p = [quark("u", (c - 1, c, c)), quark("d", (c, c, c)), quark("u", (c + 1, c, c))]
    line_n = [quark("d", (c - 1, c + 1, c)), quark("u", (c, c + 1, c)), quark("d", (c + 1, c + 1, c))]
    return {
        "q1_proton_line": world(
            "q1_proton_line",
            [quark("u", (c - 1, c, c)), quark("d", (c, c, c)), quark("u", (c + 1, c, c))],
        ),
        "q2_neutron_line": world(
            "q2_neutron_line",
            [quark("d", (c - 1, c, c)), quark("u", (c, c, c)), quark("d", (c + 1, c, c))],
        ),
        "q3_proton_triangle": world(
            "q3_proton_triangle",
            [
                quark("u", (c + 1, c + 1, c)),
                quark("u", (c, c + 1, c + 1)),
                quark("d", (c + 1, c, c + 1)),
            ],
        ),
        "q4_deuteron_rectangle": world("q4_deuteron_rectangle", line_p + line_n),
        "q5_deuteron_line": world(
            "q5_deuteron_line",
            [quark(f, (c - 3 + i, c, c)) for i, f in enumerate("ududud")],
        ),
        "q6_proton_kick": world(
            "q6_proton_kick",
            [quark("u", (c - 1, c, c), (-KICK, 0, 0)), quark("d", (c, c, c)), quark("u", (c + 1, c, c))],
        ),
        "q7_proton_dressed": world(
            "q7_proton_dressed",
            [
                quark("u", (c - 1, c, c), glue=DRESSED["proton"][0]),
                quark("d", (c, c, c), glue=DRESSED["proton"][2]),
                quark("u", (c + 1, c, c), glue=DRESSED["proton"][1]),
            ],
            width=WIDTH_DRESSED,
            strong=[STRONG, DRESSED["proton"][0]],
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--out", type=Path, default=HERE)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    print(
        f"fan: {len(fan(FAN_REACH))} directions; {SIDE}^3 open, {TICKS} intervals, width 2^37 (dressed 2^30), "
        f"sigma {STRONG}, lifetime {LIFETIME}; u {UNITS['u']} units at rho {RHO['u']}, d {UNITS['d']} at {RHO['d']}"
    )
    for name, document in worlds().items():
        path = args.out / f"{name}.json"
        path.write_text(json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8")
        print(path)


if __name__ == "__main__":
    main()
