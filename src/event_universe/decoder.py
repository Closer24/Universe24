"""The decoder of the record, integers only (the owner's word: no float anywhere, every reading a quotient with its remainder or a count over a span): it reads the run's log alone (credits, births, refusals; the rows of the board's course), holds den's circle and its own names for the planes (never the Node's), and gives every gate of UNIVERSE24 a verdict with its numbers; two views, the whole view (every click on the board) and the one-place view (a body found from its clicks alone at one Node); the gates themselves are gates.py."""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import cmp_to_key
from typing import Any

from event_universe.core import paces, rule3
from event_universe.core.paces import sine_den
from event_universe.rows import PLANE

MIL = 1000000  # readings in parts per million
HUNDRED = 100  # readings in hundredths
THOUSAND = 1000  # readings in thousandths
WIDTH = 128  # the law's width: every integer of the state and of every transient within it
FEW = 10  # the fewest decoded credits for the dilation's two halves
SPANS = 20  # the fewest spans for the lengthening's two halves
Rational = tuple[int, int]


class Record:
    """The record as the decoder reads it: the two files' integers, the planes with a gap by their legs under the decoder's names, the log's credits and births, the rows of the board's course."""

    def __init__(self, run: dict[str, Any]) -> None:
        self.run = run
        self.den = int(run["den"])
        self.gamma, self.G, self.T = int(run["gamma"]), int(run["G"]), int(run["T"])
        rows = run["universe"]["rows"]
        planes = [
            tuple(int(x) for x in r["pair"]) for r in rows if int(r["shape"]) == PLANE and r.get("pair")
        ]
        gapped = sorted((sine_den(num, self.den), num) for num, den in planes if num != den)
        self.NL = len(gapped)
        self.NAMES: dict[int, tuple[str, int]] = {
            num: (f"gapped {k}", leg) for k, (leg, num) in enumerate(gapped)
        }
        self.NAMES[self.den] = ("gap 0", 0)
        self.line_num = [int(num) for num in run["planes"]]
        self.log = run["log"]
        self.credits = [entry for entry in self.log if entry["event"] == "credit"]
        self.births = [entry for entry in self.log if entry["event"] == "birth"]
        self.rows = run["rows"]
        self.w = rule3.wall_of(self.den, self.gamma, self.G)

    def through(self, k: int) -> Record:
        """The record with its credits cut to the first k, for a gate read as it first shows."""
        found = Record.__new__(Record)
        found.__dict__.update(self.__dict__)
        found.credits = sorted(self.credits, key=lambda c: int(c["i"]))[:k]
        return found


def quot(a: int, b: int, scale: int = 1) -> int | None:
    """The integer reading of a / b: the quotient of the scaled numerator (the remainder dropped)."""
    return None if b == 0 else (a * scale) // b


def cmp_rat(p: Rational, q: Rational) -> int:
    """Order two rationals (n, d) with d > 0 by cross multiplication."""
    s = p[0] * q[1] - q[0] * p[1]
    return (s > 0) - (s < 0)


def turned(a: Rational, m: Rational, over: int) -> Rational:
    """A complex pair turned by the pair (c, s) over the scale, one half-up rounding per part."""
    c, s = a
    return (2 * (c * m[0] - s * m[1]) + over) // (2 * over), (2 * (s * m[0] + c * m[1]) + over) // (
        2 * over
    )


def solve(record: Record, credit: dict[str, Any]) -> Rational | None:
    """The species from the frame in exact integers: the same turned arrivals the Node formed (the phase pair over X and the odd tangent, half-up divisions), Rule3's line solved for x = num / den; the rational (N, D) with D > 0."""
    f, content = credit["frame"], credit["content"]
    gamma, den, unit = record.gamma, record.den, record.G
    p0, pi = paces.clock(gamma, content), paces.link_pace(gamma, content)
    w = rule3.wall_of(den, gamma, unit)
    mass = 12 * den * p0 * p0 * unit * unit
    zb = (f["re_start_before"], f["im_start_before"])
    zn = (f["re_start_now"], f["im_start_now"])
    zx = (f["re_stepped"], f["im_stepped"])
    if zn == (0, 0):
        return None
    scale, phases, odd, frames = f["X"], f["phases"], f["odd"], f["frames"]
    wl = 4 * gamma
    numer = (
        w * (zx[0] + zb[0] - 2 * zn[0]) + mass * zn[0],
        w * (zx[1] + zb[1] - 2 * zn[1]) + mass * zn[1],
    )
    denom = (mass * zn[0], mass * zn[1])
    for port, (a, b) in enumerate(zip(f["re_neighbours_start"], f["im_neighbours_start"], strict=True)):
        m: Rational = (a, frames[port] * b)
        m = turned(tuple(phases[port]), m, scale)
        n = odd[port]
        m = turned((wl * wl - n * n, 2 * wl * n), m, wl * wl + n * n)
        reach = 2 * den * pi * pi * f["factors"][port]
        denom = (denom[0] - reach * (zn[0] - m[0]), denom[1] - reach * (zn[1] - m[1]))
    dd = denom[0] * denom[0] + denom[1] * denom[1]
    if dd == 0:
        return None
    return (numer[0] * denom[0] + numer[1] * denom[1], dd)


def nearest(record: Record, x: Rational) -> str:
    """The name whose num / den lies nearest the rational x = (N, D): the smallest |N den - num D|, all integers."""
    n, d = x
    return min(record.NAMES.items(), key=lambda kv: abs(n * record.den - kv[0] * d))[1][0]


def middle(xs: list[Rational]) -> Rational:
    """The middle of sorted rationals, the mean of the two middle ones at an even count."""
    k = len(xs)
    if k % 2:
        return xs[k // 2]
    p, q = xs[k // 2 - 1], xs[k // 2]
    return (p[0] * q[1] + q[0] * p[1], 2 * p[1] * q[1])


def decoded_credits(
    record: Record,
) -> tuple[list[tuple[dict[str, Any], str, Rational]], int, int, list[int | None]]:
    """Every credit's species solved from its frame: the decoded (credit, name, x), the count read right, the count within the one-click floor, and each credit's floor on x in parts per million."""
    den, names, line_num = record.den, record.NAMES, record.line_num
    decoded = []
    right = within = 0
    floors: list[int | None] = []
    for c in sorted(record.credits, key=lambda c: int(c["i"])):
        x = solve(record, c)
        if x is None:
            continue
        name = nearest(record, x)
        right += name == names[line_num[c["line"]]][0]
        decoded.append((c, name, x))
        n, d = x
        num = line_num[c["line"]]
        within += (n * den - num * d) ** 2 <= 2 * (record.w * den) ** 2 * d
        floors.append(
            rule3.largest_below((2 * record.w * record.w * den * den * MIL * MIL) // (d * num * num))
            if num
            else None
        )
    return decoded, right, within, floors


def species(record: Record) -> tuple[dict[str, Any], list[tuple[dict[str, Any], str, Rational]]]:
    """Gates 8, 8b, 19 and 16: the species from the frame of every credit (the whole view) and over a body's track (the one-place view: the middle solve), the mass ratios from den's legs, the one-click floor."""
    out: dict[str, Any] = {}
    names, line_num = record.NAMES, record.line_num
    decoded, right, within, floor_mil = decoded_credits(record)
    tracks: dict[tuple[Any, int], list[Rational]] = defaultdict(list)
    confusion: Counter[tuple[str, str]] = Counter()
    for c, name, x in decoded:
        tracks[(tuple(c["node"]), c["line"])].append(x)
        confusion[(names[line_num[c["line"]]][0], name)] += 1
    track_right = 0
    for (_node, line), xs in tracks.items():
        xs.sort(key=cmp_to_key(cmp_rat))
        track_right += nearest(record, middle(xs)) == names[line_num[line]][0]
    born = Counter(names[line_num[b["line_pair"]]][0] for b in record.births)
    out["8b species over the track (one-place view: the middle solve of the body's track)"] = {
        "tracks": len(tracks),
        "decoded right": track_right,
        "confusion (truth->decoded) per credit": {
            f"{a}->{b}": n for (a, b), n in confusion.items() if a != b
        },
    }
    if within == len(decoded) and track_right == len(tracks) and len(born) >= 3:
        verdict = "SHOWN (every credit within the one-click floor, every track read right)"
    elif within == len(decoded):
        verdict = (
            f"SHOWN in part: every credit within the floor, tracks right {track_right} of {len(tracks)}"
        )
    else:
        verdict = f"NOT SHOWN: {len(decoded) - within} credits beyond the floor"
    out["8 families forming (whole view)"] = {
        "credits": len(record.credits),
        "species readable": len(decoded),
        "decoded right per credit": right,
        "credits within the one-click floor": within,
        "tracks right": [track_right, len(tracks)],
        "births by species (decoder)": dict(born),
        "verdict": verdict,
    }
    return out | ratios(record, floor_mil, within, len(decoded)), decoded


def ratios(record: Record, floor_mil: list[int | None], within: int, decoded: int) -> dict[str, Any]:
    """Gates 19 and 16: the mass ratios from den's legs (the planes with a gap against the lightest) and the one-click floor on x per credit."""
    names = record.NAMES
    legs = sorted(((name, leg) for name, leg in names.values() if leg), key=lambda kv: kv[1])
    num_of = {v[0]: k for k, v in names.items()}
    found: dict[str, Any] = {f"{nm}/{legs[0][0]}": quot(leg, legs[0][1], MIL) for nm, leg in legs[1:]}
    out = {
        "19 mass ratios (parts per million)": found
        | {"verdict": "SHOWN as a fit of den (the legs), read from the decoded points"}
    }
    fl = sorted(f for f in floor_mil if f is not None)
    if fl:
        spacing = (
            quot(abs(num_of[legs[-1][0]] - num_of[legs[-2][0]]), num_of[legs[-1][0]], MIL)
            if record.NL >= 2
            else None
        )
        out["16 uncertainty floor (one click)"] = {
            "floor on x per credit, parts per million: min / middle / max": [
                fl[0],
                fl[len(fl) // 2],
                fl[-1],
            ],
            "species spacing of the two heaviest, parts per million": spacing,
            "credits beyond the floor": decoded - within,
            "verdict": "SHOWN as the law's floor: no credit reads beyond it"
            if within == decoded
            else "NOT SHOWN",
        }
    return out


def charge_and_take(record: Record) -> tuple[dict[str, Any], int, int, int]:
    """Gates 17 and 15: the charge (each child's sense the sign of its own Wronskian at its Node, summed over the births) and the conservation at the click (taken against booked)."""
    births = record.births
    signs = [(w > 0) - (w < 0) for b in births for w in b["W_children"]]
    sense_sum = sum(signs)
    opposite = sum(
        1
        for b in births
        if (b["W_children"][0] > 0) != (b["W_children"][1] > 0) and 0 not in b["W_children"]
    )
    out = {
        "17 charge conservation": {
            "senses sum over births (from the children's Wronskian signs)": sense_sum,
            "children with W = 0": signs.count(0),
            "births with the two children at opposite signs": opposite,
            "verdict": "SHOWN" if sense_sum == 0 and 0 not in signs else "NOT SHOWN",
        }
    }
    booked, taken = sum(b["booked"] for b in births), sum(b["taken"] for b in births)
    exact = all(b["taken"] >= b["booked"] for b in births)
    out["15 conservation at the click"] = {
        "births": len(births),
        "taken per booked at the births (hundredths)": quot(taken, booked, HUNDRED),
        "verdict": "SHOWN as the identity taken >= booked on every birth; NOT SHOWN exact (the excess below one level of light)"
        if exact
        else "NOT SHOWN",
    }
    return out, sense_sum, taken, booked
