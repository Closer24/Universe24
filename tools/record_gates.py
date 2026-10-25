"""The nineteen gates of the owner's phenomena read on a record's three logs (the owner's words of 2026-10-25: gates for each of these phenomena so that they happen from the loader; nothing declared; the two blind hands' table of that day, agreed cold on PR #2187): each gate reads the clicks log, the Node's clock `proper`, its position (`support`, `node_detector`) and the readings on the credit line with the birth and lay lines, and names the board's view (the eras or nodes log) only where the whole board is the quantity (the volume's returns, tops, velocity and writes; the mean length's runs; the Links at the wall); it returns SHOWN or NOT SHOWN with the logs' numbers and the lack by name, every pass an existence, a sign, an order, a monotonicity or a count read from the logs and no typed threshold. Each gate's docstring is its row of the table, three cells split by ` | `: the view (clicks or board), what it reads with its pass, and the lack named where a verdict is NOT SHOWN. tools/clicks_read.py and tools/look/captions.py are loaded by their paths (the reader's functions, the legend's rules); nothing of the engine is imported. Usage, with PYTHONPATH set to the checkout's src: `PYTHONPATH=src python tools/record_gates.py examples/events/universe24 [--out <file>.json]`, the folder holding the one world's `<world>.clicks.jsonl`, `<world>.eras.jsonl` and `<world>.nodes.jsonl`."""

from __future__ import annotations

import argparse
import json
import runpy
from collections import Counter, defaultdict, namedtuple
from fractions import Fraction
from itertools import combinations, groupby
from pathlib import Path
from types import SimpleNamespace
from typing import Any

SHOWN, NOT_SHOWN = "SHOWN", "NOT SHOWN"
WORD = (NOT_SHOWN, SHOWN)  # the verdict's word by the pass
READER = SimpleNamespace(**runpy.run_path(str(Path(__file__).resolve().with_name("clicks_read.py"))))
CAPTIONS = READER.captions_module()
RATIOS = ("proton_over_electron", "neutron_over_electron", "neutron_over_proton")
FIELDS = "header eras nodes lines shape light places clocks spans bodies lights rims returns tops last v"
Record = namedtuple("Record", FIELDS)  # the three logs read once, with the readings every gate shares


def steps(values: Any) -> list[tuple[Any, Any]]:
    return list(zip(values, values[1:], strict=False))


def record_of(header: dict[str, Any], eras: list[Any], nodes: list[Any], lines: Any) -> Any:
    """A record from the logs' lines (the eras rows with their header, the nodes lines, the clicks by kind): the shape, the seed family's index (light's), every credit's Node, per Node its clock's (interval, proper) series and the spans' paces, the bodies' and light's credits with their Nodes, the bodies' rims per close, and the volume's returns, tops, last interval and velocity per interval (the board's)."""
    shape, light = tuple(int(x) for x in header["shape"]), list(header["families"]).index(header["seed"])
    places = [READER.where_of(c, shape, lines.births) for c in lines.credits]
    kinds = [(c, w, c["identity"][0] == light) for c, w in zip(lines.credits, places, strict=True)]
    clocks: dict[Any, dict[int, int]] = defaultdict(dict)
    rims: dict[Any, dict[int, set[Any]]] = defaultdict(dict)
    for c, w, is_light in kinds:
        clocks[w][c["interval"]] = c["proper"]
        if not is_light:
            rims[READER.identity_of(c)].setdefault(c["interval"], set()).add(w)
    ser = {w: sorted(s.items()) for w, s in clocks.items()}
    spans = {w: [(a, b, Fraction(q - p, b - a)) for (a, p), (b, q) in steps(s)] for w, s in ser.items()}
    bodies, lights = [(c, w) for c, w, k in kinds if not k], [(c, w) for c, w, k in kinds if k]
    rows = [e for e in eras if "interval" in e]
    held = CAPTIONS.held_rows([header, *rows])[1]
    v = {e["interval"]: e["rows"][header["held"][0]]["velocity"] for e in rows}
    found = (header, rows, nodes, lines, shape, light, places, ser, spans, bodies, lights, rims)
    tops = [t for t, _v in CAPTIONS.tops_of(held)]
    return Record(*found, CAPTIONS.returns_of(held), tops, held[-1][0], v)


def read_record(folder: Path | str) -> Any:
    """The folder's one world's three logs read once (the folder holds one clicks log, or the unpacking refuses)."""
    (clicks,) = sorted(Path(folder).glob("*.clicks.jsonl"))
    world = clicks.with_name(clicks.name.removesuffix(".clicks.jsonl"))
    names = (world.with_suffix(".eras.jsonl"), world.with_suffix(".nodes.jsonl"))
    logs = [CAPTIONS.parse_log(name.read_text(encoding="utf-8")) for name in names]
    return record_of(logs[0][0], logs[0][1:], logs[1], READER.read_log(clicks))


def gate(name: str, passed: Any, numbers: dict[str, Any]) -> dict[str, Any]:
    """One gate's result: its name, the verdict (or verdicts by name) from the pass, the view, the reads and the lack from the gate's docstring, and the numbers."""
    two, (view, reads, lack) = isinstance(passed, dict), globals()[f"gate_{name}"].__doc__.split(" | ")
    word = {k: WORD[bool(p)] for k, p in passed.items()} if two else WORD[bool(passed)]
    missing = None if (all(passed.values()) if two else passed) else lack
    return dict(gate=name, verdict=word, view=view, reads=reads, numbers=numbers, missing=missing)


def pooled(spans: dict[Any, list[Any]], first: int, last: int) -> Any:
    """The pooled pace over every span within [first, last], the proper summed over the intervals summed, as a float."""
    rows = [(p * (b - a), b - a) for s in spans.values() for a, b, p in s if a >= first and b <= last]
    return float(Fraction(sum(p for p, _i in rows)) / sum(i for _p, i in rows)) if rows else None


def runs_of(intervals: list[int]) -> list[list[int]]:
    groups = (list(g) for _k, g in groupby(enumerate(intervals), key=lambda x: x[1] - x[0]))
    return [[g[0][1], g[-1][1]] for g in groups]


def length_of(rec: Any, by_interval: dict[int, Any], c: dict[str, Any], w: Any) -> Any:
    return READER.length_at(by_interval, c["interval"], READER.index_of(w, rec.shape))


def distance(a: Any, b: Any, shape: tuple[int, int, int]) -> int:
    return sum(abs(READER.shortest(x - y, n)) for x, y, n in zip(a, b, shape, strict=True))


def gate_recurring_bangs(rec: Any) -> dict:
    """board | the volume's returns and tops (the board's) and the births per cycle (the clicks); pass: more than one return and births in a later cycle | a birth after a return (the lay lock)"""
    births = [b["interval"] for b in rec.lines.births]
    born = [sum(1 for t in births if a <= t < z) for a, z in steps([*rec.returns, rec.last + 1])]
    passed = len(rec.returns) > 1 and all(n > 0 for n in born[1:])
    numbers = dict(returns=rec.returns, tops=rec.tops, births_per_cycle=born)
    return gate("recurring_bangs", passed, numbers)


def gate_links_lengthening(rec: Any) -> dict:
    """clicks | the Node's pace, delta proper over delta interval between its successive credits (the clicks), the mean length beside; pass: the pace falls at more Nodes than it rises, first span to last, and its slope over the run is negative | the pace falling at most Nodes"""
    ends = [(s[0][2], s[-1][2]) for s in rec.spans.values() if len(s) > 1]
    fell, rose = sum(1 for a, b in ends if b < a), sum(1 for a, b in ends if b > a)
    slope = READER.slope_of([(float(a + b) / 2, float(p)) for s in rec.spans.values() for a, b, p in s])
    lengths = [sum(n["length"]) / len(n["length"]) for n in (rec.nodes[0], rec.nodes[-1])]
    numbers = dict(nodes_pace_fell=fell, nodes_pace_rose=rose, nodes_pace_equal=len(ends) - fell - rose)
    numbers.update(pace_slope_per_interval=slope, mean_length_first_last=lengths)
    return gate("links_lengthening", fell > rose and slope is not None and slope < 0, numbers)


def gate_links_cycle(rec: Any) -> dict:
    """board | the mean length's monotone runs (the board's), the Nodes' pooled pace over the rise before, the fall and the rise after each top beside, which falls through the fall too (the contraction is the sum's); pass: a falling run between two rising runs | a falling run between rising runs"""
    means = [(n["interval"], sum(n["length"]) / len(n["length"])) for n in rec.nodes]
    signs = [(y[1] > x[1]) - (y[1] < x[1]) for x, y in steps(means)]
    groups = [(s, list(g)) for s, g in groupby(range(len(signs)), key=signs.__getitem__)]
    runs = [[s, *means[i[0]], *means[i[-1] + 1]] for s, i in groups]
    passed = any(a[0] > 0 > b[0] < c[0] for a, b, c in zip(runs, runs[1:], runs[2:], strict=False))
    tops = [(t, min(r for r in rec.returns if r > t)) for t in rec.tops if max(rec.returns) > t]
    bounds = {f"{t}-{b}": ((t - (b - t), t), (t, b), (b, b + (b - t))) for t, b in tops}
    clocks = {k: [pooled(rec.spans, a, z) for a, z in spans] for k, spans in bounds.items()}
    return gate("links_cycle", passed, dict(mean_length_runs=runs, nodes_pooled_pace_around=clocks))


def gate_era_of_matter(rec: Any) -> dict:
    """clicks | the credits by identity against light's (the clicks), the writes per family (the board's); pass: light's credits precede the bodies', the bodies' outnumber light's, and intervals exist where the points' write exceeds the massless write | the bodies' credits above light's after the births"""
    light, body = [c["interval"] for c, _w in rec.lights], [c["interval"] for c, _w in rec.bodies]
    row, seed = rec.header["held"][0], rec.header["seed"]
    writes = [(e["interval"], e["rows"][row]["writes"]) for e in rec.eras]
    above = [t for t, w in writes if sum(x for k, x in w.items() if k != seed) > abs(w.get(seed, 0))]
    passed = bool(light) and bool(body) and min(body) > min(light) and len(body) > len(light)
    numbers = dict(light_credits=len(light), light_span=light[:1] + light[-1:], body_credits=len(body))
    numbers.update(body_span=body[:1] + body[-1:], matter_above_light=len(above), runs=runs_of(above))
    return gate("era_of_matter", passed and bool(above), numbers)


def gate_acceleration(rec: Any) -> dict:
    """board | the velocity's differences per interval (the board's), the Nodes' pooled pace over thirds of a rise beside; pass: an interval with the velocity rising in every rise from a return | a rise with an accelerating interval"""
    diff = {b: rec.v[b] - rec.v[a] for a, b in steps(sorted(rec.v))}
    rises = [[r, min([t for t in rec.tops if t > r], default=rec.last)] for r in rec.returns]
    accelerating = [sum(1 for t in diff if a < t <= z and diff[t] > 0) for a, z in rises]
    third = [(a, (z - a) // 3) for a, z in rises[1:]]
    pace = {a: [pooled(rec.spans, a + i * s, a + i * s + s) for i in range(3)] for a, s in third}
    numbers = dict(rises=rises, accelerating_per_rise=accelerating, nodes_pace_over_thirds=pace)
    numbers.update(intervals_accelerating=sum(1 for t in diff if diff[t] > 0))
    return gate("acceleration", bool(rises) and all(n > 0 for n in accelerating), numbers)


def gate_contraction(rec: Any) -> dict:
    """board | the velocity below 0 (the board's), the Nodes' pooled pace within the run against the span before beside, not above it (the contraction is the sum's); pass: a run of velocity below 0 | a run of velocity below 0"""
    runs = runs_of([t for t in sorted(rec.v) if rec.v[t] < 0])
    clocks = {f"{a}-{z}": [pooled(rec.spans, a - (z - a), a), pooled(rec.spans, a, z)] for a, z in runs}
    numbers = dict(intervals_below_zero=sum(1 for t in rec.v if rec.v[t] < 0), runs=runs)
    return gate("contraction", bool(runs), {**numbers, "nodes_pace_before_within": clocks})


def gate_light(rec: Any) -> dict:
    """clicks | light's quanta per interval (the board's), the massless lays, every credit's absorbed family, light's beat against the length at its Node (the clicks); pass: quanta above 0 at every interval, lays at the births and at the bodies' closes, every credit absorbing light (present_absorbed), the beat's slope over the length negative (redshift) | a light click with a beat after the births, the beat lower where the Link is longer"""
    seed, credits = rec.header["seed"], rec.lines.credits
    quanta = [e["quanta"][seed]["quanta"] for e in rec.eras]
    birth, body = {b["interval"] for b in rec.lines.births}, {c["interval"] for c, _w in rec.bodies}
    lays = [lay["interval"] for lay in rec.lines.lays if lay.get("family") == seed]
    at_births, at_closes = sum(t in birth for t in lays), sum(t in body - birth for t in lays)
    absorbing = sum(1 for c in credits if c.get("absorbed") == seed)
    beats = [(length_of(rec, READER.by_interval_of(rec.nodes), c, w), c["beat"]) for c, w in rec.lights]
    slope = READER.slope_of([(x, y) for x, y in beats if x is not None and y])
    present = min(quanta, default=0) > 0 and min(at_births, at_closes) > 0 and absorbing == len(credits)
    numbers = dict(intervals_with_light=[sum(q > 0 for q in quanta), len(quanta)], light_lays=len(lays))
    numbers.update(quanta_least_most=[min(quanta), max(quanta)] if quanta else None)
    numbers.update(lays_at_births=at_births, lays_at_body_closes=at_closes, beat_slope=slope)
    numbers.update(credits_absorbing_light=[absorbing, len(credits)], light_credits=len(beats))
    numbers.update(light_credits_with_beat=sum(1 for _x, y in beats if y))
    numbers.update(light_last_interval=max((c["interval"] for c, _w in rec.lights), default=None))
    return gate("light", dict(present_absorbed=present, redshift=bool(slope) and slope < 0), numbers)


def gate_families_forming(rec: Any) -> dict:
    """clicks | the births' children, points and senses, the credits' identity recurring (the clicks), the rest from the credits' point unread (the decoder's pair of pairs); pass: two or more points recur, every birth's senses sum to 0, every born identity is credited more than once | two points recurring, the senses summing to 0, every identity recurring"""
    names = CAPTIONS.captions_for(rec.header)
    per_point = Counter(child for b in rec.lines.births for child in set(b["children"]))
    sums = [sum(b["senses"]) for b in rec.lines.births]
    tracks = {str(list(k)): len(v) for k, v in rec.rims.items()}
    passed = len(per_point) > 1 and bool(sums) and all(s == 0 for s in sums) and bool(tracks)
    numbers = dict(births_per_point={CAPTIONS.shown(p, names): n for p, n in per_point.items()})
    numbers.update(births=len(sums), births_summing_to_zero=sums.count(0), closes_per_identity=tracks)
    return gate("families_forming", passed and all(n > 1 for n in tracks.values()), numbers)


def gate_collisions(rec: Any) -> dict:
    """clicks | the credits' rims per close, the least torus distance between two rims at their shared closes, the conversion lines (the clicks); pass: a conversion line, or two bodies each at one Node per close whose distance falls then rises | a position per close (the decoder); a body at one place (the physics)"""
    converted = sum(1 for c in rec.lines.credits if (c.get("kept"), c.get("left")) != (None, None))
    rim, pairs, met = rec.rims, {}, False
    counts = {str(list(k)): sorted(len(s) for s in v.values()) for k, v in rim.items()}
    sizes = {k: [n[0], n[-1]] for k, n in counts.items()}
    for a, b in combinations(sorted(rim), 2):
        shared = sorted(set(rim[a]) & set(rim[b]))
        least = [min(distance(x, y, rec.shape) for x in rim[a][t] for y in rim[b][t]) for t in shared]
        one = [d for t, d in zip(shared, least, strict=True) if len(rim[a][t]) == len(rim[b][t]) == 1]
        fell = [i for i, (x, y) in enumerate(steps(one)) if y < x]
        met = met or (bool(fell) and any(y > x for x, y in steps(one)[fell[0] :]))
        pairs[f"{list(a)} x {list(b)}"] = dict(shared_closes=len(shared), one_node_closes=len(one))
        pairs[f"{list(a)} x {list(b)}"]["least_distance"] = [min(least), max(least)] if least else None
    numbers = dict(conversion_lines=converted, rim_nodes_per_close_min_max=sizes, pairs=pairs)
    return gate("collisions", converted > 0 or met, numbers)


def gate_gravitational_time_dilation(rec: Any) -> dict:
    """clicks | two Nodes' proper increments between shared closes, the deeper by births as matter (the clicks); pass: among pairs with one birthed Node, the birthed one counts fewer proper intervals more often than not | the birthed Node slower more often than not"""
    birthed = {READER.as_node(n) for b in rec.lines.births for n in b.get("nodes") or []}
    clocks = {w: dict(s) for w, s in rec.clocks.items()}
    unequal, one_birthed, birthed_slow = 0, 0, 0
    for a, b in combinations(sorted(clocks), 2):
        shared = clocks[a].keys() & clocks[b].keys()
        if len(shared) < 2:
            continue
        f, z = min(shared), max(shared)
        da, db = clocks[a][z] - clocks[a][f], clocks[b][z] - clocks[b][f]
        if da == db:
            continue
        slow, fast = (a, b) if da < db else (b, a)
        unequal, one_birthed = unequal + 1, one_birthed + ((slow in birthed) != (fast in birthed))
        birthed_slow += (slow in birthed) and (fast not in birthed)
    numbers = dict(node_pairs_unequal_proper=unequal, pairs_one_birthed=one_birthed)
    numbers.update(birthed_slower=birthed_slow, other_slower=one_birthed - birthed_slow)
    return gate("gravitational_time_dilation", birthed_slow > one_birthed - birthed_slow, numbers)


def gate_gravitational_redshift(rec: Any) -> dict:
    """clicks | light's beat at two Nodes at one interval (the clicks), the length at each beside; pass: a pair of beats at two lengths with the beat lower where longer | two beats of light at two lengths at one interval, lower where longer"""
    by_t, readings = READER.by_interval_of(rec.nodes), defaultdict(list)
    for c, w in rec.lights:
        if c.get("beat"):
            readings[c["interval"]].append((length_of(rec, by_t, c, w), c["beat"]))
    pairs = [(xa, ba, xb, bb) for r in readings.values() for (xa, ba), (xb, bb) in combinations(r, 2)]
    pairs = [p for p in pairs if None not in p[::2] and p[0] != p[2] and p[1] != p[3]]
    ordered = sum(1 for xa, ba, xb, bb in pairs if (xa > xb) == (ba < bb))
    numbers = dict(beats_per_interval={t: len({b for _x, b in r}) for t, r in sorted(readings.items())})
    numbers.update(pairs_at_two_lengths_two_beats=len(pairs), beat_lower_where_longer=ordered)
    return gate("gravitational_redshift", ordered > 0, numbers)


def gate_light_path(rec: Any) -> dict:
    """clicks | light's identity across Nodes (the clicks); pass: more than one light identity, one credited at two Nodes | light's identity per quantum: every light credit carries the family's identity at its birth Node"""
    ids = {READER.identity_of(c) for c, _w in rec.lights}
    nodes = {i: {w for c, w in rec.lights if READER.identity_of(c) == i} for i in ids}
    passed = len(nodes) > 1 and any(len(v) > 1 for v in nodes.values())
    numbers = dict(light_credits=len(rec.lights), distinct_light_identities=len(nodes))
    return gate("light_path", passed, {**numbers, "nodes_credited": len(set().union(*nodes.values()))})


def gate_free_fall(rec: Any) -> dict:
    """clicks | a body's one-Node closes against matter's seat (the Node with most body credits), the distance's second differences (the clicks); pass: a track with negative second differences and no positive one | a position per close; a body at one place"""
    seat = Counter(w for _c, w in rec.bodies).most_common(1)
    rows, passed = {}, False
    for ident, closes in rec.rims.items():
        one = [next(iter(s)) for _t, s in sorted(closes.items()) if len(s) == 1]
        d = [distance(w, seat[0][0], rec.shape) for w in one] if seat else []
        second = [b - a for a, b in steps([b - a for a, b in steps(d)])]
        signs = [sum(1 for x in second if x < 0), sum(1 for x in second if x > 0)]
        passed = passed or (signs[0] > 0 and signs[1] == 0)
        rows[str(list(ident))] = dict(closes=len(closes), one_node_closes=len(one), second_signs=signs)
    numbers = dict(seat_of_matter=[list(seat[0][0]), seat[0][1]] if seat else None, tracks=rows)
    return gate("free_fall", passed, numbers)


def gate_horizon(rec: Any) -> dict:
    """board | the Links at the wall (the board's), the wall Nodes' credits, silences and pooled pace (the clicks); pass: Links at the wall and a wall Node with no credit through a wall run while other Nodes are credited (links_and_silence), the wall Nodes' pooled pace below the others' within a hole (stopped_clock) | a wall Node's clock slower than the others' (a credit behind the wall)"""
    at_wall: dict[Any, set[int]] = defaultdict(set)
    where = {READER.index_of(w, rec.shape): w for w in rec.clocks}
    for n in rec.nodes:
        for index in (i for link in n.get("horizon") or [] for i in link):
            at_wall[where.get(index, index)].add(n["interval"])
    holes = CAPTIONS.spans_of([(n["interval"], len(n.get("horizon") or [])) for n in rec.nodes])
    credited, silent, paced = sorted({t for s in rec.clocks.values() for t, _p in s}), [], {}
    for node, ts in at_wall.items():
        own = [t for t, _p in rec.clocks.get(node, [])]
        for first, last in runs_of(sorted(ts)):
            if any(first <= t <= last for t in credited) and not any(first <= t <= last for t in own):
                before = max((t for t in own if t < first), default=None)
                silent.append(dict(node=list(node), wall_run=[first, last], last_credit_before=before))
    for first, last, most in holes:
        wall = {n for n, ts in at_wall.items() if any(first <= t <= last for t in ts)}
        at = pooled({n: rec.spans.get(n, []) for n in wall}, first, last)
        off = pooled({n: s for n, s in rec.spans.items() if n not in wall}, first, last)
        paced[f"{first}-{last}"] = dict(links_most=most, wall_nodes=len(wall), pace_wall_off=[at, off])
    slow = [p["pace_wall_off"] for p in paced.values() if None not in p["pace_wall_off"]]
    numbers = dict(holes=paced, wall_nodes=len(at_wall), silent_wall_runs=silent)
    passed = dict(links_and_silence=bool(holes and silent), stopped_clock=any(a < o for a, o in slow))
    return gate("horizon", passed, numbers)


def gate_conservation(rec: Any) -> dict:
    """clicks | every line's taken, walls and excess (the clicks); pass: taken equals walls plus excess on every line (identity), the excess 0 on every line (exact) | the exact take: the excess above 0 (the take in w-ths)"""
    rows = [r for r in [*rec.lines.births, *rec.lines.credits] if r.get("taken") is not None]
    identity = sum(1 for r in rows if r["taken"] == r["walls"] + r["excess"])
    exact = sum(1 for r in rows if r["excess"] == 0)
    shares = [Fraction(r["excess"], r["taken"]) for r in rows if r["taken"]]
    passed = dict(identity=bool(rows) and identity == len(rows), exact=bool(rows) and exact == len(rows))
    numbers = dict(lines=len(rows), identity_holds=identity, excess_zero=exact)
    numbers.update(excess_over_taken=[float(min(shares)), float(max(shares))] if shares else None)
    return gate("conservation", passed, numbers)


def gate_uncertainty(rec: Any) -> dict:
    """clicks | the proper spacing of one record at one Node and the point's sine with the count (the clicks); pass: every row readable and (count sin omega Delta t)^2 at or above 1/4 in T's unit | the body credit's point decoded (a pair of pairs) and the proper's fraction"""
    per: dict[Any, list[dict[str, Any]]] = defaultdict(list)
    for c, w in zip(rec.lines.credits, rec.places, strict=True):
        per[(READER.identity_of(c), w)].append(c)
    pairs = [(a, b) for cs in per.values() for a, b in steps(sorted(cs, key=READER.interval_of))]
    rows = [(b["proper"] - a["proper"], READER.pair_of(b.get("point")), b["count"]) for a, b in pairs]
    read = [(dt, Fraction(*p), n) for dt, p, n in rows if p is not None and p[1] and abs(p[0]) <= p[1]]
    products = [n * n * (1 - cosine * cosine) * dt * dt for dt, cosine, n in read]
    floor, least = READER.HALF * READER.HALF, min(products, default=None)
    unread = sum(1 for _d, p, _n in rows if p is None)
    passed = bool(rows) and len(read) == len(rows) and least is not None and least >= floor
    numbers = dict(rows=len(rows), proper_spacing_zero=sum(1 for dt, _p, _n in rows if dt == 0))
    numbers.update(point_readable=len(read), point_pair_of_pairs=unread, floor_squared=float(floor))
    numbers.update(point_outside_circle=len(rows) - len(read) - unread)
    numbers.update(least_squared_product_in_t_units=None if least is None else float(least))
    return gate("uncertainty", passed, numbers)


def gate_charge_conservation(rec: Any) -> dict:
    """clicks | the births' senses, the credits' sense per close, the Wronskian's sign at the credited Node and not the record's charge (the clicks), the sign holder's quanta (the board's); pass: every birth's senses sum to 0 | every birth's senses summing to 0"""
    sums = [sum(b["senses"]) for b in rec.lines.births]
    per_close: dict[int, int] = defaultdict(int)
    for c in rec.lines.credits:
        per_close[c["interval"]] += c["sense"]
    holders = CAPTIONS.families_of([rec.header, *rec.eras])[1]
    holder = [e["quanta"][holders[0]]["quanta"] for e in rec.eras] if holders else []
    numbers = dict(births=len(sums), births_summing_to_zero=sums.count(0), closes=len(per_close))
    numbers.update(closes_senses_zero=sum(1 for x in per_close.values() if x == 0))
    numbers.update(sign_holder_quanta=[holder[0], holder[-1], max(holder)] if holder else None)
    return gate("charge_conservation", bool(sums) and all(s == 0 for s in sums), numbers)


def gate_arrow_of_time(rec: Any) -> dict:
    """clicks | the proper's monotonicity at every Node (the clicks), the turns (the board's), the run back across a return being the engine's test (tools/back_in_time.py --from K); pass: no proper runs back while turns exist | no proper running back while turns exist"""
    back = sum(1 for s in rec.clocks.values() for (_a, pa), (_b, pb) in steps(s) if pb < pa)
    turned, end = [n.get("turned") or [] for n in rec.nodes], rec.nodes[-1]["direction"]
    turns = sum(len(t) for t in turned)
    numbers = dict(nodes=len(rec.clocks), proper_back=back, turns=turns)
    numbers.update(turn_intervals=sum(map(bool, turned)), turned_at_end=end.count(-1))
    return gate("arrow_of_time", bool(rec.clocks) and back == 0 and turns > 0, numbers)


def gate_mass_ratios(rec: Any) -> dict:
    """clicks | the births' points' legs with the legend's names, a fit by den's choice, the body credits' point per track (the clicks); pass: the legs distinct and ordered electron, proton, neutron (fit), one readable pair per track (from_clicks) | the rest from the clicks: the body credit's point decoded"""
    names, legs = CAPTIONS.captions_for(rec.header), {}
    for b in rec.lines.births:
        for child, (num, den) in zip(b["children"], b["points"], strict=True):
            legs[names.get(child, child)] = READER.leg_below(den * den - num * num)
    e, p, n = (legs.get(k) for k in ("electron", "proton", "neutron"))
    fit = None not in (e, p, n) and e < p < n
    over = zip(RATIOS, (p, n, n), (e, e, p), strict=True)
    ratios = {k: float(Fraction(x, y)) for k, x, y in over} if fit else None
    points = [(READER.identity_of(c), READER.pair_of(c.get("point"))) for c, _w in rec.bodies]
    pairs = {i: {q for j, q in points if j == i and q is not None} for i in {i for i, _q in points}}
    unread = sum(1 for _i, pair in points if pair is None)
    from_clicks = unread == 0 and bool(pairs) and all(len(v) == 1 for v in pairs.values())
    numbers = dict(legs={k: str(v) for k, v in legs.items()}, ratios_from_the_legs=ratios)
    numbers.update(point_pair_of_pairs=unread, point_single_pair=len(points) - unread)
    numbers.update(distinct_pairs_per_identity={str(list(k)): len(v) for k, v in pairs.items()})
    return gate("mass_ratios", dict(fit=fit, from_clicks=from_clicks), numbers)


GATES = tuple((n.removeprefix("gate_"), f) for n, f in list(globals().items()) if n.startswith("gate_"))


def gates(rec: Any) -> list[dict[str, Any]]:
    return [function(rec) for _name, function in GATES]


def verdicts(results: list[dict[str, Any]]) -> dict[str, str]:
    """The verdicts by name, a two-verdict gate's as `gate.name`."""
    found: dict[str, str] = {}
    for r in results:
        words = r["verdict"] if isinstance(r["verdict"], dict) else {"": r["verdict"]}
        found.update({f"{r['gate']}.{k}" if k else r["gate"]: word for k, word in words.items()})
    return found


def summary(results: list[dict[str, Any]]) -> str:
    """One line per gate, its verdicts by name with the view and the numbers, and the count shown of the total last."""
    found, lines = verdicts(results), []
    for r in results:
        heads = "; ".join(f"{v} {k}" for k, v in verdicts([r]).items())
        lines.append(f"{heads} ({r['view']}): {json.dumps(r['numbers'], default=str)}")
    return "\n".join([*lines, f"{sum(1 for v in found.values() if v == SHOWN)} of {len(found)} shown"])


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("folder", type=Path, help="the folder holding the one world's three logs")
    parser.add_argument("--out", type=Path, default=None, help="the results as JSON (none: the summary)")
    args = parser.parse_args(argv)
    results = gates(read_record(args.folder))
    if args.out is not None:
        text = json.dumps({"verdicts": verdicts(results), "gates": results}, indent=1, default=str)
        args.out.write_text(text + "\n", encoding="utf-8")
    print(summary(results))


if __name__ == "__main__":
    main()
