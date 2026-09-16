"""Compile the four experiments' results into one summary.json for the reviewer.

Run:  PYTHONPATH=src python examples/research/bell-postulate-22/summarize.py --output DIR
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import dump, output_argument, stamp  # noqa: E402


def load(out: Path, name: str, file: str = "results.json") -> dict:
    return json.load(open(out / name / file))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    output_argument(parser)
    out = parser.parse_args().output
    e1, e1s = load(out, "e1_lightcone"), load(out, "e1_lightcone", "strict_check.json")
    e2, e2m = load(out, "e2_order_delayed"), load(out, "e2_order_delayed", "marginal_check.json")
    e3 = load(out, "e3_free_choice")
    e4 = load(out, "e4_birthcode")
    summary = {
        **stamp(),
        "E1": {
            "cases": len(e1["cases"]),
            "variants_per_case": ["control_same_number", "coin_flip", "agreement_flip"],
            "all_pass": e1["all_pass"],
            "strict_pass": e1s["pass"],
            "changed_ends": e1s["changed_ends"],
            "first_differing_tick_histogram": {},
            "runtime_seconds": e1["runtime_seconds"],
        },
        "E2": {
            "a": {
                name: {
                    "S": e2["a"][name]["S"],
                    "sigma_S": e2["a"][name]["sigma_S"],
                    "z": e2["a"][name]["z"],
                    "first_askers": e2["a"][name]["first_asker_counts"],
                }
                for name in ("alice_first", "bob_first", "symmetric")
            },
            "a_pairwise_same_product": {
                k: v["pairwise_same_product"]
                for k, v in e2["a"]["alice_first_vs_bob_first"].items()
                if k != "S"
            },
            "a_rate_comparisons_beyond_3_sigma": [
                (k, stat, cell["z"])
                for k, v in e2["a"]["alice_first_vs_bob_first"].items()
                if k != "S"
                for stat, cell in v.items()
                if isinstance(cell, dict) and not cell["within_3_sigma"]
            ],
            "a_prefixed_criterion_pass": e2["a"]["pass"],
            "a_registry_long_run_second_asker_rate": {
                k: v["long_run"]["second_asker_plus_rate"] for k, v in e2m["rows"].items()
            },
            "b_api_gap": e2["b"]["api_gap"],
            "b_variants": {
                name: {
                    "S": v["S"],
                    "sigma_S": v["sigma_S"],
                    "final_identical": v["identical_to_world_built_with_final_settings"],
                    "initial_identical": v["identical_to_world_built_with_initial_settings"],
                }
                for name, v in e2["b"]["variants"].items()
            },
            "b_legal_same_seed_table": e2["b"]["legal_same_seed_setting_table_256"],
            "runtime_seconds": e2["runtime_seconds"],
        },
        "E3": {
            "lattice": {
                name: {
                    "S": v["S"],
                    "sigma_S": v["sigma_S"],
                    "z": v["z"],
                    "coin_p": v["coin_half_vs_settings"]["p"],
                    "rest_p": v["agreement_half_quartile_vs_settings"]["p"],
                    "pass": v["pass"],
                }
                for name, v in e3["lattice"].items()
            },
            "registry": {
                name: {
                    "S": v["S"],
                    "sigma_S": v["sigma_S"],
                    "z": v["z"],
                    "coin_p": v["coin_half_vs_settings"]["p"],
                    "rest_p": v["agreement_half_quartile_vs_settings"]["p"],
                    "pass": v["pass"],
                }
                for name, v in e3["registry"].items()
            },
            "all_pass": e3["all_pass"],
            "runtime_seconds": e3["runtime_seconds"],
        },
        "E4": {
            "a": {
                name: {
                    "theory_pass": v["theory_pass"],
                    "E(A1,B1)": v["E(A1,B1)"]["E"],
                    "E(A1,A2)": v["E(A1,A2)"]["E"],
                    "E(A1,B2)": v["E(A1,B2)"]["E"],
                    "numbers": v["numbers_consumed_histogram"],
                    "distinct_values": v["distinct_number_values"],
                }
                for name, v in e4["a"].items()
            },
            "b": {
                name: {
                    k: v[k]
                    for k in v
                    if k
                    in (
                        "pass",
                        "numbers_histogram",
                        "replay_answer_equals_first_and_drew_nothing",
                        "worlds_with_three_questions",
                    )
                }
                for name, v in e4["b"].items()
            },
            "c": {
                k: e4["c"][k]
                for k in (
                    "pass",
                    "alice_plus_rate_bob_absent",
                    "sigma",
                    "alice_identical_to_full_world_same_seed",
                    "numbers_histogram",
                    "open_at_end_histogram",
                )
            },
            "runtime_seconds": e4["runtime_seconds"],
        },
    }
    hist = {}
    for case in e1["cases"]:
        for name, v in case["variants"].items():
            key = f"{name}:{v['first_differing_tick']}"
            hist[key] = hist.get(key, 0) + 1
    summary["E1"]["first_differing_tick_histogram"] = hist
    dump(out / "summary.json", summary)
    print(json.dumps(summary, indent=1)[:6000])


if __name__ == "__main__":
    main()
