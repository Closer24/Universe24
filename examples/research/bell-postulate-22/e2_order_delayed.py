"""E2: who asks first, and delayed choice.

(a) Asymmetric distances: Alice's plus detector at 3 links and Bob's at 5 (Alice asks
    first) and the mirror. CHSH with 1024 fresh registry seeds per setting pair, the
    same seeds in both orderings; ask order verified from the registry log.
(b) Delayed choice. API gap: field_rules and spatial_interactions are rejected on ray
    transport, so no in-world rule can rewrite a detector's setting between steps.
    (i) Legal: two worlds differing only in the settings, same seed and pair number.
    (ii) Flagged private-state variant: the frozen DisturbanceRecord in world._nodes is
    replaced between steps (no edit to src/), writing the intended settings after tick
    2 (after emission, before arrival) or after tick 3 (the last state before the
    asking step), and, as a control, after tick 4 (after the ask).

Run:  PYTHONPATH=src python examples/research/bell-postulate-22/e2_order_delayed.py --workers 4 --output DIR
"""

from __future__ import annotations

import argparse
import multiprocessing
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    PAIRS,
    SETTINGS,
    Logged,
    bonded_world,
    chsh_from,
    correlation_stats,
    dataclasses,
    dump,
    expected_e,
    output_argument,
    run_world,
    stamp,
)

from event_universe.core.disturbance_state import pack  # noqa: E402

PAIRS_PER_CORRELATION = 1024
SEED_BASE = 3 * 2**20
SETTING_FIELD_INDEX = 3  # world fields: quanta, momentum, train, setting


def seed_for(setting: int, index: int) -> int:
    return SEED_BASE + setting * PAIRS_PER_CORRELATION + index


# --- (a) ordering ---------------------------------------------------------------------


def order_job(job: tuple) -> tuple:
    seed, alice, bob, da, db = job
    result = run_world(bonded_world(0, alice, bob, seed, dist_alice=da, dist_bob=db))
    first = result["log"][0] if result["log"] else None
    first_end = None
    if first is not None:
        first_end = "alice" if first["setting"] == alice % 64 and first["tick"] == da else "bob"
        if da == db:
            first_end = "same_tick"
    return (
        result["alice"],
        result["bob"],
        result["closed"],
        result["numbers"],
        result["questions"],
        first_end,
        tuple(entry["tick"] for entry in result["log"]),
    )


def ordering(pool, da: int, db: int) -> dict:
    correlations = {}
    first_counts = {}
    closed = True
    numbers_ok = True
    per_pair = {}
    for setting, (left, right) in enumerate(PAIRS):
        alice, bob = SETTINGS[left], SETTINGS[right]
        jobs = [(seed_for(setting, i), alice, bob, da, db) for i in range(PAIRS_PER_CORRELATION)]
        rows = list(pool.map(order_job, jobs, chunksize=32))
        sample = [(a, b) for a, b, *_ in rows if a is not None and b is not None]
        per_pair[f"{left},{right}"] = [(a, b) for a, b, *_ in rows]
        closed = closed and all(r[2] for r in rows)
        numbers_ok = numbers_ok and all(r[3] == 1 and r[4] == 2 for r in rows)
        for r in rows:
            first_counts[r[5]] = first_counts.get(r[5], 0) + 1
        stats = correlation_stats(sample)
        stats["missing"] = PAIRS_PER_CORRELATION - len(sample)
        stats["expected_E"] = round(expected_e(alice, bob), 5)
        stats["ask_ticks"] = sorted({r[6] for r in rows})
        correlations[f"{left},{right}"] = stats
    return {
        "dist_alice": da,
        "dist_bob": db,
        "correlations": correlations,
        **chsh_from(correlations),
        "first_asker_counts": first_counts,
        "closed": closed,
        "one_number_two_questions_every_pair": numbers_ok,
        "_per_pair": per_pair,
    }


def compare_orderings(first: dict, second: dict) -> dict:
    rows = {}
    for key in first["correlations"]:
        f, s = first["correlations"][key], second["correlations"][key]
        rows[key] = {}
        for stat, sigma in (
            ("E", "sigma_E"),
            ("alice_plus_rate", "sigma_alice_rate"),
            ("bob_plus_rate", "sigma_bob_rate"),
        ):
            d = f[stat] - s[stat]
            combined = (f[sigma] ** 2 + s[sigma] ** 2) ** 0.5
            rows[key][stat] = {
                "difference": round(d, 5),
                "combined_sigma": round(combined, 5),
                "z": round(d / combined, 3) if combined else None,
                "within_3_sigma": abs(d) <= 3 * combined,
            }
        same_alice = sum(
            a == c
            for (a, _), (c, _) in zip(first["_per_pair"][key], second["_per_pair"][key], strict=False)
        )
        same_product = sum(
            a * b == c * d
            for (a, b), (c, d) in zip(first["_per_pair"][key], second["_per_pair"][key], strict=False)
        )
        rows[key]["pairwise_same_alice_outcome"] = same_alice
        rows[key]["pairwise_same_product"] = same_product
    ds = first["S"] - second["S"]
    comb = (first["sigma_S"] ** 2 + second["sigma_S"] ** 2) ** 0.5
    rows["S"] = {
        "difference": round(ds, 5),
        "combined_sigma": round(comb, 5),
        "z": round(ds / comb, 3),
        "within_3_sigma": abs(ds) <= 3 * comb,
    }
    return rows


# --- (b) delayed choice --------------------------------------------------------------


def set_setting(logged: Logged, position: tuple, setting: int) -> None:
    """FLAGGED: replace the frozen detector record in private engine state between steps."""
    node = logged.world._nodes[position]
    records = list(node.records)
    for slot, record in enumerate(records):
        if record is None:
            continue
        values = list(record.values)
        values[SETTING_FIELD_INDEX] = pack((setting % 64,))
        records[slot] = dataclasses.replace(record, values=tuple(values))
    node.records = tuple(records)


def delayed_job(job: tuple) -> tuple:
    seed, alice, bob, change_after = job
    initial_alice, initial_bob = 0, 8
    raw = bonded_world(0, initial_alice, initial_bob, seed)
    center, d = raw["shape"][0] // 2, 3
    logged = Logged(raw)
    for _ in range(raw["ticks"]):
        if logged.world.tick == change_after:
            set_setting(logged, (center - d, 1, 1), alice)
            set_setting(logged, (center + d, 1, 1), bob)
        logged.world.step()
    result = logged.outcomes()
    settings_asked = tuple((e["tick"], e["setting"]) for e in result["log"])
    return result["alice"], result["bob"], result["closed"], result["numbers"], settings_asked


def final_job(job: tuple) -> tuple:
    seed, alice, bob = job
    result = run_world(bonded_world(0, alice, bob, seed))
    return result["alice"], result["bob"], result["closed"]


def delayed(pool) -> dict:
    report = {"variants": {}}
    finals = {}
    for setting, (left, right) in enumerate(PAIRS):
        alice, bob = SETTINGS[left], SETTINGS[right]
        finals[f"{left},{right}"] = list(
            pool.map(
                final_job,
                [(seed_for(setting, i), alice, bob) for i in range(PAIRS_PER_CORRELATION)],
                chunksize=32,
            )
        )
    initial_world = {}
    for setting, (left, right) in enumerate(PAIRS):
        initial_world[f"{left},{right}"] = list(
            pool.map(
                final_job,
                [(seed_for(setting, i), 0, 8) for i in range(PAIRS_PER_CORRELATION)],
                chunksize=32,
            )
        )
    # (i) legal two-world comparison: same seed, settings a vs a2 at fixed b. The CHSH sample
    # uses different seeds per setting pair; the legal comparison at identical seed is the
    # per-seed table below.
    same_seed = {
        "pairs": 0,
        "alice_moves_with_own_setting": 0,
        "bob_moves_with_alice_setting": 0,
        "alice_moves_with_bob_setting": 0,
    }
    table_jobs = [
        (SEED_BASE + 5 * 2**16 + i, SETTINGS[left], SETTINGS[right])
        for i in range(256)
        for left, right in PAIRS
    ]
    rows = list(pool.map(final_job, table_jobs, chunksize=32))
    for i in range(256):
        cells = {PAIRS[k]: rows[i * 4 + k] for k in range(4)}
        same_seed["pairs"] += 1
        same_seed["alice_moves_with_own_setting"] += cells[("a", "b")][0] != cells[("a2", "b")][0]
        same_seed["alice_moves_with_bob_setting"] += cells[("a", "b")][0] != cells[("a", "b2")][0]
        same_seed["bob_moves_with_alice_setting"] += cells[("a", "b2")][1] != cells[("a2", "b2")][1]
    report["legal_same_seed_setting_table_256"] = same_seed
    for change_after in (2, 3, 4):
        correlations = {}
        identical_to_final = 0
        identical_to_initial = 0
        closed = True
        asked = set()
        for setting, (left, right) in enumerate(PAIRS):
            alice, bob = SETTINGS[left], SETTINGS[right]
            jobs = [
                (seed_for(setting, i), alice, bob, change_after) for i in range(PAIRS_PER_CORRELATION)
            ]
            rows = list(pool.map(delayed_job, jobs, chunksize=32))
            key = f"{left},{right}"
            identical_to_final += sum(
                (r[0], r[1]) == (f[0], f[1]) for r, f in zip(rows, finals[key], strict=False)
            )
            identical_to_initial += sum(
                (r[0], r[1]) == (f[0], f[1]) for r, f in zip(rows, initial_world[key], strict=False)
            )
            closed = closed and all(r[2] and r[3] == 1 for r in rows)
            asked |= {r[4] for r in rows}
            stats = correlation_stats(
                [(r[0], r[1]) for r in rows if r[0] is not None and r[1] is not None]
            )
            stats["expected_E"] = round(expected_e(alice, bob), 5)
            correlations[key] = stats
        total = 4 * PAIRS_PER_CORRELATION
        report["variants"][f"settings_written_after_tick_{change_after}"] = {
            "flagged": "private engine state replaced between steps (world._nodes[...].records); src/ untouched",
            "ask_happens_in_step_from_tick": 3,
            "correlations": correlations,
            **chsh_from(correlations),
            "identical_to_world_built_with_final_settings": f"{identical_to_final} of {total}",
            "identical_to_world_built_with_initial_settings": f"{identical_to_initial} of {total}",
            "settings_seen_by_registry": sorted(asked)[:8],
            "closed_and_one_number": closed,
        }
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=4)
    output_argument(parser)
    args = parser.parse_args()
    out_dir = args.output / "e2_order_delayed"
    multiprocessing.set_start_method("fork")
    started = time.perf_counter()
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        alice_first = ordering(pool, 3, 5)
        bob_first = ordering(pool, 5, 3)
        symmetric = ordering(pool, 3, 3)
        comparison = compare_orderings(alice_first, bob_first)
        comparison_sym = compare_orderings(alice_first, symmetric)
        part_b = delayed(pool)
    for run in (alice_first, bob_first, symmetric):
        run.pop("_per_pair")
    report = {
        **stamp(),
        "pairs_per_correlation": PAIRS_PER_CORRELATION,
        "a": {
            "alice_first": alice_first,
            "bob_first": bob_first,
            "symmetric": symmetric,
            "alice_first_vs_bob_first": comparison,
            "alice_first_vs_symmetric": comparison_sym,
            "pass": alice_first["within_3_sigma"]
            and bob_first["within_3_sigma"]
            and all(v["within_3_sigma"] for k, v in comparison.items() if k == "S")
            and all(
                cell["within_3_sigma"]
                for k, v in comparison.items()
                if k != "S"
                for cell in v.values()
                if isinstance(cell, dict)
            ),
        },
        "b": {
            "api_gap": "field_rules and spatial_interactions are rejected for ray transport (initialization.py: 'ray transport does not support field rules or spatial interactions'); DisturbanceRecord is a frozen dataclass; no public method rewrites a record value between steps.",
            **part_b,
        },
        "runtime_seconds": round(time.perf_counter() - started, 1),
    }
    dump(out_dir / "results.json", report)
    for name in ("alice_first", "bob_first", "symmetric"):
        r = report["a"][name]
        print(
            name,
            "S",
            r["S"],
            "+-",
            r["sigma_S"],
            "z",
            r["z"],
            "first askers",
            r["first_asker_counts"],
            "closed",
            r["closed"],
        )
    print("a pass", report["a"]["pass"])
    for name, v in part_b["variants"].items():
        print(
            name,
            "S",
            v["S"],
            "+-",
            v["sigma_S"],
            "final-identical",
            v["identical_to_world_built_with_final_settings"],
            "initial-identical",
            v["identical_to_world_built_with_initial_settings"],
        )
    print("runtime", report["runtime_seconds"])


if __name__ == "__main__":
    main()
