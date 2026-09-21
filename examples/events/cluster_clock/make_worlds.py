"""Write the two worlds of series Q, a cluster of crowds read by one
detector, at rest and moving as one, and the expectations before the runs
(`expectations.json`).

The model owner, 2026-09-21 (in conversation, translated), after series P
(a lamp inside a crowd, docs/designs/crowd_clock/DESIGN.md): "so is it
possible that this is the matter with galaxy clusters that look as if at a
constant speed when they should have flown apart?", and then "start the
additional test you proposed". The test: five members of a "cluster", each
a lamp inside its own crowd of a different density (k = 0, 0.1, 0.3, 0.6,
1 by the pinned k = 4 F / 2^16 of series P), all at rest before one fixed
detector. The detector reads a spread of 1 + z = 1 + k_i with nothing
moving: what a reader would call a velocity dispersion. Then the same five
members thrown together at 0.2 c away from the detector, each crowd's
sources thrown at v / (1 + k_i) so that they keep pace with their lamp,
which waits (series P's finding: a slowed lamp moves at v / (1 + k)): the
emulation of a crowd slowed alike. The law then reads 1 + z_i =
(1 + k_i)(1 + v / ((1 + k_i) c)) = 1 + k_i + v / c, the two terms adding,
against the product (1 + k_i)(1 + v / c) of a lamp behind an unslowed
crowd.

The world: a bar of 201 x 9 x 9 Nodes (open), the detector at x = 3
(`detector`, fixed, `reads: "age"` of `s_px1`), five lamps of `s_px1` at
x = 40, 60, 80, 100, 120 shining -x to it (2^20 units, one unit per
self-creation, the wheel [1, 64]), each with two `mass` sources three
Links up +y and +z sending series P's fan of nine directions across its
line at F_i units per interval (the member of k = 0 has none). Every lamp
lets the crowd's rows and the other lamps' light pass; the sources let the
light pass. `suspension` [1, 2^16], `release` [1, 2^16], `width` 2^20,
N = 64, 500 intervals.

    python examples/events/cluster_clock/make_worlds.py     # the worlds and expectations.json
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
from event_universe.register_map import carry_replicated  # noqa: E402


def _crowd_clock():
    """Series P's generator, the one copy of the fan, the speeds and the
    pinned k."""
    path = HERE.parent / "crowd_clock" / "make_worlds.py"
    spec = importlib.util.spec_from_file_location("crowd_clock_make_worlds", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("crowd_clock_make_worlds", module)
    spec.loader.exec_module(module)
    return module


P = _crowd_clock()
C = P.C
LENGTH = 201
SHAPE = [LENGTH, 9, 9]
Y0, Z0 = P.Y0, P.Z0
TICKS = 500
DETECTOR_X = 3
LIGHT_DIRECTION = [-1, 0, 0]
SPEED_OVER_C = 0.2
# The members: the lamp's x and the pinned k of its crowd (F = k 2^16 / 4).
MEMBERS: dict[str, tuple[int, float]] = {
    "m0": (40, 0.0),
    "m01": (60, 0.1),
    "m03": (80, 0.3),
    "m06": (100, 0.6),
    "m1": (120, 1.0),
}
WINDOW = (250, 500)
LAG_BOUND = 2
EXPECTATIONS_FORMAT = "cluster-clock-expectations-v1"
Json = dict[str, object]


def flux(k: float) -> int:
    return round(k * P.SUSPENSION[1] / (2 * P.DWELL))


def member(x: int, k: float, moving: bool) -> tuple[Json, list[Json]]:
    v = SPEED_OVER_C * C if moving else 0.0
    lamp: Json = {
        "position": [x, Y0, Z0],
        "family": "s_px1",
        "amount": P.LIGHT,
        "phase": 0,
        "lamp": {"rate": P.LAMP_RATE, "wheel": [1, P.N], "directions": [LIGHT_DIRECTION]},
        "table": {"mass": {"rule": "pass"}, "s_px1": {"rule": "pass"}},
    }
    if moving:
        lamp["momentum"] = [P.momentum(v, P.LIGHT), 0, 0]
    else:
        lamp["fixed"] = True
    sources: list[Json] = []
    f = flux(k)
    if f:
        amount = f * P.RELEASE[1] // P.RELEASE[0]
        for axis in (1, 2):
            position = [x, Y0, Z0]
            position[axis] += P.OFFSET
            source: Json = {
                "position": position,
                "family": "mass",
                "amount": amount,
                "directions": P.fan(axis),
                "table": {"s_px1": {"rule": "pass"}},
            }
            if moving:
                # The crowd slowed alike, emulated: the sources at the
                # lamp's speed on the GameBoard, v / (1 + k).
                source["momentum"] = [P.momentum(v / (1 + k), amount), 0, 0]
            else:
                source["fixed"] = True
            sources.append(source)
    return lamp, sources


def world(name: str, moving: bool) -> Json:
    detector: Json = {
        "position": [DETECTOR_X, Y0, Z0],
        "family": "detector",
        "amount": 1,
        "fixed": True,
        "table": {"s_px1": {"rule": "measure", "reads": "age"}},
    }
    measured: list[Json] = [detector]
    for x, k in MEMBERS.values():
        lamp, sources = member(x, k, moving)
        measured.append(lamp)
        measured.extend(sources)
    return {
        "law": P.LAW_VALUE,
        "model_id": f"rays-cluster-clock-{name.replace('_', '-')}-v1",
        "shape": list(SHAPE),
        "boundary": "open",
        "directions": P.declared_directions(),
        "ticks": TICKS,
        "K": P.LIGHT,
        "N": P.N,
        "release": P.RELEASE,
        "suspension": P.SUSPENSION,
        "width": P.WIDTH,
        "families": [
            {"name": "detector", "quantum": 1},
            {"name": "mass", "quantum": 0, "charge": 0, "phase": False},
            {"name": "s_px1", "quantum": 1},
        ],
        "measured": measured,
    }


def worlds() -> dict[str, Json]:
    return {
        "cluster_rest": world("cluster_rest", False),
        "cluster_moving": world("cluster_moving", True),
    }


def numbers() -> dict[str, Json]:
    """The measured events' numbers per member (the detector is 1)."""
    out: dict[str, Json] = {}
    number = 2
    for name, (x, k) in MEMBERS.items():
        sources = [number + 1, number + 2] if flux(k) else []
        out[name] = {"lamp": number, "sources": sources, "x": x, "k": k, "flux": flux(k)}
        number += 1 + len(sources)
    return out


def expectations() -> Json:
    v = SPEED_OVER_C
    ks = [k for _, k in MEMBERS.values()]
    mean = sum(ks) / len(ks)
    rest = {name: {"one_plus_z": 1 + k} for name, (_, k) in MEMBERS.items()}
    moving = {
        name: {
            "one_plus_z_additive": 1 + k + v,
            "one_plus_z_product": (1 + k) * (1 + v),
            "speed_over_c_on_the_board": v / (1 + k),
        }
        for name, (_, k) in MEMBERS.items()
    }
    return {
        "format": EXPECTATIONS_FORMAT,
        "c": C,
        "ticks": TICKS,
        "window": list(WINDOW),
        "speed_over_c_moving": SPEED_OVER_C,
        "lag_bound_links": LAG_BOUND,
        "tolerance": 0.02,
        "members": numbers(),
        "cluster_rest": {
            "members": rest,
            # what a reader of the five z would call the cluster's velocity
            # dispersion, with nothing moving: the standard deviation of k
            "z_mean": mean,
            "z_dispersion": (sum((k - mean) ** 2 for k in ks) / len(ks)) ** 0.5,
            "z_minimum": min(ks),
        },
        "cluster_moving": {
            "members": moving,
            "z_shift_of_every_member": v,
        },
    }


def main() -> None:
    for name, document in worlds().items():
        path = HERE / f"{name}.json"
        path.write_text(json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8")
        print(path.relative_to(ROOT))
    expected = expectations()
    (HERE / "expectations.json").write_text(
        json.dumps(carry_replicated(HERE / "expectations.json", expected), indent=1) + "\n",
        encoding="utf-8",
    )
    for name, m in expected["members"].items():
        r = expected["cluster_rest"]["members"][name]["one_plus_z"]
        mv = expected["cluster_moving"]["members"][name]
        print(
            f"{name}: lamp {m['lamp']} at x = {m['x']}, F = {m['flux']}, k = {m['k']}: at rest 1 + z = {r:.3f}; "
            f"moving as one 1 + z = {mv['one_plus_z_additive']:.3f} (the product would read {mv['one_plus_z_product']:.3f})"
        )
    c = expected["cluster_rest"]
    print(
        f"the cluster at rest: mean z {c['z_mean']:.3f}, dispersion {c['z_dispersion']:.3f}, minimum {c['z_minimum']:.3f}"
    )


if __name__ == "__main__":
    main()
