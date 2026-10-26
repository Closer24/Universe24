"""The reading's event lines (the owner's words of 2026-10-25: the record tells what it sees as it sees it; every gate has a label when it happens): one line per row of the table at the interval it first shows, found by reading the row on the record cut to each interval (a search on the cuts, the verdict read as standing from its first interval on), with its Node where the row names one (`at`) and its label in the gate's own words of three to six and its phenomenon in plain words (NAMES, the one table of the rows' names), for the page's labels and the bar's ticks; every line read from the record alone."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from event_universe.decoder import HALF, Record, shown

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
