"""Exporter contracts that distinguish generic state recording from a demo view."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from universe24.core import Coupling, Cube, Engine, State
from universe24.core.state import Channel
from universe24.experiments.config import checkpoint_data
from research.presenter.export import (
    MAX_COUNTER_DIGITS, ROOT, ResourceLimitError, bundle, canonical, capture,
    decimal_string, from_trace, parse_decimal, validate_bundle, write_bundle,
)


class PresenterExportTests(unittest.TestCase):
    def test_arbitrary_channel_positions_remainders_and_signed_tensor_are_complete(self):
        side = 5
        cells = {(g % side, (g // side) % side, (g // 25) % side, g):
                 Channel(g - 20, 17 - g, g % 6) for g in range(48)}
        initial = State(Cube(side), Channel(0, 0, 5), cells)
        engine = Engine(Coupling((-1, 1, -1)))
        core_before = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in (ROOT / 'universe24').rglob('*.py')}
        result = capture(engine, initial, 3, start_step=41,
                         view={'position': [4, 3, 2], 'channel': 47})
        self.assertEqual(result['background'], ['0', '0', 5])
        self.assertEqual(result['coupling']['body_signs'], [-1, 1, -1])
        self.assertEqual(result['view'], {'position': [4, 3, 2], 'channel': 47})
        current = initial
        for offset, frame in enumerate(result['frames']):
            expected = [[*addr, str(triple.a), str(triple.b), triple.r]
                        for addr, triple in sorted(current.cells.items())]
            self.assertEqual(frame['cells'], expected)
            self.assertEqual(frame['step'], 41 + offset)
            payload = {'side': side, 'background': ['0', '0', 5], 'cells': expected}
            expected_sha = hashlib.sha256(json.dumps(payload, sort_keys=True,
                separators=(',', ':')).encode('ascii')).hexdigest()
            self.assertEqual(frame['state_sha256'], expected_sha)
            current = engine.advance(current)
        self.assertEqual(initial.cells, cells)
        self.assertTrue(result['provenance']['full_rewind_equal'])
        core_after = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in (ROOT / 'universe24').rglob('*.py')}
        self.assertEqual(core_before, core_after)
        for path, digest in core_before.items():
            self.assertEqual(result['provenance']['source_sha256'][path], digest)
        self.assertEqual(len(bundle([result])['catalog']), 8)

    def test_5001_digit_counters_roundtrip_without_changing_global_guard(self):
        before = sys.get_int_max_str_digits()
        huge = 10**5000 + 123456789
        text = '1' + '0' * 4991 + '123456789'
        self.assertEqual(decimal_string(huge), text)
        self.assertEqual(decimal_string(-huge), '-' + text)
        self.assertEqual(parse_decimal(text), huge)
        self.assertEqual(parse_decimal('-' + text), -huge)
        initial = State(Cube(3), cells={(2, 0, 1, 47): Channel(huge, -huge, 5)})
        recorded = capture(Engine(Coupling((1, -1, 1))), initial, 2)
        self.assertEqual(recorded['frames'][0]['cells'], [[2, 0, 1, 47, text, '-' + text, 5]])
        self.assertEqual(sys.get_int_max_str_digits(), before)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'huge.json'
            write_bundle(path, bundle([recorded]))
            loaded = json.loads(path.read_text())
            self.assertEqual(loaded['experiments'][0]['frames'][0]['cells'][0][4], text)
        self.assertEqual(sys.get_int_max_str_digits(), before)

    def test_complete_native_trace_and_snapshot_import_reject_corruption_and_gaps(self):
        engine = Engine(Coupling((1, -1, -1)))
        initial = State(Cube(5), Channel(0, 0, 1), {(4, 0, 2, 37): Channel(-3, 2, 4)})
        states = list(engine.evolve(initial, 3))
        documents = [checkpoint_data(state, engine, 19 + i) for i, state in enumerate(states)]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'trace.jsonl'
            path.write_text('\n'.join(json.dumps(d) for d in documents) + '\n')
            imported = from_trace(path)
            produced = capture(engine, initial, 3, start_step=19)
            self.assertEqual(imported['frames'], produced['frames'])
            single = Path(tmp) / 'snapshot.json'
            single.write_text(json.dumps(documents[-1], indent=2))
            snap = from_trace(single)
            self.assertEqual(len(snap['frames']), 1)
            self.assertEqual(snap['frames'][0]['audit'], {'forward_equal': None, 'inverse_equal': None})
            path.write_text('\n'.join(json.dumps(documents[i]) for i in (0, 2, 3)))
            with self.assertRaisesRegex(ValueError, 'consecutive'):
                from_trace(path)
            bad = copy.deepcopy(documents)
            bad[1]['experiment']['seed_changes'][0]['state'][2] ^= 1
            path.write_text('\n'.join(json.dumps(d) for d in bad))
            with self.assertRaisesRegex(ValueError, 'forward mismatch'):
                from_trace(path)
            bad = copy.deepcopy(documents)
            bad[1]['coupling_fingerprint'] = '0' * 64
            path.write_text('\n'.join(json.dumps(d) for d in bad))
            with self.assertRaisesRegex(ValueError, 'fingerprint'):
                from_trace(path)

    def test_native_5001_digit_json_literal_and_duplicate_key_rejection(self):
        before = sys.get_int_max_str_digits()
        engine = Engine()
        checkpoint = checkpoint_data(State(Cube(3), cells={(1, 2, 0, 46): Channel(1, 0, 2)}), engine, 0)
        text = json.dumps(checkpoint, separators=(',', ':')).replace('"state":[1,0,2]', '"state":[' + '1' + '0' * 5000 + ',0,2]')
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'huge-native.json'
            path.write_text(text)
            result = from_trace(path)
            self.assertEqual(result['frames'][0]['cells'][0][4], '1' + '0' * 5000)
            self.assertEqual(sys.get_int_max_str_digits(), before)
            path.write_text(text.replace('"completed_steps":0', '"completed_steps":0,"completed_steps":1'))
            with self.assertRaisesRegex(ValueError, 'Duplicate'):
                from_trace(path)

    def test_passive_readouts_are_data_declarations_and_snapshot_hash_has_no_time(self):
        initial = State(Cube(4), Channel(0, 0, 3), {(0, 3, 2, 47): Channel(0, 0, 4)})
        readout = [{'id': 'one-bit', 'label': 'Custom remainder bit', 'kind': 'all_equal',
                    'clauses': [{'address': [0, 3, 2, 47], 'component': 'r', 'equals': '4'}]}]
        with_readout = capture(Engine(), initial, 3, readouts=readout)
        without = capture(Engine(), initial, 3)
        self.assertEqual(with_readout['frames'], without['frames'])
        self.assertEqual(len({f['state_sha256'] for f in without['frames']}), 1)
        self.assertEqual(with_readout['readouts'], readout)
        readout[0]['clauses'][0]['equals'] = '0'
        self.assertEqual(with_readout['readouts'][0]['clauses'][0]['equals'], '4')
        self.assertEqual(initial.at((0, 3, 2, 47)), Channel(0, 0, 4))

    def test_explicit_limits_reject_whole_run_and_writer_never_overwrites(self):
        initial = State(Cube(3), cells={(0, 0, 0, 47): Channel(1, -2, 3)})
        with self.assertRaises(ResourceLimitError):
            capture(Engine(), initial, 3, max_frames=3)
        with self.assertRaises(ResourceLimitError):
            capture(Engine(), initial, 2, max_cells=1)
        with self.assertRaises(ResourceLimitError):
            capture(Engine(), initial, 0, max_bytes=30)
        with self.assertRaises(ResourceLimitError):
            parse_decimal('1' * (MAX_COUNTER_DIGITS + 1))
        data = bundle([capture(Engine(), initial, 1)])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'output.json'
            path.write_bytes(b'original evidence')
            with self.assertRaises(FileExistsError):
                write_bundle(path, data)
            self.assertEqual(path.read_bytes(), b'original evidence')
            path = Path(tmp) / 'invalid.json'
            bad = copy.deepcopy(data)
            bad['experiments'][0]['frames'][1]['cells'][0][4] = '999'
            with self.assertRaises(ValueError):
                write_bundle(path, bad)
            self.assertFalse(path.exists())
            self.assertEqual(sorted(p.name for p in Path(tmp).iterdir()), ['output.json'])
            bool_audit = copy.deepcopy(data)
            bool_audit['experiments'][0]['frames'][1]['audit']['forward_equal'] = 1
            with self.assertRaises(ValueError):
                validate_bundle(bool_audit)

    def test_cli_config_and_checkpoint_continuation_preserve_absolute_steps(self):
        engine = Engine(Coupling((-1, -1, 1)))
        initial = State(Cube(3), cells={(2, 0, 1, 47): Channel(-2, 1, 0)})
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            source = tmp / 'resume.json'
            source.write_text(json.dumps(checkpoint_data(initial, engine, 21)))
            target = tmp / 'presenter.json'
            process = subprocess.run([sys.executable, '-m', 'research.presenter.export',
                '--checkpoint', str(source), '--steps', '2', '--output', str(target)],
                capture_output=True, text=True)
            self.assertEqual(process.returncode, 0, process.stderr)
            exported = json.loads(target.read_text())['experiments'][0]
            self.assertEqual([f['step'] for f in exported['frames']], [21, 22, 23])
            self.assertEqual(exported['coupling']['body_signs'], [-1, -1, 1])
            config = tmp / 'config.json'
            configured = checkpoint_data(initial, engine, 0)['experiment']
            configured['steps'] = 2
            config.write_text(json.dumps(configured))
            config_target = tmp / 'from-config.json'
            configured_run = subprocess.run([sys.executable, '-m', 'research.presenter.export',
                '--config', str(config), '--output', str(config_target)],
                capture_output=True, text=True)
            self.assertEqual(configured_run.returncode, 0, configured_run.stderr)
            from_config = json.loads(config_target.read_text())['experiments'][0]
            self.assertEqual([f['step'] for f in from_config['frames']], [0, 1, 2])
            self.assertEqual([f['cells'] for f in exported['frames']],
                             [f['cells'] for f in from_config['frames']])
            rejected = subprocess.run([sys.executable, '-m', 'research.presenter.export',
                '--checkpoint', str(source), '--steps', '-1', '--output', str(tmp / 'bad.json')],
                capture_output=True, text=True)
            self.assertNotEqual(rejected.returncode, 0)
            self.assertFalse((tmp / 'bad.json').exists())


if __name__ == '__main__':
    unittest.main()
