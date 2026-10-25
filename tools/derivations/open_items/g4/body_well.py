"""Hand g4, Addition 4: the fall of a packet in the well a body digs by its own form, within the laws, nothing held by
hand after the lay. The lay: the bare 9-cube torus at den 348,893, the light emptied (the start of the toy, named),
the heavy body a conjugate pair of the heavy lift "point 2 0" (g 200/269) at the centre Node, N quanta of each
sense on its two records through the click's own lay by the count (emission.laid_by_count, the law's birth at one
Node), so that its Wronskians cancel and the test body reads no electric potential while its form, 2 N quanta,
writes the volume holder at the centre; the test body 25 quanta of the composed point "point 2 -2" (g 0.69, in
the window) laid through the one lay act (lay.laid) as a packet of integer weights, the binomial C(6, 3 + x) per
axis (sigma^2 = 3 / 2 per axis, the width 2 sigma = 2.45 Links; no float anywhere), at rest in the local content,
--off Links from the centre along z, at the interval --lay-at (after the well has formed). Then the engine alone:
no hand on the volume, the swap at the top the law's own act (the pinned vacuum far from the bodies), 0 light so
0 clicks and 0 takes. The laws read on the run, each a number: (1) the conserved form, the test body's share total
per interval (the form read at the paces; exact at fixed paces, its drift the paces' change); (2) the run back
exact, step_inverse from the end to the lay's interval and every array against the state after the lay, MATCH or
the count of differing arrays; (3) the one-Link reach, the engine's own gate (tests/test_the_one_node.py), not
re-measured here; (4) the 48, the lay symmetric under the mirrors x -> 8 - x and y -> 8 - y and their exchange:
the count of Nodes where the test body's share differs from its image, 0 the law's; (5) the fixed count, the
integers one Node holds (the arrays' count, the same at every Node by construction); (6) the 128 bits, the largest
bit length of any level or remainder of any family; (7) integers only, the script's arithmetic and the readings;
(8) one act on every row alike and the two kinds of act, the acts table's gate (tests/test_the_acts_table.py), the
toy adding no act; (9) the exact take, the credit, birth and refused lines (0 of each without light); (10) no name
and no number in src/ (no edit). The fall: the test body's centroid along z in thousandths of a Link toward the
centre, its rms radius and the share within 1, 2, 3 Links of the peak, the content c at the centre, at the test
body's lay Node and at the Node between, the heavy pair's share within 1 Link of the centre, the turned Nodes.

    python tools/derivations/g4/body_well.py --heavy 400 --off 3 --lay-at 10 --intervals 110 --run-back
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from math import comb, isqrt
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from fall import GAMMA, ACTION, differing, manhattan, offsets, readings, record_share_int, snapshot_all  # noqa: E402

from event_universe import emission, records, share, world_files  # noqa: E402
from event_universe.core.paces import clock_alone  # noqa: E402
from event_universe.features import volume  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.lay import laid  # noqa: E402
from event_universe.take import Item  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402
from tests.laws_universe import light_emptied  # noqa: E402

BINOMIAL = 6  # the packet's profile per axis C(6, 3 + x), x in [-3, 3]: sigma^2 = 6 / 4 per axis, exact integers
WEIGHT_WALL = comb(BINOMIAL, BINOMIAL // 2) ** 3  # 20^3, the weight at the centre


def lay_binomial(board: Lattice, k: int, r: int, at: tuple[int, int, int], sense: int, quanta: int, kind: object) -> dict:
    """The test body: `quanta` quanta of the record `r` of the family `k` laid about `at` as the binomial packet at rest in the local content, through lay.laid, every level an integer: re_now = (A w_x w_y w_z) div 20^3, re_before = (re_now K) div W, im_before = sense (re_now S) div W, K = den Gamma^2 - (den - num) p_0(c)^2, W = den Gamma^2, S = isqrt(W^2 - K^2); A from the share by the one search isqrt."""
    family = board.families[k]
    num, den = family.pair
    first = records.record_slice(family, r).start
    shape = board.shape
    held = board.held[0]
    c_lay = int(volume.level_of(GAMMA, np.asarray(board.states[held].lines[0].now, dtype=object))[at])
    p0 = clock_alone(GAMMA, c_lay)
    w_rot = den * GAMMA * GAMMA
    k_rot = w_rot - (den - num) * p0 * p0
    s_rot = isqrt(w_rot * w_rot - k_rot * k_rot)
    unit_k = board.credit.units[k]
    off = offsets(shape, at)
    weights = np.zeros(shape, dtype=object)
    for where in np.ndindex(*shape):
        w = 1
        for a in range(3):
            d = int(off[a][where])
            w *= comb(BINOMIAL, BINOMIAL // 2 + d) if abs(d) <= BINOMIAL // 2 else 0
        weights[where] = w

    def levels(amplitude: int) -> tuple[np.ndarray, ...]:
        re_now = np.vectorize(lambda w: (amplitude * int(w)) // WEIGHT_WALL, otypes=[object])(weights)
        re_before = np.vectorize(lambda v: (int(v) * k_rot) // w_rot, otypes=[object])(re_now)
        im_before = np.vectorize(lambda v: sense * ((int(v) * s_rot) // w_rot), otypes=[object])(re_now)
        return re_now, re_before, np.zeros(shape, dtype=object), im_before

    content, factors = board.read(k, 1, r)

    def share_of(amplitude: int) -> int:
        re_now, re_before, im_now, im_before = levels(amplitude)
        remainder = board.states[k].lines[first].remainder
        lines = [records.Record(re_now, re_before, remainder), records.Record(im_now, im_before, remainder)]
        return int(np.asarray(share.family_share(family, lines, GAMMA, content, factors, board.unit), dtype=object).sum())

    amplitude = 2000
    for _ in range(4):
        amplitude = isqrt(amplitude * amplitude * quanta * unit_k // share_of(amplitude))
    re_now, re_before, im_now, im_before = levels(amplitude)
    laid(board, k, first, (re_now.astype(kind), re_before.astype(kind)), None, None)
    laid(board, k, first + 1, (im_now.astype(kind), im_before.astype(kind)), None, None)
    total = int(record_share_int(board, k, r).sum())
    return {"amplitude": amplitude, "c_lay": c_lay, "p0_lay": p0, "cos_milli": (1000 * k_rot) // w_rot, "sin_milli": (1000 * s_rot) // w_rot, "share_total": total, "unit": unit_k, "quanta_milli": (1000 * total) // unit_k, "nodes_laid": int(sum(1 for v in re_now.reshape(-1) if int(v) != 0))}


def largest_bits(board: Lattice) -> tuple[int, str]:
    found, where = 0, ""
    for fam, st in zip(board.families, board.states, strict=True):
        for n, line in enumerate(st.lines):
            for name, arr in (("now", line.now), ("before", line.before), ("remainder", line.remainder)):
                b = max(int(abs(int(v))).bit_length() for v in np.asarray(arr, dtype=object).reshape(-1))
                if b > found:
                    found, where = b, f"{fam.name} line {n} {name}"
        for n, w in enumerate(st.write_remainders):
            b = max(int(abs(int(v))).bit_length() for v in np.asarray(w, dtype=object).reshape(-1))
            if b > found:
                found, where = b, f"{fam.name} write {n}"
        for rr, row in enumerate(st.phases):
            for n, line in enumerate(row):
                for name, arr in (("now", line.now), ("before", line.before), ("remainder", line.remainder)):
                    b = max(int(abs(int(v))).bit_length() for v in np.asarray(arr, dtype=object).reshape(-1))
                    if b > found:
                        found, where = b, f"{fam.name} row {rr} phase {n} {name}"
    return found, where


def integers_per_node(board: Lattice) -> int:
    count = 0
    for st in board.states:
        count += 3 * len(st.lines) + len(st.write_remainders) + 3 * sum(len(row) for row in st.phases)
    return count


def mirror_defects(s: np.ndarray) -> dict[str, int]:
    """The count of Nodes where the test body's share differs from its image under the mirrors about the lay axis (x -> 8 - x, y -> 8 - y) and the exchange x <-> y: the cube's symmetries the lay keeps, 0 the law's."""
    a = np.asarray(s, dtype=object)
    found = {}
    found["x_mirror"] = int((a != a[::-1, :, :]).sum())
    found["y_mirror"] = int((a != a[:, ::-1, :]).sum())
    found["xy_exchange"] = int((a != np.transpose(a, (1, 0, 2))).sum())
    return found


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--den", type=int, default=348893)
    parser.add_argument("--cube", type=int, default=9)
    parser.add_argument("--heavy", type=int, default=400, help="quanta of each sense of the heavy pair at the centre")
    parser.add_argument("--heavy-family", default="point 2 0")
    parser.add_argument("--test-family", default="point 2 -2")
    parser.add_argument("--quanta", type=int, default=25)
    parser.add_argument("--off", type=int, default=3)
    parser.add_argument("--lay-at", type=int, default=10, help="the interval the test body is laid at, after the well has formed")
    parser.add_argument("--intervals", type=int, default=110)
    parser.add_argument("--run-back", action="store_true")
    parser.add_argument("--tag", default="")
    args = parser.parse_args()
    tag = args.tag or f"body_well_h{args.heavy}_q{args.quanta}_o{args.off}_l{args.lay_at}_n{args.intervals}"
    folder = Path(f"/dev/shm/tmp/g4_{tag}")
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "u.json").write_text(json.dumps({"integers": {"den": args.den, "node_clock": GAMMA, "quantum_action": ACTION}}))
    (folder / "w.json").write_text(json.dumps({"universe": "u.json", "shape": [args.cube] * 3, "intervals": args.intervals}))
    world_files.REPOSITORY_ROOT = folder
    lines_out: list[dict] = []
    board = Lattice(load_world(folder / "w.json"), output=lines_out.append)
    kind = board.kind
    light_emptied(board)
    names = [f.name for f in board.families]
    kh, kt = names.index(args.heavy_family), names.index(args.test_family)
    centre = (args.cube // 2,) * 3
    at = (centre[0], centre[1], (centre[2] - args.off) % args.cube)
    mid = (centre[0], centre[1], (centre[2] - 1) % args.cube)
    den_h = board.families[kh].pair[1]
    board.born_point(kh)
    board.born_point(kt)
    for record, sense in ((0, 1), (1, -1)):  # the conjugate pair at one Node, the click's own lay by the count
        emission.laid_by_count(board, Item(kh, args.heavy, (centre,), (den_h, den_h), sense=sense, record=record))
    heavy_total = int(record_share_int(board, kh, 0).sum()) + int(record_share_int(board, kh, 1).sum())
    header = {
        "event": "header", "den": args.den, "cube": args.cube, "heavy_family": args.heavy_family, "heavy_pair": list(board.families[kh].pair),
        "heavy_g_milli": (1000 * (board.families[kh].pair[1] - board.families[kh].pair[0])) // board.families[kh].pair[1],
        "test_family": args.test_family, "test_pair": list(board.families[kt].pair),
        "test_g_milli": (1000 * (board.families[kt].pair[1] - board.families[kt].pair[0])) // board.families[kt].pair[1],
        "heavy_quanta_each": args.heavy, "heavy_share_total": heavy_total, "heavy_unit": board.credit.units[kh],
        "heavy_quanta_milli": (1000 * heavy_total) // board.credit.units[kh], "test_quanta": args.quanta, "off": args.off, "lay_at": args.lay_at,
        "width_bits": board.world.width.bit_length() if hasattr(board.world.width, "bit_length") else int(board.world.width), "kind": str(kind),
        "amplitude_bound": board.world.amplitude_bound, "integers_per_node": integers_per_node(board), "intervals": args.intervals,
    }
    print(json.dumps(header), flush=True)
    rows = [header]
    t0 = time.time()
    laid_state = None
    test_lay = None
    marks = {0, 1, 2, 3, 5, 10, 11, 12, 13, 15, 20, 25, 30, 40, 50, 60, 75, 90, 100, 110, 125, 150, 200, args.intervals}
    shape = board.shape

    def read_all(interval: int) -> dict:
        held = board.held[0]
        c = volume.level_of(GAMMA, np.asarray(board.states[held].lines[0].now, dtype=object))
        s_h = np.asarray(record_share_int(board, kh, 0), dtype=object) + np.asarray(record_share_int(board, kh, 1), dtype=object)
        s_h = np.where(s_h > 0, s_h, 0)
        total_h = int(sum(int(v) for v in s_h.reshape(-1)))
        d_c = manhattan(shape, centre)
        within1 = int(sum(int(v) for v, d in zip(s_h.reshape(-1), d_c.reshape(-1)) if int(d) <= 1))
        bits, where = largest_bits(board)
        row = {
            "event": "reading", "interval": interval, "turned": int(board.turned.sum()), "seconds": round(time.time() - t0, 1),
            "c_centre": int(c[centre]), "c_mid": int(c[mid]), "c_test": int(c[at]), "c_min": int(min(int(v) for v in c.reshape(-1))), "c_max": int(max(int(v) for v in c.reshape(-1))),
            "heavy_share_total": total_h, "heavy_within1_milli": (1000 * within1) // total_h if total_h else None,
            "largest_bits": bits, "largest_at": where,
        }
        if test_lay is not None:
            found = readings(board, kt, 0, at)
            s_t = np.asarray(record_share_int(board, kt, 0), dtype=object)
            found["mirror_defects"] = mirror_defects(s_t)
            row["test"] = found
        return row

    rows.append(read_all(0))
    print(json.dumps(rows[-1]), flush=True)
    for step in range(1, args.intervals + 1):
        if step - 1 == args.lay_at:  # the test body laid at the start of this interval
            test_lay = lay_binomial(board, kt, 0, at, 1, args.quanta, kind)
            laid_state = snapshot_all(board)
            rows.append({"event": "lay", "interval": board.interval, "test_lay": test_lay})
            print(json.dumps(rows[-1]), flush=True)
            rows.append(read_all(board.interval))
            print(json.dumps(rows[-1]), flush=True)
        try:
            board.step()
        except RuntimeError as named:  # the engine's refusal by name: logged, the run stopped there
            rows.append({"event": "refused", "interval": board.interval, "cause": str(named)[:400]})
            print(json.dumps(rows[-1]), flush=True)
            break
        row = read_all(board.interval)
        rows.append(row)
        if board.interval in marks:
            print(json.dumps(row), flush=True)
    end = board.interval
    credits = [l for l in lines_out if isinstance(l, dict)]
    summary = {"event": "summary", "end_interval": end, "seconds": round(time.time() - t0, 1), "output_lines": len(lines_out),
               "credit_lines": sum(1 for l in credits if l.get("event") == "credit"), "birth_lines": sum(1 for l in credits if l.get("event") == "birth"),
               "refused_lines": sum(1 for l in credits if l.get("event") == "refused"), "integers_per_node": integers_per_node(board)}
    if args.run_back and laid_state is not None and end > args.lay_at:
        t1 = time.time()
        for _ in range(end - args.lay_at):
            board.step_inverse()
        diff = differing(laid_state, snapshot_all(board))
        summary["run_back"] = "MATCH" if not diff else f"MISMATCH in {len(diff)} arrays: {[str(d) for d in diff[:6]]}"
        summary["run_back_intervals"] = end - args.lay_at
        summary["run_back_seconds"] = round(time.time() - t1, 1)
    rows.append(summary)
    print(json.dumps(summary), flush=True)
    with (HERE / f"{tag}.jsonl").open("w") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")


if __name__ == "__main__":
    main()
