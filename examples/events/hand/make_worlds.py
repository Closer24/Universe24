"""Write the worlds of series P, "the hand", under the Beam Law (`hand-v1`;
the model owner, 2026-09-20, record 128 of docs/LOG_2026-09-20.md: "the
hand's three choices confirmed"; the physicist's design hand/DESIGN.md
sections 3.1, 3.3 and 3.4 with the mathematician's FORM.md; BEAM_LAW note
39). Three worlds and one control, each a re-statement of a registered weak
world with a hand on a family, an axis on a body and a parity filter on a
reader; every expectation in the README beside this file was written before
the first run, from the design's integers and the engine's own documented
rules (the flight table's first-arrival ages, the tie rule of the
apportioning at a self-creation).

`w_hand`: the W world (`weak/w_exchange`) with a second proton, the W family
given the hand -1, the neutron the axis -x and both protons the parity
filter `hand -1` on `w`: the right-hand rule sends the left-handed W AGAINST
the axis, on +x, to the proton at x = 3. `w_two_sides`: the same bar with
the axis and every hand removed, the control of the parity test: the W's
one unit goes where the tie rule of the apportioning sends it. `wu`: Wu's
experiment on a bar of 17, the neutron with the axis +x, the beta family
left-handed and the antineutrino right-handed, readers at both ends: the
beta leaves against the axis and clicks at x = 0. `nu_hand`: J2's bar with
the neutrino left-handed and two readers, the first admitting the right
hand only (0 clicks) and the second the left (every ray).

    python examples/events/hand/make_worlds.py [--out DIR]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
Json = dict[str, object]

N = 64
K = 1 << 20
PROTON = 1836
NEUTRON = 1839
CHARGE = 4
W_CONTENT = 3
W_CHARGE = -CHARGE * PROTON
W_AT = 8
W_TICKS = 16
PLUS_X = [1, 0, 0]
MINUS_X = [-1, 0, 0]
# Wu's bar: the neutron at its centre, the readers at its ends.
WU_BAR = 17
WU_NEUTRON = 8
WU_TICKS = 40
# The neutrino's bar (series J2): the source, the two readers, the far
# detector and the run.
NU_BAR = 200
NU_K = 4096
NU_SOURCE = 4096
NU_READERS = (8, 9)
NU_FAR = 190
NU_TICKS = 1037


def bar(name: str, length: int, ticks: int, families: list[Json], measured: list[Json]) -> Json:
    return {
        "law": "beam",
        "model_id": f"beam-hand-{name}-v1",
        "shape": [length, 1, 1],
        "boundary": "open",
        "ticks": ticks,
        "K": K,
        "N": N,
        "release": [1, K],
        "suspension": 0,
        "families": families,
        "measured": measured,
    }


def w_families(hand: int | None) -> list[Json]:
    w: Json = {"name": "w", "quantum": 1, "charge": W_CHARGE, "lifetime": 1, "phase": False}
    if hand is not None:
        w["hand"] = hand
    return [
        {"name": "n", "quantum": 0, "phase": False},
        {"name": "p", "quantum": 0, "charge": CHARGE, "phase": False},
        w,
    ]


def w_proton(x: int, hand: int | None) -> Json:
    """A proton; with a hand, the parity filter on the keys' `measure` of
    the W (a world declares only what differs from the keys' table)."""
    found: Json = {"position": [x, 0, 0], "family": "p", "amount": PROTON, "fixed": True}
    if hand is not None:
        found["table"] = {"w": {"rule": "measure", "hand": hand}}
    return found


def w_world(name: str, handed: bool) -> Json:
    hand = -1 if handed else None
    neutron: Json = {
        "position": [2, 0, 0],
        "family": "n",
        "amount": NEUTRON,
        "fixed": True,
        "directions": [PLUS_X, MINUS_X],
        "become": {"at": W_AT, "into": "p", "products": [["w", 1, W_CONTENT]]},
    }
    if handed:
        neutron["axis"] = MINUS_X
    return bar(name, 7, W_TICKS, w_families(hand), [w_proton(1, hand), neutron, w_proton(3, hand)])


def wu_world() -> Json:
    families: list[Json] = [
        {"name": "n", "quantum": 0, "phase": False},
        {"name": "p", "quantum": 0, "charge": CHARGE, "phase": False},
        {"name": "beta", "quantum": 1, "charge": W_CHARGE, "hand": -1},
        {"name": "nubar", "quantum": 0, "hand": 1},
        {"name": "d", "quantum": 1, "phase": False},
    ]
    neutron: Json = {
        "position": [WU_NEUTRON, 0, 0],
        "family": "n",
        "amount": NEUTRON,
        "fixed": True,
        "axis": PLUS_X,
        "become": {
            "at": W_AT,
            "into": "p",
            "products": [["beta", 1, W_CONTENT], ["nubar", 1, 0]],
        },
    }
    readers = [
        {
            "position": [x, 0, 0],
            "family": "d",
            "amount": 1,
            "fixed": True,
            # The keys' `measure` of the beta (a paid arrival) and `pass` of
            # the antineutrino (a free family is read by default).
            "table": {"nubar": "pass"},
        }
        for x in (0, WU_BAR - 1)
    ]
    return bar("wu", WU_BAR, WU_TICKS, families, [readers[0], neutron, readers[1]])


def nu_reader(x: int, hand: int | None) -> Json:
    entry: Json = {"rule": "measure"}
    if hand is not None:
        # The full circle (every phase) and the one hand.
        entry.update({"phase_window": 0, "phase_width": N, "hand": hand})
    return {"position": [x, 0, 0], "family": "d", "amount": 1, "fixed": True, "table": {"nu": entry}}


def nu_world() -> Json:
    world = bar(
        "nu_hand",
        NU_BAR,
        NU_TICKS,
        [{"name": "nu", "quantum": 0, "hand": -1}, {"name": "d", "quantum": 1, "phase": False}],
        [
            {
                "position": [0, 0, 0],
                "family": "nu",
                "amount": NU_SOURCE,
                "phase": 0,
                "fixed": True,
                "directions": [PLUS_X],
            },
            nu_reader(NU_READERS[0], 1),
            nu_reader(NU_READERS[1], -1),
            nu_reader(NU_FAR, None),
        ],
    )
    world["K"] = NU_K
    world["release"] = [1, NU_K]
    return world


def worlds() -> dict[str, Json]:
    return {
        "w_hand": w_world("w_hand", True),
        "w_two_sides": w_world("w_two_sides", False),
        "wu": wu_world(),
        "nu_hand": nu_world(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=HERE, help="Directory of the world files")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for name, world in worlds().items():
        path = args.out / f"{name}.json"
        path.write_text(json.dumps(world, separators=(",", ":")) + "\n", encoding="utf-8")
        print(path)


if __name__ == "__main__":
    main()
