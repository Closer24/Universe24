"""Hand g3's toy (2026-10-25, engine-5.0-test at 9f1f27106; no edit under src/): one body of one quantum of a gapped lift on a
bare torus with the sea emptied, the volume holder's time line set by hand, every other act the engine's. The lay is the
engine's one-Node lay by the count (`--lay point`, emission.laid_by_count, the click's own) or a standing packet of the record's
rest rotation laid through the one lay act over several Nodes (`--lay wide --sigma S`: the plane z_now = A_i,
z_before = A_i e^(i sense omega_0) in integers, A_i a Gaussian of rms S Links, its total share one quantum of the record's unit
to the rounding; the law's lay act, not a declared packet). The volume: `--hold none` the law's letter (the line set once and
stepped by its own Rule3, the swap at the top acting), `--hold rising` the deviation named: the time line re-set before every
interval to the hand profile X(c) with the level before X - d_i, d_i the least rise at which no Node tops (the swap's trigger
X2 <= X1 avoided), the hand-held well standing for the whole run and the body's own write (one level) overwritten; the run back
undoes the hand-sets in reverse order between the engine's inverse steps. The well: `--well-depth D` levels at `--well-offset R`
Links from the body along z with the profile c(r) = D div (1 + r), r the torus distance in Links (W2's), or a flat board at the
uniform content `--content C` (the beat test). Two bodies: `--pair 3` lays a second one-quantum body three Links away on z
(record 1, sense +1).

Readings per interval, integers only (Addition 3): the record's share s_i (share.family_share at the paces of its read, the
current's units, Python's integers); its total S; the peak Node; the share within 1, 2 and 3 Links of the lay Node and of the
peak as thousandths of S; the first moment along z about the lay Node, (1000 M_z) div S with its remainder, the centroid in
thousandths of a Link; the second moment, (1000 SUM s_i r_i^2) div S, the squared radius about the lay Node in thousandths; the
content c at the lay Node and at the well's centre; the Nodes turned by the swap; the proper count at the lay Node and at the
well's centre; the upward zero crossings of the record's first line at the lay Node and at the peak (the beat); every credit,
birth and refusal line; at the end the run back (MATCH when every array returns to the laid state). Floats stand nowhere.
Run: PYTHONPATH=<worktree>/src TMPDIR=/dev/shm/tmp python tools/derivations/open_items/H-Gap-Of-The-Middle-3/body_toy.py --den 24523373 --cube 9 --lay wide
     --sigma 2 --hold rising --well-depth 300 --well-offset 3 --intervals 200 --run-back --out <file>.jsonl
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # the worktree root: tests.laws_universe

from event_universe import emission, meeting_board, records, share, world_files  # noqa: E402
from event_universe.core import paces  # noqa: E402
from event_universe.core.rule3 import division_forward  # noqa: E402
from event_universe.features import volume  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.lay import laid  # noqa: E402
from event_universe.loader import circle  # noqa: E402
from event_universe.take import Item  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402
from tests.laws_universe import light_emptied, node_arrays, time_line_set  # noqa: E402

GAMMA, ACTION = 1000, 36000


def torus_offset(at, origin, cube):
    found = []
    for a, o in zip(at, origin, strict=True):
        d = (a - o) % cube
        if d > cube // 2:
            d -= cube
        found.append(d)
    return tuple(found)


def offsets(shape, origin):
    """Per Node the torus offset from `origin` on each axis (integer arrays) and the squared distance."""
    cube = shape[0]
    idx = np.indices(shape)
    offs = []
    for a in range(3):
        d = (idx[a] - origin[a]) % cube
        d = np.where(d > cube // 2, d - cube, d)
        offs.append(d.astype(object))
    r2 = offs[0] * offs[0] + offs[1] * offs[1] + offs[2] * offs[2]
    return offs, r2


def well_levels(shape, centre, depth):
    """c(r) = depth div (1 + r), r the torus distance (the integer root of the squared distance) in Links."""
    _offs, r2 = offsets(shape, centre)
    found = np.zeros(shape, dtype=object)
    for at in np.ndindex(*shape):
        r = math.isqrt(int(r2[at]))
        found[at] = depth // (1 + r)
    return found


def lift_family(board, g_target_thousandths):
    """The lift (a point of one prime at its whole power) whose g is nearest the target, as (index, name, num, den)."""
    best = None
    for index, family in enumerate(board.families):
        if not (family.plane and family.quanta):
            continue
        vector = circle.vector_of(family.name)
        if vector is None or sum(1 for v in vector if v) != 1:
            continue
        num, den = family.pair
        g_th = (den - num) * 1000 // den
        if best is None or abs(g_th - g_target_thousandths) < abs(best[0] - g_target_thousandths):
            best = (g_th, index, family.name, num, den)
    assert best is not None
    return best[1:]


def record_share(board, k, r):
    content, factors = board.read(k, 1, r)
    found = share.family_share(board.families[k], board.lines_of(k, r), board.world.node_clock, content, factors, board.unit)
    return np.asarray(found, dtype=object)


def lay_wide(board, k, record, at, sense, sigma_tenths, quanta=1):
    """The standing packet laid through the one lay act: A_i = A0 exp(-r_i^2 / (4 sigma^2)) in integers (the exponential by the
    integer power of a rational, no float), re (A_i, A_i num div den), im (0, sense A_i s div den), the total share scaled to one
    quantum of the record's unit by one measured rescale; returns the laid amplitudes' sum of squares and the share in units."""
    family = board.families[k]
    num, den = family.pair
    s = paces.sine_den(num, den)
    board.born_point(k)
    _offs, r2 = offsets(board.shape, at)
    # the Gaussian in integers: weight_i = 2^20 x exp(-r2 / (4 sigma^2)); exp by the series in rationals to 12 terms, floor
    sigma2_x4 = 4 * sigma_tenths * sigma_tenths  # in hundredths of a Link squared
    weights = np.zeros(board.shape, dtype=object)
    for node in np.ndindex(*board.shape):
        x_num, x_den = int(r2[node]) * 100, sigma2_x4  # x = r2 / (4 sigma^2)
        term_num, term_den, total_num, total_den = 1, 1, 1, 1
        for n in range(1, 14):  # exp(-x) = SUM (-x)^n / n!
            term_num, term_den = -term_num * x_num, term_den * x_den * n
            total_num, total_den = total_num * term_den + term_num * total_den, total_den * term_den
        if x_num * 1 > 12 * x_den:  # beyond x = 12 the series alternates badly: the weight is 0 at this scale
            weights[node] = 0
        else:
            weights[node] = max(0, (total_num << 20) // total_den)

    def pairs_of(scale_num, scale_den):
        amp = np.zeros(board.shape, dtype=object)
        for node in np.ndindex(*board.shape):
            amp[node] = (int(weights[node]) * scale_num) // scale_den
        re = (amp, np.asarray([[[int(a) * num // den for a in row] for row in plane] for plane in amp], dtype=object))
        im = (np.zeros(board.shape, dtype=object), np.asarray([[[sense * (int(a) * s // den) for a in row] for row in plane] for plane in amp], dtype=object))
        return amp, re, im

    # the dry run: the share of trial amplitudes at the vacuum's paces, then one rescale to one quantum
    unit = board.credit.units[k]
    trial_num, trial_den = 1 << 7, 1 << 20  # A0 = 128 at the centre
    amp, re, im = pairs_of(trial_num, trial_den)
    zeros = np.zeros(board.shape, dtype=object)
    trial = share.family_share(family, [records.Record(re[0], re[1], zeros), records.Record(im[0], im[1], zeros)], GAMMA, 0, None, board.unit)
    total = int(np.asarray(trial, dtype=object).sum())
    # share scales as A^2: A0 = 128 x sqrt(unit / total)
    scale_num = math.isqrt((trial_num * trial_num * unit * quanta) // total) if total > 0 else trial_num
    for _round in range(2):  # the floors of the integer lay lose share: the scale corrected on the measured share
        amp, re, im = pairs_of(scale_num, trial_den)
        again = share.family_share(family, [records.Record(re[0], re[1], zeros), records.Record(im[0], im[1], zeros)], GAMMA, 0, None, board.unit)
        measured = int(np.asarray(again, dtype=object).sum())
        if measured <= 0:
            break
        scale_num = math.isqrt((scale_num * scale_num * unit * quanta) // measured)
    # the centre amplitude is an integer (scale_num = A0 at the 2^20 weight): the one whose measured share is nearest the target
    best = None
    for candidate in range(max(1, scale_num - 3), scale_num + 3):
        amp, re, im = pairs_of(candidate, trial_den)
        again = share.family_share(family, [records.Record(re[0], re[1], zeros), records.Record(im[0], im[1], zeros)], GAMMA, 0, None, board.unit)
        measured = int(np.asarray(again, dtype=object).sum())
        if best is None or abs(measured - unit * quanta) < best[0]:
            best = (abs(measured - unit * quanta), candidate)
    scale_num = best[1]
    amp, re, im = pairs_of(scale_num, trial_den)
    origin = board.half_wall(k)
    mask = np.ones(board.shape, dtype=bool)
    lines = emission.emitted_lines(family, record)
    for number, (now, was) in zip(lines, (re, im), strict=True):
        laid(board, k, number, (now, was), None, origin, mask)
    board.credit.counts[k] += quanta
    laid_share = record_share(board, k, record)
    sum_sq = int(sum(int(a) * int(a) for a in amp.reshape(-1)))
    return {"A0": int(amp[at]), "sum_A2": sum_sq, "sine_den": s, "share_total": int(laid_share.sum()), "unit": unit,
            "quanta_quotient_remainder": list(divmod(int(laid_share.sum()), unit))}


def rising_before(board, x_now):
    """The level before at every Node, X - d_i, with d_i the least rise at which the holder's own step does not top: the
    engine's own coefficients of the holder's line at the Node's content (core/rule3.coefficients at the paces of the read, no
    tension), w X2 = SUM_j R_j X_j + S X1 - w X0 + r, so X2 >= floor((SUM_j R_j X_j + S X1) / w) - X0; the before X0 = X1 - d
    with d = X1 + 2 - floor(...) makes X2 >= X1 + 2 > X1 at every Node (the swap's weak maximum X2 <= X1 avoided), and the
    held write adds a level at or above 0."""
    from event_universe.core.rule3 import coefficients

    vol = board.held[0]
    num, den = board.families[vol].pair
    x = np.asarray(x_now, dtype=object)
    content = np.asarray(volume.level_of(GAMMA, x), dtype=object)
    clock, pace = paces.node_paces(GAMMA, content)
    reads, self_coefficient, wall = coefficients(num, den, GAMMA, clock, pace, None, board.unit)
    s6 = np.zeros(board.shape, dtype=object)
    for axis in range(3):
        s6 = s6 + np.roll(x, 1, axis=axis) + np.roll(x, -1, axis=axis)
    read0 = np.asarray(reads[0], dtype=object)  # every Port's reach alike at the Node without tension
    total = read0 * s6 + np.asarray(self_coefficient, dtype=object) * x
    floor = np.asarray(division_forward(total, np.asarray(wall, dtype=object), 0)[0], dtype=object)
    d = x + x + 2 - floor
    d = np.where(d < 3, 3, d).astype(object)
    return x - d


def moments(s, at, cube):
    """The integer moments of the share about `at`: the total, the first moment on z, the second moment, the share within 1, 2, 3 Links."""
    offs, r2 = offsets(s.shape, at)
    total = int(s.sum())
    mz = int((s * offs[2]).sum())
    m2 = int((s * r2).sum())
    within = []
    for reach in (1, 2, 3):
        within.append(int(s[np.asarray(r2 <= reach * reach, dtype=bool)].sum()))
    return total, mz, m2, within


def thousandths(numerator, total):
    if total <= 0:
        return [None, None]
    q, r = divmod(1000 * numerator, total)
    return [int(q), int(r)]


def snapshot(board):
    return {k: tuple(np.asarray(a, dtype=object).copy() for a in v) for k, v in node_arrays(board).items()}


def differing(a, b):
    count = 0
    for key in set(a) | set(b):
        if key not in a or key not in b:
            count += 1
            continue
        for x, y in zip(a[key], b[key], strict=False):
            if np.shape(x) != np.shape(y) or not np.array_equal(np.asarray(x, dtype=object), np.asarray(y, dtype=object)):
                count += 1
                break
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--den", type=int, required=True)
    parser.add_argument("--cube", type=int, default=9)
    parser.add_argument("--g-target", type=int, default=650, help="the lift nearest this g in thousandths")
    parser.add_argument("--lay", choices=("point", "wide"), default="wide")
    parser.add_argument("--sigma", type=int, default=20, help="the packet's rms width in tenths of a Link")
    parser.add_argument("--hold", choices=("none", "rising"), default="rising")
    parser.add_argument("--well-depth", type=int, default=0)
    parser.add_argument("--well-offset", type=int, default=3)
    parser.add_argument("--content", type=int, default=0, help="the flat board's uniform content (levels)")
    parser.add_argument("--pair", type=int, default=0, help="a second body this many Links away on z")
    parser.add_argument("--quanta", type=int, default=1, help="the body's quanta (the wide lay; the point lay by the count)")
    parser.add_argument("--intervals", type=int, default=200)
    parser.add_argument("--run-back", action="store_true", default=False)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    folder = Path(f"/dev/shm/tmp/g3_{Path(args.out).stem}")
    folder.mkdir(parents=True, exist_ok=True)
    world_files.REPOSITORY_ROOT = folder
    (folder / "u.json").write_text(json.dumps({"integers": {"den": args.den, "node_clock": GAMMA, "quantum_action": ACTION}}))
    (folder / "w.json").write_text(json.dumps({"universe": "u.json", "shape": [args.cube] * 3, "intervals": args.intervals}))
    lines: list[dict] = []
    t_load = time.time()
    board = Lattice(load_world(folder / "w.json"), output=lines.append)
    meeting_board.child_of = lambda b, i, v, w: ()  # the toy's deviation: the sea's births refused by name (the sea is emptied anyway)
    light_emptied(board)
    k, name, num, den = lift_family(board, args.g_target)
    vol = board.held[0]
    centre = args.cube // 2
    at = (centre, centre, centre)
    well_centre = (centre, centre, (centre + args.well_offset) % args.cube)
    # the hand profile of the volume's level
    if args.well_depth:
        levels = well_levels(board.shape, well_centre, args.well_depth)
    else:
        levels = np.full(board.shape, args.content, dtype=object)
    x_hand = np.asarray(volume.volume_of(GAMMA, levels), dtype=object)
    if args.hold == "rising":
        time_line_set(board, x_hand, rising_before(board, x_hand))
    else:
        time_line_set(board, x_hand, x_hand.copy())
    bodies = []
    lays = []
    if args.lay == "point":
        emission.laid_by_count(board, Item(k, args.quanta, (at,), (den, den), sense=1, record=0))
        lays.append({"record": 0, "at": list(at), "lay": "point", "quanta": args.quanta})
    else:
        lays.append({"record": 0, "at": list(at), "lay": "wide", **lay_wide(board, k, 0, at, 1, args.sigma, args.quanta)})
    bodies.append((0, at))
    if args.pair:
        at_b = (centre, centre, (centre + args.pair) % args.cube)
        if args.lay == "point":
            emission.laid_by_count(board, Item(k, 1, (at_b,), (den, den), sense=1, record=1))
            lays.append({"record": 1, "at": list(at_b), "lay": "point"})
        else:
            lays.append({"record": 1, "at": list(at_b), "lay": "wide", **lay_wide(board, k, 1, at_b, 1, args.sigma, args.quanta)})
        bodies.append((1, at_b))
    header = {"event": "header", "den": args.den, "den_bits": args.den.bit_length(), "factors": {str(p): e for p, e in circle.factors(args.den).items()},
              "cube": args.cube, "intervals": args.intervals, "family": name, "pair": [num, den], "g_thousandths": list(divmod((den - num) * 1000, den)),
              "sine_den": paces.sine_den(num, den), "unit_record": board.credit.units[k], "lay": args.lay, "sigma_tenths": args.sigma,
              "hold": args.hold, "quanta": args.quanta, "well_depth": args.well_depth, "well_centre": list(well_centre), "content": args.content, "pair": args.pair,
              "width_bits": board.world.width.bit_length(), "amplitude_bound": board.world.amplitude_bound, "families": len(board.families),
              "lays": lays, "load_seconds": round(time.time() - t_load, 2)}
    crossings = {r: {"lay": 0, "peak": 0} for r, _ in bodies}
    saved = []  # the holder's time line as the engine left it, per interval, for the run back
    with open(args.out, "w") as f:
        f.write(json.dumps(header) + "\n")
        start = snapshot(board)
        t0 = time.time()
        for step in range(args.intervals + 1):
            x = np.asarray(board.states[vol].lines[0].now, dtype=object)
            c = volume.level_of(GAMMA, x)
            row = {"event": "reading", "interval": board.interval, "bodies": [], "turned": int(np.asarray(board.turned).sum()),
                   "c_lay": int(c[at]), "c_well": int(c[well_centre]), "c_min": int(c.min()), "c_max": int(c.max()),
                   "proper_lay": int(board.proper_count[at]), "proper_well": int(board.proper_count[well_centre])}
            for r, lay_at in bodies:
                s = record_share(board, k, r)
                s = np.where(np.asarray(s, dtype=object) > 0, s, 0).astype(object)
                total, mz, m2, within = moments(s, lay_at, args.cube)
                flat = np.asarray(s, dtype=object).reshape(-1)
                peak_index = max(range(flat.size), key=lambda i: int(flat[i]))
                peak = tuple(int(i) for i in np.unravel_index(peak_index, s.shape))
                _t, _mz, _m2, within_peak = moments(s, peak, args.cube)
                line0 = board.lines_of(k, r)[0]
                up_lay = bool(line0.before[lay_at] < 0 <= line0.now[lay_at])
                up_peak = bool(line0.before[peak] < 0 <= line0.now[peak])
                crossings[r]["lay"] += int(up_lay)
                crossings[r]["peak"] += int(up_peak)
                row["bodies"].append({
                    "record": r, "peak_offset": list(torus_offset(peak, lay_at, args.cube)), "total": total,
                    "quanta": list(divmod(total, board.credit.units[k])) if total else [0, 0],
                    "centroid_z_thousandths": thousandths(mz, total), "radius2_thousandths": thousandths(m2, total),
                    "within_1_2_3_of_lay_thousandths": [thousandths(w, total)[0] for w in within],
                    "within_1_2_3_of_peak_thousandths": [thousandths(w, total)[0] for w in within_peak],
                    "share_lay_thousandths": thousandths(int(s[lay_at]), total)[0],
                    "crossings_lay": crossings[r]["lay"], "crossings_peak": crossings[r]["peak"],
                    "now_before_lay": [int(line0.now[lay_at]), int(line0.before[lay_at])],
                })
            if len(bodies) == 2:
                za = row["bodies"][0]["centroid_z_thousandths"][0]
                zb = row["bodies"][1]["centroid_z_thousandths"][0]
                row["separation_z_thousandths"] = (1000 * args.pair + zb - za) if za is not None and zb is not None else None
                pa = torus_offset(tuple(np.array(bodies[0][1]) + np.array(row["bodies"][0]["peak_offset"])), (0, 0, 0), args.cube)
                pb = torus_offset(tuple(np.array(bodies[1][1]) + np.array(row["bodies"][1]["peak_offset"])), (0, 0, 0), args.cube)
                row["peak_distance"] = sum(abs(d) for d in torus_offset(pb, pa, args.cube))
            row["seconds"] = round(time.time() - t0, 1)
            f.write(json.dumps(row) + "\n")
            if step == args.intervals:
                break
            if args.hold == "rising":
                line = board.states[vol].lines[0]
                saved.append((np.asarray(line.now, dtype=object).copy(), np.asarray(line.before, dtype=object).copy()))
                time_line_set(board, x_hand, rising_before(board, x_hand))
            n_before = len(lines)
            board.step()
            for li in lines[n_before:]:
                if li.get("event") in ("credit", "refused", "birth"):
                    f.write(json.dumps(li) + "\n")
        summary = {"event": "summary", "seconds": round(time.time() - t0, 1), "interval": board.interval,
                   "credits": sum(1 for li in lines if li.get("event") == "credit"),
                   "refused": sum(1 for li in lines if li.get("event") == "refused"),
                   "births": sum(1 for li in lines if li.get("event") == "birth"), "swaps": len(board.swaps),
                   "largest_bits": max(int(abs(int(v))).bit_length() for arrays in node_arrays(board).values() for a in arrays for v in np.asarray(a, dtype=object).reshape(-1))}
        if args.run_back:
            t1 = time.time()
            for _ in range(args.intervals):
                board.step_inverse()
                if args.hold == "rising":
                    now, before = saved.pop()
                    time_line_set(board, now, before)
            end = snapshot(board)
            summary["run_back"] = {"interval": board.interval, "arrays_differing": differing(start, end), "arrays": len(start),
                                   "seconds": round(time.time() - t1, 1),
                                   "verdict": "MATCH" if differing(start, end) == 0 and board.interval == 0 else "MISMATCH"}
        f.write(json.dumps(summary) + "\n")
    print(json.dumps(header))
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
