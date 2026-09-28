"""The reversible row of the expectation file (HIGHLIGHTS line 33): N intervals forward and N back through the clicks, every row of the GameBoard bit for bit, MATCH or MISS naming the first interval and Node that deviate; a host tool that undoes a click's ledger by hand and no law."""

from __future__ import annotations

import copy
import hashlib
from typing import Any

import numpy as np

from event_universe.core.rule3 import THE_REWRITE
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.events.records import StampedMap


def rows_of(simulation: DetectorLawSimulation) -> dict[str, np.ndarray]:
    """Every row of the board by name: each record's two levels and remainder (the bodies' own and the held families' among them), the held quanta and the interval."""
    rows: dict[str, np.ndarray] = {}
    records = list(simulation.records.items()) + [
        (f"held:{family}", record) for family, record in simulation.held_records.items()
    ]
    for identity, live in records:
        rows[f"record {identity} now"] = live.now
        rows[f"record {identity} before"] = live.before
        rows[f"record {identity} remainder"] = live.remainder
    rows["held quanta"] = np.array(simulation.held, dtype=np.int64)
    rows["interval"] = np.array([simulation.tick], dtype=np.int64)
    return rows


def digest_of(rows: dict[str, np.ndarray]) -> str:
    """One digest of the rows, the names in order."""
    found = hashlib.sha256()
    for name in sorted(rows):
        found.update(name.encode("utf-8"))
        found.update(np.ascontiguousarray(rows[name]).tobytes())
    return found.hexdigest()


def first_difference(now: dict[str, np.ndarray], then: dict[str, np.ndarray]) -> dict[str, Any]:
    """The first row and Node where `now` departs from `then`: a row present in one alone, or the first Node whose values differ."""
    for name in sorted(set(now) | set(then)):
        if name not in now or name not in then:
            return {"row": name, "node": None, "lost": name not in now}
        if now[name].shape != then[name].shape or not np.array_equal(now[name], then[name]):
            where = np.argwhere(now[name] != then[name]) if now[name].shape == then[name].shape else []
            return {"row": name, "node": [int(v) for v in where[0]] if len(where) else None}
    return {}


def ledger_of(simulation: DetectorLawSimulation) -> dict[str, Any]:
    """A click's ledger as the host keeps it: the held quanta and every block's momentum at both levels with its hold's values and carries (the recoil's kick among them)."""
    return {
        "held": copy.deepcopy(simulation.held),
        "blocks": [
            (list(b.momentum), list(b.momentum_before), dict(b.hold_value), dict(b.hold_carry))
            for b in simulation.blocks
        ],
    }


def restore_ledger(simulation: DetectorLawSimulation, ledger: dict[str, Any]) -> None:
    """The click's ledger undone by hand: the held quanta of the interval before restored and the fields held again, the blocks' momentum and hold values as they were."""
    simulation.held = copy.deepcopy(ledger["held"])
    for block, (momentum, before, value, carry) in zip(simulation.blocks, ledger["blocks"], strict=True):
        block.momentum, block.momentum_before = list(momentum), list(before)
        block.hold_value, block.hold_carry = StampedMap(value), StampedMap(carry)
    simulation._hold(simulation.register.at("the hold", "(iv)"), THE_REWRITE)


def forward(
    simulation: DetectorLawSimulation, lines: list[dict[str, Any]], intervals: int
) -> tuple[list[str], list[dict[str, Any]], dict[int, Any], dict[int, list[tuple[int, int]]]]:
    """The run forward: the digest of the rows and the ledger after every interval (the load's at index 0), every record a taking click deleted as it stood the interval before (the host's copy), and the records made at each interval (a giving's open, named at its close alone) with the body whose window made them."""
    digests, ledgers = [digest_of(rows_of(simulation))], [ledger_of(simulation)]
    previous = {identity: copy.deepcopy(live) for identity, live in simulation.records.items()}
    lost: dict[int, Any] = {}
    opened: dict[int, list[tuple[int, int]]] = {}
    for _ in range(intervals):
        simulation.step()
        for line in lines:
            if line["event"] == "gather" and line["tick"] == simulation.tick:
                lost[int(line["record"])] = previous[int(line["record"])]
        for identity in set(simulation.records) - set(previous):
            makers = [b.number for b in simulation.blocks if b.window == identity]
            opened.setdefault(simulation.tick, []).append((identity, makers[0] if makers else -1))
        previous = {identity: copy.deepcopy(live) for identity, live in simulation.records.items()}
        digests.append(digest_of(rows_of(simulation)))
        ledgers.append(ledger_of(simulation))
    return digests, ledgers, lost, opened


def step_back(
    simulation: DetectorLawSimulation,
    lines: list[dict[str, Any]],
    ledgers: list[dict[str, Any]],
    lost: dict[int, Any],
    opened: dict[int, list[tuple[int, int]]],
    t: int,
) -> None:
    """The interval t stepped back: across a click (a giving's open, a window's close with its recoil, a taking) the click's ledger undone by hand first (NO RULE UNDOES A CLICK), the record made at an open removed, a window's close reopened on its record, then the engine's inverse, then the record a taking deleted restored from the host's copy."""
    givings = [line for line in lines if line["event"] == "giving"]
    opens = opened.get(t, [])
    closes = [line for line in givings if line["tick"] == t]
    takings = [line for line in lines if line["event"] == "gather" and line["tick"] == t]
    if opens or closes or takings:
        restore_ledger(simulation, ledgers[t - 1])
    for identity, number in opens:
        simulation.records.pop(identity, None)
        block = simulation.block_by_number.get(number)
        if block is not None and block.window == identity:
            block.window = None
    for line in closes:
        live = simulation.records.get(int(line["record"]))
        if live is not None:
            block = simulation.block_by_number[int(line["measured"])]
            live.window_open, block.window = True, live.identity
    simulation.step_inverse()
    for line in takings:
        simulation.records[int(line["record"])] = lost[int(line["record"])]


def reversible_row(build: Any, intervals: int) -> dict[str, Any]:
    """The row: `build()` a fresh simulation with its lines, run `intervals` forward and back; MATCH where every interval's rows return bit for bit, MISS naming the first interval back that deviated, its first differing row and Node (read by a fresh run to that interval), or the engine's refusal by name."""
    simulation, lines = build()
    if intervals < 1:
        return {"kind": "reversible", "pin": intervals, "read": None, "verdict": "MISS"}
    digests, ledgers, lost, opened = forward(simulation, lines, intervals)
    for t in range(intervals, 0, -1):
        try:
            step_back(simulation, lines, ledgers, lost, opened, t)
        except ValueError as refusal:
            read = {"intervals_back": intervals - t, "refused": str(refusal), "interval": t}
            return {"kind": "reversible", "pin": intervals, "read": read, "verdict": "MISS"}
        if digest_of(rows_of(simulation)) != digests[t - 1]:
            again, _ = build()
            for _ in range(t - 1):
                again.step()
            miss = {"interval": t - 1, **first_difference(rows_of(simulation), rows_of(again))}
            read = {"intervals_back": intervals - t + 1, "first_miss": miss}
            return {"kind": "reversible", "pin": intervals, "read": read, "verdict": "MISS"}
    read = {"intervals_back": intervals, "first_miss": None}
    return {"kind": "reversible", "pin": intervals, "read": read, "verdict": "MATCH"}
