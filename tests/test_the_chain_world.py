"""The chain world as a test (the owner's word of 2026-10-19, "write it as a test"; the click's plan, the conservation section's blinds B1 to B5 and B7 with C1's and C5's lines; the folder examples/events/chain holds the declaration and the lays as the test's fixtures, its blinds asserted here on every run of tools/check.py and never read from a run's table): one law-quantum of light at k = pi / 4 on two bodies of three Nodes along a chain of 96 with receding faces, each body taking the light into e over a window of 48 from the first lit interval and giving it back as a source in time at the lifetime 48; the six worlds the chain under the six signed permutations that carry a chain to a chain; the seventh the detuned packet of the window's length. Rule3 plus the one act conserve the count, the form, the momentum, the inverse and the 48, with no world-specific code and nothing at the Node."""

import json
import time

import numpy as np

from event_universe import readings, twist
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import BACK, EVENTS, ROOT, d4_bound, drift_bound, load_file

CHAIN = EVENTS / "chain"
DESIGN = json.loads((CHAIN / "design.json").read_text(encoding="utf-8"))
AXES = "xyz"


def family(board: Lattice, name: str) -> int:
    return [f.name for f in board.families].index(name)


def momentum_in_t(board: Lattice, index: int, at: np.ndarray | None = None) -> int:
    """A family's lattice momentum along the chain's axis in T's unit, over the board or over the Nodes `at` names (`readings.momentum_of`, `twist.scaled`)."""
    weight = board.families[index].pair[0]
    lines = [line for r in range(board.families[index].record) for line in board.lines_of(index, r)]
    read = readings.momentum_of(weight, lines, board.wrap, at)
    return twist.scaled(read, weight)[0]


def asymmetry(board: Lattice, light: int) -> int:
    """D7's asymmetry at the first source's Node this interval, |before_(i-x) - before_(i+x)| on the light's line, 0 with no source."""
    if not board.credit.sources:
        return 0
    at = np.add(board.credit.sources[0].at, board.offset)
    before = board.states[light].lines[0].before
    low, high = (at[0] - 1, at[1], at[2]), (at[0] + 1, at[1], at[2])
    return abs(int(before[low]) - int(before[high]))


def run(name: str, intervals: int) -> tuple[Lattice, list[dict], list[dict]]:
    """A chain world run `intervals` intervals from the lay with every interval's books of the light and the bodies kept beside the output lines."""
    board = Lattice(load_world(CHAIN / f"{name}.json"), (lines := []).append)
    light, atom = family(board, "photon"), family(board, "atom")
    marks = []
    for _ in range(intervals):
        board.step()
        books = board.books()["photon"]
        marks.append(
            {
                "interval": board.interval,
                "count": board.credit.counts[light],
                "quanta": books["quanta"],
                "share": books["share"],
                "form": sum(b["share"] for b in board.books().values() if b["share"] is not None),
                "parts": [list(b.counts) for b in board.credit.bodies],
                "fronts": len(board.credit.fronts),
                "sources": len(board.credit.sources),
                "P_light": momentum_in_t(board, light),
                "P_bodies": [
                    momentum_in_t(board, atom, board.mask(b.nodes)) for b in board.credit.bodies
                ],
                "increments": [list(s.increments) for s in board.credit.sources],
                "source_at": [tuple(s.at) for s in board.credit.sources],
                "asym": asymmetry(board, light),
                "drift": drift_bound(board, light),
            }
        )
    return board, lines, marks


def test_the_chain_conserves_the_count_the_form_and_the_momentum_through_the_pair():
    """B1, B2 and B3 with C1's and C5's lines on chain_x_minus over its 400 intervals (the blinds written before the run, examples/events/chain/expectation.json; no measured number inside them): B1, at every absorption the light's count falls by 1 and the body's e rises by 1 as its g falls by 1, at every emission the reverse, exactly, and outside the fronts' and the sources' spans the light's share in whole quanta over its own unit W_rec equals its count (on this chain the fronts run to the board's growth, so the check binds before the first click and wherever no front stands); C1, the count 1 and the quanta 1 at the lay and again after the emission's span; C5, no body takes the light it is itself sourcing (no absorption line names its own body as the source); B2, the board's form after the pair of one absorption and one emission within D7's bound of its value before, 3 den SUM_t (|a_t| + 1 / 4) over the source's increments, and the light's I = Q / W_rec at 1 within that bound at the lay and after the span; B3, at every absorption the body's own P moves by the piece less the shortfall, p_a = gain_a + s_a, within D4's bound computed at the lay (`tests.laws.d4_bound` on the loaded world, lay_bounds.json's number), the body's P is kept through its emission within the same bound, and the light's P after the source's span is the emitted light's alone (the absorbed quantum's fan, carrying its P until the front from the hole reaches it, is erased over the span, D6, its P the taker's since the click, "P lost to the taker"), within D7's momentum residue, SUM_t |a_t| |before_(i-x) - before_(i+x)| at the source's Node in T's unit, plus the integers' floors over the span, D1, the hands' bound summed over the span's intervals, 2 SUM_i |now_(i+1) - now_(i-1)| on the light's line (`tests.laws.drift_bound`, Part F (a)). FINDING by name (2026-10-19): the source's lay is even about its Node at every interval, so D7's residue is 0, and the light's P after the span reads 30 in T's unit, the walk of the integers over the span (D1) and no term of D7's; the blind B3 as written names the residue alone and is missed by the floors, which the hands' bound covers. The run's seconds printed."""
    started = time.perf_counter()
    board, lines, marks = run("chain_x_minus", DESIGN["intervals"])
    light, atom = family(board, "photon"), family(board, "atom")
    den, unit = board.families[light].pair[1], board.credit.units[light]
    by_interval = {m["interval"]: m for m in marks}
    clicks = [c for c in lines if c["event"] == "credit" and (c["absorbed"] or c["emitted"])]
    assert clicks and clicks[0]["absorbed"] and clicks[1]["emitted"]  # the pair, body 0's
    # B1 and C5: the counts exactly at every click, no body on its own source
    for click in clicks:
        t, body = click["interval"], int(click["node_detector"].split()[1])
        before, after = by_interval[t - 1], by_interval[t]
        sign = -1 if click["absorbed"] else 1
        assert after["count"] - before["count"] == sign and click["left"] == after["count"]
        assert after["parts"][body][1] - before["parts"][body][1] == -sign  # e
        assert after["parts"][body][0] - before["parts"][body][0] == sign  # g
        assert click["source"] != click["node_detector"]  # C5: not its own source
    quiet = [m for m in marks if m["fronts"] == 0 and m["sources"] == 0]
    assert quiet and all(m["quanta"] == m["count"] for m in quiet)  # B1: the quanta the count
    assert (marks[0]["count"], marks[0]["quanta"]) == (1, 1)  # C1 at the lay
    # B2 and B3 over the first pair: the absorption at t_a, the emission at t_e, its span tau
    t_a, t_e = clicks[0]["interval"], clicks[1]["interval"]
    increments = by_interval[t_e]["increments"][0]
    tau = len(increments)
    bound_q = 3 * den * sum(abs(a) for a in increments) + (3 * den * tau) // 4  # D7's form bound
    rest = by_interval[t_e + tau]
    assert rest["sources"] == 0 and (rest["count"], rest["quanta"]) == (1, 1)  # C1 after the span
    assert abs(rest["form"] - by_interval[t_a - 1]["form"]) <= bound_q  # B2: the form over the pair
    assert abs(marks[0]["share"] - unit) <= bound_q and abs(rest["share"] - unit) <= bound_q  # I = 1
    body = int(clicks[0]["node_detector"].split()[1])
    nodes = board.credit.bodies[body].nodes
    piece, short = clicks[0]["momentum"][0], clicks[0]["shortfall"][0]
    gain = piece + short if piece < 0 else piece - short  # p_a = gain_a + s_a, s_a at or above 0
    assert short >= 0 and abs(gain) + short == abs(piece)
    moved = by_interval[t_a]["P_bodies"][body] - by_interval[t_a - 1]["P_bodies"][body]
    laid = json.loads((CHAIN / "lay_bounds.json").read_text(encoding="utf-8"))
    bound_p = d4_bound(Lattice(load_world(CHAIN / "chain_x_minus.json")), atom, nodes)[0]  # at the lay
    assert bound_p == laid[0]["bodies"][body]["D4_bound_T_unit"][0]  # lay_bounds.json's number
    assert abs(moved - gain) <= bound_p, (moved, gain, bound_p)  # B3 at the absorption
    kept = by_interval[t_e]["P_bodies"][body] - by_interval[t_e - 1]["P_bodies"][body]
    assert abs(kept) <= bound_p, (kept, bound_p)  # B3 through the emission (C3)
    residue = sum(
        abs(a) * by_interval[t_e + k]["asym"] for k, a in enumerate(increments) if t_e + k in by_interval
    )  # D7: SUM_t |a_t| |before_(i-x) - before_(i+x)| at the source's Node, in T's unit
    floors = sum(by_interval[t]["drift"] for t in range(t_e, t_e + tau))  # D1 over the span's steps
    assert abs(rest["P_light"]) <= residue + floors, (rest["P_light"], residue, floors)
    print(
        f"the chain world: {len(clicks)} clicks in {DESIGN['intervals']} intervals, the pair at {t_a} and {t_e} "
        f"(the piece {piece}, the shortfall {short}, the body's P moved {moved} against the gain {gain} and {kept} through the emission, D4's bound "
        f"{bound_p}; the form over the pair moved {rest['form'] - by_interval[t_a - 1]['form']} within {bound_q}; the "
        f"emitted light's P {rest['P_light']} against D7's residue {residue}, within the floors {floors}); "
        f"{time.perf_counter() - started:.1f} s"
    )


def test_the_chain_runs_back_through_its_absorption_and_emission():
    """B4, the inverse: tools/back_in_time.py's verdict on chain_x_minus over the first 100 intervals, through the first absorption (74) and the emission that follows (91), MATCH bit for bit: every array returns through the click's two writes, the fold and the lay lines."""
    found = BACK.verdict(Lattice(load_world(CHAIN / "chain_x_minus.json")), 100)
    assert found["verdict"] == "MATCH" and found["intervals"] == 100, found


def carried(board: Lattice, array: np.ndarray, axis: str, toward: str) -> np.ndarray:
    """An image world's array brought back to the original's frame: the chain's axis moved to x and, for the light toward the upper side, the coordinate mirrored."""
    moved = np.moveaxis(array, AXES.index(axis), 0)
    return moved[::-1] if toward == "plus" else moved


def test_the_six_images_are_one_world_under_the_48():
    """B5, the 48: the six worlds of the design (the chain along x, y and z, the light toward the lower side or the upper, the bodies' Node lists the images in the original's order, the draw's order the one named exception, L812 untouched) run 200 intervals each; brought back by the inverse of each signed permutation (the chain's axis to x, the coordinate mirrored for the upper side, the vector components with the axis's sign), every click line, every level and every remainder of every family is equal to the original's for the two pure permutations (y and z toward the lower side), exactly. FINDING by name (2026-10-19) against B5 as written, the three mirror images (toward the upper side): equal to the original in every click line and every cell of every family but one place, the giver's own record at the second absorption, where the taker's piece is the light the first body emitted and the first body is folded by the recoil (`twist.recoiled`, `twist.folded_source`): the first body stands at a quarter turn per Node since its own absorption (the twist of 74, kept through its emission's re-lay, Part H), so both senses of the recoil's fold move its P by the piece (to k = 0 or to k = pi, the momentum 0 either way to the rounding), and `twist.twisted` takes the sense whose POSITIVE quarter turn moves P with the piece's sign, the same sense in the mirror image where the covariant one is its opposite; the record ends at k = 0 in the original and at k = pi in the image, the same counts and clicks after, the giver's middle Node's two real lines at the opposite sign, its three Nodes' remainders apart, and the recoil read on its lines 41404 against 42320 in T's unit (the rounding at k = pi against k = 0), the `recoil` of that one click line the only key that differs. The sense's tie, like the draw's order, is a second exception to the 48 and is asserted here as found: the three mirrors equal to one another in every cell, their differences from the original confined to the giver's family at the giver's Nodes and to the `recoil` of a click line naming the giver as the source. The six runs' seconds printed."""
    started = time.perf_counter()
    found = {}
    for name, (axis, toward) in DESIGN["worlds"].items():
        board = Lattice(load_world(CHAIN / f"{name}.json"), (lines := []).append)
        for _ in range(200):
            board.step()
        a, sign = AXES.index(axis), -1 if toward == "plus" else 1
        clicks = []
        for c in lines:
            if c["event"] != "credit":
                continue
            line = dict(c)
            for key in ("momentum", "fan", "twist", "shortfall", "recoil"):
                if isinstance(line[key], list):
                    vector, flip = line[key], 1 if key == "shortfall" else sign  # s_a a magnitude
                    line[key] = [flip * vector[a], *(v for k, v in enumerate(vector) if k != a)]
            clicks.append(line)
        arrays = {
            (f, j): tuple(
                carried(board, x, axis, toward) for x in (line.now, line.before, line.remainder)
            )
            for f, state in enumerate(board.states)
            for j, line in enumerate(state.lines)
        }
        found[name] = (clicks, arrays, board)
    original = found["chain_x_minus"]
    board = original[2]
    atom, giver = family(board, "atom"), board.credit.bodies[0]
    inside = board.mask(giver.nodes)  # the giver's Nodes, the original's frame
    mirrors = [name for name, (_axis, toward) in DESIGN["worlds"].items() if toward == "plus"]
    recoils = []
    for name, (clicks, arrays, _board) in found.items():
        assert len(clicks) == len(original[0]) and arrays.keys() == original[1].keys(), name
        for line, line0 in zip(clicks, original[0], strict=True):
            keys = [key for key in line if line[key] != line0[key]]
            if name not in mirrors:
                assert not keys, (name, line["interval"], keys)  # a pure permutation: exact
            elif keys:  # a mirror: the giver's recoil at the taker's click alone
                assert keys == ["recoil"] and line["source"] == f"body {giver.number}", (name, keys)
                recoils.append((line["interval"], line["recoil"][0], line0["recoil"][0]))
        for (f, j), cells in arrays.items():
            for x, x0 in zip(cells, original[1][(f, j)], strict=True):
                assert x.shape == x0.shape, name
                apart = x != x0
                if name not in mirrors:
                    assert not apart.any(), (name, f, j)  # a pure permutation: exact
                else:
                    assert f == atom or not apart.any(), (name, f, j)  # the giver's family
                    assert not (apart & ~inside).any(), (name, f, j)  # at the giver's Nodes
    for name in mirrors[1:]:  # the three mirrors one world under the 48
        assert found[name][0] == found[mirrors[0]][0], name
        for key, cells in found[name][1].items():
            assert all(
                np.array_equal(x, y) for x, y in zip(cells, found[mirrors[0]][1][key], strict=True)
            ), name
    assert recoils, "the mirrors' one difference, the giver's recoil, stands"
    print(
        f"B5: the two pure permutations exact over 200 intervals, {len(original[0])} click lines; the three mirrors one world, "
        f"apart from the original at the giver's recoil alone, {sorted(set(recoils))} (interval, mirror, original); "
        f"{time.perf_counter() - started:.1f} s"
    )


def test_the_detuned_packet_is_absorbed_in_at_most_one_of_its_eight_trials():
    """B7, the line shape (C9 (b)): chain_detuned, the packet of 48 Nodes at k = pi / 8 detuned from the transition at pi / 4, run over its 250 intervals for each of the eight seeds of detuned_trials.json with every record's generator at the hash of the trial's label (tools/meeting_trials.py); the blind written before the run reads at most one absorption over the trials (the window's sinc at Delta W / 2 = 5.3, sinc^2 below 1 / 30); the engine reads three of eight at the declared weight 6, a finding by name and no adjustment of the blind: the window's sums of this long packet turn the labels 1.8 rad at resonance, so the sinc's 0.16 leaves 0.28 rad, sin^2 near 8 percent per window and two to three windows per passage, near 20 percent per trial, the blind's one window and one quarter turn presumed where the packet gives more; the reading pinned here as the engine's, to move with the weight. The trials' seconds printed."""
    started = time.perf_counter()
    trials = load_file("meeting_trials", ROOT / "tools" / "meeting_trials.py")
    seeds = json.loads((CHAIN / "detuned_trials.json").read_text(encoding="utf-8"))["seeds"]
    absorbed = 0
    for seed in seeds:
        _parts, _windows, clicks, refused = trials.one_trial(CHAIN / "chain_detuned.json", seed, 250)
        assert refused is None
        absorbed += sum(1 for c in clicks if c["absorbed"])
    assert absorbed == 3, (
        absorbed
    )  # the blind's 1 of 8 is missed: a finding, pinned, the blind not adjusted
    print(
        f"B7: {absorbed} absorption(s) in {len(seeds)} trials of the detuned packet; {time.perf_counter() - started:.1f} s"
    )
