"""vf11: a world run by run.record on the src named by PYTHONPATH; a small summary with per-interval hashes of the Node lines, the counts, the credits, the gates' verdicts and the SHOWN set."""
import hashlib
import json
import sys

sys.set_int_max_str_digits(0)
from event_universe.gates import gates, kind_of  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.run import record  # noqa: E402


def sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()[:16]


def main(argv):
    world_path, out_path = argv[1], argv[2]
    universe, world = load_world(world_path)
    if len(argv) > 3:
        world = dict(world, intervals=int(argv[3]))
    back = int(argv[4]) if len(argv) > 4 else 20
    rec = record(universe, world, back, lambda line: None)
    gamma = rec["gamma"]
    credits = [e for e in rec["log"] if e["event"] == "credit"]
    by_interval = {}
    for e in rec["log"]:
        by_interval.setdefault(int(e.get("i", -1)), []).append(e)
    found = gates(json.loads(json.dumps(rec)))
    verdicts = {k: v["verdict"] for k, v in found.items() if isinstance(v, dict) and "verdict" in v}
    kinds = {int(k[:2]): kind_of(v) for k, v in verdicts.items() if k[:2].strip().isdigit()}
    summary = {
        "world": world,
        "gamma": gamma,
        "counts": rec["counts"],
        "turns": rec["turns"],
        "run_back": rec["run_back"],
        "credits": len(credits),
        "laid_back": sum(1 for c in credits if "laid_back" in c),
        "births": sum(1 for e in rec["log"] if e["event"] == "birth"),
        "first_birth_interval": min([int(e["i"]) for e in rec["log"] if e["event"] == "birth"], default=None),
        "x_equals_gamma_at": [n["i"] for n in rec["nodes"] if min(n["X"]) == max(n["X"]) == gamma],
        "x_min_per_interval": [min(n["X"]) for n in rec["nodes"]],
        "node_hashes": [sha(n) for n in rec["nodes"]],
        "log_hash_by_interval": {str(i): sha(es) for i, es in sorted(by_interval.items())},
        "log_len": len(rec["log"]),
        "rows_timeless": [{k: v for k, v in r.items() if k != "milliseconds"} for r in rec["rows"]],
        "max_bits": max(max(r["max bits"], r["max transient bits"]) for r in rec["rows"]),
        "integers": sorted({r["integers"] for r in rec["rows"]}),
        "shown": sorted(n for n, kind in kinds.items() if kind.startswith("SHOWN")),
        "kinds": {str(n): kind for n, kind in sorted(kinds.items())},
        "verdicts": verdicts,
    }
    with open(out_path, "w", encoding="utf-8") as out:
        json.dump(summary, out)
    print(out_path, "counts", rec["counts"], "turns", rec["turns"], "run_back", rec["run_back"], "credits", len(credits), "shown", summary["shown"])


if __name__ == "__main__":
    main(sys.argv)
