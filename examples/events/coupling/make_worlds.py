"""Write the worlds of the coupling series C under the law of the ray, on
the plane.

One base world, the items' worlds from it (README.md here; the entry "C, the
couplings under the law of the ray, on the plane (2026-09-19)" in
docs/EXPERIMENTS.md; the readings under the law of events stay registered
as history). The series runs on a two-dimensional board by the
model owner's decision of 2026-09-19 ("cancel the runs; let it run on
two-dimensional boards"): a board of 121 x 121 x 1 with the z axis declared
periodic (`"boundary": {"z": "periodic"}`), so that the two z Ports of every
Node return to the same Node at the next interval and nothing leaks; the
centre c = (60, 60, 0), K 2^22, N 64, `release` [1, 128], `suspension` 0
(1 in world 6 only), the free family `m` (`quantum` 0, the kind following
from the quantum; charge 0; the family `q` of item 7 carries the charges),
the source a fixed measured event of content 2^24
at c (2^17 rays per heading at every self-creation; the two z headings'
rays step onto the source's own Node through the stub and come home, to be
created again over the six headings, so the net emission into the plane is
q = 6 x 2^17 = 786432 units per interval at the fixed point, exact), the
probes fixed measured events of content 1 (m in item 1) with the default
table (`read`: the push taken, the rays go on).
The worlds:

- item 1, equivalence: `1a_m<m>` one fixed probe of content m in 1, 4, 16 at
  (72, 60, 0), r = 12 on +x; `1b_m<m>` the same probe free (`fixed` false,
  momentum 0; since 2026-09-19 a step onto the source is refused, so the free
  probe ends beside it);
- item 2, the third law with unequal contents: `2`, A = 2^22 at (56, 60, 0)
  and B = 2^20 at (64, 60, 0), both fixed;
- item 3, superposition: `3` the item-2 world with a fixed probe of content 1
  at (60, 68, 0); `3a` and `3b` each source alone with the same probe (A is
  number 1 in `3` and `3a`, B number 2 in `3` and `3b`);
- item 4, retardation: `4`, the source with content-1 probes at r = 4 on -x,
  6 on +y, 8 on -y and 12 on +x (one radius per axis of the plane, the
  probes off each other's lines), the first read of each probe the reading;
- item 5, the far field: `5` the source alone, 300 intervals; `5p` the source
  with content-1 probes at r = 4, 6, 8, 12, 16, 20, 24, 30, 40 on +x (all on
  the source's line, allowed for this item: the axis pattern); `5_long` the
  source alone for 1000 intervals, the supplementary world added after the
  300-interval run read an escape of 0.89 q over its last window (the
  fixed point not reached), to read how the escape approaches q;
- item 6, the clock: `6`, the probes of `5p` with `suspension` 1;
- item 7, the electric reading: `7_<Qq>` with Q in 0, +2^23, -2^23 on the
  source and q in 0, +2, -2 on the content-1 probe at (72, 60, 0), the pairs
  00, pp, pm, mp, mm, and `7_pp_m4` the (+, +) pair with a probe of content 4
  at the same Node.

Every world runs 200 intervals but `5` (300) and `5_long` (1000).

    python examples/events/coupling/make_worlds.py
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIDE = 121
SHAPE = [SIDE, SIDE, 1]
BOUNDARY = {"z": "periodic"}
CENTRE = (60, 60, 0)
K = 1 << 22
N = 64
RELEASE = [1, 128]
SOURCE = 1 << 24
TICKS = 200
FAR_TICKS = 300
LONG_TICKS = 1000
FAR_RADII = (4, 6, 8, 12, 16, 20, 24, 30, 40)
CHARGE = 1 << 23
PROBE_CHARGE = 2
PROBE_RADIUS = 12
AXES = {
    "+x": (1, 0, 0),
    "-x": (-1, 0, 0),
    "+y": (0, 1, 0),
    "-y": (0, -1, 0),
}
# Item 4: the probes of world 4, one radius per axis of the plane.
RETARDATION_PROBES = (("-x", 4), ("+y", 6), ("-y", 8), ("+x", PROBE_RADIUS))
Json = dict[str, object]


def at(axis: str, radius: int) -> list[int]:
    """The Node at `radius` Links from the centre along an axis of the plane."""
    heading = AXES[axis]
    return [CENTRE[i] + radius * heading[i] for i in range(3)]


def measured(
    position: list[int],
    amount: int,
    *,
    family: str = "m",
    fixed: bool = True,
    charge: int | None = None,
    momentum: list[int] | None = None,
) -> Json:
    entry: Json = {"position": position, "family": family, "amount": amount, "phase": 0, "fixed": fixed}
    if charge is not None:
        entry["charge"] = charge
    if momentum is not None:
        entry["momentum"] = momentum
    return entry


def world(
    name: str, entries: list[Json], *, ticks: int = TICKS, suspension: int = 0, family: str = "m"
) -> Json:
    return {
        "law": "rays",
        "model_id": f"rays-coupling-{name.replace('_', '-')}-plane-v1",
        "shape": list(SHAPE),
        "boundary": dict(BOUNDARY),
        "ticks": ticks,
        "K": K,
        "N": N,
        "release": RELEASE,
        "suspension": suspension,
        "families": [{"name": family, "quantum": 0, "charge": 0}],
        "measured": entries,
    }


def source(*, family: str = "m", charge: int | None = None) -> Json:
    return measured(list(CENTRE), SOURCE, family=family, charge=charge)


def far_probes(*, family: str = "m") -> list[Json]:
    return [measured(at("+x", r), 1, family=family) for r in FAR_RADII]


def worlds() -> dict[str, Json]:
    found: dict[str, Json] = {}
    probe_node = at("+x", PROBE_RADIUS)
    for m in (1, 4, 16):
        found[f"1a_m{m}"] = world(f"1a_m{m}", [source(), measured(probe_node, m)])
        found[f"1b_m{m}"] = world(
            f"1b_m{m}", [source(), measured(probe_node, m, fixed=False, momentum=[0, 0, 0])]
        )
    a, b = measured(at("-x", 4), 1 << 22), measured(at("+x", 4), 1 << 20)
    found["2"] = world("2", [a, b])
    side = measured(at("+y", 8), 1)
    found["3"] = world("3", [a, b, side])
    found["3a"] = world("3a", [a, side])
    found["3b"] = world("3b", [side, b])
    found["4"] = world("4", [source(), *(measured(at(axis, r), 1) for axis, r in RETARDATION_PROBES)])
    found["5"] = world("5", [source()], ticks=FAR_TICKS)
    found["5_long"] = world("5_long", [source()], ticks=LONG_TICKS)
    found["5p"] = world("5p", [source(), *far_probes()])
    found["6"] = world("6", [source(), *far_probes()], suspension=1)
    signs = {"0": 0, "p": 1, "m": -1}
    for pair in ("00", "pp", "pm", "mp", "mm"):
        big, small = signs[pair[0]] * CHARGE, signs[pair[1]] * PROBE_CHARGE
        found[f"7_{pair}"] = world(
            f"7_{pair}",
            [
                source(family="q", charge=big),
                measured(probe_node, 1, family="q", charge=small),
            ],
            family="q",
        )
    found["7_pp_m4"] = world(
        "7_pp_m4",
        [
            source(family="q", charge=CHARGE),
            measured(probe_node, 4, family="q", charge=PROBE_CHARGE),
        ],
        family="q",
    )
    return found


def main() -> None:
    for name, document in worlds().items():
        path = HERE / f"{name}.json"
        path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
        print(path.relative_to(HERE.parents[2]))


if __name__ == "__main__":
    main()
