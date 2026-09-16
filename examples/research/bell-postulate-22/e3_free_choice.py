"""E3: free choice from inside the world (measurement independence).

Each pair's settings are chosen by a ticket from the world's own generator family
(next_ticket / ticket_draw, the polynomial congruence of core/spatial_state.py),
seeded from the same seed family as the registry:
  salted : bit = ticket_draw(next_ticket(seed, k)) < M/2, k = 0 for Alice, 1 for Bob
           (a capture_salt-like salting of the registry seed)
  bond   : the registry's own two-step number with salts bond+1 and bond+2
           (adjacent birth codes)
  state  : the raw affine state next_ticket(seed, k) without the square, parity bit
Control: random.Random(seed ^ 0xABCDEF).
Lattice: 4096 pairs per variant. Registry alone: 65536 pairs per variant with one
seed and consecutive birth codes (bond = 1..N), settings derived from (seed, bond).

Run:  PYTHONPATH=src python examples/research/bell-postulate-22/e3_free_choice.py --workers 4 --output DIR
"""

from __future__ import annotations

import argparse
import json
import multiprocessing
import random
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    PAIRS,
    PHASE_STEPS,
    PROBE,
    SETTINGS,
    TICKET_MODULUS,
    BondRegistry,
    bonded_world,
    chi2_independence,
    chsh_from,
    correlation_stats,
    dump,
    expected_e,
    mutual_information_bits,
    next_ticket,
    number_halves,
    origin_bond,
    output_argument,
    run_world,
    stamp,
    ticket_draw,
)

LATTICE_PAIRS = 4096
REGISTRY_PAIRS = 65536
SEED_BASE = 7 * 2**20
BOND = origin_bond((PROBE.CENTER, 1, 1), (PROBE.WIDTH, 3, 3), 0)
VARIANTS = ("control_python_random", "salted", "bond", "state", "state_hi", "state_hi_far")


def choose(variant: str, seed: int, bond: int) -> tuple[str, str]:
    """The setting names (a or a2, b or b2) for one pair."""
    if variant == "control_python_random":
        g = random.Random(seed ^ 0xABCDEF)
        return ("a", "a2")[g.randrange(2)], ("b", "b2")[g.randrange(2)]
    if variant == "salted":
        bits = [ticket_draw(next_ticket(seed, k)) * 2 < TICKET_MODULUS for k in (0, 1)]
    elif variant == "bond":
        bits = []
        for salt in (bond + 1, bond + 2):
            state = ticket_draw(next_ticket(seed, salt % TICKET_MODULUS))
            bits.append(ticket_draw(next_ticket(state, salt % TICKET_MODULUS)) * 2 < TICKET_MODULUS)
    elif variant == "state":
        # Degenerate by construction: the affine states for salts 0 and 1 are consecutive
        # integers (barring a modulo wrap), so the two parities are always opposite.
        bits = [next_ticket(seed, k) % 2 == 0 for k in (0, 1)]
    elif variant == "state_hi":
        # The high bit of the raw affine state, no square: salts 0 and 1 again, but the
        # bit is a threshold on the state, which differs only at one seed in 2^29.
        bits = [next_ticket(seed, k) * 2 < TICKET_MODULUS for k in (0, 1)]
    elif variant == "state_hi_far":
        # High bits of raw affine states with salts far apart (0 and M // 3).
        bits = [next_ticket(seed, k) * 2 < TICKET_MODULUS for k in (0, TICKET_MODULUS // 3)]
    else:
        raise ValueError(variant)
    return ("a", "a2")[bits[0]], ("b", "b2")[bits[1]]


def lattice_job(job: tuple) -> tuple:
    variant, index = job
    seed = SEED_BASE + index
    left, right = choose(variant, seed, BOND)
    result = run_world(bonded_world(0, SETTINGS[left], SETTINGS[right], seed))
    number = BondRegistry(seed, PHASE_STEPS).number(BOND)
    return left, right, result["alice"], result["bob"], result["closed"], result["numbers"], number


def analyse(rows: list[tuple], pairs_expected: int) -> dict:
    """CHSH with errors, marginals, and number-half vs setting dependence tests."""
    correlations = {}
    for left, right in PAIRS:
        sample = [
            (a, b)
            for chosen_left, chosen_right, a, b, *_ in rows
            if (chosen_left, chosen_right) == (left, right) and a is not None and b is not None
        ]
        stats = correlation_stats(sample)
        stats["expected_E"] = round(expected_e(SETTINGS[left], SETTINGS[right]), 5)
        correlations[f"{left},{right}"] = stats
    coin_rows, rest_rows, outcome_rows = [], [], []
    for left, right, a, _b, *_rest, number in rows:
        coin, rest = number_halves(number)
        bucket = rest * 4 // TICKET_MODULUS
        coin_rows.append((coin, f"{left},{right}"))
        rest_rows.append((bucket, f"{left},{right}"))
        outcome_rows.append((a, f"{left},{right}"))
    setting_counts = {}
    for left, right, *_ in rows:
        setting_counts[f"{left},{right}"] = setting_counts.get(f"{left},{right}", 0) + 1
    coin_test = chi2_independence(coin_rows)
    rest_test = chi2_independence(rest_rows)
    alice_test = chi2_independence(outcome_rows)
    alice_by_bob = chi2_independence([(a, right) for _left, right, a, *_ in rows])
    bob_by_alice = chi2_independence([(b, left) for left, _right, _a, b, *_ in rows])
    return {
        "pairs": len(rows),
        "setting_counts": setting_counts,
        "correlations": correlations,
        **chsh_from(correlations),
        "coin_half_vs_settings": {
            **coin_test,
            "mutual_information_bits": round(mutual_information_bits(coin_rows), 6),
        },
        "agreement_half_quartile_vs_settings": {
            **rest_test,
            "mutual_information_bits": round(mutual_information_bits(rest_rows), 6),
        },
        "alice_outcome_vs_settings": alice_test,
        "alice_outcome_vs_bob_setting": alice_by_bob,
        "bob_outcome_vs_alice_setting": bob_by_alice,
        "dependence_significant_p_0_01": min(coin_test["p"], rest_test["p"]) <= 0.01,
    }


def registry_variant(variant: str, seed: int, pairs: int) -> list[tuple]:
    registry = BondRegistry(seed, PHASE_STEPS)
    rows = []
    for bond in range(1, pairs + 1):
        # One registry seed for the whole run; the chooser's seed-family element for
        # pair `bond` is seed + bond (consecutive, as the lattice family is), except the
        # `bond` variant, which is the registry's own number generator at other bonds.
        pair_seed = seed if variant == "bond" else (seed + bond) % TICKET_MODULUS
        left, right = choose(variant, pair_seed, bond)
        a = registry.draw(bond, SETTINGS[left], 1)
        b = registry.draw(bond, SETTINGS[right], 2)
        rows.append((left, right, a, b, True, 1, registry.number(bond)))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument(
        "--skip-lattice", action="store_true", help="reuse the lattice block of an existing results.json"
    )
    output_argument(parser)
    args = parser.parse_args()
    out_dir = args.output / "e3_free_choice"
    multiprocessing.set_start_method("fork")
    started = time.perf_counter()
    report = {
        **stamp(),
        "lattice_pairs": LATTICE_PAIRS,
        "registry_pairs": REGISTRY_PAIRS,
        "lattice": {},
        "registry": {},
    }
    if args.skip_lattice:
        previous = json.load(open(out_dir / "results.json"))
        report["lattice"] = previous["lattice"]
        report["lattice_runtime_seconds_previous_run"] = previous["runtime_seconds"]
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for variant in () if args.skip_lattice else VARIANTS:
            rows = list(
                pool.map(lattice_job, [(variant, i) for i in range(LATTICE_PAIRS)], chunksize=32)
            )
            result = analyse(rows, LATTICE_PAIRS)
            result["closed"] = all(r[4] for r in rows)
            result["one_number_per_pair"] = all(r[5] == 1 for r in rows)
            result["pass"] = result["within_3_sigma"] and not result["dependence_significant_p_0_01"]
            report["lattice"][variant] = result
            print(
                "lattice",
                variant,
                "S",
                result["S"],
                "+-",
                result["sigma_S"],
                "z",
                result["z"],
                "coin p",
                round(result["coin_half_vs_settings"]["p"], 4),
                "rest p",
                round(result["agreement_half_quartile_vs_settings"]["p"], 4),
                "pass",
                result["pass"],
            )
    for variant in VARIANTS:
        # One seed, consecutive birth codes: the world's own sequence as it would run.
        for seed in (11, 12345):
            rows = registry_variant(variant, seed, REGISTRY_PAIRS)
            result = analyse(rows, REGISTRY_PAIRS)
            result["pass"] = result["within_3_sigma"] and not result["dependence_significant_p_0_01"]
            report["registry"][f"{variant}_seed_{seed}"] = result
            print(
                "registry",
                variant,
                "seed",
                seed,
                "S",
                result["S"],
                "+-",
                result["sigma_S"],
                "z",
                result["z"],
                "coin p",
                round(result["coin_half_vs_settings"]["p"], 4),
                "rest p",
                round(result["agreement_half_quartile_vs_settings"]["p"], 4),
                "pass",
                result["pass"],
            )
    report["all_pass"] = all(v["pass"] for v in report["lattice"].values()) and all(
        v["pass"] for v in report["registry"].values()
    )
    report["runtime_seconds"] = round(time.perf_counter() - started, 1)
    dump(out_dir / "results.json", report)
    print("all_pass", report["all_pass"], "runtime", report["runtime_seconds"])


if __name__ == "__main__":
    main()
