"""Independent full-register checks of the prepared signal/clock interfaces.

The sparse gather helper uses the separate exact-matrix construction, not the
production scatter, group tables, scalar update or preparation generator.
"""
from itertools import product
from contextlib import contextmanager, redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import tempfile
import time
import unittest

from research.building_blocks.preparation import prepare, pair as published_pair
from research.building_blocks.preparation import memory as published_memory
from research.reference.algebra import DIRECTIONS, coupling as matrix_coupling
from universe24 import Channel, Coupling, Cube, Engine, State


def independent_gather(cells, side, signs=(1, 1, 1)):
    reference = matrix_coupling(tuple(signs))
    inverse_ports = [{sender: receiver for receiver, sender in enumerate(row)}
                     for row in reference.ports]
    old = {address: tuple(value) for address, value in cells.items()}
    background = (0, 0, 2)
    candidates = set(old)
    for (x, y, z, sender), value in old.items():
        if value[1] == 0:
            continue
        for d, (dx, dy, dz) in enumerate(DIRECTIONS):
            candidates.add(((x-dx) % side, (y-dy) % side, (z-dz) % side,
                            inverse_ports[d][sender]))
    result = {}
    for address in candidates:
        x, y, z, receiver = address
        a, b, r = old.get(address, background)
        u = sum(reference.weights[d][receiver] *
                old.get(((x+dx) % side, (y+dy) % side, (z+dz) % side,
                         reference.ports[d][receiver]), background)[1]
                for d, (dx, dy, dz) in enumerate(DIRECTIONS))
        numerator = 2*u+r
        quotient = numerator//6
        value = (b, quotient-a, numerator-6*quotient)
        if value != background:
            result[address] = value
    return result


def independently_prepared_guide(length=8, side=61, source=True,
                                 gap=None, odd_target=None):
    origin = (side//2-length//2, side//2, side//2)
    x, y, z = origin
    cells = {}
    if source:
        cells[x, y, z, 0] = (0, 1, 2)
        cells[x, y, z, 14] = (0, -1, 2)
    for j in range(1, length+1):
        if j == gap:
            continue
        cells[x+j, y, z, 0] = (0, 0, 5 if j == odd_target else 4)
        cells[x+j, y, z, 14] = (0, 0, 0)
    return State(Cube(side), cells=cells), origin


def local_pair(state, origin, site):
    x, y, z = origin
    return state.at((x+site, y, z, 0)), state.at((x+site, y, z, 14))


def memory(state, origin, site):
    pair = local_pair(state, origin, site)
    return int((pair[0].r, pair[1].r) == (0, 4))


def audit_recorded_replay(folder):
    """Independently audit a generated replay against every full checkpoint.

    This optional audit requires an explicitly generated bundle. Normal tests
    do not depend on a pre-existing runs/ directory or saved result fixture.
    """
    folder = Path(folder)
    data = json.loads((folder/'replay_data.json').read_text())
    count = 0
    for scenario in data['scenarios']:
        checkpoints = [json.loads(line) for line in
                       (folder/'cases'/scenario['id']/'states.jsonl').read_text().splitlines()]
        assert len(checkpoints) == len(scenario['frames']) == scenario['steps']+1
        oracle = None
        previous_memory = None
        for t, (checkpoint, frame) in enumerate(zip(checkpoints, scenario['frames'])):
            experiment = checkpoint['experiment']
            assert experiment['background'] == [0, 0, 2]
            assert experiment['side'] == scenario['side']
            assert experiment['coupling_signs'] == scenario['signs']
            assert checkpoint['completed_steps'] == frame['t'] == t
            cells = {tuple(row['position'])+(row['channel'],): tuple(row['state'])
                     for row in experiment['seed_changes']}
            assert len(cells) == len(experiment['seed_changes'])
            if oracle is not None:
                oracle = independent_gather(oracle, experiment['side'],
                                            tuple(experiment['coupling_signs']))
                assert oracle == cells, (scenario['id'], t)
                count += 1
            else:
                oracle = cells
            raw = json.dumps(checkpoint, sort_keys=True, separators=(',', ':'),
                             ensure_ascii=True).encode()
            assert hashlib.sha256(raw).hexdigest() == frame['state_hash']
            assert len(cells) == frame['active_channels']
            bits = []
            for index, site in enumerate(scenario['sites']):
                values = [list(cells.get(tuple(site['position'])+(g,), (0, 0, 2)))
                          for g in (0, 14)]
                assert values == frame['cells'][index]
                bit = int(values[0][2] == 0 and values[1][2] == 4)
                assert bit == frame['memory'][index]
                bits.append(bit)
            expected_clicks = ([] if previous_memory is None else
                               [site['index'] for index, site in enumerate(scenario['sites'])
                                if bits[index] and not previous_memory[index]])
            assert expected_clicks == frame['clicks']
            previous_memory = bits
    return {'scenarios': len(data['scenarios']), 'independent_complete_updates': count}


@contextmanager
def freshly_generated_bundle():
    """Keep mutation controls separate from retained scientific evidence."""
    from research.building_blocks.run import main
    scratch = Path(__file__).resolve().parents[1]/'runs'
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='review-integrity-', dir=scratch) as folder:
        output = Path(folder)/'bundle'
        with redirect_stdout(io.StringIO()):
            status = main(['--output', str(output), '--skip-viewer'])
        assert status == 1  # The unchanged no-transfer hypothesis fails.
        yield output


class BuildingBlocksIndependentReviewTests(unittest.TestCase):
    def test_verifier_rejects_corrupted_display_and_geometry(self):
        from research.building_blocks.verify_bundle import verify
        with freshly_generated_bundle() as folder:
            self.assertEqual(verify(folder)['verification'], 'passed')
            path = folder/'replay_data.json'
            original = path.read_text()
            data = json.loads(original)
            data['scenarios'][0]['frames'][6]['memory'][6] = 0
            path.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                verify(folder)
            data = json.loads(original)
            data['scenarios'][0]['sites'][6]['position'][0] += 1
            path.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                verify(folder)

    def test_verifier_rejects_corrupted_full_state_and_missing_source_identity(self):
        from research.building_blocks.verify_bundle import verify
        with freshly_generated_bundle() as folder:
            self.assertEqual(verify(folder)['verification'], 'passed')
            path = folder/'cases'/'guide_N24'/'states.jsonl'
            original = path.read_text()
            lines = original.splitlines()
            checkpoint = json.loads(lines[6])
            checkpoint['experiment']['seed_changes'][0]['state'][2] ^= 1
            lines[6] = json.dumps(checkpoint)
            path.write_text('\n'.join(lines)+'\n')
            with self.assertRaises(ValueError):
                verify(folder)
            path.write_text(original)
            path = folder/'manifest.json'
            manifest = json.loads(path.read_text())
            del manifest['source_sha256']['research/clockwork/viewer.html']
            path.write_text(json.dumps(manifest))
            with self.assertRaises(ValueError):
                verify(folder)

    def test_short_run_cannot_certify_unsampled_retention_window(self):
        from research.building_blocks.run import run_case
        # Every receiver has activated by t=8, but detector 2's required
        # retention endpoint is t=16. A clipped sample range must not pass.
        case = {'id': 'short_review_control', 'title': 'Short retention control',
                'kind': 'negative_control', 'N': 8, 'side': 61, 'steps': 8,
                'detectors': [2], 'mode': 'guide'}
        scratch = Path(__file__).resolve().parents[1]/'runs'
        scratch.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='review-horizon-', dir=scratch) as folder:
            try:
                _, result = run_case(case, Path(folder), time.process_time(),
                                     {'cpu_seconds': 120, 'max_sparse_channels': 20000})
            except ValueError:
                return  # Rejecting a malformed acceptance horizon is valid.
            self.assertFalse(result['accepted'])

    def test_initial_gap_can_leak_later_in_the_registered_long_run(self):
        initial, origin = independently_prepared_guide(length=24, side=151, gap=10)
        states = list(Engine(Coupling()).evolve(initial, 56))
        first = next(t for t, state in enumerate(states)
                     if local_pair(state, origin, 12)[0].b != 0)
        bits = [memory(state, origin, 12) for state in states]
        clicks = [t for t in range(1, len(bits)) if bits[t] and not bits[t-1]]
        self.assertEqual(first, 32)
        self.assertEqual(clicks, [32, 38, 42, 50])
        # This is a negative regression for the frozen no-transfer hypothesis,
        # not a new successful clutch interpretation or a shorter time window.

    def test_registered_preparations_and_readouts_match_independent_definitions(self):
        root = Path(__file__).resolve().parents[1]
        protocol = json.loads((root/'research/building_blocks/protocol.json').read_text())
        for case in protocol['cases']:
            with self.subTest(case=case['id']):
                options = {'length': case['N'], 'side': case['side']}
                if case['mode'] == 'no_source':
                    options['source'] = False
                if case['mode'] == 'gap':
                    options['gap'] = case['gap']
                if case['mode'] == 'odd_remainder':
                    options['odd_target'] = case['perturb_at']
                expected, expected_origin = independently_prepared_guide(**options)
                if case['mode'] == 'source_only':
                    x, y, z = expected_origin
                    expected = State(expected.cube, cells={
                        (x, y, z, 0): (0, 1, 2), (x, y, z, 14): (0, -1, 2)})
                engine, state, origin = prepare(case)
                self.assertEqual(state, expected)
                self.assertEqual(origin, expected_origin)
                self.assertEqual(engine.coupling.body_signs, (1, 1, 1))
                for _ in range(4):
                    original_cells = dict(state.cells)
                    plain_next = engine.advance(state)
                    for j in range(case['N']+1):
                        self.assertEqual(published_pair(state, origin, j), local_pair(state, origin, j))
                        self.assertEqual(published_memory(published_pair(state, origin, j)),
                                         memory(state, origin, j))
                    self.assertEqual(dict(state.cells), original_cells)
                    self.assertEqual(engine.advance(state), plain_next)
                    state = plain_next
        # A phase-only predicate would silently accept a different parity
        # sector. The registered exact remainder predicate must not do that.
        self.assertEqual(published_memory((Channel(0, 1, 1), Channel(0, -1, 5))), 0)
        self.assertEqual(published_memory((Channel(0, 1, 0), Channel(0, -1, 4))), 1)

    def test_all_zero_counters_are_static_for_all_signed_tensors(self):
        # Remainder-only apparatus contains genuine retained state, but cannot
        # self-start: u=0 and 0<=r<6 imply quotient=0 and r_next=r.
        cells = {(1, 1, 1, g): (0, 0, g % 6) for g in range(48)}
        initial = State(Cube(3), cells=cells)
        for signs in product((-1, 1), repeat=3):
            with self.subTest(signs=signs):
                engine = Engine(Coupling(signs))
                state = initial
                for _ in range(4):
                    state = engine.advance(state)
                    self.assertEqual(state, initial)
                    self.assertEqual(independent_gather(state.cells, 3, signs),
                                     dict(initial.cells))

    def test_full_guide_and_controls_match_independent_matrix_gather(self):
        # L61 gives initial minimum boundary margin 26 > the 24-step horizon.
        for options in ({}, {"source": False}, {"gap": 3}, {"odd_target": 2}):
            with self.subTest(options=options):
                initial, _ = independently_prepared_guide(**options)
                engine = Engine(Coupling())
                state = initial
                oracle = dict(initial.cells)
                for step in range(1, 25):
                    previous = state
                    state = engine.advance(state)
                    oracle = independent_gather(oracle, initial.cube.side)
                    self.assertEqual(dict(state.cells), oracle, f"step {step}")
                    self.assertEqual(engine.rewind(state), previous)
                for _ in range(24):
                    state = engine.rewind(state)
                self.assertEqual(state, initial)

    def test_record_window_and_signal_started_clock_do_not_claim_power_flow(self):
        initial, origin = independently_prepared_guide()
        engine = Engine(Coupling())
        trajectory = list(engine.evolve(initial, 24))
        first_arrivals = [next(t for t, state in enumerate(trajectory)
                               if local_pair(state, origin, j)[0].b != 0)
                          for j in range(1, 9)]
        self.assertEqual(first_arrivals, list(range(1, 9)))
        bits = [memory(state, origin, 2) for state in trajectory]
        self.assertEqual(bits[0:16], [0, 0]+[1]*14)
        self.assertEqual(bits[16], 0)
        self.assertEqual(bits[20], 1)  # Later click defeats permanent/one-shot claims.
        cycle = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        address = (origin[0]+2, origin[1], origin[2], 0)
        for t in range(2, 16):
            self.assertEqual(tuple(local_pair(trajectory[t], origin, 2)[0][:2]),
                             cycle[(t-2) % 4])
        # Several clock rotations have no contemporaneous net input; this
        # certifies triggering rather than continuous incoming power.
        self.assertEqual([engine.input_sums(trajectory[t]).get(address, 0)
                          for t in range(2, 10)], [0]*8)

    def test_parity_and_missing_receiver_are_real_failures_of_fixed_interface(self):
        engine = Engine(Coupling())
        odd, origin = independently_prepared_guide(odd_target=2)
        odd_path = list(engine.evolve(odd, 24))
        self.assertTrue(any(local_pair(s, origin, 2)[0].b for s in odd_path))
        self.assertFalse(any(memory(s, origin, 2) for s in odd_path))
        self.assertTrue(all(local_pair(s, origin, 2)[0].r % 2 == 1
                            for s in odd_path))
        gap, origin = independently_prepared_guide(gap=3)
        gap_path = list(engine.evolve(gap, 24))
        self.assertFalse(any(memory(s, origin, 4) for s in gap_path))
        # A renderer/exporter that drops zero-counter entries loses the initial
        # guide itself, even though it can look empty in a counter-only plot.
        retained = dict(gap.cells)
        counter_only = {a: s for a, s in retained.items() if s.a or s.b}
        self.assertNotEqual(counter_only, retained)


if __name__ == "__main__":
    unittest.main()
