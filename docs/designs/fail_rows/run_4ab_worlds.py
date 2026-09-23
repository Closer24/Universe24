"""The worlds and the pins of RUN_4AB.md (rows 4a and 4b of the paper's
Table 2 turned by the algebra; the FAIL Runner A, 2026-09-23).

Writes `worlds/*.json` (every world under existing keys: `clock_stamp`,
`covariant_readings`; no engine line, no default changed) and the pins
`run_4ab_pins.json` with its print `run_4ab_pins.out`, every number a
COMPUTATION from the closed forms of the click frame
(docs/designs/click_frame/DERIVATION.md sections 2 and 3), of the identity
(DERIVATIONS_BEAM 17.6 M1 to M3) and of the engine's own flight table
(`direction_flight`, the least age at which a heading row has made a given
number of steps), before any run. Nothing here runs a world.

Usage: `PYTHONPATH=src python docs/designs/fail_rows/run_4ab_worlds.py`.
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

from event_universe.core.integer import integer_root  # noqa: E402
from event_universe.events.nature_beam import direction_flight  # noqa: E402
from event_universe.events.world import HEADING_OFFSET, Q  # noqa: E402
from event_universe.world_loading import load_world  # noqa: E402

WORLDS = HERE / "worlds"
C2 = (1, 3)
COVARIANT_KEY = {"c2": list(C2), "grain": 1}

# --- 4a: the J4 bar of series S with a detector body at its far end --------
BAR = 201
DETECTOR_NODE = 200
BORN = 10
CONTENT = 207
AT = 64
J4_TICKS = 420
J4_WIDTH = 1
MUONS = {"rest": 0, "3640": 3640, "12856": 12856}
# The catalog's rows, verbatim (examples/events/entities/families.json:
# muon, electron, electron_born_by_become, neutrino, detector_material).
J4_FAMILIES = [
    {"name": "mu", "quantum": 0, "charge": [-7344, CONTENT], "phase": True},
    {"name": "e", "quantum": 0, "charge": -15, "phase": True},
    {"name": "beta", "quantum": 1, "charge": -7344},
    {"name": "nu", "quantum": 0},
    {"name": "detector", "quantum": 1},
]

# --- the k-ladder: the cart worlds of the moving detector, k = 3 and 5 ------
CART_TICKS = 600
CART_BAR = 240
CART_WIDTH = 1 << 20
CART_K = 4202496
CART_HELD = 4194304
CART_AMOUNT = 8192
CART_GRAIN = 1 << 18
LADDER = (3, 5)
ONE_WAY_FROM = 60
ROUND_TRIP_FROM = 100

# --- 4b: series S's coasting world as registered, the stamp added ----------
COASTING_SOURCE = ROOT / "examples" / "events" / "covariant" / "coasting_none_covariant.json"
CATALOG = ROOT / "examples" / "events" / "entities" / "families.json"
STAR = "s_mz2"
Z_PIN = (0.366, 0.372)
Z_DESIGN = 0.369

Json = dict[str, object]


def muon_world(name: str, momentum: int, key: bool) -> Json:
    """Series S's J4 world (`examples/events/covariant/make_worlds.py`,
    `muon_world`) with two declarations added: a fixed detector body at the
    bar's last Node measuring the products (its click line carries `clock`,
    its own count, under `clock_stamp`), and the key present (the
    hypothesis) or absent (the law)."""
    document: Json = {
        "law": "beam",
        "model_id": f"beam-fail-rows-j4-muon-{name}-{'key' if key else 'law'}-v1",
        "shape": [BAR, 1, 1],
        "boundary": "open",
        "ticks": J4_TICKS,
        "K": 1 << 20,
        "N": 64,
        "release": [1, 1 << 20],
        "suspension": 0,
        "width": J4_WIDTH,
        "clock_stamp": True,
        "families": J4_FAMILIES,
        "measured": [
            {
                "position": [BORN, 0, 0],
                "family": "mu",
                "amount": CONTENT,
                "momentum": [momentum, 0, 0],
                "directions": [[1, 0, 0]],
                "become": {"at": AT, "into": "e", "products": [["beta", 1, CONTENT], ["nu", 1, 0]]},
            },
            {
                "position": [DETECTOR_NODE, 0, 0],
                "family": "detector",
                "amount": 1,
                "fixed": True,
                "table": {
                    "beta": {"rule": "measure", "reads": "age"},
                    "nu": {"rule": "measure", "reads": "age"},
                    "mu": {"rule": "pass"},
                    "e": {"rule": "pass"},
                },
            },
        ],
    }
    if key:
        document["covariant_readings"] = dict(COVARIANT_KEY)
    return document


def cart_world(k: int, key: bool) -> Json:
    """The cart world of the moving detector (`examples/events/moving_detector/
    make_worlds.py`, `cart_k<k>`): the post R at x = 1 (`rerelease`), the lamp
    A at x = 3 (one row per count on +x), the cart D from x = 20 at the
    momentum Q S M / (k - 1) with its own lamp on -x; `clock_stamp` as
    registered; the key present (the hypothesis) or absent (the law). The
    radar velocity is not read here (issue #937 stays as recorded)."""
    momentum = Q * CART_WIDTH * CART_K // (k - 1)
    document: Json = {
        "law": "beam",
        "model_id": f"beam-fail-rows-cart-k{k}-{'key' if key else 'law'}-v1",
        "shape": [CART_BAR, 3, 3],
        "boundary": "open",
        "ticks": CART_TICKS,
        "K": CART_K,
        "N": 64,
        "release": [1, 65536],
        "suspension": 0,
        "width": CART_WIDTH,
        "clock_stamp": True,
        "families": [
            {"name": "post", "quantum": 1},
            {"name": "source", "quantum": 1},
            {"name": "cart", "quantum": 1},
            {"name": "mass", "quantum": 0, "charge": 0, "phase": False},
        ],
        "measured": [
            {
                "position": [1, 1, 1],
                "family": "post",
                "amount": 1,
                "fixed": True,
                "directions": [[1, 0, 0]],
                "table": {
                    "cart": {"rule": "rerelease"},
                    "source": {"rule": "pass"},
                    "mass": {"rule": "pass"},
                },
            },
            {
                "position": [3, 1, 1],
                "family": "source",
                "amount": CART_AMOUNT,
                "phase": 0,
                "fixed": True,
                "held": {"mass": CART_HELD},
                "directions": [[1, 0, 0]],
                "lamp": {"rate": [1, 1], "wheel": [1, 64], "directions": [[1, 0, 0]]},
                "table": {"cart": {"rule": "pass"}, "mass": {"rule": "pass"}},
            },
            {
                "position": [20, 1, 1],
                "family": "cart",
                "amount": CART_AMOUNT,
                "phase": 0,
                "momentum": [momentum, 0, 0],
                "held": {"mass": CART_HELD},
                "directions": [[-1, 0, 0]],
                "lamp": {"rate": [1, 1], "wheel": [1, 64], "directions": [[-1, 0, 0]]},
                "table": {
                    "source": {"rule": "measure", "reads": "age"},
                    "cart": {"rule": "measure", "reads": "age"},
                    "mass": {"rule": "pass"},
                },
            },
        ],
    }
    if key:
        document["covariant_readings"] = {"c2": list(C2), "grain": CART_GRAIN}
    return document


def coasting_world() -> Json:
    """Series S's `coasting_none_covariant` as registered but for one key,
    `clock_stamp` true (no rule, no verb: the centre's click lines carry its
    own count), its families written in from the catalog."""
    document = json.loads(COASTING_SOURCE.read_text(encoding="utf-8"))
    document["clock_stamp"] = True
    # The catalog's rows written into the file (the loader confines a
    # reference to the world's parent folder): the families of the three
    # entities the registered world names, in their order, from the one
    # catalog, so the world is a portable input and no row is copied by hand.
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    by_name = {entity["name"]: entity for entity in catalog["entities"]}
    families: list[object] = []
    for entity in document.pop("entities"):
        named = by_name[str(entity["definition"])]
        if named["measured"] or named["detectors"]:
            raise ValueError(
                f"{named['name']}: the entity places events; only families are inlined here"
            )
        families.extend(named["families"])
    document.pop("entity_definitions")
    document["families"] = families
    return document


def worlds() -> dict[str, Json]:
    found: dict[str, Json] = {}
    for name, momentum in MUONS.items():
        found[f"j4_muon_{name}_key"] = muon_world(name, momentum, True)
        found[f"j4_muon_{name}_law"] = muon_world(name, momentum, False)
    for k in LADDER:
        found[f"cart_k{k}_key"] = cart_world(k, True)
        found[f"cart_k{k}_law"] = cart_world(k, False)
    found["coasting_none_covariant_stamp"] = coasting_world()
    return found


# --- the closed forms ---------------------------------------------------------


def flight_table(document: Json):
    source = json.dumps(document).encode("utf-8")
    world = load_world(source, base_dir=WORLDS, root=ROOT).world
    return direction_flight(world.directions)


def heading_age(flight, steps: int) -> int:
    """The least age at which a row on the +x heading has made `steps`
    Manhattan steps (the engine's flight table; series S's `heading_click`)."""
    heading = np.array([HEADING_OFFSET])
    age = 0
    while int(flight.manhattan_steps(heading, np.array([age]))[0]) < steps:
        age += 1
    return age


def heading_pace(flight) -> Fraction:
    heading = np.array([HEADING_OFFSET])
    period = int(flight.period[HEADING_OFFSET])
    return Fraction(int(flight.manhattan_steps(heading, np.array([period]))[0]), period)


def energy_prime(rest: int, momentum: int, grain: int = 1) -> int:
    rest_g, momentum_g = rest // grain, abs(momentum) // grain
    return integer_root(rest_g * rest_g + C2[1] * momentum_g * momentum_g)


def muon_pins(flight) -> dict[str, Json]:
    """4a: the detector body's own count at the beta product's click, under
    the key (the identity's integers: the decay at 64 + floor(63 (E' - m) / m)
    at the Node 10 + floor(64 p / m)) and under the law (the decay at 64 at
    the Node 10 + floor(64 p / (m + p)), the per-axis drive of main); the
    click at the decay's tick plus the least age at which the heading row has
    made 200 - x steps; the tolerance two ticks (series S's on the click)."""
    rest = Q * J4_WIDTH * CONTENT
    pins: dict[str, Json] = {}
    for name, p in MUONS.items():
        for key in (True, False):
            if key:
                e_prime = energy_prime(rest, p)
                gamma = e_prime / rest
                decay_tick = AT + (AT - 1) * (e_prime - rest) // rest
                node = BORN + AT * p // rest
                pace = p / e_prime if p else 0.0
            else:
                e_prime, gamma = rest, 1.0
                decay_tick = AT
                node = BORN + AT * p // (rest + p) if p else BORN
                pace = p / (rest + p) if p else 0.0
            steps = DETECTOR_NODE - node
            age = heading_age(flight, steps)
            pins[f"j4_muon_{name}_{'key' if key else 'law'}"] = {
                "momentum": p,
                "rest_energy": rest,
                "energy_at_load": e_prime,
                "gamma_of_the_identity": gamma,
                "pace_links_per_interval": pace,
                "beta_on_the_heading": pace / float(heading_pace(flight)),
                "decay": {
                    "kind": "GAMEBOARD",
                    "line": "become (the muon's own record; not the pin)",
                    "tick": decay_tick,
                    "node": [node, 0, 0],
                },
                "click": {
                    "kind": "DETECTOR",
                    "line": "click at the detector body (x = 200) of the product beta, its `clock`",
                    "steps_to_the_detector": steps,
                    "flight_age": age,
                    "count": decay_tick + age,
                    "tolerance": 2,
                },
                "ratio": {
                    "kind": "CONVERSION",
                    "line": "(the click's count less the flight's age) over 64, gamma's form as the thing compared with",
                    "value": decay_tick / AT,
                    "gamma": gamma,
                },
            }
    return pins


def cart_pins(flight) -> dict[str, Json]:
    """The k-ladder: k_AB = r / (1 - beta) (the cart's counts apart over the
    lamp's ordinals apart), k_BA = (1 + beta) / r (the post's counts apart
    over the cart's ordinals apart), their ratio (1 - beta^2) / r^2 and the
    r-free round trip (1 + beta) / (1 - beta) (the click frame section 2 (a),
    (b); section 3's table). The law: r = 1, the pace 1 / k. The key: r =
    m / E' = 1 / gamma, the pace p / E' = 1 / sqrt((k - 1)^2 + 3); beta the
    pace over the heading's c = 32 / 55 (the flight table), and beside it the
    identity's own c^2 = 1 / 3, on which the ratio is 1 exactly."""
    c = heading_pace(flight)
    rest = Q * CART_WIDTH * CART_K
    pins: dict[str, Json] = {}
    for k in LADDER:
        p = rest // (k - 1)
        for key in (True, False):
            if key:
                e_prime = energy_prime(rest, p, CART_GRAIN)
                gamma = e_prime / (rest // CART_GRAIN)
                r = 1 / gamma
                pace = (p // CART_GRAIN) / e_prime
                beta = pace / float(c)
                beta_identity = math.sqrt(3) * pace
                k_ab = r / (1 - beta)
                k_ba = (1 + beta) / r
                ratio = k_ba / k_ab
                ratio_identity = (1 - beta_identity**2) / r**2
                exact = None
            else:
                gamma, r = 1.0, 1.0
                pace = 1 / k
                beta_f = Fraction(1, k) / c
                beta = float(beta_f)
                beta_identity = math.sqrt(3) / k
                k_ab_f, k_ba_f = 1 / (1 - beta_f), 1 + beta_f
                k_ab, k_ba = float(k_ab_f), float(k_ba_f)
                ratio, ratio_identity = float(k_ba_f / k_ab_f), 1 - beta_identity**2
                exact = {
                    "k_AB": str(k_ab_f),
                    "k_BA": str(k_ba_f),
                    "ratio": str(k_ba_f / k_ab_f),
                    "round_trip": str(k_ba_f * k_ab_f),
                }
            pins[f"cart_k{k}_{'key' if key else 'law'}"] = {
                "k": k,
                "momentum": p,
                "rest_energy": rest,
                "rate_r": r,
                "gamma_of_the_identity": gamma,
                "pace_links_per_interval": pace,
                "beta_on_the_heading": beta,
                "beta_on_the_identity_c": beta_identity,
                "windows": {
                    "one_way_from_count": ONE_WAY_FROM,
                    "round_trip_from_count": ROUND_TRIP_FROM,
                },
                "band": "2 / W over a window of W counts apart (PREREGISTRATION_V2 section 5, g = 1)",
                "k_AB": {
                    "kind": "DETECTOR",
                    "value": k_ab,
                    "reads": "the cart's counts apart over the lamp's ordinals apart",
                },
                "k_BA": {
                    "kind": "DETECTOR",
                    "value": k_ba,
                    "reads": "the post's counts apart over the cart's ordinals apart",
                },
                "ratio_k_BA_over_k_AB": {
                    "kind": "DETECTOR",
                    "value": ratio,
                    "on_the_identity_c": ratio_identity,
                    "comparison": 1.0,
                    "reads": "(1 - beta^2) / r^2; 1 - beta^2 on the law, 1 under the one rate r^2 = 1 - beta^2",
                },
                "round_trip": {
                    "kind": "DETECTOR",
                    "value": k_ab * k_ba,
                    "reads": "(1 + beta) / (1 - beta), r-free",
                },
                "exact_fractions": exact,
                "radar_velocity": "NOT READ (issue #937; batch 933 stays as recorded)",
            }
    return pins


def coasting_pins() -> Json:
    grain = 1 << 18
    rest = 281749854617600
    p = 51901289008505
    e_prime = energy_prime(rest, p, grain)
    gamma = e_prime / (rest // grain)
    pace = (p // grain) / e_prime
    beta_c = math.sqrt(3) * pace
    beta_h = pace / (32 / 55)
    return {
        "star": STAR,
        "energy_at_load_at_the_grain": e_prime,
        "rest_energy_at_the_grain": rest // grain,
        "gamma_of_the_identity": gamma,
        "pace_links_per_interval": pace,
        "beta_on_the_identity_c": beta_c,
        "beta_on_the_heading": beta_h,
        "z": {
            "kind": "DETECTOR",
            "line": "the centre's pointer over the late window [300, 400), read in the centre's own count",
            "pin": list(Z_PIN),
            "design": Z_DESIGN,
            "centre_continuum": gamma * (1 + beta_c) - 1,
            "centre_heading": gamma * (1 + beta_h) - 1,
            "registered_under_the_key": 0.3674,
            "registered_without_the_key": 0.2636,
            "at_head_without_the_key": 0.2647,
            "nature": 0.315,
        },
        "k_BA": {
            "kind": "COMPUTATION",
            "value": gamma * (1 + beta_h),
            "reads": "1 + z = (1 + beta) / r, the click frame 2 (a)",
        },
        "stamp": {
            "kind": "DETECTOR",
            "line": "`clock` on every click line of the centre's measured event equals the line's tick (r_A = 1: no crowd, suspension 0)",
            "expected": "equal on every stamped line",
        },
    }


def main() -> None:
    WORLDS.mkdir(exist_ok=True)
    found = worlds()
    for name, document in found.items():
        (WORLDS / f"{name}.json").write_text(
            json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8"
        )
    flight = flight_table(found["j4_muon_rest_key"])
    pins: Json = {
        "format": "fail-rows-run-4ab-pins-v1",
        "base": "origin/main e404baa (the per-axis drive the law's drive; PR #907 not merged)",
        "c_on_the_heading": str(heading_pace(flight)),
        "j4": muon_pins(flight),
        "ladder": cart_pins(flight),
        "coasting": coasting_pins(),
    }
    (HERE / "run_4ab_pins.json").write_text(json.dumps(pins, indent=1) + "\n", encoding="utf-8")
    out: list[str] = []
    out.append(
        f"c on a heading (the flight table): {heading_pace(flight)} = {float(heading_pace(flight)):.6f} Links per interval"
    )
    out.append("")
    out.append(
        "4a, the J4 bar with a detector body at x = 200 (COMPUTATION; the click DETECTOR when read):"
    )
    for name, pin in pins["j4"].items():
        out.append(
            f"  {name}: p = {pin['momentum']}, E' = {pin['energy_at_load']}, gamma = {pin['gamma_of_the_identity']:.4f}, "
            f"pace = {pin['pace_links_per_interval']:.4f} (beta {pin['beta_on_the_heading']:.4f}); "
            f"the decay at tick {pin['decay']['tick']} at x = {pin['decay']['node'][0]} (GAMEBOARD); "
            f"{pin['click']['steps_to_the_detector']} steps, the flight's age {pin['click']['flight_age']}; "
            f"the click's count {pin['click']['count']} +- 2 (DETECTOR); the ratio {pin['ratio']['value']:.4f} against gamma {pin['ratio']['gamma']:.4f}"
        )
    out.append("")
    out.append(
        "the k-ladder, the cart worlds (COMPUTATION; each reading DETECTOR when read; the band 2 / W):"
    )
    for name, pin in pins["ladder"].items():
        exact = pin["exact_fractions"]
        out.append(
            f"  {name}: p = {pin['momentum']}, r = {pin['rate_r']:.5f} (gamma {pin['gamma_of_the_identity']:.5f}), "
            f"pace {pin['pace_links_per_interval']:.5f}, beta {pin['beta_on_the_heading']:.5f} on the heading "
            f"({pin['beta_on_the_identity_c']:.5f} on c^2 = 1/3); k_AB {pin['k_AB']['value']:.5f}, k_BA {pin['k_BA']['value']:.5f}, "
            f"the ratio {pin['ratio_k_BA_over_k_AB']['value']:.5f} (on c^2 = 1/3: {pin['ratio_k_BA_over_k_AB']['on_the_identity_c']:.5f}; "
            f"the comparison 1), the round trip {pin['round_trip']['value']:.5f}"
            + (f"; exact {exact}" if exact else "")
        )
    out.append("")
    cz = pins["coasting"]
    out.append(
        f"4b, series S's world with the stamp (COMPUTATION): E'/g {cz['energy_at_load_at_the_grain']} over {cz['rest_energy_at_the_grain']}, "
        f"gamma {cz['gamma_of_the_identity']:.5f}, pace {cz['pace_links_per_interval']:.4f}, beta {cz['beta_on_the_heading']:.4f} on the heading "
        f"({cz['beta_on_the_identity_c']:.4f} on c^2 = 1/3); z pinned {cz['z']['pin']} about {cz['z']['design']} (DETECTOR when read), "
        f"the centres {cz['z']['centre_continuum']:.4f} (c^2 = 1/3) and {cz['z']['centre_heading']:.4f} (the heading); "
        f"k_BA = 1 + z = {cz['k_BA']['value']:.4f}; the stamp: clock = tick on every click line of the centre"
    )
    (HERE / "run_4ab_pins.out").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    main()
