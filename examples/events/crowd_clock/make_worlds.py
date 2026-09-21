"""Write the eight worlds of series U, a lamp inside a crowd (a "galaxy"),
still and moving, read by a detector at rest, and the expectations before
the runs (`expectations.json`).

The model owner, 2026-09-21 (in conversation with the G2 experimenter, after
the two-stars run, translated): "this could explain something about distant
galaxies and why they look as if at high speed" and then "check it yourself
and report to the Boss". The law reads 1 + z = (1 + k)(1 + v / c) at a
detector: the source's Doppler and the source's clock slowed by the crowd
it sits in (k the presence of other numbers' rows at its Node times the
suspension's width, BEAM_LAW step 4 and note 41: the owed count). A source
cannot reach z >= 1 by motion (v < c); a large z in this law is a slow
clock. This series measures how large k the crowd of a lamp can make, whether
the light escapes at the slowed rate, and how z splits between the clock and
the motion when the whole crowd moves.

The world: a bar of 121 x 9 x 9 Nodes (open). THE LAMP (`s_px1`, the G2
star's light family, 2^20 units so that its spending over the run is 0.05 %
of its wheel's rate, a lamp of one unit per self-creation toward the
detector, the birth wheel [1, 64]) sits at the centre of its crowd. THE
CROWD: two fixed bodies of the free family `mass` three Links from the lamp
on +y and +z, each releasing `release` x amount = F units per self-creation
on every direction of a fan of nine toward the lamp's line, (dx, -3, 0) and
(dx, 0, -3) for dx = -4 .. 4 in primitive form (a free family's release is
not consumed: every direction carries the whole F): the heading's rows
cross the lamp's Node and go on to the far face, the oblique ones cross
the lamp's line one to four Links along x on either side; the lamp's table
lets them pass (`pass`: the coupling off, the clock counts them). The fan
covers a lamp that drifts up to four Links along x from its crowd. THE
DETECTOR (`detector`, fixed, at the other end of the bar, off the crowd's
lines) measures the lamp's light with `reads: "age"`. The world's
`suspension` is [1, 2^16] (series G2's scalar clock): the lamp's clock owes
by_drive(acc, presence x 1, 2^16) intervals after each self-creation.

Eight worlds: five still (the lamp and its crowd at rest, F per source
chosen so that the pinned k runs from 0.005 to 2) and three moving (the lamp
and its two sources thrown together at 0.2 c along +x, away from the
detector, at k = 0.08, 0.3 and 1).

    python examples/events/crowd_clock/make_worlds.py     # the worlds and expectations.json
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from event_universe.core.game_board import PORT_HEADINGS  # noqa: E402
from event_universe.events.nature_beam import direction_flight  # noqa: E402
from event_universe.events.world import HEADING_OFFSET, LAW_VALUE, Q  # noqa: E402

LENGTH = 121
SHAPE = [LENGTH, 9, 9]
Y0, Z0 = 4, 4
N = 64
TICKS = 500
WIDTH = 1 << 20
# The lamp's reservoir, far beyond the run's births: a lamp's wheel turns by
# its content over K (the register's lamps spend, TEST_EXPECTATIONS "the
# lamp's turn ... falls as it spends"); the first run of 2026-09-21 with
# 2^13 units read the spending as a k of 0.03 to 0.04 by the second window
# (the design's section 7), so the reservoir is 2^20 and the spending 0.05 %.
LIGHT = 1 << 20
LAMP_RATE = [1, 1]
RELEASE = [1, 1 << 16]
SUSPENSION = [1, 1 << 16]
OFFSET = 3
SPEED_OVER_C = 0.2
# The lamp's Node and the detector's Node on the axis: the still lamp at
# x = 10 shining +x to the detector at x = 110; the moving lamp at x = 40
# shining -x to the detector at x = 3 (the galaxy recedes from it).
STILL_LAMP_X, STILL_DETECTOR_X = 10, 110
MOVING_LAMP_X, MOVING_DETECTOR_X = 40, 3
# What the presence counts per unit of a heading row's flux: the probe of
# 2026-09-21 (two heading sources of F = 64 gave the presence 256 = 4 F, so
# 2 per source unit: a row at c = 0.58 Links per interval is at the Node
# for two intervals on average, "outside and here", `moment_table`).
DWELL = 2
# The release F per source per interval (every direction of its fan carries
# F) and the pinned k = 2 x F x DWELL / d per world: F chosen for
# k = 4 F / 2^16 at 0.005, 0.08, 0.3, 1 and 2.
STILL: dict[str, int] = {
    "still_005": 82,
    "still_08": 1311,
    "still_3": 4915,
    "still_1": 16384,
    "still_2": 32768,
}
MOVING: dict[str, int] = {"moving_08": 1311, "moving_3": 4915, "moving_1": 16384}
# The reading windows: the still lamp's light flies 100 Links (172
# intervals) to its detector, the moving lamp's 37 Links and growing.
STILL_WINDOWS = ((200, 350), (350, 500))
MOVING_WINDOWS = ((100, 250), (250, 400))
# The lamp leaves its crowd's fan when its lag passes this many Links.
FAN_REACH = 4
# The lowest fraction of the pinned k the lamp keeps while inside the fan
# but behind its crowd's heading (the oblique directions' crossing Nodes).
K_LOW = 0.25
EXPECTATIONS_FORMAT = "crowd-clock-expectations-v1"
Json = dict[str, object]


def beam_speed() -> float:
    table = direction_flight(((0, 0, 0), (0, 0, 0), *PORT_HEADINGS))
    heading = np.array([HEADING_OFFSET])
    period = int(table.period[HEADING_OFFSET])
    return int(table.manhattan_steps(heading, np.array([period]))[0]) / period


C = beam_speed()


def momentum(v: float, content: int) -> int:
    return round(Q * WIDTH * content * v / (1 - v))


def speed(p: int, content: int) -> float:
    return p / (Q * WIDTH * content + p)


def fan(axis: int) -> list[list[int]]:
    """The nine directions from a source three Links up the axis toward the
    lamp's line: (dx, -3, 0) or (dx, 0, -3), dx = -4 .. 4, each in its
    primitive form (the world declares coprime components; (3, -3, 0) is
    (1, -1, 0), which crosses the lamp's line three Links along x too)."""
    out = []
    for dx in range(-4, 5):
        d = [dx, 0, 0]
        d[axis] = -OFFSET
        g = math.gcd(*d)
        out.append([component // g for component in d])
    return out


def declared_directions() -> list[list[int]]:
    """The world's table of directions beyond the six headings: the two fans
    without their headings (0, -1, 0) and (0, 0, -1), which the table holds
    already."""
    return [d for d in fan(1) + fan(2) if sum(abs(c) for c in d) != 1]


def world(name: str, flux: int, moving: bool) -> Json:
    amount = flux * RELEASE[1] // RELEASE[0]
    lamp_x = MOVING_LAMP_X if moving else STILL_LAMP_X
    detector_x = MOVING_DETECTOR_X if moving else STILL_DETECTOR_X
    light_direction = [-1, 0, 0] if moving else [1, 0, 0]
    v = SPEED_OVER_C * C if moving else 0.0
    lamp: Json = {
        "position": [lamp_x, Y0, Z0],
        "family": "s_px1",
        "amount": LIGHT,
        "phase": 0,
        "lamp": {"rate": LAMP_RATE, "wheel": [1, N], "directions": [light_direction]},
        "table": {"mass": {"rule": "pass"}},
    }
    if moving:
        lamp["momentum"] = [momentum(v, LIGHT), 0, 0]
    else:
        lamp["fixed"] = True
    sources: list[Json] = []
    for axis in (1, 2):
        position = [lamp_x, Y0, Z0]
        position[axis] += OFFSET
        source: Json = {
            "position": position,
            "family": "mass",
            "amount": amount,
            "directions": fan(axis),
            "table": {"s_px1": {"rule": "pass"}},
        }
        if moving:
            source["momentum"] = [momentum(v, amount), 0, 0]
        else:
            source["fixed"] = True
        sources.append(source)
    detector: Json = {
        "position": [detector_x, Y0, Z0],
        "family": "detector",
        "amount": 1,
        "fixed": True,
        "table": {"s_px1": {"rule": "measure", "reads": "age"}},
    }
    return {
        "law": LAW_VALUE,
        "model_id": f"rays-crowd-clock-{name.replace('_', '-')}-v1",
        "shape": list(SHAPE),
        "boundary": "open",
        "directions": declared_directions(),
        "ticks": TICKS,
        "K": LIGHT,
        "N": N,
        "release": RELEASE,
        "suspension": SUSPENSION,
        "width": WIDTH,
        "families": [
            {"name": "detector", "quantum": 1},
            {"name": "mass", "quantum": 0, "charge": 0, "phase": False},
            {"name": "s_px1", "quantum": 1},
        ],
        "measured": [detector, lamp, *sources],
    }


def worlds() -> dict[str, Json]:
    found = {name: world(name, r, False) for name, r in STILL.items()}
    found.update({name: world(name, r, True) for name, r in MOVING.items()})
    return found


def pinned_k(flux: int) -> float:
    """k = the presence times the width: two sources, F units per interval on
    the one direction of each that passes the lamp's Node, each unit present
    DWELL intervals at the Node, over d = 2^16."""
    return 2 * flux * DWELL / SUSPENSION[1]


def lag(k: float, ticks: float) -> float:
    """The lamp steps only at its self-creations: its speed on the GameBoard
    is v / (1 + k) while its crowd's is v, so it lags k v t / (1 + k) Links
    after t intervals."""
    return k * SPEED_OVER_C * C * ticks / (1 + k)


def exit_tick(k: float) -> float:
    """The interval at which the lag passes the fan's reach: the lamp is out
    of its crowd, k falls to 0 and its clock and speed recover."""
    return FAN_REACH * (1 + k) / (k * SPEED_OVER_C * C)


def expectations() -> Json:
    out: Json = {
        "format": EXPECTATIONS_FORMAT,
        "c": C,
        "ticks": TICKS,
        "dwell": DWELL,
        "fan_reach": FAN_REACH,
        "speed_over_c_moving": SPEED_OVER_C,
        "still_windows": [list(w) for w in STILL_WINDOWS],
        "moving_windows": [list(w) for w in MOVING_WINDOWS],
        "worlds": {},
    }
    for name, flux in STILL.items():
        k = pinned_k(flux)
        out["worlds"][name] = {
            "flux": flux,
            "k": k,
            "k_bracket": [0.8 * k, 1.2 * k],
            "clock_rate": 1 / (1 + k),
            "one_plus_z": 1 + k,
            "clicks_per_interval": 1 / (1 + k),
            "moving": False,
        }
    flight = (MOVING_LAMP_X - MOVING_DETECTOR_X) / C
    doppler = 1 + SPEED_OVER_C
    for name, flux in MOVING.items():
        k = pinned_k(flux)
        # The lamp behind its crowd sits on the oblique directions' crossing
        # Nodes, which carry fewer rows than the heading (the probe of
        # 2026-09-21: two Links behind, half the presence): k falls with the
        # lag, between K_LOW k and k, and the exit comes between the two.
        exits = [exit_tick(k), exit_tick(K_LOW * k)]
        windows: Json = {}
        for lo, hi in MOVING_WINDOWS:
            # The detector sees the lamp's clock as it was one flight earlier;
            # a window entirely before the exit reads the slowed clock, one
            # entirely after it the Doppler alone (the lamp out of its crowd
            # steps every interval again), a window across the exit between.
            seen_lo, seen_hi = lo - flight, hi - flight
            if seen_hi <= exits[0]:
                bracket = [(1 + K_LOW * k) * doppler, (1 + k) * doppler]
            elif seen_lo >= exits[1]:
                bracket = [doppler, doppler]
            else:
                bracket = [doppler, (1 + k) * doppler]
            windows[f"{lo}-{hi}"] = {"one_plus_z_bracket": bracket}
        out["worlds"][name] = {
            "flux": flux,
            "k": k,
            "k_bracket": [K_LOW * k, k],
            "clock_rate": 1 / (1 + k),
            "exit_tick_bracket": exits,
            "one_plus_z_in_the_crowd": (1 + k) * doppler,
            "one_plus_z_doppler_only": doppler,
            "flight": flight,
            "windows": windows,
            "moving": True,
        }
    return out


def main() -> None:
    for name, document in worlds().items():
        path = HERE / f"{name}.json"
        path.write_text(json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8")
        print(path.relative_to(ROOT))
    expected = expectations()
    (HERE / "expectations.json").write_text(json.dumps(expected, indent=1) + "\n", encoding="utf-8")
    for name, e in expected["worlds"].items():
        if e["moving"]:
            seen = ", ".join(
                f"{w}: {v['one_plus_z_bracket'][0]:.3f} .. {v['one_plus_z_bracket'][1]:.3f}"
                for w, v in e["windows"].items()
            )
            exits = e["exit_tick_bracket"]
            print(
                f"{name}: F = {e['flux']}, pinned k = {e['k']:.4f}, 1 + z in the crowd "
                f"{e['one_plus_z_in_the_crowd']:.4f}, exit between ticks {exits[0]:.0f} and "
                f"{exits[1]:.0f}, windows {seen}"
            )
        else:
            print(
                f"{name}: F = {e['flux']}, pinned k = {e['k']:.4f}, clock rate {e['clock_rate']:.4f}, 1 + z = {e['one_plus_z']:.4f}"
            )


if __name__ == "__main__":
    main()
