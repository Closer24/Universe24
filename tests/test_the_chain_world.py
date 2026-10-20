"""The chain world as a test (the owner's word of 2026-10-19, "write it as a test"; the click's plan, the conservation section's blinds B1 to B5 and B7 with C1's and C5's lines; the folder examples/events/chain holds the declaration and the lays as the test's fixtures, its blinds asserted here on every run of tools/check.py and never read from a run's table): one law-quantum of light at k = pi / 4 on two bodies of three Nodes along a chain of 96 with receding faces, each body taking the light into e over a window of 48 from the first lit interval and giving it back as a source in time at the lifetime 48; the six worlds the chain under the six signed permutations that carry a chain to a chain; the seventh the detuned packet of the window's length. Rule3 plus the one act conserve the count, the form, the momentum, the inverse and the 48, with no world-specific code and nothing at the Node. The first run of this test (1be7429) found the fold's sense not covariant under the mirror at a tie (a defect, fixed the same day: the geometric sense, `twist.twisted`) and B7's bound wrongly drawn (corrected by derivation after that first run had read 3 of 8, the correction the derivation's and no fit); both are named in the folder's document."""

import json
import time

import numpy as np

from event_universe import readings, twist
from event_universe.lattice import Lattice
from tests.laws import BACK, EVENTS, d4_bound, drift_bound, family
from tests.laws_read import load_shipped

CHAIN = EVENTS / "chain"
DESIGN = json.loads((CHAIN / "design.json").read_text(encoding="utf-8"))
LAID = json.loads((CHAIN / "lay_bounds.json").read_text(encoding="utf-8"))
AXES = "xyz"
RUNS: dict[str, tuple[list[dict], dict[tuple[int, int], tuple[np.ndarray, ...]]]] = {}


def momentum_in_t(board: Lattice, index: int, at: np.ndarray | None = None) -> int:
    """A family's lattice momentum along the chain's axis in T's unit, over the board or over the Nodes `at` names (`readings.momentum_of`, `twist.scaled`)."""
    weight = board.families[index].pair[0]
    lines = [line for r in range(board.families[index].record) for line in board.lines_of(index, r)]
    read = readings.momentum_of(weight, lines, board.wrap, at)
    return twist.scaled(read, weight)[0]


def difference(board: Lattice, light: int) -> int:
    """D7's signed difference at the first source's Node this interval, before_(i-x) - before_(i+x) on the light's line, 0 with no source: an increment d at the Node changes P_x by 2 d times it in T's unit (`momentum_of` counts each Link from both ends)."""
    if not board.credit.sources:
        return 0
    at = np.add(board.credit.sources[0].at, board.offset)
    before = board.states[light].lines[0].before
    low, high = (at[0] - 1, at[1], at[2]), (at[0] + 1, at[1], at[2])
    return int(before[low]) - int(before[high])


def shares_about_the_front(board: Lattice, light: int) -> tuple[int, int]:
    """The light's share behind the latest front and ahead of it, in the current's unit: behind it the Nodes nearer its origin than the intervals since it began less the face's two, the shells it has erased, where the live light stands (a quantum laid behind the front); ahead of it the shells being faced and the levels it has still to erase, the front's span (D6); the whole share and 0 with no front. On this receding board a wave moving away from the hole at the group velocity is caught late, and a ripple of one level from the lay's edge runs ahead of every front below the credit's rounding."""
    found, _frozen = board.share_of(light)
    front = max(board.credit.fronts, key=lambda f: f.since, default=None)
    if front is None:
        return int(found.sum(dtype=object)), 0
    positions = np.indices(board.shape)[0] - int(board.offset[0])
    behind = np.abs(positions - int(front.origin[0])) <= board.interval - front.since - 2
    return int(found[behind].sum(dtype=object)), int(found[~behind].sum(dtype=object))


def run(name: str, intervals: int) -> tuple[Lattice, list[dict], list[dict]]:
    """A chain world run `intervals` intervals from the lay with every interval's books of the light and the bodies kept beside the output lines."""
    board = Lattice(load_shipped(CHAIN / f"{name}.json"), (lines := []).append)
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
                "sources": len(board.credit.sources),
                "P_light": momentum_in_t(board, light),
                "P_bodies": [
                    momentum_in_t(board, atom, board.mask(b.nodes)) for b in board.credit.bodies
                ],
                "increments": [list(s.increments) for s in board.credit.sources],
                "about": shares_about_the_front(board, light),
                "diff": difference(board, light),
                "drift": drift_bound(board, light),
            }
        )
    return board, lines, marks


def test_the_chain_conserves_the_count_the_form_and_the_momentum_through_the_pair():
    """B1, B2 and B3 with C1's and C5's lines on chain_x_minus over its 400 intervals (the blinds written before the run, examples/events/chain/expectation.json; no measured number inside them): B1, at every absorption the light's count falls by 1 and the body's e rises by 1 as its g falls by 1, at every emission the reverse, exactly, and outside the fronts' and the sources' spans the light's share in whole quanta over its own unit W_rec equals its count, the front's span read from the board: at every interval outside a source's span the light's share behind the latest front, the shells it has erased, is the live light and in whole quanta equals the count, and the share ahead of it is the levels the front has still to erase, the span, decreasing as the front catches them (`shares_about_the_front`; on this receding board the front itself never ends, its shells reaching the growing faces, a wave moving away from the hole at the group velocity is caught late, the first emission's half toward +x erased by the second absorption's front over about 200 intervals, and a ripple of one level from the lay's edge runs ahead of every front below the rounding; the whole share equals the count where nothing stands ahead, before the first click); C1, the count 1 and the quanta 1 at the lay and again after the emission's span; C5, no body takes the light it is itself sourcing (no absorption line names its own body as the source); B2, the board's form after the pair of one absorption and one emission within D7's bound of its value before, 3 den SUM_t (|a_t| + 1 / 4) over the source's increments, the light's I = Q / W_rec at 1 within the lay's own rounding at the lay, 2 x 3 den (2 A + 1) per lit Node (the amplitude's form, its two products), and within D7's bound after the span; B3, at every absorption the body's own P moves by the piece less the shortfall, p_a = gain_a + s_a, within D4's bound in the amplitude form, 4 A + 2 per line per Link along the axis (lay_bounds.json, 2352 in T's unit; the lay's phase-0 value 902 of `tests.laws.d4_bound` the consistency pin), the body's P is kept through its emission within the same bound, and the light's P after the source's span is the emitted light's alone (the absorbed quantum's fan, carrying its P until the front reaches it, is erased over the span, D6, its P the taker's since the click, "P lost to the taker"), equal to D7's identity term, 2 SUM_t a_t (before_(i-x) - before_(i+x)) at the source's Node in T's unit (an increment d at a Node moves P_x by 2 d times the neighbours' difference exactly, `momentum_of` counting each Link from both ends), plus the integers' floors over the span (D1), within the hands' bound of their sum, 2 SUM_i |now_(i+1) - now_(i-1)| per interval (`tests.laws.drift_bound`). FINDING by name (2026-10-19, the cold reader's three causes told apart and printed): the identity's term is 0, the source standing on a region the front erased before the emission, and the light's P after the span reads 30 in T's unit: Rule3's floors over the span on a row asymmetric as a whole, the absorbed fan toward -x erased during it (the third cause; not the front unfinished at the emission as such, and not the increments, laid at one Node). The run's seconds printed. Under the eighth commit of the read (2026-10-20, the carried span dropped where the body left its part) body 1 absorbs at 142 inside body 0's emission span, so the lines at the span's end 170 derive rather than pin: the count 1 less the takes inside the span (0), the share the count plus the share still ahead of the front in quanta (1), the form less the taken units plus the share ahead within D7's bound (913,836 against 9,972,000), the live light behind the front the count's; B2 is read where no front erases and no source lays (G's line of the same day, the reader's ruling after the eighth, 2026-10-20: ALGEBRA's conservation at the click, line by line, the front taking the record to 0 shell by shell and the emission's lay giving W_rec over the source's increments): the take's unit leaves as the front erases its fan over its travel and the give's is laid over the source's span, so Rule3's conservation holds on the calm stretches alone, 1 to 73 and after body 1's emission span to 302, each within D7's bound of its start with no click inside; the two complete pairs back within one bound at 302 with the live light one unit; the third pair (303, 351) is not read, its front still erasing at the run's end; the pins before, (1, 1) at 170 and the share one unit there, read a span with no other click in it."""
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
    live = [m for m in marks if m["sources"] == 0]  # outside the sources' spans
    half = unit // 2  # the credit's rounding
    assert live and all(
        (m["about"][0] + half) // unit == m["count"] for m in live
    )  # B1 within the reach
    quiet = [
        m for m in live if m["about"][1] == 0
    ]  # outside the fronts' spans too: before the first click
    assert quiet and all(m["quanta"] == m["count"] for m in quiet)  # B1: the whole share the count
    assert (marks[0]["count"], marks[0]["quanta"]) == (1, 1)  # C1 at the lay
    # B2 and B3 over the first pair: the absorption at t_a, the emission at t_e, its span tau
    t_a, t_e = clicks[0]["interval"], clicks[1]["interval"]
    increments = by_interval[t_e]["increments"][0]
    tau = len(increments)
    bound_q = 3 * den * sum(abs(a) for a in increments) + (3 * den * tau) // 4  # D7's form bound
    rest = by_interval[t_e + tau]
    assert rest["sources"] == 0
    # B2 (G's line of 2026-10-20, the reader's eye on it): the take's unit leaves the board as the front erases its
    # fan (D6) and the give's unit is laid by the source over its span (D7), so Rule3's conservation reads where no
    # front is erasing and no source is laying: the calm stretches (no source, the levels ahead of the fronts within
    # the bound), each held within D7's bound of its own start with no click inside
    calm = [
        t
        for t in sorted(by_interval)
        if by_interval[t]["sources"] == 0 and by_interval[t]["about"][1] <= bound_q
    ]
    edges = {c["interval"] for c in clicks}
    stretches: list[list[int]] = []
    for t in calm:
        if stretches and t == stretches[-1][-1] + 1 and t not in edges:
            stretches[-1].append(t)
        else:
            stretches.append([t])
    long = [s for s in stretches if len(s) > 20]
    assert len(long) >= 2 and long[0][0] == 1 and long[0][-1] == t_a - 1, [(s[0], s[-1]) for s in long]
    for s in long:
        assert all(abs(by_interval[t]["form"] - by_interval[s[0]]["form"]) <= bound_q for t in s), (
            s[0],
            s[-1],
        )
    # at the span's end: the form less the units taken inside the span plus the share still ahead of the front
    taken_inside = [c for c in clicks if c["absorbed"] and t_e < c["interval"] <= t_e + tau]
    assert (
        abs(rest["form"] - by_interval[t_a - 1]["form"] + unit * len(taken_inside) - rest["about"][1])
        <= bound_q
    )
    assert rest["count"] == 1 - len(taken_inside)  # C1 after the span, derived: the take inside the span
    assert rest["quanta"] == rest["count"] + (rest["about"][1] + half) // unit
    assert (
        abs(rest["about"][0] - unit * rest["count"]) <= bound_q
    )  # the live light behind the front, the count
    back = by_interval[
        clicks[4]["interval"] - 1
    ]  # 302: the two complete pairs back, the third pair not read
    assert abs(back["form"] - by_interval[t_a - 1]["form"]) <= bound_q and back["count"] == 1
    assert abs(back["about"][0] - unit) <= bound_q  # I = 1: the live light behind the front one unit
    fresh = Lattice(load_shipped(CHAIN / "chain_x_minus.json"))  # the lay, no interval stepped
    laid = fresh.states[light].lines[0].now.reshape(-1)
    lit, amplitude = sum(1 for v in laid if v != 0), max(abs(int(v)) for v in laid)
    bound_lay = (
        2 * 3 * den * (2 * amplitude + 1) * lit
    )  # the lay's rounding, the two products of the form
    assert abs(marks[0]["share"] - unit) <= bound_lay  # I = 1 at the lay
    body = int(clicks[0]["node_detector"].split()[1])
    nodes = board.credit.bodies[body].nodes
    at = sorted(c["interval"] for c in clicks)
    piece, short = clicks[0]["momentum"][0], clicks[0]["shortfall"][0]
    gain = piece + short if piece < 0 else piece - short  # p_a = gain_a + s_a, s_a at or above 0
    assert short >= 0 and abs(gain) + short == abs(piece)
    moved = by_interval[t_a]["P_bodies"][body] - by_interval[t_a - 1]["P_bodies"][body]
    bound_p = LAID[0]["bodies"][body]["D4_amplitude_form_T_unit"][0]  # 4 A + 2 per line per Link
    assert d4_bound(fresh, atom, nodes)[0] == LAID[0]["bodies"][body]["D4_bound_T_unit"][0]  # the pin
    assert abs(moved - gain) <= bound_p, (moved, gain, bound_p)  # B3 at the absorption
    kept = by_interval[t_e]["P_bodies"][body] - by_interval[t_e - 1]["P_bodies"][body]
    assert abs(kept) <= bound_p, (kept, bound_p)  # B3 through the emission (C3)
    span = [(k, by_interval[t_e + k]) for k in range(tau) if t_e + k in by_interval]
    identity = 2 * sum(increments[k] * m["diff"] for k, m in span)  # D7: 2 d (b_(i-x) - b_(i+x))
    floors = sum(m["drift"] for _k, m in span)  # D1 over the span's steps, the hands' bound
    assert abs(rest["P_light"] - identity) <= floors, (rest["P_light"], identity, floors)
    fan = by_interval[t_e - 1]["P_light"]  # the absorbed quantum's fan at the emission (D6)
    print(
        f"the chain world: {len(clicks)} clicks in {DESIGN['intervals']} intervals, the pair at {t_a} and {t_e} "
        f"(the piece {piece}, the shortfall {short}, the body's P moved {moved} against the gain {gain} and {kept} "
        f"through the emission, D4's amplitude form {bound_p}; the form over the pair moved "
        f"{rest['form'] - by_interval[t_a - 1]['form']} within {bound_q}; the light's P after the span "
        f"{rest['P_light']} against D7's identity term {identity}, within the floors' bound {floors}; the fan's P at "
        f"the emission {fan}, erased by the front over the span; the source at one Node); B1 live on "
        f"{len(live)} intervals and whole on {len(quiet)}, the remnants ahead of the fronts before each click "
        f"{[round(by_interval[t - 1]['about'][1] / unit, 2) for t in at[1:]]} quanta; "
        f"{time.perf_counter() - started:.1f} s"
    )


def test_the_chain_runs_back_through_its_absorption_and_emission():
    """B4, the inverse: tools/back_in_time.py's verdict on chain_x_minus over the first 100 intervals, through the first absorption (74) and the emission that follows (91), MATCH bit for bit: every array returns through the click's two writes, the fold and the lay lines."""
    found = BACK.verdict(Lattice(load_shipped(CHAIN / "chain_x_minus.json")), 100)
    assert found["verdict"] == "MATCH" and found["intervals"] == 100, found


def carried(board: Lattice, array: np.ndarray, axis: str, toward: str) -> np.ndarray:
    """An image world's array brought back to the original's frame: the chain's axis moved to x and, for the light toward the upper side, the coordinate mirrored."""
    moved = np.moveaxis(array, AXES.index(axis), 0)
    return moved[::-1] if toward == "plus" else moved


def image(name: str) -> tuple[list[dict], dict[tuple[int, int], tuple[np.ndarray, ...]]]:
    """A world run over the design's intervals and carried back to the original's frame: its credit lines with the vector keys' chain component moved to x and signed (the shortfall a magnitude), and every line's now, before and remainder per family and line; run once per process (`RUNS`)."""
    if name not in RUNS:
        axis, toward = DESIGN["worlds"][name]
        board = Lattice(load_shipped(CHAIN / f"{name}.json"), (lines := []).append)
        for _ in range(DESIGN["intervals"]):
            board.step()
        a, sign = AXES.index(axis), -1 if toward == "plus" else 1
        clicks = []
        for c in lines:
            if c["event"] != "credit":
                continue
            line = dict(c)
            for key in ("momentum", "fan", "twist", "shortfall", "recoil"):
                if isinstance(line[key], list):
                    vector, flip = line[key], 1 if key == "shortfall" else sign
                    line[key] = [flip * vector[a], *(v for k, v in enumerate(vector) if k != a)]
            clicks.append(line)
        arrays = {
            (f, j): tuple(
                carried(board, x, axis, toward) for x in (line.now, line.before, line.remainder)
            )
            for f, state in enumerate(board.states)
            for j, line in enumerate(state.lines)
        }
        RUNS[name] = (clicks, arrays)
    return RUNS[name]


def one_world(names: list[str], original: str) -> int:
    """Every world of `names` equal to `original` in every click line and every cell of every line, brought back to one frame; the click lines' count."""
    clicks0, arrays0 = image(original)
    for name in names:
        clicks, arrays = image(name)
        apart = [
            (c["interval"], key)
            for c, c0 in zip(clicks, clicks0, strict=False)
            for key in c
            if c[key] != c0[key]
        ]
        assert len(clicks) == len(clicks0) and not apart, (name, len(clicks), len(clicks0), apart)
        assert arrays.keys() == arrays0.keys(), name
        for key, cells in arrays.items():
            for x, x0 in zip(cells, arrays0[key], strict=True):
                assert x.shape == x0.shape and np.array_equal(x, x0), (name, key)
    return len(clicks0)


def test_the_two_pure_permutations_are_the_original_bit_for_bit():
    """B5, the 48, the pure permutations: the chain along y and along z with the light toward the lower side, run over the design's 400 intervals and brought back by the inverse permutation, equal to chain_x_minus in every click line, every level and every remainder of every family, the draw's order the one named exception (the bodies' Node lists the images in the original's order, L812 untouched). The runs' seconds printed."""
    started = time.perf_counter()
    count = one_world(["chain_y_minus", "chain_z_minus"], "chain_x_minus")
    print(
        f"B5: the two pure permutations exact over {DESIGN['intervals']} intervals, {count} click lines; {time.perf_counter() - started:.1f} s"
    )
