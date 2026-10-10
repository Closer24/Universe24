"""The ensemble over seeds for the paper's run (run3d_fixed/one_piece_3d_fixed.json, this folder's parent): the same world, mode file and detectors, the toss's seed the only change, run forward 172 ticks with the program, and three variants of the world: both detectors ("both"), the detector at the smaller x alone ("A", the atom at (175, 4, 4) and (176, 4, 4)) and the detector at the larger x alone ("B", at (223, 4, 4) and (224, 4, 4)). For every seed: which detector took the piece and at which close, the count at the end, and the weights of equation (2) read at every close reached (share_over_unit per body, the engine's own numbers). The summary: the click frequencies per detector with the binomial uncertainty, the fraction with no click, the far detector's frequency conditioned on the near one's click, and the prediction of equation (3) chained over the closes from the weights of a run that reached them with no click. Nothing in the repository is changed; the variant worlds are written under ensemble/worlds/ while a run lasts. The results, ensemble_seeds.json (every row) and summary.json (the same without the rows), sit beside this script. Usage: python3 -I ensemble_seeds.py [--seeds 400] [--first 1] [--variants both,A,B] [--workers 4] [--out ensemble_seeds.json]; --summarise FILE rebuilds the summary of a saved ensemble from its rows; --check recomputes the summary from the saved rows and compares it with summary.json, exit 1 where they differ (what build.sh runs)."""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import shutil
import sys
import time
from multiprocessing import Pool
from pathlib import Path

OUT = Path(__file__).resolve().parent          # run3d_fixed/ensemble
RUN = OUT.parent                                # run3d_fixed: the world, its mode file and design.json
V2 = OUT.parents[3]                             # the repository's root
sys.path.insert(0, str(V2 / "src"))

from event_universe.lattice import Lattice  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402



def load_file(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


WORLD = RUN / "one_piece_3d_fixed.json"
INTERVALS = 172
CLOSES = (48, 96, 144)
VARIANTS = {"both": (0, 1), "A": (0,), "B": (1,)}


def variant_world(variant: str, seed: int) -> Path:
    """The world with the bodies of the variant kept, both seeds set to `seed`; its mode file written beside it by tools/pixel_mode.py (the packets do not change; the digest does)."""
    folder = OUT / "worlds"
    folder.mkdir(parents=True, exist_ok=True)
    document = json.loads(WORLD.read_text(encoding="utf-8"))
    document["bodies"] = [b for i, b in enumerate(document["bodies"]) if i in VARIANTS[variant]]
    for body in document["bodies"]:
        body["node_detector"]["seed"] = seed
    path = folder / f"one_piece_3d_fixed_{variant}_{seed}.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    design = folder / "design.json"
    if not design.exists():
        shutil.copy(WORLD.with_name("design.json"), design)
    tool = load_file("pixel_mode", V2 / "tools" / "pixel_mode.py")  # writes the mode file beside a world, with that world's digest
    tool.main(["--input", str(path)])
    return path


def shares(board: Lattice, photon: int) -> dict:
    out = {}
    for nb in board.credit.bodies:
        unit = sum(int(v) ** 2 for v in nb.labels)
        out[f"body {nb.number}"] = round(sum(int(v) for v in nb.shares.values()) / unit, 6) if unit else None
    out["count"] = int(board.credit.counts[photon])
    return out


def one(args: tuple[str, int]) -> dict:
    variant, seed = args
    path = variant_world(variant, seed)
    lines: list[dict] = []
    board = Lattice(load_world(path), lines.append)
    photon = [f.name for f in board.families].index("photon")
    closes = {}
    for _ in range(INTERVALS):
        board.step()
        t = board.interval
        if t in CLOSES:
            closes[t] = shares(board, photon)
        if board.credit.counts[photon] == 0 or board.ended is not None:
            break
    taken = [c for c in lines if c["event"] == "credit" and c.get("absorbed")]
    # the body numbers are the world's after the variant's drop: map back to the original 0 (A) and 1 (B)
    kept = VARIANTS[variant]
    click = None
    if taken:
        number = int(taken[0]["node_detector"].split()[-1])
        click = {"tick": taken[0]["interval"], "detector": "AB"[kept[number]], "chance_lines": len(taken)}
    path.unlink(missing_ok=True)
    path.with_suffix(".mode.json").unlink(missing_ok=True)
    return {"variant": variant, "seed": seed, "click": click, "count_at_end": int(board.credit.counts[photon]), "closes": {str(k): v for k, v in closes.items()}, "last_tick": board.interval}


def binomial(k: int, n: int) -> list[float]:
    p = k / n if n else float("nan")
    return [round(p, 4), round(math.sqrt(p * (1 - p) / n), 4) if n else float("nan")]


def prediction(rows: list[dict], variant: str) -> dict:
    """Equation (3) chained over the closes from the weights read in a run that reached each close with no click: U starts at 1 and is lowered by the weights of every close with no click; at a close W_0 = max(min(U, 1) - sum W, 0) and P_i = W_i / (W_0 + sum W)."""
    bodies = ["body %d" % i for i in range(len(VARIANTS[variant]))]
    names = {("body %d" % i): "AB"[k] for i, k in enumerate(VARIANTS[variant])}
    weights = {}
    for t in CLOSES:
        for r in rows:
            c = r["closes"].get(str(t))
            if c and (r["click"] is None or r["click"]["tick"] >= t) and all(c.get(b) is not None for b in bodies):  # the shares at a close are the weights before its draw, kept when the draw falls at that close
                weights[t] = {names[b]: c[b] for b in bodies}
                break
    U, alive, p = 1.0, 1.0, {"A": 0.0, "B": 0.0}
    chain = {}
    for t in CLOSES:
        if t not in weights:
            break
        w = weights[t]
        s = sum(w.values())
        w0 = max(min(U, 1.0) - s, 0.0)
        denominator = w0 + s
        here = {d: w[d] / denominator for d in w}
        chain[str(t)] = {"weights": w, "no_click_weight": round(w0, 4), "chance_here": {d: round(v, 4) for d, v in here.items()}, "reached_with_no_click": round(alive, 4)}
        for d in w:
            p[d] += alive * here[d]
        alive *= w0 / denominator
        U = U - s
    return {"weights_read": {str(k): v for k, v in weights.items()}, "chain": chain, "predicted": {"A": round(p["A"], 4), "B": round(p["B"], 4), "none": round(alive, 4)}}


def summary(rows: list[dict], variant: str) -> dict:
    n = len(rows)
    a = sum(1 for r in rows if r["click"] and r["click"]["detector"] == "A")
    b = sum(1 for r in rows if r["click"] and r["click"]["detector"] == "B")
    none = n - a - b
    by_tick = {}
    for r in rows:
        if r["click"]:
            key = f"{r['click']['detector']} at {r['click']['tick']}"
            by_tick[key] = by_tick.get(key, 0) + 1
    out = {"seeds": n, "A_clicks": a, "B_clicks": b, "no_click": none, "A_frequency": binomial(a, n), "B_frequency": binomial(b, n), "no_click_fraction": binomial(none, n), "clicks_by_detector_and_tick": dict(sorted(by_tick.items())),
           "two_clicks_in_one_run": sum(1 for r in rows if r["click"] and r["click"]["chance_lines"] > 1), "prediction_from_the_weights": prediction(rows, variant)}
    if variant == "both":
        out["B_given_A_clicked"] = binomial(sum(1 for r in rows if r["click"] and r["click"]["detector"] == "A" and r["click"]["chance_lines"] > 1), a)  # one piece: a second credit line in a run where A took it
        out["B_given_A_did_not_click"] = binomial(b, n - a)
        out["A_given_B_clicked"] = binomial(sum(1 for r in rows if r["click"] and r["click"]["detector"] == "B" and r["click"]["chance_lines"] > 1), b)
        out["A_given_B_did_not_click"] = binomial(a, n - b)
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=400)
    ap.add_argument("--first", type=int, default=1)
    ap.add_argument("--variants", default="both,A,B")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out", default="ensemble_seeds.json")
    ap.add_argument("--summarise", default=None, help="rebuild the summary of a saved ensemble JSON without rerunning")
    ap.add_argument("--check", action="store_true", help="recompute the summary from the saved rows and compare it with summary.json")
    a = ap.parse_args(argv[1:])
    if a.check:
        saved = json.loads((OUT / "ensemble_seeds.json").read_text(encoding="utf-8"))
        recomputed = {k: v for k, v in saved.items() if k != "rows"}
        recomputed["summary"] = {v: summary([r for r in saved["rows"] if r["variant"] == v], v) for v in saved["variants"]}
        written = json.loads((OUT / "summary.json").read_text(encoding="utf-8"))
        same = recomputed == written and recomputed["summary"] == saved["summary"]
        print(f"ensemble_seeds --check: {len(saved['rows'])} rows over the seeds {saved['seeds']}, the summary recomputed from them {'matches' if same else 'DIFFERS FROM'} summary.json")
        return 0 if same else 1
    if a.summarise:
        saved = json.loads((OUT / a.summarise).read_text(encoding="utf-8"))
        saved["summary"] = {v: summary([r for r in saved["rows"] if r["variant"] == v], v) for v in saved["variants"]}
        (OUT / a.summarise).write_text(json.dumps(saved, indent=1), encoding="utf-8")
        (OUT / "summary.json").write_text(json.dumps({k: v for k, v in saved.items() if k != "rows"}, indent=1) + "\n", encoding="utf-8")
        print(json.dumps({k: v for k, v in saved.items() if k != "rows"}, indent=1))
        return 0
    variants = a.variants.split(",")
    jobs = [(v, s) for v in variants for s in range(a.first, a.first + a.seeds)]
    t0 = time.perf_counter()
    with Pool(a.workers) as pool:
        rows = pool.map(one, jobs, chunksize=4)
    elapsed = time.perf_counter() - t0
    report = {"world": str(WORLD.relative_to(V2)), "intervals": INTERVALS, "closes": list(CLOSES), "seeds": [a.first, a.first + a.seeds - 1], "variants": variants, "wall_time_s": round(elapsed, 1), "workers": a.workers,
              "summary": {v: summary([r for r in rows if r["variant"] == v], v) for v in variants}, "rows": rows}
    out = OUT / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=1), encoding="utf-8")
    (OUT / "summary.json").write_text(json.dumps({k: v for k, v in report.items() if k != "rows"}, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "rows"}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
