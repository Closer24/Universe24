"""tw2's runner: one world of tests/worlds under the flagged copy at TW2_TRACE (the environment), the record run
with the run back over 10 intervals, the gates read, and one summary line written as JSON to the output file:
the trace weight, the world, the record's hash (the record's JSON less its clocks), the bottoms of the mean volume
(interval, mean X, at Gamma at every Node), the tops with the whole board turning at once, the births, the body
credits, the laid levels, the run back exact of intervals, the state's max bits, the gates SHOWN by kind, gate 1
and gate 46 verdicts, the charge W total at the last mark, and the counts. Usage: run_tw2.py <world.json> <out.json>"""
import hashlib
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
# TW2_HEAD set: the head's own src (the worktree's), to show the unflagged copy is the head bit for bit
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "..", "src") if os.environ.get("TW2_HEAD") else os.path.join(HERE, "src_tw2"))

from event_universe import board, gates, rows  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.run import record  # noqa: E402


def main(argv):
    sys.set_int_max_str_digits(0)
    universe, world = load_world(argv[1])
    t0 = time.monotonic_ns()
    found = record(universe, world, 10, lambda line: None)
    seconds = (time.monotonic_ns() - t0) // 1000000000
    stripped = json.loads(json.dumps(found))
    for row in stripped["rows"]:
        row.pop("milliseconds", None)
    digest = hashlib.sha256(json.dumps(stripped, sort_keys=True).encode()).hexdigest()
    verdicts = gates.gates(found)
    rec = gates.Record(found)
    bang = board.recurring_bang(rec)["1 recurring bangs"]
    shown = verdicts["the decoder"]["rows by the verdict's kind (the numbered rows)"]
    gate46 = {k: v["verdict"] for k, v in verdicts.items() if k.split()[0] == "46"}
    gate1 = bang["verdict"]
    last = found["rows"][-1]
    summary = {
        "trace": rows.TRACE,
        "world": os.path.basename(argv[1]),
        "intervals": found["intervals"],
        "hash": digest,
        "bottoms": bang["bottoms (interval, mean X, at Gamma at every Node)"],
        "whole tops": bang["tops with every Node turning at once (interval)"],
        "births": found["counts"]["births"],
        "credits": found["counts"]["body_clicks"],
        "laid": found["counts"]["laid"],
        "turns": found["counts"]["turns"],
        "run back": found["run_back"],
        "max bits": last["max bits"],
        "max transient bits": last["max transient bits"],
        "integers": last["integers"],
        "W total": last["W total"],
        "volume mean last": last["volume mean"],
        "shown": shown,
        "gate 1": gate1,
        "gate 46": gate46,
        "seconds": seconds,
    }
    with open(argv[2], "w", encoding="utf-8") as out:
        json.dump(summary, out)
    print(json.dumps({k: summary[k] for k in ("trace", "world", "hash", "births", "credits", "run back", "max bits", "shown", "seconds")}))


if __name__ == "__main__":
    main(sys.argv)
