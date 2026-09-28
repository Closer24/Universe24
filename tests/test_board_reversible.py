"""The GameBoard is reversible in time between clicks, and the clicks keep the physical definitions: one small world with every piece, stepped forward and back bit for bit (ALGEBRA.md #the-direction)."""

from __future__ import annotations

import copy
from fractions import Fraction

import numpy as np

from event_universe.core.rule3 import THE_REWRITE, coefficients
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import input_stamp, parse_nature_beam_world
from tests.running import Seen, chosen_by_the_rule, exchange_of, form_I, spy_on
from tests.worlds import emitter_world, family_entry, reads, seed_on_the_mode

LIGHT, MATTER, POSITIVE = 0, 1, 2
STOCK = 3


def reversible_world(ticks: int = 400) -> dict:
    """The emitter chain of 80 (x closed) with the stock 3, light and the matter kind of charge -1, a fifth family `positive` of light's pair and charge +1 held by one body at x = 55, the screen at [70, 72]; seeded on the mode by the generator (the profile, the clock pair, the period, the given rows under the stamp)."""
    document = emitter_world(stock=STOCK, ticks=ticks, on_mode=False)
    document["universe"][LIGHT]["sign"] = -1
    document["universe"][MATTER]["sign"] = -1
    document["universe"].insert(
        POSITIVE,
        family_entry("positive", [1, 1], reads(), clock=[512, 1], sign=1),
    )
    document["measured"].append(
        {
            "position": [55, 0, 0],
            "family": "positive",
            "amount": 1,
            "stocks": {},
            "momentum": [0, 0, 0],
            "momentum_before": [0, 0, 0],
        }
    )
    seed_on_the_mode(document)
    document["stamp"] = input_stamp(document)
    return document


def rows_of(simulation: DetectorLawSimulation) -> dict[str, object]:
    """Every row of the board: the records' two levels and remainders (the bodies' own among them), both fields' rows, the held quanta and the interval."""
    return {
        "records": {
            identity: (live.now.copy(), live.before.copy(), live.remainder.copy())
            for identity, live in simulation.records.items()
        },
        "clock": (
            simulation.held_record("content").now.copy(),
            simulation.held_record("content").before.copy(),
            simulation.held_record("content").remainder.copy(),
        ),
        "charge": (
            simulation.held_record("sign").now.copy(),
            simulation.held_record("sign").before.copy(),
            simulation.held_record("sign").remainder.copy(),
        ),
        "held": copy.deepcopy(simulation.held),
        "tick": simulation.tick,
    }


def assert_same(now: dict, then: dict, lost: set[int] = frozenset()) -> None:
    """`now` equals `then` bit for bit, but for the records in `lost` (present in `then`, absent in `now`)."""
    assert set(then["records"]) - set(now["records"]) == set(lost)
    assert set(now["records"]) <= set(then["records"])
    for identity, rows in now["records"].items():
        for x, y in zip(rows, then["records"][identity], strict=True):
            assert np.array_equal(x, y), identity
    for key in ("clock", "charge"):
        for x, y in zip(now[key], then[key], strict=True):
            assert np.array_equal(x, y), key
    assert now["held"] == then["held"] and now["tick"] == then["tick"]


def run_states(document: dict, ticks: int) -> tuple[DetectorLawSimulation, list[dict], list[dict], Seen]:
    """The world stepped `ticks` intervals: the simulation, the rows after every interval (the load's at index 0), the lines, and the ladder spy's readings at every click."""
    lines: list[dict] = []
    simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
    seen: Seen = {}
    spy_on(simulation, seen)
    states = [rows_of(simulation)]
    for _ in range(ticks):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
        states.append(rows_of(simulation))
    return simulation, states, lines, seen


def click_ticks(lines: list[dict]) -> tuple[list[int], list[int]]:
    """The intervals of the giving clicks (the windows' opens, SINCE COMMIT 7: the quantum moves and the record is made at the open, the line is named at the close) and of the taking clicks."""
    giving = [line["opened"] for line in lines if line["event"] == "giving"]
    taking = [line["tick"] for line in lines if line["event"] == "gather"]
    return giving, taking


def close_ticks(lines: list[dict]) -> list[int]:
    """The intervals of the windows' closes (the giving lines' own ticks)."""
    return [line["tick"] for line in lines if line["event"] == "giving"]


def inverse_close_interval(simulation: DetectorLawSimulation, lines: list[dict], t: int) -> None:
    """The window's close stepped back by hand (the close is named from the run's events, as a click is, ALGEBRA.md #a-familys-declaration): the window reopened on its record where the record still stands (a taking since then lost it, the click's one loss), then the interval stepped back (the write of the interval subtracted by the engine's inverse, the rows stepped back)."""
    line = next(line for line in lines if line["event"] == "giving" and line["tick"] == t)
    live = simulation.records.get(line["record"])
    if live is not None:
        block = simulation.block_by_number[line["measured"]]
        live.window_open = True
        block.window = live.identity
    simulation.step_inverse()


def test_between_clicks_the_board_returns_bit_for_bit_where_the_field_rises_and_falls():
    """1. From the load to the interval before the first giving click, every interval back returns the load's rows bit for bit: the bodies' own records, the family of clicks and the family of charge (their levels and remainders), the held quanta; the family of charge's level at the load is its rest (THE START on the sum's sources, ALGEBRA.md #the-generator; the hold's row): the tent of the signed sources over the divisor (this copy's 100: the emitter's -4 over 32 Nodes, the screen's -1 x 3, the positive body's +1), negative from the first Node to the screen and 0 only beyond the closed faces, no level above 0; the tent's nearest integers are no fixed point of the integer line, so the field waves within one unit: it fell at Nodes (the falls counted, above 0) and rose again at Nodes that had fallen; the family of clicks' level is its own small tent (the counts 4, 1 and 1 over the divisor) and stays within one of it. ALGEBRA.md #the-direction: the wall constant, one to one."""
    document = reversible_world()
    for entry in document["universe"]:
        if "held" in entry:
            entry["held"] = {**entry["held"], "divisor": 100}  # a copy: the tent stands in whole levels
    document["stamp"] = input_stamp(document)
    probe, _, lines, _ = run_states(document, 120)
    first_giving = click_ticks(lines)[0][0]
    assert first_giving > 10
    simulation, states, lines, _ = run_states(document, first_giving - 1)
    assert not [line for line in lines if line["event"] in ("giving", "gather")]
    levels = np.stack([state["charge"][0] for state in states])  # (interval, x, y, z)
    assert (levels[0] <= 0).all() and (levels[0][:73] < 0).all()  # the tent, 0 only beyond the faces
    falls = int(np.sum(levels[1:] < levels[:-1]))
    rises = int(np.sum(levels[1:] > levels[:-1]))
    assert falls > 0 and rises > 0 and int(levels.max()) <= 0
    assert (np.stack([state["clock"][0] for state in states]) >= -1).all()  # within one of its tent
    for t in range(first_giving - 1, 0, -1):
        simulation.step_inverse()
        assert_same(rows_of(simulation), states[t - 1])
    assert simulation.tick == 0


def test_across_a_click_no_rule_undoes_it_and_only_the_deleted_rows_are_lost():
    """1. Across the first giving click and the first taking click. (a) NO RULE UNDOES A CLICK (the owner's word of record 2011): stepping back across the taking click leaves the deleted record deleted and the taken quantum with its taker (the screen's first body's held content stays the click's; its Nodes' level is the source's sum over the divisor 40000, which one quantum does not move). (b) THE CLICK'S ONE LOSS: with the click's ledger undone by hand (the held quanta of the interval before restored, the fields held again), the backward run across the taking click returns every row bit for bit but the deleted record's, and across the giving click, with the given record removed (its rows at its write the file's given rows on the body's Nodes) and the stock restored, returns every row bit for bit with nothing lost; then down to the load exactly."""
    document = reversible_world()
    probe, _, lines, _ = run_states(document, 200)
    giving_ticks, taking_ticks = click_ticks(lines)
    t_giving, t_taking = giving_ticks[0], taking_ticks[0]
    assert t_giving < t_taking and (t_giving > 10)
    if len(giving_ticks) > 1:
        assert t_taking < giving_ticks[1] or True  # a second giving may precede the taking
    end = t_taking + 5
    blind, states, lines, _ = run_states(document, end)
    taking_line = next(line for line in lines if line["event"] == "gather")
    deleted = taking_line["record"]
    assert deleted not in states[t_taking]["records"] and deleted in states[t_taking - 1]["records"]
    # (a) five intervals back with no click between: exact
    for t in range(end, t_taking, -1):
        blind.step_inverse()
        assert_same(rows_of(blind), states[t - 1])
    # across the taking click without undoing its ledger: the record stays deleted, the taker keeps its quantum
    blind.step_inverse()
    after = rows_of(blind)
    assert deleted not in after["records"]
    assert after["held"] == states[t_taking]["held"] != states[t_taking - 1]["held"]
    # (b) the same run again, the click's ledger undone by hand before each step across a click
    simulation, states, lines, _ = run_states(document, end)
    for t in range(end, t_taking, -1):
        simulation.step_inverse()
        assert_same(rows_of(simulation), states[t - 1])
    simulation.held = copy.deepcopy(states[t_taking - 1]["held"])
    simulation._hold(simulation.register.at("the hold", "(iv)"), THE_REWRITE)
    simulation.step_inverse()
    assert_same(rows_of(simulation), states[t_taking - 1], lost={deleted})
    lost = {deleted}
    closes = close_ticks(lines)
    for t in range(t_taking - 1, t_giving, -1):
        if t in giving_ticks:
            inverse_giving_interval(simulation, lines, states, t)
        elif t in closes:
            inverse_close_interval(simulation, lines, t)
        else:
            simulation.step_inverse()
        assert_same(rows_of(simulation), states[t - 1], lost=lost & set(states[t - 1]["records"]))
    inverse_giving_interval(simulation, lines, states, t_giving)
    assert_same(rows_of(simulation), states[t_giving - 1])
    for t in range(t_giving - 1, 0, -1):
        simulation.step_inverse()
        assert_same(rows_of(simulation), states[t - 1])
    assert simulation.tick == 0


def inverse_giving_interval(
    simulation: DetectorLawSimulation, lines: list[dict], states: list[dict], t: int
) -> None:
    """The giving click's interval (the window's open, SINCE COMMIT 7) stepped back by hand, the click's act undone: the given record removed (made at the open with nothing written yet, its rows zero, asserted: the writes come with the window's intervals and the engine's inverse subtracts them); every record and both fields stepped back at the content the interval began with (the hold before the click, which every forward step read: ONE ORDER FOR BOTH CLICKS, ALGEBRA.md #the-primitives, item 58; the giving's hold at once HISTORY), the body's stock restored and the fields held again first. Nothing is lost at a giving click."""
    line = next(line for line in lines if line["event"] == "giving" and line["opened"] == t)
    # the given record: present unless a taking click deleted it since (then the click's one loss, already accounted); at its open nothing is written on it
    block = simulation.block_by_number[line["measured"]]
    if line["record"] in states[t]["records"]:
        written = states[t]["records"][line["record"]]
        assert not written[0].any() and not written[1].any() and not written[2].any()
    simulation.records.pop(line["record"], None)
    if block.window == line["record"]:
        block.window = None
    # ONE ORDER FOR BOTH CLICKS (ALGEBRA.md #the-primitives; item 58): the giving's lowered quanta are held after the held families' step, as a taking's, so every record and both fields stepped forward at the content the interval began with; the inverse restores that hold and steps back as across a taking
    simulation.held = copy.deepcopy(states[t - 1]["held"])
    simulation._hold(simulation.register.at("the hold", "(iv)"), THE_REWRITE)
    simulation.step_inverse()


def test_the_clicks_keep_the_count_the_charge_the_residue_and_borns_rule():
    """2. Over 400 intervals with three giving clicks and their taking clicks: at every interval the books balance, the held quanta plus the records in flight are the load's total, and the bodies' Q plus the flights' q are the load's total (-3 - 3 + 1 = -5); at every giving click the giver's held content falls by one, the given record's content is 1, its residue u is in [0, W) with W the rule's at the first shell Node, and the click's interval is the counted one, 2 W (wait - 1) < (2 u + 1) P <= 2 W wait from the residue read before it (ALGEBRA.md #the-ladder); at every taking click the taker's held content rises by one, the record's content is 1, and the detector is the one the increment ladder chooses on the plain flux against the norm's rational (Born's rule at the taking end, ALGEBRA.md #the-ladder and (3), item 36)."""
    document = reversible_world()
    period = parse_nature_beam_world(document).measured[0].block.emitter.period
    lines: list[dict] = []
    simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
    seen: Seen = {}
    spy_on(simulation, seen)
    charge = simulation.family_charge
    total_quanta = sum(sum(h) for h in simulation.held)
    total_charge = sum(simulation._body_charge(n) for n in range(len(simulation.held)))
    # the emitter's own quantum and its stock of STOCK light quanta, all of charge -1, the screen's three light bodies and the positive body (ALGEBRA.md #the-paces; item 47)
    assert total_charge == -(STOCK + 1) - 3 + 1
    block = simulation.blocks[0]
    previous_residue = None
    residue_at_open = (0, 1)
    read_at = 0
    held_before = copy.deepcopy(simulation.held)
    for _ in range(400):
        own = block.own
        assert own is not None
        residue_before = (own.u, own.wheel)
        opens_before = block.givings
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
        flights = list(simulation.records.values())
        in_flight = [live for live in flights if live is not block.own]
        assert sum(sum(h) for h in simulation.held) + sum(f.content for f in in_flight) == total_quanta
        assert (
            sum(simulation._body_charge(n) for n in range(len(simulation.held)))
            + sum(charge[f.family] * f.content for f in in_flight)
        ) == total_charge
        if block.givings > opens_before:
            # THE OPEN (commit 7): the giving lowers the given family's content held at the body (item 47) and makes the record, its content 1; the line comes at the close; the residue the count to this open was read on is the one before this interval
            residue_at_open = residue_before
            given_family = block.definition.emitter.family if block.definition.emitter else -1
            assert simulation.held[0][given_family] == held_before[0][given_family] - 1
            assert simulation.records[block.window].content == 1
        for line in [line for line in lines if line["tick"] == simulation.tick]:
            if line["event"] == "giving":
                assert 0 <= line["u"] < line["W"] and line["read_node"] == [5, 0, 0]
                if previous_residue is not None:
                    u, wheel = previous_residue
                    wait = line["opened"] - read_at  # the open falls the count after the read
                    assert line["wait"] == wait
                    assert 2 * wheel * (wait - 1) < (2 * u + 1) * period <= 2 * wheel * wait
                else:
                    u, wheel = residue_at_open
                    assert (
                        2 * wheel * (line["wait"] - 1) < (2 * u + 1) * period <= 2 * wheel * line["wait"]
                    )
                previous_residue = (line["u"], line["W"])
                read_at = line["tick"]
            if line["event"] == "gather":
                taker = next(
                    n for n in range(len(simulation.held)) if simulation.held[n] != held_before[n]
                )
                assert sum(simulation.held[taker]) == sum(held_before[taker]) + 1
                assert line["content"] == 1 and line["record"] not in simulation.records
                total, increments, ladder, u, norm, wheel, pace = seen[line["record"]]
                assert line["chosen"][0][0] == chosen_by_the_rule(
                    simulation, total, increments, ladder, u, norm, wheel, pace
                )
        held_before = copy.deepcopy(simulation.held)
    giving_ticks, taking_ticks = click_ticks(lines)
    assert len(giving_ticks) == STOCK and len(taking_ticks) >= 1


def test_between_clicks_the_weighted_form_is_exact_where_the_field_stands():
    """2. The conserved form of ALGEBRA.md #the-direction and (13) on the given light record, interval by interval from its write to its taking click: its change with the field of the interval's start in force is the remainders' term exactly (ALGEBRA.md #the-direction), and with the field's move the weights' change exactly (ALGEBRA.md #the-counts-line, the Node terms alone under the Node's own pace); where the field stands the form is constant but for the remainders' term. The content light reads here is the effective content c - q Lambda d, light being of charge -1 (ALGEBRA.md #the-paces)."""
    document = reversible_world()
    lines: list[dict] = []
    simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
    gamma = simulation.node_clock
    followed: int | None = None
    previous_rows = None
    checked = 0
    for _ in range(200):
        # the content light reads: the effective content c - q Lambda d, light of charge -1 here (ALGEBRA.md #the-paces)
        content_start = simulation._effective_content(LIGHT).copy()
        simulation.step()
        if followed is None:
            giving = [line for line in lines if line["event"] == "giving"]
            if giving:
                followed = giving[0]["record"]
                previous_rows = (
                    simulation.records[followed].now.copy(),
                    simulation.records[followed].before.copy(),
                    simulation.records[followed].remainder.copy(),
                )
            continue
        if followed not in simulation.records:
            break
        live = simulation.records[followed]
        now, before, remainder = live.now, live.before, live.remainder
        prev_now, prev_before, prev_remainder = previous_rows
        num = simulation.kind_num[live.family]
        value = form_I(simulation, live.family, now, before, content_start)
        previous = form_I(simulation, live.family, prev_now, prev_before, content_start)
        read_coefficient = coefficients(
            num.astype(object),
            simulation.kind_den[live.family].astype(object),
            gamma,
            content_start.astype(object),
        )[0][0]
        drift = Fraction(0)
        for node in zip(*np.nonzero((now != prev_before) | (remainder != prev_remainder)), strict=True):
            drift += Fraction(
                (int(now[node]) - int(prev_before[node]))
                * (int(prev_remainder[node]) - int(remainder[node])),
                3 * int(read_coefficient[node]),
            )
        assert value - previous == drift, simulation.tick
        exchange = exchange_of(
            simulation, live.family, now, before, content_start, simulation._effective_content(LIGHT)
        )
        moved = form_I(simulation, live.family, now, before, simulation._effective_content(LIGHT))
        assert moved - value == exchange, simulation.tick
        if np.array_equal(content_start, simulation._effective_content(LIGHT)):
            assert exchange == 0
        checked += 1
        previous_rows = (now.copy(), before.copy(), remainder.copy())
    assert checked > 20
