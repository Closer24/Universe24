"""E3 follow-up: does the salted chooser's agreement-half dependence (p = 0.002 at seed 11)
persist across registry seeds? Registry alone, 65,536 pairs per seed, 16 seeds each for
the salted chooser, the bond chooser and the Python control; the p-values of the
agreement-quartile and coin tests are listed, plus a pooled chi-square (sum of the
per-seed statistics, df summed) which is the sharp test of a persistent dependence.

Run:  PYTHONPATH=src python examples/research/bell-postulate-22/e3_salted_followup.py --output DIR
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import chi2_sf, dump, output_argument, stamp  # noqa: E402
from e3_free_choice import REGISTRY_PAIRS, analyse, registry_variant  # noqa: E402

SEEDS = [11, 12345] + [1000 + 977 * k for k in range(14)]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    output_argument(parser)
    out_dir = parser.parse_args().output / "e3_free_choice"
    report = {**stamp(), "pairs_per_seed": REGISTRY_PAIRS, "seeds": SEEDS, "variants": {}}
    for variant in ("salted", "bond", "control_python_random"):
        rows_out = []
        pooled = {"coin": [0.0, 0], "rest": [0.0, 0]}
        for seed in SEEDS:
            result = analyse(registry_variant(variant, seed, REGISTRY_PAIRS), REGISTRY_PAIRS)
            coin, rest = result["coin_half_vs_settings"], result["agreement_half_quartile_vs_settings"]
            pooled["coin"][0] += coin["chi2"]
            pooled["coin"][1] += coin["df"]
            pooled["rest"][0] += rest["chi2"]
            pooled["rest"][1] += rest["df"]
            rows_out.append(
                {
                    "seed": seed,
                    "S": result["S"],
                    "sigma_S": result["sigma_S"],
                    "z": result["z"],
                    "coin_p": round(coin["p"], 4),
                    "rest_p": round(rest["p"], 4),
                    "rest_chi2": rest["chi2"],
                }
            )
        summary = {
            "rows": rows_out,
            "seeds_with_rest_p_below_0_01": sum(r["rest_p"] <= 0.01 for r in rows_out),
            "seeds_with_coin_p_below_0_01": sum(r["coin_p"] <= 0.01 for r in rows_out),
            "pooled_coin": {
                "chi2": round(pooled["coin"][0], 3),
                "df": pooled["coin"][1],
                "p": chi2_sf(*pooled["coin"]),
            },
            "pooled_rest": {
                "chi2": round(pooled["rest"][0], 3),
                "df": pooled["rest"][1],
                "p": chi2_sf(*pooled["rest"]),
            },
            "S_mean": round(sum(r["S"] for r in rows_out) / len(rows_out), 5),
            "max_abs_z_S": max(abs(r["z"]) for r in rows_out),
        }
        report["variants"][variant] = summary
        print(variant, json.dumps({k: v for k, v in summary.items() if k != "rows"}))
        print("   rest p per seed:", [r["rest_p"] for r in rows_out])
    dump(out_dir / "salted_followup.json", report)


if __name__ == "__main__":
    main()
