"""The one-world arrangement of R2 (the Sagnac ratio) after the reviewer's
ruling on RUNS.md section 4 (the collision, item 3 of the interval): the
worlds and the pins of PINS_R2.md (the New Rows Scout, 2026-09-23; docs
only, no run).

Writes `worlds/sagnac2_k<k>.json` for k = 3, 5, 9, 17 (every declaration
under existing keys: `boundary` per axis, `age_bound`, `clock_stamp`, a
lamp's `directions`, `measure` at both bodies; no engine line, no key of a
hypothesis),
validates each at load through the shipped loader (`load_world`) and never
runs one, and writes the pins `new_rows_r2_pins.json` with its print
`new_rows_r2_pins.out`, every number a COMPUTATION from the closed forms
(the r-free line of docs/ALGEBRA.md 5.1; each pulse clicked directly at
the other body, the reviewer's gate of 2026-09-23) on the engine's own
flight table, before any run.

Usage: `PYTHONPATH=src python docs/designs/new_rows/new_rows_r2_worlds.py`.
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

from event_universe.events.nature_beam import direction_flight  # noqa: E402
from event_universe.events.world import HEADING_OFFSET, Q  # noqa: E402
from event_universe.world_loading import load_world  # noqa: E402

WORLDS = HERE / "worlds"
Json = dict[str, object]

# The cart of RUN_4AB (series O's numbers) on a periodic bar, with a
# co-moving body E one Node behind it: the reviewer's arrangement (RUNS.md
# section 4, the ruling of 2026-09-23; PINS_R2.md as gated). Two numbers,
# two classes of the collision: the cart's +x pulse and E's -x pulse pass
# through each other; each body clicks the other's pulse directly, so the
# click's deposit of content is symmetric and the two drives stay in step.
TICKS = 1500
BAR = 240
AGE_BOUND = 1500
CART_WIDTH = 1 << 20
CART_K = 4202496
CART_HELD = 4194304
CART_AMOUNT = 8192
LADDER = (3, 5, 9, 17)
FROM_COUNT = 60
CART_X = 20
E_X = 19
DWELL = Fraction(55, 32)  # one Link of a heading row, intervals (the flight table)


def body(x: int, momentum: int, lamp_direction: list[int], table: Json) -> Json:
    """A body of the cart's family, momentum and content (the same
    accumulators as the cart's: it hops in step), with one lamp direction
    and the table given; its `directions` (the mass release) +x."""
    return {
        "position": [x, 1, 1],
        "family": "cart",
        "amount": CART_AMOUNT,
        "phase": 0,
        "momentum": [momentum, 0, 0],
        "held": {"mass": CART_HELD},
        "directions": [[1, 0, 0]],
        "lamp": {"rate": [1, 1], "wheel": [1, 64], "directions": [lamp_direction]},
        "table": table,
    }


def world(k: int) -> Json:
    momentum = Q * CART_WIDTH * CART_K // (k - 1)
    return {
        "law": "beam",
        "model_id": f"beam-new-rows-sagnac2-k{k}-v1",
        "shape": [BAR, 3, 3],
        "boundary": {"x": "periodic"},
        "ticks": TICKS,
        "K": CART_K,
        "N": 64,
        "release": [1, 65536],
        "suspension": 0,
        "width": CART_WIDTH,
        "age_bound": AGE_BOUND,
        "clock_stamp": True,
        "families": [
            {"name": "cart", "quantum": 1},
            {"name": "mass", "quantum": 0, "charge": 0, "phase": False},
        ],
        "measured": [
            # The cart D: the +x pulse alone; it clicks E's -x pulse on its
            # arrival from the +x side, the line stamped with its own count.
            body(
                CART_X,
                momentum,
                [1, 0, 0],
                {"cart": {"rule": "measure", "reads": "age"}, "mass": {"rule": "pass"}},
            ),
            # The body E, one Node behind: the -x pulse alone; it clicks the
            # cart's +x pulse on its arrival from the -x side, the line
            # stamped with its own count (both bodies measure: the click
            # deposits the row's content, so both M change alike).
            body(
                E_X,
                momentum,
                [-1, 0, 0],
                {"cart": {"rule": "measure", "reads": "age"}, "mass": {"rule": "pass"}},
            ),
        ],
    }


def loaded(document: Json):
    return load_world(json.dumps(document).encode("utf-8"), base_dir=WORLDS, root=ROOT)


def heading_pace(flight) -> Fraction:
    heading = np.array([HEADING_OFFSET])
    period = int(flight.period[HEADING_OFFSET])
    return Fraction(int(flight.manhattan_steps(heading, np.array([period]))[0]), period)


def pins(k: int, c: Fraction) -> Json:
    """The two returns of one ordinal, one at each body. E's -x pulse, born
    one Node behind the cart at the same count, goes round the loop and
    meets the cart from the +x side at c + v after L - 1 Links: t_- = (L -
    1) / (c + v), clicked at the cart. The cart's +x pulse goes round and
    meets E from the -x side at c - v after L - 1 Links: t_+ = (L - 1) / (c
    - v), clicked at E. Both exact in the mean (ALGEBRA.md 4.1; the tables
    and the releases run in one interval, no dwell added). The two bodies'
    counts are one clock by construction (both the age, suspension 0), so
    (n_+ - n_-) / (n_+ + n_- - 2 n_0) = (t_+ - t_-) / (t_+ + t_-) = v / c =
    beta exactly, r-free, no arrangement constant."""
    v = Fraction(1, k)
    beta = v / c
    t_minus = (BAR - 1) / (c + v)
    t_plus = (BAR - 1) / (c - v)
    ratio = (t_plus - t_minus) / (t_plus + t_minus)
    remainder_minus = k + DWELL  # one hop plus one dwell at the direct click
    remainder_plus = k + DWELL  # one hop plus one dwell at the direct click at E
    band = (remainder_minus + remainder_plus) / (t_plus + t_minus)
    return {
        "k": k,
        "momentum": Q * CART_WIDTH * CART_K // (k - 1),
        "pace_links_per_interval": str(v),
        "heading_c": str(c),
        "beta_on_the_heading": {"exact": str(beta), "value": float(beta)},
        "returns_after_the_birth_intervals": {
            "kind": "GAMEBOARD (the ticks; the cart's count equals them at r = 1, suspension 0)",
            "minus_x_at_the_cart": {
                "form": "(L - 1) / (c + v)",
                "exact": str(t_minus),
                "value": float(t_minus),
            },
            "plus_x_at_E": {"form": "(L - 1) / (c - v)", "exact": str(t_plus), "value": float(t_plus)},
            "ordinals_with_both_returns_inside_the_run": int(TICKS - math.ceil(t_plus)),
        },
        "ratio": {
            "kind": "DETECTOR (the stamps); CONVERSION (the ratio)",
            "line": "(n_+ - n_-) / (n_+ + n_- - 2 n_0) per ordinal from the cart's count "
            f"{FROM_COUNT}: n_+ from E's clock (its click of the cart's +x pulse, the record the cart's "
            "ordinal), n_- from the cart's clock (its click of E's -x pulse, the record E's ordinal), "
            "n_0 the common birth count (the birth stamp once branch birth-stamp lands); the two clocks one "
            "by construction (both counts the age, suspension 0), checked on the stamps; the mean over the window",
            "pin": {"exact": str(ratio), "value": float(ratio)},
            "beta": {"exact": str(beta), "value": float(beta)},
            "pin_less_beta": float(ratio - beta),
            "reads": "v / c exactly, r-free, no arrangement constant (ALGEBRA.md 5.1)",
            "comparison": "the Sagnac ratio v / c, Michelson-Gale 1925 (the first-order form)",
        },
        "band": {
            "kind": "COMPUTATION",
            "remainder_minus_end_counts": {
                "exact": str(remainder_minus),
                "value": float(remainder_minus),
            },
            "remainder_plus_end_counts": {"exact": str(remainder_plus), "value": float(remainder_plus)},
            "on_the_ratio": float(band),
            "reads": "the meeting remainder (one hop 1 / v plus one dwell 55 / 32) at each direct click, "
            "over the sum of the two returns (RUN_4AB 6.3)",
        },
    }


def main() -> None:
    WORLDS.mkdir(exist_ok=True)
    validated: dict[str, str] = {}
    flight = None
    for k in LADDER:
        document = world(k)
        (WORLDS / f"sagnac2_k{k}.json").write_text(
            json.dumps(document, indent=None, separators=(", ", ": ")) + "\n", encoding="utf-8"
        )
        parsed = loaded(document)
        validated[f"sagnac2_k{k}"] = parsed.world.model_id
        if flight is None:
            flight = direction_flight(parsed.world.directions)
            assert parsed.world.age_bound == AGE_BOUND
    assert flight is not None
    c = heading_pace(flight)
    found: Json = {
        "format": "new-rows-r2-pins-v1",
        "worlds_validated_at_load": validated,
        "held_mass": "kept as registered (the cart's M = 4194304 + 8192, K = 4202496); the mass rows a class of their own "
        "(amount 64, a crowd slot, never a single), colliding with nothing of content 1",
        "R2": {f"sagnac2_k{k}": pins(k, c) for k in LADDER},
    }
    (HERE / "new_rows_r2_pins.json").write_text(json.dumps(found, indent=2) + "\n", encoding="utf-8")
    lines = [
        "THE PINS OF PINS_R2.md, BEFORE ANY RUN (COMPUTATION; the worlds validated at load, none run)",
        "",
        "Worlds validated at load: " + ", ".join(f"{a} ({b})" for a, b in validated.items()),
        f"c = {c} on the heading (the engine's flight table); L = {BAR}; age_bound {AGE_BOUND}; {TICKS} intervals",
        "",
    ]
    for k in LADDER:
        p = found["R2"][f"sagnac2_k{k}"]  # type: ignore[index]
        r = p["returns_after_the_birth_intervals"]
        lines.append(
            f"k = {k}: beta = {p['beta_on_the_heading']['exact']} = {p['beta_on_the_heading']['value']:.5f}; "
            f"t_- = {r['minus_x_at_the_cart']['exact']} = {r['minus_x_at_the_cart']['value']:.2f}, "
            f"t_+ = {r['plus_x_at_E']['exact']} = {r['plus_x_at_E']['value']:.2f} intervals; "
            f"{r['ordinals_with_both_returns_inside_the_run']} ordinals with both returns inside {TICKS}; "
            f"the ratio's pin {p['ratio']['pin']['exact']} = {p['ratio']['pin']['value']:.5f} "
            f"(beta exactly, the pin less beta {p['ratio']['pin_less_beta']:+.5f}); the band {p['band']['on_the_ratio']:.4f} "
            f"(over beta {p['band']['on_the_ratio'] / p['beta_on_the_heading']['value']:.3f}) "
            f"(the remainders {p['band']['remainder_minus_end_counts']['value']:.2f} and "
            f"{p['band']['remainder_plus_end_counts']['value']:.2f} counts)"
        )
    (HERE / "new_rows_r2_pins.out").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
