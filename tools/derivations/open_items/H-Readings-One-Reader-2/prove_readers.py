"""The readers' proof: every call of the engine's reading functions on a world's run (forward and back) compared with the two readers' values at the same arguments, by wrappers set in every engine module that holds the name (the engine imported through run.py). Usage: python prove_readers.py <world.json> <out.json> [back N]. Prints per reading the calls and the calls apart; exit 0 only at 0 apart."""

from __future__ import annotations

import json
import os
import sys
from typing import Any

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import link_reader as lr  # noqa: E402
import row_reader as rr  # noqa: E402
from event_universe import run as engine_run  # noqa: E402
from event_universe.core.ports import PORT_SIDES, PORTS  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.rows import CARRIER, PLANE  # noqa: E402

COUNTS: dict[str, list[int]] = {}


def same(a: Any, b: Any) -> bool:
    """Two readings equal bit for bit: arrays by shape and every value, lists and tuples element by element, else by ==."""
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b, strict=True))
    if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
        a, b = np.asarray(a), np.asarray(b)
        return a.shape == b.shape and bool(np.all(a == b))
    return bool(a == b)


def tally(name: str, equal: bool) -> None:
    calls = COUNTS.setdefault(name, [0, 0])
    calls[0] += 1
    calls[1] += 0 if equal else 1


def patch(name: str, original: Any, wrapper: Any) -> None:
    """The wrapper set in every engine module whose attribute `name` is the original (the names bound at import)."""
    for mod_name, mod in list(sys.modules.items()):
        if mod_name.startswith("event_universe") and getattr(mod, name, None) is original:
            setattr(mod, name, wrapper)


def main(argv: list[str]) -> int:
    sys.set_int_max_str_digits(0)
    world_path, out_path = argv[1], argv[2]
    back = int(argv[argv.index("back") + 1]) if "back" in argv else 0
    links = sys.modules["event_universe.links"]
    readings = sys.modules["event_universe.readings"]
    metric = sys.modules["event_universe.metric"]
    gram = sys.modules["event_universe.gram"]

    o_link, o_link_current, o_row_current = links.link, links.link_current, links.row_current
    o_net_current, o_row_twist, o_gradient, o_turned = links.net_current, links.row_twist, links.gradient, links.turned
    o_links_of = links.links_of
    o_link_factors, o_frames, o_link_phases = readings.link_factors, readings.frames, readings.link_phases
    o_fold_links = metric.fold_links
    o_charge, o_current, o_density, o_curl = gram.charge, gram.current, gram.density, gram.curl
    o_term, o_conjugated, o_share, o_form, o_weighted = gram.term, gram.conjugated, gram.share, gram.form, gram.weighted

    def w_link(port: int, even: tuple[Any, ...] = (), odd: tuple[Any, ...] = (), frame_bits: Any = None) -> Any:
        got = o_link(port, even, odd, frame_bits)
        mine = (
            [lr.even(a, port) for a in even],
            [lr.odd_part(a, port) for a in odd],
            None if frame_bits is None else lr.frame(frame_bits, port),
        )
        tally("links.link", same(got, mine))
        return got

    def w_link_current(line: Any, port: int) -> Any:
        got = o_link_current(line, port)
        tally("links.link_current", same(got, lr.current(line.now, line.before, port)))
        return got

    def w_row_current(lines: list[Any], port: int) -> Any:
        got = o_row_current(lines, port)
        mine = sum((lr.current(line.now, line.before, port) for line in lines), start=0)
        tally("links.row_current", same(got, mine))
        return got

    def w_net_current(line: Any, axis: int) -> Any:
        got = o_net_current(line, axis)
        tally("links.net_current", same(got, lr.net_current(line.now, line.before, axis)))
        return got

    def w_row_twist(lines: list[Any], axis: int) -> Any:
        got = o_row_twist(lines, axis)
        mine = lr.twist([line.now for line in lines], [line.before for line in lines], axis)
        tally("links.row_twist", same(got, mine))
        return got

    def w_gradient(a: Any, axis: int) -> Any:
        got = o_gradient(a, axis)
        tally("links.gradient", same(got, lr.gradient(a, axis)))
        return got

    def w_turned(xs: list[Any], at: Any, scale: Any, gamma: Any) -> Any:
        got = o_turned(xs, at, scale, gamma)
        tally("links.turned", same(got, lr.turn(xs, at, scale, gamma, PLANE)))
        return got

    def w_link_factors(node: Any, axis_levels: Any = None, frozen: Any = None) -> Any:
        got = o_link_factors(node, axis_levels, frozen)
        levels = [line.now for line in node.row(CARRIER).lines[1:4]] if axis_levels is None else axis_levels
        mine = tuple(lr.factor(node.gamma, node.G, levels, port, frozen) for port in range(PORTS))
        tally("readings.link_factors", same(got, mine))
        return got

    def w_frames(node: Any, phi_rem: Any) -> Any:
        got = o_frames(node, phi_rem)
        tally("readings.frames", same(got, [lr.frame(phi_rem, port) for port in range(PORTS)]))
        return got

    def w_link_phases(node: Any, frames: list[Any], count: Any) -> Any:
        got = o_link_phases(node, frames, count)
        mine = [lr.phases(node, count, frames[port], port) for port in range(PORTS)]
        tally("readings.link_phases", same(got, mine))
        return got

    def w_fold_links(found: list[Any], rotation: int, flux_lines: list[Any], gamma: int) -> Any:
        got = o_fold_links(found, rotation, flux_lines, gamma)
        mine = [lr.fold(flux_lines[axis], rotation, gamma, port) for port, (axis, _s) in enumerate(PORT_SIDES)]
        tally("metric.fold_links", same([g.fold for g in got], mine))
        return got

    def w_charge(shape: int, lines: list[Any]) -> Any:
        got = o_charge(shape, lines)
        tally("gram.charge", same(got, rr.charge(shape, [x.before for x in lines], [x.now for x in lines])))
        return got

    def w_current(shape: int, nows: list[Any], frames: list[Any]) -> Any:
        got = o_current(shape, nows, frames)
        tally("gram.current", same(got, rr.current(shape, nows, frames)))
        return got

    def w_density(shape: int, nows: list[Any]) -> Any:
        got = o_density(shape, nows)
        tally("gram.density", same(got, rr.density(shape, nows)))
        return got

    def w_curl(odd: list[Any]) -> Any:
        got = o_curl(odd)
        tally("gram.curl", same(got, rr.curl(odd)))
        return got

    def w_term(shape: int, coefficient: Any, phi: list[Any], xs: list[Any]) -> Any:
        got = o_term(shape, coefficient, phi, xs)
        tally("gram.term", same(got, rr.term(shape, coefficient, phi, xs)))
        return got

    def w_conjugated(shape: int, xs: list[Any], frame: Any) -> Any:
        got = o_conjugated(shape, xs, frame)
        tally("gram.conjugated", same(got, rr.conjugated(shape, xs, frame)))
        return got

    def w_share(node: Any, lines: list[Any], r: Any) -> Any:
        got = o_share(node, lines, r)
        tally("gram.share", same(got, rr.share(node, [x.now for x in lines], [x.before for x in lines], r)))
        return got

    def w_form(m: Any, xs: list[Any], ys: list[Any]) -> Any:
        got = o_form(m, xs, ys)
        tally("gram.form", same(got, rr.bilinear(m, xs, ys)))
        return got

    def w_weighted(m: Any, xs: list[Any], ys: list[Any]) -> Any:
        got = o_weighted(m, xs, ys)
        tally("gram.weighted", same(got, rr.lines(m, xs, ys)))
        return got

    for name, original, wrapper in (
        ("link", o_link, w_link),
        ("link_current", o_link_current, w_link_current),
        ("row_current", o_row_current, w_row_current),
        ("net_current", o_net_current, w_net_current),
        ("row_twist", o_row_twist, w_row_twist),
        ("gradient", o_gradient, w_gradient),
        ("turned", o_turned, w_turned),
        ("link_factors", o_link_factors, w_link_factors),
        ("frames", o_frames, w_frames),
        ("link_phases", o_link_phases, w_link_phases),
        ("fold_links", o_fold_links, w_fold_links),
        ("charge", o_charge, w_charge),
        ("current", o_current, w_current),
        ("density", o_density, w_density),
        ("curl", o_curl, w_curl),
        ("term", o_term, w_term),
        ("conjugated", o_conjugated, w_conjugated),
        ("share", o_share, w_share),
        ("form", o_form, w_form),
        ("weighted", o_weighted, w_weighted),
    ):
        patch(name, original, wrapper)

    # the Link's record as one function: links_of then fold_links against lr.record, per coupling
    interval = sys.modules["event_universe.interval"]
    o_interval_readings = interval.Interval.readings

    def w_readings(self: Any) -> None:
        o_interval_readings(self)
        node = self.node
        for c, found in self.links_at.items():
            mine = lr.record(node, self.factors, self.frames, 0 * self.c, self.odd, c)
            equal = all(
                same(g.factor, m.factor) and same(g.frame, m.frame) and same(g.odd, m.odd)
                for g, m in zip(found, mine, strict=True)
            )
            tally("links.links_of (factor, frame, odd)", equal)

    interval.Interval.readings = w_readings

    universe, world = load_world(world_path)
    out: list[str] = []
    record = engine_run.record(universe, world, back, out.append)
    summary = {
        "world": world_path,
        "intervals": record["intervals"],
        "run_back": record["run_back"],
        "counts": record["counts"],
        "readings": {k: {"calls": v[0], "apart": v[1]} for k, v in sorted(COUNTS.items())},
        "calls": sum(v[0] for v in COUNTS.values()),
        "apart": sum(v[1] for v in COUNTS.values()),
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=1)
    for k, v in sorted(COUNTS.items()):
        print(f"{k}: {v[0]} calls, {v[1]} apart")
    print(f"total: {summary['calls']} calls, {summary['apart']} apart; run back {record['run_back']}")
    return 0 if summary["apart"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
