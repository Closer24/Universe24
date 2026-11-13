"""A replay board consumes saved clicks and declared initial calibration only."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
from unittest.mock import patch


from universe24.board import board_data, build_board, _script_json
from universe24.core import Engine, State, Tensor, GearType
from universe24.model import make_model_bundle, sector_map
from universe24.system.bundle import create_bundle
from universe24.system.runtime import run_bundle


class BoardContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.bundle = make_model_bundle(L=3)
        self.run = self.root / 'run'
        self.report = run_bundle(self.bundle, self.run, 3)

    def test_frames_match_recorded_states_without_trace_or_engine_access(self):
        from universe24.load import face_load_profile
        state, engine = self.bundle.seed, Engine(self.bundle.tensor)
        expected = [face_load_profile(state.b, state.L)]
        for _ in range(3):
            state = engine.step(state)
            expected.append(face_load_profile(state.b, state.L))
        (self.run / 'full_trace.jsonl.gz').unlink()
        with (patch('universe24.core.Engine.step', side_effect=AssertionError('second engine')),
              patch('universe24.system.runtime.verify_run', side_effect=AssertionError('hidden replay'))):
            data = board_data(self.run)
        self.assertEqual([frame['load'] for frame in data['frames']], expected)
        self.assertEqual(sum(frame['clicks'] for frame in data['frames']), self.report['click_count'])
        self.assertIn('public calibration', data['calibration'])
        self.assertTrue(data['calibration_sector_verified'])
        self.assertTrue(data['initial_inverse_oracle_checked'])
        self.assertIn('full trace is not opened', data['integrity'].lower())
        self.assertEqual(data['physics']['ordinary_matter'], 'Not established')
        self.assertEqual(data['physics']['dark_matter'], 'Not established')
        self.assertEqual(data['physics']['einstein_geometry'], 'Not established')

    def test_standalone_html_contains_only_recorded_frames_and_no_external_fetch(self):
        output = self.root / 'board.html'
        result = build_board(self.run, output)
        html = output.read_text()
        self.assertFalse(result['browser_evolution'])
        self.assertFalse(result['full_trace_opened'])
        self.assertIn('PASSIVE CLICK REPLAY', html)
        self.assertIn('const data=JSON.parse', html)
        self.assertNotIn('fetch(', html)
        self.assertNotIn('src="http', html)
        self.assertNotIn('full_trace.jsonl.gz', html)
        self.assertIn('Dark matter', html)
        self.assertIn('Not established', html)
        payload = html.split('id="board-data">', 1)[1].split('</script>', 1)[0]
        data = json.loads(payload)
        self.assertEqual(len(data['frames']), 4)
        self.assertEqual(data['nodes'], 27)

    def test_existing_output_is_preserved_before_inputs_are_read(self):
        output = self.root / 'existing.html'
        output.write_text('preserve me')
        with patch('universe24.board.board_data', side_effect=AssertionError('read unnecessary inputs')):
            with self.assertRaises(ValueError):
                build_board('missing', output)
        self.assertEqual(output.read_text(), 'preserve me')

    def test_report_identity_and_click_corruption_are_rejected(self):
        report_path = self.run / 'validation.json'
        original = json.loads(report_path.read_text())
        for key, value in [('run_id', 'wrong'), ('tensor_hash', 'wrong'), ('steps', -1),
                           ('nodes', 99), ('click_count', 999999), ('files', None)]:
            report = deepcopy(original)
            report[key] = value
            report_path.write_text(json.dumps(report))
            with self.subTest(key=key), self.assertRaises(ValueError):
                board_data(self.run)
        report_path.write_text(json.dumps(original))
        with (self.run / 'clicks.jsonl.gz').open('ab') as stream:
            stream.write(b'corrupt')
        with self.assertRaisesRegex(ValueError, 'checksum'):
            board_data(self.run)

    def test_foreign_tensor_rejected_even_without_clicks_or_updates(self):
        law = Tensor([GearType(f'stationary{g}', 'official') for g in range(48)],
                     [(g, 6, [(g, (0, 0, 0), 'b')]) for g in range(48)], strict_support=True)
        values = np.ones((48, 27), dtype=int)
        seed = State(3, values.copy(), values.copy(), values.copy())
        channels = [{'index':g, 'name':gear.name, 'label':gear.label,
                     'owner':'stationary test', 'purpose':'no capacity scattering'}
                    for g, gear in enumerate(law.gears)]
        foreign = create_bundle(law, seed, channels=channels, protocol=self.bundle.protocol,
                                model={'id':'foreign-stationary', 'version':'1',
                                       'domain':'stationary positive state', 'role':'research'})
        for steps in (0, 2):
            directory = self.root / f'foreign-{steps}'
            report = run_bundle(foreign, directory, steps)
            self.assertEqual(report['click_count'], 0)
            with self.subTest(steps=steps), self.assertRaisesRegex(ValueError, 'coupling'):
                board_data(directory)

    def test_invalid_raw_calibration_and_reverse_history_branch_are_rejected(self):
        original = self.bundle.seed
        for kind in ('old-nonboolean', 'current-nonboolean', 'zero-carry', 'reverse-branch'):
            a, b, r = original.a.copy(), original.b.copy(), original.r.copy()
            if kind == 'old-nonboolean':
                a[0, 0] = 3
            elif kind == 'current-nonboolean':
                b[0, 0] = 3
            elif kind == 'zero-carry':
                r[0, 0] = 0
            else:
                a = sector_map(b, original.L)
                self.assertFalse(np.array_equal(a, original.a))
            seed = State(original.L, a, b, r)
            bundle = create_bundle(self.bundle.tensor, seed, channels=self.bundle.channels,
                                   protocol=self.bundle.protocol, model=self.bundle.model)
            directory = self.root / kind
            # A valid generic replay can still be outside the board's narrower
            # forward sector. The reverse branch stays Boolean for these steps.
            report = run_bundle(bundle, directory, 2 if kind == 'reverse-branch' else 0)
            self.assertEqual(report['checks']['complete_state_rewind_to_seed'], 'passed')
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                board_data(directory)

    def test_json_script_escaping_roundtrips_untrusted_metadata(self):
        malicious = '</script><script>alert("x")</script>&\u2028'
        rendered = _script_json({'model': malicious})
        self.assertNotIn('<', rendered)
        self.assertNotIn('>', rendered)
        self.assertNotIn('&', rendered)
        self.assertEqual(json.loads(rendered), {'model': malicious})
        model = dict(self.bundle.model)
        model['id'] = malicious
        bundle = create_bundle(self.bundle.tensor, self.bundle.seed,
                               channels=self.bundle.channels, protocol=self.bundle.protocol,
                               model=model)
        run_bundle(bundle, self.root / 'untrusted-run', 0)
        output = self.root / 'escaped.html'
        build_board(self.root / 'untrusted-run', output)
        self.assertNotIn(malicious, output.read_text())
        self.assertIn('\\u003c/script\\u003e', output.read_text())


if __name__ == '__main__':
    unittest.main()
