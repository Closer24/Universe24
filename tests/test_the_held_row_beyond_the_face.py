def test_a_held_row_reads_its_own_level_beyond_an_open_face_and_the_content_never_falls_below_zero(
    monkeypatch,
):
    """F2 of the bug hunt (#1827 comment 5983321848; the owner's decision of 2026-10-04, way (ii), #1793 comment 5984369198; ALGEBRA.md, the arrival of The law in one line): on matter_alone's open 25-cube stepped by the engine's own `GameBoard.step`, (1) the content every row reads, gravity + binding, is at or above 0 at every Node and interval (the shipped engine read 24 Nodes below 0 at interval 3, the first [0, 0, 1] at -1, and 24 again at interval 5, the witness), (2) the guard's edge is never crossed, 2 cos omega(pi) = (S - SUM over the six Ports of R_ij) / w >= -2 at every Node and interval for every row, exactly in Fractions (the repeated root -2 at the content 0 admitted), (3) binding's and gravity's rows at the face Node [0, 12, 12] stay within one level of their rests, the witness that the start and the step agree at the face and that the massless row's sink holds, and (4) a GameBoard of the two slits' world stepped 40 intervals is bit for bit the shipped engine's, the fill 0 for its held rows at the start, the step and the growth, else the first differing interval and Node are named; the readings printed are GAMEBOARD diagnostics."""
    from fractions import Fraction

    import numpy as np

    from event_universe import growth, node
    from event_universe.core import ports
    from event_universe.features import start
    from event_universe.game_board import GameBoard
    from event_universe.world_files import load_world
    from tests.laws import EVENTS

    intervals, face = 60, (0, 12, 12)  # the CI clock; the 400 a GAMEBOARD diagnostic of the tool
    board = GameBoard(load_world(EVENTS / "matter_alone" / "pixel.json"))
    gamma, unit, names = board.world.node_clock, board.unit, [f.name for f in board.families]
    rows = {n: board.states[names.index(n)].lines[0] for n in ("binding", "gravity")}
    rest, levels = {n: int(row.now[face]) for n, row in rows.items()}, {n: set() for n in rows}
    lowest, edge = (0, "the start"), (Fraction(2), "the start")
    for tick in range(1, intervals + 1):
        board.step()
        for index, family in enumerate(board.families):
            content, factors = board.read(index)
            reads, self_coefficient, wall = node.rule_of(family, gamma, content, factors, unit)
            lowest = min(lowest, (int(np.min(content)), tick, family.name, int(np.argmin(content))))
            pi_mode = Fraction(int(np.min(self_coefficient - sum(reads))), int(wall))  # 2 cos omega(pi)
            edge = min(edge, (pi_mode, f"interval {tick}, {family.name}"))
        for name in rows:
            levels[name].add(int(board.states[names.index(name)].lines[0].now[face]))
    print("GAMEBOARD matter_alone: content min", lowest, "| pi min", edge, "| face levels", levels, rest)
    assert lowest[0] >= 0, (lowest, np.unravel_index(lowest[3], board.shape))  # (1) no hill by a face
    assert edge[0] >= -2, edge  # (2) the guard's edge never crossed in the run
    for name, found in levels.items():  # (3) the start and the step agree at the face, no drift
        assert max(abs(level - rest[name]) for level in found) <= 1, (name, rest[name], sorted(found))
    own, slits, kept = ports.OWN_LEVEL, EVENTS / "two_slits" / "two_slits.json", []
    with monkeypatch.context() as shipped_fill:  # the shipped engine: the fill 0 in place of OWN_LEVEL
        for module, name in ((node, "arrival"), (start, "arrival"), (growth, "sized")):
            act = getattr(module, name)
            shipped_fill.setattr(module, name, lambda *a, f=act: f(*[0 if x is own else x for x in a]))
        shipped = GameBoard(load_world(slits))
        for _ in range(40):
            shipped.step()
            kept.append([list(s.lines) for s in shipped.states])
    fixed = GameBoard(load_world(slits))
    for tick, lines in enumerate(kept, 1):
        fixed.step()
        for index, (state, was) in enumerate(zip(fixed.states, lines, strict=True)):
            for number, (line, old) in enumerate(zip(state.lines, was, strict=True)):
                for name in ("now", "before", "remainder"):
                    a, b = getattr(line, name), getattr(old, name)
                    differ = np.argwhere(a != b) if a.shape == b.shape else [list(a.shape)]
                    assert a.shape == b.shape and not len(differ), (
                        f"the two slits differ from the shipped engine at interval {tick}, the family "
                        f"{fixed.families[index].name!r} line {number} {name}, Node {list(differ[0])}"
                    )
    print("GAMEBOARD two slits: 40 intervals bit for bit against the fill 0 (held rows 0 at the faces)")
