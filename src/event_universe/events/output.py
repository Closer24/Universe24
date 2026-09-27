"""The readings and the output lines of the engine: the exact rationals of the books, the leak test, the record's click line (`gather`), the books, the bodies' contents and the state stream; each function reads the simulation it is given, and the loop binds them as its methods."""

from __future__ import annotations

from collections.abc import Iterator
from math import gcd
from typing import TYPE_CHECKING

from event_universe.core.rule3 import division_forward, rungs

if TYPE_CHECKING:
    from event_universe.events import detector_law, records

# A RATIONAL IS A PAIR OF INTEGERS (numerator, denominator) in lowest terms with the denominator
# positive: the engine holds no `fractions` (the integer rule; tests/test_integer_algebra.py). The
# pairs are Python integers without the working bound (the conserved form summed over a board and
# the body-frame booking's terms exceed 2^63, as the exact rationals they replace did); gcd, sums
# and products alone.
Ratio = tuple[int, int]
ZERO: Ratio = (0, 1)


def ratio(numerator: int, denominator: int) -> Ratio:
    """The pair (n, d) in lowest terms with d positive (one gcd; the two exact divisions by the common factor are Rule3's division act, `division_forward`, the one division of the package)."""
    if denominator < 0:
        numerator, denominator = -numerator, -denominator
    common = gcd(numerator, denominator) or 1
    return division_forward(numerator, common, 0)[0], division_forward(denominator, common, 0)[0]


def ratio_sum(terms: list[Ratio]) -> Ratio:
    """The exact sum of pairs, reduced after every addition (sums and products)."""
    numerator, denominator = 0, 1
    for n, d in terms:
        numerator, denominator = ratio(numerator * d + n * denominator, denominator * d)
    return numerator, denominator


def form_json(value: Ratio) -> list[int]:
    """A form's exact rational for the books and the state (GAMEBOARD): the pair [numerator, denominator] in lowest terms (the denominator 1 for a record at one level and for the fields; ALGEBRA.md #the-direction)."""
    numerator, denominator = ratio(value[0], value[1])
    return [numerator, denominator]


def leaks(simulation: detector_law.DetectorLawSimulation) -> list[str]:
    """The leak test: the names of the families that carry rows without a source (a held family no body ever sourced whose record has a nonzero level or remainder; a family the step alone moves with no body, no stock and no emitter that has a record), read by attribute, never by a name; a HOST reading of the state."""
    found: list[str] = []
    for family, record in simulation.held_records.items():
        if simulation._sourced_ever[(family, 0)]:
            continue
        if record.now.any() or record.before.any() or record.remainder.any():
            found.append(simulation.families[family].name)
    # every other part of a held family with no source of its own stays exactly zero (ALGEBRA.md
    # #the-interval: the leak test per part)
    for family, parts in simulation.held_parts.items():
        for record in parts:
            if simulation._sourced_ever[(family, record.part)]:
                continue
            if record.now.any() or record.before.any() or record.remainder.any():
                name = f"{simulation.families[family].name}[{record.part}]"
                if name not in found:
                    found.append(name)
    sourced = set(simulation.held_families)
    for number, entry in enumerate(simulation.world.measured):
        sourced.add(entry.family)
        sourced.update(index for index, quanta in enumerate(simulation.held[number]) if quanta)
        if entry.block is not None and entry.block.emitter is not None:
            sourced.add(entry.block.emitter.family)
    for live in simulation.records.values():
        if live.family not in sourced:
            name = simulation.families[live.family].name
            if name not in found:
                found.append(name)
    return found


def gather_line(
    simulation: detector_law.DetectorLawSimulation, live: records.LiveRecord, chosen: int | None
) -> None:
    """The record's one click line (`gather`): the content handed to the measured event at the chosen detector (or booked as escaped at a face or a set without a body; with no detector chosen, to the escaped row or, where the record's own emitter took it wholly, to `taken_by_emitter`), with `click` the chosen detector's first rung (or the completion where no rung was crossed) and `clock` the detector's own count; called once per record, at the close (`_click`) or at the receiver's rung (`_line_at_rung`)."""
    # the ladder's weights: the record's ladder of `_ladder_of` (the emitter's named sets, or the
    # block's receiver, or every declared set, the face receiver last on every ladder; ALGEBRA.md
    # #rule3 (b)), every detector off it at 0, so that the detector of u is over the ladder's own
    # sum and a detector off the ladder is never chosen
    ladder_detectors = set(simulation._ladder_of(live))
    on_ladder = [detector in ladder_detectors for detector in range(len(live.pointers))]
    weights = [(p if here else 0, 1) for p, here in zip(live.pointers, on_ladder, strict=True)]
    family = live.family
    ladder, total = rungs(weights, live.wheel)
    sunk = sum(p for p, here in zip(live.pointers, on_ladder, strict=True) if not here)
    if chosen is None:
        simulation.ledger.transit_escaped[family] += live.content
        simulation.ledger.held_escaped[family] += 0
    else:
        measured = simulation.detector_measured[chosen]
        if measured is not None and not simulation.detector_face[chosen]:
            simulation.held[measured][family] += live.content
            simulation.ledger.held_measured[family] += live.content
            simulation.ledger.transit_absorbed[family] += live.content
        else:
            # a set without a body (the face receiver, a set on free Nodes): the click consumes the
            # quantum as any click does
            simulation.ledger.transit_absorbed[family] += live.content
    simulation.layer.gathered += 1
    gather: dict[str, object] = {
        "event": "gather",
        "tick": simulation.tick,
        "arrived": simulation.tick,
        "family": simulation.families[family].name,
        "record": live.identity,
        # HOST: the giving residue, the input of the diagnostic E_N and never a reader-of-record
        # field (the reader reads `click`, `giving` and `chosen`; DECLARATIONS.md section 2 item 8)
        "u": live.u,
        # HOST: the ledger's row `taken_by_emitter` is 0 since the emitter's own take retired
        # (ALGEBRA.md #the-click); kept for the readers' form
        "taken_by_emitter": 0,
        # HOST (the receiver by name): the sinks' take of the record by this line, in the pointer's
        # unit (the faces and every set but the receiver; on no pointer); on a record with a
        # receiver alone
        "given": live.given,
        "chosen": (
            [[simulation.detector_set[chosen], simulation.detector_channel[chosen], "0"]]
            if chosen is not None
            else None
        ),
        "node": [],
        "windows": [],
        "content": live.content,
        # THE FOUR-VECTOR (ALGEBRA.md #the-primitives; commit 5 without the recoil): the count is
        # `content`, the space part the sign per axis of the chosen detector's tally, the taken quantum's
        # direction of travel (DETECTOR); [0, 0, 0] with no detector chosen. No body's momentum moves
        "momentum": (
            simulation.direction_of(live.momentum_tally.get(chosen, [0, 0, 0]))
            if chosen is not None
            else [0, 0, 0]
        ),
        "weight": [live.pointers[chosen] if chosen is not None else 0, 1],
        "total": list(total),
        "T": live.absorbed,
        "before": sum(1 for p in live.pointers if p),
        "after": 1 if chosen is not None else 0,
        "detectors": [
            [[[set_name, channel, "0"]], rung]
            for set_name, channel, rung, pointer in zip(
                simulation.detector_set, simulation.detector_channel, ladder, live.pointers, strict=True
            )
            if pointer
        ],
        # the ladder by name (the lamp's `receiver`): the sets on it, and HOST the pointers' sum at
        # the sinks (the detectors off the ladder, taken and booked, never chosen); None and 0 for
        # every detector
        **(
            {
                "ladder": sorted({simulation.detector_set[detector] for detector in live.ladder}),
                "sunk": sunk,
            }
            if live.ladder is not None
            else {}
        ),
        "giving": live.giving_tick,
        # The click's time: the interval at which the chosen detector's pointer crossed its first
        # rung (the counting form, s_D = 1 / W), the detector's own count on the click line; the
        # record completed at `tick`, when its offer was exhausted.
        "click": (
            live.first_rung[chosen]
            if chosen is not None and live.first_rung[chosen] is not None
            else simulation.tick
        ),
        # which the click's time is: the chosen detector's first rung or, where no rung was crossed
        # (a screen row's Node at 1e-4 of the norm), the completion interval; a reader never reads
        # a completion as a rung
        "click_at": (
            "rung" if chosen is not None and live.first_rung[chosen] is not None else "completion"
        ),
        # whose count the `clock` stamp is: a block's own count where the chosen detector is a
        # block's detector or a set bound to a block (keys (i) and (ii)), else the interval
        "clock_source": (
            f"measured:{simulation.detector_measured[chosen]}"
            if chosen is not None and (live.identity, chosen) in simulation.rung_counts
            else "interval"
        ),
        **(
            {
                "clock": (
                    # A block's detector: the block's own count at the first rung (the body's
                    # event in the body's own clock); a receiver as built: its count is the interval.
                    simulation.rung_counts[(live.identity, chosen)]
                    if chosen is not None and (live.identity, chosen) in simulation.rung_counts
                    else live.first_rung[chosen]
                    if chosen is not None and live.first_rung[chosen] is not None
                    else simulation.tick
                )
            }
            if simulation.world.clock_stamp
            else {}
        ),
    }
    simulation.layer.gathers.append(gather)
    if simulation.record is not None:
        simulation.record(gather)


def books(simulation: detector_law.DetectorLawSimulation, recount: bool = False) -> dict[str, object]:
    families: dict[str, object] = {}
    balanced = True
    ledger = simulation.ledger
    for index, family in enumerate(simulation.families):
        current = sum(h[index] for h in simulation.held)
        measured = {
            "initial": ledger.held_initial[index],
            "measured": ledger.held_measured[index],
            "became": 0,
            "current": current,
            "spent": ledger.held_spent[index],
            "escaped": ledger.held_escaped[index],
        }
        measured["balanced"] = measured["initial"] + measured["measured"] == (
            measured["current"] + measured["spent"] + measured["escaped"]
        )
        transit_current = sum(
            live.content for live in simulation.records.values() if live.family == index
        )
        transit = {
            "initial": 0,
            "released": ledger.transit_released[index],
            "current": transit_current,
            "absorbed": ledger.transit_absorbed[index],
            "escaped": ledger.transit_escaped[index],
            # HOST (item 10): the content the records' own emitters took
            "taken_by_emitter": ledger.taken_by_emitter[index],
            # HOST (the receiver by name): the count of records closed after their line at the
            # receiver's rung; on a world with a receiver alone (a lamp world's books byte for byte)
            **(
                {"closed_after_click": ledger.closed_after_click[index]}
                if simulation.has_receiver
                else {}
            ),
        }
        transit["balanced"] = transit["released"] == (
            transit["current"] + transit["absorbed"] + transit["escaped"] + transit["taken_by_emitter"]
        )
        balanced = balanced and bool(measured["balanced"]) and bool(transit["balanced"])
        lines: dict[str, object] = {"measured": measured, "transit": transit}
        if simulation.world.massive_record:
            # The conserved form I summed over the family's live records (massive-record-v1): a
            # GAMEBOARD diagnostic, written under the key alone.
            lines["form"] = form_json(
                ratio_sum(
                    [
                        simulation.record_form(live)
                        for live in simulation.records.values()
                        if live.family == index
                    ]
                    + [
                        simulation.record_form(record)
                        for record in (
                            [simulation.held_records[index], *simulation.held_parts[index]]
                            if index in simulation.held_records
                            else []
                        )
                        if not record.silent
                    ]
                )
            )
        families[family.name] = lines
    return {
        "tick": simulation.tick,
        "families": families,
        # Issue #1086 (the Boss's 02:00Z): the momentum books are a GAMEBOARD diagnostic, no law and
        # no pin: `held` the sum of the blocks' declared momentum vectors (the momentum on the board's
        # bodies); `transit` and `escaped` are not accounted until the massive kind's momentum books
        # are designed (ALGEBRA.md 8.11, the physicist's), and `balanced` counts content alone.
        "momentum": {
            "held": [sum(int(block.momentum[axis]) for block in simulation.blocks) for axis in range(3)],
            "transit": None,
            "escaped": None,
            "note": "transit and escaped not accounted (the massive kind's momentum books "
            "are not designed, ALGEBRA.md 8.11); balanced counts content alone",
        },
        "records": len(simulation.records),
        "balanced": balanced,
        "balanced_scope": "content alone (the momentum books are not accounted)",
    }


def contents(simulation: detector_law.DetectorLawSimulation) -> list[dict[str, object]]:
    return [
        {
            "number": number,
            "position": list(entry.position),
            "family": simulation.families[entry.family].name,
            "held": list(simulation.held[number]),
        }
        for number, entry in enumerate(simulation.world.measured)
    ]


def snapshot_stream(simulation: detector_law.DetectorLawSimulation) -> Iterator[tuple[str, object]]:
    """The state's (key, value) pairs for state.json: the tick, the held content per measured event and the live records (their identity, age, train and the detectors' pointers), not their rows."""
    yield "tick", simulation.tick
    yield "measured", simulation.contents()
    # the held families' levels over the board (GAMEBOARD; ALGEBRA.md #the-counts-line, 9.48; item
    # 51): each by its declared name and source, the Node clock's Gamma beside them
    yield "node_clock", simulation.node_clock
    yield (
        "held_fields",
        [
            {
                "family": simulation.families[family].name,
                "held": simulation.families[family].held,
                "rows": record.now.ravel().tolist(),
                "form": form_json(simulation.record_form(record)),
            }
            for family, record in simulation.held_records.items()
        ],
    )
    if simulation.world.massive_record:
        # The blocks (massive-record-v1): the corner, the momentum, the spin, and the rows of the
        # block's own record (its amplitude now over the board, GAMEBOARD:
        # the mode's extent is read from them).
        yield (
            "blocks",
            [
                {
                    "measured": block.number,
                    "family": simulation.families[block.family].name,
                    "corner": list(block.corner),
                    "side": block.definition.side,
                    "extents": list(block.definition.extents),
                    "momentum": list(block.momentum),
                    "spin": list(block.spin),
                    "fixed": block.fixed,
                    "emitted": list(block.emitted),
                    "rows": None if block.own is None else block.own.now.ravel().tolist(),
                    "form": (
                        form_json((simulation.node_record_form(block), 1))
                        if block.node_record is not None
                        else None
                        if block.own is None
                        else form_json(simulation.record_form(block.own))
                    ),
                    # the body's Node's record, (a, b, r) at the body's Node (ALGEBRA.md #what-a-body-is; item 42; GAMEBOARD)
                    "node_record": (
                        None
                        if block.node_record is None
                        else [
                            block.node_record.now,
                            block.node_record.before,
                            block.node_record.remainder,
                        ]
                    ),
                }
                for block in simulation.blocks
            ],
        )
    yield (
        "records",
        [
            {
                "record": live.identity,
                "lamp": live.lamp,
                "family": simulation.families[live.family].name,
                "u": live.u,
                # HOST (the receiver by name): whether the record's line was written at its
                # receiver's rung (it lives on with content 0); on a world with a receiver alone
                **(
                    {"clicked": live.clicked, "escaped": live.escaped} if simulation.has_receiver else {}
                ),
                "given": live.given,
                "giving": live.giving_tick,
                "age": live.age,
                "train": live.train,
                "norm": live.norm,
                "absorbed": live.absorbed,
                "pointers": dict(zip(simulation.detector_names, live.pointers, strict=True)),
                **(
                    {"form": form_json(simulation.record_form(live))}
                    if simulation.world.massive_record
                    else {}
                ),
            }
            for live in simulation.records.values()
        ],
    )
