"""Actual C2 arrivals, full-state cones, live background and exact replay."""
import gzip
import json
from pathlib import Path
import tempfile
import unittest
import numpy as np

from universe24.core import Engine, State, Tensor
from universe24.core.lattice import DIRECTIONS
from universe24.layers.causal_wave import with_causal_wave, LANES
from universe24.observe.causal_wave import changed_sites, inside_cone, wave_frame
from universe24.prepare.causal_wave import prepare_causal_wave
from universe24.tests.test_migration import scalar_step


def empty(tensor, L):
    return State(L, *[np.zeros((tensor.G, L**3), dtype=object) for _ in range(3)])


def records(clicks):
    return {(int(g), int(n), int(q), int(k))
            for g, n, q, k in zip(clicks.gear, clicks.node, clicks.quotient, clicks.kind)}


class CausalWaveTests(unittest.TestCase):
    def test_six_directions_exact_arrival_memory_and_rewind(self):
        tensor = with_causal_wave()
        self.assertFalse(tensor.support_violations())
        self.assertEqual(tensor.rank, 3)
        for lane, direction in zip(LANES, DIRECTIONS):
            with self.subTest(lane=lane):
                origin = (0, 0, 0)  # Negative lanes exercise periodic wrap.
                target = tuple((3*d) % 9 for d in direction)
                seed = prepare_causal_wave(empty(tensor, 9), tensor,
                    packets=[(lane, origin, 1)], detectors=[target])
                state, engine = seed, Engine(tensor)
                m, f = (tensor.gear_index('wave.' + n) for n in ('memory', 'response'))
                node = state.lattice.index(*target)
                seen = []
                memory_cycle = []
                for tick in range(1, 8):
                    after = engine.step(state)
                    clicks = engine.clicks(state, after, tick).select('official')
                    seen.extend((tick, int(k)) for g, n, k in zip(clicks.gear, clicks.node, clicks.kind)
                                if g == m and n == node)
                    if tick < 3:
                        self.assertEqual((int(after.a[m, node]), int(after.b[m, node]), int(after.r[m, node])), (0, 0, 2))
                    if tick <= 3:
                        self.assertFalse(np.any(after.b[f]))
                    if tick == 4:
                        self.assertEqual(after.b[f, node], 1)
                    if tick >= 3:
                        memory_cycle.append((int(after.a[m, node]), int(after.b[m, node])))
                    state = after
                self.assertEqual(seen, [(3, 2)])
                self.assertEqual(memory_cycle, [(0, 1), (1, 0), (0, -1), (-1, 0), (0, 1)])
                self.assertTrue(engine.rewind(state, 7).same_as(seed))

    def test_full_state_and_click_differences_stay_inside_cone(self):
        tensor = with_causal_wave()
        engine = Engine(tensor)
        seed = prepare_causal_wave(empty(tensor, 9), tensor,
            packets=[('px', (1, 4, 4), 1)], detectors=[(4, 4, 4)])
        control = prepare_causal_wave(seed, tensor, packets=[], detectors=[(4, 4, 4)])
        footprint = [seed.lattice.coords(n) for n in changed_sites(seed, control)]
        self.assertEqual(set(footprint), {(1, 4, 4), (0, 4, 4)})
        state, other, c2 = seed, control, 0
        for tick in range(1, 7):
            after, after_other = engine.step(state), engine.step(other)
            clicks = engine.clicks(state, after, tick).select('official')
            other_clicks = engine.clicks(other, after_other, tick).select('official')
            affected = changed_sites(after, after_other)
            affected |= {n for _, n, _, _ in records(clicks) ^ records(other_clicks)}
            self.assertTrue(all(inside_cone(seed.lattice, n, footprint, tick) for n in affected))
            c2 += np.count_nonzero(clicks.kind == 2)
            state, other = after, after_other
        self.assertGreater(c2, 0)
        self.assertTrue(engine.rewind(state, 6).same_as(seed))
        self.assertTrue(engine.rewind(other, 6).same_as(control))

    def test_background_keeps_running_before_remote_arrival(self):
        background = Tensor(['background'], [('background', 2, ())])
        tensor = with_causal_wave(background)
        initial = empty(tensor, 9)
        initial.r[0] = 2
        state = prepare_causal_wave(initial, tensor,
            packets=[('px', (0, 4, 4), 1)], detectors=[(3, 4, 4)])
        reference = State(9, initial.a[:1], initial.b[:1], initial.r[:1])
        engine, baseline = Engine(tensor), Engine(background)
        node = state.lattice.index(3, 4, 4)
        for tick in (1, 2):
            after, reference = engine.step(state), baseline.step(reference)
            self.assertFalse(np.array_equal(after.b[0], state.b[0]))
            self.assertTrue(State(9, after.a[:1], after.b[:1], after.r[:1]).same_as(reference))
            clicks = records(engine.clicks(state, after, tick).select('official'))
            if tick == 1:
                self.assertTrue(any(g == 0 and n == node for g, n, _, _ in clicks))
            self.assertEqual(after.b[tensor.gear_index('wave.memory'), node], 0)
            state = after

    def test_actual_memory_drives_response_not_event_callback(self):
        tensor = with_causal_wave()
        data = tensor.to_dict()
        data['monomials'] = [m for m in data['monomials']
                            if not (m[0] == 'wave.response' and any(f[0] == 'wave.memory' for f in m[2]))]
        data['designated_one_way'] = [d for d in data['designated_one_way'] if d[0] != 'wave.response']
        disconnected = Tensor.from_dict(data)
        seed = prepare_causal_wave(empty(tensor, 7), tensor,
            packets=[('px', (0, 3, 3), 1)], detectors=[(3, 3, 3)])
        state, control = seed, seed
        engine, other = Engine(tensor), Engine(disconnected)
        m, f = (tensor.gear_index('wave.' + n) for n in ('memory', 'response'))
        for tick in range(1, 7):
            state, control = engine.step(state), other.step(control)
            self.assertTrue(np.array_equal(state.b[m], control.b[m]))
            self.assertFalse(np.any(control.b[f]))
            self.assertEqual(bool(np.any(state.b[f] != control.b[f])), tick >= 4)

    def test_empty_unmarked_and_cancelling_packets_do_not_trigger(self):
        tensor, engine = with_causal_wave(), Engine(with_causal_wave())
        cases = [([], [(3, 3, 3)]), ([('px', (0, 3, 3), 1)], []),
                 ([('px', (0, 3, 3), 1), ('px', (0, 3, 3), -1)], [(3, 3, 3)])]
        for packets, detectors in cases:
            seed = prepare_causal_wave(empty(tensor, 7), tensor, packets=packets, detectors=detectors)
            final = engine.run(seed, 6)
            for name in ('memory', 'response'):
                g = tensor.gear_index('wave.' + name)
                self.assertFalse(np.any(final.a[g]) or np.any(final.b[g]))
            self.assertTrue(engine.rewind(final, 6).same_as(seed))

    def test_bigint_scalar_oracle_and_unprepared_history(self):
        tensor = with_causal_wave()
        seed = prepare_causal_wave(empty(tensor, 3), tensor,
            packets=[('nx', (0, 0, 0), -(1 << 100) + 1)], detectors=[(2, 0, 0)])
        seed.a[tensor.gear_index('wave.py'), 0] = 17  # No projection onto the prepared sector.
        state, oracle, engine = seed, seed, Engine(tensor)
        for _ in range(4):
            state, oracle = engine.step(state), scalar_step(tensor, oracle)
            self.assertTrue(state.same_as(oracle))
        self.assertTrue(engine.rewind(state, 4).same_as(seed))

    def test_validation_and_passive_observation(self):
        tensor = with_causal_wave()
        seed = empty(tensor, 3)
        for packet in [('bad', (0, 0, 0), 1), ('px', (3, 0, 0), 1), ('px', (0, 0, 0), 1.5)]:
            with self.assertRaises((ValueError, TypeError)):
                prepare_causal_wave(seed, tensor, packets=[packet], detectors=[])
        with self.assertRaises(ValueError):
            with_causal_wave(tensor)
        copied = State.from_dict(seed.to_dict())
        wave_frame(seed, tensor, 0)
        self.assertTrue(seed.same_as(copied))

    def test_einstein_integration_replay_includes_changed_remainders(self):
        from universe24.layers.adm import compile_adm, flat_data
        from universe24.layers.universe import UniverseProgram
        from validation.adm_reference import run, replay_trace
        einstein, parameters = compile_adm(complex_matter=True, dark_matter=True)
        program = UniverseProgram(einstein, parameters, causal_wave=True)
        data = flat_data(3)
        for name in ('chi', 'Pi_chi', 'rho_dark'):
            data[name] = np.zeros((3, 3, 3), dtype=object)
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            report = run(program, data, parameters, out)
            self.assertEqual(report['gears'], einstein.tensor.G + 54 + 9)
            self.assertTrue(report['all_arithmetic_registers_verified'])
            self.assertTrue(report['complete_rewind_exact'])
            self.assertEqual(report['causal_wave']['first_C2_microtick'], 1)
            tensor = Tensor.from_dict(json.loads((out / 'tensor.json').read_text()))
            engine = Engine(tensor)
            saved = iter(replay_trace(out / 'full_trace.jsonl.gz'))
            state = next(saved)
            seed = state
            actual_records, changed_r = [], False
            for tick, after in enumerate(saved, 1):
                self.assertTrue(engine.step(state).same_as(after))
                changed_r |= not np.array_equal(state.r, after.r)
                clicks = engine.clicks(state, after, tick).select('official')
                actual_records.extend([[tick, int(g), int(n), format(int(q), 'x'), int(k)]
                    for g, n, q, k in zip(clicks.gear, clicks.node, clicks.quotient, clicks.kind)])
                state = after
            self.assertTrue(changed_r)
            self.assertTrue(engine.rewind(state, program.ticks).same_as(seed))
            with gzip.open(out / 'official_events.jsonl.gz', 'rt') as stream:
                next(stream)
                self.assertEqual([json.loads(line) for line in stream], actual_records)
            board = json.loads((out / 'event_board.json').read_text())
            self.assertEqual(len(board['causal_wave']['frames']), program.ticks + 1)
            self.assertEqual(board['causal_wave']['frames'][0]['clicks'], [])
            self.assertEqual(board['tensor_fingerprint'], tensor.fingerprint)
            self.assertEqual(report['component_observations']['causal_wave']['C2'],
                             report['causal_wave']['C2_records'])
            wave_start, wave_stop = program.assembly.spans['causal_wave']
            self.assertFalse(any(wave_start <= row[1] < wave_stop for row in actual_records))

    def test_owned_channels_with_all_components_and_budget(self):
        from universe24.algebra.integer_circuit import Circuit
        from universe24.layers.universe import UniverseProgram
        circuit = Circuit()
        x = circuit.input('x')
        einstein = circuit.compile({'0.x': x})
        parameters = {'fields': ['x'], 'steps': 0}
        program = UniverseProgram(einstein, parameters, probe_experiment=True, causal_wave=True)
        manifest = program.channel_manifest()
        owners = {row['owner']: row['channels'] for row in manifest['components']}
        self.assertEqual(owners['causal_wave'], 9)
        self.assertEqual(owners['probe_experiment'], 26)
        self.assertEqual(len(set(program.tensor.names)), program.tensor.G)
        with self.assertRaises(ValueError):
            UniverseProgram(einstein, parameters, probe_experiment=True, causal_wave=True,
                            max_channels=program.tensor.G - 1)
        with self.assertRaises(TypeError):
            UniverseProgram(einstein, parameters, causal_wave=1)
        seed = program.prepare(5, {'x': np.ones((5, 5, 5), dtype=object)})
        after = Engine(program.tensor).step(seed)
        for component in program.assembly.components:
            expected = Engine(component.tensor).step(program.assembly.extract(seed, component.name))
            self.assertTrue(expected.same_as(program.assembly.extract(after, component.name)))
        rows = program.observe_components(seed, after, 1, Engine(program.tensor).clicks(seed, after, 1))
        self.assertIn('probe', rows)
        self.assertIn('causal_wave', rows['components'])


if __name__ == '__main__':
    unittest.main()
