"""Hand z2: the lay as one act, measured on the engine's own lay.laid (no edit of src/): (1) the three forms' change of the
two sums SUM now and SUM before (the guard reads a massless lay's change of the two sums where weights are given; the seed's
forms are laid with no weights, the uniform part the lay itself, named by the door); (2) the guard's refusal by name on a
massless lay handed weights whose change moves a sum; (3) the division act on a massless packet with weights: the two sums
taken out (the packet laid with a zero uniform part); (4) the eight mirrors and the 48 about the hole on the laid light; (5)
the count at the vacuum's weight per Node (share over W_c = 3 den T, the floor and the rounded count); (6) the seed list's
refusals by name (a lay naming a row, a one-Node body, a light packet with a width, a pair of no row). Integers only.

    PYTHONPATH=src python tools/derivations/z2/lay_checks.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
for place in (str(ROOT), str(ROOT / "src"), str(HERE)):
    if place not in sys.path:
        sys.path.insert(0, place)

import numpy as np  # noqa: E402

from event_universe import records, seed, world_files  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.lay import laid  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402
from seed_run import body_forms, cube_48, image_node, light_forms, vacuum_share  # noqa: E402

DEN, GAMMA, T = 1655909141, 1000, 36000
LIGHT = [DEN, DEN]


def board_of(folder: Path, seed_list: list, cube: int = 5) -> tuple[Lattice, dict]:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "u.json").write_text(json.dumps({"integers": {"den": DEN, "node_clock": GAMMA, "quantum_action": T}}), "utf-8")
    (folder / "w.json").write_text(json.dumps({"universe": "u.json", "shape": [cube] * 3, "intervals": 10}), "utf-8")
    world_files.REPOSITORY_ROOT = folder
    notes: dict = {}
    seed.uniform_seed = lambda board, index: light_forms(board, index, seed_list, notes)
    board = Lattice(load_world(folder / "w.json"), output=None)
    body_forms(board, seed_list, notes)
    return board, notes


def sums(board: Lattice, index: int) -> tuple[int, int]:
    line = board.states[index].lines[records.record_slice(board.families[index], 0).start]
    return int(np.asarray(line.now, dtype=object).sum()), int(np.asarray(line.before, dtype=object).sum())


def main() -> None:
    out: dict = {}
    base = Path("/dev/shm/tmp/z2_laychecks")
    # (1) the three forms' change of the two sums, each laid alone on an empty board
    forms = {
        "sea_1": [{"sea": 1}],
        "sea_1_hole": [{"sea": 1}, {"hole": [0, 0, 0]}],
        "sea_1_plus_one_at_100": [{"sea": 1}, {"at": {"pair": LIGHT, "centre": [1, 0, 0], "sigma_tenths": 0, "quanta": 1}}],
        "wave_3_modes_1_per_mode": [{"sea": {"quanta_per_mode": 1, "modes": [[1, 0, 0], [0, 1, 0], [0, 0, 1]], "centre": [2, 2, 2]}}],
    }
    out["forms"] = {}
    for name, seed_list in forms.items():
        board, notes = board_of(base / name, seed_list)
        light = board.world.seed
        now_sum, before_sum = sums(board, light)
        line = board.states[light].lines[0]
        now, before = np.asarray(line.now, dtype=object), np.asarray(line.before, dtype=object)
        e = vacuum_share(now, before, DEN)
        unit = 3 * DEN * T
        flat = [int(v) for v in e.reshape(-1)]
        centre = (0, 0, 0) if "hole" in name or name == "sea_1" else ((1, 0, 0) if "plus" in name else (2, 2, 2))
        kept48 = sum(1 for g in cube_48() if all(int(now[image_node(n, g, centre, board.shape)]) == int(now[n]) and int(before[image_node(n, g, centre, board.shape)]) == int(before[n]) for n in np.ndindex(*board.shape)))
        mirrors = [(p, s) for p, s in cube_48() if p == (0, 1, 2)]
        kept8 = sum(1 for g in mirrors if all(int(now[image_node(n, g, centre, board.shape)]) == int(now[n]) and int(before[image_node(n, g, centre, board.shape)]) == int(before[n]) for n in np.ndindex(*board.shape)))
        quanta, _frozen = board.quanta(light)
        out["forms"][name] = {
            "change_sum_now": now_sum, "change_sum_before": before_sum, "guard_would_refuse_with_weights": bool(now_sum or before_sum),
            "share_floor_per_node_hist": {str(k): v for k, v in sorted(dict(zip(*np.unique([f // unit for f in flat], return_counts=True), strict=True)).items())},
            "share_rounded_per_node_hist": {str(k): v for k, v in sorted(dict(zip(*np.unique([(f + unit // 2) // unit for f in flat], return_counts=True), strict=True)).items())},
            "engine_quanta_per_node_hist": {str(k): v for k, v in sorted(dict(zip(*np.unique(np.asarray(quanta, dtype=object).astype(int), return_counts=True), strict=True)).items())},
            "total_share_milli_quanta": (1000 * sum(flat)) // unit, "about": list(centre), "eight_mirrors_kept": kept8, "elements_of_48_kept": kept48,
            "notes": {k: v for k, v in notes.items() if k in ("wave", "at_light", "hole", "sea", "light_lay")},
        }
    # (2) the guard on a massless lay handed weights whose change moves a sum: lay.laid with weights on the light
    board, _notes = board_of(base / "guard", [{"sea": 1}])
    light = board.world.seed
    first = records.record_slice(board.families[light], 0).start
    kind = board.kind
    change = np.zeros(board.shape, dtype=object)
    change[(2, 2, 2)] = 100
    weights = np.zeros(board.shape, dtype=object)
    weights[(2, 2, 2)] = 1
    try:
        # the division act takes the uniform part out: a one-Node weight makes the change 0, so the guard passes with the lay 0
        found = laid(board, light, first, (change.astype(kind), np.zeros(board.shape, dtype=kind)), weights, None)
        out["division_act_one_node_weight"] = {"laid_change_sum_now": int(np.asarray(found[0], dtype=object).sum()), "laid_at_centre": int(found[0][(2, 2, 2)])}
    except ValueError as refusal:
        out["division_act_one_node_weight"] = {"refused": str(refusal)[:300]}
    # a packet with weights over 7 Nodes: the division act takes the sums out and the guard passes; its laid levels
    change = np.zeros(board.shape, dtype=object)
    weights = np.zeros(board.shape, dtype=object)
    for node, w in (((2, 2, 2), 8), ((1, 2, 2), 1), ((3, 2, 2), 1), ((2, 1, 2), 1), ((2, 3, 2), 1), ((2, 2, 1), 1), ((2, 2, 3), 1)):
        change[node], weights[node] = 10 * w, w
    found = laid(board, light, first, (change.astype(kind), np.zeros(board.shape, dtype=kind)), weights, None)
    out["division_act_seven_nodes"] = {"change_sum_before_act": int(change.sum()), "laid_sum_now": int(np.asarray(found[0], dtype=object).sum()),
                                       "laid_levels_centre_and_neighbour": [int(found[0][(2, 2, 2)]), int(found[0][(1, 2, 2)])]}
    # the guard's own refusal: a lay whose correction cannot take the sum out is impossible by construction (the division act
    # removes it exactly), so the guard is exercised by calling the guard function directly
    from event_universe.lay import guarded

    try:
        guarded("massless", True, 23436, 0, False)
        out["guard_direct"] = "passed (unexpected)"
    except ValueError as refusal:
        out["guard_direct"] = str(refusal)[:400]
    # (6) the seed list's refusals by name
    refusals = {
        "named_row": [{"sea": 1}, {"at": {"row": "point 2 0", "pair": [506298091, DEN], "centre": [2, 2, 2], "sigma_tenths": 12, "quanta": 10, "sense": 1}}],
        "one_node_body": [{"sea": 1}, {"at": {"pair": [506298091, DEN], "centre": [2, 2, 2], "sigma_tenths": 0, "quanta": 10, "sense": 1}}],
        "light_packet_with_width": [{"sea": 1}, {"at": {"pair": LIGHT, "centre": [2, 2, 2], "sigma_tenths": 12, "quanta": 1}}],
        "pair_of_no_row": [{"sea": 1}, {"at": {"pair": [7, DEN], "centre": [2, 2, 2], "sigma_tenths": 12, "quanta": 10, "sense": 1}}],
        "unknown_form": [{"sea": 1}, {"packet": 3}],
    }
    out["refusals"] = {}
    for name, seed_list in refusals.items():
        try:
            board_of(base / ("ref_" + name), seed_list)
            out["refusals"][name] = "ACCEPTED (unexpected)"
        except ValueError as refusal:
            out["refusals"][name] = str(refusal)[:260]
    (HERE / "lay_checks.json").write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
    print(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
