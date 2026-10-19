"""Part H, the fix pass before the owner reads (both hands' lines of 2026-10-10 on the whole local trial, the advisor's 6092354791 and the mathematician's 6092368671, the Boss's merged list 6092388848). MUST 1: the null window's re-lay keeps the fold: `twist.relaid` with no direction named lays each Node of the region in the direction standing there, so the taker's twist and the source's fold (the lattice momentum given at a click) survive a body's null close instead of being discarded unbooked (one_photon's atom kept -32,040 only to its next close at 96 before). MUST 5: a region taker (the two slits' screens, bell's sides) takes no +p of its own, so it folds no source: the source is drawn and named, its outstanding count down by one, `recoil` reads "unpaid by the region" and `lost` "P lost to the region" (`twist.unpaid`, `lists.credited_node`), the body's P unchanged."""

import time

import numpy as np

from event_universe import act, emission, lists, node, readings, records, twist, world_files
from event_universe.core import paces
from event_universe.core.ports import arrival
from event_universe.features import phase
from event_universe.lattice import Lattice
from event_universe.reports import (
    LOST_TO_LAY,
    LOST_TO_REGION,
    LOST_TO_TAKER,
    THE_LAY,
    UNPAID_BY_REGION,
)
from event_universe.world_files import load_world
from tests import laws
from tests.laws import (
    COULOMB_CHAIN,
    COULOMB_UNIVERSE,
    EVENTS,
    GRAVITY,
    coulomb_world,
    d4_bound,
    emit_and_take_world,
    levels_floor,
    one_photon_board,
    world_beside,
)
from tests.laws import EMIT_RUN as RUN

ATOM_P = 33136  # one_photon's second atom at count 1 at the derived close, 61 (2026-10-19; 32,384 about the Node of the click at 76 under the declared 48): the quarter turn's reach about the hole's Node (C6), the most the two-Node taker takes of the +x piece booked over the window (C2, C4), one quantum's 2 T sin(pi / 4) within a few percent (C1)


def test_one_photons_atom_keeps_its_momentum_past_the_null_close(tmp_path, monkeypatch):
    """MUST 1 (the advisor's run): one_photon's second atom takes at 61 (the window derived from the packet's passage, 33 from the first lit interval 29; 76 at the declared 48 until 2026-10-19) with the quarter turn applied ("P lost to the taker"), its P_x ATOM_P (the +x piece about the hole's Node, C6); the first atom's window closes with no click at 62 and its re-lay keeps each Node's direction, the taker dark after the click under C1's one quantum: P_x at 61, 62, 63 and the run's end (170) all ATOM_P (before the fix 0 from the null close); printed."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board, lines = one_photon_board(tmp_path)
    atom = next(i for i, f in enumerate(board.families) if f.name == "atom")
    read = {}
    for _ in range(board.world.intervals):
        board.step()
        if board.interval in (61, 62, 63, board.world.intervals):
            read[board.interval] = twist.fan_momentum(board, atom)[0]
    credits = [c for c in lines if c["event"] == "credit" and c["label"] == "NODEDETECTOR"]
    assert len(credits) == 1 and credits[0]["interval"] == 61
    assert credits[0]["lost"] == [LOST_TO_TAKER, LOST_TO_LAY]
    end = board.world.intervals
    floor = levels_floor(board, atom, board.mask(board.credit.bodies[1].nodes))
    assert read[61] == ATOM_P
    assert all(abs(read[t] - ATOM_P) <= floor for t in (62, 63, end)), (read, floor)
    print(
        f"Part H (MUST 1): one_photon's atom P_x at 61 {read[61]}, at 62 {read[62]}, at 63 {read[63]}, "
        f"at the end ({end}) {read[end]}; the floor {floor}"
    )


def test_the_emit_and_take_world_conserves_p_past_the_emitters_null_close(tmp_path, monkeypatch):
    """MUST 1, Part G's world with the emitter's window SHORTER than the run (48 against 200, Part G's 240 hid the loss): body 0 emits at 61 and body 1 takes at 169 with the two receivers (its null close at 121 before it); the emitter, released from its own source at the span's end on this periodic chain (C5's reach by the lay's end, 2026-10-19: the lay has no end on the ring, so the first line stands), is lit by its own circulating train and closes a null window on it at 156, after the emission and before the click, its re-lay keeping its P; P over the board and the two bodies is still conserved to the floor at the run's end; the reversal with the books MATCHes over 200; the integers printed."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    path = emit_and_take_world(tmp_path, list(range(6)), list(range(12, 18)), window=48)
    board = Lattice(load_world(path), (lines := []).append)
    atom = next(i for i, f in enumerate(board.families) if f.name == "atom")
    light = next(i for i, f in enumerate(board.families) if f.name == "pulse")
    before, after, floor = None, None, None
    for _ in range(RUN):
        if not any(c["event"] == "credit" for c in lines):
            before = twist.fan_momentum(board, light)[0] + twist.fan_momentum(board, atom)[0]
        board.step()
        taken = [c for c in lines if c["event"] == "credit" and c["absorbed"] == "pulse"]
        if taken and after is None and not board.credit.fronts and board.credit.counts[light] == 0:
            after = (
                board.interval,
                twist.fan_momentum(board, light)[0],
                twist.fan_momentum(board, atom)[0],
            )
            at = np.zeros(board.shape, dtype=bool)
            for books in board.credit.bodies:
                at |= board.mask(books.nodes)
            floor = levels_floor(board, atom, at) + 2
    taken = [c for c in lines if c["event"] == "credit" and c["absorbed"] == "pulse"]
    assert len(taken) == 1 and taken[0]["source"] == "body 0" and taken[0]["lost"] is None
    click = taken[0]["interval"]
    closes = [b.windows for b in board.credit.bodies]
    assert closes == [
        1,
        2,
    ]  # C2: the emitter's one window, lit after its source ended, the taker's null and its click
    assert before == 0 and after is not None and floor is not None
    end = (twist.fan_momentum(board, light)[0], twist.fan_momentum(board, atom)[0])
    assert abs(after[1] + after[2] - before) <= floor, (before, after, floor)
    assert abs(end[0] + end[1] - before) <= floor, (before, end, floor)
    print(
        f"Part H (MUST 1, the shorter window): the click at {click}, p = {taken[0]['momentum']}, recoil {taken[0]['recoil']}; "
        f"P before the emission {before}, after the front passed (interval {after[0]}) the light's {after[1]} and the "
        f"two bodies' {after[2]}, the total {after[1] + after[2]}; the bodies' windows closed {closes} times; "
        f"at the run's end ({RUN}) the light's {end[0]} and the bodies' {end[1]}, the total "
        f"{end[0] + end[1]}; the floor {floor}"
    )


def test_the_emit_and_take_world_with_the_shorter_window_runs_back(tmp_path, monkeypatch):
    """MUST 1, the reversal: the same world with the emitter's window 48, RUN intervals forward and back with the books, MATCH; its own test so that each half runs under the suite's bound."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    started = time.perf_counter()
    path = emit_and_take_world(tmp_path, list(range(6)), list(range(12, 18)), window=48)
    verdict = laws.BACK.verdict(Lattice(load_world(path)), RUN)
    assert verdict["verdict"] == "MATCH", verdict
    print(
        f"Part H (MUST 1, the shorter window): {RUN} forward and back: MATCH; {time.perf_counter() - started:.1f} s"
    )


def region_takes_world(tmp_path):  # type: ignore[no-untyped-def]
    """The resonance world rewritten beside tmp_path: body 0 the emitter on six Nodes (excited, [2, 3], lifetime 48, its window 48), body 1 dropped, and the declared region `counter` over every other Node of the chain of 48 (the chain's complement of the body, as shelved_ion's counter is the board's: a region a pulse passes through books no net inflow), the world's draw at the window 48."""

    def edit(world):  # type: ignore[no-untyped-def]
        world["intervals"] = RUN
        world["bodies"][0]["nodes"] = [{"node": [x, 0, 0], "weight": 1} for x in range(6)]
        world["bodies"][0]["node_detector"]["window"] = 48
        del world["bodies"][1]
        world["node_detectors"] = [{"name": "counter", "positions": [[x, 0, 0] for x in range(6, 48)]}]
        world["draw"] = {
            "window": 48,
            "seed": 24,
            "multiplier": 6364136223846793005,
            "increment": 1442695040888963407,
        }

    return world_beside(tmp_path, EVENTS / "resonance" / "resonant.json", edit)


def test_a_region_taker_names_the_source_and_folds_nothing(tmp_path, monkeypatch):
    """MUST 5: a body's light credited by a declared region: the credit line's `source` names body 0, `recoil` reads "unpaid by the region", `lost` ["P lost to the region"], the emitter's outstanding count down by one, and the body's P_x unchanged across the region's click (nothing folded); printed."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = Lattice(load_world(region_takes_world(tmp_path)), (lines := []).append)
    atom = next(i for i, f in enumerate(board.families) if f.name == "atom")
    light = next(i for i, f in enumerate(board.families) if f.name == "pulse")
    giver = board.credit.bodies[0]
    weight = board.families[atom].pair[0]
    read = {}
    for _ in range(RUN):
        board.step()
        read[board.interval] = readings.momentum_of(
            weight, board.lines_of(atom, giver.record), board.wrap
        )[0]
    credits = [c for c in lines if c["event"] == "credit" and c["label"] == "NODEDETECTOR"]
    region = [c for c in credits if c["node_detector"] == "counter"]
    assert len(region) == 1 and region[0]["family"] == "pulse"
    click = region[0]
    assert click["source"] == "body 0" and click["recoil"] == UNPAID_BY_REGION
    assert click["lost"] == [LOST_TO_REGION] and click["momentum"][0] != 0
    assert board.credit.emitters[light][0].outstanding == 0
    t = click["interval"]
    assert read[t - 1] == read[t] == read[t + 1], (read[t - 1], read[t], read[t + 1])
    print(
        f"Part H (MUST 5): the region takes at {t}: p = {click['momentum']}, source {click['source']}, "
        f"recoil {click['recoil']!r}, lost {click['lost']}; the body's P_x at {t - 1}, {t}, {t + 1}: "
        f"{read[t - 1]}, {read[t]}, {read[t + 1]} (unchanged); the emitter's outstanding count 0"
    )


def test_the_links_count_carries_each_ends_clock_and_is_plain_at_the_vacuum(tmp_path, monkeypatch):
    """MUST 3 (the mathematician's 1, the advisor's 4): `node.phased` counts n_ij per end, rounded(L(i) p_0(i), Gamma) - rounded(L(j) p_0(j), Gamma), the reader's clock at each end in one coefficient rounding (`paces.turn_factor`, kind D); at the vacuum's clock the count is L(i) - L(j) bit for bit. The Coulomb world (Part C) with a holder of the content added and the charged plane reading it: the holder's time level the ramp L = x; with the content at 0 the counts along x are -1 per Link (the ramp's difference), and with a uniform level 600 held on the content's row the clock p_0 falls below Gamma and the counts are the two ends' turn factors' difference, not the plain difference, read against the formula at every Link, and one named Link whose count with the factor differs from the plain count (the RE-CHECK's SHOULD: 38 of 399 Links on the ramp count 0 against the plain -1; the first of them asserted and printed with both counts); the two-clock closure itself is an identity from the form (theorem, both hands' RE-CHECK), its integer number on V2 OPEN: not rerun here."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    universe = {
        "integers": COULOMB_UNIVERSE["integers"],
        "families": [
            GRAVITY,
            COULOMB_UNIVERSE["families"][0],
            dict(COULOMB_UNIVERSE["families"][1], reads={"gravity": 1, "charge": 1}),
        ],
    }
    monkeypatch.setattr(laws, "COULOMB_UNIVERSE", universe)
    board = Lattice(load_world(coulomb_world(tmp_path)))
    gravity, charge, charged = (
        next(i for i, f in enumerate(board.families) if f.name == name)
        for name in ("gravity", "charge", "charged")
    )
    gamma = board.world.node_clock
    level = np.arange(COULOMB_CHAIN).reshape(board.shape).astype(board.kind)
    line = board.states[charge].lines[0]
    board.states[charge].lines[0] = records.Record(level, level.copy(), line.remainder)
    found = {}
    for content in (0, 600):
        row = board.states[gravity].lines[0]
        uniform = np.full(board.shape, content, dtype=board.kind)
        board.states[gravity].lines[0] = records.Record(uniform, uniform.copy(), row.remainder)
        rows = node.phased(charge, board.families, board.states, 1, board.wrap, gamma)
        angles = node.turning(charged, board.families, board.states, 1, 0)
        assert angles is not None
        potential = np.asarray(angles[0], dtype=object)
        clock = node.rulers(charged, board.families, board.states, 1, board.wrap, gamma, 0)[0]
        clocked = paces.turn_factor(potential, clock, gamma)
        plain = np.where(
            arrival(np.ones_like(potential), 0, 1, board.wrap) == 0,
            0,
            potential - arrival(potential, 0, 1, board.wrap),
        )
        count = np.where(
            arrival(np.ones_like(clocked), 0, 1, board.wrap) == 0,
            0,
            clocked - arrival(clocked, 0, 1, board.wrap),
        )
        row_index = next(
            r
            for r in range(len(board.states[charge].phases))
            if r != 0 and rows[r] is not board.states[charge].phases[r]
        )
        cosine, sine = (
            board.states[charge].phases[row_index][0],
            board.states[charge].phases[row_index][1],
        )
        expected = phase.iterate(
            ((cosine.now, cosine.before, cosine.remainder), (sine.now, sine.before, sine.remainder)),
            count,
            gamma,
            1,
        )
        for got, want in zip(rows[row_index][:2], expected, strict=True):
            assert all(
                np.array_equal(np.asarray(getattr(got, k)), np.asarray(w))
                for k, w in zip(("now", "before", "remainder"), want, strict=True)
            )
        p_0 = int(np.asarray(clock).reshape(-1)[0]) if np.ndim(clock) else int(clock)
        counts, plains = count.reshape(-1), plain.reshape(-1)
        differing = [k for k in range(len(counts)) if counts[k] != plains[k]]
        found[content] = (
            p_0,
            int(counts[100]),
            int(plains[100]),
            int(clocked.reshape(-1)[100]),
            int(potential.reshape(-1)[100]),
            differing,
        )
    assert (
        found[0][0] == gamma and found[0][1] == found[0][2] == -1
    )  # the vacuum: L(i) - L(j), the ramp's -1
    assert (
        found[600][0] < gamma and found[600][3] != found[600][4]
    )  # the level scaled by p_0 / Gamma per end
    assert found[0][5] == []  # at the vacuum's clock no Link's count differs from the plain
    differing = found[600][5]
    first = differing[0]
    link = (first, int(count.reshape(-1)[first]), int(plain.reshape(-1)[first]))
    assert (
        len(differing) == 38 and link[1] != link[2]
    )  # one named Link: the factor's count against the plain
    print(
        f"Part H (MUST 3): the Link's count on the ramp L = x: at the content 0 the clock p_0 = {found[0][0]} = Gamma and n = {found[0][1]} (plain {found[0][2]}); "
        f"at the uniform level 600 the clock p_0 = {found[600][0]}, the end's turn factor at the Node 100 {found[600][3]} against its level {found[600][4]}, "
        f"n = {found[600][1]} (plain {found[600][2]}); {len(differing)} of {sum(1 for p in plain.reshape(-1) if p != 0)} Links differ from the plain count, the first the Link at the index {link[0]}: "
        f"n = {link[1]} against the plain {link[2]}; the phase pairs after the act equal the formula's at every Node; the closure an identity from the form, its integer on V2 not rerun, OPEN"
    )


def test_the_files_lay_is_an_entry_in_the_emitters_draw(tmp_path, monkeypatch):
    """The hands' SHOULD: the file's lay enters the emitters' book at the books' start with the laid count (`credit.Books.of`, `emission.registered` with no body), so a laid light beside an emitter is drawn between the body and the lay by their counts. one_photon: the photon's book holds the lay alone with the laid count, and its click at 61 (the derived window) draws the lay (`source` the lay, the count down by one, the board the Part G test's). The emit-and-take world: after body 0's emission the book holds body 0 at 1; the file's lay of one quantum entered beside it, the draw's weights read [1, 1] through `twist.drawn_emitter`."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board, lines = one_photon_board(tmp_path)
    photon = next(i for i, f in enumerate(board.families) if f.name == "photon")
    laid = board.credit.counts[photon]
    assert board.credit.emitters[photon] == [emission.Emitter(None, laid, False)] and laid >= 1
    for _ in range(61):
        board.step()
    click = next(c for c in lines if c["event"] == "credit")
    assert click["source"] == THE_LAY and click["lost"] == [LOST_TO_TAKER, LOST_TO_LAY]
    assert board.credit.emitters[photon][0].outstanding == laid - 1
    path = emit_and_take_world(tmp_path, list(range(6)), list(range(12, 18)), window=240)
    board = Lattice(load_world(path), (lines := []).append)
    light = next(i for i, f in enumerate(board.families) if f.name == "pulse")
    assert light not in board.credit.emitters  # nothing laid by the file
    while not any(c["event"] == "credit" and c["emitted"] == "pulse" for c in lines):
        board.step()
    assert board.credit.emitters[light] == [emission.Emitter(0, 1, False)]
    emission.registered(board.credit.emitters, light, None, False, 1)  # the file's lay of one quantum
    weights: list[list[int]] = []

    def pick(found: list[int]) -> int:
        weights.append(list(found))
        return 1

    drawn = twist.drawn_emitter(board, light, pick)
    assert weights == [[1, 1]] and drawn is not None and drawn.body is None and drawn.outstanding == 0
    print(
        f"Part H (SHOULD, the lay in the draw): one_photon's book at the start [the lay, {laid}], at 61 source {click['source']!r} and the lay's count {laid - 1}; "
        f"the emit-and-take world at the emission ({board.interval}): body 0 at 1 beside the lay's 1, the draw's weights {weights[0]}"
    )


def test_the_twisted_taker_keeps_its_momentum_through_its_emissions_re_lay(tmp_path, monkeypatch):
    """C3, the recoil per Node (the spec's blind: the taker's P kept through the emission within the re-lay's rounding bound, D4): the emit-and-take chain with the taker declaring the giver's rate too; the taker takes the pulse at 361 (its own rate's draws advance its generator, so it takes later than the rateless taker's 169; the interval pinned to the generator's sequence, as the other pins are) and the write twists it by the piece, 42,839 less the shortfall 7 booked per axis on the credit line (`shortfall`, C3); an emission is then given to it through the one act (`lists.emission`, one alternative, no draw): its parts are re-laid each Node in its own direction, the part the quantum enters in the leaving part's own at that Node, so the phase gradient the twist wrote survives the exchange and the taker's own P (its record's terms over its Nodes, `readings.momentum_of`) is kept within D4's bound (`d4_bound`: one level's change per line and Node, SUM over the body's axis-Links of |now_i| + |before_i| + |now_j| + |before_j| + 2, in T's unit; `levels_floor`, Part F's floor over the body's Nodes, read beside it), the count moved e to g and the pulse laid as a source in time; with one direction laid at every Node, the engine before C3, the gradient was erased and the P fell to the rounding."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)

    def edit(world):  # type: ignore[no-untyped-def]
        world["intervals"] = 2 * RUN
        world["bodies"][0]["nodes"] = [{"node": [x, 0, 0], "weight": 1} for x in range(6)]
        world["bodies"][1]["nodes"] = [{"node": [x, 0, 0], "weight": 1} for x in range(12, 18)]
        world["bodies"][0]["node_detector"]["window"] = 240
        world["bodies"][1]["node_detector"]["window"] = 48
        world["bodies"][1]["rates"] = world["bodies"][0]["rates"]  # the taker emits as the giver does

    board = Lattice(
        load_world(world_beside(tmp_path, EVENTS / "resonance" / "resonant.json", edit)),
        (lines := []).append,
    )
    while not any(c["event"] == "credit" and c["absorbed"] for c in lines):
        board.step()
    taker = board.credit.bodies[1]
    atom, weight, at = taker.index, board.families[taker.index].pair[0], board.mask(taker.nodes)

    def own() -> int:  # the taker's own P_x: its record's momentum terms over its Nodes, in T's unit
        read = readings.momentum_of(weight, board.lines_of(atom, taker.record), board.wrap, at)
        return twist.scaled(read, weight)[0]

    click = next(c for c in lines if c["event"] == "credit" and c["absorbed"])
    before, floor, bound = own(), levels_floor(board, atom, at), d4_bound(board, atom, taker.nodes)[0]
    assert (click["interval"], click["node_detector"], click["momentum"]) == (
        361,
        "body 1",
        [42839, 0, 0],
    )
    assert click["shortfall"] == [7, 0, 0] and click["lost"] is None and before == 42839 - 7
    rate = next(r for r in taker.declared.rates if r.leaves == taker.part)
    act.click(board, taker, None, [lists.emission(board, taker, rate, 1)[0]])  # the emission given
    after = own()
    assert (
        taker.counts == [1, 0] and board.credit.sources and abs(after - before) <= min(floor, bound)
    ), (
        before,
        after,
        floor,
        bound,
    )
    print(
        f"C3: the taker's P_x {before} at its click, {after} after its emission's re-lay; D4's bound {bound}, the floor {floor}"
    )
