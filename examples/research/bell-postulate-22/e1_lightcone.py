"""E1: the light cone of one integer.

Two bonded worlds identical except the single pair's registry number, replaced by
bond.stream=[n]. Every tick's snapshot + inventory of both worlds is diffed; each
differing Node must lie inside the forward cone (Manhattan distance <= t - t_ask)
of an end that has already asked. Control: stream = the world's own number.

Run:  PYTHONPATH=src python examples/research/bell-postulate-22/e1_lightcone.py --output DIR
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    PHASE_STEPS,
    PROBE,
    TICKET_MODULUS,
    BondRegistry,
    Logged,
    bonded_world,
    dump,
    origin_bond,
    output_argument,
    salt_positions,
    stamp,
)

from event_universe.core.spatial_state import PHASE_COSINE_SCALE, phase_cosines  # noqa: E402

SEEDS = (1, 2, 3, 4, 5, 6, 7, 8)
WIDTH = PROBE.WIDTH
CENTER = PROBE.CENTER
BOND = origin_bond((CENTER, 1, 1), (WIDTH, 3, 3), 0)


def coin(number: int) -> int:
    return 1 if 2 * number < TICKET_MODULUS else -1


def rest(number: int) -> int:
    return (2 * number) % TICKET_MODULUS


def agree(number: int, difference: int) -> bool:
    cosine = phase_cosines(PHASE_STEPS)[difference % PHASE_STEPS]
    return rest(number) * 2 * PHASE_COSINE_SCALE < (PHASE_COSINE_SCALE - cosine) * TICKET_MODULUS


def coin_flipped(number: int) -> int:
    """Upper half flipped, lower half moved by one unit."""
    return (number + (TICKET_MODULUS + 1) // 2) % TICKET_MODULUS


def agreement_flipped(number: int, difference: int) -> int:
    """Same coin, lower half moved across the agreement threshold of the settings' difference."""
    cosine = phase_cosines(PHASE_STEPS)[difference % PHASE_STEPS]
    threshold = (PHASE_COSINE_SCALE - cosine) * TICKET_MODULUS // (2 * PHASE_COSINE_SCALE)
    target = threshold // 2 if not agree(number, difference) else (threshold + TICKET_MODULUS) // 2
    # 2n mod M = target with the same coin: coin +1 needs 2n = target (target even),
    # coin -1 needs 2n = target + M (target odd, M odd).
    if coin(number) > 0:
        target -= target % 2
        candidate = target // 2
    else:
        target += (target + 1) % 2
        candidate = (target + TICKET_MODULUS) // 2
    assert coin(candidate) == coin(number) and agree(candidate, difference) != agree(number, difference)
    return candidate


def state_of(logged: Logged) -> dict:
    """The complete per-position state of a world at the current tick, JSON-able."""
    world = logged.world
    snap = world.snapshot()
    per_position: dict[str, dict] = {}

    def slot(position) -> dict:
        return per_position.setdefault(str(tuple(position)), {})

    for node in snap["nodes"]:
        slot(node["position"])["node"] = json.loads(json.dumps(node, default=str))
    for entry in snap["spatial_fields"]:
        slot(entry["position"])["spatial"] = json.loads(json.dumps(entry, default=str))
    for node in world.inventory_view().nodes:
        rays = [str(r) for r in (node.rays[0] if node.rays else ())]
        claims = [str(c) for c in (node.claims[0] if node.claims else ())]
        incoming = str(node.incoming_spatial) if node.incoming_spatial else ""
        if rays or claims or incoming:
            slot(node.position)["inventory"] = {"rays": rays, "claims": claims, "incoming": incoming}
    globals_ = {
        "escaped_totals": json.loads(json.dumps(snap["escaped_totals"], default=str)),
        "transfers": json.loads(json.dumps(snap["transfers"], default=str)),
        "spatial_transfers": json.loads(json.dumps(snap["spatial_transfers"], default=str)),
        "registry_open": sorted(logged.registry.open),
        "registry_numbers": logged.registry.numbers,
    }
    return {"positions": per_position, "globals": globals_}


def trace(raw: dict) -> dict:
    """Run a world tick by tick; return states per tick and the asks with positions."""
    logged = Logged(raw)
    states = [state_of(logged)]
    asks = []
    for _ in range(raw["ticks"]):
        salts = salt_positions(logged)
        before = len(logged.log)
        logged.world.step()
        for entry in logged.log[before:]:
            asks.append({**entry, "position": salts.get(entry["salt"])})
        states.append(state_of(logged))
    return {"states": states, "asks": asks, "outcomes": logged.outcomes()}


def manhattan(p, q) -> int:
    return sum(abs(a - b) for a, b in zip(p, q, strict=False))


def diff_worlds(base: dict, other: dict) -> list[dict]:
    """Per tick: differing positions and differing globals."""
    rows = []
    for t, (sa, sb) in enumerate(zip(base["states"], other["states"], strict=True)):
        keys = set(sa["positions"]) | set(sb["positions"])
        differing = sorted(k for k in keys if sa["positions"].get(k) != sb["positions"].get(k))
        global_diffs = sorted(k for k in sa["globals"] if sa["globals"][k] != sb["globals"][k])
        rows.append({"tick": t, "positions": differing, "globals": global_diffs})
    return rows


def cone_check(rows: list[dict], asks: list[dict]) -> dict:
    """Every differing position must lie within t - t_ask of an end that changed answer."""
    violations = []
    first_diff = None
    for row in rows:
        t = row["tick"]
        for key in row["positions"]:
            position = tuple(json.loads(key.replace("(", "[").replace(")", "]")))
            inside = any(
                ask["tick"] < t and manhattan(position, ask["position"]) <= t - ask["tick"]
                for ask in asks
                if ask["position"] is not None
            )
            if first_diff is None:
                first_diff = t
            if not inside:
                violations.append({"tick": t, "position": position})
        for key in row["globals"]:
            if key in ("registry_open", "registry_numbers"):
                continue  # the registry is the declared exception; reported, not a Node
            if first_diff is None:
                first_diff = t
            if not any(ask["tick"] < t for ask in asks):
                violations.append({"tick": t, "global": key})
    return {"first_differing_tick": first_diff, "violations": violations}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    output_argument(parser)
    out_dir = parser.parse_args().output / "e1_lightcone"
    started = time.perf_counter()
    report = {**stamp(), "bond": BOND, "seeds": SEEDS, "cases": []}
    geometries = {
        "symmetric_3_3": (3, 3),
        "asymmetric_alice3_bob5": (3, 5),
        "asymmetric_alice5_bob3": (5, 3),
    }
    all_pass = True
    for geometry, (da, db) in geometries.items():
        for alice, bob in ((0, 8), (16, 24)):
            for seed in SEEDS:
                number = BondRegistry(seed, PHASE_STEPS).number(BOND)
                variants = {
                    "own_sequence": None,
                    "control_same_number": number,
                    "coin_flip": coin_flipped(number),
                    "agreement_flip": agreement_flipped(number, bob - alice),
                }
                traces = {
                    name: trace(
                        bonded_world(
                            0,
                            alice,
                            bob,
                            seed,
                            dist_alice=da,
                            dist_bob=db,
                            stream=None if value is None else [value],
                        )
                    )
                    for name, value in variants.items()
                }
                base = traces["own_sequence"]
                case = {
                    "geometry": geometry,
                    "settings": {"alice": alice, "bob": bob},
                    "seed": seed,
                    "number": number,
                    "numbers": {k: v for k, v in variants.items() if v is not None},
                    "asks_base": [
                        {k: a[k] for k in ("tick", "position", "setting", "outcome", "drew_number")}
                        for a in base["asks"]
                    ],
                    "outcomes": {
                        name: {
                            k: tr["outcomes"][k]
                            for k in ("alice", "bob", "closed", "numbers", "questions")
                        }
                        for name, tr in traces.items()
                    },
                    "variants": {},
                }
                for name, tr in traces.items():
                    if name == "own_sequence":
                        continue
                    rows = diff_worlds(base, tr)
                    # The cone belongs to the asks whose answer differs between the worlds;
                    # use the union of both worlds' asks (same ticks and positions).
                    asks = base["asks"] + [a for a in tr["asks"]]
                    check = cone_check(rows, asks)
                    nonempty = [r for r in rows if r["positions"] or r["globals"]]
                    case["variants"][name] = {
                        "diff_per_tick": nonempty,
                        **check,
                        "asks_variant": [
                            {k: a[k] for k in ("tick", "position", "setting", "outcome", "drew_number")}
                            for a in tr["asks"]
                        ],
                    }
                    if name == "control_same_number":
                        ok = not nonempty
                    else:
                        ok = not check["violations"]
                    case["variants"][name]["pass"] = ok
                    all_pass = all_pass and ok
                report["cases"].append(case)
                print(
                    geometry,
                    (alice, bob),
                    "seed",
                    seed,
                    "number",
                    number,
                    {
                        n: (v["pass"], v["first_differing_tick"], len(v["violations"]))
                        for n, v in case["variants"].items()
                    },
                )
    report["all_pass"] = all_pass
    report["runtime_seconds"] = round(time.perf_counter() - started, 1)
    dump(out_dir / "results.json", report)
    print("all_pass", all_pass, "runtime", report["runtime_seconds"], "s")


if __name__ == "__main__":
    main()
