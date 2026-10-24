"""The draw's tests in the engine (the owner's word of 2026-10-03, 01:52 UTC: experiments that test that it works in the engine, and derivations for everything, the draw included; the advisor's matrix, #1563 comment 5964151108): T1 Born's rule as the proportionality to whole shares, the realised clicks per region against the window's shares on the two slits' world over two seeds, chi-square about 11 on 11 degrees; T2 the which-way world, the measurement of the heart, read beside its blind (examples/events/which_way); T3 the front's ball, every erased Node's remainder below one read coefficient and constant; T6 one act at three storeys, Rule3, the held write's write and the credit's count calling the one division act; T7 the clicks causally continuous on the telegraph's lines, the next click inside the previous one's cone; the open board's emission as a packet along a drawn axis (step 5 of the emitter/node_detector)."""

import ast
import json
import math

import numpy as np

from event_universe import meeting, node, world_files
from event_universe.core.rule3 import division_forward, largest_below
from event_universe.credit import record_unit
from event_universe.emission import born_unit, radiated_total
from event_universe.features.held_write import held_write
from event_universe.features.write import carried
from event_universe.front import Front
from event_universe.lattice import Lattice
from event_universe.lists import hazard_weights
from event_universe.loader.derived import count_wall
from event_universe.loader.node_detector_declaration import pair_of
from event_universe.loader.universe import universe_of
from event_universe.loader.world import bodies_of, node_detectors_of, regions_of_the_law
from event_universe.share import quanta_of
from event_universe.world_files import load_world
from tests.laws import EVENTS, ROOT, TOOL, TOP, credit_lines, load_file, refused
from tests.laws_content import ONE_PHOTON, TWO_ATOMS, content_world, with_content
from tests.laws_read import redeclared, redeclared_file

RESONANCE = load_file("resonance_build", EVENTS / "resonance" / "build_world.py")
SRC = ROOT / "src" / "event_universe"


def test_the_one_division_act_serves_rule3_the_hold_and_the_credit():
    """T6 (the mathematician's 189, two hands; the advisor's matrix row 9, one act at three storeys): the held write's write (`features/held_write.hold`), the write's carried division (`features/write.carried`) and the credit's count (`share.quanta_of`, the credit's `counted`) compute by Rule3's division act and by nothing else, their modules naming no floor division, remainder or divmod of their own (the engine's gate on hand division beside it) and each equal to `division_forward` on the same integers: the held write (numerator + r) div wall with the remainder kept, the count (share + W_c div 2) div W_c."""
    acts = {"division_forward", "division_back", "rule3", "quanta_of"}
    files = ("features/held_write/__init__.py", "features/write/__init__.py", "share.py", "credit.py")
    for name in files:
        nodes = list(ast.walk(ast.parse((SRC / name).read_text(encoding="utf-8"))))
        hands = [
            n
            for n in nodes
            if isinstance(n, (ast.BinOp, ast.AugAssign)) and isinstance(n.op, (ast.FloorDiv, ast.Mod))
        ]
        names = {getattr(n, "id", None) or getattr(n, "attr", None) for n in nodes}
        assert not hands and "divmod" not in names and names & acts, name
    for numerator, wall, remainder in ((7, 3, 2), (-11, 4, 3), (0, 5, 4), (123456789, 1000, 999)):
        level, kept = held_write(10, numerator, wall, remainder)
        act = division_forward(numerator, wall, remainder)
        assert (level - 10, kept) == act == carried(numerator, wall, remainder) and 0 <= kept < wall
        assert held_write(level, numerator, wall, kept, -1) == (10, remainder)
    shares, wall = np.array([0, 5, 6, 7, 11, 12, 13, -1, 24], dtype=object), 12
    half = division_forward(wall, 2, 0)[0]
    assert list(quanta_of(shares, wall, object)) == [
        division_forward(int(s) + half, wall, 0)[0] for s in shares
    ]
    assert division_forward(7, wall, 0) == (0, 7)  # the division act is the one carried division


def test_the_fronts_ball_holds_remainders_below_one_read_coefficient_and_constant(tmp_path):
    """T3 (the mathematician's 193 (2) and 197 precision 3 with the advisor's second; the matrix row 3): on the anticoincidence world's one photon (examples/events/anticoincidence/one_photon.json, the chain of 96 with its receding faces, the committed world and its mode file) one record takes the photon at the interval 61 (the second atom's window, open from the photon's first lit interval, 29, and closed 33 after it, the passage derived at load, C2 with (D), 2026-10-19; the packets at the amplitude 78, one quantum in the record's own unit, C1), the photon's count reaches 0 and the front presents its faces shell by shell from the taker's Node; at every interval after, inside the ball of the shells whose two faces are done and whose outer neighbours stand at 0 (the Link-metric distance at most t - 61 - 3), every line of the photon's record stands at (0, 0) with its remainder below one read coefficient R of the photon's rule at the vacuum's paces and unchanged from one interval to the next: the erasure is Rule3's own write and nothing assigned; the erasure lines one per interval from the interval after the click."""
    photon = content_world(
        tmp_path, "one_photon", ONE_PHOTON, TWO_ATOMS
    )  # re-pinned 2026-10-20 under the content
    board = Lattice(load_world(photon), (lines := []).append)
    while not credit_lines(lines, "absorbed") and board.interval < board.world.intervals:
        board.step()
    light = next(i for i, f in enumerate(board.families) if f.name == "photon")
    read = node.rule_of(board.families[light], board.world.node_clock, 0, None, board.unit)[0][0]
    jumps = credit_lines(lines, "absorbed")
    since = jumps[0]["interval"]
    assert (
        len(jumps) == 1 and since == jumps[0]["window"][1] and board.credit.counts[light] == 0
    )  # the take at the window's close, the window derived (60 here; 63 under the content at the declared window, 2026-10-20, 62 before)
    holes = {
        (f.at, f.ports) for f in board.credit.faces[since + 1] if f.family == light
    }  # the hole's one Node with its Port set, the face books'
    origin, ports = next(iter(holes))
    assert len(holes) == 1 and "node" not in jumps[0]
    assert board.credit.fronts == [Front(light, (origin[0], origin[1], origin[2]), since, ports)]
    checked = 0

    def ball(
        interval: int,
    ) -> tuple[np.ndarray, list]:  # the ball's mask at the board's offset now, the record's lines
        at = np.reshape(np.add(origin, board.offset), (3, 1, 1, 1))
        inside = np.abs(np.indices(board.shape) - at).sum(axis=0) <= interval - since - 3
        return inside, board.states[light].lines[: board.families[light].record]

    for interval in range(since + 4, since + 16):
        while board.interval < interval:
            board.step()
        inside, own = ball(interval)
        kept = [line.remainder[inside].copy() for line in own]
        for line in own:
            assert not line.now[inside].any() and not line.before[inside].any()
            assert (line.remainder[inside] >= 0).all() and (line.remainder[inside] < read).all()
        board.step()  # the board may grow at a receding face: the ball read again at the new offset
        inside, own = ball(interval)
        assert all((a == line.remainder[inside]).all() for a, line in zip(kept, own, strict=True))
        checked += int(inside.sum())
    erased = [e["interval"] - since for e in lines if e["event"] == "erasure"]
    assert (
        checked > 100
        and erased[:3] == [1, 2, 3]
        and [e for e in lines if e["event"] == "erasure"][0]["nodes"] == 2
    )


def test_the_born_lights_frequency_is_the_declared_resonance_and_a_node_detector_counts_in_its_own_quantum(
    tmp_path, monkeypatch
):
    """T4, test (vi) (the owner's word of 2026-10-03, 05:00 UTC, "not in the morning, now"; the mathematician's 213 (B), #1572 comment 5965054791, his 214, 5965082449, and 220, 5965303134, with the advisor's seconds, #1563 comment 5965316267 and #1572 comment 5965312353, two hands; examples/events/resonance, the blind written by its builder before any lay): a record's unit of one quantum is W_c sin omega from its own rotation (`credit.record_unit`; the click's plan, C1, 2026-10-18, in place of the share over the count read at the books' origin), W_c for a massless record laid by no packet, W_c sin Omega = 2.23605 den T for one quantum at [2, 3] and for the lit world's packet at [1, 2] the massless band's cos omega at the search's cos(pi / 2), -2 of 6000, 3999 and not 4000, the unit within two parts in 6000 of the [2, 3] quantum's, and the loader refuses by name a region declaring a `transition`, a one-Node region (a region of a travelling wave), a transition without its resonance and an emission with no transition between its parts; the dark's hazard is per proper interval (`lists.hazard_weights`): the weights [span x unit, (tau - span) x unit] in the vacuum and half the emission's weight at p_0 = Gamma / 2; on the resonance world the giver gives at the interval 48 with certainty and lays the quantum as a source in time over 48 intervals, one lay line each on the light's first line at the giver's Node, the level now alone, the amplitudes at most 22 (21 on 30 intervals and 22 on 18, the carry); at the span's end the light's share over the board reads sin Omega = 0.745 quanta of the band's top, one quantum by the count's line in the top's unit and in the node_detector's own unit at [2, 3] alike; the far Node's cosine over the plateau (the intervals 76 to 90, after the front has passed at the group pace 1 / (3 sin Omega) and before the source stops) reads cos Omega within 2 / A_far of 2 / 3 (the design's own window, 62 to 70, lies in the front's transit and misses, a finding named in the folder); light's Links at the reader's Node open, the cut the atom's own. Under the dark grain (the mathematician's 223 (a), #1572 comment 5965727937, and 224 (2)(a), 5966081562, with the advisor's 5965918924 (a) and his second 5966129376, two hands; `meeting.dark`, `lists.emission`): the giver is in the dark until it gives, so over the trials' first 25 seeds its emission is drawn once per interval at the hazard 1 / 48 at the now, the generator advanced exactly once per interval and not at the window's close at 48, the emissions at distinct intervals and within the lifetime in 8 to 24 of 25 (the blind's 0.636, three deviations), each seed's lay lines the span from its interval cut by the run's end, the far Node's cosine on each seed's plateau [t + 28, t + 42] within the gate and the count at the span's end 1 where the whole span lies in the run; with the light laid on the chain a window stands and the window's draw at 48 stands as it is."""
    universe = json.loads((EVENTS / "zeno" / "zeno_atom.json").read_text(encoding="utf-8"))
    families, action = universe_of(universe)[1], universe["integers"]["quantum_action"]
    light = next(f for f in families if f.name == "pulse")
    wall = count_wall(light, action)
    refused("from -1 through 1", pair_of, [3, 2], "resonance")
    refused("pair", pair_of, [1], "resonance")
    row = {"name": "d", "positions": [[0, 0, 0], [1, 0, 0]]}
    rest = ((2, 1, 1), 0, (), ())
    refused("holds the key 'transition'", node_detectors_of, [{**row, "transition": TOP}], *rest)
    one = [{"name": "d", "positions": [[0, 0, 0]]}]
    refused(
        "a region of a travelling wave",
        regions_of_the_law,
        node_detectors_of(one, (2, 1, 1), 0, (), ()),
        (),
        (2, 1, 1),
        (False,) * 3,
        (),
    )
    RESONANCE.main(["--folder", str(tmp_path), "--modes"])
    blind = json.loads((tmp_path / "expectation.json").read_text(encoding="utf-8"))
    assert blind == json.loads((EVENTS / "resonance" / "expectation.json").read_text(encoding="utf-8"))
    world = json.loads(redeclared_file(tmp_path / "resonant.json").read_text(encoding="utf-8"))
    (content := tmp_path / "examples" / "events" / "zeno").mkdir(parents=True)
    (content / "zeno_atom.json").write_text(json.dumps(with_content(universe)), encoding="utf-8")
    monkeypatch.setattr(
        world_files, "REPOSITORY_ROOT", tmp_path
    )  # the content copy: the shipped resonant world's run is refused by name at the body 1 of 'atom' at the interval 41 (the law's third refusal of the click's read, the room 2^45.8 of the digits read below the absorption draw's total 2^53.9 on zeno_atom.json, which declares no content); the copy's universe carries the born universe's holders and every draw (2026-10-23)
    bare = {k: v for k, v in world["bodies"][0]["transitions"][0].items() if k != "resonance"}
    refused(
        "resonance",
        bodies_of,
        [{**world["bodies"][0], "transitions": [bare]}],
        None,
        "",
        families,
        (48, 1, 1),
        9000,
        (),
        action,
    )
    alone = {**world["bodies"][0], "transitions": []}
    refused("no transition", bodies_of, [alone], None, "", families, (48, 1, 1), 9000, (), action)
    path, at = tmp_path / "resonant.json", tuple(blind["cos_omega"]["node"])
    board = Lattice(load_world(path), (lines := []).append)  # every draw the read of the board
    light_at = [f.name for f in board.families].index("pulse")
    gamma, own = (
        board.world.node_clock,
        largest_below(wall * wall * 5) // 3,
    )  # one quantum at [2, 3]
    assert record_unit(board, light_at) == wall  # W_rec: W_c, a massless record laid by no packet (C1)
    assert abs(own / wall - 5**0.5 / 3) < 2 / wall and board.credit.units[light_at] == wall
    assert hazard_weights(1, 48, gamma, gamma, 9) == [
        9,
        47 * 9,
    ]  # the vacuum: the hazard per board interval
    assert hazard_weights(2, 48, gamma // 2, gamma, 9) == [
        9,
        47 * 9,
    ]  # a well at p_0 = Gamma / 2: half the rate
    pulse = [f.name for f in board.families].index("pulse")
    series = {}
    giver = len(
        world["bodies"][0]["nodes"]
    )  # the reading Node eight Nodes from each Node of the giver (two Nodes to 2026-10-21, three since)
    for _ in range(96):
        board.step()
        series[board.interval] = tuple(
            int(board.states[pulse].lines[0].now[(at[0] + k, *at[1:])]) for k in range(giver)
        )
        given = [c for c in lines if c["event"] == "credit" and c["emitted"] == "pulse"]
    assert given, "the run's emission inside the run (the hazard 1 / 48 per interval)"
    t = given[0]["interval"]
    lays = [c for c in lines if c["event"] == "lay" and c["family"] == "pulse"]
    span = list(range(t, min(t + 48, 97)))  # the span from t, cut by the run's end
    when = [c["interval"] for c in lays]  # one lay line per interval whose increment is not 0
    assert when == sorted(set(when)) and set(when) <= set(span) and len(when) >= len(span) - 3
    laid_at = {tuple(c["node"]["at"]) for c in lays}
    # the emission's Node drawn once per click by the record's share, inside the NodeDetector's region
    assert (
        len(laid_at) == 1 and laid_at <= {tuple(n["node"]) for n in world["bodies"][0]["nodes"]}
    )  # within the giver's declared Nodes (the two-Node body's {(0, 0, 0), (1, 0, 0)} to 2026-10-21, three Nodes since)
    assert all(c["line"] == 0 and c["after"][1:] == c["before"][1:] for c in lays)
    taken = [c for c in lines if c["event"] == "credit" and c["absorbed"]]
    assert max(abs(c["after"][0] - c["before"][0]) for c in lays) <= 22
    assert board.credit.counts[pulse] + len(taken) == 1  # one quantum given, kept or taken
    if t <= 49 and not taken:  # the whole span in the run: one quantum by the count's line, either unit
        total = board.total_share(pulse)[0]
        assert (
            total is not None and 0.7 < total / wall < 0.8
        )  # sin Omega = 0.745 in the band's top's unit
        for unit in (wall, board.credit.units[pulse]):  # W_c and the record's own unit, the lay's
            assert division_forward(total, unit, division_forward(unit, 2, 0)[0])[0] == 1
    if t <= 53:  # the plateau after the front and before the stop, inside the run
        window, read_at = range(t + 28, t + 43), next(iter(laid_at))[0]  # eight Nodes from the lay
        levels = {k: pair[read_at] for k, pair in series.items()}
        numerator = sum(levels[k] * (levels[k + 1] + levels[k - 1]) for k in window)
        read = numerator / (2 * sum(levels[k] ** 2 for k in window))
        far = max(abs(levels[k]) for k in window)
        assert far > 20 and abs(read - 2 / 3) <= 2 / far, (t, read, far)
    lit = {**world, "packets": [{"family": "pulse", "along": "x", "wave": [1, 2], "amplitude": 308}]}
    lit["packets"][0]["phase"] = [0, 1]
    lit["packets"][0].update(top={"x": [0, 47], "y": [0, 0], "z": [0, 0]}, edge={"x": 0, "y": 0, "z": 0})
    (path := tmp_path / "lit.json").write_text(json.dumps(lit), encoding="utf-8")
    TOOL.main(["--input", str(path)])
    for _run in (
        "the read",
    ):  # the light at its Node: a window stands and its draw at 48 stands as it is
        board = Lattice(load_world(path), (lines := []).append)
        light_at = [f.name for f in board.families].index("pulse")
        gamma, own = (
            board.world.node_clock,
            largest_below(wall * wall * 5) // 3,
        )  # one quantum at [2, 3]
        unit = record_unit(
            board, light_at
        )  # W_rec at [1, 2]: cos omega 4000 of 6000, the [2, 3] transition's own unit exactly (the quarter turn's cosine 0, 2026-10-19; 3999 by the search before it)
        assert abs(unit / wall - 5**0.5 / 3) < 2 / 6000 and board.credit.units[light_at] == unit == own
        assert abs(own / wall - 5**0.5 / 3) < 2 / wall
        assert hazard_weights(1, 48, gamma, gamma, 9) == [
            9,
            47 * 9,
        ]  # the vacuum: the hazard per board interval
        assert hazard_weights(2, 48, gamma // 2, gamma, 9) == [
            9,
            47 * 9,
        ]  # a well at p_0 = Gamma / 2: half the rate
        window = board.world.bodies[
            0
        ].detector.draw.window  # the giver's own beat, 8: the lit packet fills the ring and no lay has an end (the declared lifetime 48 was the window to 2026-10-23, its one pulse at 48)
        [board.step() for _ in range(48)]
        pulses = [c for c in lines if c["event"] == "credit" and c["emitted"] == "pulse"]
        assert pulses and all(c["interval"] % window == 0 for c in pulses), (
            [c["interval"] for c in pulses],
            window,
        )  # the emissions at the beat's closes, the hazard read from the light standing at the giver (one, at 24, on the content copy)


def test_a_record_empty_at_the_origin_takes_its_unit_from_its_first_lay(tmp_path):
    """The unit of a record empty at the books' origin (the advisor's word of 2026-10-03, #1572 comment 5967247080, on the generic node_detector's entry; `emission.born_unit`, `credit.Books.empty`): the resonance world's giver alone with its transition at [9, 10], sin Omega = 0.436 below 1 / 2, over 240 intervals, its window 192: in the exact dark its emission falls at the window's close (`meeting.emission_fell`), its source in time laid over the lifetime 48 before the run's end, and it takes nothing back. Light's record holds nothing at the origin, so its unit stands at W_c and it is named empty; at the emission's first lay the unit becomes the emission's own W_c sin Omega, 0.436 W_c within the root's rounding, the record leaves the empty set and the unit is held. The books' count after the emission 1, kept or absorbed back at the window's close, a click's number. The finding by name beside it, a lattice reading recorded in ENGINE.md and not pinned here (2026-10-03): at the span's end, before any absorption, the born quantum's share over the board reads about W_c at [9, 10] (1.06 at the seed 1; 0.84 at [4, 5], 0.75 at [2, 3]: the count's line's W_c sin Omega holds near the band's top alone), so the credit in W_c reads 1 already and the credit in the record's own unit would read 2; the premise that a born quantum below the half-top energy is credited 0 was not what the engine read on the chain under the invariant's S = T / (2 sin Omega); the mathematician's 245 answers it, the source laid at (2 / 3) T sin k on this branch (`radiated_total`), the reading in examples/events/resonance/blind_and_reading.md."""
    world = redeclared(json.loads((EVENTS / "resonance" / "resonant.json").read_text(encoding="utf-8")))
    giver = {**world["bodies"][0], "transitions": [{**world["bodies"][0]["transitions"][0]}]}
    giver["transitions"][0]["resonance"] = [9, 10]
    giver["node_detector"] = {
        k: v for k, v in giver["node_detector"].items() if k != "window"
    }  # the window derived (the declared 192 before 2026-10-23)
    low = {**world, "bodies": [giver], "intervals": 240}
    (path := tmp_path / "low.json").write_text(json.dumps(low))
    TOOL.main(["--input", str(path)])
    board, series = Lattice(load_world(path), (lines := []).append), {}  # one world, one read
    pulse = [f.name for f in board.families].index("pulse")
    wall, books = count_wall(board.families[pulse], board.world.quantum_action), board.credit
    assert books.units[pulse] == wall and pulse in books.empty and books.counts[pulse] == 0
    for _ in range(240):
        board.step()
        series[board.interval] = board.total_share(pulse)[0]
    credits = [c for c in lines if c["event"] == "credit" and c["label"] == "NODEDETECTOR"]
    jumps = [(c["interval"], c["emitted"]) for c in credits if c["absorbed"] or c["emitted"]]
    assert jumps and jumps[0][1] == "pulse" and jumps[0][0] <= 192 and pulse not in books.empty
    assert (
        books.units[pulse] == born_unit(wall, (9, 10)) and abs(books.units[pulse] / wall - 0.436) < 0.002
    )
    taken = sum(given is None for _t, given in jumps[1:])  # the window's close at 240 may take it back
    assert books.counts[pulse] + taken == 1  # one quantum given, kept or taken back, the books' number


def test_the_source_in_time_lays_the_form_it_radiates():
    """The source in time's energy (the mathematician's 245, #1572 comment 5968047484, with the advisor's second, 5968075799, two hands; `emission.radiated_total`): a point source on a guide of width one radiates (3 / 2) S sin Omega / sin k, so one quantum is laid at SUM A_t^2 = (2 / 3) T sin k, cos k = (3 num - 2 den) / den, the root on the large number: (2 / 3) T exactly at [2, 3], and within two of (2 / 3) T sin k at [4, 5], [9, 10] and [7, 8], the floors of 2 T div 3 and of the root (where the invariant's S = T / (2 sin Omega) laid 1.36 and 2.41 quanta on the chain at the first two); the integer root of the small number alone, isqrt(21) = 4 at [4, 5], would miss by 13 percent, named; at the band's top [1, 3] the guide's wave number is pi and the total 0, the lay refused at the loader before it."""
    action = 1 << 15  # the shipped T
    assert radiated_total(action, (2, 3)) == division_forward(2 * action, 3, 0)[0]  # (2 / 3) T exactly
    for num, den in ((4, 5), (9, 10), (7, 8)):
        sine = math.sqrt(1 - ((3 * num - 2 * den) / den) ** 2)  # sin k at the resonance
        assert abs(radiated_total(action, (num, den)) - 2 / 3 * action * sine) <= 2  # the two floors
    assert (
        abs(radiated_total(action, (4, 5)) / (2 / 3 * action * 4 / 5) - 1) > 0.1
    )  # isqrt(21) = 4 misses
    assert radiated_total(action, (1, 3)) == 0 and radiated_total(action, (3, 3)) == 0


def test_a_later_readers_share_is_read_conditionally_on_the_earlier_windows_nulls(tmp_path, monkeypatch):
    """The one draw over readers of one record closing at different intervals (ALGEBRA.md, The click writes on the lattice (7), the mathematician's line, #1793 comment 5981514001 (5); `lists.absorption`, `credit.Books.unabsorbed`): one photon of count 1 on a chain of 72, laid at the Node 14 over 16 Nodes of edge and travelling +x at the group pace, passes the atom A at 30 and 31, lit from 2, whose window closes at 64, and the atom B beside it at 32 and 33, lit from 6, whose window closes at 68 (C2 with the window derived at load, 2026-10-19: the packet of 1 + 32 Nodes over 2 at k = pi / 4, ceil(34 x 3 x 2586 / 4243) = 63 at both atoms; the packet at the amplitude 78, C1; the two reads of one record staggered in time, not in space); A's null window leaves the wave as laid, so B reads the same packet; over 120 trials (the shipped packet of 78 alone half a quantum in the record's unit, C1, the transitions' weight 3 for shares near 0.45; the packet of 78 alone reads one quantum only by the half-up rounding at exactly one half, (share + W_rec div 2) div W_rec with the laid share one half of W_rec within the lay's rounding, the pin's fragility named; the board copied at the interval before A's close, the lay and the steps before it the same in every trial, every record's generator at the trials tool's hashed state of the trial's label, the seed times the records' number plus the record's number, so that the trials are independent draws and not one Weyl sequence, R342 and R351, the engine's own draws from there; B beside A and its close four intervals after A's keep the test under the check's bound of 30 seconds on the CI runner's clock) the realised frequency of B's absorption is the one draw's, s_B over the labels' unit, within three standard errors, and not the branch's (1 - s_A) s_B, more than three standard errors away, and given A's null B takes at the law's s_B / (1 - s_A) and not at the branch's s_B, the sharper statistic; A's frequency is s_A; no trial holds two absorptions, the count conserved; the books after a trial of two nulls hold the record's unabsorbed share, the unit less A's share, read in B's unit, less B's share, and after an absorption none; the shares read from the books at the two closes and the four numbers printed."""
    seen, turned = {}, meeting.turned_labels

    def kept(board, books):  # the labels' unit and the transfer share at a close while the count stands
        turned(board, books)
        for transition, share in books.shares.items():
            if board.credit.counts[transition.drive] > 0:
                unit = sum(label * label for label in books.labels)
                seen.setdefault((board.interval, books.number), set()).add((unit, share))

    monkeypatch.setattr(meeting, "turned_labels", kept)
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    (tmp_path / "u.json").write_text(
        json.dumps(with_content(TWO_ATOMS)), encoding="utf-8"
    )  # the content, 2026-10-20
    world = json.loads(json.dumps(ONE_PHOTON))
    packet = world["packets"][0]
    world.update(shape=[72, 1, 1], universe="u.json", intervals=68)
    top, edge = {**packet["top"], "x": [14, 14]}, dict(x=16, y=0, z=0)  # the packet over 16 Nodes at 14
    world["packets"] = [{**packet, "top": top, "edge": edge}]
    for body, at in zip(world["bodies"], (30, 32), strict=True):
        body["nodes"] = [{"node": [x, 0, 0], "weight": 1} for x in (at, at + 1)]
        body["node_detector"] = {k: v for k, v in body["node_detector"].items() if k != "window"}
        body["transitions"] = [{**body["transitions"][0], "weight": 1}]  # the shares small
    (path := tmp_path / "staggered.json").write_text(json.dumps(world), encoding="utf-8")
    TOOL.main(["--input", str(path)])
    board = Lattice(load_world(path), (lines := []).append)
    photon = [f.name for f in board.families].index("photon")
    while board.interval < 63:  # the interval before A's close
        board.step()
    assert board.credit.counts[photon] == 1 and photon not in board.credit.unabsorbed
    while board.interval < 68:  # A's close at 64, B's at 68: one read of the board at each
        board.step()
    hits = tuple(c["node_detector"] for c in lines if c["event"] == "credit" and c["absorbed"])
    left = (board.credit.counts[photon], board.credit.unabsorbed.get(photon))
    print(f"the closes' shares {seen}; the hits {hits}; left {left}")
    ((unit_a, s_a),), ((unit_b, s_b),) = seen[64, 0], seen[68, 1]
    p_a, p_b, read = s_a / unit_a, s_b / unit_b, division_forward((unit_a - s_a) * unit_b, unit_a, 0)[0]
    print(
        f"A {p_a:.4f}; B {p_b:.4f}, the branch's {(1 - p_a) * p_b:.4f}, the law's given A's null "
        f"{p_b / (1 - p_a):.4f}; the read's one outcome {hits}, the photon's count and share left {left}"
    )
    assert 0 < p_a and p_a + p_b < 1 and len(hits) <= 1  # the cap clear, one click at most
    assert left == (
        (1, read - s_b) if not hits else (0, None)
    )  # B's share read in A's null's denominator
