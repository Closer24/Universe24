def test_the_vacuum_content_declared_above_the_holders_swing_keeps_every_content_inside_the_edge():
    """F2 fenced by way (alpha) (the owner's words of 2026-10-04, "we go with the recommendation" and "1"; the advisor's runs, #1793 comments 5985363946 and 5985373509; the mathematician's line, 5985390369; ALGEBRA.md, The vacuum content, item 22): matter_alone's open 25-cube loaded as shipped and stepped by the engine's own `GameBoard.step` over the intervals the CI clock admits (the folder's 400 the documented reading and not the test's), (a) the content every family reads, gravity + binding, at or above 1 at every Node and interval, (b) the pi mode's 2 cos omega(pi) = (S - SUM over the six Ports of R_ij) / w above -2 at every Node and interval for every row, in Fractions, (c) gravity's level at the face Node [0, 12, 12] within one of the rest the loaded universe declares, binding's swing there printed, and (d) the two slits at the declared rest stepped 40 intervals with no refusal and no end, the runner's own LAWFUL, the screen regions' inflows and N read as tools/click_counts.py reads them and printed, and the same world at the rest 0 (the loaded universe's rest replaced) stepped beside it, the first interval and Node where light's record differs printed; every reading a GAMEBOARD diagnostic."""
    from dataclasses import replace
    from fractions import Fraction

    import numpy as np

    from event_universe import node
    from event_universe.game_board import GameBoard
    from event_universe.loader.derived import count_wall
    from event_universe.world_files import load_world
    from tests.laws import EVENTS, ROOT, load_file

    intervals, face = 30, (0, 12, 12)  # the CI clock: the shipped world's start alone is 22 s here
    board = GameBoard(load_world(EVENTS / "matter_alone" / "pixel.json"))
    gamma, unit, names = board.world.node_clock, board.unit, [f.name for f in board.families]
    gravity, binding = (names.index(name) for name in ("gravity", "binding"))
    rest, levels = board.families[gravity].rest, {gravity: set(), binding: set()}
    lowest, edge = (gamma, 0, "the start", 0), (Fraction(2), "the start")
    for tick in range(intervals + 1):
        if tick:
            board.step()
        for index, family in enumerate(board.families):
            content, factors = board.read(index)
            reads, self_coefficient, wall = node.rule_of(family, gamma, content, factors, unit)
            lowest = min(lowest, (int(np.min(content)), tick, family.name, int(np.argmin(content))))
            pi_mode = Fraction(int(np.min(self_coefficient - sum(reads))), int(wall))  # 2 cos omega(pi)
            edge = min(edge, (pi_mode, f"interval {tick}, {family.name}"))
        for index in levels:
            levels[index].add(int(board.states[index].lines[0].now[face]))
    at = [int(i) for i in np.unravel_index(lowest[3], board.shape)]
    print(
        f"GAMEBOARD matter_alone over {intervals} intervals: the least content {lowest[:3]} at the Node {at}; "
        f"the least 2 cos omega(pi) {float(edge[0]):.6f} at {edge[1]}; gravity at the face {sorted(levels[gravity])} "
        f"against the file's rest {rest}; binding at the face {min(levels[binding])} to {max(levels[binding])}"
    )
    assert lowest[0] >= 1, (lowest, at)  # (a) every content above 0, inside the edge
    assert edge[0] > -2, edge  # (b) the guard's edge never reached
    assert {abs(level - rest) for level in levels[gravity]} <= {0, 1}, (rest, levels)  # (c) at the face
    world, lines = load_world(EVENTS / "two_slits" / "two_slits.json"), []
    declared = GameBoard(world, lines.append)
    bare = GameBoard(replace(world, families=tuple(replace(f, rest=0) for f in world.families)))
    light, first = world.messages[0].family, None
    for tick in range(1, 41):
        declared.step(), bare.step()
        pairs = zip(declared.states[light].lines, bare.states[light].lines, strict=True)
        for number, (line, other) in enumerate(pairs):
            differ = np.argwhere(line.now != other.now)
            if first is None and len(differ):
                first = (tick, number, [int(i) for i in differ[0]])
    assert declared.ended is None and declared.tick == 40  # (d) LAWFUL: no refusal and no end
    family, tool = world.families[light], load_file("click_counts", ROOT / "tools" / "click_counts.py")
    saw = tool.inflows(lines, [r.name for r in world.node_readers if r.declared], family.name, (1, 40))
    quanta = tool.nearest(sum(max(v, 0) for v in saw.values()), count_wall(family, world.quantum_action))
    print(
        f"GAMEBOARD two slits at the rest {max(f.rest for f in world.families)}: 40 intervals LAWFUL, the regions' inflows "
        f"{saw}, N {quanta} (the draw's window is the run's {world.draw.window} intervals, no credit before its end); "
        f"against the rest 0 light's record first differs at interval {first[0]}, line {first[1]}, Node {first[2]}"
    )
