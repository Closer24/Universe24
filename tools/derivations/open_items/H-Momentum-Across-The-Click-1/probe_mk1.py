"""mk1's probe: a world run under the src on PYTHONPATH (the flag MK1_RECOIL in the environment or not), the engine's
own writer for the rows, the Node lines and the run back (event_universe.run.forward / run_back), with the board's lattice
momentum of every record row read before and after every close (P_a = 2 num SUM_i (now_(i+a) before_i - now_i before_(i+a))
summed over the row's lines, the reading of ALGEBRA.md's The lattice momentum), the per-click identity on every booked
line (dP_take + dP_recoil, exact where 0), the gates read on the record, the final state's hash and the log's hash.
Usage: python probe_mk1.py <world.json> <intervals> <back> <out.json>. Integers only."""
import hashlib
import json
import sys
import time

import numpy as np

from event_universe import run as writer
from event_universe.gates import gates, kind_of
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import CARRIER

AXES = 3


def ints(a):
    return [int(x) for x in a.reshape(-1)]


def momenta(node):
    """Every record row's lattice momentum per axis over the board, and the board's sum."""
    found = []
    for row in node.records():
        num = row.pair[0]
        per = []
        for a in range(AXES):
            total = 0
            for line in row.lines:
                total += sum(ints(np.roll(line.now, -1, axis=a) * line.before - line.now * np.roll(line.before, -1, axis=a)))
            per.append(2 * num * total)
        found.append(per)
    board = [sum(p[a] for p in found) for a in range(AXES)]
    return found, board


def main(argv):
    sys.set_int_max_str_digits(0)
    world_path, intervals, back, out = argv[1], int(argv[2]), int(argv[3]), argv[4]
    universe, world = load_world(world_path)
    world = dict(world, intervals=intervals)
    node = Node(universe, world)
    closes = []
    original = node.click

    def click(plane_starts, held, direction=1, frame=None):
        if direction == 1:
            rows_b, board_b = momenta(node)
        original(plane_starts, held, direction, frame)
        if direction == 1:
            rows_a, board_a = momenta(node)
            closes.append({"i": node.interval, "rows_before": rows_b, "rows_after": rows_a, "board_before": board_b, "board_after": board_a})

    node.click = click
    t0 = time.monotonic_ns()
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
    log_hash = hashlib.sha256(json.dumps(kept_log, sort_keys=True).encode()).hexdigest()
    found = gates(record)
    kinds = {int(k[:2]): kind_of(v["verdict"]) for k, v in found.items() if k[:2].strip().isdigit()}
    shown = sorted(n for n, kind in kinds.items() if kind.startswith("SHOWN"))
    clicks = [e for e in kept_log if e["event"] in ("birth", "credit")]
    booked = [e for e in clicks if "kick" in e]
    identity = {
        "clicks": len(clicks),
        "laid_back": sum(1 for e in clicks if "laid_back" in e),
        "kicks booked": len(booked),
        "kicks moved (q != 0)": sum(1 for e in booked if e["kick"] != 0),
        "kicks flat (the gradient 0)": sum(1 for e in booked if e["kick_wall"] == 0),
        "identity exact (dP_take + dP_recoil = 0 on all three axes)": sum(1 for e in booked if all(e["dP_take"][a] + e["dP_recoil"][a] == 0 for a in range(AXES))),
        "identity exact among the moved": sum(1 for e in booked if e["kick"] != 0 and all(e["dP_take"][a] + e["dP_recoil"][a] == 0 for a in range(AXES))),
        "dP_take summed": [sum(e["dP_take"][a] for e in clicks) for a in range(AXES)],
        "dP_recoil summed": [sum(e["dP_recoil"][a] for e in booked) for a in range(AXES)],
        "residual summed (take + recoil)": [sum(e["dP_take"][a] for e in clicks) + sum(e["dP_recoil"][a] for e in booked) for a in range(AXES)],
        "residual abs summed": [sum(abs(e["dP_take"][a] + e.get("dP_recoil", [0, 0, 0])[a]) for e in clicks) for a in range(AXES)],
        "take abs summed": [sum(abs(e["dP_take"][a]) for e in clicks) for a in range(AXES)],
        "kick abs summed": sum(abs(e["kick"]) for e in booked),
        "kick largest": max((abs(e["kick"]) for e in booked), default=0),
    }
    board_moves = [c for c in closes if c["board_before"] != c["board_after"]]
    x_gamma = [line["i"] for line in nodes if all(x == node.gamma for x in line["X"])]
    carrier = node.row(CARRIER)
    summary = {
        "world": world_path, "intervals": intervals, "cube": node.cube, "seconds": (time.monotonic_ns() - t0) // 10**9,
        "flag": __import__("os").environ.get("MK1_RECOIL", ""),
        "final state hash": final_hash, "log hash": log_hash, "counts": counts, "run_back": returned,
        "integers per Node": sorted({r["integers"] for r in rows}), "max state bits": max(r["max bits"] for r in rows),
        "max transient bits": max(r["max transient bits"] for r in rows),
        "births": counts["births"], "credits": counts["body_clicks"], "turns": counts["turns"],
        "gates SHOWN": shown, "gate 23": found["23 the momentum across the click"], "gate 54": found["54 scattering, two packets through each other"]["verdict"],
        "gate 1": found.get("1 the recurring bang", {}).get("verdict"), "gate 46": found.get("46 the bangs recurring with the same gates", {}).get("verdict"),
        "the conservations": found["the conservations in the clicks"]["verdict"], "the three constants": found["the three constants"]["verdict"],
        "X equal Gamma at every Node at intervals": x_gamma,
        "identity": identity,
        "closes": len(closes), "closes moving the board's momentum": len(board_moves),
        "board momentum at the start": closes[0]["board_before"] if closes else None,
        "board momentum at the end": closes[-1]["board_after"] if closes else None,
        "board momentum change summed over the closes": [sum(c["board_after"][a] - c["board_before"][a] for c in closes) for a in range(AXES)],
        "board momentum abs change summed over the closes": [sum(abs(c["board_after"][a] - c["board_before"][a]) for c in closes) for a in range(AXES)],
        "rows momentum at the end": closes[-1]["rows_after"] if closes else None,
        "first closes moving the board": board_moves[:3],
    }
    json.dump({"summary": summary, "closes": closes, "gates": found, "log": kept_log, "rows": rows}, open(out, "w"), indent=0)
    print(json.dumps({k: v for k, v in summary.items() if k != "first closes moving the board"}))


if __name__ == "__main__":
    main(sys.argv)
