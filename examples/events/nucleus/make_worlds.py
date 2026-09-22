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

The bodies' drive (since 2026-09-22 the law's line drive, the model
owner's record 972, docs/designs/drive_b/DEFAULT.md; the registered runs
of 2026-09-20 were read under the per-axis drive of history, the world key
`per_axis_drive`): the pushes above are the design's integers under either
drive (a push is a row's label, the drive reads the momentum after it),
and what the drive moves is the pace of a kicked body (10^12 on a heading:
the line drive's p Q / (Q^2 S M + p T_D) = 0.0300 for a proton, the
per-axis p / (Q S M + p) = 0.0307) and the tick of a pushed body's first
Link (the toy: a constant push F per interval from its onset, the
accumulator against the wall). `expectations(drive, centred)` writes
`expectations.json` with these, every entry with its source in
`derivations`; the eight world files carry no momentum but the kicks and
are the same under either drive.

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

from event_universe.register_map import carry_replicated  # noqa: E402
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
# The two drives a body's step is derived under (docs/designs/drive_b/DEFAULT.md
# section (c)): the line drive, the law's since 2026-09-22 (the accumulator
# gains p_a Q per interval against the wall Q^2 S M + |p|_1 T_D), and the
# per-axis drive of history (p_a against Q S M + |p_a|; the world key
# `per_axis_drive`), the drive the registered runs were read under.
LINE_DRIVE = "line"
AXIS_DRIVE = "axis"
DRIVE = LINE_DRIVE
Q = 64
T_D_AXIS = 110  # the axis direction's period constant, isqrt(3 Q^2)
EXPECTATIONS_FORMAT = "nucleus-expectations-v1"
# The design's pushes per interval (README.md, the physicist's integers;
# the readings tool holds the same numbers): the toy of the dispersal's
# first step reads them as a constant push from its onset tick.
DEUTERON_PUSH = 310_967_280_640
DEUTERON_GRAVITY = 1_067_524_788
PP_PUSH = 148_716_220_864
PP_WEAK_PUSH = 4_691_779_136
PP_3_PUSH = 15_977_466_864
SQUARE_P4_PUSH = (355_957_892_670, 320_048_730_393, 0)
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


def pace(p: int, content: int, drive: str = DRIVE) -> float:
    """A body's pace at the momentum p on a heading, Links per interval: the
    line drive's p Q / (Q^2 S M + p T_D) or the per-axis drive of history's
    p / (Q S M + p)."""
    if drive == LINE_DRIVE:
        return p * Q / (Q * Q * WIDTH * content + p * T_D_AXIS)
    if drive == AXIS_DRIVE:
        return p / (Q * WIDTH * content + p)
    raise ValueError(f"unknown drive {drive!r}")


def first_link(
    push: tuple[int, int, int],
    content: int,
    onset: int,
    kick: tuple[int, int, int] = (0, 0, 0),
    drive: str = DRIVE,
    centred: bool = False,
    limit: int = TICKS,
) -> int | None:
    """The toy of a body's first Link, a GAMEBOARD number: from the onset
    tick the momentum grows by the constant push per interval on top of the
    kick, the drive's accumulators gain their rates against the wall (the
    line drive: p_a Q against Q^2 S M + |p|_1 T_D, the axis furthest over
    the wall carrying; the per-axis drive: p_a against Q S M + |p_a| on
    each axis), the threshold half the wall under `centred_step`; the
    interval of the first carry, or None within `limit`."""
    momentum = list(kick)
    drives = [0, 0, 0]
    for tick in range(1, limit + 1):
        if tick >= onset:
            momentum = [m + f for m, f in zip(momentum, push, strict=True)]
        if drive == LINE_DRIVE:
            wall = Q * Q * WIDTH * content + sum(abs(m) for m in momentum) * T_D_AXIS
            threshold = wall - wall // 2 if centred else wall
            drives = [d + m * Q for d, m in zip(drives, momentum, strict=True)]
            over = [abs(d) - threshold for d, m in zip(drives, momentum, strict=True) if m]
            if over and max(over) >= 0:
                return tick
        elif drive == AXIS_DRIVE:
            drives = [d + m for d, m in zip(drives, momentum, strict=True)]
            for d, m in zip(drives, momentum, strict=True):
                wall = Q * WIDTH * content + abs(m)
                threshold = wall - wall // 2 if centred else wall
                if m and abs(d) >= threshold:
                    return tick
        else:
            raise ValueError(f"unknown drive {drive!r}")
    return None


def expectations(drive: str = DRIVE, centred: bool = False) -> Json:
    """The pins before the runs under the named drive (the module docstring):
    the design's pushes are README.md's table under either drive; here the
    drive-dependent numbers, every entry with its source in `derivations`.
    The shipped register is `expectations()`; `expectations(AXIS_DRIVE)`
    reproduces the numbers the registered runs of 2026-09-20 were read
    under."""
    if drive == LINE_DRIVE:
        drive_note = (
            "the line drive, the law's drive of a body since 2026-09-22 (BEAM_LAW note 17 as amended, "
            "note 49; the model owner's record 972): the accumulators gain p_a Q per interval against "
            "the one wall Q^2 S M + |p|_1 T_D, the axis furthest over the wall carrying"
        )
    else:
        drive_note = (
            "the per-axis drive of history (BEAM_LAW note 17 as it ran until 2026-09-22, the world key "
            "`per_axis_drive`): each axis's accumulator gains p_a against Q S M + |p_a|"
        )
    m_p, m_n = PROTON + 1, NEUTRON + 1
    return {
        "format": EXPECTATIONS_FORMAT,
        "derivations": {
            "pushes": "declared: the design's integers per interval (README.md, the table of the expectations; the physicist's design of the strong force): a push is a row's label read at the body, the same under either drive",
            "drive": "declared: " + drive_note,
            "centred": "declared (docs/designs/drive_b/DEFAULT.md section (e), record 955): under `centred_step` the first Link comes at half the wall; the column the model owner decides at the paper's close",
            "kick_pace": "GAMEBOARD: the pace of the kicked body at 10^12 on a heading before any push, the drive's rule at the content M + 1 (the held unit)",
            "first_link": "GAMEBOARD, the toy: a constant push per interval from its onset tick on top of the kick (the design's numbers), the drive's accumulators against the wall; the tick of the first carry, or none within the run (the registered runs read the first steps off the `step` lines, which the toy brackets and does not pin: the fan's lines arrive over the first ticks and the hand-overs at contacts move the momenta)",
            "width": "declared",
        },
        "drive": drive,
        "centred": centred,
        "width": WIDTH,
        "kick": KICK,
        "worlds": {
            "deuteron_3": {
                "kick_pace": {"p": pace(KICK, m_p, drive), "n": pace(KICK, m_n, drive)},
                "first_link": {
                    "p": first_link((-DEUTERON_GRAVITY, 0, 0), m_p, 6, (-KICK, 0, 0), drive, centred),
                    "n": first_link((DEUTERON_GRAVITY, 0, 0), m_n, 6, (KICK, 0, 0), drive, centred),
                },
                "separates": "beyond 10 Links, never returns, both leave through the faces (README.md)",
            },
            "deuteron_1_kick": {
                "kick_pace": {"p": pace(KICK, m_p, drive), "n": pace(KICK, m_n, drive)},
                "first_link": {
                    "p": first_link((DEUTERON_PUSH, 0, 0), m_p, 2, (-KICK, 0, 0), drive, centred),
                    "n": first_link((-DEUTERON_PUSH, 0, 0), m_n, 2, (KICK, 0, 0), drive, centred),
                },
                "kick_outweighed_by": "tick 5 (3.1 x 10^11 x 4 > 10^12); no step (README.md)",
            },
            "pp_1_weak": {
                "first_link": first_link((-PP_WEAK_PUSH, 0, 0), m_p, 2, drive=drive, centred=centred),
                "bracket": [1, 200],
            },
            "pp_3": {
                "first_link": first_link((-PP_3_PUSH, 0, 0), m_p, 6, drive=drive, centred=centred),
                "bracket": [30, 60],
            },
            "alpha_square": {
                "first_link_p4": first_link(SQUARE_P4_PUSH, m_p, 3, drive=drive, centred=centred),
                "bracket": [1, 100],
            },
            "no_step": ["deuteron_1", "pp_1", "alpha_line"],
        },
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
    register = args.out / "expectations.json"
    register.write_text(
        json.dumps(carry_replicated(register, expectations()), indent=1) + "\n", encoding="utf-8"
    )
    expected = expectations()
    print(
        f"the {DRIVE} drive: the kicked deuteron's pace {expected['worlds']['deuteron_3']['kick_pace']['p']:.4f}, "
        f"the toy's first Links {expected['worlds']['deuteron_3']['first_link']}, "
        f"pp_1_weak {expected['worlds']['pp_1_weak']['first_link']}, pp_3 {expected['worlds']['pp_3']['first_link']}, "
        f"alpha_square p4 {expected['worlds']['alpha_square']['first_link_p4']}"
    )
    print(register)


if __name__ == "__main__":
    main()
