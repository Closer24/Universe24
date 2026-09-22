"""Write the worlds of the moving detector, a cart with a click, and the
pins before any run (`expectations.json`).

The model owner's word of 2026-09-22 (records 816 and 824: no wall; a cart
with a click; make sure we can run in the code Outside with a moving
detector, consecutive clicks). The design, with every pin written from the
Inside step and the conversion before any run, is
docs/designs/moving_detector/DESIGN.md; nothing is run here.

The cart is series O's star and series S's reader in one moving event: a
measured event of the paid family `cart` holding a mass (`held` {"mass":
M}, series G2's kind), a lamp of one unit per self-creation on -x (its
birth ordinals are its own count), a momentum on x that gives the pace v =
1 / k Nodes per self-creation exactly (`p = Q S M / (k - 1)`, the drive's
rule v = p / (Q S M + p), M the content the drive's wall reads: the held
mass plus the light), and a table that measures the lamp's rows (the family
`source`, the missing direction k_AB) and its own pulses returned by the post
(`cart`, stamped with the post's number by the `rerelease` rule: the radar
and the round trip). The lamp A at rest at x = 3 shines +x, one row per
self-creation. The post R at rest at x = 1 re-emits the cart's pulses on +x
(the transponder). Every world declares the key `clock_stamp` so that every
line a measured event writes carries its own count (`clock`), and nothing
of the tick is read by the tool. Every world declares `per_axis_drive`,
the per-axis drive of history its pins were derived under (the rule above;
the law's drive is the line drive since 2026-09-22, the model owner's
record 972, docs/designs/drive_b/DEFAULT.md, under which the cart's pace is
p Q / (Q^2 S M + p T_D), no longer the exact 1 / k): the key is transient,
removed when this series is re-pinned under the law.

| World | k | the pace v | beta = v / c | the bar | the intervals |
| --- | --- | --- | --- | --- | --- |
| `cart_k3` | 3 | 1/3 | 55/96 | 240 | 600 |
| `cart_k5` | 5 | 1/5 | 11/32 | 240 | 600 |
| `cart_k9` | 9 | 1/9 | 55/288 | 240 | 600 |
| `cart_k17` | 17 | 1/17 | 55/544 | 240 | 600 |
| `cart_quantum` | 7/3 | 3/7 (hops at gaps 2, 2, 3) | 165/224 | 320 | 600 |
| `capability_k5` | 5 | 1/5 | 11/32 | 120, no post | 300 |

c = 32 / 55 Nodes per interval on a heading, the flight table's pace.
`capability_k5` is the smallest world of step 4 (the lamp and the cart
only): its consecutive clicks are printed as DETECTOR and nothing is pinned
as nature's.

    python examples/events/moving_detector/make_worlds.py    # the worlds and expectations.json
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from event_universe.core.game_board import PORT_HEADINGS  # noqa: E402
from event_universe.events.nature_beam import direction_flight  # noqa: E402
from event_universe.events.world import HEADING_OFFSET, LAW_VALUE, Q  # noqa: E402

N = 64
# Series O's numbers: the width of the push, the mass the cart holds and its
# release, the light the lamps carry (one unit per self-creation costs one
# content).
WIDTH = 1 << 20
MASS = 1 << 22
RELEASE = [1, 1 << 16]
LIGHT = 1 << 13
LAMP_RATE = [1, 1]
CONTENT = MASS + LIGHT
POST_X = 1
LAMP_X = 3
CART_X = 20
TICKS = 600
CAPABILITY_TICKS = 300
# The windows: k_AB and k_BA from the cart's 60th count; the round trip and
# the radar from the first return to the receding cart, 2 (CART_X - POST_X)
# / (c - v) intervals after the start.
WINDOW_START = 60
EXPECTATIONS_FORMAT = "moving-detector-expectations-v1"
Json = dict[str, object]

PLUS_X = list(PORT_HEADINGS[0])
MINUS_X = list(PORT_HEADINGS[1])


def beam_speed() -> Fraction:
    """The ray's pace on a heading, read off the flight table, as a fraction
    (32 / 55 Nodes per interval)."""
    table = direction_flight(((0, 0, 0), (0, 0, 0), *PORT_HEADINGS))
    heading = np.array([HEADING_OFFSET])
    period = int(table.period[HEADING_OFFSET])
    return Fraction(int(table.manhattan_steps(heading, np.array([period]))[0]), period)


C = beam_speed()
WALL = Q * WIDTH * CONTENT  # Q S M, the drive's wall without the momentum


def momentum(pace: Fraction) -> int:
    """The momentum p (label units) that gives the pace v Nodes per
    self-creation exactly: v = p / (Q S M + p), so p = v Q S M / (1 - v); a
    whole number for every world here (the maker refuses otherwise)."""
    p = pace * WALL / (1 - pace)
    if p.denominator != 1:
        raise ValueError(f"the pace {pace} gives no whole momentum: {p}")
    return int(p)


def pace(p: int) -> Fraction:
    return Fraction(p, WALL + p)


# The worlds: the pace as a fraction, the bar's length, the intervals and
# whether the post stands.
WORLDS: dict[str, tuple[Fraction, int, int, bool]] = {
    "cart_k3": (Fraction(1, 3), 240, TICKS, True),
    "cart_k5": (Fraction(1, 5), 240, TICKS, True),
    "cart_k9": (Fraction(1, 9), 240, TICKS, True),
    "cart_k17": (Fraction(1, 17), 240, TICKS, True),
    "cart_quantum": (Fraction(3, 7), 320, TICKS, True),
    "capability_k5": (Fraction(1, 5), 120, CAPABILITY_TICKS, False),
}


def post() -> Json:
    """The transponder at rest: the cart's pulses re-emitted on +x at its
    next self-creation, stamped with its number (`rerelease`); the source's
    rows never reach it; the cart's mass rows pass."""
    return {
        "position": [POST_X, 1, 1],
        "family": "post",
        "amount": 1,
        "fixed": True,
        "directions": [PLUS_X],
        "table": {"cart": {"rule": "rerelease"}, "source": {"rule": "pass"}, "mass": {"rule": "pass"}},
    }


def source() -> Json:
    """The source, the lamp at rest (the family `source`, since the family
    name `lamp` would read as the lamp key): one row per self-creation on +x toward the cart; the
    returned pulses and the cart's mass rows pass through it. It holds the
    same mass as the cart so that its content equals K and its phase turns
    once per interval (a turn of 0 releases nothing; series O's star); its
    own mass rows go +x to the cart, which lets them pass (no push, so the
    cart's pace stays the drive's exact 1 / k)."""
    return {
        "position": [LAMP_X, 1, 1],
        "family": "source",
        "amount": LIGHT,
        "phase": 0,
        "fixed": True,
        "held": {"mass": MASS},
        "directions": [PLUS_X],
        "lamp": {"rate": LAMP_RATE, "wheel": [1, N], "directions": [PLUS_X]},
        "table": {"cart": {"rule": "pass"}, "mass": {"rule": "pass"}},
    }


def cart(v: Fraction) -> Json:
    """The moving body detector: the momentum for the pace v, a lamp of its
    own on -x, the lamp's rows and its own returned pulses measured (a click
    each, the row's age read)."""
    return {
        "position": [CART_X, 1, 1],
        "family": "cart",
        "amount": LIGHT,
        "phase": 0,
        "momentum": [momentum(v), 0, 0],
        "held": {"mass": MASS},
        "directions": [MINUS_X],
        "lamp": {"rate": LAMP_RATE, "wheel": [1, N], "directions": [MINUS_X]},
        "table": {
            "source": {"rule": "measure", "reads": "age"},
            "cart": {"rule": "measure", "reads": "age"},
            "mass": {"rule": "pass"},
        },
    }


def world(name: str) -> Json:
    v, length, ticks, with_post = WORLDS[name]
    measured = ([post()] if with_post else []) + [source(), cart(v)]
    return {
        "law": LAW_VALUE,
        "model_id": f"beam-moving-detector-{name.replace('_', '-')}-v1",
        "shape": [length, 3, 3],
        "boundary": "open",
        "ticks": ticks,
        "K": CONTENT,
        "N": N,
        "release": RELEASE,
        "suspension": 0,
        "width": WIDTH,
        "clock_stamp": True,
        # The per-axis drive of history (the module docstring): transient.
        "per_axis_drive": True,
        "families": [
            {"name": "post", "quantum": 1},
            {"name": "source", "quantum": 1},
            {"name": "cart", "quantum": 1},
            {"name": "mass", "quantum": 0, "charge": 0, "phase": False},
        ],
        "measured": measured,
    }


def worlds() -> dict[str, Json]:
    return {name: world(name) for name in WORLDS}


# -- The pins before any run (the design's section 5) -------------------------


def hop_gaps(v: Fraction, count: int = 40) -> list[int]:
    """The counts between the cart's hops from the drive's rule (the
    accumulator gains p per self-creation against the wall Q S M + p): the
    closed form, k only when 1 / v is whole, k and k + 1 otherwise."""
    p = momentum(v)
    wall = WALL + p
    acc = 0
    hops: list[int] = []
    n = 0
    while len(hops) < count:
        n += 1
        acc += p
        if acc >= wall:
            acc -= wall
            hops.append(n)
    return [b - a for a, b in zip(hops[:-1], hops[1:], strict=True)]


def pins(name: str) -> Json:
    """Every pin from the Inside step (one row per self-creation at the lamp,
    32 Links per 55 intervals, one Node per k self-creations) and the
    conversion (a ratio of counts apart); Lorentz's one symmetric factor is
    written as the comparison only and enters no pin."""
    v, length, ticks, with_post = WORLDS[name]
    beta = v / C
    k_ab = 1 / (1 - beta)
    k_ba = 1 + beta
    gaps = sorted(set(hop_gaps(v)))
    first_return = math.ceil(2 * (CART_X - POST_X) / (C - v))
    clicks_apart = k_ab  # the cart's counts between two of A's rows
    if len(gaps) == 1:
        node_change = [0, 1]  # A's rows click oftener than the cart hops
    else:
        node_change = [1, 2]  # two hops fall between consecutive clicks
    document: Json = {
        "pace": str(v),
        "momentum": momentum(v),
        "beta": {"fraction": str(beta), "value": float(beta)},
        "windows": {
            "one_way": {"from_count": WINDOW_START, "to": "the last click"},
            "round_trip_and_radar": {"from_count": first_return, "to": "the last return"},
        },
        "tolerance": "2 / W over a window of W counts apart",
        "k_AB": {
            "fraction": str(k_ab),
            "value": float(k_ab),
            "kind": "DETECTOR",
            "reads": "the cart's counts apart over the lamp's ordinals apart",
        },
        "least_step": {
            "per_count": "abs(delta node) <= delta count between any two clicks of the cart",
            "consecutive_clicks_of_the_lamp_rows": node_change,
            "pace_over_the_window": {"fraction": str(v), "value": float(v)},
            "counts_between_hops": {"values": gaps, "kind": "GAMEBOARD", "reads": "the step lines"},
            "clicks_apart": {"fraction": str(clicks_apart), "value": float(clicks_apart)},
        },
        "comparison_not_a_pin": {
            "lorentz_one_way_factor": math.sqrt((1 + beta) / (1 - beta)),
        },
    }
    if with_post:
        document.update(
            {
                "k_BA": {
                    "fraction": str(k_ba),
                    "value": float(k_ba),
                    "kind": "DETECTOR",
                    "reads": "the post's counts apart over the cart's ordinals apart",
                },
                "ratio_k_BA_over_k_AB": {
                    "fraction": str(k_ba / k_ab),
                    "value": float(k_ba / k_ab),
                    "kind": "DETECTOR",
                    "law": "1 - beta^2, stated so that it fails against the comparison 1",
                    "carries": "r_R / r_D^2",
                },
                "round_trip": {
                    "fraction": str(k_ab * k_ba),
                    "value": float(k_ab * k_ba),
                    "kind": "DETECTOR",
                    "reads": "the cart's counts apart between two returns over its ordinals apart between the births they carry; r cancels",
                },
                "radar_velocity": {
                    "fraction": str(-v),
                    "value": float(-v),
                    "kind": "DETECTOR",
                    "reads": "delta x_D / delta t_D with x_D = c (n_r - n_e) / 2 Links, t_D = (n_r + n_e) / 2 counts; Nodes per count",
                },
            }
        )
    return document


def expectations() -> Json:
    return {
        "format": EXPECTATIONS_FORMAT,
        "design": "docs/designs/moving_detector/DESIGN.md section 5",
        "c": {"fraction": str(C), "value": float(C)},
        "wall_Q_S_M": WALL,
        "worlds": {name: pins(name) for name in WORLDS},
    }


def main() -> None:
    for name, document in worlds().items():
        (HERE / f"{name}.json").write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
    (HERE / "expectations.json").write_text(
        json.dumps(expectations(), indent=1) + "\n", encoding="utf-8"
    )
    print(f"{len(WORLDS)} worlds and expectations.json written to {HERE}")


if __name__ == "__main__":
    main()
