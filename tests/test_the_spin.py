"""The spin branch (2026-10-19, stacked on the click branch; ALGEBRA.md, Spin, closed for the paper as a route, and the derivation of the same day: under the 48 every line Rule3 steps is a scalar, no record carries a spinor, and the half angle is the detector's read of two planes under a basis it declares): a quantum of spin one half is a record of two planes as two parts of one record (the family's shape [2, 2], the parts laid as one event and never summed at a Node), and a detector declaring its `axis`, the half-angle pair (c, s) with the Bloch axis (2 c s, c^2 - s^2) / (c^2 + s^2) in the x-z plane, credits the quantum to one of its two ports, up or down the axis, by the joint credit's one form on the parts' plane sums; nothing at the Node. The worlds are the tests' own (`tests.laws.spin_world`), no run beyond them. The family `spin` is a toy by name (2026-10-19): massless ([6000, 6000]) and neutral, its parts laid alike with no second pair and each plane's Wronskian 0, a test of the detector's read of two planes and of no charge; the law's electron is a quantum of the matter family re-declared at the shape [2, 2] with the sense on each plane (the second pair a quarter period on, W = T / 2 per quantum), its packet lay a generator change named and not built (ALGEBRA.md, Spin, closed for the paper as a route)."""

import json
from dataclasses import replace
from fractions import Fraction

from event_universe import lists, meeting, world_files
from event_universe.lattice import Lattice
from event_universe.loader.derived import count_wall
from event_universe.loader.draw import ports_of, settings_of_the_law
from event_universe.loader.node_detector_declaration import parts_of
from event_universe.loader.universe import universe_of
from event_universe.loader.world import node_detectors_of
from event_universe.node_detector import credit_draw
from event_universe.world_files import input_digest, load_world
from tests.laws import TOOL, ion_world, refused
from tests.laws_spin import (
    BELL,
    IDENTITY,
    PORT,
    SINGLET,
    TRIALS,
    correlation,
    exclusion_world,
    joint_shares,
    sided,
    spin_world,
    trial,
)

SEEDS = (1, 2)  # the runs per axis; the draw's statistics are read from the engine's own draw below
DRAWS = 400


def test_a_two_plane_quantum_goes_up_or_down_the_declared_axis_by_the_half_angle(tmp_path, monkeypatch):
    """Stern and Gerlach on the board: one quantum of the two-plane family (the amplitude 90, the lay 75, the share 0.9994 of the record's unit, the count 1) laid in the equal-parts state (psi_1 = psi_2, the Bloch vector along +x), one region at the chain's lower end declaring its axis as the half-angle pair (c, s) with the identity pattern; at the window's close the whole quantum is credited to the plus port or the minus port, two beams and never a smear (one credit line, count 1, nothing left, `kept` the parts the realised port reads with a coefficient other than 0, no loss, the whole quantum at one port: at the z axis (1, 0) the + port (c, s) = (1, 0) reads part 0 alone and the - port (-s, c) = (0, 1) part 1 alone, so the two beams along z are the two parts themselves), with the share (c + s)^2 / (2 (c^2 + s^2)) = cos^2 of the half angle between the axis and the state, exact in the integers' rationals: 1 / 2 at the z axis (1, 0), 1 at the x axis (1, 1), 0 at -x (1, -1), 4 / 5 at (3, 1) and 9 / 10 at (2, 1); the shares read from the engine's `parts` lines by the reader's own arithmetic equal the formula exactly, every run's port is one the share allows, the engine's weights at each side (`meeting_back.side_weights`, `sided`) equal the chain rule's over the reader's shares exactly, and the engine's generator over the reader's shares (`node_detector.credit_draw`, the states hashed as the trials tool hashes them) gives the plus port within three binomial scatters of the share over 400 draws, exactly all or none along the state."""
    for axis, expected in (
        ((1, 0), Fraction(1, 2)),
        ((1, 1), Fraction(1)),
        ((1, -1), Fraction(0)),
        ((3, 1), Fraction(4, 5)),
        ((2, 1), Fraction(9, 10)),
    ):
        path = spin_world(
            tmp_path / f"axis_{axis[0]}_{axis[1]}", monkeypatch, {"left": (axis, IDENTITY)}
        )
        for seed in SEEDS:
            board, lines = trial(path, seed, 40)
            clicks = [c for c in lines if c["event"] == "credit"]
            assert len(clicks) == 1 and clicks[0]["node_detector"] == "left", clicks
            assert clicks[0]["count"] == 1 and clicks[0]["left"] == 0, clicks
            up, down = (shares := joint_shares(lines, {"left": (axis, IDENTITY)}))[(0,)], shares[(1,)]
            assert Fraction(up, up + down) == expected, (axis, up, down)  # the half angle's share, exact
            spin = [f.name for f in board.families].index("spin")
            sided(
                board, spin, shares, [PORT[c["realised"]] for c in clicks]
            )  # the one side's coherent read
            allowed = {"plus"} if expected == 1 else {"minus"} if expected == 0 else {"plus", "minus"}
            port = clicks[0]["realised"]
            assert port in allowed, (axis, port)
            coefficients = ports_of(axis, ((1, 0), (0, 1)))[port == "minus"]
            assert clicks[0]["kept"] == [
                k for k, e in enumerate(coefficients) if e != (0, 0)
            ]  # the parts the port reads
        plus = 0
        for state in range(DRAWS):
            board.credit.state = TRIALS.hashed_state(state, board.world.width)
            plus += credit_draw(board, [up, down]) == 0
        n, p = DRAWS, float(expected)
        assert abs(plus - n * p) <= 3 * (n * p * (1 - p)) ** 0.5, (axis, plus)
        print(f"spin: the axis {axis} credits up {plus} of {n} against the share {expected}")


def test_the_axis_is_the_planes_setting_and_the_basis_the_real_lines(tmp_path, monkeypatch):
    """The settings' law (`loader/draw.settings_of_the_law`, `loader/world.node_detectors_of`): a side of a record of planes declares `axis` and a side of a record of real lines declares `basis`, each refused by name on the other kind, the two together refused, a setting with no `pattern` refused, one pattern over laid records of both kinds refused, and a setting on a body's node_detector refused; the spin world loads with its axis, and the same world with `basis` in the axis's place (its mode file re-addressed to it) is refused by name."""
    path = spin_world(tmp_path, monkeypatch, {"left": ((1, 0), IDENTITY)})
    world = json.loads(path.read_text(encoding="utf-8"))
    universe = json.loads((tmp_path / "u.json").read_text(encoding="utf-8"))
    families = universe_of(universe)[1]
    spin, pair = ([f.name for f in families].index(n) for n in ("spin", "light_pair"))
    row, shape = world["node_detectors"][0], tuple(world["shape"])
    assert load_world(path).node_detectors[0].axis == (1, 0)
    refused("both `axis` and `basis`", node_detectors_of, [{**row, "basis": [1, 0]}], shape, 0, (), ())
    refused(
        "none is declared",
        node_detectors_of,
        [{k: v for k, v in row.items() if k != "axis"}],
        shape,
        0,
        (),
        (),
    )
    refused(
        "not on a body", node_detectors_of, [{"name": "d", "block": 0, "axis": [1, 0]}], shape, 1, (), ()
    )
    refused(
        "not on a body",
        node_detectors_of,
        [{"name": "d", "block": 0, "basis": [1, 0]}],
        shape,
        1,
        (),
        (),
    )
    refused(
        "no `pattern`",
        node_detectors_of,
        [{k: v for k, v in row.items() if k != "pattern"}],
        shape,
        0,
        (),
        (),
    )
    pattern = ((1, 0), (0, 1))
    refused(
        "declares `basis` for a record of planes",
        settings_of_the_law,
        [("left", (), (1, 0), pattern)],
        [spin],
        families,
    )
    refused(
        "declares `axis` for a record of real lines",
        settings_of_the_law,
        [("left", (1, 0), (), pattern)],
        [pair],
        families,
    )
    refused(
        "records of planes and of real lines",
        settings_of_the_law,
        [("left", (1, 0), (), pattern)],
        [spin, pair],
        families,
    )
    settings_of_the_law([("left", (1, 0), (), pattern)], [spin], families)  # the axis on planes stands
    settings_of_the_law(
        [("left", (), (1, 0), pattern)], [pair], families
    )  # the basis on real lines stands
    world["node_detectors"][0] = {**{k: v for k, v in row.items() if k != "axis"}, "basis": [1, 0]}
    (wrong := tmp_path / "wrong.json").write_text(json.dumps(world) + "\n", encoding="utf-8")
    mode = json.loads((tmp_path / "spin.mode.json").read_text(encoding="utf-8"))
    mode["world_digest"] = input_digest(world)
    (tmp_path / "wrong.mode.json").write_text(json.dumps(mode) + "\n", encoding="utf-8")
    refused("declares `basis` for a record of planes", load_world, wrong)


def test_the_singlet_reads_minus_the_cosine_of_the_axes_angle_and_breaks_the_bound_at_two_root_two(
    tmp_path, monkeypatch
):
    """The singlet on the board (the Boss's item (d), 2026-10-19): two packets of the two-plane family from the centre toward the two ends, half a quantum each, the two parts laid alike on both, the left region's pattern the identity and the right region's the singlet's [[0, 1], [-1, 0]] (the partner reads the parts crossed with one sign turned, the antisymmetric pair: through `ports_of` its + port reads (s, -c) and its - port (c, s), the identity's - port (-s, c), the overall sign invisible to the norm), each region its own `axis`; the joint credit over the window gives E(a, b) = -cos(theta_a - theta_b) exact in the integers' rationals from the engine's `parts` lines at the four Bell settings, -119 / 169, 119 / 169, -120 / 169, -120 / 169, so |S| = 478 / 169 (the photons' S with (a - b) in the place of 2 (a - b)); each side's marginal 1 / 2 whatever the partner's axis; at equal axes the shares of (+, +) and (-, -) are 0 exactly, the anticorrelation, and the combination realised is one of the two the shares allow (the generator over the reader's shares never one of the two at 0); the pair is one quantum of the record, each packet half of it (the amplitude 64, the lay 54, the two shares 1.0134 of the record's unit together), and every run credits the one quantum's two sides with the one combination drawn, one line each with the count 1, nothing left (`lists.region`); the engine's weights at each side (`meeting_back.side_weights`, `sided`) equal the chain rule's over the reader's shares exactly; the engine's generator over the reader's shares at (a, b) (`node_detector.credit_draw`, 400 hashed states) within three binomial scatters of each share."""
    found = {}
    for a in BELL[:2]:
        for b in BELL[2:]:
            sides = {"left": (a, IDENTITY), "right": (b, SINGLET)}
            path = spin_world(
                tmp_path / f"{a[0]}_{a[1]}_{b[0]}_{b[1]}", monkeypatch, sides, both=True, amplitude=64
            )
            board, lines = trial(path, 1, 40)
            clicks = [c for c in lines if c["event"] == "credit"]
            assert [c["node_detector"] for c in clicks] == ["left", "right"], clicks
            assert all(c["count"] == 1 and c["left"] == 0 for c in clicks), clicks
            shares = joint_shares(lines, sides)
            spin = [f.name for f in board.families].index("spin")
            sided(
                board, spin, shares, [PORT[c["realised"]] for c in clicks]
            )  # the sides' reads the chain's
            total = sum(shares.values())
            same, different = shares[0, 0] + shares[1, 1], shares[0, 1] + shares[1, 0]
            assert Fraction(same - different, total) == correlation(a, b), (a, b, shares)
            assert Fraction(shares[0, 0] + shares[0, 1], total) == Fraction(1, 2)  # the left marginal
            assert Fraction(shares[0, 0] + shares[1, 0], total) == Fraction(1, 2)  # the right marginal
            assert shares[tuple(PORT[c["realised"]] for c in clicks)] > 0, clicks
            found[a, b] = correlation(a, b)
            print(f"singlet: the axes {a} and {b} read E = {found[a, b]}, the shares {shares}")
    a, a2, b, b2 = BELL
    assert [found[a, b], found[a, b2], found[a2, b], found[a2, b2]] == [
        Fraction(-119, 169),
        Fraction(119, 169),
        Fraction(-120, 169),
        Fraction(-120, 169),
    ]
    assert abs(found[a, b] - found[a, b2] + found[a2, b] + found[a2, b2]) == Fraction(478, 169)
    sides = {"left": ((3, 1), IDENTITY), "right": ((3, 1), SINGLET)}
    board, lines = trial(
        spin_world(tmp_path / "equal", monkeypatch, sides, both=True, amplitude=64), 1, 40
    )
    shares = joint_shares(lines, sides)
    assert shares[0, 0] == shares[1, 1] == 0 and shares[0, 1] == shares[1, 0] > 0, shares
    clicks = [c for c in lines if c["event"] == "credit"]
    assert tuple(PORT[c["realised"]] for c in clicks) in {(0, 1), (1, 0)}, clicks
    keys, counts = sorted(shares), [0] * 4
    for state in range(DRAWS):
        board.credit.state = TRIALS.hashed_state(state, board.world.width)
        counts[credit_draw(board, [shares[key] for key in keys])] += 1
    assert counts[keys.index((0, 0))] == counts[keys.index((1, 1))] == 0
    sides = {"left": (a, IDENTITY), "right": (b, SINGLET)}
    board, lines = trial(
        spin_world(tmp_path / "draws", monkeypatch, sides, both=True, amplitude=64), 2, 40
    )
    shares, counts = joint_shares(lines, sides), [0] * 4
    keys, total = sorted(shares), sum(shares.values())
    for state in range(DRAWS):
        board.credit.state = TRIALS.hashed_state(state, board.world.width)
        counts[credit_draw(board, [shares[key] for key in keys])] += 1
    for key, count in zip(keys, counts, strict=True):
        p = shares[key] / total
        assert abs(count - DRAWS * p) <= 3 * (DRAWS * p * (1 - p)) ** 0.5, (key, count, p)
    print(f"singlet: the draw at {a}, {b} gives {dict(zip(keys, counts, strict=True))} of {DRAWS}")


def test_a_full_part_refuses_the_second_quantum_by_its_declared_capacity(tmp_path, monkeypatch):
    """The exclusion as the declared rule in the detector's lists (the Boss's item (e), 2026-10-19; `lists.full`, `loader/node_detector_declaration.parts_of`): one body of two quanta in g with two excited parts e and f of capacity 1 each, both fed by one drive at one weight and one resonance, two photons of one quantum each by the record's own unit (each at the amplitude 110 lays 252,384,000 of the unit 254,237,103, W_c sin omega at k = pi / 4, 0.9927, the two 1.9854: one quantum each by the unit and not by the rounding; on main's W_c of 589,824,000 the pair reads 0.856 and counts 1) arriving one window apart (`exclusion_world` above; the body's window the packets' passage derived at load, 33, the atom branch of 2026-10-19); the closes read from the absorption's list by a spy that names each close by the board's interval as the credit lines do (60 and 93) and whose own `unabsorbed_in` read is the identity, the engine's numbers untouched. At the first close the two transitions share the unit equally and nothing has the weight 0, so the first quantum is taken, into e or into f by the draw; at the second close the part taken is full and its transition stands at the weight 0 by the declaration, the open part at its own share (9,190,267,331,637,924, the same number the open part has without any capacity) and nothing at the rest of the drive's unabsorbed share, so the second quantum is never taken by the full part: it is taken by the open part (the counts [0, 1, 1]) or passes (one quantum in each of g and the part first taken, the photon's count 1 left), over three seeds (25 and 27 pass it, 33 takes it), both outcomes seen, and at every seed no part's count stands above its capacity, the exclusion's own line; with every excited part full the absorption's list reads the two transitions at 0 and nothing at the whole unabsorbed share, the engine's draw taking nothing, the quantum passing and the body transparent by its capacity, no refusal by the draw. The body starts with its two quanta in g alone (the loader admits the start's counts in one part) and after one absorption stands in g still, the part of the largest count, the first of a tie in the declared order (`act.written`, the engine's one-part convention), its transitions and rates read from the standing part alone, its second window drawing the transitions out of g; a populated excited part the body does not stand in neither emits nor transitions, the lists per populated part the atom branch's. Without the capacity the occupied part's share is the larger (32,480,538,067,122,084, the standing label's turn) and the two shares sum above the unabsorbed share, nothing at 0, so the second quantum is taken and piles into the occupied part at the seed where it does ([0, 2, 0]): the rule is the declaration's and not derived. The loader refuses a capacity of 0 and a count above its part's capacity; `full` reads a part at its capacity and never a part declaring none."""
    closes: list[tuple[int, list[int], int, int]] = []
    original = lists.absorption

    # each close of the absorption's draw: the weights, nothing's, and the unabsorbed share the list reads
    def kept(board, drive, outcomes):
        norms = [sum(label * label for label in books.labels) for books, _transition in outcomes]
        unit, unabsorbed = board.credit.unabsorbed_in(drive, norms)  # the list's own read, booked once
        found = original(board, drive, outcomes)
        weights = [a.weight for a in found[:-1]]
        closes.append((board.interval, weights, found[-1].weight, min(unabsorbed, unit)))
        return found

    monkeypatch.setattr(meeting.lists, "absorption", kept)
    open_share, standing = 9190267331637924, 32480538067122084
    ends = {}
    for seed in (25, 27, 33):
        closes.clear()
        path = exclusion_world(tmp_path / f"capacity_{seed}", monkeypatch, 1, seed)
        board = Lattice(load_world(path), (lines := []).append)
        books = board.credit.bodies[0]
        assert (books.part, books.counts, books.declared.capacities) == (0, [2, 0, 0], (None, 1, 1))
        for _ in range(board.world.intervals):
            board.step()
        taken = [c for c in lines if c["event"] == "credit" and c["absorbed"]]
        first = taken[0]["realised"]
        assert (taken[0]["interval"], taken[0]["before"], first in "ef") == (60, "g", True), taken
        interval, weights, rest, _unabsorbed = closes[0]
        assert interval == 60 and weights[0] == weights[1] > 0 and rest == 0, closes  # the first close
        full, open_part = (1, 2) if first == "e" else (2, 1)
        interval, weights, rest, unabsorbed = closes[1]
        assert (interval, weights[full - 1], weights[open_part - 1]) == (93, 0, open_share), closes
        assert rest == unabsorbed - open_share > 0, closes  # the excluded share goes to nothing
        capacities = books.declared.capacities
        assert all(n <= cap for n, cap in zip(books.counts, capacities, strict=True) if cap is not None)
        assert max(books.counts) == 1 and books.counts[full] == 1, books.counts  # never two in one part
        if len(taken) == 2:
            assert (taken[1]["interval"], taken[1]["realised"]) == (93, "ef"[open_part - 1])
            assert books.counts == [0, 1, 1] and board.credit.counts[1] == 0
        else:
            assert books.counts[0] == 1 and board.credit.counts[1] == 1  # the second quantum passed
        ends[seed] = len(taken)
        print(
            f"exclusion: seed {seed}, the first into {first}, the second {'taken' if len(taken) == 2 else 'passed'}"
        )
    assert set(ends.values()) == {1, 2}, ends  # taken by the open part at one seed, passed at another
    books.part, books.counts, books.labels = (
        0,
        [1, 1, 1],
        [books.labels[0] or 1] * 3,
    )  # every excited part full
    photon = [f.name for f in board.families].index("photon")
    books.shares = {t: 1 for t in books.declared.transitions}
    board.credit.counts[photon], board.credit.deficits[photon] = 1, 0
    board.credit.unabsorbed.pop(photon, None), board.credit.unabsorbed_units.pop(photon, None)
    found = lists.absorption(board, photon, [(books, t) for t in books.declared.transitions])
    assert [a.weight for a in found] == [0, 0, found[-1].weight] and found[-1].weight > 0, found
    assert meeting.click(board, books, books.declared.draw, found) == 2  # the quantum passes, no refusal
    closes.clear()
    board = Lattice(
        load_world(exclusion_world(tmp_path / "none", monkeypatch, None, 25)), lambda line: None
    )
    books = board.credit.bodies[0]
    for _ in range(board.world.intervals):
        board.step()
    interval, weights, rest, unabsorbed = closes[1]
    assert (interval, weights, rest) == (93, [standing, open_share], 0) and sum(weights) > unabsorbed, (
        closes
    )
    assert books.counts == [0, 2, 0] and books.declared.capacities == (None, None, None), books.counts
    assert not lists.full(books, 1) and not lists.full(books, 0)  # no capacity declared, never full
    rows = [{"part": k, "name": n, "count": 2 if k == 0 else 0} for k, n in enumerate("gef")]
    refused(
        "capacity", parts_of, [rows[0], {**rows[1], "capacity": 0}, rows[2]], "bodies[0].parts", 3, 2
    )
    refused(
        "capacity", parts_of, [{**rows[0], "capacity": 1}, rows[1], rows[2]], "bodies[0].parts", 3, 2
    )
    names, counts, capacities = parts_of(
        [{**rows[0], "capacity": 2}, {**rows[1], "capacity": 1}, rows[2]], "p", 3, 2
    )
    assert (names, counts, capacities) == (("g", "e", "f"), (2, 0, 0), (2, 1, None))


def test_an_emission_into_a_full_lower_part_is_refused_and_nothing_takes_the_whole_hazard(
    tmp_path, monkeypatch
):
    """The cold reader's E1 (2026-10-19), the one reachable refusal of the exclusion's first form: the emission's list at a full lower part set the emission at 0 and left the rest as the hazard gave it, (lifetime - span) x unit, which is 0 where the window's lit intervals reach the lifetime (the ion-like world's lifetime 8; the span at the lifetime by hand, the body's own window 1 and 18 the counter's), so the list's total was 0 and the draw refused by name; since the fix the rest is the whole hazard, lifetime x unit, the emission at 0 (`lists.emission`, `lists.full`): read directly on the ion-like world's body standing in P with S declared at the capacity 1 and full, the span at the lifetime: the emission at 0, nothing at lifetime x unit, the draw taking nothing with no refusal; with no capacity the two weights sum to the same lifetime x unit, the emission's own hazard over the span."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = Lattice(load_world(ion_world(tmp_path, TOOL)), lambda line: None)
    books = board.credit.bodies[0]
    rate, unit = (
        books.declared.rates[0],
        count_wall(board.families[books.index], board.world.quantum_action) ** 2,
    )
    assert (books.declared.names[rate.leaves], books.declared.names[rate.enters]) == ("P", "S")
    books.part, books.counts = rate.leaves, [1, 1, 0]  # the body in P, one quantum in S
    books.declared = replace(books.declared, capacities=(1, None, None))  # S full at the capacity 1
    found = lists.emission(board, books, rate, rate.lifetime)
    assert [a.weight for a in found] == [0, rate.lifetime * unit], [a.weight for a in found]
    assert meeting.click(board, books, books.declared.draw, found) == 1  # nothing drawn, no refusal
    books.declared = replace(books.declared, capacities=())
    found = lists.emission(board, books, rate, rate.lifetime)
    assert found[0].weight > 0 and sum(a.weight for a in found) == rate.lifetime * unit
