import copy
import json
from pathlib import Path

import pytest

from .algebra import LIMIT, ONE, ZERO, Rational, evaluate, literal
from .runtime import Complex, Lab, QuantumState, RandomStream, choose


@pytest.fixture
def lab():
    return Lab(json.loads(Path(__file__).with_name("definitions.json").read_text(encoding="utf-8")))


def massive(lab, kind, mass=1, E=1, p=None, q=0, cell=0):
    return lab.insert(cell, lab.record(kind, {"mass": mass, "E": E, "p": p or [0, 0, 0], "q": q}))


def pulse(lab, E, p, cell=0):
    return lab.insert(cell, lab.record("pulse", {"E": E, "p": p}))


def state(lab):
    return copy.deepcopy((lab.cells, lab.links, lab.next_id))


def values(lab, identifier, field):
    return dict(dict(lab.cells[0])[identifier].fields)[field]


@pytest.mark.parametrize("n,d", [(0, 1), (-3, 5), (6, -8), (LIMIT, 1), (-LIMIT, 1)])
def test_positive_payload(n, d):
    from fractions import Fraction

    q = Rational.make(n, d)
    assert q.code > 0 and q.denominator > 0
    assert Fraction(q.numerator, q.denominator) == Fraction(n, d)


@pytest.mark.parametrize("value", [0.5, True, {"n": 1, "d": 0}, {"n": LIMIT + 1, "d": 1}])
def test_invalid_literals(value):
    with pytest.raises((ValueError, OverflowError, ZeroDivisionError)):
        literal(value)


def test_vector_algebra():
    a, b = literal([1, 2, 3]), literal([4, -5, 6])
    assert a.dot(b) == literal(12)
    assert a.cross(b) == literal([27, 6, -13])
    assert a.cross(b).dot(a) == literal(0)
    assert a.cross(b).dot(b) == literal(0)
    assert a.cross(b) == b.cross(a).neg()
    with pytest.raises(ValueError):
        a.mul(b)


def test_bounds_and_units(lab):
    with pytest.raises(OverflowError):
        Rational.make(LIMIT) + ONE
    with pytest.raises(OverflowError):
        Rational.make(1 << 63, 1 << 63)
    with pytest.raises(ValueError):
        literal(1, [2, 0]).add(literal(1, [0, 1]))
    with pytest.raises(ValueError):
        literal([1, 0, 0]).add(literal(1))
    expression = 1
    for _ in range(18):
        expression = {"op": "neg", "args": [expression]}
    with pytest.raises(ValueError):
        lab.eval(expression, {})
    with pytest.raises(KeyError):
        evaluate({"ref": "remote.secret"}, {}, lab.definitions["units"])


def test_annihilation_and_inverse(lab):
    ids = [massive(lab, "electron", q=-1), massive(lab, "positron", q=1)]
    before = lab.totals()
    light = lab.react(0, "annihilate", ids)
    assert len(light) == 2 and lab.totals() == before
    assert values(lab, light[0], "p") == literal([1, 0, 0], [2, 0])
    restored = lab.react(0, "pair_creation", light)
    assert len(restored) == 2 and lab.totals() == before


def test_binding_and_dissociation(lab):
    ids = [massive(lab, "constituent"), massive(lab, "constituent")]
    before = lab.totals()
    products = lab.react(0, "capture", ids)
    assert len(products) == 3
    assert values(lab, products[0], "mass") == literal(1, [2, 0])
    assert values(lab, products[1], "E") == literal({"n": 1, "d": 2}, [2, 0])
    assert lab.totals() == before
    assert len(lab.react(0, "dissociate", products)) == 2
    assert lab.totals() == before


def test_absorption_emission_recoil(lab):
    ids = [massive(lab, "ground", mass=2, E=2), pulse(lab, 3, [3, 0, 0])]
    before = lab.totals()
    excited = lab.react(0, "absorb", ids)
    assert values(lab, excited[0], "p") == literal([3, 0, 0], [2, 0])
    assert values(lab, excited[0], "mass") == literal(4, [2, 0])
    lab.react(0, "emit", excited)
    assert lab.totals() == before


@pytest.mark.parametrize("fault", ["energy", "momentum", "charge", "capacity", "duplicate", "remote"])
def test_atomic_failure(lab, fault):
    ids = [massive(lab, "electron", q=-1), massive(lab, "positron", q=1)]
    if fault == "energy":
        lab.definitions["reactions"]["annihilate"]["outputs"] = []
    elif fault == "momentum":
        lab.definitions["reactions"]["annihilate"]["outputs"][1]["fields"]["p"]["value"] = [1, 0, 0]
    elif fault == "charge":
        # Valid records, but incoming charge no longer sums to zero.
        lab.cells[0] = (
            (
                ids[0],
                lab.record("electron", {"mass": 1, "E": 1, "p": [0, 0, 0], "q": 0}),
            ),
            lab.cells[0][1],
        )
    elif fault == "capacity":
        lab.capacity = 1
    elif fault == "duplicate":
        ids[1] = ids[0]
    elif fault == "remote":
        lab.send(0, 1, ids[1])
    before = state(lab)
    with pytest.raises((ValueError, KeyError)):
        lab.react(0, "annihilate", ids)
    assert state(lab) == before


def test_below_pair_threshold(lab):
    half = {"n": 1, "d": 2}
    ids = [pulse(lab, half, [half, 0, 0]), pulse(lab, half, [{"n": -1, "d": 2}, 0, 0])]
    before = state(lab)
    with pytest.raises(ValueError, match="Conservation"):
        lab.react(0, "pair_creation", ids)
    assert state(lab) == before


@pytest.mark.parametrize(
    "kind,fields",
    [
        ("electron", {"mass": 1, "E": 1, "p": [1, 0, 0], "q": -1}),
        ("electron", {"mass": -1, "E": 1, "p": [0, 0, 0], "q": -1}),
        ("pulse", {"E": 1, "p": [0, 0, 0]}),
    ],
)
def test_invalid_kinematics(lab, kind, fields):
    with pytest.raises(ValueError):
        lab.record(kind, fields)


@pytest.mark.parametrize(
    "masses,momenta,normal,expected",
    [
        ([2, 3], [[8, 0, 0], [-3, 0, 0]], [1, 0, 0], [[-4, 0, 0], [9, 0, 0]]),
        (
            [1, 1],
            [[1, 0, 0], [0, 0, 0]],
            [1, 1, 0],
            [
                [{"n": 1, "d": 2}, {"n": -1, "d": 2}, 0],
                [{"n": 1, "d": 2}, {"n": 1, "d": 2}, 0],
            ],
        ),
        (
            [1, 1],
            [[1, 0, 0], [0, 0, 0]],
            [1, 1, 1],
            [
                [{"n": 2, "d": 3}, {"n": -1, "d": 3}, {"n": -1, "d": 3}],
                [{"n": 1, "d": 3}] * 3,
            ],
        ),
    ],
)
def test_elastic_3d(lab, masses, momenta, normal, expected):
    ids = [
        lab.insert(0, lab.record("classical", {"mass": m, "p": p, "q": 0}))
        for m, p in zip(masses, momenta, strict=True)
    ]
    before = lab.totals()
    out = lab.react(0, "elastic", ids, {"normal": literal(normal)})
    assert [values(lab, i, "p") for i in out] == [literal(p, [2, 0]) for p in expected]
    assert lab.totals() == before


def test_zero_normal_atomic(lab):
    ids = [
        lab.insert(0, lab.record("classical", {"mass": 1, "p": p, "q": 0}))
        for p in [[1, 0, 0], [0, 0, 0]]
    ]
    before = state(lab)
    with pytest.raises(ZeroDivisionError):
        lab.react(0, "elastic", ids, {"normal": literal([0, 0, 0])})
    assert state(lab) == before


def test_coupled_fields(lab):
    ids = [
        lab.insert(0, lab.record(kind, {"amplitude": a}))
        for kind, a in [("field_A", [5, 0, 0]), ("field_B", [0, 0, 0])]
    ]
    before = lab.totals()
    out = lab.react(0, "mix_fields", ids)
    assert values(lab, out[0], "amplitude") == literal([3, 0, 0], [1, 0])
    assert values(lab, out[1], "amplitude") == literal([-4, 0, 0], [1, 0])
    assert lab.totals() == before


def test_transport_ownership_and_backpressure(lab):
    lab.capacity = 1
    a = massive(lab, "electron", q=-1)
    b = massive(lab, "positron", q=1, cell=1)
    before = lab.totals()
    lab.send(0, 1, a)
    assert not lab.cells[0] and lab.totals() == before
    lab.advance_transport()
    assert len(lab.links) == 1 and lab.totals() == before
    lab.send(1, 2, b)
    lab.advance_transport()
    assert not lab.links and dict(lab.cells[1])[a].kind == "electron"
    assert dict(lab.cells[2])[b].kind == "positron" and lab.totals() == before
    with pytest.raises(ValueError):
        lab.send(1, 3, a)


def test_names_have_no_special_engine_meaning(lab):
    renamed = json.loads(
        json.dumps(lab.definitions)
        .replace("electron", "arbitrary_17")
        .replace("positron", "arbitrary_29")
    )
    other = Lab(renamed)
    ids = [massive(other, "arbitrary_17", q=-1), massive(other, "arbitrary_29", q=1)]
    before = other.totals()
    other.react(0, "annihilate", ids)
    assert other.totals() == before


def test_weighted_tickets_and_replay():
    assert [choose([3, 1], i) for i in range(4)] == [0, 0, 0, 1]

    def sequence():
        stream, result = RandomStream(12345), []
        for _ in range(100):
            stream, ticket = stream.draw(4)
            result.append(ticket)
        return result

    assert sequence() == sequence()
    assert set(sequence()) == {0, 1, 2, 3}
    with pytest.raises(ValueError):
        choose([-1, 2], 0)
    with pytest.raises(ValueError):
        RandomStream(0)


def test_quantum_interference_and_measurement(lab):
    from .algebra import rational

    matrix = tuple(
        tuple(Complex(rational(x)) for x in row) for row in lab.definitions["quantum_rotation"]
    )
    initial = QuantumState((Complex(ONE), Complex(ZERO)))
    rotated = initial.evolve(matrix)
    assert rotated.weights() == [9, 16]
    inverse = tuple(tuple(matrix[j][i].conjugate() for j in range(2)) for i in range(2))
    assert rotated.evolve(inverse) == initial  # exact destructive interference
    assert [choose(rotated.weights(), i) for i in range(25)].count(0) == 9
    parent = massive(lab, "unstable", mass=2, E=2)
    before = lab.totals()
    collapsed, out = rotated.measure_into(lab, 0, ["decay_x", "decay_y"], [parent], 24)
    assert collapsed.weights() == [0, 1]
    assert values(lab, out[0], "p") == literal([0, 1, 0], [2, 0])
    assert lab.totals() == before


def test_quantum_invalid_operator_and_atomic_coupling(lab):
    initial = QuantumState((Complex(ONE), Complex(ZERO)))
    with pytest.raises(ValueError, match="unitary"):
        initial.evolve(((Complex(ONE), Complex(ONE)), (Complex(ZERO), Complex(ONE))))
    phase = ((Complex(ZERO, ONE), Complex(ZERO)), (Complex(ZERO), Complex(ONE)))
    assert initial.evolve(phase).amplitudes[0] == Complex(ZERO, ONE)
    parent = massive(lab, "unstable", mass=2, E=2)
    lab.capacity = 1
    before = state(lab)
    with pytest.raises(ValueError):
        initial.measure_into(lab, 0, ["decay_x", "decay_y"], [parent], 0)
    assert state(lab) == before and initial.weights() == [1, 0]


def test_scheduled_decay_and_failure_replay(lab):
    parent = massive(lab, "unstable", mass=2, E=2)
    stream = RandomStream(lab.definitions["example_seed"])
    before = lab.totals()
    for _tick in range(100):
        stream, products = lab.scheduled(0, "decay", [parent], stream)
        if products:
            break
    else:
        pytest.fail("Fixed test stream did not decay within 100 ticks")
    assert len(products) == 2 and lab.totals() == before
    assert _tick > 0  # at least one survival step in this seeded trajectory
    lab.definitions["schedules"]["decay"]["weights"] = [0, 1]
    before_state, before_stream = state(lab), stream
    with pytest.raises(KeyError):
        lab.scheduled(0, "decay", [parent], stream)
    assert state(lab) == before_state and stream == before_stream


def test_rng_known_vector_and_bounded_deferral():
    following, ticket = RandomStream(1).draw(4)
    assert following.seed == 270369 and ticket == 0
    # Search bounded seeds only in the test, never in the scheduler's draw.
    found = False
    for seed in range(1, 100):
        stream = RandomStream(seed * 1234567)
        following, ticket = stream.draw(1_000_000_000)
        if ticket is None:
            assert following != stream
            found = True
            break
    assert found


def test_generic_field_names_and_new_balance(lab):
    definitions = json.loads(
        json.dumps(lab.definitions).replace('"p"', '"impulse_vector"').replace('.p"', '.impulse_vector"')
    )
    other = Lab(definitions)
    ids = [
        other.insert(
            0,
            other.record(kind, {"mass": 1, "E": 1, "impulse_vector": [0, 0, 0], "q": q}),
        )
        for kind, q in [("electron", -1), ("positron", 1)]
    ]
    before = other.totals()
    other.react(0, "annihilate", ids)
    assert other.totals() == before
    # A new conserved number is a schema change; runtime needs no new branch.
    for spec in lab.definitions["types"].values():
        spec["derived"]["new_number"] = {"value": 1}
    lab.definitions["balances"]["new_number"] = {
        "zero": 0,
        "expression": {"ref": "new_number"},
    }
    parent = massive(lab, "unstable", mass=2, E=2)
    before = state(lab)
    with pytest.raises(ValueError, match="Conservation"):
        lab.react(0, "decay_x", [parent])  # one unit cannot become two
    assert state(lab) == before


def test_energy_decomposition(lab):
    record = lab.record("excited", {"mass": 4, "E": 5, "p": [3, 0, 0], "q": 0})
    context = lab.context(record)
    assert context["rest_energy"] == literal(4, [2, 0])
    assert context["kinetic_energy"] == literal(1, [2, 0])
    assert context["rest_energy"].add(context["kinetic_energy"]) == context["E"]


def test_configured_vector_force_and_angular_momentum(lab):
    # Algebra example only: it does not claim an energy-conserving EM integrator.
    context = {
        "q": literal(-2),
        "E": literal([1, 2, 0]),
        "v": literal([0, 1, 0]),
        "B": literal([0, 0, 3]),
    }
    force = {
        "op": "mul",
        "args": [
            {"ref": "q"},
            {
                "op": "add",
                "args": [
                    {"ref": "E"},
                    {"op": "cross", "args": [{"ref": "v"}, {"ref": "B"}]},
                ],
            },
        ],
    }
    assert lab.eval(force, context) == literal([-8, -4, 0])
    assert literal([2, 0, 0]).cross(literal([0, 3, 0])) == literal([0, 0, 6])
