"""Hand r4 (2026-10-25, the follow-up): the mended riding engine (U24_RIDES=2; argv 0 runs the branch's path beside it)
measured under the laws of Addition 4: (A) MATCH through a top on the uniform gapped torus (the sea on every Node, every
act but the close, 80 intervals forward with a snapshot per interval, 80 back, the snapshots compared at every interval);
(B) MATCH through births on the hole seed (every act and the board's own close, 60 forward, 60 back), with the clicks'
readings: the births (interval, children, senses, their sum: the charge), the books per family (share, quanta, count,
deficit, drift: the exact take); (C) the cube's 48 on the sea plus one quantum at the centre (sea_plus_one(CENTRE)) with
every act and the close, 40 intervals, every array against its 48 images (tests/laws_universe.carried), the unequal entries
counted per kind of line; (D) the width: the largest integer of the state in bits over the runs; (E) the conserved form at
fixed reads on the chain (tools/derivations/open_items/H-Every-Line-Rides-4/ride_chain.py's stepper at the content 500 held 1,200 intervals): the share
total at the start and the end under the plain and the riding line. Outputs ride_mended_<flag>.json. Integers only."""

import itertools
import json
import os
import sys
from pathlib import Path

FLAG = sys.argv[1] if len(sys.argv) > 1 else "2"
os.environ["U24_RIDES"] = FLAG
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(HERE))

import numpy as np  # noqa: E402

from event_universe import flux, seed, world_files  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402
from tests.laws_universe import CENTRE, bare_torus, carried, node_arrays, sea_plus_one, uniform_sea  # noqa: E402

AT = (0, 0, 0)


def board_of(folder, intervals, lay):
    folder.mkdir(parents=True, exist_ok=True)
    world_files.REPOSITORY_ROOT = folder
    lines = []
    kept = seed.uniform_seed
    if lay is not None:
        seed.uniform_seed = lay
    try:
        board = Lattice(load_world(bare_torus(folder, 3, intervals)), output=lines.append)
    finally:
        seed.uniform_seed = kept
    return board, lines


def unequal(a, b):
    total = 0
    for key in a:
        if key not in b:
            total += sum(int(np.asarray(x, dtype=object).size) for x in a[key])
            continue
        for x, y in zip(a[key], b[key], strict=True):
            total += int((np.asarray(x, dtype=object) != np.asarray(y, dtype=object)).sum())
    return total + sum(sum(int(np.asarray(x, dtype=object).size) for x in b[key]) for key in b if key not in a)


def widest(arrays):
    return max(max(int(v).bit_length() for v in np.asarray(x, dtype=object).reshape(-1)) for value in arrays.values() for x in value)


def part_a(folder, forward=80):
    board, _lines = board_of(folder / "a", forward + 10, uniform_sea)
    snapshots = [node_arrays(board)]
    tops, bits, xs = [], 0, []
    for t in range(1, forward + 1):
        board.advanced_to_the_close()
        snapshots.append(node_arrays(board))
        bits = max(bits, widest(snapshots[-1]))
        if board.turned.any():
            tops.append((t, int(board.turned.sum())))
        xs.append(int(board.states[board.held[0]].lines[0].now[AT]))
    matched, first_miss, unequal_at = 0, None, {}
    for t in range(forward, 0, -1):
        board.step_inverse()
        bad = unequal(node_arrays(board), snapshots[t - 1])
        matched += bad == 0
        if bad and first_miss is None:
            first_miss = t
        if bad and len(unequal_at) < 6:
            unequal_at[t - 1] = bad
    return {
        "intervals_forward": forward, "tops_turned": tops, "X_largest": max(xs), "X_at_end": xs[-1],
        "intervals_matched_back": matched, "first_unmatched_pre_state": first_miss, "unequal_entries_sample": unequal_at,
        "largest_state_integer_bits": bits,
    }


def births_of(lines):
    found = []
    for line in lines:
        text = json.dumps(line, default=str)
        if "senses" in line or ("sense" in text and "children" in text):
            found.append(line)
    return found


def part_b(folder, forward=60):
    board, lines = board_of(folder / "b", forward + 10, None)
    snapshots = [node_arrays(board)]
    bits = 0
    for _t in range(1, forward + 1):
        board.step()
        snapshots.append(node_arrays(board))
        bits = max(bits, widest(snapshots[-1]))
    born = {int(k): [int(i) for i in v] for k, v in board.born_at.items()}
    births = births_of(lines)
    senses, takes = [], []
    for line in births:
        value = line.get("senses")
        if isinstance(value, list):
            senses.append([int(x) for x in value])
        takes.append({k: line.get(k) for k in ("interval", "children", "senses", "taken", "walls", "excess") if k in line})
    from event_universe import registry

    books = {}
    for i in board.order:  # the books per family read directly (Lattice.books refuses a family with no record: the branch's own min() on an empty family)
        name = board.families[i].name
        standing = registry.records_of(board.families[i], board.states[i].lines)
        total = board.total_share(i)[0] if standing else None
        laid = board.laid.get(i)
        books[name] = {
            "records": int(standing), "share_total": total, "quanta_on_board": int(board.quanta(i)[0].sum()) if standing else 0,
            "count_in_books": int(board.credit.counts[i]), "deficit": int(board.credit.deficits.get(i, 0)),
            "drift_from_laid": None if total is None or laid is None else int(total - laid),
        }
    counts = {name: book["quanta_on_board"] for name, book in books.items()}
    matched, first_miss, unequal_at = 0, None, {}
    for t in range(forward, 0, -1):
        board.step_inverse()
        bad = unequal(node_arrays(board), snapshots[t - 1])
        matched += bad == 0
        if bad and first_miss is None:
            first_miss = t
        if bad and len(unequal_at) < 6:
            unequal_at[t - 1] = bad
    return {
        "intervals_forward": forward, "points_born_at": born, "births_lines": len(births), "birth_senses": senses[:12],
        "charge_sum_over_births": sum(sum(s) for s in senses), "books_at_end": books, "quanta_at_end": counts, "takes": takes[:8],
        "X_at_end_forward": int(snapshots[-1][(board.held[0], "line", 0)][0][AT]),
        "intervals_matched_back": matched, "first_unmatched_pre_state": first_miss, "unequal_entries_sample": unequal_at,
        "largest_state_integer_bits": bits, "birth_line_keys": sorted(set(k for line in births for k in line))[:16],
    }


def part_c(folder, forward=40):
    board, _lines = board_of(folder / "c", forward + 10, sea_plus_one(CENTRE))
    for _t in range(forward):
        board.step()
    arrays = node_arrays(board)
    held = board.held
    kinds = {}
    for permutation in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            image = carried(arrays, (tuple(permutation), tuple(signs)))
            for key in arrays:
                bad = sum(int((np.asarray(x, dtype=object) != np.asarray(y, dtype=object)).sum()) for x, y in zip(arrays[key], image[key], strict=True))
                family, kind = key[0], key[1]
                name = board.families[family].name
                label = f"{name} {kind} {key[2]}" + (f" row {key[3]}" if len(key) > 3 else "")
                kinds[label] = kinds.get(label, 0) + bad
    scalar = {k: v for k, v in kinds.items() if v == 0}
    broken = {k: v for k, v in kinds.items() if v}
    return {"intervals": forward, "elements": 48, "arrays_exact_under_all_48": len(scalar), "arrays_broken": broken, "exact_arrays": sorted(scalar)[:40], "held_rows": [board.families[h].name for h in held]}


def part_e():
    import ride_chain as chain

    found = {}
    for name, ride in (("plain", 0), ("ride", 2)):
        now, before = chain.lay_wave()
        _p0, _pa, _reach, w, _s = chain.rule_at(0)
        content = 500
        rem = [(w * chain.volume_at(content)) // 2 if ride else w // 2] * chain.N
        start = chain.share_total(now, before, content)
        for _t in range(1200):
            now, before, rem = chain.step(now, before, rem, content, content, ride)
        end = chain.share_total(now, before, content)
        found[name] = {"content": content, "share_start": start, "share_end": end, "drift": end - start, "drift_per_10^6": (end - start) * 10 ** 6 // start}
    return found


if __name__ == "__main__":
    folder = Path(os.environ.get("TMPDIR", "/dev/shm/tmp")) / f"r4_mended_{FLAG}"
    found = {"flag": FLAG, "rides": flux.RIDES, "mended": getattr(flux, "MENDED", None)}
    out = HERE / f"ride_mended_{FLAG}.json"
    for name, part in (("A", lambda: part_a(folder)), ("B", lambda: part_b(folder)), ("C", lambda: part_c(folder)), ("E", part_e)):
        found[name] = part()
        out.write_text(json.dumps(found, indent=1, default=str), encoding="utf-8")
    print(json.dumps(found, indent=1, default=str))
