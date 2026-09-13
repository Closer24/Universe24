"""Independent small-state expectations for the selected deferred network.

These tests check a finite occupation/qubit model, not a derived field law or a
universal collapse trigger. Randomness below belongs to the test controller.
"""

from dataclasses import FrozenInstanceError, replace
from fractions import Fraction
from math import log2
from random import Random

import pytest

from event_universe.quantum.event_network import EventNetwork, EventNetworkConfig
from event_universe.quantum.event_rules import (
    LocalInstrument,
    LocalUnitary,
    squared_norm,
)
from event_universe.quantum.state import Amplitude


def matrix(rows):
    return tuple(tuple(Amplitude(value, 0) for value in row) for row in rows)


H = LocalUnitary(matrix(((1, 1), (1, -1))))
Z = LocalUnitary(matrix(((1, 0), (0, -1))))
CX = LocalUnitary(matrix(((1, 0, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0))))
CZ = LocalUnitary(matrix(((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, -1))))
R = LocalUnitary(matrix(((5, 0, 0, 0), (0, 3, -4, 0), (0, 4, 3, 0), (0, 0, 0, 5))))
RI = LocalUnitary(matrix(((5, 0, 0, 0), (0, 3, 4, 0), (0, -4, 3, 0), (0, 0, 0, 5))))
POSITION = LocalInstrument((matrix(((1, 0), (0, 0))), matrix(((0, 0), (0, 1)))))
DAMPING = LocalInstrument((matrix(((5, 0), (0, 3))), matrix(((0, 4), (0, 0)))))
GRID = tuple((x, y, 0) for y in range(4) for x in range(4))


def network(occupied=(), **budgets):
    return EventNetwork(EventNetworkConfig(GRID, occupied, **budgets))


def probability(reply, outcome=1):
    return Fraction(reply.weights[outcome], sum(reply.weights))


def choose(g, record, register_index, instrument, outcome):
    decision = g.prepare(record, register_index, instrument)
    assert decision.weights[outcome] > 0
    ticket = sum(decision.weights[:outcome])
    return g.commit(decision, ticket)


def fingerprint(g):
    return (g.tick, g.heads, g.events, g.records, g.successful_queries, g.host_evaluated_nodes)


def test_selected_backend_is_bound_to_existing_owner():
    from event_universe.quantum import DeferredQuantum

    owner = DeferredQuantum()
    config = EventNetworkConfig(GRID, (5,))
    g = owner.bind_event_network(config)
    assert owner.event_network is g
    assert owner.bind_event_network(config) is g
    with pytest.raises(ValueError):
        owner.bind_event_network(replace(config, occupied=()))
    with pytest.raises(ValueError):
        owner.source((0, 0, 0), 0, 1)
    other = DeferredQuantum()
    other.source((0, 0, 0), 0, 1)
    with pytest.raises(ValueError):
        other.bind_event_network(config)


def test_one_event_split_weights_and_no_automatic_lottery():
    g = network((5,))
    g.step(((R, (5, 6)),))
    assert g.host_evaluated_nodes == 0
    before = g.tick, g.events, g.heads
    reply = g.query(5)
    assert probability(reply) == Fraction(9, 25)
    assert (reply.world_ticks, reply.model_cost) == (0, 1)
    assert not g.records
    assert before == (g.tick, g.events, g.heads)
    assert g.joint_state() == ((1 << 5, Amplitude(3, 0)), (1 << 6, Amplitude(4, 0)))
    g.step(((RI, (5, 6)),))
    assert probability(g.query(5)) == 1


def test_cone_defers_unrelated_history_but_keeps_it_available():
    g = network()
    g.step(((H, (0,)), (H, (12,))))
    g.step(((CX, (0, 1)), (CX, (12, 13))))
    g.step(((Z, (1,)), (Z, (12,))))
    events = g.events
    reply = g.query(0)
    assert reply.evaluated_nodes == 4
    assert probability(reply) == Fraction(1, 2)
    assert g.events == events
    g.step(((CX, (0, 1)),))
    g.step(((H, (0,)),))
    assert probability(g.query(0)) == 1


def test_previous_correlated_record_is_not_ignored():
    g = network()
    g.step(((H, (0,)),))
    g.step(((CX, (0, 1)),))
    head = g.heads[0]
    choose(g, 1, 1, POSITION, 1)
    assert g.heads[0] == head
    assert probability(g.query(0)) == 1


def test_partial_result_keeps_entanglement_and_checkpoint_phase():
    g = network()
    g.step(((H, (0,)), (H, (1,))))
    g.step(((CX, (1, 2)),))
    g.step(((CZ, (0, 1)),))
    record = choose(g, 1, 0, POSITION, 0)
    state = g.joint_state()
    assert state == ((0, Amplitude(1, 0)), (6, Amplitude(1, 0)))
    tick = g.tick
    g.checkpoint(0)
    assert g.tick == tick and g.joint_state() == state
    assert g.records == (record,)
    g.step(((CX, (1, 2)),))
    g.step(((H, (1,)),))
    assert probability(g.query(1)) == 0


def test_pure_checkpoint_without_measurement_is_reversible():
    g = network((0,))
    g.step(((R, (0, 1)),))
    before = len(g.events)
    g.checkpoint(0)
    assert len(g.events) < before
    assert not g.records
    g.step(((RI, (0, 1)),))
    assert probability(g.query(0)) == 1


def test_no_transfer_is_conditional_update_not_identity():
    g = network()
    g.step(((H, (0,)),))
    assert probability(g.query(0)) == Fraction(1, 2)
    decision = g.prepare(0, 0, DAMPING)
    assert decision.weights == (34, 16)
    tick = g.tick
    record = g.commit(decision, 0)
    assert record.outcome == 0
    assert g.tick == tick
    assert probability(g.query(0)) == Fraction(9, 34)


def test_automatic_contact_controller_never_needs_measure_call():
    g = network((0,))
    rng = Random(4)
    for tick in range(1, 9):
        g.step(())
        decision = g.prepare(tick, 0, DAMPING)
        positive = sum(weight > 0 for weight in decision.weights)
        ticket = rng.randrange(decision.total_weight) if positive > 1 else None
        g.commit(decision, ticket)
        assert g.tick == tick
    assert any(record.outcome == 1 for record in g.records)
    assert probability(g.query(0)) == 0


def test_record_reuse_never_resamples_and_stale_request_is_rejected():
    g = network()
    g.step(((H, (0,)),))
    decision = g.prepare(7, 0, POSITION)
    record = g.commit(decision, 0)
    before = fingerprint(g)
    assert g.prepare(7, 0, POSITION) is decision
    assert g.commit(decision, 999) is record
    assert fingerprint(g) == before
    with pytest.raises(ValueError):
        g.prepare(7, 1, POSITION)
    other = g.prepare(8, 0, POSITION)
    g.step(((H, (0,)),))
    before = fingerprint(g)
    with pytest.raises(ValueError):
        g.commit(other)
    with pytest.raises(ValueError):
        g.prepare(8, 0, POSITION)
    assert fingerprint(g) == before
    with pytest.raises(FrozenInstanceError):
        record.outcome = 1


def test_certain_result_needs_no_random_number():
    g = network()
    decision = g.prepare(1, 0, POSITION)
    assert decision.weights == (1, 0)
    assert g.commit(decision).outcome == 0
    other = network()
    with pytest.raises(ValueError):
        other.commit(decision)


def test_premature_lottery_destroys_coherent_return():
    returned = Fraction(0)
    for outcome, prior in ((0, Fraction(16, 25)), (1, Fraction(9, 25))):
        g = network((0,))
        g.step(((R, (0, 1)),))
        choose(g, 1, 0, POSITION, outcome)
        g.step(((RI, (0, 1)),))
        returned += prior * probability(g.query(0))
    assert returned == Fraction(337, 625)


def test_deep_cone_finishes_iteratively_without_world_time():
    g = network(max_nodes=5000, max_eval_nodes=2500)
    for _ in range(2000):
        g.step(((Z, (0,)), (Z, (15,))))
    assert g.host_evaluated_nodes == 0
    tick = g.tick
    reply = g.query(0)
    assert reply.evaluated_nodes == 2001
    assert g.tick == tick and reply.world_ticks == 0


@pytest.mark.parametrize("invalid", [((R, (0, 2)),), ((R, (0, 1)), (Z, (1,)))])
def test_nonlocal_or_double_update_is_atomic_error(invalid):
    g = network()
    before = fingerprint(g)
    with pytest.raises(ValueError):
        g.step(invalid)
    assert fingerprint(g) == before


def test_three_dimensional_neighborhood_and_boolean_rejection():
    g = EventNetwork(EventNetworkConfig(((0, 0, 0), (0, 0, 1)), (0,)))
    g.step(((R, (0, 1)),))
    assert probability(g.query(0)) == Fraction(9, 25)
    with pytest.raises(TypeError):
        g.query(True)
    with pytest.raises(TypeError):
        EventNetworkConfig(((False, 0, 0),))


def test_node_term_query_and_record_budgets_fail_without_outcomes():
    g = network(max_nodes=16)
    before = fingerprint(g)
    with pytest.raises(OverflowError):
        g.step(((H, (0,)),))
    assert fingerprint(g) == before
    g = network(max_terms=1)
    g.step(((H, (0,)),))
    before = fingerprint(g)
    with pytest.raises(OverflowError):
        g.query(0)
    with pytest.raises(OverflowError):
        g.prepare(1, 0, POSITION)
    assert fingerprint(g) == before
    g = network(max_eval_nodes=1)
    g.step(((H, (0,)),))
    before = fingerprint(g)
    with pytest.raises(OverflowError):
        g.query(0)
    assert fingerprint(g) == before
    g = network(max_records=1)
    choose(g, 1, 0, POSITION, 0)
    before = fingerprint(g)
    with pytest.raises(OverflowError):
        g.prepare(2, 0, POSITION)
    assert fingerprint(g) == before


def test_failed_commit_or_checkpoint_preserves_all_state():
    g = network(max_eval_nodes=2)
    g.step(((H, (0,)),))
    decision = g.prepare(1, 0, POSITION)
    before = fingerprint(g)
    with pytest.raises(OverflowError):
        g.commit(decision, 0)
    with pytest.raises(OverflowError):
        g.checkpoint(0)
    assert fingerprint(g) == before


def test_bounds_and_incomplete_instruments_are_rejected():
    with pytest.raises(ValueError):
        LocalUnitary(matrix(((1, 1), (0, 1))))
    with pytest.raises(ValueError):
        LocalInstrument((matrix(((1, 0), (0, 0))),))
    with pytest.raises(OverflowError):
        LocalUnitary(matrix(((1 << 30, 0), (0, 1 << 30))))
    huge = LocalUnitary(matrix(((46340, 0), (0, 46340))))
    g = network()
    g.step(((H, (0,)),))
    before = fingerprint(g)
    with pytest.raises(OverflowError):
        g.prepare(1, 0, LocalInstrument((huge.matrix,)))
    assert fingerprint(g) == before


def dft_weights(state):
    # Independent exact 4x4 Fourier diagnostic, not a nonlocal physical gate.
    assert all(bits.bit_count() == 1 for bits, _ in state)
    phases = ((1, 0), (0, 1), (-1, 0), (0, -1))
    result = []
    for ky in range(4):
        for kx in range(4):
            real = imag = 0
            for bits, amp in state:
                q = bits.bit_length() - 1
                a, b = phases[-(kx * (q % 4) + ky * (q // 4)) % 4]
                real += amp.real * a - amp.imag * b
                imag += amp.real * b + amp.imag * a
            result.append(real * real + imag * imag)
    return result


def entropy(weights):
    total = sum(weights)
    return -sum((w / total) * log2(w / total) for w in weights if w)


def test_one_event_fourier_uncertainty_and_partial_position_information():
    g = network((5,))
    assert dft_weights(g.joint_state()) == [1] * 16
    g.step(((R, (5, 6)),))
    state = g.joint_state()
    weights = dft_weights(state)
    assert sum(weights) == 16 * squared_norm(state)
    assert entropy([9, 16]) + entropy(weights) >= 4
    choose(g, 1, 5, POSITION, 1)
    assert dft_weights(g.joint_state()) == [1] * 16
    assert probability(g.query(5)) == 1


# Independent eager reference uses a lifted dense real matrix over four active
# qubits. It neither traverses the production graph nor calls its kernels.
ACTIVE = (0, 1, 4, 5)


def eager_apply(vector, local_matrix, register_indices):
    local_register_indices = tuple(ACTIVE.index(register_index) for register_index in register_indices)
    full = [[0] * 16 for _ in range(16)]
    for out in range(16):
        for inp in range(16):
            if any(
                ((out >> q) & 1) != ((inp >> q) & 1) for q in range(4) if q not in local_register_indices
            ):
                continue
            r = sum(((out >> q) & 1) << j for j, q in enumerate(local_register_indices))
            c = sum(((inp >> q) & 1) << j for j, q in enumerate(local_register_indices))
            assert local_matrix[r][c].imag == 0
            full[out][inp] = local_matrix[r][c].real
    return [sum(coef * value for coef, value in zip(row, vector, strict=True)) for row in full]


def eager_probability(vector, register_index):
    q = ACTIVE.index(register_index)
    total = sum(value * value for value in vector)
    one = sum(value * value for i, value in enumerate(vector) if (i >> q) & 1)
    return Fraction(one, total)


@pytest.mark.parametrize("seed", range(24))
def test_random_layers_and_instruments_match_independent_eager_reference(seed):
    rng = Random(seed)
    g = network()
    vector = [1] + [0] * 15
    for layer in range(12):
        register_index = rng.choice(ACTIVE)
        if layer % 3 == 0:
            a, b = rng.choice(((0, 1), (4, 5), (0, 4), (1, 5)))
            rule, register_indices = rng.choice((CX, CZ)), (a, b)
        else:
            rule, register_indices = rng.choice((H, Z)), (register_index,)
        g.step(((rule, register_indices),))
        vector = eager_apply(vector, rule.matrix, register_indices)
        for target in ACTIVE:
            assert probability(g.query(target)) == eager_probability(vector, target)
        if layer in (4, 9):
            instrument = rng.choice((POSITION, DAMPING))
            decision = g.prepare(layer, register_index, instrument)
            branches = [eager_apply(vector, m, (register_index,)) for m in instrument.branches]
            raw = [sum(value * value for value in branch) for branch in branches]
            assert [Fraction(w, sum(decision.weights)) for w in decision.weights] == [
                Fraction(w, sum(raw)) for w in raw
            ]
            record = g.commit(decision, rng.randrange(decision.total_weight))
            vector = branches[record.outcome]
    state = dict(g.joint_state())
    total = squared_norm(tuple(state.items()))
    for i, value in enumerate(vector):
        bits = sum(((i >> j) & 1) << q for j, q in enumerate(ACTIVE))
        amp = state.get(bits, Amplitude(0, 0))
        assert Fraction(amp.real * amp.real + amp.imag * amp.imag, total) == Fraction(
            value * value, sum(v * v for v in vector)
        )
    nonzero = next(i for i, value in enumerate(vector) if value)
    ref_bits = sum(((nonzero >> j) & 1) << q for j, q in enumerate(ACTIVE))
    ref_amp = state[ref_bits]
    for bits, amp in state.items():
        i = sum(((bits >> q) & 1) << j for j, q in enumerate(ACTIVE))
        assert amp.real * vector[nonzero] == ref_amp.real * vector[i]
        assert amp.imag == 0


def test_complex_phase_survives_defer_and_checkpoint():
    zero, one = Amplitude(0, 0), Amplitude(1, 0)
    phase = LocalUnitary(((one, zero), (zero, Amplitude(0, 1))))
    inverse = LocalUnitary(((one, zero), (zero, Amplitude(0, -1))))
    g = network()
    g.step(((H, (0,)),))
    g.step(((phase, (0,)),))
    assert g.joint_state() == ((0, one), (1, Amplitude(0, 1)))
    g.checkpoint(0)
    g.step(((inverse, (0,)),))
    g.step(((H, (0,)),))
    assert probability(g.query(0)) == 0


def test_unread_remote_instrument_preserves_local_marginal():
    combined = Fraction(0)
    for outcome in (0, 1):
        g = network()
        g.step(((H, (0,)),))
        g.step(((CX, (0, 1)),))
        prior = probability(g.query(0))
        decision = g.prepare(1, 1, DAMPING)
        chance = Fraction(decision.weights[outcome], decision.total_weight)
        g.commit(decision, sum(decision.weights[:outcome]))
        combined += chance * probability(g.query(0))
    assert combined == prior == Fraction(1, 2)


def test_negative_position_record_does_not_choose_another_register():
    g = network((0,))
    g.step(((R, (0, 1)),))
    g.step(((R, (1, 2)),))
    choose(g, 1, 0, POSITION, 0)
    state = g.joint_state()
    assert {bits for bits, _ in state} == {2, 4}
    assert probability(g.query(1)) == Fraction(9, 25)
    assert not any(bits & 1 for bits, _ in state)
