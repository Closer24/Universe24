"""E4: birth-code uniqueness and one number per pair.

(a) Two bonded pairs born at the same Node and tick (13x9x3 lattice; pair 1 along x,
    pair 2 along y from the same source Node) against a control where pair 2 is born
    at the neighbouring Node (7,4,1). Cross-pair correlations and numbers consumed.
(b) Replay: Bob's plus detector at 5 links; a second bonded detector with Alice's
    setting one link past her plus detector meets a ray she left at tick 4, before
    Bob asks at tick 5. Variant with a different setting (16). Plus the registry API
    asked twice with identical arguments.
(c) A missing end: Bob's detectors removed, his ray escapes the open boundary.

Run:  PYTHONPATH=src python examples/research/bell-postulate-22/e4_birthcode.py --workers 4 --output DIR
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
    PHASE_STEPS,
    TICKET_MODULUS,
    BondRegistry,
    bonded_world,
    correlation_stats,
    dump,
    expected_e,
    origin_bond,
    output_argument,
    run_world,
    se_rate,
    stamp,
)

N = 1024
SEED_BASE = 9 * 2**20


def pair_stats(rows: list[tuple[int, int]], expected: float) -> dict:
    stats = correlation_stats([(a, b) for a, b in rows if a is not None and b is not None])
    stats["expected_E"] = round(expected, 5)
    stats["z"] = round((stats["E"] - expected) / stats["sigma_E"], 3) if stats["sigma_E"] else None
    stats["within_3_sigma"] = (
        stats["sigma_E"] is not None and abs(stats["E"] - expected) <= 3 * stats["sigma_E"]
    )
    return stats


# --- (a) ------------------------------------------------------------------------------


def two_pair_job(job: tuple) -> tuple:
    seed, source2 = job
    raw = bonded_world(
        0,
        0,
        8,
        seed,
        width=13,
        depth=9,
        second_pair={"source": source2, "hidden": 5, "alice": 0, "bob": 8},
    )
    r = run_world(raw)
    numbers = sorted({e["bond"] for e in r["log"]})
    values = sorted({BondRegistry(seed, PHASE_STEPS).number(b) for b in numbers})
    return (
        r["alice"],
        r["bob"],
        r["alice2"],
        r["bob2"],
        r["closed"],
        r["numbers"],
        r["questions"],
        tuple((e["tick"], e["bond"], e["setting"], e["outcome"], e["drew_number"]) for e in r["log"]),
        len(numbers),
        len(values),
    )


def part_a(pool) -> dict:
    out = {}
    for name, source2 in (
        ("collision_same_node_same_tick", (6, 4, 1)),
        ("control_neighbour_node", (7, 4, 1)),
    ):
        rows = list(pool.map(two_pair_job, [(SEED_BASE + i, source2) for i in range(N)], chunksize=32))
        a1 = [r[0] for r in rows]
        b1 = [r[1] for r in rows]
        a2 = [r[2] for r in rows]
        b2 = [r[3] for r in rows]
        out[name] = {
            "source_pair_2": source2,
            "bond_codes": {
                "pair_1": origin_bond((6, 4, 1), (13, 9, 3), 0),
                "pair_2": origin_bond(source2, (13, 9, 3), 0),
            },
            "E(A1,B1)": pair_stats(list(zip(a1, b1, strict=False)), expected_e(0, 8)),
            "E(A2,B2)": pair_stats(list(zip(a2, b2, strict=False)), expected_e(0, 8)),
            "E(A1,A2)": pair_stats(list(zip(a1, a2, strict=False)), 0.0),
            "E(B1,B2)": pair_stats(list(zip(b1, b2, strict=False)), 0.0),
            "E(A1,B2)": pair_stats(list(zip(a1, b2, strict=False)), 0.0),
            "E(A2,B1)": pair_stats(list(zip(a2, b1, strict=False)), 0.0),
            "numbers_consumed_histogram": {
                str(k): sum(r[5] == k for r in rows) for k in sorted({r[5] for r in rows})
            },
            "questions_histogram": {
                str(k): sum(r[6] == k for r in rows) for k in sorted({r[6] for r in rows})
            },
            "distinct_bonds_asked": {
                str(k): sum(r[8] == k for r in rows) for k in sorted({r[8] for r in rows})
            },
            "distinct_number_values": {
                str(k): sum(r[9] == k for r in rows) for k in sorted({r[9] for r in rows})
            },
            "closed": all(r[4] for r in rows),
            "example_log": rows[0][7],
        }
        out[name]["theory_pass"] = (
            out[name]["E(A1,B1)"]["within_3_sigma"]
            and out[name]["E(A2,B2)"]["within_3_sigma"]
            and all(
                out[name][k]["within_3_sigma"] for k in ("E(A1,A2)", "E(B1,B2)", "E(A1,B2)", "E(A2,B1)")
            )
            and all(r[5] == 2 and r[9] == 2 for r in rows)
        )
    return out


# --- (b) ------------------------------------------------------------------------------


def replay_job(job: tuple) -> tuple:
    seed, replay_setting = job
    r = run_world(bonded_world(0, 0, 8, seed, dist_bob=5, replay_setting=replay_setting))
    log = [(e["tick"], e["setting"], e["salt"], e["outcome"], e["drew_number"]) for e in r["log"]]
    return (
        r["alice"],
        r["bob"],
        r["closed"],
        r["numbers"],
        r["questions"],
        r["released"],
        r["open"],
        tuple(log),
    )


def part_b(pool) -> dict:
    out = {}
    for name, setting in (("same_end_same_setting", 0), ("second_detector_other_setting_16", 16)):
        rows = list(
            pool.map(replay_job, [(SEED_BASE + 2**16 + i, setting) for i in range(N)], chunksize=32)
        )
        replayed = [r for r in rows if len(r[7]) == 3]
        cached_same = sum(r[7][0][3] == r[7][1][3] and r[7][1][4] == 0 for r in replayed)
        first_left = sum(r[7][0][3] < 0 for r in rows)
        alice_first_vs_bob = [(r[7][0][3], r[1]) for r in rows]
        out[name] = {
            "replay_setting": setting,
            "worlds": len(rows),
            "alice_first_answer_minus": first_left,
            "worlds_with_three_questions": len(replayed),
            "replay_answer_equals_first_and_drew_nothing": cached_same,
            "numbers_histogram": {
                str(k): sum(r[3] == k for r in rows) for k in sorted({r[3] for r in rows})
            },
            "questions_histogram": {
                str(k): sum(r[4] == k for r in rows) for k in sorted({r[4] for r in rows})
            },
            "released_histogram": {
                str(k): sum(r[5] == k for r in rows) for k in sorted({r[5] for r in rows})
            },
            "open_at_end_histogram": {
                str(k): sum(r[6] == k for r in rows) for k in sorted({r[6] for r in rows})
            },
            "E(alice_first_answer, bob)": pair_stats(alice_first_vs_bob, expected_e(0, 8)),
            "closed": all(r[2] for r in rows),
            "example_logs": [r[7] for r in rows[:3]],
        }
        if setting == 0:
            out[name]["pass"] = (
                all(r[3] == 1 for r in rows)
                and cached_same == len(replayed)
                and len(replayed) == first_left
            )
    registry = BondRegistry(5, PHASE_STEPS)
    first = registry.draw(777, 0, 1)
    again = [registry.draw(777, 0, 1) for _ in range(10)]
    out["registry_api_repeat"] = {
        "first": first,
        "repeats": again,
        "numbers_after_11_questions": registry.numbers,
        "questions": registry.questions,
        "pass": registry.numbers == 1 and all(x == first for x in again),
    }
    return out


# --- (c) ------------------------------------------------------------------------------


def missing_job(job: tuple) -> tuple:
    seed, bob_setting, bob_present = job
    r = run_world(bonded_world(0, 0, bob_setting, seed, bob_present=bob_present))
    return r["alice"], r["bob"], r["escaped"], r["closed"], r["numbers"], r["questions"], r["open"]


def part_c(pool) -> dict:
    seeds = [SEED_BASE + 2**17 + i for i in range(N)]
    absent_8 = list(pool.map(missing_job, [(s, 8, False) for s in seeds], chunksize=32))
    absent_24 = list(pool.map(missing_job, [(s, 24, False) for s in seeds], chunksize=32))
    full_8 = list(pool.map(missing_job, [(s, 8, True) for s in seeds], chunksize=32))
    rate = sum(r[0] > 0 for r in absent_8) / N
    return {
        "worlds": N,
        "alice_plus_rate_bob_absent": round(rate, 5),
        "sigma": round(se_rate(rate, N), 5),
        "z_from_half": round((rate - 0.5) / se_rate(rate, N), 3),
        "alice_identical_between_bob_setting_8_and_24": sum(
            a[0] == b[0] for a, b in zip(absent_8, absent_24, strict=False)
        ),
        "alice_identical_to_full_world_same_seed": sum(
            a[0] == f[0] for a, f in zip(absent_8, full_8, strict=False)
        ),
        "bob_outcome_none_every_world": all(r[1] is None for r in absent_8),
        "escaped_quanta_histogram": {
            str(k): sum(r[2] == k for r in absent_8) for k in sorted({r[2] for r in absent_8})
        },
        "numbers_histogram": {
            str(k): sum(r[4] == k for r in absent_8) for k in sorted({r[4] for r in absent_8})
        },
        "questions_histogram": {
            str(k): sum(r[5] == k for r in absent_8) for k in sorted({r[5] for r in absent_8})
        },
        "open_at_end_histogram": {
            str(k): sum(r[6] == k for r in absent_8) for k in sorted({r[6] for r in absent_8})
        },
        "closed": all(r[3] for r in absent_8 + absent_24),
        "full_world_alice_plus_rate": round(sum(r[0] > 0 for r in full_8) / N, 5),
        "pass": abs(rate - 0.5) <= 3 * se_rate(rate, N)
        and all(r[4] == 1 and r[6] == 1 and r[2] == 1 for r in absent_8)
        and sum(a[0] == b[0] for a, b in zip(absent_8, absent_24, strict=False)) == N
        and sum(a[0] == f[0] for a, f in zip(absent_8, full_8, strict=False)) == N,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=4)
    output_argument(parser)
    args = parser.parse_args()
    out_dir = args.output / "e4_birthcode"
    multiprocessing.set_start_method("fork")
    started = time.perf_counter()
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        a = part_a(pool)
        print(
            "a",
            {
                k: (
                    v["theory_pass"],
                    v["E(A1,B1)"]["E"],
                    v["E(A1,A2)"]["E"],
                    v["E(A1,B2)"]["E"],
                    v["numbers_consumed_histogram"],
                    v["distinct_number_values"],
                )
                for k, v in a.items()
            },
        )
        b = part_b(pool)
        print(
            "b",
            {k: v.get("pass", "n/a") for k, v in b.items()},
            {k: v.get("numbers_histogram") for k, v in b.items() if "numbers_histogram" in v},
        )
        c = part_c(pool)
        print(
            "c", c["pass"], c["alice_plus_rate_bob_absent"], c["alice_identical_to_full_world_same_seed"]
        )
    report = {
        **stamp(),
        "worlds_per_case": N,
        "modulus": TICKET_MODULUS,
        "birth_code_collision_analysis": (
            "origin_bond = (index * 1048573 + tick) mod 1073741789 + 1 with index the Node's row-major address. "
            "The modulus is prime and 1048573 is coprime to it, so two different Nodes collide only when their "
            "ticks differ by 1048573 x (index difference) modulo the modulus, i.e. at least 1,048,573 ticks apart "
            "for neighbouring addresses; unreachable in these runs. The only reachable collision is the same Node "
            "and the same tick, which is the case measured."
        ),
        "a": a,
        "b": b,
        "c": c,
        "runtime_seconds": round(time.perf_counter() - started, 1),
    }
    dump(out_dir / "results.json", report)
    print("runtime", report["runtime_seconds"])


if __name__ == "__main__":
    main()
