"""THE FEED AND THE INDUCTION, their own folders (ALGEBRA.md #the-primitives, the rows "the feed" and "the induction"; #the-well): the fall toward content the same for every body, the contraction's vector and tensor parts, the induction's momentum part, the electric identity (a gradient of the time part and a rising vector part push alike), the inverse bit for bit with the remainders carried, the refusals, the declarations bound at (v), the fall on the board and its step back."""

from __future__ import annotations

import pytest

from event_universe.core.register import folder_of
from event_universe.core.rule3 import THE_ADVANCE, THE_INVERSE, THE_LOAD
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.features import feed, induction
from event_universe.features.feed import TENSOR_AXES, FeedFace, FeedOwn, FeedRead, FeedStart
from event_universe.features.induction import InductionOwn, InductionRead, InductionStart
from event_universe.world_files import input_stamp, parse_nature_beam_world
from tests.bodies import KIND, WELL, block_world

GAMMA = 1000
WALL = 3 * 7 * 65  # W = 3 Q M: a body of 65 quanta at the momentum unit 7
ZERO3 = (0, 0, 0)
ZERO6 = (0, 0, 0, 0, 0, 0)


def faces(minus: FeedRead, plus: FeedRead, nodes: int = 1) -> tuple[FeedFace, FeedFace]:
    return FeedFace((minus,), nodes), FeedFace((plus,), nodes)


def start(act, now, before, faces_x, distance=2, wall=WALL, faces_y=None) -> FeedStart:
    return FeedStart(act, now, before, wall, GAMMA, (faces_x, faces_y, None), (distance, distance, 1))


def induced(act, now, before, nodes, *reads) -> InductionStart:
    return InductionStart(act, now, before, WALL, GAMMA, nodes, reads)


def test_a_body_falls_toward_content_the_same_for_every_body_over_the_faces_distance():
    """The fall (ALGEBRA.md #the-well): a resting body between the time levels 400 behind and 460 ahead on x gets n_next = n_before + 2 W x 60 div (2 Gamma x 2), the remainder carried, the same whatever W; a block with 9-Node faces 4 Links apart the same per Node; a hill pushes away; no faces, no change."""
    for wall in (WALL, 5 * WALL):
        pair = faces(FeedRead(1, 400, ZERO3, ZERO6), FeedRead(1, 460, ZERO3, ZERO6))
        writes = feed.apply(start(THE_ADVANCE, (3, 5, 7), ZERO3, pair, wall=wall), FeedOwn({}))
        assert writes.momentum == (2 * wall * 60 // (2 * GAMMA * 2), 0, 0)
        assert writes.momentum_before == (3, 5, 7) and writes.contractions == ((400, 460), None, None)
        assert writes.own.carries[("feed", 0)] == 2 * wall * 60 % (2 * GAMMA * 2)
    block = faces(FeedRead(1, 9 * 400, ZERO3, ZERO6), FeedRead(1, 9 * 460, ZERO3, ZERO6), nodes=9)
    momentum = feed.apply(start(THE_ADVANCE, ZERO3, ZERO3, block, distance=4), FeedOwn({})).momentum
    assert momentum == (2 * WALL * 9 * 60 // (2 * GAMMA * 4 * 9), 0, 0)
    hill = faces(FeedRead(-1, 400, ZERO3, ZERO6), FeedRead(-1, 460, ZERO3, ZERO6))
    writes = feed.apply(start(THE_ADVANCE, ZERO3, ZERO3, hill), FeedOwn({}))
    assert writes.momentum[0] < 0 and writes.contractions[0] == (-400, -460)


def test_the_contraction_books_the_momentum_with_the_vector_and_tensor_parts_and_the_electric_identity():
    """A moving body (n = (300, -200, 0)) between faces with time, vector and tensor parts: the contraction f x [t - (n_b V_b) div W + (n_b n_c h_bc) div W^2] in Python integers (the off-diagonal pairs twice), the feed its difference; THE ELECTRIC IDENTITY: a time gradient of 120 over 2 Links and a vector part rising by 60 push alike, W x 60 per 2 Gamma per interval (the doubled term rounded once); a block of 27."""
    n = (300, -200, 0)
    minus = FeedRead(2, 500, (7, -11, 13), (1, 2, 3, -4, 5, -6))
    plus = FeedRead(2, 530, (-9, 17, 19), (2, -3, 4, 5, -6, 7))
    writes = feed.apply(start(THE_ADVANCE, n, n, faces(minus, plus)), FeedOwn({}))
    expected = []
    for read in (minus, plus):
        current = sum(n[b] * read.vector[b] for b in range(3))
        stress = sum(
            n[b] * n[c] * h * (1 if b == c else 2)
            for (b, c), h in zip(TENSOR_AXES, read.tensor, strict=True)
        )
        expected.append(
            read.factor * read.time - (read.factor * current) // WALL + (read.factor * stress) // WALL**2
        )
    assert writes.contractions[0] == tuple(expected)
    assert writes.momentum == (
        n[0] + 2 * WALL * (expected[1] - expected[0]) // (2 * GAMMA * 2),
        n[1],
        n[2],
    )
    gradient = faces(FeedRead(1, 0, ZERO3, ZERO6), FeedRead(1, 120, ZERO3, ZERO6))
    fed = feed.apply(start(THE_ADVANCE, ZERO3, ZERO3, gradient), FeedOwn({}))
    rising = induction.apply(
        induced(THE_ADVANCE, ZERO3, (1, 1, 1), 1, InductionRead(1, (60, 0, 0), ZERO3)), InductionOwn({})
    )
    push = WALL * 60 // (2 * GAMMA)
    assert fed.momentum == (2 * WALL * 60 // (2 * GAMMA), 0, 0) and rising.momentum == (push, 0, 0)
    assert rising.changes == (60, 0, 0) and rising.momentum_before == (push + 1, 1, 1)
    block = induction.apply(
        induced(THE_ADVANCE, ZERO3, ZERO3, 27, InductionRead(1, (27 * 60, 0, 0), ZERO3)),
        InductionOwn({}),
    )
    assert block.momentum == rising.momentum


def test_the_inverse_undoes_the_feed_and_the_induction_bit_for_bit_with_the_remainders():
    """Three intervals forward on changing faces and fields, then the same three backward in the reverse order: the two integers of momentum and every carry back at the start, the numerators recomputed."""
    readings = [
        (
            FeedRead(1, 400 + 7 * k, (3 * k, -k, 5), (k, 0, 1, 2, -k, 3)),
            FeedRead(-1, 390 - 5 * k, (k, 2 * k, -1), (0, k, 1, -2, k, 4)),
        )
        for k in range(3)
    ]
    own, now, before = FeedOwn({}), (250, -70, 40), (240, -60, 40)
    for minus, plus in readings:
        writes = feed.apply(
            start(THE_ADVANCE, now, before, faces(minus, plus), faces_y=faces(plus, minus)), own
        )
        own, now, before = writes.own, writes.momentum, writes.momentum_before
    assert (now, before) != ((250, -70, 40), (240, -60, 40)) and any(own.carries.values())
    for minus, plus in reversed(readings):
        writes = feed.apply(
            start(THE_INVERSE, now, before, faces(minus, plus), faces_y=faces(plus, minus)), own
        )
        own, now, before = writes.own, writes.momentum, writes.momentum_before
    assert (now, before) == ((250, -70, 40), (240, -60, 40)) and not any(own.carries.values())
    fields = [InductionRead(2, (30 * k, -k, 0), (30 * (k - 1), 1 - k, 0)) for k in range(1, 4)]
    own2, now, before = InductionOwn({}), (0, 9, -9), (1, 8, -9)
    for field in fields:
        writes = induction.apply(induced(THE_ADVANCE, now, before, 2, field), own2)
        own2, now, before = writes.own, writes.momentum, writes.momentum_before
    assert now != (0, 9, -9)
    for field in reversed(fields):
        writes = induction.apply(induced(THE_INVERSE, now, before, 2, field), own2)
        own2, now, before = writes.own, writes.momentum, writes.momentum_before
    assert (now, before) == ((0, 9, -9), (1, 8, -9)) and not any(own2.carries.values())


def test_the_refusals_by_name_and_the_declarations_the_loop_does_not_call_yet():
    pair = faces(FeedRead(1, 1, ZERO3, ZERO6), FeedRead(1, 2, ZERO3, ZERO6))
    with pytest.raises(ValueError, match="the feed's act is one of"):
        feed.apply(start(THE_LOAD, ZERO3, ZERO3, pair), FeedOwn({}))
    with pytest.raises(ValueError, match="stand 1 Links apart: from 2"):
        feed.apply(start(THE_ADVANCE, ZERO3, ZERO3, pair, distance=1), FeedOwn({}))
    with pytest.raises(ValueError, match="the same reads over the same count of Nodes"):
        feed.apply(start(THE_ADVANCE, ZERO3, ZERO3, (pair[0], FeedFace(pair[1].reads, 2))), FeedOwn({}))
    with pytest.raises(ValueError, match="wall W = 0 and clock"):
        feed.apply(start(THE_ADVANCE, ZERO3, ZERO3, pair, wall=0), FeedOwn({}))
    with pytest.raises(ValueError, match="the induction's act is one of"):
        induction.apply(induced(THE_LOAD, ZERO3, ZERO3, 1), InductionOwn({}))
    with pytest.raises(ValueError, match="count of Nodes N = 0 are from 1"):
        induction.apply(induced(THE_ADVANCE, ZERO3, ZERO3, 0), InductionOwn({}))
    for module, name, folder in ((feed, "the feed", "feed"), (induction, "the induction", "induction")):
        card = module.DECLARATION
        assert card.name == name and folder_of(name) == folder and card.place == "(v)"
        assert card.function is module.apply and card.built and card.word == "after the step"
        assert card.writes == ("a body's momentum n", "a body's remainders")


def test_bound_at_v_a_free_body_falls_toward_a_held_body_and_the_step_back_returns_it():
    """The binding (the owner's word of 09:37Z): on a periodic board a big body held in place (`fixed`) and a small free body 5 Links ahead on x; the feed reads the content's time part at the small body's faces once the field reaches them, so its momentum turns toward the big body (n = -2 on x by interval 10, the second level one interval behind, no hop), the held body is not fed; ten steps back return both levels, the drive and every remainder of the feed to the load's, bit for bit."""
    periodic = {"x": "periodic", "y": "periodic", "z": "periodic"}
    big = {
        "position": [2, 3, 3],
        "side": 2,
        "pair": WELL,
        "margin": "control",
        "amount": 400,
        "fixed": True,
    }
    small = {"position": [9, 3, 3], "side": 2, "pair": WELL, "margin": "control", "amount": 3}
    document = block_world([16, 8, 8], periodic, KIND, [big, small], ticks=12)
    for entry in document["universe"]:
        if "held" in entry:
            entry["held"] = {
                **entry["held"],
                "divisor": 1,
            }  # a copy: the field is the counts, the feed reads it
    document["stamp"] = input_stamp(document)
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    held, free = simulation.blocks
    for _ in range(10):
        simulation.step()
    # measured once under THE START (the held field at rest at the load, no transient) with no body held
    # in place (#1283): the free body -1 in ten intervals; the big body is fed from the first interval
    # too and moves away from the hole the small body's count makes in its field (the hold's write at a
    # body's Nodes is its count: a finding on #1198 for the owner, the law as written); -95 under the
    # certified rest (the levels at a half round up where the clamp's fixed point rounded down)
    # the free body falls toward the held body (negative x), |before| <= |now|; the held body is fed too
    assert free.momentum[0] < 0 and free.momentum[1:] == [0, 0] and free.momentum_before[1:] == [0, 0]
    assert abs(free.momentum_before[0]) <= abs(free.momentum[0]) and free.hold_carry[("feed", 0)] > 0
    assert held.momentum[0] < 0 and held.momentum[1:] == [0, 0]
    for _ in range(10):
        simulation.step_inverse()
    assert free.momentum == [0, 0, 0] == free.momentum_before
    assert all(value == 0 for key, value in free.hold_carry.items() if key[0] == "feed")
