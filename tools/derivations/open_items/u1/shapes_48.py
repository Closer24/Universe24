"""U1 (brief u, item (b)): the cube's 48 on the three shapes, measured on the engine's own carry (tests/test_the_board_is_the_cube_48.carried, apart, cube_48, turns_of). (1) The representation each object's lines carry: every line of every family set to its own constant level on the bare 3-cube at den 1,021, the carry applied for each of the 48 signed permutations, the induced signed permutation of the lines read back (which line each lands on, with which sign), its character per object, decomposed by the integer inner product into the cube's irreducible characters computed from the matrices (A_1g, A_1u, E_g, T_1u, T_2g), beside the metric's 10 (1 + 3 + 6) and the symmetric tensor's 6; whether any line leaves its object. (2) The run: the hole seed on the gapped 3-cube for 12 intervals and the sea plus one at the origin for 8, every one of the 47 non-trivial elements applied at every interval, the elements under which the carried state equals the state counted, the differences tallied per object. (3) The reflection on the births: the sea plus one at (1, 0, 0) and its image under x -> -x run 8 intervals, the carried run against the other bit for bit, and the births' senses at the image Nodes read from the birth lines (kept, or exchanged). Integer readings only; the output beside the script as shapes_48.json.

Run: PYTHONPATH=<worktree>/src TMPDIR=/dev/shm/tmp python tools/derivations/u1/shapes_48.py"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from event_universe import records, registry, seed, world_files  # noqa: E402
from event_universe.core.ports import AXES  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402
from tests.laws_universe import sea_plus_one, small_universe  # noqa: E402
from tests.test_the_board_is_the_cube_48 import (  # noqa: E402
    IDENTITY,
    apart,
    axis_map,
    carried,
    cube_48,
    turns_of,
)

GROUP = cube_48()
SIDE = 3


def det(m) -> int:  # type: ignore[no-untyped-def]
    pi, s = axis_map(m)
    inversions = sum(1 for a in range(AXES) for b in range(a + 1, AXES) if pi[a] > pi[b])
    return (-1) ** inversions * s[0] * s[1] * s[2]


def characters() -> dict[str, list[int]]:
    """The characters of the cube's irreducible representations from the 48 matrices, integers: A_1g 1, A_1u det, T_1u tr m, E_g (fixed axes - 1), T_2g (the off-diagonal pairs kept, with the sign product); beside them the permutation of the axes (A_1g + E_g), the symmetric tensor (6) and the metric (10 = 1 + 3 + 6)."""
    found: dict[str, list[int]] = {k: [] for k in ("A_1g", "A_1u", "T_1u", "T_1g", "E_g", "T_2g", "perm3", "sym2", "metric10", "potential4")}
    for m in GROUP:
        pi, s = axis_map(m)
        trace = int(np.trace(m))
        fixed = sum(1 for a in range(AXES) if pi[a] == a)
        pairs = sum(s[a] * s[b] for a in range(AXES) for b in range(a + 1, AXES) if {pi[a], pi[b]} == {a, b})
        sym2 = (trace * trace + int(np.trace(m @ m))) // 2
        d = det(m)
        found["A_1g"].append(1)
        found["A_1u"].append(d)
        found["T_1u"].append(trace)
        found["T_1g"].append(d * trace)
        found["E_g"].append(fixed - 1)
        found["T_2g"].append(pairs)
        found["perm3"].append(fixed)
        found["sym2"].append(sym2)
        found["metric10"].append(1 + trace + sym2)
        found["potential4"].append(1 + trace)
    return found


def decomposed(chi: list[int], irreps: dict[str, list[int]]) -> dict[str, int]:
    """The multiplicities by the integer inner product over the 48, the division exact (its remainder named where not)."""
    found = {}
    for name in ("A_1g", "A_1u", "E_g", "T_1u", "T_1g", "T_2g"):
        total = sum(a * b for a, b in zip(chi, irreps[name], strict=True))
        q, r = divmod(total, len(GROUP))
        found[name] = q if r == 0 else f"{total}/48"
    return found


def constant_board(folder: Path) -> Lattice:
    """The bare 3-cube with every point's rows born and every line of every family set to its own constant level, the remainders kept."""
    folder.mkdir(parents=True, exist_ok=True)
    world_files.REPOSITORY_ROOT = folder
    small_universe(folder)
    (folder / "w.json").write_text(json.dumps({"universe": "u.json", "shape": [SIDE] * 3, "intervals": 4}), encoding="utf-8")
    board = Lattice(load_world(folder / "w.json"))
    for index in board.turning:
        board.born_point(index)
    value = 1
    for state in board.states:
        for n, line in enumerate(state.lines):
            state.lines[n] = records.Record(np.full(board.shape, value, dtype=object), np.full(board.shape, value, dtype=object), line.remainder)
            value += 1
        for r, row in enumerate(state.phases):
            for n, line in enumerate(row):
                state.phases[r][n] = records.Record(np.full(board.shape, value, dtype=object), np.full(board.shape, value, dtype=object), line.remainder)
                value += 1
    return board


def induced(board: Lattice) -> dict:  # type: ignore[type-arg]
    """Per family the induced signed permutation of its lines under every element, its character and its decomposition; whether a line left its family."""
    found: dict = {}  # type: ignore[type-arg]
    irreps = characters()
    centre = (1, 1, 1)
    for index, family in enumerate(board.families):
        state = board.states[index]
        own = [int(line.now[centre]) for line in state.lines]
        own_phase = [int(line.now[centre]) for row in state.phases for line in row]
        chi_lines, chi_phase, left = [], [], 0
        maps = []
        for m in GROUP:
            image = carried(board, m, None)
            lines, _writes, phases = image[index]
            got = [int(np.asarray(t[0], dtype=object)[centre]) for t in lines]
            chi = 0
            table = []
            for k, v in enumerate(own):
                hits = [(t, 1 if g == v else -1) for t, g in enumerate(got) if abs(g) == v]
                if len(hits) != 1:
                    left += 1
                    continue
                t, sign = hits[0]
                table.append((k, t, sign))
                chi += sign if t == k else 0
            chi_lines.append(chi)
            got_phase = [int(np.asarray(t[0], dtype=object)[centre]) for row in phases for t in row]
            chi_p = 0
            for k, v in enumerate(own_phase):
                hits = [(t, 1 if g == v else -1) for t, g in enumerate(got_phase) if abs(g) == v]
                if len(hits) != 1:
                    left += 1
                    continue
                t, sign = hits[0]
                chi_p += sign if t == k else 0
            chi_phase.append(chi_p)
            if np.array_equal(m, np.diag([-1, 1, 1])):
                maps = table
        entry = {"lines": len(own), "lines_left_or_split": left, "character_sum": sum(chi_lines), "decomposition": decomposed(chi_lines, irreps)}
        if own_phase:
            entry["phase_lines"] = len(own_phase)
            entry["phase_decomposition"] = decomposed(chi_phase, irreps)
        entry["image_under_x_reflection"] = maps[: 8]
        found[family.name] = entry
    found["irreducible_checks"] = {
        "sym2_equals_A1g_plus_Eg_plus_T2g_on_48": all(a == 1 + e + t for a, e, t in zip(irreps["sym2"], irreps["E_g"], irreps["T_2g"], strict=True)),
        "metric10": decomposed(irreps["metric10"], irreps),
        "sym2": decomposed(irreps["sym2"], irreps),
        "potential4": decomposed(irreps["potential4"], irreps),
        "perm3": decomposed(irreps["perm3"], irreps),
        "plane_senses_kept_2_scalars": decomposed([2] * 48, irreps),
        "plane_senses_exchanged_re_plus_im_det": decomposed([1 + d for d in irreps["A_1u"]], irreps),
        "elements": len(GROUP),
        "reflections": sum(1 for d in irreps["A_1u"] if d < 0),
    }
    return found


def board_of(folder: Path, seeder, intervals: int) -> tuple[Lattice, list]:  # type: ignore[no-untyped-def, type-arg]
    folder.mkdir(parents=True, exist_ok=True)
    world_files.REPOSITORY_ROOT = folder
    small_universe(folder)
    (folder / "w.json").write_text(json.dumps({"universe": "u.json", "shape": [SIDE] * 3, "intervals": intervals}), encoding="utf-8")
    kept, lines = seed.uniform_seed, []  # type: ignore[var-annotated]
    if seeder is not None:
        seed.uniform_seed = seeder
    try:
        board = Lattice(load_world(folder / "w.json"), output=lines.append)
    finally:
        seed.uniform_seed = kept
    return board, lines


def run_invariant(folder: Path, seeder, intervals: int) -> dict:  # type: ignore[no-untyped-def, type-arg]
    """The seed invariant under the 48 run: per interval the count of the 47 non-trivial elements under which the carried state is the state, the differences tallied per family and part."""
    board, lines = board_of(folder, seeder, intervals)
    group = [m for m in GROUP if not np.array_equal(m, IDENTITY)]
    turns, per_interval, tally = turns_of(board, None), [], {}
    for _ in range(intervals):
        board.step()
        turns = turns_of(board, turns)
        state = carried(board, IDENTITY)
        held = 0
        for m in group:
            found = apart(carried(board, m, turns), state)
            if not found:
                held += 1
            for path, _node, _units in found:
                key = f"{board.families[path[0]].name} part {path[1]}"
                tally[key] = tally.get(key, 0) + 1
        births = [tuple(x["nodes"][0]) for x in lines if x.get("event") == "birth" and x["interval"] == board.interval]
        per_interval.append({"interval": board.interval, "held_of_47": held, "births": len(births), "turned_nodes": int(np.asarray(board.turned).sum())})
    return {"per_interval": per_interval, "differences_by_object": tally, "births_total": sum(1 for x in lines if x.get("event") == "birth"), "refused_total": sum(1 for x in lines if x.get("event") == "refused")}


def run_reflected(folder: Path, intervals: int) -> dict:  # type: ignore[type-arg]
    """The sea plus one at (1, 0, 0) and at its image under x -> -x: the carried run against the other, and the births' senses at the image Nodes."""
    m = np.diag([-1, 1, 1])
    at = (1, 0, 0)
    image = tuple(int(v) for v in np.mod(m @ np.array(at), SIDE))
    board, lines = board_of(folder / "a", sea_plus_one(at), intervals)
    other, other_lines = board_of(folder / "b", sea_plus_one(image), intervals)
    turns, per_interval = turns_of(board, None), []
    for _ in range(intervals):
        board.step()
        other.step()
        turns = turns_of(board, turns)
        found = apart(carried(board, m, turns), carried(other, IDENTITY))
        per_interval.append({"interval": board.interval, "differences": len(found)})
    births = [x for x in lines if x.get("event") == "birth"]
    other_births = [x for x in other_lines if x.get("event") == "birth"]
    kept = exchanged = unmatched = 0
    for b in births:
        node = np.array(b["nodes"][0])
        target = [int(v) for v in np.mod(m @ node, SIDE)]
        twin = [o for o in other_births if o["interval"] == b["interval"] and o["nodes"][0] == target and o["children"] == b["children"]]
        if len(twin) != 1:
            unmatched += 1
            continue
        if twin[0]["senses"] == b["senses"]:
            kept += 1
        elif twin[0]["senses"] == [-s for s in b["senses"]]:
            exchanged += 1
        else:
            unmatched += 1
    im_entries = 0
    for index in board.turning:
        for n, line in enumerate(board.states[index].lines):
            if n % 2 == 1:
                im_entries += int((np.asarray(line.now, dtype=object) != 0).sum()) + int((np.asarray(line.before, dtype=object) != 0).sum())
    return {
        "image_node": list(image),
        "per_interval": per_interval,
        "births": len(births),
        "senses_kept_at_the_image": kept,
        "senses_exchanged_at_the_image": exchanged,
        "unmatched": unmatched,
        "im_level_entries_an_exchange_would_negate": im_entries,
        "birth_lines_sample": [{k: b[k] for k in ("interval", "children", "senses", "nodes")} for b in births[:4]],
    }


def main() -> None:
    base = Path("/dev/shm/tmp/u1_48")
    out = {"representation_on_the_engines_carry": induced(constant_board(base / "constant"))}
    out["hole_seed_gapped_12"] = run_invariant(base / "hole", None, 12)
    out["sea_plus_one_origin_gapped_8"] = run_invariant(base / "sea", sea_plus_one((0, 0, 0)), 8)
    out["reflection_on_the_births_8"] = run_reflected(base / "refl", 8)
    (HERE / "shapes_48.json").write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
    print(json.dumps(out, default=str))


if __name__ == "__main__":
    main()
