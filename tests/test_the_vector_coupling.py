"""The absorption's vector coupling as a test (ALGEBRA.md, The pixel's representation, Theorem 2: a one-Node body reads the light's lattice gradient across its six Links, (L_(c + a) - L_(c - a)) / 2, against the transition's compiled dipole vector, and a level uniform over the body turns no Link; src/event_universe/resonance.py's `gradient` and `projected`, the transition key `dipole` beside `weight` in loader/node_detector_declaration.py): the two shipped pixel worlds examples/events/pixel/pixel_absorption_z_pi8_vector.json and pixel_absorption_z_pi8_scalar.json run their 60 intervals with the null window's write at 48 pinned bit for bit, the vector reading recomputed in plain integers from the drive's levels at the body's Node's six neighbours and equal to the engine's at every interval, the declaration's refusals by name, and the direction selection exact in the integers."""

import numpy as np

from event_universe import resonance
from event_universe.lattice import Lattice
from event_universe.loader.keys import keyed
from event_universe.loader.node_detector_declaration import (
    Transition,
    parts_of,
    rates_of,
    transitions_of,
)
from event_universe.loader.world import BODY_KEYS, BODY_REQUIRED
from tests.laws import EVENTS, family, refused
from tests.laws_read import load_shipped

FOLDER = EVENTS / "pixel"
VECTOR, SCALAR = (
    FOLDER / "pixel_absorption_z_pi8_vector.json",
    FOLDER / "pixel_absorption_z_pi8_scalar.json",
)
NODE = [5, 5, 24]  # the one-Node body of both worlds, run 4's board 11 x 11 x 33
WINDOW = 48  # the window derived at the load from the light's lay's passage (loader/window.py)
DIPOLES = (  # the vector world's four transitions: weight 1 over 1, the compiled vector over 10^6 (table_run4_board.json)
    (1, 1, (0, 0, 25777), 1000000),
    (1, 1, (0, 0, 877587), 1000000),
    (1, 1, (-197, -1065715, 0), 1000000),
    (1, 1, (1065710, -3089, 0), 1000000),
)
PAIR = (
    6818063,
    27502775,
    None,
    1,
)  # the scalar world's one transition: the pair weight k = 0.248, no dipole
NULL_CLOSE = {  # the credit line at 48 (reports.credit): the null window's re-lay labelled LATTICE, the count 0, the part g before and after, proper 47 the body's own clock in its holder's well over the board's 48
    "event": "credit",
    "label": "LATTICE",
    "interval": 48,
    "family": "electron",
    "node_detector": "body 0",
    "window": [1, 48],
    "proper": 47,
    "windows": 1,
    "before": "g",
    "realised": "g",
    "kept": None,
    "count": 0,
    "left": None,
    "absorbed": None,
    "emitted": None,
    "momentum": None,
    "fan": None,
    "lost": None,
    "source": None,
    "recoil": None,
}
BIAS = {
    "g": 10,
    "last": 1,
    "sum": 10,
}  # the draw's bias bound (features/click.bias_bound), the same in both worlds
TOTALS = {  # the bias bound's total, the body's digits read at the draw: the one word the two worlds' credit lines differ in (MEASURED)
    VECTOR: 25868186335403226514610,
    SCALAR: 25868186260117460030770,
}
RELAID = [  # the two lay lines at 48 at the body's Node (reports.lay): each line's [now, before, remainder] before and after the null window's re-lay, the same in both worlds, the body's own lay reading no drive (MEASURED)
    ([-2520, -711, 249322708992000], [-2520, -712, 165888000000000]),
    ([-1300, -2746, 325099567104000], [-1300, -2745, 165888000000000]),
]
CARRIER = {  # the z difference at the body's Node and e2's reading at the carrier's trough and crest (MEASURED, the reading DERIVED from the difference with the carry)
    28: ([0, 0, -832], -365),
    35: ([-2, 1, 1232], 541),
}
NAMES, QUANTA, OWN = (
    ("g", "e1"),
    {"photon": 1, "electron": 2},
    2,
)  # the declaration's names for the refusals
ROW = {"from": "g", "to": "e1", "drive": "photon", "weight": 1, "resonance": [5909, 6000]}


def differences(levels, at):  # type: ignore[no-untyped-def]
    """The drive's level differences across the one Node's six Links, per axis L_(c + a) - L_(c - a), a neighbour beyond the lattice reading 0, in plain integers: the test's own reading of what `resonance.gradient` reads."""

    def level(there):  # type: ignore[no-untyped-def]
        inside = all(0 <= there[a] < levels.shape[a] for a in range(3))
        return int(levels[tuple(there)]) if inside else 0

    return [
        level([c + (a == axis) for a, c in enumerate(at)])
        - level([c - (a == axis) for a, c in enumerate(at)])
        for axis in range(3)
    ]


def projected(dipole, den, slopes, carry):  # type: ignore[no-untyped-def]
    """The engine's one carried division in plain integers (`resonance.projected`): (SUM_a n_a g_a + carry) div 2 den, the floor, and the remainder kept in [0, 2 den)."""
    total = sum(n * g for n, g in zip(dipole, slopes, strict=True)) + carry
    level = total // (2 * den)
    return level, total - 2 * den * level


def test_the_two_pixel_worlds_run_their_sixty_intervals_and_the_null_windows_write_at_48_stands_bit_for_bit():
    """Both worlds over 60 intervals, the vector world's four transitions by their dipoles and the scalar world's one at the pair weight, as declared: the window derived 48, one click line per interval, no take (the body's counts [1, 0, 0, 0, 0] at the end, MEASURED), the one credit line the null window's write at 48 with the count 0 labelled LATTICE and the body's two lines re-laid at [5, 5, 24], every word pinned (MEASURED), the lay lines the same in both worlds and the credit lines differing in the draw's digits total alone."""
    for path, declared in ((VECTOR, DIPOLES), (SCALAR, (PAIR,))):
        lines: list[dict] = []  # type: ignore[type-arg]
        board = Lattice(load_shipped(path), lines.append)
        books = board.credit.bodies[0]
        assert books.nodes == (tuple(NODE),) and books.declared.draw.window == WINDOW
        assert (
            tuple((t.weight, t.weight_den, t.dipole, t.dipole_scale) for t in books.declared.transitions)
            == declared
        )
        for _ in range(60):
            board.step()
        kinds = [line["event"] for line in lines]
        assert (kinds.count("click"), kinds.count("credit"), kinds.count("lay"), len(kinds)) == (
            60,
            1,
            2,
            63,
        )
        (credit,) = [line for line in lines if line["event"] == "credit"]
        assert credit == {**NULL_CLOSE, "bias_bound": {**BIAS, "total": TOTALS[path]}}
        lays = sorted((line for line in lines if line["event"] == "lay"), key=lambda line: line["line"])
        heads = [
            (lay["interval"], lay["family"], lay["label"], lay["node"], lay["line"]) for lay in lays
        ]
        assert heads == [
            (48, "electron", "LATTICE", {"at": NODE, "label": "LATTICE"}, k) for k in range(2)
        ]
        assert [(lay["before"], lay["after"]) for lay in lays] == RELAID
        assert books.counts == [1, 0, 0, 0, 0] and board.interval == 60


def test_the_vector_reading_is_the_six_links_difference_projected_on_the_dipole_by_one_carried_division():
    """The vector world's 60 intervals: at each one the level every dipole transition read is recomputed from the photon's first line's levels at the body's Node's six neighbours after the step, the difference per axis dotted with the declared vector and divided once by 2 den with the carried remainder, and equals the engine's reading (the window's two sums advanced by the level times the two reference records, the remainder in the books, the sums held as the arrival at the close); the drive along z: the x and y differences 0 exactly through 30 and the transverse dipoles e3 and e4 reading 0 exactly there (DERIVED: 0 over 2 den is (0, 0) and the carry stays 0), the first transverse residue at 31, the differences (-1, 0, 29) from the shipped lay's roundings (three Nodes differ by one level between x 4 and x 6 at the start, MEASURED), e3 reading (0, 197) and e4 (-1, 934290) (DERIVED: 197 and -1065710 over 2 x 10^6); the z difference -832 at 28 and 1232 at 35, the carrier's trough and crest at the Node (MEASURED), e2 reading -365 and 541 there (DERIVED: 877587 g_z with the carry over 2 x 10^6); over the run 2 den SUM level + the last remainder = SUM numerator exactly, the window's sum the floor of the rational sum (DERIVED: the carried division telescopes)."""
    board = Lattice(load_shipped(VECTOR))
    books, photon = board.credit.bodies[0], family(board, "photon")
    transitions = books.declared.transitions
    at = [n + o for n, o in zip(books.nodes[0], board.offset, strict=True)]
    read = {t: [] for t in transitions}  # type: ignore[var-annotated]
    numerators = dict.fromkeys(transitions, 0)
    for _ in range(60):
        before = [(r.in_phase, r.quadrature, r.cosine[0], r.sine[0]) for r in books.references]
        carries = {t: books.gradient_carry.get(t, 0) for t in transitions}
        board.step()
        slopes = differences(board.states[photon].lines[0].now, at)
        assert tuple(slopes) == resonance.gradient(board, books, photon)
        rows = zip(transitions, books.references, before, strict=True)
        for t, reference, (in_phase, quadrature, cosine, sine) in rows:
            level, rest = projected(t.dipole, t.dipole_scale, slopes, carries[t])
            assert books.gradient_carry[t] == rest
            summed = (in_phase + level * cosine, quadrature + level * sine)
            if board.interval % WINDOW:
                assert (reference.in_phase, reference.quadrature) == summed
            else:  # the close: the two sums held as the arrival and reset
                assert reference.arrival == summed and (reference.in_phase, reference.quadrature) == (
                    0,
                    0,
                )
            read[t].append(level)
            numerators[t] += sum(n * g for n, g in zip(t.dipole, slopes, strict=True))
        if board.interval <= 30:
            assert slopes[:2] == [0, 0]
            assert all(read[t][-1] == 0 and books.gradient_carry[t] == 0 for t in transitions[2:])
        if board.interval == 31:
            assert slopes == [-1, 0, 29]
            assert [(read[t][-1], books.gradient_carry[t]) for t in transitions[2:]] == [
                (0, 197),
                (-1, 934290),
            ]
        if board.interval in CARRIER:
            assert (slopes, read[transitions[1]][-1]) == CARRIER[board.interval]
    for t in transitions:
        assert 2 * t.dipole_scale * sum(read[t]) + books.gradient_carry[t] == numerators[t]
    assert [len(levels) for levels in read.values()] == [60] * 4


def test_the_declaration_admits_the_dipole_on_a_transition_of_a_one_node_body_alone_and_refuses_each_defect_by_name():
    """The loader's own functions with no world run: the vector world's row stands as Transition(0, 1, 1, 1, (5909, 6000), 1, (0, 0, 25777), 1000000), the scalar world's pair weight as (6818063, 27502775) with no dipole, and an integer weight as the pair (k, 1); refused by name: a weight pair with the denominator 0, with its numerator 0 or not a pair, a dipole that is not [[n_x, n_y, n_z], den] (two components, four, a flat list, no scale, a number), the zero vector, the scale 0, a component not an integer, the dipole on a body of two Nodes, and the key `dipole` on a part, on a rate and on the body (keys.keyed, the unknown key)."""

    def declared(**changes):  # type: ignore[no-untyped-def]
        return transitions_of([{**ROW, **changes}], "bodies[0].transitions", NAMES, QUANTA, OWN)

    vector = [[0, 0, 25777], 1000000]
    assert declared(dipole=vector) == (Transition(0, 1, 1, 1, (5909, 6000), 1, (0, 0, 25777), 1000000),)
    assert declared(weight=[6818063, 27502775]) == (
        Transition(0, 1, 1, 6818063, (5909, 6000), 27502775),
    )
    assert declared() == (Transition(0, 1, 1, 1, (5909, 6000)),)
    refused(r"weight\[1\] must be an integer from 1 through", declared, weight=[1, 0])
    refused(r"weight\[0\] must be an integer from 1 through", declared, weight=[0, 5])
    refused(
        r"weight is an integer from 1 or a pair \[num, den\], got \[1, 2, 3\]",
        declared,
        weight=[1, 2, 3],
    )
    for wrong in ([[0, 0], 1], [[0, 0, 1, 0], 1], [0, 0, 1], [[0, 0, 1]], 7):
        refused(
            r"dipole is \[\[n_x, n_y, n_z\], den\], the vector in the Link unit over den",
            declared,
            dipole=wrong,
        )
    refused(
        "dipole is the zero vector: a transition coupling by nothing is no transition",
        declared,
        dipole=[[0, 0, 0], 1],
    )
    refused(r"dipole\[1\] must be an integer from 1 through", declared, dipole=[[0, 0, 1], 0])
    refused(r"dipole\[0\]\[2\] must be an integer", declared, dipole=[[0, 0, 1.5], 1])
    rows = [{**ROW, "dipole": vector}]
    refused(
        "six Links, and this body stands on 2 Nodes", transitions_of, rows, "b", NAMES, QUANTA, OWN, 2
    )
    parts = [
        {"part": 0, "name": "g", "count": 1, "dipole": vector},
        {"part": 1, "name": "e1", "count": 0},
    ]
    refused(r"parts\[0\] holds the unknown key 'dipole'", parts_of, parts, "parts", 2, 1)
    rate = [{"from": "e1", "to": "g", "lifetime": 40, "gives_to": "photon", "dipole": vector}]
    refused(
        r"rates\[0\] holds the unknown key 'dipole'",
        rates_of,
        rate,
        "rates",
        NAMES,
        QUANTA,
        OWN,
        declared(),
    )
    body = {"family": "electron", "nodes": [{"node": NODE, "weight": 1}], "dipole": vector}
    refused(
        r"bodies\[0\] holds the unknown key 'dipole'", keyed, body, "bodies[0]", BODY_KEYS, BODY_REQUIRED
    )


def test_a_drive_sloping_along_one_axis_turns_a_dipole_across_it_by_nothing_and_one_along_it_by_the_vector():
    """`gradient` and `projected` on the vector world's board as laid, the photon's first line set by the test to the slope 1000 x, uniform along y and z: the differences (2000, 0, 0), the z-dipoles e1 and e2 reading (0, 0) exactly (DERIVED: n_z times 0 over 2 den), e4's (1065710, -3089, 0) over 10^6 reading (1065, 1420000) (DERIVED: 1065710 x 2000 = 1065 x 2 x 10^6 + 1420000) and (1066, 0) with the carry 580000 completing the division, e3's (-197, -1065715, 0) reading (-1, 1606000) (DERIVED: -394000 = -1 x 2 x 10^6 + 1606000, the floor); a level uniform over the board turns no Link: the differences (0, 0, 0) and `sloped` False, Theorem 2's gauge statement."""
    board = Lattice(load_shipped(VECTOR))
    books, photon = board.credit.bodies[0], family(board, "photon")
    e1, e2, e3, e4 = books.declared.transitions
    line = board.states[photon].lines[0]
    line.now[...] = line.before[...] = 1000 * np.arange(board.shape[0])[:, None, None]
    assert resonance.gradient(board, books, photon) == (2000, 0, 0) and resonance.sloped(
        board, books, photon
    )
    assert resonance.projected(board, books, e1, 0) == resonance.projected(board, books, e2, 0) == (0, 0)
    assert resonance.projected(board, books, e4, 0) == (1065, 1420000)
    assert resonance.projected(board, books, e4, 580000) == (1066, 0)
    assert resonance.projected(board, books, e3, 0) == (-1, 1606000)
    line.now[...] = line.before[...] = 7
    assert resonance.gradient(board, books, photon) == (0, 0, 0) and not resonance.sloped(
        board, books, photon
    )
