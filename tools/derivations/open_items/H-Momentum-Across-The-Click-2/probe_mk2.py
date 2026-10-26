"""mk2's probe, two uses. (1) `analyse <record.json>`: on a record's log, every birth's Link axis (the axis on which
minus and plus differ), the take's momentum component along that axis against the two transverse ones, the two-Node
lay's grain 2 num_s A (one level of before at the far end of the children's re line, the plane at nothing around:
Theorem A) and the quotient p and remainder r of the along-axis component at that grain, the cap 2 num_s A^2; the
credits named as clicks with no Link. Integers only. (2) `run <world.json> <intervals> <back> <out.json>`: the
world run by the engine's own writer under the src on PYTHONPATH (the flag MK2_RECOIL=1 or not), the record written
(the cache's form: the same keys run.forward gives) and the analysis of its log printed."""
import hashlib
import json
import os
import sys

sys.set_int_max_str_digits(0)
AXES = 3


def nearest(n, w):
    """The nearest quotient of n at the wall w (w > 0), ties toward zero's side as floor of (2n + w) div 2w."""
    return (2 * n + w) // (2 * w)


def analyse(record):
    planes = [int(x) for x in record["planes"]]
    log = record["log"]
    births = [e for e in log if e["event"] == "birth"]
    credits = [e for e in log if e["event"] == "credit"]
    cube = int(record["cube"])
    rows = []
    along_abs = [0] * AXES
    transverse_abs = [0] * AXES
    take_abs = [0] * AXES
    remainders_abs = 0
    along_total_abs = 0
    exact = 0
    under_cap = 0
    for e in births:
        minus, plus = e["minus"], e["plus"]
        axis = [a for a in range(AXES) if (minus[a] - plus[a]) % cube != 0]
        assert len(axis) == 1
        a = axis[0]
        s = e["line_pair"]
        num = planes[s] if s < len(planes) else None
        A, B = e["amplitude"]
        dp = [int(x) for x in e["dP_take"]]
        grain = 2 * num * A
        cap = 2 * num * A * A
        p = nearest(-dp[a], grain)
        r = -dp[a] - grain * p
        exact += r == 0
        under_cap += abs(dp[a]) <= cap
        remainders_abs += abs(r)
        along_total_abs += abs(dp[a])
        for b in range(AXES):
            take_abs[b] += abs(dp[b])
            if b == a:
                along_abs[b] += abs(dp[b])
            else:
                transverse_abs[b] += abs(dp[b])
        rows.append({"i": e["i"], "axis": a, "dP_take": dp, "along": dp[a], "grain": grain, "p": p, "r": r, "cap": cap, "A": A, "stood": e["stood"]})
    credit_abs = [sum(abs(int(e["dP_take"][b])) for e in credits) for b in range(AXES)]
    credit_laid_back = sum(1 for e in credits if "laid_back" in e)
    return {
        "births": len(births), "credits": len(credits), "credits laid back": credit_laid_back,
        "births: take abs per axis": take_abs,
        "births: along the Link's axis, abs per axis": along_abs,
        "births: transverse to the Link's axis, abs per axis": transverse_abs,
        "births: along-axis remainder abs summed at the grain 2 num A": remainders_abs,
        "births: along-axis take abs summed": along_total_abs,
        "births: remainder exact 0": exact, "births: under the cap 2 num A^2": under_cap,
        "births: p (levels of before at the far end) largest": max((abs(r["p"]) for r in rows), default=0),
        "births: stood at nothing at both ends": sum(1 for r in rows if all(x == 0 for end in r["stood"] for x in end)),
        "credits: take abs per axis (no Link named by the click)": credit_abs,
        "first births": rows[:6],
    }


def main(argv):
    if argv[1] == "analyse":
        record = json.load(open(argv[2]))
        print(json.dumps(analyse(record), indent=0))
        return
    from event_universe import run as writer
    from event_universe.loader.world import load_world
    from event_universe.node import Node
    from event_universe.gates import gates, kind_of
    world_path, intervals, back, out = argv[2], int(argv[3]), int(argv[4]), argv[5]
    universe, world = load_world(world_path)
    world = dict(world, intervals=intervals)
    node = Node(universe, world)
    rows, nodes, hashes = writer.forward(node, intervals, back, lambda line: None)
    final_hash = node.state_hash()
    kept_log = list(node.log)
    returned = writer.run_back(node, hashes) if back else None
    counts = {k: str(v) for k, v in node.counts.items()}
    record = {
        "world": world, "universe": universe, "den": node.den, "cube": node.cube, "intervals": intervals,
        "gapped": [(str(r.pair[0]), str(writer.sine_den(r.pair[0], node.den))) for r in node.gapped if r.pair],
        "planes": [str(r.pair[0]) for r in node.records() if r.pair], "T": node.T, "gamma": node.gamma, "G": node.G,
        "counts": counts, "turns": node.turns, "rows": rows, "nodes": nodes, "run_back": returned, "log": kept_log,
    }
    json.dump(record, open(out, "w"))
    found = gates(record)
    kinds = {int(k[:2]): kind_of(v["verdict"]) for k, v in found.items() if k[:2].strip().isdigit()}
    shown = sorted(n for n, kind in kinds.items() if kind.startswith("SHOWN"))
    summary = {
        "world": world_path, "intervals": intervals, "flag": os.environ.get("MK2_RECOIL", ""),
        "final state hash": final_hash, "log hash": hashlib.sha256(json.dumps(kept_log, sort_keys=True).encode()).hexdigest(),
        "counts": counts, "run_back": returned, "integers per Node": sorted({r["integers"] for r in rows}),
        "max state bits": max(r["max bits"] for r in rows), "max transient bits": max(r["max transient bits"] for r in rows),
        "gates SHOWN": shown, "gate 23": found["23 the momentum across the click"], "gate 54": found["54 scattering, two packets through each other"]["verdict"],
        "analysis": analyse(record),
    }
    print(json.dumps(summary, indent=0))


if __name__ == "__main__":
    main(sys.argv)
