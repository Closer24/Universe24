"""m2 (hand y1): the flagged engine (U24_METRIC=1) on the bare 3-cube hole seed of the tests' small universe, N intervals forward through the births at 4 and the turns: per interval the count of integers per Node, the largest bit length, the ten lines' board sums (the write of the six), the flux lines at the origin's six face neighbours and the shears at the twelve edge Nodes (the T_1u and T_2g patterns), the charge (SUM W over the plane records), light's lattice momentum per axis, the cube's 48 on the ten (the levels of every line, the even remainders exactly, the odd remainders by the complement at their own wall), then the clicks (the births' take and senses, the credits' momentum pairs, points and beats) and the run back MATCH by tools/back_in_time.verdict on a second board of the same seed. Integers only."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[2]))  # tools/back_in_time
import y1lib  # noqa: E402

assert os.environ.get("U24_METRIC") == "1", "run with U24_METRIC=1"
from event_universe import readings, records  # noqa: E402
from event_universe.core.rule3 import wall_of  # noqa: E402

INTERVALS = int(sys.argv[1]) if len(sys.argv) > 1 else 12
ORIGIN = (0, 0, 0)
FACES = [(1, 0, 0), (2, 0, 0), (0, 1, 0), (0, 2, 0), (0, 0, 1), (0, 0, 2)]
EDGES = [(1, 1, 0), (1, 2, 0), (2, 1, 0), (2, 2, 0), (0, 1, 1), (0, 1, 2), (0, 2, 1), (0, 2, 2), (1, 0, 1), (2, 0, 1), (1, 0, 2), (2, 0, 2)]
LINE_NAMES = ["g_00", "g_xx", "g_yy", "g_zz", "g_0x", "g_0y", "g_0z", "g_xy", "g_yz", "g_zx"]
PAIRS = [(0, 1), (1, 2), (2, 0)]


def carried_volume_line(number: int, pi, s) -> tuple[int, int]:
    """The image line of the volume row's line `number` under (pi, s) and the sign it carries: g_00 to itself; g_aa to g_pi(a)pi(a) with no sign; g_0a to g_0pi(a) with s_a; g_ab to g_pi(a)pi(b) with s_a s_b."""
    if number == 0:
        return 0, 1
    if 1 <= number <= 3:
        return 1 + pi[number - 1], 1
    if 4 <= number <= 6:
        a = number - 4
        return 4 + pi[a], s[a]
    a, b = PAIRS[number - 7]
    image = tuple(sorted((pi[a], pi[b])))
    position = [tuple(sorted(p)) for p in PAIRS].index(image)
    return 7 + position, s[a] * s[b]


def the_48(board) -> dict:
    """The elements of the 48 under which the board equals its image: the levels of every line of every family (the metric's ten carried as one object, the sign's rows as scalar + vector, the planes as scalars), the even remainders and write remainders exactly, the odd remainders by the complement wall - 1 - r at the line's own wall (w for a plain line, w (X_now + X_before) for a riding line of the metric) and by the lay's gauge (wall - r) mod wall, counted apart."""
    gamma, unit = board.world.node_clock, board.unit
    volume = board.held[0]
    time = board.states[volume].lines[0]
    ride_wall = wall_of(board.families[volume].pair[1], gamma, unit) * (
        np.asarray(time.now, dtype=object) + np.asarray(time.before, dtype=object)
    )
    levels_ok = even_ok = odd_complement_ok = odd_gauge_ok = 0
    for pi, s in y1lib.signed_permutations():
        good_levels = good_even = good_odd_c = good_odd_g = True
        for i, family in enumerate(board.families):
            state = board.states[i]
            w = wall_of(family.pair[1], gamma, unit)
            for n, line in enumerate(state.lines):
                if i == volume:
                    m, sign = carried_volume_line(n, pi, s)
                    wall = ride_wall if n >= 1 else w
                elif family.wronskian:
                    width = family.width
                    row, position = divmod(n, width)
                    if position == 0:
                        m, sign = n, 1
                    else:
                        a = position - 1
                        m, sign = row * width + 1 + pi[a], s[a]
                    wall = w
                else:
                    m, sign, wall = n, 1, w
                target = state.lines[m]
                for part in ("now", "before"):
                    img = y1lib.image_of(getattr(line, part), pi, s)
                    if not np.array_equal(sign * img, np.asarray(getattr(target, part), dtype=object)):
                        good_levels = False
                r_img = y1lib.image_of(line.remainder, pi, s)
                r_target = np.asarray(target.remainder, dtype=object)
                wall_img = y1lib.image_of(wall, pi, s) if np.ndim(wall) else wall
                if sign == 1:
                    if not np.array_equal(r_img, r_target):
                        good_even = False
                else:
                    if not np.array_equal(wall_img - 1 - r_img, r_target):
                        good_odd_c = False
                    if not np.array_equal((wall_img - r_img) % wall_img, r_target):
                        good_odd_g = False
                if state.write_remainders and i in board.write_walls:  # the walls stand after the first write
                    ww = board.write_walls[i][n]
                    ww_img = y1lib.image_of(ww, pi, s) if np.ndim(ww) else ww
                    wr_img = y1lib.image_of(state.write_remainders[n], pi, s)
                    wr_target = np.asarray(state.write_remainders[m], dtype=object)
                    if sign == 1:
                        if not np.array_equal(wr_img, wr_target):
                            good_even = False
                    else:
                        if not np.array_equal(ww_img - 1 - wr_img, wr_target):
                            good_odd_c = False
                        if not np.array_equal((ww_img - wr_img) % ww_img, wr_target):
                            good_odd_g = False
        levels_ok += good_levels
        even_ok += good_even
        odd_complement_ok += good_odd_c
        odd_gauge_ok += good_odd_g
    return {"levels": levels_ok, "even_remainders": even_ok, "odd_remainders_complement": odd_complement_ok, "odd_remainders_lay_gauge": odd_gauge_ok}


def main() -> None:
    lines: list = []
    board = y1lib.board_of(Path("/dev/shm/tmp/y1_m2"), lines)
    volume, sign, light = board.held[0], board.held[1], board.world.seed
    assert board.families[volume].lines == 10, board.families[volume].lines
    out: dict = {
        "universe": {"den": 1021, "Gamma": 1000, "T": 36000, "G": board.unit},
        "volume_row": {"pair": list(board.families[volume].pair), "lines": board.families[volume].lines, "flux": board.families[volume].flux,
                       "write_walls_at_start": [int(np.asarray(w, dtype=object).reshape(-1)[0]) for w in board.write_walls.get(volume, board.walls(volume))]},
        "per_interval": [],
    }
    snap = y1lib.snapshot(board)
    bits = y1lib.bits_of(snap)
    out["per_interval"].append({"interval": 0, "integers_per_node": y1lib.count_of(snap), "largest_bits": bits[0], "largest_bits_array": bits[1], "the_48": the_48(board)})
    for k in range(1, INTERVALS + 1):
        board.step()
        snap = y1lib.snapshot(board)
        bits = y1lib.bits_of(snap)
        vol = board.states[volume].lines
        sums = {LINE_NAMES[n]: int(np.asarray(vol[n].now, dtype=object).sum()) for n in range(10)}
        flux_at_faces = {LINE_NAMES[4 + a]: [int(vol[4 + a].now[f]) for f in FACES] for a in range(3)}
        shear_at_edges = {LINE_NAMES[7 + p]: [int(vol[7 + p].now[e]) for e in EDGES] for p in range(3)}
        nonzero = {LINE_NAMES[n]: int(np.count_nonzero(np.asarray(vol[n].now, dtype=object))) for n in range(10)}
        charge = 0
        planes = 0
        for i in board.turning:
            fam = board.families[i]
            for r in range(len(board.states[i].lines) // (fam.parts * fam.width)):
                own = board.lines_of(i, r)
                charge += int(np.asarray(records.wronskian(own, True), dtype=object).sum())
                planes += 1
        momentum = readings.momentum_of(board.families[light].pair[0], board.record(light))
        out["per_interval"].append({
            "interval": k, "integers_per_node": y1lib.count_of(snap), "same_count_every_node": int(all(len(v) == 27 for key, v in snap.items() if key != "interval")),
            "largest_bits": bits[0], "largest_bits_array": bits[1],
            "board_sums": sums, "nonzero_nodes": nonzero, "flux_at_origin_faces": flux_at_faces, "shear_at_edges": shear_at_edges,
            "charge_board": charge, "plane_records": planes, "light_momentum": list(momentum), "turned_nodes": int(board.turned.sum()), "the_48": the_48(board),
        })
        print(json.dumps({"interval": k, "count": y1lib.count_of(snap), "bits": bits[0], "sums": sums, "charge": charge, "P": list(momentum), "48": out["per_interval"][-1]["the_48"]}))
    births = [li for li in lines if li["event"] == "birth"]
    credits = [li for li in lines if li["event"] == "credit"]
    refused = [li for li in lines if li["event"] == "refused"]
    out["clicks"] = {
        "births": len(births), "credits": len(credits), "refused": len(refused),
        "senses_sum": sum(sum(b["senses"]) for b in births),
        "take_exact": sum(1 for b in births if b.get("taken") == b.get("walls") + b.get("excess")),
        "take_lines": [{"interval": b["interval"], "taken": b.get("taken"), "walls": b.get("walls"), "excess": b.get("excess"), "step": b.get("step"), "senses": b["senses"], "nodes": b["nodes"]} for b in births],
        "credit_lines": [{k: c.get(k) for k in ("interval", "family", "momentum", "point", "sense", "beat", "proper", "support", "count")} for c in credits],
    }
    out["credits_momentum_sum_per_axis"] = [sum((c["momentum"][a][0] if c.get("momentum") else 0) for c in credits) for a in range(3)]
    # the run back: a second board of the same seed, N forward and N back, every array compared (tools/back_in_time.verdict, the lays crossed)
    from back_in_time import verdict
    back = verdict(y1lib.board_of(Path("/dev/shm/tmp/y1_m2_back")), INTERVALS - 1)
    out["run_back"] = back
    print(json.dumps({"clicks": {k: v for k, v in out["clicks"].items() if k not in ("take_lines", "credit_lines")}, "run_back": back}))
    (HERE / "m2_metric_run.json").write_text(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
