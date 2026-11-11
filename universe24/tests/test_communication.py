"""Independent transport, locality and reception checks for message timing."""
import unittest
import numpy as np

from universe24.core import Engine, State, Tensor, compose
from universe24.core.lattice import DIRECTIONS, ZERO
from universe24.layers.communication import LANES, build_communication
from universe24.layers.one import one_system
from universe24.prepare import vacuum_state
from universe24.prepare.communication import message_seed
from universe24.prepare.one import one_seed
from universe24.observe.communication import incoming_messages


class CommunicationTests(unittest.TestCase):
    def standalone(self, L=5):
        block = build_communication(receiver=None)
        tensor = compose(block, strict_support=True)
        return tensor, Engine(tensor), vacuum_state(tensor, L, block)

    def test_signed_bigint_packets_translate_in_all_six_directions(self):
        tensor, engine, empty = self.standalone()
        empty.r[:] = np.arange(empty.r.size).reshape(empty.r.shape) % 6
        origin = (2, 2, 2)
        values = [(-1 if d % 2 else 1) * ((1 << 90) + d) for d in range(6)]
        seed = message_seed(empty, tensor, [(lane, origin, v) for lane, v in zip(LANES, values)])
        state = seed
        for tick in range(11):
            for d, (direction, value) in enumerate(zip(DIRECTIONS, values)):
                current = tuple((x + tick * dx) % 5 for x, dx in zip(origin, direction))
                previous = tuple((x + (tick - 1) * dx) % 5 for x, dx in zip(origin, direction))
                expected_b = np.zeros(125, dtype=object)
                expected_a = expected_b.copy()
                expected_b[empty.lattice.index(*current)] = value
                expected_a[empty.lattice.index(*previous)] = value
                np.testing.assert_array_equal(state.b[d], expected_b)
                np.testing.assert_array_equal(state.a[d], expected_a)
            np.testing.assert_array_equal(state.r, seed.r)
            if tick < 10:
                state = engine.step(state)
        self.assertTrue(engine.rewind(state, 10).same_as(seed))
        self.assertGreater(engine.stats['pyint_steps'], 0)
        self.assertTrue(empty.same_as(vacuum_with_remainders(empty)))

    def test_empty_network_does_not_tick(self):
        tensor, engine, empty = self.standalone()
        self.assertTrue(engine.run(empty, 17).same_as(empty))
        self.assertEqual(incoming_messages(empty, tensor), [])
        self.assertEqual(len(engine.clicks(empty, engine.step(empty))), 0)

    def test_receiver_changes_only_after_local_arrival(self):
        system = one_system()
        tensor = compose(*system.blocks, strict_support=True)
        engine = Engine(tensor)
        empty = vacuum_state(tensor, 9, *system.blocks)
        origin = (4, 4, 4)
        seed = message_seed(empty, tensor, [('px', origin, 3)])
        initial = seed.copy()
        state, control = seed, empty
        receiver = tensor.gear_index('ref.R00')
        reference = [g for g, name in enumerate(tensor.names) if name.startswith('ref.')]
        no_reception = Tensor(tensor.gears, [m for m in tensor.monomials
                             if not (m.target in reference and any(f.gear >= 48 for f in m.factors))],
                             strict_support=True)
        disconnected = Engine(no_reception)
        silent = seed
        for tick in range(1, 5):
            state, control = engine.step(state), engine.step(control)
            silent = disconnected.step(silent)
            changed = np.any((state.a[reference] != control.a[reference]) |
                             (state.b[reference] != control.b[reference]) |
                             (state.r[reference] != control.r[reference]), axis=0)
            for node in np.flatnonzero(changed):
                xyz = state.lattice.coords(int(node))
                distance = sum(min(abs(x-y), 9-abs(x-y)) for x, y in zip(xyz, origin))
                self.assertLessEqual(distance, tick)
            np.testing.assert_array_equal(silent.b[reference], 0)
            if tick == 1:
                self.assertEqual(int(state.b[receiver, state.lattice.index(5, 4, 4)]), 3)
                self.assertEqual(int(np.count_nonzero(state.b[reference])), 1)
                self.assertEqual(int(state.b[receiver, state.lattice.index(6, 4, 4)]), 0)
        self.assertTrue(engine.rewind(state, 4).same_as(initial))
        self.assertTrue(seed.same_as(initial))

    def test_readout_uses_edges_is_passive_and_is_not_a_click_log(self):
        tensor, engine, empty = self.standalone()
        seed = message_seed(empty, tensor, [('px', (4, 0, 0), 7), ('nz', (0, 0, 0), -2)])
        before = seed.copy()
        records = incoming_messages(seed, tensor)
        self.assertEqual(records, [
            {'lane': 'px', 'source': [4, 0, 0], 'target': [0, 0, 0], 'payload': 7},
            {'lane': 'nz', 'source': [0, 0, 0], 'target': [0, 0, 4], 'payload': -2},
        ])
        self.assertTrue(seed.same_as(before))
        self.assertTrue(engine.step(seed).same_as(engine.step(before)))

    def test_default_is_communication_and_reference_is_explicit(self):
        system = one_system()
        tensor = compose(*system.blocks, strict_support=True)
        self.assertEqual((tensor.G, len(tensor), tensor.rank), (54, 306, 2))
        self.assertEqual(tensor.support_violations(), [])
        self.assertEqual(len(tensor.designations), 6)
        self.assertFalse(any('master' in name or 'cosmic' in name for name in tensor.names))
        seed, report = one_seed(system, tensor, 5)
        self.assertEqual(np.count_nonzero(seed.b[:48]), 0)
        self.assertEqual(np.count_nonzero(seed.b[48:]), 6)
        self.assertEqual(report['rng_seed_used'], False)
        self.assertTrue(Engine(tensor).rewind(Engine(tensor).run(seed, 12), 12).same_as(seed))
        old = one_system(communication=False)
        self.assertEqual(compose(*old.blocks).G, 48)
        with self.assertRaisesRegex(ValueError, 'reference'):
            one_seed(system, tensor, 3, bang='standing')

    def test_superposition_and_invalid_preparations(self):
        tensor, engine, empty = self.standalone()
        seed = message_seed(empty, tensor, [('py', (1, 1, 1), 8), ('py', (1, 1, 1), -3)])
        self.assertEqual(int(seed.b[2, empty.lattice.index(1, 1, 1)]), 5)
        self.assertTrue(engine.rewind(engine.run(seed, 7), 7).same_as(seed))
        for packet in [('bad', (0, 0, 0), 1), ('px', (-1, 0, 0), 1), ('px', (0, 0), 1)]:
            with self.assertRaises(ValueError): message_seed(empty, tensor, [packet])
        for payload in [True, 0.5]:
            with self.assertRaises(TypeError): message_seed(empty, tensor, [('px', (0, 0, 0), payload)])
        with self.assertRaises(ValueError): build_communication(receiver='comm.px')
        with self.assertRaises(TypeError): one_system(communication=1)

    def test_unprepared_history_is_not_silently_projected_to_transport(self):
        tensor, engine, empty = self.standalone()
        seed = message_seed(empty, tensor, [('px', (2, 2, 2), 1)])
        changed = seed.copy()
        changed.a[0, changed.lattice.index(1, 2, 2)] = 0
        self.assertFalse(engine.step(changed).same_as(engine.step(seed)))
        self.assertTrue(engine.inverse_step(engine.step(changed)).same_as(changed))


def vacuum_with_remainders(state):
    z = np.zeros_like(state.a)
    return State(state.L, z, z.copy(), state.r.copy())
