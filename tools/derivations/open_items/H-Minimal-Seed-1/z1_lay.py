"""Hand z1, part (a): the seed's three forms as the one lay act before the first interval. For each seed world file: the
lays' integers (the drift v = isqrt(T) the law's form, v^2 against T), the two sums of the massless row's levels after
each lay (the guard's two sums: a massless lay with no weights is laid as built and moves SUM now by name; a lay with
weights would be corrected to 0 and is not the seed's), the count at the vacuum's weight (the share summed div W_c and
the per-Node rounding's sum), the refusals by name, and the cube's 48 on the lay: the seed list carried by each of the
48 signed permutations about the origin and laid gives the carried board bit for bit (the test harness's `carried` and
`apart`, tests/test_the_board_is_the_cube_48.py), the 8 mirrors (the sign flips) counted among them.

    PYTHONPATH=src python tools/derivations/open_items/H-Minimal-Seed-1/z1_lay.py tools/derivations/open_items/H-Minimal-Seed-1/worlds/emergence_hole.json ...
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from z1lib import ROOT, board_of, drift_of, light_quanta, read_seed_world, refused  # noqa: E402

sys.path.insert(0, str(ROOT))
from tests.test_the_board_is_the_cube_48 import IDENTITY, apart, axis_map, carried, cube_48  # noqa: E402


def moved_seed(seeds: list[dict], m: np.ndarray, shape: tuple[int, int, int]) -> list[dict]:
    """The seed list carried by the signed permutation `m` about the origin: every Node of every lay mapped, (m x) mod the shape per axis."""
    found = []
    for entry in seeds:
        moved = dict(entry)
        for key in ("at", "centre"):
            if key in entry:
                image = np.mod(m @ np.array(entry[key]), np.array(shape))
                moved[key] = [int(v) for v in image]
        found.append(moved)
    return found


def sums_of(board, index: int) -> tuple[int, int]:
    line = board.states[index].lines[0]
    return int(np.asarray(line.now, dtype=object).sum()), int(np.asarray(line.before, dtype=object).sum())


def main(paths: list[str]) -> None:
    out = HERE / "out"
    out.mkdir(exist_ok=True)
    for name in paths:
        path = Path(name)
        began = time.perf_counter()
        engine, seeds = read_seed_world(path)
        folder = Path("/dev/shm/tmp") / f"z1_lay_{path.stem}"
        board, laid, _bad = board_of(path, folder)
        light = board.world.seed
        T, v = board.world.quantum_action, drift_of(board.world.quantum_action)
        total, by_div, by_node = light_quanta(board)
        shape = board.shape
        report = {
            "world": path.name,
            "engine_keys": engine,
            "seed": seeds,
            "lays": laid,
            "drift": {"v": v, "v_squared": v * v, "T": T, "v_squared_milli_over_T": (1000 * v * v) // T, "law": "v the largest integer with v^2 <= T (seed.drift_of); the share 3 den v^2 per Node against W_c = 3 den T"},
            "massless_sums_after_lay": {"sum_now": sums_of(board, light)[0], "sum_before": sums_of(board, light)[1], "nodes": int(np.prod(shape))},
            "count_at_vacuum_weight": {"share_total": total, "W_c": board.credit.units[light], "share_div_Wc": by_div, "per_node_rounded_sum": by_node},
            "integers_per_node": None,
            "width_bits": board.world.width.bit_length(),
            "kind": board.kind.__name__ if hasattr(board.kind, "__name__") else str(board.kind),
            "amplitude_bound": board.world.amplitude_bound,
        }
        from tools.node_integers import largest_bits, same_shape, total_of  # noqa: PLC0415

        bits, label = largest_bits(board)
        report["integers_per_node"] = {"count": total_of(board), "same_at_every_node": same_shape(board), "largest_bits": bits, "largest_at": label}
        # the refusals by name
        tries = {
            "a form not among the three": [{"lay": "wave", "row": [348893, 348893]}],
            "a lay named by a family": [{"lay": "at", "family": "electron", "row": [348893, 348893], "centre": [1, 0, 0]}],
            "a one-Node body (width 0)": [{"lay": "at", "row": [89493, 348893], "centre": [2, 2, 2], "width": 0, "quanta": 10}],
            "a sea of a gapped row": [{"lay": "sea", "row": [89493, 348893]}],
            "a Node off the board": [{"lay": "hole", "at": [9, 0, 0]}],
            "a pair of no row": [{"lay": "at", "row": [7, 348893], "centre": [1, 0, 0]}],
        }
        report["refusals"] = {name: refused(entry, board.families, shape) for name, entry in tries.items()}
        # the guard on a massless lay with weights: the division act takes the whole quantum out (measured on a scratch board, the lay then refused or nulled)
        from event_universe import lay  # noqa: PLC0415

        here = np.zeros(shape, dtype=bool)
        here[1, 0, 0] = True
        weights = np.where(here, 1, 0).astype(object)
        now = np.where(here, v, 0).astype(object)
        corrected = lay.corrected("massless", True, (now, now * 0), weights)
        report["guard_on_a_weighted_massless_one_node_lay"] = {"sum_now_as_laid": int(now.sum()), "sum_now_after_division_act": int(np.asarray(corrected[0], dtype=object).sum()), "reading": "the division act takes the uniform part out: a weighted massless one-Node lay lays nothing; so the seed's massless lays are laid with no weights, as built, by name"}
        try:
            lay.guarded("massless", True, v, 0, False)
            report["guard_refuses_a_moved_sum"] = False
        except ValueError as refusal:
            report["guard_refuses_a_moved_sum"] = str(refusal)[:120]
        # the 48 on the lay
        group = cube_48() if len(set(shape)) == 1 else []  # the harness's carry assumes a cube: a non-cubic board is named and its 48 read on its cubic twin (worlds/bodies_lay7.json)
        kept, mirrors_kept, mirrors = 0, 0, 0
        broken = []
        state = None
        for m in group:
            is_mirror = axis_map(m)[0] == [0, 1, 2]
            mirrors += is_mirror
            other_folder = Path("/dev/shm/tmp") / f"z1_lay_{path.stem}_m"
            moved = moved_seed(seeds, m, shape)
            moved_path = other_folder / "moved.json"
            other_folder.mkdir(parents=True, exist_ok=True)
            moved_path.write_text(json.dumps({**engine, "seed": moved}))
            (other_folder / engine["universe"]).write_text((path.parent / engine["universe"]).read_text())
            other, _l, _b = board_of(moved_path, other_folder / "run")
            differences = apart(carried(board, m, None), carried(other, IDENTITY))
            if not differences:
                kept += 1
                mirrors_kept += is_mirror
            else:
                broken.append({"element": m.tolist(), "differences": len(differences), "first": [str(d) for d in differences[:2]]})
        report["cube_48_on_the_lay"] = {"kept": kept, "of": len(group), "mirrors_kept": mirrors_kept, "mirrors": mirrors, "broken": broken[:4]}
        report["seconds"] = round(time.perf_counter() - began, 1)
        (out / f"lay_{path.stem}.json").write_text(json.dumps(report, indent=1, default=str) + "\n")
        print(json.dumps({k: report[k] for k in ("world", "drift", "massless_sums_after_lay", "count_at_vacuum_weight", "integers_per_node", "cube_48_on_the_lay", "refusals", "guard_on_a_weighted_massless_one_node_lay", "seconds")}, default=str))


if __name__ == "__main__":
    main(sys.argv[1:])
