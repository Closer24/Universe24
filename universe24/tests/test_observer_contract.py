"""Click-only inference uses explicit calibration, never hidden state access."""
from copy import deepcopy
import gzip
import hashlib
from pathlib import Path
import tempfile
import unittest

from universe24.core import Engine, exact_json
from universe24.model import make_model_bundle
from universe24.observer import (read_clicks, observed_payload, inspect_click_file,
                                 reconstruct_channel_from_clicks)
from universe24.system.checks import fixture
from universe24.system.decoder import make_transition, decode_transition


class ClickObserverContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = make_model_bundle(L=3, pattern='burst')
        cls.channel = 0
        engine, state = Engine(cls.bundle.tensor), cls.bundle.seed
        cls.initial_a = [int(v) for v in state.a[cls.channel]]
        cls.initial_b = [int(v) for v in state.b[cls.channel]]
        cls.records, cls.other_records, cls.values = [], [], []
        cls.expected_changes, cls.nonquiet_keys = [], set()
        for tick in range(1, 6):
            after = engine.step(state)
            for run_id, target in [('observer-contract', cls.records),
                                   ('another-run', cls.other_records)]:
                transition = make_transition(cls.bundle.tensor, state, after,
                                             run_id=run_id, step=tick)
                target.extend(decode_transition(transition, cls.bundle.tensor))
            cls.values.append([str(int(v)) for v in after.b[cls.channel]])
            for node, (old, current, value) in enumerate(zip(state.a[cls.channel],
                                                           state.b[cls.channel],
                                                           after.b[cls.channel])):
                if old != current:
                    cls.nonquiet_keys.add((tick, node, cls.channel))
                if current != value:
                    cls.expected_changes.append((tick, node, str(int(current)), str(int(value))))
            state = after

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.path = Path(self.temporary.name) / 'clicks.jsonl.gz'

    def write_records(self, records):
        with gzip.open(self.path, 'wt', encoding='utf-8') as stream:
            for record in records:
                stream.write(exact_json.dumps(record) + '\n')

    def observe(self, **kwargs):
        calibration = dict(channel=self.channel, node_count=27, steps=5,
                           initial_a=self.initial_a, initial_b=self.initial_b)
        calibration.update(kwargs)
        return reconstruct_channel_from_clicks(self.path, **calibration)

    def test_click_file_recovers_calibrated_channel_and_quiet_intervals(self):
        self.write_records(self.records)
        before = self.path.read_bytes()
        observed = self.observe()
        self.assertEqual(observed['values_by_step'], self.values)
        self.assertEqual([(e['step'], e['node'], e['before'], e['after'])
                          for e in observed['changes']], self.expected_changes)
        self.assertTrue(observed['changes'])
        self.assertTrue(all(e['arithmetic_event_id'] for e in observed['changes']))
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(list(Path(self.temporary.name).iterdir()), [self.path])
        self.assertEqual(inspect_click_file(self.path)['events'], len(self.records))

    def test_cross_run_projection_excludes_only_provenance(self):
        self.assertNotEqual(self.records, self.other_records)
        self.assertEqual(observed_payload(self.records), observed_payload(self.other_records))
        changed = deepcopy(self.records)
        changed[0]['quotient'] += 1
        self.assertNotEqual(observed_payload(self.records), observed_payload(changed))
        self.assertIn('quotient', observed_payload(self.records)[0])

    def test_mixed_run_and_duplicate_records_are_rejected(self):
        for records in (self.records + self.other_records, self.records + self.records):
            self.write_records(records)
            with self.assertRaises(ValueError):
                self.observe()

    def test_reordered_events_are_rejected(self):
        records = deepcopy(self.records)
        records[0], records[1] = records[1], records[0]
        self.write_records(records)
        with self.assertRaisesRegex(ValueError, 'canonical chronological order'):
            read_clicks(self.path)

    def test_mixed_tensor_and_uncalibrated_law_are_rejected(self):
        changed = deepcopy(self.records)
        other_hash = fixture().tensor.fingerprint
        for record in changed:
            record['tensor_hash'] = other_hash
            identity = {key: record[key] for key in ('run_id', 'tensor_hash', 'step', 'node', 'channel')}
            record['event_id'] = hashlib.sha256(exact_json.dumps(identity, sort_keys=True).encode('ascii')).hexdigest()
        self.write_records(self.records + changed)
        with self.assertRaises(ValueError):
            read_clicks(self.path)
        self.write_records(changed)
        with self.assertRaises(ValueError):
            self.observe()

    def test_malformed_json_fields_and_sign_are_rejected(self):
        serialized = exact_json.dumps(self.records[0])
        duplicate_key = '{"step":999,' + serialized[1:]
        with gzip.open(self.path, 'wt', encoding='utf-8') as stream:
            stream.write(duplicate_key + '\n')
        with self.assertRaisesRegex(ValueError, 'duplicate click JSON field'):
            read_clicks(self.path)
        records = deepcopy(self.records)
        records[0]['sign'] = -1
        self.write_records(records)
        with self.assertRaises(ValueError):
            read_clicks(self.path)

    def test_calibration_bounds_exact_inputs_and_positive_history_enforced(self):
        self.write_records(self.records)
        for calibration in ({'steps': 1}, {'node_count': 1}, {'channel': True},
                            {'steps': -1}, {'channel': 48}, {'initial_a': 0},
                            {'initial_b': 1.5}, {'initial_a': [1] * 26},
                            {'initial_b': [True] * 27}):
            with self.subTest(calibration=calibration), self.assertRaises(ValueError):
                self.observe(**calibration)
        records = deepcopy(self.records)
        event = next(e for e in records if e['channel'] == self.channel)
        event['quotient'] = 1
        self.write_records(records)
        with self.assertRaises(ValueError):
            self.observe()

    def test_missing_nonquiet_channel_record_is_not_invented_as_silence(self):
        key = next((e['step'], e['node'], e['channel']) for e in self.records
                   if (e['step'], e['node'], e['channel']) in self.nonquiet_keys)
        incomplete = [e for e in self.records if (e['step'], e['node'], e['channel']) != key]
        self.write_records(incomplete)
        with self.assertRaises(ValueError):
            self.observe()

    def test_unbounded_integer_observations_do_not_change_global_digit_limits(self):
        import sys
        limit = sys.get_int_max_str_digits()
        record = deepcopy(next(e for e in self.records
                               if e['step'] == 1 and e['channel'] == self.channel))
        record['quotient'] = 10 ** 5000 + 1
        self.write_records([record])
        result = self.observe(steps=1, initial_a=1, initial_b=1)
        self.assertEqual(result['changes'][0]['after'], '1' + '0' * 5000)
        self.assertEqual(result['values_by_step'][0][record['node']], '1' + '0' * 5000)
        self.assertEqual(inspect_click_file(self.path)['signed_quotient_sum'], '1' + '0' * 4999 + '1')
        self.assertEqual(sys.get_int_max_str_digits(), limit)


if __name__ == '__main__':
    unittest.main()
