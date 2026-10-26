"""The reading's event lines (the owner's words of 2026-10-25: the record tells what it sees as it sees it; every gate has a label when it happens): one line per row of the table at the interval it first shows, found by reading the row on the record cut to each interval (a search on the cuts, the verdict read as standing from its first interval on), with its Node where the row names one (`at`) and its label in the gate's own words of three to six (LABELS), for the page's labels and the bar's ticks; every line read from the record alone."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from event_universe.decoder import HALF, Record

LABELS = {
    "1": "a bang recurs",
    "1b": "the board tops, every Node turns",
    "1c": "the board returns to Gamma",
    "2": "the Links lengthen",
    "3": "the board shortens then lengthens",
    "4": "the era of matter",
    "5": "the lengthening quickens",
    "6": "the board contracts",
    "7": "light absorbed at a take",
    "8": "a body clicks",
    "8b": "a track read right",
    "9": "two bodies meet",
    "10": "the clocks run slow",
    "11": "light redder where deeper",
    "12": "light delayed or bent",
    "13": "the fall quickens",
    "14": "the horizon",
    "15": "the take pays the walls",
    "16": "the floor holds",
    "17": "a pair born",
    "18": "the run back exact",
    "19": "the mass ratio read",
    "20": "the twist's 24 and 24",
    "21": "births of both hands",
    "22": "unlike attract, like repel",
    "23": "the recoil passed",
    "24": "a pair into light",
    "25": "the entropy rises",
    "26": "three lifts, the beats ordered",
    "27": "no third alone",
    "28": "a conversion",
    "29": "light's period longer where deeper",
    "30": "the deeper clock slower",
    "31": "light's track bent or late",
    "32": "the perihelion advances",
    "33": "the body falls by its tail",
    "34": "the clock stops at the horizon",
    "35": "matter dragged, light not",
    "36": "a shear wave travels",
    "37": "one Link per interval",
    "38": "the phase shifted by the flux",
    "39": "the beat shifted in the field",
    "40": "one quantum one click",
    "41": "the spinor's two beats",
    "42": "the split along the gradient",
    "43": "the exclusion holds",
    "44": "the packet at its velocity",
    "45": "a body stands in its well",
    "46": "the bang recurs with its gates",
    "47": "the take exact",
    "48": "a black body spectrum",
    "49": "the clicks decay geometrically",
    "50": "light couples to light",
    "51": "the Casimir force",
    "52": "a third child",
    "53": "a fast packet binds",
    "54": "two packets scatter",
    "55": "the two slits",
    "56": "Bell's bound holds",
    "57": "the GHZ gate",
    "58": "the fast expansion",
    "59": "the expansion slows",
    "60": "the expansion quickens again",
    "the conservations in the clicks": "the clicks conserve",
    "the three constants": "the three constants hold",
}


def label_of(key: str) -> str:
    """The label of a row from its key: by the row's number (the key's first word) or by the key itself."""
    return LABELS.get(key.split()[0], LABELS.get(key, key))


def shown(verdict: str) -> bool:
    """A verdict that shows (whole or in part)."""
    return verdict.startswith("SHOWN")


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
    record: Record, table: tuple[Callable[[Record], dict[str, Any]], ...]
) -> list[dict[str, Any]]:
    """Every event line in the order of its interval: for every row of the table that shows on the whole record, the interval it first shows, its Node where the row names one, its label and its verdict's first clause as its numbers."""
    found = []
    for row in table:
        for key, out in row(record).items():
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
