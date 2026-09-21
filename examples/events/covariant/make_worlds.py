"""Write the worlds of series S, the covariant readings (`covariant-readings-v1`;
DERIVATIONS_BEAM section 17 as amended in 17.6, the pins of 18.1 (a) and
(c) as restated there; the model owner's decision of 2026-09-21, record
270 of the log of 2026-09-20: built beside the law in place of lorentz-v1),
and the expectations before the runs (`expectations.json`).

The hypothesis is a world key, `covariant_readings`, absent by default: under
it every body carries its energy readings (the exact square W = E'_0^2 + 3
p . p at c^2 = [1, 3], E'_0 = Q S M, and E' the largest integer with E'^2
<= W, kept by comparisons), its self-creations are gated by a second owed
count (one per E' / E'_0 = gamma intervals in the mean, 17.6 M1), the drive's
wall loses its cap term (the pace p / E' per lattice interval) and the free
release runs per lattice interval (17.6 N4). Nothing of the law's six verbs
changes; with the key absent every registered world reads as it did, byte
for byte.

The J4 worlds (17.6 M9 and N6; NATURE row 4a). An open bar of [201, 1, 1]
(the +x face at x = 200), `"law": "beam"`, K 2^20, N 64, `release` [1, 2^20]
(no row within the run), `suspension` 0, `width` 1, the key with `c2` [1, 3]
and `grain` 1. One muon of the catalog's `mu` (content 207, the electron's
whole charge -7344 over its 207 units, [-7344, 207] per unit of content) at
x = 10 with `directions` [[1, 0, 0]] alone (so that its products leave
toward the +x face, at rest too) and `become` at 64 into the catalog's `e`
(the electron family: the body left of no content) with the products
`beta` (1, 207: the catalog's electron born by `become`, a paid row of the
muon's whole content and its charge -7344) and `nu` (1, 0). Three worlds:
the muon at rest, at p = 3640 and at p = 12 856 label units (17.6 M2: the
momenta at which gamma = E' / E'_0 is 1.1074 and 1.9558, beta 0.4297 and
0.8594). The two open faces are the detectors.

The pins, written here before any run, each with its kind:

- the DETECTOR reading: the `beta` product's click on `face:+x`, at the
  design's tick 391, 367 and 345 with two ticks' tolerance (17.6 M9; N6:
  390.6, 368.2 and 345.2 with the drive's whole steps), and at the tick
  derived from the engine's own rules (the 64th self-creation below, the
  decay's Node, the flight table's steps of the heading row, `derived`);
  the decay's tick derived back from the click by the flight table;
- the GAMEBOARD reading: the `become` line's tick, the 64th self-creation,
  at the design's 64, 70.9 and 125.2 with one tick's tolerance (18.1 (a)),
  and at the tick the proper-time count gives from an empty accumulator,
  k + floor((k - 1) (E' - E'_0) / E'_0) for the k-th self-creation (64, 70
  and 124: the count charged after each of the first k - 1 self-creations),
  which is 64 gamma less (gamma - 1) to within one; the decay's Node at
  x = 10 + floor(64 p / (Q S M)) (10, 27, 72); E' at load isqrt(E'_0^2 +
  3 p^2) (13 248, 14 671, 25 910);
- the invariant E'^2 <= W < (E' + 1)^2 on every `energy` line of every
  interval of every run (GAMEBOARD; the engine refuses otherwise).

The `coasting_none` world under the key (17.6 M2, N5; NATURE row 4b; pin
(c) of 18.1): series G2's `coasting_none` as registered (the momenta as
declared, the centre's `wave` set, the families by reference) with the key
`c2` [1, 3], `grain` 2^18 (W / g^2 within the integer bound; 2^16 is
refused) and the model id `rays-hubble-stars-record-covariant-none-space-v1`,
which tells the readings tool to read z from the gather lines (since the
one click every unit of a star's light is a record and the `wave` set's own
pointer no longer turns: the register's `source` rule, record 124); the
identity's load-time diagnostic names every paid family off 3 h n = Q S d
(the 24 stars and the detector, quantum 1 at Q S = 2^26: the gap 3 - 2^26
each; a refusal only under `books`, not declared). The DETECTOR reading:
the star `s_mz2`'s z in the late window [300, 400), `1 + z = Delta t /
Delta Phi` from the gather lines (the record's birth phase u, one step per
self-creation of the lamp, against the arrival's tick;
`tools/hubble_stars_readings.py`'s rule), pinned at 0.369 +- 0.003 (the
design's pin on the registered momentum; the centre 0.3687 with the
continuum's beta = sqrt 3 p / E', 0.3663 with the lattice's on the heading,
gamma (1 + (p / E') / c) - 1 at c = 32 / 55, 17.6 N5, E'_0 = Q S x
4 198 400; both inside); the register's 0.2636 without the key (NATURE row
4b, the acoustic rule before the one click). The GAMEBOARD
readings: gamma = E' / E'_0 at load for `s_mz2` (E'_0 = Q S x 4 198 400,
the light plus the mass), the pace p / E' in Links per interval, the
invariant on every `energy` line.

Nothing here is a test: the runs are made once and registered
(`README.md`, docs/EXPERIMENTS.md, docs/VALIDATION.md); a reading outside
its pin is reported with its numbers, never moved.
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from event_universe.core.integer import integer_root  # noqa: E402
from event_universe.events.nature_beam import direction_flight  # noqa: E402
from event_universe.events.world import HEADING_OFFSET, Q  # noqa: E402
from event_universe.world_loading import families_by_definition, load_world  # noqa: E402

Json = dict[str, object]

IDENTITY = "covariant-readings-v1"
FAMILY_DEFINITIONS = "../entities/families.json"
DEFINITIONS_SOURCE = (HERE.parent / "entities" / "families.json").read_bytes()
C2 = [1, 3]
# The J4 bar: the +x face at x = 200, the muon born at x = 10.
BAR = 201
BORN = 10
CONTENT = 207
AT = 64
WIDTH = 1
TICKS = 420
# The momenta of 17.6 M2 (label units) by name.
MUONS = {"rest": 0, "3640": 3640, "12856": 12856}
# The design's pins (17.6 M9, 18.1 (a)): the 64th self-creation and the
# `beta` click on the +x face, with their tolerances.
DESIGN_DECAY = {"rest": 64.0, "3640": 70.9, "12856": 125.2}
DESIGN_CLICK = {"rest": 391, "3640": 367, "12856": 345}
DECAY_TOLERANCE = 1.0
CLICK_TOLERANCE = 2
# The coasting world under the key: the grain that fits W / g^2 in the word.
COASTING_GRAIN = 1 << 18
COASTING_MODEL = "rays-hubble-stars-record-covariant-none-space-v1"
STAR = "s_mz2"
Z_PIN = [0.366, 0.372]
LATE_WINDOW = [300, 400]


def load_generator(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def muon_world(name: str, momentum: int) -> Json:
    document: Json = {
        "law": "beam",
        "model_id": f"beam-covariant-j4_muon_{name}-v1",
        "shape": [BAR, 1, 1],
        "boundary": "open",
        "ticks": TICKS,
        "K": 1 << 20,
        "N": 64,
        "release": [1, 1 << 20],
        "suspension": 0,
        "width": WIDTH,
        "covariant_readings": {"c2": list(C2), "grain": 1},
        "families": [
            {"name": "mu", "quantum": 0, "charge": [-7344, CONTENT], "phase": True},
            {"name": "e", "quantum": 0, "charge": -15, "phase": True},
            {"name": "beta", "quantum": 1, "charge": -7344},
            {"name": "nu", "quantum": 0},
        ],
        "measured": [
            {
                "position": [BORN, 0, 0],
                "family": "mu",
                "amount": CONTENT,
                "momentum": [momentum, 0, 0],
                "directions": [[1, 0, 0]],
                "become": {
                    "at": AT,
                    "into": "e",
                    "products": [["beta", 1, CONTENT], ["nu", 1, 0]],
                },
            }
        ],
    }
    return families_by_definition(document, FAMILY_DEFINITIONS, DEFINITIONS_SOURCE)


def coasting_world() -> Json:
    """Series G2's `coasting_none` as registered (the centre's `wave` set,
    the families by reference), under the key, its model id naming the
    record rule (`rays-hubble-stars-record-...`): since the one click of
    the amplitude law every unit of a star's light is a record and the
    `wave` set's own pointer no longer turns on this world (its acoustic z
    reads undefined, `tests/test_hubble_stars_readings.py` (b)), so the
    register reads z from the gather lines, the slope of the record's birth
    phase u (the lamp's birth wheel, one step per self-creation) against
    the arrival's tick (the `source` rule of record 124;
    `tools/hubble_stars_readings.py` reads it under that model id)."""
    generator = load_generator(
        "hubble_stars_make_worlds", HERE.parent / "hubble_stars" / "make_worlds.py"
    )
    document: Json = generator.referenced(generator.world("coasting", "none"))
    found: Json = {}
    for key, value in document.items():
        found[key] = COASTING_MODEL if key == "model_id" else value
        if key == "suspension":
            found["covariant_readings"] = {"c2": list(C2), "grain": COASTING_GRAIN}
    return found


def worlds() -> dict[str, Json]:
    found = {f"j4_muon_{name}": muon_world(name, momentum) for name, momentum in MUONS.items()}
    found["coasting_none_covariant"] = coasting_world()
    return found


def energy(rest: int, momentum: int, grain: int = 1, factor: int = C2[1]) -> int:
    """E' / g at load: isqrt((E'_0 / g)^2 + d (p / g)^2), the declared
    load-time root at the identity's grain (the engine's `covariant_square`)."""
    rest_g, momentum_g = rest // grain, abs(momentum) // grain
    return integer_root(rest_g * rest_g + factor * momentum_g * momentum_g)


def self_creation_tick(k: int, rest: int, energy_prime: int) -> int:
    """The tick of the k-th self-creation under the proper-time gate from an
    empty accumulator: k + floor((k - 1) (E' - E'_0) / E'_0)."""
    return k + (k - 1) * (energy_prime - rest) // rest


def flight_table():
    """The engine's flight table of the J4 bar (the six headings)."""
    document = muon_world("rest", 0)
    source = json.dumps(document).encode("utf-8")
    world = load_world(source, base_dir=HERE, root=HERE.parent).world
    return direction_flight(world.directions)


def heading_click(steps: int) -> int:
    """The least age at which a row on the +x heading has made `steps`
    Manhattan steps (the engine's flight table)."""
    flight = flight_table()
    heading = np.array([HEADING_OFFSET])
    age = 0
    while int(flight.manhattan_steps(heading, np.array([age]))[0]) < steps:
        age += 1
    return age


def heading_pace() -> float:
    """c on a heading, Links per interval (Q / T_D = 32 / 55)."""
    flight = flight_table()
    heading = np.array([HEADING_OFFSET])
    period = int(flight.period[HEADING_OFFSET])
    return int(flight.manhattan_steps(heading, np.array([period]))[0]) / period


def muon_expectation(name: str, momentum: int) -> Json:
    rest = Q * WIDTH * CONTENT
    energy_prime = energy(rest, momentum)
    gamma = energy_prime / rest
    decay_tick = self_creation_tick(AT, rest, energy_prime)
    decay_node = BORN + AT * momentum // rest
    steps = BAR - decay_node
    click_tick = decay_tick + heading_click(steps)
    return {
        "momentum": momentum,
        "rest_energy": rest,
        "energy_at_load": energy_prime,
        "gamma": gamma,
        "beta": math.sqrt(C2[1]) * momentum / energy_prime,
        "pace": momentum / energy_prime,
        "decay": {
            "kind": "GAMEBOARD",
            "line": "become",
            "design": DESIGN_DECAY[name],
            "tolerance": DECAY_TOLERANCE,
            "derived_tick": decay_tick,
            "derived_node": [decay_node, 0, 0],
        },
        "click": {
            "kind": "DETECTOR",
            "line": "click on face:+x of the product beta",
            "design": DESIGN_CLICK[name],
            "tolerance": CLICK_TOLERANCE,
            "derived_tick": click_tick,
            "steps_to_the_face": steps,
        },
        "invariant": {"kind": "GAMEBOARD", "line": "energy", "holds": True},
    }


def coasting_expectation() -> Json:
    generator = sys.modules["hubble_stars_make_worlds"]
    star = next(s for s in generator.stars(generator.MASS) if s["name"] == STAR)
    content = int(generator.MASS) + int(generator.LIGHT)
    momentum = int(star["momentum"])
    rest = Q * int(generator.WIDTH) * content
    energy_prime = energy(rest, momentum, COASTING_GRAIN)
    gamma = energy_prime / (rest // COASTING_GRAIN)
    pace = momentum / (energy_prime * COASTING_GRAIN)
    c = heading_pace()
    return {
        "star": STAR,
        "momentum": momentum,
        "content": content,
        "rest_energy": rest,
        "rest_energy_at_the_grain": rest // COASTING_GRAIN,
        "energy_at_load_at_the_grain": energy_prime,
        "grain": COASTING_GRAIN,
        "gamma": gamma,
        "pace": pace,
        "z": {
            "kind": "DETECTOR",
            "line": "record (the centre's pointer), the late window",
            "window": list(LATE_WINDOW),
            "pin": list(Z_PIN),
            "design": 0.369,
            "centre_continuum": gamma * (1 + math.sqrt(C2[1]) * pace) - 1,
            "centre_heading": gamma * (1 + pace / c) - 1,
            "registered_without_the_key": 0.2636,
        },
        "invariant": {"kind": "GAMEBOARD", "line": "energy", "holds": True},
    }


def expectations() -> Json:
    found: Json = {
        "format": "covariant-expectations-v1",
        "identity": IDENTITY,
        "c2": list(C2),
        "worlds": {
            **{f"j4_muon_{name}": muon_expectation(name, momentum) for name, momentum in MUONS.items()},
            "coasting_none_covariant": coasting_expectation(),
        },
        "derivations": {
            "energy_at_load": (
                "isqrt(E'_0^2 + 3 p . p), E'_0 = Q S M (DERIVATIONS_BEAM 17.6 M3: the declared "
                "load-time root); gamma = E' / E'_0; the pace p / E' Links per interval (17.6 M1)"
            ),
            "decay": (
                "the design's 64 gamma (17.6 M2, 18.1 (a)) with one tick's tolerance; the derived "
                "tick the k-th self-creation under the proper-time gate from an empty accumulator, "
                "k + floor((k - 1) (E' - E'_0) / E'_0) (BEAM_LAW note 41's by_drive at the rate "
                "E' - E'_0 over the wall E'_0, charged after each self-creation), which is 64 gamma "
                "less (gamma - 1) to within one; the decay's Node 10 + floor(64 p / (Q S M)) (the "
                "drive without its cap term at 64 self-creations)"
            ),
            "click": (
                "the design's 391, 367, 345 (17.6 M9; N6: 390.6, 368.2, 345.2) with two ticks' "
                "tolerance; the derived tick the decay's tick plus the least age at which the "
                "engine's flight table has a heading row make 201 - x steps (the row born at the "
                "decay's Node x at age 0 leaves the bar through x = 200; Flight.manhattan_steps)"
            ),
            "z": (
                "the design's 0.369 +- 0.003 on the registered momentum (17.6 M2, N5; 18.1 (c)); "
                "the centres gamma (1 + beta) - 1 with beta = sqrt 3 p / E' (the continuum) and "
                "beta = (p / E') / c on the heading, c = 32 / 55 (17.6 S11); read by "
                "tools/hubble_stars_readings.py's window_point on the late window"
            ),
            "invariant": "E'^2 <= W < (E' + 1)^2 on every `energy` line (17.6 M3)",
        },
    }
    return found


def main() -> None:
    for name, document in worlds().items():
        path = HERE / f"{name}.json"
        path.write_text(json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8")
        print(path.relative_to(ROOT))
    expected = expectations()
    existing = HERE / "expectations.json"
    if existing.exists():
        # The run blocks (the source sha, the digests, the readings) are
        # written after the runs and kept.
        previous = json.loads(existing.read_text(encoding="utf-8"))
        if "runs" in previous:
            expected["runs"] = previous["runs"]
    existing.write_text(json.dumps(expected, indent=1) + "\n", encoding="utf-8")
    print(existing.relative_to(ROOT))
    for name, entry in expected["worlds"].items():  # type: ignore[union-attr]
        print(
            name,
            json.dumps(
                {k: v for k, v in entry.items() if k in ("gamma", "pace", "decay", "click", "z")}
            ),
        )


if __name__ == "__main__":
    main()
