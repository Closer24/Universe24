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
    """The run forward: the digest of the rows and the ledger after every interval (the load's at index 0), every record a report changed as it stood the interval before (the host's copy), and the records made at each interval (a giving at a body's click) with the body that gave them."""
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
            maker = simulation.records[identity].emitter
            opened.setdefault(simulation.tick, []).append((identity, -1 if maker is None else maker))
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
    """The interval t stepped back: across a click (a giving, a report with its recoil) the click's ledger undone by hand first (NO RULE UNDOES A CLICK), the record a giving made removed, the recoil's turn of the body's record undone from the copy on its line, then the engine's inverse, the giver's click given back, then the record a report changed restored from the host's copy."""
    opens = opened.get(t, [])
    takings = [line for line in lines if line["event"] == "gather" and line["tick"] == t]
    if opens or takings:
        restore_ledger(simulation, ledgers[t - 1])
    for identity, _number in opens:
        simulation.records.pop(identity, None)
    for line in lines:
        # the recoil's turn of the body's own record undone from the host's copy on the line (the click keeps the click)
        block = (
            simulation.block_by_number.get(int(line["measured"])) if line["event"] == "recoil" else None
        )
        if (
            line["event"] == "recoil"
            and line["tick"] == t
            and block is not None
            and block.own is not None
        ):
            block.own.now[block.mask] = np.array(line["levels_before"][0], dtype=np.int64)
            block.own.before[block.mask] = np.array(line["levels_before"][1], dtype=np.int64)
    simulation.step_inverse()
    for _identity, number in opens:
        block = simulation.block_by_number.get(number)
        if block is not None:
            block.new_cycle = True  # the click the giving spent
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
