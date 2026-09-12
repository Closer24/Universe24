"""Independent finite density/channel expectations, not a full physics claim."""

from fractions import Fraction
from random import Random

import pytest

from event_universe.quantum import (
    Amplitude,
    DeferredQuantum,
    EventNetworkConfig,
    GroupedInstrument,
    LocalChannel,
    LocalInstrument,
    LocalUnitary,
)
from event_universe.quantum.operations import (
    basis_measurement,
    dephasing,
    permutation,
    transition_instrument,
)
from event_universe.quantum.operations import integer_matrix as matrix

H = LocalUnitary(matrix(((1, 1), (1, -1))))
Z = LocalUnitary(matrix(((1, 0), (0, -1))))
S = LocalUnitary(((Amplitude(1, 0), Amplitude(0, 0)), (Amplitude(0, 0), Amplitude(0, 1))))
CX = permutation((0, 3, 2, 1))
DAMP = LocalChannel((matrix(((5, 0), (0, 3))), matrix(((0, 4), (0, 0)))))
PARTIAL = LocalChannel((matrix(((3, 0), (0, 3))), matrix(((4, 0), (0, 0))), matrix(((0, 0), (0, 4)))))


def space(dimensions=(2,), levels=None, **kwargs):
    config = EventNetworkConfig(
        tuple((i, 0, 0) for i in range(len(dimensions))),
        dimensions=dimensions,
        initial_levels=(0,) * len(dimensions) if levels is None else levels,
        **kwargs,
    )
    return DeferredQuantum().bind_event_network(config)


def probs(g, site=0):
    w = g.query(site).weights
    return tuple(Fraction(v, sum(w)) for v in w)


def density(g, sites=None):
    entries = g.joint_density(sites).entries
    trace = sum(v.real for a, b, v in entries if a == b)
    return {(a, b): (Fraction(v.real, trace), Fraction(v.imag, trace)) for a, b, v in entries}


@pytest.mark.parametrize(
    "middle,expected",
    [
        (Z, (0, 1)),
        (S, (Fraction(1, 2),) * 2),
        (dephasing(2), (Fraction(1, 2),) * 2),
        (PARTIAL, (Fraction(17, 25), Fraction(8, 25))),
    ],
)
def test_interference_and_unobserved_environment(middle, expected):
    g = space()
    for op in (H, middle, H):
        g.step(((op, (0,)),))
    assert probs(g) == expected
    assert g.records == ()
    assert g.tick == 3


def test_grouped_outcome_is_mixed_not_a_hidden_measurement():
    g = space()
    g.step(((H, (0,)),))
    record = g.commit(g.prepare(10, 0, GroupedInstrument((basis_measurement(2).branches,))))
    assert record.outcome == 0
    assert record.decision.weights == (2,)
    before = g.tick
    g.checkpoint(0)
    assert g.tick == before
    g.step(((H, (0,)),))
    assert probs(g) == (Fraction(1, 2),) * 2
    with pytest.raises(ValueError, match="single wavefunction"):
        g.joint_state()


def test_multiple_groups_do_not_normalize_terms_individually():
    # Outcome 0: dephase with probability 16/25; outcome 1: identity with 9/25.
    g = space()
    g.step(((H, (0,)),))
    p = basis_measurement(2).branches

    def scale(m, k):
        return tuple(tuple(Amplitude(v.real * k, v.imag * k) for v in row) for row in m)

    instr = GroupedInstrument(((scale(p[0], 4), scale(p[1], 4)), (matrix(((3, 0), (0, 3))),)))
    d = g.prepare(1, 0, instr)
    assert d.weights == (32, 18)
    g.commit(d, 0)
    g.step(((H, (0,)),))
    assert probs(g) == (Fraction(1, 2),) * 2


def test_bell_partial_trace_reset_no_signaling_and_checkpoint():
    g = space((2, 2))
    g.step(((H, (0,)),))
    g.step(((CX, (0, 1)),))
    before = density(g, (0,))
    assert before == {(0, 0): (Fraction(1, 2), 0), (1, 1): (Fraction(1, 2), 0)}
    g.step(((DAMP, (1,)),))
    assert density(g, (0,)) == before
    assert probs(g, 1) == (Fraction(41, 50), Fraction(9, 50))
    state = density(g)
    g.checkpoint(0)
    assert density(g) == state
    g.step(((H, (1,)),))
    g.step(((H, (1,)),))
    assert density(g) == state


def test_qutrit_and_colocated_registers_keep_mixed_radix():
    cfg = EventNetworkConfig(
        ((1, 1, 1), (1, 1, 1)),
        dimensions=(3, 2),
        initial_levels=(2, 1),
        register_names=("occupation", "spin"),
    )
    g = DeferredQuantum().bind_event_network(cfg)
    assert g.joint_state() == ((5, Amplitude(1, 0)),)
    g.step(((permutation((1, 2, 0)), (0,)),))
    assert g.joint_state() == ((3, Amplitude(1, 0)),)
    g.step(((permutation((5, 4, 3, 2, 1, 0)), (0, 1)),))
    assert g.joint_state() == ((2, Amplitude(1, 0)),)
    assert probs(g) == (0, 0, 1)
    g.step(((dephasing(3), (0,)),))
    assert probs(g) == (0, 0, 1)


def test_finite_transition_and_fermion_exchange_sign():
    g = space((3,), (1,))
    d = g.prepare(1, 0, transition_instrument(3, 1, 2))
    g.commit(d)
    assert probs(g) == (0, 0, 1)
    f = space((2, 2), (1, 1))
    f.step(((permutation((0, 2, 1, 3), (1, 1, 1, -1)), (0, 1)),))
    assert f.joint_state() == ((3, Amplitude(-1, 0)),)
    with pytest.raises(ValueError):
        space((2,), (2,))


def test_channel_failures_are_explicit():
    with pytest.raises(ValueError):
        LocalChannel((matrix(((1, 1), (0, 1))),))
    with pytest.raises(ValueError):
        GroupedInstrument(((),))
    with pytest.raises(ValueError):
        basis_measurement(True)
    with pytest.raises(ValueError):
        space((5,))
    g = space(max_terms=2)
    g.step(((H, (0,)),))
    g.step(((dephasing(2), (0,)),))
    with pytest.raises(OverflowError, match="density"):
        g.query(0)


def test_unrelated_channel_history_stays_available():
    g = space((2, 2, 2))
    g.step(((H, (2,)),))
    g.step(((dephasing(2), (2,)),))
    q = g.query(0)
    assert q.evaluated_nodes == 1
    assert probs(g, 2) == (Fraction(1, 2),) * 2


def test_chsh_exact_rational_settings_and_no_signaling():
    settings_a = (matrix(((1, 0), (0, -1))), matrix(((0, 1), (1, 0))))
    settings_b = (matrix(((3, 4), (4, -3))), matrix(((3, -4), (-4, -3))))
    corr = []

    def instrument(observable, scale):
        return LocalInstrument(
            tuple(
                tuple(
                    tuple(Amplitude(scale * int(i == j) + sgn * v.real, 0) for j, v in enumerate(row))
                    for i, row in enumerate(observable)
                )
                for sgn in (1, -1)
            )
        )

    for a in settings_a:
        for b in settings_b:
            joint = {}
            for out_a in (0, 1):
                g = space((2, 2))
                g.step(((H, (0,)),))
                g.step(((CX, (0, 1)),))
                d = g.prepare(1, 0, instrument(a, 1))
                p_a = Fraction(d.weights[out_a], sum(d.weights))
                g.commit(d, sum(d.weights[:out_a]))
                db = g.prepare(2, 1, instrument(b, 5))
                for out_b in (0, 1):
                    joint[out_a, out_b] = p_a * Fraction(db.weights[out_b], sum(db.weights))
            assert sum(joint.values()) == 1
            assert sum(joint[0, b] for b in (0, 1)) == Fraction(1, 2)
            assert sum(joint[a, 0] for a in (0, 1)) == Fraction(1, 2)
            corr.append(sum((1 if a == b else -1) * v for (a, b), v in joint.items()))
    assert corr == [Fraction(3, 5), Fraction(3, 5), Fraction(4, 5), Fraction(-4, 5)]
    assert corr[0] + corr[1] + corr[2] - corr[3] == Fraction(14, 5)


def test_exchange_sign_changes_interference_in_a_fixed_number_sector():
    zero, one, phase = Amplitude(0, 0), Amplitude(1, 0), Amplitude(1, 1)
    mix = LocalUnitary(
        (
            (phase, zero, zero, zero),
            (zero, one, one, zero),
            (zero, one, Amplitude(-1, 0), zero),
            (zero, zero, zero, phase),
        )
    )
    probabilities = []
    for signs in ((1, 1, 1, 1), (1, 1, 1, -1)):
        g = space((2, 2, 2), (1, 1, 0))
        g.step(((mix, (1, 2)),))
        g.step(((permutation((0, 2, 1, 3), signs), (0, 1)),))
        g.step(((permutation((0, 2, 1, 3)), (0, 1)),))
        g.step(((mix, (1, 2)),))
        assert all(bits.bit_count() == 2 for bits, _ in g.joint_state())
        probabilities.append(probs(g, 1))
    assert probabilities == [(0, 1), (1, 0)]


def test_record_discard_reduces_to_classical_markov_probabilities():
    g = space()
    rotation = LocalUnitary(matrix(((3, -4), (4, 3))))
    classical = (Fraction(1), Fraction(0))
    for _ in range(5):
        g.step(((rotation, (0,)),))
        g.step(((dephasing(2), (0,)),))
        a, b = classical
        classical = ((9 * a + 16 * b) / 25, (16 * a + 9 * b) / 25)
        assert probs(g) == classical
        assert g.records == ()


def test_dense_independent_reference_for_mixed_radix_channels():
    # A separate dense rational evaluator uses explicit subsystem indices.
    # No production evolution/layout function generates the reference result.
    for seed in range(12):
        rng = Random(seed)
        g = space((2, 3))
        rho = [[Fraction(int(i == j == 0)) for j in range(6)] for i in range(6)]
        for _ in range(6):
            target = rng.randrange(2)
            if target == 0:
                rule = rng.choice((H, DAMP, dephasing(2)))
            else:
                rule = rng.choice((permutation((1, 2, 0)), dephasing(3)))
            matrices = rule.kraus if isinstance(rule, LocalChannel) else (rule.matrix,)
            dense = []
            for m in matrices:
                a = [[Fraction(0) for j in range(6)] for i in range(6)]
                for i in range(6):
                    for j in range(6):
                        same_other = (i // 2 == j // 2) if target == 0 else (i % 2 == j % 2)
                        if same_other:
                            a[i][j] = Fraction(
                                m[i % 2][j % 2].real if target == 0 else m[i // 2][j // 2].real
                            )
                dense.append(a)
            following = [
                [
                    sum(k[i][r] * rho[r][s] * k[j][s] for k in dense for r in range(6) for s in range(6))
                    for j in range(6)
                ]
                for i in range(6)
            ]
            norm = sum(following[i][i] for i in range(6))
            rho = [[v / norm for v in row] for row in following]
            g.step(((rule, (target,)),))
            actual = density(g)
            expected = {(i, j): (rho[i][j], 0) for i in range(6) for j in range(6) if rho[i][j]}
            assert actual == expected
