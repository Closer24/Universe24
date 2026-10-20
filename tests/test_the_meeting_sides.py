"""The meeting that runs back at N sides and with the erasure's taper (the reader's verdict of 2026-10-19, points 11 and 13; ALGEBRA.md, The meeting's reading; The meeting's identity), beside tests/test_the_meeting_back.py: (i) the reader's case, a two-part record with the identity pattern on every side read at three sides at the settings (3, 4), (1, 1), (1, 0), where the middle side's weights by the chain rule from the booked joint (1 / 2, 1 / 2) differ from the re-weighted one-side share (49 / 50, 1 / 50) by the cross terms of the third side's read, so the engine draws every side after the first on the chain and the law's two-sided words are the last side's alone, tested equal there; no signalling at N sides, every side's marginal its own; (j) the erasure's taper in the back mode, the fronts the act's as built, the erasure lines and the end state equal bit for bit to the root mode's at any seed on regions whose inflow enters at one Node; and the cone stepped alone (the owner's word of 2026-10-20, only the cone moves and the whole board steps as ever): (k) the shipped fifth world and the shipped GHZ world read under the cone and under the whole board with every line, the close and the lay equal and fewer Node-steps in the cone, (l) its three refusals by name. The worlds the tests' own (tests/laws_spin.py), no world or family name in the engine."""

import json
from dataclasses import replace
from fractions import Fraction

import numpy as np
import pytest

from event_universe import meeting_back, reports
from event_universe.features.click import drawn, hashed
from event_universe.features.front import distances
from event_universe.lattice import Lattice
from event_universe.loader.draw import BOARD, CONE, ports_of
from event_universe.records import Record
from event_universe.world_files import load_world
from tests.laws import BACK as GATE
from tests.laws import EVENTS, TOOL, family, world_beside
from tests.laws_spin import (
    BELL,
    IDENTITY,
    PORT,
    SINGLET,
    digest,
    joint_shares,
    marginal_of,
    spin_world,
    trial,
)


def test_a_middle_side_reads_the_chain_rules_local_form_and_the_last_within_the_walk(
    tmp_path, monkeypatch
):
    """(i) N sides, the reader's case (the verdict's point 11 of 2026-10-19; B6 and Q1 of 2026-10-20): the two-part record with the identity pattern on every side read at three sides at the settings (3, 4), (1, 1) and (1, 0), the third region four Nodes inside the left one with one Node between; the three credit lines in the declared order with the count 1, nothing left and the scales 25, 50 and 50 (the norms' squares cumulative); the first side's weights the marginal exactly (the Gram of the two identity patterns after it the identity, so SUM_k e_k(p)^2 M_kk, 1 / 2 and 1 / 2); its realised coefficients (3, 4) or (-4, 3) written at the birth take two magnitudes, so from there the parts part by the remainders' walk (the law's regime for weighted parts): the middle side's weights 1 / 2 and 1 / 2 EXACTLY whatever the walk (the Gram the identity, the equal ports w(+) = w(-) = M'_00 + M'_11), and the last side's coherent read within the walk's bound of the chain rule's 9 / 25 and 16 / 25 (|w / SUM w - the fraction| under 2 x 10^-3, the deviation printed); the realised triple the three draws on the states hashed from the seed, the names and the window with the engine's weights; no signalling: the first side's weights the same at other settings of the sides after it, 1 / 2 at both."""
    reader = {"left": ((3, 4), IDENTITY), "near": ((1, 1), IDENTITY), "right": ((1, 0), IDENTITY)}
    other = {"left": ((3, 4), IDENTITY), "near": ((5, 12), IDENTITY), "right": ((1, 1), IDENTITY)}
    firsts = {}
    for label, sides in (("reader", reader), ("other", other)):
        path = spin_world(
            tmp_path / label, monkeypatch, sides, both=True, amplitude=64, regions={"near": [5, 6, 7, 8]}
        )
        board, lines = trial(path, 1, 40)
        spin, draw, modulus = family(board, "spin"), board.world.draw, board.world.width + 1
        books, clicks = board.credit, [c for c in lines if c["event"] == "credit"]
        realised = [PORT[c["realised"]] for c in clicks]
        assert [(c["node_detector"], c["order"], c["count"], c["left"]) for c in clicks] == [
            (name, order, 1, 0) for order, name in enumerate(sides, 1)
        ]
        for side, (name, _ports) in enumerate(books.sides):
            state = hashed(draw.seed, name, 1, modulus)
            weights = books.weights[(spin, name)]
            assert drawn(state, draw.multiplier, draw.increment, modulus, weights)[0] == realised[side]
        firsts[label] = books.weights[(spin, "left")]
        assert Fraction(firsts[label][0], sum(firsts[label])) == Fraction(1, 2) and board.passes == 7
        if label == "reader":
            joint = joint_shares(lines, sides, 0)
            assert [c["scale"] for c in clicks] == [25, 25, 9]  # the norm of the coefficients standing
            middle = books.weights[(spin, "near")]
            assert middle[0] == middle[1] > 0  # the equal ports, exact whatever the walk
            last, fixed = books.weights[(spin, "right")], {0: realised[0], 1: realised[1]}
            chain = marginal_of(joint, 2, fixed)
            deviation = abs(Fraction(last[0], sum(last)) - Fraction(chain[0], sum(chain)))
            assert Fraction(chain[0], sum(chain)) in (Fraction(9, 25), Fraction(16, 25))
            assert deviation < Fraction(2, 1000), (last, chain)
            print(
                f"the reader's case: the realised triple {realised}, the middle side {middle}, the last side "
                f"{last} against the chain {chain}, the walk's deviation {float(deviation):.2e}"
            )
    assert firsts["reader"] == firsts["other"]  # no signalling: the first side's read its own


def test_the_tapered_front_runs_inside_the_clicks_light_cone_after_the_last_sides_close(
    tmp_path, monkeypatch
):
    """(j) The erasure's taper under the one meeting (the verdict's point 13 of 2026-10-19; A3c of 2026-10-20: the fronts begin at the one close after the last side, no front from every click): the singlet world with regions of two Nodes at the chain's ends, whose inflow enters at the inner Node alone, and `erasure` 3, run 126 intervals at two seeds; the two sides draw at the close 40 with the orders 1 and 2 and the count's write follows the last side; the two fronts begin at the close from the hole's Nodes, the regions' inner Nodes whatever the ports realised, one shell per interval at the Link distance of the intervals since the click (inside the click's light cone), two Nodes at most on the chain, the shells beyond the grown board the taper's last lines, and end at the close plus the farthest Node's distance, one and the taper, the record's count 0 and its share erased; the back-in-time gate reads MATCH over the 40 intervals after the close, across the tapered shells (the frames before the close the possibilities' run by the law, the inverse returning the realised past there)."""
    sides = {"left": (BELL[0], IDENTITY), "right": (BELL[2], SINGLET)}
    ends = {"left": [0, 1], "right": [31, 32]}
    path = spin_world(tmp_path, monkeypatch, sides, both=True, amplitude=64, regions=ends, erasure=3)
    runs = {}
    for seed in (1, 5):
        lines: list[dict] = []  # type: ignore[type-arg]
        board = Lattice(load_world(path), lines.append)
        board.credit.declaration = replace(board.world.draw, seed=seed)
        for _ in range(126):
            board.step()
        runs[seed] = (board, lines)
    spin = family(board, "spin")
    for board, lines in runs.values():
        erasures = [e for e in lines if e["event"] == "erasure"]
        clicks = [c for c in lines if c["event"] == "credit"]
        assert not board.credit.fronts and board.credit.counts[spin] == 0
        assert board.total_share(spin)[0] == 0 and board.world.erasure == 3
        close = clicks[0]["interval"]
        assert [(c["node_detector"], c["order"], c["interval"]) for c in clicks] == [
            ("left", 1, 40),
            ("right", 2, 40),
        ]
        for origin in ((1, 0, 0), (31, 0, 0)):  # the regions' inner Nodes, where the inflow enters
            shells = [e for e in erasures if tuple(e["origin"]) == origin]
            at = tuple(o + f for o, f in zip(origin, board.offset, strict=True))
            farthest = int(distances(board.shape, at, board.world.periodic).max())
            taper = board.world.erasure
            assert [e["interval"] for e in shells] == list(
                range(close + 1, close + farthest + taper + 2)
            )
            assert all(e["distance"] == e["interval"] - close and e["nodes"] <= 2 for e in shells)
            beyond = [e["interval"] for e in shells if e["nodes"] == 0]
            assert beyond == list(range(close + farthest + 1, close + farthest + taper + 2))
        assert len(erasures) == 2 * len(shells)
    gate = Lattice(load_world(path))
    for _ in range(41):  # through the close: the click, the writes, the hole and the fronts' start
        gate.step()
    assert GATE.verdict(gate, 40)["verdict"] == "MATCH"
    print(
        f"the taper after the one close: {len(erasures)} erasure lines at the seeds 1 and 5, the shells to "
        f"{max(e['interval'] for e in erasures)} on the board of {board.shape[0]}, the realised ports "
        f"{[(s, [c['realised'] for c in runs[s][1] if c['event'] == 'credit']) for s in runs]}"
    )


def test_the_cone_stepped_alone_returns_the_board_runs_close_at_fewer_node_steps(tmp_path, monkeypatch):
    """(k) The cone stepped alone (the owner's word of 2026-10-20; ALGEBRA.md, The meeting's reading; The interval's dependency radius is one Link): the shipped fifth world (singlet_back_a_b, the cone by default) and the shipped GHZ world (x, y, y) with `meeting: back`, each run whole under the cone and under `reach: board` beside it; the two runs' every output line equal (the credit lines with the realised ports, the parts, the faces), the two boards equal bit for bit at the end, the books equal; the frames' sequence of tick, interval, direction and pass equal and, at every frame of both runs, the hash of every array of the board equal in order (`digest` over `meeting_back.snapshot`: the cone-alone trajectory is the board's at every step and not at the ends alone, the assertion naming the first frame that differs), and at the birth the board equal to the lay bit for bit (frame 0 inside S_0 and outside it alike, the growths all popped); the Node-steps of the reading (`credit.stepped`, in the cone the box with its ring per step, on the board its volume) counted at the same intervals, the cone's fewer at every interval and in all (the saving modest on the shipped boards, which the cone fills early); the growths of the receding faces popped on the way back and replayed on the way forward, the board's growth log and shape at the end the board run's and the record's history stack empty; no refusal."""
    runs = {}
    for folder, name, edit in (
        ("bell_singlet", "singlet_a_b.json", {}),
        ("ghz", "ghz_x_y_y.json", {}),
    ):
        source = EVENTS / folder / name
        for reach in (None, BOARD):
            edits = {**edit, **({"reach": reach} if reach else {})}

            def edited(w, e=edits):  # type: ignore[no-untyped-def]
                w["draw"].pop("meeting", None)  # the one meeting needs no key (the files move with it)
                w["draw"].update(e)

            path = world_beside(tmp_path / f"{folder}_{reach}", source, edited)
            lines, frames, digests = [], [], []
            board = Lattice(load_world(path), lines.append)
            zero = meeting_back.snapshot(board)

            def seen(t, d, p, b=board, frames=frames, digests=digests, zero=zero):
                frames.append((b.tick, t, d, p))
                digests.append(digest(b))  # the frame's state, every array
                if p == 2 and t == 0:  # the first run back reaches the lay bit for bit, unwritten
                    assert meeting_back.first_difference(zero, meeting_back.snapshot(b)) is None

            board.observers.append(seen)
            for _ in range(board.world.intervals):
                board.step()
            runs[name, reach] = (board, lines, frames, digests)
        cone, whole = runs[name, None], runs[name, BOARD]
        assert cone[0].credit.reach == CONE and whole[0].credit.reach == BOARD
        assert cone[1] == whole[1] and cone[2] == whole[2] and len(cone[1]) > 100
        first = next((f for f, a, b in zip(cone[2], cone[3], whole[3], strict=True) if a != b), None)
        assert first is None, (
            f"the cone-alone trajectory first differs from the board's at the frame (tick, interval, direction, pass) {first}"
        )
        assert (
            meeting_back.first_difference(
                meeting_back.snapshot(whole[0]), meeting_back.snapshot(cone[0])
            )
            is None
        )
        assert cone[0].books() == whole[0].books() and cone[0].shape == whole[0].shape
        assert cone[0].growths == whole[0].growths and cone[0].growths
        stepped = {reach: runs[name, reach][0].credit.stepped for reach in (None, BOARD)}
        assert sorted(stepped[None]) == sorted(stepped[BOARD]) and len(stepped[None]) > 1
        assert all(stepped[None][t] <= stepped[BOARD][t] for t in stepped[None])
        assert sum(stepped[None].values()) < sum(stepped[BOARD].values())
        print(
            f"the cone stepped alone on {name}: Node-steps {sum(stepped[None].values())} against the board's "
            f"{sum(stepped[BOARD].values())}, {len(cone[0].growths)} growths read anew from the box, the lines "
            f"{[c['realised'] for c in cone[1] if c['event'] == 'credit']} in both"
        )


def test_the_cone_stepped_alone_refuses_a_moved_rest_a_broken_cone_and_an_act_outside_by_name(
    tmp_path, monkeypatch
):
    """(l) The three refusals of the cone stepped alone by name (the reader's verdict of 2026-10-20), on the singlet world laid on a chain of 120 Nodes with the regions about the centre where the chain of 33 has them (no growth in 40 intervals, the chain's ends outside the record's cone at the close): a level moved by hand at the interval 39 at 42 Links from the lay, the first step back's ring, refused at that step as the rest moved at the cone's edge (read from the board's own arrays); a level moved inside the cone at 34 Links, far from the record, refused as the cone not holding when the shrinking cone's shell reaches the past the inverse computes for a level with no past; a lay of the books' log at a Node outside the cone at its interval refused as an act outside the record's cone before the step re-presents it; the same world untouched read under the cone and under the board with the two closes equal bit for bit and |G(0)| the lay's 13 Nodes within one Link."""
    sides = {"left": (BELL[0], IDENTITY), "right": (BELL[2], SINGLET)}
    regions = {"left": [44, 45, 46, 47], "right": [73, 74, 75, 76]}

    def world(label, reach=None):
        return spin_world(
            tmp_path / label,
            monkeypatch,
            sides,
            both=True,
            amplitude=64,
            length=120,
            reach=reach,
            regions=regions,
        )

    def moved(board, x):  # a level moved by hand at the chain's Node x, a new array beside the old
        spin, line = family(board, "spin"), board.states[family(board, "spin")].lines[0]
        now = np.array(line.now, copy=True)
        now[x + board.offset[0], 0, 0] += 1
        board.states[spin].lines[0] = Record(now, line.before, line.remainder)

    for label, x, text in (
        ("edge", 12, "the rest at the record's cone's edge moved at the interval 40"),
        ("inside", 100, "the record's cone did not hold at the interval"),
    ):
        board = Lattice(load_world(world(label)))
        for _ in range(39):
            board.step()
        moved(board, x)
        with pytest.raises(RuntimeError, match=text):
            board.step()
    board = Lattice(load_world(world("act")))
    for _ in range(39):
        board.step()
    board.credit.lays[20] = [reports.lay(20, "spin", 0, [10, 0, 0], [0, 0, 0], [0, 0, 0])]
    with pytest.raises(
        RuntimeError, match=r"an act of the interval 20 stands at the Node \[10, 0, 0\] outside"
    ):
        board.step()
    boards = [Lattice(load_world(world(str(reach), reach))) for reach in (None, BOARD)]
    for board in boards:
        for _ in range(40):
            board.step()
    assert meeting_back.first_difference(*(meeting_back.snapshot(b) for b in boards)) is None
    assert boards[0].credit.cone[0] == 15 and boards[0].credit.reach == CONE
    print(
        f"the three refusals by name; the untouched chain of 120 read alike in the two reaches, |G(0)| {boards[0].credit.cone[0]}"
    )


def born_world(folder, monkeypatch, seed, window=200, intervals=124):  # type: ignore[no-untyped-def]
    """The born pair's world (the owner's word of 2026-10-20; ALGEBRA.md, The lay across parts; The births' book): the spin world's chain with no packet, the giver family `atom` added to its universe ([1, 1299], two parts of a plane, reading no holder), one atom body at the Node 12 standing in its part e, the transition g to e by `spin` at the resonance [5414, 6000] and the rate e to g with the lifetime 24 giving its quantum to `spin`, the body's own books with its `seed` (its window the passage of its drive's lay, derived at load); the two regions of the singlet with the identity pattern; `meeting: back` with the board's reach and the world's window `window` over `intervals` intervals; the mode file by the generator; the world's path."""
    sides = {"left": (BELL[0], IDENTITY), "right": (BELL[2], IDENTITY)}
    path = spin_world(folder, monkeypatch, sides, both=True, amplitude=64, reach=BOARD)
    universe = json.loads((folder / "u.json").read_text(encoding="utf-8"))
    universe["families"].append({"name": "atom", "pair": [1, 1299], "dimension": [2, 2], "reads": {}})
    (folder / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    world = json.loads(path.read_text(encoding="utf-8"))
    world["packets"], world["intervals"], world["draw"]["window"] = [], intervals, window
    world["bodies"] = [
        {
            "family": "atom",
            "nodes": [{"node": [12, 0, 0], "weight": 1}],
            "parts": [{"part": 0, "name": "g", "count": 0}, {"part": 1, "name": "e", "count": 1}],
            "transitions": [
                {"from": "g", "to": "e", "drive": "spin", "weight": 1, "resonance": [5414, 6000]}
            ],
            "rates": [{"from": "e", "to": "g", "lifetime": 24, "gives_to": "spin"}],
            "node_detector": {
                "multiplier": 6364136223846793005,
                "increment": 1442695040888963407,
                "seed": seed,
            },
        }
    ]
    path.write_text(json.dumps(world) + "\n", encoding="utf-8")
    TOOL.main(["--input", str(path)])
    return path


def test_a_record_born_of_an_emission_is_laid_on_every_part_alike_and_read_from_its_birth(
    tmp_path, monkeypatch
):
    """(m) The lay across parts and the births' book (the owner's word of 2026-10-20; ALGEBRA.md, The lay across parts; The births' book): the born pair's world (`born_world`, the first of eight seeds whose atom emits before the interval 60), run 124 intervals under `meeting: back` with a window longer than the run (the lays logged, no click): the emission lays the quantum of `spin` on every part alike, the lay lines of the birth interval on the first line of each part at the Node 12 with the same levels, the two parts' lines equal bit for bit at the end (the symmetric lay stepped by one rule) and the `parts` lines' sums equal part by part; the births' book holds the birth's interval and the Node, `birth_of` reads it, the books count one quantum; the run back from the close stops at the birth, the board there equal bit for bit to the frame the forward run recorded right after the birth's lays, the cone's root the birth's Node, and the run forward returns the close bit for bit."""
    for seed in range(8):
        path = born_world(tmp_path / str(seed), monkeypatch, seed)
        lines, frames = [], {}
        board = Lattice(load_world(path), lines.append)
        spin = family(board, "spin")
        board.observers.append(
            lambda t, d, p, b=board, frames=frames: frames.__setitem__(t, meeting_back.snapshot(b))
        )
        for _ in range(board.world.intervals):
            board.step()
        if spin in board.credit.births and board.credit.births[spin][0] <= 60:
            break
    else:
        raise AssertionError("no seed of eight emitted before the interval 60")
    birth, nodes = board.credit.births[spin]
    width = board.families[spin].width
    assert 0 < birth <= 60 and nodes == ((12, 0, 0),) and board.credit.counts[spin] == 1
    first = [line for line in lines if line["event"] == "lay" and line["family"] == "spin"]
    first = [line for line in first if line["interval"] == birth]
    assert sorted(line["line"] for line in first) == [0, width]
    assert len({tuple(line["after"]) for line in first}) == 1 and first[0]["after"][0] != 0
    state = board.states[spin]
    for k in range(width):  # the parts alike bit for bit: the symmetric lay stepped by one rule
        for array in ("now", "before", "remainder"):
            assert (getattr(state.lines[k], array) == getattr(state.lines[width + k], array)).all()
    parts = [line for line in lines if line["event"] == "parts" and line["family"] == "spin"]
    assert parts and all(
        line["levels"][k] == line["levels"][width + k] for line in parts for k in range(width)
    )
    assert meeting_back.birth_of(board, spin) == birth and board.books()["spin"]["quanta"] == 1
    kept = meeting_back.run_back(board, spin)
    assert board.interval == birth and board.credit.birth == birth and board.credit.support == nodes
    assert meeting_back.first_difference(frames[birth], meeting_back.snapshot(board)) is None
    meeting_back.run_forward(board, spin, board.world.intervals, kept)
    print(
        f"the born pair: the atom at the seed {seed} emitted at the interval {birth}, the quantum laid on the "
        f"lines {sorted(line['line'] for line in first)} alike, the run back to the birth exact"
    )


def test_the_gram_read_is_the_chain_rules_local_form_from_the_sides_own_books(tmp_path, monkeypatch):
    """(n) The per-side books and the Gram read (ALGEBRA.md, The meeting's identity, the Gram theorem; the owner's word of 2026-10-20): the Gram of no side is the matrix of ones, the identity pattern's the identity, the GHZ's third pattern's the reader's matrix; the quadratic form on the moments [[5, 5], [5, 5]] at the setting (12, 5) with the identity pattern reads 845 and 845 under the identity Gram and 1445 and 245 under the ones; the antisymmetric first side's coefficients the determinant's; on the singlet world at two settings the first side's weights at its draw are the Gram read of the test's own second moments from the `parts` lines (the engine's books the same products) with the partner's Gram, and equal the marginal of the joint shares exactly (the chain rule's local form, the Gram theorem)."""
    identity = tuple(tuple(pair) for pair in IDENTITY)
    assert meeting_back.gram_of([], 2) == [[1, 1], [1, 1]]
    assert meeting_back.gram_of([identity], 2) == [[1, 0], [0, 1]]
    ghz = ((1, 0), (0, -1), (0, -1), (-1, 0))
    assert meeting_back.gram_of([ghz], 4) == [[1, 0, 0, -1], [0, 1, 1, 0], [0, 1, 1, 0], [-1, 0, 0, 1]]
    ports = ports_of((12, 5), identity)
    coefficients, five = [list(port) for port in ports], [[(5, 0), (5, 0)], [(5, 0), (5, 0)]]
    assert meeting_back.side_weights(five, coefficients, [[1, 0], [0, 1]]) == [845, 845]
    assert meeting_back.side_weights(five, coefficients, [[1, 1], [1, 1]]) == [1445, 245]
    for a, b in ((BELL[0], BELL[2]), (BELL[1], BELL[3])):
        sides = {"left": (a, IDENTITY), "right": (b, SINGLET)}
        path = spin_world(
            tmp_path / f"{a[0]}_{a[1]}_{b[0]}_{b[1]}",
            monkeypatch,
            sides,
            both=True,
            amplitude=64,
            reach=BOARD,
        )
        board, lines = trial(path, 1, 40)
        spin, joint = family(board, "spin"), joint_shares(lines, sides, 0)
        width = board.families[spin].width
        own = {name: [[0, 0], [0, 0]] for name in sides}
        for row in (r for r in lines if r["event"] == "parts"):
            for member in range(2):
                for k in range(2):
                    for m in range(2):
                        levels = row["levels"]
                        own[row["node_detector"]][k][m] += sum(
                            levels[k * width + i][member] * levels[m * width + i][member]
                            for i in range(width)
                        )
        assert all(any(map(any, own[name])) for name in sides)
        first = meeting_back.coefficients_of(board.families[spin], board.credit.sides[0][1], True)
        gram = meeting_back.gram_of([board.credit.patterns["right"]], 2)
        pairs = [[(value, 0) for value in row] for row in own["left"]]  # the real moments as pairs
        weights = meeting_back.side_weights(pairs, first, gram)
        assert weights == board.credit.weights[(spin, "left")]  # the engine's moments the test's own
        marginal = marginal_of(joint, 0)
        assert Fraction(weights[0], sum(weights)) == Fraction(marginal[0], sum(marginal))
        antisymmetric = meeting_back.coefficients_of(
            replace(board.families[spin], exchange=-1), board.credit.sides[0][1], True
        )
        assert antisymmetric == [
            [(-port[1][0], -port[1][1]), port[0]] for port in board.credit.sides[0][1]
        ]  # the determinant's lambdas on pairs
        print(
            f"the Gram read at {a}, {b}: the first side's weights {weights}, the marginal of J {marginal}"
        )
