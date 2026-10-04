def test_a_declared_windows_hazard_spans_its_lit_intervals_alone_and_the_dark_ones_their_own_grain(
    monkeypatch,
):
    """The emission's hazard over a declared window (ALGEBRA.md, The dark, step 4, and The click writes on the lattice (5), KNOWN, the rate drawn per window; A3 of the alignment audit, #1793 comment 5982140872, with the advisor's second, 5982171035 (2); `meeting.jumped`, `meeting.emitted`, `NodeBooks.lit`): the resonance world's giver, in e at the lifetime 48, its window set to W = 8, `dark` replaced by a schedule over the giver alone and `emitted` by a spy recording the span it is drawn at and emission nothing; (i) over a window whose intervals 2, 3 and 6 are dark, each dark interval draws at the span 1 as it passes and the close at the lit count 5, the spans summing to W = 8, every interval in exactly one draw's span; (ii) a window with no dark interval draws once, at its close, at the span W, the shipped behaviour bit for bit; (iii) a window whose close is dark draws the close at 1 and then its seven lit intervals at 7, the sum W again; the lit count and the elapsed count 0 again after every close."""
    from dataclasses import replace

    from event_universe import meeting
    from event_universe.lattice import Lattice
    from event_universe.world_files import load_world
    from tests.laws import EVENTS

    board = Lattice(load_world(EVENTS / "resonance" / "resonant.json"))
    giver = board.credit.bodies[0]
    assert giver.part == 1 and giver.declared.rates[0].lifetime == 48  # in e, the lifetime above W
    giver.declared = replace(giver.declared, draw=replace(giver.declared.draw, window=8))
    schedule = {(1, 2), (1, 3), (1, 6), (3, 8)}  # the (window, interval) pairs that are dark
    at, spans = {"window": 0}, []

    def dark(board, books):
        return books is giver and (at["window"], books.elapsed) in schedule

    def emitted(board, books, grain):
        if books is giver:
            spans.append((at["window"], books.elapsed, grain))
        return False

    monkeypatch.setattr(meeting, "dark", dark)
    monkeypatch.setattr(meeting, "gave", emitted)
    for at["window"] in (1, 2, 3):
        for _ in range(8):
            board.step()
        assert (giver.lit, giver.elapsed) == (0, 0)  # the counts begin again with the window
    drawn = {w: [(i, span) for v, i, span in spans if v == w] for w in (1, 2, 3)}
    for w, draws in drawn.items():
        print(f"window {w}: " + ", ".join(f"interval {i} span {span}" for i, span in draws))
    assert drawn[1] == [(2, 1), (3, 1), (6, 1), (8, 5)]  # the dark ones at 1, the close the lit count
    assert drawn[2] == [(8, 8)]  # no dark interval: the window's length, as shipped
    assert drawn[3] == [(8, 1), (8, 7)]  # a dark close: the interval, then the lit intervals
    assert all(sum(span for _i, span in draws) == 8 for draws in drawn.values())  # each interval once
