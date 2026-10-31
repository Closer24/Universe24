"""Tensor24's load, the Node-clock's initialization: the board and its Meshes, every gear on its train's rows, the square found by its kinds' character
with its 0i rows odd, the chosen strengths read, each refusal named, the round's promise at the edges of its dial, and the plans laid from the kinds' tables and the star, term 5's push in the books' form among them."""

import itertools
import json
from pathlib import Path

import numpy as np

from tensor24 import main
from tensor24.engine import state, step
from tensor24.engine.mesh import stretches
from tensor24.runner import load as loading
from tensor24.runner import run
from tensor24.runner.board import board
from tensor24.runner.files import NAMES as FILES
from tensor24.runner.files import held_departures, sites_of, vocabulary
from tensor24.runner.run import promises
from tests import frame

UNIVERSE = Path(__file__).resolve().parents[1] / "examples" / "tensor24" / "universe.json"
INTEGERS = json.loads(UNIVERSE.read_text(encoding="utf-8"))["integers"]
SHAPE = (3, 4, 5)  # a board of sides that differ, so no two axes are taken for each other
SITES = sites_of(SHAPE)
NAMES, PARTS = "wave spin axial stress potential field".split(), (2, 1, 1, 1, 2, 1)
KINDS = (["A1"], ["T1"], ["A2"], ["T2"], ["A1", "T1"], ["T1", "A1"])  # each kind but E, two of two
TRAINS = [{"name": n, "kinds": k, "part": p} for n, k, p in zip(NAMES, KINDS, PARTS, strict=True)]
SQUARE, LIKE = ("A1", "T1", "A1", "E", "T2"), ("T1", "T1", "T1", "A1")  # the square, and as many rows
METRIC = {"name": "metric", "kinds": list(SQUARE), "part": 1}
HAND, PAIR = {"name": "held", "kinds": ["A1", "A2"], "part": 1}, {"kinds": ["T1", "T2"], "part": 1}
FIVE = [TRAINS[0], METRIC, HAND, {"name": "giver", **PAIR}, {"name": "taker", **PAIR}]  # the click world
CHOSEN = {"key": 1, "push": 0, "notch": 0, "hold": 0, "spring": 0, "tie": 0, "mesh": 0}  # the file's
SITE, WIDE = 3, 1 << 70  # where the gears are laid, and their counts, past 64 bits
MADE = main.made(loading.star(len(SHAPE)))  # the kinds, tables and square by main.py's one joint
EVEN = "the edge key 152434288 is even: an edge's two click teeth born at its half sum to key - 2, no pair (D1)"


def loaded(trains, gears=(), chosen=CHOSEN, sites=SITES):
    """The files held against the engine's kinds, then loaded, as the run does: the departures, or the loaded and none."""
    kinds, c, square, lifted = MADE
    universe = {"integers": INTEGERS, "trains": [dict(t) for t in trains], "chosen": dict(chosen)}
    setting = {"gears": [list(g) for g in gears]}
    found = held_departures(universe, setting, vocabulary(kinds, square, lifted))
    held, found = (None, found) if found else loading.load(universe, setting, sites, *MADE)
    return (None if found else held), found


def test_the_load_lays_the_board_and_every_gear_on_its_trains_rows_and_names_each_refusal(
    monkeypatch, tmp_path
):
    """Yes: the board and its Meshes as numpy wraps them, every gear on its train's rows past 64 bits, the square by its kinds' character in every order with its 0i rows odd, the chosen key and the notch at 3 read (a chosen strength, pending the owner's word), no term of J but the notch's.
    No: each refusal named with nothing loaded and no raise (the reviews' gear off a later train, its tooth, its b at every site, a bound read on train 0, 64-bit arrays, the MemoryError dropped from the lay's guard, each passed every test once); a tooth at or below its dial named by the promise; an even edge key named by the run (D1's pair law)."""
    spokes, meshes = loading.geometry(nb := board(SHAPE), len(SHAPE))
    assert (nb == frame.board(SHAPE)).all() and (spokes == frame.spokes(len(SHAPE))).all()
    assert (meshes == frame.meshes_of(nb)).all()
    labels, dims, _ = vocabulary(MADE[0], *MADE[2:])
    rows = [sum(dims[labels.index(k)] for k in t["kinds"]) * t["part"] for t in TRAINS]
    _, row, _, *counts = wave = (0, rows[0] - 1, SITE, WIDE, WIDE + 1, WIDE + 2)
    held, found = loaded(TRAINS, laid := [wave, (len(rows) - 1, rows[-1] - 1, SITE, WIDE + 1, WIDE, 0)])
    a, b, r, rd, k = held.state
    assert (
        found == []
        and all(x.dtype == object for x in held.state)
        and not any(f.any() for f, _ in held.potential)
    )
    sides = (
        (1 + len(SHAPE)) * len(TRAINS) * len(TRAINS)
    )  # every side at every reach, a Mesh edge's at its + end
    assert all(x.shape == (sum(rows), SITES) for x in (a, b, r, rd)) and k.shape == (sides, SITES)
    assert (a[row, SITE], b[row, SITE], r[row, SITE]) == tuple(counts)  # the wave's last row, as laid
    assert (a[-1, SITE], b[-1, SITE]) == (WIDE + 1, WIDE) and not k.any()  # the last train's last row
    assert (a != 0).sum() == (b != 0).sum() == len(laid) and (r != 0).sum() == 1 and not rd.any()
    assert not any(np.shares_memory(*pair) for pair in itertools.combinations(held.state, 1 + 1))
    assert (held.click[-1] == CHOSEN["key"]).all() and held.click[-1].shape == (sides, 1)
    universe, rate = {"integers": INTEGERS, "trains": TRAINS, "chosen": CHOSEN}, INTEGERS["full_rate"]
    grip, spokes = INTEGERS["den"] * rate * rate, len(frame.spokes(len(SHAPE)))  # den Gamma^2
    _, _, _, grips, (rest, *ones), *_ = loading.laid_out(universe, list(SHAPE), held)
    # the teeth at rest 6 den Gamma^2, each grip den Gamma^2, s, T_k, T_d at 1 (the audit's loaders at 7 den Gamma^2 and at 2 den Gamma^2 a grip passed every test); no square: every row even
    assert (rest == spokes * grip).all() and (grips == grip).all() and all((x == 1).all() for x in ones)
    for kinds in [*sorted(set(itertools.permutations(SQUARE))), LIKE]:
        held, found = loaded([*TRAINS, {**METRIC, "kinds": list(kinds)}])
        assert found == [] and held.trains.square.tolist() == [0] * len(TRAINS) + [int(kinds != LIKE)]
    # the square's 0i rows, the three after its 00 slot, odd under the mirror, every other row even; the notch's monomials at the chosen h: 2 h on the 00 slot squared, h on each pair of ii slots, on the square train alone
    held, _ = loaded([*TRAINS, METRIC], chosen={**CHOSEN, "notch": 3})
    (*_, even), zero = loading.laid_out(universe, list(SHAPE), held)[4], int(held.trains.first[-1])
    assert not even[odd := range(zero + 1, zero + 4)].any() and set(np.delete(even, odd).tolist()) == {1}
    (factor, (one, two)), _ = held.potential  # the notch, in the two-leg block
    named = set(one[factor != 0].tolist()) | set(two[factor != 0].tolist())  # the square's legs alone
    assert sorted(set(factor.tolist())) == [0, 3, 6] and named <= set(range(zero, zero + 10))
    lit = [
        tuple(sorted(x)) for x in zip(one[factor != 0].tolist(), two[factor != 0].tolist(), strict=True)
    ]
    assert len(set(lit)) == len(
        lit
    )  # each pair of slots once, at both its orders' factor summed (MIN2's S1)
    for trains, gears, named in [
        ([{**TRAINS[1], "kinds": ["E3/2"]}], [], "'E3/2' is none of the kinds"),
        ([{**TRAINS[1], "kinds": ["E"]}], [], "'E' has no whole basis the 24 permute"),
        ([{**TRAINS[1], "kinds": list(SQUARE), "part": 2}], [], "'E' has no whole basis the 24 permute"),
        ([TRAINS[0]], [(0, rows[0], 0, 1, 0, 0)], f"component {rows[0]} off train 0's {rows[0]} rows"),
        ([*TRAINS, METRIC, {**METRIC, "name": "twin"}], [], "one metric family: 'metric', 'twin'"),
    ]:
        held, found = loaded(trains, gears)
        assert held is None and any(named in line for line in found), found
    # the promise names a tooth at its edge's dial and one below it, sites 1 and 2, and holds one at D - 1, past 64 bits (the eighth review's fifth, carried to the fine tooth at 8b43839a1)
    d, w, off = 2 * WIDE, WIDE + 0 * np.arange(3, dtype=object)[None, :], {1: 2 * WIDE, 2: -2 * WIDE - 1}
    held = state.State(w + 1, w, np.array([[d - 1, off[1], off[2]]], dtype=object), 0 * w, 0 * w)
    dial = f"not within the edge's dial [-{d}, {d}) of the teeth {WIDE} and {WIDE}"
    assert promises(held, w, w) == [f"row 0, site {x}: the tooth {t} {dial}" for x, t in off.items()]
    # D1's hypothesis where it is used: the click world's edge key laid one up, even, named by the run, nothing written
    edged, paths = loading.edging, [UNIVERSE.parents[1] / "tensor24-click" / f"{n}.json" for n in FILES]
    monkeypatch.setattr(loading, "edging", lambda *a: (*edged(*a)[:2], edged(*a)[2] + 1))
    assert run.run(main.ENGINE, paths, tmp_path / "even.jsonl") == [EVEN] and not any(tmp_path.iterdir())
    monkeypatch.setattr(loading, "edging", edged)
    _, found = loaded(TRAINS, sites=1 << 64)
    assert len(found) == 1 and found[0].startswith(f"piece.shape: {sum(rows)} rows at")
    monkeypatch.setattr(np, "zeros", lambda *a, **k: (_ for _ in ()).throw(MemoryError("no room")))
    named = f"piece.shape: {sum(rows)} rows at {SITES} sites, more than the arrays of this machine hold"
    assert loaded(TRAINS)[1] == [f"{named} (no room)"]


def monomials(held):
    """J's potential's monomials, block by block (the two-leg block, then the four-leg), each one's factor and its legs."""
    return [
        (f, tuple(legs))
        for fs, block in held.potential
        for f, legs in zip(fs, block.T.tolist(), strict=True)
    ]


def shared(held, senses):
    """Term 11's weights by loops, the edges' naive model: per term of J's plan, block by block and leg by leg as contract.pushes lays them, its weight onto every train of its monomial, kappa (L - l) / L where the monomial is live with value legs in two trains or more, L its legs and l its own train's (a position one leg, a held train's positions one leg together), kappa the product of senses and of every such L, each once; and kappa / senses, the key's scale."""
    trains, listed = [held.trains[n] for n in range(len(held.trains))], monomials(held)
    of = {r: n for n, t in enumerate(trains) for r in range(t.first, t.first + t.rows())}
    sizes = [
        0,
        *itertools.accumulate(len(fs) for fs, _ in held.potential),
    ]  # each block's first monomial
    terms = [
        (at + m, j)
        for (fs, block), at in zip(held.potential, sizes, strict=False)
        for j in range(len(block))
        for m in range(len(fs))
    ]
    counted = [{} for _ in listed]
    for (_, legs), count in zip(listed, counted, strict=True):
        for n in (of[leg] for leg in legs):
            count[n] = 1 if held.trains.held[n] else count.get(n, 0) + 1
    edged = {m for m, (f, _) in enumerate(listed) if f and len(counted[m]) > 1}
    kappa = int(np.prod(sorted({senses, *(sum(counted[m].values()) for m in edged)})))
    weight = np.zeros((len(terms), len(trains)), dtype=object)
    for i, (m, j) in enumerate(terms):
        total, own = sum(counted[m].values()), counted[m][of[listed[m][1][j]]]
        weight[i, list(counted[m])] = kappa * (total - own) // total if m in edged else 0
    return weight, kappa // senses


def test_the_plans_are_laid_from_the_kinds_tables_the_edges_and_the_coupling_familys_frame():
    """Yes: on the click world's shape at hold 1, spring 3 and tie 1 (the files' chosen strengths, pending the owner's word) the held hand and the tied hands are found by character, the held rows' own spring the chosen spring and their grips 0, the tie hold f on the dot product's diagonal, the hands' tie tie on it once, the board's wave in no monomial; term 11 on the edges by its naive model (shared): each term of J's plan weighs kappa (L - l) / L onto the trains of its monomial, NC29b's 3 on the hands' tie, 4 on a tie's held legs and 2 on its tied pair at kappa 6, its leg's train beside it, every side's key the universe's times kappa / senses;
    term 5's push in the books' form: every row gliding a count a round alike pushes the 00 slot by k0 = Spokes x senses (the clock's read, from the star) times the momenta in and out of every row the push does not land on, a tent along z pushes the zz slot by minus its two z Meshes' stretches squared, nothing lands elsewhere, the drive's teeth senses on the 00 and ii rows and 1 elsewhere, in either order of the trains; the gradient vertex at mesh 3 (a chosen strength, pending the owner's word) on the board's wave and a tied (T1, T2) hand, -mesh onto each M_i's row from the wave's difference along i and +mesh onto the wave's row from M_i's, each term laid once with its other two readings the unit (one potential's two pushes, never a push laid twice or a cubic vertex), the T2 rows and the wave's second part in none.
    No: the board's wave, the square and an own monomial (a spring) weigh on no edge, so the edges are the held hand and the two tied hands' triangle; the tie off the diagonal and the hands' tie the other way are 0; the two tied hands swapped in the file lay the same plan and grips; the pushed rows' own momenta push nothing, and push 0 pushes nothing; the wave with no vector hand lays no gradient vertex."""
    # term 6's frame on the board's wave, the square, the held hand (A1, A2) and two tied (T1, T2) hands, at hold 1, spring 3 and tie 1
    chosen = {**CHOSEN, "hold": 1, "spring": 3, "tie": 1}
    held, found = loaded(FIVE, chosen=chosen)
    wave, _, hand, giver, taker = (held.trains[n] for n in range(len(FIVE)))
    span = lambda t: range(t.first, t.first + t.rows())  # noqa: E731
    v = {legs: f for f, legs in monomials(held) if f}  # the monomials with a factor, by their legs
    laid = main.layout({"integers": INTEGERS, "trains": FIVE, "chosen": chosen}, list(SHAPE), held)
    spring, f = chosen["spring"], int(laid.gearing.rest[0, 0]) // INTEGERS["full_rate"]
    flags = (held.trains.held.tolist(), held.trains.tied.tolist(), held.trains.gripped.tolist())
    assert flags == ([0, 0, 1, 0, 0], [0, 0, 0, 1, 1], [1, 1, 0, 1, 1])  # held, tied, gripped
    assert found == [] and len(v) == len([f for f, _ in monomials(held) if f])
    assert all(v[k, k] == spring for k in span(hand))  # the held rows' own spring
    assert all(v[x, x, k, k] == f for x in span(giver) for k in span(hand))  # the tie, hold x f x 1
    both = list(zip(span(giver), span(taker), strict=True))  # the hands' rows, component by component
    assert all(v[x, y] == 1 and (y, x) not in v for x, y in both)  # the hands' tie, once
    assert not any(x != y and {x, y} <= set(span(giver)) for x, y, *_ in v)  # the tie off the diagonal
    assert not any(set(leg) & set(span(wave)) for leg in v)  # the wave untied
    assert set(laid.grip[list(span(hand))].ravel().tolist()) == {0}  # the held hand holds no Mesh
    weight, train, key = held.click
    wanted, scale = shared(held, senses := len(frame.spokes(len(SHAPE))) // len(SHAPE))
    of = {r: n for n, t in enumerate(held.trains[n] for n in range(len(FIVE))) for r in span(t)}
    legged = [
        of[int(r)] for _, block in held.potential for r in block.reshape(-1)
    ]  # each term's leg's train
    assert (
        frame.same([weight], [wanted])
        and train.tolist() == legged
        and (key == scale * chosen["key"]).all()
    )
    tri = [
        n for n in range(len(FIVE)) if held.trains.held[n] + held.trains.tied[n]
    ]  # the held and tied hands
    edges = {(int(train[i]), u) for (i, u), w in np.ndenumerate(weight) if w and train[i] != u}
    assert edges == {(x, y) for x in tri for y in tri if x != y}  # the triangle, each way
    assert (np.delete(laid.grip, list(span(hand)), axis=0) == laid.grip[0, 0]).all()
    swapped, _ = loaded([*FIVE[:3], *reversed(FIVE[3:])], chosen=chosen)  # the two tied hands swapped
    blocks = zip(swapped.potential, held.potential, strict=True)
    assert all(np.array_equal(x, y) for one, two in blocks for x, y in zip(one, two, strict=True))
    z = np.indices(SHAPE)[-1].reshape(-1).astype(object)  # term 5's push: each site's place along z
    for trains, push in itertools.product(([TRAINS[0], METRIC], [METRIC, TRAINS[0]]), (1, 0)):
        universe = {"integers": INTEGERS, "trains": trains, "chosen": {**CHOSEN, "push": push}}
        laid = main.layout(universe, list(SHAPE), held := loaded(trains, chosen=universe["chosen"])[0])
        (zero,), b = [t.first for t in held.trains if t.square], held.state[0]  # every row gliding alike
        pushed, senses = [zero, *range(zero + 4, zero + 7)], len(laid.spokes) // len(SHAPE)  # 00, ii
        b[-1], k0 = WIDE * np.minimum(z, SHAPE[-1] - z), len(laid.spokes) * senses  # a tent along z
        t, glide = b[-1].reshape(SHAPE), state.State(b + 1, b, *held.state[2:])
        j = step.stress(laid, glide, 0 * b, sum(step.dials(laid, glide)), stretches(laid, b + 1))
        tent = -push * sum(np.square(np.roll(t, n, -1) - t) for n in (1, -1)).reshape(-1)  # the zz slot
        assert (j[zero] == push * k0 * (len(j) - len(pushed))).all() and (j[pushed[-1]] == tent).all()
        assert not np.delete(j, (zero, pushed[-1]), axis=0).any()  # nothing lands elsewhere
        assert laid.gearing.drive[:, 0].tolist() == [senses if r in pushed else 1 for r in range(len(j))]
        assert set(laid.clock.factor.tolist()) == {0, k0}  # the clock's read at k0
    strength, pair = 3, [TRAINS[0], {"name": "tied", **PAIR}]  # the board's wave and a tied hand
    held, _ = loaded(pair, chosen={**CHOSEN, "mesh": strength})
    ((one, two, three), factor, target), rows, hand = held.mesh, len(held.state[0]), held.trains[1].first
    terms = sorted((int(f), int(t), int(v)) for f, t, v in zip(one, target, factor, strict=True) if v)
    wanted = [((1 + i) * rows, hand + i, -strength) for i in range(len(SHAPE))]  # M_i by L's difference
    wanted += [((1 + i) * rows + hand + i, 0, strength) for i in range(len(SHAPE))]  # L by M_i's
    _, alone, _ = loaded([TRAINS[0]], chosen={**CHOSEN, "mesh": strength})[0].mesh  # the wave alone
    assert terms == sorted(wanted) and {*two.tolist(), *three.tolist()} == {-1} and not alone.any()
