"""The readers' proof (H-Readings-One-Reader-1): a world run in-process through event_universe.run (back 20) with every reading function of the engine rebound to a wrapper that computes the reader's value at the same arguments and counts the calls and the ones apart; every Link record metric.fold_links returns compared with link_reader.read_link at the interval's captured arguments; the dead readings (gram.term with no axis matrix) and the twice-read phases counted. Integers only. Usage: proof_readers.py <world.json> <out.json>."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import link_reader as lr  # noqa: E402
import row_reader as rr  # noqa: E402
from event_universe import gram, links, metric, readings, run  # noqa: E402
from event_universe.core.ports import AXES, PORTS  # noqa: E402
from event_universe.core.ports import PORT_SIDES  # noqa: E402
from event_universe.links import Link  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.rows import CARRIER  # noqa: E402

sys.set_int_max_str_digits(0)
COUNTS: dict[str, list[int]] = {}
CAPTURED: dict[str, object] = {}


def same(a, b) -> bool:
    if isinstance(a, Link):
        return isinstance(b, Link) and all(same(getattr(a, s), getattr(b, s)) for s in Link.__slots__)
    if isinstance(a, (list, tuple)):
        return isinstance(b, (list, tuple)) and len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    if a is None or b is None:
        return a is b
    x, y = np.asarray(a, dtype=object), np.asarray(b, dtype=object)
    return x.shape == y.shape and bool(np.all(x == y))


def tally(name: str, apart: bool, extra: str | None = None) -> None:
    c = COUNTS.setdefault(name, [0, 0])
    c[0] += 1
    c[1] += int(apart)
    if extra:
        COUNTS.setdefault(extra, [0, 0])[0] += 1


def kind_of(shape: int, m) -> str | None:
    for kind in ("G", "GJ", "K", "GA0", "GA1", "GA2"):
        try:
            if rr.matrix(shape, kind) == m:
                return kind
        except IndexError:
            pass
    return None


def rebind(mod, fname, reader):
    orig = getattr(mod, fname)
    key = f"{mod.__name__.split('.')[-1]}.{fname}"

    def wrapped(*args, **kwargs):
        found = orig(*args, **kwargs)
        try:
            mine = reader(found, *args, **kwargs)
            apart = mine is not NotImplemented and not same(found, mine)
        except Exception as e:  # noqa: BLE001
            apart, mine = True, repr(e)
            COUNTS.setdefault(key + " ERROR " + repr(e)[:80], [0, 0])[0] += 1
        tally(key, apart)
        return found

    for name, m in list(sys.modules.items()):
        if name.startswith("event_universe"):
            for attr, val in list(vars(m).items()):
                if val is orig:
                    setattr(m, attr, wrapped)
    return wrapped


def levels_of(node, axis_levels):
    return [line.now for line in node.row(CARRIER).lines[1 : 1 + AXES]] if axis_levels is None else axis_levels


def install():
    # the Link's record
    rebind(links, "link", lambda found, port, even=(), odd=(), frame_bits=None: (
        [lr.even(a, port) for a in even], [lr.odd_sum(a, port) for a in odd],
        None if frame_bits is None else lr.frame(frame_bits, port)))
    rebind(links, "link_current", lambda found, line, port: lr.current(line.now, line.before, port))
    rebind(links, "net_current", lambda found, line, axis: lr.net_current(line.now, line.before, axis))
    rebind(links, "row_twist", lambda found, lines, axis: lr.twist([(l.now, l.before) for l in lines], axis))
    rebind(links, "row_current", lambda found, lines, port: sum((lr.current(l.now, l.before, port) for l in lines), start=0))
    rebind(links, "gradient", lambda found, a, axis: lr.gradient(a, axis))
    rebind(links, "wronskian", lambda found, re, im: rr.charge(2, [re.before, im.before], [re.now, im.now]))
    rebind(links, "cross", lambda found, *a: lr.cross(*a))
    rebind(links, "turn_pair", lambda found, *a: lr.turn_pair(*a))
    rebind(links, "turned", lambda found, xs, at, scale, gamma: lr.turned(xs, at, scale, gamma))
    def links_of_reader(found, factors, frames, phases, odd_lines):
        CAPTURED.setdefault("links_order", []).append(id(found))
        CAPTURED.setdefault("links_kept", []).append(found)
        return [Link(factors[p], frames[p], phases[p][0], phases[p][1], lr.odd_sum(odd_lines[a], p)) for p, (a, _s) in enumerate(PORT_SIDES)]

    rebind(links, "links_of", links_of_reader)

    def factors_reader(found, node, axis_levels=None, frozen=None):
        CAPTURED["levels"], CAPTURED["frozen"] = levels_of(node, axis_levels), frozen
        return tuple(lr.factor(node.gamma, node.G, levels_of(node, axis_levels)[a], p, frozen) for p, (a, _s) in enumerate(PORT_SIDES))

    rebind(readings, "link_factors", factors_reader)

    def frames_reader(found, node, phi_rem):
        CAPTURED["bits"] = phi_rem
        return [lr.frame(phi_rem, p) for p in range(PORTS)]

    rebind(readings, "frames", frames_reader)

    def phases_reader(found, node, frames, count):
        last = CAPTURED.get("phase_args")
        if last is not None and same(last, (frames, count)):
            tally("readings.link_phases SPELLED TWICE (same args as the last call)", False)
        CAPTURED["phase_args"] = (frames, count)
        return [lr.phase(node, count, frames[p], p) for p in range(PORTS)]

    rebind(readings, "link_phases", phases_reader)

    def count_reader(found, node, cphi, phi):
        CAPTURED["count"] = found
        CAPTURED["links_order"], CAPTURED["links_kept"] = [], []
        return NotImplemented

    rebind(readings, "centred_count", count_reader)

    def rotation_reader(found, node, pair):
        CAPTURED["node"] = node
        return NotImplemented

    rebind(metric, "rotation_of", rotation_reader)

    def fold_reader(found, links_, rotation, flux_lines, gamma):
        node = CAPTURED["node"]
        for p, (a, _s) in enumerate(PORT_SIDES):
            at = links_[p]
            coupling = CAPTURED["links_order"].index(id(links_))
            mine = lr.read_link(node, p, CAPTURED["levels"][a], CAPTURED["frozen"], CAPTURED["bits"], CAPTURED["count"],
                                CAPTURED["odd"][a], flux_lines[a], rotation, coupling)
            tally("ONE READER read_link vs the engine's Link record (per Link per record row per interval)", not same(found[p], mine))
        return [Link(at.factor, at.frame, at.cosine, at.sine, at.odd, lr.fold(flux_lines[a], rotation, gamma, p)) for p, (a, _s) in enumerate(PORT_SIDES) for at in (links_[p],)]

    rebind(metric, "fold_links", fold_reader)
    rebind(metric, "net_flux", lambda found, g, nows, velocities, axis: rr.flux(len(nows), nows, velocities, axis) if kind_of(len(nows), g) == "G" else NotImplemented)
    rebind(metric, "stress_parts", lambda found, rows, shape: [sum((num * rr.stress(len(levels), levels, a, a) for levels, num, g in rows), start=0) + np.zeros(shape, dtype=object) for a in range(AXES)])
    rebind(metric, "shear_parts", lambda found, rows, shape: [sum((num * rr.stress(len(levels), levels, a, (a + 1) % AXES) for levels, num, g in rows), start=0) + np.zeros(shape, dtype=object) for a in range(AXES)])
    # the row's gram
    rebind(gram, "charge", lambda found, shape, lines: rr.charge(shape, [l.before for l in lines], [l.now for l in lines]))
    rebind(gram, "current", lambda found, shape, nows, frames: rr.current(shape, nows, frames))
    rebind(gram, "density", lambda found, shape, nows: rr.density(shape, nows))
    rebind(gram, "conjugated", lambda found, shape, xs, frame: rr.conjugated(shape, xs, frame))

    def curl_reader(found, odd):
        CAPTURED["odd"] = odd
        return rr.curl(odd)

    rebind(gram, "curl", curl_reader)

    def term_reader(found, shape, coefficient, phi, xs):
        if not gram.axes(shape):
            tally("gram.term DEAD (no axis matrix: the curl read by nothing)", False)
        return rr.term(shape, coefficient, phi, xs)

    rebind(gram, "term", term_reader)

    def form_reader(found, m, xs, ys):
        kind = kind_of(len(xs), m)
        if kind is None:
            tally("gram.form at a matrix of no name", False)
            return NotImplemented
        tally(f"gram.form as the bilinear {kind}", False)
        return rr.form(len(xs), kind, xs, ys)

    rebind(gram, "form", form_reader)

    def weighted_reader(found, m, xs, ys):
        kind = kind_of(len(xs), m)
        if kind is None:
            return NotImplemented
        tally(f"gram.weighted as the bilinear {kind}", False)
        return rr.lines(len(xs), kind, xs, ys)

    rebind(gram, "weighted", weighted_reader)
    rebind(gram, "share", lambda found, node, lines, r: NotImplemented)
    rebind(gram, "period", lambda found, node, lines, standing: NotImplemented)


def main(world_path: str, out_path: str) -> None:
    install()
    universe, world = load_world(world_path)
    found = run.record(universe, world, 20, lambda s: None)
    summary = {
        "world": world_path,
        "intervals": found["intervals"],
        "run_back": found["run_back"],
        "log": len(found["log"]),
        "counts": {k: {"calls": v[0], "apart": v[1]} for k, v in sorted(COUNTS.items())},
        "calls": sum(v[0] for k, v in COUNTS.items() if " as the " not in k and "DEAD" not in k and "TWICE" not in k),
        "apart": sum(v[1] for v in COUNTS.values()),
    }
    Path(out_path).write_text(json.dumps(summary, indent=1))
    for k, v in sorted(COUNTS.items()):
        print(f"{k}: {v[0]} calls, {v[1]} apart")
    print("run back", found["run_back"], "log", len(found["log"]), "calls", summary["calls"], "apart", summary["apart"])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
