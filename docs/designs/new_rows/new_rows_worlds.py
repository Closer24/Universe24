"""The worlds and the pins of PINS.md (the New Rows Scout, 2026-09-23, step 1
of the Boss's order on the owner's word of record 1173: four candidate new
rows of the comparison table, R1 to R4).

Writes `worlds/*.json` (every world under existing keys: `boundary` per
axis, `clock_stamp`, a lamp's `directions`, `phase_window`; no engine line,
no key of a hypothesis, no default changed), validates every world at load
through the shipped loader (`load_world`) and never runs one, and writes the
pins `new_rows_pins.json` with its print `new_rows_pins.out`: every number a
COMPUTATION from the closed forms of the click frame (the r-free lines,
docs/ALGEBRA.md 5.1), from the click's own rungs (`amplitude.rungs`, BEAM_LAW
note 46) on the engine's half-angle tables, and from the engine's own flight
table (`direction_flight`), before any run; the registered readings of R1
and R4 are read from their register files and repeated, not recomputed.

Usage: `PYTHONPATH=src python docs/designs/new_rows/new_rows_worlds.py`.
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

from event_universe.core.phase import phase_cosines, phase_sines  # noqa: E402
from event_universe.events.amplitude import rungs  # noqa: E402
from event_universe.events.nature_beam import direction_flight  # noqa: E402
from event_universe.events.world import HEADING_OFFSET, Q  # noqa: E402
from event_universe.world_loading import load_world  # noqa: E402

WORLDS = HERE / "worlds"
Json = dict[str, object]

# --- R2, the Sagnac ratio: the cart of RUN_4AB on a periodic bar -------------
# The cart world of the moving detector (examples/events/moving_detector/
# make_worlds.py, `cart_k<k>`; docs/designs/fail_rows/run_4ab_worlds.py,
# `cart_world`) with three declarations changed and nothing added: the x axis
# periodic (the loop), the cart's lamp on both headings (the two
# counter-propagating pulses of one birth), the post and the source removed
# (no transponder: the returns are the pulses' own after one turn of the loop).
SAGNAC_TICKS = 1500
SAGNAC_BAR = 240
CART_WIDTH = 1 << 20
CART_K = 4202496
CART_HELD = 4194304
CART_AMOUNT = 8192
SAGNAC_LADDER = (3, 5, 9, 17)
SAGNAC_FROM_COUNT = 60

# --- R3, Malus at three new settings: malus_22_5's world at another window ---
# examples/events/amplitude/malus_22_5.json as registered (the lamp on the
# wheel [159, 256], the which-path `read` at x = 4, the window at x = 6), the
# window's setting the one declaration changed; the catalog's two families
# (photon: `light`; counter_material: `counter`) inlined so that the world is
# a portable input from this folder (the loader confines a reference to the
# world's parent folder), as run_4ab_worlds.py inlines the coasting world's.
MALUS_SOURCE = ROOT / "examples" / "events" / "amplitude" / "malus_22_5.json"
CATALOG = ROOT / "examples" / "events" / "entities" / "families.json"
MALUS_SETTINGS = (16, 40, 48)
MALUS_N = 256
MALUS_BIRTHS = 256

# --- R1 and R4, registered readings repeated, not recomputed -----------------
PAIR_EXPECTATIONS = ROOT / "examples" / "events" / "amplitude" / "expectations.json"
RUN_4AB_READINGS = ROOT / "docs" / "designs" / "fail_rows" / "run_4ab_readings.json"
RUN_4AB_PINS = ROOT / "docs" / "designs" / "fail_rows" / "run_4ab_pins.json"


def sagnac_world(k: int) -> Json:
    momentum = Q * CART_WIDTH * CART_K // (k - 1)
    return {
        "law": "beam",
        "model_id": f"beam-new-rows-sagnac-k{k}-v1",
        "shape": [SAGNAC_BAR, 3, 3],
        "boundary": {"x": "periodic"},
        "ticks": SAGNAC_TICKS,
        "K": CART_K,
        "N": 64,
        "release": [1, 65536],
        "suspension": 0,
        "width": CART_WIDTH,
        "clock_stamp": True,
        "families": [
            {"name": "cart", "quantum": 1},
            {"name": "mass", "quantum": 0, "charge": 0, "phase": False},
        ],
        "measured": [
            {
                "position": [20, 1, 1],
                "family": "cart",
                "amount": CART_AMOUNT,
                "phase": 0,
                "momentum": [momentum, 0, 0],
                "held": {"mass": CART_HELD},
                "directions": [[1, 0, 0], [-1, 0, 0]],
                "lamp": {
                    "rate": [1, 1],
                    "wheel": [1, 64],
                    "directions": [[1, 0, 0], [-1, 0, 0]],
                },
                "table": {
                    "cart": {"rule": "measure", "reads": "age"},
                    "mass": {"rule": "pass"},
                },
            },
        ],
    }


def malus_world(setting: int) -> Json:
    document = json.loads(MALUS_SOURCE.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    by_name = {entity["name"]: entity for entity in catalog["entities"]}
    families: list[object] = []
    for entity in document.pop("entities"):
        named = by_name[str(entity["definition"])]
        if named["measured"] or named["detectors"]:
            raise ValueError(f"{named['name']}: the entity places events; only families are inlined")
        families.extend(named["families"])
    document.pop("entity_definitions")
    document["families"] = families
    document["model_id"] = f"beam-new-rows-malus-s{setting}-v1"
    window_entry = document["measured"][2]["table"]["light"]
    if window_entry != {"phase_window": 32}:
        raise ValueError("malus_22_5's window entry is not the one this file expects")
    window_entry["phase_window"] = setting
    return document


def worlds() -> dict[str, Json]:
    found: dict[str, Json] = {}
    for k in SAGNAC_LADDER:
        found[f"sagnac_k{k}"] = sagnac_world(k)
    for setting in MALUS_SETTINGS:
        found[f"malus_s{setting}"] = malus_world(setting)
    return found


# --- the closed forms ---------------------------------------------------------


def loaded(document: Json):
    """The world through the shipped loader: validated at load, never run."""
    return load_world(json.dumps(document).encode("utf-8"), base_dir=WORLDS, root=ROOT)


def heading_pace(flight) -> Fraction:
    heading = np.array([HEADING_OFFSET])
    period = int(flight.period[HEADING_OFFSET])
    return Fraction(int(flight.manhattan_steps(heading, np.array([period]))[0]), period)


def sagnac_pins(k: int, c: Fraction) -> Json:
    """The two returns of one birth at the cart's own count, r-free. The
    co-moving pulse (+x, the cart's heading) closes on the receding cart at
    c - v after one turn of the loop, the counter-propagating pulse (-x)
    meets it at c + v: t_+ = L / (c - v), t_- = L / (c + v) intervals after
    the birth, exactly in the mean (the accumulators' carries, ALGEBRA 4.1);
    the cart's own count is r times the interval (r = 1 on the law), so the
    ratio (n_+ - n_-) / (n_+ + n_- - 2 n_0) = v / c = beta whatever r."""
    v = Fraction(1, k)
    beta = v / c
    t_plus = SAGNAC_BAR / (c - v)
    t_minus = SAGNAC_BAR / (c + v)
    remainder_per_end = k + Fraction(55, 32)
    return {
        "k": k,
        "momentum": Q * CART_WIDTH * CART_K // (k - 1),
        "pace_links_per_interval": str(v),
        "heading_c": str(c),
        "beta_on_the_heading": {"exact": str(beta), "value": float(beta)},
        "returns_after_the_birth_intervals": {
            "kind": "GAMEBOARD (the ticks; the cart's count equals them at r = 1)",
            "co_moving_plus_x": {"exact": str(t_plus), "value": float(t_plus)},
            "counter_minus_x": {"exact": str(t_minus), "value": float(t_minus)},
            "ordinals_with_both_returns_inside_the_run": int(SAGNAC_TICKS - math.ceil(t_plus)),
        },
        "ratio": {
            "kind": "DETECTOR",
            "line": "(n_+ - n_-) / (n_+ + n_- - 2 n_0) over the ordinals from the cart's count "
            f"{SAGNAC_FROM_COUNT}, n_0 the birth line's clock, n_+ and n_- the two click lines "
            "of that ordinal at the cart (its own family), read from the stamped clock alone",
            "pin": {"exact": str(beta), "value": float(beta)},
            "reads": "v / c, r-free (the click frame's r-free lines; ALGEBRA.md 5.1)",
            "comparison": "the Sagnac ratio v / c, Michelson-Gale 1925 (the first-order form)",
        },
        "band": {
            "kind": "COMPUTATION",
            "remainder_per_end_counts": {
                "exact": str(remainder_per_end),
                "value": float(remainder_per_end),
            },
            "on_the_ratio": float(2 * remainder_per_end / (t_plus + t_minus)),
            "reads": "one hop (k intervals) plus one dwell (55/32) at each return, RUN_4AB.md section 6.3, "
            "over the sum of the two returns; a mean over the window narrows it",
        },
    }


def malus_pins(setting: int) -> Json:
    """One polariser: the row born on label 0 read at the window s (the
    which-path read at x = 4 with no rotation before it keeps the whole beam
    on label 0), the cells + and - weighing C'[s]^2 and S'[s]^2 (the malus
    note's section 3 (ii)), the counts over 256 births by the click's rungs."""
    cosines, sines = phase_cosines(2 * MALUS_N), phase_sines(2 * MALUS_N)
    c_s, s_s = int(cosines[setting]), int(sines[setting])
    weights = [((256 * c_s) ** 2, 1), ((256 * s_s) ** 2, 1)]
    found, total = rungs(weights, MALUS_BIRTHS)
    counts = [found[0], found[1] - found[0]]
    angle = 180.0 * setting / MALUS_N
    cos2 = math.cos(math.radians(angle)) ** 2
    return {
        "setting": setting,
        "angle_degrees": angle,
        "tables": {"C": c_s, "S": s_s, "norm_over_65536": (c_s * c_s + s_s * s_s) / 65536},
        "weights": {"0+": weights[0][0], "0-": weights[1][0]},
        "rungs": [0, *found],
        "counts": {"kind": "DETECTOR", "0+": counts[0], "0-": counts[1]},
        "pass_fraction": {"kind": "DETECTOR", "value": counts[0] / MALUS_BIRTHS},
        "comparison": {"cos2": cos2, "count_times_256": 256 * cos2},
        "departure": {"kind": "COMPUTATION", "value": counts[0] / MALUS_BIRTHS - cos2},
        "reads": "the pass cell 0+ over the 256 births (u = ordinal x 159 mod 256, every residue once)",
    }


def registered_r1() -> Json:
    expectations = json.loads(PAIR_EXPECTATIONS.read_text(encoding="utf-8"))
    pair = expectations["pair"]
    return {
        "kind": "DETECTOR (registered; repeated, not recomputed)",
        "source": "examples/events/amplitude/expectations.json, pair.marginal and pair.chsh",
        "marginal": pair["marginal"],
        "births": 64,
        "cells": {label: entry["counts"] for label, entry in pair["chsh"].items()},
        "marginals_from_the_cells": {
            label: {
                "first_plus": entry["counts"]["++"] + entry["counts"]["+-"],
                "second_plus": entry["counts"]["++"] + entry["counts"]["-+"],
            }
            for label, entry in pair["chsh"].items()
        },
    }


def registered_r4() -> Json:
    readings = json.loads(RUN_4AB_READINGS.read_text(encoding="utf-8"))["runs"]
    pins = json.loads(RUN_4AB_PINS.read_text(encoding="utf-8"))["ladder"]
    out: Json = {
        "kind": "DETECTOR (registered by RUN_4AB.md section 6.3; repeated, not recomputed)",
        "source": "docs/designs/fail_rows/run_4ab_readings.json, runs.<world>.readings.round_trip",
    }
    for name in ("cart_k3_law", "cart_k5_law", "cart_k3_key", "cart_k5_key"):
        trip = readings[name]["readings"]["round_trip"]
        pin = pins.get(name, {}) if isinstance(pins, dict) else {}
        exact = pin.get("exact_fractions") if isinstance(pin, dict) else None
        out[name] = {
            "read": trip["value"],
            "window_counts": trip["window"],
            "returns": trip["ordinals"],
            "pin": trip["pin"],
            "pin_exact": exact["round_trip"] if isinstance(exact, dict) else None,
            "counts_off": trip["counts_off"],
            "remainder_per_end": trip["remainder_per_end"],
            "against_the_band_as_pinned": trip["verdict"],
            "against_the_preregistration_band": trip["verdict_v2"],
        }
    return out


def main() -> None:
    WORLDS.mkdir(exist_ok=True)
    documents = worlds()
    validated: dict[str, str] = {}
    flight = None
    for name, document in documents.items():
        path = WORLDS / f"{name}.json"
        path.write_text(
            json.dumps(document, indent=None, separators=(", ", ": ")) + "\n", encoding="utf-8"
        )
        world = loaded(document)
        validated[name] = world.world.model_id if hasattr(world.world, "model_id") else "loaded"
        if name == "sagnac_k3":
            flight = direction_flight(world.world.directions)
    assert flight is not None
    c = heading_pace(flight)
    pins: Json = {
        "format": "new-rows-pins-v1",
        "worlds_validated_at_load": validated,
        "R1_marginals": registered_r1(),
        "R2_sagnac": {f"sagnac_k{k}": sagnac_pins(k, c) for k in SAGNAC_LADDER},
        "R3_malus": {f"malus_s{s}": malus_pins(s) for s in MALUS_SETTINGS},
        "R4_round_trip": registered_r4(),
    }
    (HERE / "new_rows_pins.json").write_text(json.dumps(pins, indent=2) + "\n", encoding="utf-8")
    lines = [
        "THE PINS OF PINS.md, BEFORE ANY RUN (COMPUTATION unless labelled; the worlds validated at load, none run)",
        "",
        "Worlds validated at load: " + ", ".join(f"{k} ({v})" for k, v in validated.items()),
        "",
        "R1 the marginals (registered, DETECTOR): pair.marginal = "
        f"{pins['R1_marginals']['marginal']} of 64 at every setting; from the cells: "
        + "; ".join(
            f"{label}: first + {m['first_plus']}, second + {m['second_plus']}"
            for label, m in pins["R1_marginals"]["marginals_from_the_cells"].items()
        ),
        "",
        f"R2 the Sagnac ratio on the periodic bar of {SAGNAC_BAR} Nodes, c = {c} on the heading:",
    ]
    for k in SAGNAC_LADDER:
        p = pins["R2_sagnac"][f"sagnac_k{k}"]
        lines.append(
            f"  k = {k}: beta = {p['beta_on_the_heading']['exact']} = {p['beta_on_the_heading']['value']:.5f}; "
            f"the returns t_+ = {p['returns_after_the_birth_intervals']['co_moving_plus_x']['exact']} = "
            f"{p['returns_after_the_birth_intervals']['co_moving_plus_x']['value']:.2f}, "
            f"t_- = {p['returns_after_the_birth_intervals']['counter_minus_x']['exact']} = "
            f"{p['returns_after_the_birth_intervals']['counter_minus_x']['value']:.2f} intervals; "
            f"{p['returns_after_the_birth_intervals']['ordinals_with_both_returns_inside_the_run']} ordinals with both "
            f"returns inside {SAGNAC_TICKS}; the band on the ratio {p['band']['on_the_ratio']:.4f} "
            f"(the remainder {p['band']['remainder_per_end_counts']['value']:.3f} counts per end)"
        )
    lines.append("")
    lines.append("R3 Malus at the new settings (N = 256, W = 256; the half-angle tables of 512):")
    for s in MALUS_SETTINGS:
        p = pins["R3_malus"][f"malus_s{s}"]
        lines.append(
            f"  s = {s} ({p['angle_degrees']:.3f} degrees): C' = {p['tables']['C']}, S' = {p['tables']['S']}, "
            f"rungs {p['rungs']}, the counts 0+ {p['counts']['0+']}, 0- {p['counts']['0-']}: "
            f"the pass {p['counts']['0+']} of 256 = {p['pass_fraction']['value']:.5f} against cos^2 = "
            f"{p['comparison']['cos2']:.5f} (x 256 = {p['comparison']['count_times_256']:.2f}), "
            f"the departure {p['departure']['value']:+.5f}"
        )
    lines.append("")
    lines.append("R4 the round trip (registered by RUN_4AB 6.3, DETECTOR):")
    for name in ("cart_k3_law", "cart_k5_law", "cart_k3_key", "cart_k5_key"):
        p = pins["R4_round_trip"][name]
        lines.append(
            f"  {name}: read {p['read']:.5f} over {p['window_counts']} counts ({int(p['returns'])} returns) "
            f"against the pin {p['pin']:.5f} ({p['pin_exact']}); {p['counts_off']:+.2f} counts off, the remainder "
            f"{p['remainder_per_end']:.2f} per end; {p['against_the_band_as_pinned']} against the band as pinned, "
            f"{p['against_the_preregistration_band']} against the preregistration's band"
        )
    (HERE / "new_rows_pins.out").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
