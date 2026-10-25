"""Hand z2 (2026-10-25): the seed as a list of lays, each the click's own lay act, three forms (sea, at, hole), laid
on the branch's engine with no edit of src/ (the seed's door, seed.uniform_seed, taken by this script's generic lay as
the tests take it), the run with the engine's own three logs (tools/eras.py's header, interval and node lines, so that
tools/record_gates.py reads them), the per-record readings for the bodies' gathering, the snapshots and the run back.

The world file in the generic form: {"universe": ..., "shape": [...], "intervals": N, "seed": [lay, lay, ...]}; the
branch's loader refuses the key `seed`, so the script strips it and lays the list itself. The forms, each one call of
lay.laid with no weights (the uniform part IS the lay, the seed's door, ALGEBRA.md, The uniform seed is a lay):
  {"sea": n}                      light at n quanta on every Node: the drift v_n = isqrt(n T), the level before 0;
  {"sea": {"quanta_per_mode": q, "modes": [[mx,my,mz], ...], "centre": [x,y,z]}}  light as a standing wave, the modes
                                  summed, q quanta per mode (R4's seed under the ride), symmetric under the 48 about the centre;
  {"hole": [x,y,z]}               the light at the Node taken to 0 (the lay's origin, the law's hole);
  {"at": {"pair": [num,den], "centre": [x,y,z], "sigma_tenths": s, "quanta": N, "sense": +-1, "record": r}}
                                  a packet: for the light's pair with sigma 0, N quanta more at the Node (the drift
                                  v = isqrt((sea + N) T) there); for a gapped pair a binomial packet of sigma 1.22 Links
                                  (sigma_tenths 12, C(6, 3 + x) per axis) at rest in the local content on the record r
                                  with the sense, N quanta, laid at the interval 0 after the start (g4's lay form).
Refused by name: a lay naming a row ("row"/"name"/"family"), a one-Node body (a gapped pair at sigma 0, G-S2), a light
packet with a width (the guard: a massless lay with weights moves the two sums), a pair no row of the universe carries.

    PYTHONPATH=src python tools/derivations/z2/seed_run.py world.json --out-dir DIR [--read-every 10] [--run-back all|40|0]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from itertools import permutations, product
from math import comb
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
for place in (str(ROOT), str(ROOT / "src"), str(ROOT / "tools")):
    if place not in sys.path:
        sys.path.insert(0, place)

import numpy as np  # noqa: E402

import eras  # noqa: E402  (tools/eras.py: header_of, interval_line, node_lines, kept_lines, volume_residuals, whole)
from event_universe import records, registry, seed, share, world_files  # noqa: E402
from event_universe.core.paces import clock_alone  # noqa: E402
from event_universe.core.rule3 import largest_below  # noqa: E402
from event_universe.features import volume  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.lay import laid  # noqa: E402
from event_universe.meeting_back import crossed, first_difference, snapshot  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402

Node = tuple[int, int, int]
SCALE = 10**6  # the cosines' integer scale for the standing wave's lay
BINOMIAL = 6  # the packet's profile per axis C(6, 3 + x): sigma^2 = 6 / 4 per axis, sigma 1.22 Links (sigma_tenths 12)


def refuse(text: str) -> None:
    raise ValueError("the seed is refused by name: " + text)


def isqrt(n: int) -> int:
    return largest_below(n)


def offsets(shape: tuple[int, ...], origin: Node) -> np.ndarray:
    coords = np.indices(shape)
    found = np.zeros_like(coords)
    for a in range(3):
        n = shape[a]
        d = (coords[a] - origin[a]) % n
        found[a] = np.where(d > n // 2, d - n, d)
    return found


def manhattan(shape: tuple[int, ...], origin: Node) -> np.ndarray:
    return np.abs(offsets(shape, origin)).sum(axis=0)


def cos_scaled(m: int, x: int, n: int) -> int:
    """cos(2 pi m x / n) in units of 10^-6 by integer roots alone, for the fifth and the seventh roots of unity where they
    are needed (n = 5: cos 72 = (sqrt 5 - 1) / 4, cos 144 = -(sqrt 5 + 1) / 4; n = 7 and others: the Chebyshev
    recurrence from cos(2 pi / n) read once by an integer bisection on the polynomial is not needed here, n is 5)."""
    r = (m * x) % n
    if n == 5:
        root5 = isqrt(5 * SCALE * SCALE)
        table = {0: SCALE, 1: (root5 - SCALE) // 4, 2: -(root5 + SCALE) // 4}
        return table[min(r, n - r)]
    if n == 4:
        return {0: SCALE, 1: 0, 2: -SCALE}[min(r, n - r)]
    if n == 3:
        return {0: SCALE, 1: -SCALE // 2}[min(r, n - r)]
    refuse(f"a standing wave on a side of {n} Nodes has no integer cosine table here")
    return 0


def rounded_div(a: int, b: int) -> int:
    """a / b rounded half away from zero on the integers (the law's mirror of the carry), b above 0."""
    q, r = divmod(abs(a), b)
    q += 1 if 2 * r >= b else 0
    return q if a >= 0 else -q


def wave_levels(shape: tuple[int, ...], modes: list[list[int]], centre: Node, amplitude: int) -> tuple[np.ndarray, np.ndarray]:
    """The standing wave's two levels: now = A SUM_m cos(k_m . (x - c)), before = A SUM_m cos(omega_m) cos(k_m . (x - c)),
    cos omega_m = (1 / 3) SUM_a cos(2 pi m_a / n_a) the massless band, every value an integer rounded once."""
    now = np.zeros(shape, dtype=object)
    before = np.zeros(shape, dtype=object)
    off = offsets(shape, centre)
    for m in modes:
        cos_omega = sum(cos_scaled(m[a], 1, shape[a]) for a in range(3)) // 3  # scaled
        for where in np.ndindex(*shape):
            c = SCALE
            for a in range(3):
                c = c * cos_scaled(m[a], int(off[a][where]), shape[a]) // SCALE
            now[where] += rounded_div(amplitude * c, SCALE)
            before[where] += rounded_div(amplitude * c * cos_omega, SCALE * SCALE)
    return now, before


def vacuum_share(now: np.ndarray, before: np.ndarray, den: int) -> np.ndarray:
    """The light's share per Node at the vacuum's paces, exactly: 3 den (now^2 + before^2) - den now SUM_6 before."""
    s6 = sum(np.roll(before, d, axis=a) for a in range(3) for d in (1, -1))
    return 3 * den * (now * now + before * before) - den * now * s6


def light_forms(board: Lattice, index: int, seed_list: list[dict[str, Any]], notes: dict[str, Any]) -> None:
    """The seed's door: the light's forms laid before the start through the one lay act with no weights."""
    family = board.families[index]
    T, den, shape = board.world.quantum_action, family.pair[1], board.shape
    now = np.zeros(shape, dtype=object)
    before = np.zeros(shape, dtype=object)
    sea_quanta = 0
    for item in seed_list:
        inner = item.get("at", {}) if isinstance(item.get("at"), dict) else {}
        if any(key in item or key in inner for key in ("row", "name", "family")):
            refuse(f"a lay named by a row or a family: {sorted(set(item) | set(inner))} (the row is its pair, a number and no name)")
        if "sea" in item:
            form = item["sea"]
            if isinstance(form, int):
                v = isqrt(form * T)
                now += v
                sea_quanta += form
                notes.setdefault("sea", []).append({"quanta_per_node": form, "drift_level": v, "v2_over_T_milli": 1000 * v * v // T})
            else:
                modes, centre, q = form["modes"], tuple(form["centre"]), int(form["quanta_per_mode"])
                target = q * len(modes) * 3 * den * T
                amplitude = 100
                trail = []
                for _ in range(8):
                    a, b = wave_levels(shape, modes, centre, amplitude)
                    total = int(vacuum_share(a, b, den).sum())
                    trail.append([amplitude, total // (3 * den * T), (1000 * total) // (3 * den * T)])
                    if total == 0:
                        amplitude *= 2
                        continue
                    new = isqrt(amplitude * amplitude * target // total)
                    if new == amplitude:
                        break
                    amplitude = new
                a, b = wave_levels(shape, modes, centre, amplitude)
                e = vacuum_share(a, b, den)
                unit = 3 * den * T
                now, before = now + a, before + b
                notes.setdefault("wave", []).append({
                    "modes": modes, "centre": list(centre), "quanta_per_mode": q, "amplitude": amplitude, "search": trail,
                    "total_quanta_milli": (1000 * int(e.sum())) // unit,
                    "largest_node_share_milli": (1000 * int(max(int(v) for v in e.reshape(-1)))) // unit,
                    "nodes_at_or_above_one_quantum": int(sum(1 for v in e.reshape(-1) if int(v) >= unit)),
                    "largest_level": int(max(abs(int(v)) for v in a.reshape(-1))),
                    "levels_at_centre_axis": [int(a[(centre[0] + d) % shape[0], centre[1], centre[2]]) for d in range(-2, 3)],
                })
        elif "hole" in item:
            at = tuple(int(x) for x in item["hole"])
            notes.setdefault("hole", []).append({"at": list(at), "level_taken": int(now[at])})
            now[at], before[at] = 0, 0
        elif "at" in item:
            form = item["at"]
            pair = tuple(int(x) for x in form["pair"])
            if pair != tuple(family.pair):
                continue  # a body's packet, laid after the start
            if int(form.get("sigma_tenths", 0)) != 0:
                refuse("a light packet with a width moves the two sums SUM now and SUM before, which the guard refuses (a massless lay with weights)")
            at = tuple(int(x) for x in form["centre"])
            v = isqrt((sea_quanta + int(form["quanta"])) * T)
            notes.setdefault("at_light", []).append({"at": list(at), "quanta_more": int(form["quanta"]), "level": v, "share_milli": 1000 * v * v // T})
            now[at] = v
        else:
            refuse(f"an unknown form {sorted(item)}; the forms are sea, at and hole")
    first = records.record_slice(family, 0).start
    unit = 3 * den * T
    e = vacuum_share(now, before, den)
    counts = [(int(v) + unit // 2) // unit for v in e.reshape(-1)]
    floors = [int(v) // unit for v in e.reshape(-1)]
    notes["light_lay"] = {
        "sum_now": int(now.sum()), "sum_before": int(before.sum()), "nodes": int(np.prod(shape)),
        "quanta_rounded_total": sum(counts), "quanta_floor_total": sum(floors),
        "nodes_with_two_whole_quanta": sum(1 for f in floors if f >= 2), "nodes_with_one_whole": sum(1 for f in floors if f == 1),
        "nodes_at_zero": sum(1 for v in now.reshape(-1) if int(v) == 0),
    }
    kind = board.kind
    for line in range(family.parts * family.width):
        laid(board, index, first + line, (now.astype(kind), before.astype(kind)), None, None)


def lay_body(board: Lattice, k: int, r: int, at: Node, sense: int, quanta: int) -> dict[str, Any]:
    """A body's packet (g4's lay form, the one lay act): `quanta` quanta of the record r of the family k about `at` as the
    binomial packet at rest in the local content, every level an integer: re_now = (A w) div 20^3, re_before = (re_now K) div W,
    im_before = sense (re_now S) div W, K = den Gamma^2 - (den - num) p_0(c)^2, W = den Gamma^2, S = isqrt(W^2 - K^2); A from the
    share by the search isqrt."""
    family = board.families[k]
    gamma = board.world.node_clock
    num, den = family.pair
    first = records.record_slice(family, r).start
    shape, held, kind = board.shape, board.held[0], board.kind
    c_lay = int(volume.level_of(gamma, np.asarray(board.states[held].lines[0].now, dtype=object))[at])
    p0 = clock_alone(gamma, c_lay)
    w_rot = den * gamma * gamma
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
    wall = comb(BINOMIAL, BINOMIAL // 2) ** 3

    def levels(amplitude: int) -> tuple[np.ndarray, ...]:
        re_now = np.vectorize(lambda w: (amplitude * int(w)) // wall, otypes=[object])(weights)
        re_before = np.vectorize(lambda v: (int(v) * k_rot) // w_rot, otypes=[object])(re_now)
        im_before = np.vectorize(lambda v: sense * ((int(v) * s_rot) // w_rot), otypes=[object])(re_now)
        return re_now, re_before, np.zeros(shape, dtype=object), im_before

    content, factors = board.read(k, 1, r)

    def share_of(amplitude: int) -> int:
        re_now, re_before, im_now, im_before = levels(amplitude)
        remainder = board.states[k].lines[first].remainder
        lines = [records.Record(re_now, re_before, remainder), records.Record(im_now, im_before, remainder)]
        return int(np.asarray(share.family_share(family, lines, gamma, content, factors, board.unit), dtype=object).sum())

    amplitude = 2000
    for _ in range(5):
        amplitude = isqrt(amplitude * amplitude * quanta * unit_k // share_of(amplitude))
    re_now, re_before, im_now, im_before = levels(amplitude)
    laid(board, k, first, (re_now.astype(kind), re_before.astype(kind)), None, None)
    laid(board, k, first + 1, (im_now.astype(kind), im_before.astype(kind)), None, None)
    total = int(np.where(record_share(board, k, r) > 0, record_share(board, k, r), 0).sum())
    return {"pair": [num, den], "g_milli": 1000 * (den - num) // den, "centre": list(at), "sense": sense, "record": r, "quanta": quanta,
            "amplitude": amplitude, "c_lay": c_lay, "share_quanta_milli": 1000 * total // unit_k, "unit": unit_k,
            "nodes_laid": int(sum(1 for v in re_now.reshape(-1) if int(v) != 0)), "largest_level": int(max(abs(int(v)) for v in re_now.reshape(-1)))}


def body_forms(board: Lattice, seed_list: list[dict[str, Any]], notes: dict[str, Any]) -> None:
    """The gapped pairs' packets laid at the interval 0 after the start, the records born at their first lay."""
    light = board.world.seed
    pairs = {tuple(f.pair): i for i, f in enumerate(board.families)}
    for item in seed_list:
        if "at" not in item:
            continue
        form = item["at"]
        pair = tuple(int(x) for x in form["pair"])
        if pair == tuple(board.families[light].pair):
            continue
        if pair not in pairs:
            refuse(f"the pair {list(pair)} is no row of the universe (the rows' pairs are the universe's numbers)")
        if int(form.get("sigma_tenths", 0)) == 0:
            refuse("a one-Node body: a body is laid over its packet and never at one Node (G-S2, the owner's reading under measurement)")
        if int(form.get("sigma_tenths", 0)) != 12:
            refuse("the packet's width here is sigma 1.22 Links (sigma_tenths 12, the binomial C(6, 3 + x)); no other integer profile is laid")
        k = pairs[pair]
        board.born_point(k)
        found = lay_body(board, k, int(form.get("record", 0)), tuple(int(x) for x in form["centre"]), int(form.get("sense", 1)), int(form["quanta"]))
        notes.setdefault("bodies", []).append(found)


def record_share(board: Lattice, k: int, r: int) -> np.ndarray:
    content, factors = board.read(k, 1, r)
    own = share.family_share(board.families[k], board.lines_of(k, r), board.world.node_clock, content, factors, board.unit)
    return np.asarray(own, dtype=object)


def torus_distance(a: Node, b: Node, shape: tuple[int, ...]) -> int:
    return sum(min((x - y) % n, (y - x) % n) for x, y, n in zip(a, b, shape, strict=True))


def body_readings(board: Lattice, centres: list[Node] | None = None) -> dict[str, Any]:
    """Per born record: its quanta (milli), the peak Node with its quanta, the share within one Link of the peak, the Wronskian's
    sign; per lay centre (the bodies' seed) the share within one Link of the centre and the local peak within two Links of it
    with its offset; the pairs of records at or above one whole quantum with their peaks' torus distance (adjacent peaks W-S5's
    predicate), and per record the distance between the local peaks of the two centres."""
    shape = board.shape
    rows = []
    centres = centres or []
    for k in board.order:
        fam = board.families[k]
        if not fam.plane or not board.states[k].lines:
            continue
        unit = board.credit.units[k]
        for r in range(registry.records_of(fam, board.states[k].lines)):
            s = record_share(board, k, r)
            s = np.where(s > 0, s, 0)
            total = int(s.sum())
            if total == 0:
                continue
            flat = [int(v) for v in s.reshape(-1)]
            peak_i = max(range(len(flat)), key=flat.__getitem__)
            peak = tuple(int(x) for x in np.unravel_index(peak_i, shape))
            d = manhattan(shape, peak)
            within1 = sum(v for v, dd in zip(flat, d.reshape(-1), strict=True) if int(dd) <= 1)
            w = board.lines_of(k, r)
            wr = 0
            for re, im in zip(w[0::2], w[1::2], strict=True):
                wr += int(np.asarray(re.now * im.before - im.now * re.before, dtype=object).sum())
            row = {"family": fam.name, "pair": list(fam.pair), "record": r, "quanta_milli": 1000 * total // unit, "peak": list(peak),
                   "peak_quanta_milli": 1000 * flat[peak_i] // unit, "within1_milli": 1000 * within1 // total, "wronskian_sign": (wr > 0) - (wr < 0)}
            locals_ = []
            for c in centres:
                dc = manhattan(shape, c).reshape(-1)
                near = [i for i in range(len(flat)) if int(dc[i]) <= 2]
                li = max(near, key=flat.__getitem__)
                lp = tuple(int(x) for x in np.unravel_index(li, shape))
                w1 = sum(v for v, dd in zip(flat, dc, strict=True) if int(dd) <= 1)
                locals_.append({"centre": list(c), "within1_of_centre_milli": 1000 * w1 // total, "local_peak": list(lp),
                                "local_peak_quanta_milli": 1000 * flat[li] // unit, "offset_from_centre": torus_distance(lp, c, shape)})
            if len(locals_) >= 2:
                row["local_peaks_distance"] = torus_distance(tuple(locals_[0]["local_peak"]), tuple(locals_[1]["local_peak"]), shape)
            if locals_:
                row["at_centres"] = locals_
            rows.append(row)
    whole = [row for row in rows if row["quanta_milli"] >= 1000]
    pairs = []
    for i in range(len(whole)):
        for j in range(i + 1, len(whole)):
            a, b = whole[i], whole[j]
            pairs.append({"a": [a["family"], a["record"]], "b": [b["family"], b["record"]], "distance": torus_distance(tuple(a["peak"]), tuple(b["peak"]), shape),
                          "senses": [a["wronskian_sign"], b["wronskian_sign"]]})
    largest = max((row["quanta_milli"] for row in rows), default=0)
    return {"records": rows, "records_whole": len(whole), "largest_record_quanta_milli": largest,
            "pairs_within_one_link": sum(1 for p in pairs if p["distance"] <= 1), "pairs_adjacent": sum(1 for p in pairs if p["distance"] == 1),
            "pairs_same_node": sum(1 for p in pairs if p["distance"] == 0), "pairs": pairs[:60]}


def integers_at_node(board: Lattice) -> tuple[int, int, str]:
    count, found, where = 0, 0, ""
    for fam, st in zip(board.families, board.states, strict=True):
        count += 3 * len(st.lines) + len(st.write_remainders) + 3 * sum(len(row) for row in st.phases)
        arrays = [(f"{fam.name} line {n} {name}", getattr(line, name)) for n, line in enumerate(st.lines) for name in ("now", "before", "remainder")]
        arrays += [(f"{fam.name} write {n}", w) for n, w in enumerate(st.write_remainders)]
        arrays += [(f"{fam.name} row {rr} phase {n} {name}", getattr(line, name)) for rr, row in enumerate(st.phases) for n, line in enumerate(row) for name in ("now", "before", "remainder")]
        for label, arr in arrays:
            b = max(int(abs(int(v))).bit_length() for v in np.asarray(arr, dtype=object).reshape(-1))
            if b > found:
                found, where = b, label
    return count, found, where


def cube_48() -> list[tuple[tuple[int, int, int], tuple[int, int, int]]]:
    return [(p, s) for p in permutations(range(3)) for s in product((1, -1), repeat=3)]


def image_node(node: Node, element: Any, centre: Node, shape: tuple[int, ...]) -> Node:
    permutation, signs = element
    off = [((node[a] - centre[a] + shape[a] // 2) % shape[a]) - shape[a] // 2 for a in range(3)]
    moved = [0, 0, 0]
    for a in range(3):
        moved[permutation[a]] = signs[a] * off[a]
    return tuple((centre[a] + moved[a]) % shape[a] for a in range(3))


def clicks_48(lines: list[dict[str, Any]], centre: Node, shape: tuple[int, ...]) -> dict[str, Any]:
    """The clicks' images under the 48 about `centre`: the multiset of (interval, event, family, node, sense) of the credit and
    birth lines against its image, the count of elements under which they are equal (the symmetry in the clicks)."""
    found = []
    for line in lines:
        if line.get("event") == "credit":
            found.append((line["interval"], "credit", line.get("family"), tuple(np.unravel_index(line["node_detector"], shape)), line.get("sense")))
        elif line.get("event") == "birth":
            for node, sense, child in zip(line.get("nodes") or [], line.get("senses") or [], line.get("children") or [], strict=False):
                found.append((line["interval"], "birth", child, tuple(int(x) for x in node), sense))
    base = sorted(found)
    kept = 0
    for element in cube_48():
        image = sorted((t, e, f, image_node(n, element, centre, shape), s) for t, e, f, n, s in found)
        kept += image == base
    return {"elements_keeping_the_clicks": kept, "lines_read": len(found)}


def run(args: argparse.Namespace) -> None:
    world_path = Path(args.world).resolve()
    generic = json.loads(world_path.read_text(encoding="utf-8"))
    seed_list = generic.pop("seed")
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    folder = Path(args.scratch) if args.scratch else out
    folder.mkdir(parents=True, exist_ok=True)
    universe = json.loads((world_path.parent / generic["universe"]).read_text(encoding="utf-8"))
    (folder / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    stripped = {**generic, "universe": "u.json"}
    (folder / "w.json").write_text(json.dumps(stripped), encoding="utf-8")
    world_files.REPOSITORY_ROOT = folder
    notes: dict[str, Any] = {"seed": seed_list}
    name = world_path.stem
    clicks_path, eras_path, nodes_path = (out / f"{name}.{kind}.jsonl" for kind in ("clicks", "eras", "nodes"))
    refused_path, readings_path = out / f"{name}.refused.jsonl", out / f"{name}.readings.jsonl"
    all_lines: list[dict[str, Any]] = []
    kept_clicks = clicks_path.open("w", encoding="utf-8")
    kept_refused = refused_path.open("w", encoding="utf-8")

    def keep(line: dict[str, object]) -> None:
        all_lines.append(line)
        if line.get("event") in ("click", "density", "credit", "lay", "birth"):
            kept_clicks.write(json.dumps(line) + "\n")
        elif line.get("event") == "refused":
            kept_refused.write(json.dumps(line) + "\n")

    seed.uniform_seed = lambda board, index: light_forms(board, index, seed_list, notes)
    began = time.perf_counter()
    board = Lattice(load_world(folder / "w.json"), output=keep)
    body_forms(board, seed_list, notes)
    count0, bits0, where0 = integers_at_node(board)
    notes["integers_per_node_at_start"], notes["largest_bits_at_start"] = count0, [bits0, where0]
    notes["load_seconds"] = round(time.perf_counter() - began, 2)
    light = board.world.seed
    quanta0, _frozen = board.quanta(light)
    notes["light_quanta_per_node_at_start"] = {str(k): v for k, v in sorted(dict(zip(*np.unique(np.asarray(quanta0, dtype=object).astype(int), return_counts=True), strict=True)).items())}
    centre = tuple(int(x) for x in (args.centre or [0, 0, 0]))
    centres = [tuple(int(x) for x in item["at"]["centre"]) for item in seed_list if "at" in item and tuple(item["at"]["pair"]) != tuple(board.families[light].pair)]
    centres = list(dict.fromkeys(centres))
    if args.check_lay:
        light_arr = np.asarray(board.states[light].lines[0].now, dtype=object)
        kept48 = sum(1 for g in cube_48() if all(int(light_arr[image_node(n, g, centre, board.shape)]) == int(light_arr[n]) for n in np.ndindex(*board.shape)))
        notes["light_lay_48_about_centre"] = {"centre": list(centre), "elements_keeping_the_lay": kept48}
    intervals = int(args.intervals or generic["intervals"])
    directions = [1] * int(np.prod(board.shape))
    snapshots: dict[int, Any] = {}
    window = intervals if args.run_back == "all" else int(args.run_back)
    if window:
        snapshots[0] = snapshot(board)
    readings = readings_path.open("w", encoding="utf-8")
    readings.write(json.dumps({"event": "notes", **notes}, default=str) + "\n")
    print(json.dumps({"event": "notes", **{k: v for k, v in notes.items() if k != "seed"}}, default=str), flush=True)
    with eras_path.open("w", encoding="utf-8") as log, nodes_path.open("w", encoding="utf-8") as kept_nodes:
        log.write(json.dumps(eras.header_of(folder / "w.json", board, intervals)) + "\n")
        previous = None
        births_by_interval: dict[int, int] = {}
        for t in range(1, intervals + 1):
            kept = eras.kept_lines(board)
            time_line = board.states[board.held[0]].lines[0]
            before = (eras.whole(time_line.now), eras.whole(time_line.before))
            n_lines = len(all_lines)
            try:
                board.step()
            except (ValueError, RuntimeError) as refusal:
                line = {"interval": board.interval, "refused": str(refusal), "seconds": time.perf_counter() - began}
                log.write(json.dumps(line) + "\n")
                print(json.dumps(line), flush=True)
                break
            line = eras.interval_line(board, kept, time.perf_counter() - began)
            eras.volume_residuals(previous, line)
            previous = line
            log.write(json.dumps(line) + "\n")
            kept_nodes.write(json.dumps(eras.node_lines(board, before, directions)) + "\n")
            new = all_lines[n_lines:]
            births_by_interval[t] = sum(1 for l in new if l.get("event") == "birth")
            if window and t >= intervals - window:
                snapshots[t] = snapshot(board)
            if t % args.read_every == 0 or t == intervals or t <= 3:
                count, bits, where = integers_at_node(board)
                held = board.states[board.held[0]].lines[0]
                levels = volume.level_of(board.world.node_clock, np.asarray(held.now, dtype=object))
                flat = [int(v) for v in np.asarray(levels, dtype=object).reshape(-1)]
                reading = {"event": "reading", "interval": t, "seconds": round(time.perf_counter() - began, 1), "births": births_by_interval[t],
                           "credits": sum(1 for l in new if l.get("event") == "credit"), "refused": sum(1 for l in new if l.get("event") == "refused"),
                           "turned": int(board.turned.sum()), "integers_per_node": count, "largest_bits": [bits, where],
                           "content_levels_min_max": [min(flat), max(flat)], "content_at_centre": flat[int(np.ravel_multi_index(centre, board.shape))],
                           "light_quanta": line["quanta"][board.families[light].name].get("quanta"), "bodies": body_readings(board, centres)}
                readings.write(json.dumps(reading, default=str) + "\n")
                readings.flush()
                short = {k: v for k, v in reading.items() if k != "bodies"}
                short["bodies"] = {k: v for k, v in reading["bodies"].items() if k not in ("records", "pairs")}
                print(json.dumps(short, default=str), flush=True)
    kept_clicks.close()
    kept_refused.close()
    end = board.interval
    summary: dict[str, Any] = {"event": "summary", "end_interval": end, "seconds": round(time.perf_counter() - began, 1),
                               "births": sum(births_by_interval.values()), "births_first_last": [min((t for t, n in births_by_interval.items() if n), default=None), max((t for t, n in births_by_interval.items() if n), default=None)],
                               "credits": sum(1 for l in all_lines if l.get("event") == "credit"), "refused_lines": sum(1 for l in all_lines if l.get("event") == "refused"),
                               "swap_fires_total": sum(n for at, d, n in board.swaps if d == 1), "swap_fire_intervals": len({at for at, d, n in board.swaps if d == 1}),
                               "clicks_48": clicks_48(all_lines, centre, board.shape)}
    if window and end > 0:
        t0 = time.perf_counter()
        matched, miss = 0, None
        back = min(window, end)
        for _ in range(back):
            crossed(board, all_lines)
            try:
                board.step_inverse()
            except RuntimeError as refusal:
                miss = {"refused": str(refusal), "interval": board.interval}
                break
            found = first_difference(snapshots[board.interval], snapshot(board))
            if found is not None:
                miss = {"interval": board.interval, "array": found[0], "node": list(map(int, found[1])) if hasattr(found[1], "__iter__") else found[1]}
                break
            matched += 1
        summary["run_back"] = {"verdict": "MATCH" if miss is None else "MISS", "intervals_back": matched, "of": back, "miss": miss, "seconds": round(time.perf_counter() - t0, 1)}
    readings.write(json.dumps(summary, default=str) + "\n")
    readings.close()
    print(json.dumps(summary, default=str), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("world", help="the generic world file with its seed list")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--scratch", default=None, help="the folder the stripped world and the universe are written to (TMPDIR)")
    parser.add_argument("--intervals", type=int, default=None)
    parser.add_argument("--read-every", type=int, default=10)
    parser.add_argument("--run-back", default="40", help="all, or the window's intervals, or 0")
    parser.add_argument("--centre", type=int, nargs=3, default=None, help="the Node the 48 are read about (the hole, or the wave's centre)")
    parser.add_argument("--check-lay", action="store_true")
    run(parser.parse_args())


if __name__ == "__main__":
    main()
