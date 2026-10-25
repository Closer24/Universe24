"""ol1's instrument: a world run `intervals` forward on the engine PYTHONPATH names (src or src_ol1 under its flags), with an
optional lay by this script after the world file's lays (a JSON spec): {"beam": {...}} the BEAM, a record with a gap laid at every
Node as a quarter-turn plane wave along one axis, z(x) = i^(wave x) z_rest (the rest lay's levels turned a quarter per Node along
the axis; wave 0 the uniform rest lay bit for bit), the rotation remainders of the negated lines mirrored to wall - 1 - r (the
exact image under the quarter turn, cs1's mirror), the least amplitude whose share at the origin is at or above `quanta` units;
or cs7's cycle pattern on the gap-0 plane (cs5_run.lay_pattern, the pattern file's keys). The WHOLE state of the board kept at
every interval (every line's now, before, rotation remainder and write remainder at every Node); for every top where the whole
board turned, the fall compared with the mirror of the rise over every Node and every line: S(top + k) against E(S(top - 1 - k)),
E the exchange and the conjugation with the remainders mirrored by the one rule as node.exchange and the engine's gram.conjugation
(the copy's K under its flag) give it; the first k that parts, the lines that part at it with the first Node's integers; the
bottoms, the exact returns to Gamma at every Node, the credits and the laid-back count, the records' current and charge at the
origin per interval, the shape-4 row's four levels at the origin per interval, the run back of `back` intervals by the state hash,
the census. Integers only. Usage: ol1_run.py <world.json> <intervals> <back> <out.json> [lay.json]"""
import json
import os
import sys
import time

sys.set_int_max_str_digits(0)
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from event_universe import gram, readings  # noqa: E402
from event_universe.core.paces import sine_den  # noqa: E402
from event_universe.core.rule3 import mirrored, quotient  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER, POTENTIAL, Line, zeros  # noqa: E402

ORIGIN = (0, 0, 0)
TURNS = 4


def at0(a):
    return int(np.asarray(a)[ORIGIN]) if np.ndim(a) else int(a)


def turned_quarter(re, im, q):
    """(re, im) turned by q quarters: i^q z."""
    q = q % TURNS
    if q == 0:
        return re, im
    if q == 1:
        return -im, re
    if q == 2:
        return -re, -im
    return im, -re


def beam_levels(node, row, amplitude, sense, axis, wave):
    """The beam's four level arrays: the rest lay's scalars turned i^(wave x) at the Node's coordinate x along the axis."""
    rest = gram.rest(row.shape, amplitude, [1, 0], row.pair[0], node.den, sine_den(row.pair[0], node.den), sense)
    rn, rb, inow, ib = int(rest[0].now), int(rest[0].before), int(rest[1].now), int(rest[1].before)
    arrays = [zeros(node.shape) for _ in range(4)]
    phases = zeros(node.shape)
    for at in np.ndindex(*node.shape):
        q = (wave * at[axis]) % TURNS
        phases[at] = q
        a, b = turned_quarter(rn, inow, q)
        c, d = turned_quarter(rb, ib, q)
        arrays[0][at], arrays[1][at], arrays[2][at], arrays[3][at] = a, c, b, d
    return arrays, phases


def lay_beam(node, spec):
    row = node.by_index[int(spec["row"])]
    rec = node.records().index(row)
    sense, axis, wave = int(spec.get("sense", 1)), int(spec.get("axis", 0)), int(spec.get("wave", 1))
    rule = node.rule(row.pair, node.content(), node.link_factors())

    def share_min(amplitude):
        arrays, _p = beam_levels(node, row, amplitude, sense, axis, wave)
        lines = [Line(arrays[0], arrays[1], None, node.w), Line(arrays[2], arrays[3], None, node.w)]
        return min(int(v) for v in node.share(lines, rule).reshape(-1))

    if "amplitude" in spec:
        amplitude = int(spec["amplitude"])
    else:
        target = int(spec.get("quanta", 1)) * node.units[rec]
        high = 1
        while share_min(high) < target:
            high = high + high
        low = 0
        while high - low > 1:
            middle = int(quotient(low + high, 2))
            if share_min(middle) < target:
                low = middle
            else:
                high = middle
        amplitude = high
    arrays, phases = beam_levels(node, row, amplitude, sense, axis, wave)
    node.lay(rec, Ellipsis, tuple(arrays))
    mirrored_lines = 0
    if int(spec.get("mirror", 1)) == 1:
        re, im = row.lines
        for at in np.ndindex(*node.shape):
            q = int(phases[at])
            wall = int(np.asarray(re.wall)[at]) if np.ndim(re.wall) else int(re.wall)
            if q in (1, 2):
                re.rem[at] = wall - 1 - int(re.rem[at])
                mirrored_lines += 1
            if q in (2, 3):
                im.rem[at] = wall - 1 - int(im.rem[at])
                mirrored_lines += 1
    node.start_content, node.start_x = node.content(), node.row(CARRIER).lines[0].now
    frames = readings.frames(node, node.walled().lines[0].rem)
    current = gram.current(row.shape, [line.now for line in row.lines], frames)
    return {
        "event": "lay_beam", "i": 0, "row_index": int(spec["row"]), "line_pair": rec, "amplitude": amplitude,
        "sense": sense, "axis": axis, "wave": wave, "share_min": share_min(amplitude), "unit": node.units[rec],
        "mirrored_lines": mirrored_lines, "levels_at_origin": [at0(a) for a in arrays],
        "W_at_origin": at0(gram.charge(row.shape, row.lines)), "J_at_origin": [at0(j) for j in current],
    }


def names_of(node):
    found = []
    for r in node.rows_:
        tag = f"shape {r.shape}" + ("" if r.pair is None else f" gap {min(int(r.gap), 10**6)}") + (" (walled)" if r.wall is not None else "")
        for j in range(len(r.lines)):
            found.append(f"{tag} line {j}")
    return found


def state_of(node):
    """Every line of the board: (now, before, rem, wr) as object arrays (wr None where the line writes not), with the wall."""
    found = []
    for r in node.rows_:
        for line in r.lines:
            found.append((line.now.copy(), line.before.copy(), line.rem.copy(), None if line.wr is None else line.wr.copy(),
                          line.wall, line.wwall))
    return found


def exchanged(node, state):
    """The exchange and the conjugation of a kept state over the whole board, by node.exchange's rule with the engine's own K."""
    found = []
    i = 0
    for r in node.rows_:
        k = gram.conjugation(r.shape)
        n = len(r.lines)
        nows = [state[i + j][0] for j in range(n)]
        befores = [state[i + j][1] for j in range(n)]
        new_nows, new_befores = gram.matvec(k, befores), gram.matvec(k, nows)
        for j in range(n):
            reversals = 1 + (k[j][j] < 0)
            rem = mirrored(state[i + j][2], state[i + j][4], reversals)
            wr = None if state[i + j][3] is None else mirrored(state[i + j][3], state[i + j][5], reversals if os.environ.get("OL1_ODD", "") in ("exch", "exchkick") else 1)
            found.append((new_nows[j], new_befores[j], rem, wr, state[i + j][4], state[i + j][5]))
        i += n
    return found


def equal(a, b):
    return bool(np.all(np.asarray(a, dtype=object) == np.asarray(b, dtype=object)))


def line_equal(x, y):
    for f in range(4):
        if x[f] is None and y[f] is None:
            continue
        if not equal(x[f], y[f]):
            return False
    return True


def first_node_off(x, y):
    """The first Node (ndindex order) and field where two lines differ, with the integers."""
    fields = ("now", "before", "rem", "wr")
    for f in range(4):
        if x[f] is None:
            continue
        off = np.asarray(x[f], dtype=object) != np.asarray(y[f], dtype=object)
        if off.any():
            at = tuple(int(v) for v in np.argwhere(off)[0])
            return {"field": fields[f], "node": list(at), "fall": int(x[f][at]), "mirror of the rise": int(y[f][at]),
                    "difference": int(x[f][at]) - int(y[f][at]), "nodes off": int(off.sum())}
    return None


def main(argv):
    world_path, intervals, back, out_path = argv[1], int(argv[2]), int(argv[3]), argv[4]
    universe, world = load_world(world_path)
    node = Node(universe, world)
    lay_line = None
    if len(argv) > 5:
        spec = json.load(open(argv[5]))
        if "beam" in spec:
            lay_line = lay_beam(node, spec["beam"])
        else:
            import cs5_run
            lay_line = {k: v for k, v in cs5_run.lay_pattern(node, spec).items() if k != "phases"}
        node.log.append(lay_line)
    names = names_of(node)
    gamma = node.gamma
    sign_k = [j for j, r in enumerate(node.rows_) if r.shape == POTENTIAL and r.wall is None][0]
    sign_first = sum(len(r.lines) for r in node.rows_[:sign_k])
    states, xs, spreads, charges, currents, exact, turns, sign = {0: state_of(node)}, {}, {}, {}, {}, {}, [], {}
    hashes = []
    t0 = time.monotonic_ns()
    for t in range(intervals):
        if back and t >= intervals - back:
            hashes.append(node.state_hash())
        node.step()
        i = node.interval
        states[i] = state_of(node)
        x = [int(v) for v in node.row(CARRIER).lines[0].now.reshape(-1)]
        xs[i] = sum(x) // len(x)
        spreads[i] = max(x) - min(x)
        exact[i] = min(x) == max(x) == gamma
        frames = readings.frames(node, node.walled().lines[0].rem)
        charges[i] = [at0(gram.charge(r.shape, r.lines)) for r in node.gapped]
        currents[i] = [[at0(j) for j in gram.current(r.shape, [line.now for line in r.lines], frames)] for r in node.gapped]
        sign[i] = [[at0(line.now), None if line.wr is None else at0(line.wr)] for line in node.rows_[sign_k].lines]
        if node.turned.any():
            turns.append((i, int(node.turned.sum())))
    forward_ms = (time.monotonic_ns() - t0) // 1000000
    count = int(node.cube) ** 3
    tops = [i for i, n in turns if n == count]
    ks = sorted(xs)
    bottoms = [(k, xs[k]) for k in ks[1:-1] if xs[k] <= xs[k - 1] and xs[k] < xs[k + 1]]
    exact_at = [k for k in ks if exact[k]]
    retrace = []
    for top in tops:
        first, same, per_line_first = None, 0, {}
        for k in range(1, top):
            if top + k > intervals:
                break
            mirror = exchanged(node, states[top - 1 - k])
            parted = [(nm, a, b) for nm, a, b in zip(names, states[top + k], mirror, strict=True) if not line_equal(a, b)]
            for nm, a, b in parted:
                if nm not in per_line_first:
                    per_line_first[nm] = {"k": k, **first_node_off(a, b)}
            if not parted:
                if first is None:
                    same += 1
                continue
            if first is None:
                first = {"k": k, "fall interval": top + k, "mirrored rise interval": top - 1 - k, "X fall": xs[top + k],
                         "X rise mirror": xs.get(top - 2 - k), "lines parted": len(parted),
                         "parted": [{"line": nm, **first_node_off(a, b)} for nm, a, b in parted[:8]]}
            if len(per_line_first) == len(names) or k > first["k"] + 40:
                break
        x_first = None
        for k in range(0, top - 2):
            if top + k > intervals:
                break
            if xs[top + k] != xs[top - 2 - k]:
                x_first = {"k": k, "X fall": xs[top + k], "X rise": xs[top - 2 - k]}
                break
        retrace.append({"top": top, "equal k before the parting": same, "first parting (state)": first,
                        "first parting per line (k, field, node, integers)": per_line_first, "first parting (X)": x_first})
    credits = [e for e in node.log if e["event"] == "credit"]
    back_exact = 0
    for k in range(len(hashes)):
        node.step_back()
        back_exact += node.state_hash() == hashes[len(hashes) - 1 - k]
    n_ints, bits = node.census()
    marks = [k for k in ks if k % 25 == 0 or k in (1, 2, 3)]
    out = {
        "world": world_path, "lay": lay_line, "engine": os.environ.get("PYTHONPATH", ""),
        "flags": {k: v for k, v in os.environ.items() if k.startswith(("OL1_", "CS7_", "CS4_"))},
        "intervals": intervals, "forward ms": forward_ms, "cube": node.cube, "gamma": gamma, "T": node.T,
        "uniform (spread 0) of intervals": [sum(1 for k in ks if spreads[k] == 0), len(ks)],
        "turns (interval, count)": turns, "tops": tops, "bottoms (interval, mean X)": bottoms,
        "exact at Gamma at every Node": exact_at, "X at marks": {str(k): xs[k] for k in marks},
        "credits": len(credits), "laid back": sum(1 for c in credits if "laid_back" in c),
        "credits in the first rise": sum(1 for c in credits if tops and c["i"] < tops[0]),
        "counts": {k: int(v) for k, v in node.counts.items()},
        "sign row at the origin at marks [now, wr] x 4": {str(k): sign[k] for k in marks},
        "W per gapped record at the origin at marks": {str(k): charges[k] for k in marks},
        "J per gapped record at the origin at marks": {str(k): currents[k] for k in marks},
        "J summed over the records, nonzero intervals": sum(1 for k in ks if k > 0 and any(sum(c[a] for c in currents[k]) != 0 for a in range(3))),
        "J max abs summed over the records": max(abs(sum(c[a] for c in currents[k])) for k in ks if k > 0 for a in range(3)) if node.gapped else 0,
        "odd lines nonzero intervals": sum(1 for k in ks if k > 0 and any(sign[k][1 + a][0] != 0 for a in range(3))),
        "odd lines max abs": max(abs(sign[k][1 + a][0]) for k in ks if k > 0 for a in range(3)),
        "retrace": retrace, "run back": {"intervals": len(hashes), "exact": back_exact}, "integers": n_ints, "bits": bits,
        "final state hash": node.state_hash(),
    }
    json.dump(out, open(out_path, "w"), indent=1, default=str)
    print(json.dumps({k: out[k] for k in ("world", "flags", "lay", "tops", "bottoms (interval, mean X)", "exact at Gamma at every Node", "credits", "laid back", "counts", "J summed over the records, nonzero intervals", "J max abs summed over the records", "odd lines nonzero intervals", "odd lines max abs", "run back", "integers", "bits", "forward ms")}, default=str))
    for r in retrace:
        print(json.dumps({"top": r["top"], "equal k": r["equal k before the parting"], "state parting": None if r["first parting (state)"] is None else {k: v for k, v in r["first parting (state)"].items() if k != "parted"}, "parted lines": None if r["first parting (state)"] is None else r["first parting (state)"]["parted"], "X parting": r["first parting (X)"]}, default=str))


if __name__ == "__main__":
    main(sys.argv)
