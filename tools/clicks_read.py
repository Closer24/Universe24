"""The reader of the clicks log alone, a host tool that computes nothing from a Node's level (ALGEBRA.md, The click writes on the lattice; The click's read of the board; No click names a Node; The uncertainty relation is the detector's three declarations; The uncertainty principle is the record's and the click's; The board is deterministic, but it cannot be read through clicks, because of the uncertainty principle; The click's unit: the whole of a click is the detector's own transition; What a click reads of a quantum; The lattice momentum; The paces compose; The horizon; the builder's rule of method of 2026-10-24, #2187 comment 6382837913: the clicks log is the record, the eras and nodes lines are looks). From the credit, birth and lay lines of `<world>.clicks.jsonl` and nothing else it reads what the credits say of the bodies: the mass (`point`, the reduced pair [num, den] the click read, T sin omega in T's unit, and the rest, the record's own point with no label from the click's four pairs, 3 cos omega / SUM_a cos k_a, 2026-10-24), the position (`support`, the shell Node of a body's click, or the board's own click's Node by its x-major index `node_detector`, and the window's close), the velocity (two credits of one `identity`, the Links between them on the torus over the intervals between their closes, and over the taker's own `proper` intervals), the momentum (`momentum`, per axis [sign_a, num_a, den_a], the frame's running cosine along the axis, 2 cos k_a = (a_{+a} + a_{-a}) / a_i, with the Link current's sign, as the click's view writes it since 2026-10-24: p_a = sign_a x T sin k_a per Link in T's unit, the leg of the pair over its den, and the word where the pair lies outside the circle, no running wave along the axis; the former `fan` and `recoil` struck from the line the same day), the energy (`count` whole quanta, each T sin omega of the point, and with the momentum the band's form from the pairs directly), bound or free (the credits of one identity at one Node, the `beat` between their closes), and beside the bodies the uncertainty table per family and window (the count's floor, the where's spread on the torus in Links, the momentum's spread in T's unit and their product in Links x T against the law's floor T / 2) and the GR table (the dilation of a taker's `proper` against the board's intervals, light's click spacing per Node, the Nodes silent while others click, a free body's track against the straight line). Every cell the log cannot fill names the key it lacks.

The seven tables of the record's checks (the owner's words of 2026-10-24, 16:3x and 16:4x UTC: all the epochs since the big bang must show in the clicks, another big bang that does not erase information, the attraction of bodies that click, relativity in the clicks, the Links' lengthening measured in the clicks, all in one world; one place decodes the clicks and may use whatever it wants, like a human, distinguishing bound bodies, moving ones, light), each a reading of the clicks log with the eras and nodes logs as looks beside it where the table names them, nothing of it in src/: `density_table` (the clicks per interval and the epochs named bang, rise, top, fall and return, their bounds the eras log's tops and returns, tools/look/captions.py, or the density's own runs where no eras log is given), `tracks_table` (per identity the series of its credits over time, the where the torus coordinates), `distance_table` (per common close the torus's shortest distance in Links between two tracks and its slope in Links per interval, the two longest bodies' tracks or two the caller names; the tracks that stand named, light's fall from the GR table beside them), `ledger_table` (per cycle the bang, the top, the return, the births per point and sense, the eras log's quanta per family before and after the return and the tracks whose credits span it, captions.ledger_of's shape), `dilation_vs_clock` (the GR table's dilation per where against the content's clock, the pace e^-U from the nodes log's `length` summed over the intervals, within one interval or not), `spacing_vs_length` (light's click spacing per where with e^U at each close and the sign of the relation over the board, on both sides of a return) and `births_table` (per cycle per point, named by captions.captions_for, per sense the count, the senses' sum per cycle); every number of them from the lines, the names of nature from the legend.

Usage: `PYTHONPATH=src python tools/clicks_read.py <world>.clicks.jsonl [--shape X Y Z] [--eras <world>.eras.jsonl] [--nodes <world>.nodes.jsonl] [--bodies '[F, R]' '[F, R]'] [--out <file>.json]`
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import defaultdict
from fractions import Fraction
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
NO_WAVE = "no running wave along the axis: the pair lies outside the circle"
ONE_NODE_LAY = "a one-Node lay: SUM_a cos k_a = 0, nothing beside the Node to read; a body is counted from its many clicks"
VACUUM_PACES = "exact where the Node's pace equals the board's: the Node's clock at the board's interval, the vacuum's paces; the rest's value stands as read either way"
FLOOR = "T / 2 in Links x T: the where's spread in Links times the momentum's spread in T's unit"
HALF = Fraction(1, 2)  # the law's floor of Delta x Delta p in Links x T


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


def mass_of(credit: Line, birth: Line | None = None) -> dict[str, Any]:
    """The mass: `point`, the reduced pair the click read from the three levels, as T sin omega in T's unit (a point at rest; for the credited massless record the quantum's frequency), with the `rest`, the record's own point from the click's four pairs with no label (`rest_of`, 2026-10-24), the `beat` (3 T sin omega, the click's own unit), the `kind` (1 or 2, the record's width) and the `sense` (-1, 0, 1, the Wronskian's sign); the family's label (`realised`, `emitted` or the birth's `children`) names the family and no number; the birth's `points` and `records` are the children's."""
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
    found["rest"] = rest_of(credit)
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


def cosine_of(reading: Any) -> tuple[int, tuple[int, int]] | None:
    """One axis of `momentum` as the click's view writes it (2026-10-24), [sign_a, num_a, den_a]: the Link current's sign along the axis with the frame's running cosine, 2 cos k_a = (a_{+a} + a_{-a}) / a_i, as the reduced pair, (sign, (num, den)); None where the axis holds no reading or the record's lines read different cosines there (the lines' pairs in order after the sign)."""
    if reading is None or len(reading) != 3 or not all(isinstance(v, int) for v in reading):
        return None
    return (int(reading[0]), (int(reading[1]), int(reading[2])))


def p_of(reading: Any) -> float | str:
    """p_a in T's unit from one axis of `momentum`: sign_a x leg_below(den_a^2 - num_a^2) / den_a, T sin k_a per Link with the Link current's sign (ALGEBRA.md, The lattice momentum, Part F; exact at a Pythagorean pair, the leg's floor otherwise); the word where the pair lies outside the circle (|num_a| > den_a: no running wave along the axis), or the lines' different cosines named."""
    cosine = cosine_of(reading)
    if cosine is None:
        return lacking("momentum") if reading is None else f"the lines read different cosines: {reading}"
    sign, (num, den) = cosine
    if abs(num) > den:
        return NO_WAVE
    return sign * leg_below(den * den - num * num) / den


def rest_of(credit: Line) -> dict[str, Any] | str:
    """The mass from the click with no label (2026-10-24): at the plain paces Rule3's line at a mode is 3 den cos omega(k) = num SUM_a cos k_a, so the record's own rest point is num / den = 3 cos omega / SUM_a cos k_a = 3 (after + before) / SUM_j now_j, an exact rational of the click's four pairs, the temporal `point` and the three spatial pairs of `momentum`: the reduced pair [num, den] with its value (1 for the massless record at every click whatever k); None named where SUM_a cos k_a = 0 (`ONE_NODE_LAY`: a born body's mass is read at its later clicks); the paces: exact at the vacuum's paces (`VACUUM_PACES`, the Node's clock `proper` at the board's interval), and approximate near matter, where the paces change the reaches, named where `proper` shows the Node's clock off the board's interval (the dilation rows of the GR table), the paces' correction lacking."""
    pair, momentum = pair_of(credit.get("point")), credit.get("momentum")
    if pair is None or momentum is None:
        return lacking(
            *[key for key, value in (("point", pair), ("momentum", momentum)) if value is None]
        )
    cosines = [cosine for cosine in map(cosine_of, momentum) if cosine is not None]
    if len(cosines) < len(momentum):
        return f"the lines read different cosines: {momentum}"
    total = sum((Fraction(num, den) for _sign, (num, den) in cosines), Fraction(0))
    if total == 0:
        return {"rest": None, "note": ONE_NODE_LAY}
    rest = 3 * Fraction(pair[0], pair[1]) / total
    found: dict[str, Any] = {"rest": [rest.numerator, rest.denominator], "value": float(rest)}
    proper, window = credit.get("proper"), credit.get("window")
    if proper is None or not window:
        found["paces"] = lacking("proper", "window")
    elif int(proper) == int(window[1]):
        found["paces"] = VACUUM_PACES
    else:
        found["paces"] = (
            f"approximate: the Node's clock {proper} against the board's interval {window[1]}, "
            "the paces change the reaches near matter, the paces' correction lacking; "
            "the rest's value stands as read either way"
        )
    return found


def momentum_of(credit: Line) -> dict[str, Any]:
    """The momentum kept: `momentum` as the click wrote it, per axis [sign_a, num_a, den_a] (the frame's running cosine with the Link current's sign, 2026-10-24), and `p`, p_a per axis in T's unit (`p_of`); both named lacking where the log has none (the key None at a level now 0, or absent on a log before the click's view); the former `fan` and `recoil`, struck from the line on 2026-10-24, read from no log."""
    momentum = credit.get("momentum")
    if momentum is None:
        return {"momentum": lacking("momentum"), "p": lacking("momentum")}
    return {"momentum": momentum, "p": [p_of(reading) for reading in momentum]}


def energy_of(credit: Line, point: Any = None) -> dict[str, Any]:
    """The energy: `count` whole quanta; at rest the count times T sin omega of the point, in T's unit; with the momentum the band's form from the click's pairs directly, cos omega(k) = cos omega_0 - (1 / 3) SUM_a (1 - cos k_a) with cos k_a = num_a / den_a, an exact rational, the count times its sine in T's unit (the leg's floor over the den; no T needed); the word where an axis reads no running wave or the lines read different cosines."""
    count = credit.get("count")
    pair = pair_of(credit.get("point") if point is None else point)
    found: dict[str, Any] = {"quanta": count if count is not None else lacking("count")}
    if count is None or pair is None or abs(pair[0]) > pair[1]:
        found["rest"] = lacking("count") if count is None else lacking("point")
        found["with_momentum"] = found["rest"]
        return found
    found["rest"] = count * sine_of(pair)
    momentum = credit.get("momentum")
    cosines = [cosine for cosine in map(cosine_of, momentum or ()) if cosine is not None]
    if momentum is None:
        found["with_momentum"] = lacking("momentum")
    elif len(cosines) < len(momentum):
        found["with_momentum"] = f"the lines read different cosines: {momentum}"
    elif any(abs(num) > den for _sign, (num, den) in cosines):
        found["with_momentum"] = NO_WAVE
    else:
        lost = sum((1 - Fraction(num, den) for _sign, (num, den) in cosines), Fraction(0)) / 3
        cosine = Fraction(pair[0], pair[1]) - lost
        if abs(cosine) > 1:
            found["with_momentum"] = f"cos omega(k) = {cosine} outside the circle: no band reading"
        else:
            found["with_momentum"] = count * sine_of((cosine.numerator, cosine.denominator))
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


def bodies_table(lines: Lines, shape: Shape | None = None) -> list[dict[str, Any]]:
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
                "energy": energy_of(last),
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
                "energy": energy_of(credit),
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
    """The checks of the uncertainty table: a count below one whole quantum or a window below one interval; over two or more credits with their momentum written, a product Delta x Delta p per axis (the where's spread in Links times the momentum's spread in T's unit, Links x T) below the law's floor T / 2 (`FLOOR`), named with its number; an axis whose spread is a word (no running wave, the lines' different cosines) is not judged."""
    found: list[str] = []
    if counts and min(counts) < 1:
        found.append("a count below one whole quantum")
    if length < 1:
        found.append("a window below one interval")
    product = row["product"]
    if row["credits"] > 1 and isinstance(product, list):
        for axis in AXES:
            if isinstance(product[axis], float) and product[axis] < HALF:
                found.append(
                    f"axis {axis}: Delta x Delta p = {product[axis]} Links x T, below the law's floor T / 2"
                )
    return found


def spread_of(values: list[Any]) -> float | str:
    """max - min over the credits of one axis's p_a in T's unit; the first word where a credit's axis reads one (no running wave along the axis, or the lines' different cosines)."""
    words = [value for value in values if isinstance(value, str)]
    if words:
        return words[0]
    return float(max(values) - min(values))


def uncertainty_table(lines: Lines, shape: Shape | None = None) -> list[dict[str, Any]]:
    """Per family and window: the credits, the count's floor and sum, the window's length N, Delta E Delta t in the click's units (whole quanta over N intervals, the window resolving 2 pi / N in rotation and 2 pi T in Delta E Delta t, against the law's T / 2), the where's spread per axis on the torus in Links, the momentum's spread per axis in T's unit (max - min of p_a over the credits, `p_of`), their product per axis in Links x T, the law's floor T / 2 named (`FLOOR`), and the violation check (`violations_of`)."""
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
            found = [[p_of(reading) for reading in m] for m in momenta]  # p_a per credit in T's unit
            row["momentum_spread"] = [spread_of([p[axis] for p in found]) for axis in AXES]
            spread = row["where_spread"]
            row["product"] = (
                [
                    x * p if isinstance(p, float) else p
                    for x, p in zip(spread, row["momentum_spread"], strict=True)
                ]
                if isinstance(spread, list)
                else spread
            )
        row["floor"] = FLOOR
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


CAPTIONS = Path(__file__).with_name("look") / "captions.py"
CAPTIONS_NAME = "clicks_read_captions"
ZERO = {"credits": 0, "births": 0, "lays": 0}
STANDS = "the tracks stand: the one-Node body's group velocity 0"
FIRST_RISE = "the first rise alone"
NO_SHAPE = "the shape lacking: pass --shape"
NO_ERAS = "the eras log lacking: pass --eras"
NO_NODES = "the nodes log lacking: pass --nodes"
WORDS = {
    -1: "the spacing longer where e^U is smaller",
    0: "the spacing equal at every length",
    1: "the spacing longer where e^U is larger",
}  # the sign of light's click spacing against the Link's length over the board


def captions_module() -> Any:
    """tools/look/captions.py loaded by its path, the legend's functions a look beside the clicks (held_rows, returns_of, tops_of, spans_of, captions_for, shown, parse_log): the reader computes nothing of the engine; the names of nature it takes from the legend."""
    found = sys.modules.get(CAPTIONS_NAME)
    if found is None:
        spec = importlib.util.spec_from_file_location(CAPTIONS_NAME, CAPTIONS)
        if spec is None or spec.loader is None:
            raise ImportError(f"{CAPTIONS} cannot be loaded")
        found = importlib.util.module_from_spec(spec)
        sys.modules[CAPTIONS_NAME] = found
        spec.loader.exec_module(found)
    return found


def interval_of(line: Line) -> int | None:
    """A line's interval: `interval`, else a credit's window's close; None where neither stands."""
    if line.get("interval") is not None:
        return int(line["interval"])
    window = line.get("window")
    return int(window[1]) if window else None


def counts_per_interval(lines: Lines) -> dict[int, dict[str, int]]:
    """The clicks per interval, {interval: {credits, births, lays}} over every interval a line names, in order; an interval with no line has no entry: 0 of each."""
    found: dict[int, dict[str, int]] = {}
    for key, kind in (("credits", lines.credits), ("births", lines.births), ("lays", lines.lays)):
        for line in kind:
            at = interval_of(line)
            if at is not None:
                found.setdefault(at, dict(ZERO))[key] += 1
    return dict(sorted(found.items()))


def cycles_of(eras: list[Line]) -> list[dict[str, Any]]:
    """The cycles the eras log gives (captions.returns_of and tops_of on the held row): per cycle the bang's interval, the top within it (the largest where several) with its volume, the cycle's last interval and the return, the next bang's interval, None for the open last cycle."""
    captions = captions_module()
    _lines, held = captions.held_rows(eras)
    bangs, tops = captions.returns_of(held), captions.tops_of(held)
    found: list[dict[str, Any]] = []
    for k, bang in enumerate(bangs):
        to = int(bangs[k + 1]) - 1 if k + 1 < len(bangs) else int(held[-1][0])
        inside = [(at, volume) for at, volume in tops if bang <= at <= to]
        top = max(inside, key=lambda t: t[1]) if inside else None
        found.append(
            {
                "cycle": k + 1,
                "bang": int(bang),
                "to": to,
                "top": top[0] if top else None,
                "volume": top[1] if top else None,
                "return": int(bangs[k + 1]) if k + 1 < len(bangs) else None,
            }
        )
    return found


def epoch_row(
    name: str,
    cycle: int,
    first: int,
    last: int,
    counts: dict[int, dict[str, int]],
    densest: int | None,
    volume: Any = None,
) -> dict[str, Any]:
    """One epoch's row: its name, cycle and bounds, the clicks within it summed, the credits per interval and the clicks' own words (the densest clicks of the run where the epoch holds them, quiet where no line falls in it)."""
    inside = [counts.get(at, ZERO) for at in range(first, last + 1)]
    credits, births, lays = (sum(c[key] for c in inside) for key in ("credits", "births", "lays"))
    intervals = last - first + 1
    over = f"over {intervals} interval" + ("s" if intervals != 1 else "")
    words = f"{credits} credits, {births} births, {lays} lays {over}"
    if densest is not None and first <= densest <= last and credits:
        words += f"; the densest clicks of the run at {densest}"
    if credits + births + lays == 0:
        words = f"quiet: no line of the clicks log {over}"
    row: dict[str, Any] = {
        "name": name,
        "cycle": cycle,
        "from": first,
        "to": last,
        "intervals": intervals,
        "credits": credits,
        "births": births,
        "lays": lays,
        "credits_per_interval": credits / intervals,
        "words": words,
    }
    if volume is not None:
        row["volume"] = volume
    return row


def density_table(lines: Lines, eras: list[Line] | None = None) -> dict[str, Any]:
    """The epochs read from the clicks' density: per interval {credits, births, lays} (`per_interval`, the intervals with a line), the densest interval, the births' spans (captions.spans_of on the births per interval) and the epochs, each {name, cycle, from, to, intervals, credits, births, lays, credits_per_interval, words}: with the eras log the bounds are its tops and returns (`cycles_of`), the first cycle's first interval the bang, every later cycle's first the return, between them the rise, the top (with its volume) and the fall, and where the log gives one cycle with no top and no return the one epoch after the bang is named `the first rise alone`; without the eras log the bounds are the density's own runs, the first run of intervals with credits the bang, every later run `clicks` and the gaps between them `quiet`."""
    captions = captions_module()
    counts = counts_per_interval(lines)
    rows = [{"interval": at, **c} for at, c in counts.items()]
    lit = [r for r in rows if r["credits"]]
    densest = max(lit, key=lambda r: (r["credits"], -r["interval"]))["interval"] if lit else None
    found: dict[str, Any] = {"per_interval": rows}
    found["densest"] = (
        {"interval": densest, "credits": counts[densest]["credits"]}
        if densest is not None
        else "no credit line"
    )
    series = [(at, counts.get(at, ZERO)) for at in range(min(counts), max(counts) + 1)] if counts else []
    found["birth_spans"] = [
        {"from": a, "to": b, "most": m}
        for a, b, m in captions.spans_of([(at, c["births"]) for at, c in series])
    ]
    epochs: list[dict[str, Any]] = []
    if eras is not None:
        cycles = cycles_of(eras)
        for cycle in cycles:
            k, bang, to, top = cycle["cycle"], cycle["bang"], cycle["to"], cycle["top"]
            epochs.append(epoch_row("bang" if k == 1 else "return", k, bang, bang, counts, densest))
            if top is not None:
                if top > bang + 1:
                    epochs.append(epoch_row("rise", k, bang + 1, top - 1, counts, densest))
                epochs.append(epoch_row("top", k, top, top, counts, densest, cycle["volume"]))
                if to > top:
                    epochs.append(epoch_row("fall", k, top + 1, to, counts, densest))
            elif to > bang:
                name = FIRST_RISE if len(cycles) == 1 else "rise"
                epochs.append(epoch_row(name, k, bang + 1, to, counts, densest))
        bounds = "the eras log's tops and returns"
        if not cycles:
            bounds += ": no row of the held family, no epoch"
        elif len(cycles) == 1 and cycles[0]["top"] is None:
            bounds += f"; no top and no return in the log: {FIRST_RISE}"
    else:
        dense = captions.spans_of([(at, c["credits"]) for at, c in series])
        for number, (first, last, _most) in enumerate(dense):
            if number:
                gap = (dense[number - 1][1] + 1, first - 1)
                epochs.append(epoch_row("quiet", number, gap[0], gap[1], counts, densest))
            epochs.append(
                epoch_row("bang" if number == 0 else "clicks", number + 1, first, last, counts, densest)
            )
        bounds = "the density's own runs: no eras log, the clicks name no top and no return"
    found["epochs"], found["bounds"] = epochs, bounds
    return found


def tracks_table(lines: Lines, shape: Shape | None = None) -> dict[str, Any]:
    """Per identity the series of its credits over time, [{close, where, proper, point, sense}] in the order of the closes, the where the torus coordinates from `support` or from the Node's x-major index over the shape (`where_of`); `one_body` where the credits fall one per close, else the credited record at several Nodes in one close (the board's own light), named."""
    shape = shape_of(lines, shape)
    rows: list[dict[str, Any]] = []
    for key, track in tracks_of(lines).items():
        series: list[dict[str, Any]] = []
        for credit in track:
            where = where_of(credit, shape, lines.births)
            row: dict[str, Any] = {"close": int(credit["window"][1])}
            if isinstance(where, tuple):
                row["where"] = list(where)
            else:
                row["where"] = where if where is not None else lacking("support", "node_detector")
            for name in ("proper", "point", "sense"):
                row[name] = credit[name] if credit.get(name) is not None else lacking(name)
            series.append(row)
        series.sort(key=lambda s: (s["close"], str(s["where"])))
        closes = [s["close"] for s in series]
        one_body = len(set(closes)) == len(closes)
        rows.append(
            {
                "identity": json.loads(key),
                "credits": len(track),
                "closes": sorted(set(closes)),
                "one_body": one_body,
                "series": series,
                "note": "" if one_body else NO_ONE_BODY,
            }
        )
    return {"rows": rows, "note": "" if rows else lacking("identity")}


def slope_of(points: list[tuple[float, float]]) -> float | None:
    """The least-squares slope of y over x; None with fewer than two distinct x."""
    if len({x for x, _y in points}) < 2:
        return None
    mean_x = sum(x for x, _y in points) / len(points)
    mean_y = sum(y for _x, y in points) / len(points)
    above = sum((x - mean_x) * (y - mean_y) for x, y in points)
    return above / sum((x - mean_x) ** 2 for x, _y in points)


def light_identity(lines: Lines) -> Identity | None:
    """Light's identity, the one every credit of the board's own click carries (`node_detector` the Node's index); None where none or several."""
    found = {
        identity_of(c)
        for c in lines.credits
        if isinstance(c.get("node_detector"), int) and not isinstance(c.get("node_detector"), bool)
    }
    found.discard(None)
    return found.pop() if len(found) == 1 else None


def track_key(identity: Any) -> str:
    """An identity as `tracks_of` keys it: its JSON, a list for a pair."""
    return json.dumps(list(identity) if isinstance(identity, list | tuple) else identity)


def light_fall(lines: Lines, shape: Shape | None, light: Identity | None) -> Any:
    """Light's fall from the GR table's track rows: the row of light's identity (its velocity per interval and its deviations from the straight line, or the credited record at several Nodes named) where the table has it, else the words why not."""
    if light is None:
        return "no identity of light: no credit of the board's own click carries one"
    rows = gr_table(lines, shape)["tracks"]["rows"]
    row = next((r for r in rows if list(r["identity"]) == list(light)), None)
    return row if row is not None else f"light {list(light)}: no track row in the GR table"


def distance_table(
    lines: Lines, shape: Shape | None = None, a: Any = None, b: Any = None
) -> dict[str, Any]:
    """Per common close the torus's shortest distance in Links between two tracks' wheres (the shortest signed Links per axis, the shortest path's Links |dx| + |dy| + |dz| as the distance and the straight line's square beside it, no root taken) and over the closes its least-squares slope in Links per interval and its fall, the last distance less the first; the two identities `a` and `b` as the caller names them, else the two longest tracks of bodies (one credit per close, light's identity apart); where both tracks stand at one Node the note says so by name (`STANDS`), light's fall from the GR table beside it (`light_fall`); with fewer than two bodies' tracks the note says the check reads light's fall alone."""
    shape = shape_of(lines, shape)
    tracks = tracks_of(lines)
    light = light_identity(lines)
    light_key = track_key(light) if light is not None else None
    bodies = sorted(
        (
            key
            for key, track in tracks.items()
            if key != light_key
            and len(track) > 1
            and len({int(c["window"][1]) for c in track}) == len(track)
        ),
        key=lambda key: (-len(tracks[key]), key),
    )
    chosen = [track_key(x) for x in (a, b) if x is not None] or bodies[:2]
    found: dict[str, Any] = {
        "identities": [json.loads(key) for key in chosen],
        "rows": [],
        "slope": None,
        "fall": None,
        "note": "",
        "light_fall": light_fall(lines, shape, light),
    }
    if len(chosen) < 2:
        found["note"] = "fewer than two bodies' tracks" + (
            ": the light's one track alone, the check reads light's fall alone"
            if light_key in tracks
            else ""
        )
        return found
    missing = [key for key in chosen if key not in tracks]
    if missing:
        found["note"] = "no track of " + ", ".join(missing)
        return found
    if shape is None:
        found["note"] = NO_SHAPE
        return found
    wheres = [{int(c["window"][1]): where_of(c, shape, lines.births) for c in tracks[k]} for k in chosen]
    for close in sorted(set(wheres[0]) & set(wheres[1])):
        p, q = wheres[0][close], wheres[1][close]
        if isinstance(p, tuple) and isinstance(q, tuple):
            links = [shortest(q[axis] - p[axis], shape[axis]) for axis in AXES]
            found["rows"].append(
                {
                    "close": close,
                    "wheres": [list(p), list(q)],
                    "links": links,
                    "distance": sum(abs(d) for d in links),
                    "square": sum(d * d for d in links),
                }
            )
    rows = found["rows"]
    if not rows:
        found["note"] = "no common close of the two tracks"
        return found
    found["slope"] = slope_of([(float(r["close"]), r["distance"]) for r in rows])
    found["fall"] = rows[-1]["distance"] - rows[0]["distance"]
    standing = [len({w for w in track.values() if isinstance(w, tuple)}) == 1 for track in wheres]
    if all(standing):
        found["note"] = STANDS
    elif found["fall"] < 0:
        found["note"] = "the distance falls over the run"
    else:
        found["note"] = "the distance holds" if found["fall"] == 0 else "the distance grows over the run"
    return found


def quanta_at(by_interval: dict[int, Line], at: int | None) -> dict[str, int] | None:
    """The eras log's quanta per family at an interval (the `quanta` of its line, each family's `quanta` count); None where the log has no such line."""
    line = by_interval.get(at) if at is not None else None
    if line is None or not isinstance(line.get("quanta"), dict):
        return None
    return {
        family: int((q.get("quanta") if isinstance(q, dict) else q) or 0)
        for family, q in line["quanta"].items()
    }


def births_in(lines: Lines, first: int, last: int) -> list[Line]:
    """The birth lines whose interval lies within [first, last]."""
    return [
        b
        for b in lines.births
        if first <= (interval_of(b) if interval_of(b) is not None else first - 1) <= last
    ]


def born_by_point(births: list[Line]) -> tuple[dict[str, dict[str, int]], dict[str, Any]]:
    """The births' children counted per point (the child's name) and sense, and each point's pair where the birth lines carry `points`."""
    counts: dict[str, dict[str, int]] = {}
    points: dict[str, Any] = {}
    for birth in births:
        children, senses = birth.get("children") or [], birth.get("senses") or []
        pairs = birth.get("points") or []
        for k, child in enumerate(children):
            sense = str(senses[k]) if k < len(senses) else lacking("senses")
            per = counts.setdefault(str(child), {})
            per[sense] = per.get(sense, 0) + 1
            if k < len(pairs):
                points[str(child)] = pairs[k]
    return counts, points


def ledger_table(lines: Lines, eras: list[Line]) -> dict[str, Any]:
    """The ledger per cycle, captions.ledger_of's shape as a reader table: per cycle {cycle, bang, to, top, volume, return, open, births (per point and sense), points, counts (the eras log's quanta per family at the top, before the return and at the return), erased (the families whose count stood above 0 before the return and fell to 0 at it), tracks_across (the identities whose credits span the return, with their closes before and after), credits, lays, turns, horizon, standing (the quanta at the cycle's end)}, and the one sentence the rows show."""
    captions = captions_module()
    eras_lines, _held = captions.held_rows(eras)
    by_interval = {int(line["interval"]): line for line in eras_lines}
    tracks = tracks_of(lines)
    rows: list[dict[str, Any]] = []
    for cycle in cycles_of(eras):
        bang, to, back = cycle["bang"], cycle["to"], cycle["return"]
        born, points = born_by_point(births_in(lines, bang, to))
        before = quanta_at(by_interval, back - 1) if back is not None else None
        after = quanta_at(by_interval, back) if back is not None else None
        erased = (
            [f for f, n in before.items() if n > 0 and after.get(f, 0) == 0]
            if before is not None and after is not None
            else []
        )
        across: list[dict[str, Any]] = []
        for key, track in tracks.items():
            closes = [int(c["window"][1]) for c in track]
            if back is not None and min(closes) < back <= max(closes):
                across.append(
                    {
                        "identity": json.loads(key),
                        "closes_before": sum(1 for c in closes if c < back),
                        "closes_after": sum(1 for c in closes if c >= back),
                    }
                )
        inside = [line for at, line in by_interval.items() if bang <= at <= to]
        rows.append(
            {
                **{k: cycle[k] for k in ("cycle", "bang", "to", "top", "volume", "return")},
                "open": back is None,
                "births": born,
                "points": points,
                "counts": {
                    "at_top": quanta_at(by_interval, cycle["top"]),
                    "before_return": before,
                    "at_return": after,
                },
                "erased": erased,
                "tracks_across": across,
                "credits": sum(1 for c in lines.credits if bang <= (interval_of(c) or bang - 1) <= to),
                "lays": sum(1 for lay in lines.lays if bang <= (interval_of(lay) or bang - 1) <= to),
                "turns": sum(int(line.get("fires", 0) or 0) for line in inside),
                "horizon": max((int(line.get("horizon", 0) or 0) for line in inside), default=0),
                "standing": quanta_at(by_interval, to),
            }
        )
    closed = [row for row in rows if row["return"] is not None]
    erased_rows = [row for row in closed if row["erased"]]
    if not rows:
        finding = "No bang read: the eras log holds no row of the held family."
    elif not closed:
        finding = (
            f"One cycle in the intervals logged, from {rows[0]['bang']} to {rows[0]['to']}: no return."
        )
    elif erased_rows:
        finding = "Erased across a return: " + "; ".join(
            f"cycle {row['cycle']} at {row['return']}: {', '.join(row['erased'])}" for row in erased_rows
        )
    else:
        crossing = sum(len(row["tracks_across"]) for row in closed)
        finding = (
            f"Nothing erased across the {len(closed)} returns: every family's count above 0 before a return "
            f"stands at it; {crossing} tracks cross a return."
        )
    return {"rows": rows, "finding": finding}


def index_of(where: Any, shape: Shape) -> int:
    """A Node's x-major index over the shape, the nodes log's order."""
    return int(where[0]) * shape[1] * shape[2] + int(where[1]) * shape[2] + int(where[2])


def length_at(by_interval: dict[int, Line], at: int, index: int) -> float | None:
    """The Link's length e^U at a Node and interval from the nodes log's `length`; None where the log lacks the line, the Node or a length above 0."""
    line = by_interval.get(at)
    lengths = line.get("length") if line is not None else None
    if not isinstance(lengths, list) or index >= len(lengths) or not lengths[index]:
        return None
    return float(lengths[index])


def by_interval_of(nodes: list[Line]) -> dict[int, Line]:
    """The nodes log's lines by interval."""
    return {int(line["interval"]): line for line in nodes if line.get("interval") is not None}


def dilation_vs_clock(lines: Lines, nodes: list[Line], shape: Shape | None = None) -> dict[str, Any]:
    """The GR table's dilation per where (successive credits at one Node, `proper_intervals` over `intervals`) against the clock the Node's content gives, the pace e^-U = 1 / `length` from the nodes log at that Node: per row the two closes' lengths and paces, the clock's intervals (the pace summed over the intervals after the first close, or the two closes' mean pace over the intervals where the log lacks some, named), the difference proper less clock and whether it lies within one interval; the verdict over every where judged."""
    shape = shape_of(lines, shape)
    dilation = gr_table(lines, shape)["dilation"]
    by_interval = by_interval_of(nodes)
    rows: list[dict[str, Any]] = []
    off: list[Any] = []
    for d in dilation["rows"]:
        first, last = (int(x) for x in d["closes"])
        row: dict[str, Any] = {
            key: d[key]
            for key in ("where", "identities", "closes", "proper_intervals", "intervals", "ratio")
        }
        if shape is None:
            row.update(clock_intervals=None, clock=NO_SHAPE, difference=None, within_one_interval=None)
            rows.append(row)
            continue
        index = index_of(d["where"], shape)
        ends = [length_at(by_interval, at, index) for at in (first, last)]
        paces = {at: length_at(by_interval, at, index) for at in range(first + 1, last + 1)}
        row["length"] = ends
        row["pace"] = [1 / x if x else None for x in ends]
        if all(paces.values()):
            row["clock_intervals"] = sum(1 / x for x in paces.values() if x)
            row["clock"] = "the pace e^-U summed over the intervals after the first close"
        elif all(ends):
            lacked = [at for at, x in paces.items() if not x]
            row["clock_intervals"] = (1 / ends[0] + 1 / ends[1]) / 2 * d["intervals"]  # type: ignore[operator]
            row["clock"] = (
                f"the two closes' mean pace over {d['intervals']} intervals: "
                f"the nodes log lacks the Node's length at {lacked}"
            )
        else:
            row.update(
                clock_intervals=None,
                clock="the nodes log lacks the Node's length at the closes",
                difference=None,
                within_one_interval=None,
            )
            rows.append(row)
            continue
        row["difference"] = d["proper_intervals"] - row["clock_intervals"]
        row["within_one_interval"] = abs(row["difference"]) <= 1
        if not row["within_one_interval"]:
            off.append(d["where"])
        rows.append(row)
    judged = [row for row in rows if row["within_one_interval"] is not None]
    if not nodes:
        note = NO_NODES
    else:
        note = dilation["note"] if not rows else ""
    if not judged:
        verdict = "nothing judged: no where with two closes and the Node's length in the nodes log"
    elif not off:
        verdict = (
            "the dilation per Node read from the clicks matches the content's clock within one interval "
            f"at every where judged ({len(judged)})"
        )
    else:
        verdict = f"off by more than one interval at {len(off)} of {len(judged)} wheres: {off}"
    return {"rows": rows, "note": note, "verdict": verdict}


def relation_of(pairs: list[tuple[float, float, int, int]]) -> dict[str, Any]:
    """The relation of light's click spacing to e^U over the spans given, (mean length, spacing, first close, last close): the least-squares slope of the spacing over the mean length, its sign and the words (`WORDS`)."""
    slope = slope_of([(x, y) for x, y, _first, _last in pairs])
    if slope is None:
        words = "no relation read: fewer than two spans at different lengths"
        return {"spans": len(pairs), "slope": None, "sign": None, "words": words}
    sign = 1 if slope > 0 else (-1 if slope < 0 else 0)
    return {"spans": len(pairs), "slope": slope, "sign": sign, "words": WORDS[sign]}


def spacing_vs_length(
    lines: Lines,
    nodes: list[Line],
    shape: Shape | None = None,
    light: str = "light",
    eras: list[Line] | None = None,
) -> dict[str, Any]:
    """Light's click spacing per where (the GR table's `light_spacing`, the spans between successive closes of light's credits at one Node) with the Link's length e^U from the nodes log at each close and the span's mean, and over the board the relation's sign (`relation_of`: the spacing against the mean length over every span); with the eras log the same on both sides of every return (the spans closed before it, the spans begun at or after it, the spans across it counted) and whether the two sides agree."""
    shape = shape_of(lines, shape)
    spacing = gr_table(lines, shape, light)["light_spacing"]
    by_interval = by_interval_of(nodes)
    rows: list[dict[str, Any]] = []
    pairs: list[tuple[float, float, int, int]] = []
    for r in spacing["rows"]:
        index = index_of(r["where"], shape) if shape is not None else None
        spans: list[dict[str, Any]] = []
        for first, last in zip(r["closes"], r["closes"][1:], strict=False):
            ends = (
                [length_at(by_interval, at, index) for at in (first, last)]
                if index is not None
                else [None, None]
            )
            mean = (ends[0] + ends[1]) / 2 if ends[0] and ends[1] else None
            spans.append(
                {"closes": [first, last], "spacing": last - first, "length": ends, "mean_length": mean}
            )
            if mean is not None:
                pairs.append((mean, float(last - first), int(first), int(last)))
        rows.append({"where": r["where"], "spans": spans})
    found: dict[str, Any] = {"rows": rows, "relation": relation_of(pairs), "sides": []}
    if eras is not None:
        for back in [cycle["bang"] for cycle in cycles_of(eras)[1:]]:
            before = relation_of([p for p in pairs if p[3] < back])
            after = relation_of([p for p in pairs if p[2] >= back])
            found["sides"].append(
                {
                    "return": back,
                    "before": before,
                    "after": after,
                    "across": sum(1 for p in pairs if p[2] < back <= p[3]),
                    "same_sign": before["sign"] is not None and before["sign"] == after["sign"],
                }
            )
    if not nodes:
        found["note"] = NO_NODES
    elif shape is None:
        found["note"] = NO_SHAPE
    else:
        found["note"] = spacing["note"] if not rows else ""
    return found


def births_table(lines: Lines, eras: list[Line] | None = None) -> dict[str, Any]:
    """The births per cycle per point per sense, from the birth lines: `rows` one per cycle and point {cycle, point, shown (the legend's caption beside the name, captions.captions_for on the eras log's header: electron, proton, neutron by rising sine, the rest their name alone), caption, senses (the count per sense), records (the children of that point), lists (the birth lines whose first child is that point, the legend's count)}, `cycles` one per cycle {cycle, bang, to, lists, records, sense_sum, charge_kept (the senses summing to 0)} and `total` per point over the run; the cycles from the eras log's bangs, else one cycle over the births' own intervals."""
    captions = captions_module()
    names = captions.captions_for(eras[0] if eras else None)
    cycles = cycles_of(eras) if eras else []
    ats = [at for at in (interval_of(b) for b in lines.births) if at is not None]
    if not cycles and ats:
        cycles = [{"cycle": 1, "bang": min(ats), "to": max(ats), "return": None}]
    rows: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    total: dict[str, dict[str, Any]] = {}
    for cycle in cycles:
        births = births_in(lines, cycle["bang"], cycle["to"])
        counts, _points = born_by_point(births)
        for point in sorted(counts):
            senses = dict(sorted(counts[point].items()))
            lists = sum(1 for b in births if (b.get("children") or [None])[0] == point)
            records = sum(senses.values())
            rows.append(
                {
                    "cycle": cycle["cycle"],
                    "point": point,
                    "shown": captions.shown(point, names),
                    "caption": names.get(point),
                    "senses": senses,
                    "records": records,
                    "lists": lists,
                }
            )
            held = total.setdefault(
                point, {"shown": captions.shown(point, names), "lists": 0, "records": 0}
            )
            held["lists"] += lists
            held["records"] += records
        sense_sum = sum(int(s) for b in births for s in (b.get("senses") or []))
        summaries.append(
            {
                "cycle": cycle["cycle"],
                "bang": cycle["bang"],
                "to": cycle["to"],
                "lists": len(births),
                "records": sum(len(b.get("children") or []) for b in births),
                "sense_sum": sense_sum,
                "charge_kept": sense_sum == 0,
            }
        )
    note = "" if lines.births else "no birth line in the clicks log"
    if lines.births and not names:
        note = "no caption: the eras log's header names no points (or no eras log given)"
    return {"rows": rows, "cycles": summaries, "total": total, "note": note}


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
    parser.add_argument("--out", type=Path, default=None, help="write the tables as JSON here")
    parser.add_argument(
        "--light",
        default=None,
        help="the massless family's name for the GR table's spacing; the first credit's family otherwise",
    )
    parser.add_argument(
        "--eras",
        type=Path,
        default=None,
        help="the eras log, a look beside the clicks: the epochs' tops and returns, the ledger's quanta per family, the births' cycles and the legend's names",
    )
    parser.add_argument(
        "--nodes",
        type=Path,
        default=None,
        help="the nodes log, a look beside the clicks: the Link's length e^U per Node and interval, the clock and the spacing read against it",
    )
    parser.add_argument(
        "--bodies",
        nargs=2,
        metavar=("A", "B"),
        default=None,
        help="two identities for the distance table as JSON ('[3, 0]' '[3, 1]'); the two longest bodies' tracks otherwise",
    )
    args = parser.parse_args(argv)
    lines = read_log(args.log)
    captions = captions_module()
    eras = captions.parse_log(args.eras.read_text(encoding="utf-8")) if args.eras else None
    nodes = captions.parse_log(args.nodes.read_text(encoding="utf-8")) if args.nodes else []
    declared = (args.shape[0], args.shape[1], args.shape[2]) if args.shape else None
    if declared is None and eras and isinstance(eras[0].get("shape"), list):
        declared = (int(eras[0]["shape"][0]), int(eras[0]["shape"][1]), int(eras[0]["shape"][2]))
    shape = shape_of(lines, declared)
    light = args.light or (str(lines.credits[0].get("family")) if lines.credits else "light")
    a, b = (json.loads(args.bodies[0]), json.loads(args.bodies[1])) if args.bodies else (None, None)
    tables = {
        "log": str(args.log),
        "lines": {
            "credits": len(lines.credits),
            "births": len(lines.births),
            "lays": len(lines.lays),
            "others": len(lines.others),
        },
        "shape": list(shape) if shape else lacking("shape"),
        "bodies": bodies_table(lines, shape),
        "uncertainty": uncertainty_table(lines, shape),
        "gr": gr_table(lines, shape, light),
        "density": density_table(lines, eras),
        "tracks": tracks_table(lines, shape),
        "distance": distance_table(lines, shape, a, b),
        "ledger": ledger_table(lines, eras) if eras is not None else NO_ERAS,
        "dilation_vs_clock": dilation_vs_clock(lines, nodes, shape) if nodes else NO_NODES,
        "spacing_vs_length": spacing_vs_length(lines, nodes, shape, light, eras) if nodes else NO_NODES,
        "births": births_table(lines, eras),
    }
    text = json.dumps(tables, indent=1)
    if args.out is not None:
        args.out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
