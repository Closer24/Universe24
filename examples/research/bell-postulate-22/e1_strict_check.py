"""E1 post-hoc strict cone check: a differing Node must lie inside the forward cone of an
end whose ANSWER differs between the two worlds (not merely any end that asked), and the
side whose answer did not change must show no difference at all.

Run:  PYTHONPATH=src python examples/research/bell-postulate-22/e1_strict_check.py --output DIR
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import output_argument  # noqa: E402


def manhattan(p, q) -> int:
    return sum(abs(a - b) for a, b in zip(p, q, strict=False))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    output_argument(parser)
    out_dir = parser.parse_args().output / "e1_lightcone"
    report = json.load(open(out_dir / "results.json"))
    strict_violations = []
    summary = {
        "cases": 0,
        "variants_checked": 0,
        "changed_ends": {"alice_only": 0, "bob_only": 0, "both": 0, "none": 0},
    }
    per_tick_radius = {}
    for case in report["cases"]:
        summary["cases"] += 1
        for name, variant in case["variants"].items():
            if name == "control_same_number":
                continue
            summary["variants_checked"] += 1
            changed = [
                b
                for b, v in zip(case["asks_base"], variant["asks_variant"], strict=True)
                if b["outcome"] != v["outcome"]
            ]
            key = {
                0: "none",
                1: "alice_only" if changed and changed[0]["position"][0] < 6 else "bob_only",
                2: "both",
            }[len(changed)]
            summary["changed_ends"][key] += 1
            for row in variant["diff_per_tick"]:
                t = row["tick"]
                for pos_key in row["positions"]:
                    position = tuple(json.loads(pos_key.replace("(", "[").replace(")", "]")))
                    inside = any(
                        a["tick"] < t and manhattan(position, a["position"]) <= t - a["tick"]
                        for a in changed
                    )
                    # the radius actually reached, per tick since the first changed ask
                    if changed:
                        reach = min(
                            manhattan(position, a["position"]) - (t - a["tick"]) for a in changed
                        )
                        per_tick_radius[reach] = per_tick_radius.get(reach, 0) + 1
                    if not inside:
                        strict_violations.append(
                            {
                                "geometry": case["geometry"],
                                "seed": case["seed"],
                                "variant": name,
                                "tick": t,
                                "position": position,
                            }
                        )
    result = {
        **summary,
        "strict_violations": strict_violations,
        "slack_histogram_(distance_minus_radius,_<=0_means_inside)": dict(
            sorted(per_tick_radius.items())
        ),
        "pass": not strict_violations,
    }
    json.dump(result, open(out_dir / "strict_check.json", "w"), indent=2)
    print(json.dumps(result, indent=2)[:2000])


if __name__ == "__main__":
    main()
