"""The reading's event lines, the rows' names, the rows that are words alone and the eras in the clicks' view: the event lines (the owner's words of 2026-10-25: the record tells what it sees as it sees it; every gate has a label when it happens): one line per row of the table at the interval it first shows, found by reading the row on the record cut to each interval (a search on the cuts, the verdict read as standing from its first interval on), with its Node where the row names one (`at`) and its label in the gate's own words of three to six and its phenomenon in plain words (NAMES, the one table of the rows' names), for the page's labels and the bar's ticks; every line read from the record alone."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from event_universe.decoder import HALF, LISTED, PAIR, Record, quot, shown
from event_universe.predicates import unread
from event_universe.rows import QUARTET

NAMES = {
    "1": ("a bang recurs", "the recurring bang"),
    "1b": ("the board tops, every Node turns", "the board topping, every Node turning at once"),
    "1c": ("the board returns to Gamma", "the board returning to Gamma"),
    "2": ("the Links lengthen", "the lengthening of the Links"),
    "3": ("the board shortens then lengthens", "the Links shortening, then lengthening"),
    "4": ("the era of matter", "the era of matter"),
    "5": ("the lengthening quickens", "the acceleration of the expansion"),
    "6": ("the board contracts", "the contraction"),
    "7": ("light absorbed at a take", "light present and absorbed"),
    "8": ("a body clicks", "the families forming"),
    "8b": ("a track read right", "the species over a body's track"),
    "9": ("two bodies meet", "the collision of two bodies"),
    "10": ("the clocks run slow", "gravitational time dilation"),
    "11": ("light redder where deeper", "gravitational redshift"),
    "12": ("light delayed or bent", "the delay and the bending of light"),
    "13": ("the fall quickens", "free fall"),
    "14": ("the horizon", "the horizon, a black hole"),
    "15": ("the take pays the walls", "conservation at the click"),
    "16": ("the floor holds", "the uncertainty floor"),
    "17": ("a pair born", "charge conservation"),
    "18": ("the run back exact", "the arrow of time and its reversal"),
    "19": ("the mass ratio read", "the mass ratios"),
    "20": ("the twist's 24 and 24", "the twist, P and C violated, CP kept"),
    "21": ("births of both hands", "the handedness of the birth"),
    "22": ("unlike attract, like repel", "Coulomb's sign"),
    "23": ("the recoil passed", "the momentum across the click"),
    "24": ("a pair into light", "the merger of a pair into light"),
    "25": ("the entropy rises", "the entropy rising"),
    "26": ("three lifts, the beats ordered", "the three lifts and their masses"),
    "27": ("no third alone", "confinement, no third alone"),
    "28": ("a conversion", "the neutron's conversion"),
    "29": ("light's period longer where deeper", "the redshift of light"),
    "30": ("the deeper clock slower", "the dilation of a body's clock"),
    "31": ("light's track bent or late", "the deflection and the Shapiro delay"),
    "32": ("the perihelion advances", "the perihelion's advance"),
    "33": ("the body falls by its tail", "free fall by the tail"),
    "34": ("the clock stops at the horizon", "the stopped clock at the horizon"),
    "35": ("matter dragged, light not", "frame dragging"),
    "36": ("a shear wave travels", "gravitational waves, the shears"),
    "37": ("one Link per interval", "Maxwell's one Link per interval"),
    "38": ("the phase shifted by the flux", "the Aharonov-Bohm phase"),
    "39": ("the beat shifted in the field", "the Zeeman and Stark shifts"),
    "40": ("one quantum one click", "the photoelectric click"),
    "41": ("the spinor's two beats", "the spinor's two beats"),
    "42": ("the split along the gradient", "Stern-Gerlach, the split along the gradient"),
    "43": ("the exclusion holds", "the exclusion"),
    "44": ("the packet at its velocity", "the moving packet's velocity"),
    "45": ("a body stands in its well", "the bound body in its well"),
    "46": ("the bang recurs with its gates", "the bang recurring with its gates"),
    "47": ("the take exact", "the exact take"),
    "48": ("a black body spectrum", "the black body"),
    "49": ("the clicks decay geometrically", "the exponential decay"),
    "50": ("light couples to light", "light on light"),
    "51": ("the Casimir force", "the Casimir force and the running alpha"),
    "52": ("a third child", "the neutrino"),
    "53": ("a fast packet binds", "a fast packet binding"),
    "54": ("two packets scatter", "scattering, two packets through each other"),
    "55": ("the two slits", "the two slits"),
    "56": ("Bell's bound holds", "Bell's correlation"),
    "57": ("the GHZ gate", "the GHZ correlation"),
    "58": ("the fast expansion", "the fast expansion after the bang, in the clicks"),
    "59": ("the expansion slows", "the deceleration, in the clicks"),
    "60": ("the expansion quickens again", "the acceleration, in the clicks"),
    "61": ("the horizon radiates", "the horizon radiating, Hawking's radiation in the clicks"),
    "the conservations in the clicks": ("the clicks conserve", "the conservations in the clicks"),
    "the three constants": ("the three constants hold", "the three constants"),
}  # every row by its number (the key's first word) or its key: its label of three to six words for the page, and the phenomenon in plain words for the table


def names_of(key: str) -> tuple[str, str]:
    """A row's label and phenomenon from its key: by the row's number (the key's first word) or by the key itself."""
    return NAMES.get(key.split()[0], NAMES.get(key, (key, key)))


def label_of(key: str) -> str:
    """The label of a row, its words of three to six."""
    return names_of(key)[0]


def phenomenon_of(key: str) -> str:
    """The phenomenon of a row in plain words, the first column of the gates of the phenomena."""
    return names_of(key)[1]


def eras_of(out: dict[str, Any], intervals: int) -> dict[str, Any]:
    """The eras row from the rows already read: the bangs (the seed's and one after every exact return of row 1c), the tops of row 1b, and the spans from each bang, from the era of matter (4), the acceleration (5) and the bang recurring (46) at the interval each first shows, each span to the next's start."""
    rows = {k.split()[0]: v for k, v in out.items() if isinstance(v, dict)}
    tops: list[int] = next((v for n, v in rows.get("1b", {}).items() if n.startswith("tops")), [])
    returns: list[int] = next(
        (v for n, v in rows.get("1c", {}).items() if n.startswith("exact returns")), []
    )
    bangs = [1] + [int(i) + 1 for i in returns]
    starts = [(b, "1", label_of("1")) for b in bangs] + [
        (e["i"], e["gate"].split()[0], e["label"])
        for e in out["events"]
        if e["i"] is not None and e["gate"].split()[0] in ("4", "5", "46")
    ]
    starts.sort(key=lambda s: (s[0], s[1]))
    spans = [
        [i, starts[k + 1][0] if k + 1 < len(starts) else intervals + 1, g, label]
        for k, (i, g, label) in enumerate(starts)
    ]
    return {
        "bangs": bangs,
        "tops": [int(i) for i in tops],
        "spans (from, to, the gate, its label)": spans,
    }


def first_interval(record: Record, row: Callable[[Record], dict[str, Any]], key: str) -> int:
    """The least interval at which the row shows on the record cut to it, by a search on the cuts (the verdict read as standing from its first interval on)."""
    low, high = 1, record.intervals
    while low < high:
        mid = (low + high) // HALF
        if shown(row(record.to(mid))[key]["verdict"]):
            high = mid
        else:
            low = mid + 1
    return low


def first_shown(
    record: Record, read: list[tuple[Callable[[Record], dict[str, Any]], dict[str, Any]]]
) -> list[dict[str, Any]]:
    """Every event line in the order of its interval: for every row of the table that shows on the whole record (the rows as read once, each with its reading), the interval it first shows, its Node where the row names one, its label and its verdict's first clause as its numbers."""
    found = []
    for row, rows in read:
        for key, out in rows.items():
            if not shown(out["verdict"]):
                continue
            i = first_interval(record, row, key)
            at = row(record.to(i))[key].get("at")
            found.append(
                {
                    "gate": key,
                    "label": label_of(key),
                    "i": i,
                    "node": None if at is None else list(at),
                    "numbers": out["verdict"].split(";")[0].split(" (")[0],
                }
            )
    return sorted(found, key=lambda e: (int(e["i"]), e["gate"]))


def wave_lay(record: Record) -> bool:
    """Whether the world lays a packet with a wave number (the `wave` key of an `at` lay, MV-S1)."""
    return any("wave" in lay for lay in record.run["world"].get("seed", []))


def no_wave(record: Record) -> str:
    """Why a row of a packet's motion is not read: no wave lay in the world, else no position per close."""
    return (
        "no lay with a wave number in the world"
        if not wave_lay(record)
        else "a position per close is not read"
    )


def no_field(record: Record) -> str:
    """Why the spinor's two beats are not read: a quartet's universe has no held field, the others no shape-8 row."""
    quartet = any(int(r["shape"]) == QUARTET for r in record.run["universe"]["rows"])
    return "no held field in the world" if quartet else "no shape-8 row in the record's universe"


def no_conversion(record: Record) -> str:
    """Why the neutrino is not read: no conversion in the record, every prime of den within the width."""
    points = len(record.circle())
    return f"no conversion in the record and every prime of den within the width ({points} points on den's circle)"


UNREAD: tuple[tuple[str, str | Callable[[Record], str], str], ...] = (
    (
        "20 the twist's 24 and 24",
        "one seed's run; the 48 images are the board test's",
        "the 24 rotations' records equal, the 24 reflections' equal with the senses exchanged",
    ),
    (
        "28 the conversion list",
        "no record ends at a Node where others begin (the conversion act is not in the engine)",
        "a lift ends and its children begin at one Node, the charge and the count kept",
    ),
    (
        "32 the perihelion",
        no_wave,
        "the orbit's turning point advancing over a body's positions per close",
    ),
    (
        "35 frame dragging for matter, light not dragged",
        "no mass moves beside a body's track in the world",
        "a plane's track turned beside a moving mass, light's not",
    ),
    (
        "36 the shears as waves",
        "the rows carry the tension's extremes and no shear line",
        "the + polarisation travelling across the board, the x polarisation absent",
    ),
    (
        "38 the Aharonov-Bohm phase",
        "no held flux in the world",
        "a plane's clicks around a held flux shifted by the enclosed count",
    ),
    (
        "39 the Zeeman and Stark shifts",
        "no held field in the world (the toy's one-Node test carries the doublet)",
        "a body's beat shifted beside a neighbour's field, the doublet split",
    ),
    (
        "41 the spinor's two beats",
        no_field,
        "two beats of one quantum at rest in a held uniform field (the Zeeman doublet, tests/test_the_quartet.py)",
    ),
    (
        "42 the split along the gradient (Stern-Gerlach)",
        "no gradient field in the world (the toy's records carry the verdict)",
        "a neutral packet's credits in two spots along the gradient's axis, re-split on a second axis",
    ),
    (
        "44 the moving lay's velocity against k",
        no_wave,
        "the centroid at the group velocity v = P / (2 E); the momentum summed before and after a collision",
    ),
    (
        "48 the black body",
        "no gap-0 credit in the record (the sea one mode)",
        "a spectrum over the light credits' beats at a detector",
    ),
    (
        "50 light on light",
        "no two light packets in the world",
        "two light packets' credits coupled after crossing",
    ),
    (
        "51 the Casimir force and the running alpha",
        "no plates and no bound pair in the world",
        "a force between plates; a bound pair's beat changing with the content",
    ),
    ("52 the neutrino", no_conversion, "a third child's credits at a conversion"),
    (
        "53 a fast packet binds at its lay",
        no_wave,
        "a heavy packet keeps its velocity, or its stop is read as the momentum into its well and named",
    ),
    (
        "54 scattering, two packets through each other",
        "two packets of one plane are not told apart by their line, and the momentum across the click is row 23",
        "the packets scatter, the momentum summed before and after",
    ),
)  # the rows no record from the seed carries: the key, why (a sentence, or read from the record), the predicate


def stub(number: str) -> Callable[[Record], dict[str, Any]]:
    """The row function of an UNREAD row by its number (the key's first word): NOT READ with its why and its predicate."""
    key, why, predicate = next(entry for entry in UNREAD if entry[0].split()[0] == number)

    def row(record: Record) -> dict[str, Any]:
        return unread(key, why(record) if callable(why) else why, predicate)

    row.__name__ = row.__qualname__ = f"row_{number}"
    return row


def eighths_of(record: Record) -> tuple[list[int | None], list[list[int]], list[tuple[int, list[int]]]]:
    """The eras in the clicks' view (rows 58 to 60): the spacing of a line's credits at one Node in the Node's own proper count, its mean per eighth of the run (the whole run's eighths, so a cut reads the same eighths; an eighth read once complete), the growth of each eighth over the complete one before it as (the eighth, the growth), and the last credit of each eighth (its interval and Node)."""
    eighths: list[list[int]] = [[] for _ in range(LISTED)]
    last: list[tuple[int, list[int]]] = [(0, []) for _ in range(LISTED)]
    whole = int(record.run["intervals"])
    for cs in record.bodies_of().values():
        for a, b in zip(cs, cs[1:], strict=False):
            k = int(quot((int(b["i"]) - 1) * LISTED, whole) or 0)
            eighths[k].append(int(b["proper"]) - int(a["proper"]))
            last[k] = max(last[k], (int(b["i"]), list(b["node"])), key=lambda p: p[0])
    means = [
        quot(sum(s), len(s)) if s and k < int(quot(record.intervals * LISTED, whole) or 0) else None
        for k, s in enumerate(eighths)
    ]
    growths: list[list[int]] = []
    for k in range(1, LISTED):
        m, n = means[k - 1], means[k]
        if m is not None and n is not None:
            growths.append([k, n - m])
    return means, growths, last


def era_row(
    record: Record, key: str, found: Callable[[list[int]], int | None], words: str, cause: str
) -> dict[str, Any]:
    """One era row: SHOWN at the growth found (the eighth completing the reading, its last credit's interval and Node), else NOT SHOWN with the cause, NOT READ with fewer than two growths."""
    means, growths, last = eighths_of(record)
    numbers = {
        "mean spacing per eighth (proper count)": means,
        "growth per eighth over the one before (the eighth, the growth)": growths,
    }
    if len(growths) < PAIR:
        return {key: numbers | {"verdict": "NOT READ: fewer than two eighths' growths of the spacing"}}
    at = found([g for _k, g in growths])
    if at is None:
        return {key: numbers | {"verdict": f"NOT SHOWN: {cause}"}}
    i, node = last[growths[at][0]]
    return {
        key: numbers
        | {"at": node, "verdict": f"SHOWN: {words} (the eighth whose last credit is at {i})"}
    }


def fast_expansion(record: Record) -> dict[str, Any]:
    """Row 58: the fast expansion after the bang, the spacing's growth largest in the first eighths (the first growth above zero and above the next)."""
    return era_row(
        record,
        "58 the fast expansion after the bang",
        lambda g: 1 if g[0] > 0 and g[0] > g[1] else None,
        "the credits' spacing grows fastest in the first eighths",
        "the first growth of the spacing is not above zero and above the next",
    )


def deceleration(record: Record) -> dict[str, Any]:
    """Row 59: the deceleration, a later eighth's growth of the spacing smaller than the one before."""
    return era_row(
        record,
        "59 the deceleration in the clicks",
        lambda g: next((k for k in range(1, len(g)) if g[k] < g[k - 1]), None),
        "an eighth's growth of the spacing smaller than the one before",
        "no eighth's growth smaller than the one before",
    )


def acceleration_in_clicks(record: Record) -> dict[str, Any]:
    """Row 60: the acceleration in the clicks, after a slowing an eighth's growth of the spacing larger than the one before."""

    def quickens(g: list[int]) -> int | None:
        slow = next((k for k in range(1, len(g)) if g[k] < g[k - 1]), len(g))
        return next((j for j in range(slow + 1, len(g)) if g[j] > g[j - 1]), None)

    return era_row(
        record,
        "60 the acceleration in the clicks",
        quickens,
        "after a slowing, an eighth's growth of the spacing larger than the one before",
        "no eighth's growth larger than the one before after a slowing",
    )
