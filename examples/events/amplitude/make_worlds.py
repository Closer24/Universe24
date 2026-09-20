"""Write the worlds of series L, the amplitude law (`amplitude-v1`; the
model owner, 2026-09-20, Highlights 5.4, "DECIDED: `amplitude-v1` is
built"; the physicist's and the mathematician's design,
scratchpad/amplitude/DESIGN.md, sections 3.4, 7 and 14), and the
expectations pinned before the runs (`expectations.json`, every integer
the design's, from its check scripts `mz.py` and `slits_read.py`).

L1, the Mach-Zehnder interferometer and Elitzur-Vaidman (the design's
section 3.4, the acceptance tests 1, 3 and 8). A plane of 5 x 5 with z
periodic, K 2^20, N 64, `release` [0, 1], `suspension` 0, `amplitude`
true, 75 intervals. The source at (0, 0), a lamp of `light` of content
2^20 (its turn 1 phase step per self-creation for far more births than
the run holds, so the birth phase u of the record born at tick t is
t - 1: the 64 births of the ticks 1 .. 64 span the circle once and
complete by tick 75, the 11 born after are open at the end) releasing
one record per self-creation on +x (arm 1) and +y (arm 2, the
reflection's quarter turn 16 on the row: the source's own splitter),
two rows of amount 1 with the multiplicity 2 (one quantum on two paths).
Mirror 1 at (3, 0) re-emits +x arrivals on +y, mirror 2 at (0, 3) re-emits
+y arrivals on +x, both `rerelease` on one direction (the equal split with
one weight: no change of amplitude). The splitter at (3, 3), a `rerelease`
whose split table is selected by the arrival (`inputs`): a row arriving
along +y (arm 1) is transmitted on +y toward D2 with the weight a and
reflected on +x toward D1 with the weight b and the quarter turn 16; a row
arriving along +x (arm 2) transmitted on +x toward D1 with a and reflected
on +y toward D2 with b and 16; A = a^2 + b^2 = c^2 for the Pythagorean pair
(20, 21, 29) of the design (the shares 400/841 and 441/841; no triple is
balanced) and 2 for the balanced (1, 1) split the owner admitted. D1 at
(4, 3) and D2 at (3, 4), one-Node detectors reading `sum`.

| world | the splitter | arm 2 | `phase_per_link` | the design's counts over the 64 births |
| --- | --- | --- | --- | --- |
| `mz_equal` | (20, 21) | equal | 0 | D1 64, D2 0 (the offers 1681/1682, 1/1682) |
| `mz_half` | (20, 21) | a half turn 32 on the row | 0 | D1 0, D2 64 |
| `mz_quarter` | (20, 21) | a quarter turn 16 on the row | 0 | D1 32, D2 32 |
| `mz_balanced` | (1, 1) | equal | 0 | D1 64, D2 0 (D2's rows cancel on the lattice) |
| `mz_345` | (3, 4) | equal | 0 | D1 63, D2 1 (the rung moved: u = 63 falls in D2) |
| `mz_unequal_f0` | (20, 21) | longer by two intervals | 0 | D1 64, D2 0 (the rows accumulate in phase) |
| `mz_unequal_f8` | (20, 21) | longer by two intervals | [8, 1] | D1 32, D2 32 (a delay of two intervals at 8 steps per interval is a quarter turn) |
| `mz_unequal_f16` | (20, 21) | longer by two intervals | [16, 1] | D1 0, D2 64 |
| `ev_29` | (20, 21), arm 2 absorbed at (0, 3) | equal | 0 | absorber 32, D1 17, D2 15 |
| `ev_169` | (119, 120), arm 2 absorbed | equal | 0 | absorber 32, D1 16, D2 16 |

"Arm 2 longer by two intervals" is made on the flight table: arm 1
carries two pass-through re-emitters at (3, 1) and (3, 2), each re-born
row starting a fresh digital line whose first step is at its first
interval (m(1) = 1), so each advances arm 1 by one interval; arm 2 then
reaches the ports two intervals after arm 1, and the phase per interval of
age, carried through every re-emission, reads the delay as the design's
f x 2 (the pair form of `phase_per_link` under the key, the owner's
unification (1)). The absorber of Elitzur-Vaidman is a measured event of
`light` at (0, 3) in place of mirror 2 (the keys' rule measures the paid
arrival; a detector of one Node named `absorber`).

    python examples/events/amplitude/make_worlds.py [--out DIR]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
N = 64
QUARTER = N // 4
HALF = N // 2
# The source's content and the clock's rate: the turn is 1 phase step per
# self-creation (content / K) for the first several hundred births.
SOURCE_CONTENT = 1 << 20
CLOCK = 1 << 20
# The last birth of the circle, tick 64, completes at tick 75 (the ports
# click 11 intervals after a birth on the flight table).
MZ_TICKS = 75
PLUS_X = [1, 0, 0]
PLUS_Y = [0, 1, 0]
PYTHAGOREAN_29 = (20, 21)
PYTHAGOREAN_169 = (119, 120)
BALANCED = (1, 1)
PYTHAGOREAN_5 = (3, 4)


def mirror(position: list[int], direction: list[int]) -> dict[str, object]:
    """A re-emitter of `light` on one direction (the equal split with one
    weight: no change of amplitude)."""
    return {
        "position": position,
        "family": "light",
        "amount": 1,
        "fixed": True,
        "table": {"light": "rerelease"},
        "directions": [direction],
    }


def mach_zehnder(
    name: str,
    splitter: tuple[int, int] = PYTHAGOREAN_29,
    arm_turn: int = 0,
    unequal: bool = False,
    frequency: list[int] | None = None,
    absorber: bool = False,
    ticks: int = MZ_TICKS,
) -> dict[str, object]:
    """The Mach-Zehnder world of the design's section 3.4 (the docstring's
    table): `splitter` the pair (a, b), `arm_turn` the phase added to arm
    2's row at the birth beyond the reflection's quarter turn, `unequal`
    the two pass-through re-emitters on arm 1, `frequency` the pair form
    of `phase_per_link`, `absorber` Elitzur-Vaidman's absorber in place of
    mirror 2."""
    a, b = splitter
    family: dict[str, object] = {"name": "light", "quantum": 1}
    if frequency is not None:
        family["phase_per_link"] = list(frequency)
    measured: list[dict[str, object]] = [
        {
            "position": [0, 0, 0],
            "family": "light",
            "amount": SOURCE_CONTENT,
            "fixed": True,
            "lamp": {
                "rate": [1, 1],
                "directions": [PLUS_X, PLUS_Y],
                "turns": [0, (QUARTER + arm_turn) % N],
            },
        },
        mirror([3, 0, 0], PLUS_Y),
    ]
    if absorber:
        measured.append({"position": [0, 3, 0], "family": "light", "amount": 1, "fixed": True})
    else:
        measured.append(mirror([0, 3, 0], PLUS_X))
    if unequal:
        measured.append(mirror([3, 1, 0], PLUS_Y))
        measured.append(mirror([3, 2, 0], PLUS_Y))
    measured.append(
        {
            "position": [3, 3, 0],
            "family": "light",
            "amount": 1,
            "fixed": True,
            "table": {
                "light": {
                    "rule": "rerelease",
                    "inputs": [PLUS_Y, PLUS_X],
                    "weights": [[b, a], [a, b]],
                    "turns": [[QUARTER, 0], [0, QUARTER]],
                }
            },
            "directions": [PLUS_X, PLUS_Y],
        }
    )
    measured.append({"position": [4, 3, 0], "family": "light", "amount": 1, "fixed": True})
    measured.append({"position": [3, 4, 0], "family": "light", "amount": 1, "fixed": True})
    detectors: list[dict[str, object]] = []
    if absorber:
        detectors.append({"name": "absorber", "positions": [[0, 3, 0]], "reading": "sum"})
    detectors.append({"name": "D1", "positions": [[4, 3, 0]], "reading": "sum"})
    detectors.append({"name": "D2", "positions": [[3, 4, 0]], "reading": "sum"})
    return {
        "law": "beam",
        "model_id": f"beam-amplitude-{name}-v1",
        "shape": [5, 5, 1],
        "boundary": {"z": "periodic"},
        "ticks": ticks,
        "K": CLOCK,
        "N": N,
        "release": [0, 1],
        "suspension": 0,
        "amplitude": True,
        "families": [family],
        "measured": measured,
        "detectors": detectors,
    }


def mach_zehnder_worlds() -> dict[str, dict[str, object]]:
    return {
        "mz_equal": mach_zehnder("mz_equal"),
        "mz_half": mach_zehnder("mz_half", arm_turn=HALF),
        "mz_quarter": mach_zehnder("mz_quarter", arm_turn=QUARTER),
        "mz_balanced": mach_zehnder("mz_balanced", splitter=BALANCED),
        "mz_345": mach_zehnder("mz_345", splitter=PYTHAGOREAN_5),
        "mz_unequal_f0": mach_zehnder("mz_unequal_f0", unequal=True),
        "mz_unequal_f8": mach_zehnder("mz_unequal_f8", unequal=True, frequency=[8, 1]),
        "mz_unequal_f16": mach_zehnder("mz_unequal_f16", unequal=True, frequency=[16, 1]),
        "ev_29": mach_zehnder("ev_29", absorber=True),
        "ev_169": mach_zehnder("ev_169", splitter=PYTHAGOREAN_169, absorber=True),
    }


# The design's integers (mz.txt), written before any run: per world the
# offers of one record (exact fractions of the pointer unit, as the design
# states them) and the clicks over the 64 births u = 0 .. 63, in the
# layer's order of the sets.
MACH_ZEHNDER_EXPECTATIONS: dict[str, dict[str, object]] = {
    "mz_equal": {"offers": {"D1": "1681/1682", "D2": "1/1682"}, "clicks": {"D1": 64, "D2": 0}},
    "mz_half": {"offers": {"D1": "1/1682", "D2": "1681/1682"}, "clicks": {"D1": 0, "D2": 64}},
    "mz_quarter": {"offers": {"D1": "1/2", "D2": "1/2"}, "clicks": {"D1": 32, "D2": 32}},
    "mz_balanced": {"offers": {"D1": "1", "D2": "0"}, "clicks": {"D1": 64, "D2": 0}},
    "mz_345": {"offers": {"D1": "49/50", "D2": "1/50"}, "clicks": {"D1": 63, "D2": 1}},
    "mz_unequal_f0": {
        "offers": {"D1": "1681/1682", "D2": "1/1682"},
        "clicks": {"D1": 64, "D2": 0},
    },
    "mz_unequal_f8": {"offers": {"D1": "1/2", "D2": "1/2"}, "clicks": {"D1": 32, "D2": 32}},
    "mz_unequal_f16": {
        "offers": {"D1": "1/1682", "D2": "1681/1682"},
        "clicks": {"D1": 0, "D2": 64},
    },
    "ev_29": {
        "offers": {"absorber": "1/2", "D1": "441/1682", "D2": "200/841"},
        "clicks": {"absorber": 32, "D1": 17, "D2": 15},
    },
    "ev_169": {
        "offers": {"absorber": "1/2", "D1": "7200/28561", "D2": "14161/57122"},
        "clicks": {"absorber": 32, "D1": 16, "D2": 16},
    },
}


def expectations() -> dict[str, object]:
    return {
        "format": "amplitude-expectations-v1",
        "births": N,
        "mach_zehnder": MACH_ZEHNDER_EXPECTATIONS,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--out", type=Path, default=HERE)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for name, world in mach_zehnder_worlds().items():
        path = args.out / f"{name}.json"
        path.write_text(json.dumps(world) + "\n", encoding="utf-8")
        print(
            f"{path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}: {world['ticks']} intervals"
        )
    (args.out / "expectations.json").write_text(
        json.dumps(expectations(), indent=1) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
