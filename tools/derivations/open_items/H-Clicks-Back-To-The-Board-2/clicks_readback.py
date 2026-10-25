"""Hand N2: a read-back of the 300-interval hole-seed clicks log (out/hole300.clicks.jsonl) and the entropy table (out/hole_seed_entropy_table.json): the births' intervals with the draws' rooms at those intervals and the bits those draws wrote (an upper bound on the births' own bits, several draws sharing an interval), the first light-lift birth, the credits whose beat is not None (kind, family, beat, proper), the realised points of the credits, the refusals per cause per 50 intervals, and the first and last click intervals. Integers only.

Run: PYTHONPATH=<worktree>/src TMPDIR=/dev/shm/tmp /home/user/Universe24/venv314/bin/python tools/derivations/open_items/H-Clicks-Back-To-The-Board-2/clicks_readback.py
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

OUT = Path(__file__).with_name("out")


def main() -> None:
    lines = [json.loads(line) for line in (OUT / "hole300.clicks.jsonl").read_text(encoding="utf-8").splitlines()]
    table = {row["interval"]: row for row in json.loads((OUT / "hole_seed_entropy_table.json").read_text(encoding="utf-8"))}
    births = [line for line in lines if line["event"] == "birth"]
    credits = [line for line in lines if line["event"] == "credit"]
    refused = [line for line in lines if line["event"] == "refused"]
    birth_intervals = sorted({line["interval"] for line in births})
    bits_at_birth_intervals = sum(sum((room - 1).bit_length() for room in table[t]["rooms"]) for t in birth_intervals)
    draws_at_birth_intervals = sum(table[t]["draws"] for t in birth_intervals)
    light = [line["interval"] for line in births if "point 0 2" in line["children"]]
    beats = Counter((line.get("kind"), line.get("family"), line.get("beat"), line.get("proper")) for line in credits if line.get("beat") is not None)
    realised = Counter(line.get("realised") for line in credits)
    emitted = Counter(line.get("emitted") for line in credits)
    absorbed = Counter(line.get("absorbed") for line in credits)
    senses = Counter(line.get("sense") for line in credits)
    momentum_signs = Counter(json.dumps([axis[0] for axis in line.get("momentum") or []]) for line in credits)
    per50: dict[int, Counter] = {}
    for line in refused:
        per50.setdefault((line["interval"] - 1) // 50, Counter())[line["cause"]] += 1
    found = {
        "births": len(births),
        "birth_intervals": birth_intervals,
        "draws_at_birth_intervals": draws_at_birth_intervals,
        "bits_written_by_the_draws_at_birth_intervals_upper_bound": bits_at_birth_intervals,
        "first_light_lift_birth_interval": light[:1],
        "light_lift_births": len(light),
        "births_nodes": dict(Counter(json.dumps(line["nodes"]) for line in births)),
        "credits": len(credits),
        "credits_with_a_beat": {json.dumps(k): v for k, v in beats.items()},
        "credits_realised": {str(k): v for k, v in realised.items()},
        "credits_emitted": {str(k): v for k, v in emitted.items()},
        "credits_absorbed": {str(k): v for k, v in absorbed.items()},
        "credits_senses": {str(k): v for k, v in senses.items()},
        "credits_momentum_signs_per_axis": dict(momentum_signs),
        "credits_first_last_interval": [credits[0]["interval"], credits[-1]["interval"]] if credits else None,
        "credits_node_detectors": len({line.get("node_detector") for line in credits}),
        "refused_per_50_intervals": {str(k * 50 + 1) + "-" + str(k * 50 + 50): dict(v) for k, v in sorted(per50.items())},
        "last_click_record_interval": max(line["interval"] for line in lines if line["event"] in ("credit", "birth")),
    }
    (OUT / "clicks_readback.json").write_text(json.dumps(found, indent=1), encoding="utf-8")
    text = json.dumps(found, indent=1)
    (OUT / "clicks_readback.txt").write_text(text + "\n", encoding="utf-8")
    sys.stdout.write(text + "\n")


if __name__ == "__main__":
    main()
