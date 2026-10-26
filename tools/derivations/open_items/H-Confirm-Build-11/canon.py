"""vf11 (c): the plasma_3 world run to N under permuted universe files, with a canonical per-interval hash independent of the file's order of rows (the rows keyed by shape, pair and wall; every line's now, before, rem and wr), and the shape-4 row's time line's write remainder hashed by itself. `make` writes the permuted files; `run <world> <N> <out>` runs one."""
import hashlib
import json
import sys
from pathlib import Path

sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER, POTENTIAL  # noqa: E402

HERE = Path(__file__).resolve().parent
TOY = HERE.parents[3] / "tests" / "worlds"


def text(a):
    return " ".join(str(int(v)) for v in a.reshape(-1))


def canon(node):
    parts = []
    for r in sorted(node.rows_, key=lambda r: (r.shape, r.pair or (0, 0), r.wall or 0)):
        for line in r.lines:
            for a in (line.now, line.before, line.rem, line.wr):
                if a is not None:
                    parts.append(text(a))
    return hashlib.sha256("|".join(parts).encode()).hexdigest()[:16]


def make():
    universe = json.loads((TOY / "universe_toy.json").read_text())
    world = json.loads((TOY / "world_plasma_3.json").read_text())
    rows = universe["rows"]  # 0 gap0, 1 light, 2 heavy, 3 third, 4 carrier, 5 potential, 6 walled
    (HERE / "worlds").mkdir(exist_ok=True)
    plans = {
        "original": [0, 1, 2, 3, 4, 5, 6],
        "gapped_after": [0, 1, 4, 5, 2, 3, 6],
        "gapped_before": [3, 2, 1, 0, 5, 4, 6],
    }
    for name, order in plans.items():
        new_index = {old: new for new, old in enumerate(order)}
        u = {"integers": universe["integers"], "rows": [rows[old] for old in order]}
        w = dict(world, universe=f"universe_{name}.json")
        w["seed"] = [dict(lay, row=new_index[lay["row"]]) for lay in world["seed"]]
        (HERE / "worlds" / f"universe_{name}.json").write_text(json.dumps(u))
        (HERE / "worlds" / f"world_plasma_3_{name}.json").write_text(json.dumps(w))
        print(name, "rows", [rows[old]["shape"] for old in order], "seed", w["seed"])


def run(world_path, n, out_path):
    universe, world = load_world(world_path)
    node = Node(universe, world)
    print("acts' order of rows_:", [(r.shape, r.gap) for r in node.rows_])
    hashes, wr_hashes, x_min = [], [], []
    for _ in range(n):
        node.step()
        hashes.append(canon(node))
        wr_hashes.append(hashlib.sha256(text(node.row(POTENTIAL).lines[0].wr).encode()).hexdigest()[:16])
        x_min.append(int(node.row(CARRIER).lines[0].now.min()))
    out = {
        "world": world_path, "intervals": n, "turns": node.turns,
        "counts": {k: int(v) for k, v in node.counts.items()},
        "canon_hashes": hashes, "time_line_wr_hashes": wr_hashes, "x_min": x_min,
        "rows_order": [(r.shape, r.gap) for r in node.rows_],
    }
    Path(out_path).write_text(json.dumps(out))
    print(out_path, "turns", node.turns, "counts", out["counts"])


if __name__ == "__main__":
    if sys.argv[1] == "make":
        make()
    else:
        run(sys.argv[2], int(sys.argv[3]), sys.argv[4])
