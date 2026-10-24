"""The reader of the clicks log alone, a host tool that computes nothing from a Node's level (ALGEBRA.md, The click writes on the lattice; The click's read of the board; No click names a Node; The uncertainty relation is the detector's three declarations; The uncertainty principle is the record's and the click's; The board is deterministic, but it cannot be read through clicks, because of the uncertainty principle; The click's unit: the whole of a click is the detector's own transition; What a click reads of a quantum; The lattice momentum; The paces compose; The horizon; the builder's rule of method of 2026-10-24, #2187 comment 6382837913: the clicks log is the record, the eras and nodes lines are looks). From the credit, birth and lay lines of `<world>.clicks.jsonl` and nothing else it reads what the credits say of the bodies: the mass (`point`, the reduced pair [num, den] the click read, T sin omega in T's unit), the position (`support`, the shell Node of a body's click, or the board's own click's Node by its x-major index `node_detector`, and the window's close), the velocity (two credits of one `identity`, the Links between them on the torus over the intervals between their closes, and over the taker's own `proper` intervals), the momentum (`momentum`, `fan`, `recoil`), the energy (`count` whole quanta, each T sin omega of the point), bound or free (the credits of one identity at one Node, the `beat` between their closes), and beside the bodies the uncertainty table per family and window (the count's floor, the where's spread on the torus, the momentum's spread and their product in the click's units) and the GR table (the dilation of a taker's `proper` against the board's intervals, light's click spacing per Node, the Nodes silent while others click, a free body's track against the straight line). Every cell the log cannot fill names the key it lacks.

Usage: `PYTHONPATH=src python tools/clicks_read.py <world>.clicks.jsonl [--shape X Y Z] [--action T] [--out <file>.json]`
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, NamedTuple

Line = dict[str, Any]
Node = tuple[int, int, int]
Shape = tuple[int, int, int]
Identity = tuple[int, int] | str
AXES = (0, 1, 2)
ONE_WINDOW = "one window: nothing to compare"
TWO_CLOCKS = "the two credits' proper are two Nodes' clocks: no one taker's own interval"
NO_ONE_BODY = "a record credited at several Nodes in one close: the credited record and no one body"


class Lines(NamedTuple):
    """The log's lines by kind, each list in file order: the credits, the births, the lays and the rest."""

    credits: list[Line]
    births: list[Line]
    lays: list[Line]
    others: list[Line]


def lacking(*keys: str) -> str:
    """The cell of a reading the log cannot give, naming the keys it lacks."""
    return "unreadable: " + ", ".join(keys) + " lacking"


def read_log(path: Path) -> Lines:
    """The clicks log read whole, one JSON object per line, split by `event`; no eras or nodes line is read."""
    found = Lines([], [], [], [])
    kinds: dict[str, list[Line]] = {"credit": found.credits, "birth": found.births, "lay": found.lays}
    for text in path.read_text(encoding="utf-8").splitlines():
        if text.strip():
            line = json.loads(text)
            kinds.get(str(line.get("event")), found.others).append(line)
    return found


def as_node(value: Any) -> Node:
    """A Node at the file's coordinates from a line's list."""
    return (int(value[0]), int(value[1]), int(value[2]))


def named_nodes(lines: Lines) -> list[Node]:
    """Every Node a line names: the lays' `node.at`, the births' `nodes`, the credits' `support`."""
    found: list[Node] = []
    for lay in lines.lays:
        node = lay.get("node")
        if isinstance(node, dict) and node.get("at") is not None:
            found.append(as_node(node["at"]))
    for birth in lines.births:
        found.extend(as_node(node) for node in birth.get("nodes") or [])
    found.extend(as_node(c["support"]) for c in lines.credits if c.get("support") is not None)
    return found


def shape_of(lines: Lines, declared: Shape | None = None) -> Shape | None:
    """The torus's extent per axis: as declared, else max + 1 over every Node the lines name; None where no line names a Node."""
    if declared is not None:
        return declared
    nodes = named_nodes(lines)
    if not nodes:
        return None
    return (
        max(n[0] for n in nodes) + 1,
        max(n[1] for n in nodes) + 1,
        max(n[2] for n in nodes) + 1,
    )


def where_of(credit: Line, shape: Shape | None, births: list[Line]) -> Node | str | None:
    """The where of a credit: `support`, the shell Node of a body's click; else the board's own click's Node, its x-major index `node_detector` unravelled over `shape` and checked against the birth lines of the same interval; else the taker's name, a region with no Node; None where nothing names it."""
    if credit.get("support") is not None:
        return as_node(credit["support"])
    taker = credit.get("node_detector")
    if isinstance(taker, str):
        return taker
    if isinstance(taker, bool) or not isinstance(taker, int):
        return None
    born = [
        as_node(node)
        for birth in births
        if birth.get("interval") == credit.get("interval")
        for node in birth.get("nodes") or []
    ]
    if shape is None:
        return born[0] if len(born) == 1 else None
    x, rest = divmod(taker, shape[1] * shape[2])
    y, z = divmod(rest, shape[2])
    found = (x, y, z)
    if born and found not in born:
        raise ValueError(
            f"the credit {taker} at the interval {credit.get('interval')} unravels to {list(found)} over "
            f"the shape {list(shape)}, a Node no birth line of that interval names"
        )
    return found


def birth_beside(credit: Line, shape: Shape | None, births: list[Line]) -> Line | None:
    """The birth line beside a credit: the birth of the same interval at the credit's where, else the one birth of that interval, else None."""
    where = where_of(credit, shape, births)
    beside = [b for b in births if b.get("interval") == credit.get("interval")]
    at_where = [b for b in beside if where in [as_node(n) for n in b.get("nodes") or []]]
    if at_where:
        return at_where[0]
    return beside[0] if len(beside) == 1 else None


def identity_of(credit: Line) -> Identity | None:
    """The taker's identity across windows: `identity`, [family index, record index]; else `node_detector` where it names a body (`body n`); None for the board's own click, whose index names a place and no body."""
    identity = credit.get("identity")
    if identity is not None:
        return (int(identity[0]), int(identity[1]))
    taker = credit.get("node_detector")
    return taker if isinstance(taker, str) and taker.startswith("body") else None


def leg_below(square: int) -> int:
    """The largest integer x with x * x <= square, by a bisection on comparisons of integers alone (the law's one search, core/rule3.largest_below, written here so that the reader imports nothing of the engine): the leg of a Pythagorean point exactly, no root."""
    if square < 0:
        raise ValueError(f"no integer has a square at most {square}: the search is refused")
    high = 1
    while high * high <= square:
        high = high + high
    low = 0
    while high - low > 1:
        middle = (low + high) // 2
        if middle * middle <= square:
            low = middle
        else:
            high = middle
    return low


def pair_of(point: Any) -> tuple[int, int] | None:
    """A point's reduced pair [num, den] as two integers; None where the key holds none, or a list of pairs (the record's lines reading different points at the credited Node)."""
    if point is None or len(point) != 2 or not all(isinstance(v, int) for v in point):
        return None
    return (int(point[0]), int(point[1]))


def sine_of(pair: tuple[int, int]) -> float:
    """sin omega of a point's reduced pair (num, den), cos omega = num / den: the leg over den, the leg the largest integer whose square is at most den^2 - num^2 (exact at a Pythagorean point): T sin omega in T's unit, the mass of a point at rest and the frequency of a massless record."""
    num, den = pair
    return leg_below(den * den - num * num) / den


def action_of(credit: Line) -> int | None:
    """T from the click's own keys where no --action is given: the `beat` is 3 T sin omega of the `point`, so T = beat x den div (3 x leg), exact where den divides 3 T leg; None where the point or the beat is lacking or the point has no leg (a massless record at its rest)."""
    pair, beat = pair_of(credit.get("point")), credit.get("beat")
    if pair is None or beat is None or abs(pair[0]) > pair[1]:
        return None
    leg = leg_below(pair[1] * pair[1] - pair[0] * pair[0])
    return int(beat) * pair[1] // (3 * leg) if leg else None


def mass_of(credit: Line, birth: Line | None = None) -> dict[str, Any]:
    """The mass: `point`, the reduced pair the click read from the three levels, as T sin omega in T's unit (a point at rest; for the credited massless record the quantum's frequency), with the `beat` (3 T sin omega, the click's own unit), the `kind` (1 or 2, the record's width) and the `sense` (-1, 0, 1, the Wronskian's sign); the family's label (`realised`, `emitted` or the birth's `children`) names the family and no number; the birth's `points` and `records` are the children's."""
    point = credit.get("point")
    pair = pair_of(point)
    children = (birth or {}).get("children") or []
    label = credit.get("realised") or credit.get("emitted") or (children[0] if children else None)
    found: dict[str, Any] = {"label": label if label is not None else lacking("realised", "emitted")}
    if pair is None:
        found["point"] = (
            lacking("point") if point is None else f"the lines read different points: {point}"
        )
        found["mass"] = found["point"]
    elif abs(pair[0]) > pair[1]:
        found["point"] = list(pair)
        found["mass"] = f"the point {list(pair)} lies outside the circle: no rotation"
    else:
        found["point"] = list(pair)
        found["mass"] = sine_of(pair)
    for key in ("beat", "kind", "sense"):
        found[key] = credit[key] if credit.get(key) is not None else lacking(key)
    if birth is not None and birth.get("senses") is not None:
        found["senses_born"] = birth["senses"]
    if birth is not None and birth.get("points") is not None:
        found["children_points"] = birth["points"]
        found["children_records"] = birth.get("records")
    return found


def position_of(
    credit: Line, shape: Shape | None, births: list[Line], clock_written: bool = True
) -> dict[str, Any]:
    """The position: the where (`where_of`), the when (the window's close in the board's intervals), the taker's own time `proper` and its event clock `windows`; `proper` is marked a constant where no credit of the log has a clock written."""
    where = where_of(credit, shape, births)
    window = credit.get("window")
    found: dict[str, Any] = {
        "where": list(where)
        if isinstance(where, tuple)
        else (where if where is not None else lacking("support", "node_detector")),
        "when": window[1] if window else lacking("window"),
        "window": window if window else lacking("window"),
    }
    proper = credit.get("proper")
    if proper is None:
        found["proper"] = lacking("proper")
    else:
        found["proper"] = proper if clock_written else f"constant {proper}: no clock written on this log"
    found["windows"] = credit["windows"] if credit.get("windows") is not None else lacking("windows")
    return found


def shortest(difference: int, extent: int) -> int:
    """The shortest signed count of Links between two coordinates on a ring of `extent` Nodes."""
    half = extent // 2
    return (difference + half) % extent - half


def wrapped(difference: float, extent: int) -> float:
    """The same for a real difference, in (-extent / 2, extent / 2]."""
    half = extent / 2
    return (difference + half) % extent - half


def velocity_of(first: Line, last: Line, shape: Shape | None) -> dict[str, Any] | None:
    """The velocity between two credits of one identity: the Links between their wheres on the torus over the intervals between their closes, and over the taker's own proper intervals; None where the two share no identity, no Node or no elapsed interval."""
    identity = identity_of(first)
    if identity is None or identity != identity_of(last) or shape is None:
        return None
    a, b = where_of(first, shape, []), where_of(last, shape, [])
    if not (isinstance(a, tuple) and isinstance(b, tuple)):
        return None
    intervals = int(last["window"][1]) - int(first["window"][1])
    if intervals == 0:
        return None
    links = [shortest(b[axis] - a[axis], shape[axis]) for axis in AXES]
    found: dict[str, Any] = {
        "links": links,
        "intervals": intervals,
        "per_interval": [d / intervals for d in links],
    }
    proper = (first.get("proper"), last.get("proper"))
    if proper[0] is None or proper[1] is None:
        found["per_proper_interval"] = lacking("proper")
    elif a != b:
        found["per_proper_interval"] = TWO_CLOCKS
    elif proper[1] == proper[0]:
        found["per_proper_interval"] = "no proper interval elapsed between the two closes"
    else:
        elapsed = int(proper[1]) - int(proper[0])
        found["proper_intervals"] = elapsed
        found["per_proper_interval"] = [d / elapsed for d in links]
    return found


def momentum_of(credit: Line) -> dict[str, Any]:
    """The four-flux kept: `momentum` (p_a per axis in T's unit per Link), `fan` (the record's P_a over the board) and `recoil` (-p_a owed by the source), each named lacking where the log has none."""
    return {
        key: credit[key] if credit.get(key) is not None else lacking(key)
        for key in ("momentum", "fan", "recoil")
    }


def energy_of(credit: Line, point: Any = None, action: int | None = None) -> dict[str, Any]:
    """The energy: `count` whole quanta; at rest the count times T sin omega of the point, in T's unit; with the momentum the band's form, cos omega(k) = cos omega_0 - (1 / 3) SUM_a (1 - cos k_a) with sin k_a = p_a / T, T given (`--action`) or read from the beat and the point (`action_of`)."""
    count = credit.get("count")
    pair = pair_of(credit.get("point") if point is None else point)
    found: dict[str, Any] = {"quanta": count if count is not None else lacking("count")}
    if count is None or pair is None or abs(pair[0]) > pair[1]:
        found["rest"] = lacking("count") if count is None else lacking("point")
        found["with_momentum"] = found["rest"]
        return found
    found["rest"] = count * sine_of(pair)
    momentum = credit.get("momentum")
    action = action_of(credit) if action is None else action
    if momentum is None:
        found["with_momentum"] = lacking("momentum")
    elif action is None:
        found["with_momentum"] = "the band's form needs T: pass --action"
    elif any(abs(int(p)) > action for p in momentum):
        found["with_momentum"] = "a momentum above T: no band reading"
    else:
        legs = [leg_below(action * action - int(p) * int(p)) for p in momentum]  # T cos k_a per axis
        num, den = pair
        scale = 3 * den * action  # cos omega(k) = (3 num T - den SUM_a (T - T cos k_a)) / (3 den T)
        cosine = 3 * num * action - den * sum(action - leg for leg in legs)
        found["with_momentum"] = count * leg_below(scale * scale - cosine * cosine) / scale
        found["action"] = action
    return found


def tracks_of(lines: Lines) -> dict[str, list[Line]]:
    """The credits per identity (its JSON as the key), in the order of their closes; a credit with no identity is in no track."""
    found: dict[str, list[Line]] = defaultdict(list)
    for credit in lines.credits:
        identity = identity_of(credit)
        if identity is not None:
            found[json.dumps(identity)].append(credit)
    return {key: sorted(track, key=lambda c: int(c["window"][1])) for key, track in found.items()}


def bound_or_free(track: list[Line], shape: Shape | None, births: list[Line]) -> dict[str, Any]:
    """Bound or free: a track of one credit is unreadable; successive credits at one Node are a body bound there, its beats the spans between its closes (the `beat` key beside them); wheres that move are a free body with its speed."""
    if len(track) < 2:
        why = "one credit" + ("" if identity_of(track[0]) is not None else ", " + lacking("identity"))
        return {
            "verdict": f"unreadable: {why}",
            "support": None,
            "beats": [],
            "beat": track[0].get("beat"),
        }
    wheres = [where_of(c, shape, births) for c in track]
    closes = [int(c["window"][1]) for c in track]
    beats = [b - a for a, b in zip(closes, closes[1:], strict=False)]
    found: dict[str, Any] = {"beats": beats, "beat": [c.get("beat") for c in track]}
    if isinstance(wheres[0], tuple) and all(w == wheres[0] for w in wheres):
        found.update(verdict=f"bound at {list(wheres[0])}", support=list(wheres[0]))
        return found
    if len(set(closes)) < len(closes):
        found.update(verdict=NO_ONE_BODY, support=None, closes=sorted(set(closes)))
        found["distinct_wheres"] = len({w for w in wheres if isinstance(w, tuple)})
        return found
    velocity = velocity_of(track[0], track[-1], shape)
    moving = f", v = {json.dumps(velocity['per_interval'])} Links per interval" if velocity else ""
    found.update(verdict="free" + moving, support=None)
    found["wheres"] = [list(w) if isinstance(w, tuple) else w for w in wheres]
    return found


def partners(rows: list[dict[str, Any]]) -> None:
    """Two or more bodies bound at one Node: each row's `bound_with` names the others and says whether their summed count per close is one constant (what one gives the other takes)."""
    by_support: dict[Node, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        support = row["bound_or_free"].get("support")
        if support is not None:
            by_support[as_node(support)].append(row)
    for group in by_support.values():
        if len(group) < 2:
            continue
        closes = [sorted(row["counts"]) for row in group]
        same = all(c == closes[0] for c in closes)
        sums = {close: sum(row["counts"][close] for row in group) for close in closes[0]} if same else {}
        for row in group:
            row["bound_with"] = {
                "identities": [other["identity"] for other in group if other is not row],
                "counts_conserved": same and len(set(sums.values())) == 1,
            }


def bodies_table(
    lines: Lines, shape: Shape | None = None, action: int | None = None
) -> list[dict[str, Any]]:
    """One row per identity (per credit where the log has no identity): mass, position, velocity, momentum, energy, bound or free; every cell the log cannot fill names its key."""
    shape = shape_of(lines, shape)
    clock_written = any(c.get("proper") not in (None, 0) for c in lines.credits)
    rows: list[dict[str, Any]] = []
    for key, track in tracks_of(lines).items():
        last = track[-1]
        closes = [int(c["window"][1]) for c in track]
        velocity: Any = velocity_of(track[0], last, shape) if len(track) > 1 else None
        if len(set(closes)) < len(closes):
            velocity = NO_ONE_BODY
        elif velocity is None:
            velocity = "unreadable: one credit" if len(track) < 2 else lacking("support")
        rows.append(
            {
                "identity": json.loads(key),
                "credits": len(track),
                "mass": mass_of(last),
                "position": position_of(last, shape, lines.births, clock_written),
                "velocity": velocity,
                "momentum": momentum_of(last),
                "energy": energy_of(last, None, action),
                "bound_or_free": bound_or_free(track, shape, lines.births),
                "counts": {int(c["window"][1]): c.get("count") for c in track},
            }
        )
    for credit in lines.credits:
        if identity_of(credit) is not None:
            continue
        rows.append(
            {
                "identity": lacking("identity"),
                "credits": 1,
                "mass": mass_of(credit, birth_beside(credit, shape, lines.births)),
                "position": position_of(credit, shape, lines.births, clock_written),
                "velocity": lacking("identity"),
                "momentum": momentum_of(credit),
                "energy": energy_of(credit, None, action),
                "bound_or_free": bound_or_free([credit], shape, lines.births),
                "counts": {int(credit["window"][1]): credit.get("count")}
                if credit.get("window")
                else {},
            }
        )
    rows.extend(born_bodies(lines))
    partners(rows)
    return rows


def born_bodies(lines: Lines) -> list[dict[str, Any]]:
    """One row per child record of the birth lines that carry `records` and `points` (the click's view of the birth): its identity by the family's name and the record's index, its mass from its point, its sense, its position the birth's Node and close; no credit of its own, so velocity, momentum and bound or free are unreadable by name."""
    rows: list[dict[str, Any]] = []
    for birth in lines.births:
        records_, points = birth.get("records"), birth.get("points")
        if records_ is None or points is None:
            continue
        children, senses = birth.get("children") or [], birth.get("senses") or []
        for k, (record, point) in enumerate(zip(records_, points, strict=True)):
            pair = pair_of(point)
            mass: Any = (
                sine_of(pair) if pair is not None and abs(pair[0]) <= pair[1] else lacking("point")
            )
            where = birth["nodes"][0] if birth.get("nodes") else None
            rows.append(
                {
                    "identity": {"family": children[k] if k < len(children) else None, "record": record},
                    "credits": 0,
                    "mass": {
                        "label": children[k] if k < len(children) else lacking("children"),
                        "point": list(pair) if pair else lacking("point"),
                        "mass": mass,
                        "sense": senses[k] if k < len(senses) else lacking("senses"),
                    },
                    "position": {
                        "where": where if where is not None else lacking("nodes"),
                        "when": birth.get("interval"),
                        "born": True,
                    },
                    "velocity": "unreadable: born once, no credit of its own",
                    "momentum": lacking("momentum"),
                    "energy": {"quanta": 1, "rest": mass},
                    "bound_or_free": {
                        "verdict": "unreadable: born once, no credit of its own",
                        "support": None,
                        "beats": [],
                    },
                    "counts": {},
                }
            )
    return rows


def extent_of(coordinates: set[int], extent: int) -> int:
    """The Links of the shortest arc of a ring of `extent` Nodes that covers the coordinates: the ring less its largest gap."""
    ordered = sorted(coordinates)
    gaps = [b - a for a, b in zip(ordered, ordered[1:], strict=False)]
    gaps.append(extent - ordered[-1] + ordered[0])
    return extent - max(gaps) + 1


def violations_of(row: dict[str, Any], counts: list[int], length: int) -> list[str]:
    """The checks of the uncertainty table: a count below one whole quantum or a window below one interval; over two or more credits with their momentum written, a where of one Link at a momentum spread below one unit."""
    found: list[str] = []
    if counts and min(counts) < 1:
        found.append("a count below one whole quantum")
    if length < 1:
        found.append("a window below one interval")
    spread, momentum = row["where_spread"], row["momentum_spread"]
    if row["credits"] > 1 and isinstance(spread, list) and isinstance(momentum, list):
        for axis in AXES:
            if spread[axis] <= 1 and momentum[axis] < 1:
                found.append(f"axis {axis}: a where of one Link at a momentum spread below one unit")
    return found


def uncertainty_table(lines: Lines, shape: Shape | None = None) -> list[dict[str, Any]]:
    """Per family and window: the credits, the count's floor and sum, the window's length N, Delta E Delta t in the click's units (whole quanta over N intervals, the window resolving 2 pi / N in rotation and 2 pi T in Delta E Delta t, against the law's T / 2), the where's spread per axis on the torus, the momentum's spread per axis, their product, and the violation check."""
    shape = shape_of(lines, shape)
    groups: dict[tuple[str, int, int], list[Line]] = defaultdict(list)
    for credit in lines.credits:
        window = credit.get("window") or [credit.get("interval"), credit.get("interval")]
        groups[(str(credit.get("family")), int(window[0]), int(window[1]))].append(credit)
    rows: list[dict[str, Any]] = []
    for (family, first, last), credits in sorted(groups.items()):
        length = last - first + 1
        counts = [int(c["count"]) for c in credits if c.get("count") is not None]
        nodes = [w for w in (where_of(c, shape, lines.births) for c in credits) if isinstance(w, tuple)]
        momenta = [c["momentum"] for c in credits if c.get("momentum") is not None]
        row: dict[str, Any] = {
            "family": family,
            "window": [first, last],
            "intervals": length,
            "credits": len(credits),
            "count_min": min(counts) if counts else lacking("count"),
            "count_sum": sum(counts) if counts else lacking("count"),
            "energy_time": {
                "quanta": min(counts),
                "intervals": length,
                "rotation_resolved": f"2 pi / {length}",
                "product": "2 pi T",
                "floor": "T / 2",
            }
            if counts
            else lacking("count"),
            "distinct_wheres": len(set(nodes)) if nodes else lacking("support", "node_detector"),
        }
        if not nodes:
            row["where_spread"] = lacking("support", "node_detector")
        elif shape is None:
            row["where_spread"] = "the shape lacking: pass --shape"
        else:
            row["where_spread"] = [extent_of({n[axis] for n in nodes}, shape[axis]) for axis in AXES]
        if len(momenta) < len(credits):
            row["momentum_spread"] = row["product"] = lacking("momentum")
        else:
            row["momentum_spread"] = [
                max(m[axis] for m in momenta) - min(m[axis] for m in momenta) for axis in AXES
            ]
            spread = row["where_spread"]
            row["product"] = (
                [x * p for x, p in zip(spread, row["momentum_spread"], strict=True)]
                if isinstance(spread, list)
                else spread
            )
        row["violations"] = violations_of(row, counts, length)
        rows.append(row)
    return rows


def gr_table(lines: Lines, shape: Shape | None = None, light: str = "light") -> dict[str, Any]:
    """The four readings of general relativity from the clicks, each its rows or a note naming what the log lacks: (a) the dilation, a taker's successive `proper` differences over its successive closes' differences (the clock's pace at the taker's content, The paces compose); (b) light's click spacing per Node, the spans between successive closes of light's credits at one where (two wheres at different content give the redshift); (c) the Nodes silent while others click, credited before the log's last close and never after (the missing clicks of a region behind the wall, The horizon); (d) a free body's track against the straight line of the torus."""
    shape = shape_of(lines, shape)
    tracks = tracks_of(lines)
    clock_written = any(c.get("proper") not in (None, 0) for c in lines.credits)
    found: dict[str, Any] = {}
    at_where: dict[Node, list[Line]] = defaultdict(list)
    for credit in lines.credits:
        where = where_of(credit, shape, lines.births)
        if isinstance(where, tuple) and credit.get("window"):
            at_where[where].append(credit)
    dilation: list[dict[str, Any]] = []
    for where, credits in sorted(at_where.items()):  # `proper` is the credited Node's own clock
        ordered = sorted(credits, key=lambda c: int(c["window"][1]))
        for a, b in zip(ordered, ordered[1:], strict=False):
            intervals = int(b["window"][1]) - int(a["window"][1])
            if a.get("proper") is None or b.get("proper") is None or not clock_written or not intervals:
                continue
            elapsed = int(b["proper"]) - int(a["proper"])
            dilation.append(
                {
                    "where": list(where),
                    "identities": [identity_of(a), identity_of(b)],
                    "closes": [a["window"][1], b["window"][1]],
                    "proper": [a["proper"], b["proper"]],
                    "proper_intervals": elapsed,
                    "intervals": intervals,
                    "ratio": elapsed / intervals,
                }
            )
    if not clock_written:
        note = lacking("proper")
    else:
        note = "" if dilation else "one credit per where: no two closes of one Node's clock"
    found["dilation"] = {"rows": dilation, "note": note}
    closes = [int(c["window"][1]) for c in lines.credits if c.get("window")]
    per_where: dict[Node, list[int]] = defaultdict(list)
    lit: dict[Node, list[int]] = defaultdict(list)
    for credit in lines.credits:
        where = where_of(credit, shape, lines.births)
        if isinstance(where, tuple) and credit.get("window"):
            per_where[where].append(int(credit["window"][1]))
            if credit.get("family") == light:
                lit[where].append(int(credit["window"][1]))
    spacing = [
        {"where": list(w), "closes": c, "spacings": [b - a for a, b in zip(c, c[1:], strict=False)]}
        for w, c in sorted(lit.items())
        if len(c) > 1
    ]
    note = "" if spacing else ("no credit of light" if not lit else "one credit per where: no spacing")
    found["light_spacing"] = {"rows": spacing, "note": note}
    silent = [
        {"where": list(w), "credits": len(c), "last_close": max(c)}
        for w, c in sorted(per_where.items())
        if closes and max(c) < max(closes)
    ]
    if not closes:
        note = lacking("window")
    elif len(set(closes)) == 1:
        note = ONE_WINDOW
    else:
        note = "" if silent else "every where credited at the log's last close: no silence to read"
    found["silent"] = {"rows": silent, "note": note, "last_close": max(closes) if closes else None}
    straight: list[dict[str, Any]] = []
    for key, track in tracks.items():
        wheres = [where_of(c, shape, lines.births) for c in track]
        velocity = velocity_of(track[0], track[-1], shape) if len(track) > 1 else None
        if velocity is None or shape is None or not all(isinstance(w, tuple) for w in wheres):
            continue
        if len({int(c["window"][1]) for c in track}) < len(track):
            straight.append({"identity": json.loads(key), "credits": len(track), "note": NO_ONE_BODY})
            continue
        start, began = wheres[0], int(track[0]["window"][1])
        deviations = []
        for where, credit in zip(wheres, track, strict=True):
            elapsed = int(credit["window"][1]) - began
            assert isinstance(where, tuple) and isinstance(start, tuple)
            deviations.append(
                [
                    wrapped(
                        where[axis] - start[axis] - velocity["per_interval"][axis] * elapsed, shape[axis]
                    )
                    for axis in AXES
                ]
            )
        straight.append(
            {
                "identity": json.loads(key),
                "credits": len(track),
                "per_interval": velocity["per_interval"],
                "deviations": deviations,
                "note": "two credits: straight by construction" if len(track) == 2 else "",
            }
        )
    note = (
        "" if straight else (lacking("identity") if not tracks else "one credit per identity: no track")
    )
    found["tracks"] = {"rows": straight, "note": note}
    return found


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("log", type=Path, help="the clicks log, <world>.clicks.jsonl")
    parser.add_argument(
        "--shape",
        type=int,
        nargs=3,
        metavar=("X", "Y", "Z"),
        default=None,
        help="the torus's extent per axis, where the lines name too few Nodes to give it",
    )
    parser.add_argument(
        "--action",
        type=int,
        default=None,
        help="T, the quantum's action, for the band's form of the energy",
    )
    parser.add_argument("--out", type=Path, default=None, help="write the tables as JSON here")
    parser.add_argument(
        "--light",
        default=None,
        help="the massless family's name for the GR table's spacing; the first credit's family otherwise",
    )
    args = parser.parse_args(argv)
    lines = read_log(args.log)
    declared = (args.shape[0], args.shape[1], args.shape[2]) if args.shape else None
    shape = shape_of(lines, declared)
    light = args.light or (str(lines.credits[0].get("family")) if lines.credits else "light")
    tables = {
        "log": str(args.log),
        "lines": {
            "credits": len(lines.credits),
            "births": len(lines.births),
            "lays": len(lines.lays),
            "others": len(lines.others),
        },
        "shape": list(shape) if shape else lacking("shape"),
        "bodies": bodies_table(lines, shape, args.action),
        "uncertainty": uncertainty_table(lines, shape),
        "gr": gr_table(lines, shape, light),
    }
    text = json.dumps(tables, indent=1)
    if args.out is not None:
        args.out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
