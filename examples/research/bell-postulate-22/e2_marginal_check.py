"""E2 follow-up: is the second asker's marginal biased in the world's own sequence?

The lattice run at (a2, b) read a second-asker plus rate of 0.5498 over 1,024
consecutive registry seeds (3.2 sigma from 0.5). The registry alone reproduces the
lattice pair by pair (E2, README), so the question is answered by the registry:
first- and second-asker plus rates over a million consecutive seeds per setting
pair, and the spread of block rates over blocks of 1,024 consecutive seeds against
the binomial 0.0156.

Run:  PYTHONPATH=src python examples/research/bell-postulate-22/e2_marginal_check.py --output DIR
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    PAIRS,
    PHASE_STEPS,
    SETTINGS,
    BondRegistry,
    dump,
    origin_bond,
    output_argument,
    stamp,
)

BOND = origin_bond((6, 1, 1), (13, 3, 3), 0)
SEED_BASE = 3 * 2**20  # the E2 seed family
BLOCK = 1024
BLOCKS = 256


def rates(
    first_setting: int, second_setting: int, seeds: range
) -> tuple[float, float, float, list[float]]:
    first_plus = second_plus = agree = 0
    block_rates = []
    block_plus = 0
    for i, seed in enumerate(seeds):
        registry = BondRegistry(seed, PHASE_STEPS)
        a = registry.draw(BOND, first_setting, 1)
        b = registry.draw(BOND, second_setting, 2)
        first_plus += a > 0
        second_plus += b > 0
        block_plus += b > 0
        agree += a == b
        if (i + 1) % BLOCK == 0:
            block_rates.append(block_plus / BLOCK)
            block_plus = 0
    n = len(seeds)
    return first_plus / n, second_plus / n, agree / n, block_rates


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    output_argument(parser)
    out_dir = parser.parse_args().output / "e2_order_delayed"
    report = {**stamp(), "bond": BOND, "rows": {}}
    n = BLOCK * BLOCKS
    for setting, (left, right) in enumerate(PAIRS):
        a, b = SETTINGS[left], SETTINGS[right]
        # the very seeds E2 used for this setting pair, then a long consecutive run
        e2_seeds = range(SEED_BASE + setting * BLOCK, SEED_BASE + (setting + 1) * BLOCK)
        f1, s1, g1, _ = rates(a, b, e2_seeds)
        f2, s2, g2, blocks = rates(a, b, range(SEED_BASE, SEED_BASE + n))
        mean = sum(blocks) / len(blocks)
        spread = math.sqrt(sum((x - mean) ** 2 for x in blocks) / (len(blocks) - 1))
        sigma_block = math.sqrt(0.25 / BLOCK)
        report["rows"][f"{left},{right}"] = {
            "E2_block": {
                "seeds": [e2_seeds.start, e2_seeds.stop - 1],
                "first_asker_plus_rate": f1,
                "second_asker_plus_rate": s1,
                "agreement": g1,
                "z_second_from_half": round((s1 - 0.5) / sigma_block, 3),
            },
            "long_run": {
                "seeds": n,
                "first_asker_plus_rate": round(f2, 5),
                "second_asker_plus_rate": round(s2, 5),
                "sigma": round(math.sqrt(0.25 / n), 5),
                "z_first": round((f2 - 0.5) / math.sqrt(0.25 / n), 3),
                "z_second": round((s2 - 0.5) / math.sqrt(0.25 / n), 3),
                "agreement": round(g2, 5),
            },
            "blocks_of_1024": {
                "count": len(blocks),
                "spread_of_second_rate": round(spread, 5),
                "binomial_sigma": round(sigma_block, 5),
                "max_abs_z": round(max(abs(x - 0.5) / sigma_block for x in blocks), 3),
                "blocks_beyond_3_sigma": sum(abs(x - 0.5) > 3 * sigma_block for x in blocks),
            },
        }
        print(f"{left},{right}", json.dumps(report["rows"][f"{left},{right}"]))
    dump(out_dir / "marginal_check.json", report)


if __name__ == "__main__":
    main()
