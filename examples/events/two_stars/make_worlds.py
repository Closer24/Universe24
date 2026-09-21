"""Write the three worlds of series O, two stars moving toward each other, each
the detector of the other, under the Beam Law, and the expectations before
the runs (`expectations.json`).

The model owner's request (2026-09-21, in conversation with the G2
experimenter): "document an experiment of two stars moving toward each
other; they are creatures from outside": each star is an observer external
to the other, and both are external to the lattice, so the experiment asks
what two outside observers read of each other, whether they read each other
alike, and whether their readings show the lattice's own frame (the owner's
form of Lorentz, record 162 of docs/LOG_2026-09-20.md: "a moving body is a
detector moving over the Nodes"). The design is
docs/designs/two_stars/DESIGN.md; nothing is run here and nothing is
registered.

The two stars are the catalog's star (docs/ENTITY_CATALOG.md): one measured
event of a paid family of its own (`s_px1`, `s_mx1`: the two families of
series G2's inner x stars, defined in entities/families.json) that holds a
mass (`held` {"mass": M}, the free family `mass`, the universal gravity
column) and is a lamp of rate 1 unit per self-creation on BOTH headings of
the axis (each unit costing E = h f = 1 content and carrying the star's clock
phase at birth): the inward light reaches the other star, the outward light
reaches a fixed lab detector behind the star. Each star's table entry for
the other's light is `{"rule": "measure", "reads": "age"}`: the star clicks
the other's light, the click line carrying the row's phase and its age (the
flight time); the star IS the detector. Two fixed detectors of the paid
family `detector` at the ends of the bar read the outward light the same
way (the lattice's frame). The mass rows (F = M x release per direction per
self-creation) go both ways on the axis: each star reads the other's rows
(`read`, the default: the push toward the emitter, the gravity between them)
and the detectors read them for nothing (fixed).

Three worlds on a bar of 201 x 3 x 3 Nodes (open; the rows fly on the axis
headings only), 500 intervals, no suspension (k = 0, no clock slows: the
question is the motion's reading alone):

| World | star A (`s_px1`, x = 70) | star B (`s_mx1`, x = 130) | the mass entry | the question |
| --- | --- | --- | --- | --- |
| `symmetric` | +v (toward B) | -v (toward A) | `read` (gravity on) | the two outsiders in the symmetric frame |
| `rest_frame` | +2v (toward B) | at rest | `read` | the same closing speed with one star in the lattice's frame |
| `symmetric_pass` | +v | -v | `pass` (gravity off) | the control: the motion's reading without the push |

v = 0.2 c on the lattice (c = 32 / 55 Links per interval on a heading), so
the closing speed is 0.4 c in every world; the momentum from the speed by
the drive's rule v = p / (Q S M + p), the content the light plus the mass.

    python examples/events/two_stars/make_worlds.py            # the worlds and expectations.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from event_universe.core.game_board import PORT_HEADINGS  # noqa: E402
from event_universe.events.nature_beam import direction_flight  # noqa: E402
from event_universe.events.world import HEADING_OFFSET, LAW_VALUE, Q  # noqa: E402
from event_universe.register_map import carry_replicated  # noqa: E402

LENGTH = 201
SHAPE = [LENGTH, 3, 3]
CENTRE = (LENGTH // 2, 1, 1)
N = 64
TICKS = 500
# The width of the push, as in series G2: a row of amount a moves a star's
# speed by (1 - v)^2 a / S.
WIDTH = 1 << 20
# The mass a star holds and its release: F = MASS / 2^16 = 64 units per
# direction per self-creation, series G2's gravity crowd.
MASS = 1 << 22
RELEASE = [1, 1 << 16]
# The light a star carries (one unit per self-creation per heading costs 1
# content; 2 x TICKS units are spent of LIGHT over the run, 1000 of 8192).
LIGHT = 1 << 13
LAMP_RATE = [1, 1]
# The two stars' Nodes and the two lab detectors' Nodes on the axis.
STAR_A_X = 70
STAR_B_X = 130
LAB_LEFT_X = 5
LAB_RIGHT_X = 195
# The speed on the lattice, as a fraction of c.
SPEED_OVER_C = 0.2
WINDOWS = ((50, 150), (150, 250))
EXPECTATIONS_FORMAT = "two-stars-expectations-v1"
Json = dict[str, object]

PLUS_X = list(PORT_HEADINGS[0])
MINUS_X = list(PORT_HEADINGS[1])


def beam_speed() -> float:
    """The ray's speed on a heading, read off the flight table."""
    table = direction_flight(((0, 0, 0), (0, 0, 0), *PORT_HEADINGS))
    heading = np.array([HEADING_OFFSET])
    period = int(table.period[HEADING_OFFSET])
    return int(table.manhattan_steps(heading, np.array([period]))[0]) / period


C = beam_speed()
CONTENT = MASS + LIGHT


def momentum(v: float, content: int) -> int:
    """The momentum p (label units) that gives the speed v (Links per
    interval) to a free measured event of content `content`: v = p / (Q S
    M + p)."""
    return round(Q * WIDTH * content * v / (1 - v))


def speed(p: int, content: int) -> float:
    return p / (Q * WIDTH * content + p)


# The three worlds: the two stars' speeds on the lattice as fractions of c
# (positive toward +x) and the rule of the mass entry at a star.
WORLDS: dict[str, tuple[float, float, str]] = {
    "symmetric": (SPEED_OVER_C, -SPEED_OVER_C, "read"),
    "rest_frame": (2 * SPEED_OVER_C, 0.0, "read"),
    "symmetric_pass": (SPEED_OVER_C, -SPEED_OVER_C, "pass"),
}


def star(name: str, x: int, v_over_c: float, mass_rule: str, other: str) -> Json:
    v = v_over_c * C
    p = momentum(abs(v), CONTENT) * (1 if v > 0 else -1 if v < 0 else 0)
    table: Json = {other: {"rule": "measure", "reads": "age"}}
    # A world declares only what differs from the generated table: `read`
    # is a free family's default, so the mass entry is written for `pass`.
    if mass_rule != "read":
        table["mass"] = {"rule": mass_rule}
    return {
        "position": [x, CENTRE[1], CENTRE[2]],
        "family": name,
        "amount": LIGHT,
        "phase": 0,
        "momentum": [p, 0, 0],
        "held": {"mass": MASS},
        "directions": [PLUS_X, MINUS_X],
        "lamp": {"rate": LAMP_RATE, "wheel": [1, N], "directions": [PLUS_X, MINUS_X]},
        "table": table,
    }


def lab(x: int) -> Json:
    return {
        "position": [x, CENTRE[1], CENTRE[2]],
        "family": "detector",
        "amount": 1,
        "fixed": True,
        "table": {name: {"rule": "measure", "reads": "age"} for name in ("s_px1", "s_mx1")},
    }


def world(name: str) -> Json:
    v_a, v_b, mass_rule = WORLDS[name]
    return {
        "law": LAW_VALUE,
        "model_id": f"rays-two-stars-{name.replace('_', '-')}-v1",
        "shape": list(SHAPE),
        "boundary": "open",
        "ticks": TICKS,
        "K": CONTENT,
        "N": N,
        "release": RELEASE,
        "suspension": 0,
        "width": WIDTH,
        "families": [
            {"name": "detector", "quantum": 1},
            {"name": "mass", "quantum": 0, "charge": 0, "phase": False},
            {"name": "s_px1", "quantum": 1},
            {"name": "s_mx1", "quantum": 1},
        ],
        "measured": [
            lab(LAB_LEFT_X),
            lab(LAB_RIGHT_X),
            star("s_px1", STAR_A_X, v_a, mass_rule, "s_mx1"),
            star("s_mx1", STAR_B_X, v_b, mass_rule, "s_px1"),
        ],
    }


def worlds() -> dict[str, Json]:
    return {name: world(name) for name in WORLDS}


# -- The expectation before the runs ------------------------------------------


def one_plus_z(v_source: float, v_reader: float) -> float:
    """1 + z read by a reader of a lamp on a heading under the law as built
    (DERIVATIONS_BEAM 2.2 and 2.5; BEAM_LAW note 48): the lamp's rows stand
    c - v_s apart ahead of it, so a reader at rest meets them at the rate
    c / (c - v_s); a reader moving toward the rows meets them at 1 + v_r / c
    of that rate (the crossing rule); 1 + z is the emitter's rate over the
    reader's count. v_source > 0 toward the reader, v_reader > 0 toward the
    source (Links per interval)."""
    return (1 - v_source / C) / (1 + v_reader / C)


def natures_one_plus_z(closing_over_c: float) -> float:
    """Nature's one Doppler formula for an approach at the relative speed
    beta = closing_over_c: sqrt((1 - beta) / (1 + beta))."""
    return ((1 - closing_over_c) / (1 + closing_over_c)) ** 0.5


def relativistic_sum(a: float, b: float) -> float:
    return (a + b) / (1 + a * b)


def derivation(name: str) -> Json:
    """The continuum derivation of the approach: the two stars' speeds under
    the gravity of the line (each reads the other's F = MASS / 2^16 units per
    self-creation, arriving at the rate (1 + v_r / c) / (1 - v_s / c) of the
    emitter's rate, each row of amount a moving the reader's speed by (1 -
    |v|)^2 a / S toward the emitter, BEAM_LAW note 31), the first contact
    (the stars one Link apart), and per window the mutual 1 + z each star
    reads of the other, the lab detectors' 1 + z of the receding stars, and
    nature's value at the same closing speed."""
    v_a0, v_b0, mass_rule = WORLDS[name]
    x_a, x_b = float(STAR_A_X), float(STAR_B_X)
    v_a, v_b = v_a0 * C, v_b0 * C
    F = MASS * RELEASE[0] / RELEASE[1] if mass_rule == "read" else 0.0
    history: list[dict[str, float]] = []
    contact: int | None = None
    for t in range(1, TICKS + 1):
        history.append({"t": t - 1, "x_a": x_a, "x_b": x_b, "v_a": v_a, "v_b": v_b})
        if contact is None:
            gap = x_b - x_a
            # B's rows reach A moving -x at c; A moves +x at v_a: the rate.
            rate_a = F * (1 + v_a / C) / (1 - (-v_b) / C) if gap > 1 else 0.0
            rate_b = F * (1 + (-v_b) / C) / (1 - v_a / C) if gap > 1 else 0.0
            v_a += rate_a * (1 - abs(v_a)) ** 2 / WIDTH
            v_b -= rate_b * (1 - abs(v_b)) ** 2 / WIDTH
            x_a += v_a
            x_b += v_b
            if x_b - x_a <= 1.0:
                # The contact: the first refused step hands the stepping
                # body's x component to the occupant (BEAM_LAW note 31 (ix));
                # the lower number (A) steps first: A's component to B.
                contact = t
                p_a = momentum(abs(v_a), CONTENT) * (1 if v_a > 0 else -1)
                p_b = momentum(abs(v_b), CONTENT) * (1 if v_b > 0 else -1 if v_b < 0 else 0)
                p_b += p_a
                p_a = 0
                v_a = 0.0
                v_b = speed(abs(p_b), CONTENT) * (1 if p_b > 0 else -1 if p_b < 0 else 0)
                x_b = x_a + 1.0
        else:
            # After the contact the pair is at one Link: every further step
            # of one onto the other is a hand-over (the derivation stops
            # following the motion; the run reads it).
            pass

    def at(t: float) -> dict[str, float]:
        return history[min(int(t), len(history) - 1)]

    windows: dict[str, Json] = {}
    for lo, hi in WINDOWS:
        t0 = (lo + hi) / 2.0
        s = at(t0)
        va, vb = s["v_a"], s["v_b"]
        # A reads B: B's rows toward A (B's speed toward A is -vb), A toward
        # the rows at va.
        mutual_a = one_plus_z(-vb, va)
        mutual_b = one_plus_z(va, -vb)
        lab_left = one_plus_z(-va, 0.0)  # A recedes from the left lab
        lab_right = one_plus_z(vb, 0.0)  # B recedes from the right lab
        closing = relativistic_sum(abs(va) / C, abs(vb) / C)
        windows[f"{lo}-{hi}"] = {
            "t0": t0,
            "v_a_over_c": va / C,
            "v_b_over_c": vb / C,
            "gap": s["x_b"] - s["x_a"],
            "A_reads_B": mutual_a,
            "B_reads_A": mutual_b,
            "lab_left_reads_A": lab_left,
            "lab_right_reads_B": lab_right,
            "natures_mutual": natures_one_plus_z(closing),
            "natures_lab": (1 + abs(va) / C) / (1 - (va / C) ** 2) ** 0.5,
        }
    return {
        "rows_per_direction": F,
        "contact_tick": contact,
        "windows": windows,
        "speeds_at_contact": None
        if contact is None
        else {
            "v_a_over_c": history[contact - 1]["v_a"] / C,
            "v_b_over_c": history[contact - 1]["v_b"] / C,
        },
    }


def expectations() -> Json:
    return {
        "format": EXPECTATIONS_FORMAT,
        "c": C,
        "ticks": TICKS,
        "windows": [list(w) for w in WINDOWS],
        "grain_in_z": 0.003,
        "worlds": {name: derivation(name) for name in WORLDS},
    }


def main() -> None:
    print(f"c = {C:.5f} Links per interval on a heading; v = {SPEED_OVER_C} c = {SPEED_OVER_C * C:.5f}")
    for name, document in worlds().items():
        path = HERE / f"{name}.json"
        path.write_text(json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8")
        print(path.relative_to(ROOT))
    expected = expectations()
    (HERE / "expectations.json").write_text(
        json.dumps(carry_replicated(HERE / "expectations.json", expected), indent=1) + "\n",
        encoding="utf-8",
    )
    for name, entry in expected["worlds"].items():
        print(
            f"{name}: contact at tick {entry['contact_tick']}, speeds at contact {entry['speeds_at_contact']}"
        )
        for key, w in entry["windows"].items():
            print(
                f"  window {key}: v_a/c {w['v_a_over_c']:+.4f} v_b/c {w['v_b_over_c']:+.4f} gap {w['gap']:.1f}; "
                f"A reads B 1+z {w['A_reads_B']:.4f}, B reads A {w['B_reads_A']:.4f}, "
                f"labs {w['lab_left_reads_A']:.4f} / {w['lab_right_reads_B']:.4f}; "
                f"nature mutual {w['natures_mutual']:.4f}, lab {w['natures_lab']:.4f}"
            )


if __name__ == "__main__":
    main()
