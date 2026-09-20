"""Write the worlds of series I, "the nucleus", under the Beam Law in space:
nucleons that are free bodies holding one unit of a strong family with a
lifetime, bound or not by the one coupling over the columns (the model
owner, 2026-09-20: "one mechanism for all the laws on the GameBoard"; "the
strong force's range is a lifetime, L"; the contact through the table),
read at the bodies themselves (their `read` records, their `contact`
records, their steps).

The register's nucleons (README.md here; the physicist's design of the
strong force, section 3): three free families without a phase circle,
`p` (charge per unit of content 4), `n` (no charge) and `nuclear` (the
column `strong` with the value G = 10000 per unit and the sign minus, the
lifetime 3: its rays reach the six neighbours, the twelve face diagonals,
the eight cube diagonals and the second Link of a heading and click on the
border `lifetime` at the age 3). A proton is a body of `p`, content 1836,
holding one unit of `nuclear` (`held`): the charges M 1837, Q 7344 and G
10000; a neutron 1839 of `n` holding one unit: 1840, 0, 10000. Every body
releases one row of its held content per direction of the fan of the 290
primitive directions with |a| + |b| + |c| <= 6 per interval (`release`
[1, 1]). The push per interval between two bodies at mirror Nodes within
the reach is (Q_A Q_B - G_A G_B - M_A M_B) x U(r) per unit per direction,
U(1) = 3008 on the axis: two protons at one Link bind because G^2 + M^2 >
Q^2 (103 374 569 > 53 934 336; the least G that binds is 7111), a proton and
a neutron by G^2 + M_p M_n, and beyond the reach only Q^2 - M_A x 1836
remains. `suspension` 0, `width` 2^28 (W = 64 x 2^28 x M = 3.2 x 10^13
label units against a push of 3.1 x 10^11 per interval: a body steps at
about p / W Links per interval, the slow regime), K 2^20, N 64, an open
cube of SIDE^3 Nodes, TICKS intervals; under the contact through the table
every refused step of a body onto its neighbour hands its momentum
component to the neighbour, so a bound pair's labels stay bounded and the
books close. The worlds (DESIGN section 6, I1 to I6; the budget cut I7 to
I10: the clock beside the nucleus, the cube of 64, the core family and the
lifetimes across fans are not run):

| world | what |
| --- | --- |
| `deuteron_1` | a proton and a neutron at one Link |
| `deuteron_3` | the same at three Links, each kicked outward by 10^12 |
| `deuteron_1_kick` | at one Link, each kicked outward by 10^12 |
| `pp_1` | two protons at one Link |
| `pp_1_weak` | two protons at one Link with G = 7000, below the binding |
| `pp_3` | two protons at three Links |
| `alpha_square` | p n / n p, the 2 x 2 square |
| `alpha_line` | p n n p on the axis |

    python examples/events/nucleus/make_worlds.py [--out DIR]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "src"))

from event_universe.world_loading import families_by_definition  # noqa: E402

# The shipped definitions the world's families come from where they equal
# them (the model owner's decision of 2026-09-20, record 113).
FAMILY_DEFINITIONS = "../entities/families.json"
DEFINITIONS_SOURCE = (HERE.parent / "entities" / "families.json").read_bytes()


K = 1 << 20
N = 64
SIDE = 21
TICKS = 3000
WIDTH = 1 << 28
PROTON = 1836
NEUTRON = 1839
CHARGE = 4
STRONG = 10000
WEAK_STRONG = 7000
LIFETIME = 3
KICK = 10**12
FAN_REACH = 6
HEADINGS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
Json = dict[str, object]


def fan(reach: int) -> list[tuple[int, int, int]]:
    """Every primitive direction (a, b, c) with 1 <= |a| + |b| + |c| <=
    reach, in a fixed order (290 for the reach 6, the six headings among
    them)."""
    found = []
    for a in range(-reach, reach + 1):
        for b in range(-reach, reach + 1):
            for c in range(-reach, reach + 1):
                size = abs(a) + abs(b) + abs(c)
                if 0 < size <= reach and math.gcd(math.gcd(abs(a), abs(b)), abs(c)) == 1:
                    found.append((a, b, c))
    found.sort()
    return found


def nucleon(
    family: str, position: tuple[int, int, int], momentum: tuple[int, int, int] = (0, 0, 0)
) -> Json:
    """A proton (`p`) or a neutron (`n`): its content under its own family,
    one unit of `nuclear` held, released on the whole fan."""
    body: Json = {
        "position": list(position),
        "family": family,
        "amount": PROTON if family == "p" else NEUTRON,
        "held": {"nuclear": 1},
        "fixed": False,
    }
    if any(momentum):
        body["momentum"] = list(momentum)
    return body


def world(name: str, bodies: list[Json], strong: int = STRONG) -> Json:
    directions = fan(FAN_REACH)
    declared = [list(v) for v in directions if v not in HEADINGS]
    whole_fan = list(range(2, 8 + len(declared)))
    for body in bodies:
        body["directions"] = whole_fan
    return {
        "law": "beam",
        "model_id": f"beam-nucleus-{name}-space-v1",
        "shape": [SIDE, SIDE, SIDE],
        "boundary": "open",
        "ticks": TICKS,
        "K": K,
        "N": N,
        "release": [1, 1],
        "suspension": 0,
        "width": WIDTH,
        "directions": declared,
        "families": [
            {"name": "p", "quantum": 0, "charge": CHARGE, "phase": False},
            {"name": "n", "quantum": 0, "phase": False},
            {
                "name": "nuclear",
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
    return {
        "deuteron_1": world("deuteron_1", [nucleon("p", (c, c, c)), nucleon("n", (c + 1, c, c))]),
        "deuteron_3": world(
            "deuteron_3",
            [nucleon("p", (c - 1, c, c), (-KICK, 0, 0)), nucleon("n", (c + 2, c, c), (KICK, 0, 0))],
        ),
        "deuteron_1_kick": world(
            "deuteron_1_kick",
            [nucleon("p", (c, c, c), (-KICK, 0, 0)), nucleon("n", (c + 1, c, c), (KICK, 0, 0))],
        ),
        "pp_1": world("pp_1", [nucleon("p", (c, c, c)), nucleon("p", (c + 1, c, c))]),
        "pp_1_weak": world(
            "pp_1_weak", [nucleon("p", (c, c, c)), nucleon("p", (c + 1, c, c))], strong=WEAK_STRONG
        ),
        "pp_3": world("pp_3", [nucleon("p", (c - 1, c, c)), nucleon("p", (c + 2, c, c))]),
        "alpha_square": world(
            "alpha_square",
            [
                nucleon("p", (c, c, c)),
                nucleon("n", (c + 1, c, c)),
                nucleon("n", (c, c + 1, c)),
                nucleon("p", (c + 1, c + 1, c)),
            ],
        ),
        "alpha_line": world(
            "alpha_line",
            [
                nucleon("p", (c - 1, c, c)),
                nucleon("n", (c, c, c)),
                nucleon("n", (c + 1, c, c)),
                nucleon("p", (c + 2, c, c)),
            ],
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--out", type=Path, default=HERE)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    directions = fan(FAN_REACH)
    print(
        f"fan: {len(directions)} directions; {SIDE}^3 open, {TICKS} intervals, width 2^28, "
        f"G = {STRONG} (weak {WEAK_STRONG}), lifetime {LIFETIME}"
    )
    for name, document in worlds().items():
        path = args.out / f"{name}.json"
        document = families_by_definition(document, FAMILY_DEFINITIONS, DEFINITIONS_SOURCE)
        path.write_text(json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8")
        print(path)


if __name__ == "__main__":
    main()
