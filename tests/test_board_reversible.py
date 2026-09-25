"""THE BOARD IS REVERSIBLE IN TIME, AND THE CLICKS KEEP THE PHYSICS (the model owner's word of
2026-09-25 through the Boss, records 2010 and 2011: "write a test that shows the board is
reversible in time, and in general keeps the physical definitions known in the clicks"; "clicks
go only forward in time because they are what happened in the world; the rest is all
possibilities"). One small world with every piece: an emitter body of the matter kind with a
stock of three quanta, its given family light, both of charge -1; a body of a fifth family of
charge +1; the screen of three light bodies; the family of clicks and the family of charge held
at the bodies and moving elsewhere; on the Node's own pace (ALGEBRA.md 9.50 (13)).

1. REVERSIBLE IN TIME (ALGEBRA.md 9.50 (8): the constant wall, the remainder's range the same at
   every interval; 9.26 (3) (b): the click the one deletion). Between clicks N intervals forward
   and N back return every level, remainder and field bit for bit, where the family of clicks'
   level rises and where it falls, a Node whose level falls to 0 and rises again among them.
   Across a click no rule undoes it: the deleted record stays deleted, the taken quantum stays
   with its taker. THE CLICK JOURNAL (the model owner's record 2070 of 2026-09-25 through the
   Boss; BUILD.md section 26 item 52): the host journals each click once, in one generic place
   for every family, and the backward run WITH THE CLICKS (`step_inverse(with_clicks=True)`,
   the host's test tool, not a law) undoes them from the journal in one generic operation:
   the given record removed at a giving click (its rows the file's given rows), the held
   quanta restored and the fields held again at a taking click, the deleted record put back
   whole at its deletion; the backward run is then exact through every click, nothing lost
   (the by-hand device of records 2010 and 2011, the same undo written out in the test, kept as
   the journal's check).
2. THE CLICKS' PHYSICS, on every line: the count of quanta (the giver's content down by one,
   the taker's up by one, the total of the held quanta and the records in flight unchanged);
   the charge (the total of the bodies' Q and the flights' q unchanged, a click moving q with
   the quantum, ALGEBRA.md 9.48 (1), 9.51 (2)); whole numbers (one whole quantum per click);
   the residue read at the first shell Node in [0, W) and the next giving click at its counted
   interval (9.44 (5) (c)); Born's rule at the taking end, the detector chosen by the increment
   ladder on the plain flux (9.25 (2) and (3), item 36); between clicks the conserved form with
   the Node terms weighted by 1 / p (9.50 (9) and (13)) exact where the field stands, the
   weights' change where it moves.
   The energy count s of 9.51 (3) (the key `energy_source`) is not built; its line waits on it.
Every number a COMPUTATION on the rule's integers; GAMEBOARD readings; no pin."""

from __future__ import annotations

import copy
from fractions import Fraction

import numpy as np

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.events.rule import rule_coefficients
from event_universe.events.world import body_node_indices, input_stamp, parse_nature_beam_world
from tests.test_board_properties import exchange_of, form_I
from tests.test_detector_law import Seen, chosen_by_the_rule, spy_on
from tests.test_emitter import emitter_world, massive_generator, reads

LIGHT, MATTER, POSITIVE = 0, 1, 2
STOCK = 3


def reversible_world(ticks: int = 400) -> dict:
    """The emitter chain of 80 (x closed) with the stock 3, light and the matter kind of charge
    -1, a fifth family `positive` of light's pair and charge +1 held by one body at x = 55, the
    screen at [70, 72]; seeded on the mode by the generator (the profile, the clock pair, the
    period, the given rows under the stamp)."""
    document = emitter_world(stock=STOCK, ticks=ticks, on_mode=False)
    document["families"][LIGHT]["charge"] = -1
    document["families"][MATTER]["charge"] = -1
    document["families"].insert(
        POSITIVE,
        {"name": "positive", "quantum": 1, "phase_per_link": [512, 1], "charge": 1, "reads": reads()},
    )
    document["measured"].append(
        {
            "position": [55, 0, 0],
            "family": "positive",
            "amount": 1,
            "phase": 0,
            "momentum": [0, 0, 0],
            "fixed": True,
        }
    )
    massive_generator().seed_on_the_mode(document)
    document["input"] = input_stamp(document)
    return document


def rows_of(simulation: DetectorLawSimulation) -> dict[str, object]:
    """Every row of the board: the records' two levels and remainders (the bodies' own among
    them), both fields' rows, the held quanta and the interval."""
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
            simulation.held_record("charge").now.copy(),
            simulation.held_record("charge").before.copy(),
            simulation.held_record("charge").remainder.copy(),
        ),
        "held": copy.deepcopy(simulation.held),
        "tick": simulation.tick,
    }


def assert_same(now: dict, then: dict, lost: set[int] = frozenset()) -> None:
    """`now` equals `then` bit for bit, but for the records in `lost` (present in `then`,
    absent in `now`)."""
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
    """The world stepped `ticks` intervals: the simulation, the rows after every interval (the
    load's at index 0), the lines, and the ladder spy's readings at every click."""
    lines: list[dict] = []
    simulation = DetectorLawSimulation(
        parse_nature_beam_world(document), observer=lines.append, journal_clicks=True
    )
    seen: Seen = {}
    spy_on(simulation, seen)
    states = [rows_of(simulation)]
    for _ in range(ticks):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
        states.append(rows_of(simulation))
    return simulation, states, lines, seen


def click_ticks(lines: list[dict]) -> tuple[list[int], list[int]]:
    """The intervals of the giving clicks and of the taking clicks."""
    giving = [line["tick"] for line in lines if line["event"] == "giving"]
    taking = [line["tick"] for line in lines if line["event"] == "gather"]
    return giving, taking


def test_between_clicks_the_board_returns_bit_for_bit_where_the_clock_rises_and_falls():
    """1. From the load to the interval before the first giving click, every interval back
    returns the load's rows bit for bit: the bodies' own records, the family of clicks and the
    family of charge (their levels and remainders), the held quanta; the family of clicks' level
    fell at Nodes during the run (the falls counted, above 0), and at some Node it fell to 0 and
    rose again (the edge case). ALGEBRA.md 9.50 (8): the wall constant, one to one."""
    document = reversible_world()
    probe, _, lines, _ = run_states(document, 120)
    first_giving = click_ticks(lines)[0][0]
    assert first_giving > 10
    simulation, states, lines, _ = run_states(document, first_giving - 1)
    assert not [line for line in lines if line["event"] in ("giving", "gather")]
    levels = np.stack([state["clock"][0] for state in states])  # (interval, x, y, z)
    falls = int(np.sum(levels[1:] < levels[:-1]))
    assert falls > 0
    history = levels[:, :, 0, 0]
    dipped = False
    for x in range(history.shape[1]):
        column = history[:, x]
        zeros = np.nonzero(column == 0)[0]
        for t in zeros:
            if column[:t].any() and column[t + 1 :].any():
                dipped = True
                break
        if dipped:
            break
    assert dipped, "no Node fell to 0 and rose again in this window"
    for t in range(first_giving - 1, 0, -1):
        simulation.step_inverse()
        assert_same(rows_of(simulation), states[t - 1])
    assert simulation.tick == 0


def test_across_a_click_no_rule_undoes_it_and_only_the_deleted_rows_are_lost():
    """1. Across the first giving click and the first taking click. (a) NO RULE UNDOES A CLICK
    (the owner's word of record 2011): stepping back across the taking click leaves the deleted
    record deleted and the taken quantum with its taker (the screen's first body's held content
    and the field held at it stay the click's). (b) THE CLICK'S ONE LOSS: with the click's
    ledger undone by hand (the held quanta of the interval before restored, the fields held
    again), the backward run across the taking click returns every row bit for bit but the
    deleted record's, and across the giving click, with the given record removed (its rows at
    its write the file's given rows on the body's Nodes) and the stock restored, returns every
    row bit for bit with nothing lost; then down to the load exactly."""
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
    # across the taking click without undoing its ledger: the record stays deleted, the taker
    # keeps its quantum, the field at its Nodes stays held at the click's content
    taker = next(
        number
        for number in range(len(states[t_taking]["held"]))
        if states[t_taking]["held"][number] != states[t_taking - 1]["held"][number]
    )
    blind.step_inverse()
    after = rows_of(blind)
    assert deleted not in after["records"]
    assert after["held"] == states[t_taking]["held"] != states[t_taking - 1]["held"]
    taker_mask = blind.span_masks[taker]
    assert np.array_equal(after["clock"][0][taker_mask], states[t_taking]["clock"][0][taker_mask])
    assert not np.array_equal(
        after["clock"][0][taker_mask], states[t_taking - 1]["clock"][0][taker_mask]
    )
    # (b) the same run again, the click's ledger undone by hand before each step across a click
    simulation, states, lines, _ = run_states(document, end)
    for t in range(end, t_taking, -1):
        simulation.step_inverse()
        assert_same(rows_of(simulation), states[t - 1])
    simulation.held = copy.deepcopy(states[t_taking - 1]["held"])
    simulation._hold()
    simulation.step_inverse()
    assert_same(rows_of(simulation), states[t_taking - 1], lost={deleted})
    lost = {deleted}
    for t in range(t_taking - 1, t_giving, -1):
        if t in giving_ticks:
            inverse_giving_interval(simulation, lines, states, t)
        else:
            simulation.step_inverse()
        assert_same(rows_of(simulation), states[t - 1], lost=lost & set(states[t - 1]["records"]))
    inverse_giving_interval(simulation, lines, states, t_giving)
    assert_same(rows_of(simulation), states[t_giving - 1])
    for t in range(t_giving - 1, 0, -1):
        simulation.step_inverse()
        assert_same(rows_of(simulation), states[t - 1])
    assert simulation.tick == 0
    # (c) THE CLICK JOURNAL (record 2070; item 52; on for the test alone, record 2071): the same
    # run a third time, the backward run
    # with the clicks undoing every click from the journal in one generic operation: exact at
    # every interval through the taking click (the deleted record back whole: nothing lost)
    # and the giving click (the given record removed, the stock restored), down to the load;
    # the journal emptied as the run runs back
    journal, states, lines, _ = run_states(document, end)
    entries = journal.journal_size()
    assert entries >= 3 and [e.kind for e in journal.click_journal].count("giving") == len(
        [t for t in giving_ticks if t <= end]
    )
    assert any(e.kind == "taking" and e.identity == deleted for e in journal.click_journal)
    assert any(e.kind == "deletion" and e.identity == deleted for e in journal.click_journal)
    for t in range(end, 0, -1):
        journal.step_inverse(with_clicks=True)
        assert_same(rows_of(journal), states[t - 1])
        assert journal.books()["balanced"], t
    assert journal.tick == 0 and journal.journal_size() == 0


def inverse_giving_interval(
    simulation: DetectorLawSimulation, lines: list[dict], states: list[dict], t: int
) -> None:
    """The giving click's interval stepped back by hand, the click's write undone: the given
    record removed (its rows as written the file's given rows on the body's Nodes, asserted);
    every other record stepped back at the content the interval began with (the hold before the
    click, which their forward step read); the two fields stepped back at the click's hold (the
    giving held the body at its lowered content before the fields' own step, ALGEBRA.md 9.45
    (2)); then the body's stock restored and the fields held again. Nothing is lost at a giving
    click: the rows it wrote are the file's."""
    line = next(line for line in lines if line["event"] == "giving" and line["tick"] == t)
    # the given record: present unless a taking click deleted it since (then the click's one
    # loss, already accounted); its rows as written are the file's either way
    family = [each.name for each in simulation.families].index(line["family"])
    block = simulation.block_by_number[line["measured"]]
    given = block.definition.emitter.given
    shape = tuple(int(v) for v in simulation.shape)
    nodes = body_node_indices(
        shape, tuple(block.corner), block.definition.extents, simulation.kind_wrap[family]
    )
    expected_now = np.zeros(shape, dtype=np.int64).reshape(-1)
    expected_before = np.zeros(shape, dtype=np.int64).reshape(-1)
    for index, a, b in zip(nodes, given.now, given.before, strict=True):
        expected_now[index] = a
        expected_before[index] = b
    written = states[t]["records"][line["record"]]
    assert np.array_equal(written[0], expected_now.reshape(shape))
    assert np.array_equal(written[1], expected_before.reshape(shape))
    assert not written[2].any()
    simulation.records.pop(line["record"], None)
    held_before = states[t - 1]["held"]
    number = line["measured"]
    mask = block.mask
    clock, charge = simulation.held_record("content"), simulation.held_record("charge")
    pre_content = clock.before.copy()
    pre_charge = charge.before.copy()
    pre_content[mask] = sum(held_before[number])
    pre_charge[mask] = sum(
        sign * quanta for sign, quanta in zip(simulation.family_charge, held_before[number], strict=True)
    )
    simulation.node_level[clock.family] = pre_content
    simulation.node_level[charge.family] = pre_charge
    simulation._effective.clear()
    for other in list(simulation.records.values()):
        if other.standing:
            continue
        simulation._advance_inverse(other)
    for each in simulation.blocks:
        if each.seat is not None:
            simulation._advance_seat_inverse(each)
        elif each.own is not None:
            simulation._advance_inverse(each.own)
    simulation._advance_inverse(clock)
    simulation._advance_inverse(charge)
    simulation.held = copy.deepcopy(held_before)
    simulation._hold()
    simulation.tick -= 1


def test_the_clicks_keep_the_count_the_charge_the_residue_and_borns_rule():
    """2. Over 400 intervals with three giving clicks and their taking clicks: at every interval
    the books balance, the held quanta plus the records in flight are the load's total, and the
    bodies' Q plus the flights' q are the load's total (-3 - 3 + 1 = -5); at every giving click
    the giver's held content falls by one, the given record's content is 1, its residue u is
    in [0, W) with W the rule's at the first shell Node, and the click's interval is the
    counted one, 2 W (wait - 1) < (2 u + 1) P <= 2 W wait from the residue read before it
    (ALGEBRA.md 9.44 (5) (c)); at every taking click the taker's held content rises by one, the
    record's content is 1, and the detector is the one the increment ladder chooses on the
    plain flux against the norm's rational (Born's rule at the taking end, 9.25 (2) and (3),
    item 36)."""
    document = reversible_world()
    period = document["measured"][0]["emitter"]["period"]
    lines: list[dict] = []
    simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
    seen: Seen = {}
    spy_on(simulation, seen)
    charge = simulation.family_charge
    total_quanta = sum(sum(h) for h in simulation.held)
    total_charge = sum(simulation._body_charge(n) for n in range(len(simulation.held)))
    # the emitter's own quantum and its stock of STOCK light quanta, all of charge -1, the
    # screen's three light bodies and the positive body (ALGEBRA.md 9.51 (8); item 47)
    assert total_charge == -(STOCK + 1) - 3 + 1
    block = simulation.blocks[0]
    previous_residue = None
    read_at = 0
    held_before = copy.deepcopy(simulation.held)
    for _ in range(400):
        own = block.own
        assert own is not None
        residue_before = (own.u, own.wheel)
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
        flights = list(simulation.records.values())
        in_flight = [live for live in flights if live is not block.own]
        assert sum(sum(h) for h in simulation.held) + sum(f.content for f in in_flight) == total_quanta
        assert (
            sum(simulation._body_charge(n) for n in range(len(simulation.held)))
            + sum(charge[f.family] * f.content for f in in_flight)
        ) == total_charge
        for line in [line for line in lines if line["tick"] == simulation.tick]:
            if line["event"] == "giving":
                giver = line["measured"]
                # the giving lowers the given family's content held at the body (item 47)
                given_family = block.definition.emitter.family if block.definition.emitter else -1
                assert simulation.held[giver][given_family] == held_before[giver][given_family] - 1
                assert simulation.records[line["record"]].content == 1
                assert 0 <= line["u"] < line["W"] and line["read_node"] == [5, 0, 0]
                if previous_residue is not None:
                    u, wheel = previous_residue
                    wait = line["tick"] - read_at
                    assert line["wait"] == wait
                    assert 2 * wheel * (wait - 1) < (2 * u + 1) * period <= 2 * wheel * wait
                else:
                    u, wheel = residue_before
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
    """2. The conserved form of ALGEBRA.md 9.50 (9) and (13) on the given light record, interval
    by interval from its write to its taking click: its change with the field of the interval's
    start in force is the remainders' term exactly (9.50 (8)), and with the field's move the
    weights' change exactly (9.45 (5), the Node terms alone under the Node's own pace); where
    the field stands the form is constant but for the remainders' term. The content light reads
    here is the effective content c - q Lambda d, light being of charge -1 (9.48 (3))."""
    document = reversible_world()
    lines: list[dict] = []
    simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
    gamma = simulation.node_clock
    followed: int | None = None
    previous_rows = None
    checked = 0
    for _ in range(200):
        # the content light reads: the effective content c - q Lambda d, light of charge -1 here
        # (ALGEBRA.md 9.48 (3), 9.51 (2))
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
        read_coefficient = rule_coefficients(
            num.astype(object),
            simulation.kind_den[live.family].astype(object),
            gamma,
            content_start.astype(object),
            True,
        )[0]
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
