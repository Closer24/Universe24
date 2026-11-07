"""Finite regression checks of the signal-clock algebra and its limitations."""
import unittest
from itertools import product

from research.signal_clocks.algebra_checks import local_two_arrivals, phase_oracle
from universe24.core.rule3 import forward
from universe24.core.state import Channel
from universe24.observation.clicks import classify
from universe24.core import Coupling, Cube, Engine, State
from universe24.core.group_2o import group


class SignalClockAlgebraTests(unittest.TestCase):
    def test_signed_phase_oracle_and_remainder_event(self):
        for a, b in ((0, 0), (1, -2), (-7, 4)):
            for r in range(6):
                for u in range(-15, 16):
                    old = Channel(a, b, r)
                    new = phase_oracle(old, u)
                    self.assertEqual(new, forward(old, u))
                    self.assertEqual(new.r % 2, r % 2)
                    self.assertEqual(new.r != r, u % 3 != 0)

    def test_quiet_remainder_write_is_not_a_carry_event(self):
        old = Channel(0, 0, 0)
        written = phase_oracle(old, 1)
        self.assertEqual(written, Channel(0, 0, 2))
        self.assertEqual(written.b + old.a, 0)
        carry = phase_oracle(old, 3)
        self.assertEqual(carry, Channel(0, 1, 0))
        self.assertEqual(carry.r, old.r)

    def test_two_prescribed_arrivals_wait_and_create_three_records(self):
        samples = local_two_arrivals(wait=6, tail=8)
        memory = [tuple(c[2] for c in s["pair"]) for s in samples]
        events = [t for t in range(1, len(memory)) if memory[t] != memory[t-1]]
        self.assertEqual(events, [1, 8])
        self.assertEqual(memory[0], (2, 2))
        self.assertEqual(set(memory[1:8]), {(4, 0)})
        self.assertEqual(set(memory[8:]), {(0, 4)})
        self.assertTrue(all(c[0] == c[1] == 0 for s in samples[:8] for c in s["pair"]))
        self.assertTrue(any(c[0] or c[1] for c in samples[9]["pair"]))

    def test_retained_state_changes_same_input_counter_response(self):
        off = [phase_oracle(Channel(0, 0, r), u) for r, u in ((2, 1), (2, -1))]
        on = [phase_oracle(Channel(0, 0, r), u) for r, u in ((4, 1), (0, -1))]
        self.assertEqual([x.b for x in off], [0, 0])
        self.assertEqual([x.b for x in on], [1, -1])

    def test_two_authentic_guarded_C_events_with_prescribed_stronger_arrivals(self):
        samples = local_two_arrivals(wait=6, tail=8, amplitude=4)
        events = [s["step"] for s in samples if any(c is not None for c in s["guarded_C"])]
        self.assertEqual(events, [1, 8])
        self.assertEqual(samples[1]["guarded_C"], [1, 2])
        self.assertEqual(samples[8]["guarded_C"], [1, 2])
        self.assertEqual(tuple(x[2] for x in samples[0]["pair"]), (2, 2))
        self.assertEqual(tuple(x[2] for x in samples[1]["pair"]), (4, 0))
        self.assertEqual(tuple(x[2] for x in samples[8]["pair"]), (0, 4))
        self.assertTrue(all(s["guarded_C"] == [None, None] for s in samples[2:8]))

    def test_zero_input_cannot_stop_nonzero_counter_pair(self):
        for old in (Channel(0, 1, 0), Channel(3, -7, 5), Channel(-10**100, 1, 3)):
            state = old
            for k in range(1, 5):
                state = phase_oracle(state, 0)
                self.assertTrue(state.a or state.b)
                self.assertEqual(state == old, k == 4)

    def test_asymmetric_memory_allows_two_unit_arrival_C_events(self):
        pair = (Channel(0, 0, 4), Channel(0, 0, 2))
        memories = [(4, 2)]
        events = []
        for t, sums in enumerate([(1, -1)] + [(0, 0)] * 6 + [(1, -1)] + [(0, 0)] * 8, 1):
            after = tuple(forward(old, u) for old, u in zip(pair, sums))
            classified = tuple(classify(old, new) for old, new in zip(pair, after))
            if any(c is not None for c in classified):
                events.append((t, classified))
            memories.append(tuple(c.r for c in after))
            pair = after
        self.assertEqual(events, [(1, ((1, 1), None)), (8, (None, (2, -1)))])
        self.assertEqual(set(memories[1:8]), {(0, 0)})
        self.assertEqual(set(memories[8:]), {(2, 4)})

    def test_closed_single_channel_period_four_has_no_guarded_C_events(self):
        phases = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for signs in product((-1, 1), repeat=3):
            coupling = Coupling(signs)
            engine = Engine(coupling)
            for side in (3, 5):
                cube = Cube(side)
                center = (side // 2,) * 3
                for g in range(48):
                    source = (*center, g)
                    initial = State(cube, Channel(0, 0, 2), {source: Channel(0, 1, 2)})
                    state = initial
                    recipients = [cube.adjacent(source, d, coupling.ports[d][g]) for d in range(6)]
                    self.assertEqual(len(set(recipients)), 6)
                    for step in range(1, 9):
                        after = engine.advance(state)
                        self.assertEqual(engine.rewind(after), state)
                        self.assertTrue(all(classify(state.at(addr), after.at(addr)) is None
                                            for addr in state.cells.keys() | after.cells.keys()))
                        a, b = phases[step % 4]
                        expected = {source: Channel(a, b, 2)}
                        if step % 4 in (1, 2):
                            expected.update({addr: Channel(0, 0, 2 + 2 * coupling.weights[d][g])
                                             for d, addr in enumerate(recipients)})
                        self.assertEqual(after, State(cube, Channel(0, 0, 2), expected))
                        self.assertEqual(after == initial, step % 4 == 0)
                        state = after

    def test_quadratic_counter_record_identity_and_phase_dependence(self):
        for a, b in product(range(-3, 4), repeat=2):
            for r in range(6):
                for u in range(-8, 9):
                    old = Channel(a, b, r)
                    new = forward(old, u)
                    ell = new.b + old.a
                    self.assertEqual(new.a**2 + new.b**2,
                                     a*a + b*b + ell*ell - 2*a*ell)
                    if u == 0:
                        self.assertEqual(new.a**2 + new.b**2, a*a+b*b)
        for amplitude in range(1, 8):
            growing = forward(Channel(amplitude, 0, 0), -1)
            shrinking = forward(Channel(-amplitude, 0, 0), -1)
            self.assertEqual(growing.a**2+growing.b**2, (amplitude+1)**2)
            self.assertEqual(shrinking.a**2+shrinking.b**2, (amplitude-1)**2)

    def test_central_channel_pair_complement_is_equivariant(self):
        algebra = group()
        ids = {q: i for i, q in enumerate(algebra.quaternions)}
        negative = [ids[tuple(tuple(-x for x in coordinate) for coordinate in q)]
                    for q in algebra.quaternions]
        self.assertEqual(negative[0], 14)
        for signs in product((-1, 1), repeat=3):
            coupling = Coupling(signs)
            for d in range(6):
                for g in range(48):
                    self.assertEqual(coupling.ports[d][negative[g]], negative[coupling.ports[d][g]])
                    self.assertEqual(coupling.weights[d][negative[g]], coupling.weights[d][g])
        for a, b, r, u in product(range(-2, 3), range(-2, 3), (0, 2, 4), range(-6, 7)):
            new = forward(Channel(a, b, r), u)
            companion = forward(Channel(-a, -b, 4-r), -u)
            self.assertEqual(companion, Channel(-new.a, -new.b, 4-new.r))

    def test_paired_rest_is_equivalent_to_bounded_cumulative_input(self):
        for theta in range(3):
            for inputs in product(range(-2, 3), repeat=4):
                pair = (Channel(0, 0, 2*theta), Channel(0, 0, 4-2*theta))
                cumulative = 0
                bounded_through_now = True
                rested_through_now = True
                for u in inputs:
                    cumulative += u
                    bounded_through_now = bounded_through_now and -theta <= cumulative <= 2-theta
                    pair = (forward(pair[0], u), forward(pair[1], -u))
                    rested_through_now = rested_through_now and all(c.a == c.b == 0 for c in pair)
                    self.assertEqual(rested_through_now, bounded_through_now)
                    if rested_through_now:
                        self.assertEqual(pair[0].r, 2*(theta+cumulative))
                        self.assertEqual(pair[1].r, 2*(2-theta-cumulative))


if __name__ == "__main__":
    unittest.main()
