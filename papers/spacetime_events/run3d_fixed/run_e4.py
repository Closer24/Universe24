"""Worker E4: the paper's run on a FIXED three-dimensional board at bd0e13557 under the blind (BRIEF_E4_FIXED.md), E3's run_e3.py adapted: the board [400, 8, 8], x open with no receding key, 172 intervals, and the numbers the three hostile reviews asked for, (a)-(h).

Four readings of papers/spacetime_events/run3d_fixed/one_piece_3d_fixed.json on the V2 engine alone:
 (i)   the twin: the world with its draw against the same world without it (node_detector, transitions, rates removed), the differing Nodes per tick as a 3D set;
 (ii)  the reversal with the books: 172 forward with snapshots, step_inverse back to 0, books intact, the lay lines crossed;
 (iii) the reversal without the erasure's record: credit.faces and credit.fronts emptied before stepping back, the wrong set per tick as a 3D set (and iii-b with the lays crossed);
 (iv)  the two detectors: the credit lines, which clicked, the tick and the hole's Node, any second click, the books' count after the first click; the shares at every close.
Nothing in the worktree is changed; the twin world lives under papers/spacetime_events/run3d_fixed/twin/.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

V2 = Path(__file__).resolve().parents[3]  # the repository's root; this script lives in papers/spacetime_events/run3d_fixed/
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(V2 / "src"))

from event_universe.lattice import Lattice  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402


def load_file(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


TOOL = load_file("pixel_mode", V2 / "tools" / "pixel_mode.py")
BACK = load_file("back_in_time", V2 / "tools" / "back_in_time.py")
WORLD = OUT / "one_piece_3d_fixed.json"
INTERVALS = 172
EXPECTED_CLICK = 96  # the blind's tick
CLOSES = (48, 96, 144)
Node = tuple[int, int, int]


def records_of(prefix: str, value) -> list[tuple[str, np.ndarray]]:
    found = []
    if isinstance(value, list):
        for k, item in enumerate(value):
            found += records_of(f"{prefix}[{k}]", item)
    elif hasattr(value, "now"):
        for key in ("now", "before", "remainder"):
            found.append((f"{prefix}.{key}", np.asarray(getattr(value, key)).copy()))
    else:
        found.append((prefix, np.asarray(value).copy()))
    return found


def snapshot(board: Lattice) -> dict:
    arrays = []
    for family, state in zip(board.families, board.states, strict=True):
        arrays += records_of(f"{family.name}.lines", state.lines)
        arrays += records_of(f"{family.name}.write_remainders", list(state.write_remainders))
        arrays += records_of(f"{family.name}.phases", state.phases)
    return {"shape": tuple(board.shape), "offset": tuple(board.offset), "arrays": arrays}


def nodes_of(where: np.ndarray, offset, x_from: int = 0) -> set[Node]:
    return {(int(i) + x_from - offset[0], int(j), int(k)) for i, j, k in where}


def box(nodes: set[Node]) -> list[int] | None:
    if not nodes:
        return None
    xs, ys, zs = zip(*nodes, strict=True)
    return [min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)]


def differing_same_board(a: dict, b: dict) -> tuple[set[Node], dict[str, int]]:
    nodes: set[Node] = set()
    labels: dict[str, int] = {}
    if a["shape"] != b["shape"] or a["offset"] != b["offset"]:
        return {(-10**9, 0, 0)}, {"shape": -1}
    for (label, was), (label2, now) in zip(a["arrays"], b["arrays"], strict=True):
        assert label == label2
        where = np.argwhere(was != now)
        if len(where):
            found = nodes_of(where, a["offset"])
            nodes |= found
            labels[label] = len(found)
    return nodes, labels


def differing_twin(a: dict, b: dict) -> dict:
    """The fixed board: both boards the same shape and offset the whole run (asserted); per array the differing Nodes, and the photon's alone."""
    assert a["shape"] == b["shape"] and a["offset"] == b["offset"], (a["shape"], b["shape"])
    nodes: set[Node] = set()
    photon: set[Node] = set()
    labels: dict[str, int] = {}
    for (label, was), (label2, now) in zip(a["arrays"], b["arrays"], strict=True):
        assert label == label2
        where = np.argwhere(was != now)
        if len(where):
            found = nodes_of(where, a["offset"])
            nodes |= found
            labels[label] = len(found)
            if label.startswith("photon."):
                photon |= found
    return {"nodes": nodes, "photon": photon, "labels": labels}


def variant_world(folder_name: str, drop: tuple[str, ...]) -> Path:
    folder = OUT / folder_name
    folder.mkdir(parents=True, exist_ok=True)
    document = json.loads(WORLD.read_text(encoding="utf-8"))
    for body in document["bodies"]:
        for key in drop:
            body.pop(key, None)
    path = folder / f"one_piece_3d_fixed_{folder_name}.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    shutil.copy(WORLD.with_name("design.json"), folder / "design.json")
    TOOL.main(["--input", str(path)])
    original = json.loads(WORLD.with_suffix(".mode.json").read_text(encoding="utf-8"))
    made = json.loads(path.with_suffix(".mode.json").read_text(encoding="utf-8"))
    assert made["packets"] == original["packets"], "the variant's packets differ from the original's"
    return path


def distance(a: Node, b: Node) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def photon_profile(board: Lattice, photon: int, lay_x: float) -> dict:
    """(e): the photon line's extent along x (any Node across nonzero), and per side of the lay the x of the largest |value| at (4, 4) and that value, and the largest |value| anywhere."""
    now = np.asarray(board.states[photon].lines[0].now)
    along = now.any(axis=(1, 2))
    nz = np.nonzero(along)[0]
    profile = now[:, 4, 4]
    xs = np.arange(now.shape[0])
    left = np.where(xs < lay_x, np.abs(profile), -1)
    right = np.where(xs > lay_x, np.abs(profile), -1)
    lx, rx = int(np.argmax(left)), int(np.argmax(right))
    return {"x_min": int(nz.min()) if len(nz) else None, "x_max": int(nz.max()) if len(nz) else None, "nodes": int(now.astype(bool).sum()),
            "peak_minus_x": [lx, int(profile[lx])], "peak_plus_x": [rx, int(profile[rx])], "largest_abs": int(np.abs(now).max())}


def shares_read(board: Lattice, photon: int) -> dict:
    """(c): the bodies' labels, shares and the books' unabsorbed share right after a close, as E3's probe48 read them."""
    out = {}
    for nb in board.credit.bodies:
        unit = sum(int(v) ** 2 for v in nb.labels)
        out[f"body {nb.number}"] = {"labels": [int(v) for v in nb.labels], "labels_unit": unit, "shares": {str(k.drive) + f" {k.leaves}->{k.enters}": int(v) for k, v in nb.shares.items()},
                                   "share_over_unit": [round(int(v) / unit, 6) for v in nb.shares.values()], "windows": nb.windows, "clock": [int(v) for v in nb.clock], "part": nb.part, "counts": [int(v) for v in nb.counts]}
    out["books"] = {"photon_count": int(board.credit.counts[photon]), "unabsorbed": {str(k): int(v) for k, v in board.credit.unabsorbed.items()}, "unabsorbed_units": {str(k): int(v) for k, v in board.credit.unabsorbed_units.items()},
                    "unabsorbed_over_unit": {str(k): round(int(v) / int(board.credit.unabsorbed_units[k]), 6) for k, v in board.credit.unabsorbed.items()}}
    shares = [list(nb.shares.values())[0] if nb.shares else 0 for nb in board.credit.bodies]
    units = [sum(int(v) ** 2 for v in nb.labels) for nb in board.credit.bodies]
    out["sum_of_shares_over_unit"] = round(sum(int(s) / u for s, u in zip(shares, units)), 6)
    out["no_click_weight_over_unit_as_engine"] = round(max(min(1.0, float(out["books"]["unabsorbed_over_unit"].get(str(photon), 0.0))) - out["sum_of_shares_over_unit"], 0.0), 6) if board.credit.counts[photon] > 0 else "no draw: the count is 0"
    return out


def atom_values(snap: dict, nodes: list[Node]) -> dict:
    return {label: [int(arr[n]) for n in nodes] for label, arr in snap["arrays"] if label.startswith("atom.")}


def main() -> None:
    report: dict = {}
    report["engine"] = subprocess.run(["git", "rev-parse", "HEAD"], cwd=V2, capture_output=True, text=True, check=True).stdout.strip()
    report["worktree_status"] = subprocess.run(["git", "status", "--short"], cwd=V2, capture_output=True, text=True, check=True).stdout.strip()
    report["world"] = json.loads(WORLD.read_text(encoding="utf-8"))
    mode = json.loads(WORLD.with_suffix(".mode.json").read_text(encoding="utf-8"))
    report["mode_packets"] = [{k: v for k, v in p.items() if k != "moving"} for p in mode["packets"]]

    twin_path = variant_world("twin", ("node_detector", "transitions", "rates"))
    lines: list[dict] = []
    clicked = Lattice(load_world(WORLD), lines.append)
    plain = Lattice(load_world(twin_path))
    photon = [f.name for f in clicked.families].index("photon")
    takers = [tuple(tuple(n) for n in b.nodes) for b in clicked.world.bodies]
    atom_nodes = [n for t in takers for n in t]
    report["books_at_start"] = {"counts": dict(clicked.credit.counts), "units": dict(clicked.credit.units)}
    report["board"] = {"shape": list(clicked.shape), "offset": list(clicked.offset), "receding": list(clicked.world.receding), "nodes": int(np.prod(clicked.shape)), "open_axes": list(clicked.world.open_axes)}
    report["f_families"] = {"pairs": {f.name: list(f.pair) for f in clicked.families}, "universe_integers": {"node_clock": clicked.world.node_clock, "quantum_action": clicked.world.quantum_action, "width": clicked.world.width, "link_unit": clicked.world.link_unit},
                            "bodies_rates": [b["rates"] for b in report["world"]["bodies"]], "bodies_transitions": [b["transitions"] for b in report["world"]["bodies"]]}
    lay_x = (report["world"]["packets"][0]["top"]["x"][0] + report["world"]["packets"][1]["top"]["x"][0]) / 2

    # (e) the packets at the lay
    now0 = np.asarray(clicked.states[photon].lines[0].now)
    X = now0.shape[0]
    profile0 = now0[:, 4, 4]
    nz = np.nonzero(profile0)[0]
    report["e_packets_at_load"] = {"profile_x_at_4_4": {str(int(x)): int(profile0[x]) for x in range(int(nz.min()) - 1, int(nz.max()) + 2)}, "x_extent": [int(nz.min()), int(nz.max())], "nodes_nonzero": int(now0.astype(bool).sum()),
                                   "cross_section_uniform": bool(all((now0[x][2:6, 2:6] == now0[x, 4, 4]).all() and not now0[x][:2].any() and not now0[x][6:].any() and not now0[x][:, :2].any() and not now0[x][:, 6:].any() for x in range(X))),
                                   "mirror_x_to_X-1-x_equal": bool((now0 == now0[::-1]).all()), "mirror_sign_flipped": bool((now0 == -now0[::-1]).all()),
                                   "before_equals_now": bool((np.asarray(clicked.states[photon].lines[0].before) == now0).all()), "before_profile_x_at_4_4": {str(int(x)): int(np.asarray(clicked.states[photon].lines[0].before)[x, 4, 4]) for x in range(int(nz.min()) - 1, int(nz.max()) + 2)}}

    # --- forward, both boards side by side
    t0 = time.perf_counter()
    forward = {clicked.interval: snapshot(clicked)}
    twin_snaps = {}
    twin_rows = []
    counts_by_tick = {}
    edges = {0: (-clicked.offset[0], clicked.shape[0] - clicked.offset[0] - 1)}
    profiles = {0: photon_profile(clicked, photon, lay_x)}
    closes = {}
    first_twin = None
    board_wiped = {}
    for _ in range(INTERVALS):
        clicked.step()
        plain.step()
        t = clicked.interval
        forward[t] = snapshot(clicked)
        counts_by_tick[t] = dict(clicked.credit.counts)
        edges[t] = (-clicked.offset[0], clicked.shape[0] - clicked.offset[0] - 1)
        if t <= 48 or t in (96, 144, 170, 172):
            profiles[t] = photon_profile(clicked, photon, lay_x)
        twin_snap = snapshot(plain)
        found = differing_twin(forward[t], twin_snap)
        if found["nodes"]:
            if first_twin is None:
                first_twin = (t, found["labels"], sorted(found["nodes"])[:4])
            twin_rows.append({"interval": t, "nodes": found["nodes"], "photon": found["photon"], "labels": found["labels"]})
        if t in CLOSES:
            closes[t] = {"shares": shares_read(clicked, photon), "atom_clicked": atom_values(forward[t], atom_nodes), "atom_twin": atom_values(twin_snap, atom_nodes), "atom_nodes": [list(n) for n in atom_nodes],
                         "lines_at_tick": [{k: v for k, v in l.items() if k not in ("ports",)} for l in lines if l["interval"] == t and l["event"] != "face"],
                         "atom_arrays_differing_from_twin": {label: [list(n) for n in sorted(nodes_of(np.argwhere(a != b), clicked.offset))] for (label, a), (_l, b) in zip(forward[t]["arrays"], twin_snap["arrays"], strict=True) if label.startswith("atom.") and (a != b).any()}}
        if t in (170, 172):
            clicked_now = np.asarray(clicked.states[photon].lines[0].now)
            clicked_before = np.asarray(clicked.states[photon].lines[0].before)
            twin_now = np.asarray(plain.states[photon].lines[0].now)
            twin_before = np.asarray(plain.states[photon].lines[0].before)
            zero_here_nonzero_twin = nodes_of(np.argwhere((clicked_now == 0) & (clicked_before == 0) & ((twin_now != 0) | (twin_before != 0))), clicked.offset)
            board_wiped[t] = {"twin_differing_all_arrays": len(found["nodes"]), "twin_differing_photon_arrays": len(found["photon"]), "photon_zero_now_and_before_where_twin_nonzero": len(zero_here_nonzero_twin),
                              "photon_zero_now_and_before_where_twin_nonzero_box": box(zero_here_nonzero_twin), "twin_differing_photon_box": box(found["photon"])}
        if clicked.ended is not None or plain.ended is not None:
            report["ended"] = {"clicked": clicked.ended, "twin": plain.ended, "interval": t}
            break
    t_forward = time.perf_counter() - t0
    end = clicked.interval
    report["h_times"] = {"forward_both_boards_s": round(t_forward, 2)}

    # (e) group speed over 0..48
    ticks = sorted(k for k in profiles if k <= 48)
    p0, p48 = profiles[0], profiles[48]
    report["e_motion_0_to_48"] = {"profiles": {str(k): profiles[k] for k in profiles},
                                  "front_plus_x_nodes_per_tick": round((p48["x_max"] - p0["x_max"]) / 48, 4), "front_minus_x_nodes_per_tick": round((p0["x_min"] - p48["x_min"]) / 48, 4),
                                  "peak_plus_x_nodes_per_tick": round((p48["peak_plus_x"][0] - p0["peak_plus_x"][0]) / 48, 4), "peak_minus_x_nodes_per_tick": round((p0["peak_minus_x"][0] - p48["peak_minus_x"][0]) / 48, 4),
                                  "front_plus_x_by_tick": [[k, profiles[k]["x_max"]] for k in ticks], "peak_plus_x_by_tick": [[k, *profiles[k]["peak_plus_x"]] for k in ticks]}

    # (iv) the two detectors
    credits = [c for c in lines if c["event"] == "credit"]
    absorbed = [c for c in credits if c.get("absorbed")]
    lays = [l for l in lines if l["event"] == "lay"]
    face_lines = [l for l in lines if l["event"] == "face"]
    erasures = [l for l in lines if l["event"] == "erasure"]
    click_tick = absorbed[0]["interval"] if absorbed else None
    holes = sorted({tuple(f.at) for f in clicked.credit.faces.get((click_tick or 0) + 1, []) if f.family == photon}) if click_tick else []
    hole = holes[0] if holes else None
    lay_nodes = sorted({(l["interval"], l["family"], l["line"], tuple(BACK.node_of(clicked, l)[1])) for l in lays})
    report["iv_two_detectors"] = {
        "verdict": "holds" if (len(absorbed) == 1 and click_tick == EXPECTED_CLICK and (counts_by_tick[click_tick][photon] == 0) and len(holes) == 1 and hole in takers[int(absorbed[0]["node_detector"].split()[-1])]) else "does not hold",
        "credit_lines": credits,
        "clicks_absorbed": [(c["interval"], c["node_detector"], c["proper"], c["window"], c["count"], c["left"]) for c in absorbed],
        "which_clicked": absorbed[0]["node_detector"] if absorbed else None,
        "click_tick": click_tick,
        "hole_nodes_file_coordinates": [list(h) for h in holes],
        "takers": [[list(n) for n in t] for t in takers],
        "second_click": len(absorbed) > 1,
        "books_count_photon_by_tick": {t: c[photon] for t, c in counts_by_tick.items() if t in (47, 48, 49, 95, 96, 97, 144, 145, 170, end)},
        "fronts": [(f.family, list(f.origin), f.since) for f in clicked.credit.fronts],
        "lay_lines": {"count": len(lays), "nodes": sorted({n[3] for n in lay_nodes}), "by_interval_family_line_node": lay_nodes},
        "face_lines_count": len(face_lines),
        "event_kinds": sorted({l["event"] for l in lines}),
        "c_closes": closes,
    }
    # (a) the shells, (b) the faces
    report["a_erased_nodes_per_shell"] = [(l["interval"], l["distance"], l["nodes"]) for l in erasures]
    report["a_erased_nodes_total_to_end"] = sum(l["nodes"] for l in erasures)
    report["a_erased_nodes_total_to_170"] = sum(l["nodes"] for l in erasures if l["interval"] <= 170)
    faces_all = [(k, f) for k, v in clicked.credit.faces.items() for f in v]
    faces_photon = [(k, f) for k, f in faces_all if f.family == photon]
    nonzero = [(k, f) for k, f in faces_all if f.value is not None and f.value != 0]
    value_none = sum(1 for _k, f in faces_all if f.value is None)
    nodes_faces = {tuple(f.at) for _k, f in faces_all}
    nodes_nonzero = {tuple(f.at) for _k, f in nonzero}
    per_key = {}
    for k, f in faces_all:
        row = per_key.setdefault(k, {"faces": 0, "nonzero": 0, "nodes": set(), "nodes_nonzero": set()})
        row["faces"] += 1
        row["nodes"].add(tuple(f.at))
        if f.value is not None and f.value != 0:
            row["nonzero"] += 1
            row["nodes_nonzero"].add(tuple(f.at))
    report["b_faces"] = {
        "intervals_keyed": [min(clicked.credit.faces), max(clicked.credit.faces)] if clicked.credit.faces else None,
        "count": len(faces_all), "count_photon_family": len(faces_photon), "count_keyed_to_170": sum(1 for k, _f in faces_all if k <= 170), "count_keyed_to_172": sum(1 for k, _f in faces_all if k <= 172),
        "nonzero_value_count": len(nonzero), "zero_value_count": len(faces_all) - len(nonzero) - value_none, "value_none_count": value_none,
        "distinct_nodes": len(nodes_faces), "nodes_with_at_least_one_nonzero_wiped_value": len(nodes_nonzero),
        "distinct_nodes_keyed_to_170": len({tuple(f.at) for k, f in faces_all if k <= 170}), "distinct_nodes_keyed_to_172": len({tuple(f.at) for k, f in faces_all if k <= 172}),
        "per_keyed_interval": {str(k): [r["faces"], r["nonzero"], len(r["nodes"]), len(r["nodes_nonzero"])] for k, r in sorted(per_key.items())},
        "per_keyed_interval_columns": ["faces", "faces with nonzero value", "distinct Nodes", "Nodes with a nonzero value"],
        "largest_abs_value": max((abs(f.value) for _k, f in nonzero), default=0), "ports_used": sorted({f.port for _k, f in faces_all}), "fronts_at_end": len(clicked.credit.fronts),
        "board_wiped_read_directly": board_wiped,
    }

    # (i) the twin against the blind
    taker = set(takers[int(absorbed[0]["node_detector"].split()[-1])]) if absorbed else set()
    rows_i, violations, hull_short = [], [], []
    for r in twin_rows:
        t = r["interval"]
        allnodes = r["nodes"]
        if click_tick is not None and t >= click_tick + 2:
            radius = t - (click_tick + 1)
            bad = sorted(n for n in allnodes if distance(n, hole) > radius)
        else:
            bad = sorted(n for n in allnodes if n not in taker and n != hole)
        if bad:
            violations.append((t, len(bad), bad[:6]))
        b = box(allnodes)
        rows_i.append([t, b, len(allnodes), r["labels"], len(r["photon"])])
        if click_tick is not None and t >= click_tick + 2 and b is not None:
            radius = t - (click_tick + 1)
            expected = [max(hole[0] - radius, edges[t][0]), min(hole[0] + radius, edges[t][1]), max(0, 4 - radius), min(7, 4 + radius), max(0, 4 - radius), min(7, 4 + radius)]
            if b != expected:
                hull_short.append((t, b, expected))
    verdict_i = first_twin is not None and first_twin[0] == click_tick and not violations and set(sorted(twin_rows[0]["nodes"])) <= taker
    report["i_twin"] = {
        "verdict": "holds" if verdict_i else "does not hold",
        "first_difference": first_twin,
        "nodes_differing_at_click_tick": sorted(twin_rows[0]["nodes"]) if twin_rows else None,
        "ball": "|dx| + |dy| + |dz| <= t - (click_tick + 1) about the hole, from click_tick + 2; at click_tick and click_tick + 1 the taker's Nodes and the hole",
        "outside_ball": violations,
        "bounding_box_short_of_the_clipped_ball": hull_short[:20],
        "bounding_box_short_count": len(hull_short),
        "intervals_differing": len(twin_rows),
        "shapes_same_whole_run": True,
        "edges_x": list(edges[0]),
        "last_interval": end,
    }
    (OUT / "i_twin_rows.json").write_text(json.dumps({"columns": ["interval", "[min x, max x, min y, max y, min z, max z]", "count all arrays", "labels: array -> Nodes", "count photon arrays"], "rows": rows_i}, indent=0), encoding="utf-8")

    # --- the reversals
    clicked.output = None

    def reverse(board: Lattice, cross: bool) -> tuple[dict, list]:
        rows, first = [], None
        t0 = time.perf_counter()
        for _ in range(end):
            if cross:
                BACK.crossed(board, lines)
            board.step_inverse()
            nodes, labels = differing_same_board(forward[board.interval], snapshot(board))
            if nodes:
                if first is None:
                    first = (board.interval, labels, sorted(nodes)[:4])
                rows.append([board.interval, box(nodes), len(nodes)])
        too_fast = []
        for (t, b, _n), (t2, b2, _n2) in zip(rows, rows[1:]):
            if t2 != t - 1 or b is None or b2 is None:
                continue
            e2 = edges[t2]
            faults = []
            if b2[0] < b[0] - 1 and b2[0] != e2[0]:
                faults.append("min x")
            if b2[1] > b[1] + 1 and b2[1] != e2[1]:
                faults.append("max x")
            for k, (lo_face, hi_face) in ((2, (0, 7)), (4, (0, 7))):
                if b2[k] < b[k] - 1 and b2[k] != lo_face:
                    faults.append(["min y", "min z"][k // 2 - 1])
                if b2[k + 1] > b[k + 1] + 1 and b2[k + 1] != hi_face:
                    faults.append(["max y", "max z"][k // 2 - 1])
            if faults:
                too_fast.append((t2, b2, b, faults))
        return {"first_mismatch": first, "rows_count": len(rows), "rows_first3": rows[:3], "rows_last3": rows[-3:], "ends_moving_faster_than_one_node_per_tick": too_fast, "time_s": round(time.perf_counter() - t0, 2), "back_to": board.interval}, rows

    with_books = copy.deepcopy(clicked)
    ii, rows_ii = reverse(with_books, cross=True)
    report["ii_books"] = {"verdict": "holds" if ii["first_mismatch"] is None and ii["back_to"] == 0 else "does not hold", "lays_crossed": True, **ii}
    (OUT / "ii_books_rows.json").write_text(json.dumps({"columns": ["interval", "bounding box", "count"], "rows": rows_ii}, indent=0), encoding="utf-8")

    without = copy.deepcopy(clicked)
    cleared = {"faces_intervals": [min(without.credit.faces), max(without.credit.faces)], "faces_count": sum(len(v) for v in without.credit.faces.values()), "fronts_count": len(without.credit.fronts), "what": "board.credit.faces = {} and board.credit.fronts = []; nothing else; the lay lines not crossed"}
    without.credit.faces = {}
    without.credit.fronts = []
    iii, rows_iii = reverse(without, cross=False)
    last_shell = sorted({tuple(f.at) for f in clicked.credit.faces.get(end, []) if f.family == photon})
    reach_box = box(set(last_shell))
    first_row = rows_iii[0] if rows_iii else None
    reach_ok = first_row is not None and reach_box is not None and all(first_row[1][2 * k] >= reach_box[2 * k] - 1 and first_row[1][2 * k + 1] <= reach_box[2 * k + 1] + 1 for k in range(3))
    first_ok = iii["first_mismatch"] is not None and iii["first_mismatch"][0] == end - 1
    total_nodes = int(np.prod(clicked.shape))
    at0 = next((r for r in rows_iii if r[0] == 0), None)
    jumps = [(a[0], b[0], a[1], b[1]) for a, b in zip(rows_iii, rows_iii[1:]) if a[1] and b[1] and (abs(b[1][0] - a[1][0]) > 1 or abs(b[1][1] - a[1][1]) > 1)]
    report["iii_no_books"] = {"verdict": "holds" if (first_ok and reach_ok and not iii["ends_moving_faster_than_one_node_per_tick"]) else "does not hold", "cleared": cleared, "front_reach_at_end_bounding_box": reach_box, "front_reach_at_end_nodes": len(last_shell),
                              "g_wrong_at_tick_0": at0, "g_wrong_at_tick_0_over_board": [at0[2] if at0 else 0, total_nodes], "g_x_end_jumps_above_one_node": jumps, "g_rows_marks": [r for r in rows_iii if r[0] in (171, 170, 169, 160, 150, 144, 120, 100, 97, 96, 95, 72, 50, 48, 24, 1, 0)], **iii}
    (OUT / "iii_no_books_rows.json").write_text(json.dumps({"columns": ["interval", "bounding box", "count"], "rows": rows_iii}, indent=0), encoding="utf-8")

    without_b = copy.deepcopy(clicked)
    without_b.credit.faces = {}
    without_b.credit.fronts = []
    iii_b, rows_iii_b = reverse(without_b, cross=True)
    report["iii_b_no_faces_lays_crossed"] = {"beside_the_blind": "the same clearing as (iii) with the lay lines crossed as in (ii)", "same_rows_as_iii": rows_iii_b == rows_iii, **iii_b}
    (OUT / "iii_b_no_faces_lays_crossed_rows.json").write_text(json.dumps({"columns": ["interval", "bounding box", "count"], "rows": rows_iii_b}, indent=0), encoding="utf-8")
    report["h_times"].update({"ii_s": ii["time_s"], "iii_s": iii["time_s"], "iii_b_s": iii_b["time_s"], "total_s": round(time.perf_counter() - T_START, 2)})

    (OUT / "report_e4.json").write_text(json.dumps(report, indent=1, default=str), encoding="utf-8")

    # the figure's data
    families = []
    for family, state in zip(clicked.families, clicked.states, strict=True):
        n_lines = len(state.lines)
        remainders = len(list(state.write_remainders))
        phases = len(records_of("p", state.phases))
        families.append({"family": family.name, "lines": n_lines, "integers_per_node": {"lines_now_before_remainder": n_lines * 3, "write_remainders": remainders, "phase_arrays": phases, "total": n_lines * 3 + remainders + phases}, "pair": list(family.pair)})
    figure = {
        "engine": report["engine"],
        "world": str(WORLD.relative_to(V2)),
        "board": {"shape": report["world"]["shape"], "boundary": report["world"]["boundary"], "receding": None, "edges_x": list(edges[0]), "nodes": total_nodes},
        "detectors": [{"body": k, "nodes": [list(n) for n in t]} for k, t in enumerate(takers)],
        "window": 48,
        "click": {"tick": click_tick, "node": list(hole) if hole else None, "body": report["iv_two_detectors"]["which_clicked"]},
        "intervals": end,
        "i_erased_set_after_click": [[t, b, n] for t, b, n, _l, _p in rows_i if click_tick is not None and t > click_tick],
        "i_ball_bound": "|dx| + |dy| + |dz| <= t - (click.tick + 1) about click.node, cut by the y and z faces",
        "ii_crossed_first_mismatch": ii["first_mismatch"],
        "iii_wrong_set_backward": rows_iii,
        "iii_b_wrong_set_backward_lays_crossed": rows_iii_b,
        "erased_nodes_per_shell": report["a_erased_nodes_per_shell"],
        "erased_nodes_total": report["a_erased_nodes_total_to_end"],
        "faces_count": len(faces_all),
        "faces_nonzero_value_count": len(nonzero),
        "shares_at_closes": {str(t): closes[t]["shares"] for t in closes},
        "words": {"neighbours_per_node": 6, "axes": 3, "links_per_interval": 1, "families": families, "integers_per_node_total": sum(f["integers_per_node"]["total"] for f in families)},
    }
    (OUT / "figure_data.json").write_text(json.dumps(figure, indent=1), encoding="utf-8")

    brief = {k: v for k, v in report.items() if k not in ("world", "i_twin", "iv_two_detectors", "a_erased_nodes_per_shell", "e_motion_0_to_48", "b_faces", "mode_packets")}
    brief["i_twin"] = {k: v for k, v in report["i_twin"].items()}
    brief["iv"] = {k: v for k, v in report["iv_two_detectors"].items() if k not in ("credit_lines", "lay_lines", "c_closes")}
    brief["iv"]["lay_lines_count"] = report["iv_two_detectors"]["lay_lines"]["count"]
    brief["iv"]["lay_nodes"] = report["iv_two_detectors"]["lay_lines"]["nodes"]
    brief["b_faces"] = {k: v for k, v in report["b_faces"].items() if k != "per_keyed_interval"}
    brief["shells_first10_last3"] = report["a_erased_nodes_per_shell"][:10] + report["a_erased_nodes_per_shell"][-3:]
    brief["shell_counts_distinct"] = sorted({n for _t, _s, n in report["a_erased_nodes_per_shell"]})
    brief["e_speeds"] = {k: v for k, v in report["e_motion_0_to_48"].items() if k != "profiles"}
    brief["c_closes_shares"] = {str(t): closes[t]["shares"] for t in closes}
    brief["d_closes_atom"] = {str(t): {"differing_from_twin": closes[t]["atom_arrays_differing_from_twin"], "lines": closes[t]["lines_at_tick"]} for t in closes}
    brief["i_rows_marks"] = [r[:3] + [r[4]] for r in rows_i if r[0] in (96, 97, 98, 99, 100, 104, 110, 120, 144, 170, 172)]
    print(json.dumps(brief, indent=1, default=str))


if __name__ == "__main__":
    T_START = time.perf_counter()
    main()
