"""Part H, the fix pass before the owner reads (both hands' lines of 2026-10-10 on the whole local trial, the advisor's 6092354791 and the mathematician's 6092368671, the Boss's merged list 6092388848). MUST 1: the null window's re-lay keeps the fold: `take.relaid` with no direction named lays each Node of the region in the direction standing there, so the taker's twist and the source's fold (the lattice momentum given at a click) survive a body's null close instead of being discarded unbooked (one_photon's atom kept -32,040 only to its next close at 96 before). MUST 5: a region taker (the two slits' screens, bell's sides) takes no +p of its own, so it folds no source: the source is drawn and named, its outstanding count down by one, `recoil` reads "unpaid by the region" and `lost` "P lost to the region" (`take.unpaid`, `lists.credited_node`), the body's P unchanged (its test deleted 2026-10-20 with the twist's under the owner's rule, the reader's ruling: its sentence the write's booking at a region, its world's region read at the content 0 refused by the exact vacuum; the booking stands in the code until the twist round)."""

import numpy as np

from event_universe import emission, node, records, take, world_files
from event_universe.core import paces
from event_universe.core.ports import arrival
from event_universe.features import phase
from event_universe.lattice import Lattice
from event_universe.reports import (
    LOST_TO_LAY,
    LOST_TO_TAKER,
    THE_LAY,
)
from event_universe.world_files import load_world
from tests import laws
from tests.laws import (
    COULOMB_CHAIN,
    COULOMB_UNIVERSE,
    GRAVITY,
    coulomb_world,
)
from tests.laws_content import one_photon_board


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
        node.seed_phases(
            board, board.world
        )  # the pairs and the Node's phase row re-read from the state set by hand, so that the act is the first from rest (the centred count, 2026-10-23)
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
        fresh = records.phase_lines(
            board.families[charge], board.shape, board.kind, gamma, board.world.width.bit_length()
        )[
            row_index
        ]  # the seed at the angle 0: the pair after one act stands at the count's size from it (the centred count, 2026-10-23: the Link's count is the Node's reading, K after the first act from rest the clocked potentials' difference)
        cosine, sine = fresh[0], fresh[1]
        expected = phase.iterate(
            ((cosine.now, cosine.before, cosine.remainder), (sine.now, sine.before, sine.remainder)),
            np.abs(count),  # the pair at the count's size, read with the count's sign (2026-10-21)
            phase.unit(
                gamma
            ),  # the line's unit 2 Gamma, the half angle (the centred count, 2026-10-23; the former unit Gamma)
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
    """The hands' SHOULD: the file's lay enters the emitters' book at the books' start with the laid count (`credit.Books.of`, `emission.registered` with no body), so a laid light beside an emitter is drawn between the body and the lay by their counts. one_photon: the photon's book holds the lay alone with the laid count, and its click at 62 (the derived window, the first atom's read) draws the lay (`source` the lay, the count down by one, the board the Part G test's). The file's lay of one more quantum and a body's quantum entered beside it, the draw's weights read [1, 1] through `take.drawn_emitter` and the body's entry drawn. Re-pinned 2026-10-20 under the content: the first atom\'s click at 63 where it fell at 62."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board, lines = one_photon_board(tmp_path)
    photon = next(i for i, f in enumerate(board.families) if f.name == "photon")
    laid = board.credit.counts[photon]
    assert board.credit.emitters[photon] == [emission.Emitter(None, laid, False)] and laid >= 1
    while not [c for c in lines if c["event"] == "credit" and c["absorbed"]] and board.interval < 170:
        board.step()
    click = next(c for c in lines if c["event"] == "credit" and c["absorbed"])
    assert (
        click["interval"] == click["window"][1]
    )  # the click at the window's close, the window derived (60 here; 63 under the content at the declared window, 2026-10-20, 62 at the exact vacuum)
    assert click["source"] == THE_LAY and click["lost"] == [LOST_TO_TAKER, LOST_TO_LAY]
    assert board.credit.emitters[photon][0].outstanding == laid - 1
    emission.registered(
        board.credit.emitters, photon, None, False, 1
    )  # the file's lay of one more quantum
    emission.registered(board.credit.emitters, photon, 0, False, 1)  # a body's quantum beside the lay's
    weights: list[list[int]] = []

    def pick(found: list[int]) -> int:
        weights.append(list(found))
        return 1

    drawn = take.drawn_emitter(board, photon, pick)
    assert weights == [[laid, 1]] and drawn is not None and drawn.body == 0 and drawn.outstanding == 0
    print(
        f"Part H (SHOULD, the lay in the draw): one_photon's book at the start [the lay, {laid}], at {click['interval']} source {click['source']!r} and the lay's count {laid - 1}; "
        f"a body's quantum entered beside it, the draw's weights {weights[0]}"
    )
